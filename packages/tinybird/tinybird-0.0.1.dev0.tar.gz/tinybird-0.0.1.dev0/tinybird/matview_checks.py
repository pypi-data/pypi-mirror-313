import json
import logging
import re
from typing import Dict, List, Optional, Tuple

from chtoolset import query as chquery
from chtoolset.query import check_compatible_types

from tinybird.ch import HTTPClient
from tinybird.ch_utils.exceptions import CHException
from tinybird.datatypes import nullable_types

from .views.api_errors.datasources import MatviewDatasourceError
from .views.api_errors.pipes import SQLPipeError


class EngineTypes:
    MERGE_TREE = "MergeTree"
    REPLACING_MERGE_TREE = "ReplacingMergeTree"
    SUMMING_MERGE_TREE = "SummingMergeTree"
    AGGREGATING_MERGE_TREE = "AggregatingMergeTree"
    COLLAPSING_MERGE_TREE = "CollapsingMergeTree"
    VERSIONED_COLLAPSING_MERGE_TREE = "VersionedCollapsingMergeTree"
    JOIN = "Join"
    DISTRIBUTED = "Distributed"


GROUPABLE_ENGINES = [
    EngineTypes.SUMMING_MERGE_TREE,
    EngineTypes.AGGREGATING_MERGE_TREE,
    EngineTypes.DISTRIBUTED,  # Accepted for internal / metrics tables
]

AGGREGATE_FUNCTION_NAME = "AggregateFunction"
SIMPLE_AGGREGATE_FUNCTION_NAME = "SimpleAggregateFunction"


def aggregated_function_in_type(column_type):
    return AGGREGATE_FUNCTION_NAME in column_type or SIMPLE_AGGREGATE_FUNCTION_NAME in column_type


class SQLValidationException(Exception):
    pass


def origin_column_type_is_compatible_with_destination_type(origin: str, destination: str) -> Tuple[bool, Optional[str]]:
    """
    >>> origin_column_type_is_compatible_with_destination_type('Int32', 'Int64')
    (True, None)
    >>> origin_column_type_is_compatible_with_destination_type('Int64', 'String')
    (False, 'Automatic conversion from Int64 to String is not supported: Automatic casting to String is disallowed.')
    >>> origin_column_type_is_compatible_with_destination_type('Int32', 'UInt64')
    (False, "Automatic conversion from Int32 to UInt64 is not supported: Int32 might contain values that won't fit inside a column of type UInt64.")
    >>> origin_column_type_is_compatible_with_destination_type('Int64', 'Int32')
    (False, "Automatic conversion from Int64 to Int32 is not supported: Int64 might contain values that won't fit inside a column of type Int32.")
    >>> origin_column_type_is_compatible_with_destination_type("Date", "DateTime")
    (True, None)
    >>> origin_column_type_is_compatible_with_destination_type("DateTime", "DateTime")
    (True, None)
    >>> origin_column_type_is_compatible_with_destination_type("DateTime", "DateTime64")
    (True, None)
    >>> origin_column_type_is_compatible_with_destination_type("DateTime('Europe/Madrid')", "DateTime('Europe/Madrid')")
    (True, None)
    >>> origin_column_type_is_compatible_with_destination_type('AggregateFunction(count)', 'AggregateFunction(count)')
    (True, None)
    >>> origin_column_type_is_compatible_with_destination_type('AggregateFunction(avg, Int64)', 'AggregateFunction(count)')
    (False, 'Automatic conversion from AggregateFunction(avg, Int64) to AggregateFunction(count) is not supported: Incompatible aggregate functions: avg vs count.')
    >>> origin_column_type_is_compatible_with_destination_type('TEXT', 'TEXT')
    (True, None)
    >>> origin_column_type_is_compatible_with_destination_type("DateTime('Etc/UTC')", "DateTime")
    (True, None)
    >>> origin_column_type_is_compatible_with_destination_type("DateTime", "DateTime('Etc/UTC')")
    (True, None)
    >>> origin_column_type_is_compatible_with_destination_type("LowCardinality(String)", "String")
    (True, None)
    >>> origin_column_type_is_compatible_with_destination_type("String", "LowCardinality(String)")
    (True, None)
    >>> origin_column_type_is_compatible_with_destination_type("LowCardinality(Int32)", "Int16")
    (False, "Automatic conversion from LowCardinality(Int32) to Int16 is not supported: LowCardinality(Int32) might contain values that won't fit inside a column of type Int16.")
    >>> origin_column_type_is_compatible_with_destination_type("Int32", "LowCardinality(Int16)")
    (False, "Automatic conversion from Int32 to LowCardinality(Int16) is not supported: Int32 might contain values that won't fit inside a column of type LowCardinality(Int16).")
    >>> origin_column_type_is_compatible_with_destination_type("LowCardinality(Int16)", "Int32")
    (True, None)
    >>> origin_column_type_is_compatible_with_destination_type("LowCardinality(DateTime)", "DateTime64")
    (True, None)
    >>> origin_column_type_is_compatible_with_destination_type("LowCardinality(Nullable(String))", "String")
    (False, "Automatic conversion from LowCardinality(Nullable(String)) to String is not supported: LowCardinality(Nullable(String)) might contain values that won't fit inside a column of type String.")
    >>> origin_column_type_is_compatible_with_destination_type("Nullable(String)", "String")
    (False, "Automatic conversion from Nullable(String) to String is not supported: Nullable(String) might contain values that won't fit inside a column of type String.")
    >>> origin_column_type_is_compatible_with_destination_type("Nullable(Int32)", "Int32")
    (False, "Automatic conversion from Nullable(Int32) to Int32 is not supported: Nullable(Int32) might contain values that won't fit inside a column of type Int32.")
    >>> origin_column_type_is_compatible_with_destination_type("String", "LowCardinality(Nullable(String))")
    (True, None)
    """
    exception_message = f"Automatic conversion from {origin} to {destination} is not supported"
    try:
        check_compatible_types(origin, destination)
        return True, None
    except ValueError as e:
        return False, f"{exception_message}: {str(e)}."


def columns_in_pipe_and_not_in_table(pipe_columns: Dict[str, str], table_columns: Dict[str, str]) -> list:
    """
    >>> columns_in_pipe_and_not_in_table({'a': 'String', 'b': 'String'}, {'a': 'String', 'b': 'String'})
    []
    >>> columns_in_pipe_and_not_in_table({'a': 'String', 'b': 'String'}, {'a': 'String', 'b': 'String', 'c': 'String'})
    []
    >>> columns_in_pipe_and_not_in_table({'a': 'String', 'c': 'String'}, {'a': 'String', 'b': 'String'})
    ['c']
    >>> columns_in_pipe_and_not_in_table({'a': 'String', 'd': 'String'}, {'a': 'String', 'b': 'String', 'c': 'String'})
    ['d']
    >>> columns_in_pipe_and_not_in_table({'a.b': 'String', 'a.c': 'String'}, {'a': 'String', 'b': 'String', 'c': 'String'})
    ['a.b', 'a.c']
    """
    pipe_names = set(map(lambda column: column, pipe_columns))
    table_names = set(map(lambda column: column, table_columns))
    return sorted(pipe_names.difference(table_names))


def check_column_types_match(columns, schema, is_cli=False, is_from_ui=False):
    """
    >>> check_column_types_match([{'name':'a', 'type':'String'}], [{'name':'a', 'type':'String'},{'name':'b', 'type':'Int32'}])

    >>> check_column_types_match([{'name':'a', 'type':'String'},{'name':'b', 'type':'Int32'}], [{'name':'a', 'type':'String'},{'name':'b', 'type':'Int32'}])

    >>> check_column_types_match([{'name':'a', 'type':'String'},{'name':'b', 'type':'Int32'}], [{'name':'a', 'type':'String'},{'name':'b', 'type':'Int64'}])

    >>> check_column_types_match([{'name':'a', 'type':'String'},{'name':'b', 'type':'Int32'}], [{'name':'a', 'type':'String'},{'name':'b', 'type':'Nullable(Int64)'}])

    >>> check_column_types_match([{'name':'a', 'type':'String'},{'name':'b', 'type':'Int32', 'nullable': False}], [{'name':'a', 'type':'String'},{'name':'b', 'type':'Int64', 'nullable': True}])

    >>> check_column_types_match([{'name':'a', 'type':'String'},{'name':'b', 'type':'Int32'}], [{'name':'a', 'type':'String'},{'name':'b', 'type':'SimpleAggregateFunction(sum, Nullable(Int64))'}])

    >>> check_column_types_match([{'name': 'sum_units', 'type': 'AggregateFunction(sum, Int32)'}], [{'name': 'sum_units', 'type': 'AggregateFunction(sum, Int32)'}])

    >>> check_column_types_match([{'name': 'b', 'type': "DateTime('Europe/Madrid')"}, {'name': 'c', 'type': 'AggregateFunction(count)'}], [{'name': 'b', 'type': "DateTime('Europe/Madrid')"}, {'name': 'c', 'type': 'AggregateFunction(count)'}])

    >>> check_column_types_match([{'name':'a', 'type':'String'},{'name':'b', 'type':'Int32'}], [{'name':'a', 'type':'String'}])
    Traceback (most recent call last):
    ...
    tinybird.matview_checks.SQLValidationException: The pipe has columns ['b'] not found in the destination Data Source.
    >>> check_column_types_match([{'name':'a', 'type':'String'},{'name':'b', 'type':'Int32'}], [{'name':'a', 'type':'String'}, {'name':'b', 'type':'String'}])
    Traceback (most recent call last):
    ...
    tinybird.matview_checks.SQLValidationException: Incompatible column types {'b': 'String'} (Data Source) != {'b': 'Int32'} (pipe): Automatic conversion from Int32 to String is not supported: Automatic casting to String is disallowed.
    >>> check_column_types_match([{'name':'a', 'type':'String'},{'name':'b', 'type':'Int32'}], [{'name':'a', 'type':'String'}, {'name':'c', 'type':'Int32'}])
    Traceback (most recent call last):
    ...
    tinybird.matview_checks.SQLValidationException: The pipe has columns ['b'] not found in the destination Data Source.
    >>> check_column_types_match([{'name':'a', 'type':'String'},{'name':'b', 'type':'Int32', 'nullable': True}], [{'name':'a', 'type':'String'},{'name':'b', 'type':'Int64', 'nullable': False}])
    Traceback (most recent call last):
    ...
    tinybird.matview_checks.SQLValidationException: Incompatible column types {'b': 'Int64'} (Data Source) != {'b': 'Nullable(Int32)'} (pipe): Automatic conversion from Nullable(Int32) to Int64 is not supported: Nullable(Int32) might contain values that won't fit inside a column of type Int64.
    >>> check_column_types_match([{'name':'b', 'type':'LowCardinality(String)', 'nullable': True}], [{'name':'b', 'type':'LowCardinality(String)', 'nullable': False}])
    Traceback (most recent call last):
    ...
    tinybird.matview_checks.SQLValidationException: Incompatible column types {'b': 'LowCardinality(String)'} (Data Source) != {'b': 'LowCardinality(Nullable(String))'} (pipe): Automatic conversion from LowCardinality(Nullable(String)) to LowCardinality(String) is not supported: LowCardinality(Nullable(String)) might contain values that won't fit inside a column of type LowCardinality(String).
    >>> check_column_types_match([{'name':'b', 'type':'LowCardinality(String)', 'nullable': True}], [{'name':'b', 'type':'LowCardinality(Nullable(String))', 'nullable': False}])
    >>> check_column_types_match([{'name':'b', 'type':'LowCardinality(String)', 'nullable': True}], [{'name':'b', 'type':'LowCardinality(String)', 'nullable': True}])
    >>> check_column_types_match([{'name':'b', 'type':'Array(String)', 'nullable': True}], [{'name':'b', 'type':'Array(String)', 'nullable': False}])
    Traceback (most recent call last):
    ...
    tinybird.matview_checks.SQLValidationException: Incompatible column types {'b': 'Array(String)'} (Data Source) != {'b': 'Array(Nullable(String))'} (pipe): Automatic conversion from Array(Nullable(String)) to Array(String) is not supported: Array(Nullable(String)) might contain values that won't fit inside a column of type Array(String).
    >>> check_column_types_match([{'name':'b', 'type':'Array(String)', 'nullable': True}], [{'name':'b', 'type':'Array(Nullable(String))', 'nullable': False}])
    >>> check_column_types_match([{'name':'b', 'type':'Array(String)', 'nullable': True}], [{'name':'b', 'type':'Array(String)', 'nullable': False}])
    Traceback (most recent call last):
    ...
    tinybird.matview_checks.SQLValidationException: Incompatible column types {'b': 'Array(String)'} (Data Source) != {'b': 'Array(Nullable(String))'} (pipe): Automatic conversion from Array(Nullable(String)) to Array(String) is not supported: Array(Nullable(String)) might contain values that won't fit inside a column of type Array(String).
    >>> check_column_types_match([{'name':'b', 'type':'DateTime(3)', 'nullable': True}], [{'name':'b', 'type':'Nullable(DateTime(3))', 'nullable': False}])
    >>> check_column_types_match([{'name':'b', 'type':'DateTime(3)', 'nullable': True}], [{'name':'b', 'type':'DateTime(3)', 'nullable': False}])
    Traceback (most recent call last):
    ...
    tinybird.matview_checks.SQLValidationException: Incompatible column types {'b': 'DateTime(3)'} (Data Source) != {'b': 'Nullable(DateTime(3))'} (pipe): Automatic conversion from Nullable(DateTime(3)) to DateTime(3) is not supported: Nullable(DateTime(3)) might contain values that won't fit inside a column of type DateTime(3).
    >>> check_column_types_match([{'name':'b', 'type':'Tuple(String, String)', 'nullable': True}], [{'name':'b', 'type':'Tuple(Nullable(String), Nullable(String))', 'nullable': False}])
    >>> check_column_types_match([{'name':'b', 'type':'Tuple(String, String)', 'nullable': True}], [{'name':'b', 'type':'Tuple(String, String)', 'nullable': False}])
    Traceback (most recent call last):
    ...
    tinybird.matview_checks.SQLValidationException: Incompatible column types {'b': 'Tuple(String, String)'} (Data Source) != {'b': 'Tuple(Nullable(String), Nullable(String))'} (pipe): Automatic conversion from Tuple(Nullable(String), Nullable(String)) to Tuple(String, String) is not supported: Tuple(Nullable(String), Nullable(String)) might contain values that won't fit inside a column of type Tuple(String, String).
    >>> check_column_types_match([{'name':'b', 'type':'Tuple(LowCardinality(String), LowCardinality(String))', 'nullable': True}], [{'name':'b', 'type':'Tuple(LowCardinality(Nullable(String)), LowCardinality(Nullable(String)))', 'nullable': False}])
    >>> check_column_types_match([{'name':'b', 'type':'Tuple(LowCardinality(String), LowCardinality(String))', 'nullable': True}], [{'name':'b', 'type':'Tuple(LowCardinality(String), LowCardinality(String))', 'nullable': False}])
    Traceback (most recent call last):
    ...
    tinybird.matview_checks.SQLValidationException: Incompatible column types {'b': 'Tuple(LowCardinality(String), LowCardinality(String))'} (Data Source) != {'b': 'Tuple(LowCardinality(Nullable(String)), LowCardinality(Nullable(String)))'} (pipe): Automatic conversion from Tuple(LowCardinality(Nullable(String)), LowCardinality(Nullable(String))) to Tuple(LowCardinality(String), LowCardinality(String)) is not supported: Tuple(LowCardinality(Nullable(String)), LowCardinality(Nullable(String))) might contain values that won't fit inside a column of type Tuple(LowCardinality(String), LowCardinality(String)).
    >>> check_column_types_match([{'name':'b', 'type':'Array(LowCardinality(String))', 'nullable': True}], [{'name':'b', 'type':'Array(LowCardinality(Nullable(String)))', 'nullable': False}])
    >>> check_column_types_match([{'name':'b', 'type':'Array(LowCardinality(String))', 'nullable': True}], [{'name':'b', 'type':'Array(LowCardinality(String))', 'nullable': False}])
    Traceback (most recent call last):
    ...
    tinybird.matview_checks.SQLValidationException: Incompatible column types {'b': 'Array(LowCardinality(String))'} (Data Source) != {'b': 'Array(LowCardinality(Nullable(String)))'} (pipe): Automatic conversion from Array(LowCardinality(Nullable(String))) to Array(LowCardinality(String)) is not supported: Array(LowCardinality(Nullable(String))) might contain values that won't fit inside a column of type Array(LowCardinality(String)).
    """

    def nullable_column_type(column):
        try:
            result = column["type"]
            if column.get("nullable", None):
                for nullable_type in nullable_types:
                    if nullable_type in column["type"]:
                        matches = re.findall(f"{nullable_type}\(.*\)", column["type"])
                        if matches:
                            for match in matches:
                                result = column["type"].replace(match, f"Nullable({match})")
                        else:
                            result = column["type"].replace(nullable_type, f"Nullable({nullable_type})")
            return result
        except Exception as e:
            logging.exception(e)
            return result

    pipe_columns = dict(map(lambda column: (column["name"], nullable_column_type(column)), columns))
    table_columns = dict(map(lambda column: (column["name"], nullable_column_type(column)), schema))

    extra_columns = columns_in_pipe_and_not_in_table(pipe_columns, table_columns)
    if extra_columns:
        raise SQLValidationException(SQLPipeError.error_columns_match(extra_columns=str(extra_columns)))

    unmmatched_columns_pipe = {}
    unmmatched_columns_table = {}
    is_unmatched = False
    accumulated_error_messages: List[str] = []

    for pipe_column_name, pipe_column_type in pipe_columns.items():
        table_column_type = table_columns[pipe_column_name]

        types_compatible, error_message = origin_column_type_is_compatible_with_destination_type(
            pipe_column_type, table_column_type
        )
        if not types_compatible:
            is_unmatched = True
            unmmatched_columns_pipe[pipe_column_name] = pipe_column_type
            unmmatched_columns_table[pipe_column_name] = table_column_type
            accumulated_error_messages.append(error_message or "")

    if is_unmatched:
        message_error_column_type = ""

        for i in range(len(unmmatched_columns_table)):
            message_error_column_type += f"\n** Column {(i+1)}:"
            message_error_column_type += f"\n\t** Data Source:  {list(unmmatched_columns_table.items())[i]}"
            message_error_column_type += f"\n\t** Pipe:\t {list(unmmatched_columns_pipe.items())[i]}"
            message_error_column_type += f"\n\t** Error:\t {accumulated_error_messages[i]} \n"

        raise SQLValidationException(
            SQLPipeError.error_column_types_match(
                message_error_column_type=message_error_column_type,
                table_columns=str(unmmatched_columns_table),
                pipe_columns=str(unmmatched_columns_pipe),
                is_cli=is_cli,
                is_from_ui=is_from_ui,
                error_messages=" ".join(accumulated_error_messages),
            )
        )


def check_aggregation(
    sql, explains, table_details, group_by_columns_list: Optional[List[str]] = None, check_group_by=True
):
    """
    This method checks if the columns used in the GROUP BY statement match the sorting key defined in the table engine
    It is meant to be used in the engines defined in GROUPABLE_ENGINES

    It checks first if there is a GROUP BY statement present

    If it does, then it checks if the columns are correct
    """

    explains_copy = explains[:]
    explains_copy.reverse()
    sorting_key_list = table_details.sorting_key.replace(" ", "").split(",")

    sql_tokens = sql.replace(" ", "").replace("\n", "").strip().split(",")
    group_by = [sql_token for sql_token in sql_tokens if "groupby" in sql_token.lower()]
    if not group_by:
        raise SQLValidationException(SQLPipeError.error_missing_group_by(sorting_keys=sorting_key_list))

    if check_group_by:
        group_by_columns_list = group_by_columns_list if group_by_columns_list else []
        keys_match_explain = set(group_by_columns_list) == set(sorting_key_list)

        if not keys_match_explain:
            error = SQLPipeError.error_keys_match(
                sorting_keys=", ".join(sorting_key_list),
                group_by_columns=", ".join(group_by_columns_list) if group_by_columns_list else "no columns",
            )
            raise SQLValidationException(error)


def check_if_engine_has_aggregating_functions(engine_full, columns):
    if not _is_aggregating_engine(engine_full):
        agg_column = next((column for column in columns if AGGREGATE_FUNCTION_NAME in column["type"]), None)

        if agg_column:
            error = MatviewDatasourceError.error_aggregate_function_engine(engine_full=engine_full)
            raise SQLValidationException(error)


def check_is_valid_engine(
    sql,
    table_details,
    query_lines,
    columns,
    schema,
    group_by_columns: str,
    check_group_by=True,
    is_cli=False,
    is_from_ui=False,
):
    check_column_types_match(columns, schema, is_cli, is_from_ui)

    if table_details.engine in GROUPABLE_ENGINES:
        group_by_columns_list = group_by_columns.split(",") if group_by_columns else []
        check_aggregation(sql, query_lines, table_details, group_by_columns_list, check_group_by)


def _is_aggregating_engine(engine_full):
    return next((engine for engine in GROUPABLE_ENGINES if engine in engine_full), None)


def _compare_engine_setting(value, setting_value):
    if not value:
        return False

    REPLACE_VALUES = {"`": "", " ": "", "(": "", ")": ""}

    value = value.translate(str.maketrans(REPLACE_VALUES))
    setting_value = setting_value.translate(str.maketrans(REPLACE_VALUES))

    return value != setting_value


def check_engines_match(settings, table_details, datasource, is_cli=False, is_from_ui=False):
    DONT_CHECK = ["ttl"]
    for setting_key, setting_value in settings.items():
        if setting_key.startswith("engine"):
            key = "engine" if setting_key == "engine" else setting_key.replace("engine_", "")

            if key in DONT_CHECK:
                continue

            value = table_details.details.get(key, "").replace("Replicated", "")

            if _compare_engine_setting(value, setting_value):
                error = SQLPipeError.error_engine_match(
                    datasource_name=datasource.name,
                    value=value,
                    setting_value=setting_value,
                    setting_key=setting_key.upper(),
                    is_cli=is_cli,
                    is_from_ui=is_from_ui,
                )

                raise SQLValidationException(error)


# Check engine partition key to avoid, when possible, creating MV with partition keys with too much cardinality
# Avoiding CH TOO_MANY_PARTS error on ingestion
# See https://gitlab.com/tinybird/analytics/-/issues/5309
async def check_engine_partition_key(database_server, database, engine_settings, left_table, user_query):
    partition_key = engine_settings.get("engine_partition_key", None)
    if not partition_key or partition_key == "tuple()":
        return

    # Step 1: get the most recent active part for the source/landing DS
    client = HTTPClient(host=database_server, database=database)
    try:
        query_get_parts_of_interest = f"""
SELECT name
FROM system.parts
WHERE active AND database = '{left_table[0]}' AND table = '{left_table[1]}' AND bytes_on_disk < 512*1024*1024
ORDER BY modification_time DESC
LIMIT 1
FORMAT JSON
"""
        headers, body = await client.query(
            query_get_parts_of_interest, read_only=True, max_execution_time=5, max_threads=1
        )
        data = json.loads(body)
        parts = [row["name"] for row in data["data"]]
        if len(parts) == 0:
            return
    except CHException as e:
        logging.warning(f"CH error with query_get_parts_of_interest: {e}")
        # TODO as this is an initial version, let's avoid erroring if the check fails for an unknown reason
        return

    # Step 2: get unique number of values for the partition key column(s) on recent data
    try:
        replacements = {
            (left_table[0], left_table[1]): (
                "",
                f"""(
        SELECT *
        FROM {left_table[0]}.{left_table[1]}
        WHERE _part IN ({",".join(f"'{part}'" for part in parts)})
        )""",
            )
        }
        query_with_last_data_parts = chquery.replace_tables(user_query, replacements, default_database=database)

        query_cardinality = f"""
SELECT max(cardinality) AS max_cardinality FROM (
    SELECT uniq({partition_key}) AS cardinality FROM (
        {query_with_last_data_parts}
    )
)
FORMAT JSON
"""
        headers, body = await client.query(query_cardinality, read_only=True, max_execution_time=5, max_threads=1)
        data = json.loads(body)
        if len(data["data"]) == 0:
            return
        partition_key_cardinality = data["data"][0]["max_cardinality"]
    except CHException as e:
        logging.warning(f"CH error with query_cardinality: {e}")
        # TODO as this is an initial version, let's avoid erroring if the check fails for an unknown reason
        return

    # Step 3: raise an exception if the number is higher than the threshold
    allowed_partition_key_cardinality = 10
    if partition_key_cardinality > allowed_partition_key_cardinality:
        raise SQLValidationException(SQLPipeError.error_engine_partition_key())
