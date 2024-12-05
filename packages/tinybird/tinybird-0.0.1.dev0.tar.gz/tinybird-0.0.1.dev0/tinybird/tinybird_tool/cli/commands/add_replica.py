import asyncio
import logging
import sys

import click
from humanfriendly.tables import format_smart_table

from tinybird.user_tables import check_missing_tables

from ... import common
from ..cli_base import cli
from ..helpers import get_workspaces_data, recreate_workspace_internal
from .clickhouse_provisioning import provision_cluster


@cli.command()
@click.argument("cluster")
@click.argument("current_replica")
@click.argument("new_replica")
@click.option("--name-needle", default=None, help="Filter workspaces by name needle")
@click.option("--dry-run", is_flag=True)
@click.option("--include-deleted", is_flag=True)
@click.option("--wait-for-replication", is_flag=True)
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
def add_replica(
    cluster: str,
    current_replica: str,
    new_replica: str,
    name_needle: str | None,
    dry_run: bool,
    include_deleted: bool,
    wait_for_replication: bool,
    config: click.Path | None,
) -> None:
    """Provision a new replica

    This command will create all the workspaces currently existing on the cluster CLUSTER
    on a new replica (NEW_REPLICA). CURRENT_REPLICA is a Hostname/IP of an active replica
    of the cluster, to be used to fetch the table metadata.
    """
    logging.basicConfig(level=logging.INFO)
    common.setup_redis_client(config=config)

    found_workspaces = get_workspaces_data(None, name_needle, cluster, include_deleted)

    if not found_workspaces:
        click.secho("No workspaces to replicate", fg="yellow")
        sys.exit(1)

    column_names = [
        "name",
        "id",
        "cluster",
        "database",
        "database_server",
        "datasources",
        "linkers",
        "BI Connector",
        "origin",
        "releases",
        "deleted",
    ]
    click.secho("\nList of the workspaces in the target cluster", bold=True)
    click.echo(format_smart_table(found_workspaces, column_names=column_names))

    if not click.confirm(f"Recreate the workspaces from {current_replica} to {new_replica}?"):
        click.secho("Skipping the creation of the new replica", fg="yellow")
        sys.exit(1)

    ws_creation_arguments = {
        "orig_host": current_replica,
        "dest_host": new_replica,
        "create_tables": True,
        "create_materialized_views": False,
        "ignore_existing_tables": True,
        "ignore_missing_resources": True,
        "workers": 4,
        "dry_run": dry_run,
        "debug": False,
        "skip_wait_for_replication": not wait_for_replication,
        "storage_policy": None,
    }

    click.secho("Creating tables on all the workspaces, skipping materialized views", bold=True)
    for ws in found_workspaces:
        ws_creation_arguments["workspace_id"] = ws.id
        recreate_workspace_internal(**ws_creation_arguments)

    ws_creation_arguments["create_tables"] = False
    ws_creation_arguments["create_materialized_views"] = True

    click.secho("Creating only materialized views on all the workspaces", bold=True)
    for ws in found_workspaces:
        ws_creation_arguments["workspace_id"] = ws.id
        recreate_workspace_internal(**ws_creation_arguments)

    click.secho("Running provisioning for the new replica", bold=True)
    provision_cluster(host=new_replica, cluster=cluster, config=config, dry_run=dry_run)

    click.secho(
        "Checking all metadata exists in the new replica. Internal not checked due to legacy missing quarantine",
        bold=True,
    )

    response = asyncio.run(check_missing_tables(new_replica, cluster))
    if not response.stats:
        click.secho(f"Error getting data for replica: {new_replica}. Checked {response.stats}", fg="red")
    else:
        if not response.tables:
            click.secho(
                f"No missing tables found in {cluster} for replica: {new_replica}. Checked {response.stats}", fg="green"
            )
        else:
            click.secho(
                f"Found {len(response.tables)} missing tables in {cluster} for replica: {new_replica}. Checked {response.stats}",
                fg="red",
            )
            headers = ["Database", "Table id", "Num replicas exists"]
            click.secho(format_smart_table(response.tables, column_names=headers))
            click.secho(
                f"Re-run command or use another replica, seems that are {len(response.tables)} tables missing in {current_replica}. If exists in 0 replicas maybe you can ignore it",
                fg="red",
            )
