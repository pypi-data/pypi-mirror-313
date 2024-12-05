#!/usr/bin/env python3
import collections
import copy
import itertools
import json
import math
import pathlib
import re
import signal
import string
import sys
import termios
import time
import traceback
import types
import typing
import urllib.parse
import uuid
from dataclasses import dataclass
from datetime import datetime
from difflib import SequenceMatcher
from enum import Enum
from fcntl import ioctl
from functools import partial
from os import getpid
from typing import Any, Callable, Dict, List, Match, Optional, Tuple

import click
import requests
from ansible import context
from ansible.cli import initialize_locale
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.inventory.group import Group
from ansible.inventory.host import Host
from ansible.module_utils.common.collections import ImmutableDict
from ansible.vars.manager import VariableManager
from click.termui import confirm, secho, style, visible_prompt_func
from click.types import STRING, Choice
from click.utils import echo
from git.repo import Repo
from humanfriendly import InvalidSize, format_size
from packaging import version
from prettytable import PrettyTable

from .alert_provisioning import (
    ch_is_down_silenced,
    delete_alert,
    generate_alert_json,
    get_alert_group,
    get_alerts_status,
    post_alert,
)
from .ansible_config import AnsibleGlobalConfig, get_ansible_config, log_fatal, reset_ansible_config
from .aws_operations import (
    find_instance_id_and_region as find_instance_id_and_region_aws,
)
from .aws_operations import resize_volume as resize_disk_aws
from .aws_operations import (
    scale_instance as scale_instance_aws,
)
from .aws_operations import (
    start_instance as start_instance_aws,
)
from .aws_operations import (
    stop_instance as stop_instance_aws,
)
from .azure_operations import list_server_data_disks, parse_lsscsi_output
from .azure_operations import resize_server_disk as resize_server_disk_azure
from .backupview import S3, open_backup
from .clickhouse_queries import (
    _check_replication_status_error_count_query_get,
    _check_replication_status_error_info_query_get,
    _cluster_query_get,
    _zk_metadata_version_issue_query,
    run_remote_query,
)
from .clickhouse_varnish_probe import set_clickhouse_varnish_probe_to_disabled, set_clickhouse_varnish_probe_to_enabled
from .disks import ServerDisk
from .gcp_operations import get_server_disk as get_server_disk_gcp
from .gcp_operations import get_zone_from_name as get_zone_from_name_gcp
from .gcp_operations import migrate_server_disk
from .gcp_operations import resize_server_disk as resize_server_disk_gcp
from .gcp_operations import scale_instance as scale_instance_gcp
from .gcp_operations import start_instance as start_instance_gcp
from .gcp_operations import stop_instance as stop_instance_gcp
from .gitlab import create_upgrade_mr, create_upgrade_ticket
from .initialize_ansible_environment import get_analytics_repo
from .logging import log_error, log_header, log_info, log_success, log_warning, preprocess_message
from .mutexbot import (
    MutexBotResource,
    get_tb_region_from_resource_name,
    list_resources,
    release_resource,
    reserve_resource,
)
from .prompt import prompt_for_choice, prompt_for_confirmation, prompt_for_input
from .restart_vm import restart_instance
from .ssh import run_ssh_command
from .utils import CONTEXT_SETTINGS

repo = get_analytics_repo()
REPO_ROOT = pathlib.Path(str(repo.working_tree_dir)).absolute()
DEPLOY_FOLDER = REPO_ROOT / "deploy"
INVENTORIES_FOLDER = REPO_ROOT / "deploy" / "inventories"

RESERVE_LOCK = "Reserve platform lock"
REMOVE_COPY_REPLICA = "Remove Split Replica from Copy Replica Set"
PENDING_START_CH = "Start ClickHouse service"
PENDING_START_GATHERER = "Start Gatherer service"
DEPROVISION_ALERTS = "Deprovision temporary ClickHouse alerts"
PENDING_ENABLE_CLICKHOUSE_PROBE = "Re-enable clickhouse Probe"
PLATFORM_LOCK_CHANNEL = "platform-lock"


def push_new_line_via_stdin() -> None:
    """This is a hack to simulate a new line input from the user (used when capturing Ctrl+C)"""
    tty_path = "/proc/{}/fd/0".format(getpid())
    with open(tty_path, "w") as tty_fd:
        ioctl(tty_fd, termios.TIOCSTI, "\n".encode())


def general_exception_hook(type_: type, value: Exception, traceback_: types.TracebackType) -> None:
    log_error("Exception raised, traceback:")
    traceback.print_exception(value)

    # Config is supposed to be initialized already here so interactive parameter doesn't matter
    get_ansible_config().cleanup_if_needed(force_cleanup=True)


def enable_general_exception_hook() -> None:
    if not hasattr(enable_general_exception_hook, "old_hook"):
        enable_general_exception_hook.old_hook = sys.excepthook  # type: ignore
    sys.excepthook = general_exception_hook  # type: ignore


def disable_general_exception_hook() -> None:
    if hasattr(enable_general_exception_hook, "old_hook"):
        sys.excepthook = enable_general_exception_hook.old_hook
        delattr(enable_general_exception_hook, "old_hook")


def generate_silence_url(matchers: List[str]) -> str:
    base_silence_url = "https://grafana.tinybird.app/alerting/silence/new?alertmanager=grafana"
    description = "&comment=Automatically+created+by+platform+tool"
    str_matchers = ""
    for matcher in matchers:
        str_matchers += "&matcher=" + urllib.parse.quote(matcher)
    return base_silence_url + description + str_matchers


def get_rollback_commit(repo: Repo, rollback_commit: Optional[str]) -> Optional[str]:
    # if commit passed as a parameter use it
    # otherwise use previous commit
    current_commit = repo.head.commit
    log_warning(f"Trying to rollback from commit {current_commit.hexsha}")
    if rollback_commit:
        if rollback_commit == "is_rollback":
            return None
        log_info(f"Rollback to --rollback-commit {rollback_commit}")
        checkout_commit = rollback_commit
    else:
        commits = list(repo.iter_commits("HEAD", max_count=2))
        if len(commits) < 2:
            log_info("No previous commit found")
            checkout_commit = None
        else:
            previous_commit = commits[-1]
            checkout_commit = previous_commit.hexsha
            log_info(f"Rollback to previous commit: {previous_commit.hexsha}")

    if checkout_commit:
        return checkout_commit
    else:
        raise Exception("No commit found to rollback. Use --rollback-commit to specify a given commit")


def do_the_prompt_with_options(text: str, options: List[str], default: str) -> str:
    if not get_ansible_config().interactive:
        return default
    options_msg = ""
    for option in options:
        if options_msg:
            options_msg += "/"
        if option == default:
            options_msg += option.upper()
        else:
            options_msg += option.lower()
    prompt = "[WARNING] " + style(preprocess_message(text, "yellow", "black"), blink=True) + f" [{options_msg}]: "
    while not get_ansible_config().quit:
        try:
            echo(prompt, nl=False)
            value = visible_prompt_func("").lower().strip()
        except (KeyboardInterrupt, EOFError):
            return default

        if not value:
            value = default
        if len(value) == 1:
            final_option = None
            for option in options:
                if option[0].lower() == value[0]:
                    if not final_option:
                        final_option = option.lower()
                    else:
                        log_warning(f"Several options start with the letter {value}. Please write the full option")
            if final_option:
                return final_option
        else:
            for option in options:
                if option.lower() == value:
                    return value
        echo("Error: invalid input")
    echo(default)
    return default


def do_the_anyways_or_exit(fatal_msg: str) -> None:
    conf = get_ansible_config()
    if not conf.interactive or not prompt_for_confirmation("Do you want to continue anyway?", default=False):
        log_fatal(fatal_msg)


def do_the_proceed_with_changes_or_exit(check_only: bool) -> None:
    conf = get_ansible_config()
    secho("")

    if check_only:
        log_success("Checks finished. Remember you can use --no-check-only to apply the changes")
        sys.exit(0)

    log_warning("We are **NOW** going to proceed with the changes (step by step)")

    if conf.interactive and not prompt_for_confirmation(
        "Are you sure you want to continue with the process?", default=True
    ):
        log_fatal("User cancelled")


def check_git_status() -> None:
    """Check the status of the deploy folder"""

    if repo.is_dirty(index=True, working_tree=True, untracked_files=True, submodules=True, path=DEPLOY_FOLDER):
        log_warning("The deploy/ folder contains **uncommitted changes**:")
        # noinspection PyProtectedMember
        untracked_files = repo._get_untracked_files(DEPLOY_FOLDER)
        modified_files = repo.git.diff("--name-only", "HEAD", "--", "deploy").splitlines() + untracked_files
        for line in modified_files:
            log_warning("\t" + line)
        do_the_anyways_or_exit("Unclean git status")


def get_single_ansible_host(server: str) -> Host:
    hosts = get_ansible_config().inventory.get_hosts(server)
    if not hosts:
        all_hosts = get_ansible_config().inventory.get_hosts()
        all_hosts.sort(reverse=True, key=lambda host: SequenceMatcher(None, server, host.name).ratio())
        closest = all_hosts[0] if len(all_hosts) else None
        close_matches: List[str] = []
        for host in all_hosts:
            if SequenceMatcher(None, server, host.name).ratio() > 0.66:
                close_matches.append(host.name)
        if not len(close_matches) and closest:
            log_fatal(f"Could not find server: **{server}**. Maybe you meant **{closest}**")
        elif len(close_matches):
            log_fatal(f"Could not find server: **{server}**. Maybe you meant **{close_matches}**")
        else:
            log_fatal(f"Could not find server: **{server}**.")
    if len(hosts) != 1:
        log_fatal(f"Matched more than one host: **{hosts}**")
    return hosts[0]


def get_host_region_inventory(host: Host) -> str:
    # Some servers (ITX Staging) declare it as a variable of the host
    # But most of them declare it as a variable of the group
    if "tb_region" in host.vars:
        return str(host.vars["tb_region"])

    # Iterate over ansible groups to find which one declares the host
    inventories_found: List[Group] = []
    for ansible_group in get_ansible_config().inventory.groups:
        g: Group = get_ansible_config().inventory.groups[ansible_group]
        if host in g.hosts and "tb_region" in g.get_vars():
            inventories_found.append(g)

    if not inventories_found:
        log_fatal(f"Could not find the **tb_region** for host: **{host}**")
    if len(inventories_found) != 1:
        log_warning(
            f"Found more than one affected **tb_region** from inventories: **{inventories_found}**. Will select first known region."
        )
        for inventory in inventories_found:
            tb_region = inventory.get_vars()["tb_region"]
            if tb_region == "unknown":
                continue
            log_info(f"using region: **{tb_region}**")
            return str(tb_region)

    return str(inventories_found[0].get_vars()["tb_region"])


def get_host_affected_ch_clusters(host: Host) -> List[str]:
    prefix: str = "clickhouse_cluster_"
    clusters: List[Group] = []

    all_groups = get_ansible_config().inventory.groups
    for group in all_groups:
        if str(group).startswith(prefix) and host in all_groups[group].hosts:
            clusters.append(group)

    if not clusters:
        log_fatal(f"Could not find the **clickhouse_cluster** for host: **{host}**")

    return [str(cluster)[len(prefix) :] for cluster in clusters]


def get_host_main_clickhouse_cluster(
    host: Host,
    cluster_query: str = _cluster_query_get,
) -> str:
    _, output, output_err = run_remote_query(host, cluster_query)

    response = json.loads(output)["data"]
    return str(response[0]["cluster"])


def run_ssh_command_with_retry(host: Host, cmd: str, timeout: int = 300) -> Tuple[int, str, str]:
    relaunch = True
    return_code: int = 0
    output_std: str = ""
    output_err: str = ""

    while relaunch:
        relaunch = False

        return_code, output_std, output_err = run_ssh_command(host, cmd, timeout=timeout)

        if return_code:
            log_warning(f"Failed to execute command: **{cmd}**")
            log_warning("=========================================")
            log_warning(f"{output_std}")
            log_warning(f"{output_err}")
            log_warning("=========================================")
            log_warning("Please log into the server yourself and check what happened")

            option = do_the_prompt_with_options(
                "How do you want to proceed?", ["continue", "relaunch", "abort"], default="abort"
            )

            if option == "relaunch":
                relaunch = True

            elif option == "abort":
                log_fatal("User aborted the operation")

    return return_code, output_std, output_err


def wait_for_ch_service(host: Host, verbose: bool = False) -> None:
    # After the process is restarted it will take a while (depending on the ClickHouse version, storage tables, etc)
    # To be ready to accept queries. Nothing to do but wait
    echo("* Waiting for the server to be up", nl=False)
    sleep_for = 2
    ask_after_seconds = 30
    active = False
    while not active:
        loop_start = time.time()
        while not active and not get_ansible_config().quit and time.time() - loop_start < ask_after_seconds:
            echo(".", nl=False)
            code, _, _ = run_remote_query(host, "SELECT 1", fatal=False)
            active = code == 0
            if not active:
                time.sleep(sleep_for)
        echo("")

        if not active:
            log_info(f"Over **{ask_after_seconds}** seconds have passed but the server is not responding yet")
            if verbose:
                _, output_std, output_err = run_ssh_command_with_retry(
                    host, "sudo systemctl status clickhouse-server", timeout=10
                )
                if output_err:
                    log_warning(output_err)
                if output_std:
                    log_info(output_std)
            option = do_the_prompt_with_options("How do you want to proceed?", ["wait", "abort"], default="wait")
            if option == "abort":
                log_fatal("User aborted waiting for ClickHouse to be up")


def clickhouse_service_restart_and_wait(host: Host, verbose: bool = False) -> None:
    log_header("Restarting CH service using systemd")

    cmd = "sudo systemctl restart clickhouse-server"
    _, _, _ = run_ssh_command_with_retry(host, cmd)
    wait_for_ch_service(host, verbose=verbose)
    log_success(f"Restarted ClickHouse service at **{host}**")


def clickhouse_service_status(host: Host, verbose: bool = False) -> None:
    log_header("Checking CH service using systemd")

    cmd = "sudo systemctl status clickhouse-server | grep Active"
    _, output, _ = run_ssh_command_with_retry(host, cmd, timeout=900)
    log_info(f"ClickHouse service status at **{host}**:\n{output}")


def clickhouse_service_start_and_wait(host: Host, verbose: bool = False) -> None:
    log_header("Starting CH service using systemd")

    cmd = "sudo systemctl start clickhouse-server"
    _, _, _ = run_ssh_command_with_retry(host, cmd, timeout=900)
    wait_for_ch_service(host, verbose=verbose)
    get_ansible_config().pending_cleanup_actions.pop(PENDING_START_CH, None)
    log_success(f"Started ClickHouse service at **{host}**")


def clickhouse_service_stop(host: Host) -> None:
    log_header("Stopping CH service using systemd")
    cmd = "sudo systemctl stop clickhouse-server"
    _, _, _ = run_ssh_command_with_retry(host, cmd)

    def start_clickhouse_host() -> None:
        clickhouse_service_start_and_wait(host)

    get_ansible_config().pending_cleanup_actions[PENDING_START_CH] = start_clickhouse_host
    log_success(f"Stopped the ClickHouse service at **{host}**")


class SystemdCommand(Enum):
    START = "start"
    STOP = "stop"


def wait_for_gatherer_service_command(host: Host, command: SystemdCommand) -> None:
    echo(f"* Waiting for the server to {command.value}", nl=False)
    sleep_for = 2
    ask_after_seconds = 60
    done = False
    cmd = "systemctl status tinybird-gatherer"

    def _is_done(output: str) -> bool:
        if command == SystemdCommand.START:
            return "Active: active (running)" in output

        return "CGroup: /system.slice/tinybird-gatherer.service" not in output

    while not done:
        loop_start = time.time()
        while not done and not get_ansible_config().quit and time.time() - loop_start < ask_after_seconds:
            echo(".", nl=False)
            _, output_std, _ = run_ssh_command(host, cmd)
            done = _is_done(output_std)
            if not done:
                time.sleep(sleep_for)
        echo("")

        if not done:
            log_info(f"Over **{ask_after_seconds}** seconds have passed but the server is not responding yet")
            option = do_the_prompt_with_options("How do you want to proceed?", ["wait", "abort"], default="wait")
            if option == "abort":
                log_fatal(f"User aborted waiting for Gatherer to {command.value}")


def gatherer_service_start_and_wait(host: Host) -> None:
    log_header("Starting Gatherer service using systemd")

    cmd = "sudo systemctl start tinybird-gatherer"
    _, _, _ = run_ssh_command_with_retry(host, cmd)
    wait_for_gatherer_service_command(host, SystemdCommand.START)
    get_ansible_config().pending_cleanup_actions.pop(PENDING_START_GATHERER, None)
    log_success(f"Started Gatherer service at **{host}**")


def gatherer_service_stop(host: Host) -> None:
    log_header("Stopping Gatherer service using systemd")
    cmd = "sudo systemctl stop tinybird-gatherer"
    _, _, _ = run_ssh_command_with_retry(host, cmd)
    wait_for_gatherer_service_command(host, SystemdCommand.STOP)

    def start_gatherer_host() -> None:
        gatherer_service_start_and_wait(host)

    get_ansible_config().pending_cleanup_actions[PENDING_START_GATHERER] = start_gatherer_host
    log_success(f"Stopped the Gatherer service at **{host}**")


def check_replication_status(
    host: Host,
    cluster_name: str,
    check_after_restart: bool = False,
    count_query: Callable[[str], str] = _check_replication_status_error_count_query_get,
    info_query: Callable[[str, int], str] = _check_replication_status_error_info_query_get,
) -> List[str]:
    max_table_problems = 5
    sleep_for = 2
    ask_after_seconds = 30
    iteration = 0
    loop_start = time.time()

    while True:
        iteration += 1
        must_ask: bool = False
        _, output, output_err = run_remote_query(host, count_query(cluster_name), fatal=not check_after_restart)

        output_servers = []
        response = None
        max_errors = 0
        try:
            response = json.loads(output)["data"]
            if response != []:
                output_servers = [s["host"] for s in response]
                max_errors = max([int(s["errors"]) for s in response])
        except ValueError:
            log_warning(f"Could not parse response from remote server: {output} {output_err}")
            must_ask = True
            max_errors = 1

        if max_errors == 0:
            echo("\n")
            log_success(f"No replication issues found in cluster **{cluster_name}**")
            return output_servers

        must_ask = get_ansible_config().quit or must_ask or time.time() - loop_start > ask_after_seconds

        if not must_ask:
            if iteration == 1:
                echo("* Waiting for replication", nl=False)
            echo(".", nl=False)
            time.sleep(sleep_for)
        else:
            echo("\n")
            log_info(f"Over **{ask_after_seconds}** seconds have passed but the server is not replicated yet")
            if response:
                log_warning(f"**{json.dumps(response, indent=4)}**")

            _, output, output_err = run_remote_query(
                host, info_query(cluster_name, max_table_problems), fatal=not check_after_restart
            )
            try:
                response = json.loads(output)["data"]
                log_warning(f"Error list (might be different from the previous check) (max **{max_table_problems}**): ")
                for table in response:
                    log_warning(f"**{json.dumps(table, indent=4)}**")
            except ValueError:
                log_warning(f"Could not parse response from remote server: {output} {output_err}")

            if check_after_restart:
                option = do_the_prompt_with_options(
                    "How do you want to proceed?", ["continue", "recheck"], default="recheck"
                )
                if option == "continue":
                    return output_servers
            else:
                option = do_the_prompt_with_options(
                    "How do you want to proceed?", ["continue", "recheck", "abort"], default="recheck"
                )
                if option == "continue":
                    return output_servers
                elif option == "abort":
                    log_fatal("Aborted due to replication issues")

            iteration = 0
            loop_start = time.time()


def check_fetch_replication_status(host: Host, cluster_name: str, traffic_stopped_time: float) -> None:
    def query_with_count(cluster_name: str) -> str:
        # TODO: Remove allow_experimental_analyzer = 0 when all ClickHouse are in 24.8+
        return f"""
            SELECT
                hostname() as host,
                countIf(inserts_oldest_time != 0 AND inserts_oldest_time < now() - INTERVAL '{int(time.time() - traffic_stopped_time)}' SECOND) as errors
            FROM clusterAllReplicas('{cluster_name}', system.replicas)
            GROUP BY host
            FORMAT JSON
            SETTINGS allow_experimental_analyzer = 0"""

    def query_with_info(cluster_name: str, limit: int) -> str:
        return f"""
            SELECT
                hostname() as hostname,
                database,
                table,
                queue_size,
                inserts_in_queue,
                absolute_delay,
                inserts_oldest_time
            FROM clusterAllReplicas('{cluster_name}', system.replicas)
            WHERE inserts_oldest_time != 0 AND inserts_oldest_time < now() - INTERVAL '{int(time.time() - traffic_stopped_time)}' SECOND
            LIMIT {limit}
            FORMAT JSON"""

    check_replication_status(
        host=host,
        cluster_name=cluster_name,
        check_after_restart=False,
        count_query=query_with_count,
        info_query=query_with_info,
    )


def check_ddl_replication_status(host: Host, cluster_name: str, check_after_restart: bool = False) -> None:
    def check_if_ddl_error_in_cluster(cluster_name: str) -> str:
        # We are adding a dummy query to the union to ensure we always get a result when there are no DDL operations
        return f"""
            SELECT host, sum(errors) as errors
            FROM (
                SELECT hostname() as host, 0 as errors
                UNION ALL
                SELECT
                    hostname() as host,
                    countIf(status NOT IN ('Finished', 'Removing') AND exception_code > 0) as errors
                FROM clusterAllReplicas('{cluster_name}', system.distributed_ddl_queue)
                GROUP BY host
            )
            GROUP BY host
            FORMAT JSON"""

    def get_ddl_errors_in_cluster(cluster_name: str, limit: int) -> str:
        return f"""
            SELECT
                hostname() as hostname,
                status,
                exception_code,
                exception_text,
                cluster,
                query
            FROM clusterAllReplicas('{cluster_name}', system.distributed_ddl_queue)
            WHERE (status NOT IN ('Finished', 'Removing') AND exception_code > 0)
            LIMIT {limit}
            FORMAT JSON"""

    log_info(f"Verifying the DDL replication status of cluster **{cluster_name}**")
    check_replication_status(
        host=host,
        cluster_name=cluster_name,
        check_after_restart=check_after_restart,
        count_query=check_if_ddl_error_in_cluster,
        info_query=get_ddl_errors_in_cluster,
    )

    def check_if_ddl_delayed_in_cluster(cluster_name: str) -> str:
        """
        We check if the last entry in the distributed_ddl_queue is the same in all the replicas.
        If it's not, it means that the DDL operation are delayed in some of the replicas.
        """

        return f"""
            WITH last_entries AS
            (
                SELECT
                    host,
                    max(entry) AS last_entry
                FROM clusterAllReplicas('{cluster_name}', system.distributed_ddl_queue)
                WHERE status = 'Finished'
                GROUP BY host
            )
            SELECT
                host,
                if(last_entry < (
                    SELECT max(last_entry)
                    FROM last_entries
                ), 1, 0) AS errors
            FROM last_entries
            FORMAT JSON"""

    def get_ddl_delayed_in_cluster(cluster_name: str, limit: int) -> str:
        """
        We check if the last entry in the distributed_ddl_queue is the same in all the replicas.
        """

        return f"""
            SELECT
                hostname() as hostname,
                now() as current_time,
                query_create_time,
                status,
                entry,
                exception_code,
                exception_text,
                query
            FROM clusterAllReplicas('{cluster_name}', system.distributed_ddl_queue)
            WHERE status = 'Finished'
            ORDER BY entry DESC
            LIMIT 1 BY hostname
            FORMAT JSON"""

    log_info(f"Verifying the DDL replication delay of cluster **{cluster_name}**")
    check_replication_status(
        host=host,
        cluster_name=cluster_name,
        check_after_restart=check_after_restart,
        count_query=check_if_ddl_delayed_in_cluster,
        info_query=get_ddl_delayed_in_cluster,
    )


def check_replication_status_after_restart(host: Host, main_clickhouse_cluster: str) -> None:
    log_info(f"Verifying the insert/merge replication status of cluster **{main_clickhouse_cluster}**")
    _ = check_replication_status(host, main_clickhouse_cluster, check_after_restart=True)

    check_ddl_replication_status(host, main_clickhouse_cluster, check_after_restart=True)


def check_if_server_contains_non_replicated_tables(host: Host) -> None:
    """If the server contains non replicated tables we can't safely reboot it"""

    log_header("Checking table engines")

    query = """
        SELECT
            database, engine, count()
        FROM system.tables
        WHERE
            database NOT IN ('system', 'information_schema', 'INFORMATION_SCHEMA')
            AND engine NOT IN ('Distributed', 'Kafka', 'MaterializedView', 'Null', 'StreamingQuery', 'View')
            AND engine NOT LIKE 'Replicated%'
            AND name NOT LIKE '%_aux_copy_%'
            AND name != 'tb_server_disabled'
        GROUP BY database, engine
        ORDER BY database, engine
            """
    _, output, _ = run_remote_query(host, query)
    output_databases = [line for line in output.split("\n") if line]
    if output_databases:
        log_warning("Found several **non-replicated tables** in this server:")
        for line in output_databases:
            log_warning("\t" + line)
        detailed_log = """
            If there's an operation over any non-replicated table there might be data loss.
            Keep in mind that Join tables are deprecated and therefore should be ignored.
            If there's any issue tell the customer to re-ingest the data.
        """
        log_warning(f"Restarting this server **is not safe**. {detailed_log}")
        conf = get_ansible_config()
        if conf.interactive and not prompt_for_confirmation("Do you want to continue anyway?", default=False):
            log_fatal("Can't restart the server without affecting the service")
    else:
        log_success("All table engines are ok")


def check_active_queries_in_server(
    host: Host,
    minutes_to_last_populate: int = 10,
    minutes_to_last_copy: int = 120,
    minutes_to_last_sink: int = 120,
    active_queries_pending_seconds: int = 60,
    max_active_merges: int = 12,
    max_insert_queries: int = 9999,
    dry_run: bool = False,
    is_interactive: bool = False,
) -> None:
    """Get an idea of the active queries, populates and merges"""
    # TODO: Consider informing about mutations or other background ops

    log_header("Checking running operations in this ClickHouse server")

    reload = True
    iterator = 0
    while reload:
        reload = False
        iterator += 1
        query = f"""
        SELECT * FROM
        (
            SELECT
                count() as populate_queries
            FROM system.query_log
            WHERE
                event_date >= yesterday()
                AND event_time > now() - toIntervalMinute({minutes_to_last_populate})
                AND type = 'QueryStart'
                AND http_user_agent LIKE '%populate%'
        ) populate,
        (
            SELECT
                groupUniqArray(simpleJSONExtractString(log_comment, 'job_id')) as copy_job_ids,
                length(copy_job_ids) as copies_active
            FROM system.query_log
            WHERE
                is_initial_query AND
                event_date >= yesterday() AND
                event_time > now() - toIntervalMinute({minutes_to_last_copy}) AND
                http_user_agent='tb-copy-query' AND
                type = 'QueryStart' AND
                simpleJSONExtractString(log_comment, 'job_id') != '' AND
                simpleJSONExtractString(log_comment, 'job_id') NOT IN (
                    SELECT simpleJSONExtractString(log_comment, 'job_id')
                    FROM system.query_log
                    WHERE
                        event_date >= yesterday() AND
                        event_time > now() - toIntervalMinute({minutes_to_last_copy}) AND (
                            -- Match DROP table statements with is_last_step = True
                            type > 1 AND
                            http_user_agent = 'no-tb-internal-copy-query' AND
                            query_kind='Drop' AND
                            simpleJSONExtractBool(log_comment, 'is_last_step') = true
                        )
                )
        ) copies,
        (
            SELECT
                count() as merges_active,
                max((elapsed * (1 - progress)) / progress) as merges_max_estimated_to_finish
            FROM system.merges
        ) merges,
        (
            SELECT
                count() as queries_active,
                max(estimated_remaining_time) as queries_estimated_remaining_time
            FROM
            (
                SELECT
                    least(100 * read_rows/total_rows_approx, 90) as progress_percentage,
                    elapsed,
                    (elapsed * (100 - progress_percentage)) / progress_percentage   as estimated_remaining_time
                FROM system.processes
                WHERE query_id != queryID()
            )
        ) queries,
        (
            -- 22.8 doesn't have query_kind: SELECT count() as active FROM system.processes WHERE query_kind = 'Insert'
            SELECT count() as active FROM system.processes WHERE query ilike '%insert%' AND query_id != queryID()
        ) inserts,
        (
            SELECT
                count() as sinks_active
            FROM system.query_log
            WHERE
                event_date >= yesterday()
                AND event_time > now() - toIntervalMinute({minutes_to_last_sink})
                AND type = 'QueryStart'
                AND http_user_agent='tb-datasink-query'
                AND query_id NOT IN (
                    SELECT query_id
                    FROM system.query_log
                    WHERE
                        event_date >= yesterday()
                        AND event_time > now() - toIntervalMinute({minutes_to_last_sink})
                        AND type > 1
                        AND http_user_agent='tb-datasink-query'
                )
        ) sinks,
        (
            SELECT
                count() as mutations_active
            FROM system.mutations
            WHERE not is_done
        ) mutations
        FORMAT JSON
        SETTINGS allow_experimental_analyzer = 0
        """
        _, output, output_err = run_remote_query(host, query)

        warnings: bool = False
        data: List[Dict[str, int]] = []
        try:
            data = json.loads(output)["data"]
            if len(data) != 1:
                log_warning(f"Expected one row and got {len(data)}")
                warnings = True
        except ValueError:
            log_warning(f"Could not parse response from remote server: {output} {output_err}")
            warnings = True

        if not warnings:
            response = data[0]

            def extract_prop(r: Dict[str, int], p: str) -> int:
                try:
                    return int(r[p] or 0)
                except Exception:
                    log_warning(f"Could not extract {p} from response ({r})")
                    return 999

            populate_queries = extract_prop(response, "populate.populate_queries")
            active_merges = extract_prop(response, "merges.merges_active")
            active_merges_sec = extract_prop(response, "merges.merges_max_estimated_to_finish")
            active_queries = extract_prop(response, "queries.queries_active")
            active_queries_sec = extract_prop(response, "queries.queries_estimated_remaining_time")
            active_inserts = extract_prop(response, "inserts.active")
            active_copy_jobs = extract_prop(response, "copies.copies_active")
            active_sink_jobs = extract_prop(response, "sinks.sinks_active")
            active_mutations = extract_prop(response, "mutations.mutations_active")

            log_info(f"**Populate queries** in the last {minutes_to_last_populate} minutes: **{populate_queries}**")
            if populate_queries:
                warnings = True

            log_info(f"**Active queries**: **{active_queries}**. Estimated **{active_queries_sec}** seconds to finish")
            if active_queries_sec > active_queries_pending_seconds:
                warnings = True
            if active_queries and not active_queries_pending_seconds:
                warnings = True

            log_info(f"**Active merges**: **{active_merges}**. Estimated **{active_merges_sec}** seconds to finish")
            if active_merges > max_active_merges:
                warnings = True

            log_info(f"**Active inserts**: **{active_inserts}**")
            if active_inserts > max_insert_queries:
                warnings = True

            log_info(f"**Active Copy Jobs**: **{active_copy_jobs}**")
            json_response = typing.cast(Dict[str, list[str]], response)
            active_copy_jobs_ids: list[str] = json_response.get("copies.copy_job_ids", [])
            for active_copy_job in active_copy_jobs_ids:
                log_info(f"> /v0/jobs/{active_copy_job}")
            if active_copy_jobs:
                warnings = True

            log_info(f"**Active Sinks**: **{active_sink_jobs}**")
            if active_sink_jobs:
                warnings = True

            log_info(f"**Active Mutations**: **{active_mutations}**")
            if active_mutations:
                warnings = True

        if iterator == 20 and not is_interactive:
            log_fatal(
                "Cancelling. The server has ongoing operations and it's not safe to stop without manual intervention."
            )

        if dry_run:
            log_info("Don't worry if there are running operations, will double-check after disabling CH instance")
            return

        if warnings:
            log_warning("Restarting this server with running operations might not be safe")
            option = do_the_prompt_with_options(
                "How do you want to proceed?", ["continue", "recheck", "abort"], default="recheck"
            )
            if option == "abort":
                log_fatal("Cancelling operation because the server has operations in progress")
            if option == "recheck":
                reload = True
                echo("")
        else:
            log_success("There isn't any important operation in progress")

        time.sleep(15)


def cancel_process_handler(_signum: Any, _frame: Any) -> None:  # pylint: disable=unused-argument
    secho("\n\nCANCEL REQUEST RECEIVED", err=True, fg="red")
    log_warning("Continuing until it's safe to exit")
    push_new_line_via_stdin()
    get_ansible_config().quit = True


def execute_playbook(
    playbook: str, tags: List[str], diff: bool = True, check: bool = True, skip_tags: List[str] | None = None
) -> int:
    initialize_locale()

    old_args = context.CLIARGS
    conf = get_ansible_config()
    inventory = copy.deepcopy(conf.inventory)

    skip_tags = skip_tags or []

    # Note that most, if not all, of these settings are mandatory. Most come from a StackOverflow example, some
    # from the source code of python-ansible (seeing what the CLI does) and some by pure experimentation to see what
    # worked (mostly the become* ones)
    context.CLIARGS = ImmutableDict(
        listtags=False,
        listtasks=False,
        listhosts=False,
        syntax=False,
        connection="ssh",
        timeout=10,
        module_path=None,
        forks=100,
        remote_user=None,
        private_key_file=None,
        ssh_common_args=None,
        ssh_extra_args=None,
        sftp_extra_args=None,
        scp_extra_args=None,
        become=None,
        become_method="sudo",
        become_user="root",
        verbosity=True,
        start_at_task=None,
        subset=True,
        diff=diff,
        check=check,
        tags=tags,
        skip_tags=skip_tags,
    )

    # We need a new variable manager so it reloads the config set above in the context
    new_variable_manager = VariableManager(loader=conf.loader, inventory=inventory)
    executor = PlaybookExecutor(
        playbooks=[DEPLOY_FOLDER / playbook],
        inventory=inventory,
        variable_manager=new_variable_manager,
        loader=conf.loader,
        passwords={},
    )
    result: int = executor.run()
    context.CLIARGS = old_args
    return result


@dataclass
class ValidatedClickHouseServer:
    server: str
    host: Host
    main_clickhouse_cluster: str
    has_varnish: bool


def clickhouse_validate_server_before_stop(
    server: str, is_gatherer: bool = False, ignore_dirty_repo: bool = False, is_interactive: bool = False
) -> ValidatedClickHouseServer:
    log_header("Validating if the CH service can be stopped safely")

    # We warn if there are changes in the deploy folder to avoid unexpected changes creeping in
    if not ignore_dirty_repo:
        check_git_status()

    host = get_single_ansible_host(server)
    main_clickhouse_cluster = get_host_main_clickhouse_cluster(host)
    has_varnish = False

    if not is_gatherer:
        has_varnish = True
        check_if_server_contains_non_replicated_tables(host)

    # check_active_queries_in_server(host, dry_run=True, is_interactive=False)

    ch_server = ValidatedClickHouseServer(server, host, main_clickhouse_cluster, has_varnish)
    return ch_server


def clickhouse_wait_for_fetches_before_stop(ch_server: ValidatedClickHouseServer, traffic_stopped_time: float) -> None:
    check_fetch_replication_status(ch_server.host, ch_server.main_clickhouse_cluster, traffic_stopped_time)


def clickhouse_validate_server_after_start(server: str) -> None:
    log_header("Validating if the CH service has started correctly")
    host = get_single_ansible_host(server)
    main_clickhouse_cluster = get_host_main_clickhouse_cluster(host)

    log_header("Wait for replication")
    check_replication_status_after_restart(host, main_clickhouse_cluster)


def reserve_platform_lock(host: Host, duration: str, channel: str, notes: str | None) -> None:
    log_info("Reserving platform lock")

    if not notes:
        notes = " ".join(sys.argv[1:])

    tb_region = get_host_region_inventory(host)
    resource_name = get_tb_region_from_resource_name(tb_region)

    code, resources = list_resources()
    if code != 200:
        log_fatal("failed to list platform locks")

    res = MutexBotResource(**next(r for r in resources if r["name"] == resource_name))
    if res.active_reservation:
        until = res.active_reservation.astimezone(tz=None).strftime("%d/%m/%Y, %H:%M:%S %Z")
        log_warning(
            f"Resource {res.name} has already been reserved by {res.active_reservation_user_name} until {until}. Notes: {res.active_reservation_reason}."
        )
        if get_ansible_config().interactive:
            while not prompt_for_confirmation("Is this you?", default=False):
                pass
            log_info("Cool, proceeding.")
            return

    code, message = reserve_resource(resource_name, duration, notes, channel)
    if code != 201:
        log_fatal(f"failed to reserve the platform lock:\n{message}")

    log_info(message)


def release_platform_lock(host: Host, channel: str) -> None:
    log_info("Releasing platform lock")

    tb_region = get_host_region_inventory(host)
    resource_name = get_tb_region_from_resource_name(tb_region)

    code, message = release_resource(resource_name, channel)
    if code != 200:
        if code == 208:
            log_warning("reservation was not found, please check the platform-lock channel")
            return

        log_warning(f"failed to release the platform lock:\n{message}")
        log_warning("Please release the platform lock manually: https://app.slack.com/client/T01L9DQRBAR/C04MH24K8TZ")
        if get_ansible_config().interactive:
            echo("")
            while not prompt_for_confirmation("Have you released the lock?", default=False):
                pass
        return
    log_info(message)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("server", type=STRING)
@click.argument("action", type=STRING)
@click.option("-n", "--notes", "notes", default=None, help="Add custom notes to platform lock reserve")
def platform_lock(server: str, action: str, notes: str | None) -> None:
    """
    Reserve/release resource on platform-lock channel.
    """

    host = get_single_ansible_host(server)
    if action == "reserve":
        reserve_platform_lock(host, "5h", PLATFORM_LOCK_CHANNEL, notes)
    elif action == "release":
        release_platform_lock(host, PLATFORM_LOCK_CHANNEL)


def clickhouse_apply_operations_before_stop(
    ch_server: ValidatedClickHouseServer, ignore_lock: bool, notes: str | None
) -> None:
    conf = get_ansible_config()

    if not ignore_lock:
        reserve_platform_lock(ch_server.host, "5h", PLATFORM_LOCK_CHANNEL, notes)

    if ch_server.has_varnish:
        log_header("Changing clickhouse table probe to disabled")
        check_ddl_replication_status(ch_server.host, ch_server.main_clickhouse_cluster)
        set_clickhouse_varnish_probe_to_disabled(ch_server.host)
        get_ansible_config().pending_cleanup_actions[PENDING_ENABLE_CLICKHOUSE_PROBE] = partial(
            set_clickhouse_varnish_probe_to_enabled, ch_server.host
        )
    else:
        log_success("Skipping clickhouse table probe changes since there is no varnish for this server")

    conf.cleanup_if_needed()

    # Capture Ctrl+C to undo changes if necessary
    signal.signal(signal.SIGINT, cancel_process_handler)

    log_header("Rechecking running operations")
    check_active_queries_in_server(
        ch_server.host,
        minutes_to_last_populate=1,
        minutes_to_last_copy=120,
        active_queries_pending_seconds=1,
        max_active_merges=9999,
        max_insert_queries=0,
        is_interactive=conf.interactive,
    )
    traffic_stopped_time = time.time()  # Get it after we've checked there were no INSERTS

    log_header("Waiting for all local parts to be replicated")
    if ch_server.has_varnish:
        # We now need to ensure we can safely shutdown the server. The main concern is that if this server was
        # receiving writes (or doing merges with zero copy) it might have the only copy of some data that hasn't been
        # replicated yet. If the server doesn't start again the data would be lost, and if the server takes too long
        # to restart other servers won't have the data nor they will be able to merge parts
        clickhouse_wait_for_fetches_before_stop(ch_server, traffic_stopped_time)
    else:
        log_success("Not checking replication since we don't have servers to wait for")


def clickhouse_apply_operations_after_start(ch_server: ValidatedClickHouseServer, ignore_lock: bool) -> None:
    if ch_server.has_varnish:
        log_header("Changing clickhouse table probe to enabled")
        set_clickhouse_varnish_probe_to_enabled(ch_server.host)
        get_ansible_config().pending_cleanup_actions.pop(PENDING_ENABLE_CLICKHOUSE_PROBE, None)
    else:
        log_success("Skipping clickhouse table probe changes since there is no varnish for this server")

    if not ignore_lock:
        release_platform_lock(ch_server.host, PLATFORM_LOCK_CHANNEL)

    log_header("Finished the post-start operations")


def clickhouse_validate_conf_changes(ch_server: ValidatedClickHouseServer, is_gatherer: bool = False) -> None:
    log_header("Checking ClickHouse configuration changes")

    _, output_std, _ = run_remote_query(ch_server.host, "Select version() as v FORMAT CSV", fatal=True)
    currently_installed: str = ""
    try:
        lines = output_std.splitlines()
        if len(lines) != 1:
            log_fatal(f"Failed to read currently running version ({output_std})")
        currently_installed = lines[0].rstrip().replace('"', "").rsplit(".", 1)[0]
        # Strip the build number
        currently_installed = (
            currently_installed.rsplit(".", 1)[0] if currently_installed.count(".") == 3 else currently_installed
        )
    except ValueError:
        log_fatal("Failed to check running version")

    host_vars = get_ansible_config().variable_manager.get_vars(host=ch_server.host)
    target_ch_version_variable = "clickhouse_version" if not is_gatherer else "gatherer_clickhouse_version"
    if not host_vars or target_ch_version_variable not in host_vars:
        log_fatal(f"Could not get CH version from the inventory of server **{ch_server.host}**")
    next_version = host_vars[target_ch_version_variable]
    # Strip the build number
    next_version = next_version.rsplit(".", 1)[0] if next_version.count(".") == 3 else next_version

    log_info(f"CH version installed:    **{style(currently_installed)}**")
    color = "white" if currently_installed == next_version else "yellow"
    log_info(f"CH version to install:   **{style(next_version, fg=color, bg='black')}**")


def clickhouse_prefetch_packages(ch_hosts: List[str], is_gatherer: bool = False) -> None:
    log_header("Prefetch ClickHouse packages to speed up installation")

    conf = get_ansible_config()
    conf.inventory.subset(ch_hosts)
    affected_hosts_len = len(conf.inventory._subset)
    if affected_hosts_len <= 0:
        log_fatal(
            f"Could not filter hosts for CH packages prefetch based on **{','.join(ch_hosts)}**. Found"
            f" {affected_hosts_len} hosts"
        )

    playbook = "clickhouse.yml" if not is_gatherer else "gatherer_clickhouse.yml"
    res = execute_playbook(playbook, tags=["prefetch"], diff=True, check=False)
    if res != 0:
        log_info("There was an error **APPLYING** CH prefetch (See logs above). Cancelling the operation")
        log_fatal("Execution cancelled")

    conf.inventory.subset(None)  # Reset the subset for future calls that might happen later on
    log_success("ClickHouse packages prefetched")


def clickhouse_show_config_changes(ch_servers: list[Host]) -> None:
    conf = get_ansible_config()
    conf.inventory.subset(ch_servers)

    playbook = "clickhouse.yml"
    tags = ["configuration", "install"]
    if conf.interactive and prompt_for_confirmation(
        "Do you want to only apply config (default is install and config)?", default=False
    ):
        tags.remove("install")

    res = execute_playbook(playbook, tags, diff=True, check=True)
    if res != 0:
        log_info("There was an error **CHECKING** CH changes (See logs above). Cancelling the operation")
        log_fatal("Execution cancelled")

    conf.inventory.subset(None)  # Reset the subset for future calls that might happen later on
    log_success("The changes that would be applied are above.")


def clickhouse_apply_config_changes(ch_server: ValidatedClickHouseServer, is_gatherer: bool = False) -> None:
    log_header("Reviewing ClickHouse playbook")

    conf = get_ansible_config()
    conf.inventory.subset(ch_server.server)
    # For some reason checking with conf.inventory.get_hosts() after applying the subset does not always work
    # As it sometimes returns empty while mixing the 2 patterns (`all` and the subset)
    # So we just check that the subset has one element which is what we needed anyway
    # noinspection PyProtectedMember
    affected_hosts_len = len(conf.inventory._subset)
    if affected_hosts_len != 1:
        log_fatal(
            f"Could not filter hosts for CH config based on the host **{ch_server.server}**. Found"
            f" {affected_hosts_len} hosts"
        )

    playbook = "clickhouse.yml" if not is_gatherer else "gatherer_clickhouse.yml"
    tags = ["configuration", "install"]
    if conf.interactive:
        if prompt_for_confirmation("Do you want to only apply config (default is install and config)?", default=False):
            tags.remove("install")
        res = execute_playbook(playbook, tags, diff=True, check=True)
        if res != 0:
            log_info("There was an error **REVIEWING** CH config (See logs above). Cancelling the operation")
            log_fatal("Execution cancelled")

        if not prompt_for_confirmation("Do you want to APPLY the changes shown above?", default=True):
            log_fatal("User rejected CH changes")

    res = execute_playbook(playbook, tags, diff=True, check=False)
    if res != 0:
        log_info("There was an error **CHANGING** CH config (See logs above). Cancelling the operation")
        log_fatal("Execution cancelled")

    conf.inventory.subset(None)  # Reset the subset for future calls that might happen later on
    log_success("ClickHouse changes applied")


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("server", type=STRING)
@click.option("-i", "--interactive/--no-interactive", default=True, help="Interact with the user or use safe defaults?")
@click.option("-c", "--check-only/--no-check-only", default=True, help="Should the script stop after the checks?")
@click.option("-l", "--ignore-lock/--no-ignore-lock", default=False, help="Remind about acquiring the platform lock")
@click.option("-n", "--notes", "notes", default=None, help="Add custom notes to platform lock reserve")
def clickhouse_restart(server: str, interactive: bool, check_only: bool, ignore_lock: bool, notes: str | None) -> None:
    log_warning("Are you restarting a ClickHouse instance to prevent a OOM due to a memory leak?")
    log_warning(
        f"""If true, follow the next steps:
            1. scp clickhouse/get_memory_info.sh {server}:~/
            2. ssh {server} 'sudo ./get_memory_info.sh'
            3. scp {server}:~/GENERATED_FILE_NAME.txt ~/Downloads/
            4. Upload the file to the following issue: https://gitlab.com/tinybird/analytics/-/issues/10892
        """
    )

    """Restarts a ClickHouse server safely"""
    conf = get_ansible_config(interactive)

    ch_server: ValidatedClickHouseServer = clickhouse_validate_server_before_stop(server)

    do_the_proceed_with_changes_or_exit(check_only)

    clickhouse_apply_operations_before_stop(ch_server, ignore_lock, notes)
    clickhouse_service_restart_and_wait(ch_server.host)

    clickhouse_validate_server_after_start(server)
    clickhouse_apply_operations_after_start(ch_server, ignore_lock)

    log_success("Restart completed. Thank you for flying with Tinybird airlines")
    conf.cleanup_if_needed(force_cleanup=True)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("cluster", type=STRING)
@click.option("-i", "--interactive/--no-interactive", default=True, help="Interact with the user or use safe defaults?")
@click.option("-c", "--check-only/--no-check-only", default=True, help="Should the script stop after the checks?")
@click.option("-l", "--ignore-lock/--no-ignore-lock", default=False, help="Remind about acquiring the platform lock")
@click.option(
    "-d", "--ignore-dirty-repo/--no-ignore-dirty-repo", default=False, help="Check that the repo is not dirty"
)
@click.option("-rc", "--rollback-commit", help="The commit hash to rollback in case of needed")
@click.option("-vv", "--verbose/--no-verbose", default=False, help="Prints more logs")
@click.option("-wr", "--with-rollback/--no-rollback", default=False, help="Wheter to do an automatic rollback or not")
@click.option("-n", "--notes", "notes", default=None, help="Add custom notes to platform lock reserve")
@click.option("-p", "--prefetch/--no-prefetch", default=False, help="Prefetch CH packages")
def clickhouse_cluster_apply_config(
    cluster: str,
    interactive: bool,
    check_only: bool,
    ignore_lock: bool,
    ignore_dirty_repo: bool,
    rollback_commit: str,
    verbose: bool,
    with_rollback: bool,
    notes: str | None,
    prefetch: bool,
) -> None:
    conf = get_ansible_config(interactive)
    key = "clickhouse_cluster_" + cluster
    if key not in conf.inventory.groups:
        log_fatal(f"Could not find **{key}** group in the inventory")
    cluster_hosts = conf.inventory.groups[key].get_hosts()

    if not ignore_lock:
        reserve_platform_lock(cluster_hosts[0], "5h", PLATFORM_LOCK_CHANNEL, notes)

    enable_general_exception_hook()
    do_rollback, conf, checkout_commit = _do_clickhouse_cluster_apply_config(
        cluster,
        interactive,
        check_only,
        ignore_lock,
        ignore_dirty_repo,
        verbose,
        with_rollback,
        skip_alerts=False,
        rollback_commit=rollback_commit,
        prefetch=prefetch,
    )
    if do_rollback:
        _do_clickhouse_cluster_rollback(conf, checkout_commit, cluster, verbose, prefetch)
    disable_general_exception_hook()

    if not ignore_lock:
        release_platform_lock(cluster_hosts[0], PLATFORM_LOCK_CHANNEL)


def _do_clickhouse_cluster_rollback(
    conf: AnsibleGlobalConfig, checkout_commit: str | None, cluster: str, verbose: bool, prefetch: bool
) -> None:
    if not checkout_commit:
        log_warning("Checkout commit is None, exiting")
        return
    log_warning("Applying rollback procedure")
    if conf.interactive:
        option = do_the_prompt_with_options("How do you want to proceed?", ["rollback", "finish"], default="rollback")
        if option == "finish":
            return

    current_commit = repo.head.commit.hexsha
    try:
        current_branch = repo.active_branch.name
        was_on_branch = True
        log_info(f"Original state: branch {current_branch}")
    except TypeError:
        # If it's in detached HEAD state
        was_on_branch = False
        log_info(f"Original state: detached HEAD at {checkout_commit}")

    repo.git.checkout(checkout_commit)
    log_info(f"Checked out to: {checkout_commit}")
    log_info(repo.git.diff(current_commit, checkout_commit))
    reset_ansible_config()
    _do_clickhouse_cluster_apply_config(
        cluster,
        conf.interactive,
        False,
        True,
        True,
        verbose,
        with_rollback=False,
        skip_alerts=True,
        rollback_commit=None,
        prefetch=prefetch,
    )
    if was_on_branch:
        repo.git.checkout(current_branch)
        log_info(f"Returned to branch: {current_branch}")
    else:
        repo.git.checkout(checkout_commit)
        log_info(f"Returned to commit: {checkout_commit}")


def _do_clickhouse_cluster_apply_config(
    cluster: str,
    interactive: bool,
    check_only: bool,
    ignore_lock: bool,
    ignore_dirty_repo: bool,
    verbose: bool,
    with_rollback: bool,
    skip_alerts: bool,
    rollback_commit: Optional[str],
    prefetch: bool,
) -> Tuple[bool, AnsibleGlobalConfig, str | None]:
    """Applies new CH config (or package version changes) to a cluster safely"""
    conf = get_ansible_config(interactive)

    do_rollback = False
    checkout_commit = None

    key = "clickhouse_cluster_" + cluster
    if key not in conf.inventory.groups:
        log_fatal(f"Could not find **{key}** group in the inventory")
    cluster_hosts = conf.inventory.groups[key].get_hosts()

    # Check that the repo is clean -- otherwise the rollback might overwrite user changes
    if not ignore_dirty_repo:
        if repo.is_dirty(index=True, working_tree=True, untracked_files=False, submodules=True, path=REPO_ROOT):
            log_fatal(
                "The repo contains **uncommitted changes**. Please commit or stash them, otherwise they might be overwritten by the rollback process"
            )
        if repo.is_dirty(index=True, working_tree=True, untracked_files=True, submodules=True, path=REPO_ROOT):
            log_warning(
                "The repo contains **untracked files**. Please take into account that they might be overwritten by the rollback process"
            )
            do_the_anyways_or_exit("User cancelled due to the presence of untracked files")

    if not check_only:
        # Provision the cluster-level alerts
        log_header("Provisioning alerts for all cluster replicas")
        cluster_hosts_str = list(map(str, cluster_hosts))
        _provision_alerts(cluster_hosts_str, None, REPO_ROOT / "grafana/alerts/upgrades-all-cluster")
        conf.pending_cleanup_actions[DEPROVISION_ALERTS] = partial(
            _deprovision_alerts, cluster_hosts_str, None, ["CH upgrades", "CH upgrades/post-upgrade"]
        )
        log_info("Alerts provisioned")

        # Prefetch CH packages in all cluster replicas
        cluster_hosts_str = list(map(str, cluster_hosts))
        log_header(f"Prefetch CH packages in all servers: {','.join(cluster_hosts_str)}")
        if prefetch:
            clickhouse_prefetch_packages(cluster_hosts)
    else:
        clickhouse_show_config_changes(cluster_hosts)
        log_success("Run with --no-check-only to apply these changes")
        return do_rollback, conf, checkout_commit

    # Upgrade replicas
    for _i, host in enumerate(cluster_hosts):
        if do_rollback:
            break
        log_header(f"{host}: validating if the CH service can be modified safely")
        ch_server: ValidatedClickHouseServer = clickhouse_validate_server_before_stop(
            host, ignore_dirty_repo=ignore_dirty_repo, is_interactive=conf.interactive
        )
        clickhouse_validate_conf_changes(ch_server)

        do_the_proceed_with_changes_or_exit(check_only)

        # Disable alerts for this replica
        cluster_alerts_group = get_alert_group("CH upgrades")
        if cluster_alerts_group is not None:
            deprovision_alerts_for_replica(str(host), cluster_alerts_group["rules"])

        # always ignore lock here as we reserved previously
        clickhouse_apply_operations_before_stop(ch_server, True, None)

        with ch_is_down_silenced(str(ch_server.host)):
            clickhouse_service_stop(ch_server.host)
            clickhouse_apply_config_changes(ch_server)

            # Provision all-cluster alerts again
            _provision_alerts(str(host), None, REPO_ROOT / "grafana/alerts/upgrades-all-cluster")
            # Provision post-upgrade alerts for this replica
            _provision_alerts(
                str(host),
                None,
                REPO_ROOT / "grafana/alerts/post-upgrade",
                extra_vars={"upgrade_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")},
            )

            clickhouse_service_start_and_wait(ch_server.host, verbose=verbose)
        # Check replication status
        clickhouse_validate_server_after_start(ch_server.server)
        # Re-enable CH instance and avoid releasing the lock (done at the end of the process)
        clickhouse_apply_operations_after_start(ch_server, ignore_lock=True)

        log_success(f"Config changes applied for {host}. Waiting 3 minutes to check alerts.")
        time.sleep(3 * 60)

        while True:
            if do_rollback or skip_alerts:
                break
            # Cluster-level alerts
            cluster_alerts = get_alerts_status("CH upgrades") or []
            # Post-upgrade alerts
            post_upgrade_alerts = get_alerts_status("CH upgrades/post-upgrade") or []
            all_alerts = cluster_alerts + post_upgrade_alerts

            def _keyfunc(x: Any) -> Any:
                labels = x["labels"]
                return labels.get("replica", labels.get("instance", None))

            # TODO: the alerts should have a link to a panel/explore query to check them
            all_alerts = [
                ca
                for ca in all_alerts
                if not ca["state"].startswith("Normal") and ca["labels"]["replica"] == str(ch_server.host)
            ]
            for instance, alerts in itertools.groupby(sorted(all_alerts, key=_keyfunc), _keyfunc):
                log_warning(f"Alerts failing for {instance}:")
                for alert in alerts:
                    log_info(f"  - {alert['labels']['alertname']}: {alert['state']}")

            if all_alerts:
                log_warning("There are alerts **failing** for the cluster, please review them")
            else:
                log_info("All alerts are in normal state")
                if not conf.interactive:
                    break
            if conf.interactive:
                option = do_the_prompt_with_options(
                    "How do you want to proceed?", ["continue", "recheck", "rollback"], default="recheck"
                )
                if option == "continue":
                    break
                elif option == "rollback":
                    if not with_rollback:
                        log_warning("To do a rollback use the --with-rollback flag")
                        break
                    else:
                        checkout_commit = get_rollback_commit(repo, rollback_commit)
                        if checkout_commit:
                            do_rollback = True
                            break
            else:
                try:
                    if not with_rollback:
                        log_warning("To do a rollback use the --with-rollback flag")
                        break
                    else:
                        checkout_commit = get_rollback_commit(repo, rollback_commit)
                        if checkout_commit:
                            do_rollback = True
                            break
                except Exception as e:
                    log_fatal(str(e))

    if not do_rollback:
        log_success("Config changes applied. Thank you for flying with Tinybird airlines")
    conf.pending_cleanup_actions.pop(DEPROVISION_ALERTS)()
    conf.cleanup_if_needed(force_cleanup=True)

    return do_rollback, conf, checkout_commit


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("server", type=STRING)
@click.option("-l", "--ignore-lock/--no-ignore-lock", default=False, help="Remind about acquiring the platform lock")
@click.option("-c", "--check-only/--no-check-only", default=True, help="Should the script stop after the checks?")
@click.option("-n", "--notes", "notes", default=None, help="Add custom notes to platform lock reserve")
def clickhouse_stop(server: str, check_only: bool, ignore_lock: bool, notes: str | None) -> None:
    """Stop CH server safely"""
    ch_server: ValidatedClickHouseServer = clickhouse_validate_server_before_stop(server=server)

    do_the_proceed_with_changes_or_exit(check_only)

    clickhouse_apply_operations_before_stop(ch_server, ignore_lock, notes)
    clickhouse_service_stop(ch_server.host)

    log_success("Done. Thank you for flying with Tinybird airlines")


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("server", type=STRING)
@click.option("-c", "--check-only/--no-check-only", default=True, help="Should the script stop after the checks?")
def clickhouse_start(server: str, check_only: bool) -> None:
    """Start CH server safely"""
    host = get_single_ansible_host(server)

    do_the_proceed_with_changes_or_exit(check_only)

    clickhouse_service_start_and_wait(host)

    clickhouse_validate_server_after_start(server)

    log_success("Done. Thank you for flying with Tinybird airlines")


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("server", type=STRING)
def clickhouse_status(server: str) -> None:
    """Check CH server status"""
    host = get_single_ansible_host(server)

    clickhouse_service_status(host, False)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("server", type=STRING)
@click.option("-i", "--interactive/--no-interactive", default=True, help="Interact with the user or use safe defaults?")
@click.option("-c", "--check-only/--no-check-only", default=True, help="Should the script stop after the checks?")
@click.option("-l", "--ignore-lock/--no-ignore-lock", default=False, help="Remind about acquiring the platform lock")
@click.option("-n", "--notes", default=None, help="Add custom notes to platform lock reserve")
@click.option("-p", "--prefetch/--no-prefetch", default=False, help="Prefetch CH packages")
def clickhouse_apply_config(
    server: str, interactive: bool, check_only: bool, ignore_lock: bool, notes: str | None, prefetch: bool
) -> None:
    """Applies new CH config (or package version changes) to a server safely"""
    conf = get_ansible_config(interactive)

    log_header("Validating if the CH service can be modified safely")
    ch_server: ValidatedClickHouseServer = clickhouse_validate_server_before_stop(server)

    clickhouse_validate_conf_changes(ch_server)

    do_the_proceed_with_changes_or_exit(check_only)

    if prefetch:
        clickhouse_prefetch_packages([ch_server.server])

    clickhouse_apply_operations_before_stop(ch_server, ignore_lock, notes)
    with ch_is_down_silenced(str(ch_server.host)):
        clickhouse_service_stop(ch_server.host)
        clickhouse_apply_config_changes(ch_server)
        clickhouse_service_start_and_wait(ch_server.host)

    clickhouse_validate_server_after_start(ch_server.server)
    clickhouse_apply_operations_after_start(ch_server, ignore_lock)

    log_success("Config changes applied. Thank you for flying with Tinybird airlines")
    conf.cleanup_if_needed(force_cleanup=True)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("server", type=STRING)
@click.option("-i", "--interactive/--no-interactive", default=True, help="Interact with the user or use safe defaults?")
@click.option("-c", "--check-only/--no-check-only", default=True, help="Should the script stop after the checks?")
@click.option("-l", "--ignore-lock/--no-ignore-lock", default=False, help="Remind about acquiring the platform lock")
@click.option("-n", "--notes", default=None, help="Add custom notes to platform lock reserve")
@click.option("-p", "--prefetch/--no-prefetch", default=False, help="Prefetch CH packages")
def gatherer_apply_config(
    server: str, interactive: bool, check_only: bool, ignore_lock: bool, notes: str | None, prefetch: bool
) -> None:
    """Applies new Gatherer's CH config (or package version changes) to a server safely"""
    conf = get_ansible_config(interactive)

    log_header("Validating if the CH service can be modified safely")
    ch_server: ValidatedClickHouseServer = clickhouse_validate_server_before_stop(server, is_gatherer=True)
    clickhouse_validate_conf_changes(ch_server, is_gatherer=True)

    if check_only:
        secho("")
        log_success("Checks finished. Remember you can use --no-check-only to apply the changes")
        sys.exit(0)

    if not ignore_lock:
        reserve_platform_lock(ch_server.host, "5h", "auto-lock by colibri", PLATFORM_LOCK_CHANNEL)

    gatherer_service_stop(ch_server.host)

    clickhouse_apply_operations_before_stop(ch_server, ignore_lock, notes)
    with ch_is_down_silenced(str(ch_server.host)):
        clickhouse_service_stop(ch_server.host)
        if prefetch:
            clickhouse_prefetch_packages([ch_server.server], is_gatherer=True)
        clickhouse_apply_config_changes(ch_server, is_gatherer=True)
        clickhouse_service_start_and_wait(ch_server.host)

    gatherer_service_start_and_wait(ch_server.host)

    if not ignore_lock:
        release_platform_lock(ch_server.host, PLATFORM_LOCK_CHANNEL)

    log_success("Config changes applied. Thank you for flying with Tinybird airlines")
    conf.cleanup_if_needed(force_cleanup=True)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("server", type=STRING)
@click.argument("instance_type", type=STRING)
@click.option("-p", "--project", default="stddevco", help="Project where to do the operation")
@click.option("-i", "--interactive/--no-interactive", default=True, help="Interact with the user or use safe defaults?")
@click.option("-c", "--check-only/--no-check-only", default=True, help="Should the script stop after the checks?")
@click.option("-l", "--ignore-lock/--no-ignore-lock", default=False, help="Remind about acquiring the platform lock")
@click.option("-n", "--notes", "notes", default=None, help="Add custom notes to platform lock reserve")
def clickhouse_gcp_resize(
    server: str,
    instance_type: str,
    project: str,
    interactive: bool,
    check_only: bool,
    ignore_lock: bool,
    notes: str | None,
) -> None:
    """
    Resize a CH instance in GCP safely
    """
    conf = get_ansible_config(interactive)

    ch_server: ValidatedClickHouseServer = clickhouse_validate_server_before_stop(server)
    do_the_proceed_with_changes_or_exit(check_only)

    clickhouse_apply_operations_before_stop(ch_server, ignore_lock, notes)
    with ch_is_down_silenced(str(ch_server.host)):
        clickhouse_service_stop(ch_server.host)

        zone = get_zone_from_name_gcp(project, server)
        if zone and prompt_for_confirmation(f"We are going to stop, resize and start {server}. Are you sure?"):
            stop_instance_gcp(project, zone, server)
            scale_instance_gcp(project, zone, server, instance_type)
            start_instance_gcp(project, zone, server)

        clickhouse_service_start_and_wait(ch_server.host)

    clickhouse_validate_server_after_start(ch_server.server)
    clickhouse_apply_operations_after_start(ch_server, ignore_lock)

    log_success("Restart completed. Thank you for flying with Tinybird airlines")
    conf.cleanup_if_needed(force_cleanup=True)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("server", type=STRING)
@click.argument("instance_type", type=STRING)
@click.option("-i", "--interactive/--no-interactive", default=True, help="Interact with the user or use safe defaults?")
@click.option("-c", "--check-only/--no-check-only", default=True, help="Should the script stop after the checks?")
@click.option("-l", "--ignore-lock/--no-ignore-lock", default=False, help="Remind about acquiring the platform lock")
@click.option("-n", "--notes", "notes", default=None, help="Add custom notes to platform lock reserve")
def clickhouse_aws_resize(
    server: str,
    instance_type: str,
    interactive: bool,
    check_only: bool,
    ignore_lock: bool,
    notes: str | None,
) -> None:
    """
    Resize a CH instance in AWS safely
    """
    conf = get_ansible_config(interactive)

    ch_server: ValidatedClickHouseServer = clickhouse_validate_server_before_stop(server)
    do_the_proceed_with_changes_or_exit(check_only)

    clickhouse_apply_operations_before_stop(ch_server, ignore_lock, notes)
    with ch_is_down_silenced(str(ch_server.host)):
        clickhouse_service_stop(ch_server.host)

    if server.startswith("aws-wadus"):
        aws_profile = "development"
    else:
        aws_profile = "production"
        log_info(f"Searching instance `{server}` using AWS profile `{aws_profile}`...")
        instances = find_instance_id_and_region_aws(server, aws_profile=aws_profile)
        stopped = False
        try:
            if not instances:
                raise Exception(f"Instance '{server}' not found")

            if len(instances) > 1:
                raise Exception(
                    f"Found {len(instances)} instances with the name '{server}' in the following regions {[i[1] for i in instances]}, expected only one instance in one region."
                )

            region = instances[0][0]
            instance_id = instances[0][1]
            if prompt_for_confirmation(
                f"We are going to stop, resize to {instance_type} and start {server}. Are you sure?"
            ):
                stopped = stop_instance_aws(region, instance_id, aws_profile)
                scale_instance_aws(region, instance_id, instance_type, aws_profile)
        except Exception as e:
            log_error(f"Error resizing instance {server}: {e}")
        finally:
            if stopped:
                start_instance_aws(region, instance_id, aws_profile)

        clickhouse_service_start_and_wait(ch_server.host)

    clickhouse_validate_server_after_start(ch_server.server)
    clickhouse_apply_operations_after_start(ch_server, ignore_lock)

    log_success("Restart completed. Thank you for flying with Tinybird airlines")
    conf.cleanup_if_needed(force_cleanup=True)


@click.command(hidden=True)
@click.argument("server", type=STRING)
@click.option(
    "-t", "--disk-type", default="balanced", type=Choice(["standard", "balanced", "ssd"], case_sensitive=False)
)
def change_gcp_server_disk(server: str, disk_type: str) -> None:
    """
    Changes the type of a disk for a GCP server. Only works on single disk servers.

    [WARNING] This script shutdowns the server.\n
    [WARNING] Currently only the platform team has the needed permissions to execute the script.

    \b
    It is not possible to do this on the fly on GCP, this is the procedure:
     - Shutdown the server
     - Create a snapshot for the boot disk
     - Create a disk from the snapshot
     - Delete the snapshot
     - Detach the disk from the machine an attach the new one
     - Start the server

    The old disk will be left unchanged, to be able to rollback the operation (manually)
    """
    log_info(f"Changing the disk of the server {server} to be a {disk_type} disk")
    if not prompt_for_confirmation(
        "[WARNING] " + style("Is the server already out of production?"),
        default=False,
    ):
        return
    log_info("Starting disk migration")
    migrate_server_disk(server, disk_type)
    log_success("Disk migration completed. Have a nice day")

    confirm(
        "[WARNING] "
        + style(
            "The snapshot schedules are lost on this operation, if this was a ClickHouse writer please restore it"
            " manually?",
            fg="yellow",
            bg="black",
            blink=True,
        ),
        default=False,
    )


def human_to_gib(human: str) -> float:
    human = human.strip()
    try:
        size = float(human)
        return size
    except ValueError:
        pass  # Contained a unit

    if "G" in human:
        unit = 1
    elif "T" in human:
        unit = 1024
    else:
        raise ValueError("Didn't recognize unit")

    return float(human.rstrip("GTiB").strip()) * unit


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("server", type=STRING)
def resize_azure_server_disk(server: str) -> None:
    """
    Resizes a disk of an Azure server.

    [WARNING] This script restarts the vm.\n

    \b
    It is not possible to do this on the fly on Azure, this is the procedure:
     - Deallocates (stops) the server
     - Resize the disk
     - Starts the server again
     - Data disk: resize the partition on the disk
    """

    log_warning("💡 IMPORTANT: this script restarts the vm, please be sure to take it out of production use")

    disks_info = list_server_data_disks(server)
    secho("These are the data disks present in the machine:(name: size)", bold=True)
    for name, size in disks_info:
        echo(f"{name}: {size}GB")

    secho("\nWhich disk do you wish to resize?", bold=True)
    chosen_name = str(prompt_for_choice([disk_info[0] for disk_info in disks_info]))
    chosen_disk = next(di for di in disks_info if di[0] == chosen_name)

    new_size = click.prompt("Enter the new size for the disk, in GB", type=int)

    if new_size <= chosen_disk[1]:
        log_warning("Disk partition downsizing is not supported")
        return

    secho(f"\nThis will resize {chosen_name} from {chosen_disk[1]}GB to {new_size}GB\n", bold=True)
    if not prompt_for_confirmation("Do you want to proceed with these changes?"):
        sys.exit()

    echo("good")
    lun = resize_server_disk_azure(server, chosen_disk[0], new_size)

    # resize partition for data disk
    if lun != 100:
        echo("resizing partition...")
        ret_code, stdout, stderr = run_ssh_command_with_retry(server, f"lsscsi 1:0:0:{lun} -b --size")

        vm_disks = parse_lsscsi_output(stdout)
        if len(vm_disks) != 1:
            log_error(
                "0 or more than 1 disk is returned. Please contact Fast Responders or Platform Team for assistance"
            )
            sys.exit()

        _san, dev, _size = vm_disks[0]

        # This command has been seen to time out with 300s
        ret_code, stdout, stderr = run_ssh_command_with_retry(server, f"sudo growpart {dev} 1", timeout=1800)
        ret_code, stdout, stderr = run_ssh_command_with_retry(server, f"sudo resize2fs {dev}1")
        echo("complete")

    # summarize the actions taken
    echo(f"Resized {chosen_name} from {chosen_disk[1]}GB to {new_size}GB")


def _get_server_disk_info(server: str) -> List[ServerDisk]:
    disk_id_prefixes = ("scsi-0Google_PersistentDisk_", "nvme-Amazon_Elastic_Block_Store_")
    host = get_single_ansible_host(server)
    _, stdout, _ = run_ssh_command_with_retry(host, "sudo lsblk -J -l -b -o NAME,FSTYPE,SIZE,MOUNTPOINT")
    disks_info = json.loads(stdout)["blockdevices"]

    _, stdout, _ = run_ssh_command_with_retry(host, "sudo df --output=size,used,target -B1| awk '(NR>1)'")
    disks_size_used_list = [i for i in stdout.split("\n") if i != ""]
    disks_used = dict()
    disks_size = dict()
    for element in disks_size_used_list:
        size, used, mountpoint = element.split()
        disks_used.update({mountpoint: used})
        disks_size.update({mountpoint: size})

    _, stdout, _ = run_ssh_command_with_retry(
        host, "ls /dev/disk/by-id | xargs -I{} bash -c 'echo \"{} $(readlink -f /dev/disk/by-id/{})\"'"
    )
    disks_ids_list = [i for i in stdout.split("\n") if i != ""]

    disks_ids = dict()
    for element in disks_ids_list:
        v, k = element.split()
        if v.startswith(disk_id_prefixes):
            disks_ids.update({k.strip("/dev"): v})
    return [
        ServerDisk(
            server,
            item["name"],
            item["fstype"],
            int(disks_size[item["mountpoint"]]) if item["mountpoint"] in disks_size else 0,
            item["mountpoint"],
            int(disks_used[item["mountpoint"]]) if item["mountpoint"] in disks_used else 0,
            disks_ids.get(item["name"], ""),
        )
        for item in disks_info
    ]


def _create_pretty_table() -> PrettyTable:
    x = PrettyTable(
        horizontal_char="─",
        vertical_char="│",
        junction_char="┼",
        top_junction_char="┬",
        right_junction_char="┤",
        left_junction_char="├",
        bottom_junction_char="┴",
        bottom_right_junction_char="┘",
        bottom_left_junction_char="└",
        top_left_junction_char="┌",
        top_right_junction_char="┐",
    )
    x.align = "l"
    return x


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("server", type=STRING)
def resize_gcp_server_disk(server: str) -> None:
    """
    Resizes a disk of an GCP server.
    """

    secho(f"Resizing disk for server: {server}", bg="blue", fg="white")
    disks_info = _get_server_disk_info(server)
    disks_ext4 = sorted([i for i in disks_info if i.fstype == "ext4" and i.name != "md0"], key=lambda x: x.name)

    for disk_info in disks_ext4:
        project = "stddevco"
        zone = get_zone_from_name_gcp(project, disk_info.server)
        disk_info.add_cloud_project_id(project)
        disk_info.add_cloud_disk_zone(zone)
        disk = get_server_disk_gcp(disk_info)
        disk_info.add_cloud_size(disk.size_gb)
        disk_info.add_cloud_size(disk.size_gb)
        disk_info.add_cloud_disk_name(disk.name)
    echo("These are the data disks present in the machine:")
    x = _create_pretty_table()
    x.field_names = ["Name", "Mountpoint", "Filesystem Size", "Cloud Size", "% Used"]

    for di in disks_ext4:
        x.add_row(
            [di.cloud_disk_name, di.mountpoint, format_size(di.size, binary=True), f"{di.cloud_size} GB", di.perc_used]
        )
    echo(x.get_formatted_string(out_format="text"))

    if len(disks_ext4) > 1:
        log_warning("💡 You should ignore the root disk, since it should not be used for storing data")
        log_warning(
            """💡 Remember that ClickHouse chooses the disks based on free space:
    - If all the disk are the same size, try to resize all of them.
    - Otherwise, resize the the smaller one."""
        )

    if len(disks_ext4) > 1:
        secho("\nWhich disk do you wish to resize?", bold=True)
    chosen_name = str(prompt_for_choice([disk_info.cloud_disk_name for disk_info in disks_ext4]))

    chosen_disk = next(part for part in disks_ext4 if part.cloud_disk_name == chosen_name)

    secho("\nDo you want to set a fixed size or a percentage", bold=True)
    size_option = prompt_for_choice(["Set cloud disk size", "Set target usage percentage for filesystem"])
    if size_option == "Set cloud disk size":
        prompt_text = "Enter the cloud disk new size (in GiB)"
    else:
        prompt_text = "Enter the new usage percentage for filesystem"
    new_size_prompt = prompt_for_input(prompt_text)

    ext4_overhead_gb = chosen_disk.cloud_size - (chosen_disk.size >> 30)

    if size_option == "Set target usage percentage for filesystem":
        new_size_bytes = int((chosen_disk.used * 100) // int(new_size_prompt)) + (ext4_overhead_gb << 30)
    else:
        try:
            new_size_bytes = int(new_size_prompt) << 30
        except InvalidSize:
            log_warning("Invalid Size")
            sys.exit()

    new_size_gb = new_size_bytes >> 30  # must be integer and in GB for the AWS API

    if new_size_gb <= chosen_disk.cloud_size:
        log_warning("Disk partition downsizing is not supported")
        sys.exit()

    # Present the user a confirmation dialog
    percent_increase = (new_size_bytes / chosen_disk.size - 1) * 100
    echo(
        f"This will resize {chosen_disk.cloud_disk_name} from {chosen_disk.cloud_size} GB to"
        f" {new_size_gb} GB (a {percent_increase:.2f} % increase)"
    )
    if not prompt_for_confirmation("Do you want to proceed with these changes?"):
        sys.exit()

    if percent_increase >= 20 and not prompt_for_confirmation("This increase is more than 20 %, do you confirm again?"):
        sys.exit()

    echo("This will take some time")

    resize_server_disk_gcp(chosen_disk, new_size_gb)

    # Resize the partition and the filesystem
    base_device = chosen_disk.name.rstrip(string.digits).rstrip("p")
    # This command has been seen to time out with 300s
    ret_code, stdout, stderr = run_ssh_command_with_retry(server, f"sudo growpart /dev/{base_device} 1", timeout=1800)
    ret_code, stdout, stderr = run_ssh_command_with_retry(server, f"sudo resize2fs /dev/{chosen_disk.name}")

    # Summarize the actions taken
    echo(
        f"Resized {chosen_disk.cloud_disk_name} from {chosen_disk.cloud_size} GB to {new_size_gb} GB (a"
        f" {percent_increase:.2f} %)"
    )


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("server", type=STRING)
def resize_aws_server_disk(server: str) -> None:
    """
    Resizes a disk of an AWS server. Needs AWS_PROFILE exported.
    """

    # List partitions as seen from the host machine
    host = get_single_ansible_host(server)
    aws_region = host.get_vars()["placement"]["region"]
    ret_code, stdout, stderr = run_ssh_command_with_retry(host, "lsblk -J -l -o NAME,FSTYPE,SIZE,MOUNTPOINT,FSUSE%")
    disks_info = json.loads(stdout)["blockdevices"]
    ext4_partitions = [di for di in disks_info if di["fstype"] == "ext4" and "nvme" in di["name"]]
    echo("These are the data disks present in the machine:")
    for di in ext4_partitions:
        echo(f"{di['name']}\t{di['size']}")

    # Ask the user to select a partition
    chosen_partition_name = do_the_prompt_with_options(
        "Which disk do you wish to resize?",
        [disk_info["name"] for disk_info in ext4_partitions],
        default=ext4_partitions[0]["name"],
    )
    chosen_partition = next(part for part in ext4_partitions if part["name"] == chosen_partition_name)

    # Show the user the current usage of the FS in the partition
    ret_code, stdout, stderr = run_ssh_command_with_retry(
        host, f"sudo df -ht ext4 {chosen_partition['mountpoint']} | tail -n +2"
    )
    partition_info = stdout.strip().split()

    log_info(f"The current usage for this partition's filesystem is {partition_info[4]}")

    # Ask the user for the new size
    new_size = click.prompt("Enter the new size for the disk, in GiB or as a target occupation percentage (e.g. 80 %)")

    chosen_partition_size = human_to_gib(chosen_partition["size"])

    if new_size.strip().endswith("%"):
        new_size = float(new_size.strip().rstrip("%"))
        new_size = float(partition_info[4].rstrip("%")) * chosen_partition_size / new_size
    else:
        new_size = human_to_gib(new_size)
    new_size = math.ceil(new_size)  # must be integer for the AWS API

    if new_size <= chosen_partition_size:
        log_warning("Disk partition downsizing is not supported")
        return

    # Present the user a confirmation dialog
    percent_increase = (new_size / chosen_partition_size - 1) * 100
    echo(
        f"This will resize {chosen_partition_name} from {chosen_partition_size} GiB to {new_size} GiB (a"
        f" {percent_increase:.2f} % increase)"
    )
    if not confirm(style("Do you want to proceed with these changes?", blink=False), default=False):
        return

    if percent_increase >= 20 and not confirm(
        style("This increase is more than 20 %, do you confirm again?", blink=False), default=False
    ):
        return

    echo("This will take some time")

    # Find the volume id of the chosen partition
    ret_code, stdout, stderr = run_ssh_command_with_retry(
        host, "ls /dev/disk/by-id | xargs -I{} bash -c 'echo \"{} $(readlink -f /dev/disk/by-id/{})\"'"
    )

    volume_devices = [line.split() for line in stdout.splitlines()]
    volume_device = next(x[0] for x in volume_devices if chosen_partition_name in x[1])
    start_id = volume_device.find("vol") + 3
    volume_id = "vol-" + volume_device[start_id : start_id + 17]

    if server.startswith("aws-wadus"):
        aws_profile = "development"
    else:
        aws_profile = "production"
    # Do the actual resizing of the volume
    resize_disk_aws(volume_id, new_size, aws_region, aws_profile)
    # Resize the partition and the filesystem
    base_device = chosen_partition_name.rstrip(string.digits).rstrip("p")
    # This command has been seen to time out with 300s
    ret_code, stdout, stderr = run_ssh_command_with_retry(host, f"sudo growpart /dev/{base_device} 1", timeout=1800)
    ret_code, stdout, stderr = run_ssh_command_with_retry(host, f"sudo resize2fs /dev/{chosen_partition_name}")

    # Summarize the actions taken
    echo(
        f"Resized {chosen_partition_name} from {chosen_partition_size} GiB to {new_size} GiB (a"
        f" {percent_increase:.2f} %)"
    )


def list_database_tables(host: str, database: str, only_replicated_tables: bool = True) -> Dict[str, Any]:
    only_replicated_tables_cond = "AND engine LIKE 'Replicated%'"
    list_tables_query = f"""
    SELECT
        name,
        extract(create_table_query, 'ENGINE\\s+=\\s+(\\w+)') as engine,
        extract(engine_full, '\\'([^\\']*)\\'') as replication_path,
        create_table_query
    FROM system.tables
    WHERE
        database = '{database}'
        {only_replicated_tables_cond if only_replicated_tables else ''}
    FORMAT JSON
    """
    _, output, output_err = run_remote_query(host, list_tables_query)
    data: Dict[str, Any] = json.loads(output)["data"]
    return data


def print_query(host: str, query: str) -> Tuple[None, None, None]:
    """
    For implementing --check-only.
    """
    echo(style(f"Would execute on {host}", "green"))
    echo(query)

    return None, None, None


@dataclass
class S3Backup:
    endpoint: str


@dataclass
class AzureBackup:
    sa_endpoint: str
    container: str
    name: str


def parse_backup_name(name: str) -> S3Backup | AzureBackup:
    if name.startswith("S3"):
        return S3Backup(name.split("'")[1])
    else:
        return AzureBackup(*name.split("'")[1::2])


def get_s3_query(endpoint: str, access_key: str, secret_key: str) -> str:
    if access_key is None:
        return f"S3('{endpoint}')"
    return f"S3('{endpoint}', '{access_key}', '{secret_key}')"


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("host", type=STRING)
@click.argument("database", type=STRING)
@click.option("-t", "--table", type=STRING, required=False, multiple=True)
@click.option(
    "-d",
    "--no-allow-old-schema/--allow-old-schema",
    default=True,
    help="Should the script restore a table that doesn't exist currently?",
)
@click.option("--backup-endpoint", required=False, type=STRING, help="S3 backup endpoint")
@click.option("--s3-access-key", required=False, type=STRING, help="HMAC access key for GCP servers")
@click.option("--s3-secret-key", required=False, type=STRING, help="HMAC secret key for GCP servers")
@click.option("--replicated", required=False, is_flag=True, help="Whether to create tables as replicated")
@click.option("-c", "--check-only/--no-check-only", default=True, help="Should the script stop after the checks?")
def restore_clickhouse_database(
    host: str,
    database: str,
    table: str,
    backup_endpoint: str,
    s3_access_key: str,
    s3_secret_key: str,
    replicated: bool,
    check_only: bool,
    no_allow_old_schema: bool,
) -> None:
    """
    Restore a database backup made by the scheduler on a ClickHouse server.
    """
    _run_remote_query: Callable[[str, str], Any] = print_query if check_only else run_remote_query
    cluster = get_host_main_clickhouse_cluster(host)

    if not backup_endpoint:
        query = f"""
            SELECT
                rowNumberInAllBlocks() + 1 as number,
                name,
                id,
                start_time,
                formatReadableSize(uncompressed_size) AS size
            FROM clusterAllReplicas({cluster}, merge(system, 'backup_log*'))
            WHERE (length(id) = 26) AND (status = 'BACKUP_CREATED') AND (start_time >= (now() - toIntervalDay(7)))
            ORDER BY start_time DESC
            FORMAT JSON
        """
        _, output, output_err = run_remote_query(host, query)

        response = json.loads(output)["data"]
        t = _create_pretty_table()
        t.field_names = ["Number", "ID", "Start time", "Size"]
        for row in response:
            t.add_row([row["number"], row["id"], row["start_time"], row["size"]])

        echo("Backups in the last week")
        echo(t.get_formatted_string(out_format="text"))

        to_restore = click.prompt("Enter the number of the backup that you wish to restore")
        to_restore = next(row for row in response if row["number"] == to_restore)

        s3_backup_endpoint = parse_backup_name(to_restore["name"])
    else:
        s3_backup_endpoint = S3Backup(backup_endpoint)

    # Give warning about what this implies and ask for confirmation
    if not check_only and not prompt_for_confirmation(
        "This will delete the current data on the database (including MVs). Are you sure you want to continue with the process?",
        default=False,
    ):
        log_fatal("User cancelled")

    # This is most likely not the best model for authentication but it will serve for
    # development, since for now this is to be used exclusively for testing by the platform team
    if isinstance(s3_backup_endpoint, AzureBackup):
        log_fatal("Restoring Azure backups with colibri is not supported yet")

    if (not s3_access_key or not s3_secret_key) and (host.startswith("tb-") or host.startswith("gcp-")):
        s3_access_key = click.prompt("Please provide the access key")
        s3_secret_key = click.prompt("Please provide the secret key")

    if isinstance(s3_backup_endpoint, S3Backup):
        log_info("Opening backup, this might take a long time")
        backup = open_backup(S3(s3_backup_endpoint.endpoint, s3_access_key, s3_secret_key))  # type: ignore
        log_info("Opened backup successfully")

    # List tables from the target database in order to recreate them with a new replication path
    if not table:
        tables = backup.get_tables(database=database)
        tables = [{"name": t, "create_query": backup.get_create_query(database=database, table=t)} for t in tables]
    else:
        tables = [{"name": t, "create_query": backup.get_create_query(database=database, table=t)} for t in table]

    # Create a new database for the new tables
    suffix = "_" + str(uuid.uuid4()).replace("-", "_")
    uuid_regex = re.compile("_\\w{8}_\\w{4}_\\w{4}_\\w{4}_\\w{12}")

    if uuid_regex.search(database):  # Don't let the database name grow indefinitely accross restores
        new_database = uuid_regex.sub(suffix, database)
    else:
        new_database = database + suffix

    if replicated:
        create_database_query = f"""
        CREATE DATABASE {new_database} ON CLUSTER {cluster}
        """
    else:
        create_database_query = f"""
        CREATE DATABASE {new_database}
        """

    _, output, output_err = _run_remote_query(host, create_database_query)

    # Recreate each table with a different replication path
    database_name_regex = re.compile("(CREATE TABLE\\s+)(\\w+).(\\w+)")
    replication_path_regex = re.compile("(ENGINE = \\w+)\\(\\'([^\\']+)\\'([^\\)]+\\))")
    table_uuid_regex = re.compile("UUID '\\w{8}-\\w{4}-\\w{4}-\\w{4}-\\w{12}'")
    for t in tables:
        # Skip materialized views
        if t["create_query"].startswith("CREATE MATERIALIZED VIEW") or t["create_query"].startswith("CREATE VIEW"):
            continue

        create_table_query = table_uuid_regex.sub("", t["create_query"])
        if replicated:
            # Build new replication path
            replication_path_match = replication_path_regex.search(create_table_query)
            if isinstance(replication_path_match, Match):
                replication_path = replication_path_match.groups()[1]
            if uuid_regex.search(replication_path):  # Same for the replication path
                new_replication_path = uuid_regex.sub(suffix, replication_path)
            else:
                new_replication_path = replication_path + suffix

            # Use new replication path in create query
            create_table_query = database_name_regex.sub(
                f"\\g<1>{new_database}.\\g<3> ON CLUSTER {cluster}", create_table_query
            )
            create_table_query = replication_path_regex.sub(
                f"\\g<1>('{new_replication_path}'\\g<3>", create_table_query
            )
        else:
            # Use MergeTree engine and don't create table ON CLUSTER
            create_table_query = database_name_regex.sub(f"\\g<1>{new_database}.\\g<3>", create_table_query)
            create_table_query = replication_path_regex.sub("ENGINE = MergeTree", create_table_query)
        _, output, output_err = _run_remote_query(host, create_table_query)

    create_table_setting = "must exist" if no_allow_old_schema else "if not exists"
    # Restore the database
    if isinstance(s3_backup_endpoint, S3Backup):
        endpoint = s3_backup_endpoint.endpoint

    echo("Restoring, this can take a long time depending on the size of the database")
    if not table:
        restore_query = f"""
        RESTORE DATABASE {database} AS {new_database} FROM {get_s3_query(endpoint, s3_access_key, s3_secret_key)}
        SETTINGS allow_different_database_def = 1, allow_different_table_def = 1,
                 create_database = 'must exist', create_table = '{create_table_setting}'
        """
        _, output, output_err = _run_remote_query(host, restore_query)
    else:
        for t in tables:
            restore_query = f"""
            RESTORE table {database}.{t['name']} AS {new_database}.{t['name']} FROM {get_s3_query(endpoint, s3_access_key, s3_secret_key)}
            SETTINGS allow_different_database_def = 1, allow_different_table_def = 1,
                     create_database = 'must exist', create_table = '{create_table_setting}'
            """
            _, output, output_err = _run_remote_query(host, restore_query, max_execution_time=144000)  # type: ignore

    echo(f"Restore complete. The old database is now in {new_database}.")
    echo("Check that it is safe to exchange these databases and run")
    echo(f"\tcolibri exchange-clickhouse-databases {host} {database} {suffix.lstrip('_')}")


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("host", type=STRING)
@click.argument("database", type=STRING)
@click.argument("restored_database_uuid", type=STRING)
@click.option("-c", "--check-only/--no-check-only", default=True, help="Should the script stop after the checks?")
@click.option("-d", "--drop-old/--no-drop-old", default=False, help="Should the script drop the old database?")
def exchange_clickhouse_databases(
    host: str, database: str, restored_database_uuid: str, check_only: bool, drop_old: bool
) -> None:
    """
    Exchange the tables of a database with those of a restored copy.
    """
    _run_remote_query: Callable[[str, str], Any] = print_query if check_only else run_remote_query
    cluster = get_host_main_clickhouse_cluster(host)
    new_database = f"{database}_{restored_database_uuid}"
    # Exchange all the tables with the new ones
    response = list_database_tables(host, new_database)
    for table_info in response:
        table_name = table_info["name"]  # type: ignore
        exchange_table_query = f"""
        EXCHANGE TABLES {database}.{table_name} AND {new_database}.{table_name} ON CLUSTER {cluster}
        """
        _run_remote_query(host, exchange_table_query)

    if drop_old:
        drop_database_query = f"""
        DROP DATABASE {new_database} ON CLUSTER {cluster}
        """
        _run_remote_query(host, drop_database_query)
    else:
        echo(f"Remember to drop the old database {new_database}")

    if check_only:
        echo("Run with --no-check-only to execute the above queries")


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("-f", "--filter", "name_filter", default=None, help="Filter clusters by name")
@click.option("-r", "--region", "region_filter", default=None, help="Filter clusters by region")
@click.option("-c", "--current-version", "version_filter", default=None, help="Filter clusters by version")
@click.option("-v", "--version", "desired_version", default=None, help="ClickHouse desired version")
@click.option(
    "-t", "--create-tickets", is_flag=True, default=False, help="Create tickets to upgrade clusters with an old version"
)
@click.option(
    "-m",
    "--create-mr",
    type=str,
    default=None,
    help="Gitlab API Token for creating MRs to upgrade clusters with an old version",
)
@click.option("-u", "--missing-upgrade", is_flag=True, default=False, help="List all the cluster with an old version")
def ch_versions(
    name_filter: Optional[str],
    region_filter: Optional[str],
    version_filter: Optional[str],
    desired_version: Optional[str],
    create_tickets: bool,
    create_mr: Optional[str],
    missing_upgrade: bool,
) -> None:
    """
    Get information about the current ClickHouse cluster versions and create tickets to upgrade them
    """
    conf = get_ansible_config(False)
    versions_map = collections.defaultdict(list)
    tracked_hosts = set()  # To avoid hosts that are on several clusters
    current_version = "0.0"
    issue = None

    if desired_version:
        current_version = desired_version

    if create_tickets:
        if not missing_upgrade:
            log_fatal("Create tickets flag only works with the missing upgrade flag enabled")
        if not confirm(
            style("Are you sure that you want to create tickets for every old cluster?", blink=False), default=False
        ):
            return

    for ch_cluster in conf.inventory.groups:
        if not ch_cluster.startswith("clickhouse_cluster"):
            continue

        # Pick the first hosts from the group to have all the variables
        cluster_hosts = conf.inventory.groups[ch_cluster].get_hosts()
        if not cluster_hosts:
            log_warning("ClickHouse cluster {ch_cluster} is empty (no hosts)")
            continue
        ch_host = cluster_hosts[0]
        ch_vars = conf.variable_manager.get_vars(host=ch_host)

        if "clickhouse_version" not in ch_vars:
            log_warning("Missing clickhouse_version variable on host {ch_vars['inventory_hostname']}")
            continue
        if ch_host in tracked_hosts:
            continue
        ch_version = ch_vars["clickhouse_version"]
        if not desired_version and version.parse(ch_version) > version.parse(current_version):
            current_version = ch_version
        versions_map[ch_version].append(ch_cluster)
        tracked_hosts.add(ch_host)

    if missing_upgrade:
        log_info(f"Detected current version: {current_version}")
        log_info("Listing all the servers older than current version")
    t = _create_pretty_table()
    t.field_names = ["Version", "Region", "Cluster", "Hosts"]
    for ch_version, clusters in versions_map.items():
        if missing_upgrade and (version.parse(ch_version) >= version.parse(current_version)):
            continue
        for cluster in clusters:
            host_names = ", ".join(map(str, conf.inventory.groups[cluster].get_hosts()))
            ch_host = conf.inventory.groups[cluster].get_hosts()[0]
            ch_vars = conf.variable_manager.get_vars(host=ch_host)
            if name_filter and name_filter not in cluster:
                continue

            region = ch_vars["tb_region"]
            if region_filter and region_filter not in region:
                continue

            cluster_version = ch_vars["clickhouse_version"]
            if version_filter and version_filter not in cluster_version:
                continue

            cluster_name = cluster.removeprefix("clickhouse_cluster_")
            t.add_row([ch_version, region, cluster_name, host_names])
            if create_tickets:
                ticket_url = create_upgrade_ticket(cluster_name, current_version, host_names)
                log_info(f"Ticket for cluster {cluster}: {ticket_url}")
                if ticket_url:
                    issue = ticket_url.split("/")[-1]

            if create_mr is not None:
                token = create_mr
                pr_url = create_upgrade_mr(token, cluster_name, current_version, issue)
                log_info(f"Link for MR {cluster} : {pr_url}")

    echo(t.get_formatted_string(out_format="text"))


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("host", type=STRING)
@click.argument("zk_host", type=STRING)
@click.option("-i", "--interactive/--no-interactive", default=True, help="Interact with the user or use safe defaults?")
@click.option("-c", "--check-only/--no-check-only", default=True, help="Should the script stop after the checks?")
@click.option("-l", "--ignore-lock/--no-ignore-lock", default=False, help="Remind about acquiring the platform lock")
@click.option("-n", "--notes", "notes", default=None, help="Add custom notes to platform lock reserve")
def fix_zk_metadata(
    host: str, zk_host: str, interactive: bool, check_only: bool, ignore_lock: bool, notes: str | None
) -> None:
    """
    Fix ZK metadata versions from ClickHouse.
    """
    conf = get_ansible_config(interactive)

    ch_server: ValidatedClickHouseServer = clickhouse_validate_server_before_stop(host)
    # Retrieve all problematic tables
    _, output, _ = run_remote_query(ch_server.server, _zk_metadata_version_issue_query)

    data = json.loads(output)["data"]
    if len(data) == 0:
        log_success("All tables have the right metadata version")
        return

    if conf.interactive and not confirm(
        "[WARNING] "
        + style(f"There are {len(data)} problematic tables, do you want to proceed?", fg="yellow", bg="black"),
        default=True,
    ):
        return

    # Remove ClickHouse server from Varnish safely
    do_the_proceed_with_changes_or_exit(check_only)
    clickhouse_apply_operations_before_stop(ch_server, ignore_lock, notes)

    # Iterate all problematic tables and fix the metadata version
    for row in data:
        resource = row["resource"]
        zk_path = row["zk_path"]
        zk_version = row["zk_version"]
        expected_version = row["expected_version"]
        queue = row["queue"]

        if zk_version == expected_version:
            log_warning(f"{resource}: versions already match")
            continue
        if queue > 0:
            log_warning(f"{resource}: can't apply version changes if replication queue is not empty")
            continue

        log_info(
            f"{resource}: Current version {zk_version} while expected version {expected_version}. Changing to the expected version."
        )
        cmd = f"/opt/zookeeper-3.8.3/bin/zkCli.sh set {zk_path}/metadata_version {expected_version}"
        return_code, _, _ = run_ssh_command(zk_host, cmd)
        if return_code:
            log_error(f"{resource}: failed to apply ZK metadata version change")
            continue

        return_code, _, _ = run_remote_query(ch_server.server, f"SYSTEM RESTART REPLICA {resource}")
        if return_code:
            log_error(f"{resource}: failed to restart replica")
            continue

    clickhouse_apply_operations_after_start(ch_server, ignore_lock)
    log_success("Operation completed. Thank you for flying with Tinybird airlines")
    conf.cleanup_if_needed(force_cleanup=True)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("server", type=STRING)
def restart_vm(server: str) -> None:
    """
    Restart a VM on any cloud provider, the cloud provider will be autodetected by the name of the server

    [WARNING] This script restart the server in a non ordered fashion, you need to take care of preparing the server to be restarted first
    """
    log_info(f"Restarting the server {server}")
    if not confirm(
        "[WARNING] " + style("Is the server already out of production?", fg="yellow", bg="black", blink=True),
        default=False,
    ):
        return
    log_info("Starting VM restart")
    try:
        restart_instance(server)
    except Exception as e:
        log_error(str(e))
        return
    log_success("Restart completed")


def provision_alerts_for_replica(replica: str, alerts_dir: pathlib.Path, extra_vars: Any = None) -> None:
    for alert_file in alerts_dir.glob("*.jsonnet"):
        alert_json = generate_alert_json(str(alert_file), replica, extra_vars)
        try:
            r = post_alert(alert_json)
            if not r.ok:
                log_warning(f"Failed provisioning {alert_file.name}: {r}")
        except requests.exceptions.HTTPError as exc:
            if exc.response.status_code == 400:
                alerts = get_alerts_status("CH upgrades") or []
                provisioned_replicas = [p_r for p_r in alerts if p_r["labels"]["replica"] == replica]
                if len(provisioned_replicas) > 0:
                    log_warning(f"Could not provision alert for {replica}. It already has an alert provisioned.")
            else:
                log_error(f"Could not provision alert. {alert_file.name}: {exc}")


def get_replicas_for(cluster: str) -> list[str]:
    all_group_vars = get_ansible_config().inventory.groups["all"].get_vars()
    varnish_clusters = all_group_vars["varnish_clusters"]

    for region in varnish_clusters:
        for cluster_ in varnish_clusters[region]:
            if cluster_ == cluster:
                return list(varnish_clusters[region][cluster])
    log_error(f"No cluster matching name: {cluster}")
    return []


def _provision_alerts(
    replicas: list[str] | str, cluster: str | None, alerts_dir: pathlib.Path, extra_vars: Any = None
) -> None:
    """
    Provision alerts for replica/cluster (internal function).
    """
    if isinstance(replicas, str):
        replicas = [replicas]
    if cluster:
        replicas = get_replicas_for(cluster)
    if not replicas:
        log_warning("Neither replica nor cluster specified, doing nothing")
    for replica in replicas:
        log_info(f"Provisioning alerts for {replica}")
        provision_alerts_for_replica(replica, alerts_dir, extra_vars)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("--replica", type=STRING, multiple=True, required=False)
@click.option("--cluster", type=STRING, required=False)
@click.option("--alerts_dir", type=pathlib.Path, default=REPO_ROOT / "grafana/alerts")
def provision_alerts(replica: list[str], cluster: str, alerts_dir: pathlib.Path) -> None:
    """
    Provision alerts for replica/cluster (command).
    """
    _provision_alerts(replica, cluster, alerts_dir)


def deprovision_alerts_for_replica(replica: str, alerts: Any) -> None:
    for alert in alerts:
        if replica in alert["title"]:
            delete_alert(alert["uid"])


def _deprovision_alerts(replicas: list[str], cluster: Optional[str], groups: list[str] | None = None) -> None:
    """
    Remove alerts for replica/cluster (internal function).
    """
    if groups is None:
        all_alerts = [get_alert_group("CH upgrades")]
    else:
        all_alerts = [get_alert_group(g) for g in groups]
    all_alerts = [g for g in all_alerts if g is not None]

    if cluster:
        replicas += get_replicas_for(cluster)
    for replica in replicas:
        for group in all_alerts:
            deprovision_alerts_for_replica(replica, group["rules"])
        log_info(f"Alerts for {replica} have been deprovisioned.")


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("-r", "--replica", type=STRING, multiple=True, required=False)
@click.option("--cluster", type=STRING, required=False)
def deprovision_alerts(replica: list[str], cluster: str, groups: list[str] | None = None) -> None:
    """
    Remove alerts for replica/cluster (command).
    """
    _deprovision_alerts(list(replica), cluster, groups)
