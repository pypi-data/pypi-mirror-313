"""
Everything regarding guessing about CSV structure (header, types) and so on is here
"""

import csv
import logging
import re
import statistics
import string
from collections import namedtuple
from io import StringIO
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import numpy.typing as npt
from datasketch import MinHash

from .datatypes import guessers, numbers_types

csv.field_size_limit(1024 * 1024)

DELIMITERS = [
    (",", 1),
    ("\t", 1),
    (";", 1),
    ("|", 1),
    (" ", 0.7),
]

DelimiterMetrics = namedtuple("DelimiterMetrics", ["delimiter", "ratio", "mode", "weight", "rows"])


def guess_delimiter(csv_extract: str, escapechar: Optional[str] = None) -> str:
    """
    >>> guess_delimiter('a,b,c,d\\na,b,c,d')
    ','
    >>> guess_delimiter('a,"b|c|d",c,d\\na,b,c,d\\na,b,c,d')
    ','
    >>> guess_delimiter('"2020-04-23 14:09:42","2020-04-23 14:09:42","main","3e25a061-63d1-41bb-8e80-d2e5fb034b1e","http://192.168.1.51:8080/","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36","pageload","","","","","","",""')
    ','
    >>> guess_delimiter('"2020-04-23 14:09:42","2020-04-23 14:09:42","main","3e25a061-63d1-41bb-8e80-d2e5fb034b1e","http://192.168.1.51:8080/","Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/80.0.3987.95 Mobile/15E148 Safari/604.1","pageload","","","","","","",""')
    ','
    >>> guess_delimiter('1\\n2\\n3')
    ','
    >>> guess_delimiter('field 1.1;field 1.2;field 1.3\\nfield 2.1;field 2.2;field 2.3')
    ';'
    >>> guess_delimiter('field 1.1;field 1.2\;;field 1.3\\nfield 2.1;field 2.2;field 2.3')
    ' '
    >>> guess_delimiter('field 1.1;field 1.2\;;field 1.3\\nfield 2.1;field 2.2;field 2.3', '\\\\')
    ';'
    """
    delimiter_stdev = []
    delimiter_rows = []
    for delimiter, weight in DELIMITERS:
        try:
            rows = [
                row
                for row in csv.reader(StringIO(csv_extract, newline=None), delimiter=delimiter, escapechar=escapechar)
            ]
            delimiter_rows.append(len(rows))
            columns_per_row = [len(row) for row in rows]
            try:
                columns_count_mode = statistics.mode(columns_per_row)
                rows_different_than_mode = len([x for x in columns_per_row if x != columns_count_mode])
                if columns_count_mode > 1:  # We don't care about the delimiter if the number of columns is 1
                    delimiter_stdev.append(
                        DelimiterMetrics(
                            delimiter,
                            rows_different_than_mode / columns_count_mode,
                            columns_count_mode,
                            weight,
                            len(rows),
                        )
                    )
            except statistics.StatisticsError:
                # it raises an exception when there are equally common values
                # discard it since it's not a good candidate
                pass
        except csv.Error:
            # _csv.Error: field larger than field limit (131072), while trying a non-valid delimiter
            pass
    try:
        rows_mode = statistics.mode(delimiter_rows)
    except Exception:
        rows_mode = -1

    if not delimiter_stdev:
        # TODO: try to load using csv with every single delimiter
        logging.info("delimiter couldn't be guest, using default one")
        # I'm feeling lucky
        return DELIMITERS[0][0]
    # use - sign because we want higher to be first
    delimiter_stdev.sort(key=lambda a: (a.ratio, -a.mode * a.weight * (2 if rows_mode == a.rows else 1)))
    return delimiter_stdev[0][0]


def guess_number_of_columns(
    csv_extract: str, delimiter: str, number_of_rows_to_analize: Optional[int] = None, escapechar: Optional[str] = None
) -> int:
    """
    >>> guess_number_of_columns("", ",")
    0
    >>> guess_number_of_columns("1,2,3\\n1,2,3,4\\n1,2,3,4\\n1,2,3,4\\n", ",")
    4
    >>> guess_number_of_columns("1,2,3\\n1,2,3,4\\n1,2,3,4\\n1,2,3,4\\n", ",", 1)
    3
    """
    rows_processed = 0
    times = []

    def continue_processing_rows(processed):
        if not number_of_rows_to_analize:
            return True
        return processed <= number_of_rows_to_analize

    data = csv.reader(StringIO(csv_extract, newline=None), delimiter=delimiter, escapechar=escapechar)

    data_iterator = data.__iter__()
    while True:
        try:
            row = data_iterator.__next__()
            if not continue_processing_rows(rows_processed):
                break
            times.append(len(row))
            rows_processed += 1
        except StopIteration:
            break
        except Exception:
            continue

    if len(times) == 0:
        return 0
    try:
        mode = statistics.mode(times)
        if mode == 0:
            return times[0]
        return mode
    except statistics.StatisticsError:
        return times[0]


def guess_new_line(csv_extract: str) -> Optional[str]:
    """
    >>> guess_new_line('a,b,c,d\\r\\na,b,c,d\\r\\na,b,c,d')
    '\\r\\n'
    >>> guess_new_line('a,b,c,d\\ra,b,c,d\\ra,b,c,d')
    '\\r'
    >>> guess_new_line('a,b,c,d\\na,b,c,d\\na,b,c,d')
    '\\n'
    >>> guess_new_line('a,b,c,d')
    """
    unix = len(re.findall("\r\n", csv_extract))
    windows = len(re.findall("\n", csv_extract))
    mac = len(re.findall("\r", csv_extract))
    if not unix and not mac and not windows:
        return None
    if unix >= windows and unix >= mac:
        return "\r\n"
    elif windows > mac:
        return "\n"
    elif mac > 0:
        return "\r"
    raise Exception("no newline found")


def encode_line_structure(line: str) -> str:
    s = []
    for x in line.lower():
        if x in string.digits:
            s.append("D")
        elif x in string.punctuation:
            s.append("P")
        else:
            s.append("A")
    return "".join(s)


# Detect outliers using the median absolute deviation
def is_outlier(points: npt.NDArray[np.float_], thresh: float = 3.0) -> npt.NDArray[np.bool_]:
    """
    >>> is_outlier(np.array([0.5, 0.5, 0.5]))
    array([False, False, False])
    >>> is_outlier(np.array([0.5, 0.5, 100]))
    array([False, False,  True])
    >>> is_outlier(np.array([0.5, 0.6, 0.7]))
    array([False, False, False])
    >>> is_outlier(np.array([50, 60, 70]))
    array([False, False, False])
    >>> is_outlier(np.array([50, 60, 150]))
    array([False, False,  True])
    >>> is_outlier(np.array([0, 0, 0, 0, 0, 5]))
    array([False, False, False, False, False,  True])
    """
    if len(points.shape) == 1:
        points = points[:, None]
    median = np.median(points)
    diff = np.sqrt(np.sum((points - median) ** 2, axis=-1))
    med_abs_deviation = np.median(diff)
    return 0.6745 * diff > thresh * med_abs_deviation


def has_header(
    csv_extract: str, delimiter: str, escapechar: Optional[str] = None
) -> Union[Tuple[bool, str, int], Tuple[bool, int, int]]:
    """compares the first line with the other ones and check they are different
    >>> has_header('"abcd","1.3","2019-01-13","2019-04-14","131600.0","131600.0"\\n"abcd","1.3","2019-01-13","2019-04-14","131600.0","131600.0"', ',')[0]
    False
    >>> has_header('aa %CE%92%CE 1 4854\\naa %CE%98%CE%B5 1 4917\\naa %AD%CF%84_%CE%95 1 4832\\naa %CE%A0%CE%B9 1 4828', ' ')
    (False, '', 0)
    >>> has_header('1,3.74,248190913\\n567,233.74,909132481', ',')
    (False, '', 0)
    >>> has_header('1589446145571,Chrome,81.0,', ',')
    (False, '', 0)
    """

    # TODO use difference between guessed types and header type check to evaluate, for example, when a
    # column is integer and just the first line has characters is an indicator that file has header
    column_number = guess_number_of_columns(csv_extract, delimiter)

    # we use this list to return the actual header length
    header_line = next(StringIO(csv_extract, newline=None))

    # skip white lines and mal formed ones
    unquoted_lines: List[str] = []

    header_candidate = StringIO()
    rows_candidates = StringIO()
    wrote_header = False

    csv_header_writer = csv.writer(header_candidate, delimiter=delimiter, quoting=csv.QUOTE_ALL)
    csv_body_writer = csv.writer(rows_candidates, delimiter=delimiter, quoting=csv.QUOTE_ALL)

    for row in csv.reader(StringIO(csv_extract, newline=None), delimiter=delimiter, escapechar=escapechar):
        if len(row) == column_number:
            # csv.reader does not preserve quotes, so next time we guess_number_of_columns
            # it might give inconsistent results (for example when a double quoted field contained a linebreak)
            # source file might not have quotes at all, but adding them it doesn't harm to the rest of the logic
            if wrote_header:
                csv_body_writer.writerow(row)
            else:
                csv_header_writer.writerow(row)
                wrote_header = True
            unquoted_lines.append(delimiter.join(row))

    if len(unquoted_lines) == 1:
        return False, "", 0

    columns_header = [x for x in guess_columns(header_candidate.getvalue(), delimiter)]
    columns_rows = [x for x in guess_columns(rows_candidates.getvalue(), delimiter)]

    if any(
        x["type"].startswith("Date")
        or x["type"].startswith("Float")
        or x["type"].startswith("Int")
        or x["type"].startswith("UInt")
        for x in columns_header
    ):
        return False, "", 0

    # all integers, no header
    if all(x["type"] in numbers_types for x in columns_header):
        return False, "", 0

    # when a column in the header is not null and its type is different from the type on the rows
    # that means it's a header
    for i, h in enumerate(columns_header):
        if i >= len(columns_rows):
            break
        r = columns_rows[i]
        if not h["nullable"] and h["type"] != r["type"]:
            header = header_line.strip()
            return True, hash(header), len(header)

    # This minhash technique doesn't work well with few lines
    hashes = []
    for line in unquoted_lines:
        hashes.append(hash_line(line))

    # calculate distance to 10 other lines (use **2 to get lines not very close since closer ones tend to look alike)
    distances = []
    for i, _x in enumerate(hashes):
        distances.append(np.mean([hashes[i].jaccard(hashes[rr**2 % len(hashes)]) for rr in range(10)]))

    outliers = is_outlier(np.array(distances))
    header = header_line.strip()
    return outliers[0], hash(header), len(header)


def hash_line(line: str) -> MinHash:
    m = MinHash(num_perm=128)
    data = encode_line_structure(line)
    for x in data.split("P"):
        m.update(x.encode("utf-8"))
    return m


def dialect_header_len(dialect: Dict[str, Any]) -> int:
    if dialect["has_header"]:
        return dialect["header_len"] + len(dialect["new_line"])
    return 0


def get_dialect(csv_extract: str, dialect_overrides: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    dialect_overrides = dialect_overrides or {}
    escapechar = dialect_overrides.get("escapechar", None)

    delimiter = dialect_overrides.get("delimiter", None) or guess_delimiter(csv_extract, escapechar)
    hh, header_hash, header_len = has_header(csv_extract, delimiter, escapechar)
    new_line = dialect_overrides.get("new_line", None) or guess_new_line(csv_extract)

    return {
        "delimiter": delimiter,
        "escapechar": escapechar,
        "has_header": hh,
        "header_hash": header_hash,
        "header_len": header_len,
        "new_line": new_line,
    }


def value_type(value: str) -> str:
    """
    >>> value_type('')
    'Null'
    >>> value_type('\\\\N')
    'Null'
    >>> value_type('2')
    'Int8'
    >>> value_type('2.0')
    'Float32'
    >>> value_type('asd2.0')
    'String'
    >>> value_type('2018-09-01')
    'Date'
    >>> value_type('2018-09-01 00:12:32')
    'DateTime'
    >>> value_type('2018-09-01T00:12:32')
    'DateTime'
    >>> value_type('2018-05-16T00:00:00.000Z')
    'DateTime64'
    >>> value_type('-73.967269897460937')
    'Float32'
    >>> value_type('40.769187927246094')
    'Float32'
    >>> value_type('2017-12-24 00:00:00 +0100')
    'DateTime'
    >>> value_type("2018-09-29_2018-09-30_2018-09-29_AIR3314465_INFERRED")
    'String'
    >>> value_type("03/07/2019 6:10:08")
    'DateTime'
    >>> value_type('28079004_1_38')
    'String'
    >>> value_type('[1,2,3]')
    'Array(Int32)'
    >>> value_type("['1','2','3']")
    'Array(String)'
    >>> value_type("[1.0,2.0,3.0]")
    'Array(Float32)'
    >>> value_type("['1.0',2.0,3.0]")
    'String'
    >>> value_type("[]")
    'Null'
    >>> value_type("1100024563867")
    'Int64'
    >>> value_type("1100024563867.1")
    'Float64'
    >>> value_type(str(pow(2,15)))
    'UInt16'
    >>> value_type(str(pow(2,16)))
    'Int32'
    """
    if not value or value == "\\N" or value == "[]":
        return "Null"
    for k, t in guessers.items():
        if t(value):
            return k
    return "String"


integers_s = ["Int64", "Int32", "Int16", "Int8"]
integers_u = ["UInt64", "UInt32", "UInt16", "UInt8"]
floats = ["Float32", "Float64"]
integers_s_types = set(integers_s)
integers_u_types = set(integers_u)
integers_types = set(integers_s + integers_u)
float_types = set(floats)


def pick_type(types: List[str]) -> str:
    """
    >>> pick_type(['Null', 'Null'])
    'String'
    >>> pick_type(['Int8', 'UInt8', 'Int16'])
    'Int32'
    >>> pick_type(['Int8', 'Int16', 'UInt16'])
    'Int32'
    >>> pick_type(['Int8', 'UInt8'])
    'Int16'
    >>> pick_type(['UInt8', 'Int8'])
    'Int16'
    >>> pick_type(['UInt64', 'UInt32'])
    'UInt64'
    >>> pick_type(['Int16'])
    'Int32'
    >>> pick_type(['UInt16'])
    'UInt32'
    >>> pick_type(['Int64', 'UInt64'])
    'Int64'
    >>> pick_type(['UInt64', 'UInt16'])
    'UInt64'
    >>> pick_type(['Float32', 'Int16'])
    'Float32'
    >>> pick_type(['Float32', 'UInt16'])
    'Float32'
    >>> pick_type(['Float32', 'Int16', 'Int8', 'UInt8'])
    'Float32'
    >>> pick_type(['Float32', 'Int16', 'Int8', 'String'])
    'String'
    >>> pick_type(['Float32', 'Float64', 'Int8'])
    'Float64'
    """
    types_as_set = set([t for t in types if t != "Null"])
    if types_as_set and len(integers_types & types_as_set) == len(types_as_set):
        best_integer_type = "Int64"
        if integers_u_types & types_as_set:
            best_integer_type = next(
                (integers_u[max(i - 1, 0)] for i, itype in enumerate(integers_u) if itype in types_as_set), "UInt64"
            )
        if integers_s_types & types_as_set:
            best_integer_type = next(
                (integers_s[max(i - 1, 0)] for i, itype in enumerate(integers_s) if itype in types_as_set), "Int64"
            )
        return best_integer_type
    elif len(types_as_set) == 1:
        return list(types_as_set)[0]
    elif len(types_as_set) == 2:
        if "Float32" in types_as_set and (integers_types & types_as_set):
            return "Float32"
        if "Float64" in types_as_set and (integers_types & types_as_set):
            return "Float64"
    elif len(types_as_set) > 2:
        non_integer_types = types_as_set - integers_types - float_types
        if "Float64" in types_as_set and len(non_integer_types) == 0:
            return "Float64"
        if "Float32" in types_as_set and len(non_integer_types) == 0:
            return "Float32"
    # safer
    return "String"
    """
    if len([x for t in x if t != 'Null']) == 0:
        return 'String' # all of them are null, so we set to string to be safe
    if all(t == x[0] for t in x if t != 'Null'):
        return x[0]
    if all(t == x[0] for t in x if t != 'Null'):
        return x[0]
    if any(t == 'String' for t in x if t != 'Null'):
        return 'Stringhttps://duckduckgo.com/?q=hijos+julio+iglesias&ia=web'
    if any(t == 'Float32' for t in x if t != 'Null'):
        return 'Float32'
    """


def column_names(csv_extract: str, delimiter: str, column_number: int) -> List[str]:
    """
    >>> column_names('a,b,c,d\\n1,2.0,c,d\\n3,2.1,2,d', delimiter=',', column_number=4)
    ['a', 'b', 'c', 'd']
    >>> column_names('a,B,c,D\\n1,2.0,c,d\\n3,2.1,2,d', delimiter=',', column_number=4)
    ['a', 'b', 'c', 'd']
    """
    r = csv.reader(StringIO(csv_extract, newline=None), delimiter=delimiter)
    first_row = next(x for x in r if len(x) == column_number)
    # check all of them have non empty value

    return [x.lower() if x else "unnamed_%d" % i for i, x in enumerate(first_row)]


def guess_column_names(
    csv_extract: str, delimiter: str, column_number: int, escapechar: Optional[str] = None
) -> List[str]:
    r = csv.reader(StringIO(csv_extract, newline=None), delimiter=delimiter, escapechar=escapechar)
    # skip empty lines or invalid lines
    first_row = next(x for x in r if len(x) == column_number)
    return ["column_%02d" % i for i in range(len(first_row))]


def guess_columns(csv_extract: str, delimiter: str, escapechar: Optional[str] = None) -> List[Dict[str, Any]]:
    # flake8: noqa: E501
    """
    >>> guess_columns('a,b,c,d\\n1,2.0,c,d\\n3,2.1,2,d', delimiter=',')
    [{'type': 'Int16', 'nullable': False}, {'type': 'Float32', 'nullable': False}, {'type': 'String', 'nullable': False}, {'type': 'String', 'nullable': False}]
    >>> guess_columns('a,b,c,d\\n1,2.0,c,d\\n3,2.1,,d', delimiter=',')
    [{'type': 'Int16', 'nullable': False}, {'type': 'Float32', 'nullable': False}, {'type': 'String', 'nullable': True}, {'type': 'String', 'nullable': False}]
    >>> guess_columns('a\\n2019-02-01', delimiter=',')
    [{'type': 'Date', 'nullable': False}]
    >>> guess_columns('a\\n"2019-02-01"', delimiter=',')
    [{'type': 'Date', 'nullable': False}]
    >>> guess_columns('a,"2019-02-01"', delimiter=',')
    [{'type': 'String', 'nullable': False}, {'type': 'Date', 'nullable': False}]
    >>> guess_columns('a,b,c,d\\n\\\\N,2.0,c,d\\n3,2.1,2,d', delimiter=',')
    [{'type': 'Int16', 'nullable': True}, {'type': 'Float32', 'nullable': False}, {'type': 'String', 'nullable': False}, {'type': 'String', 'nullable': False}]
    """
    if len(csv_extract) == 0:
        return []

    column_number = guess_number_of_columns(csv_extract, delimiter)
    r = csv.reader(StringIO(csv_extract, newline=None), delimiter=delimiter, escapechar=escapechar)

    # skip new line just in case
    f: List[Any] = []

    while len(f) == 0 or len(f) != column_number:
        try:
            f = next(r)
        except StopIteration:
            break

    column_types: List[List[Any]] = [[] for x in f]
    nrows = 0
    for row in r:
        if len(row) == len(f):
            nrows += 1
            for i, column in enumerate(row):
                column_types[i].append(value_type(column))
    else:
        # just one row
        if nrows == 0:
            for i, column in enumerate(f):
                column_types[i].append(value_type(column))

    guessed_column_types = []
    for x in column_types:
        _type = pick_type(x)
        guessed_column_types.append(
            {
                "type": _type,
                # array types can't be nullable
                "nullable": any(t == "Null" for t in x) and not _type.startswith("Array"),
            }
        )
    return guessed_column_types


if __name__ == "__main__":
    import sys

    with open(sys.argv[1], "rb") as file:
        data = file.read().decode()

    delimiter = guess_delimiter(data)  # [:100*1024])
    print(guess_number_of_columns(data, delimiter))  # noqa: T201
    print(has_header(data, delimiter))  # noqa: T201
    print(guess_columns(data, delimiter))  # noqa: T201
