import json
from typing import Any, Dict, List, Optional, Set

from tinybird.ch import HTTPClient
from tinybird.datasource import Datasource
from tinybird.tinybird_tool.common import setup_redis_client
from tinybird.user import User, UserAccount, UserWorkspaceRelationship, public

virtual_clusters_raw = {
    "itxcadenas_pilot": "itxcadenas",
    "itx_z_pro_stock": "itx_z_pro",
    "live": "itxcadenas",
    "thn_rt": "thn",
    "lookiero": "eu_public_b",
}

virtual_clusters_to_original = {
    f"http://{vc}:6081": f"http://{virtual_clusters_raw[vc]}:6081" for vc in virtual_clusters_raw
}


def run_query(database_server, sql, **kwargs):
    extra_params = {"max_execution_time": 7200, "max_result_bytes": 0, **kwargs}
    client = HTTPClient(database_server, database=None)
    try:
        headers, body = client.query_sync(sql, read_only=False, **extra_params)
        if "application/json" in headers["content-type"]:
            return json.loads(body)
        return body
    except Exception as e:
        print(f' - [ERROR] Failed to run query: "{sql}"\nReason={e}')


cached_size_and_resources_calls = {}


def get_workspace_size_and_resources(ws: User) -> Optional[Dict[str, Any]]:
    if ws.database_server not in cached_size_and_resources_calls:
        measures = run_query(
            ws.database_server,
            """
select
    database,
    count() as resources,
    sum(total_bytes) as size
from system.tables
group by database
FORMAT JSON
    """,
        ).get("data", [])
        cached_size_and_resources_calls[ws.database_server] = {
            measure["database"]: {"size": measure["size"], "resources": measure["resources"]} for measure in measures
        }
    return cached_size_and_resources_calls[ws.database_server].get(ws.database, None)


def get_active_ws(inactivity_days: int) -> Set[str]:
    public_user = public.get_public_user()
    workspaces_all = public_user.get_datasource("workspaces_all")
    assert isinstance(workspaces_all, Datasource)
    datasources_ops_log = public_user.get_datasource("datasources_ops_log")
    assert isinstance(datasources_ops_log, Datasource)
    filter_by_database_server_sql = f"""
    JOIN (
        SELECT
            *
        FROM
            {public_user.database}.{workspaces_all.id}
    )
    ON id = user_id"""
    active_workspaces_datasources_query = f"""
    SELECT
        groupUniqArray(user_id) as active_workspaces_datasources
    FROM
        {public_user.database}.{datasources_ops_log.id}
        {filter_by_database_server_sql}
    WHERE
        timestamp > now() - INTERVAL {inactivity_days} DAY
    FORMAT JSON"""
    active_workspaces_datasources = run_query(public_user.database_server, active_workspaces_datasources_query).get(
        "data", []
    )
    active_workspaces_datasources_ids = active_workspaces_datasources[0].get("active_workspaces_datasources", [])
    pipe_stats = public_user.get_datasource("pipe_stats")
    assert isinstance(pipe_stats, Datasource)
    active_workspaces_pipes_query = f"""
    SELECT
        groupUniqArray(user_id) as active_workspaces_pipes
    FROM
        {public_user.database}.{pipe_stats.id}
        {filter_by_database_server_sql}
    WHERE
        date > now() - INTERVAL {inactivity_days} DAY
    FORMAT JSON"""
    active_workspaces_pipes = run_query(public_user.database_server, active_workspaces_pipes_query).get("data", [])
    active_workspaces_pipes_ids = active_workspaces_pipes[0].get("active_workspaces_pipes", [])
    return set(active_workspaces_datasources_ids) | set(active_workspaces_pipes_ids)


def get_stats(workspaces: List[User], inactivity_days: int) -> None:
    active_workspaces = get_active_ws(inactivity_days)
    print("name,id,database,database_server,plan,type,deleted,database_found,active,size,number_of_resources")
    for ws in workspaces:
        name = ws.name if len(ws.name) > 2 and ws.name != "," else "unknown_name"
        database_server = virtual_clusters_to_original.get(ws.database_server, ws.database_server)
        size_and_res = get_workspace_size_and_resources(ws)
        if size_and_res is None:
            database_found = "False"
            size = 0
            resources = 0
        else:
            database_found = "True"
            size = size_and_res["size"] or 0
            resources = size_and_res["resources"] or 0
        type = "branch" if ws.is_branch else "main"
        active = ws.id in active_workspaces
        print(
            f"{name},{ws.id},{ws.database},{database_server},{ws.plan},{type},{ws.deleted},{database_found},{active},{size},{resources}"
        )


def get_orphan_databases() -> None:
    existing_workspaces = User.get_all(include_branches=True, include_releases=False)
    tracked_databases_in_redis = {ws.database: {"database_server": ws.database_server} for ws in existing_workspaces}
    tracked_database_servers_raw = {ws.database_server for ws in existing_workspaces}
    tracked_database_servers = {
        virtual_clusters_to_original.get(database_server, database_server)
        for database_server in tracked_database_servers_raw
    }
    print("database_server,database,problem,size,number_of_resources,original_database_server")
    for database_server in tracked_database_servers:
        found_databases_in_ch = run_query(
            database_server,
            """
        select
            database,
            count() as resources,
            sum(total_bytes) as size
        from system.tables
        where database NOT IN ('system', 'INFORMATION_SCHEMA', 'information_schema')
        group by database
        FORMAT JSON
        """,
        ).get("data", [])
        for row in found_databases_in_ch:
            track = False
            problem = ""
            original_database_server = ""
            if row["database"] not in tracked_databases_in_redis:
                track = True
                problem = "database_not_tacked"
            if (
                row["database"] in tracked_databases_in_redis
                and virtual_clusters_to_original.get(
                    tracked_databases_in_redis[row["database"]]["database_server"],
                    tracked_databases_in_redis[row["database"]]["database_server"],
                )
                != database_server
            ):
                track = True
                problem = "database_server_mismatch"
                original_database_server = tracked_databases_in_redis[row["database"]]["database_server"]
            if track:
                print(
                    f"{database_server},{row['database']},{problem},{row['size'] or 0},{row['resources']},{original_database_server}"
                )


def execute() -> None:
    config_file = "/mnt/disks/tb/tinybird/pro.py"
    settings, redis_client = setup_redis_client(config_file)  # type: ignore
    User.config(redis_client, settings["jwt_secret"], replace_executor=None, secrets_key=settings["secrets_key"])
    UserAccount.config(redis_client, settings["jwt_secret"])
    UserWorkspaceRelationship.config(redis_client)
    # Output 1: database info per workspace (main and branches)
    workspaces_to_check = User.get_all(include_branches=True, include_releases=False, count=None)
    inactivity_days = 90
    get_stats(workspaces_to_check, inactivity_days)
    # Outout 2: Orphan databases without information in
    # get_orphan_databases()


if __name__ == "__main__":
    execute()
