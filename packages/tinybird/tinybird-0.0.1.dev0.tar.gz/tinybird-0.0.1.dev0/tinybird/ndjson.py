import datetime
import decimal
import logging
import numbers
import re
import struct
import time
import traceback
from dataclasses import dataclass
from decimal import Decimal, DecimalException
from io import SEEK_SET, BytesIO
from typing import Any, Callable, List, Optional, Union
from uuid import UUID

import ciso8601
import msgspec
import orjson
from pytz import utc

from tinybird import fast_leb128
from tinybird.datatypes import get_decimal_limits, parse_decimal_type
from tinybird.hfi.hfi_settings import hfi_settings

fast_leb128_encode = fast_leb128.encode
datetime_struct_packer = struct.Struct("<I").pack
datetime64_struct_packer = struct.Struct("<q").pack
date_struct_packer = struct.Struct("<H").pack
date32_struct_packer = struct.Struct("<i").pack
parse_datetime = ciso8601.parse_datetime
partition_offset_timestamp_struct_packer = struct.Struct("<hqI").pack


class DateTimeParseError(Exception):
    pass


class NullNotAllowedException(Exception):
    pass


FAMILY_STRING = 1
FAMILY_NUMERIC = 2
FAMILY_ARRAY = 3
FAMILY_DATETIME = 4
FAMILY_DATETIME64 = 5
FAMILY_DATE = 6
FAMILY_UUID = 7
FAMILY_DATE32 = 8
FAMILY_MAP = 9
FAMILY_BOOL = 10
FAMILY_DECIMAL = 11
FAMILY_FIXED_STRING = 12
FAMILY_BIG_NUMERIC = 13
FAMILY_JSON = 14

# datetime64 and date32 ranges have been updated to 1900 to 2299 in version 22.8 (2022-08-18), but previous versions only support ranges from 1925 to 2283
# https://clickhouse.com/docs/en/whats-new/changelog/#-clickhouse-release-228-2022-08-18
# https://github.com/ClickHouse/ClickHouse/pull/39425


@dataclass
class TypeValidRange:
    min_value: Any
    max_value: Any
    min_str: str
    max_str: str
    _type: Optional[Any] = None


def is_datetime_out_of_range(timestamp_posix, datetime_range):
    return datetime_range and (timestamp_posix < datetime_range.min_value or timestamp_posix > datetime_range.max_value)


def is_number_out_of_range(value, integer_range):
    return (
        integer_range
        and isinstance(value, numbers.Number)
        and (value < integer_range.min_value or value > integer_range.max_value)
    )


def is_decimal_out_of_range(value: Decimal, valid_range):
    return valid_range and (value < valid_range.min_value or value > valid_range.max_value)


def get_out_of_bounds_error(column: Optional[str], jsonpath: str, _type: str, value: Any, min: str, max: str):
    return f"Value {value} out of bounds for type '{_type}' in column '{column}' with jsonpath '{jsonpath}'. Value must be between {min} and {max}"


def get_string_too_long_error(column: str, jsonpath: str, _type: str, value: Any):
    return f"Value '{value}' is too long for type '{_type}' in column '{column}' with jsonpath '{jsonpath}'."


datetime_limit = TypeValidRange(
    datetime.datetime(1970, 1, 1, tzinfo=utc).timestamp(),
    datetime.datetime(2106, 2, 7, 6, 28, 15, tzinfo=utc).timestamp(),
    "1970-01-01 00:00:00",
    "2106-02-07 06:28:15",
)
datetime64_limit = TypeValidRange(
    datetime.datetime(1925, 1, 1, tzinfo=utc).timestamp(),
    datetime.datetime(2283, 11, 11, 23, 59, 59, 999999, tzinfo=utc).timestamp(),
    "1925-01-01 00:00:00",
    "2283-11-11 23:59:59",
)
date_limit = TypeValidRange(
    datetime.datetime(1970, 1, 1, tzinfo=utc).timestamp(),
    datetime.datetime(2149, 6, 6, 23, 59, 59, 999999, tzinfo=utc).timestamp(),
    "1970-01-01",
    "2149-06-06",
)
date32_limit = TypeValidRange(
    datetime.datetime(1925, 1, 1, tzinfo=utc).timestamp(),
    datetime.datetime(2283, 11, 11, 23, 59, 59, 99999, tzinfo=utc).timestamp(),
    "1925-01-01",
    "2283-11-11",
)


number_limits = {
    "Int8": TypeValidRange(-128, 127, "-128", "127", numbers.Number),
    "Int16": TypeValidRange(-32768, 32767, "-32768", "32767", numbers.Number),
    "Int32": TypeValidRange(-2147483648, 2147483647, "-2147483648", "2147483647", numbers.Number),
    # orjson min value is -9223372036854775807, so the limit is set to it instead -9223372036854775808
    # https://github.com/ijl/orjson#int
    "Int64": TypeValidRange(
        -9223372036854775807, 9223372036854775807, "-9223372036854775808", "9223372036854775807", numbers.Number
    ),
    "Int128": TypeValidRange(
        -170141183460469231731687303715884105728,
        170141183460469231731687303715884105727,
        "-170141183460469231731687303715884105728",
        "170141183460469231731687303715884105727",
        numbers.Number,
    ),
    "Int256": TypeValidRange(
        -57896044618658097711785492504343953926634992332820282019728792003956564819968,
        57896044618658097711785492504343953926634992332820282019728792003956564819967,
        "-57896044618658097711785492504343953926634992332820282019728792003956564819968",
        "57896044618658097711785492504343953926634992332820282019728792003956564819967",
        numbers.Number,
    ),
    "UInt8": TypeValidRange(0, 255, "0", "255", numbers.Number),
    "UInt16": TypeValidRange(0, 65535, "0", "65535", numbers.Number),
    "UInt32": TypeValidRange(0, 4294967295, "0", "4294967295", numbers.Number),
    "UInt64": TypeValidRange(0, 18446744073709551615, "0", "18446744073709551615", numbers.Number),
    "UInt128": TypeValidRange(
        0, 340282366920938463463374607431768211455, "0", "340282366920938463463374607431768211455", numbers.Number
    ),
    "UInt256": TypeValidRange(
        0,
        115792089237316195423570985008687907853269984665640564039457584007913129639935,
        "0",
        "115792089237316195423570985008687907853269984665640564039457584007913129639935",
        numbers.Number,
    ),
}

# These types are deserialized using msgspec instead of orjson
# because orjson limitations with numbers above 64 bits
# that's why they are handled differently
big_numeric_types = {"Int128", "UInt128", "Int256", "UInt256"}


@dataclass
class JSONType:
    family: int
    nullable: bool
    struct_format: Optional[Callable[[Union[float, int]], bytes]]
    subtype: Any
    type_str: str
    limits: Optional[TypeValidRange] = None
    has_default_value: Optional[bool] = False

    def is_nullable(self):
        return self.nullable or (
            self.subtype is not None and hasattr(self.subtype, "nullable") and self.subtype.nullable
        )


@dataclass
class JSONColumn:
    path: Any
    typ: JSONType
    simplepath: Any
    name: str


@dataclass
class ExtendedJSONDeserialization:
    # Simple columns are not included in "complex" to enable performance optimizations
    strings: list  # Non nullable String fields at single level JSONPaths
    numerics: list  # Non nullable Number fields at single level JSONPaths
    datetimes: list  # Non nullable Datetime fields at single level JSONPaths
    datetimes64: list  # Non nullable Datetime64 fields at single level JSONPaths
    complex: list  # Other fields
    simplepath_to_column_name: dict
    query_columns: list
    query_columns_types: list
    original_order_columns: list


# Struct format conversion to serialize numbers into CH's RowBinary format
# https://docs.python.org/3/library/struct.html#format-characters
struct_format_table = {
    "Int8": "<b",
    "UInt8": "<B",
    "Int16": "<h",
    "UInt16": "<H",
    "Int32": "<i",
    "UInt32": "<I",
    "Int64": "<q",
    "UInt64": "<Q",
    "Float32": "<f",
    "Float64": "<d",
}
for key in struct_format_table.copy():
    struct_format_table[f"Nullable({key})"] = struct_format_table[key]


class UnsupportedType(Exception):
    pass


def get_inner_type(data_type: str) -> str:
    if inner_nullable_type := re.match(r"^Nullable\((.*)\)$", data_type):
        return inner_nullable_type.group(1)

    return data_type


def get_jsontype(typ: str, nullable: bool, has_default_value: Optional[bool] = False):
    if re.match(r"^Array\((.*)\)$", typ):
        inner_type = get_inner_type(typ[6:-1])
        subtype = get_jsontype(inner_type, nullable, has_default_value)
        return JSONType(FAMILY_ARRAY, False, None, subtype, typ, has_default_value=has_default_value)
    if re.match(r"^Map\((.*)\)$", typ):
        key_type_name, _, value_type_name = typ[4:-1].partition(",")
        key_type = get_jsontype(key_type_name.strip(), False, has_default_value)
        value_type = get_jsontype(
            get_inner_type(value_type_name.strip()), "Nullable" in value_type_name, has_default_value
        )
        if key_type.family == FAMILY_BIG_NUMERIC or value_type.family == FAMILY_BIG_NUMERIC:
            raise UnsupportedType(f"Unsupported type in Map: {typ}")
        return JSONType(FAMILY_MAP, nullable, None, (key_type, value_type), typ, has_default_value=has_default_value)
    if "FixedString" in typ:
        n = None
        if m := re.match(r"^FixedString\(\s*(\d+)\s*\)$", typ):
            n = int(m.group(1))
        if n is None or n == 0:
            raise UnsupportedType(f"Unsupported flavour of FixedString type: {typ}")
        return JSONType(FAMILY_FIXED_STRING, nullable, None, n, typ, has_default_value=has_default_value)
    if "String" in typ:
        return JSONType(FAMILY_STRING, nullable, None, None, typ, has_default_value=has_default_value)
    if typ in struct_format_table:
        limit = number_limits.get(typ, None)
        return JSONType(
            FAMILY_NUMERIC, nullable, struct.Struct(struct_format_table[typ]).pack, None, typ, limit, has_default_value
        )
    if typ in big_numeric_types:
        signed = "I" == typ[0]
        length = int(typ[-3:]) // 8
        limit = number_limits.get(typ, None)
        return JSONType(
            FAMILY_BIG_NUMERIC, nullable, None, (signed, length), typ, limit, has_default_value=has_default_value
        )
    if "DateTime64" in typ:
        try:
            resolution = int(typ[len("DateTime64(") : len("DateTime64(") + 1])
        except Exception:
            resolution = 3
        multiplier = 10**resolution
        return JSONType(FAMILY_DATETIME64, nullable, None, multiplier, typ, datetime64_limit, has_default_value)
    if typ == "Date":
        return JSONType(FAMILY_DATE, nullable, None, None, typ, date_limit, has_default_value)
    if typ == "Date32":
        return JSONType(FAMILY_DATE32, nullable, None, None, typ, date32_limit, has_default_value)
    if "DateTime" in typ:
        return JSONType(FAMILY_DATETIME, nullable, None, None, typ, datetime_limit, has_default_value)
    if "UUID" in typ:
        return JSONType(FAMILY_UUID, nullable, None, None, typ, has_default_value=has_default_value)
    if typ in ["Bool", "Boolean"]:
        return JSONType(FAMILY_BOOL, nullable, None, None, typ, has_default_value=has_default_value)
    if "Decimal" in typ:
        parsed_decimal = parse_decimal_type(typ)
        if not parsed_decimal:
            raise UnsupportedType(f"Unsupported flavour of Decimal type: {typ}")
        b, p, s = parsed_decimal
        subtype = (b // 8, p, s)
        min_value, max_value = get_decimal_limits(p, s)
        limits = TypeValidRange(min_value, max_value, str(min_value), str(max_value))
        return JSONType(FAMILY_DECIMAL, nullable, None, subtype, typ, limits, has_default_value)
    if "JSON" in typ and hfi_settings.get("allow_json_type", False):
        return JSONType(FAMILY_JSON, nullable, None, None, typ, has_default_value=has_default_value)
    raise UnsupportedType(f"Unsupported type: {typ}")


# get_path() transforms a JSONPath into an intermediate path format like:
# '$.field.subfield' => ['field', 'subfield']
# '$.product[:].details.country' => ['product', ['details', 'country']]
def get_path(jsonpath: str):
    """
    >>> get_path('$')
    []
    >>> get_path('$[:]')
    [[]]
    >>> get_path('$.product')
    ['product']
    >>> get_path('$.product.country')
    ['product', 'country']
    >>> get_path('$.product.country.code')
    ['product', 'country', 'code']
    >>> get_path('$.products[:]')
    ['products', []]
    >>> get_path('$.products[:].code')
    ['products', ['code']]
    >>> get_path('$.products[:].code.id')
    ['products', ['code', 'id']]
    >>> get_path("$.['product.code']")
    ['product.code']
    >>> get_path("$.['product.code'].id")
    ['product.code', 'id']
    >>> get_path("$.['product.codes'][:].id")
    ['product.codes', ['id']]
    >>> get_path("$.product.['code.id']")
    ['product', 'code.id']
    >>> get_path("$.products[:].['code.id']")
    ['products', ['code.id']]
    >>> get_path("$.['product-codes'][:].id")
    ['product-codes', ['id']]
    >>> get_path('$.["product-codes"][:].id')
    Traceback (most recent call last):
    ...
    Exception: Invalid JSONPath ["product-codes"][:].id. The path inside brackets should be single quoted.
    >>> get_path('$.[product-codes][:].id')
    Traceback (most recent call last):
    ...
    Exception: Invalid JSONPath [product-codes][:].id. The path inside brackets should be single quoted.
    >>> get_path('$.products[:].countries[:]')
    Traceback (most recent call last):
    ...
    Exception: Nested arrays are not supported. Found 3 levels of nesting.
    >>> get_path('wrong')
    Traceback (most recent call last):
    ...
    Exception: Invalid JSONPath wrong
    """
    if jsonpath.startswith("$."):
        jsonpath = jsonpath[2:]
    elif jsonpath.startswith("$[:]"):
        jsonpath = jsonpath[1:]
    elif jsonpath == "$":
        return []
    else:
        raise Exception(f"Invalid JSONPath {jsonpath}")
    array_parts = jsonpath.split("[:]")

    def get_subpaths(simple_jsonpath: str):
        # split by dots not inside brackets (test.['whatever.bla']) => test, ['whatever.bla']
        elems = re.split("\.(?![^[]*])", simple_jsonpath)
        parts = []
        for elem in elems:
            if not elem:
                continue
            if "['" in elem:
                parts.append(elem[2:-2])
            elif "[" in elem:
                raise Exception(f"Invalid JSONPath {jsonpath}. The path inside brackets should be single quoted.")
            else:
                parts.append(elem)
        return parts

    if len(array_parts) == 1:
        return get_subpaths(array_parts[0])
    if len(array_parts) == 2:
        return get_subpaths(array_parts[0]) + [get_subpaths(array_parts[1])]  # noqa: RUF005
    raise Exception(f"Nested arrays are not supported. Found {len(array_parts)} levels of nesting.")


# value_at(x, path) extract the value at the specified path of the "x" JSON object
# where path is in get_path() format
def value_at(x, path):
    for subpath in path:
        if type(subpath) == str:  # noqa: E721
            x = x[subpath]
        else:
            x = [value_at(child, subpath) for child in x]
    return x


# extend_json_deserialization() transforms a Redis-stored json_deserialization
# into an intermediate format
def extend_json_deserialization(json_deserialization):
    extended_json_deserialization = ExtendedJSONDeserialization([], [], [], [], [], dict(), [], [], [])
    query_columns = []

    def heuristic(t):
        s = 0
        if "Array" in t:
            s += 1000
        if "Nullable" in t:
            s += 100
        if "16" in t:
            s += 10
        if "32" in t:
            s += 20
        if "64" in t:
            s += 30
        if "U" in t:
            s += 1
        return s

    extended_json_deserialization.original_order_columns = [column["name"] for column in json_deserialization]

    rawtype_for_name = {}
    # Sorting the columns significantly improves performance
    # Probably due to CPU's branch predictor, as it this makes it process
    # first one type of column, then another one, instead of
    # changing the deserialization path every time in "random" order
    for column in sorted(json_deserialization, key=heuristic):
        path = get_path(column["jsonpath"])
        default_value = column.get("default_value", None) is not None
        typ = get_jsontype(column["type"], column["nullable"] or ("Nullable" in column["type"]), default_value)
        simplepath = path[0] if (len(path) == 1 and type(path[0]) == str) else None  # noqa: E721

        def raw_type(c):
            _type = c["type"]
            if c["nullable"]:
                _type = f"Nullable({_type})"
            if default_value := c.get("default_value", None):
                _type = f"{_type} {default_value}"
            return _type

        rawtype_for_name[column["name"]] = raw_type(column)
        c = JSONColumn(path, typ, simplepath, column["name"])
        if (
            not simplepath
            or typ.nullable
            or (
                typ.family
                in (
                    FAMILY_DATE,
                    FAMILY_DATE32,
                    FAMILY_UUID,
                    FAMILY_ARRAY,
                    FAMILY_MAP,
                    FAMILY_BOOL,
                    FAMILY_DECIMAL,
                    FAMILY_FIXED_STRING,
                    FAMILY_BIG_NUMERIC,
                )
            )
        ):
            extended_json_deserialization.complex.append((c, column))
        elif typ.family == FAMILY_STRING or typ.family == FAMILY_JSON:
            extended_json_deserialization.strings.append(c)
        elif typ.family == FAMILY_NUMERIC:
            extended_json_deserialization.numerics.append(c)
        elif typ.family == FAMILY_DATETIME:
            extended_json_deserialization.datetimes.append(c)
        elif typ.family == FAMILY_DATETIME64:
            extended_json_deserialization.datetimes64.append((c, typ.subtype))
        else:
            raise Exception(f"Unexpected condition {typ}")
    for c in extended_json_deserialization.strings:
        query_columns.append(c.name)
        extended_json_deserialization.simplepath_to_column_name[c.simplepath] = c.name
    for c in extended_json_deserialization.numerics:
        query_columns.append(c.name)
        extended_json_deserialization.simplepath_to_column_name[c.simplepath] = c.name
    for c in extended_json_deserialization.datetimes:
        query_columns.append(c.name)
        extended_json_deserialization.simplepath_to_column_name[c.simplepath] = c.name
    for c, _ in extended_json_deserialization.datetimes64:
        query_columns.append(c.name)
        extended_json_deserialization.simplepath_to_column_name[c.simplepath] = c.name
    for c, _ in extended_json_deserialization.complex:
        query_columns.append(c.name)
    extended_json_deserialization.strings = [(c.simplepath, c.typ) for c in extended_json_deserialization.strings]
    extended_json_deserialization.numerics = [(c.simplepath, c.typ) for c in extended_json_deserialization.numerics]
    extended_json_deserialization.datetimes = [(c.simplepath, c.typ) for c in extended_json_deserialization.datetimes]
    extended_json_deserialization.datetimes64 = [
        (c.simplepath, multiplier, c.typ) for c, multiplier in extended_json_deserialization.datetimes64
    ]
    extended_json_deserialization.query_columns = query_columns
    extended_json_deserialization.query_columns_types = [rawtype_for_name[name] for name in query_columns]
    return extended_json_deserialization


def rowbinary_serialize(
    typ: JSONType, value, buffer_write, leb128_buffer, parse_or_null_ints_in_array=False, has_value=True
):
    if not has_value:
        return

    if typ.nullable and typ.family == FAMILY_STRING:
        buffer_write(b"\x01" if value is None else b"\x00")
        if value is None:
            return

    family = typ.family
    if typ.family in {FAMILY_STRING, FAMILY_JSON}:
        # Quick fix to avoid quarantine in some edge cases
        # (datetime guessed as string by error in analyze function)
        if isinstance(value, datetime.datetime):
            value = str(value)
        # Quick fix to avoid quarantine in JSON objects
        # being mapped to String
        if isinstance(value, dict):
            value = orjson.dumps(value)
        value = value.encode("utf-8") if not isinstance(value, bytes) else value
        value_len = fast_leb128_encode(leb128_buffer, len(value))
        buffer_write(value_len)
        buffer_write(value)
    elif family == FAMILY_NUMERIC:
        try:
            vv = typ.struct_format(value)  # type: ignore
        except struct.error as e:
            # if nullable, non numbers in array are inserted as Null
            if typ.nullable and (parse_or_null_ints_in_array or value is None):
                buffer_write(b"\x01")
                return
            if is_number_out_of_range(value, typ.limits):
                raise IntegerOutOfRange(
                    "Error parsing integer",
                    typ.type_str,
                    typ.limits.min_str,  # type: ignore
                    typ.limits.max_str,  # type: ignore
                    value,
                )
            raise e
        if typ.nullable:
            buffer_write(b"\x00")
        buffer_write(vv)
    elif family == FAMILY_ARRAY:
        len_value = len(value) if value else 0
        array_len = fast_leb128_encode(leb128_buffer, len_value)
        buffer_write(array_len)
        if value:
            for x in value:
                try:
                    rowbinary_serialize(typ.subtype, x, buffer_write, leb128_buffer, parse_or_null_ints_in_array=True)
                except DateTimeParseError as e:
                    if typ.subtype.nullable:
                        buffer_write(b"\x01")
                        continue
                    raise e
    elif family in [FAMILY_DATETIME, FAMILY_DATETIME64, FAMILY_DATE, FAMILY_DATE32]:
        try:
            if typ.nullable and value is None:
                buffer_write(b"\x01")
                return

            if isinstance(value, datetime.datetime):
                timestamp = value
            elif isinstance(value, datetime.date):
                timestamp = datetime.datetime.fromtimestamp(time.mktime(value.timetuple()))
            else:
                timestamp = parse_datetime(value)
        except TypeError:
            try:
                timestamp = datetime.datetime.fromtimestamp(value)
            except (OverflowError, OSError) as e:
                raise DateTimeParseError(str(e))
            except ValueError:
                try:
                    timestamp = datetime.datetime.fromtimestamp(value / 1000)
                except ValueError as e:
                    raise DateTimeParseError(str(e))
            except TypeError as e:
                raise DateTimeParseError(str(e))
        except ValueError as e:
            raise DateTimeParseError(str(e))

        try:
            if is_datetime_out_of_range(timestamp.timestamp(), typ.limits):
                raise DateTimeOutOfRange(message="", min=typ.limits.min_str, max=typ.limits.max_str)  # type: ignore
        except ValueError:
            raise DateTimeOutOfRange(message="", min=typ.limits.min_str, max=typ.limits.max_str)  # type: ignore

        if typ.nullable:
            buffer_write(b"\x00")
        timestamp_posix = timestamp.timestamp()
        if family == FAMILY_DATETIME:
            buffer_write(datetime_struct_packer(int(timestamp_posix)))
        elif family == FAMILY_DATETIME64:
            # For datetime64, the subtype stores the resolution multiplier
            resolution = typ.subtype
            buffer_write(datetime64_struct_packer(int(timestamp_posix * resolution)))
        elif family == FAMILY_DATE:
            SECONDS_IN_DAY = 86400
            buffer_write(date_struct_packer(int(timestamp_posix) // SECONDS_IN_DAY))
        elif family == FAMILY_DATE32:
            SECONDS_IN_DAY = 86400
            buffer_write(date32_struct_packer(int(timestamp_posix) // SECONDS_IN_DAY))
    elif family == FAMILY_UUID:
        value = value.decode("utf-8") if isinstance(value, bytes) else value
        if value is None and typ.nullable:
            buffer_write(b"\x01")
            return
        try:
            uuid = UUID(value)
        except ValueError:
            raise TypeError()
        if typ.nullable:
            buffer_write(b"\x00")
        buffer_write(uuid.bytes_le[6:8])
        buffer_write(uuid.bytes_le[4:6])
        buffer_write(uuid.bytes_le[0:4])
        buffer_write(uuid.bytes_le[15:16])
        buffer_write(uuid.bytes_le[14:15])
        buffer_write(uuid.bytes_le[13:14])
        buffer_write(uuid.bytes_le[12:13])
        buffer_write(uuid.bytes_le[11:12])
        buffer_write(uuid.bytes_le[10:11])
        buffer_write(uuid.bytes_le[9:10])
        buffer_write(uuid.bytes_le[8:9])
    elif family == FAMILY_MAP:
        len_value = len(value) if value else 0
        array_len = fast_leb128_encode(leb128_buffer, len_value)
        buffer_write(array_len)
        if value:
            for x in value.items():
                rowbinary_serialize(typ.subtype[0], x[0], buffer_write, leb128_buffer, parse_or_null_ints_in_array=True)
                rowbinary_serialize(typ.subtype[1], x[1], buffer_write, leb128_buffer, parse_or_null_ints_in_array=True)
    elif family == FAMILY_BOOL:
        if value is None and typ.nullable:
            buffer_write(b"\x01")
            return
        if value in [0, False]:
            boolean_value = False
        elif value in [1, True]:
            boolean_value = True
        else:
            raise TypeError()
        if typ.nullable:
            buffer_write(b"\x00")
        buffer_write(b"\x01" if boolean_value else b"\x00")
    elif family == FAMILY_DECIMAL:
        if value is None and typ.nullable:
            buffer_write(b"\x01")
            return
        bytes_length, precision, scale = typ.subtype
        with decimal.localcontext(prec=precision + 2):  # we use more precision than required, for better rounding
            try:
                decimal_value = Decimal(value)
                try:
                    decimal_value = round(decimal_value, scale)
                except decimal.InvalidOperation:
                    # Rounding fails if the integral part is too big for the precision
                    raise (
                        DecimalOutOfRange(message="", min=typ.limits.min_str, max=typ.limits.max_str, value=value)
                        if typ.limits
                        else TypeError()
                    )
                if typ.limits and is_decimal_out_of_range(decimal_value, typ.limits):
                    raise DecimalOutOfRange(message="", min=typ.limits.min_str, max=typ.limits.max_str, value=value)
                int_value = int(decimal_value * (10**scale))
            except (ValueError, DecimalException):
                raise TypeError()
        bytes_value = int_value.to_bytes(bytes_length, byteorder="little", signed=True)
        if typ.nullable:
            buffer_write(b"\x00")
        buffer_write(bytes_value)
    elif family == FAMILY_FIXED_STRING:
        if value is None and typ.nullable:
            buffer_write(b"\x01")
            return
        value = value.encode("utf-8") if not isinstance(value, bytes) else value
        padding = typ.subtype - len(value)
        if padding < 0:
            raise StringTooLong()
        if typ.nullable:
            buffer_write(b"\x00")
        buffer_write(value + b"\x00" * padding)
    elif family == FAMILY_BIG_NUMERIC:
        if value is None and typ.nullable:
            buffer_write(b"\x01")
            return
        if typ.nullable:
            buffer_write(b"\x00")
        if is_number_out_of_range(value, typ.limits):
            raise IntegerOutOfRange(
                "Error parsing integer",
                typ.type_str,
                typ.limits.min_str,  # type: ignore
                typ.limits.max_str,  # type: ignore
                value,
            )
        signed, bytes_length = typ.subtype
        value = value.to_bytes(bytes_length, byteorder="little", signed=signed)
        buffer_write(value)


fast_leb_table = None


class JSONToRowbinary:
    def __init__(
        self,
        extended_json_deserialization: ExtendedJSONDeserialization,
        topic=None,
        truncate_value=False,
        store_headers=False,
        store_binary_headers=False,
    ):
        self.leb128_buffer = fast_leb128.create_buffer()
        global fast_leb_table
        if not fast_leb_table:
            fast_leb_table = [bytes(fast_leb128_encode(self.leb128_buffer, x)) for x in range(0, 256)]
        self.fast_leb_table = fast_leb_table
        self.bin_buffer = BytesIO()
        self.quarantine_buffer = BytesIO()
        self.extended_json_deserialization = extended_json_deserialization
        self.total_rows = 0
        self.quarantine_rows = 0
        self.invalid_rows = 0
        if topic:
            topic_utf8 = topic.encode("utf-8")
            self.topic_encoded = bytes(fast_leb128_encode(self.leb128_buffer, len(topic_utf8))) + topic_utf8
        self.truncate_value = truncate_value
        self.store_headers = store_headers
        self.store_binary_headers = store_binary_headers

    def write_start_value(self, value=True):
        has_value_flag = b"\x00" if value is not None and value is not False else b"\x01"
        self.bin_buffer.write(has_value_flag)

    def write_start_value_quarantine(self, value=True):
        has_value_flag = b"\x00" if value is not None and value is not False else b"\x01"
        self.quarantine_buffer.write(has_value_flag)

    def get_value(self, _object, _path, _type):
        _value = _object.get(_path, None)
        if not _type.has_default_value and _value is None and not _type.family == FAMILY_JSON:
            if _path not in _object:
                raise KeyError()
            else:
                raise NullNotAllowedException()

        return _value

    def convert(self, json_obj, metadata=None, import_id=None, obj=None):
        # THIS FUNCTION IS THE CURRENT HFI/NDJSON/PARQUETKAFKA HOT SPOT
        # MODIFICATIONS HERE SHOULD COME WITH PROPER BENCHMARKING
        # TO COMPARE THE PERFORMANCE BEFORE/AFTER THE CHANGES
        #
        # Desired encoding defined by CH docs:
        # https://clickhouse.tech/docs/en/interfaces/formats/#rowbinary
        # struct.pack docs:
        # https://docs.python.org/3.8/library/struct.html#format-characters
        error_columns: List[Optional[str]] = []
        errors: List[str] = []
        buffer_write = self.bin_buffer.write
        quarantine_buffer_write = self.quarantine_buffer.write
        self_fast_leb_table = self.fast_leb_table
        extended_json_deserialization = self.extended_json_deserialization

        backup_index = self.bin_buffer.tell()
        quarantine_backup_index = self.quarantine_buffer.tell()
        obj_big_numeric = None

        try:
            simplepath = None

            if metadata:
                value = metadata[0]
                partition = metadata[1]
                offset = metadata[2]
                timestamp = metadata[3]
                key = metadata[4]

                if self.truncate_value:
                    self.write_start_value()
                    buffer_write(b"\x00")
                else:
                    value_len = len(value)
                    if value_len < 256:
                        value_len_encoded = self_fast_leb_table[value_len]
                    else:
                        value_len_encoded = fast_leb128_encode(self.leb128_buffer, value_len)
                    self.write_start_value()
                    buffer_write(value_len_encoded)
                    buffer_write(value)

                self.write_start_value()
                buffer_write(self.topic_encoded)
                if not (timestamp >= 0 and timestamp <= 4294967295):
                    # sometimes timestamp is invalid
                    timestamp = 0

                self.write_start_value()
                buffer_write(struct.Struct(struct_format_table["Int16"]).pack(partition))

                self.write_start_value()
                buffer_write(struct.Struct(struct_format_table["Int64"]).pack(offset))

                self.write_start_value()
                buffer_write(datetime_struct_packer(int(timestamp)))

                self.write_start_value()
                if key is None:
                    buffer_write(b"\x00")
                else:
                    key_len = len(key)
                    if key_len < 256:
                        key_len_encoded = self_fast_leb_table[key_len]
                    else:
                        key_len_encoded = fast_leb128_encode(self.leb128_buffer, key_len)
                    buffer_write(key_len_encoded)
                    buffer_write(key)

                if self.store_headers:
                    headers = metadata[5]
                    self.write_start_value()
                    if self.store_binary_headers:
                        mapType = get_jsontype("Map(String,String)", True)
                        rowbinary_serialize(mapType, headers, buffer_write, self.leb128_buffer)
                    else:
                        # legacy headers stored as JSON
                        if headers is None:
                            buffer_write(b"\x00")
                        else:
                            header_len = len(headers)
                            if header_len < 256:
                                header_len_encoded = self_fast_leb_table[header_len]
                            else:
                                header_len_encoded = fast_leb128_encode(self.leb128_buffer, header_len)
                            buffer_write(header_len_encoded)
                            buffer_write(headers)

            extended_json_deserialization = self.extended_json_deserialization
            if not extended_json_deserialization:
                return

            if obj is None:
                obj = orjson.loads(json_obj)

            if not isinstance(obj, dict) and len(extended_json_deserialization.simplepath_to_column_name):
                error_columns.append("")
                res = json_obj.decode("utf-8", "replace").replace("\n", "")
                errors.append(f"JSON root must be an object, but it was a {get_type(obj)}")
                obj = {}
                return

            # This is basically an optimized inlining version of rowbinary_serialize
            # for performance reasons
            _name: Optional[str] = None
            is_number_error_added = False
            for simplepath, typ in extended_json_deserialization.strings:
                try:
                    value = self.get_value(obj, simplepath, typ)
                    if typ.family == FAMILY_JSON:
                        if not isinstance(value, dict):
                            raise InvalidJsonValue()
                        value = orjson.dumps(value)
                    if value is not None and not isinstance(value, bytes):
                        # Quick fix to avoid quarantine in some edge cases
                        # (datetime guessed as string by error in analyze function)
                        if isinstance(value, datetime.datetime):
                            value = str(value)
                        # Quick fix to avoid quarantine in JSON objects
                        # being mapped to String
                        if isinstance(value, dict):
                            value = orjson.dumps(value)
                        value = value.encode("utf-8") if not isinstance(value, bytes) else value
                except AttributeError:
                    raise NullNotAllowedException()
                if value is not None:
                    value_len = len(value)
                    if value_len < 256:
                        value_len_encoded = self_fast_leb_table[value_len]
                    else:
                        value_len_encoded = fast_leb128_encode(self.leb128_buffer, value_len)
                    self.write_start_value(value)
                    buffer_write(value_len_encoded)
                    buffer_write(value)
                else:
                    self.write_start_value(value)

            for simplepath, typ in extended_json_deserialization.numerics:
                value = self.get_value(obj, simplepath, typ)
                try:
                    if value is None:
                        self.write_start_value(value)
                        continue
                    else:
                        _bytes = typ.struct_format(value)
                        self.write_start_value()
                        buffer_write(_bytes)
                except struct.error:
                    if is_number_out_of_range(value, typ.limits):
                        _name = extended_json_deserialization.simplepath_to_column_name[simplepath]
                        msg = get_out_of_bounds_error(
                            _name, f"$.{simplepath}", typ.type_str, value, typ.limits.min_str, typ.limits.max_str
                        )
                        error_columns.append(_name)
                        errors.append(msg)
                        is_number_error_added = True
                    raise
            for simplepath, typ in extended_json_deserialization.datetimes:
                value = self.get_value(obj, simplepath, typ)
                if value is None and typ.has_default_value:
                    self.write_start_value(value)
                    continue
                if value is None:
                    raise NullNotAllowedException()
                try:
                    if isinstance(value, datetime.datetime):
                        timestamp = value
                    elif isinstance(value, datetime.date):
                        timestamp = datetime.datetime.fromtimestamp(time.mktime(value.timetuple()))
                    else:
                        timestamp = parse_datetime(value)
                except TypeError:
                    try:
                        timestamp = datetime.datetime.fromtimestamp(value)
                    except (OverflowError, OSError):
                        _name = extended_json_deserialization.simplepath_to_column_name[simplepath]
                        error_columns.append(_name)
                        errors.append(
                            f"Error DateTime parser failed. While processing column '{_name}' with jsonpath '$.{simplepath}'"
                        )
                        break
                    except ValueError:
                        try:
                            timestamp = datetime.datetime.fromtimestamp(value / 1000)
                        except ValueError:
                            _name = extended_json_deserialization.simplepath_to_column_name[simplepath]
                            error_columns.append(_name)
                            errors.append(
                                f"Error DateTime parser failed. While processing column '{_name}' with jsonpath '$.{simplepath}'"
                            )
                            break
                except ValueError:
                    _name = extended_json_deserialization.simplepath_to_column_name[simplepath]
                    error_columns.append(_name)
                    errors.append(
                        f"Error DateTime parser failed. While processing column '{_name}' with jsonpath '$.{simplepath}'"
                    )
                    break
                timestamp_posix = timestamp.timestamp()
                if is_datetime_out_of_range(timestamp_posix, typ.limits):
                    _name = extended_json_deserialization.simplepath_to_column_name[simplepath]
                    error_columns.append(_name)
                    errors.append(
                        get_out_of_bounds_error(
                            _name, f"$.{simplepath}", typ.type_str, value, typ.limits.min_str, typ.limits.max_str
                        )
                    )
                    break
                _bytes = datetime_struct_packer(int(timestamp_posix))
                self.write_start_value(value)
                buffer_write(_bytes)

            for simplepath, resolution_multiplier, typ in extended_json_deserialization.datetimes64:
                value = self.get_value(obj, simplepath, typ)
                if value is None and typ.has_default_value:
                    self.write_start_value(value)
                    continue
                try:
                    if isinstance(value, datetime.datetime):
                        timestamp = value
                    else:
                        timestamp = parse_datetime(value)
                except TypeError:
                    try:
                        timestamp = datetime.datetime.fromtimestamp(value)
                    except (OverflowError, OSError):
                        _name = extended_json_deserialization.simplepath_to_column_name[simplepath]
                        error_columns.append(_name)
                        errors.append(
                            f"Error DateTime parser failed. While processing column '{_name}' with jsonpath '$.{simplepath}'"
                        )
                        break
                    except ValueError:
                        try:
                            timestamp = datetime.datetime.fromtimestamp(value / 1000)
                        except ValueError:
                            _name = extended_json_deserialization.simplepath_to_column_name[simplepath]
                            error_columns.append(_name)
                            errors.append(
                                f"Error DateTime parser failed. While processing column '{_name}' with jsonpath '$.{simplepath}'"
                            )
                            break
                except ValueError:
                    _name = extended_json_deserialization.simplepath_to_column_name[simplepath]
                    error_columns.append(_name)
                    errors.append(
                        f"Error DateTime parser failed. While processing column '{_name}' with jsonpath '$.{simplepath}'"
                    )
                    break

                try:
                    timestamp_posix = timestamp.timestamp()
                except ValueError:
                    error_columns.append(_name)
                    errors.append(
                        get_out_of_bounds_error(
                            _name, f"$.{simplepath}", typ.type_str, value, typ.limits.min_str, typ.limits.max_str
                        )
                    )
                    break

                if is_datetime_out_of_range(timestamp_posix, typ.limits):
                    _name = extended_json_deserialization.simplepath_to_column_name[simplepath]
                    error_columns.append(_name)
                    errors.append(
                        get_out_of_bounds_error(
                            _name, f"$.{simplepath}", typ.type_str, value, typ.limits.min_str, typ.limits.max_str
                        )
                    )
                    break
                self.write_start_value(value)
                buffer_write(datetime64_struct_packer(int(timestamp_posix * resolution_multiplier)))

            # arrays, nested, map and nulls
            def is_family_big_numeric_or_subtype_big_numeric(typ):
                return typ.family == FAMILY_BIG_NUMERIC or (
                    typ.family == FAMILY_ARRAY
                    and typ.subtype is not None
                    and isinstance(typ.subtype, JSONType)
                    and typ.subtype.family == FAMILY_BIG_NUMERIC
                )

            for column, meta in extended_json_deserialization.complex:
                has_value = True
                try:
                    if not column.path:
                        # this is the root object
                        ch = "\n" if isinstance(json_obj, str) else b"\n"
                        value = json_obj.rstrip(ch)
                    elif is_family_big_numeric_or_subtype_big_numeric(column.typ):
                        if obj_big_numeric is None:
                            obj_big_numeric = msgspec.json.decode(json_obj)
                        value = value_at(obj_big_numeric, column.path)
                    else:
                        value = value_at(obj, column.path)
                except Exception:
                    has_value = False
                    if column.typ.is_nullable() or column.typ.has_default_value:
                        value = None
                    else:
                        error_columns.append(column.name)
                        errors.append(
                            f"Strict type checking failed. Null value not allowed on column '{column.name}'. While accessing jsonpath '{meta['jsonpath']}'"
                        )
                        break
                try:
                    if value is None and not column.typ.is_nullable() and not column.typ.has_default_value:
                        error_columns.append(column.name)
                        errors.append(
                            f"Strict type checking failed. Null value not allowed on column '{column.name}'. While accessing jsonpath '{meta['jsonpath']}'"  # TODO: extract function
                        )
                        break
                    if has_value and not column.typ.is_nullable() and value is None:
                        has_value = False

                    self.write_start_value(has_value)
                    rowbinary_serialize(
                        column.typ,
                        value,
                        buffer_write,
                        self.leb128_buffer,
                        has_value=has_value,
                    )
                except (DateTimeOutOfRange, DateTimeParseError) as e:
                    # if nullable, wrong dates are inserted as Null
                    if column.typ.nullable:
                        buffer_write(b"\x01")
                        continue
                    error_columns.append(column.name)
                    if isinstance(e, DateTimeOutOfRange):
                        errors.append(
                            get_out_of_bounds_error(column.name, meta["jsonpath"], meta["type"], value, e.min, e.max)
                        )
                    else:
                        _type = f"Nullable({meta['type']})" if meta["nullable"] else meta["type"]
                        errors.append(
                            f"Strict type checking failed. Value {value} on column '{column.name}' is a {get_type(value)} when a {_type} was expected. While accessing jsonpath '{meta['jsonpath']}'"
                        )
                    break
                except (IntegerOutOfRange, DecimalOutOfRange) as e:
                    error_columns.append(column.name)
                    errors.append(
                        get_out_of_bounds_error(
                            column=column.name,
                            jsonpath=meta["jsonpath"],
                            _type=meta["type"],
                            value=e.value,
                            min=e.min,
                            max=e.max,
                        )
                    )
                    break
                except (TypeError, struct.error, AttributeError):
                    error_columns.append(column.name)
                    _type = f"Nullable({meta['type']})" if meta["nullable"] else meta["type"]
                    errors.append(
                        f"Strict type checking failed. Value {value} on column '{column.name}' is a {get_type(value)} when a {_type} was expected. While accessing jsonpath '{meta['jsonpath']}'"
                    )
                    break
                except StringTooLong:
                    error_columns.append(column.name)
                    errors.append(get_string_too_long_error(column.name, meta["jsonpath"], meta["type"], value))
                    break
                except InvalidJsonValue:
                    error_columns.append(column.name)
                    errors.append(
                        f"Strict type checking failed. The value on column '{column.name}' is not a valid JSON Object. While accessing jsonpath '{meta['jsonpath']}'"
                    )
                    break
        except struct.error:
            if not is_number_error_added:
                _name = (
                    _name if _name is not None else extended_json_deserialization.simplepath_to_column_name[simplepath]
                )
                error_columns.append(_name)
                try:
                    path_type_index = extended_json_deserialization.query_columns.index(simplepath)
                    path_type = extended_json_deserialization.query_columns_types[path_type_index]
                    errors.append(
                        f"Strict type checking failed. Value {value} on column '{_name}' is a {get_type(value)} when a {path_type} was expected. While accessing jsonpath '$.{simplepath}'"
                    )
                except Exception:
                    errors.append(
                        f"Strict type checking failed. Value {value} on column '{_name}' is a {get_type(value)}. While accessing jsonpath '$.{simplepath}'"
                    )
        except orjson.JSONDecodeError:
            error_columns.append("")
            res = json_obj.decode("utf-8", "replace").replace("\n", "")
            errors.append(f"Line is not a valid JSON: '{res}'")
            obj = {}
        except KeyError:
            _name = _name if _name is not None else extended_json_deserialization.simplepath_to_column_name[simplepath]
            error_columns.append(_name)
            res = json_obj.decode("utf-8", "replace").replace("\n", "")
            errors.append(
                f"Strict type checking failed. Object does not have column '{_name}', you should send a value or recreate the table with a Nullable column type. While accessing jsonpath '$.{simplepath}'"
            )
        except NullNotAllowedException:
            _name = _name if _name is not None else extended_json_deserialization.simplepath_to_column_name[simplepath]
            error_columns.append(_name)
            errors.append(
                f"Strict type checking failed. Null value not allowed on column '{_name}'. While accessing jsonpath '$.{simplepath}'"
            )
        except InvalidJsonValue:
            _name = _name if _name is not None else extended_json_deserialization.simplepath_to_column_name[simplepath]
            msg = f"Strict type checking failed. The value on column '{_name}' is not a valid JSON Object. While accessing jsonpath '$.{simplepath}'"
            error_columns.append(_name)
            errors.append(msg)
            obj = {}
        except Exception as e:
            # at this point all errors should have been addressed
            error_columns.append("")
            err = f"Unknown error when parsing NDJSON: {e}\nTraceback: {traceback.format_exc()}"
            errors.append(err)
            obj = {}
            logging.warning(err)
        finally:
            self.total_rows += 1
            if len(errors):
                try:
                    self.append_to_quarantine(
                        error_columns,
                        errors,
                        import_id,
                        extended_json_deserialization,
                        quarantine_buffer_write,
                        obj_big_numeric if obj_big_numeric is not None else obj,
                        self_fast_leb_table,
                        self.leb128_buffer,
                        all_null=error_columns[0] == "",
                        metadata=metadata,
                    )
                    self.quarantine_rows += 1
                except Exception as exc:
                    logging.warning(f"Could not generate quarantine row: {exc}")
                    self.invalid_rows += 1
                    self.quarantine_buffer.seek(quarantine_backup_index, SEEK_SET)
                    self.quarantine_buffer.truncate(quarantine_backup_index)
                self.bin_buffer.seek(backup_index, SEEK_SET)
                self.bin_buffer.truncate(backup_index)

    def append_to_quarantine(
        self,
        error_columns,
        errors,
        import_id,
        extended_json_deserialization,
        quarantine_buffer_write,
        obj,
        self_fast_leb_table,
        leb128_buffer,
        all_null=False,
        metadata=None,
    ):
        if metadata:
            value = metadata[0]
            partition = metadata[1]
            offset = metadata[2]
            timestamp = metadata[3]
            key = metadata[4]

            self.write_start_value_quarantine()
            quarantine_buffer_write(b"\x01" if value is None else b"\x00")
            if value is not None:
                value_len = len(value)
                if value_len < 256:
                    value_len_encoded = self_fast_leb_table[value_len]
                else:
                    value_len_encoded = fast_leb128_encode(self.leb128_buffer, value_len)
                quarantine_buffer_write(value_len_encoded)
                quarantine_buffer_write(value)

            self.write_start_value_quarantine()
            quarantine_buffer_write(b"\x00")
            quarantine_buffer_write(self.topic_encoded)

            self.write_start_value_quarantine()
            quarantine_buffer_write(b"\x00")
            value = str(partition).encode("utf-8")
            if value:
                value_len = len(value)
                if value_len < 256:
                    value_len = self_fast_leb_table[value_len]
                else:
                    value_len = fast_leb128_encode(leb128_buffer, value_len)
                quarantine_buffer_write(value_len)
                quarantine_buffer_write(value)

            self.write_start_value_quarantine()
            quarantine_buffer_write(b"\x00")
            value = str(offset).encode("utf-8")
            if value:
                value_len = len(value)
                if value_len < 256:
                    value_len = self_fast_leb_table[value_len]
                else:
                    value_len = fast_leb128_encode(leb128_buffer, value_len)
                quarantine_buffer_write(value_len)
                quarantine_buffer_write(value)

            self.write_start_value_quarantine()
            quarantine_buffer_write(b"\x00")
            value = str(timestamp).encode("utf-8")
            if value:
                value_len = len(value)
                if value_len < 256:
                    value_len = self_fast_leb_table[value_len]
                else:
                    value_len = fast_leb128_encode(leb128_buffer, value_len)
                quarantine_buffer_write(value_len)
                quarantine_buffer_write(value)

            self.write_start_value_quarantine()
            quarantine_buffer_write(b"\x01" if key is None else b"\x00")
            if key is not None:
                key_len = len(key)
                if key_len < 256:
                    key_len_encoded = self_fast_leb_table[key_len]
                else:
                    key_len_encoded = fast_leb128_encode(self.leb128_buffer, key_len)
                quarantine_buffer_write(key_len_encoded)
                quarantine_buffer_write(key)

            if self.store_headers:
                self.write_start_value_quarantine()
                quarantine_buffer_write(b"\x00")
                headers = metadata[5]
                if headers is None:
                    quarantine_buffer_write(b"\x00")
                else:
                    if self.store_binary_headers:
                        headers = str(headers).encode("utf-8")
                    header_len = len(headers)
                    if header_len < 256:
                        header_len_encoded = self_fast_leb_table[header_len]
                    else:
                        header_len_encoded = fast_leb128_encode(self.leb128_buffer, header_len)
                    quarantine_buffer_write(header_len_encoded)
                    quarantine_buffer_write(headers)

        for simplepath in (
            extended_json_deserialization.strings
            + extended_json_deserialization.numerics
            + extended_json_deserialization.datetimes
            + extended_json_deserialization.datetimes64
        ):
            if isinstance(simplepath, tuple):
                simplepath = simplepath[0]
            if all_null:
                value = None
            else:
                value = obj.get(simplepath, None)
            self.write_start_value_quarantine()
            quarantine_buffer_write(b"\x01" if value is None else b"\x00")
            if value is None:
                continue
            if type(value) is not str:
                value = str(value)
            value = value.encode("utf-8")
            value_len = len(value)
            if value_len < 256:
                value_len = self_fast_leb_table[value_len]
            else:
                value_len = fast_leb128_encode(leb128_buffer, value_len)
            quarantine_buffer_write(value_len)
            quarantine_buffer_write(value)

        for column, _ in extended_json_deserialization.complex:
            try:
                if all_null:
                    value = None
                else:
                    value = value_at(obj, column.path)
            except Exception:
                value = None
            self.write_start_value_quarantine()
            quarantine_buffer_write(b"\x01" if value is None else b"\x00")
            if value is None:
                continue
            if type(value) is not str:
                value = str(value)
            value = value.encode("utf-8")
            value_len = len(value)
            if value_len < 256:
                value_len = self_fast_leb_table[value_len]
            else:
                value_len = fast_leb128_encode(leb128_buffer, value_len)
            quarantine_buffer_write(value_len)
            quarantine_buffer_write(value)

        # preserve this order -> c__error, c__error_column, c__import_id, insertion_date
        value = errors
        len_value = len(value) if value else 0
        array_len = self_fast_leb_table[len_value]
        self.write_start_value_quarantine()
        quarantine_buffer_write(array_len)
        if value:
            for x in value:
                x = x.encode("utf-8")
                value_len = len(x)
                if value_len < 256:
                    value_len = self_fast_leb_table[value_len]
                else:
                    value_len = fast_leb128_encode(leb128_buffer, value_len)
                quarantine_buffer_write(value_len)
                quarantine_buffer_write(x)

        value = error_columns
        len_value = len(value) if value else 0
        array_len = self_fast_leb_table[len_value]
        self.write_start_value_quarantine()
        quarantine_buffer_write(array_len)
        if value:
            for x in value:
                x = x.encode("utf-8")
                value_len = len(x)
                if value_len < 256:
                    value_len = self_fast_leb_table[value_len]
                else:
                    value_len = fast_leb128_encode(leb128_buffer, value_len)
                quarantine_buffer_write(value_len)
                quarantine_buffer_write(x)

        value = import_id
        self.write_start_value_quarantine()
        quarantine_buffer_write(b"\x01" if value is None else b"\x00")
        if value is not None:
            value = value.encode("utf-8")
            value_len = len(value)
            if value_len < 256:
                value_len = self_fast_leb_table[value_len]
            else:
                value_len = fast_leb128_encode(leb128_buffer, value_len)
            quarantine_buffer_write(value_len)
            quarantine_buffer_write(value)

        # insertion_date
        timestamp_posix = datetime.datetime.now().timestamp()
        self.write_start_value_quarantine()
        quarantine_buffer_write(datetime_struct_packer(int(timestamp_posix)))

    def flush(self):
        data = self.bin_buffer.getvalue()
        quarantine_data = self.quarantine_buffer.getvalue()
        self.reset()

        return data, quarantine_data

    def reset(self):
        self.bin_buffer.seek(0)
        self.bin_buffer.truncate()

        self.quarantine_buffer.seek(0)
        self.quarantine_buffer.truncate()


class IntegerOutOfRange(Exception):
    def __init__(self, message, int_type, min, max, value):
        super().__init__(message)
        self.int_type = int_type
        self.min = min
        self.max = max
        self.value = value


class DateTimeOutOfRange(Exception):
    def __init__(self, message, min, max):
        super().__init__(message)
        self.min = min
        self.max = max


class DecimalOutOfRange(Exception):
    def __init__(self, message, min, max, value):
        super().__init__(message)
        self.min = min
        self.max = max
        self.value = value


class StringTooLong(Exception):
    pass


class InvalidJsonValue(Exception):
    pass


def get_type(value):
    found_type = type(value)
    if found_type in (int, float):
        return "number"
    elif found_type is str:
        return "string"
    elif found_type is list:
        return "list"
    elif value is None:
        return "null"
    else:
        return str(found_type)
