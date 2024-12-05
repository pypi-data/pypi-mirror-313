import asyncio
import datetime
import string
from typing import Any, Dict, List, Optional

import orjson

from tinybird.ch import normalize_column_name
from tinybird.csv_tools import csv_from_python_object_async
from tinybird.sampler import Guess, guess
from tinybird.views.ch_local import ch_local_query

ANALYZE_DEFAULT_TIMEOUT: int = 10

ANALYZE_COLUMNS_LIMIT: int = 10000


async def analyze(
    rows, timeout: int = ANALYZE_DEFAULT_TIMEOUT, format="ndjson", header=None
) -> Optional[Dict[str, Any]]:
    guessed: List[Guess] = []
    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for row in rows:
        await asyncio.sleep(0)
        guess("", "", guessed, row, t, path="$" if format == "ndjson" else "csv")
    if format == "csv":
        # csv doesn't have a "root" object
        guessed = list(filter(lambda x: x[3] != "csv", guessed))
    if not guessed:
        return None

    guess_csv = await csv_from_python_object_async(guessed)

    structure = """
            user_id LowCardinality(String),
            datasource_id LowCardinality(String),
            timestamp DateTime,

            path LowCardinality(String),
            type LowCardinality(String),
            num Float64,
            str String"""
    stdout = await ch_local_query(
        analyze_query("", "", type=format),
        guess_csv.encode("utf-8"),
        "CSV",
        timeout=timeout,
        input_structure=structure,
        input_random_access_table="data_guess",
    )
    columns, schema = process_analyze_query_result(stdout, header=header, include_first_seen=False)
    result = {
        "columns": columns,
        "schema": schema,
    }
    if format == "ndjson":
        schema_parts = [
            f"{x['name']} {x['recommended_type']} `json:{x['path']}`" for x in columns if x["recommended_type"]
        ]
        augmented_schema = ", ".join(schema_parts)
        result["schema"] = augmented_schema
    return result


def process_analyze_query_result(query_result, header=None, include_first_seen=True):
    analysis = orjson.loads(query_result)
    schema_columns = []
    columns = []
    names = set()
    for i, c in enumerate(analysis["data"]):
        if not c["recommended_type"]:
            continue
        if not include_first_seen:
            del c["first_seen_date"]
        array_replace = "_"
        name = (
            c["path"]
            .replace("$.", "")
            .replace(".", "_")
            .replace("-", "_")
            .replace("[:]", array_replace)
            .replace("['", "")
            .replace("']", "")
            .replace("$", "DOLLAR_SIGN_")
        )
        name = name[:-1] if name.endswith("_") else name
        if header and i < len(header):
            name = header[i]
        # Replace SQL "unfriendly" characters
        sql_friendly_characters = string.ascii_letters + string.digits + "_"
        name = name.translate({ord(c): c if c in sql_friendly_characters else "_" for c in name})
        j = 2
        while name in names:
            name = f"{name}_{j}"
            j += 1
        names.add(name)
        c["name"] = normalize_column_name(name)
        schema_columns.append(f"{c['name']} {c['recommended_type']}")
        columns.append(c)
    schema = ", ".join(schema_columns)
    return columns, schema


def analyze_query(user_id, datasource_id, type="ndjson", analyze_column_limit: int = ANALYZE_COLUMNS_LIMIT):
    count_path = "$" if type == "ndjson" else "csv.0"
    # The Left JOIN with the super_path is needed to
    # check if a field within an array should be nullable or not
    # Simply checking total_rows matches total_rows_with_path is not ok, as there are potentially more than one sampled array item per root object
    query = f"""
SELECT
    path,
    first_seen_date,
    present_pct,
    recommended_type
FROM (
SELECT
    a.path AS path,
    first_seen_date,
    total_rows_with_path,
    total_rows,
    total_arrays,
    total_array_items,
    is_array,
    str_stores_datetime_pct,
    total_rows_with_path / if(is_array, total_array_items, toFloat64(total_rows)) AS present_pct,
    total_arrays/total_rows AS present_array_pct,
    has_nulls OR present_pct < 1 OR (is_array AND (present_array_pct < 1)) AS nullable,
    like(a.path, '%[:]%[:]%') as is_nested_array,
    multiIf(mixed_types, 'Multiple JSON types stored at the same JSONPath',
            is_nested_array, 'Nested arrays are not supported',
            NULL) AS error,
    multiIf(error is NOT NULL, NULL,
            json_type = 'string'
                AND str_stores_datetime_pct > 0.8
                AND str_stores_datetime64_pct = 0
                AND str_has_time_pct > 0, 'DateTime',
            json_type = 'string'
                AND str_stores_datetime_pct > 0.8
                AND str_stores_datetime64_pct > 0, 'DateTime64',
            json_type = 'string'
                AND str_stores_datetime_pct > 0.8
                AND str_has_time_pct = 0
                AND str_is_iso_date_pct > 0, 'Date',
            json_type = 'string'
                AND str_stores_datetime_pct > 0.8
                AND str_has_time_pct = 0
                AND str_is_iso_date_pct = 0, 'String',
            json_type = 'string', 'String',
            json_type = 'date' AND str_is_iso_date_pct > 0, 'Date',
            json_type = 'number' AND json_floats > 0 AND num_max_bits < 16, 'Float32',
            json_type = 'number' AND json_floats > 0, 'Float64',
            json_type = 'number'
                AND num_integer_pct = 1
                AND num_max_bits < 10, 'Int16',
            json_type = 'number'
                AND num_integer_pct = 1
                AND num_max_bits < 26, 'Int32',
            json_type = 'number'
                AND num_integer_pct = 1, 'Int64',
            json_type = 'number'
                AND num_few_digits_pct = 1
                AND num_max_bits < 16, 'Float32',
            json_type = 'number', 'Float64',
            json_type = 'bool', 'UInt8',
            NULL) AS recommended_type_base,
    if(nullable, concat('Nullable(', recommended_type_base, ')'), recommended_type_base) AS recommended_type_base_nullable,
    if (is_array, concat('Array(', recommended_type_base_nullable, ')'), recommended_type_base_nullable) AS recommended_type
FROM
(SELECT path,
        like(path, '%[:]%') as is_array,
        if(is_array, substr(path, 1, position(path, '[:]') - 1), '{count_path}') AS super_path,
        any(type) AS json_type,
        uniq(type) > 1 AS mixed_types,
        MIN(timestamp) AS first_seen_date,
        MIN(num) AS num_min,
        MAX(num) AS num_max,
        countIf(str = 'f') AS json_floats,
        ceil(log2(greatest(num_max, abs(num_min)))) AS num_max_bits,
        countIf(round(num) = num)/count() AS num_integer_pct,
        countIf(round(num, 3) = num)/count() AS num_few_digits_pct,
        countIf(str != '' AND (toFloat64OrNull(str) IS NULL) AND NOT(
            str ilike 'jan%' OR
            str ilike 'feb%' OR
            str ilike 'mar%' OR
            str ilike 'apr%' OR
            str ilike 'may%' OR
            str ilike 'jun%' OR
            str ilike 'jul%' OR
            str ilike 'aug%' OR
            str ilike 'sep%' OR
            str ilike 'oct%' OR
            str ilike 'nov%' OR
            str ilike 'dec%'
         ) AND (parseDateTimeBestEffortOrNull(str) IS NOT NULL )
          AND match(str, '^([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$') != 1 -- this avoids HH:MM:SS is parsed as a DateTime
        ) / count() AS str_stores_datetime_pct,
        countIf(match(str, '([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](|.0+Z?)$') == 1) / count() AS str_has_time_pct,
        countIf(match(str, '^[0-9][0-9][0-9][0-9]-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$') == 1) / count() AS str_is_iso_date_pct,
        countIf(str != '' AND (toUnixTimestamp64Micro(parseDateTime64BestEffortOrZero(str)) % (1000*1000)) != 0)/count() AS str_stores_datetime64_pct
    FROM data_guess
    WHERE user_id = '{user_id}' AND datasource_id = '{datasource_id}' AND type != 'null' AND type != 'object'
    GROUP BY path
    ORDER BY first_seen_date DESC
    LIMIT {analyze_column_limit}) AS a
INNER JOIN
(
    SELECT
        path,
        count() AS total_rows_with_path,
        countIf(type = 'null') > 0 AS has_nulls
    FROM data_guess
    WHERE user_id = '{user_id}' AND datasource_id = '{datasource_id}'
    GROUP BY path
) AS b
ON (a.path = b.path)
LEFT JOIN
(SELECT
    path,
    count() AS total_arrays,
    sum(num) AS total_array_items
    FROM data_guess
    WHERE user_id = '{user_id}' AND datasource_id = '{datasource_id}' AND type = 'array'
    GROUP BY path
) AS c
ON (a.super_path = c.path)
CROSS JOIN
(
SELECT count() AS total_rows
FROM data_guess
    WHERE user_id = '{user_id}' AND datasource_id = '{datasource_id}' AND path = '{count_path}'
) AS d

ORDER BY present_pct DESC, path
)
FORMAT JSON;
"""
    return query
