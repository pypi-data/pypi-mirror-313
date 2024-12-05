import datetime
import logging

from tinybird.connector_settings import DataConnectors
from tinybird.data_connector import DataSink, ResourceNotConnected
from tinybird.data_sinks.limits import MinPeriodBetweenScheduledSinkJobs
from tinybird.data_sinks.tracker import SinksAPILogRecord, SinksOpsLogResults, sinks_tracker
from tinybird.data_sinks.validation import DataSinkScheduleUpdateRequest
from tinybird.gc_scheduler.constants import DEFAULT_TIMEZONE
from tinybird.gc_scheduler.sinks import create_datasink_schedule_sink, update_datasink_sink
from tinybird.pipe import Pipe
from tinybird.tokens import AccessToken
from tinybird.user import User as Workspace
from tinybird.views.api_errors.pipes import MIN_PERIOD_BETWEEN_SINK_JOBS_EXCEEDED, ForbiddenError

logger = logging.getLogger("DataSinkService")


class DataSinkService:
    """
    This class is responsible for handling the business logic of the DataSink API, offloading the view from the
    responsibility of handling the business logic and making the view more readable and maintainable.
    It also provides some helper methods to interact with the DataSink model, and do semantic validations
    related to the operation of updating a DataSink schedule.

    The current main responsibility of this class is to update the schedule of a DataSink, and log any error that
    occurs during the process. This is done by calling the `update_schedule` method, which receives a
    `DataSinkScheduleUpdateRequest` object, and returns the updated pipe.

    In order to instantiate this class, it requires a `Workspace`, a `Pipe`, and an `AccessToken` object.
    The Pipe must be of type `DataSink`
    """

    def __init__(self, workspace: Workspace, pipe: Pipe, access_token: AccessToken, api_host: str) -> None:
        self.workspace = workspace
        self.pipe = pipe
        self.access_token = access_token
        self.api_host = api_host

    def get_timezone(self, data_sink: DataSink | None) -> str:
        settings = data_sink.settings if data_sink is not None else {}
        return settings.get("timezone", DEFAULT_TIMEZONE)

    def check_schedule_limit(self, schedule_cron: str | None) -> None:
        if schedule_cron is None:
            return
        limit = MinPeriodBetweenScheduledSinkJobs()
        min_period = limit.get_limit_for(self.workspace)
        if limit.has_reached_limit_in(min_period, {"cron_schedule": schedule_cron}):
            error_params = limit.get_error_message_params(self.workspace)
            message = MIN_PERIOD_BETWEEN_SINK_JOBS_EXCEEDED.format(**error_params)
            raise ForbiddenError(message)

    async def _create_schedule_sink(self, data_sink: DataSink, cron: str) -> DataSink:
        timezone = self.get_timezone(data_sink)
        return await create_datasink_schedule_sink(self.workspace, self.pipe, data_sink, self.api_host, cron, timezone)

    async def update_schedule(self, request: DataSinkScheduleUpdateRequest) -> DataSink | None:
        """
        update the pipe schedule, return the schedule data sink if it exists after the update, or none otherwise
        there's a bunch of cases:
        Case    | Original schedule   | Requested schedule  | Result
        1       | None                | None                | None
        2       | None                | Cron                | new data sink
        3       | Cron                | None                | delete schedule data sink, return None
        4       | Cron                | Different cron      | update schedule data sink, return updated data sink
        5       | Cron                | Same cron           | return original schedule data sink

        """
        try:
            data_sink = DataSink.get_by_resource_id(self.pipe.id, self.workspace.id)
            self.check_schedule_limit(request.schedule_cron)
            schedule_data_sink = self.get_scheduled_data_sink(data_sink)

            # cases 1 and 2
            if schedule_data_sink is None:
                if request.schedule_cron is not None:
                    schedule_data_sink = await self._create_schedule_sink(data_sink, request.schedule_cron)

                return schedule_data_sink

            # case 3
            current_cron = schedule_data_sink.settings.get("cron")
            if request.schedule_cron is None:
                await schedule_data_sink.delete()
                return None

            # cases 4 and 5
            if current_cron != request.schedule_cron:
                timezone = self.get_timezone(data_sink)
                schedule_data_sink = await update_datasink_sink(schedule_data_sink, request.schedule_cron, timezone)
            return schedule_data_sink
        except Exception as e:
            self.log_sink_error(data_sink, str(e))
            raise

    def get_scheduled_data_sink(self, data_sink: DataSink) -> DataSink | None:
        if data_sink.service == DataConnectors.GCLOUD_SCHEDULER:
            return data_sink
        try:
            return DataSink.get_by_resource_id(data_sink.id, self.workspace.id)
        except ResourceNotConnected:
            return None

    def log_sink_error(self, data_sink: DataSink, error: str) -> None:
        try:
            if sinks_tracker.is_enabled():
                timestamp = datetime.datetime.now(datetime.UTC)
                resource_tags = self.workspace.get_tag_names_by_resource(self.pipe.id, self.pipe.name)
                record = SinksAPILogRecord(
                    workspace_id=self.workspace.id,
                    workspace_name=self.workspace.name,
                    timestamp=timestamp,
                    service=data_sink.service or "",
                    pipe_id=self.pipe.id,
                    pipe_name=self.pipe.name,
                    result=SinksOpsLogResults.ERROR,
                    token_name=self.access_token.name,
                    error=error,
                    resource_tags=resource_tags,
                )
                sinks_tracker.append_api_log(record)
        except Exception as e:
            logger.exception(f"sinks_tracker - Could not log sink error: {e}")
