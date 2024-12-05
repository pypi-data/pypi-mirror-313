import json
import logging
from collections import defaultdict
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, cast

from tinybird.ch import (
    WAIT_ALTER_REPLICATION_OWN,
    CHException,
    Partition,
    Partitions,
    ch_attach_partitions,
    ch_query_table_partitions,
    ch_truncate_table_with_fallback,
    ch_wait_for_mutations,
)
from tinybird.datasource import SharedDatasource
from tinybird.job import Job, JobCancelledException, JobExecutor, JobKind
from tinybird.limits import Limit
from tinybird.syncasync import async_to_sync
from tinybird.user import User as Workspace
from tinybird.workspace_service import WorkspaceCloneResponse, WorkspaceService
from tinybird_shared.clickhouse.errors import CHErrors

LOG_TAG = "[DATA_BRANCH_LOG]"
ERROR_TAG = "[DATA_BRANCH_LOG_ERROR]"

NOT_FOUND = "Not found"
ERROR = "Error"
WARNING = "Warning"
DONE = "Done"
NO_PARTITIONS_FOUND = "No partitions found"
IGNORED = "Ignored"
FILTERED_BY_SIZE = "Filtered by size"

ATTACH_DATA_PARTITIONS_TIMEOUT = 60


class DataBranchMode(Enum):
    LAST_PARTITION = "last_partition"
    ALL_PARTITIONS = "all_partitions"


DATA_BRANCH_MODES = [a.value for a in DataBranchMode]


class DataBranchConflictError(Exception):
    pass


class DataBranchCreateError(Exception):
    def __init__(self, clone_errors: WorkspaceCloneResponse, *args: object) -> None:
        self.clone_errors = clone_errors
        super().__init__(*args)

    def __str__(self) -> str:
        return json.dumps(self.as_dict())

    def as_dict(self) -> Dict[str, Any]:
        return {
            "message": super().__str__(),
            "errors": self.clone_errors["errors_datasources"]
            + self.clone_errors["errors_pipes"]
            + self.clone_errors["errors_tokens"],
        }


class DataBranchResponse:
    def __init__(self, branch_id: str):
        self.branch_id = branch_id
        self.response: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.errors = ""

    def update(
        self,
        datasource_name: str,
        status: str,
        partition: Optional[str] = None,
        error: Optional[str] = None,
        warning: Optional[str] = None,
    ):
        o = {"status": status, "partition": partition}
        if error:
            o["error"] = error
            self.errors += f"Error: {error} while processing partition {partition} from Datasource {datasource_name}"
        if warning:
            o["error"] = warning
        self.response[datasource_name].append(o)

    def has(self, datasource_name: str) -> bool:
        return datasource_name in self.response

    def to_dict(self):
        return [{"datasource": {"name": name}, "partitions": partitions} for name, partitions in self.response.items()]


def new_data_branch_job(
    job_executor: JobExecutor,
    origin_workspace: Workspace,
    branch_workspace: Workspace,
    clone_resources: bool,
    data_branch_mode: Optional[str],
    ignore_datasources: Optional[List[str]] = None,
) -> "DataBranchJob":
    j = DataBranchJob(
        origin_workspace=origin_workspace,
        branch_workspace=branch_workspace,
        ignore_datasources=ignore_datasources,
        clone_resources=clone_resources,
        data_branch_mode=data_branch_mode,
    )
    j.save()
    logging.info(
        f"New data branch job created: job_id={j.id}, origin_database_server={origin_workspace.database_server}, origin_database={origin_workspace.database}, branch_name={branch_workspace.name}, branch_id={branch_workspace.id}, branch_database={branch_workspace.database}"
    )
    job_executor.put_job(j)
    return j


class DataBranchJob(Job):
    def __init__(
        self,
        origin_workspace: Workspace,
        branch_workspace: Workspace,
        ignore_datasources: Optional[List[str]],
        clone_resources: bool,
        data_branch_mode: Optional[str],
    ) -> None:
        self.origin = origin_workspace.id
        self.origin_database_server: str = origin_workspace.database_server
        self.origin_database: str = origin_workspace.database

        self.branch_workspace: str = branch_workspace.id
        self.branch_database_server: str = branch_workspace.database_server
        self.branch_database: str = branch_workspace.database
        self.branch_cluster: Optional[str] = branch_workspace.cluster

        # TODO: review using branch info. For the moment just make it work for two clusters
        self.database_server: str = branch_workspace.database_server
        self.database: str = self.origin_database
        self.databases = [
            origin_workspace.database,
            *list(
                set(
                    [
                        ds.original_ds_database
                        for ds in origin_workspace.get_datasources()
                        if isinstance(ds, SharedDatasource)
                    ]
                )
            ),
        ]

        self.ignore_datasources = ignore_datasources
        self.datasources = [
            ds.id
            for ds in origin_workspace.get_datasources()
            if ignore_datasources is None or ds.name not in ignore_datasources
        ]

        self.partitions: List[Dict[str, Any]] = []

        self.data_branch_mode = data_branch_mode
        self.clone_resources = clone_resources
        self.progress_percentage: float = 0

        Job.__init__(self, kind=JobKind.DATA_BRANCH, user=origin_workspace)

    def to_json(self, u: Optional[Workspace] = None, debug=None):
        d = super().to_json(u, debug)

        d["origin_workspace"] = self.origin
        d["branch_workspace"] = self.branch_workspace
        d["partitions"] = self.partitions

        d["progress_percentage"] = self.progress_percentage

        d["result"] = self.result
        if self.result.get("error"):
            err = self.result["error"]
            if isinstance(err, str):
                d["error"] = err
            else:
                d["error"] = err.get("message")
                d["errors"] = err.get("errors")

        return d

    def run(self):
        def function_to_execute(job: Job):
            try:
                job = cast(DataBranchJob, job)
                job.mark_as_working()

                origin_workspace = Workspace.get_by_id(self.origin)
                if not origin_workspace:
                    self.mark_as_cancelled()
                    return

                branch_workspace = Workspace.get_by_id(self.branch_workspace)
                if not branch_workspace:
                    self.mark_as_cancelled()
                    return

                if self.clone_resources:
                    branch_workspace = clone_resources(origin_workspace, branch_workspace)

                response = attach_data(
                    origin_workspace,
                    branch_workspace,
                    self.data_branch_mode,
                    self.ignore_datasources,
                    self,
                )

                result: Dict[str, Any] = {
                    "id": branch_workspace.id,
                    "name": branch_workspace.name,
                    "partitions": response.to_dict() or {},
                }

                if response.errors:
                    result["error"] = response.errors
                    self.mark_as_error(result)
                else:
                    self.mark_as_done(result, None)

            except JobCancelledException:
                self.mark_as_cancelled()

            except Exception as e:
                logging.exception(f"{ERROR_TAG} job_id => {job.id} - workspace_id => {job.user_id} - {str(e)}")
                error: Dict[str, Any] = (
                    {"error": e.as_dict()} if isinstance(e, DataBranchCreateError) else {"error": str(e)}
                )
                self.mark_as_error(error)

        self.job_executor.submit(function_to_execute, self)
        return self

    def on_new_partition_processed(self, partition: Optional[str], progress: DataBranchResponse) -> None:
        if partition:
            logging.info(f"{LOG_TAG} job_id => {self.id} - partition processed => {partition}")
        self.updated_at = datetime.utcnow()
        self.partitions = progress.to_dict()
        self.save()

    def update_progress(self, total: float, current: float) -> None:
        self.progress_percentage = current / total * 100
        logging.info(f"{LOG_TAG} job_id => {self.id} - progress => {self.progress_percentage}")
        self.save()


def clone_resources(origin: Workspace, branch_workspace: Workspace) -> Workspace:
    """Performs a schema clone.

    If called from within a job, the job instance should be passed in `job_context`.
    """
    clone_sync = async_to_sync(WorkspaceService.clone)
    clone_response: WorkspaceCloneResponse = clone_sync(branch_workspace, origin)
    if clone_response["errors_datasources"] or clone_response["errors_pipes"] or clone_response["errors_tokens"]:
        raise DataBranchCreateError(clone_response)

    # Return a fresh copy, after the clone
    result = Workspace.get_by_id(branch_workspace.id)
    assert isinstance(result, Workspace)
    return result


def attach_data(
    origin: Workspace,
    branch_workspace: Workspace,
    data_branch_mode: Optional[str],
    ignore_datasources: Optional[List[str]],
    job_context: DataBranchJob,
) -> DataBranchResponse:
    """Attaches data to the new workspace.

    If called from within a job, the job instance should be passed in `job_context`.
    """
    attach_data_sync = async_to_sync(_attach_data_async)
    return attach_data_sync(
        origin=origin,
        branch_workspace=branch_workspace,
        data_branch_mode=data_branch_mode,
        job_context=job_context,
        ignore_datasources=ignore_datasources,
    )


async def _attach_data_async(
    origin: Workspace,
    branch_workspace: Workspace,
    data_branch_mode: Optional[str],
    ignore_datasources: Optional[List[str]],
    job_context: DataBranchJob,
) -> DataBranchResponse:
    # Update the container job
    job_context.branch_workspace = branch_workspace.id
    job_context.branch_database_server = branch_workspace.database_server
    job_context.branch_cluster = branch_workspace.cluster
    job_context.branch_database = branch_workspace.database
    job_context.database_server = branch_workspace.database_server

    # Get a fresh copy after WorkspaceService.clone()
    branch_workspace = Workspace.get_by_id(branch_workspace.id)
    assert isinstance(branch_workspace, Workspace)

    result: DataBranchResponse

    if data_branch_mode == DataBranchMode.ALL_PARTITIONS.value:
        logging.info(f"{LOG_TAG} Cloning with ALL_PARTITIONS from {origin.id} to {branch_workspace.id}...")
        result = await attach_all_partitions(job_context)
    elif data_branch_mode == DataBranchMode.LAST_PARTITION.value:
        logging.info(f"{LOG_TAG} Cloning with LAST_PARTITION from {origin.id} to {branch_workspace.id}...")
        result = await attach_last_partitions(origin, branch_workspace, job_context, ignore_datasources)
    else:
        logging.info(f"{LOG_TAG} No data cloning from {origin.id} to {branch_workspace.id}...")
        result = DataBranchResponse(branch_workspace.id)
        # If no data to attach, let's update the process to 100%
        job_context.update_progress(total=1, current=1)

    return result


async def attach_all_partitions(
    job_context: DataBranchJob,
) -> DataBranchResponse:
    origin_workspace = Workspace.get_by_id(job_context.origin)
    branch_workspace = Workspace.get_by_id(job_context.branch_workspace)

    # TODO: We need to add the same logic for shared datasources and quarantine tables that we have in attach_last_partitions

    # get all partitions except ignored
    partitions = (
        await ch_query_table_partitions(
            job_context.origin_database_server,
            job_context.databases,
            table_names=job_context.datasources,
            only_last=False,
        )
        if job_context.datasources
        else []
    )

    return await attach_partitions(
        origin_workspace,
        branch_workspace,
        partitions,
        job_context.id,
        progress_listener=job_context,
        truncate=True,
        ignore_datasources=job_context.ignore_datasources,
    )


async def attach_last_partitions(
    origin_workspace: Workspace,
    branch_workspace: Workspace,
    job_context: DataBranchJob,
    ignore_datasources: Optional[List[str]] = None,
) -> DataBranchResponse:
    # get all databases involved
    databases = [
        origin_workspace.database,
        *list(
            set(
                [
                    ds.original_ds_database
                    for ds in origin_workspace.get_datasources()
                    if isinstance(ds, SharedDatasource)
                ]
            )
        ),
    ]

    # get all datasources except ignored ones
    datasources = (
        [ds for ds in origin_workspace.get_datasources() if ds.name not in ignore_datasources]
        if ignore_datasources
        else [ds for ds in origin_workspace.get_datasources()]
    )

    # We only want to attach the partitions + quarantine data is not shared
    datasources_ids = [ds.id for ds in datasources] + [
        ds.id + "_quarantine" for ds in datasources if not isinstance(ds, SharedDatasource)
    ]

    # get only last partition
    partitions = (
        await ch_query_table_partitions(
            origin_workspace.database_server,
            databases,
            table_names=datasources_ids,
            only_last=True,
        )
        if not ignore_datasources or datasources
        else []
    )

    # attach to branch workspace
    return await attach_partitions(
        origin_workspace,
        branch_workspace,
        partitions,
        job_context.id if job_context else "no_job",
        progress_listener=job_context,
        raise_if_mutations=True,
        ignore_datasources=ignore_datasources,
    )


async def attach_partitions(
    origin_workspace: Workspace,
    destination_workspace: Workspace,
    partitions: List[Partition],
    job_id: str,
    progress_listener: DataBranchJob,
    truncate: Optional[bool] = False,
    attach_wait_setting: str = WAIT_ALTER_REPLICATION_OWN,
    raise_if_mutations: Optional[bool] = False,
    ignore_datasources: Optional[List[str]] = None,
) -> DataBranchResponse:
    response: DataBranchResponse = DataBranchResponse(destination_workspace.id)

    iterating_limits = origin_workspace.get_limits(prefix="iterating")
    attach_parts_max_size = iterating_limits.get("iterating_attach_max_part_size", Limit.iterating_attach_max_part_size)
    attach_parts_batch_number = iterating_limits.get(
        "iterating_attach_parts_batch_number", Limit.iterating_attach_parts_batch_number
    )

    # If not partitions, mark job as 100 of progress
    if not partitions:
        progress_listener.update_progress(1, 1)

    # convert list of partitions to dict of table => list of partitions
    partitions_by_table = defaultdict(list)
    for p in partitions:
        partitions_by_table[(p.database, p.table)].append(p)

    total_progress = len(partitions) + len(partitions_by_table.keys()) if truncate else len(partitions)
    current_progress = 0

    def get_datasources(origin_table_id: str):
        try:
            origin_ds = origin_workspace.get_datasource(origin_table_id, include_read_only=True)
            if not origin_ds:
                logging.info(
                    f"{LOG_TAG} job_id => {job_id} - possible orphan table in {origin_workspace.id} => {origin_table_id}"
                )
                return None, None

            target_ds = destination_workspace.get_datasource(origin_ds.name, include_read_only=True)
            if not target_ds:
                logging.info(
                    f"{LOG_TAG} job_id => {job_id} - table not found in {destination_workspace.id} => {origin_ds.name}"
                )
                return origin_ds, None

            return origin_ds, target_ds
        except Exception as e:
            logging.exception(f"{ERROR_TAG} job_id => {job_id} - {destination_workspace.id} - {str(e)}")
            return None, None

    if truncate:
        logging.info(f"{LOG_TAG} job_id => {job_id} - {destination_workspace.id} - truncate tables ")
        truncated_tables = []
        for p in partitions:
            current_progress += 1
            progress_listener.update_progress(total_progress, current_progress)

            if p.table in truncated_tables:
                continue
            await wait_for_mutations(
                origin_workspace.database_server,
                origin_workspace.database,
                p.table,
                raise_if_mutations=raise_if_mutations,
                cluster=origin_workspace.cluster,
            )
            truncated_tables.append(p.table)

            _, target_ds = get_datasources(p.table)
            if target_ds:
                params = origin_workspace.ddl_parameters(skip_replica_down=True)
                try:
                    await ch_truncate_table_with_fallback(
                        destination_workspace.database_server,
                        destination_workspace.database,
                        target_ds.id,
                        destination_workspace.cluster,
                        wait_setting=attach_wait_setting,
                        **params,
                    )
                except Exception as e:
                    logging.exception(f"{ERROR_TAG} job_id => {job_id} - {destination_workspace.id} - {str(e)}")

    for database_table, partition_objects in partitions_by_table.items():
        p_to_attach, p_filtered_by_size = Partitions().split_by_size(partition_objects, attach_parts_max_size)
        _partitions = Partitions().as_sql_list(p_to_attach)
        _partitions_filtered = Partitions().as_sql_list(p_filtered_by_size)
        _is_quarantine_table = "quarantine" in database_table[1]

        logging.info(
            f"{LOG_TAG} job_id => {job_id} - {destination_workspace.id} - table => {database_table} - partitions => {_partitions}"
        )
        logging.info(
            f"{LOG_TAG} job_id => {job_id} - {destination_workspace.id} - table => {database_table} - filtered partitions => {_partitions_filtered}"
        )
        current_progress += 1

        progress_listener.update_progress(total_progress, current_progress)

        origin_ds, target_ds = get_datasources(database_table[1])
        if not origin_ds:
            continue
        if not target_ds:
            response.update(origin_ds.name, NOT_FOUND)
            continue

        for _p_f in _partitions_filtered:
            response.update(target_ds.name, FILTERED_BY_SIZE, _p_f)

        if _partitions:
            batch = attach_parts_batch_number or len(_partitions)
            for i in range(0, len(_partitions), batch):
                _p_batch = _partitions[i : i + batch]

                try:
                    # in prod avg time of an attach partition operation is ~50ms so we should be fine in most cases
                    # TODO: if database_server is different for both workspaces we should do FETCH PARTITION instead
                    await wait_for_mutations(
                        origin_workspace.database_server,
                        database_table[0],
                        database_table[1],
                        raise_if_mutations=raise_if_mutations,
                        cluster=origin_workspace.cluster,
                    )

                    try:
                        if _p_batch:
                            await ch_attach_partitions(
                                destination_workspace.database_server,
                                destination_workspace.database,
                                target_ds.id if not _is_quarantine_table else target_ds.id + "_quarantine",
                                origin_ds.id if not _is_quarantine_table else origin_ds.id + "_quarantine",
                                _p_batch,
                                wait_setting=attach_wait_setting,
                                origin_database=database_table[0],
                                max_execution_time=ATTACH_DATA_PARTITIONS_TIMEOUT,
                                user_agent="no-tb-data-branching-alter-query",
                            )
                        for _p in _p_batch:
                            response.update(target_ds.name, DONE, _p)
                        for _p in _p_batch:
                            progress_listener.on_new_partition_processed(_p, response)
                    except CHException as e:
                        logging.exception(
                            f"{LOG_TAG} job_id => {job_id} - {destination_workspace.id} - {e.code} - {str(e)} - fallback to attach partition"
                        )
                        if e.code == CHErrors.TIMEOUT_EXCEEDED:
                            datasource = origin_workspace.get_datasource(database_table[1])
                            datasource_name = datasource.name if datasource else ""
                            warning = f"Data from {datasource_name} Data Source could not be attached. If you need data from the main Workspace, please retry. If the problem persists, contact us at support@tinybird.co"
                            for _p in _p_batch:
                                response.update(target_ds.name, WARNING, _p, warning=warning)
                            for _p in _p_batch:
                                progress_listener.on_new_partition_processed(_p, response)
                        else:
                            for _p in _p_batch:
                                response.update(target_ds.name, ERROR, _p, str(e))
                            for _p in _p_batch:
                                progress_listener.on_new_partition_processed(_p, response)
                            return response
                except Exception as e:
                    ex_str = str(e).replace("\n", " ")
                    logging.exception(f"{ERROR_TAG} job_id => {job_id} - {destination_workspace.id} - {ex_str}")
                    # attach partition has some requirements (tables structure, storage policy, etc. must match)
                    # let's report an error so the user can copy data in any other way, but other partitions could still be attached
                    for _p in _p_batch:
                        response.update(target_ds.name, ERROR, _p, str(e))
                    for _p in _p_batch:
                        progress_listener.on_new_partition_processed(_p, response)
                    return response

    for ds in destination_workspace.get_datasources():
        if not response.has(ds.name) and not any([p.table for p in partitions if p.table == ds.id]):
            if ignore_datasources and ds.name in ignore_datasources:
                response.update(ds.name, IGNORED, "")
            else:
                response.update(ds.name, NO_PARTITIONS_FOUND, "")
    progress_listener.on_new_partition_processed(None, response)
    return response


async def wait_for_mutations(
    database_server: str,
    database: str,
    table: str,
    cluster: Optional[str] = None,
    raise_if_mutations: Optional[bool] = False,
):
    max_mutations_seconds_to_wait = 0 if raise_if_mutations else 360
    try:
        result = await ch_wait_for_mutations(
            database_server,
            database,
            table,
            max_mutations_seconds_to_wait=max_mutations_seconds_to_wait,
            cluster=cluster,
            skip_unavailable_replicas=True,
        )
        if result is False:
            logging.info(f"{LOG_TAG} mutations detected for {database}.{table}")
            raise RuntimeError(f"{ERROR_TAG} mutations detected for {database}.{table}")
    except RuntimeError as e:
        logging.exception(f"{ERROR_TAG} {str(e)}")
        raise DataBranchConflictError(
            "Cannot attach partitions because mutations are detected, please wait until any data operation (DELETE, TTL, etc.) finishes and retry in a few seconds."
        )
