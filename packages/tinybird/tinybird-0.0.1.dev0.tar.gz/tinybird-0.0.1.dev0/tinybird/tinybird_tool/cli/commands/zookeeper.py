import json
import sys

import click
from humanfriendly.tables import format_pretty_table

from tinybird.ch import HTTPClient

from ..cli_base import cli


@cli.command()
@click.argument("database_server")
@click.option("-t", "--table", "selected_tables", multiple=True)
@click.option("-c", "--cluster", "cluster", default=None)
@click.option("--dry-run", is_flag=True, default=False)
@click.option("--debug", is_flag=True, default=False)
def restore_tables_zookeeper(database_server, selected_tables, cluster, dry_run, debug):
    """Restore tables ZK information on a server"""

    def run_query(sql, force_run=False, **kwargs):
        if debug:
            click.secho(f"    > Query: {sql}")
        if dry_run and not force_run:
            click.secho(f'    - [DRY RUN] Skipping query: "{sql}"', fg="cyan")
            return {}
        extra_params = {"max_execution_time": 7200, "max_result_bytes": 0, **kwargs}
        client = HTTPClient(database_server)
        try:
            headers, body = client.query_sync(sql, read_only=False, **extra_params)
            if "application/json" in headers["content-type"]:
                return json.loads(body)
            return body
        except Exception as e:
            click.secho(f' - [ERROR] Failed to run query: "{sql}"\nReason={e}', fg="red")

    on_cluster = f" ON CLUSTER {cluster} " if cluster else ""

    tables_query = """SELECT
            database,
            table,
            engine
        FROM
            system.replicas
        WHERE engine like 'Replicated%'
        FORMAT JSON"""

    tables = run_query(tables_query, force_run=True).get("data", [])

    def is_selected(t):
        return not selected_tables or t["table"] in selected_tables

    tables_to_restore = list(filter(is_selected, tables))

    def echo_section(title, **kwargs):
        click.secho(f" {title:79}", **kwargs)

    column_names = ["database", "table", "engine"]
    echo_section("All tables found'", bg="magenta", fg="white")
    click.echo(
        format_pretty_table(
            [[t["database"], t["table"], t["engine"]] for t in tables_to_restore], column_names=column_names
        )
    )

    echo_section("Warning", bg="red", fg="white")
    click.echo(" - This script will recreate the tables data in zookeeper.")

    if not click.confirm("Do you want to continue?"):
        click.secho("Skipping recreate tables data in zookeeper.", fg="yellow")
        sys.exit(1)

    for t in tables_to_restore:
        click.echo("")
        echo_section(f"Recreating table='{t}'", bg="green", fg="white")
        run_query(f"SYSTEM RESTORE REPLICA `{t['database']}`.`{t['table']}` {on_cluster}")
