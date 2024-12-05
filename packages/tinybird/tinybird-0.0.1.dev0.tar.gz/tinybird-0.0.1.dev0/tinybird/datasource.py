import base64
import re
import typing
from datetime import datetime
from typing import Any, Dict, List, Optional, Self, Tuple

from tinybird.datafile import ImportReplacements
from tinybird.matview_checks import EngineTypes
from tinybird.token_scope import scopes

from .ch import MAX_EXECUTION_TIME, ch_last_update_kafka_ops_log_async, ch_table_details_async, ch_table_schema_async
from .ch_utils.constants import LIVE_WS_NAME, MAIN_WS_NAME, SNAPSHOT_WS_NAME
from .ch_utils.engine import TableDetails
from .data_connector import DataConnector, DataLinker, DataSourceNotConnected
from .pipe import Pipe
from .resource import Resource
from .sql import schema_to_sql_columns

if typing.TYPE_CHECKING:
    from tinybird.hook import Hook
    from tinybird.tracker import HookLogEntry, OpsLogEntry
    from tinybird.user import User


REGEX_REMOVE_HTML = re.compile("<.?br.?>")


class DatasourceTypes:
    NDJSON = "ndjson"
    COPY = "copy"
    CSV = "csv"
    KAFKA = "kafka"
    SNOWFLAKE = "snowflake"
    BIGQUERY = "bigquery"
    S3 = "s3"
    S3_IAMROLE = "s3_iamrole"
    GCS = "gcs"
    DYNAMODB = "dynamodb"


DATASOURCE_CONNECTOR_TYPES = [
    DatasourceTypes.DYNAMODB,
    DatasourceTypes.GCS,
    DatasourceTypes.S3_IAMROLE,
    DatasourceTypes.S3,
    DatasourceTypes.SNOWFLAKE,
    DatasourceTypes.BIGQUERY,
]


class Datasource:
    """
    >>> datasource = Datasource('abcd', 'test')
    >>> datasource.get_replacements()
    {'test': 'abcd', 'test_quarantine': 'abcd_quarantine'}
    """

    def __init__(self, _id: str, name: str) -> None:
        self.id: str = _id
        self._name = name
        self.cluster: Optional[str] = None
        self.tags: Dict[str, Any] = {}
        self._hooks: List["Hook"] = []
        self.used_by: List[Pipe] = []
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.replicated: bool = False
        self.headers: Dict[str, Any] = {}
        self.shared_with: List[str] = []
        self.json_deserialization: List[Dict[str, Any]] = []
        self.ignore_paths: List[str] = []
        self._description = ""
        self.data_linker: Optional[DataLinker] = None
        self.engine: Dict[str, str] = {}
        self.service: Optional[str] = None
        self.service_conf: Optional[Dict[str, Any]] = None
        self.version = None  # TODO: This is not being used. Should we remove it?
        self.project = None  # TODO: Is this being used somewhere?
        self.last_commit: Dict[str, Any] = {"content_sha": "", "status": "ok", "path": ""}
        self.errors_discarded_at: Optional[datetime] = None

    def get_release_replacements(
        self,
        workspace: Optional["User"] = None,
        origin_workspace: Optional["User"] = None,
        main_workspace: Optional["User"] = None,
    ) -> Dict[str | Tuple[str, str], str]:
        result: Dict[str | Tuple[str, str], str] = dict()
        if not workspace:
            return result
        if main_workspace:
            workspace = main_workspace
        for release in workspace.get_releases():
            if ds := release.get_datasource(self.name):
                result[(f"v{release.semver.replace('.', '_').replace('-', '_')}", ds.name)] = ds.id
                result[(f"v{release.semver.replace('.', '_').replace('-', '_')}", ds.name + "_quarantine")] = (
                    ds.id + "_quarantine"
                )
                if release.is_live:
                    result.update({(LIVE_WS_NAME, ds.name): ds.id})

        if not origin_workspace:
            return result

        if (branch_release := origin_workspace.current_release) and (ds := branch_release.get_datasource(self.name)):
            result.update({(LIVE_WS_NAME, ds.name): ds.id})

        if ds := origin_workspace.get_datasource(self.name):
            result.update({(MAIN_WS_NAME, self.name): ds.id})
        return result

    def get_replacements(
        self,
        staging_table: bool = False,
        workspace: Optional["User"] = None,
        origin_workspace: Optional["User"] = None,
        main_workspace: Optional["User"] = None,
        release_replacements: bool = False,
    ):
        """
        return the replacements for this datasource
        """
        table_id = f"{self.id}_staging" if staging_table and self.tags.get("staging", False) else self.id
        release_replacements_dict = (
            self.get_release_replacements(workspace, origin_workspace, main_workspace) if release_replacements else {}
        )
        return {self.name: table_id, self.name + "_quarantine": self.id + "_quarantine", **release_replacements_dict}

    def __repr__(self):
        return f"{self.__class__}({self.id}/{self.name})"

    def install_hook(self, hook: "Hook"):
        self._hooks.append(hook)
        return hook

    def uninstall_hook(self, hook: "Hook"):
        self._hooks.remove(hook)

    @property
    def hooks(self):
        return self._hooks

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    def hook_log(self) -> List["HookLogEntry"]:
        log: List[HookLogEntry] = []
        for h in self._hooks:
            for hook_log in h.log:
                log.append(hook_log)
        return log

    def operations_log(self) -> List["OpsLogEntry"]:
        log: List[OpsLogEntry] = []
        for h in self._hooks:
            for hook_log in h.ops_log:
                log.append(hook_log)
        return log

    @property
    def resource(self) -> str:
        return "Datasource"

    @property
    def resource_name(self) -> str:
        return "Data Source"

    @property
    def database(self) -> Optional[str]:
        return None

    def get_dependent_join_datasources(self) -> List[Dict[str, str]]:
        dependent_datasources = self.tags.get("dependent_datasources", {})

        return [
            {"datasource": datasource, "workspace": value.get("workspace")}
            for datasource, value in dependent_datasources.items()
            if value.get("engine") == EngineTypes.JOIN
        ]

    def __eq__(self, other):
        """
        >>> ds0 = Datasource('abcd', 'foo')
        >>> ds1 = Datasource('abcd', 'foo')
        >>> ds0 == ds1
        True
        >>> ds0 == None
        False
        >>> Datasource('abcd', 'foo') == Datasource('abcd', 'bar')
        True
        >>> Datasource('abcd', 'foo') == Datasource('zzzz', 'foo')
        True
        >>> class F:
        ...    id = 'abcd'
        ...    name = 'foo'
        >>> ds0 == F()
        False
        """
        return other is not None and isinstance(self, type(other)) and (self.id == other.id or self.name == other.name)

    def touch(self):
        self.updated_at = datetime.now()

    @staticmethod
    def from_dict(t: Dict[str, Any]) -> "Datasource":
        ds = Datasource(t["id"], t["name"])
        ds._load_rest_of_content_from_dict(t)
        return ds

    @staticmethod
    def _remove_html_br(string: str) -> str:
        # Silly and simple implementation to remove HTML markup
        """
        >>> Datasource._remove_html_br('this is some html<br>')
        'this is some html'
        >>> Datasource._remove_html_br('this is some html<br/>')
        'this is some html'
        >>> Datasource._remove_html_br('this is some html</br>')
        'this is some html'
        """
        return REGEX_REMOVE_HTML.sub("", string)

    def _load_rest_of_content_from_dict(self, t: Dict[str, Any]) -> "Self":
        self.cluster = t.get("cluster", None)
        self.created_at = t.get("created_at", datetime.now())
        self.updated_at = t.get("updated_at", self.created_at)
        self.tags = t.get("tags", {})
        self.replicated = t.get("replicated", False)
        self.version = t.get("version")
        self.project = t.get("project")
        self.headers = t.get("headers", {})
        self.json_deserialization = t.get("json_deserialization", [])
        self.ignore_paths = t.get("ignore_paths", [])
        self._description = Datasource._remove_html_br(t.get("description", ""))
        self.shared_with = t.get("shared_with", [])
        self.engine = t.get("engine", {})
        self.service = t.get("service", None)
        self.service_conf = t.get("service_conf", None)
        self.last_commit = t.get("last_commit", {})
        self.errors_discarded_at = t.get("errors_discarded_at", None)
        return self

    def get_data_linker(self) -> Optional[DataLinker]:
        return DataLinker.get_by_datasource_id(self.id)

    def get_service_conf(self) -> Optional[Dict[str, Any]]:
        if not self.service_conf:
            return None

        # BigQuery is the only service that has a different configuration
        # For the rest, use the data linker.
        if self.service != "bigquery":
            return None

        SERVICE_REPLACEMENTS: Dict[str, str] = {
            "service": "import_service",
            "connection": "import_connection",
            "mode": "import_strategy",
            "cron": "import_schedule",
            "sql_query": "import_query",
            "query": "import_query",
            "external_data_source": "import_external_datasource",
            "bucket_uri": "import_bucket_uri",
            "from_time": "import_from_timestamp",
        }

        conf: Dict[str, Any] = {"import_service": self.service}
        conf.update(
            dict(
                (SERVICE_REPLACEMENTS[k.lower()], v)
                for k, v in self.service_conf.items()
                if SERVICE_REPLACEMENTS.get(k.lower(), "")
            )
        )

        # Querys are stored in b64
        query: Optional[str] = conf.get("import_query", None)
        if query:
            try:
                conf["import_query"] = base64.standard_b64decode(query.encode()).decode("utf-8")
            except (
                UnicodeDecodeError
            ):  # First versions didn't encode queries in base64 so this is to add backwards-compatibility
                pass

        return conf

    @property
    def json_deserialization(self) -> List[Dict[str, Any]]:
        try:
            if not self.data_linker:
                self.data_linker = self.get_data_linker()
                self.__json_deserialization = self.data_linker.settings["json_deserialization"]  # type: ignore
            return self.__json_deserialization
        except Exception:
            return self.__json_deserialization

    @json_deserialization.setter
    def json_deserialization(self, val):
        self.__json_deserialization = val

    @property
    def datasource_type(self):
        if self.service:
            return self.service
        if self.tags.get("source_copy_pipes", None):
            return DatasourceTypes.COPY
        if self.json_deserialization:
            return DatasourceTypes.NDJSON
        return DatasourceTypes.CSV

    def to_dict(self, include_internal_data=False, update_last_commit_status=False):
        obj: Dict[str, Any] = {
            "id": self.id,
            "name": self.name,
            "cluster": self.cluster,
            "tags": self.tags,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "replicated": self.replicated,
            "version": 0,
            "project": None,
            "headers": self.headers,
            "shared_with": self.shared_with,
            "json_deserialization": self.json_deserialization,
            "ignore_paths": self.ignore_paths,
            "engine": self.engine,
            "description": self.description,
            "used_by": [{"id": x.id, "name": x.name} for x in self.used_by],
            "service": self.service,
            "service_conf": self.service_conf,
            "last_commit": {
                "content_sha": self.last_commit.get("content_sha", ""),
                "status": self.last_commit.get("status", "ok"),
                "path": self.last_commit.get("path", ""),
            },
            "errors_discarded_at": self.errors_discarded_at,
        }

        if update_last_commit_status:
            obj["last_commit"]["status"] = "changed"

        try:
            data_linker: Optional[DataLinker] = self.get_data_linker()
            if data_linker:
                obj.update(
                    {
                        **data_linker.service_settings,
                        "service": data_linker.service,
                        "connector": data_linker.data_connector_id,
                    }
                )
        except Exception:
            pass
        return obj

    def to_json(self, include_internal_data=False, attrs=None):
        """
        a json compatible version of the object
        """
        d = self.to_dict(include_internal_data)
        d["created_at"] = str(d["created_at"])
        d["updated_at"] = str(d["updated_at"])
        d["errors_discarded_at"] = str(d["errors_discarded_at"]) if d.get("errors_discarded_at") else None
        d["replicated"] = bool(d["replicated"])

        if d.get("service", None):
            d["type"] = d["service"]
        elif self.json_deserialization:
            d["type"] = DatasourceTypes.NDJSON
        else:
            d["type"] = DatasourceTypes.CSV

        if "json_deserialization" in d:
            del d["json_deserialization"]
        if "ignore_paths" in d:
            del d["ignore_paths"]
        if d.get("service", None) is None:
            del d["service"]
            del d["service_conf"]

        if attrs:
            result = {}
            for attr in attrs:
                if d.get(attr, None):
                    result[attr] = d.get(attr, None)
            d = result
        return d

    async def last_update(self, pu, u):
        obj = self.to_json()
        updated_at = obj["updated_at"]
        if obj.get("service", None) != DatasourceTypes.KAFKA:
            return updated_at
        kafka_last_update = await ch_last_update_kafka_ops_log_async(
            pu["database_server"], pu["database"], u.id, self.id
        )
        no_rows = kafka_last_update is None or kafka_last_update == "1970-01-01 00:00:00"
        return updated_at.split(".")[0] if no_rows else kafka_last_update

    async def table_metadata(
        self,
        u: "User",
        include_default_columns: bool = False,
        include_jsonpaths: bool = False,
        include_stats: bool = False,
        include_meta_columns: bool = True,
        include_engine: bool = False,
        include_indices: bool = False,
        max_execution_time: Optional[int] = MAX_EXECUTION_TIME,
    ) -> Tuple[TableDetails, List[Dict[str, Any]]]:
        return await self._table_metadata(
            u.database_server,
            u.database,
            include_default_columns=include_default_columns,
            include_jsonpaths=include_jsonpaths,
            include_stats=include_stats,
            include_engine=include_engine,
            include_meta_columns=include_meta_columns,
            include_indices=include_indices,
            max_execution_time=max_execution_time,
        )

    async def _table_metadata(
        self,
        database_server: str,
        database: str,
        include_default_columns: bool = False,
        include_jsonpaths: bool = False,
        include_stats: bool = False,
        include_meta_columns: bool = True,
        include_engine: bool = True,
        include_indices: bool = False,
        max_execution_time: Optional[int] = MAX_EXECUTION_TIME,
    ) -> Tuple[TableDetails, List[Dict[str, Any]]]:
        schema = await ch_table_schema_async(
            self.id,
            database_server,
            database,
            include_default_columns=include_default_columns,
            include_meta_columns=include_meta_columns,
            max_execution_time=max_execution_time,
        )
        if not schema:
            raise ValueError("couldn't find table")
        if (
            (not self.engine or self.engine.get("engine", None) is None)
            or include_stats
            or include_engine
            or include_indices
        ):
            # this call can be slowish, that's why it's cached in self.engine on data source creation
            if include_engine:
                engine = await ch_table_details_async(
                    self.id,
                    database_server,
                    database=database,
                    include_stats=False,
                    max_execution_time=max_execution_time,
                )
            else:
                engine = await ch_table_details_async(
                    self.id,
                    database_server,
                    database=database,
                    include_stats=True,
                    max_execution_time=max_execution_time,
                )
        else:
            engine = TableDetails(self.engine)

        if include_jsonpaths and self.json_deserialization:
            for column in schema:
                column["jsonpath"] = None
                for j in self.json_deserialization:
                    if j["name"] == column["name"]:
                        column["jsonpath"] = j.get("jsonpath", None)
                        break
        return engine, schema

    async def to_datafile(
        self, workspace: "User", workspaces_accessible_by_user: List[Dict[str, Any]], filtering_tags: List[str]
    ) -> str:
        table_details: TableDetails
        schema: List[Dict[str, Any]]
        table_details, schema = await self.table_metadata(
            workspace,
            include_default_columns=True,
            include_jsonpaths=True,
            include_meta_columns=False,
            include_engine=True,
            include_indices=True,
        )

        doc: List[str] = []

        created_by_pipe: Optional[str] = self.tags.get("created_by_pipe", None)
        if created_by_pipe:
            pipe = workspace.get_pipe(created_by_pipe)
            if pipe:
                doc.append(f"# Data Source created from Pipe '{pipe.name}'")
            else:
                doc.append(f"# Data Source created from Pipe '{created_by_pipe}'")

        if workspace:
            tokens = workspace.get_access_tokens_for_resource(self.id, scopes.DATASOURCES_APPEND)
            for t in tokens:
                doc.append(f'TOKEN "{t.name}" APPEND\n')

        if self.description:
            doc.append("DESCRIPTION >")
            doc.append(f"    {self.description}")

        if filtering_tags:
            doc.append(f'TAGS "{", ".join(filtering_tags)}"')

        doc += ["", "SCHEMA >"]
        columns = schema_to_sql_columns(schema)
        doc.append(",\n".join(map(lambda x: f"    {x}", columns)))
        doc.append("")
        doc.append(table_details.to_datafile())
        doc.append("")

        indexes = table_details.indexes
        if len(indexes):
            doc += ["", "INDEXES >"]
            doc.append(",\n".join(map(lambda index: f"    {index.to_datafile()}", indexes)))
            doc.append("")

        # Service imports
        service_conf = self.get_service_conf()
        if service_conf:
            for key, value in service_conf.items():
                quote = "'"
                if "\n" in value:
                    key = f"{key} >\n"
                if "'" in value:
                    quote = '"'
                doc.append(f"{key.upper()} {quote}{value}{quote}")
            doc.append("")

        try:
            data_linker: Optional[DataLinker] = self.get_data_linker()
            data_connector: Optional[DataConnector] = None
            if data_linker and data_linker.data_connector_id:
                data_connector = DataConnector.get_by_id(data_linker.data_connector_id)

            if self.service in [
                DatasourceTypes.DYNAMODB,
                DatasourceTypes.GCS,
                DatasourceTypes.S3_IAMROLE,
                DatasourceTypes.S3,
                DatasourceTypes.SNOWFLAKE,
            ]:
                doc.append(f"IMPORT_SERVICE '{self.service}'")
                if data_connector:
                    doc.append(f"IMPORT_CONNECTION_NAME '{data_connector.name}'")

                if data_linker:
                    for k, v in data_linker.settings.items():
                        quote = "'"
                        datafile_key = ImportReplacements.get_datafile_param_for_linker_param(self.service, k)
                        if not datafile_key:
                            continue
                        datafile_value = ImportReplacements.get_datafile_value_for_linker_value(self.service, k, v)
                        if not datafile_value:
                            continue
                        if "\n" in datafile_value:
                            datafile_key = f"{datafile_key} >\n"
                        if "'" in datafile_value:
                            quote = '"'
                        doc.append(f"{datafile_key.upper()} {quote}{datafile_value}{quote}")
            elif data_connector and data_linker:
                doc.append(f"KAFKA_CONNECTION_NAME '{data_connector.name}'")
                for key, value in data_linker.service_settings.items():
                    doc.append(f"{key.upper()} '{value}'")
            doc.append("")
        except DataSourceNotConnected:
            pass

        if self.shared_with:
            workspace_names: List[str] = []
            for shared_to in self.shared_with:
                workspace_name = next((w["name"] for w in workspaces_accessible_by_user if w["id"] == shared_to), None)
                if workspace_name:
                    workspace_names.append(workspace_name)

            if workspace_names:
                doc += ["", "SHARED_WITH >"]
                doc.append("\n".join(map(lambda x: f"    {x}", workspace_names)))

        return "\n".join(doc)

    def to_hash(self, tables_metadata) -> int:
        return tables_metadata[self.id].hash

    def get_cached_source_csv_headers(self) -> Dict[str, Any]:
        """
        >>> datasource = Datasource('abcd', 'test')
        >>> datasource.get_cached_source_csv_headers()

        >>> datasource.cache_source_csv_headers(['header1','header2'], 'thehash')
        >>> datasource.get_cached_source_csv_headers()
        {'header': ['header1', 'header2'], 'header_hash': 'thehash'}
        """
        return self.headers.get("dialect", None)

    def cache_source_csv_headers(self, header: str, header_hash: str) -> None:
        self.headers["dialect"] = {"header": header, "header_hash": header_hash}

    def cache_delimiter(self, delimiter: str) -> None:
        """
        >>> datasource = Datasource('abcd', 'test')
        >>> datasource.headers.get('cached_delimiter', None)

        >>> datasource.cache_delimiter(',')
        >>> datasource.headers.get('cached_delimiter', None)
        ','
        >>> datasource.cache_delimiter(';')
        >>> datasource.headers.get('cached_delimiter', None)
        ','
        """
        if self.headers.get("cached_delimiter", None) is None:
            self.headers["cached_delimiter"] = delimiter

    @property
    def is_read_only(self) -> bool:
        return False

    @classmethod
    def duplicate_datasource(self, datasource):
        prefix = datasource.id.split("_")[0]
        new_datasource = Datasource(Resource.guid(prefix), datasource.name)
        new_datasource.cluster = datasource.cluster
        new_datasource.replicated = datasource.replicated
        new_datasource.tags = datasource.tags.copy()
        new_datasource.json_deserialization = datasource.json_deserialization.copy()

        return new_datasource

    def get_shared_with(self):
        return self.shared_with


class SharedDSDistributedMode:
    read_only = "read_only"


class SharedDatasource(Datasource):
    """
    >>> sd = SharedDatasource('id', 'workspace_id', 'workspace_name', 'ds_database', 'ds_name', 'ds_description')
    >>> sd.name
    'workspace_name.ds_name'
    >>> sd.name = 'new_name'
    Traceback (most recent call last):
    ...
    Exception: Datasource name for a SharedDatasource can't be changed
    >>> sd.created_at = '2020-01-01'  # overwrite to make testing easier
    >>> sd.updated_at = '2020-01-01'  # overwrite to make testing easier
    >>> sd.to_json()
    {'id': 'id', 'name': 'workspace_name.ds_name', 'cluster': None, 'tags': {}, 'created_at': '2020-01-01', 'updated_at': '2020-01-01', 'replicated': False, 'version': 0, 'project': None, 'headers': {}, 'engine': {}, 'description': 'ds_description', 'used_by': [], 'last_commit': {'content_sha': '', 'status': 'ok', 'path': ''}, 'errors_discarded_at': None, 'shared_from': {'original_workspace_name': 'workspace_name', 'original_workspace_id': 'workspace_id', 'original_ds_name': 'ds_name', 'original_ds_description': 'ds_description', 'distributed_mode': None}, 'type': 'csv'}
    >>> sd.to_json(include_internal_data=True)
    {'id': 'id', 'name': 'workspace_name.ds_name', 'cluster': None, 'tags': {}, 'created_at': '2020-01-01', 'updated_at': '2020-01-01', 'replicated': False, 'version': 0, 'project': None, 'headers': {}, 'shared_with': [], 'engine': {}, 'description': 'ds_description', 'used_by': [], 'last_commit': {'content_sha': '', 'status': 'ok', 'path': ''}, 'errors_discarded_at': None, 'shared_from': {'original_workspace_name': 'workspace_name', 'original_workspace_id': 'workspace_id', 'original_ds_name': 'ds_name', 'original_ds_description': 'ds_description', 'distributed_mode': None, 'original_ds_database': 'ds_database'}, 'type': 'csv'}
    >>> sd.get_replacements()
    {'id': ('ds_database', 'id'), ('workspace_name', 'ds_name'): ('ds_database', 'id'), ('workspace_name', 'ds_name_quarantine'): ('ds_database', 'id_quarantine')}
    """

    def __init__(
        self,
        _id: str,
        workspace_id: str,
        workspace_name: str,
        ds_database: str,
        ds_name: str,
        ds_description: str,
        distributed_mode: Optional[str] = None,
    ) -> None:
        super().__init__(_id, self._generate_shared_data_source_name(workspace_name, ds_name))

        self.original_workspace_name = workspace_name
        self.original_workspace_id = workspace_id
        self.original_ds_name = ds_name
        self.original_ds_database = ds_database
        self.original_ds_description = ds_description
        self.distributed_mode = distributed_mode

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, _):
        raise Exception("Datasource name for a SharedDatasource can't be changed")

    @property
    def description(self):
        return self.original_ds_description

    @description.setter
    def description(self, _):
        raise Exception("Datasource description for a SharedDatasource can't be changed")

    @property
    def database(self):
        return None if self.distributed_mode else self.original_ds_database

    def get_replacements(
        self,
        staging_table: bool = False,
        workspace: Optional["User"] = None,
        origin_workspace: Optional["User"] = None,
        main_workspace: Optional["User"] = None,
        release_replacements: bool = False,
    ):
        table_id = f"{self.id}_staging" if staging_table and self.tags.get("staging", False) else self.id
        if self.distributed_mode:
            return {
                self.name: table_id,
                self.name + "_quarantine": self.id + "_quarantine",
                (self.original_workspace_name, self.original_ds_name): table_id,
                (self.original_workspace_name, f"{self.original_ds_name}_quarantine"): self.id + "_quarantine",
            }
        else:
            return {
                table_id: (self.original_ds_database, table_id),
                (self.original_workspace_name, self.original_ds_name): (self.original_ds_database, table_id),
                (self.original_workspace_name, f"{self.original_ds_name}_quarantine"): (
                    self.original_ds_database,
                    f"{self.id}_quarantine",
                ),
            }

    def to_dict(self, include_internal_data=False, update_last_commit_status=False):
        base_dict = super().to_dict(update_last_commit_status=update_last_commit_status)
        shared_from_content = {
            "original_workspace_name": self.original_workspace_name,
            "original_workspace_id": self.original_workspace_id,
            "original_ds_name": self.original_ds_name,
            "original_ds_description": self.original_ds_description,
            "distributed_mode": self.distributed_mode,
        }
        if include_internal_data:
            shared_from_content["original_ds_database"] = self.original_ds_database
        else:
            del base_dict["shared_with"]
        base_dict.update({"shared_from": shared_from_content})
        return base_dict

    @staticmethod
    def from_dict(t: Dict[str, Any]) -> "SharedDatasource":
        ds = SharedDatasource(
            t["id"],
            t["shared_from"]["original_workspace_id"],
            t["shared_from"]["original_workspace_name"],
            t["shared_from"]["original_ds_database"],
            t["shared_from"]["original_ds_name"],
            t["shared_from"].get("original_ds_description", ""),
            t["shared_from"].get("distributed_mode", None),
        )
        return ds._load_rest_of_content_from_dict(t)

    async def table_metadata(
        self,
        u: "User",
        include_default_columns: bool = False,
        include_jsonpaths: bool = False,
        include_stats: bool = False,
        include_meta_columns: bool = True,
        include_engine: bool = False,
        include_indices: bool = False,
        max_execution_time: Optional[int] = MAX_EXECUTION_TIME,
    ) -> Tuple[TableDetails, List[Dict[str, Any]]]:
        return await self._table_metadata(
            u.database_server,
            u.database if self.distributed_mode else self.original_ds_database,
            include_default_columns=include_default_columns,
            include_jsonpaths=include_jsonpaths,
            include_stats=include_stats,
            include_meta_columns=include_meta_columns,
            include_indices=include_indices,
            max_execution_time=max_execution_time,
        )

    @staticmethod
    def _generate_shared_data_source_name(origin_workspace_name: str, origin_datasource_name: str) -> str:
        return f"{origin_workspace_name}.{origin_datasource_name}"

    def update_shared_name(self, origin_workspace_name: str, origin_datasource_name: str):
        self._name = self._generate_shared_data_source_name(origin_workspace_name, origin_datasource_name)
        self.original_workspace_name = origin_workspace_name
        self.original_ds_name = origin_datasource_name

    def update_shared_description(self, origin_datasource_description):
        self.original_ds_description = origin_datasource_description

    @property
    def is_read_only(self) -> bool:
        return True


class BranchSharedDatasource(SharedDatasource):
    def get_replacements(
        self,
        staging_table: bool = False,
        workspace: Optional["User"] = None,
        origin_workspace: Optional["User"] = None,
        main_workspace: Optional["User"] = None,
        release_replacements: bool = False,
    ):
        """
        return the replacements for this datasource
        """
        table_id = f"{self.id}_staging" if staging_table and self.tags.get("staging", False) else self.id
        return {
            (self.original_workspace_name, self.original_ds_name): table_id,
            (self.original_workspace_name, self.original_ds_name + "_quarantine"): self.id + "_quarantine",
        }

    @staticmethod
    def from_dict(t: Dict[str, Any]) -> "BranchSharedDatasource":
        ds = BranchSharedDatasource(
            t["id"],
            t["shared_from"]["original_workspace_id"],
            t["shared_from"]["original_workspace_name"],
            t["shared_from"]["original_ds_database"],
            t["shared_from"]["original_ds_name"],
            t["shared_from"].get("original_ds_description", ""),
        )
        return ds._load_rest_of_content_from_dict(t)

    async def table_metadata(
        self,
        u: "User",
        include_default_columns: bool = False,
        include_jsonpaths: bool = False,
        include_stats: bool = False,
        include_meta_columns: bool = True,
        include_engine: bool = False,
        include_indices: bool = False,
        max_execution_time: Optional[int] = MAX_EXECUTION_TIME,
    ) -> Tuple[TableDetails, List[Dict[str, Any]]]:
        return await self._table_metadata(
            u.database_server,
            u.database if self.distributed_mode or u.is_branch else self.original_ds_database,
            include_default_columns=include_default_columns,
            include_jsonpaths=include_jsonpaths,
            include_stats=include_stats,
            include_meta_columns=include_meta_columns,
            max_execution_time=max_execution_time,
            include_engine=include_engine,
            include_indices=include_indices,
        )

    def get_data_linker(self):
        raise DataSourceNotConnected


class BranchDatasource(Datasource):
    def __init__(self, _id, name, origin_database):
        super().__init__(_id, name)
        self.origin_database = origin_database

    def get_replacements(
        self,
        staging_table: bool = False,
        workspace: Optional["User"] = None,
        origin_workspace: Optional["User"] = None,
        main_workspace: Optional["User"] = None,
        release_replacements: bool = False,
    ):
        repl = super().get_replacements(
            staging_table=staging_table,
            workspace=workspace,
            origin_workspace=origin_workspace,
            main_workspace=main_workspace,
            release_replacements=release_replacements,
        )
        if origin_workspace:
            if ds := origin_workspace.get_datasource(self.name):
                repl.update({(MAIN_WS_NAME, self.name): (self.origin_database, ds.id)})
            else:
                repl.update({(MAIN_WS_NAME, self.name): (self.origin_database, self.id)})

            if (
                workspace
                and (snapshot := workspace.get_snapshot())
                and (snapshot_ds := snapshot.get_datasource(self.name))
            ):
                repl.update({(SNAPSHOT_WS_NAME, self.name): snapshot_ds.id})
        return repl

    def to_dict(self, include_internal_data=False, update_last_commit_status=False):
        base_dict = super().to_dict(
            include_internal_data=include_internal_data, update_last_commit_status=update_last_commit_status
        )
        base_dict.update({"origin_database": self.origin_database})
        return base_dict

    @staticmethod
    def from_dict(t: Dict[str, Any]) -> "BranchDatasource":
        ds = BranchDatasource(t["id"], t["name"], t.get("origin_database", ""))
        return ds._load_rest_of_content_from_dict(t)


class KafkaBranchDatasource(BranchDatasource):
    def __init__(self, _id, name, origin_database, origin_connector_id):
        super().__init__(_id, name, origin_database)
        self.origin_connector_id = origin_connector_id

    def to_dict(self, include_internal_data=False, update_last_commit_status=False):
        base_dict = super().to_dict(
            include_internal_data=include_internal_data, update_last_commit_status=update_last_commit_status
        )
        base_dict.update({"origin_connector_id": self.origin_connector_id})
        return base_dict

    @staticmethod
    def from_dict(t: Dict[str, Any]) -> "KafkaBranchDatasource":
        ds = KafkaBranchDatasource(t["id"], t["name"], t["origin_database"], t["origin_connector_id"])
        return ds._load_rest_of_content_from_dict(t)

    def get_data_linker(self):
        raise DataSourceNotConnected


def get_datasources_internal_ids(datasources: List[Datasource], default_database: str) -> List[Tuple[str, str]]:
    db_tables = [
        (ds.database if isinstance(ds, SharedDatasource) and ds.database else default_database, ds.id)
        for ds in datasources
    ]
    db_tables = list(dict.fromkeys(db_tables))
    return db_tables


def get_trigger_datasource(workspace, left_table):
    if not left_table:
        return ""

    if len(left_table) == 1:
        left_table = left_table[0]
    else:
        left_table = left_table[1]

    ds = workspace.get_datasource(left_table, include_read_only=True)
    if not ds:
        return ""
    return ds.to_json(attrs=["id", "name"])
