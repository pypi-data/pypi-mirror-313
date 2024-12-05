import click

from tinybird.feature_flags import FeatureFlagWorkspaces
from tinybird.user import User as Workspace

from ... import common
from ..cli_base import cli


@cli.command()
@click.option("--feature-flag", default=None)
@click.option(
    "--only-workspaces", default=None, type=str, help="comma separated list of workspaces IDs to apply the FF"
)
@click.option(
    "--except-workspaces", default=None, type=str, help="comma separated list of workspaces IDs to not apply the FF"
)
@click.option("--is-active", type=bool, default=True)
@click.option("--dry-run", is_flag=True, default=False)
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
def set_workspaces_feature_flag(feature_flag, only_workspaces, except_workspaces, is_active, dry_run, config):
    """Enable a feature flag in a workspace"""
    if dry_run:
        print("Dry run execution activated")

    if not feature_flag:
        raise Exception("Feature flag must be defined")

    workspace_feature_flags = [ff.value for ff in FeatureFlagWorkspaces]

    if feature_flag not in workspace_feature_flags:
        click.secho(f"Feature flag {feature_flag} is not valid. Valid FF are: {workspace_feature_flags}", fg="orange")

    common.setup_redis_client(config=config)

    only_workspaces = [] if not only_workspaces else only_workspaces.split(",")
    except_workspaces = [] if not except_workspaces else except_workspaces.split(",")

    workspaces = Workspace.get_all(include_branches=True, include_releases=True)

    for workspace in workspaces:
        try:
            if (only_workspaces and workspace.id in only_workspaces) or (
                except_workspaces and workspace.id not in except_workspaces
            ):
                click.secho(f"Workspace '{workspace.name}' ({workspace.id})'", fg="blue")
                feature_flags = workspace["feature_flags"]
                feature_flags.update({feature_flag: is_active})

                if not dry_run:
                    with Workspace.transaction(workspace.id) as ws:
                        ws["feature_flags"] = feature_flags

                click.secho(f"** Updated flags for workspace {workspace.name} ({workspace.id}): {feature_flags}")
            else:
                click.secho(f"Ignored Workspace '{workspace.name}' ({workspace.id})'", fg="blue")
        except Exception as e:
            click.secho(
                f"** [Error] could not update feature flag for workspace {workspace.name} ({workspace.id}): {e}"
            )


@cli.command()
@click.option("--feature-flag", default=None)
@click.option("--dry-run", is_flag=True, default=False)
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
def delete_workspaces_feature_flag(feature_flag, dry_run, config):
    """Delete a feature flag in a workspace"""
    if dry_run:
        print("Dry run execution activated")

    if not feature_flag:
        raise Exception("Feature flag must be defined")

    workspace_feature_flags = [ff.value for ff in FeatureFlagWorkspaces]

    if feature_flag not in workspace_feature_flags:
        click.secho(f"Feature flag {feature_flag} is not valid. Valid FF are: {workspace_feature_flags}", fg="orange")

    common.setup_redis_client(config=config)

    workspaces = Workspace.get_all(include_branches=True, include_releases=True)

    for workspace in workspaces:
        try:
            click.secho(f"Workspace '{workspace.name}' ({workspace.id})'", fg="blue")
            feature_flags = workspace["feature_flags"]

            if feature_flag in feature_flags:
                del feature_flags[feature_flag]

            if not dry_run:
                with Workspace.transaction(workspace.id) as ws:
                    ws["feature_flags"] = feature_flags

            click.secho(f"** Deleted flags for workspace {workspace.name} ({workspace.id}): {feature_flags}")
        except Exception as e:
            click.secho(
                f"** [Error] could not delete feature flag for workspace {workspace.name} ({workspace.id}): {e}"
            )


@cli.command()
@click.option("--feature-flag", default=None)
@click.option("--dry-run", is_flag=True, default=False)
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
def list_feature_flag_used(feature_flag, dry_run, config):
    """List the workspaces using certain feature flag"""
    if dry_run:
        print("Dry run execution activated")

    if not feature_flag:
        raise Exception("Feature flag must be defined")

    workspace_feature_flags = [ff.value for ff in FeatureFlagWorkspaces]

    if feature_flag not in workspace_feature_flags:
        click.secho(f"Feature flag {feature_flag} is not valid. Valid FF are: {workspace_feature_flags}", fg="orange")

    common.setup_redis_client(config=config)

    workspaces = Workspace.get_all(include_branches=True, include_releases=True)

    for workspace in workspaces:
        try:
            feature_flags = workspace["feature_flags"]

            if feature_flag in feature_flags:
                click.secho(
                    f"** Workspace {workspace.name} ({workspace.id}) feature_flag {feature_flag} = {workspace.feature_flags.get(feature_flag)}"
                )

        except Exception as e:
            click.secho(f"** [Error] could not check feature flag for workspace {workspace.name} ({workspace.id}): {e}")
