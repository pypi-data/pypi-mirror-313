import json
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Set

from tinybird.ch_utils.constants import COPY_ENABLED_TABLE_FUNCTIONS
from tinybird.data_connector import DataConnectors, DataSink

from .chart import Chart
from .resource import Resource
from .sql import as_subquery
from .sql_template import (
    Template,
    TemplateExecutionResults,
    get_used_tables_in_template,
    get_var_names_and_types,
    render_sql_template,
)
from .sql_toolset import ReplacementsDict, replace_tables, sql_get_used_tables

EXAMPLE_PIPE_OBJECT = {
    "name": "pipe_name",
    "nodes": [
        {"sql": "select * from datasource_foo limit 1", "name": "node_00"},
        {"sql": "select count() from node_00", "name": "node_01"},
    ],
}


class CopyModes:
    APPEND = "append"
    REPLACE = "replace"

    valid_modes = (APPEND, REPLACE)

    @staticmethod
    def is_valid(node_mode):
        return node_mode.lower() in CopyModes.valid_modes


class PipeTypes:
    MATERIALIZED = "materialized"
    ENDPOINT = "endpoint"
    COPY = "copy"
    DATA_SINK = "sink"
    STREAM = "stream"
    DEFAULT = "default"


class PipeNodeTypes:
    MATERIALIZED = "materialized"
    ENDPOINT = "endpoint"
    STANDARD = "standard"
    DEFAULT = "default"
    DATA_SINK = "sink"
    COPY = "copy"
    STREAM = "stream"

    valid_types = (MATERIALIZED, ENDPOINT, STANDARD, COPY, DATA_SINK, STREAM)

    @staticmethod
    def is_valid(node_type):
        return node_type.lower() in PipeNodeTypes.valid_types


class PipeNodeTags:
    MATERIALIZING = "materializing"
    COPY_TARGET_DATASOURCE = "copy_target_datasource"
    COPY_TARGET_WORKSPACE = "copy_target_workspace"


class NodeNotFound(Exception):
    pass


class PipeValidationException(Exception):
    pass


class NodeValidationException(Exception):
    pass


class EndpointNodesCantBeDropped(ValueError):
    pass


class DependentMaterializedNodeOnUpdateException(Exception):
    pass


class DependentException(Exception):
    def __init__(self, dependencies: Dict, pipes: List[str], nodes: List[str]):
        self._dependencies = dependencies
        self._pipes = pipes
        self._nodes = nodes

    @property
    def dependencies(self):
        return self._dependencies

    @property
    def pipes(self):
        return self._pipes

    @property
    def nodes(self):
        return self._nodes

    @property
    def pipe_names(self):
        return ",".join(self.dependencies.keys())

    @property
    def node_names(self):
        return ",".join([f'({",".join(nodes)})' for nodes in self.dependencies.values()])

    @property
    def all_dependencies(self) -> Dict:
        return {"dependencies": self.dependencies, "dependent_pipes": self.pipes, "dependent_nodes": self.nodes}


class DependentMaterializedNodeException(DependentException):
    def __init__(
        self,
        upstream_mat_pipes: List[str],
        upstream_mat_nodes: List[str],
        downstream_mat_pipes: List[str],
        downstream_mat_nodes: List[str],
        dependencies: Dict,
        workspace_name: str,
        include_workspace_name: bool = False,
        is_api: bool = False,
        is_cli: bool = False,
    ):
        self._mat_nodes = list(set().union(upstream_mat_nodes, downstream_mat_nodes))
        self._dependencies = dependencies

        self.upstream_mat_pipes = ",".join(upstream_mat_pipes) if upstream_mat_pipes else ""
        self.upstream_mat_nodes = ",".join(upstream_mat_nodes) if upstream_mat_nodes else ""
        self.downstream_mat_pipes = ",".join(downstream_mat_pipes) if downstream_mat_pipes else ""
        self.downstream_mat_nodes = ",".join(downstream_mat_nodes) if downstream_mat_nodes else ""

        self.affected_materializations_message = ""
        if self.upstream_mat_nodes:
            self.affected_materializations_message += f'Affected upstream materializations => Pipes="{self.upstream_mat_pipes}", nodes="{self.upstream_mat_nodes}". '
        if self.downstream_mat_nodes:
            self.affected_materializations_message += f'Affected downstream materializations => Pipes="{self.downstream_mat_pipes}", nodes="{self.downstream_mat_nodes}". '

        self.break_ingestion_message = "This operation will break ingestion due to broken Materialized Views, unlink the Materialized Nodes or remove the dependency with the Data Source. "
        if self.upstream_mat_nodes and not self.downstream_mat_nodes:
            self.break_ingestion_message = (
                "The Data Source is the target of a Materialized View. Deleting it may break your data ingestion. "
            )
            self.break_ingestion_message += (
                "Set the `force` parameter to `true` to unlink the dependent Materialized Nodes and delete the Data Source. "
                if is_api
                else ""
            )

        pipes, nodes = parse_dependencies(dependencies, workspace_name, include_workspace_name)
        pipe_names = ",".join(pipes) if pipes else ""
        node_names = ",".join(nodes) if nodes else ""
        self.dependent_pipes_message = f'The Data Source is used in => Pipes="{pipe_names}", nodes="{node_names}"'

        if is_cli:
            self.affected_materializations_message = "\n" + self.affected_materializations_message
            self.dependent_pipes_message = "\n" + self.dependent_pipes_message
        super().__init__(dependencies, pipes, nodes)

    @property
    def has_downstream_dependencies(self):
        return self.downstream_mat_nodes != ""

    @property
    def dependencies(self):
        return self._dependencies

    @property
    def pipes(self):
        return self._pipes

    @property
    def nodes(self):
        return self._nodes

    @property
    def pipe_names(self):
        return ",".join(self.dependencies.keys())

    @property
    def node_names(self):
        return ",".join([f'({",".join(nodes)})' for nodes in self.dependencies.values()])


class DependentCopyPipeException(DependentException):
    def __init__(
        self, dependencies: Dict, workspace_name: str, include_workspace_name: bool = False, is_cli: bool = False
    ):
        dependencies = dependencies
        pipes, nodes = parse_dependencies(dependencies, workspace_name, include_workspace_name)
        pipe_names = ",".join(pipes) if pipes else ""
        node_names = ",".join(nodes) if nodes else ""
        self.dependent_pipes_message = f'The Data Source is used in => Pipes="{pipe_names}", nodes="{node_names}"'
        self.break_copy_message = (
            "The Data Source is the target of a Copy Pipe. If you force the deletion, the copy will be unset."
        )

        if is_cli:
            self.dependent_pipes_message = "\n" + self.dependent_pipes_message
        super().__init__(dependencies, pipes, nodes)


def parse_dependencies(dependencies: Dict, workspace_name: str, include_workspace_name: bool = False):
    dependent_pipes_names, dependent_node_names = [], []
    for pipe_dependency in dependencies.get("pipes", []):
        pipe_ws = pipe_dependency["workspace"]
        ws_prefix = f"{pipe_ws}." if include_workspace_name or pipe_ws != workspace_name else ""
        dependent_pipes_names.append(ws_prefix + pipe_dependency["name"])
        for node_info in pipe_dependency["nodes"]:
            dependent_node_names.append(ws_prefix + node_info["name"])
    return dependent_pipes_names, dependent_node_names


class PipeNode:
    """
    >>> node = PipeNode('pipe_node_name', 'select * from other_pipe_node')
    >>> node.dependencies
    ['other_pipe_node']
    >>> node.sql = 'select * from my_new_pipe'
    >>> node.dependencies
    ['my_new_pipe']
    >>> node.sql = 'select * from shared.datasource'
    >>> node.dependencies
    ['shared.datasource']
    >>> node.sql = "%select * from templated_shared.datasource"
    >>> node.dependencies
    ['templated_shared.datasource']
    >>> node.sql = "%select * from {% if defined(test) %}{{TABLE('my_new_pipe_inside_if')}}{% else %}testing_table{% end %}" # noqa: E501
    >>> set(node.dependencies) == {'testing_table', 'my_new_pipe_inside_if'}
    True
    >>> node.sql = "%select * from {% if defined(test) %}{{TABLE('shared.datasource')}}{% else %}testing_table{% end %}" # noqa: E501
    >>> set(node.dependencies) == {'testing_table', 'shared.datasource'}
    True
    >>> node.sql = "%select * from {{TABLE('shared.datasource')}}"
    >>> node.dependencies
    ['shared.datasource']
    >>> node.sql = 'this is a non valid sql'
    >>> try:
    ...     node.dependencies
    ...     print("should not print this")
    ... except ValueError as e:
    ...     print("raised")
    raised
    >>> node.sql = 'this is a non valid sql'
    >>> node.ignore_sql_errors = True
    >>> node.dependencies
    []
    """

    def __init__(
        self,
        name: Optional[str],
        sql: Optional[str],
        description: Optional[str] = None,
        materialized: Optional[str] = None,
        guid: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        tags: Optional[Dict[str, Any]] = None,
        mode: Optional[str] = None,
        node_type: Optional[str] = None,
    ) -> None:
        if not name or not sql:
            raise ValueError("The name and sql parameters are mandatory in pipe nodes")
        self.id = guid or Resource.guid()
        self._name = name
        self._sql = sql
        self._mode = mode
        self._description = description
        self.materialized = materialized
        self._node_type = node_type
        self.cluster: Optional[str] = None
        self.tags = tags or {}
        self._dependencies: Optional[Set[str]] = None
        self._template_params: Optional[List[Dict[str, Any]]] = None
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or self.created_at
        # TODO: Remove this as it's not being used  https://gitlab.com/tinybird/analytics/-/issues/2374
        self.version = 0
        self.project = None
        self.result: Optional[Dict[str, Any]] = None

        # when this is True the SQL stored in _sql attribute does not need to
        # be checked for valid syntax (or be a valid template)
        # in this way it allows to store non-valid SQL
        self.ignore_sql_errors = False

    @property
    def dependencies(self) -> List[str]:
        if self._dependencies is None:
            try:
                tables = sql_get_used_tables(
                    self.sql, raising=True, table_functions=False, function_allow_list=COPY_ENABLED_TABLE_FUNCTIONS
                )
                self._dependencies = set([f"{d[0]}.{d[1]}" if d[0] != "" else d[1] for d in tables])
                if self.is_template():
                    self._dependencies.update(get_used_tables_in_template(self._sql.strip()[1:]))
            except Exception as e:
                if not self.ignore_sql_errors:
                    raise e
                else:
                    # dependencies always need to be a set
                    self._dependencies = set()
        return list(self._dependencies)

    @property
    def template_params(self) -> List[Dict[str, Any]]:
        self._template_params = getattr(self, "_template_params", None)
        if self._template_params is None:
            self._template_params = self._get_template_params()
        return self._template_params

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.__update_updated_at()

    @property
    def mode(self):
        if hasattr(self, "_mode"):
            return self._mode
        return None

    @mode.setter
    def mode(self, value):
        self._mode = value
        self.__update_updated_at()

    def is_template(self) -> bool:
        """
        >>> node = PipeNode('node_name', 'select * from source_table')
        >>> node.is_template()
        False
        >>> node.sql = '%select * from source_table'
        >>> node.is_template()
        True
        >>> node.sql = '\\n'
        >>> node.is_template()
        False
        """
        clean_sql = self._sql.strip()
        return clean_sql[0] == "%" if clean_sql else False

    @property
    def is_materializing(self) -> bool:
        return self.tags.get(PipeNodeTags.MATERIALIZING, False) is True

    # needed to use in map(func, iterable)
    def get_template_params(self) -> List[Dict[str, Any]]:
        return self.template_params

    def _get_template_params(self) -> List[Dict[str, Any]]:
        if self.is_template():
            try:
                t = Template(self._sql[1:])
                return get_var_names_and_types(t, node_id=self.id)
            except Exception as e:
                if self.ignore_sql_errors:
                    return []
                else:
                    raise e
        return []

    def get_sql_and_template_results(
        self,
        variables: Optional[Dict[str, Any]] = None,
        secrets: Optional[List[str]] = None,
    ):
        return render_sql_template(self._sql[1:], variables, test_mode=variables is None, secrets=secrets)

    @property
    def sql(self) -> str:
        if self.is_template():
            sql, _, _ = self.get_sql_and_template_results()
            return sql
        return self._sql

    @sql.setter
    def sql(self, value):
        self._sql = value
        self._dependencies = None
        self._template_params = None
        self.__update_updated_at()

    def render_sql(
        self,
        variables: Optional[Dict[str, Any]] = None,
        template_execution_results: Optional[TemplateExecutionResults] = None,
        secrets: Optional[List[str]] = None,
    ) -> str:
        if self.is_template():
            if template_execution_results is None:
                template_execution_results = TemplateExecutionResults()
            sql, _template_execution_results, _ = self.get_sql_and_template_results(
                variables=variables, secrets=secrets
            )
            template_execution_results.update_all(_template_execution_results)
            return sql
        return self._sql

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value):
        self._description = value
        self.__update_updated_at()

    @property
    def node_type(self) -> Optional[str]:
        if hasattr(self, "_node_type"):
            return self._node_type
        return None

    @node_type.setter
    def node_type(self, value):
        self._node_type = value

    def get_replacements(
        self,
        variables: Optional[Dict[str, Any]] = None,
        template_execution_results: Optional[TemplateExecutionResults] = None,
        secrets: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        replacements = {
            self.name: self.id,
            self.id: lambda: as_subquery(
                f"SELECT * FROM {self.materialized}"
                if self.materialized
                else self.render_sql(variables, template_execution_results=template_execution_results, secrets=secrets)
            ),
        }
        if self.materialized and self.tags.get("staging", False):
            replacements[self.materialized] = replacements[self.id]
        return ReplacementsDict(replacements)

    def to_dict(self, attrs=None):
        """
        >>> n1 = PipeNode('abcd', 'select 1', 'new pipe node')
        >>> print(n1.to_dict().get('node_type'))
        None
        >>> n2 = PipeNode('node1', 'select 2', 'new pipe node 1', node_type=PipeNodeTypes.STANDARD)
        >>> n2.to_dict().get('node_type')
        'standard'
        >>> n2.node_type = PipeNodeTypes.ENDPOINT
        >>> n2.to_dict().get('node_type')
        'endpoint'
        """
        node = {}

        if not attrs:
            node = {
                "id": self.id,
                "name": self.name,
                "sql": self._sql,
                "description": self.description,
                "materialized": self.materialized,
                "cluster": self.cluster,
                "tags": self.tags,
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "version": self.version,
                "project": self.project,
                "result": self.result,
                "ignore_sql_errors": self.ignore_sql_errors,
                "node_type": self.node_type,
            }
            if self.mode:
                node["mode"] = self.mode
            return node
        else:
            for attr in attrs:
                try:
                    node[attr] = getattr(self, attr)
                except AttributeError:
                    pass
            return node

    def to_json(self, dependencies: bool = True, attrs: Optional[List[str]] = None) -> Dict[str, Any]:
        d = self.to_dict(attrs=attrs)
        if not attrs:
            d["created_at"] = str(self.created_at)
            d["updated_at"] = str(self.updated_at)
            if dependencies:
                d["dependencies"] = self.dependencies
                d["params"] = self.template_params
            return d
        else:
            node = {}
            for attr in attrs:
                try:
                    node[attr] = getattr(self, attr)
                except AttributeError:
                    pass
            if "created_at" in d:
                d["created_at"] = str(self.created_at)
            if "updated_at" in d:
                d["updated_at"] = str(self.updated_at)
            if "params" in attrs:
                d["params"] = self.template_params

            d.update(node)
            return d

    def __repr__(self):
        return f"{self.__class__}({self.name})"

    @property
    def resource(self) -> str:
        return "Node"

    @property
    def resource_name(self) -> str:
        return "Node"

    def __eq__(self, other):
        """
        >>> n0 = PipeNode('abcd', 'select 1')
        >>> n0 == PipeNode('abcd', 'select 1', guid=n0.id)
        True
        >>> n0 == None
        False
        >>> PipeNode('abcd', 'select 1') == PipeNode('abcd', 'select 1')
        True
        >>> PipeNode('a', 'select 1', guid='uuuu') == PipeNode('z', 'select 1', guid='uuuu')
        True
        >>> class F:
        ...    id = n0.id
        ...    name = 'abcd'
        >>> n0 == F()
        False
        """
        return (
            other is not None
            and type(self) == type(other)  # noqa: E721
            and (self.id == other.id or self.name == other.name)
        )

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "PipeNode":
        node = PipeNode(
            d["name"],
            d["sql"],
            description=d.get("description", None),
            materialized=d.get("materialized", None),
            mode=d.get("mode", None),
            guid=d.get("id", None),
            node_type=d.get("node_type", PipeNodeTypes.STANDARD),
        )
        node.cluster = d.get("cluster", None)
        node.tags = d.get("tags", {})
        node.created_at = d.get("created_at", datetime.now())
        node.updated_at = d.get("updated_at", node.created_at)
        node.version = d.get("version", 0)
        node.project = d.get("project", None)
        node.ignore_sql_errors = d.get("ignore_sql_errors", False)

        return node

    def __update_updated_at(self):
        self.updated_at = datetime.now()


class TransformationPipeline:
    """
    >>> t = TransformationPipeline()
    >>> n0 = PipeNode('node0', 'select * from source_table')
    >>> t.append(n0)
    >>> n1 = PipeNode('node1', 'select count() from node0')
    >>> t.append(n1)
    >>> t.append(PipeNode('node2', 'select * from node1 where a = 1'))
    >>> from chtoolset import query as chquery
    >>> expected_query = chquery.format(f'select * from (select count() from (select * from source_table) as {n0.name}) as {n1.name} where a = 1')
    >>> t.get_sql_for_node('node2') == expected_query
    True
    >>> t.append(PipeNode('node3', 'select * from test_00'))
    >>> t.get_sql_for_node('node3')
    'SELECT *\\nFROM test_00'
    >>> t.append(PipeNode('node1', 'select * from node0'))
    Traceback (most recent call last):
    ...
    ValueError: Node name "node1" already exists in pipe. Node names must be unique within a given pipe.
    >>> t.get_sql_for_node('node3')
    'SELECT *\\nFROM test_00'
    """

    def __init__(
        self,
        nodes: Optional[List[PipeNode]] = None,
        endpoint: Optional[str] = None,
        copy_node: Optional[str] = None,
        sink_node: Optional[str] = None,
        stream_node: Optional[str] = None,
    ) -> None:
        self.nodes: List[PipeNode] = []
        self.endpoint = endpoint

        if nodes:
            for node in nodes:
                if endpoint and node.id == endpoint:
                    node.node_type = PipeNodeTypes.ENDPOINT
                elif copy_node and node.id == copy_node:
                    node.node_type = PipeNodeTypes.COPY
                elif sink_node and node.id == sink_node:
                    node.node_type = PipeNodeTypes.DATA_SINK
                elif stream_node and node.id == stream_node:
                    node.node_type = PipeNodeTypes.STREAM
                elif node.materialized is not None:
                    node.node_type = PipeNodeTypes.MATERIALIZED
                else:
                    node.node_type = PipeNodeTypes.STANDARD
                self.append(node)

    @property
    def node_names(self) -> List[str]:
        return [x.name for x in self.nodes]

    def clone(self):
        nodes = list(map(PipeNode.from_dict, map(PipeNode.to_dict, self.nodes)))
        endpoint = self.endpoint
        return TransformationPipeline(nodes=nodes, endpoint=endpoint)

    def get_replacements(
        self,
        variables: Optional[Dict[str, Any]] = None,
        template_execution_results: Optional[TemplateExecutionResults] = None,
        secrets: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """return replacement for all the nodes"""
        replacements = {}
        for node in self.nodes:
            replacements.update(
                node.get_replacements(variables, template_execution_results=template_execution_results, secrets=secrets)
            )
        return replacements

    def get_materialized_tables(self):
        return list(filter(None, [node.materialized for node in self.nodes]))

    def get_sql_for_node(
        self,
        node_name_or_id: Optional[str],
        variables: Optional[Dict[str, Any]] = None,
        template_execution_results: Optional[TemplateExecutionResults] = None,
        timestamp: Optional[datetime] = None,
        secrets: Optional[List[str]] = None,
    ) -> str:
        """
        >>> t = TransformationPipeline()
        >>> n0 = PipeNode('node0', 'select * from source_table')
        >>> t.append(n0)
        >>> n1 = PipeNode('node1', 'select count() from node0')
        >>> t.append(n1)
        >>> t.append(PipeNode('node2', 'select * from node1 where a = 1'))
        >>> t.get_sql_for_node('node0')
        'SELECT *\\nFROM source_table'
        >>> from chtoolset import query as chquery
        >>> expected_query = chquery.format(f'select count() from (select * from source_table) as {n0.name}')
        >>> t.get_sql_for_node('node1') == expected_query
        True
        >>> expected_query = chquery.format(f'select * from (select count() from (select * from source_table) as {n0.name}) as {n1.name} where a = 1')
        >>> t.get_sql_for_node('node2') == expected_query
        True
        >>> t.append(PipeNode('node3', 'select * from node2 where a = 1'))
        >>> expected_query = chquery.format(f'select * from (select * from (select count() from (select * from source_table) as {n0.name}) as {n1.name} where a = 1) as node2 where a = 1')
        >>> t.get_sql_for_node('node3') == expected_query
        True
        >>> t.get_sql_for_node('doesnotexist')
        Traceback (most recent call last):
        ...
        Exception: Node 'doesnotexist' not found
        >>> t.get_node(t.nodes[0].id) == t.nodes[0]
        True
        """
        node: Optional[PipeNode] = Resource.by_name_or_id(self.nodes, node_name_or_id)
        if not node:
            raise Exception(f"Node '{node_name_or_id}' not found")
        sql = (
            f"SELECT * FROM {node.materialized}"
            if node.materialized
            else node.render_sql(variables, template_execution_results, secrets=secrets)
        )
        return replace_tables(
            sql,
            self.get_replacements(variables, template_execution_results, secrets=secrets),
            timestamp=node.updated_at,
        )

    def next_valid_name(self, prefix: str = "") -> str:
        """
        >>> prefix = 'pipe_name'
        >>> t = TransformationPipeline()
        >>> t.append(PipeNode(f'{prefix}0', 'select * from source_table'))
        >>> first_node = t.last()
        >>> t.append(PipeNode(f'{prefix}_1', 'select * from source_table'))
        >>> t.next_valid_name(prefix)
        'pipe_name_2'
        >>> t.drop_node(first_node.id)
        >>> t.next_valid_name(prefix)
        'pipe_name_2'
        >>> t.append(PipeNode('pipe_name2', 'select * from source_table'))
        >>> t.next_valid_name(prefix)
        'pipe_name_3'
        >>> t.append(PipeNode('pipe_name_4', 'select * from source_table'))
        >>> t.append(PipeNode('pipe_name_3', 'select * from source_table'))
        >>> t.next_valid_name(prefix)
        'pipe_name_5'
        """
        names = [x.name for x in self.nodes]
        pattern = re.compile(rf"{prefix}.*?(\d+)$")
        next_i = len(self.nodes)
        for name in names:
            m = re.match(pattern, name)
            if m and m.groups():
                next_i = max(next_i, int(m.group(1)) + 1)
        return f"{prefix}_{next_i}"

    def append(self, node: PipeNode) -> None:
        """
        >>> t_pipe = TransformationPipeline()
        >>> n0 = PipeNode('test', 'select * from source_table')
        >>> print(n0.node_type)
        None
        >>> t_pipe.append(n0)
        >>> n0.node_type = PipeNodeTypes.STANDARD
        >>> n0.to_dict().get('node_type')
        'standard'
        >>> t_pipe = TransformationPipeline()
        >>> n1 = PipeNode('test', 'select * from source_table', node_type=PipeNodeTypes.COPY)
        >>> n1.node_type
        'copy'
        >>> t_pipe.append(n1)
        >>> t_pipe_n1 = t_pipe.to_json()[0]
        >>> t_pipe_n1.get('node_type')
        'copy'
        >>> t_pipe = TransformationPipeline()
        >>> n2 = PipeNode('test', 'select * from source_table')
        >>> print(n2.node_type)
        None
        >>> t_pipe.append(n2)
        >>> t_pipe_n1 = t_pipe.to_json()[0]
        >>> print(t_pipe_n1.get('node_type'))
        None
        """
        if node.name in self.node_names:
            raise ValueError(
                f'Node name "{node.name}" already exists in pipe. Node names must be unique within a given pipe.'
            )
        if not hasattr(node, "_node_type"):
            node.node_type = None
        self.nodes.append(node)

    def get_dependent_nodes(self, node_name_or_id: Optional[str]) -> List[PipeNode]:
        target_node: Optional[PipeNode] = self.get_node(node_name_or_id)
        if not target_node:
            return []

        def get_node_dependencies(node: PipeNode) -> List[str]:
            try:
                return node.dependencies
            except Exception:
                return []

        dependent_nodes = {target_node.id: target_node}

        seen_dependencies: Set[str] = set()
        dependencies = get_node_dependencies(target_node)
        while dependencies:
            dep_name = dependencies.pop()
            seen_dependencies.add(dep_name)
            node = self.get_node(dep_name)
            if node:
                dependent_nodes[node.id] = node
                for d in get_node_dependencies(node):
                    if d not in seen_dependencies:
                        dependencies.append(d)

        return list(dependent_nodes.values())

    def __len__(self):
        return len(self.nodes)

    def last(self) -> PipeNode:
        return self.nodes[-1]

    def update_node(
        self,
        node_name_or_id: Optional[str],
        sql: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        mode: Optional[str] = None,
        node_type: Optional[str] = None,
    ) -> "PipeNode":
        node: Optional[PipeNode] = self.get_node(node_name_or_id)
        if node is None:
            raise NodeNotFound()
        if sql:
            node.sql = sql
        if name:
            if name in [x.name for x in self.nodes]:
                raise ValueError(
                    f'Node name "{name}" already exists in pipe. Node names must be unique within a given pipe.'
                )
            node.name = name
        if description is not None:
            node.description = description
        if mode is not None:
            node.mode = mode
        if node_type is not None:
            node.node_type = node_type
        return node

    def set_node_mode(self, node_name_or_id: Optional[str], mode: Optional[str]) -> "PipeNode":
        """
        >>> pipe = Pipe('test', [{'name': 't0', 'sql': 'select * from test_ds'}])
        >>> node = pipe.set_node_mode(pipe.pipeline.last().id, mode='append', edited_by = '')
        >>> node.mode
        'append'
        >>> _ = pipe.append_node(PipeNode('t1', 'select * from test'))
        >>> node = pipe.set_node_mode(pipe.pipeline.last().id, mode=None, edited_by = '')
        >>> node.mode
        """
        node: Optional[PipeNode] = self.get_node(node_name_or_id)
        if node is None:
            raise NodeNotFound()
        node.mode = mode
        return node

    def set_node_tag(self, node_name_or_id: Optional[str], tag: str, value: str | bool) -> "PipeNode":
        node = self.get_node(node_name_or_id)
        if not node:
            raise NodeNotFound()
        node.tags[tag] = value
        return node

    def drop_node_tag(self, node_name_or_id: Optional[str], tag: str) -> "PipeNode":
        node = self.get_node(node_name_or_id)
        if not node:
            raise NodeNotFound()

        if tag in node.tags:
            del node.tags[tag]
        return node

    def drop_node(self, node_name_or_id: Optional[str]) -> None:
        node_index = self.get_node_index(node_name_or_id)
        if node_index is not None and node_index >= 0:
            del self.nodes[node_index]

    def to_dict(self, node_attrs=None) -> List[Dict[str, Any]]:
        return list(map(lambda node: node.to_dict(attrs=node_attrs), self.nodes))

    def to_json(self, dependencies: bool = True, node_attrs: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        return [node.to_json(dependencies=dependencies, attrs=node_attrs) for node in self.nodes]

    def get_node_index(self, node_name_or_id: Optional[str]) -> Optional[int]:
        if not node_name_or_id:
            return None
        node_name_or_id = Resource.normalize(node_name_or_id)
        return next((i for i, x in enumerate(self.nodes) if x.id == node_name_or_id or x.name == node_name_or_id), None)

    def get_node(self, node_name_or_id: Optional[str]) -> Optional[PipeNode]:
        return Resource.by_name_or_id(self.nodes, node_name_or_id)

    def get_dependencies(self) -> List[str]:
        deps = []
        for x in self.nodes:
            deps += x.dependencies
        return list(set(deps))

    def get_params(self, node_name_or_id: Optional[str]) -> List[Dict[str, Any]]:
        params = [y for x in map(PipeNode.get_template_params, self.get_dependent_nodes(node_name_or_id)) for y in x]
        unique_params: Dict[str, Any] = {}
        for d in params:
            name = d["name"]
            # Parameter definitions are now merged so that all definitions are
            # taken into account for OpenAPI and UI.
            # All parameter definition properties are merged, but the ones that
            # include `used_in: 'function_call'`, which are not complete because
            # the parameter does not provide a complete definition when used like:
            # `defined(parameter)` or even `defined({{Int8(parameter)}})`.
            # The only one that works properly is `defined(Int8(parameter))`
            if name not in unique_params:
                unique_params[name] = d
            elif getattr(d, "used_in", "") != "function_call":
                current_parameter_config = {**unique_params[name]}
                unique_params[name] = {
                    k: (d.get(k) or current_parameter_config.get(k)) for k in set(d) | set(current_parameter_config)
                }

        return [x for x in unique_params.values() if x.get("name", "_")[0] != "_"]

    def node_comparator(self, id0, id1):
        i0 = i1 = -1
        for i, x in enumerate(self.nodes):
            if x.id == id0:
                i0 = i
            if x.id == id1:
                i1 = i
        if i0 == i1:
            return 0
        if i0 > i1:
            return 1
        if i0 < i1:
            return -1


class Pipe:
    """
    >>> pipe = Pipe('test', [{'name': 'test_0', 'sql': 'select * from test_ds'}])
    >>> pipe.get_replacements()
    {}
    >>> n0 = pipe.pipeline.nodes[0]
    >>> pipe.endpoint = n0.id
    >>> r = pipe.get_replacements()
    >>> r[pipe.id]  # The pipe query is the one from the node.
    '(\\nSELECT *\\nFROM test_ds\\n)'
    >>> n1 = pipe.append_node(PipeNode('test_1', 'select * from test_ds where a = 1'))
    >>> n1.name
    'test_1'
    >>> n1.sql
    'select * from test_ds where a = 1'
    >>> n1.description is None
    True
    >>> n1.dependencies
    ['test_ds']
    >>> r = pipe.get_replacements()
    >>> r[pipe.id]  # The pipe query continues to be the one from the endpoint.
    '(\\nSELECT *\\nFROM test_ds\\n)'
    >>> pipe.endpoint = n1.id
    >>> r = pipe.get_replacements()
    >>> r[pipe.id]  # The query for the pipe gets updated with the new endpoint.
    '(\\nSELECT *\\nFROM test_ds\\nWHERE a = 1\\n)'
    >>> p = Pipe('desc', [], description='wadus')
    >>> p.description
    'wadus'
    """

    def __init__(
        self,
        name: str,
        nodes: List[Dict[str, Any]],
        description: Optional[str] = None,
        guid: Optional[str] = None,
        endpoint: Optional[str] = None,
        parent: Optional[str] = None,
        copy_node: Optional[str] = None,
        sink_node: Optional[str] = None,
        edited_by: Optional[str] = None,
        workspace_id: Optional[str] = None,
        stream_node: Optional[str] = None,
    ) -> None:
        self.id = guid or Resource.guid()
        self.name = name
        self.description = description
        self.created_at = datetime.now()
        self.edited_by = edited_by
        self.updated_at = self.created_at
        self.pipeline = TransformationPipeline(endpoint=endpoint, copy_node=copy_node, sink_node=sink_node)
        self._endpoint = endpoint
        self._copy_node = copy_node
        self._sink_node = sink_node
        self._stream_node = stream_node
        self.parent = parent
        self.set_nodes(nodes, endpoint, copy_node, sink_node, sink_node)
        self.last_commit: Dict[str, Any] = {"content_sha": "", "path": ""}
        self.workspace_id = workspace_id

    def clone_with_new_ids(self) -> "Pipe":
        """returns a new pipe with different id's
        >>> pipe = Pipe('test', [{'name': 'test_0', 'sql': 'select * from test_ds'}])
        >>> pipe.id != None
        True
        >>> pclone = pipe.clone_with_new_ids()
        >>> pclone.id != None
        True
        >>> pclone.id != pipe.id
        True
        >>> pclone.id != pipe.id
        True
        >>> pipe.pipeline.nodes[0].id != pclone.pipeline.nodes[0].id
        True
        >>> pipe.pipeline.nodes[0].sql
        'select * from test_ds'
        >>> pclone.pipeline.nodes[0].sql
        'select * from test_ds'
        """
        nodes = self.pipeline.to_dict()
        for x in nodes:
            x["id"] = None
        return Pipe(self.name, nodes, description=self.description)

    def copy_from_pipe(self, pipe_to_swap: "Pipe") -> "Pipe":
        self._endpoint = pipe_to_swap.endpoint
        self._copy_node = pipe_to_swap.copy_node
        self._sink_node = pipe_to_swap.sink_node
        self._stream_node = pipe_to_swap.stream_node
        self._parent = pipe_to_swap.parent
        self.pipeline.nodes = pipe_to_swap.pipeline.nodes
        self.description = pipe_to_swap.description
        self.updated_at = datetime.now()
        self.edited_by = pipe_to_swap.edited_by
        return self

    @property
    def pipe_type(self) -> str:
        # NOTE: Some pipes for old clients have materialized nodes but also endpoint nodes.
        # On these cases, the type will be 'endpoint' by default
        if self.endpoint:
            return PipeTypes.ENDPOINT
        if self.copy_node:
            return PipeTypes.COPY
        if self.sink_node:
            return PipeTypes.DATA_SINK
        if self.stream_node:
            return PipeTypes.STREAM
        if self.is_materialized:
            return PipeTypes.MATERIALIZED
        return PipeTypes.DEFAULT

    @property
    def endpoint_charts(self) -> List[Dict[str, Any]] | None:
        return [chart.to_json() for chart in Chart.get_all_by_owner(self.id)]

    @property
    def copy_target_datasource(self):
        if not self.copy_node:
            return None
        node = self.pipeline.get_node(self.copy_node)
        if not node:
            return None
        return node.tags.get(PipeNodeTags.COPY_TARGET_DATASOURCE)

    @property
    def copy_target_workspace(self):
        if not self.copy_node:
            return None
        node = self.pipeline.get_node(self.copy_node)
        if not node:
            return None
        return node.tags.get(PipeNodeTags.COPY_TARGET_WORKSPACE)

    @property
    def copy_mode(self):
        if not self.copy_node:
            return None
        node = self.pipeline.get_node(self.copy_node)
        if not node:
            return None
        return node.mode

    @property
    def is_materialized(self) -> bool:
        return len(self.get_materialized_tables()) > 0

    def get_materialized_tables(self):
        return self.pipeline.get_materialized_tables()

    @property
    def endpoint(self) -> Optional[str]:
        return self._endpoint

    @endpoint.setter
    def endpoint(self, node_name_or_id: Optional[str]):
        if node_name_or_id and not self.pipeline.get_node(node_name_or_id):
            raise ValueError(f"Pipe '{self.name}' does not contain the '{node_name_or_id}' node")
        self._endpoint = node_name_or_id
        self.updated_at = datetime.now()

    @property
    def copy_node(self) -> Optional[str]:
        return self._copy_node

    @copy_node.setter
    def copy_node(self, node_name_or_id: Optional[str]) -> None:
        if not node_name_or_id:
            self._copy_node = None
            return
        node = self.pipeline.get_node(node_name_or_id)
        if not node:
            raise ValueError(f"Pipe '{self.name}' does not contain the '{node_name_or_id}' node")
        self._copy_node = node.id
        self.updated_at = datetime.now()

    def get_copy_node(self) -> PipeNode:
        copy_node: Optional[PipeNode] = self.pipeline.get_node(self.copy_node)
        if not copy_node:
            raise NodeNotFound(f"Pipe '{self.name}' does not contain the '{self.copy_node}' node")
        return copy_node

    @property
    def sink_node(self):
        return self._sink_node

    @sink_node.setter
    def sink_node(self, node_name_or_id: Optional[str]) -> None:
        if not node_name_or_id:
            self._sink_node = None
            return
        node = self.pipeline.get_node(node_name_or_id)
        if not node:
            raise ValueError(f"Pipe '{self.name}' does not contain the '{node_name_or_id}' node")
        self._sink_node = node.id
        self.updated_at = datetime.now()

    def get_sink_node(self):
        sink_node = self.pipeline.get_node(self.sink_node)
        if not sink_node:
            raise NodeNotFound(f"Pipe '{self.name}' does not contain the '{self.sink_node}' node")
        return sink_node

    @property
    def stream_node(self):
        return self._stream_node

    @stream_node.setter
    def stream_node(self, node_name_or_id: Optional[str]) -> None:
        if not node_name_or_id:
            self._stream_node = None
            return
        node = self.pipeline.get_node(node_name_or_id)
        if not node:
            raise ValueError(f"Pipe '{self.name}' does not contain the '{node_name_or_id}' node")
        self._stream_node = node.id
        self.updated_at = datetime.now()

    def get_stream_node(self):
        stream_node = self.pipeline.get_node(self.stream_node)
        if not stream_node:
            raise NodeNotFound(f"Pipe '{self.name}' does not contain the '{self.stream_node}' node")
        return stream_node

    def get_dependencies(self):
        return self.pipeline.get_dependencies()

    def get_params(self) -> List[Dict[str, Any]]:
        if self.endpoint:
            return self.pipeline.get_params(self.endpoint)
        return []

    def get_schedule(self, workspace_id: Optional[str] = None, fallback_main: Optional[bool] = False) -> Dict[str, Any]:
        data_sink = None
        schedule: Dict[str, Any] = {}
        if self.pipe_type not in [PipeTypes.COPY, PipeTypes.DATA_SINK]:
            return schedule

        try:
            if not workspace_id:
                workspace_id = self.workspace_id if hasattr(self, "workspace_id") and self.workspace_id else None

            # Note: when we have different types of DataSink, we should support them
            # If Data Sink is not a Google Cloud Scheduler Sink,
            # we need to retrieve the linked sink because there can
            # be a GCS/S3 data sink that is scheduled
            data_sink = DataSink.get_by_resource_id(self.id, workspace_id, fallback_main)
            is_regular_data_sink = data_sink.service != DataConnectors.GCLOUD_SCHEDULER
            if is_regular_data_sink:
                data_sink = DataSink.get_by_resource_id(data_sink.id, workspace_id, fallback_main)

            if data_sink:
                data_sink_settings = data_sink.to_json().get("settings")
                schedule.update(data_sink_settings)

            return schedule
        except Exception:
            return schedule

    def is_node_endpoint(self, node_name_or_id: Optional[str]) -> bool:
        """
        Check if a node is the current endpoint
        """
        if not node_name_or_id:
            return False
        if not self.endpoint:
            return False
        endpoint_node = self.pipeline.get_node(self.endpoint)
        other_node = self.pipeline.get_node(node_name_or_id)
        return endpoint_node is not None and other_node is not None and endpoint_node.id == other_node.id

    def is_published(self) -> bool:
        return self.endpoint is not None

    def drop_node(self, node_name_or_id: Optional[str], edited_by: Optional[str]) -> None:
        """
        >>> pipe = Pipe('test', [{'name': 'test_0', 'sql': 'select * from test_ds'}])
        >>> pipe.endpoint = pipe.pipeline.last().id
        >>> node = pipe.append_node(PipeNode('test_1', 'select * from source_table'))
        >>> _ = pipe.append_node(PipeNode('test_2', 'select count() from node0'))
        >>> pipe.drop_node(node.id, '')
        >>> len(pipe.pipeline)
        2
        >>> pipe.drop_node(pipe.pipeline.nodes[0].id, '')  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
            ...
        EndpointNodesCantBeDropped: You cannot remove an endpoint node, unpublish the endpoint before
        """
        if self.is_node_endpoint(node_name_or_id):
            raise EndpointNodesCantBeDropped("You cannot remove an endpoint node, unpublish the endpoint before")
        self.pipeline.drop_node(node_name_or_id)
        if edited_by:
            self.edited_by = edited_by
        self.updated_at = datetime.now()

    def update_node(
        self,
        id_: str,
        sql: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        mode: Optional[str] = None,
        node_type: Optional[str] = None,
        edited_by: Optional[str] = None,
    ) -> PipeNode:
        """
        >>> pipe = Pipe('test', [{'name': 't0', 'sql': 'select * from test_ds'}])
        >>> node = pipe.update_node(pipe.pipeline.last().id, 'select * from test_ds_new')
        >>> node.sql
        'select * from test_ds_new'
        >>> _ = pipe.append_node(PipeNode('t1', 'select * from test'))
        >>> node = pipe.update_node(pipe.pipeline.last().id, 'select * from test_ds_new')
        >>> node.sql
        'select * from test_ds_new'
        """
        node = self.pipeline.update_node(id_, sql, name, description, mode, node_type)
        if edited_by:
            self.edited_by = edited_by
        self.updated_at = datetime.now()
        return node

    def set_node_mode(self, id_: str, mode: Optional[str], edited_by: Optional[str]) -> PipeNode:
        """
        >>> name = 'pipe_name'
        >>> t = TransformationPipeline()
        >>> t.append(PipeNode(f'{name}0', 'select * from source_table'))
        >>> node = t.set_node_mode(t.last().id, mode='append')
        >>> node.mode
        'append'
        >>> node = t.set_node_mode(t.last().id, mode=None)
        >>> node.mode
        """
        node = self.pipeline.set_node_mode(id_, mode)
        if edited_by:
            self.edited_by = edited_by
        self.updated_at = datetime.now()
        return node

    def set_node_tag(
        self, node_name_or_id: str, tag: Optional[str], value: str | bool, edited_by: Optional[str]
    ) -> PipeNode:
        if not tag:
            raise ValueError("Tag is not defined")
        node = self.pipeline.set_node_tag(node_name_or_id, tag, value)
        if edited_by:
            self.edited_by = edited_by
        self.updated_at = datetime.now()
        return node

    def drop_node_tag(self, node_name_or_id: str, tag: Optional[str], edited_by: Optional[str]) -> PipeNode:
        if not tag:
            raise ValueError("Tag is not defined")
        node = self.pipeline.drop_node_tag(node_name_or_id, tag)
        if edited_by:
            self.edited_by = edited_by
        self.updated_at = datetime.now()
        return node

    def change_node_position(self, node_name_or_id: str, new_position: int, edited_by: Optional[str]) -> None:
        node_found = self.pipeline.get_node(node_name_or_id)
        if node_found is None:
            raise ValueError("Node not found in Pipe")
        if new_position < 0 or new_position > len(self.pipeline.nodes):
            raise ValueError("Nodes can only be moved to positions already in use by other nodes.")
        self.pipeline.drop_node(node_name_or_id)
        self.pipeline.nodes.insert(new_position, node_found)
        if edited_by:
            self.edited_by = edited_by
        self.updated_at = datetime.now()

    def set_nodes(
        self,
        nodes: List[Dict[str, Any]],
        endpoint: Optional[str] = None,
        copy_node: Optional[str] = None,
        sink_node: Optional[str] = None,
        stream_node: Optional[str] = None,
    ) -> None:
        for x in nodes:
            provided_node_type = x.get("node_type", x.get("type"))

            if not x.get("name"):
                x["name"] = self.next_valid_name()
            if endpoint and x.get("id") == endpoint:
                x["node_type"] = PipeNodeTypes.ENDPOINT
            elif copy_node and x.get("id") == copy_node:
                x["node_type"] = PipeNodeTypes.COPY
            elif sink_node and x.get("id") == sink_node:
                x["node_type"] = PipeNodeTypes.DATA_SINK
            elif stream_node and x.get("id") == stream_node:
                x["node_type"] = PipeNodeTypes.STREAM
            elif x.get("materialized", None) is not None:
                x["node_type"] = PipeNodeTypes.MATERIALIZED
            elif provided_node_type is not None:
                x["node_type"] = provided_node_type.lower()
            else:
                x["node_type"] = PipeNodeTypes.STANDARD

            node = PipeNode.from_dict(x)

            self.pipeline.append(node)
            self.updated_at = datetime.now()

    def next_valid_name(self) -> str:
        return self.pipeline.next_valid_name(self.name)

    def append_node(self, node: PipeNode, edited_by: Optional[str] = None) -> PipeNode:
        self.pipeline.append(node)
        self.updated_at = datetime.now()
        if edited_by:
            self.edited_by = edited_by
        return self.pipeline.last()

    def has_node(self, name: Optional[str]) -> bool:
        return any(node.name == name for node in self.pipeline.nodes)

    def get_replacements(
        self,
        variables: Optional[Dict[str, Any]] = None,
        template_execution_results: Optional[TemplateExecutionResults] = None,
        secrets: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Returns the replacemnts for this pipe
        """
        if self.endpoint:
            return ReplacementsDict(
                {
                    self.name: self.id,
                    self.id: lambda: as_subquery(
                        self.pipeline.get_sql_for_node(
                            self.endpoint, variables, template_execution_results, secrets=secrets
                        )
                    ),
                }
            )

        for node in self.pipeline.nodes:
            if node.materialized:
                return ReplacementsDict({self.name: self.id, self.id: node.materialized})

        return {}

    def __repr__(self):
        return f"{self.__class__}({self.name})"

    @property
    def resource(self) -> str:
        return "Pipe"

    @property
    def resource_name(self) -> str:
        return "Pipe"

    def __eq__(self, other):
        """
        >>> nodes = [{'name': 'p0', 'sql': 'select 1'}]
        >>> p0 = Pipe('abcd', nodes)
        >>> p1 = Pipe('abcd', nodes, guid=p0.id)
        >>> p0 == p1
        True
        >>> p0 == None
        False
        >>> Pipe('abcd', nodes) == Pipe('abcd', nodes)
        True
        >>> Pipe('a', nodes, guid='uuuu') == Pipe('z', nodes, guid='uuuu')
        True
        >>> class F:
        ...    id = p0.id
        ...    name = 'abcd'
        >>> p0 == F()
        False
        """
        return (
            other is not None
            and type(self) == type(other)  # noqa: E721
            and (self.id == other.id or self.name == other.name)
        )

    @staticmethod
    def from_dict(t: Dict[str, Any]) -> "Pipe":
        pipe = Pipe(
            t["name"],
            nodes=t.get("nodes", None),
            description=t.get("description", None),
            guid=t["id"],
            endpoint=t.get("endpoint", None),
            copy_node=t.get("copy_node", None),
            sink_node=t.get("sink_node", None),
            stream_node=t.get("stream_node", None),
            workspace_id=t.get("workspace_id", None),
        )

        pipe.created_at = t.get("created_at", datetime.now())
        pipe.edited_by = t.get("edited_by", None)
        pipe.updated_at = t.get("updated_at", pipe.created_at)
        pipe.parent = t.get("parent")
        pipe.last_commit = t.get("last_commit", {})
        return pipe

    def to_dict(
        self, attrs: Optional[List[str]] = None, node_attrs: Optional[List[str]] = None, update_last_commit_status=False
    ) -> Dict[str, Any]:
        if not attrs:
            pipe: Dict[str, Any] = {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "endpoint": self.endpoint,
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "edited_by": self.edited_by,
                "parent": self.parent,
                "type": self.pipe_type,
                "workspace_id": self.workspace_id or "",
                "last_commit": {
                    "content_sha": self.last_commit.get("content_sha"),
                    "path": self.last_commit.get("path"),
                    "status": str(self.last_commit.get("status")),
                },
            }

            if self.pipe_type == PipeTypes.ENDPOINT:
                pipe["endpoint_charts"] = self.endpoint_charts

            if update_last_commit_status:
                pipe["last_commit"]["status"] = "changed"

            if self.sink_node:
                pipe.update(
                    {
                        "sink_node": self.sink_node,
                        "schedule": self.get_schedule(fallback_main=True),
                    }
                )
            if self.stream_node:
                pipe.update(
                    {
                        "stream_node": self.stream_node,
                    }
                )
            if self.copy_node:
                pipe.update(
                    {
                        "copy_node": self.copy_node,
                        "copy_target_datasource": self.copy_target_datasource,
                        "copy_target_workspace": self.copy_target_workspace,
                        "copy_mode": self.copy_mode or CopyModes.APPEND,
                        "schedule": self.get_schedule(fallback_main=True),
                    }
                )
            if (attrs and "nodes" in attrs) or not attrs or node_attrs:
                pipe["nodes"] = self.pipeline.to_dict(node_attrs=node_attrs)
        else:
            pipe = {}

            if "type" in attrs:
                pipe["type"] = self.pipe_type
            if self.pipe_type == PipeTypes.ENDPOINT and "endpoint_charts" in attrs:
                pipe["endpoint_charts"] = self.endpoint_charts
            for attr in attrs:
                try:
                    if attr == "schedule":
                        pipe["schedule"] = self.get_schedule(fallback_main=True)
                        continue
                    pipe[attr] = getattr(self, attr)
                except AttributeError:
                    pass
        return pipe

    def to_json(
        self,
        dependencies: bool = True,
        attrs: Optional[List[str]] = None,
        node_attrs: Optional[List[str]] = None,
        limited_representation: bool = False,
    ) -> Dict[str, Any]:
        """
        a json compatible version of the object
        """
        pipe = self.to_dict(attrs=attrs, node_attrs=node_attrs)
        if (attrs and "nodes" in attrs) or not attrs or node_attrs:
            pipe["nodes"] = self.pipeline.to_json(dependencies=dependencies, node_attrs=node_attrs)
        if "created_at" in pipe:
            pipe["created_at"] = str(pipe["created_at"])
        if "updated_at" in pipe:
            pipe["updated_at"] = str(pipe["updated_at"])

        if limited_representation:
            # TODO: For the limited representation we should change from a blacklist approach to a whitelist one
            if "edited_by" in pipe:
                pipe["edited_by"] = ""
            if "nodes" in pipe:
                for node in pipe["nodes"]:
                    node["sql"] = ""
                    if "dependencies" in node:
                        node["dependencies"] = []

        return pipe

    def to_hash(self) -> int:
        return hash(
            str(
                [
                    {
                        key: value
                        for key, value in iter(sorted(node.to_dict().items()))
                        if key
                        not in [
                            "created_at",
                            "updated_at",
                            "ignore_sql_errors",
                            "edited_by",
                            "id",
                            "materialized",
                            "tags",
                        ]
                    }
                    for node in self.pipeline.nodes
                ]
            )
        )

    @staticmethod
    def validate(pipe_obj: Dict[str, Any]) -> None:
        if "name" not in pipe_obj:
            raise PipeValidationException(
                "should have a name object, example object:\n" + json.dumps(EXAMPLE_PIPE_OBJECT, indent=4)
            )
        if "nodes" not in pipe_obj:
            raise PipeValidationException(
                "should have a nodes object, example object:\n" + json.dumps(EXAMPLE_PIPE_OBJECT, indent=4)
            )

        if not Resource.validate_name(pipe_obj["name"]):
            raise PipeValidationException(
                f'Invalid pipe name "{pipe_obj["name"]}". {Resource.name_help(pipe_obj["name"])}'
            )
        # check nodes have different names
        names = [x.get("name", None) for x in pipe_obj["nodes"]]
        if len(set(names)) != len(names):
            raise PipeValidationException("every node must have a unique name, there are nodes with the same name")

    def get_relevant_node(self):
        """
        >>> p = Pipe('test', [{'name': 't0', 'sql': 'SELECT 1', 'pipe_type': 'endpoint'}])
        >>> t = TransformationPipeline()
        >>> n0 = PipeNode('node0', 'select * from source_table')
        >>> t.append(n0)
        >>> t.endpoint = n0.id
        >>> p.pipeline = t
        >>> p.get_relevant_node() == n0
        True
        >>> p1 = Pipe('test1', [{'name': 't1', 'sql': 'SELECT 1', 'pipe_type': 'copy'}])
        >>> t1 = TransformationPipeline()
        >>> n1_0 = PipeNode('node0', 'select * from source_table')
        >>> t1.append(n1_0)
        >>> p1.pipeline = t1
        >>> p1.copy_node = n1_0.id
        >>> p1.get_relevant_node() == n1_0
        True
        >>> p2 = Pipe('test2', [{'name': 't2', 'sql': 'SELECT 1', 'pipe_type': 'sink'}])
        >>> t2 = TransformationPipeline()
        >>> n2_0 = PipeNode('node0', 'select * from source_table')
        >>> t2.append(n2_0)
        >>> p2.pipeline = t2
        >>> p2.sink_node = n2_0.id
        >>> p2.get_relevant_node() == n2_0
        True
        >>> p3 = Pipe('test3', [{'name': 't3', 'sql': 'SELECT 1', 'pipe_type': 'materialized'}])
        >>> t3 = TransformationPipeline()
        >>> n3_0 = PipeNode('node0', 'select * from source_table', materialized=True)
        >>> t3.append(n3_0)
        >>> p3.pipeline = t3
        >>> p3.get_relevant_node() == n3_0
        True
        >>> p4 = Pipe('test4', [{'name': 't4', 'sql': 'SELECT 1', 'pipe_type': 'default'}])
        >>> t4 = TransformationPipeline()
        >>> n4_0 = PipeNode('node0', 'select * from source_table')
        >>> t4.append(n4_0)
        >>> n4_1 = PipeNode('node1', 'select * from source_table')
        >>> t4.append(n4_1)
        >>> p4.pipeline = t4
        >>> p4.get_relevant_node() == n4_1
        True
        """
        if self.pipe_type == PipeTypes.ENDPOINT:
            return self.pipeline.get_node(self.pipeline.endpoint)
        if self.pipe_type == PipeTypes.COPY:
            return self.pipeline.get_node(self.copy_node)
        if self.pipe_type == PipeTypes.DATA_SINK:
            return self.pipeline.get_node(self.sink_node)
        if self.pipe_type == PipeTypes.STREAM:
            return self.pipeline.get_node(self.stream_node)
        if self.pipe_type == PipeTypes.MATERIALIZED:
            # Returns the first materialized node found.
            # Some customers (THN) have more than one materialized node per pipe
            # Take that into account when using this method
            materialized_node = None
            for node in self.pipeline.nodes:
                if node.materialized is not None and not materialized_node:
                    materialized_node = node
            return materialized_node
        if self.pipe_type == PipeTypes.DEFAULT:
            return self.pipeline.last()

        raise PipeValidationException(f"Pipe '{self.name}' type has not implemented how to retrieve its relevant node.")


if __name__ == "__main__":
    """
    t = TransformationPipeline()
    t.append('node0', 'select * from source_table')
    t.append('node1', 'select count() from node0')
    t.append('node2', 'select * from node1 where a = 1')
    print(t.get_sql_for_node('node2'))
    """
    t = TransformationPipeline()
    t.append(PipeNode("node1", "select * from test_00"))
    print(t.get_sql_for_node("node1"))  # noqa: T201
