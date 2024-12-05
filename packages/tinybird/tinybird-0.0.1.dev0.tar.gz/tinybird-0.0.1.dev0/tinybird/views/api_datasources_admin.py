import asyncio
import csv
import json
import logging
import random
import re
import zlib
from dataclasses import asdict
from datetime import datetime, timezone
from distutils import util
from io import StringIO
from typing import Any, Dict, List, Optional, cast

import aiohttp
import googleapiclient.errors
import orjson
import pyarrow.parquet as pq
import tornado
from attr import dataclass
from packaging import version
from streaming_form_data.parser import StreamingFormDataParser
from tornado.web import url

import tinybird.views.shared.utils as SharedUtils
from tinybird.ch import ch_analyze_from_url, ch_wait_for_mutations
from tinybird.ch_utils.ddl import DDL_OUTPUT_MODE_NULL_STATUS_ON_TIMEOUT
from tinybird.ch_utils.engine import TableDetails
from tinybird.csv_guess import get_dialect
from tinybird.csv_importer import CSVImporterSettings
from tinybird.csv_processing_queue import cut_csv_extract, process_chunk
from tinybird.datasource_metrics import DataSourceMetrics
from tinybird.datasource_recommendations import DataSourceRecommendations
from tinybird.datasource_service import DatasourceService
from tinybird.feature_flags import FeatureFlagsWorkspaceService, FeatureFlagWorkspaces
from tinybird.guess_analyze import analyze, analyze_query, process_analyze_query_result
from tinybird.ingest.data_connectors import ConnectorException
from tinybird.ingest.external_datasources.admin import get_or_create_workspace_service_account
from tinybird.integrations.dynamodb.utils import add_item_prefix_to_jsonpath
from tinybird.iterating.branching_modes import BRANCH_MODES, BranchMode
from tinybird.iterating.hook import allow_force_delete_materialized_views
from tinybird.ndjson import UnsupportedType, extend_json_deserialization
from tinybird.pipe import DependentCopyPipeException, DependentMaterializedNodeException, parse_dependencies
from tinybird.sql import TableIndex, schema_to_sql_columns
from tinybird.sql_template import SQLTemplateException
from tinybird.text_encoding_guessing import decode_with_guess
from tinybird.user_workspace import UserWorkspaceRelationship
from tinybird.views.aiohttp_shared_session import get_shared_session
from tinybird.views.api_data_linkers import add_cdk_data_linker, prepare_connector_service, update_dag
from tinybird.views.api_errors import RequestErrorException
from tinybird.views.api_errors.data_connectors import DataConnectorsClientErrorBadRequest
from tinybird.views.api_errors.utils import replace_table_id_with_datasource_id
from tinybird.views.block_tracker import DummyBlockLogTracker
from tinybird.views.ch_local import ch_local_query
from tinybird.views.CSVDialect import dialect_from_handler
from tinybird.views.entities_datafiles import generate_datasource_datafile
from tinybird.views.gzip_utils import has_gzip_magic_code, is_gzip_file
from tinybird.views.json_deserialize_utils import (
    DYNAMODB_META_COLUMNS,
    KAFKA_META_COLUMNS,
    InvalidJSONPath,
    SchemaJsonpathMismatch,
    json_deserialize_merge_schema_jsonpaths,
    parse_augmented_schema,
)
from tinybird.views.multipart import CustomMultipartTarget
from tinybird.views.ndjson_importer import IngestionError, NDJSONIngester, SingleChunker
from tinybird.views.utils import is_valid_json, split_ndjson, validate_redirects_and_internal_ip
from tinybird_shared.clickhouse.errors import CHErrors
from tinybird_shared.retry.retry import retry_ondemand_async

from .. import tracker
from ..ch import (
    FALLBACK_PARTITION_COLUMN,
    WAIT_ALTER_REPLICATION_OWN,
    CHAnalyzeError,
    CSVInfo,
    HTTPClient,
    TablesToSwapWithWorkspace,
    ch_many_tables_details_async,
    ch_swap_tables,
    ch_table_details_async,
    ch_table_exists_async,
    ch_truncate_table_with_fallback,
    rows_affected_by_delete,
    table_structure,
)
from ..ch_utils.exceptions import CHException, CHLocalException
from ..data_connector import DataConnector, DataConnectors, DataConnectorSchema, DataLinker, DataSourceNotConnected
from ..datasource import Datasource, SharedDatasource, get_datasources_internal_ids
from ..hook import (
    AlterDatasourceHook,
    DeleteDatasourceHook,
    LandingDatasourceHook,
    LastDateDatasourceHook,
    PGSyncDatasourceHook,
    TruncateDatasourceHook,
    get_partial_replace_dependencies,
)
from ..job import new_delete_job
from ..limits import GB, FileSizeException, Limit
from ..plan_limits.delete import DeleteLimits
from ..sql import engine_supports_delete, parse_indexes_structure, parse_table_structure
from ..syncasync import sync_to_async
from ..table import alter_index_operations, alter_table_operations
from ..tokens import scopes
from ..tracker import OpsLogEntry
from ..user import (
    DatasourceAlreadySharedWithWorkspace,
    DatasourceIsNotSharedWithThatWorkspace,
    DataSourceIsReadOnly,
    DataSourceNotFound,
    ResourceAlreadyExists,
    User,
    UserAccount,
    Users,
    public,
)
from ..workspace_service import WorkspaceService
from .api_errors.datasources import (
    ClientErrorBadRequest,
    ClientErrorConflict,
    ClientErrorForbidden,
    ClientErrorNotFound,
    ServerErrorInternal,
)
from .base import (
    ApiHTTPError,
    BaseHandler,
    URLMethodSpec,
    _calculate_edited_by,
    authenticated,
    check_rate_limit,
    requires_write_access,
    user_authenticated,
    with_scope,
)
from .mailgun import MailgunService

ANALYZE_SIZE = 32 * (1024**2)
MAX_BODY_SIZE_BYTES_STREAM = 10 * (1024**3)
MAX_EXECUTION_TIME_ALTER = 60
PREVIEW_ROWS = 100


REPLICATION_ALTER_PARTITIONS_ASYNC = 0
REPLICATION_ALTER_PARTITIONS_SYNC = 2
DATASOURCE_VALID_PROMOTION_SERVICES = [DataConnectors.SNOWFLAKE, DataConnectors.BIGQUERY]
VALID_SERVICES = [
    DataConnectors.KAFKA,
    DataConnectors.GCLOUD_SCHEDULER,
    DataConnectors.SNOWFLAKE,
    DataConnectors.BIGQUERY,
    DataConnectors.GCLOUD_STORAGE_HMAC,
    DataConnectors.GCLOUD_STORAGE,
    DataConnectors.AMAZON_DYNAMODB,
    DataConnectors.AMAZON_S3,
    DataConnectors.AMAZON_S3_IAMROLE,
]


def detect_format(data: bytes):
    """
    >>> detect_format(b'1')
    'csv'
    >>> detect_format(b'1,a,d')
    'csv'
    >>> detect_format(b'1,{}')
    'csv'
    >>> detect_format(b'1\\n')
    'csv'
    >>> detect_format(b'1\\n1')
    'csv'
    >>> detect_format(b'1\\n1\\n')
    'csv'
    >>> detect_format(b'1')
    'csv'
    >>> detect_format(b'')
    'csv'
    >>> detect_format(b'  ')
    'csv'
    >>> detect_format(b'1.5')
    'csv'
    >>> detect_format(b'string')
    'csv'
    >>> detect_format(b'{}')
    'ndjson'
    >>> detect_format(b'{ }')
    'ndjson'
    >>> detect_format(b'{"a"}')
    'csv'
    >>> detect_format(b"{'a'}")
    'csv'
    >>> detect_format(b"{'a': 1}")
    'csv'
    >>> detect_format(b'{"a": 1}')
    'ndjson'
    >>> detect_format(b'{"a": 1}\\n')
    'ndjson'
    >>> detect_format(b'{"a": 1}\\n{"a": 2}')
    'ndjson'
    >>> detect_format(b'{"a": 1}\\n{"a": 2}\\n')
    'ndjson'
    >>> detect_format(b'{"a": 1}\\n\\n\\n\\n{"a": 2}\\n')
    'ndjson'
    >>> detect_format(b'{"a": 1}\\n{"a": 2}\\n{"a": 2}')
    'ndjson'
    >>> detect_format(b'{\"a\": 1}')
    'ndjson'
    >>> detect_format(b'{"foo":[5,6.8],"foo":"bar"}')
    'ndjson'
    >>> detect_format(b'PAR1_whatever5goes5here')
    'parquet'
    >>> detect_format(b'aPAR1')
    'csv'
    """
    if data[:4] == b"PAR1":
        return "parquet"
    lines = split_ndjson(data)
    # an NDJSON MUST end in a new line, so this should not be a valid NDJSON
    # we are supporting it though, for the typical case of a manually generated oneliner NDJSON
    # Reference: https://github.com/ndjson/ndjson-spec#31-serialization
    if len(lines) == 1:
        return "ndjson" if is_valid_json(lines[0]) else "csv"
    if len(lines) > PREVIEW_ROWS:
        random.seed(0)
        lines = random.sample(lines, k=PREVIEW_ROWS)
    for line in lines:
        try:
            # The parser MAY silently ignore empty lines, e.g. \n\n
            # https://github.com/ndjson/ndjson-spec#32-parsing
            if not line:
                continue
            if is_valid_json(line, raise_errors=True):
                return "ndjson"
        except Exception:
            # If one row is a valid json, then detect as NDJSON, wrong rows will go to quarantine
            pass
    # If no rows were valid json, assume csv
    return "csv"


def get_shared_with_workspaces(datasource: Datasource):
    shared_with_workspaces = []
    for ws_id in datasource.shared_with:
        ws = Users.get_by_id(ws_id)
        ws_name = ws.name if ws else ws_id
        shared_with_workspaces.append({"id": ws_id, "name": ws_name})
    return shared_with_workspaces


class APIDataSourcesHandler(BaseHandler):
    @authenticated
    @check_rate_limit(Limit.api_datasources_list)
    async def get(self):
        """
        .. code-block:: bash
            :caption: getting a list of your Data Sources

            curl \\
            -H "Authorization: Bearer <DATASOURCES:READ token>" \\
            -X GET "https://api.tinybird.co/v0/datasources"

        Get a list of the Data Sources in your account.

        .. container:: hint

            The token you use to query the available Data Sources will determine what Data Sources get returned: only those accessible with the token you are using will be returned in the response.

        .. sourcecode:: json
            :caption: Successful response

            {
                "datasources": [{
                    "id": "t_a049eb516ef743d5ba3bbe5e5749433a",
                    "name": "your_datasource_name",
                    "cluster": "tinybird",
                    "tags": {},
                    "created_at": "2019-11-13 13:53:05.340975",
                    "updated_at": "2022-02-11 13:11:19.464343",
                    "replicated": true,
                    "version": 0,
                    "project": null,
                    "headers": {},
                    "shared_with": [
                        "89496c21-2bfe-4775-a6e8-97f1909c8fff"
                    ],
                    "engine": {
                        "engine": "MergeTree",
                        "engine_sorting_key": "example_column_1",
                        "engine_partition_key": "",
                        "engine_primary_key": "example_column_1"
                    },
                    "description": "",
                    "used_by": [],
                    "type": "csv",
                    "columns": [{
                            "name": "example_column_1",
                            "type": "Date",
                            "codec": null,
                            "default_value": null,
                            "jsonpath": null,
                            "nullable": false,
                            "normalized_name": "example_column_1"
                        },
                        {
                            "name": "example_column_2",
                            "type": "String",
                            "codec": null,
                            "default_value": null,
                            "jsonpath": null,
                            "nullable": false,
                            "normalized_name": "example_column_2"
                        }
                    ],
                    "statistics": {
                        "bytes": 77822,
                        "row_count": 226188
                    },
                    "new_columns_detected": {},
                    "quarantine_rows": 0
                }]
            }

        .. csv-table:: Request parameters
            :header: "Key", "Type", "Description"
            :widths: 20, 20, 60

            "attrs", "String", "comma separated list of the Data Source attributes to return in the response. Example: ``attrs=name,id,engine``. Leave empty to return a full response"

        Note that the ``statistics``'s  ``bytes`` and ``row_count`` attributes might be ``null`` depending on how the Data Source was created.
        """
        workspace = self.get_workspace_from_db()
        attrs = self.get_argument("attrs", None)
        if attrs:
            attrs = attrs.split(",")

        self.set_header("content-type", "application/json")
        datasources = Users.get_datasources(workspace)
        pipes = Users.get_pipes(workspace)
        project = self.get_argument("project", None)
        if project:
            datasources = [x for x in datasources if x["project"] == project]

        if not self.is_admin() and not self.has_scope(scopes.DATASOURCES_CREATE):
            token_resources = self._get_access_info().get_resources_for_scope(
                scopes.DATASOURCES_READ, scopes.PIPES_READ
            )
            datasources = [t for t in datasources if t.id in token_resources]
            pipes = [p for p in pipes if p.id in token_resources]

        if attrs is None or "used_by" in attrs:
            for ds in datasources:
                ds.used_by = Users.get_datasource_used_by(workspace, ds, pipes)

        connector_settings = {}
        if attrs is None or "connector" in attrs:
            connector_settings = DataConnector.get_public_settings_by_datasource(workspace.id)

        async def get_tables_meta(datasources: List[Datasource]):
            if not datasources:
                return {}

            tables_meta: Dict[str, Dict[str, Any]] = {}
            for ds in datasources:
                tables_meta[ds.id] = {"engine": None, "statistics": {"bytes": None, "row_count": None}}

            include_stats = attrs is None or "statistics" in attrs
            db_tables = get_datasources_internal_ids(datasources, default_database=workspace.database)
            all_details: Dict[str, Dict[str, TableDetails]] = {}
            if db_tables:
                try:
                    all_details = await ch_many_tables_details_async(
                        workspace.database_server, datasources=db_tables, timeout=3, include_stats=include_stats
                    )
                except Exception as e:
                    logging.exception(f"Query failed to retrieve tables information {e}")

            for db_key in all_details:
                for db_table in all_details[db_key]:
                    details: TableDetails = all_details[db_key][db_table]
                    try:
                        tables_meta[details.name] = {
                            "engine": {
                                "engine": details.engine,
                                "engine_sorting_key": details.sorting_key,
                                "engine_partition_key": details.partition_key,
                                "engine_primary_key": details.primary_key,
                            }
                        }

                        if attrs is None or "columns" in attrs:
                            # poor man's schema parsing
                            columns = []
                            try:
                                create_table_query = details.details.get("create_table_query")
                                if create_table_query:
                                    init_columns_index = create_table_query.find("(")
                                    end_columns_index = create_table_query.rfind("ENGINE")
                                    if "PROJECTION" in create_table_query:
                                        end_columns_index = create_table_query[:end_columns_index].rfind("PROJECTION")
                                        end_columns_index = create_table_query[:end_columns_index].rfind(",")
                                    else:
                                        end_columns_index = create_table_query[:end_columns_index].rfind(")")
                                    columns_as_string = create_table_query[init_columns_index + 1 : end_columns_index]
                                    columns = parse_table_structure(columns_as_string)
                            except Exception as e:
                                logging.exception(f"Unhandled exception when parsing schema columns: {str(e)}")

                            tables_meta[details.name]["columns"] = columns

                        if include_stats:
                            tables_meta[details.name]["statistics"] = {
                                "bytes": details.details.get("total_bytes"),
                                "row_count": details.details.get("total_rows"),
                            }
                        tables_meta[details.name]["indexes"] = [asdict(index) for index in details.indexes]
                    except KeyError:
                        logging.warning(f"Could not format engine/stats for {details}")

            return tables_meta

        tables_meta = {}
        if attrs is None or "statistics" in attrs or "columns" in attrs:
            tables_meta = await get_tables_meta(datasources)

        new_columns = {}
        if attrs and "new_columns_detected" in attrs:
            paths_by_status = await get_paths_by_status(datasources, workspace)
            for ds_id, status in paths_by_status.items():
                new_columns[ds_id] = bool(status["new"])

        async def get_quarantine_data(workspace: User):
            client = HTTPClient(workspace.database_server, database=workspace.database)
            quarantine_data: Dict[str, Any] = {}
            query = f"""
            SELECT name, total_rows
            FROM system.tables
            WHERE database = '{workspace.database}' AND name LIKE '%_quarantine'
            FORMAT JSON;
            """

            body = None
            try:
                _, body = await client.query(query)
                quarantine_datasources = orjson.loads(body)["data"]
            except Exception:
                logging.exception(f"Query failed to retrieve quarantine datasources: SQL={query} BODY={body!r}")
                quarantine_datasources = []

            quarantine_data = {}

            for ds in quarantine_datasources:
                quarantine_data[ds["name"]] = ds["total_rows"]
            return quarantine_data

        quarantine_data = {}
        if attrs and "quarantine_rows" in attrs:
            quarantine_data = await get_quarantine_data(workspace)

        include_workspace_names = self.get_argument("include_workspace_names", None) == "true"

        def _get_datasource_info(datasource: Datasource):
            datasource_info = Datasource.to_json(datasource, attrs=attrs)

            if include_workspace_names:
                datasource_info["shared_with_workspaces"] = get_shared_with_workspaces(datasource)

            return {
                **datasource_info,
                **connector_settings.get(datasource.id, {}),
                **tables_meta.get(datasource.id, {}),
                "new_columns_detected": new_columns.get(datasource.id, {}),
                "quarantine_rows": quarantine_data.get(f"{datasource.id}_quarantine", 0),
            }

        self.write_json({"datasources": list(map(_get_datasource_info, datasources))})


class APIDataSourceHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @authenticated
    async def get(self, ds_name):
        """
        .. code-block:: bash
            :caption: Getting information about a particular Data Source

            curl \\
            -H "Authorization: Bearer <DATASOURCES:READ token>" \\
            -X GET "https://api.tinybird.co/v0/datasources/datasource_name"

        Get Data Source information and stats. The token provided must have read access to the Data Source.

        .. sourcecode:: json
            :caption: Successful response

            {
                "id": "t_bd1c62b5e67142bd9bf9a7f113a2b6ea",
                "name": "datasource_name",
                "statistics": {
                    "bytes": 430833,
                    "row_count": 3980
                },
                "used_by": [{
                    "id": "t_efdc62b5e67142bd9bf9a7f113a34353",
                    "name": "pipe_using_datasource_name"
                }]
                "updated_at": "2018-09-07 23:50:32.322461",
                "created_at": "2018-11-28 23:50:32.322461",
                "type": "csv"
            }

        .. csv-table:: Request parameters
            :header: "Key", "Type", "Description"
            :widths: 20, 20, 60

            "attrs", "String", "comma separated list of the Data Source attributes to return in the response. Example: ``attrs=name,id,engine``. Leave empty to return a full response"

        ``id`` and ``name`` are two ways to refer to the Data Source in SQL queries and API endpoints. The only difference is that the ``id`` never changes; it will work even if you change the ``name`` (which is the name used to display the Data Source in the UI). In general you can use ``id`` or ``name`` indistinctively:

        Using the above response as an example:

        ``select count(1) from events_table``

        is equivalent to

        ``select count(1) from t_bd1c62b5e67142bd9bf9a7f113a2b6ea``

        The id ``t_bd1c62b5e67142bd9bf9a7f113a2b6ea`` is not a descriptive name so you can add a description like ``t_my_events_datasource.bd1c62b5e67142bd9bf9a7f113a2b6ea``

        The ``statistics`` property contains information about the table. Those numbers are an estimation: ``bytes`` is the estimated data size on disk and ``row_count`` the estimated number of rows. These statistics are updated whenever data is appended to the Data Source.

        The ``used_by`` property contains the list of pipes that are using this data source. Only Pipe ``id`` and ``name`` are sent.

        The ``type`` property indicates the ``format`` used when the Data Source was created. Available formats are ``csv``, ``ndjson``, and ``parquet``. The Data Source ``type`` indicates what file format you can use to ingest data.

        """
        workspace = self.get_workspace_from_db()
        cli_version = self._get_cli_version()

        if not ds_name:
            return

        datafile = ds_name.endswith(".datasource")
        if datafile:
            ds_name = ds_name.rsplit(".", 1)[0]
        ds_meta = workspace.get_datasource(ds_name, include_read_only=True)

        if not ds_meta:
            raise ApiHTTPError.from_request_error(ClientErrorNotFound.nonexisting_data_source(name=ds_name))

        if (
            not self.is_admin()
            and not self.has_scope(scopes.DATASOURCES_CREATE)
            and ds_meta.id not in self._get_access_info().get_resources_for_scope(scopes.DATASOURCES_READ)
        ):
            raise ApiHTTPError.from_request_error(ClientErrorForbidden.token_doesnt_have_access_to_this_resource())

        if datafile:
            try:
                is_cli_with_tags_enabled = cli_version is None or cli_version > version.parse("5.7.0")
                self.set_header("content-type", "text/plain")
                datafile = await generate_datasource_datafile(
                    workspace, ds_meta, self._get_access_info(), tags_cli_support_enabled=is_cli_with_tags_enabled
                )
                self.write(datafile)
            except ValueError as e:
                error = str(e)
                logging.exception(error)
                raise ApiHTTPError(404, error)
            except Exception as e:
                logging.exception(e)
                raise ApiHTTPError.from_request_error(ServerErrorInternal.failed_datafile(error=e))
            return

        attr_query_param: str = self.get_argument("attrs", "used_by")  # type: ignore
        attrs: List[str] = attr_query_param.split(",")

        if "used_by" in attrs:
            if not self.is_admin() and not self.has_scope(scopes.DATASOURCES_CREATE):
                token_resources = self._get_access_info().get_resources_for_scope(
                    scopes.DATASOURCES_READ, scopes.PIPES_READ
                )
                pipes = [p for p in workspace.get_pipes() if p.id in token_resources]
                ds_meta.used_by = workspace.get_datasource_used_by(ds_meta, pipes)
            else:
                ds_meta.used_by = workspace.get_datasource_used_by(ds_meta)

        self.set_header("content-type", "application/json")
        include_workspace_names = self.get_argument("include_workspace_names", None) == "true"
        ds_response = ds_meta.to_json()

        if include_workspace_names:
            ds_response["shared_with_workspaces"] = get_shared_with_workspaces(ds_meta)

        pu = public.get_public_user()
        ds_response["updated_at"] = await ds_meta.last_update(pu, workspace)

        try:
            table_details, schema = await ds_meta.table_metadata(
                workspace,
                include_default_columns=True,
                include_jsonpaths=True,
                include_stats=True,
                include_indices=True,
            )
            if not ds_meta.json_deserialization and ds_response["type"] == "kafka":
                analysis = await analyze_datasource(workspace, ds_meta)
                for column in schema:
                    for analyzed_column in analysis:
                        if column["name"] == analyzed_column["name"]:
                            column["jsonpath"] = analyzed_column["path"]
                            break
            ds_response["engine"] = table_details.to_json()
            ds_response["statistics"] = table_details.statistics
            indexes = table_details.indexes
            ds_response["indexes"] = [asdict(index) for index in table_details.indexes] if indexes else []
            ds_response["schema"] = {"columns": schema, "sql_schema": table_structure(schema)}
        except Exception as e:
            logging.exception(f"Failed to retrieve engine information: {e}")
            ds_response["engine"] = {"error": "Failed to retrieve engine information"}
            ds_response["schema"] = {"error": "Failed to retrieve schema information"}

        debug = self.get_argument("debug", "").split(",")

        if debug:
            client = HTTPClient(workspace["database_server"], database=workspace["database"])

            if "columns" in debug:
                columns_query = f"""
                    WITH (SELECT compression FROM (
                        SELECT
                            default_compression_codec compression,
                            count() c
                        FROM system.parts
                        WHERE
                            database = '{workspace['database']}'
                            and table = '{ds_meta.id}'
                        GROUP BY 1 ORDER BY c DESC
                        LIMIT 1
                    )) AS default_compression_codec
                    SELECT
                        name,
                        type,
                        default_kind,
                        default_expression,
                        compression_codec = '' ? concat(default_compression_codec, ' (Default)') : compression_codec as compression_codec,
                        data_compressed_bytes,
                        data_uncompressed_bytes,
                        data_uncompressed_bytes/data_compressed_bytes as data_compression_ratio,
                        marks_bytes,
                        is_in_partition_key,
                        is_in_sorting_key,
                        is_in_primary_key,
                        is_in_sampling_key
                    FROM
                        system.columns
                    WHERE
                        database = '{workspace['database']}'
                        and table = '{ds_meta.id}'
                FORMAT JSON
                """
                _, body = await client.query(columns_query, read_only=True)
                result = orjson.loads(body)
                ds_response.update({"columns": result.get("data", [])})

            if "parts" in debug:
                parts_query = f"""
                    SELECT
                        partition,
                        count() as parts_count,
                        sum(rows) as rows,
                        sum(bytes_on_disk) as bytes_on_disk,
                        sum(data_compressed_bytes) as data_compressed_bytes,
                        sum(data_uncompressed_bytes) as data_uncompressed_bytes,
                        data_uncompressed_bytes/data_compressed_bytes as compression_ratio,
                        avg(level) as avg_level
                    FROM
                        system.parts
                    WHERE
                        active
                        and database = '{workspace['database']}'
                        and table = '{ds_meta.id}'
                    GROUP BY
                        partition
                    WITH TOTALS
                    ORDER BY
                        parts_count desc
                    FORMAT JSON
                """
                _, body = await client.query(parts_query, read_only=True)
                result = orjson.loads(body)
                ds_response.update({"parts": result.get("data", [])})

        paths_by_status = await get_paths_by_status([ds_meta], workspace)
        ds_response["new_columns_detected"] = bool(paths_by_status[ds_meta.id]["new"])

        self.write_json(ds_response)

    @staticmethod
    async def rename_shared_data_sources_on_data_source_name_change(
        datasource: Datasource,
        origin_workspace: "User",
        user_email_making_the_request: Optional[str],
        dependencies: Optional[List[str]] = None,
    ) -> None:
        for shared_with_ws_id in datasource.shared_with:
            try:
                await Users.alter_shared_datasource_name(
                    shared_with_ws_id,
                    datasource.id,
                    origin_workspace.id,
                    origin_workspace.name,
                    datasource.name,
                    user_email_making_the_request,
                    dependencies=dependencies,
                )
            except Exception as e:
                logging.exception(f"Couldn't update shared Data Source name on origin Data Source name change: {e}")
                raise e

    @authenticated
    @requires_write_access
    @with_scope(scopes.DATASOURCES_CREATE)
    async def put(self, ds_name: str) -> None:
        """
        Update Data Source attributes

        .. sourcecode:: bash
            :caption: Updating the name of a Data Source

            curl \\
            -H "Authorization: Bearer <DATASOURCES:CREATE token>" \\
            -X PUT "https://api.tinybird.co/v0/datasources/:name?name=new_name"

        .. sourcecode:: bash
            :caption: Promoting a Data Source to a Snowflake one

            curl \\
                -H "Authorization: Bearer <DATASOURCES:CREATE token>" \\
                -X PUT "https://api.tinybird.co/v0/datasources/:name" \\
                -d "connector=1d8232bf-2254-4d68-beff-4dd9aa505ab0" \\
                -d "service=snowflake" \\
                -d "cron=*/30 * * * *" \\
                -d "query=select a, b, c from test" \\
                -d "mode=replace" \\
                -d "external_data_source=database.schema.table" \\
                -d "ingest_now=True" \\

        .. csv-table:: Request parameters
            :header: "Key", "Type", "Description"
            :widths: 20, 20, 60

            "name", "String", "new name for the Data Source"
            "token", "String", "Auth token. Only required if no Bearer Authorization header is sent. It should have ``DATASOURCES:CREATE`` scope for the given Data Source"
            "connector", "String", "Connector ID to link it to"
            "service", "String", "Type of service to promote it to. Only 'snowflake' or 'bigquery' allowed"
            "cron", "String", "Cron-like pattern to execute the connector's job"
            "query", "String", "Optional: custom query to collect from the external data source"
            "mode", "String", "Only replace is allowed for connectors"
            "external_data_source", "String", "External data source to use for Snowflake"
            "ingest_now", "Boolean", "To ingest the data immediately instead of waiting for the first execution determined by cron"
        """
        """
        TODO Add to docs when the Shared Data Sources feature gets publicly released:

        .. container:: hint

            Caution: if this Workspace owns shared Data Sources, the name of these Data Sources will also be renamed at
            the destination Workspaces. This will break the pipes and queries using it.

        """
        workspace = self.get_workspace_from_db()
        user_making_the_request_email = None
        workspace_admin_users = self.get_resources_for_scope(scopes.ADMIN_USER)
        if workspace_admin_users:
            try:
                user_account = UserAccount.get_by_id(workspace_admin_users[0])
                if not user_account:
                    logging.exception(f"Unexpected error: User {workspace_admin_users[0]} not found")
                else:
                    user_making_the_request_email = user_account.email
            except Exception:
                pass

        ds = workspace.get_datasource(ds_name, include_used_by=True)

        if not ds:
            raise ApiHTTPError.from_request_error(ClientErrorNotFound.nonexisting_data_source(name=ds_name))

        datasource = ds

        new_name = self.get_argument("name", None, True)
        edited_by = _calculate_edited_by(self._get_access_info())
        if new_name is not None:
            # if the name does not change just return the table
            if new_name == ds.name:
                self.write_json(ds.to_json())
                return

            error = None
            try:
                dependencies = workspace.get_dependencies(recursive=False, pipe=None, datasource_name=ds.name)
                ds_dependencies = dependencies.get(ds.name, None)
                datasource = await Users.alter_datasource_name(
                    workspace, ds.name, new_name, edited_by, dependencies=ds_dependencies
                )

                token = self._get_token()

                if token is None:
                    raise ConnectorException(message="Token not found")

            except ConnectorException as e:
                error = str(e)
                raise ApiHTTPError(400, error)
            except ResourceAlreadyExists as e:
                error = str(e)
                raise ApiHTTPError(409, error)
            except ValueError as e:
                error = str(e)
                raise ApiHTTPError(400, error)
            finally:
                ops_log_entry = OpsLogEntry(  # FIXME change ops log entry
                    start_time=datetime.now(timezone.utc),
                    event_type="rename",
                    datasource_id=ds.id,
                    datasource_name=ds.name if error else new_name,
                    workspace_id=workspace.id,
                    workspace_email=workspace.name,  # FIXME user name? or better identify both the workspace and the user?
                    result="error" if error else "ok",
                    elapsed_time=0,
                    error=error,
                    rows=0,
                    rows_quarantine=0,
                    options={"old_name": ds.name, "new_name": new_name},
                )
                tracker.track_datasource_ops([ops_log_entry], request_id=self._request_id, workspace=workspace)

            await self.rename_shared_data_sources_on_data_source_name_change(
                datasource, workspace, user_making_the_request_email, dependencies=ds_dependencies
            )

        # FIXME: we should have an easy way to update TAGS
        tag = self.get_argument("backfill_column", None)
        if datasource.tags.get("backfill_column") != tag:
            try:
                datasource.tags["backfill_column"] = tag
                if not Users.update_datasource(workspace, datasource):
                    raise ApiHTTPError(422, "Cannot update Data Source tags")
            except Exception as e:
                logging.exception(e)
                raise ApiHTTPError(422, "Cannot update Data Source tags") from e

        service = self.get_argument("service", None)

        # We want to promote the Data Source to a connector's one
        # TODO: add s3 to the list of valid promotion services and implement the modification
        # TODO: add GCS SA to the list of valid promotion services and implement the modification
        if service is None:
            pass
        elif service not in VALID_SERVICES:
            raise ApiHTTPError.from_request_error(
                ClientErrorBadRequest.invalid_parameter(parameter="service", value=service, valid=VALID_SERVICES)
            )
        elif service in DATASOURCE_VALID_PROMOTION_SERVICES:
            service = service.lower()
            if ds.service is not None and service != ds.service:
                raise ApiHTTPError.from_request_error(DataConnectorsClientErrorBadRequest.data_linker_other_type())

            data_connector = None
            if service not in [DataConnectors.BIGQUERY]:
                connector_id = self.get_argument("connector", None)
                if connector_id is None:
                    raise ApiHTTPError.from_request_error(
                        ClientErrorBadRequest.missing_parameter(parameter="connector")
                    )
                data_connector = DataConnector.get_by_id(connector_id)
                if data_connector is None:
                    raise ApiHTTPError.from_request_error(
                        ClientErrorBadRequest.invalid_connector(connector=connector_id)
                    )

            _, datasource_schema = await ds.table_metadata(workspace)
            columns = schema_to_sql_columns(datasource_schema)
            schema = ", ".join(columns)

            ds_service_conf, conn_params = await prepare_connector_service(
                self, workspace, service, data_connector, schema
            )

            token = await add_cdk_data_linker(ds, data_connector, conn_params, service, workspace)

            try:
                _ = await get_or_create_workspace_service_account(workspace)
            except googleapiclient.errors.HttpError as e:
                raise ApiHTTPError(e.status_code, e.reason) from e

            # Update the workspace after adding (if necessary) the CDK key
            workspace = Users.get_by_id(workspace.id)
            await update_dag(service, workspace, ds, token, ds_service_conf)  # type: ignore

            with User.transaction(workspace.id) as workspace:
                datasource = cast(Datasource, workspace.get_datasource(ds.id))
                datasource.service = service
                if service in [DataConnectors.BIGQUERY]:
                    datasource.service_conf = ds_service_conf
                workspace.update_datasource(datasource)

        self.write_json(datasource.to_json())

    @authenticated
    @requires_write_access
    async def delete(self, ds_name: str) -> None:
        """
        .. code-block:: bash
            :caption: Dropping a Data Source

            curl \\
            -H "Authorization: Bearer <DATASOURCES:DROP token>" \\
            -X DELETE "https://api.tinybird.co/v0/datasources/:name"

        Drops a Data Source from your account.

        .. csv-table:: Request parameters
            :header: "Key", "Type", "Description"
            :widths: 20, 20, 60

            "force", "String", "Default: ``false`` . The ``force`` parameter is taken into account when trying to delete Materialized Views. By default, when using ``false`` the deletion will not be carried out; you can enable it by setting it to ``true``. If the given Data Source is being used as the trigger of a Materialized Node, it will not be deleted in any case."
            "dry_run", "String", "Default: ``false``. It allows you to test the deletion. When using ``true`` it will execute all deletion validations and return the possible affected materializations and other dependencies of a given Data Source."
            "token", "String", "Auth token. Only required if no Bearer Authorization header is sent. It must have ``DROP:datasource_name`` scope for the given Data Source."
        """
        workspace = self.get_workspace_from_db()
        force = self.get_argument("force", "false") == "true"
        dry_run = self.get_argument("dry_run", "false") == "true"
        is_from_cli = bool(self.get_argument("cli_version", None))
        is_from_ui = self.get_argument("from", None) == "ui"
        is_api = not is_from_cli and not is_from_ui

        ds = workspace.get_datasource(ds_name, include_used_by=True, include_read_only=True)
        if not ds:
            raise ApiHTTPError.from_request_error(ClientErrorNotFound.nonexisting_data_source(name=ds_name))

        workspace_admin_users = self.get_resources_for_scope(scopes.ADMIN_USER)
        user_account: Optional[UserAccount] = None
        dependencies_response = None

        if (
            not self.is_admin()
            and not self.has_scope(scopes.DATASOURCES_CREATE)
            and ds.id not in self.get_dropable_resources()
        ):
            raise ApiHTTPError.from_request_error(
                ClientErrorForbidden.invalid_data_source_permission_drop(name=ds_name)
            )

        if workspace_admin_users:
            try:
                user_account = UserAccount.get_by_id(workspace_admin_users[0])
                if not user_account:
                    raise ApiHTTPError(404, f"User {workspace_admin_users[0]} not found")
                assert isinstance(user_account, UserAccount)
            except Exception:
                pass

        if isinstance(ds, SharedDatasource):
            raise ApiHTTPError.from_request_error(
                ClientErrorBadRequest.can_not_delete_data_source_as_it_is_a_shared_ds_in_a_destination_ws(name=ds_name)
            )

        try:
            """
            DS2 is downstream from DS1.
            DS1 is upstream from DS2.

            DS2 can be deleted when using force.
            DS1 cannot be deleted, since it would break ingestion in DS2.

            +------+  insert/replace   +---------+  MV1to2   +-----+
            | user | ----------------> |   DS1   | --------> | DS2 |
            +------+                   +---------+           +-----+
            """
            dependencies = Users.check_used_by_pipes(workspace, ds.id, force=force, is_api=is_api, is_cli=is_from_cli)

            if dry_run:
                dep_pipe_names, dep_node_names = parse_dependencies(dependencies, workspace.name)
                response = {
                    "dependencies": dependencies,
                    "dependent_pipes": dep_pipe_names,
                    "dependent_nodes": dep_node_names,
                }
                self.write_json(response)
                self.set_status(200)
                return

        except DependentMaterializedNodeException as dependent_exception:
            branch_mode = BranchMode(
                self.get_api_option("branch_mode", BRANCH_MODES, default_option=BranchMode.NONE.value)
            )
            if not allow_force_delete_materialized_views(workspace, branch_mode=branch_mode):
                if dry_run and force:
                    dependencies_response = dependent_exception.all_dependencies
                elif not force or (force and dependent_exception.has_downstream_dependencies):
                    raise ApiHTTPError.from_request_error(
                        ClientErrorConflict.conflict_materialized_node(
                            break_ingestion_message=dependent_exception.break_ingestion_message,
                            affected_materializations_message=dependent_exception.affected_materializations_message,
                            dependent_pipes_message=dependent_exception.dependent_pipes_message,
                        )
                    )
            else:
                if not force:
                    dependencies_response = dependent_exception.all_dependencies

        except DependentCopyPipeException as dependent_exception:
            branch_mode = BranchMode(
                self.get_api_option("branch_mode", BRANCH_MODES, default_option=BranchMode.NONE.value)
            )
            if not allow_force_delete_materialized_views(workspace, branch_mode=branch_mode):
                if dry_run and force:
                    dependencies_response = dependent_exception.all_dependencies
                elif not force:
                    raise ApiHTTPError.from_request_error(
                        ClientErrorConflict.conflict_copy_pipes(
                            break_copy_message=dependent_exception.break_copy_message,
                            dependent_pipes_message=dependent_exception.dependent_pipes_message,
                        )
                    )
            else:
                if not force:
                    dependencies_response = dependent_exception.all_dependencies

        if dependencies_response:
            self.write_json(dependencies_response)
            self.set_status(200)
            return

        b_mode = self.get_api_option("branch_mode", BRANCH_MODES, default_option=BranchMode.NONE.value)
        assert isinstance(b_mode, str)
        edited_by = _calculate_edited_by(self._get_access_info())
        try:
            ds_deleted = await DatasourceService.drop_datasource(
                workspace=workspace,
                ds=ds,
                force=force,
                branch_mode=b_mode,
                request_id=self._request_id,
                job_executor=self.application.job_executor,
                user_account=user_account,
                edited_by=edited_by,
            )
            if ds_deleted:
                self.set_status(204)
        except RequestErrorException as ex:
            req_err = ex.request_error
            logging.exception(f"Failed to delete datasource {ds_name}: {str(ex)}")
            raise ApiHTTPError.from_request_error(req_err)
        except (ApiHTTPError, Exception):
            raise


@dataclass
class AlterQuery:
    query: str
    alter_sync: int = REPLICATION_ALTER_PARTITIONS_SYNC
    max_execution_time: int = MAX_EXECUTION_TIME_ALTER
    distributed_ddl_task_timeout: int = MAX_EXECUTION_TIME_ALTER - 2
    distributed_ddl_output_mode: str = "none"


class APIDataSourceAlterHandler(BaseHandler):
    @authenticated
    @requires_write_access
    @with_scope(scopes.DATASOURCES_CREATE)
    async def post(self, ds_name: str) -> None:
        """
        Modify the Data Source schema.

        This endpoint supports the operation to alter the following fields of a Data Source:

        .. csv-table:: Request parameters
            :header: "Key", "Type", "Description"
            :widths: 20, 20, 60

            "schema", "String", "Optional. Set the whole schema that adds new columns to the existing ones of a Data Source."
            "description", "String", "Optional. Sets the description of the Data Source."
            "kafka_store_raw_value", "Boolean", "Optional. Default: false. When set to true, the 'value' column of a Kafka Data Source will save the JSON as a raw string."
            "kafka_store_headers", "Boolean", "Optional. Default: false. When set to true, the 'headers' of a Kafka Data Source will be saved as a binary map."
            "ttl", "String", "Optional. Set to any value accepted in ClickHouse for a TTL or to 'false'  to remove the TTL."
            "dry", "Boolean", "Optional. Default: false. Set to true to show what would be modified in the Data Source, without running any modification at all."

        The schema parameter can be used to add new columns at the end of the existing ones in a Data Source.

        Be aware that currently we don't validate if the change will affect the existing MVs (Materialized Views) attached to the Data Source to be modified, so this change may break existing MVs.
        For example, avoid changing a Data Source that has a MV created with something like ``SELECT * FROM Data Source ...``. If you want to have forward compatible MVs with column additions, create them especifying the columns instead of using the ``*`` operator.

        Also, take in account that, for now, the only engines supporting adding new columns are those inside the MergeTree family.

        To add a column to a Data Source, call this endpoint with the Data Source name and the new schema definition.

        For example, having a Data Source created like this:

        .. code-block:: bash
            :caption: Creating a Data Source from a schema

            curl \\
            -H "Authorization: Bearer <DATASOURCES:CREATE token>" \\
            -X POST "https://api.tinybird.co/v0/datasources" \\
            -d "name=stocks" \\
            -d "schema=symbol String, date Date, close Float32"

        if you want to add a new column 'concept String', you need to call this endpoint with the new schema:

        .. code-block:: bash
            :caption: Adding a new column to an existing Data Source

            curl \\
            -H "Authorization: Bearer <DATASOURCES:CREATE token>" \\
            -X POST "https://api.tinybird.co/v0/datasources/stocks/alter" \\
            -d "schema=symbol String, date Date, close Float32, concept String"

        If everything went ok, you will get the operations done in the response:

        .. code-block:: json
            :caption: ADD COLUMN operation resulted from the schema change.

            {
                "operations": [
                    "ADD COLUMN `concept` String"
                ]
            }

        You can also view the inferred operations without executing them adding ``dry=true`` in the parameters.

        - To modify the description of a Data Source:

        .. code-block:: bash
            :caption: Modifying the description a Data Source

            curl \\
            -H "Authorization: Bearer <DATASOURCES:CREATE token>" \\
            -X POST "https://api.tinybird.co/v0/datasources/stocks/alter" \\
            -d "name=stocks" \\
            -d "description=My new description"

        - To save in the "value" column of a Kafka Data Source the JSON as a raw string:

        .. code-block:: bash
            :caption: Saving the raw string in the value column of a Kafka Data Source

            curl \\
            -H "Authorization: Bearer <DATASOURCES:CREATE token>" \\
            -X POST "https://api.tinybird.co/v0/datasources/stocks/alter" \\
            -d "name=stocks" \\
            -d "kafka_store_raw_value=true"
            -d "kafka_store_headers=true"

        - To modify the TTL of a Data Source:

        .. code-block:: bash
            :caption: Modifying the TTL of a Data Source

            curl \\
            -H "Authorization: Bearer <DATASOURCES:CREATE token>" \\
            -X POST "https://api.tinybird.co/v0/datasources/stocks/alter" \\
            -d "name=stocks" \\
            -d "ttl=12 hours"

        - To remove the TTL of a Data Source:

        .. code-block:: bash
            :caption: Modifying the TTL of a Data Source

            curl \\
            -H "Authorization: Bearer <DATASOURCES:CREATE token>" \\
            -X POST "https://api.tinybird.co/v0/datasources" \\
            -d "name=stocks" \\
            -d "ttl=false"

        - To add default values to the columns of a Data Source:

        .. code-block:: bash
            :caption: Modifying default values

            curl \\
            -H "Authorization: Bearer <DATASOURCES:CREATE token>" \\
            -X POST "https://api.tinybird.co/v0/datasources" \\
            -d "name=stocks" \\
            -d "schema=symbol String DEFAULT '-', date Date DEFAULT now(), close Float32 DEFAULT 1.1"

        - To add default values to the columns of a NDJSON Data Source, add the default definition after the jsonpath definition:

        .. code-block:: bash
            :caption: Modifying default values in a NDJSON Data Source

            curl \\
            -H "Authorization: Bearer <DATASOURCES:CREATE token>" \\
            -X POST "https://api.tinybird.co/v0/datasources" \\
            -d "name=stocks" \\
            -d "schema=symbol String `json:$.symbol` DEFAULT '-', date Date `json:$.date` DEFAULT now(), close `json:$.close` Float32 DEFAULT 1.1"

        - To make a column nullable, change the type of the column adding the Nullable type prefix to old one:

        .. code-block:: bash
            :caption: Converting column "close" to Nullable

            curl \\
            -H "Authorization: Bearer <DATASOURCES:CREATE token>" \\
            -X POST "https://api.tinybird.co/v0/datasources" \\
            -d "name=stocks" \\
            -d "schema=symbol String `json:$.symbol, date Date `json:$.date`, close `json:$.close` Nullable(Float32)"

        - To drop a column, just remove the column from the schema definition. It will not be possible removing columns that are part of the primary or partition key:

        .. code-block:: bash
            :caption: Remove column "close" from the Data Source

            curl \\
            -H "Authorization: Bearer <DATASOURCES:CREATE token>" \\
            -X POST "https://api.tinybird.co/v0/datasources" \\
            -d "name=stocks" \\
            -d "schema=symbol String `json:$.symbol, date Date `json:$.date`"

        .. container:: hint

            You can also alter the JSONPaths of existing Data Sources. In that case you have to specify the `JSONPath <jsonpaths url_>`_ in the schema in the same way as when you created the Data Source.
        """
        workspace = self.get_workspace_from_db()
        ds = workspace.get_datasource(ds_name)
        if not ds:
            raise ApiHTTPError.from_request_error(ClientErrorNotFound.nonexisting_data_source(name=ds_name))

        # FIXME 8162-index include indexes
        engine, schema = await ds.table_metadata(workspace, include_default_columns=True, include_indices=True)
        has_internal_columns = len([c for c in schema if c.get("auto")]) > 0

        cli_version = self._get_cli_version()
        is_old_cli = cli_version and cli_version < version.parse("5.0.0")
        include_auto = not is_old_cli
        current_schema = table_structure(schema, include_auto=include_auto)
        new_schema = None
        new_indices = None
        new_jsonpaths = None
        json_conf = []
        if self.get_argument("schema", None, True) is not None:
            augmented_schema = self.get_argument("schema", None, True)
            try:
                remove_columns = None
                if ds.service is not None and ds.service == DataConnectors.KAFKA:
                    remove_columns = KAFKA_META_COLUMNS
                if ds.service is not None and ds.service == DataConnectors.AMAZON_DYNAMODB:
                    remove_columns = DYNAMODB_META_COLUMNS
                parsed_schema = parse_augmented_schema(augmented_schema, remove_columns=remove_columns)
            except Exception as err:
                raise ApiHTTPError(400, str(err))
            new_schema = parsed_schema.schema
            new_jsonpaths = parsed_schema.jsonpaths

        indexes = self.get_argument("indexes", None)
        if indexes is not None:
            try:
                new_indices = parse_indexes_structure(indexes.splitlines() if indexes != "0" else [])
            except Exception as err:
                raise ApiHTTPError(400, str(err))

        data_linker: Optional[DataLinker] = None
        try:
            data_linker = ds.get_data_linker()
        except DataSourceNotConnected:
            pass

        dry_execution = self.get_argument("dry", "false").lower() == "true"

        description = self.get_argument("description", None)
        if not dry_execution and description is not None:
            await Users.alter_datasource_description(workspace, ds.id, description)

        should_discard_errors = self.get_argument("errors_discarded_at", None) == "true"
        if not dry_execution and should_discard_errors:
            await Users.discard_datasource_errors(workspace, ds.id)

        kafka_store_raw_value = self.get_argument("kafka_store_raw_value", None)
        kafka_store_headers = self.get_argument("kafka_store_headers", None)
        kafka_operations = []
        is_kafka_ds = (data_linker and data_linker.service == DataConnectors.KAFKA) or (
            ds.service == DataConnectors.KAFKA
        )

        def to_bool(raw_value, argname):
            if raw_value is None:
                return None

            try:
                return bool(util.strtobool(raw_value))
            except Exception:
                err = ClientErrorBadRequest.invalid_value_for_argument(
                    argument=argname, value=raw_value, valid="'true', 'false'"
                )
                raise ApiHTTPError.from_request_error(err)

        if kafka_store_raw_value or kafka_store_headers:
            kafka_store_raw_value = to_bool(kafka_store_raw_value, "kafka_store_raw_value")
            kafka_store_headers = to_bool(kafka_store_headers, "kafka_store_headers")

            # check DS is of type kafka
            if not data_linker:
                if kafka_store_raw_value:
                    raise ApiHTTPError.from_request_error(
                        ClientErrorBadRequest.invalid_argument_for_non_kafka(argument="kafka_store_raw_value")
                    )
                else:
                    raise ApiHTTPError.from_request_error(
                        ClientErrorBadRequest.invalid_argument_for_non_kafka(argument="kafka_store_headers")
                    )

            # store on DS / Redis
            with DataLinker.transaction(data_linker.id) as linker:
                if kafka_store_raw_value:
                    linker.update_settings({"kafka_store_raw_value": kafka_store_raw_value})
                if kafka_store_headers:
                    linker.update_settings({"kafka_store_headers": kafka_store_headers})

            await DataLinker.publish(data_linker.id)

            # record operations for response
            if kafka_store_raw_value:
                kafka_operations.append(f"kafka_store_raw_value: {kafka_store_raw_value}")
            if kafka_store_headers:
                kafka_operations.append(f"kafka_store_headers: {kafka_store_headers}")

        new_ttl = self.get_argument("ttl", None, True)
        if (
            not new_schema
            and kafka_store_raw_value is None
            and kafka_store_headers is None
            and description is None
            and not new_ttl
            and new_indices is None
            and should_discard_errors is False
        ):
            raise ApiHTTPError.from_request_error(
                ClientErrorBadRequest.alter_no_parameters(
                    parameters="'new_schema', 'kafka_store_raw_value', 'kafka_store_headers', 'description', 'ttl', 'indexes', 'errors_discarded_at'"
                )
            )

        is_ttl_changes = engine.diff_ttl(new_ttl)

        def get_indices_changes(
            new_indices: List[TableIndex], existing_indices: Optional[List[TableIndex]] = None
        ) -> Dict[str, List[TableIndex]]:
            if not existing_indices:
                existing_indices = []
            result: Dict[str, List[TableIndex]] = {"add": [], "delete": [], "modify": []}

            dict1 = {index.name: index for index in new_indices}
            dict2 = {index.name: index for index in existing_indices}

            for name, index1 in dict1.items():
                index2 = dict2.get(name)
                if index2 is None:
                    result["add"].append(index1)
                elif index1 != index2:
                    result["modify"].append(index1)

            for name, index2 in dict2.items():
                if name not in dict1:
                    result["delete"].append(index2)

            return result

        existing_indices: List[TableIndex] = engine.indexes
        is_indices_changes = False
        if new_indices is not None:
            indices_changes = get_indices_changes(new_indices, existing_indices)
            is_indices_changes = not all(not indexes for indexes in indices_changes.values())

        if not new_schema and not is_ttl_changes and not is_indices_changes:
            self.write_json({"operations": kafka_operations})
            return
        if is_kafka_ds and new_schema:
            if "`__headers` " in current_schema:
                kafka_store_headers = True

            kafka_metadata_prefix = True
            if data_linker:
                kafka_metadata_prefix = data_linker.all_settings.get("metadata_with_prefix", None)
            else:
                # ds.service == 'kafka' & not DataLinker happens in branches. Once we have the data_linker also
                # defined in a branch we should use that instead of continue using this else.
                kafka_metadata_prefix = "`__value` String" in current_schema
            schema = DataConnectorSchema.get_schema(
                "kafka",
                kafka_metadata_prefix=kafka_metadata_prefix,
                kafka_store_headers=kafka_store_headers,
            )
            new_schema = f"{schema}, {new_schema}"

        if ds.service == DataConnectors.AMAZON_DYNAMODB:
            schema = DataConnectorSchema.get_schema("dynamodb")
            jsonpaths = DataConnectorSchema.get_jsonpaths("dynamodb")
            new_schema = f"{schema}, {new_schema}"
            new_jsonpaths = f"{jsonpaths}, {new_jsonpaths}"

        if new_schema:
            new_columns = parse_table_structure(new_schema)
            new_schema_transformed = table_structure(new_columns)

            if not engine.supports_alter_add_column():
                raise ApiHTTPError.from_request_error(
                    ClientErrorBadRequest.alter_engine_not_supported(engine=engine.engine)
                )

            try:
                table_operations, table_operations_quarantine = await alter_table_operations(
                    workspace,
                    current_schema,
                    new_schema_transformed,
                    has_internal_columns,
                    new_jsonpaths,
                    engine,
                )
            except ValueError as e:
                raise ApiHTTPError.from_request_error(ClientErrorBadRequest.alter_not_supported(reason=str(e)))
            # Check jsonpaths are valid and generate json_conf
            try:
                if new_jsonpaths or ds.json_deserialization:
                    if is_kafka_ds:
                        kafka_meta_columns = KAFKA_META_COLUMNS.copy()
                        if not kafka_store_headers:
                            kafka_meta_columns.remove("__headers")
                        json_conf = json_deserialize_merge_schema_jsonpaths(
                            new_columns[len(kafka_meta_columns) :], new_jsonpaths
                        )
                    else:
                        json_conf = json_deserialize_merge_schema_jsonpaths(new_columns, new_jsonpaths)
                    # Generating the "extended" config will validate types
                    extend_json_deserialization(json_conf)
                    if ds.service == DataConnectors.AMAZON_DYNAMODB:
                        json_conf = add_item_prefix_to_jsonpath(json_conf)
            except SchemaJsonpathMismatch:
                raise ApiHTTPError.from_request_error(
                    ClientErrorBadRequest.alter_not_supported(
                        reason=f"Schema must have jsonpaths: schema={self.get_argument('schema')}"
                    )
                )
            except InvalidJSONPath as e:
                raise ApiHTTPError.from_request_error(
                    ClientErrorBadRequest.alter_not_supported(
                        reason=f"Schema has invalid jsonpaths. {e}. schema={self.get_argument('schema')}"
                    )
                )
            except UnsupportedType as e:
                raise ApiHTTPError.from_request_error(ClientErrorBadRequest.alter_not_supported(reason=f"{e}"))
        else:
            table_operations = []

        count_mutation_ops = len([op for op in table_operations if op.create_mutation])

        # Check max operations. Only allow one mutation (several ADD columns are allowed to preserve previous api behavior)
        if count_mutation_ops > 0 and len(table_operations) > 1:
            raise ApiHTTPError.from_request_error(
                ClientErrorBadRequest.max_alter_operations(number_operations=len(table_operations))
            )

        dependencies_clean = []
        if count_mutation_ops > 0:
            # get dependent pipes
            dependencies = Users.get_datasource_dependencies(workspace, ds.id)
            dependent_pipes = dependencies.get("pipes")
            if dependent_pipes is not None and any(dependent_pipes):
                dependencies_clean = [pipe["name"] for pipe in dependent_pipes]

        table_operations_clean = [re.sub(r"( AFTER| FIRST)(.*)$", "", op.sql) for op in table_operations]

        index_operations: List[str] = []
        if is_indices_changes:
            try:
                index_operations = await alter_index_operations(indices_changes)
            except ValueError as e:
                raise ApiHTTPError.from_request_error(ClientErrorBadRequest.alter_not_supported(reason=str(e)))

        # Compares the exising jsonschema (if any) with the new one (if any)
        is_jsonpath_different = json_conf != ds.json_deserialization
        if (
            not table_operations
            and not is_jsonpath_different
            and not kafka_operations
            and new_ttl is None
            and description is None
            and not index_operations
        ):
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.alter_no_operations())

        engine_operations = []
        if is_ttl_changes:
            if new_ttl is not None and new_ttl.lower() == "false" and engine.ttl is not None:
                engine_operations = ["REMOVE TTL"]
            elif new_ttl is not None and new_ttl.lower() != "false":
                engine_operations = [f"MODIFY TTL {new_ttl}"]

        if (table_operations or engine_operations or is_jsonpath_different or index_operations) and not dry_execution:

            def build_query(sql: str) -> AlterQuery:
                return AlterQuery(sql)

            # sets replication_alter_partitions to 0
            def build_async_query(sql: str) -> AlterQuery:
                return AlterQuery(
                    sql,
                    alter_sync=REPLICATION_ALTER_PARTITIONS_ASYNC,
                    max_execution_time=MAX_EXECUTION_TIME_ALTER,
                )

            def build_async_query_ddl(sql: str) -> AlterQuery:
                return AlterQuery(
                    sql,
                    alter_sync=REPLICATION_ALTER_PARTITIONS_ASYNC,
                    max_execution_time=MAX_EXECUTION_TIME_ALTER,
                    distributed_ddl_task_timeout=MAX_EXECUTION_TIME_ALTER - 2,
                    distributed_ddl_output_mode=DDL_OUTPUT_MODE_NULL_STATUS_ON_TIMEOUT,
                )

            cluster_clause = f"ON CLUSTER {workspace.cluster}" if workspace.cluster else ""
            exists_quarantine = await ch_table_exists_async(
                f"{ds.id}_quarantine", workspace.database_server, workspace.database
            )
            queries: list[AlterQuery] = []
            if table_operations:
                table_operations_sql = [op.sql for op in table_operations]
                if cluster_clause:
                    func = build_async_query_ddl
                else:
                    func = build_query
                queries += [
                    func(f"ALTER TABLE {workspace.database}.{ds.id} {cluster_clause} {', '.join(table_operations_sql)}")
                ]
                if table_operations_quarantine and exists_quarantine:
                    table_operations_quarantine_sql = [op.sql for op in table_operations_quarantine]
                    queries += [
                        func(
                            f"ALTER TABLE {workspace.database}.{ds.id}_quarantine {cluster_clause} {', '.join(table_operations_quarantine_sql)}"
                        ),
                    ]
            if engine_operations:
                queries += [
                    build_async_query(f"ALTER TABLE {workspace.database}.{ds.id} {op}") for op in engine_operations
                ]
            if index_operations:
                queries += [
                    build_async_query_ddl(f"ALTER TABLE {workspace.database}.{ds.id} {cluster_clause} {op}")
                    for op in index_operations
                ]

            ds.install_hook(
                AlterDatasourceHook(
                    workspace, table_operations_clean + engine_operations + index_operations, dependencies_clean
                )
            )
            ds.install_hook(PGSyncDatasourceHook(workspace))

            error = None
            try:
                for hook in ds.hooks:
                    hook.before_alter_datasource(ds)

                for query in queries:
                    client = HTTPClient(workspace.database_server, database=workspace.database)

                    await client.query(
                        query.query,
                        read_only=False,
                        alter_sync=query.alter_sync,
                        max_execution_time=query.max_execution_time,
                        distributed_ddl_task_timeout=query.distributed_ddl_task_timeout,
                        distributed_ddl_output_mode=query.distributed_ddl_output_mode,
                    )

                for hook in ds.hooks:
                    hook.after_alter_datasource(ds)

                try:
                    if new_schema and (new_jsonpaths or ds.json_deserialization):
                        if data_linker:
                            with DataLinker.transaction(data_linker.id) as linker:
                                linker.update_settings({"json_deserialization": json_conf})
                            await DataLinker.publish(data_linker.id)
                        else:
                            Users.alter_datasource_json_deserialization(workspace, ds.id, json_conf)

                    if new_ttl is not None:
                        Users.alter_datasource_ttl(workspace, ds.id, new_ttl)
                except SchemaJsonpathMismatch:
                    raise ApiHTTPError.from_request_error(
                        ClientErrorBadRequest.alter_not_supported(
                            reason=f"Mismatch between schema and jsonpath parameters: schema={self.get_argument('schema')} jsonpath={new_jsonpaths}"
                        )
                    )

            except CHException as e:
                error = str(e)
                if (
                    e.code == CHErrors.DUPLICATE_COLUMN
                    and str(FALLBACK_PARTITION_COLUMN.get("normalized_name", "")) in error
                    and is_old_cli
                ):
                    error += ". Try upgrading the CLI to version 5.0.0 or higher to avoid this error."
                logging.exception(error)
                user_error = replace_table_id_with_datasource_id(workspace, error)
                raise ApiHTTPError(400, user_error)

            finally:
                if error:
                    for hook in ds.hooks:
                        hook.on_error(ds, error)
                tracker.track_datasource_ops(ds.operations_log(), request_id=self._request_id, workspace=workspace)
                # wait for mutations for some time
                if queries:

                    async def wait_for_mutations(database_server, database, table, cluster):
                        try:
                            mutations_finished = await ch_wait_for_mutations(
                                database_server,
                                database,
                                table,
                                max_mutations_seconds_to_wait=5,
                                cluster=cluster,
                                skip_unavailable_replicas=True,
                            )
                            if mutations_finished is False:
                                logging.warning(f"Mutations still detected for alter in {database}.{table}")
                        except RuntimeError as exc:
                            logging.exception(f"Error waiting for mutations after alter in {database}.{table}: {exc}")

                    await wait_for_mutations(workspace.database_server, workspace.database, ds.id, workspace.cluster)

                    if new_schema and table_operations_quarantine and exists_quarantine:
                        await wait_for_mutations(
                            workspace.database_server, workspace.database, f"{ds.id}_quarantine", workspace.cluster
                        )

        result = {"operations": kafka_operations + table_operations_clean + engine_operations + index_operations}
        if dependencies_clean:
            result.update({"dependencies": dependencies_clean})

        self.write_json(result)


class APIDataSourceExchangeHandler(BaseHandler):
    @authenticated
    @requires_write_access
    @with_scope(scopes.DATASOURCES_CREATE)
    async def post(self):
        workspace = self.get_workspace_from_db()

        is_exchange_api_allowed = FeatureFlagsWorkspaceService.feature_for_id(
            FeatureFlagWorkspaces.EXCHANGE_API, "", workspace.feature_flags
        )

        if not is_exchange_api_allowed:
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.exchange_disabled())

        ds_a_name_or_id = self.get_argument("datasource_a", None, True)
        if ds_a_name_or_id is None:
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.missing_parameter(parameter="datasource_a"))

        ds_b_name_or_id = self.get_argument("datasource_b", None, True)
        if ds_b_name_or_id is None:
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.missing_parameter(parameter="datasource_b"))

        ds_a = workspace.get_datasource(ds_a_name_or_id)
        if not ds_a:
            raise ApiHTTPError.from_request_error(ClientErrorNotFound.nonexisting_data_source(name=ds_a_name_or_id))

        ds_b = workspace.get_datasource(ds_b_name_or_id)
        if not ds_b:
            raise ApiHTTPError.from_request_error(ClientErrorNotFound.nonexisting_data_source(name=ds_b_name_or_id))

        error: Optional[str] = None
        try:
            completed_operations = {}

            # Swap CH table names
            tables_to_swap = [TablesToSwapWithWorkspace(workspace.database, ds_a.id, ds_b.id, workspace.id, None, None)]
            await ch_swap_tables(
                workspace.database_server,
                tables_to_swap,
                workspace.cluster,
                **workspace.ddl_parameters(skip_replica_down=True),
            )
            completed_operations["ch_swap_tables"] = (
                ch_swap_tables,
                [workspace.database_server, tables_to_swap, workspace.cluster],
                workspace.ddl_parameters(skip_replica_down=True),
            )
            # Swap CH quarantine table names
            quarantine_tables_to_swap = [
                TablesToSwapWithWorkspace(
                    workspace.database, f"{ds_a.id}_quarantine", f"{ds_b.id}_quarantine", workspace.id, None, None
                )
            ]
            await ch_swap_tables(
                workspace.database_server,
                quarantine_tables_to_swap,
                workspace.cluster,
                **workspace.ddl_parameters(skip_replica_down=True),
            )
            completed_operations["ch_swap_tables_quarantine"] = (
                ch_swap_tables,
                [workspace.database_server, quarantine_tables_to_swap, workspace.cluster],
                workspace.ddl_parameters(skip_replica_down=True),
            )

            # Swap engines cache
            Users.alter_datasource_engine(workspace, ds_a_name_or_id, ds_b.engine)
            completed_operations["alter_datasource_engine_a"] = (
                Users.alter_datasource_engine,
                [workspace, ds_a_name_or_id, ds_a.engine],
                {},
            )

            Users.alter_datasource_engine(workspace, ds_b_name_or_id, ds_a.engine)
            completed_operations["alter_datasource_engine_b"] = (
                Users.alter_datasource_engine,
                [workspace, ds_b_name_or_id, ds_b.engine],
                {},
            )

            # Swap json deserialization
            Users.alter_datasource_json_deserialization(workspace, ds_a_name_or_id, ds_b.json_deserialization)
            completed_operations["alter_datasource_json_deserialization_a"] = (
                Users.alter_datasource_json_deserialization,
                [workspace, ds_a_name_or_id, ds_a.json_deserialization],
                {},
            )

            Users.alter_datasource_json_deserialization(workspace, ds_b_name_or_id, ds_a.json_deserialization)
            completed_operations["alter_datasource_json_deserialization_b"] = (
                Users.alter_datasource_json_deserialization,
                [workspace, ds_b_name_or_id, ds_b.json_deserialization],
                {},
            )

        except Exception as e:
            logging.exception(e)

            # Revert completed operations
            for operation, (func, args, kwargs) in reversed(completed_operations.items()):
                try:
                    if asyncio.iscoroutinefunction(func):
                        await func(*args, **kwargs)
                    else:
                        func(*args, **kwargs)
                except Exception as revert_exception:
                    logging.exception(f"Failed to revert operation {operation}: {revert_exception}")
            error = str(e)
            raise ApiHTTPError.from_request_error(ServerErrorInternal.failed_exchange(error=error))
        finally:
            ops_log_entry = OpsLogEntry(
                start_time=datetime.now(timezone.utc),
                event_type="exchange",
                datasource_id=ds_a.id,
                datasource_name=ds_a.name,
                workspace_id=workspace.id,
                workspace_email=workspace.name,
                result="error" if error else "ok",
                elapsed_time=0,
                error=error,
                rows=0,
                rows_quarantine=0,
                options={"datasource_a": ds_a.name, "datasource_b": ds_b.name},
            )
            tracker.track_datasource_ops([ops_log_entry], request_id=self._request_id, workspace=workspace)

        self.set_status(200)


class APIDataSourceTruncateHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @authenticated
    @requires_write_access
    @with_scope(scopes.DATASOURCES_CREATE)
    async def post(self, ds_name):
        """
        Truncates a Data Source in your account. If the Data Source has dependent Materialized Views, those **won't** be truncated in cascade. In case you want to delete data from other dependent Materialized Views, you'll have to do a subsequent call to this method. Auth token in use must have the ``DATASOURCES:CREATE`` scope.

        .. code-block:: bash
            :caption: Truncating a Data Source

            curl \\
                -H "Authorization: Bearer <DATASOURCES:CREATE token>" \\
                -X POST "https://api.tinybird.co/v0/datasources/name/truncate"

        This works as well for the ``quarantine`` table of a Data Source. Remember that the quarantine table for a Data Source has the same name but with the "_quarantine" suffix.

        .. code-block:: bash
            :caption: Truncating the quarantine table from a Data Source

            curl \\
                -H "Authorization: Bearer <DATASOURCES:DROP token>" \\
                -X POST "https://api.tinybird.co/v0/datasources/:name_quarantine/truncate"
        """
        workspace = self.get_workspace_from_db()

        is_quarantine_table = ds_name.endswith("_quarantine")
        if is_quarantine_table:
            ds = get_datasource_quarantine(workspace, ds_name)
        else:
            ds = workspace.get_datasource(ds_name)
        if not ds:
            raise ApiHTTPError.from_request_error(ClientErrorNotFound.nonexisting_data_source(name=ds_name))

        ds.install_hook(TruncateDatasourceHook(workspace))
        ds.install_hook(LandingDatasourceHook(workspace))
        ds.install_hook(LastDateDatasourceHook(workspace))

        try:
            for hook in ds.hooks:
                hook.before_truncate(ds)
            table_details, _ = await ds.table_metadata(workspace)
            if table_details.engine != "Null" or is_quarantine_table:
                await ch_truncate_table_with_fallback(
                    workspace.database_server,
                    workspace.database,
                    ds.id,
                    workspace.cluster,
                    wait_setting=WAIT_ALTER_REPLICATION_OWN,
                    **workspace.ddl_parameters(skip_replica_down=True),
                )
            for hook in ds.hooks:
                after_truncate_async = sync_to_async(hook.after_truncate)
                await after_truncate_async(ds)
        except ValueError as e:
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.failed_truncate(error=str(e)))
        except Exception as e:
            logging.exception(e)
            raise ApiHTTPError.from_request_error(ServerErrorInternal.failed_truncate(error=e))
        finally:
            tracker.track_datasource_ops(ds.operations_log(), request_id=self._request_id, workspace=workspace)

        self.set_status(205)


class APIDataSourceDeleteHandler(BaseHandler):
    async def count_rows_to_be_deleted(self, workspace: User, datasource: Datasource):
        try:
            return await rows_affected_by_delete(workspace, datasource.id, self.delete_condition)

        except Exception as e:
            logging.exception(f"Query failed to retrieve count rows for delete_condition information: error: {e}")
            raise ApiHTTPError.from_request_error(ServerErrorInternal.failed_delete_condition(error=e))

    async def validate_engine_supported(self, workspace: User, datasource: Datasource):
        table_details = await ch_table_details_async(
            table_name=datasource.id, database_server=workspace["database_server"], database=workspace["database"]
        )
        if not engine_supports_delete(table_details.engine):
            raise ApiHTTPError.from_request_error(
                ClientErrorBadRequest.engine_not_supported_for_delete(engine=table_details.engine)
            )

    async def validate_and_init_datasource_delete(self, workspace: User, ds_name: Optional[str]):
        source_delete_condition = self.get_argument("delete_condition", None)

        if not ds_name:
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.invalid_data_source_delete_name())

        if ds_name.endswith("_quarantine"):
            existing_datasource = get_datasource_quarantine(workspace, ds_name)
        else:
            existing_datasource = Users.get_datasource(workspace, ds_name)
        if not existing_datasource:
            raise ApiHTTPError.from_request_error(
                ClientErrorBadRequest.nonexisting_data_source_delete_name(name=ds_name)
            )
        if not source_delete_condition:
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.mandatory_delete_condition())

        # We do a replacement of the tables to force validation and do any replacements that were necessary
        try:
            select_query = f"SELECT * FROM {existing_datasource.id} WHERE ({source_delete_condition})"
            replaced_select = Users.replace_tables(workspace, select_query)
            self.delete_condition = replaced_select[replaced_select.find("WHERE") + len("WHERE") :]
        except Exception as e:
            raise ApiHTTPError.from_request_error(
                ClientErrorBadRequest.failed_delete_condition(delete_condition=source_delete_condition, error=str(e))
            ) from e

        await self.validate_engine_supported(workspace, existing_datasource)

        workspace_max_jobs = DeleteLimits.max_active_delete_jobs.get_limit_for(workspace)
        if DeleteLimits.max_active_delete_jobs.has_reached_limit_in(workspace_max_jobs, {"workspace": workspace}):
            raise ApiHTTPError.from_request_error(
                ClientErrorBadRequest.max_active_delete_jobs(workspace_max_jobs=workspace_max_jobs)
            )

        self.datasource = existing_datasource
        self.datasource.install_hook(DeleteDatasourceHook(workspace, existing_datasource, source_delete_condition))
        self.datasource.install_hook(LandingDatasourceHook(workspace))
        self.datasource.install_hook(LastDateDatasourceHook(workspace))
        return self.datasource

    def launch_delete_job(self, workspace, datasource, delete_condition):
        job = new_delete_job(
            job_executor=self.application.job_executor,
            delete_condition=delete_condition,
            headers=self.get_headers(),
            workspace=workspace,
            datasource=datasource,
            request_id=self._request_id,
        )
        self.write_json({**self.get_job_output(job, workspace), **{"delete_id": job.id}})

        self.delete_id = job.id
        self.job_id = job.id

        return job

    @authenticated
    @requires_write_access
    @with_scope(scopes.DATASOURCES_CREATE)
    async def post(self, ds_name):
        """
        Deletes rows from a Data Source in your account given a SQL condition. Auth token in use must have the ``DATASOURCES:CREATE`` scope.

        .. code-block:: bash
            :caption: Deleting rows from a Data Source given a SQL condition

            curl \\
                -H "Authorization: Bearer <DATASOURCES:CREATE token>" \\
                --data "delete_condition=(country='ES')" \\
                "https://api.tinybird.co/v0/datasources/:name/delete"

        When deleting rows from a Data Source, the response will not be the final result of the deletion but a Job. You can check the job status and progress using the `Jobs API <api_reference_job url_>`_.
        In the response, ``id``, ``job_id``, and ``delete_id`` should have the same value:

        .. sourcecode:: json
            :caption: Delete API Response

            {
                "id": "64e5f541-xxxx-xxxx-xxxx-00524051861b",
                "job_id": "64e5f541-xxxx-xxxx-xxxx-00524051861b",
                "job_url": "https://api.tinybird.co/v0/jobs/64e5f541-xxxx-xxxx-xxxx-00524051861b",
                "job": {
                    "kind": "delete_data",
                    "id": "64e5f541-xxxx-xxxx-xxxx-00524051861b",
                    "job_id": "64e5f541-xxxx-xxxx-xxxx-00524051861b",
                    "status": "waiting",
                    "created_at": "2023-04-11 13:52:32.423207",
                    "updated_at": "2023-04-11 13:52:32.423213",
                    "started_at": null,
                    "is_cancellable": true,
                    "datasource": {
                        "id": "t_c45d5ae6781b41278fcee365f5bxxxxx",
                        "name": "shopping_data"
                    },
                    "delete_condition": "event = 'search'"
                },
                "status": "waiting",
                "delete_id": "64e5f541-xxxx-xxxx-xxxx-00524051861b"
            }

        To check on the progress of the delete job, use the ``job_id`` from the Delete API response to query the `Jobs API <api_reference_job url_>`_.

        For example, to check on the status of the above delete job:

        .. code-block:: bash
            :caption: checking the status of the delete job

            curl \\
                -H "Authorization: Bearer <TOKEN>" \\
                https://api.tinybird.co/v0/jobs/64e5f541-xxxx-xxxx-xxxx-00524051861b

        Would respond with:

        .. sourcecode:: json
            :caption: Job API Response

            {
                "kind": "delete_data",
                "id": "64e5f541-xxxx-xxxx-xxxx-00524051861b",
                "job_id": "64e5f541-xxxx-xxxx-xxxx-00524051861b",
                "status": "done",
                "created_at": "2023-04-11 13:52:32.423207",
                "updated_at": "2023-04-11 13:52:37.330020",
                "started_at": "2023-04-11 13:52:32.842861",
                "is_cancellable": false,
                "datasource": {
                    "id": "t_c45d5ae6781b41278fcee365f5bc2d35",
                    "name": "shopping_data"
                },
                "delete_condition": " event = 'search'",
                "rows_affected": 100
            }

        .. _delete_engines_parameters_and_options:
        .. raw:: html

            <h3 id="delete_engines_parameters_and_options">Data Source engines supported</h3>

        Tinybird uses ClickHouse as the underlying storage technology. ClickHouse features different strategies to store data, these different strategies define not only where and how the data is stored but what kind of data access, queries, and availability your data has. In ClickHouse terms, a Tinybird Data Source uses a `Table Engine <https://clickhouse.tech/docs/en/engines/table_engines/>`_ that determines those factors.

        Currently, Tinybird supports deleting data for data sources with the following Engines:

        - MergeTree
        - ReplacingMergeTree
        - SummingMergeTree
        - AggregatingMergeTree
        - CollapsingMergeTree
        - VersionedCollapsingMergeTree


        .. _delete_dependent_views:
        .. raw:: html

            <h3 id="delete_dependent_views">Dependent views deletion</h3>

        If the Data Source has dependent Materialized Views, those won't be cascade deleted. In case you want to delete data from other dependent Materialized Views, you'll have to do a subsequent call to this method for the affected view with a proper ``delete_condition``. This applies as well to the associated ``quarantine`` Data Source.

        .. csv-table:: Request parameters
            :header: "KEY", "TYPE", "DESCRIPTION"
            :widths: 5, 5, 30

            delete_condition, String, "Mandatory. A string representing the WHERE SQL clause you'd add to a regular DELETE FROM <table> WHERE <delete_condition> statement. Most of the times you might want to write a simple ``delete_condition`` such as ``column_name=value`` but any valid SQL statement including conditional operators is valid "
            dry_run, String, "Default: ``false``. It allows you to test the deletion. When using ``true`` it will execute all deletion validations and return number of matched ``rows_to_be_deleted``."

        """
        dry_run = self.get_argument("dry_run", "false") == "true"
        workspace = self.get_workspace_from_db()
        ds = await self.validate_and_init_datasource_delete(workspace, ds_name)

        if dry_run:
            rows_to_be_deleted = await self.count_rows_to_be_deleted(workspace, ds)
            response = {"rows_to_be_deleted": rows_to_be_deleted}
            self.write_json(response)
            self.set_status(200)
        else:
            self.launch_delete_job(workspace, ds, self.delete_condition)
            self.set_status(201)


def get_datasource_quarantine(user: User, ds_name: str) -> Optional[Datasource]:
    source_ds_name = ds_name[: len(ds_name) - len("_quarantine")]
    ds = Users.get_datasource(user, source_ds_name)
    if not ds:
        return None

    ds_dict = ds.to_dict()
    ds_dict["id"] += "_quarantine"
    ds_dict["name"] += "_quarantine"
    ds_dict["statistics"] = {}
    return Datasource.from_dict(ds_dict)


class APIDataSourceShareHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.mailgun_service = MailgunService(self.application.settings)

    @user_authenticated
    @requires_write_access
    async def post(self, datasource_id: str) -> None:
        """
        Requires user's own admin token. We will use it to know if the user has rights on the two workspaces involved.

        .. code-block:: bash
            :caption: Sharing a Data Source

            curl \\
            -H "Authorization: Bearer <ADMIN token>" \\
            -X POST "https://api.tinybird.co/v0/datasources/{datasource_id}/share" \\
            -d "origin_workspace_id={origin_workspace_id}" \\
            -d "destination_workspace_id={destination_workspace_id}"

        """
        user = self.get_user_from_db()

        origin_workspace = self._get_workspace_from_argument("origin_workspace_id")
        destination_workspace = self._get_workspace_from_argument("destination_workspace_id")
        if origin_workspace.id == destination_workspace.id:
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.cannot_share_datasource_with_parent_workspace())

        if origin_workspace.is_branch or destination_workspace.is_branch:
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.can_not_share_data_sources_between_branches())

        if not user.has_access_to(origin_workspace.id) or not user.has_access_to(destination_workspace.id):
            raise ApiHTTPError.from_request_error(ClientErrorForbidden.invalid_permissions_to_share_a_datasource())

        if not UserWorkspaceRelationship.user_is_admin(user_id=user.id, workspace_id=origin_workspace.id):
            raise ApiHTTPError.from_request_error(
                ClientErrorForbidden.invalid_permissions_to_share_a_datasource_as_guest()
            )

        if not origin_workspace.name_is_normalized_and_unique():
            raise ApiHTTPError.from_request_error(
                ClientErrorBadRequest.origin_workspace_does_not_have_a_normalized_and_unique_name(
                    name=origin_workspace.name
                )
            )

        share_between_clusters_activated = FeatureFlagsWorkspaceService.feature_for_id(
            FeatureFlagWorkspaces.SHARE_DATASOURCES_BETWEEN_CLUSTERS, "", origin_workspace.feature_flags
        )
        if not share_between_clusters_activated and not origin_workspace.lives_in_the_same_ch_cluster_as(
            destination_workspace
        ):
            raise ApiHTTPError.from_request_error(
                ClientErrorBadRequest.can_not_share_data_sources_between_workspaces_in_different_clusters()
            )

        try:
            new_ds = await WorkspaceService.share_a_datasource_between_workspaces(
                origin_workspace, datasource_id, destination_workspace
            )
        except DataSourceNotFound as data_source_not_found_exc:
            raise ApiHTTPError.from_request_error(
                ClientErrorNotFound.nonexisting_data_source(name=data_source_not_found_exc.datasource_name)
            )

        except DataSourceIsReadOnly:
            raise ApiHTTPError.from_request_error(
                ClientErrorBadRequest.a_shared_data_source_can_not_be_reshared(datasource_id=datasource_id)
            )

        except DatasourceAlreadySharedWithWorkspace as error:
            raise ApiHTTPError.from_request_error(
                ClientErrorBadRequest.data_source_already_shared_with_workspace(
                    datasource_name=error.datasource_name, workspace_id=error.workspace_id
                )
            )

        except Exception as e:
            logging.exception(e)
            error_message = str(e)
            raise ApiHTTPError(500, error_message)

        await self._send_notification_on_data_source_shared(user, destination_workspace, new_ds.name)

        self.set_status(200)

    async def _send_notification_on_data_source_shared(
        self, user_making_the_sharing: UserAccount, destination_workspace: User, new_ds_name: str
    ):
        workspace_users_emails = destination_workspace.get_user_emails_that_have_access_to_this_workspace()
        send_to_emails = list(filter(lambda x: x != user_making_the_sharing.email, workspace_users_emails))

        if len(send_to_emails) != 0:
            notification_result = await self.mailgun_service.send_notification_on_data_source_shared(
                send_to_emails, new_ds_name, destination_workspace.name, destination_workspace.id
            )

            if notification_result.status_code != 200:
                logging.error(
                    f"Notification for Data Source has been shared was not delivered to {send_to_emails}, "
                    f"code: {notification_result.status_code} reason: {notification_result.content}"
                )

    @user_authenticated
    @requires_write_access
    async def delete(self, datasource_id):
        """
        Requires user's own admin token. We will use it to know if the user has rights on the two workspaces involved.

        .. code-block:: bash
            :caption: Sharing a Data Source

            curl \\
            -H "Authorization: Bearer <ADMIN token>" \\
            -X DELETE "https://api.tinybird.co/v0/datasources/{datasource_id}/share" \\
            -d "origin_workspace_id={origin_workspace_id}" \\
            -d "destination_workspace_id={destination_workspace_id}"
        """
        user = self.get_user_from_db()

        origin_workspace = self._get_workspace_from_argument("origin_workspace_id")
        destination_workspace = self._get_workspace_from_argument("destination_workspace_id")

        if not user.has_access_to(origin_workspace.id) or not user.has_access_to(destination_workspace.id):
            raise ApiHTTPError.from_request_error(
                ClientErrorForbidden.invalid_permissions_to_stop_sharing_a_datasource()
            )

        if not UserWorkspaceRelationship.user_is_admin(user_id=user.id, workspace_id=origin_workspace.id):
            raise ApiHTTPError.from_request_error(
                ClientErrorForbidden.invalid_permissions_to_unshare_a_datasource_as_guest()
            )

        data_source_at_destination_workspace = destination_workspace.get_datasource(
            datasource_id, include_read_only=True
        )
        if data_source_at_destination_workspace and not isinstance(
            data_source_at_destination_workspace, SharedDatasource
        ):
            raise ApiHTTPError.from_request_error(
                ClientErrorBadRequest.a_normal_data_source_can_not_be_unshared(datasource_id=datasource_id)
            )
        try:
            await Users.stop_sharing_a_datasource(user, origin_workspace, destination_workspace, datasource_id)

        except DataSourceNotFound as data_source_not_found_exc:
            raise ApiHTTPError.from_request_error(
                ClientErrorNotFound.nonexisting_data_source(name=data_source_not_found_exc.datasource_name)
            )
        except DatasourceIsNotSharedWithThatWorkspace:
            raise ApiHTTPError.from_request_error(
                ClientErrorBadRequest.data_source_is_not_shared_with_that_workspace(
                    origin_workspace_name=origin_workspace.name, destination_workspace_name=destination_workspace.name
                )
            )
        except DependentMaterializedNodeException as e:
            raise ApiHTTPError.from_request_error(
                ClientErrorConflict.conflict_materialized_node(
                    break_ingestion_message=e.break_ingestion_message,
                    affected_materializations_message=e.affected_materializations_message,
                    dependent_pipes_message=e.dependent_pipes_message,
                )
            )

        except Exception as e:
            logging.exception(e)
            error = str(e)
            raise ApiHTTPError(500, error)

        self.set_status(204)

    def _get_workspace_from_argument(self, workspace_argument_name: str) -> User:
        workspace_id = self.get_argument(workspace_argument_name)
        workspace = User.get_by_id(workspace_id)
        if workspace is None:
            raise ApiHTTPError(400, f"Workspace '{workspace_id}' not found")
        return workspace


@tornado.web.stream_request_body
class APIAnalyze(BaseHandler):
    def __init__(self, application, request, **kwargs):
        self.decompressor = None
        self.first_data_chunk_received = False
        super().__init__(application, request, **kwargs)

    def check_xsrf_cookie(self):
        pass

    @check_rate_limit(Limit.api_datasources_create_schema)
    async def prepare(self):
        if self.request.method != "POST":
            return
        self.check_api_options(["url", "format", "dialect_delimiter", "dialect_escapechar", "dialect_new_line", "from"])
        if "gzip" in self.request.headers.get("Content-Encoding", "") or "gzip" in self.request.headers.get(
            "Content-Type", ""
        ):
            self.decompressor = zlib.decompressobj(wbits=16 + 15)
        self.workspace = self.get_workspace_from_db()
        self.request.connection.set_max_body_size(MAX_BODY_SIZE_BYTES_STREAM)
        content_type = self.request.headers.get("content-type", "")
        self.buffer = SingleChunker()
        self.multipart = content_type.startswith("multipart/form-data")
        if self.multipart:
            self._parser = StreamingFormDataParser(headers=self.request.headers)

            self.ndjson_multipart_target = CustomMultipartTarget(self._write)
            self.parquet_multipart_target = CustomMultipartTarget(self._write)
            self.csv_multipart_target = CustomMultipartTarget(self._write)
            self.autodetect_multipart_target = CustomMultipartTarget(self._write)
            self._parser.register("ndjson", self.ndjson_multipart_target)
            self._parser.register("parquet", self.parquet_multipart_target)
            self._parser.register("csv", self.csv_multipart_target)
            self._parser.register("file", self.autodetect_multipart_target)

    def _write(self, chunk):
        if not self.first_data_chunk_received:
            if has_gzip_magic_code(chunk):
                self.decompressor = zlib.decompressobj(wbits=16 + 15)
            self.first_data_chunk_received = True

        if self.decompressor:
            chunk = self.decompressor.decompress(chunk)
        self.buffer.write(chunk)

    async def data_received(self, chunk):
        try:
            if self.multipart:
                # We are using sync_to_async just to be sure that any blocking code is executed in the thread pool
                # When running a CSV replace, we will run some hooks that will run ON CLUSTER queries.
                # If a replica is down, the ON CLUSTER will take longer and would block the event loop.
                # Using sync_to_async we can run the code in the thread pool and not block the event loop.
                await sync_to_async(self._parser.data_received)(chunk)
            else:
                self._write(chunk)
        except IngestionError as e:
            return self.write_error(400, error=str(e))

    @authenticated
    @requires_write_access
    @with_scope(scopes.DATASOURCES_CREATE)
    async def post(self):
        """
        The Analyze API takes a sample of a supported file (``csv``, ``ndjson``, ``parquet``) and guesses the file format, schema, columns, types, nullables and JSONPaths (in the case of NDJSON paths).

        This is a helper endpoint to create Data Sources without having to write the schema manually.

        Take into account Tinybird's guessing algorithm is not deterministic since it takes a random portion of the file passed to the endpoint, that means it can guess different types or nullables depending on the sample analyzed. We recommend to double check the schema guessed in case you have to make some manual adjustments.

        .. code-block:: bash
            :caption: Analyze a local file

            curl \\
            -H "Authorization: Bearer <DATASOURCES:CREATE token>" \\
            -X POST "https://api.tinybird.co/v0/analyze" \\
            -F "file=@path_to_local_file"

        .. code-block:: bash
            :caption: Analyze a remote file

            curl \\
            -H "Authorization: Bearer <DATASOURCES:CREATE token>" \\
            -G -X POST "https://api.tinybird.co/v0/analyze" \\
            --data-urlencode "url=https://example.com/file"

        .. sourcecode:: json
            :caption: Analyze response

            {
                "analysis": {
                    "columns": [
                        {
                            "path": "$.a_nested_array.nested_array[:]",
                            "recommended_type": "Array(Int16)",
                            "present_pct": 3,
                            "name": "a_nested_array_nested_array"
                        },
                        {
                            "path": "$.an_array[:]",
                            "recommended_type": "Array(Int16)",
                            "present_pct": 3,
                            "name": "an_array"
                        },
                        {
                            "path": "$.field",
                            "recommended_type": "String",
                            "present_pct": 1,
                            "name": "field"
                        },
                        {
                            "path": "$.nested.nested_field",
                            "recommended_type": "String",
                            "present_pct": 1,
                            "name": "nested_nested_field"
                        }
                    ],
                    "schema": "a_nested_array_nested_array Array(Int16) `json:$.a_nested_array.nested_array[:]`, an_array Array(Int16) `json:$.an_array[:]`, field String `json:$.field`, nested_nested_field String `json:$.nested.nested_field`"
                },
                "preview": {
                    "meta": [
                        {
                            "name": "a_nested_array_nested_array",
                            "type": "Array(Int16)"
                        },
                        {
                            "name": "an_array",
                            "type": "Array(Int16)"
                        },
                        {
                            "name": "field",
                            "type": "String"
                        },
                        {
                            "name": "nested_nested_field",
                            "type": "String"
                        }
                    ],
                    "data": [
                        {
                            "a_nested_array_nested_array": [
                                1,
                                2,
                                3
                            ],
                            "an_array": [
                                1,
                                2,
                                3
                            ],
                            "field": "test",
                            "nested_nested_field": "bla"
                        }
                    ],
                    "rows": 1,
                    "statistics": {
                        "elapsed": 0.000310539,
                        "rows_read": 2,
                        "bytes_read": 142
                    }
                }
            }

        The ``columns`` attribute contains the guessed columns and for each one:

        - ``path``: The JSONPath syntax in the case of NDJSON/Parquet files
        - ``recommended_type``: The guessed database type
        - ``present_pct``: If the value is lower than 1 then there was nulls in the sample used for guessing
        - ``name``: The recommended column name

        The ``schema`` attribute is ready to be used in the `Data Sources API <api_reference_datasource url_>`_

        The ``preview`` contains up to 10 rows of the content of the file.
        """
        self.decompressor = None
        if self.multipart and not self.buffer.buffer_size():
            err = ClientErrorBadRequest.wrong_multipart_name()
            self.write_error(err[0], error=err[1])
            return

        url = self.get_argument("url", None)
        if url:
            url = await validate_redirects_and_internal_ip(url, self.application.settings)
            session = get_shared_session()

            format = self.get_api_option("format", {"csv", "ndjson", "parquet", "auto"}, "auto")
            extension = SharedUtils.UrlUtils.get_file_extension(url)
            is_parquet_format = format == "parquet" or extension == "parquet"

            if is_parquet_format:
                # with parquet we need to download the entire file to analyze it
                max_url_size = self.workspace.get_limits(prefix="import").get(
                    "import_max_url_parquet_file_size_gb", None
                )
                max_url_size = max_url_size * GB if max_url_size is not None else None

                try:
                    SharedUtils.UrlUtils.check_file_size_limit(url, self.workspace, max_url_size, is_parquet=True)
                except FileSizeException as e:
                    raise ApiHTTPError(413, str(e))
                except Exception as e:
                    err = ClientErrorBadRequest.invalid_url_fetch_error(url=url, error_code=500, error_message=str(e))
                    raise ApiHTTPError.from_request_error(err)

                if FeatureFlagsWorkspaceService.feature_for_id(
                    FeatureFlagWorkspaces.PARQUET_THROUGH_CLICKHOUSE, self.workspace.id, self.workspace.feature_flags
                ):
                    return await self._analyze_with_clickhouse(url=url, format="parquet")
                else:
                    max_size_to_analyze = (
                        max_url_size if max_url_size is not None else Limit.import_max_url_parquet_file_size_dev_gb * GB
                    )
                    self.buffer = SingleChunker(max_size_to_analyze)
            else:
                max_size_to_analyze = ANALYZE_SIZE

            async def f(retry_me):
                try:
                    async with session.get(url, allow_redirects=False) as resp:
                        if not resp.ok:
                            retry_me()
                            try:
                                msg = await resp.text()
                            except Exception as e:
                                msg = str(e)
                            err = ClientErrorBadRequest.invalid_url_fetch_error(
                                url=url, error_code=resp.status, error_message=msg
                            )
                            raise ApiHTTPError.from_request_error(err)
                        if not self.decompressor and (
                            "gzip" in resp.headers.get("Content-Encoding", "")
                            or "gzip" in resp.headers.get("Content-Type", "")
                            or is_gzip_file(url)
                        ):
                            self.decompressor = zlib.decompressobj(wbits=16 + 15)
                        received_bytes = 0
                        download_completed = False
                        while received_bytes < max_size_to_analyze and not download_completed:
                            try:
                                chunk = await resp.content.readexactly(ANALYZE_SIZE)
                            except asyncio.IncompleteReadError as e:
                                chunk = e.partial
                                download_completed = True
                            if not chunk:
                                if received_bytes == 0:
                                    raise ApiHTTPError.from_request_error(ClientErrorBadRequest.no_data_url(url=url))
                                else:
                                    download_completed = True
                                    break
                            self._write(chunk)
                            received_bytes += len(chunk)
                except aiohttp.client_exceptions.ServerTimeoutError as e:
                    err = ClientErrorBadRequest.url_fetch_error(url=url, error_message=str(e))
                    raise ApiHTTPError.from_request_error(err)

            await retry_ondemand_async(f, backoff_policy=[1, 2])
        elif self.buffer.buffer_size() == 0:
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.no_data())
        await self._analyze()

    async def _analyze(self):
        try:
            head = self.buffer.head(ANALYZE_SIZE)
            format = self.get_api_option("format", {"csv", "ndjson", "parquet", "auto"}, "auto")
            if format == "auto" and self.multipart:
                if self.ndjson_multipart_target.written:
                    format = "ndjson"
                elif self.csv_multipart_target.written:
                    format = "csv"
                elif self.parquet_multipart_target.written:
                    format = "parquet"
            if format == "auto":
                format = detect_format(head)
            if format == "ndjson":
                await self._analyze_ndjson(head)
            elif format == "csv":
                await self._analyze_csv_legacy(head)
            elif format == "parquet":
                await self._analyze_parquet(self.buffer)
        except CHException as e:
            error = str(e)
            if isinstance(e, CHLocalException):
                error = str(e.ch_error)
            logging.exception(error)
            raise ApiHTTPError.from_request_error(
                ClientErrorBadRequest.unsupported_file_to_analyze_db_error(format=format, error=error)
            )
        except Exception as e:
            import traceback

            logging.exception(traceback.format_exc())
            raise e

    async def _analyze_ndjson(self, data):
        # json_guess
        lines = split_ndjson(data)
        raw_lines = lines
        if len(lines) > 2_000:
            random.seed(0)
            lines = random.sample(lines, k=1000)
        rows = []
        for line in lines:
            try:
                rows.append(orjson.loads(line))
            except orjson.JSONDecodeError:
                pass
        analysis = await analyze(rows)
        if not analysis:
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.unsupported_file_to_analyze(format="ndjson"))

        augmented_schema = analysis["schema"]
        parsed_schema = parse_augmented_schema(augmented_schema)
        schema = parsed_schema.schema
        jsonpaths = parsed_schema.jsonpaths
        try:
            json_conf = json_deserialize_merge_schema_jsonpaths(parse_table_structure(schema), jsonpaths)
        except SchemaJsonpathMismatch:
            logging.exception(
                f"Analyze mismatch between schema and jsonpath parameters: schema={schema} jsonpath={jsonpaths}"
            )
            self.write_error(500, error="Internal server error: mismatch between schema and jsonpath parameters")
            return
        extended_json_deserialization = extend_json_deserialization(json_conf)
        json_importer = NDJSONIngester(
            extended_json_deserialization=extended_json_deserialization,
            workspace_id=self.workspace.id,
            pusher="dry",
            block_tracker=DummyBlockLogTracker(),
        )
        # push data
        json_importer.write(b"\n".join(raw_lines[:PREVIEW_ROWS]) + b"\n")
        preview_data, _preview_quarantine = await json_importer.finish()
        # get preview
        response = {
            "analysis": analysis,
            "preview": preview_data,
        }
        # return response
        self.write_json(response)

    async def _analyze_parquet(self, data):
        try:
            pq_file = pq.ParquetFile(data.get_chunk(True))
        except Exception as e:
            logging.error(f"Error on _analyze_parquet. File is not a valid Parquet file: {e}")
            self.write_error(400, error="File is not a valid Parquet file")
            return
        for data in pq_file.iter_batches(64 * 1024, use_threads=False):
            rows = data.to_pylist()
            break
        if len(rows) > PREVIEW_ROWS:
            random.seed(0)
            rows = random.sample(rows, k=PREVIEW_ROWS)
        analysis = await analyze(rows)
        if not analysis:
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.unsupported_file_to_analyze(format="parquet"))

        augmented_schema = analysis["schema"]
        parsed_schema = parse_augmented_schema(augmented_schema)
        schema = parsed_schema.schema
        jsonpaths = parsed_schema.jsonpaths
        try:
            json_conf = json_deserialize_merge_schema_jsonpaths(parse_table_structure(schema), jsonpaths)
        except SchemaJsonpathMismatch:
            logging.exception(
                f"Analyze mismatch between schema and jsonpath parameters: schema={schema} jsonpath={jsonpaths}"
            )
            self.write_error(500, error="Internal server error: mismatch between schema and jsonpath parameters")
            return
        extended_json_deserialization = extend_json_deserialization(json_conf)
        json_importer = NDJSONIngester(
            extended_json_deserialization=extended_json_deserialization,
            workspace_id=self.workspace.id,
            pusher="dry",
            format="parquet",
            block_tracker=DummyBlockLogTracker(),
        )
        json_importer._decoder.limit_rows = PREVIEW_ROWS
        # push data
        json_importer._chunker = self.buffer
        preview_data, _preview_quarantine = await json_importer.finish()
        # get preview
        response = {
            "analysis": analysis,
            "preview": preview_data,
        }
        # return response
        self.write_json(response)

    async def _analyze_with_clickhouse(self, url: str, format: str):
        try:
            ch_analysis = await ch_analyze_from_url(url=url, format=format, limit=PREVIEW_ROWS)
        except CHAnalyzeError as e:
            self.write_error(400, error=str(e))
            return

        analysis: Dict[str, Any] = {}
        analysis["columns"] = ch_analysis.columns
        analysis["schema"] = ch_analysis.schema
        response = {
            "analysis": analysis,
            "preview": ch_analysis.preview,
        }
        self.write_json(response)

    async def _analyze_csv_legacy(self, data):
        data = data[: CSVImporterSettings.BYTES_TO_GUESS_CSV]
        extract, encoding = decode_with_guess(data)
        extract = cut_csv_extract(extract, CSVImporterSettings.BYTES_TO_GUESS_CSV)
        logging.info("extracted data length: %d", len(extract))
        dialect_overrides = dialect_from_handler(self)

        info = await sync_to_async(CSVInfo.extract_from_csv_extract)(
            extract, dialect_overrides=dialect_overrides._asdict(), type_guessing=True
        )
        csv_info = info.to_json()
        columns = [
            {
                "name": c["normalized_name"],
                "path": c["name"],
                "present_pct": 1 if not c["nullable"] else None,
                "recommended_type": c["type"],
            }
            for c in csv_info["schema"]
        ]
        schema = csv_info["sql_schema"]
        dialect = {
            "delimiter": csv_info["dialect"]["delimiter"],
            "has_header": bool(csv_info["dialect"]["has_header"]),
            "newline": csv_info["dialect"]["new_line"],
            "escapechar": csv_info["dialect"]["escapechar"],
            "encoding": encoding,
        }
        preview = None
        try:
            chunk, fmt, output_dialect, _ = next(
                process_chunk(extract, csv_info["schema"], csv_info["dialect"], [], None, None, use_native=False)
            )
            preview = await ch_local_query(
                "select * from table limit 10",
                chunk,
                fmt,
                schema,
                "JSON",
                dialect=output_dialect,
                timeout=10,
            )
            preview = orjson.loads(preview)
        except CHLocalException as e:
            raise ApiHTTPError.from_request_error(
                ClientErrorBadRequest.unsupported_file_to_analyze_db_error(format="csv", error=str(e.ch_error))
            )
        except Exception as e:
            raise ApiHTTPError.from_request_error(
                ClientErrorBadRequest.unsupported_file_to_analyze_db_error(format="csv", error=str(e))
            )

        response = {
            "analysis": {
                "columns": columns,
                "schema": schema,
            },
            "dialect": dialect,
            "preview": preview if preview else None,
        }
        self.write_json(response)

    async def _analyze_csv(self, data):
        data = data[: 256 * 1024]
        # decode
        data, encoding = decode_with_guess(data)
        # get dialect
        try:
            # since get_dialect is more permissive, this will fail with invalid CSVs
            # see test_analyze_wrong_file_error
            dialect = csv.Sniffer().sniff(data)
            # we still use our own dialect since it supports several corner cases
            new_dialect = get_dialect(data, {})
            has_header = bool(new_dialect["has_header"])
        except csv.Error as e:
            raise ApiHTTPError.from_request_error(ServerErrorInternal.analyze_csv_problem(error=e))

        dialect_override = dialect_from_handler(self)
        dialect.delimiter = dialect_override.delimiter or new_dialect["delimiter"]
        dialect.escapechar = dialect_override.escapechar or new_dialect["escapechar"]
        dialect.lineterminator = dialect_override.new_line or new_dialect["new_line"]

        # get rows
        reader = csv.reader(StringIO(data, newline=dialect.lineterminator), dialect)

        header = None
        lines = []
        for row in reader:
            if has_header and not header:
                header = row
            else:
                lines.append(row)
            if len(lines) >= 2000:
                break
        # send to analyze query
        analysis = await analyze(lines, format="csv", header=header)
        # preview first lines
        normalized_csv_buffer = StringIO()
        writer = csv.writer(normalized_csv_buffer, csv.unix_dialect)
        writer.writerows(lines)
        normalized_csv = normalized_csv_buffer.getvalue()

        def input_type(t):
            if "DateTime" in t:
                return "String"
            return t

        structure = ",".join(
            map(lambda c: f"{c['path'].replace('.', '_')} {input_type(c['recommended_type'])}", analysis["columns"])
        )

        def column_query_part(c):
            t = c["recommended_type"]
            name = c["path"].replace(".", "_")
            if "DateTime64" in t:
                if "null" in t:
                    return f"parseDateTime64BestEffortOrNull({name})"
                return f"parseDateTime64BestEffortOrZero({name})"
            if "DateTime" in t:
                if "null" in t:
                    return f"parseDateTimeBestEffortOrNull({name})"
                return f"parseDateTimeBestEffortOrZero({name})"
            return f"{name}"

        def alias(index):
            if header and index < len(header):
                return header[index]
            else:
                return f"column_{index}"

        query_part = ",".join([f"{column_query_part(x)} AS {alias(i)} " for i, x in enumerate(analysis["columns"])])
        preview_bytes = await ch_local_query(
            f"SELECT {query_part} FROM table",
            normalized_csv.encode("utf-8"),
            input_format="CSV",
            input_structure=structure,
        )
        preview = orjson.loads(preview_bytes)
        response = {
            "dialect": {
                "encoding": encoding,
                "newline": dialect.lineterminator,
                "delimiter": dialect.delimiter,
                "has_header": has_header,
            },
            "analysis": analysis,
            "preview": preview,
        }
        # return response
        self.write_json(response)


class APIDataSourceAnalyzeHandler(BaseHandler):
    @authenticated
    async def get(self, ds_name):
        workspace = self.get_workspace_from_db()
        datasource = workspace.get_datasource(ds_name, include_read_only=True)

        if not datasource:
            raise ApiHTTPError.from_request_error(ClientErrorNotFound.nonexisting_data_source(name=ds_name))

        if (
            not self.is_admin()
            and not self.has_scope(scopes.DATASOURCES_CREATE)
            and datasource.id not in self._get_access_info().get_resources_for_scope(scopes.DATASOURCES_READ)
        ):
            raise ApiHTTPError.from_request_error(ClientErrorForbidden.token_doesnt_have_access_to_this_resource())

        columns = await analyze_datasource(workspace, datasource)
        result = {
            "analysis": {
                "columns": columns,
            }
        }
        self.write_json(result)


async def analyze_datasource(workspace: User, datasource: Datasource) -> List[Dict[str, Any]]:
    pu = public.get_public_user()
    client = HTTPClient(pu.database_server, database=pu.database)
    _, query_result = await client.query(analyze_query(workspace.id, datasource.id, type=datasource.to_json()["type"]))
    paths_by_status = (await get_paths_by_status([datasource], workspace))[datasource.id]
    columns, _schema = process_analyze_query_result(query_result)
    seen_paths = set()

    paths_by_status_sets = {k: set(v) for k, v in paths_by_status.items()}
    for c in columns:
        seen_paths.add(c["path"])
        if c["path"] in paths_by_status_sets["new"]:
            c["status"] = "new"
        elif c["path"] in paths_by_status_sets["ingesting"]:
            c["status"] = "ingesting"
        elif c["path"] in paths_by_status_sets["ignored"]:
            c["status"] = "ignored"

    # Corner case, we may be ingesting a path without the data_guess knowing about it
    # this is unlikely unless the user sends wrong data, but that can happen (quarantine)
    for path in paths_by_status["ingesting"]:
        if path in seen_paths:
            continue
        col = next(x for x in datasource.json_deserialization if x["jsonpath"] == path)
        columns.append(
            {
                "name": col["name"],
                "path": path,
                "present_pct": 0,
                "recommended_type": None,
                "first_seen_date": None,
                "status": "ingesting",
            }
        )
    return columns


# Returns a dictionary of items with datasource IDs as keys
# with another dictionary as values.
# The second dictionary has 'ingesting', 'new', and 'ignored' as keys,
# and a list of JSONPaths as values.
async def get_paths_by_status(datasources: List[Datasource], workspace: User):
    paths_by_status: Dict[str, Dict[str, List[Any]]] = {}
    if not datasources:
        return paths_by_status
    for ds in datasources:
        paths_by_status[ds.id] = {
            "ingesting": [],
            "new": [],
            "ignored": [],
        }

    # Add paths that are being ingested already
    for ds in datasources:
        for column in ds.json_deserialization:
            paths_by_status[ds.id]["ingesting"].append(column["jsonpath"])

    # Add paths that are set to be ignored
    for ds in datasources:
        for path in ds.ignore_paths:
            if path not in paths_by_status[ds.id]["ingesting"]:
                paths_by_status[ds.id]["ignored"].append(path)

    # Add "new" paths, those that has been seen by `data_guess`
    # but that are not being ingested, not have been ignored by the user
    pu = public.get_public_user()
    tables_in_sql = ", ".join([f"'{ds.id}'" for ds in datasources])
    sql = f"""
    SELECT
        path,
        datasource_id
    FROM data_guess
    WHERE
        user_id = '{workspace.id}'
        AND datasource_id IN ({tables_in_sql})
        AND type NOT IN ('object', 'array', 'null')
    GROUP BY path, datasource_id
    FORMAT JSON
    """
    client = HTTPClient(pu.database_server, database=pu.database)
    body = None
    try:
        _, body = await client.query(sql, read_only=True, max_execution_time=3)
        rows = orjson.loads(body)["data"]
    except Exception:
        logging.exception(f"Query failed to retrieve data_guess information: SQL={sql} BODY={body!r}")
        rows = []
    for row in rows:
        ds_id = row["datasource_id"]
        path = row["path"]
        if (path in paths_by_status[ds_id]["ingesting"]) or (path in paths_by_status[ds_id]["ignored"]):
            continue
        paths_by_status[ds_id]["new"].append(path)

    return paths_by_status


class APIDependenciesHandler(BaseHandler):
    @authenticated
    @with_scope(scopes.DATASOURCES_CREATE)
    async def get(self) -> None:
        workspace = self.get_workspace_from_db()

        check_for_partial_replace = self.get_argument("check_for_partial_replace", default="false") == "true"
        datasource_name = self.get_argument("datasource", default=None)

        if not check_for_partial_replace:
            no_deps = self.get_argument("no_deps", default="false") == "true"
            recursive = self.get_argument("recursive", default="false") == "true"
            match = self.get_argument("match", default=None)
            pipe = self.get_argument("pipe", default=None)
            pattern = re.compile(match) if match else None

            try:
                response = workspace.get_dependencies(recursive=recursive, pipe=pipe, datasource_name=datasource_name)
            except SQLTemplateException as e:
                pipe_id = pipe.id if pipe else ""
                pipe_name = pipe.name if pipe else ""
                logging.exception(
                    f"cannot get dependencies: {str(e)} - pipe: {pipe_id}:{pipe_name} - datasource: {datasource_name}"
                )

            result = {}  # type: ignore
            for x in response:
                if not pattern or pattern.search(x):
                    if no_deps:
                        result[x] = []
                    else:
                        deps = response[x]
                        deps.sort()
                        result[x] = deps

            self.write_json({"dependencies": result})
        else:
            if not datasource_name:
                raise ApiHTTPError(
                    400, "To calculate the dependencies for a partial replace you need to select a Data Source."
                )
            datasource = workspace.get_datasource(datasource_name, include_read_only=True)
            if not datasource:
                raise ApiHTTPError(400, f"Data Source '{datasource_name}' not found")

            def get_ds_name(ds):
                if workspace.id == ds["workspace"]["id"]:
                    return ds["datasource"]["name"]
                else:
                    return f"{ds['workspace']['name']}.{ds['datasource']['name']}"

            deps_partial = await sync_to_async(get_partial_replace_dependencies)(workspace, datasource)
            self.write_json(
                {
                    "dependencies": {
                        get_ds_name(ds): [pipe["name"] for pipe in ds["pipes"]]
                        for ds in deps_partial["compatible_datasources"]
                    },
                    "incompatible_datasources": {
                        get_ds_name(ds): [] for ds in deps_partial["incompatible_datasources"]
                    },
                }
            )


#
# curl "http://localhost:8001/v0/datasources/events/ignore_paths" \
# -H "Authorization: Bearer $TOKEN" \
# -d '["$.wadus"]'
class APIDataSourceIgnorePathsHandler(BaseHandler):
    @authenticated
    @requires_write_access
    @with_scope(scopes.DATASOURCES_CREATE)
    async def post(self, ds_name):
        workspace = self.get_workspace_from_db()
        try:
            ignore_paths = json.loads(self.request.body)
        except Exception as e:
            logging.warn(e)
            raise ApiHTTPError(400, "Invalid request. Body must contain a list of strings (JSONPaths) in JSON format.")
        ds = workspace.get_datasource(ds_name)
        Users.alter_datasource_ignore_paths(workspace, ds.id, ignore_paths)


class APIDataSourceMetricsHandler(BaseHandler):
    @authenticated
    async def get(self, ds_name):
        workspace = self.get_workspace_from_db()
        datasource = workspace.get_datasource(ds_name, include_read_only=True)

        if not datasource:
            raise ApiHTTPError.from_request_error(ClientErrorNotFound.nonexisting_data_source(name=ds_name))

        metric = self.get_argument("type", default="storage")
        interval = int(self.get_argument("interval", default=60))
        workspace = workspace.get_main_workspace() if workspace.is_release else workspace
        datasource_metrics = DataSourceMetrics(workspace, datasource, metric, interval)
        metrics = await datasource_metrics.get_metric()
        self.write_json(metrics)


class APIDataSourceRecommendationsHandler(BaseHandler):
    @authenticated
    async def get(self, ds_name):
        workspace = self.get_workspace_from_db()
        datasource = workspace.get_datasource(ds_name, include_read_only=True)
        if not datasource:
            raise ApiHTTPError.from_request_error(ClientErrorNotFound.nonexisting_data_source(name=ds_name))

        _, columns = await datasource.table_metadata(
            workspace, include_default_columns=True, include_jsonpaths=True, include_stats=True
        )
        schema = table_structure(columns)
        api_key = self.application.settings.get("openai", {}).get("api_key", "")
        datasource_recommendations = DataSourceRecommendations(api_key)
        use_cases = await datasource_recommendations.generate_use_cases_from_schema(datasource, schema)
        self.write_json({"use_cases": use_cases})


class APIDataSourcesRecommendationsHandler(BaseHandler):
    @authenticated
    async def get(self):
        api_key = self.application.settings.get("openai", {}).get("api_key", "")
        prompt = self.get_argument("prompt", default="")
        datasource_recommendations = DataSourceRecommendations(api_key)
        recommendation_type = self.get_argument("type", "schema")

        if recommendation_type == "mockingbird_schema":
            schema = await datasource_recommendations.generate_mockingbird_schema(prompt)
            self.write_json({"schema": schema})
            return

        schema = await datasource_recommendations.generate_schema_from_description(prompt)
        self.write_json({"schema": schema})


def handlers():
    return [
        URLMethodSpec("GET", r"/v0/datasources/?", APIDataSourcesHandler),
        url(r"/v0/datasources/(.+)/alter", APIDataSourceAlterHandler),
        url(r"/v0/datasources/(.+)/share", APIDataSourceShareHandler),
        url(r"/v0/datasources/(.+)/truncate", APIDataSourceTruncateHandler),
        url(r"/v0/datasources/(.+)/analyze", APIDataSourceAnalyzeHandler),
        url(r"/v0/datasources/(.+)/delete", APIDataSourceDeleteHandler),
        url(r"/v0/datasources/(.+)/ignore_paths", APIDataSourceIgnorePathsHandler),
        url(r"/v0/datasources/(.+)/metrics", APIDataSourceMetricsHandler),
        url(r"/v0/datasources/(.+)/recommendations", APIDataSourceRecommendationsHandler),
        url(r"/v0/datasources/exchange", APIDataSourceExchangeHandler),
        url(r"/v0/datasources/recommendations", APIDataSourcesRecommendationsHandler),
        url(r"/v0/datasources/(.+)", APIDataSourceHandler),
        url(r"/v0/analyze/?", APIAnalyze),
        url(r"/v0/dependencies", APIDependenciesHandler),
    ]
