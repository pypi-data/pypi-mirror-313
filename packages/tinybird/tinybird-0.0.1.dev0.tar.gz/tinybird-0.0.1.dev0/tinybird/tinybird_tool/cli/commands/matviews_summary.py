import json
import re
import sys
import time
from datetime import datetime
from typing import Any, Dict

import click
import requests

from tinybird.ch import HTTPClient, ch_table_dependent_views_sync, ch_table_details_async
from tinybird.syncasync import async_to_sync
from tinybird.user import User as Workspace
from tinybird.user import Users

from ... import common
from ..cli_base import cli

ch_table_details_sync = async_to_sync(ch_table_details_async)


@cli.command()
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
@click.option("--token", type=str, help="Internal workspace token in eu-shared")
def matviews_summary(config, token):
    conf, _ = common.setup_redis_client(config=config)
    host = conf["api_host"]

    workspaces = Workspace.get_all(include_branches=True, include_releases=True)
    date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    if not token:
        click.secho("ERROR: Provide r@localhost Internal workspace token", fg="red")
        sys.exit(1)

    for workspace in workspaces:
        engine_per_database = {}
        try:
            click.secho(f"** Workspace '{workspace.id}'", fg="blue")
            for ds in workspace.get_datasources():
                if hasattr(ds, "original_workspace_id"):
                    original_workspace = Users.get_by_id(ds.original_workspace_id)
                else:
                    original_workspace = workspace

                click.secho(f"** Datasource '{ds.name}'", fg="blue")
                engine = ch_table_details_sync(
                    ds.id, original_workspace["database_server"], database=original_workspace["database"]
                )

                time.sleep(0.1)
                dependent_views = ch_table_dependent_views_sync(
                    original_workspace["database_server"], original_workspace["database"], ds.id
                )
                time.sleep(0.1)
                ds_obj = ds.to_json()
                engine_obj = engine.to_json()
                engine_per_database[ds.id] = engine_obj

                nodes = [Users.get_node(workspace, dependent_view.table) for dependent_view in dependent_views]

                ds_obj["engine"] = engine_obj["engine"]
                ds_obj["engine_full"] = engine_obj["engine_full"]
                ds_obj["workspace_id"] = workspace.id
                ds_obj["workspace_name"] = workspace.name
                ds_obj["date"] = date
                ds_obj["dependent_views"] = [
                    node.materialized for node in nodes if node is not None and node.materialized
                ] or []
                ds_obj["dependent_pipes"] = [node.id for node in nodes if node is not None and node.id] or []
                ds_obj["is_shared"] = 0 if original_workspace.id == workspace.id else 1

                if not ds_obj["dependent_views"]:
                    ds_obj["dependent_views"] = []
                if not ds_obj["dependent_pipes"]:
                    ds_obj["dependent_pipes"] = []

                _, _, target_ds, _, _, _ = Users.get_used_by_materialized_nodes(workspace, ds.name)

                ds_obj["dependencies"] = target_ds
                time.sleep(0.1)
                params = {"name": "datasource_metrics"}

                r = requests.post(
                    f"{host}/v0/events",
                    params=params,
                    headers={"Authorization": f"Bearer {token}"},
                    data=json.dumps(ds_obj),
                )

                if r.status_code >= 400:
                    click.secho(f"** Error: could not append. Reason: {r.text}", fg="red")
                else:
                    click.secho("** appended", fg="green")

            for pipe in workspace.get_pipes():
                click.secho(f"** Pipe '{pipe.name}'", fg="blue")
                obj: Dict[str, Any] = {}
                obj["date"] = date
                obj["workspace_id"] = workspace.id
                obj["workspace_name"] = workspace.name
                obj["pipe"] = pipe.id
                obj["matviews"] = []

                for node in pipe.pipeline.nodes:
                    if "getting_started" in node.name:
                        continue
                    click.secho(f"** Node '{node.name}'", fg="blue")

                    if node.materialized:
                        d = workspace.get_datasource(node.materialized, include_read_only=True)
                        if not d:
                            continue

                        if hasattr(d, "original_workspace_id"):
                            original_workspace = Users.get_by_id(d.original_workspace_id)
                        else:
                            original_workspace = workspace
                            engine = ch_table_details_sync(
                                node.materialized,
                                original_workspace["database_server"],
                                database=original_workspace["database"],
                            )

                            time.sleep(0.1)
                            obj["matviews"].append(
                                {
                                    "datasource": node.materialized,
                                    "sql": node.sql,
                                    "engine_full": engine.engine_full,
                                    "engine": engine.engine,
                                    "id": node.id,
                                }
                            )

                if len(obj["matviews"]):
                    params = {"name": "matviews_metrics"}
                    r = requests.post(
                        f"{host}/v0/events",
                        params=params,
                        headers={"Authorization": f"Bearer {token}"},
                        data=json.dumps(obj),
                    )
                    if r.status_code >= 400:
                        click.secho(f"** Error: could not append. Reason: {r.text}", fg="red")
                    else:
                        click.secho("** appended", fg="green")
                else:
                    click.secho("** discarded", fg="blue")
        except Exception as e:
            import traceback

            traceback.print_exc()
            click.secho(f"** error: {e}")


@cli.command()
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
def matviews_using_asterisk(config):
    config, _ = common.setup_redis_client(config)
    clusters = config.get("clickhouse_clusters", {})
    materialized_views_with_asterisk = []

    for _, cluster in clusters.items():
        client = HTTPClient(cluster)

        try:
            _, _ = client.query_sync("SELECT 1")
        except Exception:
            click.secho(f"Skipping cluster {cluster}")
            continue

        click.secho(f"** Getting materialized views list for cluster {cluster}...")
        matviews_query = f"""
            SELECT
                '{cluster}' as cluster,
                database,
                name,
                as_select as query
            FROM system.tables
            WHERE engine = 'MaterializedView'
            AND
                as_select LIKE '%*%'
            ORDER BY cluster, database
            FORMAT JSON
        """

        _, body = client.query_sync(matviews_query)

        materialized_views = json.loads(body)["data"]

        click.secho("** Checking which ones use asterisk wildcard to get all columns...")
        for materialized_view in materialized_views:
            query = f"EXPLAIN AST {materialized_view['query']}"
            _, result = client.query_sync(query)
            query_ast = result.decode("utf-8").replace("\n", "")

            if re.search(r"\bAsterisk\b", query_ast):
                materialized_views_with_asterisk.append(materialized_view)

    click.secho("** List of materialized views by database:")
    for view in materialized_views_with_asterisk:
        click.secho(f"{view['cluster']} - {view['database']}.{view['name']}")
