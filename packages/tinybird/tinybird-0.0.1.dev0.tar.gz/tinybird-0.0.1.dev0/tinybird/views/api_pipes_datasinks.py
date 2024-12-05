import json
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import ValidationError

from tinybird.ch import ch_create_kafka_table_engine, ch_drop_table, ch_get_columns_from_query
from tinybird.constants import ExecutionTypes
from tinybird.data_connector import DataConnector, DataSink, ResourceNotConnected
from tinybird.data_sinks.config import UnknownCompressionCodecAlias, WriteStrategy, expand_compression_codec_alias
from tinybird.data_sinks.data_sink_service import DataSinkService
from tinybird.data_sinks.job import create_data_sink_job, get_bucket_path
from tinybird.data_sinks.limits import SinkLimitReached
from tinybird.data_sinks.parameters import replace_parameters_in_file_template
from tinybird.data_sinks.tracker import SinksAPILogRecord, SinksOpsLogResults, sinks_tracker
from tinybird.data_sinks.validation import (
    DataSinkPipeRequest,
    DataSinkPipeRequestBlobStorage,
    DataSinkPipeRequestKafka,
    DataSinkScheduleUpdateRequest,
    SinkJobValidationTimeoutExceeded,
    dry_run_validate_sink_pipe,
    validate_compression_codec,
    validate_file_template_columns_or_raise,
    validate_sink_pipe,
)
from tinybird.gc_scheduler.constants import GCloudScheduleException
from tinybird.gc_scheduler.sinks import create_datasink_schedule_sink
from tinybird.model import retry_transaction_in_case_of_concurrent_edition_error_async
from tinybird.pipe import NodeNotFound, Pipe, PipeNode, PipeTypes
from tinybird.resource import ForbiddenWordException
from tinybird.sql_template import TemplateExecutionResults
from tinybird.tokens import AccessToken, scopes
from tinybird.user import (
    PipeIsDataSink,
    PipeIsNotDataSink,
    PipeIsNotDefault,
    PipeNotFound,
    SinkNodeNotFound,
    TokenNotFound,
    Users,
)
from tinybird.user import User as Workspace
from tinybird.validation_utils import handle_pydantic_errors
from tinybird.views.api_errors.pipes import DataSinkError, ForbiddenError
from tinybird.views.base import (
    ApiHTTPError,
    BaseHandler,
    _calculate_edited_by,
    authenticated,
    requires_write_access,
    with_scope,
)
from tinybird.views.shared.utils import NodeUtils as SharedNodeUtils


@dataclass()
class NodeUtils:
    @staticmethod
    def kafka_sink_target_table(node_id: str) -> str:
        return f"{node_id}_kafka_events"

    @staticmethod
    async def create_node_datasink(
        workspace: Workspace,
        pipe_name_or_id: str,
        node_name_or_id: str,
        edited_by: Optional[str],
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
                            await SharedNodeUtils.validate_node_sql(workspace, pipe, node)
                        except ForbiddenWordException as e:
                            raise ApiHTTPError(
                                403, str(e), documentation="/api-reference/api-reference.html#forbidden-names"
                            )

            await Users.set_node_of_pipe_as_datasink_async(workspace.id, pipe_name_or_id, node_name_or_id, edited_by)

        except PipeNotFound:
            raise ApiHTTPError(404, f"Pipe '{pipe_name_or_id}' not found")
        except NodeNotFound:
            raise ApiHTTPError(400, f"Pipe '{pipe_name_or_id}' does not contain the '{node_name_or_id}' node")
        except PipeIsDataSink as dataSinkException:
            raise ApiHTTPError(
                400,
                str(dataSinkException),
                documentation="/api-reference/pipe-api.html#put--v0-pipes-(.+)-nodes-(.+)-sink",
            )
        except PipeIsNotDefault as e:
            raise ApiHTTPError(403, str(e))
        except Exception as exc:
            raise ApiHTTPError(400, str(exc))

        pipe = Users.get_pipe(workspace, pipe_name_or_id)
        if pipe:
            return pipe.to_json()
        raise ApiHTTPError(404, f"Pipe '{pipe_name_or_id}' not found")

    @staticmethod
    async def drop_node_sink(workspace: Workspace, pipe: Pipe, node_id: str, edited_by: Optional[str]) -> None:
        """
        >>> import asyncio
        >>> from tinybird.user import UserAccount
        >>> u = UserAccount.register('drop_node_sink@example.com', 'pass')
        >>> w = Workspace.register('drop_node_sink_workspace', admin=u.id)
        >>> w = Workspace.get_by_id(w.id)
        >>> nodes = [{'name': 'normal_node', 'sql': 'select 1'}, {'name': 'sink_node', 'sql': 'select 1'}]
        >>> sink_pipe = Users.add_pipe_sync(w, 'sink_pipe_1', nodes=nodes)
        >>> normal_node = sink_pipe.pipeline.get_node('normal_node')
        >>> w = Workspace.get_by_id(w.id)
        >>> asyncio.run(NodeUtils.drop_node_sink(w, sink_pipe, normal_node.id, ''))
        Traceback (most recent call last):
        ...
        tinybird.user.SinkNodeNotFound
        >>> w = Workspace.get_by_id(w.id)
        >>> asyncio.run(NodeUtils.drop_node_sink(w, sink_pipe, normal_node.id, ''))
        Traceback (most recent call last):
        ...
        tinybird.user.SinkNodeNotFound
        """

        if pipe.pipe_type != PipeTypes.DATA_SINK:
            raise SinkNodeNotFound()

        if not pipe.sink_node or pipe.sink_node != node_id:
            raise SinkNodeNotFound()

        try:
            await NodeUtils.drop_node_sink_kafka_resources(workspace, node_id)
            await Users.drop_sink_of_pipe_node_async(workspace.id, pipe.id, node_id, edited_by)
        except Exception:
            raise ApiHTTPError.from_request_error(DataSinkError.error_deleting_sink_node())

    @staticmethod
    async def create_node_sink_kafka_resources(
        workspace: Workspace,
        pipe: Pipe,
        node: PipeNode,
        data_connector: DataConnector,
        topic: str,
    ) -> None:
        template_execution_results = TemplateExecutionResults()
        # Kafka Sinks only supports sink_timestamp variable
        variables = {"sink_timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}

        node_sql = node.render_sql(
            variables=variables,
            template_execution_results=template_execution_results,
        )
        sql, _ = await workspace.replace_tables_async(
            node_sql,
            pipe=pipe,
            use_pipe_nodes=True,
            extra_replacements={},
            template_execution_results=template_execution_results,
            variables=variables,
        )
        columns = await ch_get_columns_from_query(
            database=workspace.database,
            database_server=workspace.database_server,
            sql=sql,
        )

        target_table = NodeUtils.kafka_sink_target_table(node.id)
        await ch_create_kafka_table_engine(
            workspace=workspace,
            name=target_table,
            columns=columns,
            kafka_security_protocol=data_connector.settings.get("kafka_security_protocol", ""),
            kafka_bootstrap_servers=data_connector.settings.get("kafka_bootstrap_servers", ""),
            kafka_sasl_mechanism=data_connector.settings.get("kafka_sasl_mechanism", ""),
            kafka_sasl_password=data_connector.settings.get("kafka_sasl_plain_password", ""),
            kafka_sasl_username=data_connector.settings.get("kafka_sasl_plain_username", ""),
            kafka_topic=topic,
        )

    @staticmethod
    async def drop_node_sink_kafka_resources(workspace: Workspace, node_id: str) -> None:
        target_table = NodeUtils.kafka_sink_target_table(node_id)
        await ch_drop_table(
            database=workspace.database,
            database_server=workspace.database_server,
            table=target_table,
            cluster=workspace.cluster,
            avoid_max_table_size=True,
            **workspace.ddl_parameters(skip_replica_down=True),
        )


class APIPipeSinkHandler(BaseHandler):
    POST_DOC_URL = "/api-reference/sink-pipes-api#post-v0pipespipe-idsinks"
    PUT_DOC_URL = "/api-reference/sink-pipes-api#put-v0pipespipe-idsink"

    def check_xsrf_cookie(self):
        pass

    def log_sink_error(
        self,
        workspace: Workspace,
        pipe: Pipe,
        token_name: str,
        error: str,
        data_sink: DataSink,
        file_compression: str,
        file_format: str,
        file_template: str,
    ):
        options = {}
        if data_sink.service_blob_storage:
            options = {
                "bucket_path": get_bucket_path(data_sink=data_sink),
                "file_template": file_template,
                "file_format": file_format,
                "file_compression": file_compression,
            }

        try:
            if sinks_tracker.is_enabled():
                resource_tags = workspace.get_tag_names_by_resource(pipe.id, pipe.name)
                record: SinksAPILogRecord = SinksAPILogRecord(
                    workspace_id=workspace.id,
                    workspace_name=workspace.name,
                    timestamp=datetime.utcnow(),
                    service=data_sink.service or "",
                    pipe_id=pipe.id,
                    pipe_name=pipe.name,
                    result=SinksOpsLogResults.ERROR,
                    token_name=token_name,
                    error=error,
                    parameters={},
                    options=options,
                    resource_tags=resource_tags,
                )
                sinks_tracker.append_api_log(record)
        except Exception as e:
            logging.exception(f"sinks_tracker - Could not log sink error: {e}")

    def get_validated_pipe(self, pipe_name_or_id: str) -> Pipe:
        workspace = self.get_workspace_from_db()
        pipe = workspace.get_pipe(pipe_name_or_id)
        if not pipe:
            raise PipeNotFound(f"Pipe '{pipe_name_or_id}' not found")

        self.set_span_tag({"pipe_id": pipe.id, "pipe_name": pipe.name})

        if pipe.pipe_type != PipeTypes.DATA_SINK:
            raise PipeIsNotDataSink(f"The pipe '{pipe.name}' should be a Sink pipe")

        return pipe

    def get_data_sink(self, pipe_id: str) -> DataSink:
        workspace = self.get_workspace_from_db()
        try:
            return DataSink.get_by_resource_id(pipe_id, workspace.id)
        except ResourceNotConnected as e:
            if workspace.is_branch_or_release_from_branch:
                raise ApiHTTPError(404, f"{e}. Recreate the sink in the branch to be able to test it.")
            raise ApiHTTPError(404, str(e))

    @authenticated
    @with_scope(scopes.PIPES_READ)
    async def post(self, pipe_name_or_id):
        workspace = self.get_workspace_from_db()
        sink_timestamp = datetime.utcnow()

        pipe = workspace.get_pipe(pipe_name_or_id)
        if not pipe:
            raise ApiHTTPError(404, f"Pipe '{pipe_name_or_id}' not found")
        self.set_span_tag({"pipe_id": pipe.id, "pipe_name": pipe.name})

        if pipe.pipe_type != PipeTypes.DATA_SINK:
            raise ApiHTTPError(
                403, f"The pipe '{pipe.name}' should be a Sink pipe", documentation="/api-reference/pipe-api.html"
            )

        try:
            data_sink = DataSink.get_by_resource_id(pipe.id, workspace.id)
        except ResourceNotConnected as e:
            if workspace.is_branch_or_release_from_branch:
                raise ApiHTTPError(404, f"{e}. Recreate the sink in the branch to be able to test it.")
            raise ApiHTTPError(404, str(e))

        node = pipe.pipeline.get_node(pipe.sink_node)
        token_name: str = self.get_token_name_or_raise()

        variables = {k: v[0].decode() for k, v in self.request.arguments.items()}
        variables["sink_timestamp"] = sink_timestamp.strftime("%Y-%m-%d %H:%M:%S")

        file_format = variables.get("format", data_sink.settings.get("format", "CSV"))

        # S3 Sink required variables
        file_template: str = ""
        replaced_file_template: str = ""
        file_compression: str = ""
        write_strategy: str = ""

        if data_sink.service_blob_storage:
            file_template = variables.get("file_template", data_sink.settings.get("file_template", ""))
            compression_codec_arg: str = variables.get("compression", data_sink.settings.get("compression", ""))
            write_strategy = variables.get(
                "write_strategy", data_sink.settings.get("write_strategy", WriteStrategy.NEW)
            )

            try:
                file_compression = expand_compression_codec_alias(compression_codec_arg)
            except UnknownCompressionCodecAlias:
                file_compression = compression_codec_arg

        execution_type = self.get_argument("_execution_type", ExecutionTypes.MANUAL)

        try:
            node_sql = node.render_sql(variables=variables)

            if data_sink.service_blob_storage:
                DataSinkPipeRequestBlobStorage.validate_file_format(file_format)
                DataSinkPipeRequestBlobStorage.validate_write_strategy(write_strategy)
                if file_compression:
                    validate_compression_codec(file_compression, file_format)

                available_variables = {**variables, "job_id": ""}.keys()
                await validate_file_template_columns_or_raise(
                    workspace, pipe, node_sql, file_template, available_variables
                )
                replaced_file_template = replace_parameters_in_file_template(file_template, variables)

                # write strategy: new | truncate
                # * by default is NEW
                # * for backwards compatibility: it's set to truncate if file is partitioned
                # * TRUNCATE will have precedence if both set
                if "{" in replaced_file_template or "}" in replaced_file_template:
                    write_strategy = WriteStrategy.TRUNCATE
                    await self.transaction_update_sink(data_sink.id, write_strategy)

            sql, _ = await workspace.replace_tables_async(
                node_sql,
                pipe=pipe,
                use_pipe_nodes=True,
                extra_replacements={},
                template_execution_results=TemplateExecutionResults(),
                variables=variables,
            )
            job = await create_data_sink_job(
                self.application.job_executor,
                workspace=workspace,
                pipe=pipe,
                sql=sql,
                file_template=replaced_file_template,
                file_format=file_format,
                file_compression=file_compression,
                token_name=token_name,
                data_sink=data_sink,
                request_id=self._request_id,
                execution_type=execution_type,
                write_strategy=write_strategy,
                job_timestamp=sink_timestamp,
            )

        except ApiHTTPError as e:
            self.log_sink_error(
                workspace, pipe, token_name, str(e), data_sink, file_compression, file_format, file_template
            )
            raise e
        except ValueError as e:
            self.log_sink_error(
                workspace, pipe, token_name, str(e), data_sink, file_compression, file_format, file_template
            )
            raise ApiHTTPError(400, str(e), documentation=self.POST_DOC_URL) from e
        except SinkLimitReached as e:
            self.log_sink_error(
                workspace, pipe, token_name, str(e), data_sink, file_compression, file_format, file_template
            )
            raise ApiHTTPError(403, str(e), documentation=self.POST_DOC_URL) from e
        except SinkJobValidationTimeoutExceeded as e:
            self.log_sink_error(
                workspace, pipe, token_name, str(e), data_sink, file_compression, file_format, file_template
            )
            raise ApiHTTPError(504, str(e), documentation=self.POST_DOC_URL) from e
        except Exception as e:
            self.log_sink_error(
                workspace, pipe, token_name, str(e), data_sink, file_compression, file_format, file_template
            )
            raise ApiHTTPError(500, f"Error while creating Sink job. {str(e)}")

        response = node.to_json()
        response["job"] = job.to_public_json(job, self.application.settings["api_host"])
        self.set_span_tag({"job_id": job.id})
        self.write_json(response)

    @authenticated
    @with_scope(scopes.PIPES_CREATE)
    async def put(self, pipe_name_or_id: str):
        try:
            pipe = self.get_validated_pipe(pipe_name_or_id)
            workspace = self.get_workspace_from_db()
            access_token = self.get_token_or_raise()
            api_host: str = self.application.settings["api_host"]
            data_sink_service = DataSinkService(workspace, pipe, access_token, api_host)
            decoded_arguments = {k: v[0].decode() for k, v in self.request.arguments.items()}
            parsed_request = DataSinkScheduleUpdateRequest(**decoded_arguments)
            await data_sink_service.update_schedule(parsed_request)
            # the response is the 'updated' pipe. We wouldn't really need to call the get_pipe method
            # again, as the to_json method pulls the latest data from redis but we do it anyway to make sure
            # the data is up to date in case the to_json method is modified in the future
            updated_pipe = self.get_validated_pipe(pipe_name_or_id)
            response = updated_pipe.to_json()
            self.write_json(response)
        except ValueError as e:
            raise ApiHTTPError(400, str(e), documentation=self.PUT_DOC_URL) from e
        except PipeNotFound as e:
            raise ApiHTTPError(404, str(e), documentation=self.PUT_DOC_URL) from e
        except PipeIsNotDataSink as e:
            raise ApiHTTPError(403, str(e), documentation=self.PUT_DOC_URL) from e
        except TokenNotFound as e:
            raise ApiHTTPError(403, str(e), documentation=self.PUT_DOC_URL) from e
        except ForbiddenError as e:
            raise ApiHTTPError(403, str(e), documentation=self.PUT_DOC_URL) from e
        except ResourceNotConnected as e:
            raise ApiHTTPError(404, str(e), documentation=self.PUT_DOC_URL) from e
        except Exception as e:
            raise ApiHTTPError(500, f"Error while updating Sink job. {str(e)}") from e

    def get_token_or_raise(self) -> AccessToken:
        access_token = self._get_access_info()
        if not access_token or not access_token.name:
            raise TokenNotFound("No token provided")
        return access_token

    def get_token_name_or_raise(self) -> str:
        access_token = self._get_access_info()
        if not access_token or not access_token.name:
            raise ApiHTTPError(403, "No token provided")
        return access_token.name

    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def transaction_update_sink(self, sink_id: str, write_strategy: WriteStrategy) -> DataSink:
        with DataSink.transaction(sink_id) as data_sink:
            data_sink.update_settings(write_strategy=write_strategy.value)
            return data_sink


class APIPipeNodeSinkHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @authenticated
    @with_scope(scopes.PIPES_CREATE)
    async def post(self, pipe_name_or_id: str, node_name_or_id: str):
        """
        This is documented in the `tinyibird-docs` repo. https://gitlab.com/tinybird/tinybird-docs
        """
        workspace = self.get_workspace_from_db()

        pipe = self.get_pipe_or_raise(workspace, pipe_name_or_id)
        self.set_span_tag({"pipe_id": pipe.id, "pipe_name": pipe.name})

        # TODO: ADD PROPER RESOURCE PERMISSIONS CHECK
        # access_token = self._get_access_info()
        # if pipe.id not in access_token.get_resources_for_scope(scopes.PIPES_READ):
        #     raise ApiHTTPError(403, f"Provided token does not allow access to '{pipe.id}' pipe")

        node = self.get_pipenode_or_raise(pipe, node_name_or_id)
        service: str = self.get_argument("service", None)
        connection_name: str = self.get_argument("connection", None)
        path: str = self.get_argument("path", None)
        file_template: str = self.get_argument("file_template", None)
        topic: str = self.get_argument("topic", None)
        export_format: str = self.get_argument("format", "csv")
        schedule_cron = self.get_argument("schedule_cron", None)
        if schedule_cron and schedule_cron.lower() == "none":
            schedule_cron = None
        ignore_sql_errors = self.get_argument("ignore_sql_errors", "false") == "true"
        api_host = self.application.settings["api_host"]
        compression = self.get_argument("compression", None)
        dry_run = self.get_argument("dry_run", "false").lower() == "true"
        edited_by = _calculate_edited_by(self._get_access_info())
        write_strategy = self.get_argument("write_strategy", WriteStrategy.NEW)

        if dry_run:
            try:
                dry_run_validate_sink_pipe(override=False, workspace=workspace, schedule_cron=schedule_cron)
            except ValidationError as e:
                raise ApiHTTPError(400, json.dumps(handle_pydantic_errors(e))) from None
            self.write_json({"dry_run_passed": True})
        else:
            try:
                data_sinkpipe_request = await validate_sink_pipe(
                    service=service,
                    connection_name=connection_name,
                    file_template=file_template,
                    file_format=export_format,
                    topic=topic,
                    ignore_sql_errors=ignore_sql_errors,
                    compression=compression,
                    path=path,
                    schedule_cron=schedule_cron,
                    workspace=workspace,
                    api_host=api_host,
                    new_pipe=pipe,
                    new_node=node,
                    new_pipe_name=pipe_name_or_id,
                    override=False,
                    write_strategy=write_strategy,
                )
            except ValidationError as e:
                raise ApiHTTPError(400, json.dumps(handle_pydantic_errors(e))) from None

            response = await create_data_sink_pipe(data_sinkpipe_request, edited_by)
            self.write_json(response)

    @authenticated
    @requires_write_access
    @with_scope(scopes.PIPES_CREATE)
    async def delete(self, pipe_name_or_id: str, node_name_or_id: str) -> None:
        workspace = self.get_workspace_from_db()
        edited_by = _calculate_edited_by(self._get_access_info())

        try:
            pipe = self.get_pipe_or_raise(workspace, pipe_name_or_id)
            node = self.get_pipenode_or_raise(pipe, node_name_or_id)
            await NodeUtils.drop_node_sink(workspace, pipe, node.id, edited_by)
        except SinkNodeNotFound:
            raise ApiHTTPError(400, f"Pipe '{pipe_name_or_id}' node '{node_name_or_id}' is not set as sink")
        except Exception as exc:
            raise ApiHTTPError(400, str(exc))

        pipe = Users.get_pipe(workspace, pipe_name_or_id)
        if not pipe:
            raise ApiHTTPError(404, f"Pipe '{pipe_name_or_id}' not found")

        response = pipe.to_json()
        response["url"] = f'{self.application.settings["api_host"]}/v0/pipes/{pipe.name}.json'
        self.write_json(response)

    def get_pipe_or_raise(self, workspace: Workspace, pipe_name_or_id: str):
        pipe = workspace.get_pipe(pipe_name_or_id)

        if pipe:
            return pipe

        raise ApiHTTPError(404, f"Pipe '{pipe_name_or_id}' not found")

    def get_pipenode_or_raise(self, pipe: Pipe, node_name_or_id: str):
        node = pipe.pipeline.get_node(node_name_or_id)

        if node:
            return node

        raise ApiHTTPError(404, f"Pipe '{pipe.name}' does not contain the '{node_name_or_id}' node")


async def create_data_sink_pipe(request: DataSinkPipeRequest, edited_by: Optional[str]) -> Dict[str, Any]:
    data_sink = None
    schedule_sink = None
    exception_error = None
    response = {}

    try:
        # Create Sink Node and Data Sink
        await NodeUtils.create_node_datasink(
            workspace=request.workspace,
            pipe_name_or_id=request.new_pipe.id,
            node_name_or_id=request.new_node.id,
            edited_by=edited_by,
            ignore_sql_errors=request.ignore_sql_errors,
        )

        data_sink_settings = {}

        match request:
            case DataSinkPipeRequestBlobStorage():
                data_sink_settings = {
                    "bucket_path": request.path,
                    "file_template": request.file_template,
                    "format": request.file_format,
                    "compression": request.compression,
                    "write_strategy": request.write_strategy.value,
                }
            case DataSinkPipeRequestKafka():
                # Create Kafka resources
                await NodeUtils.create_node_sink_kafka_resources(
                    request.workspace,
                    request.new_pipe,
                    request.new_node,
                    request.data_connector,
                    request.topic,
                )

                data_sink_settings = {
                    "topic": request.topic,
                    "target_table": NodeUtils.kafka_sink_target_table(request.new_node.id),
                    "format": request.file_format,
                }
            case _:
                raise Exception(f"Unsupported data sink service: {request.__class__.__name__}")

        data_sink = DataSink.add_sink(
            request.data_connector,
            resource=request.original_pipe if request.original_pipe else request.new_pipe,
            settings=data_sink_settings,
            workspace=request.workspace,
        )

        if request.schedule_cron and data_sink:
            # in order to create the correct endpoint url to hit when a schedule job is run
            # since the original pipe id will be retained
            schedule_pipe = request.original_pipe if request.original_pipe else request.new_pipe
            schedule_sink = await create_datasink_schedule_sink(
                request.workspace,
                schedule_pipe,
                data_sink,
                request.api_host,
                request.schedule_cron,
            )

        sink_pipe = Users.get_pipe(request.workspace, request.new_pipe_name)
        response = sink_pipe.to_json() if sink_pipe else {}
    except ApiHTTPError as httpE:
        exception_error = httpE
    except GCloudScheduleException as gcE:
        exception_error = ApiHTTPError(gcE.status, str(gcE), documentation="/api-reference/schedule-api.html")
    except Exception as e:
        logging.exception(f"Could not create sink node in pipe error: {e}")
        exception_error = ApiHTTPError(500, f"Could not create sink pipe: {e}")

    if not exception_error:
        return response

    if data_sink:
        await data_sink.delete()
    if schedule_sink:
        await schedule_sink.delete()

    if isinstance(request, DataSinkPipeRequestKafka):
        # Remove Kafka resource when error
        try:
            await NodeUtils.drop_node_sink_kafka_resources(request.workspace, request.new_node.id)
        except Exception as e:
            logging.error(
                f"Orphan table: {NodeUtils.kafka_sink_target_table(request.new_node.id)} in workspace {request.workspace.id}. Due to {e}"
            )

    raise exception_error
