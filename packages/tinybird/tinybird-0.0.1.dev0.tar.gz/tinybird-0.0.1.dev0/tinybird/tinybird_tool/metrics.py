import json
import logging
import re
from typing import Any, Dict, List, Optional, Union

from tinybird.ch import HTTPClient, ch_flush_logs_on_all_replicas
from tinybird.default_tables import (
    DEFAULT_METRICS_CLUSTER_TABLES,
    DEFAULT_METRICS_CLUSTER_VIEWS,
    DEFAULT_METRICS_TABLES,
    DEFAULT_METRICS_VIEWS,
    DefaultTable,
    DefaultView,
)
from tinybird.internal_resources import _create_host_metrics_tables, init_metrics_tables
from tinybird.user import User, public

from . import common


def add_metrics_to_host(
    conf: Dict[str, Any],
    host: str,
    dry_run: bool = False,
    host_cluster: Optional[str] = None,
    metrics_database: Optional[str] = None,
) -> None:
    """Provision metrics MVs in the target host"""
    metrics_cluster = conf.get("metrics_cluster", None)
    metrics_database_server = conf.get("metrics_database_server", None)

    common.run_until_complete(
        init_metrics_tables(
            host=host,
            metrics_cluster=metrics_cluster,
            metrics_database_server=metrics_database_server,
            metrics_cluster_tables=[],
            metrics_cluster_views=[],
            metrics_tables=DEFAULT_METRICS_TABLES,
            metrics_views=DEFAULT_METRICS_VIEWS,
            metrics_database=metrics_database or "default",
            add_datasources=False,
            dry_run=dry_run,
            host_cluster=host_cluster,
        )
    )


async def fix_metrics_on_host(
    conf: Dict[str, Any],
    host: str,
    tables: List[str],
    metrics_database: str = "default",
    exchange_tables: bool = False,
    copy_data: bool = False,
    dry_run: bool = False,
) -> None:
    metrics_cluster: str = conf["metrics_cluster"]
    if not metrics_cluster:
        logging.info("Missing 'metrics_cluster' in config.")
        return
    else:
        logging.info(f"Using metrics cluster '{metrics_cluster}'")

    public_user: User = public.get_public_user()

    await ch_flush_logs_on_all_replicas(database_server=host, cluster=metrics_cluster)

    # Go table by table to identify problems earlier
    for table in tables:
        new_table: str = f"{table}__v2"
        mapping: Dict[str, str] = {table: new_table}

        # Step 1: Recreate the table with a '__v2' suffix

        metrics_tables = [t for t in DEFAULT_METRICS_TABLES if t.name == table]

        await _create_host_metrics_tables(
            host,
            metrics_cluster,
            metrics_database,
            metrics_tables,
            public_user,
            False,
            dry_run,
            table_mapping=mapping,
            ignore_errors=False,
        )

        await ch_flush_logs_on_all_replicas(host)

        client: HTTPClient = HTTPClient(host, database=public_user.database)

        # Step 2: EXCHANGE old and new tables
        if exchange_tables:
            logging.info("Exchanging tables...")
            sql_exchange: str = f"EXCHANGE TABLES {table} AND {new_table}"
            if dry_run:
                logging.info(f'Run query: "{sql_exchange}" on host {host}')
            else:
                await client.query(sql_exchange, read_only=False)

        # Step 3: Insert prev data into the good table
        if exchange_tables and copy_data:
            logging.info("Copying data...")
            sql_copy: str = f"INSERT INTO {table} SELECT * FROM {new_table}"
            if dry_run:
                logging.info(f'Run query: "{sql_copy}" on host {host}')
            else:
                try:
                    await client.query(sql_copy, read_only=False)
                except Exception as e:
                    # We did a recent migration, but maybe these tables weren't upadted
                    # as we updated default_tables after the manual intervention and
                    # some hosts were added in the meantime.
                    error = str(e)
                    missing_migration = ("NUMBER_OF_COLUMNS_DOESNT_MATCH" in error) or (
                        "Number of columns doesn" in error
                    )
                    if not missing_migration:
                        logging.info("NUMBER_OF_COLUMNS_DOESNT_MATCH: Probably __inserted_at is missing")
                        raise e


def _check_engine_template(engine_template: str, engine_values: List[str]) -> bool:
    """
    >>> template = "Distributed('{cluster}', '{database}', 'ficticious_metrics_table', rand())"
    >>> engine = "Distributed('my_cluster', 'my_database', 'ficticious_metrics_table', rand())"
    >>> _check_engine_template(template, [engine])
    True
    >>> template = "Distributed('{cluster}', '{database}', 'ficticious_metrics_table', rand())"
    >>> engine = "Distributed('my_cluster', 'my_database', 'ficticious_metrics_table')"
    >>> _check_engine_template(template, [engine])
    False
    """
    # Make the template a valid regex
    tpl: str = re.escape(engine_template)
    tpl = re.sub(r"\\\{[a-z_]+\\\}", "[^']+", tpl)

    return any(re.match(tpl, v) for v in engine_values)


def _check_engine(expected: str, engine_values: List[str]) -> bool:
    """
    >>> expected = "MergeTree() ORDER BY (user_id, datasource_id, topic, timestamp) PARTITION BY toYYYYMMDD(timestamp) TTL timestamp + INTERVAL 30 DAY"
    >>> engine = "MergeTree() ORDER BY (user_id, datasource_id, topic, timestamp) PARTITION BY toYYYYMMDD(timestamp) TTL timestamp + INTERVAL 30 DAY"
    >>> _check_engine(expected, [engine])
    True
    >>> expected = "MergeTree() ORDER BY (user_id, datasource_id, topic, timestamp) PARTITION BY toYYYYMMDD(timestamp) TTL timestamp + INTERVAL 30 DAY"
    >>> engine = "MergeTree() ORDER BY (user_id, datasource_id, topic, timestamp) PARTITION BY toYYYYMMDD(timestamp)"
    >>> _check_engine(expected, [engine])
    False
    """
    return expected in engine_values


def _check_replicated_engine(expected: str, engine_values: List[str]) -> bool:
    """
    >>> expected = "MergeTree() ORDER BY (user_id, datasource_id, topic, timestamp) PARTITION BY toYYYYMMDD(timestamp) TTL timestamp + INTERVAL 30 DAY"
    >>> engine = "ReplicatedMergeTree(...)"
    >>> _check_replicated_engine(expected, [engine])
    True
    >>> expected = "MergeTree() ORDER BY (user_id, datasource_id, topic, timestamp) PARTITION BY toYYYYMMDD(timestamp) TTL timestamp + INTERVAL 30 DAY"
    >>> engine = "ReplicatedSummingMergeTree(...)"
    >>> _check_replicated_engine(expected, [engine])
    False
    """
    if not all(v.startswith("Replicated") for v in engine_values):
        return True  # Not Replicated<whatever> engine

    # For Replicated<whatever> engines.
    # The <whatever> part must match the definition engine.
    m: Optional[re.Match] = re.match("^([a-zA-Z0-9_]+)\(", expected)
    if m is None:
        return True  # Not a match?

    return any(v.startswith(f"Replicated{m[1]}") for v in engine_values)


async def check_metrics_tables(
    conf: Dict[str, Any],
    check_host: str,
    check_clusters: Optional[str] = None,
    verbose: bool = False,
    ignore_data_clusters: bool = False,
    ignore_metrics_cluster: bool = False,
    ignore_unknown_hosts: bool = False,
    info: bool = False,
    use_ssh: bool = False,
    look_at_specific_database: Optional[str] = None,
) -> List[str]:
    """Checks that metrics tables are present everywhere.

    Returns the list of errors found in human readable form.
    """

    errors: List[str] = []

    try:
        metrics_cluster: Optional[str] = conf.get("metrics_cluster", None)

        client: Optional[HTTPClient] = None if use_ssh else HTTPClient(check_host)

        clusters: List[str] = (
            check_clusters.split(",") if check_clusters else await common.get_all_clusters(check_host, client)
        )
        clusters = [c for c in clusters if c]  # Some cleanup

        hostnames: Dict[str, str] = await common.get_hostnames(check_host, clusters, client)

        # all_clusters = Dict indexed by cluster names containing hosts list
        all_clusters: Dict[str, List[str]] = await common.get_all_hosts(check_host, clusters, client)

        if verbose or info:
            logging.info("HOSTS:")
            for ip, hostname in hostnames.items():
                logging.info(f"* {hostname} ({ip})")
            logging.info("")

            logging.info("CLUSTERS:")
            for k, cluster_hosts in all_clusters.items():
                logging.info(f"* {k}")
                for addr in cluster_hosts:
                    logging.info(f"  > {addr} ({hostnames.get(addr, addr)})")
            logging.info("")

        # One pass to delete to-be-ignored clusters
        ignored_clusters: List[str] = []
        for k in list(all_clusters.keys()):
            if (ignore_metrics_cluster and k == metrics_cluster) or (ignore_data_clusters and k != metrics_cluster):
                ignored_clusters.append(k)
                del all_clusters[k]

        if (verbose or info) and len(ignored_clusters) > 0:
            logging.info("IGNORED CLUSTERS:")
            for ic in ignored_clusters:
                logging.info(f"* {ic}")
            logging.info("")

        if info:
            return errors

        # Resources required in metrics clusters
        metrics_host_resources: List[str] = [t.name for t in DEFAULT_METRICS_CLUSTER_TABLES] + [
            v.name for v in DEFAULT_METRICS_CLUSTER_VIEWS
        ]

        # Resources required in data clusters
        data_host_resources: List[str] = [t.name for t in DEFAULT_METRICS_TABLES] + [
            v.name for v in DEFAULT_METRICS_VIEWS
        ]

        items: List[Dict[str, Any]] = []

        def accumulate_error(err_msg: str) -> None:
            logging.exception(err_msg)
            errors.append(err_msg)

        for cluster in all_clusters.keys():
            if verbose:
                logging.info(f"Fetching tables for {addr} on cluster {cluster}...")

            database_filter = "" if not look_at_specific_database else f"AND database = '{look_at_specific_database}'"

            check_query: str = f"""
                SELECT
                    hostName() as hostname,
                    database,
                    name,
                    create_table_query,
                    engine_full
                FROM
                    clusterAllReplicas('{cluster}', system.tables)
                WHERE
                    name in ('{"','".join(data_host_resources + metrics_host_resources)}')
                    {database_filter}
                FORMAT JSON
            """

            try:
                partial = json.loads(await common.execute_on_remote(check_host, check_query, client))["data"]

                if verbose and len(partial) > 0:
                    logging.info(f" - {len(partial)} rows fetched.")
                items += partial
            except Exception as ex:
                accumulate_error(f"ERROR fetching tables for {addr} on cluster {cluster}: {str(ex)}...")

        # Index existing tables by host+table
        existing_tables: Dict[str, Dict[str, Any]] = {}
        for item in items:
            existing_tables[f"{item['hostname']}-{item['name']}"] = item

        # Check if all required resources exist and have a correct definition
        for cluster, hosts_addresses in all_clusters.items():
            if "gatherer" in cluster:
                continue

            required_resources: List[str] = (
                metrics_host_resources if cluster == metrics_cluster else data_host_resources
            )

            for addr in hosts_addresses:
                if addr not in hostnames:
                    if ignore_unknown_hosts:
                        logging.info(f"IGNORING checks for {addr} on cluster {cluster}' (can't resolve hostname)")
                        logging.info("")
                        continue
                    if verbose:
                        logging.info(f"WARNING: Can't resolve hostname for {addr} on cluster {cluster}")

                h_name: str = hostnames.get(addr, addr)
                if verbose:
                    logging.info(f"Checking {addr} ({h_name}) on cluster {cluster}...")

                for t in required_resources:
                    # Check 1: Test resource existence
                    table: Optional[Dict[str, Any]] = existing_tables.get(f"{h_name}-{t}") or existing_tables.get(
                        f"{addr}-{t}"
                    )
                    if table is None:
                        accumulate_error(f"MISSING {t} in {addr} ({h_name}) on cluster {cluster}'")
                    else:
                        # Check 2: Test table engines
                        def get_resource(name: str) -> Optional[Union[DefaultTable, DefaultView]]:
                            return (
                                next((t for t in DEFAULT_METRICS_TABLES if t.name == name), None)
                                or next((t for t in DEFAULT_METRICS_CLUSTER_TABLES if t.name == name), None)
                                or next((t for t in DEFAULT_METRICS_VIEWS if t.name == name), None)
                                or next((t for t in DEFAULT_METRICS_CLUSTER_VIEWS if t.name == name), None)
                            )

                        resource = get_resource(t)
                        if resource is None:
                            logging.exception(f"INTERNAL ERROR: {t} not found in `default_tables.py`???")
                            continue

                        if isinstance(resource, DefaultView):
                            if verbose:
                                logging.info(f"Skipping view {resource.name}...")
                            continue

                        if verbose:
                            logging.info(f"Checking engine for {t}...")

                        # We check against both, the engine in the CREATE TABLE definition
                        # and the engine that CH informs as `engine_full``
                        actual_engine: str = re.findall("ENGINE\s+\=\s+(.+)$", table["create_table_query"])[0]
                        actual_full_engine: str = table["engine_full"]
                        expected_engine: str

                        engine_ok: bool = True
                        engines = [actual_engine, actual_full_engine]

                        # Check the actual engine against the expected
                        # being one (`engine_template` or `engine`)

                        if resource.engine_template:
                            if not _check_engine_template(
                                resource.engine_template, engines
                            ) and not _check_replicated_engine(resource.engine_template, engines):
                                engine_ok = False
                                expected_engine = resource.engine_template
                        elif resource.engine:
                            if not _check_engine(resource.engine, engines) and not _check_replicated_engine(
                                resource.engine, engines
                            ):
                                engine_ok = False
                                expected_engine = resource.engine
                        else:
                            # Just in the extrange case a table doesn't have
                            # # an engine defined.
                            engine_ok = False
                            expected_engine = "<Not found>"

                        if not engine_ok:
                            accumulate_error(
                                f"""BAD ENGINE for {t} in {addr} ({h_name}):)
- Expected: {expected_engine}")
- Actual  : {actual_engine}"""
                            )
    except Exception as e:
        logging.warning(f"[check_metrics_tables] {str(e)}")

    return errors
