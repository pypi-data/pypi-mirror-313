import logging

import click

from tinybird.default_tables import (
    DEFAULT_METRICS_CLUSTER_TABLES,
    DEFAULT_METRICS_CLUSTER_VIEWS,
    DEFAULT_METRICS_TABLES,
    DEFAULT_METRICS_VIEWS,
)
from tinybird.internal_resources import init_metrics_tables
from tinybird.tinybird_tool.metrics import check_metrics_tables, fix_metrics_on_host
from tinybird.user import public

from ... import common
from ..cli_base import cli


@cli.command()
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
@click.option("--database-name", default="default")
@click.option("--dry-run", is_flag=True, default=False)
def init_metrics_cluster_and_internal(config: click.Path, database_name: str, dry_run=False) -> None:
    """Init metrics cluster infrastructure

    This command provision all the tinybird metrics infrastructure, which means creating tables
    and views in the metrics cluster and distributed tables and views on the internal cluster.
    """
    logging.basicConfig(level=logging.INFO)
    conf, _ = common.setup_redis_client(config)
    metrics_cluster = conf.get("metrics_cluster", None)
    metrics_database_server = conf.get("metrics_database_server", None)

    common.run_until_complete(
        init_metrics_tables(
            host=public.get_public_user().database_server,
            metrics_cluster=metrics_cluster,
            metrics_database=database_name,
            metrics_database_server=metrics_database_server,
            metrics_cluster_tables=DEFAULT_METRICS_CLUSTER_TABLES,
            metrics_cluster_views=DEFAULT_METRICS_CLUSTER_VIEWS,
            metrics_tables=DEFAULT_METRICS_TABLES,
            metrics_views=DEFAULT_METRICS_VIEWS,
            add_datasources=True,
            dry_run=dry_run,
        )
    )


@cli.command(name="fix-metrics-in-host")
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
@click.option("--host", type=str)
@click.option("--tables", type=str, help='Comma separated list of "distributed_" tables to fix')
@click.option("--metrics-database", type=str, default="default")
@click.option("--exchange-tables", is_flag=True, default=False)
@click.option("--copy-data", is_flag=True, default=False)
@click.option("--dry-run", is_flag=True, default=False)
def fix_metrics_in_host_command(
    config: click.Path,
    host: str,
    tables: str,
    metrics_database: str,
    exchange_tables: bool = False,
    copy_data: bool = False,
    dry_run: bool = False,
) -> None:
    logging.basicConfig(level=logging.INFO)
    conf, _ = common.setup_redis_client(config)

    if not host:
        logging.info(f"Missing host: {host}")
        return

    table_list: list[str] = tables.split(",")
    if not table_list:
        logging.info("Missing tables")
        return

    common.run_until_complete(
        fix_metrics_on_host(
            conf=conf,
            host=host,
            tables=table_list,
            metrics_database=metrics_database,
            exchange_tables=exchange_tables,
            copy_data=copy_data,
            dry_run=dry_run,
        )
    )


@cli.command(name="check-metrics-tables")
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
@click.option(
    "--check-host",
    type=str,
    help="Hostname for internal instance (if empty, uses the `internal_database_server` key in `pro.py`).",
)
@click.option(
    "--check-clusters",
    type=str,
    help="Comma separated list of clusters to check (all reachable clusters if not specified).",
)
@click.option("--verbose", is_flag=True, default=False, help="Show extra information during the process.")
@click.option("--ignore-data-clusters", is_flag=True, default=False, help="Ignore checks in data clusters.")
@click.option("--ignore-metrics-cluster", is_flag=True, default=False, help="Ignore checks in the metrics cluster.")
@click.option(
    "--ignore-unknown-hosts",
    is_flag=True,
    default=False,
    help="Ignore checks on unknown hosts (when we can't resolve the hostname).",
)
@click.option("--info", is_flag=True, default=False, help="Show clusters info and exit.")
@click.option("--use-ssh", is_flag=True, default=False, help="Use clickhouse client over ssh to query the host.")
def check_metrics_tables_command(
    config: click.Path,
    check_host: str | None = None,
    check_clusters: str | None = None,
    verbose: bool = False,
    ignore_data_clusters: bool = False,
    ignore_metrics_cluster: bool = False,
    ignore_unknown_hosts: bool = False,
    info: bool = False,
    use_ssh: bool = False,
):
    """Checks that metrics tables are present everywhere."""

    logging.basicConfig(level=logging.INFO)
    conf, _ = common.setup_redis_client(config=config)

    logging.info("Checking for metrics tables and views...")

    if not check_host:
        check_host = conf.get("internal_database_server")
        if not check_host:
            logging.info("Missing --check-host and `internal_database_server` in config.")
            return
        logging.info(f"Using `internal_database_server`={check_host}.")

    errors: list[str] = common.run_until_complete(
        check_metrics_tables(
            conf=conf,
            check_host=check_host,
            check_clusters=check_clusters,
            verbose=verbose,
            ignore_data_clusters=ignore_data_clusters,
            ignore_metrics_cluster=ignore_metrics_cluster,
            ignore_unknown_hosts=ignore_unknown_hosts,
            info=info,
            use_ssh=use_ssh,
        )
    )

    if len(errors) == 0:
        logging.info("All checks passed.")
    else:
        logging.error(f"ERROR: Found {len(errors)} error(s).")
