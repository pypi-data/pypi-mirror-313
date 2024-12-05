import logging
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from tinybird.ch_utils.engine import TableDetails
from tinybird.datasource import Datasource
from tinybird.iterating.hook_utils import allow_drop_table
from tinybird.views.api_errors.datasources import ClientErrorBadRequest

from .blocks import Block
from .ch import (
    ERROR_COLUMNS,
    MAX_COLUMNS_SCHEMA,
    CHTable,
    CSVInfo,
    HTTPClient,
    QuarantineCHTable,
    ch_drop_table_with_fallback,
    ch_table_exists_sync,
    ch_table_list_exist,
)
from .ch_utils.exceptions import CHException
from .csv_processing_queue import CsvChunkQueueRegistry
from .csv_tools import csv_from_python_object
from .limits import Limit
from .matview_checks import check_if_engine_has_aggregating_functions
from .sql import TableIndex, TableProjection, parse_table_structure, schema_to_sql_columns
from .syncasync import sync_to_async
from .user import User as Workspace
from .user import Users as Workspaces


async def column_replace_default_expression(workspace: Workspace, column: Dict[str, Any]) -> None:
    """
    For values of MATERIALIZED, DEFAULT AND ALIAS we need to verify that they don't access any forbidden tables
    Note that the values could be both a function or a scalar subquery:
        `hash` UInt64 MATERIALIZED bitOr(bitShiftLeft(property_id::UInt64, 32), fingerprint::UInt64)
        `three` String ALIAS event_time IN (SELECT event_time FROM visits)
    Also currently ALIAS is not supported by the parser, but we accept it here anyway since the process is the same
    """
    if not column["default_value"]:
        return

    default_value = column["default_value"]
    lower_default = default_value.strip().lower()
    if not (
        lower_default.startswith("materialized")
        or lower_default.startswith("default")
        or lower_default.startswith("alias")
    ):
        return default_value

    default_type = default_value.split()[0]
    q = "select " + default_value.strip()[len(default_type) :]
    q = Workspaces.replace_tables(workspace, q)
    column["default_value"] = q.replace("SELECT", default_type, 1)


async def create_table_from_schema(
    workspace: Workspace,
    datasource: Datasource,
    schema: str,
    engine: Optional[Any] = None,
    create_quarantine: bool = True,
    options: Optional[Dict[str, Any]] = None,
    not_exists: bool = False,
    quarantine_engine: Optional[str] = None,
    indexes: Optional[List[TableIndex]] = None,
    projections: Optional[List[TableProjection]] = None,
):
    """
    Validates schema and creates a clickhouse compatible table.
    It also creates a quarantine table based on create_quarantine.
    """
    options = options or {}
    params: Dict[str, Any] = workspace.ddl_parameters(skip_replica_down=True)

    async def _create_table_in_ch(
        _columns: List[Dict[str, Any]],
        _table_name: str,
        cluster: Optional[str],
        engine: Any,
        indexes: Optional[List[TableIndex]] = None,
        projections: Optional[List[TableProjection]] = None,
        is_quarantine: bool = False,
    ):
        try:
            ch_table = QuarantineCHTable if is_quarantine else CHTable
            table = ch_table(
                _columns,
                cluster=cluster,
                engine=engine,
                storage_policy=workspace.storage_policy,
                not_exists=not_exists,
                indexes=indexes,
                projections=projections,
            )
            check_if_engine_has_aggregating_functions(table.engine, _columns)
            q = table.as_sql(workspace["database"], _table_name)
        except Exception as e:
            raise ValueError(f"Invalid data source structure: {e}")

        client = HTTPClient(workspace["database_server"], database=workspace["database"])
        return await client.query(q, read_only=False, **params)

    try:
        columns = parse_table_structure(schema)
        # replace table in columns with default values.
        for column in columns:
            await column_replace_default_expression(workspace, column)
    except Exception as e:
        raise ValueError(f"Invalid data source structure: {e}")

    for hook in datasource.hooks:
        hook.ops_log_options = options
        before_create = sync_to_async(hook.before_create)
        await before_create(datasource)
    await _create_table_in_ch(
        columns,
        datasource.id,
        workspace.cluster,
        engine,
        indexes=indexes,
        projections=projections,
    )

    if create_quarantine:
        safe_columns = CSVInfo.convert_columns_to_safe_types(columns, include_fallback=False)
        await _create_table_in_ch(
            ERROR_COLUMNS + safe_columns,
            f"{datasource.id}_quarantine",
            workspace.cluster,
            engine=quarantine_engine,
            is_quarantine=True,
        )
    for hook in datasource.hooks:
        hook.ops_log_options = options
        after_create = sync_to_async(hook.after_create)
        await after_create(datasource)


async def alter_index_operations(index_changes: Dict[str, List[TableIndex]]) -> List[str]:
    operations: List[str] = []
    processing_order = ["delete", "modify", "add"]

    for key in processing_order:
        indexes = index_changes.get(key, [])
        if key == "delete":
            for index in indexes:
                operations.append(f"DROP INDEX IF EXISTS {index.name}")
        elif key == "add":
            for index in indexes:
                operations.append(f"ADD INDEX IF NOT EXISTS {index.to_datafile()}")
                operations.append(f"MATERIALIZE INDEX IF EXISTS {index.name}")
        elif key == "modify":
            for index in indexes:
                operations.append(f"DROP INDEX IF EXISTS {index.name}")
                operations.append(f"ADD INDEX IF NOT EXISTS {index.to_datafile()}")
                operations.append(f"MATERIALIZE INDEX IF EXISTS {index.name}")

    return operations


def quote(column_name: str):
    if not column_name[0] == "`" and not column_name[-1] == "`":
        return f"`{column_name}`"
    return column_name


@dataclass
class AlterOperation:
    """Defines a CH alter table operation"""

    sql: str
    create_mutation: bool

    @staticmethod
    def add_column(column_sql: str, first=False, after_column=None):
        position = ""
        if first:
            position = " FIRST"
        elif after_column:
            position = f" AFTER {after_column}"
        return AlterOperation(f"ADD COLUMN {column_sql}{position}", create_mutation=False)

    @staticmethod
    def drop_column(column_name: str):
        return AlterOperation(f"DROP COLUMN {quote(column_name)}", create_mutation=True)

    @staticmethod
    def set_default(column_name: str, default_value: str):
        if default_value is None:
            return AlterOperation(f"MODIFY COLUMN {quote(column_name)} REMOVE DEFAULT", create_mutation=False)
        else:
            return AlterOperation(
                f"MODIFY COLUMN {quote(column_name)} DEFAULT {default_value.replace('DEFAULT ', '')}",
                create_mutation=False,
            )

    @staticmethod
    def remove_default(column_name: str):
        return AlterOperation(f"MODIFY COLUMN {quote(column_name)} REMOVE DEFAULT", create_mutation=False)

    @staticmethod
    def to_nullable(column_name, _type):
        return AlterOperation(f"MODIFY COLUMN {quote(column_name)} Nullable({_type})", create_mutation=True)

    @staticmethod
    def to_nullable_and_set_default(column_name, _type, default_value):
        if default_value is None:
            raise ValueError(
                "Making a column Nullable and removing the Default value can't be done together. Please execute one operation at a time."
            )
        return AlterOperation(
            f"MODIFY COLUMN {quote(column_name)} Nullable({_type}) DEFAULT {default_value.replace('DEFAULT ', '')}",
            create_mutation=True,
        )

    @staticmethod
    def modify_column(column_sql: str):
        return AlterOperation(f"MODIFY COLUMN {column_sql}", create_mutation=True)

    @staticmethod
    def from_sql(sql: str):
        return AlterOperation(sql, create_mutation=True)


def _remove_allowed_modifications_in_signature(signature):
    allowed_modifications = {"default_value", "nullable"}

    filtered_signature = []
    for column in signature:
        filtered_signature_items = [i for i in column if (isinstance(i, str) or i[0] not in allowed_modifications)]
        filtered_signature.append(tuple(filtered_signature_items))
    return filtered_signature


async def alter_table_operations(
    workspace: Workspace,
    schema_a: str,
    schema_b: str,
    has_internal_columns: bool = False,
    jsonpaths: Optional[str] = None,
    engine: Optional[TableDetails] = None,
):
    operations: list[AlterOperation] = []
    operations_quarantine: list[AlterOperation] = []

    def columns_signature(schema: str):
        columns = parse_table_structure(schema)
        columns_dict = {c["normalized_name"]: (i, c) for i, c in enumerate(columns)}
        columns_signature = [
            tuple([c["normalized_name"]] + list(zip(c.keys(), c.values(), strict=True)))  # noqa: RUF005
            for c in columns
        ]
        return columns_dict, columns_signature

    def check_column_droppable(column_name: str, engine: Optional[TableDetails]):
        if engine is None:
            return

        if engine.sorting_key is not None and re.search(rf"(^|[(,\s]){column_name}($|[,)\s])", engine.sorting_key):
            raise ValueError(
                f"Dropping the '{column_name}' column is not supported because it is part of the sorting key"
            )

        index_exp_pattern = rf"^(.+\({column_name}\)|{column_name})$"
        if (
            engine.indexes is not None
            and (indexes_using_column := [i for i in engine.indexes if re.search(index_exp_pattern, i.expr)])
            and len(indexes_using_column) > 0
        ):
            raise ValueError(
                f"Dropping the '{column_name}' column is not supported because it is part of  index '{indexes_using_column[0].name}'"
            )

        return

    def get_column_name(signature, index):
        return [t[1] for t in signature[index] if t[0] == "normalized_name"][0]

    columns_a, signature_a = columns_signature(schema_a)
    columns_b, signature_b = columns_signature(schema_b)

    if len(columns_b) > MAX_COLUMNS_SCHEMA:
        raise ValueError(ClientErrorBadRequest.num_columns_not_supported(parameters=MAX_COLUMNS_SCHEMA))

    modified_columns: list[AlterOperation] = []
    modified_columns_add_default: list[AlterOperation] = []
    dropped_columns = []
    signature_a_clean = _remove_allowed_modifications_in_signature(signature_a)
    signature_b_clean = _remove_allowed_modifications_in_signature(signature_b)

    dropped_modified_columns = set(signature_a_clean) - set(signature_b_clean)
    for c, *_c_args in dropped_modified_columns:
        if c in columns_b:
            current_column = schema_to_sql_columns([columns_a[c][1]])[0]
            modified_column = schema_to_sql_columns([columns_b[c][1]])[0]
            raise ValueError(
                f"Modifying the '{c}' column is not supported. Changing from '{current_column}' to '{modified_column}'"
            )
        else:
            column_to_drop = columns_a[c][1]
            check_column_droppable(column_to_drop["name"], engine)
            dropped_columns.append(schema_to_sql_columns([column_to_drop])[0].split(" ")[0])

    any_modify_column_with_default = False
    new_columns = []
    added_columns = set(signature_b_clean) - set(signature_a_clean)
    for c, *_c_args in added_columns:
        position, column = columns_b[c]

        await column_replace_default_expression(workspace, column)
        new_column = schema_to_sql_columns([column])[0]

        new_column_quarantine = schema_to_sql_columns(
            [
                {
                    "name": column["name"],
                    "normalized_name": column["normalized_name"],
                    "type": "String",
                    "nullable": True,
                    "default_value": None,
                    "codec": None,
                }
            ]
        )[0]
        new_columns.append((position, new_column, new_column_quarantine))
        any_modify_column_with_default |= column.get("default_value", None) is not None

    alter_with_order = len([c for c in new_columns if c[0] < len(signature_a)]) > 0
    for _position, new_column, new_column_quarantine in sorted(new_columns):
        if not alter_with_order and not has_internal_columns:
            operations.append(AlterOperation.add_column(new_column))
            operations_quarantine.append(AlterOperation.add_column(new_column_quarantine))
        else:
            if _position == 0:
                operations.append(AlterOperation.add_column(new_column, first=True))
                operations_quarantine.append(AlterOperation.add_column(new_column_quarantine, first=True))
            else:
                column = get_column_name(signature_b, _position - 1)
                operations.append(AlterOperation.add_column(new_column, after_column=column))
                operations_quarantine.append(AlterOperation.add_column(new_column_quarantine, after_column=column))

    # alter columns

    diff_columns_alter = set(signature_a) - set(signature_b)
    modified_columns_keys = set([item[0] for item in diff_columns_alter])
    modified_column_keys_ordered = [c for c, *_c_args in signature_a if c in modified_columns_keys and c in columns_b]
    for c in modified_column_keys_ordered:
        mod_current_column = columns_a[c][1]
        mod_current_column_sql = schema_to_sql_columns([mod_current_column])[0]
        mod_modified_column = columns_b[c][1]
        mod_modified_column_sql = schema_to_sql_columns([columns_b[c][1]])[0]

        convert_to_nullable = (
            mod_current_column.get("nullable", False) is False and mod_modified_column.get("nullable", False) is True
        )
        modify_default = mod_current_column.get("default_value", None) != mod_modified_column.get("default_value", None)
        if modify_default and not mod_current_column.get("default_value", False):
            any_modify_column_with_default = True
        column_name = mod_modified_column.get("normalized_name", mod_modified_column["name"])
        column_type = mod_modified_column["type"]
        default_value = mod_modified_column.get("default_value", None)

        if convert_to_nullable and modify_default:
            modified_columns.append(AlterOperation.to_nullable_and_set_default(column_name, column_type, default_value))
        elif convert_to_nullable:
            modified_columns.append(AlterOperation.to_nullable(column_name, column_type))
        elif modify_default:
            modified_columns_add_default.append(AlterOperation.set_default(column_name, default_value))
        else:
            raise ValueError(
                f"Modifying the '{c}' column is not supported. Changing from '{mod_current_column_sql}' to '{mod_modified_column_sql}'"
            )

    for op in modified_columns:
        operations.append(op)
    for op in modified_columns_add_default:
        operations.append(op)

    for dropped_column in dropped_columns:
        operations.append(AlterOperation.drop_column(dropped_column))
        operations_quarantine.append(AlterOperation.drop_column(dropped_column))

    return operations, operations_quarantine


def table_exists(workspace: Workspace, datasource: Datasource):
    return ch_table_exists_sync(datasource.id, workspace.database_server, workspace.database)


def analyze_csv_and_create_tables_if_dont_exist(
    workspace: Workspace,
    datasource: Datasource,
    csv_extract: str,
    dialect_overrides: Optional[Dict[str, str]] = None,
    type_guessing=True,
):
    database = workspace.database
    cluster = workspace.cluster
    database_server = workspace.database_server
    table_name = datasource.id

    datasource_exists = ch_table_exists_sync(table_name, database_server, database)
    info = CSVInfo.extract_from_csv_extract(
        csv_extract,
        dialect_overrides=dialect_overrides,
        type_guessing=type_guessing,
        cached_source_csv_header_info=datasource.get_cached_source_csv_headers(),
        skip_stats_collection=datasource_exists,
    )

    # cache source CSV headers on creation so it can be used when the header guessing does not work in append mode
    # it'll be persisted by a before_create hook
    if info.dialect["has_header"]:
        datasource.cache_source_csv_headers(
            header=str([x["name"] for x in info.columns]), header_hash=info.dialect.get("header_hash", None)
        )

    ch_table = info.get_ch_table(storage_policy=workspace.storage_policy)
    ch_table.cluster = cluster

    if not datasource:
        raise ValueError("datasource not provided")

    def _create_table(sql: str):
        logging.debug("creating table: %s" % sql)

        client = HTTPClient(database_server, database)
        try:
            client.query_sync(sql, read_only=False, **workspace.ddl_parameters(skip_replica_down=True))
        except CHException as e:
            logging.exception(e)
            raise Exception("failed creating table: %s" % str(e))

    if not datasource_exists:
        table_created = False
        for hook in datasource.hooks:
            table_created = table_created or hook.before_create(datasource)
        if not table_created:
            _create_table(ch_table.as_sql(database, table_name))
            ch_table_safe = info.get_ch_table(safe_types=True)
            ch_table_safe = QuarantineCHTable(
                ERROR_COLUMNS + ch_table_safe.columns,
                cluster=cluster,
                storage_policy=workspace.storage_policy,
            )
            _create_table(ch_table_safe.as_sql(database, f"{table_name}_quarantine"))

        for hook in datasource.hooks:
            hook.after_create(datasource)
    else:
        # TODO: check if the table_schema is compatible with the CSV
        pass
    return info


async def drop_table(workspace: Workspace, table_id: str, sync: bool = False, force: bool = False) -> List[Exception]:
    tables = [table_id, f"{table_id}_quarantine", f"{table_id}_staging"]
    exists_tables = await ch_table_list_exist(tables, workspace["database_server"], workspace["database"])

    results: List[Exception] = []
    for name, exists in exists_tables:
        if exists or force:
            try:
                # The snapshot Release in a Branch needs to be immutable
                if not allow_drop_table(workspace, name):
                    logging.info(
                        f"Drop table not allowed: workspace {workspace.name} ({workspace.id}, {workspace.database}), name {name}"
                    )
                    continue
                await ch_drop_table_with_fallback(
                    workspace.database_server,
                    workspace.database,
                    name,
                    workspace.cluster,
                    exists_clause=True,
                    sync=sync,
                    **workspace.ddl_parameters(skip_replica_down=True),
                )
                logging.info(
                    f"Drop table succeeded: workspace {workspace.name} ({workspace.id}, {workspace.database}), name {name}"
                )
            except Exception as e:
                logging.exception(
                    f"Drop table failed: workspace {workspace.name} ({workspace.id}, {workspace.database}), name {name}. Error: {e}"
                )
                results.append(e)
    return results


def append_data_to_table(
    *,
    database_server: str,
    database: str,
    cluster: Optional[str],
    table_name: str,
    rows: List[Any],
    import_id: Optional[str] = None,
    with_quarantine: bool = True,
    columns=None,
) -> None:
    if not rows:
        return
    block = Block(
        id="id",
        table_name=table_name,
        data=csv_from_python_object(rows),
        database_server=database_server,
        database=database,
        cluster=cluster,
        dialect={
            "delimiter": ",",
            "new_line": "\r\n",
        },
        import_id=import_id,
        max_execution_time=Limit.ch_chunk_max_execution_time,
        csv_columns=columns,
        quarantine=with_quarantine,
    )
    CsvChunkQueueRegistry.get_or_create().process(block)
