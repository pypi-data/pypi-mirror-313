import logging
import sys
from typing import Any, Callable, Optional

import click
from click.decorators import argument as click_argument
from click.decorators import group as click_group
from click.decorators import option as click_option

from tinybird.app import get_config
from tinybird.constants import BillingPlans
from tinybird.data_connector import DataConnector, DataLinker, DataSink
from tinybird.feature_flags import FeatureFlagWorkspaces
from tinybird.redis_config import get_redis_config
from tinybird.user import User as Workspace
from tinybird_shared.redis_client.redis_client import TBRedisClientSync

logging.basicConfig(level=logging.INFO)


class UnsupportedSettingException(Exception):
    pass


class UnsupportedPlanFilterException(Exception):
    pass


def update_workspace_settings(
    changes: dict[str, Any],
    check: bool,
    plans: Optional[list[str]] = None,
    cond: Optional[Callable] = None,
    interactive: bool = False,
) -> None:
    if (plans is None or len(plans) == 0) and cond is None:
        logging.info("No plan or condition specified, setting will be updated in all workspaces in the region")
        _ask_for_confirmation(interactive)

    workspaces = get_workspaces_to_update(plans, cond=cond)

    workspace_descriptions = map(_get_workspace_description, workspaces)
    workspaces_str = "\n".join(workspace_descriptions)
    logging.info(
        f"Applying changes (setting, value): {changes} for the following {len(workspaces)} workspaces:\n\n{workspaces_str}"
    )
    _ask_for_confirmation(interactive)

    count = _update_workspaces(workspaces, changes, check)
    logging.info(f"Setting updated for {count} workspaces")


def _get_workspace_description(workspace: Workspace) -> str:
    shown_bits = [
        str(workspace.id),
        str(workspace.name),
        str(workspace.use_gatherer),
        str(workspace.plan),
        str(workspace.organization_id),
        str(workspace.created_at),
    ]
    return "\t".join(shown_bits)


def get_workspaces_to_update(
    plans: Optional[list[str]] = None,
    cond: Optional[Callable] = None,
) -> list[Workspace]:
    if plans is not None and len(plans) > 0:
        return _get_workspaces_by_plans(plans, cond=cond)

    return _get_all_workspaces(cond=cond)


def _get_all_workspaces(cond: Optional[Callable] = None) -> list[Workspace]:
    return [
        workspace
        for workspace in Workspace.get_all(include_releases=True, include_branches=True)
        if not workspace.origin and (cond is None or cond(workspace))
    ]


def _get_workspaces_by_plans(plans: list[str], cond: Optional[Callable] = None) -> list[Workspace]:
    logging.info(f"Getting workspaces of plans: {plans}")
    workspaces: list[Workspace] = []

    all_workspaces = [
        workspace
        for workspace in Workspace.get_all(include_releases=True, include_branches=True)
        if not workspace.origin
    ]
    for workspace in all_workspaces:
        if workspace.plan in plans and (cond is None or cond(workspace)):
            workspaces.append(workspace)

    return workspaces


def _update_workspaces(workspaces: list[Workspace], changes: dict[str, bool], check: bool) -> int:
    count = 0
    for workspace in workspaces:
        try:
            with Workspace.transaction(workspace.id) as workspace:
                _change_settings(workspace, changes, check)
            count += 1
        except Exception as ex:
            logging.warning(f"Error updating workspace {workspace.id}: {ex}")

    return count


def _change_settings(workspace: Workspace, changes: dict[str, bool], check: bool) -> None:
    feature_flags = [flag.value for flag in FeatureFlagWorkspaces]
    for setting_name, value in changes.items():
        if setting_name in workspace:
            old_value = workspace[setting_name]
            if check:
                logging.info(f"Not applying {setting_name}={value} because of --check")
            else:
                workspace[setting_name] = value
                logging.info(f"Applied {setting_name} on {workspace.id}: {old_value} -> {value}")
        elif setting_name in feature_flags:
            old_value = workspace.feature_flags.get(setting_name, None)
            if check:
                logging.info(f"Not applying ff {setting_name}={value} because of --check")
            else:
                workspace.feature_flags[setting_name] = value
                logging.info(f"Applied ff {setting_name} on {workspace.id}: {old_value} -> {value}")
        else:
            raise ValueError(f"Setting {setting_name} not found in {_get_workspace_description(workspace)}")


def _parse_value(value: str) -> bool:
    if value == "None":
        return True

    if value.lower() not in ["true", "false"]:
        raise ValueError(f"Value {value} should be 'true' or 'false'")
    return value.lower() == "true"


def _ask_for_confirmation(interactive=True):
    if interactive:
        click.confirm("Do you want to continue?", abort=True)


@click_group()
def cli() -> None:
    pass


@click.command()
@click_argument("setting")
@click_argument("value")
@click_option("-k", "--kafka", default=None, help="Change only on kafka workspaces")
@click_option("--check/--no-check", default=False, help="Check without applying the config")
@click_option(
    "-p",
    "--plans",
    multiple=True,
    type=click.Choice(
        [BillingPlans.DEV, BillingPlans.PRO, BillingPlans.CUSTOM, BillingPlans.ENTERPRISE], case_sensitive=False
    ),
    help="Setting will be updated in workspaces in particular plans.",
)
def update_setting(
    setting: str, value: str, kafka: Optional[str], check: bool, plans: Optional[list[str]] = None
) -> None:
    try:
        parsed_value = _parse_value(value)
        kafka_enabled = kafka is not None and kafka.lower() == "true"
        cond = _has_kafka_connection if kafka_enabled else None
        update_workspace_settings({setting: parsed_value}, check, plans, cond=cond, interactive=True)
        sys.exit(0)
    except ValueError as exc:
        logging.error(exc)
        sys.exit(1)


def _has_kafka_connection(workspace: Workspace) -> bool:
    data_connectors = DataConnector.get_all_by_owner(workspace.id, limit=100)
    for connector in data_connectors:
        for linker in connector.get_linkers():
            if linker.service == "kafka":
                return True
    return False


if __name__ == "__main__":
    config = "/mnt/disks/tb/tinybird/pro.py"

    conf = get_config(config_file=config)
    redis_config = get_redis_config(conf)
    redis_client = TBRedisClientSync(redis_config)
    Workspace.config(redis_client, conf["jwt_secret"], secrets_key=conf["secrets_key"], replace_executor=None)
    DataLinker.config(redis_client)
    DataConnector.config(redis_client)
    DataSink.config(redis_client)

    update_setting()
