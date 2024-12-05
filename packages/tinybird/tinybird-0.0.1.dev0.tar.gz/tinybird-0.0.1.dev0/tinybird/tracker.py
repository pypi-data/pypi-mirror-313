import asyncio
import json
import logging
import os
import re
import threading
import traceback
import uuid
from collections import defaultdict
from dataclasses import dataclass, fields
from datetime import datetime, timedelta, timezone
from queue import PriorityQueue
from time import monotonic, time
from typing import Any, Dict, List, NamedTuple, Optional, Tuple, Union

import orjson
import requests.exceptions

from tinybird.ch import CHException, HTTPClient, ch_get_ops_log_extended_data_by_query_id
from tinybird.csv_tools import csv_from_python_object
from tinybird.datasource import Datasource
from tinybird.distributed import WorkingGroup
from tinybird.gatherer_common import (
    GATHERER_DYNAMODBSTREAMS_SOURCE_TAG,
    GATHERER_HFI_SOURCE_TAG,
    GATHERER_JOB_PROCESSOR_SOURCE_TAG,
    GATHERER_KAFKA_SOURCE_TAG,
)
from tinybird.model import batched
from tinybird_shared.metrics.statsd_client import statsd_client
from tinybird_shared.redis_client.redis_client import TBRedisClientSync, TBRedisConfig
from tinybird_shared.retry.retry import retry_sync

from .sql_toolset import sql_get_used_tables
from .table import append_data_to_table
from .user import User as Workspace
from .user import UserDoesNotExist as WorkspaceDoesNotExist
from .user import public
from .views.api_errors.utils import replace_table_id_with_datasource_id

DATASOURCES_OPS_LOG_TRACKER_SLEEP_TIME = 0.5
CDK_SOURCES = ["https://storage.googleapis.com/dev-cdk-data", "https://storage.googleapis.com/tinybird-cdk-production"]


class HookLogEntry(NamedTuple):
    hook_id: str
    name: str
    operation: str
    datasource_id: Optional[str]
    datasource_name: Optional[str]
    workspace_id: str
    workspace_email: str
    timestamp: Union[int, float]
    elapsed: float
    status: str
    error: Optional[str]


HookLogEntries = List[HookLogEntry]


def track_hooks(
    hooks_logs_entries: HookLogEntries,
    request_id: Optional[str] = None,
    import_id: Optional[str] = None,
    job_id: Optional[str] = None,
    source: Optional[str] = None,
    workspace: Optional[Workspace] = None,
) -> None:
    rows = []
    for hook_log_entry in hooks_logs_entries:
        error = hook_log_entry.error
        if workspace:
            error = replace_table_id_with_datasource_id(
                workspace, error, error_datasource_id=hook_log_entry.datasource_id
            )
        rows.append(
            (
                datetime.fromtimestamp(hook_log_entry.timestamp),
                request_id,
                import_id,
                job_id,
                source or "",
                hook_log_entry.hook_id,
                hook_log_entry.name,
                hook_log_entry.operation,
                hook_log_entry.status,
                hook_log_entry.workspace_id,
                hook_log_entry.workspace_email,
                hook_log_entry.datasource_id,
                hook_log_entry.datasource_name,
                hook_log_entry.elapsed,
                error,
            )
        )
    u = public.get_public_user()
    t = u.get_datasource("hook_log")
    if not t:
        raise Exception("hook_log Data Source not found in the public user")
    append_data_to_table(
        database_server=u.database_server,
        database=u.database,
        cluster=u.cluster,
        table_name=t.id,
        rows=rows,
        with_quarantine=False,
    )


@dataclass
class OpsLogEntry:
    start_time: datetime
    event_type: str
    datasource_id: str
    datasource_name: str
    workspace_id: str
    workspace_email: str
    result: str
    elapsed_time: float
    error: Optional[str]
    rows: int
    rows_quarantine: int
    options: Dict[Any, Any]
    use_tracker: bool = False
    update_with_blocks: bool = False
    pipe_id: Optional[str] = None
    pipe_name: Optional[str] = None


OpsLogEntries = List[OpsLogEntry]


@dataclass
class DatasourceOpsLogRecord:
    timestamp: Any
    event_type: str
    datasource_id: str
    datasource_name: str
    user_id: str
    user_mail: str
    result: str
    elapsed_time: float
    error: Optional[str]
    request_id: str
    import_id: Optional[str]
    job_id: Optional[str]
    rows: Optional[int]
    rows_quarantine: Optional[int]
    blocks_ids: List[str]
    Options__Names: List[str]
    Options__Values: List[str]
    operation_id: str
    read_rows: int
    read_bytes: int
    written_rows: int
    written_bytes: int
    written_rows_quarantine: int
    written_bytes_quarantine: int
    pipe_id: str
    pipe_name: str
    release: str  # filled when going through DatasourceOpsTracker
    resource_tags: List[str]
    cpu_time: float = 0.0

    @classmethod
    def get_columns(cls) -> List[str]:
        return [field.name.replace("__", ".") for field in fields(cls)]

    @classmethod
    def get_csv_columns(cls) -> List[Dict[str, str]]:
        return [{"name": column} for column in cls.get_columns()]

    def values(self) -> List[str]:
        return [getattr(self, field.name) for field in fields(self)]

    def update_with_blocks(self, blocks: List[Dict[str, Any]]) -> None:
        for block in blocks:
            if "process_return" in block and block["process_return"] is not None:
                db_stats = block["process_return"][0].get("db_stats")
                for db_stat in db_stats:
                    self.update_with_db_summary(db_stat["summary"])
                quarantine_db_stats = block["process_return"][0].get("quarantine_db_stats")
                for quarantine_db_stat in quarantine_db_stats:
                    self.update_with_quarantine_db_summary(quarantine_db_stat["summary"])

    def update_with_db_summary(self, db_summary: Dict[str, Any]) -> None:
        self.written_rows += int(db_summary["written_rows"])
        self.written_bytes += int(db_summary["written_bytes"])

    def update_with_quarantine_db_summary(self, quarantine_db_summary: Dict[str, Any]) -> None:
        self.written_rows_quarantine += int(quarantine_db_summary["written_rows"])
        self.written_bytes_quarantine += int(quarantine_db_summary["written_bytes"])

    def update_with_materialization(self, materialization: Dict[str, Any]) -> None:
        self.written_rows -= int(materialization["sum_written_rows"])
        self.written_bytes -= int(materialization["sum_written_bytes"])

        # when a populate fails we save the append_log_entry.record created from the PopulateJob
        # that entry does not report written rows nor bytes, but the materialization might have written rows
        # for this reason we force round to 0 since these columns need to be unsigned
        self.written_rows = max(self.written_rows, 0)
        self.written_bytes = max(self.written_bytes, 0)

    def update_with_quarantine_materialization(self, quarantine_materialization: Dict[str, Any]) -> None:
        self.written_rows_quarantine -= int(quarantine_materialization["sum_written_rows"])
        self.written_bytes_quarantine -= int(quarantine_materialization["sum_written_bytes"])

    def update_with_main_workspace(self) -> None:
        workspace = Workspace.get_by_id(self.user_id)
        if workspace:
            # update with main if it is a release
            self.user_id = workspace.main_id
            self.release = workspace.release_semver()


@dataclass
class DatasourceOpsLogEntry:
    eta: datetime
    record: DatasourceOpsLogRecord
    workspace: Optional[Workspace]
    query_ids: List[str]
    query_ids_quarantine: List[str]
    cluster: Optional[str] = None
    # If the query never reached the landing (i.e. the insert to the Gatherer failed) then we can skip some steps like
    # retrieving materialization logs
    landing_reached: bool = True
    view_name: Optional[str] = None
    triggered_views: Optional[Dict[str, List[str]]] = None
    triggered_views_attempts: int = 0
    materialization_logs_attempts: int = 0

    def __lt__(self, other: "DatasourceOpsLogEntry") -> int:
        if other is None:
            return False
        return self.eta < other.eta

    @classmethod
    def create_from_blocks(
        cls,
        record: DatasourceOpsLogRecord,
        workspace: Optional[Workspace],
        blocks: List[Dict[str, Any]],
    ) -> "DatasourceOpsLogEntry":
        query_ids: List[str] = []
        query_ids_quarantine: List[str] = []
        if blocks is not None:
            for block in blocks:
                process_return = block.get("process_return", None)
                if process_return is None:
                    continue
                db_stats = process_return[0].get("db_stats")
                for db_stat in db_stats:
                    query_ids.append(db_stat["query_id"])
                quarantine_db_stats = process_return[0].get("quarantine_db_stats")
                for quarantine_db_stat in quarantine_db_stats:
                    query_ids_quarantine.append(quarantine_db_stat["query_id"])
        return DatasourceOpsLogEntry(
            eta=record.timestamp + timedelta(seconds=record.elapsed_time),
            record=record,
            workspace=workspace,
            query_ids=query_ids,
            query_ids_quarantine=query_ids_quarantine,
        )


class DatasourceOpsTrackerRegistry:
    _lock = threading.Lock()
    _tracker: Optional["DatasourceOpsTracker"] = None

    DEFAULT_DELAY = 10.0

    @classmethod
    def create(
        cls,
        delay: float = DEFAULT_DELAY,
        sleep_time: Optional[float] = None,
        monitoring_context: Optional[str] = None,
    ) -> "DatasourceOpsTracker":
        if cls._tracker:
            return cls._tracker
        with cls._lock:
            if not cls._tracker:
                logging.info("Starting DatasourceOpsTracker")
                if threading.main_thread() != threading.current_thread():
                    logging.error(
                        f"Starting DatasourceOpsTracker from thread={threading.current_thread()}. This is a bug.\n"
                        f"Was DatasourceOpsTrackerRegistry.create() called after stop()?\n"
                        f"PID: {os.getpid()}\n"
                        f"Stack: \n {traceback.format_stack()}"
                    )
                cls._tracker = DatasourceOpsTracker(delay, sleep_time, monitoring_context)
                if delay > 0.0:
                    cls._tracker.start()
            return cls._tracker

    @classmethod
    def get(cls):
        if cls._tracker:
            return cls._tracker
        logging.error(f"Trying to get DatasourceOpsTracker not created before: Stack {traceback.format_stack()}")

    @classmethod
    def stop(cls, timeout: Optional[float] = None) -> None:
        logging.info("Stopping DatasourceOpsTracker")
        with cls._lock:
            if cls._tracker:
                cls._tracker.shutdown(timeout)
                cls._tracker = None

    @classmethod
    def flush(cls, timeout: Optional[float] = None) -> None:
        with cls._lock:
            if cls._tracker:
                cls._tracker.flush(timeout)


MaterializationResponse = Dict[str, Any]


class MaterializationsOpsTracker:
    def __init__(self, append_log_entry: DatasourceOpsLogEntry) -> None:
        self.append_log_entry = append_log_entry

    def generate_materializations_ops_log_records(
        self, materializations: List[MaterializationResponse], quarantine: bool = False
    ) -> List[DatasourceOpsLogRecord]:
        materializations_ops_log_records: List[DatasourceOpsLogRecord] = []
        candidate_workspaces: List[Workspace] = (
            [self.append_log_entry.workspace] if self.append_log_entry.workspace else []
        )

        for mat in materializations:
            # update append log entry
            if quarantine:
                self.append_log_entry.record.update_with_quarantine_materialization(mat)
            else:
                self.append_log_entry.record.update_with_materialization(mat)

            # get metadata to create materializations records
            mat_workspace: Optional[Workspace] = None
            database_name = mat["view_name"].split(".")[0]

            if "__populate_" in database_name:
                database_name = database_name.split("__populate_")[0]

            for ws in candidate_workspaces:
                if ws and ws.database == database_name:
                    mat_workspace = ws
                    break

            if mat_workspace is None:
                try:
                    mat_workspace = Workspace.get_by_database(database_name)
                    candidate_workspaces.append(mat_workspace)
                except WorkspaceDoesNotExist:
                    pass

            if mat_workspace is None:
                logging.exception(
                    f"MaterializationsOpsTracker error: Workspace not found for materialization {str(mat)}"
                )
                continue

            pipe_node_id = self.append_log_entry.view_name or mat["view_name"].split(".")[1]
            target_id = mat["view_target"].split(".")[1]
            pipe_metadata_workspace, pipe = mat_workspace.find_pipe_in_releases_metadata_by_pipe_node_id(pipe_node_id)
            # In case the pipe is inside a release, the ds_ops_log is expected to be created using the workspace_metadata from that release.
            # If the pipe is not found, let's at least search for the datasource data from the main workspace (mat_workspace)
            workspace_to_look_for_ds = pipe_metadata_workspace or mat_workspace
            (
                metadata_workspace,
                target_ds,
            ) = workspace_to_look_for_ds.find_datasource_in_releases_metadata_by_datasource_id(target_id)
            if metadata_workspace and target_ds:
                resource_tags = [
                    tag.name for tag in metadata_workspace.get_tags_by_resource(target_ds.id, target_ds.name)
                ]
                materialization_record = DatasourceOpsLogRecord(
                    timestamp=mat["min_event_time"],
                    event_type=self.append_log_entry.record.event_type,
                    datasource_id=target_ds.id,
                    datasource_name=target_ds.name,
                    user_id=metadata_workspace.id,
                    user_mail="",
                    result="ok" if not mat.get("exception") else "error",
                    elapsed_time=mat["sum_view_duration_ms"] / 1000,
                    error=mat.get("exception", ""),
                    request_id="",
                    import_id=None,
                    job_id=None,
                    rows=mat["sum_written_rows"],
                    rows_quarantine=0,
                    blocks_ids=[],
                    Options__Names=[],
                    Options__Values=[],
                    read_rows=mat["sum_read_rows"],
                    read_bytes=mat["sum_read_bytes"],
                    written_rows=mat["sum_written_rows"],
                    written_bytes=mat["sum_written_bytes"],
                    written_rows_quarantine=0,
                    written_bytes_quarantine=0,
                    operation_id=self.append_log_entry.record.operation_id,
                    pipe_id=pipe.id if pipe else f"removed_pipe_with_mv_in_node_id_{pipe_node_id}",
                    pipe_name=pipe.name if pipe else f"removed_pipe_with_mv_in_node_id_{pipe_node_id}",
                    release="",  # filled in update_with_main_workspace
                    resource_tags=resource_tags,
                )

                materialization_record.update_with_main_workspace()
                materializations_ops_log_records.append(materialization_record)
            else:
                pipe_id = pipe.id if pipe else None
                ds_id = target_ds.id if target_ds else None
                error_message = f"MaterializationsOpsTracker: Resources not found for materialization. Pipe: '{pipe_id}', Data Source: '{ds_id}'. Materialization log: {str(mat)}"
                # TODO: not supporting shared datasources from other clusters
                if "distributed" in target_id or "distributed" in pipe_node_id:
                    logging.warning(error_message)
                else:
                    logging.exception(error_message)

        return materializations_ops_log_records

    def filter_entry_materializations(
        self,
        all_materializations: List[MaterializationResponse],
        quarantine: bool = False,
    ) -> List[MaterializationResponse]:
        materializations_aggregator: Dict[str, MaterializationResponse] = {}
        if not quarantine:
            query_id_attr = "query_ids"
        else:
            query_id_attr = "query_ids_quarantine"

        for materialization in all_materializations:
            # filter related to query_ids
            if materialization["initial_query_id"] in getattr(self.append_log_entry, query_id_attr):
                # aggregate by view
                view_name: str = materialization["view_name"]
                if view_name in materializations_aggregator:
                    agg_view: MaterializationResponse = materializations_aggregator[view_name]

                    agg_view["sum_read_rows"] += materialization["sum_read_rows"]
                    agg_view["sum_read_bytes"] += materialization["sum_read_bytes"]
                    agg_view["sum_written_rows"] += materialization["sum_written_rows"]
                    agg_view["sum_written_bytes"] += materialization["sum_written_bytes"]
                    agg_view["sum_view_duration_ms"] += materialization["sum_view_duration_ms"]
                    agg_view["min_event_time"] = min(agg_view["min_event_time"], materialization["min_event_time"])
                    agg_view["exception"] = (
                        materialization["exception"] if materialization["exception"] else agg_view["exception"]
                    )
                else:
                    materializations_aggregator.update({view_name: materialization})

        return list(materializations_aggregator.values())


MAX_TRIGGERED_VIEWS_ATTEMPTS = 10
MAX_MATERIALIZATION_LOGS_ATTEMPTS = 10


ClusterName = str
QueryID = str


class LogEntryReturnedToQueue(Exception):
    pass


class DatasourceOpsTracker:
    def __init__(
        self,
        delay: float,
        sleep_time: Optional[float] = None,
        monitoring_context: Optional[str] = None,
    ) -> None:
        self._queue: PriorityQueue[Tuple[datetime, DatasourceOpsLogEntry]] = PriorityQueue()
        self._lock = threading.Lock()
        self._thread: Optional[threading.Thread] = None
        self._exit_event = threading.Event()
        self._delay = delay
        self._public_ws: Optional[Workspace] = None
        self._client: Optional[HTTPClient] = None
        self._sleep_time = sleep_time if sleep_time else DATASOURCES_OPS_LOG_TRACKER_SLEEP_TIME
        self._monitoring_context = monitoring_context if monitoring_context else "tinybird"

    @property
    def public_ws(self) -> Workspace:
        if not self._public_ws:
            self._public_ws = public.get_public_user()
        return public.get_public_user()

    @property
    def client(self) -> HTTPClient:
        if not self._client:
            self._client = HTTPClient(self.public_ws.database_server, self.public_ws.database)
        return self._client

    @property
    def ds_ops_logs(self) -> Optional[Datasource]:
        return self.public_ws.get_datasource("datasources_ops_log")

    @property
    def ds_materializations_logs(self) -> Optional[Datasource]:
        return self.public_ws.get_datasource("distributed_materializations_log")

    @property
    def is_alive(self) -> bool:
        if not self._thread:
            return False
        return self._thread.is_alive()

    def start(self) -> None:
        with self._lock:
            if not self.is_alive:
                self._thread = threading.Thread(target=self._target, name="tracker.DatasourceOpsTracker")
                self._thread.start()

    def shutdown(self, timeout: Optional[float] = None) -> None:
        with self._lock:
            if self._thread:
                if timeout is None:
                    timeout = 1.0
                self._wait_for_flush(self._delay + timeout)
                self._exit_event.set()
                self._thread = None

    def _timed_queue_join(self, timeout: float) -> bool:
        deadline = time() + timeout
        queue = self._queue

        queue.all_tasks_done.acquire()

        try:
            while queue.unfinished_tasks:
                remaining = deadline - time()
                if remaining <= 0:
                    return False
                queue.all_tasks_done.wait(timeout=remaining)
            return True
        finally:
            queue.all_tasks_done.release()

    def _wait_for_flush(self, timeout: float) -> None:
        if self.is_alive and timeout > 0.0 and not self._timed_queue_join(timeout):
            extra_params = {"pending": self._queue.qsize() + 1, "dropped_logs": self._queue.queue}
            logging.error("DatasourceOpsTracker flush timeout, dropped pending logs", extra=extra_params)

    def flush(self, timeout: Optional[float] = None) -> None:
        # Useful for testing purposes
        with self._lock:
            if self._thread:
                if timeout is None:
                    timeout = self._delay + 1
                self._wait_for_flush(timeout)

    def __del__(self) -> None:
        with self._lock:
            if self._thread:
                self._wait_for_flush(self._delay + 1)

    def submit(self, log_entry: DatasourceOpsLogEntry, extra_delay: bool = False) -> None:
        if extra_delay:
            log_entry.eta = log_entry.eta + timedelta(seconds=1)
        self._queue.put_nowait((log_entry.eta, log_entry))

    @classmethod
    def _must_override_rows(cls, record: DatasourceOpsLogRecord) -> bool:
        """Determines if the rows field must be overridden with written_rows.

        >>> class DatasourceOpsLogRecordMock():
        ...    def __init__(self, event_type, rows):
        ...        self.event_type = event_type
        ...        self.rows = rows
        >>> record = DatasourceOpsLogRecordMock("append", 10)
        >>> DatasourceOpsTracker._must_override_rows(record)
        True
        >>> record = DatasourceOpsLogRecordMock("append-hfi", 10)
        >>> DatasourceOpsTracker._must_override_rows(record)
        True
        >>> record = DatasourceOpsLogRecordMock("whatever", None)
        >>> DatasourceOpsTracker._must_override_rows(record)
        True
        >>> record = DatasourceOpsLogRecordMock("whatever", 10)
        >>> DatasourceOpsTracker._must_override_rows(record)
        False
        """
        return record.event_type in ("append", "append-hfi") or record.rows is None

    def _pre_insert_record_update(self, entry: DatasourceOpsLogEntry) -> DatasourceOpsLogRecord:
        # LFI app hook to track rows & rows_quarantine is racy
        # Use values calculated from clickhouse
        #
        # rows is None by default in case the number of rows cannot be retrieved
        # from the table for whatever reason (in my case, because the table did not exist).
        # In those cases, we also need to fix it using the information that is provided by ClickHouse.
        record = entry.record
        if DatasourceOpsTracker._must_override_rows(record):
            record.rows = record.written_rows
            record.rows_quarantine = record.written_rows_quarantine
        record.update_with_main_workspace()
        return record

    def _report_consumer(self, num_consumed: int, timings: Dict[str, float]) -> None:
        try:
            statsd_client.incr(
                f"{self._monitoring_context}.{statsd_client.region_machine}.tracker_ops_logs.processed",
                num_consumed,
            )
            statsd_client.gauge(
                f"{self._monitoring_context}.{statsd_client.region_machine}.tracker_ops_logs.waiting",
                self._queue.qsize(),
            )
            statsd_client.timing(
                f"{self._monitoring_context}.{statsd_client.region_machine}.tracker_ops_logs.consumer_loop_lag",
                timings.get("iteration", 0.0),
            )
            if "processing" in timings:
                statsd_client.timing(
                    f"{self._monitoring_context}.{statsd_client.region_machine}.tracker_ops_logs.consumer_processing",
                    timings["processing"],
                )
            if "inserting" in timings:
                statsd_client.timing(
                    f"{self._monitoring_context}.{statsd_client.region_machine}.tracker_ops_logs.consumer_inserting",
                    timings["inserting"],
                )
        except Exception as exc:
            logging.exception(f"Error reporting stats for datasources_ops_log tracker: {exc}")

    @staticmethod
    def _group_log_entries_by_cluster(
        log_entries: List[DatasourceOpsLogEntry],
    ) -> Dict[ClusterName, List[DatasourceOpsLogEntry]]:
        entries_by_cluster: Dict[ClusterName, List[DatasourceOpsLogEntry]] = defaultdict(list)

        for entry in log_entries:
            if entry.workspace is None or entry.workspace.cluster is None:
                logging.warning(f"Skipping LogEntry due to missing workspace data: {entry}")
                continue

            cluster = entry.cluster or entry.workspace.cluster
            entries_by_cluster[cluster].append(entry)

        return entries_by_cluster

    @staticmethod
    def _batch_query_ids(cluster, query_ids: List[str]) -> List[List[str]]:
        """
        Requests with too many query_ids must be divided into multiple requests with a smaller number of ids
        We found that queries with ~5000 query_ids hit the `max_query_size` limit
        """
        max_length = 3000

        if len(query_ids) > max_length:
            logging.warning(f"Found more than 3000 query_ids for cluster {cluster} when processing log entries")

            # Divide query_ids in chunks of max_length elements (the last chunk might have less)
            chunks = batched(iter(query_ids), max_length)
            return [list(chunked_query_ids) for chunked_query_ids in chunks]

        return [query_ids]

    def _get_materialization_logs(
        self,
        cluster: ClusterName,
        initial_query_ids: List[QueryID],
        queries_include_any_populates: bool = False,
    ) -> List[MaterializationResponse]:
        initial_query_ids_in = "','".join(initial_query_ids)
        # TODO(eclbg): use timestamp of entries instead of relying on predefined intervals
        interval = "8 hour" if queries_include_any_populates else "60 minute"
        query = f"""
            SELECT
                min(event_time) as min_event_time,
                sum(read_rows) as sum_read_rows,
                sum(read_bytes) as sum_read_bytes,
                sum(written_rows) as sum_written_rows,
                sum(written_bytes) as sum_written_bytes,
                sum(view_duration_ms) as sum_view_duration_ms,
                initial_query_id,
                view_name,
                view_target,
                maxIf(exception, exception != '') as exception
            FROM clusterAllReplicas('{cluster}', system.query_views_log)
            WHERE initial_query_id IN ('{initial_query_ids_in}')
            AND view_type = 2
            AND status > 1
            AND event_date >= yesterday()
            AND event_time > now() - interval {interval}
            GROUP BY initial_query_id, view_name, view_target, exception_code
            FORMAT JSON
            """
        _, r = self.client.query_sync(query, skip_unavailable_shards=1, max_execution_time=30)
        return orjson.loads(r)["data"]

    @staticmethod
    def _classify_entries_by_completeness(
        cluster_entries: List[DatasourceOpsLogEntry],
    ) -> Tuple[List[DatasourceOpsLogEntry], List[DatasourceOpsLogEntry]]:
        """
        Classify entries that have all the additional data (detected by triggered_views being set) and those that
        need to be searched in query_log for completing them.
        - Entries without any query_id or that didn't reach the landing won't be in query_log so they are complete
        - Entries that come from QueryLogTracker or were re-enqueued at the mats step are also complete
        """
        complete_entries: List[DatasourceOpsLogEntry] = []
        incomplete_entries: List[DatasourceOpsLogEntry] = []

        for log_entry in cluster_entries:
            entry_query_ids = log_entry.query_ids + log_entry.query_ids_quarantine

            if not log_entry.landing_reached or not entry_query_ids:
                log_entry.triggered_views = {}

            if log_entry.triggered_views is not None:
                complete_entries.append(log_entry)
                continue

            log_entry.triggered_views_attempts += 1
            incomplete_entries.append(log_entry)

        return complete_entries, incomplete_entries

    def _complete_entries_or_resubmit(
        self, cluster: str, incomplete_entries: List[DatasourceOpsLogEntry]
    ) -> List[DatasourceOpsLogEntry]:
        """
        Complete entries with extended data from query_log. Entries with query_ids missing in query_log will be
        re-enqueued for a later retry
        """
        if not incomplete_entries:
            return []

        complete_entries: List[DatasourceOpsLogEntry] = []
        query_ids_to_search: List[str] = []

        for log_entry in incomplete_entries:
            query_ids_to_search.extend(log_entry.query_ids + log_entry.query_ids_quarantine)

        extended_data_by_query_id = {}
        batches = self._batch_query_ids(cluster, query_ids_to_search)
        for query_ids_batch in batches:
            batch_result = ch_get_ops_log_extended_data_by_query_id(self.client, cluster, query_ids_batch)
            extended_data_by_query_id.update(batch_result)

        for log_entry in incomplete_entries:
            all_entry_query_ids = log_entry.query_ids + log_entry.query_ids_quarantine
            missing_query_ids = [id for id in all_entry_query_ids if id not in extended_data_by_query_id.keys()]

            if not missing_query_ids:
                log_entry.triggered_views = {}
                for query_id in all_entry_query_ids:
                    log_entry.triggered_views[query_id] = extended_data_by_query_id[query_id]["views"]
                    log_entry.record.cpu_time += extended_data_by_query_id[query_id]["cpu_time"]

                complete_entries.append(log_entry)
            else:
                # Some (or all) query_ids couldn't be found in query_log, resubmitting for a later retry
                if log_entry.triggered_views_attempts < MAX_TRIGGERED_VIEWS_ATTEMPTS:
                    logging.warning(
                        f"query_ids not found in query_log in cluster {cluster}. Returning log_entry to queue. "
                        f"Attempt {log_entry.triggered_views_attempts} of {MAX_TRIGGERED_VIEWS_ATTEMPTS}"
                    )
                    self.submit(log_entry, extra_delay=True)
                else:
                    if log_entry.record.error:
                        report = logging.warning
                        complete_entries.append(log_entry)
                    else:
                        report = logging.error

                    extra = {
                        "query_ids": all_entry_query_ids,
                        "datasource_id": log_entry.record.datasource_id,
                        "workspace_id": log_entry.workspace.id if log_entry.workspace else "",
                    }
                    cluster = log_entry.workspace.cluster if log_entry.workspace and log_entry.workspace.cluster else ""
                    report(
                        f"Max attempts reached waiting for query_id log in cluster {cluster}. "
                        f"Dropping entry. Error: {log_entry.record.error}",
                        extra=extra,
                    )

        return complete_entries

    @staticmethod
    def _get_query_ids_with_triggered_views(entries: List[DatasourceOpsLogEntry]) -> List[str]:
        query_ids_with_triggered_views: List[str] = []

        for entry in entries:
            assert entry.triggered_views is not None
            for query_id, views in entry.triggered_views.items():
                if len(views) > 0:
                    query_ids_with_triggered_views.append(query_id)

        return query_ids_with_triggered_views

    def _generate_mat_records(
        self,
        mats_tracker: MaterializationsOpsTracker,
        cluster_mats: List[MaterializationResponse],
        log_entry: DatasourceOpsLogEntry,
        quarantine: bool,
    ) -> List[DatasourceOpsLogRecord]:
        def _filter_triggered_views(triggered_views: Dict[str, List[str]], query_ids: List[str]) -> set[str]:
            filtered_views: List[str] = []
            for query_id, views in triggered_views.items():
                if query_id in query_ids:
                    filtered_views += views

            return set(filtered_views)

        query_ids = log_entry.query_ids_quarantine if quarantine else log_entry.query_ids
        assert log_entry.triggered_views is not None
        entry_triggered_views = _filter_triggered_views(log_entry.triggered_views, query_ids)

        if not entry_triggered_views:
            return []

        materializations = mats_tracker.filter_entry_materializations(cluster_mats, quarantine)

        if len(entry_triggered_views) == len(materializations):
            try:
                materialization_records = mats_tracker.generate_materializations_ops_log_records(
                    materializations, quarantine
                )
                statsd_client.incr(
                    f"{self._monitoring_context}.{statsd_client.region}.tracker_ops_logs.processed_mvs",
                    len(materialization_records),
                )

                return materialization_records
            except Exception as exc:
                logging.exception(f"Error generating materialization logs: {exc}")
        else:
            log_entry.materialization_logs_attempts += 1

            if log_entry.materialization_logs_attempts < MAX_MATERIALIZATION_LOGS_ATTEMPTS:
                logging.warning(
                    "Some expected materialization logs have not been found in query_views_log. Returning "
                    f"log_entry to queue. Attempt {log_entry.materialization_logs_attempts} of "
                    f"{MAX_MATERIALIZATION_LOGS_ATTEMPTS}"
                )
                self.submit(log_entry, extra_delay=True)
                raise LogEntryReturnedToQueue
            else:
                if log_entry.record.error:
                    # if there's already an error in the record, we don't escalate logging level since the main issue is already logged
                    report = logging.warning
                else:
                    # if there's no error logged, we escalate logging level as there's no explanation for the missing materialization logs
                    report = logging.error

                extra = {
                    "datasource_id": log_entry.record.datasource_id,
                    "workspace_id": log_entry.workspace.id if log_entry.workspace else "",
                    "materialization_attempts": log_entry.materialization_logs_attempts,
                }
                cluster = log_entry.workspace.cluster if log_entry.workspace and log_entry.workspace.cluster else ""
                report(
                    f"Max attempts reached waiting for materialization logs in cluster {cluster}. "
                    f"Continuing with incomplete info. Error: {log_entry.record.error}",
                    extra=extra,
                )

        return []

    def _remove_and_hydrate_populate_record(
        self, mat_records: List[DatasourceOpsLogRecord], entry: DatasourceOpsLogEntry
    ) -> Tuple[List[DatasourceOpsLogRecord], DatasourceOpsLogEntry]:
        """
        When a populate job is executed, internally we create a Null datasource and a MV that will populate the target datasource.
        Therefore all the information (read_rows, read_bytes, written_rows, written_bytes) from the insert to the Null datasource is
        reported in the matview.
        This function removes the record from the matview and the initial entry is hydrated with that information.
        """
        duplicated_record = next(
            (
                x
                for x in mat_records
                if x.event_type == entry.record.event_type and x.datasource_id == entry.record.datasource_id
            ),
            None,
        )

        if duplicated_record:
            logging.info(f"Duplicated record found for {entry.record.datasource_id} and status {entry.record.result}.")
            entry.record.resource_tags = entry.record.resource_tags or duplicated_record.resource_tags
            entry.record.cpu_time = max(entry.record.cpu_time, duplicated_record.cpu_time)
            entry.record.read_rows = max(entry.record.read_rows, duplicated_record.read_rows)
            entry.record.read_bytes = max(entry.record.read_bytes, duplicated_record.read_bytes)
            entry.record.written_rows = max(entry.record.written_rows, duplicated_record.written_rows)
            entry.record.written_bytes = max(entry.record.written_bytes, duplicated_record.written_bytes)
            entry.record.written_rows_quarantine = max(
                entry.record.written_rows_quarantine,
                duplicated_record.written_rows_quarantine,
            )
            entry.record.written_bytes_quarantine = max(
                entry.record.written_bytes_quarantine,
                duplicated_record.written_bytes_quarantine,
            )
            entry.record.rows = entry.record.rows or duplicated_record.rows
            entry.record.rows_quarantine = entry.record.rows_quarantine or duplicated_record.rows_quarantine
            entry.record.elapsed_time = max(entry.record.elapsed_time, duplicated_record.elapsed_time)
            mat_records.remove(duplicated_record)
        # TODO: Remove this condition when we have verify everything works as expected
        else:
            logging.warning(
                f"Not found duplicated record for {entry.record.datasource_id} and status {entry.record.result}"
            )

        return mat_records, entry

    def _generate_log_records(self, log_entries: List[DatasourceOpsLogEntry]) -> List[DatasourceOpsLogRecord]:
        records: List[DatasourceOpsLogRecord] = []

        entries_by_cluster = self._group_log_entries_by_cluster(log_entries)

        for cluster, cluster_entries in entries_by_cluster.items():
            # 1. Get entries with complete extended data (triggered_views and cpu_time). Incomplete ones are re-enqueued
            complete_entries, incomplete_entries = self._classify_entries_by_completeness(cluster_entries)
            complete_entries += self._complete_entries_or_resubmit(cluster, incomplete_entries)

            logging.info(f"Found {len(complete_entries)} complete entries from {len(cluster_entries)} cluster entries")

            # 2. Get materialization logs for entries that have some triggered_views
            query_ids = self._get_query_ids_with_triggered_views(complete_entries)

            cluster_mats: List[MaterializationResponse] = []
            if query_ids:
                try:
                    populates_in_cluster = any(entry.view_name is not None for entry in complete_entries)
                    batches = self._batch_query_ids(cluster, query_ids)
                    for query_ids_batch in batches:
                        cluster_mats += self._get_materialization_logs(cluster, query_ids_batch, populates_in_cluster)
                except Exception as e:
                    logging.error(f"Failed to get materializations for cluster {cluster}", extra={"error": e})

            for entry in complete_entries:
                mats_tracker = MaterializationsOpsTracker(entry)

                # 3. Generate materialization log records for entries with triggered views.
                # If materialization logs can't be found yet, entry is re-enqueued

                mat_records = []
                if entry.triggered_views:
                    try:
                        mat_records = self._generate_mat_records(mats_tracker, cluster_mats, entry, quarantine=False)
                        mat_records += self._generate_mat_records(mats_tracker, cluster_mats, entry, quarantine=True)
                    except LogEntryReturnedToQueue:
                        continue

                # 4. Generate landing record
                # TODO: Use a constant for the event type
                is_populate_record = entry.record.event_type == "populateview"
                if is_populate_record:
                    mat_records, entry = self._remove_and_hydrate_populate_record(mat_records, entry)

                records += mat_records
                records.append(self._pre_insert_record_update(entry))

        return records

    def _insert_log_records(self, records: List[DatasourceOpsLogRecord]) -> None:
        try:
            ds_ops_logs = self.ds_ops_logs
            if ds_ops_logs:
                rows = [record.values() for record in records]
                columns = f"({', '.join(DatasourceOpsLogRecord.get_columns())})"

                @retry_sync((CHException, requests.exceptions.ConnectionError), tries=2, delay=0.5)
                def insert_chunk(query: str, chunk: Any) -> None:
                    self.client.insert_chunk(query, chunk, log_as_error=False)

                insert_chunk(
                    f"insert into `{ds_ops_logs.id}` {columns} FORMAT CSV",
                    csv_from_python_object(rows),
                )
            else:
                logging.error("datasources_ops_log Data Source not found in the public user")
        except Exception as exc:
            logging.exception(f"Datasources ops log insertion error: {exc}")

    def _target(self) -> None:
        while not self._exit_event.is_set():
            records_to_insert: List[DatasourceOpsLogRecord] = []
            entries_to_process: List[DatasourceOpsLogEntry] = []
            num_tasks_done = 0
            timings: Dict = {}
            start_iteration = monotonic()

            while not self._queue.empty():
                _, log_entry = self._queue.get()
                try:
                    if datetime.now(timezone.utc) >= log_entry.eta + timedelta(seconds=self._delay):
                        entries_to_process.append(log_entry)
                    else:
                        self.submit(log_entry)
                        break
                except Exception as exc:
                    logging.exception(f"Failed getting log_entry from queue {log_entry}: {exc}")
                finally:
                    num_tasks_done += 1

            try:
                if entries_to_process:
                    start_processing = monotonic()
                    records_to_insert += self._generate_log_records(entries_to_process)
                    timings["processing"] = monotonic() - start_processing

                if records_to_insert:
                    start_inserting = monotonic()
                    self._insert_log_records(records_to_insert)
                    timings["inserting"] = monotonic() - start_inserting
            except Exception as err:
                err_msg = f"Failed generating or inserting datasource ops log {log_entry}: {err}"
                logging.exception(err_msg)
            finally:
                # TODO(eclbg): this is incorrect, we're marking as many tasks done as tasks we had to perform,
                # regardless of the result
                # Mark tasks as done only when append_data_to_table is called
                for _ in range(num_tasks_done):
                    self._queue.task_done()

            timings["iteration"] = monotonic() - start_iteration
            self._report_consumer(len(records_to_insert), timings)

            self._exit_event.wait(self._sleep_time)


def track_datasource_ops(
    ops_log_entries: OpsLogEntries,
    request_id=None,
    import_id=None,
    job_id=None,
    source=None,
    blocks_ids=None,
    connector=None,
    service=None,
    workspace=None,
    blocks=None,
    pipe_id=None,
    pipe_name=None,
) -> None:
    blocks_ids = blocks_ids if isinstance(blocks_ids, list) else []
    blocks_ids = list(set([b for b in blocks_ids if isinstance(b, str)]))

    rows = []
    for ops_log_entry in ops_log_entries:
        if source:
            ops_log_entry.options["source"] = source
        if connector:
            ops_log_entry.options["connector"] = connector
        if service:
            ops_log_entry.options["service"] = service

        error = ops_log_entry.error
        if workspace:
            error = replace_table_id_with_datasource_id(
                workspace, error, error_datasource_id=ops_log_entry.datasource_id
            )

        if "source" in ops_log_entry.options:
            # hide internal connectors bucket
            ops_log_entry.options["source"] = try_replace_source(
                workspace, ops_log_entry.datasource_id, ops_log_entry.options.get("source", "")
            )

        resource_tags: List[str] = []
        if workspace and ops_log_entry.datasource_id:
            resource_tags = [
                tag.name
                for tag in workspace.get_tags_by_resource(ops_log_entry.datasource_id, ops_log_entry.datasource_name)
            ]

        record = DatasourceOpsLogRecord(
            timestamp=ops_log_entry.start_time,
            event_type=ops_log_entry.event_type,
            datasource_id=ops_log_entry.datasource_id,
            datasource_name=ops_log_entry.datasource_name,
            user_id=ops_log_entry.workspace_id,
            user_mail=ops_log_entry.workspace_email,
            result=ops_log_entry.result,
            elapsed_time=ops_log_entry.elapsed_time,
            error=error,
            request_id=request_id,
            import_id=import_id,
            job_id=job_id,
            rows=ops_log_entry.rows,
            rows_quarantine=ops_log_entry.rows_quarantine,
            blocks_ids=blocks_ids,
            Options__Names=list(ops_log_entry.options.keys()),
            Options__Values=list(ops_log_entry.options.values()),
            read_rows=0,
            read_bytes=0,
            written_rows=0,
            written_bytes=0,
            written_rows_quarantine=0,
            written_bytes_quarantine=0,
            operation_id=import_id,
            pipe_id=pipe_id or ops_log_entry.pipe_id or "",
            pipe_name=pipe_name or ops_log_entry.pipe_name or "",
            release="",  # fill later,
            resource_tags=resource_tags,
        )

        datasources_ops_tracker = DatasourceOpsTrackerRegistry.get()

        if record.event_type == "append" or ops_log_entry.use_tracker or ops_log_entry.update_with_blocks:
            if blocks is not None:
                record.update_with_blocks(blocks)
            else:
                logging.warning(f"Append record {record} with no blocks")

        if record.event_type == "append" or ops_log_entry.use_tracker:
            if datasources_ops_tracker and datasources_ops_tracker.is_alive:
                datasources_ops_tracker.submit(
                    DatasourceOpsLogEntry.create_from_blocks(record=record, workspace=workspace, blocks=blocks)
                )
            else:
                logging.info("DatasourceOpsTracker is not alive, log directly sent to datasources_ops_log")
                record.update_with_main_workspace()
                rows.append(record.values())
        else:
            record.update_with_main_workspace()
            rows.append(record.values())

    if rows:
        u = public.get_public_user()
        ds = u.get_datasource("datasources_ops_log")
        if not ds:
            raise Exception("datasources_ops_log Data Source not found in the public user")
        append_data_to_table(
            database_server=u.database_server,
            database=u.database,
            cluster=u.cluster,
            table_name=ds.id,
            rows=rows,
            with_quarantine=False,
            columns=DatasourceOpsLogRecord.get_csv_columns(),
        )


def track_blocks(
    request_id,
    import_id,
    job_id,
    workspace: Workspace,
    source,
    blocks,
    block_log,
    token_id,
    datasource_id,
    datasource_name,
) -> None:
    # generate the data and send to the main queue
    blocks_map = {x["block_id"]: x for x in blocks}

    rows = []
    source = try_replace_source(workspace, datasource_id, source)
    for x in block_log:
        if x["status"] == "done" and x["block_id"] in blocks_map:
            b = blocks_map[x["block_id"]]
            start_offset = b.get("start_offset", None)
            end_offset = b.get("end_offset")
            process_return = b.get("process_return")
            lines = None
            parser = None
            empty_lines = None
            quarantine_lines = None
            nbytes = None

            if process_return:
                process_return = process_return[0]
                lines = process_return.get("lines", None)
                parser = process_return.get("parser", None)
                empty_lines = process_return.get("empty_lines", None)
                quarantine_lines = process_return.get("quarantine", None)
                nbytes = process_return.get("bytes", None)

            processing_time = b.get("processing_time", None)
            processing_error = b.get("processing_error", None)

            if processing_error and workspace:
                processing_error = replace_table_id_with_datasource_id(
                    workspace, processing_error, error_datasource_id=datasource_id
                )

            extra = (
                start_offset,
                end_offset,
                lines,
                parser,
                quarantine_lines,
                empty_lines,
                nbytes,
                processing_time,
                processing_error,
            )
        else:
            extra = (None, None, None, None, None, None, None, None, None)

        rows.append(
            (  # noqa: RUF005
                x["timestamp"],
                request_id,
                import_id,
                job_id,
                source,
                token_id,
                x["block_id"],
                x["status"],
                workspace.id,
                # FIXME: Does it make sense to keep this? A workspace can have no email and some other places we just use the name.
                workspace["email"] if "email" in workspace else workspace.name,  # noqa: SIM401
                datasource_id,
                datasource_name,
            )
            + extra
        )

    u = public.get_public_user()
    t = u.get_datasource("block_log")
    if not t:
        raise Exception("datasources_ops_log Data Source not found in the public user")
    append_data_to_table(
        database_server=u.database_server,
        database=u.database,
        cluster=u.cluster,
        table_name=t.id,
        rows=rows,
        with_quarantine=False,
    )


class QueryLogTracker:
    """
    Collects the logs generated by the Gatherer
    """

    THREAD_SLEEP_IN_SECONDS: int = 4
    DEFAULT_READ_BATCH_LIMIT: int = 1000

    UA_ORIGIN_MAP: Dict[str, str] = {
        f"tb-{GATHERER_KAFKA_SOURCE_TAG}-gatherer": "kafka",
        f"tb-{GATHERER_HFI_SOURCE_TAG}-gatherer": "hfi",
        f"tb-{GATHERER_JOB_PROCESSOR_SOURCE_TAG}-gatherer": "job_processor",
        f"tb-{GATHERER_DYNAMODBSTREAMS_SOURCE_TAG}-gatherer": "dynamodb",
    }

    def __init__(
        self,
        redis_config: TBRedisConfig,
        clusters: Dict[str, str],
        start_timestamp: datetime,
        read_batch_limit: Optional[int],
    ) -> None:
        self.working_group_name = "query_log_tracker"
        self._redis_client = TBRedisClientSync(redis_config)
        self._clusters = clusters
        self._start_timestamp: float = start_timestamp.timestamp()
        self._read_batch_limit: int = (
            read_batch_limit if read_batch_limit is not None else QueryLogTracker.DEFAULT_READ_BATCH_LIMIT
        )
        self._tracker: DatasourceOpsTracker = DatasourceOpsTrackerRegistry.create()
        self._exit_flag: asyncio.Event = asyncio.Event()
        self._cached_http_clients: Dict[str, HTTPClient] = {}
        self._task: Optional[asyncio.Task] = None

    async def init(self, start_process: bool = True):
        try:
            self._asyncio_loop = asyncio.get_running_loop()
            self._exit_flag = asyncio.Event()
            self._working_group = WorkingGroup(self.working_group_name, str(uuid.uuid4()))
            await self._working_group.init()
            if start_process:
                await self._track_queries_async()
                self._task = asyncio.create_task(self._loop())
        except Exception as e:
            logging.exception(f"Error initializing the query log tracker: {e}")

    async def _loop(self) -> None:
        logging.info("QueryLogTracker: starting tracing queries")
        while not self._exit_flag.is_set():
            try:
                await asyncio.wait_for(self._exit_flag.wait(), timeout=self.THREAD_SLEEP_IN_SECONDS)
            except asyncio.TimeoutError:
                await self._track_queries_async()
            except Exception as e:
                logging.exception(f"Unhandled exception {e}.\nTraceback: {traceback.format_exc()}")

    def terminate(self) -> None:
        # The asyncio.Event needs to be set from the same thread it
        # was created from. So, we schedule a coroutine to set it.
        async def set_flag_in_loop():
            self._exit_flag.set()
            await self._working_group.exit()

        logging.info("QueryLogTracker: stopping tracing queries")
        asyncio.run_coroutine_threadsafe(set_flag_in_loop(), loop=self._asyncio_loop)

    async def join(self) -> None:
        if self._task:
            await self._task

    def _redis_ch_hosts_timestamp_key(self, cluster: str) -> str:
        return f"{self.working_group_name}:{cluster}:ch_hosts"

    def _get_ch_hosts_last_timestamps(self, cluster: str) -> Dict[str, float]:
        get_all_response = self._redis_client.hgetall(self._redis_ch_hosts_timestamp_key(cluster))
        return {key.decode(): float(value.decode()) for (key, value) in get_all_response.items()}

    def _update_start_timestamp_for_host(self, cluster: str, ch_host: str, start_timestamp: float) -> None:
        self._redis_client.hset(self._redis_ch_hosts_timestamp_key(cluster), ch_host, start_timestamp)

    def datetime_now(self) -> datetime:
        return datetime.now()

    def get_start_timestamp(self, cluster: str) -> Tuple[float, Dict[str, float]]:
        """
        Returns the initial timestamps
        """
        cluster_last_timestamp = (self.datetime_now() - timedelta(minutes=10)).timestamp()
        if cluster_last_timestamp < self._start_timestamp:
            cluster_last_timestamp = self._start_timestamp
        ch_hosts_last_timestamp = self._get_ch_hosts_last_timestamps(cluster)

        return cluster_last_timestamp, ch_hosts_last_timestamp

    def _build_query(self, cluster_last_timestamp: float, hosts_last_timestamp: Dict[str, float], cluster: str) -> str:
        time_filter_using_cluster_last_timestamp = f"event_time >= toDateTime(fromUnixTimestamp(toUInt32({cluster_last_timestamp}))) AND event_time_microseconds::double > {cluster_last_timestamp}"

        limited_ch_host_timestamp = (datetime.now() - timedelta(hours=4)).timestamp()

        def limit_ch_host_timestamp(ch_host_timestamp: float):
            return ch_host_timestamp if ch_host_timestamp > limited_ch_host_timestamp else limited_ch_host_timestamp

        if hosts_last_timestamp:
            ch_hosts_filters = [
                (
                    f"(hostname() = '{ch_host}' "
                    f"and event_time >= toDateTime(fromUnixTimestamp(toUInt32({limit_ch_host_timestamp(ch_host_timestamp)})))"
                    f"and event_time_microseconds::double > {limit_ch_host_timestamp(ch_host_timestamp)})"
                )
                for ch_host, ch_host_timestamp in hosts_last_timestamp.items()
            ]
            ch_host_names = [f"'{ch_host}'" for ch_host in hosts_last_timestamp]
            ch_host_names_with_commas = ", ".join(ch_host_names)
            excluded_hosts_list = (
                f"(hostname() not IN ({ch_host_names_with_commas}) and {time_filter_using_cluster_last_timestamp})"
                if hosts_last_timestamp
                else None
            )
            if excluded_hosts_list:
                ch_hosts_filters.append(excluded_hosts_list)
            hosts_filtering_query = " OR ".join(ch_hosts_filters)

        else:
            hosts_filtering_query = time_filter_using_cluster_last_timestamp

        # We need to use fetch the finish datetime as later we will use this datetime to look for the MV
        # The DatasourceOpsLogTracker will wait 10 seconds after the eta field
        return f"""
            SELECT
                query_id,
                event_time_microseconds::double as timestamp_microseconds,
                query_duration_ms / 1000 as elapsed_time_seconds,
                written_rows,
                written_bytes,
                query,
                views,
                http_user_agent,
                exception_code,
                exception,
                hostname() as ch_host,
                ProfileEvents['OSCPUVirtualTimeMicroseconds']/1e6 as cpu_time
            FROM
                clusterAllReplicas('{cluster}', system.query_log)
            WHERE
                http_user_agent in ('{"','".join(QueryLogTracker.UA_ORIGIN_MAP.keys())}')
                AND event_date >= yesterday()
                AND ({hosts_filtering_query})
                AND is_initial_query == 1
                AND type > 1
                AND query_kind == 'Insert'
                AND NOT has(databases, 'public')
            ORDER BY
                event_time_microseconds ASC
            {f"LIMIT {self._read_batch_limit}" if self._read_batch_limit > 0 else ""}
            FORMAT JSON
        """

    async def get_queries(
        self, cluster: str, varnish_host: str, cluster_last_timestamp: float, hosts_last_timestamp: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        try:
            client: Optional[HTTPClient] = self._cached_http_clients.get(varnish_host, None)
            if client is None:
                client = HTTPClient(varnish_host)
                self._cached_http_clients[varnish_host] = client
            assert isinstance(client, HTTPClient)

            # Check if instance is up and reachable
            up = await client.ping()
            if not up:
                logging.warning(
                    f"Can't track queries from the Gatherer: Ping down for varnish_host {varnish_host} in cluster {cluster}"
                )
                statsd_client.incr(
                    f"{self._tracker._monitoring_context}.{statsd_client.region_machine}.tracker_ops_logs.ping_down"
                )
                return []

            query = self._build_query(cluster_last_timestamp, hosts_last_timestamp, cluster)

            async def query_data(**kwargs: Any) -> List[Dict[str, Any]]:
                _, result = await client.query(query, max_threads=1, max_execution_time=30, **kwargs)
                data: List[Dict[str, Any]] = json.loads(result).get("data", [])
                return data

            retries = 2
            extra_params: Dict[str, Any] = {}
            while retries > 0:
                try:
                    data = await query_data(**extra_params)
                    return data
                except CHException as e:
                    retries -= 1
                    if retries == 0:
                        raise e
                    logging.warning(e)
                    extra_params["skip_unavailable_shards"] = 1
                    await asyncio.sleep(3)

        except Exception as e:
            logging.exception(e)
        return []

    async def _track_queries_async(self) -> None:
        """Fetches the query_log based on known user-agents and feeds the
        ops tracker with all needed info.

        It tries to not discard any single log entry for *ANY* reason.
        That's why we assign default values in case any field is missing.
        """

        # Only 1 instance will run this
        score_index = self._working_group.score_index("main")
        if score_index != 0:
            logging.debug("Not running QueryLogTracker as it's not main process")
            return

        if self._exit_flag.is_set():
            return

        logging.debug(f"QueryLogTracker listening to {self._clusters}")
        for cluster, varnish_host in self._clusters.items():
            if self._exit_flag.is_set():
                break

            if any(x in cluster for x in ("gatherer", "internal", "metrics")):
                continue

            cluster_last_timestamp, hosts_last_timestamp = self.get_start_timestamp(cluster)

            logging.info(
                f"Processing {cluster} on {varnish_host} since {cluster_last_timestamp}/{datetime.fromtimestamp(cluster_last_timestamp).strftime('%d/%m/%Y, %H:%M:%S')} and for hosts: {hosts_last_timestamp}"
            )

            query_logs: List[Dict[str, Any]] = await self.get_queries(
                cluster, varnish_host, cluster_last_timestamp, hosts_last_timestamp
            )

            statsd_client.incr(
                f"{self._tracker._monitoring_context}.{statsd_client.region_machine}.tracker_ops_logs.gatherer_query_logs_to_process",
                len(query_logs),
            )

            if len(query_logs) == 0:
                continue

            ch_hosts_to_be_updated = {}

            for query_log in query_logs:
                query_id: str = query_log.get("query_id", "")
                gatherer_query = query_log.get("query", "")
                exception_code = int(query_log.get("exception_code", "0"))
                exception = query_log.get("exception", "")

                # As sql_get_used_tables does not support INSERT INTO __ SELECT * FROM __
                # We need to transform the insert statement to a select
                insert_query = gatherer_query.split("SELECT")[0]
                transformed_query = insert_query.replace("INSERT INTO", "SELECT * FROM")
                clean_query = re.sub(r"\(.*?\)", "", transformed_query)
                used_tables = sql_get_used_tables(clean_query, raising=False, table_functions=False)
                if len(used_tables) != 1:
                    logging.warning(
                        f"Unexpected used_tables result for query_id {query_id} in {cluster}: {used_tables}"
                    )
                    continue

                database = used_tables[0][0]
                table = used_tables[0][1]
                workspace_id: str = ""
                workspace: Optional[Workspace] = None
                if database:
                    try:
                        workspace = Workspace.get_by_database(database)
                        workspace_id = workspace.id
                    except WorkspaceDoesNotExist:
                        logging.warning(f"Non existant Workspace: {query_log}")
                        workspace_id = database  # Fallbacks to database

                is_quarantine: bool = False
                if table.endswith("_quarantine"):
                    table = table[:-11]
                    is_quarantine = True

                datasource_id: str = table
                datasource_name: str = ""
                if workspace:
                    workspace, datasource = workspace.find_datasource_in_releases_metadata_by_datasource_id(table)
                    if not datasource:
                        logging.warning(f"Non existant Datasource: {query_log}")
                    else:
                        datasource_name = datasource.name

                last_timestamp = float(query_log.get("timestamp_microseconds", time() * 1000000))
                elapsed_time: float = query_log.get("elapsed_time_seconds", 0)
                written_rows: int = query_log.get("written_rows", 0)
                written_bytes: int = query_log.get("written_bytes", 0)
                cpu_time: float = query_log.get("cpu_time", 0)
                triggered_views: Dict[str, List[str]] = {query_id: query_log.get("views", [])}
                ch_host: str = query_log.get("ch_host", "unknown")

                ua: str = query_log.get("http_user_agent", "")
                mapped_source: Optional[str] = QueryLogTracker.UA_ORIGIN_MAP.get(ua, None)
                event_type: str = f"append-{mapped_source}" if mapped_source else "append"

                resource_tags: List[str] = []

                if workspace:
                    resource_tags = [tag.name for tag in workspace.get_tags_by_resource(datasource_id, datasource_name)]

                record = DatasourceOpsLogRecord(
                    timestamp=datetime.fromtimestamp(last_timestamp, tz=timezone.utc),
                    event_type=event_type,
                    datasource_id=datasource_id,
                    datasource_name=datasource_name,
                    user_id=workspace_id,
                    user_mail=workspace.name if workspace else "",
                    result="ok" if exception_code == 0 else "error",
                    elapsed_time=elapsed_time,
                    error=None if exception_code == 0 else exception,
                    request_id="",
                    import_id=None,
                    job_id=None,
                    rows=(0 if is_quarantine else written_rows),
                    rows_quarantine=(written_rows if is_quarantine else 0),
                    blocks_ids=[],
                    Options__Names=[],
                    Options__Values=[],
                    operation_id=query_id,
                    read_rows=0,
                    read_bytes=0,
                    written_rows=0 if is_quarantine else written_rows,
                    written_bytes=0 if is_quarantine else written_bytes,
                    written_rows_quarantine=written_rows if is_quarantine else 0,
                    written_bytes_quarantine=written_bytes if is_quarantine else 0,
                    pipe_id="",
                    pipe_name="",
                    release="",
                    cpu_time=cpu_time,
                    resource_tags=resource_tags,
                )

                entry = DatasourceOpsLogEntry(
                    eta=record.timestamp,
                    record=record,
                    workspace=workspace,
                    query_ids=[query_id] if not is_quarantine else [],
                    query_ids_quarantine=[] if not is_quarantine else [query_id],
                    triggered_views=triggered_views,
                )

                self._tracker.submit(entry)
                ch_hosts_to_be_updated[ch_host] = last_timestamp

            for ch_host, last_timestamp in ch_hosts_to_be_updated.items():
                self._update_start_timestamp_for_host(cluster, ch_host, last_timestamp)

            logging.info(f"'{self.working_group_name}' loop processed {len(query_logs)} log entries from {cluster}")


def try_replace_source(workspace: Workspace, datasource_id: str, source: str) -> str:
    if any(x for x in CDK_SOURCES if x in source):
        ds: Optional[Datasource] = None
        if workspace:
            ds = workspace.get_datasource(datasource_id)
        if ds:
            return ds.datasource_type
        else:
            return "connector"
    return source
