import copy
import logging
import re
from typing import Any, Dict, List, Optional, Tuple

from chtoolset import query as chquery

from tinybird.ch import CHTable, HTTPClient, ch_explain_query_json_async, ch_get_columns_from_query, partition
from tinybird.ch_utils.engine import TableDetails
from tinybird.ch_utils.exceptions import CHException
from tinybird.datasource import get_trigger_datasource
from tinybird.limits import Limit
from tinybird.matview_checks import (
    SQLValidationException,
    check_engine_partition_key,
    check_engines_match,
    check_is_valid_engine,
)
from tinybird.pipe import Pipe, PipeNode
from tinybird.protips import ProTips, ProTipsService
from tinybird.sql import schema_to_sql_columns
from tinybird.sql_template import TemplateExecutionResults
from tinybird.user import ServicesDataSourcesError, User, Users
from tinybird.views.api_errors.pipes import SQLPipeError
from tinybird.views.entities_datafiles import generate_pipe_datafile
from tinybird_shared.clickhouse.errors import CHErrors

gb_regex = re.compile("^[a-zA-Z0-9_ ,]*$")
is_wrapped_regex = re.compile("(select\s+\*\s+from\s+)\((.*)\)", re.IGNORECASE | re.DOTALL)

AFTER_GROUP_BY_STATEMENTS = ["SAMPLE", "ARRAY JOIN", "HAVING", "ORDER BY", "LIMIT", "SETTINGS", "UNION", "FORMAT"]

CODES = {
    "GROUP_BY": {
        "code": "GROUP_BY",
        "weight": 100,
    },
    "SPEED": {
        "code": "SPEED",
        "weight": 101,
    },
    "SIM": {
        "code": "SIM",
        "weight": 102,
    },
    "SIM_UNKNOWN": {
        "code": "SIM_UNKNOWN",
        "weight": 103,
    },
}


class AnalyzeException(Exception):
    pass


class LeftTableException(AnalyzeException):
    def __init__(self, error):
        self.error = error
        super().__init__(
            f"There was an error ({error}) when getting the Data Source form the query. Please, check you are using a valid Data Source"
        )


class Materialized(CHTable):
    # These limits are chosen because "reasons"

    def __init__(
        self,
        workspace: User,
        node: PipeNode,
        pipe: Pipe,
        target: Optional[str],
        default_date_partition: str = "toYYYYMM",
        populate_condition: Optional[str] = None,
    ):
        self.node = node
        self.pipe = pipe
        self.workspace = workspace
        self.target_datasource_name = target
        self.database_server = workspace.database_server
        self.database = workspace.database
        self.warnings: List[Dict[str, Any]] = []
        self.default_date_partition = default_date_partition
        self.left_table: Optional[Tuple[str, str]] = None
        self.populate_condition = populate_condition
        self.sql_populate_condition = ""

        materialize_limits = workspace.get_limits(prefix="ch")
        self.PERFORMANCE_VALIDATION_LIMIT = materialize_limits.get(
            "materialize_performance_validation_limit", Limit.materialize_performance_validation_limit
        )

        self.PERFORMANCE_VALIDATION_SECONDS = materialize_limits.get(
            "materialize_performance_validation_seconds", Limit.materialize_performance_validation_seconds
        )

        self.PERFORMANCE_VALIDATION_THREADS = materialize_limits.get(
            "materialize_performance_validation_threads", Limit.materialize_performance_validation_threads
        )

    def normalize_and_compare(self, original, rewritten):
        normalized_original = re.sub(r"\s+", " ", original).strip().lower()
        normalized_rewritten = re.sub(r"\s+", " ", rewritten).strip().lower()

        rewrites = []  # type: ignore
        if normalized_original == normalized_rewritten:
            return rewrites

        state_pattern = r"\b\w+state\b"
        states_in_original = re.findall(state_pattern, normalized_original)
        states_in_rewritten = re.findall(state_pattern, normalized_rewritten)

        # delete the -states already present in the original clause
        for match in states_in_original:
            if match in states_in_rewritten:
                states_in_rewritten.remove(match)

        for match in states_in_rewritten:
            func_pattern = re.compile(match, re.IGNORECASE)
            func_matches = func_pattern.findall(rewritten)
            for func in func_matches:
                rewrites.append(func)

        rewrites_set = set(rewrites)
        unique_list = sorted(list(rewrites_set))
        formatted_list = []
        for func in unique_list:
            original_func = func[: -len("State")]
            formatted_list.append(f"{original_func} -> {func}")

        return formatted_list

    async def analyze(self):
        try:
            self.warnings = []
            self.replaced_sql, _ = await self.workspace.replace_tables_async(
                self.node.sql,
                pipe=self.pipe,
                use_pipe_nodes=True,
                template_execution_results=TemplateExecutionResults(),
                allow_use_internal_tables=False,
                release_replacements=True,
            )

            try:
                left_table = await self.validate_query(self.replaced_sql)
            except LeftTableException as e:
                raise e
            except AnalyzeException as e:
                logging.warning(
                    f"error when validating the matview query, check the application logs for more info: {str(e)}"
                )
                logging.warning(
                    f"matview query validation => ws: {self.workspace.name} - pipe: {self.pipe.name} - node: {self.node.name} - sql: {self.replaced_sql}"
                )
                self.warnings.append(
                    {
                        "text": str(e),
                        "code": CODES["SPEED"]["code"],
                        "weight": CODES["SPEED"]["weight"],
                        "documentation": "https://www.tinybird.co/docs/publish/materialized-views#why-am-i-getting-a-ui-error-message",
                    }
                )
                try:
                    left_table = chquery.get_left_table(self.replaced_sql, default_database=self.database)
                except Exception as e:
                    raise LeftTableException(str(e))

            self.left_table = left_table

            if self.populate_condition:
                filtered_node_query = self.replaced_sql.replace(
                    f"{left_table[0]}.{left_table[1]}",
                    f"(SELECT * FROM {left_table[0]}.{left_table[1]} WHERE {self.populate_condition})",
                )
                self.sql_populate_condition, _ = await self.workspace.replace_tables_async(
                    filtered_node_query,
                    pipe=self.pipe,
                    use_pipe_nodes=True,
                    template_execution_results=TemplateExecutionResults(),
                    allow_use_internal_tables=False,
                    release_replacements=True,
                )

            columns = await ch_get_columns_from_query(self.database_server, self.database, self.replaced_sql)
            self._check_columns(columns)

            is_agg_merge_tree, self.sorting_key = await process_group_by(
                self.replaced_sql, self.database, self.database_server, left_table=left_table
            )

            if is_agg_merge_tree:
                # make sure all the agg functions have the State combinator
                # the reason is that ch_get_columns_from_query (AKA DESCRIBE) will return the proper
                # AggregateFunction(fn, type)
                # We could replace count() with sum(1) in the query to get a better aggregation too
                # but that complicates types and queries
                self.rewritten_sql = chquery.rewrite_aggregation_states(self.node.sql)

                sql, _ = await self.workspace.replace_tables_async(
                    self.rewritten_sql,
                    pipe=self.pipe,
                    use_pipe_nodes=True,
                    template_execution_results=TemplateExecutionResults(),
                    allow_use_internal_tables=False,
                    release_replacements=True,
                )

                columns = await ch_get_columns_from_query(self.database_server, self.database, sql)

                super().__init__(
                    columns=columns,
                    default_date_partition=self.default_date_partition,
                )

                try:
                    self.validate_group_by()
                except AnalyzeException as e:
                    logging.exception(
                        f"error when analyzing the group by expression for a matview, check the application logs for more info: {str(e)}"
                    )
                    logging.warning(
                        f"group by expression error => ws: {self.workspace.name} - pipe: {self.pipe.name} - node: {self.node.name} - sql: {self.replaced_sql}"
                    )
                    self.warnings.append(
                        {
                            "text": str(e),
                            "code": CODES["GROUP_BY"]["code"],
                            "weight": CODES["GROUP_BY"]["weight"],
                            "documentation": "https://tinybird.co/docs/guides/materialized-views.html",
                        }
                    )

                # add warning if sql is rewritten
                if self.rewritten_sql:
                    rewrites = self.normalize_and_compare(self.node.sql, self.rewritten_sql)
                    if len(rewrites) > 0:
                        info = "Rewritten functions: " + ", ".join(rewrites) + "."
                        self.warnings.append(
                            ProTipsService.protips[ProTips.STATE_MODIFIERS.name].to_json(
                                description_replacements={"rewrites": info}
                            )
                        )

                self.engine_name = "AggregatingMergeTree"
                partition_expr = f"PARTITION BY {self.partition_expr}" if self.partition_expr else ""
                order_by_expr = f"ORDER BY ({self.sorting_key})" if self.sorting_key else ""
                engine_settings = [self.engine_name, partition_expr, order_by_expr]
                self.engine = " ".join(engine_settings)

            else:
                sql = self.replaced_sql
                super().__init__(
                    columns=columns,
                    default_date_partition=self.default_date_partition,
                )
                self.engine_name = "MergeTree"
                self.sorting_key = ",".join(self.index_columns)
                self.rewritten_sql = self.node.sql.strip()
        except Exception as e:
            if isinstance(e, CHException):
                # TODO handle here more exceptions as they arise
                if e.code in [CHErrors.NOT_AN_AGGREGATE]:
                    raise AnalyzeException(str(e)) from e
            elif isinstance(e, ServicesDataSourcesError):
                raise e
            elif isinstance(e, ValueError):
                raise AnalyzeException(str(e)) from e
            raise e

    def validate_group_by(self):
        not_present = []
        schema_columns = [x["name"].lower() for x in self.columns]
        for gg in [x.strip() for x in self.sorting_key.split(",")]:
            if gg.lower() not in schema_columns:
                not_present.append(gg)

        hint = "This might indicate a not valid Materialized View, please make sure you aggregate and GROUP BY in the topmost query."
        if len(not_present) == 1:
            raise AnalyzeException(
                f"Column '{not_present[0]}' is present in the GROUP BY but not in the SELECT clause. {hint}"
            )
        elif len(not_present) > 1:
            raise AnalyzeException(
                f"Columns '{', '.join(not_present)}' are present in the GROUP BY but not in the SELECT clause. {hint}"
            )

    async def validate_query(self, sql: str):
        """
        In the validation we want to ensure that the ingestion won't break because of this MV.
        This has evolved quite a bit with the experience / incidents we've seen up to this point
        A bit of history of things that have been done:
        - Nothing, just push the MV as is and if CH accepts it we're ok.
        - Validate that the columns and types match (this is still done)
        - {query} LIMIT 0. This has the issue that CH wasn't (and in some times isn't) clever enough to discard subqueries
        and CTEs so it could take a lot of time to return
        - DESCRIBE {query}. Better but it doesn't cover all the issues (like invalid types into functions)
        - EXPLAIN PLAN {query}. More comprehensive than {query} but slow in some cases.

        The current proposal is to execute the SQL query over a simulated "batch" of data. This validates the query
        types and also check with (some) of the customer current values in the table. More importantly it allows us to
        assert that the performance of the MV is "adequate"
        """

        error = "UNKNOWN"
        left_table = None
        try:
            left_table = chquery.get_left_table(sql, default_database=self.database)
        except Exception as e:
            error = str(e)

        if not left_table or not left_table[0] or not left_table[1]:
            raise LeftTableException(error)
        replacements = {
            (left_table[0], left_table[1]): (
                "",
                f"( SELECT * FROM {left_table[0]}.{left_table[1]} LIMIT {self.PERFORMANCE_VALIDATION_LIMIT} )",
            )
        }
        batch_query = chquery.replace_tables(sql, replacements, default_database=self.database)
        client = HTTPClient(host=self.database_server, database=self.database)
        retry = False
        try:
            await client.query(
                batch_query,
                read_only=True,
                max_execution_time=self.PERFORMANCE_VALIDATION_SECONDS,
                max_threads=self.PERFORMANCE_VALIDATION_THREADS,
                asterisk_include_materialized_columns=True,
                asterisk_include_alias_columns=True,
            )
        except CHException as e:
            if e.code == CHErrors.TIMEOUT_EXCEEDED or e.code == CHErrors.TOO_MANY_ROWS_OR_BYTES:
                # logging exception for now although we retry with format null
                logging.warning("retry analyze with format null : " + str(e))
                batch_query += " FORMAT Null"
                retry = True
            else:
                logging.exception(f"unhandled validation error: {str(e)}")

        if retry:
            # Just in case the MV failed because it was reading data from disk (not cached), retry again
            # Maybe in the future we should instead try to get the latest ingested data or something like that
            try:
                await client.query(
                    batch_query,
                    read_only=True,
                    max_execution_time=self.PERFORMANCE_VALIDATION_SECONDS,
                    max_threads=self.PERFORMANCE_VALIDATION_THREADS,
                    asterisk_include_materialized_columns=True,
                    asterisk_include_alias_columns=True,
                )
            except CHException as e:
                if e.code == CHErrors.TIMEOUT_EXCEEDED:
                    raise AnalyzeException(
                        "The performance of this query is not compatible with realtime ingestion."
                    ) from e
                logging.exception(f"unhandled validation error: {str(e)}")

        return left_table

    def _partition(self):
        self.partition_column, self.partition_expr = partition(
            self.columns,
            default_date_partition=self.default_date_partition,
        )

    async def to_json(self, include_datafile=False, include_schema=True, include_engine_full=True):
        # FIXME: we're supporting here both 'engine' and 'type' since 'type' is being used in some engine operations
        # We should refactor this in order to unify it

        engine = {
            "partition_key": self.partition_expr,
            "sorting_key": self.sorting_key,
            "engine": self.engine_name,
            "type": self.engine_name,
        }

        if include_engine_full:
            engine["engine_full"] = self.engine

        datasource_name = self.target_datasource_name or f"mv_{self.pipe.name}_{self.node.name}"

        response = {
            "analysis": {
                "pipe": {
                    "id": self.pipe.id,
                    "name": self.pipe.name,
                },
                "node": self.node.to_json(dependencies=False, attrs=["id", "name"]),
                "datasource": {
                    "name": datasource_name,
                    "schema": self.table_structure(),
                    "engine": engine,
                    "columns": self.columns,
                },
                "partition_column": self.partition_column,
                "columns": self.columns,
                "sql": self.rewritten_sql,
                "trigger_datasource": get_trigger_datasource(self.workspace, self.left_table),
            }
        }

        if self.populate_condition:
            response["analysis"]["sql_populate_condition"] = self.sql_populate_condition

        if include_datafile:
            doc = []
            copy_pipe = copy.deepcopy(self.pipe)

            if include_schema:
                doc.append(f"# Data Source generated from Pipe '{copy_pipe.name}'")
                doc += ["", "SCHEMA >"]
                columns = schema_to_sql_columns(self.columns)
                doc.append(",\n".join(map(lambda x: f"    {x}", columns)))
                doc.append("")

            doc.append(TableDetails(engine).to_datafile(include_empty_details=True))
            datafile = "\n".join(doc)
            response["analysis"]["datasource"]["datafile"] = datafile
            index = copy_pipe.pipeline.nodes.index(self.node)
            copy_pipe.pipeline.nodes[index].sql = self.rewritten_sql
            response["analysis"]["pipe"]["datafile"] = await generate_pipe_datafile(
                copy_pipe, self.workspace, materialized_node_name=(self.node.name, datasource_name)
            )

        return {**response, **{"warnings": self.warnings}}

    async def validate(
        self,
        columns: Optional[List[Dict[str, Any]]] = None,
        engine_settings: Optional[Dict[str, Any]] = None,
        is_cli: bool = False,
        is_from_ui: bool = False,
        override_datasource: bool = False,
    ) -> List[str]:
        if override_datasource:
            return []

        workspace = self.workspace
        engine_settings = engine_settings if engine_settings else {}
        datasource = Users.get_datasource(workspace, self.target_datasource_name)

        # this is legit, target data source might not exist
        if not datasource:
            return []

        sql_replaced, _ = await self.workspace.replace_tables_async(
            self.node.sql,
            pipe=self.pipe,
            use_pipe_nodes=True,
            template_execution_results=TemplateExecutionResults(),
            allow_use_internal_tables=False,
            release_replacements=True,
        )

        if not columns:
            columns = await ch_get_columns_from_query(workspace.database_server, workspace.database, sql_replaced)

        table_details, schema = await datasource.table_metadata(workspace)
        query_lines = chquery.format(sql_replaced).splitlines()
        errors = []

        try:
            try:
                left_table = chquery.get_left_table(sql_replaced, default_database=self.database)
            except Exception as e:
                raise LeftTableException(str(e))

            check_group_by, group_by_columns = await process_group_by(
                sql_replaced, self.database, self.database_server, left_table=left_table, skip_on_multiple_group_by=True
            )
            check_is_valid_engine(
                sql_replaced,
                table_details,
                query_lines,
                columns,
                schema,
                group_by_columns,
                check_group_by=check_group_by,
                is_cli=is_cli,
                is_from_ui=is_from_ui,
            )
        except SQLValidationException as e:
            errors.append(f"{str(e)}. {SQLPipeError.override_datasource_msg(is_from_ui=is_from_ui, is_cli=is_cli)}")
        try:
            check_engines_match(engine_settings, table_details, datasource, is_cli=is_cli, is_from_ui=is_from_ui)
        except SQLValidationException as e:
            errors.append(f"{str(e)}. {SQLPipeError.override_datasource_msg(is_from_ui=is_from_ui, is_cli=is_cli)}")
        try:
            await check_engine_partition_key(
                self.database_server, self.database, engine_settings, left_table, sql_replaced
            )
        except SQLValidationException as e:
            errors.append(f"{str(e)}. {SQLPipeError.override_datasource_msg(is_from_ui=is_from_ui, is_cli=is_cli)}")
        if workspace.is_branch and workspace.origin:
            main_workspace = Users.get_by_id(workspace.origin)
            if main_workspace.database == left_table[0]:
                errors.append("Materialization from 'main' is forbidden.")
        return errors


def _try_get_wrapped_sql(sql: str) -> str:
    """
    Given a SQL query, tries to identify if it contains a subquery wrapped in parentheses. If such a subquery is found,
    returns the subquery. Otherwise, returns the original SQL query.

    >>> _try_get_wrapped_sql('SELECT * FROM table')
    'SELECT * FROM table'
    >>> _try_get_wrapped_sql('(  SELECT * FROM table  )')
    '(  SELECT * FROM table  )'
    >>> _try_get_wrapped_sql('SELECT * FROM table WHERE id > 1')
    'SELECT * FROM table WHERE id > 1'
    >>> _try_get_wrapped_sql("SELECT * FROM (SELECT id, name FROM p.m)")
    'SELECT id, name FROM p.m'
    >>> _try_get_wrapped_sql("SELECT * FROM (SELECT id, name FROM p.m) WHERE id > 1000")
    'SELECT id, name FROM p.m'
    >>> _try_get_wrapped_sql("SELECT * FROM (SELECT name, count() count FROM p.m GROUP BY city) WHERE (count > 1000)")
    'SELECT * FROM (SELECT name, count() count FROM p.m GROUP BY city) WHERE (count > 1000)'
    >>> _try_get_wrapped_sql("SELECT * FROM (SELECT * FROM ( SELECT * FROM ( SELECT * FROM test_table) AS node) AS e) AS node_1")
    'SELECT * FROM ( SELECT * FROM ( SELECT * FROM test_table) AS node) AS e'
    >>> _try_get_wrapped_sql("SELECT (SELECT 1 FROM b) FROM a")
    'SELECT (SELECT 1 FROM b) FROM a'
    >>> _try_get_wrapped_sql("SELECT (SELECT 1 FROM b) FROM a AS node_1")
    'SELECT (SELECT 1 FROM b) FROM a AS node_1'
    >>> _try_get_wrapped_sql("SELECT (SELECT 1 FROM b) FROM a AS node_1 WHERE hola = a")
    'SELECT (SELECT 1 FROM b) FROM a AS node_1 WHERE hola = a'
    >>> _try_get_wrapped_sql("no valid sql")
    'no valid sql'
    """
    is_wrapped = is_wrapped_regex.match(sql)
    if is_wrapped and len(is_wrapped.groups()) == 2:
        wrapped_query = is_wrapped.groups()[1]

        try:
            chquery.format(wrapped_query)
            return wrapped_query
        except ValueError:
            return sql

    return sql


def check_join(plans: List[Dict[str, Any]]) -> bool:
    is_join = False

    try:
        if len(plans) == 1 and plans[0]["Plan"]["Plans"][0]["Node Type"] == "Aggregating":
            return False
    except Exception:
        pass

    for p in plans:
        if p.get("Node Type") == "Join":
            return True

        plan = p.get("Plan", {})
        if plan.get("Node Type") == "Join":
            return True

        is_join = check_join(p.get("Plans", []))
        if is_join:
            return True

        is_join = check_join(plan.get("Plans", []))
        if is_join:
            return True

    return is_join


def check_group_by(plan: Dict[str, Any], left_table, is_left_table_present: bool = False):
    left_table_check = False

    plans = plan.get("Plans", [])
    if not is_left_table_present:
        is_left_table_present = plan.get("Description") == left_table

    if plans:
        for p in plans:
            if not is_left_table_present:
                is_left_table_present = p.get("Description") == left_table
            plan = p.get("Plan", {})

            if plan:
                if not is_left_table_present:
                    is_left_table_present = plan.get("Description") == left_table
                if "Before GROUP BY" in plan.get("Description", ""):
                    left_table_check = check_left_table(plan, left_table, is_left_table_present)
                    if left_table_check:
                        return True

                return check_group_by(plan, left_table)
            else:
                if "Before GROUP BY" in p.get("Description", ""):
                    left_table_check = check_left_table(p, left_table, is_left_table_present)
                    if left_table_check:
                        return True
                return check_group_by(p, left_table, is_left_table_present)

    if "Before GROUP BY" in plan.get("Description", ""):
        left_table_check = check_left_table(plan, left_table, is_left_table_present)

    return left_table_check


def check_is_left_table(plan: Dict[str, Any], left_table, is_left_table_present: bool = False):
    is_left_table = plan.get("Description") == left_table or (
        not is_left_table_present and plan.get("Description") == "Read from NullSource"
    )

    if is_left_table:
        return True


def check_left_table(plan, left_table, is_left_table_present=False):
    is_left_table = check_is_left_table(plan, left_table, is_left_table_present)

    if is_left_table:
        return True

    plans = plan.get("Plans", [])

    for p in plans:
        is_left_table = check_is_left_table(p, left_table, is_left_table_present)
        if is_left_table:
            return True

        inner_plan = p.get("Plan", {})

        if inner_plan:
            is_left_table = check_is_left_table(inner_plan, left_table, is_left_table_present)
        else:
            is_left_table = check_left_table(p, left_table, is_left_table_present)

        if is_left_table:
            return True

        return check_left_table(p, left_table, is_left_table_present)
    return is_left_table


async def process_group_by(
    sql: str,
    database: str,
    database_server: str,
    left_table: Optional[Tuple[str, str]],
    skip_on_multiple_group_by: bool = False,
):
    """
    >>> import asyncio
    >>> asyncio.run(process_group_by('SELECT 1', 'database', 'database_server', left_table=None))
    (False, None)
    >>> asyncio.run(process_group_by('SELECT count() number, date FROM database.table GROUP BY date', 'database', 'database_server', left_table=('database', 'table')))
    (True, 'date')
    >>> asyncio.run(process_group_by('SELECT count() number, date FROM database.table GROUP BY date ORDER BY number', 'database', 'database_server', left_table=('database', 'table')))
    (True, 'date')
    >>> asyncio.run(process_group_by('SELECT count() n, date as year FROM (SELECT count() number, date FROM database.table GROUP BY date) GROUP BY year', 'database', 'database_server', left_table=('database', 'table')))
    (True, 'date')
    >>> asyncio.run(process_group_by('SELECT count() n, date as year FROM (SELECT count() number, date FROM database.table GROUP BY date ORDER BY number) GROUP BY year ORDER BY n', 'database', 'database_server', left_table=('database', 'table')))
    (True, 'date')
    >>> asyncio.run(process_group_by('SELECT count() n, date as year, whatever as something_else FROM (SELECT count() number, date, whatever FROM database.table GROUP BY date, whatever ORDER BY number) GROUP BY year, something_else ORDER BY n', 'database', 'database_server', left_table=('database', 'table')))
    (True, 'date,whatever')
    >>> asyncio.run(process_group_by('SELECT count() n, date as year FROM database.table a INNER JOIN (SELECT count() number, date as year FROM database.table) b on a.date = b.year GROUP BY date ORDER BY n', 'database', 'database_server', left_table=('database', 'table')))
    (True, 'date')
    """

    sql = _try_get_wrapped_sql(sql)
    explain: List[Dict[str, Any]] = []

    try:
        explain = await ch_explain_query_json_async(database, database_server, sql)
    except Exception:
        pass

    # FIXME: use it on CH 22
    # if left_table and explain:
    #     is_left_table = check_plans(explain, f'{left_table[0]}.{left_table[1]}')

    #     if not is_left_table:
    #         return False, None

    if check_join(explain):
        return False, None

    query_lines = chquery.format(sql).splitlines()

    if skip_on_multiple_group_by:
        group_by_statements = [line for line in query_lines if "group by" in line.lower()]
        if len(group_by_statements) > 1:
            return False, None

    is_agg, columns = _process_group_by(query_lines=query_lines, left_table=left_table)
    return is_agg, columns


def _process_group_by(query_lines: List[str], left_table: Optional[Tuple[str, str]]) -> Tuple[bool, Optional[str]]:
    """
    >>> _process_group_by(['SELECT', '1'], left_table=None)
    (False, None)
    >>> _process_group_by(['FROM database.table', 'GROUP BY', '    number,', '    date'], left_table=('database', 'table'))
    (True, 'number,date')
    >>> _process_group_by(['FROM database.table', 'GROUP BY', '    number,', '    date', ') AS d ON number = d.number'], left_table=('database', 'table'))
    (True, 'number,date')
    >>> _process_group_by(['SELECT', '    count() AS c,', '    number', 'FROM database.table', 'GROUP BY number'], left_table=('database', 'table'))
    (True, 'number')
    >>> _process_group_by([ 'SELECT', '    toStartOfDay(date) AS day,', '    id,', '    data,', '    count() AS c', 'FROM database.table', 'GROUP BY', '    day,', '    id,', '    data', 'ORDER BY c DESC', 'LIMIT 10'], left_table=('database', 'table'))
    (True, 'day,id,data')
    >>> _process_group_by([ 'SELECT', '    toStartOfDay(date) AS day,', '    id,', '    data,', '    count() AS c', 'FROM database.table', 'GROUP BY', '    day,', '    id,', '    data', 'ORDER BY c desc, id asc', 'LIMIT 10'], left_table=('database', 'table'))
    (True, 'day,id,data')
    >>> _process_group_by([') AS d ON a.number = d.number', '    GROUP BY number', '    FROM database.table', '        number', '        count() AS c,', '    SELECT', '(', 'INNER JOIN', 'FROM database.table AS a', 'SELECT *'], left_table=('database', 'table'))
    (False, None)
    >>> _process_group_by(['SELECT', '    toStartOfMinute(photo_submitted_at) AS d,', '    exif_camera_model AS e,', '    count() AS c', 'FROM database.table', 'GROUP BY', '    d,', '    e', 'ORDER BY', '    d DESC,', '    e ASC'], left_table=('database', 'table'))
    (True, 'd,e')
    >>> _process_group_by(['SELECT', '    Country,', '    count() AS c', 'FROM database.table', 'GROUP BY Country'], left_table=('database', 'table'))
    (True, 'Country')
    >>> _process_group_by(['SELECT * FROM database.table', 'GROUP BY Country'], left_table=('database', 'table'))
    (True, 'Country')
    >>> _process_group_by(['SELECT', '    column_1,', '    column_2', 'FROM', '(', '    SELECT', '        column_1,', '        column_2,', '        sumState(1) AS whatever', '    FROM database.table', '    GROUP BY', '        column_1,', '        column_2', '    ORDER BY', '        column_1 ASC,', '        column_2 ASC', ') AS a', 'WHERE whatever = 1'], left_table=('database', 'table'))
    (True, 'column_1,column_2')
    >>> _process_group_by(['SELECT', '    count() AS c,', '    number', 'FROM database.table', 'LEFT JOIN', '(', '    SELECT toInt32(number) AS number', '    FROM numbers(100)', ') USING (number)', 'GROUP BY number'], left_table=('database', 'table'))
    (True, 'number')
    >>> _process_group_by(['(SELECT * FROM database.table', ') AS x', 'ANY LEFT JOIN database.other_table AS u ON (toDate(x.date) = u.date)', 'GROUP BY', '    number,', '    date'], left_table=('database', 'table'))
    (True, 'number,date')
    >>> _process_group_by(['SELECT', '    column0,', '    column1,', '    column2,', 'FROM', '(', '    SELECT', '        column0,', '        column1,', '        (arrayJoin(auxiliary_table) AS t).1 AS column2,', '        t.2 AS column3', '    FROM database.leftable', ') AS x', 'ANY LEFT JOIN database.anothertable AS cUSD ON (toDate(x.column0) = cUSD.date)', 'GROUP BY', '    column0,', '    column1,', '    column2'], left_table=('database', 'leftable', ''))
    (True, 'column0,column1,column2')
    >>> _process_group_by(['SELECT', '    column0,', '    column1,', '    column2,', 'FROM', '(', '    SELECT', '        column0,', '        column1,', '        (arrayJoin(auxiliary_table) AS t).1 AS column2,', '        t.2 AS column3', '    FROM database.leftable', ') AS x', 'ANY LEFT JOIN database.anothertable AS cUSD ON (toDate(x.column0) = cUSD.date)', 'GROUP BY', '    column0,', '    column1,', '    column2'], left_table=('database', 'leftable', ''))
    (True, 'column0,column1,column2')
    >>> _process_group_by(['SELECT', '    column0,', '    column1,', '    column2,', 'FROM', '(', '    SELECT', '        column0,', '        column1,', '        t.1 AS column2,', '        t.2 AS column3', '    FROM database.leftable as u', 'ARRAY JOIN auxiliary_table as t', ') AS x', 'ANY LEFT JOIN database.anothertable AS cUSD ON (toDate(x.column0) = cUSD.date)', 'GROUP BY', '    column0,', '    column1,', '    column2'], left_table=('database', 'leftable', ''))
    (True, 'column0,column1,column2')
    >>> _process_group_by(['SELECT', '    toDate(timestamp) AS date,', '    device,', '    browser,', '    location,', '    pathname,', '    uniqState(session_id) AS visits,', '    countState() AS hits', 'FROM', '(', '    SELECT', '        *', '        FROM d_743e5d.t_75633b8305044b0f8a4857fdad01c753 AS analytics_events', '        WHERE action = "page_hit"', '    ) AS parsed_hits', 'WHERE 1 = 1',  'GROUP BY', '    date,', '    device,', '    browser,', '    location,', '    pathname'], left_table=('d_743e5d', 't_75633b8305044b0f8a4857fdad01c753', ''))
    (True, 'date,device,browser,location,pathname')
    """

    if not left_table:
        return False, None

    def _process_inner(lines: List[str]):
        try:
            regex = re.compile(f".*from `?{left_table[0]}`?.`?{left_table[1]}`?")
            query_lines_reversed = lines[::-1]
            if (
                "group by" in query_lines_reversed[0].lower()
                and len([c for c in query_lines_reversed if " join" in c.lower()]) == 1
            ):
                sorting_key = query_lines_reversed[0].replace("GROUP BY", "").replace(" ", "").strip()
                if sorting_key:
                    return True, sorting_key

            left_table_indices = [i for i, line in enumerate(query_lines_reversed) if regex.match(line.lower())]

            for left_table_index in left_table_indices:
                lines_list = query_lines_reversed[:left_table_index][::-1]

                for i, line in enumerate(list(lines_list)):
                    if "from " in line.lower():
                        break  # TODO check:

                    if "group by" in line.lower():
                        group_by = line
                        columns = group_by.replace("GROUP BY", "").replace(" ", "").strip()
                        if columns != "":
                            return True, columns

                        lines_column_list = lines_list[i:]
                        group_by_list = []

                        for column in list(lines_column_list):
                            present_after_group_by_statemnts = [
                                statement for statement in AFTER_GROUP_BY_STATEMENTS if statement in column.strip()
                            ]
                            if len(present_after_group_by_statemnts) > 0:
                                break

                            if "GROUP BY" not in column and not column.startswith(" "):
                                continue

                            if "GROUP BY" == column.strip():
                                continue

                            group_by_list.append(column.replace("GROUP BY", "").replace(",", ""))

                        sorting_key = ",".join([part.replace(" ", "").strip() for part in group_by_list])
                        if sorting_key != "" and gb_regex.fullmatch(sorting_key):
                            return True, sorting_key
        except Exception as e:
            logging.exception(
                f"Error while processing GROUP BY in materialized view {str(e)} - query: {query_lines} - left_table: {left_table}"
            )
        return False, None

    return _process_inner(query_lines)


def get_agg(c: Dict[str, Any]) -> str:
    """
    >>> get_agg({'name': 'test', 'type': 'Int32'})
    'test'
    >>> get_agg({'name': 'test', 'type': 'AggregateFunction(avg, Int32)'})
    'avgMerge(test) as test'
    >>> get_agg({'name': 'test', 'type': 'SimpleAggregateFunction(sum, UInt64)'})
    'sum(test) as test'
    >>> get_agg({'name': 'test', 'type': 'AggregateFunction(topK(10), Int32)'})
    'topKMerge(10)(test) as test'
    >>> get_agg({'name': 'test', 'type': 'AggregateFunction(topKWeighted(2), DateTime, UInt64)'})
    'topKWeightedMerge(2)(test) as test'
    """
    if "AggregateFunction" not in c["type"]:
        return c["name"]

    fn = c["type"].split(",")[0].replace("SimpleAggregateFunction(", "").replace("AggregateFunction(", "")
    if ")" in fn and "(" not in fn:
        fn = fn.replace(")", "")

    if "SimpleAggregateFunction" in c["type"]:
        return f"{fn}({c['name']}) as {c['name']}"
    else:
        if "(" in fn:
            parts = fn.split("(")
            fn = f"{parts[0]}Merge({''.join(parts[1:])}"
        else:
            fn = f"{fn}Merge"
        return f"{fn}({c['name']}) as {c['name']}"
