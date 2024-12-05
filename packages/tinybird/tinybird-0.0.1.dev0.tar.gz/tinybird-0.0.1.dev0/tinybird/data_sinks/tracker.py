import logging
import time
from collections import deque
from datetime import datetime, timezone
from enum import Enum
from itertools import groupby
from typing import Any, List, Optional, Tuple, ValuesView
from urllib.parse import urljoin

import orjson
import requests
from pydantic import BaseModel, field_serializer

from tinybird.ch import HTTPClient, UserAgents
from tinybird.ch_utils.exceptions import CHException
from tinybird.internal_thread import InternalThread
from tinybird.user import public
from tinybird_shared.metrics.statsd_client import statsd_client

SINKS_OPS_LOG_DATASOURCE_NAME: str = "sinks_ops_log"
SINKS_OPS_LOG_TRACKER_TIMEOUT_SECONDS: int = 2
SINKS_OPS_LOG_TIMER_SECONDS: float = 30.0
SINKS_OPS_LOG_MAX_RECORDS: int = 1000
SINKS_TRACKER_SHUTDOWN_WAIT_TIMEOUT_SECONDS = 30.0


def get_sinks_append_token() -> str:
    """
    This is used in tests to get the token to append data to the sinks_ops_log datasource.
    """
    internal_workspace = public.get_public_user()
    access_token = internal_workspace.get_token(f"{SINKS_OPS_LOG_DATASOURCE_NAME} (Data Source append)")
    if not access_token:
        logging.warning(f"No {SINKS_OPS_LOG_DATASOURCE_NAME} token found for the 'Internal' workspace")
        access_token = internal_workspace.get_token("admin token")
        if not access_token:
            logging.warning("No admin token found for the 'Internal' workspace")
            return ""
    return access_token.token


def get_internal_admin_token() -> str:
    """
    This is used for local dev since sinks_ops_log token is not available.
    Also for tests to query the contents of sinks_ops_log datasource.
    """
    internal_workspace = public.get_public_user()
    access_token = internal_workspace.get_token("admin token")
    if not access_token:
        raise Exception(f"No {SINKS_OPS_LOG_DATASOURCE_NAME} token found for the 'Internal' workspace")
    return access_token.token


class SinksTrackerWrongAppendMethodUsed(Exception):
    pass


class SinksOpsLogResults(Enum):
    OK: str = "ok"
    ERROR: str = "error"
    CANCELLED: str = "cancelled"


def _null_values_to_empty_strings(mapping: dict[str, Any]) -> dict[str, Any]:
    return {k: v if v is not None else "" for k, v in mapping.items()}


class SinksQueryLogEntry(BaseModel):
    query_id: str
    read_rows: int
    read_bytes: int
    written_rows: int
    written_bytes: int
    cpu_time: float


class SinksOpsLogBaseRecord(BaseModel):
    workspace_id: str
    workspace_name: str
    timestamp: datetime
    service: str
    pipe_id: str
    pipe_name: str
    token_name: str
    result: SinksOpsLogResults
    elapsed_time: float = 0.0
    read_rows: int = 0
    written_rows: int = 0
    read_bytes: int = 0
    written_bytes: int = 0
    error: Optional[str] = None
    job_id: Optional[str] = None
    output: List[str] = []
    parameters: dict[str, Any] = {}
    options: dict[str, Any] = {}
    cpu_time: float = 0.0
    resource_tags: List[str] = []

    @field_serializer("parameters")
    def serialize_parameters_with_empty_strings(self, parameters: dict[str, Any]):
        return _null_values_to_empty_strings(parameters)

    @field_serializer("options")
    def serialize_options_with_empty_strings(self, options: dict[str, Any]):
        return _null_values_to_empty_strings(options)


class SinksAPILogRecord(SinksOpsLogBaseRecord):
    pass


class SinksExecutionLogRecord(SinksOpsLogBaseRecord):
    workspace_database: str
    workspace_cluster: str
    query_id: str


class SinksOpsLogAppendParams(BaseModel):
    name: str
    token: str


class SinksOpsLogTracker(InternalThread):
    def __init__(self):
        """
        This class is responsible for tracking Sinks operations and sending it to Tinybird via the Events API.
        We will use a thread to send the data in batches, so we don't block the main thread.
        - We will use a timer to send the data every SINKS_OPS_LOG_TIMER_SECONDS seconds
        - If the number of records is greater than SINKS_OPS_LOG_MAX_RECORDS, we will reduce the timer by half
        """
        self._max_records: int = SINKS_OPS_LOG_MAX_RECORDS
        super().__init__(name="sinks_tracker", exit_queue_timeout=SINKS_OPS_LOG_TIMER_SECONDS)
        self._cached_http_clients: dict[str, HTTPClient] = {}
        self.records_from_executions: dict[str, SinksExecutionLogRecord] = {}
        self.records_from_api_errors: deque[SinksAPILogRecord] = deque()
        self.append_url: str = ""
        self.params: SinksOpsLogAppendParams = SinksOpsLogAppendParams(name=SINKS_OPS_LOG_DATASOURCE_NAME, token="")

    def init(self, tb_api_host: str, token: str) -> None:
        self.append_url = urljoin(tb_api_host, "/v0/events")
        self.params = SinksOpsLogAppendParams(name=SINKS_OPS_LOG_DATASOURCE_NAME, token=token)
        logging.info(f"sinks_tracker - Initialized with host '{tb_api_host}' and append token")

    def is_enabled(self) -> bool:
        """
        >>> sinks_tracker = SinksOpsLogTracker()
        >>> sinks_tracker.is_enabled()
        False
        >>> sinks_tracker.init("https://api.tinybird.co", "test")
        >>> sinks_tracker.is_enabled()
        True
        """
        return self.append_url != "" and self.params.token != ""

    def action(self) -> Tuple[bool, Optional[str]]:
        # Using a Shallow Copy here to avoid
        # unintended updates to the records
        execution_records = dict(self.records_from_executions)
        api_errors = self._get_current_items_from_deque(self.records_from_api_errors)
        return self.flush(execution_records, api_errors)

    def flush(
        self, execution_records: dict[str, SinksExecutionLogRecord], api_errors_records: list[SinksAPILogRecord]
    ) -> Tuple[bool, Optional[str]]:
        if not execution_records and not api_errors_records:
            logging.info("sinks_tracker - No records to send")
            return True, None

        # -- Process to flush logs
        #  1. Peform query to query_log to gather Sinks query_log entries
        #  2. Fill current SinksOpsLog record with written and transferred data
        #  3. Ingest records that have read and written bytes and logs ready

        query_log_entries = self.retrieve_query_log_entries_from_clusters(execution_records)
        records_to_flush = self.populate_sinksopslog_records_with_query_log(execution_records, query_log_entries)

        logging.info(
            f"sinks_tracker - {len(execution_records)} pending records, {len(records_to_flush)} found in the query_log."
        )
        if not records_to_flush and not api_errors_records:
            return True, None

        # Send updated records to SinksOpsLog
        logging.info(f"sinks_tracker - Sending {len(records_to_flush)} records")
        try:
            r: requests.Response = requests.post(
                url=self.append_url,
                params=self.params.model_dump(),
                data=self._serialize_records([*records_to_flush, *api_errors_records]),
                timeout=SINKS_OPS_LOG_TRACKER_TIMEOUT_SECONDS,
            )
        except requests.exceptions.RequestException as e:
            message = str(e)
            logging.exception(f"Error sending {len(records_to_flush)} records. Text: {message}")
            return False, message

        if r.status_code not in (200, 202):
            # TODO: here, we should have a fallback to ingesting directly via ClickHouse
            message = r.text
            self.records_from_api_errors.extend(api_errors_records)
            logging.exception(f"Error sending {len(records_to_flush)} records. Status:{r.status_code}, Text: {message}")
            return False, message

        self.remove_flushed_records(records_to_flush)
        return True, None

    def shutdown(self) -> None:
        logging.warning("sinks_tracker - Starting shutdown...")
        logging.warning("sinks_tracker - Terminating sinks tracker thread...")
        self.terminate()
        self.join()
        logging.warning("sinks_tracker - Sinks tracker thread terminated")
        # Once we've reached this point the thread is dead so we don't need to worry about concurrency
        logging.warning(
            "sinks_tracker - %d execution records & %d api error records pending flush...",
            len(self.records_from_executions),
            len(self.records_from_api_errors),
        )
        wait_start = time.perf_counter()
        while len(self.records_from_executions) > 0 or len(self.records_from_api_errors) > 0:
            time.sleep(1)  # Sleep here instead at the end as we'll most likely need to wait for the query_log
            execution_records = dict(self.records_from_executions)
            api_errors = self._get_current_items_from_deque(self.records_from_api_errors)
            self.flush(execution_records, api_errors)
            if (time.perf_counter() - wait_start) >= SINKS_TRACKER_SHUTDOWN_WAIT_TIMEOUT_SECONDS:
                self._print_unflushed_records(self.records_from_executions.values())
                raise TimeoutError("Sink tracker shutdown timed out")
        logging.warning("sinks_tracker - shutdown finished.")

    def _print_unflushed_records(self, records: ValuesView[SinksExecutionLogRecord]) -> None:
        for record in records:
            logging.warning(f"sinks_tracker - Unflushed record - Job ID: {record.job_id}")

    def append_execution_log(self, record: SinksExecutionLogRecord) -> None:
        logging.info(f"sinks_tracker - Appending record - Job ID: {record.job_id}")
        self._check_for_errors_in_internal_sinks(record)
        self.records_from_executions[record.query_id] = record

    def append_api_log(self, record: SinksAPILogRecord) -> None:
        logging.info("sinks_tracker - Appending API Error Log record")
        self.records_from_api_errors.append(record)

    def get_query_log_entries(
        self, cluster: str, host: str, query_ids: list[str], start_timestamp: datetime
    ) -> list[SinksQueryLogEntry]:
        client: Optional[HTTPClient] = self._cached_http_clients.get(host, None)
        if client is None:
            client = HTTPClient(host)
            self._cached_http_clients[host] = client

        query = self._render_query_log_sql(cluster, start_timestamp, query_ids)

        try:
            _, result = client.query_sync(query, skip_unavailable_shards=1)
            data = orjson.loads(result).get("data", [])
        except (CHException, requests.exceptions.RequestException, orjson.JSONDecodeError) as e:
            logging.exception(e)
            return []

        return [SinksQueryLogEntry(**entry_data) for entry_data in data]

    def retrieve_query_log_entries_from_clusters(
        self, execution_records: dict[str, SinksExecutionLogRecord]
    ) -> list[SinksQueryLogEntry]:
        query_log_entries: list[SinksQueryLogEntry] = []
        records_by_cluster = self._group_records_by_cluster(execution_records.values())

        for (database_server, cluster), records in records_by_cluster.items():
            oldest_record = min(records, key=get_timestamp_from_record)
            query_ids = [record.query_id for record in records if record.query_id]
            query_records = self.get_query_log_entries(cluster, database_server, query_ids, oldest_record.timestamp)
            query_log_entries.extend(query_records)

        return query_log_entries

    def populate_sinksopslog_records_with_query_log(
        self, execution_records: dict[str, SinksExecutionLogRecord], query_log_entries: list[SinksQueryLogEntry]
    ) -> list[SinksExecutionLogRecord]:
        populated_records: list[SinksExecutionLogRecord] = []
        for log_entry in query_log_entries:
            query_id = log_entry.query_id
            if sink_record := execution_records.get(query_id):
                populated_records.append(sink_record.model_copy(update=log_entry.model_dump()))
        return populated_records

    def remove_flushed_records(self, flushed_records: list[SinksExecutionLogRecord]) -> None:
        for flushed_record in flushed_records:
            self.records_from_executions.pop(flushed_record.query_id)

        self.set_exit_queue_timeout()
        logging.info(
            f"Flushing Records · {len(flushed_records)} records flushed. {len(self.records_from_executions)} still remaining."
        )

    def set_exit_queue_timeout(self) -> None:
        """
        This method will set the exit_queue_timeout based on the number of records.
        - If the number of records is greater than SINKS_OPS_LOG_MAX_RECORDS, we will reduce the timer by half.
        - If the number of records is less, and the timeout is less than half of SINKS_OPS_LOG_TIMER_SECONDS, we will increase the
        timer by double.
        - If the number of records is less, and the timeout is greater than half of SINKS_OPS_LOG_TIMER_SECONDS, we will set the
        timer to SINKS_OPS_LOG_TIMER_SECONDS.
        >>> sinks_tracker = SinksOpsLogTracker()
        >>> sinks_tracker.records_from_executions = {str(i): str(i) for i in range(1, 750)}
        >>> sinks_tracker.records_from_api_errors = [str(i) for i in range(1, 751)]
        >>> sinks_tracker.set_exit_queue_timeout()
        >>> sinks_tracker.exit_queue_timeout
        15.0
        >>> sinks_tracker.set_exit_queue_timeout()
        >>> sinks_tracker.exit_queue_timeout
        7.5
        >>> sinks_tracker.set_exit_queue_timeout()
        >>> sinks_tracker.set_exit_queue_timeout()
        >>> sinks_tracker.set_exit_queue_timeout()
        >>> sinks_tracker.set_exit_queue_timeout()
        >>> sinks_tracker.exit_queue_timeout
        1.0
        >>> sinks_tracker.records_from_executions = {}
        >>> sinks_tracker.records_from_api_errors = [str(i) for i in range(1, 501)]
        >>> sinks_tracker.set_exit_queue_timeout()
        >>> sinks_tracker.set_exit_queue_timeout()
        >>> sinks_tracker.set_exit_queue_timeout()
        >>> sinks_tracker.set_exit_queue_timeout()
        >>> sinks_tracker.exit_queue_timeout
        16.0
        >>> sinks_tracker.set_exit_queue_timeout()
        >>> sinks_tracker.exit_queue_timeout
        30.0
        >>> sinks_tracker.set_exit_queue_timeout()
        >>> sinks_tracker.exit_queue_timeout
        30.0
        """
        remaining_elements = len(self.records_from_executions) + len(self.records_from_api_errors)
        if remaining_elements >= self._max_records:
            self.exit_queue_timeout = float(max(self.exit_queue_timeout / 2, 1.0))
        elif self.exit_queue_timeout < (SINKS_OPS_LOG_TIMER_SECONDS / 2):
            self.exit_queue_timeout = self.exit_queue_timeout * 2
        else:
            self.exit_queue_timeout = SINKS_OPS_LOG_TIMER_SECONDS

    def _render_query_log_sql(self, cluster: str, timestamp: datetime, query_ids: list[str]):
        timestamp_str = timestamp.replace(tzinfo=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        return f"""
            WITH JSONExtractString(log_comment, 'job_service') = 'kafka' AS is_kafka
            SELECT
                query_id,
                read_rows,
                read_bytes,
                written_rows,
                is_kafka ? written_bytes : ProfileEvents['WriteBufferFromS3Bytes'] as written_bytes,
                toFloat32(ProfileEvents['OSCPUVirtualTimeMicroseconds']/1e6) as cpu_time
            FROM
                clusterAllReplicas('{cluster}', system.query_log)
            WHERE
                http_user_agent in ('{UserAgents.SINKS.value}')
                AND event_date >= toDate('{timestamp_str}')
                AND event_time >= toDateTime('{timestamp_str}')
                AND is_initial_query == 1
                AND type > 1
                AND query_id in ('{"', '".join(query_ids)}')
            LIMIT {len(query_ids)}
            FORMAT JSON
        """

    def _serialize_records(self, records: list[SinksOpsLogBaseRecord]) -> bytes:
        return "\n".join(
            record.model_dump_json(exclude={"query_id", "workspace_database", "workspace_cluster"})
            for record in records
        ).encode(errors="replace")

    def _group_records_by_cluster(
        self,
        records: ValuesView[SinksExecutionLogRecord],
    ) -> dict[Tuple[str, str], list[SinksExecutionLogRecord]]:
        sorted_records = sorted(records, key=group_by_databaseserver_and_cluster_fn)
        return {key: list(group) for key, group in groupby(sorted_records, key=group_by_databaseserver_and_cluster_fn)}

    def _get_current_items_from_deque(self, api_errors_deque: deque) -> list[SinksAPILogRecord]:
        return [api_errors_deque.popleft() for _ in range(0, len(api_errors_deque))]

    def _check_for_errors_in_internal_sinks(self, record: SinksExecutionLogRecord):
        if record.error and record.workspace_id == public.INTERNAL_WORKSPACE_ID:
            logging.warning(f"Error executing Internal sink {record.pipe_name}. Error: {record.error}")
            statsd_client.incr(f"tinybird.internal_sink.{statsd_client.region}.{record.pipe_name}.failure")


def group_by_databaseserver_and_cluster_fn(record: SinksExecutionLogRecord) -> Tuple[str, str]:
    return record.workspace_database, record.workspace_cluster


def get_timestamp_from_record(record: SinksExecutionLogRecord) -> datetime:
    return record.timestamp


sinks_tracker: SinksOpsLogTracker = SinksOpsLogTracker()
