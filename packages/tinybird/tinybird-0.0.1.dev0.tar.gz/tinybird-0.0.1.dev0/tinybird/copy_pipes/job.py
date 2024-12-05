import json
import logging
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, cast

import requests
import ulid

import tinybird.job as jobs
import tinybird.plan_limits.copy as PlanLimitsCopy
import tinybird.views.shared.utils as SharedUtils
from tinybird import tracker
from tinybird.ch import (
    MAX_EXECUTION_TIME,
    WAIT_ALTER_REPLICATION_OWN,
    CHReplication,
    TablesToSwap,
    ch_attach_partitions_sync,
    ch_create_table_as_table_sync,
    ch_drop_table_sync,
    ch_get_columns_from_query_sync,
    ch_guarded_query,
    ch_swap_tables_sync,
    ch_table_details,
    ch_table_partitions_sync,
)
from tinybird.ch_utils.exceptions import CHException
from tinybird.cluster import (
    CannotFindOptimalReplica,
    CannotFindRandomReplica,
    get_optimal_replica_based_on_load,
    get_random_clickhouse_replica,
)
from tinybird.constants import ExecutionTypes
from tinybird.copy_pipes.cluster import get_clickhouse_replicas_for_copy
from tinybird.copy_pipes.errors import CopyJobErrorMessages
from tinybird.data_connector import DataSink
from tinybird.dataflow import DataFlow, DataFlowStep
from tinybird.datasource import Datasource
from tinybird.feature_flags import FeatureFlagsWorkspaceService, FeatureFlagWorkspaces
from tinybird.gc_scheduler.sinks import pause_sink
from tinybird.limits import Limit, Limits
from tinybird.model import retry_transaction_in_case_of_concurrent_edition_error_sync
from tinybird.pipe import CopyModes, Pipe, PipeTypes
from tinybird.raw_events.definitions.base import JobExecutionType, JobStatus
from tinybird.raw_events.definitions.copy_log import CopyJobLog, CopyJobMetadata, JobProcessedData
from tinybird.raw_events.raw_events_batcher import EventType, RawEvent, raw_events_batcher
from tinybird.user import User as Workspace
from tinybird.user import Users as Workspaces
from tinybird.views.utils import validate_table_function_host
from tinybird_shared.clickhouse.errors import CHErrors

# We might need to revisit this timeout eventually
# This makes the ch_guarded_query http client to timeout while the query is still running in CH
# It allows job cancellation after this timeout
COPY_GUARDED_QUERY_TIMEOUT = 300


class CopyUserAgents:
    COPY_QUERY = "tb-copy-query"
    INTERNAL_COPY_QUERY = "no-tb-internal-copy-query"


class CopyJob(jobs.Job):
    def __init__(
        self,
        workspace: Workspace,
        sql: str,
        request_id: str,
        target_datasource: Datasource,
        mode: Optional[str] = CopyModes.APPEND,
        pipe: Optional[Pipe] = None,
        execution_type: Optional[str] = ExecutionTypes.MANUAL,
        target_workspace: Optional[Workspace] = None,
        copy_timestamp: Optional[datetime] = None,
        use_query_queue: bool = False,
        copy_server: Optional[str] = None,
        max_threads: Optional[int] = None,
        parameters: Optional[Dict[str, str]] = None,
        ch_params_keys: Optional[Set[str]] = None,
        is_table_function: Optional[bool] = False,
    ) -> None:
        force_nonatomic_append_mode = FeatureFlagsWorkspaceService.feature_for_id(
            FeatureFlagWorkspaces.FORCE_NONATOMIC_COPY, "", workspace.feature_flags
        )

        self.database_server: str = workspace.database_server
        self.destination_server_for_job: str | None = None
        self.database: str = workspace.database
        self.cluster: str = workspace.cluster if workspace.cluster else Workspace.default_cluster
        self.sql: str = sql
        self.query_id: str = ulid.new().str
        self.force_nonatomic_append_mode = force_nonatomic_append_mode
        self.execution_type = execution_type
        self.request_id: str = request_id
        self.pipe_id: str = pipe.id if pipe else ""
        self.pipe_name: str = pipe.name if pipe else ""
        self.workspace_id: str = workspace.id
        self.target_database: str = target_workspace.database if target_workspace else self.database
        self.target_workspace_id: str = target_workspace.id if target_workspace else workspace.id
        self.processed_data: Dict[str, int] = {
            "read_rows": 0,
            "read_bytes": 0,
            "written_rows": 0,
            "written_bytes": 0,
            "virtual_cpu_time_microseconds": 0,
        }
        self.dependent_datasources: Dict[str, Any] = {}
        self.max_threads = max_threads
        self.parameters = parameters
        self.mode = mode if mode and CopyModes.is_valid(mode) else CopyModes.APPEND
        self.ch_params_keys = ch_params_keys if ch_params_keys else set()
        self.is_table_function = is_table_function

        job_kind = jobs.JobKind.COPY
        if use_query_queue:
            job_kind = jobs.JobKind.COPY_MAIN
        if workspace.is_branch_or_release_from_branch:
            job_kind = jobs.JobKind.COPY_BRANCH

        jobs.Job.__init__(
            self,
            kind=job_kind,
            user=workspace,
            datasource=target_datasource,
        )

        self.__ttl__ = 3600 * int(
            workspace.get_limits(prefix="copy").get("copy_max_job_ttl_in_hours", Limit.copy_max_job_ttl_in_hours)
        )

        self.created_at: datetime = copy_timestamp if copy_timestamp else self.created_at

    @property
    def is_cancellable(self) -> bool:
        return self.status in [jobs.JobStatus.WAITING, jobs.JobStatus.WORKING]

    def __getstate__(self) -> Dict[str, Any]:
        """
        Method to be used during pickling to remove the job_executor or workspaces attributes
        >>> job = CopyJob(workspace=Workspace(), sql='select 1', request_id='123', target_datasource=Datasource(name='ds', _id='123'))
        >>> job.some_attribute = 'foo'
        >>> job.user, job.workspace, job.target_workspace = Workspace(), Workspace(), Workspace()
        >>> state = job.__getstate__()
        >>> assert 'user' not in state
        >>> assert state['some_attribute'] == 'foo'
        >>> assert 'workspace' not in state
        >>> assert 'target_workspace' not in state
        """
        state = super().__getstate__()
        if "workspace" in state:
            del state["workspace"]
        if "target_workspace" in state:
            del state["target_workspace"]
        return state

    def __setstate__(self, state: Dict[str, Any]) -> None:
        """
        >>> workspace = Workspace()
        >>> workspace.save()
        >>> # Test CopyJob with workspace_id stored in state but not workspace
        >>> job = CopyJob(workspace=workspace, sql='select 1', request_id='123', target_datasource=Datasource(name='ds', _id='123'))
        >>> job.__setstate__(job.__getstate__())
        >>> assert job.workspace_id == workspace.id == job.workspace.id
        >>> # Test CopyJob with workspace stored in state but not workspace_id
        >>> job = CopyJob(workspace=workspace, sql='select 1', request_id='123', target_datasource=Datasource(name='ds', _id='123'))
        >>> job.target_workspace = workspace
        >>> job.workspace = workspace
        >>> state = job.__dict__.copy()
        >>> del state['workspace_id']
        >>> del state['target_workspace_id']
        >>> job.__setstate__(state)
        >>> assert job.workspace_id == job.workspace.id
        >>> assert job.target_workspace_id == job.target_workspace.id
        """
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
        if "workspace_id" not in state and "workspace" in state:
            self.workspace_id = state["workspace"].id
            save_required = True
        if "target_workspace_id" not in state and "target_workspace" in state:
            self.target_workspace_id = state["target_workspace"].id
            save_required = True
        if save_required:
            self.save()

        if self.user_id is not None:
            self.user = Workspace.get_by_id(self.user_id)
        if self.target_workspace_id is not None:
            self.target_workspace = Workspace.get_by_id(self.target_workspace_id)
        if self.workspace_id is not None:
            self.workspace = Workspace.get_by_id(self.workspace_id)

    @staticmethod
    async def validate(
        sql: str,
        target_datasource: Datasource,
        workspace: "Workspace",
        app_settings: Dict[str, Any],
        target_workspace=None,
        is_table_function: bool = False,
        ch_params_keys: Optional[Set[str]] = None,
    ) -> None:
        ch_params = workspace.get_secrets_ch_params_by(ch_params_keys) if ch_params_keys else {}
        if is_table_function:
            try:
                await validate_table_function_host(sql, app_settings, ch_params=ch_params)
            except ValueError as e:
                logging.exception(e)
                raise SharedUtils.CopyException(str(e), status=400)
            except Exception as e:
                logging.exception(e)
                raise SharedUtils.CopyException("Invalid table function URL", status=400)

        try:
            await SharedUtils.SQLUtils.validate_query_columns_for_schema(
                sql=sql,
                datasource=target_datasource,
                workspace=target_workspace if target_workspace else workspace,
                ch_params=ch_params,
            )
        except CHException as e:
            if is_table_function and e.code in [CHErrors.TIMEOUT_EXCEEDED]:
                logging.warning(f"Timeout exceeded on validate query for table function, skipping: {e}")
                pass
            else:
                raise e

        workspace_max_jobs = PlanLimitsCopy.CopyLimits.max_active_copy_jobs.get_limit_for(workspace)
        if PlanLimitsCopy.CopyLimits.max_active_copy_jobs.has_reached_limit_in(
            workspace_max_jobs, {"workspace": workspace}
        ):
            raise SharedUtils.CopyException(
                f"You have reached the maximum number of copy jobs ({workspace_max_jobs}). ", status=403
            )

    def get_insert_sql(self, database: str, database_server: str, datasource_id: str, sql: str) -> str:
        ch_params = self.workspace.get_secrets_ch_params_by(self.ch_params_keys) if self.ch_params_keys else {}
        try:
            columns = ch_get_columns_from_query_sync(database_server, database, sql, ch_params=ch_params)
        except CHException as e:
            if hasattr(self, "is_table_function") and self.is_table_function and e.code in [CHErrors.TIMEOUT_EXCEEDED]:
                logging.warning(
                    f"Timeout exceeded on validate query for table function, fallback to get columns from source: {e}"
                )
                assert isinstance(self.datasource, Datasource)
                columns = ch_get_columns_from_query_sync(
                    database_server, database, f"SELECT * FROM {database}.{self.datasource.id}", ch_params=ch_params
                )
            else:
                raise e

        append_copy_sql = f"""
            INSERT INTO {database}.{datasource_id}
            (
                {','.join([f"`{c['name']}`" for c in columns])}
            )
            {sql}
        """
        return append_copy_sql

    def create_step_aux_table(
        self,
        datasource: Datasource,
        workspace: Workspace,
        aux_table_id: str,
        database_server: str,
        exception_function: str,
        cluster: Optional[str] = None,
    ) -> str:
        exception_function = "ch_table_details"
        table_details = ch_table_details(
            datasource.id,
            database_server,
            workspace.database,
            user_agent=CopyUserAgents.INTERNAL_COPY_QUERY,
            query_settings=self.query_settings(),
        )
        settings = {**workspace.ddl_parameters(skip_replica_down=cluster is not None), **self.query_settings()}
        exception_function = "ch_create_table_as_table_sync"
        ch_create_table_as_table_sync(
            database_server=database_server,
            database=workspace.database,
            table_name=aux_table_id,
            as_table_name=datasource.id,
            engine=table_details.engine_full,
            not_exists=True,
            user_agent=CopyUserAgents.INTERNAL_COPY_QUERY,
            cluster=cluster,
            **settings,
        )
        return exception_function

    def get_aux_copy_datasource_id_from_step(self, step: DataFlowStep, index: str = "0"):
        return f"{step.step_datasource.id}_aux_copy_{step.step_id}_{index}"

    def to_json(self, workspace: Optional[Workspace] = None, debug: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        job = super().to_json(workspace, debug)
        job.update(
            {
                "query_id": self.query_id,
                "query_sql": " ".join(self.sql.split()),
                "dependent_datasources": self.dependent_datasources,
                "processed_data": self.processed_data,
                "execution_type": self.execution_type,
                "mode": self.mode,
            }
        )

        if hasattr(self, "parameters") and self.parameters:
            job["parameters"] = self.parameters
        if self.pipe_id:
            job["pipe_id"] = self.pipe_id
        if self.pipe_name:
            job["pipe_name"] = self.pipe_name
        if self.status == jobs.JobStatus.ERROR and "error" in self.result:
            job["error"] = self.result["error"]
        if self.force_nonatomic_append_mode:
            job["forced_nonatomic"] = self.force_nonatomic_append_mode

        return job

    @classmethod
    def run_append_copy_job(cls, job: jobs.Job) -> None:
        job = cast("CopyJob", job)

        try:
            cls.run_append_copy(job)
        except jobs.JobCancelledException:
            job = cast("CopyJob", job.mark_as_cancelled())
            job.track()
        except Exception as e:
            error = str(e)
            job = cast("CopyJob", job.mark_as_error({"error": error}))
            job.track(error=error)
        else:
            job = cast("CopyJob", job.mark_as_done({}, None))
            job.track()

    @classmethod
    def run_atomic_copy_job(cls, job: jobs.Job) -> None:
        job = cast("CopyJob", job)
        dataflow_steps = None
        try:
            assert isinstance(job.datasource, Datasource)
            source_pipe = job.workspace.get_pipe(job.pipe_id)

            dataflow_steps, dataflow_skipped_steps = DataFlow.get_steps(
                source_workspace=job.target_workspace,
                source_datasource=job.datasource,
                source_pipe=source_pipe,
                source_sql=job.sql,
                check_partition_keys=False,
                initial_query_id=job.query_id,
            )
            cls.run_atomic_copy_cascade(job, dataflow_steps, dataflow_skipped_steps)
        except jobs.JobCancelledException:
            job = cast("CopyJob", job.mark_as_cancelled())
            job.track_steps(dataflow_steps)
        except AttributeError as e:
            logging.error(f"Error in Copy Job with ID '{job.id}' for workspace '{job.workspace_id}': {e}")
            error_message = CopyJobErrorMessages.internal
            job = cast("CopyJob", job.mark_as_error({"error": error_message}))
            job.track(error=error_message)
        except Exception as e:
            error = str(e)
            job = cast("CopyJob", job.mark_as_error({"error": error}))
            job.track(error=error)
        else:
            job = cast("CopyJob", job.mark_as_done({}, None))
            job.track_steps(dataflow_steps)

    def run(self) -> "CopyJob":
        # Check whether source_pipe is COPY and if it's not
        # redirect the job to the append mode to support
        # /sql_copy endpoint temporarily
        source_pipe = self.workspace.get_pipe(self.pipe_id)

        if self.mode and not CopyModes.is_valid(self.mode):
            logging.exception(f"copy job mode not supported {self.mode}")
            return self

        if self.mode == CopyModes.REPLACE:
            self.job_executor.submit(CopyJob.run_atomic_copy_job, self)
            return self

        if not source_pipe or (source_pipe and source_pipe.pipe_type != PipeTypes.COPY):
            self.job_executor.submit(CopyJob.run_append_copy_job, self)
            return self

        if self.force_nonatomic_append_mode:
            self.job_executor.submit(CopyJob.run_append_copy_job, self)
        else:
            self.job_executor.submit(CopyJob.run_atomic_copy_job, self)

        return self

    def track(self, error: Optional[str] = None) -> None:
        elapsed_time = (datetime.now(timezone.utc) - self.created_at.replace(tzinfo=timezone.utc)).total_seconds()

        pipe_id = self.pipe_id if hasattr(self, "pipe_id") else ""
        pipe_name = self.pipe_name if hasattr(self, "pipe_name") else ""

        assert isinstance(self.datasource, Datasource)
        assert isinstance(self.target_workspace, Workspace)

        resource_tags: List[str] = []
        if self.target_workspace:
            resource_tags = [
                tag.name for tag in self.target_workspace.get_tags_by_resource(self.datasource.id, self.datasource.name)
            ]

        self.create_record_to_log(
            error,
            datasource={"id": self.datasource.id, "name": self.datasource.name},
            elapsed_time=elapsed_time,
            pipe={"name": pipe_name, "id": pipe_id},
            processed_data=self.processed_data,
            status=self.status,
            workspace={
                "id": self.target_workspace.id,
                # FIXME: Does it make sense to keep this? A workspace can have no email and some other places we just use the name.
                "name": self.target_workspace["email"]  # noqa: SIM401
                if "email" in self.target_workspace
                else self.target_workspace.name,
            },
            resource_tags=resource_tags,
        )

    def track_steps(self, dataflow_steps: Optional[List[DataFlowStep]], error: Optional[str] = None) -> None:
        if not dataflow_steps:
            logging.warning(f"No dataflow steps found for job {self.id}. Skipping tracking.")
            return

        if hasattr(self, "dependent_datasources") and self.dependent_datasources:
            steps = self.dependent_datasources.get("steps")
            assert isinstance(steps, list)
            for step in steps:
                step_pipe = step.get("pipes", [])[0]
                step_datasource = step.get("datasource")
                step_workspace = step.get("workspace")
                step_status = step.get("status")
                step_processed_data = step.get("processed_data")
                step_elapsed_time = step.get("elapsed_time", 0)

                resource_tags: List[str] = []
                try:
                    if workspace := Workspaces.get_by_id(step_workspace.get("id", "")):
                        resource_tags = [
                            tag.name
                            for tag in workspace.get_tags_by_resource(
                                step_datasource.get("id", ""), step_datasource.get("name", "")
                            )
                        ]
                except Exception:
                    logging.warning(f"Error retrieving tags for job {self.id}")

                self.create_record_to_log(
                    error,
                    step_datasource,
                    step_elapsed_time,
                    step_pipe,
                    step_processed_data,
                    step_status,
                    step_workspace,
                    resource_tags=resource_tags,
                )
        else:
            warn_msg = f"No dependent datasources found for job {self.id}."
            logging.warning(warn_msg)

    def create_record_to_log(
        self,
        error,
        datasource: Dict[str, str],
        elapsed_time,
        pipe: Dict[str, str],
        processed_data: Dict[str, int],
        status,
        workspace: Dict[str, str],
        resource_tags: List[str],
    ):
        tracker_registry = tracker.DatasourceOpsTrackerRegistry.get()
        if not tracker_registry or not tracker_registry.is_alive:
            logging.warning("DatasourceOpsTrackerRegistry is dead")
            return
        try:
            result = "ok"
            if self.status == jobs.JobStatus.ERROR:
                result = "error"
            elif self.status == jobs.JobStatus.CANCELLED:
                result = "cancelled"
            mode = self.mode if self.mode else CopyModes.APPEND

            record = tracker.DatasourceOpsLogRecord(
                timestamp=self.created_at.replace(tzinfo=timezone.utc),
                event_type=jobs.JobKind.COPY,
                datasource_id=datasource.get("id", ""),
                datasource_name=datasource.get("name", ""),
                user_id=workspace.get("id", ""),
                user_mail=workspace.get("name", ""),
                result=result,
                elapsed_time=elapsed_time,
                error=error if self.status == jobs.JobStatus.ERROR and error else "",
                request_id=self.request_id if self.request_id else self.id,
                import_id=self.id,
                job_id=self.id,
                rows=processed_data.get("written_rows", 0) if processed_data else 0,
                rows_quarantine=0,
                blocks_ids=[],
                Options__Names=list(["job", "execution_type", "mode"]),
                Options__Values=list(
                    [
                        json.dumps(self.to_json()),
                        self.execution_type if self.execution_type else ExecutionTypes.MANUAL,
                        mode,
                    ]
                ),
                pipe_id=pipe.get("id", ""),
                pipe_name=pipe.get("name", ""),
                read_rows=processed_data.get("read_rows", 0) if processed_data else 0,
                read_bytes=processed_data.get("read_bytes", 0) if processed_data else 0,
                written_rows=processed_data.get("written_rows", 0) if processed_data else 0,
                written_bytes=processed_data.get("written_bytes", 0) if processed_data else 0,
                written_rows_quarantine=0,
                written_bytes_quarantine=0,
                operation_id=self.id,
                release="",
                cpu_time=(
                    float(processed_data.get("virtual_cpu_time_microseconds", 0) / 1_000_000) if processed_data else 0
                ),
                resource_tags=resource_tags,
            )

            entry = tracker.DatasourceOpsLogEntry(
                record=record,
                eta=datetime.now(timezone.utc),
                workspace=self.target_workspace,
                query_ids=[],
                query_ids_quarantine=[],
            )
            tracker_registry.submit(entry)
        except Exception as e:
            logging.exception(str(e))
        logging.info(f"Log for copy job '{self.id}' submitted to tracker.")

    def query_settings(self) -> Dict[str, Any]:
        query_settings = {"log_comment": self._generate_log_comment()}
        return query_settings

    def insert_query_settings(self) -> Dict[str, Any]:
        workspace = Workspace.get_by_id(self.workspace_id)
        max_insert_threads = workspace.get_limits(prefix="copy").get(
            "copy_max_insert_threads", Limit.ch_max_insert_threads
        )
        max_execution_time = PlanLimitsCopy.CopyLimits.max_job_execution_time.get_limit_for(workspace, self)
        max_result_bytes = workspace.get_limits(prefix="ch").get("max_result_bytes", Limit.ch_max_result_bytes)
        join_algorithm = workspace.get_limits(prefix="copy").get("copy_join_algorithm", Limit.copy_join_algorithm)

        workspace_max_threads = workspace.get_limits(prefix="copy").get("copy_max_threads")
        max_threads = (
            Limits.max_threads(
                workspace=workspace_max_threads, endpoint_cheriff=None, request=None, template=self.max_threads
            )
            or Limit.ch_max_threads
        )

        settings = {
            "max_execution_time": max_execution_time,
            "max_insert_threads": max_insert_threads,
            "max_threads": max_threads,
            "max_result_bytes": max_result_bytes,
            "join_algorithm": join_algorithm,
            **self.query_settings(),
        }

        # max_memory_usage limit is only applied if they are explicitly set in Cheriff.
        # Server limits are applied otherwise
        general_max_memory_usage = workspace.get_limits(prefix="ch").get("max_memory_usage")
        copy_max_memory_usage = workspace.get_limits(prefix="copy").get("copy_max_memory_usage")
        if max_memory_usage := copy_max_memory_usage or general_max_memory_usage:
            settings["max_memory_usage"] = max_memory_usage

        if max_bytes_before_external_group_by := workspace.get_limits(prefix="copy").get(
            "copy_max_bytes_before_external_group_by"
        ):
            settings["max_bytes_before_external_group_by"] = max_bytes_before_external_group_by

        return settings

    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def _update_job_processed_data(self, processed_data: Dict[str, int]) -> None:
        with jobs.Job.transaction(self.id) as thejob:
            if hasattr(thejob, "processed_data"):
                thejob.processed_data.update(processed_data)

    def run_append_copy(j: "CopyJob") -> None:
        j.mark_as_working()
        assert isinstance(j.datasource, Datasource)

        query = j.get_insert_sql(
            database=j.target_workspace.database,
            database_server=j.database_server,
            datasource_id=j.datasource.id,
            sql=j.sql,
        )

        ch_params = j.workspace.get_secrets_ch_params_by(j.ch_params_keys) if j.ch_params_keys else {}
        try:
            _query_id, query_response = ch_guarded_query(
                database_server=j.database_server,
                database=j.target_workspace.database,
                query=query,
                cluster=j.cluster,
                query_id=j.query_id,
                user_agent=CopyUserAgents.COPY_QUERY,
                retries=False,
                **j.insert_query_settings(),
                **ch_params,  # type: ignore
            )
        except CHException as e:
            j._update_job_processed_data(json.loads(e.headers.get("X-Clickhouse-Summary", "{}")))
            raise e

        if isinstance(query_response, dict) and query_response.keys() >= j.processed_data.keys():
            processed_data: Dict[str, int] = {key: int(query_response.get(key, 0)) for key in j.processed_data.keys()}
        else:
            logging.warning("no processed data found in copy job")
            processed_data = j.processed_data
        j._update_job_processed_data(processed_data)

    def has_been_externally_cancelled_function_generator(self) -> Callable[[], bool]:
        def has_been_cancelled() -> bool:
            job = jobs.Job.get_by_id(self.id)
            return job is not None and job.status == jobs.JobStatus.CANCELLING

        return has_been_cancelled

    def run_atomic_copy_cascade(
        j: "CopyJob", dataflow_steps: List[DataFlowStep], dataflow_skipped_steps: List[DataFlowStep]
    ):
        job_reporter = jobs.DataFlowJobReporter(j.id)
        logger = j.getLogger()

        has_been_externally_cancelled = j.has_been_externally_cancelled_function_generator()

        if has_been_externally_cancelled() or j.status == jobs.JobStatus.CANCELLED:
            raise jobs.JobCancelledException()

        if j.status == jobs.JobStatus.WAITING:
            j.mark_as_working()
        logger.info(f"atomic copy job started with status={j.status}")

        job_reporter.add_steps(dataflow_steps)
        job_reporter.add_skipped_steps(dataflow_skipped_steps)

        # PRE: initial copy replacements
        extra_replacements = {}
        for _, step in enumerate(dataflow_steps):
            if step.step_copy:
                aux_copy_table_id = j.get_aux_copy_datasource_id_from_step(step)
                extra_replacements.update(
                    {
                        (step.step_workspace.database, step.step_datasource.id): (
                            step.step_workspace.database,
                            aux_copy_table_id,
                        )
                    }
                )

        last_executed_step_index = 0

        processed_data: Optional[Dict[str, Any]] = {}
        start_time = None

        copy_replicas = get_clickhouse_replicas_for_copy(j.workspace)
        max_threads_limit = j.workspace.get_limits("copy").get(
            "copy_max_threads_query_limit_per_replica", Limit.copy_max_threads_query_limit_per_replica
        )
        try:
            # we query the database server we will use to run the copy
            # we will not use varnish, but the database server directly
            j.destination_server_for_job = get_server_to_run_copy(
                j.id,
                j.database_server,
                j.cluster,
                copy_replicas,
                j.insert_query_settings(),
                CopyUserAgents.INTERNAL_COPY_QUERY,
                max_threads_limit,
            )
        except CannotFindRandomReplica:
            raise SharedUtils.CopyException(
                "There was a problem while finding a Database Server to run the job. Please try again."
            )

        try:
            groups_tables_to_swap: List[TablesToSwap] = []
            # MAIN: step by step atomic copies
            for step_index, step in enumerate(dataflow_steps):
                try:
                    sql = ""
                    last_executed_step_index = step_index
                    last_mv_index = 0
                    start_time = datetime.now(timezone.utc)

                    job_reporter.change_step_status(step_index, jobs.JobStatus.WORKING)
                    j.send_raw_event()

                    if step.step_materialized_views:
                        processed_data = {}

                        for index, step_materialized_view in enumerate(step.step_materialized_views):
                            try:
                                last_mv_index = index
                                job_reporter.change_step_pipe_status(step_index, index, jobs.JobStatus.WORKING)
                                j.send_raw_event()

                                pipe = step_materialized_view.pipe
                                # NOTE: we only one materialized view per pipe, this is a temp solution to have backwards compatibility with some old users
                                query_id = step.step_query_id if index == 0 else None  # FIXME

                                aux_copy_table_id = j.get_aux_copy_datasource_id_from_step(
                                    step, index=f"{step_index}{index}"
                                )
                                extra_replacements.update(
                                    {
                                        (step.step_workspace.database, step_materialized_view.datasource_id): (
                                            step.step_workspace.database,
                                            aux_copy_table_id,
                                        )
                                    }
                                )

                                sql = Workspaces.replace_tables(
                                    step.step_workspace,
                                    step_materialized_view.node.sql,
                                    pipe=pipe,
                                    use_pipe_nodes=True,
                                    extra_replacements=extra_replacements,
                                    release_replacements=True,
                                    function_allow_list=j.workspace.allowed_table_functions(),
                                )
                                view_processed_data, tables_to_swap = j._run_copy_step(
                                    workspace=step.step_workspace,
                                    datasource=step.step_datasource,
                                    sql=sql,
                                    query_id=query_id,
                                    database_server=j.destination_server_for_job,
                                    aux_table_id=aux_copy_table_id,
                                    has_been_externally_cancelled=has_been_externally_cancelled,
                                    mode=j.mode,
                                    cluster=None if j.mode == CopyModes.APPEND else j.cluster,
                                )
                                if tables_to_swap:
                                    groups_tables_to_swap.append(tables_to_swap)

                                if view_processed_data:
                                    processed_data = {
                                        "read_rows": int(processed_data.get("read_rows", 0))
                                        + int(view_processed_data.get("read_rows", 0)),
                                        "read_bytes": int(processed_data.get("read_bytes", 0))
                                        + int(view_processed_data.get("read_bytes", 0)),
                                        "written_rows": int(processed_data.get("written_rows", 0))
                                        + int(view_processed_data.get("written_rows", 0)),
                                        "written_bytes": int(processed_data.get("written_bytes", 0))
                                        + int(view_processed_data.get("written_bytes", 0)),
                                        "virtual_cpu_time_microseconds": int(
                                            processed_data.get("virtual_cpu_time_microseconds", 0)
                                        )
                                        + int(view_processed_data.get("virtual_cpu_time_microseconds", 0)),
                                    }
                                job_reporter.change_step_pipe_status(step_index, index, jobs.JobStatus.DONE)
                                j.send_raw_event()
                            except jobs.JobCancelledException:
                                job_reporter.change_step_pipe_status(step_index, index, jobs.JobStatus.CANCELLED)
                                j.send_raw_event()
                                raise jobs.JobCancelledException()
                    elif step.step_copy:
                        pipe = step.step_copy.pipe
                        aux_copy_table_id = j.get_aux_copy_datasource_id_from_step(step)
                        extra_replacements.update(
                            {
                                (step.step_workspace.database, step.step_datasource.id): (
                                    step.step_workspace.database,
                                    aux_copy_table_id,
                                )
                            }
                        )

                        if not step.step_copy.sql:
                            copy_node = pipe.get_copy_node()
                            sql = Workspaces.replace_tables(
                                step.step_workspace,
                                copy_node.sql,
                                pipe=pipe,
                                use_pipe_nodes=True,
                                extra_replacements=extra_replacements,
                                release_replacements=True,
                                function_allow_list=j.workspace.allowed_table_functions(),
                            )
                        else:
                            sql = step.step_copy.sql

                        processed_data, tables_to_swap = j._run_copy_step(
                            workspace=step.step_workspace,
                            datasource=step.step_datasource,
                            sql=sql,
                            query_id=step.step_query_id,
                            database_server=j.destination_server_for_job,
                            aux_table_id=aux_copy_table_id,
                            has_been_externally_cancelled=has_been_externally_cancelled,
                            mode=j.mode,
                            cluster=None if j.mode == CopyModes.APPEND else j.cluster,
                        )
                        if tables_to_swap:
                            groups_tables_to_swap.append(tables_to_swap)

                        job_reporter.change_step_pipe_status(step_index, 0, jobs.JobStatus.DONE)
                        j.send_raw_event()

                    job_reporter.change_step_status(step_index, jobs.JobStatus.DONE)
                    j.send_raw_event()
                except jobs.JobCancelledException:
                    job_reporter.change_step_pipe_status(step_index, 0, jobs.JobStatus.CANCELLED)
                    job_reporter.change_step_status(step_index, jobs.JobStatus.CANCELLED)
                    raise jobs.JobCancelledException()
                except Exception as e:
                    job_reporter.change_step_status(step_index, jobs.JobStatus.ERROR)
                    job_reporter.change_step_pipe_status(step_index, last_mv_index, jobs.JobStatus.ERROR)
                    if hasattr(e, "processed_data"):
                        processed_data = e.processed_data
                    logging.warning(
                        f"There was a problem while copying data: {step.step_workspace.name}.{step.step_datasource.name}: {e}"
                    )
                    raise SharedUtils.CopyException(e)
                finally:
                    if start_time:
                        elapsed_time = (datetime.now(timezone.utc) - start_time).total_seconds()
                        job_reporter.change_elapsed_time(step_index, elapsed_time)
                    if processed_data:
                        job_reporter.change_processed_data(step_index, processed_data)
        except Exception as e:
            raise e
        finally:
            if len(groups_tables_to_swap):
                max_wait_for_replication_seconds = j.workspace.get_limits(prefix="ch").get(
                    "max_wait_for_replication_seconds", Limit.ch_max_wait_for_replication_seconds
                )
                for table_to_swap in groups_tables_to_swap:
                    replication_success = CHReplication.ch_wait_for_replication_sync(
                        j.destination_server_for_job,
                        j.cluster,
                        j.database,
                        table_to_swap.new_table,
                        wait=max_wait_for_replication_seconds,
                    )

                    if not replication_success:
                        error_message = f"Failed to wait for replication in table {j.workspace.database}.{table_to_swap.new_table} when copy with replace"
                        logging.error(error_message)
                        raise SharedUtils.CopyException(
                            "Unexpected error, please retry or contact us at support@tinybird.co"
                        )

                ch_swap_tables_sync(
                    j.destination_server_for_job,
                    groups_tables_to_swap,
                    j.cluster,
                    user_agent=CopyUserAgents.INTERNAL_COPY_QUERY,
                    **j.query_settings(),
                    **j.user.ddl_parameters(skip_replica_down=True),
                )
                logging.info(f"Swapped tables: {groups_tables_to_swap}")
            for step_index, step in enumerate(dataflow_steps):
                is_last_step = step_index == len(dataflow_steps) - 1
                j._remove_aux_copy_tables(
                    j.destination_server_for_job,
                    job_reporter,
                    step_index,
                    step,
                    is_last_step,
                    last_executed_step_index,
                    cluster=None if j.mode == CopyModes.APPEND else j.cluster,
                )
        logger.info("atomic copy job done")
        job_reporter.mark_as_done()
        return job_reporter.get_processed_data()

    def _run_copy_step(
        self,
        workspace: Workspace,
        datasource: Datasource,
        sql: str,
        aux_table_id: str,
        query_id: Optional[str],
        database_server: str,
        has_been_externally_cancelled: Optional[Callable[[], bool]],
        mode: Optional[str] = CopyModes.APPEND,
        cluster: Optional[str] = None,
    ) -> Tuple[Optional[Dict[str, Any]], Optional[TablesToSwap]]:
        processed_data: dict = {
            "read_rows": 0,
            "read_bytes": 0,
            "written_rows": 0,
            "written_bytes": 0,
            "virtual_cpu_time_microseconds": 0,
        }
        query_id = query_id or ulid.new().str
        exception: Optional[Exception] = None
        exception_function = ""
        timeout = MAX_EXECUTION_TIME
        tables_to_swap: Optional[TablesToSwap] = None

        try:
            exception_function = "ch_get_columns_from_query_sync"
            query = self.get_insert_sql(
                database=workspace.database,
                database_server=database_server,
                datasource_id=aux_table_id,
                sql=sql,
            )

            # 1. Create temp target duplicate
            exception_function = self.create_step_aux_table(
                datasource, workspace, aux_table_id, database_server, exception_function, cluster=cluster
            )

            # 2. Guarded query append on target_duplicate
            exception_function = "ch_guarded_query"
            query_settings = self.insert_query_settings()
            timeout = query_settings.get("max_execution_time", MAX_EXECUTION_TIME)
            ch_params = workspace.get_secrets_ch_params_by(self.ch_params_keys) if self.ch_params_keys else {}
            _query_id, query_response = ch_guarded_query(
                database_server=database_server,
                database=workspace.database,
                query=query,
                cluster=cluster,
                query_id=query_id,
                user_agent=CopyUserAgents.COPY_QUERY,
                timeout=COPY_GUARDED_QUERY_TIMEOUT,
                has_been_externally_cancelled=has_been_externally_cancelled,
                backend_hint=self.id,
                disable_upstream_fallback=True,
                retries=False,
                **{**query_settings, **ch_params},
            )

            # 3. Check if the job has been cancelled externally
            if has_been_externally_cancelled and has_been_externally_cancelled():
                raise jobs.JobCancelledException()

            if mode == CopyModes.APPEND:
                # 4. When it finishes, attach partitions
                exception_function = "ch_table_partitions_sync"
                query_settings = self.query_settings()
                timeout = query_settings.get("max_execution_time", MAX_EXECUTION_TIME)
                partitions = ch_table_partitions_sync(
                    database_server=database_server,
                    database_name=workspace.database,
                    table_names=[aux_table_id],
                    backend_hint=self.id,
                    disable_upstream_fallback=True,
                    user_agent=CopyUserAgents.INTERNAL_COPY_QUERY,
                    query_settings=query_settings,
                )

                if partitions:
                    settings = {
                        **self.query_settings(),
                        "max_execution_time": self.insert_query_settings().get(
                            "max_execution_time", MAX_EXECUTION_TIME
                        ),
                    }
                    exception_function = "ch_attach_partitions_sync"
                    timeout = settings.get("max_execution_time", MAX_EXECUTION_TIME)
                    ch_attach_partitions_sync(
                        database_server,
                        workspace.database,
                        destination_table=datasource.id,
                        origin_table=aux_table_id,
                        partitions=partitions,
                        wait_setting=WAIT_ALTER_REPLICATION_OWN,
                        backend_hint=self.id,
                        disable_upstream_fallback=True,
                        user_agent=CopyUserAgents.INTERNAL_COPY_QUERY,
                        query_settings=settings,
                    )
            else:
                # 5. We'll exchange tables once all copy steps finish
                tables_to_swap = TablesToSwap(workspace.database, datasource.id, aux_table_id)

            if isinstance(query_response, dict) and query_response.keys() >= processed_data.keys():
                return {key: int(query_response.get(key, 0)) for key in processed_data.keys()}, tables_to_swap
            else:
                logging.warning("no processed data found in copy job")
                return processed_data, tables_to_swap

        except CHException as e:
            exception = e
            if e.code in [CHErrors.TIMEOUT_EXCEEDED, CHErrors.UNFINISHED, CHErrors.NETWORK_ERROR]:
                error_message = (
                    CopyJobErrorMessages.timeout_backfill.format(timeout_seconds=timeout)
                    if workspace.is_branch_or_release_from_branch or workspace.is_release
                    else CopyJobErrorMessages.timeout.format(timeout_seconds=timeout)
                )
                processed_data = json.loads(e.headers.get("X-Clickhouse-Summary", "{}"))
                raise SharedUtils.CopyException(error_message, processed_data=processed_data)
            actionable_error: bool = exception_function in [
                "ch_guarded_query",
                "ch_create_table_as_table_sync",
                "ch_get_columns_from_query_sync",
            ]
            # If the copy job has cancelled, let's just raise a JobCancelledException
            # When we cancel a copy job, the KILL QUERY might raise a timeout exception if the query is still running. Let's ignore it.
            if actionable_error and has_been_externally_cancelled and has_been_externally_cancelled():
                logging.warning(
                    f"Job {self.id} has been externally cancelled. So, we are ignoring the exception raised by {exception_function} raised an exception: {e}"
                )
                raise jobs.JobCancelledException()
            elif actionable_error:
                processed_data = json.loads(e.headers.get("X-Clickhouse-Summary", "{}"))
                raise SharedUtils.CopyException(
                    f"There was a problem while copying data: {e}", processed_data=processed_data
                )
            else:
                raise SharedUtils.CopyException(CopyJobErrorMessages.generic)
        except requests.exceptions.ReadTimeout as e:
            exception = e
            raise SharedUtils.CopyException(CopyJobErrorMessages.timeout.format(timeout_seconds=timeout))
        except jobs.JobCancelledException as e:
            exception = e
            raise e
        except SharedUtils.CopyException as e:
            exception = e
            raise e
        except Exception as e:
            exception = e
            raise SharedUtils.CopyException(f"There was a problem while copying data: {e}")
        finally:
            if exception and not isinstance(exception, jobs.JobCancelledException):
                logging.warning(
                    f"[CopyException] There was a problem while copying data in function {exception_function}: {exception} (job_id={self.id} workspace={workspace.id} database={workspace.database} workspace_name={workspace.name} datasource={datasource.id} datasource_name={datasource.name} aux_table_id={aux_table_id})"
                )

    def _remove_aux_copy_tables(
        self,
        job_database_server: str,
        job_reporter: jobs.DataFlowJobReporter,
        step_index: int,
        step: DataFlowStep,
        is_last_step: bool,
        last_executed_step_index: int = 0,
        cluster: Optional[str] = None,
    ) -> None:
        if step_index > last_executed_step_index:
            job_reporter.change_step_status(step_index, jobs.JobStatus.CANCELLED)
            job_reporter.change_step_pipe_status(step_index, 0, jobs.JobStatus.CANCELLED)

        if step.step_materialized_views:
            for index, _ in enumerate(step.step_materialized_views):
                is_last_mv_step = index == len(step.step_materialized_views) - 1
                is_last_drop_step = is_last_step and is_last_mv_step
                aux_copy_table_id = self.get_aux_copy_datasource_id_from_step(step, index=f"{step_index}{index}")
                try:
                    logging.info(f"before dropping table: {aux_copy_table_id}")
                    ch_drop_table_sync(
                        job_database_server,
                        step.step_workspace.database,
                        aux_copy_table_id,
                        avoid_max_table_size=True,
                        user_agent=CopyUserAgents.INTERNAL_COPY_QUERY,
                        log_comment=self._generate_log_comment({"is_last_step": is_last_drop_step}),
                        cluster=cluster,
                        **step.step_workspace.ddl_parameters(skip_replica_down=cluster is not None),
                    )
                    logging.info(f"dropped table: {aux_copy_table_id}")
                except Exception as e:
                    logging.exception(f"Exception on drop table {aux_copy_table_id}: {e}")
        elif step.step_copy:
            aux_copy_table_id = self.get_aux_copy_datasource_id_from_step(step)
            try:
                logging.info(f"before dropping table: {aux_copy_table_id}")
                ch_drop_table_sync(
                    job_database_server,
                    step.step_workspace.database,
                    aux_copy_table_id,
                    avoid_max_table_size=True,
                    user_agent=CopyUserAgents.INTERNAL_COPY_QUERY,
                    log_comment=self._generate_log_comment({"is_last_step": is_last_step}),
                    cluster=cluster,
                    **step.step_workspace.ddl_parameters(skip_replica_down=cluster is not None),
                )
                logging.info(f"dropped table: {aux_copy_table_id}")
            except Exception as e:
                logging.exception(f"Exception on drop table {aux_copy_table_id}: {e}")

    def send_raw_event(self: "CopyJob") -> None:
        updated_copy_job = self.get_by_id(self.id)
        if not updated_copy_job:
            logging.exception(f"Copy job {self.id} not found")
            return
        copyjob_event = convert_copyjob_to_rawevent(updated_copy_job)
        raw_events_batcher.append_record(copyjob_event)


async def new_copy_job(
    job_executor: jobs.JobExecutor,
    sql: str,
    request_id: str,
    workspace: Workspace,
    target_datasource: Datasource,
    app_settings: Dict[str, Any],
    target_workspace: Optional[Workspace] = None,
    pipe: Optional[Pipe] = None,
    execution_type: Optional[str] = ExecutionTypes.MANUAL,
    copy_timestamp: Optional[datetime] = None,
    use_query_queue: bool = False,
    max_threads: Optional[int] = None,
    parameters: Optional[Dict[str, str]] = None,
    mode: Optional[str] = CopyModes.APPEND,
    is_table_function: bool = False,
    ch_params_keys: Optional[Set[str]] = None,
) -> CopyJob:
    try:
        await CopyJob.validate(
            sql,
            target_datasource,
            workspace,
            app_settings,
            target_workspace,
            is_table_function,
            ch_params_keys=ch_params_keys,
        )
    except SharedUtils.CopyException as error:
        logging.debug(f"Copy job validation failed: {str(error)}")
        raise error
    except Exception as e:
        logging.debug(f"Copy job failed to create: {str(e)}")
        raise e

    j = create_copy(
        sql=sql,
        request_id=request_id,
        workspace=workspace,
        pipe=pipe,
        execution_type=execution_type,
        target_datasource=target_datasource,
        target_workspace=target_workspace,
        copy_timestamp=copy_timestamp,
        use_query_queue=use_query_queue,
        max_threads=max_threads,
        parameters=parameters,
        mode=mode,
        ch_params_keys=ch_params_keys,
        is_table_function=is_table_function,
    )

    logging.info(
        f"New copy job created: job_id={j.id}, database_server={j.database_server},"
        f" database={workspace.database}, sql={sql}"
    )
    job_executor.put_job(j)
    return j


def create_copy(
    workspace: Workspace,
    sql: str,
    target_datasource: Datasource,
    request_id: str,
    execution_type: Optional[str] = ExecutionTypes.MANUAL,
    pipe: Optional[Pipe] = None,
    copy_timestamp: Optional[datetime] = None,
    use_query_queue: bool = False,
    target_workspace: Optional[Workspace] = None,
    max_threads: Optional[int] = None,
    parameters: Optional[Dict[str, str]] = None,
    mode: Optional[str] = CopyModes.APPEND,
    ch_params_keys: Optional[Set[str]] = None,
    is_table_function: Optional[bool] = False,
):
    j = CopyJob(
        workspace=workspace,
        sql=sql,
        target_datasource=target_datasource,
        request_id=request_id,
        pipe=pipe,
        execution_type=execution_type,
        copy_timestamp=copy_timestamp,
        use_query_queue=use_query_queue,
        target_workspace=target_workspace,
        max_threads=max_threads,
        parameters=parameters,
        mode=mode,
        ch_params_keys=ch_params_keys,
        is_table_function=is_table_function,
    )
    j.save()
    j.send_raw_event()
    return j


async def cancel_pipe_copy_jobs(
    job_executor: jobs.JobExecutor, pipe: Pipe, data_sink: DataSink, api_host: str
) -> tuple[list[dict[str, str | dict[str, Any] | Any]], list[dict[str, str | dict[str, Any] | Any]]]:
    wip_jobs, queued_jobs = job_executor.get_wip_and_queued_jobs()
    not_cancelled_jobs: list[dict[str, str | dict[str, Any] | Any]] = []
    cancelled_jobs: list[dict[str, str | dict[str, Any] | Any]] = []
    if len(wip_jobs) == 0 and len(queued_jobs) == 0:
        logging.info("No jobs to cancel")
        # Pause the pipe's schedule incase there are jobs that are already done, or resulted in an error
        await pause_sink(data_sink)
        raise jobs.JobNotInCancellableStatusException()
    # Cancel jobs in waiting state that have the given pipe id
    for job in queued_jobs:
        assert isinstance(job, CopyJob)
        await jobs.cancel_job(api_host, cancelled_jobs, job, job_executor, not_cancelled_jobs, pipe)
    # Cancel jobs in working state that have the given pipe id
    for job in wip_jobs:
        assert isinstance(job, CopyJob)
        await jobs.cancel_job(api_host, cancelled_jobs, job, job_executor, not_cancelled_jobs, pipe)
    # Pause the pipe's schedule
    await pause_sink(data_sink)
    logging.info("atomic copy cancelled successfully")
    return cancelled_jobs, not_cancelled_jobs


def get_server_to_run_copy(
    job_id: str,
    database_server: str,
    cluster: str,
    copy_servers: list[str],
    query_settings: Dict[str, Any],
    user_agent: str,
    max_threads_limit: int,
) -> str:
    if len(copy_servers) > 1:
        try:
            return get_optimal_replica_based_on_load(
                job_id,
                database_server,
                cluster,
                copy_servers,
                query_settings,
                user_agent,
                max_threads_limit,
            )
        except CannotFindOptimalReplica:
            get_random_clickhouse_replica(job_id, copy_servers, user_agent, query_settings)

    return get_random_clickhouse_replica(job_id, copy_servers, user_agent, query_settings)


def convert_copyjob_to_rawevent(copy_job: "CopyJob") -> RawEvent:
    metadata = CopyJobMetadata(
        dependent_datasources=copy_job.dependent_datasources,
        processed_data=JobProcessedData(**copy_job.processed_data),
        execution_type=JobExecutionType(copy_job.execution_type),
        parameters=copy_job.parameters,
        pipe_name=copy_job.pipe_name,
        query_id=copy_job.query_id,
        query_sql=copy_job.sql,
        mode=copy_job.mode,
    )

    job_error = (
        copy_job.result["error"] if copy_job.status == jobs.JobStatus.ERROR and "error" in copy_job.result else None
    )

    copy_job_log = CopyJobLog(
        job_id=copy_job.id,
        job_type="copy",
        status=JobStatus(copy_job.status),
        error=job_error,
        pipe_id=copy_job.pipe_id,
        datasource_id=copy_job.datasource.id if copy_job.datasource else None,
        created_at=copy_job.created_at,
        started_at=copy_job.started_at,
        updated_at=copy_job.updated_at,
        job_metadata=metadata,
    )

    return RawEvent(
        timestamp=datetime.utcnow(),
        workspace_id=copy_job.workspace_id,
        request_id=copy_job.request_id,
        event_type=EventType.COPY,
        event_data=copy_job_log,
    )
