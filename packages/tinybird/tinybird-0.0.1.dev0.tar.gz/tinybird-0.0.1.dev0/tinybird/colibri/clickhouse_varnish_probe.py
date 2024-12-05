import enum
import json
import time

import click
from ansible.inventory.host import Host

from .ansible_config import log_fatal
from .clickhouse_queries import run_remote_query
from .logging import log_error, log_info, log_success, log_warning, preprocess_message
from .prompt import prompt_for_confirmation
from .utils import CONTEXT_SETTINGS

_VARNISH_PROBE_TABLE_NAME = "default.tb_server_disabled"
_VARNISH_TRAFFIC_WAIT_SECONDS = 5


class HostStatus(enum.StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"
    FAILED = "FAILED"


def _get_affected_clusters_with_hosts(host: Host | str) -> dict[str, list[str]]:
    query = """SELECT DISTINCT cluster FROM system.clusters WHERE is_local=1 FORMAT JSON"""
    _, stdout, _ = run_remote_query(host, query, fatal=True)

    clusters: dict[str, list[str]] = {c["cluster"]: [] for c in json.loads(stdout)["data"]}

    for cluster in clusters:
        query = f"""
            SELECT
                hostname() AS hostname
            FROM
                clusterAllReplicas('{cluster}', system.clusters)
            WHERE
                is_local == 1 AND cluster == '{cluster}'
            ORDER BY
                hostname ASC
            FORMAT JSON
        """

        _, stdout, _ = run_remote_query(host, query, fatal=True)

        clusters[cluster] = [h["hostname"] for h in json.loads(stdout)["data"]]

    return clusters


def _ensure_not_all_disabled(host_to_disable: Host | str) -> None:
    log_info("Checking if we can safely disable the instance...")

    statuses = get_clickhouse_varnish_probe_status_all_clusters_replicas(host_to_disable)

    for cluster_name, cluster_hosts in statuses.items():
        enabled_hosts = [h for h, s in cluster_hosts.items() if s[0] == HostStatus.ENABLED]
        disabled_hosts = [h for h, s in cluster_hosts.items() if s[0] == HostStatus.DISABLED]
        failed_hosts = [h for h, s in cluster_hosts.items() if s[0] == HostStatus.FAILED]

        if failed_hosts:
            log_warning(
                f"Failed checking the following cluster **{cluster_name}** members: **{', '.join(failed_hosts)}**"
            )

        if host_to_disable in failed_hosts:
            log_fatal(f"Couldn't check status for **{host_to_disable}**, aborting.")

        # Check if host is already disabled
        if host_to_disable in disabled_hosts:
            log_info(f"Instance **{host_to_disable}** is already disabled for cluster **{cluster_name}**, skipping...")
            continue

        # Check clusters with 1 instance
        if len(enabled_hosts) + len(disabled_hosts) == 1:
            log_warning(
                f"Cluster **{cluster_name}** only has **1 instance**, **disabling {host_to_disable} will take down the cluster completely**."
            )

            if not prompt_for_confirmation("Are you sure you want to continue with the process?", default=True):
                log_fatal("User cancelled.")

            else:
                continue

        # Check that the host to disable is not already disabled (if it is nothing changes) and that we have more than 1 enabled hosts.
        if len(enabled_hosts) <= 1:
            log_warning(
                f"Cluster **{cluster_name}** currently has **{len(enabled_hosts)} enabled** instances and **{len(disabled_hosts)} disabled** instances."
            )
            if failed_hosts:
                log_warning(
                    f"Additionally, **status check failed for {len(failed_hosts)} instances, considering them as disabled.**"
                )
            log_warning(f"**Disabling '{host_to_disable}' will take down the cluster completely**.")

            if not prompt_for_confirmation("Are you sure you want to continue with the process?", default=False):
                log_fatal("User cancelled.")

        log_info(
            f"Cluster **{cluster_name}** will have **{len(enabled_hosts) - 1} instances enabled** and **{len(disabled_hosts) + 1} instances disabled**."
        )
        if failed_hosts:
            log_info(
                f"Additionally, **status check failed for {len(failed_hosts)} instances, considering them as disabled.**"
            )


def _change_clickhouse_probe(host: Host | str, disabled: bool, error_is_fatal: bool) -> tuple[int, str, str, str]:
    query = f"""INSERT INTO {_VARNISH_PROBE_TABLE_NAME}(disabled) VALUES ({'true' if disabled else 'false'})"""
    return *run_remote_query(host, query, fatal=error_is_fatal), query


def set_clickhouse_varnish_probe_to_disabled(host: Host | str) -> None:
    _ensure_not_all_disabled(host)

    _change_clickhouse_probe(host, disabled=True, error_is_fatal=True)

    log_info(f"Disabled **{host}**, waiting {_VARNISH_TRAFFIC_WAIT_SECONDS} seconds...")
    time.sleep(_VARNISH_TRAFFIC_WAIT_SECONDS)


def set_clickhouse_varnish_probe_to_enabled(host: Host | str) -> None:
    rc, _, output_err, query = _change_clickhouse_probe(host, disabled=False, error_is_fatal=False)

    if rc == 0:
        log_info(f"Enabled **{host}**, waiting {_VARNISH_TRAFFIC_WAIT_SECONDS} seconds...")
        time.sleep(_VARNISH_TRAFFIC_WAIT_SECONDS)
    else:
        log_error("Failed changing Varnish ClickHouse probe to enable instance.")
        log_error(f"Query: {query}")
        log_error("=========================================")
        log_error(output_err)
        log_error("=========================================")
        log_error(
            "This error is considered not critical and will continue, resolve the issue and try enabling the instance again"
        )


def get_clickhouse_varnish_probe_status(host: Host | str) -> tuple[HostStatus, str | None]:
    query = f"SELECT disabled, toDateTime(changed, 'UTC') as changed_utc FROM {_VARNISH_PROBE_TABLE_NAME} ORDER BY changed DESC LIMIT 1 FORMAT JSON"
    rc, output, output_err = run_remote_query(host, query)

    if rc != 0:
        log_error(f"Failed checking Varnish ClickHouse probe status for host '{host}'.")
        log_error(f"Query: {query}")
        log_error("=========================================")
        log_error(output_err)
        log_error("=========================================")
        return HostStatus.FAILED, None

    result = json.loads(output)

    if result["data"]:
        return (
            HostStatus.DISABLED if result["data"][0]["disabled"] else HostStatus.ENABLED,
            result["data"][0]["changed_utc"],
        )

    return HostStatus.ENABLED, None


def get_clickhouse_varnish_probe_status_all_clusters_replicas(
    host: Host | str,
) -> dict[str, dict[str, tuple[HostStatus, str | None]]]:
    affected = _get_affected_clusters_with_hosts(host)

    statuses: dict[str, dict[str, tuple[HostStatus, str | None]]] = {}

    for cluster_name, cluster_hosts in affected.items():
        statuses[cluster_name] = {}

        for check_host in cluster_hosts:
            statuses[cluster_name][check_host] = get_clickhouse_varnish_probe_status(check_host)

    return statuses


@click.group(context_settings=CONTEXT_SETTINGS, short_help="Control CH instance Varnish traffic")
def clickhouse_varnish_probe() -> None:
    pass


@clickhouse_varnish_probe.command(name="enable", short_help="Enable Varnish sending traffic to an instance")
@click.argument("server", type=click.STRING)
def clickhouse_varnish_probe_enable(server: str) -> None:
    log_info(f"Enabling traffic from Varnish to **{server}**...")
    set_clickhouse_varnish_probe_to_enabled(server)
    log_success("Done!")


@clickhouse_varnish_probe.command(name="disable", short_help="Disable Varnish sanding traffic to an instance")
@click.argument("server", type=click.STRING)
def clickhouse_varnish_probe_disable(server: str) -> None:
    log_info(f"Disabling traffic from Varnish to **{server}**...")
    set_clickhouse_varnish_probe_to_disabled(server)
    log_success("Done!")


@clickhouse_varnish_probe.command(name="status", short_help="Check if Varnish is enabled for an instance")
@click.option(
    "--all-replicas",
    is_flag=True,
    default=False,
    help="Shows the status for all the replicas of the cluster the instance belongs to",
)
@click.argument("server", type=click.STRING)
def clickhouse_varnish_probe_status(server: str, all_replicas: bool = False) -> None:
    if all_replicas:
        log_info(f"Checking traffic status Varnish to all clusters replicas **{server}** belongs to...")
        statuses = get_clickhouse_varnish_probe_status_all_clusters_replicas(server)

        for cluster_name, cluster_hosts in statuses.items():
            log_info(f"Cluster **{cluster_name}** statuses:")

            for hostname, (status, change_date) in cluster_hosts.items():
                click.secho(
                    preprocess_message(f"**{hostname}**")
                    + ": "
                    + preprocess_message(f"**{status}**", "green" if status == HostStatus.ENABLED else "red")
                    + (preprocess_message(f" @ **{change_date}** (UTC)") if change_date else "")
                )

    else:
        log_info(f"Checking traffic status Varnish to **{server}**...")
        status, change_date = get_clickhouse_varnish_probe_status(server)

        click.secho(
            preprocess_message(f"**{server}**")
            + ": "
            + preprocess_message(f"**{status}**", "green" if status == HostStatus.ENABLED else "red")
            + (preprocess_message(f" @ **{change_date}** (UTC)") if change_date else "")
        )
