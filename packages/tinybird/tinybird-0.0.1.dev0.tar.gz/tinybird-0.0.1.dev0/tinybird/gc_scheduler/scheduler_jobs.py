import asyncio
import hashlib
import logging
from typing import List, Optional

import google.auth
from google.api_core.exceptions import AlreadyExists, InvalidArgument, NotFound
from google.cloud import scheduler_v1beta1
from google.cloud.scheduler_v1beta1 import CloudSchedulerClient, Job, RetryConfig

from tinybird.gc_scheduler.constants import (
    DEFAULT_TIMEZONE,
    ErrorCreatingScheduleException,
    GCloudScheduleException,
    SchedulerJobActions,
)

DEFAULT_RETRY_CONFIG = RetryConfig(
    retry_count=3, max_retry_duration="60s", min_backoff_duration="10s", max_backoff_duration="60s", max_doublings=5
)


class GCloudScheduler:
    project_id: str = ""
    region: str = ""
    service_account_key_location: str = "local"

    @classmethod
    def config(
        cls,
        project_id: str,
        region: str,
        service_account_key_location: str,
    ):
        cls.project_id = project_id
        cls.region = region
        cls.service_account_key_location = service_account_key_location

    @classmethod
    def get_client(cls, scopes: Optional[List[str]] = None) -> CloudSchedulerClient:
        key_filename = cls.service_account_key_location
        if not key_filename or key_filename == "local":
            creds, _ = google.auth.default(scopes)
            return scheduler_v1beta1.CloudSchedulerClient.from_service_account_info(creds)
        return scheduler_v1beta1.CloudSchedulerClient.from_service_account_file(filename=key_filename)

    @classmethod
    def get_parent_name(cls):
        return f"projects/{cls.project_id}/locations/{cls.region}"

    @classmethod
    def get_parent(cls, scheduler_client: CloudSchedulerClient):
        return scheduler_client.common_location_path(cls.project_id, cls.region)


class GCloudSchedulerJobs:
    @staticmethod
    async def update_job_status(action: str, job_name: str, job_settings: Optional[dict] = None):
        """
        >>> import asyncio
        >>> from unittest.mock import patch, MagicMock
        >>> GCloudScheduler.config('project_id', 'region', 'local')
        >>> mock_scheduler = MagicMock()

        >>> with patch.object(GCloudScheduler, "get_client", return_value=mock_scheduler):
        ...     asyncio.run(GCloudSchedulerJobs.update_job_status(SchedulerJobActions.PAUSE, 'job_name'))
        ...     mock_scheduler.pause_job.assert_called_once_with(name='projects/project_id/locations/region/jobs/job_name')

        >>> with patch.object(GCloudScheduler, "get_client", return_value=mock_scheduler):
        ...     asyncio.run(GCloudSchedulerJobs.update_job_status(SchedulerJobActions.RESUME, 'job_name'))
        ...     mock_scheduler.resume_job.assert_called_once_with(name='projects/project_id/locations/region/jobs/job_name')

        >>> with patch.object(GCloudScheduler, "get_client", return_value=mock_scheduler):
        ...     asyncio.run(GCloudSchedulerJobs.update_job_status(SchedulerJobActions.DELETE, 'job_name'))
        ...     mock_scheduler.delete_job.assert_called_once_with(name='projects/project_id/locations/region/jobs/job_name')

        >>> job_settings = {'gcscheduler_target_url': 'https://example.com', 'cron': '0 0 * * ', 'gcscheduler_job_name': 'job_name'}
        >>> job = Job({'name': 'projects/project_id/locations/region/jobs/job_name', 'http_target': {'uri': 'https://example.com', 'http_method': 'POST'}, 'schedule': '0 0 * * ', 'time_zone': 'Etc/UTC', 'retry_config': DEFAULT_RETRY_CONFIG})
        >>> with patch.object(GCloudScheduler, "get_client", return_value=mock_scheduler):
        ...     asyncio.run(GCloudSchedulerJobs.update_job_status(action=SchedulerJobActions.UPDATE, job_name='job_name', job_settings=job_settings))
        ...     mock_scheduler.update_job.assert_called_once_with(job=job)

        >>> with patch.object(GCloudScheduler, "get_client", return_value=mock_scheduler):
        ...     with patch("google.cloud.scheduler_v1beta1.services.cloud_scheduler.client.CloudSchedulerClient.pause_job", side_effect=NotFound(message='job not found')):
        ...         asyncio.run(GCloudSchedulerJobs.update_job_status(SchedulerJobActions.PAUSE, 'job_name'))

        >>> with patch.object(GCloudScheduler, "get_client", return_value=mock_scheduler):
        ...     asyncio.run(GCloudSchedulerJobs.update_job_status('unknown', 'job_name'))
        Traceback (most recent call last):
        ...
        ValueError: Invalid action: unknown
        """
        try:
            scheduler_client = GCloudScheduler.get_client()
            gc_name = f"{GCloudScheduler.get_parent_name()}/jobs/{job_name}"
            if action == SchedulerJobActions.PAUSE:
                await asyncio.to_thread(scheduler_client.pause_job, name=gc_name)
            elif action == SchedulerJobActions.RESUME:
                await asyncio.to_thread(scheduler_client.resume_job, name=gc_name)
            elif action == SchedulerJobActions.DELETE:
                await asyncio.to_thread(scheduler_client.delete_job, name=gc_name)
            elif action == SchedulerJobActions.UPDATE and job_settings is not None:
                job_config = GCloudSchedulerJobs.get_job_config(job_settings)
                job: google.cloud.scheduler_v1beta1.Job = Job(job_config)
                await asyncio.to_thread(scheduler_client.update_job, job=job)
            else:
                raise ValueError(f"Invalid action: {action}")
        except ValueError:
            raise
        except google.api_core.exceptions.NotFound:
            logging.warning(f"Trying to {action} a non existing Schedule: {job_name}")
            raise GCloudScheduleException(
                404, f"Tried to {action} a non existing Schedule, contact support@tinybird.co, job_name: {job_name}"
            )
        except Exception:
            raise GCloudScheduleException(
                500, f"Error trying to {action} Schedule, contact support@tinybird.co, job_name: {job_name}"
            )

    @staticmethod
    async def delete_scheduler(gcscheduler_job_name):
        await GCloudSchedulerJobs.update_job_status(SchedulerJobActions.DELETE, gcscheduler_job_name)

    @staticmethod
    def generate_job_name(workspace_id: str, pipe_id: str, type: str = "copy") -> str:
        return f"gcs_{type}_workspace_{workspace_id}_pipe_{pipe_id}_{hashlib.sha224(pipe_id.encode()).hexdigest()[:6]}"

    @staticmethod
    async def manage_job(action: str, job_settings: dict) -> Job:
        try:
            job_config = GCloudSchedulerJobs.get_job_config(job_settings)
            scheduler_client = GCloudScheduler.get_client()
            job: google.cloud.scheduler_v1beta1.Job = Job(job_config)
            parent = GCloudScheduler.get_parent(scheduler_client)
            scheduler_job = await GCloudSchedulerJobs.create_or_update_job(action, job, parent, scheduler_client)
        except InvalidArgument as grpcError:
            logging.warning(f"{grpcError.details} {grpcError.message}")
            raise GCloudScheduleException(
                400,
                f"'schedule_cron' is invalid. '{job_settings['cron']}' is not a valid crontab expression. Use a valid crontab expression or contact us at support@tinybird.co",
            )
        except AlreadyExists:
            logging.warning(f"Already existing Schedule but no DataSink: {job_settings['gcscheduler_job_name']}")
            raise GCloudScheduleException(
                500,
                f'Pipe already has an unexpected Schedule, contact support@tinybird.co, job_name: {job_settings["gcscheduler_job_name"]}',
            )
        except NotFound:
            logging.warning(f"Schedule not found: {job_settings['gcscheduler_job_name']}")
            raise GCloudScheduleException(
                500, f'Tried to update non-existing Schedule, job_name: {job_settings["gcscheduler_job_name"]}'
            )
        except Exception:
            logging.exception(f"Error trying to  {action}: {job_settings['gcscheduler_job_name']}")
            raise
        GCloudSchedulerJobs.check_job_creation(job_config, scheduler_job)
        return scheduler_job

    @staticmethod
    async def create_or_update_job(action, job, parent, scheduler_client):
        """
        >>> import asyncio
        >>> from unittest.mock import patch, MagicMock
        >>> GCloudScheduler.config('project_id', 'region', 'local')
        >>> mock_scheduler = MagicMock()
        >>> job_settings = {'gcscheduler_target_url': 'https://example.com', 'cron': '0 0 * * ', 'gcscheduler_job_name': 'job_name'}
        >>> job = Job({'name': 'projects/project_id/locations/region/jobs/job_name', 'http_target': {'uri': 'https://example.com', 'http_method': 'POST'}, 'schedule': '0 0 * * ', 'time_zone': 'Etc/UTC'})
        >>> asyncio.run(GCloudSchedulerJobs.create_or_update_job('unknown', job, mock_scheduler, mock_scheduler))
        Traceback (most recent call last):
        ...
        ValueError: Invalid action: unknown
        """
        if action == SchedulerJobActions.CREATE:
            scheduler_job = await asyncio.to_thread(scheduler_client.create_job, parent=parent, job=job)
        elif action == SchedulerJobActions.UPDATE:
            scheduler_job = await asyncio.to_thread(scheduler_client.update_job, job=job)
        else:
            raise ValueError(f"Invalid action: {action}")
        return scheduler_job

    @staticmethod
    def get_job_config(job_settings: dict) -> dict:
        """
        >>> GCloudScheduler.config('project_id', 'region', 'local')
        >>> job_settings = {'gcscheduler_target_url': 'https://example.com', 'cron': '0 0 * * ', 'gcscheduler_job_name': 'job_name'}
        >>> job_config = GCloudSchedulerJobs.get_job_config(job_settings)
        >>> job_config['retry_config'] == DEFAULT_RETRY_CONFIG
        True
        >>> job_config['name'] == 'projects/project_id/locations/region/jobs/job_name'
        True
        >>> job_config['http_target'] == {'http_method': 'POST', 'uri': 'https://example.com'}
        True
        >>> job_config['time_zone'] == 'Etc/UTC'
        True
        >>> job_config['schedule'] == '0 0 * * '
        True
        >>> job_settings = {'gcscheduler_target_url': 'https://example.com', 'cron': '0 0 * * ', 'timezone': 'America/Sao_Paulo', 'gcscheduler_job_name': 'job_name'}
        >>> job_config = GCloudSchedulerJobs.get_job_config(job_settings)
        >>> job_config['retry_config'] == DEFAULT_RETRY_CONFIG
        True
        >>> job_config['name'] == 'projects/project_id/locations/region/jobs/job_name'
        True
        >>> job_config['time_zone'] == 'America/Sao_Paulo'
        True
        >>> job_config['schedule'] == '0 0 * * '
        True
        >>> job_config['http_target'] == {'http_method': 'POST', 'uri': 'https://example.com'}
        True
        >>> job_settings = {'cron': '0 0 * * ',  'gcscheduler_job_name': 'job_name'}
        >>> GCloudSchedulerJobs.get_job_config(job_settings)
        Traceback (most recent call last):
        ...
        ValueError: Missing required Job setting: gcscheduler_target_url
        >>> job_settings = {'gcscheduler_target_url': 'https://example.com', 'gcscheduler_job_name': 'job_name'}
        >>> GCloudSchedulerJobs.get_job_config(job_settings)
        Traceback (most recent call last):
        ...
        ValueError: Missing required Job setting: cron
        >>> job_settings = {'gcscheduler_target_url': 'https://example.com', 'cron': '0 0 * * '}
        >>> GCloudSchedulerJobs.get_job_config(job_settings)
        Traceback (most recent call last):
        ...
        ValueError: Missing required Job setting: gcscheduler_job_name
        """
        timezone = job_settings.get(
            "timezone", DEFAULT_TIMEZONE
        )  # https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
        schedule = job_settings.get("cron")
        uri = job_settings.get("gcscheduler_target_url")
        job_name = job_settings.get("gcscheduler_job_name")

        if not uri or not schedule or not job_name:
            missing_setting = (
                "gcscheduler_target_url" if not uri else "cron" if not schedule else "gcscheduler_job_name"
            )
            raise ValueError(f"Missing required Job setting: {missing_setting}")

        return {
            "name": f"{GCloudScheduler.get_parent_name()}/jobs/{job_name}",
            "http_target": {"http_method": "POST", "uri": uri},
            "schedule": schedule,
            "time_zone": timezone,
            "retry_config": DEFAULT_RETRY_CONFIG,
        }

    @staticmethod
    def check_job_creation(job_config: dict, job: Job):
        """
        >>> job_config = {'name': 'my_job', 'schedule': '*/5 * * * *', 'time_zone': 'US/Pacific'}
        >>> job = Job({'name': 'my_job', 'schedule': '*/10 * * * *', 'time_zone': 'US/Pacific'})
        >>> try:
        ...     GCloudSchedulerJobs.check_job_creation(job_config, job)
        ... except ErrorCreatingScheduleException as e:
        ...     assert str(e) == f'Job creation failed: {job}'
        ...
        >>> job = Job({'name': 'another_job', 'schedule': '*/5 * * * *', 'time_zone': 'US/Pacific'})
        >>> try:
        ...     GCloudSchedulerJobs.check_job_creation(job_config, job)
        ... except ErrorCreatingScheduleException as e:
        ...     assert str(e) == f'Job creation failed: {job}'
        ...
        >>> job = Job({'name': 'my_job', 'schedule': '*/5 * * * *', 'time_zone': 'US/Eastern'})
        >>> try:
        ...     GCloudSchedulerJobs.check_job_creation(job_config, job)
        ... except ErrorCreatingScheduleException as e:
        ...     assert str(e) == f'Job creation failed: {job}'
        """
        try:
            assert job.name == job_config["name"]
            assert job.schedule == job_config["schedule"]
            assert job.time_zone == job_config["time_zone"]
        except AssertionError:
            raise ErrorCreatingScheduleException(f"Job creation failed: {job}")
