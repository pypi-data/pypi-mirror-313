import asyncio
import hashlib
import json
import logging
import re
import time
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

import orjson
import ulid
from chtoolset import query as chquery
from tornado.httputil import HTTPHeaders
from tornado.web import url

from tinybird.ch_utils.constants import COPY_ENABLED_TABLE_FUNCTIONS
from tinybird.ch_utils.user_profiles import WorkspaceUserProfiles
from tinybird.copy_pipes.job import new_copy_job
from tinybird.datasource import Datasource, SharedDatasource
from tinybird.feature_flags import FeatureFlagsWorkspaceService, FeatureFlagWorkspaces
from tinybird.playground.playground_service import PlaygroundService
from tinybird.sql_template_fmt import format_sql_template
from tinybird.user import User as Workspace
from tinybird.views.api_errors.pipes import process_syntax_error
from tinybird.views.utils import validate_table_function_host
from tinybird_shared.clickhouse.errors import CHErrors
from tinybird_shared.metrics.statsd_client import statsd_client

from ..ch import CacheConfig, HTTPClient, UserAgents, _ch_cancel_query_async_operation, remove_stream_operators_from_sql
from ..ch_utils.debug import get_execution_info, get_query_explain, get_trace_info
from ..ch_utils.exceptions import CHException
from ..limits import EndpointLimits, Limit, Limits
from ..sql import get_format, remove_format
from ..sql_template import (
    SQLTemplateCustomError,
    SQLTemplateException,
    TemplateExecutionResults,
    extract_variables_from_sql,
    get_used_tables_in_template,
    render_sql_template,
)
from ..sql_toolset import replace_tables, replacements_to_tuples, sql_get_used_tables
from ..timing import Timer
from ..tokens import scopes
from ..tornado_template import ParseError, UnClosedIfError
from ..user import PipeWithoutEndpoint, QueryNotAllowed, QueryNotAllowedForToken, public
from .api_errors.datasources import ClientErrorBadRequest
from .base import (
    ApiHTTPError,
    BaseHandler,
    authenticated,
    check_endpoint_concurrency_limit,
    check_plan_limit,
    check_workspace_limit,
)
from .utils import get_variables_for_query, is_table_function_in_error, validate_sql_parameter

VALID_FORMATS = (
    "JSON",
    "CSV",
    "CSVWithNames",
    "TSV",
    "TSVWithNames",
    "PrettyCompact",
    "JSONEachRow",
    "Parquet",
    "JSONStrings",
    "Prometheus",
)

# This is a global variable to keep track of the number of threads we need to assign to each endpoint
max_threads_by_endpoint: Dict[str, int] = {}

if TYPE_CHECKING:
    from tinybird.playground.playground import Playground
    from tinybird.user import Pipe


class APIQueryHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    async def try_to_cancel_clickhouse_request(self):
        try:
            if hasattr(self, "cancel_info"):
                database_server, database, query_id, cluster, fetch_time = self.cancel_info
                if time.monotonic() - fetch_time >= 1:
                    logging.warning(f"Connection closed by client, trying to cancel request: {self.cancel_info}")
                    await _ch_cancel_query_async_operation(
                        database_server, database, query_id, cluster, is_first=True, check_status=False
                    )
                    logging.warning(f"KILL query sent: {self.cancel_info}")
                else:
                    logging.warning(f"Connection closed by client, not cancelling request: {self.cancel_info}")
        except Exception as e:
            logging.warning(e)

    # def on_connection_close(self):
    #     try:
    #         tornado.ioloop.IOLoop.current().spawn_callback(self.try_to_cancel_clickhouse_request)
    #     except Exception as e:
    #         logging.warning(e)
    #     super().on_connection_close()

    def prepare(self):
        """max query size 3 kb"""
        kilobyte = 1024
        self.request.connection.set_max_body_size(3 * kilobyte)

    @authenticated
    @check_plan_limit(Limit.build_plan_api_requests)
    @check_workspace_limit(Limit.workspace_api_requests)
    @check_endpoint_concurrency_limit(query_api=True)
    async def get(self):
        """

        Executes a SQL query using the engine.

        .. code-block:: bash
            :caption: Running sql queries against your data

            curl --data "SELECT * FROM <pipe>" https://api.tinybird.co/v0/sql

        As a response, it gives you the query metadata, the resulting data and some performance statistics.

        .. sourcecode:: json
            :caption: Successful response

            {
            "meta": [
                {
                    "name": "VendorID",
                    "type": "Int32"
                },
                {
                    "name": "tpep_pickup_datetime",
                    "type": "DateTime"
                }
            ],
            "data": [
                {
                    "VendorID": 2,
                    "tpep_pickup_datetime": "2001-01-05 11:45:23",
                    "tpep_dropoff_datetime": "2001-01-05 11:52:05",
                    "passenger_count": 5,
                    "trip_distance": 1.53,
                    "RatecodeID": 1,
                    "store_and_fwd_flag": "N",
                    "PULocationID": 71,
                    "DOLocationID": 89,
                    "payment_type": 2,
                    "fare_amount": 7.5,
                    "extra": 0.5,
                    "mta_tax": 0.5,
                    "tip_amount": 0,
                    "tolls_amount": 0,
                    "improvement_surcharge": 0.3,
                    "total_amount": 8.8
                },
                {
                    "VendorID": 2,
                    "tpep_pickup_datetime": "2002-12-31 23:01:55",
                    "tpep_dropoff_datetime": "2003-01-01 14:59:11"
                }
            ],
            "rows": 3,
            "rows_before_limit_at_least": 4,
            "statistics":
                {
                    "elapsed": 0.00091042,
                    "rows_read": 4,
                    "bytes_read": 296
                }
            }

        Data can be fetched in different formats. Just append ``FORMAT <format_name>`` to your SQL query:

        .. code-block:: SQL
            :caption: Requesting different formats with SQL

            SELECT count() from <pipe> FORMAT JSON

        .. csv-table:: Request parameters
            :header: "Key", "Type", "Description"
            :widths: 20, 20, 60

            "q", "String", "The SQL query"
            "pipeline", "String", "(Optional) The name of the pipe. It allows writing a query like 'SELECT * FROM _' where '_' is a placeholder for the 'pipeline' parameter"
            "output_format_json_quote_64bit_integers", "int", "(Optional) Controls quoting of 64-bit or bigger integers (like UInt64 or Int128) when they are output in a JSON format. Such integers are enclosed in quotes by default. This behavior is compatible with most JavaScript implementations. Possible values: 0 — Integers are output without quotes. 1 — Integers are enclosed in quotes. Default value is 0"
            "output_format_json_quote_denormals", "int", "(Optional) Controls representation of inf and nan on the UI instead of null e.g when dividing by 0 - inf and when there is no representation of a number in Javascript - nan. Possible values: 0 - disabled, 1 - enabled. Default value is 0"
            "output_format_parquet_string_as_string", "int", "(Optional) Use Parquet String type instead of Binary for String columns. Possible values: 0 - disabled, 1 - enabled. Default value is 0"

        .. csv-table:: Available formats
            :header: "format", "Description"
            :widths: 20, 80

            "CSV", "CSV without header"
            "CSVWithNames", "CSV with header"
            "JSON", "JSON including data, statistics and schema information"
            "TSV", "TSV without header"
            "TSVWithNames", "TSV with header"
            "PrettyCompact", "Formatted table"
            "JSONEachRow", "Newline-delimited JSON values (NDJSON)"
            "Parquet", "Apache Parquet"
            "Prometheus", "Prometheus text-based format"

        As you can see in the example above, timestamps do not include a time
        zone in their serialization. Let's see how that relates to timestamps
        ingested from your original data:

        * If the original timestamp had no time zone associated, you'll read
          back the same date and time verbatim.

          If you ingested the timestamp ``2022-11-14 11:08:46``, for example,
          Tinybird sends ``"2022-11-14 11:08:46"`` back. This is so regardless
          of the time zone of the column in ClickHouse.

        * If the original timestamp had a time zone associated, you'll read back
          the corresponding date and time in the time zone of the destination
          column in ClickHouse, which is UTC by default.

          If you ingested ``2022-11-14 12:08:46.574295 +0100``, for instance,
          Tinybird sends ``"2022-11-14 11:08:46"`` back for a ``DateTime``, and
          ``"2022-11-14 06:08:46"`` for a ``DateTime('America/New_York')``.
        """
        pipeline = self.get_argument("pipeline", None)
        playground = self.get_argument("playground", None)
        finalize_aggregations = self.get_argument("finalize_aggregations", False) == "true"
        release_replacements = self.get_argument("release_replacements", False) == "true"

        q = self.get_argument("q", None, True)
        if not q:
            raise ApiHTTPError(400, "missing q parameter. example q=select%201")
        q = remove_stream_operators_from_sql(q)
        validate_sql_parameter(q)
        from_param = self.get_argument("from", None)

        self.log(q)
        max_threads = self._get_max_threads_param()
        output_format_json_quote_64bit_integers = self._get_output_format_json_quote_64bit_integers()
        output_format_parquet_string_as_string = self._get_output_format_parquet_string_as_string()
        output_format_json_quote_denormals = self._get_output_format_json_quote_denormals()

        workspace = self.get_workspace_from_db()
        endpoint_user_profile = workspace.profiles.get(WorkspaceUserProfiles.ENDPOINT_USER_PROFILE.value, None)
        if endpoint_user_profile:
            self.set_span_tag({"user_profile": endpoint_user_profile})

        variables = self._get_template_parameters()
        if not variables:
            # filter out our SQL_API_PARAMS from user parameters
            # this is to avoid raising an error if required variables are not provided, to avoid breaking the UI
            (_, variables) = get_variables_for_query(request=self.request, from_param=from_param)

        return await self._query(
            q,
            pipeline,
            max_threads,
            variables=variables,
            query_id=self._request_id,
            output_format_json_quote_64bit_integers=output_format_json_quote_64bit_integers,
            output_format_parquet_string_as_string=output_format_parquet_string_as_string,
            output_format_json_quote_denormals=output_format_json_quote_denormals,
            finalize_aggregations=finalize_aggregations,
            from_param=from_param,
            playground_id=playground,
            user=endpoint_user_profile,
            fallback_user_auth=True,
            release_replacements=release_replacements and self.is_admin(),
            secrets=workspace.get_secrets_for_template() if self.is_admin() else None,
        )

    @authenticated
    @check_plan_limit(Limit.build_plan_api_requests)
    @check_workspace_limit(Limit.workspace_api_requests)
    @check_endpoint_concurrency_limit(query_api=True)
    async def post(self):
        """

                Executes a SQL query using the engine, while providing a templated or non templated query
                string and the custom parameters that will be translated into the query.
                The custom parameters provided should not have the same name as the request parameters
                for this endpoint (outlined below), as they are reserved in order to get accurate results
                for your query.

                .. code-block:: bash
                    :caption: Running sql queries against your data

                    For example:

                    1. Providing the value to the query via the POST body:

                    curl -X POST \\
                        -H "Authorization: Bearer <PIPE:READ token>" \\
                        -H "Content-Type: application/json" \\
                        "https://api.tinybird.co/v0/sql" -d \\
                        '{
                            "q":"% SELECT * FROM <pipe> where column_name = {{String(column_name)}}",
                            "column_name": "column_name_value"
                        }'

                    2. Providing a new value to the query from the one defined within the pipe in the POST body:

                    curl -X POST \\
                        -H "Authorization: Bearer <PIPE:READ token>" \\
                        -H "Content-Type: application/json" \\
                        "https://api.tinybird.co/v0/sql" -d \\
                        '{
                            "q":"% SELECT * FROM <pipe> where column_name = {{String(column_name, "column_name_value")}}",
                            "column_name": "new_column_name_value"
                        }'

                    3. Providing a non template query in the POST body:

                    curl -X POST \\
                        -H "Authorization: Bearer <PIPE:READ token>" \\
                        -H "Content-Type: application/json" \\
                        "https://api.tinybird.co/v0/sql" -d \\
                        '{
                            "q":"SELECT * FROM <pipe>"
                        }'

                    4. Providing a non template query as a string in the POST body with a content type of "text/plain":

                    curl -X POST \\
                        -H "Authorization: Bearer <PIPE:READ token>" \\
                        -H "Content-Type: text/plain" \\
                        "https://api.tinybird.co/v0/sql" -d "SELECT * FROM <pipe>"

                .. csv-table:: Request parameters
                    :header: "Key", "Type", "Description"
                    :widths: 20, 20, 60

                    "pipeline", "String", "(Optional) The name of the pipe. It allows writing a query like 'SELECT * FROM _' where '_' is a placeholder for the 'pipeline' parameter"
                    "output_format_json_quote_64bit_integers", "int", "(Optional) Controls quoting of 64-bit or bigger integers (like UInt64 or Int128) when they are output in a JSON format. Such integers are enclosed in quotes by default. This behavior is compatible with most JavaScript implementations. Possible values: 0 — Integers are output without quotes. 1 — Integers are enclosed in quotes. Default value is 0"
                    "output_format_json_quote_denormals", "int", "(Optional) Controls representation of inf and nan on the UI instead of null e.g when dividing by 0 - inf and when there is no representation of a number in Javascript - nan. Possible values: 0 - disabled, 1 - enabled. Default value is 0"
                    "output_format_parquet_string_as_string", "int", "(Optional) Use Parquet String type instead of Binary for String columns. Possible values: 0 - disabled, 1 - enabled. Default value is 0"

                As a response, it gives you the query metadata, the resulting data and some performance statistics.

                .. sourcecode:: json
                    :caption: Successful response

                    {
                    "meta": [
                        {
                            "name": "VendorID",
                            "type": "Int32"
                        },
                        {
                            "name": "tpep_pickup_datetime",
                            "type": "DateTime"
                        }
                    ],
                    "data": [
                        {
                            "VendorID": 2,
                            "tpep_pickup_datetime": "2001-01-05 11:45:23",
                            "tpep_dropoff_datetime": "2001-01-05 11:52:05",
                            "passenger_count": 5,
                            "trip_distance": 1.53,
                            "RatecodeID": 1,
                            "store_and_fwd_flag": "N",
                            "PULocationID": 71,
                            "DOLocationID": 89,
                            "payment_type": 2,
                            "fare_amount": 7.5,
                            "extra": 0.5,
                            "mta_tax": 0.5,
                            "tip_amount": 0,
                            "tolls_amount": 0,
                            "improvement_surcharge": 0.3,
                            "total_amount": 8.8
                        },
                        {
                            "VendorID": 2,
                            "tpep_pickup_datetime": "2002-12-31 23:01:55",
                            "tpep_dropoff_datetime": "2003-01-01 14:59:11"
                        }
                    ],
                    "rows": 3,
                    "rows_before_limit_at_least": 4,
                    "statistics":
                        {
                            "elapsed": 0.00091042,
                            "rows_read": 4,
                            "bytes_read": 296
                        }
                    }

                Data can be fetched in different formats. Just append ``FORMAT <format_name>`` to your SQL query:

                .. code-block:: SQL
                    :caption: Requesting different formats with SQL

                    SELECT count() from <pipe> FORMAT JSON

                .. csv-table:: Available formats
                    :header: "format", "Description"
                    :widths: 20, 80

                    "CSV", "CSV without header"
                    "CSVWithNames", "CSV with header"
                    "JSON", "JSON including data, statistics and schema information"
                    "TSV", "TSV without header"
                    "TSVWithNames", "TSV with header"
                    "PrettyCompact", "Formatted table"
                    "JSONEachRow", "Newline-delimited JSON values (NDJSON)"
                    "Parquet", "Apache Parquet"

                As you can see in the example above, timestamps do not include a time
                zone in their serialization. Let's see how that relates to timestamps
                ingested from your original data:

                * If the original timestamp had no time zone associated, you'll read
                  back the same date and time verbatim.

                  If you ingested the timestamp ``2022-11-14 11:08:46``, for example,
                  Tinybird sends ``"2022-11-14 11:08:46"`` back. This is so regardless
                  of the time zone of the column in ClickHouse.

                * If the original timestamp had a time zone associated, you'll read back
                  the corresponding date and time in the time zone of the destination
                  column in ClickHouse, which is UTC by default.

                  If you ingested ``2022-11-14 12:08:46.574295 +0100``, for instance,
                  Tinybird sends ``"2022-11-14 11:08:46"`` back for a ``DateTime``, and
                  ``"2022-11-14 06:08:46"`` for a ``DateTime('America/New_York')``.
                """
        pipeline = self.get_argument("pipeline", None)
        playground = self.get_argument("playground", None)
        finalize_aggregations = self.get_argument("finalize_aggregations", False) == "true"
        release_replacements = self.get_argument("release_replacements", False) == "true"
        from_param = self.get_argument("from", None)
        (q, variables) = get_variables_for_query(request=self.request, from_param=from_param)

        if not q:
            raise ApiHTTPError(400, "The request body should contain a query")

        q = remove_stream_operators_from_sql(q)
        max_threads = self._get_max_threads_param()
        output_format_json_quote_64bit_integers = self._get_output_format_json_quote_64bit_integers()
        output_format_parquet_string_as_string = self._get_output_format_parquet_string_as_string()
        output_format_json_quote_denormals = self._get_output_format_json_quote_denormals()
        template_parameters = self._get_template_parameters()

        workspace = self.get_workspace_from_db()

        endpoint_user_profile = workspace.profiles.get(WorkspaceUserProfiles.ENDPOINT_USER_PROFILE.value, None)
        if endpoint_user_profile:
            self.set_span_tag({"user_profile": endpoint_user_profile})

        # save the body of the request in the spans tag column for observability
        body = self._get_query_body()
        if isinstance(body, dict):
            self.set_span_tag({"request_body": body})

        return await self._query(
            q=q,
            pipeline=pipeline,
            max_threads=max_threads,
            variables=template_parameters if template_parameters else variables,
            query_id=self._request_id,
            output_format_json_quote_64bit_integers=output_format_json_quote_64bit_integers,
            output_format_parquet_string_as_string=output_format_parquet_string_as_string,
            output_format_json_quote_denormals=output_format_json_quote_denormals,
            finalize_aggregations=finalize_aggregations,
            release_replacements=release_replacements and self.is_admin(),
            from_param=from_param,
            user=endpoint_user_profile,
            fallback_user_auth=True,
            playground_id=playground,
            secrets=workspace.get_secrets_for_template() if self.is_admin() else None,
        )

    def _get_query_body(self) -> Union[str, dict]:
        try:
            request_body = self.request.body.decode()
            body = json.loads(request_body)
        except UnicodeDecodeError:
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.invalid_encoding())
        except Exception:
            body = request_body
        return body

    def _mark_if_request_is_billable(
        self, from_param: Optional[str] = "", querying_only_service_datasource: bool = False
    ):
        """
        Super dirty approximation that may let some users abuse it, but it's one fast way to know if some query
        comes from the UI so we can discard it for billing purposes. We will improve this in case some users start
        abusing it. If you know a better and easier way to track this kind of billable requests without having to
        deal with a perfectly exposed api parameter and without having to change a lot how the UI interacts with the
        backend, let's implement it!
        """
        if from_param == "ui" or querying_only_service_datasource:
            self.set_span_tag({"billable": "false"})

    def _get_user_agent(self, from_param: Optional[str] = "", querying_only_service_datasources: bool = False) -> str:
        if from_param == "ui":
            return UserAgents.UI_QUERY.value
        elif from_param == "karman":
            return UserAgents.KARMAN_QUERY.value
        elif querying_only_service_datasources:
            return UserAgents.INTERNAL_QUERY.value

        return UserAgents.API_QUERY.value

    def _get_max_threads_param(self) -> int:
        max_threads = self.get_argument("max_threads", None, True)
        if max_threads is not None:
            try:
                max_threads = int(max_threads)
                if max_threads <= 0:
                    raise ApiHTTPError(400, "max_threads must be at least 1")
            except ValueError:
                raise ApiHTTPError(400, "max_threads must be an integer value")
        return max_threads

    def _get_output_format_json_quote_64bit_integers(self) -> Optional[int]:
        arg_value = self.get_argument("output_format_json_quote_64bit_integers", None, True)
        if arg_value is not None:
            try:
                arg_value = int(arg_value)
                if arg_value != 0 and arg_value != 1:
                    raise ApiHTTPError(400, "output_format_json_quote_64bit_integers must be 0 or 1")
            except ValueError:
                raise ApiHTTPError(400, "output_format_json_quote_64bit_integers must be an integer value")
        return arg_value

    def _get_output_format_json_quote_denormals(self) -> Optional[int]:
        arg_value = self.get_argument("output_format_json_quote_denormals", None, True)
        if arg_value is not None:
            try:
                arg_value = int(arg_value)
                if arg_value != 0 and arg_value != 1:
                    raise ApiHTTPError(400, "output_format_json_quote_denormals must be 0 or 1")
            except ValueError:
                raise ApiHTTPError(400, "output_format_json_quote_denormals must be an integer value")
        return arg_value

    def _get_output_format_parquet_string_as_string(self) -> Optional[int]:
        arg_value = self.get_argument("output_format_parquet_string_as_string", None, True)
        if arg_value is not None:
            try:
                arg_value = int(arg_value)
                if arg_value != 0 and arg_value != 1:
                    raise ApiHTTPError(400, "output_format_parquet_string_as_string must be 0 or 1")
            except ValueError:
                raise ApiHTTPError(400, "output_format_parquet_string_as_string must be an integer value")
        return arg_value

    def _get_template_parameters(self):
        """
        These template parameters are meant for previewing queries in the UI.
        Passed to the query generation function, so they should work the
        same as if provided in the Pipe API
        """
        template_parameters = self.get_argument("template_parameters", None)

        try:
            if template_parameters:
                return json.loads(template_parameters)
        except Exception:
            raise ApiHTTPError(400, "template_parameters must be a well-formed JSON")

    def _generate_log_comment(
        self, workspace: Workspace, pipe: Optional["Pipe"], playground: Optional["Playground"] = None
    ) -> bytes:
        """
        Generate a log that will be used for debugging or validator to have better tracking of the queries
        """
        log = {"workspace": workspace.name}
        if pipe:
            log["pipe"] = pipe.name
        if playground:
            log["playground"] = playground.name

        return orjson.dumps(log)

    def _get_pipe_if_not_exists(self, pipe: Optional["Pipe"], pipe_name_or_id: Optional[str]) -> Optional["Pipe"]:
        if pipe:
            return pipe

        if pipe_name_or_id:
            workspace = self.get_workspace_from_db()
            pipe = workspace.get_pipe(pipe_name_or_id)
            if not pipe:
                logging.info(f"Pipe Not Found in APIQuery · Pipeline: {pipe_name_or_id}")
                not_found_resource = f"Resource '{pipe_name_or_id}' not found"
                raise ApiHTTPError(403, not_found_resource)

        return pipe

    def _get_playground_if_not_exists(
        self, playground: Optional["Playground"], playground_id: Optional[str], semver: Optional[str] = None
    ) -> Optional["Playground"]:
        if playground:
            return playground

        if playground_id:
            workspace = self.get_workspace_from_db()
            _workspace = workspace
            if semver:
                _workspace = workspace.get_main_workspace()
            playground = PlaygroundService.get_playground_by_workspace(_workspace.id, playground_id, semver)
            if not playground:
                not_found_resource = f"Resource '{playground_id}' not found"
                raise ApiHTTPError(403, not_found_resource)

        return playground

    async def _query(
        self,
        q: str,
        pipeline: Optional[str],
        max_threads: Optional[int] = None,
        # The variables are the parameters that will be used to replace the placeholders in the query
        variables: Optional[Dict[str, Any]] = None,
        t_start: Optional[float] = None,
        query_id: Optional[str] = None,
        output_format_json_quote_64bit_integers: Optional[int] = None,
        output_format_json_quote_denormals: Optional[int] = None,
        output_format_parquet_string_as_string: Optional[int] = None,
        user_agent: Optional[str] = None,
        finalize_aggregations: bool = False,
        copy_to: Optional[Datasource] = None,
        from_param: Optional[str] = None,
        playground_id: Optional[str] = None,
        release_replacements: bool = False,
        user: Optional[str] = None,
        fallback_user_auth: bool = False,
        explain: bool = False,
        secrets: Optional[List[str]] = None,
    ):
        t_start = t_start or time.time()

        # At this point we don't know if we only use service datasources, so we assume we don't
        # and mark only based on the from_param.
        # We will check it again later, when we have the tables used in the query.
        if not copy_to:
            self._mark_if_request_is_billable(from_param, False)

        # check format
        format = get_format(q)
        if format and format.lower() not in map(str.lower, VALID_FORMATS):
            raise ApiHTTPError(403, "invalid format, available ones: %s" % ", ".join(VALID_FORMATS))

        parameters = variables if variables else {}
        self.set_span_tag({"parameters": parameters})

        workspace = self.get_workspace_from_db()
        semver = self.get_argument("__tb__semver", None)
        pipe = None
        playground = None
        render_time = None
        template_execution_results = TemplateExecutionResults()
        query_warnings = []
        q = q.strip()
        local_variables = {}

        if FeatureFlagsWorkspaceService.feature_for_id(
            FeatureFlagWorkspaces.INHERITED_TEMPLATING_VARIABLES, workspace.id, workspace.feature_flags
        ) and (pipeline or playground_id):
            pipe = self._get_pipe_if_not_exists(pipe, pipeline) if pipeline else None
            playground = (
                self._get_playground_if_not_exists(playground, playground_id, semver) if playground_id else None
            )
            pipe_or_playground = pipe or playground
            params = []
            query_to_extract = q[1:] if q[0] == "%" else q
            try:

                def get_dependencies(query: str) -> List[str]:
                    query = query[1:] if query[0] == "%" else query
                    sql, _, _ = render_sql_template(query, variables=None, test_mode=True, secrets=secrets)
                    tables = sql_get_used_tables(
                        sql, raising=True, table_functions=False, function_allow_list=COPY_ENABLED_TABLE_FUNCTIONS
                    )
                    dependencies = set([f"{d[0]}.{d[1]}" if d[0] != "" else d[1] for d in tables])
                    dependencies.update(get_used_tables_in_template(query))

                    return list(dependencies)

                def get_params_recursively(
                    query: str, visited_nodes: Optional[set[str]] = None
                ) -> List[Dict[str, Any]]:
                    visited_nodes = visited_nodes or set()
                    params = []
                    dependencies = get_dependencies(query)

                    for dep in dependencies:
                        if dep in visited_nodes:
                            continue
                        visited_nodes.add(dep)
                        if pipe_or_playground and (dep_node := pipe_or_playground.pipeline.get_node(dep)):
                            params += dep_node.get_template_params()
                            params += get_params_recursively(dep_node._sql, visited_nodes)

                        if dependant_pipe := workspace.get_pipe(dep):
                            params += dependant_pipe.get_params()
                            endpoint_params = dependant_pipe.pipeline.get_params(dependant_pipe.endpoint)
                            params += endpoint_params

                    return params

                params = get_params_recursively(query_to_extract)

                def extract_variables_recursively(
                    query: str, params: List[Dict[str, Any]], visited_nodes: Optional[set[str]] = None
                ) -> dict:
                    visited_nodes = visited_nodes or set()
                    variables = {}
                    dependencies = get_dependencies(query)
                    for dep in dependencies:
                        visited_nodes.add(dep)

                        if pipe_or_playground and (dep_node := pipe_or_playground.pipeline.get_node(dep)):
                            variables.update(extract_variables_recursively(dep_node._sql, params, visited_nodes))
                            variables.update(extract_variables_from_sql(dep_node._sql, params))

                        if dependant_pipe := workspace.get_pipe(dep):
                            for node in dependant_pipe.pipeline.nodes:
                                variables.update(extract_variables_recursively(node._sql, params, visited_nodes))
                                variables.update(extract_variables_from_sql(node._sql, params))

                    return variables

                local_variables.update(extract_variables_recursively(query_to_extract, params))
                local_variables.update(extract_variables_from_sql(query_to_extract, params))

            except Exception as e:
                logging.error(f"Error extracting variables from sql: {e}")
                raise e

        is_template = len(q) > 0 and q[0] == "%"
        if is_template or len(local_variables) > 0:
            # templated
            query_to_render = q[1:] if is_template else q
            try:
                test_mode = bool(not variables)
                if len(local_variables) > 0:
                    url_variables = variables or {}
                    variables = {**local_variables, **url_variables}

                with Timer("render sql template") as render_time:
                    q, template_execution_results, variable_warnings = render_sql_template(
                        query_to_render, variables, test_mode=test_mode, secrets=secrets
                    )

                    if len(variable_warnings) == 1:
                        query_warnings.append(
                            'The parameter name "{}" is a reserved word. Please, choose another name or the pipe will not work as expected.'.format(
                                variable_warnings[0]
                            )
                        )
                    elif len(variable_warnings) > 1:
                        query_warnings.append(
                            'The parameter names {} and "{}" are reserved words. Please, choose another name or the pipe will not work as expected.'.format(
                                ", ".join(['"{}"'.format(param) for param in variable_warnings[:-1]]),
                                variable_warnings[-1],
                            )
                        )
            except SQLTemplateCustomError as e:
                self.set_status(e.code)
                self.write(e.err)
                return
            except (ValueError, SQLTemplateException) as e:
                raise ApiHTTPError(
                    400, str(e), documentation=getattr(e, "documentation", "/query/query-parameters.html")
                )
            except (SyntaxError, ParseError, UnClosedIfError) as e:
                pipes = workspace.get_used_pipes_in_query(q=q)
                error = process_syntax_error(e, pipes=pipes)
                raise ApiHTTPError(400, error)
            except Exception as e:
                logging.warning(e)
                raise ApiHTTPError(500, str(e))
        raw_query = q
        workspace = self.get_workspace_from_db()
        readable_resources = None if self.is_admin() else self.get_readable_resources()
        query_id = query_id or ulid.new().str

        playground = self._get_playground_if_not_exists(playground, playground_id, semver)

        use_pipe_nodes = self.is_admin()
        allow_direct_access_to_service_datasources_replacements = self.is_admin() or self.has_scope(scopes.PIPES_CREATE)
        has_organization = bool(workspace.organization_id)
        if not has_organization and workspace.is_branch_or_release_from_branch:
            has_organization = bool(workspace.get_main_workspace().organization_id)

        allow_using_org_service_datasources = has_organization and self.is_organization_admin

        # The filters are used to filter the tables used in the query based on the access token
        access_token = self._get_access_info()
        filters = access_token.get_filters() if access_token else {}

        if semver and not copy_to:
            try:
                if semver == "regression-main":
                    workspace = workspace.get_main_workspace()
                if not workspace:
                    raise ValueError(f"Could not find Release {semver}")
            except Exception as e:
                raise ApiHTTPError(400, str(e))

        pipe = self._get_pipe_if_not_exists(pipe, pipeline)
        client = HTTPClient(workspace["database_server"], database=workspace["database"])

        try:
            with Timer("replace tables in sql") as replace_time:
                replaced_query, used_tables = await workspace.replace_tables_async(
                    q,
                    readable_resources=readable_resources,
                    pipe=pipe,
                    filters=filters,
                    use_pipe_nodes=use_pipe_nodes,
                    variables=variables,
                    template_execution_results=template_execution_results,
                    check_functions=True,
                    allow_direct_access_to_service_datasources_replacements=allow_direct_access_to_service_datasources_replacements,
                    allow_using_org_service_datasources=allow_using_org_service_datasources,
                    finalize_aggregations=finalize_aggregations,
                    playground=playground,
                    release_replacements=(release_replacements or copy_to) and self.is_admin(),
                    output_one_line=True,
                    secrets=secrets,
                )
                if semver == "regression":
                    # run query replaced in test branch in the main branch
                    replaced_query = replaced_query.replace(
                        f"{workspace.database}.",
                        f"{workspace.get_main_workspace().database}.",
                    )
                    workspace = workspace.get_main_workspace()
                    client = HTTPClient(workspace["database_server"], database=workspace["database"])
        except QueryNotAllowedForToken as e:
            raise ApiHTTPError(403, str(e), documentation="/api-reference/token-api.html")
        except QueryNotAllowed as e:
            if is_table_function_in_error(workspace, e) and from_param == "ui":
                try:
                    replaced_query, used_tables = await workspace.replace_tables_async(
                        q,
                        readable_resources=readable_resources,
                        pipe=pipe,
                        filters=filters,
                        use_pipe_nodes=use_pipe_nodes,
                        variables=variables,
                        template_execution_results=template_execution_results,
                        check_functions=True,
                        allow_direct_access_to_service_datasources_replacements=allow_direct_access_to_service_datasources_replacements,
                        allow_using_org_service_datasources=allow_using_org_service_datasources,
                        finalize_aggregations=finalize_aggregations,
                        playground=playground,
                        release_replacements=(release_replacements or copy_to) and self.is_admin(),
                        output_one_line=True,
                        function_allow_list=workspace.allowed_table_functions(),
                        secrets=secrets,
                    )
                    try:
                        ch_params = workspace.get_secrets_ch_params_by(template_execution_results.ch_params)
                        await validate_table_function_host(
                            replaced_query, self.application.settings, ch_params=ch_params
                        )
                    except ValueError as exc:
                        raise ApiHTTPError(400, str(exc), documentation="/api-reference/query-api.html")
                except QueryNotAllowed as ex:
                    raise ApiHTTPError(403, str(ex), documentation="/api-reference/query-api.html") from e
            else:
                raise ApiHTTPError(403, str(e), documentation="/api-reference/query-api.html")
        except PipeWithoutEndpoint as e:
            raise ApiHTTPError(400, str(e), documentation="/api-reference/pipe-api.html")
        except SQLTemplateCustomError as e:
            self.set_span_tag({"error": str(e.err), "http.status_code": e.code})
            self.set_status(e.code)
            self.write(e.err)
            return
        except (ValueError, SQLTemplateException) as e:
            raise ApiHTTPError(400, str(e), documentation=getattr(e, "documentation", "/query/query-parameters.html"))
        except (SyntaxError, ParseError, UnClosedIfError) as e:
            pipes = workspace.get_used_pipes_in_query(q=q, pipe=pipe)
            error = process_syntax_error(e, pipes=pipes)
            raise ApiHTTPError(400, error)

        max_execution_time = workspace.get_max_execution_time(is_admin=self.is_admin())

        max_threads_by_endpoint_according_to_cheriff = (
            workspace.get_endpoint_limit(pipe.name, EndpointLimits.max_threads) if pipe else None
        )
        max_threads_by_pipe_stats_rt = max_threads_by_endpoint.get(pipe.id) if pipe else None

        ch_limits = workspace.get_limits(prefix="ch")
        max_threads = Limits.max_threads(
            workspace=ch_limits.get("max_threads", None),
            endpoint_cheriff=max_threads_by_endpoint_according_to_cheriff or max_threads_by_pipe_stats_rt,
            request=max_threads,
            template=template_execution_results.get("max_threads", None),
        )
        max_result_bytes = ch_limits.get("max_result_bytes", Limit.ch_max_result_bytes)
        max_memory_usage = ch_limits.get("max_memory_usage", None)

        query_settings = {
            "max_execution_time": max_execution_time,
            "max_result_bytes": max_result_bytes,
            "log_comment": self._generate_log_comment(workspace, pipe, playground),
        }

        if max_threads:
            query_settings["max_threads"] = max_threads

        if max_memory_usage:
            query_settings["max_memory_usage"] = max_memory_usage

        if output_format_json_quote_64bit_integers is not None:
            query_settings["output_format_json_quote_64bit_integers"] = output_format_json_quote_64bit_integers

        if output_format_json_quote_denormals is not None:
            query_settings["output_format_json_quote_denormals"] = output_format_json_quote_denormals

        if output_format_parquet_string_as_string is not None:
            query_settings["output_format_parquet_string_as_string"] = output_format_parquet_string_as_string

        if max_estimated_execution_time := ch_limits.get("max_estimated_execution_time"):
            query_settings["max_estimated_execution_time"] = max_estimated_execution_time

        if timeout_before_checking_execution_speed := ch_limits.get("timeout_before_checking_execution_speed"):
            query_settings["timeout_before_checking_execution_speed"] = timeout_before_checking_execution_speed

        activate_feature = template_execution_results.get("activate", None)
        enabled_analyzer_in_cheriff = workspace.get_endpoint_limit(pipe.name, EndpointLimits.analyzer) if pipe else None
        if activate_feature == "analyzer" or enabled_analyzer_in_cheriff:
            query_settings["allow_experimental_analyzer"] = 1
        elif activate_feature == "parallel_replicas":
            query_settings["allow_experimental_parallel_reading_from_replicas"] = 1
            # Setting use_hedged_requests should be deactivated when using parallel replicas
            # see: https://github.com/ClickHouse/ClickHouse/issues/38904
            query_settings["use_hedged_requests"] = 0
            # Setting these values to force parallel replicas to use all replicas
            # probably those settings need to be adjusted in the future
            query_settings["max_parallel_replicas"] = 100
            query_settings["prefer_localhost_replica"] = 0

        if user:
            query_settings["user"] = user

        if self.get_argument("explain", "false") == "true" or explain:
            try:
                q_public, _ = await workspace.replace_tables_async(
                    raw_query,
                    readable_resources=readable_resources,
                    pipe=pipe,
                    filters=filters,
                    use_pipe_nodes=use_pipe_nodes,
                    variables=variables,
                    template_execution_results=template_execution_results,
                    check_functions=True,
                    allow_direct_access_to_service_datasources_replacements=allow_direct_access_to_service_datasources_replacements,
                    allow_using_org_service_datasources=allow_using_org_service_datasources,
                    finalize_aggregations=finalize_aggregations,
                    playground=playground,
                    release_replacements=(release_replacements or copy_to) and self.is_admin(),
                    output_one_line=True,
                    # The below, and not passing secrets=secrets are the differences with the previous call to to
                    # replace_tables_async
                    use_service_datasources_replacements=False,
                )

                explain_result = await self.get_public_query_explain(
                    query=q_public,
                    query_public=replaced_query,
                    workspace=workspace,
                    client=client,
                    query_settings=query_settings,
                )

                self.write_json(explain_result)
                return
            except Exception as e:
                raise ApiHTTPError(400, str(e))

        if self.get_argument("debug", "false") in ("query", "analyze", "query_results"):
            debug_q = replaced_query
            if not self.get_argument("debug_source_tables", "false") == "true":
                debug_replacements = {(workspace["database"], x.id): x.name for x in workspace.get_datasources()}
                debug_q = replace_tables(replaced_query, debug_replacements, default_database="")
            self.write(
                f"""
                <h1>QUERY DEBUG</h1>
                <h2>SERVER = {workspace['database_server']}</h2>
                <h2>DATABASE = {workspace['database']}</h2>
                <h2>SQL</h2>
                <textarea rows=40 style="width: 100%;">{debug_q}</textarea>
            """
            )

            if self.get_argument("debug", "false") in ("analyze", "query_results"):
                # Get the EXPLAIN info
                query_explain = await get_query_explain(client, remove_format(replaced_query), **query_settings)
                self.write(
                    f"""
                    <br>
                    <h2>EXPLAIN<h2>
                    <textarea rows=40 style="width: 100%;">{query_explain}</textarea>
                """
                )

            if self.get_argument("debug", "false") == "analyze":
                # run the query with trace log
                trace_log = await get_trace_info(
                    client, replaced_query, workspace["database_server"], query_id, **query_settings
                )
                # try with the default port
                self.write(
                    f"""
                    <h2>TRACE</h2>
                    <textarea rows=40 style="width: 100%;">{trace_log}</textarea>
                    <p>
                    <a href="?debug=query_results&query_id={query_id}">See execution results</a>
                    </p>
                """
                )
            elif (
                self.get_argument("debug", "false") == "query_results"
                and self.get_argument("query_id", None) is not None
            ):
                ei = await get_execution_info(
                    client, self.get_argument("query_id"), workspace["database_server"], workspace["cluster"]
                )
                if ei:
                    self.write("""<h2>EXECUTION</h2><table>""")
                    for name, value in ei:
                        self.write(f"""<tr><td>{name}</td><td>{value}</td></tr>""")
                    self.write("""</table>""")
                else:
                    self.write("""No results yet, wait for a few seconds and reload""")
            return

        query_hash = f"{workspace.id}:{hashlib.md5(replaced_query.encode()).hexdigest()}"

        # Setting the backend_hint_default as the query hash. Leaving the door open to future improvements where
        # the hint could be based on the databases/tables being used in the query. That way we could do a more
        # efficient usage of the CH page cache
        backend_hint_default = query_hash
        disabled_backend_hint_in_cheriff = (
            workspace.get_endpoint_limit(pipe.name, EndpointLimits.backend_hint) if pipe else None
        )
        backend_hint = None if disabled_backend_hint_in_cheriff else backend_hint_default
        backend_hint = template_execution_results.get("backend_hint", backend_hint)

        enabled_max_bytes_before_external_group_by = (
            workspace.get_endpoint_limit(pipe.name, EndpointLimits.max_bytes_before_external_group_by) if pipe else None
        )
        if enabled_max_bytes_before_external_group_by:
            query_settings["max_bytes_before_external_group_by"] = enabled_max_bytes_before_external_group_by

        cache_ttl = template_execution_results.get("cache_ttl", None)
        cache_config = None
        if cache_ttl:
            cache_config = CacheConfig(query_hash, cache_ttl)
        ch_params = workspace.get_secrets_ch_params_by(template_execution_results.ch_params)

        async def fetch_query(
            attempt: int = 0, user_agent: Optional[str] = None, compressed: bool = False
        ) -> Tuple[HTTPHeaders, bytes, Timer]:
            user_agent = user_agent or UserAgents.API_QUERY.value

            try:
                with Timer("fetching query results from ch") as fetch_time:
                    self.cancel_info = (
                        workspace.database_server,
                        workspace.database,
                        query_id,
                        workspace.cluster,
                        time.monotonic(),
                    )
                    headers, body = await client.query(
                        replaced_query,
                        query_id=query_id,
                        compress=compressed,
                        read_cluster=True,
                        read_only=True,
                        backend_hint=backend_hint,
                        user_agent=user_agent,
                        cache_config=cache_config,
                        cluster=workspace.cluster,
                        fallback_user_auth=fallback_user_auth,
                        **query_settings,
                        **ch_params,
                    )
            except CHException as e:
                extra_headers = {"X-DB-Exception-Code": e.code}
                if "X-DB-Backend" in e.headers:
                    extra_headers["X-DB-Backend"] = e.headers["X-DB-Backend"]
                if cache_ttl and "X-Cache-Hits" in e.headers:
                    extra_headers["X-Cache-Hits"] = e.headers["X-Cache-Hits"]
                if e.fatal:
                    logging.exception(f"Unexpected error, query_id: {query_id} error: {e}")
                    raise ApiHTTPError(
                        500,
                        "Unexpected error, contact support@tinybird.co, request id: %s" % query_id,
                        extra_headers=extra_headers,
                    ) from e
                status_code = 400
                error_message = str(e)
                if e.code == CHErrors.TIMEOUT_EXCEEDED:
                    status_code = 408
                elif e.code == CHErrors.QUERY_WAS_CANCELLED:
                    status_code = 499
                    error_message = "Query was cancelled because the client closed the connection"
                elif e.code == CHErrors.TOO_MANY_SIMULTANEOUS_QUERIES:
                    raise ApiHTTPError(500, error_message, extra_headers=extra_headers) from e
                elif e.code == CHErrors.MEMORY_LIMIT_EXCEEDED:
                    if e.is_global_memory_limit:
                        status_code = 500
                        # we only log the total memory limit because we need to alert, the query memory limit is just fine and can be fixed by the user or via support
                        statsd_client.incr(f"tinybird.{statsd_client.region_machine}.ch_errors.MEMORY_LIMIT_EXCEEDED")
                    elif e.is_query_memory_limit:
                        status_code = 400
                elif e.code == CHErrors.UNKNOWN_IDENTIFIER:
                    # In some cases where clickhouse can't find a column in a query, the error message contains the full
                    # failing query. We don't want to show that to our users. Instead, we will show them the query as
                    # they can see it in tinybird.
                    # The full query is included in UNKNOWN_IDENTIFIER errors matching the patterns below:
                    missing_cols_error_regex = r"\[Error\] Missing columns: ('.*') while processing query: "
                    unknown_expression_identifier_regex = r"\[Error\] Unknown expression identifier .* in scope "
                    missing_cols_match = re.match(missing_cols_error_regex, error_message)
                    unknown_expression_match = re.match(unknown_expression_identifier_regex, error_message)
                    if missing_cols_match is not None:
                        error_message = (
                            f"{missing_cols_match.group(0)}'{raw_query}'"
                            f", required_columns: {missing_cols_match.group(1)}. (UNKNOWN_IDENTIFIER)"
                        )
                    if unknown_expression_match is not None:
                        error_message = f"{unknown_expression_match.group(0)}{raw_query}. (UNKNOWN_IDENTIFIER)"
                    raise ApiHTTPError(
                        400,
                        error_message,
                        extra_headers=extra_headers,
                    ) from e
                elif e.code == CHErrors.UNKNOWN_TABLE:
                    # Trying to report the original node/pipe/datasource
                    used_tables = sql_get_used_tables(
                        replaced_query, raising=False, default_database=workspace["database"], table_functions=False
                    )
                    not_found_resource = None
                    for table in used_tables:
                        database, table_name, _ = table
                        complete_table_name = f"{database}.{table_name}" if database != "" else table_name
                        if complete_table_name in error_message:
                            table_name = complete_table_name.split(".")[-1]
                            r = workspace.get_resource(table_name)
                            if r:
                                is_quarantine = (
                                    table_name.endswith("_quarantine") and r.resource.lower() == "datasource"
                                )
                                if is_quarantine:
                                    not_found_resource = f"{r.resource} '{r.name}_quarantine' is not found. Quarantine tables are created when creating a Data Source or when trying to ingest data to them."
                                    status_code = 404
                                else:
                                    not_found_resource = f"{r.resource} '{r.name}' not available at this time, you should retry the request"
                            else:
                                not_found_resource = (
                                    f"Resource '{table_name}' not available at this time, you should retry the request"
                                )
                            break
                    if attempt <= 2:
                        attempt += 1
                        logging.warning(f"Retrying query {query_id}; attempt={attempt}")
                        await asyncio.sleep(0.1 * attempt)
                        return await fetch_query(attempt=attempt, user_agent=user_agent, compressed=compressed)
                    # Hiding internal table name
                    status_code = 409 if status_code != 404 else status_code
                    error_message = not_found_resource or "Unable to resolve resources in query"
                elif e.code == CHErrors.BAD_ARGUMENTS and format == "Prometheus":
                    error_message = f"Prometheus requires the query output to conform to a specific structure: {e}"
                await self._insert_bytes_summary_data_in_span(e.headers)
                raise ApiHTTPError(status_code, error_message, extra_headers=extra_headers) from e
            return headers, body, fetch_time

        compressed = "gzip" in self.request.headers.get("Accept-Encoding", "")
        if copy_to:
            job = await new_copy_job(
                self.application.job_executor,
                workspace=workspace,
                sql=replaced_query,
                target_datasource=copy_to,
                request_id=self._request_id,
                use_query_queue=True,
                app_settings=self.application.settings,
            )
            return job
        else:
            public_db: str = public.get_public_database()
            only_internal = all(database == public_db for database, _, _ in used_tables) if used_tables else False

            user_agent = self._get_user_agent(from_param, only_internal)
            self._mark_if_request_is_billable(from_param, only_internal)
            headers, body, fetch_time = await fetch_query(user_agent=user_agent, compressed=compressed)

        if "JSONEachRow" in replaced_query:
            self.set_header("content-type", "application/x-ndjson")
        else:
            self.set_header("content-type", headers["content-type"])
        if "X-DB-Backend" in headers:
            db_backend = headers["X-DB-Backend"]
            self.set_header("X-DB-Backend", db_backend)
            self.set_span_tag({"db_backend": db_backend})

        if cache_ttl and "X-Cache-Hits" in headers:
            cache_hits = headers["X-Cache-Hits"]
            self.set_header("X-Cache-Hits", cache_hits)
            self.set_span_tag({"cache_hits": cache_hits})

        await self._insert_bytes_summary_data_in_span(headers)

        if "content-encoding" in headers:
            self.set_header("content-encoding", headers["content-encoding"])
        render_time_seconds = 0
        if render_time:
            render_time_seconds = render_time.elapsed_seconds()
        replace_time_seconds = replace_time.elapsed_seconds()
        db_fetch_time_seconds = fetch_time.elapsed_seconds()
        db_time_seconds = headers.get("X-Request-Time-total", 0)
        db_fetch_queue_time_seconds = headers.get("X-Request-Time-queue", 0)

        if FeatureFlagsWorkspaceService.feature_for_id(
            FeatureFlagWorkspaces.LOG_MORE_HTTP_INSIGHTS, workspace.id, workspace.feature_flags
        ):
            insights = ["namelookup", "connect", "appconnect", "pretransfer", "starttransfer", "redirect"]
            insights_tags: Dict[str, Any] = {}
            for x in insights:
                insights_tags[x] = headers.get(f"X-Request-Time-{x}", 0)
            self.set_span_tag(insights_tags)

        self.set_header(
            "X-TB-Statistics",
            f'{{"elapsed":{time.time() - t_start},"db":{db_time_seconds},"fetch":{db_fetch_time_seconds},"threads":{max_threads}}}',
        )

        self.set_header(
            "X-Tb-Warning",
            json.dumps(query_warnings),
        )

        self.set_span_tag(
            {
                "fetch_time": db_fetch_time_seconds,
                "fetch_queue_time": db_fetch_queue_time_seconds,
                "db_time": db_time_seconds,
                "render_time": render_time_seconds,
                "replace_time": replace_time_seconds,
                "max_threads": max_threads,
                "compressed": compressed,
            }
        )
        self.write(body)

    async def _insert_bytes_summary_data_in_span(self, headers: HTTPHeaders) -> None:
        if "X-ClickHouse-Summary" in headers:
            self.set_header("X-DB-Statistics", headers["X-ClickHouse-Summary"])
            ch_summary = json.loads(headers["X-ClickHouse-Summary"])
            self.set_span_tag(
                {
                    "read_rows": ch_summary.get("read_rows", 0),
                    "read_bytes": ch_summary.get("read_bytes", 0),
                    "result_rows": ch_summary.get("result_rows", 0),
                    "virtual_cpu_time_microseconds": ch_summary.get("virtual_cpu_time_microseconds", 0),
                }
            )

    async def get_public_query_explain(
        self,
        query: str,
        query_public: str,
        workspace: Workspace,
        client: HTTPClient,
        query_settings: Dict[str, Any],
        description: bool = False,
    ) -> Dict[str, str]:
        debug_replacements = {
            (x.original_ds_database if type(x) is SharedDatasource else workspace["database"], x.id): x.name
            for x in workspace.get_datasources()
        }
        debug_query = replace_tables(query_public, debug_replacements, default_database="")

        # Get the EXPLAIN info
        query_explain = ""
        explain_error = ""

        try:
            query_explain = await get_query_explain(client, remove_format(query), **query_settings)

            # Replace database name to the public one
            for (db_id, ds_id), name in debug_replacements.items():
                query_explain = query_explain.replace(f"{db_id}.{ds_id}", name)
        except Exception as e:
            explain_error = str(e)

        return {
            "debug_query": debug_query,
            "query_explain": query_explain,
            "explain_error": explain_error,
        }


class APIQueryTablesHandler(BaseHandler):
    async def _tables(self):
        q = self.get_argument("q")
        validate_sql_parameter(q)
        raising = self.get_argument("raising", "false") == "true"
        is_copy = self.get_argument("is_copy", "false") == "true"
        table_functions = self.get_argument("table_functions", "false") == "true"
        try:
            tables = sql_get_used_tables(
                q,
                raising=raising,
                table_functions=table_functions,
                function_allow_list=COPY_ENABLED_TABLE_FUNCTIONS if is_copy else None,
            )
            if not table_functions:
                non_function_tables: List[Tuple[str, str]] = [(table[0], table[1]) for table in tables]
                return self.write_json({"tables": non_function_tables})
            self.write_json({"tables": tables})
        except Exception as e:
            raise ApiHTTPError(400, str(e))

    @authenticated
    async def get(self):
        await self._tables()

    @authenticated
    async def post(self):
        await self._tables()


class APIQueryReplaceHandler(BaseHandler):
    async def _replace(self):
        q = self.get_argument("q")
        validate_sql_parameter(q)
        r = self.get_argument("replacements", "{}")

        try:
            replacements = json.loads(r)
            parsed_replacements = replacements_to_tuples(replacements)
            replaced_q = replace_tables(q, replacements=parsed_replacements)
            self.write_json({"query": replaced_q})
        except Exception as e:
            raise ApiHTTPError(400, str(e))

    @authenticated
    async def get(self):
        await self._replace()

    @authenticated
    async def post(self):
        await self._replace()


class APIQueryCopyHandler(APIQueryHandler):
    @authenticated
    async def post(self):
        copy_to = self.get_argument("copy_to", None)
        workspace = self.get_workspace_from_db()

        try:
            q = self.request.body.decode()
        except UnicodeDecodeError:
            raise ApiHTTPError.from_request_error(ClientErrorBadRequest.invalid_encoding())
        if not q:
            raise ApiHTTPError(400, "The request body should contain a query")

        if not copy_to:
            raise ApiHTTPError(400, "The 'copy_to' argument needs to be a Branch Data Source name")

        datasource = workspace.get_datasource(copy_to)
        if not datasource:
            raise ApiHTTPError(400, f"Data Source {copy_to} does not exist or is read-only.")

        try:
            job = await self._query(q, None, copy_to=datasource, release_replacements=True)
            response = {}
            response["job"] = job.to_json()
            response["job"]["job_url"] = self.application.settings["api_host"] + "/v0/jobs/" + job.id
            self.write_json(response)
        except QueryNotAllowed as e:
            raise ApiHTTPError(403, str(e))
        except (ValueError, SQLTemplateException) as e:
            raise ApiHTTPError(400, str(e))


class APIQueryFormatHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @authenticated
    async def get(self):
        """
        Formats a SQL template.

        To save the formatted SQL you have to:

        - Create a Node
        - Call this method for an existing Node
        - Update the Node with the new SQL

        .. sourcecode:: bash
            :caption: Format a SQL

            curl
                -H "Authorization: Bearer <PIPE:READ token>" \\
                -X POST "https://api.tinybird.co/v0/sql_format?q=select+a,b,c+from+ds"

        .. csv-table:: Response codes
            :header: "Code", "Description"
            :widths: 20, 80

            "200", "No error"
            "403", "Forbidden. Provided token doesn't have permissions, it needs ``ADMIN``"
            "500", "Intenal server error"
        """
        q = self.get_argument("q", None, True)
        line_length = int(self.get_argument("line_length", 0))
        with_clickhouse = self.get_argument("with_clickhouse_format", "false") == "true"

        if not q:
            raise ApiHTTPError(400, "missing q parameter. example q=select%201")
        validate_sql_parameter(q)

        try:
            if with_clickhouse:
                formatted_sql = chquery.format(q.strip())
            else:
                formatted_sql = format_sql_template(q.strip(), line_length=line_length)
            self.write_json({"q": formatted_sql})
        except Exception as e:
            logging.exception(f"Unhandled error on format node: {str(e)}")
            raise ApiHTTPError(500, str(e))


def handlers():
    return [
        url(r"/v0/sql", APIQueryHandler, name="api_sql"),
        url(r"/v0/sql_tables", APIQueryTablesHandler),
        url(r"/v0/sql_replace", APIQueryReplaceHandler),
        url(r"/v0/sql_format", APIQueryFormatHandler),
        url(r"/v0/sql_copy", APIQueryCopyHandler),
    ]
