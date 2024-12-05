import json
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, fields
from functools import partial
from typing import Iterator, List, Optional, Union

import click

from tinybird.ch import CHReplication, HTTPClient, ch_get_columns_from_query_sync
from tinybird.ch_utils.engine import engine_local_to_replicated
from tinybird.ch_utils.exceptions import CHException
from tinybird.data_connector import DataConnector
from tinybird.datasource import SharedDatasource
from tinybird.user import User as Workspace
from tinybird.user import Users
from tinybird_shared.clickhouse.errors import CHErrors


@dataclass
class WorkspaceData:
    name: str
    id: str
    cluster: Optional[str]
    database: str
    database_server: str
    datasources: int
    linkers: str
    enabled_pg: bool
    origin: Optional[str]
    number_releases: int
    deleted: bool

    def __iter__(self):
        for field in fields(self):
            yield getattr(self, field.name)


def get_workspaces_data(
    email_needle: str | None,
    name_needle: str | None,
    cluster: str | None,
    include_deleted: bool | None,
    only_branches: bool = False,
    only_releases: bool = False,
) -> List[WorkspaceData]:
    # get all metadata filter later
    workspaces: Union[Iterator[Workspace], List[Workspace]] = Workspace.get_all(
        include_branches=True, include_releases=True
    )

    def matching_email(ws: Workspace) -> bool:
        ws_users = ws.get_workspace_users()
        for u in ws_users:
            email: str = u.get("email", "")
            if email_needle and email_needle.lower() in email.lower():
                return True
        return False

    if email_needle:
        workspaces = filter(matching_email, workspaces)

    if name_needle:
        workspaces = filter(lambda ws: ws.name and name_needle in ws.name, workspaces)

    if cluster:
        workspaces = filter(lambda ws: ws.cluster == cluster, workspaces)

    if not include_deleted:
        workspaces = filter(lambda ws: not ws.deleted, workspaces)

    if only_branches:
        workspaces = filter(lambda ws: ws.is_branch, workspaces)

    if only_releases:
        workspaces = filter(lambda ws: ws.is_release, workspaces)

    found_workspaces: List[WorkspaceData] = []
    for ws in workspaces:
        data_connectors = DataConnector.get_user_data_connectors(ws.id)

        linkers_count = sum([len(c["linkers"]) for c in data_connectors])
        linkers_hosts = set()
        for c in data_connectors:
            for linker in c["linkers"]:
                linker_ch_host = linker.get("settings", {}).get("clickhouse_host", None)
                if linker_ch_host:
                    linkers_hosts.add(linker_ch_host)
        found_workspaces.append(
            WorkspaceData(
                ws.name,
                ws.id,
                ws.cluster,
                ws.database,
                ws.database_server,
                len([ds for ds in ws.get_datasources() if not isinstance(ds, SharedDatasource)]),
                f"{linkers_count} {linkers_hosts}",
                ws.enabled_pg,
                ws.origin,
                len(ws.releases),
                ws.deleted,
            )
        )

    return sorted(found_workspaces, key=lambda x: x.name.lower())


def is_engine(engine, table):
    return engine in table["engine"]


is_materialized = partial(is_engine, "Materialized")
is_join = partial(is_engine, "Join")
is_mergetree = partial(is_engine, "MergeTree")
is_replicated = partial(is_engine, "Replicated")


def is_materialized_with_inner(table):
    return is_materialized(table) and "ENGINE" in table["create_table_query"]


def is_inner(table):
    return table["name"].startswith(".inner")


SUFFIX_TABLE_CONVERTED_TO_REPLICATED = "__renamed_before_converting_to_replicated"


def is_already_converted_to_replicated(table):
    return SUFFIX_TABLE_CONVERTED_TO_REPLICATED in table["name"]


def recreate_workspace_internal(
    orig_host,
    dest_host,
    workspace_id,
    create_tables,
    create_materialized_views,
    ignore_existing_tables,
    ignore_missing_resources,
    workers,
    dry_run,
    debug,
    skip_wait_for_replication,
    storage_policy,
):
    workspace = Workspace.get_by_id(workspace_id)
    database_server = orig_host
    database = workspace["database"]
    click.secho(f"Recreating workspace {workspace.name} (database {database}) from {database_server} to {dest_host}")

    def section(msg):
        click.secho(msg, bg="bright_blue", fg="black", bold=True)

    def orig_query(sql):
        client = HTTPClient(database_server, database=database)
        headers, body = client.query_sync(sql)
        if "application/json" in headers["content-type"]:
            return json.loads(body)
        return body

    def dest_query(sql, desc=None, force_run=False, **kwargs):
        if desc:
            click.secho(f"## {desc}")
        if debug:
            click.secho(f" > Query: {sql}")
        if dry_run and not force_run:
            click.secho(f' - [DRY RUN] Skipping query: "{sql}"', fg="cyan")
            return {}
        extra_params = {"max_execution_time": 7200, "max_result_bytes": 0, **kwargs}
        client = HTTPClient(dest_host, database=database)
        try:
            headers, body = client.query_sync(sql, read_only=False, **extra_params)
            if "application/json" in headers["content-type"]:
                return json.loads(body)
            return body
        except Exception as e:
            click.secho(f' - [ERROR] Failed to run query: "{sql}"\nReason={e}', fg="red")
            raise e

    def dest_query_and_wait_for_replication(sql, table_name, desc=None):
        dest_query(sql, desc=desc)
        if dry_run:
            click.secho(f" - [DRY RUN] [{table_name}] Skipping wait for replication", fg="cyan")
            return True
        if skip_wait_for_replication:
            click.secho(f" - [{table_name}] Skipping wait for replication", fg="cyan")
            return True
        replication_success = CHReplication.ch_wait_for_replication_sync(
            database_server, workspace.cluster, database, table_name, wait=5 * 60 * 60, debug=False
        )
        if not replication_success:
            click.secho(f" - [{table_name}] Failed to wait for replication", fg="red")
        else:
            click.secho(f" - [{table_name}] Successfully waited for replication", fg="green")

    # Create database
    tables_query = f"""SELECT
            name,
            engine,
            engine_full,
            create_table_query
        FROM
            system.tables
        WHERE
            database = '{database}'
        FORMAT JSON"""

    try:
        orig_result = orig_query(tables_query).get("data", [])
        orig_tables = {t["name"]: t for t in orig_result}
    except CHException as e:
        if e.code != CHErrors.UNKNOWN_DATABASE:
            raise e
        click.secho(f" - [{database}] Doesn't exists in origin, skipping database creation", fg="red")
        return

    section("# Creating database")
    if dry_run:
        click.secho(" - [DRY RUN] Skipping database creation", fg="cyan")
    else:
        try:
            client = HTTPClient(dest_host, database=None)
            client.query_sync(f"create database {database}", read_only=False)
        except CHException as e:
            if e.code != CHErrors.DATABASE_ALREADY_EXISTS:
                raise e

    try:
        dest_result = dest_query(tables_query).get("data", [])
    except CHException as e:
        if e.code != CHErrors.UNKNOWN_DATABASE:
            raise e
        dest_result = []
    dest_tables = {t["name"]: t for t in dest_result}

    # ---------------------------------------------------------------------
    # Validation phase
    # ---------------------------------------------------------------------

    # Validate every table has a resource associated with it
    if not ignore_missing_resources:
        for name, table in orig_tables.items():
            if is_already_converted_to_replicated(table):
                continue
            try:
                ds = Users.get_datasource(workspace, name)
                pipe = Users.get_pipe_by_node(workspace, name)
                pipe_view = Users.get_pipe(workspace, name)
                if not ds and not pipe and not pipe_view:
                    raise ValueError("Resource not found")
            except Exception:
                click.secho(f"Couldn't find resource for table '{name}', engine='{table['engine']}'", fg="red")
                if not click.confirm("Do you want to continue?"):
                    sys.exit(1)

    # Validate destination database doesn't have any of the resources
    if not ignore_existing_tables:
        for name, table in orig_tables.items():
            if name in dest_tables:
                click.secho(f"Table '{name}' already exists", fg="red")
                if debug:
                    click.secho(f" > Origin Query:      {table['create_table_query']}")
                    click.secho(f" > Destination Query: {dest_tables[name]['create_table_query']}")
                click.secho("We will skip the creation in the destination server", fg="red")
                if click.confirm("Do you want to continue?"):
                    continue
                sys.exit(1)

    # ---------------------------------------------------------------------
    # Creation phase
    # ---------------------------------------------------------------------

    # Recreate replicated tables and wait for replication to finish
    section("# Creating tables")
    create_tasks = []
    for name, table in orig_tables.items():
        if is_already_converted_to_replicated(table):
            continue
        if is_inner(table):
            click.secho(f" - [{name}] Skipping .inner table from Materialized View", fg="magenta")
            continue

        create_table_query = table["create_table_query"]

        if storage_policy is not None and table["engine"] not in ("Null", "Join"):
            if "SETTINGS" in table["create_table_query"]:
                create_table_query = table["create_table_query"].replace(
                    "SETTINGS", f"SETTINGS storage_policy='{storage_policy}', "
                )
            else:
                create_table_query = table["create_table_query"] + f" SETTINGS storage_policy='{storage_policy}'"

        resource = (
            Users.get_datasource(workspace, name)
            or Users.get_pipe_by_node(workspace, name)
            or Users.get_pipe(workspace, name)
        )
        resource_name = resource.name if resource else "unknown"
        if is_materialized(table):
            if not create_materialized_views:
                click.secho(
                    f" - [{name}] Skipping Materialized View creation for resource {resource_name}", fg="magenta"
                )
                continue
            if is_materialized_with_inner(table):
                click.echo(
                    f" ********* Converting MATERIALIZED VIEW TO for table='{table['name']}' with ReplicatedMergeTree"
                    " engine"
                )
                replicated_engine = engine_local_to_replicated(
                    table["engine_full"], database, f".inner.{table['name']}"
                )
                create_table_query = table["create_table_query"].replace(table["engine_full"], replicated_engine)

                click.echo("=" * 100)
                click.echo(table["create_table_query"])
                click.echo("-" * 100)
                click.echo(create_table_query)
                click.echo("=" * 100)
        else:
            if not create_tables:
                click.secho(f" - [{name}] Skipping Table creation for resource {resource_name}", fg="magenta")
                continue
        if name in dest_tables:
            click.secho(f" - [{name}] Skipping creation for resource {resource_name}, it already exists", fg="magenta")
            continue

        create_tasks.append(
            [
                create_table_query,
                name,
                f"Creating table {name} for resource {resource_name}",
            ]
        )

    with ThreadPoolExecutor(max_workers=workers, thread_name_prefix="recreate_database") as executor:
        for task in create_tasks:
            executor.submit(dest_query_and_wait_for_replication, *task)
        executor.shutdown(wait=True)

    # Populate non replicated engines
    populate_tasks = []
    for name, table in orig_tables.items():
        node = Users.get_node_by_materialized(workspace, name, i_know_what_im_doing=True)
        if node and is_join(table):
            pipe = Users.get_pipe_by_node(workspace, node.id)
            select_sql = Users.replace_tables(workspace, node.sql, pipe=pipe, use_pipe_nodes=True)
            columns_dict = ch_get_columns_from_query_sync(database_server, database, select_sql)
            columns_str = ",".join([f"`{c['name']}`" for c in columns_dict])
            populate_tasks.append(
                [f"TRUNCATE TABLE {database}.`{name}`", f"[{name}] Truncate table to make sure is empty"]
            )
            populate_tasks.append(
                [f"INSERT INTO {database}.`{name}` ({columns_str}) {select_sql}", f"[{name}] Populating table"]
            )

    # Only populate join tables when we are creating them
    if create_tables and populate_tasks:
        section("# Populating non-replicated Join tables from their MV queries")

        with ThreadPoolExecutor(max_workers=workers, thread_name_prefix="recreate_database") as executor:
            for task in populate_tasks:
                executor.submit(dest_query, *task)
            executor.shutdown(wait=True)
