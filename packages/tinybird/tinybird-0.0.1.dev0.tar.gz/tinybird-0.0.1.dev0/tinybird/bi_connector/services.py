import logging
from functools import reduce

from tinybird.bi_connector.database import CHBIDatabase, CHBIManagementAuthentication, CHBIServer, CHReplicatedEngine
from tinybird.bi_connector.users import CHBIConnectorUser
from tinybird.ch import CHException, HTTPClient, ch_create_view, ch_table_columns
from tinybird.datasource import Datasource
from tinybird.pipe import Pipe
from tinybird.sql_template import SQLTemplateCustomError, SQLTemplateException
from tinybird.tornado_template import ParseError, UnClosedIfError
from tinybird.user import User as Workspace

_bi_management_password: str = ""


class BIConnectorConfiguration(Exception):
    pass


def set_bi_management_password(password: str):
    global _bi_management_password
    _bi_management_password = password


async def initialize_bi_connector(
    workspace: Workspace, bi_server: CHBIServer, bi_user: CHBIConnectorUser, database_prefix: str = ""
):
    management_user_auth = CHBIManagementAuthentication(user="bi_management", password=_bi_management_password)
    db_management_client = HTTPClient(bi_server.get_server_url(management_user_auth), database=None)

    await drop_existing_resources(db_management_client, f"{workspace.database}", bi_user)

    # Build BI Database
    bi_database = await create_replicated_database(db_management_client, workspace, database_prefix=database_prefix)
    bi_user = bi_user.model_copy(update={"default_database": bi_database})

    # Mirror tables and endpoints without parameters
    datasources = workspace.get_datasources()
    await create_distributed_tables_for_datasources(db_management_client, workspace, bi_user, datasources)

    pipes = workspace.get_pipes()
    for pipe in pipes:
        await create_views_for_pipes(bi_server.get_server_url(management_user_auth), bi_database, workspace, pipe)

    # Build User
    await create_bi_user(db_management_client, bi_user)

    # Grant SELECT permissions for that DB
    await grant_select_permissions_for_db(db_management_client, bi_database, bi_user)


async def create_replicated_database(client: HTTPClient, workspace: Workspace, database_prefix=""):
    database_name = f"{database_prefix}{workspace.database}"

    bi_db_engine = CHReplicatedEngine(
        zookeeper_path=f"/clickhouse/bi_connector_dbs/{database_name}",
        shard_name="default_shard",
        replica_name="bi_server",
    )

    bi_database = CHBIDatabase(
        name=database_name, engine=bi_db_engine, comment=f"BI Connector Database for {workspace.name} ({workspace.id})"
    )

    create_database_statement = f"""
    CREATE DATABASE {bi_database.name}
    ENGINE = Replicated('{bi_db_engine.zookeeper_path}', '{bi_db_engine.shard_name}', '{bi_db_engine.replica_name}')
    """

    await client.query(create_database_statement, read_only=False, user_agent="no-tb-bi-management-query")

    return bi_database


async def create_distributed_tables_for_datasources(
    client: HTTPClient, workspace: Workspace, bi_user: CHBIConnectorUser, datasources: list[Datasource]
):
    if not bi_user.default_database:
        raise BIConnectorConfiguration("BI User does not have a created database")

    create_table_queries = []

    for datasource in datasources:
        database_server: str = workspace.database_server
        database: str = workspace.database
        cluster: str = workspace.cluster or ""
        table_id: str = datasource.id
        table_name: str = datasource.name

        columns = await ch_table_columns(database_server, database, table_id)

        create_table_queries.append(
            render_create_table_query(bi_user.default_database.name, table_id, database, cluster, table_id, columns)
        )
        create_table_queries.append(
            render_create_table_query(bi_user.default_database.name, table_name, database, cluster, table_id, columns)
        )

    for create_table in create_table_queries:
        await client.query(create_table, read_only=False, user_agent="no-tb-bi-management-query")

    return create_table_queries


def render_create_table_query(
    bi_database_name: str,
    bi_table_name: str,
    remote_database_name: str,
    remote_cluster_name: str,
    remote_table_name: str,
    columns,
):
    def aggregate_column(agg_columns, column):
        agg_columns.append(f"`{column.get('name')}` {column.get('type')}")
        return agg_columns

    column_statements: list[str] = reduce(aggregate_column, columns, [])

    return f"""
    CREATE TABLE IF NOT EXISTS {bi_database_name}.{bi_table_name}(
        {','.join(column_statements)}
    )
    ENGINE = Distributed({remote_cluster_name}, {remote_database_name}, {remote_table_name})
    """


async def create_views_for_pipes(bi_server_address: str, bi_database: CHBIDatabase, workspace: Workspace, pipe: Pipe):
    if pipe.endpoint:
        logging.info(f"on endpoint changed {pipe.name}")
        try:
            sql = pipe.pipeline.get_sql_for_node(pipe.endpoint)
            sql = workspace.replace_tables(sql)
        except (
            SyntaxError,
            CHException,
            SQLTemplateException,
            SQLTemplateCustomError,
            ParseError,
            UnClosedIfError,
            ValueError,
        ) as e:
            logging.warning(str(e))
            return
        except Exception as e:
            logging.warning(
                f"error on endpoint change {pipe.name}: {e}. Endpoints with templates cannot be published as pg tables so we ignore this type of exceptions."
            )
            return
        await ch_create_view(bi_server_address, bi_database.name, pipe.name, sql)
        logging.info(f"end on endpoint changed {pipe.name}")


async def create_bi_user(client: HTTPClient, bi_user: CHBIConnectorUser):
    if not bi_user.default_database:
        raise BIConnectorConfiguration("BI User does not have a created database")

    create_user_statement = f"""
    CREATE USER OR REPLACE {bi_user.name}
    IDENTIFIED WITH plaintext_password BY '{bi_user.password.password}'
    DEFAULT DATABASE {bi_user.default_database.name}
    GRANTEES NONE
    SETTINGS PROFILE 'bi_connector'
    """

    await client.query(create_user_statement, read_only=False, user_agent="no-tb-bi-management-query")


async def grant_select_permissions_for_db(client: HTTPClient, database: CHBIDatabase, bi_user: CHBIConnectorUser):
    grant_select_permissions_statement = f"""
    GRANT SELECT ON {database.name}.* TO {bi_user.name}
    """

    await client.query(grant_select_permissions_statement, read_only=False, user_agent="no-tb-bi-management-query")

    grant_select_to_informationschema_permissions_statement = f"""
    GRANT SELECT ON INFORMATION_SCHEMA.* TO {bi_user.name}
    """

    await client.query(
        grant_select_to_informationschema_permissions_statement, read_only=False, user_agent="no-tb-bi-management-query"
    )

    grant_show_databases_permissions_statement = f"""
    GRANT SHOW DATABASES ON {database.name}.* TO {bi_user.name}
    """

    await client.query(
        grant_show_databases_permissions_statement, read_only=False, user_agent="no-tb-bi-management-query"
    )

    grant_show_tables_permissions_statement = f"""
    GRANT SHOW TABLES ON {database.name}.* TO {bi_user.name}
    """

    await client.query(grant_show_tables_permissions_statement, read_only=False, user_agent="no-tb-bi-management-query")

    grant_show_columns_permissions_statement = f"""
    GRANT SHOW COLUMNS ON {database.name}.* TO {bi_user.name}
    """

    await client.query(
        grant_show_columns_permissions_statement, read_only=False, user_agent="no-tb-bi-management-query"
    )


async def drop_existing_resources(client: HTTPClient, database_name: str, bi_user: CHBIConnectorUser):
    # TODO: We might want to revoke all privileges for dropped users at some point
    # await client.query(f'REVOKE ALL PRIVILEGES ON *.* FROM {bi_user.name}')
    await client.query(f"DROP DATABASE IF EXISTS {database_name}", read_only=False)
    await client.query(f"DROP USER IF EXISTS {bi_user.name}", read_only=False)
