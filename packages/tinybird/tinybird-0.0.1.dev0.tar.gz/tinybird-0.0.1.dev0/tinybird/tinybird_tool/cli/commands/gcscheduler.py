import asyncio

import click

from tinybird.data_connector import DataConnector, DataSink
from tinybird.gc_scheduler.constants import SchedulerJobActions
from tinybird.gc_scheduler.scheduler_jobs import GCloudScheduler, GCloudSchedulerJobs

from ... import common
from ..cli_base import cli


class QueryLogEntryNotFound(Exception):
    pass


class SinksOpsLogNotFound(Exception):
    pass


@cli.command()
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
@click.option("--workspace-id", default=None, type=str, help="Update scheduler of a specific workspace")
@click.option("--gcs-job-id", default=None, type=str, help="Update scheduler of a specific google scheduler job")
@click.option("--sleep", type=float, default=None)
@common.coro
async def reset_gcscheduler_retry_config(
    config: click.Path | None, workspace_id: str | None, gcs_job_id: str | None, sleep: float = 0
):
    """Command to update the gcscheduler retry config"""
    settings, _ = common.setup_redis_client(config)

    GCloudScheduler.config(
        settings.get("gcscheduler_project_id", ""),
        settings.get("gcscheduler_region", ""),
        settings.get("gcscheduler_service_account_key_location", ""),
    )

    # Update by job id
    if gcs_job_id:
        click.echo(f"** Updating {gcs_job_id}")
        await GCloudSchedulerJobs.update_job_status(action=SchedulerJobActions.UPDATE, job_name=gcs_job_id)
        click.echo("Done")
        return

    # Update by workspace id
    if workspace_id:
        data_connectors = DataConnector.get_all_by_owner_and_service(owner=workspace_id, service="gcscheduler")
        for data_connector in data_connectors:
            gcscheduler_data_sinks = data_connector.get_sinks()
            for data_sink in gcscheduler_data_sinks:
                await _update_data_sink_job(data_sink=data_sink, sleep=sleep)
        return

    # Update all
    all_data_sinks = DataSink.get_all()
    gcscheduler_data_sinks = [data_sink for data_sink in all_data_sinks if data_sink.service == "gcscheduler"]
    for data_sink in gcscheduler_data_sinks:
        await _update_data_sink_job(data_sink=data_sink, sleep=sleep)


async def _update_data_sink_job(data_sink: DataSink, sleep: float = 0):
    gcscheduler_job_name = data_sink.settings.get("gcscheduler_job_name")

    if not gcscheduler_job_name:
        return

    click.echo(f"** Updating {gcscheduler_job_name}")
    try:
        await GCloudSchedulerJobs.update_job_status(
            action=SchedulerJobActions.UPDATE, job_name=gcscheduler_job_name, job_settings=data_sink.settings
        )
        await asyncio.sleep(sleep)
        click.echo("Done")
    except Exception as e:
        click.echo(f"** Error updating job {gcscheduler_job_name}: {e}")
