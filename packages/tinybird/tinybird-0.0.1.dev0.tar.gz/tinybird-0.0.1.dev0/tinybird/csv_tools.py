import asyncio
import csv
from datetime import date, datetime
from enum import Enum
from io import StringIO
from typing import Any, List
from uuid import UUID

text_type = str


def is_quoted(s: str) -> bool:
    return len(s) > 1 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'"))


def object_to_csv_string(item: Any, quote_string: bool = False) -> str:
    if item is None:
        return "\\N"

    elif isinstance(item, datetime):
        return "%s" % item.strftime("%Y-%m-%d %H:%M:%S")

    elif isinstance(item, date):
        return "%s" % item.strftime("%Y-%m-%d")

    elif isinstance(item, list) or isinstance(item, tuple):
        return "[%s]" % ", ".join(text_type(object_to_csv_string(x, True)) for x in item)

    elif isinstance(item, Enum):
        return object_to_csv_string(item.value, quote_string=quote_string)

    elif isinstance(item, UUID):
        return "%s" % str(item)

    else:
        if isinstance(item, str):
            if quote_string:
                # We use single quotes for inner structures => "['a', 'list']"
                # ClickHouse does not deal with double quotes => "[""a"", ""list""]"
                return "'%s'" % item.replace("'", "''")
            if is_quoted(item):
                item = item[1:-1]
            return item
        return item


def csv_from_python_object(rows: List[Any]) -> str:
    """
    generates csv from a list of python objects
    >>> csv_from_python_object([[datetime(2018, 9, 7, 23, 50), date(2019, 9, 7), 'tes"t', 123.0, None, 3]])
    '"2018-09-07 23:50:00","2019-09-07","tes""t","123.0",\\\\N,"3"\\r\\n'
    >>> csv_from_python_object([[[], [1,2,3], ['1', '2', '3']]])
    '"[]","[1, 2, 3]","[\\'1\\', \\'2\\', \\'3\\']"\\r\\n'
    >>> csv_from_python_object([[[], [1,2,3], ['1', 'what\\'s your name', '3']]])
    '"[]","[1, 2, 3]","[\\'1\\', \\'what\\'\\'s your name\\', \\'3\\']"\\r\\n'

    >>> csv_from_python_object([["column with single quote ' <- here"]])
    '"column with single quote \\' <- here"\\r\\n'
    >>> csv_from_python_object([["column with , comma"]])
    '"column with , comma"\\r\\n'

    # flake8: noqa: E501
    # FIXME The column index=13, value="'NoneType' object has no attribute 'install_hook'"
    # FIXME is not properly encoded when used in BufferedInsert.insert_buffer.
    >>> rows = [[7630219889256120669, 'APIDataSourceHandler', 1580913067, 1580913067.5470011, 0.00055694580078125, None, 'tornado', None, '58a6add2-99d1-4011-9031-168b760577eb', 'user@example.com', '/v0/datasources/wadus', 'DELETE', None, "'NoneType' object has no attribute 'install_hook'", ['{"timestamp": 1580913067.5475516, "values": {"event": "error", "error.object": null}}'], '{"span.kind": "server", "user": "58a6add2-99d1-4011-9031-168b760577eb", "user_email": "user@example.com"}']]
    >>> _ = csv_from_python_object(rows)
    """
    csv_chunk = StringIO()
    w = csv.writer(csv_chunk, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
    w.writerows([map(object_to_csv_string, x) for x in rows])
    b = csv_chunk.getvalue()
    # Workaround CH treating '"\\N"' as the string literal instead of None
    # QUOTE_MINIMAL cannot be used to fix this, as that introduces the problem
    # of leaving single quotes without proper treatment
    return b.replace('"\\N"', "\\N")


async def csv_from_python_object_async(rows: List[Any]) -> str:
    """
    generates csv from a list of python objects
    >>> asyncio.run(csv_from_python_object_async([[datetime(2018, 9, 7, 23, 50), date(2019, 9, 7), 'tes"t', 123.0, None, 3]]))
    '"2018-09-07 23:50:00","2019-09-07","tes""t","123.0",\\\\N,"3"\\r\\n'
    >>> asyncio.run(csv_from_python_object_async([[[], [1,2,3], ['1', '2', '3']]]))
    '"[]","[1, 2, 3]","[\\'1\\', \\'2\\', \\'3\\']"\\r\\n'
    >>> asyncio.run(csv_from_python_object_async([[[], [1,2,3], ['1', 'what\\'s your name', '3']]]))
    '"[]","[1, 2, 3]","[\\'1\\', \\'what\\'\\'s your name\\', \\'3\\']"\\r\\n'
    >>> asyncio.run(csv_from_python_object_async([["column with single quote ' <- here"]]))
    '"column with single quote \\' <- here"\\r\\n'
    >>> asyncio.run(csv_from_python_object_async([["column with , comma"]]))
    '"column with , comma"\\r\\n'

    # flake8: noqa: E501
    # FIXME The column index=13, value="'NoneType' object has no attribute 'install_hook'"
    # FIXME is not properly encoded when used in BufferedInsert.insert_buffer.
    >>> rows = [[7630219889256120669, 'APIDataSourceHandler', 1580913067, 1580913067.5470011, 0.00055694580078125, None, 'tornado', None, '58a6add2-99d1-4011-9031-168b760577eb', 'user@example.com', '/v0/datasources/wadus', 'DELETE', None, "'NoneType' object has no attribute 'install_hook'", ['{"timestamp": 1580913067.5475516, "values": {"event": "error", "error.object": null}}'], '{"span.kind": "server", "user": "58a6add2-99d1-4011-9031-168b760577eb", "user_email": "user@example.com"}']]
    >>> _ = asyncio.run(csv_from_python_object_async(rows))
    """
    csv_chunk = StringIO()
    w = csv.writer(csv_chunk, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
    processed_rows_without_yield = 0
    for row in rows:
        w.writerows([map(object_to_csv_string, x) for x in [row]])
        processed_rows_without_yield += 1
        if processed_rows_without_yield >= 10:
            processed_rows_without_yield = 0
            await asyncio.sleep(0)
    b = csv_chunk.getvalue()
    # Workaround CH treating '"\\N"' as the string literal instead of None
    # QUOTE_MINIMAL cannot be used to fix this, as that introduces the problem
    # of leaving single quotes without proper treatment
    return b.replace('"\\N"', "\\N")
