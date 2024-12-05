import dataclasses
import json
import logging
import numbers
import os
import re
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Tuple, cast

import ulid

from tinybird.ch import UserAgents, ch_guarded_query
from tinybird.connector_settings import DataConnectors, SinkConnectorSettings
from tinybird.constants import ExecutionTypes
from tinybird.data_connector import DataConnector, DataSink
from tinybird.data_connectors.constants import JOBID_METADATA_HEADER_NAME
from tinybird.data_connectors.local_connectors import (
    BucketFileInfo,
    BucketInfo,
    build_longest_static_prefix_of_destination,
    build_session_from_credentials,
    local_connector_from_settings,
)
from tinybird.data_sinks.billing import BillingDetails
from tinybird.data_sinks.config import (
    FILE_TEMPLATE_PROPERTIES_REGEX,
    SUPPORTED_EXPORT_FORMATS_MAPPING,
    ExportFormat,
    UnknownCompressionCodec,
    UnknownCompressionCodecAlias,
    WriteStrategy,
    expand_compression_codec_alias,
    get_compression_codec_extension,
)
from tinybird.data_sinks.exceptions import DataSinkException
from tinybird.data_sinks.limits import SinkLimits
from tinybird.data_sinks.parameters import replace_parameters_in_file_template
from tinybird.data_sinks.tracker import SinksExecutionLogRecord, SinksOpsLogResults, sinks_tracker
from tinybird.feature_flags import FeatureFlagsWorkspaceService, FeatureFlagWorkspaces
from tinybird.integrations.s3 import get_aws_session_name
from tinybird.job import Job, JobCancelledException, JobExecutor, JobKind, JobStatus
from tinybird.limits import Limit
from tinybird.pipe import Pipe
from tinybird.providers.auth import AuthProviderException
from tinybird.providers.aws.credentials import TemporaryAWSCredentials
from tinybird.providers.aws.exceptions import AWSClientException
from tinybird.providers.aws.s3 import head_object, list_objects
from tinybird.providers.aws.session import AWSSession
from tinybird.providers.gcp.session import GCPSession
from tinybird.raw_events.definitions.base import JobExecutionType
from tinybird.raw_events.definitions.base import JobStatus as JobStatusForLog
from tinybird.raw_events.definitions.sinks_log import (
    FinishedSinkJobMetadata,
    SinkBlobStorageJobOptions,
    SinkJobLog,
    SinkJobMetadata,
    SinkJobOptions,
    SinkKafkaJobOptions,
)
from tinybird.raw_events.raw_events_batcher import EventType, RawEvent, raw_events_batcher
from tinybird.sql_template import sqlescape_for_string_expression
from tinybird.user import User as Workspace

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# We might need to revisit this timeout eventually
# This makes the ch_guarded_query http client to timeout while the INSERT query is still running in CH
# It allows job cancellation after this timeout
SINKS_GUARDED_QUERY_TIMEOUT = 300


class S3Defaults:
    max_inflight_parts_for_one_file: int = 20
    allow_parallel_part_upload: int = 1


@dataclasses.dataclass(frozen=True)
class SinkConfiguration:
    export_location_url: str
    file_name: str
    format: str
    compression_codec: Optional[str]
    partition_by_expression: Optional[str]
    billing_details: BillingDetails
    render_internal_compression_in_binary_formats: bool

    def has_compression(self) -> bool:
        return bool(self.compression_codec)

    @property
    def export_url(self) -> str:
        filename = self._render_filename_with_extensions()
        return os.path.join(self.export_location_url, filename)

    def _is_binary_format(self) -> bool:
        return self.format in (ExportFormat.PARQUET, ExportFormat.ORC, ExportFormat.AVRO)

    def _render_filename_with_extensions(self) -> str:
        if (
            not self.compression_codec
            or self.compression_codec == "none"
            or (self._is_binary_format() and not self.render_internal_compression_in_binary_formats)
        ):
            return f"{self.file_name}.{self.format}"
        try:
            compression_codec_extension = get_compression_codec_extension(self.compression_codec)
        except UnknownCompressionCodec as err:
            raise DataSinkException(f"Unknown compression codec '{self.compression_codec}'") from err

        if self._is_binary_format():
            return f"{self.file_name}.{compression_codec_extension}.{self.format}"
        else:
            return f"{self.file_name}.{self.format}.{compression_codec_extension}"

    @property
    def ch_format(self) -> str:
        format = ExportFormat(self.format.lower())
        return SUPPORTED_EXPORT_FORMATS_MAPPING[format]


class CHQuerySettings(dict[str, Any]):
    def render(self) -> str:
        rendered_kvs = ", ".join(self._render_kv_pair(k, v) for k, v in self.items())
        return f"SETTINGS {rendered_kvs}"

    def _render_kv_pair(self, k: str, v: Any) -> str:
        if isinstance(v, numbers.Number):
            return f"{k} = {v}"
        else:  # Otherwise assume everything is a string
            return f"{k} = '{v}'"


@dataclasses.dataclass(frozen=True)
class InsertIntoS3Query:
    url: str
    format: str
    select_statement: str
    settings: CHQuerySettings
    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None
    headers: Optional[dict[str, str]] = None
    partition_by_expression: Optional[str] = None

    def render(self) -> str:
        rendered_args = ", ".join(self._get_s3_table_function_args())
        query_fragments = [
            f"INSERT INTO FUNCTION s3({rendered_args})",
            f"PARTITION BY {self.partition_by_expression}" if self.partition_by_expression else None,
            self.select_statement,
            self.settings.render() if self.settings else None,
        ]
        return "\n".join(filter(None, query_fragments))

    def with_access_key_credentials(self, access_key_id: str, secret_access_key: str) -> "InsertIntoS3Query":
        return dataclasses.replace(self, access_key_id=access_key_id, secret_access_key=secret_access_key)

    def with_headers(self, headers: dict[str, str]) -> "InsertIntoS3Query":
        return dataclasses.replace(self, headers=headers)

    def _get_s3_table_function_args(self) -> list[str]:
        args = [f"'{self.url}'"]
        if self.access_key_id:
            args.append(f"'{self.access_key_id}'")
        if self.secret_access_key:
            args.append(f"'{self.secret_access_key}'")
        args.append(f"'{self.format}'")
        if self.headers:
            rendered_header_kvs = ", ".join(f"'{k}'='{v}'" for k, v in self.headers.items())
            args.append(f"headers({rendered_header_kvs})")
        return args


def query_settings_from_sink_config(config: SinkConfiguration) -> CHQuerySettings:
    settings = CHQuerySettings()
    if config.format.lower() == ExportFormat.PARQUET and config.compression_codec:
        settings["output_format_parquet_compression_method"] = config.compression_codec
    elif config.format.lower() == ExportFormat.ORC and config.compression_codec:
        settings["output_format_orc_compression_method"] = config.compression_codec
    elif config.format.lower() == ExportFormat.AVRO and config.compression_codec:
        # Avro uses yet another name for no compression so we handle it inline for now
        settings["output_format_avro_codec"] = (
            "null" if config.compression_codec == "none" else config.compression_codec
        )
    return settings


class DataSinkBaseJob(Job):
    def __init__(
        self,
        workspace: Workspace,
        pipe: Pipe,
        data_sink: DataSink,
        sql: str,
        token_name: str,
        billing_provider: str,
        billing_region: str,
        request_id: str = "",
        execution_type: Optional[str] = ExecutionTypes.SCHEDULED,
        job_timestamp: Optional[datetime] = None,
        job_kind: str = JobKind.SINK,
    ) -> None:
        self.database: str = workspace.database
        self.cluster: str = workspace.cluster if workspace.cluster else Workspace.default_cluster
        self.sql = sql
        self.query_id: str = ulid.new().str
        self.request_id = request_id
        self.pipe_id: str = pipe.id if pipe else ""
        self.pipe_name: str = pipe.name if pipe else ""
        self.workspace_id: str = workspace.id
        self.token_name = token_name
        self.billing_provider = billing_provider
        self.billing_region = billing_region
        self.execution_type = execution_type
        self.job_timestamp = job_timestamp

        # We're getting the database server from cheriff,
        # just in case there is an override for virtual clusters
        self.database_server: str = workspace.get_limits(prefix="sinks").get("sinks_cluster", workspace.database_server)

        if data_sink.data_connector_id is None or data_sink.service is None:
            raise DataSinkException(
                "There's been an error with the Data Connector configuration. Please, check it still exists and the Service it exports to."
            )
        self.data_connector_id: str = data_sink.data_connector_id
        self.service: str = data_sink.service

        if workspace.is_branch_or_release_from_branch:
            job_kind = JobKind.SINK_BRANCH

        Job.__init__(self, kind=job_kind, user=workspace)

        self.__ttl__ = 3600 * int(
            workspace.get_limits(prefix="sinks").get("sinks_max_job_ttl_in_hours", Limit.sinks_max_job_ttl_in_hours)
        )

    @property
    def sink_job_options(self) -> SinkJobOptions:
        raise NotImplementedError()

    @staticmethod
    async def validate(workspace: Workspace) -> None:
        SinkLimits.max_active_jobs.evaluate(workspace)

    @classmethod
    def run_data_sink(cls, j: "Job") -> None:
        raise NotImplementedError()

    def to_json(
        self,
        workspace: Optional[Workspace] = None,
        debug: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        job = super().to_json(workspace, debug)
        job.update(
            {
                "query_id": self.query_id,
                "query_sql": " ".join(self.sql.split()),
                "pipe": {"id": self.pipe_id, "name": self.pipe_name},
                "token_name": self.token_name,
                "service": self.service,
            }
        )

        if self.status == JobStatus.ERROR and "error" in self.result:
            job["error"] = self.result["error"]
        return job

    def to_public_json(self, job: Job, api_host: str = ""):
        public_json = super().to_public_json(job, api_host)

        public_json.update({"pipe": {"id": public_json["pipe_id"], "name": public_json["pipe_name"]}})

        del public_json["pipe_id"]
        del public_json["pipe_name"]

        return public_json

    def run(self) -> "DataSinkBaseJob":
        self.job_executor.submit(self.__class__.run_data_sink, self)
        return self

    def send_raw_event(self, output: list[str] | None = None, billing_details: BillingDetails | None = None) -> None:
        updated_sink_job = self.get_by_id(self.id)
        if not updated_sink_job:
            logging.exception(f"DataSink job {self.id} not found")
            return
        sinkjob_event = convert_sinkjob_to_rawevent(updated_sink_job, output, billing_details)
        raw_events_batcher.append_record(sinkjob_event)

    def track(
        self,
        output: list[str],
        error: Optional[str] = None,
        billing: Optional[BillingDetails] = None,
    ) -> None:
        if not sinks_tracker.is_enabled():
            logging.info(
                f"sinks_tracker - Cannot log sink execution because tracker is not enabled - Job ID: {self.id}"
            )
            return

        finished_timestamp: datetime = self.updated_at.replace(tzinfo=timezone.utc)
        elapsed_time: float = (finished_timestamp - self.created_at.replace(tzinfo=timezone.utc)).total_seconds()

        record: SinksExecutionLogRecord = self.create_record_to_log(
            elapsed_time=elapsed_time, output=output, error=error, billing=billing
        )
        sinks_tracker.append_execution_log(record)

    def create_record_to_log(
        self,
        elapsed_time: float,
        output: list[str],
        error: Optional[str] = None,
        billing: Optional[BillingDetails] = None,
    ) -> SinksExecutionLogRecord:
        raise NotImplementedError()

    def _get_result_from_status(self) -> SinksOpsLogResults:
        result = SinksOpsLogResults.OK
        if self.status == JobStatus.ERROR:
            result = SinksOpsLogResults.ERROR
        elif self.status == JobStatus.CANCELLED:
            result = SinksOpsLogResults.CANCELLED
        return result


class DataSinkBlobStorageJob(DataSinkBaseJob):
    def __init__(
        self,
        workspace: Workspace,
        pipe: Pipe,
        data_sink: DataSink,
        sql: str,
        token_name: str,
        file_template: str,
        file_format: str,
        billing_provider: str,
        billing_region: str,
        file_compression: str = "",
        request_id: str = "",
        write_strategy: str = "",
        execution_type: Optional[str] = ExecutionTypes.SCHEDULED,
        job_timestamp: Optional[datetime] = None,
    ) -> None:
        super().__init__(
            workspace=workspace,
            pipe=pipe,
            data_sink=data_sink,
            sql=sql,
            token_name=token_name,
            billing_provider=billing_provider,
            billing_region=billing_region,
            request_id=request_id,
            execution_type=execution_type,
            job_timestamp=job_timestamp,
        )
        # These properties coming in the constructor override
        # the ones defined in the sink, because they might be coming
        # from the POST request that triggered the Sink job
        self.file_template = file_template
        self.file_format = file_format
        self.file_compression = file_compression
        self.write_strategy = write_strategy

        self.bucket_path: str = get_bucket_path(data_sink=data_sink)

    @property
    def sink_job_options(self) -> SinkJobOptions:
        return SinkBlobStorageJobOptions(
            file_template=self.file_template,
            file_format=self.file_format,
            file_compression=self.file_compression,
            bucket_path=self.bucket_path,
            execution_type=JobExecutionType(self.execution_type),
        )

    def get_data_sql(
        self,
        sql: str,
        session: AWSSession | GCPSession,
        configuration: SinkConfiguration,
        include_meta_headers: bool,
    ) -> str:
        settings = query_settings_from_sink_config(configuration)
        settings["log_comment"] = json.dumps(
            self._log_comment({**configuration.billing_details.model_dump(), "job_service": "blob_storage"})
        )
        query = InsertIntoS3Query(
            url=configuration.export_url,
            format=configuration.ch_format,
            select_statement=sql,
            settings=settings,
            partition_by_expression=configuration.partition_by_expression,
        )

        headers = {}
        if include_meta_headers:
            headers[f"x-amz-meta-{JOBID_METADATA_HEADER_NAME}"] = self.id
        if isinstance(session, AWSSession):
            access_key = session.get_credentials()
            if isinstance(access_key, TemporaryAWSCredentials):
                headers["x-amz-security-token"] = access_key.session_token
            query = query.with_access_key_credentials(access_key.access_key_id, access_key.secret_access_key)
        elif isinstance(session, GCPSession):
            oauth2_token = session.get_credentials().token
            headers["Authorization"] = f"Bearer {oauth2_token}"

        return query.with_headers(headers).render()

    def to_json(
        self,
        workspace: Optional[Workspace] = None,
        debug: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        job = super().to_json(workspace, debug)
        job.update(
            {
                "options": {
                    "file_template": self.file_template,
                    "file_format": self.file_format,
                    "file_compression": self._get_compression_codec(),
                    "bucket_path": self.bucket_path,
                    "execution_type": self.execution_type,
                    "write_strategy": self.write_strategy if hasattr(self, "write_strategy") else "",
                },
            }
        )

        return job

    def explode_template_parts(self, file_template: str) -> Tuple[str, Optional[str]]:
        if "{" not in file_template or "}" not in file_template:
            return file_template, None

        matched_columns = re.finditer(FILE_TEMPLATE_PROPERTIES_REGEX, file_template)

        elements_to_concat = []
        properties_len_start = 999999
        properties_len_end = 0

        for column in matched_columns:
            properties_dict = column.groupdict()
            column_name = properties_dict.get("column_name", "")
            date_format = properties_dict.get("date_format")
            separator = properties_dict.get("separator") or ""

            if column_name.isdigit():
                elements_to_concat.append(f"toString(rand() % {column_name})")
            elif date_format:
                elements_to_concat.append(f"formatDateTime({column_name}, '{date_format}')")
            else:
                elements_to_concat.append(f"toString({column_name})")

            if separator:
                elements_to_concat.append(f"'{sqlescape_for_string_expression(separator)}'")

            match_span = column.span()
            properties_len_start = min(properties_len_start, match_span[0])
            properties_len_end = max(properties_len_end, match_span[1])

        partitioned_file_template = (
            f"{file_template[:properties_len_start]}{{_partition_id}}{file_template[properties_len_end + 1:]}"
        )
        return (
            partitioned_file_template,
            f"concat({','.join(elements_to_concat)})" if len(elements_to_concat) > 1 else elements_to_concat[0],
        )

    def _get_compression_codec(self) -> Optional[str]:
        if not self.file_compression:
            return None

        try:
            return expand_compression_codec_alias(self.file_compression.lower())
        except UnknownCompressionCodecAlias:
            # In the original implementation we pass an empty string to the job so this allows us to use Optional while we change it
            return self.file_compression.lower()

    @classmethod
    def run_data_sink(cls, j: "Job") -> None:
        job = j.mark_as_working()
        job = cast(DataSinkBlobStorageJob, job)
        output_files: list[str] = []

        # Cutting out the SQL string to a
        # reasonable amount of parameters
        # to prevent Redis jobs taking so
        # so much space saved in memory
        # after finishing
        final_job_sql = job.sql[:2000]
        billing_details: Optional[BillingDetails] = None  # To be set later

        try:
            workspace = Workspace.get_by_id(job.workspace_id)
            data_connector: Optional[DataConnector] = DataConnector.get_by_id(job.data_connector_id)
            if not data_connector:
                err_msg = f"Data Connector ({job.data_connector_id}) has not been found. Please check if still exists or create another one."
                raise DataSinkException(err_msg)
            settings = cast(SinkConnectorSettings, data_connector.validated_settings)
            credentials = settings.credentials
            local_connector = local_connector_from_settings(settings)
            bucket_info = local_connector.get_bucket_info(credentials, job.bucket_path)

            is_files_observability_enabled = FeatureFlagsWorkspaceService.feature_for_id(
                FeatureFlagWorkspaces.DATA_SINKS_FILES_OBSERVABILITY,
                "",
                workspace.feature_flags,
            )

            billing_details = BillingDetails(
                origin_provider=job.billing_provider,
                origin_region=job.billing_region,
                destination_provider=settings.get_provider_name(),
                destination_region=settings.get_region(),
            )

            # Another replace for Job specific properties
            available_properties = {"job_id": job.id}
            replaced_file_name = replace_parameters_in_file_template(job.file_template, available_properties)
            file_name, partition_by_expression = job.explode_template_parts(replaced_file_name)
            compression_codec = job._get_compression_codec()

            render_internal_compression_in_binary_formats = workspace.get_limits(prefix="sinks").get(
                "sinks_render_internal_compression_in_binary_formats",
                Limit.sinks_render_internal_compression_in_binary_formats,
            )

            sink_configuration = SinkConfiguration(
                export_location_url=bucket_info.url,
                file_name=file_name,
                format=job.file_format.lower(),
                compression_codec=compression_codec,
                partition_by_expression=partition_by_expression,
                billing_details=billing_details,
                render_internal_compression_in_binary_formats=render_internal_compression_in_binary_formats,
            )

            session = build_session_from_credentials(
                credentials=settings.credentials,
                session_name=get_aws_session_name(workspace),
                endpoint_url=settings.endpoint_url,
            )
            export_query = job.get_data_sql(
                sql=job.sql,
                session=session,
                configuration=sink_configuration,
                include_meta_headers=is_files_observability_enabled,
            )
            query_settings = job.query_settings(workspace)
            if sink_configuration.format == ExportFormat.PARQUET:
                output_format_parquet_string_as_string = workspace.get_limits(prefix="sinks").get(
                    "sinks_output_format_parquet_string_as_string", Limit.sinks_output_format_parquet_string_as_string
                )
                query_settings["output_format_parquet_string_as_string"] = output_format_parquet_string_as_string

            ch_guarded_query(
                database_server=job.database_server,
                database=job.database,
                query=export_query,
                cluster=job.cluster,
                query_id=job.query_id,
                user_agent=UserAgents.SINKS.value,
                timeout=SINKS_GUARDED_QUERY_TIMEOUT,
                read_cluster=True,
                read_only=True,
                retries=False,
                **query_settings,
            )

            # Observability on Files is under FF because it only
            # works on CH >= 24.1.6. We should remove the FF when
            # every cluster is updated and we don't have this restriction
            if is_files_observability_enabled and isinstance(session, AWSSession):
                region = None if "unknown" == settings.get_region() else settings.get_region()
                output_files = job.get_exported_files(session, bucket_info, region, replaced_file_name)

            # Sink jobs are sometimes getting stuck. We add a log to see if they are finishing.
            # https://gitlab.com/tinybird/analytics/-/issues/14058
            logging.info(f"Marking sink job {j.id} as done")

            # There is a bug which makes jobs get stuck when
            # trying to execute any mark_as_* functions with the value
            # returned from any mark_as_* function. It can only be
            # executed with the job coming in the function arguments.
            # It is due to the fact that we're stripping `job_executor`
            # property because we return the transaction job. We should look into it.
            job = cast(DataSinkBlobStorageJob, j.mark_as_done({}, None, final_job_sql, should_send_raw_event=False))
            job.track(output=output_files, billing=billing_details)
            job.send_raw_event(output=output_files, billing_details=billing_details)

        except JobCancelledException:
            job = cast(DataSinkBlobStorageJob, j.mark_as_cancelled(final_job_sql))
            job.track(output=output_files)
        except AuthProviderException as err:
            # If this fails it means the machine is not properly configured
            logging.exception("Auth provider error on sink job execution")
            error = "Internal server error. Please contact support@tinybird.co."
            job = cast(
                DataSinkBlobStorageJob, j.mark_as_error({"error": error}, final_job_sql, should_send_raw_event=False)
            )
            job.track(output=output_files, error=error)
            job.send_raw_event(output=output_files, billing_details=billing_details)
            raise DataSinkException(f"There was a problem while exporting data: {err}")
        except Exception as err:
            job = cast(
                DataSinkBlobStorageJob, j.mark_as_error({"error": str(err)}, final_job_sql, should_send_raw_event=False)
            )
            job.track(output=output_files, error=str(err))
            job.send_raw_event(output=output_files, billing_details=billing_details)
            raise DataSinkException(f"There was a problem while exporting data: {err}")

    def query_settings(self, workspace: Workspace) -> Dict[str, Any]:
        max_execution_time = SinkLimits.max_execution_time.get_limit_for(workspace)
        s3_max_inflight_parts_for_one_file = workspace.get_limits(prefix="sinks").get(
            "sinks_s3_max_inflight_parts_for_one_file", S3Defaults.max_inflight_parts_for_one_file
        )
        s3_allow_parallel_part_upload = workspace.get_limits(prefix="sinks").get(
            "sinks_s3_allow_parallel_part_upload", S3Defaults.allow_parallel_part_upload
        )
        max_threads = workspace.get_limits(prefix="sinks").get("sinks_max_threads", Limit.ch_max_threads)
        max_insert_threads = workspace.get_limits(prefix="sinks").get("sinks_max_insert_threads", 0)
        max_result_bytes = workspace.get_limits(prefix="sinks").get("sinks_max_result_bytes", Limit.ch_max_result_bytes)
        output_format_parallel_formatting = workspace.get_limits(prefix="sinks").get(
            "sinks_output_format_parallel_formatting", Limit.sinks_output_format_parallel_fomatting
        )

        settings = {
            "max_execution_time": max_execution_time,
            "max_threads": max_threads,
            "max_insert_threads": max_insert_threads,
            "max_result_bytes": max_result_bytes,
            "s3_create_new_file_on_insert": 1,
            "s3_max_inflight_parts_for_one_file": s3_max_inflight_parts_for_one_file,
            "s3_allow_parallel_part_upload": s3_allow_parallel_part_upload,
            "join_algorithm": "auto",
            "output_format_parallel_formatting": output_format_parallel_formatting,
        }

        # max_memory_usage and max_result_bytes limits are only applied
        # if they are explicitly set in Cheriff. Server limits are applied otherwise
        if max_memory_usage := workspace.get_limits(prefix="sinks").get("sinks_max_memory_usage"):
            settings["max_memory_usage"] = max_memory_usage

        if max_bytes_before_external_group_by := workspace.get_limits(prefix="sinks").get(
            "sinks_max_bytes_before_external_group_by"
        ):
            settings["max_bytes_before_external_group_by"] = max_bytes_before_external_group_by

        if max_insert_delayed_streams_for_parallel_write := workspace.get_limits(prefix="sinks").get(
            "sinks_max_insert_delayed_streams_for_parallel_write"
        ):
            settings["max_insert_delayed_streams_for_parallel_write"] = max_insert_delayed_streams_for_parallel_write

        if max_bytes_before_external_sort := workspace.get_limits(prefix="sinks").get(
            "sinks_max_bytes_before_external_sort"
        ):
            settings["max_bytes_before_external_sort"] = max_bytes_before_external_sort

        if self.write_strategy == WriteStrategy.TRUNCATE:
            settings["s3_truncate_on_insert"] = 1

        return settings

    def get_exported_files(
        self,
        session: AWSSession,
        bucket: BucketInfo,
        region: Optional[str],
        file_template: str,
    ) -> list[str]:
        # Get the deepest known prefix to list as fewer files as possible from the bucket
        filter_prefix = build_longest_static_prefix_of_destination(bucket.prefix, file_template)
        objects = list_objects(session, bucket.name, prefix=filter_prefix, region=region)
        # Map to BucketFileInfo to keep the API for now:
        bucket_files = [BucketFileInfo(obj.key, obj.last_modified, obj.size) for obj in objects]
        # Filter out exported files. Workaround
        # until we have headers is to compare
        # dates with last modified dates in files
        job_started_at = cast(datetime, self.started_at)
        uploaded_files = [file for file in bucket_files if file.is_modified_after(job_started_at)]

        # Second Round of Filtering for Files
        # to match the custom metadata added
        # in the CH query with the job id
        return [
            to_log_file_str(file)
            for file in uploaded_files
            if _has_tb_job_id(session, bucket, file, self.id, region=region)
        ]

    def create_record_to_log(
        self,
        elapsed_time: float,
        output: list[str],
        error: Optional[str] = None,
        billing: Optional[BillingDetails] = None,
    ) -> SinksExecutionLogRecord:
        workspace = Workspace.get_by_id(self.workspace_id)

        options = {
            "file_template": self.file_template if self.file_template else "",
            "file_format": self.file_format,
            "file_compression": self._get_compression_codec() or "",
            "bucket_path": self.bucket_path,
            "execution_type": self.execution_type,
        }
        if hasattr(self, "job_timestamp") and self.job_timestamp:
            options["job_timestamp"] = self.job_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        if billing:
            options.update(billing.model_dump())

        resource_tags = workspace.get_tag_names_by_resource(self.pipe_id, self.pipe_name)
        return SinksExecutionLogRecord(
            workspace_id=workspace.id,
            workspace_name=workspace.name,
            workspace_database=workspace.database_server,
            workspace_cluster=workspace.cluster or "",
            query_id=self.query_id,
            timestamp=self.created_at,
            service=self.service,
            pipe_id=self.pipe_id,
            pipe_name=self.pipe_name,
            token_name=self.token_name,
            result=self._get_result_from_status(),
            elapsed_time=elapsed_time,
            error=error,
            job_id=self.id,
            output=output,
            parameters={},
            options=options,
            resource_tags=resource_tags,
        )


class DataSinkKafkaJob(DataSinkBaseJob):
    def __init__(
        self,
        workspace: Workspace,
        pipe: Pipe,
        data_sink: DataSink,
        sql: str,
        token_name: str,
        billing_provider: str,
        billing_region: str,
        request_id: str = "",
        write_strategy: str = "",
        execution_type: Optional[str] = ExecutionTypes.SCHEDULED,
        job_timestamp: Optional[datetime] = None,
    ) -> None:
        super().__init__(
            workspace=workspace,
            pipe=pipe,
            data_sink=data_sink,
            sql=sql,
            token_name=token_name,
            billing_provider=billing_provider,
            billing_region=billing_region,
            request_id=request_id,
            execution_type=execution_type,
            job_timestamp=job_timestamp,
        )
        self.target_table: str = data_sink.settings.get("target_table", "")
        self.topic: str = data_sink.settings.get("topic", "")
        if not self.target_table or not self.topic:
            raise DataSinkException(
                "There's been an error with the Kafka Data Connector configuration. Recreate the Kafka Sink or contact us at support@tinybird.co."
            )

    @property
    def sink_job_options(self) -> SinkJobOptions:
        return SinkKafkaJobOptions(
            topic=self.topic,
            execution_type=JobExecutionType(self.execution_type),
        )

    def to_json(
        self,
        workspace: Optional[Workspace] = None,
        debug: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        job = super().to_json(workspace, debug)
        job.update(
            {
                "options": {
                    "topic": self.topic,
                    "execution_type": self.execution_type,
                },
            }
        )

        return job

    @classmethod
    def run_data_sink(cls, j: "Job") -> None:
        job = j.mark_as_working()
        job = cast(DataSinkKafkaJob, job)

        # Cutting out the SQL string to a
        # reasonable amount of parameters
        # to prevent Redis jobs taking so
        # so much space saved in memory
        # after finishing
        final_job_sql = job.sql[:2000]

        try:
            workspace = Workspace.get_by_id(job.workspace_id)
            data_connector: Optional[DataConnector] = DataConnector.get_by_id(job.data_connector_id)
            if not data_connector:
                err_msg = f"Data Connector ({job.data_connector_id}) has not been found. Please check if still exists or create another one."
                raise DataSinkException(err_msg)

            query_settings = job.query_settings(workspace)
            export_query = f"INSERT INTO {job.database}.{job.target_table} {job.sql}"

            ch_guarded_query(
                database_server=job.database_server,
                database=job.database,
                query=export_query,
                cluster=job.cluster,
                query_id=job.query_id,
                user_agent=UserAgents.SINKS.value,
                timeout=SINKS_GUARDED_QUERY_TIMEOUT,
                retries=False,
                **query_settings,
            )

            # Sink jobs are sometimes getting stuck. We add a log to see if they are finishing.
            # https://gitlab.com/tinybird/analytics/-/issues/14058
            logging.info(f"Marking sink job {j.id} as done")

            # There is a bug which makes jobs get stuck when
            # trying to execute any mark_as_* functions with the value
            # returned from any mark_as_* function. It can only be
            # executed with the job coming in the function arguments.
            # It is due to the fact that we're stripping `job_executor`
            # property because we return the transaction job. We should look into it.
            job = cast(DataSinkKafkaJob, j.mark_as_done({}, None, final_job_sql, should_send_raw_event=False))
            job.track(output=[])
            job.send_raw_event()

        except JobCancelledException:
            job = cast(DataSinkKafkaJob, j.mark_as_cancelled(final_job_sql))
            job.track(output=[])
        except Exception as err:
            job = cast(
                DataSinkKafkaJob, j.mark_as_error({"error": str(err)}, final_job_sql, should_send_raw_event=False)
            )
            job.track(output=[], error=str(err))
            job.send_raw_event()
            raise DataSinkException(f"There was a problem while exporting data: {err}")

    def query_settings(self, workspace: Workspace) -> Dict[str, Any]:
        max_execution_time = SinkLimits.max_execution_time.get_limit_for(workspace)
        max_threads = workspace.get_limits(prefix="sinks").get("sinks_max_threads", Limit.ch_max_threads)
        max_result_bytes = workspace.get_limits(prefix="sinks").get("sinks_max_result_bytes", Limit.ch_max_result_bytes)
        output_format_parallel_formatting = workspace.get_limits(prefix="sinks").get(
            "sinks_output_format_parallel_formatting", Limit.sinks_output_format_parallel_fomatting
        )

        settings = {
            "max_execution_time": max_execution_time,
            "max_threads": max_threads,
            "max_result_bytes": max_result_bytes,
            "join_algorithm": "auto",
            "output_format_parallel_formatting": output_format_parallel_formatting,
        }

        # max_memory_usage and max_result_bytes limits are only applied
        # if they are explicitly set in Cheriff. Server limits are applied otherwise
        if max_memory_usage := workspace.get_limits(prefix="sinks").get("sinks_max_memory_usage"):
            settings["max_memory_usage"] = max_memory_usage

        if max_bytes_before_external_group_by := workspace.get_limits(prefix="sinks").get(
            "sinks_max_bytes_before_external_group_by"
        ):
            settings["max_bytes_before_external_group_by"] = max_bytes_before_external_group_by

        if max_insert_delayed_streams_for_parallel_write := workspace.get_limits(prefix="sinks").get(
            "sinks_max_insert_delayed_streams_for_parallel_write"
        ):
            settings["max_insert_delayed_streams_for_parallel_write"] = max_insert_delayed_streams_for_parallel_write

        if max_bytes_before_external_sort := workspace.get_limits(prefix="sinks").get(
            "sinks_max_bytes_before_external_sort"
        ):
            settings["max_bytes_before_external_sort"] = max_bytes_before_external_sort

        settings["log_comment"] = json.dumps(self._log_comment({"job_service": "kafka"}))

        return settings

    def create_record_to_log(
        self,
        elapsed_time: float,
        output: list[str],
        error: Optional[str] = None,
        billing: Optional[BillingDetails] = None,
    ) -> SinksExecutionLogRecord:
        workspace = Workspace.get_by_id(self.workspace_id)

        options = {
            "topic": self.topic,
            "execution_type": self.execution_type,
        }
        if hasattr(self, "job_timestamp") and self.job_timestamp:
            options["job_timestamp"] = self.job_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        if billing:
            options.update(billing.model_dump())

        resource_tags = workspace.get_tag_names_by_resource(self.pipe_id, self.pipe_name)
        return SinksExecutionLogRecord(
            workspace_id=workspace.id,
            workspace_name=workspace.name,
            workspace_database=workspace.database_server,
            workspace_cluster=workspace.cluster or "",
            query_id=self.query_id,
            timestamp=self.created_at,
            service=self.service,
            pipe_id=self.pipe_id,
            pipe_name=self.pipe_name,
            token_name=self.token_name,
            result=self._get_result_from_status(),
            elapsed_time=elapsed_time,
            error=error,
            job_id=self.id,
            output=output,
            parameters={},
            options=options,
            resource_tags=resource_tags,
        )


async def create_data_sink_job(
    job_executor: JobExecutor,
    workspace: Workspace,
    pipe: Pipe,
    data_sink: DataSink,
    sql: str,
    token_name: str,
    file_template: str = "",
    file_format: str = "",
    write_strategy: WriteStrategy = WriteStrategy.NEW,
    file_compression: str = "",
    request_id: str = "",
    execution_type: Optional[str] = ExecutionTypes.MANUAL,
    job_timestamp: Optional[datetime] = None,
):
    await DataSinkBaseJob.validate(workspace)
    job = create_job(
        workspace=workspace,
        pipe=pipe,
        sql=sql,
        file_template=file_template,
        file_format=file_format.lower(),
        file_compression=file_compression,
        token_name=token_name,
        billing_provider=job_executor._billing_provider,
        billing_region=job_executor._billing_region,
        data_sink=data_sink,
        request_id=request_id,
        execution_type=execution_type,
        write_strategy=write_strategy,
        job_timestamp=job_timestamp,
    )
    logging.info(
        f"New data sink job created: job_id={job.id}, database_server={workspace.database_server}, database={workspace.database}, sql={sql}"
    )
    job_executor.put_job(job)
    job.send_raw_event()
    return job


def create_job(
    workspace: Workspace,
    pipe: Pipe,
    data_sink: DataSink,
    sql: str,
    token_name: str,
    billing_provider: str,
    billing_region: str,
    file_template: str = "",
    file_format: str = "",
    file_compression: str = "",
    request_id: str = "",
    execution_type: Optional[str] = ExecutionTypes.MANUAL,
    write_strategy: str = "",
    job_timestamp: Optional[datetime] = None,
):
    job: DataSinkBaseJob
    match data_sink.service:
        case DataConnectors.KAFKA:
            job = DataSinkKafkaJob(
                workspace=workspace,
                pipe=pipe,
                data_sink=data_sink,
                sql=sql,
                token_name=token_name,
                billing_region=billing_region,
                billing_provider=billing_provider,
                request_id=request_id,
                execution_type=execution_type,
                write_strategy=write_strategy,
                job_timestamp=job_timestamp,
            )
        case _:
            job = DataSinkBlobStorageJob(
                workspace=workspace,
                pipe=pipe,
                sql=sql,
                file_template=file_template,
                file_format=file_format,
                file_compression=file_compression,
                token_name=token_name,
                billing_region=billing_region,
                billing_provider=billing_provider,
                data_sink=data_sink,
                request_id=request_id,
                execution_type=execution_type,
                write_strategy=write_strategy,
                job_timestamp=job_timestamp,
            )

    job.save()
    return job


def _has_tb_job_id(
    session: AWSSession,
    bucket: BucketInfo,
    file: BucketFileInfo,
    job_id: str,
    region: Optional[str],
) -> bool:
    try:
        head_response = head_object(session, bucket.name, file.path, region=region)
        return head_response.metadata.get(JOBID_METADATA_HEADER_NAME) == job_id
    except AWSClientException as error:  # We don't want this to fail loudly and break the whole process
        logging.error("Error while getting S3 Object Head for Sinks: %s", error)
        return False


def to_log_file_str(bucket_file: BucketFileInfo) -> str:
    return json.dumps({"path": bucket_file.path, "size": bucket_file.size})


def get_bucket_path(data_sink: DataSink) -> str:
    bucket_path: str = data_sink.settings.get("bucket_path", "")
    branch = data_sink.settings.get("branch", "")

    if bucket_path and branch:
        return f"{bucket_path}/branch_{branch}"

    return bucket_path


def convert_sinkjob_to_rawevent(
    sink_job: "DataSinkBaseJob", output: list[str] | None, billing_details: BillingDetails | None
) -> RawEvent:
    sink_job_metadata_options = {
        "pipe_name": sink_job.pipe_name,
        "query_id": sink_job.query_id,
        "query_sql": sink_job.sql,
        "token_name": sink_job.token_name,
        "service": sink_job.service,
        "options": sink_job.sink_job_options,
    }

    has_all_details = output is not None and billing_details is not None
    sink_job_metadata = (
        FinishedSinkJobMetadata.model_validate(
            {**sink_job_metadata_options, "output": output, "billing_details": billing_details}
        )
        if has_all_details
        else SinkJobMetadata.model_validate(sink_job_metadata_options)
    )

    job_error = sink_job.result["error"] if sink_job.status == JobStatus.ERROR and "error" in sink_job.result else None

    sink_job_log = SinkJobLog(
        job_id=sink_job.id,
        job_type="sink",
        status=JobStatusForLog(sink_job.status),
        error=job_error,
        pipe_id=sink_job.pipe_id,
        datasource_id=None,
        created_at=sink_job.created_at,
        started_at=sink_job.started_at,
        updated_at=sink_job.updated_at,
        job_metadata=sink_job_metadata,
    )

    return RawEvent(
        timestamp=datetime.utcnow(),
        workspace_id=sink_job.workspace_id,
        request_id=sink_job.request_id,
        event_type=EventType.SINK,
        event_data=sink_job_log,
    )
