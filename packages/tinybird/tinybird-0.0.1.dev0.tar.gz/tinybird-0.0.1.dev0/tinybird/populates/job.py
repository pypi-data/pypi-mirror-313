import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union, cast

import orjson
import ulid

import tinybird.views.shared.utils as SharedUtils
from tinybird import tracker
from tinybird.ch import (
    CHTableLocation,
    HTTPClient,
    StepCollector,
    ch_create_null_table_with_mv_for_mv_populate,
    ch_create_null_table_with_mv_for_mv_populate_with_fetch,
    ch_create_temporary_databases_sync,
    ch_describe_query_sync,
    ch_drop_database_sync,
    ch_drop_table_sync,
    ch_explain_plan_query,
    ch_get_columns_from_left_table_used_in_query_sync,
    ch_get_replica_load,
    ch_get_replicas_for_table_sync,
    ch_guarded_query,
    ch_move_partitions_to_disk_sync,
    ch_row_count_sync,
    ch_source_table_for_view,
    ch_source_table_for_view_sync,
    ch_table_details,
    ch_table_partitions_for_sample_sync,
    ch_table_partitions_sync,
    ch_truncate_databases_sync,
    ch_truncate_table_with_fallback,
    create_user_tables_on_pool_replica,
    table_stats,
    url_from_host,
    wait_for_database_replication,
)
from tinybird.ch_utils.engine import TableDetails, ttl_condition_from_engine_full
from tinybird.ch_utils.exceptions import CHException
from tinybird.cluster import (
    CannotFindOptimalReplica,
    CannotFindRandomReplica,
    get_optimal_replica_based_on_load,
    get_random_clickhouse_replica,
)
from tinybird.constants import MATVIEW_BACKFILL_VALUE_WAIT
from tinybird.dataflow import DataFlow
from tinybird.feature_flags import FeatureFlagsWorkspaceService, FeatureFlagWorkspaces
from tinybird.job import Job, JobCancelledException, JobExecutor, JobKind, JobStatus
from tinybird.limits import Limit
from tinybird.model import (
    retry_job_transaction_in_case_of_error_sync,
    retry_transaction_in_case_of_concurrent_edition_error_sync,
)
from tinybird.populates.cluster import (
    get_clickhouse_replicas_for_populates,
    get_clickhouse_settings_for_populates,
    get_dynamic_disk_settings_for_populates,
    get_pool_cluster_name,
    get_pool_replicas,
)
from tinybird.raw_events.definitions.base import JobStatus as JobStatusForLog
from tinybird.raw_events.definitions.populate_log import PopulateJobLog, PopulateJobMetadata
from tinybird.raw_events.raw_events_batcher import EventType, RawEvent, raw_events_batcher
from tinybird.resource import Resource
from tinybird.sql_template import TemplateExecutionResults
from tinybird.syncasync import async_to_sync
from tinybird.user import User as Workspace
from tinybird.user import UserAccountDoesNotExist, public
from tinybird.user import Users as Workspaces
from tinybird.views.api_errors.utils import replace_table_id_with_datasource_id
from tinybird_shared.clickhouse.errors import CHErrors

MAX_POPULATE_INSERT_QUERY_DURATION_SECONDS_TO_OPTIMIZE = 300  # 5 minutes
MAX_POPULATE_MOVE_PARTS_EXECUTION_TIME = 4 * 3600
POPULATE_GUARDED_QUERY_TIMEOUT = 10
POPULATE_TIME_BEFORE_CHECK_TIMEOUT = 120

RETRIABLE_CH_EXCEPTIONS = [
    CHErrors.TIMEOUT_EXCEEDED,
    CHErrors.KEEPER_EXCEPTION,
    CHErrors.TOO_MANY_RETRIES_TO_FETCH_PARTS,
]


class PopulateUserAgents:
    INTERNAL_POPULATE = "no-tb-populate"
    POPULATE_QUERY = "no-tb-populate-query"
    POPULATE_ALTER_QUERY = "no-tb-populate-alter-query"


class PopulateException(Exception):
    pass


class PopulateJobQuery:
    def __init__(
        self,
        query_id: str,
        sql: Optional[str],
        status: str,
        database_server: Optional[str],
        partition: Optional[str] = None,
    ) -> None:
        self.query_id = query_id
        self.sql = sql
        self.status = status
        self._database_server = database_server
        self.partition = partition
        self.max_retries = 3
        self.retry_count = 0
        self.total_steps: int = 0
        self.remaining_steps: int = 0
        self.steps: List[Dict[str, Any]] = []

    @property
    def database_server(self) -> Optional[str]:
        return getattr(self, "_database_server", None)

    def as_log_dict(self) -> Dict[str, Any]:
        log: Dict[str, str | int | None] = {
            "query_id": self.query_id,
            "status": self.status,
            "partition": self.partition,
        }
        if hasattr(self, "steps") and self.steps:
            log = {**log, "steps": self.steps_as_json()}
        if hasattr(self, "total_steps") and self.total_steps > 0:
            log["total_steps"] = self.total_steps
            log["remaining_steps"] = self.remaining_steps
        return log

    def steps_as_json(self):
        if hasattr(self, "steps"):
            exclude_keys = ["id"]
            return [{key: step[key] for key in step if key not in exclude_keys} for step in self.steps]
        return []


class PopulateJobQueryStepCollector(StepCollector):
    def __init__(self, job_id: str, query: PopulateJobQuery):
        self.job_id = job_id
        self.query = query

    def add_step(self, id: Tuple[Any, Any, Any], status: str, kind: str) -> Optional[Dict[str, Any]]:
        if not hasattr(self.query, "steps"):
            return None
        destination_database_name, datasource_id, partition = id
        step: Dict[str, Any] = {"id": id, "status": status, "partition": partition, "kind": kind}
        if (ws := Workspace.get_by_database(destination_database_name)) and (ds := ws.get_datasource(datasource_id)):
            step["resource"] = f"{ws.name}.{ds.name}"

        self.query.steps.append(step)
        PopulateJobQueries.update_query_step(self.job_id, self.query.query_id, step)
        return step

    def update_step(
        self, id: Tuple[Any, Any, Any], step_query_id: str, status: str, kind: str, error: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        if not hasattr(self.query, "steps"):
            return None
        step = next((step for step in self.query.steps if step["id"] == id and step["kind"] == kind), None)
        if not step:
            step = self.add_step(id, status, kind)
        if not step:
            return None

        step["query_id"] = step_query_id
        step["status"] = status
        if status == "working" and "started_at" not in step:
            step["started_at"] = str(datetime.now(timezone.utc).replace(tzinfo=None))

        if status in ["done", "error"]:
            if "started_at" in step:
                started_at = datetime.strptime(step["started_at"], "%Y-%m-%d %H:%M:%S.%f")
                step["elapsed_time"] = (datetime.now(timezone.utc).replace(tzinfo=None) - started_at).total_seconds()
            if status == "done":
                self.query.remaining_steps = max(0, self.query.remaining_steps - 1)
                PopulateJobQueries.remove_query_step(self.job_id, self.query.query_id, step)
                return step
            if error:
                step["error"] = error
        PopulateJobQueries.update_query_step(self.job_id, self.query.query_id, step)
        return step

    def update_stats(self, total_steps: int):
        if not hasattr(self.query, "total_steps"):
            return

        self.query.total_steps = total_steps
        PopulateJobQueries.update_query_stats(self.job_id, self.query.query_id, total_steps, total_steps)


class PopulateJobQueries:
    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def update_query_step(job_id: str, query_id: str, step: Dict[str, Any]) -> None:
        with Job.transaction(job_id) as j:
            j = cast("PopulateJob", j)
            query = next((q for q in j.queries if q.query_id == query_id), None)
            if query:
                index = next(
                    (
                        i
                        for i, _step in enumerate(query.steps)
                        if _step["id"] == step["id"] and _step["kind"] == step["kind"]
                    ),
                    None,
                )
                if index is not None:
                    query.steps[index] = step
                else:
                    query.steps.append(step)
        j.send_raw_event()

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def remove_query_step(job_id: str, query_id: str, step: Dict[str, Any]) -> None:
        with Job.transaction(job_id) as j:
            j = cast("PopulateJob", j)
            query = next((q for q in j.queries if q.query_id == query_id), None)
            if query:
                indexes = [
                    i
                    for i, _step in enumerate(query.steps)
                    if _step["id"] == step["id"] and _step["kind"] == step["kind"]
                ]
                for index in indexes:
                    del query.steps[index]
                    query.remaining_steps = max(0, query.remaining_steps - 1)

        j.send_raw_event()

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def update_query_status(job_id: str, query_id: str, new_status: str) -> None:
        with Job.transaction(job_id) as j:
            j = cast("PopulateJob", j)
            for query in j.queries:
                if query.query_id == query_id:
                    query.status = new_status
                    break
        j.send_raw_event()

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def update_queries_cancelled(job_id: str, query_id: str) -> None:
        with Job.transaction(job_id) as j:
            j = cast("PopulateJob", j)
            for query in j.queries:
                if query.query_id == query_id:
                    query.status = JobStatus.DONE
                else:
                    query.status = JobStatus.CANCELLED if query.status == JobStatus.WAITING else query.status
        j.send_raw_event()

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def update_query_id(job_id: str, query_id: str, new_query_id: str) -> Tuple[Optional[PopulateJobQuery], Job]:
        new_query = None
        with Job.transaction(job_id) as j:
            j = cast("PopulateJob", j)
            for query in j.queries:
                if query.query_id == query_id:
                    query.query_id = new_query_id
                    query.retry_count += 1
                    new_query = query
                    break
        j.send_raw_event()
        return new_query, j

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def update_query_stats(job_id: str, query_id: str, total_steps: int, remaining_steps: int) -> None:
        with Job.transaction(job_id) as j:
            j = cast("PopulateJob", j)
            query = next((q for q in j.queries if q.query_id == query_id), None)
            if query:
                query.total_steps = total_steps
                query.remaining_steps = remaining_steps

        j.send_raw_event()

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def append_new_queries(
        job_id: str, queries: List[PopulateJobQuery], temporal_tables: Optional[List[Optional[str]]] = None
    ) -> None:
        with Job.transaction(job_id) as j:
            j = cast("PopulateJob", j)
            j.queries += queries
            if not temporal_tables:
                return
            for table in temporal_tables:
                if not table:
                    continue
                j.temporal_tables.append(table)
        j.send_raw_event()


class PopulateJob(Job):
    UNLINK_ERROR_MESSAGE = ": the Materialized View has been unlinked and it's not materializing data. Fix the issue in the Materialized View and create it again. See https://www.tinybird.co/docs/api-reference/pipe-api.html#post--v0-pipes-(.+)-nodes-(.+)-population to learn how to check the status of the Job"

    def __init__(
        self,
        user: Workspace,
        view_node: str,
        view_sql: str,
        target_table: str,
        pipe_id: Optional[str] = None,
        pipe_name: Optional[str] = None,
        pipe_url: Optional[str] = None,
        populate_subset: Optional[str] = None,
        populate_condition: Optional[str] = None,
        truncate: bool = False,
        unlink_on_populate_error: bool = False,
        request_id: str = "",
        branch_id: Optional[str] = None,
        check_first_population_on_error: Optional[bool] = True,
    ) -> None:
        self.user = user
        self.view_sql = view_sql
        self.target_table = target_table
        self.view_node = view_node
        self.pipe_id = pipe_id
        self.pipe_name = pipe_name
        self.pipe_url = pipe_url
        self.query_id = ulid.new().str
        self.queries: List[PopulateJobQuery] = []
        self.temporal_tables: List[str] = []
        self.populate_subset = get_populate_subset(populate_subset)
        self.populate_condition = populate_condition
        self.database_server = user["database_server"]
        self.database = user["database"]
        self.destination_server_for_job: str | None = None
        self.truncate = truncate
        self.unlink_on_populate_error = unlink_on_populate_error
        self.request_id = request_id
        self.branch_id = branch_id
        self.backfill_condition: Optional[str] = None
        self.check_first_population_on_error = check_first_population_on_error
        self.insert_query_settings: Dict[str, Any] = {}
        self.cluster = user.cluster

        datasource = None
        meta_workspace = user

        if target_table:
            try:
                datasource = Workspaces.get_datasource(meta_workspace, target_table)
            except Exception as e:
                logging.exception(f"Failed get data source '{target_table}' information on populate: {e}")
                datasource = None

        Job.__init__(self, JobKind.POPULATE, user, datasource=datasource)

        self.__ttl__ = 3600 * int(
            user.get_limits(prefix="populate").get("populate_max_job_ttl_in_hours", Limit.populate_max_job_ttl_in_hours)
        )

    def __setstate__(self, state: Dict[str, Any]) -> None:
        if "queries" not in state:
            self.queries = [
                PopulateJobQuery(
                    query_id=state["query_id"],
                    sql=None,
                    status=state["status"],
                    database_server=None,
                    partition=state.get("partition", None),
                )
            ]
        super().__setstate__(state)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def save_backfill_condition(job_id: str, backfill_condition: Optional[str] = None) -> "PopulateJob":
        with Job.transaction(job_id) as j:
            j = cast("PopulateJob", j)
            j.backfill_condition = backfill_condition
        return j

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def prevent_unlink_on_error(job_id: str) -> "PopulateJob":
        with Job.transaction(job_id) as j:
            j = cast("PopulateJob", j)
            j.check_first_population_on_error = False
            j.unlink_on_populate_error = False
        return j

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def update_destination_server(job_id: str, server: str) -> "PopulateJob":
        with Job.transaction(job_id) as job:
            job = cast("PopulateJob", job)
            job.destination_server_for_job = server
            return job

    def is_sampled(self) -> bool:
        return hasattr(self, "populate_subset") and self.populate_subset > 0

    def to_json(self, workspace: Optional[Workspace] = None, debug: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        job = super().to_json(workspace, debug)

        job["query_id"] = self.query_id

        if self.pipe_id:
            job["pipe_id"] = self.pipe_id
        if self.pipe_name:
            job["pipe_name"] = self.pipe_name

        if hasattr(self, "populate_subset") and self.populate_subset and self.populate_subset >= 0:
            job["populate_subset"] = self.populate_subset

        if hasattr(self, "populate_condition") and self.populate_condition:
            job["populate_condition"] = self.populate_condition

        if hasattr(self, "backfill_condition") and self.backfill_condition:
            job["backfill_condition"] = self.backfill_condition

        if self.stats:
            job["statistics"] = self.stats

        if self.status == JobStatus.ERROR and "error" in self.result:
            job["error"] = self.result["error"]
            job["help"] = "https://www.tinybird.co/guide/transformation-pipes"

            if self.pipe_name and self.pipe_id:
                pipe_url_detail = f": {self.pipe_url}" if self.pipe_url else ""
                job["detail"] = (
                    f"Please make sure the pipe '{self.user.name}.{self.pipe_name}' ({self.pipe_id}) is correct{pipe_url_detail}"
                )

        datasource = self.datasource_to_json(workspace=workspace)
        if datasource:
            job.update({"datasource": datasource})

        return job

    def send_raw_event(self: "PopulateJob") -> None:
        updated_populate_job = self.get_by_id(self.id)
        if not updated_populate_job:
            logging.exception(f"Populate job {self.id} not found")
            return
        populatejob_event = convert_populatejob_to_rawevent(updated_populate_job)
        raw_events_batcher.append_record(populatejob_event)

    async def progress_details(self) -> Dict[str, Any]:
        queries_details: List = []
        progress_details = {"queries": queries_details, "progress_percentage": 0}
        if not self.queries:
            return progress_details

        queries_ids = [f"'{query.query_id}'" for query in self.queries]
        query_table = (
            f"clusterAllReplicas('{self.user.cluster}', system.processes)" if self.user.cluster else "system.processes"
        )

        q = f"""SELECT
            query_id,
            100*read_rows/total_rows_approx as progress_percentage,
            elapsed as elapsed_time,
            greatest(0.0, (elapsed / (read_rows/total_rows_approx)) * (1 - (read_rows/total_rows_approx))) as estimated_remaining_time
        FROM {query_table}
        WHERE query_id IN ({', '.join(queries_ids)})
        FORMAT JSON
        """
        queries_progress: Dict[str, Any] = {}
        try:
            client = HTTPClient(self.user.database_server, database=self.user.database)
            _, body = await client.query(q)
            query_metrics: Dict[str, Any] = json.loads(body)
            queries_progress = {q["query_id"]: q for q in query_metrics.get("data", [])}
        except Exception as e:
            logging.warning(e)

        for pop_query in self.queries:
            status = pop_query.status
            # If the job failed as a whole, the status of the individual queries might be inconsistent.
            # For instance, a query failed but we were not able to move it from "working" to "error" status.
            # Also, any pending queries will stay as waiting after the job failed.
            # In those cases, if you request the progress details, you will receive the job marked as error
            # but some of the queries marked as working or waiting.
            # With this, we avoid having that inconsistency.
            if self.status == JobStatus.ERROR and status not in (JobStatus.DONE, JobStatus.ERROR):
                status = JobStatus.ERROR

            query_progress = queries_progress.get(pop_query.query_id, {})
            query_progress_percentage: float = query_progress.get("progress_percentage", 0) or 0

            if query_progress_percentage > 100:
                del query_progress["progress_percentage"]
                query_progress["progress"] = "Query is still running but cannot estimate progress"
            else:
                if pop_query.total_steps > 0:
                    _progress_percentage = query_progress_percentage
                    if _progress_percentage > 0:
                        _progress_percentage /= 2
                        steps_percentage = (pop_query.remaining_steps / pop_query.total_steps * 100) / 2
                        query_progress["progress_percentage"] = _progress_percentage + steps_percentage

            query_details = {
                "query_id": pop_query.query_id,
                "status": status,
                **query_progress,
            }

            if hasattr(pop_query, "partition") and pop_query.partition:
                query_details.update({"partition": pop_query.partition})

            if hasattr(pop_query, "steps") and pop_query.steps:
                query_details.update({"steps": pop_query.steps_as_json()})

            if hasattr(pop_query, "total_steps") and pop_query.total_steps > 0:
                query_details["total_steps"] = pop_query.total_steps
                query_details["remaining_steps"] = pop_query.remaining_steps

            queries_details.append(query_details)

        if not queries_details:
            pass
        elif all([q["status"] == JobStatus.DONE for q in queries_details]):
            progress_details["progress_percentage"] = 100
        else:
            progress_per_query: float = 1 / len(queries_details)
            _progress_per_query = progress_per_query
            progress_percentage: float = 0
            for d in queries_details:
                if d["status"] == JobStatus.DONE:
                    progress_percentage += progress_per_query
                elif d["status"] == JobStatus.WORKING:
                    if d.get("total_steps", 0) > 0:
                        _progress_per_query = progress_per_query / 2
                    if "progress_percentage" in d:
                        # progress_percentage might be None when the query has just started
                        if "progress" not in d:
                            progress_percentage += _progress_per_query * (d["progress_percentage"] or 0) / 100
                    else:
                        if d.get("remaining_steps", 0) > 0:
                            steps_percentage = (
                                (d["total_steps"] - d["remaining_steps"]) / d["total_steps"] * _progress_per_query
                            )
                            progress_percentage += _progress_per_query + steps_percentage
            progress_details["progress_percentage"] = progress_percentage * 100

        return progress_details

    def should_unlink(self, exception: Exception) -> bool:
        try:
            if self.unlink_on_populate_error:
                return True

            if not isinstance(exception, CHException):
                return False

            if isinstance(exception, PopulateException):
                return False

            if exception.code in [CHErrors.TIMEOUT_EXCEEDED]:
                return False

            if not self.unlink_on_populate_error and not self.check_first_population_on_error:
                return False

            return self.is_first_population()
        except Exception as e:
            logging.warning(str(e))
            return False

    def is_first_population(self) -> bool:
        try:
            pu = public.get_public_user()
            datasource = pu.get_datasource("datasources_ops_log")
            if not datasource:
                return False

            assert isinstance(self.user_id, str)
            workspace = Workspace.get_by_id(self.user_id)
            sql = f"""
                SELECT count() AS c FROM {datasource.id}
                WHERE
                    user_id = '{workspace.main_id}'
                    AND datasource_id = '{self.target_table}'
                    AND event_type = 'populateview'
                    AND result = 'ok'
                FORMAT JSON
            """

            client = HTTPClient(pu.database_server, database=pu.database)
            _, body = client.query_sync(sql, read_only=True, user_agent=PopulateUserAgents.INTERNAL_POPULATE)
            res = json.loads(body)["data"]
            # implicitly unlink if it's the first population
            return len(res) > 0 and res[0]["c"] == 0
        except UserAccountDoesNotExist:
            return False

    def run(self) -> "PopulateJob":
        def function_to_execute(job: Job) -> None:
            job = cast("PopulateJob", job)
            unlink_error = ""
            try:
                PopulateJob.populate(job)
            except JobCancelledException:
                job = cast("PopulateJob", self.mark_as_cancelled())
                job.track()
            except Exception as e:
                try:
                    j = Job.get_by_id(job.id)
                    if not j:
                        logging.exception(f"Populate job {job.id} not found")
                        return
                    job = cast("PopulateJob", j)
                    if job.should_unlink(e):
                        unlink_matview_sync = async_to_sync(unlink_matview)
                        unlink_matview_sync(job.user, job.view_node)
                        unlink_error = PopulateJob.UNLINK_ERROR_MESSAGE
                except Exception as e_unlink:
                    logging.exception(str(e_unlink))

                logging.info(f"Marking job {job.id} as error: {str(e)}{unlink_error}")
                error = f"{str(e)}{unlink_error}"
                job = cast("PopulateJob", self.mark_as_error({"error": error}))
                job.track(error)
            else:
                job = cast("PopulateJob", self.mark_as_done({}, None))
                PopulateJob.save_counts(job)
                job.track()

        if hasattr(self, "job_executor"):
            self.job_executor.submit(function_to_execute, self)
        else:
            function_to_execute(self)
        return self

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def save_counts(job: "PopulateJob") -> "PopulateJob":
        stats = job.get_counts()
        if not stats:
            return job
        with Job.transaction(job.id) as j:
            j = cast("PopulateJob", j)
            if not j.stats:
                j.stats = {}

            j.stats["row_count"] = {"live": stats[0], "current": stats[1]}
        return j

    def get_counts(self) -> Optional[Tuple[int, int]]:
        assert self.user_id

        workspace = Workspace.get_by_id(self.user_id)
        if not workspace.is_release:
            return None
        main = workspace.get_main_workspace()

        ds_release = workspace.get_datasource(self.target_table)
        if not ds_release:
            return -1, -1
        ds_main = main.get_datasource(ds_release.name)
        if not ds_main:
            return -1, -1
        release_count = ch_row_count_sync(workspace.database_server, workspace.database, self.target_table)
        main_count = ch_row_count_sync(main.database_server, main.database, ds_main.id)

        return main_count, release_count

    def track(self, error: Optional[str] = None) -> None:
        try:
            assert self.user_id

            workspace = Workspace.get_by_id(self.user_id)
            target_ds = workspace.get_datasource(self.target_table)
            source_table = ch_source_table_for_view_sync(workspace.database_server, workspace.database, self.view_node)
            source_ds = None
            if source_table:
                source_ds = workspace.get_datasource(source_table.table)

            datasource_id = target_ds.id if target_ds else self.target_table
            datasource_name = target_ds.name if target_ds else "unknown"

            resource_tags: List[str] = []
            if workspace:
                resource_tags = [tag.name for tag in workspace.get_tags_by_resource(datasource_id, datasource_name)]

            record = tracker.DatasourceOpsLogRecord(
                timestamp=self.created_at.replace(tzinfo=timezone.utc),
                event_type=JobKind.POPULATE,
                datasource_id=datasource_id,
                datasource_name=datasource_name,
                user_id=workspace.id,
                # FIXME: Does it make sense to keep this? A workspace can have no email and some other places we just use the name.
                user_mail=workspace["email"] if "email" in workspace else workspace.name,  # noqa: SIM401
                result="ok" if self.status == JobStatus.DONE else self.status,
                elapsed_time=(
                    datetime.now(timezone.utc) - self.created_at.replace(tzinfo=timezone.utc)
                ).total_seconds(),
                error=error if self.status == JobStatus.ERROR and error else "",
                request_id=self.request_id if self.request_id else self.id,
                import_id=self.id,
                job_id=self.id,
                rows=0,
                rows_quarantine=0,
                blocks_ids=[],
                Options__Names=list(["job", "trigger_datasource_id"]),
                Options__Values=list([json.dumps(self.to_json()), source_ds.id if source_ds else "unknown"]),
                pipe_id=self.pipe_id or "",
                pipe_name=self.pipe_name or "",
                read_rows=0,
                read_bytes=0,
                written_rows=0,
                written_bytes=0,
                written_rows_quarantine=0,
                written_bytes_quarantine=0,
                operation_id=self.id,
                release="",
                resource_tags=resource_tags,
            )
            dot = tracker.DatasourceOpsTrackerRegistry.get()
            query_ids = [
                query.query_id
                for query in self.queries
                if query.status not in [JobStatus.CANCELLING, JobStatus.CANCELLED, JobStatus.WAITING]
            ]

            if dot and dot.is_alive:
                rec = tracker.DatasourceOpsLogEntry(
                    record=record,
                    eta=datetime.now(timezone.utc),
                    workspace=workspace,
                    query_ids=query_ids,
                    query_ids_quarantine=[],
                    cluster=self.cluster if hasattr(self, "cluster") else workspace.cluster,
                    view_name=self.view_node,
                )
                dot.submit(rec)
            else:
                logging.exception("DatasourceOpsTrackerRegistry is dead")
        except Exception as e:
            logging.exception(str(e))

    def has_been_externally_cancelled_function_generator(self) -> Callable[[], bool]:
        def has_been_cancelled() -> bool:
            job = Job.get_by_id(self.id)
            return job is not None and job.status == JobStatus.CANCELLING

        return has_been_cancelled

    def wait_until_backfill_condition(
        self, workspace: Workspace, source_table: Optional[CHTableLocation]
    ) -> Optional[str]:
        if not source_table:
            return None

        source_ds = workspace.get_datasource(source_table.table, include_read_only=True)
        if not source_ds and workspace.is_release:
            try:
                source_ds = workspace.get_main_workspace().get_datasource(source_table.table, include_read_only=True)
            except ValueError as e:
                logging.error(f"Error on populate the process will continue: {str(e)}")
        backfill_column = source_ds.tags.get("backfill_column") if source_ds else None
        backfill_value = None
        pipe = Workspaces.get_pipe_by_node(workspace, self.view_node)
        if pipe:
            node = pipe.pipeline.get_node(self.view_node)
            backfill_value = node.tags.get("backfill_value") if node else None
            logging.warning(f"pipe name: {pipe.name}")
        else:
            logging.error(
                f"pipe not found on populate: node: {self.view_node} - pipe: {self.pipe_id} - workspace: {workspace.id}"
            )
        logging.warning(f"backfill_column: {backfill_column}")
        logging.warning(f"backfill_value: {backfill_value}")
        backfill_condition = None
        if backfill_column and backfill_value and not (hasattr(self, "populate_condition") and self.populate_condition):
            backfill_condition = f"{backfill_column} <= '{backfill_value}'"

            # wait for backfill_condition
            def wait_until(target_time_str):
                target_time = datetime.strptime(target_time_str, "%Y-%m-%d %H:%M:%S")
                target_time = target_time.replace(tzinfo=timezone.utc)
                current_time = datetime.now(timezone.utc)
                wait_seconds = (target_time - current_time).total_seconds()

                if wait_seconds > 0:
                    if wait_seconds > MATVIEW_BACKFILL_VALUE_WAIT:
                        logging.warning(
                            f"The target time {target_time_str} is way in the future. This might indicate the `backfill_column` is not UTC"
                        )
                    else:
                        logging.warning(f"Waiting for {wait_seconds} seconds until {target_time_str}")
                        time.sleep(wait_seconds)
                else:
                    logging.warning(f"The target time {target_time_str} is already in the past.")

            wait_until(backfill_value)
        return backfill_condition

    def get_initial_query_settings(self) -> Dict[str, Any]:
        workspace = Workspace.get_by_id(self.user.id)

        # 1. Workspace Limits
        populate_limits = workspace.get_limits(prefix="populate")

        # 2. Get Config Limits
        populate_settings_config = get_clickhouse_settings_for_populates(workspace)

        # 3. Calculate Initial Settings - Workspace Limits orevail over Config Limits for memory, threads, and insert block size

        # 3.1 - threads
        max_insert_threads = populate_settings_config.get("max_insert_threads", Limit.ch_max_insert_threads)
        max_insert_threads = populate_limits.get("populate_max_insert_threads", max_insert_threads)
        max_threads = populate_limits.get("populate_max_threads", max_insert_threads)

        # 3.2 - insert block size
        max_insert_block_size = populate_settings_config.get(
            "max_insert_block_size", Limit.populate_max_insert_block_size
        )
        max_insert_block_size = populate_limits.get("populate_max_insert_block_size", max_insert_block_size)

        # 3.3 - memory usage percentage
        max_memory_usage_percentage = populate_settings_config.get("max_memory_usage_percentage", None)
        max_memory_usage_percentage = populate_limits.get(
            "populate_max_memory_usage_percentage", Limit.populate_max_memory_usage_percentage
        )

        if self.destination_server_for_job and max_memory_usage_percentage:
            memory_available, _ = ch_get_replica_load(database_server=self.destination_server_for_job)
            max_memory_usage = int(memory_available * float(max_memory_usage_percentage))
        else:
            max_memory_usage = populate_limits.get("populate_max_memory_usage", Limit.populate_max_memory_usage)

        # 3.4 - defaults
        min_insert_block_size_rows = populate_limits.get(
            "populate_min_insert_block_size_rows", Limit.populate_min_insert_block_size_rows
        )
        min_insert_block_size_bytes = populate_limits.get(
            "populate_min_insert_block_size_bytes", Limit.populate_min_insert_block_size_bytes
        )

        timeout_before_checking_execution_speed = populate_limits.get(
            "populate_timeout_before_checking_execution_speed", POPULATE_TIME_BEFORE_CHECK_TIMEOUT
        )

        # 4. Set Settings
        populate_settings = {
            "max_insert_threads": max_insert_threads,
            "max_threads": max_threads,
            "max_insert_block_size": max_insert_block_size,
            "min_insert_block_size_rows": min_insert_block_size_rows,
            "min_insert_block_size_bytes": min_insert_block_size_bytes,
            "preferred_block_size_bytes": min_insert_block_size_bytes,
            "max_memory_usage": max_memory_usage,
            "timeout_before_checking_execution_speed": timeout_before_checking_execution_speed,
        }

        if max_estimated_execution_time := populate_limits.get("populate_max_estimated_execution_time"):
            populate_settings["max_estimated_execution_time"] = max_estimated_execution_time

        settings = {key: value for key, value in populate_settings.items() if value is not None}
        return settings

    @retry_job_transaction_in_case_of_error_sync()
    def update_cluster(self: "PopulateJob", cluster_name: str) -> "PopulateJob":
        with PopulateJob.transaction(self.id) as job:
            job.cluster = cluster_name
            return job

    @staticmethod
    def run_populate_on_replica(database_server: str, job: "PopulateJob") -> None:
        """
        runs populate on a specific replica given the materialized view id.
        Most likely view_sql and target_table can be guessed from the matview id but this gives some flexibility

        in order to populate a table we could just execute:

        insert into table MAT_VIEW_QUERY

        but this fails when source table is large.

        To avoid this an intermediate table with NUll engine is used, in this way the data is written in chunks
        """
        temporal_null_table = None
        temporal_view_from_null_table = None

        j = PopulateJob.get_by_id(job.id)
        if not j:
            raise PopulateException(f"Populate job {job.id} not found")
        job = j
        workspace = job.user
        logger = job.getLogger()
        workspace_database = workspace.database
        mv_id = job.view_node
        view_sql = job.view_sql
        target_table = job.target_table
        num_partitions = 1

        # This is to decide whether or not use the revamp, since if job.destination_server_for_job is defined,
        # it will have the same value as the current database_server
        # If at some point we decide to use the revamp as default, we can remove this check

        is_preview_release = workspace.is_release or workspace.is_release_in_branch
        use_revamp = job.destination_server_for_job and not is_preview_release
        use_pool_replica = (
            FeatureFlagsWorkspaceService.feature_for_id(
                FeatureFlagWorkspaces.POOL_REPLICA_FOR_POPULATES, workspace.id, workspace.feature_flags
            )
            and use_revamp
        )
        pool_replica_databases = set()
        pool_replica_disk_settings = None
        origin_database_server = j.database_server if use_pool_replica else database_server
        logger.info(
            f"Populate ({job.id}) uses revamp: {use_revamp}. Destination server: {job.destination_server_for_job}. Is preview release: {is_preview_release}"
        )

        populates_database = workspace_database
        insert_into_cluster = workspace.cluster if not use_revamp else ""
        populate_databases_mapping: Dict[str, str] = {}
        tables_path: Dict[str, str] = {}

        try:
            # get source table
            source_table = ch_source_table_for_view_sync(origin_database_server, workspace_database, mv_id)
            if not source_table:
                raise Exception(
                    f"Error: Trigger Data Source for Materialized Pipe {job.pipe_name} does not exist. Please check `tinybird.datasource_ops_log` to look for traces on `create` and `delete` event_types."
                )

            target_table_details = ch_table_details(target_table, origin_database_server, workspace_database)
            if not target_table_details:
                raise Exception(
                    f"Error: Materialized View with ID {target_table} for Pipe {job.pipe_name} does not exist. Please check `tinybird.datasource_ops_log` to look for traces on `create` and `delete` event_types."
                )

            if job.truncate:
                ch_truncate_table_sync = async_to_sync(ch_truncate_table_with_fallback)
                ch_truncate_table_sync(origin_database_server, workspace_database, target_table, cluster=None)

            queries: List[PopulateJobQuery] = []
            populate_table = f"{Resource.guid()}_view_node_{mv_id}"
            backfill_condition = job.wait_until_backfill_condition(workspace, source_table)

            if target_table_details.engine.lower() != "join":
                columns = None
                column_names = "*"

                try:
                    columns = ch_get_columns_from_left_table_used_in_query_sync(
                        database=workspace_database, database_server=origin_database_server, sql=view_sql
                    )
                    column_names = ",".join([c.get("name") for c in columns]) if columns and len(columns) else "*"
                except Exception as e:
                    logging.warning(f"Populate error: could not get columns for query {view_sql} {e}")

                if use_revamp:
                    try:
                        (
                            dependent_databases,
                            dependent_materialized_views,
                            dependent_data_sources,
                        ) = job.get_dependent_databases(workspace, source_table.table, job.query_id)

                        if use_pool_replica:
                            job.update_cluster(get_pool_cluster_name())
                            pool_replica_disk_settings = get_dynamic_disk_settings_for_populates(workspace)
                            if not pool_replica_disk_settings:
                                raise PopulateException("No disk settings found for populates while using pool replica")
                            pool_replica_databases = create_user_tables_on_pool_replica(
                                origin_database_server,
                                database_server,
                                dependent_databases,
                                dependent_data_sources,
                                dependent_materialized_views,
                                view_sql,
                                pool_replica_disk_settings,
                            )

                        (
                            populates_database,
                            tables_path,
                            populate_databases_mapping,
                        ) = ch_create_temporary_databases_sync(
                            database_server=database_server,
                            origin_database=workspace_database,
                            all_databases=dependent_databases,
                            dependent_data_sources=dependent_data_sources,
                            dependent_materialized_views=dependent_materialized_views,
                            disk_settings=pool_replica_disk_settings,
                            # important: do not set a cluster here
                        )
                    except CHException as e:
                        logging.error(f"Populate {job.id} failed while creating the temporary database, error: {e}")
                        error = replace_table_id_with_datasource_id(job.user, str(e))
                        raise PopulateException(
                            f"Job failed before start. {error}. In case of doubt, please contact us at support@tinybird.co dbs, {dependent_data_sources}, views {dependent_materialized_views}"
                        )
                    except Exception as e:
                        logging.error(f"Populate {job.id} failed while creating the temporary database, error: {e}")
                        raise PopulateException(
                            f"Job failed due to an internal error, try it again. If the problem persists, please contact us at support@tinybird.co. {e}"
                        )

                    target_table_details = ch_table_details(target_table, database_server, populates_database)
                    if not target_table_details:
                        logging.error(
                            f"Populate {job.id} failed while getting details from the temporary database {populates_database}"
                        )
                        raise PopulateException(
                            "Job failed due to an internal error, try it again. If the problem persists, please contact us at support@tinybird.co"
                        )

                    (
                        temporal_null_table,
                        temporal_view_from_null_table,
                    ) = ch_create_null_table_with_mv_for_mv_populate_with_fetch(
                        workspace=workspace,
                        source_table=source_table,
                        target_database=populates_database,
                        target_table=target_table,
                        target_table_details=target_table_details,
                        temporal_table_sufix=f"tmp_populate_new_{populate_table}",
                        view_sql=view_sql,
                        temporal_view_sufix=f"tmp_populate_view_new_{populate_table}",
                        include_ttl_in_replacements_operation=True,
                        columns=columns,
                        target_database_server=database_server,
                    )

                    source_table_details = ch_table_details(
                        table_name=source_table.table,
                        database_server=database_server,
                        database=source_table.database,
                    )
                    source_ttl = ttl_condition_from_engine_full(source_table_details.engine_full)
                else:
                    try:
                        temporal_table_sufix = f"tmp_populate_{populate_table}"
                        temporal_view_sufix = f"tmp_populate_view_{populate_table}"
                        (
                            temporal_null_table,
                            temporal_view_from_null_table,
                        ) = ch_create_null_table_with_mv_for_mv_populate(
                            workspace=workspace,
                            source_table=source_table,
                            target_table=target_table,
                            target_table_details=target_table_details,
                            temporal_table_sufix=temporal_table_sufix,
                            view_sql=view_sql,
                            temporal_view_sufix=temporal_view_sufix,
                            include_ttl_in_replacements_operation=True,
                            columns=columns,
                            **workspace.ddl_parameters(skip_replica_down=True),
                        )
                    except Exception as e:
                        if not columns:
                            raise e

                        # fallback without the subset of columns
                        logging.warning(
                            f"Populate error: fallback due to column mismatch. Columns: {columns}. Error: {e} - {job.to_json()}"
                        )

                        columns = None
                        column_names = "*"

                        (
                            temporal_null_table,
                            temporal_view_from_null_table,
                        ) = ch_create_null_table_with_mv_for_mv_populate(
                            workspace=workspace,
                            source_table=source_table,
                            target_table=target_table,
                            target_table_details=target_table_details,
                            temporal_table_sufix=temporal_table_sufix,
                            view_sql=view_sql,
                            temporal_view_sufix=temporal_view_sufix,
                            include_ttl_in_replacements_operation=True,
                            create_or_replace=True,
                            **workspace.ddl_parameters(skip_replica_down=True),
                        )

                    source_table_details = ch_table_details(
                        table_name=source_table.table,
                        database_server=database_server,
                        database=source_table.database,
                    )
                    source_ttl = ttl_condition_from_engine_full(source_table_details.engine_full)
                    # populate_subset has precedence over the rest
                if job.is_sampled():
                    MAX_ROWS = 2000000
                    partitions = ch_table_partitions_for_sample_sync(
                        database_server,
                        source_table.database,
                        source_table.table,
                        sample_percentage=job.populate_subset,
                        max_rows=MAX_ROWS,
                    )
                    num_partitions = len(partitions)
                    if len(partitions) > 1:
                        for p in partitions:
                            select_query = build_partition_query(
                                database_server=database_server,
                                source_table=source_table,
                                source_table_details=source_table_details,
                                partition=p[0],
                                limit=p[1],
                                ttl=source_ttl,
                                backfill_condition=backfill_condition,
                                column_names=column_names,
                            )
                            queries.append(
                                PopulateJobQuery(
                                    query_id=ulid.new().str,
                                    sql=f"""
                                    INSERT INTO {populates_database}.{temporal_null_table}
                                    {select_query}
                                    """,
                                    status=JobStatus.WAITING,
                                    database_server=database_server,
                                    partition=p[0],
                                )
                            )
                    else:
                        stats = table_stats(source_table.table, database_server, source_table.database)
                        row_count = stats.get("row_count", 100)
                        limit = min(round(row_count * job.populate_subset) or 1, MAX_ROWS)

                        select_query = build_partition_query(
                            database_server=database_server,
                            source_table=source_table,
                            source_table_details=TableDetails(),
                            partition=None,
                            limit=limit,
                            ttl=source_ttl,
                            backfill_condition=backfill_condition,
                            column_names=column_names,
                        )
                        queries.append(
                            PopulateJobQuery(
                                query_id=ulid.new().str,
                                sql=f"""
                                INSERT INTO {populates_database}.{temporal_null_table}
                                {select_query}
                                """,
                                status=JobStatus.WAITING,
                                database_server=database_server,
                            )
                        )
                else:
                    populate_condition = PopulateJob.get_populate_condition(job, workspace, source_table)
                    partition_names = ch_table_partitions_sync(
                        database_server=database_server,
                        database_name=source_table.database,
                        table_names=[source_table.table],
                        condition=populate_condition,
                        disable_upstream_fallback=True,
                    )
                    if len(partition_names) > 1:
                        for partition_name in partition_names:
                            select_query = build_partition_query(
                                database_server=database_server,
                                source_table=source_table,
                                source_table_details=source_table_details,
                                partition=partition_name,
                                limit=None,
                                ttl=source_ttl,
                                populate_condition=populate_condition,
                                backfill_condition=backfill_condition,
                                column_names=column_names,
                            )
                            try:
                                select_query = Workspaces.replace_tables(
                                    workspace, select_query, release_replacements=True
                                )
                            except ValueError as e:
                                populate_condition_message = (
                                    f", SQL condition: {populate_condition}" if populate_condition else ""
                                )
                                raise Exception(f"[Error] {e}{populate_condition_message}")

                            queries.append(
                                PopulateJobQuery(
                                    query_id=ulid.new().str,
                                    sql=f"""INSERT INTO {populates_database}.{temporal_null_table}
                                    {select_query}
                                """,
                                    status=JobStatus.WAITING,
                                    database_server=database_server,
                                    partition=partition_name,
                                )
                            )
                    else:
                        select_query = build_partition_query(
                            database_server=database_server,
                            source_table=source_table,
                            source_table_details=TableDetails(),
                            partition=None,
                            limit=None,
                            ttl=source_ttl,
                            populate_condition=populate_condition,
                            backfill_condition=backfill_condition,
                            column_names=column_names,
                        )
                        try:
                            select_query = Workspaces.replace_tables(workspace, select_query, release_replacements=True)
                        except ValueError as e:
                            populate_condition_message = (
                                f", SQL condition: {populate_condition}" if populate_condition else ""
                            )
                            raise Exception(f"[Error] {e}{populate_condition_message}")
                        queries.append(
                            PopulateJobQuery(
                                query_id=ulid.new().str,
                                sql=f"""
                                INSERT INTO {populates_database}.{temporal_null_table}
                                {select_query}
                                """,
                                status=JobStatus.WAITING,
                                database_server=database_server,
                            )
                        )

            else:  # join table
                # join tables need to be populated without chunks because if the mat view contains a group by
                # and they join key is in the grouping keys when they are inserted in many batches, later batches
                # could override the first ones.
                queries.append(
                    PopulateJobQuery(
                        ulid.new().str,
                        f"INSERT INTO {populates_database}.{target_table} {view_sql}",
                        JobStatus.WAITING,
                        database_server,
                    )
                )

            temporal_tables: List[Optional[str]] = [temporal_null_table, temporal_view_from_null_table]
            PopulateJobQueries.append_new_queries(job.id, queries, temporal_tables=temporal_tables)

            if backfill_condition:
                job = PopulateJob.save_backfill_condition(job.id, backfill_condition)

            has_been_cancelled_function = job.has_been_externally_cancelled_function_generator()

            def _process_query(query, workspace):
                PopulateJobQueries.update_query_status(job.id, query.query_id, JobStatus.WORKING)
                workspace = workspace.get_by_id(workspace.id)

                if has_been_cancelled_function():
                    PopulateJobQueries.update_query_status(job.id, query.query_id, JobStatus.CANCELLED)
                else:
                    populate_max_execution_time = job.__ttl__ / num_partitions if num_partitions > 0 else job.__ttl__

                    if use_revamp:
                        populate_limits = workspace.get_limits(prefix="populate")
                        max_execution_time = populate_limits.get(
                            "populate_move_parts_max_execution_time", MAX_POPULATE_MOVE_PARTS_EXECUTION_TIME
                        )

                        started_at = time.monotonic()

                        _, query_finish_logs, query = PopulateJob.run_insert_query(
                            database_server=database_server,
                            populates_database=populates_database,
                            temporary_databases=populate_databases_mapping,
                            query=query,
                            insert_into_cluster=insert_into_cluster,
                            populate_max_execution_time=populate_max_execution_time,  # type: ignore
                            job=job,
                            has_been_externally_cancelled=has_been_cancelled_function,
                        )

                        elapsed_seconds = time.monotonic() - started_at

                        next_insert_query_settings = PopulateJob.get_next_insert_query_settings(
                            database_server, job.id, elapsed_seconds, query_finish_logs
                        )
                        PopulateJob.update_insert_query_settings(job.id, next_insert_query_settings)

                        PopulateJob.fetch_data(
                            job_id=job.id,
                            query_id=query.query_id,
                            database_server=database_server,
                            original_database_server=workspace.database_server,
                            populates_database=populates_database,
                            tables_path=tables_path,
                            temporary_databases=populate_databases_mapping,
                            has_been_externally_cancelled=has_been_cancelled_function,
                            cluster=workspace.cluster,
                            timeout_before_checking_execution_speed=POPULATE_TIME_BEFORE_CHECK_TIMEOUT,
                            timeout=POPULATE_GUARDED_QUERY_TIMEOUT,
                            max_execution_time=max_execution_time,
                            step_collector=PopulateJobQueryStepCollector(job.id, query),
                        )
                    else:
                        _, query_finish_logs = ch_guarded_query(
                            database_server,
                            populates_database,
                            # FIXME argument has incompatible type "Optional[str]"; expected "str"
                            cast(str, query.sql),
                            insert_into_cluster,
                            query_id=query.query_id,
                            max_execution_time=populate_max_execution_time,  # type: ignore
                            has_been_externally_cancelled=has_been_cancelled_function,
                            user_agent=PopulateUserAgents.POPULATE_QUERY,
                            timeout=POPULATE_GUARDED_QUERY_TIMEOUT,
                            disable_upstream_fallback=True,
                            retries=False,
                            **job.insert_query_settings,
                        )

                    if query_finish_logs and query_finish_logs.get("type") == "QueryFinish":
                        PopulateJobQueries.update_query_status(job.id, query.query_id, JobStatus.DONE)
                    elif has_been_cancelled_function():
                        PopulateJobQueries.update_query_status(job.id, query.query_id, JobStatus.CANCELLED)
                    else:
                        PopulateJobQueries.update_query_status(job.id, query.query_id, JobStatus.ERROR)
                        logging.error(f"Populate {job.id} failed on query {query.query_id}")
                        if query.partition:
                            raise PopulateException(
                                f"Job failed due to an internal error while populating partition {query.partition}, try it again. If the problem persists, please contact us at support@tinybird.co"
                            )
                        raise PopulateException(
                            "Job failed due to an internal error, try it again. If the problem persists, please contact us at support@tinybird.co"
                        )

            max_parallel_queries = workspace.get_limits(prefix="populate").get("populate_max_concurrent_queries", None)
            if max_parallel_queries:
                with ThreadPoolExecutor(
                    max_workers=max_parallel_queries, thread_name_prefix=f"populate_run_query_{job.id}"
                ) as executor:
                    futures = [executor.submit(_process_query, query, workspace) for query in queries]
                    for future in futures:
                        try:
                            future.result()
                        except Exception as e:
                            logger.exception(f"Populate query failed on thread: {e}")
                            raise e
            else:
                for query in queries:
                    _process_query(query, workspace)

            if use_pool_replica:
                for database in populate_databases_mapping.keys():
                    wait_for_database_replication(database_server, database)

            if has_been_cancelled_function():
                raise JobCancelledException()

            assert_no_mv_links_original_table_with_aux_database(
                database_server, source_table, target_table_details, job.started_at
            )
        except JobCancelledException as e:
            raise e
        except CHException as e:
            logger.exception(e)
            if (
                e.code in [CHErrors.ILLEGAL_TYPE_OF_COLUMN_FOR_FILTER, CHErrors.SYNTAX_ERROR]
                and hasattr(job, "populate_condition")
                and job.populate_condition
            ):
                raise Exception(f"[Error] SQL condition is not valid: `{job.populate_condition}`")
            raise e
        except Exception as e:
            logger.exception(e)
            raise e

        finally:
            # Drop first the MV then the Null table to avoid dependency problems
            tables_to_drop: List[Optional[str]] = [temporal_view_from_null_table, temporal_null_table]
            PopulateJob.drop_temporal_stuff(
                tables_to_drop=tables_to_drop,
                database_server=database_server,
                database=populates_database,
                cluster=insert_into_cluster,
                **job.user.ddl_parameters(skip_replica_down=True),
            )

            if use_revamp:
                PopulateJob.clean_temporal_data(
                    database_server=database_server,
                    populates_database=populates_database,
                    tables_path=tables_path,
                    temporary_databases=populate_databases_mapping,
                    **job.user.ddl_parameters(),
                )
            if use_pool_replica:
                for database in pool_replica_databases:
                    ch_drop_database_sync(database_server=database_server, database=database, sync=True)

    @staticmethod
    def get_populate_condition(job: "PopulateJob", workspace: Workspace, source_table: CHTableLocation) -> str:
        condition = job.populate_condition if hasattr(job, "populate_condition") and job.populate_condition else ""
        if condition:
            select_query = f"""
                SELECT * FROM {source_table.database}.{source_table.table}
            """
            try:
                select_query_replaced = Workspaces.replace_tables(workspace, select_query, release_replacements=True)
                select_condition_query_replaced = Workspaces.replace_tables(
                    workspace, select_query + "WHERE " + condition, release_replacements=True
                )
                condition = (
                    select_condition_query_replaced.replace(select_query_replaced, "").replace("WHERE", "").strip()
                )
            except ValueError as e:
                raise Exception(f"[Error] SQL condition is not valid: `{job.populate_condition}` - {str(e)}")
        return condition

    @staticmethod
    def drop_temporal_stuff(
        tables_to_drop: List[Optional[str]],
        database_server: str,
        database: str,
        cluster: Optional[str],
        **extra_params: Any,
    ) -> None:
        for table in tables_to_drop:
            if not table:
                continue
            try:
                logging.info(f"before dropping table: {table}")
                ch_drop_table_sync(
                    database_server=database_server,
                    database=database,
                    table=table,
                    cluster=cluster,
                    avoid_max_table_size=True,
                    **extra_params,
                )
                logging.info(f"dropped table: {table}")
            except Exception as e:
                logging.exception(f"Exception on drop table {table}: {e}")

    @staticmethod
    def clean_temporal_data(
        database_server: str,
        populates_database: str,
        tables_path: Dict[str, str],
        temporary_databases: Dict[str, str],
        **extra_params: Any,
    ) -> None:
        try:
            for tmp_database in temporary_databases.values():
                ch_drop_database_sync(database_server=database_server, database=tmp_database, **extra_params)
        except Exception as e:
            logging.exception(f"Populate error: cannot drop temporal {populates_database} database {e}")

    @staticmethod
    def truncate_temporal_data(
        database_server: str,
        temporary_databases: Dict[str, str],
        **extra_params: Any,
    ) -> None:
        try:
            databases = [database for _, database in temporary_databases.items()]
            ch_truncate_databases_sync(database_server, databases, **extra_params)
        except Exception as e:
            logging.exception(f"Populate error: cannot truncate temporal data {e}")
            raise e

    @classmethod
    def run_insert_query(
        cls,
        database_server: str,
        populates_database: str,
        temporary_databases: Dict[str, str],
        query: PopulateJobQuery,
        insert_into_cluster: Optional[str],
        populate_max_execution_time: int,
        job: Job,
        has_been_externally_cancelled: Optional[Callable[[], bool]] = None,
    ) -> Tuple[str, Dict[str, Any], PopulateJobQuery]:
        # We refresh the job object to avoid anyone modifying it while we are running the query
        j = cls.get_by_id(job.id)
        if not j:
            raise PopulateException(f"Populate job {job.id} not found")
        job = j
        memory_error = None

        try:
            logging.info(f"Populate ({job.id}) query run, retry count = {query.retry_count}")
            query_id, query_finish_logs = ch_guarded_query(
                database_server,
                populates_database,
                # FIXME argument has incompatible type "Optional[str]"; expected "str"
                cast(str, query.sql),
                insert_into_cluster,
                query_id=query.query_id,
                max_execution_time=populate_max_execution_time,
                has_been_externally_cancelled=has_been_externally_cancelled,
                user_agent=PopulateUserAgents.POPULATE_QUERY,
                timeout=POPULATE_GUARDED_QUERY_TIMEOUT,
                disable_upstream_fallback=True,
                retries=False,
                **job.insert_query_settings,
            )
            return query_id, query_finish_logs, query
        except CHException as e:
            if e.code != CHErrors.MEMORY_LIMIT_EXCEEDED:
                logging.warning(f"Populate ({job.id}) failed: {e}")
                raise e
            logging.info(f"Populate ({job.id}) failed due to a MEMORY_LIMIT_EXCEEDED error")
            memory_error = str(e)

        if query.retry_count > query.max_retries:
            logging.warning(
                f"Populate ({job.id}) could not run after {query.max_retries} retries due to a MEMORY_LIMIT_EXCEEDED error"
            )
            raise Exception(memory_error)
        try:
            PopulateJob.truncate_temporal_data(
                database_server=database_server,
                temporary_databases=temporary_databases,
                **job.user.ddl_parameters(),
            )
            logging.info(f"Populate ({job.id}) temporal data truncated after MEMORY_LIMIT_EXCEEDED error")
        except Exception as e:
            logging.exception(
                f"Populate ({job.id}) could not truncate temporal data after a MEMORY_LIMIT_EXCEEDED error: {e}"
            )
            # Return the original memory error which is the root cause of the operation
            raise Exception(memory_error)

        job = PopulateJob.update_insert_query_settings_after_memory_error(job_id=job.id)
        assert isinstance(job, PopulateJob)

        updated_query, job = PopulateJobQueries.update_query_id(
            job_id=job.id, query_id=query.query_id, new_query_id=ulid.new().str
        )
        assert isinstance(updated_query, PopulateJobQuery)
        assert isinstance(job, PopulateJob)

        return PopulateJob.run_insert_query(
            database_server,
            populates_database,
            temporary_databases,
            updated_query,
            insert_into_cluster,
            populate_max_execution_time,
            job,
            has_been_externally_cancelled,
        )

    @staticmethod
    def fetch_data(
        job_id: str,
        query_id: str,
        database_server: str,
        original_database_server: str,
        populates_database: str,
        tables_path: Dict[str, str],
        temporary_databases: Dict[str, str],
        max_execution_time: int,
        cluster: str,
        has_been_externally_cancelled: Optional[Callable[[], bool]] = None,
        timeout: Optional[int] = POPULATE_GUARDED_QUERY_TIMEOUT,
        timeout_before_checking_execution_speed: Optional[int] = POPULATE_TIME_BEFORE_CHECK_TIMEOUT,
        step_collector: Optional[StepCollector] = None,
    ) -> None:
        try:
            ch_move_partitions_to_disk_sync(
                populate_databases_mapping=temporary_databases,
                original_database_server=original_database_server,
                database_server=database_server,
                tables_path=tables_path,
                max_execution_time=max_execution_time,
                cluster=cluster,
                user_agent=PopulateUserAgents.POPULATE_ALTER_QUERY,
                retriable_exceptions=RETRIABLE_CH_EXCEPTIONS,
                has_been_externally_cancelled=has_been_externally_cancelled,
                timeout_before_checking_execution_speed=timeout_before_checking_execution_speed,
                timeout=timeout,
                step_collector=step_collector,
            )
        except CHException as e:
            logging.exception(f"Populate error: moving partitions to disk failed {e}")
            if e.code in RETRIABLE_CH_EXCEPTIONS:
                job = Job.get_by_id(job_id)
                job = cast("PopulateJob", job)
                # FIXME: better message
                job.mark_as_cancelling(
                    result={
                        "message": "Populate could not finish and has been cancelled, and some partition queries might not have finished. Check which ones are pending and retry them."
                    }
                )
                PopulateJobQueries.update_queries_cancelled(job_id, query_id)
                raise JobCancelledException()
            raise PopulateException(
                "Job failed due to an internal error. If the problem persists, please contact us at support@tinybird.co"
            )
        except Exception as e:
            logging.exception(f"Populate error: moving partitions to disk failed {e}")
            raise e

    @staticmethod
    def get_next_insert_query_settings(
        database_server: str,
        job_id: str,
        query_elapsed_seconds: int | float,
        query_finish_logs: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        job = PopulateJob.get_by_id(job_id)
        if not job:
            raise PopulateException(f"Populate job {job_id} not found")

        insert_query_settings = job.insert_query_settings
        if query_elapsed_seconds < MAX_POPULATE_INSERT_QUERY_DURATION_SECONDS_TO_OPTIMIZE:
            logging.info(
                f"Populate ({job_id}) query using default settings, no need to optimize: query duration = {query_elapsed_seconds} seconds"
            )
            return insert_query_settings

        if not query_finish_logs:
            logging.info(f"Populate ({job_id}) query using default settings, no query_finish_logs present")
            return insert_query_settings

        workspace = Workspace.get_by_id(job.user.id)
        ch_limits = workspace.get_limits(prefix="ch")
        populate_limits = workspace.get_limits(prefix="populate")

        # config limits
        populate_settings_config = get_clickhouse_settings_for_populates(workspace)
        max_memory_usage_percentage = populate_settings_config.get("max_memory_usage_percentage", None)

        # 3.2 - insert block size
        max_insert_block_size = populate_settings_config.get("max_insert_block_size", None)
        memory_thresholds = populate_settings_config.get("memory_thresholds", None)
        cpu_thresholds = populate_settings_config.get("cpu_thresholds", None)

        try:
            memory_thresholds = parse_thresholds(memory_thresholds) if memory_thresholds else [None, None]
            cpu_thresholds = parse_thresholds(cpu_thresholds) if cpu_thresholds else [None, None]

            MIN_MEMORY_THRESHOLD = (
                None
                if memory_thresholds[0] is None
                else float(populate_limits.get("populate_min_memory_threshold", memory_thresholds[0]))
            )
            MAX_MEMORY_THRESHOLD = (
                None
                if memory_thresholds[1] is None
                else float(populate_limits.get("populate_max_memory_threshold", memory_thresholds[1]))
            )
            MIN_CPU_THRESHOLD = (
                None
                if cpu_thresholds[0] is None
                else float(populate_limits.get("populate_min_cpu_threshold", cpu_thresholds[0]))
            )
            MAX_CPU_THRESHOLD = (
                None
                if cpu_thresholds[1] is None
                else float(populate_limits.get("populate_max_cpu_threshold", cpu_thresholds[1]))
            )
            MEMORY_PERCENTAGE = (
                None
                if max_memory_usage_percentage is None
                else float(populate_limits.get("populate_max_memory_usage_percentage", max_memory_usage_percentage))
            )

            if (
                not MIN_MEMORY_THRESHOLD
                or not MAX_MEMORY_THRESHOLD
                or not MIN_CPU_THRESHOLD
                or not MAX_CPU_THRESHOLD
                or not MEMORY_PERCENTAGE
            ):
                logging.info(f"Populate ({job_id}) query using default settings, no thresholds present")
                return insert_query_settings
        except Exception as e:
            logging.exception(
                f"Populate error: Populate ({job_id}) query using default settings, configuration is wrong: {e}"
            )
            return insert_query_settings

        # Get query usage
        query_memory_usage = int(query_finish_logs.get("memory_usage", 0))
        query_cpu_usage = int(query_finish_logs.get("cpu_usage", 0))

        if not query_memory_usage and not query_cpu_usage:
            logging.info(
                f"Populate ({job_id}) query using default settings, no need to optimize: memory and cpu query usage too low"
            )
            return insert_query_settings

        # Get clickhouse usage
        memory_available, cpu_available = ch_get_replica_load(database_server=database_server)

        if not memory_available and not cpu_available:
            logging.info(
                f"Populate ({job_id}) query using default settings, no need to optimize: not enough info on system.asynchronous_metrics"
            )
            return insert_query_settings

        # 1. Get current values
        current_max_insert_block_size = int(insert_query_settings.get("max_insert_block_size", max_insert_block_size))
        current_min_insert_block_size_bytes = int(
            insert_query_settings.get("min_insert_block_size_bytes", max_insert_block_size)
        )

        ch_max_insert_threads = ch_limits.get("max_insert_threads", Limit.ch_max_insert_threads)
        current_threads = int(insert_query_settings.get("max_insert_threads", ch_max_insert_threads))
        new_threads = current_threads

        # 2. Calculate memory bandwith. We request this on each query since it could have changed in Cheriff
        memory_available = int(MEMORY_PERCENTAGE * memory_available)

        # 3. Memory Thresholds
        is_memory_low_usage = query_memory_usage < memory_available * MIN_MEMORY_THRESHOLD
        is_memory_medium_usage = (
            query_memory_usage >= memory_available * MIN_MEMORY_THRESHOLD
            and query_memory_usage < memory_available * MAX_MEMORY_THRESHOLD
        )

        # 4. CPU thresholds
        is_cpu_low_usage = query_cpu_usage < cpu_available * MIN_CPU_THRESHOLD
        is_cpu_medium_usage = (
            query_cpu_usage >= cpu_available * MIN_CPU_THRESHOLD and query_cpu_usage < cpu_available * MAX_CPU_THRESHOLD
        )

        # 5. Update threads if necessary. Leave space for background merges if new_threads is > than cpu_available / 2
        if is_cpu_low_usage and is_memory_low_usage:
            new_threads = min(current_threads + 4, int(cpu_available / 2))
        elif is_memory_medium_usage and (is_cpu_low_usage or is_cpu_medium_usage):
            new_threads = min(current_threads + 2, int(cpu_available / 2))

        # 6. Update block size differently depending on memory
        if is_memory_low_usage:
            memory_to_use = memory_available * MIN_MEMORY_THRESHOLD
            new_max_insert_block_size = int((memory_to_use / (2 * new_threads)) / 256) * 10
            new_min_insert_block_size_bytes = int(memory_to_use / (2 * new_threads))
        elif is_memory_medium_usage:
            memory_to_use = query_memory_usage
            new_max_insert_block_size = int((memory_to_use / (4 * new_threads)) / 256) * 10
            new_min_insert_block_size_bytes = int(memory_to_use / (4 * new_threads))
        else:
            new_max_insert_block_size = current_max_insert_block_size
            new_min_insert_block_size_bytes = current_min_insert_block_size_bytes

        # 7. Set settings
        insert_query_settings["max_insert_threads"] = new_threads
        insert_query_settings["max_threads"] = new_threads
        insert_query_settings["max_insert_block_size"] = new_max_insert_block_size
        insert_query_settings["min_insert_block_size_rows"] = 0  # rely on min_insert_block_size_bytes
        insert_query_settings["min_insert_block_size_bytes"] = new_min_insert_block_size_bytes
        insert_query_settings["preferred_block_size_bytes"] = new_min_insert_block_size_bytes

        logging.info(f"Populate ({job_id}) query using custom settings: settings = {insert_query_settings}")

        return insert_query_settings

    @staticmethod
    def update_insert_query_settings_after_memory_error(job_id: str) -> Job:
        # In case of a memory exception, we half all resources to mitigate it on the next try
        job = PopulateJob.get_by_id(job_id)
        if not job:
            raise PopulateException(f"Populate job {job_id} not found")

        insert_query_settings = job.insert_query_settings
        current_max_insert_block_size = int(
            insert_query_settings.get("max_insert_block_size", Limit.populate_max_insert_block_size)
        )
        new_max_insert_block_size = int(current_max_insert_block_size / 2)

        current_min_insert_block_size_bytes = int(
            insert_query_settings.get("min_insert_block_size_bytes", Limit.populate_max_insert_block_size)
        )
        new_min_insert_block_size_bytes = int(current_min_insert_block_size_bytes / 2)

        current_threads = int(insert_query_settings.get("max_insert_threads", Limit.ch_max_insert_threads))
        new_threads = int(current_threads / 2) if current_threads > 2 else 1

        insert_query_settings["max_insert_block_size"] = new_max_insert_block_size
        insert_query_settings["min_insert_block_size_bytes"] = new_min_insert_block_size_bytes
        insert_query_settings["preferred_block_size_bytes"] = new_min_insert_block_size_bytes
        insert_query_settings["min_insert_block_size_rows"] = 0
        insert_query_settings["max_insert_threads"] = new_threads
        insert_query_settings["max_threads"] = new_threads

        logging.info(
            f"Populate ({job_id}) query using new settings after memory error: settings = {insert_query_settings}"
        )

        return PopulateJob.update_insert_query_settings(job.id, insert_query_settings)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def update_insert_query_settings(job_id: str, insert_query_settings: Dict[str, Any]) -> Job:
        with Job.transaction(job_id) as job:
            job = cast("PopulateJob", job)
            job.insert_query_settings = insert_query_settings
            return job

    @staticmethod
    def get_database_servers(j: "PopulateJob") -> Tuple[List[str], "PopulateJob"]:
        u = j.user
        logger = j.getLogger()
        logger.info("started")

        table_details = ch_table_details(
            table_name=j.target_table, database_server=u.database_server, database=u.database
        )

        if not table_details:
            raise RuntimeError(f"Could not find target table '{j.target_table}'")

        use_old_populates = FeatureFlagsWorkspaceService.feature_for_id(
            FeatureFlagWorkspaces.USE_POPULATES_OLD, u.id, u.feature_flags
        )
        multiple_views_per_pipe_restricted = FeatureFlagsWorkspaceService.feature_for_id(
            FeatureFlagWorkspaces.PIPE_NODE_RESTRICTIONS, u.id, u.feature_flags
        )
        use_revamp = not use_old_populates and multiple_views_per_pipe_restricted
        use_pool_replica = (
            FeatureFlagsWorkspaceService.feature_for_id(
                FeatureFlagWorkspaces.POOL_REPLICA_FOR_POPULATES, u.id, u.feature_flags
            )
            and use_revamp
        )
        dedicated_database_servers = (
            get_pool_replicas() if use_pool_replica else get_clickhouse_replicas_for_populates(u)
        )
        database_servers = dedicated_database_servers if len(dedicated_database_servers) else [u.database_server]

        if not replicate_populate_manually(table_details, u):
            if use_revamp:
                try:
                    assert u.cluster is not None
                    destination_server = get_server_to_run_populate(
                        j.id,
                        j.database_server,
                        u.cluster,
                        database_servers,
                        j.insert_query_settings,
                        PopulateUserAgents.INTERNAL_POPULATE,
                        128,
                    )
                    logging.info(f"Populate {j.id} using destination server: {destination_server}")
                    database_servers = [destination_server]
                    j = PopulateJob.update_destination_server(j.id, destination_server)
                except CannotFindRandomReplica:
                    raise Exception(
                        "There was a problem while finding a Database Server to run the job. Please try again."
                    )
        else:
            # TODO can we remove this part of the code (?) it is to support Join Engine
            logger.info("Needs manual replication")
            # manually run insert query on every replica
            cluster = u.cluster
            source_table = ch_source_table_for_view_sync(u.database_server, u.database, j.view_node)
            assert isinstance(source_table, CHTableLocation)
            assert cluster is not None
            replicas = ch_get_replicas_for_table_sync(
                u.database_server, source_table.database, source_table.table, cluster
            )
            if not replicas:
                logger.info("table does not have replicas")
                # original table is not replicated so run just in current database
                replicas = [url_from_host(u.database_server)]
            database_servers = replicas
        return database_servers, j

    @staticmethod
    def populate(j: "PopulateJob") -> None:
        """
        populate a table with the view.
        It checks if the target table is replicated and runs in all of the replicas if it's not
        (mostly useful for Join tables)
        """
        logger = j.getLogger()
        logger.info(f"started with status={j.status}")

        def _run_job_on_replica(database_server: str) -> str:
            PopulateJob.run_populate_on_replica(database_server, j)
            return database_server

        # Even if the status was already `working`,
        # we want to re-enqueue the job in different internal queues.
        if j.status == JobStatus.WAITING:
            j.mark_as_working()

        database_servers, j = PopulateJob.get_database_servers(j)
        initial_insert_query_settings = j.get_initial_query_settings()
        PopulateJob.update_insert_query_settings(j.id, initial_insert_query_settings)

        with ThreadPoolExecutor(max_workers=len(database_servers)) as local_executor:
            try:
                logger.info(f"running populate job on {database_servers}")
                for database_server in local_executor.map(_run_job_on_replica, database_servers):
                    logger.info(f"finished database_server = {database_server}")

            except JobCancelledException as e:
                raise e

            except Exception as e:
                if isinstance(e, CHException) and e.code == CHErrors.TYPE_MISMATCH:
                    logger.warning(str(e))
                else:
                    logger.error("failed to run populate query")
                    logger.exception(e)
                raise e

        logger.info("done")

    @property
    def is_cancellable(self) -> bool:
        return self.status in {JobStatus.WAITING, JobStatus.WORKING}

    def get_dependent_databases(
        self, workspace, table_name, query_id
    ) -> Tuple[List[str], Set[Tuple[str, str]], Set[Tuple[str, str]]]:
        source_datasource = workspace.get_datasource(table_name, include_read_only=True)
        workspace_id = (
            source_datasource.original_workspace_id
            if hasattr(source_datasource, "original_workspace_id")
            else workspace.id
        )
        source_workspace = Workspace.get_by_id(workspace_id)
        dataflow_steps, _ = DataFlow.get_steps(
            source_workspace=source_workspace,
            source_datasource=source_datasource,
            initial_query_id=query_id,
            check_partition_keys=False,
            skip_incompatible_partitions=True,
        )

        dependent_materialized_views: Set[Tuple[str, str]] = set()
        dependent_data_sources: Set[Tuple[str, str]] = set()

        step_index = 0
        for step in dataflow_steps:
            if step.step_materialized_views:
                for step_mv in step.step_materialized_views:
                    # Do not create Materialized View from the source table in the original
                    # database to the Materialized Table in the auxiliary database table.
                    # This prevents newly inserted rows to the source table be propagated to
                    # the tables downstream and create duplicates when attaching partitions
                    # if step.step_workspace.database = 'database' and 'source_table.table_name'
                    if step_index == 0 and step_mv.node.materialized in source_datasource.tags.get(
                        "dependent_datasources", {}
                    ):
                        step_index += 1
                        continue

                    dependent_materialized_views.add((step.step_workspace.database, step_mv.node.id))
            if step.step_datasource:
                dependent_data_sources.add((step.step_workspace.database, step.step_datasource.id))
            step_index += 1

        return (
            list({step.step_workspace.database for step in dataflow_steps}),
            dependent_materialized_views,
            dependent_data_sources,
        )


def create_populate(
    user: Workspace,
    view_node: str,
    sql: str,
    target_table: str,
    pipe_id: Optional[str] = None,
    pipe_name: Optional[str] = None,
    pipe_url: Optional[str] = None,
    populate_subset: Optional[Any] = None,
    populate_condition: Optional[Any] = None,
    truncate: bool = False,
    unlink_on_populate_error: bool = False,
    request_id: str = "",
    branch_id: Optional[str] = None,
    check_first_population_on_error: Optional[bool] = True,
):
    j = PopulateJob(
        user=user,
        view_node=view_node,
        view_sql=sql,
        target_table=target_table,
        pipe_id=pipe_id,
        pipe_name=pipe_name,
        pipe_url=pipe_url,
        populate_subset=populate_subset,
        populate_condition=populate_condition,
        truncate=truncate,
        unlink_on_populate_error=unlink_on_populate_error,
        request_id=request_id,
        branch_id=branch_id,
        check_first_population_on_error=check_first_population_on_error,
    )
    j.save()
    j.send_raw_event()
    return j


async def new_populate_job(
    job_executor: JobExecutor,
    user: Workspace,
    view_node,
    sql: str,
    target_table: str,
    pipe_id: str,
    pipe_name: str,
    pipe_url: Optional[str] = None,
    populate_subset=None,
    populate_condition: Optional[str] = None,
    truncate: bool = False,
    source_table: Optional[CHTableLocation] = None,
    unlink_on_populate_error: bool = False,
    request_id: str = "",
    check_first_population_on_error: Optional[bool] = True,
) -> PopulateJob:
    try:
        await validate_populate_condition(user, view_node, populate_condition, source_table=source_table)
    except PopulateException as e:
        raise e
    j = create_populate(
        user=user,
        view_node=view_node,
        sql=sql,
        target_table=target_table,
        pipe_id=pipe_id,
        pipe_name=pipe_name,
        pipe_url=pipe_url,
        populate_subset=populate_subset,
        populate_condition=populate_condition,
        truncate=truncate,
        unlink_on_populate_error=unlink_on_populate_error,
        request_id=request_id,
        check_first_population_on_error=check_first_population_on_error,
    )
    logging.info(
        f"New populate job created: job_id={j.id}, user={user.id}, view_node={view_node}, sql={sql}, target_table={target_table}"
    )
    job_executor.put_job(j)
    try:
        workspace = user
        job = j
        target_ds = Workspaces.get_by_id(workspace.id).get_datasource(target_table)
        source_table = ch_source_table_for_view_sync(workspace.database_server, workspace.database, view_node)
        source_ds = None
        if source_table:
            source_ds = workspace.get_datasource(source_table.table)
        dot = tracker.DatasourceOpsTrackerRegistry.get()
        if dot and dot.is_alive:
            resource_tags: List[str] = []
            if workspace and target_ds:
                resource_tags = [tag.name for tag in workspace.get_tags_by_resource(target_ds.id, target_ds.name)]

            record = tracker.DatasourceOpsLogRecord(
                timestamp=job.created_at.replace(tzinfo=timezone.utc),
                event_type="populateview-queued",
                datasource_id=target_ds.id if target_ds else target_table,
                datasource_name=target_ds.name if target_ds else "unknown",
                user_id=workspace.id,
                # FIXME: Does it make sense to keep this? A workspace can have no email and some other places we just use the name.
                user_mail=workspace["email"] if "email" in workspace else workspace.name,  # noqa: SIM401
                result="ok",
                elapsed_time=(datetime.now(timezone.utc) - job.created_at.replace(tzinfo=timezone.utc)).total_seconds(),
                error="",
                request_id=job.request_id if job.request_id else job.id,
                import_id=job.id,
                job_id=job.id,
                rows=0,
                rows_quarantine=0,
                blocks_ids=[],
                Options__Names=list(["job", "trigger_datasource_id"]),
                Options__Values=list([json.dumps(job.to_json()), source_ds.id if source_ds else "unknown"]),
                pipe_id=job.pipe_id,
                pipe_name=job.pipe_name,
                read_rows=0,
                read_bytes=0,
                written_rows=0,
                written_bytes=0,
                written_rows_quarantine=0,
                written_bytes_quarantine=0,
                operation_id=job.id,
                release="",
                resource_tags=resource_tags,
            )
            rec = tracker.DatasourceOpsLogEntry(
                record=record,
                eta=datetime.now(timezone.utc),
                workspace=workspace,
                query_ids=[],
                query_ids_quarantine=[],
                view_name=job.view_node,
            )
            dot.submit(rec)
    except Exception as e:
        logging.exception(f"populateview-queued failed {str(e)}")
    return j


def get_populate_subset(populate_subset: Optional[str]) -> float:
    """
    >>> get_populate_subset('blabla')
    -1
    >>> get_populate_subset('-1')
    -1
    >>> get_populate_subset('2')
    -1
    >>> get_populate_subset(None)
    -1
    >>> get_populate_subset('0')
    -1
    >>> get_populate_subset('0.1')
    0.1
    >>> get_populate_subset('1')
    1.0
    >>> get_populate_subset(None)
    -1
    """

    if populate_subset is None:
        return -1

    try:
        value = float(populate_subset)
        if value > 0 and value <= 1:
            return value
        return -1
    except Exception:
        return -1


def convert_populatejob_to_rawevent(populate_job: "PopulateJob") -> RawEvent:
    metadata = PopulateJobMetadata(
        query_id=populate_job.query_id,
        pipe_name=populate_job.pipe_name,
        pipe_url=populate_job.pipe_url,
        populate_subset=populate_job.populate_subset,
        populate_condition=populate_job.populate_condition,
        backfill_condition=populate_job.backfill_condition,
        queries=[query.as_log_dict() for query in populate_job.queries],
    )

    job_error = (
        populate_job.result["error"]
        if populate_job.status == JobStatus.ERROR and "error" in populate_job.result
        else None
    )

    workspace_id_from_user = populate_job.user.id if populate_job.user else ""
    workspace_id_from_user_id = populate_job.user_id if populate_job.user_id else ""
    workspace_id = workspace_id_from_user or workspace_id_from_user_id

    populate_job_log = PopulateJobLog(
        job_id=populate_job.id,
        job_type="populate",
        status=JobStatusForLog(populate_job.status),
        error=job_error,
        pipe_id=populate_job.pipe_id,
        datasource_id=populate_job.target_table,
        created_at=populate_job.created_at,
        started_at=populate_job.started_at,
        updated_at=populate_job.updated_at,
        job_metadata=metadata,
    )

    return RawEvent(
        timestamp=datetime.now(timezone.utc),
        workspace_id=workspace_id,
        request_id=populate_job.request_id,
        event_type=EventType.POPULATE,
        event_data=populate_job_log,
    )


async def unlink_matview(workspace: Workspace, view_node: str) -> None:
    node = None
    pipe = None
    try:
        node = workspace.get_node(view_node)
        if not node:
            return

        pipe = workspace.get_pipe_by_node(node.id)

        if not pipe:
            return
    except Exception:
        pass

    node = await SharedUtils.NodeUtils.delete_node_materialized_view(workspace, node, force=True)

    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def save_meta(workspace, pipe, node):
        with Workspace.transaction(workspace.id) as w:
            w.update_node(pipe.id, node)
            return w

    save_meta(workspace, pipe, node)


unlink_matview_sync = async_to_sync(unlink_matview)


def replicate_populate_manually(table_details: TableDetails, workspace: Workspace) -> bool:
    if not workspace.clusters:
        return False
    return not table_details.is_replicated()


async def validate_populate_condition(
    workspace: Workspace, mv_id: str, populate_condition: Optional[str], source_table: Optional[CHTableLocation] = None
) -> None:
    try:
        if not populate_condition:
            return

        ds_name = ""
        if not source_table:
            source_table = await ch_source_table_for_view(workspace.database_server, workspace.database, mv_id)

        if source_table:
            ds = Workspaces.get_datasource(workspace, source_table.table)
            if ds:
                ds_name = ds.name

            query_with_populate_condition = f"""
                SELECT * FROM {source_table.database}.{source_table.table}
                WHERE {populate_condition}
            """

            replaced_sql, _ = await workspace.replace_tables_async(
                query_with_populate_condition,
                template_execution_results=TemplateExecutionResults(),
                allow_use_internal_tables=False,
                release_replacements=True,
            )

            await ch_explain_plan_query(workspace["database_server"], workspace["database"], replaced_sql)
    except Exception as e:
        raise PopulateException(
            f"Cannot apply SQL condition, make sure the syntax is valid and the condition can be applied to the {ds_name} Data Source: `{populate_condition}` - {str(e)}"
        ) from e


def build_partition_query(
    database_server: str,
    source_table: CHTableLocation,
    source_table_details: TableDetails,
    partition: Optional[str],
    limit: Optional[int],
    ttl: Optional[str],
    populate_condition: Optional[str] = None,
    backfill_condition: Optional[str] = None,
    column_names: Optional[str] = None,
) -> str:
    where_clause = ""
    if source_table_details and partition:
        where_clause = add_and_condition_to_where(where_clause, f"{source_table_details.partition_key} = {partition}")

    if ttl:
        where_clause = add_and_condition_to_where(where_clause, ttl)

    if backfill_condition:
        where_clause = add_and_condition_to_where(where_clause, backfill_condition)

    if populate_condition:
        where_clause = add_and_condition_to_where(where_clause, populate_condition)

    limit_clause = f" LIMIT {limit}" if limit else ""
    columns_str = column_names or "*"

    select_query = """
        SELECT {columns_str}
        FROM {database}.{table}
        {where_clause}
        {limit_clause}
    """
    select_query = select_query.format(
        columns_str=columns_str,
        database=source_table.database,
        table=source_table.table,
        limit_clause=limit_clause,
        where_clause=where_clause,
    )

    logging.info(f"SELECT_QUERY => {select_query}")

    try:
        ch_describe_query_sync(database_server, source_table.database, select_query, format="JSON")
    except Exception:
        # this is a fallback to remove the ttl expression
        where_clause = ""
        if source_table_details and partition:
            where_clause = add_and_condition_to_where(
                where_clause, f"{source_table_details.partition_key} = {partition}"
            )

        if populate_condition:
            where_clause = add_and_condition_to_where(where_clause, populate_condition)

        select_query = select_query.format(
            database=source_table.database,
            table=source_table.table,
            limit_clause=limit_clause,
            where_clause=where_clause,
        )
    return select_query


def add_and_condition_to_where(where_clause: Optional[str], condition: str) -> str:
    return f"{where_clause} AND {condition}" if where_clause else f" WHERE {condition}"


def get_server_to_run_populate(
    job_id: str,
    database_server: str,
    cluster: str,
    populate_servers: list[str],
    query_settings: Dict[str, Any],
    user_agent: str,
    max_threads_limit: int,
) -> str:
    if not populate_servers:
        populate_servers = [database_server]
    if len(populate_servers) > 1:
        try:
            return get_optimal_replica_based_on_load(
                job_id,
                database_server,
                cluster,
                populate_servers,
                query_settings,
                user_agent,
                max_threads_limit,
            )
        except CannotFindOptimalReplica:
            logging.warning(f"Populate: {job_id} could not find optimal replica, using a random one")
            get_random_clickhouse_replica(job_id, populate_servers, user_agent, query_settings)
    return get_random_clickhouse_replica(job_id, populate_servers, user_agent, query_settings)


def parse_thresholds(thresholds: Union[str, List[Optional[float]]]) -> List[Optional[float]]:
    if isinstance(thresholds, str):
        return json.loads(thresholds)
    return thresholds


def assert_no_mv_links_original_table_with_aux_database(
    database_server: str,
    original_table_id: CHTableLocation,
    destination_table_id: TableDetails,
    job_started_at: datetime | None,
):
    if not job_started_at:
        logging.info("Exception while checking MVs linking original table: No job started_at time")
        return

    job_start_time_str = job_started_at.strftime("%Y-%m-%d %H:%M:%S")
    query = f"""
    SELECT databases
    FROM system.query_log
    WHERE
        type > 1 AND
        event_date = today() AND
        event_time >= '{job_start_time_str}' AND
        event_time < '{job_start_time_str}' + INTERVAL 30 SECOND AND
        query_kind = 'Create' AND
        query LIKE 'CREATE MATERIALIZED VIEW IF NOT EXISTS%__populate_%' AND
        arrayExists(x -> match(x, '^(.*)INSERT(.*)ON {destination_table_id.database}.{destination_table_id.name}$'), used_privileges) AND
        arrayExists(x -> match(x, '^SELECT(.*)ON {original_table_id.database}.{original_table_id.table}$'), used_privileges)
    FORMAT JSON
    """

    try:
        client = HTTPClient(database_server)
        _, body = client.query_sync(query)
        json_response = orjson.loads(body)
    except Exception as e:
        # This is an accessory check for production
        # purposes. So it's not acceptable to raise any
        # exceptions due to anything failing here
        logging.info("Exception while checking MVs linking original table: %s", str(e))
        return

    databases: list[Dict[str, str]] = json_response.get("data", [])
    if len(databases) > 0:
        logging.info(
            "Materialized View linking Original Table and Populate Database has been created. Databases: %s", databases
        )
