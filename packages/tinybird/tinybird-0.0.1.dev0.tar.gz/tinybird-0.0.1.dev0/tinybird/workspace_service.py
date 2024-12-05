import asyncio
import copy
import logging
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Tuple, TypedDict, Union

from tinybird import tracker
from tinybird.ch import (
    TableDetails,
    ch_create_materialized_view,
    ch_create_table_as_table,
    ch_many_tables_details_async,
    ch_table_details_async,
    table_structure,
)
from tinybird.constants import BillingPlans, user_workspace_relationships
from tinybird.datasource import Datasource, SharedDatasource, SharedDSDistributedMode
from tinybird.feature_flags import FeatureFlagWorkspaces
from tinybird.git_settings import GitHubSettings, GitHubSettingsStatus
from tinybird.hook import CreateDatasourceHook, PGSyncDatasourceHook
from tinybird.limits import Limit
from tinybird.model import retry_transaction_in_case_of_concurrent_edition_error_async
from tinybird.organization.organization import Organizations
from tinybird.pipe import Pipe, PipeNode
from tinybird.sql import TableIndex, TableProjection
from tinybird.table import create_table_from_schema
from tinybird.token_scope import scopes
from tinybird.tracing import ClickhouseTracer
from tinybird.user_workspace import UserWorkspaceRelationship, UserWorkspaceRelationshipAlreadyExists
from tinybird.views.api_pipes import NodeUtils

from .constants import CHCluster
from .notifications_service import NotificationsService
from .user import CreateTokenError, DataSourceNotFound, UserAccount
from .user import User as Workspace
from .user import Users as Workspaces
from .useraccounts_service import UserAccountsService

VERSION_PATTERN = r"v\d+(_\d+)*\.\w+"


class MaxOwnedWorkspacesLimitReached(Exception):
    def __init__(self, email: str, max_owned_limit: int):
        super().__init__()
        self.email = email
        self.max_owned_limit = max_owned_limit


class InvalidRoleException(Exception):
    pass


@dataclass
class TableMetadata:
    id: str
    database: str
    schema: List[Dict[str, str]]
    details: Optional[TableDetails] = None
    details_distributed: Optional[TableDetails] = None
    indexes: Optional[List[TableIndex]] = None
    projections: Optional[List[TableProjection]] = None

    @property
    def hash(self) -> int:
        if not self.details:
            return hash(str(self.schema))
        else:
            return hash(str(self.schema)) + hash(str(self.details.to_json(exclude=["engine_full"])))

    @classmethod
    async def _get_details_from_distributed(
        cls, workspace: Workspace, distributed_details: TableDetails
    ) -> Optional[TableDetails]:
        import re

        from tinybird.user import public

        match_distributed_params = re.match("Distributed\((.*)\)$", distributed_details.engine_full)  # type: ignore
        distributed_engine_params = (
            match_distributed_params.group(1).replace("'", "").split(", ") if match_distributed_params else []
        )
        if public.metrics_cluster() and distributed_engine_params[0] == public.metrics_cluster().name:  # type: ignore
            default_server = public.metrics_cluster().server_url  # type: ignore
        elif distributed_engine_params[0] == public.get_public_user().cluster:  # noqa: SIM114
            default_server = public.get_public_user().database_server
        # TODO: patch for split. assume distributed in Internal is in internal as we have internal per region
        elif workspace == public.get_public_user() or workspace.origin == public.get_public_user().id:
            default_server = public.get_public_user().database_server
        else:
            # TODO: just works if distributed it's own cluster or tinybird internal uses cases public or metrics cluster
            return None
        details_for_distributed = await ch_many_tables_details_async(
            default_server, datasources=[(distributed_engine_params[1], distributed_engine_params[2])], timeout=2
        )
        return details_for_distributed[distributed_engine_params[1]][distributed_engine_params[2]]

    @classmethod
    async def create_from_workspace(cls, workspace: Workspace) -> Dict[str, "TableMetadata"]:
        workspace_table_metadata = {}
        schemas, details = await workspace.tables_metadata()
        for datasource in workspace.get_datasources():
            ds_database = datasource.database if datasource.database else workspace.database
            schema = [
                {k: v for k, v in schema.items() if k not in ["table", "database"]}
                for schema in schemas
                if schema["table"] == datasource.id and schema["database"] == ds_database
            ]
            table_details = details[ds_database].get(datasource.id) if ds_database in details else None
            ds_indices = []
            ds_projections = []
            if table_details:
                ds_indices = table_details.indexes
                ds_projections = table_details.projections
            if table_details and table_details.engine == "Distributed":
                details_distributed = await cls._get_details_from_distributed(workspace, table_details)
            else:
                details_distributed = None
            workspace_table_metadata.update(
                {
                    datasource.id: TableMetadata(
                        id=datasource.id,
                        database=ds_database,
                        schema=schema,
                        details=table_details,
                        details_distributed=details_distributed,
                        indexes=ds_indices,
                        projections=ds_projections,
                    )
                }
            )
        return workspace_table_metadata


class Resource(TypedDict):
    id: str
    name: str


class ResourceDiff(TypedDict):
    new: List[Resource]
    modified: List[Resource]
    deleted: List[Resource]
    forked: List[Resource]
    only_metadata: List[Resource]


@dataclass
class WorkspaceDiff:
    datasources: ResourceDiff
    pipes: ResourceDiff

    @classmethod
    def build_empty(cls):
        return WorkspaceDiff(
            datasources={"new": [], "modified": [], "deleted": [], "only_metadata": [], "forked": []},
            pipes={"new": [], "modified": [], "deleted": [], "only_metadata": [], "forked": []},
        )


class CreateBranchResourceError(TypedDict):
    id: str
    name: str
    error: Optional[str]


class WorkspaceCloneResponse(TypedDict):
    errors_datasources: List[CreateBranchResourceError]
    errors_pipes: List[CreateBranchResourceError]
    errors_tokens: List[CreateBranchResourceError]


class WorkspaceService:
    @classmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def enable_versions_by_default_for_specific_users(cls, workspace: Workspace, user_creating_it: UserAccount):
        not_allowed_emails_domains = ["vercel.com", "split.io", "inditex.com", "zara.com", "thehotelsnetwork.com"]
        if any([user_creating_it.email.endswith(domain) for domain in not_allowed_emails_domains]):
            return

        with Workspace.transaction(workspace.id) as w:
            w.feature_flags[FeatureFlagWorkspaces.VERSIONS_GA.value] = False
            remote = GitHubSettings(
                status=GitHubSettingsStatus.UNLINKED.value,
            )
            await w.update_remote(remote=remote)

    # TODO tracer should be configured instead of sent through the parameters.
    @classmethod
    async def register_and_initialize_workspace(
        cls,
        name: str,
        user_creating_it: UserAccount,
        cluster: Optional[CHCluster] = None,
        normalize_name_and_try_different_on_collision: bool = False,
        tracer: Optional[ClickhouseTracer] = None,
        origin: Optional[Workspace] = None,
    ) -> Workspace:
        if len(user_creating_it.owned_workspaces) >= int(user_creating_it.max_owned_limit):
            raise MaxOwnedWorkspacesLimitReached(user_creating_it.email, user_creating_it.max_owned_limit)

        if not cluster:
            cluster = (
                CHCluster(name=origin.cluster, server_url=origin.database_server)
                if origin and origin.cluster
                else await user_creating_it.get_cluster()
            )

        plan = None
        # If the workspace is a branch, we leave the plan unset so that Workspace.register decides which to pick
        if origin is None:
            # If user creating the workspace is member of an org and the workspace is in the org's dedicated
            # cluster, the workspace shouldn't have dev limits. So we set the plan as Enterprise
            org = await Organizations.get_by_email(user_creating_it.email)
            if org is not None and cluster in [dc.cluster for dc in org.get_dedicated_clusters()]:
                plan = BillingPlans.ENTERPRISE

        workspace = Workspace.register(
            name=name,
            admin=user_creating_it.id,
            cluster=cluster,
            normalize_name_and_try_different_on_collision=normalize_name_and_try_different_on_collision,
            origin=origin,
            plan=plan,
        )

        if not workspace:
            raise Exception("")

        try:
            await Workspaces.create_database(workspace)
        except Exception as e:
            # TODO: evaluate if make sense to enable not just for Branches
            if origin:
                logging.exception(f"Error creating database for Branch '{workspace.name}', reason: {e}")
                await workspace.delete()
            raise e
        if tracer:
            cls.trace_workspace_operation(tracer, workspace, "NewWorkspaceCreated", user_creating_it)

        # TODO: Remove this when we make the feature GA
        await WorkspaceService.enable_versions_by_default_for_specific_users(workspace, user_creating_it)

        return Workspaces.get_by_id(workspace.id)

    @classmethod
    async def invite_users_to_workspace(
        cls,
        admin: str,
        workspace_id: str,
        users_emails: List[str],
        notify_users: bool = False,
        role: Optional[str] = None,
    ) -> None:
        if role is not None and role not in user_workspace_relationships:
            raise InvalidRoleException(f"Role '{role}' is not valid. Roles available: {user_workspace_relationships}.")

        await UserAccountsService.register_users_if_dont_exist(users_emails, notify_users=notify_users)

        await Workspaces.add_users_to_workspace_async(workspace_id, users_emails, role)

        if notify_users:
            await NotificationsService.notify_workspace_invite(
                admin=admin, workspace=Workspace.get_by_id(workspace_id), invitee_emails=users_emails
            )

    @classmethod
    async def _gather_with_concurrency(cls, n, *tasks):
        semaphore = asyncio.Semaphore(n)

        async def sem_task(task):
            async with semaphore:
                return await task

        return await asyncio.gather(*(sem_task(task) for task in tasks))

    @classmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def clone_limits(cls, workspace: Workspace, branch_workspace: Workspace) -> Workspace:
        ddl_max_execution_time = workspace.get_limits(prefix="ch").get("ddl_max_execution_time", None)
        if ddl_max_execution_time:
            with Workspace.transaction(branch_workspace.id) as ws:
                ws.set_user_limit("ddl_max_execution_time", ddl_max_execution_time, "ch")
            return ws
        return branch_workspace

    @classmethod
    async def clone(cls, branch_workspace: Workspace, workspace: Workspace) -> WorkspaceCloneResponse:
        concurrency_limit = int(
            workspace.get_limits(prefix="iterating").get(
                "iterating_creation_concurrency", Limit.iterating_creation_concurrency
            )
        )
        branch_workspace = await WorkspaceService.clone_limits(workspace, branch_workspace)
        errors_datasources = await WorkspaceService.clone_datasources(workspace, branch_workspace, concurrency_limit)
        errors_pipes = await WorkspaceService.clone_pipes(workspace, branch_workspace, concurrency_limit)
        errors_tokens = await WorkspaceService.clone_tokens(workspace, branch_workspace)
        await WorkspaceService.clone_members(workspace, branch_workspace)
        branch_workspace = Workspace.get_by_id(branch_workspace.id)
        # set same release
        # TODO: register_workspace might accept release on creation if we create workspace from git
        from tinybird.iterating.release import Release, ReleaseStatus

        release = workspace.current_release
        semver = release.semver if release else "0.0.0"
        commit = release.commit if release else "fake-commit"
        rollback = branch_workspace.clone(semver)

        @retry_transaction_in_case_of_concurrent_edition_error_async()
        async def set_rollback_release(branch_workspace, semver, commit):
            with Workspace.transaction(branch_workspace.id) as ws:
                ws.releases = [
                    Release(id=rollback.id, semver=semver, commit=commit, status=ReleaseStatus.rollback).to_dict()
                ]
                ws.flush()

        await set_rollback_release(branch_workspace, semver, commit)

        await Workspaces.add_release(
            workspace=branch_workspace,
            commit=commit,
            semver=f"{semver}-snapshot",
            status=ReleaseStatus.live,
            force=True,
        )

        if workspace.feature_flags:

            @retry_transaction_in_case_of_concurrent_edition_error_async()
            async def set_feature_flags(branch_workspace):
                with Workspace.transaction(branch_workspace.id) as ws:
                    ws.feature_flags = workspace.feature_flags.copy()
                    # TODO: get rid of this dirty stuff when evolving read only setting
                    ws.feature_flags.pop(FeatureFlagWorkspaces.PROD_READ_ONLY.value, None)

            await set_feature_flags(branch_workspace)
        response = WorkspaceCloneResponse(
            errors_datasources=errors_datasources, errors_pipes=errors_pipes, errors_tokens=errors_tokens
        )

        return response

    @classmethod
    async def clone_datasources(
        cls,
        workspace_origin: Workspace,
        workspace_destination: Workspace,
        concurrency: int = Limit.iterating_creation_concurrency,
    ) -> List[CreateBranchResourceError]:
        response: List[CreateBranchResourceError] = []
        workspace_tables_metadata = await TableMetadata.create_from_workspace(workspace_origin)
        tasks_clone_in_ch = []
        for datasource in workspace_origin.get_datasources():
            try:
                if isinstance(datasource, SharedDatasource):
                    cloned_datasource = await Workspaces.add_branch_shared_datasource(
                        workspace_destination,
                        ds_id=datasource.id,
                        original_workspace_id=datasource.original_workspace_id,
                        original_workspace_name=datasource.original_workspace_name,
                        original_ds_database=datasource.original_ds_database,
                        original_ds_name=datasource.original_ds_name,
                        original_ds_description=datasource.original_ds_description,
                    )
                else:
                    origin_connector_id = datasource.to_dict().get("connector", None)
                    cloned_datasource = await Workspaces.add_datasource_async(
                        workspace_destination,
                        datasource.name,
                        tags=datasource.tags.copy(),
                        cluster=workspace_destination.cluster,
                        json_deserialization=datasource.json_deserialization.copy(),
                        description=datasource.description,
                        fixed_id=datasource.id,
                        origin_connector_id=origin_connector_id,
                        service_name=datasource.service,
                        service_conf=datasource.service_conf,
                    )

                schema = table_structure(workspace_tables_metadata[datasource.id].schema, include_auto=True)
                details = workspace_tables_metadata[datasource.id].details
                if details is None:
                    continue

                if details.engine == "Distributed":
                    details = workspace_tables_metadata[datasource.id].details_distributed
                    # Skip distributed if not in use cases supported
                    if details is None:
                        continue

                if details.engine_full is None:
                    logging.warning(f"Datasource {datasource.id} has no engine_full, skipping")
                    continue

                tasks_clone_in_ch.append(
                    WorkspaceService.clone_datasource_in_ch(
                        cloned_datasource,
                        workspace_destination,
                        workspace_origin,
                        schema,
                        details.engine_full,
                        response,
                        indexes=workspace_tables_metadata[datasource.id].indexes,
                        projections=workspace_tables_metadata[datasource.id].projections,
                    )
                )
            except Exception as exc:
                logging.exception(f"Exception cloning datasource {datasource.id}: {exc}")
                response.append({"id": datasource.id, "name": datasource.name, "error": str(exc)})

        await cls._gather_with_concurrency(concurrency, *tasks_clone_in_ch)
        return response

    @classmethod
    async def clone_datasource_in_ch(
        cls,
        cloned_datasource: Datasource,
        workspace_destination: Workspace,
        original_workspace: Workspace,
        schema: str,
        engine: str,
        response: List[CreateBranchResourceError],
        indexes: Optional[List[TableIndex]] = None,
        projections: Optional[List[TableProjection]] = None,
    ) -> None:
        cloned_datasource.install_hook(CreateDatasourceHook(workspace_destination))
        cloned_datasource.install_hook(PGSyncDatasourceHook(workspace_destination))
        error = None
        try:
            await create_table_from_schema(
                workspace=workspace_destination,
                datasource=cloned_datasource,
                schema=schema,
                engine=engine,
                # We will create it in the next step
                create_quarantine=False,
                indexes=indexes,
                projections=projections,
            )

            # Quarantine tables can use legacy settings or have been modified by ADD COLUMN
            # So, we need to generate it using CREATE TABLE ... AS
            # https://gitlab.com/tinybird/analytics/-/issues/11333
            quarantine_info = await ch_table_details_async(
                table_name=cloned_datasource.id + "_quarantine",
                database_server=original_workspace.database_server,
                database=original_workspace.database,
                include_stats=True,
            )
            # Only create quarantine if there are rows
            if quarantine_info.statistics.get("row_count"):
                await ch_create_table_as_table(
                    database_server=workspace_destination.database_server,
                    database=workspace_destination.database,
                    table_name=cloned_datasource.id + "_quarantine",
                    as_table_name=cloned_datasource.id + "_quarantine",
                    as_table_database=original_workspace.database,
                    engine=quarantine_info.engine_full,
                    cluster=workspace_destination.cluster,
                    **workspace_destination.ddl_parameters(),
                )

        except Exception as e:
            logging.exception(f"Exception {e}")
            error = e
        finally:
            if error:
                for hook in cloned_datasource.hooks:
                    hook.on_error(cloned_datasource, error)
                await Workspaces.drop_datasource_async(workspace_destination, cloned_datasource.id)
                response.append({"id": cloned_datasource.id, "name": cloned_datasource.name, "error": str(error)})

            tracker.track_hooks(cloned_datasource.hook_log(), source="branch", workspace=workspace_destination)

            tracker.track_datasource_ops(
                cloned_datasource.operations_log(), source="branch", workspace=workspace_destination
            )

    @classmethod
    async def clone_pipes(
        cls,
        workspace_origin: Workspace,
        workspace_destination: Workspace,
        concurrency: int = Limit.iterating_creation_concurrency,
    ) -> List[CreateBranchResourceError]:
        response: List[CreateBranchResourceError] = []
        for pipe in workspace_origin.get_pipes():
            try:
                await Workspaces.clone_pipe(
                    workspace_destination,
                    pipe,
                    fixed_id=pipe.id,
                )
            except Exception as exc:
                logging.exception(f"Error cloning pipe {pipe.id}: {exc}")
                response.append({"id": pipe.id, "name": pipe.name, "error": str(exc)})

        # Update workspace_destination with pipes
        workspace_destination = Workspace.get_by_id(workspace_destination.id)

        # Assure all pipes are created before MV are created as they can be dependant
        views_to_clone = []
        for pipe in workspace_origin.get_pipes():
            for node in pipe.pipeline.nodes:
                if node.materialized:
                    views_to_clone.append(WorkspaceService.clone_view(workspace_destination, pipe, node, response))

        await cls._gather_with_concurrency(concurrency, *views_to_clone)
        return response

    @classmethod
    async def clone_view(
        cls, workspace_destination: Workspace, pipe: Pipe, node: PipeNode, response: List[CreateBranchResourceError]
    ):
        # In case we are trying to clone a migration MV, the release might not be present in the branch
        # So, the replace backfill condition will fail and we will continue as we do not need to create the MV
        has_release = re.search(VERSION_PATTERN, node.sql)
        try:
            extra_replacements: Dict[Tuple[str, str], Union[str, Tuple[str, str]]] = {}
            sql, _, node, _ = await NodeUtils.replace_backfill_condition_in_sql(
                workspace_destination, pipe, node, node.sql, extra_replacements
            )

            await ch_create_materialized_view(
                workspace_destination, node.id, sql, node.materialized, drop_on_error=not has_release
            )

        except Exception as e:
            if not has_release:
                logging.exception(f"Error creating cloned materialized view for {pipe.id}: {str(e)}")
                response.append({"id": pipe.id, "name": pipe.name, "error": str(e)})
            else:
                logging.info(
                    f"Skipped cloning MV {pipe.name} with node {node.name} in workspace {workspace_destination.name}: expected error {str(e)}"
                )
        finally:
            workspace_destination.update_node(pipe.id, node)

    @classmethod
    async def clone_tokens(
        cls, workspace_origin: Workspace, workspace_destination: Workspace
    ) -> List[CreateBranchResourceError]:
        response: List[CreateBranchResourceError] = []

        async def clone_token(token):
            try:
                if not (
                    token.has_scope(scopes.ADMIN)
                    or token.has_scope(scopes.TOKENS)
                    or (token.has_scope(scopes.ADMIN_USER))
                ):
                    token = copy.deepcopy(token)
                    _scopes = [
                        f"{scope['type']}:{scope.get('resource', '')}" for scope in token.to_dict().get("scopes", [])
                    ]
                    await Workspaces.create_new_token(
                        workspace_destination, token.name, _scopes, token.origin, description=token.description
                    )
            except CreateTokenError as exc:
                # 'create datasource token' is created by default in all workspaces
                if token.name != "create datasource token":
                    logging.exception(f"Error cloning token {token.name}: {exc}")
                    response.append({"id": token.id, "name": token.name, "error": str(exc)})
            except Exception as exc:
                logging.exception(f"Error cloning token {token.name}: {exc}")
                response.append({"id": token.id, "name": token.name, "error": str(exc)})

        await cls._gather_with_concurrency(20, *[clone_token(token) for token in workspace_origin.get_tokens()])
        return response

    @classmethod
    async def compare_workspaces(cls, workspace_a: Workspace, workspace_b: Workspace) -> WorkspaceDiff:
        workspace_diff = WorkspaceDiff.build_empty()

        workspace_a_tables_metadata = await TableMetadata.create_from_workspace(workspace_a)
        workspace_b_tables_metadata = await TableMetadata.create_from_workspace(workspace_b)
        for ds_in_a in workspace_a.get_datasources():
            ds_in_b = workspace_b.get_datasource(ds_in_a.name, include_read_only=True) or workspace_b.get_datasource(
                ds_in_a.id, include_read_only=True
            )
            if not ds_in_b:
                workspace_diff.datasources["deleted"].append({"id": ds_in_a.id, "name": ds_in_a.name})
            else:
                if ds_in_b.to_hash(workspace_b_tables_metadata) != ds_in_a.to_hash(workspace_a_tables_metadata):
                    workspace_diff.datasources["modified"].append({"id": ds_in_a.id, "name": ds_in_a.name})
                elif ds_in_a.id != ds_in_b.id:
                    workspace_diff.datasources["forked"].append({"id": ds_in_a.id, "name": ds_in_a.name})
                elif ds_in_a.name != ds_in_b.name or ds_in_a.description != ds_in_b.description:
                    workspace_diff.datasources["only_metadata"].append({"id": ds_in_a.id, "name": ds_in_a.name})
        for ds_in_b in workspace_b.get_datasources():
            if not workspace_a.get_datasource(ds_in_b.name, include_read_only=True) and not workspace_a.get_datasource(
                ds_in_b.id, include_read_only=True
            ):
                workspace_diff.datasources["new"].append({"id": ds_in_b.id, "name": ds_in_b.name})
        for pipe_in_a in workspace_a.get_pipes():
            pipe_in_b = workspace_b.get_pipe(pipe_in_a.name) or workspace_b.get_pipe(pipe_in_a.id)
            if not pipe_in_b:
                workspace_diff.pipes["deleted"].append({"id": pipe_in_a.id, "name": pipe_in_a.name})
            else:
                if pipe_in_b.to_hash() != pipe_in_a.to_hash():
                    workspace_diff.pipes["modified"].append({"id": pipe_in_a.id, "name": pipe_in_a.name})
                elif (pipe_in_b.get_materialized_tables() != pipe_in_a.get_materialized_tables()) or (
                    pipe_in_b.endpoint != pipe_in_a.endpoint
                ):
                    workspace_diff.pipes["forked"].append({"id": pipe_in_a.id, "name": pipe_in_a.name})
                elif pipe_in_a.name != pipe_in_b.name or pipe_in_a.description != pipe_in_b.description:
                    workspace_diff.pipes["only_metadata"].append({"id": pipe_in_a.id, "name": pipe_in_a.name})

        for pipe_in_b in workspace_b.get_pipes():
            if not workspace_a.get_pipe(pipe_in_b.name) and not workspace_a.get_pipe(pipe_in_b.id):
                workspace_diff.pipes["new"].append({"id": pipe_in_b.id, "name": pipe_in_b.name})
        return workspace_diff

    @classmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def clone_members(cls, workspace_origin: Workspace, workspace_destination: Workspace) -> None:
        with Workspace.transaction(workspace_destination.id) as ws:
            for member in UserWorkspaceRelationship.get_by_workspace(
                workspace_origin.id, workspace_origin.max_seats_limit
            ):
                try:
                    UserWorkspaceRelationship.create_relationship(
                        member.user_id, workspace_destination.id, member.relationship
                    )
                    ws.create_workspace_access_token(member.user_id)
                except UserWorkspaceRelationshipAlreadyExists:
                    pass

    @classmethod
    async def share_a_datasource_between_workspaces(
        cls, origin_workspace: Workspace, datasource_id: str, destination_workspace: Workspace
    ) -> Datasource:
        # TODO include rest of the checks from the API here.
        # TODO ensure only DataSources coming from the original DS can be shared (probably already done, but doble check).

        origin_workspace = await Workspaces.mark_datasource_as_shared(
            origin_workspace, datasource_id, destination_workspace.id
        )
        datasource = origin_workspace.get_datasource(datasource_id)
        if not datasource:
            raise DataSourceNotFound(datasource_id)

        new_ds: Datasource

        if origin_workspace.lives_in_the_same_ch_cluster_as(destination_workspace):
            new_ds = await Workspaces.add_shared_datasource(
                destination_workspace,
                datasource.id,
                origin_workspace.id,
                origin_workspace.name,
                origin_workspace.database,
                datasource.name,
                datasource.description,
            )
        else:
            # Create first the DataSource in the Workspace
            new_ds = await Workspaces.add_shared_datasource(
                destination_workspace,
                datasource.id,
                origin_workspace.id,
                origin_workspace.name,
                origin_workspace.database,
                datasource.name,
                datasource.description,
                distributed_mode=SharedDSDistributedMode.read_only,
            )
            # get schema from the original DS:
            workspace_tables_metadata = await TableMetadata.create_from_workspace(origin_workspace)
            schema = table_structure(workspace_tables_metadata[datasource.id].schema, include_auto=True)
            # create distributed
            await create_table_from_schema(
                workspace=destination_workspace,
                datasource=new_ds,
                schema=schema,
                engine=f"Distributed({origin_workspace.cluster}, {origin_workspace.database}, {datasource_id})",
                create_quarantine=True,
                quarantine_engine=f'Distributed({origin_workspace.cluster}, {origin_workspace.database}, {f"{datasource_id}_quarantine"})',
            )

            # add datasource to workspace
            return new_ds

        return new_ds

    @classmethod
    def trace_workspace_operation(
        cls, tracer: ClickhouseTracer, workspace: Workspace, operation: str, user: Optional[UserAccount] = None
    ):
        span = None

        try:
            span = tracer.start_span()
            span.set_operation_name(operation)
            span.set_tag("workspace", workspace.id)
            span.set_tag("workspace_name", workspace.name)
            span.set_tag("database", workspace.database)
            span.set_tag("database_server", workspace.database_server)
            span.set_tag("plan", workspace.plan)
            span.set_tag("organization_id", workspace.organization_id)
            span.set_tag("origin", workspace.origin)
            span.set_tag("created_at", workspace.created_at.strftime("%Y-%m-%d %H:%M:%S"))

            if user:
                span.set_tag("user", user.id)
                span.set_tag("user_email", user.email)

            if operation == "WorkspaceDeleted":
                span.set_tag("deleted_at", datetime.fromtimestamp(int(span.start_time)).strftime("%Y-%m-%d %H:%M:%S"))

            span.set_tag("http.status_code", 200)
            tracer.record(span)

        except Exception as e:
            extra = {"span": span.tags} if span else {}
            logging.exception(
                f"Could not record operation '{operation}' for workspace '{workspace.id}', reason: {e}", extra=extra
            )
