import asyncio
import functools
import json
import logging
from datetime import UTC, datetime
from typing import Dict, cast

from tornado.escape import json_decode
from tornado.web import url

from tinybird.connector_settings import DataConnectorType, DynamoDBConnectorSetting
from tinybird.data_connector import DataConnector, DataConnectors, DataLinker, DataSourceNotConnected
from tinybird.data_connectors.local_connectors import build_session_from_credentials
from tinybird.datasource import Datasource
from tinybird.ingest.cdk_utils import CDKUtils
from tinybird.ingest.preview_connectors.base_connector import BasePreviewConnector as PreviewConnector
from tinybird.ingest.scheduling import DEFAULT_RUNS_TO_FETCH, SchedulerRequestFailed, ScheduleState, get_schedule
from tinybird.integrations.dynamodb.sync_job import DynamoDBSyncJob, create_ddb_sync_job
from tinybird.job import JobKind, JobStatus
from tinybird.model import retry_transaction_in_case_of_concurrent_edition_error_sync
from tinybird.providers.aws.dynamodb import (
    DynamoDBExportConfiguration,
    DynamoDBExportDescription,
    export_table_to_point_in_time,
)
from tinybird.providers.aws.exceptions import AWSClientException, PITRExportNotAvailable
from tinybird.providers.aws.session import AWSSession
from tinybird.tokens import scopes
from tinybird.views.api_errors import RequestError
from tinybird.views.api_errors.datasources import (
    ClientErrorBadRequest,
    ClientErrorNotFound,
    ClientNotAllowed,
    DynamoDBDatasourceError,
)
from tinybird.views.base import ApiHTTPError, BaseHandler, authenticated, with_scope


def to_api_error(err: RequestError) -> ApiHTTPError:
    return ApiHTTPError.from_request_error(err)


def _assert_is_scheduled(ds: Datasource) -> None:
    # Using the exitence of a service associated to a DS as a proxy to
    # indicate if it's scheduleable. We might want to improve this at a later
    # stage when we know more about the connectors
    if not ds.service:
        raise to_api_error(ClientNotAllowed.datasource_not_scheduleable(ds=ds.id))


def handle_scheduler_errors(func):
    @functools.wraps(func)
    async def inner(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except SchedulerRequestFailed as err:
            raise ApiHTTPError(503, str(err) or "Service Unavailable") from err

    return inner


class DatasourceScheduleHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @authenticated
    async def prepare(self) -> None:
        super().prepare()
        self._workspace = self.current_workspace
        self._datasource = self._get_datasource(self.path_args[0])

        if self._datasource.service != DataConnectorType.AMAZON_DYNAMODB:
            _assert_is_scheduled(self._datasource)
            self._schedule = await get_schedule(
                CDKUtils.cdk_webserver_url,
                self._workspace.id,
                self._datasource.id,
                CDKUtils.get_credentials_provider_async(),
            )

    def on_finish(self):
        super().on_finish()  # In case we do anything in the superclass
        if hasattr(self, "_schedule") and self._schedule:
            self._schedule.shutdown()

    def _get_datasource(self, datasource_id: str) -> Datasource:
        if ds := self._workspace.get_datasource(datasource_id):
            return ds
        raise to_api_error(ClientErrorNotFound.nonexisting_data_source(name=datasource_id))

    @property
    def _json_body_args(self) -> Dict:
        try:
            return json_decode(self.request.body)
        except json.decoder.JSONDecodeError as err:
            raise to_api_error(ClientErrorBadRequest.invalid_json_body()) from err


class APIDatasourceScheduleStateHandler(DatasourceScheduleHandler):
    @authenticated
    @with_scope(scopes.ADMIN)
    @handle_scheduler_errors
    async def get(self, _: str):
        if self._datasource.service in [
            DataConnectors.AMAZON_S3,
            DataConnectors.AMAZON_S3_IAMROLE,
            DataConnectors.GCLOUD_STORAGE,
        ]:
            connector = PreviewConnector()
            state = await connector.get_current_state(self._workspace.id, self._datasource.id) or ScheduleState.RUNNING
            self.write_json({"state": state})
        else:
            state = await self._schedule.get_state()
            self.write_json({"state": state.value})

    @authenticated
    @with_scope(scopes.ADMIN)
    @handle_scheduler_errors
    async def put(self, _: str):
        try:
            state = self._json_body_args["state"]
            await self._set_scheduler_state(state)
        except KeyError as err:
            raise to_api_error(ClientErrorBadRequest.missing_body_param(param="state")) from err

    async def _set_scheduler_state(self, state: str) -> None:
        if state == ScheduleState.RUNNING:
            if self._datasource.service in [
                DataConnectors.AMAZON_S3,
                DataConnectors.AMAZON_S3_IAMROLE,
                DataConnectors.GCLOUD_STORAGE,
            ]:
                connector = PreviewConnector()
                await connector.unpause_executions(self._workspace.id, self._datasource.id)
            else:
                await self._schedule.unpause()
        elif state == ScheduleState.PAUSED:
            if self._datasource.service in [
                DataConnectors.AMAZON_S3,
                DataConnectors.AMAZON_S3_IAMROLE,
                DataConnectors.GCLOUD_STORAGE,
            ]:
                connector = PreviewConnector()
                await connector.pause_executions(self._workspace.id, self._datasource.id)
            else:
                runs = await self._schedule.list_runs()
                last_run = runs[-1] if len(runs) else None
                if last_run and last_run["state"] == "running":
                    raise to_api_error(
                        ClientErrorBadRequest.cannot_pause_with_ongoing_run(datasource_name=self._datasource.name)
                    )
                await self._schedule.pause()
        else:
            raise to_api_error(ClientErrorBadRequest.invalid_scheduler_state(state=state))


class APIDatasourceSchedulerRunsHandler(DatasourceScheduleHandler):
    @authenticated
    @with_scope(scopes.ADMIN)
    @handle_scheduler_errors
    async def get(self, datasource_id: str):
        if self._datasource.service in [
            DataConnectors.AMAZON_S3,
            DataConnectors.AMAZON_S3_IAMROLE,
            DataConnectors.GCLOUD_STORAGE,
        ]:
            connector = PreviewConnector()
            runs = await connector.retrieve_executions(self._workspace.id, datasource_id)

            res = {"datasource_id": datasource_id, "datasource_name": self._datasource.name, "runs": runs}
            self.write_json(res)
        else:
            limit = self.get_query_argument("limit", default=DEFAULT_RUNS_TO_FETCH)
            runs = await self._schedule.list_runs(limit=limit)
            state = await self._schedule.get_state()
            if state == ScheduleState.PAUSED:
                runs = [run for run in runs if run["state"] != "running"]
                logging.warning(
                    f"Filtered out running runs for paused datasource datasource_id={self._datasource.id} in workspace_id={self._workspace.id}"
                )
            res = {"datasource_id": datasource_id, "datasource_name": self._datasource.name, "runs": runs}
            self.write_json(res)

    @authenticated
    @with_scope(scopes.ADMIN)
    @handle_scheduler_errors
    async def post(self, datasource_id: str):
        if self._datasource.service in [
            DataConnectors.AMAZON_S3,
            DataConnectors.AMAZON_S3_IAMROLE,
            DataConnectors.GCLOUD_STORAGE,
        ]:
            connector = PreviewConnector()
            _ = await connector.execute_now(self._workspace.id, datasource_id)

            res = {
                "datasource_id": datasource_id,
                "datasource_name": self._datasource.name,
                "run_id": f"manual__{datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')}",
                "state": "queued",
            }
            self.write_json(res)
        elif self._datasource.service == DataConnectors.AMAZON_DYNAMODB:
            result = await self.trigger_dynamodb_sync(datasource_id)
            self.write_json(result)
        else:
            run_details = await self._schedule.trigger()
            res = {
                "datasource_id": datasource_id,
                "datasource_name": self._datasource.name,
                **run_details,
            }
            self.write_json(res)

    async def trigger_dynamodb_sync(self, datasource_id: str):
        if any_dynamodbjob_in_progress(self._workspace.id, self._datasource.id):
            raise ApiHTTPError.from_request_error(
                DynamoDBDatasourceError.dynamodb_sync_already_in_progress(datasource_name=self._datasource.name)
            )

        # Get all needed models and settings
        try:
            data_linker = DataLinker.get_by_datasource_id(self._datasource.id)
        except DataSourceNotConnected:
            raise ApiHTTPError.from_request_error(
                ClientErrorBadRequest.missing_connector(service_name=DataConnectors.AMAZON_DYNAMODB)
            )

        if not data_linker.data_connector_id:
            raise ApiHTTPError.from_request_error(
                ClientErrorBadRequest.missing_connector(service_name=DataConnectors.AMAZON_DYNAMODB)
            )

        table_name = data_linker.settings.get("dynamodb_table_arn")
        data_connector = DataConnector.get_by_id(data_linker.data_connector_id)
        settings = cast(DynamoDBConnectorSetting, data_connector.validated_settings)
        session = cast(AWSSession, build_session_from_credentials(credentials=settings.credentials))

        # Trigger table export in AWS
        dynamodb_export_time = datetime.now(UTC)

        def export_dynamodb_table_to_s3() -> DynamoDBExportDescription:
            export_configuration = DynamoDBExportConfiguration(
                table_arn=table_name,
                export_time=dynamodb_export_time,
                bucket=data_linker.settings.get("dynamodb_export_bucket"),
            )
            return export_table_to_point_in_time(session, export_configuration, settings.dynamodb_iamrole_region)

        try:
            dynamodb_export_description = await asyncio.get_running_loop().run_in_executor(
                None, export_dynamodb_table_to_s3
            )
        except PITRExportNotAvailable:
            raise ApiHTTPError.from_request_error(DynamoDBDatasourceError.pitr_not_available(table_name=table_name))
        except AWSClientException as err:
            raise ApiHTTPError.from_request_error(
                DynamoDBDatasourceError.error_while_triggering_dynamodb_export(error_message=str(err))
            )

        # Update Linker and Trigger DynamoDB Sync Job
        update_table_export_in_data_linker(data_linker, dynamodb_export_description, dynamodb_export_time)

        sync_job = create_ddb_sync_job(
            self.application.job_executor,
            workspace=self._workspace,
            datasource=self._datasource,
            data_linker=data_linker,
            request_id=self._request_id,
        )

        return {
            "datasource_id": datasource_id,
            "datasource_name": self._datasource.name,
            "run_id": sync_job.id,
            "state": "queued",
        }


@retry_transaction_in_case_of_concurrent_edition_error_sync()
def update_table_export_in_data_linker(
    data_linker: DataLinker, export: DynamoDBExportDescription, export_time: datetime
) -> DataLinker:
    with DataLinker.transaction(data_linker.id) as linker:
        linker.update_settings(
            {"dynamodb_export_time": export_time.isoformat(), "initial_export_arn": export.export_arn}
        )
        return linker


def any_dynamodbjob_in_progress(workspace_id: str, datasource_id: str) -> bool:
    all_jobs = DynamoDBSyncJob.get_all_by_owner(workspace_id)
    return any(
        job.kind == JobKind.DYNAMODB_SYNC
        and job.datasource_id == datasource_id
        and job.status in {JobStatus.WAITING, JobStatus.WORKING}
        for job in all_jobs
    )


def handlers():
    return [
        url(
            r"/v0/datasources/([^/]+)/scheduling/state",
            APIDatasourceScheduleStateHandler,
        ),
        url(
            r"/v0/datasources/([^/]+)/scheduling/runs",
            APIDatasourceSchedulerRunsHandler,
        ),
    ]
