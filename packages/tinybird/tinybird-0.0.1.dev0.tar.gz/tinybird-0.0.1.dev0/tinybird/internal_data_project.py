import asyncio
import logging
import os
from typing import Any, Coroutine, Dict, Iterable, List, Optional

from tinybird.ch import ch_create_materialized_view
from tinybird.client import TinyB
from tinybird.datafile import get_project_filenames, process_file
from tinybird.pipe import PipeNodeTypes
from tinybird.sql import parse_indexes_structure, parse_table_structure
from tinybird.table import create_table_from_schema
from tinybird.token_origin import TokenOrigin
from tinybird.token_scope import ScopeException
from tinybird.tokens import AccessToken, scope_names
from tinybird.user import User, Users, public
from tinybird.views.api_pipes import NodeUtils
from tinybird.views.api_tokens import format_token
from tinybird.views.json_deserialize_utils import json_deserialize_merge_schema_jsonpaths, parse_augmented_schema
from tinybird.workspace_service import WorkspaceService


async def push_internal_data_project(workspace: User, project_path: Optional[str] = None) -> None:
    # Get the project dir in the repo
    if not project_path:
        project_path = f"{os.path.dirname(__file__)}/data_projects/Internal"
    project_filenames = get_project_filenames(project_path)

    # Parse all datasources
    to_run: Dict[str, Any] = {}

    resource_versions: Dict[str, Optional[int]] = {}

    async def parse_project_files(filenames: Iterable[str]):
        for filename in filenames:
            if os.path.isdir(filename):
                await parse_project_files(filenames=get_project_filenames(filename))
            else:
                file_resources = await process_file(
                    filename, TinyB("token", "host"), resource_versions=resource_versions
                )
                for resource in file_resources:
                    to_run[resource["resource_name"]] = resource
                    # get_project_filenames is processing datasources first
                    if resource["version"]:
                        resource_versions[resource["resource_name"]] = resource["version"]

    # Fill `to_run` with all the resources in the project
    await parse_project_files(filenames=project_filenames)

    # Insert datasources into CH
    ds_tasks: List[Coroutine[Any, Any, None]] = []

    def _get_engine_args(params: Dict[str, str]) -> Dict[str, str]:
        engine_args = {"type": params["engine"]}
        for k, v in params.items():
            if k.startswith("engine_"):
                engine_args[k[len("engine_") :]] = v
        return engine_args

    for _, res in to_run.items():
        if res["resource"] == "datasources":
            params = res["params"]
            if workspace.get_datasource(params["name"]):
                continue

            json_deserialization = None
            schema = params["schema"]
            if params.get("format", "csv") != "csv":
                parsed_schema = parse_augmented_schema(schema)
                if parsed_schema.jsonpaths:
                    new_columns = parse_table_structure(parsed_schema.schema)
                    json_deserialization = json_deserialize_merge_schema_jsonpaths(new_columns, parsed_schema.jsonpaths)
                    schema = parsed_schema.schema

            ds = await Users.add_datasource_async(workspace, params["name"], json_deserialization=json_deserialization)
            engine = _get_engine_args(params)

            if res.get("shared_with"):
                for workspace_to_share in res["shared_with"]:
                    # this is because of CI
                    if workspace_to_share == "Internal":
                        w = Users.get_by_name(public.INTERNAL_USER_WORKSPACE_NAME)
                    else:
                        w = Users.get_by_name(workspace_to_share)
                    try:
                        await WorkspaceService.share_a_datasource_between_workspaces(workspace, ds.id, w)
                    except ValueError as e:
                        logging.warning(f"Could not share datasource {ds.name} with workspace {w.name}: {str(e)}")

            if res.get("tokens"):
                await _manage_tokens(workspace, ds=res)

            indexes = params.get("indexes")
            new_indexes = None
            if indexes is not None and len(indexes):
                new_indexes = parse_indexes_structure(indexes.splitlines() if indexes != "0" else [])

            logging.info(f"Creating datasource {ds.name} in cluster {workspace.cluster} {workspace.database_server}")
            ds_tasks.append(
                create_table_from_schema(
                    workspace=workspace,
                    datasource=ds,
                    schema=schema,
                    engine=engine,
                    create_quarantine=False,
                    not_exists=True,
                    indexes=new_indexes,
                )
            )

    await asyncio.gather(*ds_tasks)

    # Insert pipes into CH
    for _, res in to_run.items():
        if res["resource"] == "pipes":
            # FIXME support more than one node
            workspace = User.get_by_id(workspace.id)
            assert isinstance(workspace, User)

            res_node = res["nodes"][-1] if len(res["nodes"]) > 1 else res["nodes"][0]
            params = res_node["params"]
            if workspace.get_pipe(res["name"]):
                continue

            def parse_node(node):
                if "params" in node:
                    if "mode" in node["params"]:
                        # FIXME: we need to proper support mode
                        node["params"].pop("mode")
                    node.update(node["params"])
                    del node["params"]
                return node

            # FIXME schedule not supported yet, only on-demand and single node
            if params["type"] == "copy":
                pipe = Users.add_pipe_sync(workspace, res["name"], nodes=[parse_node(node) for node in res["nodes"]])
                workspace = User.get_by_id(workspace.id)
                target_datasource = (
                    Users.get_datasource(workspace, params["target_datasource"])
                    if params.get("target_datasource")
                    else None
                )
                if not target_datasource:
                    raise RuntimeError(
                        f'Datasource {params["target_datasource"]} not found while initializing Internal data project'
                    )
                await NodeUtils.create_node_copy(
                    workspace=workspace,
                    pipe_name_or_id=pipe.id,
                    node_name_or_id=pipe.pipeline.nodes[0].id,
                    target_datasource_id=target_datasource.id,
                    mode=None,
                    edited_by="Init internal resources",
                    target_workspace_id=workspace.id,
                    ignore_sql_errors=True,
                )
                continue

            if params["type"] == "materialized":
                # FIXME support create data source?
                target_datasource = (
                    Users.get_datasource(workspace, params["datasource"]) if params.get("datasource") else None
                )

                if not target_datasource:
                    raise RuntimeError(
                        f'Datasource {params["datasource"]} not found while initializing Internal data project'
                    )

            pipe = Users.add_pipe_sync(workspace, res["name"], nodes=[parse_node(node) for node in res["nodes"]])
            node = pipe.pipeline.last()

            if params["type"] == "materialized":
                node.materialized = target_datasource.id  # type: ignore
            else:
                pipe.endpoint = node.id
                pipe.update_node(node.id, node_type=PipeNodeTypes.ENDPOINT)
                node.materialized = None

            Users.update_pipe(workspace, pipe)
            if params["type"] == "materialized":
                # this is because of CI
                if "yepcode_integration" in res_node["sql"]:
                    sql = res_node["sql"].replace("yepcode_integration", public.INTERNAL_YEPCODE_WORKSPACE_NAME)
                else:
                    sql = res_node["sql"]
                sql = Users.replace_tables(
                    workspace, sql, pipe=pipe, use_pipe_nodes=True, use_service_datasources_replacements=False
                )
                await ch_create_materialized_view(
                    workspace,
                    node.id,
                    sql,
                    engine=None,
                    target_table=target_datasource.id,  # type: ignore
                    if_not_exists=True,
                )

            if "tokens" in res and res["tokens"] and params["type"] != "materialized":
                await _manage_tokens(workspace, pipe=res)


async def _manage_tokens(
    workspace: User, ds: Optional[Dict[str, Any]] = None, pipe: Optional[Dict[str, Any]] = None
) -> None:
    # search for token with specified name and adds it if not found or adds permissions to it
    t: Optional[AccessToken] = None
    if ds:
        r = ds
        origin_code = "DS"
        r_scope = "DATASOURCES"
        r_name = r["params"]["name"]
    elif pipe:
        r = pipe
        origin_code = "P"
        r_scope = "PIPES"
        r_name = r["name"]
    for tk in r["tokens"]:
        token_name = tk["token_name"]
        t = Users.get_token_access_info(workspace, token_name)
        if t:
            break
    if not t:
        token_name = tk["token_name"]
        origin = TokenOrigin(origin_code, r_name)
        new_scopes = [f"{r_scope}:{tk['permissions']}:{r_name}"]
        await Users.create_new_token(workspace, token_name, new_scopes, origin)
    else:
        new_scopes = [f"{r_scope}:{tk['permissions']}:{r_name}"]
        formatted_token: Dict[str, Any] = format_token(workspace, t)
        for x in formatted_token["scopes"]:
            sc = x["type"] if "resource" not in x else f"{x['type']}:{x['resource']}"
            new_scopes.append(sc)
        with User.transaction(workspace.id) as workspace:
            safe_tokens = workspace.tokens
            token_id = formatted_token["name"]

            if not workspace.get_token_access_info(token_id, safe_tokens):
                raise RuntimeError(f"Auth token {token_name} not found while trying to update it")

            # Get the object reference from workspace's list, not from safe_tokens
            token = workspace.get_token_access_info(token_id)
            if not token:
                return

            token.clean_scopes()
            if new_scopes:
                for s in new_scopes:
                    scope, name_or_uid, _filters = AccessToken.parse(s)
                    if scope:
                        resource = None
                        if name_or_uid:
                            resource = workspace.get_resource_id_for_scope(scope, name_or_uid)
                        try:
                            token.add_scope(scope, resource, _filters)
                        except ScopeException as e:
                            raise e
                    else:
                        raise RuntimeError(
                            "Invalid provided scope, valid ones are: %s" % ", ".join(scope_names.values())
                        )
