import click
from humanfriendly.tables import format_smart_table

from tinybird.user import User as Workspace

from ... import common
from ..cli_base import cli


@cli.group()
def gatherer():
    """Tinybird commands related to gatherer"""
    pass


@gatherer.command(name="list")
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
@click.option("--enabled/--disabled", default=False, help="List workspace with Gatherer disabled or enabled")
@click.option("--branch", is_flag=True, default=False, help="Include branches")
@click.option("--workspace_id", default=None, help="Filter by id")
def list_workspaces(config, enabled: bool, branch: bool, workspace_id: str):
    common.setup_redis_client(config)
    workspaces = Workspace.get_all(include_branches=branch, include_releases=False)
    workspaces_found = filter(lambda ws: ws.is_active and ws.use_gatherer == enabled, workspaces)

    if workspace_id:
        workspaces_found = filter(lambda ws: ws.id == workspace_id, workspaces_found)

    column_names = ["name", "id", "cluster", "database", "branch", "gatherer", "allow fallback", "allow s3 backups"]

    click.echo(f"Workspaces with gatherer => {'enabled' if enabled else 'disabled'}")

    click.echo(
        format_smart_table(
            [
                (
                    x.name,
                    x.id,
                    x.cluster,
                    x.database,
                    x.is_branch,
                    x.use_gatherer,
                    x.allow_gatherer_fallback,
                    x.gatherer_allow_s3_backup_on_user_errors,
                )
                for x in workspaces_found
            ],
            column_names=column_names,
        )
    )


@gatherer.command(name="update")
@click.argument("workspace_id")
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
@click.option(
    "--enable/--disable",
    default=None,
    help="Enable or disable. By default should be enabledSkip if dont want to change",
)
@click.option(
    "--allow-fallback/--no-fallback",
    default=None,
    help="Allow fallback. By default should be disabled. Skip if dont want to change",
)
@click.option(
    "--backup-on-errors/--no-backup-on-errors",
    default=None,
    help="Backup to s3 on errors. By default should be enabled. Skip if dont want to change",
)
def update_workspace(workspace_id: str, config, enable: bool, allow_fallback: bool, backup_on_errors: bool):
    common.setup_redis_client(config)
    workspace = Workspace.get_by_id(workspace_id)

    with Workspace.transaction(workspace_id) as w:
        if enable is not None:
            w.use_gatherer = enable
        if allow_fallback is not None:
            w.allow_gatherer_fallback = allow_fallback
        if backup_on_errors is not None:
            w.gatherer_allow_s3_backup_on_user_errors = backup_on_errors

    workspace = Workspace.get_by_id(workspace_id)

    column_names = ["name", "id", "cluster", "database", "branch", "gatherer", "allow fallback", "allow s3 backups"]

    click.echo(
        format_smart_table(
            [
                (
                    x.name,
                    x.id,
                    x.cluster,
                    x.database,
                    x.is_branch,
                    x.use_gatherer,
                    x.allow_gatherer_fallback,
                    x.gatherer_allow_s3_backup_on_user_errors,
                )
                for x in [workspace]
            ],
            column_names=column_names,
        )
    )
