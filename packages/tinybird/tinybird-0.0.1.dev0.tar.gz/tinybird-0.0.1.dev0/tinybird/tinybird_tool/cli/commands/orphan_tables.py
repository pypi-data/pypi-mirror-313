import asyncio
from datetime import datetime

import click
from humanfriendly.tables import format_smart_table
from tabulate import tabulate

from tinybird.ch import ch_drop_table_sync, ch_get_tables_metadata_sync
from tinybird.user_tables import check_missing_tables, get_all_tables

from ... import common
from ..cli_base import cli


@cli.command()
@click.option(
    "--clean",
    is_flag=True,
    default=False,
    help="Removes all orphan tables and materialized views from ClickHouse prior to the last --days days yesterday",
)
@click.option("--days", help="Days since the table was last modified", default=2)
@click.option("--dry-run", is_flag=True, default=False, help="To be used with --clean, will not remove tables")
@click.option(
    "--database",
    help="The database name to check/remove tables. If empty it will look in all databases except system and public",
)
@click.option("--only-materialized", is_flag=True, default=False, help="Only list or drop materialized views")
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
def orphan_tables(clean, days, dry_run, database, only_materialized, config):
    """List and clean (i.e. drop) orphan tables and MVs"""
    common.setup_redis_client(config)
    date_format = "%Y-%m-%d %H:%M:%S"
    users_by_database, users_tables, ch_servers = get_all_tables(only_materialized=only_materialized)
    ch_tables = ch_get_tables_metadata_sync(database_servers=ch_servers, only_materialized=only_materialized)
    unexpected_tables = []

    click.secho("Orphan tables to clean: ")

    for t, (engine, size, mtime, database_server, _count, _cluster) in ch_tables.items():
        try:
            if database and len(t) and database != t[0]:
                continue
            if t[0] in ["public", "system"] or t in users_tables:
                continue

            expected_engine = engine.startswith("Replicated") or engine in ("MaterializedView", "Join", "Null")
            if not t[1].startswith("t_") or not expected_engine:
                unexpected_tables.append([t, engine, size, mtime, database_server])
                continue
            if clean:
                clusters = users_by_database.get(t[0], ["user-deleted", None])[1]
                mdatetime = datetime.strptime(mtime, date_format)
                if (datetime.utcnow() - mdatetime).days >= int(days) or days == 0:
                    if dry_run:
                        click.secho(
                            f" ⚠️  {t[0]}.{t[1]} on database server {database_server} would be dropped", fg="yellow"
                        )
                        continue
                    if not clusters:
                        ch_drop_table_sync(database_server, t[0], t[1], avoid_max_table_size=True, exists_clause=True)
                    else:
                        for cluster in clusters:
                            ch_drop_table_sync(
                                database_server,
                                t[0],
                                t[1],
                                cluster=cluster,
                                avoid_max_table_size=True,
                                exists_clause=True,
                            )
                    click.secho(f" ✅   {t[0]}.{t[1]} on database server {database_server} was dropped", fg="green")
            else:
                click.secho(
                    f"{users_by_database.get(t[0], ['user-deleted'])[0]:24} {mtime:20} {size.replace(' ', ''):8} {engine:32} {f'`{t[0]}`.`{t[1]}`'}"
                )
        except Exception as e:
            click.secho(e, fg="red")
    if not clean:
        click.secho("\n Add --clean to remove them. \n")
    if unexpected_tables:
        click.secho(f"\nFound {len(unexpected_tables)} unexpected tables:\n", fg="yellow")
        headers = ["Table name", "Engine", "Size", "Last modified", "Database server"]
        table = tabulate(unexpected_tables, headers=headers)
        click.secho(table, fg="yellow")
        click.secho("\nThese tables cannot be created using Tinybird only and should be reviewed manually", fg="yellow")


@cli.command()
@click.argument("replica")
@click.argument("cluster")
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
def missing_tables_on_replica(replica: str, cluster: str, config):
    """List tables and MVs not present in replica"""
    common.setup_redis_client(config)
    response = asyncio.run(check_missing_tables(replica, cluster=cluster))
    if not response.stats:
        click.secho(f"Error getting data for replica: {replica}. Checked {response.stats}", fg="red")
    else:
        if not response.tables:
            click.secho(
                f"No missing tables in {cluster} found for replica: {replica}. Checked {response.stats}", fg="green"
            )
        else:
            click.secho(
                f"Found {len(response.tables)} missing tables in {cluster} for replica: {replica}. Checked {response.stats}",
                fg="red",
            )
            headers = ["Database", "Table id", "Num replicas exists"]
            click.secho(format_smart_table(response.tables, column_names=headers))
