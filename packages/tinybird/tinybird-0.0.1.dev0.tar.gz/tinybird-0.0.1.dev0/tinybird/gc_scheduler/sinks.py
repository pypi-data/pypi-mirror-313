import logging
from typing import Optional
from urllib.parse import urljoin

import pytz

from tinybird.data_connector import DataConnector, DataConnectors, DataSink, ResourceNotConnected
from tinybird.gc_scheduler.constants import (
    DEFAULT_TIMEZONE,
    ExistingSinkException,
    SchedulerJobActions,
    SchedulerJobStatus,
)
from tinybird.gc_scheduler.scheduler_jobs import GCloudScheduler, GCloudSchedulerJobs
from tinybird.model import retry_transaction_in_case_of_concurrent_edition_error_async
from tinybird.pipe import Pipe
from tinybird.token_scope import scopes
from tinybird.user import User, Users


def get_or_create_gc_scheduler_data_connector(workspace: "User") -> DataConnector:
    """
    >>> from unittest.mock import MagicMock, patch
    >>> workspace_mock = MagicMock()
    >>> workspace_mock.id = 1
    >>> workspace_mock.is_release = False
    >>> workspace_mock.is_branch = False
    >>> workspace_mock.is_branch_or_release_from_branch = False
    >>> workspace_mock.origin = None
    >>> workspace_mock.get_main_workspace = MagicMock()
    >>> workspace_mock.get_main_workspace.return_value = workspace_mock
    >>> GCloudScheduler.config('project_id', 'region', 'local')

    >>> with patch.object(DataConnector, 'get_user_gcscheduler_connectors', return_value=None):
    ...     with  patch.object(DataConnector, 'add_connector', return_value=MagicMock()) as add_mock:
    ...         result = get_or_create_gc_scheduler_data_connector(workspace_mock)
    ...         assert isinstance(result, MagicMock)
    ...         add_mock.assert_called_once_with(workspace=workspace_mock, name=f'gc_scheduler_{workspace_mock.id}',
    ...                                          service=DataConnectors.GCLOUD_SCHEDULER,
    ...                                          settings={'gcscheduler_region': GCloudScheduler.region})

    >>> mock_data_connector = MagicMock()
    >>> with patch.object(DataConnector, 'get_user_gcscheduler_connectors', return_value=mock_data_connector):
    ...     with  patch.object(DataConnector, 'add_connector', return_value=MagicMock()) as add_mock:
    ...         result = get_or_create_gc_scheduler_data_connector(workspace_mock)
    ...         assert isinstance(result, MagicMock)
    ...         add_mock.assert_not_called()
    """
    main_workspace_id = workspace.get_main_workspace().id
    data_connector = DataConnector.get_user_gcscheduler_connectors(main_workspace_id)

    if not data_connector:
        main_workspace = workspace
        try:
            main_workspace = workspace.get_main_workspace()
        except Exception:
            logging.exception(f"Workspace origin for workspace {workspace.name} ({workspace.id}) does not exist")

        settings = {"gcscheduler_region": GCloudScheduler.region}
        data_connector = DataConnector.add_connector(
            workspace=main_workspace,
            name=f"gc_scheduler_{main_workspace.id}",
            service=DataConnectors.GCLOUD_SCHEDULER,
            settings=settings,
        )
    return data_connector


async def create_copy_schedule_sink(
    workspace: "User",
    pipe: "Pipe",
    api_host: str,
    cron: Optional[str] = "",
    timezone: Optional[str] = None,
    mode: Optional[str] = None,
) -> DataSink:
    data_sink = None

    try:
        data_sink = DataSink.get_by_resource_id(pipe.id, workspace.id)
        status = data_sink.settings.get("status") if data_sink else None
        if data_sink and status != SchedulerJobStatus.SHUTDOWN:
            raise ExistingSinkException(f"Pipe {pipe.name} already has an existing Schedule")
    except ResourceNotConnected:
        pass

    data_connector = get_or_create_gc_scheduler_data_connector(workspace)
    gcscheduler_job_name = GCloudSchedulerJobs.generate_job_name(workspace.id, pipe.id)
    gcscheduler_target_url = build_target_url(workspace, pipe, api_host, "copy", mode)

    settings = {
        "timezone": timezone or DEFAULT_TIMEZONE,
        "status": SchedulerJobStatus.SHUTDOWN,
        "gcscheduler_target_url": gcscheduler_target_url,
        "gcscheduler_job_name": gcscheduler_job_name,
    }

    if cron and cron != "@on-demand":
        settings["cron"] = cron
        settings["status"] = SchedulerJobStatus.RUNNING
        await GCloudSchedulerJobs.manage_job(SchedulerJobActions.CREATE, settings)

    if not data_sink:
        data_sink = DataSink.add_sink(
            data_connector=data_connector, resource=pipe, settings=settings, workspace=workspace
        )
        return data_sink

    return data_sink


async def create_datasink_schedule_sink(
    workspace: User,
    pipe: Pipe,
    data_sink: DataSink,
    api_host: str,
    cron: str,
    timezone: Optional[str] = None,
) -> DataSink:
    scheduled_data_sink = None

    try:
        scheduled_data_sink = DataSink.get_by_resource_id(data_sink.id, workspace.id)
        status = scheduled_data_sink.settings.get("status") if scheduled_data_sink else None
        if scheduled_data_sink and status != SchedulerJobStatus.SHUTDOWN:
            raise ExistingSinkException(f"Pipe {pipe.name} already has an existing Schedule")
    except ResourceNotConnected:
        pass

    data_connector = get_or_create_gc_scheduler_data_connector(workspace)
    gcscheduler_job_name = GCloudSchedulerJobs.generate_job_name(workspace.id, pipe.id, "sink")
    gcscheduler_target_url = build_target_url(workspace, pipe, api_host, "sink")

    timezone = timezone or DEFAULT_TIMEZONE
    settings = {
        "timezone": timezone,
        "status": SchedulerJobStatus.SHUTDOWN,
        "gcscheduler_target_url": gcscheduler_target_url,
        "gcscheduler_job_name": gcscheduler_job_name,
    }

    if cron and cron != "@on-demand":
        settings["cron"] = cron
        settings["status"] = SchedulerJobStatus.RUNNING
        await GCloudSchedulerJobs.manage_job(SchedulerJobActions.CREATE, settings)
        await transaction_update_sink_schedule(data_sink.id, cron, timezone)

    if not scheduled_data_sink:
        scheduled_data_sink = DataSink.add_sink(
            data_connector=data_connector, resource=data_sink, settings=settings, workspace=workspace
        )
        return scheduled_data_sink
    return scheduled_data_sink


@retry_transaction_in_case_of_concurrent_edition_error_async()
async def transaction_update_sink_schedule(sink_id: str, cron: str, timezone: str) -> DataSink:
    with DataSink.transaction(sink_id) as data_sink:
        data_sink.update_settings(cron=cron, timezone=timezone)
        return data_sink


async def remove_schedule_data_sink(pipe, workspace_id: str, delete_sink: bool = True):
    try:
        data_sink = DataSink.get_by_resource_id(pipe.id, workspace_id)
        await data_sink.delete(delete_sink)
    except ResourceNotConnected:
        pass


@retry_transaction_in_case_of_concurrent_edition_error_async()
async def update_copy_sink(
    workspace: "User", pipe: "Pipe", api_host: str, data_sink: "DataSink", cron: str, timezone: str
):
    settings = data_sink.settings

    if settings.get("cron") == cron and settings.get("timezone") == timezone:
        return data_sink

    if settings["status"] == SchedulerJobStatus.SHUTDOWN:
        data_sink = await create_copy_schedule_sink(
            workspace=workspace, pipe=pipe, api_host=api_host, cron=cron, timezone=timezone
        )
        settings["status"] = SchedulerJobStatus.RUNNING

    if cron:
        settings["cron"] = cron
    if timezone:
        settings["timezone"] = timezone

    await GCloudSchedulerJobs.manage_job(SchedulerJobActions.UPDATE, settings)

    with DataSink.transaction(data_sink.id) as data_sink:
        data_sink.update_settings(cron=cron, timezone=timezone, status=settings.get("status"))
        return data_sink


async def update_datasink_sink(data_sink: "DataSink", cron: str, timezone: str) -> DataSink:
    if data_sink.settings.get("cron") == cron and data_sink.settings.get("timezone") == timezone:
        return data_sink
    data_sink.settings["cron"] = cron
    data_sink.settings["timezone"] = timezone

    await GCloudSchedulerJobs.manage_job(SchedulerJobActions.UPDATE, data_sink.settings)
    return await transaction_update_sink_schedule(data_sink.id, cron, timezone)


@retry_transaction_in_case_of_concurrent_edition_error_async()
async def pause_sink(data_sink: "DataSink"):
    if data_sink.settings.get("status") == SchedulerJobStatus.SHUTDOWN:
        # TODO fixme
        return data_sink

    await GCloudSchedulerJobs.update_job_status(SchedulerJobActions.PAUSE, data_sink.settings["gcscheduler_job_name"])
    with DataSink.transaction(data_sink.id) as data_sink:
        data_sink.update_status(status=SchedulerJobStatus.PAUSED)
        return data_sink


@retry_transaction_in_case_of_concurrent_edition_error_async()
async def resume_sink(data_sink: "DataSink"):
    if data_sink.settings.get("status") == SchedulerJobStatus.SHUTDOWN:
        # TODO fixme
        return data_sink

    await GCloudSchedulerJobs.update_job_status(SchedulerJobActions.RESUME, data_sink.settings["gcscheduler_job_name"])
    with DataSink.transaction(data_sink.id) as data_sink:
        data_sink.update_status(status=SchedulerJobStatus.RUNNING)
        return data_sink


def build_target_url(workspace: "User", pipe: "Pipe", api_host: str, type: str, mode: Optional[str] = None) -> str:
    """
    >>> import re
    >>> from unittest.mock import MagicMock
    >>> from tinybird.user import UserAccount

    >>> u = UserAccount.register('test_build_target_url@example.com', 'pass')
    >>> workspace = User.register('test_build_target_url', admin=u.id)
    >>> copy_pipe = Pipe(guid=1, name='my_copy_pipe', nodes={})
    >>> sink_pipe = Pipe(guid=1, name='my_sink_pipe', nodes={})
    >>> api_host = 'https://api.example.com'
    >>> regex = r'https:\/\/api\.example\.com\/v0\/pipes\/\d+\/(copy|sink)\?token=[^&]+'

    >>> target_url = build_target_url(workspace, copy_pipe, api_host, 'copy', None)
    >>> match = re.match(regex, target_url)
    >>> assert match is not None

    >>> # If we execute again, the token will already exist
    >>> target_url = build_target_url(workspace, copy_pipe, api_host, 'copy', 'append')
    >>> match = re.match(regex, target_url)
    >>> assert match is not None

    >>> target_url = build_target_url(workspace, sink_pipe, api_host, 'sink', 'replace')
    >>> match = re.match(regex, target_url)
    >>> assert match is not None

    >>> # If we execute again, the token will already exist
    >>> target_url = build_target_url(workspace, sink_pipe, api_host, 'sink')
    >>> match = re.match(regex, target_url)
    >>> assert match is not None
    """
    token_name = f"scheduled_{type}_{pipe.id}"
    token = Users.get_token(workspace, token_name)
    if not token:
        schedule_token = Users.add_token(workspace, token_name, scopes.PIPES_READ, pipe.id)
    else:
        schedule_token = token.token

    _mode = f"&_mode={mode}" if mode else ""
    return urljoin(api_host, f"/v0/pipes/{pipe.id}/{type}?token={schedule_token}&_execution_type=scheduled{_mode}")


def valid_tz_database_format(tz_string):
    """
    >>> valid_tz_database_format('US/Pacific')
    True
    >>> valid_tz_database_format('US/Pacific-New')
    False
    >>> valid_tz_database_format(None)
    False
    """
    try:
        pytz.timezone(tz_string)
        return True
    except pytz.UnknownTimeZoneError:
        return False


def should_change_status(action: str, data_sink: "DataSink") -> bool:
    current_status = data_sink.settings.get("status")
    already_paused = action == SchedulerJobActions.PAUSE and current_status == SchedulerJobStatus.PAUSED
    already_running = action == SchedulerJobActions.RESUME and current_status == SchedulerJobStatus.RUNNING
    return not (already_paused or already_running)
