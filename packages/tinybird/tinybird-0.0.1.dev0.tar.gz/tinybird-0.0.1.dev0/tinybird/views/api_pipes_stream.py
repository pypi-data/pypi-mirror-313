import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from tinybird.ch import (
    ch_create_kafka_table_engine,
    ch_create_streaming_query,
    ch_drop_table,
    ch_get_columns_from_query,
)
from tinybird.data_connector import DataConnector, DataConnectorNotFound, DataConnectorType, DataSink
from tinybird.feature_flags import FeatureFlagsWorkspaceService, FeatureFlagWorkspaces
from tinybird.pipe import NodeNotFound, Pipe, PipeNode, PipeTypes
from tinybird.resource import ForbiddenWordException
from tinybird.sql_template import TemplateExecutionResults
from tinybird.tokens import scopes
from tinybird.user import PipeIsNotDefault, PipeIsStream, PipeNotFound, StreamNodeNotFound, Users
from tinybird.user import User as Workspace
from tinybird.views.api_errors.pipes import StreamError
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
class StreamNodeUtils:
    @staticmethod
    async def create_node_stream(
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

            await Users.set_node_of_pipe_as_stream_async(workspace.id, pipe_name_or_id, node_name_or_id, edited_by)

        except PipeNotFound:
            raise ApiHTTPError(404, f"Pipe '{pipe_name_or_id}' not found")
        except NodeNotFound:
            raise ApiHTTPError(400, f"Pipe '{pipe_name_or_id}' does not contain the '{node_name_or_id}' node")
        except PipeIsStream as streamException:
            raise ApiHTTPError(
                400,
                str(streamException),
                documentation="/api-reference/pipe-api.html#put--v0-pipes-(.+)-nodes-(.+)-stream",
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
    async def drop_node_stream(workspace: Workspace, pipe: Pipe, node_id: str, edited_by: Optional[str]) -> None:
        """
        >>> import asyncio
        >>> from tinybird.user import UserAccount
        >>> u = UserAccount.register('drop_node_stream@example.com', 'pass')
        >>> w = Workspace.register('drop_node_stream_workspace', admin=u.id)
        >>> w = Workspace.get_by_id(w.id)
        >>> nodes = [{'name': 'normal_node', 'sql': 'select 1'}, {'name': 'sink_node', 'sql': 'select 1'}]
        >>> stream_pipe = Users.add_pipe_sync(w, 'stream_pipe_1', nodes=nodes)
        >>> normal_node = stream_pipe.pipeline.get_node('normal_node')
        >>> w = Workspace.get_by_id(w.id)
        >>> asyncio.run(StreamNodeUtils.drop_node_stream(w, stream_pipe, normal_node.id, ''))
        Traceback (most recent call last):
        ...
        tinybird.user.StreamNodeNotFound
        >>> w = Workspace.get_by_id(w.id)
        >>> asyncio.run(StreamNodeUtils.drop_node_stream(w, stream_pipe, normal_node.id, ''))
        Traceback (most recent call last):
        ...
        tinybird.user.StreamNodeNotFound
        """

        if pipe.pipe_type != PipeTypes.STREAM:
            raise StreamNodeNotFound()

        if not pipe.stream_node or pipe.stream_node != node_id:
            raise StreamNodeNotFound()

        try:
            await drop_stream_ch_resources(workspace, node_id)
            await Users.drop_stream_of_pipe_node_async(workspace.id, pipe.id, node_id, edited_by)
        except Exception:
            raise ApiHTTPError.from_request_error(StreamError.error_deleting_stream_node())

    @staticmethod
    def get_data_connector(workspace: Workspace, connection_name: str):
        if connector := DataConnector.get_by_owner_and_name(workspace.id, connection_name):
            return connector
        if workspace.origin and (connector := DataConnector.get_by_owner_and_name(workspace.origin, connection_name)):
            return connector
        raise DataConnectorNotFound(connection_name)

    @staticmethod
    async def create_stream(
        workspace: Workspace,
        data_connector: DataConnector,
        pipe: Pipe,
        node: PipeNode,
        kafka_topic: str,
        edited_by: Optional[str] = None,
        ignore_sql_errors: bool = False,
    ):
        data_sink = None
        settings = {
            "topic": kafka_topic,
        }

        try:
            data_sink = DataSink.add_sink(
                data_connector,
                resource=pipe,
                settings=settings,
                workspace=workspace,
            )
            await StreamNodeUtils.create_node_stream(
                workspace=workspace,
                pipe_name_or_id=pipe.name,
                node_name_or_id=node.name,
                edited_by=edited_by,
                ignore_sql_errors=ignore_sql_errors,
            )
            template_execution_results = TemplateExecutionResults()
            node_sql = node.render_sql(template_execution_results=template_execution_results)

            sql, _ = await workspace.replace_tables_async(
                node_sql,
                pipe=pipe,
                use_pipe_nodes=True,
                extra_replacements={},
                template_execution_results=template_execution_results,
                variables={},
            )
            columns = await ch_get_columns_from_query(
                database=workspace.database, database_server=workspace.database_server, sql=sql
            )
            await create_stream_ch_resources(
                workspace=workspace,
                data_connector=data_connector,
                data_sink=data_sink,
                columns=columns,
                sql=sql,
                node_id=node.id,
            )
            stream_pipe = Users.get_pipe(workspace, pipe.name)
            return stream_pipe.to_json() if stream_pipe else {}
        except Exception as e:
            try:
                if data_sink:
                    await data_sink.delete()
                await drop_stream_ch_resources(workspace, node.id)
                await Users.drop_stream_of_pipe_node_async(workspace.id, pipe.id, node.id, None)
            except Exception as cleanup_error:
                logging.exception(f"Some error occurred while cleaning up stream resources: {cleanup_error}")

            logging.exception(f"Could not create stream node in pipe error: {e}")
            raise ApiHTTPError(500, f"Could not create stream pipe: {e}")


class APIPipeNodeStreamHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @authenticated
    @with_scope(scopes.PIPES_CREATE)
    async def post(self, pipe_name_or_id: str, node_name_or_id: str):
        """
        This endpoint sets a pipe as a stream pipe, allowing users to export data to either Amazon S3 or Google Cloud Storage (GCS).

        Restrictions:

        * You can't set a Stream pipe if the pipe is already materializing. You must unlink the Materialization first.
        * You can't set a Stream pipe if the pipe is already an endpoint. You must unpublish the endpoint first.
        * You can't set a Stream pipe if the pipe is already copying. You must unset the copy first.
        * You can't set a Stream pipe if the pipe is already a sink. You must unset the sink first.

        .. sourcecode:: bash
            :caption: Setting the pipe as a Stream pipe
            curl -X POST \\
                -H "Authorization: Bearer <PIPE:CREATE>" \\
                    "https://api.tinybird.co/v0/pipes/:pipe/nodes/:node/stream" \\
                -d "connection=your_s3_or_gcs_connection"

        .. csv-table:: Request parameters
            :header: "Key", "Type", "Description"
            :widths: 20, 20, 60

            "connection", "String", "The name of the connection to either S3 or GCS where the data will be exported. The connection should be pre-configured and authenticated with the appropriate credentials."

        .. code-block:: json
            ::caption Successful response

            {
                "id": "t_feb688a8f57b417e894c0f172c5bbc0e",
                "name": "my_stream_pipe",
                "description": 'This is a pipe that exports to an external service',
                "endpoint": None,
                "created_at": "2023-06-28 14:58:02.221548",
                "updated_at": "2023-06-28 14:58:02.240103",
                "parent": None,
                "type": "stream",
                "stream_node": "t_1b4b954fd56443f79058c9d3c7ff2e18",
                "nodes": [{
                    "id": "t_1b4b954fd56443f79058c9d3c7ff2e18",
                    "name": "my_stream_pipe0",
                    "sql": "SELECT * FROM my_datasource",
                    "description": None,
                    "materialized": None,
                    "cluster": None,
                    "tags": {},
                    "created_at": "2023-06-28 14:58:02.221560",
                    "updated_at": "2023-06-28 14:58:02.221560",
                    "version": 0,
                    "project": None,
                    "result": None,
                    "ignore_sql_errors": False,
                    "node_type": "stream",
                    "dependencies": [
                        "my_datasource"
                    ],
                    "params": []
                }]
            }
        """
        workspace = self.get_workspace_from_db()

        pipe = self.get_pipe_or_raise(workspace, pipe_name_or_id)
        self.set_span_tag({"pipe_id": pipe.id, "pipe_name": pipe.name})
        node = self.get_pipenode_or_raise(pipe, node_name_or_id)
        connection_name: str = self.get_argument("connection", None)
        ignore_sql_errors = self.get_argument("ignore_sql_errors", "false") == "true"
        edited_by = _calculate_edited_by(self._get_access_info())
        kafka_topic = self.get_argument("kafka_topic", None)

        if not FeatureFlagsWorkspaceService.feature_for_id(
            FeatureFlagWorkspaces.STREAMING_QUERIES, workspace.id, workspace.feature_flags
        ):
            raise ApiHTTPError(400, "Streaming queries are not enabled for this workspace")

        if not connection_name:
            raise ApiHTTPError(400, "'connection' is required for setting a Pipe as stream")

        if not kafka_topic:
            raise ApiHTTPError(400, "'topic' is required for setting a Pipe as stream")

        data_connector = StreamNodeUtils.get_data_connector(workspace, connection_name)

        if data_connector.service != DataConnectorType.KAFKA:
            raise ApiHTTPError(400, "Only Kafka connections are supported for Streaming queries")

        response = await StreamNodeUtils.create_stream(
            workspace=workspace,
            data_connector=data_connector,
            pipe=pipe,
            node=node,
            edited_by=edited_by,
            ignore_sql_errors=ignore_sql_errors,
            kafka_topic=kafka_topic,
        )
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
            await StreamNodeUtils.drop_node_stream(workspace, pipe, node.id, edited_by)
        except StreamNodeNotFound:
            raise ApiHTTPError(400, f"Pipe '{pipe_name_or_id}' node '{node_name_or_id}' is not set as stream")
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


def build_streaming_query_name(node_id: str) -> str:
    return f"{node_id}_kafka_writer"


def build_kafka_table_engine_name(node_id: str) -> str:
    return f"{node_id}_kafka_events"


async def drop_stream_ch_resources(workspace: Workspace, node_id: str) -> None:
    streaming_query = build_streaming_query_name(node_id)
    target_table = build_kafka_table_engine_name(node_id)

    await ch_drop_table(
        database=workspace.database,
        database_server=workspace.database_server,
        table=streaming_query,
        cluster=workspace.cluster,
    )
    await ch_drop_table(
        database=workspace.database,
        database_server=workspace.database_server,
        table=target_table,
        cluster=workspace.cluster,
    )


async def create_stream_ch_resources(
    workspace: Workspace,
    data_connector: DataConnector,
    data_sink: DataSink,
    columns: List[Dict[str, str]],
    sql: str,
    node_id: str,
) -> None:
    streaming_query = build_streaming_query_name(node_id)
    target_table = build_kafka_table_engine_name(node_id)
    await ch_create_kafka_table_engine(
        workspace=workspace,
        name=target_table,
        columns=columns,
        kafka_security_protocol=data_connector.settings.get("kafka_security_protocol", ""),
        kafka_bootstrap_servers=data_connector.settings.get("kafka_bootstrap_servers", ""),
        kafka_sasl_mechanism=data_connector.settings.get("kafka_sasl_mechanism", ""),
        kafka_sasl_password=data_connector.settings.get("kafka_sasl_plain_password", ""),
        kafka_sasl_username=data_connector.settings.get("kafka_sasl_plain_username", ""),
        kafka_topic=data_sink.settings.get("topic", ""),
    )
    await ch_create_streaming_query(workspace=workspace, name=streaming_query, target_table=target_table, sql=sql)
