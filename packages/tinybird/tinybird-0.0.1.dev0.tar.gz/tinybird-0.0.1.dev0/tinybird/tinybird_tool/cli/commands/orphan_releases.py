import asyncio
import json
from typing import List

import click
from humanfriendly.tables import format_smart_table

from tinybird.ch import HTTPClient
from tinybird.user import User as Workspace

from ... import common
from ..cli_base import cli
from ..helpers import WorkspaceData, get_workspaces_data


@cli.command()
@click.option("--name_needle", default=None, help="Filter releases by name needle")
@click.option("--cluster", default=None)
@click.option("--include-deleted", is_flag=True)
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
def orphan_releases(name_needle, cluster, include_deleted, config):
    """List  matching an email needle"""
    common.setup_redis_client(config)

    # We need to get all releases from all workspaces, including deleted ones
    # We might include old branches that didn't have releases. We will handle as releases
    found_releases = get_workspaces_data(None, name_needle, cluster, include_deleted=True, only_releases=True)
    all_workspaces = Workspace.get_all(include_branches=True, include_releases=True)
    workspaces_active_ids = [ws.id for ws in all_workspaces if not ws.deleted]

    possible_orphan_releases: List[Workspace] = list(
        filter(lambda x: x.origin not in workspaces_active_ids, found_releases)
    )

    column_names = ["name", "id", "cluster", "database", "origin"]
    click.secho("\nList of possible orphan releases in the target cluster", bold=True)
    click.echo(
        format_smart_table(
            [
                (release.name, release.id, release.cluster, release.database, release.origin)
                for release in possible_orphan_releases
            ],
            column_names=column_names,
        )
    )
    if possible_orphan_releases and click.confirm("\nDo you want review them to clean?\n"):
        for possible_release in possible_orphan_releases:
            release: Workspace = Workspace.get_by_id(possible_release.id)
            click.secho(f"\nChecking if deleting orphan '{release.name}' '{release.id}' is safe")

            # If the database not exists, it should be safe to remove the release
            client = HTTPClient(release.database_server)
            _, body = client.query_sync("SHOW DATABASES FORMAT JSON")
            databases = json.loads(body)["data"]
            if release.database not in [database["name"] for database in databases]:
                click.secho(
                    f"✅ Safe to delete. Database '{release.database}' does not exist in cluster '{release.cluster}'"
                )
                if click.confirm(f"Do you want to delete orphan release {release.name} from redis?"):
                    Workspace._delete(release.id)
                    click.secho(f"Deleted {release.name}", fg="green")
            else:
                # Added some extra validations to make sure we don't have a inconsistent state
                origin = Workspace.get_by_id(release.origin)
                if origin and origin.deleted:
                    click.secho(
                        f"⚠️ Database '{release.database}' exists in cluster. The origin workspace'{origin.id}' is soft-deleted. Please review manually",
                        fg="yellow",
                    )
                elif origin and not origin.deleted:
                    click.secho(
                        f"🚨 Database '{release.database}' exists in cluster. The origin workspace'{origin.id}' is not soft-deleted. Please review manually. This seems like a bug",
                        fg="yellow",
                    )
                else:
                    click.secho(
                        f"🚨 Database '{release.database}' exists in cluster. The origin workspace is not found. Please review manually. This seems like a bug",
                        fg="yellow",
                    )
    else:
        click.secho("Skipping clean", fg="yellow")

    # TODO: We should include what future orphan releases metadata is.
    if click.confirm("\nDo you want review future orphan releases metadata?\n"):
        # If a release is not connect to the origin workspace, should be safe to remove
        future_possible_orphan = []
        for release in found_releases:
            origin = Workspace.get_by_id(release.origin)
            if origin and not origin.deleted and not origin.get_release_by_id(release.id):
                future_possible_orphan.append(release)

        column_names = ["name", "id", "cluster", "database", "origin"]
        click.secho("\nList of possible future orphan releases metadata in the target cluster", bold=True)
        click.echo(
            format_smart_table(
                [
                    (release.name, release.id, release.cluster, release.database, release.origin)
                    for release in future_possible_orphan
                ],
                column_names=column_names,
            )
        )
        if future_possible_orphan and click.confirm("\nDo you want review them to clean?\n"):
            for future_possible in future_possible_orphan:
                release = Workspace.get_by_id(future_possible.id)
                origin = Workspace.get_by_id(release.origin)

                # We check again if the release is not in the origin workspace
                click.secho(f"\nChecking if deleting orphan '{release.name}' '{release.id}' is safe")
                if not origin.get_release_by_id(release.id):
                    click.secho(
                        f"✅ Safe to delete. Release '{release.id}' not in origin {origin.id} releases {origin.releases}'"
                    )
                    if click.confirm("\nDo you want to delete it?\n"):
                        # TODO: This will only mark the release as soft-deleted, but will not remove it from Redis.
                        # Shouldn't we remove it from Redis directly?
                        asyncio.run(release.delete())
                        release.save()
                        click.secho(f"Deleted: Release '{release.id}'")
                else:
                    click.secho(
                        f"⚠️ Not safe to delete check origin releases. Release '{release.id}' in origin {origin.id} releases {origin.releases}'"
                    )
        else:
            click.secho("Skipping clean", fg="yellow")

    if click.confirm("\nDo you want to check for orphan legacy releases detected as branches or orphan branches?\n"):
        all_metadata = get_workspaces_data(None, name_needle, cluster, include_deleted)

        # not branches or releases ids. not origin
        workspaces_ids = [metadata.id for metadata in all_metadata if not metadata.origin]

        # filter by origin is workspace and releases 0 and in name has __ that is patter for releases
        possible_orphan_releases: List[WorkspaceData] = list(
            filter(
                lambda x: x.origin and x.origin in workspaces_ids and x.number_releases == 0 and "__" in x.name,
                all_metadata,
            )
        )

        possible_orphan_legacy_releases: List[WorkspaceData] = []
        # filter metadata not a release
        for release in possible_orphan_releases:
            origin = Workspace.get_by_id(release.origin)
            if origin and not origin.deleted:
                release_in_origin = origin.get_release_by_id(release.id)
                if not release_in_origin:
                    possible_orphan_legacy_releases.append(release)

        column_names = ["name", "id", "cluster", "database", "origin"]
        click.secho("\nList of possible orphan legacy releases in the target cluster", bold=True)
        click.echo(
            format_smart_table(
                [
                    (release.name, release.id, release.cluster, release.database, release.origin)
                    for release in possible_orphan_legacy_releases
                ],
                column_names=column_names,
            )
        )
        if not possible_orphan_legacy_releases:
            click.secho("No orphan legacy releases detected", fg="blue")
        elif click.confirm("\nDo you want review them to clean?\n"):
            for possible_release in possible_orphan_legacy_releases:
                release = Workspace.get_by_id(possible_release.id)
                click.secho(f"\nChecking if deleting orphan '{release.name}' '{release.id}' is safe")
                client = HTTPClient(release.database_server)
                _, body = client.query_sync("SHOW DATABASES FORMAT JSON")
                databases = json.loads(body)["data"]
                if release.database not in [database["name"] for database in databases]:
                    click.secho(
                        f"🚨 It should be safe to delete. Database '{release.database}' does not exist in cluster '{release.cluster}'."
                        "But still do a manual check to ensure it's safe to delete"
                    )
                    if not click.confirm(f"Do you want to delete orphan release {release.name} from redis?"):
                        click.secho("Skipping clean", fg="yellow")
                        continue

                    Workspace._delete(release.id)
                    click.secho(f"Deleted {release.name}", fg="green")
                else:
                    click.secho(
                        f"⚠️ Database '{release.database}' exists in cluster '{release.cluster}' review manually",
                        fg="yellow",
                    )
        else:
            click.secho("Skipping clean", fg="yellow")
