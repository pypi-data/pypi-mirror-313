import pickle
import sys
import time
from datetime import datetime, timedelta
from typing import Optional

import click

from tinybird.job import JOB_TTL_IN_HOURS, Job, JobExecutor, JobKind
from tinybird.populates.job import PopulateJob
from tinybird.raw_events.raw_events_batcher import raw_events_batcher
from tinybird.user import User as Workspace

from ... import common
from ..cli_base import cli


def check_job(job: Optional[Job]) -> Job:
    if not isinstance(job, Job):
        click.secho("Job is not a valid Job object", fg="red", err=True)
        sys.exit(1)
    return job


@cli.command()
@click.argument("jobs", nargs=-1)
@click.option("--error", "-e", required=True)
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
@click.option(
    "--job-kind",
    type=str,
    default=None,
    help="Only mark as error jobs of this kind, e.g. import, populateview, copy, sink, etc.",
)
@click.option("--workspace-id", type=str, default=None, help="Only mark as error jobs for this Workspace ID")
@click.option("--only-waiting", is_flag=True, default=False)
@click.option(
    "--unlink-on-error/--no-unlink-on-error",
    is_flag=True,
    default=False,
    help="On populate jobs, use --unlink-on-error to try to unlink the Materialized View when marking the job as error",
)
def mark_job_error(jobs, error, config, job_kind, workspace_id, only_waiting, unlink_on_error):
    """Mark jobs as errors and remove them from the Redis queue"""
    conf, redis_client = common.setup_redis_client(config)
    redis_config = common.get_redis_config(conf)
    jobs = set(jobs)
    if job_kind and job_kind not in vars(JobKind).values():
        click.secho(f"Invalid job kind '{job_kind}'", fg="red", err=True)
        click.secho(
            f"Valid kinds of jobs are: {', '.join([v for v in vars(JobKind).values() if isinstance(v, str) and v != 'tinybird.job'])}",
            fg="red",
            err=True,
        )
        sys.exit(1)

    job_executor = JobExecutor(
        redis_client=redis_client,
        redis_config=redis_config,
    )

    # Ensure all Redis queues are discovered from the ALIVE_QUEUES. Since we're not running
    # the consumer which discovers them automagically and we're not using put_job to creat
    # the JobThreadPoolExecutors, we need to explicitly discover them.
    job_executor.check_for_new_queues()

    # Raw Events Batcher to send jobs_log updates
    hfi_host = conf.get("api_host", "")
    raw_events_batcher.init(api_host=hfi_host)

    raw_events_batcher.start()

    if workspace_id:
        workspace_jobs = set()
        workspace = Workspace.get_by_id(workspace_id)
        if not workspace:
            click.secho(f"Workspace with id '{workspace_id}' not found", fg="red", err=True)
            sys.exit(1)
        all_jobs = job_executor.get_pending_jobs()
        for job in all_jobs:
            if (
                (hasattr(job, "workspace_id") and job.workspace_id == workspace.id)
                or (hasattr(job, "database") and job.database == workspace.database)
                or (hasattr(job, "user_id") and job.user_id == workspace.id)
            ):
                workspace_jobs.add(job.id)
        if workspace_jobs:
            click.secho(
                f"Added {len(workspace_jobs)} jobs from Workspace '{workspace.name}' ({workspace.id}) to mark as error",
                fg="green",
                bold=True,
            )
        else:
            click.secho(f"No jobs found for Workspace '{workspace.name}' ({workspace.id})", fg="yellow", bold=True)
        jobs = jobs.union(workspace_jobs)

    if not jobs:
        click.secho("No jobs specified", fg="red", err=True)
        sys.exit(1)

    def _print_info(j):
        return {"job_id": j.id, "status": j.status, "result": j.result}

    number_of_jobs_marked = 0
    for job_id in jobs:
        j = Job.get_by_id(job_id)
        if j:
            if job_kind and j.kind != job_kind:
                click.secho(
                    f"Skipping job '{j.id}' of kind '{j.kind}' (only marking as error '{job_kind}')", fg="yellow"
                )
                continue
            if only_waiting and j.status != "waiting":
                click.secho(
                    f"Skipping job '{j.id}' with status '{j.status}' (only marking as error waiting jobs)", fg="yellow"
                )
                continue
            if j.kind == "populateview":
                if unlink_on_error:
                    click.secho(
                        "Marking populates as error means it could also unlink the materialized views.",
                        bold=True,
                        fg="yellow",
                    )
                    if not click.confirm("Are you sure you want to continue marking this job as an error?"):
                        continue
                else:
                    PopulateJob.prevent_unlink_on_error(job_id)
                    j = Job.get_by_id(job_id)

            j = check_job(j)

            click.secho(
                f"Marking {j.kind} job '{j.id}' with error '{error}' and removing it from Redis queue", fg="green"
            )
            click.secho(f"   Before: {_print_info(j)}")
            j.mark_as_error({"error": error})
            j = Job.get_by_id(job_id)
            j = check_job(j)
            click.secho(f"   After:  {_print_info(j)}")
            number_of_jobs_marked += 1

            try:
                executor = job_executor.get_job_executor(j)
                executor._redis_queue.task_done(
                    job_id
                )  # task_done already removes the job from the WIP queue if present
                executor._redis_queue.rem_queue(job_id)
                click.secho("   Job removed from Redis queue")
            except Exception as e:
                click.secho(f"  Error removing job from Redis queue: {e}", fg="red", err=True)
                pass
        else:
            click.secho(f"Could not mark job as errored: '{job_id}' not found", fg="red", err=True)
    click.secho(f"Marked {number_of_jobs_marked} jobs as an error", fg="green", bold=True)
    raw_events_batcher.shutdown()


@cli.command()
@click.option("--older-than-hours", type=int, default=JOB_TTL_IN_HOURS)
@click.option("--workspace_id", type=str, default=None, help="Only remove jobs for this Workspace ID")
@click.option("--dry-run", is_flag=True, default=False)
@click.option(
    "--adjust-expiration/--do-not-adjust-expiration",
    is_flag=True,
    default=True,
    help=(
        "Change the expiration of existing jobs that are not old enough for removal but will get older than"
        " --older-than-hours otherwise."
    ),
)
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
def delete_old_jobs(older_than_hours, workspace_id, dry_run, adjust_expiration, config):
    """Purge old jobs on redis"""
    if dry_run:
        click.secho("DRY RUN mode: commands will NOT execute", bg="blue", fg="white")

    _, redis_client = common.setup_redis_client(config)

    text = f"This script will delete jobs from Redis older than {older_than_hours} hours"
    if adjust_expiration:
        text += f" and set expire of the rest to their remaining time of {older_than_hours} hours"

    if workspace_id:
        try:
            workspace = Workspace.get_by_id(workspace_id)
            text += f" for the workspace={workspace_id} ({workspace.name})"
        except Exception:
            click.secho(f"Could not find workspace {workspace_id}", fg="red")
            sys.exit(1)

    click.secho(text, bg="red", fg="white")
    click.confirm("Do you want to continue?", abort=True)
    now = datetime.utcnow()
    older_than_seconds = older_than_hours * 3600
    delta = timedelta(seconds=older_than_seconds)
    ns = "jobs"
    deleted = 0
    expired = 0

    for k in redis_client.scan_iter(f"{ns}:*", count=10000):
        parts = k.decode().split(":")
        if len(parts) != 2:
            continue  # skip, for instance, :last_updated$ keys
        key = k.decode()
        last_updated_key = f"{key}:last_updated"
        b = redis_client.get(last_updated_key)
        last_updated = None
        if b:
            try:
                last_updated = float(b)
            except Exception:
                pass
        if last_updated:
            age = now - datetime.fromtimestamp(last_updated)

            if workspace_id:
                b = redis_client.get(key)
                job = None
                try:
                    job = pickle.loads(b)
                except Exception as e:
                    click.secho(f"Found invalid job for key={key}, could not load: {e}", fg="magenta")
                if job and hasattr(job, "user_id") and job.user_id != workspace_id:
                    click.secho(
                        (
                            f"{'[DRY RUN] ' if dry_run else ''}Skipping job from other Workspace. key={key},"
                            f" age={age}, workspace={job.user_id}"
                        ),
                        fg="yellow",
                    )
                    continue

            if age > delta:
                click.secho(f"{'[DRY RUN] ' if dry_run else ''}Deleting key={key}, age={age}", fg="red")
                deleted += 1
                if not dry_run:
                    redis_client.delete(key, last_updated_key)
            else:
                ttl = redis_client.ttl(key)
                remaining_ttl = int(older_than_seconds - age.total_seconds())
                if adjust_expiration:
                    click.secho(
                        (
                            f"{'[DRY RUN] ' if dry_run else ''}Setting expire for key={key}, age={age}, old_ttl={ttl},"
                            f" new_ttl={remaining_ttl}"
                        ),
                        fg="yellow",
                    )
                    expired += 1
                    if not dry_run:
                        redis_client.expire(key, remaining_ttl)
                        redis_client.expire(last_updated_key, remaining_ttl)
        else:
            ttl = redis_client.ttl(key)
            click.secho(f"Expiring key={key}, age=unknown, ttl={ttl}", fg="yellow")
            if not dry_run:
                if ttl > older_than_seconds:
                    redis_client.expire(key, older_than_seconds)
                redis_client.delete(last_updated_key)
    click.secho(f"Deleted {deleted} jobs, set expired for {expired} jobs", bg="blue", fg="white")


@cli.command()
@click.option(
    "--batch-size", type=int, default=10_000, help="The number of children to remove from the set in each iteration"
)
@click.option(
    "--batch-sleep-seconds", type=float, default=0.5, help="The wait in seconds between each remove iteration"
)
@click.option("--dry-run", is_flag=True, default=False)
def remove_jobs_children(batch_size, batch_sleep_seconds, dry_run, config):
    """Removes children from jobs' owner Redis sorted set.

    As the sets might have in the orders of million of objects, the script does the removal in several iterations.
    You can adjust the iterations pace with --batch-size and --batch-sleep-seconds.

    For more details, check https://gitlab.com/tinybird/analytics/-/issues/3773.
    """
    if dry_run:
        click.secho("DRY RUN mode: commands will NOT execute", bg="blue", fg="white")

    click.secho("This script will remove children jobs from their owners", bg="red", fg="white")
    click.secho(f"Batch size={batch_size}, sleep={batch_sleep_seconds}s", bg="blue", fg="white")
    click.confirm("Do you want to continue?", abort=True)

    _, redis_client = common.setup_redis_client(config)

    def remove_to_end(k, start):
        start_time = time.monotonic()
        if not dry_run:
            redis_client.zremrangebyrank(k, start, -1)
        click.secho(
            (
                f"\t{'[DRY RUN] ' if dry_run else ''}Removed from start={start}, to stop={-1}, took"
                f" {round(time.monotonic() - start_time, 3)}s"
            ),
            fg="blue",
        )

    for k in redis_client.scan_iter(f"{Job.__namespace__}:owner:*", count=10000):
        set_cardinality = redis_client.zcard(k)
        if set_cardinality > Job.__owner_max_children__:
            click.secho(f"{'[DRY RUN] ' if dry_run else ''}Pruning key={k}, cardinality={set_cardinality}", fg="red")
            for i in range(set_cardinality, Job.__owner_max_children__, -batch_size):
                remove_to_end(k, i)
                time.sleep(batch_sleep_seconds)
            remove_to_end(k, Job.__owner_max_children__)
