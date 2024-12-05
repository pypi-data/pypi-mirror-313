import base64
import dataclasses
import datetime as dt
import difflib
import io
import json
import logging
import os
import typing
from typing import Any, Optional

import click
import google.auth
from tabulate import tabulate

from tinybird.data_connector import DataConnectors, DataLinker
from tinybird.ingest.cdk_utils import normalize_version
from tinybird.limits import DEFAULT_CDK_VERSION
from tinybird.syncasync import async_to_sync
from tinybird.user import User as Workspace
from tinybird.user import Users as Workspaces

from ... import common
from ...composer import (
    DEFAULT_BACKUP_DIR,
    ComposerCDKDAGConfig,
    ComposerCDKDAGFileReader,
    NoDAGBackupFound,
    PatternNotFound,
)
from ..cli_base import cli

LOG_LEVEL = logging.DEBUG if os.environ.get("DEBUG") else logging.INFO

logger = logging.getLogger(__name__)
log_formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
log_handler = logging.StreamHandler()
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)
logger.setLevel(LOG_LEVEL)

COMPOSER_BUCKET = "europe-west3-tinybird-compo-cee9fdc8-bucket"  # DEV
# COMPOSER_BUCKET = "europe-west3-tinybird-compo-fb41b036-bucket"   # PRO


class DataclassJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)  # type: ignore
        if isinstance(obj, dt.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        return super().default(obj)


@cli.group()
def cdk_dag():
    """Tinybird cdk commands"""


@cdk_dag.command(name="download-file")
@click.argument("workspace-id", type=str)
@click.argument("datasource-id", type=str)
@click.option("-b", "--bucket", type=str, envvar="COMPOSER_BUCKET", help="GCS bucket where composer stores DAG files")
def cdk_dag_download_file(workspace_id: str, datasource_id: str, bucket: str):
    credentials, _ = google.auth.default()
    reader = ComposerCDKDAGFileReader(credentials, bucket)
    dag_file = reader.get_dag_file(workspace_id, datasource_id)
    click.echo(reader.read_dag_file(dag_file).read())


@cdk_dag.command(name="get")
@click.argument("workspace-id", type=str)
@click.argument("datasource-id", type=str)
@click.option("-b", "--bucket", type=str, envvar="COMPOSER_BUCKET", help="GCS bucket where composer stores DAG files")
def cdk_dag_get(workspace_id: str, datasource_id: str, bucket: str):
    credentials, _ = google.auth.default()
    reader = ComposerCDKDAGFileReader(credentials, bucket)
    dag_file = reader.get_dag_file(workspace_id, datasource_id)
    click.echo(reader.get_dag_config(dag_file).model_dump_json())


def _list_dag_configs(
    reader: ComposerCDKDAGFileReader,
    workspace_id: Optional[str] = None,
    version: Optional[str] = None,
    kind: Optional[str] = None,
    warning: bool = False,
) -> typing.Iterable[ComposerCDKDAGConfig]:
    for dag_file in reader.list_dag_files(workspace_id=workspace_id):
        try:
            dag_config = reader.get_dag_config(dag_file)
            if (not version or dag_config.container_version == version) and (not kind or dag_config.kind == kind):
                yield dag_config
        except PatternNotFound as err:
            logger.error(f"DAG CONFIG PARSING ERROR: {err}")
            if not warning:
                raise
        except FileNotFoundError as err:
            logger.error(f"Failed to read DAG config file: {err}")
            if not warning:
                raise
        except Exception as err:
            logger.error(f"Failed to read DAG config file: {err}")
            if not warning:
                raise


@cdk_dag.command(name="list")
@click.option("-w", "--workspace-id", type=str, help="Only include dags config files for this workspace id")
@click.option("-v", "--version", type=str, help="Only show dags config files for this version")
@click.option(
    "-k", "--kind", type=click.Choice(["bigquery", "snowflake"]), help="Only show dags config files for this version"
)
@click.option("--check", is_flag=True, help="Validate ")
@click.option("--warning", is_flag=True, help="Print parse errors as warnings")
@click.option("-b", "--bucket", type=str, envvar="COMPOSER_BUCKET", help="GCS bucket where composer stores DAG files")
def cdk_dag_list(
    workspace_id: Optional[str],
    version: Optional[str],
    kind: Optional[str],
    check: bool,
    warning: bool,
    bucket: str,
):
    credentials, _ = google.auth.default()
    reader = ComposerCDKDAGFileReader(credentials, bucket)
    dag_configs = _list_dag_configs(reader, workspace_id=workspace_id, version=version, kind=kind, warning=warning)
    for dag_config in dag_configs:
        if check:
            list(map(logger.warning, reader.check_dag_config(dag_config)))
        else:
            print(dag_config.model_dump_json())


@cdk_dag.command(name="sync-dag-config-to-redis")
@click.option("-w", "--workspace-id", type=str, help="Only include dags config files for this workspace id")
@click.option("-b", "--bucket", type=str, envvar="COMPOSER_BUCKET", help="GCS bucket where composer stores DAG files")
@click.option("-r", "--region", type=str, help="region hint to filter dags by tb_endpoint. e.g. us-east.aws")
@click.option("--yes", is_flag=True, default=False, help="Do not ask for confirmation")
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Run the command without updating Redis",
)
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
def cdk_dag_sync_dag_config_to_redis(
    workspace_id: Optional[str], bucket: str, region: str, dry_run: bool, yes: bool, config: Any
):
    common.setup_redis_client(config=config)

    if dry_run:
        click.echo("** [DRY_RUN] mode")

    credentials, _ = google.auth.default()
    reader = ComposerCDKDAGFileReader(credentials, bucket)
    dag_configs = _list_dag_configs(reader, workspace_id=workspace_id if workspace_id else None, warning=True)
    i = 0
    for dag_config in dag_configs:
        i += 1
        click.echo(f"*********** {i}")
        try:
            if region and region not in dag_config.tb_endpoint:
                continue
            else:
                click.echo(f"Found DAG in region {region}")

            cron = dag_config.schedule_interval
            mode = dag_config.mode
            encoded_query = dag_config.query

            workspace_id = dag_config.workspace_id
            datasource_id = dag_config.datasource_id

            workspace = Workspace.get_by_id(workspace_id)
            if not workspace:
                click.echo(f"** Error: Workspace {workspace_id} not found")
                continue

            if workspace.is_branch or workspace.is_release_in_branch:
                continue

            datasource = workspace.get_datasource(datasource_id)
            if not datasource:
                click.echo(f"** Error: Data Source {datasource_id} not found")
                continue

            if dag_config.kind == DataConnectors.BIGQUERY:
                ds_service_conf = {
                    "CRON": cron,
                    "MODE": mode,
                    "SQL_QUERY": encoded_query,
                    "SQL_QUERY_AUTOGENERATED": dag_config.query_autogenerated,
                }

                if datasource.service_conf:
                    is_synced = all(
                        datasource.service_conf.get(key, "") == value for key, value in ds_service_conf.items()
                    )
                else:
                    is_synced = False

                if is_synced:
                    click.echo(f"** BigQuery Data Source {datasource_id} is synced, nothing to do!")
                    continue
                else:
                    click.echo(
                        f"** BigQuery Data Source {datasource_id} unsynced: DAG: {ds_service_conf} != DS: {datasource.service_conf}"
                    )
                    if datasource.service_conf:
                        datasource.service_conf.update(ds_service_conf)
                    else:
                        datasource.service_conf = ds_service_conf

                if dry_run:
                    click.echo(f"** [DRY_RUN] BigQuery Data Source {datasource_id} will be synced")
                else:
                    if yes or click.confirm("Update BigQuery Data Source?"):
                        result = Workspaces.update_datasource(workspace, datasource)
                        if not result:
                            click.echo(f"** BigQuery Data Source {datasource_id} not updated")
                        else:
                            click.echo(f"** BigQuery Data Source {datasource_id} updated")
            elif dag_config.kind == DataConnectors.SNOWFLAKE:
                try:
                    linker = DataLinker.get_by_datasource_id(datasource.id)
                except Exception:
                    click.echo(
                        f"** Error: Data Linker for Snowflake Data Source {datasource_id} not found. Workspace {workspace_id} =>  {dag_config}"
                    )
                    continue

                if linker.service != DataConnectors.SNOWFLAKE:
                    click.echo("** Error: Data Linker should be snowflake kind")
                    continue

                linker_settings = {
                    "cron": dag_config.schedule_interval,
                    "mode": dag_config.mode,
                    "query": base64.b64decode(dag_config.query).decode("ascii"),
                    "query_autogenerated": dag_config.query_autogenerated,
                    "stage": dag_config.sfk_settings.stage,
                }

                is_synced = all(linker.settings.get(key) == value for key, value in linker_settings.items())

                if is_synced:
                    click.echo(f"** Snowflake Data Source {datasource_id} is synced, nothing to do!")
                    continue
                else:
                    click.echo(
                        f"** Snowflake Data Source {datasource_id} unsynced: DAG: {linker_settings} != DS: {linker.settings}"
                    )

                if dry_run:
                    click.echo(f"** [DRY_RUN] Snowflake Data Source {datasource_id} will be synced")
                else:
                    if yes or click.confirm("Update Snowflake Data Linker?"):
                        async_to_sync(DataLinker.update_settings_async)(linker, linker_settings)
                        click.echo(f"** Snowflake Data Source {datasource_id} updated")
            else:
                click.echo(
                    "Only supported kinds are bigquery and snowflake, others need implementation.", err=True, nl=False
                )
        except Exception as e:
            click.echo(f"Unhandled exception: {str(e)}")


@cdk_dag.command(name="backup-create")
@click.argument("workspace-id", type=str)
@click.argument("datasource-id", type=str)
@click.option("--backup-dir", type=str, default=DEFAULT_BACKUP_DIR, help="Directory where the backups will be stored")
@click.option("-b", "--bucket", type=str, envvar="COMPOSER_BUCKET", help="GCS bucket where composer stores DAG files")
def cdk_dag_backup_create(workspace_id: str, datasource_id: str, backup_dir: str, bucket: str):
    credentials, _ = google.auth.default()
    reader = ComposerCDKDAGFileReader(credentials, bucket)

    dag_file = reader.get_dag_file(workspace_id, datasource_id)
    reader.backup_dag_file(backup_dir, dag_file)


@cdk_dag.command(name="backup-many")
@click.option("-w", "--workspace-id", type=str, help="Only include dags config files for this workspace id")
@click.option("--backup-dir", type=str, default=DEFAULT_BACKUP_DIR, help="Directory where the backups will be stored")
@click.option("-b", "--bucket", type=str, envvar="COMPOSER_BUCKET", help="GCS bucket where composer stores DAG files")
def cdk_dag_backup_create_many(workspace_id: Optional[str], backup_dir: str, bucket: str):
    credentials, _ = google.auth.default()
    reader = ComposerCDKDAGFileReader(credentials, bucket)
    for dag_file in reader.list_dag_files(workspace_id=workspace_id):
        reader.backup_dag_file(backup_dir, dag_file)


@cdk_dag.command(name="backup-get")
@click.argument("workspace-id", type=str)
@click.argument("datasource-id", type=str)
@click.option("--id", type=str, help="Only include dags config files for this workspace id")
@click.option("--backup-dir", type=str, default=DEFAULT_BACKUP_DIR, help="Directory where the backups will be stored")
@click.option("-b", "--bucket", type=str, envvar="COMPOSER_BUCKET", help="GCS bucket where composer stores DAG files")
def cdk_dag_backup_get(workspace_id: str, datasource_id: str, id: Optional[str], backup_dir: str, bucket: str):
    credentials, _ = google.auth.default()
    reader = ComposerCDKDAGFileReader(credentials, bucket)
    try:
        if id:
            backup = reader.get_dag_backup(backup_dir, workspace_id, datasource_id, id)
        else:
            backup = reader.get_latest_dag_backup(backup_dir, workspace_id, datasource_id)
    except NoDAGBackupFound as err:
        print(err)
        exit(1)
    print(backup.dag_file_content)


@cdk_dag.command(name="backup-list")
@click.option("-w", "--workspace-id", type=str, help="Only include dags config files for this workspace id")
@click.option("-d", "--datasource-id", type=str, help="Only include dags config files for this workspace id")
@click.option("--backup-dir", type=str, default=DEFAULT_BACKUP_DIR, help="Directory where the backups will be stored")
@click.option("--json", "as_json", is_flag=True, help="Print each record as json")
@click.option("-b", "--bucket", type=str, envvar="COMPOSER_BUCKET", help="GCS bucket where composer stores DAG files")
def cdk_dag_backup_list(
    workspace_id: Optional[str], datasource_id: Optional[str], backup_dir: str, as_json: bool, bucket: str
):
    credentials, _ = google.auth.default()
    reader = ComposerCDKDAGFileReader(credentials, bucket)
    backups = reader.list_backups(backup_dir, workspace_id, datasource_id)
    if as_json:
        for backup in backups:
            print(backup.model_dump_json(exclude={"dag_file_content"}))
    else:
        print(tabulate((backup.model_dump(exclude={"dag_file_content"}) for backup in backups), headers="keys"))


def _upgrade_dag(
    reader: ComposerCDKDAGFileReader,
    config: ComposerCDKDAGConfig,
    version: str,
    apply: bool,
    backup: bool,
    backup_dir: str,
    envvars: Optional[dict] = None,
) -> None:
    dag_file = config.dag_file
    logger.info("Starting upgrade of dag %s. Versions: [%s -> %s]", dag_file.dag_id, config.container_version, version)
    logger.info("Calculating dagfile diff...")
    current_dag_file_content = reader.read_dag_file(dag_file)
    updated_dag_file_content = reader.render_updated_dag_file(config, version=version, envvars=envvars)
    for line in difflib.unified_diff(
        current_dag_file_content.readlines(), io.StringIO(updated_dag_file_content).readlines()
    ):
        click.echo(line, err=True, nl=False)

    click.confirm("Do you want to apply the displayed changes?", abort=True)

    if not apply:
        click.echo(updated_dag_file_content)
        return

    if backup:
        logger.info("Backing up DAG file...")
        reader.backup_dag_file(backup_dir, dag_file)
    reader.overwrite_dag_file(dag_file, updated_dag_file_content)


def _parse_envvars(ctx, param, value):
    if value is None:
        return {}

    envvars = value.split(" ")
    result = {}
    for envvar in envvars:
        try:
            key, val = envvar.split("=")
            result[key] = val
        except ValueError:
            raise click.BadParameter("Key-value pairs must be in the format key=value.")
    return result


@cdk_dag.command(name="upgrade")
@click.argument("workspace-id", type=str)
@click.argument("datasource-id", type=str)
@click.option("-v", "--version", type=str, default=DEFAULT_CDK_VERSION, help="Version to bump the dag to")
@click.option("--backup", is_flag=True, default=False, help="Create a backup before upgrading the DAG")
@click.option("--apply", is_flag=True, help="Actually apply the changes")
@click.option("--backup-dir", type=str, default=DEFAULT_BACKUP_DIR, help="Directory where the backups will be stored")
@click.option("-b", "--bucket", type=str, envvar="COMPOSER_BUCKET", help="GCS bucket where composer stores DAG files")
@click.option("--envvars", callback=_parse_envvars, help="Key-value environment variables")
def cdk_dag_upgrade(
    workspace_id: str,
    datasource_id: str,
    version: str,
    backup: bool,
    apply: bool,
    backup_dir: str,
    bucket: str,
    envvars: dict,
):
    if not apply:
        msg = "Command executed in dry run mode, no changes will be applied. Please use the --apply flag to apply changes."
        logger.info(msg)
    credentials, _ = google.auth.default()
    reader = ComposerCDKDAGFileReader(credentials, bucket)
    dag_file = reader.get_dag_file(workspace_id, datasource_id)
    config = reader.get_dag_config(dag_file)
    version = normalize_version(version)
    _upgrade_dag(reader, config, version, apply, backup, backup_dir, envvars)


@cdk_dag.command(name="upgrade-many")
@click.option("-w", "--workspace-id", type=str, help="Only include dags config files for this workspace id")
@click.option(
    "-k", "--kind", type=click.Choice(["bigquery", "snowflake"]), help="Only show dags config files for this version"
)
@click.option("-v", "--from-version", type=str, help="Version to bump the dag from")
@click.option("--to-version", type=str, default=DEFAULT_CDK_VERSION, help="Version to bump the dag to")
@click.option("--backup", is_flag=True, default=False, help="Create a backup before upgrading the DAG")
@click.option("--apply", is_flag=True, help="Actually apply the changes")
@click.option("--warning", is_flag=True, help="Print parse errors as warnings")
@click.option("--backup-dir", type=str, default=DEFAULT_BACKUP_DIR, help="Directory where the backups will be stored")
@click.option("-b", "--bucket", type=str, envvar="COMPOSER_BUCKET", help="GCS bucket where composer stores DAG files")
@click.option("--envvars", callback=_parse_envvars, help="Key-value environment variables")
def cdk_dag_upgrade_many(
    workspace_id: Optional[str],
    kind: Optional[str],
    from_version: Optional[str],
    to_version: str,
    backup: bool,
    apply: bool,
    warning: bool,
    backup_dir: str,
    bucket: str,
    envvars: dict,
):
    if not apply:
        msg = "Command executed in dry run mode, no changes will be applied. Please use the --apply flag to apply changes."
        logger.info(msg)
    credentials, _ = google.auth.default()
    reader = ComposerCDKDAGFileReader(credentials, bucket)
    dag_configs = list(
        _list_dag_configs(reader, workspace_id=workspace_id, version=from_version, kind=kind, warning=warning)
    )
    if not dag_configs:
        logger.info("No DAGs selected for upgrade. Exiting...")
        return
    logger.info("The following DAGs will be upgraded:")
    to_version = normalize_version(to_version)
    for config in dag_configs:
        if config.container_version == to_version:
            logger.debug("DAG %s is already on version %s, skipping.", config.dag_file.dag_id, to_version)
        else:
            logger.info(" - %s [%s -> %s]", config.dag_file.dag_id, config.container_version, to_version)

    click.confirm("Do you want to proceed? Confirmation will be asked for each individual DAG", abort=True)
    for config in dag_configs:
        if config.container_version != to_version:
            _upgrade_dag(reader, config, to_version, apply, backup, backup_dir, envvars)
