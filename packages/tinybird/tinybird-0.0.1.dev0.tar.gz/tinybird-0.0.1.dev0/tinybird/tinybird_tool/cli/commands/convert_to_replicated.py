import json
import sys

import click
from humanfriendly.tables import format_pretty_table

from tinybird.ch import HTTPClient
from tinybird.ch_utils.engine import engine_local_to_replicated

from ..cli_base import cli
from ..helpers import (
    SUFFIX_TABLE_CONVERTED_TO_REPLICATED,
    is_already_converted_to_replicated,
    is_mergetree,
    is_replicated,
)


@cli.command()
@click.argument("database_server")
@click.argument("database")
@click.option("-t", "--table", "selected_tables", multiple=True)
@click.option("--dry-run", is_flag=True, default=False)
@click.option("--debug", is_flag=True, default=False)
def convert_to_replicated(database_server, database, selected_tables, dry_run, debug):
    """Convert all MergeTree tables into ReplicatedMergeTree"""

    def run_query(sql, force_run=False, **kwargs):
        if debug:
            click.secho(f"    > Query: {sql}")
        if dry_run and not force_run:
            click.secho(f'    - [DRY RUN] Skipping query: "{sql}"', fg="cyan")
            return {}
        extra_params = {"max_execution_time": 7200, "max_result_bytes": 0, **kwargs}
        client = HTTPClient(database_server, database=database)
        try:
            headers, body = client.query_sync(sql, read_only=False, **extra_params)
            if "application/json" in headers["content-type"]:
                return json.loads(body)
            return body
        except Exception as e:
            click.secho(f' - [ERROR] Failed to run query: "{sql}"\nReason={e}', fg="red")
            click.confirm("Do you want to continue?", abort=True)

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

    tables = run_query(tables_query, force_run=True).get("data", [])

    def is_selected(t):
        return not selected_tables or t["name"] in selected_tables

    tables_to_convert = []
    for t in tables:
        if is_selected(t) and is_mergetree(t) and not is_replicated(t) and not is_already_converted_to_replicated(t):
            tables_to_convert.append(t)

    def echo_section(title, **kwargs):
        click.secho(f" {title:79}", **kwargs)

    column_names = ["name", "engine"]
    echo_section(f"All tables found at database='{database}'", bg="magenta", fg="white")
    click.echo(format_pretty_table([[t["name"], t["engine"]] for t in tables], column_names=column_names))

    if not tables_to_convert:
        echo_section("There are non replicated MergeTree tables to convert", bg="green", fg="white")
        sys.exit(0)

    echo_section("Tables to convert from MergeTree to ReplicatedMergeTree", bg="blue", fg="white")
    click.echo(format_pretty_table([[t["name"], t["engine"]] for t in tables_to_convert], column_names=column_names))

    echo_section("Warning", bg="red", fg="white")
    click.echo(" - BEWARE, this procedure incurs in some downtime.")
    click.echo(" - This script will convert all MergeTree engine tables list above to ReplicatedMergeTree versions.")
    click.echo(
        " - It will rename table names, detach their data, create new tables and attach the data from the renamed"
        " tables into the new tables."
    )
    click.echo(
        " - You can read more about this procedure at"
        " https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/replication/#converting-from-mergetree-to-replicatedmergetree."
    )

    if not click.confirm("Do you want to continue?"):
        click.secho(
            f"Skipping converting from MergeTree to ReplicatedMergeTree for database='{database}'.", fg="yellow"
        )
        sys.exit(1)

    def table_names(t):
        target_table = t["name"]
        old_mergetree_table = f"{target_table}{SUFFIX_TABLE_CONVERTED_TO_REPLICATED}"
        return target_table, old_mergetree_table

    echo_section("Important", bg="yellow")
    click.echo(
        " - Initially, the attached partitions don't take extra disk space as they are mere hard links. However, as the"
        " tables get new data or new merges happen, the old files will be relevant in terms of disk usage."
    )
    click.echo(" - This script does not take care of removing the now old MergeTree tables.")
    click.echo(" - If something goes wrong, you can always revert to use the old tables with the following queries:")

    click.echo("=" * 79)
    for t in tables_to_convert:
        target_table, old_mergetree_table = table_names(t)
        click.echo(
            f"RENAME TABLE `{database}`.`{target_table}` TO `{database}`.`{target_table}__replicated_broken`,"
            f" `{database}`.`{old_mergetree_table}` TO `{database}`.`{target_table}`;"
        )
    click.echo("=" * 79)

    for t in tables_to_convert:
        click.echo("")
        target_table, old_mergetree_table = table_names(t)
        echo_section(f"Migrating table='{target_table}'", bg="green", fg="white")

        click.echo(f"1. Renaming current table from {target_table} to {old_mergetree_table}")
        run_query(f"RENAME TABLE `{database}`.`{target_table}` TO `{database}`.`{old_mergetree_table}`")

        click.echo(f"2. Stopping merges at table {old_mergetree_table}")
        run_query(f"SYSTEM STOP MERGES `{database}`.`{old_mergetree_table}`")

        click.echo(f"3. Creating new table='{target_table}' with ReplicatedMergeTree engine")
        replicated_engine = engine_local_to_replicated(t["engine_full"], database, target_table)
        create_table_query = t["create_table_query"].replace(t["engine_full"], replicated_engine)
        run_query(create_table_query)

        click.echo("4. Retrieving all partitions from the original table")
        partitions_query = f"""SELECT
            DISTINCT partition_id
        FROM
            system.parts
        WHERE
            database = '{database}'
            AND table = '{target_table if dry_run else old_mergetree_table}'
        FORMAT JSON
        """
        partitions = run_query(partitions_query, force_run=True).get("data", [])
        click.echo(format_pretty_table([[p["partition_id"]] for p in partitions], column_names=["partition_id"]))

        click.echo("5. Attaching all partitions from the MergeTree to the new ReplicatedMergeTree table")
        for p in partitions:
            run_query(
                f"ALTER TABLE `{database}`.`{target_table}` ATTACH PARTITION ID '{p['partition_id']}' FROM"
                f" `{database}`.`{old_mergetree_table}`"
            )

        click.echo(f"6. Restart merges at {old_mergetree_table} just in case we need to go back")
        run_query(f"SYSTEM START MERGES `{database}`.`{old_mergetree_table}`")
