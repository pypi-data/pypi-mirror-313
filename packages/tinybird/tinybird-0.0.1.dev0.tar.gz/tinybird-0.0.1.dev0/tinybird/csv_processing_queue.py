"""This is the global processing queue for csv chunks.

    res = process_queue.process(csv_chunk)
    process_queue.terminate()

It can process a queue

    q = queue.Queue()
    process.process_queue(q)
    q.put(block)
    q.put(block)
    q.put(block)
    q.join()

"""

import ast
import csv
import json
import logging
import math
import os
import queue
import re
import signal
import threading
import time
import traceback
import uuid
from datetime import datetime
from decimal import Decimal, DecimalException
from io import StringIO
from multiprocessing import Barrier, Event, JoinableQueue, Process, Queue, cpu_count
from typing import Any, Dict, List, Optional, Tuple, Union

import ulid
from setproctitle import setproctitle

from .blocks import Block
from .ch import (
    ERROR_COLUMNS,
    CHSummary,
    CHTable,
    CSVInfo,
    HTTPClient,
    ch_table_schema,
    create_quarantine_table_from_landing_sync,
)
from .ch_utils.exceptions import CHException
from .csv_guess import guess_delimiter, guess_new_line, guess_number_of_columns, has_header
from .csv_tools import csv_from_python_object
from .datatypes import (
    get_decimal_limits,
    is_type_datetime,
    is_type_datetime64,
    is_type_decimal,
    parse_decimal_type,
    testers,
)
from .timing import Timer

BYTES_TO_GUESS_CSV = 1024 * 50
MIN_BYTES_GUESS = 1024 * 10
MAX_GUESS_BYTES = int(1e6)  # ~ 1mb
DUMMY_BLOCK_ID = "DummyBlock"
EXTRACT_TYPE_PARAMS = re.compile(r"\((.*)\)")


class CsvChunkQueueRegistry:
    _root_process_lock = threading.Lock()
    _root_process_queue: Optional["CsvChunkQueue"] = None

    DEFAULT_WORKERS = min(6, max(1, math.ceil(cpu_count() / 2)))

    @classmethod
    def get_or_create(
        cls, workers: int = DEFAULT_WORKERS, app_name: str = "unknown", debug: bool = False
    ) -> "CsvChunkQueue":
        if cls._root_process_queue:
            return cls._root_process_queue
        with cls._root_process_lock:
            if not cls._root_process_queue:
                logging.info("Starting CsvChunkQueue")
                if threading.main_thread() != threading.current_thread():
                    logging.critical(
                        f"Starting CsvChunkQueue from thread={threading.current_thread()}. This is a bug.\n"
                        f"Was CsvChunkQueueRegistry.get_or_create() called after stop()?\n"
                        f"PID: {os.getpid()}\n"
                        f"Stack: \n {traceback.format_stack()}"
                    )
                cls._root_process_queue = CsvChunkQueue(workers, app_name, debug)
                if workers > 0:
                    cls._root_process_queue.start()
                    cls._root_process_queue.start_supervisor()
                    cls._root_process_queue.start_dummy_block_supervisor()
            return cls._root_process_queue

    @classmethod
    def stop(cls) -> None:
        logging.info("Stopping CsvChunkQueue")
        with cls._root_process_lock:
            if cls._root_process_queue:
                if cls._root_process_queue.workers > 0:
                    cls._root_process_queue.terminate()
                cls._root_process_queue = None


def cut_csv_extract(csv_extract, max_size):
    """
    >>> cut_csv_extract('1,2,3', 1)
    '1,2,3'
    >>> cut_csv_extract('1,2,3', 100)
    '1,2,3'
    >>> cut_csv_extract('1,2,3\\n', 100)
    '1,2,3'
    >>> cut_csv_extract('1,2,3\\n4,5,6', 100)
    '1,2,3\\n4,5,6'
    >>> cut_csv_extract('1,2,3\\n4,5,6\\n', 100)
    '1,2,3\\n4,5,6'
    >>> cut_csv_extract('1,2,3\\n4,5,6\\n', 6)
    '1,2,3\\n4,5,6'
    >>> cut_csv_extract('1,2,3\\n4,5,6', 6)
    '1,2,3'
    >>> cut_csv_extract('1,2,3\\n4,5,6', 1)
    '1,2,3'
    >>> cut_csv_extract('1,2,3\\n4,5,6', 12)
    '1,2,3\\n4,5,6'
    >>> cut_csv_extract('1,2,3\\n4', 7)
    '1,2,3'
    """
    newline = guess_new_line(csv_extract)
    limit_pos = csv_extract.rindex(newline) if newline else len(csv_extract)
    if len(csv_extract) < max_size:
        limit_pos = len(csv_extract)
        limit_pos = limit_pos if csv_extract[limit_pos - 1] != newline else limit_pos - 1
    return csv_extract[:limit_pos]


def prepare_extract(data, escapechar=None):
    bytes_to_guess = max(MIN_BYTES_GUESS, min(int(len(data) * 0.05), MAX_GUESS_BYTES))
    csv_extract = data[:bytes_to_guess]
    with Timer() as timing:
        # csv_extract = extract.decode(chardet.detect(extract)['encoding'])
        newline = guess_new_line(csv_extract)
        if newline and len(csv_extract) == bytes_to_guess:
            fixed_extract = csv_extract[: csv_extract.rindex(newline)]
        else:
            # most likely a oneliner
            fixed_extract = csv_extract
        delimiter = guess_delimiter(fixed_extract, escapechar)
    logging.info("guessing time %f", timing.interval)
    return fixed_extract, delimiter, newline


def infer_csv_chunk_schema(
    chunk: str, data_table_schema: List[Any], dialect: Dict[Any, Any], csv_columns: Optional[List[Any]] = None
) -> List[Any]:
    """
    >>> infer_csv_chunk_schema( '1,2,3,4,5\\n1,2,3,4,5\\n', [{"name": 'column1'}, {"name": 'column2'}, {"name": 'column3'}, {"name": 'column4'}, {"name": 'column5'}], {"delimiter": ","})
    [{'name': 'column1'}, {'name': 'column2'}, {'name': 'column3'}, {'name': 'column4'}, {'name': 'column5'}]
    >>> infer_csv_chunk_schema( '1,2,3,4\\n1,2,3,4\\n', [{"name": 'column1'}, {"name": 'column2'}, {"name": 'column3'}, {"name": 'column4'}, {"name": 'column5'}], {"delimiter": ","})
    [{'name': 'column1'}, {'name': 'column2'}, {'name': 'column3'}, {'name': 'column4'}]
    >>> infer_csv_chunk_schema( '1,2,3,4', [{"name": 'column1'}, {"name": 'column2'}, {"name": 'column3'}, {"name": 'column4'}, {"name": 'column5'}], {"delimiter": ","})
    [{'name': 'column1'}, {'name': 'column2'}, {'name': 'column3'}, {'name': 'column4'}]
    >>> infer_csv_chunk_schema( '', [{"name": 'column1'}, {"name": 'column2'}, {"name": 'column3'}, {"name": 'column4'}, {"name": 'column5'}], {"delimiter": ","})
    []
    >>> infer_csv_chunk_schema( '1,2,3,4,5,6', [{"name": 'column1'}, {"name": 'column2'}, {"name": 'column3'}, {"name": 'column4'}, {"name": 'column5'}], {"delimiter": ","})
    [{'name': 'column1'}, {'name': 'column2'}, {'name': 'column3'}, {'name': 'column4'}, {'name': 'column5'}]
    >>> infer_csv_chunk_schema( '1,2\\n1,2,3\\n1,2,3\\n1,2,3,4', [{"name": 'column1'}, {"name": 'column2'}, {"name": 'column3'}, {"name": 'column4'}, {"name": 'column5'}], {"delimiter": ","})
    [{'name': 'column1'}, {'name': 'column2'}, {'name': 'column3'}]
    >>> infer_csv_chunk_schema( '2020-10-12,1,mec', [{'name': 'c1', 'type': 'Int8'}, {'name': 'c2', 'type': 'String'}, {'name': 'c3', 'type': 'Date'}], {"delimiter": ","}, [{'name': 'c3', 'type': 'Date'}, {'name': 'c1', 'type': 'Int8'}, {'name': 'c2', 'type': 'String'}])
    [{'name': 'c3', 'type': 'Date'}, {'name': 'c1', 'type': 'Int8'}, {'name': 'c2', 'type': 'String'}]
    >>> infer_csv_chunk_schema( '2020-10-12,1,mec', [{'name': 'c1', 'type': 'Int8'}, {'name': 'c2', 'type': 'String'}, {'name': 'c3', 'type': 'Date'}], {"delimiter": ","}, [{'name': '   c2"', 'type': 'String'}, {'name': '"c3  "', 'type': 'Date'}, {'name': '"    c1"', 'type': 'Int8'}, ])
    [{'name': 'c2', 'type': 'String'}, {'name': 'c3', 'type': 'Date'}, {'name': 'c1', 'type': 'Int8'}]
    >>> infer_csv_chunk_schema( '2020-10-12,1,mec,2.3', [{'name': 'c1', 'type': 'Int8'}, {'name': 'c2', 'type': 'String'}, {'name': 'c3', 'type': 'Date'}], {"delimiter": ","}, [{'name': 'c3', 'type': 'Date'}, {'name': 'c1', 'type': 'Int8'}, {'name': 'c2', 'type': 'String'}, {'name': 'c4', 'type': 'Float'}])
    [{'name': 'c3', 'type': 'Date'}, {'name': 'c1', 'type': 'Int8'}, {'name': 'c2', 'type': 'String'}]
    """

    # In case the csv_columns is provided, look if the names and types of the columns match the `data_table_schema`
    # and return a reordered version of the same that matches the order provided in the CSV
    if csv_columns:

        def _normalize(value):
            return value.strip(' "')

        data_table_schema_set = set([_normalize(x["name"]) for x in data_table_schema])
        csv_columns_set = set([_normalize(x["name"]) for x in csv_columns])

        # In case the CSV columns include at least all names in the DB schema, we can carry on with the ingestion
        # after reordering the schema to appropriately fit the one provided in the CSV header
        if csv_columns_set.issuperset(data_table_schema_set):
            reordered_data_table_schema = []
            for csv_column in csv_columns:
                for table_column in data_table_schema:
                    if _normalize(csv_column["name"]) == _normalize(table_column["name"]):
                        reordered_data_table_schema.append(table_column)
                        break

            return reordered_data_table_schema

    # Infer the CSV schema just comparing the number of columns in the data vs the number of columns in the table.
    # TODO "number_of_columns", as the dialect, are already being calculated in the CSVInfo object, so we can just send
    # that as we send the dialect.
    number_of_columns = guess_number_of_columns(chunk, dialect["delimiter"], 100)

    return data_table_schema[:number_of_columns]


def import_csv_chunk(
    data,
    table_name: str,
    database_server: str = "localhost",
    dialect: Optional[Dict[str, Any]] = None,
    database: str = "default",
    cluster: Optional[str] = None,
    block_status_log=None,
    import_id: Optional[str] = None,
    max_execution_time=10,
    csv_columns=None,
    with_quarantine=True,
):
    # get a part of the file
    if block_status_log is not None:
        block_status_log.append({"status": "guessing", "timestamp": datetime.utcnow()})

    data_table_schema = ch_table_schema(table_name, database_server, database)
    if not data_table_schema:
        logging.exception(
            f"Failed to get {database}.{table_name} schema @ {database_server}. If you see this in production"
            ", it means that either the table no longer exists or we can't contact CH. While running "
            "integration tests, the most likely scenario is that the tearDown didn't stop all background "
            " 'processes' and one of them is trying to insert to a table that has been deleted (ops_log?)"
        )
        # TODO: this should stop import process and raise a 500
        raise Exception("Failed to import, can't get table schema")

    quarantine_table_columns = None
    if with_quarantine:
        # Internal inserts are done with `with_quarantine=False` as internal datasources don't have quarantine tables
        # And, for historical reasons, we allow existing DSs to not have a quarantine table
        # If we can't get the schema (likely because the table doesn't exist), continue as if quarantine was disabled
        quarantine_table_columns = ch_table_schema(f"{table_name}_quarantine", database_server, database)

    if not dialect:
        fixed_extract, delimiter, newline = prepare_extract(data)
        dialect = {
            "delimiter": delimiter,
            "new_line": newline,
        }
        with Timer("guess header") as header_timing:
            _has_header, _, header_len = has_header(fixed_extract, delimiter)
        logging.info(f"Getting header for {database}.{table_name}: {header_timing.interval}")
        # when dialect is passed the function I assume the header is already removed
        # so this "if" is correctly indented
        if _has_header:
            data = data[header_len + len(newline) :]
        dialect["has_header"] = _has_header
        dialect["header_len"] = header_len

    with Timer("infer csv schema") as schema_timing:
        # https://gitlab.com/tinybird/analytics/-/merge_requests/1481
        # It assumes the CSV chunk has the same schema than the table but might include less columns
        # This was added to support the case where the CSV has less columns than the table.
        # This scenario can happen if we alter the datasource and ADD a column, but we have not yet modify the import to include the new column.
        # TODO: If we are ingesting the same CSV all the time, the schema should be the same, so we should not need to infer the schema again.
        csv_chunk_schema = infer_csv_chunk_schema(data, data_table_schema, dialect, csv_columns)
    logging.info(f"Inferring schema for {database}.{table_name}: {schema_timing.interval}")

    return load_csv_chunk(
        data=data,
        table_name=table_name,
        table_columns=data_table_schema,
        csv_chunk_schema=csv_chunk_schema,
        quarantine_table_columns=quarantine_table_columns,
        dialect=dialect,
        database_server=database_server,
        database=database,
        cluster=cluster,
        block_status_log=block_status_log,
        import_id=import_id,
        max_execution_time=max_execution_time,
        with_quarantine=with_quarantine,
    )


def filter_error_columns_to_use_only_the_existing_ones_in_the_quarantine_table(
    quarantine_table_schema: Optional[List[Any]], error_columns: List[Any]
) -> List[Any]:
    """
    >>> filter_error_columns_to_use_only_the_existing_ones_in_the_quarantine_table( \
    None, [{"name": 'c__error_column'}, {"name": 'c__error'}, {"name": 'c__import_id'}])
    []
    >>> filter_error_columns_to_use_only_the_existing_ones_in_the_quarantine_table( \
    [], [{"name": 'c__error_column'}, {"name": 'c__error'}, {"name": 'c__import_id'}])
    []
    >>> filter_error_columns_to_use_only_the_existing_ones_in_the_quarantine_table( \
    [{"name": 'c__error_column'}], [{"name": 'c__error_column'}, {"name": 'c__error'}, {"name": 'c__import_id'}])
    [{'name': 'c__error_column'}]
    >>> filter_error_columns_to_use_only_the_existing_ones_in_the_quarantine_table( \
    [{"name": 'c__error_column'}, {"name": 'c__error'}, {"name": 'c__import_id'}], [{"name": 'c__error_column'}, {"name": 'c__error'}, {"name": 'c__import_id'}])
    [{'name': 'c__error_column'}, {'name': 'c__error'}, {'name': 'c__import_id'}]
    """
    if quarantine_table_schema is None:
        return []

    column_names_in_quarantine_table = set([column["name"] for column in quarantine_table_schema])
    error_columns_names = set([column["name"] for column in error_columns])

    columns_in_common = column_names_in_quarantine_table & error_columns_names

    return list(filter(lambda column: column["name"] in columns_in_common, error_columns))


def initial_newline_chars(data):
    """
    >>> initial_newline_chars('\\r\\n\\r\\nabcd')
    4
    >>> initial_newline_chars('\\n\\n\\n')
    3
    >>> initial_newline_chars('\\n\\n\\n123,"\\n\\n"')
    3
    >>> initial_newline_chars('\\n\\n\\n\\r"')
    3
    """
    i = 0
    data_len = len(data)
    while i < data_len:
        if data[i] == "\n":
            i += 1
        elif data[i] == "\r" and i < (data_len - 1) and data[i + 1] == "\n":
            i += 2
        else:
            break
    return i


class InsertCHException(CHException):
    def __init__(
        self,
        msg,
        ch_summaries: Optional[List[CHSummary]] = None,
        ch_summaries_quarantine: Optional[List[CHSummary]] = None,
    ):
        super().__init__(msg)
        self.ch_summaries = ch_summaries if ch_summaries is not None else []
        self.ch_summaries_quarantine = ch_summaries_quarantine if ch_summaries_quarantine is not None else []


def load_csv_chunk(
    *,
    data,
    table_name,
    table_columns: List[Dict[str, Any]],
    csv_chunk_schema: List[Dict[str, Any]],
    quarantine_table_columns: Optional[List[Any]],
    dialect: Dict[str, Any],
    database_server: str = "localhost",
    database: str = "default",
    cluster: Optional[str] = None,
    block_status_log=None,
    import_id: Optional[str] = None,
    max_execution_time: int = 10,
    with_quarantine: bool = True,
):
    # Remove initial new lines as clickhouse-local will choke on those
    ignored_chars = initial_newline_chars(data)
    if ignored_chars > 0:
        data = data[ignored_chars:]
    logging.info(
        f"Importing chunk for {database}.{table_name}: "
        f"{len(table_columns)} columns, {len(data)} bytes ({ignored_chars} ignored)"
    )
    client = HTTPClient(database_server, database)

    def _insert_chunk(
        chunk,
        fmt,
        table,
        columns,
        insert_dialect,
        # We had to set a timeout because the default one is 10 seconds and it's not enough for zero copy without hot disk
        max_execution_time=30,
        ch_summaries: Optional[List[CHSummary]] = None,
    ):
        query = insert_query(columns, table, fmt)
        logging.debug(query)
        query_id = ulid.new().str

        try:
            h, content = client.insert_chunk(
                query, chunk, dialect=insert_dialect, max_execution_time=max_execution_time, query_id=query_id
            )
        except CHException as e:
            if ch_summaries is not None and e.headers:
                ch_summary = e.headers.get("X-Clickhouse-Summary")
                ch_summaries.append(CHSummary(query_id=query_id, summary=json.loads(ch_summary) if ch_summary else {}))
                exc = InsertCHException(str(e), ch_summaries)
                raise exc
            raise e
        res = content.decode()
        # TODO: parse error properly
        if "Exception" in res:
            logging.exception(res)
            raise Exception(f"Failed to insert data into table {table}: {res}")
        if ch_summaries is not None:
            ch_summary = h.get("X-Clickhouse-Summary")
            ch_summaries.append(CHSummary(query_id=query_id, summary=json.loads(ch_summary) if ch_summary else {}))

    def _log_status(status: str):
        if block_status_log is not None:
            block_status_log.append({"status": status, "timestamp": datetime.utcnow()})

    # In branches, we create the quarantine table on demand https://gitlab.com/tinybird/analytics/-/issues/9012
    # If we don't have `quarantine_table_columns`, means that the quarantine table does not exist
    create_quarantine_table = not quarantine_table_columns and with_quarantine
    if create_quarantine_table:
        safe_columns = CSVInfo.convert_columns_to_safe_types(table_columns, include_fallback=False)
        quarantine_table_columns = ERROR_COLUMNS + safe_columns

    error_columns_schema_for_insert = filter_error_columns_to_use_only_the_existing_ones_in_the_quarantine_table(
        quarantine_table_columns, ERROR_COLUMNS
    )

    stats: List[dict] = []
    ch_summaries: List[CHSummary] = []
    quarantine_ch_summaries: List[CHSummary] = []

    for i, (chunk, fmt, output_dialect, quarantine_chunk) in enumerate(
        process_chunk(data, csv_chunk_schema, dialect, stats, import_id, error_columns_schema_for_insert)
    ):
        if chunk:
            _log_status("inserting_chunk:%d" % i)
            try:
                _insert_chunk(
                    chunk,
                    fmt,
                    table_name,
                    csv_chunk_schema,
                    output_dialect,
                    max_execution_time=max_execution_time,
                    ch_summaries=ch_summaries,
                )
            finally:
                _log_status("done_inserting_chunk:%d" % i)

        if quarantine_chunk and with_quarantine:
            # If we have a quarantine rows to insert, but the table does not exist yet. Let's create it
            if create_quarantine_table:
                try:
                    create_quarantine_table_from_landing_sync(
                        landing_datasource_name=table_name,
                        database_server=database_server,
                        database=database,
                        cluster=cluster,
                        quarantine_columns=quarantine_table_columns,
                    )
                    create_quarantine_table = False
                except Exception as e:
                    logging.error(f"Unable to create quarantine table in CH: {str(e)}")
                    continue

            try:
                _insert_chunk(
                    quarantine_chunk,
                    fmt,
                    table_name + "_quarantine",
                    csv_chunk_schema + error_columns_schema_for_insert,
                    output_dialect,
                    max_execution_time=max_execution_time,
                    ch_summaries=quarantine_ch_summaries,
                )
            except InsertCHException as e:
                # Keep ch_summaries on quarantine attribute
                e.ch_summaries_quarantine = e.ch_summaries
                e.ch_summaries = []
                raise e

    stats[0].update(
        {
            "db_stats": [ch_summary.to_dict() for ch_summary in ch_summaries],
            "quarantine_db_stats": [ch_summary.to_dict() for ch_summary in quarantine_ch_summaries],
        }
    )
    return stats


def insert_query(columns, table_name, fmt="CSV"):
    columns_list = ",".join(f"`{x['normalized_name']}`" for x in columns if not x["auto"])
    return 'INSERT INTO "%s" (%s) FORMAT %s' % (table_name, columns_list, fmt)


class CheckException(Exception):
    def __init__(self, msg, column):
        self.column = column
        Exception.__init__(self, msg)


def is_convertible_type(s):
    return s != "String" and not s.startswith("Array") and not s.startswith("SimpleAggregateFunction")


def _find_field_casting_expression(
    field_name: str, field_type: str, nullable: bool, force_low_cardinality_to_string: bool = False
) -> str:
    if "Tuple" in field_type:
        return field_name
    elif field_type.startswith("Nullable"):
        match = re.search(r"Nullable\s*\((.*)\)", field_type)
        if not match:
            raise CheckException(f"Failed to parse field type {field_type}", field_name)
        return _find_field_casting_expression("x", match.group(1), True, force_low_cardinality_to_string)
    elif field_type.startswith("Array"):
        match = re.search(r"Array\s*\((.*)\)", field_type)
        if not match:
            raise CheckException(f"Failed to parse field type {field_type}", field_name)
        casting_expression = _find_field_casting_expression(
            "x", match.group(1), nullable, force_low_cardinality_to_string=True
        )
        return f"arrayMap(x -> {casting_expression}, `{field_name}`)"
    elif "DateTime64" in field_type:
        match = EXTRACT_TYPE_PARAMS.search(field_type)
        params = "," + match.group(1) if match is not None else ""
        if nullable:
            return f"if(empty(toString(`{field_name}`)), null, parseDateTime64BestEffortOrNull(toString(`{field_name}`){params}))"
        return f"parseDateTime64BestEffort(toString(`{field_name}`){params})"
    elif "DateTime" in field_type:
        match = EXTRACT_TYPE_PARAMS.search(field_type)
        params = "," + match.group(1) if match is not None else ""
        if nullable:
            return f"if(empty(toString(`{field_name}`)), null, parseDateTimeBestEffortOrNull(toString(`{field_name}`){params}))"
        return f"parseDateTimeBestEffort(toString(`{field_name}`){params})"
    elif field_type == "Date":
        if nullable:
            return f"if(empty(toString(`{field_name}`)), null, toDate(parseDateTimeBestEffortOrNull(toString(`{field_name}`))))"
        return f"toDate(parseDateTimeBestEffort(toString(`{field_name}`)))"
    elif field_type.startswith("FixedString"):
        match = EXTRACT_TYPE_PARAMS.search(field_type)
        params = "," + match.group(1) if match is not None else ""
        return f"toFixedString(`{field_name}`{params})"
    elif field_type.startswith("Decimal"):
        parsed_decimal = parse_decimal_type(field_type)
        if not parsed_decimal:
            raise CheckException(f"Failed to parse field type {field_type}", field_name)
        b, p, s = parsed_decimal
        func_name = f"toDecimal{b}OrNull" if nullable else f"toDecimal{b}"
        return f"{func_name}(toString(`{field_name}`), {s})"
    elif is_convertible_type(field_type):
        if "LowCardinality" in field_type:
            if force_low_cardinality_to_string:
                return f"toString(`{field_name}`)"
            return f"CAST(toString(`{field_name}`) AS {field_type})"
        if nullable:
            # FIXME: xOrNull functions will accept invalid values in Nullable fields and toX functions will ignore
            # some overflows, causing inconsistencies between the ClickHouse and the Python parsers.
            # Check https://gitlab.com/tinybird/analytics/-/issues/14126 for more details.
            if field_type == "Bool":
                return f"accurateCastOrNull(`{field_name}`, 'Bool')"
            return f"to{field_type}OrNull(toString(`{field_name}`))"
        else:
            return f"to{field_type}(toString(`{field_name}`))"
    else:
        return field_name


def cast_column(name: str, _type: str, nullable: bool) -> str:
    field_casting_expression = _find_field_casting_expression(name, _type, nullable)

    if field_casting_expression == name:  # If we don't need to cast then we don't need to alias.
        return field_casting_expression
    else:
        return f"{field_casting_expression} as `{name}`"


# TODO: We should create a hypothesis test to check if the clickhouse-local is able to parse any given chunk of CSV data
def convert_to_native(encoded_chunk, columns, dialect):
    try:
        with Timer("clickhouse csv processing") as timing:
            query = "select %s from table" % ",".join(
                [cast_column(x["normalized_name"], x["type"], x["nullable"]) for x in columns]
            )
            logging.debug(query)
            # remap date columns to string
            parsing_columns = []
            for c in columns:
                x = c.copy()
                # change
                if is_convertible_type(x["type"]):
                    x["type"] = "String"
                parsing_columns.append(x)
            extra_options = {}
            if dialect["delimiter"] in [" ", "\t"]:
                input_format = "CustomSeparated"
                extra_options["format_custom_field_delimiter"] = dialect["delimiter"]
                extra_options["format_custom_escaping_rule"] = "CSV"
            else:
                input_format = "CSV"

            processed_data = CHTable(parsing_columns).query(
                data=encoded_chunk,
                query=query,
                input_format=input_format,
                output_format="Native",
                dialect=dialect,
                extra_options=extra_options,
            )

        stats = {
            "lines": -1,
            "parser": "clickhouse",
            "invalid_lines": 0,
            "quarantine": 0,
            "time": timing.interval,
            "empty_lines": 0,
            "bytes": len(encoded_chunk),
        }
        return processed_data, stats
    except Exception as e:
        logging.exception("failed processing chunk with clickhouse-local %s" % e)
        raise e


def quote(s):
    """
    >>> quote('"SEGOHOUSE" ASESORES INMOBILIARIOS')
    '"\"\"SEGOHOUSE\"\" ASESORES INMOBILIARIOS\"'
    >>> quote('\\\\N')
    '\\\\N'
    """
    if s == "\\N":
        return s
    return '"' + s.replace('"', '""') + '"'


NEWLINE = "\n"
DELIMITER = ","


class QuarantineRowsAccumulator:
    def __init__(self, error_columns_to_use: Optional[List[Any]], import_id: Optional[str]):
        if error_columns_to_use is None:
            self._error_column_names_available = set()
        else:
            self._error_column_names_available = set([column["name"] for column in error_columns_to_use])

        self._quarantine_rows: List[list] = []
        self._import_id = import_id

    def append_to_quaratine_rows(self, columns_with_data, column_errors_array, errors_array):
        error_data = []
        # Maintain here the same order as the order in the ERROR_COLUMNS
        if "c__error_column" in self._error_column_names_available:
            error_data.append(column_errors_array)

        if "c__error" in self._error_column_names_available:
            error_data.append(errors_array)

        if "c__import_id" in self._error_column_names_available:
            error_data.append(self._import_id)

        self._quarantine_rows.append(columns_with_data + error_data)

    def __len__(self):
        return len(self._quarantine_rows)

    def get_as_csv(self):
        return csv_from_python_object(self._quarantine_rows).encode("utf-8")


def process_chunk(
    chunk,
    data_table_schema: List[Any],
    dialect: Dict[str, Any],
    stats: List[Dict[Any, Any]],
    import_id: Optional[str] = None,
    error_columns_schema_for_insert: Optional[List[Any]] = None,
    use_native: bool = True,
):
    column_number = len(data_table_schema)

    encoded = chunk.encode()
    db_parse_error = None

    output_dialect = {
        "delimiter": DELIMITER,
        "new_line": NEWLINE,
    }

    if use_native:
        try:
            data, ch_stats = convert_to_native(encoded, data_table_schema, dialect)
            yield data, "Native", output_dialect, None
            stats.append(ch_stats)
            return
        except Exception as e:
            db_parse_error = str(CHException(str(e)))
            # error processing with clickhouse, fallback to python...

    reader = csv.reader(
        StringIO(chunk, newline=None), delimiter=dialect["delimiter"], escapechar=dialect.get("escapechar", None)
    )

    quarantine_row_accumulator = QuarantineRowsAccumulator(error_columns_schema_for_insert, import_id)

    def none(s):
        return s if s else "\\N"

    def type_checker(_type, column_name, nullable):
        def _f(s):
            type_to_check = _type
            if is_type_datetime64(_type):
                type_to_check = "DateTime64"
            elif is_type_datetime(_type):
                type_to_check = "DateTime"
            if nullable and (not s or s == "\\N"):
                return s
            if not testers[type_to_check](s):
                raise CheckException("value '%s' on column '%s' is not %s" % (s, column_name, _type), column_name)
            return s

        def _check_decimal(min_value, max_value, value):
            if nullable and (not value or value == "\\N"):
                return value
            try:
                decimal_value = Decimal(value)
                if min_value <= decimal_value <= max_value:
                    return value
            except DecimalException:
                pass
            raise CheckException("value '%s' on column '%s' is not %s" % (value, column_name, _type), column_name)

        if is_type_decimal(_type):
            dec_b, dec_p, dec_s = parse_decimal_type(_type)  # Avoid variable name collision
            min_value, max_value = get_decimal_limits(dec_p, dec_s)
            return lambda value: _check_decimal(min_value, max_value, value)

        return _f

    def check_null(column_name):
        def _f(s):
            if not s or s == "\\N":
                raise CheckException("Null value not allowed on column '%s'" % column_name, column_name)
            return s

        return _f

    def get_processor(x):
        processors = []
        if (
            x["type"]
            not in (
                "Float32",
                "Float64",
                "Int8",
                "UInt8",
                "Int16",
                "UInt16",
                "UInt32",
                "Int32",
                "UInt64",
                "Int64",
                "Int128",
                "UInt128",
                "Int256",
                "UInt256",
                "Date",
                "DateTime",
                "DateTime64",
                "Bool",
            )
            and not is_type_datetime64(x["type"])
            and not is_type_datetime(x["type"])
            and not parse_decimal_type(x["type"])
        ):
            processors.append(quote)
        else:
            processors.append(type_checker(x["type"], x["normalized_name"], x["nullable"]))

        if not x["nullable"]:
            processors.append(check_null(x["normalized_name"]))
        else:
            processors.append(none)

        def _f(xx):
            for fn in processors:
                xx = fn(xx)
            return xx

        return _f

    processors = [get_processor(x) for x in data_table_schema]

    logging.info("processing chunk %.2f mb" % (len(chunk) / (1024 * 1024.0)))

    def prepare_chunk(buff, use_native=True):
        uniform_csv_chunk = NEWLINE.join(buff).encode("utf8")
        if use_native:
            try:
                data, _ = convert_to_native(uniform_csv_chunk, data_table_schema, output_dialect)
                return data, "Native", output_dialect, None
            except Exception as e:
                logging.exception("failed to normalize the CSV: %s", e)
                raise Exception(f"failed to normalize the CSV chunk: {CHException(str(e))}") from e
        else:
            return uniform_csv_chunk, "CSV", output_dialect, None

    with Timer() as timing:
        valid_rows = []
        empty_lines = 0
        total_lines = 0
        invalid_lines = 0
        cached_header = dialect.get("header", None)
        for r in reader:
            total_lines += 1
            row: List[Any] = list(r)

            if len(row) == 0:
                empty_lines += 1

            elif len(row) == column_number:
                # omit the header
                if cached_header and row == ast.literal_eval(cached_header):
                    quarantine_row_accumulator.append_to_quaratine_rows(row, [], ["Found header row in wrong position"])
                    invalid_lines += 1
                    continue

                clean_row = []
                cleaning_errors = []
                for p, x in zip(processors, row, strict=True):
                    try:
                        clean_row.append(p(x))
                    except CheckException as e:
                        cleaning_errors.append({"column": e.column, "error": str(e)})
                if cleaning_errors:
                    column_errors_array = [x["column"] for x in cleaning_errors]
                    errors_array = [x["error"] for x in cleaning_errors]
                    quarantine_row_accumulator.append_to_quaratine_rows(row, column_errors_array, errors_array)
                else:
                    valid_rows.append(DELIMITER.join(clean_row))

                if len(valid_rows) > 0 and len(valid_rows) % 100000 == 0:
                    yield prepare_chunk(valid_rows, use_native=use_native)
                    valid_rows = []

            else:
                row_columns = len(row)
                column_errors_array = []
                errors_array = [f"Row contains {row_columns} columns, expected {column_number}"]
                if row_columns > column_number:
                    quarantine_row = row[: column_number - 1]
                    quarantine_row.append(json.dumps(row[column_number - 1 :], separators=(",", ":")))
                else:
                    quarantine_row = row[:] + ([None] * (column_number - row_columns))
                quarantine_row_accumulator.append_to_quaratine_rows(quarantine_row, column_errors_array, errors_array)

                invalid_lines += 1

        if len(valid_rows) > 0:
            logging.info("remaining rows: %d" % len(valid_rows))
            yield prepare_chunk(valid_rows, use_native=use_native)

        if len(quarantine_row_accumulator) > 0:
            yield None, "CSV", output_dialect, quarantine_row_accumulator.get_as_csv()

    logging.info(
        "finished processing chunk (time: %f s), processed %d lines (%d quarantine, %d empty)"
        % (timing.interval, total_lines, len(quarantine_row_accumulator), empty_lines)
    )
    stats.append(
        {
            "lines": total_lines,
            "parser": "python",
            "quarantine": len(quarantine_row_accumulator),
            "time": timing.interval,
            "invalid_lines": invalid_lines,
            "empty_lines": empty_lines,
            "bytes": len(chunk),
            "db_parse_error": db_parse_error,
        }
    )


class CsvChunkQueue:
    def __init__(self, workers, app_name, debug):
        self.app_name = app_name
        self.debug = debug
        self.queue: "JoinableQueue[Tuple[str, Block]]" = JoinableQueue()
        self.queues = []
        self.queues_blocks = {}
        self.queues_results = {}
        self.blocks_results = {}
        self.block_status_log = {}
        self.processed_queue = Queue()
        self.block_log_queue = Queue()
        self.last_dummy_block_processed_at = datetime.utcnow()
        self.supervisor = None
        self.dummy_supervisor = None
        self.workers = workers

        # variables to simulate qsize in osx
        self.blocks_in_count = 0
        self.blocks_out_count = 0
        self.exiting_event = Event()
        self.fn = import_csv_chunk
        self.started_processes_barrier = Barrier(workers + 1)

        if self.workers > 0:
            logging.info(f"Creating {workers} CSV worker processes")
            self.processes = [
                Process(
                    target=process_csv_chunk,
                    name=f"ProcessCsvChunk-{i}",
                    args=(
                        i,
                        self.queue,
                        self.block_log_queue,
                        self.fn,
                        self.processed_queue,
                        self.started_processes_barrier,
                        self.app_name,
                        self.debug,
                    ),
                )
                for i in range(workers)
            ]

            self.threads = [
                threading.Thread(target=self._consume_blocks_log, name="consume_blocks_log"),
                threading.Thread(target=self._consume_processed_blocks, name="consume_processed_blocks"),
            ]
        else:
            self.processes = []
            self.threads = []

    def start(self):
        for p in self.processes:
            p.start()
        for t in self.threads:
            t.start()
        self.started_processes_barrier.wait()

    def start_supervisor(self):
        def _supervisor():
            while not self.exiting_event.is_set():
                killed = False
                for p in self.processes:
                    if not p.is_alive() and not self.exiting_event.is_set():
                        logging.critical(f"Process PID={p.pid} {p} not alive, Application is going to shutdown")
                        # Signal the main process for performing cleanup operations
                        killed = True
                        os.kill(os.getpid(), signal.SIGTERM)
                        break
                if killed:
                    break
                self.exiting_event.wait(5)

        self.supervisor = threading.Thread(name="QueueProcessesSupervisor", daemon=True, target=_supervisor)
        self.supervisor.start()

    def start_dummy_block_supervisor(self):
        def _supervisor():
            while not self.exiting_event.is_set():
                q = queue.Queue()
                results = []
                block_log = []
                self.process_queue(q, results, block_log)
                q.put(
                    Block(
                        id=DUMMY_BLOCK_ID,
                        table_name=None,
                        data=None,
                        database_server=None,
                        database=None,
                        cluster=None,
                        dialect=None,
                        import_id=None,
                        max_execution_time=None,
                        csv_columns=None,
                        quarantine=False,
                    )
                )
                q.join()
                done = next((e for e in block_log if e.get("status", None) == "done"), None)
                if done and isinstance(done.get("timestamp", None), datetime):
                    self.last_dummy_block_processed_at = done["timestamp"]
                self.remove_queue(q)
                self.exiting_event.wait(15)

        self.dummy_supervisor = threading.Thread(name="QueueDummyBlockSupervisor", daemon=True, target=_supervisor)
        self.dummy_supervisor.start()

    def blocks_waiting(self):
        try:
            return self.queue.qsize()
        except NotImplementedError:
            # osx does not implement this
            return self.blocks_in_count - self.blocks_out_count

    def _consume_blocks_log(self):
        while True:
            block_id, res = self.block_log_queue.get()
            if block_id is None:
                break
            logging.debug("block_log %s" % res)
            block_status_log = self.block_status_log.get(block_id, None)
            if block_status_log is not None:
                block_status_log.append(res)

    def _consume_processed_blocks(self):
        while True:
            next_block = self.processed_queue.get()
            if not next_block:
                break
            block_id, res = next_block
            q = self.queues_blocks.get(block_id, None)
            if q:
                self.blocks_out_count += 1
                # add result to the list
                res_list = self.queues_results.get(block_id, None)
                self.blocks_results[block_id] = res
                if res_list is not None:
                    res_list.append(res)
                block_status_log = self.block_status_log.get(block_id, None)
                if block_status_log is not None:
                    block_status_log.append(
                        {"block_id": res["block_id"], "status": "done", "timestamp": datetime.utcnow()}
                    )

                q.task_done()
            logging.debug(block_id + " processed")

    def process(self, block: Block):
        id = str(uuid.uuid4())
        self.queue.put((id, block))
        return id

    def remove_queue(self, queue):
        if queue in self.queues:
            queue.put(None)
        else:
            raise ValueError("queue not in processed queues, process_queue must be called before removing it")

    def process_queue(self, queue: queue.Queue, res_list=None, block_status_log=None):
        self.queues.append(queue)

        def consume_queue():
            logging.debug(f"queue thread started Queue={id(queue)}")
            while True:
                block = queue.get()

                if isinstance(block, Block):
                    if block.id is not DUMMY_BLOCK_ID:
                        logging.info(
                            f"Queue={id(queue)} "
                            f"Block_id={block.id} "
                            f"table_name={block.table_name} "
                            f"database_server={block.database_server} "
                            f"database={block.database}"
                        )
                elif block is not None:
                    logging.info(f"Queue={id(queue)}; {type(block)} Block")
                if block is None:
                    self.queues.remove(queue)
                    blocks_to_clear = [k for k, v in self.queues_blocks.items() if v == queue]

                    for x in blocks_to_clear:
                        if x in self.queues_results:
                            del self.queues_results[x]
                        if x in self.queues_blocks:
                            del self.queues_blocks[x]
                        if x in self.blocks_results:
                            del self.blocks_results[x]
                        if x in self.block_status_log:
                            del self.block_status_log[x]
                    queue.task_done()
                    logging.debug(f"finishing thread Queue={id(queue)}")
                    break
                # do not use process since it could lead to a race condition
                block_id = str(uuid.uuid4())
                if res_list is not None:
                    self.queues_results[block_id] = res_list
                if block_status_log is not None:
                    self.block_status_log[block_id] = block_status_log

                self.queues_blocks[block_id] = queue
                self.blocks_in_count += 1
                self.queue.put((block_id, block))

        ths = threading.Thread(target=consume_queue, name="csv_process_queue")
        ths.start()

    # Wait until all the tasks are processed. MEANT FOR TESTS ONLY
    def wait_for_queue(self):
        logging.warning(f"[CSV processing QUEUE] Waiting - PID: {os.getpid()}")
        self.queue.join()

    def terminate(self):
        """wait until queue is empty and terminate processes"""
        if self.exiting_event.is_set():
            logging.warning(f"[CSV processing QUEUE] Already terminating - Queue: {self.queue}, PID: {os.getpid()}")
            return

        logging.info(f"[CSV processing QUEUE] Terminating - Queue: {self.queue}, PID: {os.getpid()}")
        self.exiting_event.set()
        if self.supervisor:
            self.supervisor.join()
        if self.dummy_supervisor:
            self.dummy_supervisor.join()

        self.processed_queue.put(None)
        self.block_log_queue.put((None, None))

        # We need to send a None block so that processes that are processing them know that
        # they need to exit their while-true loop.
        for p in self.processes:
            if p.is_alive():
                self.process(None)

        logging.info(
            f"[CSV processing QUEUE] Waiting for main queue {self.queue}: {len(self.processes)} processes - PID: {os.getpid()}"
        )
        alive = 1
        retries = 0
        killed = False
        while alive:
            retries += 1
            alive = 0
            for p in self.processes:
                if p.is_alive():
                    alive = 1
                    if retries < 30:
                        logging.debug(f"{p.pid} is alive. Trying to JOIN - PID: {os.getpid()}")
                        p.join(timeout=0.5)
                    else:
                        logging.exception(f"{p.pid} is NOT DEAD. SIGKILL - PID: {os.getpid()}")
                        killed = True
                        p.kill()

        # In case we have killed any of the processes, we can't join the queue anymore
        # because there will most likely be some block not processed.
        if not killed:
            self.wait_for_queue()
            logging.info(f"JOINED Main queue {self.queue} - PID: {os.getpid()}")


def process_csv_chunk(
    worker_id,
    queue: "JoinableQueue[Tuple[str, Block]]",
    block_log_queue,
    fn,
    processed_queue,
    started_processes_barrier,
    app_name,
    debug,
):
    setproctitle("tinybird_server csv_worker")

    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, signal.SIG_IGN)

    from tinybird.utils.log import configure_logging

    configure_logging(app_name, debug)

    logging.info(f"[CSV processing QUEUE] Starting process #{worker_id} - PID: {os.getpid()}")
    started_processes_barrier.wait()

    while True:
        try:
            _id, block = queue.get(timeout=0.5)
        except Exception:
            continue

        if block is None:
            logging.info(f"[CSV processing QUEUE] Process #{worker_id} - PID: {os.getpid()} received None block")
            queue.task_done()
            break

        (
            block_id,
            table_name,
            data,
            database_server,
            database,
            cluster,
            dialect,
            import_id,
            chunk_max_execution_time,
            csv_columns,
            with_quarantine,
        ) = block

        error = None
        error_type = None
        res: Optional[Union[str, List[dict]]] = None
        with Timer("processing block %s" % block_id) as timing:
            try:
                block_log_queue.put(
                    (_id, {"block_id": block_id, "status": "processing", "timestamp": datetime.utcnow()})
                )
                block_log: List[Any] = []
                if block_id == DUMMY_BLOCK_ID:
                    res = f"{DUMMY_BLOCK_ID}-OK"
                else:
                    res = fn(
                        data,
                        table_name,
                        database_server=database_server,
                        dialect=dialect,
                        database=database,
                        cluster=cluster,
                        block_status_log=block_log,
                        import_id=import_id,
                        max_execution_time=chunk_max_execution_time,
                        csv_columns=csv_columns,
                        with_quarantine=with_quarantine,
                    )
                for x in block_log:
                    block_log_queue.put(
                        (_id, {"block_id": block_id, "status": x["status"], "timestamp": x["timestamp"]})
                    )
            except (CHException, Exception, InsertCHException) as e:
                error_type = "ClickHouse" if isinstance(e, CHException) else "Exception"
                error = str(e)
                block_log_queue.put(
                    (_id, {"block_id": block_id, "status": "processing_error", "timestamp": datetime.utcnow()})
                )
                logging.exception(e)
                if isinstance(e, InsertCHException):
                    ch_summaries = e.ch_summaries
                    quarantine_ch_summaries = e.ch_summaries_quarantine
                    res = [
                        {
                            "db_stats": [ch_summary.to_dict() for ch_summary in ch_summaries],
                            "quarantine_db_stats": [ch_summary.to_dict() for ch_summary in quarantine_ch_summaries],
                        }
                    ]
        queue.task_done()
        # TODO: errors

        processed_queue.put(
            (
                _id,
                {
                    "block_id": block_id,
                    "process_return": res,
                    "processing_time": timing.interval,
                    "processing_error": error,
                    "processing_error_type": error_type,
                },
            )
        )
    logging.info(f"[CSV processing QUEUE] Ending process #{worker_id} - PID: {os.getpid()}")


if __name__ == "__main__":

    def dummy(*args, **kwargs):
        time.sleep(0.5)
        print("dummy", args)  # noqa: T201
        return args[1]

    class DummyCsvChunkQueue(CsvChunkQueue):
        def __init__(self):
            CsvChunkQueue.__init__(self, CsvChunkQueueRegistry.DEFAULT_WORKERS)
            self.fn = dummy

    r = DummyCsvChunkQueue()
    r.start()

    q0: queue.Queue = queue.Queue()
    res0: List = []
    r.process_queue(q0, res0)
    for x in range(8):
        block = (f"b_id_{x}", "A", f"data-A-{x}".encode(), "database_server", "database", "dialect")
        q0.put(block)
    q0.put(None)

    q1: queue.Queue = queue.Queue()
    res1: List = []
    r.process_queue(q1, res1)
    for x in range(2):
        # block_id, table_name, data, database_server, database, dialect = block
        block = (f"b_id_{x}", "B", f"data-B-{x}".encode(), "database_server", "database", "dialect")
        q1.put(block)
    q1.put(None)

    q0.join()
    q1.join()
    r.queue.join()
    print("results-0", res0)  # noqa: T201
    print("results-1", res1)  # noqa: T201
    r.terminate()
