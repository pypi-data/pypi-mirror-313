import asyncio
import sys

import click

from tinybird.data_connector import DataConnector
from tinybird.tinybird_tool import common
from tinybird.tinybird_tool.cli.cli_base import cli
from tinybird.user import UserDoesNotExist, Users


@cli.command()
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
@click.option("--dry-run", is_flag=True)
@click.option("--yes", is_flag=True)
def delete_orphan_data_connectors(config, dry_run, yes):
    """Deletes orphan data connectors"""
    common.setup_redis_client(config=config)

    try:
        for data_connector in DataConnector.get_all():
            try:
                if not data_connector.user_id:
                    continue
                Users.get_by_id(data_connector.user_id)
            except UserDoesNotExist:
                if dry_run:
                    click.secho(f"[DRY RUN] Skip data connector {data_connector.id} deletion", fg="cyan")
                    click.secho(data_connector.to_json())
                    continue

                if yes or click.confirm(f"DELETE {data_connector.id}? (It cannot be undone)"):
                    asyncio.run(data_connector.hard_delete())
                    click.secho(f"{data_connector.id} deleted!", fg="green")
    except Exception as e:
        click.secho(f"Unknown exception {str(e)}", fg="red")
        sys.exit(1)
