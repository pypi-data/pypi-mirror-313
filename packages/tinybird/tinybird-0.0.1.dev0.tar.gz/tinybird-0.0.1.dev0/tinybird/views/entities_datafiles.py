import logging
import textwrap
from typing import Any, Dict, List, Optional, Tuple

from tinybird.ch import ch_table_details_async
from tinybird.data_connector import DataConnector, DataSink
from tinybird.datafile import PipeNodeTypes, format_datasource, format_pipe, parse_datasource, parse_pipe
from tinybird.datasource import Datasource
from tinybird.pipe import Pipe
from tinybird.sql_template_fmt import DEFAULT_FMT_LINE_LENGTH
from tinybird.token_scope import scopes
from tinybird.tokens import AccessToken
from tinybird.user import User as Workspace
from tinybird.user import UserAccount
from tinybird.user import Users as Workspaces


async def generate_datasource_datafile(
    workspace: Workspace,
    ds_meta: Datasource,
    current_token: Optional[AccessToken],
    format: Optional[bool] = False,
    tags_cli_support_enabled: Optional[bool] = True,
) -> str:
    workspaces_accessible_by_the_user: List[Dict[str, Any]] = []
    # When we want to get the datafile and the datasource is shared, let's replace the workspace_id for the name
    if ds_meta.shared_with and current_token:
        # We use the same approach as when fetching the list of workspaces
        resources = current_token.get_resources_for_scope(scopes.ADMIN_USER)
        if resources:
            user = UserAccount.get_by_id(resources[0])
            if not user:
                raise Exception(f"Unexpected error: User {resources[0]} not found")
            workspaces_accessible_by_the_user = await user.get_workspaces(with_environments=False)

    filtering_tags = []
    if tags_cli_support_enabled is None or tags_cli_support_enabled:
        try:
            main_workspace = workspace.get_main_workspace()
            filtering_tags = [tag.name for tag in main_workspace.get_tags_by_resource(ds_meta.id, ds_meta.name)]
        except Exception:
            pass

    datafile_content = await ds_meta.to_datafile(
        workspace, workspaces_accessible_by_the_user, filtering_tags=filtering_tags
    )

    if not format:
        return datafile_content

    try:
        datafile = parse_datasource(filename=ds_meta.name, replace_includes=False, content=datafile_content)
        datafile_content_formatted = await format_datasource(filename=ds_meta.name, datafile=datafile)
    except Exception as e:
        logging.warning(f"Error on generate_datasource_datafile, fallback to default content: {e}")
        return datafile_content

    return datafile_content_formatted


async def generate_pipe_datafile(
    pipe: Pipe,
    workspace: Workspace,
    materialized_node_name: Optional[Tuple[str, str]] = None,
    format: Optional[bool] = False,
    tags_cli_support_enabled: Optional[bool] = True,
) -> str:
    """
    >>> import asyncio
    >>> nodes = [{'name': 'p0', 'sql': 'select 1'}]
    >>> p0 = Pipe('abcd', nodes)
    >>> asyncio.run(generate_pipe_datafile(p0, None))
    'NODE p0\\nSQL >\\n\\n    select 1\\n\\n\\n'
    """

    doc = []

    if pipe.description:
        doc.append(f"DESCRIPTION >\n\t{pipe.description}\n\n")

    if workspace:
        tokens = workspace.get_access_tokens_for_resource(pipe.id, scopes.PIPES_READ)
        for t in tokens:
            doc.append(f'TOKEN "{t.name}" READ\n')

    # You have to explicitly set it to False to disable it, so dev cli versions can use it
    if tags_cli_support_enabled is None or tags_cli_support_enabled:
        filtering_tags = []
        try:
            main_workspace = workspace.get_main_workspace()
            tags = main_workspace.get_tags_by_resource(pipe.id, pipe.name)
            filtering_tags = [tag.name for tag in tags]
        except Exception:
            pass

        if filtering_tags:
            doc.append(f'TAGS "{", ".join(filtering_tags)}"\n')

    for x in pipe.pipeline.to_dict():
        sql = textwrap.indent(x["sql"], " " * 4)
        node = f"NODE {x['name']}\n"

        if x.get("description", None):
            desc = textwrap.indent(x["description"], " " * 4)
            node += f"DESCRIPTION >\n{desc}\n\n"

        node += f"SQL >\n\n{sql}"
        node_type = x.get("node_type", None)
        if x["materialized"]:
            ds = Workspaces.get_datasource(workspace, x["materialized"])
            node += "\n\nTYPE materialized\n"
            if ds:
                node += f"DATASOURCE {ds.name}\n"
            else:
                engine = await ch_table_details_async(
                    f".inner.{x['materialized']}", workspace["database_server"], database=workspace["database"]
                )
                node += engine.to_datafile()
            node += "\n\n"
        elif materialized_node_name and materialized_node_name[0] == x["name"]:
            node += "\n\nTYPE materialized\n"
            node += f"DATASOURCE {materialized_node_name[1]}\n"
            node += "\n\n"
        elif node_type == PipeNodeTypes.COPY and (
            target_datasource := Workspaces.get_datasource(workspace, pipe.copy_target_datasource)
        ):
            node += "\n\nTYPE copy\n"
            node += f"TARGET_DATASOURCE {target_datasource.name}\n"
            if x.get("mode"):
                node += f"COPY_MODE {x.get('mode')}\n"
            schedule = pipe.get_schedule(workspace_id=workspace.id, fallback_main=True)
            cron = schedule.get("cron", "@on-demand")
            node += f"COPY_SCHEDULE {cron}\n"
            node += "\n\n"
        elif node_type == PipeNodeTypes.DATA_SINK:
            data_sink = DataSink.get_by_resource_id(pipe.id, workspace.id, fallback_main=True)
            node += "\n\nTYPE sink\n"
            node += f"EXPORT_SERVICE {data_sink.service}\n"
            connector: Optional[DataConnector] = (
                DataConnector.get_by_id(data_sink.data_connector_id) if data_sink.data_connector_id else None
            )
            if connector:
                node += f"EXPORT_CONNECTION_NAME {connector.name}\n"
            if bucket_path := data_sink.settings.get("bucket_path"):
                node += f"EXPORT_BUCKET_URI {bucket_path}\n"
            file_template = data_sink.settings.get("file_template")
            if file_template:
                node += f"EXPORT_FILE_TEMPLATE {file_template}\n"
            export_format = data_sink.settings.get("format")
            if export_format:
                node += f"EXPORT_FORMAT {export_format}\n"
            compression = data_sink.settings.get("compression")
            if compression:
                node += f"EXPORT_COMPRESSION {compression.lower()}\n"
            strategy = data_sink.settings.get("strategy")
            if strategy:
                node += f"EXPORT_STRATEGY {strategy}\n"
            if topic := data_sink.settings.get("topic"):
                node += f"EXPORT_KAFKA_TOPIC {topic}\n"
            schedule = pipe.get_schedule(workspace_id=workspace.id, fallback_main=True)
            cron = schedule.get("cron", "@on-demand")
            node += f"EXPORT_SCHEDULE {cron}\n"
            node += "\n\n"
        elif node_type == PipeNodeTypes.STREAM:
            data_sink = DataSink.get_by_resource_id(pipe.id, workspace.id, fallback_main=True)
            node += "\n\nTYPE stream\n"
            stream_connection: Optional[DataConnector] = (
                DataConnector.get_by_id(data_sink.data_connector_id) if data_sink.data_connector_id else None
            )
            if stream_connection:
                node += f"KAFKA_CONNECTION_NAME {stream_connection.name}\n"
            topic = data_sink.settings.get("topic")
            node += f"KAFKA_TOPIC {topic}\n"
            node += "\n\n"
        else:
            node += "\n\n\n"

        doc.append(node)

    datafile_content = "\n".join(doc)

    if not format:
        return datafile_content

    try:
        datafile = parse_pipe(filename=pipe.name, replace_includes=False, content=datafile_content)
        datafile_content_formatted = await format_pipe(
            filename=pipe.name,
            line_length=DEFAULT_FMT_LINE_LENGTH,
            unroll_includes=False,
            replace_includes=False,
            datafile=datafile,
        )
    except Exception as e:
        logging.warning(f"Error on generate_pipe_datafile, fallback to default content: {e}")
        return datafile_content

    return datafile_content_formatted
