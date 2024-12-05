import logging
import pickle

import click

from tinybird.ch import HTTPClient
from tinybird.constants import CHCluster
from tinybird.default_tables import DEFAULT_TABLES
from tinybird.feature_flags import FeatureFlagWorkspaces
from tinybird.internal_resources import init_internal_tables
from tinybird.token_scope import scopes
from tinybird.user import User as Workspace
from tinybird.user import UserAccount, Users, public

from ... import common
from ..cli_base import cli


@cli.command()
@click.option("--output-dir", default="users-backup", type=click.Path(exists=True))
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
def backup_users(output_dir, config):
    _, redis_client = common.setup_redis_client(config)

    def safe_model(namespace):
        keys = []
        for k in redis_client.scan_iter(f"{namespace}:*"):
            parts = k.decode().split(":")
            if len(parts) == 2:
                keys.append(k.decode())
        models = redis_client.mget(keys)
        for b in models:
            try:
                model = pickle.loads(b)
                with open(f"{output_dir}/{namespace}_{model['id']}.db", "wb") as w:
                    w.write(b)
                print(f"Performed backup for model: {namespace} id: {model['id']}")
            except Exception as e:
                print(f"Could not dump user from Redis: {e}")

    safe_model("users")
    safe_model("user_accounts")
    safe_model("user_workspace_relationship")


@cli.command()
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
@click.option("--clickhouse-cluster", default="tinybird", help="The ClickHouse cluster to set for the internal user.")
@click.option("--clickhouse-server", default=None)
@click.option("--database-name", default=None)
def create_internal_user(
    config: click.Path, clickhouse_cluster: str, clickhouse_server: str | None, database_name: str | None
) -> None:
    """Create or update internal tables and views"""
    logging.basicConfig(level=logging.INFO)
    common.setup_redis_client(config)

    if database_name:
        public.INTERNAL_USER_DATABASE = database_name

    database_server = clickhouse_server if clickhouse_server is not None else Workspace.default_database_server
    cluster = CHCluster(name=clickhouse_cluster, server_url=database_server)

    common.run_until_complete(
        init_internal_tables(
            DEFAULT_TABLES, clickhouse_cluster=cluster, read_only=False, job_executor=None, populate_views=False
        )
    )


@cli.command()
@click.argument("email")
@click.argument("password")
@click.argument("name")
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
@click.option("--database", default=None)
@click.option("--database-host", default=None)
@click.option("--activate", default=False)
@click.option("--cluster", default=None)
@click.option("--storage-policy", default=None)
@click.option("--plan", default=None)
def register_user(email, password, name, config, database, database_host, activate, cluster, storage_policy, plan):
    """Creates a new user"""
    common.setup_redis_client(config)

    u = UserAccount.register(email, password)
    database_server = database_host if database_host is not None else Workspace.default_database_server
    workspace = Workspace.register(name=name, admin=u.id, cluster=CHCluster(name=cluster, server_url=database_server))

    if database_host:
        workspace["database_server"] = database_host
    client = HTTPClient(workspace["database_server"], database=None)
    cluster_sql = ""
    if cluster:
        workspace.clusters = [cluster]
        cluster_sql = f"ON CLUSTER {cluster}"
    client.query_sync(f"create database {(database or workspace['database'])} {cluster_sql}", read_only=False)
    if database:
        workspace["database"] = database
    if activate:
        workspace.confirmed_account = True
    if storage_policy and storage_policy != "default":
        workspace.storage_policies = {storage_policy: 0}
        workspace.feature_flags[FeatureFlagWorkspaces.ENABLE_STORAGE_POLICY.value] = True
    if plan:
        workspace.plan = plan

    workspace.save()

    print("created user, id: %s" % workspace["id"])
    print("created user, database: %s" % workspace["database"])
    print("admin token: %s" % Users.get_token_for_scope(workspace, scopes.ADMIN_USER))
    print("auth token: %s" % UserAccount.get_token_for_scope(u, scopes.AUTH))
