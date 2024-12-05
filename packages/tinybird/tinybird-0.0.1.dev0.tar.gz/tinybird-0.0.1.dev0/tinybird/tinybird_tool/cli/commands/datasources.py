from typing import Any, Dict, List, Union

import click
from humanfriendly.tables import format_pretty_table

from tinybird.ch import ch_table_details_async
from tinybird.datasource import SharedDatasource
from tinybird.syncasync import async_to_sync
from tinybird.user import User as Workspace
from tinybird.user import Users

from ... import common
from ..cli_base import cli


@cli.command()
@click.argument("email_needle")
@click.option(
    "-o", "--output", type=click.Choice(["pretty", "tsv"], case_sensitive=False), help="TSV is useful for Spreadsheets"
)
@click.option("--sql-where", is_flag=True, help="Useful when having to use output in SQL queries")
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
def datasources(email_needle, output, sql_where, config):
    """List datasouces matching an email needle"""
    common.setup_redis_client(config)
    all_workspaces = Workspace.get_all(include_branches=True, include_releases=True)

    matching_workspaces = set()
    for ws in all_workspaces:
        ws_users = ws.get_workspace_users()
        for u in ws_users:
            email = u.get("email", "")
            if email_needle.lower() in email.lower():
                matching_workspaces.add(ws.id)

    found_datasouces: List[List[Union[str | bool]]] = []
    for ws_id in matching_workspaces:
        ws = Workspace.get_by_id(ws_id)
        datasources = ws.get_datasources()

        for ds in datasources:
            found_datasouces.append(
                [
                    ws.name,
                    ws.id,
                    ws.database_server,
                    ws.database,
                    ds.name,
                    ds.id,
                    isinstance(ds, SharedDatasource),
                ]
            )

    found_datasouces = sorted(found_datasouces, key=lambda x: x[0].lower() if isinstance(x[0], str) else x[0])

    column_names = [
        "workspace_name",
        "workspace_id",
        "server",
        "database",
        "datasource_name",
        "datasource_id",
        "is_shared",
    ]

    if output == "tsv":
        print("\t".join(["email_needle"] + column_names[:4]))
        for datasource in found_datasouces:
            print("\t".join([str(v) for v in [email_needle] + datasource[:4]]))
    else:
        click.echo(format_pretty_table(found_datasouces, column_names=column_names))

    if sql_where:
        click.secho("SQL WHERE clauses", bg="blue", fg="white")
        column_names = ["name", "id", "database_server", "database"]

        def sql_in(values):
            return ", ".join([f"'{v}'" for v in list(set(values))])

        for i, c in enumerate(column_names):
            click.echo(f"{c} IN ({sql_in([ws[i] for ws in found_datasouces])})")


@cli.command()
@click.argument("email_needle")
@click.option(
    "-o", "--output", type=click.Choice(["pretty", "tsv"], case_sensitive=False), help="TSV is useful for Spreadsheets"
)
@click.option("--sql-where", is_flag=True, help="Useful when having to use output in SQL queries")
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
def datasources_shared(email_needle, output, sql_where, config):
    """List all the shared datasouces matching an email needle"""
    common.setup_redis_client(config)
    all_workspaces = Workspace.get_all(include_branches=True, include_releases=True)

    matching_workspaces = set()
    for ws in all_workspaces:
        ws_users = ws.get_workspace_users()
        for u in ws_users:
            email = u.get("email", "")
            if email_needle.lower() in email.lower():
                matching_workspaces.add(ws.id)

    found_datasouces = []
    for ws_id in matching_workspaces:
        ws = Workspace.get_by_id(ws_id)
        datasources = ws.get_datasources()

        for ds in datasources:
            for shared_ds in ds.get_shared_with():
                found_datasouces.append(
                    [
                        ws.name,
                        ws.id,
                        ws.database_server,
                        ws.database,
                        ds.name,
                        Workspace.get_by_id(shared_ds).name,
                        shared_ds,
                    ]
                )

    found_datasouces = sorted(found_datasouces, key=lambda x: x[0].lower())

    column_names = [
        "workspace_name",
        "workspace_id",
        "server",
        "database",
        "datasource_name",
        "shared_with",
        "shared_with_id",
    ]

    if output == "tsv":
        print("\t".join(["email_needle"] + column_names[:4]))
        for datasource in found_datasouces:
            print("\t".join([str(v) for v in [email_needle] + datasource[:4]]))
    else:
        click.echo(format_pretty_table(found_datasouces, column_names=column_names))

    if sql_where:
        click.secho("SQL WHERE clauses", bg="blue", fg="white")
        column_names = ["name", "id", "database_server", "database"]

        def sql_in(values):
            return ", ".join([f"'{v}'" for v in list(set(values))])

        for i, c in enumerate(column_names):
            click.echo(f"{c} IN ({sql_in([ws[i] for ws in found_datasouces])})")


@cli.command()
@click.option("--dry-run", is_flag=True, default=False)
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
@click.option("--workspace", type=str, help="comma separated list of workspaces IDs")
@click.option("--force", is_flag=True, default=False, help="force recalc engine")
def update_ds_meta(dry_run, config, workspace, force):
    if dry_run:
        print("Dry run execution activated")
    common.setup_redis_client(config=config)

    users = Workspace.get_all(include_branches=True, include_releases=True)
    workspaces = [] if not workspace else workspace.split(",")

    for user in users:
        try:
            click.secho(f"User '{user.id}'", fg="blue")
            if user.id in workspaces or not workspaces:
                datasources = user.get_datasources()
                click.secho(f"{str(len(datasources))} data sources found", fg="blue")
                for _, datasource in enumerate(datasources):
                    click.secho(f"Data source '{datasource.id}'", fg="blue")
                    if not datasource.engine or force:
                        click.secho("Data source has no engine", fg="blue")
                        if not dry_run:
                            engine = async_to_sync(ch_table_details_async)(
                                datasource.id, user["database_server"], database=user["database"]
                            )
                            click.secho("Got metadata", fg="blue")
                            datasource.engine = engine.to_json(exclude=["engine_full"])
                            Users.update_datasource_sync(user, datasource)
                            click.secho("Saved data source", fg="green")
                        else:
                            click.secho("[DRY RUN] Would get metadata", fg="blue")
                else:
                    click.secho("[DRY RUN] Would save user", fg="blue")
            else:
                click.secho("Discarded", fg="blue")
        except Exception as e:
            click.secho(str(e))


@cli.command()
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
def get_engine_settings(config):
    """Get all the settings being used in data source engines"""
    common.setup_redis_client(config)

    all_engine_settings: Dict[str, Any] = {}

    for workspace in Workspace.get_all(include_branches=True, include_releases=True):
        try:
            datasources = workspace.get_datasources()
            for datasource in datasources:
                settings = datasource.engine.get("settings", None)
                if settings:
                    if workspace.id not in all_engine_settings:
                        all_engine_settings[workspace.id] = {}
                    all_engine_settings[workspace.id][datasource.id] = settings
        except Exception as e:
            import traceback

            traceback.print_exc()
            click.secho(f"** error: {e}")

    click.secho(all_engine_settings)
