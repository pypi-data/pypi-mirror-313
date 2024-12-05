from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import orjson

from tinybird.ch import (
    ERROR_COLUMNS,
    CHTable,
    CSVInfo,
    HTTPClient,
    QuarantineCHTable,
    ch_table_details_async,
    url_from_host,
)
from tinybird.ch_utils.exceptions import CHException
from tinybird.datasource import Datasource
from tinybird.pg import PGService
from tinybird.sql import TableIndex, parse_table_structure
from tinybird.syncasync import sync_to_async
from tinybird.user import User, Users, public
from tinybird.views.aiohttp_shared_session import get_shared_session
from tinybird.views.json_deserialize_utils import (
    ParsedAugmentedSchema,
    json_deserialize_merge_schema_jsonpaths,
    parse_augmented_schema,
)


class DatasourceCreationError(ValueError):
    pass


# TODO: We should change this method to be generic and use all the existing methods to create a datasource
async def create_datasource(
    workspace: User,
    ds_name: str,
    schema: str,
    json_deserialization: List[Dict[str, Any]],
    engine_full: Optional[str] = None,
    service_name: Optional[str] = None,
    service_conf: Optional[dict] = None,
    connector: Optional[str] = None,
    indexes: Optional[List[TableIndex]] = None,
):
    start_time = datetime.now(timezone.utc)
    cluster = workspace.cluster

    datasource: Datasource = await sync_to_async(Users.add_datasource_sync)(
        workspace,
        ds_name,
        cluster=cluster,
        json_deserialization=json_deserialization,
        service_name=service_name,
        service_conf=service_conf,
    )

    columns = parse_table_structure(schema)
    for col in columns:
        del col["jsonpath"]
    quarantine_columns = ERROR_COLUMNS + CSVInfo.convert_columns_to_safe_types(columns)
    try:
        create_sql, create_quarantine_sql = _generate_table_creation_sql(
            workspace, datasource, columns, quarantine_columns, cluster, engine_full, indexes
        )
    except DatasourceCreationError as exc:
        await sync_to_async(Users.drop_datasource)(workspace, datasource.id)
        raise exc

    client = HTTPClient(workspace.database_server, workspace.database)
    params = {"database": workspace.database, **workspace.ddl_parameters(skip_replica_down=True)}

    try:
        await _execute_table_creation(client, params, create_sql)
    except CHException as e:
        await sync_to_async(Users.drop_datasource)(workspace, datasource.id)
        error_message = f"Error creating CH table {str(e)}"
        await _log_ops(workspace, datasource, start_time, True, error_message)
        raise e

    try:
        await _execute_table_creation(client, params, create_quarantine_sql)
    except CHException as e:
        await sync_to_async(Users.drop_datasource)(workspace, datasource.id)
        error_message = f"Error creating CH table {str(e)}"
        await _log_ops(workspace, datasource, start_time, True, error_message)
        raise e

    engine = await ch_table_details_async(datasource.id, workspace.database_server, database=workspace.database)
    datasource.engine = engine.to_json(exclude=["engine_full"])
    await sync_to_async(Users.update_datasource_sync)(workspace, datasource)
    await sync_to_async(lambda: PGService(workspace).sync_foreign_tables(datasources=[datasource]))()
    await _log_ops(workspace, datasource, start_time, service_name=service_name, connector=connector)

    return datasource


def _generate_table_creation_sql(workspace, datasource, columns, quarantine_columns, cluster, engine_full, indexes):
    try:
        create_sql = CHTable(
            columns, cluster=cluster, engine=engine_full, storage_policy=workspace.storage_policy, indexes=indexes
        ).as_sql(workspace.database, datasource.id)

        create_quarantine_sql = QuarantineCHTable(
            quarantine_columns,
            cluster=cluster,
            storage_policy=workspace.storage_policy,
        ).as_sql(workspace.database, f"{datasource.id}_quarantine")

        return create_sql, create_quarantine_sql
    except ValueError as exc:
        raise DatasourceCreationError(f"Invalid data source structure: {exc}")


async def _execute_table_creation(http_client: HTTPClient, params: Dict[str, Any], sql: str):
    return await http_client.query(sql, read_only=False, **params)


def parse_datasource_schema(schema: str | None) -> Tuple[ParsedAugmentedSchema | None, List[Dict[str, Any]]]:
    json_deserialization: List[Dict[str, Any]] = []

    if not schema:
        return None, json_deserialization

    parsed_schema = parse_augmented_schema(schema)
    columns = parse_table_structure(parsed_schema.schema)

    if parsed_schema.jsonpaths:
        json_deserialization = json_deserialize_merge_schema_jsonpaths(columns, parsed_schema.jsonpaths)

    return parsed_schema, json_deserialization


async def _log_ops(
    workspace: User,
    datasource: Datasource,
    start_time: datetime,
    is_error: bool = False,
    error: Optional[str] = None,
    service_name: Optional[str] = None,
    connector: Optional[str] = None,
):
    pu = public.get_public_user()
    table = next(x for x in pu.datasources if x["name"] == "datasources_ops_log")
    database_server_url = url_from_host(pu.database_server)
    query = f"""INSERT INTO {pu.database}.{table['id']}(
                    timestamp,
                    event_type,
                    datasource_id,
                    datasource_name,
                    user_id,
                    user_mail,
                    result,
                    elapsed_time,
                    error,
                    request_id,
                    import_id,
                    job_id,
                    rows,
                    rows_quarantine,
                    blocks_ids,
                    Options.Names,
                    Options.Values,
                    release
                ) FORMAT JSONEachRow"""

    options_logs = {"source": "schema"}

    if connector:
        options_logs["connector"] = connector
    if service_name:
        options_logs["service"] = service_name

    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event_type": "create",
        "datasource_id": datasource.id,
        "datasource_name": datasource.name,
        "user_id": workspace.main_id,
        "user_mail": "",
        "result": "ok" if not is_error else "error",
        "elapsed_time": 0 if not start_time else (datetime.now(timezone.utc) - start_time).total_seconds(),
        "error": error,
        "request_id": "",
        "import_id": None,
        "job_id": None,
        "rows": 0,
        "rows_quarantine": 0,
        "blocks_ids": [],
        "Options.Names": list(options_logs.keys()),
        "Options.Values": list(options_logs.values()),
        "release": workspace.release_semver(),
    }

    data = orjson.dumps(log_entry)
    params = {"database": pu.database, "query": query}
    async with get_shared_session().request("POST", url=database_server_url, params=params, data=data) as resp:
        result = await resp.content.read()
        if resp.status >= 400:
            raise Exception(
                f"Error creating CH table for quarantine {resp.status}: {result.decode('utf-8', 'replace')}"
            )
