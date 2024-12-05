import asyncio
import json
from itertools import chain
from typing import List, Set

import click
from humanfriendly.tables import format_smart_table

from tinybird.ch import HTTPClient
from tinybird.job import JobExecutor
from tinybird.user import User as Workspace
from tinybird.user import UserAccount

from ... import common
from ..cli_base import cli
from ..helpers import get_workspaces_data


def get_all_databases(database_server: str) -> List[str]:
    client = HTTPClient(database_server)
    _, body = client.query_sync("SHOW DATABASES FORMAT JSON")
    databases = json.loads(body)["data"]
    return [database["name"] for database in databases]


@cli.command()
@click.option("--name_needle", default=None, help="Filter workspaces by name needle")
@click.option("--cluster", default=None)
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
def orphan_branches(name_needle, cluster, config):
    """
    This command will list all the orphan branches and allow you to remove them if you want
    An orphan branch is a branch that either
    - The database no longer exists, but the workspace still alive in Redis
    - The origin workspace is deleted, but the branch was not removed
    - The origin workspace does not consider the branch as a child
    """
    conf, redis_client = common.setup_redis_client(config)
    redis_config = common.get_redis_config(conf)
    common.setup_connectors_config(conf)

    job_executor = JobExecutor(
        redis_client=redis_client,
        redis_config=redis_config,
    )
    all_workspaces = Workspace.get_all(include_branches=True, include_releases=True)
    workspaces_active_ids = [ws.id for ws in all_workspaces if not ws.deleted]

    # First, let's look for any branch that either the database no longer exists or the origin workspace is deleted
    branches = get_workspaces_data(None, name_needle, cluster, include_deleted=True, only_branches=True)
    branch_database_servers: Set[str] = {w.database_server for w in branches}
    branch_databases: Set[str] = set(
        chain.from_iterable([get_all_databases(server) for server in branch_database_servers])
    )

    # If the database of the branch and the origin does not exist, we can delete it safely
    branches_safe_to_delete: List[Workspace] = [
        Workspace.get_by_id(x.id)
        for x in branches
        if x.database not in branch_databases and x.origin not in workspaces_active_ids
    ]

    # We should review why the branch is soft deleted and if we can delete it
    soft_deleted_branches: List[Workspace] = [
        Workspace.get_by_id(x.id) for x in branches if x.deleted and x.id not in [y.id for y in branches_safe_to_delete]
    ]

    # Branches not deleted without database
    branches_not_deleted_without_database: List[Workspace] = [
        Workspace.get_by_id(x.id)
        for x in branches
        if x.database not in branch_databases
        and x.id not in [y.id for y in branches_safe_to_delete + soft_deleted_branches]
    ]

    column_names = ["name", "id", "cluster", "database", "origin", "safe"]
    click.secho("\nList of possible orphan branches in the target cluster", bold=True)
    click.echo(
        format_smart_table(
            [
                (x.name, x.id, x.cluster, x.database, x.origin, "✅" if x in branches_safe_to_delete else "🚨")
                for x in branches_safe_to_delete + soft_deleted_branches + branches_not_deleted_without_database
            ],
            column_names=column_names,
        )
    )

    if click.confirm("\nDo you want to delete orphan branches?"):
        for branch in branches_safe_to_delete:
            if click.confirm(f"✅ Safe to delete {branch.name} {branch.id}. You want to delete it?"):
                info = branch.get_workspace_info()
                owner = UserAccount.get_by_id(info["owner"])
                asyncio.run(
                    UserAccount.delete_workspace(
                        owner, branch, hard_delete=True, job_executor=job_executor, track_log=False
                    )
                )
                click.secho(f"Deleted {branch.name}", fg="green")

        # We have to be extra careful with soft deleted branches as we might detect a legacy release as a branch
        # and we don't want to delete it
        # We have a dedicated command for releases in `orphan-releases`
        for branch in soft_deleted_branches:
            if click.confirm(f"🚨 Branch {branch.name} {branch.id} is soft deleted. You want to delete it?"):
                info = branch.get_workspace_info()
                owner = UserAccount.get_by_id(info["owner"])
                asyncio.run(
                    UserAccount.delete_workspace(
                        owner, branch, hard_delete=True, job_executor=job_executor, track_log=False
                    )
                )
                click.secho(f"Deleted {branch.name}", fg="green")

        # We shouldn't have branches not deleted with a database, we need to review how they reach this point
        # But should be safe to remove them
        for branch in branches_not_deleted_without_database:
            if click.confirm(
                f"🚨 Branch {branch.name} {branch.id} is not deleted, but the database does not exist. You want to delete it?"
            ):
                info = branch.get_workspace_info()
                owner = UserAccount.get_by_id(info["owner"])
                asyncio.run(
                    UserAccount.delete_workspace(
                        owner, branch, hard_delete=True, job_executor=job_executor, track_log=False
                    )
                )
                click.secho(f"Deleted {branch.name}", fg="green")
