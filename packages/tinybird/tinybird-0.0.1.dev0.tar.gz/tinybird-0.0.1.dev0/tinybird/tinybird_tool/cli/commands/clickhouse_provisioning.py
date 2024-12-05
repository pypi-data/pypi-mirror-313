import logging

import click

from tinybird.ch import HTTPClient
from tinybird.ch_utils.exceptions import CHException
from tinybird.tinybird_tool.metrics import add_metrics_to_host, check_metrics_tables

from ... import common
from ..cli_base import cli


def _add_disabled_table_on_all_cluster_instances(host: str, cluster: str, dry_run: bool = False) -> None:
    """Creates the server disabled table on all instances of a ClickHouse cluster."""
    client = HTTPClient(host)

    table_name = "default.tb_server_disabled"

    logging.info(f"Creating '{table_name}' on cluster '{cluster}' using '{host}'...")

    query_create = f"""
    CREATE TABLE IF NOT EXISTS {table_name} ON CLUSTER {cluster}
    (
        `changed` DateTime DEFAULT now(),
        `disabled` Boolean
    )
    ENGINE = MergeTree
    ORDER BY (changed)
    TTL changed + INTERVAL 1 YEAR"""

    if dry_run:
        logging.info(f"Table creation query: {query_create}")
    else:
        try:
            client.query_sync(query_create, read_only=False)
        except CHException as e:
            raise Exception(f"Failed creating table: {e}") from e


def _add_backup_log_replicated_table(
    host: str, cluster: str, dry_run: bool = False, public_database: str | None = None
) -> None:
    """Creates the backup log MVs on all instances of a ClickHouse cluster."""
    client = HTTPClient(host)

    public_database_name = public_database or "public"

    system_table = "system.backup_log"
    destination_table = f"{public_database_name}.backup_log_materialized"
    materialized_view = f"{public_database_name}.backup_log_materialized_view"

    logging.info(f"Checking '{system_table}' existence on '{host}'...")
    query_check = "SELECT throwIf(count() == 0, 'Table not present in host') FROM system.tables where database = 'system' and name = 'backup_log'"

    if dry_run:
        logging.info(f"Table check query: {query_check}")
    else:
        try:
            client.query_sync(query_check)
        except CHException as e:
            raise Exception(f"Failed checking table existence: {e}") from e

    logging.info(f"Creating '{destination_table}' table on cluster '{cluster}' using '{host}'...")
    query_destination_table = f"""
    CREATE TABLE IF NOT EXISTS {destination_table} ON CLUSTER {cluster}
    (
        `id` String,
        `name` String,
        `base_backup_name` String,
        `status` String,
        `event_date` Date,
        `event_time_microseconds` DateTime64(6),
        `event_time` DateTime,
        `start_time` DateTime,
        `end_time` DateTime,
        `num_files` UInt64,
        `total_size` UInt64,
        `num_entries` UInt64,
        `uncompressed_size` UInt64,
    )
    ENGINE = ReplicatedMergeTree('/clickhouse/tables/{cluster}/{destination_table}', '{{replica}}')
    PARTITION BY toYYYYMM(event_date)
    ORDER BY (event_date, event_time_microseconds)
    TTL event_date + toIntervalMonth(1)
    SETTINGS index_granularity = 8192, min_bytes_for_wide_part=0, min_rows_for_wide_part=0
    COMMENT 'Materializes the contents of {system_table}.'
    """

    if dry_run:
        logging.info(f"Table creation query: {query_destination_table}")
    else:
        try:
            client.query_sync(query_destination_table, read_only=False)
        except CHException as e:
            raise Exception(f"Failed creating table: {e}") from e

    logging.info(f"Creating '{materialized_view}' MV on cluster '{cluster}' using '{host}'...")
    query_materialized_view = f"""
    CREATE MATERIALIZED VIEW IF NOT EXISTS {materialized_view} ON CLUSTER {cluster} TO {destination_table}
    AS
    SELECT
        id,
        name,
        base_backup_name,
        status::String as status,
        event_time_microseconds::Date as event_date,
        event_time_microseconds::DateTime as event_time,
        event_time_microseconds,
        end_time,
        start_time,
        num_files,
        total_size,
        num_entries,
        uncompressed_size
    FROM {system_table}
    """

    if dry_run:
        logging.info(f"MV creation query: {query_materialized_view}")
    else:
        try:
            client.query_sync(query_materialized_view, read_only=False)
        except CHException as e:
            raise Exception(f"Failed creating MV: {e}") from e


def provision_cluster(
    *,
    host: str,
    cluster: str,
    config: click.Path | None = None,
    use_hostname: bool = False,
    dry_run: bool = False,
    metrics_host_cluster: str | None = None,
    metrics_database: str | None = None,
    public_database: str | None = None,
) -> None:
    """
    Runs all the provisioning tasks for a single ClickHouse host or for all host in a ClickHouse cluster.
    """

    # /!\ IMPORTANT /!\
    # All code in this function MUST BE IDEMPOTENT as it can, and will be, run several times for a cluster. For example,
    # when adding a replica to a cluster.

    conf, _ = common.setup_redis_client(config)

    logging.info(f"Getting all instances from cluster '{cluster}'...")

    try:
        cluster_hosts = common.run_until_complete(
            common.get_cluster_members_with_ports(host, cluster, HTTPClient(host))
        )
    except CHException as e:
        raise Exception(f"Failed getting cluster members: {e}") from e

    if len(cluster_hosts) == 0:
        raise Exception(f"No hosts found for cluster '{cluster}'.")

    logging.info(
        f"Cluster '{cluster}' hosts to provision: "
        + ", ".join(f"{ch['host_name']} ({ch['host_address']}:{ch['http_port']})" for ch in cluster_hosts)
    )

    # [HOST TASKS]: Tasks that need to be run for each instance of a cluster.
    for ch in cluster_hosts:
        remote_addr = f"{ch['host_name'] if use_hostname else ch['host_address']}:{ch['http_port']}"

        logging.info(
            f"Provisioning '{ch['host_name']}' ({ch['host_address']}) from cluster '{cluster}' connecting to '{remote_addr}'..."
        )

        # TASK: Add metrics tables to the host
        try:
            add_metrics_to_host(conf, remote_addr, dry_run, metrics_host_cluster, metrics_database)
        except Exception as e:
            raise Exception(f"Failed adding metrics to host '{ch['host_name']}': {e}") from e

    # [CLUSTER TASKS]: Tasks that need to be run in any instance of a cluster (ON CLUSTER operations typically).
    first_host_remote_addr = f"{cluster_hosts[0]['host_name'] if use_hostname else cluster_hosts[0]['host_address']}:{cluster_hosts[0]['http_port']}"

    # TASK: Check that metrics tables are present on all replicas
    if not dry_run:
        errors: list[str] = common.run_until_complete(check_metrics_tables(conf, first_host_remote_addr))

        if len(errors) == 0:
            logging.info("All metrics tables checks passed.")
        else:
            for err in errors:
                logging.error(err)

            raise Exception(f"Found {len(errors)} metric tables error(s).")

    # TASK: Create backups logs replicated tables on all replicas
    try:
        _add_backup_log_replicated_table(first_host_remote_addr, cluster, dry_run, public_database)
    except Exception as e:
        raise Exception(f"Failed adding backup log replicated table to cluster '{cluster}': {e}") from e

    # TASK: Create server disabled table on all replicas
    try:
        _add_disabled_table_on_all_cluster_instances(first_host_remote_addr, cluster, dry_run)
    except Exception as e:
        raise Exception(f"Failed adding disabled table to cluster '{cluster}': {e}") from e


@cli.command()
@click.option("--host", required=True, help="One of the hosts of the ClickHouse cluster")
@click.option("--cluster", required=True, help="ClickHouse cluster to provision all hosts")
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
@click.option("--use-hostname", is_flag=True, default=False, help="Use ClickHouse server hostnames instead of the IPs")
@click.option("--dry-run", is_flag=True, default=False)
@click.option("--metrics-host-cluster", type=click.STRING, default=None, help="This is mostly used for testing")
@click.option("--metrics-database", type=click.STRING, default=None, help="This is mostly used for testing")
@click.option("--public-database", type=click.STRING, default=None, help="This is mostly used for testing")
def provision_clickhouse_cluster(
    host: str,
    cluster: str,
    config: click.Path | None = None,
    use_hostname: bool = False,
    dry_run: bool = False,
    metrics_host_cluster: str | None = None,
    metrics_database: str | None = None,
    public_database: str | None = None,
    single_host: bool = False,
) -> None:
    """Runs provisioning tasks for all the hosts of a ClickHouse cluster."""
    # DO NOT add provisioning code in this CLI function. Do it in provision_cluster as it can be called from other places
    # like add-replica cli command.
    logging.basicConfig(level=logging.INFO)
    provision_cluster(
        host=host,
        cluster=cluster,
        config=config,
        use_hostname=use_hostname,
        dry_run=dry_run,
        metrics_host_cluster=metrics_host_cluster,
        metrics_database=metrics_database,
        public_database=public_database,
    )
