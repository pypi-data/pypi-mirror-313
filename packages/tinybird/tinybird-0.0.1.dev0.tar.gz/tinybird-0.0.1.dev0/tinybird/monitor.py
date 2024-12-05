import asyncio
import json
import logging
import random
import re
import threading
import time
import traceback
from abc import ABC, abstractmethod
from asyncio import AbstractEventLoop, Task
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from distutils.util import strtobool
from os import environ, path
from string import Template
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
from uuid import uuid4

import aiofiles
import aiohttp
import orjson
import requests
import ulid
from humanfriendly.tables import format_pretty_table
from pydantic import BaseModel

from tinybird.ch import (
    HTTPClient,
    UserAgents,
    ch_get_clusters_hosts_async,
    ch_get_databases_metadata,
    ch_get_tables_metadata,
)
from tinybird.ch_utils.exceptions import CHException
from tinybird.cluster_settings import ClusterSettings, ClusterSettingsOperations
from tinybird.constants import Relationships
from tinybird.csv_importer import CsvChunkQueueRegistry
from tinybird.datasource_batcher import get_datasource_append_token, get_internal_admin_token
from tinybird.distributed import WorkingGroup
from tinybird.gatherer_common.gatherer_config import get_region_gatherers_config
from tinybird.job import Job, JobKind, JobStatus, sanitize_database_server
from tinybird.limits import EndpointLimits
from tinybird.notifications_service import NotificationsService
from tinybird.organization.organization import Organization
from tinybird.populates.job import PopulateJob
from tinybird.query_booster import booster
from tinybird.raw_events.definitions.projection import ProjectionEvent
from tinybird.raw_events.raw_events_batcher import EventType, RawEvent, raw_events_batcher
from tinybird.sql_template import get_template_and_variables
from tinybird.sql_toolset import replace_tables_chquery_cached, sql_get_used_tables_cached
from tinybird.tinybird_tool.metrics import check_metrics_tables
from tinybird.user import User as Workspace
from tinybird.user import UserAccount, UserDoesNotExist, public
from tinybird.user import Users as Workspaces
from tinybird.user_tables import get_all_tables
from tinybird.user_workspace import UserWorkspaceRelationship
from tinybird.views.api_query import max_threads_by_endpoint
from tinybird.views.base import QUERY_API
from tinybird_shared.clickhouse.errors import CHErrors
from tinybird_shared.metrics.statsd_client import statsd_client

MONITOR_DELAY_STARTUP_TIME = 15
MONITOR_REPLACE_EXECUTOR_INTERVAL_IN_SECONDS = 0.2  # 200 ms
MONITOR_APP_IN_SECONDS = 60  # 1 minute
DEDICATED_INFRA_METRICS_TASK_FREQ_IN_SECONDS = 10
MONITOR_JOBS_IN_SECONDS = 60 * 15  # 15 minute
MONITOR_METRICS_CHECKER_INTERVAL_IN_SECONDS = 3600  # 60 minutes
MONITOR_ORPHAN_INTERVAL_IN_SECONDS = 900  # 15 minutes
MONITOR_GATHERER_AVAILABILITY_INTERVAL_IN_SECONDS = 60  # 1 minute
MONITOR_WORKSPACES_TO_HARD_DELETE_INTERVAL_IN_SECONDS = 3600 * 24  # 1 day
MAX_JOB_AGE_IN_SECONDS = 3600  # 60 minutes
MAX_COPY_JOB_AGE_IN_SECONDS = 2 * 3600  # 120 minutes
EXCLUDED_NAMES_FROM_ORPHAN_MVS = ["_generator", "_tmp_", "_mirror_", "_landing_to_filtered_"]

"""
Instructions to create a new Monitor:
- Create a new class inheriting MonitorTask and:
    - Select a monitor_name. Should be unique per Monitor.
    - Select a task_frequency_in_seconds to configure the frequency of execution.
    - With `single_instance_execution` you'll activate a WorkingGroup to limit parallelism so this Monitor is only
      executed in one instance.
    - Implement `action` with the Monitor's implementation
- After that, instantiate the new class inside the `Monitor`'s `__init__` method.
"""


class Monitor:
    def __init__(
        self, conf: Dict[str, Any], is_executed_inside_job_processor: bool, is_reader: bool, hfi_host: str
    ) -> None:
        self._conf = conf

        self.monitor_list: List[MonitorTask] = [
            AppMetricsMonitorTask(),
            ReplaceExecutorQueuedMonitorTask(),
        ]

        if is_executed_inside_job_processor:
            # We need to import the monitor inside the if block to avoid circular imports
            # We should extract all the monitoring tasks in smaller files
            from tinybird.orb_integration.monitor import MonitorIntegrationWithOrb

            self.monitor_list.extend(
                [
                    OldAndStuckJobsMetricsMonitorTask(),
                    MetricsTablesCheckerMonitorTask(self._conf),
                    OrphanMetricsCheckerMonitorTask(),
                    WorkspacesToHardDeleteCheckerMonitorTask(),
                    GathererAvailabilityCheckerMonitorTask(self._conf),
                    EndpointIndexesMonitorTask(),
                    EndpointConcurrencyMonitorTask(),
                    DedicatedInfrastructureMonitorTask(hfi_host),
                    MonitorIntegrationWithOrb(),
                    CpuTimeOveruseMonitorTaskHourly(
                        region=conf.get("tb_region", ""), clusters=conf.get("clickhouse_clusters", {})
                    ),
                    CpuTimeOveruseMonitorTaskDaily(
                        region=conf.get("tb_region", ""), clusters=conf.get("clickhouse_clusters", {})
                    ),
                ]
            )
        elif is_reader:
            self.monitor_list.append(EndpointMonitorTask())

    async def init(self) -> None:
        for monitor in self.monitor_list:
            await monitor.init()

    def terminate(self) -> None:
        for monitor in self.monitor_list:
            monitor.terminate()


class MonitorTask(ABC):
    """
    Class to implement a monitor Task. It uses the same pattern as tinybird.internal_thread.InternalThread but
    MonitorTask runs inside the asyncio loop.
    """

    def __init__(self, monitor_name: str, task_frequency_in_seconds: float, single_instance_execution: bool) -> None:
        self.monitor_name = monitor_name
        self.task_frequency_in_seconds = task_frequency_in_seconds
        self.single_instance_execution = single_instance_execution

        self._exit_flag: asyncio.Event = asyncio.Event()
        self._working_group: WorkingGroup = WorkingGroup(self.monitor_name, str(uuid4()))

        self._task: Optional[Task] = None

    async def init(self) -> None:
        try:
            self._asyncio_loop: AbstractEventLoop = asyncio.get_running_loop()
            if self.single_instance_execution:
                await self._working_group.init()
            self._task = asyncio.create_task(self._loop())
        except Exception as e:
            logging.exception(f"Error initializing the monitor '{self.monitor_name}': {e}")

    async def _delay_startup(self) -> None:
        random_delay_for_startup_time = random.randint(0, MONITOR_DELAY_STARTUP_TIME)
        await asyncio.sleep(random_delay_for_startup_time)

    async def _loop(self) -> None:
        logging.info(f"Monitor: starting loop for Monitor Task: '{self.monitor_name}'")
        await self._delay_startup()

        while not self._exit_flag.is_set():
            try:
                score_index = 0
                start_time = time.monotonic()
                if self.single_instance_execution:
                    score_index = self._working_group.score_index("main")
                if score_index == 0:
                    try:
                        await self.action()
                    except Exception as e:
                        logging.exception(
                            f"Unhandled exception inside Monitor Task '{self.monitor_name}': {e}.\nTraceback: {traceback.format_exc()}"
                        )

                try:
                    elapsed = time.monotonic() - start_time
                    await asyncio.wait_for(
                        self._exit_flag.wait(), timeout=max(self.task_frequency_in_seconds - elapsed, 0)
                    )
                except asyncio.TimeoutError:
                    pass
            except Exception as e:
                logging.exception(
                    f"Unhandled exception inside Monitor Task '{self.monitor_name}': {e}.\nTraceback: {traceback.format_exc()}"
                )

    def terminate(self) -> None:
        # The asyncio.Event needs to be set from the same thread it
        # was created from. So, we schedule a coroutine to set it.
        async def set_flag_in_loop() -> None:
            self._exit_flag.set()
            if self.single_instance_execution:
                await self._working_group.exit()

        asyncio.run_coroutine_threadsafe(set_flag_in_loop(), loop=self._asyncio_loop)

    @abstractmethod
    async def action(self) -> None:
        """
        Override this method to add the Monitor's implementation
        """
        raise NotImplementedError("This method should be implemented by the subclass")


class AppMetricsMonitorTask(MonitorTask):
    def __init__(self) -> None:
        super().__init__(
            monitor_name="app_metrics_monitor",
            task_frequency_in_seconds=MONITOR_APP_IN_SECONDS,
            single_instance_execution=False,
        )

    async def action(self) -> None:
        await self._send_csv_info()
        await self._send_threads_info()
        await self._send_cache_metrics()
        await self._send_redis_cache_metrics()

    @staticmethod
    async def _send_csv_info() -> None:
        csv_queue = CsvChunkQueueRegistry.get_or_create()
        queues = len(csv_queue.queues)
        blocks_waiting = csv_queue.blocks_waiting()
        last_block_processed_at = csv_queue.last_dummy_block_processed_at.timestamp()
        statsd_client.gauge(f"tinybird.{statsd_client.region_app_machine}.csv.queues", queues)
        statsd_client.gauge(f"tinybird.{statsd_client.region_app_machine}.csv.blocks_waiting", blocks_waiting)
        statsd_client.gauge(
            f"tinybird.{statsd_client.region_app_machine}.csv.last_block_processed", last_block_processed_at
        )

    @staticmethod
    async def _send_threads_info() -> None:
        threads = threading.enumerate()
        statsd_client.gauge(f"tinybird.{statsd_client.region_app_machine}.threads", len(threads))

    @staticmethod
    async def _send_cache_metrics() -> None:
        def send_metrics(metrics_path: str, fun: Callable) -> None:
            hits, misses, _, currsize = fun()
            statsd_client.gauge(f"{metrics_path}.hits", hits)
            statsd_client.gauge(f"{metrics_path}.misses", misses)
            statsd_client.gauge(f"{metrics_path}.currsize", currsize)

        send_metrics(
            f"tinybird.{statsd_client.region_app_machine}.template_cache", get_template_and_variables.cache_info
        )
        send_metrics(
            f"tinybird.{statsd_client.region_app_machine}.used_tables_cache", sql_get_used_tables_cached.cache_info
        )
        send_metrics(
            f"tinybird.{statsd_client.region_app_machine}.replace_tables_cache",
            replace_tables_chquery_cached.cache_info,
        )

    @staticmethod
    async def _send_redis_cache_metrics() -> None:
        for model, cache in Workspace.__object_cache_by_id__.items():
            hits = cache.hits
            misses = cache.misses
            currsize = cache.currsize

            base_path = f"tinybird.{statsd_client.region}.redis_cache.{model}"
            statsd_client.incr(f"{base_path}.hits", hits)
            statsd_client.incr(f"{base_path}.misses", misses)
            statsd_client.gauge(f"{base_path}.currsize", currsize)


class OldAndStuckJobsMetricsMonitorTask(MonitorTask):
    def __init__(self) -> None:
        super().__init__(
            monitor_name="old_and_stuck_jobs_metrics",
            task_frequency_in_seconds=MONITOR_JOBS_IN_SECONDS,
            single_instance_execution=True,
        )

    async def action(self) -> None:
        logging.debug("[JOB MONITOR]: collecting and sending stats")
        start_time = datetime.now(timezone.utc)
        pending_jobs = await self._get_pending_jobs_info()
        logging.info(f"[JOB MONITOR]: getting all the pending jobs took {datetime.now(timezone.utc) - start_time}")

        await self._send_jobs_health_info(pending_jobs)
        await self._send_queue_size_metrics(pending_jobs)

    @staticmethod
    async def _get_pending_jobs_info() -> List[Job]:
        # We do not use the executors to know the WIP jobs because we might miss jobs that are running in a background JobProcess.
        # A JobProcessor might have a job stuck in the WORKING state, but as it's running in another executor we are not able to know it.
        pending_jobs = [
            j for j in Job.iterate(batch_count=100) if j.status == JobStatus.WORKING or j.status == JobStatus.WAITING
        ]
        return pending_jobs

    @staticmethod
    async def _job_working_with_exception(job: PopulateJob) -> bool:
        try:
            # We only want to check for the queries that are still working
            query_ids = [query.query_id for query in job.queries if query.status == JobStatus.WORKING]
            if not query_ids:
                return False

            client = HTTPClient(host=job.database_server)
            cluster = job.user.cluster
            query_log = f"clusterAllReplicas('{cluster}', system.query_log)" if cluster else "system.query_log"

            # We need to check for the last hour as we do not expect a query to fail and the job to still be working
            # In case we have a job that is working but the query has failed, we will log a warning during that hour to be able to debug it
            sql = f"""
                SELECT
                    query_id,
                    exception
                FROM {query_log}
                WHERE
                    query_id IN ({', '.join([f"'{q}'" for q in query_ids])})
                    AND type > 2
                    AND event_time >= parseDateTimeBestEffort('{job.created_at}')
                    AND event_time < now() - INTERVAL 5 MINUTE
                    AND event_date >= toDate('{job.created_at}')
                FORMAT JSON
            """
            _, body = await client.query(
                sql, read_only=True, max_threads=1, skip_unavailable_shards=1, max_execution_time=30
            )
            data = orjson.loads(body)["data"]
            if data:
                logging.warning(
                    f"[JOB MONITOR] Job {job.id} is working but raised an exception in CH with query_id '{data[0]['query_id']}' and exception '{data[0]['exception']}'"
                )
                return True
            return False
        except CHException as e:
            if e.code == CHErrors.TIMEOUT_EXCEEDED:
                logging.warning(f"[JOB MONITOR] Job {job.id} is working but CH took too long to respond")
            else:
                logging.exception(f"[JOB MONITOR] Error getting job progress details: {e}")
            return False
        except Exception as e:
            logging.exception(f"[JOB MONITOR] Error getting job progress details: {e}")
            return False

    async def _send_jobs_health_info(self, pending_jobs: List[Job]) -> None:
        # We need to use `datetime.utcnow()` instead of `datetime.now(timezone.utc)` because the `Job.created_at` is a naive datetime
        # and we need to compare it with another naive datetime https://gitlab.com/tinybird/analytics/-/issues/13843
        now = datetime.utcnow()

        try:
            u = public.get_public_user()
            database_server = u.database_server
            old_jobs = 0
            for j in pending_jobs:
                if j.kind == JobKind.POPULATE:
                    if j.status != JobStatus.WORKING:
                        continue

                    # Check if the query_id in working state has raised an exception in CH, but the job is still working
                    if isinstance(j, PopulateJob):
                        if await self._job_working_with_exception(j):
                            logging.warning(f"[JOB MONITOR] Job {j.id} is working but raised an exception in CH")
                    else:
                        # This should never happen, but we are logging it just in case
                        logging.warning(f"[JOB MONITOR] Job {j.id} is not a PopulateJob, but kind is {j.kind}")

                else:
                    delta = now - j.created_at
                    job_age = delta.total_seconds()
                    is_old_copy_job = j.kind == JobKind.COPY and job_age > MAX_COPY_JOB_AGE_IN_SECONDS
                    is_old_job = job_age > MAX_JOB_AGE_IN_SECONDS and j.kind != JobKind.COPY
                    if is_old_job or is_old_copy_job:
                        old_jobs = old_jobs + 1
                        logging.warning(
                            f"Old job detected: {j.id}. Status {j.status}. Age: {delta.total_seconds()} seconds"
                        )
                    continue

            statsd_client.gauge(
                f"tinybird.{statsd_client.region_machine}.jobs.{sanitize_database_server(database_server)}.old_jobs",
                old_jobs,
            )

        except Exception as e:
            logging.exception(f"[JOB MONITOR] Error getting jobs health status: {e}")

    @staticmethod
    async def _send_queue_size_metrics(pending_jobs: List[Job]) -> None:
        try:
            u = public.get_public_user()
            database_server = u.database_server
            queued_count_by_key: defaultdict[str, int] = defaultdict(int)
            for job in pending_jobs:
                # Some job subclasses have a .database_server field
                job_database_server = getattr(job, "database_server", database_server)
                status = "wip" if job.status == JobStatus.WORKING else "queued"
                queued_count_by_key[f"{sanitize_database_server(job_database_server)}.{job.kind}.{status}"] += 1

            for key, count in queued_count_by_key.items():
                # since every host should send the same stat, use "unknown" to reduce cardinality
                statsd_client.gauge(f"tinybird.{statsd_client.region}.unknown.jobs.{key}", count)
        except Exception as e:
            logging.exception(f"[JOB MONITOR] Error getting queue sizes: {e}")


class ReplaceExecutorQueuedMonitorTask(MonitorTask):
    def __init__(self) -> None:
        super().__init__(
            monitor_name="replace_executor_queued",
            task_frequency_in_seconds=MONITOR_REPLACE_EXECUTOR_INTERVAL_IN_SECONDS,
            single_instance_execution=False,
        )

    async def action(self) -> None:
        if Workspace.replace_executor:
            work_queue_size = Workspace.replace_executor._work_queue.qsize()
        else:
            work_queue_size = 0
        statsd_client.gauge(
            f"tinybird.{statsd_client.region_app_machine}.replace_executor_queue",
            work_queue_size,
        )


class MetricsTablesCheckerMonitorTask(MonitorTask):
    def __init__(self, conf: Dict[str, Any]) -> None:
        super().__init__(
            monitor_name="metrics_tables_checker",
            task_frequency_in_seconds=MONITOR_METRICS_CHECKER_INTERVAL_IN_SECONDS,
            single_instance_execution=True,
        )
        self._conf = conf

    async def action(self) -> None:
        internal_server: Optional[str] = self._conf.get("internal_database_server")
        if not internal_server:
            logging.exception("internal_database_server not defined")
            return

        errors: List[str] = await check_metrics_tables(conf=self._conf, check_host=internal_server)
        if len(errors) > 0:
            err_str: str = "\n - ".join(errors)
            logging.exception(f"Metrics tables errors found:\n - {err_str}")
        else:
            logging.info("Metrics tables checker found 0 errors.")


class OrphanMetricsCheckerMonitorTask(MonitorTask):
    def __init__(self) -> None:
        super().__init__(
            monitor_name="orphan_metrics",
            task_frequency_in_seconds=MONITOR_ORPHAN_INTERVAL_IN_SECONDS,
            single_instance_execution=True,
        )

    async def action(self) -> None:
        await self._send_orphan_info()
        all_workspaces_metadata = await self._get_all_metadata()
        await self._send_orphan_branches_and_releases(all_workspaces_metadata)
        # temporary disabled to validate first manually
        # await self._send_orphan_metadata_info(all_workspaces_metadata)

    @staticmethod
    async def _get_tables_metadata() -> Tuple[Set, Dict, Dict]:
        logging.info("[ORPHAN MONITOR]: getting all metadata from redis")
        users_by_database, users_tables, ch_servers = await asyncio.to_thread(
            get_all_tables, only_main_workspaces=True, only_active_workspaces=True
        )
        logging.info("[ORPHAN MONITOR]: getting all tables from clickhouses")
        ch_tables = await ch_get_tables_metadata(database_servers=ch_servers, filter_engines=("View", "Distributed"))
        return users_tables, ch_tables, users_by_database

    @staticmethod
    async def _get_all_metadata() -> List[Workspace]:
        return await asyncio.to_thread(Workspace.get_all, include_releases=True, include_branches=True)

    @staticmethod
    async def _send_orphan_branches_and_releases(workspaces: List[Workspace]) -> None:
        workspace_ids = {ws.id for ws in workspaces}
        orphan_branches_and_releases = (ws for ws in workspaces if ws.origin and ws.origin not in workspace_ids)
        # If the branch or release has an origin but the origin no longer exists, we will consider it an orphan
        # If the workspace is soft-deleted, we will detect it in another place and hard-delete it which should remove these branches/releases
        for workspace in orphan_branches_and_releases:
            # New branches will have child_kind == ChildKind.BRANCH so it should be fine
            if workspace.is_branch:
                logging.warning(
                    f"[ORPHAN MONITOR] orphan branch: {workspace.cluster} {workspace.name} {workspace.id} created at {workspace.created_at} {workspace.database}"
                )
                statsd_client.incr(f"tinybird.orphan_branch.{workspace.cluster}_{workspace.id}")
            else:
                logging.warning(
                    f"[ORPHAN MONITOR] orphan release: {workspace.cluster} {workspace.name} {workspace.id} created at {workspace.created_at} {workspace.database}"
                )
                statsd_client.incr(f"tinybird.orphan_release.{workspace.cluster}_{workspace.id}")

        # We are hard deleting branches, so if we find a soft deleted branch, we should remove them
        soft_deleted_branches = [ws for ws in workspaces if ws.is_branch and ws.deleted]
        for workspace in soft_deleted_branches:
            logging.warning(
                f"[ORPHAN MONITOR] soft deleted branch: {workspace.cluster} {workspace.name} {workspace.id} created at {workspace.created_at} {workspace.database}"
            )
            statsd_client.incr(f"tinybird.orphan_branch.{workspace.cluster}_{workspace.id}")

        # Branches and workspaces should always have at least 1 member
        workspaces_without_members = [
            ws for ws in workspaces if not ws.is_release and len(ws.members) == 0 and not ws.deleted
        ]
        for ws in workspaces_without_members:
            logging.warning(
                f"[ORPHAN MONITOR] workspace without members: {ws.cluster} {ws.name} {ws.id} created at {ws.created_at} {ws.database}"
            )

        # We might still have orphan releases and specially branches that are not deleted, but still the CH database not exists
        # https://gitlab.com/tinybird/analytics/-/issues/13060
        # TODO: Move this outside and clean a bit the code
        database_servers = {(ws.database_server, ws.cluster) for ws in workspaces}
        ch_databases = await ch_get_databases_metadata(
            database_servers=database_servers, avoid_database_names=("system",)
        )
        workspaces_without_database = [
            ws for ws in workspaces if ws.database not in ch_databases.get(ws.cluster or "", [])
        ]
        for ws in workspaces_without_database:
            logging.warning(
                f"[ORPHAN MONITOR] orphan workspace: {ws.cluster} {ws.id} {ws.name} created at: {ws.created_at} deleted: {ws.deleted} {ws.database}"
            )

    @staticmethod
    async def _send_orphan_metadata_info(workspaces: Optional[List[Workspace]] = None) -> None:
        try:
            if workspaces is None:
                workspaces = await asyncio.to_thread(Workspace.get_all, include_releases=True, include_branches=True)

            workspaces = [ws for ws in workspaces if ws.is_active]

            ch_servers: Set[Tuple[str, Optional[str]]] = set()
            for ws in workspaces:
                if ws.clusters:
                    for cluster in ws.clusters:
                        ch_servers.add((ws.database_server, cluster))
                else:
                    ch_servers.add((ws.database_server, None))
            ch_databases = await ch_get_databases_metadata(
                database_servers=ch_servers, avoid_database_names=("system",)
            )
            # all clusters have public override with correct info for Internal
            u = public.get_public_user()
            ch_databases[u.cluster if u.cluster else u.database_server] += [u.database]
            if ch_databases:
                for ws in workspaces:
                    ch_cluster_databases = (
                        ch_databases.get(ws.cluster, []) if ws.cluster else ch_databases.get(ws.database_server, [])
                    )
                    if ws.database not in ch_cluster_databases:
                        statsd_client.incr(f"tinybird.orphan_metadata.{ws.cluster}_{ws.id}.{ws.database}")
                        logging.warning(
                            f"orphan metadata '{ws.id}:{ws.name}': database '{ws.database}' not found at {ws.clusters}"
                        )
        except Exception:
            logging.exception("Error detecting orphan workspaces metadata")

    async def _send_orphan_info(self) -> None:
        (users_tables, ch_tables, users_by_database) = await self._get_tables_metadata()
        # get hosts per clusters
        hosts_per_cluster: Dict[str, int] = {}
        logging.info("[ORPHAN MONITOR]: looking for hosts in clusters")
        internal_workspace = public.get_public_user()
        for host in await ch_get_clusters_hosts_async(internal_workspace.database_server):
            if host["cluster"] not in hosts_per_cluster:
                hosts_per_cluster[host["cluster"]] = 0
            hosts_per_cluster[host["cluster"]] += 1

        logging.info("[ORPHAN MONITOR]: looking for orphans")
        for t, (engine, mtime, database_server, count, cluster) in ch_tables.items():
            database_server = sanitize_database_server(database_server)

            def _is_excluded(table: str) -> bool:
                return any(suffix in table for suffix in EXCLUDED_NAMES_FROM_ORPHAN_MVS)

            database = t[0]
            table_id = t[1]

            # check orphan ch resources
            if t not in users_tables:
                user_database_info = users_by_database.get(database, [])
                is_deleted = False if user_database_info and user_database_info[2] else True

                if not is_deleted and not _is_excluded(table_id) and engine == "MaterializedView":
                    u = Workspace.get_by_name(user_database_info[0])
                    if u:
                        _, materialized_view = u.find_pipe_in_releases_metadata_by_pipe_node_id(table_id)
                        if not materialized_view:
                            statsd_client.incr(f"tinybird.orphan_matviews_non_deleted.{database_server}")
                            logging.warning(
                                f"[ORPHAN MONITOR] orphan {engine} at {database_server} since {mtime}: {database}.{table_id}"
                            )
                        else:
                            logging.warning(
                                f"[ORPHAN MONITOR] false positive on orphan at {database_server}: {database}.{table_id}"
                            )
                    else:
                        logging.warning(
                            f"[ORPHAN MONITOR] discarded orphan as workspace not found for {database}.{table_id}"
                        )

                def _is_orphan_aux_copy(table: str, mtime: str) -> bool:
                    modified_time = datetime.strptime(mtime, "%Y-%m-%d %H:%M:%S")
                    return "aux_copy" in table and modified_time < datetime.utcnow() - timedelta(days=2)

                if not is_deleted and _is_orphan_aux_copy(table_id, mtime):
                    statsd_client.incr(f"tinybird.orphan_aux_copy.{database_server}")
                    logging.warning(f"orphan aux copy table at {database_server} since {mtime}: {database}.{table_id}")

            # check missing in replicas
            try:
                if not _is_excluded(table_id) and count < hosts_per_cluster[cluster]:
                    if t in users_tables:
                        statsd_client.incr(f"tinybird.missing_ch_resource.{cluster}")
                        logging.warning(
                            f"[ORPHAN MONITOR] missing {engine} at {cluster} present since {mtime} on {count} of {hosts_per_cluster[cluster]}: {database}.{table_id}"
                        )
                    else:
                        statsd_client.incr(f"tinybird.missing_ch_resource_not_in_metadata.{cluster}")
                        logging.warning(
                            f"[ORPHAN MONITOR] not in metadata missing {engine} at {cluster} present since {mtime} on {count} of {hosts_per_cluster[cluster]}: {database}.{table_id}"
                        )
            except Exception as exc:
                logging.exception(
                    f"[ORPHAN MONITOR]: Unexpected error checking {database}.{table_id} missing in replicas: {exc} "
                )


class WorkspacesToHardDeleteCheckerMonitorTask(MonitorTask):
    def __init__(self) -> None:
        super().__init__(
            monitor_name="workspaces_to_hard_delete",
            task_frequency_in_seconds=MONITOR_WORKSPACES_TO_HARD_DELETE_INTERVAL_IN_SECONDS,
            single_instance_execution=True,
        )

    async def action(self) -> None:
        ws_to_hard_delete: List[Workspace] = Workspace.get_soft_deleted_workspaces_for_hard_deletion()
        ws_by_cluster: Dict[Optional[str], List[Workspace]] = {}

        for ws in ws_to_hard_delete:
            if ws.cluster not in ws_by_cluster:
                ws_by_cluster[ws.cluster] = []
            ws_by_cluster[ws.cluster].append(ws)

        for cluster, ws_list in ws_by_cluster.items():
            statsd_client.gauge(f"tinybird.{statsd_client.region}.{cluster}.ws_to_hard_delete", len(ws_list))
            logging.info(f"Workspaces pending hard deletion at {cluster}: {len(ws_list)}")


class GathererAvailabilityCheckerMonitorTask(MonitorTask):
    def __init__(self, conf: Dict[str, Any]) -> None:
        super().__init__(
            monitor_name="gatherer_availability",
            task_frequency_in_seconds=MONITOR_GATHERER_AVAILABILITY_INTERVAL_IN_SECONDS,
            single_instance_execution=True,
        )
        self._conf = conf
        self._region: str = conf["tb_region"]

    async def action(self) -> None:
        expected_gatherers: int = int(self._conf.get("expected_gatherers", 0))
        if expected_gatherers == 0:
            logging.warning(f"No Gatherers expected in {self._region} region")
            return

        available_gatherers = self._count_available_gatherers()
        self._send_available_gatherers_info(expected_gatherers, available_gatherers)

    def _count_available_gatherers(self) -> int:
        available_gatherers_config = get_region_gatherers_config(self._region)
        return len(available_gatherers_config)

    def _send_available_gatherers_info(self, expected_gatherers: int, available_gatherers: int) -> None:
        if available_gatherers == 0:
            statsd_client.incr(f"tinybird.{statsd_client.region_machine}.no_gatherer")
            logging.warning(f"No Gatherers available in {self._region} region (expected: {expected_gatherers})")
            return

        if available_gatherers < expected_gatherers:
            statsd_client.incr(f"tinybird.{statsd_client.region_machine}.gatherer_ha_compromised")
            logging.warning(
                f"Expected Gatherers in {self._region} region: {expected_gatherers}, only {available_gatherers} found"
            )


class EndpointMonitorTask(MonitorTask):
    """
    This monitor tracks the endpoints performance and assign resources according to the performance.
    """

    def __init__(self) -> None:
        super().__init__(
            "endpoint_monitor",
            task_frequency_in_seconds=3600,
            # Let's run the same process in each reader for now to avoid having to use Redis
            single_instance_execution=False,
        )

        self.clusters = ["eu_public_a"]

    async def action(self) -> None:
        try:
            public_user = public.get_public_user()
            client = HTTPClient(public_user.database_server, database=public_user.database)
            pipe_stats_rt = public_user.get_datasource("pipe_stats_rt")
            workspaces_all = public_user.get_datasource("workspaces_all")
            if not pipe_stats_rt or not workspaces_all:
                logging.error(
                    f"pipe_stats_rt datasource {pipe_stats_rt} or workspaces_all datasource {workspaces_all} not found."
                )
                return

            # For now, we will only assign threads to the fast endpoints
            clusters_interested = " AND ".join([f"database_server LIKE '%{cluster}%'" for cluster in self.clusters])
            sql = f"""
                SELECT
                    pipe_id,
                    quantile(0.9)(duration) as p90_duration
                FROM {pipe_stats_rt.id}
                WHERE
                    start_datetime >= now() - INTERVAL 24 HOUR
                    AND user_id IN (
                        SELECT id
                        FROM {workspaces_all.id}
                        WHERE {clusters_interested}
                    )
                GROUP BY pipe_id
                HAVING p90_duration <= 0.1
                FORMAT JSON
            """
            _, body = await client.query(sql, max_threads=1)
            data = json.loads(body)["data"]
            previous_endpoints = max_threads_by_endpoint.copy()
            for row in data:
                pipe_id: str = row["pipe_id"]
                max_threads_by_endpoint[pipe_id] = 1
                previous_endpoints.pop(pipe_id, None)

            # Remove all the previous endpoints that are not in the current list
            for pipe_id in previous_endpoints:
                max_threads_by_endpoint.pop(pipe_id, None)

        except Exception as e:
            logging.exception(f"Error in endpoint monitor: {e}")


class EndpointIndexesMonitorTask(MonitorTask):
    """
    Monitor task that tracks the performance of endpoint indexes by querying the ClickHouse query log.
    """

    def __init__(self) -> None:
        super().__init__(
            "endpoint_indexes_monitor",
            task_frequency_in_seconds=900,
            single_instance_execution=True,
        )

    async def action(self) -> None:
        try:
            public_user = public.get_public_user()
            client = HTTPClient(public_user.database_server, database=public_user.database)

            projections_ds = public_user.get_datasource("projections")
            if not projections_ds:
                logging.error("Projections Data Source is not available")
                return

            projections_sql = f"""
                SELECT
                    name,
                    status
                FROM {public_user.database}.{projections_ds.id} FINAL
                FORMAT JSON
            """
            _, body = await client.query(
                projections_sql,
                max_threads=1,
                max_execution_time=30,
                user_agent=UserAgents.BOOSTER.value,
            )
            projections_status: Dict[str, str] = {p["name"]: p["status"] for p in json.loads(body)["data"]}

            sql_clusters = "SELECT DISTINCT name FROM system.clusters WHERE name NOT LIKE 'itx%' AND name NOT LIKE '%_internal' AND name NOT LIKE '%_metrics' AND name NOT LIKE '%_gatherer' FORMAT JSON"
            _, body = await client.query(sql_clusters, max_threads=1, user_agent=UserAgents.BOOSTER.value)
            clusters = json.loads(body)["data"]

            sql_template = """
                WITH {hours} * 3_600 AS _elapsed
                SELECT
                    JSONExtractString(log_comment, 'workspace') AS workspace,
                    JSONExtractString(log_comment, 'pipe') AS pipe,
                    normalized_query_hash || '_' || cityHash64(arraySort(tables)) AS query_hash_tables,
                    avg(read_bytes) / 1_000_000 AS read_mb,
                    sum(ProfileEvents['OSCPUVirtualTimeMicroseconds'] / 1_000_000 / _elapsed) AS cpus,
                    count() / _elapsed AS qps,
                    any(query) AS query
                FROM clusterAllReplicas('{cluster}', system.query_log)
                WHERE
                    event_date >= toDate(now() - toIntervalHour({hours}))
                    AND event_time >= now() - toIntervalHour({hours})
                    AND type > 1
                    AND http_user_agent = 'tb-api-query'
                GROUP BY
                    workspace,
                    pipe,
                    query_hash_tables
                HAVING read_mb > 200 and qps > 0.01
                ORDER BY cpus DESC
                LIMIT 40
                FORMAT JSON
            """

            projections_sql_template = """
                SELECT
                    q.query_hash_tables AS query_hash_tables,
                    database,
                    datasource_id AS table,
                    name AS projection_name,
                    projection,
                    updated_at,
                    last_call,
                    has(projections_last_calls, database || '.' || datasource_id || '.' || name) projection_used,
                    date_diff('minutes', updated_at, last_call) minutes,
                    projection_used <> 1 AND minutes > 60 to_block,
                    last_call < now() - toIntervalHour({hours}) to_delete
                FROM {public_database}.{projections_ds_id} AS p FINAL
                ANY LEFT JOIN (
                    SELECT
                        normalized_query_hash AS query_hash,
                        normalized_query_hash || '_' || cityHash64(arraySort(tables)) AS query_hash_tables,
                        max(event_time) AS last_call,
                        groupUniqArrayArray(projections) AS projections_last_calls
                    FROM clusterAllReplicas('{cluster}', system.query_log)
                    WHERE
                        event_date >= toDate(now() - toIntervalHour({hours}))
                        AND event_time >= now() - toIntervalHour({hours})
                        AND type > 1
                        AND http_user_agent = 'tb-api-query'
                    GROUP BY
                        query_hash,
                        query_hash_tables
                ) AS q ON (q.query_hash_tables = p.query_hash_tables) OR (q.query_hash = p.query_hash)
                WHERE status = 'created'
                    AND (database, table) IN (
                        SELECT database, name FROM cluster('{cluster}', system.tables)
                    )
                FORMAT JSON
            """

            for cluster in clusters:
                sql = sql_template.format(cluster=cluster["name"], hours=1)
                _, body = await client.query(
                    sql,
                    max_threads=1,
                    max_execution_time=120,
                    skip_unavailable_shards=1,
                    user_agent=UserAgents.BOOSTER.value,
                )
                data = json.loads(body)["data"]

                for row in data:
                    try:
                        workspace = Workspace.get_by_name(row["workspace"])
                    except UserDoesNotExist:
                        logging.warning(
                            f"{self.__class__.__name__}: Optimizable query in cluster {cluster['name']}: Workspace {row['workspace']} not found"
                        )
                        continue

                    projections = await booster.suggest_projections(workspace, row["query"])
                    if not projections:
                        continue

                    log_output = f"Optimizable query in cluster {cluster['name']}: Workspace: {row['workspace']}, Pipe: {row['pipe']}, Query hash: {row['query_hash_tables']}.\n"
                    log_output += (
                        f"Query reasons: {row['read_mb']:.2f}MB, {row['cpus']:.2f}CPUs, {row['qps']:.2f}QPS.\n"
                    )
                    slack_message = (
                        f":racing_car: Optimizable query in cluster `{cluster['name']}` :racing_car:\n\n"
                        f"Workspace: `{row['workspace']}`, pipe: `{row['pipe']}`, query hash: `{row['query_hash_tables']}`."
                    )
                    send_slack_message = False
                    for projection in projections:
                        log_output += f"Table: {projection.database}.{projection.table}. "
                        if projection.error_message:
                            log_output += f"{projection.error_message}\n"
                            continue

                        log_output += f"Suggested projection: {projection.projection}.\n"

                        successful, message = await booster.create_projection(workspace, projection, projections_status)
                        if not successful:
                            log_output += f"Projection not created: {message}\n"
                        else:
                            send_slack_message = True
                            create_sql = "; ".join(projection.alter_queries)
                            slack_message += (
                                f"\n\nCreated projection: `{projection.projection}`.\n\n```\n{create_sql}\n```"
                            )

                            raw_events_batcher.append_record(
                                RawEvent(
                                    timestamp=datetime.now(timezone.utc),
                                    workspace_id=workspace.id,
                                    request_id=uuid4().hex,
                                    event_type=EventType.PROJECTIONS,
                                    event_data=ProjectionEvent(
                                        database=projection.database,
                                        datasource_id=projection.table,
                                        name=projection.name,
                                        query_hash_tables=row["query_hash_tables"],
                                        status="created",
                                        updated_at=datetime.now(timezone.utc),
                                        projection=projection.projection or "",
                                    ),
                                )
                            )

                    if send_slack_message:
                        # Send suggested projection to Slack
                        requests.post(  # noqa: ASYNC210
                            "https://hooks.slack.com/services/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",
                            headers={"Content-type": "application/json"},
                            data=json.dumps(
                                {
                                    "type": "mrkdwn",
                                    "text": slack_message,
                                }
                            ),
                        )

                    logging.info(f"{self.__class__.__name__}: {log_output}")

                sql = projections_sql_template.format(
                    public_database=public_user.database,
                    projections_ds_id=projections_ds.id,
                    cluster=cluster["name"],
                    hours=24,
                )

                _, body = await client.query(
                    sql,
                    max_threads=1,
                    max_execution_time=120,
                    user_agent=UserAgents.BOOSTER.value,
                    allow_experimental_analyzer=0,  # TODO: Remove once 24.2 and ealier versions are deprecated from the CI
                )
                projections_data: List[Dict[str, Any]] = json.loads(body)["data"]

                projection_events = await booster.cleanup_projections(projections_data)
                for projection_event in projection_events:
                    raw_events_batcher.append_record(projection_event)

        except CHException as e:
            if e.code == CHErrors.TIMEOUT_EXCEEDED:
                logging.warning(f"{self.__class__.__name__}: {e}\nTraceback: {traceback.format_exc()}")
            else:
                logging.exception(f"{self.__class__.__name__}: {e}")

        except Exception as e:
            logging.exception(f"{self.__class__.__name__}: {e}")


@dataclass
class ConcurrencyAnalysisInfo:
    user_id: str
    name: str
    pipe_name: str
    database_server: str
    qps_estimated: int
    requests: int
    qps: int
    errors: int
    ok: int
    error_ok_ratio: float


CONCURRENCY_LIMITS: Dict[Tuple[str, str], Dict[str, Any]] = dict()
MINUTES_TO_CLEANUP = 5


class EndpointConcurrencyMonitorTask(MonitorTask):
    """
    Monitor task that tracks MemoryTracking to adjust concurrency of endpoints with errors.
    """

    def __init__(self) -> None:
        super().__init__(
            "endpoint_concurrency_monitor",
            task_frequency_in_seconds=15,
            single_instance_execution=True,
        )

    def terminate(self) -> None:
        logging.info(f"{self.__class__.__name__} terminate: {CONCURRENCY_LIMITS.keys()}")
        asyncio.run_coroutine_threadsafe(self.clean_up_limits(force=True), loop=self._asyncio_loop)
        super().terminate()

    async def clean_up_limits(self, force: bool = False) -> None:
        try:
            logging.info(f"{self.__class__.__name__} clean_up_limits: {CONCURRENCY_LIMITS.keys()}")
            for wp, value in CONCURRENCY_LIMITS.copy().items():
                try:
                    workspace_id, pipe_name = wp
                    timestamp = value["timestamp"]
                    now = datetime.now(timezone.utc)
                    difference = now - timestamp
                    if force or difference >= timedelta(minutes=MINUTES_TO_CLEANUP):
                        logging.info(f"{self.__class__.__name__} rollback max_concurrent_queries limit: {wp}")
                        key = EndpointLimits.get_limit_key(pipe_name, EndpointLimits.max_concurrent_queries)
                        await Workspaces.set_endpoint_limit(
                            Workspace.get_by_id(workspace_id),
                            key,
                            0,
                            pipe_name,
                            EndpointLimits.max_concurrent_queries.name,
                        )
                        del CONCURRENCY_LIMITS[wp]
                except Exception as e:
                    logging.exception(f"{self.__class__.__name__} clean_up_limits: {str(e)}")
        except Exception as e:
            logging.exception(f"{self.__class__.__name__} clean_up_limits: {str(e)}")

    def should_run(self) -> bool:
        if environ.get("PYTEST", None):
            logging.warning(f"{self.__class__.__name__} endpoint_concurrency_monitor disabled in pytest")
            return False
        return True

    async def get_cluster_settings(self) -> Tuple[List[str], List[str]]:
        all_cluster_settings = await asyncio.to_thread(ClusterSettings.get_all)
        cluster_dict = {
            str(cluster_settings.cluster_name): {
                "enabled": strtobool(
                    str(
                        cluster_settings.settings.get(ClusterSettingsOperations.ENDPOINT_CONCURRENCY_LIMITER, {})
                        .get("settings", {})
                        .get("enabled", "1")
                    )
                ),
                "dry_run": strtobool(
                    str(
                        cluster_settings.settings.get(ClusterSettingsOperations.ENDPOINT_CONCURRENCY_LIMITER, {})
                        .get("settings", {})
                        .get("dry_run", "0")
                    )
                ),
            }
            for cluster_settings in all_cluster_settings
        }

        async def _get_dedicated_clusters_with_no_cluster_settings():
            try:
                internal = public.get_public_user()
                client = HTTPClient(internal.database_server, database=internal.database)
                dedicated_infrastructure_metrics_logs = internal.get_datasource("dedicated_infrastructure_metrics_logs")
                assert dedicated_infrastructure_metrics_logs
                table_name = f"{internal.database}.{dedicated_infrastructure_metrics_logs.id}"
                _, body = await client.query(
                    f"SELECT distinct cluster FROM {table_name} where timestamp > now() - interval 20 second FORMAT JSON",
                    max_execution_time=5,
                    skip_unavailable_shards=1,
                )
                for cluster in json.loads(body)["data"]:
                    cluster_name = cluster.get("cluster")
                    if cluster_name not in cluster_dict:
                        cluster_dict[cluster_name] = {"enabled": 1, "dry_run": 0}
            except Exception as e:
                logging.exception(f"{self.__class__.__name__}: Exception getting list of clusters - {e}")

        await _get_dedicated_clusters_with_no_cluster_settings()
        cluster_names = [name for name, d in cluster_dict.items() if d["enabled"]]
        apply_limit_cluster_names = [name for name, d in cluster_dict.items() if not d["dry_run"]]
        return cluster_names, apply_limit_cluster_names

    async def run_query(self, cluster_names: List[str]) -> List[ConcurrencyAnalysisInfo]:
        try:
            here = path.abspath(path.dirname(__file__))

            internal = public.get_public_user()
            client = HTTPClient(internal.database_server, database=internal.database)

            async with aiofiles.open(path.join(here, "sql", "endpoint_concurrency_limiter.sql"), "r") as file:
                endpoint_concurrency_limiter_template = await file.read()
            pipe_stats_rt = internal.get_datasource("pipe_stats_rt")
            assert pipe_stats_rt
            workspaces_all = internal.get_datasource("workspaces_all")
            assert workspaces_all
            organizations_all_rt = internal.get_datasource("organizations_all_rt")
            assert organizations_all_rt
            dedicated_infrastructure_metrics_logs = internal.get_datasource("dedicated_infrastructure_metrics_logs")
            assert dedicated_infrastructure_metrics_logs
            quoted_cluster_names = [f"'{name}'" for name in cluster_names]
            cluster_names_str = f"({','.join(quoted_cluster_names)})"

            replacements = {
                "pipe_stats_rt": f"{internal.database}.{pipe_stats_rt.id}",
                "workspaces_all": f"{internal.database}.{workspaces_all.id}",
                "organizations_all_rt": f"{internal.database}.{organizations_all_rt.id}",
                "dedicated_infrastructure_metrics_logs": f"{internal.database}.{dedicated_infrastructure_metrics_logs.id}",
                "now": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                "cluster_names": cluster_names_str,
            }
            template = Template(endpoint_concurrency_limiter_template)
            endpoint_concurrency_limiter_sql = template.substitute(replacements)
            query_id = ulid.new().str
            logging.info(f"{self.__class__.__name__}: {query_id}")
            _, body = await client.query(
                endpoint_concurrency_limiter_sql,
                max_execution_time=5,
                skip_unavailable_shards=1,
                query_id=query_id,
            )
            response = [ConcurrencyAnalysisInfo(**elem) for elem in json.loads(body)["data"]]
            return response
        except CHException as e:
            if e.code == CHErrors.TIMEOUT_EXCEEDED:
                logging.warning(f"{self.__class__.__name__}: {query_id} - {e}\nTraceback: {traceback.format_exc()}")
            else:
                logging.exception(f"{self.__class__.__name__}: {query_id} - {e}")
            raise e

    async def apply_limits(self, data: List[ConcurrencyAnalysisInfo], apply_limit_cluster_names: List[str]):
        for elem in data:
            try:
                ws_id = elem.user_id
                w = Workspace.get_by_id(ws_id)
                pipe_name = elem.pipe_name
                cluster = w.cluster
                if cluster not in apply_limit_cluster_names:
                    logging.info(f"{self.__class__.__name__}: {cluster} is in dry_run mode")
                    continue

                pipe = w.get_pipe(pipe_name)
                if not pipe and pipe_name not in ["query_api", "query_api_from_ui"]:
                    logging.info(f"{self.__class__.__name__}: Pipe not found {pipe_name}")
                    continue
                if pipe_name == "query_api":
                    pipe_name = QUERY_API
                elif pipe_name == "query_api_from_ui":
                    continue

                max_concurrent_queries = max(1, int(elem.qps_estimated))
                key = EndpointLimits.get_limit_key(pipe_name, EndpointLimits.max_concurrent_queries)

                await Workspaces.set_endpoint_limit(
                    w, key, max_concurrent_queries, pipe_name, EndpointLimits.max_concurrent_queries.name
                )
                email_sent = (w.id, pipe_name) in CONCURRENCY_LIMITS
                CONCURRENCY_LIMITS[(w.id, pipe_name)] = {
                    "timestamp": datetime.now(timezone.utc),
                    "email_sent": email_sent,
                }

                logging.info(
                    f"{self.__class__.__name__}: max_concurrent_queries limit for {cluster} - {w.name} - {pipe_name} - {max_concurrent_queries}"
                )
            except Exception as e:
                logging.info(
                    f"{self.__class__.__name__}: Error when setting max_concurrent_queries limit for {cluster} - {w.name} - {pipe_name} => {str(e)}"
                )
        logging.info(f"{self.__class__.__name__} current limits: {CONCURRENCY_LIMITS}")

    async def send_slack_notification(self, data: List[ConcurrencyAnalysisInfo], apply_limit_cluster_names: List[str]):
        message = []
        for item in data:
            workspace = Workspace.get_by_id(item.user_id)
            msg_dry_run = "[DRY_RUN]" if workspace.cluster not in apply_limit_cluster_names else ""
            message.append(f"{msg_dry_run} {str(item)}")

        slack_message = ("\n\n").join(message)
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url="https://hooks.slack.com/services/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",
                headers={"Content-type": "application/json"},
                data=json.dumps(
                    {
                        "type": "mrkdwn",
                        "text": slack_message,
                    }
                ),
                timeout=aiohttp.ClientTimeout(total=self.task_frequency_in_seconds),
            ) as response:
                text = await response.text()
                if response.status >= 400:
                    logging.warning(
                        f"{self.__class__.__name__}: Failed send notification to Slack: {response.status} - {text}"
                    )

    async def send_email(self, data: List[ConcurrencyAnalysisInfo], apply_limit_cluster_names: List[str]):
        try:
            result = defaultdict(list)
            for item in data:
                if item.pipe_name == "query_api":
                    continue
                key = (item.user_id, item.pipe_name)
                if not CONCURRENCY_LIMITS.get(key, {}).get("email_sent"):
                    result[item.user_id].append((item.pipe_name, item.qps_estimated))

            for workspace_id, pipes_concurrency in dict(result).items():
                workspace = Workspace.get_by_id(workspace_id)
                if workspace.cluster not in apply_limit_cluster_names:
                    continue

                user_workspaces = UserWorkspaceRelationship.get_by_workspace(workspace.id, workspace.max_seats_limit)
                owners = [uw for uw in user_workspaces if uw.relationship == Relationships.ADMIN]
                if not len(owners):
                    continue

                user_accounts = []
                for owner in owners:
                    owner_user = UserAccount.get_by_id(owner.user_id)
                    if not owner_user:
                        logging.exception(f"{self.__class__.__name__}: User {owner.user_id} not found")
                        continue
                    user_accounts.append(owner_user)

                response = await NotificationsService.notify_max_concurrent_queries_limit(
                    user_accounts, workspace, pipes_concurrency
                )
                if key in CONCURRENCY_LIMITS:
                    CONCURRENCY_LIMITS[key]["email_sent"] = True
                logging.info(
                    f"{self.__class__.__name__}: Email sent: {workspace.name} - {pipes_concurrency} - {response}"
                )
        except Exception as e:
            logging.exception(f"{self.__class__.__name__}: Error sending email: {str(e)}")

    async def notify(self, data: List[ConcurrencyAnalysisInfo], apply_limit_cluster_names: List[str]):
        await self.send_slack_notification(data, apply_limit_cluster_names)
        await self.send_email(data, apply_limit_cluster_names)

    async def action(self) -> None:
        try:
            if not self.should_run():
                return

            cluster_names, apply_limit_cluster_names = await self.get_cluster_settings()
            if not len(cluster_names):
                return
            logging.info(f"{self.__class__.__name__}: Enabled clusters - {cluster_names}")
            logging.info(f"{self.__class__.__name__}: Apply limit clusters - {apply_limit_cluster_names}")

            response = await self.run_query(cluster_names)
            if not len(response):
                logging.info(f"{self.__class__.__name__}: No data found")
                return

            await self.apply_limits(response, apply_limit_cluster_names)
            await self.notify(response, apply_limit_cluster_names)
        except Exception as e:
            logging.exception(f"{self.__class__.__name__}: {e}")
        finally:
            await self.clean_up_limits()


class DedicatedInfrastructureMetricRecord(BaseModel):
    timestamp: datetime
    organization_id: str
    metric: str
    host: str
    cluster: str
    value: str
    description: str


class DedicatedInfrastructureMonitorTask(MonitorTask):
    """
    This monitor task is responsible for monitoring the clusters with dedicated infrastructure, gather metrics of the clusters and append them into Internal workspace.
    """

    def __init__(self, hfi_host: str) -> None:
        super().__init__(
            "dedicated_infrastructure_monitor",
            task_frequency_in_seconds=DEDICATED_INFRA_METRICS_TASK_FREQ_IN_SECONDS,
            single_instance_execution=True,
        )
        self.hfi_host = hfi_host
        self.datasource_name = "dedicated_infrastructure_metrics_logs"
        self.append_url = f"{hfi_host}/v0/events"

    # TODO: We should have a class to handle appending to Internal datasources
    async def append_metrics_records(self, metrics: List[DedicatedInfrastructureMetricRecord]) -> None:
        # TODO: We try to get the token from the datasource, but if it doesn't exist we get the admin token from the Internal workspace.
        # This is for running this locally
        # We should fix this to not need to run this locally
        token = get_datasource_append_token(self.datasource_name)
        if token is None:
            logging.warning(f"get_datasource_append_token returned None for '{self.datasource_name}' datasource")
            token = get_internal_admin_token()

        if not token:
            logging.warning(
                f"No token found for the '{self.datasource_name}' datasource or admin token in the 'Internal' workspace"
            )
            statsd_client.incr(f"tinybird.{statsd_client.region}.cluster_metrics_append.failure")
            return

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url=self.append_url,
                    params={"token": token, "name": self.datasource_name},
                    data="\n".join(record.model_dump_json() for record in metrics).encode(errors="replace"),
                    timeout=aiohttp.ClientTimeout(total=self.task_frequency_in_seconds),
                ) as response:
                    text = await response.text()
                    if response.status in [200, 202]:
                        statsd_client.incr(f"tinybird.{statsd_client.region}.cluster_metrics_append.success")
                    else:
                        logging.warning(
                            f"Failed to append metrics to the dedicated infrastructure metrics datasource: {response.status} - {text}"
                        )
                        statsd_client.incr(f"tinybird.{statsd_client.region}.cluster_metrics_append.failure")
        except Exception as e:
            logging.warning(f"Error appending metrics to the dedicated infrastructure metrics datasource: {e}")
            statsd_client.incr(f"tinybird.{statsd_client.region}.cluster_metrics_append.failure")

    async def action(self) -> None:
        organizations_with_cluster_metrics_exposed: List[Organization] = [
            o for o in await Organization.get_all_async() if len(o.get_dedicated_clusters_exposing_metrics()) > 0
        ]

        all_metrics_records: List[DedicatedInfrastructureMetricRecord] = []
        for organization in organizations_with_cluster_metrics_exposed:
            cluster_metrics = await organization.get_cluster_metrics()
            all_metrics_records.extend(
                DedicatedInfrastructureMetricRecord(
                    timestamp=cluster_metric.timestamp,
                    organization_id=organization.id,
                    metric=cluster_metric.metric,
                    host=cluster_metric.host,
                    cluster=cluster_metric.cluster,
                    value=cluster_metric.value,
                    description=cluster_metric.description,
                )
                for cluster_metric in cluster_metrics
            )
        await self.append_metrics_records(all_metrics_records)


# Birdwatcher mapper is not available in the backend. Adding it like this as it's only expected to be used during the development of this Alert.
BIRDWATCHER_REGION_URL_MAPPER: Dict[str, str] = {
    "ap-east-aws": "AWS-AP-EAST",
    "aws-eu-central-1": "AWS-EU",
    "aws-split-us-east": "SPLIT",
    "us-east-aws": "AWS-US-EAST",
    "aws-us-west-2": "AWS-US-WEST",
    "eu_shared": "GCP-EU",
    "us_east": "GCP-US-EAST",
    "itx_c_pro": "ITX-C",
    "itx_c_stg": "ITX-C-STG",
    "itx_z_stg": "ITX-Z-STG",
    "itx_tech": "ITX-TECH",
    "itx_z_pro": "ITX-DRIVE",
    "itx_z_rt_pro": "ITX-RT",
}


class CpuTimeOveruseMonitorTaskBaseClass(MonitorTask):
    """
    This monitor task is responsible for monitoring the CPU time overuse in the clusters.
    """

    def __init__(self, name: str, task_frequency_in_seconds: int, region: str, clusters: Dict[str, str]) -> None:
        super().__init__(
            name,
            task_frequency_in_seconds,
            single_instance_execution=True,
        )
        self._region = region
        self._clusters = clusters
        self._list_of_regions_where_the_monitor_should_not_run = [
            "ap-east-aws",
            "aws-split-us-east",
            "itx_c_pro",
            "itx_c_stg",
            "itx_z_stg",
            "itx_tech",
            "itx_z_pro",
            "itx_z_rt_pro",
        ]
        self._slack_channel_webhook_url = (
            "https://hooks.slack.com/services/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"
        )

    async def _send_slack_message(self, message: str) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=self._slack_channel_webhook_url,
                headers={"Content-type": "application/json"},
                data=json.dumps(
                    {
                        "type": "mrkdwn",
                        "text": message,
                    }
                ),
                timeout=aiohttp.ClientTimeout(total=self.task_frequency_in_seconds),
            ) as response:
                text = await response.text()
                if response.status >= 400:
                    logging.warning(
                        f"{self.__class__.__name__}: Failed send notification to Slack: {response.status} - {text}"
                    )

    async def _build_query_for_5_minutes_window(self, ch_cluster: str, time_window_in_seconds: int) -> str:
        sql = f"""
SELECT 
    current_database,
    long_window_start,
    max(total_cpu_time_in_lw) as cpu_time_in_long_window,
    
    -- 0.25 vCPU alerts
    sum(0_25_vCPU_cpu_overage_exceeded_alert) as 0_25_cpu,
    sum(0_25_vCPU_interval_burst_exceeded_alert) as 0_25_intervals,
    -- 0.5 vCPU alerts
    sum(0_5_vCPU_cpu_overage_exceeded_alert) as 0_5_cpu,
    sum(0_5_vCPU_interval_burst_exceeded_alert) as 0_5_intervals,
    -- 1 vCPU alerts
    sum(1_vCPU_cpu_overage_exceeded_alert) as 1_cpu,
    sum(1_vCPU_interval_burst_exceeded_alert) as 1_intervals,
    -- 2 vCPU alerts
    sum(2_vCPU_cpu_overage_exceeded_alert) as 2_cpu,
    sum(2_vCPU_interval_burst_exceeded_alert) as 2_intervals,
    -- 3 vCPU alerts
    sum(3_vCPU_cpu_overage_exceeded_alert) as 3_cpu,
    sum(3_vCPU_interval_burst_exceeded_alert) as 3_intervals,
    -- 4 vCPU alerts
    sum(4_vCPU_cpu_overage_exceeded_alert) as 4_cpu,
    sum(4_vCPU_interval_burst_exceeded_alert) as 4_intervals
FROM (
    WITH 
        -- Interval definitions
        5 AS short_window_seconds,
        300 AS long_window_seconds,
        (long_window_seconds / short_window_seconds) AS total_intervals,
        (total_intervals * 0.2) AS burst_intervals, -- 20% burst allowance

        -- CPU allowance for 0.25 vCPU
        0.25 AS 0_25_vCPU,
        0_25_vCPU * short_window_seconds as 0_25_vCPU_cpu_time_allowed_short,
        0_25_vCPU * long_window_seconds as 0_25_vCPU_cpu_time_allowed_long,
        (0_25_vCPU_cpu_time_allowed_long * 0.2) AS 0_25_vCPU_cpu_burst,

        -- CPU allowance for 0.5 vCPU
        0.5 AS 0_5_vCPU,
        0_5_vCPU * short_window_seconds as 0_5_vCPU_cpu_time_allowed_short,
        0_5_vCPU * long_window_seconds as 0_5_vCPU_cpu_time_allowed_long,
        (0_5_vCPU_cpu_time_allowed_long * 0.2) AS 0_5_vCPU_cpu_burst,

        -- CPU allowance for 1 vCPU
        1 AS 1_vCPU, -- simulating a 1 CPU plan
        1_vCPU * short_window_seconds as 1_vCPU_cpu_time_allowed_short,
        1_vCPU * long_window_seconds as 1_vCPU_cpu_time_allowed_long,
        (1_vCPU_cpu_time_allowed_long * 0.2) AS 1_vCPU_cpu_burst,

        -- CPU allowance for 2 vCPU
        2 AS 2_vCPU, -- simulating a 2 CPU plan
        2_vCPU * short_window_seconds as 2_vCPU_cpu_time_allowed_short,
        2_vCPU * long_window_seconds as 2_vCPU_cpu_time_allowed_long,
        (2_vCPU_cpu_time_allowed_long * 0.2) AS 2_vCPU_cpu_burst,

        -- CPU allowance for 3 vCPU
        3 AS 3_vCPU, -- simulating a 3 CPU plan
        3_vCPU * short_window_seconds as 3_vCPU_cpu_time_allowed_short,
        3_vCPU * long_window_seconds as 3_vCPU_cpu_time_allowed_long,
        (3_vCPU_cpu_time_allowed_long * 0.2) AS 3_vCPU_cpu_burst,

        -- CPU allowance for 4 vCPU
        4 AS 4_vCPU, -- simulating a 4 CPU plan
        4_vCPU * short_window_seconds as 4_vCPU_cpu_time_allowed_short,
        4_vCPU * long_window_seconds as 4_vCPU_cpu_time_allowed_long,
        (4_vCPU_cpu_time_allowed_long * 0.2) AS 4_vCPU_cpu_burst
    SELECT 
        current_database,
        toStartOfInterval(time_point, INTERVAL 5 second) as short_window_start,
        toStartOfFiveMinutes(time_point) as long_window_start,
        -- Base CPU metrics
        round(sum(cpu_time_in_s_total), 2) as cpu_time_in_sw,
        round(sum(cpu_time_in_sw) OVER long_window ,2) as total_cpu_time_in_lw,

        -- 0.25 vCPU Overage calculations
        round(if(cpu_time_in_sw > 0_25_vCPU_cpu_time_allowed_short,
            cpu_time_in_sw - 0_25_vCPU_cpu_time_allowed_short,
            0) ,2) as 0_25_vCPU_cpu_time_overage,
        -- 0.25 vCPU Token calculations
        if(cpu_time_in_sw > 0_25_vCPU_cpu_time_allowed_short, 1, 0) as 0_25_vCPU_interval_exceeded,
        round(sum(0_25_vCPU_cpu_time_overage) OVER long_window ,2) as 0_25_vCPU_total_cpu_time_overage_in_lw,
        sum(0_25_vCPU_interval_exceeded) OVER long_window as 0_25_vCPU_total_interval_exceeded_in_lw,
        -- 0.25 vCPU Alerts raised
        if(0_25_vCPU_total_cpu_time_overage_in_lw > 0_25_vCPU_cpu_burst, 1, 0) as 0_25_vCPU_cpu_overage_exceeded_alert,
        if(0_25_vCPU_total_interval_exceeded_in_lw > burst_intervals, 1, 0) as 0_25_vCPU_interval_burst_exceeded_alert,

        -- 0.5 vCPU Overage calculations
        round(if(cpu_time_in_sw > 0_5_vCPU_cpu_time_allowed_short,
            cpu_time_in_sw - 0_5_vCPU_cpu_time_allowed_short,
            0) ,2) as 0_5_vCPU_cpu_time_overage,
        -- 0.5 vCPU Token calculations
        if(cpu_time_in_sw > 0_5_vCPU_cpu_time_allowed_short, 1, 0) as 0_5_vCPU_interval_exceeded,
        round(sum(0_5_vCPU_cpu_time_overage) OVER long_window ,2) as 0_5_vCPU_total_cpu_time_overage_in_lw,
        sum(0_5_vCPU_interval_exceeded) OVER long_window as 0_5_vCPU_total_interval_exceeded_in_lw,
        -- 0.5 vCPU Alerts raised
        if(0_5_vCPU_total_cpu_time_overage_in_lw > 0_5_vCPU_cpu_burst, 1, 0) as 0_5_vCPU_cpu_overage_exceeded_alert,
        if(0_5_vCPU_total_interval_exceeded_in_lw > burst_intervals, 1, 0) as 0_5_vCPU_interval_burst_exceeded_alert,

        -- 1 vCPU Overage calculations
        round(if(cpu_time_in_sw > 1_vCPU_cpu_time_allowed_short,
            cpu_time_in_sw - 1_vCPU_cpu_time_allowed_short,
            0) ,2) as 1_vCPU_cpu_time_overage,
        -- 1 vCPU Token calculations  
        if(cpu_time_in_sw > 1_vCPU_cpu_time_allowed_short, 1, 0) as 1_vCPU_interval_exceeded,
        round(sum(1_vCPU_cpu_time_overage) OVER long_window ,2) as 1_vCPU_total_cpu_time_overage_in_lw,
        sum(1_vCPU_interval_exceeded) OVER long_window as 1_vCPU_total_interval_exceeded_in_lw,
        -- 1 vCPU Alerts raised
        if(1_vCPU_total_cpu_time_overage_in_lw > 1_vCPU_cpu_burst, 1, 0) as 1_vCPU_cpu_overage_exceeded_alert,
        if(1_vCPU_total_interval_exceeded_in_lw > burst_intervals, 1, 0) as 1_vCPU_interval_burst_exceeded_alert,

        -- 2 vCPU Overage calculations
        round(if(cpu_time_in_sw > 2_vCPU_cpu_time_allowed_short,
            cpu_time_in_sw - 2_vCPU_cpu_time_allowed_short,
            0) ,2) as 2_vCPU_cpu_time_overage,
        -- 2 vCPU Token calculations
        if(cpu_time_in_sw > 2_vCPU_cpu_time_allowed_short, 1, 0) as 2_vCPU_interval_exceeded,
        round(sum(2_vCPU_cpu_time_overage) OVER long_window ,2) as 2_vCPU_total_cpu_time_overage_in_lw,
        sum(2_vCPU_interval_exceeded) OVER long_window as 2_vCPU_total_interval_exceeded_in_lw,
        -- 2 vCPU Alerts raised
        if(2_vCPU_total_cpu_time_overage_in_lw > 2_vCPU_cpu_burst, 1, 0) as 2_vCPU_cpu_overage_exceeded_alert,
        if(2_vCPU_total_interval_exceeded_in_lw > burst_intervals, 1, 0) as 2_vCPU_interval_burst_exceeded_alert,

        -- 3 vCPU Overage calculations
        round(if(cpu_time_in_sw > 3_vCPU_cpu_time_allowed_short,
            cpu_time_in_sw - 3_vCPU_cpu_time_allowed_short,
            0) ,2) as 3_vCPU_cpu_time_overage,
        -- 3 vCPU Token calculations
        if(cpu_time_in_sw > 3_vCPU_cpu_time_allowed_short, 1, 0) as 3_vCPU_interval_exceeded,
        round(sum(3_vCPU_cpu_time_overage) OVER long_window ,2) as 3_vCPU_total_cpu_time_overage_in_lw,
        sum(3_vCPU_interval_exceeded) OVER long_window as 3_vCPU_total_interval_exceeded_in_lw,
        -- 3 vCPU Alerts raised
        if(3_vCPU_total_cpu_time_overage_in_lw > 3_vCPU_cpu_burst, 1, 0) as 3_vCPU_cpu_overage_exceeded_alert,
        if(3_vCPU_total_interval_exceeded_in_lw > burst_intervals, 1, 0) as 3_vCPU_interval_burst_exceeded_alert,

        -- 4 vCPU Overage calculations
        round(if(cpu_time_in_sw > 4_vCPU_cpu_time_allowed_short,
            cpu_time_in_sw - 4_vCPU_cpu_time_allowed_short,
            0) ,2) as 4_vCPU_cpu_time_overage,
        -- 4 vCPU Token calculations
        if(cpu_time_in_sw > 4_vCPU_cpu_time_allowed_short, 1, 0) as 4_vCPU_interval_exceeded,
        round(sum(4_vCPU_cpu_time_overage) OVER long_window ,2) as 4_vCPU_total_cpu_time_overage_in_lw,
        sum(4_vCPU_interval_exceeded) OVER long_window as 4_vCPU_total_interval_exceeded_in_lw,
        -- 4 vCPU Alerts raised
        if(4_vCPU_total_cpu_time_overage_in_lw > 4_vCPU_cpu_burst, 1, 0) as 4_vCPU_cpu_overage_exceeded_alert,
        if(4_vCPU_total_interval_exceeded_in_lw > burst_intervals, 1, 0) as 4_vCPU_interval_burst_exceeded_alert

    FROM (
        -- Logs from query_log expanded to spread CPU usage along time.
        SELECT
            current_database,
            time_point,
            sum(cpu_time_in_s / total_seconds) AS cpu_time_in_s_total
        FROM (
            -- Filtered events from query log.
            SELECT
                current_database,
                start_time,
                end_time,
                cpu_time_in_s,
                toUInt32(dateDiff('second', start_time, end_time)) + 1 AS total_seconds,
                arrayMap(x -> (start_time + x), range(total_seconds)) AS time_points
            FROM
            (
                SELECT
                    splitByString('__', current_database)[1] as current_database,
                    event_time AS start_time,
                    addMilliseconds(event_time, query_duration_ms) AS end_time,
                    (ProfileEvents['OSCPUVirtualTimeMicroseconds']) / 1000000. AS cpu_time_in_s
                FROM clusterAllReplicas({ch_cluster}, system.query_log)
                WHERE (event_date = today()) 
                    AND (event_time > toStartOfInterval(now() - INTERVAL {time_window_in_seconds} SECOND, INTERVAL 5 MINUTE))
                    AND (type >= 2) 
                    AND (current_database NOT IN ('system', 'default'))
                    AND (http_user_agent != 'tb-internal-query')
            )
        )
        ARRAY JOIN time_points AS time_point
        GROUP BY current_database, time_point
    )
    GROUP BY current_database, short_window_start, long_window_start
        WINDOW
        long_window AS (
            PARTITION BY current_database, long_window_start 
            ORDER BY short_window_start
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        )
    ORDER BY current_database, short_window_start
)
WHERE 
    0_25_vCPU_cpu_overage_exceeded_alert = 1 OR 0_25_vCPU_interval_burst_exceeded_alert = 1 OR
    0_5_vCPU_cpu_overage_exceeded_alert = 1 OR 0_5_vCPU_interval_burst_exceeded_alert = 1 OR
    1_vCPU_cpu_overage_exceeded_alert = 1 OR 1_vCPU_interval_burst_exceeded_alert = 1 OR
    2_vCPU_cpu_overage_exceeded_alert = 1 OR 2_vCPU_interval_burst_exceeded_alert = 1 OR
    3_vCPU_cpu_overage_exceeded_alert = 1 OR 3_vCPU_interval_burst_exceeded_alert = 1 OR
    4_vCPU_cpu_overage_exceeded_alert = 1 OR 4_vCPU_interval_burst_exceeded_alert = 1
GROUP BY current_database, long_window_start
ORDER BY current_database, long_window_start
"""
        return sql

    async def _execute_query(self, sql: str, database_server: str) -> List[Any]:
        client = HTTPClient(database_server)
        sql = f"{sql} FORMAT JSON"
        _, body = await client.query(
            sql,
            read_only=True,
            max_threads=1,
            skip_unavailable_shards=1,
            max_execution_time=30,
            user_agent=UserAgents.CPU_TIME_ALERT.value,
        )
        return json.loads(body)["data"]

    async def _get_public_clusters_hosts(self) -> Dict[str, str]:
        public_clusters: Dict[str, str] = {}
        for cluster_name, varnish_host in self._clusters.items():
            # Public clusters have different names in each region. Adding exceptions to cover all of them:
            if "public" in cluster_name or "common" in cluster_name or cluster_name in ("us_east", "us_east_2"):
                public_clusters[cluster_name] = varnish_host
        return public_clusters

    async def _skip_region(self) -> bool:
        return self._region in self._list_of_regions_where_the_monitor_should_not_run or "wadus" in self._region


class CpuTimeOveruseMonitorTaskHourly(CpuTimeOveruseMonitorTaskBaseClass):
    def __init__(self, region: str, clusters: Dict[str, str]) -> None:
        super().__init__(
            "cpu_time_overuse_monitor_hourly",
            task_frequency_in_seconds=3600,
            region=region,
            clusters=clusters,
        )

    async def action(self) -> None:
        if await self._skip_region():
            return

        public_clusters = await self._get_public_clusters_hosts()

        for ch_cluster, varnish_host in public_clusters.items():
            sql = await self._build_query_for_5_minutes_window(ch_cluster, time_window_in_seconds=3600)

            try:
                workspaces_with_overuse = await self._execute_query(sql, database_server=varnish_host)
            except CHException as e:
                if e.code == CHErrors.TIMEOUT_EXCEEDED:
                    logging.warning(f"{self.__class__.__name__}: {e}\nTraceback: {traceback.format_exc()}")
                    continue
                else:
                    raise e

            if not workspaces_with_overuse:
                slack_message = "*###*\n"
                slack_message += (
                    f"*### {ch_cluster}: No Workspaces found with overuse in the last hour using burst algorithm*\n"
                )
                slack_message += "*###*\n"
                await self._send_slack_message(slack_message)
                continue

            reports_per_database = defaultdict(list)
            slack_message = "*###*\n"
            slack_message += f"*### Workspaces with overuse in {ch_cluster} in the last hour using burst algorithm:*\n"
            slack_message += "*###*\n"
            for report_line in workspaces_with_overuse:
                current_database = report_line.pop("current_database")
                reports_per_database[current_database].append(report_line)

            for database_report in reports_per_database:
                ws = Workspace.get_by_database(database_report)

                slack_message += f"*Workspace {ws.name}/{ws.id}/{ws.database}:*\n"
                birdwatcher_region = BIRDWATCHER_REGION_URL_MAPPER.get(self._region, "")
                if not birdwatcher_region:
                    logging.error(f"Birdwatcher region not found in mapper: {self._region}")
                slack_message += f" - Birdwatcher URL: https://birdwatcher.tinybird.co/?workspaces={ws.id}-{birdwatcher_region} (region in URL may not be correct) \n"

                reports = reports_per_database[database_report]
                # Format the reports into a pretty table
                headers = [
                    "Time Window Start",
                    "CPU Time (s)",
                    "0.25 CPU",
                    "0.25 Intervals",
                    "0.5 CPU",
                    "0.5 Intervals",
                    "1 CPU",
                    "1 Intervals",
                    "2 CPU",
                    "2 Intervals",
                    "3 CPU",
                    "3 Intervals",
                    "4 CPU",
                    "4 Intervals",
                ]

                rows = [
                    [
                        str(r["long_window_start"]),
                        str(r["cpu_time_in_long_window"]),
                        str(r["0_25_cpu"]),
                        str(r["0_25_intervals"]),
                        str(r["0_5_cpu"]),
                        str(r["0_5_intervals"]),
                        str(r["1_cpu"]),
                        str(r["1_intervals"]),
                        str(r["2_cpu"]),
                        str(r["2_intervals"]),
                        str(r["3_cpu"]),
                        str(r["3_intervals"]),
                        str(r["4_cpu"]),
                        str(r["4_intervals"]),
                    ]
                    for r in reports
                ]
                formatted_table = format_pretty_table(rows, headers)
                formatted_table = re.sub(r"\x1b\[[0-9;]*[a-zA-Z]", "", formatted_table)
                slack_message += "\n```\n" + formatted_table + "\n```\n"

            await self._send_slack_message(slack_message)


class CpuTimeOveruseMonitorTaskDaily(CpuTimeOveruseMonitorTaskBaseClass):
    def __init__(self, region: str, clusters: Dict[str, str]) -> None:
        super().__init__(
            "cpu_time_overuse_monitor_daily",
            task_frequency_in_seconds=86400,
            region=region,
            clusters=clusters,
        )

    async def _build_query_for_daily_summary(self, ch_cluster: str, time_window_in_seconds: int) -> str:
        five_minute_query = await self._build_query_for_5_minutes_window(ch_cluster, time_window_in_seconds)

        sql = f"""
        SELECT
            current_database,
            avg(cpu_time_in_long_window) as avg_cpu_in_alerted_intervals,
            countIf(0_25_cpu > 0) as 0_25_cpu_alerts,
            countIf(0_25_intervals > 0) as 0_25_intervals_alerts,
            countIf(0_5_cpu > 0) as 0_5_cpu_alerts,
            countIf(0_5_intervals > 0) as 0_5_intervals_alerts,
            countIf(1_cpu > 0) as 1_cpu_alerts,
            countIf(1_intervals > 0) as 1_intervals_alerts,
            countIf(2_cpu > 0) as 2_cpu_alerts,
            countIf(2_intervals > 0) as 2_intervals_alerts,
            countIf(3_cpu > 0) as 3_cpu_alerts,
            countIf(3_intervals > 0) as 3_intervals_alerts,
            countIf(4_cpu > 0) as 4_cpu_alerts,
            countIf(4_intervals > 0) as 4_intervals_alerts
        FROM (
            {five_minute_query}
        ) GROUP BY current_database
        """
        return sql

    async def action(self) -> None:
        if await self._skip_region():
            return

        public_clusters = await self._get_public_clusters_hosts()

        for ch_cluster, varnish_host in public_clusters.items():
            sql = await self._build_query_for_daily_summary(ch_cluster, time_window_in_seconds=3600)

            try:
                workspaces_with_overuse = await self._execute_query(sql, database_server=varnish_host)
            except CHException as e:
                if e.code == CHErrors.TIMEOUT_EXCEEDED:
                    logging.warning(f"{self.__class__.__name__}: {e}\nTraceback: {traceback.format_exc()}")
                    continue
                else:
                    raise e

            if not workspaces_with_overuse:
                slack_message = "*###*\n"
                slack_message += f"*### Daily summary for {ch_cluster}: No Workspaces found with overuse in the last 24 hours using burst algorithm*\n"
                slack_message += "*###*\n"
                await self._send_slack_message(slack_message)
                continue

            reports_per_database = defaultdict(list)
            slack_message = "*###*\n"
            slack_message += f"*### Daily summary for {ch_cluster}: Workspaces with overuse in the last 24 hours using burst algorithm:*\n"
            slack_message += "*###*\n"
            for report_line in workspaces_with_overuse:
                current_database = report_line.pop("current_database")
                reports_per_database[current_database].append(report_line)

            for database_report in reports_per_database:
                ws = Workspace.get_by_database(database_report)

                slack_message += f"*Workspace {ws.name}/{ws.id}/{ws.database}:*\n"
                birdwatcher_region = BIRDWATCHER_REGION_URL_MAPPER.get(self._region, "")
                if not birdwatcher_region:
                    logging.error(f"Birdwatcher region not found in mapper: {self._region}")
                slack_message += f" - Birdwatcher URL: https://birdwatcher.tinybird.co/?workspaces={ws.id}-{birdwatcher_region} (region in URL may not be correct) \n"

                reports = reports_per_database[database_report]
                # Format the reports into a pretty table
                headers = [
                    "Database",
                    "Avg CPU during alerts",
                    "0.25 CPU Alerts",
                    "0.25 Interval Alerts",
                    "0.5 CPU",
                    "0.5 Interval",
                    "1 CPU",
                    "1 Interval",
                    "2 CPU",
                    "2 Interval",
                    "3 CPU",
                    "3 Interval",
                    "4 CPU",
                    "4 Interval",
                ]

                rows = [
                    [
                        str(database_report),
                        str(r["avg_cpu_in_alerted_intervals"]),
                        str(r["0_25_cpu_alerts"]),
                        str(r["0_25_intervals_alerts"]),
                        str(r["0_5_cpu_alerts"]),
                        str(r["0_5_intervals_alerts"]),
                        str(r["1_cpu_alerts"]),
                        str(r["1_intervals_alerts"]),
                        str(r["2_cpu_alerts"]),
                        str(r["2_intervals_alerts"]),
                        str(r["3_cpu_alerts"]),
                        str(r["3_intervals_alerts"]),
                        str(r["4_cpu_alerts"]),
                        str(r["4_intervals_alerts"]),
                    ]
                    for r in reports
                ]
                formatted_table = format_pretty_table(rows, headers)
                formatted_table = re.sub(r"\x1b\[[0-9;]*[a-zA-Z]", "", formatted_table)
                slack_message += "\n```\n" + formatted_table + "\n```\n"

            await self._send_slack_message(slack_message)
