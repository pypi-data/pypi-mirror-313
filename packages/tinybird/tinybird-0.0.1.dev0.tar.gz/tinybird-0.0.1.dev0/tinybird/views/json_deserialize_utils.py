import re
from typing import Any, Dict, List, NamedTuple, Optional, Set

from tinybird.sql import parse_table_structure

KAFKA_META_COLUMNS = {"__value", "__topic", "__partition", "__offset", "__timestamp", "__key", "__headers"}
DYNAMODB_META_COLUMNS = {"_event_name", "_timestamp", "_record", "_is_deleted"}


class SchemaJsonpathMismatch(Exception):
    pass


class InvalidJSONPath(Exception):
    pass


class SchemaSyntaxError(Exception):
    pass


class ParsedAugmentedSchema(NamedTuple):
    schema: str
    jsonpaths: Optional[str]


# Parse an augmented schema with JSONPath information
# into a CH-compatible schema and a list of jsonpaths
def parse_augmented_schema(augmented_schema: str, remove_columns: Set[str] | None = None) -> ParsedAugmentedSchema:
    columns = parse_table_structure(augmented_schema)
    check_duplicated_names(columns)
    if remove_columns is not None:
        columns = [col for col in columns if col["name"] not in remove_columns]

    def raw_type(c: Dict[str, Any]):
        return f"Nullable({c['type']})" if c["nullable"] else c["type"]

    schema = ", ".join([f"{c['name']} {raw_type(c)} {c['default_value'] or ''} {c['codec'] or ''}" for c in columns])
    jsonpaths = None
    if [c for c in columns if c.get("jsonpath", None)]:
        jsonpaths = ", ".join([c["jsonpath"] or "" for c in columns])
    return ParsedAugmentedSchema(schema=schema, jsonpaths=jsonpaths)


def check_duplicated_names(columns: List[Dict[str, Any]]) -> None:
    seen = set()
    for col in columns:
        if col["name"] in seen:
            raise DuplicatedColumn(col["name"])
        seen.add(col["name"])


class DuplicatedColumn(Exception):
    def __init__(self, column_name):
        super().__init__(f"Duplicated column in schema: '{column_name}'")


def json_deserialize_merge_schema_jsonpaths(
    schema: List[Dict[str, Any]], jsonpaths_as_string: Optional[str]
) -> List[Dict[str, Any]]:
    if not jsonpaths_as_string:
        raise SchemaJsonpathMismatch()
    jsonpaths = [x.strip() for x in jsonpaths_as_string.split(",")]
    if len(schema) != len(jsonpaths):
        raise SchemaJsonpathMismatch()

    def merge_schema_jsonpath(i: int) -> Dict[str, Any]:
        sch = schema[i]
        jsonpath = jsonpaths[i]
        column_type = sch["type"]
        validate_jsonpath(jsonpath, column_type)
        return {
            "name": sch["name"],
            "type": column_type,
            "nullable": sch["nullable"],
            "default_value": sch["default_value"],
            "codec": sch["codec"],
            "jsonpath": jsonpath.strip(),
        }

    cols = list(map(merge_schema_jsonpath, range(0, len(schema))))
    return cols


validate_jsonpath_regex = re.compile("""\$((\.(([\w-]+)|(\['[^']*'\])))|(\[:\]))*""")


def is_jsonpath_valid(p: str) -> bool:
    """
    >>> is_jsonpath_valid('$.prop')
    True
    >>> is_jsonpath_valid("$.['prop']")
    True
    >>> is_jsonpath_valid("$.['$schema']")
    True
    >>> is_jsonpath_valid('$[:]')
    True
    >>> is_jsonpath_valid('$[:][:]')
    True
    >>> is_jsonpath_valid('$[:][:].wadus')
    True
    >>> is_jsonpath_valid('$.wadus.wadus')
    True
    >>> is_jsonpath_valid('$.wadus.wadus[:]')
    True
    >>> is_jsonpath_valid('$')
    True
    >>> is_jsonpath_valid('wadus')
    False
    >>> is_jsonpath_valid('.wadus')
    False
    >>> is_jsonpath_valid('$wadus')
    False
    >>> is_jsonpath_valid('$..wadus')
    False
    >>> is_jsonpath_valid('$.wadus[:]wadus')
    False
    >>> is_jsonpath_valid('$.aria-hidden')
    True
    >>> is_jsonpath_valid('$.aria-hidden[:].aria-hidden')
    True
    >>> is_jsonpath_valid(None)
    False
    >>> is_jsonpath_valid('')
    False
    """
    return bool(p and validate_jsonpath_regex.fullmatch(p))


validate_array_regex = re.compile("""Array\(.+\)""")


def is_json_array(_type: str) -> bool:
    """
    >>> is_json_array('Array(Int32)')
    True
    >>> is_json_array('Array()')
    False
    >>> is_json_array('array(Int32)')
    False
    >>> is_json_array('Int32')
    False
    """
    return bool(_type and validate_array_regex.fullmatch(_type))


def validate_jsonpath(p: str, t: str) -> None:
    if not is_jsonpath_valid(p):
        raise InvalidJSONPath(f"Invalid JSONPath: '{p}'")
    if is_json_array(t) and "[:]" not in p:
        raise InvalidJSONPath(
            f"Invalid JSONPath: '{p}' is not a valid json array path. Array field should use the operator [:]"
        )
