import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from distutils import util
from functools import partial
from typing import Any, Dict, FrozenSet, List, Optional, Tuple, Union, cast

import ulid
from chtoolset import query as chquery
from croniter import croniter
from packaging import version
from pydantic import ValidationError
from tornado.concurrent import run_on_executor
from tornado.escape import json_decode
from tornado.web import url

from tinybird.ch_utils.engine import engine_full_from_dict
from tinybird.ch_utils.user_profiles import WorkspaceUserProfiles
from tinybird.connector_settings import DataConnectors
from tinybird.constants import MATVIEW_BACKFILL_VALUE_WAIT, ExecutionTypes
from tinybird.copy_pipes.job import cancel_pipe_copy_jobs, new_copy_job
from tinybird.copy_pipes.validation import (
    get_copy_datasource_definition,
    validate_copy_pipe,
    validate_copy_pipe_or_raise,
    validate_gcs_cron_expression,
)
from tinybird.data_connector import DataConnectorNotFound, DataSink, ResourceNotConnected
from tinybird.data_sinks.config import WriteStrategy
from tinybird.data_sinks.validation import validate_sink_pipe
from tinybird.feature_flags import FeatureFlagsWorkspaceService, FeatureFlagWorkspaces
from tinybird.gc_scheduler.constants import DEFAULT_TIMEZONE, GCloudScheduleException
from tinybird.gc_scheduler.sinks import (
    create_copy_schedule_sink,
    pause_sink,
    remove_schedule_data_sink,
    resume_sink,
    update_copy_sink,
)
from tinybird.integrations.dynamodb.sync_job import DynamoDBSyncJob
from tinybird.iterating.branching_modes import BRANCH_MODES, BranchMode
from tinybird.job import (
    Job,
    JobAlreadyBeingCancelledException,
    JobExecutor,
    JobKind,
    JobNotInCancellableStatusException,
    JobStatus,
)
from tinybird.limits import Limits
from tinybird.plan_limits.copy import CopyLimits
from tinybird.populates.job import (
    PopulateException,
    PopulateJob,
    get_populate_subset,
    new_populate_job,
    validate_populate_condition,
)
from tinybird.protips import ProTipsService
from tinybird.tornado_template import ParseError, UnClosedIfError
from tinybird.validation_utils import handle_pydantic_errors
from tinybird.views.api_errors.pipes import (
    AppendNodeError,
    ChartError,
    CopyError,
    CopyNodeError,
    DataSinkError,
    PipeClientErrorForbidden,
    PipeClientErrorNotFound,
    PipeDefinitionError,
    SQLPipeError,
    process_syntax_error,
)
from tinybird.views.api_pipes_datasinks import APIPipeNodeSinkHandler, APIPipeSinkHandler, create_data_sink_pipe
from tinybird.views.api_pipes_datasinks import NodeUtils as SinkNodeUtils
from tinybird.views.api_pipes_stream import APIPipeNodeStreamHandler, StreamNodeUtils
from tinybird.views.entities_datafiles import generate_pipe_datafile
from tinybird.views.shared.utils import CopyException, SQLUtils
from tinybird.views.utils import is_table_function_in_error, validate_table_function_host
from tinybird_shared.clickhouse.errors import CHErrors, is_user_error

from .. import tracker
from ..ch import (
    CHTable,
    CHTableLocation,
    HTTPClient,
    ch_alter_table_modify_query,
    ch_create_materialized_view,
    ch_table_details_async,
)
from ..ch_utils.exceptions import CHException
from ..chart import Chart
from ..datasource import Datasource
from ..hook import (
    CreateDatasourceHook,
    DeleteCompleteDatasourceHook,
    LandingDatasourceHook,
    LastDateDatasourceHook,
    PGSyncDatasourceHook,
)
from ..limits import Limit
from ..materialized import AnalyzeException, Materialized
from ..matview_checks import SQLValidationException
from ..pg import PGService
from ..pipe import (
    CopyModes,
    DependentMaterializedNodeException,
    DependentMaterializedNodeOnUpdateException,
    EndpointNodesCantBeDropped,
    NodeNotFound,
    NodeValidationException,
    Pipe,
    PipeNode,
    PipeNodeTypes,
    PipeTypes,
    PipeValidationException,
)
from ..resource import ForbiddenWordException, Resource
from ..sql import engine_patch_replicated_engine, schema_to_sql_columns
from ..sql_template import SQLTemplateCustomError, SQLTemplateException, TemplateExecutionResults, render_sql_template
from ..table import create_table_from_schema, drop_table
from ..timing import Timer
from ..tokens import AccessToken, scopes
from ..tracker import OpsLogEntry
from ..user import (
    CopyNodeNotFound,
    EndpointNotFound,
    PipeIsCopy,
    PipeIsMaterialized,
    PipeIsNotDefault,
    PipeNotFound,
    QueryNotAllowed,
    ResourceAlreadyExists,
    ServicesDataSourcesError,
    User,
    Users,
)
from .api_errors.datasources import (
    ClientErrorBadRequest,
    ClientErrorConflict,
    ClientErrorForbidden,
    ServerErrorInternal,
)
from .api_query import APIQueryHandler
from .base import (
    ApiHTTPError,
    BaseHandler,
    _calculate_edited_by,
    authenticated,
    check_endpoint_concurrency_limit,
    check_endpoint_rps_limit,
    check_organization_limit,
    check_plan_limit,
    check_workspace_limit,
    read_only_from_ui,
    requires_write_access,
    with_scope,
)
from .openapi import OpenAPIExampleTypes, generate_openapi_endpoints_response
from .shared.utils import DataSourceUtils as SharedDataSourceUtils
from .shared.utils import NodeUtils as SharedNodeUtils
from .utils import filter_query_variables, get_variables_for_query, validate_sql_parameter

LAST_JOBS_TO_CANCEL = 100
MAX_DATA_SIZE_TO_STORE_IN_NODE = 500 * 1024  # 0.5Mb
ROW_DEFAULT_LIMIT = 342  # 342 becuase is the number of 15 minute chunks in a month
VALID_NODE_KEYS = (
    "datasource",
    "description",
    "engine_settings",
    "engine",
    "ignore_sql_errors",
    "materialized",
    "name",
    "override_datasource",
    "populate_condition",
    "populate_subset",
    "populate",
    "sql",
    "type",
    "with_staging",
)

VALID_NODE_COPY_KEYS = ("datasource", "target_datasource", "description", "ignore_sql_errors", "name", "sql")


@dataclass
class SourceTable:
    database: str
    table: str


@dataclass()
class NodeUtils:
    @staticmethod
    async def create_endpoint(
        workspace: User,
        pipe_name_or_id: str,
        node_name_or_id: str,
        edited_by: Optional[str],
        ignore_sql_errors: bool = False,
        api_host: str = "",
        is_cli: bool = False,
    ) -> Dict[str, Any]:
        try:
            pipe = workspace.get_pipe(pipe_name_or_id)
            if not pipe:
                raise PipeNotFound()
            # check if pipe has an endpoint node
            endpoint_nodes = [
                node
                for node in pipe.pipeline.nodes
                if node.node_type == PipeNodeTypes.ENDPOINT and node.name != node_name_or_id
            ]
            # if so un-publish the node as an endpoint
            if len(endpoint_nodes) == 1:
                existing_endpoint_node: PipeNode = endpoint_nodes[0]
                pipe = await NodeUtils.drop_endpoint(
                    workspace, existing_endpoint_node.id, pipe.id, edited_by, ignore_sql_errors, pipe
                )

            # create the new node as the endpoint
            if node_name_or_id:
                node: Optional[PipeNode] = pipe.pipeline.get_node(node_name_or_id)
                if node:
                    node.ignore_sql_errors = bool(ignore_sql_errors)
                    if not ignore_sql_errors:
                        try:
                            await SharedNodeUtils.validate_node_sql(workspace, pipe, node)
                        except ForbiddenWordException as e:
                            raise ApiHTTPError(
                                403, str(e), documentation="/api-reference/api-reference.html#forbidden-names"
                            )

                    try:
                        if not node.materialized:
                            await Users.check_dependent_nodes_by_materialized_node(workspace, node.id)
                    except DependentMaterializedNodeOnUpdateException as e:
                        logging.warning(
                            f"DependentMaterializedNodeOnUpdateException {str(e)} - ws: {workspace.id} - node: {node.id} - pipe: {pipe.id}"
                        )
                        raise ApiHTTPError(403, str(e))
                    except Exception as e:
                        logging.exception(
                            f"DependentMaterializedNodeOnUpdateException {str(e)} - ws: {workspace.id} - node: {node.id} - pipe: {pipe.id}"
                        )
            workspace = await Users.set_node_of_pipe_as_endpoint_async(
                workspace.id, pipe_name_or_id, node_name_or_id, edited_by
            )
        except PipeNotFound:
            raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))
        except NodeNotFound:
            raise ApiHTTPError(400, f"Pipe '{pipe_name_or_id}' does not contain the '{node_name_or_id}' node")
        except PipeIsMaterialized as e:
            raise ApiHTTPError(403, str(e))
        except PipeIsCopy as e:
            if is_cli:
                pass
            else:
                raise ApiHTTPError(403, str(e))
        except PipeIsNotDefault as e:
            if is_cli:
                pass
            else:
                raise ApiHTTPError(403, str(e))
        except ApiHTTPError as e:
            raise e
        except Exception as exc:
            raise ApiHTTPError(400, str(exc))

        pipe = workspace.get_pipe(pipe_name_or_id)
        if not pipe:
            raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))

        await PGService(workspace).on_endpoint_changed(pipe)

        try:
            response = pipe.to_json()
        except Exception as e:
            if not ignore_sql_errors:
                raise e
            response = pipe.to_json(dependencies=False)

        response["url"] = f"{api_host}/v0/pipes/{pipe.name}.json"

        token = workspace.get_unique_token_for_resource(pipe.id, scopes.PIPES_READ)

        if token:
            response["token"] = token

        return response

    @staticmethod
    async def drop_endpoint(
        workspace: User,
        node_name_or_id: str,
        pipe_name_or_id: str,
        edited_by: Optional[str],
        ignore_sql_errors: bool = False,
        pipe: Optional[Pipe] = None,
    ) -> Pipe:
        try:
            if not pipe:
                pipe = workspace.get_pipe(pipe_name_or_id)
                if not pipe:
                    raise PipeNotFound()
            node = pipe.pipeline.get_node(node_name_or_id)
            if not node:
                raise NodeNotFound()

            node.ignore_sql_errors = ignore_sql_errors
            if not ignore_sql_errors:
                try:
                    await SharedNodeUtils.validate_node_sql(workspace, pipe, node)
                except ForbiddenWordException as e:
                    raise ApiHTTPError(400, str(e), documentation="/api-reference/api-reference.html#forbidden-names")
            try:
                if not node.materialized:
                    await Users.check_dependent_nodes_by_materialized_node(workspace, node.id)
            except DependentMaterializedNodeOnUpdateException as e:
                logging.warning(
                    f"DependentMaterializedNodeOnUpdateException {str(e)} - ws: {workspace.id} - node: {node.id} - pipe: {pipe.id}"
                )
                raise ApiHTTPError(403, str(e))
            except Exception as e:
                logging.exception(
                    f"DependentMaterializedNodeOnUpdateException {str(e)} - ws: {workspace.id} - node: {node.id} - pipe: {pipe.id}"
                )
            workspace = await Users.drop_endpoint_of_pipe_node_async(
                workspace.id, pipe_name_or_id, node_name_or_id, edited_by
            )
        except PipeNotFound:
            raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))
        except NodeNotFound:
            raise ApiHTTPError(400, f"Pipe '{pipe_name_or_id}' does not contain the '{node_name_or_id}' node")
        except EndpointNotFound:
            raise ApiHTTPError(400, f"Pipe '{pipe_name_or_id}' node '{node_name_or_id}' is not an endpoint")
        except ApiHTTPError:
            raise
        except Exception as exc:
            raise ApiHTTPError(400, str(exc))

        pipe = workspace.get_pipe(pipe_name_or_id)
        if not pipe:
            raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))
        await PGService(workspace).on_endpoint_changed(pipe)
        return pipe

    @staticmethod
    async def create_node_copy(
        workspace: User,
        pipe_name_or_id: str,
        node_name_or_id: str,
        target_datasource_id: str,
        mode: Optional[str],
        edited_by: Optional[str],
        target_workspace_id: Optional[str] = None,
        ignore_sql_errors: bool = False,
    ) -> Dict[str, Any]:
        try:
            pipe = workspace.get_pipe(pipe_name_or_id)
            if not pipe:
                raise PipeNotFound()

            if node_name_or_id:
                node = pipe.pipeline.get_node(node_name_or_id)
                if node:
                    node.ignore_sql_errors = bool(ignore_sql_errors)
                    if not ignore_sql_errors:
                        try:
                            await SharedNodeUtils.validate_node_sql(
                                workspace, pipe, node, function_allow_list=workspace.allowed_table_functions()
                            )
                        except ForbiddenWordException as e:
                            raise ApiHTTPError(
                                403, str(e), documentation="/api-reference/api-reference.html#forbidden-names"
                            )

            await Users.set_node_of_pipe_as_copy_async(
                workspace.id,
                pipe_name_or_id,
                node_name_or_id,
                target_datasource_id,
                mode,
                edited_by,
                target_workspace_id,
            )

            await Users.set_source_copy_pipes_tag(
                target_workspace_id if target_workspace_id else workspace.id,
                target_datasource_id=target_datasource_id,
                source_pipe_id=pipe.id,
            )

        except PipeNotFound:
            raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))
        except NodeNotFound:
            raise ApiHTTPError(400, f"Pipe '{pipe_name_or_id}' does not contain the '{node_name_or_id}' node")
        except PipeIsCopy as copyExc:
            raise ApiHTTPError(
                400, str(copyExc), documentation="/api-reference/pipe-api.html#put--v0-pipes-(.+)-nodes-(.+)-copy"
            )
        except PipeIsMaterialized as e:
            raise ApiHTTPError(403, str(e))
        except Exception as exc:
            raise ApiHTTPError(400, str(exc))

        pipe = Users.get_pipe(workspace, pipe_name_or_id)
        if pipe:
            return pipe.to_json()
        raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))

    @staticmethod
    async def update_copy_target(
        workspace: User,
        pipe_name_or_id: str,
        target_datasource_id: str,
        former_datasource_id: str,
        former_workspace_id: str,
        target_workspace_id: str,
        edited_by: Optional[str],
        ignore_sql_errors: bool = False,
    ) -> Dict[str, Any]:
        try:
            pipe = workspace.get_pipe(pipe_name_or_id)
            if not pipe:
                raise PipeNotFound()

            node = pipe.get_copy_node()
            node.ignore_sql_errors = bool(ignore_sql_errors)
            if not ignore_sql_errors:
                try:
                    await SharedNodeUtils.validate_node_sql(
                        workspace, pipe, node, function_allow_list=workspace.allowed_table_functions()
                    )
                except ForbiddenWordException as e:
                    raise ApiHTTPError(403, str(e), documentation="/api-reference/api-reference.html#forbidden-names")
            await Users.update_copy_target_async(
                workspace.id, pipe.id, target_datasource_id, edited_by, target_workspace_id
            )
            await Users.update_source_copy_pipes_tag(
                target_workspace_id=target_workspace_id,
                target_datasource_id=target_datasource_id,
                former_workspace_id=former_workspace_id,
                former_datasource_id=former_datasource_id,
                source_pipe_id=pipe.id,
            )
        except PipeNotFound:
            raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))
        except NodeNotFound:
            raise ApiHTTPError(400, f"Cannot find copy node in pipe '{pipe_name_or_id}'")
        except PipeIsMaterialized as e:
            raise ApiHTTPError(403, str(e))
        except Exception as exc:
            raise ApiHTTPError(400, str(exc))

        pipe = Users.get_pipe(workspace, pipe_name_or_id)
        if pipe:
            return pipe.to_json()
        raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))

    @staticmethod
    async def update_new_pipe_type_when_overriden(
        materialized_node: PipeNode,
        new_pipe: Optional[Pipe],
        new_pipe_name: str,
        override: bool,
        pipe: Pipe,
        target_datasource: Datasource,
        target_workspace: User,
        workspace: User,
        edited_by: Optional[str],
    ) -> Tuple[Optional[Pipe], User]:
        IS_PIPE_ENDPOINT_RESTRICTIONS_ACTIVE = FeatureFlagsWorkspaceService.feature_for_id(
            FeatureFlagWorkspaces.PIPE_ENDPOINT_RESTRICTIONS, "", workspace.feature_flags
        )
        materialization_incompatibility = materialized_node and IS_PIPE_ENDPOINT_RESTRICTIONS_ACTIVE
        endpoint_node: Optional[PipeNode] = None
        copy_node: Optional[PipeNode] = None
        sink_node: Optional[PipeNode] = None
        stream_node: Optional[PipeNode] = None
        if override and new_pipe and pipe.endpoint and not new_pipe.endpoint and not materialization_incompatibility:
            former_endpoint_node = pipe.pipeline.get_node(pipe.endpoint)
            endpoint_node = new_pipe.pipeline.get_node(former_endpoint_node.name) if former_endpoint_node else None
        if (
            new_pipe
            and endpoint_node
            and pipe.pipe_type == PipeTypes.ENDPOINT
            and new_pipe.pipe_type == PipeTypes.DEFAULT
        ):
            workspace = await Users.set_node_of_pipe_as_endpoint_async(
                workspace.id, new_pipe.id, endpoint_node.id, edited_by
            )
        if override and new_pipe and pipe.copy_node and not new_pipe.copy_node and not materialization_incompatibility:
            former_copy_node = pipe.pipeline.get_node(pipe.copy_node)
            copy_node = new_pipe.pipeline.get_node(former_copy_node.name) if former_copy_node else None
        if (
            copy_node
            and new_pipe
            and pipe.pipe_type == PipeTypes.COPY
            and new_pipe.pipe_type == PipeTypes.DEFAULT
            and target_datasource
            and target_workspace
        ):
            workspace = await Users.set_node_of_pipe_as_copy_async(
                workspace.id, new_pipe.id, copy_node.id, target_datasource.id, edited_by, target_workspace.id
            )
        if override and new_pipe and pipe.sink_node and not new_pipe.sink_node and not materialization_incompatibility:
            former_sink_node = pipe.pipeline.get_node(pipe.sink_node)
            sink_node = new_pipe.pipeline.get_node(former_sink_node.name) if former_sink_node else None
        if sink_node and new_pipe and pipe.pipe_type == PipeTypes.DATA_SINK and new_pipe.pipe_type == PipeTypes.DEFAULT:
            workspace = await Users.set_node_of_pipe_as_datasink_async(
                workspace.id, new_pipe.id, sink_node.id, edited_by
            )
            if pipe.get_schedule(workspace.id) and not new_pipe.get_schedule(workspace.id):
                await remove_schedule_data_sink(pipe, workspace.id, delete_sink=False)

        if (
            override
            and new_pipe
            and pipe.stream_node
            and not new_pipe.stream_node
            and not materialization_incompatibility
        ):
            former_stream_node = pipe.pipeline.get_node(pipe.stream_node)
            stream_node = new_pipe.pipeline.get_node(former_stream_node.name) if former_stream_node else None
        if stream_node and new_pipe and pipe.pipe_type == PipeTypes.STREAM and new_pipe.pipe_type == PipeTypes.DEFAULT:
            workspace = await Users.set_node_of_pipe_as_stream_async(
                workspace.id, new_pipe.id, stream_node.id, edited_by
            )

        new_pipe = Users.get_pipe(workspace, new_pipe_name)
        return new_pipe, workspace

    @staticmethod
    async def drop_node_copy(
        workspace: User, pipe: Pipe, node_id: str, edited_by: Optional[str], hard_delete: Optional[bool] = False
    ) -> None:
        """
        >>> import asyncio
        >>> from tinybird.user import UserAccount
        >>> u = UserAccount.register('drop_node_copy@example.com', 'pass')
        >>> w = User.register('drop_node_copy_workspace', admin=u.id)
        >>> w = User.get_by_id(w.id)
        >>> nodes = [{'name': 'normal_node', 'sql': 'select 1'}, {'name': 'copy_node', 'sql': 'select 1'}]
        >>> copy_pipe = Users.add_pipe_sync(w, 'copy_pipe_1', nodes=nodes)
        >>> normal_node = copy_pipe.pipeline.get_node('normal_node')
        >>> w = User.get_by_id(w.id)
        >>> asyncio.run(NodeUtils.drop_node_copy(w, copy_pipe, normal_node.id, ''))
        Traceback (most recent call last):
        ...
        tinybird.user.CopyNodeNotFound
        >>> w.set_node_of_pipe_as_copy('copy_pipe_1', 'copy_node', 'datasource', w.id, None, '')
        >>> w = User.get_by_id(w.id)
        >>> asyncio.run(NodeUtils.drop_node_copy(w, copy_pipe, normal_node.id, ''))
        Traceback (most recent call last):
        ...
        tinybird.user.CopyNodeNotFound
        """

        if pipe.pipe_type != PipeTypes.COPY:
            raise CopyNodeNotFound()

        if not pipe.copy_node or pipe.copy_node != node_id:
            raise CopyNodeNotFound()

        try:
            await PipeUtils.delete_scheduled_sink(pipe.id, workspace.id)
        except Exception as e:
            logging.exception(f"Could not remove scheduled copy, error: {e}")

        try:
            target_datasource_id = pipe.copy_target_datasource
            target_workspace_id = pipe.copy_target_workspace
            if not hard_delete:
                await Users.drop_copy_of_pipe_node_async(workspace.id, pipe.id, node_id, edited_by)
                await Users.remove_source_copy_pipes_tag(
                    target_workspace_id if target_workspace_id else workspace.id, target_datasource_id, pipe.id
                )
        except Exception as e:
            logging.warning(f"Could not delete copy node, error: {e} - {target_workspace_id} - {workspace.id}")
            raise ApiHTTPError(409, "Could not delete copy node, please retry or contact us at support@tinybird.co")

    @staticmethod
    async def delete_node_materialized_view(
        workspace: User, node: PipeNode, cancel_fn=None, force: bool = False, hard_delete: bool = False
    ):
        try:
            return await SharedNodeUtils.delete_node_materialized_view(
                workspace, node, cancel_fn=cancel_fn, force=force, hard_delete=hard_delete
            )
        except Exception:
            raise ApiHTTPError(
                409,
                f"Could not delete materialized node with name '{node.name}', please retry or contact us at support@tinybird.co",
            )

    @staticmethod
    def get_engine_settings(node, workspace):
        return {key: value for key, value in node.items() if key.startswith("engine_")}

    @staticmethod
    async def analyze_node(
        workspace: User,
        pipe: Pipe,
        node: PipeNode,
        target: Optional[str],
        include_datafile: bool = False,
        include_schema: bool = True,
        populate_condition: Optional[str] = None,
        include_engine_full: bool = True,
    ):
        materialized_view = Materialized(workspace, node, pipe, target, populate_condition=populate_condition)
        await materialized_view.analyze()
        response = await materialized_view.to_json(
            include_datafile=include_datafile, include_schema=include_schema, include_engine_full=include_engine_full
        )
        return response

    @staticmethod
    async def analyze_copy_node(workspace: User, pipe: Pipe, node: PipeNode, target_datasource: str):
        return await get_copy_datasource_definition(workspace, pipe, node, target_datasource)

    @staticmethod
    async def validate_override_datasource(workspace: User, ds_name: str, override_datasource: bool = False):
        if not override_datasource:
            return False
        target_datasource = workspace.get_datasource(ds_name)
        if not target_datasource:
            return False

        try:
            if target_datasource.shared_with:
                raise ApiHTTPError.from_request_error(
                    ClientErrorConflict.conflict_override_shared_materialized_node(
                        workspaces_names=",".join(target_datasource.shared_with)
                    )
                )

            Users.check_used_by_pipes(workspace, target_datasource.id)
        except DependentMaterializedNodeException as e:

            def is_used_in_a_single_materialized_node(
                ws: User, ds: Datasource, e: DependentMaterializedNodeException
            ) -> bool:
                mat_node = ws.get_node_by_materialized(ds.id, i_know_what_im_doing=True)
                if mat_node and len(set(e._mat_nodes)) == 1 and e._mat_nodes[0] == mat_node.name:
                    pipes = []
                    for pipe_name in e._pipes:
                        if (p := ws.get_pipe(pipe_name)) and any([n.materialized for n in p.pipeline.nodes]):
                            pipes.append(pipe_name)

                    if len(set(pipes)) == 1:
                        return True

                return False

            if not is_used_in_a_single_materialized_node(workspace, target_datasource, e):
                raise ApiHTTPError.from_request_error(
                    ClientErrorConflict.conflict_override_materialized_node(
                        affected_materializations_message=e.affected_materializations_message,
                        dependent_pipes_message=e.dependent_pipes_message,
                    )
                )

        return True

    @staticmethod
    async def analyze_materialized_view(
        workspace: User,
        pipe: Pipe,
        node: PipeNode,
        mode: str,
        target_datasource: Optional[str],
        engine_settings,
        validate_materialized_view=False,
        is_cli=False,
        is_from_ui=False,
        include_datafile=False,
        include_schema=True,
        populate_condition=None,
        override_datasource=False,
    ):
        try:
            error_tag = "Cannot materialize node: " if mode == "materialized" else ""
            errors: List[str] = []
            is_exception = False
            template_execution_results = TemplateExecutionResults()

            if mode == "explain":
                if node.materialized:
                    return {"hints": [], "explain": []}

                sql = node.render_sql(
                    secrets=workspace.get_secrets_for_template(), template_execution_results=template_execution_results
                )

                return await ProTipsService.get_tips(
                    workspace=workspace, pipe=pipe, sql=sql, template_execution_results=template_execution_results
                )
            else:
                if node.is_template():
                    raise ApiHTTPError.from_request_error(AppendNodeError.materialized_nodes_dont_support_templates())

                if validate_materialized_view:
                    validate_materialized_view_errors = await NodeUtils.validate_materialized_view(
                        workspace=workspace,
                        node=node,
                        pipe=pipe,
                        target_datasource=target_datasource,
                        is_cli=is_cli,
                        engine_settings=engine_settings,
                        is_from_ui=is_from_ui,
                        return_errors=True,
                        override_datasource=override_datasource,
                    )
                    errors = errors + validate_materialized_view_errors

                response = await NodeUtils.analyze_node(
                    workspace,
                    pipe,
                    node,
                    target_datasource,
                    include_datafile=include_datafile,
                    include_schema=include_schema,
                    populate_condition=populate_condition,
                )

                sql = node.render_sql(
                    secrets=workspace.get_secrets_for_template(),
                    template_execution_results=template_execution_results,
                )

                try:
                    tips = await ProTipsService.get_tips(
                        workspace=workspace,
                        pipe=pipe,
                        sql=sql,
                        materializing=True,
                        template_execution_results=template_execution_results,
                    )
                    response["warnings"] += tips["warnings"]
                except Exception as e:
                    logging.exception(f"error on protips: {str(e)}")

                return response
        except ServicesDataSourcesError as e:
            is_exception = True
            raise ApiHTTPError(403, f"{error_tag}{str(e)}", documentation="/monitoring/service-datasources.html")
        except (SQLTemplateException, CHException, QueryNotAllowed) as e:
            is_exception = True
            logging.warning(f"Node analyze warning: {e}")
            raise ApiHTTPError(400, str(e))
        except (SyntaxError, ParseError, UnClosedIfError) as e:
            pipes = workspace.get_used_pipes_in_query(q=node._sql, pipe=pipe)
            error = process_syntax_error(e, pipes=pipes)
            errors.append(error)
        except (PipeNotFound, NodeNotFound) as e:
            is_exception = True
            raise e
        except AnalyzeException as e:
            errors.append(str(e))
        except ApiHTTPError as e:
            errors.append(str(e.error_message))
        except Exception as exc:
            is_exception = True
            logging.warning(f"Unhandled Node analyze Error: {exc}")
            raise ApiHTTPError(400, str(exc))
        finally:
            if errors and not is_exception:
                msg = errors[0]
                if len(errors) > 1:
                    msg = "Multiple errors found: " + "\n".join(errors)
                raise ApiHTTPError(400, f"{error_tag}{str(msg)}")

    @staticmethod
    async def validate_materialized_view(
        workspace: User,
        node: PipeNode,
        pipe: Pipe,
        target_datasource: Optional[str],
        engine_settings,
        is_cli: bool = False,
        is_from_ui: bool = False,
        return_errors: bool = False,
        override_datasource: bool = False,
    ) -> List[str]:
        try:
            materialized = Materialized(workspace, node, pipe, target_datasource)
            errors = await materialized.validate(
                columns=None,
                engine_settings=engine_settings,
                is_cli=is_cli,
                is_from_ui=is_from_ui,
                override_datasource=override_datasource,
            )
        except Exception as e:
            raise e
        else:
            if errors and return_errors:
                return errors

            if errors:
                msg = errors[0]
                if len(errors) > 1:
                    msg = "Multiple errors found: " + "\n".join(errors)
                raise ApiHTTPError(400, msg)

            return []

    @staticmethod
    async def validate_node(
        workspace: User,
        sql: str,
        pipe: Pipe,
        name: Optional[str],
        description: Optional[str],
        engine_settings: Optional[dict],
        datasource: Optional[str],
        populate_subset: Optional[str],
        is_cli: Optional[bool],
        is_from_ui: Optional[bool],
        include_datafile: Optional[bool],
        include_schema: Optional[bool],
        override_datasource: Optional[bool] = False,
        node_type: Optional[str] = "standard",
        ignore_sql_errors: bool = False,
        analyze_materialized_view: bool = False,
        is_aux_pipe: bool = False,
        check_endpoint: bool = True,
        function_allow_list: Optional[FrozenSet[str]] = None,
    ):
        if not sql or not sql.strip():
            raise ApiHTTPError(
                400, 'Wrong SQL for node, check if the SQL is sent correctly in the body or using the "sql"'
            )

        if not is_aux_pipe:
            name = name if name else pipe.next_valid_name()

        try:
            if name is not None and not Resource.validate_name(name):
                raise ApiHTTPError(400, f'Invalid Node name "{name}". {Resource.name_help(name)}')
        except ForbiddenWordException as e:
            raise ApiHTTPError(400, str(e), documentation="/api-reference/api-reference.html#forbidden-names")

        if populate_subset:
            populate_subset_value = get_populate_subset(populate_subset)
            if not populate_subset_value or populate_subset_value <= 0:
                if is_cli:
                    su = "--subset"
                else:
                    su = "populate_subset"
                raise ApiHTTPError(400, f'"{su}" must be a decimal number > 0 and <= 1')

        try:
            node = PipeNode(name, sql, description=description)
            node.ignore_sql_errors = ignore_sql_errors
            if not ignore_sql_errors:
                await SharedNodeUtils.validate_node_sql(
                    workspace, pipe, node, check_endpoint=check_endpoint, function_allow_list=function_allow_list
                )
        except ForbiddenWordException as e:
            raise ApiHTTPError(400, str(e), documentation="/api-reference/api-reference.html#forbidden-names")
        except (ValueError, CHException) as e:
            raise ApiHTTPError(400, str(e))
        except (SyntaxError, ParseError, UnClosedIfError) as e:
            pipes = workspace.get_used_pipes_in_query(q=sql, pipe=pipe)
            error = process_syntax_error(e, pipes=pipes)
            raise ApiHTTPError(400, error)

        if not is_aux_pipe and pipe.has_node(name):
            raise ApiHTTPError(
                400, f'Node name "{name}" already exists in pipe. Node names must be unique within a given pipe.'
            )

        if not PipeNodeTypes.is_valid(node_type):
            raise ApiHTTPError(
                400, f"Invalid node type: '{node_type}', valid types are: {', '.join(PipeNodeTypes.valid_types)}"
            )

        node.node_type = node_type

        if node_type == "materialized" and analyze_materialized_view:
            pipe_node = PipeNode(name, sql, description=description)
            await NodeUtils.analyze_materialized_view(
                workspace=workspace,
                pipe=pipe,
                node=pipe_node,
                mode="materialized",
                target_datasource=datasource,
                engine_settings=engine_settings,
                is_cli=is_cli,
                is_from_ui=is_from_ui,
                include_datafile=include_datafile,
                include_schema=include_schema,
                validate_materialized_view=True,
                override_datasource=override_datasource,
            )

        return node

    @staticmethod
    async def validate_nodes(
        workspace: User,
        pipe: Pipe,
        nodes: List[Dict[str, Any]],
        is_cli: Optional[bool],
        is_from_ui: Optional[bool],
        include_datafile: Optional[bool],
        include_schema: Optional[bool],
        populate_subset: Optional[str],
        ignore_sql_errors: bool = False,
        check_endpoint: bool = True,
        analyze_materialized_view: bool = False,
    ):
        allow_table_functions = any(
            [node for node in nodes if node.get("type", "standard") == PipeNodeTypes.COPY]
        ) or all([node for node in nodes if node.get("type", "standard") == "standard"])
        for node in nodes:
            name: str = node.get("name", "")

            if not Resource.validate_name(name):
                raise ApiHTTPError(400, f'Invalid Node name "{name}". {Resource.name_help(name)}')

            sql = node.get("sql", None)
            name = node.get("name", None)
            description = node.get("description", None)
            engine_settings = NodeUtils.get_engine_settings(node, workspace)
            datasource = node.get("datasource", None)
            override_datasource = node.get("override_datasource", "false") == "true"
            node_type = node.get("type", "standard")

            await NodeUtils.validate_node(
                workspace=workspace,
                sql=sql,
                pipe=pipe,
                name=name,
                description=description,
                engine_settings=engine_settings,
                datasource=datasource,
                override_datasource=override_datasource,
                populate_subset=populate_subset,
                is_cli=is_cli,
                is_from_ui=is_from_ui,
                include_datafile=include_datafile,
                include_schema=include_schema,
                node_type=node_type,
                ignore_sql_errors=ignore_sql_errors,
                analyze_materialized_view=analyze_materialized_view,
                is_aux_pipe=True,
                check_endpoint=check_endpoint,
                function_allow_list=workspace.allowed_table_functions() if allow_table_functions else None,
            )

        return nodes

    @staticmethod
    async def replace_backfill_condition_in_sql(
        workspace: User,
        pipe: Pipe,
        node: PipeNode,
        sql: str,
        extra_replacements: Dict[Tuple[str, str], Union[str, Tuple[str, str]]],
    ) -> Tuple[str, Tuple[str, str, Optional[str]], PipeNode, str]:
        _sql, _ = await workspace.replace_tables_async(
            sql,
            pipe=pipe,
            use_pipe_nodes=True,
            extra_replacements=extra_replacements,
            template_execution_results=TemplateExecutionResults(),
            release_replacements=True,
        )
        source_table = chquery.get_left_table(_sql, default_database=workspace.database)
        source_ds = workspace.get_datasource(source_table[1], include_read_only=True)
        # FIXME: This is when the matview uses as landing -> live.landing_ds. Make get_replacements to only replace `live` and no other arbitrary vX_Y_Z release
        if not source_ds and workspace.is_release:
            source_ds = workspace.get_main_workspace().get_datasource(source_table[1], include_read_only=True)
        if source_ds and "backfill_column" in source_ds.tags:
            backfill_column = source_ds.tags.get("backfill_column")
            if backfill_column:
                # FIXME: check backfill_column is in source_ds.columns
                backfill_value = (datetime.now(timezone.utc) + timedelta(seconds=MATVIEW_BACKFILL_VALUE_WAIT)).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                extra_replacements[(source_table[0], source_table[1])] = (
                    f"(SELECT * FROM {source_table[0]}.{source_table[1]} WHERE {backfill_column} > '{backfill_value}')"
                )
                sql, _ = await workspace.replace_tables_async(
                    sql,
                    pipe=pipe,
                    use_pipe_nodes=True,
                    extra_replacements=extra_replacements,
                    template_execution_results=TemplateExecutionResults(),
                    release_replacements=True,
                )
                node.tags["backfill_value"] = backfill_value
            else:
                sql = _sql
        else:
            sql = _sql
        return sql, source_table, node, _sql


@dataclass()
class DataSourceUtils:
    @staticmethod
    async def set_dependent_datasources_tag(workspace, view, target_table_id, engine, target_workspace=None):
        return await SharedDataSourceUtils.set_dependent_datasources_tag(
            workspace, view, target_table_id, engine, target_workspace
        )

    @staticmethod
    async def update_dependent_datasources_tag(workspace, view, target_table_id):
        return await SharedDataSourceUtils.update_dependent_datasources_tag(workspace, view, target_table_id)

    @staticmethod
    async def get_view_sources(workspace, view):
        return await SharedDataSourceUtils.get_view_sources(workspace, view)

    @staticmethod
    def get_cascade_views(source_datasource, workspace):
        return SharedDataSourceUtils.get_cascade_views(source_datasource, workspace)

    @staticmethod
    async def override_datasource(
        workspace: User,
        original_target_datasource: Datasource,
        target_datasource: Datasource,
        job_executor: JobExecutor,
        request_id: str,
        edited_by: Optional[str],
    ) -> Datasource:
        old_mat_node = workspace.get_node_by_materialized(original_target_datasource.id, i_know_what_im_doing=True)
        if old_mat_node:
            await NodeUtils.delete_node_materialized_view(
                workspace,
                old_mat_node,
                cancel_fn=partial(PipeUtils.cancel_populate_jobs, workspace, old_mat_node.id, job_executor),
            )

        original_target_datasource.install_hook(DeleteCompleteDatasourceHook(workspace))
        original_target_datasource.install_hook(PGSyncDatasourceHook(workspace))
        original_target_datasource.install_hook(LandingDatasourceHook(workspace))
        original_target_datasource.install_hook(LastDateDatasourceHook(workspace))
        is_datasource_dropped = await Users.drop_datasource_async(workspace, original_target_datasource.id)
        if is_datasource_dropped:
            try:
                for hook in original_target_datasource.hooks:
                    hook.before_delete(original_target_datasource)
                results = await drop_table(workspace, original_target_datasource.id)
                if results:
                    logging.exception(
                        f"Failed to delete some of the Data Source tables: user={workspace.id}, datasource={original_target_datasource.id}, results={results}"
                    )
                for hook in original_target_datasource.hooks:
                    hook.after_delete(original_target_datasource)
            except Exception as e:
                logging.exception(e)
                raise ApiHTTPError.from_request_error(ServerErrorInternal.failed_delete(error=e))
            finally:
                tracker.track_hooks(original_target_datasource.hook_log(), workspace=workspace)
                tracker.track_datasource_ops(original_target_datasource.operations_log(), workspace=workspace)

        try:
            error = None
            return await Users.alter_datasource_name(
                workspace, target_datasource.name, original_target_datasource.name, edited_by
            )
        except ResourceAlreadyExists as e:
            error = str(e)
            raise ApiHTTPError(409, error)
        except ValueError as e:
            error = str(e)
            raise ApiHTTPError(400, error)
        finally:
            ops_log_entry = OpsLogEntry(
                start_time=datetime.now(timezone.utc),
                event_type="override",
                datasource_id=target_datasource.id,
                datasource_name=target_datasource.name,
                workspace_id=workspace.id,
                workspace_email=workspace.name,
                result="error" if error else "ok",
                elapsed_time=0,
                error=error,
                rows=0,
                rows_quarantine=0,
                options={"old_id": original_target_datasource.id, "new_id": target_datasource.id},
            )
            tracker.track_datasource_ops([ops_log_entry], request_id=request_id, workspace=workspace)

    @staticmethod
    def check_target_permissions(
        workspace: User,
        token_access: Optional[AccessToken],
        target_datasource: Datasource,
        target_workspace: Optional[User],
    ):
        if not token_access:
            raise ApiHTTPError.from_request_error(ClientErrorForbidden.invalid_permissions_to_copy_data())
        datasource_append_scope = token_access.may_append_ds(target_datasource.id)
        if not datasource_append_scope:
            raise ApiHTTPError.from_request_error(ClientErrorForbidden.invalid_permissions_to_copy_data())
        if target_workspace and not workspace.lives_in_the_same_ch_cluster_as(target_workspace):
            raise ApiHTTPError.from_request_error(
                ClientErrorBadRequest.cannot_copy_data_between_workspaces_in_different_clusters()
            )


@dataclass()
class PipeUtils:
    @staticmethod
    async def cancel_populate_jobs(workspace, node_id, job_executor):
        try:
            jobs = sorted(
                Job.get_all_by_owner(workspace.id, limit=LAST_JOBS_TO_CANCEL), key=lambda j: j.created_at, reverse=True
            )
            for job in jobs:
                try:
                    if job.kind == JobKind.POPULATE and job.view_node == node_id and job.is_cancellable:
                        job = job.try_to_cancel(job_executor)
                        job.status = JobStatus.CANCELLED
                        cast(PopulateJob, job).track()
                except Exception as e:
                    logging.warning(f"cancel_populate_job: {str(e)}")
        except Exception as e:
            logging.warning(f"cancel_populate_jobs: {str(e)}")

    @staticmethod
    async def cancel_dynamodb_jobs(workspace_id: str, datasource_id: str, job_executor):
        try:
            jobs = sorted(
                Job.get_all_by_owner(workspace_id, limit=LAST_JOBS_TO_CANCEL), key=lambda j: j.created_at, reverse=True
            )
            for job in jobs:
                try:
                    if (
                        job.kind == JobKind.DYNAMODB_SYNC
                        and job.is_cancellable
                        and cast(DynamoDBSyncJob, job).datasource_id == datasource_id
                    ):
                        job.try_to_cancel(job_executor)
                except Exception as e:
                    logging.warning(f"cancel_dynamodb_job: {str(e)}")
        except Exception as e:
            logging.warning(f"cancel_dynamodb_jobs: {str(e)}")

    @staticmethod
    async def generate_clone_pipe_with_data(
        pipe: Pipe,
        u: User,
        filters,
        readable_resources,
        use_pipe_nodes=False,
        variables=None,
        row_limit=ROW_DEFAULT_LIMIT,
        output_format_json_quote_64bit_integers=0,
        output_format_json_quote_denormals=0,
        finalize_aggregations=False,
    ):
        """
        generates a clone of pipe (using new id's) in which every node has the data filled
        It needs:
            u - the user in which database everything is going to be executed
            filters - filters coming from the token
            readable_resources: resources from `u` which are visible for this pipe. If None it assumes the token has admin permissions.

        In other words `u` is where pipe is going to read from and filters and readable_resources are the permissions.
        """
        new_pipe = pipe.clone_with_new_ids()

        # fill the nodes with the data
        for node in new_pipe.pipeline.nodes:
            try:
                q = node._sql
                q = q.strip()
                if node.is_template():
                    q = f"%select * from ({q[1:]}) limit {row_limit} FORMAT JSON"
                else:
                    q = f"select * from ({q}) limit {row_limit} FORMAT JSON"
                headers, data = await PipeUtils.query(
                    q,
                    new_pipe,
                    u,
                    filters,
                    readable_resources,
                    use_pipe_nodes,
                    variables=variables,
                    output_format_json_quote_64bit_integers=output_format_json_quote_64bit_integers,
                    output_format_json_quote_denormals=output_format_json_quote_denormals,
                )

                # rows are limited to row_limit but each row can contain a lot of data
                if len(data) > MAX_DATA_SIZE_TO_STORE_IN_NODE:
                    node.result = {"data": None, "error": "node response is too large"}
                else:
                    node.result = {"data": json.loads(data), "error": None}
            except (CHException, ApiHTTPError) as e:
                node.result = {"data": None, "error": str(e)}
        return new_pipe

    @staticmethod
    async def query(
        q,
        pipe,
        u,
        filters,
        readable_resources,
        use_pipe_nodes,
        variables=None,
        max_threads=4,
        output_format_json_quote_64bit_integers=0,
        output_format_json_quote_denormals=0,
        finalize_aggregations=False,
    ):
        try:
            # check format
            template_execution_results = TemplateExecutionResults()
            q = q.strip()
            if q[0] == "%":
                # templated
                with Timer("render sql template"):
                    # we are not adding secrets here but this code is only used in snapshots and they are deprecated
                    q, template_execution_results, _ = render_sql_template(
                        q[1:], variables, test_mode=variables is None
                    )
            client = HTTPClient(u["database_server"], database=u["database"])

            with Timer("replace tables in sql"):
                q, _ = await u.replace_tables_async(
                    q,
                    readable_resources=readable_resources,
                    pipe=pipe,
                    filters=filters,
                    use_pipe_nodes=True,
                    variables=variables,
                    template_execution_results=template_execution_results,
                    finalize_aggregations=finalize_aggregations,
                    release_replacements=True,
                )

            backend_hint = template_execution_results.get("backend_hint", None)

            ch_limits = u.get_limits(prefix="ch")
            max_threads = Limits.max_threads(
                ch_limits.get("max_threads", None),
                endpoint_cheriff=None,
                request=max_threads,
                template=template_execution_results.get("max_threads", None),
            )

            extra_params = {
                "output_format_json_quote_64bit_integers": output_format_json_quote_64bit_integers,
                "output_format_json_quote_denormals": output_format_json_quote_denormals,
            }
            if max_threads:
                extra_params["max_threads"] = max_threads

            query_id = ulid.new().str
            with Timer("fetching query results from ch"):
                compressed = False
                headers, body = await client.query(
                    q,
                    query_id=query_id,
                    compress=compressed,
                    read_cluster=True,
                    backend_hint=backend_hint,
                    read_only=True,
                    **extra_params,
                )
            return headers, body
        except (ValueError, SQLTemplateException) as e:
            raise ApiHTTPError(400, str(e), documentation=getattr(e, "documentation", "/query/query-parameters.html"))
        except (SyntaxError, ParseError, UnClosedIfError) as e:
            pipes = u.get_used_pipes_in_query(q=q, pipe=pipe)
            error = process_syntax_error(e, pipes=pipes)
            raise ApiHTTPError(400, error)

    @staticmethod
    def parse_copy_parameters(
        workspace: User,
        token_access: Optional[AccessToken],
        target_datasource_name_or_id: str,
        target_workspace_name_or_id: Optional[str] = None,
        target_token: Optional[str] = None,
    ) -> Tuple[Optional[User], Datasource]:
        target_workspace = None

        if target_workspace_name_or_id:
            try:
                target_workspace = Users.get_by_id_or_name(target_workspace_name_or_id)
            except Exception as e:
                raise ApiHTTPError(404, str(e))

        if target_workspace and not target_workspace.lives_in_the_same_ch_cluster_as(workspace):
            raise ApiHTTPError.from_request_error(
                ClientErrorBadRequest.cannot_copy_data_between_workspaces_in_different_clusters()
            )

        if target_workspace and target_token:
            target_datasource = target_workspace.get_datasource(target_datasource_name_or_id)
            token_access = target_workspace.get_token_access_info(target_token)
        else:
            target_datasource = workspace.get_datasource(target_datasource_name_or_id)

        if not target_datasource:
            workspace_name = workspace.name if not target_workspace else target_workspace.name
            raise ApiHTTPError(
                404, f"Target Data Source '{target_datasource_name_or_id}' not found in {workspace_name} Workspace"
            )

        DataSourceUtils.check_target_permissions(workspace, token_access, target_datasource, target_workspace)

        return (target_workspace, target_datasource)

    @staticmethod
    async def delete_scheduled_sink(pipe_id: str, workspace_id: str):
        data_sink = None

        try:
            data_sink = DataSink.get_by_resource_id(pipe_id, workspace_id)
        except Exception:
            pass

        if data_sink:
            await data_sink.delete()

    @staticmethod
    async def validate_copy_target_datasource(
        pipe: Optional[Pipe],
        node_sql: str,
        workspace: User,
        target_datasource: Datasource,
        app_settings: Dict[str, Any],
        target_workspace: Optional[User] = None,
        function_allow_list: Optional[FrozenSet[str]] = None,
        template_execution_results: Optional[TemplateExecutionResults] = None,
    ):
        if template_execution_results is None:
            template_execution_results = TemplateExecutionResults()
        secrets = workspace.get_secrets_for_template()

        try:
            try:
                is_table_function = False
                sql, _ = await workspace.replace_tables_async(
                    node_sql,
                    pipe=pipe,
                    use_pipe_nodes=True,
                    extra_replacements={},
                    template_execution_results=template_execution_results,
                    release_replacements=True,
                    secrets=secrets,
                )
            except QueryNotAllowed as e:
                if is_table_function_in_error(workspace, e, function_allow_list):
                    sql, _ = await workspace.replace_tables_async(
                        node_sql,
                        pipe=pipe,
                        use_pipe_nodes=True,
                        extra_replacements={},
                        template_execution_results=template_execution_results,
                        release_replacements=True,
                        function_allow_list=function_allow_list,
                        secrets=secrets,
                    )
                    is_table_function = True
                    try:
                        ch_params = workspace.get_secrets_ch_params_by(template_execution_results.ch_params)
                        await validate_table_function_host(sql, app_settings, ch_params=ch_params)
                    except ValueError:
                        raise ApiHTTPError(
                            400, "Cannot parse table function host", documentation="/api-reference/query-api.html"
                        )
                else:
                    raise e

            max_execution_time = CopyLimits.max_job_execution_time.get_limit_for(workspace)
            await SQLUtils.validate_query_columns_for_schema(
                sql,
                datasource=target_datasource,
                workspace=target_workspace if target_workspace else workspace,
                max_execution_time=max_execution_time,
                ch_params=workspace.get_secrets_ch_params_by(template_execution_results.ch_params),
            )
        except CHException as e:
            if is_table_function and e.code in [CHErrors.TIMEOUT_EXCEEDED]:
                logging.warning(f"Timeout exceeded on validate query for table function, skipping: {e}")
                return
            error = str(e)
            # format error message for missing columns
            if "missing columns" in error.lower():
                raise SQLValidationException(SQLPipeError.missing_columns_error(error, node_sql))
            raise e

    @staticmethod
    async def delete_pipe(
        workspace: User,
        pipe: Pipe,
        job_executor: JobExecutor | Any,
        edited_by: Optional[str],
        hard_delete: bool = False,
    ) -> None:
        for node in pipe.pipeline.nodes:
            if node.materialized:
                await NodeUtils.delete_node_materialized_view(
                    workspace,
                    node,
                    cancel_fn=partial(PipeUtils.cancel_populate_jobs, workspace, node.id, job_executor),
                    hard_delete=hard_delete,
                )

        if pipe.pipe_type == PipeTypes.COPY:
            assert isinstance(pipe.copy_node, str)
            await NodeUtils.drop_node_copy(workspace, pipe, pipe.copy_node, edited_by, hard_delete)

        if pipe.pipe_type == PipeTypes.DATA_SINK:
            assert isinstance(pipe.sink_node, str)
            await SinkNodeUtils.drop_node_sink(workspace, pipe, pipe.sink_node, edited_by)

        if pipe.pipe_type == PipeTypes.STREAM:
            assert isinstance(pipe.stream_node, str)
            await StreamNodeUtils.drop_node_stream(workspace, pipe, pipe.stream_node, edited_by)

        try:
            if not hard_delete and pipe.endpoint:
                await Users.check_dependent_nodes_by_materialized_node(workspace, pipe.endpoint)
        except DependentMaterializedNodeOnUpdateException as e:
            logging.warning(
                f"DependentMaterializedNodeOnUpdateException {str(e)} - ws: {workspace.id} - node: {pipe.endpoint} - pipe: {pipe.id}"
            )
            raise DependentMaterializedNodeOnUpdateException(str(e))
        except Exception as e:
            logging.exception(
                f"DependentMaterializedNodeOnUpdateException {str(e)} - ws: {workspace.id} - node: {pipe.endpoint} - pipe: {pipe.id}"
            )

        dropped = await Users.drop_pipe_async(workspace, pipe.id)
        if dropped:
            await PGService(workspace).on_pipe_deleted(pipe)
            try:
                main_workspace = workspace.get_main_workspace()
                await Users.remove_resource_from_tags(main_workspace, resource_id=pipe.id, resource_name=pipe.name)
            except Exception as e:
                logging.exception(
                    f"Exception while removing pipe from tags {str(e)} - ws: {workspace.id} - pipe: {pipe.name}"
                )
        else:
            raise PipeNotFound()


class NodeMaterializationBaseHandler(BaseHandler):
    def get_engine_settings(self, workspace):
        settings = self.request.arguments.items()
        return {key: value[0].decode() for key, value in settings if key.startswith("engine_")}

    async def create_materialized_view(
        self,
        workspace: User,
        node: PipeNode,
        datasource: Optional[str],
        sql: Any,
        pipe: Pipe,
        edited_by: Optional[str],
        override_datasource: bool = False,
        datasource_description: str = "",
        populate: bool = False,
        populate_subset: Optional[Any] = None,
        populate_condition: Optional[Any] = None,
        with_staging: bool = False,
        is_cli: bool = False,
        engine: Optional[Any] = None,
        engine_settings: Optional[Any] = None,
        is_from_ui: bool = False,
        include_datafile: bool = False,
        include_schema: bool = False,
        analyze_materialized_view: bool = True,
        unlink_on_populate_error: bool = False,
    ) -> Tuple[Optional[PopulateJob], bool, Optional[Datasource], PipeNode, Any]:
        created_datasource: bool = False
        added_datasource: bool = False
        job = None

        if node.is_template():
            raise ApiHTTPError.from_request_error(AppendNodeError.materialized_nodes_dont_support_templates())

        if not datasource:
            raise ApiHTTPError.from_request_error(AppendNodeError.datasource_parameter_mandatory())

        branch_mode = BranchMode(self.get_api_option("branch_mode", BRANCH_MODES, default_option=BranchMode.NONE.value))
        if branch_mode == BranchMode.FORK and engine is not None:
            raise ApiHTTPError.from_request_error(
                PipeDefinitionError.fork_downstream_do_not_support_pipes_with_engine()
            )

        cluster = workspace.cluster

        # You can also define other options:
        # - Whether it should have a staging (blue/green) behaviour when pushing new data.
        if with_staging:
            node.tags["staging"] = True

        target_datasource = Users.get_datasource(workspace, datasource)
        columns = None

        try:
            response = await NodeUtils.analyze_node(
                workspace,
                pipe,
                node,
                datasource,
                include_datafile=False,
                include_schema=True,
                include_engine_full=False,
            )

            analysis = response.get("analysis", {})
            columns = analysis.get("datasource", {}).get("columns", [])
            analysis_sql = analysis.get("sql")
            warnings = response.get("warnings")
        except (AnalyzeException, ValueError, CHException) as e:
            raise ApiHTTPError(400, str(e))
        except Exception as e:
            raise ApiHTTPError(500, str(e))

        if not target_datasource or override_datasource:
            if not self.has_scope(scopes.DATASOURCES_CREATE) and not self.is_admin():
                raise ApiHTTPError.from_request_error(
                    AppendNodeError.datasource_create_scope_required_to_create_datasource()
                )

            if (
                override_datasource
                and not self.is_admin()
                and not self.has_scope(scopes.DATASOURCES_CREATE)
                and target_datasource
                and target_datasource.id not in self.get_dropable_resources()
            ):
                raise ApiHTTPError.from_request_error(
                    AppendNodeError.datasource_drop_scope_required_to_override_datasource()
                )

        target_datasource = Users.get_datasource(workspace, datasource)
        must_override_datasource = await NodeUtils.validate_override_datasource(
            workspace, datasource, override_datasource=override_datasource
        )
        must_override_datasource &= target_datasource is not None

        original_target_datasource: Optional[Datasource] = None
        if not target_datasource or must_override_datasource:
            node.sql = analysis_sql
            sql = analysis_sql
            if must_override_datasource:
                original_target_datasource = target_datasource
                datasource += f"_override_{Resource.guid()[-6:]}"
            try:
                if not engine:
                    engine = analysis.get("datasource", {}).get("engine", {})
                else:
                    engine = self._parse_engine(engine=engine, columns=columns, engine_settings=engine_settings)

                error: Optional[Exception] = None
                target_datasource = None

                target_datasource = await Users.add_datasource_async(
                    workspace,
                    datasource,
                    cluster=cluster,
                    tags={"created_by_pipe": pipe.id},
                    description=datasource_description,
                )
                target_datasource.install_hook(CreateDatasourceHook(workspace))
                target_datasource.install_hook(PGSyncDatasourceHook(workspace))
                target_datasource.install_hook(LandingDatasourceHook(workspace))
                target_datasource.install_hook(LastDateDatasourceHook(workspace))
                schema = ", ".join(schema_to_sql_columns(columns))

                added_datasource = True

                await create_table_from_schema(
                    workspace=workspace, datasource=target_datasource, schema=schema, engine=engine
                )

                created_datasource = True
            except ServicesDataSourcesError as e:
                error = e
                raise ApiHTTPError(403, str(e), documentation="/monitoring/service-datasources.html")
            except ResourceAlreadyExists as e:
                error = e
                raise ApiHTTPError(409, str(e))
            except (ValueError, CHException) as e:
                error = e
                raise ApiHTTPError(400, str(e))
            except ApiHTTPError as e:
                error = e
                raise e
            except Exception as e:
                error = e
                logging.exception(f"Materialize Error: {e}")
                raise ApiHTTPError(500, str(e))
            finally:
                if target_datasource:
                    try:
                        if error:
                            for hook in target_datasource.hooks:
                                hook.on_error(target_datasource, error)
                        tracker.track_hooks(
                            target_datasource.hook_log(),
                            request_id=self._request_id,
                            source="pipe",
                            workspace=workspace,
                        )
                        tracker.track_datasource_ops(
                            target_datasource.operations_log(),
                            request_id=self._request_id,
                            source="pipe",
                            workspace=workspace,
                        )
                    except Exception as e:
                        logging.exception(e)
                        raise e
                    finally:
                        if error and (created_datasource or added_datasource):
                            await self._drop_created_data_source_on_failed_materialization(workspace, target_datasource)

        refreshed_datasource = Users.get_datasource(workspace, datasource)
        assert isinstance(refreshed_datasource, Datasource)
        target_table = refreshed_datasource.id

        engine_settings = self.get_engine_settings(workspace)

        try:
            # In order to avoid analyzing twice in the UI, when creating the materialized view we set analyze=false to avoid
            # analyzing it again. This option would be hidden to the user and set to True by default.
            if analyze_materialized_view:
                _ = await NodeUtils.analyze_materialized_view(
                    workspace=workspace,
                    pipe=pipe,
                    node=node,
                    mode="materialized",
                    target_datasource=target_table,
                    engine_settings=engine_settings,
                    validate_materialized_view=True,
                    is_cli=is_cli,
                    is_from_ui=is_from_ui,
                    include_datafile=include_datafile,
                    include_schema=include_schema,
                )
            else:
                try:
                    await NodeUtils.validate_materialized_view(
                        workspace=workspace,
                        node=node,
                        pipe=pipe,
                        target_datasource=target_table,
                        engine_settings=engine_settings,
                        is_cli=is_cli,
                        is_from_ui=is_from_ui,
                    )
                except Exception as original_error:
                    try:
                        node.sql = analysis_sql
                        sql = analysis_sql
                        await NodeUtils.validate_materialized_view(
                            workspace=workspace,
                            node=node,
                            pipe=pipe,
                            target_datasource=target_table,
                            engine_settings=engine_settings,
                            is_cli=is_cli,
                            is_from_ui=is_from_ui,
                        )
                    except Exception as e:
                        logging.warning(f"Error on validating materialized view from analyzed sql: {str(e)}")
                        raise original_error
        except (ApiHTTPError, Exception) as e:
            if created_datasource:
                await self._drop_created_data_source_on_failed_materialization(workspace, refreshed_datasource)
            raise e

        extra_replacements = {}

        if with_staging:
            table_details = await ch_table_details_async(
                table_name=target_table, database_server=workspace["database_server"], database=workspace["database"]
            )
            target_table_staging = f"{target_table}_staging"
            extra_replacements = {target_table: target_table_staging}

            # Since there could be more than one view pointing to the same table we need to have a special
            # ReplicatedEngine path that includes the node.id so it's not shared with existing tables
            # Why isn't the table dropped and replaced fully? I don't know, and at this point I'm too afraid to ask
            table_details_original_engine = table_details.original_engine
            assert isinstance(table_details_original_engine, str)
            engine_full = engine_patch_replicated_engine(
                table_details_original_engine,
                table_details.original_engine_full,
                f"{workspace['database']}.{node.id}_{target_table_staging}",
            )

            # "NOT EXISTS" for the same reason
            create_staging_table_query = CHTable(
                [],
                cluster=workspace.cluster,
                engine=engine_full if engine_full else "",
                not_exists=True,
                as_table=f"{workspace['database']}.{target_table}",
                storage_policy=workspace.storage_policy,
            ).as_sql(workspace["database"], target_table_staging)

            target_table = target_table_staging

            try:
                client = HTTPClient(workspace["database_server"], database=workspace["database"])
                _ = await client.query(
                    create_staging_table_query, read_only=False, **workspace.ddl_parameters(skip_replica_down=True)
                )
            except Exception as e:
                logging.exception(e)
                raise ApiHTTPError(500, "Could not create staging table")

        sql, source_table_tuple, node, populate_sql = await NodeUtils.replace_backfill_condition_in_sql(
            workspace,
            pipe,
            node,
            sql,
            extra_replacements,  # type: ignore
        )

        has_error = False
        try:
            node.cluster = cluster
            source_table = CHTableLocation(source_table_tuple[0], source_table_tuple[1])
            await validate_populate_condition(workspace, node.id, populate_condition, source_table=source_table)

            # if must_override swap the old and new datasources
            if must_override_datasource:
                assert isinstance(original_target_datasource, Datasource)
                refreshed_datasource = await DataSourceUtils.override_datasource(
                    workspace,
                    original_target_datasource,
                    target_datasource,
                    self.application.job_executor,
                    self._request_id,
                    edited_by,
                )
                target_datasource = refreshed_datasource

            _ = await ch_create_materialized_view(workspace, node.id, sql, target_table)

            node.materialized = target_table

            try:
                await Users.update_node_of_pipe(workspace.id, pipe.id, node, edited_by)
            except PipeNotFound:
                raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe.name))

            table_details, _ = await refreshed_datasource.table_metadata(workspace)

            await DataSourceUtils.set_dependent_datasources_tag(
                workspace=workspace, view=node.id, target_table_id=target_table, engine=table_details.engine
            )

            populate_subset = get_populate_subset(populate_subset)
            if populate or (populate_subset and populate_subset > 0) or populate_condition:
                pipe_url = f'{self.application.settings["host"]}/{workspace.id}/pipe/{pipe.id}'

                job = await new_populate_job(
                    self.application.job_executor,
                    workspace,
                    node.id,
                    populate_sql,
                    target_table,
                    pipe.id,
                    pipe.name,
                    pipe_url,
                    populate_subset=populate_subset,
                    populate_condition=populate_condition,
                    source_table=source_table,
                    unlink_on_populate_error=unlink_on_populate_error,
                    request_id=self._request_id,
                )

        except ApiHTTPError:
            has_error = True
            raise
        except QueryNotAllowed as e:
            raise ApiHTTPError(403, str(e))
        except PopulateException as e:
            has_error = True
            raise ApiHTTPError(
                400, str(e), documentation="/api-reference/pipe-api.html#post--v0-pipes-(.+)-nodes-(.+)-population"
            )
        except ValueError as e:
            has_error = True
            raise ApiHTTPError(400, str(e), documentation=getattr(e, "documentation", "/query/query-parameters.html"))
        except CHException as e:
            has_error = True
            if e.code == CHErrors.TABLE_ALREADY_EXISTS:
                raise ApiHTTPError(409, f"The Materialized View '{node.name}' already exists")
            if e.code == CHErrors.UNKNOWN_STORAGE:
                raise ApiHTTPError.from_request_error(ClientErrorBadRequest.invalid_ch_unknown_storage(engine=engine))
            if e.code == CHErrors.QUERY_IS_NOT_SUPPORTED_IN_MATERIALIZED_VIEW or e.code == CHErrors.CANNOT_PARSE_TEXT:
                raise ApiHTTPError(400, str(e))
            if e.code in [CHErrors.DATA_TYPE_CANNOT_BE_USED_IN_TABLES, CHErrors.CANNOT_CONVERT_TYPE]:
                raise ApiHTTPError(
                    400,
                    "Error when creating the Materialized View, make sure there is no column with type `Nullable(Nothing)` => `NULL as column_name`",
                )
            logging.exception(f"Materialize Error: {e}")
            raise ApiHTTPError(500, f"Unknown error: '{e}'")
        except Exception as e:
            has_error = True
            logging.exception(f"Materialize Error: {e}")
            raise ApiHTTPError(500, f"Unknown error: '{e}'")
        finally:
            if has_error and created_datasource:
                await self._drop_created_data_source_on_failed_materialization(workspace, refreshed_datasource)

        return job, created_datasource, target_datasource, node, warnings

    async def _drop_created_data_source_on_failed_materialization(self, workspace: User, datasource: Datasource):
        try:
            results = await drop_table(workspace, datasource.id)
            logging.info(f"Drop created Data Source on failed materialization: {results}")
            await Users.drop_datasource_async(workspace, datasource.id)
        except Exception as e:
            # not raising the exception here since it's something internal and we already raise the caller exceptions
            # logging a message though to track possible errors
            logging.exception(f"Error on drop data source on failed materialization, possible orphan metadata: {e}")

    def _parse_engine(
        self, engine: Optional[str], columns: List[Dict[str, Any]], engine_settings: Optional[Dict[str, str]] = None
    ) -> Optional[str]:
        try:
            if engine is None:
                return None
            engine_args = engine_settings if engine_settings else {}
            if not engine_args:
                for k in self.request.arguments.keys():
                    if k.startswith("engine_"):
                        engine_args[k[len("engine_") :]] = self.get_argument(k)
            return engine_full_from_dict(engine, engine_args, columns=columns)
        except Exception as e:
            raise ApiHTTPError(400, str(e))


class APIPipeNodeAnalysisHandler(NodeMaterializationBaseHandler):
    def check_xsrf_cookie(self):
        pass

    @authenticated
    @with_scope(scopes.PIPES_CREATE)
    async def get(self, pipe_name_or_id: str, node_name_or_id: str) -> None:
        try:
            workspace = self.get_workspace_from_db()
            pipe = workspace.get_pipe(pipe_name_or_id)

            if not pipe:
                raise PipeNotFound()

            node = pipe.pipeline.get_node(node_name_or_id)

            if not node:
                raise NodeNotFound()

            mode = self.get_argument("mode", "materialized")
            dry_run = self.get_argument("dry_run", False) == "true"
            target_datasource = self.get_argument("datasource", None)
            engine_settings = self.get_engine_settings(workspace)
            is_cli = self.get_argument("cli_version", None)
            is_from_ui = self.get_argument("from", None) == "ui"
            include_datafile = self.get_argument("include_datafile", False) == "true"
            include_schema = self.get_argument("include_schema", "true") == "true"
            populate_condition = self.get_argument("populate_condition", None)
            override_datasource = self.get_argument("override_datasource", False) == "true"

            if mode == "copy":
                response = await NodeUtils.analyze_copy_node(
                    workspace=workspace, pipe=pipe, node=node, target_datasource=target_datasource
                )
            else:
                response = await NodeUtils.analyze_materialized_view(
                    workspace=workspace,
                    pipe=pipe,
                    node=node,
                    mode=mode,
                    target_datasource=target_datasource,
                    engine_settings=engine_settings,
                    validate_materialized_view=dry_run,
                    is_cli=is_cli,
                    is_from_ui=is_from_ui,
                    include_datafile=include_datafile,
                    include_schema=include_schema,
                    populate_condition=populate_condition,
                    override_datasource=override_datasource,
                )
            self.write_json(response)
        except (AnalyzeException, QueryNotAllowed, CHException) as ee:
            raise ApiHTTPError(400, str(ee))
        except PipeNotFound:
            raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))
        except NodeNotFound:
            raise ApiHTTPError(400, f"Pipe '{pipe_name_or_id}' does not contain the '{node_name_or_id}' node")
        except (SyntaxError, ParseError, UnClosedIfError) as e:
            if not node:
                raise ApiHTTPError(400, f"Pipe '{pipe_name_or_id}' does not contain the '{node_name_or_id}' node")
            pipes = workspace.get_used_pipes_in_query(q=node._sql, pipe=pipe)
            error = process_syntax_error(e, pipes=pipes)
            raise ApiHTTPError(400, error)
        except ApiHTTPError as e:
            raise e
        except Exception as exc:
            logging.warning(f"Node analyze Error: {exc}")
            raise ApiHTTPError(500, str(exc))


class APIPipeNodeExplainHandler(APIQueryHandler):
    def check_xsrf_cookie(self):
        pass

    @authenticated
    @check_plan_limit(Limit.build_plan_api_requests)
    @check_workspace_limit(Limit.workspace_api_requests)
    async def get(self, pipe_name_or_id: str, node_name_or_id: str | None = None) -> None:
        """
        Return the explain plan and the whole debug query for the node.

        If no node is specified, the most relevant node of the pipe will be used:

        - The endpoint node for endpoints.
        - The node that materializes for materialized views.
        - The copy node for Copy pipes.
        - The last node for general pipes.

        It accepts query parameters to test the query with different values.

        .. sourcecode:: bash
            :caption: Getting the explain plan

            curl -X GET \\
                -H "Authorization: Bearer <PIPE:READ and DATASOURCE:READ token>" \\
                "https://api.tinybird.co/v0/pipes/:pipe_name/nodes/:node_name/explain?department=Engineering"

            or

            curl -X GET \\
                -H "Authorization: Bearer <PIPE:READ and DATASOURCE:READ token>" \\
                "https://api.tinybird.co/v0/pipes/:pipe_name/explain?department=Engineering"

        .. code-block:: json
            :caption: Successful response

            {
                "debug_query": "SELECT country, department FROM (SELECT * FROM employees AS employees) AS an_endpoint_0 WHERE department = 'Engineering'",
                "query_explain": "Expression ((Projection + Before ORDER BY)) Filter ((WHERE + (Projection + Before ORDER BY))) ReadFromMergeTree (employees) Indexes: MinMax Condition: true Parts: 6/6 Granules: 6/6 Partition Condition: true Parts: 6/6 Granules: 6/6 PrimaryKey Condition: true Parts: 6/6 Granules: 6/6"
            }

        .. csv-table:: Request parameters
            :header: "Key", "Type", "Description"
            :widths: 20, 20, 60

            "token", "String", "Auth token. Ensure it has the ``PIPE:READ`` and the proper ``DATASOURCE:READ`` scopes on it."
            "pipe_name", "Float", "The name or id of the pipe."
            "node_name", "String", "Optional. The name or id of the node to explain. If not provided, the most relevant node of the pipe will be used."
            "params", "String", "Optional. The value of the parameters to test the query with. They are regular URL query parameters."

        .. csv-table:: Response codes
            :header: "Code", "Description"
            :widths: 20, 80

            "200", "No error"
            "400", "Could not get a node to run the explain plan"
            "403", "Forbidden. Provided token doesn't have permissions to run the explain plan, it needs ``ADMIN`` or ``PIPE:READ`` and ``DATASOURCE:READ``"
            "404", "Pipe not found, Node not found"

        """

        t_start = time.time()

        workspace = self.get_workspace_from_db()
        endpoint_user_profile = workspace.profiles.get(WorkspaceUserProfiles.ENDPOINT_USER_PROFILE.value, None)

        pipe = workspace.get_pipe(pipe_name_or_id)
        if not pipe:
            raise ApiHTTPError(404, f"The pipe '{pipe_name_or_id}' does not exist")

        node = pipe.pipeline.get_node(node_name_or_id)
        if not node:
            try:
                node = pipe.get_relevant_node()
            except PipeValidationException as e:
                raise ApiHTTPError(501, str(e))

        if not node:
            raise ApiHTTPError(400, f"Could not get a node to run the explain plan on the pipe '{pipe_name_or_id}'")

        access_token = self._get_access_info()
        if (
            not self.is_admin()
            and access_token is not None
            and pipe.id not in access_token.get_resources_for_scope(scopes.PIPES_READ)
        ):
            raise ApiHTTPError.from_request_error(ClientErrorForbidden.token_doesnt_have_access_to_this_resource())

        from_param = self.get_argument("from", None)

        variables = {k: v[0].decode() for k, v in self.request.query_arguments.items()}

        # save pipe_id in the tag so it can be used to get the real from spans table
        # the url could contain the id or the pipe name (and if it's renamed you can lose the track)

        parameters = variables if variables else {}
        self.set_span_tag({"pipe_id": pipe.id, "pipe_name": pipe.name, "parameters": parameters})

        if endpoint_user_profile:
            self.set_span_tag({"user_profile": endpoint_user_profile})

        return await self._query(
            node._sql,
            pipe_name_or_id,
            variables=variables,
            t_start=t_start,
            query_id=self._request_id,
            from_param=from_param,
            user=endpoint_user_profile,
            fallback_user_auth=True,
            explain=True,
        )


class APIPipeEndpointHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @authenticated
    @requires_write_access
    @with_scope(scopes.PIPES_CREATE)
    async def put(self, pipe_name_or_id):
        # """
        # Sets the enabled transformation node of the Pipe, so it becomes accessible as an API endpoint.

        # .. sourcecode:: bash
        #     :caption: Changing the endpoint

        #     curl -X PUT \\
        #         -H "Authorization: Bearer <PIPE:CREATE token>" \\
        #         -d 't_bd1e095da943494d9410a812b24cea81' "https://api.tinybird.co/v0/pipes/:name/endpoint"

        # ``node_id`` to be enabled must be sent as part of the body. If empty, it will disable the current enabled node. Returns a full description of the Pipe in JSON.

        # .. code-block:: json
        #     :caption: Successful response

        #     {
        #         "id": "t_60d8f84ce5d349b28160013ce99758c7",
        #         "name": "my_pipe",
        #         "description": "this is my pipe description",
        #         "nodes": [{
        #             "id": "t_bd1e095da943494d9410a812b24cea81",
        #             "name": "get_all",
        #             "sql": "SELECT * FROM my_datasource",
        #             "description": "This is a description for the **first** node",
        #             "materialized": null,
        #             "cluster": null,
        #             "dependencies": ["my_datasource"],
        #             "tags": {},
        #             "created_at": "2019-09-03 19:56:03.704840",
        #             "updated_at": "2019-09-04 07:05:53.191437",
        #             "version": 0,
        #             "project": null,
        #             "result": null,
        #             "ignore_sql_errors": false
        #         }],
        #         "endpoint": "t_bd1e095da943494d9410a812b24cea81",
        #         "created_at": "2019-09-03 19:56:03.193446",
        #         "updated_at": "2019-09-10 07:18:39.797083",
        #         "parent": null
        #     }

        # .. container:: hint

        #     The response will contain a ``token`` if there's a **unique READ token** for this pipe. You could use this token to share your endpoint.

        # .. csv-table:: Response codes
        #     :header: "Code", "Description"
        #     :widths: 20, 80

        #     "200", "No error"
        #     "400", "empty or wrong id"
        #     "403", "Forbidden. Provided token doesn't have permissions to publish a pipe, it needs ``ADMIN`` or ``PIPE:CREATE``"
        #     "404", "Pipe not found"
        # """
        try:
            node_name_or_id = self.request.body.decode().strip()
            ignore_sql_errors = self.get_argument("ignore_sql_errors", False) == "true"
            edited_by = _calculate_edited_by(self._get_access_info())
            response = await NodeUtils.create_endpoint(
                self.get_workspace_from_db(),
                pipe_name_or_id,
                node_name_or_id,
                edited_by,
                ignore_sql_errors,
                self.application.settings["api_host"],
            )
            self.write_json(response)
        except UnicodeDecodeError:
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.invalid_encoding())


class APIPipeNodeEndpointHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @authenticated
    @requires_write_access
    @with_scope(scopes.PIPES_CREATE)
    @read_only_from_ui
    async def post(self, pipe_name_or_id, node_name_or_id):
        """
        Publishes an API endpoint

        .. sourcecode:: bash
            :caption: Publishing an endpoint

            curl -X POST \\
                -H "Authorization: Bearer <PIPE:CREATE token>" \\
                "https://api.tinybird.co/v0/pipes/:pipe/nodes/:node/endpoint"

        .. code-block:: json
            :caption: Successful response

            {
                "id": "t_60d8f84ce5d349b28160013ce99758c7",
                "name": "my_pipe",
                "description": "this is my pipe description",
                "nodes": [{
                    "id": "t_bd1e095da943494d9410a812b24cea81",
                    "name": "get_all",
                    "sql": "SELECT * FROM my_datasource",
                    "description": "This is a description for the **first** node",
                    "materialized": null,
                    "cluster": null,
                    "dependencies": ["my_datasource"],
                    "tags": {},
                    "created_at": "2019-09-03 19:56:03.704840",
                    "updated_at": "2019-09-04 07:05:53.191437",
                    "version": 0,
                    "project": null,
                    "result": null,
                    "ignore_sql_errors": false
                }],
                "endpoint": "t_bd1e095da943494d9410a812b24cea81",
                "created_at": "2019-09-03 19:56:03.193446",
                "updated_at": "2019-09-10 07:18:39.797083",
                "parent": null
            }

        .. container:: hint

            The response will contain a ``token`` if there's a **unique READ token** for this pipe. You could use this token to share your endpoint.

        .. csv-table:: Response codes
            :header: "Code", "Description"
            :widths: 20, 80

            "200", "No error"
            "400", "Wrong node id"
            "403", "Forbidden. Provided token doesn't have permissions to publish a pipe, it needs ``ADMIN`` or ``PIPE:CREATE``"
            "404", "Pipe not found"
        """
        ignore_sql_errors = self.get_argument("ignore_sql_errors", False) == "true"
        is_cli = self.get_argument("cli_version", False) is not False
        edited_by = _calculate_edited_by(self._get_access_info())
        response = await NodeUtils.create_endpoint(
            self.get_workspace_from_db(),
            pipe_name_or_id,
            node_name_or_id,
            edited_by,
            ignore_sql_errors,
            self.application.settings["api_host"],
            is_cli,
        )
        self.write_json(response)

    @authenticated
    @requires_write_access
    @with_scope(scopes.PIPES_CREATE)
    @read_only_from_ui
    async def delete(self, pipe_name_or_id: str, node_name_or_id: str) -> None:
        """
        Unpublishes an API endpoint

        .. sourcecode:: bash
            :caption: Unpublishing an endpoint

            curl -X DELETE \\
                -H "Authorization: Bearer <PIPE:CREATE token>" \\
                "https://api.tinybird.co/v0/pipes/:pipe/nodes/:node/endpoint"

        .. csv-table:: Response codes
            :header: "Code", "Description"
            :widths: 20, 80

            "200", "No error"
            "400", "Wrong node id"
            "403", "Forbidden. Provided token doesn't have permissions to publish a pipe, it needs ``ADMIN`` or ``PIPE:CREATE``"
            "404", "Pipe not found"
        """

        workspace = self.get_workspace_from_db()
        ignore_sql_errors = self.get_argument("ignore_sql_errors", False) == "true"
        edited_by = _calculate_edited_by(self._get_access_info())
        pipe = await NodeUtils.drop_endpoint(workspace, node_name_or_id, pipe_name_or_id, edited_by, ignore_sql_errors)
        response = pipe.to_json()
        response["url"] = f'{self.application.settings["api_host"]}/v0/pipes/{pipe.name}.json'

        token = workspace.get_unique_token_for_resource(pipe.id, scopes.PIPES_READ)

        if token:
            response["token"] = token

        self.write_json(response)


class APIPipePopulationHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @authenticated
    @requires_write_access
    @with_scope(scopes.PIPES_CREATE)
    async def post(self, pipe_name_or_id, node_name_or_id):
        """
        Populates a Materialized View

        .. sourcecode:: bash
            :caption: Populating a Materialized View

            curl
                -H "Authorization: Bearer <PIPE:CREATE token>" \\
                -X POST "https://api.tinybird.co/v0/pipes/:pipe/nodes/:node/population" \\
                -d "populate_condition=toYYYYMM(date) = 202203"

        The response will not be the final result of the import but a Job. You can check the job status and progress using the `Jobs API <api_reference_job url_>`_.

        Alternatively you can use a query like this to check the operations related to the populate Job:

        .. sourcecode:: sql
            :caption: Check populate jobs in the datasources_ops_log including dependent Materialized Views triggered

            SELECT *
            FROM tinybird.datasources_ops_log
            WHERE
                timestamp > now() - INTERVAL 1 DAY
                AND operation_id IN (
                    SELECT operation_id
                    FROM tinybird.datasources_ops_log
                    WHERE
                        timestamp > now() - INTERVAL 1 DAY
                        and datasource_id = '{the_datasource_id}'
                        and job_id = '{the_job_id}'
                )
            ORDER BY timestamp ASC

        When a populate job fails for the first time, the Materialized View is automatically unlinked. In that case you can get failed population jobs and their errors to fix them with a query like this:

        .. sourcecode:: sql
            :caption: Check failed populate jobs

            SELECT *
            FROM tinybird.datasources_ops_log
            WHERE
                datasource_id = '{the_datasource_id}'
                AND pipe_name = '{the_pipe_name}'
                AND event_type LIKE 'populateview%'
                AND result = 'error'
            ORDER BY timestamp ASC

        Alternatively you can use the ``unlink_on_populate_error='true'`` flag to always unlink the Materialized View if the populate job does not work as expected.

        .. csv-table:: Request parameters
            :header: "Key", "Type", "Description"
            :widths: 20, 20, 60

            "token", "String", "Auth token. Ensure it has the ``PIPE:CREATE`` scope on it"
            "populate_subset", "Float", "Optional. Populate with a subset percent of the data (limited to a maximum of 2M rows), this is useful to quickly test a materialized node with some data. The subset must be greater than 0 and lower than 0.1. A subset of 0.1 means a 10 percent of the data in the source Data Source will be used to populate the Materialized View. It has precedence over ``populate_condition``"
            "populate_condition", "String", "Optional. Populate with a SQL condition to be applied to the trigger Data Source of the Materialized View. For instance, ``populate_condition='date == toYYYYMM(now())'`` it'll populate taking all the rows from the trigger Data Source which ``date`` is the current month. ``populate_condition`` is not taken into account if the ``populate_subset`` param is present. Including in the ``populate_condition`` any column present in the Data Source ``engine_sorting_key`` will make the populate job process less data."
            "truncate", "String", "Optional. Default is ``false``. Populates over existing data, useful to populate past data while new data is being ingested. Use ``true`` to truncate the Data Source before populating."
            "unlink_on_populate_error", "String", "Optional. Default is ``false``. If the populate job fails the Materialized View is unlinked and new data won't be ingested in the Materialized View."

        .. csv-table:: Response codes
            :header: "Code", "Description"
            :widths: 20, 80

            "200", "No error"
            "400", "Node is not materialized"
            "403", "Forbidden. Provided token doesn't have permissions to append a node to the pipe, it needs ``ADMIN`` or ``PIPE:CREATE``"
            "404", "Pipe not found, Node not found"
        """

        workspace = self.get_workspace_from_db()
        pipe = workspace.get_pipe(pipe_name_or_id)

        if not pipe:
            raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))

        node = pipe.pipeline.get_node(node_name_or_id)

        if not node:
            raise ApiHTTPError(404, f"Node {node_name_or_id} not found")

        if not node.materialized:
            raise ApiHTTPError(400, f"Node '{node_name_or_id}' is not materialized")

        populate_subset = self.get_argument("populate_subset", None)
        populate_condition = self.get_argument("populate_condition", None)
        truncate = self.get_argument("truncate", "false") == "true"
        unlink_on_populate_error = self.get_argument("unlink_on_populate_error", None) == "true"
        datasource = Users.get_datasource(workspace, node.materialized)

        try:
            sql, _ = await workspace.replace_tables_async(
                node.sql,
                pipe=pipe,
                use_pipe_nodes=True,
                extra_replacements={},
                template_execution_results=TemplateExecutionResults(),
                release_replacements=True,
            )

            pipe_url = f'{self.application.settings["host"]}/{workspace.id}/pipe/{pipe.id}'

            job = await new_populate_job(
                self.application.job_executor,
                workspace,
                node.id,
                sql,
                datasource.id,
                pipe.id,
                pipe.name,
                pipe_url,
                populate_subset=populate_subset,
                truncate=truncate,
                populate_condition=populate_condition,
                unlink_on_populate_error=unlink_on_populate_error,
                request_id=self._request_id,
            )
        except PopulateException as e:
            raise ApiHTTPError(
                400, str(e), documentation="/api-reference/pipe-api.html#post--v0-pipes-(.+)-nodes-(.+)-population"
            )
        except QueryNotAllowed as e:
            raise ApiHTTPError(403, str(e))
        except (ValueError, SQLTemplateException) as e:
            raise ApiHTTPError(400, str(e), documentation=getattr(e, "documentation", "/query/query-parameters.html"))

        response = node.to_json()

        if job:
            response["job"] = job.to_json()
            response["job"]["job_url"] = self.application.settings["api_host"] + "/v0/jobs/" + job.id

        response["datasource"] = datasource.to_json()
        self.write_json(response)


class APIPipeMaterializationHandler(NodeMaterializationBaseHandler):
    def check_xsrf_cookie(self):
        pass

    @authenticated
    @requires_write_access
    @with_scope(scopes.PIPES_CREATE)
    @read_only_from_ui
    async def post(self, pipe_name_or_id: str, node_name_or_id: str) -> None:
        """
        Creates a Materialized View

        .. sourcecode:: bash
            :caption: Creating a Materialized View

            curl \\
                -H "Authorization: Bearer <PIPE:CREATE token>" \\
                -X POST "https://api.tinybird.co/v0/pipes/:pipe/nodes/:node/materialization?datasource=my_data_source_name&populate=true"


        .. csv-table:: Request parameters
            :header: "Key", "Type", "Description"
            :widths: 20, 20, 60

            "token", "String", "Auth token. Ensure it has the ``PIPE:CREATE`` scope on it"
            "datasource", "String", "Required. Specifies the name of the destination Data Source where the Materialized View schema is defined. If the Data Source does not exist, it creates automatically with the default settings."
            "override_datasource", "Boolean", "Optional. Default ``false`` When the target Data Source of the Materialized View exists in the Workspace it'll be overriden by the ``datasource`` specified in the request."
            "populate", "Boolean", "Optional. Default ``false``. When ``true``, a job is triggered to populate the destination datasource."
            "populate_subset", "Float", "Optional. Populate with a subset percent of the data (limited to a maximum of 2M rows), this is useful to quickly test a materialized node with some data. The subset must be greater than 0 and lower than 0.1. A subset of 0.1 means a 10 percent of the data in the source Data Source will be used to populate the Materialized View. Use it together with ``populate=true``, it has precedence over ``populate_condition``"
            "populate_condition", "String", "Optional. Populate with a SQL condition to be applied to the trigger Data Source of the Materialized View. For instance, ``populate_condition='date == toYYYYMM(now())'`` it'll populate taking all the rows from the trigger Data Source which ``date`` is the current month. Use it together with ``populate=true``. ``populate_condition`` is not taken into account if the ``populate_subset`` param is present. Including in the ``populate_condition`` any column present in the Data Source ``engine_sorting_key`` will make the populate job process less data."
            "unlink_on_populate_error", "String", "Optional. Default is ``false``. If the populate job fails the Materialized View is unlinked and new data won't be ingested in the Materialized View."
            "engine", "String", "Optional. Engine for destination Materialized View. If the Data Source already exists, the settings are not overriden."
            "engine_*", String, "Optional. Engine parameters and options. Requires the ``engine`` parameter. If the Data Source already exists, the settings are not overriden. `Check Engine Parameters and Options for more details <api_reference_datasource url_>`_"

        SQL query for the materialized node must be sent in the body encoded in utf-8

        .. csv-table:: Response codes
            :header: "Code", "Description"
            :widths: 20, 80

            "200", "No error"
            "400", "Node already being materialized"
            "403", "Forbidden. Provided token doesn't have permissions to append a node to the pipe, it needs ``ADMIN`` or ``PIPE:CREATE``"
            "404", "Pipe not found, Node not found"
            "409", "The Materialized View already exists or ``override_datasource`` cannot be performed"
        """

        workspace = self.get_workspace_from_db()

        pipe = workspace.get_pipe(pipe_name_or_id)
        if not pipe:
            raise ApiHTTPError(404, f"Pipe {pipe_name_or_id} not found")

        p = pipe.pipeline.clone()
        node = p.get_node(node_name_or_id)

        if not node:
            raise ApiHTTPError(404, f"Node {node_name_or_id} not found")

        if node.is_materializing:
            raise ApiHTTPError(400, f"Node {node_name_or_id} is already being materialized")

        IS_PIPE_ENDPOINT_RESTRICTIONS_ACTIVE = FeatureFlagsWorkspaceService.feature_for_id(
            FeatureFlagWorkspaces.PIPE_ENDPOINT_RESTRICTIONS, "", workspace.feature_flags
        )
        if IS_PIPE_ENDPOINT_RESTRICTIONS_ACTIVE and pipe.endpoint:
            raise ApiHTTPError(
                403,
                f"Pipe {pipe_name_or_id} cannot be materialized because it is an endpoint. Pipes can only have one output: endpoint or materialized node. You can copy the pipe and publish it as an endpoint, or unlink the materialized view.",
            )

        IS_PIPE_NODE_RESTRICTIONS_ACTIVE = FeatureFlagsWorkspaceService.feature_for_id(
            FeatureFlagWorkspaces.PIPE_NODE_RESTRICTIONS, "", workspace.feature_flags
        )
        materialized_tables = pipe.pipeline.get_materialized_tables()
        if IS_PIPE_NODE_RESTRICTIONS_ACTIVE and materialized_tables:
            raise ApiHTTPError(
                403,
                f"Pipe {pipe_name_or_id} already has a node materializing. Pipes can only have one output: endpoint or materialized node. You can unlink the current materialized view and try again.",
            )
        edited_by = _calculate_edited_by(self._get_access_info())
        try:
            await Users.mark_node_as_materializing(workspace, pipe_name_or_id, node_name_or_id, edited_by)
        except Exception as e:
            logging.exception(
                f"Error marking node {node_name_or_id} from pipe {pipe_name_or_id} as materializing. Workspace: {workspace.name} ({workspace.id}). Error: {e}"
            )

        datasource = self.get_argument("datasource", None)
        override_datasource = self.get_argument("override_datasource", "false") == "true"
        datasource_description = self.get_argument("description", "")
        populate = self.get_argument("populate", "false") == "true"
        with_staging = self.get_argument("with_staging", "false") == "true"
        engine = self.get_argument("engine", None)
        engine_settings = self.get_engine_settings(workspace)
        populate_subset = self.get_argument("populate_subset", None)
        populate_condition = self.get_argument("populate_condition", None)
        is_cli = self.get_argument("cli_version", None)
        is_from_ui = self.get_argument("from", None) == "ui"
        analyze_materialized_view = self.get_argument("analyze", "true") == "true"
        include_datafile = self.get_argument("include_datafile", False) == "true"
        include_schema = self.get_argument("include_schema", "true") == "true"
        unlink_on_populate_error = self.get_argument("unlink_on_populate_error", None) == "true"

        # NOTE
        # If the SQL comes in the body, we overwrite the node's content
        # We use that since, from the UI, we want to apply some changes to the node
        # This behaviour won't be present in the API

        try:
            sql = self.request.body.decode().strip()

            if not sql:
                sql = node.sql
            else:
                node.sql = sql

            job, created_datasource, target_datasource, node, warnings = await self.create_materialized_view(
                workspace=workspace,
                node=node,
                datasource=datasource,
                override_datasource=override_datasource,
                datasource_description=datasource_description,
                sql=sql,
                pipe=pipe,
                populate=populate,
                populate_subset=populate_subset,
                populate_condition=populate_condition,
                with_staging=with_staging,
                is_cli=is_cli,
                engine=engine,
                engine_settings=engine_settings,
                is_from_ui=is_from_ui,
                include_datafile=include_datafile,
                include_schema=include_schema,
                analyze_materialized_view=analyze_materialized_view,
                unlink_on_populate_error=unlink_on_populate_error,
                edited_by=edited_by,
            )

            response = node.to_json()

            if job:
                response["job"] = job.to_json()
                response["job"]["job_url"] = self.application.settings["api_host"] + "/v0/jobs/" + job.id

            if target_datasource:
                response["datasource"] = target_datasource.to_json()
                response["created_datasource"] = created_datasource

            if warnings:
                response["warnings"] = warnings

            self.write_json(response)
        except UnicodeDecodeError:
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.invalid_encoding())
        except ApiHTTPError as e:
            raise e
        except Exception as e:
            logging.exception(e)
            raise ApiHTTPError(500, str(e))
        finally:
            try:
                await Users.unmark_node_as_materializing(workspace, pipe_name_or_id, node_name_or_id, edited_by)
            except Exception as e:
                logging.exception(
                    f"Error unmarking node {node_name_or_id} from pipe {pipe_name_or_id} as materializing. Workspace: {workspace.name} ({workspace.id}). Error: {e}"
                )

    @authenticated
    @requires_write_access
    @with_scope(scopes.PIPES_CREATE)
    @read_only_from_ui
    async def delete(self, pipe_name_or_id: str, node_name_or_id: str) -> None:
        """
        Removes a Materialized View

        By removing a Materialized View, nor the Data Source nor the Node are deleted. The Data Source will still be present, but will stop receiving data from the Node.

        .. sourcecode:: bash
            :caption: Removing a Materialized View

            curl \
                -H "Authorization: Bearer <PIPE:CREATE token>" \\
                -X DELETE "https://api.tinybird.co/v0/pipes/:pipe/nodes/:node/materialization"

        .. csv-table:: Response codes
            :header: "Code", "Description"
            :widths: 20, 80

            "204", "No error, Materialized View removed"
            "403", "Forbidden. Provided token doesn't have permissions to append a node to the pipe, it needs ``ADMIN`` or ``PIPE:CREATE``"
            "404", "Pipe not found, Node not found"
        """

        workspace = self.get_workspace_from_db()
        pipe = workspace.get_pipe(pipe_name_or_id)

        if not pipe:
            raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))

        p = pipe.pipeline.clone()
        node = p.get_node(node_name_or_id)

        if not node:
            raise ApiHTTPError(404, f"Node '{node_name_or_id}' not found")

        if not node.materialized:
            raise ApiHTTPError(400, f"Node '{node_name_or_id}' is not materialized")

        node = await NodeUtils.delete_node_materialized_view(
            workspace,
            node,
            cancel_fn=partial(PipeUtils.cancel_populate_jobs, workspace, node.id, self.application.job_executor),
        )
        edited_by = _calculate_edited_by(self._get_access_info())
        try:
            await Users.update_node_of_pipe(workspace.id, pipe.id, node, edited_by)
        except PipeNotFound:
            raise ApiHTTPError(404, f"Pipe '{pipe_name_or_id}' not found.")

        self.set_status(204)


class APIPipeNodeAppendHandler(NodeMaterializationBaseHandler):
    def check_xsrf_cookie(self):
        pass

    @authenticated
    @requires_write_access
    @with_scope(scopes.PIPES_CREATE)
    @read_only_from_ui
    async def post(self, pipe_name_or_id: str) -> None:
        """
        Appends a new node to a Pipe.

        .. sourcecode:: bash
            :caption: adding a new node to a pipe

            curl \\
                -H "Authorization: Bearer <PIPE:CREATE token>" \\
                -d 'select * from node_0' "https://api.tinybird.co/v0/pipes/:name/nodes?name=node_name&description=explanation"

        Appends a new node that creates a Materialized View

        .. sourcecode:: bash
            :caption: adding a Materialized View using a materialized node

            curl \\
                -H "Authorization: Bearer <PIPE:CREATE token>" \\
                -d 'select id, sum(amount) as amount, date from my_datasource' "https://api.tinybird.co/v0/pipes/:name/nodes?name=node_name&description=explanation&type=materialized&datasource=new_datasource&engine=AggregatingMergeTree"


        .. csv-table:: Request parameters
            :header: "Key", "Type", "Description"
            :widths: 20, 20, 60

            "name", "String", "The referenceable name for the node."
            "description", "String", "Use it to store a more detailed explanation of the node."
            "token", "String", "Auth token. Ensure it has the ``PIPE:CREATE`` scope on it"
            "type", "String", "Optional. Available options are {``standard`` (default), ``materialized``, ``endpoint``}. Use ``materialized`` to create a Materialized View from your new node."
            "datasource", "String", "Required with ``type=materialized``. Specifies the name of the destination Data Source where the Materialized View schema is defined."
            "override_datasource", "Boolean", "Optional. Default ``false`` When the target Data Source of the Materialized View exists in the Workspace it'll be overriden by the ``datasource`` specified in the request."
            "populate", "Boolean", "Optional. Default ``false``. When ``true``, a job is triggered to populate the destination Data Source."
            "populate_subset", "Float", "Optional. Populate with a subset percent of the data (limited to a maximum of 2M rows), this is useful to quickly test a materialized node with some data. The subset must be greater than 0 and lower than 0.1. A subset of 0.1 means a 10 percent of the data in the source Data Source will be used to populate the Materialized View. Use it together with ``populate=true``, it has precedence over ``populate_condition``"
            "populate_condition", "String", "Optional. Populate with a SQL condition to be applied to the trigger Data Source of the Materialized View. For instance, ``populate_condition='date == toYYYYMM(now())'`` it'll populate taking all the rows from the trigger Data Source which ``date`` is the current month. Use it together with ``populate=true``. ``populate_condition`` is not taken into account if the ``populate_subset`` param is present. Including in the ``populate_condition`` any column present in the Data Source ``engine_sorting_key`` will make the populate job process less data."
            "unlink_on_populate_error", "String", "Optional. Default is ``false``. If the populate job fails the Materialized View is unlinked and new data won't be ingested in the Materialized View."
            "engine", "String", "Optional. Engine for destination Materialized View. Requires the ``type`` parameter as ``materialized``."
            "engine_*", String, "Optional. Engine parameters and options. Requires the ``type`` parameter as ``materialized`` and the ``engine`` parameter. `Check Engine Parameters and Options for more details <api_reference_datasource url_>`_"


        SQL query for the transformation node must be sent in the body encoded in utf-8

        .. csv-table:: Response codes
            :header: "Code", "Description"
            :widths: 20, 80

            "200", "No error"
            "400", "empty or wrong SQL or API param value"
            "403", "Forbidden. Provided token doesn't have permissions to append a node to the pipe, it needs ``ADMIN`` or ``PIPE:CREATE``"
            "404", "Pipe not found"
            "409", "There's another resource with the same name, names must be unique | The Materialized View already exists | ``override_datasource`` cannot be performed"
        """

        workspace = self.get_workspace_from_db()
        pipe = workspace.get_pipe(pipe_name_or_id)

        if not pipe:
            raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))

        try:
            sql_body = self.request.body.decode()
        except UnicodeDecodeError:
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.invalid_encoding())
        datasource = self.get_argument("datasource", None)
        override_datasource = self.get_argument("override_datasource", "false") == "true"
        description = self.get_argument("description", None)
        engine = self.get_argument("engine", None)
        engine_settings = self.get_engine_settings(workspace)
        ignore_sql_errors = self.get_argument("ignore_sql_errors", False) == "true"
        include_datafile = self.get_argument("include_datafile", False) == "true"
        include_schema = self.get_argument("include_schema", "true") == "true"
        is_cli = self.get_argument("cli_version", False)
        is_from_ui = self.get_argument("from", None) == "ui"
        name = self.get_argument("name", None)
        node_type = self.get_argument("type", "standard")
        populate_condition = self.get_argument("populate_condition", None)
        populate_subset = self.get_argument("populate_subset", None)
        sql = self.get_argument("sql", sql_body)
        populate = self.get_argument("populate", "false") == "true"
        with_staging = self.get_argument("with_staging", "false") == "true"
        unlink_on_populate_error = self.get_argument("unlink_on_populate_error", None) == "true"
        edited_by = _calculate_edited_by(self._get_access_info())

        allow_table_functions = node_type in [PipeNodeTypes.COPY, PipeNodeTypes.DEFAULT, PipeNodeTypes.STANDARD]
        try:
            node = await NodeUtils.validate_node(
                workspace=workspace,
                sql=sql,
                pipe=pipe,
                name=name,
                description=description,
                engine_settings=engine_settings,
                datasource=datasource,
                override_datasource=override_datasource,
                populate_subset=populate_subset,
                is_cli=is_cli,
                is_from_ui=is_from_ui,
                include_datafile=include_datafile,
                include_schema=include_schema,
                node_type=node_type,
                ignore_sql_errors=ignore_sql_errors,
                analyze_materialized_view=True,
                check_endpoint=False,
                function_allow_list=workspace.allowed_table_functions() if allow_table_functions else None,
            )
        except ApiHTTPError as e:
            raise e
        except Exception as e:
            logging.exception(e)
            raise ApiHTTPError(500, str(e))

        job = None
        target_datasource = None
        created_datasource = False
        warnings = None

        if node_type == "materialized":
            IS_PIPE_NODE_RESTRICTIONS_ACTIVE = FeatureFlagsWorkspaceService.feature_for_id(
                FeatureFlagWorkspaces.PIPE_NODE_RESTRICTIONS, "", workspace.feature_flags
            )
            if IS_PIPE_NODE_RESTRICTIONS_ACTIVE:
                materialized_nodes = pipe.pipeline.get_materialized_tables()
                if len(materialized_nodes) > 1:
                    raise ApiHTTPError(
                        403,
                        "The pipe already has a materialized view. Pipes can only have one output. Set only one node to materialize and try again.",
                    )

            try:
                job, created_datasource, target_datasource, node, warnings = await self.create_materialized_view(
                    workspace=workspace,
                    node=node,
                    datasource=datasource,
                    override_datasource=override_datasource,
                    sql=sql,
                    pipe=pipe,
                    populate=populate,
                    populate_subset=populate_subset,
                    populate_condition=populate_condition,
                    with_staging=with_staging,
                    is_cli=is_cli,
                    engine=engine,
                    engine_settings=engine_settings,
                    is_from_ui=is_from_ui,
                    include_datafile=include_datafile,
                    include_schema=include_schema,
                    unlink_on_populate_error=unlink_on_populate_error,
                    analyze_materialized_view=False,  # We analyze it before
                    edited_by=edited_by,
                )
            except ApiHTTPError as e:
                raise e
            except Exception as e:
                logging.exception(e)
                raise ApiHTTPError(500, str(e))

        try:
            workspace = await Users.append_node_to_pipe_async(workspace.id, node, pipe.id, edited_by)
            if node_type == "endpoint":
                try:
                    is_cli = self.get_argument("cli_version", False) is not False
                    await NodeUtils.create_endpoint(
                        workspace,
                        pipe_name_or_id,
                        name,
                        edited_by,
                        ignore_sql_errors,
                        self.application.settings["api_host"],
                        is_cli,
                    )

                except Exception as e:
                    raise e
        except PipeNotFound:
            raise ApiHTTPError(
                404, f"Pipe '{pipe_name_or_id}' not found. Has it been deleted in the middle of this operation?"
            )

        pipe = workspace.get_pipe(pipe_name_or_id)
        assert isinstance(pipe, Pipe)

        await PGService(workspace).on_endpoint_changed(pipe)
        response = node.to_json()
        response["url"] = f'{self.application.settings["api_host"]}/v0/pipes/{pipe.name}.json'

        if job:
            response["job"] = job.to_json()
            response["job"]["job_url"] = self.application.settings["api_host"] + "/v0/jobs/" + job.id

        if target_datasource:
            response["datasource"] = target_datasource.to_json()
            response["created_datasource"] = created_datasource

        if warnings:
            response["warnings"] = warnings

        self.write_json(response)


class APIPipeNodeHandler(NodeMaterializationBaseHandler):
    def check_xsrf_cookie(self):
        pass

    @authenticated
    @requires_write_access
    @with_scope(scopes.PIPES_CREATE)
    @read_only_from_ui
    async def put(self, pipe_name_or_id: str, node_name_or_id: str) -> None:
        """
        Changes a particular transformation node in the Pipe

        .. sourcecode:: bash
            :caption: Editing a Pipe's transformation node

            curl -X PUT \\
                -H "Authorization: Bearer <PIPE:CREATE token>" \\
                -d 'select * from node_0' "https://api.tinybird.co/v0/pipes/:name/nodes/:node_id?name=new_name&description=updated_explanation"

        .. csv-table:: Request parameters
            :header: "Key", "Type", "Description"
            :widths: 20, 20, 60

            "name", "String", "new name for the node"
            "description", "String", "new description for the node"
            "token", "String", "Auth token. Ensure it has the ``PIPE:CREATE`` scope on it"

        Please, note that the desired SQL query should be sent in the body encoded in utf-8.

        .. csv-table:: Response codes
            :header: "Code", "Description"
            :widths: 20, 80

            "200", "No error"
            "400", "Empty or wrong SQL"
            "403", "Forbidden. Provided token doesn't have permissions to change the last node to the pipe, it needs ``ADMIN`` or ``PIPE:CREATE``"
            "404", "Pipe not found"
            "409", "There's another resource with the same name, names must be unique"

        """

        workspace = self.get_workspace_from_db()

        pipe = workspace.get_pipe(pipe_name_or_id)
        if not pipe:
            raise ApiHTTPError(404, "pipe not found")

        new_position = self.get_argument("position", None)
        edited_by = _calculate_edited_by(self._get_access_info())

        if new_position:
            try:
                pipe = await Users.change_node_position_async(
                    workspace, pipe_name_or_id, node_name_or_id, new_position, edited_by
                )
            except ValueError as e:
                raise ApiHTTPError(400, str(e))

            self.set_status(200)
            response = pipe.to_json()
            return self.write_json(response)

        try:
            sql_body = self.request.body.decode()
        except UnicodeDecodeError:
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.invalid_encoding())
        sql = self.get_argument("sql", sql_body)

        new_name = self.get_argument("name", None)
        new_description = self.get_argument("description", None)

        if not sql and not new_name and not (new_description is not None):
            raise ApiHTTPError(
                400,
                "Either the body should contain the SQL query to be used, or the name, description, or sql params must be present",
            )

        # check the query is right creating a view and checking errors
        p = pipe.pipeline.clone()
        node = p.get_node(node_name_or_id)
        if not node:
            raise ApiHTTPError(404, f'Node with id "{node_name_or_id}" not found')

        if node.materialized:
            raise ApiHTTPError(403, "Cannot modify a Materialized Node")

        if (
            pipe.pipe_type == PipeTypes.DATA_SINK
            and (data_sink := DataSink.get_by_resource_id(pipe.id, workspace.id))
            and data_sink.service == DataConnectors.KAFKA
        ):
            raise ApiHTTPError(403, "Cannot modify a Kafka Sink Node")

        try:
            if sql or new_name:
                await Users.check_dependent_nodes_by_materialized_node(workspace, node.id)
        except DependentMaterializedNodeOnUpdateException as e:
            logging.warning(
                f"DependentMaterializedNodeOnUpdateException {str(e)} - ws: {workspace.id} - node: {node.id} - pipe: {pipe.id}"
            )
            raise ApiHTTPError(403, str(e))
        except Exception as e:
            logging.exception(
                f"DependentMaterializedNodeOnUpdateException {str(e)} - ws: {workspace.id} - node: {node.id} - pipe: {pipe.id}"
            )

        if new_name:
            try:
                if not Resource.validate_name(new_name):
                    raise ApiHTTPError(400, f'Invalid pipe name "{new_name}". {Resource.name_help(new_name)}')
            except ForbiddenWordException as e:
                raise ApiHTTPError(400, str(e), documentation="/api-reference/api-reference.html#forbidden-names")
            existing_resource = Users.get_resource(workspace, new_name)
            if existing_resource and node != existing_resource and not isinstance(existing_resource, PipeNode):
                raise ApiHTTPError(
                    409,
                    f'There is already a {existing_resource.resource_name} with name "{new_name}". Pipe and Data Source names must be globally unique',
                )

        if sql:
            node.sql = sql
        if new_name:
            node.name = new_name
        if new_description is not None:
            node.description = new_description
        ignore_sql_errors = self.get_argument("ignore_sql_errors", False) == "true"
        try:
            node.ignore_sql_errors = bool(ignore_sql_errors)
            if not ignore_sql_errors:
                await SharedNodeUtils.validate_node_sql(
                    workspace,
                    pipe,
                    node,
                    function_allow_list=(
                        workspace.allowed_table_functions()
                        if pipe.pipe_type in [PipeTypes.COPY, PipeTypes.DEFAULT]
                        else None
                    ),
                )

        except ForbiddenWordException as e:
            raise ApiHTTPError(400, str(e), documentation="/api-reference/api-reference.html#forbidden-names")
        except (ValueError, CHException) as e:
            raise ApiHTTPError(400, str(e))

        try:
            pipe = await Users.update_node_in_pipe_async(
                workspace,
                edited_by,
                pipe_name_or_id,
                node_name_or_id,
                sql,
                new_name,
                new_description,
                ignore_sql_errors,
            )
        except ValueError as e:
            raise ApiHTTPError(400, str(e))
        except NodeNotFound:
            raise ApiHTTPError(404, f"Node '{node_name_or_id}' not found.")

        await PGService(workspace).on_endpoint_changed(pipe)

        node = pipe.pipeline.get_node(new_name or node_name_or_id)

        response = node.to_json()
        response["url"] = f'{self.application.settings["api_host"]}/v0/pipes/{pipe.name}.json'
        self.write_json(response)

    @authenticated
    @requires_write_access
    @with_scope(scopes.PIPES_DROP)
    @read_only_from_ui
    async def delete(self, pipe_name_or_id: str, node_name_or_id: str) -> None:
        """
        Drops a particular transformation node in the Pipe. It does not remove related nodes so this could leave the Pipe in an unconsistent state. For security reasons, enabled nodes can't be removed.

        .. sourcecode:: bash
            :caption: removing a node from a pipe

            curl -X DELETE "https://api.tinybird.co/v0/pipes/:name/nodes/:node_id"

        .. csv-table:: Response codes
            :header: "Code", "Description"
            :widths: 20, 80

            "204", "No error, removed node"
            "400", "The node is published. Published nodes can't be removed"
            "403", "Forbidden. Provided token doesn't have permissions to change the last node of the pipe, it needs ADMIN or IMPORT"
            "404", "Pipe not found"
        """

        workspace = self.get_workspace_from_db()
        pipe = workspace.get_pipe(pipe_name_or_id)

        if not pipe:
            raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))

        p = pipe.pipeline.clone()
        node = p.get_node(node_name_or_id)

        if not node:
            raise ApiHTTPError(404, f"Node '{node_name_or_id}' not found")

        try:
            if not node.materialized:
                await Users.check_dependent_nodes_by_materialized_node(workspace, node.id)
        except DependentMaterializedNodeOnUpdateException as e:
            logging.warning(
                f"DependentMaterializedNodeOnUpdateException {str(e)} - ws: {workspace.id} - node: {node.id} - pipe: {pipe.id}"
            )
            raise ApiHTTPError(403, str(e))
        except Exception as e:
            logging.exception(
                f"DependentMaterializedNodeOnUpdateException {str(e)} - ws: {workspace.id} - node: {node.id} - pipe: {pipe.id}"
            )

        if pipe.pipe_type == PipeTypes.MATERIALIZED:
            await NodeUtils.delete_node_materialized_view(
                workspace,
                node,
                cancel_fn=partial(PipeUtils.cancel_populate_jobs, workspace, node.id, self.application.job_executor),
            )
        edited_by = _calculate_edited_by(self._get_access_info())
        if pipe.pipe_type == PipeTypes.COPY and pipe.copy_node == node.id:
            await NodeUtils.drop_node_copy(workspace, pipe, node.id, edited_by)

        try:
            await Users.drop_node_from_pipe_async(workspace, pipe_name_or_id, node_name_or_id, edited_by)
        except PipeNotFound:
            raise ApiHTTPError(404, "pipe not found")
        except NodeNotFound:
            raise ApiHTTPError(404, f"Node '{node_name_or_id}' not found")
        except EndpointNodesCantBeDropped:
            raise ApiHTTPError(
                400, f"Node '{node_name_or_id}' is an endpoint, unpublish the endpoint before removing the node"
            )

        await PGService(workspace).on_endpoint_changed(pipe)
        self.set_status(204)


class APIPipeListHandler(NodeMaterializationBaseHandler):
    executor = ThreadPoolExecutor(4, thread_name_prefix="api_pipes")

    def check_xsrf_cookie(self):
        pass

    def prepare(self):
        self.pipe_def = None
        if self.request.headers.get("Content-Type", None) == "application/json":
            try:
                self.pipe_def = json_decode(self.request.body)
                if "description" not in self.pipe_def:
                    self.pipe_def["description"] = None
            except json.JSONDecodeError as e:
                raise ApiHTTPError(400, f"invalid JSON line {e.lineno}, column {e.colno}: {e.msg}")

    @authenticated
    @requires_write_access
    @with_scope(scopes.PIPES_CREATE)
    @read_only_from_ui
    async def post(self) -> None:
        """
        Creates a new Pipe. There are 3 ways to create a Pipe

        .. sourcecode:: bash
            :caption: Creating a Pipe providing full JSON

            curl -X POST \\
                -H "Authorization: Bearer <PIPE:CREATE token>" \\
                -H "Content-Type: application/json" \\
                "https://api.tinybird.co/v0/pipes" \\
                -d '{
                    "name":"pipe_name",
                    "description": "my first pipe",
                    "nodes": [
                        {"sql": "select * from my_datasource limit 10", "name": "node_00", "description": "sampled data" },
                        {"sql": "select count() from node_00", "name": "node_01" }
                    ]
                }'

        If you prefer to create the minimum Pipe, and then append your transformation nodes you can set your name and first transformation node's SQL in your POST request

        .. sourcecode:: bash
            :caption: Creating a pipe with a name and a SQL query

            curl -X POST \\
                -H "Authorization: Bearer <PIPE:CREATE token>" \\
                "https://api.tinybird.co/v0/pipes?name=pipename&sql=select%20*%20from%20events"

        Pipes can be also created as copies of other Pipes. Just use the ``from`` argument:

        .. sourcecode:: bash
            :caption: Creating a pipe from another pipe

            curl -X POST \\
                -H "Authorization: Bearer <PIPE:CREATE token>" \\
                "https://api.tinybird.co/v0/pipes?name=pipename&from=src_pipe"

        .. container:: hint

            Bear in mind, if you use this method to overwrite an existing Pipe, the endpoint will only be maintained if the node name is the same.

        """
        source_pipe = None
        workspace = self.get_workspace_from_db()

        pipe_name: str = self.get_argument("name", None)
        pipe_description = self.get_argument("description", None)
        sql = self.get_argument("sql", None)
        populate = self.get_argument("populate", "false") == "true"
        populate_subset = self.get_argument("populate_subset", None)
        populate_condition = self.get_argument("populate_condition", None)
        unlink_on_populate_error = self.get_argument("unlink_on_populate_error", None) == "true"
        # FIXME: use different parameter to set 'from_pipe' https://gitlab.com/tinybird/analytics/-/merge_requests/4280#note_1059605746
        from_pipe = self.get_argument("from", None)
        is_from_ui = self.get_argument("from", None) == "ui"
        is_cli = self.get_argument("cli_version", None)
        ignore_sql_errors = self.get_argument("ignore_sql_errors", False) == "true"
        include_datafile = self.get_argument("include_datafile", False) == "true"
        include_schema = self.get_argument("include_schema", "true") == "true"
        force = self.get_argument("force", "false") == "true"
        edited_by = _calculate_edited_by(self._get_access_info())

        if not self.pipe_def:
            if not pipe_name:
                raise ApiHTTPError(400, "name is empty")
            if not sql and not from_pipe:
                raise ApiHTTPError(
                    400,
                    "source sql and from query are empty. You must set sql so it becomes the first node or a source pipe to copy definition from",
                )
            if sql and from_pipe:
                raise ApiHTTPError(400, "source sql and from can't be set at the same time")

            if sql:
                validate_sql_parameter(sql)
                self.pipe_def = {
                    "name": pipe_name,
                    "description": pipe_description,
                    "nodes": [{"name": f"{pipe_name}_0", "sql": sql}],
                }
            else:
                source_pipe = workspace.get_pipe(from_pipe)
                if not source_pipe:
                    raise ApiHTTPError(400, f"pipe {from_pipe} does not exist")
                # check permissions
                readable_resources = self.get_readable_resources()
                if source_pipe.id not in readable_resources and not self.is_admin():
                    raise ApiHTTPError(403, f"token has no READ scope for {from_pipe}")
                self.pipe_def = source_pipe.to_dict()
                self.pipe_def["name"] = pipe_name
                if pipe_description:
                    self.pipe_def["description"] = pipe_description

        pipe_name = self.pipe_def.get("name")

        # Copy Parameters
        target_datasource_name_or_id = self.pipe_def.get("target_datasource")
        target_workspace_name_or_id = self.pipe_def.get("target_workspace")
        target_token = self.pipe_def.get("target_token")
        schedule_cron = self.pipe_def.get("schedule_cron")

        # Sink mandatory parameters
        connection_name: str = ""
        sink_service: str = ""

        # Stream mandatory parameters
        topic: str = ""

        if not force:
            existing_resource = workspace.get_resource(pipe_name)
            if existing_resource and not isinstance(existing_resource, PipeNode):
                raise ApiHTTPError(
                    409,
                    f'There is already a {existing_resource.resource_name} with name "{pipe_name}". Pipe names must be globally unique',
                )

        # TODO move check to Pipe.validate method when FF is not needed
        IS_PIPE_NODE_RESTRICTIONS_ACTIVE = FeatureFlagsWorkspaceService.feature_for_id(
            FeatureFlagWorkspaces.PIPE_NODE_RESTRICTIONS, "", workspace.feature_flags
        )
        if IS_PIPE_NODE_RESTRICTIONS_ACTIVE:
            materialized_nodes = [
                node for node in self.pipe_def.get("nodes") if node.get("type") == PipeNodeTypes.MATERIALIZED
            ]
            if len(materialized_nodes) > 1:
                raise ApiHTTPError.from_request_error(
                    PipeDefinitionError.more_than_expected_nodes_of_type(node_type=PipeNodeTypes.MATERIALIZED)
                )

        sink_nodes = [
            node
            for node in self.pipe_def.get("nodes")
            if node.get("type", "default").lower() == PipeNodeTypes.DATA_SINK
        ]

        if len(sink_nodes) > 1:
            raise ApiHTTPError.from_request_error(
                PipeDefinitionError.more_than_expected_nodes_of_type(node_type=PipeNodeTypes.DATA_SINK)
            )
        if len(sink_nodes) == 1:
            sink_service = self.get_mandatory_argument_or_raise("service", self.pipe_def)
            connection_name = self.get_mandatory_argument_or_raise("connection", self.pipe_def)

        stream_nodes = [
            node for node in self.pipe_def.get("nodes") if node.get("type", "default").lower() == PipeNodeTypes.STREAM
        ]

        if len(stream_nodes) > 1:
            raise ApiHTTPError.from_request_error(
                PipeDefinitionError.more_than_expected_nodes_of_type(node_type=PipeNodeTypes.STREAM)
            )
        if len(stream_nodes) == 1:
            connection_name = self.get_mandatory_argument_or_raise("connection", self.pipe_def)
            topic = self.get_mandatory_argument_or_raise("kafka_topic", self.pipe_def)

        endpoint_nodes = [
            node
            for node in self.pipe_def.get("nodes")
            if (
                node.get("type", "default").lower() == PipeNodeTypes.ENDPOINT
                or node.get("node_type", "default").lower() == PipeTypes.ENDPOINT.lower()
            )
        ]
        if len(endpoint_nodes) > 1:
            raise ApiHTTPError.from_request_error(
                PipeDefinitionError.more_than_expected_nodes_of_endpoint(node_type=PipeNodeTypes.ENDPOINT)
            )

        copy_nodes = [
            node
            for node in self.pipe_def.get("nodes")
            if node.get("type", "default").lower() == PipeNodeTypes.COPY
            or node.get("node_type", "default").lower() == PipeNodeTypes.COPY
        ]
        if len(copy_nodes) > 1:
            raise ApiHTTPError.from_request_error(
                PipeDefinitionError.more_than_expected_nodes_of_type(node_type=PipeNodeTypes.COPY)
            )

        pipe = workspace.get_pipe(pipe_name)

        materialized_nodes = []
        if pipe:
            materialized_nodes = [node for node in pipe.pipeline.nodes if node.materialized]

        override = bool(pipe and force)
        new_pipe_name = pipe_name if not override else f"{pipe_name}__override"

        if override:
            assert isinstance(pipe, Pipe)

            try:
                branch_mode = BranchMode(
                    self.get_api_option("branch_mode", BRANCH_MODES, default_option=BranchMode.NONE.value)
                )
                if pipe.endpoint and not branch_mode == BranchMode.FORK:
                    await Users.check_dependent_nodes_by_materialized_node(workspace, pipe.endpoint)
            except DependentMaterializedNodeOnUpdateException as e:
                logging.warning(
                    f"DependentMaterializedNodeOnUpdateException {str(e)} - ws: {workspace.id} - node: {pipe.endpoint} - pipe: {pipe.id}"
                )
                raise ApiHTTPError(403, str(e))
            except Exception as e:
                logging.exception(
                    f"DependentMaterializedNodeOnUpdateException {str(e)} - ws: {workspace.id} - node: {pipe.endpoint} - pipe: {pipe.id}"
                )

        try:
            if pipe and pipe.pipe_type == PipeTypes.STREAM:
                raise NodeValidationException("Unlink the stream node before overriding the Pipe")

            Pipe.validate(self.pipe_def)
            nodes: List[Dict[str, Any]] = []

            valid_keys = VALID_NODE_KEYS if not from_pipe else VALID_NODE_COPY_KEYS

            for node in self.pipe_def["nodes"]:
                node_type = node.get("node_type", node.get("type"))
                if node_type == PipeNodeTypes.COPY and not source_pipe:
                    validate_copy_pipe_or_raise(workspace, pipe, schedule_cron, override, node.get("mode"))
                    token_access = self._get_access_info()
                    target_workspace, target_datasource = PipeUtils.parse_copy_parameters(
                        workspace=workspace,
                        token_access=token_access,
                        target_datasource_name_or_id=target_datasource_name_or_id,
                        target_workspace_name_or_id=target_workspace_name_or_id or workspace.id,
                        target_token=target_token,
                    )

                    copy_pipe = Pipe("copy_pipe_for_validation", nodes)
                    pipe_node = PipeNode(node.get("name", ""), node.get("sql", ""), mode=node.get("mode"))
                    template_execution_results = TemplateExecutionResults()
                    node_sql = pipe_node.render_sql(
                        secrets=workspace.get_secrets_for_template(),
                        template_execution_results=template_execution_results,
                    )
                    await PipeUtils.validate_copy_target_datasource(
                        copy_pipe,
                        node_sql,
                        workspace,
                        target_datasource,
                        self.application.settings,
                        target_workspace,
                        function_allow_list=workspace.allowed_table_functions(),
                        template_execution_results=template_execution_results,
                    )

                if Resource.validate_name(node.get("name", "allow_pass_if_no_name")):
                    filtered_node = {k: node.get(k) for k in valid_keys if node.get(k)}
                    engine_settings = NodeUtils.get_engine_settings(node, workspace)
                    filtered_node.update(engine_settings)
                    nodes.append(filtered_node)
                else:
                    node_name = node.get("name", "allow_pass_if_no_name")
                    raise NodeValidationException(f'Invalid node name "{node_name}". {Resource.name_help(node_name)}')
        except ForbiddenWordException as e:
            raise ApiHTTPError(400, str(e), documentation="/api-reference/api-reference.html#forbidden-names")
        except PipeValidationException as e:
            raise ApiHTTPError(400, str(e))
        except NodeValidationException as e:
            raise ApiHTTPError(400, str(e))
        except SQLTemplateCustomError as e:
            self.set_status(e.code)
            self.write(e.err)
            return
        except (SyntaxError, ParseError, UnClosedIfError) as e:
            pipes = workspace.get_used_pipes_in_query(q=node.get("sql"))
            error = process_syntax_error(e, pipes=pipes, pipe_def=self.pipe_def)
            raise ApiHTTPError(400, error, documentation=getattr(e, "documentation", "/query/query-parameters.html"))
        except (ValueError, SQLTemplateException) as e:
            raise ApiHTTPError(400, str(e), documentation=getattr(e, "documentation", "/query/query-parameters.html"))
        except (SQLValidationException, CHException) as e:
            raise ApiHTTPError(400, str(e))

        try:
            override_pipe = workspace.get_pipe(new_pipe_name)
            if override_pipe:
                await Users.drop_pipe_async(workspace, new_pipe_name)
            new_pipe = await Users.add_pipe_async(
                workspace, new_pipe_name, edited_by, nodes=nodes, description=self.pipe_def["description"]
            )
        except ResourceAlreadyExists as e:
            raise ApiHTTPError(409, str(e))
        except ValueError as e:
            raise ApiHTTPError(400, str(e))
        except Exception as e:
            raise ApiHTTPError(400, str(e))
        try:
            await NodeUtils.validate_nodes(
                workspace=workspace,
                pipe=new_pipe,
                nodes=nodes,
                is_cli=is_cli,
                is_from_ui=is_from_ui,
                include_datafile=include_datafile,
                include_schema=include_schema,
                populate_subset=populate_subset,
                ignore_sql_errors=ignore_sql_errors,
                check_endpoint=False,
                analyze_materialized_view=True,
            )
            error_exception = None
        except ForbiddenWordException as e:
            error_exception = ApiHTTPError(
                400, str(e), documentation="/api-reference/api-reference.html#forbidden-names"
            )
        except ApiHTTPError as e:
            error_exception = e
        except Exception as e:
            error_exception = ApiHTTPError(400, str(e))  # FIXME
        finally:
            if error_exception:
                try:
                    for node in new_pipe.pipeline.nodes:
                        await NodeUtils.delete_node_materialized_view(
                            workspace,
                            node,
                            cancel_fn=partial(
                                PipeUtils.cancel_populate_jobs, workspace, node.id, self.application.job_executor
                            ),
                        )
                    await Users.drop_pipe_async(workspace, new_pipe.id)
                except Exception as e:
                    logging.error(
                        f"Orphan pipe: {new_pipe.id} in workspace {workspace.id} while trying to delete an errored pipe in node validations - {str(e)}"
                    )
                raise error_exception

        job = None
        created_datasource = None
        target_datasource = None  # type: ignore
        target_workspace = None
        warnings = None
        materialized_node = None

        if (
            not from_pipe
            and override
            and not populate
            and pipe
            and self._can_alter_table_modify_query(workspace, pipe, new_pipe, nodes)
        ):
            # Instead of creating a new materialized view:
            # Run an ALTER TABLE ... MODIFY QUERY on the existing materialized view
            new_materialized_nodes = [node for node in new_pipe.pipeline.nodes if node.node_type == "materialized"]
            node = materialized_nodes[0]
            new_node = new_materialized_nodes[0]
            try:
                assert pipe
                await self._alter_table_modify_query(
                    workspace,
                    pipe,
                    node,
                    new_pipe,
                    new_node,
                )
                logging.info(
                    "[MODIFY QUERY] Finished alter table ... modify query successfully on ws %s node %s",
                    workspace.name,
                    node.name,
                )
            finally:
                await Users.drop_pipe_async(workspace, new_pipe.id)
        elif not from_pipe:
            try:
                for i, node in enumerate(nodes):
                    guid = new_pipe.pipeline.nodes[i].id
                    if node.get("type", "standard") == "materialized":
                        (
                            job,
                            created_datasource,
                            target_datasource,
                            node,
                            warnings,
                        ) = await self._create_materialized_pipe(
                            node,
                            new_pipe,
                            is_cli,
                            is_from_ui,
                            workspace,
                            populate,
                            populate_subset,
                            populate_condition,
                            unlink_on_populate_error,
                            guid,
                            edited_by,
                        )
                    elif node.get("type", node.get("node_type", "standard")) == PipeNodeTypes.COPY:
                        response = await self._create_copy_pipe(
                            node,
                            workspace,
                            target_datasource_name_or_id,
                            target_workspace_name_or_id,
                            target_token,
                            new_pipe,
                            guid,
                            ignore_sql_errors,
                            schedule_cron,
                            override,
                            pipe,
                            new_pipe_name,
                            edited_by,
                        )
                    elif (
                        node.get("type", "default").lower() == PipeTypes.ENDPOINT.lower()
                        or node.get("node_type", "default").lower() == PipeTypes.ENDPOINT.lower()
                    ):
                        await self._create_endpoint_pipe(new_pipe_name, workspace, node, ignore_sql_errors, edited_by)
                    elif node.get("type", node.get("node_type", "standard")) == PipeNodeTypes.DATA_SINK:
                        await self._create_data_sink_pipe(
                            node=node,
                            workspace=workspace,
                            new_pipe=new_pipe,
                            override=override,
                            pipe=pipe,
                            connection_name=connection_name,
                            service=sink_service,
                            ignore_sql_errors=ignore_sql_errors,
                            new_pipe_name=new_pipe_name,
                            schedule_cron=schedule_cron,
                        )
                    elif node.get("type", node.get("node_type", "standard")) == PipeNodeTypes.STREAM:
                        await self._create_stream_pipe(
                            node=node,
                            workspace=workspace,
                            new_pipe=new_pipe,
                            override=override,
                            pipe=pipe,
                            connection_name=connection_name,
                            topic=topic,
                            ignore_sql_errors=ignore_sql_errors,
                        )

            except Exception as e:
                try:
                    for node in new_pipe.pipeline.nodes:
                        await NodeUtils.delete_node_materialized_view(
                            workspace,
                            node,
                            cancel_fn=partial(
                                PipeUtils.cancel_populate_jobs, workspace, node.id, self.application.job_executor
                            ),
                        )
                    await Users.drop_pipe_async(workspace, new_pipe.id)
                except Exception as exc:
                    logging.error(
                        f"Orphan pipe: {new_pipe.id} in workspace {workspace.id} while trying to delete an errored pipe in materialization - {str(exc)} - original exception: {str(e)}"
                    )
                raise e

            new_pipe = Users.get_pipe(target_workspace or workspace, new_pipe_name)  # type: ignore
            pipe = Users.get_pipe(target_workspace or workspace, pipe_name)
            assert isinstance(pipe, Pipe)
            new_pipe, workspace = await NodeUtils.update_new_pipe_type_when_overriden(  # type: ignore
                materialized_node,  # type: ignore
                new_pipe,
                new_pipe_name,
                override,
                pipe,
                target_datasource,
                target_workspace,  # type: ignore
                workspace,
                edited_by,
            )

            if override:
                if materialized_nodes:
                    # Drop materializations from original pipes
                    try:
                        for materialized_node in materialized_nodes:
                            await NodeUtils.delete_node_materialized_view(
                                workspace,
                                materialized_node,
                                cancel_fn=partial(
                                    PipeUtils.cancel_populate_jobs,
                                    workspace,
                                    materialized_node.id,
                                    self.application.job_executor,
                                ),
                            )
                    except Exception as e:
                        logging.exception(f"Error on delete node on pipe override, possible orphan view: {e}")
                if pipe.pipe_type == PipeTypes.DATA_SINK:
                    node_id: str = pipe.get_sink_node().id
                    await SinkNodeUtils.drop_node_sink_kafka_resources(workspace, node_id)
                if pipe.pipe_type == PipeTypes.COPY and new_pipe.pipe_type == PipeTypes.COPY:
                    await Users.update_source_copy_pipes_tag(
                        target_workspace_id=new_pipe.copy_target_workspace,
                        target_datasource_id=new_pipe.copy_target_datasource,
                        former_workspace_id=pipe.copy_target_workspace,
                        former_datasource_id=pipe.copy_target_datasource,
                        source_pipe_id=pipe.id,
                    )
                if (
                    pipe.pipe_type in [PipeTypes.COPY, PipeTypes.DATA_SINK]
                    and new_pipe.pipe_type not in [PipeTypes.COPY, PipeTypes.DATA_SINK, PipeTypes.DEFAULT]
                    and pipe.get_schedule(workspace.id)
                ):
                    await remove_schedule_data_sink(pipe=pipe, workspace_id=workspace.id)

                await Users.copy_pipeline(workspace, pipe_name, new_pipe_name)
                await Users.drop_pipe_async(workspace, new_pipe.id)

        pipe = Users.get_pipe(workspace, pipe_name)
        assert isinstance(pipe, Pipe)

        if source_pipe:
            try:
                pipe.parent = source_pipe.id
                await Users.alter_pipe(workspace, pipe.id, parent=source_pipe.id, edited_by=edited_by)
            except ResourceAlreadyExists as e:
                raise ApiHTTPError(409, str(e))
            except ValueError as e:
                raise ApiHTTPError(400, str(e))

        workspace = Users.get_by_id(workspace.id)

        await PGService(workspace).on_endpoint_changed(pipe)

        try:
            response = pipe.to_json()
        except (SyntaxError, ParseError, UnClosedIfError, ValueError, SQLTemplateException) as e:
            logging.warning(f"error on pipe.to_json(): {str(e)}")
            response = pipe.to_json(dependencies=False)

        response["url"] = f'{self.application.settings["api_host"]}/v0/pipes/{pipe.name}.json'

        if job:
            response["job"] = job.to_json()
            response["job"]["job_url"] = self.application.settings["api_host"] + "/v0/jobs/" + job.id

        if target_datasource:
            response["datasource"] = target_datasource.to_json()
            response["created_datasource"] = created_datasource
        else:
            materialized_tables = pipe.pipeline.get_materialized_tables()
            # TODO check more than one materialized view and raise error (backwards compatibility check)
            if materialized_tables:
                datasource = workspace.get_datasource(materialized_tables[0])
                assert isinstance(datasource, Datasource)
                response["datasource"] = datasource.to_json()

        if warnings:
            for node in response["nodes"]:
                if node["materialized"]:
                    node["warnings"] = warnings

        self.write_json(response)

    def _can_alter_table_modify_query(
        self, workspace: User, pipe: Pipe, new_pipe: Pipe, node_dicts: List[Dict[str, Any]]
    ):
        if workspace.is_release:
            logging.info(f"[MODIFY QUERY] Workspace {workspace.name} is a release")
            return False
        # check valid pipe
        if pipe.pipe_type != PipeTypes.MATERIALIZED:
            logging.info(f"[MODIFY QUERY] Pipe {pipe.name} is not a materialized pipe")
            return False
        # check one materialized node each
        materialized_nodes = [node for node in pipe.pipeline.nodes if node.materialized]
        if len(materialized_nodes) != 1:
            logging.info(f"[MODIFY QUERY] Pipe {pipe.name} does not have exactly one materialized node")
            return False
        new_materialized_nodes = [
            node for node in new_pipe.pipeline.nodes if node.node_type == PipeNodeTypes.MATERIALIZED
        ]
        if len(new_materialized_nodes) != 1:
            logging.info(f"[MODIFY QUERY] New pipe {new_pipe.name} does not have exactly one materialized node")
            return False
        # check that the datasource does not change
        datasource_id = materialized_nodes[0].materialized
        datasource = Users.get_datasource(workspace, datasource_id)
        if not datasource:
            logging.info(f"[MODIFY QUERY] Datasource {datasource_id} not found")
            return False
        new_materialized_dicts = [node_dict for node_dict in node_dicts if node_dict.get("type") == "materialized"]
        if len(new_materialized_dicts) != 1:
            logging.info(f"[MODIFY QUERY] New pipe {new_pipe.name} does not have exactly one materialized node")
            return False
        new_datasource_name = new_materialized_dicts[0].get("datasource")
        if datasource.name != new_datasource_name:
            logging.info(
                f"[MODIFY QUERY] Datasource {datasource.name} does not match new datasource {new_datasource_name}"
            )
            return False
        # check there are only standard and materialized nodes
        for node in pipe.pipeline.nodes:
            if node.node_type != PipeNodeTypes.MATERIALIZED and node.node_type != PipeNodeTypes.STANDARD:
                logging.info(f"[MODIFY QUERY] Pipe {pipe.name} should only have standard and materialized nodes")
                return False
        for new_node in new_pipe.pipeline.nodes:
            if new_node.node_type != PipeNodeTypes.MATERIALIZED and new_node.node_type != PipeNodeTypes.STANDARD:
                logging.info(f"[MODIFY QUERY] Pipe {new_pipe.name} should only have standard and materialized nodes")
                return False
        logging.info(f"[MODIFY QUERY] Can alter table for materialized pipe {pipe.name}")
        return True

    async def _create_data_sink_pipe(
        self,
        node: dict,
        workspace: User,
        override: bool,
        connection_name: str,
        service: str,
        ignore_sql_errors: bool,
        new_pipe_name: str,
        new_pipe: Pipe,
        pipe: Optional[Pipe] = None,
        schedule_cron: Optional[str] = None,
    ) -> None:
        # Mandatory parameters
        topic: str = ""
        path: str = ""
        file_template: str = ""

        if service == DataConnectors.KAFKA:
            topic = self.get_mandatory_argument_or_raise("kafka_topic", self.pipe_def)
        else:
            path = self.get_mandatory_argument_or_raise("path", self.pipe_def)
            file_template = self.get_mandatory_argument_or_raise("file_template", self.pipe_def)

        file_format: str = self.pipe_def.get("format", "CSV")
        compression = self.pipe_def.get("compression", None)
        write_strategy = self.pipe_def.get("write_strategy", WriteStrategy.NEW)
        api_host = self.application.settings["api_host"]
        workspace = Users.get_by_id(workspace.id)
        new_node = new_pipe.pipeline.get_node(node.get("name"))
        edited_by = _calculate_edited_by(self._get_access_info())
        if not new_node:
            raise ApiHTTPError(400, "Missing node")

        try:
            data_sinkpipe_request = await validate_sink_pipe(
                service=service,
                connection_name=connection_name,
                file_template=file_template,
                file_format=file_format,
                topic=topic,
                ignore_sql_errors=ignore_sql_errors,
                compression=compression,
                new_node=new_node,
                path=path,
                new_pipe=new_pipe,
                schedule_cron=schedule_cron,
                workspace=workspace,
                new_pipe_name=new_pipe_name,
                api_host=api_host,
                original_pipe=pipe,
                override=override,
                write_strategy=write_strategy,
            )

        except ValidationError as e:
            raise ApiHTTPError(400, json.dumps(handle_pydantic_errors(e))) from None

        # remove data sink and or schedule when overriding a sink pipe
        # to create a new sink and schedule if schedule_cron is provided
        # or when creating a sink from a copy pipe that had a schedule
        pipe_schedule = pipe.get_schedule(workspace.id) if pipe else None
        if (override and pipe and pipe.pipe_type == PipeTypes.DATA_SINK) or (
            override and pipe and pipe_schedule and pipe.pipe_type == PipeTypes.COPY
        ):
            await remove_schedule_data_sink(pipe=pipe, workspace_id=workspace.id)
        await create_data_sink_pipe(data_sinkpipe_request, edited_by)

    async def _create_stream_pipe(
        self,
        node: dict,
        workspace: User,
        override: bool,
        connection_name: str,
        topic: str,
        ignore_sql_errors: bool,
        new_pipe: Pipe,
        pipe: Optional[Pipe] = None,
    ) -> None:
        workspace = Users.get_by_id(workspace.id)
        new_node = new_pipe.pipeline.get_node(node.get("name"))
        edited_by = _calculate_edited_by(self._get_access_info())
        if not new_node:
            raise ApiHTTPError(400, "Missing node")

        # remove data sink and or schedule when overriding a sink pipe
        # to create a new sink and schedule if schedule_cron is provided
        # or when creating a sink from a copy pipe that had a schedule
        if override and pipe and pipe.pipe_type == PipeTypes.DATA_SINK:
            await remove_schedule_data_sink(pipe=pipe, workspace_id=workspace.id)

        try:
            data_connector = StreamNodeUtils.get_data_connector(workspace, connection_name)
        except DataConnectorNotFound:
            raise ApiHTTPError(404, "Data Connector not found")

        await StreamNodeUtils.create_stream(
            workspace=workspace,
            data_connector=data_connector,
            pipe=new_pipe,
            node=new_node,
            edited_by=edited_by,
            ignore_sql_errors=ignore_sql_errors,
            kafka_topic=topic,
        )

    async def _create_copy_pipe(
        self,
        node: dict,
        workspace: User,
        target_datasource_name_or_id: str,
        target_workspace_name_or_id: str,
        target_token: str,
        new_pipe: Pipe,
        guid: str,
        ignore_sql_errors: bool,
        schedule_cron: str,
        override: bool,
        pipe: Optional[Pipe],
        new_pipe_name: str,
        edited_by: Optional[str],
    ) -> dict:
        # Adding this here as a workaround to support setting
        # Copy Nodes from POST /v0/pipes
        data_sink = None
        try:
            workspace = Users.get_by_id(workspace.id)
            token_access = self._get_access_info()
            target_workspace, target_datasource = PipeUtils.parse_copy_parameters(
                workspace=workspace,
                token_access=token_access,
                target_datasource_name_or_id=target_datasource_name_or_id,
                target_workspace_name_or_id=target_workspace_name_or_id or workspace.id,
                target_token=target_token,
            )
            if not target_workspace:
                raise ApiHTTPError(404, "No target workspace found")

            response = await NodeUtils.create_node_copy(
                workspace=workspace,
                pipe_name_or_id=new_pipe.id,
                node_name_or_id=guid,
                target_datasource_id=target_datasource.id,
                mode=node.get("mode", CopyModes.APPEND),
                edited_by=edited_by,
                target_workspace_id=target_workspace.id,
                ignore_sql_errors=ignore_sql_errors,
            )

            if schedule_cron:
                api_host = self.application.settings["api_host"]
                # remove sink's or copy's schedule before creating copy's schedule for original pipe
                if (
                    override
                    and pipe
                    and pipe.pipe_type in [PipeTypes.DATA_SINK, PipeTypes.COPY]
                    and pipe.get_schedule(workspace_id=workspace.id)
                ):
                    await remove_schedule_data_sink(pipe=pipe, workspace_id=target_workspace.id)
                schedule_pipe = pipe if override else new_pipe
                assert isinstance(schedule_pipe, Pipe)
                data_sink = await create_copy_schedule_sink(
                    workspace, schedule_pipe, api_host, cron=schedule_cron, mode=node.get("mode", CopyModes.APPEND)
                )
        except (SyntaxError, ParseError, UnClosedIfError) as e:
            error = SQLPipeError.error_sql_template(
                error_message=str(e), pipe_name=new_pipe_name, node_name=node.get("name")
            )
            raise ApiHTTPError(400, error, documentation=getattr(e, "documentation", "/query/query-parameters.html"))
        except (ValueError, SQLTemplateException) as e:
            raise ApiHTTPError(400, str(e), documentation=getattr(e, "documentation", "/query/query-parameters.html"))
        except SQLValidationException as e:
            raise ApiHTTPError(400, str(e))
        except GCloudScheduleException as e:
            raise ApiHTTPError(e.status, str(e), documentation="/api-reference/schedule-api.html")
        except ApiHTTPError as e:
            if data_sink is not None:
                await data_sink.delete()
            raise ApiHTTPError(e.status_code, e.log_message, e.documentation)
        except Exception as e:
            logging.exception(f"Could not create copy node in pipe error: {e}")
            if data_sink is not None:
                await data_sink.delete()
            raise ApiHTTPError(
                500,
                "Could not create copy pipe, kindly contact us at support@tinybird.co if you need assistance",
            )
        return response

    async def _create_endpoint_pipe(
        self, new_pipe_name: str, workspace: User, node: dict, ignore_sql_errors: bool, edited_by: Optional[str]
    ) -> dict:
        is_cli = self.get_argument("cli_version", False) is not False
        workspace = Users.get_by_id(workspace.id)
        return await NodeUtils.create_endpoint(
            workspace,
            new_pipe_name,
            node["name"],
            edited_by,
            ignore_sql_errors,
            self.application.settings["api_host"],
            is_cli,
        )

    async def _create_materialized_pipe(
        self,
        node: dict,
        new_pipe: Pipe,
        is_cli: bool,
        is_from_ui: bool,
        workspace: User,
        populate: bool,
        populate_subset: str,
        populate_condition: str,
        unlink_on_populate_error: bool,
        guid: str,
        edited_by: Optional[str],
    ) -> Tuple[PopulateJob, bool, Datasource, PipeNode, Any]:
        name = node.get("name")
        sql = node.get("sql")
        description = node.get("description")
        datasource = node.get("datasource", None)
        override_datasource = node.get("override_datasource", "false") == "true"
        engine = node.get("engine", None)
        engine_settings = NodeUtils.get_engine_settings(node, workspace)

        node_populate = node.get("populate", "false") == "true" if node.get("populate", None) else populate
        node_populate_subset = node.get("populate_subset") if node.get("populate_subset", None) else populate_subset
        node_populate_condition = (
            node.get("populate_condition") if node.get("populate_condition", None) else populate_condition
        )
        node_unlink_on_populate_error = unlink_on_populate_error
        if should_unlink := node.get("unlink_on_populate_error", None):
            node_unlink_on_populate_error = should_unlink == "true"

        with_staging = node.get("with_staging", "false") == "true"
        materialized_node = PipeNode(name, sql, guid=guid, description=description)

        job, created_datasource, target_datasource, node_returned, warnings = await self.create_materialized_view(
            workspace=workspace,
            node=materialized_node,
            datasource=datasource,
            override_datasource=override_datasource,
            sql=sql,
            pipe=new_pipe,
            populate=node_populate,
            populate_subset=node_populate_subset,
            populate_condition=node_populate_condition,
            with_staging=with_staging,
            is_cli=is_cli,
            engine=engine,
            engine_settings=engine_settings,
            is_from_ui=is_from_ui,
            analyze_materialized_view=False,
            unlink_on_populate_error=node_unlink_on_populate_error,
            edited_by=edited_by,
        )
        job = cast(PopulateJob, job)
        target_datasource = cast(Datasource, target_datasource)

        return job, created_datasource, target_datasource, node_returned, warnings

    async def _alter_table_modify_query(
        self,
        workspace: User,
        pipe: Pipe,
        node: PipeNode,
        new_pipe: Pipe,
        new_node: PipeNode,
    ) -> None:
        new_sql = new_node.sql
        target_database = workspace.database
        target_table = node.id
        try:
            # As we are going to modify the MV atomically, we do not need to add the backfill column & value to do the populate
            sql, _ = await workspace.replace_tables_async(
                new_sql,
                pipe=new_pipe,
                use_pipe_nodes=True,
                extra_replacements={},
                template_execution_results=TemplateExecutionResults(),
                release_replacements=True,
            )
            await ch_alter_table_modify_query(
                workspace,
                target_database,
                target_table,
                sql,
                **workspace.ddl_parameters(skip_replica_down=True),
            )
        except CHException as ch_exception:
            if ch_exception.code == CHErrors.TIMEOUT_EXCEEDED:
                logging.exception(
                    f"[DESYNC-MV] Workspace {workspace.id}: could not run ALTER TABLE ... MODIFY QUERY in {target_database}.{target_table} with SQL {sql}, possible outdated definition in Redis"
                )
                raise ApiHTTPError(500, "Operation timed out, please retry to ensure consistency.")
            logging.warning(f"CH exception modifying query: {ch_exception}")
            raise ApiHTTPError(400, str(ch_exception))
        except QueryNotAllowed as exc:
            logging.warning(f"Query not allowed modifying query: {exc}")
            raise ApiHTTPError(403, str(exc))
        except (ValueError, SQLTemplateException) as exc:
            logging.warning(f"Value error not allowed modifying query: {exc}")
            raise ApiHTTPError(
                400, str(exc), documentation=getattr(exc, "documentation", "/query/query-parameters.html")
            )

        try:
            # copy relevant materialization data from old node to new node
            new_node.id = node.id
            new_node.materialized = node.materialized
            await Users.update_pipe_async(workspace, new_pipe)
            await Users.copy_pipeline(workspace, pipe.name, new_pipe.name)
        except Exception:
            logging.exception(
                f"[DESYNC-MV] Workspace {workspace.id}: Could not copy pipe {new_pipe.name} in pipe {pipe.name} with SQL {new_sql}, possible outdated definition in Redis"
            )
            raise ApiHTTPError(500, "Operation partially executed, please retry to ensure consistency.")

    def get_mandatory_argument_or_raise(self, argument_name, pipe_def: Dict[str, str]):
        argument_value = self.pipe_def.get(argument_name, None)
        if not argument_value:
            raise ApiHTTPError.from_request_error(DataSinkError.missing_parameter(parameter_name=argument_name))

        return argument_value

    @run_on_executor
    def _get_pipes(
        self,
        project: Optional[str],
        dependencies: bool = False,
        attrs: Optional[List[str]] = None,
        node_attrs: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        workspace = self.get_workspace_from_db()
        pipes = workspace.get_pipes()

        limited_representation = False
        if project:
            pipes = [x for x in pipes if x["project"] == project]  # type: ignore
        if not self.is_admin() and not self.has_scope(scopes.PIPES_CREATE):
            access_info = self._get_access_info()
            assert isinstance(access_info, AccessToken)
            token_pipes = access_info.get_resources_for_scope(scopes.PIPES_READ)
            pipes = [t for t in pipes if t.id in token_pipes]
            limited_representation = True

        response_pipes = []

        for pipe in pipes:
            response = pipe.to_json(
                dependencies=dependencies,
                attrs=attrs,
                node_attrs=node_attrs,
                limited_representation=limited_representation,
            )
            response["url"] = f'{self.application.settings["api_host"]}/v0/pipes/{pipe.name}.json'
            response_pipes.append(response)

        return response_pipes

    @authenticated
    async def get(self) -> None:
        """
        Get a list of pipes in your account.

        .. code-block:: bash
            :caption: getting a list of your pipes

            curl -X GET \\
                -H "Authorization: Bearer <PIPE:CREATE token>" \\
                "https://api.tinybird.co/v0/pipes"

        Pipes in the response will be the ones that are accessible using a particular token with read permissions for them.

        .. code-block:: json
            :caption: Successful response

            {
                "pipes": [{
                    "id": "t_55c39255e6b548dd98cb6da4b7d62c1c",
                    "name": "my_pipe",
                    "description": "This is a description",
                    "endpoint": "t_h65c788b42ce4095a4789c0d6b0156c3",
                    "created_at": "2022-11-10 12:39:38.106380",
                    "updated_at": "2022-11-29 13:33:40.850186",
                    "parent": null,
                    "nodes": [{
                        "id": "t_h65c788b42ce4095a4789c0d6b0156c3",
                        "name": "my_node",
                        "sql": "SELECT col_a, col_b FROM my_data_source",
                        "description": null,
                        "materialized": null,
                        "cluster": null,
                        "tags": {},
                        "created_at": "2022-11-10 12:39:47.852303",
                        "updated_at": "2022-11-10 12:46:54.066133",
                        "version": 0,
                        "project": null,
                        "result": null,
                        "ignore_sql_errors": false
                        "node_type": "default"
                    }],
                    "url": "https://api.tinybird.co/v0/pipes/my_pipe.json"
                }]
            }

        .. csv-table:: Request parameters
            :header: "Key", "Type", "Description"
            :widths: 20, 20, 60

            "dependencies", "boolean", "The response will include the nodes dependent data sources and pipes, default is ``false``"
            "attrs", "String", "comma separated list of the pipe attributes to return in the response. Example: ``attrs=name,description``"
            "node_attrs", "String", "comma separated list of the node attributes to return in the response. Example ``node_attrs=id,name``"

        .. container:: hint

            Pipes id's are immutable so you can always refer to them in your 3rd party applications to make them compatible with Pipes once they are renamed.

        .. container:: hint

            For lighter JSON responses consider using the ``attrs`` and ``node_attrs`` params to return exactly the attributes you need to consume.

        """
        project = self.get_argument("project", None)

        attrs = self.get_argument("attrs", None)
        node_attrs = self.get_argument("node_attrs", None)

        if attrs:
            attrs = attrs.split(",")

        if node_attrs:
            node_attrs = node_attrs.split(",")

        try:
            dependencies = bool(util.strtobool(self.get_argument("dependencies", "false")))
        except Exception:
            err = ClientErrorBadRequest.invalid_parameter(
                parameter="dependencies", value=self.get_argument("dependencies", "false"), valid="'true', 'false'"
            )
            raise ApiHTTPError.from_request_error(err)

        try:
            response_pipes = await self._get_pipes(
                project, dependencies=dependencies, attrs=attrs, node_attrs=node_attrs
            )
            self.write_json({"pipes": response_pipes})
        except Exception as e:
            raise ApiHTTPError(400, str(e))


class APIPipeDataHandler(APIQueryHandler):
    @authenticated
    @check_plan_limit(Limit.build_plan_api_requests)
    @check_organization_limit()
    @check_workspace_limit(Limit.workspace_api_requests)
    @check_endpoint_rps_limit()
    @check_endpoint_concurrency_limit()
    async def get(self, pipe_name_or_id, fmt):
        """
        Returns the published node data in a particular format.

        .. code-block:: bash
            :name: pipe-get-data
            :caption: Getting data for a pipe

            curl -X GET \\
                -H "Authorization: Bearer <PIPE:READ token>" \\
                "https://api.tinybird.co/v0/pipes/:name.format"

        .. csv-table:: Request parameters
            :name: pipe-q-parameter
            :header: "Key", "Type", "Description"
            :widths: 20, 20, 60

            "q", "String", "Optional, query to execute, see API Query endpoint"
            "output_format_json_quote_64bit_integers", "int", "(Optional) Controls quoting of 64-bit or bigger integers (like UInt64 or Int128) when they are output in a JSON format. Such integers are enclosed in quotes by default. This behavior is compatible with most JavaScript implementations. Possible values: 0 — Integers are output without quotes. 1 — Integers are enclosed in quotes. Default value is 0"
            "output_format_json_quote_denormals", "int", "(Optional) Controls representation of inf and nan on the UI instead of null e.g when dividing by 0 - inf and when there is no representation of a number in Javascript - nan. Possible values: 0 - disabled, 1 - enabled. Default value is 0"
            "output_format_parquet_string_as_string", "int", "(Optional) Use Parquet String type instead of Binary for String columns. Possible values: 0 - disabled, 1 - enabled. Default value is 0"

        .. container:: hint

            The ``q`` parameter is a SQL query (see `Query API <api_reference_query url_>`_). When using this endpoint to query your Pipes, you can use the ``_`` shortcut, which refers to your Pipe name

        .. csv-table:: Available formats
            :name: pipe-format-parameter
            :header: "format", "Description"
            :widths: 20, 80

            "csv", "CSV with header"
            "json", "JSON including data, statistics and schema information"
            "ndjson", "One JSON object per each row"
            "parquet", "A Parquet file. Some libraries might not properly process ``UInt*`` data types, if that's your case cast those columns to signed integers with ``toInt*`` functions. ``String`` columns are exported as ``Binary``, take that into account when reading the resulting Parquet file, most libraries convert from Binary to String (e.g. Spark has this configuration param: ``spark.sql.parquet.binaryAsString``)"
            "prometheus", "Prometheus text-based format. The output table must include name (String) and value (number) as required columns, with optional help (String), timestamp (number), and type (String) (valid values: counter, gauge, histogram, summary, untyped, or empty). Labels should be a Map(String, String), and rows for the same metric with different labels must appear consecutively. The table must be sorted by the name column."
        """
        await self.run_request(pipe_name_or_id, fmt)

    @authenticated
    @requires_write_access
    @check_plan_limit(Limit.build_plan_api_requests)
    @check_organization_limit()
    @check_workspace_limit(Limit.workspace_api_requests)
    @check_endpoint_rps_limit()
    @check_endpoint_concurrency_limit()
    async def post(self, pipe_name_or_id, fmt):
        """
        Returns the published node data in a particular format, passing the parameters in the request body. Use this endpoint when the query is too long to be passed as a query string parameter.

        When using the post endpoint, there are no traces of the parameters in the pipe_stats_rt Data Source.

        See the get endpoint for more information.
        """
        await self.run_request(pipe_name_or_id, fmt, with_post=True)

    async def run_request(self, pipe_name_or_id: str, fmt: str, with_post: bool = False):
        t_start = time.time()

        try:
            if not Resource.validate_name(pipe_name_or_id):
                raise ApiHTTPError(400, "Invalid pipe name")
        except ForbiddenWordException:
            # at this point the endpoint has been already created, let's just pass this error
            # it's very likely the above validation is not needed
            pass

        fmts = {
            "csv": "CSVWithNames",
            "json": "JSON",
            "ndjson": "JSONEachRow",
            "parquet": "Parquet",
            "prometheus": "Prometheus",
        }
        if fmt.lower() not in fmts:
            raise ApiHTTPError(400, f"Format '{fmt}' not supported, it must be one of {', '.join(fmts.keys())}")

        workspace = self.get_workspace_from_db()

        endpoint_user_profile = workspace.profiles.get(WorkspaceUserProfiles.ENDPOINT_USER_PROFILE.value, None)

        pipe = workspace.get_pipe(pipe_name_or_id)
        if not pipe:
            raise ApiHTTPError(404, f"The pipe '{pipe_name_or_id}' does not exist")

        access_token = self._get_access_info()

        if (
            not self.is_admin()
            and access_token is not None
            and pipe.id not in access_token.get_resources_for_scope(scopes.PIPES_READ)
        ):
            raise ApiHTTPError.from_request_error(ClientErrorForbidden.token_doesnt_have_access_to_this_resource())

        if not pipe.endpoint:
            raise ApiHTTPError(
                404,
                f"The pipe '{pipe.name}' does not have an endpoint yet",
                documentation="/api-reference/pipe-api.html",
            )

        from_param = self.get_argument("from", None)

        q = self.get_argument("q", None, True)
        if q:
            validate_sql_parameter(q)
            if q[0] == "%":
                raise ApiHTTPError(400, "'q' parameter doesn't support templates")

            query = f"{q} FORMAT {fmts[fmt.lower()]}"
        else:
            query = f"SELECT * from {pipe.name} FORMAT {fmts[fmt.lower()]}"

        max_threads = self._get_max_threads_param()
        output_format_json_quote_64bit_integers = self._get_output_format_json_quote_64bit_integers()
        output_format_json_quote_denormals = self._get_output_format_json_quote_denormals()
        output_format_parquet_string_as_string = self._get_output_format_parquet_string_as_string()

        if with_post:
            (_, variables) = get_variables_for_query(self.request, from_param=None, filter_sql_params=False)
        else:
            variables = filter_query_variables(self.request.query_arguments, filter_sql_params=False)
            variables = {k: v[0].decode() for k, v in variables.items()}  # type: ignore

        # save pipe_id in the tag so it can be used to get the real from spans table
        # the url could contain the id or the pipe name (and if it's renamed you can lose the track)
        parameters = variables if variables else {}
        fixed_params = access_token.get_fixed_params().get(pipe.id) if access_token else None
        if fixed_params:
            parameters.update(fixed_params)
            variables = {**variables, **fixed_params} if variables else fixed_params

        self.set_span_tag({"pipe_id": pipe.id, "pipe_name": pipe.name, "parameters": parameters})

        try:
            main_workspace = workspace.get_main_workspace()
            resource_tags = [tag.name for tag in main_workspace.get_tags_by_resource(pipe.id, pipe.name)]
            if len(resource_tags) > 0:
                self.set_span_tag({"resource_tags": resource_tags})
        except Exception:
            pass

        if endpoint_user_profile:
            self.set_span_tag({"user_profile": endpoint_user_profile})

        if q:
            secrets = workspace.get_secrets_for_template() if self.is_admin() else None
        else:
            secrets = workspace.get_secrets_for_template()

        return await self._query(
            query,
            pipe_name_or_id,
            max_threads,
            variables=variables,
            t_start=t_start,
            query_id=self._request_id,
            output_format_json_quote_64bit_integers=output_format_json_quote_64bit_integers,
            output_format_json_quote_denormals=output_format_json_quote_denormals,
            output_format_parquet_string_as_string=output_format_parquet_string_as_string,
            finalize_aggregations=False,
            from_param=from_param,
            user=endpoint_user_profile,
            fallback_user_auth=True,
            secrets=secrets,
        )


class APIPipeLastUpdateHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @authenticated
    async def get(self, pipe_name_or_id: str) -> None:
        """
        Get pipe last update information. Provided Auth Token must have read access to the Pipe.

        .. code-block:: bash
            :caption: Getting last update information about a particular pipe

            curl -X GET \\
                -H "Authorization: Bearer <PIPE:READ token>" \\
                "https://api.tinybird.co/v0/pipes/:name/last_update"

        ``pipe_id`` and ``pipe_name`` are two ways to refer to the pipe in SQL queries and API endpoints the only difference is ``pipe_id`` never changes so it'll work even if you change the ``pipe_name`` (which is the name used to display the pipe). In general you can use ``pipe_id`` or ``pipe_name`` indistinctly:

        .. code-block:: json
            :caption: Successful response

            {
                "id": "t_bd1c62b5e67142bd9bf9a7f113a2b6ea",
                "name": "events_pipe",
                "edited_by": "your@email.com"
                "updated_at": "2024-09-20 10:36:06.190338",
            }

        """
        workspace = self.get_workspace_from_db()
        allowed_attrs = ["id", "name", "edited_by", "updated_at"]

        if pipe_name_or_id:
            pipe = Users.get_pipe(workspace, pipe_name_or_id)
            if pipe:
                readable_resources = self.get_readable_resources()
                can_read_all_pipes = self.is_admin() or self.has_scope(scopes.PIPES_CREATE)
                if pipe.id not in readable_resources and not can_read_all_pipes:
                    raise ApiHTTPError(403, f"token has no READ scope for {pipe_name_or_id}")

                limited_representation = not can_read_all_pipes

                response = pipe.to_json(attrs=allowed_attrs, limited_representation=limited_representation)
                self.write_json(response)
            else:
                raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))


class APIPipeHandler(NodeMaterializationBaseHandler):
    def check_xsrf_cookie(self):
        pass

    @authenticated
    async def get(self, pipe_name_or_id: str) -> None:
        """
        Get pipe information. Provided Auth Token must have read access to the Pipe.

        .. code-block:: bash
            :caption: Getting information about a particular pipe

            curl -X GET \\
                -H "Authorization: Bearer <PIPE:READ token>" \\
                "https://api.tinybird.co/v0/pipes/:name"

        ``pipe_id`` and ``pipe_name`` are two ways to refer to the pipe in SQL queries and API endpoints the only difference is ``pipe_id`` never changes so it'll work even if you change the ``pipe_name`` (which is the name used to display the pipe). In general you can use ``pipe_id`` or ``pipe_name`` indistinctly:

        .. code-block:: json
            :caption: Successful response

            {
                "id": "t_bd1c62b5e67142bd9bf9a7f113a2b6ea",
                "name": "events_pipe",
                "pipeline": {
                    "nodes": [{
                        "name": "events_ds_0"
                        "sql": "select * from events_ds_log__raw",
                        "materialized": false
                    }, {
                        "name": "events_ds",
                        "sql": "select * from events_ds_0 where valid = 1",
                        "materialized": false
                    }]
                }
            }

        .. container:: hint

            You can make your Pipe's id more descriptive by prepending information such as ``t_my_events_table.bd1c62b5e67142bd9bf9a7f113a2b6ea``

        """
        workspace = self.get_workspace_from_db()
        cli_version = self._get_cli_version()

        if pipe_name_or_id:
            pipefile = False
            if pipe_name_or_id.endswith(".pipe"):
                pipe_name_or_id = pipe_name_or_id.rsplit(".", 1)[0]
                pipefile = True

            pipe = Users.get_pipe(workspace, pipe_name_or_id)
            if pipe:
                readable_resources = self.get_readable_resources()
                can_read_all_pipes = self.is_admin() or self.has_scope(scopes.PIPES_CREATE)
                if pipe.id not in readable_resources and not can_read_all_pipes:
                    raise ApiHTTPError(403, f"token has no READ scope for {pipe_name_or_id}")

                limited_representation = not can_read_all_pipes

                if pipefile:
                    if limited_representation:
                        raise ApiHTTPError(
                            403,
                            f"token needs at least CREATE scope to retrieve the pipefile representation {pipe_name_or_id}",
                        )
                    is_cli_with_tags_enabled = cli_version is None or cli_version > version.parse("5.7.0")
                    self.set_header("content-type", "text/plain")
                    content = await generate_pipe_datafile(
                        pipe, workspace, tags_cli_support_enabled=is_cli_with_tags_enabled
                    )
                    self.write(content)
                else:
                    self.set_header("content-type", "application/json")
                    response = pipe.to_json(limited_representation=limited_representation)
                    response["url"] = f'{self.application.settings["api_host"]}/v0/pipes/{pipe.name}.json'
                    self.write_json(response)
            else:
                raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))

    @authenticated
    @requires_write_access
    @with_scope(scopes.PIPES_CREATE)
    @read_only_from_ui
    async def put(self, pipe_name_or_id: str) -> None:
        """
        Changes Pipe's metadata. When there is another Pipe with the same name an error is raised.

        .. sourcecode:: bash
            :caption: editing a pipe

            curl -X PUT \\
                -H "Authorization: Bearer <PIPE:CREATE token>" \\
                "https://api.tinybird.co/v0/pipes/:name?name=new_name"

        .. csv-table:: Request parameters
            :header: "Key", "Type", "Description"
            :widths: 20, 20, 60

            "name", "String", "new name for the pipe"
            "description", "String", "new Markdown description for the pipe"
            "token", "String", "Auth token. Ensure it has the ``PIPE:CREATE`` scope on it"
        """

        workspace = self.get_workspace_from_db()

        pipe = workspace.get_pipe(pipe_name_or_id)
        if not pipe:
            raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))

        old_id = pipe.id

        new_name = self.get_argument("name", None, True)
        new_description = self.get_argument("description", None)

        try:
            if pipe.endpoint:
                await Users.check_dependent_nodes_by_materialized_node(workspace, pipe.endpoint)
        except DependentMaterializedNodeOnUpdateException as e:
            logging.warning(
                f"DependentMaterializedNodeOnUpdateException {str(e)} - ws: {workspace.id} - node: {pipe.endpoint} - pipe: {pipe.id}"
            )
            raise ApiHTTPError(403, str(e))
        except Exception as e:
            logging.exception(
                f"DependentMaterializedNodeOnUpdateException {str(e)} - ws: {workspace.id} - node: {pipe.endpoint} - pipe: {pipe.id}"
            )

        try:
            edited_by = _calculate_edited_by(self._get_access_info())
            pipe = await Users.alter_pipe(workspace, pipe_name_or_id, new_name, new_description, edited_by=edited_by)
            assert isinstance(pipe, Pipe)
            await PGService(workspace).on_pipe_renamed(old_id, pipe)
        except ResourceAlreadyExists as e:
            raise ApiHTTPError(409, str(e))
        except ValueError as e:
            raise ApiHTTPError(400, str(e))

        response = pipe.to_json()
        response["url"] = f'{self.application.settings["api_host"]}/v0/pipes/{pipe.name}.json'

        self.write_json(response)

    @authenticated
    @requires_write_access
    @read_only_from_ui
    async def delete(self, pipe_name_or_id: str) -> None:
        """
        Drops a Pipe from your account. Auth token in use must have the ``DROP:NAME`` scope.

        .. code-block:: bash
            :caption: Dropping a pipe

            curl -X DELETE \\
                -H "Authorization: Bearer <PIPE:CREATE token>" \\
                "https://api.tinybird.co/v0/pipes/:name"

        """
        workspace = self.get_workspace_from_db()
        pipe = Users.get_pipe(workspace, pipe_name_or_id)
        edited_by = _calculate_edited_by(self._get_access_info())
        if not pipe:
            raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))

        if self.is_admin() or pipe.id in self.get_dropable_resources():
            try:
                await PipeUtils.delete_pipe(
                    workspace, pipe, self.application.job_executor, edited_by, hard_delete=False
                )
                self.set_status(204)
            except DependentMaterializedNodeOnUpdateException as e:
                raise ApiHTTPError(403, str(e))
            except PipeNotFound:
                raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))
        else:
            raise ApiHTTPError.from_request_error(PipeClientErrorForbidden.no_drop_scope())


class APIPipeRequestsHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @authenticated
    @with_scope(scopes.PIPES_CREATE)
    async def get(self, pipe_name_or_id: str) -> None:
        """
        Get information about the requests made to a particular pipe during the last 3 months. Provided Auth Token must have read access to the Pipe.

        .. code-block:: bash
            :caption: Getting pipe requests information.

            curl -X GET "https://api.tinybird.co/v0/pipes/:name/requests"

        .. code-block:: json
            :caption: Successful response

            {
                "requests": {
                    "top": [
                        {
                            "endpoint_url": "https://api.tinybird.co/v0/pipes/your_pipe.json?date_start=2019-01-01&date_end=2019-10-18",
                            "requests_count": 18,
                            "avg_duration": 0.1301900545756022
                        },
                        {
                            "endpoint_url": "https://api.tinybird.co/v0/pipes/your_pipe.json?date_start=2017-01-01&date_end=2020-12-31",
                            "requests_count": 12,
                            "avg_duration": 0.15853595733642578
                        }
                    ]
                }
            }

        .. csv-table:: Response codes
            :header: "Code", "Description"
            :widths: 20, 80

            "200", "No error"
            "404", "Pipe not found"
            "403", "Forbidden. Provided token doesn't have permissions to publish a pipe, it needs ``ADMIN`` or ``PIPE:CREATE``"
            "500", "Internal error. Could not compute requests metrics."
        """

        # This endpoint is deprecated and shouldn't be used
        # TODO: Review in Spans if we still get requests and remove the handler in case we don't have any more requests

        workspace = self.get_workspace_from_db()

        pipe = Users.get_pipe(workspace, pipe_name_or_id)
        if not pipe:
            raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))

        self.write_json({"requests": {"top": []}})


class APIPipesOpenAPIHandler(BaseHandler):
    @authenticated
    @with_scope(scopes.PIPES_READ)
    async def get(self):
        """
        .. code-block:: bash
            :caption: get an OpenAPI definition of your pipes

            curl -X GET "https://api.tinybird.co/v0/pipes/openapi.json"

        Get an OpenAPI definition of Pipes in your account.

        .. container:: hint

            The pipes in the response will be the ones that are accessible using a particular token with read permissions for them.

        .. code-block:: json
            :caption: Successful response

            {
                "openapi": "3.0",
                "info": {}
                "host": "",
                ...
            }

        """
        self.set_header("content-type", "application/json")

        workspace = self.get_workspace_from_db()

        pipes = Users.get_pipes(workspace)
        token = self._get_access_info()
        show_examples = self.get_argument("examples", OpenAPIExampleTypes.FAKE)
        optional_fields = self.get_argument("optional_fields", "false") == "true"

        if not self.is_admin():
            resources = self.get_readable_resources()
            pipes = [pipe for pipe in pipes if pipe.id in resources]

        try:
            response = await generate_openapi_endpoints_response(
                settings=self.application.settings,
                workspace=workspace,
                pipes=pipes,
                token=token,
                show_examples=show_examples,
                optional_fields=optional_fields,
            )

            self.write_json(response)
        except Exception as e:
            logging.exception(f"Could not get endpoint information: {e}")
            raise ApiHTTPError(500, f"Could not get endpoint information: {e}")


class APIPipeWithDataHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @authenticated
    async def get(self, pipe_name_or_id):
        workspace = self.get_workspace_from_db()

        pipe = Users.get_pipe(workspace, pipe_name_or_id)
        output_format_json_quote_64bit_integers = self.get_argument("output_format_json_quote_64bit_integers", 0)
        output_format_json_quote_denormals = self.get_argument("output_format_json_quote_denormals", 0)
        finalize_aggregations = self.get_argument("finalize_aggregations", False) == "true"

        if pipe:
            # generate a new pipe
            readable_resources = None
            use_pipe_nodes = False
            if not self.is_admin():
                readable_resources = self.get_readable_resources()
            else:
                use_pipe_nodes = True
            filters = self._get_access_info().get_filters()
            variables = {k: v[0].decode() for k, v in self.request.query_arguments.items()}
            new_pipe = await PipeUtils.generate_clone_pipe_with_data(
                pipe,
                workspace,
                filters,
                readable_resources,
                use_pipe_nodes,
                variables,
                output_format_json_quote_64bit_integers=output_format_json_quote_64bit_integers,
                output_format_json_quote_denormals=output_format_json_quote_denormals,
                finalize_aggregations=finalize_aggregations,
            )
            self.render_data(new_pipe)
        else:
            raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))


class APIPipeCopyHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    def log_copy_error(
        self,
        workspace: "User",
        pipe: "Pipe",
        copy_timestamp: datetime,
        error,
        datasource: Optional["Datasource"] = None,
    ):
        try:
            resource_tags: List[str] = []
            if workspace and datasource:
                resource_tags = [tag.name for tag in workspace.get_tags_by_resource(datasource.id, datasource.name)]

            record = tracker.DatasourceOpsLogRecord(
                timestamp=copy_timestamp.replace(tzinfo=timezone.utc),
                event_type=JobKind.COPY,
                datasource_id=datasource.id if datasource else "",
                datasource_name=datasource.name if datasource else "",
                user_id=workspace.id,
                # FIXME: Does it make sense to keep this? A workspace can have no email and some other places we just use the name.
                user_mail=workspace["email"] if "email" in workspace else workspace.name,  # noqa: SIM401
                result="error",
                elapsed_time=0,
                error=error,
                request_id=self._request_id,
                import_id=self._request_id,
                job_id="",
                rows=0,
                rows_quarantine=0,
                blocks_ids=[],
                Options__Names=[],
                Options__Values=[],
                pipe_id=pipe.id if pipe else "",
                pipe_name=pipe.name if pipe else "",
                read_rows=0,
                read_bytes=0,
                written_rows=0,
                written_bytes=0,
                written_rows_quarantine=0,
                written_bytes_quarantine=0,
                operation_id=self._request_id,
                release="",
                resource_tags=resource_tags,
            )
            dot = tracker.DatasourceOpsTrackerRegistry.get()
            if dot and dot.is_alive:
                rec = tracker.DatasourceOpsLogEntry(
                    record=record,
                    eta=datetime.now(timezone.utc),
                    workspace=workspace,
                    query_ids=[],
                    query_ids_quarantine=[],
                )
                dot.submit(rec)
            else:
                logging.warning("DatasourceOpsTrackerRegistry is dead")
        except Exception as e:
            logging.exception(f"Could not log copy error: {e}")

    async def _delete_scheduled_sink(self, *args, **kwargs):
        workspace = self.get_workspace_from_db()

        try:
            workspace_id = workspace.id if workspace else None
            await PipeUtils.delete_scheduled_sink(args[0], workspace_id)
            return True
        except Exception as e:
            logging.warning(f"error on unlink copy node: {str(e)}")
            return False

    @requires_write_access
    @with_scope(scopes.PIPES_READ)
    async def post(self, pipe_name_or_id):
        """
        Runs a copy job, using the settings previously set in the pipe.
        You can use this URL to do an on-demand copy.
        This URL is also used by the scheduler to make the programmed calls.

        This URL accepts parameters, just like in a regular endpoint.

        This operation is asynchronous and will copy the output of the endpoint to an existing datasource.

        .. sourcecode:: bash
            :caption: Runs a copy job on a Copy pipe

            curl
                -H "Authorization: Bearer <PIPE:READ token>" \\
                -X POST "https://api.tinybird.co/v0/pipes/:pipe/copy?param1=test&param2=test2"

        .. csv-table:: Request parameters
            :header: "Key", "Type", "Description"
            :widths: 20, 20, 60

            "token", "String", "Auth token. Ensure it has the ``PIPE:READ`` scope on it"
            "parameters", "String", "Optional. The value of the parameters to run the Copy with. They are regular URL query parameters."
            "_mode", "String", "Optional. One of 'append' or 'replace'. Default is 'append'."

        .. csv-table:: Response codes
            :header: "Code", "Description"
            :widths: 20, 80

            "200", "No error"
            "400", "Pipe is not a Copy pipe or there is a problem with the SQL query"
            "400", "The columns in the SQL query don't match the columns in the target Data Source"
            "403", "Forbidden. The provided token doesn't have permissions to append a node to the pipe (``ADMIN`` or ``PIPE:READ`` and ``DATASOURCE:APPEND``)"
            "403", "Job limits exceeded. Tried to copy more than 100M rows, or there are too many active (working and waiting) Copy jobs."
            "404", "Pipe not found, Node not found or Target Data Source not found"

        The response will not be the final result of the copy but a Job. You can check the job status and progress using the `Jobs API <api_reference_job url_>`_.

        .. code-block:: json
            :caption: Successful response

            {
                "id": "t_33ec8ac3c3324a53822fded61a83dbbd",
                "name": "emps",
                "sql": "SELECT * FROM employees WHERE starting_date > '2016-01-01 00:00:00'",
                "description": null,
                "materialized": null,
                "cluster": null,
                "tags": {
                    "copy_target_datasource": "t_0be6161a5b7b4f6180b10325643e0b7b",
                    "copy_target_workspace": "5a70f2f5-9635-47bf-96a9-7b50362d4e2f"
                },
                "created_at": "2023-03-01 10:14:04.497547",
                "updated_at": "2023-03-01 10:14:04.497547",
                "version": 0,
                "project": null,
                "result": null,
                "ignore_sql_errors": false,
                "dependencies": [ "employees" ],
                "params": [],
                "job": {
                    "kind": "copy",
                    "id": "f0b2f107-0af8-4c28-a83b-53053cb45f0f",
                    "job_id": "f0b2f107-0af8-4c28-a83b-53053cb45f0f",
                    "status": "waiting",
                    "created_at": "2023-03-01 10:41:07.398102",
                    "updated_at": "2023-03-01 10:41:07.398128",
                    "started_at": null,
                    "is_cancellable": true,
                    "datasource": {
                        "id": "t_0be6161a5b7b4f6180b10325643e0b7b"
                    },
                    "query_id": "19a8d613-b424-4afd-95f1-39cfbd87e827",
                    "query_sql": "SELECT * FROM d_b0ca70.t_25f928e33bcb40bd8e8999e69cb02f94 AS employees WHERE starting_date > '2016-01-01 00:00:00'",
                    "pipe_id": "t_3aa11a5cabd1482c905bc8dfc551a84d",
                    "pipe_name": "copy_emp",
                    "job_url": "https://api.tinybird.co/v0/jobs/f0b2f107-0af8-4c28-a83b-53053cb45f0f"
                }
            }
        """

        workspace = self.get_workspace_from_db()
        execution_type = self.get_argument("_execution_type", ExecutionTypes.MANUAL)
        mode = self.get_argument("_mode", None)
        copy_timestamp = datetime.utcnow()

        pipe = workspace.get_pipe(pipe_name_or_id)
        if not pipe:
            error = ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))
            self.log_copy_error(
                workspace=workspace, pipe=pipe, copy_timestamp=copy_timestamp, error=error.error_message
            )
            raise error
        self.set_span_tag({"pipe_id": pipe.id, "pipe_name": pipe.name})

        if pipe.pipe_type not in PipeTypes.COPY:
            error = ApiHTTPError.from_request_error(CopyError.no_copy_pipe(pipe_name=pipe.name))
            self.log_copy_error(
                workspace=workspace, pipe=pipe, copy_timestamp=copy_timestamp, error=error.error_message
            )
            raise error

        target_datasource_name_or_id = pipe.copy_target_datasource
        target_workspace_id = pipe.copy_target_workspace
        target_workspace = User.get_by_id(target_workspace_id)
        target_datasource = target_workspace.get_datasource(target_datasource_name_or_id)
        if not target_datasource:
            error = ApiHTTPError.from_request_error(
                CopyError.no_target_datasource(
                    target_datasource_name_or_id=target_datasource_name_or_id, pipe_name_or_id=pipe_name_or_id
                )
            )
            self.log_copy_error(
                workspace=workspace, pipe=pipe, copy_timestamp=copy_timestamp, error=error.error_message
            )
            raise error

        node = pipe.pipeline.get_node(pipe.copy_node)

        (_, variables) = get_variables_for_query(request=self.request, from_param=None, filter_sql_params=False)
        variables["copy_timestamp"] = copy_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        parameters = variables if variables else {}
        self.set_span_tag({"parameters": parameters})
        template_execution_results = TemplateExecutionResults()
        secrets = workspace.get_secrets_for_template()
        is_table_function = False
        try:
            node_sql = node.render_sql(
                variables=variables, template_execution_results=template_execution_results, secrets=secrets
            )

            try:
                sql, _ = await workspace.replace_tables_async(
                    node_sql,
                    pipe=pipe,
                    use_pipe_nodes=True,
                    extra_replacements={},
                    template_execution_results=template_execution_results,
                    variables=variables,
                    release_replacements=True,
                    secrets=secrets,
                )
            except QueryNotAllowed as e:
                if is_table_function_in_error(workspace, e):
                    sql, _ = await workspace.replace_tables_async(
                        node_sql,
                        pipe=pipe,
                        use_pipe_nodes=True,
                        extra_replacements={},
                        template_execution_results=template_execution_results,
                        variables=variables,
                        release_replacements=True,
                        function_allow_list=workspace.allowed_table_functions(),
                        secrets=secrets,
                    )
                    is_table_function = True
                else:
                    raise e

            if not mode:
                mode = node.mode

            if mode and not CopyModes.is_valid(mode):
                valid_modes = ", ".join(CopyModes.valid_modes)
                raise ApiHTTPError.from_request_error(CopyError.invalid_mode(mode=mode, valid_modes={valid_modes}))

            ch_params_keys = template_execution_results.ch_params
            job = await new_copy_job(
                self.application.job_executor,
                sql=sql,
                request_id=self._request_id,
                workspace=workspace,
                pipe=pipe,
                execution_type=execution_type,
                target_datasource=target_datasource,
                target_workspace=target_workspace,
                copy_timestamp=copy_timestamp,
                max_threads=template_execution_results.get("max_threads", None),
                parameters=parameters,
                mode=mode,
                app_settings=self.application.settings,
                is_table_function=is_table_function,
                ch_params_keys=ch_params_keys,
            )

        except CHException as e:
            self.log_copy_error(
                datasource=target_datasource,
                workspace=target_workspace or workspace,
                pipe=pipe,
                copy_timestamp=copy_timestamp,
                error=e,
            )
            if is_user_error(str(e)) or is_table_function:
                raise ApiHTTPError(400, str(e))
            else:
                raise ApiHTTPError(
                    500,
                    f"Could not run copy pipe {pipe.name}, kindly contact us at support@tinybird.co if you need assistance",
                )
        except QueryNotAllowed as e:
            self.log_copy_error(
                datasource=target_datasource,
                workspace=target_workspace or workspace,
                pipe=pipe,
                copy_timestamp=copy_timestamp,
                error=e,
            )
            raise ApiHTTPError(403, str(e))
        except SQLValidationException as e:
            self.log_copy_error(
                datasource=target_datasource,
                workspace=target_workspace or workspace,
                pipe=pipe,
                copy_timestamp=copy_timestamp,
                error=e,
            )
            raise ApiHTTPError(400, str(e))
        except (SyntaxError, ParseError, UnClosedIfError) as e:
            pipes = workspace.get_used_pipes_in_query(q=node_sql, pipe=pipe)
            error = process_syntax_error(e, pipes=pipes)
            self.log_copy_error(
                datasource=target_datasource,
                workspace=target_workspace or workspace,
                pipe=pipe,
                copy_timestamp=copy_timestamp,
                error=error,
            )
            raise ApiHTTPError(400, error, documentation=getattr(e, "documentation", "/query/query-parameters.html"))
        except (ValueError, SQLTemplateException) as e:
            self.log_copy_error(
                datasource=target_datasource,
                workspace=target_workspace or workspace,
                pipe=pipe,
                copy_timestamp=copy_timestamp,
                error=e,
            )
            raise ApiHTTPError(400, str(e), documentation=getattr(e, "documentation", "/query/query-parameters.html"))
        except CopyException as e:
            self.log_copy_error(
                datasource=target_datasource,
                workspace=target_workspace or workspace,
                pipe=pipe,
                copy_timestamp=copy_timestamp,
                error=e,
            )
            raise ApiHTTPError(e.status, str(e), documentation="/api-reference/pipe-api.html#post--v0-pipes-(.+)-copy")
        except ApiHTTPError as e:
            self.log_copy_error(
                datasource=target_datasource,
                workspace=target_workspace or workspace,
                pipe=pipe,
                copy_timestamp=copy_timestamp,
                error=e,
            )
            raise ApiHTTPError(e.status_code, e.log_message)
        except Exception as e:
            self.log_copy_error(
                datasource=target_datasource,
                workspace=target_workspace or workspace,
                pipe=pipe,
                copy_timestamp=copy_timestamp,
                error=e,
            )
            raise ApiHTTPError(
                500,
                f"Could not run copy pipe {pipe.name}, kindly contact us at support@tinybird.co if you need assistance",
            )
        response = node.to_json()

        if job:
            response["job"] = job.to_json()
            response["job"]["job_url"] = self.application.settings["api_host"] + "/v0/jobs/" + job.id
            self.set_span_tag({"job_id": job.id})

        self.write_json(response)


class APIPipeNodeCopyHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @authenticated
    @requires_write_access
    @with_scope(scopes.PIPES_CREATE)
    async def post(self, pipe_name_or_id: str, node_name_or_id: str) -> None:
        """
        Calling this endpoint sets the pipe as a Copy one with the given settings. Scheduling is optional.

        To run the actual copy after you set the pipe as a Copy one, you must call the POST ``/v0/pipes/:pipe/copy`` endpoint.

        If you need to change the target Data Source or the scheduling configuration, you can call PUT endpoint.

        Restrictions:

        * You can set only one schedule per Copy pipe.
        * You can't set a Copy pipe if the pipe is already materializing. You must unlink the Materialization first.
        * You can't set a Copy pipe if the pipe is already an endpoint. You must unpublish the endpoint first.


        .. sourcecode:: bash
            :caption: Setting the pipe as a Copy pipe

            curl -X POST \\
                -H "Authorization: Bearer <PIPE:CREATE and DATASOURCE:APPEND token>" \\
                    "https://api.tinybird.co/v0/pipes/:pipe/nodes/:node/copy" \\
                -d "target_datasource=my_destination_datasource" \\
                -d "schedule_cron=*/15 * * * *"

        .. csv-table:: Request parameters
            :header: "Key", "Type", "Description"
            :widths: 20, 20, 60

            "token", "String", "Auth token. Ensure it has the ``PIPE:CREATE`` and ``DATASOURCE:APPEND`` scopes on it"
            "target_datasource", "String", "Name or the id of the target Data Source."
            "schedule_cron", "String", "Optional. A crontab expression."

        .. code-block:: json
            :caption: Successful response

            {
                "id": "t_3aa11a5cabd1482c905bc8dfc551a84d",
                "name": "my_copy_pipe",
                "description": "This is a pipe to copy",
                "type": "copy",
                "endpoint": null,
                "created_at": "2023-03-01 10:14:04.497505",
                "updated_at": "2023-03-01 10:34:19.113518",
                "parent": null,
                "copy_node": "t_33ec8ac3c3324a53822fded61a83dbbd",
                "copy_target_datasource": "t_0be6161a5b7b4f6180b10325643e0b7b",
                "copy_target_workspace": "5a70f2f5-9635-47bf-96a9-7b50362d4e2f",
                "nodes": [{
                    "id": "t_33ec8ac3c3324a53822fded61a83dbbd",
                    "name": "emps",
                    "sql": "SELECT * FROM employees WHERE starting_date > '2016-01-01 00:00:00'",
                    "description": null,
                    "materialized": null,
                    "cluster": null,
                    "mode": "append",
                    "tags": {
                        "copy_target_datasource": "t_0be6161a5b7b4f6180b10325643e0b7b",
                        "copy_target_workspace": "5a70f2f5-9635-47bf-96a9-7b50362d4e2f"
                    },
                    "created_at": "2023-03-01 10:14:04.497547",
                    "updated_at": "2023-03-01 10:14:04.497547",
                    "version": 0,
                    "project": null,
                    "result": null,
                    "ignore_sql_errors": false,
                    "dependencies": [ "employees" ],
                    "params": []
                }]
            }
        """
        workspace = self.get_workspace_from_db()

        pipe = workspace.get_pipe(pipe_name_or_id)
        if not pipe:
            raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))
        self.set_span_tag({"pipe_id": pipe.id, "pipe_name": pipe.name})

        node = pipe.pipeline.get_node(node_name_or_id)
        if not node:
            raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))
        # Workaround to bypass max. pipes limit from CLI
        # when pushing Copy Pipe first and then push the node
        # (Coming from pre-release behaviour)
        is_cli = self.get_argument("cli_version", False) is not False
        if is_cli and pipe.pipe_type == PipeTypes.COPY:
            response = pipe.to_json()
            self.write_json(response)

        schedule_cron = self.get_argument("schedule_cron", None)
        mode = self.get_argument("mode", None)
        if schedule_cron and schedule_cron.lower() == "none":
            schedule_cron = None

        dry_run = self.get_argument("dry_run", False)

        if dry_run:
            copy_pipe_errors = await validate_copy_pipe(
                schedule_cron=schedule_cron, workspace=workspace, node=node, mode=mode
            )
            # send errors in json format for easy parsing from the UI
            if copy_pipe_errors.get("errors") is not None and len(copy_pipe_errors.get("errors")) > 0:
                assert isinstance(copy_pipe_errors, Dict)
                raise ApiHTTPError(400, json.dumps(copy_pipe_errors))
            return self.write_json(
                {
                    "dry_run_passed": True,
                }
            )

        ignore_sql_errors = self.get_argument("ignore_sql_errors", "false") == "true"
        target_datasource_name_or_id = self.get_argument("target_datasource", None)
        target_workspace_name_or_id = self.get_argument("target_workspace", None)
        target_token = self.get_argument("target_token", None)
        edited_by = _calculate_edited_by(self._get_access_info())

        validate_copy_pipe_or_raise(workspace, pipe, schedule_cron, mode)

        if not target_datasource_name_or_id:
            raise ApiHTTPError.from_request_error(CopyNodeError.target_datasource_parameter_mandatory())

        token_access = self._get_access_info()
        target_workspace, target_datasource = PipeUtils.parse_copy_parameters(
            workspace=workspace,
            token_access=token_access,
            target_datasource_name_or_id=target_datasource_name_or_id,
            target_workspace_name_or_id=target_workspace_name_or_id,
            target_token=target_token,
        )
        data_sink = None
        try:
            template_execution_results = TemplateExecutionResults()
            node_sql = node.render_sql(
                secrets=workspace.get_secrets_for_template(), template_execution_results=template_execution_results
            )

            target_datasource_id = target_datasource.id
            target_workspace_id = target_workspace.id if target_workspace else None

            await PipeUtils.validate_copy_target_datasource(
                pipe,
                node_sql,
                workspace,
                target_datasource,
                self.application.settings,
                target_workspace,
                function_allow_list=workspace.allowed_table_functions(),
                template_execution_results=template_execution_results,
            )

            # check and create sink first and if successful validate and create the copy node
            if schedule_cron:
                api_host = self.application.settings["api_host"]
                data_sink = await create_copy_schedule_sink(workspace, pipe, api_host, cron=schedule_cron, mode=mode)

            response = await NodeUtils.create_node_copy(
                workspace=workspace,
                pipe_name_or_id=pipe_name_or_id,
                node_name_or_id=node_name_or_id,
                target_datasource_id=target_datasource_id,
                mode=mode,
                target_workspace_id=target_workspace_id,
                ignore_sql_errors=ignore_sql_errors,
                edited_by=edited_by,
            )

            pipe = Users.get_pipe(workspace, pipe_name_or_id)
            assert isinstance(pipe, Pipe)
            response = pipe.to_json()

            self.write_json(response)
        except SQLTemplateCustomError as e:
            self.set_status(e.code)
            self.write(e.err)
            return
        except (SyntaxError, ParseError, UnClosedIfError) as e:
            assert isinstance(pipe, Pipe)
            error = SQLPipeError.error_sql_template(error_message=str(e), pipe_name=pipe.name, node_name=node.name)
            raise ApiHTTPError(400, error, documentation=getattr(e, "documentation", "/query/query-parameters.html"))
        except (ValueError, SQLTemplateException) as e:
            raise ApiHTTPError(400, str(e), documentation=getattr(e, "documentation", "/query/query-parameters.html"))
        except SQLValidationException as e:
            raise ApiHTTPError(400, str(e))
        except GCloudScheduleException as e:
            raise ApiHTTPError(e.status, str(e), documentation="/api-reference/schedule-api.html")
        except ApiHTTPError as e:
            if data_sink is not None:
                await data_sink.delete()
            raise ApiHTTPError(e.status_code, e.log_message, e.documentation)
        except Exception as e:
            logging.exception(f"Could not create copy node in pipe error: {e}")
            if data_sink is not None:
                await data_sink.delete()
            raise ApiHTTPError(
                500, "Could not create copy pipe, kindly contact us at support@tinybird.co if you need assistance"
            )

    @authenticated
    @requires_write_access
    @with_scope(scopes.PIPES_CREATE)
    async def delete(self, pipe_name_or_id: str, node_name_or_id: str) -> None:
        """
        Removes the Copy type of the pipe.
        By removing the Copy type, nor the node nor the pipe are deleted.
        The pipe will still be present, but will stop any scheduled and copy settings.

        .. sourcecode:: bash
            :caption: Unsetting the pipe as a Copy pipe

            curl -X DELETE \\
                -H "Authorization: Bearer <PIPE:CREATE token>" \\
                "https://api.tinybird.co/v0/pipes/:pipe/nodes/:node/copy"

        .. csv-table:: Response codes
            :header: "Code", "Description"
            :widths: 20, 80

            "204", "No error"
            "400", "Wrong node id"
            "403", "Forbidden. Provided token doesn't have permissions to publish a pipe, it needs ``ADMIN`` or ``PIPE:CREATE``"
            "404", "Pipe not found"
        """

        workspace = self.get_workspace_from_db()
        edited_by = _calculate_edited_by(self._get_access_info())

        try:
            pipe = workspace.get_pipe(pipe_name_or_id)
            if not pipe:
                raise PipeNotFound()

            node = pipe.pipeline.get_node(node_name_or_id)
            assert isinstance(node, PipeNode)
            await NodeUtils.drop_node_copy(workspace, pipe, node.id, edited_by)
        except PipeNotFound:
            raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))
        except NodeNotFound:
            raise ApiHTTPError(400, f"Pipe '{pipe_name_or_id}' does not contain the '{node_name_or_id}' node")
        except CopyNodeNotFound:
            raise ApiHTTPError(400, f"Pipe '{pipe_name_or_id}' node '{node_name_or_id}' is not set as copy")
        except GCloudScheduleException as e:
            raise ApiHTTPError(e.status, str(e))
        except Exception as exc:
            raise ApiHTTPError(400, str(exc))

        pipe = Users.get_pipe(workspace, pipe_name_or_id)
        if not pipe:
            raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))

        self.set_status(204)

    @authenticated
    @requires_write_access
    @with_scope(scopes.PIPES_CREATE)
    async def put(self, pipe_name_or_id: str, node_name_or_id: str) -> None:
        """
        Calling this endpoint will update a Copy pipe with the given settings: you can change its target Data Source, as well as adding or modifying its schedule.

        .. sourcecode:: bash
            :caption: Updating a Copy Pipe

            curl -X PUT \\
                -H "Authorization: Bearer <PIPE:CREATE token>" \\
                    "https://api.tinybird.co/v0/pipes/:pipe/nodes/:node/copy" \\
                -d "target_datasource=other_destination_datasource" \\
                -d "schedule_cron=*/15 * * * *"

        .. csv-table:: Request parameters
            :header: "Key", "Type", "Description"
            :widths: 20, 20, 60

            "token", "String", "Auth token. Ensure it has the ``PIPE:CREATE`` scope on it"
            "target_datasource", "String", "Optional. Name or the id of the target Data Source."
            "schedule_cron", "String", "Optional. A crontab expression. If schedule_cron='None' the schedule will be removed from the copy pipe, if it was defined"

        .. code-block:: json
            :caption: Successful response

            {
                "id": "t_3aa11a5cabd1482c905bc8dfc551a84d",
                "name": "my_copy_pipe",
                "description": "This is a pipe to copy",
                "type": "copy",
                "endpoint": null,
                "created_at": "2023-03-01 10:14:04.497505",
                "updated_at": "2023-03-01 10:34:19.113518",
                "parent": null,
                "copy_node": "t_33ec8ac3c3324a53822fded61a83dbbd",
                "copy_target_datasource": "t_2f046a4b2cc44137834a35420a533465",
                "copy_target_workspace": "5a70f2f5-9635-47bf-96a9-7b50362d4e2f",
                "nodes": [{
                    "id": "t_33ec8ac3c3324a53822fded61a83dbbd",
                    "name": "emps",
                    "sql": "SELECT * FROM employees WHERE starting_date > '2016-01-01 00:00:00'",
                    "description": null,
                    "materialized": null,
                    "cluster": null,
                    "mode": "append",
                    "tags": {
                        "copy_target_datasource": "t_2f046a4b2cc44137834a35420a533465",
                        "copy_target_workspace": "5a70f2f5-9635-47bf-96a9-7b50362d4e2f"
                    },
                    "created_at": "2023-03-01 10:14:04.497547",
                    "updated_at": "2023-03-07 09:08:34.206123",
                    "version": 0,
                    "project": null,
                    "result": null,
                    "ignore_sql_errors": false,
                    "dependencies": [ "employees" ],
                    "params": []
                }]
            }
        """
        workspace = self.get_workspace_from_db()
        ignore_sql_errors = self.get_argument("ignore_sql_errors", "false") == "true"
        edited_by = _calculate_edited_by(self._get_access_info())

        pipe = workspace.get_pipe(pipe_name_or_id)
        if not pipe:
            raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))
        self.set_span_tag({"pipe_id": pipe.id, "pipe_name": pipe.name})

        if pipe.pipe_type != PipeTypes.COPY:
            raise ApiHTTPError(
                400,
                f"Pipe '{pipe_name_or_id}' is not a copy pipe",
                documentation="/api-reference/pipe-api.html#post--v0-pipes-(.+)-nodes-(.+)-copy",
            )

        node = pipe.pipeline.get_node(node_name_or_id)
        if not node or node.id != pipe.copy_node:
            raise ApiHTTPError(
                400,
                f"Pipe '{pipe_name_or_id}' does not contain the '{node_name_or_id}' node or it is not the copy node",
            )

        mode = self.get_argument("mode", None)
        validate_copy_pipe_or_raise(workspace, pipe, None, mode)

        schedule_cron = self.get_argument("schedule_cron", None)
        if schedule_cron and schedule_cron.lower() == "none":
            schedule_cron = "@on-demand"

        if schedule_cron and schedule_cron != "@on-demand":
            if not croniter.is_valid(schedule_cron):
                raise ApiHTTPError(
                    400,
                    f"'schedule_cron' is invalid. '{schedule_cron}' is not a valid crontab expression. Use a valid crontab expression or contact us at support@tinybird.co",
                )

            suggested_cron = validate_gcs_cron_expression(schedule_cron)
            if suggested_cron:
                raise ApiHTTPError.from_request_error(
                    CopyError.invalid_cron_without_range(schedule_cron=schedule_cron, suggested_cron=suggested_cron)
                )

            min_period = CopyLimits.min_period_between_copy_jobs.get_limit_for(workspace)
            if CopyLimits.min_period_between_copy_jobs.has_reached_limit_in(
                min_period, {"schedule_cron": schedule_cron}
            ):
                copy_error_params = CopyLimits.min_period_between_copy_jobs.get_error_message_params(min_period)
                raise ApiHTTPError.from_request_error(
                    CopyError.min_period_between_copy_jobs_exceeded(**copy_error_params),
                    documentation="/api-reference/pipe-api.html#quotas-and-limits",
                )

        current_cron, current_timezone = None, None
        try:
            data_sink = DataSink.get_by_resource_id(pipe.id, workspace.id)
            current_cron, current_timezone = data_sink.settings.get("cron"), data_sink.settings.get("timezone")
            if schedule_cron == "@on-demand":
                new_cron = None
            else:
                new_cron = schedule_cron or current_cron
            new_timezone = current_timezone or DEFAULT_TIMEZONE
        except Exception:
            data_sink = None
            new_cron, new_timezone = schedule_cron if schedule_cron != "@on-demand" else None, DEFAULT_TIMEZONE

        workspace = self.get_workspace_from_db()
        new_target_datasource_name_or_id = self.get_argument("target_datasource", None)
        new_target_workspace_name_or_id = self.get_argument("target_workspace", None)
        new_target_token = self.get_argument("target_token", None)
        if new_target_datasource_name_or_id:
            token_access = self._get_access_info()
            target_workspace, target_datasource = PipeUtils.parse_copy_parameters(
                workspace=workspace,
                token_access=token_access,
                target_datasource_name_or_id=new_target_datasource_name_or_id,
                target_workspace_name_or_id=new_target_workspace_name_or_id,
                target_token=new_target_token,
            )
            target_workspace = target_workspace if target_workspace else workspace
            # update to new datasource
            if target_datasource.id != pipe.copy_target_datasource:
                try:
                    template_execution_results = TemplateExecutionResults()
                    node_sql = node.render_sql(
                        secrets=workspace.get_secrets_for_template(),
                        template_execution_results=template_execution_results,
                    )
                    await PipeUtils.validate_copy_target_datasource(
                        pipe,
                        node_sql,
                        workspace,
                        target_datasource,
                        self.application.settings,
                        target_workspace,
                        function_allow_list=workspace.allowed_table_functions(),
                        template_execution_results=template_execution_results,
                    )
                    await NodeUtils.update_copy_target(
                        workspace=workspace,
                        pipe_name_or_id=pipe.id,
                        target_datasource_id=target_datasource.id,
                        former_datasource_id=pipe.copy_target_datasource,
                        target_workspace_id=target_workspace.id,
                        former_workspace_id=pipe.copy_target_workspace,
                        edited_by=edited_by,
                        ignore_sql_errors=ignore_sql_errors,
                    )
                except (SyntaxError, ParseError, UnClosedIfError) as e:
                    error = SQLPipeError.error_sql_template(
                        error_message=str(e), pipe_name=pipe.name, node_name=node.name
                    )
                    raise ApiHTTPError(
                        400, error, documentation=getattr(e, "documentation", "/query/query-parameters.html")
                    )
                except (ValueError, SQLTemplateException) as e:
                    raise ApiHTTPError(400, str(e))
                except SQLValidationException as e:
                    raise ApiHTTPError(400, str(e))
                except ApiHTTPError as e:
                    raise ApiHTTPError(e.status_code, e.log_message, e.documentation)
                except Exception as e:
                    logging.exception(f"Could not update copy node datasource in pipe error: {e}")
                    raise ApiHTTPError(
                        500,
                        "Could not update target Data Source, kindly contact us at support@tinybird.co if you need assistance",
                    )

            if new_cron == current_cron and target_datasource.id == pipe.copy_target_datasource:
                raise ApiHTTPError(
                    400, "There is nothing to update, please update either the schedule cron or Data Source"
                )

        api_host = self.application.settings["api_host"]
        try:
            pipe = Users.get_pipe(workspace, pipe_name_or_id)
            assert isinstance(pipe, Pipe)
            if mode and mode != node.mode:
                pipe = await Users.update_node_in_pipe_async(workspace, edited_by, pipe.id, node.id, mode=mode)
            if data_sink and (current_cron == new_cron):
                # Do not recreate the data sink if schedule
                # expression is the same as we had before
                pass
            elif data_sink and new_cron:
                await update_copy_sink(workspace, pipe, api_host, data_sink, new_cron, new_timezone)
            elif data_sink and current_cron and not new_cron:
                await data_sink.delete()
            elif not data_sink:
                await create_copy_schedule_sink(
                    workspace, pipe, api_host, cron=new_cron, timezone=new_timezone, mode=mode
                )
            response = pipe.to_json()
            self.write_json(response)
        except GCloudScheduleException as e:
            raise ApiHTTPError(e.status, str(e), documentation="/api-reference/schedule-api.html")


class APIPipeCopyPauseHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @authenticated
    @requires_write_access
    @with_scope(scopes.PIPES_CREATE)
    async def post(self, pipe_name_or_id):
        """
        Pauses the scheduling. This affects any future scheduled Copy job. Any copy operation currently copying data will be completed.

        .. sourcecode:: bash
            :caption: Pauses a scheduled copy

            curl -X POST \\
                    -H "Authorization: Bearer <PIPE:CREATE token>" \\
                   "https://api.tinybird.co/v0/pipes/:pipe/copy/pause"

        .. csv-table:: Response codes
            :header: "Code", "Description"
            :widths: 20, 80

            "200", "Scheduled copy paused correctly"
            "400", "Pipe is not copy"
            "404", "Pipe not found, Scheduled copy for pipe not found"
        """

        workspace = self.get_workspace_from_db()

        pipe = workspace.get_pipe(pipe_name_or_id)
        if not pipe:
            raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))
        self.set_span_tag({"pipe_id": pipe.id, "pipe_name": pipe.name})

        if pipe.pipe_type != PipeTypes.COPY:
            raise ApiHTTPError.from_request_error(CopyError.no_copy_pipe(pipe_name=pipe.name))

        try:
            data_sink = DataSink.get_by_resource_id(pipe.id, workspace.id)
            if not data_sink:
                raise ApiHTTPError.from_request_error(CopyError.schedule_not_found(pipe_name_or_id=pipe_name_or_id))
        except ResourceNotConnected:
            raise ApiHTTPError.from_request_error(CopyError.non_scheduled())

        try:
            data_sink = await pause_sink(data_sink)
        except GCloudScheduleException as e:
            raise ApiHTTPError(e.status, str(e), documentation="/api-reference/schedule-api.html")

        pipe = Users.get_pipe(workspace, pipe_name_or_id)
        self.write_json(pipe.to_json())


class APIPipeCopyResumeHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @authenticated
    @requires_write_access
    @with_scope(scopes.PIPES_CREATE)
    async def post(self, pipe_name_or_id):
        """
        Resumes a previously paused scheduled copy.

        .. sourcecode:: bash
            :caption: Resumes a Scheduled copy

            curl -X POST \\
                    -H "Authorization: Bearer <PIPE:CREATE token>" \\
                   "https://api.tinybird.co/v0/pipes/:pipe/copy/resume"

        .. csv-table:: Response codes
            :header: "Code", "Description"
            :widths: 20, 80

            "200", "Scheduled copy resumed correctly"
            "400", "Pipe is not copy"
            "404", "Pipe not found, Scheduled copy for pipe not found"
        """

        workspace = self.get_workspace_from_db()

        pipe = workspace.get_pipe(pipe_name_or_id)
        if not pipe:
            raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))
        self.set_span_tag({"pipe_id": pipe.id, "pipe_name": pipe.name})

        if pipe.pipe_type != PipeTypes.COPY:
            raise ApiHTTPError.from_request_error(CopyError.no_copy_pipe(pipe_name=pipe.name))

        try:
            data_sink = DataSink.get_by_resource_id(pipe.id, workspace.id)
            if not data_sink:
                raise ApiHTTPError.from_request_error(CopyError.schedule_not_found(pipe_name_or_id=pipe_name_or_id))
        except ResourceNotConnected:
            raise ApiHTTPError.from_request_error(CopyError.non_scheduled())

        try:
            data_sink = await resume_sink(data_sink)
        except GCloudScheduleException as e:
            raise ApiHTTPError(e.status, str(e), documentation="/api-reference/schedule-api.html")

        pipe = Users.get_pipe(workspace, pipe_name_or_id)
        self.write_json(pipe.to_json())


class APIPipeCopyCancelHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @authenticated
    @requires_write_access
    @with_scope(scopes.DATASOURCES_CREATE)
    async def post(self, pipe_name_or_id):
        """
        Cancels jobs that are working or waiting that are tied to the pipe and pauses the scheduling of copy jobs for this pipe.
        To allow scheduled copy jobs to run for the pipe, the copy pipe must be resumed and the already cancelled jobs will not be resumed.

        .. sourcecode:: bash
            :caption: Cancels scheduled copy jobs tied to the pipe

            curl -X POST \\
                    -H "Authorization: Bearer <PIPE:CREATE token>" \\
                   "https://api.tinybird.co/v0/pipes/:pipe/copy/cancel"

        .. csv-table:: Response codes
            :header: "Code", "Description"
            :widths: 20, 80

            "200", "Scheduled copy pipe cancelled correctly"
            "400", "Pipe is not copy"
            "400", "Job is not in cancellable status"
            "400", "Job is already being cancelled"
            "404", "Pipe not found, Scheduled copy for pipe not found"

        .. code-block:: json
            :caption: Successful response

            {
                "id": "t_fb56a87a520441189a5a6d61f8d968f4",
                "name": "scheduled_copy_pipe",
                "description": "none",
                "endpoint": "none",
                "created_at": "2023-06-09 10:54:21.847433",
                "updated_at": "2023-06-09 10:54:21.897854",
                "parent": "none",
                "type": "copy",
                "copy_node": "t_bb96e50cb1b94ffe9e598f870d88ad1b",
                "copy_target_datasource": "t_3f7e6534733f425fb1add6229ca8be4b",
                "copy_target_workspace": "8119d519-80b2-454a-a114-b092aea3b9b0",
                "schedule": {
                    "timezone": "Etc/UTC",
                    "cron": "0 * * * *",
                    "status": "paused"
                },
                "nodes": [
                    {
                        "id": "t_bb96e50cb1b94ffe9e598f870d88ad1b",
                        "name": "scheduled_copy_pipe_0",
                        "sql": "SELECT * FROM landing_ds",
                        "description": "none",
                        "materialized": "none",
                        "cluster": "none",
                        "tags": {
                            "copy_target_datasource": "t_3f7e6534733f425fb1add6229ca8be4b",
                            "copy_target_workspace": "8119d519-80b2-454a-a114-b092aea3b9b0"
                        },
                        "created_at": "2023-06-09 10:54:21.847451",
                        "updated_at": "2023-06-09 10:54:21.847451",
                        "version": 0,
                        "project": "none",
                        "result": "none",
                        "ignore_sql_errors": "false",
                        "node_type": "copy",
                        "dependencies": [
                            "landing_ds"
                        ],
                        "params": []
                    }
                ],
                "cancelled_jobs": [
                    {
                        "id": "ced3534f-8b5e-4fe0-8dcc-4369aa256b11",
                        "kind": "copy",
                        "status": "cancelled",
                        "created_at": "2023-06-09 07:54:21.921446",
                        "updated_at": "2023-06-09 10:54:22.043272",
                        "job_url": "https://api.tinybird.co/v0/jobsjobs/ced3534f-8b5e-4fe0-8dcc-4369aa256b11",
                        "is_cancellable": "false",
                        "pipe_id": "t_fb56a87a520441189a5a6d61f8d968f4",
                        "pipe_name": "pipe_test_scheduled_copy_pipe_cancel_multiple_jobs",
                        "datasource": {
                            "id": "t_3f7e6534733f425fb1add6229ca8be4b",
                            "name": "target_ds_test_scheduled_copy_pipe_cancel_multiple_jobs"
                        }
                    },
                    {
                        "id": "b507ded9-9862-43ae-8863-b6de17c3f914",
                        "kind": "copy",
                        "status": "cancelling",
                        "created_at": "2023-06-09 07:54:21.903036",
                        "updated_at": "2023-06-09 10:54:22.044837",
                        "job_url": "https://api.tinybird.co/v0/jobsb507ded9-9862-43ae-8863-b6de17c3f914",
                        "is_cancellable": "false",
                        "pipe_id": "t_fb56a87a520441189a5a6d61f8d968f4",
                        "pipe_name": "pipe_test_scheduled_copy_pipe_cancel_multiple_jobs",
                        "datasource": {
                            "id": "t_3f7e6534733f425fb1add6229ca8be4b",
                            "name": "target_ds_test_scheduled_copy_pipe_cancel_multiple_jobs"
                        }
                    }
                ]
            }
        """

        workspace = self.get_workspace_from_db()

        pipe = workspace.get_pipe(pipe_name_or_id)
        if not pipe:
            raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))
        self.set_span_tag({"pipe_id": pipe.id, "pipe_name": pipe.name})

        if pipe.pipe_type != PipeTypes.COPY:
            raise ApiHTTPError.from_request_error(CopyError.no_copy_pipe(pipe_name=pipe.name))

        try:
            data_sink = DataSink.get_by_resource_id(pipe.id, workspace.id)
            if not data_sink:
                raise ApiHTTPError.from_request_error(CopyError.schedule_not_found(pipe_name_or_id=pipe_name_or_id))
        except ResourceNotConnected:
            raise ApiHTTPError.from_request_error(CopyError.non_scheduled_cancel())

        try:
            cancelled_jobs, not_cancelled_jobs = await cancel_pipe_copy_jobs(
                job_executor=self.application.job_executor,
                pipe=pipe,
                data_sink=data_sink,
                api_host=self.application.settings["api_host"],
            )
        except JobNotInCancellableStatusException:
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.job_not_in_cancellable_status())
        except JobAlreadyBeingCancelledException:
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.job_already_being_canceled())
        except GCloudScheduleException as e:
            raise ApiHTTPError(
                e.status,
                f"{str(e)}, scheduled copy pipe jobs have already been cancelled",
                documentation="/api-reference/schedule-api.html",
            )
        pipe = Users.get_pipe(workspace, pipe_name_or_id)
        pipe = pipe.to_json()
        if len(not_cancelled_jobs) > 0:
            pipe.update(
                {
                    "not_cancelled_jobs": not_cancelled_jobs,
                }
            )
        if len(cancelled_jobs) > 0:
            pipe.update(
                {
                    "cancelled_jobs": cancelled_jobs,
                }
            )
        self.write_json(pipe)


class APIPipeEndpointChartsHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @authenticated
    @with_scope(scopes.PIPES_READ)
    async def get(self, pipe_name_or_id):
        workspace = self.get_workspace_from_db()
        pipe = Users.get_pipe(workspace, pipe_name_or_id)

        if not pipe:
            raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))

        if pipe.pipe_type != PipeTypes.ENDPOINT:
            raise ApiHTTPError.from_request_error(ChartError.invalid_pipe_type())

        charts = Chart.get_all_by_owner(pipe.id)
        self.write_json([chart.to_json() for chart in charts])

    @authenticated
    @requires_write_access
    @with_scope(scopes.PIPES_CREATE)
    async def post(self, pipe_name_or_id):
        workspace = self.get_workspace_from_db()
        pipe = Users.get_pipe(workspace, pipe_name_or_id)
        data = json_decode(self.request.body) or {}
        name = data.get("name", "")
        description = data.get("description", "")
        index = data.get("index", "")
        categories = data.get("categories", [])
        chart_type = data.get("type", "line")
        styles = data.get("styles", {})
        show_name = data.get("show_name", False)
        show_legend = data.get("show_legend", False)
        group_by = data.get("group_by", None)

        if not pipe:
            raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))

        if pipe.pipe_type != PipeTypes.ENDPOINT:
            raise ApiHTTPError.from_request_error(ChartError.invalid_pipe_type())

        chart = Chart(
            pipe_id=pipe.id,
            name=name,
            type=chart_type,
            index=index,
            categories=categories,
            description=description,
            styles=styles,
            show_name=show_name,
            show_legend=show_legend,
            group_by=group_by,
        )
        chart.save()
        self.write_json(chart.to_json())


class APIPipeEndpointChartHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @authenticated
    async def get(self, pipe_name_or_id, chart_id):
        workspace = self.get_workspace_from_db()
        pipe = Users.get_pipe(workspace, pipe_name_or_id)

        if not pipe:
            raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))

        chart = Chart.get_by_id(chart_id)

        if not chart or chart.pipe_id != pipe.id:
            raise ApiHTTPError.from_request_error(ChartError.not_found(chart_id=chart_id))

        self.write_json(chart.to_json())

    @authenticated
    @requires_write_access
    @with_scope(scopes.PIPES_DROP)
    async def delete(self, pipe_name_or_id, chart_id):
        workspace = self.get_workspace_from_db()
        pipe = Users.get_pipe(workspace, pipe_name_or_id)

        if not pipe:
            raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))

        chart = Chart.get_by_id(chart_id)

        if not chart or chart.pipe_id != pipe.id:
            raise ApiHTTPError.from_request_error(ChartError.not_found(chart_id=chart_id))

        await Chart.delete(chart_id)
        self.set_status(204)

    @authenticated
    @requires_write_access
    @with_scope(scopes.PIPES_CREATE)
    async def put(self, pipe_name_or_id, chart_id):
        workspace = self.get_workspace_from_db()
        pipe = Users.get_pipe(workspace, pipe_name_or_id)
        data = json_decode(self.request.body) or {}
        chart_props = Chart.__props__
        chart_data = {k: v for k, v in data.items() if k in chart_props}

        if not pipe:
            raise ApiHTTPError.from_request_error(PipeClientErrorNotFound.no_pipe(pipe_name_or_id=pipe_name_or_id))

        chart = Chart.get_by_id(chart_id)

        if not chart or chart.pipe_id != pipe.id:
            raise ApiHTTPError.from_request_error(ChartError.not_found(chart_id=chart_id))

        chart = await Chart.update_chart(chart_id, chart_data)
        self.write_json(chart.to_json())


def handlers():
    return [
        url(r"/v0/pipes/openapi.json", APIPipesOpenAPIHandler, name="pipes_openapi"),
        url(r"/v0/pipes/?", APIPipeListHandler),
        # Nodes
        url(r"/v0/pipes/(.+)/nodes/(.+)/analysis", APIPipeNodeAnalysisHandler),
        url(r"/v0/pipes/(.+)/nodes/(.+)/explain", APIPipeNodeExplainHandler),
        url(r"/v0/pipes/(.+)/explain", APIPipeNodeExplainHandler),
        url(r"/v0/pipes/(.+)/nodes/(.+)/endpoint", APIPipeNodeEndpointHandler),
        url(r"/v0/pipes/(.+)/endpoint/charts/(.+)", APIPipeEndpointChartHandler),
        url(r"/v0/pipes/(.+)/endpoint/charts", APIPipeEndpointChartsHandler),
        url(
            r"/v0/pipes/(.+)/endpoint", APIPipeEndpointHandler
        ),  # Old endpoint we should support for now https://gitlab.com/tinybird/analytics/-/issues/2526
        url(r"/v0/pipes/(.+)/nodes/(.+)/population", APIPipePopulationHandler),
        url(r"/v0/pipes/(.+)/nodes/(.+)/copy", APIPipeNodeCopyHandler),
        url(r"/v0/pipes/(.+)/nodes/(.+)/sink", APIPipeNodeSinkHandler),
        url(r"/v0/pipes/(.+)/nodes/(.+)/stream", APIPipeNodeStreamHandler),
        url(r"/v0/pipes/(.+)/nodes/(.+)/materialization", APIPipeMaterializationHandler),
        url(r"/v0/pipes/(.+)/nodes", APIPipeNodeAppendHandler),
        url(r"/v0/pipes/(.+)/nodes/(.+)", APIPipeNodeHandler),
        url(r"/v0/pipes/(.+)/requests", APIPipeRequestsHandler),
        # When adding any new format please make sure to include it also in the nginx configuration, so it redirects to th readers
        url(r"/v0/pipes/(.+)\.(json|csv|ndjson|parquet|prometheus)", APIPipeDataHandler),
        url(r"/v0/pipes/(.+)/sink", APIPipeSinkHandler),
        url(r"/v0/pipes/(.+)/copy", APIPipeCopyHandler),
        url(r"/v0/pipes/(.+)/copy/pause", APIPipeCopyPauseHandler),
        url(r"/v0/pipes/(.+)/copy/resume", APIPipeCopyResumeHandler),
        url(r"/v0/pipes/(.+)/copy/cancel", APIPipeCopyCancelHandler),
        url(r"/v0/pipes/(.+)/last_update", APIPipeLastUpdateHandler),
        url(r"/v0/pipes/(.+\.pipe)", APIPipeHandler),
        url(r"/v0/pipes/(.+)", APIPipeHandler),
    ]
