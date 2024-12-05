import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, cast

from chtoolset import query as chquery

from tinybird.ch import (
    ch_explain_estimate_async,
    ch_explain_query_json_async,
    ch_get_columns_from_query,
    ch_table_details,
)
from tinybird.pipe import Pipe
from tinybird.sql_template import TemplateExecutionResults
from tinybird.user import User

PRO_TIPS_DOCUMENTATION_URL = "https://www.tinybird.co/docs"


# Note: these values have to match with the section titles from
# the documentation tips
class ProTips(Enum):
    FULL_SCAN_SORTING_KEY = "avoiding-full-scans"
    FULL_SCAN_FILTER = "avoiding-full-scans#"
    HUGE_JOIN = "avoiding-big-joins"
    AGG = "why-use-materialized-views"
    MULTIPLE_JOIN = "avoiding-big-joins#"
    SINGLE_JOIN = "avoiding-big-joins##"
    AGG_FUNCTIONS = "merging-aggregate-functions"
    STATE_MODIFIERS = "what-should-i-use-materialized-views-for"
    ENGINE_REPLACING_MERGE_TREE = "use-a-replacingmergetree-engine"


class ProTipsGroups(Enum):
    QUERY = "guides/best-practices-for-faster-sql"
    DATA_SOURCE = "concepts/data-sources"
    MATVIEW = "guides/materialized-views"
    MATVIEW_STATE_MODIFIER = "concepts/materialized-views"
    ENGINE_REPLACING_MERGE_TREE = "guides/querying-data/deduplication-strategies"


def get_merge_agg(column_type: str, column_name: str) -> Optional[str]:
    """
    >>> get_merge_agg('AggregateFunction(count)', 'c')
    'c => countMerge(c) as c'
    >>> get_merge_agg('AggregateFunction(topK(10), Int64)', 't')
    't => topKMerge(10)(t) as t'
    """

    parameters_in_function_regex = r"\(([^)]+)\)"
    agg_function_parameters = re.findall(parameters_in_function_regex, column_type)

    params = agg_function_parameters[0].split(",") if len(agg_function_parameters) else []

    if len(params):
        agg_function = params[0].strip()
        if "(" in agg_function:
            return f"{column_name} => {params[0].strip().replace('(', 'Merge(')})({column_name}) as {column_name}"
        return f"{column_name} => {params[0].strip()}Merge({column_name}) as {column_name}"
    return None


def has_table_with_engine(engine: str, workspace: User, tables: List[Any]) -> bool:
    for item in tables:
        _, table_id, _ = item

        if table_id:
            result = ch_table_details(
                table_name=table_id,
                database_server=workspace.database_server,
                database=workspace.database,
            )

            if result.engine == engine:
                return True
    return False


@dataclass()
class ProTip:
    code: str
    link: str
    description: str
    weight: int
    materialized: bool = False
    description_info: Optional[str] = None
    group: Optional[str] = None

    @property
    def documentation(self) -> str:
        return f'{PRO_TIPS_DOCUMENTATION_URL}/{self.group}.html#{self.link.replace("#", "")}' if self.group else ""

    def to_json(self, description_replacements: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        return {
            "code": self.code,
            "text": (
                self.description
                if not description_replacements or not self.description_info
                else f"{self.description} {self.description_info.format(**description_replacements)}"
            ),
            "documentation": self.documentation,
            "weight": self.weight,
            "materialized": self.materialized,
        }


class ProTipsService:
    protips: Dict[str, ProTip] = {
        ProTips.FULL_SCAN_SORTING_KEY.name: ProTip(
            code=ProTips.FULL_SCAN_SORTING_KEY.name,
            link=ProTips.FULL_SCAN_SORTING_KEY.value,
            description="This query is reading all the data in the Data Source (full scan). You can improve performance by filtering by any column present in the ENGINE_SORTING_KEY in the WHERE clause.",
            description_info="Columns present in the ENGINE_SORTING_KEY: {sorting_key}",
            weight=100,
            group=ProTipsGroups.QUERY.value,
        ),
        ProTips.FULL_SCAN_FILTER.name: ProTip(
            code=ProTips.FULL_SCAN_FILTER.name,
            link=ProTips.FULL_SCAN_FILTER.value,
            description="This query is reading all the data in the Data Source (full scan), the statements used in the WHERE clause are not filtering any data. You can improve performance by changing the filter in the WHERE clause.",
            description_info=None,
            weight=200,
            group=ProTipsGroups.QUERY.value,
        ),
        ProTips.AGG.name: ProTip(
            code=ProTips.AGG.name,
            link=ProTips.AGG.value,
            description="This query is doing an aggregation. You can improve performance by creating a Materialized View.",
            description_info=None,
            weight=300,
            group=ProTipsGroups.MATVIEW.value,
        ),
        ProTips.HUGE_JOIN.name: ProTip(
            code=ProTips.HUGE_JOIN.name,
            link=ProTips.HUGE_JOIN.value,
            description="This query is doing a JOIN that needs to process more than 1M rows. You can improve performance by narrowing the number of rows in the JOINED Data Source.",
            description_info=None,
            weight=100,
            group=ProTipsGroups.QUERY.value,
            materialized=True,
        ),
        ProTips.MULTIPLE_JOIN.name: ProTip(
            code=ProTips.MULTIPLE_JOIN.name,
            link=ProTips.MULTIPLE_JOIN.value,
            description="This query is doing multiple JOINs. Make sure they don't process unnecessary data.",
            description_info=None,
            weight=200,
            group=ProTipsGroups.QUERY.value,
            materialized=True,
        ),
        ProTips.SINGLE_JOIN.name: ProTip(
            code=ProTips.SINGLE_JOIN.name,
            link=ProTips.SINGLE_JOIN.value,
            description="This query is doing a JOIN. Make sure it does not process unnecessary data.",
            description_info=None,
            weight=300,
            group=ProTipsGroups.QUERY.value,
            materialized=True,
        ),
        ProTips.AGG_FUNCTIONS.name: ProTip(
            code=ProTips.AGG_FUNCTIONS.name,
            link=ProTips.AGG_FUNCTIONS.value,
            description="Some columns need to be aggregated by using the -Merge suffix. Make sure you do this as late in the pipeline as possible for better performance:",
            description_info="{columns}",
            weight=100,
            group=ProTipsGroups.QUERY.value,
        ),
        ProTips.STATE_MODIFIERS.name: ProTip(
            code=ProTips.STATE_MODIFIERS.name,
            link=ProTips.STATE_MODIFIERS.value,
            description="The query will be rewritten adding the -State modifier for the Materialized View to work properly.",
            description_info="{rewrites}",
            weight=100,
            group=ProTipsGroups.MATVIEW_STATE_MODIFIER.value,
            materialized=True,
        ),
        ProTips.ENGINE_REPLACING_MERGE_TREE.name: ProTip(
            code=ProTips.ENGINE_REPLACING_MERGE_TREE.name,
            link=ProTips.ENGINE_REPLACING_MERGE_TREE.value,
            description="Not seeing the expected results? This query uses a Data Source with the ReplacingMergeTree engine, which may cause some duplicated data due to how it processes and merges records. To get the latest data, try adding FINAL to your query.",
            weight=300,
            group=ProTipsGroups.ENGINE_REPLACING_MERGE_TREE.value,
        ),
    }

    @classmethod
    def iterate_plans(
        cls,
        plans: List[Dict[str, Any]],
        hints: List[Dict[str, str]],
        warnings: List[Dict[str, str]],
        joins: List[Dict[str, str]],
        workspace: User,
        query_sql: str,
        sorting_key: Optional[str] = None,
        joined_action: bool = False,
    ) -> None:
        DEFAULT_GRANULARITY = 8192
        MIN_THRESHOLD = 1000000
        for plan in plans:
            PLAN_NODE_TYPE = plan.get("Node Type", "")
            PLAN_DESCRIPTION = plan.get("Description", "")
            subplan_joined_action = joined_action

            if PLAN_NODE_TYPE == "Join" and "JOIN" in PLAN_DESCRIPTION:
                joins.append(cls.protips[ProTips.MULTIPLE_JOIN.name].to_json())
                subplan_joined_action = True
            elif PLAN_NODE_TYPE == "Aggregating":
                hints.append(cls.protips[ProTips.AGG.name].to_json())

            if "Plans" in plan:
                cls.iterate_plans(
                    plan["Plans"],
                    hints,
                    warnings,
                    joins,
                    workspace,
                    query_sql,
                    sorting_key,
                    joined_action=subplan_joined_action,
                )
                continue

            if "MergeTree" in PLAN_NODE_TYPE:
                PLAN_INDEXES: List[Dict[str, Any]] = plan.get("Indexes", [])

                if not PLAN_INDEXES:
                    sorting_key = (
                        sorting_key if sorting_key else cls.get_sorting_key(workspace=workspace, query_sql=query_sql)
                    )
                    description_replacements = {"sorting_key": sorting_key} if sorting_key else None
                    hints.append(
                        cls.protips[ProTips.FULL_SCAN_SORTING_KEY.name].to_json(
                            description_replacements=description_replacements
                        )
                    )
                else:
                    full_scan_2_counter = 0
                    full_scan_counter = 0

                    for index in PLAN_INDEXES:
                        if "Keys" not in index and index.get("Condition", "true") == "true":
                            if not subplan_joined_action:
                                full_scan_counter += 1
                                continue
                            if subplan_joined_action and index["Selected Granules"] > (
                                MIN_THRESHOLD / DEFAULT_GRANULARITY
                            ):
                                warnings.append(cls.protips[ProTips.HUGE_JOIN.name].to_json())
                        else:
                            if (
                                index["Initial Granules"] == index["Selected Granules"]
                                and index["Initial Granules"] != 0
                                and index["Selected Granules"] > (MIN_THRESHOLD / DEFAULT_GRANULARITY)
                            ):
                                if subplan_joined_action:
                                    warnings.append(cls.protips[ProTips.HUGE_JOIN.name].to_json())
                                else:
                                    full_scan_2_counter += 1

                    if full_scan_2_counter > 0 and full_scan_2_counter == len(PLAN_INDEXES):
                        hints.append(cls.protips[ProTips.FULL_SCAN_FILTER.name].to_json())

                    if full_scan_counter > 0 and full_scan_counter == len(PLAN_INDEXES):
                        sorting_key = (
                            sorting_key
                            if sorting_key
                            else cls.get_sorting_key(workspace=workspace, query_sql=query_sql)
                        )
                        description_replacements = {"sorting_key": sorting_key} if sorting_key else None
                        hints.append(
                            cls.protips[ProTips.FULL_SCAN_SORTING_KEY.name].to_json(
                                description_replacements=description_replacements
                            )
                        )

    @classmethod
    def get_sorting_key(cls, workspace: User, query_sql: str) -> Optional[str]:
        try:
            table = chquery.get_left_table(query_sql, default_database=workspace.database)
        except Exception:
            return None

        if not table:
            return None

        datasource = workspace.get_datasource(table[1])
        if not datasource:
            return None

        sorting_key = datasource.engine.get("sorting_key", None)
        if sorting_key == "tuple()":
            return None

        return sorting_key

    @classmethod
    async def get_agg_columns(cls, workspace: User, query_sql: str) -> List[str]:
        columns = await ch_get_columns_from_query(workspace.database_server, workspace.database, query_sql)

        agg_columns = [column for column in columns if column.get("type", "").startswith("AggregateFunction")]
        merge_agg_columns = [
            get_merge_agg(cast(str, column.get("type")), cast(str, column.get("name"))) for column in agg_columns
        ]
        result = [column for column in merge_agg_columns if column is not None]

        return result

    @classmethod
    async def get_tips(
        cls,
        workspace: User,
        pipe: Pipe,
        sql: str,
        materializing: bool = False,
        template_execution_results: Optional[TemplateExecutionResults] = None,
    ) -> Dict[str, List[Dict[str, str]]]:
        hints: List[Dict[str, str]] = []
        warnings: List[Dict[str, str]] = []
        joins: List[Dict[str, str]] = []

        if template_execution_results is None:
            template_execution_results = TemplateExecutionResults()

        query_sql, used_tables = await workspace.replace_tables_async(
            sql,
            pipe=pipe,
            use_pipe_nodes=True,
            template_execution_results=template_execution_results,
            release_replacements=True,
            allow_using_org_service_datasources=True,
        )

        has_replacing_merge_tree = has_table_with_engine(
            engine="ReplacingMergeTree", workspace=workspace, tables=used_tables
        )

        if has_replacing_merge_tree and "FINAL" not in query_sql:
            hints.append(cls.protips[ProTips.ENGINE_REPLACING_MERGE_TREE.name].to_json())

        agg_columns = await cls.get_agg_columns(workspace, query_sql)

        if len(agg_columns):
            description_replacements = {"columns": ", ".join(agg_columns)}
            warnings.append(
                cls.protips.get(ProTips.AGG_FUNCTIONS.name).to_json(description_replacements=description_replacements)  # type: ignore
            )

        ch_params = workspace.get_secrets_ch_params_by(template_execution_results.ch_params)
        explain_result = await ch_explain_query_json_async(
            database_server=workspace["database_server"],
            database=workspace["database"],
            sql=query_sql,
            explain_type="json=1, indexes=1",
            ch_params=ch_params,
        )

        estimate_result = await ch_explain_estimate_async(
            database_server=workspace["database_server"],
            database=workspace["database"],
            sql=query_sql,
            ch_params=ch_params,
        )

        datasources = []

        if estimate_result and estimate_result.get("data"):
            datasources = [
                {"id": result.get("table"), "rows": result.get("rows", 0)} for result in estimate_result.get("data", [])
            ]

        for elem in explain_result:
            if "Plan" in elem:
                plans = elem["Plan"].get("Plans", [])
                cls.iterate_plans(plans, hints, warnings, joins, workspace, query_sql)

        if len(joins) > 1:
            warnings.append(joins[0])
        elif len(joins) == 1:
            warnings.append(cls.protips.get(ProTips.SINGLE_JOIN.name).to_json())  # type: ignore

        hints.sort(key=lambda x: x.get("weight", 0))
        warnings.sort(key=lambda x: x.get("weight", 0))

        warnings = list({frozenset(item.items()): item for item in warnings}.values())

        def filter_materialized(x):
            return True if not materializing else x.get("materialized", False)

        return {
            "hints": list(filter(filter_materialized, hints)),
            "warnings": list(filter(filter_materialized, warnings)),
            "datasources": list(filter(filter_materialized, datasources)),
        }
