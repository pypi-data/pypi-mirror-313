import logging
import os
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from enum import Enum
from functools import reduce
from typing import Any, Callable, Dict, List, Optional, Tuple, TypedDict, cast

import orjson
import ulid

from tinybird import tracker
from tinybird.ch import CHSummary, ch_escape_string, ch_guarded_query, ch_table_schema
from tinybird.ch_utils.describe_table import TableColumn
from tinybird.ch_utils.exceptions import CHException
from tinybird.connector_settings import DynamoDBConnectorSetting
from tinybird.data_connector import DataConnector, DataLinker
from tinybird.data_connectors.local_connectors import build_session_from_credentials
from tinybird.datasource import Datasource
from tinybird.integrations.dynamodb.column_mapping import build_column_mapping
from tinybird.integrations.dynamodb.limits import DynamoDBLimit
from tinybird.integrations.dynamodb.models import DynamoDBExportFile
from tinybird.job import (
    ColumnMapping,
    ColumnTypeCasting,
    Job,
    JobCancelledException,
    JobExecutor,
    JobKind,
    JobStatus,
    StaticColumnMapping,
    build_import_query_parts,
    get_column_type_castings,
)
from tinybird.limits import Limit
from tinybird.model import retry_transaction_in_case_of_concurrent_edition_error_sync
from tinybird.providers.auth import AuthProviderException
from tinybird.providers.aws.dynamodb import DynamoDBFinishedExportDescription, describe_export
from tinybird.providers.aws.exceptions import AWSClientException
from tinybird.providers.aws.s3 import get_object, get_signed_url
from tinybird.providers.aws.session import AWSSession
from tinybird.user import User as Workspace
from tinybird_shared.retry.retry import retry_sync

PartSummary = TypedDict(
    "PartSummary", {"read_rows": int, "read_bytes": int, "written_rows": int, "written_bytes": int, "elapsed_ns": int}
)
ImportedPart = TypedDict("ImportedPart", {"query_id": str, "summary": PartSummary})


def get_static_columns(timestamp: datetime) -> dict[str, StaticColumnMapping]:
    return {
        "_event_name": StaticColumnMapping(
            target="_event_name", value="SNAPSHOT", source_table_column=TableColumn("dummy", "Int8")
        ),
        "_record": StaticColumnMapping(
            target="_record",
            value="Item",
            wrap_in_quotes=False,
            source_table_column=TableColumn("dummy", "Int8"),
        ),
        "_timestamp": StaticColumnMapping(
            target="_timestamp",
            value=str(timestamp),
            source_table_column=TableColumn("dummy", "Int8"),
        ),
        "_is_deleted": StaticColumnMapping(
            target="_is_deleted",
            value=0,
            wrap_in_quotes=False,
            source_table_column=TableColumn("dummy", "Int8"),
        ),
    }


class DynamoDBExportStatus(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class DynamoDBFileImportStatus(str, Enum):
    WAITING = "WAITING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class DynamoDBSyncError(Exception):
    pass


class DynamoDBExportInProgress(Exception):
    pass


class DynamoDBSyncJob(Job):
    """
    # DynamoDB Sync Job

    ## What's the process
    When creating a DynamoDB Datasource, the API handler triggers a new Point-in-Time Export for the DynamoDB table that gets uploaded into an S3 bucket defined by the user in our configuration. The export is handled by AWS, and before reaching the end of the create_dynamodb_datasource function, we launch a job to process that specific export that was triggered.

    The Job gets the DataSource and DataLinker configuration, and waits until the export is performed. I am aware that concurrency is set to 2 Sync Jobs per Database, and some exports can delay other exports depending on how long they take. Will take care of this later by re-enqueuing jobs until there's an export that is finished.

    ## What does the job do?
    - The job waits until the export is performed
    - Reads the manifest-files.json that is included within the export folder, and generates signed URLs for all of them
    - Generates a column mapping to be able to ingest the data from the file into the landing DS
    - Inserts the data reading the file directly on ClickHouse with url() function, and reads and casts columns from the mappings.
    """

    def __init__(self, workspace: Workspace, datasource: Datasource, data_linker: DataLinker, request_id: str) -> None:
        job_id = str(uuid.uuid4())
        self.workspace_id: str = workspace.id
        self.datasource_id: str = datasource.id
        self.data_linker_id: str = data_linker.id
        self.database: str = workspace.database
        self.database_server: str = workspace.database_server
        self.s3_import_status: Dict[str, Any] = {}
        self.request_id: str = request_id
        Job.__init__(self, JobKind.DYNAMODB_SYNC, workspace, job_id, datasource=datasource)

    def to_json(self, workspace: Optional[Workspace] = None, debug: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        job = super().to_json(workspace, debug)

        if self.stats:
            job["stats"] = self.stats

        if self.status == JobStatus.ERROR and "error" in self.result:
            job["error"] = self.result["error"]

        if hasattr(self, "s3_import_status"):
            job["s3_import_status"] = self.s3_import_status

        return job

    @property
    def is_cancellable(self) -> bool:
        return self.status in {JobStatus.WAITING, JobStatus.WORKING}

    def run(self) -> "DynamoDBSyncJob":
        self.job_executor.submit(DynamoDBSyncJob.run_sync, self)
        return self

    @classmethod
    def run_sync(cls, j: Job) -> None:
        job = j.mark_as_working()
        job = cast(DynamoDBSyncJob, job)

        workspace = Workspace.get_by_id(job.workspace_id)
        datasource = workspace.get_datasource(job.datasource_id)

        try:
            if not datasource:
                raise DynamoDBSyncError(f"Datasource {job.datasource_id} not found")

            data_linker = job.get_data_linker(job.data_linker_id)
            data_connector = job.get_data_connector(data_linker.data_connector_id or "")

            connector_settings = cast(DynamoDBConnectorSetting, data_connector.validated_settings)
            linker_settings = data_linker.settings

            aws_session = job.get_aws_session(connector_settings)
            dynamodb_export_bucket = linker_settings.get("dynamodb_export_bucket", "")

            table_schema = ch_table_schema(
                table_name=job.datasource_id,
                database_server=job.database_server,
                database=job.database,
                include_default_columns=True,
                include_meta_columns=True,
            )

            if table_schema is None:
                raise DynamoDBSyncError("There was a problem while getting schema for destination table")

            try:
                export_description = job.wait_until_ddb_export_is_ready(
                    aws_session,
                    linker_settings.get("initial_export_arn", ""),
                    connector_settings.get_region(),
                )
                j.getLogger().info(
                    f"DynamoDB Export for {job.id} finished (workspace {job.workspace_id}), started at  {export_description.export_time}"
                )
            except DynamoDBExportInProgress:
                # Create new DynamoDBSync Job that waits until export is ready
                # New job is created to avoid blocking the queue
                workspace = Workspace.get_by_id(job.workspace_id)
                datasource = workspace.get_datasource(job.datasource_id)
                if not datasource:
                    raise DynamoDBSyncError(f"Datasource {job.datasource_id} not found")

                new_job = create_ddb_sync_job(
                    j.job_executor,
                    workspace=workspace,
                    datasource=datasource,
                    data_linker=data_linker,
                    request_id=job.request_id,
                )
                j.getLogger().warning(f"DynamoDB Export from job {job.id} wil be continued in new job {new_job.id}")
                raise DynamoDBSyncError(
                    f"DynamoDB Export from AWS is still in progress. Job '{new_job.id}' will try again to import your data."
                )

            # Determine whether this was a previously in-progress
            # import, and let it continue importing only the files
            # that were not imported in the previous run.
            if len(job.s3_import_status) <= 0:
                exported_files = job.get_files_to_import(
                    session=aws_session,
                    bucket=dynamodb_export_bucket,
                    region=connector_settings.get_region(),
                    export_manifest_path=export_description.export_manifest,
                )

                job.update_import_status(job.generate_initial_stats(exported_files))
            else:
                exported_files = job.get_unimported_files(job.s3_import_status)

            j.getLogger().info(f"DynamoDB syncing {len(exported_files)} from S3")

            all_files_processed_correctly = job.process_files_with_records(
                ch_table_name=job.datasource_id,
                export_time=export_description.export_time.replace(tzinfo=None),
                exported_files=exported_files,
                datasource_schema=table_schema,
                json_deserialization=linker_settings.get("json_deserialization", []),
                bucket_name=dynamodb_export_bucket,
                connector_settings=connector_settings,
            )

            j.getLogger().info(f"DynamoDB sync finished for job {j.id} (workspace {job.workspace_id})")
            job = cast(
                DynamoDBSyncJob,
                j.mark_as_done({}, None)
                if all_files_processed_correctly
                else j.mark_as_error(
                    {"error": "Some files were not processed correctly. Please check 's3_import_status' correctly"}
                ),
            )
            job.track(workspace=workspace, datasource=datasource)
        except AuthProviderException:
            # If this fails it means the machine is not properly configured
            logging.exception("Auth provider error on dynamodb job execution")
            error = "Internal server error. Please contact support@tinybird.co."
            job = cast(DynamoDBSyncJob, j.mark_as_error({"error": error}))
            job.track(workspace=workspace, datasource=datasource)
        except DynamoDBSyncError as err:
            job = cast(DynamoDBSyncJob, j.mark_as_error({"error": str(err)}))
            job.track(workspace=workspace, datasource=datasource)
        except JobCancelledException:
            job = cast(DynamoDBSyncJob, j.mark_as_cancelled())
            job.track(workspace=workspace, datasource=datasource)
        except Exception as err:
            job = cast(DynamoDBSyncJob, j.mark_as_error({"error": str(err)}))
            job.track(workspace=workspace, datasource=datasource)
            raise DynamoDBSyncError(f"There was a problem while syncing data: {err}")

    @retry_sync(DynamoDBExportInProgress, delay=60, backoff=1)
    def wait_until_ddb_export_is_ready(
        self, session: AWSSession, export_arn: str, region: str
    ) -> DynamoDBFinishedExportDescription:
        export_description = describe_export(session, export_arn, region)

        if export_description.export_status == DynamoDBExportStatus.FAILED:
            self.getLogger().warning(f"DynamoDB Export failed for job {self.id}: {export_description.failure_message}")
            raise DynamoDBSyncError(
                f"DynamoDB Export Failed: {export_description.failure_message} ({export_description.failure_code})"
            )

        if export_description.export_status == DynamoDBExportStatus.IN_PROGRESS:
            raise DynamoDBExportInProgress("DynamoDB Export from AWS is still in progress")

        return export_description

    def process_files_with_records(
        self,
        ch_table_name: str,
        export_time: datetime,
        exported_files: list[DynamoDBExportFile],
        datasource_schema: list[dict[str, Any]],
        json_deserialization: list[dict[str, Any]],
        bucket_name: str,
        connector_settings: DynamoDBConnectorSetting,
    ) -> bool:
        has_been_externally_cancelled = self.has_been_externally_cancelled_function_generator()

        workspace = Workspace.get_by_id(self.workspace_id)
        dynamodb_limits = workspace.get_limits(prefix="dynamodb")
        file_processing_workers_in_ddb_sync = int(
            dynamodb_limits.get(
                "dynamodb_file_processing_workers_in_ddb_sync", DynamoDBLimit.file_processing_workers_in_ddb_sync
            )
        )

        if has_been_externally_cancelled() or self.status == JobStatus.CANCELLED:
            raise JobCancelledException()

        column_mapping, column_type_castings = self.get_column_definition_for_insert(
            export_time=export_time,
            datasource_schema=datasource_schema,
            json_deserialization=json_deserialization,
        )

        def process_file(file: DynamoDBExportFile) -> DynamoDBFileImportStatus:
            if has_been_externally_cancelled():
                raise JobCancelledException()

            # Creating a new session here because the old one may
            # make URLs expire when it expires. If this works, we'll
            # make it better to catch the exception and so on
            aws_session = self.get_aws_session(connector_settings)

            try:
                url, _ = get_signed_url(
                    session=aws_session,
                    bucket_name=bucket_name,
                    file_name=file.dataFileS3Key,
                    region=connector_settings.get_region(),
                )
            except AWSClientException as e:
                self.update_file_import_status(
                    file.dataFileS3Key, {"status": DynamoDBFileImportStatus.FAILED, "error": str(e)}
                )
                return DynamoDBFileImportStatus.FAILED

            try:
                insert_summary = self.insert_from_url(
                    self.database_server, self.database, ch_table_name, url, column_mapping, column_type_castings
                )
                self.update_file_import_status(
                    file.dataFileS3Key,
                    {
                        "query_id": insert_summary.query_id,
                        "status": DynamoDBFileImportStatus.COMPLETED,
                        "summary": {
                            "read_rows": insert_summary.summary.get("read_rows", 0),
                            "read_bytes": insert_summary.summary.get("read_bytes", 0),
                            "written_rows": insert_summary.summary.get("written_rows", 0),
                            "written_bytes": insert_summary.summary.get("written_bytes", 0),
                            "elapsed_ns": insert_summary.summary.get("elapsed_ns", 0),
                        },
                    },
                )
                return DynamoDBFileImportStatus.COMPLETED
            except DynamoDBSyncError as e:
                self.update_file_import_status(
                    file.dataFileS3Key, {"status": DynamoDBFileImportStatus.FAILED, "error": str(e)}
                )
                return DynamoDBFileImportStatus.FAILED

        all_files_imported_correctly = True
        with ThreadPoolExecutor(
            max_workers=file_processing_workers_in_ddb_sync, thread_name_prefix=f"dynamodbsync_file_process_{self.id}"
        ) as executor:
            futures = [executor.submit(process_file, file) for file in exported_files]
            for future in futures:
                file_import_result = future.result()
                is_file_imported_OK = file_import_result == DynamoDBFileImportStatus.COMPLETED
                all_files_imported_correctly &= is_file_imported_OK

        return all_files_imported_correctly

    def get_files_to_import(
        self, session: AWSSession, bucket: str, region: str, export_manifest_path: str
    ) -> list[DynamoDBExportFile]:
        files_manifest_path = self.get_files_manifest_path(export_manifest_path)
        files = self.read_ddbjson_file_from_s3(session=session, bucket=bucket, key=files_manifest_path)

        return [file for file in files if file.itemCount > 0]

    def get_files_manifest_path(self, export_manifest_path: str) -> str:
        directory = os.path.dirname(export_manifest_path)
        return os.path.join(directory, "manifest-files.json")

    def get_aws_session(self, data_connector_settings: DynamoDBConnectorSetting) -> AWSSession:
        return cast(AWSSession, build_session_from_credentials(credentials=data_connector_settings.credentials))

    def get_data_linker(self, data_linker_id: str) -> DataLinker:
        data_linker = DataLinker.get_by_id(data_linker_id)

        if not data_linker:
            raise DynamoDBSyncError(f"Data Linker ({data_linker_id}) has not been found.")

        return data_linker

    def get_data_connector(self, data_connector_id: str) -> DataConnector:
        data_connector = DataConnector.get_by_id(data_connector_id)

        if not data_connector:
            raise DynamoDBSyncError(
                f"Data Connector ({data_connector_id}) has not been found. Please check if still exists or create another one."
            )

        return data_connector

    def read_ddbjson_file_from_s3(self, session: AWSSession, bucket: str, key: str) -> list[DynamoDBExportFile]:
        file_object = get_object(session, bucket, key)
        assert file_object.body
        self.getLogger().info(f"DynamoDB ddbjson file: File size of {key} in bucket {bucket}: {file_object.size} bytes")
        lines = file_object.body.iter_lines()
        return [DynamoDBExportFile(**orjson.loads(line.decode("utf-8"))) for line in lines]

    def get_column_definition_for_insert(
        self,
        export_time: datetime,
        datasource_schema: list[dict[str, Any]],
        json_deserialization: list[dict[str, Any]],
    ) -> Tuple[dict[str, ColumnMapping | StaticColumnMapping], list[ColumnTypeCasting]]:
        column_mapping: dict[str, ColumnMapping | StaticColumnMapping] = {
            **build_column_mapping(json_deserialization, datasource_schema),
            **get_static_columns(export_time),
        }

        column_type_castings = get_column_type_castings(datasource_schema, column_mapping)
        return column_mapping, column_type_castings

    def insert_from_url(
        self,
        database_server: str,
        database: str,
        table: str,
        url: str,
        column_mapping: dict[str, ColumnMapping | StaticColumnMapping],
        type_castings: list[ColumnTypeCasting],
    ) -> CHSummary:
        target_columns, source_columns, source_conditions = build_import_query_parts(column_mapping, type_castings)
        query_id = ulid.new().str

        query = f"INSERT INTO {database}.`{table}` ({target_columns}) WITH UnmarshalledJSON AS (SELECT accurateCast(JSONRemoveDynamoDBAnnotations(Item), 'String') as Item FROM url({ch_escape_string(url)}, JSONEachRow)) SELECT {source_columns} FROM UnmarshalledJSON WHERE {source_conditions}"

        try:
            _query_id, query_response = ch_guarded_query(
                database_server=database_server,
                database=database,
                query=query,
                query_id=query_id,
                user_agent="no-tb-dynamodb-sync",
                **self._get_import_query_settings(),
            )

            return CHSummary(query_id=query_id, summary=query_response)
        except CHException as e:
            raise DynamoDBSyncError(f"Error while syncing data: {e}")

    def _get_import_query_settings(self) -> Dict[str, Any]:
        workspace = Workspace.get_by_id(self.workspace_id)

        dynamodb_limits = workspace.get_limits(prefix="dynamodb")
        ch_limits = workspace.get_limits(prefix="ch")

        ch_max_insert_threads = ch_limits.get("max_insert_threads", Limit.ch_max_insert_threads)

        max_insert_threads = dynamodb_limits.get("dynamodb_max_insert_threads", ch_max_insert_threads)
        max_threads = dynamodb_limits.get("dynamodb_max_threads", DynamoDBLimit.max_threads)
        max_insert_block_size = dynamodb_limits.get(
            "dynamodb_max_insert_block_size", DynamoDBLimit.max_insert_block_size
        )
        min_insert_block_size_rows = dynamodb_limits.get(
            "dynamodb_min_insert_block_size_rows", DynamoDBLimit.min_insert_block_size_rows
        )
        min_insert_block_size_bytes = dynamodb_limits.get(
            "dynamodb_min_insert_block_size_bytes", DynamoDBLimit.min_insert_block_size_bytes
        )
        max_memory_usage = dynamodb_limits.get("dynamodb_max_memory_usage", DynamoDBLimit.max_memory_usage)
        max_execution_time = dynamodb_limits.get("dynamodb_max_execution_time", DynamoDBLimit.max_execution_time)

        max_partitions_per_insert_block = dynamodb_limits.get(
            "dynamodb_max_partitions_per_insert_block",
            DynamoDBLimit.max_partitions_per_insert_block,
        )

        insert_deduplicate = dynamodb_limits.get("dynamodb_insert_deduplicate", DynamoDBLimit.insert_deduplicate)
        enable_url_encoding = dynamodb_limits.get("dynamodb_enable_url_encoding", DynamoDBLimit.enable_url_encoding)
        input_format_try_infer_datetimes = dynamodb_limits.get(
            "dynamodb_input_format_try_infer_datetimes", DynamoDBLimit.input_format_try_infer_datetimes
        )
        input_format_try_infer_dates = dynamodb_limits.get(
            "dynamodb_input_format_try_infer_dates", DynamoDBLimit.input_format_try_infer_dates
        )

        import_dynamodb_settings = {
            "max_insert_threads": max_insert_threads,
            "max_threads": max_threads,
            "max_insert_block_size": max_insert_block_size,
            "min_insert_block_size_rows": min_insert_block_size_rows,
            "min_insert_block_size_bytes": min_insert_block_size_bytes,
            "max_memory_usage": max_memory_usage,
            "max_execution_time": max_execution_time,
            "max_partitions_per_insert_block": max_partitions_per_insert_block,
            "insert_deduplicate": insert_deduplicate,
            "enable_url_encoding": enable_url_encoding,
            "input_format_try_infer_datetimes": input_format_try_infer_datetimes,
            "input_format_try_infer_dates": input_format_try_infer_dates,
            "http_allow_get_request_for_file_info": 1,
            "input_format_json_try_infer_named_tuples_from_objects": 0,
        }

        settings: Dict[str, Any] = {key: value for key, value in import_dynamodb_settings.items() if value is not None}

        settings.update({"log_comment": self._generate_log_comment()})
        return settings

    def generate_initial_stats(self, files_to_ingest: List[DynamoDBExportFile]) -> Dict[str, Dict[str, str]]:
        return {file.dataFileS3Key: {"status": DynamoDBFileImportStatus.WAITING} for file in files_to_ingest}

    def get_unimported_files(self, all_files: Dict[str, Any]) -> List[DynamoDBExportFile]:
        return [
            DynamoDBExportFile(dataFileS3Key=file_key, itemCount=1)
            for (file_key, file_status) in all_files.items()
            if file_status.get("status") == DynamoDBFileImportStatus.WAITING
        ]

    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def update_import_status(self, new_value):
        with DynamoDBSyncJob.transaction(self.id) as job:
            if hasattr(job, "s3_import_status"):
                job.s3_import_status = new_value

            return job.s3_import_status

    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def update_file_import_status(self, file_key, new_value):
        with DynamoDBSyncJob.transaction(self.id) as job:
            if hasattr(job, "s3_import_status"):
                job.s3_import_status[file_key] = new_value

            return job.s3_import_status

    def has_been_externally_cancelled_function_generator(self) -> Callable[[], bool]:
        def has_been_cancelled() -> bool:
            job = Job.get_by_id(self.id)
            return job is not None and (job.status == JobStatus.CANCELLING or job.status == JobStatus.CANCELLED)

        return has_been_cancelled

    def track(
        self,
        workspace: Workspace,
        datasource: Optional[Datasource],
    ):
        tracker_registry = tracker.DatasourceOpsTrackerRegistry.get()
        if not tracker_registry or not tracker_registry.is_alive:
            logging.warning("DatasourceOpsTrackerRegistry is dead")
            return
        try:
            updated_job = DynamoDBSyncJob.get_by_id(self.id)
            if not updated_job:
                raise Exception(f"DynamoDB Sync job {self.id} not found")

            result = "ok"
            if updated_job.status == JobStatus.ERROR:
                result = "error"
            elif updated_job.status == JobStatus.CANCELLED:
                result = "cancelled"

            processed_data = self.get_aggregated_import_data(updated_job.s3_import_status)

            resource_tags: List[str] = []
            if workspace and datasource:
                resource_tags = [tag.name for tag in workspace.get_tags_by_resource(datasource.id, datasource.name)]

            record = tracker.DatasourceOpsLogRecord(
                timestamp=updated_job.created_at.replace(tzinfo=timezone.utc),
                event_type="sync-dynamodb",
                datasource_id=datasource.id if datasource else "",
                datasource_name=datasource.name if datasource else "",
                user_id=workspace.id or "",
                user_mail=workspace.name or "",
                result=result,
                elapsed_time=processed_data["elapsed_ns"],
                error=(
                    updated_job.result["error"]
                    if updated_job.status == JobStatus.ERROR and "error" in updated_job.result
                    else ""
                ),
                request_id=updated_job.request_id if updated_job.request_id else updated_job.id,
                import_id=updated_job.id,
                job_id=updated_job.id,
                rows=processed_data.get("written_rows", 0) if processed_data else 0,
                rows_quarantine=0,
                blocks_ids=[],
                Options__Names=list(["job"]),
                Options__Values=list([orjson.dumps(updated_job.to_json()).decode("utf-8")]),
                pipe_id="",
                pipe_name="",
                read_rows=processed_data.get("read_rows", 0) if processed_data else 0,
                read_bytes=processed_data.get("read_bytes", 0) if processed_data else 0,
                written_rows=processed_data.get("written_rows", 0) if processed_data else 0,
                written_bytes=processed_data.get("written_bytes", 0) if processed_data else 0,
                written_rows_quarantine=0,
                written_bytes_quarantine=0,
                operation_id=updated_job.id,
                release="",
                resource_tags=resource_tags,
            )

            entry = tracker.DatasourceOpsLogEntry(
                record=record,
                eta=datetime.now(timezone.utc),
                workspace=workspace,
                query_ids=[],
                query_ids_quarantine=[],
            )
            tracker_registry.submit(entry)
        except Exception as e:
            logging.exception(str(e))
        logging.info(f"Log for DynamoDB Sync job '{self.id}' submitted to tracker.")

    def get_aggregated_import_data(self, import_parts: Dict[str, ImportedPart]) -> PartSummary:
        parts = import_parts.values()

        def sum_statistics(total: PartSummary, part: ImportedPart) -> PartSummary:
            if part.get("summary") is None:
                return total

            total["read_rows"] += int(part["summary"]["read_rows"])
            total["read_bytes"] += int(part["summary"]["read_bytes"])
            total["written_rows"] += int(part["summary"]["written_rows"])
            total["written_bytes"] += int(part["summary"]["written_bytes"])
            total["elapsed_ns"] += int(part["summary"]["elapsed_ns"])
            return total

        default_value: PartSummary = {
            "read_rows": 0,
            "read_bytes": 0,
            "written_rows": 0,
            "written_bytes": 0,
            "elapsed_ns": 0,
        }
        return reduce(sum_statistics, parts, default_value)


def create_ddb_sync_job(
    job_executor: JobExecutor, workspace: Workspace, datasource: Datasource, data_linker: DataLinker, request_id: str
):
    job = DynamoDBSyncJob(
        workspace=workspace,
        datasource=datasource,
        data_linker=data_linker,
        request_id=request_id,
    )
    job.save()
    job_executor.put_job(job)
    logging.info(
        f"New DynamoDB Job created: job_id={job.id}, database_server={workspace.database_server}, database={workspace.database}, datasource={datasource.id}"
    )
    return job
