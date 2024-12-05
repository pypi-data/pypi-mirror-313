import logging
from dataclasses import dataclass
from typing import List, Optional, Set, Tuple

from tinybird.ch import ch_get_tables_metadata
from tinybird.datasource import Datasource
from tinybird.pipe import Pipe
from tinybird.user import User


def get_all_tables(
    only_materialized: bool = False,
    avoid_database_servers: Optional[List[str]] = None,
    only_active_workspaces: bool = False,
    only_main_workspaces: bool = False,
    include_releases: bool = True,
    strict_for_missing: bool = False,
):
    users_by_database = {}
    users_tables = set()
    ch_servers: Set[Tuple[str, Optional[str]]] = set()

    # This will retrive all the workspaces and not just 1000 as it has `fast_scan=True`
    all_users = User.get_all(include_releases=include_releases, include_branches=True)
    if only_active_workspaces:
        all_users = [w for w in all_users if w.is_active]
    if only_main_workspaces:
        all_users = [w for w in all_users if not w.origin]

    def get_resources_from_releases(workspace_id: str) -> Tuple[List[Datasource], List[Pipe]]:
        datasources = []
        pipes = []
        workspace: Optional["User"] = User.get_by_id(workspace_id)
        if not workspace or strict_for_missing:
            return [], []

        for release in workspace.get_releases():
            if not release.metadata:
                continue
            datasources += release.metadata.get_datasources()
            pipes += release.metadata.get_pipes()
        return datasources, pipes

    for u in all_users:
        try:
            if avoid_database_servers and any(avoid in u.database_server for avoid in avoid_database_servers):
                continue
            users_by_database[u.database] = (u.name, u.clusters, u.is_active)
            if u.clusters:
                for cluster in u.clusters:
                    ch_servers.add((u.database_server, cluster))
            else:
                ch_servers.add((u.database_server, None))
            datasources, pipes = get_resources_from_releases(u.id)
            if not only_materialized:
                for ds in u.get_datasources() + datasources:
                    if not strict_for_missing or not ds.is_read_only:
                        users_tables.add((u.database, ds.id))
                        if not strict_for_missing or not u.is_branch:
                            users_tables.add((u.database, f"{ds.id}_quarantine"))
            for p in u.get_pipes() + pipes:
                for n in p.pipeline.nodes:
                    if n.materialized:
                        r_id = f".inner.{n.id}" if n.id == n.materialized else n.materialized
                        if only_materialized:
                            users_tables.add((u.database, n.id))  # The MaterializedView
                        else:
                            users_tables.add(
                                (u.database, r_id)
                            )  # The target table, probably already added in get_datasources
                            users_tables.add((u.database, n.id))  # The MaterializedView
        except Exception as e:
            logging.warning(f"Error with workspace {u.id} - {u.name} - {u.database}: {e}")

    return users_by_database, users_tables, ch_servers


@dataclass
class MissingTablesResponse:
    tables: List[Tuple[str, str, int]]  # tuple of database, table id
    stats: int  # number of tables checked


async def check_missing_tables(database_server: str, cluster: str) -> MissingTablesResponse:
    users_by_database, users_tables, _ = get_all_tables(
        only_active_workspaces=True, include_releases=False, strict_for_missing=True
    )
    # Don't pass cluster to got to specific replica
    ch_servers = [(database_server, "")]
    ch_tables = await ch_get_tables_metadata(database_servers=ch_servers, filter_engines=("View", "Distributed"))
    databases = [
        database
        for database, (_, clusters, is_active) in users_by_database.items()
        if is_active and ((cluster and cluster in clusters) or not cluster)
    ]
    missing_tables = []
    counter = 0
    # remove
    metadata_tables = [(database, table) for database, table in users_tables if database in databases]
    for database, table in metadata_tables:
        if (database, table) not in ch_tables:
            missing_tables.append((database, table, 0))
        counter += 1

    if missing_tables:
        ch_tables = await ch_get_tables_metadata(
            database_servers=[(database_server, cluster)], filter_engines=("View", "Distributed")
        )
        missing_tables = [
            (database, table, 0)
            if (database, table) not in ch_tables
            else (database, table, ch_tables[(database, table)][3])
            for database, table, _count in missing_tables
        ]

    return MissingTablesResponse(tables=missing_tables, stats=counter)
