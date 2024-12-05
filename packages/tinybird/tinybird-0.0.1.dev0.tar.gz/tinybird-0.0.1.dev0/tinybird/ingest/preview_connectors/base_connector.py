from typing import Any, List, Optional, Tuple

from tinybird.data_connector import DataConnectors
from tinybird.data_connectors.credentials import ConnectorCredentials
from tinybird.ingest.data_connectors import Connector, ConnectorException, ConnectorParameters
from tinybird.ingest.preview_connectors.yepcode_utils import (
    YepCodeDatasourceNotFound,
    YepCodeRemoveDatasourceError,
    cancel_datasource_jobs,
    create_connector,
    get_bucket_list,
    get_datasource_details,
    get_executions,
    get_preview,
    pause_executions,
    remove_datasource,
    resume_executions,
    trigger_execution,
)
from tinybird.ingest.scheduling import ScheduleState
from tinybird.job import JobExecutor

JOB_CREATED = "CREATED"
JOB_RUNNING = "RUNNING"
JOB_FINISHED = "FINISHED"
JOB_ERROR = "ERROR"
JOB_KILLED = "KILLED"
JOB_REJECTED = "REJECTED"

job_status_map = {
    JOB_CREATED: "running",
    JOB_RUNNING: "running",
    JOB_FINISHED: "done",
}


class BasePreviewConnector(Connector):
    def __init__(self):
        self.connector: Optional[DataConnectors] = None

    def make_credentials(self, credentials: ConnectorCredentials) -> dict[str, Any]:
        return {}

    def make_parameters(self, parameters: ConnectorParameters) -> dict[str, Any]:
        return {}

    async def bucket_list(
        self,
        credentials: ConnectorCredentials,
        working_zone: Optional[str] = None,
    ) -> List[str]:
        api_credentials = self.make_credentials(credentials)
        assert self.connector is not None

        buckets = await get_bucket_list(
            connector=self.connector,
            credentials=api_credentials,
            zone_id=working_zone,
        )

        if buckets.get("error"):
            raise ConnectorException(message=buckets["error"])

        return [b.get("name") for b in buckets.get("buckets", [])]

    async def preview_summary(
        self,
        credentials: ConnectorCredentials,
        tb_token: str,
        tb_endpoint: str,
        parameters: ConnectorParameters,
        workspace_id: str,
        working_zone: Optional[str] = None,
    ) -> dict[str, Any]:
        api_credentials = self.make_credentials(credentials)
        api_params = self.make_parameters(parameters)
        assert self.connector is not None

        preview = await get_preview(
            connector=self.connector,
            credentials=api_credentials,
            tb_token=tb_token,
            tb_endpoint=tb_endpoint,
            params=api_params,
            zone_id=working_zone,
            workspace_id=workspace_id,
        )

        if preview.get("error"):
            raise ConnectorException(message=preview["error"])

        preview_chunk: dict[str, Any] = {"files": []}

        for file in preview.get("sampleFiles", []):
            preview_chunk["files"].append({"name": file.get("name"), "size": file.get("size")})

        preview_chunk["total_size"] = preview.get("totalSize", 0)
        preview_chunk["num_files"] = preview.get("numFiles", 0)

        return preview_chunk

    async def preview(
        self,
        credentials: ConnectorCredentials,
        tb_token: str,
        tb_endpoint: str,
        parameters: ConnectorParameters,
        workspace_id: str,
        working_zone: Optional[str] = None,
    ) -> Tuple[bytes, Optional[dict[str, Any]]]:
        api_credentials = self.make_credentials(credentials)
        api_params = self.make_parameters(parameters)
        assert self.connector is not None

        preview = await get_preview(
            connector=self.connector,
            credentials=api_credentials,
            tb_token=tb_token,
            tb_endpoint=tb_endpoint,
            params=api_params,
            zone_id=working_zone,
            workspace_id=workspace_id,
        )

        if preview.get("error"):
            raise ConnectorException(message=preview["error"])

        preview_chunk = "\n".join(preview.get("sampleLines", [])) if preview.get("sampleLines") else ""

        return preview_chunk.encode("utf-8"), preview.get("dataGuessing")

    async def link_connector(
        self,
        tb_token: str,
        workspace_id: str,
        datasource_id: str,
        credentials: ConnectorCredentials,
        parameters: ConnectorParameters,
        cron: Optional[str] = None,
        working_zone: Optional[str] = None,
        tb_endpoint: Optional[str] = None,
    ) -> dict[Any, Any]:
        api_credentials = self.make_credentials(credentials)
        api_params = self.make_parameters(parameters)
        assert self.connector is not None

        result = await create_connector(
            connector=self.connector,
            tb_token=tb_token,
            workspace_id=workspace_id,
            datasource_id=datasource_id,
            credentials=api_credentials,
            params=api_params,
            cron=cron,
            zone_id=working_zone,
            tb_endpoint=tb_endpoint,
        )

        if isinstance(result, dict):
            if result.get("error"):
                raise ConnectorException(message=result["error"])

            if result.get("message") and result.get("message") == "Datasource created successfully":
                return {"message": "Datasource is being created"}
        else:
            if not result:
                return {"message": "Datasource is being created"}

            if "created successfully" in result:
                return {"message": "Datasource is being created"}
            else:
                raise ConnectorException(message=result)

        return result

    async def execute_now(
        self,
        workspace_id: str,
        datasource_id: str,
    ) -> dict[Any, Any]:
        result = await trigger_execution(
            workspace_id=workspace_id,
            datasource_id=datasource_id,
        )

        if isinstance(result, dict) and result.get("error"):
            raise ConnectorException(message=result["error"])

        return result

    async def retrieve_executions(
        self,
        workspace_id: str,
        datasource_id: str,
    ) -> List[dict[Any, Any]]:
        executions = await get_executions(
            workspace_id=workspace_id,
            datasource_id=datasource_id,
        )

        if isinstance(executions, dict) and executions.get("error"):
            raise ConnectorException(message=executions["error"])

        result_executions = []
        for execution in executions:
            status = execution.get("status")

            if status in (JOB_CREATED, JOB_RUNNING, JOB_FINISHED):
                result_executions.append(
                    {
                        "id": execution.get("executionId"),
                        "execution_date": execution.get("startTimeUtc", execution.get("startTime")),
                        "start_date": execution.get("startTimeUtc", execution.get("startTime")),
                        "end_date": execution.get("endTimeUtc", execution.get("endTime")),
                        "state": job_status_map.get(status),
                    }
                )

        return result_executions

    async def pause_executions(
        self,
        workspace_id: str,
        datasource_id: str,
    ) -> dict[Any, Any]:
        result = await pause_executions(
            workspace_id=workspace_id,
            datasource_id=datasource_id,
        )

        if isinstance(result, dict) and result.get("error"):
            raise ConnectorException(message=result["error"])

        return result

    async def unpause_executions(
        self,
        workspace_id: str,
        datasource_id: str,
    ) -> dict[Any, Any]:
        result = await resume_executions(
            workspace_id=workspace_id,
            datasource_id=datasource_id,
        )

        if isinstance(result, dict) and result.get("error"):
            raise ConnectorException(message=result["error"])

        return result

    async def get_current_state(self, workspace_id: str, datasource_id: str) -> Optional[ScheduleState]:
        result = await get_datasource_details(workspace_id, datasource_id)
        if result.get("error") or result.get("ingesting") is None:
            return None

        return ScheduleState.RUNNING if result.get("ingesting") else ScheduleState.PAUSED

    async def remove_linker(
        self,
        workspace_id: str,
        datasource_id: str,
        job_executor: Optional[JobExecutor] = None,
    ):
        try:
            await remove_datasource(
                workspace_id=workspace_id,
                datasource_id=datasource_id,
            )
            await cancel_datasource_jobs(datasource_id=datasource_id, job_executor=job_executor)
        except YepCodeDatasourceNotFound:
            pass
        except YepCodeRemoveDatasourceError as e:
            raise ConnectorException(str(e))


class PreviewConnectorMock(BasePreviewConnector):
    async def bucket_list(
        self,
        credentials: ConnectorCredentials,
        working_zone: Optional[str] = None,
    ) -> List[str]:
        return ["myfirstbucket", "mysecondbucket"]

    async def preview_summary(
        self,
        credentials: ConnectorCredentials,
        tb_token: str,
        tb_endpoint: str,
        parameters: ConnectorParameters,
        workspace_id: str,
        working_zone: Optional[str] = None,
    ) -> dict[str, Any]:
        return {
            "sampleFiles": [
                {"name": "myfile1.csv", "size": 653},
                {"name": "myfile2.csv", "size": 695},
            ],
            "total_size": 13480,
            "num_files": 20,
        }

    async def preview(
        self,
        credentials: ConnectorCredentials,
        tb_token: str,
        tb_endpoint: str,
        parameters: ConnectorParameters,
        workspace_id: str,
        working_zone: Optional[str] = None,
    ) -> Tuple[bytes, Optional[dict[str, Any]]]:
        return b"Some cool string;40\nSome other cool string;41", None

    async def link_connector(
        self,
        tb_token: str,
        workspace_id: str,
        datasource_id: str,
        credentials: ConnectorCredentials,
        parameters: ConnectorParameters,
        cron: Optional[str] = None,
        working_zone: Optional[str] = None,
        tb_endpoint: Optional[str] = None,
    ) -> dict[Any, Any]:
        return {"message": "Datasource is being created"}

    async def execute_now(
        self,
        workspace_id: str,
        datasource_id: str,
    ) -> dict[Any, Any]:
        return {}

    async def retrieve_executions(
        self,
        workspace_id: str,
        datasource_id: str,
    ) -> List[dict[Any, Any]]:
        return [
            {
                "id": "b2289ca0-b1da-4761-8641-27e65fe8a2f8",
                "execution_date": "2023-06-27T12:52:45.241+00:00",
                "start_date": "2023-06-27T12:52:45.241+00:00",
                "end_date": "2023-06-27T12:52:47.635+00:00",
                "state": "FINISHED",
            },
            {
                "id": "c4e318f0-6d37-42e3-b0e7-98cec21b1d9f",
                "execution_date": "2023-06-19T14:17:44.992+00:00",
                "start_date": "2023-06-27T12:52:45.241+00:00",
                "end_date": "2023-06-19T14:17:47.411+00:00",
                "state": "FINISHED",
            },
        ]

    async def remove_linker(
        self,
        workspace_id: str,
        datasource_id: str,
        job_executor: Optional[JobExecutor] = None,
    ) -> dict[Any, Any]:
        return {}
