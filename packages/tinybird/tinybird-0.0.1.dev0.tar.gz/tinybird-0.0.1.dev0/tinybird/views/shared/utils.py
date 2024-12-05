import asyncio
import logging
import os
import urllib.parse
from dataclasses import dataclass
from typing import Any, Dict, FrozenSet, List, Optional, Tuple

import requests

import tinybird.plan_limits.copy as PlanLimitsCopy
from tinybird.ch import (
    MAX_EXECUTION_TIME,
    ch_database_exists,
    ch_describe_query,
    ch_explain_plan_query,
    ch_get_columns_from_query,
    ch_source_table_for_view,
)
from tinybird.datasource import Datasource
from tinybird.limits import get_url_file_size_checker
from tinybird.matview_checks import check_column_types_match
from tinybird.pipe import Pipe, PipeNode, PipeNodeTypes
from tinybird.sql_template import TemplateExecutionResults
from tinybird.table import drop_table
from tinybird.user import QueryNotAllowed, User, Users
from tinybird.views.utils import is_table_function_in_error


class CopyException(Exception):
    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args)
        self.status = kwargs.get("status", 500)
        self.processed_data = kwargs.get("processed_data", {})


@dataclass()
class DataSourceUtils:
    @staticmethod
    async def set_dependent_datasources_tag(
        workspace: User, view: str, target_table_id: str, engine: str, target_workspace: Optional[User] = None
    ) -> None:
        try:
            source_datasource, source_workspace = await DataSourceUtils.get_view_sources(workspace, view)

            if not source_datasource or not source_workspace:
                return

            if source_datasource.id == target_table_id:
                return

            target_workspace = target_workspace or workspace

            Users.set_dependent_datasource_tag(
                source_workspace, source_datasource.id, target_table_id, target_workspace.id, engine
            )

            cascade_views = DataSourceUtils.get_cascade_views(source_datasource, source_workspace)
            for cascade_view in cascade_views:
                await DataSourceUtils.set_dependent_datasources_tag(
                    source_workspace, cascade_view, target_table_id, engine, target_workspace
                )
        except Exception as e:
            logging.exception(
                f"Could not set dependent data sources for workspace {workspace}, view {view}, table {target_table_id}. Error: {e}"
            )

    @staticmethod
    async def update_dependent_datasources_tag(workspace: User, view: str, target_table_id: Optional[str]) -> None:
        try:
            if not target_table_id:
                return

            source_datasource, source_workspace = await DataSourceUtils.get_view_sources(workspace, view)
            if not source_datasource or not source_workspace:
                return

            if source_datasource.id == target_table_id:
                return

            Users.update_dependent_datasource_tag(source_workspace, source_datasource.id, target_table_id)

            cascade_views = DataSourceUtils.get_cascade_views(source_datasource, source_workspace)

            for cascade_view in cascade_views:
                await DataSourceUtils.update_dependent_datasources_tag(source_workspace, cascade_view, target_table_id)
        except Exception as e:
            logging.exception(
                f"Could not update dependent data sources for workspace {workspace.name}, view {view}, table {target_table_id}. Error: {e}"
            )

    @staticmethod
    async def get_view_sources(workspace: User, view: str) -> Tuple[Optional[Datasource], Optional[User]]:
        source_table = await ch_source_table_for_view(
            database_server=workspace["database_server"], database=workspace["database"], view=view
        )

        if not source_table:
            logging.warning(f"There is no source table for view {view} on database {workspace['database']}")
            return None, None

        source_datasource = Users.get_datasource(workspace, source_table.table, include_read_only=True)
        source_workspace = Users.get_source_workspace(workspace, source_datasource)
        source_datasource = Users.get_datasource(source_workspace, source_table.table)

        return source_datasource, source_workspace

    @staticmethod
    def get_cascade_views(source_datasource: Datasource, workspace: User) -> List[str]:
        cascade_views = set()

        for pipe in workspace.get_pipes():
            for node in pipe.pipeline.nodes:
                if node.materialized == source_datasource.id:
                    cascade_views.add(node.id)

        return list(cascade_views)


@dataclass()
class NodeUtils:
    @staticmethod
    async def delete_node_materialized_view(
        workspace: User, node: Optional[PipeNode] = None, cancel_fn=None, force: bool = False, hard_delete: bool = False
    ) -> Optional[PipeNode]:
        if not node:
            return None

        if node.materialized or force:
            logging.info(
                f"Trying to drop view: workspace {workspace.name} ({workspace.id}, {workspace.database}), name {node.id}"
            )
            try:
                if cancel_fn:
                    await cancel_fn()

                if hard_delete and not await ch_database_exists(workspace.database_server, workspace.database):
                    return None

                await DataSourceUtils.update_dependent_datasources_tag(
                    workspace=workspace, view=node.id, target_table_id=node.materialized
                )

                results = await drop_table(workspace, node.id)
                if results:
                    raise results[0]

            except Exception as e:
                logging.exception(f"Could not drop view {node.id}: {e}")
                raise e
        node.materialized = None
        return node

    @staticmethod
    async def validate_node_sql(
        workspace: User,
        pipe: Pipe,
        node: PipeNode,
        check_endpoint: bool = True,
        function_allow_list: Optional[FrozenSet[str]] = None,
    ) -> None:
        try:
            is_table_function = False
            template_execution_results = TemplateExecutionResults()

            secrets = workspace.get_secrets_for_template()
            _sql = node.render_sql(secrets=secrets, template_execution_results=template_execution_results)

            sql, _ = await workspace.replace_tables_async(
                query=_sql,
                pipe=pipe,
                use_pipe_nodes=True,
                template_execution_results=template_execution_results,
                check_endpoint=check_endpoint,
                release_replacements=True,
                allow_using_org_service_datasources=True,
                secrets=secrets,
            )
        except QueryNotAllowed as e:
            try:
                if is_table_function_in_error(workspace, e, function_allow_list):
                    sql, _ = await workspace.replace_tables_async(
                        query=_sql,
                        pipe=pipe,
                        use_pipe_nodes=True,
                        template_execution_results=template_execution_results,
                        check_endpoint=check_endpoint,
                        release_replacements=True,
                        allow_using_org_service_datasources=True,
                        function_allow_list=function_allow_list,
                        secrets=secrets,
                    )
                    is_table_function = True
                else:
                    raise e
            except Exception as e:
                logging.warning("Could not replace tables in query: %s" % node.sql)
                raise e
        except Exception as e:
            logging.warning("Could not replace tables in query: %s" % node.sql)
            raise e

        database_server = workspace["database_server"]
        database = workspace["database"]

        max_execution_time = (
            PlanLimitsCopy.CopyLimits.max_job_execution_time.get_limit_for(workspace)
            if node.node_type == PipeNodeTypes.COPY
            else MAX_EXECUTION_TIME
        )

        if is_table_function:
            return

        await asyncio.gather(
            ch_describe_query(
                database_server,
                database,
                sql,
                format="JSON",
                max_execution_time=max_execution_time,
                ch_params=workspace.get_secrets_ch_params_by(template_execution_results.ch_params),
            ),
            ch_explain_plan_query(
                database_server,
                database,
                sql,
                with_result=False,
                max_execution_time=max_execution_time,
                ch_params=workspace.get_secrets_ch_params_by(template_execution_results.ch_params),
            ),
        )


@dataclass()
class SQLUtils:
    @staticmethod
    async def validate_query_columns_for_schema(
        sql: str,
        datasource: Datasource,
        workspace: User,
        max_execution_time: Optional[int] = MAX_EXECUTION_TIME,
        ch_params: Optional[Dict[str, Any]] = None,
    ) -> None:
        sql_columns = await ch_get_columns_from_query(
            workspace.database_server, workspace.database, sql, max_execution_time, ch_params=ch_params
        )

        _, table_schema = await datasource.table_metadata(workspace, max_execution_time=max_execution_time)
        check_column_types_match(columns=sql_columns, schema=table_schema)


@dataclass()
class UrlUtils:
    @staticmethod
    def check_file_size_limit(
        url: str,
        workspace: User,
        file_size_limit: int,
        datasource_id: Optional[str] = None,
        is_parquet: bool = False,
    ) -> Tuple[int, bool]:
        head_available = False
        with requests.head(url, allow_redirects=False) as r:
            if r.status_code != 200:
                file_size = None
            else:
                file_size = int(r.headers["Content-Length"])
                head_available = True

        if file_size is None:
            with requests.get(
                url,
                stream=True,
                allow_redirects=False,
            ) as r:
                if r.status_code != 200:
                    raise Exception(f"Invalid URL. Status code: {r.status_code}")
                file_size = int(r.headers["Content-Length"])
        get_url_file_size_checker(file_size_limit, workspace.plan, workspace.id, datasource_id, is_parquet)(file_size)
        return (file_size, head_available)

    @staticmethod
    def get_file_extension(url: str) -> str:
        """
        >>> UrlUtils.get_file_extension("https://s3.amazonaws.com/bucket-name/file-name.txt?AWSAccessKeyId=AKIAIOSFODNN7EXAMPLE&Signature=dGVzdA%3D%3D&Expires=1500000000")
        'txt'
        >>> UrlUtils.get_file_extension("/path/to/local/file-name.txt")
        'txt'
        >>> UrlUtils.get_file_extension("https://example.com/path/to/file-name")
        ''
        >>> UrlUtils.get_file_extension("/path/to/file")
        ''
        >>> UrlUtils.get_file_extension("/path/to/local/file-name.snappy.parquet")
        'parquet'
        """

        parsed_url = urllib.parse.urlparse(url)
        path = parsed_url.path
        _, ext = os.path.splitext(path)
        return ext.lstrip(".")
