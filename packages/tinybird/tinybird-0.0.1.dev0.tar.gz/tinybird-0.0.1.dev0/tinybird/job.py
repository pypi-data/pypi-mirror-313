"""
each time a user request to process a csv a job is created.
This file contains the logic to create the check job state
"""

import asyncio
import json
import logging
import queue
import random
import re
import threading
import time
import traceback
import typing
import uuid
import zlib
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Set, Tuple, Union, cast

import aiohttp
import orjson
import redis
import ulid
from tornado.httputil import HTTPHeaders

import tinybird.views.shared.utils as SharedUtils
from tinybird import tracker
from tinybird.blocks import blocks_json
from tinybird.ch import (
    CHAnalyzeError,
    CHParquetMetadata,
    CHSummary,
    HTTPClient,
    ch_delete_condition_sync,
    ch_describe_table_from_url,
    ch_escape_string,
    ch_get_parquet_metadata_from_url,
    ch_table_schema,
    create_quarantine_table_from_landing_sync,
    rows_affected_by_delete_sync,
)
from tinybird.ch_utils.describe_table import DescribeTable, TableColumn
from tinybird.ch_utils.exceptions import CHException
from tinybird.connector_settings import DataConnectors
from tinybird.csv_importer import import_csv
from tinybird.data_connector import DataSourceNotConnected
from tinybird.dataflow import DataFlowStep
from tinybird.datasource import Datasource
from tinybird.default_secrets import running_in_testing_environment
from tinybird.feature_flags import FeatureFlagsWorkspaceService, FeatureFlagWorkspaces
from tinybird.hook_resources import HookException, hook_log_json
from tinybird.integrations.s3 import sign_s3_url
from tinybird.limits import GB, FileSizeException, Limit, get_url_file_size_checker
from tinybird.model import (
    RedisModel,
    retry_job_transaction_in_case_of_error_sync,
    retry_transaction_in_case_of_concurrent_edition_error_sync,
)
from tinybird.ndjson import ExtendedJSONDeserialization, extend_json_deserialization, get_path
from tinybird.providers.aws.exceptions import AWSClientException, InvalidS3URL
from tinybird.raw_events.definitions.base import JobStatus as JobStatusForLog
from tinybird.raw_events.definitions.delete_log import DeleteJobLog, DeleteJobMetadata
from tinybird.raw_events.definitions.import_log import ImportJobLog, ImportJobMetadata, ParquetImportJobMetadata
from tinybird.raw_events.raw_events_batcher import EventType, RawEvent, raw_events_batcher
from tinybird.redis_queue import RedisQueue
from tinybird.shutdown import ShutdownApplicationStatus
from tinybird.syncasync import async_to_sync, sync_to_async
from tinybird.timing import Timer
from tinybird.user import User as Workspace
from tinybird.user import Users as Workspaces
from tinybird.views.aiohttp_shared_session import get_shared_session
from tinybird.views.api_errors.utils import build_error_summary, get_errors, replace_table_id_with_datasource_id
from tinybird.views.block_tracker import NDJSONBlockLogTracker
from tinybird.views.gzip_utils import is_gzip_file
from tinybird.views.ndjson_importer import (
    NDJSON_CHUNK_SIZE,
    NDJSON_CHUNK_SIZE_COMPRESSED,
    NDJSONIngester,
    PushError,
    safe_sql_column,
)
from tinybird_shared.clickhouse.errors import CHErrors, is_user_error
from tinybird_shared.metrics.statsd_client import statsd_client
from tinybird_shared.redis_client.redis_client import TBRedisClientSync, TBRedisConfig
from tinybird_shared.retry.retry import retry_ondemand_async

if typing.TYPE_CHECKING:
    from tinybird.hook import Hook


HOOKS_ERR_DEFAULT = "We weren't able to identify the source problem automatically, reach us at support@tinybird.co"
HOOKS_ERR_MEMORY_LIMIT = "Query reached memory limit for queries, probably caused by a query that generates a materialized view. See https://docs.tinybird.co/guides/performance.html#memory-limit-reached-when-running-a-query"

JOB_TTL_IN_HOURS = 48
MAX_UINT32 = 4294967295

SUPPORTED_CH_ERRORS_CODES = [CHErrors.NO_SUCH_COLUMN_IN_TABLE]


def translate_ch_error_to_user_on_post_hook_error(ch_err_exception) -> Union[str, int, None]:
    """
    translates clickhouse error messages to something a user can understand
    >>> translate_ch_error_to_user_on_post_hook_error(CHException('Code: 241, e.displayText() = DB::Exception: Memory limit (for query) exceeded: would use 4.66 GiB (attempt to allocate chunk of 4503240 bytes), maximum: 4.66 GiB: While executing SinkToOutputStream')) == HOOKS_ERR_MEMORY_LIMIT
    True
    """
    if ch_err_exception.code == CHErrors.MEMORY_LIMIT_EXCEEDED or "memory limit" in str(ch_err_exception):
        return HOOKS_ERR_MEMORY_LIMIT
    if ch_err_exception.code in SUPPORTED_CH_ERRORS_CODES:
        return ch_err_exception
    return None


def get_database_server_and_queue_type(key: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Get the database server and the queue type from a Redis queue.
    Examples of keys in production:

    queue:jobs:10.156.0.3:query_queue:items_processed
    queue:jobs:10.156.0.3:import_queue:items_processed
    queue:jobs:http://audiense:6081:import_queue
    queue:jobs:http://audiense:6081:import_queue:items_processed
    queue:jobs:http://audiense:6081:import_queue:wip_items
    queue:jobs:http://thn:6081:import_queue
    queue:jobs:http://velaris:6081:import_queue

    >>> get_database_server_and_queue_type('queue:jobs:database_server:import_queue')
    ('database_server', 'import')
    >>> get_database_server_and_queue_type('queue:jobs:database_server:import_queue:wip_items')
    ('database_server', 'import')
    >>> get_database_server_and_queue_type('queue:jobs:database_server:import_parquet_queue')
    ('database_server', 'import_parquet')
    >>> get_database_server_and_queue_type('queue:jobs:database_server:import_parquet_queue:wip_items')
    ('database_server', 'import_parquet')
    >>> get_database_server_and_queue_type('queue:jobs:database_server:query_queue')
    ('database_server', 'query')
    >>> get_database_server_and_queue_type('queue:jobs:database_server:query_queue:items_processed')
    ('database_server', 'query')
    >>> get_database_server_and_queue_type('queue:jobs:database_server:export_queue')
    ('database_server', 'export')
    >>> get_database_server_and_queue_type('queue:jobs:database_server:export_queue:items_processed')
    ('database_server', 'export')
    >>> get_database_server_and_queue_type('queue:jobs:database_server:sink_queue')
    ('database_server', 'sink')
    >>> get_database_server_and_queue_type('queue:jobs:database_server:sink_queue:items_processed')
    ('database_server', 'sink')
    >>> get_database_server_and_queue_type('queue:jobs:database_server:branching_queue')
    ('database_server', 'branching')
    >>> get_database_server_and_queue_type('queue:jobs:database_server:branching_queue:items_processed')
    ('database_server', 'branching')
    >>> get_database_server_and_queue_type('queue:jobs:database_server:dynamodb_sync_queue')
    ('database_server', 'dynamodb_sync')
    >>> get_database_server_and_queue_type('queue:jobs:database_server:dynamodb_sync_queue:items_processed')
    ('database_server', 'dynamodb_sync')
    >>> get_database_server_and_queue_type('queue:jobs:http://thn:6081:import_queue')
    ('http://thn:6081', 'import')
    >>> get_database_server_and_queue_type('queue:jobs:http://thn:6081:query_queue:wip_items')
    ('http://thn:6081', 'query')
    >>> get_database_server_and_queue_type('mec')
    (None, None)
    """
    res = re.search(
        rf"{RedisQueue.NAMESPACE}:{JobThreadPoolExecutor.REDIS_NAMESPACE}:(.*):({JobExecutor.IMPORT}|{JobExecutor.IMPORT_PARQUET}|{JobExecutor.QUERY}|{JobExecutor.POPULATE}|{JobExecutor.COPY}|{JobExecutor.SINK}|{JobExecutor.BRANCHING}|{JobExecutor.DYNAMODB_SYNC}){JobThreadPoolExecutor.REDIS_QUEUE_SUFFIX}",
        key,
    )
    if res and len(res.groups()) == 2:
        return cast(Tuple[Optional[str], Optional[str]], res.groups())
    else:
        return None, None


def sanitize_database_server(database_server: str) -> str:
    """ "
    >>> sanitize_database_server('1.2.3.4')
    '1_2_3_4'
    >>> sanitize_database_server('http://1.2.3.4:8080')
    'http___1_2_3_4_8080'
    """
    return "".join([c if c.isalnum() else "_" for c in database_server])


class JobStatus:
    WAITING = "waiting"
    WORKING = "working"
    CANCELLING = "cancelling"

    DONE = "done"
    ERROR = "error"
    CANCELLED = "cancelled"


class JobKind:
    DELETE_DATA = "delete_data"
    IMPORT = "import"
    POPULATE = "populateview"
    QUERY = "query"
    COPY = "copy"
    COPY_MAIN = "copy_from_main"
    COPY_BRANCH = "copy_from_branch"
    DATA_BRANCH = "data_branch"
    DEPLOY = "deploy_branch"
    REGRESSION = "regression_tests"
    SINK = "sink"
    SINK_BRANCH = "sink_from_branch"
    DYNAMODB_SYNC = "dynamodb_sync"


JOB_PARQUET_TYPES = ("ndjson", "parquet")


JOB_PROGRESS_STATUSES = [JobStatus.WAITING, JobStatus.WORKING, JobStatus.CANCELLING]


class WipJobsQueueRegistry:
    _root_wip_jobs_queue: Optional[queue.Queue] = None

    @classmethod
    def get_or_create(cls) -> queue.Queue:
        if not cls._root_wip_jobs_queue:
            cls._root_wip_jobs_queue = queue.Queue()
        return cls._root_wip_jobs_queue

    @classmethod
    def stop(cls) -> None:
        if cls._root_wip_jobs_queue:
            cls._root_wip_jobs_queue.join()


class DataFlowJobReporter:
    def __init__(self, job_id: Optional[str]) -> None:
        if job_id is None or Job.get_by_id(job_id) is None:
            self._job_present = False
            return

        self._job_id = job_id
        self._job_present = True
        self._processed_data: dict = {"read_rows": 0, "read_bytes": 0, "written_rows": 0, "written_bytes": 0}

        with Job.transaction(self._job_id) as job:
            if hasattr(job, "dependent_datasources"):
                job.dependent_datasources = {"progress_percentage": 0, "steps": [], "skipped_steps": []}
        self._total_step_materialized_views = 0

    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def add_steps(self, steps_to_execute: List[DataFlowStep]) -> None:
        if not self._job_present:
            return

        steps = [self.get_map_step_to_json(step, JobStatus.WAITING) for step in steps_to_execute]
        self._total_step_materialized_views = sum([len(execution["pipes"]) for execution in steps])

        with Job.transaction(self._job_id) as job:
            if hasattr(job, "dependent_datasources"):
                job.dependent_datasources["steps"] = steps

    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def add_skipped_steps(self, skipped_steps: List[DataFlowStep]) -> None:
        if not self._job_present:
            return

        with Job.transaction(self._job_id) as job:
            if hasattr(job, "dependent_datasources"):
                as_dicts = self.get_map_skipped_steps_to_json(skipped_steps)
                job.dependent_datasources["skipped_steps"] = as_dicts

    @staticmethod
    def get_map_step_to_json(step_to_map: DataFlowStep, status: Optional[str] = None) -> Dict[str, Any]:
        pipes = []

        if step_to_map.step_copy:
            pipe = {
                "id": step_to_map.step_copy.pipe.id,
                "name": step_to_map.step_copy.pipe.name,
                "node": {"id": step_to_map.step_copy.node.id, "name": step_to_map.step_copy.node.name},
            }
            if status:
                pipe["status"] = status
            pipes.append(pipe)

        if step_to_map.step_materialized_views:
            for materialized_view in step_to_map.step_materialized_views:
                pipe = {
                    "id": materialized_view.pipe.id,
                    "name": materialized_view.pipe.name,
                    "node": {"id": materialized_view.node.id, "name": materialized_view.node.name},
                }
                if status:
                    pipe["status"] = status
                pipes.append(pipe)

        step = {
            "workspace": {"id": step_to_map.step_workspace.id, "name": step_to_map.step_workspace.name},
            "status": status,
            "pipes": pipes,
            "datasource": {"id": step_to_map.step_datasource.id, "name": step_to_map.step_datasource.name},
        }

        if step_to_map.step_query_id:
            step["query_id"] = step_to_map.step_query_id

        return step

    @staticmethod
    def get_map_steps_to_json(steps: List[DataFlowStep]) -> List[Dict[str, Any]]:
        return [DataFlowJobReporter.get_map_step_to_json(step) for step in steps]

    @staticmethod
    def get_map_skipped_steps_to_json(skipped_steps: List[DataFlowStep]) -> List[Dict[str, Any]]:
        return [
            {
                "workspace": {"id": step_to_map.step_workspace.id, "name": step_to_map.step_workspace.name},
                "datasource": {"id": step_to_map.step_datasource.id, "name": step_to_map.step_datasource.name},
            }
            for step_to_map in skipped_steps
        ]

    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def change_step_status(self, step_index: int, step_new_status: str) -> None:
        if not self._job_present:
            return

        with Job.transaction(self._job_id) as job:
            if hasattr(job, "dependent_datasources"):
                job.dependent_datasources["steps"][step_index]["status"] = step_new_status

    def update_process_percentage(
        self, job_info: Dict[str, Any], new_step_status: str, step_index: int, materialized_view_index: int
    ) -> float:
        if new_step_status != JobStatus.DONE:
            return job_info["progress_percentage"]

        current_position = 0
        for step_position in range(0, step_index):
            if step_position == step_index:
                current_position += materialized_view_index
            else:
                current_position += len(job_info["steps"][step_position]["pipes"])

        if self._total_step_materialized_views == 0:
            return 0
        else:
            return (current_position + 1) / self._total_step_materialized_views * 100

    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def change_step_pipe_status(self, step_index: int, materialized_view_index: int, step_new_status: str) -> None:
        if not self._job_present:
            return

        with Job.transaction(self._job_id) as job:
            if hasattr(job, "dependent_datasources"):
                job.dependent_datasources["steps"][step_index]["pipes"][materialized_view_index]["status"] = (
                    step_new_status
                )
                job.dependent_datasources["progress_percentage"] = self.update_process_percentage(
                    job.dependent_datasources, step_new_status, step_index, materialized_view_index
                )

    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def change_processed_data(self, step_index: int, processed_data: Optional[Dict[str, Any]]) -> None:
        if not self._job_present:
            return

        if not processed_data:
            return

        with Job.transaction(self._job_id) as job:
            if hasattr(job, "dependent_datasources"):
                job.dependent_datasources["steps"][step_index]["processed_data"] = processed_data
                self._processed_data = {
                    "read_rows": int(self._processed_data.get("read_rows", 0))
                    + int(processed_data.get("read_rows", 0)),
                    "read_bytes": int(self._processed_data.get("read_bytes", 0))
                    + int(processed_data.get("read_bytes", 0)),
                    "written_rows": int(self._processed_data.get("written_rows", 0))
                    + int(processed_data.get("written_rows", 0)),
                    "written_bytes": int(self._processed_data.get("written_bytes", 0))
                    + int(processed_data.get("written_bytes", 0)),
                }
            if hasattr(job, "processed_data"):
                job.processed_data.update(self._processed_data)

    def get_processed_data(self) -> Optional[Dict[str, Any]]:
        if not self._job_present:
            return None

        return self._processed_data

    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def mark_as_done(self) -> None:
        if not self._job_present:
            return

        with Job.transaction(self._job_id) as job:
            if hasattr(job, "dependent_datasources"):
                for datasource in job.dependent_datasources["steps"]:
                    datasource["status"] = JobStatus.DONE

    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def change_elapsed_time(self, step_index: int, elapsed_time: Any) -> None:
        if not self._job_present:
            return
        with Job.transaction(self._job_id) as job:
            if hasattr(job, "dependent_datasources"):
                job.dependent_datasources["steps"][step_index]["elapsed_time"] = elapsed_time


class JobLogHandler(logging.StreamHandler):
    def __init__(self, job: "Job") -> None:
        logging.StreamHandler.__init__(self)
        self.job = job

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        self.job.log(msg)


class JobNotInCancellableStatusException(Exception):
    pass


class JobAlreadyBeingCancelledException(Exception):
    pass


class JobThreadPoolExecutor:
    """
    This is a utility class built on top of ThreadPoolExecutor. It also contains the Redis queue that belongs
    to a particular database server.
    This way, it can read for new jobs in the queue only whenever there are available workers in its ThreadPoolExecutor,
    """

    REDIS_NAMESPACE = "jobs"
    REDIS_QUEUE_SUFFIX = "_queue"

    def __init__(
        self,
        database_server: str,
        redis_config: TBRedisConfig,
        workers: int,
        kind: str,
        shutdown_wait: bool = True,
    ) -> None:
        self.database_server = database_server
        self.kind = kind
        self._local_executor_wip_jobs: Set[str] = set()
        self._workers = workers
        self._redis_queue: RedisQueue = RedisQueue(
            name=f"{JobThreadPoolExecutor.REDIS_NAMESPACE}:{database_server}:{kind}{JobThreadPoolExecutor.REDIS_QUEUE_SUFFIX}",
            namespace=RedisQueue.NAMESPACE,
            redis_config=redis_config,
        )
        self._lock = threading.RLock()
        self._lock_key = f"lock_get_job_{self.kind}"
        self._redis_client = TBRedisClientSync(redis_config)
        self.shutdown_wait = shutdown_wait

        self._thread_pool_executor: Optional[ThreadPoolExecutor]
        if workers > 0:
            logging.info(
                f"Creating JobThreadPoolExecutor for {database_server} and type {kind} with {workers} workers "
                f"for queue '{self._redis_queue.waiting_queue_key}'"
            )
            self._thread_pool_executor = ThreadPoolExecutor(max_workers=workers, thread_name_prefix=f"jobs_{kind}")
        else:
            logging.info(
                f"Not creating JobThreadPoolExecutor for {database_server} and type {kind} because is set without workers "
                f"for queue '{self._redis_queue.waiting_queue_key}'"
            )
            self._thread_pool_executor = None

    def submit(self, function: Callable[["Job"], Any], job: "Job") -> Any:
        def _wrapper_function() -> Any:
            try:
                return function(job)
            except BaseException as e:
                # The ThreadPoolExecutor doesn't log the exception, so we have to do it manually
                logging.exception(f"Job {job.id} crashed: {e}")
                raise e

        if not self._thread_pool_executor:
            raise Exception(f"Job {job.id} cannot be submitted to be executed because there is no job consumer set up")
        with self._lock:
            self._local_executor_wip_jobs.add(job.id)

        logging.info(f"Submitting job {job.id} to be executed in {self._thread_pool_executor._thread_name_prefix}")
        return self._thread_pool_executor.submit(_wrapper_function)

    def get_job_mutex_lock(self) -> bool:
        ttl_ms = int(JobProcessor.NO_JOB_SLEEP_TIME_IN_SECS * 1000 * 2)
        return self._redis_client.set(self._lock_key, "acquired", px=ttl_ms, nx=True)

    def get_job_mutex_release(self) -> None:
        self._redis_client.delete(self._lock_key)

    def get_job(self) -> Optional[str]:
        if ShutdownApplicationStatus.is_application_exiting():
            logging.warning("Should not be taking new jobs as application is exiting")
            return None
        if self._thread_pool_executor and self._executors_available():
            # There's a race condition where two Job Processors might pop jobs
            # from the queue after ensuring that there's no WIP jobs. Let's use
            # a simple distributed lock pattern described by the Redis
            # documentation in https://redis.io/commands/set/ This pattern is
            # chosen over a Redlock implementation for the sake of simplicity
            acquired = self.get_job_mutex_lock()
            if not acquired:
                # Backoff to avoid different Job Processors checking at the same time
                time.sleep(JobProcessor.NO_JOB_SLEEP_TIME_IN_SECS / 2)
                return None
            try:
                wip_job_ids = self._redis_queue.get_wip()
                if len(wip_job_ids) >= self._workers:
                    return None
                job_id = self._redis_queue.pop_queue_and_add_to_wip()
                if job_id:
                    job = Job.get_by_id(job_id)
                    if job is None or not isinstance(job, Job):
                        logging.error(f"Job {job_id} cannot be retrieved from Redis. Removing it from the queue")
                        self._redis_queue.rem_wip(job_id)
                        return None
                    self._update_alive_queue()
            finally:
                self.get_job_mutex_release()
            return job_id
        else:
            return None

    def put_job(self, job_id: str) -> None:
        self._redis_queue.put_queue(job_id)
        self._update_alive_queue()

    def _update_alive_queue(self) -> None:
        now = int(time.time())
        self._redis_queue.db.zadd(JobExecutor.ALIVE_QUEUES, {self._redis_queue.waiting_queue_key: now})

    def get_pending_jobs(self) -> Tuple[List["Job"], List["Job"]]:
        tmp_queued_jobs: List[str] = self._redis_queue.get_queued()
        tmp_wip_jobs: List[str] = self._redis_queue.get_wip()

        queued_jobs = []
        wip_jobs = []

        # Filter from the queued jobs all those that are already cancelled. This
        # has the drawback that we have to deserialize them all just to know
        # their status. We can't take out the jobs from the queue as we do with
        # the WIP one until they're picked up, though.
        for job_id in tmp_queued_jobs:
            try:
                job = Job.get_by_id(job_id)
                if job and job.status in [JobStatus.WAITING, JobStatus.CANCELLING]:
                    queued_jobs.append(job)
            except Exception:
                logging.warning(f"Job {job_id} cannot be retrieved from Redis. Removing it from the pending queue")
                pass

        # Defensive programming to avoid returning job ids that either are no longer
        # WIP or that no longer exist. This should not happen under normal circumstances,
        # but may happen if the JobProcessor dies suddenly without finishing properly.
        # Since the WIP queue does not have a TTL while the jobs do, we need to have
        # some extra logic to avoid users of this API falling into the trap of trying
        # to get the status of a job that no longer exists.
        remove_wip_jobs: List[str] = []
        for job_id in tmp_wip_jobs:
            try:
                job = Job.get_by_id(job_id)
                if not job:
                    continue
                if job.status not in [JobStatus.WAITING, JobStatus.WORKING, JobStatus.CANCELLING]:
                    remove_wip_jobs.append(job_id)
                    logging.warning(
                        f"Job {job_id} status {job.status} not in waiting/working/cancelling status. Removing it from the WIP queue"
                    )
                else:
                    wip_jobs.append(job)
            except Exception:
                remove_wip_jobs.append(job_id)
                logging.warning(f"Job {job_id} cannot be retrieved from Redis. Removing it from the WIP queue")
                pass
        for job_id in remove_wip_jobs:
            self._redis_queue.rem_wip(job_id)
            tmp_wip_jobs.remove(job_id)

        return wip_jobs, queued_jobs

    def shutdown(self, wait: bool = True) -> None:
        if self._thread_pool_executor:
            # We are using wait=True, when we do a shutdown, we will wait for all the jobs to finish.
            # We will use wait=False, from the method `check_for_new_queues`, because it's previously indicating that no jobs should be there
            wip_jobs = self._redis_queue.get_wip()
            logging.info(
                f"Shutting down JobThreadPoolExecutor for {self.database_server} and type {self.kind} we have {len(wip_jobs)} jobs in progress "
                f"{'we will wait for them to finish' if wait else 'we will not wait for them to finish'}"
            )
            self._thread_pool_executor.shutdown(wait=wait)

    def job_finished(self, job_id: str) -> None:
        self._redis_queue.task_done(job_id)

        # This is the only method that is executed in one of the threads from the pool. The rest of the methods
        # are executed from the main thread. Thus, we need to ensure _wip_jobs is protected.
        with self._lock:
            if job_id in self._local_executor_wip_jobs:
                self._local_executor_wip_jobs.remove(job_id)
        self._update_alive_queue()

    def has_jobs_wip(self) -> bool:
        with self._lock:
            return len(self._local_executor_wip_jobs) > 0

    def _executors_available(self) -> bool:
        with self._lock:
            return len(self._local_executor_wip_jobs) < self._workers


class JobProcessor(threading.Thread):
    NO_JOB_SLEEP_TIME_IN_SECS = 0.5

    def __init__(self, job_executor: "JobExecutor", *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.name = "jobs_processor"
        self._exit_event = threading.Event()
        self._job_executor = job_executor

    def terminate(self) -> None:
        self._exit_event.set()

    def run(self) -> None:
        connection_failures = 0
        max_backoff = 5

        random_ms_to_avoid_retring_at_the_same_time = round(random.random(), 3)
        time_to_wait_for_each_failed_connection_attempt = 2 + random_ms_to_avoid_retring_at_the_same_time
        while not self._exit_event.is_set():
            job_id = None
            j = None
            try:
                try:
                    # Since we have a queue per type and database_server, we often need to check if there's a new queue
                    # created for a database_server. This is due to the fact that JobThreadPoolExecutors are created
                    # lazily only when submitting new jobs. So, this check is needed both when starting
                    # or when new database_server are added at runtime.
                    self._job_executor.check_for_new_queues()

                    executors = self._job_executor.get_all_executors()
                    if executors:
                        for executor in executors:
                            job_id = executor.get_job()
                            if job_id:
                                break
                        connection_failures = 0
                except redis.exceptions.ConnectionError as e:
                    connection_failures = min(max_backoff, connection_failures + 1)
                    time_to_wait = time_to_wait_for_each_failed_connection_attempt**connection_failures
                    logging.exception(
                        f"Consume jobs queue failed with Redis Connection error, waiting {time_to_wait} seconds before trying to connect again: {e}"
                    )
                    time.sleep(time_to_wait)
                if not job_id:
                    self._exit_event.wait(self.NO_JOB_SLEEP_TIME_IN_SECS)
                    continue
                j = Job.get_by_id(job_id)
                assert isinstance(j, Job)
                j.set_job_executor(self._job_executor)
                j.run()
            except Exception as e:
                if j:
                    j.mark_as_error({"error": "Job failed to finish for an unknown reason. Try again."})
                logging.exception(f"Consume jobs queue uncaught exception on job_id '{job_id}' {e}")


class JobExecutor:
    """This takes care of parallelization and ordering of job execution.

    There are many executor types that process jobs. They are independent and don't know anything about each other.
    This means that jobs will always run in parallel when they are in different executors.
    A few examples of executors include:

        - Import executors

        These executors process jobs that require preparing data before sending it to ClickHouse.

        They will handle any instance of the ImportJob, that's basically all the append and replace operations created
        via a POST /v0/datasources request with an url parameter.

        They consume resources (CPU, memory, IOPS) from the machine where they are running. The JobProcessor machine
        should have enough of those resources.

        They will parallelize jobs based on two things: (1) the database_server and (2) the import_workers.
        Workspaces in different database servers will have different executors, thus running in parallel. This is kind
        of risky if we consider the previous information about the required resources to run these jobs: if we had too
        many different database servers, we could have a lot of these jobs trying to run in parallel. Especially, if
        combined with the import_workers setting that drives the amount of total jobs per database server to run at
        the same time.
        However, we have another measure that takes care of how many resources we use in the machine processing these
        jobs: we have another buffering mechanism taking care of how many chunks of data we process at the same time in
        a job processor. You can find more details at https://gitlab.com/tinybird/analytics/-/merge_requests/1779.


        - Query executors

        These executors process jobs that are ClickHouse bound because they are about executing queries in the database.

        In general, this include the populate, delete, and the general purpose query jobs.

        They affect the performance of the workspace's database server as they put queries running on those servers.

        They will parallelize only based on the destination database server. They will only run one job at the time for
        each different database server. For instance, this helps when you have to reason about doing several populate
        operations as you can decide what to run first.

        - Export Data Sink executors

        These executors process jobs that export data to an external service like AWS S3 or GCS.

        Unless overriden, there will only be one Export Data Sink queue per database server. So only one export
        job will be run per database server, no parallel jobs within the same job executor.

    FAQ

        - What happens if I'm running a populate job and I send a replace for one of the involved DS in the populate?

            To be confirmed.

            Initial analysis:
            The replace operation at some point will "exchange table old to new, new to old" and "drop table old". With
            the populate query running and using the "old" table, I don't know if ClickHouse will lock any of those
            operations (exchange/rename, drop) or if it will be able to keep running the populate queries.
            The other major thing to consider is with the way we do the populates per partition, some queries could work
            with the "old" table data and other queries could use the "new" table data, so for sure you can expect
            inconsistent results.

    """

    _import_threadpool_executors: Dict[str, JobThreadPoolExecutor]
    _import_parquet_threadpool_executors: Dict[str, JobThreadPoolExecutor]
    _query_threadpool_executors: Dict[str, JobThreadPoolExecutor]
    _populate_threadpool_executors: Dict[str, JobThreadPoolExecutor]
    _copy_threadpool_executors: Dict[str, JobThreadPoolExecutor]
    _sink_threadpool_executors: Dict[str, JobThreadPoolExecutor]
    _branching_threadpool_executors: Dict[str, JobThreadPoolExecutor]
    _dynamodb_sync_threadpool_executors: Dict[str, JobThreadPoolExecutor]
    _consumer: bool = False
    _last_queue_keys_check: Optional[int] = None

    IMPORT = "import"
    IMPORT_PARQUET = "import_parquet"
    COPY = "export"
    QUERY = "query"
    POPULATE = "populate"
    SINK = "sink"
    BRANCHING = "branching"
    DYNAMODB_SYNC = "dynamodb_sync"
    ALIVE_QUEUES = None
    ALIVE_QUEUES_TTL_IN_SECONDS = 2 * 60 * 60  # 2h
    CHECK_NEW_QUEUES_FREQ_IN_SECONDS = 10

    def __init__(
        self,
        redis_client: TBRedisClientSync,
        redis_config: TBRedisConfig,
        consumer: bool = False,
        import_workers: int = 0,
        import_workers_per_database: Optional[Dict[str, Any]] = None,
        import_parquet_workers: int = 0,
        import_parquet_workers_per_database: Optional[Dict[str, Any]] = None,
        query_workers: int = 0,
        query_workers_per_database: Optional[Dict[str, Any]] = None,
        populate_workers: int = 0,
        populate_workers_per_database: Optional[Dict[str, Any]] = None,
        copy_workers: int = 0,
        copy_workers_per_database: Optional[Dict[str, Any]] = None,
        sink_workers: int = 0,
        sink_workers_per_database: Optional[Dict[str, Any]] = None,
        branching_workers: int = 0,
        branching_workers_per_database: Optional[Dict[str, Any]] = None,
        dynamodb_sync_workers: int = 0,
        dynamodb_sync_workers_per_database: Optional[Dict[str, Any]] = None,
        billing_provider: str = "unknown",
        billing_region: str = "unknown",
    ) -> None:
        # We need to initialize `ALIVE_QUEUES` here once the `RedisQueue.NAMESPACE` has been modified in conftest to be
        # able to parallelize tests. Otherwise, it would be initialized to the default value, causing clashes.
        JobExecutor.ALIVE_QUEUES = f"{RedisQueue.NAMESPACE}:alive_queues"
        self._import_workers = import_workers
        self._import_workers_per_database = (
            import_workers_per_database if import_workers_per_database is not None else {}
        )
        self._import_parquet_workers = import_parquet_workers
        self._import_parquet_workers_per_database = (
            import_parquet_workers_per_database if import_parquet_workers_per_database is not None else {}
        )
        self._query_workers = query_workers
        self._query_workers_per_database = query_workers_per_database if query_workers_per_database is not None else {}
        self._populate_workers = populate_workers
        self._populate_workers_per_database = (
            populate_workers_per_database if populate_workers_per_database is not None else {}
        )
        self._copy_workers = copy_workers
        self._copy_workers_per_database = copy_workers_per_database if copy_workers_per_database is not None else {}
        self._sink_workers = sink_workers
        self._sink_workers_per_database = sink_workers_per_database if sink_workers_per_database is not None else {}
        self._branching_workers = branching_workers
        self._branching_workers_per_database = (
            branching_workers_per_database if branching_workers_per_database is not None else {}
        )
        self._dynamodb_sync_workers = dynamodb_sync_workers
        self._dynamodb_sync_workers_per_database = (
            dynamodb_sync_workers_per_database if dynamodb_sync_workers_per_database is not None else {}
        )
        self._import_threadpool_executors = {}
        self._import_parquet_threadpool_executors = {}
        self._query_threadpool_executors = {}
        self._populate_threadpool_executors = {}
        self._copy_threadpool_executors = {}
        self._sink_threadpool_executors = {}
        self._branching_threadpool_executors = {}
        self._dynamodb_sync_threadpool_executors = {}
        self._redis_client: TBRedisClientSync = redis_client
        self._redis_config = redis_config
        self._consumer = consumer
        self._billing_region = billing_region
        self._billing_provider = billing_provider
        self.id = ulid.new().str

    def _create_import_executor_if_needed(self, database_server: str) -> None:
        # when there is a limit per database, set it up
        if database_server not in self._import_threadpool_executors:
            logging.info(f"New Redis queue found for import jobs for database server '{database_server}'")
            workers = (
                self._import_workers_per_database[database_server]
                if self._import_workers_per_database.get(database_server) is not None
                else self._import_workers
            )
            self._import_threadpool_executors[database_server] = JobThreadPoolExecutor(
                database_server, self._redis_config, workers, JobExecutor.IMPORT
            )

    def _create_import_parquet_executor_if_needed(self, database_server: str) -> None:
        # when there is a limit per database, set it up
        if database_server not in self._import_parquet_threadpool_executors:
            logging.info(f"New Redis queue found for import parquet jobs for database server '{database_server}'")
            workers = (
                self._import_parquet_workers_per_database[database_server]
                if self._import_parquet_workers_per_database.get(database_server) is not None
                else self._import_parquet_workers
            )
            self._import_parquet_threadpool_executors[database_server] = JobThreadPoolExecutor(
                database_server, self._redis_config, workers, JobExecutor.IMPORT_PARQUET
            )

    def _create_query_executor_if_needed(self, database_server: str) -> None:
        if database_server not in self._query_threadpool_executors:
            logging.info(f"New Redis queue found for query jobs for database server '{database_server}'")
            workers = (
                self._query_workers_per_database[database_server]
                if self._query_workers_per_database.get(database_server) is not None
                else self._query_workers
            )
            self._query_threadpool_executors[database_server] = JobThreadPoolExecutor(
                database_server, self._redis_config, workers, JobExecutor.QUERY
            )

    def _create_populate_executor_if_needed(self, database_server: str) -> None:
        if database_server not in self._populate_threadpool_executors:
            logging.info(f"New Redis queue found for populate jobs for database server '{database_server}'")
            workers = (
                self._populate_workers_per_database[database_server]
                if self._populate_workers_per_database.get(database_server) is not None
                else self._populate_workers
            )
            self._populate_threadpool_executors[database_server] = JobThreadPoolExecutor(
                database_server, self._redis_config, workers, JobExecutor.POPULATE
            )

    def _create_copy_executor_if_needed(self, database_server: str) -> None:
        if database_server not in self._copy_threadpool_executors:
            logging.info(f"New Redis queue found for copy jobs for database server '{database_server}'")
            workers = (
                self._copy_workers_per_database[database_server]
                if self._copy_workers_per_database.get(database_server) is not None
                else self._copy_workers
            )
            self._copy_threadpool_executors[database_server] = JobThreadPoolExecutor(
                database_server, self._redis_config, workers, JobExecutor.COPY
            )

    def _create_sink_executor_if_needed(self, database_server: str) -> None:
        if database_server not in self._sink_threadpool_executors:
            logging.info(f"New Redis queue found for sink jobs for database server '{database_server}'")
            workers = (
                self._sink_workers_per_database[database_server]
                if self._sink_workers_per_database.get(database_server) is not None
                else self._sink_workers
            )
            self._sink_threadpool_executors[database_server] = JobThreadPoolExecutor(
                database_server, self._redis_config, workers, JobExecutor.SINK
            )

    def _create_branching_executor_if_needed(self, database_server: str) -> None:
        if database_server not in self._branching_threadpool_executors:
            logging.info(f"New Redis queue found for branching jobs for database server '{database_server}'")
            workers = (
                self._branching_workers_per_database[database_server]
                if self._branching_workers_per_database.get(database_server) is not None
                else self._branching_workers
            )
            self._branching_threadpool_executors[database_server] = JobThreadPoolExecutor(
                database_server, self._redis_config, workers, JobExecutor.BRANCHING
            )

    def _create_dynamodb_sync_executor_if_needed(self, database_server: str) -> None:
        if database_server not in self._dynamodb_sync_threadpool_executors:
            logging.info(f"New Redis queue found for dynamodb_sync jobs for database server '{database_server}'")
            workers = (
                self._dynamodb_sync_workers_per_database[database_server]
                if self._dynamodb_sync_workers_per_database.get(database_server) is not None
                else self._dynamodb_sync_workers
            )
            self._dynamodb_sync_threadpool_executors[database_server] = JobThreadPoolExecutor(
                database_server, self._redis_config, workers, JobExecutor.DYNAMODB_SYNC
            )

    @staticmethod
    def _is_import_kind(job: "Job") -> bool:
        return job.kind == JobKind.IMPORT and hasattr(job, "format") and job.format not in JOB_PARQUET_TYPES

    @staticmethod
    def _is_import_parquet_kind(job: "Job") -> bool:
        return job.kind == JobKind.IMPORT and hasattr(job, "format") and job.format in JOB_PARQUET_TYPES

    @staticmethod
    def _is_copy_kind(job_kind: str) -> bool:
        return job_kind == JobKind.COPY

    @staticmethod
    def _is_sink_kind(job_kind: str) -> bool:
        return job_kind == JobKind.SINK

    @staticmethod
    def _is_populate_kind(job_kind: str) -> bool:
        return job_kind == JobKind.POPULATE

    @staticmethod
    def _is_branching_kind(job_kind: str) -> bool:
        return job_kind in [JobKind.REGRESSION, JobKind.DATA_BRANCH, JobKind.COPY_BRANCH, JobKind.SINK_BRANCH]

    @staticmethod
    def _is_dynamodb_sync_kind(job_kind: str) -> bool:
        return job_kind == JobKind.DYNAMODB_SYNC

    def _create_executor_if_needed(self, job: "Job") -> None:
        database_server: str = job.get_database_server()
        if self._is_import_kind(job):
            self._create_import_executor_if_needed(database_server)
        elif self._is_import_parquet_kind(job):
            self._create_import_parquet_executor_if_needed(database_server)
        elif self._is_copy_kind(job.kind):
            self._create_copy_executor_if_needed(database_server)
        elif self._is_sink_kind(job.kind):
            self._create_sink_executor_if_needed(database_server)
        elif self._is_populate_kind(job.kind):
            self._create_populate_executor_if_needed(database_server)
        elif self._is_branching_kind(job.kind):
            self._create_branching_executor_if_needed(database_server)
        elif self._is_dynamodb_sync_kind(job.kind):
            self._create_dynamodb_sync_executor_if_needed(database_server)
        else:
            self._create_query_executor_if_needed(database_server)

    def _get_executors(self, job: "Job") -> Dict[str, JobThreadPoolExecutor]:
        if self._is_import_kind(job):
            executors = self._import_threadpool_executors
        elif self._is_import_parquet_kind(job):
            executors = self._import_parquet_threadpool_executors
        elif self._is_copy_kind(job.kind):
            executors = self._copy_threadpool_executors
        elif self._is_sink_kind(job.kind):
            executors = self._sink_threadpool_executors
        elif self._is_populate_kind(job.kind):
            executors = self._populate_threadpool_executors
        elif self._is_branching_kind(job.kind):
            executors = self._branching_threadpool_executors
        elif self._is_dynamodb_sync_kind(job.kind):
            executors = self._dynamodb_sync_threadpool_executors
        else:
            executors = self._query_threadpool_executors
        return executors

    def submit(self, function_to_execute: Callable[["Job"], None], job: "Job") -> Any:
        """
        Submit a new task to be executed (function_to_execute) in the ThreadPoolExecutor that
        belongs to the job given.
        """
        self._create_executor_if_needed(job)
        executors = self._get_executors(job)

        return executors[job.get_database_server()].submit(function_to_execute, job)

    def put_job(self, job: "Job") -> None:
        """
        Put the job provided into its belonging Redis queue so that it's run whenever there are
        available workers for that database server.
        """
        self._create_executor_if_needed(job)
        job.set_job_executor(self)
        executors = self._get_executors(job)
        executors[job.get_database_server()].put_job(job.id)

    def join(self) -> None:
        for executor in self._import_threadpool_executors.values():
            logging.info(f"Shutting down import executor for database server '{executor.database_server}'")
            executor.shutdown(wait=executor.shutdown_wait)
            logging.info(f"Import executor for database server '{executor.database_server}' has been shut down")
        for executor in self._import_parquet_threadpool_executors.values():
            logging.info(f"Shutting down import parquet executor for database server '{executor.database_server}'")
            executor.shutdown(wait=executor.shutdown_wait)
            logging.info(f"Import parquet executor for database server '{executor.database_server}' has been shut down")
        for executor in self._query_threadpool_executors.values():
            logging.info(f"Shutting down query executor for database server '{executor.database_server}'")
            executor.shutdown(wait=executor.shutdown_wait)
            logging.info(f"Query executor for database server '{executor.database_server}' has been shut down")
        for executor in self._populate_threadpool_executors.values():
            logging.info(f"Shutting down populate executor for database server '{executor.database_server}'")
            executor.shutdown(wait=executor.shutdown_wait)
            logging.info(f"Populate executor for database server '{executor.database_server}' has been shut down")
        for executor in self._copy_threadpool_executors.values():
            logging.info(f"Shutting down copy executor for database server '{executor.database_server}'")
            executor.shutdown(wait=executor.shutdown_wait)
            logging.info(f"Export executor for database server '{executor.database_server}' has been shut down")
        for executor in self._sink_threadpool_executors.values():
            logging.info(f"Shutting down sink executor for database server '{executor.database_server}'")
            executor.shutdown(wait=executor.shutdown_wait)
            logging.info(f"Sink executor for database server '{executor.database_server}' has been shut down")
        for executor in self._branching_threadpool_executors.values():
            logging.info(f"Shutting down branching executor for database server '{executor.database_server}'")
            executor.shutdown(wait=executor.shutdown_wait)
            logging.info(f"Branching executor for database server '{executor.database_server}' has been shut down")
        for executor in self._dynamodb_sync_threadpool_executors.values():
            logging.info(f"Shutting down dynamodb_sync executor for database server '{executor.database_server}'")
            executor.shutdown(wait=executor.shutdown_wait)
            logging.info(f"DynamoDB Sync executor for database server '{executor.database_server}' has been shut down")

    def get_job_executor(self, job: "Job") -> JobThreadPoolExecutor:
        executors = self._get_executors(job)
        return executors[job.get_database_server()]

    def get_all_executors(self) -> Iterable[JobThreadPoolExecutor]:
        return (
            list(self._import_threadpool_executors.values())
            + list(self._import_parquet_threadpool_executors.values())
            + list(self._query_threadpool_executors.values())
            + list(self._populate_threadpool_executors.values())
            + list(self._copy_threadpool_executors.values())
            + list(self._sink_threadpool_executors.values())
            + list(self._branching_threadpool_executors.values())
            + list(self._dynamodb_sync_threadpool_executors.values())
        )

    def get_wip_and_queued_jobs(self) -> Tuple[List["Job"], List["Job"]]:
        # When starting with no consumer, there is no JobProcessor. Thus, there are no periodic checks
        # to check_for_new_queues, which is why we need to explicitly do it here.
        self.check_for_new_queues(force=True)
        executors = self.get_all_executors()
        wip_jobs = []
        queued_jobs = []
        if executors:
            for executor in executors:
                wip_jobs_tmp, queued_jobs_tmp = executor.get_pending_jobs()
                wip_jobs += wip_jobs_tmp
                queued_jobs += queued_jobs_tmp

        return wip_jobs, queued_jobs

    def get_pending_jobs(self) -> List["Job"]:
        wip_jobs, queued_jobs = self.get_wip_and_queued_jobs()
        return wip_jobs + queued_jobs

    def is_queue_modified_within_timespan(self, timespan: int, last_updated_timestamp: float) -> bool:
        return last_updated_timestamp >= timespan

    def has_wip_items(self, queue_key: bytes) -> bool:
        try:
            return self._redis_client.scard(f"{queue_key.decode('utf-8')}:{RedisQueue.WIP_KEY_NAME}") > 0
        except UnicodeDecodeError as e:
            logging.exception(f"Can't decode queue_key {queue_key!r}: {e}")
            return False

    def refresh_alive_queues(self, force_alive: Optional[bool] = False) -> Set[bytes]:
        alive_queues = set()
        two_hours_before = int(time.time()) - JobExecutor.ALIVE_QUEUES_TTL_IN_SECONDS

        # Get all queues defined in the "queue:alive_queues" Redis Key
        # and the latest modification time
        job_queues = self._redis_client.zrange(JobExecutor.ALIVE_QUEUES, 0, -1, withscores=True)

        # Return queues that have work-in-progress elements
        # or have modified within the last 2h
        for queue_name, last_updated_time in job_queues:
            if (
                force_alive
                or self.is_queue_modified_within_timespan(two_hours_before, last_updated_time)
                or self.has_wip_items(queue_name)
            ):
                alive_queues.add(queue_name)
            else:
                # Remove the old queues from Redis that are not considered alive anymore
                self._redis_client.zrem(JobExecutor.ALIVE_QUEUES, queue_name)

        return alive_queues

    def check_for_new_queues(self, force=False) -> None:
        # Ensure that we run this at most every CHECK_NEW_QUEUES_FREQ_IN_SECONDS seconds
        now = int(time.time())
        if force or (
            not self._last_queue_keys_check
            or now - self._last_queue_keys_check > JobExecutor.CHECK_NEW_QUEUES_FREQ_IN_SECONDS
        ):
            force_alive = force or self._last_queue_keys_check is None
            self._last_queue_keys_check = now

            # Collect from Redis the recent queues that are considered alive and ask the existing threads without
            # their corresponding Redis queues to finish to release unnecessary resources.
            assert isinstance(JobExecutor.ALIVE_QUEUES, str)
            queues = self.refresh_alive_queues(force_alive)
            import_queues_alive = set()
            import_parquet_queues_alive = set()
            query_queues_alive = set()
            populate_queues_alive = set()
            copy_queues_alive = set()
            sink_queues_alive = set()
            branching_queues_alive = set()
            dynamodb_sync_queues_alive = set()
            for key in queues:
                queue_name = key.decode("utf-8")
                database_server, _type = get_database_server_and_queue_type(queue_name)
                if database_server is None or _type is None:
                    continue

                if JobExecutor.IMPORT == _type:
                    self._create_import_executor_if_needed(database_server)
                    import_queues_alive.add(database_server)
                elif JobExecutor.IMPORT_PARQUET == _type:
                    self._create_import_parquet_executor_if_needed(database_server)
                    import_parquet_queues_alive.add(database_server)
                elif JobExecutor.QUERY == _type:
                    self._create_query_executor_if_needed(database_server)
                    query_queues_alive.add(database_server)
                elif JobExecutor.POPULATE == _type:
                    self._create_populate_executor_if_needed(database_server)
                    populate_queues_alive.add(database_server)
                elif JobExecutor.SINK == _type:
                    self._create_sink_executor_if_needed(database_server)
                    sink_queues_alive.add(database_server)
                elif JobExecutor.COPY == _type:
                    self._create_copy_executor_if_needed(database_server)
                    copy_queues_alive.add(database_server)
                elif JobExecutor.BRANCHING == _type:
                    self._create_branching_executor_if_needed(database_server)
                    branching_queues_alive.add(database_server)
                elif JobExecutor.DYNAMODB_SYNC == _type:
                    self._create_dynamodb_sync_executor_if_needed(database_server)
                    dynamodb_sync_queues_alive.add(database_server)

            def _shutdown_executors(queues_alive: Set[str], threadpool: Dict[str, JobThreadPoolExecutor]) -> None:
                to_shutdown = [
                    database_server for database_server in threadpool.keys() if database_server not in queues_alive
                ]
                for database_server in to_shutdown:
                    if not threadpool[database_server].has_jobs_wip():
                        # If no jobs are in progress, we shouldn't have any tasks in the queue
                        # Validation to check the issue https://gitlab.com/tinybird/analytics/-/issues/14058
                        # TODO: If no jobs are in progress, why not use wait=True and be confident about it?
                        pending_tasks = (
                            threadpool[database_server]._thread_pool_executor._work_queue.qsize()  # type: ignore
                            if threadpool[database_server]._thread_pool_executor
                            else 0
                        )
                        if pending_tasks > 0:
                            logging.warning(
                                f"We still have {pending_tasks} being processed for {database_server} with type {threadpool[database_server].kind}"
                            )

                        threadpool[database_server].shutdown(wait=False)
                        del threadpool[database_server]

            # Only try to shut down executors during our normal cycle calling this method without force.
            # This is to avoid a potential race condition in which we call get_wip_and_queued_jobs from
            # a different thread, which ends up calling this method with force=True.
            if not force:
                _shutdown_executors(import_queues_alive, self._import_threadpool_executors)
                _shutdown_executors(import_parquet_queues_alive, self._import_parquet_threadpool_executors)
                _shutdown_executors(query_queues_alive, self._query_threadpool_executors)
                _shutdown_executors(populate_queues_alive, self._populate_threadpool_executors)
                _shutdown_executors(copy_queues_alive, self._copy_threadpool_executors)
                _shutdown_executors(sink_queues_alive, self._sink_threadpool_executors)
                _shutdown_executors(branching_queues_alive, self._branching_threadpool_executors)
                _shutdown_executors(dynamodb_sync_queues_alive, self._dynamodb_sync_threadpool_executors)

    def job_finished(self, job: "Job") -> None:
        database_server = job.get_database_server()
        executors = self._get_executors(job)
        if database_server in executors:
            executors[database_server].job_finished(job.id)
            statsd_prefix = f"tinybird.{statsd_client.region_machine}.jobs.{sanitize_database_server(database_server)}.{job.get_database()}.{job.kind}"
            job_status = "ok" if job.status != JobStatus.ERROR else "error"
            statsd_client.incr(f"{statsd_prefix}.{job_status}")
            if job.updated_at is not None:
                statsd_client.timing(f"{statsd_prefix}.total", (job.updated_at - job.created_at).seconds)
            if job.started_at is not None:
                statsd_client.timing(f"{statsd_prefix}.working", (job.updated_at - job.started_at).seconds)
        else:
            logging.warning(
                f"Job {job.id} finished, but there is no executor available for database_server {database_server}. This should only happen running tests"
            )

    def is_consumer(self) -> bool:
        return self._consumer

    def start_consumer(self) -> Optional[JobProcessor]:
        if self._consumer:
            job_processor = JobProcessor(job_executor=self)
            if running_in_testing_environment():
                job_processor.daemon = True
            job_processor.start()
            return job_processor
        else:
            logging.warning("Jobs is not a consumer, set or load it as a consumer")
            return None

    def _clean(self) -> None:
        """
        Method to be used during testing only to make sure that there are no leftovers in terms
        of queues or jobs.
        """
        queue_keys = self._redis_client.keys(f"{RedisQueue.NAMESPACE}:*")
        for key in queue_keys:
            self._redis_client.delete(key)
        jobs = self._redis_client.keys(f"{Job.__namespace__}:*")
        for key in jobs:
            self._redis_client.delete(key)


class Job(RedisModel):
    """base class for all jobs"""

    __namespace__ = "jobs"
    __ttl__ = JOB_TTL_IN_HOURS * 3600
    __owner__ = "user_id"
    # This property can be overriden in certain
    # environments depending on configuration variables
    # through override_owner_max_children()
    __owner_max_children__ = 100

    @staticmethod
    def create_import(
        url: str,
        headers: Dict[str, str],
        workspace: Workspace,
        datasource: Datasource,
        request_id: str,
        dialect_overrides: Dict[str, Any],
        type_guessing: bool = True,
        mode: str = "create",
        job_id: Optional[str] = None,
        replace_condition: Optional[str] = None,
        format: Optional[str] = None,
    ):
        j = ImportJob(
            workspace=workspace,
            datasource=datasource,
            url=url,
            headers=headers,
            request_id=request_id,
            dialect_overrides=dialect_overrides,
            type_guessing=type_guessing,
            mode=mode,
            job_id=job_id,
            replace_condition=replace_condition,
            format=format,
        )
        j.save()
        return j

    @staticmethod
    def create_delete(delete_condition: str, headers, workspace: Workspace, datasource, request_id: str):
        j = DeleteJob(
            workspace=workspace,
            datasource=datasource,
            delete_condition=delete_condition,
            headers=headers,
            request_id=request_id,
        )
        j.save()
        return j

    def __init__(
        self,
        kind: str,
        user: Optional[Workspace],
        job_id: Optional[str] = None,
        datasource: Optional[Datasource] = None,
    ) -> None:
        self.id: str = job_id if job_id is not None else str(uuid.uuid4())
        self.kind: str = kind
        self.user_id: Optional[str] = user.id if user is not None else None
        self.workspace_name: str = user.name if user is not None else ""
        self.created_at: datetime = datetime.utcnow()
        self.updated_at: datetime = self.created_at
        self.started_at: Optional[datetime] = None
        self.status: str = JobStatus.WAITING
        self._result: Optional[Dict[str, Any]] = None
        self.stats: Optional[Dict[str, Any]] = None
        self.datasource: Optional[Datasource] = datasource

        self.logs: List[Tuple[str, datetime, str, str, str, str]] = []

    @classmethod
    def override_owner_max_children(cls, owner_max_children: int):
        cls.__owner_max_children__ = owner_max_children

    @classmethod
    def get_owner_max_children(cls) -> int:
        return cls.__owner_max_children__

    def __getstate__(self) -> Dict[str, Any]:
        state = self.__dict__.copy()
        if "user" in state:
            del state["user"]
        if "job_executor" in state:
            del state["job_executor"]
        return state

    def __setstate__(self, state: Dict[str, Any]) -> None:
        self.__dict__.update(state)
        save_required = False
        if "created_at" not in state:
            self.created_at = datetime.utcnow()
            save_required = True
        if "updated_at" not in state:
            self.updated_at = datetime.utcnow()
            save_required = True
        if "user_id" not in state and "user" in state:
            self.user_id = state["user"].id
            save_required = True
        if save_required:
            self.save()
        if self.user_id is not None:
            self.user: Workspace = Workspace.get_by_id(self.user_id)

    def to_json(self, workspace: Optional[Workspace] = None, debug: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        job: Dict[str, Any] = {
            "kind": self.kind,
            "id": self.id,
            "job_id": self.id,
            "status": self.status,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            "started_at": str(self.started_at) if self.started_at else None,
            "is_cancellable": self.is_cancellable,
        }

        if hasattr(self, "mode") and self.mode:
            job.update({"mode": self.mode})

        datasource = self.datasource_to_json(workspace=workspace)
        if datasource:
            job.update({"datasource": datasource})

        return job

    def datasource_to_json(self, workspace: Optional[Workspace] = None) -> Optional[Dict[str, Any]]:
        if not hasattr(self, "datasource"):
            return None

        if self.datasource is None:
            return None

        datasource = {"id": self.datasource.id}

        if workspace:
            # Using the name as the id might refer to a temporal data source.
            # An example of that is when using mode=replace.
            # This might lead to unexpected results if the user changes
            # another Data Source's name to the one associated with the job.
            ds = Workspaces.get_datasource(workspace, self.datasource.name)
            if not ds:
                # Trying to load from the ID.
                # This should cover the scenario where the user changed the Data
                # Source name and the job was not a mode=replace one.
                ds = Workspaces.get_datasource(workspace, self.datasource.id)
            if ds:
                datasource = ds.to_json()

        return datasource

    def to_public_json(self, job: "Job", api_host: str = ""):
        workspace_job = {
            "id": job.id,
            "kind": job.kind,
            "status": job.status,
            "created_at": str(job.created_at),
            "updated_at": str(job.updated_at),
            "is_cancellable": job.is_cancellable,
        }
        if api_host:
            workspace_job.update(
                {
                    "job_url": f"{api_host}/v0/jobs/{job.id}",
                }
            )
        if hasattr(job, "pipe_name") and hasattr(job, "pipe_id"):
            workspace_job.update(
                {
                    "pipe_id": job.pipe_id,
                    "pipe_name": job.pipe_name,
                }
            )
        try:
            if hasattr(job, "datasource") and job.datasource:
                workspace_job.update({"datasource": {"id": job.datasource.id, "name": job.datasource.name}})
        except Exception as e:
            logging.exception(f'There was a problem with job "{job.id}" data source: {e}')
        return workspace_job

    async def progress_details(self):
        return {}

    @property
    def result(self) -> Dict[str, Any]:
        return self._result if self._result else {}

    @result.setter
    def result(self, value: Optional[Dict[str, Any]]) -> None:
        self._result = value

    def getLogger(
        self,
    ) -> logging.Logger:  # TODO store the logger in the object so it can be stored inside it and avoid recreation
        logger = logging.getLogger(f"job-{self.id}")
        handler = JobLogHandler(self)
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    def log(self, message) -> None:
        self.logs.append((self.id, datetime.utcnow(), message, self.user["id"], self.status, self.kind))

    def _to_storage(self):
        return self

    @classmethod
    def _from_storage(cls, value):
        return value

    def send_raw_event(self: "Job") -> None:
        pass

    def mark_as_done(
        self: "Job", result: Any, stats: Any, sql: str | None = None, should_send_raw_event: bool = True
    ) -> "Job":
        @retry_job_transaction_in_case_of_error_sync()
        def _done(j: "Job") -> "Job":
            with Job.transaction(j.id) as j:
                j.updated_at = datetime.utcnow()
                j.status = JobStatus.DONE
                j.result = result
                j.stats = stats
                if sql and hasattr(j, "sql"):
                    j.sql = sql
                return j

        j = _done(self)

        if should_send_raw_event and hasattr(self, "send_raw_event"):
            j.send_raw_event()

        # To allow using this method from the outside after deserializing a job
        # from Redis. Note the job_executor is never serialized.
        if hasattr(self, "job_executor"):
            self.job_executor.job_finished(j)
        return j

    def mark_as_cancelling(
        self: "Job", result: Optional[Dict[str, Any]], sql: str | None = None, should_send_raw_event: bool = True
    ) -> "Job":
        @retry_job_transaction_in_case_of_error_sync()
        def _cancelling(j: "Job") -> "Job":
            with Job.transaction(j.id) as j:
                j.updated_at = datetime.utcnow()
                j.status = JobStatus.CANCELLING
                # FIXME expression has type "Optional[Dict[str, Any]]", variable has type "Dict[str, Any]")
                j.result = cast(Dict[str, Any], result)
                j.stats = None
                if sql and hasattr(j, "sql"):
                    j.sql = sql
                return j

        j = _cancelling(self)

        if should_send_raw_event and hasattr(self, "send_raw_event"):
            j.send_raw_event()

        # To allow using this method from the outside after deserializing a job
        # from Redis. Note the job_executor is never serialized.
        if hasattr(self, "job_executor"):
            self.job_executor.job_finished(j)
        return j

    def mark_as_error(
        self: "Job", result: Optional[Dict[str, Any]], sql: str | None = None, should_send_raw_event: bool = True
    ) -> "Job":
        @retry_job_transaction_in_case_of_error_sync()
        def _error(j: "Job") -> "Job":
            with Job.transaction(j.id) as j:
                j.updated_at = datetime.utcnow()
                j.status = JobStatus.ERROR
                # FIXME expression has type "Optional[Dict[str, Any]]", variable has type "Dict[str, Any]")
                j.result = cast(Dict[str, Any], result)
                j.stats = None
                if sql and hasattr(j, "sql"):
                    j.sql = sql
                return j

        j = _error(self)

        if should_send_raw_event and hasattr(self, "send_raw_event"):
            j.send_raw_event()

        # To allow using this method from the outside after deserializing a job
        # from Redis. Note the job_executor is never serialized.
        if hasattr(self, "job_executor"):
            self.job_executor.job_finished(j)
        return j

    def mark_as_working(self) -> "Job":
        @retry_job_transaction_in_case_of_error_sync()
        def _working(j: "Job") -> "Job":
            with Job.transaction(j.id) as j:
                j.updated_at = datetime.utcnow()
                j.started_at = j.updated_at
                if j.status in (JobStatus.CANCELLING, JobStatus.CANCELLED):
                    raise JobCancelledException()
                if j.status in (JobStatus.ERROR, JobStatus.DONE):
                    raise RuntimeError(
                        f"Job tried to transition from the '{j.status}' final status to '{JobStatus.WORKING}' status"
                    )
                j.status = JobStatus.WORKING
                return j

        j = _working(self)

        if hasattr(self, "send_raw_event"):
            j.send_raw_event()

        return j

    @property
    def is_cancellable(self) -> bool:
        return self.status == JobStatus.WAITING

    def try_to_cancel(self, job_executor: Optional[JobExecutor] = None) -> "Job":
        logger = self.getLogger()

        @retry_transaction_in_case_of_concurrent_edition_error_sync()
        def _try_to_cancel_in_transaction() -> "Job":
            with Job.transaction(self.id) as job:
                if job.status == JobStatus.CANCELLING:
                    logger.info("Tried to cancel Job with id: %s which is already being cancelled", job.id)
                    raise JobAlreadyBeingCancelledException(job.id)

                if not job.is_cancellable:
                    logger.info("Job %s is not in a cancellable status", job.id)
                    raise JobNotInCancellableStatusException(job.id)

                job.updated_at = datetime.utcnow()

                if job.status == JobStatus.WAITING:
                    job.status = JobStatus.CANCELLED
                    job.stats = None
                else:
                    job.status = JobStatus.CANCELLING
            return job

        job = _try_to_cancel_in_transaction()
        final_status = job.status
        if final_status == JobStatus.CANCELLED:
            # try_to_cancel is the only method that can be called on a Job object deserialized directly
            # from Redis via the /jobs/(.+)/cancel API. In this case, the job does not have a job_executor
            # set to it, so we need to retrieve it from the parameter.
            if hasattr(self, "job_executor"):
                self.job_executor.job_finished(self)
            else:
                assert isinstance(job_executor, JobExecutor)
                job_executor.job_finished(self)
        return job

    @property
    def can_be_mark_as_cancelled(self: "Job") -> bool:
        return bool(self.status == JobStatus.CANCELLING)

    def mark_as_cancelled(self: "Job", sql: str | None = None) -> "Job":
        logger = self.getLogger()
        error = False

        @retry_job_transaction_in_case_of_error_sync()
        def _cancel(j: "Job", query: str | None = None) -> Tuple[bool, "Job"]:
            with Job.transaction(j.id) as job:
                if query and hasattr(job, "sql"):
                    job.sql = query

                if job.status == JobStatus.CANCELLED:
                    return False, job

                if job.status != JobStatus.CANCELLING:
                    logger.error(
                        "Job %s has not been correctly cancelled and can't transition to CANCELLED from %s",
                        self.id,
                        job.status,
                    )
                    return True, job
                else:
                    job.updated_at = datetime.utcnow()
                    job.status = JobStatus.CANCELLED
                    job.stats = None
                    return False, job

        error, j = _cancel(self, sql)

        if error:
            self.mark_as_error(None)
        else:
            if hasattr(self, "send_raw_event"):
                j.send_raw_event()

            if hasattr(self, "job_executor"):
                self.job_executor.job_finished(j)
            logger.info("Job %s correctly cancelled", self.id)
        return j

    def get_database_server(self) -> str:
        """Some subclasses have a `database_server` property. We can't safely add the property to the base
        class without breaking our Redis persistence. So we revert to this method to get rid of Mypy
        errors.
        """
        return self.database_server  # type: ignore

    def set_job_executor(self, job_executor: JobExecutor) -> None:
        """Some subclasses have a `job_executor` property. We can't safely add the property to the base
        class without breaking our Redis persistence. So we revert to this method to get rid of Mypy
        errors.
        """
        self.job_executor: JobExecutor = job_executor

    def get_database(self) -> str:
        """Some subclasses have a `database` property. We can't safely add the property to the base
        class without breaking our Redis persistence. So we revert to this method to get rid of Mypy
        errors.
        """
        return self.database  # type: ignore

    def run(self) -> "Job":
        """Subclasses implement this method and is called in a generic instance.
        We need to declare here in order to Mypy to pass.
        """
        self.getLogger().exception("Job::run() called")
        return self

    def _log_comment(self, extra_fields: Dict[str, Any] | None = None) -> dict:
        return {
            "job_id": self.id,
            "job_kind": self.kind,
            # TODO: Remove this once all the jobs already have the workspace attribute
            "workspace_name": self.workspace_name if hasattr(self, "workspace_name") else "",
            **(extra_fields or {}),
        }

    def _generate_log_comment(self, extra_fields: Dict[str, Any] | None = None) -> bytes:
        """
        Generate a log that will be used for debugging or validator to have better tracking of the queries
        """
        log = orjson.dumps(self._log_comment(extra_fields))
        return log


class DeleteJob(Job):
    def __init__(
        self,
        workspace: Workspace,
        datasource: Datasource,
        delete_condition: str,
        headers: Dict[str, str],
        request_id: str,
    ) -> None:
        self.database_server = workspace.database_server
        self.database = workspace.database
        self.delete_condition = delete_condition
        self.headers = headers
        self.request_id = request_id
        Job.__init__(self, JobKind.DELETE_DATA, workspace, datasource=datasource)

    def to_json(self, workspace: Optional[Workspace] = None, debug: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        job = super().to_json(workspace, debug)

        assert isinstance(self.datasource, Datasource)
        job.update(
            {
                "delete_condition": self.delete_condition,
                "datasource": {"id": self.datasource.id, "name": self.datasource.name},
            }
        )

        if self.status == JobStatus.ERROR and "error" in self.result:
            job["error"] = self.result["error"]
        return job

    def send_raw_event(self: "DeleteJob") -> None:
        updated_delete_job = self.get_by_id(self.id)
        if not updated_delete_job:
            logging.exception(f"Delete job {self.id} not found")
            return
        deletejob_event = convert_deletejob_to_rawevent(updated_delete_job)
        raw_events_batcher.append_record(deletejob_event)

    def run(self) -> "DeleteJob":
        def function_to_execute(job: Job) -> None:
            job = cast("DeleteJob", job)
            try:
                DeleteJob.run_delete(job)
            except JobCancelledException:
                self.mark_as_cancelled()
            except Exception as e:
                self.mark_as_error({"error": str(e)})
            else:
                self.mark_as_done({}, None)

        self.job_executor.submit(function_to_execute, self)
        return self

    @staticmethod
    def run_delete(j: "DeleteJob") -> None:
        logger = j.getLogger()

        assert isinstance(j.datasource, Datasource)
        assert isinstance(j.user_id, str)

        try:
            workspace = j.user
            j.mark_as_working()
            for hook in j.datasource.hooks:
                hook.before_delete_with_condition(j.datasource)

            rows_aprox_affected: Optional[int] = None
            extra_params = {}

            allow_subqueries = False
            if FeatureFlagsWorkspaceService.feature_for_id(
                FeatureFlagWorkspaces.DELETE_JOB_ALLOW_NONDETERMINISTIC_MUTATIONS, workspace.id, workspace.feature_flags
            ):
                extra_params.update({"allow_nondeterministic_mutations": 1})
                allow_subqueries = True

            try:
                rows_aprox_affected = rows_affected_by_delete_sync(workspace, j.datasource.id, j.delete_condition)
            except Exception as e:
                logging.exception(
                    f"Problem while trying to get rows_affected_by_delete_sync - Job {j.id} - Datasource {j.datasource.id} Database {j.database}: {str(e)}"
                )
                if allow_subqueries:
                    raise
                else:
                    rows_aprox_affected = None

            # In case we didn't retrive the number of rows or the numbers of rows > 0, let's run run the delete operation
            if rows_aprox_affected is None or rows_aprox_affected > 0:
                ch_delete_condition_sync(
                    j.database_server,
                    j.database,
                    j.datasource.id,
                    j.delete_condition,
                    cluster=workspace.cluster,
                    wait_replicas=0,
                    extra_params=extra_params,
                )

            for hook in j.datasource.hooks:
                hook.after_delete_with_condition(j.datasource)
        except JobCancelledException as e:
            raise e
        except Exception as e:
            logger.error("Failed to complete the delete with condition job")
            logger.exception(e)
            for hook in j.datasource.hooks:
                hook.on_error(j.datasource, str(e))
            raise e
        finally:
            user = Workspace.get_by_id(j.user_id)
            tracker.track_datasource_ops(
                j.datasource.operations_log(), request_id=j.request_id, job_id=j.id, workspace=user
            )
            tracker.track_hooks(
                j.datasource.hook_log(), request_id=j.request_id, job_id=j.id, source="delete", workspace=user
            )


class CHExceptionWithSummary(Exception):
    def __init__(self, query_id: str, ch_error: str, headers: Optional[HTTPHeaders] = None):
        super().__init__(ch_error)
        self.ch_summary = (
            CHSummary(query_id=query_id, summary=json.loads(headers.get("X-ClickHouse-Summary"))) if headers else None
        )


class ImportJob(Job):
    """import job state"""

    def __init__(
        self,
        workspace: Workspace,
        datasource: Datasource,
        url: str,
        headers: Dict[str, str],
        request_id: str,
        dialect_overrides: Optional[Dict[str, str]],
        type_guessing: bool = True,
        mode: str = "create",
        job_id: Optional[str] = None,
        replace_condition: Optional[str] = None,
        format: Optional[str] = None,
    ) -> None:
        database_server = workspace.database_server
        database = workspace.database
        self.url = url
        self.mode = mode
        self.database = database
        self.database_server = database_server
        self.headers = headers
        self.request_id = request_id
        self.dialect_overrides = dialect_overrides or {}
        self.type_guessing = type_guessing
        self.block_log: List[Dict[str, str]] = []
        self.other_datasources_to_replace: Dict[str, Any] = {}
        self.replace_condition = replace_condition
        self.format = format
        self.parquet_stats: Optional[Dict[str, Any]] = None
        kind = JobKind.IMPORT
        Job.__init__(self, kind, workspace, job_id, datasource=datasource)

        self.__ttl__ = 3600 * int(
            workspace.get_limits(prefix="import").get("import_max_job_ttl_in_hours", Limit.import_max_job_ttl_in_hours)
        )

    def __setstate__(self, state: Dict[str, Any]) -> None:
        super().__setstate__(state)
        if "mode" not in state:
            self.mode = "unknown"

    def get_s3_dataconnector_if_exists(self) -> Optional[str]:
        data_linker = None
        try:
            data_linker = self.datasource.get_data_linker() if self.datasource else None
        except DataSourceNotConnected:
            pass
        is_S3_datasource = bool(data_linker and data_linker.service == DataConnectors.AMAZON_S3_IAMROLE)
        data_connector_id = data_linker.data_connector_id if data_linker and is_S3_datasource else None
        return data_connector_id

    def to_json(self, workspace: Optional[Workspace] = None, debug: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        datasource = self.datasource_to_json(workspace=workspace)

        errors, quarantine_rows, invalid_lines = get_errors(self.result.get("blocks", []))
        if self.result.get("quarantine_rows") is not None:
            quarantine_rows = self.result["quarantine_rows"]

        d = super().to_json(workspace, debug)
        d.update(
            {
                "import_id": self.id,
                "mode": self.mode,
                "url": self.url,
                "statistics": self.stats,
                "datasource": datasource,
                "quarantine_rows": quarantine_rows,
                "invalid_lines": invalid_lines,
            }
        )

        if hasattr(self, "other_datasources_to_replace") and self.other_datasources_to_replace:
            d["other_datasources_to_replace"] = self.other_datasources_to_replace

        if hasattr(self, "replace_condition") and self.replace_condition:
            d["replace_condition"] = self.replace_condition

        self.add_debug_to_json(d, debug)

        job_error = self.result.get(JobStatus.ERROR, None)

        if job_error:
            errors.insert(0, job_error)

        if (self.status == JobStatus.ERROR and errors) or invalid_lines > 0 or quarantine_rows > 0:
            d["error"] = build_error_summary(errors, quarantine_rows, invalid_lines)
            if errors:
                d["errors"] = errors

        return d

    def add_debug_to_json(self, response: Dict[str, Any], debug: Optional[Dict[str, Any]]) -> None:
        if debug:
            if "blocks" in debug:
                response["blocks"] = self.result.get("blocks", [])
            if "block_log" in debug:
                response["block_log"] = blocks_json(self.block_log)
            if "hook_log" in debug:
                assert isinstance(self.datasource, Datasource)
                response["hook_log"] = hook_log_json(self.datasource.hook_log())

    def send_raw_event(self: "ImportJob") -> None:
        updated_import_job = self.get_by_id(self.id)
        if not updated_import_job:
            logging.exception(f"Import job {self.id} not found")
            return
        importjob_event = convert_importjob_to_rawevent(updated_import_job)
        raw_events_batcher.append_record(importjob_event)

    def run(self) -> "ImportJob":
        def function_to_execute(job: Job) -> None:
            job = cast("ImportJob", job)

            try:
                assert isinstance(self.user_id, str)
                user = Workspace.get_by_id(self.user_id)

                if self.datasource is not None and user.get_datasource(self.datasource.name) is None:
                    raise Exception("Datasource no longer exists.")

                data_connector_id = self.get_s3_dataconnector_if_exists()
                if data_connector_id and isinstance(user, Workspace):
                    try:
                        signed_url = async_to_sync(sign_s3_url)(data_connector_id, user, self.url, self.id)
                        if isinstance(signed_url, str):
                            self.update_url(signed_url)
                            job.url = signed_url
                    except (
                        InvalidS3URL,
                        AWSClientException,
                    ) as e:  # for the moment we are not going to raise the exception and will continue with the import, once this is _the way_ to import anything from S3, we should
                        logging.exception(f"Failed to sign S3 URL for job {self.id} {e}")
                        pass
                    except Exception as e:
                        logging.exception(f"Uncontrolled exception trying to sign S3 URL for job {self.id} {e}")
                        pass

                if self.format == "csv" or self.format is None:
                    r = ImportJob.import_csv_job(job)
                else:
                    r = ImportJob.import_parquet_ndjson_job(job)
                import_result = r["import_result"]

                assert isinstance(self.datasource, Datasource)

                tracker.track_blocks(
                    request_id=self.request_id,
                    workspace=user,
                    import_id=self.id,
                    job_id=self.id,
                    source=self.url,
                    block_log=self.block_log,
                    blocks=import_result.get("blocks", []),
                    token_id="",
                    datasource_id=self.datasource.id,
                    datasource_name=self.datasource.name,
                )

                tracker.track_hooks(
                    self.datasource.hook_log(),
                    request_id=self.request_id,
                    import_id=self.id,
                    job_id=self.id,
                    source=job.url,
                    workspace=user,
                )

                blocks_ids = [b["block_id"] for b in self.block_log]

                # We don't want to track datasource_ops when sending to the Gatherer
                if import_result.get("track_datasource_ops", True):
                    tracker.track_datasource_ops(
                        self.datasource.operations_log(),
                        request_id=self.request_id,
                        import_id=self.id,
                        job_id=self.id,
                        source=job.url,
                        blocks_ids=blocks_ids,
                        workspace=user,
                        blocks=import_result.get("blocks", []),
                    )

                # Mark only after tracking everything
                # This is done so we can effectively wait for the tasks once the job is marked as done (or error)
                if "error" in import_result:
                    self.mark_as_error(import_result)
                else:
                    self.mark_as_done(import_result, import_result["stats"])

                logging.debug(f"finished job = {r}")
            except JobCancelledException:
                self.mark_as_cancelled()
            except Exception as e:
                logging.exception(f"Failed to run import {self.format if self.format else 'csv'} job {self.id} {e}")
                self.mark_as_error({"error": str(e)})

        self.job_executor.submit(function_to_execute, self)

        return self

    @staticmethod
    def import_csv_job(j: "ImportJob") -> Dict[str, Any]:
        datasource = j.datasource
        error = None
        import_result = {}

        try:
            j.mark_as_working()

            assert datasource
            import_result = import_csv(
                j.user,  # FIXME workspace
                datasource,
                j.url,
                headers=j.headers,
                existing_block_status_log=j.block_log,
                dialect_overrides=j.dialect_overrides,
                type_guessing=j.type_guessing,
                import_id=j.id,
            )

            if "error" in import_result:
                error = import_result["error"]

                user_errors = []

                for error_ in import_result.get("errors", []):
                    if is_user_error(error_):
                        user_errors.append(replace_table_id_with_datasource_id(j.user, error_))

                if user_errors:
                    error += f" ({', '.join(user_errors)})"
            else:
                try:
                    assert isinstance(datasource, Datasource)
                    for hook in datasource.hooks:
                        hook.after_append(datasource)
                except Exception as e:
                    error = None
                    if isinstance(e, CHException):
                        error = translate_ch_error_to_user_on_post_hook_error(e)
                    if isinstance(e, HookException):
                        error = str(e)
                    if not error:
                        error = HOOKS_ERR_DEFAULT
                    error = f"Error when running after import tasks on job {j.id}: {error}"
                    raise Exception(error) from e
        except JobCancelledException as e:
            raise e
        except Exception as e:
            logging.exception(f"Job='{j.id}' {e}")
            error = str(e)

        if error:
            assert isinstance(datasource, Datasource)
            for hook in datasource.hooks:
                hook.on_error(datasource, error)

            import_result["error"] = error

        return {"import_result": import_result}

    @staticmethod
    def get_max_file_size_limit(workspace: Workspace, format: str) -> int:
        limit_key = "import_max_url_parquet_file_size_gb" if format == "parquet" else "import_max_url_file_size_gb"
        size_limit_workspace_gb = workspace.get_limits(prefix="import").get(limit_key, None)
        limits = []
        if size_limit_workspace_gb is not None:
            limits.append(size_limit_workspace_gb * GB)

        file_size_limit = min(limits) if len(limits) > 0 else None

        return file_size_limit  # type: ignore

    @staticmethod
    def get_replace_hook(datasource: Optional[Datasource]) -> Optional["Hook"]:
        if datasource is None:
            return None

        from tinybird.hook import ReplaceDatasourceBaseHook

        return next(filter(lambda hook: isinstance(hook, ReplaceDatasourceBaseHook), datasource.hooks), None)

    @staticmethod
    def get_append_hook(datasource: Optional[Datasource]) -> Optional["Hook"]:
        if datasource is None:
            return None

        from tinybird.hook import AppendDatasourceHook

        return next(filter(lambda hook: isinstance(hook, AppendDatasourceHook), datasource.hooks), None)

    def _get_schema_from_describe_table(self, format: str, timeout: int, **extra_params: Any) -> DescribeTable:
        return asyncio.run(ch_describe_table_from_url(self.url, format, timeout, **extra_params))

    def _run_query(self, client: HTTPClient, query: str, **kwargs) -> Tuple[HTTPHeaders, bytes]:
        try:
            return client.query_sync(q=query, read_only=False, **kwargs)
        except CHException as e:
            if e.code == CHErrors.UNKNOWN_DATABASE:
                self._create_database(client, kwargs.get("database"))
                return client.query_sync(q=query, read_only=False, **kwargs)
            else:
                raise e

    def _create_database(self, client: HTTPClient, database: Optional[str] = None) -> None:
        database = database if database is not None else client.database
        create_query = f"CREATE DATABASE IF NOT EXISTS {database}"
        client.query_sync(q=create_query, read_only=False, database=None)

    def _parquet_import_url_query_settings(self) -> Dict[str, Any]:
        workspace = Workspace.get_by_id(self.user.id)

        import_limits = workspace.get_limits(prefix="import")
        ch_limits = workspace.get_limits(prefix="ch")

        # we were already using max_insert_threads from general ch limits
        ch_max_insert_threads = ch_limits.get("max_insert_threads", Limit.ch_max_insert_threads)

        max_insert_threads = import_limits.get("import_parquet_url_max_insert_threads", ch_max_insert_threads)
        max_threads = import_limits.get("import_parquet_url_max_threads", Limit.import_parquet_url_max_threads)
        max_insert_block_size = import_limits.get(
            "import_parquet_url_max_insert_block_size", Limit.import_parquet_url_max_insert_block_size
        )
        min_insert_block_size_rows = import_limits.get(
            "import_parquet_url_min_insert_block_size_rows", Limit.import_parquet_url_min_insert_block_size_rows
        )
        min_insert_block_size_bytes = import_limits.get(
            "import_parquet_url_min_insert_block_size_bytes", Limit.import_parquet_url_min_insert_block_size_bytes
        )
        max_memory_usage = import_limits.get(
            "import_parquet_url_max_memory_usage", Limit.import_parquet_url_max_memory_usage
        )
        max_execution_time = import_limits.get(
            "import_parquet_url_max_execution_time", Limit.import_parquet_url_max_execution_time
        )

        input_format_parquet_max_block_size = import_limits.get(
            "import_parquet_url_input_format_parquet_max_block_size",
            Limit.import_parquet_url_input_format_parquet_max_block_size,
        )
        input_format_parquet_allow_missing_columns = import_limits.get(
            "import_parquet_url_input_format_parquet_allow_missing_columns",
            Limit.import_parquet_url_input_format_parquet_allow_missing_columns,
        )
        input_format_null_as_default = import_limits.get(
            "import_parquet_url_input_format_null_as_default", Limit.import_parquet_url_input_format_null_as_default
        )

        max_partitions_per_insert_block = import_limits.get(
            "import_parquet_url_max_partitions_per_insert_block",
            Limit.import_parquet_url_max_partitions_per_insert_block,
        )

        insert_deduplicate = import_limits.get(
            "import_parquet_url_insert_deduplicate", Limit.import_parquet_url_insert_deduplicate
        )

        date_time_overflow_behavior = import_limits.get(
            "import_parquet_url_date_time_overflow_behavior", Limit.import_parquet_url_date_time_overflow_behavior
        )

        enable_url_encoding = import_limits.get(
            "import_parquet_url_enable_url_encoding", Limit.import_parquet_url_enable_url_encoding
        )

        input_format_parquet_skip_columns_with_unsupported_types_in_schema_inference = import_limits.get(
            "import_parquet_url_input_format_parquet_skip_columns_with_unsupported_types_in_schema_inference",
            Limit.import_parquet_url_input_format_parquet_skip_columns_with_unsupported_types_in_schema_inference,
        )

        import_parquet_url_settings = {
            "max_insert_threads": max_insert_threads,
            "max_threads": max_threads,
            "max_insert_block_size": max_insert_block_size,
            "min_insert_block_size_rows": min_insert_block_size_rows,
            "min_insert_block_size_bytes": min_insert_block_size_bytes,
            "max_memory_usage": max_memory_usage,
            "max_execution_time": max_execution_time,
            "input_format_parquet_max_block_size": input_format_parquet_max_block_size,
            "input_format_parquet_allow_missing_columns": input_format_parquet_allow_missing_columns,
            "input_format_null_as_default": input_format_null_as_default,
            "max_partitions_per_insert_block": max_partitions_per_insert_block,
            "insert_deduplicate": insert_deduplicate,
            "date_time_overflow_behavior": date_time_overflow_behavior,
            "enable_url_encoding": enable_url_encoding,
            "input_format_parquet_skip_columns_with_unsupported_types_in_schema_inference": input_format_parquet_skip_columns_with_unsupported_types_in_schema_inference,
        }

        settings: Dict[str, Any] = {
            key: value for key, value in import_parquet_url_settings.items() if value is not None
        }

        settings.update({"log_comment": self._generate_log_comment()})
        return settings

    def _parquet_internal_op_url_settings(self) -> Dict[str, Any]:
        workspace = Workspace.get_by_id(self.user.id)

        import_limits = workspace.get_limits(prefix="import")

        max_execution_time = import_limits.get(
            "import_parquet_url_max_execution_time", Limit.import_parquet_url_max_execution_time
        )

        enable_url_encoding = import_limits.get(
            "import_parquet_url_enable_url_encoding", Limit.import_parquet_url_enable_url_encoding
        )

        input_format_parquet_skip_columns_with_unsupported_types_in_schema_inference = import_limits.get(
            "import_parquet_url_input_format_parquet_skip_columns_with_unsupported_types_in_schema_inference",
            Limit.import_parquet_url_input_format_parquet_skip_columns_with_unsupported_types_in_schema_inference,
        )

        internal_op_parquet_url_settings = {
            "enable_url_encoding": str(enable_url_encoding),
            "max_execution_time": str(max_execution_time),
            "input_format_parquet_skip_columns_with_unsupported_types_in_schema_inference": str(
                input_format_parquet_skip_columns_with_unsupported_types_in_schema_inference
            ),
        }

        settings: Dict[str, Any] = {
            key: value for key, value in internal_op_parquet_url_settings.items() if value is not None
        }
        settings.update({"log_comment": self._generate_log_comment()})
        return settings

    def _import_from_url(
        self,
        client: HTTPClient,
        database: str,
        table: str,
        column_mapping: Dict[str, "ColumnMapping"],
        type_castings: List["ColumnTypeCasting"],
    ) -> CHSummary:
        target_columns, source_columns, source_conditions = build_import_query_parts(column_mapping, type_castings)
        query = f"INSERT INTO {database}.`{table}` ({target_columns}) SELECT {source_columns} FROM url({ch_escape_string(self.url)}, Parquet) WHERE {source_conditions}"
        request_params = {
            "query_id": {self.id},
            **self._parquet_import_url_query_settings(),
        }
        try:
            headers, _ = self._run_query(client=client, query=query, user_agent="tb-lfi", **request_params)
            ch_summary = CHSummary(query_id=self.id, summary=json.loads(headers.get("X-ClickHouse-Summary")))
            return ch_summary
        except CHException as e:
            exc = CHExceptionWithSummary(self.id, f"Error inserting from url: {e}", headers=e.headers)
            raise exc

    def _import_quarantine_from_url(
        self,
        client: HTTPClient,
        database: str,
        table: str,
        column_mapping: Dict[str, "ColumnMapping"],
        type_castings: List["ColumnTypeCasting"],
        quarantine_schema: List[Dict[str, Any]],
    ) -> CHSummary:
        target_columns, source_columns, source_conditions = build_import_quarantine_query_parts(
            column_mapping,
            type_castings,
            quarantine_schema,
            self.id,
        )
        query_id = str(uuid.uuid4())  # can't reuse the one from job
        query = f"INSERT INTO {database}.`{table}_quarantine` ({target_columns}) SELECT {source_columns} FROM url({ch_escape_string(self.url)}, Parquet) WHERE {source_conditions}"
        request_params = {
            "query_id": query_id,
            **self._parquet_import_url_query_settings(),
        }
        try:
            headers, _ = self._run_query(client=client, query=query, user_agent="tb-lfi", **request_params)
            ch_summary = CHSummary(query_id=query_id, summary=json.loads(headers.get("X-ClickHouse-Summary")))
            return ch_summary
        except CHException as e:
            raise Exception(f"Error inserting quarantine from url: {e}")

    def import_through_ch(
        self,
        workspace: Workspace,
        file_size_limit: int,
        format: str,
        json_deserialization: List[Dict[str, Any]],
        replace_hook: Optional["Hook"] = None,
        append_hook: Optional["Hook"] = None,
    ) -> Dict[str, Any]:
        assert workspace
        assert self.datasource

        # Work on it
        job_updated = self.mark_as_working()
        self.started_at = job_updated.started_at
        self.updated_at = job_updated.updated_at
        self.status = job_updated.status

        blocks = []
        block_id = None
        ch_summary: Optional[CHSummary] = None
        error: Optional[str] = None
        successful_rows = 0
        quarantine_rows = 0
        is_parquet_empty = False

        hook_options = {"source": self.url, "format": self.format}

        if append_hook:
            append_hook.ops_log_options = {**append_hook.ops_log_options, **hook_options}
            append_hook.before_append(self.datasource)

        try:
            with Timer() as timing:
                block_tracker = NDJSONBlockLogTracker(job_url=self.url)

                # Check for size limit
                file_size, head_available = SharedUtils.UrlUtils.check_file_size_limit(
                    self.url,
                    workspace,
                    file_size_limit,
                    self.datasource.id,
                    is_parquet=True,
                )
                self.parquet_stats = {
                    "file_bytes": file_size,
                }

                # We only get metadata if head method is available, because if not CH will download the entire file
                # It is not available for AWS S3 signed urls
                if head_available:
                    # Load some metadata, to later include it in the stats
                    ch_get_parquet_metadata_from_url_sync = async_to_sync(ch_get_parquet_metadata_from_url)
                    parquet_metadata: CHParquetMetadata = ch_get_parquet_metadata_from_url_sync(
                        self.url, 300, **self._parquet_internal_op_url_settings()
                    )
                    is_parquet_empty = parquet_metadata.num_rows == 0
                    self.parquet_stats.update(
                        {
                            "row_count": parquet_metadata.num_rows,
                            "column_count": parquet_metadata.num_columns,
                            "row_group_count": parquet_metadata.num_row_groups,
                            "uncompressed_bytes": parquet_metadata.total_uncompressed_size,
                        }
                    )

                if not is_parquet_empty:
                    # Check for compatible schema
                    assert self.datasource
                    url_schema = self._get_schema_from_describe_table(
                        format, 300, **self._parquet_internal_op_url_settings()
                    )
                    datasource_schema = ch_table_schema(
                        table_name=self.datasource.id,
                        database_server=self.database_server,
                        database=self.database,
                        include_default_columns=True,
                        include_meta_columns=True,
                    )
                    if not datasource_schema:
                        raise Exception("Error checking datasource schema compatibility")

                    column_mapping = build_column_mapping(json_deserialization, url_schema)
                    if len(column_mapping) == 0:
                        raise Exception(
                            "Schema mismatch: At least one Data Source column must point to a column in the source. Check the JSONPaths in the schema."
                        )
                block = block_tracker.on_fetching()
                block_id = block["block_id"]

                if not is_parquet_empty:
                    ch_http_client = HTTPClient(host=self.database_server, database=self.database)
                    assert datasource_schema
                    column_type_castings = get_column_type_castings(datasource_schema, column_mapping)
                    ch_summary = self._import_from_url(
                        client=ch_http_client,
                        database=self.database,
                        table=self.datasource.id,
                        column_mapping=column_mapping,
                        type_castings=column_type_castings,
                    )

                block_tracker.on_inserting_chunk(block_id=block_id)
                block_tracker.track_offset(block, file_size)

            successful_rows = int(ch_summary.summary["written_rows"]) if ch_summary else 0
            quarantine_ch_summary = None

            if (
                FeatureFlagsWorkspaceService.feature_for_id(
                    FeatureFlagWorkspaces.PARQUET_THROUGH_CLICKHOUSE_QUARANTINE, workspace.id, workspace.feature_flags
                )
                and not is_parquet_empty
                and len(column_type_castings)
            ):
                # successful rows include the ones in materialization so we can't know if we don't need quarantine
                quarantine_ch_summary = self._import_quarantine_from_url(
                    client=ch_http_client,
                    database=self.database,
                    table=self.datasource.id,
                    column_mapping=column_mapping,
                    type_castings=column_type_castings,
                    quarantine_schema=self._prepare_quarantine_table(),
                )
                quarantine_rows = int(quarantine_ch_summary.summary["written_rows"])

            block_tracker.on_done_inserting_chunk(
                block_id=block_id,
                total_rows=successful_rows + quarantine_rows,
                quarantine_rows=quarantine_rows,
                processing_time=timing.interval,
                ch_summaries=[ch_summary] if ch_summary else [],
                quarantine_ch_summaries=[quarantine_ch_summary] if quarantine_ch_summary and quarantine_rows else [],
                parser="clickhouse",
            )

            block_tracker.on_done(block_id)
            blocks = list(block_tracker.blocks.values())

            if quarantine_rows > 0:
                self.result = {
                    "error": f"{quarantine_rows} rows with errors were quarantined.",
                    "quarantine_rows": quarantine_rows,
                }

        except Exception as e:
            error = str(e)
            if isinstance(e, CHAnalyzeError) and ("Unsupported Parquet type" in str(e) or "Invalid URL" in str(e)):
                logging.warning("Error importing job through CH: %s", e)
            else:
                logging.exception("Error importing job through CH: %s", e)
            self.status = JobStatus.ERROR
            self.result = {"error": str(e)}
            if block_id is not None:
                if hasattr(e, "ch_summary") and e.ch_summary:
                    if ch_summary is None:
                        ch_summary = e.ch_summary
                        quarantine_ch_summary = None
                    else:
                        quarantine_ch_summary = e.ch_summary
                    successful_rows = int(ch_summary.summary["written_rows"]) if ch_summary else 0
                    quarantine_rows = int(quarantine_ch_summary.summary["written_rows"]) if quarantine_ch_summary else 0
                    block_tracker.on_error(
                        block_id,
                        error,
                        total_rows=successful_rows,
                        quarantine_rows=quarantine_rows,
                        processing_time=0,
                        ch_summaries=[ch_summary],
                        quarantine_ch_summaries=[quarantine_ch_summary]
                        if quarantine_ch_summary and quarantine_rows
                        else [],
                        parser="clickhouse",
                    )
                else:
                    block_tracker.on_error(block_id, error)
                block_tracker.on_done(block_id)
                blocks = list(block_tracker.blocks.values())

        if append_hook:
            append_hook.ops_log_options = {**append_hook.ops_log_options, **hook_options}
            if error:
                append_hook.on_error(self.datasource, error)
            else:
                append_hook.after_append(  # type: ignore [call-arg]
                    self.datasource,
                    appended_rows=successful_rows,
                    appended_rows_quarantine=quarantine_rows,
                    elapsed_time=0,
                )
        if replace_hook:
            replace_hook.ops_log_options = {**replace_hook.ops_log_options, **hook_options}
            if error:
                replace_hook.on_error(self.datasource, error)
            else:
                replace_hook.after_append(self.datasource)

        self.block_log = block_tracker.block_status_log
        self.save()

        import_result = {
            "blocks": blocks,
            "table": self.datasource.id,
            "time": timing.interval,
            "stats": {
                "bytes": int(ch_summary.summary["written_bytes"]) if ch_summary else 0,
                "row_count": successful_rows,
            },
            "track_datasource_ops": True,
        }
        import_result.update(self.result)

        return {"import_result": import_result}

    def _prepare_quarantine_table(self):
        assert self.datasource
        quarantine_schema = ch_table_schema(
            table_name=f"{self.datasource.id}_quarantine",
            database_server=self.database_server,
            database=self.database,
            include_default_columns=True,
            include_meta_columns=False,
        )
        if not quarantine_schema:
            # Quarantine table is missing, we should create it
            create_quarantine_table_from_landing_sync(
                landing_datasource_name=self.datasource.id,
                database_server=self.user.database_server,
                database=self.user.database,
                cluster=self.user.cluster,
            )

            quarantine_schema = ch_table_schema(
                table_name=f"{self.datasource.id}_quarantine",
                database_server=self.database_server,
                database=self.database,
                include_default_columns=True,
                include_meta_columns=False,
            )
        return quarantine_schema

    @staticmethod
    def import_parquet_ndjson_job(j: "ImportJob") -> Dict[str, Any]:
        async def parquet_ndjson_process_job(
            job: ImportJob,
            workspace: Workspace,
            file_size_limit: int,
            extended_json_deserialization: ExtendedJSONDeserialization,
            replace_hook: Optional["Hook"] = None,
            append_hook: Optional["Hook"] = None,
            block_tracker=None,
        ):
            assert job.user_id
            assert job.format
            assert job.datasource
            importer = NDJSONIngester(
                extended_json_deserialization,
                database_server=job.database_server,
                database=job.database,
                workspace_id=job.user_id,
                datasource_id=job.datasource.id,
                format=job.format,
                pusher="lfi",
                sample_iterations=20,
                import_id=job.request_id,
                block_tracker=block_tracker,
                max_import_size=file_size_limit,
                cluster=workspace.cluster,
            )
            job_updated = job.mark_as_working()
            job.started_at = job_updated.started_at
            job.updated_at = job_updated.updated_at
            job.status = job_updated.status

            options = {"source": job.url, "format": job.format}

            if append_hook:
                append_hook.ops_log_options = {**append_hook.ops_log_options, **options}
                append_hook.before_append(job.datasource)

            session = get_shared_session()

            async def f(retry_me):
                nonlocal options, append_hook, job, importer
                assert importer.block_tracker
                assert job.datasource
                try:
                    error = None
                    decompressor = None
                    block = None
                    first_chunk = True
                    async with session.get(job.url, allow_redirects=False) as resp:
                        if not resp.ok:
                            retry_me()
                            error = await resp.text()
                            logging.error(f"Error getting job {job.id} on {job.url}: {error}")
                            raise Exception(
                                f"There was a problem with job '{job.id}': '{job.url}' failed with status code {resp.status}."
                            )

                        file_size = int(resp.headers.get("content-length", 0))
                        get_url_file_size_checker(file_size_limit, workspace.plan, workspace.id, job.datasource.id)(
                            file_size
                        )

                        if (
                            "gzip" in resp.headers.get("Content-Encoding", "")
                            or "gzip" in resp.headers.get("Content-Type", "")
                            or is_gzip_file(job.url)
                        ):
                            decompressor = zlib.decompressobj(16 + zlib.MAX_WBITS)

                        import_start = time.time()
                        timeout = None
                        chunk_size = NDJSON_CHUNK_SIZE if not decompressor else NDJSON_CHUNK_SIZE_COMPRESSED

                        while True:
                            try:
                                block = importer.block_tracker.on_fetching()
                                chunk = await resp.content.readexactly(chunk_size)
                            except asyncio.IncompleteReadError as e:
                                chunk = e.partial
                                block = importer.block_tracker.on_incomplete_read()
                            except asyncio.TimeoutError:
                                # We only want to retry if we haven't processed anything
                                # Otherwise, some data could have reached CH, and we would
                                # be duplicating data without informing the user of the issue
                                if first_chunk:
                                    retry_me()
                                timeout = f"{time.time() - import_start}s"
                                logging.exception(
                                    f"Timeout after {timeout} reading a chunk of size {chunk_size} bytes "
                                    f"for job {job.id} and URL {job.url}. First chunk = {first_chunk}\n"
                                    f"Traceback: {traceback.format_exc()}"
                                )
                                break

                            if not chunk:
                                break
                            if decompressor:
                                importer.block_tracker.on_decompressing()
                                chunk = decompressor.decompress(chunk)

                                # If the file is formed concatenating several gzipped files
                                # the decompressor stops to decompress when it find \x1f\x8b
                                # setting eof=true and unused_data=the rest of the data.
                                # To fix this, we create a new decompressor
                                while decompressor.eof and decompressor.unused_data:
                                    unused_data = decompressor.unused_data
                                    decompressor = zlib.decompressobj(16 + zlib.MAX_WBITS)
                                    chunk_tmp = decompressor.decompress(unused_data)
                                    chunk = chunk + chunk_tmp

                                # calc compressed chunk size to get NDJSON_CHUNK_SIZE uncompressed
                                # using the compression ratio
                                if first_chunk and len(chunk) > 0:
                                    chunk_size = int(NDJSON_CHUNK_SIZE_COMPRESSED * NDJSON_CHUNK_SIZE / len(chunk))
                            importer.write(chunk)
                            await importer.work(block)
                            first_chunk = False
                        if not timeout:
                            if decompressor:
                                chunk = decompressor.flush()
                                importer.write(chunk)
                            await importer.finish(block)
                    job.status = JobStatus.DONE if not timeout and importer.quarantined_rows == 0 else JobStatus.ERROR
                    if timeout:
                        error = f"Timeout after {timeout} reading a chunk. First chunk = {first_chunk}. url={job.url} id={job.id}"
                        job.result = {
                            "error": error,
                            "quarantine_rows": importer.quarantined_rows,
                        }
                    elif importer.quarantined_rows > 0:
                        job.result = {
                            "error": f"{importer.quarantined_rows} rows with errors were quarantined.",
                            "quarantine_rows": importer.quarantined_rows,
                        }
                    else:
                        job.result = {
                            "quarantine_rows": importer.quarantined_rows,
                        }

                except aiohttp.InvalidURL as e:
                    error = f"InvalidURL: {str(e)} url={job.url} id={job.id}"
                    job.status = JobStatus.ERROR
                    job.result = {"error": error}
                    block_id = block["block_id"] if block else None
                    importer.block_tracker.on_error(block_id, e)
                    importer.block_tracker.on_done(block_id)
                except (asyncio.exceptions.TimeoutError, aiohttp.ServerTimeoutError) as e:
                    if first_chunk:
                        retry_me()
                    error = f"Timeout: url={job.url} id={job.id}"
                    job.status = JobStatus.ERROR
                    job.result = {"error": error}
                    block_id = block["block_id"] if block else None
                    importer.block_tracker.on_error(block_id, e)
                    importer.block_tracker.on_done(block_id)
                except FileSizeException as e:
                    error = f"NDJSON/Parquet import error: {e} url={job.url} id={job.id}"
                    job.status = JobStatus.ERROR
                    job.result = {"error": error}
                    block_id = block["block_id"] if block else None
                    importer.block_tracker.on_error(block_id, e)
                    importer.block_tracker.on_done(block_id)
                except (PushError, Exception) as e:
                    error = f"NDJSON/Parquet import unhandled exception while streaming: {e} url={job.url} id={job.id}"
                    logging.exception(f"{error}\nTraceback: {traceback.format_exc()}")
                    job.status = JobStatus.ERROR
                    job.result = {"error": error}
                    block_id = block["block_id"] if block else None
                    if isinstance(e, PushError):
                        ch_summaries = e.ch_summaries
                        quarantine_ch_summaries = e.ch_summaries_quarantine
                        successful_rows = sum([int(stat.summary.get("written_rows", 0)) for stat in ch_summaries])
                        quarantine_rows = sum(
                            [int(stat.summary.get("written_rows", 0)) for stat in quarantine_ch_summaries]
                        )
                        importer.block_tracker.on_error(
                            block_id,
                            e,
                            total_rows=successful_rows,
                            quarantine_rows=quarantine_rows,
                            processing_time=0,
                            ch_summaries=ch_summaries,
                            quarantine_ch_summaries=quarantine_ch_summaries,
                        )
                    else:
                        importer.block_tracker.on_error(block_id, e)
                    importer.block_tracker.on_done(block_id)
                job.save()
                if append_hook:
                    append_hook.ops_log_options = {**append_hook.ops_log_options, **options}
                    if error:
                        append_hook.on_error(job.datasource, error)
                    else:
                        after_append = sync_to_async(append_hook.after_append)
                        await after_append(
                            job.datasource,
                            appended_rows=importer.successful_rows,
                            appended_rows_quarantine=importer.quarantined_rows,
                            elapsed_time=0,
                        )
                if replace_hook:
                    replace_hook.ops_log_options = {**replace_hook.ops_log_options, **options}
                    if error:
                        replace_hook.on_error(job.datasource, error)
                    else:
                        after_append = sync_to_async(replace_hook.after_append)
                        await after_append(job.datasource)

            with Timer() as timing:
                await retry_ondemand_async(f, backoff_policy=[1, 2, 4])
            if importer.block_tracker and hasattr(importer.block_tracker, "block_status_log"):
                block_status_log = importer.block_tracker.block_status_log
            else:
                block_status_log = []
            job.block_log = block_status_log
            table_name = job.datasource.id
            stats = {
                "bytes": importer.ch_written_bytes,
                "row_count": importer.ch_written_rows,
            }

            if importer.block_tracker and hasattr(importer.block_tracker, "blocks"):
                blocks = list(importer.block_tracker.blocks.values())
            else:
                blocks = []

            import_result = {"blocks": blocks, "table": table_name, "time": timing.interval, "stats": stats}
            import_result.update(job.result)
            return {"import_result": import_result}

        assert j.datasource
        assert j.user_id
        assert j.format
        workspace = Workspace.get_by_id(j.user_id)
        assert workspace

        replace_hook = ImportJob.get_replace_hook(j.datasource)
        append_hook = ImportJob.get_append_hook(j.datasource)
        file_size_limit = ImportJob.get_max_file_size_limit(workspace, j.format)

        if j.datasource is not None and hasattr(j.datasource, "json_deserialization"):
            extended_json_deserialization = extend_json_deserialization(j.datasource.json_deserialization)
        else:
            j.result = {"error": "Datasource doesn't have json_deserialization attribute"}
            j.save()
            return {"import_result": j.result}

        if j.format == "parquet" and FeatureFlagsWorkspaceService.feature_for_id(
            FeatureFlagWorkspaces.PARQUET_THROUGH_CLICKHOUSE, workspace.id, workspace.feature_flags
        ):
            r = j.import_through_ch(
                workspace=workspace,
                file_size_limit=file_size_limit,
                format=j.format,
                json_deserialization=j.datasource.json_deserialization,
                replace_hook=replace_hook,
                append_hook=append_hook,
            )
        else:
            import_ndjson_parquet_sync = async_to_sync(parquet_ndjson_process_job)
            r = import_ndjson_parquet_sync(
                job=j,
                workspace=workspace,
                file_size_limit=file_size_limit,
                extended_json_deserialization=extended_json_deserialization,
                replace_hook=replace_hook,
                append_hook=append_hook,
                block_tracker=NDJSONBlockLogTracker(j.url),
            )

        return r

    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def update_url(self, url) -> None:
        with ImportJob.transaction(self.id) as j:
            j.url = url


class JobCancelledException(Exception):
    pass


def new_import_job(
    job_executor: JobExecutor,
    url: str,
    headers: Dict[str, str],
    user: Workspace,
    datasource: Datasource,
    request_id: str,
    dialect_overrides: Dict[str, Any],
    type_guessing: bool = True,
    mode: str = "create",
    job_id: Optional[str] = None,
    replace_condition: Optional[str] = None,
    format: Optional[str] = None,
) -> ImportJob:
    j = Job.create_import(
        workspace=user,
        datasource=datasource,
        url=url,
        headers=headers,
        request_id=request_id,
        dialect_overrides=dialect_overrides,
        type_guessing=type_guessing,
        mode=mode,
        job_id=job_id,
        replace_condition=replace_condition,
        format=format,
    )
    logging.info(f"New import job created: job_id={j.id}, user={user.id}, datasource={datasource.id}, url={url}")
    job_executor.put_job(j)
    j.send_raw_event()
    return j


def new_delete_job(
    job_executor: JobExecutor,
    delete_condition: str,
    headers: Dict[str, str],
    workspace: Workspace,
    datasource: Datasource,
    request_id: str,
) -> DeleteJob:
    j = Job.create_delete(
        workspace=workspace,
        datasource=datasource,
        delete_condition=delete_condition,
        headers=headers,
        request_id=request_id,
    )
    logging.info(
        f"New delete job created: job_id={j.id}, user={workspace.id}, datasource={datasource.id}, delete_condition={delete_condition}"
    )
    job_executor.put_job(j)
    j.send_raw_event()
    return j


async def cancel_job(api_host, cancelled_jobs, job, job_executor, not_cancelled_jobs, pipe):
    job.set_job_executor(job_executor)
    if job.pipe_id is not None and job.pipe_id == pipe.id:
        if job.is_cancellable:
            job.try_to_cancel()
            if job.status == JobStatus.CANCELLED or JobStatus.CANCELLING:
                job = Job.get_by_id(job.id)
                cancelled_jobs.append(job.to_public_json(job, api_host=api_host))
        # check in case user tries to cancel more than once
        elif job.status == JobStatus.CANCELLING:
            logging.info("Job already being cancelled")
            cancelled_jobs.append(job.to_public_json(job, api_host=api_host))
        else:
            logging.info("Job not in cancellable status")
            not_cancelled_jobs.append(job.to_public_json(job, api_host))


def filter_jobs(workspace_jobs: List["Job"], filters: Dict[str, str | Any]):
    """
    Filter job results based on status, kind, pipe_id, pipe_name, created_before and created_after params

    >>> user = Workspace()
    >>> user.save()
    >>> test_job_1 = Job(user=user, job_id="1f6a5a3d-cfcb-4244-ba0b-0bfa1d1752fb", kind="import", datasource=Datasource("t_49806938714f4b72a225599cdee6d3ab", "my_datasource_2"))
    >>> test_job_1.status = "done"
    >>> test_job_1.created_at = datetime.fromisoformat("2020-12-20 15:08:09.051310")
    >>> test_job_1.updated_at = datetime.fromisoformat("2020-12-20 15:08:09.051310")
    >>> jobs: List['Job'] = []
    >>> jobs.append(test_job_1)
    >>> test_job_2 = Job(user=user, job_id="1f6a5a3d-cfcb-4244-ba0b-0bfa1d1752fb", kind="populate", datasource=Datasource("t_49806938714f4b72a225599cdee6d3ab", "my_datasource_2"))
    >>> test_job_2.status = "done"
    >>> test_job_2.created_at = datetime.fromisoformat("2020-12-01 15:08:09.051310")
    >>> test_job_2.updated_at = datetime.fromisoformat("2020-12-01 15:08:09.051310")
    >>> jobs.append(test_job_2)
    >>> test_job_3 = Job(user=user, job_id="1f6a5a3d-cfcb-4244-ba0b-0bfa1d1752fb", kind="copy", datasource=Datasource("t_49806938714f4b72a225599cdee6d3ab", "my_datasource_2"))
    >>> test_job_3.status = "done"
    >>> test_job_3.created_at = datetime.fromisoformat("2020-12-12 15:08:09.051310")
    >>> test_job_3.updated_at = datetime.fromisoformat("2020-12-12 15:08:09.051310")
    >>> jobs.append(test_job_3)
    >>> filtered = filter_jobs(jobs, {"kind": None, "created_before": "2020-12-10 15:08:09.051310", "created_after": None, "pipe_name": None, "pipe_id": None, "status": None})
    >>> len(filtered)
    1
    >>> filtered[0].kind
    'populate'
    >>> filtered[0].status
    'done'
    >>> filtered = filter_jobs(jobs, {"kind": "populate", "status": "done", "created_before": None, "created_after": None, "pipe_name": None, "pipe_id": None})
    >>> len(filtered)
    1
    >>> filtered[0].kind
    'populate'
    >>> filtered[0].status
    'done'
    >>> filtered = filter_jobs(jobs, {"kind": None, "created_after": "2020-12-10 15:08:09.051310", "created_before": None, "pipe_name": None, "pipe_id": None, "status": None})
    >>> len(filtered)
    2
    >>> filtered[0].kind
    'import'
    >>> filtered[1].kind
    'copy'
    >>> filtered[0].status
    'done'
    >>> filtered[1].status
    'done'
    >>> filtered = filter_jobs(jobs, {"kind": None, "created_after": "2020-12-01T10:13:25.855Z", "created_before": "2020-12-21T15:13:25.855Z", "pipe_name": None, "pipe_id": None, "status": None})
    >>> len(filtered)
    3
    >>> filtered[0].kind
    'import'
    >>> filtered[1].kind
    'populate'
    >>> filtered[2].kind
    'copy'
    >>> filtered[0].status
    'done'
    >>> filtered[1].status
    'done'
    >>> filtered[2].status
    'done'
    """

    kind = filters.get("kind", None)
    status = filters.get("status", None)
    created_after = filters.get("created_after", None)
    created_before = filters.get("created_before", None)
    created_after_date = None
    created_before_date = None
    if created_after:
        created_after_date = datetime.fromisoformat(created_after)
    if created_before:
        created_before_date = datetime.fromisoformat(created_before)
    pipe_id = filters.get("pipe_id", None)
    pipe_name = filters.get("pipe_name", None)

    filter_items = [
        {"field": "kind", "value": kind},
        {"field": "status", "value": status},
        {"field": "pipe_id", "value": pipe_id},
        {"field": "pipe_name", "value": pipe_name},
    ]

    filters_with_values = [filter_item for filter_item in filter_items if filter_item.get("value") is not None]

    def is_job_matching_parameters(job: Job, filters_items: List[dict[str, str]]):
        matching_filters = [
            filter_item
            for filter_item in filters_items
            if hasattr(job, filter_item["field"]) and getattr(job, filter_item["field"]) == filter_item["value"]
        ]
        if len(matching_filters) != len(filters_items):
            return False

        if created_before_date and job.created_at.timestamp() > created_before_date.timestamp():
            return False

        if created_after_date and job.created_at.timestamp() < created_after_date.timestamp():
            return False

        return True

    filtered_jobs = [job for job in workspace_jobs if is_job_matching_parameters(job, filters_with_values)]
    return filtered_jobs


# Raw Events Transformations


def convert_importjob_to_rawevent(import_job: "ImportJob") -> RawEvent:
    errors, quarantine_rows, invalid_lines = get_errors(import_job.result.get("blocks", []))
    error = None

    parser = None
    for block in import_job.result.get("blocks", []):
        if block.get("process_return", None):
            parser = block["process_return"][0].get("parser", parser)

    # This is meant for jobs that do not have import blocks
    job_error = import_job.result.get(JobStatus.ERROR, None)
    if job_error:
        errors.insert(0, job_error)

    if (import_job.status == JobStatus.ERROR and errors) or invalid_lines > 0 or quarantine_rows > 0:
        error = build_error_summary(errors, quarantine_rows, invalid_lines)

    metadata_options = {
        "mode": import_job.mode,
        "url": import_job.url,
        "statistics": import_job.stats if import_job.stats else {},
        "replace_condition": import_job.replace_condition if import_job.replace_condition else "",
        "errors": errors,
        "quarantine_rows": quarantine_rows,
        "invalid_lines": invalid_lines,
        "other_datasources_to_replace": (
            import_job.other_datasources_to_replace if import_job.other_datasources_to_replace else {}
        ),
        "format": import_job.format,
        "parser": parser,
    }

    metadata = (
        ParquetImportJobMetadata.model_validate({**metadata_options, "parquet_statistics": import_job.parquet_stats})
        if import_job.parquet_stats is not None
        else ImportJobMetadata.model_validate(metadata_options)
    )

    workspace = Workspace.get_by_id(import_job.user_id) if import_job.user_id else None
    datasource_json = import_job.datasource_to_json(workspace=workspace)

    import_job_log = ImportJobLog(
        job_id=import_job.id,
        job_type="import",
        status=JobStatusForLog(import_job.status),
        error=error,
        pipe_id=None,
        datasource_id=datasource_json["id"] if datasource_json else None,
        created_at=import_job.created_at,
        started_at=import_job.started_at,
        updated_at=import_job.updated_at,
        job_metadata=metadata,
    )

    return RawEvent(
        timestamp=datetime.now(timezone.utc),
        workspace_id=import_job.user_id if import_job.user_id else "",
        request_id=import_job.request_id,
        event_type=EventType.IMPORT,
        event_data=import_job_log,
    )


def convert_deletejob_to_rawevent(delete_job: "DeleteJob") -> RawEvent:
    job_error = (
        delete_job.result["error"] if delete_job.status == JobStatus.ERROR and "error" in delete_job.result else None
    )

    delete_job_log = DeleteJobLog(
        job_id=delete_job.id,
        job_type="delete",
        status=JobStatusForLog(delete_job.status),
        error=job_error,
        pipe_id=None,
        datasource_id=delete_job.datasource.id if delete_job.datasource else None,
        created_at=delete_job.created_at,
        started_at=delete_job.started_at,
        updated_at=delete_job.updated_at,
        job_metadata=DeleteJobMetadata(delete_condition=delete_job.delete_condition),
    )

    return RawEvent(
        timestamp=datetime.utcnow(),
        workspace_id=delete_job.user_id if delete_job.user_id else "",
        request_id=delete_job.request_id,
        event_type=EventType.DELETE,
        event_data=delete_job_log,
    )


@dataclass
class ColumnMapping:
    target: str
    source: str
    source_table_column: TableColumn


@dataclass
class StaticColumnMapping:
    target: str
    value: str | int
    source_table_column: TableColumn
    wrap_in_quotes: bool = True

    @property
    def source(self) -> str:
        return f"'{self.value}'" if self.wrap_in_quotes else f"{self.value}"


def build_column_mapping(
    json_deserialization: List[Dict[str, Any]], source_schema: DescribeTable
) -> Dict[str, ColumnMapping]:
    """
    >>> source_schema=DescribeTable(columns={'bar': TableColumn(name="bar", type="String"), 'foobar': TableColumn(name="foobar", type="String")})
    >>> json_deserialization=[{"name": "foo", "jsonpath": "$.bar"}]
    >>> build_column_mapping(json_deserialization, source_schema)
    {'foo': ColumnMapping(target='foo', source='`bar`', source_table_column=TableColumn(name='bar', type='String', is_subcolumn=False))}
    >>> source_schema=DescribeTable(columns={'foo': TableColumn(name="foo", type="String"), 'foobar': TableColumn(name="foobar", type="String")})
    >>> build_column_mapping(json_deserialization, source_schema)
    {}
    >>> json_deserialization=[{"name": "foobar", "jsonpath": "$.foo.bar"}]
    >>> build_column_mapping(json_deserialization, source_schema)
    {}
    >>> source_schema=DescribeTable(columns={'list': TableColumn(name="list", type="Array(String)")})
    >>> json_deserialization=[{"name": "list", "jsonpath": "$.list[:]"}]
    >>> build_column_mapping(json_deserialization, source_schema)
    {'list': ColumnMapping(target='list', source='arrayMap(x -> x, `list`)', source_table_column=TableColumn(name='list', type='Array(String)', is_subcolumn=False))}
    >>> source_schema=DescribeTable(columns={'foo': TableColumn(name="foo", type="Tuple(bar String, bar2 String)"), 'foo.bar': TableColumn(name="foo.bar", type="String", is_subcolumn=True), 'foo.bar2': TableColumn(name="foo.bar2", type="String", is_subcolumn=True)})
    >>> json_deserialization=[{"name": "c", "jsonpath": "$.foo.bar"}]
    >>> build_column_mapping(json_deserialization, source_schema)
    {'c': ColumnMapping(target='c', source="tupleElement(`foo`, 'bar')", source_table_column=TableColumn(name='foo.bar', type='String', is_subcolumn=True))}
    >>> json_deserialization=[{"name": "c", "jsonpath": "$.foo.baro"}]
    >>> build_column_mapping(json_deserialization, source_schema)
    {}
    >>> source_schema=DescribeTable(columns={'m': TableColumn(name="m", type="Map(String, Map(String, Map(String, String)))"), 'm.keys': TableColumn(name="m.keys", type="Array(String)", is_subcolumn=True), 'm.values': TableColumn(name="m.values", type="Array(Map(String, Map(String, String)))", is_subcolumn=True), 'm.values.keys': TableColumn(name="m.values.keys", type="Array(Array(String))", is_subcolumn=True), 'm.values.values': TableColumn(name="m.values.values", type="Array(Array(Map(String, String)))", is_subcolumn=True)})
    >>> json_deserialization=[{"name": "c", "jsonpath": "$.m.key1"}]
    >>> build_column_mapping(json_deserialization, source_schema)
    {'c': ColumnMapping(target='c', source="`m`['key1']", source_table_column=TableColumn(name='m.values', type='Array(Map(String, Map(String, String)))', is_subcolumn=True))}
    """
    mapping = {}
    for dest_column in json_deserialization:
        dest_column_name = dest_column["name"]
        column_path = get_path(dest_column["jsonpath"])

        source_column = source_schema.column_from_jsonpath(column_path)

        if source_column:
            mapping[dest_column_name] = ColumnMapping(
                target=dest_column_name, source=source_column[1], source_table_column=source_column[0]
            )

    return mapping


@dataclass
class ColumnTypeCasting:
    target_column: str
    source_column: str
    target_type: str
    source_type: str


def get_column_type_castings(
    target_schema: List[Dict[str, Any]], column_mapping: Mapping[str, ColumnMapping | StaticColumnMapping]
) -> List[ColumnTypeCasting]:
    """
    >>> target_schema=[{"normalized_name": "id", "type": "Int8"}, {"normalized_name": "name", "type": "String"}, {"normalized_name": "val", "type": "Float32"}]
    >>> column_mapping={"id": ColumnMapping(target='id', source='`user_id`', source_table_column=TableColumn(name='user_id', type='Int16')), "name": ColumnMapping(target='name', source='`user_name`', source_table_column=TableColumn(name='user_name', type='String')), "val": ColumnMapping(target='val', source='`val`', source_table_column=TableColumn(name='vale', type='Float64'))}
    >>> get_column_type_castings(target_schema, column_mapping)
    [ColumnTypeCasting(target_column='id', source_column='`user_id`', target_type='Int8', source_type='Int16')]
    >>> target_schema=[{"normalized_name": "val", "type": "Array(String)"}]
    >>> column_mapping={"val": ColumnMapping(target='val', source='`val`', source_table_column=TableColumn(name='val', type='String'))}
    >>> get_column_type_castings(target_schema, column_mapping)
    []
    >>> target_schema=[{"normalized_name": "id", "type": "LowCardinality(Int8)"}, {"normalized_name": "name", "type": "LowCardinality(String)"}, {"normalized_name": "val", "type": "Float32"}]
    >>> column_mapping={"id": ColumnMapping(target='id', source='`user_id`', source_table_column=TableColumn(name='user_id', type='Int16')), "name": ColumnMapping(target='name', source='`user_name`', source_table_column=TableColumn(name='user_name', type='String')), "val": ColumnMapping(target='val', source='`val`', source_table_column=TableColumn(name='vale', type='Float64'))}
    >>> get_column_type_castings(target_schema, column_mapping)
    [ColumnTypeCasting(target_column='id', source_column='`user_id`', target_type='Int8', source_type='Int16')]
    >>> target_schema=[{"normalized_name": "c", "type": "Int8"}]
    >>> column_mapping={"c": ColumnMapping(target='c', source="tupleElement(`m`, 'x')", source_table_column=TableColumn(name='m.x', type='String', is_subcolumn=True))}
    >>> get_column_type_castings(target_schema, column_mapping)
    [ColumnTypeCasting(target_column='c', source_column="tupleElement(`m`, 'x')", target_type='Int8', source_type='String')]
    >>> target_schema=[{"normalized_name": "id", "type": "LowCardinality(Int8)"}, {"normalized_name": "name", "type": "LowCardinality(Nullable(String))"}, {"normalized_name": "val", "type": "Float32"}]
    >>> column_mapping={"id": ColumnMapping(target='id', source='`user_id`', source_table_column=TableColumn(name='user_id', type='Int16')), "name": ColumnMapping(target='name', source='`user_name`', source_table_column=TableColumn(name='user_name', type='Nullable(String)')), "val": ColumnMapping(target='val', source='`val`', source_table_column=TableColumn(name='vale', type='Float64'))}
    >>> get_column_type_castings(target_schema, column_mapping)
    [ColumnTypeCasting(target_column='id', source_column='`user_id`', target_type='Int8', source_type='Int16')]

    """
    target_types = {column["normalized_name"]: column["type"] for column in target_schema}

    type_castings = []
    for target_column_name, column_map in column_mapping.items():
        target_type = target_types[target_column_name]
        source_type = column_map.source_table_column.type
        if target_type != source_type:
            if (target_type.startswith("Float") or target_type.startswith("Nullable(Float")) and (
                source_type.startswith("Float") or source_type.startswith("Nullable(Float")
            ):
                # We allow losing precision when casting a float to another float type
                continue

            if target_type.startswith("Array"):
                # accurateCastOrNull over arrays is not possible, since CH forbids Nullable(Array).
                # accurateCastOrDefault is also affected https://github.com/ClickHouse/ClickHouse/issues/61982
                continue

            if target_type.startswith("LowCardinality"):
                # Only cast if LowCardinality T is different

                target_type = target_type.removeprefix("LowCardinality(").removesuffix(")")

                if target_type == source_type:
                    continue

            type_casting = ColumnTypeCasting(
                source_column=column_map.source,
                target_column=target_column_name,
                target_type=target_type,
                source_type=source_type,
            )
            type_castings.append(type_casting)
    return type_castings


def build_import_query_parts(
    column_mapping: Mapping[str, ColumnMapping | StaticColumnMapping], type_castings: List[ColumnTypeCasting]
):
    """
    >>> column_mapping={"id": ColumnMapping(target='id', source='`user_id`', source_table_column=TableColumn(name='user_id', type='Int16'))}
    >>> type_castings=[]
    >>> build_import_query_parts(column_mapping, type_castings)
    ('`id`', '`user_id`', '1 = 1')
    >>> column_mapping={"id": ColumnMapping(target='id', source='`user_id`', source_table_column=TableColumn(name='user_id', type='Int16')), "name": ColumnMapping(target='name', source='`user_name`', source_table_column=TableColumn(name='user_name', type='String'))}
    >>> type_castings=[(ColumnTypeCasting(source_column='`user_id`', target_column='id', target_type='Int64', source_type='String'))]
    >>> build_import_query_parts(column_mapping, type_castings)
    ('`id`, `name`', "accurateCastOrNull(`user_id`, 'Int64'), `user_name`", "1 = 1 AND (`user_id` IS NULL OR accurateCastOrNull(`user_id`, 'Int64') IS NOT NULL)")
    """

    type_castings_map = {x.target_column: x for x in type_castings}
    target_column_names = []
    source_selectors = []
    for target_column_name, column_map in column_mapping.items():
        target_column_names.append(safe_sql_column(target_column_name))
        type_casting = type_castings_map.get(target_column_name, None)
        if type_casting is None:
            source_selectors.append(column_map.source)
        else:
            source_selectors.append(
                f"accurateCastOrNull({column_map.source}, {ch_escape_string(type_casting.target_type)})"
            )

    return ", ".join(target_column_names), ", ".join(source_selectors), build_type_casting_condition(type_castings)


def build_import_quarantine_query_parts(
    column_mapping: Dict[str, ColumnMapping],
    type_castings: List[ColumnTypeCasting],
    quarantine_schema: List[Dict[str, Any]],
    import_id: str,
):
    """
    >>> column_mapping={"id": ColumnMapping(target='id', source='`user_id`', source_table_column=TableColumn(name='user_id', type='Int16')), "name": ColumnMapping(target='name', source='`user_name`', source_table_column=TableColumn(name='user_name', type='String')), "age": ColumnMapping(target='age', source='`age`', source_table_column=TableColumn(name='age', type='Int64'))}
    >>> type_castings=[(ColumnTypeCasting(source_column='`user_id`', target_column='id', target_type='Int64', source_type='String'))]
    >>> quarantine_schema=[{"normalized_name": "c__error"}, {"normalized_name": "c__error_column"}, {"normalized_name": "c__import_id"}, {"normalized_name": "id"}, {"normalized_name": "age"}]
    >>> import_id = 'abcd'
    >>> build_import_quarantine_query_parts(column_mapping, type_castings, quarantine_schema, 'abcd')
    ('`c__error`, `c__error_column`, `c__import_id`, `id`, `age`', "arrayFilter(x -> not isNull(x), array(IF((`user_id` IS NULL OR accurateCastOrNull(`user_id`, 'Int64') IS NOT NULL), null, 'Failed to convert source column \\\\'user_id\\\\' from String to Int64'))), arrayFilter(x -> not isNull(x), array(IF((`user_id` IS NULL OR accurateCastOrNull(`user_id`, 'Int64') IS NOT NULL), null, 'id'))), 'abcd', `user_id`, `age`", "NOT (1 = 1 AND (`user_id` IS NULL OR accurateCastOrNull(`user_id`, 'Int64') IS NOT NULL))")
    >>> column_mapping={"col": ColumnMapping(target='col', source="tupleElement(`m`, 'x')", source_table_column=TableColumn(name='m.x', type='String', is_subcolumn=True))}
    >>> type_castings=[ColumnTypeCasting(target_column='col', source_column="tupleElement(`m`, 'x')", target_type='Int8', source_type='String')]
    >>> quarantine_schema=[{"normalized_name": "c__error"}, {"normalized_name": "c__error_column"}, {"normalized_name": "c__import_id"}, {"normalized_name": "col"}]
    >>> build_import_quarantine_query_parts(column_mapping, type_castings, quarantine_schema, 'abcd')
    ('`c__error`, `c__error_column`, `c__import_id`, `col`', "arrayFilter(x -> not isNull(x), array(IF((tupleElement(`m`, 'x') IS NULL OR accurateCastOrNull(tupleElement(`m`, 'x'), 'Int8') IS NOT NULL), null, 'Failed to convert source column \\\\'m.x\\\\' from String to Int8'))), arrayFilter(x -> not isNull(x), array(IF((tupleElement(`m`, 'x') IS NULL OR accurateCastOrNull(tupleElement(`m`, 'x'), 'Int8') IS NOT NULL), null, 'col'))), 'abcd', tupleElement(`m`, 'x')", "NOT (1 = 1 AND (tupleElement(`m`, 'x') IS NULL OR accurateCastOrNull(tupleElement(`m`, 'x'), 'Int8') IS NOT NULL))")
    """
    if len(type_castings) == 0:
        raise Exception("Attempted to import rows to quarantine, but original import should have worked.")

    error_column_array_items = []
    error_array_items = []

    for type_casting in type_castings:
        type_casting_condition = build_single_type_casting_condition(type_casting)
        source_path = (
            column_mapping[type_casting.target_column].source_table_column.name
            if type_casting.target_column in column_mapping
            else type_casting.source_column
        )
        error_message = f"Failed to convert source column '{source_path}' from {type_casting.source_type} to {type_casting.target_type}"
        error_array_items.append(f"IF({type_casting_condition}, null, {ch_escape_string(error_message)})")
        error_column_array_items.append(
            f"IF({type_casting_condition}, null, {ch_escape_string(type_casting.target_column)})"
        )

    # Fill data for all fields, then exclude the ones not in the schema
    column_values = {
        "c__import_id": ch_escape_string(import_id),
        "c__error_column": f"arrayFilter(x -> not isNull(x), array({','.join(error_column_array_items)}))",
        "c__error": f"arrayFilter(x -> not isNull(x), array({','.join(error_array_items)}))",
    }

    for target_column_name, column_map in column_mapping.items():
        column_values[target_column_name] = column_map.source

    target_column_names = []
    source_selectors = []
    for quarantine_column in quarantine_schema:
        quarantine_column_name = quarantine_column["normalized_name"]
        if quarantine_column_name not in column_values:
            continue
        target_column_names.append(safe_sql_column(quarantine_column_name))
        source_selectors.append(column_values[quarantine_column_name])

    condition = f"NOT ({build_type_casting_condition(type_castings)})"
    return ", ".join(target_column_names), ", ".join(source_selectors), condition


def build_type_casting_condition(type_castings: List[ColumnTypeCasting]):
    """
    >>> type_castings=[]
    >>> build_type_casting_condition(type_castings)
    '1 = 1'
    >>> type_castings.append(ColumnTypeCasting(source_column='`id`', target_column='user_id', target_type='Int64', source_type='String'))
    >>> type_castings.append(ColumnTypeCasting(source_column='`age`', target_column='age', target_type='Int8', source_type='Int16'))
    >>> build_type_casting_condition(type_castings)
    "1 = 1 AND (`id` IS NULL OR accurateCastOrNull(`id`, 'Int64') IS NOT NULL) AND (`age` IS NULL OR accurateCastOrNull(`age`, 'Int8') IS NOT NULL)"
    """
    conditions = ["1 = 1"]
    for type_casting in type_castings:
        conditions.append(build_single_type_casting_condition(type_casting))
    return " AND ".join(conditions)


def build_single_type_casting_condition(type_casting: ColumnTypeCasting):
    """
    >>> type_casting = ColumnTypeCasting(source_column='`id`', target_column='user_id', target_type='Int64', source_type='String')
    >>> build_single_type_casting_condition(type_casting)
    "(`id` IS NULL OR accurateCastOrNull(`id`, 'Int64') IS NOT NULL)"
    """
    return f"({type_casting.source_column} IS NULL OR accurateCastOrNull({type_casting.source_column}, {ch_escape_string(type_casting.target_type)}) IS NOT NULL)"
