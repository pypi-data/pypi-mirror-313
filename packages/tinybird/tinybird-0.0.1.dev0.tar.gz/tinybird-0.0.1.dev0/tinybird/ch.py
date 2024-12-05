import ast
import asyncio
import dataclasses
import json
import logging
import os
import re
import shutil
import subprocess
import tempfile
import time
import traceback
import uuid
import zlib
from abc import ABC, abstractmethod  # encoding: utf-8
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from enum import Enum
from io import BytesIO, StringIO
from itertools import filterfalse, tee
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterable, List, NamedTuple, Optional, Set, Tuple, Union
from urllib.parse import urlparse

import orjson
import pycurl
import requests
import ulid
from chtoolset import query as chquery
from chtoolset.query import check_valid_write_query, get_left_table
from requests import RequestException, Response, Session
from requests.adapters import HTTPAdapter
from tornado.curl_httpclient import CurlAsyncHTTPClient
from tornado.httpclient import AsyncHTTPClient, HTTPError, HTTPRequest, HTTPResponse
from tornado.httputil import HTTPHeaders, url_concat
from urllib3.util.retry import Retry

from tinybird.sql import (
    TableIndex,
    TableProjection,
    engine_can_be_replicated,
    get_format_group,
    schema_to_sql_columns,
    wrap_finalize_aggregation,
)
from tinybird.syncasync import async_to_sync
from tinybird.views.json_deserialize_utils import DYNAMODB_META_COLUMNS, KAFKA_META_COLUMNS
from tinybird.views.request_context import engine_dict
from tinybird_shared.clickhouse.errors import CHErrors
from tinybird_shared.retry.retry import retry_sync

from . import csv_guess, text_encoding_guessing
from .ch_utils.ddl import DDL_OUTPUT_MODE_NULL_STATUS_ON_TIMEOUT, DDLQueryStatusResponse
from .ch_utils.describe_table import DescribeTable
from .ch_utils.engine import (
    TableDetails,
    engine_full_from_dict,
    engine_local_to_replicated,
    ttl_condition_from_engine_full,
)
from .ch_utils.exceptions import CHException
from .csv_guess import column_names, dialect_header_len, guess_column_names, guess_columns, guess_delimiter
from .csv_tools import csv_from_python_object
from .limits import Limit
from .sql_toolset import format_where_for_mutation_command, replace_tables, sql_get_used_tables

if TYPE_CHECKING:
    from tinybird.user import User


HOST_PATTERNS = {
    "postgresql": r"postgresql\(\s*([`'])(.*?)\1",
    "url": r"url\(\s*([`'])(.*?)\1",
    "mysql": r"mysql\(\s*([`'])(.*?)\1",
    "azureBlobStorage": r"azureBlobStorage\(\s*([`'])(.*?)\1",
    "gcs": r"gcs\(\s*([`'])(.*?)\1",
    "s3": r"s3\(\s*([`'])(.*?)\1",
    "iceberg": r"iceberg\(\s*([`'])(.*?)\1",
    "mongodb": r"mongodb\(\s*([`'])(.*?)\1",
    "deltaLake": r"deltaLake\(\s*([`'])(.*?)\1",
}


class StepCollector(ABC):
    @abstractmethod
    def add_step(self, id: Tuple[Any, Any, Any], status: str, kind: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def update_step(
        self, id: Tuple[Any, Any, Any], step_query_id: str, status: str, kind: str, error: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def update_stats(self, total_steps: int):
        pass


class UserAgents(Enum):
    INTERNAL_QUERY = "tb-internal-query"
    UI_QUERY = "tb-ui-query"
    KARMAN_QUERY = "tb-karman-query"
    API_QUERY = "tb-api-query"
    DELETE = "tb-delete-condition"
    SINKS = "tb-datasink-query"
    BOOSTER = "tb-booster-query"
    CPU_TIME_ALERT = "no-tb-cpu-time-alert-query"


WAIT_ALTER_REPLICATION_NO = "no_wait"
WAIT_ALTER_REPLICATION_OWN = "own"
WAIT_ALTER_REPLICATION_ALL = "all"
VALID_WAIT_VALUES = (WAIT_ALTER_REPLICATION_NO, WAIT_ALTER_REPLICATION_OWN, WAIT_ALTER_REPLICATION_ALL)


def validate_wait_setting(wait_setting: str) -> None:
    if wait_setting not in VALID_WAIT_VALUES:
        raise ValueError(f"Wait must be any of {VALID_WAIT_VALUES}, found='{wait_setting}'")


# TODO: Remove this monkey patching after updating to Tornado 6.1
# Fixed in: https://github.com/tornadoweb/tornado/pull/2679
class CurlAsyncHTTPClientMonkeyPatch(CurlAsyncHTTPClient):
    def _curl_setup_request(
        self,
        curl: pycurl.Curl,
        request: HTTPRequest,
        buffer: BytesIO,
        headers: HTTPHeaders,
    ) -> None:
        super()._curl_setup_request(curl, request, buffer, headers)

        if not request.decompress_response:
            curl.setopt(pycurl.ENCODING, None)


AsyncHTTPClient.configure(CurlAsyncHTTPClientMonkeyPatch, max_clients=80)


# bytes read to guess csv data types
CSV_SAMPLE_SIZE = 1024 * 100  # 100k
CSV_SAMPLE_LINES = 300

DEFAULT_TYPE = "String"

MUTATIONS_SYNC_RUN_ASYNC = 0
MUTATIONS_SYNC_WAIT_CURRENT_SERVER = 1
MUTATIONS_SYNC_WAIT_REPLICAS = 2
MAX_DELETE_CONDITION_EXECUTION_TIME = 30 * 60
MAX_EXECUTION_TIME = 10

MAX_COLUMNS_SCHEMA = 500
MAX_MUTATIONS_SECONDS_TO_WAIT = 360
MAX_CRASH_COUNTER = 10
MAX_QUERY_LOG_EMPTY_COUNTER = 100

MAX_EXECUTION_TIME_CLUSTER_INSTANCES_SECONDS = 3
MAX_EXECUTION_TIME_FLUSH_LOGS_SECONDS = 6
SKIP_PARTITION_SIZE_SAFEGUARD = 0
SKIP_TABLE_SIZE_SAFEGUARD = 0


def normalize_column_name(text: str) -> str:
    """
    >>> normalize_column_name('abc')
    'abc'
    >>> normalize_column_name('0')
    'c_0'
    >>> normalize_column_name('foo&bar')
    'foo_bar'
    >>> normalize_column_name('123-bar')
    'c_123_bar'
    >>> normalize_column_name('Options.Values')
    'Options_Values'
    """
    text = re.sub(r"[^0-9a-zA-Z_]", "_", text)
    if text[0] in "0123456789":
        return "c_" + text
    return text


def normalize_column_name_suggestion(text: str) -> str:
    """
    >>> normalize_column_name_suggestion('avgState(round(a))')
    'avgState_round_a'
    >>> normalize_column_name_suggestion('sumStateIf(value, 1=1)')
    'sumStateIf_value1_1'
    >>> normalize_column_name_suggestion('groupBitXor(toUInt32(number))')
    'groupBitXor_toUInt32_number'
    >>> normalize_column_name_suggestion('groupArrayArray([number])')
    'groupArrayArraynumber'
    """

    normalized_column_name = normalize_column_name(text)
    normalized_column_name = normalized_column_name.replace("__", "")

    if normalized_column_name[-1] == "_":
        normalized_column_name = normalized_column_name[:-1]
    return normalized_column_name


class CSVInfo:
    """this class contains information about a csv file like the columns,
    size, parts and so on"""

    def __init__(self, columns: List[Dict[str, Any]], dialect: Dict[str, Any], extract=None) -> None:
        # self.size = size
        self.columns: List[Dict[str, Any]] = columns
        self.extract = extract
        self.dialect = dialect
        self.encoding = "utf-8"

    def to_json(self) -> Dict[str, Any]:
        return {
            "schema": self.columns,
            "extract": self.extract,
            "encoding": self.encoding,
            "dialect": {
                "delimiter": self.dialect["delimiter"],
                "has_header": 1 if self.dialect["has_header"] else 0,
                "header_len": self.dialect["header_len"],
                "new_line": self.dialect["new_line"],
                "escapechar": self.dialect.get("escapechar", None),
            },
            "sql_schema": table_structure(self.columns),
        }

    def header_len(self) -> int:
        return dialect_header_len(self.dialect)

    def get_delimiter(self) -> str:
        return self.dialect["delimiter"]

    @staticmethod
    def convert_columns_to_safe_types(
        columns: List[Dict[str, Any]], include_fallback: bool = True
    ) -> List[Dict[str, Any]]:
        converted_columns = []
        column_list = [x["name"] for x in columns]
        fallback_partition_column_name = get_fallback_partition_column_name(column_list)

        for x in columns:
            if x["name"] == fallback_partition_column_name:
                continue
            converted_columns.append(
                {
                    "name": x["name"],
                    "normalized_name": x["normalized_name"],
                    "type": "String",
                    "nullable": True,
                    "auto": False,
                }
            )
        return converted_columns

    def get_ch_table(self, safe_types: bool = False, storage_policy: Optional[str] = None) -> "CHTable":
        """return clickhouse table needed to be generated"""
        columns = self.columns
        if safe_types:
            columns = CSVInfo.convert_columns_to_safe_types(columns)
        return CHTable(columns, engine=engine_dict.get(), storage_policy=storage_policy)

    @staticmethod
    def guess_delimiter(csv_extract: str) -> str:
        return guess_delimiter(csv_extract)

    @staticmethod
    def from_not_decoded_csv(csv_extract: bytes) -> "CSVInfo":
        data, encoding = text_encoding_guessing.decode_with_guess(csv_extract)
        info = CSVInfo.extract_from_csv_extract(data)
        info.encoding = encoding
        return info

    @staticmethod
    def has_cached_header(cached_source_csv_header_info: Dict[str, Any], guessed_header_hash: Any) -> bool:
        # when appending we want to avoid inserting the header as a row
        # we cache the headers in the CSV used on create and if the header guessing fails
        # we use it as a backup
        # for now we expect a full match of both headers
        # see test_append_and_create_no_autoguess_headers_second_time for an example
        if (
            cached_source_csv_header_info
            and "header_hash" in cached_source_csv_header_info
            and "header" in cached_source_csv_header_info
        ):
            return cached_source_csv_header_info["header_hash"] == guessed_header_hash
        return False

    @staticmethod
    def extract_from_csv_extract(
        csv_extract: str,
        safe_types: bool = False,
        dialect_overrides: Optional[Dict[str, Any]] = None,
        type_guessing: bool = True,
        cached_source_csv_header_info=None,
        skip_stats_collection=False,
    ) -> "CSVInfo":
        """extract info from csv from the first csv bytes
        >>> info = CSVInfo.extract_from_csv_extract('a,b,c,d\\n' + '\\n'.join(['10,2.0,"test",2010-10-20']*200))
        >>> info.columns
        [{'name': 'a', 'normalized_name': 'a', 'type': 'Int16', 'nullable': False, 'auto': False, 'stats': {'uniq': 1, 'quantiles': [10, 10, 10, 10, 10]}}, {'name': 'b', 'normalized_name': 'b', 'type': 'Float32', 'nullable': False, 'auto': False, 'stats': {'quantiles': [2, 2, 2, 2, 2]}}, {'name': 'c', 'normalized_name': 'c', 'type': 'String', 'nullable': False, 'auto': False, 'stats': {'uniq': 1}}, {'name': 'd', 'normalized_name': 'd', 'type': 'Date', 'nullable': False, 'auto': False, 'stats': {}}]
        >>> info = CSVInfo.extract_from_csv_extract('a|b|c|d\\n' + '\\n'.join(['10|2.0|"test"|2010-10-20']*200))
        >>> info.columns
        [{'name': 'a', 'normalized_name': 'a', 'type': 'Int16', 'nullable': False, 'auto': False, 'stats': {'uniq': 1, 'quantiles': [10, 10, 10, 10, 10]}}, {'name': 'b', 'normalized_name': 'b', 'type': 'Float32', 'nullable': False, 'auto': False, 'stats': {'quantiles': [2, 2, 2, 2, 2]}}, {'name': 'c', 'normalized_name': 'c', 'type': 'String', 'nullable': False, 'auto': False, 'stats': {'uniq': 1}}, {'name': 'd', 'normalized_name': 'd', 'type': 'Date', 'nullable': False, 'auto': False, 'stats': {}}]
        """

        dialect = csv_guess.get_dialect(csv_extract, dialect_overrides)

        columns = []
        csv_stream = StringIO(csv_extract, newline=None)

        column_type_guess = guess_columns(csv_extract, dialect["delimiter"], escapechar=dialect["escapechar"])

        if dialect["has_header"]:
            _column_names = column_names(csv_extract, dialect["delimiter"], len(column_type_guess))
        elif CSVInfo.has_cached_header(cached_source_csv_header_info, dialect["header_hash"]):
            _column_names = ast.literal_eval(cached_source_csv_header_info["header"])
            dialect["has_header"] = True
        else:
            _column_names = guess_column_names(
                csv_extract, dialect["delimiter"], len(column_type_guess), escapechar=dialect["escapechar"]
            )

        for i, name in enumerate(_column_names):
            columns.append(
                {
                    "name": name,
                    "normalized_name": normalize_column_name(name),
                    "type": column_type_guess[i]["type"] if type_guessing else "String",
                    "nullable": column_type_guess[i]["nullable"],
                    "auto": False,
                }
            )
        if safe_types:
            columns = CSVInfo.convert_columns_to_safe_types(columns)

        extra_options = {}
        if dialect["delimiter"] in [" ", "\t"]:
            input_format = "CustomSeparated"
            extra_options["format_custom_field_delimiter"] = dialect["delimiter"]
            extra_options["format_custom_escaping_rule"] = "CSV"
        else:
            input_format = "CSV"

        if dialect["has_header"]:
            input_format = f"{input_format}WithNames"

        # This sync query is used just to collect some stats about the values in the columns. This is later used to
        # distinguish the column with more uniqueness in candidate_index_columns to choose which column should be the one
        # used for the hash. We sometimes want to avoid this. e.g. when processing the CSV header info of a CSV which
        # table has already been created.
        if not skip_stats_collection:
            try:
                stats = CHTable(columns, engine=engine_dict.get()).query(
                    data=csv_extract.encode(),
                    query=table_stats_sql("table", columns),
                    input_format=input_format,
                    dialect=dialect,
                    extra_options=extra_options,
                )
                assert isinstance(stats, Dict)
                st = group_by_column_postfix(stats["data"][0])
                for x in columns:
                    x["stats"] = dict(st.get(x["normalized_name"], []))
            except Exception as e:
                logging.warning(e)

        # read a few lines to include as a sample
        csv_stream.seek(0)
        sample_lines = csv_stream.readline()
        for _x in range(10):
            sample_lines += csv_stream.readline()

        return CSVInfo(columns, extract=sample_lines, dialect=dialect)


def table_structure(columns: List[Dict[str, Any]], include_auto: bool = False) -> str:
    columns = (
        list(filter(lambda column: "auto" not in column or not column["auto"], columns))
        if not include_auto
        else columns
    )
    return ", ".join(schema_to_sql_columns(columns))


_clickhouse_path = None


def get_processor_path() -> str:
    global _clickhouse_path
    if not _clickhouse_path:
        _clickhouse_path = shutil.which("clickhouse")
        if not _clickhouse_path:
            logging.critical("Could not find 'clickhouse' binary in the $PATH")
            exit(1)
    return _clickhouse_path


ERROR_COLUMNS = [
    {
        "name": "c__error_column",
        "normalized_name": "c__error_column",
        "type": "Array(String)",
        "nullable": False,
        "auto": False,
    },
    {
        "name": "c__error",
        "normalized_name": "c__error",
        "type": "Array(String)",
        "nullable": False,
        "auto": False,
    },
    {
        "name": "c__import_id",
        "normalized_name": "c__import_id",
        "type": "String",
        "nullable": True,
        "auto": False,
    },
]
ERROR_COLUMNS_NAMES = {x["name"] for x in ERROR_COLUMNS}
ERROR_COLUMNS_SORTED = sorted(ERROR_COLUMNS, key=lambda x: x["name"])  # type: ignore
ERROR_COLUMNS_SORTED_NAMES = [x["name"] for x in ERROR_COLUMNS_SORTED]
ERROR_COLUMNS_SORTED_TYPES = [x["type"] for x in ERROR_COLUMNS_SORTED]

FALLBACK_PARTITION_COLUMN = {
    "name": "insertion_date",
    "normalized_name": "insertion_date",
    "type": "DateTime DEFAULT now()",
    "auto": True,
    "nullable": False,
}


def all_nullable(columns: List[Dict[str, Any]]) -> bool:
    return next((x for x in columns if not x["nullable"] and x["name"] not in ERROR_COLUMNS_NAMES), None) is None


def partition(columns: List[Dict[str, Any]], default_date_partition: str = "toYear") -> Tuple[str, str]:
    """pick partition column and expression
    >>> partition([{ "name": "test", "normalized_name": "test", "type": "Date", "nullable": False}])
    ('test', 'toYear(`test`)')
    >>> partition([{ "name": "foo.bar", "normalized_name": "foo.bar", "type": "Date", "nullable": False}])
    ('foo.bar', 'toYear(`foo.bar`)')
    >>> columns = [{'name': 'c0', 'normalized_name': 'c0', 'type': 'String', 'nullable': True, 'auto': False}]
    >>> partition(columns)
    ('', '')
    >>> partition(columns + [FALLBACK_PARTITION_COLUMN])
    ('insertion_date', 'toYear(`insertion_date`)')
    >>> partition(columns + ERROR_COLUMNS)
    ('', '')
    >>> partition(ERROR_COLUMNS + columns + [FALLBACK_PARTITION_COLUMN])  # test changing the order
    ('insertion_date', 'toYear(`insertion_date`)')
    >>> partition([{ "name": "c", "normalized_name": "c", "type": "String", "nullable": False}])
    ('', '')
    >>> partition([{ "name": "u", "normalized_name": "u", "type": "UInt8", "nullable": False}])
    ('', '')
    >>> partition([{ "name": "foo.bar", "normalized_name": "foo.bar", "type": "String", "nullable": False}])
    ('', '')
    >>> partition([{ "name": "u.i", "normalized_name": "u.i", "type": "UInt8", "nullable": False}])
    ('', '')
    >>> partition([{ "name": "foo.bar", "normalized_name": "foo.bar", "type": "Array(String)", "nullable": False}, { "name": "u", "normalized_name": "u", "type": "UInt8", "nullable": False}])
    ('', '')
    """
    # pick date or datetime column first.
    column: str = next(
        (
            x["normalized_name"]
            for x in columns
            if x["type"].startswith("Date") and not x["nullable"] and x["name"] not in ERROR_COLUMNS_NAMES
        ),
        "",
    )
    expression: str = f"{default_date_partition}(`{column}`)" if column else ""
    return column, expression


def choose_index_columns(columns: List[Dict[str, Any]]) -> Optional[List[str]]:
    """pick candidate index columns using the column with the most flat probability distribution
    >>> choose_index_columns([{'name': 'c0', 'normalized_name': 'c0', 'type': 'String', 'nullable': True, 'auto': False}]) is None
    True
    >>> choose_index_columns([{'name': 'c0', 'normalized_name': 'c0', 'type': 'String', 'nullable': False, 'auto': False}] + ERROR_COLUMNS)
    ['c0']
    """
    result: List[str] = []
    elegible_columns = [
        x
        for x in columns
        if (
            not x["nullable"]
            and (x["type"] == "String" or "Int" in x["type"])
            and x["name"] not in ERROR_COLUMNS_NAMES
            and not x["type"].startswith("Array(")
        )
    ]

    # let's try with some float column
    if not elegible_columns:
        elegible_columns = [
            x
            for x in columns
            if (
                not x["nullable"]
                and ("Float" in x["type"])
                and x["name"] not in ERROR_COLUMNS_NAMES
                and not x["type"].startswith("Array(")
            )
        ]

    if elegible_columns:
        elegible_columns = sorted(elegible_columns, key=lambda s: s["stats"].get("uniq", 0) if "stats" in s else 0)
        number_of_columns = min(len(elegible_columns), 3)  # up to three columns with the more unique values
        subset = elegible_columns[-number_of_columns:]
        for c in subset:
            result.append(c["normalized_name"])

    return result if len(result) else None


VALID_COLUMN_NAME_RE = r"^[a-zA-Z_][\.0-9a-zA-Z_]*$"
RESERVED_KEYWORDS = {"index"}


class CHTable:
    """contains information for a clickhouse table"""

    def __init__(
        self,
        columns: List[Dict[str, Any]],
        cluster: Optional[str] = None,
        engine: Optional[Any] = None,
        not_exists: Optional[bool] = False,
        as_table: str = "",
        default_date_partition: str = "toYear",
        add_fallback_partition_column: bool = False,
        storage_policy: Optional[str] = None,
        indexes: Optional[List[TableIndex]] = None,
        projections: Optional[List[TableProjection]] = None,
        disk_settings: Optional[dict[str, Any]] = None,
    ):
        """
        >>> random = {'name': 'random', 'normalized_name': 'random', 'type': 'String', 'nullable': True, 'auto': False }
        >>> columns = [random]

        >>> t = CHTable(columns)
        >>> t.columns == [random]
        True
        >>> t.candidate_index_columns

        >>> t.partition_column
        ''
        >>> t.partition_expr
        ''
        >>> t.engine
        'MergeTree() ORDER BY (tuple())'

        >>> CHTable([{'name': 'index', 'normalized_name': 'index', 'type': 'String', 'nullable': True, 'auto': False }])
        Traceback (most recent call last):
        ...
        ValueError: Invalid column name 'index' at position 1, 'index' is a reserved keyword
        >>> col = {'name': 'c1', 'normalized_name': 'c1', 'type': 'String', 'nullable': True, 'auto': False }
        >>> CHTable([col, col])
        Traceback (most recent call last):
        ...
        ValueError: Column with name 'c1' is duplicated at positions 1 and 2
        >>> CHTable([{'name': '1col', 'normalized_name': '1col', 'type': 'String', 'nullable': True, 'auto': False }])
        Traceback (most recent call last):
        ...
        ValueError: Column '1col' should have an alias and start by a character. Change the query and try it again.

        >>> CHTable([{'name': '1', 'normalized_name': '1', 'type': 'String', 'nullable': True, 'auto': False }])
        Traceback (most recent call last):
        ...
        ValueError: Column '1' should have an alias and start by a character. Change the query and try it again.
        """
        self.columns = columns[:]  # clone original columns
        self._check_columns(columns)

        if disk_settings and storage_policy:
            raise ValueError("disk_settings and storage_policy cannot be used together")

        self.cluster = cluster
        self.engine = None
        self.not_exists = not_exists
        self.partition_column: Optional[str] = None
        self.partition_expr: Optional[str] = None
        self.candidate_index_columns = None
        self.as_table = as_table
        self.storage_policy = storage_policy
        self.indexes = indexes
        self.projections = projections
        self.disk_settings: Optional[Dict[str, Any]] = disk_settings
        self.default_date_partition = default_date_partition
        self.add_fallback_partition_column = add_fallback_partition_column
        self.fallback_partition_column_name = self._get_fallback_partition_column_name()

        if self.as_table:
            if len(self.columns) != 0:
                raise ValueError("Improper use of CHTable. You can't pass both column definition and as_table")
            if not engine or not isinstance(engine, str):
                raise ValueError("Improper use of CHTable. You need to pass engine definition with as_table")

        if isinstance(engine, str):
            self.engine = engine
        elif not self.as_table:
            self._partition()
            engine = engine or {}

            self.candidate_index_columns = choose_index_columns(self.columns)
            # we are actively working on deprecating this, we keep it for now to avoid breaking changes
            # for those data sources that already use it, once this is done, we can move this logic to QuaratineCHTable
            add_fallback_column = self.add_fallback_partition_column and (
                (not self.partition_expr and all_nullable(self.columns))
                or (not self.partition_column and not self.candidate_index_columns)
            )

            keep_fallback_column = self.fallback_partition_column_name in engine.get(
                "sorting_key", ""
            ) or self.fallback_partition_column_name in engine.get("partition_key", "")
            no_existing_fallback_column = not any(
                x["normalized_name"] == self.fallback_partition_column_name for x in self.columns
            )
            if no_existing_fallback_column and (add_fallback_column or keep_fallback_column):
                fallback_partition_column = FALLBACK_PARTITION_COLUMN.copy()
                fallback_partition_column["name"] = self.fallback_partition_column_name
                fallback_partition_column["normalized_name"] = self.fallback_partition_column_name

                self.columns.append(fallback_partition_column)
                self.partition_column = self.fallback_partition_column_name
                self.partition_expr = f"toYear(`{self.fallback_partition_column_name}`)"
                self.candidate_index_columns = [self.fallback_partition_column_name]
            self.engine = self._engine(engine)

    def _get_fallback_partition_column_name(self) -> str:
        return str(FALLBACK_PARTITION_COLUMN["name"])

    def _check_columns(self, columns_to_check: List[Dict[str, Any]]) -> Dict[str, int]:
        columns = columns_to_check[:]  # clone original columns
        unique_columns: Dict[str, int] = {}

        for i, c in enumerate(columns):
            normalized_name = c["normalized_name"]
            if normalized_name in RESERVED_KEYWORDS:
                raise ValueError(
                    f"Invalid column name '{c['name']}' at position {i+1}, '{normalized_name}' is a reserved keyword"
                )
            if not re.match(VALID_COLUMN_NAME_RE, normalized_name):
                if "(" in c["name"]:
                    column_name = c["name"]
                    column_name_suggestion = normalize_column_name_suggestion(column_name)
                    raise ValueError(
                        f"Column '{c['name']}' should have an alias. Change the query and try it again. i.e: {c['name']} {column_name_suggestion}"
                    )
                raise ValueError(
                    f"Column '{c['name']}' should have an alias and start by a character. Change the query and try it again."
                )
            if normalized_name in unique_columns:
                position = unique_columns[normalized_name]
                raise ValueError(f"Column with name '{c['name']}' is duplicated at positions {position} and {i+1}")
            unique_columns[normalized_name] = i + 1

        return unique_columns

    def _partition(self) -> None:
        self.partition_column, self.partition_expr = partition(
            self.columns, default_date_partition=self.default_date_partition
        )

    def _engine(self, engine_dict: Dict[str, Any]) -> str:
        self.index_columns = self._get_index_columns()
        engine_dict = self.get_engine_settings(engine_dict)
        engine_type = engine_dict.pop("type", engine_dict.pop("engine", "MergeTree"))
        return engine_full_from_dict(engine_type, engine_dict, columns=self.columns)

    def _get_index_columns(self) -> List[str]:
        index_columns = []
        if self.partition_column and self.partition_expr:
            index_columns = [self.partition_column]
        if self.candidate_index_columns:
            index_columns += self.candidate_index_columns
        # this is to remove duplicates from index_columns while preserving the order
        return list(dict.fromkeys(index_columns))

    def get_engine_settings(self, engine_dict: Dict[str, Any]) -> Dict[str, Any]:
        return {"sorting_key": ", ".join(self.index_columns), "partition_key": self.partition_expr, **engine_dict}

    def cluster_clause(self) -> str:
        return f"ON CLUSTER {self.cluster}" if self.cluster else ""

    def database_engine(self, engine: Optional[str], database: str, table_name: str) -> Optional[str]:
        if self.cluster and engine_can_be_replicated(engine) and engine:
            return engine_local_to_replicated(engine, database, table_name)
        return engine

    def as_sql(
        self, database: str, table_name: str, skip_validation: bool = False, create_or_replace: Optional[bool] = False
    ) -> str:
        indices_clause = ""
        if self.indexes:
            indices_clause = ",\n" + ",\n".join([index.to_sql() for index in self.indexes])

        projections_clause = ""
        if self.projections:
            projections_clause = ",\n" + ",\n".join([projection.to_sql() for projection in self.projections])

        original_query = """
        CREATE TABLE {or_replace} {not_exists} {database}.{table_name} {cluster_clause}
        {columns_clause}
        ENGINE = {engine}""".format(
            database=database,
            table_name=table_name,
            or_replace="OR REPLACE" if create_or_replace else "",
            not_exists="IF NOT EXISTS" if self.not_exists else "",
            columns_clause=(
                "(" + ",\n".join(schema_to_sql_columns(self.columns)) + indices_clause + projections_clause + ")"
                if self.columns
                else f"AS {self.as_table}"
            ),
            cluster_clause=self.cluster_clause(),
            engine=self.database_engine(self.engine, database, table_name),
        )
        # If you find this code while trying to push odd table settings, please revisit what you are doing
        # The engine shall not contain any blocked settings and you shouldn't pass skip_validation unless you are 100%
        # sure the settings don't come from external sources
        # Currently the only good reason to have this option to skip validation is because we sometimes (and against
        # the CH team advice) change settings directly in ClickHouse and we want to maintain them when we copy DS
        # That's why skip_validation is possible if you are copying a table (self.as_table)
        #
        # In the future, once 21.9 is not supported, we should be able to remove the engine completely when doing
        # a copy from a table since `CREATE TABLE x AS z` works (no columns, no engine). It might need tweaks for
        # replication. When this happens, then we can remove this exception and always force validation
        if skip_validation and not self.as_table:
            raise Exception("skip_validation can only be used to copy tables")
        parsed_query = check_valid_write_query(original_query, validate_table_settings=not skip_validation)

        # We need to manually add the storage policy after validation as the validation is meant to block external usage
        # of settings like this one

        if self.storage_policy and self.engine and "MergeTree" in self.engine:
            parsed_query = add_settings(parsed_query, "storage_policy", f"'{self.storage_policy}'")
        elif self.disk_settings:
            parsed_query = add_settings(parsed_query, "disk", format_disk_settings(self.disk_settings))

        return parsed_query

    def table_structure(self) -> str:
        return table_structure(self.columns)

    def _prepare_query_command(
        self, clickhouse_bin_path, data, file, query, input_format, output_format, dialect, extra_options
    ):
        if data is not None:
            file.write(data)
            file.flush()
            os.fsync(file.fileno())

        if "`table`" in query:
            t = "`table`"
        else:
            t = "table"

        structure = self.table_structure().replace("'", r"\'")
        sql = re.sub(rf"from\s+{t}", "from file('%s', '%s', '%s')" % (file.name, input_format, structure), query)
        logging.debug(sql)

        # transform map to a list of cmd line options
        options = []
        for k, v in extra_options.items():
            options.append(f"--{k}")
            options.append(v)

        command = [  # noqa: RUF005
            clickhouse_bin_path,
            "local",
            "-q",
            sql,
            "--format",
            output_format,
            "--input_format_defaults_for_omitted_fields",
            "1",
            "--format_csv_delimiter",
            "," if not dialect else dialect.get("delimiter", ","),
            "--date_time_input_format",
            "best_effort",
            "--format_csv_allow_single_quotes",
            "1",  # Changed default in CH 22.7
        ] + options

        return command

    def _parse_query_output(self, command, output_format, process, stdout, stderr):
        if process.returncode != 0:
            logging.info(f"ClickHouse local failed {process.returncode}. Command " + str(command))
            if stderr:
                msg = stderr.decode("utf-8", "surrogateescape")
                logging.info(f"ClickHouse local returned error: {msg}")
                if "Exception" in msg:
                    raise Exception(msg)
            else:
                logging.warning("ClickHouse local EMPTY stderr")
            raise Exception(f"CH return code: {process.returncode}")
        if output_format == "JSON":
            return json.loads(stdout.decode())
        return stdout

    def query(
        self,
        *,
        query: str,
        data: Optional[bytes] = None,
        input_format: str = "CSV",
        output_format: str = "JSON",
        dialect=None,
        extra_options: Optional[Dict] = None,
        timeout=60,
    ) -> Union[bytes, Dict[str, Any]]:
        extra_options = {} if extra_options is None else extra_options
        clickhouse_bin_path = get_processor_path()
        logging.debug(f"static data query: {query}")
        logging.debug(f"input format: {input_format}")

        Path("/tmp/tinybird/query").mkdir(parents=True, exist_ok=True)

        # instead of sending data with communicate write to a temporary file (5x faster)
        with tempfile.NamedTemporaryFile(mode="wb", delete=False, prefix="data_", dir="/tmp/tinybird/query") as f:
            try:
                command = self._prepare_query_command(
                    clickhouse_bin_path=clickhouse_bin_path,
                    data=data,
                    file=f,
                    query=query,
                    input_format=input_format,
                    output_format=output_format,
                    dialect=dialect,
                    extra_options=extra_options,
                )

                env = os.environ.copy()
                env["TZ"] = "UTC"

                # cwd changed since CH local can't work on non existing paths (which can happen when running CLI tests)
                with subprocess.Popen(
                    command,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd="/tmp",
                    env=env,
                ) as p:
                    try:
                        # This tries to mitigate the problem found in https://gitlab.com/tinybird/analytics/-/issues/1250
                        # which relates to https://bugs.python.org/issue23213
                        stdout, stderr = p.communicate(timeout=timeout)
                    except subprocess.TimeoutExpired:
                        logging.warning("Stuck ClickHouse local: KILL")
                        p.kill()
                        stdout, stderr = p.communicate()

                    stdout = self._parse_query_output(
                        command=command, output_format=output_format, process=p, stdout=stdout, stderr=stderr
                    )
            finally:
                os.unlink(f.name)

        return stdout

    async def query_async(
        self,
        *,
        query: str,
        data: Optional[bytes] = None,
        input_format: str = "CSV",
        output_format: str = "JSON",
        dialect=None,
        extra_options: Optional[Dict] = None,
        timeout=60,
    ) -> Union[bytes, Dict[str, Any]]:
        extra_options = {} if extra_options is None else extra_options
        clickhouse_bin_path = get_processor_path()
        logging.debug(f"static data query: {query}")
        logging.debug(f"input format: {input_format}")

        Path("/tmp/tinybird/query").mkdir(parents=True, exist_ok=True)

        # instead of sending data with communicate, write to a temporary file (5x faster)
        with tempfile.NamedTemporaryFile(mode="wb", delete=False, prefix="data_", dir="/tmp/tinybird/query") as f:
            try:
                command = self._prepare_query_command(
                    clickhouse_bin_path=clickhouse_bin_path,
                    data=data,
                    file=f,
                    query=query,
                    input_format=input_format,
                    output_format=output_format,
                    dialect=dialect,
                    extra_options=extra_options,
                )

                env = os.environ.copy()
                env["TZ"] = "UTC"

                # cwd changed since CH local can't work on non existing paths (which can happen when running CLI tests)
                p = await asyncio.create_subprocess_exec(
                    *command,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd="/tmp",
                    env=env,
                )

                try:
                    stdout, stderr = await asyncio.wait_for(p.communicate(), timeout=timeout)
                except asyncio.TimeoutError:
                    p.terminate()
                    raise

                stdout = self._parse_query_output(
                    command=command, output_format=output_format, process=p, stdout=stdout, stderr=stderr
                )
            finally:
                os.unlink(f.name)

        return stdout


class QuarantineCHTable(CHTable):
    def __init__(self, columns: List[Dict[str, Any]], **kwargs):
        """
        >>> c0 = {'name': 'c0', 'normalized_name': 'c0', 'type': 'String', 'nullable': True, 'auto': False }
        >>> columns = [c0]

        >>> t = QuarantineCHTable(columns)
        >>> t.columns == [c0, FALLBACK_PARTITION_COLUMN]
        True
        >>> t.candidate_index_columns
        ['insertion_date']

        >>> t = QuarantineCHTable(columns + ERROR_COLUMNS)
        >>> t.columns == columns + ERROR_COLUMNS + [FALLBACK_PARTITION_COLUMN]
        True
        >>> t.candidate_index_columns
        ['insertion_date']


        >>> t = QuarantineCHTable(ERROR_COLUMNS + columns)  # test changing the order
        >>> t.columns == ERROR_COLUMNS + [c0, FALLBACK_PARTITION_COLUMN]
        True
        >>> t.partition_column
        'insertion_date'
        >>> t.partition_expr
        'toYear(`insertion_date`)'
        >>> t.candidate_index_columns
        ['insertion_date']
        """
        self.add_fallback_partition_column = True
        super().__init__(columns, add_fallback_partition_column=self.add_fallback_partition_column, **kwargs)

    def _get_fallback_partition_column_name(self) -> str:
        column_names = [x["name"] for x in self.columns]
        return get_fallback_partition_column_name(column_names)


def add_settings(query: str, setting_name: str, setting_value: str) -> str:
    if " SETTINGS " in query:
        return query.replace(" SETTINGS ", f" SETTINGS {setting_name}={setting_value}, ")
    return query + f" SETTINGS {setting_name}={setting_value}"


def format_disk_settings(disk_settings: dict[str, Any]) -> str:
    formatted_disk_settings = "disk("
    required_settings = ["type", "endpoint", "access_key_id", "secret_access_key"]
    for setting in required_settings:
        if setting not in disk_settings:
            raise ValueError(f"Missing required disk setting: {setting}")

    formatted_disk_settings += f"type='{disk_settings['type']}', "
    formatted_disk_settings += f"endpoint='{disk_settings['endpoint']}', "
    formatted_disk_settings += f"access_key_id='{disk_settings['access_key_id']}', "
    formatted_disk_settings += f"secret_access_key='{disk_settings['secret_access_key']}'"
    return formatted_disk_settings + ")"


def group_by_column_postfix(res: Dict[str, Any]):
    """utility function that returns a dictionary with keys when column names have column names
    group_by_column_postfix(query('select avg(test) test__avg, max(test) test__max'))

    {
        'test': {
            'max': 123,
            'avg': 2
        }

    }
    >>> group_by_column_postfix({'test__avg': 0, 'test__max': 1, 'test__rambo__avg': 2, 'test__rambo__max': 3})
    defaultdict(<class 'list'>, {'test': [('avg', 0), ('max', 1)], 'test__rambo': [('avg', 2), ('max', 3)]})
    """
    st = defaultdict(list)
    for (c, fn), value in [(k.rsplit("__", 1), v) for k, v in res.items()]:
        st[c].append((fn, value))
    return st


def table_stats_sql(table_name: str, columns: List[Dict[str, Any]], extended: bool = False) -> str:
    stats = []
    for c in columns:
        _type = c["type"]
        column = c["normalized_name"]
        if _type == "String" or "UInt" in _type or "Int" in _type:
            stats.append("toUInt32(uniqCombined(`%s`)) as `%s__uniq`" % (column, column))
            if extended:
                stats.append("topK(10)(`%s`) as `%s__topk`" % (column, column))
        if ("Float" in _type or "UInt" in _type or "Int" in _type) and "Array" not in _type:
            stats.append("quantilesTDigest(0, 0.25, 0.5, 0.75, 1)(`%s`) as `%s__quantiles`" % (column, column))
            if extended:
                stats.append("avg(`%s`) as `%s__avg`" % (column, column))
                stats.append("min(`%s`) as `%s__min`" % (column, column))
                stats.append("max(`%s`) as `%s__max`" % (column, column))
                # stats.append('histogram(10)(`%s`) as `%s___hist`' % (column, column))

    sql = "select %s from `%s`" % (",".join(stats), table_name)
    return sql


def _parse_column(column: Dict[str, Any]) -> Dict[str, Any]:
    RESERVED_COLUMNS = ["insertion_date"]
    nullable = column["type"].startswith("Nullable")
    t = column["type"] if not nullable else column["type"][len("Nullable(") : -1]  # ')'
    default_value: Optional[str] = f"{column.get('default_type', '')} {column.get('default_expression', '')}"
    default_value = None if default_value in (" ", "DEFAULT NULL") else default_value
    if (codec_expression := column.get("codec_expression", None)) and "CODEC" not in codec_expression:
        codec_expression = f"CODEC({codec_expression})"
    return {
        "name": column["name"],
        "normalized_name": column["name"],
        "codec": codec_expression or None,
        "type": t,
        "nullable": nullable,
        "auto": column["name"] in RESERVED_COLUMNS,
        "default_value": default_value,
    }


def parse_schema(
    body: bytes, include_default_columns: bool = False, attr: str = "data", include_meta_columns: bool = True
) -> List[Dict[str, Any]]:
    columns: List[Dict[str, Any]] = []
    schema = json.loads(body)[attr]

    kafka_checker_columns = ["__value", "__topic", "__partition", "__offset", "__timestamp", "__key"]

    column_names = [c["name"] for c in schema]

    meta_columns = set()
    is_kafka = all([c in column_names for c in kafka_checker_columns])
    if is_kafka:
        meta_columns = KAFKA_META_COLUMNS
    is_dynamodb = all([c in column_names for c in DYNAMODB_META_COLUMNS])
    if is_dynamodb:
        meta_columns = DYNAMODB_META_COLUMNS

    for column in schema:
        if not include_meta_columns and column["name"] in meta_columns:
            continue
        c = _parse_column(column)
        if column.get("default_type", "").lower() == "materialized":
            if include_default_columns:
                columns.append(c)
        else:
            columns.append(c)
    if not columns and is_kafka and "__value" in column_names:
        for column in schema:
            if column["name"] == "__value":
                c = _parse_column(column)
                columns.append(c)
    return columns


def _parse_schemas(body: bytes, include_default_columns: bool = False, attr: str = "data") -> List[Dict[str, Any]]:
    columns: List[Dict[str, Any]] = []
    schema = json.loads(body)[attr]

    for column in schema:
        c = _parse_column(column)
        c.update({"table": column["table"], "database": column["database"]})
        if column.get("default_type", "").lower() == "materialized":
            if include_default_columns:
                columns.append(c)
        else:
            columns.append(c)
    return columns


def create_table_query_to_engine_advanced(create_table_query: str, clean_settings: bool = True) -> Tuple[str, str, str]:
    """Extracts info from create_table_query. Removes unsupported settings
    >>> create_table_query_to_engine_advanced("CREATE TABLE big_table (`number` Int64) ENGINE = MergeTree ORDER BY tuple() SETTINGS merge_with_ttl_timeout = 43200")
    ('MergeTree ORDER BY tuple() SETTINGS merge_with_ttl_timeout = 43200', 'merge_with_ttl_timeout = 43200', '')
    >>> create_table_query_to_engine_advanced("CREATE TABLE default.materializations_log (`event_time` DateTime, `host` String, `initial_query_id` String, `view_name` String, `view_target` String, `view_duration_ms` UInt64, `read_rows` UInt64, `read_bytes` UInt64, `written_rows` UInt64, `written_bytes` UInt64, `peak_memory_usage` Int64, `exception_code` Int32, `exception` String) ENGINE = ReplicatedMergeTree('/clickhouse/tables/{layer}-{shard}/default.materializations_log', '{replica}') ORDER BY (initial_query_id, event_time) TTL event_time + toIntervalHour(8) SETTINGS index_granularity = 8192")
    ("ReplicatedMergeTree('/clickhouse/tables/{layer}-{shard}/default.materializations_log', '{replica}') ORDER BY (initial_query_id, event_time) TTL event_time + toIntervalHour(8) SETTINGS index_granularity = 8192", 'index_granularity = 8192', 'event_time + toIntervalHour(8)')
    >>> create_table_query_to_engine_advanced("CREATE TABLE t (`number` Int64) ENGINE = MergeTree ORDER BY tuple() SETTINGS storage_policy = 's3' ")
    ('MergeTree ORDER BY tuple()', '', '')
    >>> create_table_query_to_engine_advanced("CREATE TABLE d.t (`a` Int32) ENGINE = MergeTree ORDER BY a SETTINGS storage_policy = 'lower_max_size', merge_with_ttl_timeout = 45200")
    ('MergeTree ORDER BY a SETTINGS merge_with_ttl_timeout = 45200', 'merge_with_ttl_timeout = 45200', '')
    >>> create_table_query_to_engine_advanced("CREATE TABLE d.t (`a` Int32) ENGINE = MergeTree ORDER BY a SETTINGS merge_with_ttl_timeout = 45200, storage_policy = 'lower_max_size', index_granularity = 1")
    ('MergeTree ORDER BY a SETTINGS merge_with_ttl_timeout = 45200', 'merge_with_ttl_timeout = 45200', '')
    >>> create_table_query_to_engine_advanced("CREATE TABLE d.t (`a` Int32) ENGINE = MergeTree ORDER BY a SETTINGS storage_policy = 'lower_max_size', merge_with_ttl_timeout = 45200", clean_settings=False)
    ("MergeTree ORDER BY a SETTINGS storage_policy = 'lower_max_size', merge_with_ttl_timeout = 45200", "storage_policy = 'lower_max_size', merge_with_ttl_timeout = 45200", '')
    >>> create_table_query_to_engine_advanced("CREATE TABLE d.t (`a` Int32) ENGINE = MergeTree ORDER BY a SETTINGS merge_with_ttl_timeout = 45200, storage_policy = 'lower_max_size', index_granularity = 1", clean_settings=False)
    ("MergeTree ORDER BY a SETTINGS merge_with_ttl_timeout = 45200, storage_policy = 'lower_max_size', index_granularity = 1", "merge_with_ttl_timeout = 45200, storage_policy = 'lower_max_size', index_granularity = 1", '')
    >>> create_table_query_to_engine_advanced("CREATE TABLE d_03d680.t_ea9e3e784ef149caa1fcd5d772e61c42 (`snapshot_id` DateTime, `EVENT_DATE` DateTime64(3), `EVENT_PK` String, `FECHA_MODIFICACION` String, `ID_LOCALIZACION` Int32, `ID_INSTALACION_RFID` Int32, `UBICACION_RFID` Int16, `COD_PRODUCTO_AS400` Int16, `MODELO` Int32, `CALIDAD` Int32, `COLOR` Int32, `TALLA` Int16, `OP` String, `UNIDADES` Int32) ENGINE = ReplicatedMergeTree('/clickhouse/tables/{layer}-{shard}/d_03d680.t_ea9e3e784ef149caa1fcd5d772e61c42', '{replica}') PARTITION BY toStartOfHour(snapshot_id) ORDER BY (snapshot_id, ID_LOCALIZACION, ID_INSTALACION_RFID, COD_PRODUCTO_AS400, MODELO, CALIDAD, COLOR, TALLA, UBICACION_RFID) TTL snapshot_id + toIntervalHour(1) SETTINGS index_granularity = 8192, ttl_only_drop_parts = 1, merge_with_ttl_timeout = 1800", clean_settings=True)
    ("ReplicatedMergeTree('/clickhouse/tables/{layer}-{shard}/d_03d680.t_ea9e3e784ef149caa1fcd5d772e61c42', '{replica}') PARTITION BY toStartOfHour(snapshot_id) ORDER BY (snapshot_id, ID_LOCALIZACION, ID_INSTALACION_RFID, COD_PRODUCTO_AS400, MODELO, CALIDAD, COLOR, TALLA, UBICACION_RFID) TTL snapshot_id + toIntervalHour(1) SETTINGS index_granularity = 8192, ttl_only_drop_parts = 1, merge_with_ttl_timeout = 1800", 'index_granularity = 8192, ttl_only_drop_parts = 1, merge_with_ttl_timeout = 1800', 'snapshot_id + toIntervalHour(1)')
    >>> create_table_query_to_engine_advanced("CREATE TABLE d_03d680.t_ea9e3e784ef149caa1fcd5d772e61c42 (`snapshot_id` DateTime, `EVENT_DATE` DateTime64(3), `EVENT_PK` String, `FECHA_MODIFICACION` String, `ID_LOCALIZACION` Int32, `ID_INSTALACION_RFID` Int32, `UBICACION_RFID` Int16, `COD_PRODUCTO_AS400` Int16, `MODELO` Int32, `CALIDAD` Int32, `COLOR` Int32, `TALLA` Int16, `OP` String, `UNIDADES` Int32) ENGINE = ReplicatedMergeTree('/clickhouse/tables/{layer}-{shard}/d_03d680.t_ea9e3e784ef149caa1fcd5d772e61c42', '{replica}') PARTITION BY toStartOfHour(snapshot_id) ORDER BY (snapshot_id, ID_LOCALIZACION, ID_INSTALACION_RFID, COD_PRODUCTO_AS400, MODELO, CALIDAD, COLOR, TALLA, UBICACION_RFID) TTL snapshot_id + toIntervalHour(1) SETTINGS index_granularity = 8192, ttl_only_drop_parts = 1, merge_with_ttl_timeout = 1800", clean_settings=False)
    ("ReplicatedMergeTree('/clickhouse/tables/{layer}-{shard}/d_03d680.t_ea9e3e784ef149caa1fcd5d772e61c42', '{replica}') PARTITION BY toStartOfHour(snapshot_id) ORDER BY (snapshot_id, ID_LOCALIZACION, ID_INSTALACION_RFID, COD_PRODUCTO_AS400, MODELO, CALIDAD, COLOR, TALLA, UBICACION_RFID) TTL snapshot_id + toIntervalHour(1) SETTINGS index_granularity = 8192, ttl_only_drop_parts = 1, merge_with_ttl_timeout = 1800", 'index_granularity = 8192, ttl_only_drop_parts = 1, merge_with_ttl_timeout = 1800', 'snapshot_id + toIntervalHour(1)')
    >>> create_table_query_to_engine_advanced("CREATE TABLE d_03d680.t_9ffe6f6790be4fae908685d3da4ee6f1 (`snapshot_id` DateTime, `COD_PRODUCTO_AS400` Int16, `MODELO` Int32, `CALIDAD` Int32, `unidades` SimpleAggregateFunction(sum, Int64)) ENGINE = ReplicatedAggregatingMergeTree('/clickhouse/tables/{layer}-{shard}/d_03d680.t_9ffe6f6790be4fae908685d3da4ee6f1', '{replica}') PARTITION BY snapshot_id ORDER BY (snapshot_id, COD_PRODUCTO_AS400, MODELO, CALIDAD) TTL snapshot_id + toIntervalHour(1) SETTINGS index_granularity = 8192", clean_settings=True)
    ("ReplicatedAggregatingMergeTree('/clickhouse/tables/{layer}-{shard}/d_03d680.t_9ffe6f6790be4fae908685d3da4ee6f1', '{replica}') PARTITION BY snapshot_id ORDER BY (snapshot_id, COD_PRODUCTO_AS400, MODELO, CALIDAD) TTL snapshot_id + toIntervalHour(1) SETTINGS index_granularity = 8192", 'index_granularity = 8192', 'snapshot_id + toIntervalHour(1)')
    >>> create_table_query_to_engine_advanced("CREATE TABLE d_03d680.t_9ffe6f6790be4fae908685d3da4ee6f1 (`snapshot_id` DateTime, `COD_PRODUCTO_AS400` Int16, `MODELO` Int32, `CALIDAD` Int32, `unidades` SimpleAggregateFunction(sum, Int64)) ENGINE = ReplicatedAggregatingMergeTree('/clickhouse/tables/{layer}-{shard}/d_03d680.t_9ffe6f6790be4fae908685d3da4ee6f1', '{replica}') PARTITION BY snapshot_id ORDER BY (snapshot_id, COD_PRODUCTO_AS400, MODELO, CALIDAD) TTL snapshot_id + toIntervalHour(1) SETTINGS index_granularity = 8192", clean_settings=False)
    ("ReplicatedAggregatingMergeTree('/clickhouse/tables/{layer}-{shard}/d_03d680.t_9ffe6f6790be4fae908685d3da4ee6f1', '{replica}') PARTITION BY snapshot_id ORDER BY (snapshot_id, COD_PRODUCTO_AS400, MODELO, CALIDAD) TTL snapshot_id + toIntervalHour(1) SETTINGS index_granularity = 8192", 'index_granularity = 8192', 'snapshot_id + toIntervalHour(1)')
    >>> create_table_query_to_engine_advanced("CREATE TABLE d_3c7e8e.t_72be0d1ddd2d43119fac82bf5a51bd5c (`snapshot_id` DateTime, `event_date` DateTime64(3), `event_pk` Int16, `fecha_modificacion` DateTime, `id_localizacion` Int16, `id_instalacion_rfid` Int16, `ubicacion_rfid` Int16, `cod_producto_as400` Int16, `modelo` Int16, `calidad` Int16, `color` Int16, `talla` Int16, `op` String, `unidades` Int16) ENGINE = ReplicatedMergeTree('/clickhouse/tables/{layer}-{shard}/d_3c7e8e.t_72be0d1ddd2d43119fac82bf5a51bd5c', '{replica}') PARTITION BY toYear(snapshot_id) ORDER BY (snapshot_id, talla, op, unidades) TTL snapshot_id + toIntervalHour(1) SETTINGS index_granularity = 8192, ttl_only_drop_parts = 1, merge_with_ttl_timeout = 1800")
    ("ReplicatedMergeTree('/clickhouse/tables/{layer}-{shard}/d_3c7e8e.t_72be0d1ddd2d43119fac82bf5a51bd5c', '{replica}') PARTITION BY toYear(snapshot_id) ORDER BY (snapshot_id, talla, op, unidades) TTL snapshot_id + toIntervalHour(1) SETTINGS index_granularity = 8192, ttl_only_drop_parts = 1, merge_with_ttl_timeout = 1800", 'index_granularity = 8192, ttl_only_drop_parts = 1, merge_with_ttl_timeout = 1800', 'snapshot_id + toIntervalHour(1)')
    >>> create_table_query_to_engine_advanced("CREATE TABLE d_847c8c.t_2b218d63890047d5976c5f28a36656a0 (`projectId` String, `projectName` String, `projectRepo` String, `ownerId` String, `updatedAt` DateTime64(3)) ENGINE = ReplicatedReplacingMergeTree('/clickhouse/tables/{layer}-{shard}/d_847c8c.t_2b218d63890047d5976c5f28a36656a0', '{replica}', updatedAt) PARTITION BY tuple() PRIMARY KEY projectId ORDER BY projectId SETTINGS index_granularity = 32")
    ("ReplicatedReplacingMergeTree('/clickhouse/tables/{layer}-{shard}/d_847c8c.t_2b218d63890047d5976c5f28a36656a0', '{replica}', updatedAt) PARTITION BY tuple() PRIMARY KEY projectId ORDER BY projectId SETTINGS index_granularity = 32", 'index_granularity = 32', '')
    """

    try:
        if clean_settings:
            cleaned_table = chquery.check_valid_write_query(create_table_query, clean_table_settings=True)
            engine_full = cleaned_table.split(" ENGINE = ")[1]
        else:
            engine_full = create_table_query.split(" ENGINE = ")[1]
    except Exception as e:
        logging.exception(f"Failed to parse data from {create_table_query}: {str(e)}")
        return "", "", ""

    settings_array = engine_full.split(" SETTINGS ")
    cleaned_settings = settings_array[1] if len(settings_array) > 1 else ""
    ttl_array = engine_full.split(" TTL ")
    ttl = ttl_array[1][: -(len(cleaned_settings) + len(" SETTINGS "))] if len(ttl_array) > 1 else ""
    return engine_full, cleaned_settings, ttl


def _get_ch_table_details_query(datasources: List[Tuple[str, str]], include_stats: bool) -> str:
    # Instead of doing
    #       (database, name) IN {datasources}
    # We do:
    #   database in {databases} and table in {tables}
    # This second approach is much faster (say 3s vs 0.004s for the same tables for example)
    # This is not the same at SQL level (since you could get tables with the same name in different databases)
    # but it's ok for us since the table names are random and "should" not be duplicated

    databases = list(dict.fromkeys(ds[0] for ds in datasources if ds[0] is not None))
    tables = list(dict.fromkeys(ds[1] for ds in datasources if ds[1] is not None))
    table_condition = f"""
                   database in {tuple(databases)}
               AND name in {tuple(tables)}
               AND engine != 'View'
    """

    if not include_stats:
        return f"""
            SELECT
                database,
                name,
                create_table_query,
                engine,
                partition_key,
                sorting_key,
                primary_key,
                sampling_key
            FROM system.tables
            WHERE {table_condition}
            FORMAT JSON
        """

    return f"""
        SELECT
                database,
                name,
                create_table_query,
                engine,
                partition_key,
                sorting_key,
                primary_key,
                sampling_key,
                total_rows,
                total_bytes
            FROM system.tables t
            WHERE {table_condition}
            FORMAT JSON
        """


async def ch_table_details_async(
    table_name: str,
    database_server: str = "localhost",
    database: str = "default",
    include_stats: bool = False,
    clean_settings: bool = True,
    max_execution_time: Optional[int] = MAX_EXECUTION_TIME,
) -> TableDetails:
    client = HTTPClient(database_server, database=database)
    sql = _get_ch_table_details_query([(database, table_name)], include_stats)
    try:
        _, body = await client.query(sql, max_execution_time=max_execution_time)
    except CHException:
        return TableDetails(None)
    rows = json.loads(body).get("data", [])
    if not rows:
        return TableDetails(None)

    engine_full, settings, ttl = create_table_query_to_engine_advanced(
        rows[0]["create_table_query"], clean_settings=clean_settings
    )

    rows[0]["engine_full"] = engine_full
    rows[0]["settings"] = settings
    rows[0]["ttl"] = ttl

    return TableDetails(rows[0])


def ch_table_details(
    table_name: str,
    database_server: str = "localhost",
    database: str = "default",
    include_stats: bool = False,
    clean_settings: bool = True,
    user_agent: Optional[str] = None,
    query_settings: Optional[Dict[str, Any]] = None,
) -> TableDetails:
    query_settings = query_settings or {}
    client = HTTPClient(database_server, database=database)
    sql = _get_ch_table_details_query([(database, table_name)], include_stats)
    try:
        _, body = client.query_sync(sql, user_agent=user_agent, **query_settings)
    except CHException:
        return TableDetails(None)
    rows = json.loads(body).get("data", [])
    if not rows:
        return TableDetails(None)

    engine_full, settings, ttl = create_table_query_to_engine_advanced(
        rows[0]["create_table_query"], clean_settings=clean_settings
    )

    rows[0]["engine_full"] = engine_full
    rows[0]["settings"] = settings
    rows[0]["ttl"] = ttl

    return TableDetails(rows[0])


async def ch_many_tables_details_async(
    database_server: str, datasources: List[Tuple[str, str]], timeout: int = 10, include_stats: bool = False
) -> Dict[str, Dict[str, TableDetails]]:
    if not datasources:
        return {}
    client = HTTPClient(database_server, None)
    sql = _get_ch_table_details_query(datasources, include_stats)
    try:
        _, body = await client.query(sql, max_execution_time=timeout)
    except CHException as exc:
        logging.error(f"Error database_tables_details_async {exc}")
        return {}
    rows = json.loads(body).get("data", [])
    table_details: Dict[str, Dict[str, TableDetails]] = {}
    for row in rows:
        engine_full, settings, ttl = create_table_query_to_engine_advanced(
            row["create_table_query"], clean_settings=True
        )

        row["engine_full"] = engine_full
        row["settings"] = settings
        row["ttl"] = ttl

        if row["database"] not in table_details:
            table_details.update({row["database"]: {}})
        table_details[row["database"]].update({row["name"]: TableDetails(row)})
    return table_details


async def ch_storage_policies(database: str, database_server: str) -> List[Dict[str, Any]]:
    sql = """
        SELECT *
        FROM system.storage_policies
        FORMAT JSON
    """

    client = HTTPClient(database_server, database=database)
    _, result = await client.query(sql)
    return json.loads(result).get("data", [])


def ch_table_partitions_for_sample_sync(
    database_server: str, database: str, table_name: str, sample_percentage: float = 0.1, max_rows: int = 2000000
) -> List[Tuple[str, int]]:
    # this query returns an array of tuples (partition, _limit)
    # partition is the key of the partition and limit the number of rows to populate from each partition to reach the sample_percentage
    # it sorts partitions by modification time so you populate most recent data
    # it return all the partitions until reach `least(ceil(sum(rows) * {sample_percentage}), {max_rows}) as total_rows`, the last partition returned has a "_limit" of total_rows - partition_rows to match the sample_percentage
    sql = f"""
            SELECT
                partition,
                min(_limit) _limit
            FROM (
                WITH (
                    SELECT least(ceil(sum(rows) * {sample_percentage}), {max_rows})
                    FROM system.parts
                    WHERE
                        database = '{database}'
                        AND table = '{table_name}'
                        AND active
                ) as total_rows
                SELECT
                    partitions partition,
                    if (acc_rows <= total_rows, toInt64(_rows), toInt64(total_rows - acc_rows + _rows)) _limit
                FROM (
                        SELECT
                            arrayCumSum(groupArray(rows)) acc_rows,
                            groupArray(rows) _rows,
                            groupArray(partition) partitions
                    FROM (
                        SELECT
                            sum(rows) rows,
                            partition
                        FROM system.parts
                        WHERE
                            database = '{database}'
                            AND table = '{table_name}'
                            AND active
                        GROUP BY partition ORDER BY partition DESC
                    )
                )
                ARRAY JOIN acc_rows, partitions, _rows
                WHERE _limit <= total_rows AND _limit > 0
            )
            GROUP BY partition
            FORMAT JSON
    """

    client = HTTPClient(database_server, database=database)
    _, result = client.query_sync(sql)
    table_partitions = json.loads(result).get("data", [])
    partitions = list(sorted(set([(p["partition"], p["_limit"]) for p in table_partitions])))

    table_details = ch_table_details(table_name, database_server, database)

    partition_key = table_details.partition_key
    if not partition_key or partition_key in ["tuple()", ""]:
        return partitions

    partition_type_sql = f"DESCRIBE (SELECT {partition_key} as partition_key FROM {database}.{table_name}) FORMAT JSON"
    _, result = client.query_sync(partition_type_sql)
    meta = json.loads(result).get("data", [{}])
    partition_key_type = meta[0].get("type", None)
    # we need to check basic types and also types like 'DateTime(UTC/...)'
    if __needs_quote(partition_key_type):
        partitions = [(f"'{p[0]}'", p[1]) for p in partitions]

    return partitions


async def ch_last_update_kafka_ops_log_async(
    database_server: str, database: str, user_id: str, table_name: str
) -> Optional[str]:
    sql = f"""
        SELECT
            max(timestamp) timestamp
        FROM kafka_ops_log
        WHERE
            datasource_id = '{table_name}' AND
            user_id = '{user_id}' AND
            committed_messages > 0
        FORMAT JSON
        """
    try:
        client = HTTPClient(database_server, database=database)
        _, body = await client.query(sql, max_execution_time=1)
        data = json.loads(body)["data"]
        if len(data):
            return data[0]["timestamp"]
        return None
    except Exception:
        return None


async def ch_get_columns_from_query(
    database_server: str,
    database: str,
    sql: str,
    max_execution_time: Optional[int] = MAX_EXECUTION_TIME,
    ch_params: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    _, body = await ch_describe_query(
        database_server,
        database,
        sql,
        format="JSON",
        is_query=True,
        max_execution_time=max_execution_time,
        ch_params=ch_params,
    )
    return parse_schema(body, attr="data")


def ch_get_columns_from_query_sync(
    database_server: str, database: str, sql: str, ch_params: Optional[Dict[str, str]] = None
) -> List[Dict[str, Any]]:
    _, body = ch_describe_query_sync(database_server, database, sql, format="JSON", is_query=True, ch_params=ch_params)
    return parse_schema(body, attr="data")


async def ch_table_schema_async(
    table_name: str,
    database_server: str,
    database: str,
    include_default_columns: bool = False,
    include_meta_columns: bool = True,
    max_execution_time: Optional[int] = MAX_EXECUTION_TIME,
) -> Optional[List[Dict[str, Any]]]:
    try:
        _, body = await ch_describe_query(
            database_server, database, table_name, format="JSON", is_query=False, max_execution_time=max_execution_time
        )
    except CHException:
        return None
    return parse_schema(
        body,
        include_default_columns=include_default_columns,
        include_meta_columns=include_meta_columns,
    )


async def ch_databases_tables_schema_async(
    database_server: str, condition: str, include_default_columns: bool = False, timeout: int = 10
) -> List[Dict[str, str]]:
    client = HTTPClient(database_server, None)
    try:
        sql = f"""
        SELECT
            database,
            table,
            name,
            type,
            default_kind as default_type,
            default_expression,
            compression_codec as codec_expression
        FROM system.columns
        WHERE {condition}
        ORDER BY database, table, position
        FORMAT JSON
        """
        _, body = await client.query(sql, max_execution_time=timeout)
    except CHException:
        return []
    return _parse_schemas(body, include_default_columns)


async def ch_database_exists(server: str, database: str) -> bool:
    """Checks if a given database exists in a server"""
    query = f"EXISTS DATABASE `{database}` FORMAT JSON"

    try:
        client = HTTPClient(server)
        _, body = await client.query(query)
        body_json = json.loads(body)
        result = body_json["data"][0]["result"] if len(body_json["data"]) else 0
        return result > 0
    except Exception as e:
        logging.exception(f"Error while checking if database {database} exists @ {server}: {str(e)}")
        raise


def ch_table_exists_sync(table_name: str, server: str, database: str) -> bool:
    """Checks if a given database.table_name exists in a server"""
    query = f"""
    SELECT count() as c
    FROM system.tables where database = '{database}' and name = '{table_name}'
    FORMAT JSON"""

    try:
        client = HTTPClient(server, database=database)
        _, body = client.query_sync(query)
        result = json.loads(body)
        count = result["data"][0]["c"] == 1 if len(result["data"]) else 0
        if count > 1:
            raise Exception(f"LOGICAL ERROR: Found {count} instances of {database}.{table_name} @ {server}")
        return count == 1
    except Exception as e:
        logging.exception(f"Error while checking if table {database}.{table_name} exists @ {server}: {str(e)}")
        raise


async def ch_table_exists_async(table_name: str, server: str, database: str) -> bool:
    """Checks if a given database.table_name exists in a server"""
    query = f"EXISTS TABLE `{database}`.`{table_name}` FORMAT JSON"

    try:
        client = HTTPClient(server, database=database)
        _, body = await client.query(query)
        body_json = json.loads(body)
        result = body_json["data"][0]["result"] if len(body_json["data"]) else 0
        return result > 0
    except Exception as e:
        logging.exception(f"Error while checking if table {database}.{table_name} exists @ {server}: {str(e)}")
        raise


async def ch_table_list_exist(table_name_list: List[str], server: str, database: str) -> List[Tuple[str, bool]]:
    """Checks if a list of table names exist in a database @ server
    Returns a list of [(table_name : str, table_exists : boolean)]"""
    query = f"""
    SELECT name, count() as c
    FROM system.tables where database = '{database}' and name IN {tuple(table_name_list)}
    GROUP BY name FORMAT JSON"""

    try:
        client = HTTPClient(server, database=database)
        _, body = await client.query(query)
        query_result = json.loads(body)
        data = query_result["data"]

        found_tables = []
        result = []

        for row in data:
            count = row["c"]
            if count > 1:
                raise Exception(f"LOGICAL ERROR: Found {count} instances of {database}.{row['name']} @ server {server}")
            found_tables += [row["name"]]
            result += [(row["name"], True)]
        for table_name in table_name_list:
            if table_name not in found_tables:
                result += [(table_name, False)]

        return result

    except Exception as e:
        logging.exception(f"Error while checking if tables {table_name_list} exists in {database} @ {server}: {str(e)}")
        raise


def ch_table_schema(
    table_name: str,
    database_server: str = "localhost",
    database: str = "default",
    include_default_columns: bool = False,
    include_meta_columns: bool = True,
) -> Optional[List[Dict[str, Any]]]:
    try:
        _, body = ch_describe_query_sync(database_server, database, table_name, format="JSON", is_query=False)
    except CHException:
        return None
    return parse_schema(
        body, include_default_columns=include_default_columns, include_meta_columns=include_meta_columns
    )


async def ch_describe_query(
    database_server: str,
    database: str,
    sql: str,
    format: Optional[str] = None,
    is_query: bool = True,
    max_execution_time: Optional[int] = MAX_EXECUTION_TIME,
    ch_params: Optional[Dict[str, Any]] = None,
) -> Tuple[HTTPHeaders, bytes]:
    client, query = _prepare_query(database_server, database, "DESCRIBE", sql, format=format, is_query=is_query)
    if not ch_params:
        ch_params = {}
    return await client.query(query, max_execution_time=max_execution_time, **ch_params)


def ch_describe_query_sync(
    database_server: str,
    database: str,
    sql: str,
    format: Optional[str] = None,
    is_query: bool = True,
    ch_params: Optional[Dict[str, Any]] = None,
):
    client, query = _prepare_query(database_server, database, "DESCRIBE", sql, format=format, is_query=is_query)
    if not ch_params:
        ch_params = {}
    return client.query_sync(query, **ch_params)


async def ch_explain_query(
    database_server: str,
    database: str,
    sql: str,
    format: Optional[str] = None,
    is_query=True,
    explain_type="PLAN",
    max_execution_time: Optional[int] = MAX_EXECUTION_TIME,
    use_index_for_in_with_subqueries: int = 0,
    ch_params: Optional[Dict[str, Any]] = None,
):
    client, query = _prepare_query(
        database_server, database, f"EXPLAIN {explain_type}", sql, format=format, is_query=is_query
    )
    if ch_params is None:
        ch_params = {}
    # use_index_for_in_with_subqueries = 0 because of this bug https://github.com/ClickHouse/ClickHouse/issues/34642
    # https://gitlab.com/tinybird/analytics/-/issues/3252
    return await client.query(
        query,
        use_index_for_in_with_subqueries=use_index_for_in_with_subqueries,
        read_only=True,
        max_execution_time=max_execution_time,
        **ch_params,
    )


async def ch_explain_plan_query(
    database_server: str,
    database: str,
    sql: str,
    format: Optional[str] = None,
    is_query: bool = True,
    with_result: bool = True,
    max_execution_time: Optional[int] = MAX_EXECUTION_TIME,
    ch_params: Optional[Dict[str, Any]] = None,
):
    if not ch_params:
        ch_params = {}
    result = await ch_explain_query(
        database_server,
        database,
        sql,
        format=format,
        is_query=is_query,
        max_execution_time=max_execution_time,
        ch_params=ch_params,
    )
    return result if with_result else None


async def ch_explain_query_json_async(
    database: str,
    database_server: str,
    sql: str,
    explain_type: str = "json=1",
    max_execution_time: Optional[int] = MAX_EXECUTION_TIME,
    use_index_for_in_with_subqueries: int = 0,
    ch_params: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    _, body = await ch_explain_query(
        database_server,
        database,
        sql,
        explain_type=explain_type,
        use_index_for_in_with_subqueries=use_index_for_in_with_subqueries,
        max_execution_time=max_execution_time,
        ch_params=ch_params,
    )
    body = body.decode("utf-8").replace("\n", "").replace("\\n", "").replace("\\", "\\\\")

    try:
        return json.loads(body)
    except json.JSONDecodeError as e:
        logging.exception(f"EXPLAIN query as JSON failed when parsing the response: {e}")
    except Exception:
        pass

    return []


async def ch_explain_estimate_async(
    database: str, database_server: str, sql: str, ch_params: Optional[Dict[str, Any]] = None
) -> Dict:
    _, body = await ch_explain_query(
        database_server, database, sql, format="JSON", explain_type="ESTIMATE", ch_params=ch_params
    )
    body = body.decode("utf-8").replace("\n", "").replace("\\n", "").replace("\\", "\\\\")

    try:
        return json.loads(body)
    except json.JSONDecodeError as e:
        logging.exception(f"EXPLAIN ESTIMATE query as JSON failed when parsing the response: {e}")
    except Exception:
        pass

    return {}


def _prepare_query(
    database_server: str, database: str, prefix_sql: str, sql: str, format: Optional[str] = None, is_query=True
) -> Tuple["HTTPClient", str]:
    client = HTTPClient(database_server, database=database)
    if is_query:
        # Use (Select * FROM query) so it swallows duplicated columns when doing Select col1, col2, * FROM table
        # which can't be used for table creation (and fails under DESCRIBE)
        sql = f"(SELECT * FROM ({sql}))"
    else:
        sql = f"`{sql}`"

    query = f'{prefix_sql} {sql} {f"FORMAT {format}" if format else ""}'
    return client, query


async def ch_finalize_aggregations(database_server: str, database: str, sql: str) -> str:
    try:
        fm_group = get_format_group(sql)
        qq = sql[0 : -len(fm_group)] if fm_group else sql
        (_, body) = await ch_describe_query(database_server, database, qq, format="JSON")
        result: Dict[str, Any] = json.loads(body)
        return wrap_finalize_aggregation(qq, result, fm_group)
    except Exception:
        return sql


@dataclass
class TablesToSwap:
    """Sets to the new_table the name from the old_table"""

    common_database: str
    old_table: str
    new_table: str


@dataclass(frozen=True)
class TablesToSwapWithWorkspace:
    """Tables to swap with the workspace they belong to"""

    common_database: str
    old_table: str
    new_table: Optional[str]
    workspace: str
    pipe_id: Optional[str]
    pipe_name: Optional[str]


def _generate_ch_swap_tables_sql(
    tables_to_swap: Union[List[TablesToSwap], List[TablesToSwapWithWorkspace]], cluster: Optional[str] = None
):
    """
        >>> from chtoolset.query import format as chformat
        >>> query = _generate_ch_swap_tables_sql([\
            TablesToSwap('user_ds', 'first_table_source', 'first_table_dest'),\
            TablesToSwap('user_ds', 'sec_table_source', 'sec_table_dest')], \
            'the_cluster')
        >>> chformat(query) == chformat('EXCHANGE TABLES user_ds.first_table_source AND user_ds.first_table_dest, user_ds.sec_table_source AND user_ds.sec_table_dest ON CLUSTER the_cluster')
        True
    """

    cluster_clause = f"\nON CLUSTER {cluster}" if cluster else ""
    table_swap_template = "\n\t{database}.{table_a} AND {database}.{table_b}"

    return f"""EXCHANGE TABLES{','.join(
        [
            table_swap_template.format(database=swap.common_database, table_a=swap.old_table, table_b=swap.new_table)
            for swap in tables_to_swap
        ]
    )}{cluster_clause}"""


def ch_swap_tables_sync(
    database_server: str,
    tables_to_swap: Union[List[TablesToSwap], List[TablesToSwapWithWorkspace]],
    cluster: Optional[str] = None,
    **extra_params: Any,
):
    sql = _generate_ch_swap_tables_sql(tables_to_swap, cluster)
    client = HTTPClient(database_server, database=None)
    return client.query_sync(sql, read_only=False, **extra_params)


async def ch_swap_tables(
    database_server: str,
    tables_to_swap: Union[List[TablesToSwap], List[TablesToSwapWithWorkspace]],
    cluster: Optional[str] = None,
    **extra_params: Any,
):
    sql = _generate_ch_swap_tables_sql(tables_to_swap, cluster)
    client = HTTPClient(database_server, database=None)
    return await client.query(sql, read_only=False, **extra_params)


def ch_create_table_as_table_sync(
    database_server: str,
    database: str,
    table_name: str,
    as_table_name: str,
    columns: Optional[List[Dict[str, Any]]] = None,
    engine: Optional[str] = None,
    cluster: Optional[str] = None,
    as_table_database: Optional[str] = None,
    not_exists: Optional[bool] = False,
    user_agent: Optional[str] = None,
    create_or_replace: Optional[bool] = False,
    **extra_params: Any,
):
    as_table_database = database if as_table_database is None else as_table_database

    other_table_as_query = CHTable(
        columns if columns else [],
        cluster=cluster,
        engine=engine,
        as_table=f"{as_table_database}.{as_table_name}" if not columns else "",
        not_exists=not_exists,
        storage_policy=None,
    ).as_sql(database, table_name, skip_validation=bool(not columns), create_or_replace=create_or_replace)
    logging.info(f"NULL_TABLE => {other_table_as_query}")

    client = HTTPClient(database_server, database=database)
    return client.query_sync(other_table_as_query, read_only=False, user_agent=user_agent, **extra_params)


async def ch_create_table_as_table(
    database_server: str,
    database: str,
    table_name: str,
    as_table_name: str,
    engine: Optional[str] = None,
    cluster: Optional[str] = None,
    as_table_database: Optional[str] = None,
    **extra_params: Any,
):
    as_table_database = database if as_table_database is None else as_table_database
    as_table = f"{as_table_database}.{as_table_name}"
    other_table_as_query = CHTable([], cluster=cluster, engine=engine, as_table=as_table, storage_policy=None).as_sql(
        database, table_name, skip_validation=True
    )
    client = HTTPClient(database_server, database=database)
    return await client.query(other_table_as_query, read_only=False, **extra_params)


def create_table_on_external_replica(
    database_server: str, database: str, table_details: TableDetails, disk_settings: dict[str, Any]
) -> None:
    if not table_details.details:
        raise ValueError("TableDetails object has no details")
    create_query = table_details.details["create_table_query"]
    create_query_with_disk = add_settings(create_query, "disk", format_disk_settings(disk_settings))
    client = HTTPClient(database_server, database=database)
    client.query_sync(create_query_with_disk, read_only=False)


async def ch_drop_table_with_fallback(
    database_server: str,
    database: str,
    table: str,
    cluster: Optional[str] = None,
    exists_clause: bool = True,
    sync: bool = False,
    avoid_max_table_size: bool = False,
    **extra_params: Any,
) -> None:
    try:
        await ch_drop_table(
            database_server,
            database,
            table,
            cluster,
            exists_clause,
            sync,
            avoid_max_table_size,
            **extra_params,
        )
    except CHException as e:
        if e.code == CHErrors.TABLE_SIZE_EXCEEDS_MAX_DROP_SIZE_LIMIT:
            deleted_date = str(date.today()).replace("-", "_")
            new_table_name = f"{table}_deleted_{deleted_date}"
            await ch_rename_table(database_server, database, table, new_table_name, cluster, **extra_params)
            logging.warning(f"Need to manually DROP {database}.{new_table_name} ON CLUSTER {cluster}")
        else:
            raise e from None


async def ch_drop_table(
    database_server: str,
    database: str,
    table: str,
    cluster: Optional[str] = None,
    exists_clause: bool = True,
    sync: bool = False,
    avoid_max_table_size: bool = False,
    **extra_params: Any,
) -> None:
    cluster_clause = f"ON CLUSTER {cluster}" if cluster else ""
    if_exists_clause = "IF EXISTS" if exists_clause else ""
    sql = f"DROP TABLE {if_exists_clause} {database}.{table} {cluster_clause} {'SYNC' if sync else ''}"
    client = HTTPClient(database_server, database=database)
    if avoid_max_table_size:
        await client.query(
            sql,
            read_only=False,
            **extra_params,
            max_table_size_to_drop=SKIP_TABLE_SIZE_SAFEGUARD,
            max_partition_size_to_drop=SKIP_PARTITION_SIZE_SAFEGUARD,
        )
    else:
        await client.query(sql, read_only=False, **extra_params)


def ch_insert_rows_sync(
    database_server: str, database: str, table: str, rows: Any, log_as_error: bool = True, named_columns: str = ""
):
    client = HTTPClient(database_server, database=database)
    return client.insert_chunk(
        f"INSERT INTO {table} {named_columns} FORMAT CSV",
        csv_from_python_object(rows).encode("utf-8"),
        log_as_error=log_as_error,
    )


def ch_drop_table_sync(
    database_server: str,
    database: str,
    table: str,
    cluster: Optional[str] = None,
    exists_clause: bool = True,
    sync: Optional[bool] = False,
    avoid_max_table_size: bool = False,
    **extra_params: Any,
):
    cluster_clause = f"ON CLUSTER {cluster}" if cluster else ""
    if_exists_clause = "IF EXISTS" if exists_clause else ""
    sql = f"DROP TABLE {if_exists_clause} {database}.{table} {cluster_clause} {'SYNC' if sync else ''}"
    client = HTTPClient(database_server, database=database)
    if avoid_max_table_size:
        return client.query_sync(
            sql,
            read_only=False,
            **extra_params,
            max_table_size_to_drop=SKIP_TABLE_SIZE_SAFEGUARD,
            max_partition_size_to_drop=SKIP_PARTITION_SIZE_SAFEGUARD,
        )
    else:
        return client.query_sync(sql, read_only=False, **extra_params)


async def ch_rename_table(
    database_server: str,
    database: str,
    current_table_name: str,
    new_table_name: str,
    cluster: Optional[str] = None,
    **extra_params: Any,
):
    cluster_clause = f"ON CLUSTER {cluster}" if cluster else ""
    sql = f"RENAME TABLE {database}.{current_table_name} TO {database}.{new_table_name} {cluster_clause}"
    client = HTTPClient(database_server, database=database)
    return await client.query(sql, read_only=False, **extra_params)


async def ch_create_view(
    database_server: str, database: str, view_name: str, query: str, cluster: Optional[str] = None
):
    cluster_clause = f"ON CLUSTER {cluster}" if cluster else ""
    sql = f"CREATE VIEW {database}.{view_name} {cluster_clause} AS SELECT * FROM ({query})"
    client = HTTPClient(database_server, database=database)
    return await client.query(sql, read_only=False)


async def ch_drop_view(
    database_server: str, database: str, view_name: str, cluster: Optional[str] = None
) -> Tuple[HTTPHeaders, bytes]:
    cluster_clause = f"ON CLUSTER {cluster}" if cluster else ""
    sql = f"DROP VIEW IF EXISTS {database}.{view_name} {cluster_clause}"
    client = HTTPClient(database_server, database=database)
    return await client.query(sql, read_only=False)


def ch_replace_partitions_sync(
    database_server: str,
    database: str,
    destination_table: str,
    origin_table: str,
    partitions: List[str],
    max_execution_time: int,
    wait_setting: str = WAIT_ALTER_REPLICATION_ALL,
    lock_acquire_timeout: Optional[int] = None,
    **extra_params: Any,
):
    # TODO do a backup before doing the replacement?
    validate_wait_setting(wait_setting)
    client = HTTPClient(database_server, database=database)
    # https://clickhouse.com/docs/en/sql-reference/statements/alter/#synchronicity-of-alter-queries
    replication_sync = VALID_WAIT_VALUES.index(wait_setting)

    for p in partitions:
        replace_partition_sql = (
            f"ALTER TABLE {database}.{destination_table} REPLACE PARTITION {p} FROM {database}.{origin_table}"
        )

        client.query_sync(
            replace_partition_sql,
            read_only=False,
            alter_sync=replication_sync,
            lock_acquire_timeout=lock_acquire_timeout,
            max_execution_time=max_execution_time,
            **extra_params,
        )


def ch_attach_partitions_sync(
    database_server: str,
    database: str,
    destination_table: str,
    origin_table: str,
    partitions: List[str],
    wait_setting: str = WAIT_ALTER_REPLICATION_ALL,
    origin_database: Optional[str] = None,
    backend_hint: Optional[str] = None,
    disable_upstream_fallback: Optional[bool] = False,
    retries: bool = False,
    user_agent: Optional[str] = None,
    query_settings: Optional[Dict[str, Any]] = None,
):
    origin_database = origin_database or database
    validate_wait_setting(wait_setting)

    replace_partitions_sql = f"""
    ALTER TABLE {database}.{destination_table}
        {','.join([f"ATTACH PARTITION {p} FROM {origin_database}.{origin_table}" for p in partitions])}
    """
    client = HTTPClient(database_server, database=database)
    query_settings = query_settings or {}
    query_settings["alter_sync"] = VALID_WAIT_VALUES.index(wait_setting)
    return client.query_sync(
        replace_partitions_sql,
        read_only=False,
        backend_hint=backend_hint,
        disable_upstream_fallback=disable_upstream_fallback,
        retries=retries,
        user_agent=user_agent,
        **query_settings,
    )


def partition_sql(partition: str):
    """
    Ideally, we should cast the partition value based on the actual partition
    key type. I don't know if we can gather that information from any of the
    system tables, but we could run a query with the partition key to get the
    partition data type and cast accordingly.

    When the partition key is a tuple, the partition value from system.parts has
    the correct type casts. However, when it's a simple value, i.e. a Numeric or
    a String value, it returns plain text.

    https://clickhouse.com/docs/en/sql-reference/statements/alter/partition/#how-to-set-partition-expression

    >>> partition_sql('2018-01-01')
    "'2018-01-01'"
    >>> partition_sql('201801')
    '201801'
    >>> partition_sql('I2020')
    "'I2020'"
    >>> partition_sql("('USD',201810)")
    "('USD',201810)"
    >>> partition_sql('1')
    '1'
    >>> partition_sql('2018-09-29 00:00:00')
    "'2018-09-29 00:00:00'"
    >>> partition_sql('tuple()')
    'tuple()'
    >>> partition_sql("")
    "''"
    >>> partition_sql("(")
    "'('"
    >>> partition_sql(")")
    "')'"
    >>> partition_sql(")na")
    "')na'"
    """
    if partition == "":
        return "''"

    if "'" in partition and partition[0] != "(" and partition[-1] != ")":
        partition = partition.replace("'", "\\'")

    p = partition
    try:
        _ = float(partition)
    except Exception:
        if (partition and (partition != "tuple()" and partition[0] != "(" and partition[-1] != ")")) or len(
            partition
        ) == 1:
            p = f"'{partition}'"
    return p


async def ch_fetch_partitions(
    database_server: str,
    database: str,
    destination_table: str,
    origin_table: str,
    partitions: List[str],
    origin_database: Optional[str] = None,
    max_execution_time: Optional[int] = None,
    user_agent: str = UserAgents.INTERNAL_QUERY.value,
    cluster: Optional[str] = None,
):
    origin_database = origin_database or database

    table_path = f"{origin_database}.{origin_table}"
    original_table_path = "/clickhouse/tables/{layer}-{shard}/" + table_path

    fetch_partition_expr = []
    for p in partitions:
        fetch_partition_expr.append(f"FETCH PARTITION {p} FROM '{original_table_path}'")

    partitions_sql = f"""
        ALTER TABLE {database}.{destination_table}
            {','.join(fetch_partition_expr)}
        """

    client = HTTPClient(database_server)
    return await client.query(
        partitions_sql, read_only=False, max_execution_time=max_execution_time, user_agent=user_agent
    )


async def ch_attach_partitions(
    database_server: str,
    database: str,
    destination_table: str,
    origin_table: str,
    partitions: List[str],
    wait_setting: str = WAIT_ALTER_REPLICATION_ALL,
    origin_database: Optional[str] = None,
    max_execution_time: Optional[int] = None,
    already_fetched: bool = False,
    user_agent: str = UserAgents.INTERNAL_QUERY.value,
):
    origin_database = origin_database or database
    validate_wait_setting(wait_setting)

    partition_expr = []
    for p in partitions:
        if already_fetched:
            partition_expr.append(f"ATTACH PARTITION {p}")
        else:
            partition_expr.append(f"ATTACH PARTITION {p} FROM {origin_database}.{origin_table}")

    partitions_sql = f"""
        ALTER TABLE {database}.{destination_table}
            {','.join(partition_expr)}
        """

    client = HTTPClient(database_server, database=database)
    replication_sync = VALID_WAIT_VALUES.index(wait_setting)
    return await client.query(
        partitions_sql,
        read_only=False,
        alter_sync=replication_sync,
        max_execution_time=max_execution_time,
        user_agent=user_agent,
    )


def ch_get_ops_log_extended_data_by_query_id(
    client: "HTTPClient", cluster: str, query_ids: List[str]
) -> Dict[str, Dict[str, Any]]:
    """Get from query_log some extra data we need for tracking ops logs, like the list of triggered views and CPU time"""

    query_ids_in = "','".join(query_ids)
    sql = f"""
        SELECT
            query_id,
            views,
            ProfileEvents['OSCPUVirtualTimeMicroseconds']/1e6 AS cpu_time
        FROM clusterAllReplicas('{cluster}', system.query_log)
        WHERE
            event_date >= yesterday()
            AND event_time > now() - INTERVAL 8 HOUR
            AND query_id in ('{query_ids_in}')
            AND is_initial_query = 1
            AND type > 1
        FORMAT JSON
    """

    try:
        headers, body = client.query_sync(
            sql,
            max_execution_time=MAX_EXECUTION_TIME,
            skip_unavailable_shards=1,
            log_comment="QUERY_TRIGGERED_VIEWS",
        )
        result = json.loads(body)

        if len(result["data"]) == 0:
            logging.warning("query_log does not contain any entry for query_ids %s", query_ids_in)
            return {}

        data_by_query_id: Dict[str, Dict[str, Any]] = {}
        for row in result["data"]:
            data_by_query_id[row["query_id"]] = {"views": row["views"], "cpu_time": row["cpu_time"]}

        return data_by_query_id

    except Exception as e:
        logging.warning("Failed to retrieve views from query_log for query_ids %s, reason: %s", query_ids_in, e)
        return {}


async def _get_query_log(
    database_server: str, database: str, query_id: str, cluster: Optional[str] = None, elapsed: Optional[float] = 0.0
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    query_table = f"clusterAllReplicas('{cluster}', system.query_log)" if cluster else "system.query_log"
    interval_event_time = "INTERVAL 2 DAY"
    seconds_per_hour = 3_600
    if elapsed:
        hours = int(elapsed // seconds_per_hour) + 1
        interval_event_time = f"INTERVAL {str(hours)} HOUR"

    sql = f"""
        SELECT
            type,
            event_time,
            exception,
            read_rows,
            read_bytes,
            written_rows,
            written_bytes,
            ((ProfileEvents['UserTimeMicroseconds']) + (ProfileEvents['SystemTimeMicroseconds'])) / 1000 AS user_time_ms,
            if((query_duration_ms > 1) AND (user_time_ms > 1), user_time_ms / query_duration_ms, 0) AS cpu_usage,
            memory_usage,
            ProfileEvents['OSCPUVirtualTimeMicroseconds'] as virtual_cpu_time_microseconds
        FROM {query_table}
        WHERE
            event_date >= toDate(now() - {interval_event_time})
            AND event_time > now() - {interval_event_time}
            AND current_database = '{database}'
            AND query_id = '{query_id}'
        ORDER BY
            event_time DESC
        FORMAT JSON
    """

    client = HTTPClient(database_server, database=None)
    try:
        # skip_unavailable_shards: We'd rather get partial info than no info
        headers, body = await client.query(sql, max_execution_time=5, skip_unavailable_shards=1)
        result = json.loads(body)
        return result["data"], headers
    except Exception as e:
        logging.warning(f"Failed to retrieve query status from query_log, reason: {e}")
        return ([], {})


def ch_flush_logs_on_all_replicas_sync(
    database_server: str, cluster: Optional[str] = None, user_agent: Optional[str] = None
) -> None:
    try:
        on_cluser = f" ON CLUSTER {cluster}" if cluster else ""
        client = HTTPClient(database_server, database=None)
        client.query_sync(
            f"SYSTEM FLUSH LOGS{on_cluser}",
            read_only=False,
            user_agent=user_agent or "tb-internal-query",
            max_execution_time=MAX_EXECUTION_TIME_FLUSH_LOGS_SECONDS,
            # TODO: Remove once we remove the automatic retries in query_sync. https://gitlab.com/tinybird/analytics/-/issues/12112
            retries=False,
        )
    except Exception as e:
        logging.warning(f"Cannot flush logs on all replicas: {str(e)}")


async def ch_flush_logs_on_all_replicas(
    database_server: str, cluster: Optional[str] = None, user_agent: Optional[str] = None
):
    try:
        on_cluster = f" ON CLUSTER {cluster}" if cluster else ""
        client = HTTPClient(database_server, database=None)
        await client.query(
            f"SYSTEM FLUSH LOGS{on_cluster}",
            read_only=False,
            user_agent=user_agent or "tb-internal-query",
            max_execution_time=MAX_EXECUTION_TIME_FLUSH_LOGS_SECONDS,
        )
    except Exception as e:
        logging.warning(f"Cannot flush logs on all replicas: {str(e)}")


async def ch_wait_for_query(
    database_server: str,
    database: str,
    query_id: str,
    cluster: Optional[str] = None,
    wait_seconds: int = 60,
    check_frequency_seconds: int = 3,
    started_at: Optional[float] = None,
    has_been_externally_cancelled: Optional[Callable[[], bool]] = None,
) -> Tuple[str, Optional[Dict[str, Any]]]:
    finished = False
    if started_at is None:
        started_at = time.monotonic()

    query_logs: List[Dict[str, Any]] = []
    crash = False
    crash_counter = 0
    query_log_empty_counter = 0

    while not finished:
        if has_been_externally_cancelled and has_been_externally_cancelled():
            await ch_wait_for_query_cancellation(
                database_server, database, query_id, cluster, wait_seconds, check_frequency_seconds
            )
            return query_id, None

        elapsed = time.monotonic() - started_at
        query_logs, headers = await _get_query_log(database_server, database, query_id, cluster, elapsed=elapsed)
        status = await _get_query_status(database_server, cluster, query_id, is_first=True)
        finished = any(i for i in query_logs if i["type"] != "QueryStart")

        if not finished and status == CancelAsyncOperationStatus.NOT_FOUND and len(query_logs) > 0:
            # there's no entry in the query log after 'QueryStart' but the query is not running on any replica
            crash_counter += 1
            logging.warning(f"crash counter set to str({crash_counter}) for query {query_id}")
        # if len(query_logs) == 0 means logs are not being flushed, it can be expected or not see: https://gitlab.com/tinybird/analytics/-/issues/15003#note_2098114499
        # if status from system.processes is WAITING, it means the query is running so we could just wait until it is not waiting anymore
        # but since we use system.query_log to get stats and other stuff let's make the job to fail with an internal error
        if len(query_logs) == 0 and status == CancelAsyncOperationStatus.NOT_FOUND:
            logging.warning(
                f"crash counter set to str({query_log_empty_counter}) for query {query_id} because cannot find query in system.query_log"
            )
            query_log_empty_counter += 1
        else:
            query_log_empty_counter = 0
        if query_log_empty_counter > MAX_QUERY_LOG_EMPTY_COUNTER:
            logging.warning(
                f"query_id {query_id} is not in query_log, if this happens for a while it's an indicator that query_log is not being flushed"
            )
            finished = True
            crash = True
        if crash_counter > MAX_CRASH_COUNTER:
            finished = True
            crash = True
        if finished:
            break
        elapsed = time.monotonic() - started_at
        if elapsed > wait_seconds:
            raise CHException(
                f"Code: 159, e.displayText() = DB::Exception: Timeout exceeded: elapsed {elapsed} seconds, maximum: {wait_seconds}"
            )
        await asyncio.sleep(check_frequency_seconds)

    query_error = next((i for i in query_logs if i["type"] not in ("QueryStart", "QueryFinish")), None)
    if query_error:
        raise CHException(
            query_error["exception"],
            headers=HTTPHeaders(
                {
                    "X-ClickHouse-Summary": json.dumps(
                        {
                            "read_rows": query_error["read_rows"],
                            "read_bytes": query_error["read_bytes"],
                            "written_rows": query_error["written_rows"],
                            "written_bytes": query_error["written_bytes"],
                            "virtual_cpu_time_microseconds": query_error["virtual_cpu_time_microseconds"],
                        }
                    )
                }
            ),
        )
    if crash:
        logging.warning(f"crash on ch_wait_for_query for query_id: {query_id}, database: {database}")
        error_code = "00"
        if query_log_empty_counter > MAX_QUERY_LOG_EMPTY_COUNTER:
            error_code = "01"
            await ch_wait_for_query_cancellation(
                database_server, database, query_id, cluster, wait_seconds, check_frequency_seconds
            )
        msg = f"Job failed due to an internal error: {error_code}, try it again. If the problem persists, please contact us at support@tinybird.co"
        logging.exception(msg)
        raise Exception(msg)

    query_finish_logs: Optional[Dict[str, Any]] = next((i for i in query_logs if i["type"] == "QueryFinish"), None)
    ch_server = headers.get("X-ClickHouse-Server-Display-Name")
    if ch_server and query_finish_logs:
        query_finish_logs.update({"X-ClickHouse-Server-Display-Name": ch_server})
    return query_id, query_finish_logs


def ch_guarded_query(
    database_server: str,
    database: str,
    query: str,
    cluster: Optional[str] = None,
    max_execution_time: int = 60,
    query_id: Optional[str] = None,
    check_frequency_seconds: int = 3,
    has_been_externally_cancelled: Optional[Callable[[], bool]] = None,
    user_agent: Optional[str] = None,
    timeout: Optional[int] = None,
    read_only: bool = False,
    read_cluster: bool = False,
    backend_hint: Optional[str] = None,
    disable_upstream_fallback: Optional[bool] = False,
    retries: bool = True,
    **kwargs,
):
    """Use this method for long-running queries.

    Queries where you don't need to return their result, but you want to ensure they ran until they finished,
    or they raised an error. E.g., populate a table with an insert query.

    This is SLOW. DO NOT USE IT for interactive queries where you expect the result within 5 seconds or less.

    This doesn't only rely on the HTTP request but also in the query result. This is useful when the query might take
    longer than the configured connection timeout for the HTTP request.

    For instance, that could happen when the ClickHouse server is behind a load balancer, e.g. Varnish, that might
    close the connection but the query is still running in ClickHouse.
    """
    started_at = time.monotonic()
    query_id = query_id or ulid.new().str

    if has_been_externally_cancelled:
        is_externally_cancelled = has_been_externally_cancelled()
        if is_externally_cancelled:
            return query_id, None

    client = HTTPClient(database_server, database=database)

    try:
        response = {"type": "QueryFinish"}
        headers, content = client.query_sync(
            query,
            read_only=read_only,
            query_id=query_id,
            user_agent=user_agent,
            max_execution_time=max_execution_time,
            timeout=timeout if timeout else max_execution_time,
            wait_end_of_query=1,
            read_cluster=read_cluster,
            backend_hint=backend_hint,
            disable_upstream_fallback=disable_upstream_fallback,
            retries=retries,
            **kwargs,
        )

        if has_been_externally_cancelled and has_been_externally_cancelled():
            return query_id, None

        if "::Exception" in content.decode("utf-8"):
            raise CHException(content.decode("utf-8"))

        ch_summary = headers.get("X-ClickHouse-Summary")
        if ch_summary:
            results = json.loads(ch_summary)
            response.update(results)
            # TODO: Remove once we use CH >= 24.6.10 everywhere
            if "virtual_cpu_time_microseconds" not in results:
                response["virtual_cpu_time_microseconds"] = "0"

        ch_server = headers.get("X-ClickHouse-Server-Display-Name")
        if ch_server:
            response.update({"X-ClickHouse-Server-Display-Name": ch_server})
        return query_id, response
    except Exception as e:
        logging.warning(f"Error in ch_guarded_query: {e}, {traceback.format_exc()}")

    # If something went wrong we read from the query log. It might be that the query was already running
    # (from a previous execution) or some other error
    wait_seconds_long_enough_so_the_ch_timeout_raises_before_app_timeout = (
        max_execution_time + check_frequency_seconds + 1
    )
    return async_to_sync(ch_wait_for_query)(
        database_server,
        database,
        query_id,
        cluster,
        wait_seconds_long_enough_so_the_ch_timeout_raises_before_app_timeout,
        check_frequency_seconds,
        started_at,
        has_been_externally_cancelled,
    )


class CancelAsyncOperationStatus(Enum):
    # The cancellation can't find the query if it's not currently running or if it's already finished/cancelled
    NOT_FOUND = "NOT_FOUND"
    # The signal to kill the query has already been sent and clickhouse is trying to kill the query
    WAITING = "WAITING"
    # query cancelled on cluster and next it's not in system.processes so it was effectively cancelled
    CANCELLED = "CANCELLED"
    # the cancelled status is unknown, this is returned when the status is not checked
    UNKNOWN = "UNKNOWN"


async def _ch_cancel_query_async_operation(
    database_server: str, database: str, query_id: str, cluster: Optional[str] = None, is_first=True, check_status=True
) -> CancelAsyncOperationStatus:
    """
    This method is safe to be called multiple times for the same query_id. It will return
    CancelAsyncOperationStatus.WAITING the first and next times the cancellation is requested for the same query_id for non cluster queries

    When cancelling on cluster it'll return:
        - NOT_FOUND if the query is not in system.processes and is_first=True
        - CANCELLED if the query is not in system.processes
        - WAITING if it's marked as `is_cancelled` in system.processes but it's still there
        - UNKNOWN if `check_status` is False since the status is not checked
    """
    cluster_clause = f"ON CLUSTER {cluster} " if cluster else ""
    client = HTTPClient(database_server, database=database)

    query = f"KILL QUERY {cluster_clause}WHERE query_id='{query_id}' ASYNC FORMAT JSON;"
    _, body = await client.query(
        query,
        read_only=False,
        # If one replica is down, not need to wait for it as the query would be have been killed anyway
        max_execution_time=2,
        distributed_ddl_task_timeout=1,
        distributed_ddl_output_mode=DDL_OUTPUT_MODE_NULL_STATUS_ON_TIMEOUT,
    )
    if body == b"" and not cluster:
        return CancelAsyncOperationStatus.NOT_FOUND

    if not check_status:
        return CancelAsyncOperationStatus.UNKNOWN

    if cluster:
        return await _get_query_status(database_server, cluster, query_id, is_first)

    result = json.loads(body)
    if cluster or result["data"][0].get("kill_status", "") == "waiting":
        return CancelAsyncOperationStatus.WAITING

    raise RuntimeError(
        f"Unknown cancel result for query {query_id}, kill_status received: {result['data'][0]['kill_status']}"
    )


async def ch_get_running_kill_queries_async(database_server: str, cluster: Optional[str] = None) -> int:
    try:
        from_clause = f"clusterAllReplicas('{cluster}', system.processes)" if cluster else "system.processes"
        client = HTTPClient(database_server)
        query = f"SELECT count() as c FROM {from_clause} WHERE current_database != 'default' AND query LIKE 'KILL QUERY%' FORMAT JSON;"
        # skip_unavailable_shards: We'd rather get partial info than no info
        _, body = await client.query(query, read_only=False, max_execution_time=3, skip_unavailable_shards=1)
        count = json.loads(body)["data"][0].get("c", 0)
        return count
    except Exception as e:
        logging.warning(f"Failed to retrieve running KILL queries from system.processes, reason: {e}")
        pass
    return 0


async def _get_query_status(database_server: str, cluster: Optional[str], query_id: str, is_first: bool = False):
    try:
        from_clause = f"clusterAllReplicas('{cluster}', system.processes)" if cluster else "system.processes"
        client = HTTPClient(database_server)
        query = f"SELECT count() as c, countIf(is_cancelled = 1) cancelled FROM {from_clause} WHERE query_id = '{query_id}' FORMAT JSON"
        # skip_unavailable_shards: We'd rather get partial info than no info
        _, body = await client.query(query, read_only=False, max_execution_time=3, skip_unavailable_shards=1)
        data = json.loads(body)["data"][0]
        exists_query = data["c"] > 0
        is_cancelling = data["cancelled"] > 0
        if not exists_query:
            if not is_first:
                return CancelAsyncOperationStatus.CANCELLED
            else:
                # query might have been effectively killed but since it does not show up in system.processes
                # we can't know if it was CANCELLED or NOT_FOUND so we return NOT_FOUND
                return CancelAsyncOperationStatus.NOT_FOUND
        if is_cancelling:
            return CancelAsyncOperationStatus.WAITING
    except Exception as e:
        logging.warning(f"Failed to retrieve query status from system.processes, reason: {e}")
        return CancelAsyncOperationStatus.WAITING


class WaitingCancelOperationResult(Enum):
    # The function can't find the query to kill it, usually because it's not running or if it's already finished/cancelled.
    NOT_FOUND = "NOT_FOUND"
    # The function have found the killable query and have been able to track it until it finished.
    CANCELLED = "CANCELLED"


async def ch_wait_for_query_cancellation(
    database_server: str,
    database: str,
    query_id: str,
    cluster: Optional[str],
    wait_seconds: int = 60,
    check_frequency_seconds: int = 5,
) -> WaitingCancelOperationResult:
    finished = False
    started_at = time.monotonic()
    query_found_and_we_are_trying_to_cancel_it = False

    first = True
    while not finished:
        elapsed = time.monotonic() - started_at
        if elapsed > wait_seconds:
            raise CHException(
                f"Code: 159, e.displayText() = DB::Exception: Timeout exceeded: elapsed {elapsed} seconds, maximum: {wait_seconds}"
            )

        cancellation_status = await _ch_cancel_query_async_operation(
            database_server, database, query_id, cluster, is_first=first
        )
        first = False
        if cancellation_status == CancelAsyncOperationStatus.NOT_FOUND:
            finished = True
        elif cancellation_status == CancelAsyncOperationStatus.WAITING:
            query_found_and_we_are_trying_to_cancel_it = True
            await asyncio.sleep(check_frequency_seconds)
        elif cancellation_status == CancelAsyncOperationStatus.CANCELLED:
            return WaitingCancelOperationResult.CANCELLED

    if query_found_and_we_are_trying_to_cancel_it:
        return WaitingCancelOperationResult.CANCELLED
    return WaitingCancelOperationResult.NOT_FOUND


def ch_get_replica_load(database_server: str):
    # Returns available threads, and the percentage of memory and cpu available (0-100)
    client = HTTPClient(database_server)
    get_consumption_sql = """
        SELECT
            metric,
            value
        FROM system.asynchronous_metrics
        WHERE metric in (
            'OSMemoryAvailable',
            'OSIdleTime'
        )
        FORMAT JSON
    """
    available_memory = None
    available_cpu_cores = None

    try:
        _, body = client.query_sync(get_consumption_sql)
        data = json.loads(body).get("data", [])
        if not data:
            return None, None

        result = {item["metric"]: item["value"] for item in data}

        available_cpu_cores = int(result.get("OSIdleTime", 0))
        available_memory = int(result.get("OSMemoryAvailable", 0))
        return available_memory, available_cpu_cores
    except Exception as e:
        logging.exception(f"Error on getting replica load: {e}")
    return available_memory, available_cpu_cores


def _select_from_create_materialized_view_query(create_materialized_view_query: str) -> str:
    """
    >>> _select_from_create_materialized_view_query("CREATE MATERIALIZED VIEW db.mv ON CLUSTER '{cluster}' AS SELECT 1")
    'SELECT 1'
    >>> _select_from_create_materialized_view_query("CREATE MATERIALIZED VIEW db.mv ON CLUSTER '{cluster}' AS SELECT 1 FROM db.table")
    'SELECT 1 FROM db.table'
    >>> create_materialized_view_query = 'CREATE MATERIALIZED VIEW d_test_832b9e91833f4239bf95d4a92d297178.t_dee6b5354df14b78b5de87c79411251b TO d_test_832b9e91833f4239bf95d4a92d297178.t_10a7d3f236074acea681b9b7052b92df (`a` UInt64, `date` Date) AS SELECT a, date FROM d_test_832b9e91833f4239bf95d4a92d297178.t_d1f5663f92af411a8d04b8e5c1cb8c76 AS origin_datasource_name_5356b0b9846943018ba3e4fe8f194c3e'
    >>> _select_from_create_materialized_view_query(create_materialized_view_query)
    'SELECT a, date FROM d_test_832b9e91833f4239bf95d4a92d297178.t_d1f5663f92af411a8d04b8e5c1cb8c76 AS origin_datasource_name_5356b0b9846943018ba3e4fe8f194c3e'
    """
    # Split on " AS SELECT " to handle both cases with and without parentheses
    parts = create_materialized_view_query.split(" AS SELECT ")
    if len(parts) != 2:
        raise ValueError("Invalid materialized view query format")
    return f"SELECT {parts[1].strip()}"


def _create_materialized_view_query(
    database: str,
    view_name: str,
    sql: str,
    target_table: Optional[str] = None,
    target_database: Optional[str] = None,
    engine: Optional[str] = None,
    cluster: Optional[str] = None,
    if_not_exists: bool = False,
):
    if target_table and engine:
        raise ValueError("You can only specify engine or target_table params, not both")

    target_database = target_database if target_database else database

    try:
        # We use get_left_table as a way to validate the query (both that is valid and that it can be used in a MV)
        _ = get_left_table(sql)
    except ValueError as e:
        raise ValueError(f"Invalid SQL for materialized view: {str(e)}") from e

    cluster_clause = f"ON CLUSTER {cluster}" if cluster else ""
    if_exists_clause = "IF NOT EXISTS" if not if_not_exists else ""
    to = f"TO `{target_database}`.`{target_table}`" if target_table else ""
    if cluster and engine_can_be_replicated(engine) and engine:
        engine = engine_local_to_replicated(engine, database, view_name)
    engine_clause = f"ENGINE = {engine}" if engine else ""
    return f"CREATE MATERIALIZED VIEW {if_exists_clause} {database}.{view_name} {cluster_clause} {to} {engine_clause} AS {sql}"


async def ch_create_materialized_view(
    workspace: "User",
    view_name: str,
    sql: str,
    target_table: Optional[str] = None,
    target_database: Optional[str] = None,
    engine: Optional[str] = None,
    if_not_exists: bool = False,
    drop_on_error: bool = True,
):
    target_database = target_database if target_database else workspace.database
    create_view_query = _create_materialized_view_query(
        workspace.database,
        view_name,
        sql,
        target_table=target_table,
        target_database=target_database,
        engine=engine,
        cluster=workspace.cluster,
        if_not_exists=if_not_exists,
    )
    params: Dict[str, Any] = workspace.ddl_parameters(skip_replica_down=True)
    try:
        client = HTTPClient(workspace.database_server, database=workspace.database)
        await client.query(create_view_query, read_only=False, **params)
    except Exception as e:
        try:
            logging.warning(f"Error on create_materialized_view, will try to drop it to avoid an orphan matview: {e}")
            if not drop_on_error:
                logging.exception(f"Error on create_materialized_view, possible orphan matview: {e}")
                raise e
            await ch_drop_table(
                workspace.database_server,
                target_database,
                view_name,
                cluster=workspace.cluster,
                **params,
            )
            raise e
        except Exception as exc:
            # handled error
            if isinstance(exc, CHException) and exc.code in [
                CHErrors.DATA_TYPE_CANNOT_BE_USED_IN_TABLES,
                CHErrors.CANNOT_CONVERT_TYPE,
            ]:
                logging.warning(str(exc))
                raise exc from e
            logging.exception(f"Error on create_materialized_view, possible orphan matview: {exc}")
            raise exc from e


async def ch_create_kafka_table_engine(
    workspace: "User",
    name: str,
    columns: List[Dict[str, str]],
    kafka_bootstrap_servers: str,
    kafka_topic: str,
    kafka_security_protocol: str,
    kafka_sasl_mechanism: str,
    kafka_sasl_username: str,
    kafka_sasl_password: str,
    if_not_exists: bool = False,
):
    cluster_clause = f"ON CLUSTER {workspace.cluster}" if workspace.cluster else ""
    if_exists_clause = "IF NOT EXISTS" if not if_not_exists else ""
    columns_clause = f"({', '.join(schema_to_sql_columns(columns))})"
    create_query = f"""
    CREATE TABLE {if_exists_clause} {workspace.database}.{name} {cluster_clause} {columns_clause}
    ENGINE = Kafka
    SETTINGS
        kafka_security_protocol = '{kafka_security_protocol}',
        kafka_sasl_mechanisms = '{kafka_sasl_mechanism}',
        kafka_sasl_username = '{kafka_sasl_username}',
        kafka_sasl_password = '{kafka_sasl_password}',
        kafka_broker_list = '{kafka_bootstrap_servers}',
        kafka_topic_list = '{kafka_topic}',
        kafka_group_name = 'tinybirdco',
        kafka_format = 'JSONEachRow';
    """
    client = HTTPClient(workspace.database_server, database=workspace.database)
    params: Dict[str, Any] = workspace.ddl_parameters(skip_replica_down=True)
    return await client.query(create_query, read_only=False, **params)


async def ch_create_streaming_query(
    workspace: "User",
    name: str,
    target_table: str,
    sql: str,
    if_not_exists: bool = False,
):
    cluster_clause = f"ON CLUSTER {workspace.cluster}" if workspace.cluster else ""
    if_exists_clause = "IF NOT EXISTS" if not if_not_exists else ""
    create_query = f"CREATE STREAMING QUERY {if_exists_clause} {name} {cluster_clause} TO {target_table} AS {sql}"
    client = HTTPClient(workspace.database_server, database=workspace.database)
    params: Dict[str, Any] = workspace.ddl_parameters(skip_replica_down=True)
    # Always enable the analyzer when creating streaming queries.
    # Despite it will work, if analyzer is not enabled ClickHouse will use the old analyzer
    # to analyze the query and retrieve column types while using the new analyzer to create
    # the streaming query. This could lead to issues and broken streaming queries.
    #
    # TO-DO: Remove this when allow_experimental_analyzer is enabled everywhere.
    params["allow_experimental_analyzer"] = 1
    return await client.query(create_query, read_only=False, **params)


def ch_create_materialized_view_sync(
    database_server: str,
    database: str,
    view_name: str,
    sql: str,
    target_table: Optional[str] = None,
    target_database: Optional[str] = None,
    engine: Optional[str] = None,
    cluster: Optional[str] = None,
    if_not_exists: bool = False,
    **extra_params: Any,
):
    target_database = target_database if target_database else database
    create_view_query = _create_materialized_view_query(
        database,
        view_name,
        sql,
        target_table=target_table,
        target_database=target_database,
        engine=engine,
        cluster=cluster,
        if_not_exists=if_not_exists,
    )

    try:
        client = HTTPClient(database_server, database=database)
        return client.query_sync(create_view_query, read_only=False, **extra_params)
    except Exception as e:
        try:
            logging.warning(f"Error on create_materialized_view, will try to drop it to avoid an orphan matview: {e}")
            ch_drop_table_sync(database_server, target_database, view_name, cluster=cluster, **extra_params)
            raise e
        except Exception as exc:
            logging.exception(f"Error on create_materialized_view, possible orphan matview: {exc}")
            raise exc from e


def ch_get_create_materialized_view_query_sync(database_server: str, database: str, view_name: str):
    sql = f"SELECT create_table_query FROM system.tables WHERE database = '{database}' AND name = '{view_name}' FORMAT JSON"
    _, result = HTTPClient(database_server).query_sync(sql)
    return json.loads(result).get("data", [{}])[0].get("create_table_query", "")


def _table_partitions_query(database_name: str, table_names: List[str], condition: str = ""):
    tables_in_sql = ", ".join([f"'{t}'" for t in table_names])
    partition_condition = ""
    if condition:
        for table_name in table_names:
            partition_condition += f"""
            AND (
            partition_id IN (
            SELECT _partition_id
            FROM {database_name}.{table_name}
            WHERE {condition}
            GROUP BY _partition_id))
            """
    sql = f"""
    SELECT DISTINCT partition
    FROM (
        SELECT partition, partition_id, sum(rows) rows, max(modification_time) modification_time
        FROM system.parts
        WHERE
            database = '{database_name}'
            AND table IN ({tables_in_sql})
            AND active
        GROUP BY partition, partition_id
    ) """
    sql += """WHERE rows > 0
    {partition_condition}
    ORDER BY modification_time DESC, partition DESC
    FORMAT JSON
    """
    return sql, partition_condition


def _query_table_partitions_with_condition_fallback_sync(
    database_server: str,
    database_name: str,
    table_names: List[str],
    condition: str = "",
    backend_hint: Optional[str] = None,
    disable_upstream_fallback: Optional[bool] = False,
    user_agent: Optional[str] = UserAgents.INTERNAL_QUERY.value,
    query_settings: Optional[Dict[str, Any]] = None,
) -> List[str]:
    sql, partition_condition = _table_partitions_query(database_name, table_names, condition)
    client = HTTPClient(database_server, database=database_name)
    query_settings = query_settings or {}
    try:
        _, result = client.query_sync(
            sql.format(partition_condition=partition_condition),
            user_agent=user_agent,
            max_execution_time=60,
            backend_hint=backend_hint,
            disable_upstream_fallback=disable_upstream_fallback,
            **query_settings,
        )
    except CHException as e:
        logging.exception(f"Failed to filter partitions by condition: {e}")
        # fallback to query without partition conditions
        _, result = client.query_sync(sql.format(partition_condition=""), user_agent=user_agent, **query_settings)

    table_partitions = json.loads(result).get("data", [])
    partitions = [p["partition"] for p in table_partitions]
    return partitions


def ch_table_partitions_sync(
    database_server: str,
    database_name: str,
    table_names: List[str],
    condition: str = "",
    backend_hint: Optional[str] = None,
    disable_upstream_fallback: Optional[bool] = False,
    user_agent: Optional[str] = None,
    query_settings: Optional[Dict[str, Any]] = None,
) -> List[str]:
    table_name = table_names if isinstance(table_names, str) else table_names[0]
    table_details = ch_table_details(table_name, database_server, database_name)
    if table_details.engine.lower() == "":  # Necessary check because of the View usage on ITX
        return []

    partitions = _query_table_partitions_with_condition_fallback_sync(
        database_server,
        database_name,
        table_names,
        condition,
        backend_hint,
        disable_upstream_fallback,
        user_agent,
        query_settings,
    )
    partition_key = table_details.partition_key
    if not partition_key or partition_key in ["tuple()", ""]:
        return partitions

    partition_type_sql = (
        f"DESCRIBE (SELECT {partition_key} as partition_key FROM {database_name}.{table_name}) FORMAT JSON"
    )
    client = HTTPClient(database_server, database=database_name)
    _, result = client.query_sync(
        partition_type_sql,
        user_agent=user_agent,
        disable_upstream_fallback=disable_upstream_fallback,
        **(query_settings or {}),
    )
    data = json.loads(result).get("data", [{}])
    partition_key_type = data[0].get("type", None)

    # we need to check basic types and also types like 'DateTime(UTC/...)'
    if __needs_quote(partition_key_type):
        partitions = [f"'{p}'" for p in partitions]

    return partitions


def __needs_quote(partition_key_type: Optional[str]):
    return partition_key_type and (
        partition_key_type
        in [
            "UUID",
            "Date",
            "DateTime",
            "String",
            "LowCardinality(String)",
        ]
        or partition_key_type.startswith("DateTime(")
    )


def __prepare_table_columns_client(database_server: str, database: str, table_name: str) -> Tuple["HTTPClient", str]:
    sql = f"""SELECT *
    FROM system.columns
    WHERE
        database = '{database}'
        AND table = '{table_name}'
    FORMAT JSON
    """
    return HTTPClient(database_server, database=database), sql


async def ch_table_columns(database_server: str, database: str, table_name: str) -> List[Dict[str, Any]]:
    client, sql = __prepare_table_columns_client(database_server, database, table_name)
    _, result = await client.query(sql)
    return json.loads(result).get("data", [])


def ch_table_columns_sync(database_server, database, table_name) -> List[Dict[str, Any]]:
    client, sql = __prepare_table_columns_client(database_server, database, table_name)
    _, result = client.query_sync(sql)
    return json.loads(result).get("data", [])


async def ch_truncate_table_with_fallback(
    database_server: str,
    database: str,
    table: str,
    cluster: Optional[str] = None,
    wait_setting: str = WAIT_ALTER_REPLICATION_ALL,
    **extra_params: Any,
) -> None:
    """
    Be aware that in a cluster, client.query will not raise Exception if the truncate fails.
    The truncate may fail in tables with unsupported engines as Null, View, File or URL.
    https://clickhouse.tech/docs/en/sql-reference/statements/truncate/
    """
    try:
        await ch_truncate_table(
            database_server,
            database,
            table,
            cluster,
            wait_setting,
            **extra_params,
        )
    except CHException as e:
        if e.code == CHErrors.TABLE_SIZE_EXCEEDS_MAX_DROP_SIZE_LIMIT:
            truncated_date = str(date.today()).replace("-", "_")
            new_table_name = f"{table}_too_big_to_truncate_{truncated_date}_{str(uuid.uuid4())[:8]}"
            await ch_create_exact_empty_copy(database_server, database, table, cluster, new_table_name, **extra_params)
            tables_to_swap = [TablesToSwap(common_database=database, old_table=table, new_table=new_table_name)]
            await ch_swap_tables(database_server, tables_to_swap, cluster, **extra_params)
            logging.warning(f"Need to manually DROP {database}.{new_table_name} ON CLUSTER {cluster}")
        else:
            raise e from None


async def ch_truncate_table(
    database_server: str,
    database: str,
    table: str,
    cluster: Optional[str] = None,
    wait_setting: str = WAIT_ALTER_REPLICATION_ALL,
    max_execution_time: Optional[int] = None,
    **extra_params: Any,
) -> None:
    validate_wait_setting(wait_setting)
    replication_sync = VALID_WAIT_VALUES.index(wait_setting)
    cluster_clause = f"ON CLUSTER {cluster}" if cluster else ""
    sql = f"TRUNCATE TABLE {database}.{table} {cluster_clause}"
    client = HTTPClient(database_server, database=database)

    await client.query(
        sql,
        read_only=False,
        alter_sync=replication_sync,
        max_execution_time=max_execution_time,
        skip_unavailable_shards=1,
        **extra_params,
    )


async def ch_create_exact_empty_copy(
    database_server: str, database: str, table: str, cluster: Optional[str], new_table_name: str, **extra_params: Any
):
    table_details = await ch_table_details_async(table, database_server, database, clean_settings=False)
    await ch_create_table_as_table(
        database_server,
        database,
        new_table_name,
        table,
        engine=table_details.engine_full,
        cluster=cluster,
        **extra_params,
    )


class CHTableLocation(NamedTuple):
    database: str
    table: str


def ch_create_null_table_with_mv_for_mv_populate(
    workspace: "User",
    source_table: CHTableLocation,
    target_table: str,
    target_table_details: TableDetails,
    temporal_table_sufix: str,
    view_sql: str,
    temporal_view_sufix: str,
    include_ttl_in_replacements_operation: bool = False,  # TODO True for populates, but may be useful as well for replaces, we just need to check that the operation doesn't break existing replaces
    columns: Optional[List[Dict[str, Any]]] = None,
    create_or_replace: Optional[bool] = False,
    **extra_params: Any,
) -> Tuple[str, str]:
    """
    Given:
    +--------------+  view_sql +--------------+
    | source_table | --------> | target_table |
    +--------------+           +--------------+
    Creates a Null table based on source_table + a mv with the SQL in view_sql so we can repopulate
    target_table. This repopulate can be done with the data from source_table using an INSERT INTO + SELECT.
    """
    # create a null table
    temporal_null_table = f"{target_table}_{temporal_table_sufix}"
    ch_create_table_as_table_sync(
        database_server=workspace.database_server,
        database=workspace.database,
        table_name=temporal_null_table,
        as_table_name=source_table.table,
        columns=columns,
        engine="Null()",
        cluster=workspace.cluster,
        as_table_database=source_table.database,
        create_or_replace=create_or_replace,
        **extra_params,
    )

    # create a mat view from that temporal table
    temporal_view_from_null_table = f"{target_table}_{temporal_view_sufix}"
    replacements: Dict[Union[CHTableLocation, Tuple[str, str]], str] = {}
    if source_table.database != workspace.database:
        replacements[source_table] = temporal_null_table
    else:
        replacements[(source_table.database, source_table.table)] = temporal_null_table
    if include_ttl_in_replacements_operation:
        replacements = include_ttl_in_replacements(
            replacements, view_sql, workspace.database, workspace.database_server, source_table, target_table
        )

    # Replaces the view_sql with the new Null table name.
    view_sql_with_null_table_as_source = replace_tables(
        sql=view_sql, replacements=replacements, default_database=workspace.database, only_replacements=True
    )

    if include_ttl_in_replacements_operation:
        view_sql_with_null_table_as_source = _apply_ttl_condition(
            workspace.database_server, workspace.database, target_table_details, view_sql_with_null_table_as_source
        )

    ch_create_materialized_view_sync(
        database_server=workspace.database_server,
        database=workspace.database,
        view_name=temporal_view_from_null_table,
        sql=view_sql_with_null_table_as_source,
        target_table=target_table,
        cluster=workspace.cluster,
        **extra_params,
    )

    return temporal_null_table, temporal_view_from_null_table


def ch_create_null_table_with_mv_for_mv_populate_with_fetch(
    workspace: "User",
    source_table: CHTableLocation,
    target_database: str,
    target_table: str,
    target_table_details: TableDetails,
    temporal_table_sufix: str,
    view_sql: str,
    temporal_view_sufix: str,
    include_ttl_in_replacements_operation: bool = True,
    target_database_server: Optional[str] = None,
    columns: Optional[List[Dict[str, Any]]] = None,
) -> Tuple[str, str]:
    """
    Given:
    +--------------+  view_sql +--------------+
    | source_table | --------> | target_table |
    +--------------+           +--------------+
    Creates a Null table based on source_table + a mv with the SQL in view_sql so we can repopulate
    target_table. This repopulate can be done with the data from source_table using an INSERT INTO + SELECT.
    """
    # create a null table
    temporal_null_table = f"{target_table}_{temporal_table_sufix}"

    target_database_server = target_database_server if target_database_server else workspace.database_server

    ch_create_table_as_table_sync(
        database_server=target_database_server,
        database=target_database,
        table_name=temporal_null_table,
        as_table_name=source_table.table,
        columns=columns,
        engine="Null()",
        as_table_database=source_table.database,
        **workspace.ddl_parameters(),
    )

    # create a mat view from that temporal table
    temporal_view_from_null_table = f"{target_table}_{temporal_view_sufix}"
    replacements: Dict[Union[CHTableLocation, Tuple[str, str]], str] = {}
    replacements[source_table] = temporal_null_table

    if include_ttl_in_replacements_operation:
        replacements = include_ttl_in_replacements(
            replacements, view_sql, target_database, target_database_server, source_table, target_table
        )

    # Replaces the view_sql with the new Null table name.
    view_sql_with_null_table_as_source = replace_tables(
        sql=view_sql, replacements=replacements, default_database=target_database, only_replacements=True
    )

    if include_ttl_in_replacements_operation:
        view_sql_with_null_table_as_source = _apply_ttl_condition(
            target_database_server, target_database, target_table_details, view_sql_with_null_table_as_source
        )

    ch_create_materialized_view_sync(
        database_server=target_database_server,
        database=target_database,
        view_name=temporal_view_from_null_table,
        sql=view_sql_with_null_table_as_source,
        target_table=target_table,
        target_database=target_database,
        **workspace.ddl_parameters(),
    )

    return temporal_null_table, temporal_view_from_null_table


def _apply_ttl_condition(database_server: str, workspace_database: str, table_details: TableDetails, query: str) -> str:
    target_ttl = ttl_condition_from_engine_full(table_details.engine_full)
    if target_ttl:
        _query = f"SELECT * FROM ({query}) WHERE {target_ttl}"
        try:
            ch_describe_query_sync(database_server, workspace_database, _query, format="JSON")
            query = _query
        except Exception:
            # the query with the new condition is not valid and we don't care
            pass
    return query


def _ch_source_table_for_view_query(view: str, database: Optional[str] = None) -> str:
    database_clause = f" AND has(dependencies_database, '{database}') " if database else ""
    return f"""
        SELECT database, name FROM system.tables
        WHERE has(dependencies_table, '{view}')
        {database_clause}
        FORMAT JSON
    """


def ch_source_table_for_view_sync(
    database_server: str, database: str, view: str, **extra_params: Any
) -> Optional[CHTableLocation]:
    sql = _ch_source_table_for_view_query(view, database=database)
    client = HTTPClient(database_server, database=database)
    _, body = client.query_sync(sql, **extra_params)
    result = json.loads(body)
    if len(result["data"]) == 0:
        return None
    return CHTableLocation(result["data"][0]["database"], result["data"][0]["name"])


async def ch_source_table_for_view(database_server: str, database: str, view: str) -> Optional[CHTableLocation]:
    sql = _ch_source_table_for_view_query(view, database=database)
    client = HTTPClient(database_server, database=database)
    _, body = await client.query(sql)
    result = json.loads(body)
    if len(result["data"]) == 0:
        return None
    return CHTableLocation(result["data"][0]["database"], result["data"][0]["name"])


def _ch_table_dependent_views_sql(database: str, table_name: str) -> str:
    return f"""
        SELECT database, name
        FROM (
            SELECT arrayJoin(arrayZip(dependencies_database, dependencies_table)) as _table
            FROM system.tables
            WHERE database = '{database}' AND name = '{table_name}'
            ) deps
        JOIN system.tables ON _table.1 = database AND _table.2 = name
        WHERE engine = 'MaterializedView'
        FORMAT JSON;
    """


def ch_table_dependent_views_sync(database_server: str, database: str, table_name: str) -> List[CHTableLocation]:
    sql = _ch_table_dependent_views_sql(database, table_name)
    client = HTTPClient(database_server, database=database)
    _, body = client.query_sync(sql)
    result = json.loads(body)
    return [CHTableLocation(v["database"], v["name"]) for v in result["data"]]


async def ch_table_dependent_views_async(database_server: str, database: str, table_name: str) -> List[CHTableLocation]:
    sql = _ch_table_dependent_views_sql(database, table_name)
    client = HTTPClient(database_server, database=database)
    _, body = await client.query(sql)
    result = json.loads(body)
    return [CHTableLocation(v["database"], v["name"]) for v in result["data"]]


_ch_get_cluster_hosts_query = """
        SELECT
            cluster,
            shard_num,
            shard_weight,
            replica_num,
            host_name,
            host_address,
            port,
            is_local
        FROM system.clusters
        FORMAT JSON
    """


def ch_get_clusters_hosts(database_server: str) -> List[Dict[str, Any]]:
    client = HTTPClient(database_server)
    _, body = client.query_sync(_ch_get_cluster_hosts_query, read_only=False)
    result = json.loads(body)
    return result["data"]


async def ch_get_clusters_hosts_async(database_server: str) -> List[Dict[str, str]]:
    client: HTTPClient = HTTPClient(database_server)
    extra_params: Dict[str, Any] = {"skip_unavailable_shards": 1}
    body: bytes
    _, body = await client.query(_ch_get_cluster_hosts_query, read_only=False, **extra_params)
    result: Dict[str, Any] = json.loads(body.decode())
    return result["data"]


async def ch_server_is_reachable(database_server: str) -> bool:
    client: HTTPClient = HTTPClient(database_server)
    return await client.ping()


async def ch_server_is_reachable_and_has_cluster(server_url: str, cluster_name: str) -> bool:
    """Validates that clickhouse is reachable on `server_url` and has the cluster `cluster_name`."""

    try:
        ch_hosts_clusters = await ch_get_clusters_hosts_async(server_url)
    except Exception as ex:
        logging.warning(f"Couldn't connect to ClickHouse in {server_url} to get hosts and clusters: {ex}")
        return False
    cluster_found = next((ch["cluster"] for ch in ch_hosts_clusters if ch["cluster"] == cluster_name), None)
    return cluster_found is not None


def ch_get_replicas_for_table_sync(database_server: str, database: str, table_name: str, cluster: str):
    """
    Wait for the cluster to have the data in all replicated tables.
    This is useful when other operations, e.g. OPTIMIZE, depend on the
    availability of the data.
    # TODO Wait only for the leader?
    """
    client = HTTPClient(database_server, database=database)
    sql = f"""
    SELECT
        *
    FROM
        clusterAllReplicas('{cluster}', view(
            SELECT host_address, getServerPort('http_port') as http_port
            FROM system.clusters
            WHERE
                cluster = '{cluster}' AND
                is_local AND
                (SELECT count() FROM system.tables WHERE database = '{database}' AND table = '{table_name}') = 1
        ))
    FORMAT JSON
    """
    _, body = client.query_sync(sql)
    return [url_from_host(x["host_address"], port=x["http_port"]) for x in json.loads(body)["data"]]


def _ch_get_cluster_instances_query(cluster: str) -> str:
    return f"""
    SELECT
        *
    FROM
        clusterAllReplicas('{cluster}', view(
            SELECT host_address, getServerPort('http_port') as http_port, cluster
            FROM system.clusters
            WHERE cluster = '{cluster}' AND is_local
        ))
    FORMAT JSON
    """


async def ch_get_cluster_instances(database_server: str, database: Optional[str] = None, cluster: str = "", **kwargs):
    client = HTTPClient(database_server, database=database)
    _, body = await client.query(_ch_get_cluster_instances_query(cluster), **kwargs)
    return [(url_from_host(x["host_address"], port=x["http_port"]), x["cluster"]) for x in json.loads(body)["data"]]


def ch_get_cluster_instances_sync(
    database_server: str, database: Optional[str] = None, filter_by_cluster: str = "", **kwargs
):
    client = HTTPClient(database_server, database=database)
    _, body = client.query_sync(_ch_get_cluster_instances_query(filter_by_cluster), **kwargs)
    return [(url_from_host(x["host_address"], port=x["http_port"]), x["cluster"]) for x in json.loads(body)["data"]]


def is_table_engine_replicated(client: "HTTPClient", database: str, table_name: str, **extra_params: Any) -> bool:
    try:
        sql = f"""
            SELECT engine from system.tables
            WHERE database = '{database}'
            AND name = '{table_name}'
            FORMAT JSON
            """
        _, body = client.query_sync(sql, max_execution_time=3, **extra_params)
        rows = json.loads(body)["data"]
        return bool(len(rows) and "Replicated" in rows[0]["engine"])
    except Exception as e:
        logging.error(f"Error checking if table {database}.{table_name} is replicated: {e}")
        return False


class CHReplication:
    @staticmethod
    def ch_wait_for_replication_sync(
        database_server: str,
        cluster: Optional[str],
        database: str,
        table_name: str,
        wait: int = 180,
        debug: bool = True,
        wait_for_merges: bool = False,
        **extra_params: Any,
    ) -> bool:
        """
        Wait for the cluster to have the data in all replicated tables.
        This is useful when other operations, e.g. OPTIMIZE, depend on the
        availability of the data.
        # TODO Wait only for the leader?
        """

        client = HTTPClient(database_server, database=database)
        sql = f"""
            SELECT zookeeper_path
            FROM system.replicas
            WHERE database = '{database}' AND table = '{table_name}'
            FORMAT JSON
        """
        _, body = client.query_sync(sql, **extra_params)
        rows = json.loads(body)["data"]
        if not rows:
            if is_table_engine_replicated(client, database, table_name):
                logging.warning(f"No rows when checking replication status: {database}.{table_name}")
                return False
            else:
                logging.warning(f"Not replicated: {database}.{table_name}")
                return True

        zoo_path = rows[0]["zookeeper_path"]

        sql = f"""
            SELECT name
            FROM system.zookeeper
            WHERE path = '{zoo_path}/replicas'
            FORMAT JSON
        """
        _, body = client.query_sync(sql)
        names = [x["name"] for x in json.loads(body)["data"]]

        replica_count = len(names)
        if replica_count <= 1:
            if debug:
                logging.info(f"[REPLICATION] ({database}.{table_name}) NO NEED TO WAIT. ONLY {replica_count} REPLICA")
            return True

        # we should wait for items in the queue that are not merges as default action
        # but there are some cases where we do want to wait for them to finish, for exameple
        # before running any operation that force a merge (like an OPTIMIZE)
        wait_for_merges_condition = """and value not like '%block_id: \\nmerge%'"""
        if wait_for_merges:
            wait_for_merges_condition = ""

        subqueries = "UNION ALL".join(
            [
                f"""
            SELECT
                '{name}' as replica,
                count() c
            FROM system.zookeeper
            WHERE path = '{zoo_path}/replicas/{name}/queue'
            {wait_for_merges_condition}
        """
                for name in names
            ]
        )
        sql = f"""
        SELECT
            sum(c) as queue_length,
            groupArrayIf((replica, c), c > 0) as missing_replicas
        FROM ({subqueries}) FORMAT JSON"""
        i = 1
        while True:
            try:
                _, body = client.query_sync(sql, **extra_params)
            except Exception as e:
                logging.exception(f"Failed to check replicas queue status: {e}")
                raise RuntimeError(f"Could not determine replication status for table '{table_name}'")

            results = json.loads(body)["data"][0]
            queue_length = int(results["queue_length"])
            missing_replicas = results["missing_replicas"]
            if queue_length == 0:
                if debug:
                    logging.info(
                        f"[REPLICATION] ({database}.{table_name}) AWAITED SUCCESSFULLY. ATTEMPT={i}. REPLICAS={replica_count}"
                    )
                return True
            if i >= wait:
                if debug:
                    logging.exception(
                        f"[REPLICATION] ({database}.{table_name}) FAILED TO WAIT. ATTEMPT={i}. REPLICAS={replica_count}. MISSING REPLICAS={missing_replicas}"
                    )
                return False
            if debug:
                logging.info(
                    f"[REPLICATION] ({database}.{table_name}) WAITING. ATTEMPT={i}. REPLICAS={replica_count}. MISSING REPLICAS={missing_replicas}"
                )
            i += 1
            time.sleep(1)


async def ch_get_replicas_with_problems_per_cluster_host(database_server: str = "localhost", **kwchecks):
    client = HTTPClient(database_server)
    replicas: Dict[str, Any] = defaultdict(list)
    try:
        _, body = await client.query(
            "SELECT DISTINCT host_address as host_address, cluster, hostName() as host_name FROM system.clusters ORDER BY is_local DESC FORMAT JSON"
        )
        clusters = json.loads(body)["data"]
        host_addresses: List[str] = [c["host_address"] for c in clusters]
        if not host_addresses:
            return replicas
        _, body = await client.query(
            f"""SELECT cluster, host_address, hostName() AS host_name
            FROM remote('{','.join(host_addresses)}', system.clusters)
            WHERE is_local
            FORMAT JSON"""
        )
        result = json.loads(body)["data"]
        if not result:
            result = [
                {
                    "host_name": clusters[0]["host_name"],
                    "cluster": clusters[0]["cluster"],
                    "host_address": clusters[0]["host_address"],
                }
            ]
        host_name_to_cluster: Dict[str, str] = {c["host_name"]: c["cluster"] for c in result}
        host_name_to_address: Dict[str, str] = {c["host_name"]: c["host_address"] for c in result}
        query = f"""
            SELECT
                hostName() as host_name,
                database,
                table,
                is_leader,
                is_readonly,
                is_session_expired,
                future_parts,
                parts_to_check,
                queue_size,
                inserts_in_queue,
                merges_in_queue,
                part_mutations_in_queue,
                absolute_delay
            FROM remote('{','.join(host_name_to_address.values())}', system.replicas)
            WHERE
                is_readonly
                OR is_session_expired
                OR future_parts > {kwchecks.get('future_parts', 20)}
                OR parts_to_check > {kwchecks.get('parts_to_check', 10)}
                OR queue_size > {kwchecks.get('queue_size', 100)}
                OR inserts_in_queue > {kwchecks.get('inserts_in_queue', 50)}
                OR merges_in_queue > {kwchecks.get('merges_in_queue', 50)}
                OR absolute_delay > {kwchecks.get('absolute_delay', 30)}
            FORMAT JSON
        """
        _, body = await client.query(query)
        result = json.loads(body)["data"]
        for r in result:
            r["cluster"] = host_name_to_cluster.get(r.get("host_name"))
            replicas[host_name_to_address.get(r.get("host_name"), "")].append(r)
    except Exception as e:
        logging.warning(f"Could not retrieve replicas status: {e}")
    return replicas


async def ch_get_data_from_all_replicas(
    database_server: str,
    cluster: str,
    database: str,
    table_name: str,
    before_from: Optional[str] = None,
    after_from: Optional[str] = None,
):
    client = HTTPClient(database_server)
    before_from = before_from or "*"
    after_from = after_from or ""

    try:
        sql = f"""
            SELECT
                {before_from}
            FROM
                (
                    SELECT
                        distinct *
                    FROM clusterAllReplicas(
                        '{cluster}',
                        '{database}.{table_name}'
                    )
                )
            {after_from}
            FORMAT JSON
        """
        _, body = await client.query(sql)
        return json.loads(body)
    except Exception as e:
        logging.exception(f"Failed to get data from all replicas: {e}")
        raise RuntimeError(f"Could not get data from all replicas for table '{table_name}'")


async def ch_get_zookeeper_paths_for_cluster_host(database_server: str, cluster_host: str) -> List[str]:
    sql = f"""
        SELECT DISTINCT
            zookeeper_path
        FROM remote('{cluster_host}', system.replicas)
    """
    client = HTTPClient(database_server)
    zookeeper_paths = set()

    try:
        _, body = await client.query(f"{sql} FORMAT JSON")
        data = list(map(lambda x: x["zookeeper_path"], json.loads(body)["data"]))
        zookeeper_paths.update(data)
    except Exception:
        pass

    return list(zookeeper_paths)


async def ch_get_zookeeper_replicas_with_problems(database_server: str = "localhost"):
    def get_zookeeper_replicas(zookeeper_path: str, cluster_names: List[str]) -> str:
        return f"""
            SELECT
                name,
                path
            FROM system.zookeeper
            WHERE path = '{zookeeper_path}/replicas'
            AND name NOT IN {cluster_names}
        """

    cluster_hosts: List[str] = []
    cluster_names: List[str] = []

    client = HTTPClient(database_server)

    try:
        _, body = await client.query(
            "SELECT DISTINCT host_address as cluster_host, host_name as cluster_name FROM system.clusters FORMAT JSON"
        )
        cluster_hosts = list(map(lambda x: x["cluster_host"], json.loads(body)["data"]))
        cluster_names = list(map(lambda x: x["cluster_name"], json.loads(body)["data"]))
    except Exception:
        pass

    zookeeper_paths = set()

    for cluster_host in cluster_hosts:
        cluster_host_zookeeper = await ch_get_zookeeper_paths_for_cluster_host(database_server, cluster_host)
        zookeeper_paths.update(cluster_host_zookeeper)

    zookeeper_paths_replicas_query = "UNION ALL".join(
        [get_zookeeper_replicas(zookeeper_path, cluster_names) for zookeeper_path in list(zookeeper_paths)]
    )
    zookeeper_replicas = []

    try:
        _, body = await client.query(f"SELECT * FROM ({zookeeper_paths_replicas_query}) FORMAT JSON")
        zookeeper_replicas = json.loads(body)["data"]
    except Exception:
        pass

    return zookeeper_replicas


def _get_command_wait_for_mutations(
    command: Optional[str], cluster: Optional[str], database: str, table_name: str
) -> str:
    command_sql = f"AND command = '{format_where_for_mutation_command(command)}'" if command else "AND 1=1"
    sql = f"""
        SELECT count() as pending_mutations
        FROM {f"clusterAllReplicas({cluster}, system.mutations)" if cluster else "system.mutations"}
        WHERE
            database = '{database}'
            AND table = '{table_name}'
            AND NOT is_done
            {command_sql}
        FORMAT JSON
    """
    return sql


def _check_pending_mutations(body, table_name, max_wait_attemps, attemp) -> Optional[bool]:
    pending_mutations = int(json.loads(body)["data"][0]["pending_mutations"])
    if pending_mutations == 0:
        logging.info(
            f"[{table_name}] Mutations finished successfully: MUTATIONS LENGTH={pending_mutations}; ATTEMPT={attemp}; PENDING ATTEMPTS={max_wait_attemps - attemp}"
        )
        return True
    if attemp == max_wait_attemps:
        logging.exception(
            f"[{table_name}] Failed to wait for mutations: MUTATIONS LENGTH={pending_mutations}; ATTEMPT={attemp}; PENDING ATTEMPTS={max_wait_attemps - attemp}"
        )
        return False
    logging.debug(
        f"[{table_name}] Waiting for mutations: MUTATIONS LENGTH={pending_mutations}; ATTEMPT={attemp}; PENDING ATTEMPTS={max_wait_attemps - attemp}"
    )
    return None


def ch_wait_for_mutations_sync(
    database_server: str,
    database: str,
    table_name: str,
    command: Optional[str] = None,
    max_mutations_seconds_to_wait: Optional[int] = None,
    cluster: Optional[str] = None,
    skip_unavailable_replicas: bool = False,
    **extra_params: Any,
) -> bool:
    client = HTTPClient(database_server, database=database)
    sql = _get_command_wait_for_mutations(command, cluster, database, table_name)

    i = 1
    wait = max_mutations_seconds_to_wait or MAX_MUTATIONS_SECONDS_TO_WAIT
    extra_params = {**extra_params, "skip_unavailable_shards": int(skip_unavailable_replicas)}
    while True:
        try:
            _, body = client.query_sync(sql, **extra_params)
        except Exception as e:
            logging.exception(f"Failed to check mutations status: {e}")
            raise RuntimeError(f"Could not determine mutation status for table '{table_name}'")
        result = _check_pending_mutations(body, table_name, wait, i)
        if result is not None:
            return result
        i += 1
        time.sleep(1)


async def ch_wait_for_mutations(
    database_server: str,
    database: str,
    table_name: str,
    command: Optional[str] = None,
    max_mutations_seconds_to_wait: Optional[int] = None,
    cluster: Optional[str] = None,
    skip_unavailable_replicas: bool = False,
) -> bool:
    client = HTTPClient(database_server, database=database)
    sql = _get_command_wait_for_mutations(command, cluster, database, table_name)
    i = 1
    wait = max_mutations_seconds_to_wait or MAX_MUTATIONS_SECONDS_TO_WAIT
    extra_params: Dict[str, Any] = {"skip_unavailable_shards": int(skip_unavailable_replicas)}
    while True:
        try:
            _, body = await client.query(sql, **extra_params)
        except Exception as e:
            logging.exception(f"Failed to check mutations status: {e}")
            raise RuntimeError(f"Could not determine mutation status for table '{table_name}'")
        result = _check_pending_mutations(body, table_name, wait, i)
        if result is not None:
            return result
        i += 1
        await asyncio.sleep(1)


async def ch_row_count(
    database_server: str,
    database: str,
    table_name: str,
    condition: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> int:
    client = HTTPClient(database_server, database=database)
    sql = f"""
        SELECT count() as c
        FROM {database}.{table_name}
        WHERE {condition if condition else '1=1'}
        FORMAT JSON
    """
    _, body = await client.query(sql, read_only=True, max_execution_time=3, user_agent=user_agent)
    rows = orjson.loads(body)["data"]
    return rows[0]["c"]


def ch_row_count_sync(
    database_server: str,
    database: str,
    table_name: str,
    condition: Optional[str] = None,
    user_agent: Optional[str] = UserAgents.INTERNAL_QUERY.value,
    max_execution_time: int = 3,
) -> int:
    client = HTTPClient(database_server, database=database)
    sql = f"""
        SELECT count() as c
        FROM {database}.{table_name}
        WHERE {condition if condition else '1=1'}
        FORMAT JSON
    """
    _, body = client.query_sync(sql, read_only=True, max_execution_time=max_execution_time, user_agent=user_agent)
    rows = orjson.loads(body)["data"]
    return rows[0]["c"]


async def rows_affected_by_delete(workspace: "User", table_name: str, delete_condition: str) -> int:
    return await ch_row_count(
        workspace.database_server, workspace.database, table_name, delete_condition, user_agent=UserAgents.DELETE.value
    )


def rows_affected_by_delete_sync(workspace: "User", table_name: str, delete_condition: str) -> int:
    return ch_row_count_sync(
        workspace.database_server,
        workspace.database,
        table_name,
        delete_condition,
        user_agent=UserAgents.DELETE.value,
        max_execution_time=MAX_EXECUTION_TIME,
    )


# Note that this function assumes the delete_condition has been validated and replaced
# Currently done in validate_and_init_datasource_delete
def ch_delete_condition_sync(
    database_server: str,
    database: str,
    table_name: str,
    delete_condition: str,
    cluster: Optional[str] = None,
    wait_replicas: int = MUTATIONS_SYNC_WAIT_REPLICAS,
    extra_params: Optional[dict] = None,
):
    cluster_clause = f"ON CLUSTER {cluster}" if cluster else ""
    sql = f"""
        ALTER TABLE {database}.{table_name}
        {cluster_clause}
        DELETE WHERE {delete_condition}
    """
    return ch_guarded_query(
        database_server,
        database,
        sql,
        cluster,
        max_execution_time=MAX_DELETE_CONDITION_EXECUTION_TIME,
        mutations_sync=wait_replicas,
        user_agent=UserAgents.DELETE.value,
        **(extra_params or {}),
    )


def table_stats(table_name: str, database_server: str = "localhost", database: str = "default") -> Dict[str, Any]:
    client = HTTPClient(database_server, database=database)
    sql = f"""
    SELECT
        sum(bytes) bytes, sum(rows) row_count
    FROM system.parts
    WHERE
        database = '{database}'
        AND table = '{table_name}'
        AND active
    """
    _, body = client.query_sync(sql + " format JSON")
    data: List[Dict[str, Any]] = json.loads(body)["data"]
    return data[0]


def ch_get_tables_stats(tables_ids: List[str], database_server: str = "localhost", database: str = "default"):
    client = HTTPClient(database_server, database=database)
    sql = f"""
        SELECT
            name as id,
            total_bytes as bytes,
            total_rows as row_count
        FROM system.tables
        WHERE
            database = '{database}' and name in {tables_ids}
        """
    data = []

    _, body = client.query_sync(sql + " format JSON")

    try:
        data = json.loads(body)["data"]
    except Exception:
        pass

    return data


def ch_get_tables_metadata_sync(
    database_servers: Iterable[Tuple[str, str]],
    avoid_database_names: Tuple = ("system", "default"),
    database_names: Optional[Tuple] = (),
    only_materialized=False,
):
    ch_tables: Dict[Any, Any] = {}

    for server, cluster in database_servers:
        try:
            database_names_sql = f"and database in {database_names}" if database_names else ""
            only_materialized_sql = " and engine = 'MaterializedView' " if only_materialized else ""
            query_table = f"clusterAllReplicas('{cluster}', system.tables)" if cluster else "system.tables"
            query = f"""
            SELECT
                count() as count,
                database,
                name,
                engine,
                max(metadata_modification_time) as mtime,
                if(engine like '%MergeTree', formatReadableSize(max(total_bytes)), '-') disk_usage
            FROM {query_table}
            WHERE
                database not in {avoid_database_names} AND engine not in ('View')
                {database_names_sql}
                {only_materialized_sql}
            GROUP BY database, name, engine
            ORDER BY max(total_bytes) DESC
            FORMAT JSON
            """
            client = HTTPClient(server)
            _, body = client.query_sync(query)
            result = json.loads(body)
            ch_tables = {
                **ch_tables,
                **{
                    (t["database"], t["name"]): (t["engine"], t["disk_usage"], t["mtime"], server, t["count"], cluster)
                    for t in result["data"]
                },
            }
        except Exception as e:
            logging.error(f"Failed to get tables metadata from {server}: {e}")
            continue
    return ch_tables


async def ch_get_tables_metadata(
    database_servers: Iterable[Tuple[str, str]],
    avoid_database_names: Tuple = ("public", "system", "default"),
    filter_engines: Tuple = ("View",),
    database_names: Optional[Tuple] = (),
    only_materialized: bool = False,
):
    ch_tables: Dict[Any, Any] = {}

    avoid_database_names_query = f"""('{"','".join(avoid_database_names)}')"""
    filter_engines_query = f"""('{"','".join(filter_engines)}')"""

    for server, cluster in database_servers:
        database_names_sql = f"and database in {database_names}" if database_names else ""
        only_materialized_sql = " and engine = 'MaterializedView' " if only_materialized else ""
        query_table = f"clusterAllReplicas('{cluster}', system.tables)" if cluster else "system.tables"
        query = f"""
        SELECT
            count() as count,
            database,
            name,
            engine,
            max(metadata_modification_time) as mtime
        FROM {query_table}
        WHERE
            database not in {avoid_database_names_query} AND engine not in {filter_engines_query}
            {database_names_sql}
            {only_materialized_sql}
        GROUP BY database, name, engine
        FORMAT JSON
        """

        try:
            client = HTTPClient(server)
            _, body = await client.query(query)
            result = json.loads(body)
            ch_tables = {
                **ch_tables,
                **{
                    (t["database"], t["name"]): (t["engine"], t["mtime"], server, t["count"], cluster)
                    for t in result["data"]
                },
            }
        except Exception as e:
            logging.warning(f"Could not get tables metadata information for server {server} on cluster {cluster}: {e}")

    return ch_tables


async def ch_get_databases_metadata(
    database_servers: Iterable[Tuple[str, Optional[str]]],
    avoid_database_names: Tuple = ("public", "system", "default"),
    skip_unavailable_replicas: bool = True,
) -> Dict[str, List[str]]:
    ch_databases: Dict[str, List[str]] = {}

    avoid_database_names_query = f"""('{"','".join(avoid_database_names)}')"""
    extra_params: Dict = {}
    if skip_unavailable_replicas:
        extra_params = {"skip_unavailable_shards": 1}

    for server, cluster in database_servers:
        query_table = f"clusterAllReplicas('{cluster}', system.databases)" if cluster else "system.databases"
        query = f"""
        SELECT
            name,
        FROM {query_table}
        WHERE
            name not in {avoid_database_names_query}
        FORMAT JSON
        """

        try:
            client = HTTPClient(server)
            _, body = await client.query(query, **extra_params)
            result = json.loads(body)
            if cluster:
                if cluster not in ch_databases:
                    ch_databases[cluster] = []
                ch_databases[cluster] += [t["name"] for t in result["data"]]
            else:
                if server not in ch_databases:
                    ch_databases[server] = []
                ch_databases[server] += [t["name"] for t in result["data"]]
        except Exception as e:
            logging.warning(
                f"Could not get databases metadata information for server {server} on cluster {cluster}: {e}"
            )

    return ch_databases


def host_port_from_url(url: str) -> Tuple[str, int]:
    """
    >>> host_port_from_url('http://localhost')
    ('localhost', 8123)
    >>> host_port_from_url('http://127.0.0.1:1234')
    ('127.0.0.1', 1234)
    >>> host_port_from_url('192.168.1.160:8125')
    ('192.168.1.160', 8125)
    """
    p = urlparse(url)
    netloc = p.netloc if len(p.netloc) else url
    split_port = netloc.split(":")
    http_host = split_port[0]
    http_port = 0
    if len(split_port) > 1:
        http_port = int(split_port[1])

    if http_port == 0:
        http_port = 8123

    return http_host, http_port


def url_from_host(host: str, port: str = "8123") -> str:
    """
    >>> url_from_host('localhost')
    'http://localhost:8123/'
    >>> url_from_host(host='http://1.2.3.4:8888/')
    'http://1.2.3.4:8888/'
    >>> url_from_host('http://1.2.3.4:8888')
    'http://1.2.3.4:8888/'
    >>> url_from_host('1.2.3.4:8888')
    'http://1.2.3.4:8888/'
    """
    h = urlparse(host)
    if h.scheme in ("http", "https"):
        if host[-1] != "/":
            return host + "/"
        return host
    if ":" in host:
        host, port = host.split(":")
    return HTTPClient.SERVER_URL % (host, port)


@dataclass
class CacheConfig:
    """Defines the cache key and ttl for a request"""

    key: str
    ttl: Optional[str]


class HTTPClient:
    SERVER_URL: str = "http://%s:%s/"
    # Above this query length we will never use GET and instead use POST and pass the query in the body
    MAX_GET_LENGTH: int = 4096
    DEFAULT_RETRY_COUNT: int = 5
    DEFAULT_BACKOFF: float = 0.2
    DEFAULT_RETRY_ON_STATUS: List[int] = [502, 503, 504]

    def __repr__(self) -> str:
        return f"HTTPClient(host='{self.host}', database='{self.database}')"

    def __init__(self, host: str = "localhost", database: Optional[str] = None, url: Optional[str] = None) -> None:
        self.host: str = host
        self.database: str = database if database else "default"
        self.url: Optional[str] = url
        self._session: Optional[Session] = None
        self._no_retry_session: Optional[Session] = None
        self._http_client: Optional[AsyncHTTPClient] = None

    def __del__(self):
        if self._session:
            self._session.close()

    def get_session(self, use_default_retry_policy: bool = True) -> Session:
        if use_default_retry_policy:
            if self._session is None:
                self._session = requests.Session()
                retries = Retry(
                    total=HTTPClient.DEFAULT_RETRY_COUNT,
                    backoff_factor=HTTPClient.DEFAULT_BACKOFF,
                    status_forcelist=HTTPClient.DEFAULT_RETRY_ON_STATUS,
                )
                self._session.mount("http://", HTTPAdapter(max_retries=retries))
            return self._session
        else:
            if self._no_retry_session is None:
                self._no_retry_session = requests.Session()
                self._no_retry_session.mount("http://", HTTPAdapter(max_retries=0))
            return self._no_retry_session

    @property
    def session(
        self,
    ) -> Session:
        return self.get_session(True)

    @property
    def http_client(self):
        if not self._http_client:
            self._http_client = AsyncHTTPClient(defaults=dict(request_timeout=3600.0))
        return self._http_client

    @property
    def endpoint(self) -> str:
        """
        >>> c = HTTPClient()
        >>> c.endpoint
        'http://localhost:8123/'
        >>> c = HTTPClient(host='http://1.2.3.4:8888/')
        >>> c.endpoint
        'http://1.2.3.4:8888/'
        >>> c = HTTPClient(host='http://1.2.3.4:8888')
        >>> c.endpoint
        'http://1.2.3.4:8888/'
        """
        if self.url:
            return self.url
        return url_from_host(self.host)

    def get_params(
        self,
        q: str,
        method="GET",
        query_id: Optional[str] = None,
        extra_params: Optional[Dict[str, Any]] = None,
        user_agent: Optional[str] = None,
    ):
        """
        >>> params, body = HTTPClient().get_params('', extra_params={'max_execution_time': 30})
        >>> params['max_execution_time']
        30
        >>> params['lock_acquire_timeout']
        30
        >>> params, body = HTTPClient().get_params('', extra_params={'max_execution_time': None})
        >>> params['max_execution_time']
        10

        """

        if not query_id:
            query_id = ulid.new().str

        if not extra_params:
            extra_params = {}
        DEFAULT_LOCK_ACQUIRE_TIMEOUT = 120
        if extra_params.get("max_execution_time", None) is None:
            extra_params["max_execution_time"] = (
                MAX_EXECUTION_TIME  # seconds, it's overridden by `chunk_max_execution_time` limit in the user model when used from `insert_chunk`
            )

        bypass_cache = 1
        if user_agent == UserAgents.API_QUERY.value:
            bypass_cache = 0

        params = {
            "database": self.database,
            "query_id": query_id,
            "query": q,
            "max_result_bytes": 100 * 1024 * 1024,  # 100 megabytes
            "log_queries": 1,
            "optimize_throw_if_noop": 1,
            "output_format_json_quote_64bit_integers": 0,
            "lock_acquire_timeout": min(DEFAULT_LOCK_ACQUIRE_TIMEOUT, extra_params["max_execution_time"]),
            # Allow to read from cache filesystem but bypass writing non existing keys
            # This way the filesystem cache won't get filled when running one time queries
            # such as populates, UI queries, copies, replaces, etc.
            "read_from_filesystem_cache_if_exists_otherwise_bypass_cache": bypass_cache,
            # Change HTTP to wait until the query finishes to reply
            # It is done so CH doesn't start streaming data before as it causes 2 main problems: statistics aren't
            # available in the request and errors which happened at runtime won't be reported in the HTTP Status
            # and instead they will appear at the end of the body. This happens because CH needs to finish writting
            # the HTTP headers before it can start sending the body, so to stream data it inserts the default headers
            "wait_end_of_query": 1,
            # At most 100 megabytes of response will be buffered in memory.
            # The rest will be buffered TO DISK ( http_buffers/ under CH temp folder )
            # Note that CH will throw when the result reaches "max_result_bytes" so it shouldn't cache GBs of data
            # unless we are allowing GBs of result in max_result_bytes
            "buffer_size": 100 * 1024 * 1024,
        }

        params = {**params, **extra_params}
        body = None
        if method == "POST":
            body = params["query"]
            del params["query"]
        return params, body

    def insert_chunk(
        self,
        query: str,
        chunk,
        dialect: Optional[Dict[str, Any]] = None,
        max_execution_time: int = MAX_EXECUTION_TIME,
        query_id: Optional[str] = None,
        log_as_error=True,
        user_agent: Optional[str] = None,
        extra_params: Optional[Dict[str, Any]] = None,
    ):
        headers = {
            "User-Agent": user_agent if user_agent is not None else "tb-insert-chunk",
        }
        delimiter = "," if not dialect else dialect.get("delimiter", ",")
        max_execution_time = max_execution_time or MAX_EXECUTION_TIME

        extra_params = {
            "format_csv_delimiter": delimiter,
            "input_format_defaults_for_omitted_fields": 1,
            "max_execution_time": max_execution_time,
            "query_id": query_id if query_id else ulid.new().str,
            **(extra_params or {}),
        }
        params, _ = self.get_params(
            query, method="GET", extra_params=extra_params, user_agent=user_agent
        )  # use get to avoid using the body to send the query

        # TODO: use a different session for writing, if for any reason CH is overloaded
        # it will try to rewrite too soon overloading it more
        try:
            r = self.session.request(url=self.endpoint, method="POST", params=params, data=chunk, headers=headers)
        except UnicodeEncodeError:
            # Sometimes http.client can't decode our `chunk` using latin-1 because it contains unexpected chars (like \u2018)
            # If that's the case, we retry encoding the chunk as utf-8
            r = self.session.request(
                url=self.endpoint, method="POST", params=params, data=chunk.encode("utf-8"), headers=headers
            )

        if r.status_code >= 400:
            # log here the error, when working with varnish the response could be totally different to what
            # CH reports and therefore the CHException parsing will not work
            err_msg = f"insert chunk failed {len(chunk)} in clickhouse: {r.status_code}, {r.headers} {r.content.decode('utf-8')}"
            if log_as_error:
                logging.exception(err_msg)
            else:
                logging.warning(err_msg)
            raise CHException(r.text or r.content.decode("utf-8"), headers=r.headers)

        return r.headers, r.content

    def query_sync(
        self,
        q: str,
        query_id: Optional[str] = None,
        read_cluster: bool = False,
        backend_hint: Optional[str] = None,
        read_only: bool = True,
        timeout: Optional[float] = None,
        user_agent: Optional[str] = None,
        fallback_user_auth: bool = False,
        disable_upstream_fallback: Optional[bool] = False,
        retries: bool = True,
        **extra_params: Any,
    ) -> Tuple[HTTPHeaders, bytes]:
        method = "GET"
        if len(q) > HTTPClient.MAX_GET_LENGTH and read_only:
            extra_params.update({"readonly": 2})
            method = "POST"
        if not read_only:
            method = "POST"

        headers = {
            "User-Agent": user_agent if user_agent is not None else UserAgents.INTERNAL_QUERY.value,
        }
        if read_cluster:
            headers["X-TB-Read-Cluster"] = "true"
        if backend_hint:
            headers["X-TB-Backend-Hint"] = backend_hint

        # Add default backend_hint to write queries. It's a way to prevent queries from Analytics to go to different writers
        # This is something temporary until we change all processes that require single writer (populates, replaces, copy, etc)
        # to send a proper backend_hint to avoid going to different writers by themselves
        if not read_cluster and not backend_hint:
            headers["X-TB-Backend-Hint"] = "SINGLE_WRITER_HINT"

        if disable_upstream_fallback:
            headers["X-TB-Disable-Fallback"] = "true"

        def perform_request(session: Session, query_id: str) -> Response:
            """Performs a request using the passed Session and query_id."""

            params, body = self.get_params(
                q, method=method, query_id=query_id, extra_params=extra_params, user_agent=user_agent
            )
            req_timeout = (
                Limit.requests_connect_timeout,
                min(timeout or Limit.requests_bytes_between_timeout, int(params["max_execution_time"]) + 1),
            )

            r: Response = session.request(
                url=self.endpoint, method=method, params=params, data=body, headers=headers, timeout=req_timeout
            )

            return r

        if query_id:
            # Use the default retry policy for this request
            r = perform_request(self.get_session(use_default_retry_policy=retries), query_id=query_id)
        else:
            # Implement the retry logic in order to being able to regenerate the query_id in each attempt.
            for i in range(HTTPClient.DEFAULT_RETRY_COUNT):
                request_status = None
                try:
                    query_id = ulid.new().str
                    r = perform_request(self.get_session(use_default_retry_policy=False), query_id=query_id)
                    request_status = r.status_code
                    if request_status not in HTTPClient.DEFAULT_RETRY_ON_STATUS or not retries:
                        break

                except (ConnectionError, RequestException) as ex:
                    # It was the last chance. Bubble up the exception
                    if i == HTTPClient.DEFAULT_RETRY_COUNT - 1 or not retries:
                        raise ex

                logging.warning(
                    f"Retrying query_id={query_id} method={method} status={request_status} read_only={read_only} in {self.host}. Try {i + 2}/{HTTPClient.DEFAULT_RETRY_COUNT}"
                )
                if i > 0:  # Add a delay after the second try (just like urllib)
                    time.sleep(HTTPClient.DEFAULT_BACKOFF * (2**i))

        if r.status_code >= 400:
            exception = CHException(r.text or r.content.decode(), headers=r.headers)

            if (
                exception.code in [CHErrors.UNKNOWN_USER, CHErrors.AUTHENTICATION_FAILED]
                and extra_params.get("user")
                and fallback_user_auth
            ):
                logging.exception(f"ClickHouse Profile Error (user {extra_params.get('user')}): {exception}")

                # Retry without user settings
                del extra_params["user"]

                return self.query_sync(
                    q=q,
                    query_id=query_id,
                    read_only=read_only,
                    timeout=timeout,
                    user_agent=user_agent,
                    fallback_user_auth=False,
                    **extra_params,
                )
            else:
                raise exception
        return r.headers, r.content

    async def query(
        self,
        q: str,
        query_id: Optional[str] = None,
        compress: bool = False,
        read_cluster: bool = False,
        backend_hint: Optional[str] = None,
        read_only: bool = True,
        user_agent: Optional[str] = None,
        cache_config: Optional[CacheConfig] = None,
        cluster: Optional[str] = None,
        fallback_user_auth: bool = False,
        **extra_params: Any,
    ) -> Tuple[HTTPHeaders, bytes]:
        method = "GET"
        if len(q) > HTTPClient.MAX_GET_LENGTH and read_only:
            extra_params.update({"readonly": 2})
            method = "POST"
        if not read_only:
            method = "POST"

        headers = {
            "User-Agent": user_agent if user_agent is not None else UserAgents.INTERNAL_QUERY.value,
        }
        if compress:
            headers["Accept-Encoding"] = "gzip"
            extra_params.update({"enable_http_compression": 1})
        if read_cluster:
            headers["X-TB-Read-Cluster"] = "true"
            if backend_hint:
                headers["X-TB-Backend-Hint"] = backend_hint
            if cache_config and cache_config.ttl:
                headers["X-TB-Read-Cache-Key"] = cache_config.key
                headers["X-TB-Read-Cache-TTL"] = cache_config.ttl

        # Add default backend_hint to write queries. It's a way to prevent queries from Analytics to go to different writers
        # This is something temporary until we change all processes that require single writer (populates, replaces, copy, etc)
        # to send a proper backend_hint to avoid going to different writers by themselves
        if not read_cluster and not backend_hint:
            headers["X-TB-Backend-Hint"] = "SINGLE_WRITER_HINT"

        params, body = self.get_params(
            q, method=method, query_id=query_id, extra_params=extra_params, user_agent=user_agent
        )
        url = url_concat(self.endpoint, params)

        response_headers: HTTPHeaders
        debug_read_buffer = False

        try:
            # Add an extra second so CH has time to reply on timeouts
            http_timeout = int(params["max_execution_time"]) + 1
            start = time.time()
            response: HTTPResponse = await self.http_client.fetch(
                url, method=method, body=body, headers=headers, decompress_response=False, request_timeout=http_timeout
            )

            # Compress response in Python code, in case CH server could not compress the response with gzip
            body = response.body
            if compress and (
                "Content-Encoding" not in response.headers or response.headers["Content-Encoding"] != "gzip"
            ):
                o = zlib.compressobj(wbits=16 + 15)
                b = BytesIO()
                while True:
                    chunk = response.buffer.read(64 * 1024)
                    debug_read_buffer = True
                    if not chunk:
                        break
                    b.write(o.compress(chunk))
                    await asyncio.sleep(0)
                b.write(o.flush())
                body = b.getvalue()
                response.headers["Content-Encoding"] = "gzip"

            response_headers = response.headers
            response_headers["X-Request-Time"] = response.request_time
            for k, v in response.time_info.items():
                response_headers[f"X-Request-Time-{k}"] = v

            # TODO: check in case of a timeout and depending on the operation if there is an orphan resource
            if params.get("distributed_ddl_output_mode") == DDL_OUTPUT_MODE_NULL_STATUS_ON_TIMEOUT:
                DDLQueryStatusResponse.from_client_response(response_headers, body, query_id)
            return response_headers, body
        except HTTPError as e:
            if "Content-Encoding" in e.response.headers and e.response.headers["Content-Encoding"] == "gzip":
                try:
                    # window size = 16 to be compatible with streamed gzip
                    body = zlib.decompress(e.response.body, wbits=16 + 15)
                except Exception:
                    logging.info(f"DEBUG error response body {e}")
                    logging.info(f"DEBUG error response headers {e.response.headers}")
                    logging.info(f"DEBUG error response body {e.response.body}")
                    logging.info(f"DEBUG read buffer: {debug_read_buffer}")
                    body = e.response.body
            else:
                body = e.response.body

            response_headers = e.response.headers
            target_server = self.host
            if response_headers and "X-ClickHouse-Server-Display-Name" in response_headers:
                target_server = f"{response_headers['X-ClickHouse-Server-Display-Name']}@{self.host}"
            query_description = f"SERVER: {target_server} ID: {params['query_id']} QUERY: `{q[0:80]}`"

            if body:
                exception = CHException(str(body), headers=response_headers)

                if (
                    exception.code in [CHErrors.UNKNOWN_USER, CHErrors.AUTHENTICATION_FAILED]
                    and extra_params.get("user")
                    and fallback_user_auth
                ):
                    logging.exception(f"ClickHouse Profile Error (user {extra_params.get('user')}): {exception}")

                    # Retry without user settings
                    del extra_params["user"]

                    # FIXME
                    return await self.query(
                        q=q,
                        query_id=query_id,
                        compress=compress,
                        read_cluster=read_cluster,
                        backend_hint=backend_hint,
                        read_only=read_only,
                        user_agent=user_agent,
                        cache_config=cache_config,
                        cluster=cluster,
                        fallback_user_auth=False,
                        **extra_params,
                    )
                else:
                    logging.warning(f"ClickHouse Error: {query_description} ERROR: {str(body)}")
                    raise exception

            if e.code == 599 and (time.time() - start) >= http_timeout:
                # We are logging all the time info to help with debugging the issue https://gitlab.com/tinybird/analytics/-/issues/15969
                metrics = [
                    "namelookup",
                    "connect",
                    "appconnect",
                    "pretransfer",
                    "starttransfer",
                    "redirect",
                    "queue",
                    "total",
                ]
                time_info_str = ", ".join(f"{k}: {v}" for k, v in e.response.time_info.items() if k in metrics)
                logging.warning(
                    f"ClickHouse Error (No response): {query_description} - Max execution time: {params['max_execution_time']}s Time info: {time_info_str}"
                )

                ch_exception = CHException(
                    f"Code: {CHErrors.TIMEOUT_EXCEEDED}, e.displayText() = DB::Exception: Timeout exceeded: maximum {params['max_execution_time']} seconds",
                    fatal=False,
                )
                ch_exception.code = CHErrors.TIMEOUT_EXCEEDED
                raise ch_exception from e

            logging.warning(f"ClickHouse Error (Unknown {e.code}): {query_description} ERROR {str(e)}")
            raise CHException(f"Code: {e.code}, DB::Exception: {str(e)}", fatal=True, headers=e.response.headers)

    def replicas_status(self, timeout: float = 0.5) -> Dict[str, int]:
        """
        return replicas status for this host
        """
        # verbose adds status for each table
        url = self.endpoint + "replicas_status?verbose=1"
        try:
            r = requests.get(url=url, timeout=timeout)
            if r.status_code != 200:
                raise Exception(f"can't get replica status {r.content!r} {r.status_code!r}")

            # parse response, format is:
            # table:\tAbsolute delay: <int>. Relative delay: <int>\n
            # table2:\tAbsolute delay: <int>. Relative delay: <int>\n

            table_delay: Dict[str, int] = {}
            for x in r.text.split("\n"):
                m = re.match("(.*):\tAbsolute delay: (\d+)", x)
                if m:
                    table_delay[m.groups()[0]] = int(m.groups()[1])
            return table_delay
        except Exception as e:
            raise Exception(f"can't get replica status {e}")

    async def ping(self) -> bool:
        """
        Check if instance is available
        """

        url = self.endpoint + "ping"

        try:
            response: HTTPResponse = await self.http_client.fetch(url)
            return response.code == 200
        except HTTPError:
            return False


@dataclass
class CHSummary:
    """Track X-Clickhouse-Summary header per query_id"""

    query_id: str
    summary: Dict[str, str]

    def to_dict(self):
        return dataclasses.asdict(self)


def include_ttl_in_replacements(
    replacements: Dict[Union[CHTableLocation, Tuple[str, str]], str],
    view_sql: str,
    default_database: str,
    database_server: str,
    source_table: CHTableLocation,
    target_table,
) -> Dict[Union[CHTableLocation, Tuple[str, str]], str]:
    used_tables: List[Tuple[str, str, str]] = sql_get_used_tables(
        view_sql, raising=False, default_database=default_database, table_functions=False
    )
    res = defaultdict(list)
    for database, table, _ in used_tables:
        if database == source_table.database and table == source_table.table:
            continue
        res[database].append(table)

    for database in res:
        tables = [f"'{table}'" for table in res[database]]
        tables_as_string = f"({','.join(tables)})"
        client = HTTPClient(database_server, database=database)
        try:
            sql = f"""
                SELECT
                    database,
                    name,
                    engine_full
                FROM system.tables
                WHERE database = '{database}' and name IN {tables_as_string}
                FORMAT JSON
            """
            _, body = client.query_sync(sql)
        except CHException:
            return replacements
        rows: List[Dict[str, str]] = json.loads(body).get("data", [])
        for row in rows:
            database = row["database"]
            table = row["name"]
            ttl = ttl_condition_from_engine_full(row["engine_full"])
            if ttl:
                replacements[(database, table)] = f"(SELECT * FROM {database}.{table} WHERE {ttl})"

    return replacements


@dataclass
class Partition:
    partition: str
    table: str
    database: str
    bytes_on_disk: int

    def as_sql(self) -> str:
        return partition_sql(self.partition)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "partition": self.partition,
            "table": self.table,
            "database": self.database,
            "bytes_on_disk": self.bytes_on_disk,
        }


class Partitions:
    def as_sql_list(self, partitions: List[Partition]) -> List[str]:
        partitions_list = [p.as_sql() for p in partitions]
        if any([p for p in partitions_list if isinstance(p, str)]):
            return [p if isinstance(p, str) else f"'{p}'" for p in partitions_list]
        return partitions_list

    def split_by_size(self, partitions: List[Partition], max_bytes: int) -> Tuple[List[Partition], List[Partition]]:
        def is_max_part(p: Partition) -> bool:
            return p.bytes_on_disk >= max_bytes

        t1, t2 = tee(partitions)
        return list(filterfalse(is_max_part, t1)), list(filter(is_max_part, t2))


async def ch_query_table_partitions(
    database_server: str,
    database_names: List[str],
    table_names: Optional[List[str]] = None,
    only_last: Optional[bool] = False,
) -> List[Partition]:
    if only_last:
        sql = f"""
        SELECT partition, table, database, bytes_on_disk
        FROM (
            SELECT table, partition, database, sum(rows) rows, max(modification_time) modification_time, sum(bytes_on_disk) bytes_on_disk
            FROM system.parts
            WHERE
                database IN {database_names}
                {f'AND table in {table_names}' if table_names else ''}
                AND active
            GROUP BY partition, table, database
        ) WHERE rows > 0
        ORDER BY table, modification_time DESC LIMIT 1 BY table FORMAT JSON"""
    else:
        sql = f"""
        SELECT partition, table, database, bytes_on_disk
        FROM (
            SELECT table, partition, database, sum(rows) rows, sum(bytes_on_disk) bytes_on_disk
            FROM system.parts
            WHERE
                database IN {database_names}
                {f'AND table in {table_names}' if table_names else ''}
                AND active
            GROUP BY partition, table, database
        ) WHERE rows > 0 FORMAT JSON"""

    client = HTTPClient(database_server)
    _, result = await client.query(sql)
    table_partitions = json.loads(result).get("data", [])
    partitions = [
        Partition(
            partition=p["partition"], table=p["table"], database=p["database"], bytes_on_disk=int(p["bytes_on_disk"])
        )
        for p in table_partitions
    ]
    return partitions


async def ch_drop_database(
    database_server: str,
    database: str,
    cluster: Optional[str] = None,
    max_execution_time: Optional[int] = None,
    **extra_params: Any,
) -> bytes:
    client = HTTPClient(database_server)
    cluster_clause = f"ON CLUSTER {cluster}" if cluster else ""

    sql = f"DROP DATABASE IF EXISTS {database} {cluster_clause}"
    _, result = await client.query(
        sql,
        read_only=False,
        max_execution_time=max_execution_time,
        max_table_size_to_drop=SKIP_TABLE_SIZE_SAFEGUARD,
        max_partition_size_to_drop=SKIP_PARTITION_SIZE_SAFEGUARD,
        **extra_params,
    )
    return result


def ch_drop_database_sync(
    database_server: str, database: str, cluster: Optional[str] = None, sync: bool = False, **extra_params: Any
) -> bytes:
    client = HTTPClient(database_server)
    cluster_clause = f"ON CLUSTER {cluster}" if cluster else ""
    sync_clause = "SYNC" if sync else ""
    sql = f"DROP DATABASE IF EXISTS {database} {cluster_clause} {sync_clause}"
    _, result = client.query_sync(
        sql,
        read_only=False,
        **extra_params,
        max_table_size_to_drop=SKIP_TABLE_SIZE_SAFEGUARD,
        max_partition_size_to_drop=SKIP_PARTITION_SIZE_SAFEGUARD,
    )
    return result


def ch_truncate_databases_sync(
    database_server: str,
    databases: List[str],
    cluster: Optional[str] = None,
    max_execution_time: Optional[int] = None,
    **extra_params: Any,
):
    tables_query = f"""
        SELECT
            database,
            name
        FROM system.tables
        WHERE
            database IN ('{"','".join(databases)}')
            AND engine LIKE '%MergeTree'
        FORMAT JSON
    """
    client = HTTPClient(database_server)
    _, body = client.query_sync(tables_query)
    tables = json.loads(body).get("data", [])
    cluster_clause = f"ON CLUSTER {cluster}" if cluster else ""
    for table in tables:
        try:
            database = table.get("database")
            table_name = table.get("name")

            sql = f"TRUNCATE TABLE IF EXISTS {database}.{table_name} {cluster_clause}"
            _, result = client.query_sync(
                sql,
                read_only=False,
                max_execution_time=max_execution_time,
                max_table_size_to_drop=SKIP_TABLE_SIZE_SAFEGUARD,
                max_partition_size_to_drop=SKIP_PARTITION_SIZE_SAFEGUARD,
                **extra_params,
            )
        except Exception as e:
            logging.warning(f"Could not truncate table {database}.{table_name}: {e}")
            raise e


async def ch_check_all_mvs_are_empty(
    database_server: str,
    cluster: str,
    query_id: str,
    period: int,
    max_execution_time: Optional[int] = MAX_EXECUTION_TIME,
) -> bool:
    client = HTTPClient(database_server, database=None)
    user_agent = UserAgents.INTERNAL_QUERY.value

    async def make_query():
        sql = f"""SELECT
                    uniqExactIf(view_uuid, exception_code != 0 and written_bytes == 0) as failed_mvs_with_no_written_bytes,
                    uniqExact(view_uuid) as total_mvs
                FROM clusterAllReplicas({cluster}, system.query_views_log)
                WHERE
                    event_date >= yesterday()
                    AND event_time > now() - INTERVAL {period} SECOND
                    AND initial_query_id ='{query_id}' FORMAT JSON"""
        _, body = await client.query(sql, read_only=True, user_agent=user_agent, max_execution_time=max_execution_time)
        data = json.loads(body).get("data", [])
        if len(data) == 0:
            return False
        result = data[0]

        if "total_mvs" not in result or "failed_mvs_with_no_written_bytes" not in result:
            return False

        # Since this method is used to know whether a Null engine has lost all data,
        # this may happen both if all MVs have failed or if there is are MV at all.
        return result["failed_mvs_with_no_written_bytes"] == result["total_mvs"]

    await ch_flush_logs_on_all_replicas(database_server, cluster, user_agent)
    return await make_query()


def parse_partition_expression(partition: str):
    """
    >>> parse_partition_expression("tuple()")
    'PARTITION tuple()'
    >>> parse_partition_expression("'whatever'")
    "PARTITION 'whatever'"
    >>> parse_partition_expression("whatever")
    "PARTITION 'whatever'"
    >>> parse_partition_expression("('1234',3)")
    "PARTITION tuple('1234',3)"
    """

    if partition.startswith("("):
        partition = f"tuple{partition}"
    elif "tuple()" in partition:
        partition = "tuple()"
    elif not partition.startswith("'"):
        partition = f"'{partition}'"
    return f"PARTITION {partition}"


def ch_move_partitions_to_disk_sync(
    populate_databases_mapping: Dict[str, str],
    database_server: str,
    original_database_server: str,
    tables_path: Dict[str, str],
    max_execution_time: int,
    cluster: str,
    retriable_exceptions: Optional[List[int]],
    user_agent: Optional[str] = UserAgents.INTERNAL_QUERY.value,
    wait_setting: Optional[str] = WAIT_ALTER_REPLICATION_ALL,
    has_been_externally_cancelled: Optional[Callable[[], bool]] = None,
    timeout_before_checking_execution_speed: Optional[int] = None,
    timeout: Optional[int] = None,
    step_collector: Optional[StepCollector] = None,
) -> None:
    client = HTTPClient(database_server, database="default")
    src_databases = list(populate_databases_mapping.values())
    retriable_exceptions = retriable_exceptions or []

    tables_query = f"""
        SELECT
            database,
            table,
            groupUniqArray(partition) as partitions,
            sum(bytes_on_disk) as total_bytes
        FROM system.parts
        WHERE
            active
            AND database IN ('{"','".join(src_databases)}')
        GROUP BY database, table
        HAVING total_bytes > 0
        FORMAT JSON
    """

    _, body = client.query_sync(tables_query)
    tables = json.loads(body).get("data", [])

    # This dict holds mappings for databases in reverse k/v
    # to facilitate reverse lookup when attaching partitions
    populate_databases_mapping_reverse: Dict[str, str] = {v: k for k, v in populate_databases_mapping.items()}

    total_partitions = 0
    for table in tables:
        partitions = table.get("partitions", [])
        origin_database_name = table.get("database")
        destination_database_name = populate_databases_mapping_reverse.get(origin_database_name)
        total_partitions += len(partitions)

    if step_collector:
        step_collector.update_stats(total_partitions)

    # Attach fetched partitions
    for table in tables:
        origin_database_name = table.get("database")
        destination_database_name = populate_databases_mapping_reverse.get(origin_database_name)
        origin_table_name = f"{origin_database_name}.{table['table']}"
        target_table_name = f"{destination_database_name}.{table['table']}"
        partitions = table.get("partitions", [])
        moved_partitions = []
        # TODO: don't attach partition by partition do them all at once for each table
        for partition in partitions:
            partition_expr = parse_partition_expression(partition)
            step_id = (destination_database_name, table["table"], partition)

            try:
                attach_partition_query = (
                    f"ALTER TABLE {target_table_name} ATTACH {partition_expr} FROM {origin_table_name}"
                )
                _query_id = ulid.new().str

                def _do_attach(step_id: Tuple[str | None, Any, Any], attach_partition_query: str, query_id: str):
                    if step_collector:
                        step_collector.update_step(step_id, query_id, "working", "attach")
                    _, query_finish_logs = ch_guarded_query(
                        database_server,
                        "default",
                        attach_partition_query,
                        query_id=query_id,
                        max_execution_time=max_execution_time,
                        has_been_externally_cancelled=has_been_externally_cancelled,
                        user_agent=user_agent,
                        timeout=10,
                        disable_upstream_fallback=True,
                        retries=True,
                    )

                    if step_collector:
                        step_collector.update_step(step_id, query_id, "done", "attach")

                _do_attach(step_id, attach_partition_query, _query_id)
                moved_partitions.append(partition)
            except CHException as e:
                if step_collector:
                    step_collector.update_step(
                        step_id,
                        _query_id,
                        "error",
                        "attach",
                        f"Job failed while populating partition {partition}",
                    )
                logging.exception(
                    f"Populate error: Partition {partition} could not be attached on table {origin_table_name}, error: {e}"
                )
                raise e
            except Exception as e:
                if step_collector:
                    step_collector.update_step(step_id, _query_id, "error", "attach", str(e))
                logging.exception(
                    f'Populate error: partition {partition} could not be attached on table {target_table_name}, error: {e}. Successful partitions moved are: {",".join(moved_partitions)}'
                )
                raise e

            @retry_sync(CHException, tries=3, delay=3, backoff=2, ch_error_codes=retriable_exceptions)
            def run_drop_partition_query(
                partition: str, partition_expr: str, origin_table_name: str, drop_query_id: str
            ):
                drop_partition_query = f"ALTER TABLE {origin_table_name} DROP {partition_expr}"
                client.query_sync(
                    drop_partition_query,
                    read_only=False,
                    user_agent=user_agent,
                    query_id=drop_query_id,
                    max_execution_time=max_execution_time,
                    max_table_size_to_drop=SKIP_TABLE_SIZE_SAFEGUARD,
                    max_partition_size_to_drop=SKIP_PARTITION_SIZE_SAFEGUARD,
                )

            try:
                drop_query_id = ulid.new().str
                run_drop_partition_query(partition, partition_expr, origin_table_name, drop_query_id)
                if step_collector:
                    step_collector.update_step(step_id, drop_query_id, "done", "clean")
            except CHException as e:
                if step_collector:
                    # Setting it as "done" instead of marking it as error for the user
                    step_collector.update_step(step_id, drop_query_id, "done", "clean")
                logging.exception(
                    f"Populate error: Partition {partition} could not be dropped on table {origin_table_name}, error: {e}"
                )
                raise e
            except Exception as e:
                # Raising an exception here to stop the populate and avoid
                # inserting duplicated data into populate destination tables
                logging.exception(
                    f"Populate error: Partition {partition} could not be dropped on table {origin_table_name}, error: {e}"
                )
                raise Exception("An Internal Error ocurred while running populate")


async def ch_alter_table_modify_query(
    workspace: "User",
    database: str,
    view_name: str,
    sql: str,
    **extra_params: Any,
) -> bytes:
    client = HTTPClient(workspace.database_server)
    cluster = workspace.cluster
    cluster_clause = f"ON CLUSTER {cluster}" if cluster else ""

    alter_table_query = f"ALTER TABLE {database}.{view_name} {cluster_clause} MODIFY QUERY {sql}"
    _, result = await client.query(
        alter_table_query,
        read_only=False,
        **extra_params,
    )
    return result


def ch_create_temporary_databases_sync(
    database_server: str,
    origin_database: str,
    all_databases: List[str],
    dependent_data_sources: Set[Tuple[str, str]],
    cluster: Optional[str] = None,
    dependent_materialized_views: Optional[Set[Tuple[str, str]]] = None,
    disk_settings: Optional[dict[str, Any]] = None,
) -> Tuple[str, Dict[str, str], Dict[str, str]]:
    client = HTTPClient(database_server, database="default")
    tmp_databases_mapping: Dict[str, str] = {}
    suffix = f"_populate_{str(uuid.uuid4())[:4]}"
    cluster_clause = f"ON CLUSTER {cluster}" if cluster else ""

    for database in all_databases:
        temporary_database = f"{database}_{suffix}"
        tmp_databases_mapping[database] = temporary_database

        # Create temporary empty temporary database
        create_database_query = f"""
            CREATE DATABASE {temporary_database} {cluster_clause}
        """
        client.query_sync(create_database_query, read_only=False)  # FIXME add max execution time

    # Get MaterializedViews and Replicated(MergeTree) tables from the original database
    tables_query = f"""
        SELECT
            database,
            name,
            engine,
            partition_key,
            sorting_key,
            primary_key,
            create_table_query,
            if(engine = 'MaterializedView', 1, 0) as priority
        FROM system.tables
        WHERE
            database IN ('{"','".join(all_databases)}')
            AND (
                engine = 'MaterializedView'
                OR
                engine = 'Null'
                OR
                engine LIKE '%MergeTree'
            )
            AND name NOT LIKE '%_quarantine'
            AND name NOT LIKE '%_tmp_%'
        ORDER BY priority ASC
        FORMAT JSON
    """
    _, body = client.query_sync(tables_query)
    tables = json.loads(body).get("data", [])

    # Recreate the tables in the new database. First MergeTree tables, then Materialized Views.
    tables_path: Dict[str, str] = {}

    def _replace_dependent_data_sources(create_table_sql: str, suffix: str) -> str:
        for d in dependent_data_sources:
            create_table_sql = create_table_sql.replace(f"{d[0]}.{d[1]}", f"{d[0]}_{suffix}.{d[1]}")
        return create_table_sql

    for table in tables:
        temporary_database_name = tmp_databases_mapping.get(table.get("database"), "")
        if table["engine"] == "MaterializedView" or ("Replicated" not in table["engine"]):
            if (
                isinstance(dependent_materialized_views, set)
                and table["engine"] == "MaterializedView"
                and (table.get("database"), table.get("name")) not in dependent_materialized_views
            ):
                logging.warning(
                    f"Continue with the process since {table.get('database')}.{table.get('name')} is not a dependent materialized view"
                )
                continue

            create_table_sql = table["create_table_query"]
            create_table_sql = create_table_sql.replace(
                f"{table.get('database')}.{table.get('name')}", f"{temporary_database_name}.{table.get('name')}"
            )
            # Replace only dependent data sources
            create_table_sql = _replace_dependent_data_sources(create_table_sql, suffix)
            create_table_sql = create_table_sql.replace(
                f"{temporary_database_name}.{table['name']} TO ",
                f"{temporary_database_name}.{table['name']} {cluster_clause} TO ",
            )

            if table["engine"] == "MaterializedView":
                create_table_sql = create_table_sql.replace(
                    "CREATE MATERIALIZED VIEW", "CREATE MATERIALIZED VIEW IF NOT EXISTS"
                )
            else:
                create_table_sql = create_table_sql.replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS")

            logging.info(
                f"Replaced query on temporary database for table {table.get('database')}.{table.get('name')}: {create_table_sql}"
            )
        else:
            engine_full, _, _ = create_table_query_to_engine_advanced(table["create_table_query"])
            engine_full = engine_full.replace(table.get("database", ""), temporary_database_name) if engine_full else ""
            create_table_sql = CHTable(
                columns=[],
                cluster=None,
                engine=engine_full,
                not_exists=True,
                as_table=f"{table.get('database')}.{table.get('name')}",
                disk_settings=disk_settings,
            ).as_sql(temporary_database_name, table.get("name"), skip_validation=True)
        try:
            _, body = client.query_sync(create_table_sql, read_only=False)
        except CHException as e:
            logging.warning(f"Table {table['name']} could not be created on database {temporary_database}, error: {e}")
            ch_error_message = str(e).replace(f"_{suffix}", "")
            raise CHException(ch_error_message)
        except Exception as e:
            logging.warning(f"Table {table['name']} could not be created on database {temporary_database}, error: {e}")
            raise e

    temporary_database = tmp_databases_mapping.get(origin_database, "")
    return temporary_database, tables_path, tmp_databases_mapping


def create_quarantine_table_from_landing_sync(
    *,
    landing_datasource_name: str,
    database_server: str,
    database: str,
    cluster: Optional[str],
    quarantine_columns: Optional[List[Dict[str, Any]]] = None,
) -> None:
    if not quarantine_columns:
        landing_columns = ch_table_schema(landing_datasource_name, database_server, database)
        if not landing_columns:
            raise Exception(f"Unable to fetch schema of {database}.{landing_datasource_name}")

        safe_columns = CSVInfo.convert_columns_to_safe_types(landing_columns, include_fallback=False)
        quarantine_columns = ERROR_COLUMNS + safe_columns

    table = QuarantineCHTable(quarantine_columns, cluster=cluster, not_exists=True)
    create_sql = table.as_sql(database, landing_datasource_name + "_quarantine")
    client = HTTPClient(database_server, database=database)
    client.query_sync(
        create_sql,
        read_only=False,
        # TODO: This should request the `ddl_parameters` from the workspace
        max_execution_time=30,
        distributed_ddl_task_timeout=28,
        distributed_ddl_output_mode=DDL_OUTPUT_MODE_NULL_STATUS_ON_TIMEOUT,
    )


async def create_quarantine_table_from_landing(
    landing_datasource_name: str,
    database_server: str,
    database: str,
    cluster: Optional[str],
    quarantine_columns: Optional[List[Dict[str, Any]]] = None,
) -> None:
    if not quarantine_columns:
        landing_columns = await ch_table_schema_async(landing_datasource_name, database_server, database)
        if not landing_columns:
            raise Exception(f"Unable to fetch schema of {database}.{landing_datasource_name}")

        safe_columns = CSVInfo.convert_columns_to_safe_types(landing_columns, include_fallback=False)
        quarantine_columns = ERROR_COLUMNS + safe_columns

    table = QuarantineCHTable(quarantine_columns, cluster=cluster, not_exists=True)
    create_sql = table.as_sql(database, landing_datasource_name + "_quarantine")
    client = HTTPClient(database_server, database=database)
    await client.query(
        create_sql,
        read_only=False,
        # TODO: This should requests the `ddl_parameters` from the workspace
        max_execution_time=30,
        distributed_ddl_task_timeout=28,
        distributed_ddl_output_mode=DDL_OUTPUT_MODE_NULL_STATUS_ON_TIMEOUT,
    )


async def ch_check_user_profile_exists(database_server: str, user: str, database: Optional[str] = None):
    try:
        client = HTTPClient(database_server, database=database)
        return await client.query(q="SELECT 1", user=user, fallback_user_auth=False)
    except Exception as e:
        logging.error(f"Can not use user {user} on {database_server}: {e}")
        raise e


def map_tinybird_format_to_ch_format(tinybird_format: str) -> str:
    mapping = {
        "parquet": "Parquet",
        "csv": "CSVWithNames",
        "ndjson": "JSONEachRow",
    }
    ch_format = mapping.get(tinybird_format)
    if ch_format is not None:
        return ch_format
    raise Exception(f"Unsupported format: {tinybird_format}")


@dataclass
class CHAnalysis:
    columns: List[Dict[str, Optional[Union[str, int]]]]
    columns_schema: List[str]
    schema: str
    preview: Dict[str, Any]


class CHAnalyzeError(Exception):
    pass


async def ch_analyze_from_url(url: str, format: str, limit: int) -> CHAnalysis:
    ch_format = map_tinybird_format_to_ch_format(format)
    query = f"SELECT * FROM url({ch_escape_string(url)}, {ch_format}) LIMIT {limit}"
    try:
        preview_data = await CHTable([]).query_async(
            query=query,
            output_format="JSON",
            extra_options={
                # TODO: change to auto when upgrading clickhouse-local to 24.8+
                # See comment: https://gitlab.com/tinybird/analytics/-/issues/15468#note_2140089029
                "schema_inference_make_columns_nullable": "false",
            },
        )
    except Exception as e:
        error = f"File is not a valid {format} file"
        if "RECEIVED_ERROR_FROM_REMOTE_IO_SERVER" in str(e):
            error = f"Invalid URL: cannot access '{url}'"
        if "Unsupported Parquet type" in str(e):
            parsed_error = parse_unsupported_parquet_type(str(e))
            if parsed_error:
                error += f": {parsed_error}"
        raise CHAnalyzeError(error)

    assert isinstance(preview_data, dict)

    columns: List[Dict[str, Optional[Union[str, int]]]] = []
    schema: List[str] = []
    for column in preview_data["meta"]:
        name = column["name"]
        normalized_name = normalize_column_name(name)
        _type = column["type"]
        name = f"{name}[:]" if "Array" in _type else name
        columns.append(
            {
                "path": f"$.{name}",
                "recommended_type": _type,
                "name": normalized_name,
                "present_pct": 1 if not _type.startswith("Nullable") else None,
            }
        )
        schema.append(f"{normalized_name} {_type} `json:$.{name}`")

    ch_analyze = CHAnalysis(columns=columns, columns_schema=schema, schema=", ".join(schema), preview=preview_data)
    return ch_analyze


async def ch_describe_table_from_url(
    url: str, format: str, timeout: int = 60, override_query: str = "", **extra_params: Any
) -> DescribeTable:
    query = override_query or f"DESCRIBE TABLE url({ch_escape_string(url)})"
    try:
        extra_options = {"describe_include_subcolumns": "true", **extra_params}
        describe_table_data = await CHTable([]).query_async(
            query=query,
            output_format="JSON",
            extra_options=extra_options,
            timeout=timeout,
        )
    except Exception as e:
        logging.warning(f"Exception getting DESCRIBE TABLE from url: {url} error: {e}")
        error = f"File is not a valid {format} file"
        if "RECEIVED_ERROR_FROM_REMOTE_IO_SERVER" in str(e):
            error = f"Invalid URL: cannot access '{url}'"
        if "Unsupported Parquet type" in str(e):
            parsed_error = parse_unsupported_parquet_type(str(e))
            if parsed_error:
                error += f": {parsed_error}"
        raise CHAnalyzeError(error)

    assert isinstance(describe_table_data, dict)

    return DescribeTable.from_query_data_response(describe_table_data["data"])


def ch_escape_string(string: str):
    """
    Escapes a string by adding quotes and backslashes, so it can be used it in a ClickHouse SQL query.
    See https://clickhouse.com/docs/en/sql-reference/syntax#string for string syntax in CH
    It is only mandatory to escape single quotes and backslashes, but we escape the others to improve readability

    >>> ch_escape_string("'foo\\\\'")
    "'\\\\'foo\\\\\\\\\\\\''"
    >>> ch_escape_string("\\'\\b\\f\\r\\n\\t\\0\\a\\v")
    "'\\\\'\\\\b\\\\f\\\\r\\\\n\\\\t\\\\0\\\\a\\\\v'"
    """
    translations = {
        "\\": "\\\\",
        "'": "\\'",
        "\b": "\\b",
        "\f": "\\f",
        "\r": "\\r",
        "\n": "\\n",
        "\t": "\\t",
        "\0": "\\0",
        "\a": "\\a",
        "\v": "\\v",
    }
    table = string.maketrans(translations)
    return f"'{string.translate(table)}'"


def get_columns_from_ast(ast_str: str) -> List[str]:
    """
    >>> get_columns_from_ast("                  Identifier status")
    ['status']
    >>> get_columns_from_ast("Identifier status")
    ['status']
    >>> get_columns_from_ast("             TableIdentifier d_1234.t_abcd   Identifier status")
    ['status']
    >>> get_columns_from_ast("   Identifier status$")
    ['status$']
    >>> get_columns_from_ast("   Identifier stat-us$")
    ['stat-us$']
    >>> get_columns_from_ast("│                  Identifier new_semver                                            ││                  Literal ''                                                       ││                Literal 'post'                                                     ││                Literal ''                                                         ││              Function and (children 1)                                            ││               ExpressionList (children 5)                                         ││                Function equals (children 1)                                       ││                 ExpressionList (children 2)                                       ││                  Identifier operation_name      ")
    ['new_semver', 'operation_name']
    >>> get_columns_from_ast("             TableIdentifier d_1234.t_abcd   Asterisk Identifier status")
    []
    >>> get_columns_from_ast("Asterisk")
    []
    """
    # We can't filter out columns in presence of a SELECT * from any subquery
    has_asterisk = re.search(r"\bAsterisk\b", ast_str.replace("\n", ""))
    if has_asterisk:
        return []

    columns = re.findall(r"(?:^|\s)Identifier ([\S]+)", ast_str.replace("\n", ""))

    all_columns = []
    for column in columns:
        if "." in column:
            all_columns.append(column.split(".")[1])
        all_columns.append(column)
    return all_columns


def ch_get_columns_from_left_table_used_in_query_sync(database_server: str, database: str, sql: str):
    client = HTTPClient(database_server, database=database)

    # 1. Get all columns from left table
    left_table = get_left_table(sql)
    all_columns = ch_get_columns_from_query_sync(
        database_server, database, f"SELECT * FROM {left_table[0]}.{left_table[1]}"
    )
    left_table_columns = [column.get("name") for column in all_columns]

    # 2. Get columns used in the query
    _, result = client.query_sync(f"EXPLAIN AST optimize=1 {sql}")
    query_ast = result.decode("utf-8").replace("\n", "")
    query_columns = get_columns_from_ast(query_ast)

    # 3. Filter out columns from query present in the left table
    subset_columns = list(set(query_columns) & set(left_table_columns))

    return [c for c in all_columns if c.get("name") in subset_columns]


@dataclass
class CHParquetMetadata:
    num_columns: int
    num_rows: int
    num_row_groups: int
    total_uncompressed_size: int


async def ch_get_parquet_metadata_from_url(url: str, timeout: int = 60, **extra_params: Any) -> CHParquetMetadata:
    query = f"SELECT num_columns, num_rows, num_row_groups, total_uncompressed_size FROM url({ch_escape_string(url)}, ParquetMetadata)"
    try:
        ch_result = await CHTable([]).query_async(
            query=query,
            output_format="JSON",
            extra_options=extra_params,
            timeout=timeout,
        )
    except Exception as e:
        logging.exception(f"Exception getting Parquet Metadata from url: {url} error: {e}")
        error = "File is not a valid Parquet file"
        if "RECEIVED_ERROR_FROM_REMOTE_IO_SERVER" in str(e):
            error = f"Invalid URL: cannot access '{url}'"
        if "Unsupported Parquet type" in str(e):
            parsed_error = parse_unsupported_parquet_type(str(e))
            if parsed_error:
                error += f": {parsed_error}"
        raise Exception(error)

    assert isinstance(ch_result, dict)

    return CHParquetMetadata(
        num_columns=int(ch_result["data"][0]["num_columns"]),
        num_rows=int(ch_result["data"][0]["num_rows"]),
        num_row_groups=int(ch_result["data"][0]["num_row_groups"]),
        total_uncompressed_size=int(ch_result["data"][0]["total_uncompressed_size"]),
    )


def extract_host(call_string):
    """
    Extracts the host (or URL) from a function call string in SQL-like syntax.

    Args:
    call_string (str): The function call string from which to extract the host.

    Returns:
    str: The host or URL from the function call string.

    Examples:
    >>> extract_host("select * from postgresql(`postgres{1|2|3}:5432`, 'postgres_database', 'postgres_table', 'user', 'password')")

    >>> extract_host("select * from postgresql(`postgres1:5431|postgres2:5432`, 'postgres_database', 'postgres_table', 'user', 'password')")

    >>> extract_host("select * from postgresql('localhost:5432', 'clickhouse', 'nice.table', 'postgrsql_user', 'password', 'nice.schema')")
    'localhost:5432'
    >>> extract_host("select * from postgresql('localhost:5432', 'test', 'test', 'postgresql_user', 'password')")
    'localhost:5432'
    >>> extract_host("SELECT * FROM postgresql('localhost:5432', 'clickhouse', 'nice.table', 'postgrsql_user', 'password', 'nice.schema')")
    'localhost:5432'
    >>> extract_host("SELECT * FROM url('http://127.0.0.1:12345/', CSV, 'column1 String, column2 UInt32', headers('Accept'='text/csv; charset=utf-8')) LIMIT 3;")
    'http://127.0.0.1:12345/'
    >>> extract_host("SELECT name FROM mysql(`mysql:3306`, 'mysql_database', 'mysql_table', 'user', 'password');")
    'mysql:3306'
    >>> extract_host("SELECT * FROM azureBlobStorage('http://azurite1:10000/devstoreaccount1', 'test_container', 'test_1.csv', 'devstoreaccount1', 'Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==', 'CSV', 'auto', 'column1 UInt32, column2 UInt32, column3 UInt32');")
    'http://azurite1:10000/devstoreaccount1'
    >>> extract_host("SELECT * FROM gcs('https://storage.googleapis.com/my-test-bucket-768/data.csv.gz', 'CSV', 'column1 UInt32, column2 UInt32, column3 UInt32', 'gzip') LIMIT 2;")
    'https://storage.googleapis.com/my-test-bucket-768/data.csv.gz'
    >>> extract_host("SELECT * FROM mongodb('127.0.0.1:27017', 'test', 'my_collection', 'test_user', 'password', 'log_type String, host String, command String', 'connectTimeoutMS=10000')")
    '127.0.0.1:27017'
    >>> extract_host("SELECT * FROM iceberg('http://test.s3.amazonaws.com/clickhouse-bucket/test_table', 'test', 'test')")
    'http://test.s3.amazonaws.com/clickhouse-bucket/test_table'
    """

    for _, pattern in HOST_PATTERNS.items():
        match = re.search(pattern, call_string)
        if match:
            host = match.group(2)
            # Handle cases where multiple replicas or different formats are not supported
            if "|" in host or "{" in host:
                return None

            return host


def remove_stream_operators_from_sql(sql: str) -> str:
    """
    Removes stream operators from a SQL query.

    Args:
    sql (str): The SQL query string.

    Returns:
    str: The SQL query string without stream operators (STREAM, STREAM TAIL).

    Examples:
    >>> remove_stream_operators_from_sql("SELECT * FROM table STREAM")
    'SELECT * FROM table'
    >>> remove_stream_operators_from_sql("SELECT * FROM table STREAM TAIL")
    'SELECT * FROM table'
    >>> remove_stream_operators_from_sql("SELECT * FROM table stream")
    'SELECT * FROM table'
    >>> remove_stream_operators_from_sql("SELECT * FROM table stream tail")
    'SELECT * FROM table'
    >>> remove_stream_operators_from_sql("SELECT * FROM table STREAM TAIL WHERE column = 1")
    'SELECT * FROM table WHERE column = 1'
    >>> remove_stream_operators_from_sql("SELECT * FROM table stream WHERE column = 1")
    'SELECT * FROM table WHERE column = 1'
    >>> remove_stream_operators_from_sql("SELECT stream_id FROM table WHERE column = 1")
    'SELECT stream_id FROM table WHERE column = 1'
    >>> remove_stream_operators_from_sql("SELECT stream_id FROM table STREAM WHERE column = 1")
    'SELECT stream_id FROM table WHERE column = 1'
    >>> remove_stream_operators_from_sql("SELECT stream_id FROM table STREAM WHERE column = 1 JOIN (SELECT * FROM table STREAM) USING stream_id")
    'SELECT stream_id FROM table WHERE column = 1 JOIN (SELECT * FROM table) USING stream_id'
    """
    return re.sub(r"(FROM\s+[a-z0-9_]+)\s+STREAM(?:\s+TAIL)?", r"\1", sql, flags=re.IGNORECASE)


async def ch_get_version(database_server: str) -> str:
    client = HTTPClient(database_server)
    _, result = await client.query("SELECT version()", read_only=True)
    version = result.decode("utf-8").strip()

    try:
        parts = version.split(".")
        version = ".".join(parts[:2])
    except Exception:
        version = ""

    return version


def parse_unsupported_parquet_type(error: str) -> str:
    parsed_error = ""
    if "Unsupported Parquet type" in str(error):
        try:
            pattern = r"Unsupported Parquet type '[^']+' of an input column '[^']+'"
            match = re.search(pattern, str(error))
            if match:
                parsed_error += match.group()
        except Exception as e:
            logging.exception(f"Error parsing unsupported type error: {e}")
    return parsed_error


def get_tables_from_database(database_server: str, database: str) -> List[str]:
    client = HTTPClient(database_server)
    _, result = client.query_sync(
        f"SELECT name FROM system.tables WHERE database = '{database}' FORMAT JSON", read_only=True
    )
    tables_json = json.loads(result.decode("utf-8"))
    tables = [row["name"] for row in tables_json["data"]]
    return tables


def create_user_tables_on_pool_replica(
    original_database_server: str,
    target_database_server: str,
    dependent_databases: List[str],
    dependent_data_sources: Set[Tuple[str, str]],
    dependent_materialized_views: Set[Tuple[str, str]],
    populate_view_sql: str,
    disk_settings: dict[str, Any],
) -> Set[str]:
    # In the inputs, we have the downstream dependencies, but we need the upstream ones (the ones that are used in the view SQL)
    source_tables = sql_get_used_tables(populate_view_sql, table_functions=False)
    all_dependent_data_sources = dependent_data_sources
    all_dependent_databases = set(dependent_databases)

    # We'll store the databases and data sources created in the pool
    pool_databases: Set[str] = set()
    pool_data_sources: Set[Tuple[str, str]] = set()

    for database_name, table_name, _ in source_tables:
        all_dependent_data_sources.add((database_name, table_name))
        all_dependent_databases.add(database_name)
    target_client = HTTPClient(target_database_server)
    for database_name in all_dependent_databases:
        target_client.query_sync(f"CREATE DATABASE IF NOT EXISTS {database_name}", read_only=False)
        pool_databases.add(database_name)

    for database_name, table_name in all_dependent_data_sources:
        table_details = ch_table_details(
            table_name=table_name, database_server=original_database_server, database=database_name
        )
        create_table_on_external_replica(target_database_server, database_name, table_details, disk_settings)
        pool_data_sources.add((database_name, table_name))
    for database_name, table_name in dependent_materialized_views:
        create_table_query = ch_get_create_materialized_view_query_sync(
            original_database_server, database_name, table_name
        )
        source_tables = sql_get_used_tables(
            _select_from_create_materialized_view_query(create_table_query), table_functions=False
        )
        for database_name, table_name, _ in source_tables:
            if database_name not in pool_databases:
                target_client.query_sync(f"CREATE DATABASE IF NOT EXISTS {database_name}", read_only=False)
                pool_databases.add(database_name)
            if (database_name, table_name) not in pool_data_sources:
                table_details = ch_table_details(
                    table_name=table_name, database_server=original_database_server, database=database_name
                )
                create_table_on_external_replica(target_database_server, database_name, table_details, disk_settings)
                pool_data_sources.add((database_name, table_name))

        target_client.query_sync(create_table_query, read_only=False)

    for database_name, table_name in pool_data_sources:
        CHReplication.ch_wait_for_replication_sync(
            database_server=target_database_server,
            cluster=None,
            database=database_name,
            table_name=table_name,
        )
    return pool_databases


def wait_for_database_replication(database_server: str, database: str) -> None:
    tables = get_tables_from_database(database_server, database)
    client = HTTPClient(database_server)
    for table in tables:
        if is_table_engine_replicated(client, database, table):
            CHReplication.ch_wait_for_replication_sync(
                database_server=database_server,
                cluster=None,
                database=database,
                table_name=table,
            )


def get_fallback_partition_column_name(columns_names: List[str]) -> str:
    """
    >>> get_fallback_partition_column_name(["column1", "column2"])
    'insertion_date'
    >>> get_fallback_partition_column_name(["column1", "column2", "insertion_date"])
    '__insertion_date'
    >>> get_fallback_partition_column_name(["column1", "column2", "insertion_date", "__insertion_date"])
    '____insertion_date'
    """
    target_column_name = str(FALLBACK_PARTITION_COLUMN["name"])

    while target_column_name in columns_names:
        target_column_name = "__" + target_column_name

    return target_column_name
