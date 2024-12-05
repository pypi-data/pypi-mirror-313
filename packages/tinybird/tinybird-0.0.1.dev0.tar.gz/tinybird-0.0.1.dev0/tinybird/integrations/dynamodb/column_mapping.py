import re
from typing import Any, Dict, List, Tuple

from tinybird.ch_utils.describe_table import TableColumn
from tinybird.job import ColumnMapping
from tinybird.ndjson import get_path


def build_column_mapping(
    json_deserialization: List[Dict[str, Any]], target_schema: List[Dict[str, Any]]
) -> Dict[str, ColumnMapping]:
    mapping = {}
    target_types = {column["normalized_name"]: get_column_type_name(column) for column in target_schema}
    for column in json_deserialization:
        # Replace $.Item to $. in the JSONPath because we don't need it here
        column_jsonpath = re.sub(r"\$\.Item\.([\w_-]+)", r"$.\1", column["jsonpath"])

        column_name: str = column["name"]
        column_original_type: str = column["type"]
        column_target_type: str = target_types[column_name]
        default_value = column["default_value"]

        column_source: str = get_source_for_column(
            "Item", column_jsonpath, column_target_type, column_original_type, default_value
        )

        table_column = TableColumn(column_jsonpath, type=column_target_type, is_subcolumn=True)
        mapping[column_name] = ColumnMapping(target=column_name, source=column_source, source_table_column=table_column)

    return mapping


def get_source_for_column(
    source_property: str,
    jsonpath: str,
    dest_column_type: str,
    dest_column_type_without_modifiers: str,
    default_value: str | None = None,
) -> str:
    """
    >>> get_source_for_column('Item','$.product_id','String','String')
    "JSONExtract(`Item`, 'product_id', 'String')"
    >>> get_source_for_column('Item','$.product_id','String','String','default')
    "JSONExtract(`Item`, 'product_id', 'Nullable(String)')"
    >>> get_source_for_column('Item','$.products[:]','Array(String)','Array(String)')
    "JSONExtract(`Item`, 'products', 'Array(String)')"
    >>> get_source_for_column('Item','$.products[:].id','Array(String)','Array(String)')
    "arrayMap(x -> JSONExtract(x, 'id', 'String'), JSONExtractArrayRaw(`Item`, 'products'))"
    >>> get_source_for_column('Item','$.products[:].id','Array(LowCardinality(String))','Array(LowCardinality(String))')
    "arrayMap(x -> JSONExtract(x, 'id', 'LowCardinality(String)'), JSONExtractArrayRaw(`Item`, 'products'))"
    >>> get_source_for_column('Item','$.products[:].id','Array(Nullable(LowCardinality(String)))','Array(LowCardinality(String))')
    "arrayMap(x -> JSONExtract(x, 'id', 'LowCardinality(String)'), JSONExtractArrayRaw(`Item`, 'products'))"
    >>> get_source_for_column('Item', '$.some_date', 'Date', 'Date')
    "JSONExtract(`Item`, 'some_date', 'String')"
    >>> get_source_for_column('Item', '$.some_date[:]', 'Array(Date)', 'Array(Date)')
    "JSONExtract(`Item`, 'some_date', 'Array(String)')"
    >>> get_source_for_column('Item', '$.some_datetime', 'DateTime', 'DateTime')
    "parseDateTime64BestEffortOrNull(JSONExtract(`Item`, 'some_datetime', 'String'), 0)"
    >>> get_source_for_column('Item', '$.some_datetime', 'DateTime64', 'DateTime64')
    "parseDateTime64BestEffortOrNull(JSONExtract(`Item`, 'some_datetime', 'String'), 3)"
    >>> get_source_for_column('Item', '$.some_datetime', 'DateTime64(6)', 'DateTime64(6)', 'Now64()')
    "parseDateTime64BestEffortOrNull(JSONExtract(`Item`, 'some_datetime', 'Nullable(String)'), 6)"
    >>> get_source_for_column('Item', '$.some_dates[:]','Array(DateTime)','Array(DateTime)')
    "arrayMap(x -> parseDateTime64BestEffortOrNull(x, 0), JSONExtract(`Item`, 'some_dates', 'Array(String)'))"
    >>> get_source_for_column('Item', '$.some_dates[:]','Array(DateTime64)','Array(DateTime64)')
    "arrayMap(x -> parseDateTime64BestEffortOrNull(x, 3), JSONExtract(`Item`, 'some_dates', 'Array(String)'))"
    >>> get_source_for_column('Item', '$.some_dates[:]','Array(DateTime64(6))','Array(DateTime64(6))')
    "arrayMap(x -> parseDateTime64BestEffortOrNull(x, 6), JSONExtract(`Item`, 'some_dates', 'Array(String)'))"
    >>> get_source_for_column('Item', '$.some_date[:]', 'Array(Nullable(DateTime64(3)))', 'Array(Nullable(DateTime64(3)))')
    "arrayMap(x -> parseDateTime64BestEffortOrNull(x, 3), JSONExtract(`Item`, 'some_date', 'Array(Nullable(String))'))"
    >>> get_source_for_column('Item','$.products[:].date','Array(Date)','Array(Date)')
    "arrayMap(x -> JSONExtract(x, 'date', 'String'), JSONExtractArrayRaw(`Item`, 'products'))"
    >>> get_source_for_column('Item','$.products[:].datetime','Array(DateTime64(3))','Array(DateTime64(3))')
    "arrayMap(x -> parseDateTime64BestEffortOrNull(JSONExtract(x, 'datetime', 'String'), 3), JSONExtractArrayRaw(`Item`, 'products'))"
    """
    column_path = get_path(jsonpath)

    last_element = column_path[-1]

    if isinstance(last_element, list) and len(last_element) > 0:
        type_without_prefix = (
            dest_column_type_without_modifiers.removeprefix("Array(").removesuffix(")")
            if dest_column_type_without_modifiers.startswith("Array(")
            else dest_column_type_without_modifiers
        )

        # Case: ['products', ['code.id']] or ['products', 'subproperty', ['code', 'id']]
        json_properties = column_path[:-1]
        array_params = ",".join(f"'{item}'" for item in last_element)
        property_params = ",".join(f"'{item}'" for item in json_properties)

        date_type, precision, replacement = handle_date_types(type_without_prefix)
        if date_type in [None, "Date"]:
            return f"arrayMap(x -> JSONExtract(x, {array_params}, '{replacement}'), JSONExtractArrayRaw(`{source_property}`, {property_params}))"
        else:
            return f"arrayMap(x -> parseDateTime64BestEffortOrNull(JSONExtract(x, {array_params}, '{replacement}'), {precision}), JSONExtractArrayRaw(`{source_property}`, {property_params}))"

    elif isinstance(last_element, list):
        json_properties = column_path[:-1]
        property_params = ",".join(f"'{item}'" for item in json_properties)

        date_type, precision, replacement = handle_date_types(dest_column_type)
        if date_type in [None, "Date"]:
            return f"JSONExtract(`{source_property}`, {property_params}, '{replacement}')"
        else:
            return f"arrayMap(x -> parseDateTime64BestEffortOrNull(x, {precision}), JSONExtract(`{source_property}`, {property_params}, '{replacement}'))"

    else:
        if not dest_column_type.startswith("Nullable(") and default_value is not None:
            dest_column_type = f"Nullable({dest_column_type})"
        property_params = ",".join(f"'{item}'" for item in column_path)

        date_type, precision, replacement = handle_date_types(dest_column_type)
        if date_type in [None, "Date"]:
            return f"JSONExtract(`{source_property}`, {property_params}, '{replacement}')"
        else:
            return f"parseDateTime64BestEffortOrNull(JSONExtract(`{source_property}`, {property_params}, '{replacement}'), {precision})"


def handle_date_types(column_type: str) -> Tuple[str | None, str, str]:
    re_date = re.fullmatch(r"(?:.*\()?(Date(?:Time(?:64)?)?(?:\((\d*)\))?)(?:\)*)?", column_type)
    if re_date is None:
        return None, "0", column_type
    date_type, precision = re_date.groups()
    precision = "3" if date_type == "DateTime64" else precision
    precision = "0" if precision is None else precision
    replacement_type = column_type.replace(date_type, "String")
    return date_type, precision, replacement_type


def get_column_type_name(column: Dict[str, Any]) -> str:
    type_name: str = column.get("type", "")
    is_nullable = column.get("nullable")
    is_array_or_map_or_tuple = (
        type_name.startswith("Array(") or type_name.startswith("Map(") or type_name.startswith("Tuple(")
    )

    if is_nullable and not is_array_or_map_or_tuple:
        return f"Nullable({type_name})"

    return type_name
