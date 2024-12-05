import asyncio
import json
import logging
import re
import time
import traceback
import uuid
import zlib
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timezone
from io import BytesIO
from queue import Queue
from typing import Any, Dict, List, Optional, cast

import tornado
from pydantic import ValidationError
from streaming_form_data import StreamingFormDataParser
from streaming_form_data.targets import BaseTarget
from tornado.concurrent import run_on_executor
from tornado.httputil import parse_body_arguments

from tinybird.connector_settings import DynamoDBConnectorSetting
from tinybird.data_connectors.credentials import IAMRoleAWSCredentials, S3ConnectorCredentials
from tinybird.data_connectors.local_connectors import build_session_from_credentials
from tinybird.datasource import DatasourceTypes
from tinybird.feature_flags import FeatureFlagsWorkspaceService, FeatureFlagWorkspaces
from tinybird.hfi.utils import (
    get_error_message_and_http_code_for_ch_error_code,
    get_mv_error_not_propagated,
    is_materialized_view_error,
)
from tinybird.ingest.cdk_utils import is_cdk_service_datasource
from tinybird.ingest.data_connectors import (
    ConnectorContext,
    ConnectorException,
    GCSSAConnectorCredentials,
    GCSSAConnectorParameters,
    S3ConnectorParameters,
    S3IAMConnectorParameters,
)
from tinybird.ingest.datasource_creation import create_datasource, parse_datasource_schema
from tinybird.ingest.preview_connectors.amazon_s3_connector import S3PreviewConnector
from tinybird.ingest.preview_connectors.amazon_s3_iam_connector import S3IAMPreviewConnector
from tinybird.ingest.preview_connectors.gcs_sa_connector import GCSSAPreviewConnector
from tinybird.ingest.preview_connectors.yepcode_utils import format_date_to_iso_utc
from tinybird.integrations.dynamodb.limits import DynamoDBLimit
from tinybird.integrations.dynamodb.models import DynamoDBLinkerConfiguration, DynamoDBTableConfiguration
from tinybird.integrations.dynamodb.sync_job import create_ddb_sync_job
from tinybird.integrations.dynamodb.utils import add_item_prefix_to_jsonpath
from tinybird.iterating.branching_modes import BRANCH_MODES, BranchMode
from tinybird.iterating.hook import allow_reuse_datasource_name, install_iterating_hooks, on_create_new_datasource
from tinybird.kafka_utils import KafkaTbUtils
from tinybird.matview_checks import EngineTypes
from tinybird.ndjson import UnsupportedType, extend_json_deserialization
from tinybird.providers.aws.dynamodb import (
    DynamoDBExportConfiguration,
    DynamoDBExportDescription,
    DynamoDBTable,
    describe_table,
    export_table_to_point_in_time,
    get_dynamodb_datasource_columns,
)
from tinybird.providers.aws.exceptions import AWSClientException, PITRExportNotAvailable
from tinybird.providers.aws.session import AWSSession
from tinybird.sql import TableIndex, parse_indexes_structure, parse_table_structure
from tinybird.validation_utils import handle_pydantic_errors
from tinybird.views.api_data_linkers import add_cdk_data_linker, prepare_connector_service, update_dag
from tinybird.views.CSVDialect import dialect_from_handler
from tinybird.views.gzip_utils import has_gzip_magic_code
from tinybird.views.json_deserialize_utils import (
    KAFKA_META_COLUMNS,
    DuplicatedColumn,
    InvalidJSONPath,
    SchemaJsonpathMismatch,
    json_deserialize_merge_schema_jsonpaths,
    parse_augmented_schema,
)
from tinybird.views.multipart import CustomMultipartTarget
from tinybird.views.ndjson_importer import (
    IngestionError,
    IngestionInternalError,
    NDJSONBlockLogTracker,
    NDJSONIngester,
    PushError,
)
from tinybird.views.request_context import engine_dict
from tinybird_shared.clickhouse.errors import CHErrors

from .. import text_encoding_guessing, tracker
from ..blocks import Block, blocks_json
from ..ch import MAX_COLUMNS_SCHEMA, CSVInfo, ch_table_exists_sync
from ..ch_utils.engine import get_engine_config
from ..ch_utils.exceptions import CHException
from ..csv_guess import dialect_header_len, get_dialect, guess_delimiter, has_header
from ..csv_importer import (
    BufferedCSVProcessor,
    CSVImporterSettings,
    datasource_name_default,
    datasource_name_from_url,
    fetch_csv_extract,
)
from ..csv_processing_queue import MAX_GUESS_BYTES, CsvChunkQueueRegistry, prepare_extract
from ..data_connector import (
    VALID_AUTO_OFFSET_RESET,
    DataConnector,
    DataConnectorEngine,
    DataConnectors,
    DataConnectorSchema,
    DataLinker,
    DataSourceNotConnected,
    InvalidSettingsException,
    KafkaSettings,
)
from ..datasource import Datasource
from ..hook import (
    AppendDatasourceHook,
    CreateDatasourceHook,
    LandingDatasourceHook,
    LastDateDatasourceHook,
    PGSyncDatasourceHook,
    ReplaceDatasourceBaseHook,
    ReplaceDatasourceHook,
)
from ..hook_resources import hook_log_json
from ..job import WipJobsQueueRegistry, new_import_job
from ..limits import Limit
from ..resource import ForbiddenWordException, Resource
from ..syncasync import sync_to_async
from ..table import analyze_csv_and_create_tables_if_dont_exist, create_table_from_schema, drop_table, table_exists
from ..tokens import scopes
from ..user import ResourceAlreadyExists, User, Users
from .api_errors.data_connectors import (
    DataConnectorsClientErrorBadRequest,
    DataConnectorsClientErrorNotFound,
    DataConnectorsUnprocessable,
)
from .api_errors.datasources import (
    ClientErrorBadRequest,
    ClientErrorEntityTooLarge,
    ClientErrorForbidden,
    ClientErrorLengthRequired,
    DynamoDBDatasourceError,
    ServerErrorInternal,
)
from .api_errors.utils import build_error_summary, get_errors, validate_url_error
from .base import ApiHTTPError, BaseHandler, URLMethodSpec, authenticated, requires_write_access
from .utils import validate_redirects_and_internal_ip

MAX_ENCODING_GUESS_BYTES = int(1e5)  # 100kb
MAX_BODY_SIZE_FULL_BODY = 8
MAX_BODY_SIZE_FULL_BODY_UNITS = "MB"
MAX_BODY_SIZE_BYTES_FULL_BODY = MAX_BODY_SIZE_FULL_BODY * (1024**2)
MAX_BODY_SIZE_STREAM = 10
MAX_BODY_SIZE_STREAM_UNITS = "GB"
MAX_BODY_SIZE_BYTES_STREAM = MAX_BODY_SIZE_STREAM * (1024**3)
MAX_WAITING_BLOCKS = 3
STREAM_BACKPRESSURE_WAIT = 0.1
STREAM_BACKPRESSURE_MAX_WAIT = 5
VALID_FORMATS = {"csv", "ndjson", "parquet"}
VALID_EXTENSIONS = [
    "csv",
    "csv.gz",
    "ndjson",
    "ndjson.gz",
    "jsonl",
    "jsonl.gz",
    "json",
    "json.gz",
    "parquet",
    "parquet.gz",
]
FORMATS_WITHOUT_JSONPATHS = {"csv", "csv.gz"}


class NoData(Exception):
    pass


class CustomTarget(BaseTarget, BufferedCSVProcessor):
    def __init__(
        self,
        queue,
        workspace: "User",
        datasource: Datasource,
        block_status_log: List[Dict[str, Any]],
        decompressor,
        dialect_overrides: Dict[str, Any],
        import_id: str,
        type_guessing: bool = True,
        encoding: Optional[str] = None,
    ):
        self.workspace = workspace
        self.datasource = datasource
        self.table_name = datasource.id
        self.dialect_overrides = dialect_overrides
        self.database_server = workspace.database_server
        self.database = workspace.database
        self.queue = queue
        self.first = True
        self.dialect: Dict[str, Any] = {}
        self.block_status_log = block_status_log
        self.current_block_id: Optional[str] = None
        self.waiting_for_the_table_queue: List[Block] = []
        self.decompressor = decompressor
        self.import_id = import_id
        self.type_guessing = type_guessing
        self.cluster: Optional[str] = None
        self.csv_columns: Optional[List[Dict[str, Any]]] = None
        self.first_data_chunk_received: bool = False
        self.cluster = workspace.cluster
        self._table_exists = False
        BufferedCSVProcessor.__init__(self, dialect=dialect_overrides, encoding=encoding)
        BaseTarget.__init__(self)
        # make the initial block small so table is created as soon as possible and
        # next blocks from the stream can be processed in parallel
        if dialect_overrides.get("new_line", None) is None:
            self.chunk_size = CSVImporterSettings.BYTES_TO_GUESS_CSV

    def table_exists(self) -> bool:
        return self._table_exists

    def first_block_finished(self) -> bool:
        return any(x["status"] == "done" for x in self.block_status_log)

    def process_csv_chunk(self, csv_chunk):
        logging.info("processing chunk: %d" % len(csv_chunk))
        block_id = self.current_block_id
        with_quarantine = True
        # reset
        self.current_block_id = None
        if self.first:
            self.first = False
            if self.encoding is None:
                _, self.encoding = text_encoding_guessing.decode_with_guess(csv_chunk[:MAX_ENCODING_GUESS_BYTES])

            self.block_status_log.append(
                {"block_id": block_id, "status": "queued", "timestamp": datetime.now(timezone.utc)}
            )

            csv_chunk = csv_chunk.decode(self.encoding)
            escapechar = self.dialect_overrides.get("escapechar", None)
            fixed_extract, _, _ = prepare_extract(csv_chunk, escapechar)
            try:
                if table_exists(self.workspace, self.datasource):
                    delimiter = self.dialect_overrides["delimiter"] or guess_delimiter(fixed_extract, escapechar)
                    if has_header(fixed_extract, delimiter, escapechar)[0]:
                        csv_info = CSVInfo.extract_from_csv_extract(
                            fixed_extract,
                            dialect_overrides=self.dialect_overrides,
                            type_guessing=self.type_guessing,
                            skip_stats_collection=True,
                        )
                        dialect = csv_info.dialect
                        self.csv_columns = csv_info.columns
                    else:
                        dialect = get_dialect(fixed_extract, dialect_overrides=self.dialect_overrides)
                else:
                    csv_info = analyze_csv_and_create_tables_if_dont_exist(
                        self.workspace,
                        self.datasource,
                        fixed_extract,
                        dialect_overrides=self.dialect_overrides,
                        type_guessing=self.type_guessing,
                    )
                    dialect = csv_info.dialect
                self._table_exists = True
            except Exception as e:
                for hook in self.datasource.hooks:
                    hook.on_error(self.datasource, e)
                raise e

            self.dialect = dialect
            csv_chunk = csv_chunk[dialect_header_len(self.dialect) :]

            try:
                for hook in self.datasource.hooks:
                    hook.before_append(self.datasource)
            except Exception as e:
                logging.exception(e)
                raise Exception("failed to execute before append hooks")

            self.queue.put(
                Block(
                    id=block_id,
                    table_name=self.table_name,
                    data=csv_chunk,
                    database_server=self.database_server,
                    database=self.database,
                    cluster=self.cluster,
                    dialect=self.dialect,
                    import_id=self.import_id,
                    max_execution_time=self.workspace.get_limits(prefix="ch").get(
                        "chunk_max_execution_time", Limit.ch_chunk_max_execution_time
                    ),
                    csv_columns=self.csv_columns,
                    quarantine=with_quarantine,
                )
            )
            # once the first block is loaded set the chunk size back to
            # the regular size
            self.chunk_size = CSVImporterSettings.CHUNK_SIZE
        else:
            self.block_status_log.append(
                {"block_id": block_id, "status": "queued", "timestamp": datetime.now(timezone.utc)}
            )
            if self.first_block_finished() or self.table_exists():
                # send the blocks received while creating the table
                self.flush_waiting_blocks()
                self.queue.put(
                    Block(
                        id=block_id,
                        table_name=self.table_name,
                        data=csv_chunk.decode(self.encoding),
                        database_server=self.database_server,
                        database=self.database,
                        cluster=self.cluster,
                        dialect=self.dialect,
                        import_id=self.import_id,
                        max_execution_time=self.workspace.get_limits(prefix="ch").get(
                            "chunk_max_execution_time", Limit.ch_chunk_max_execution_time
                        ),
                        csv_columns=self.csv_columns,
                        quarantine=with_quarantine,
                    )
                )
            else:
                # first block didn't finish so table is not created
                logging.info("queued streamed block")
                self.block_status_log.append(
                    {"block_id": block_id, "status": "prequeued", "timestamp": datetime.now(timezone.utc)}
                )
                self.waiting_for_the_table_queue.append(
                    Block(
                        id=block_id,
                        table_name=self.table_name,
                        data=csv_chunk.decode(self.encoding),
                        database_server=self.database_server,
                        database=self.database,
                        cluster=self.cluster,
                        dialect=self.dialect,
                        import_id=self.import_id,
                        max_execution_time=self.workspace.get_limits(prefix="ch").get(
                            "chunk_max_execution_time", Limit.ch_chunk_max_execution_time
                        ),
                        csv_columns=self.csv_columns,
                        quarantine=with_quarantine,
                    )
                )
                if len(self.waiting_for_the_table_queue) > MAX_WAITING_BLOCKS:
                    # clean blocks
                    error_str = "Max queued blocks on stream uploading"
                    for hook in self.datasource.hooks:
                        hook.on_error(self.datasource, error_str)
                    self.waiting_for_the_table_queue = []
                    logging.error(error_str)
                    raise Exception(error_str)

    def flush_waiting_blocks(self) -> None:
        if self.first_block_finished():
            for x in self.waiting_for_the_table_queue:
                self.queue.put(x)
            self.waiting_for_the_table_queue = []

    def has_pending_blocks(self) -> bool:
        return len(self.waiting_for_the_table_queue) > 0

    def on_data_received(self, chunk: bytes) -> None:
        if not self.first_data_chunk_received:
            if has_gzip_magic_code(chunk):
                self.decompressor = zlib.decompressobj(wbits=16 + 15)
            self.first_data_chunk_received = True
        if not self.current_block_id:
            self.current_block_id = str(uuid.uuid4())
            self.block_status_log.append(
                {"block_id": self.current_block_id, "status": "receiving", "timestamp": datetime.now(timezone.utc)}
            )
        if self.decompressor:
            chunk = self.decompressor.decompress(chunk)
        self.write(chunk)

    def flush_decompress_buffer(self) -> None:
        if self.decompressor:
            chunk = self.decompressor.flush()
            if chunk:
                self.write(chunk)


class AnalyzeCustomTarget(BaseTarget):
    def __init__(self, decompressor):
        super().__init__()
        self.decompressor = decompressor
        self.buffer = BytesIO()

    def on_data_received(self, chunk: bytes) -> None:
        if len(self.buffer.getbuffer()) > MAX_GUESS_BYTES:
            return
        if self.decompressor:
            chunk = self.decompressor.decompress(chunk)
        self.buffer.write(chunk)

    def flush_decompress_buffer(self) -> None:
        if self.decompressor:
            chunk = self.decompressor.flush()
            if chunk:
                self.buffer.write(chunk)


class DatasourceCreateModes:
    CREATE = "create"
    APPEND = "append"
    REPLACE = "replace"
    MIGRATE = "migrate"

    @staticmethod
    def valid_modes():
        return set(
            [
                DatasourceCreateModes.CREATE,
                DatasourceCreateModes.APPEND,
                DatasourceCreateModes.REPLACE,
                DatasourceCreateModes.MIGRATE,
            ]
        )

    @staticmethod
    def is_valid(mode: str) -> bool:
        return mode in DatasourceCreateModes.valid_modes()


def validate_replace_condition_contains_partition(
    replace_condition: Optional[str], partition_key: Optional[str]
) -> bool:
    """
    >>> validate_replace_condition_contains_partition('toYear(date)==2020', 'toYear(date)')
    True
    >>> validate_replace_condition_contains_partition('toYear(timestamp)==2020', 'toYear(date)')
    False
    """
    return not partition_key or not replace_condition or partition_key in replace_condition


@tornado.web.stream_request_body
class APIDataSourcesImportHandler(BaseHandler):
    executor = ThreadPoolExecutor(4, thread_name_prefix="datasources_handler")

    def check_xsrf_cookie(self):
        pass

    def initialize(self):
        self.main_process_queue = CsvChunkQueueRegistry.get_or_create()
        self.block_status_log: List[Dict[str, Any]] = []
        self.processing_responses = []
        self.upload_type: str = "none"
        self.full_body: bytes = b""
        self.last_block: int = 0  # last block sent during data uploading
        self.progress: bool = False
        self.decompressor = None
        self.import_id: Optional[str] = None
        self.job_id: Optional[str] = None
        self.encoding: Optional[str] = None
        self.engine_full: Optional[str] = None
        self.first_data_chunk_received: bool = False
        self.connector: Optional[str] = None
        self.service_name: Optional[str] = None
        self.name: Optional[str] = None

    async def validate_and_set_create_params(self):
        workspace = self.get_workspace_from_db()

        if not DatasourceCreateModes.is_valid(self.mode):
            valid_modes = ",".join(DatasourceCreateModes.valid_modes())
            raise ApiHTTPError.from_request_error(
                ClientErrorBadRequest.invalid_mode(mode=self.mode, valid_modes=valid_modes)
            )

        if self.url:
            self.url = await validate_redirects_and_internal_ip(self.url, self.application.settings)

        if self.name:
            self.validate_datasource_access_mode(workspace)
            self.validate_name(workspace)

        if self.connector:
            await self.validate_connector(workspace)

        if self.schema:
            self.validate_schema()

        if self.mode == DatasourceCreateModes.REPLACE:
            self.validate_and_init_datasource_replace(workspace)

        if self.mode == DatasourceCreateModes.APPEND:
            self.validate_and_init_datasource_append(workspace)

        if self.mode == DatasourceCreateModes.CREATE:
            self.validate_engine(workspace)
            self.validate_datasource_create(workspace)

        if self.mode == DatasourceCreateModes.MIGRATE and self.connector:
            self.datasource = workspace.get_datasource(self.name)

        if (
            self.connector
            and self.data_connector.service
            not in [
                DataConnectors.AMAZON_S3,
                DataConnectors.AMAZON_S3_IAMROLE,
                DataConnectors.GCLOUD_STORAGE,
            ]
            and self.get_argument("schema", None, True) is not None
        ):
            augmented_schema = self.get_argument("schema", None, True)
            indexes = self.get_argument("indexes", None)
            parsed_schema = parse_augmented_schema(augmented_schema, remove_columns=KAFKA_META_COLUMNS)
            new_columns = parse_table_structure(parsed_schema.schema)
            self.indexes = parse_indexes_structure(indexes.splitlines() if indexes else None)
            if parsed_schema.jsonpaths:
                self.json_deserialization = json_deserialize_merge_schema_jsonpaths(
                    new_columns, parsed_schema.jsonpaths
                )
                self.schema += ", " + parsed_schema.schema
            elif (hasattr(self, "kafka_store_raw_value") and self.kafka_store_raw_value) or (
                hasattr(self, "kafka_store_headers") and self.kafka_store_headers
            ):
                self.json_deserialization = []
            else:
                raise ApiHTTPError.from_request_error(
                    ClientErrorBadRequest.missing_jsonpaths(service=self.data_connector.service)
                )
        else:
            self.json_deserialization = []

        if self.get_argument("format", "csv") not in ("ndjson", "parquet") and not self.datasource:
            branch_mode = BranchMode(
                self.get_api_option("branch_mode", BRANCH_MODES, default_option=BranchMode.NONE.value)
            )
            self.datasource = await self.create_new_datasource(
                workspace, self.json_deserialization, hooks=True, branch_mode=branch_mode
            )

    async def create_new_datasource(
        self,
        workspace: User,
        json_deserialization: Any,
        hooks: Optional[bool] = False,
        branch_mode: BranchMode = BranchMode.NONE,
    ):
        if not self.name:
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.invalid_schema_datasource_name())

        try:
            json_conf = None
            fixed_id = await on_create_new_datasource(workspace, self.name, branch_mode=branch_mode)
            if self.get_argument("format", "csv") in ("ndjson", "parquet"):
                try:
                    json_conf = json_deserialize_merge_schema_jsonpaths(
                        parse_table_structure(self.schema), self.jsonpaths
                    )
                except ValueError as e:
                    raise ApiHTTPError(400, log_message=f"Schema error. {e}. Schema={self.get_argument('schema')}")
                except SchemaJsonpathMismatch:
                    raise ApiHTTPError(
                        400,
                        log_message="mode=create with format=ndjson or format=parquet requires to set jsonpaths on the schema",
                    )
                except InvalidJSONPath as e:
                    raise ApiHTTPError(400, log_message=f"Schema error. {e}.")

                try:
                    extend_json_deserialization(json_conf)
                except UnsupportedType as e:
                    raise ApiHTTPError(400, log_message=str(e))
                except Exception as e:
                    raise ApiHTTPError(400, log_message=str(e))

            self.datasource = await Users.add_datasource_async(
                workspace,
                self.name,
                cluster=self.cluster,
                tags=self.tags,
                prefix=self.get_datasource_guid_prefix(),
                json_deserialization=json_deserialization,
                description=self.get_argument("description", ""),
                fixed_id=fixed_id,
                service_name=self.service_name,
            )
            if json_conf:
                self.datasource = Users.alter_datasource_json_deserialization(workspace, self.datasource.id, json_conf)
        except ResourceAlreadyExists as e:
            raise ApiHTTPError(409, log_message=str(e))
        except ValueError as e:
            raise ApiHTTPError(400, log_message=str(e))
        if hooks:
            self.datasource.install_hook(CreateDatasourceHook(workspace))
            install_iterating_hooks(workspace, self.datasource, branch_mode=branch_mode)
            self.datasource.install_hook(PGSyncDatasourceHook(workspace))
            self.datasource.install_hook(LandingDatasourceHook(workspace))
            self.datasource.install_hook(LastDateDatasourceHook(workspace))
        return self.datasource

    def validate_name(self, workspace: "User"):
        if not self.name:
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.invalid_schema_datasource_name())
        try:
            if not Resource.validate_name(self.name) and not workspace.is_branch:
                raise ApiHTTPError.from_request_error(
                    ClientErrorBadRequest.invalid_data_source_name(
                        name=self.name, name_help=Resource.name_help(self.name)
                    )
                )
        except ForbiddenWordException:
            raise ApiHTTPError.from_request_error(
                ClientErrorBadRequest.forbidden_data_source_name(
                    name=self.name, name_help=Resource.name_help(self.name)
                ),
                documentation="/api-reference/api-reference.html#forbidden-names",
            )
        if workspace.get_pipe(self.name):
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.invalid_pipe_name(name=self.name))

    def validate_datasource_access_mode(self, workspace: "User"):
        datasource_found = workspace.get_datasource(self.name, include_read_only=True)
        if not datasource_found:
            return
        elif datasource_found.is_read_only and not workspace.is_branch:
            raise ApiHTTPError.from_request_error(
                ClientErrorBadRequest.can_not_import_data_in_data_source_as_it_is_read_only(name=self.name)
            )

    def validate_schema(self):
        if not self.name:
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.invalid_schema_datasource_name())
        if self.mode != DatasourceCreateModes.CREATE and self.mode != DatasourceCreateModes.MIGRATE:
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.invalid_schema_mode())
        columns = parse_table_structure(self.schema)
        if len(columns) > MAX_COLUMNS_SCHEMA:
            raise ApiHTTPError.from_request_error(
                ClientErrorBadRequest.num_columns_not_supported(parameters=MAX_COLUMNS_SCHEMA)
            )

    def _get_engine_args(self):
        engine_args = {"type": self.get_argument("engine", "MergeTree")}
        for k in self.request.arguments.keys():
            if k.startswith("engine_"):
                engine_args[k[len("engine_") :]] = self.get_argument(k)
        return engine_args

    def validate_engine(self, workspace: "User"):
        if not self.engine_full:
            try:
                engine_args = self._get_engine_args()
                self.engine_full = engine_args
                get_engine_config(engine_args["type"])
            except ValueError as e:
                raise ApiHTTPError(400, str(e))

    def set_and_validate_dialect_overrides(self):
        dialect = dialect_from_handler(self)
        self.dialect_overrides = {
            "delimiter": dialect.delimiter,
            "escapechar": dialect.escapechar,
            "new_line": dialect.new_line,
        }

    def validate_and_init_datasource_replace(self, workspace: "User"):
        if not self.name:
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.invalid_data_source_replace_name())
        if not self.is_admin() and not self.has_scope(scopes.DATASOURCES_CREATE):
            raise ApiHTTPError.from_request_error(ClientErrorForbidden.invalid_data_source_token_replace())
        existing_datasource = workspace.get_datasource(self.name)
        if not existing_datasource:
            raise ApiHTTPError.from_request_error(
                ClientErrorBadRequest.nonexisting_data_source_replace_name(name=self.name)
            )

        self.existing_datasource = existing_datasource
        self.datasource = Datasource.duplicate_datasource(existing_datasource)
        partition_key = existing_datasource.engine.get("partition_key")

        if not validate_replace_condition_contains_partition(self.replace_condition, partition_key):
            logging.warning(
                f"The replace condition '{self.replace_condition}' does not contain the partition key '{partition_key}' of datasource {existing_datasource.id}."
            )

        if self.job_id is None:
            self.job_id = str(uuid.uuid4())

        self.datasource.install_hook(
            ReplaceDatasourceHook(
                workspace, existing_datasource, self.replace_options, self.replace_condition, self.job_id
            )
        )
        self.datasource.install_hook(LandingDatasourceHook(workspace))
        self.datasource.install_hook(LastDateDatasourceHook(workspace))

    def validate_topic_not_used_in_connector(
        self,
        connector_linkers: List[DataLinker],
        kafka_topic: str,
        workspace: User,
    ):
        branch_id = None
        if workspace.is_branch_or_release_from_branch:
            branch_id = workspace.origin if workspace.is_release else workspace.id

        for linker in connector_linkers:
            linker_settings = linker.settings
            if linker_settings.get("branch") != branch_id:
                # Only check linkers from the same branch
                continue
            if linker_settings["kafka_topic"] == kafka_topic:
                raise ApiHTTPError.from_request_error(
                    ClientErrorBadRequest.topic_repeated_in_branch(topic=kafka_topic, branch=workspace.name)
                    if branch_id
                    else ClientErrorBadRequest.topic_repeated_in_workspace(topic=kafka_topic, workspace=workspace.name)
                )

    async def validate_kafka_group_not_used(
        self, workspace: User, data_connector: DataConnector, kafka_topic: str, kafka_group_id: str
    ) -> None:
        response = await KafkaTbUtils.get_kafka_topic_group(workspace, data_connector, kafka_topic, kafka_group_id)
        if response.get("error") == "group_id_already_active_for_topic":
            raise ApiHTTPError.from_request_error(DataConnectorsUnprocessable.auth_groupid_in_use())
        elif response.get("error") == "connection_error":
            raise ApiHTTPError.from_request_error(
                DataConnectorsUnprocessable.unable_to_connect(error=response["error"])
            )
        elif response.get("error"):
            raise ApiHTTPError.from_request_error(
                DataConnectorsUnprocessable.auth_groupid_failed(error=response["error"])
            )

    async def validate_connector(self, workspace: "User") -> None:
        if not self.connector:
            return None

        self.data_connector: Optional[DataConnector] = DataConnector.get_by_id(self.connector)

        if not self.data_connector:
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.invalid_connector(connector=self.connector))

        branch_mode = BranchMode(self.get_api_option("branch_mode", BRANCH_MODES, default_option=BranchMode.NONE.value))
        self.datasource = workspace.get_datasource(self.name)
        if self.datasource and branch_mode == BranchMode.FORK:
            raise ApiHTTPError(
                400,
                log_message=f"Data Source {self.name} already exists.\nAt the moment, the {self.data_connector.service} datasources require a post Release https://www.tinybird.co/docs/version-control/deployment-strategies#postrelease-increment-e-g-1-0-0-to-1-0-0-1 \nTo deploy to a new Release create a different Data Source with a different name.",
            )

        if self.data_connector.service == DataConnectors.AMAZON_DYNAMODB:
            try:
                DynamoDBTableConfiguration(
                    dynamodb_table_arn=self.get_argument("dynamodb_table_arn", None),
                    dynamodb_export_bucket=self.get_argument("dynamodb_export_bucket", None),
                )
            except ValidationError as e:
                raise ApiHTTPError(400, handle_pydantic_errors(e)) from e

        if self.data_connector.service == DataConnectors.KAFKA:
            main_workspace = workspace.get_main_workspace()
            kafka_connectors = DataConnector.get_all_by_owner_and_service(main_workspace.id, "kafka")
            linkers_by_connector = {connector.id: connector.get_linkers() for connector in kafka_connectors}
            max_topics = main_workspace.get_limits(prefix="kafka").get("max_topics", Limit.kafka_max_topics)

            if sum(len(connectors) for connectors in linkers_by_connector.values()) >= max_topics:
                raise ApiHTTPError.from_request_error(ClientErrorBadRequest.max_topics_limit(max_topics=max_topics))

            self.kafka_topic = self.get_argument("kafka_topic", None)
            self.kafka_group_id = self.get_argument("kafka_group_id", None)
            if self.kafka_topic is None:
                raise ApiHTTPError.from_request_error(ClientErrorBadRequest.required_setting(setting="topic"))
            if self.kafka_group_id is None:
                raise ApiHTTPError.from_request_error(ClientErrorBadRequest.required_setting(setting="group_id"))
            self.kafka_key_avro_deserialization = self.get_argument("kafka_key_avro_deserialization", "")

            self.kafka_auto_offset_reset = self.get_argument("kafka_auto_offset_reset", KafkaSettings.AUTO_OFFSET_RESET)
            if self.kafka_auto_offset_reset not in VALID_AUTO_OFFSET_RESET:
                raise ApiHTTPError.from_request_error(
                    ClientErrorBadRequest.invalid_setting(
                        setting="kafka_auto_offset_reset", valid_values=VALID_AUTO_OFFSET_RESET
                    )
                )

            if workspace.is_branch:
                # In branches, we only consume newer messages and add a suffix to the group ids
                self.kafka_group_id = f"{self.kafka_group_id}_{workspace.name}"
                self.kafka_auto_offset_reset = "latest"

            self.kafka_store_raw_value = self.get_argument("kafka_store_raw_value", "false")
            if self.kafka_store_raw_value.lower() not in {"true", "false"}:
                raise ApiHTTPError.from_request_error(
                    ClientErrorBadRequest.invalid_setting(
                        setting="kafka_store_raw_value", valid_values={"true", "false"}
                    )
                )
            self.kafka_store_raw_value = self.kafka_store_raw_value.lower() == "true"

            self.kafka_store_headers = self.get_argument("kafka_store_headers", "false")
            if self.kafka_store_headers.lower() not in {"true", "false"}:
                raise ApiHTTPError.from_request_error(
                    ClientErrorBadRequest.invalid_setting(setting="kafka_store_headers", valid_values={"true", "false"})
                )
            self.kafka_store_headers = self.kafka_store_headers.lower() == "true"

            persistent = self.get_argument("persistent", "true").lower() == "true"
            ttl = self.get_argument("ttl", None) or self.get_argument("engine_ttl", None)

            legacy_kafka_metadata = FeatureFlagsWorkspaceService.feature_for_id(
                FeatureFlagWorkspaces.LEGACY_KAFKA_METADATA, "", workspace.feature_flags
            )
            kafka_metadata_prefix = not legacy_kafka_metadata

            user_schema = self.get_argument("schema", None, True)
            user_schema_parsed = (
                parse_augmented_schema(user_schema, remove_columns=KAFKA_META_COLUMNS).schema if user_schema else None
            )
            indexes = self.get_argument("indexes", None)
            self.indexes = parse_indexes_structure(indexes.splitlines() if indexes else None)
            kafka_schema = DataConnectorSchema.get_schema(
                service="kafka",
                kafka_metadata_prefix=kafka_metadata_prefix,
                kafka_store_headers=self.kafka_store_headers,
            )
            schema_to_check = f"{kafka_schema}, {user_schema_parsed}" if user_schema_parsed else kafka_schema

            engine_args = self._get_engine_args()
            self.engine_full = DataConnectorEngine.get_kafka_engine(
                persistent=persistent,
                ttl=ttl,
                kafka_metadata_prefix=kafka_metadata_prefix,
                engine_args=engine_args,
                schema=schema_to_check,
            )
            self.schema = kafka_schema

            self.validate_topic_not_used_in_connector(
                linkers_by_connector.get(self.connector, []), self.kafka_topic, workspace
            )
            await self.validate_kafka_group_not_used(
                workspace, self.data_connector, self.kafka_topic, self.kafka_group_id
            )

            self.service_name = DataConnectors.KAFKA

    async def add_kafka_data_linker(self, workspace: "User") -> None:
        try:
            DataLinker.get_by_datasource_id(self.datasource.id)
        except Exception:
            pass
        else:
            raise ApiHTTPError(400, f"Data source {self.datasource.name} is already linked to a connector")

        # Added validation to satisfy mypy
        if not self.data_connector or not self.data_connector.name:
            raise ApiHTTPError(400, "Invalid connector")

        token = await Users.add_data_source_connector_token_async(
            user_id=workspace.id, connector_name=self.data_connector.name, datasource=self.datasource
        )

        tb_clickhouse_table = f"{workspace.database}.{self.datasource.id}"

        legacy_kafka_metadata = workspace.feature_flags.get(FeatureFlagWorkspaces.LEGACY_KAFKA_METADATA.value, False)
        kafka_metadata_prefix = not legacy_kafka_metadata
        linker_settings = {
            "tb_datasource": self.datasource.id,
            "tb_token": token,
            "tb_clickhouse_table": tb_clickhouse_table,
            "tb_clickhouse_host": "",
            "kafka_topic": self.kafka_topic,
            "kafka_group_id": self.kafka_group_id,
            "kafka_auto_offset_reset": self.kafka_auto_offset_reset,
            "kafka_store_raw_value": self.kafka_store_raw_value,
            "kafka_store_headers": self.kafka_store_headers,
            "kafka_store_binary_headers": True,
            "tb_max_wait_seconds": KafkaSettings.MAX_WAIT_SECONDS,
            "tb_max_wait_records": KafkaSettings.MAX_WAIT_RECORDS,
            "tb_max_wait_bytes": KafkaSettings.MAX_WAIT_BYTES,
            "tb_max_partition_lag": KafkaSettings.MAX_PARTITION_LAG,
            "kafka_target_partitions": KafkaSettings.TARGET_PARTITIONS,
            "json_deserialization": self.json_deserialization,
            "linker_workers": 1,
            "metadata_with_prefix": kafka_metadata_prefix,
            "kafka_key_avro_deserialization": self.kafka_key_avro_deserialization,
            "tb_message_size_limit": None,
        }

        await DataLinker.add_linker(
            data_connector=self.data_connector,
            datasource=self.datasource,
            workspace=workspace,
            settings=linker_settings,
        )

    async def add_dynamodb_data_linker(
        self,
        workspace: "User",
        table_description: DynamoDBTable,
        json_deserialization: List[Dict[str, Any]],
        export_description: DynamoDBExportDescription,
        dynamodb_export_time: datetime,
    ) -> None:
        try:
            DataLinker.get_by_datasource_id(self.datasource.id)
        except DataSourceNotConnected:
            pass
        else:
            raise ApiHTTPError(400, f"Data source {self.datasource.name} is already linked to a connector")

        # Added validation to satisfy mypy
        if not self.data_connector or not self.data_connector.name:
            raise ApiHTTPError(400, "Invalid connector")

        linker_settings = DynamoDBLinkerConfiguration(
            tb_datasource=self.datasource.id,
            tb_clickhouse_table=f"{workspace.database}.{self.datasource.id}",
            dynamodb_table_arn=self.get_argument("dynamodb_table_arn"),
            dynamodb_export_bucket=self.get_argument("dynamodb_export_bucket"),
            dynamodb_export_time=dynamodb_export_time.isoformat(),
            initial_export_arn=export_description.export_arn,
            json_deserialization=json_deserialization,
            attribute_definitions=table_description.attribute_definitions,
        )

        data_linker = await DataLinker.add_linker(
            data_connector=self.data_connector,
            datasource=self.datasource,
            workspace=workspace,
            settings=linker_settings.model_dump(),
        )

        return data_linker

    def get_datasource_guid_prefix(self) -> str:
        if self.engine and "join" in self.engine.lower():
            return "j"
        if self.engine_full and isinstance(self.engine_full, str) and "join" in self.engine_full.lower():
            return "j"
        if (
            self.engine_full
            and isinstance(self.engine_full, dict)
            and "join" in self.engine_full.get("type", "").lower()
        ):
            return "j"
        return "t"

    def validate_datasource_create(self, workspace: "User"):
        if not self.name:
            if self.url:
                self.name = datasource_name_from_url(self.url)
            else:
                self.name = datasource_name_default()

        if self.get_argument("with_last_date", "false") == "true":
            self.tags["last_date"] = True

        # FIXME: we should have an easy way to update TAGS
        backfill_column = self.get_argument("backfill_column", None)
        if backfill_column:
            self.tags["backfill_column"] = backfill_column

        branch_mode = BranchMode(self.get_api_option("branch_mode", BRANCH_MODES, default_option=BranchMode.NONE.value))
        if (
            workspace.get_datasource(self.name)
            and not self.connector
            and not allow_reuse_datasource_name(workspace, branch_mode=branch_mode)
        ):
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.invalid_data_source_create_name(name=self.name))
        if not self.has_scope(scopes.DATASOURCES_CREATE) and not self.is_admin():
            raise ApiHTTPError.from_request_error(ClientErrorForbidden.invalid_data_source_token_create())

    def validate_and_init_datasource_append(self, workspace: "User"):
        if not self.name:
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.nonexisting_data_source_append_name())
        self.datasource = workspace.get_datasource(self.name, include_read_only=workspace.is_branch)

        if not self.is_admin() and not self.has_scope(scopes.DATASOURCES_CREATE):
            if not self.datasource:
                raise ApiHTTPError.from_request_error(ClientErrorForbidden.invalid_data_source_token_append_create())
            if self.datasource.id not in self.get_appendable_resources():
                raise ApiHTTPError.from_request_error(
                    ClientErrorForbidden.invalid_data_source_token_append(name=self.datasource.name)
                )

        if self.datasource:
            FORBIDDEN_APPEND_TO_JOIN = FeatureFlagsWorkspaceService.feature_for_id(
                FeatureFlagWorkspaces.FORBIDDEN_APPEND_TO_JOIN, "", workspace.feature_flags
            )

            if not FORBIDDEN_APPEND_TO_JOIN:
                if self.datasource.engine.get("engine") == EngineTypes.JOIN:
                    request_error = ClientErrorBadRequest.invalid_append_data_source_join(
                        datasource_name=self.datasource.name
                    )
                    raise ApiHTTPError.from_request_error(
                        request_error=request_error, documentation="/api-reference/datasource-api.html"
                    )

                dependent_join_datasources = self.datasource.get_dependent_join_datasources()

                if dependent_join_datasources:
                    parsed_dependent_datasources = []

                    for join_ds in dependent_join_datasources:
                        join_workspace = Users.get_by_id(join_ds.get("workspace", ""))
                        datasource = join_workspace.get_datasource(join_ds.get("datasource"))
                        if datasource:
                            parsed_dependent_datasources.append(f"{join_workspace.name}.{datasource.name}")

                    request_error = ClientErrorBadRequest.invalid_append_data_source_dependent_join(
                        datasource_name=f"{workspace.name}.{self.datasource.name}",
                        datasources=", ".join(parsed_dependent_datasources),
                    )

                    raise ApiHTTPError.from_request_error(
                        request_error=request_error, documentation="/api-reference/datasource-api.html"
                    )

            self.datasource.install_hook(AppendDatasourceHook(workspace))
            self.datasource.install_hook(LandingDatasourceHook(workspace))
            self.datasource.install_hook(LastDateDatasourceHook(workspace))

    def source_desc(self) -> str:
        if self.datasource.datasource_type in (DatasourceTypes.BIGQUERY, DatasourceTypes.SNOWFLAKE):
            return self.datasource.datasource_type
        if self.url:
            return self.url
        elif self.schema:
            return "schema"
        else:
            return self.upload_type

    @run_on_executor
    def wait_to_finish(self):
        if self.upload_type == "stream":
            # when the first block arrives the table is created with it but if while it's being
            # created new blocks arrive, those need to be placed in a temporal queue (they can't be added to the
            # processing queue because we don't know if table has been created)
            # we need to wait and flush blocks when table is created
            while self.target.has_pending_blocks():
                self.target.flush_waiting_blocks()
                time.sleep(0.02)
        self.queue.join()
        self.main_process_queue.remove_queue(self.queue)
        blocks = self.processing_responses

        errors, quarantined_rows, invalid_lines = get_errors(blocks)

        block_log = blocks_json(self.block_status_log)

        if errors:
            for i in range(len(errors)):
                if is_materialized_view_error(errors[i]):
                    errors[i] = get_mv_error_not_propagated(str(errors[i]))

            for hook in self.datasource.hooks:
                hook.on_error(self.datasource, build_error_summary(errors, quarantined_rows, invalid_lines, True))
        else:
            try:
                for hook in self.datasource.hooks:
                    hook.after_append(self.datasource)
            except Exception as e:
                errors.append(str(e))
                # capturing this exception, errors will be logged to hooks_log
                # so we should report them
                logging.exception(f"failed to execute post-hooks: {e}")

        workspace = self.get_workspace_from_db()

        source = self.source_desc()
        blocks_ids = [b["block_id"] for b in blocks]

        tracker.track_blocks(
            workspace=workspace,
            request_id=self._request_id,
            import_id=self._request_id,
            job_id=None,
            source=source,
            block_log=self.block_status_log,
            blocks=blocks,
            token_id="",
            datasource_id=self.datasource.id,
            datasource_name=self.datasource.name,
        )

        tracker.track_hooks(
            self.datasource.hook_log(),
            request_id=self._request_id,
            import_id=self._request_id,
            source=source,
            workspace=workspace,
        )

        tracker.track_datasource_ops(
            self.datasource.operations_log(),
            request_id=self._request_id,
            import_id=self._request_id,
            source=source,
            blocks_ids=blocks_ids,
            workspace=workspace,
            blocks=blocks,
        )

        ds = Users.get_datasource(workspace, self.datasource.name, include_read_only=workspace.is_branch)

        _ = WipJobsQueueRegistry.get_or_create().get()
        WipJobsQueueRegistry.get_or_create().task_done()

        return ds, blocks, block_log, errors, invalid_lines, quarantined_rows

    def flush_buffer(self):
        if self.upload_type == "stream":
            self.target.flush_decompress_buffer()
        elif self.upload_type == "full_body" and self.decompressor:
            chunk = self.decompressor.flush()
            if chunk:
                self.full_body += chunk

    async def control_csv_queue_backpressure(self):
        """This method checks the size of the queue in csv_processing_queue to limit the memory consumption in multipart imports.
        If the queue length is equal to the limit we slow down the receiving pace to a chunk every STREAM_BACKPRESSURE_WAIT secs.
        If the queue length is bigger than the limit, we wait up to STREAM_BACKPRESSURE_MAX_WAIT secs to consume the next chunk.
        We do not block completely the reception to avoid problems with the client.
        """
        queue_size = CsvChunkQueueRegistry.get_or_create().blocks_waiting()
        waiting_time = 0
        chunk_limit = CSVImporterSettings.MAX_MEMORY_IN_PROCESS_QUEUE // CSVImporterSettings.CHUNK_SIZE
        # slow down the reception pace
        if queue_size == chunk_limit:
            await asyncio.sleep(STREAM_BACKPRESSURE_WAIT)
        else:
            # block reception until STREAM_BACKPRESSURE_MAX_WAIT to not use more memory
            while queue_size > chunk_limit and waiting_time < STREAM_BACKPRESSURE_MAX_WAIT:
                logging.info(
                    f"waiting to get chunk for queue to reduce, estimated items: {queue_size}. import_id: {self.import_id}"
                )
                await asyncio.sleep(STREAM_BACKPRESSURE_WAIT)
                waiting_time += STREAM_BACKPRESSURE_WAIT
                queue_size = CsvChunkQueueRegistry.get_or_create().blocks_waiting()

    async def data_received(self, chunk):
        web_form = self.request.headers.get("Content-Type", None) == "application/x-www-form-urlencoded"
        if self.get_argument("format", "csv") in ("ndjson", "parquet") and not web_form:
            try:
                block = self.json_block_tracker.on_data_received()
                if self.upload_type == "stream":
                    # We are using sync_to_async just to be sure that any blocking code is executed in the thread pool
                    # When running a CSV replace, we will run some hooks that will run ON CLUSTER queries.
                    # If a replica is down, the ON CLUSTER will take longer and would block the event loop.
                    # Using sync_to_async we can run the code in the thread pool and not block the event loop.
                    await sync_to_async(self._parser.data_received)(chunk)
                else:
                    if not self.first_data_chunk_received:
                        self.first_data_chunk_received = True
                        if has_gzip_magic_code(chunk):
                            self.decompressor = zlib.decompressobj(wbits=16 + 15)
                    if self.decompressor:
                        self.json_block_tracker.on_decompressing()
                        chunk = self.decompressor.decompress(chunk)
                    self.json_importer.write(chunk)
                await self.json_importer.work(block)
            except ApiHTTPError as e:
                block_id = block["block_id"] if block else None
                self.json_block_tracker.on_error(block_id, e)
                self.json_block_tracker.on_done(block_id)
                return self.write_error(e.status_code, error=e.error_message, documentation=e.documentation)
            except Exception as e:
                error = f"NDJSON/Parquet import unhandled exception while streaming: {e}"
                logging.exception(error)
                block_id = block["block_id"] if block else None
                self.json_block_tracker.on_error(block_id, e)
                self.json_block_tracker.on_done(block_id)
                return self.write_error(500, error=error)
            return

        if self.upload_type == "stream":
            try:
                await self.control_csv_queue_backpressure()
                # We are using sync_to_asy  nc just to be sure that any blocking code is executed in the thread pool
                # When running a CSV replace, we will run some hooks that will run ON CLUSTER queries.
                # If a replica is down, the ON CLUSTER will take longer and would block the event loop.
                # Using sync_to_async we can run the code in the thread pool and not block the event loop.
                await sync_to_async(self._parser.data_received)(chunk)
            except ValueError as e:
                logging.exception(e)
                tracker.track_hooks(
                    self.datasource.hook_log(),
                    request_id=self._request_id,
                    import_id=self.import_id,
                    source="stream",
                    workspace=self._current_workspace,
                )
                tracker.track_datasource_ops(
                    self.datasource.operations_log(),
                    request_id=self._request_id,
                    import_id=self.import_id,
                    source="stream",
                    workspace=self._current_workspace,
                )
                self.main_process_queue.remove_queue(self.queue)
                return self.write_error(400, error=str(e))
            except Exception as e:
                error = ServerErrorInternal.import_problem(error=f"{e}\nTraceback: {traceback.format_exc()}").message
                tracker.track_hooks(
                    self.datasource.hook_log(),
                    request_id=self._request_id,
                    import_id=self.import_id,
                    source="stream",
                    workspace=self._current_workspace,
                )
                tracker.track_datasource_ops(
                    self.datasource.operations_log(),
                    request_id=self._request_id,
                    import_id=self.import_id,
                    source="stream",
                    workspace=self._current_workspace,
                )
                logging.exception(e)
                self.main_process_queue.remove_queue(self.queue)
                return self.write_error(500, error=error)

        elif self.upload_type == "full_body":
            if not self.first_data_chunk_received:
                self.first_data_chunk_received = True
                if has_gzip_magic_code(chunk):
                    self.decompressor = zlib.decompressobj(wbits=16 + 15)
            if self.decompressor:
                chunk = self.decompressor.decompress(chunk)
            self.full_body += chunk

        if self.progress:
            # send current status
            blocks = blocks_json(self.block_status_log)
            # write streamed json if there are new blocks
            if blocks and len(blocks) > self.last_block:
                self.write("\n".join(json.dumps(b) for b in blocks[self.last_block :]))
                self.write("\n")
                self.flush()
                self.last_block = len(blocks)

    def launch_job(self, url, format=None):
        headers = self.get_headers()
        workspace = self.get_workspace_from_db()

        if self.job_id is None:
            self.job_id = str(uuid.uuid4())
        job = new_import_job(
            job_executor=self.application.job_executor,
            url=url,
            headers=headers,
            user=workspace,
            datasource=self.datasource,
            request_id=self._request_id,
            dialect_overrides=self.dialect_overrides,
            type_guessing=self.type_guessing,
            mode=self.mode,
            job_id=self.job_id,
            replace_condition=self.replace_condition,
            format=format,
        )
        self.write_json({**self.get_job_output(job, workspace, debug=self.debug), **{"import_id": job.id}})

        self.import_id = job.id
        self.job_id = job.id

        return job

    async def _create_datasource(
        self,
        datasource: Datasource,
        schema: str,
        engine: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
        indexes: Optional[List[TableIndex]] = None,
    ):
        """
        validates schema and creates a clickhouse compatible table. It also creates a quarantine table
        """
        workspace = self.get_workspace_from_db()

        error = None
        try:
            await create_table_from_schema(
                workspace=workspace,
                datasource=datasource,
                schema=schema,
                engine=engine,
                options=options,
                indexes=indexes,
            )

        except (ValueError, CHException) as e:
            error = e
            if isinstance(e, ValueError):
                raise ApiHTTPError(400, str(e))
            if e.code == CHErrors.TABLE_ALREADY_EXISTS:
                raise ApiHTTPError.from_request_error(
                    ClientErrorBadRequest.invalid_ch_table_exists(name=datasource.name)
                )
            if e.code == CHErrors.UNKNOWN_STORAGE:
                raise ApiHTTPError.from_request_error(ClientErrorBadRequest.invalid_ch_unknown_storage(engine=engine))
            else:
                raise ApiHTTPError(400, str(e))
        finally:
            if error:
                for hook in self.datasource.hooks:
                    hook.on_error(datasource, error)
                await Users.drop_datasource_async(workspace, datasource.id)

            tracker.track_hooks(
                self.datasource.hook_log(), request_id=self._request_id, source="schema", workspace=workspace
            )

            if self.data_connector:
                tracker.track_datasource_ops(
                    self.datasource.operations_log(),
                    request_id=self._request_id,
                    source="schema",
                    connector=self.data_connector.id,
                    service=self.data_connector.service,
                    workspace=workspace,
                )
            else:
                tracker.track_datasource_ops(
                    self.datasource.operations_log(), request_id=self._request_id, source="schema", workspace=workspace
                )
        return datasource

    def get_upload_type(self):
        content_type = self.request.headers.get("content-type", "")
        if content_type.startswith("multipart/form-data"):
            return "stream"
        return "full_body"

    async def _prepare(self):
        workspace = self.get_workspace_from_db()
        self.json_workspace = workspace
        self.database_server = workspace["database_server"]
        self.database = workspace["database"]
        self.cluster = workspace["clusters"][0] if workspace["clusters"] else None
        self.datasource = None
        self.tags = {}
        self.replace_hook = None
        self.append_hook = None
        try:
            await self.get_and_validate_args()
        except DuplicatedColumn as e:
            raise ApiHTTPError(400, log_message=str(e))

    async def get_and_validate_args(self):
        self.format = self.get_argument("format", "csv")
        if self.format not in VALID_FORMATS:
            raise ApiHTTPError(400, log_message=f"Invalid format {self.format}.")
        self.mode = self.get_argument("mode", DatasourceCreateModes.CREATE)
        self.replace_condition = self.get_argument("replace_condition", None)

        self.replace_options = {}
        skip_incompatible_partition_key = self.get_argument("skip_incompatible_partition_key", None)
        if skip_incompatible_partition_key is not None:
            self.replace_options["skip_incompatible_partition_key"] = skip_incompatible_partition_key == "true"
        replace_truncate_when_empty = self.get_bool_argument(
            ReplaceDatasourceBaseHook.replace_truncate_when_empty_flag, False
        )
        if replace_truncate_when_empty is True:
            self.replace_options[ReplaceDatasourceBaseHook.replace_truncate_when_empty_flag] = (
                replace_truncate_when_empty
            )

        self.name: Optional[str] = self.get_argument("name", None)
        self.augmented_schema = self.get_argument("schema", None)
        indexes = self.get_argument("indexes", None)
        self.indexes = parse_indexes_structure(indexes.splitlines() if indexes else None)
        if self.augmented_schema:
            parsed_schema = parse_augmented_schema(self.augmented_schema)
            self.schema = parsed_schema.schema
            self.jsonpaths = parsed_schema.jsonpaths
            if (
                parsed_schema.jsonpaths is not None
                and self.get_argument("connector", None) is None
                and self.format not in ("ndjson", "parquet")
            ):
                raise ApiHTTPError(
                    400,
                    log_message="Setting jsonpaths requires to set 'format=ndjson' or 'format=parquet', but it was not set.",
                )
        else:
            self.schema = None
            self.jsonpaths = None

        self.engine = self.get_argument("engine", None)
        self.url = self.get_argument("url", None)
        self.type_guessing = self.get_argument("type_guessing", "true").lower() == "true"
        self.progress = self.get_argument("progress", "false") == "true"
        self.token_name = self._get_access_info().name
        self.debug = self.get_argument("debug", None)
        self.connector = self.get_argument("connector", None)
        self.data_connector = None

        self.encoding = self.get_charset_from_req_headers()
        self.set_and_validate_dialect_overrides()

        await self.validate_and_set_create_params()

    async def check_datasources_rate_limit(self, create_mode: Optional[bool] = None):
        schema = create_mode or self.get_argument("schema", None)
        if schema:
            await self.check_rate_limit(Limit.api_datasources_create_schema)
        else:
            await self.check_rate_limit(Limit.api_datasources_create_append_replace)

    async def prepare_ndjson(self, check_rate_limit: bool = False):
        self.json_time_start = time.time()
        await self._prepare()

        if check_rate_limit:
            await self.check_datasources_rate_limit(self.mode == DatasourceCreateModes.CREATE)

        if self.mode == DatasourceCreateModes.CREATE:
            if not self.schema:
                raise ApiHTTPError(
                    400,
                    log_message="mode=create with format=ndjson or format=parquet requires to set parameter 'schema'.",
                )
            branch_mode = BranchMode(
                self.get_api_option("branch_mode", BRANCH_MODES, default_option=BranchMode.NONE.value)
            )
            self.datasource = await self.create_new_datasource(self.json_workspace, None, branch_mode=branch_mode)
            self.datasource = Users.get_datasource(self.json_workspace, self.datasource.id)
            options = {"source": "schema", "format": self.get_argument("format")}
            workspace = self.get_workspace_from_db()
            create_hook = self.datasource.install_hook(CreateDatasourceHook(workspace))
            pgsync_hook = self.datasource.install_hook(PGSyncDatasourceHook(workspace))
            iterating_hooks = install_iterating_hooks(workspace, self.datasource, branch_mode=branch_mode)
            await self._create_datasource(
                self.datasource,
                self.schema,
                engine=self.engine_full,
                options=options,
                indexes=self.indexes,
            )
            self.datasource.uninstall_hook(create_hook)
            self.datasource.uninstall_hook(pgsync_hook)
            if iterating_hooks:
                for h in iterating_hooks:
                    self.datasource.uninstall_hook(h)
            self.json_datasource = self.datasource
        elif self.mode == DatasourceCreateModes.REPLACE:
            self.replace_hook = next(
                filter(lambda hook: isinstance(hook, ReplaceDatasourceBaseHook), self.datasource.hooks)
            )
            # Careful! Despite the name, `before_create` actually creates the staging datasource tables!
            before_append = sync_to_async(self.replace_hook.before_append)
            await before_append(self.datasource)
            before_create = sync_to_async(self.replace_hook.before_create)
            await before_create(self.datasource)
            after_create = sync_to_async(self.replace_hook.after_create)
            await after_create(self.datasource)
        elif self.mode == DatasourceCreateModes.APPEND:
            if self.datasource:
                self.append_hook = next(
                    filter(lambda hook: isinstance(hook, AppendDatasourceHook), self.datasource.hooks)
                )
            else:
                raise ApiHTTPError(
                    400,
                    log_message="NDJSON/Parquet Data Sources must be created first with 'mode=create' and including `jsonpath` in the schema in the form: `column_name` type `json:$.<jsonpath>`.",
                )
        else:
            raise ApiHTTPError(
                400, log_message="NDJSON/Parquet Data Sources supports modes: 'create', 'append', 'replace'."
            )
        if not self.datasource.json_deserialization:
            raise ApiHTTPError(
                400,
                log_message="Appending NDJSON/Parquet files to CSV Data Sources is not supported. You can't import NDJSON/Parquet to this datasource because it was created from a CSV file. If you created the datasource with `tb push datasource`, add jsonpaths to the columns, see an example here https://docs.tinybird.co/api-reference/datasource-api.html#jsonpaths",
            )
        if self.get_argument("url", None) is None:
            sample_iterations = 20 if self.mode == DatasourceCreateModes.CREATE else 10
            self.json_block_tracker = NDJSONBlockLogTracker()
            extended_json_deserialization = extend_json_deserialization(self.datasource.json_deserialization)
            self.json_importer = NDJSONIngester(
                extended_json_deserialization,
                database_server=self.database_server,
                database=self.database,
                workspace_id=self.json_workspace.id,
                datasource_id=self.datasource.id,
                pusher="lfi",
                format=self.get_argument("format"),
                sample_iterations=sample_iterations,
                import_id=self._request_id,
                block_tracker=self.json_block_tracker,
                cluster=self.json_workspace.cluster,
            )
            self.request.connection.set_max_body_size(MAX_BODY_SIZE_BYTES_STREAM)
            if self.upload_type == "stream":
                self._parser = StreamingFormDataParser(headers=self.request.headers)

                def write_cb(chunk):
                    if not self.first_data_chunk_received:
                        self.first_data_chunk_received = True
                        if has_gzip_magic_code(chunk):
                            self.decompressor = zlib.decompressobj(wbits=16 + 15)
                    if self.decompressor:
                        self.json_block_tracker.on_decompressing()
                        chunk = self.decompressor.decompress(chunk)
                    self.json_importer.write(chunk)

                self.json_multipart_target = CustomMultipartTarget(write_cb)
                self._parser.register("ndjson", self.json_multipart_target)
                self._parser.register("parquet", self.json_multipart_target)

        return True

    @authenticated
    async def prepare(self):
        try:
            self.requires_prepare_ndjson = False
            if self.request.method != "POST":
                return

            if "gzip" in self.request.headers.get("Content-Encoding", "") or "gzip" in self.request.headers.get(
                "Content-Type", ""
            ):
                self.decompressor = zlib.decompressobj(wbits=16 + 15)

            content_length_header = self.request.headers.get("content-length", None)
            self.content_length = int(content_length_header) if content_length_header else 0
            self.upload_type = self.get_upload_type()

            _format = self.get_argument("format", None)
            _service = self.get_argument("service", None)
            if self.upload_type == "full_body":
                # We limit the max full body request size.
                # For bigger uploads, you should use a multipart request.
                if not content_length_header:
                    err = ClientErrorLengthRequired.length_required()
                    return self.write_error(err.status_code, error=err.message)

                elif self.content_length > MAX_BODY_SIZE_BYTES_FULL_BODY:
                    err = ClientErrorEntityTooLarge.entity_too_large_full_body(
                        max_body_size=MAX_BODY_SIZE_FULL_BODY,
                        units=MAX_BODY_SIZE_FULL_BODY_UNITS,
                        api_host=self.application.settings["api_host"],
                    )
                    return self.write_error(
                        err.status_code,
                        error=err.message,
                        documentation="/api-reference/datasource-api.html#post--v0-datasources-?",
                    )
                web_form = self.request.headers.get("Content-Type", None) == "application/x-www-form-urlencoded"
                if _format is None or web_form:
                    # if arguments are sent in the body at this point we don't know the format yet
                    # we extract the arguments from the body in the `post` method and then call prepare_ndjson if it needs be
                    self.requires_prepare_ndjson = True
                    return

            # We want to rate limit just the POST requests
            # We check the limit for upload_type == 'full_body' in the create method
            await self.check_datasources_rate_limit()

            if _format in ("ndjson", "parquet") and _service is None:
                await self.prepare_ndjson()
                return

            await self._prepare()

            if self.schema:
                return  # schema creation does not need body/stream

            if self.url:
                # We detected some HTTP clients sending some content in the body
                # when they do a POST request. However, when using a URL, we don't
                # need to prepare the body/stream.
                return

            if self.upload_type == "stream":
                WipJobsQueueRegistry.get_or_create().put(self.upload_type)
                logging.debug("streamed upload")

                # before preparing queues and all the stuff check if content length is less than max body
                if content_length_header:
                    try:
                        if self.content_length > MAX_BODY_SIZE_BYTES_STREAM:
                            err = ClientErrorEntityTooLarge.entity_too_large_stream(
                                max_body_size=MAX_BODY_SIZE_STREAM,
                                units=MAX_BODY_SIZE_STREAM_UNITS,
                                api_host=self.application.settings["api_host"],
                            )
                            return self.write_error(
                                err.status_code,
                                error=err.message,
                                documentation="/api-reference/api-reference.html#limits",
                            )
                    except ValueError:
                        # if content-length is not an integer let the flow continue as a stream
                        pass

                self.executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="datasources_prepare_multipart")
                self.request.connection.set_max_body_size(MAX_BODY_SIZE_BYTES_STREAM)
                self._parser = StreamingFormDataParser(headers=self.request.headers)
                self.bytes_read = 0
                self.queue = Queue()
                logging.info(f"[stream] csv_process_queue Queue={id(self.queue)}")
                self.main_process_queue.process_queue(self.queue, self.processing_responses, self.block_status_log)

                workspace = self.get_workspace_from_db()

                self.target = CustomTarget(
                    self.queue,
                    workspace,
                    self.datasource,
                    self.block_status_log,
                    self.decompressor,
                    self.dialect_overrides,
                    self._request_id,
                    self.type_guessing,
                    self.encoding,
                )
                self._parser.register("csv", self.target)
        except ApiHTTPError as e:
            return self.write_error(e.status_code, error=e.error_message, documentation=e.documentation)
        except ValueError as e:
            return self.write_error(400, error=str(e))
        except Exception as e:
            error = ServerErrorInternal.import_problem(
                error=f'{str(e)}, Job id: {getattr(self, "job_id", "no job")}' f"\nTraceback: {traceback.format_exc()}"
            )
            return self.write_error(error.status_code, error=error.message)

    @run_on_executor
    def fetch_extracts(self, url: str, headers: Optional[Dict[str, str]], num_extracts: int) -> str:
        csv_extracts, new_line = fetch_csv_extract(url, headers, num_extracts)
        if csv_extracts:
            return (new_line or "").join(csv_extracts)
        return ""

    async def create_dynamodb_datasource(self):
        workspace = self.get_workspace_from_db()
        self.name: Optional[str] = self.get_argument("name", None)
        self.connector: Optional[str] = self.get_argument("connector", None)
        branch_mode = BranchMode(self.get_api_option("branch_mode", BRANCH_MODES, default_option=BranchMode.NONE.value))

        # DataSource Validations
        self.validate_name(workspace)
        self.validate_datasource_create(workspace)
        await self.validate_datasource_doesnt_exist(workspace, branch_mode)

        # Data Connector Validations
        if self.connector is None:
            raise ApiHTTPError.from_request_error(
                ClientErrorBadRequest.missing_connector(service_name=DataConnectors.AMAZON_DYNAMODB)
            )
        await self.validate_connector(workspace)

        # Get Table Definition from AWS
        table_name: str = self.get_argument("dynamodb_table_arn")
        settings = cast(DynamoDBConnectorSetting, cast(DataConnector, self.data_connector).validated_settings)
        session = cast(AWSSession, build_session_from_credentials(credentials=settings.credentials))

        def read_dynamodb_table_definition() -> DynamoDBTable:
            return describe_table(session, table_name, settings.dynamodb_iamrole_region)

        try:
            dynamodb_table = await asyncio.get_running_loop().run_in_executor(None, read_dynamodb_table_definition)
        except AWSClientException as err:
            raise ApiHTTPError.from_request_error(
                DynamoDBDatasourceError.error_while_reading_dynamodb_table(error_message=str(err))
            )

        if not dynamodb_table.has_streams_enabled():
            raise ApiHTTPError.from_request_error(DynamoDBDatasourceError.streams_not_configured(table_name=table_name))

        dynamodb_limits = workspace.get_limits(prefix="dynamodb")
        max_table_size_bytes = dynamodb_limits.get("dynamodb_max_table_size_bytes", DynamoDBLimit.max_table_size_bytes)
        max_table_write_capacity_units = dynamodb_limits.get(
            "dynamodb_max_table_write_capacity_units", DynamoDBLimit.max_table_write_capacity_units
        )

        table_size_bytes = dynamodb_table.table_size_bytes
        if table_size_bytes and table_size_bytes > max_table_size_bytes:
            raise ApiHTTPError.from_request_error(
                DynamoDBDatasourceError.table_size_exceeds_limit(
                    table_name=table_name,
                    table_gb=table_size_bytes / (1024**3),
                    limit_gb=max_table_size_bytes / (1024**3),
                )
            )

        table_wcu = dynamodb_table.table_write_capacity_units
        if table_wcu and table_wcu > max_table_write_capacity_units:
            raise ApiHTTPError.from_request_error(
                DynamoDBDatasourceError.table_write_capacity_exceeds_limit(
                    table_name=table_name,
                    table_wcu=table_wcu,
                    limit_wcu=max_table_write_capacity_units,
                )
            )

        # Schema Parsing
        current_datasource_schema = self.get_argument("schema")
        datasource_schema = f"{self.get_argument('schema')}, {get_dynamodb_datasource_columns(dynamodb_table.stream_view_type, current_datasource_schema)}"

        try:
            parsed_schema, json_deserialization = parse_datasource_schema(datasource_schema)
            self.schema = parsed_schema.schema
        except InvalidJSONPath as exc:
            exception_message = str(exc)

            if exception_message == "Invalid JSONPath: ''":
                exception_message = "Columns need to include JSONPath in the schema definition"

            raise ApiHTTPError(
                400,
                log_message=f"Schema error. {exception_message}",
                documentation="/ingest/dynamodb#2-1-create-a-data-source-file",
            )
        except SchemaJsonpathMismatch:
            raise ApiHTTPError(
                400,
                log_message="Schema error. Columns need to include JSONPath in the schema definition",
                documentation="/ingest/dynamodb#2-1-create-a-data-source-file",
            )

        if not len(json_deserialization):
            raise ApiHTTPError(
                400,
                log_message="Schema error. Columns need to have associated JSONPaths",
                documentation="/ingest/dynamodb#2-1-create-a-data-source-file",
            )

        try:
            extend_json_deserialization(parse_table_structure(datasource_schema))
        except UnsupportedType as e:
            raise ApiHTTPError(400, log_message=f"Schema error. {e}")

        indexes = self.get_argument("indexes", None)
        self.indexes = parse_indexes_structure(indexes.splitlines() if indexes else None)

        # Override some Engine Configurations to make RMT work
        ddb_key_schemas = dynamodb_table.get_key_schemas_by_type()
        try:
            self.engine_full = DataConnectorEngine.get_dynamodb_engine(
                schema=self.schema,
                ddb_key_schemas=ddb_key_schemas,
                engine_args={**self._get_engine_args(), "ver": "_timestamp", "is_deleted": "_is_deleted"},
            )
        except InvalidSettingsException as e:
            raise ApiHTTPError.from_request_error(
                DynamoDBDatasourceError.missing_ddb_property_in_sorting_key(property_name=str(e), table_name=table_name)
            )

        fixed_id = await on_create_new_datasource(workspace, self.name, branch_mode=branch_mode)

        # Trigger initial PITR export before creating the DataSource
        dynamodb_export_time = datetime.now(UTC)

        def export_dynamodb_table_to_s3() -> DynamoDBExportDescription:
            export_configuration = DynamoDBExportConfiguration(
                table_arn=table_name,
                export_time=dynamodb_export_time,
                bucket=self.get_argument("dynamodb_export_bucket"),
            )
            return export_table_to_point_in_time(session, export_configuration, settings.dynamodb_iamrole_region)

        try:
            dynamodb_export_description = await asyncio.get_running_loop().run_in_executor(
                None, export_dynamodb_table_to_s3
            )
        except PITRExportNotAvailable:
            raise ApiHTTPError.from_request_error(DynamoDBDatasourceError.pitr_not_available(table_name=table_name))
        except AWSClientException as err:
            raise ApiHTTPError.from_request_error(
                DynamoDBDatasourceError.error_while_triggering_dynamodb_export(error_message=str(err))
            )

        self.datasource: Datasource = await Users.add_datasource_async(
            workspace,
            self.name,
            cluster=workspace.cluster,
            json_deserialization=json_deserialization,
            service_name=DataConnectors.AMAZON_DYNAMODB,
            fixed_id=fixed_id,
        )
        self.datasource.install_hook(CreateDatasourceHook(workspace))
        self.datasource.install_hook(PGSyncDatasourceHook(workspace))
        install_iterating_hooks(workspace, self.datasource, branch_mode=branch_mode)

        options = {
            "source": "schema",
            "service": DataConnectors.AMAZON_DYNAMODB,
            "connector": self.connector,
        }

        self.datasource = await self._create_datasource(
            self.datasource,
            self.schema,
            engine=self.engine_full,
            options=options,
            indexes=self.indexes,
        )

        if workspace.is_branch_or_release_from_branch:
            return self.datasource, None  # don't link to Dynamo if we are in a branch

        data_linker = await self.add_dynamodb_data_linker(
            workspace,
            dynamodb_table,
            add_item_prefix_to_jsonpath(json_deserialization),
            dynamodb_export_description,
            dynamodb_export_time,
        )

        sync_job = create_ddb_sync_job(
            self.application.job_executor,
            workspace=workspace,
            datasource=self.datasource,
            data_linker=data_linker,
            request_id=self._request_id,
        )
        return self.datasource, sync_job.id

    async def validate_datasource_doesnt_exist(self, workspace: "User", branch_mode: BranchMode) -> None:
        self.datasource = workspace.get_datasource(self.name)

        if self.datasource and branch_mode == BranchMode.FORK:
            raise ApiHTTPError(
                400,
                log_message=f"Data Source {self.name} already exists.\nAt the moment, the BigQuery and Snowflake connectors require a post Release https://www.tinybird.co/docs/version-control/deployment-strategies#postrelease-increment-e-g-1-0-0-to-1-0-0-1 \nTo deploy to a new Release create a different Data Source with a different name.",
            )

        if self.datasource:
            raise ApiHTTPError(400, log_message=f"Data source {self.name} already exists.")

    async def create_cdk_datasource(self):
        workspace = self.get_workspace_from_db()
        self.name = self.get_argument("name", None)
        self.validate_name(workspace)
        self.validate_datasource_create(workspace)
        self.connector = self.get_argument("connector", None)
        self.engine = None
        self.engine_full = None
        if self.connector:
            await self.validate_connector(workspace)
        augmented_schema = self.get_argument("schema")
        indexes = self.get_argument("indexes", None)
        self.indexes = parse_indexes_structure(indexes.splitlines() if indexes else None)
        parsed_schema = parse_augmented_schema(augmented_schema)
        self.schema = parsed_schema.schema
        self.mode = DatasourceCreateModes.CREATE
        self.validate_schema()
        self.validate_engine(workspace)
        service_name = self.get_argument("service", "").lower()
        branch_mode = BranchMode(self.get_api_option("branch_mode", BRANCH_MODES, default_option=BranchMode.NONE.value))

        self.datasource = workspace.get_datasource(self.name)
        if self.datasource and branch_mode == BranchMode.FORK:
            raise ApiHTTPError(
                400,
                log_message=f"Data Source {self.name} already exists.\nAt the moment, the BigQuery and Snowflake connectors require a post Release https://www.tinybird.co/docs/version-control/deployment-strategies#postrelease-increment-e-g-1-0-0-to-1-0-0-1 \nTo deploy to a new Release create a different Data Source with a different name.",
            )
        if self.datasource:
            raise ApiHTTPError(400, log_message=f"Data source {self.name} already exists.")

        self.data_connector = self.data_connector if hasattr(self, "data_connector") else None
        service_conf, conn_params = await prepare_connector_service(
            self, workspace, service_name, self.data_connector, self.schema
        )
        ds_service_conf = service_conf if service_name == DataConnectors.BIGQUERY else None
        fixed_id = await on_create_new_datasource(workspace, self.name, branch_mode=branch_mode)

        # TODO: We should centralize this inside 1 method
        self.datasource: Datasource = await sync_to_async(Users.add_datasource_sync)(
            workspace,
            self.name,
            cluster=workspace.cluster,
            json_deserialization=None,
            service_name=service_name,
            service_conf=ds_service_conf,
            fixed_id=fixed_id,
        )
        self.datasource.install_hook(CreateDatasourceHook(workspace))
        self.datasource.install_hook(PGSyncDatasourceHook(workspace))
        install_iterating_hooks(workspace, self.datasource, branch_mode=branch_mode)

        options = {"source": "schema"}
        if self.connector:
            options["connector"] = self.connector
        if service_name:
            options["service"] = service_name

        self.datasource = await self._create_datasource(
            self.datasource,
            self.schema,
            engine=self.engine_full,
            options=options,
            indexes=self.indexes,
        )

        # TODO: This should be a Hook
        token = await add_cdk_data_linker(self.datasource, self.data_connector, conn_params, service_name, workspace)
        await update_dag(service_name, workspace, self.datasource, token, service_conf)

        return self.datasource

    @authenticated
    @requires_write_access
    async def post(self):
        """
        This endpoint supports 3 modes to enable 3 distinct operations, depending on the parameters provided:

         - Create a new Data Source with a schema
         - Append data to an existing Data Source
         - Replace data in an existing Data Source

        The mode is controlled by setting the ``mode`` parameter, for example, ``-d "mode=create"``.
        Each mode has different `rate limits <rate_limits url_>`_.

        When importing remote files by URL, if the server hosting the remote file supports HTTP Range headers, the import process will be parallelized.

        .. csv-table:: Request parameters
            :header: "KEY", "TYPE", "DESCRIPTION"
            :widths: 5, 5, 30

            mode, String,"Default: ``create``. Other modes: ``append`` and ``replace``. |br| The ``create`` mode creates a new Data Source and attempts to import the data of the CSV if a URL is provided or the body contains any data. |br| The ``append`` mode inserts the new rows provided into an existing Data Source (it will also create it if it does not exist yet). |br| The ``replace`` mode will remove the previous Data Source and its data and replace it with the new one; Pipes or queries pointing to this Data Source will immediately start returning data from the new one and without disruption once the replace operation is complete. |br|  |br| The ``create`` mode will automatically name the Data Source if no ``name`` parameter is provided; for the ``append`` and ``replace`` modes to work, the ``name`` parameter must be provided and the schema must be compatible."
            name, String, "Optional. Name of the Data Source to create, append or replace data. This parameter is mandatory when using the ``append`` or ``replace`` modes."
            url, String, "Optional. The URL of the CSV with the data to be imported"
            dialect_delimiter, String, "Optional. The one-character string separating the fields. We try to guess the delimiter based on the CSV contents using some statistics, but sometimes we fail to identify the correct one. If you know your CSV's field delimiter, you can use this parameter to explicitly define it."
            dialect_new_line, String, "Optional. The one- or two-character string separating the records. We try to guess the delimiter based on the CSV contents using some statistics, but sometimes we fail to identify the correct one. If you know your CSV's record delimiter, you can use this parameter to explicitly define it."
            dialect_escapechar, String, "Optional. The escapechar removes any special meaning from the following character. This is useful if the CSV does not use double quotes to encapsulate a column but uses double quotes in the content of a column and it is escaped with, e.g. a backslash."
            schema, String, "Optional. Data Source schema in the format 'column_name Type, column_name_2 Type2...'. When creating a Data Source with format ``ndjson`` the ``schema`` must include the ``jsonpath`` for each column, see the ``JSONPaths`` section for more details."
            engine, String, "Optional. Engine for the underlying data. Requires the ``schema`` parameter."
            engine_*, String, "Optional. Engine parameters and options, check the `Engines <https://www.tinybird.co/docs/concepts/data-sources.html#supported-engines>`_ section for more details"
            progress, String, "Default: ``false``. When using ``true`` and sending the data in the request body, Tinybird will return block status while loading using Line-delimited JSON."
            token, String, "Auth token with create or append permissions. Required only if no Bearer Authorization header is found"
            type_guessing, String, "Default: ``true`` The ``type_guessing`` parameter is not taken into account when replacing or appending data to an existing Data Source. When using ``false`` all columns are created as ``String`` otherwise it tries to guess the column types based on the CSV contents. Sometimes you are not familiar with the data and the first step is to get familiar with it: by disabling the type guessing, we enable you to quickly import everything as strings that you can explore with SQL and cast to the right type or shape in whatever way you see fit via a Pipe."
            debug, String, "Optional. Enables returning debug information from logs. It can include ``blocks``, ``block_log`` and/or ``hook_log``"
            replace_condition, String, "Optional. When used in combination with the ``replace`` mode it allows you to replace a portion of your Data Source that matches the ``replace_condition`` SQL statement with the contents of the ``url`` or query passed as a parameter. See this `guide <https://www.tinybird.co/guide/replacing-and-deleting-data#replace-data-selectively>`_ to learn more."
            replace_truncate_when_empty, Boolean, "Optional. When used in combination with the ``replace`` mode it allows truncating the Data Source when empty data is provided. Not supported when ``replace_condition`` is specified"
            format, String, "Default: ``csv``. Indicates the format of the data to be ingested in the Data Source. By default is ``csv`` and you should specify ``format=ndjson`` for NDJSON format, and ``format=parquet`` for Parquet files."

        **Examples**

        .. code-block:: bash
            :caption: Creating a CSV Data Source from a schema

            curl \\
            -H "Authorization: Bearer <DATASOURCES:CREATE token>" \\
            -X POST "https://api.tinybird.co/v0/datasources" \\
            -d "name=stocks" \\
            -d "schema=symbol String, date Date, close Float32"

        .. code-block:: bash
            :caption: Creating a CSV Data Source from a local CSV file with schema inference

            curl \\
            -H "Authorization: Bearer <DATASOURCES:CREATE token>" \\
            -X POST "https://api.tinybird.co/v0/datasources?name=stocks" \\
            -F csv=@local_file.csv

        .. code-block:: bash
            :caption: Creating a CSV Data Source from a remote CSV file with schema inference

            curl \\
            -H "Authorization: Bearer <DATASOURCES:CREATE token>" \\
            -X POST "https://api.tinybird.co/v0/datasources" \\
            -d "name=stocks" \\
            -d url='https://.../data.csv'

        .. code-block:: bash
            :caption: Creating an empty Data Source with a ReplacingMergeTree engine and custom engine settings

            curl \\
            -H "Authorization: Bearer <DATASOURCES:CREATE token>" \\
            -X POST "https://api.tinybird.co/v0/datasources" \\
            -d "schema=pk UInt64, insert_date Date, close Float32" \\
            -d "engine=ReplacingMergeTree" \\
            -d "engine_sorting_key=pk" \\
            -d "engine_ver=insert_date" \\
            -d "name=test123" \\
            -d "engine_settings=index_granularity=2048, ttl_only_drop_parts=false"

        .. code-block:: bash
            :caption: Appending data to a Data Source from a local CSV file

            curl \\
            -H "Authorization: Bearer <DATASOURCES:CREATE token>" \\
            -X POST "https://api.tinybird.co/v0/datasources?name=data_source_name&mode=append" \\
            -F csv=@local_file.csv

        .. code-block:: bash
            :caption: Appending data to a Data Source from a remote CSV file

            curl \\
            -H "Authorization: Bearer <DATASOURCES:CREATE token>" \\
            -X POST "https://api.tinybird.co/v0/datasources" \\
            -d mode='append' \\
            -d name='data_source_name' \\
            -d url='https://.../data.csv'

        .. code-block:: bash
            :caption: Replacing data with a local file

            curl \\
            -H "Authorization: Bearer <DATASOURCES:CREATE token>" \\
            -X POST "https://api.tinybird.co/v0/datasources?name=data_source_name&mode=replace" \\
            -F csv=@local_file.csv

        .. code-block:: bash
            :caption: Replacing data with a remote file from a URL

            curl \\
            -H "Authorization: Bearer <DATASOURCES:CREATE token>" \\
            -X POST "https://api.tinybird.co/v0/datasources" \\
            -d mode='replace' \\
            -d name='data_source_name' \\
            --data-urlencode "url=http://example.com/file.csv"
        """
        try:
            self.response_written = False
            if self.upload_type == "full_body":
                parse_body_arguments(
                    self.request.headers.get("Content-Type", ""), self.full_body, self.request.arguments, {}
                )

            service_name = self.get_argument("service", "").lower()
            if is_cdk_service_datasource(service_name):
                # if self.requires_prepare_ndjson:
                #     await self.prepare_ndjson()
                datasource = await self.create_cdk_datasource()
                self.write_json(
                    {
                        "datasource": datasource.to_json(),
                        "import_id": self._request_id,
                        "error": None,
                    }
                )
                return

            if service_name == DataConnectors.AMAZON_DYNAMODB:
                datasource, import_job_id = await self.create_dynamodb_datasource()
                self.write_json(
                    {
                        "datasource": datasource.to_json(),
                        "import_id": import_job_id,
                        "error": None,
                    }
                )
                return

            if service_name in [
                DataConnectors.AMAZON_S3,
                DataConnectors.AMAZON_S3_IAMROLE,
                DataConnectors.GCLOUD_STORAGE,
            ]:
                workspace = self.get_workspace_from_db()
                self.name = self.get_argument("name", None)

                self.schema = "c String `json:$.c`"  # I guess this is just to have a default, but :shrug:
                datasource_schema = self.get_argument("schema", None)

                try:
                    parsed_schema, json_deserialization = parse_datasource_schema(datasource_schema)
                    if parsed_schema:
                        self.schema = parsed_schema.schema
                except InvalidJSONPath as exc:
                    exception_message = str(exc)

                    if exception_message == "Invalid JSONPath: ''":
                        exception_message = "Columns need to include JSONPath in the schema definition"
                        raise ApiHTTPError(
                            400,
                            log_message=exception_message,
                            documentation="/ingest/s3#load-files-from-an-s3-bucket-using-the-cli",
                        )

                    raise ApiHTTPError.from_request_error(
                        ClientErrorBadRequest.missing_jsonpaths(service=service_name),
                        documentation="/ingest/s3#load-files-from-an-s3-bucket-using-the-cli",
                    )
                except SchemaJsonpathMismatch:
                    raise ApiHTTPError.from_request_error(
                        ClientErrorBadRequest.missing_jsonpaths(service=service_name),
                        documentation="/ingest/s3#load-files-from-an-s3-bucket-using-the-cli",
                    )

                indexes = self.get_argument("indexes", None)
                self.indexes = parse_indexes_structure(indexes.splitlines() if indexes else None)

                connector_id = self.get_argument("connector", None)
                data_connector = DataConnector.get_by_id(connector_id)
                if not data_connector:
                    raise ApiHTTPError.from_request_error(DataConnectorsClientErrorNotFound.no_data_connector())

                bucket_uri = self.get_argument("bucket_uri", None)
                from_time = self.get_argument("from_time", None)
                file_format = self.get_argument("format", None)

                if file_format not in FORMATS_WITHOUT_JSONPATHS and not len(json_deserialization):
                    raise ApiHTTPError(
                        400,
                        log_message="Schema error. Columns need to have associated JSONPaths",
                        documentation="/ingest/s3#load-files-from-an-s3-bucket-using-the-cli",
                    )

                if bucket_uri is None:
                    raise ApiHTTPError.from_request_error(
                        DataConnectorsClientErrorBadRequest.missing_param(param="bucket_uri")
                    )

                if file_format is not None and file_format not in VALID_EXTENSIONS:
                    raise ApiHTTPError.from_request_error(
                        DataConnectorsClientErrorBadRequest.format_not_supported(formats=["csv", "ndjson", "parquet"])
                    )
                elif file_format is None and not bool(
                    re.search(r"\.(" + "|".join(VALID_EXTENSIONS) + ")$", bucket_uri)
                ):
                    raise ApiHTTPError.from_request_error(
                        DataConnectorsClientErrorBadRequest.file_extension_not_supported(
                            extensions=VALID_EXTENSIONS, formats=["csv", "ndjson", "parquet"]
                        )
                    )

                jsonpaths_extensions = [e for e in VALID_EXTENSIONS if "csv" not in e]
                if (
                    parsed_schema
                    and not json_deserialization
                    and (
                        file_format in jsonpaths_extensions
                        or bool(re.search(r"\.(" + "|".join(jsonpaths_extensions) + ")$", bucket_uri))
                    )
                ):
                    raise ApiHTTPError.from_request_error(ClientErrorBadRequest.missing_jsonpaths(service=service_name))

                if self.name is None:
                    raise ApiHTTPError.from_request_error(
                        DataConnectorsClientErrorBadRequest.missing_param(param="name")
                    )

                try:
                    from_time = format_date_to_iso_utc(from_time) if from_time is not None else None
                except ValueError:
                    raise ApiHTTPError.from_request_error(
                        DataConnectorsClientErrorBadRequest.invalid_settings(
                            message=f"'{from_time}' isn't a valid value for parameter 'from_time'"
                        )
                    )

                # Only create S3 connections when the workspace is not a branch
                # https://gitlab.com/tinybird/analytics/-/issues/9964
                if not workspace.is_branch and service_name in [
                    DataConnectors.AMAZON_S3,
                    DataConnectors.AMAZON_S3_IAMROLE,
                    DataConnectors.GCLOUD_STORAGE,
                ]:
                    if service_name == DataConnectors.AMAZON_S3:
                        connector = ConnectorContext(S3PreviewConnector())
                        credentials = S3ConnectorCredentials(
                            access_key_id=data_connector.settings.get("s3_access_key_id"),
                            secret_access_key=data_connector.settings.get("s3_secret_access_key"),
                            region=data_connector.settings.get("s3_region"),
                        )
                        parameters = S3ConnectorParameters(
                            bucket_uri=bucket_uri, from_time=from_time, file_format=file_format
                        )

                    if service_name == DataConnectors.AMAZON_S3_IAMROLE:
                        connector = ConnectorContext(S3IAMPreviewConnector())
                        credentials = IAMRoleAWSCredentials(
                            role_arn=data_connector.settings.get("s3_iamrole_arn"),
                            external_id=data_connector.settings.get("s3_iamrole_external_id"),
                            region=data_connector.settings.get("s3_iamrole_region"),
                        )
                        parameters = S3IAMConnectorParameters(
                            bucket_uri=bucket_uri, from_time=from_time, file_format=file_format
                        )

                    if service_name == DataConnectors.GCLOUD_STORAGE:
                        connector = ConnectorContext(GCSSAPreviewConnector())
                        credentials = GCSSAConnectorCredentials(
                            private_key_id=data_connector.settings.get("gcs_private_key_id"),
                            client_x509_cert_url=data_connector.settings.get("gcs_client_x509_cert_url"),
                            project_id=data_connector.settings.get("gcs_project_id"),
                            client_id=data_connector.settings.get("gcs_client_id"),
                            client_email=data_connector.settings.get("gcs_client_email"),
                            private_key=data_connector.settings.get("gcs_private_key"),
                        )
                        parameters = GCSSAConnectorParameters(
                            bucket_uri=bucket_uri, from_time=from_time, file_format=file_format
                        )

                    try:
                        DEFAULT_CRON = "0 12 * * *"

                        cron = self.get_argument("cron", DEFAULT_CRON)

                        if not cron:
                            cron = DEFAULT_CRON

                        self.validate_engine(workspace)

                        # TODO: We should centralize everything inside 1 method.
                        try:
                            self.datasource = await create_datasource(
                                workspace,
                                self.name,
                                self.schema,
                                json_deserialization,
                                self.engine_full,
                                service_name,
                                connector=connector_id,
                                indexes=self.indexes,
                            )
                        except CHException as e:
                            raise ApiHTTPError(400, str(e))

                        token = await Users.add_data_source_connector_token_async(
                            user_id=workspace.id, connector_name=data_connector.name, datasource=self.datasource
                        )

                        linker_settings = {
                            "tb_token": token,
                            "bucket_uri": bucket_uri,
                            "mode": "append",
                            "query": None,
                            "query_autogenerated": False,
                            "cron": cron,
                            "ingest_now": True,
                            "stage": None,
                            "from_time": from_time,
                            "file_format": file_format,
                        }

                        await DataLinker.add_linker(
                            data_connector=data_connector,
                            datasource=self.datasource,
                            workspace=workspace,
                            settings=linker_settings,
                        )

                        _ = await connector.link_connector(
                            tb_token=token,
                            workspace_id=workspace.id,
                            datasource_id=self.datasource.id,
                            credentials=credentials,
                            parameters=parameters,
                            cron=cron,
                            working_zone="gcp#europe-west2",
                            tb_endpoint=self.request.host,
                        )  # TODO: get working zone from request
                        try:
                            _ = await connector.execute_now(workspace_id=workspace.id, datasource_id=self.datasource.id)
                        except Exception as e:
                            logging.error(f"Error running connector execute now: {e}")

                    except ConnectorException as e:
                        logging.error(f"Error creating preview datasource ({service_name}): {str(e)}")

                        self.clear()

                        # Delete recently created data linker
                        try:
                            if self.datasource:
                                linker = DataLinker.get_by_datasource_id(self.datasource.id)
                                if linker:
                                    DataLinker._delete(linker.id)
                        except Exception as e:
                            logging.error(f"Error deleting existing linker: {e}")

                        # Delete recently created data source
                        try:
                            if self.datasource:
                                ds_deleted = await Users.drop_datasource_async(workspace, self.datasource.id)
                                if ds_deleted:
                                    _ = await drop_table(workspace, self.datasource.id)
                        except Exception as e:
                            logging.error(f"Error deleting existing datasource: {e}")

                        if "Not all required params" in e.message:
                            raise ApiHTTPError.from_request_error(DataConnectorsClientErrorBadRequest.missing_params())

                        raise ApiHTTPError.from_request_error(
                            DataConnectorsClientErrorBadRequest.invalid_settings(message="Unknown error")
                        )
                else:
                    # TODO: We should centralize everything inside 1 method.
                    self.validate_engine(workspace)
                    self.datasource = await create_datasource(
                        workspace,
                        self.name,
                        self.schema,
                        json_deserialization,
                        self.engine_full,
                        service_name,
                        indexes=self.indexes,
                    )

                response = {
                    "datasource": self.datasource.to_json(),
                    "quarantine_rows": 0,
                    "invalid_lines": 0,
                    "error": False,
                }

                self.write_json(response)

                return response

            if self.get_argument("format", "csv") == "csv":
                self.flush_buffer()

                # We won't use the schema, just to check if it's valid
                schema = self.get_argument("schema", None)
                if schema:
                    table_structure = parse_table_structure(schema)
                    filtered_table_structure = [x for x in table_structure if x.get("jsonpath") is not None]
                    if len(table_structure) == len(filtered_table_structure):
                        try:
                            extend_json_deserialization(table_structure)
                        except UnsupportedType as e:
                            raise ApiHTTPError(400, log_message=str(e))

            if self.get_argument("format", "csv") in ("ndjson", "parquet"):
                # we set this variable in the `prepare` method
                # it indicates arguments are sent in the body and we need to prepare the ndjson stuff
                if self.requires_prepare_ndjson:
                    await self.prepare_ndjson(check_rate_limit=True)
                error = None
                datasource = self.existing_datasource if self.mode == DatasourceCreateModes.REPLACE else self.datasource
                if self.mode == DatasourceCreateModes.CREATE:
                    self.append_hook = datasource.install_hook(AppendDatasourceHook(self.json_workspace))

                if self.url is None:
                    source = None
                    if self.upload_type == "stream":
                        source = "stream"
                    elif self.upload_type == "full_body":
                        source = "full_body"  # This is half a lie. Full body is also streamed for ndjson.
                    options = {
                        "source": "schema" if source is None else source,
                        "format": self.get_argument("format"),
                    }

                    def send_error(error: str, status: int):
                        block = self.json_block_tracker.get_current_block()
                        block_id = block["block_id"]
                        self.json_block_tracker.on_error(block_id, error)
                        self.json_block_tracker.on_done(block_id)
                        self.set_status(status)
                        self.write_json(
                            {
                                "datasource": datasource.to_json(),
                                "import_id": self._request_id,
                                "quarantine_rows": self.json_importer.quarantined_rows,
                                "invalid_lines": 0,
                                "error": error,
                            }
                        )
                        self.response_written = True

                    try:
                        if self.decompressor:
                            chunk = self.decompressor.flush()
                            self.json_importer.write(chunk)
                        if self.append_hook:
                            self.append_hook.ops_log_options = {**self.append_hook.ops_log_options, **options}
                            self.append_hook.before_append(self.datasource)
                        block = self.json_block_tracker.get_current_block()
                        await self.json_importer.finish(block)

                        if (
                            self.mode != DatasourceCreateModes.CREATE
                            and not self.json_importer.written
                            and self.upload_type == "stream"
                        ):
                            err = ClientErrorBadRequest.ndjson_multipart_name()
                            return self.write_error(err.status_code, error=err.message)
                    except IngestionInternalError as e:
                        error = str(e)
                        http_code = 500
                        logging.exception(e)
                        block = self.json_block_tracker.get_current_block()
                        block_id = block["block_id"]
                        if isinstance(e, PushError):
                            ch_summaries = e.ch_summaries
                            quarantine_ch_summaries = e.ch_summaries_quarantine
                            successful_rows = sum([int(stat.summary.get("written_rows", 0)) for stat in ch_summaries])
                            quarantine_rows = sum(
                                [int(stat.summary.get("written_rows", 0)) for stat in quarantine_ch_summaries]
                            )
                            self.json_block_tracker.on_error(
                                block_id,
                                e,
                                total_rows=successful_rows,
                                quarantine_rows=quarantine_rows,
                                processing_time=0,
                                ch_summaries=ch_summaries,
                                quarantine_ch_summaries=quarantine_ch_summaries,
                            )
                        else:
                            self.json_block_tracker.on_error(block_id, e)
                        self.json_block_tracker.on_done(block_id)
                        if is_materialized_view_error(error):
                            error = get_mv_error_not_propagated(str(e))
                            http_code = 422
                        elif e.error_code:
                            error, http_code = get_error_message_and_http_code_for_ch_error_code(error, e.error_code)
                        send_error(error, http_code)
                    except IngestionError as e:
                        error = str(e)
                        logging.warning(error)
                        send_error(error, 400)
                    except Exception as e:
                        error = (
                            f"NDJSON/Parquet import unhandled exception when finishing: {e}\n{traceback.format_exc()}"
                        )
                        logging.exception(error)
                        block = self.json_block_tracker.get_current_block()
                        block_id = block["block_id"]
                        self.json_block_tracker.on_error(block_id, e)
                        self.json_block_tracker.on_done(block_id)
                else:
                    self.launch_job(self.url, self.get_argument("format"))
                    return

                if self.json_importer.written or self.mode == DatasourceCreateModes.APPEND or error:
                    if self.append_hook:
                        self.append_hook.ops_log_options = {**self.append_hook.ops_log_options, **options}
                        if error:
                            self.append_hook.on_error(datasource, error)
                        else:
                            self.append_hook.after_append(
                                self.datasource,
                                appended_rows=self.json_importer.successful_rows,
                                appended_rows_quarantine=self.json_importer.quarantined_rows,
                                elapsed_time=0,
                            )

                    if self.replace_hook:
                        self.replace_hook.ops_log_options = {**self.replace_hook.ops_log_options, **options}
                        if error:
                            self.replace_hook.on_error(datasource, error)
                        else:
                            after_append = sync_to_async(self.replace_hook.after_append)
                            await after_append(self.datasource)
                    workspace = self.get_workspace_from_db()
                    tracker.track_hooks(
                        self.datasource.hook_log(),
                        request_id=self._request_id,
                        import_id=self._request_id,
                        source=source,
                        workspace=workspace,
                    )
                    tracker.track_blocks(
                        request_id=self._request_id,
                        workspace=workspace,
                        import_id=self._request_id,
                        job_id=None,
                        source=source,
                        block_log=self.json_importer.block_tracker.block_status_log,
                        blocks=list(self.json_importer.block_tracker.blocks.values()),
                        token_id="",
                        datasource_id=datasource.id,
                        datasource_name=datasource.name,
                    )
                    tracker.track_datasource_ops(
                        self.datasource.operations_log(),
                        request_id=self._request_id,
                        source=source,
                        blocks_ids=self.json_importer.block_tracker.block_ids,
                        import_id=self._request_id,
                        workspace=workspace,
                        blocks=list(self.json_importer.block_tracker.blocks.values()),
                    )
                if self.response_written:
                    return
                if error:
                    self.write_error(500, error=error)
                    return
                if self.json_importer.quarantined_rows:
                    error = f"There was an error with file contents: {self.json_importer.quarantined_rows} rows in quarantine."
                else:
                    error = False

                self.write_json(
                    {
                        "datasource": datasource.to_json(),
                        "import_id": self._request_id,
                        "quarantine_rows": self.json_importer.quarantined_rows,
                        "invalid_lines": 0,
                        "error": error,
                    }
                )
                return

            return await self.create()
        except ApiHTTPError as e:
            return self.write_error(e.status_code, error=e.error_message, documentation=e.documentation)
        except ValueError as e:
            return self.write_error(400, error=str(e))

    def create_replace_with_empty_body(self, workspace: User):
        # This is needed for the Replace Hook to work for empty files
        if not ch_table_exists_sync(self.datasource.id, self.database_server, self.database):
            table_created = False
            for hook in self.datasource.hooks:
                table_created = table_created or hook.before_create(self.datasource)
            if not table_created:
                return self.write_error(400, error="cannot create table with empty file")
            for hook in self.datasource.hooks:
                hook.after_create(self.datasource)
        for hook in self.datasource.hooks:
            hook.before_append(self.datasource)
        for hook in self.datasource.hooks:
            hook.after_append(self.datasource)
        tracker.track_datasource_ops(
            self.datasource.operations_log(),
            request_id=self._request_id,
            import_id=self._request_id,
            source="body",
            blocks_ids=[],
            workspace=workspace,
        )

        ds = Users.get_datasource(workspace, self.datasource.name)
        response = self.build_create_response(ds, [], [], [], 0, 0)  # type: ignore[arg-type]
        self.write_json(response)

    @tornado.gen.coroutine
    def create(self):
        start = time.time()
        engine_dict.set(self.engine_full)
        workspace = self.get_workspace_from_db()

        # We assume a max request connection size, we don't want to parse body
        # arguments for large bodies.
        # Check MAX_BODY_SIZE_BYTES_FULL_BODY and the prepare method for more details.
        if self.upload_type == "full_body":
            # For full body uploads we have to delay the rate limit until we have parsed the body
            # It's not the best approach, but we need to know the mode and schema

            try:
                yield self.check_datasources_rate_limit()
            except ApiHTTPError as e:
                return self.write_error(e.status_code, error=e.error_message, documentation=e.documentation)
            except ValueError as e:
                return self.write_error(500, error=f"{e}\nTraceback: {traceback.format_exc()}")

            try:
                yield self._prepare()
            except ApiHTTPError as e:
                if e.status_code >= 500:
                    error = ServerErrorInternal.import_problem(error=str(e)).message
                    logging.exception(error)
                return self.write_error(e.status_code, error=e.error_message, documentation=e.documentation)
            except ValueError as e:
                logging.exception(e)
                return self.write_error(400, error=str(e))
            except Exception as e:
                error = ServerErrorInternal.import_problem(error=f"{e}\nTraceback: {traceback.format_exc()}").message
                logging.exception(error)
                return self.write_error(500, error=error)

        if self.mode == DatasourceCreateModes.MIGRATE:
            self.write_json(self.datasource.to_json())
            return

        if self.schema:
            self.datasource = yield self._create_datasource(
                self.datasource,
                self.schema,
                engine=self.engine_full,
                options={"source": "schema"},
                indexes=self.indexes,
            )
            if self.connector and self.data_connector.service == DataConnectors.KAFKA:
                yield self.add_kafka_data_linker(self.get_workspace_from_db())

            yield self.finish({"datasource": self.datasource.to_json()})
            return

        if self.url:
            err = validate_url_error(self.url)

            if err:
                bad = ClientErrorBadRequest.not_supported_url()
                return self.write_error(bad.status_code, error=bad.message)

            self.launch_job(self.url, self.format)
            return

        else:
            self.import_id = self._request_id
            self.job_id = None

            if self.upload_type == "stream":
                try:
                    if self.mode == DatasourceCreateModes.REPLACE and len(self.target.buffer.getbuffer()) == 0:
                        self.create_replace_with_empty_body(workspace)
                        return
                    # We are using sync_to_async just to be sure that any blocking code is executed in the thread pool
                    # When running a CSV replace, we will run some hooks that will run ON CLUSTER queries.
                    # If a replica is down, the ON CLUSTER will take longer and would block the event loop.
                    # Using sync_to_async we can run the code in the thread pool and not block the event loop.
                    yield sync_to_async(self.target.flush)()
                except (ValueError, Exception) as e:
                    # Forces exiting the queue processing loop
                    self.queue.put(None)

                    tracker.track_hooks(
                        self.datasource.hook_log(),
                        request_id=self._request_id,
                        import_id=self.import_id,
                        source="stream",
                        workspace=workspace,
                    )
                    tracker.track_datasource_ops(
                        self.datasource.operations_log(),
                        request_id=self._request_id,
                        import_id=self.import_id,
                        source="stream",
                        workspace=workspace,
                    )

                    if isinstance(e, ValueError):
                        return self.write_error(400, error=str(e))
                    else:
                        error = ServerErrorInternal.import_problem(
                            error=f"{e}\nTraceback: {traceback.format_exc()}"
                        ).message
                        logging.exception(error)
                        return self.write_error(500, error=f"{e}\nTraceback: {traceback.format_exc()}")

            elif self.upload_type == "full_body":
                if len(self.full_body) == 0:
                    self.create_replace_with_empty_body(workspace)
                    return
                WipJobsQueueRegistry.get_or_create().put(self.upload_type)
                self.executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="datasources_prepare_body")
                self.queue = Queue()

                logging.info(f"[full_body] csv_process_queue Queue={id(self.queue)}")

                self.main_process_queue.process_queue(self.queue, self.processing_responses, self.block_status_log)

                if self.encoding is not None:
                    encoding = self.encoding
                else:
                    _, encoding = text_encoding_guessing.decode_with_guess(self.full_body[:MAX_ENCODING_GUESS_BYTES])
                chunk = self.full_body.decode(encoding)
                escapechar = self.dialect_overrides.get("escapechar", None)
                fixed_extract, _, _ = prepare_extract(chunk, escapechar)

                try:
                    create_table_from_csv_async = sync_to_async(analyze_csv_and_create_tables_if_dont_exist)
                    workspace = self.get_workspace_from_db()

                    csv_info: CSVInfo = yield create_table_from_csv_async(
                        workspace,
                        self.datasource,
                        fixed_extract,
                        dialect_overrides=self.dialect_overrides,
                        type_guessing=self.type_guessing,
                    )

                    chunk = chunk[csv_info.header_len() :]

                    try:
                        for hook in self.datasource.hooks:
                            hook.before_append(self.datasource)
                    except Exception as e:
                        logging.exception(e)
                        return self.write_error(500, error="Failed to execute before append hooks")

                    with_quarantine = True

                    self.queue.put(
                        Block(
                            id=str(uuid.uuid4()),
                            table_name=self.datasource.id,
                            data=chunk,
                            database_server=self.database_server,
                            database=self.database,
                            cluster=self.cluster,
                            dialect=csv_info.dialect,
                            import_id=self._request_id,
                            max_execution_time=workspace.get_limits(prefix="ch").get(
                                "chunk_max_execution_time", Limit.ch_chunk_max_execution_time
                            ),
                            csv_columns=csv_info.columns,
                            quarantine=with_quarantine,
                        )
                    )
                except (ValueError, Exception) as e:
                    # Forces exiting the queue processing loop
                    self.queue.put(None)
                    for hook in self.datasource.hooks:
                        hook.on_error(self.datasource, e)
                    tracker.track_hooks(
                        self.datasource.hook_log(),
                        request_id=self._request_id,
                        import_id=self._request_id,
                        source="body",
                        workspace=workspace,
                    )
                    tracker.track_datasource_ops(
                        self.datasource.operations_log(),
                        request_id=self._request_id,
                        import_id=self._request_id,
                        source="body",
                        workspace=workspace,
                    )

                    if isinstance(e, ValueError):
                        return self.write_error(400, error=str(e))
                    else:
                        error = ServerErrorInternal.import_problem(
                            error=f"{e}\nTraceback: {traceback.format_exc()}"
                        ).message
                        logging.exception(error)
                        return self.write_error(500, error=f"{e}\nTraceback: {traceback.format_exc()}")
            else:
                e = f'Wrong upload type: "{self.upload_type}"'  # type: ignore
                error = ServerErrorInternal.import_problem(error=f"{e}\nTraceback: {traceback.format_exc()}").message
                logging.exception(error)
                return self.write_error(500, error=error)

            ds, blocks, block_log, errors, invalid_lines, quarantined_rows = yield self.wait_to_finish()
            response = self.build_create_response(ds, blocks, block_log, errors, invalid_lines, quarantined_rows)

            if errors:
                self.set_status(400)
            else:
                delimiter = None
                if self.upload_type == "full_body":
                    delimiter = csv_info.dialect["delimiter"]
                elif self.upload_type == "stream":
                    delimiter = self.target.dialect["delimiter"]
                if delimiter is not None:
                    workspace = self.get_workspace_from_db()
                    yield Users.cache_delimiter_used_in_datasource_async(workspace, self.datasource, delimiter)

            self.write_json(response)
        end = time.time()
        logging.info(f"import_time: {end - start}")

    def build_create_response(self, ds: Datasource, blocks, block_log, errors, invalid_lines, quarantined_rows):
        response = {
            "import_id": self.import_id,
            "datasource": ds.to_json(),
            "quarantine_rows": quarantined_rows,
            "invalid_lines": invalid_lines,
            "error": False,
        }

        if self.job_id:
            response["job_id"] = self.job_id

        if self.debug:
            if "blocks" in self.debug:
                response["blocks"] = blocks
            if "block_log" in self.debug:
                response["block_log"] = block_log
            if "hook_log" in self.debug:
                response["hook_log"] = hook_log_json(self.datasource.hook_log())

        if errors or invalid_lines > 0 or quarantined_rows > 0:
            response["error"] = build_error_summary(errors, quarantined_rows, invalid_lines)
            if errors:
                response["errors"] = errors

        return response


def handlers():
    return [
        URLMethodSpec("POST", r"/v0/datasources/?", APIDataSourcesImportHandler),
    ]
