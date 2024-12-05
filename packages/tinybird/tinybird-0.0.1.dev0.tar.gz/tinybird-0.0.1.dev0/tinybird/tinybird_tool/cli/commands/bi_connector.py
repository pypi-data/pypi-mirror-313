import logging

import click

from tinybird.pg import PGService
from tinybird.user import User as Workspace
from tinybird.user import Users

from ... import common
from ..cli_base import cli

logger = logging.getLogger("tinybird_tool.bi_connector")


@cli.command()
@click.option("--dry-run", is_flag=True, default=False)
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
@click.option("--workspace", type=str, help="comma separated list of workspaces IDs")
@click.option("--clickhouse-ip", type=str, help="new ClickHouse server IP")
def migrate_bi_connector(dry_run, config, workspace, clickhouse_ip, clickhouse_port=8123):
    if dry_run:
        print("Dry run execution activated")
    common.setup_redis_client(config=config)

    workspaces = [] if not workspace else workspace.split(",")

    for workspace_id in workspaces:
        try:
            ws = Users.get_by_id(workspace_id)
            click.secho(f"Workspace '{ws.id}'", fg="blue")
            pg_service = PGService(ws)
            ws["enabled_pg"] = False
            ws["pg_foreign_server"] = clickhouse_ip
            ws["pg_foreign_server_port"] = clickhouse_port

            if dry_run:
                click.secho(f"[DRY RUN] disable postgres feature flag for workspace {ws.name}", fg="blue")
            else:
                ws.save()

            if dry_run:
                click.secho(f"[DRY RUN] change server host to {clickhouse_ip}", fg="blue")
            else:
                pg_service.alter_server(host=clickhouse_ip)

            ws["enabled_pg"] = True
            if dry_run:
                click.secho(f"[DRY RUN] enable postgres feature flag for workspace {ws.name}", fg="blue")
            else:
                ws.save()

            ds = ws.get_datasources()
            pipes = [pipe for pipe in ws.get_pipes() if pipe.is_published()]
            if dry_run:
                click.secho("[DRY RUN] sync foreign tables", fg="blue")
                for d in ds:
                    click.secho(f"[DRY RUN] sync data source{d.name}", fg="blue")
                for pipe in pipes:
                    click.secho(f"[DRY RUN] sync endpoint {pipe.name}", fg="blue")
            else:
                click.secho("syncing foreign tables", fg="blue")
                common.run_until_complete(pg_service.sync_foreign_tables_async(datasources=ds, pipes=pipes))
                click.secho("done", fg="blue")
        except Exception as e:
            click.secho(str(e))


@cli.command()
@click.option("--dry-run", is_flag=True, default=False)
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
@click.option(
    "--workspaces", type=str, default="", help="comma separated list of workspaces IDs. default is all workspaces"
)
@click.option("--pg-connector-ip", type=str, help="new Postgres server IP")
@click.option("-y", "--yes", "confirm", is_flag=True, default=False, help="skip confirmation")
def migrate_pg_connector(
    dry_run: bool, config: click.Path, workspaces: str, confirm: bool, pg_connector_ip: str
) -> None:
    _migrate_pg_connector(dry_run, config, workspaces, confirm, pg_connector_ip)


def _migrate_pg_connector(
    dry_run: bool, config: click.Path, workspaces: str, confirm: bool, pg_connector_ip: str
) -> None:
    if dry_run:
        click.secho("Dry run execution activated")
    common.setup_redis_client(config=config)

    ws_ids = [ws_id.strip() for ws_id in workspaces.split(",") if ws_id.strip()]
    if len(ws_ids) == 0:
        confirm_message = "Performing operation on all workspaces. Do you want to continue?"
        confirm = confirm or dry_run or click.confirm(confirm_message, abort=True)

    workspaces_iter = Workspace._get_by_keys(ws_ids) if ws_ids else Workspace.get_all(True, True)

    for workspace in workspaces_iter:
        click.secho(f"Workspace '{workspace.id}'", fg="blue")
        if dry_run:
            old_ip = workspace["pg_server"]
            message = f"[DRY RUN] update worskpace {workspace.id} pg server from {old_ip} to {pg_connector_ip}"
            click.secho(message)
            continue
        update_workspace_pg_connector(workspace, pg_connector_ip)


def update_workspace_pg_connector(workspace: Workspace, pg_connector_ip: str) -> None:
    try:
        # skip deleted workspaces
        if workspace.deleted:
            logger.info(f"Skipping workspace {workspace.id} because it is deleted")
            return

        # update the workspace pg connector ip
        Users.set_attribute(workspace.id, "pg_server", pg_connector_ip)
        logger.info(f"Updated workspace {workspace.id} pg connector to {pg_connector_ip}")

        # and rebuild tables in the new pg connector
        pg_service = PGService(workspace)
        common.run_until_complete(pg_service.sync_foreign_tables_async())
        logger.info(f"Rebuilt tables in pg connector for workspace {workspace.id}")
    except Exception as e:
        logger.exception(f"Error updating workspace {workspace.id} pg connector: {e}")
