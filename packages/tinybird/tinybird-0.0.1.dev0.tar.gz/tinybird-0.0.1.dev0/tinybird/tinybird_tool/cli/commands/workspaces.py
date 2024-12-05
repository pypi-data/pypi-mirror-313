import asyncio
import operator
import sys
from dataclasses import fields
from pathlib import Path
from typing import Optional

import click
from humanfriendly.tables import format_smart_table

from tinybird.job import JobExecutor
from tinybird.organization.organization import Organization, Organizations
from tinybird.organization.organization_service import OrganizationService
from tinybird.user import User as Workspace
from tinybird.user import UserAccount

from ... import common
from ..cli_base import cli
from ..helpers import WorkspaceData, get_workspaces_data, recreate_workspace_internal


@cli.group()
def workspaces():
    """Tinybird command to manage workspaces"""
    pass


@workspaces.command(name="list")
@click.option("--email_needle", default=None)
@click.option("--name_needle", default=None, help="Filter workspaces by name needle")
@click.option("--cluster", default=None)
@click.option(
    "-o", "--output", type=click.Choice(["pretty", "tsv"], case_sensitive=False), help="TSV is useful for Spreadsheets"
)
@click.option("--sql-where", is_flag=True, help="Useful when having to use output in SQL queries")
@click.option("--include-deleted", is_flag=True)
@click.option("--only-branches", is_flag=True)
@click.option("--only-releases", is_flag=True)
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
def list_workspaces(
    email_needle, name_needle, cluster, output, sql_where, include_deleted, only_branches, only_releases, config
):
    """List workspaces matching an email needle"""
    common.setup_redis_client(config)
    found_workspaces = get_workspaces_data(
        email_needle, name_needle, cluster, include_deleted, only_branches, only_releases
    )

    column_names = [f.name for f in fields(WorkspaceData)]
    if output == "tsv":
        print("\t".join(["email_needle"] + column_names[:4]))
        for ws in found_workspaces:
            print("\t".join([str(v) for v in [email_needle, *[ws.name, ws.id, ws.cluster, ws.database]]]))
    else:
        click.echo(format_smart_table(found_workspaces, column_names=column_names))

    if sql_where:
        click.secho("SQL WHERE clauses", bg="blue", fg="white")
        column_names = ["name", "id", "database_server", "database"]

        def sql_in(values):
            return ", ".join([f"'{v}'" for v in list(set(values))])

        for c in column_names:
            click.echo(f"{c} IN ({sql_in([ws.__dict__[c] for ws in found_workspaces])})")


@workspaces.command(name="recreate")
@click.argument("orig_host")
@click.argument("dest_host")
@click.argument("workspace_id")
@click.option("--create-tables/--no-create-tables", is_flag=True, default=True)
@click.option("--create-materialized-views/--no-create-materialized-views", is_flag=True, default=True)
@click.option("--ignore-existing-tables", is_flag=True, default=False)
@click.option("--ignore-missing-resources", is_flag=True, default=False)
@click.option("--workers", type=int, default=4)
@click.option("--dry-run", is_flag=True, default=False)
@click.option("--debug", is_flag=True, default=False)
@click.option("--skip-wait-for-replication", is_flag=True, default=False)
@click.option("--storage-policy", default=None)
@click.option("--remove-storage-policy", is_flag=True, default=False)
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
def recreate_workspace(
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
    remove_storage_policy,
    config,
):
    """Recreate a workspace in another server"""
    common.setup_redis_client(config)

    if storage_policy is not None and remove_storage_policy:
        click.secho("Cannot set a storage_policy and remove it at the same time")
        sys.exit(1)

    try:
        workspace = Workspace.get_by_id(workspace_id)
    except Exception:
        click.secho(f"Workspace with id '{workspace_id}' not found", fg="red")
        sys.exit(1)

    if not click.confirm(f"Recreate database for workspace='{workspace.id}', name='{workspace.name}'?"):
        click.secho(f"Skipping database recreation for id='{workspace.id}', name='{workspace.name}'", fg="yellow")
        sys.exit(1)

    if remove_storage_policy:
        # Setting the storage policy to an empty string removes it
        storage_policy = ""

    recreate_workspace_internal(
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
    )


@workspaces.command(name="hard-delete")
@click.argument("workspace_id")
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
@click.option("--dry-run/--no-dry-run", is_flag=True, default=True)
@click.option("--yes", is_flag=True, default=False)
@click.option("--debug", is_flag=True, default=False)
@common.coro
async def hard_delete_workspace(workspace_id: str, config: click.Path, dry_run: bool, yes: bool, debug: bool) -> None:
    if debug:
        loop = asyncio.get_running_loop()
        loop.set_debug(True)

    """Hard deletes a soft deleted workspace"""
    conf, redis_client = common.setup_redis_client(config)
    redis_config = common.get_redis_config(conf)
    common.setup_connectors_config(conf)

    job_executor = JobExecutor(
        redis_client=redis_client,
        redis_config=redis_config,
    )

    log_prefix = "[DRY RUN] " if dry_run else ""

    w: Optional[Workspace] = Workspace.get_by_id(workspace_id)
    if not w:
        click.secho(f"{log_prefix}Workspace with id '{workspace_id}' not found", fg="red")
        return

    if not w.deleted:
        click.secho(
            (
                f"{log_prefix}Workspace with id '{workspace_id}' was not previously deleted by a user. This script is just for"
                " hard deleting user deleted workspaces."
            ),
            fg="red",
        )
        return

    if w.is_release:
        click.secho(
            f"{log_prefix}Workspace with id '{workspace_id}' is a release. Releases cannot be hard deleted directly.",
            fg="red",
        )
        return

    try:
        info = w.get_workspace_info()
        owner = UserAccount.get_by_id(info["owner"])
        if dry_run:
            click.secho(f"[DRY RUN] Skip workspace {w.name} deletion", fg="cyan")
            return

        if yes or click.confirm(f"DELETE {w.name}? (It cannot be undone)"):
            await UserAccount.delete_workspace(owner, w, hard_delete=True, job_executor=job_executor, track_log=False)
            deleted_workspace = Workspace.get_by_id(w.id)
            if not dry_run and deleted_workspace:
                click.secho(f"[ERROR]: {w.id}/{w.name} => Workspace was not deleted", fg="red")
            else:
                click.secho(f"{log_prefix}{w.id}/{w.name} deleted!", fg="green")
    except Exception as e:
        click.secho(f"[ERROR]: {w.name} => {str(e)}", fg="red")


@workspaces.command(name="prune-deleted")
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
@click.option("--dry-run/--no-dry-run", is_flag=True, default=True)
@click.option("--batch", default=5)
@click.option("--yes", is_flag=True, default=False)
@click.option("--debug", is_flag=True, default=False)
@common.coro
async def hard_delete_soft_deleted_workspaces_after_safety_time(
    config: click.Path, dry_run: bool, batch: int, yes: bool, debug: bool
) -> None:
    if debug:
        loop = asyncio.get_running_loop()
        loop.set_debug(True)

    """Hard deletes ALL soft deleted workspaces"""
    conf, redis_client = common.setup_redis_client(config)
    redis_config = common.get_redis_config(conf)
    common.setup_connectors_config(conf)

    job_executor = JobExecutor(
        redis_client=redis_client,
        redis_config=redis_config,
    )

    ws_to_remove = Workspace.get_soft_deleted_workspaces_for_hard_deletion()
    log_prefix = "[DRY RUN] " if dry_run else ""

    if not ws_to_remove:
        click.secho(log_prefix + "No Workspaces to be removed found", fg="green")
        return

    ws_to_remove = sorted(ws_to_remove, key=operator.itemgetter("deleted_date"))
    column_names = ["name", "id", "database", "datasources", "pipes", "deleted_date"]
    column_content = []
    total_datasources = 0
    total_pipes = 0

    for ws in ws_to_remove:
        total_datasources += len(ws.get_datasources())
        total_pipes += len(ws.get_pipes())

        column_content.append(
            [
                ws.name,
                ws.id,
                ws.database,
                len(ws.get_datasources()),
                len(ws.get_pipes()),
                ws.deleted_date,
            ]
        )
    click.echo(format_smart_table(column_content, column_names=column_names))
    click.secho(
        log_prefix
        + f"{len(ws_to_remove)} Workspaces with {total_datasources} datasources and {total_pipes} pipes will be removed. The removal batch will contain a max of {batch} workspaces.",
        fg="green",
    )

    start_process = yes or click.confirm(
        log_prefix + f"Do you want to start the hard-delete process for a batch of {batch}?"
    )
    if not start_process:
        click.secho(log_prefix + "Process cancelled", fg="red")
        return

    for w in ws_to_remove:
        if batch == 0:
            return
        try:
            info = w.get_workspace_info()
            owner = UserAccount.get_by_id(info["owner"])
            click.secho(log_prefix + f"Removing {w.id}/{w.name}...", fg="green")
            ws_still_present = None
            if not dry_run:
                await UserAccount.delete_workspace(
                    owner, w, hard_delete=True, job_executor=job_executor, track_log=False
                )
                ws_still_present = Workspace.get_by_id(w.id)

            if ws_still_present:
                click.secho(f"[ERROR]: {w.id}/{w.name} => Workspace was not deleted", fg="red")
            else:
                click.secho(log_prefix + f"{w.id}/{w.name} deleted!", fg="green")
        except Exception as e:
            click.secho(f"[ERROR]: {w.id}/{w.name} => {str(e)}", fg="red")
        finally:
            batch -= 1


@workspaces.command(name="backup")
@click.argument("save_path", type=click.Path(exists=True))
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
@click.option("--workspaces", type=str, help="comma separated list of workspaces IDs")
@click.option("--dry-run", is_flag=True, default=False)
def backup_workspaces_raw_from_redis_to_files(
    save_path: str, config: click.Path, workspaces: str, dry_run: bool
) -> None:
    """Save all the workspaces to files, to be recovered with the restore command later"""
    _, redis_client = common.setup_redis_client(config)

    workspaces_list = (
        Workspace.get_all(include_branches=True, include_releases=True)
        if not workspaces
        else [Workspace.get_by_id(w) for w in workspaces.split(",")]
    )

    for ws in workspaces_list:
        workspace_redis_key = f"{Workspace.__namespace__}:{ws.id}"
        file_path = Path(save_path).joinpath(f"{ws.id}.backup")

        click.secho(
            f"{'[DRY_RUN] ' if dry_run else ''}Writting backup from Redis key: '{workspace_redis_key}' to file '{file_path}'."
        )

        content = redis_client.get(workspace_redis_key)
        if not dry_run:
            with open(file_path, "wb") as file:
                file.write(content)


@workspaces.command(name="restore")
@click.argument("folder_with_data", type=click.Path(exists=True))
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
@click.option("--workspaces", type=str, help="comma separated list of workspaces IDs")
@click.option("--dry-run", is_flag=True, default=False)
def restore_workspaces_raw_from_files_to_redis(
    folder_with_data: str, config: click.Path, workspaces: str, dry_run: bool
) -> None:
    """Restore all the workspaces from a backup"""
    _, redis_client = common.setup_redis_client(config)

    workspaces_list = (
        Workspace.get_all(include_branches=True, include_releases=True)
        if not workspaces
        else [Workspace.get_by_id(w) for w in workspaces.split(",")]
    )

    for ws in workspaces_list:
        file_path = Path(folder_with_data).joinpath(f"{ws.id}.backup")
        workspace_redis_key = f"{Workspace.__namespace__}:{ws.id}"
        click.secho(
            f"{'[DRY_RUN] ' if dry_run else ''}Writting backup from file '{file_path}' to Redis key: '{workspace_redis_key}'."
        )

        with open(file_path, "rb") as file:
            content = file.read()

        if not dry_run:
            redis_client.set(workspace_redis_key, content)
            # Do a fake transaction to force a cleanup of the internal server's caches
            with Workspace.transaction(ws.id):
                pass
            click.secho(f"Workspace '{workspace_redis_key}' restored.")


@workspaces.command(name="add-to-organization")
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
@click.option("--organization-ids", type=str, help="The IDs of the Organizations we are going to add Workspaces to")
@click.option("--dry-run", is_flag=True, default=False)
def add_workspaces_to_organization(config, organization_ids: str, dry_run: bool):
    """Adds existing Workspaces to an Organization: if a member of the Organization is an admin on a Workspace, it is automatically added to the Organization"""
    common.setup_redis_client(config)
    organizations = set()
    for organization_id in organization_ids.split(","):
        organization = Organization.get_by_id(organization_id)
        if not organization:
            click.secho(f"Organization with id '{organization_id}' not found", fg="red")
        else:
            organizations.add(organization)

    for organization in organizations:
        click.secho(f"Looking for Workspaces to add to Organization '{organization.name}'", bold=True)

        workspaces = asyncio.run(OrganizationService.get_existing_workspaces_outside_organization(organization))
        added_workspaces = False

        for workspace in workspaces:
            if dry_run:
                click.secho(
                    f"Would add Workspace '{workspace.name}' with plan {workspace.plan} to Organization '{organization.name}'",
                    fg="blue",
                )
                continue

            try:
                organization = Organizations.add_workspace(organization, workspace)
            except Exception as e:
                click.secho(
                    f"Error adding Workspace '{workspace.name}' to Organization '{organization.name}': {e}",
                    fg="red",
                )
                continue
            click.secho(
                f"Added Workspace '{workspace.name}' with plan {workspace.plan} to Organization '{organization.name}'",
                fg="green",
            )
            added_workspaces = True

        if not added_workspaces:
            click.secho(f"No Workspaces added to Organization '{organization.name}'", fg="blue")


@workspaces.command(name="fix-database-servers")
@click.option("--email_needle", default=None)
@click.option("--name_needle", default=None, help="Filter workspaces by name needle")
@click.option("--cluster", default=None)
@click.option("--include-deleted", is_flag=True)
@click.option("--only-branches", is_flag=True)
@click.option("--only-releases", is_flag=True)
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
@click.option("--dry-run/--no-dry-run", is_flag=True, default=True)
def fix_database_servers(
    email_needle, name_needle, cluster, include_deleted, only_branches, only_releases, config, dry_run
):
    """Fix the database servers, changing _ with - on all of them"""
    common.setup_redis_client(config)
    found_workspaces = get_workspaces_data(
        email_needle, name_needle, cluster, include_deleted, only_branches, only_releases
    )

    # We are only interested in workspaces with a database server with _
    workspaces_to_update = [ws for ws in found_workspaces if "_" in ws.database_server]

    if len(workspaces_to_update) == 0:
        click.secho("All clean, no workspaces found with a wrong database server")
        return

    click.secho(f"Found {len(workspaces_to_update)} that will be updated")
    column_names = ["name", "cluster", "database_server", "datasources", "deleted"]
    workspaces_table = [
        [ws.name, ws.cluster, ws.database_server, ws.datasources, ws.deleted] for ws in workspaces_to_update
    ]
    click.echo(format_smart_table(workspaces_table, column_names=column_names))

    for ws in workspaces_to_update:
        server_with_dash = ws.database_server.replace("_", "-")
        log_prefix = "[DRY RUN] " if dry_run else ""
        click.secho(f"{log_prefix}Changing {ws.name} server to {server_with_dash}")
        if dry_run:
            continue
        with Workspace.transaction(ws.id) as changed_ws:
            changed_ws["database_server"] = server_with_dash
