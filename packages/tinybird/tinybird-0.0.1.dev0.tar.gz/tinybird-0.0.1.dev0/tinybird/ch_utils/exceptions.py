import logging
import re
from dataclasses import dataclass
from typing import List, Optional

from tornado.httputil import HTTPHeaders

from tinybird_shared.clickhouse.errors import (
    MEMORY_LIMIT_FOR_QUERY_EXCEEDED,
    MEMORY_LIMIT_TOTAL_EXCEEDED,
    CHErrors,
    get_name_from_ch_code,
)

SQL_TIP_TAG = "Contact us at support@tinybird.co for help or read this SQL tip: "
AGG_FN_REGEX = re.compile("(?<=for aggregate function )(.*)(?=\. )")
BACKTICKS_PATTERN = re.compile("`([^`]+)`")


@dataclass
class CHCustomError:
    codes: List[int]
    message: str
    doc: str

    def __init__(self, codes: List[int], message: str, doc: str, use_sql_tip: Optional[bool] = True):
        self.codes = codes
        self.message = f"{message} {SQL_TIP_TAG} {doc}" if use_sql_tip else f"{message} {doc}"
        self.doc = doc


class CHCustomErrors:
    wrong_partition = CHCustomError(
        [CHErrors.INVALID_PARTITION_VALUE, CHErrors.TOO_MANY_PARTS, CHErrors.TOO_MANY_PARTITIONS],
        "Please make sure the ENGINE_PARTITION_KEY setting is correct. Large number of partitions is a common misconception. Partitioning is not intended to speed up SELECT queries (the ENGINE_SORTING_KEY is sufficient to make range queries fast), partitions are intended for data manipulation.",
        "https://www.tinybird.co/docs/concepts/data-sources.html#partitioning",
    )

    illegal_aggregation = CHCustomError(
        [CHErrors.ILLEGAL_AGGREGATION],
        "You cannot use the aggregate function '{agg_problematic_function}' or its alias inside another aggregate function.",
        "https://www.tinybird.co/docs/concepts/data-sources.html#partitioning",
    )

    needs_merge = CHCustomError(
        [CHErrors.ILLEGAL_TYPE_OF_ARGUMENT],
        "Some columns need to be aggregated by using the -Merge suffix.{merge_hint} Make sure you do this as late in the pipeline as possible for better performance",
        "https://tinybird.co/docs/guides/best-practices-for-faster-sql.html#merging-aggregate-functions",
    )

    too_many_simultaneous_queries = CHCustomError(
        [CHErrors.TOO_MANY_SIMULTANEOUS_QUERIES],
        "The server is processing too many queries at the same time. This could be because there are more requests than usual, because they are taking longer, or because the server is overloaded. Please check your requests or contact us at support@tinybird.co",
        "",
    )

    internal_clickhouse_error = CHCustomError(
        [CHErrors.BACKUP_NOT_FOUND],
        "Request failed due to an internal error. If the problem persists, please contact us at support@tinybird.co",
        "",
        False,
    )

    unknown_secret_error = CHCustomError(
        [CHErrors.UNKNOWN_QUERY_PARAMETER],
        "Cannot access secret '{x}'. Check the secret exists in the Workspace and the token has the required scope.",
        "",
        False,
    )

    postgres_statement_timeout_error = CHCustomError(
        [CHErrors.STD_EXCEPTION],
        "Query cancelled due to statement timeout in postgres. Make sure you use a user with a proper statement timeout to run this type of query.",
        "",
        False,
    )

    postgres_lost_connection_error = CHCustomError(
        [CHErrors.STD_EXCEPTION],
        "Lost connection to postgres database. You might need to specify the optional `schema` argument. Usage: postgresql(host:port, database, table, user, password, schema)",
        "",
        False,
    )

    memory_limit = CHCustomError(
        [CHErrors.MEMORY_LIMIT_EXCEEDED],
        "Memory limit (for query) exceeded. Make sure the query just process the required data.",
        "https://tinybird.co/docs/guides/best-practices-for-faster-sql.html#memory-limit-reached-title",
    )


class CHException(Exception):
    def __init__(self, ch_error: Optional[str], fatal: bool = False, headers: HTTPHeaders = None):
        """
        >>> e = CHException('Code: 62, e.displayText() = DB::Exception: Syntax error: failed at position 99 (line 1, col 99): h, avg(trip_distance) c from `yellow_tripdata_2017_06` group by d, h order by h asc format JSON . Expected one of: IN, alias, AND, OR, token, IS, BETWEEN, LIKE, NOT LIKE, NOT IN, GLOBAL IN, GLOBAL NOT IN, Comma, QuestionMark, AS, e.what() = DB::Exception')
        >>> str(e)
        '[Error] Syntax error: failed at position 99 (line 1, col 99): h, avg(trip_distance) c from `yellow_tripdata_2017_06` group by d, h order by h asc format JSON . Expected one of: IN, alias, AND, OR, token, IS, BETWEEN, LIKE, NOT LIKE, NOT IN, GLOBAL IN, GLOBAL NOT IN, Comma, QuestionMark, AS,'

        >>> e = CHException('(version 19.6.1.1) Code: 57, e.displayText() = DB::Exception: Table d_821dba.tracker already exists.')
        >>> str(e)
        '[Error] Table d_821dba.tracker already exists.'
        >>> e.code
        57

        >>> e = CHException('Code: 32, e.displayText() = DB::Exception: Attempt to read after eof: Cannot parse Int16 from String, because value is too short (version 19.13.1.1)')
        >>> str(e)
        '[Error] Attempt to read after eof: Cannot parse Int16 from String, because value is too short'
        >>> e.code
        32
        >>> e = CHException(None)
        >>> str(e)
        '[Unknown error]'
        >>> e = CHException('CH return code: 70')
        >>> str(e)
        '[Unknown error: 70 - CANNOT_CONVERT_TYPE]'
        >>> e =CHException('empty response from ClickHouse server: HTTP 599: Operation timed out after 20 seconds')
        >>> str(e)
        '[Error] empty response from ClickHouse server: HTTP 599: Operation timed out after 20 seconds'

        >>> e = CHException('Poco::Exception. Code: 1000, e.code() = 0, e.displayText() = Exception: Cannot load time zone AAAAAAA (version 21.3.13.1)')
        >>> e.code
        1000
        >>> str(e)
        '[Error] Cannot load time zone AAAAAAA'

        >>> e = CHException('Code: 432, e.displayText() = DB::Exception: Received from db-ch-node2.a1s:9000, 172.16.101.61. DB::Exception: Unknown codec family code: 0: (while reading column date): (while reading from part /var/lib/clickhouse/data/db_shard/cdr/20190107-107_0_10594_10/ from mark 4312 with max_rows_to_read = 8192).')
        >>> e.code
        432
        >>> str(e)
        '[Error] Unknown codec family code: 0: (while reading column date).'

        >>> e = CHException('''Code: 60. DB::Exception: Table test_d1mgai.rmt doesn't exist. (UNKNOWN_TABLE) (version 21.11.1.1) (from [::1]:49632) (comment: '/mnt/ch/ClickHouse/tests/queries/0_stateless/01155_old_mutation_parts_to_do.sh')''')
        >>> e.code
        60
        >>> str(e)
        "[Error] Table test_d1mgai.rmt doesn't exist. (UNKNOWN_TABLE)"

        >>> e = CHException('''Code: 40. DB::Exception: Super bad exception (while inventing error /mnt/disks/tb/...) (version 21.11.1.1)''')
        >>> e.code
        40
        >>> str(e)
        '[Error] Super bad exception'
        >>> e = CHException('''Code: 252. DB::Exception: Received from clickhouse:9000, 172.27.0.2. DB::Exception: Too many partitions for single INSERT block (more than 100). The limit is controlled by 'max_partitions_per_insert_block' setting. Large number of partitions is a common misconception. It will lead to severe negative performance impact, including slow server startup, slow INSERT queries and slow SELECT queries. Recommended total number of partitions for a table is under 1000..10000. Please note, that partitioning is not intended to speed up SELECT queries (the ENGINE_SORTING_KEY is sufficient to make range queries fast). Partitions are intended for data manipulation (DROP PARTITION, etc).''')
        >>> e.code
        252
        >>> str(e)
        '[Error] Please make sure the ENGINE_PARTITION_KEY setting is correct. Large number of partitions is a common misconception. Partitioning is not intended to speed up SELECT queries (the ENGINE_SORTING_KEY is sufficient to make range queries fast), partitions are intended for data manipulation. Contact us at support@tinybird.co for help or read this SQL tip:  https://www.tinybird.co/docs/concepts/data-sources.html#partitioning'

        >>> e = CHException('Code: 159. DB::Exception: Timeout exceeded: elapsed 10.274018039 seconds, maximum: 10. (TIMEOUT_EXCEEDED) (version 24.1.6.52 (official build))')
        >>> str(e)
        '[Error] Timeout exceeded: elapsed 10.274018039 seconds, maximum: 10 contact us at support@tinybird.co to raise limits'

        >>> e = CHException('Code: 159, e.displayText() = DB::Exception: Timeout exceeded: elapsed 2 seconds, maximum: 1')
        >>> str(e)
        '[Error] Timeout exceeded: elapsed 2 seconds, maximum: 1 contact us at support@tinybird.co to raise limits'

        >>> e = CHException('Code: 159. DB::Exception: Timeout exceeded: elapsed 12.571560466 seconds, maximum: 10: While processing (SE...')
        >>> str(e)
        '[Error] Timeout exceeded: elapsed 12.571560466 seconds, maximum: 10 contact us at support@tinybird.co to raise limits'

        """
        code = clickhouse_parse_code_error(ch_error, headers)
        err = _parse_error_err(ch_error, code)
        logging.debug(f"{ch_error}\nParsed error message: {err}")

        super().__init__(err)

        self.code = code
        self._fatal = fatal
        self.headers = headers or {}

    @property
    def fatal(self):
        return self._fatal or self.code == CHErrors.NO_REMOTE_SHARD_AVAILABLE

    @property
    def is_global_memory_limit(self):
        return self.code == CHErrors.MEMORY_LIMIT_EXCEEDED and MEMORY_LIMIT_TOTAL_EXCEEDED in str(self)

    @property
    def is_query_memory_limit(self):
        return self.code == CHErrors.MEMORY_LIMIT_EXCEEDED and MEMORY_LIMIT_FOR_QUERY_EXCEEDED in str(self)


def clickhouse_parse_code_error(err: Optional[str], headers: HTTPHeaders) -> Optional[int]:
    if headers and "X-Clickhouse-Exception-Code" in headers:
        return int(headers["X-Clickhouse-Exception-Code"])

    if err:
        code_error = re.match(r".*?[c|C]ode: (\d+)", err)
        if code_error:
            return int(code_error.groups()[0])

    return None


def _parse_error_err(err, code):
    if code is not None and err is not None:
        #  Accept DB::Exception, DB::ErrnoException and DB::ParsingException and Exception:
        try:
            original_error = err
            err = re.match(".*[DB::]+.*Exception: (.*)|.*std::exception\. Code: 1001(.*)", err, re.DOTALL)
            err_message = (
                "[Error] %s" % _parse_err_str(err, code, original_error)
                if err
                else f"[Unknown error: {code} - {get_name_from_ch_code(code)}]"
            )
        except Exception as e:
            logging.exception(f"unable to extract info for error: {e}")
            err_message = f"[Error] {err}" if err is not None else "[Unknown error]"
    else:
        err_message = f"[Error] {err}" if err is not None else "[Unknown error]"
        logging.warning(f"unable to extract info for error: {err}")

    return err_message


def _parse_err_str(err, code, original_error):
    if int(code) in CHCustomErrors.wrong_partition.codes:
        return CHCustomErrors.wrong_partition.message

    if int(code) in CHCustomErrors.needs_merge.codes and "Illegal type AggregateFunction" in original_error:
        try:
            agg_fn = AGG_FN_REGEX.findall(original_error)
            if agg_fn and len(agg_fn):
                return CHCustomErrors.needs_merge.message.format(merge_hint=f" Use '{agg_fn[0]}Merge'.")
            return CHCustomErrors.needs_merge.message.format(merge_hint="")
        except Exception:
            return CHCustomErrors.needs_merge.message.format(merge_hint="")

    if int(code) in CHCustomErrors.memory_limit.codes:
        if MEMORY_LIMIT_TOTAL_EXCEEDED in original_error:
            return f"{MEMORY_LIMIT_TOTAL_EXCEEDED}. Contact us at support@tinybird.co if the problem persists."
        elif MEMORY_LIMIT_FOR_QUERY_EXCEEDED in original_error:
            return CHCustomErrors.memory_limit.message

    if int(code) in CHCustomErrors.illegal_aggregation.codes:
        agg_problematic_function = _get_agg_problematic_function(original_error)
        if agg_problematic_function:
            return CHCustomErrors.illegal_aggregation.message.format(agg_problematic_function=agg_problematic_function)

    if int(code) in CHCustomErrors.too_many_simultaneous_queries.codes:
        return CHCustomErrors.too_many_simultaneous_queries.message

    if int(code) in CHCustomErrors.internal_clickhouse_error.codes:
        return CHCustomErrors.internal_clickhouse_error.message

    if int(code) in CHCustomErrors.unknown_secret_error.codes:
        secret_name = BACKTICKS_PATTERN.findall(original_error)
        x = secret_name[0] if secret_name and len(secret_name) else "unknown"
        return CHCustomErrors.unknown_secret_error.message.format(x=x)

    if int(code) == CHErrors.STD_EXCEPTION:
        if "statement timeout" in original_error:
            return CHCustomErrors.postgres_statement_timeout_error.message
        elif "Lost connection" in original_error:
            return CHCustomErrors.postgres_lost_connection_error.message
        elif "pqxx::insufficient_privilege" in original_error:
            return "Insufficient privilege, please check your postgres user permissions"

    err = (
        err.groups()[0]
        .replace("e.what() = DB::Exception", "")
        .replace("e.what() = DB::ErrnoException", "")
        .replace("e.what() = DB::ParsingException", "")
        .replace("e.displayText() = DB::Exception", "")
        .replace("e.displayText() = DB::ErrnoException", "")
        .replace("e.displayText() = DB::ParsingException", "")
        .replace(": While executing File )", "")
        .replace(" )", "")
        .replace("(TIMEOUT_EXCEEDED)", "")
    )

    err = re.sub(r"\(version [^\)]*\).*", "", err)  # Delete server version and anything after it
    err = re.sub(r"(: )?\(while reading from part.*?\)", "", err)  # Reading parts includes local paths
    err = re.sub(r"(: )?\(.*/mnt/disks.*?\)", "", err)  # Anything that includes /mnt/disks is leaking

    if int(code) == CHErrors.TIMEOUT_EXCEEDED:
        try:
            return f"{err.split('While')[0].rstrip(' .:')} contact us at support@tinybird.co to raise limits"
        except Exception:
            pass

    return err.strip()


def _get_agg_problematic_function(error):
    try:
        return (
            error.split("Aggregate function")[1].split("is found inside another aggregate function in query")[0].strip()
        )
    except Exception:
        return None


class CHLocalException(CHException):
    def __init__(self, ch_local_returncode, ch_local_error, query, fatal=False, headers=None):
        """
        >>> e = CHLocalException(62, 'Code: 62, e.displayText() = DB::Exception: Syntax error: failed at position 99 (line 1, col 99): h, avg(trip_distance) c from `yellow_tripdata_2017_06` group by d, h order by h asc format JSON . Expected one of: IN, alias, AND, OR, token, IS, BETWEEN, LIKE, NOT LIKE, NOT IN, GLOBAL IN, GLOBAL NOT IN, Comma, QuestionMark, AS, e.what() = DB::Exception', 'bla')
        >>> str(e.ch_error)
        '[Error] Syntax error: failed at position 99 (line 1, col 99): h, avg(trip_distance) c from `yellow_tripdata_2017_06` group by d, h order by h asc format JSON . Expected one of: IN, alias, AND, OR, token, IS, BETWEEN, LIKE, NOT LIKE, NOT IN, GLOBAL IN, GLOBAL NOT IN, Comma, QuestionMark, AS,'

        >>> e = CHLocalException(57, '(version 19.6.1.1) Code: 57, e.displayText() = DB::Exception: Table d_821dba.tracker already exists.', 'bla')
        >>> str(e.ch_error)
        '[Error] Table d_821dba.tracker already exists.'
        >>> e.ch_error.code
        57

        >>> e = CHLocalException(32, 'Code: 32, e.displayText() = DB::Exception: Attempt to read after eof: Cannot parse Int16 from String, because value is too short (version 19.13.1.1)', 'bla')
        >>> str(e.ch_error)
        '[Error] Attempt to read after eof: Cannot parse Int16 from String, because value is too short'
        >>> e.ch_error.code
        32
        >>> e = CHLocalException(None, None, None)
        >>> str(e.ch_error)
        '[Unknown error]'
        >>> e = CHLocalException(70, 'CH return code: 70', 'bla')
        >>> str(e.ch_error)
        '[Unknown error: 70 - CANNOT_CONVERT_TYPE]'
        >>> e = CHLocalException(None, 'empty response from ClickHouse server: HTTP 599: Operation timed out after 20 seconds', None)
        >>> str(e.ch_error)
        '[Error] empty response from ClickHouse server: HTTP 599: Operation timed out after 20 seconds'
        """
        error = f"Clickhouse-local failed with status code {ch_local_returncode}: {ch_local_error}\n on query: {query}"
        super().__init__(error)
        self.ch_error = CHException(str(ch_local_error) if ch_local_error else None, fatal=fatal, headers=headers)
        self.ch_local_returncode = ch_local_returncode
        self.query = query
