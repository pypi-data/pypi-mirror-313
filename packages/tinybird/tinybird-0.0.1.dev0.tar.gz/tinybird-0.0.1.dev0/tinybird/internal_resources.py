import asyncio
import logging
import os
import uuid
from typing import Any, Dict, List, Optional, Tuple

from tinybird.internal_data_project import push_internal_data_project
from tinybird.sql import parse_table_structure
from tinybird.tokens import scopes

from .ch import CHTable, HTTPClient, ch_flush_logs_on_all_replicas
from .ch_utils.exceptions import CHException
from .constants import CHCluster
from .default_tables import DefaultTable, DefaultView
from .job import JobExecutor
from .table import create_table_from_schema
from .user import NameAlreadyTaken, User, UserAccountDoesNotExist, UserAccounts, UserDoesNotExist, Users, public

CH_INTERNAL_HOST = os.environ.get("CLICKHOUSE_CLUSTER_INTERNAL_HOST", "ci_ch_internal")
CH_INTERNAL_CLUSTER = os.environ.get("CLICKHOUSE_INTERNAL_CLUSTER", "internal")
CH_INTERNAL_PORT = os.environ.get("CLICKHOUSE_INTERNAL_PORT", "6081")
CH_INTERNAL_ADDRESS = f"{CH_INTERNAL_HOST}:{CH_INTERNAL_PORT}"
INTERNAL_CLUSTER = CHCluster(name=CH_INTERNAL_CLUSTER, server_url=CH_INTERNAL_ADDRESS)


async def init_internal_tables(
    tables: List[DefaultTable],
    clickhouse_cluster: Optional[CHCluster] = None,
    read_only: bool = False,
    populate_views: bool = True,
    metrics_cluster: Optional[str] = None,
    metrics_database: str = "default",
    job_executor: Optional[JobExecutor] = None,
) -> None:
    """initialize internal tables (used for application purposes)"""
    workspace, yepcode_workspace, is_created = await _get_or_create_internal_workspace(clickhouse_cluster)

    # We're using include datafiles in Internal that need this environment variable set. If it is not already set,
    # we set it to the default value and unset it after initializing Internal
    orb_billing_region_unset = False
    if os.environ.get("ORB_BILLING_REGION") is None:
        orb_billing_region_unset = True
        os.environ["ORB_BILLING_REGION"] = "DEFAULT"
    orb_events_sink_dest_unset = False
    if os.environ.get("ORB_EVENTS_SINK_DEST") is None:
        orb_events_sink_dest_unset = True
        os.environ["ORB_EVENTS_SINK_DEST"] = "disabled"
    try:
        if not read_only:
            logging.info("Initializing internal Data Sources")
            if is_created:
                # we create the internal data project only if the Internal workspace is created
                # otherwise, we assume that the project is already created and it's deployed independently
                # FIXME: if first push fails, we need a way to retry it, for now we can just tb push --push-deps manually
                await push_internal_data_project(
                    yepcode_workspace, project_path=f"{os.path.dirname(__file__)}/data_projects/yepcode_integration"
                )
                await push_internal_data_project(workspace)
            await _create_additional_internal_tables(workspace, tables, metrics_cluster, metrics_database)
    finally:
        if orb_billing_region_unset:
            del os.environ["ORB_BILLING_REGION"]
        if orb_events_sink_dest_unset:
            del os.environ["ORB_EVENTS_SINK_DEST"]


async def init_metrics_tables(
    host: str,
    metrics_cluster: Optional[str],
    metrics_database_server: Optional[str],
    metrics_tables: Optional[List[DefaultTable]] = None,
    metrics_views: Optional[List[DefaultView]] = None,
    metrics_cluster_tables: Optional[List[DefaultTable]] = None,
    metrics_cluster_views: Optional[List[DefaultView]] = None,
    metrics_database: str = "default",
    add_datasources: bool = True,
    dry_run: bool = False,
    host_cluster: Optional[str] = None,
) -> None:
    """
    Initialize metrics tables and views related to metrics

    For metrics cluster:
        - Tables are created
        - Views are created
    For Internal workspace (add_datasources == True):
        - A datasource with a distributed engine to the metrics cluster
        - A materialized view that pushes data to this data source, so it's inserted
          directly into the common metrics cluster, in the 'default' database by default
    For each host: (specify one and add_datasources == False)
        - Some tables and materialized as Internal workspace but without datasource
    """
    if not metrics_cluster or not metrics_database_server:
        logging.info(
            f"No metrics cluster configured: metrics_cluster={metrics_cluster}, metrics_database_server={metrics_database_server}"
        )
        return

    client = HTTPClient(metrics_database_server)
    await _create_metrics_database(client, metrics_database_server, metrics_cluster, metrics_database, dry_run)

    metrics_cluster_tables = metrics_cluster_tables or []
    metrics_cluster_views = metrics_cluster_views or []
    await _create_metrics_cluster_tables(client, metrics_cluster, metrics_database, metrics_cluster_tables, dry_run)
    await _create_metrics_cluster_views(client, metrics_cluster, metrics_database, metrics_cluster_views, dry_run)

    public_user = public.get_public_user()
    metrics_tables = metrics_tables or []
    metrics_views = metrics_views or []

    await ch_flush_logs_on_all_replicas(host)
    await _create_host_metrics_tables(
        host,
        metrics_cluster,
        metrics_database,
        metrics_tables,
        public_user,
        add_datasources,
        dry_run,
        host_cluster=host_cluster,
    )
    await _create_host_metrics_views(
        host, metrics_views, public_user, add_datasources, dry_run, host_cluster=host_cluster
    )


async def _get_or_create_internal_workspace(clickhouse_cluster: Optional[CHCluster]) -> Tuple[User, User, bool]:
    is_created = True
    try:
        workspace = public.get_public_user()
        is_created = False
        logging.info("Public user already exists")
    except (UserDoesNotExist, UserAccountDoesNotExist):
        logging.info(f"Creating public user with cluster in ClickHouse cluster={clickhouse_cluster}")
        workspace = public.register_public_user(cluster=clickhouse_cluster)
    try:
        yepcode_workspace = Users.get_by_name(public.INTERNAL_YEPCODE_WORKSPACE_NAME)
    except (UserDoesNotExist, UserAccountDoesNotExist):
        try:
            user_account = UserAccounts.get_by_email(public.INTERNAL_USER_EMAIL)
            yepcode_workspace = User.register(
                name=public.INTERNAL_YEPCODE_WORKSPACE_NAME, admin=user_account.id, cluster=clickhouse_cluster
            )
        except NameAlreadyTaken:
            pass
    if clickhouse_cluster:
        await Users.set_cluster(yepcode_workspace, clickhouse_cluster)
    else:
        await Users.create_database(yepcode_workspace)

    client = HTTPClient(workspace.database_server, database=None)
    cluster_clause = f"ON CLUSTER {workspace.cluster}" if workspace.cluster else ""
    # Try to create the public database always since in dev is pretty common to delete things from CH and not from redis
    await client.query(f"CREATE DATABASE IF NOT EXISTS {workspace.database} {cluster_clause}", read_only=False)

    logging.info(f"Public user is setup on cluster {workspace.cluster}")
    return workspace, yepcode_workspace, is_created


async def _create_additional_internal_tables(
    workspace: User, tables: List[DefaultTable], metrics_cluster: Optional[str], metrics_database: Optional[str]
) -> None:
    workspace = User.get_by_id(workspace.id)
    pending_tables = [table for table in tables if not workspace.get_datasource(table.name, False, False)]
    template_engine_vars = {"cluster": metrics_cluster, "database": metrics_database} if metrics_cluster else {}

    if not pending_tables:
        logging.info("All internal Data Sources already exist")
    else:
        logging.info(f"Creating missing internal Data Sources ({len(pending_tables)}/{len(tables)})")
        created = Users.add_many_datasources(
            workspace,
            datasources=[(table.name, table.fixed_name) for table in pending_tables],
            cluster=workspace.cluster,
            tags={"__version": 0},
        )

        random_id = uuid.uuid4().hex
        with User.transaction(workspace.id) as user:
            for ds in created:
                read_token_name = f"{ds.name} (Data Source read {random_id})"
                append_token_name = f"{ds.name} (Data Source append {random_id}"

                user.add_token(read_token_name, scopes.DATASOURCES_READ, ds.id)
                user.add_token(append_token_name, scopes.DATASOURCES_APPEND, ds.id)

        tasks = []
        for t in pending_tables:
            tasks.append(
                create_table_from_schema(
                    workspace=workspace,
                    datasource=next(d for d in created if d.name == t.name),
                    schema=t.schema,
                    engine=t.engine_template.format(**template_engine_vars)
                    if metrics_cluster and t.engine_template
                    else t.engine,
                    create_quarantine=False,
                    not_exists=True,
                )
            )
        await asyncio.gather(*tasks)

    for table in tables:
        ds = Users.get_datasource(workspace, table.name)

        async def run_migration(u, datasource, migration):
            client = HTTPClient(u["database_server"], database=u["database"])
            cluster_clause = f"ON CLUSTER {workspace.cluster}" if workspace.cluster else ""
            q = f"ALTER TABLE {u.database}.{datasource.id} {cluster_clause} {', '.join(migration)}"
            await client.query(q, read_only=False)

        current_version = latest_version = ds.tags.get("__version", 0)
        for version, migration in enumerate(table.migrations, 1):
            if version > current_version:
                await run_migration(workspace, ds, migration)
                latest_version = version

        if current_version != latest_version:
            with User.transaction(workspace.id) as internal_workspace:
                ds.tags["__version"] = latest_version
                internal_workspace.update_datasource(ds)


async def _create_metrics_database(client: HTTPClient, server: str, cluster: str, database: str, dry_run: bool):
    create_database_query = f"CREATE DATABASE IF NOT EXISTS {database} on cluster {cluster}"

    if dry_run:
        logging.info(f"Run query: {create_database_query} in {server}")
    else:
        try:
            await client.query(create_database_query, read_only=False)
        except CHException as e:
            logging.warning(f"Exception when creating {database} database on {cluster}: {str(e)}")


async def _create_metrics_cluster_tables(
    client: HTTPClient, cluster: str, database: str, tables: List[DefaultTable], dry_run: bool
):
    logging.info(f"Initializing tables in metrics cluster '{cluster}'")
    queries = []

    for table in tables:
        try:
            columns = parse_table_structure(table.schema)
            ch_table = CHTable(columns, cluster=cluster, engine=table.engine, not_exists=True)
            query = ch_table.as_sql(database, table.name)
            queries.append((table.name, table.fixed_name, query))
        except CHException as e:
            logging.warning(f"Exception when creating {table.name} table: {e}")

    async def create_metrics_table_helper(name, query):
        logging.info(
            f"Creating metrics table '{name}' on host='{client.host}', cluster='{cluster}', database='{database}'"
        )
        if dry_run:
            logging.info(f"Metrics table query {query} on {cluster} in {database}")
        else:
            try:
                await client.query(query, read_only=False)
            except CHException as e:
                logging.warning(f"Exception when creating table '{name}', query: '{query}', error: {e}")

    tasks = []
    for name, _, query in queries:
        tasks.append(create_metrics_table_helper(name, query))
    await asyncio.gather(*tasks)


async def _create_metrics_cluster_views(
    client: HTTPClient, cluster: str, database: str, views: List[DefaultView], dry_run: bool
):
    logging.info(f"Initializing views in metrics cluster '{cluster}'")

    async def create_metrics_matview_helper(metrics_view: DefaultView):
        template_view_vars = {"metrics_database": database}
        query = metrics_view.query_template.format(**template_view_vars)

        logging.info(
            f"Creating metrics view '{metrics_view.name}' on host='{client.host}', cluster='{cluster}', database='{database}'"
        )
        if dry_run:
            logging.info(f"Metrics cluster view query {query} ")
        else:
            try:
                matview_query = f"""
                            CREATE MATERIALIZED VIEW IF NOT EXISTS {database}.{metrics_view.name} ON CLUSTER {cluster}
                            TO {database}.{metrics_view.table}
                            AS ({query})
                        """
                await client.query(matview_query, read_only=False)
            except CHException as e:
                logging.exception(f"Exception when creating {database}.{metrics_view.name} view: {e}")

    tasks = []
    for view in views:
        tasks.append(create_metrics_matview_helper(view))
    await asyncio.gather(*tasks)


async def _create_host_metrics_tables(
    host: str,
    metrics_cluster: str,
    database: str,
    tables: List[DefaultTable],
    public_user: User,
    add_datasources: bool,
    dry_run: bool,
    table_mapping: Optional[Dict[str, str]] = None,
    ignore_errors: bool = True,
    host_cluster: Optional[str] = None,
) -> None:
    metrics_table_queries: List[Tuple[str, bool, Any]] = []

    for table in tables:
        table_name: str = table.name

        logging.info(f"Initializing table '{table_name}' on '{host}'")

        if table_mapping and table_name in table_mapping:
            new_name = table_mapping[table_name]
            logging.info(f" >>> '{table_name}' will be created as {new_name} on '{host}'")
            table_name = new_name

        try:
            datasource = Users.get_datasource(public_user, table_name) if add_datasources and not host_cluster else None
            if not datasource:
                engine: Optional[str]

                if table.engine_template:
                    template_engine_vars = {"cluster": metrics_cluster, "database": database}
                    engine = table.engine_template.format(**template_engine_vars)
                else:
                    engine = table.engine
                columns = parse_table_structure(table.schema)
                cluster: Optional[str] = None
                if host_cluster:
                    cluster = host_cluster
                elif add_datasources:
                    cluster = public_user.cluster
                ch_table = CHTable(columns, cluster=cluster, engine=engine, not_exists=True)
                query = ch_table.as_sql(public_user.database, table_name)
                metrics_table_queries.append((table_name, table.fixed_name, query))
            else:
                logging.info(f"Internal Data Source '{table_name}' already exists")
        except CHException as e:
            logging.warning(f"Exception when creating {table_name} table: {e}")
            if not ignore_errors:
                raise e

    logging.info(f"Initializing tables in metrics on '{host}'")

    if host_cluster:
        cluster_clause = f"ON CLUSTER {host_cluster} "
    else:
        cluster_clause = f"ON CLUSTER {public_user.cluster} " if add_datasources and public_user.cluster else ""

    create_database_query = f"CREATE DATABASE IF NOT EXISTS {public_user.database} {cluster_clause}"
    if dry_run:
        logging.info(f'Run query: "{create_database_query}" on host {host}')
    else:
        try:
            client = HTTPClient(host, database=None)
            await client.query(create_database_query, read_only=False)
        except CHException as e:
            logging.warning(f"Exception when creating {public_user.database} user database: {str(e)}")
            if not ignore_errors:
                raise e

    for name, fixed_name, query in metrics_table_queries:
        logging.info(f"Creating {name} on host {host}...")
        if dry_run:
            logging.info(f"Metrics table query {query} on host {host}")
        else:
            create_datasource = True
            try:
                client = HTTPClient(host, database=public_user.database)
                await client.query(query, read_only=False)
            except CHException as e:
                logging.info(f"Exception when creating data source '{name}', query: '{query}', error: {e}")
                if not ignore_errors:
                    raise e

                error = str(e)
                create_datasource = "TABLE_ALREADY_EXISTS" in error or "already exists" in error

            if add_datasources and create_datasource:
                await Users.add_datasource_async(
                    public_user, ds_name=name, cluster=public_user.cluster, fixed_name=fixed_name
                )


async def _create_host_metrics_views(
    host: str,
    views: List[DefaultView],
    public_user: User,
    add_datasources: bool,
    dry_run: bool,
    host_cluster: Optional[str] = None,
) -> None:
    logging.info(f"Initializing metrics views for host {host}")

    for metrics_view in views:
        logging.info(f"Creating metrics view '{metrics_view.name}'for host {host}")

        if host_cluster:
            cluster_clause = f"ON CLUSTER {host_cluster} "
        else:
            cluster_clause = f"ON CLUSTER {public_user.cluster} " if add_datasources and public_user.cluster else ""
        matview_query = f"""
                    CREATE MATERIALIZED VIEW IF NOT EXISTS {public_user.database}.{metrics_view.name} {cluster_clause}
                    TO {public_user.database}.{metrics_view.table}
                    AS ({metrics_view.query_template})
                """
        if dry_run:
            logging.info(f"Metrics view query {matview_query} on host {host}")

        else:
            client = HTTPClient(host, database=public_user.database)

            try:
                await client.query(matview_query, read_only=False)
            except CHException as e:
                if "UNKNOWN_TABLE" in str(e):
                    logging.warning(f"Flush logs to force creation system logs tables for {matview_query}")
                    await ch_flush_logs_on_all_replicas(host, public_user.cluster, user_agent="tb-internal-query")
                    await client.query(matview_query, read_only=False)
                else:
                    raise e
