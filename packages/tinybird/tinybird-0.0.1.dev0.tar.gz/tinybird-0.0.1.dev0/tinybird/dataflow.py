import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import ulid
from toposort import toposort

from tinybird.ch import (
    MAX_EXECUTION_TIME,
    ch_get_columns_from_query_sync,
    ch_table_dependent_views_sync,
    ch_table_details,
)
from tinybird.ch_utils.engine import TableDetails
from tinybird.ch_utils.exceptions import CHException
from tinybird.copy_pipes.errors import CopyJobErrorMessages
from tinybird.datasource import Datasource
from tinybird.matview_checks import origin_column_type_is_compatible_with_destination_type
from tinybird.pipe import Pipe, PipeNode, PipeTypes
from tinybird.user import User, Users
from tinybird.views.shared.utils import CopyException
from tinybird_shared.clickhouse.errors import CHErrors


@dataclass
class DataFlowNode:
    pipe: Pipe
    node: PipeNode  # support multiple MV nodes.
    sql: Optional[str]
    datasource_id: str
    source_has_been_processed: bool


@dataclass
class DataSourceFlowNode:
    workspace: User
    datasource: Datasource


@dataclass
class DataSourceFlowNodeSimple:
    workspace_id: str
    datasource_id: str


@dataclass
class DataFlowStep:
    step_id: str
    step_datasource: Datasource
    step_workspace: User
    step_materialized_views: Optional[List[DataFlowNode]]
    step_copy: Optional[DataFlowNode]
    step_query_id: Optional[str]


class DependentTableException(Exception):
    def __init__(self, pipe_name: str, node_name: str, node_id: str, node_materialized: str) -> None:
        super().__init__(
            f"Could not find the dependent table to populate: [{pipe_name}]:{node_name}[{node_id}] points to {node_materialized} but it does not exist"
        )


class DependentViewException(Exception):
    def __init__(self, dependent_view_name: str) -> None:
        super().__init__(f"Could not find query to populate depending view: {dependent_view_name}")


def get_partition_key_type(database_server: str, table_details: TableDetails) -> str:
    describe = ch_get_columns_from_query_sync(
        database_server,
        table_details.database,
        f"""
        SELECT {table_details.partition_key} from {table_details.name}
    """,
    )
    return describe[0]["type"]


def get_map_database_per_workspace(workspace: User, datasource_name_or_id: str) -> Dict[str, User]:
    map_database_per_workspace = {workspace.database: workspace}
    source_datasource = Users.get_datasource(workspace, datasource_name_or_id)

    if source_datasource:
        for shared_with_workspace in source_datasource.shared_with:
            external_workspace = User.get_by_id(shared_with_workspace)
            map_database_per_workspace[external_workspace.database] = external_workspace

    return map_database_per_workspace


def is_tables_partition_compatible(
    database_server: str, source_table_details: TableDetails, destination_table_details: TableDetails
) -> bool:
    if not source_table_details.partition_key or source_table_details.partition_key in ["tuple()", ""]:
        return False

    if not destination_table_details.partition_key or destination_table_details.partition_key in ["tuple()", ""]:
        return False

    source_partition_key_type = get_partition_key_type(database_server, source_table_details)
    destination_partition_key_type = get_partition_key_type(database_server, destination_table_details)

    compatible, _ = origin_column_type_is_compatible_with_destination_type(
        source_partition_key_type, destination_partition_key_type
    )
    return compatible


def get_is_source_materialized_view_to_add(
    pipe: Pipe,
    node: PipeNode,
    dependent_datasource_id: str,
    materialized_views_flow_nodes: Dict[str, List[DataFlowNode]],
) -> bool:
    if node.materialized == dependent_datasource_id:
        list_of_materialized_views = [
            (materialized_view_location.pipe, materialized_view_location.node)
            for materialized_view_location in materialized_views_flow_nodes[dependent_datasource_id]
        ]
        if (pipe, node) not in list_of_materialized_views:
            return True
    return False


@dataclass
class DataFlowItems:
    datasources: defaultdict
    materialized_views: defaultdict
    map_datasource_to_id: Dict[str, Datasource]
    map_datasource_to_workspace: Dict[str, User]
    skipped: List[DataFlowStep]


class DataFlow:
    @staticmethod
    def get_nodes(
        source_table_details: TableDetails,
        source_workspace: User,
        source_datasource: Datasource,
        skip_incompatible_partitions: bool = False,
        check_partition_keys: bool = True,
    ) -> DataFlowItems:
        datasources_flow_nodes = defaultdict(set)
        materialized_views_flow_nodes = defaultdict(list)
        valid_nodes_list = []

        map_datasource_to_id: Dict[str, Datasource] = {source_datasource.id: source_datasource}
        map_datasource_to_workspace: Dict[str, User] = {source_datasource.id: source_workspace}

        skipped_steps: List[DataFlowStep] = []
        datasources_list: List[DataSourceFlowNode] = [
            DataSourceFlowNode(workspace=source_workspace, datasource=source_datasource)
        ]
        datasources_visited = set()

        dependent_pipes = []
        while len(datasources_list) > 0:
            next_datasource_flow_node = datasources_list.pop()

            if next_datasource_flow_node.datasource.id in datasources_visited:
                continue

            datasources_visited.add(next_datasource_flow_node.datasource.id)

            map_database_per_workspace = get_map_database_per_workspace(
                next_datasource_flow_node.workspace, next_datasource_flow_node.datasource.id
            )

            dependent_views = ch_table_dependent_views_sync(
                next_datasource_flow_node.workspace.database_server,
                next_datasource_flow_node.workspace.database,
                next_datasource_flow_node.datasource.id,
            )

            for dependent_view in dependent_views:
                if dependent_view.database not in map_database_per_workspace:
                    logging.warning(
                        f"Dependent view is in a deleted workspace: {dependent_view.database}.{dependent_view.table}"
                    )
                    continue

                workspace_with_dependent_view = map_database_per_workspace[dependent_view.database]
                node = Users.get_node(workspace_with_dependent_view, dependent_view.table)

                if not node:
                    raise DependentViewException(
                        dependent_view_name=f"{dependent_view.database}.{dependent_view.table}"
                    )
                assert isinstance(node, PipeNode)

                pipe = Users.get_pipe_by_node(workspace_with_dependent_view, node.id)
                assert isinstance(pipe, Pipe)
                dependent_pipes.append(pipe.id)

                dependent_datasource = Users.get_datasource(workspace_with_dependent_view, node.materialized)

                if not dependent_datasource:
                    # looks like there is a pipe with a materialized node that points to a table
                    # that was removed
                    pipe = Users.get_pipe_by_node(workspace_with_dependent_view, dependent_view.table)
                    assert isinstance(pipe, Pipe)
                    raise DependentTableException(
                        pipe_name=pipe.name,
                        node_name=node.name,
                        node_id=node.id,
                        node_materialized=f"{workspace_with_dependent_view.database}{node.materialized}",
                    )

                dependent_table_details = ch_table_details(
                    table_name=dependent_datasource.id,
                    database_server=workspace_with_dependent_view.database_server,
                    database=workspace_with_dependent_view.database,
                )

                if check_partition_keys:
                    is_table_compatible = is_tables_partition_compatible(
                        database_server=workspace_with_dependent_view.database_server,
                        source_table_details=source_table_details,
                        destination_table_details=dependent_table_details,
                    )

                    if not is_table_compatible:
                        if skip_incompatible_partitions:
                            skipped_steps.append(
                                DataFlowStep(
                                    step_id=str(ulid.new().hex),
                                    step_datasource=dependent_datasource,
                                    step_workspace=workspace_with_dependent_view,
                                    step_materialized_views=[],
                                    step_copy=None,
                                    step_query_id=None,
                                )
                            )
                            continue
                        else:
                            raise Exception(
                                f"Data Source {dependent_datasource.name} has incompatible partitions. Check the PARTITION KEY is present and it's compatible with the target Data Source. If you want to ignore all the Data Sources with incompatible partitions, use the option 'skip_incompatible_partitions' to skip them."
                            )

                datasource_flow_node_simple = (
                    next_datasource_flow_node.workspace.id,
                    next_datasource_flow_node.datasource.id,
                )
                datasource_flow_node_key = (workspace_with_dependent_view.id, dependent_datasource.id)
                datasources_flow_nodes[datasource_flow_node_key].add(datasource_flow_node_simple)
                valid_nodes_list.append(node.id)

                materialized_flow_node = DataFlowNode(
                    pipe=pipe,
                    node=node,
                    sql=None,
                    datasource_id=dependent_datasource.id,
                    source_has_been_processed=True,
                )
                materialized_flow_node_key = dependent_datasource.id
                materialized_views_flow_nodes[materialized_flow_node_key].append(materialized_flow_node)

                map_datasource_to_id[dependent_datasource.id] = dependent_datasource
                map_datasource_to_workspace[dependent_datasource.id] = workspace_with_dependent_view

                datasource_flow_node = DataSourceFlowNode(
                    workspace=workspace_with_dependent_view, datasource=dependent_datasource
                )
                datasources_list.append(datasource_flow_node)

        # Search for Materialized Views that write to the Data Source that depends on the original Data Source
        for dfn in datasources_flow_nodes:
            workspace_where_datasource_exists = User.get_by_id(dfn[0])
            pipes = workspace_where_datasource_exists.get_pipes()
            for p in pipes:
                if p.id in dependent_pipes:
                    for n in p.pipeline.nodes:
                        # HERE check if it comes from a recognized data source, otherwise DELETE IT
                        if n.id in valid_nodes_list and get_is_source_materialized_view_to_add(
                            p, n, dfn[1], materialized_views_flow_nodes
                        ):
                            materialized_views_flow_nodes[dfn[1]].append(
                                DataFlowNode(
                                    pipe=p, node=n, sql=None, datasource_id=dfn[1], source_has_been_processed=False
                                )
                            )

        return DataFlowItems(
            datasources=datasources_flow_nodes,
            materialized_views=materialized_views_flow_nodes,
            map_datasource_to_id=map_datasource_to_id,
            map_datasource_to_workspace=map_datasource_to_workspace,
            skipped=skipped_steps,
        )

    @staticmethod
    def get_steps(
        source_workspace: User,
        source_datasource: Datasource,
        source_pipe: Optional[Pipe] = None,
        source_sql: Optional[str] = None,
        initial_query_id: Optional[str] = None,
        skip_incompatible_partitions: bool = False,
        check_partition_keys: bool = True,
    ) -> Tuple[List[DataFlowStep], List[DataFlowStep]]:
        steps = []
        try:
            source_table_details = ch_table_details(
                table_name=source_datasource.id,
                database_server=source_workspace.database_server,
                database=source_workspace.database,
            )

            dataflow_data = DataFlow.get_nodes(
                source_table_details=source_table_details,
                source_workspace=source_workspace,
                source_datasource=source_datasource,
                skip_incompatible_partitions=skip_incompatible_partitions,
                check_partition_keys=check_partition_keys,
            )

            # 1. If the source pipe is present, and it is a copy, we should add the initial copy operation as the first step
            # We might want in the future to chain copy pipes, right now the "cascade" only works by using materialized views
            if source_pipe and source_pipe.pipe_type == PipeTypes.COPY:
                source_node = source_pipe.get_copy_node()
                step_query_id = initial_query_id if initial_query_id else ulid.new().str
                steps.append(
                    DataFlowStep(
                        step_id=str(ulid.new().hex),
                        step_datasource=dataflow_data.map_datasource_to_id[source_datasource.id],
                        step_workspace=dataflow_data.map_datasource_to_workspace[source_datasource.id],
                        step_materialized_views=[],
                        step_copy=DataFlowNode(
                            pipe=source_pipe,
                            node=source_node,
                            sql=source_sql,
                            datasource_id="",
                            source_has_been_processed=True,
                        ),
                        step_query_id=step_query_id,
                    )
                )

            # 2. We build the dependencies graph by getting the tables connected by materialized views
            datasources_flow_graph = toposort(dataflow_data.datasources)
            datasource_index = 0
            is_source_copy = source_pipe and source_pipe.pipe_type == PipeTypes.COPY
            for datasources_flow_nodes in datasources_flow_graph:
                for datasource_flow_node in datasources_flow_nodes:
                    step_materialized_views = dataflow_data.materialized_views[datasource_flow_node[1]]
                    if len(step_materialized_views):
                        step_query_id = (
                            initial_query_id
                            if initial_query_id and datasource_index == 0 and not is_source_copy
                            else ulid.new().str
                        )
                        datasource_index += 1
                        steps.append(
                            DataFlowStep(
                                step_id=str(ulid.new().hex),
                                step_datasource=dataflow_data.map_datasource_to_id[datasource_flow_node[1]],
                                step_workspace=dataflow_data.map_datasource_to_workspace[datasource_flow_node[1]],
                                step_materialized_views=step_materialized_views,
                                step_copy=None,
                                step_query_id=step_query_id,
                            )
                        )
            return steps, dataflow_data.skipped
        except CHException as e:
            logging.exception(f"Error when getting steps for the copy job: {e}")
            if e.code == CHErrors.TIMEOUT_EXCEEDED:
                raise CopyException(CopyJobErrorMessages.timeout.format(timeout_seconds=MAX_EXECUTION_TIME))
            else:
                raise CopyException("There was a problem while copying data, kindly contact us at support@tinybird.co")
