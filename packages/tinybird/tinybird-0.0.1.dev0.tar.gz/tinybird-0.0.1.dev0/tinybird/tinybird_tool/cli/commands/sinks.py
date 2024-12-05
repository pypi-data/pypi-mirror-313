from datetime import datetime, timedelta, timezone
from functools import partial
from itertools import groupby
from typing import Tuple

import click
import orjson
import requests

from tinybird.ch import HTTPClient, UserAgents
from tinybird.ch_utils.exceptions import CHException
from tinybird.data_sinks.billing import BillingDetails
from tinybird.data_sinks.job import DataSinkBaseJob, DataSinkBlobStorageJob, DataSinkKafkaJob
from tinybird.data_sinks.tracker import SinksExecutionLogRecord
from tinybird.job import JobStatus
from tinybird.user import User, public

from ... import common
from ..cli_base import cli


class QueryLogEntryNotFound(Exception):
    pass


class SinksOpsLogNotFound(Exception):
    pass


@cli.command()
@click.argument("job_ids", nargs=-1)
@click.option("-c", "--check-only/--no-check-only", default=True, help="Should the script stop after the checks?")
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
def recover_sinksopslog_job_record(
    job_ids: str,
    check_only: bool,
    config: click.Path | None,
):
    """Command to generate a SinksOpsLog record and ingest it through ClickHouse after tracker failed to do so"""
    common.setup_redis_client(config)

    # Get Jobs instances from Redis
    jobs = [j for j in (DataSinkBaseJob.get_by_id(job) for job in job_ids) if j is not None]

    click.secho(f"** {len(jobs)} Job(s) Found", fg="green")
    for job in jobs:
        click.echo(f"**** {job.id} - Workspace: {job.workspace_id} - Pipe: {job.pipe_name}")

    # Group them by Database Server and cluster
    sorted_jobs = sorted(jobs, key=get_db_and_cluster_tuple)
    jobs_by_cluster = {key: list(group) for key, group in groupby(sorted_jobs, key=get_db_and_cluster_tuple)}

    # Get records from query_log
    all_query_log_entries = {}
    for (database_server, cluster), records in jobs_by_cluster.items():
        query_ids = [record.query_id for record in records if isinstance(record.query_id, str) and len(record.query_id)]
        query_log_records = get_records_from_query_log(database_server, cluster, query_ids)
        all_query_log_entries.update(
            {(database_server, record.get("query_id")): record for record in query_log_records}
        )

    if not len(all_query_log_entries):
        click.echo("No records found in system.query_log")
        return

    click.secho(f"** {len(all_query_log_entries.values())} Record(s) Found in system.query_log", fg="green")

    # Generate SinksRecord for Ingestion
    sinksopslog_records = list(map(partial(create_sinksopslog_record, all_query_log_entries), jobs))

    click.echo("\n")
    for sinksopslog_record in sinksopslog_records:
        click.echo(f"SinksOpsLog Record - Job ID: {sinksopslog_record.job_id}")
        click.echo(sinksopslog_record.model_dump_json())
        click.echo("\n")

    if check_only:
        click.secho(
            "CHECK ONLY - No records were ingested. Use --no-check-only to ingest them into ClickHouse", fg="red"
        )
        return

    # Push to ClickHouse
    push_records_to_clickhouse(sinksopslog_records)

    click.secho("Records for Jobs have been properly ingested. All good now ✨", fg="green")


def create_sinksopslog_record(
    query_log_records: dict[Tuple[str, str], dict], job: DataSinkBlobStorageJob | DataSinkKafkaJob
):
    query_log_record = query_log_records.get((job.user.database_server, job.query_id))

    if not query_log_record:
        raise QueryLogEntryNotFound(f"Query Log entry for {job.id} not found")

    job_error = job.result["error"] if job.status == JobStatus.ERROR and "error" in job.result else ""

    finished_timestamp: datetime = job.updated_at.replace(tzinfo=timezone.utc)
    elapsed_time: float = (finished_timestamp - job.created_at.replace(tzinfo=timezone.utc)).total_seconds()

    job_record = job.create_record_to_log(
        elapsed_time=elapsed_time,
        output=[],
        error=job_error,
        billing=BillingDetails(**orjson.loads(query_log_record.get("log_comment", ""))),
    )
    return job_record.model_copy(
        update={
            "read_rows": query_log_record.get("read_rows"),
            "read_bytes": query_log_record.get("read_bytes"),
            "written_rows": query_log_record.get("written_rows"),
            "written_bytes": query_log_record.get("ProfileEvents", {}).get("WriteBufferFromS3Bytes", 0),
        }
    )


def get_records_from_query_log(database_server: str, cluster: str, records: list[str]):
    client = HTTPClient(database_server)
    two_days_before_now = datetime.utcnow() - timedelta(hours=48)
    query = render_query_log_sql(cluster, two_days_before_now, records)

    try:
        _, result = client.query_sync(query, skip_unavailable_shards=1)
        return orjson.loads(result).get("data", [])
    except (CHException, requests.exceptions.RequestException, orjson.JSONDecodeError) as e:
        click.echo(f"Query to ClickHouse failed: {e}")
        return []


def interpolate_record_to_string(record: SinksExecutionLogRecord) -> str:
    return f"""
        '{record.timestamp.replace(tzinfo=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}',
        '{record.workspace_id}',
        '{record.workspace_name}',
        '{record.service}',
        '{record.pipe_id}',
        '{record.pipe_name}',
        '{record.result.value}',
        {f"'{record.error}'" if isinstance(record.error, str) and len(record.error) else 'NULL'},
        {record.elapsed_time},
        '{record.job_id}',
        {record.read_rows},
        {record.written_rows},
        {record.read_bytes},
        {record.written_bytes},
        {record.output},
        {record.parameters},
        {record.options},
        '{record.token_name}'"""


def push_records_to_clickhouse(records: list):
    public_user: User = public.get_public_user()
    client = HTTPClient(public_user.database_server, database=public_user.database)

    database_name = public_user.database
    sinks_ops_log = public_user.get_datasource("sinks_ops_log")

    if not sinks_ops_log:
        raise SinksOpsLogNotFound(f"SinksOpsLog DataSource not found for {public_user.name}")

    records_strings = f"({'),('.join(map(interpolate_record_to_string, records))})"

    sql = f"""INSERT INTO {database_name}.{sinks_ops_log.id} (`timestamp`,`workspace_id`,`workspace_name`,`service`,`pipe_id`,`pipe_name`,`result`,`error`,`elapsed_time`,`job_id`,`read_rows`,`written_rows`,`read_bytes`,`written_bytes`,`output`,`parameters`,`options`,`token_name`)
              VALUES {records_strings}"""

    try:
        headers, body = client.query_sync(sql, read_only=False)
        if "application/json" in headers["content-type"]:
            return orjson.loads(body)
        return body
    except Exception as e:
        click.secho(f' - [ERROR] Failed to run query: "{sql}"\nReason={e}', fg="red")
        raise e


def get_db_and_cluster_tuple(job):
    return (job.user.database_server, job.user.cluster)


def render_query_log_sql(cluster: str, timestamp: datetime, query_ids: list[str]):
    timestamp_str = timestamp.replace(tzinfo=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    return f"""
        SELECT
            *
        FROM
            clusterAllReplicas('{cluster}', system.query_log)
        WHERE
            http_user_agent in ('{UserAgents.SINKS.value}')
            AND event_date >= toDate('{timestamp_str}')
            AND event_time >= toDateTime('{timestamp_str}')
            AND is_initial_query == 1
            AND type > 1
            AND query_id in ('{"', '".join(query_ids)}')
        LIMIT {len(query_ids)}
        FORMAT JSON
    """
