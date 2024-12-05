import io

from ansible.inventory.host import Host

from .ansible_config import log_fatal
from .logging import log_warning
from .ssh import get_connection, run_ssh_command


def run_remote_query(
    host: Host | str, query: str, fatal: bool = True, max_execution_time: int = 300
) -> tuple[int, str, str]:
    _, tmpfile, _ = run_ssh_command(host, "mktemp")
    tmpfile = tmpfile.strip()

    conn = get_connection(host)
    conn.run(f"cat > {tmpfile}", timeout=300, hide="both", in_stream=io.StringIO(query), warn=True)

    ch_cmd = f"clickhouse client --max_execution_time {max_execution_time} --queries-file {tmpfile}"

    # Prevent reading STDIN on INSERTS that have data
    if "INSERT" in query and "VALUES" in query:
        ch_cmd += " < /dev/null"

    return_code, output_std, output_err = run_ssh_command(host, ch_cmd)

    if fatal and return_code:
        log_warning(f"Failed to execute query: **{query}**")
        log_warning(ch_cmd)
        log_warning("=========================================")
        log_warning(f"{output_err}")
        log_warning("=========================================")
        log_fatal("I would rather not continue (see logs above)")

    return return_code, output_std, output_err


# We can have only one cluster in the normal setups, and 2 clusters on the failover setup.
# So with this query we are targeting to get the cluster with less hosts
_cluster_query_get = """
                SELECT
                    cluster,
                    count() count
                FROM system.clusters
                WHERE cluster in
                    ( SELECT
                        cluster
                        FROM system.clusters
                        WHERE is_local
                    )
                GROUP BY cluster
                ORDER BY count ASC
                LIMIT 1
                FORMAT JSON"""

_full_replication_error_check = """
                       is_readonly
                    OR is_session_expired
                    OR future_parts > 20
                    OR parts_to_check > 10
                    OR queue_size > 100
                    OR inserts_in_queue > 50
                    OR merges_in_queue > 50
                    OR absolute_delay > 30"""

_zk_metadata_version_issue_query = """
                SELECT
                    t1.resource resource,
                    t4.path zk_path,
                    t1.metadata_version zk_version,
                    t2.version expected_version,
                    t2.value_clean table_metadata,
                    t4.value_clean replica_metadata,
                    t3.queue::UInt32 queue
                FROM
                (
                    SELECT
                        concat(database, '.', `table`) AS resource,
                        metadata_version
                    FROM system.tables
                    WHERE startsWith(engine, 'Replicated')
                ) AS t1
                INNER JOIN
                (
                    SELECT
                        concat(database, '.', `table`) AS resource,
                        version,
                        replaceRegexpAll(
                            value, '\n(merge parameters format version: \d+|version column: [a-z0-9_]+)', ''
                        ) value_clean
                    FROM system.zookeeper zk
                    INNER JOIN system.replicas r ON r.zookeeper_path = zk.path
                    WHERE (path IN (
                        SELECT zookeeper_path
                        FROM system.replicas
                    )) AND (name = 'metadata')
                ) AS t2 ON t2.resource = t1.resource
                INNER JOIN
                (
                    SELECT
                        concat(database, '.', `table`) AS resource,
                        path,
                        replaceRegexpAll(
                            value, '\n(merge parameters format version: \d+|version column: [a-z0-9_]+)', ''
                        ) value_clean
                    FROM system.zookeeper zk
                    INNER JOIN system.replicas r ON r.replica_path = zk.path
                    WHERE (path IN (
                        SELECT replica_path
                        FROM system.replicas
                    )) AND (name = 'metadata')
                ) AS t4 ON t4.resource = t1.resource
                LEFT JOIN
                (
                    SELECT
                        concat(database, '.', `table`) AS resource,
                        count() AS queue
                    FROM system.replication_queue
                    WHERE (type != 'MERGE_PARTS')
                    GROUP BY 1
                ) AS t3 ON t3.resource = t1.resource
                WHERE version != metadata_version
                    AND table_metadata = replica_metadata
                FORMAT JSON"""


def _check_replication_status_error_count_query_get(cluster_name: str) -> str:
    return f"""
                SELECT
                    hostname() as host,
                    countIf({_full_replication_error_check}) as errors
                FROM clusterAllReplicas('{cluster_name}', system.replicas)
                WHERE database NOT LIKE '%__populate_%'
                GROUP BY host
                FORMAT JSON"""


def _check_replication_status_error_info_query_get(cluster_name: str, limit: int) -> str:
    return f"""
                    SELECT
                        hostname() as hostname,
                        database,
                        table,
                        is_readonly,
                        is_session_expired,
                        future_parts,
                        parts_to_check,
                        queue_size,
                        inserts_in_queue,
                        merges_in_queue,
                        absolute_delay
                    FROM clusterAllReplicas('{cluster_name}', system.replicas)
                    WHERE ({_full_replication_error_check})
                        AND database NOT LIKE '%__populate_%'
                    LIMIT {limit}
                    FORMAT JSON
                """
