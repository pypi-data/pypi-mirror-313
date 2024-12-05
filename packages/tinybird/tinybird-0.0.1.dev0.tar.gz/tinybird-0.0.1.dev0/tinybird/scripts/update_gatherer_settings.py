import logging
import sys
from pathlib import Path
from typing import Any, Callable, Optional

import click
from click.decorators import argument as click_argument
from click.decorators import group as click_group
from click.decorators import option as click_option

from tinybird.app import get_config
from tinybird.constants import BillingPlans
from tinybird.data_connector import DataConnector, DataLinker, DataSink
from tinybird.model import retry_transaction_in_case_of_concurrent_edition_error_sync
from tinybird.redis_config import get_redis_config
from tinybird.user import User as Workspace
from tinybird_shared.redis_client.redis_client import TBRedisClientSync

SUPPORTED_SETTINGS = [
    "use_gatherer",
    "gatherer_wait_false_traffic",
    "gatherer_wait_true_traffic",
    "gatherer_deduplication",
]
VALUE_TYPES_BY_SETTING = {
    "use_gatherer": "bool",
    "gatherer_wait_false_traffic": "float",
    "gatherer_wait_true_traffic": "float",
    "gatherer_deduplication": "bool",
}

logging.basicConfig(level=logging.INFO)


class UnsupportedSettingException(Exception):
    pass


class UnsupportedPlanFilterException(Exception):
    pass


def update_gatherer_settings(
    changes: dict[str, Any],
    file: Optional[Path] = None,
    plans: Optional[list[str]] = None,
    cond: Optional[Callable] = None,
    interactive: bool = False,
) -> None:
    if file is None and (plans is None or len(plans) == 0):
        logging.info("No file or plan specified, setting will be updated in all workspaces in the region")
        _ask_for_confirmation(interactive)

    workspaces = get_workspaces_to_update(file, plans, cond=cond)

    workspace_descriptions = map(_get_workspace_description, workspaces)
    workspaces_str = "\n".join(workspace_descriptions)
    logging.info(
        f"Applying changes (setting, value): {changes} for the following {len(workspaces)} workspaces:\n\n{workspaces_str}"
    )
    _ask_for_confirmation(interactive)

    count = _update_workspaces(workspaces, changes)
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
    file: Optional[Path] = None,
    plans: Optional[list[str]] = None,
    cond: Optional[Callable] = None,
) -> list[Workspace]:
    if file is not None:
        return _get_workspaces_in_file(file, cond=cond)

    if plans is not None and len(plans) > 0:
        return _get_workspaces_by_plans(plans, cond=cond)

    return _get_all_workspaces(cond=cond)


def _get_all_workspaces(cond: Optional[Callable] = None) -> list[Workspace]:
    return [
        ws
        for ws in Workspace.get_all(include_releases=True, include_branches=True)
        if not ws.origin and (cond is None or cond(ws))
    ]


def _get_workspaces_in_file(file: Path, cond: Optional[Callable] = None) -> list[Workspace]:
    logging.info(f"Getting workspaces in file {file}")
    workspaces: list[Workspace] = []

    with open(file) as ws_file:
        workspaces_to_enable_hfi_gatherer = ws_file.readlines()

    for ws_id in workspaces_to_enable_hfi_gatherer:
        workspace = Workspace.get_by_id(ws_id.strip())
        if workspace and (cond is None or cond(workspace)):
            workspaces.append(workspace)

    return workspaces


def _get_workspaces_by_plans(plans: list[str], cond: Optional[Callable] = None) -> list[Workspace]:
    logging.info(f"Getting workspaces of plans: {plans}")
    workspaces: list[Workspace] = []

    all_workspaces = [ws for ws in Workspace.get_all(include_releases=True, include_branches=True) if not ws.origin]
    for workspace in all_workspaces:
        if workspace.plan in plans and (cond is None or cond(workspace)):
            workspaces.append(workspace)

    return workspaces


def _update_workspaces(workspaces: list[Workspace], changes: dict[str, Any]) -> int:
    count = 0
    for workspace in workspaces:
        try:

            @retry_transaction_in_case_of_concurrent_edition_error_sync()
            def _update_workspace(workspace: Workspace, changes: dict[str, Any]) -> None:
                with Workspace.transaction(workspace.id) as ws:
                    for setting_name, value in changes.items():
                        ws[setting_name] = value

            _update_workspace(workspace, changes)
            count += 1
        except Exception as ex:
            logging.warning(f"Error updating workspace {workspace.id}: {ex}")

    return count


def _parse_value(setting: str, value: str) -> Any:
    if setting not in SUPPORTED_SETTINGS:
        raise UnsupportedSettingException(f"Setting {setting} is not supported by this script.")

    expected_type = VALUE_TYPES_BY_SETTING[setting]

    if value == "None":
        return None

    if expected_type == "bool":
        if value.lower() not in ["true", "false"]:
            raise ValueError(f"Value {value} has the wrong type. Expected type: {VALUE_TYPES_BY_SETTING[setting]}")
        return value.lower() == "true"
    else:
        return eval(expected_type)(value)


def _ask_for_confirmation(interactive=True):
    if interactive:
        click.confirm("Do you want to continue?", abort=True)


@click_group()
def cli() -> None:
    pass


@cli.command()
@click_option("-f", "--file", type=click.Path(exists=True), help="File containing the list of workspaces IDs")
@click_option(
    "-p",
    "--plans",
    multiple=True,
    type=click.Choice(
        [BillingPlans.DEV, BillingPlans.PRO, BillingPlans.CUSTOM, BillingPlans.ENTERPRISE], case_sensitive=False
    ),
    help="Setting will be updated in workspaces in particular plans.",
)
def enable_gatherer(file: Optional[Path] = None, plans: Optional[list[str]] = None) -> None:
    def _is_not_fully_enabled(ws):
        return not ws.use_gatherer

    try:
        update_gatherer_settings({"use_gatherer": True}, file, plans, cond=_is_not_fully_enabled, interactive=True)
        sys.exit(0)
    except Exception as exc:
        logging.warning(str(exc))
        sys.exit(1)


@cli.command()
@click_argument("setting")
@click_argument("value")
@click_option("-f", "--file", type=click.Path(exists=True), help="File containing the list of workspaces IDs")
@click_option(
    "-p",
    "--plans",
    multiple=True,
    type=click.Choice(
        [BillingPlans.DEV, BillingPlans.PRO, BillingPlans.CUSTOM, BillingPlans.ENTERPRISE], case_sensitive=False
    ),
    help="Setting will be updated in workspaces in particular plans.",
)
def update_setting(setting: str, value: str, file: Optional[Path] = None, plans: Optional[list[str]] = None) -> None:
    try:
        parsed_value = _parse_value(setting, value)
        update_gatherer_settings({setting: parsed_value}, file, plans, interactive=True)
        sys.exit(0)
    except Exception as exc:
        logging.warning(str(exc))
        sys.exit(1)


@cli.command()
def disable_gatherer():
    def _is_enabled(ws):
        return ws.use_gatherer

    try:
        update_gatherer_settings({"use_gatherer": False}, None, None, cond=_is_enabled, interactive=True)
        sys.exit(0)
    except Exception as exc:
        logging.warning(str(exc))
        sys.exit(1)


if __name__ == "__main__":
    config = "/mnt/disks/tb/tinybird/pro.py"
    # config = "/home/pablo/Tinybird/analytics/pablo_conf.py"  # to test in local

    conf = get_config(config_file=config)
    redis_config = get_redis_config(conf)
    redis_client = TBRedisClientSync(redis_config)
    Workspace.config(redis_client, conf["jwt_secret"], secrets_key=conf["secrets_key"], replace_executor=None)
    DataLinker.config(redis_client)
    DataConnector.config(redis_client)
    DataSink.config(redis_client)

    cli()
