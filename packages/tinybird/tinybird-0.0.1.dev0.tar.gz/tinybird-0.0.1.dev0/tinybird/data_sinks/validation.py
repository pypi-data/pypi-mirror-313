import asyncio
import logging
import re
import typing
from typing import Optional, cast

from croniter import croniter
from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from tinybird.ch import ch_get_columns_from_query
from tinybird.ch_utils.exceptions import CHException
from tinybird.connector_settings import S3ConnectorSetting, S3IAMConnectorSetting, SinkConnectorSettings
from tinybird.copy_pipes.validation import validate_gcs_cron_expression
from tinybird.data_connector import DataConnector, DataConnectorNotFound, DataConnectors
from tinybird.data_connectors.local_connectors import (
    build_longest_static_prefix_of_destination,
    build_session_from_credentials,
    local_connector_from_settings,
)
from tinybird.data_sinks.config import (
    DEFAULT_AVRO_COMPRESSON_CODEC,
    DEFAULT_ORC_COMPRESSON_CODEC,
    DEFAULT_PARQUET_COMPRESSON_CODEC,
    FILE_TEMPLATE_PROPERTIES_REGEX,
    SUPPORTED_AVRO_COMPRESSION_CODECS,
    SUPPORTED_COMPRESSION_CODECS,
    SUPPORTED_EXPORT_FORMATS_MAPPING,
    SUPPORTED_ORC_COMPRESSION_CODECS,
    SUPPORTED_PARQUET_COMPRESSION_CODECS,
    SUPPORTED_REGION_PREFIXES,
    SUPPORTED_WRITE_STRATEGIES,
    ExportFormat,
    UnknownCompressionCodecAlias,
    WriteStrategy,
    expand_compression_codec_alias,
)
from tinybird.data_sinks.limits import SinkLimits, SinkScheduleFrequencyLimitExceeded
from tinybird.integrations.s3 import get_aws_session_name
from tinybird.pipe import Pipe, PipeNode, PipeTypes
from tinybird.providers.aws.exceptions import (
    AuthenticationFailed,
    AWSClientException,
    Forbidden,
    InvalidRegionName,
    NoSuchBucket,
)
from tinybird.providers.aws.s3 import list_objects
from tinybird.providers.aws.session import AWSSession
from tinybird.providers.gcp.session import GCPSession
from tinybird.providers.gcp.storage import list_blobs
from tinybird.resource import ForbiddenWordException
from tinybird.sql_template import TemplateExecutionResults
from tinybird.user import User as Workspace
from tinybird.views.api_errors.data_connectors import DataConnectorsClientErrorNotFound
from tinybird.views.api_errors.pipes import INVALID_CRON_MESSAGE, INVALID_CRON_WITHOUT_RANGE_MESSAGE, DataSinkError
from tinybird.views.base import ApiHTTPError
from tinybird.views.shared.utils import NodeUtils as SharedNodeUtils
from tinybird_shared.clickhouse.errors import CHErrors


class SinkJobValidationTimeoutExceeded(Exception):
    pass


async def validate_file_template_columns_or_raise(
    workspace: Workspace, pipe: Optional[Pipe], node_sql: str, file_template: str, variable_names: set[str]
) -> None:
    if "{" not in file_template or "}" not in file_template:
        return

    column_matches = re.findall(FILE_TEMPLATE_PROPERTIES_REGEX, file_template)
    file_template_column_names = set([column[0] for column in column_matches if not column[0].isdigit()])

    # Check if columns are defined in node sql
    sql, _ = await workspace.replace_tables_async(
        node_sql,
        pipe=pipe,
        use_pipe_nodes=True,
        extra_replacements={},
        template_execution_results=TemplateExecutionResults(),
    )
    try:
        query_columns = await ch_get_columns_from_query(
            workspace.database_server,
            workspace.database,
            sql,
            max_execution_time=SinkLimits.max_execution_time.get_limit_for(workspace),
        )
    except CHException as err:
        if err.code == CHErrors.TIMEOUT_EXCEEDED:
            raise SinkJobValidationTimeoutExceeded(err) from err
        raise
    query_column_names: set[str] = set([column.get("name", "") for column in query_columns])
    query_column_types = {column["name"]: column["type"] for column in query_columns}

    # Get columns that are not in the provided query
    missing_columns_or_parameters = file_template_column_names.difference(query_column_names, variable_names)

    if len(missing_columns_or_parameters):
        interpolated_properties = "', '".join(missing_columns_or_parameters)
        interpolated_valid_columns = "', '".join(query_column_names)
        raise ApiHTTPError.from_request_error(
            DataSinkError.missing_parameters_or_invalid_columns_in_file_template(
                missing_columns=interpolated_properties, valid_columns=interpolated_valid_columns
            )
        )

    # Validate that date format in dynamic properties is used on date columns
    date_format_in_nondate_column = next(
        (
            (column_name, date_format, query_column_types.get(column_name, ""))
            for column_name, _, date_format, _ in column_matches
            if date_format and not query_column_types.get(column_name, "").startswith("Date")
        ),
        None,
    )

    if date_format_in_nondate_column:
        column_name, date_format, column_type = date_format_in_nondate_column
        raise ApiHTTPError.from_request_error(
            DataSinkError.date_format_used_in_nondate_column(
                column=column_name, date_format=date_format, column_type=column_type
            )
        )


class DataSinkPipeDryRunRequest(BaseModel):
    schedule_cron: Optional[str] = None
    workspace: Workspace
    override: bool
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_validator(mode="after")
    def validate_scheduled_cron(self) -> "DataSinkPipeDryRunRequest":
        if not self.schedule_cron:
            return self
        if not croniter.is_valid(self.schedule_cron):
            raise ValueError(f"Invalid schedule_cron {self.schedule_cron}")
        try:
            SinkLimits.max_scheduled_job_frequency.evaluate(self.workspace, self.schedule_cron)
        except SinkScheduleFrequencyLimitExceeded:
            err_params = SinkLimits.max_scheduled_job_frequency.get_error_message_params(self.workspace)
            raise ValueError(
                "The specified cron expression schedules sink jobs exceeding the allowable rate limit. "
                f"According to the imposed limit, only one sink job per pipe may be scheduled every {err_params['cron_schedule_limit']} seconds. "
                f'To adhere to this limit, the recommended cron expression is "{err_params["cron_recommendation"]}".'
            )
        return self

    @model_validator(mode="after")
    def validate_max_sink(self) -> "DataSinkPipeDryRunRequest":
        if not self.override and SinkLimits.max_sink_pipes.is_limit_reached(self.workspace):
            raise ApiHTTPError.from_request_error(DataSinkError.max_amount_reached())
        return self


class DataSinkPipeRequest(DataSinkPipeDryRunRequest):
    connection_name: str
    ignore_sql_errors: bool
    file_format: str
    api_host: str
    new_node: PipeNode
    new_pipe: Pipe
    new_pipe_name: str
    original_pipe: Optional[Pipe] = None

    @property
    def data_connector(self) -> DataConnector:
        try:
            return _recursively_search_connector_by_name(self.workspace, self.connection_name)
        except DataConnectorNotFound as err:
            req_err = DataConnectorsClientErrorNotFound.no_data_connector()
            raise ApiHTTPError.from_request_error(req_err) from err


class DataSinkPipeRequestKafka(DataSinkPipeRequest):
    topic: str


class DataSinkPipeRequestBlobStorage(DataSinkPipeRequest):
    file_template: str
    path: str
    write_strategy: WriteStrategy
    compression: Optional[str] = None

    @model_validator(mode="after")
    def validate_bucket_path(self) -> "DataSinkPipeRequestBlobStorage":
        if self.data_connector.service in (
            DataConnectors.GCLOUD_STORAGE_HMAC,
            DataConnectors.GCLOUD_STORAGE_SA,
        ) and not re.match(r"(gc?s://)(.*)", self.path):
            raise ValueError(
                f'"{self.path}" is not a valid bucket path for Google Cloud Storage. Try again with this format: gs://<bucket-path>'
            )
        if (
            self.data_connector.service == DataConnectors.AMAZON_S3
            or self.data_connector.service == DataConnectors.AMAZON_S3_IAMROLE
        ) and not re.match(r"(s3://)(.*)", self.path):
            raise ValueError(
                f'"{self.path}" is not a valid bucket path for Amazon S3. Try again with this format: s3://<bucket-path>'
            )

        return self

    @model_validator(mode="after")
    def validate_region_is_whitelisted(self) -> "DataSinkPipeRequestBlobStorage":
        connector_settings = self.data_connector.validated_settings
        if isinstance(connector_settings, S3IAMConnectorSetting | S3ConnectorSetting):
            region = connector_settings.get_region()
            if not region.startswith(tuple(SUPPORTED_REGION_PREFIXES)):
                raise ValueError(f"Region '{region}' is not supported for sink pipes.")
        return self

    @field_validator("file_format", mode="before")
    @classmethod
    def validate_file_format(cls, v: str) -> str:
        if v and v.lower() not in SUPPORTED_EXPORT_FORMATS_MAPPING:
            err_msg = (
                f"Export format not supported: '{v}'. Must be one of: {', '.join(SUPPORTED_EXPORT_FORMATS_MAPPING)}"
            )
            raise ValueError(err_msg)
        return v.lower()

    @field_validator("write_strategy", mode="before")
    @classmethod
    def validate_write_strategy(cls, v: str) -> str:
        if v and v.lower() not in SUPPORTED_WRITE_STRATEGIES:
            err_msg = f"Export strategy not supported: '{v}'. Must be one of: {', '.join(SUPPORTED_WRITE_STRATEGIES)}"
            raise ValueError(err_msg)
        return v.lower()

    @field_validator("compression", mode="before")
    @classmethod
    def expand_compression_alias(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        try:
            return expand_compression_codec_alias(v.lower())
        except UnknownCompressionCodecAlias:
            return v.lower()

    @model_validator(mode="after")
    def validate_codec_is_supported_by_compression_and_apply_defaults(self) -> typing.Self:
        if self.compression:
            validate_compression_codec(self.compression, self.file_format)
        elif self.file_format == ExportFormat.PARQUET:
            self.compression = DEFAULT_PARQUET_COMPRESSON_CODEC
        elif self.file_format == ExportFormat.ORC:
            self.compression = DEFAULT_ORC_COMPRESSON_CODEC
        elif self.file_format == ExportFormat.AVRO:
            self.compression = DEFAULT_AVRO_COMPRESSON_CODEC
        else:
            self.compression = "none"
        return self

    @field_validator("new_pipe")
    @classmethod
    def validate_new_pipe(cls, v: Pipe) -> Pipe:
        if v.pipe_type == PipeTypes.DATA_SINK:
            raise ValueError(
                f"Pipe {v.id} cannot be set to sink because it already is set as sink, kindly update the pipe instead"
            )

        if v.pipe_type != PipeTypes.DEFAULT:
            raise ValueError(f"Pipe {v.id} cannot be set to sink because it already is set as {v.pipe_type}")
        return v


class DataSinkScheduleUpdateRequest(BaseModel):
    schedule_cron: str | None = None

    @field_validator("schedule_cron")
    @classmethod
    def validate_schedule_cron(cls, cron: str | None) -> str | None:
        if not cron or cron.lower() in ["none", "@on-demand"]:
            return None

        # validate cron expression
        if not croniter.is_valid(cron):
            message = INVALID_CRON_MESSAGE.format(schedule_cron=cron)
            raise ValueError(message)

        # validate cron expression for gcs
        suggested_cron = validate_gcs_cron_expression(cron)
        if suggested_cron is not None:
            message = INVALID_CRON_WITHOUT_RANGE_MESSAGE.format(
                schedule_cron=cron,
                suggested_cron=suggested_cron,
            )
            raise ValueError(message)

        return cron


def validate_compression_codec(codec: str, file_format: str) -> None:
    if ExportFormat.PARQUET == file_format.lower():
        if codec.lower() not in SUPPORTED_PARQUET_COMPRESSION_CODECS:
            raise ValueError(
                f"Invalid compression for parquet file '{codec}'. "
                f"Use a valid or supported compression from {SUPPORTED_PARQUET_COMPRESSION_CODECS} or contact us at support@tinybird.co"
            )
    elif ExportFormat.ORC == file_format.lower():
        if codec.lower() not in SUPPORTED_ORC_COMPRESSION_CODECS:
            raise ValueError(
                f"Invalid compression for ORC file '{codec}'. "
                f"Use a valid or supported compression from {SUPPORTED_ORC_COMPRESSION_CODECS} or contact us at support@tinybird.co"
            )
    elif ExportFormat.AVRO == file_format.lower():
        if codec.lower() not in SUPPORTED_AVRO_COMPRESSION_CODECS:
            raise ValueError(
                f"Invalid compression for AVRO file '{codec}'. "
                f"Use a valid or supported compression from {SUPPORTED_AVRO_COMPRESSION_CODECS} or contact us at support@tinybird.co"
            )
    else:
        if codec.lower() not in SUPPORTED_COMPRESSION_CODECS:
            raise ValueError(
                f"Invalid compression '{codec}'. "
                f"Please use a valid or supported compression from {SUPPORTED_COMPRESSION_CODECS} or contact us at support@tinybird.co"
            )


def _recursively_search_connector_by_name(workspace: Workspace, connector_name: str):
    if connector := DataConnector.get_by_owner_and_name(workspace.id, connector_name):
        return connector
    if workspace.origin and (connector := DataConnector.get_by_owner_and_name(workspace.origin, connector_name)):
        return connector
    raise DataConnectorNotFound(connector_name)


async def _assert_can_read_from_target_location(
    workspace: Workspace, connector: DataConnector, path: str, file_template: str
) -> None:
    settings = cast(SinkConnectorSettings, connector.validated_settings)
    local_connector = local_connector_from_settings(settings)
    bucket_info = local_connector.get_bucket_info(settings.credentials, path)
    prefix = build_longest_static_prefix_of_destination(bucket_info.prefix, file_template)
    region = None if "unknown" == settings.get_region() else settings.get_region()

    def inner_func() -> None:
        session = build_session_from_credentials(
            settings.credentials, session_name=get_aws_session_name(workspace), endpoint_url=settings.endpoint_url
        )
        if isinstance(session, AWSSession):
            # We try to fetch 1 key because we only need to check if we can't read, this way we avoid listing up to 1k objets.
            list_objects(session, bucket_info.name, prefix=prefix, region=region, max_keys=1)
        elif isinstance(session, GCPSession):
            list_blobs(session, bucket_info.name, prefix=prefix, max_results=1)

    await asyncio.get_running_loop().run_in_executor(None, inner_func)


async def validate_sink_pipe(
    service: str,
    connection_name: str,
    file_template: str,
    ignore_sql_errors: bool,
    path: str,
    file_format: str,
    topic: str,
    workspace: Workspace,
    api_host: str,
    new_node: PipeNode,
    new_pipe: Pipe,
    new_pipe_name: str,
    override: bool,
    write_strategy: WriteStrategy = WriteStrategy.NEW,
    original_pipe: Optional[Pipe] = None,
    schedule_cron: Optional[str] = None,
    compression: Optional[str] = None,
) -> DataSinkPipeRequest:
    if not ignore_sql_errors:
        try:
            await SharedNodeUtils.validate_node_sql(workspace, new_pipe, new_node)
        except ForbiddenWordException as e:
            raise ApiHTTPError(400, str(e))

    if service == DataConnectors.KAFKA:
        return DataSinkPipeRequestKafka(
            connection_name=connection_name,
            ignore_sql_errors=ignore_sql_errors,
            topic=topic,
            schedule_cron=schedule_cron,
            workspace=workspace,
            api_host=api_host,
            original_pipe=original_pipe,
            file_format=file_format,
            override=override,
            new_node=new_node,
            new_pipe=new_pipe,
            new_pipe_name=new_pipe_name,
        )

    result = DataSinkPipeRequestBlobStorage(
        connection_name=connection_name,
        file_template=file_template,
        ignore_sql_errors=ignore_sql_errors,
        compression=compression,
        path=path,
        schedule_cron=schedule_cron,
        workspace=workspace,
        api_host=api_host,
        original_pipe=original_pipe,
        file_format=file_format,
        override=override,
        new_node=new_node,
        new_pipe=new_pipe,
        new_pipe_name=new_pipe_name,
        write_strategy=write_strategy,
    )

    try:
        await _assert_can_read_from_target_location(workspace, result.data_connector, path, file_template)
    except NoSuchBucket as err:
        req_err = DataSinkError.no_such_bucket(bucket=err)
        raise ApiHTTPError.from_request_error(req_err) from err
    except AuthenticationFailed as err:  # 401
        req_err = DataSinkError.authentication_failed(message=err)
        raise ApiHTTPError.from_request_error(req_err) from err
    except Forbidden as err:  # 403
        req_err = DataSinkError.forbidden(message=err)
        raise ApiHTTPError.from_request_error(req_err) from err
    except InvalidRegionName as err:  # 400
        raise ApiHTTPError(400, str(err)) from err
    except AWSClientException as err:  # 500
        logging.exception(f"Unexpected Boto3 client error: {err}")
        raise ApiHTTPError(500, "Internal server error") from err
    return result


def dry_run_validate_sink_pipe(
    override: bool, workspace: Workspace, schedule_cron: Optional[str] = None
) -> DataSinkPipeDryRunRequest:
    return DataSinkPipeDryRunRequest(override=override, workspace=workspace, schedule_cron=schedule_cron)
