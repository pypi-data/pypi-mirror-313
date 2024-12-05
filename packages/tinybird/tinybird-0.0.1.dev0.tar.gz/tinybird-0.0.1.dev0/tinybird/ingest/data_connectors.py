import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, List, Optional, Tuple

from tornado.httpclient import AsyncHTTPClient, HTTPRequest

from tinybird.data_connectors.credentials import ConnectorCredentials
from tinybird.job import JobExecutor

ANALYZE_ENDPOINT = "/v0/analyze"


class ConnectorParameters:
    pass


@dataclass
class GCSSAConnectorCredentials(ConnectorCredentials):
    private_key_id: str
    client_x509_cert_url: str
    project_id: str
    client_id: str
    client_email: str
    private_key: str


@dataclass
class S3ConnectorParameters(ConnectorParameters):
    bucket_uri: str
    from_time: str
    file_format: str


@dataclass
class S3IAMConnectorParameters(ConnectorParameters):
    bucket_uri: str
    from_time: str
    file_format: str
    sample_file_uri: Optional[str] = None


@dataclass
class GCSSAConnectorParameters(ConnectorParameters):
    bucket_uri: str
    from_time: str
    file_format: str


class Connector(ABC):
    @abstractmethod
    def make_credentials(self, credentials: ConnectorCredentials) -> dict[str, Any]:
        pass

    @abstractmethod
    def make_parameters(self, parameters: ConnectorParameters) -> dict[str, Any]:
        pass

    @abstractmethod
    async def bucket_list(
        self,
        credentials: ConnectorCredentials,
        working_zone: Optional[str] = None,
    ) -> List[str]:
        pass

    @abstractmethod
    async def preview_summary(
        self,
        credentials: ConnectorCredentials,
        tb_token: str,
        tb_endpoint: str,
        parameters: ConnectorParameters,
        workspace_id: str,
        working_zone: Optional[str] = None,
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    async def preview(
        self,
        credentials: ConnectorCredentials,
        tb_token: str,
        tb_endpoint: str,
        parameters: ConnectorParameters,
        workspace_id: str,
        working_zone: Optional[str] = None,
    ) -> Tuple[bytes, Optional[dict[str, Any]]]:
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    async def execute_now(
        self,
        workspace_id: str,
        datasource_id: str,
    ) -> dict[Any, Any]:
        pass

    @abstractmethod
    async def retrieve_executions(
        self,
        workspace_id: str,
        datasource_id: str,
    ) -> List[dict[Any, Any]]:
        pass

    @abstractmethod
    async def remove_linker(
        self,
        workspace_id: str,
        datasource_id: str,
        job_executor: Optional[JobExecutor] = None,
    ) -> dict[Any, Any]:
        pass


class ConnectorContext:
    """
    This class defines the interface for the different AWS S3 connectors.
    This class leverages the Strategy pattern.
    """

    def __init__(self, connector: Connector) -> None:
        self._connector = connector

    async def _retrieve_preview(
        self, tb_endpoint: str, tb_token: str, preview_chunk: bytes
    ) -> dict[str, List[dict[str, Any]]]:
        protocol = "https://"
        if "localhost" in tb_endpoint or "127.0.0.1" in tb_endpoint:
            protocol = "http://"

        request = HTTPRequest(
            url=protocol + tb_endpoint + ANALYZE_ENDPOINT,
            method="POST",
            body=preview_chunk,
            headers={"Authorization": f"Bearer {tb_token}"},
        )
        client = AsyncHTTPClient()
        response = await client.fetch(request)
        return json.loads(response.body)

    async def get_bucket_list(
        self,
        credentials: ConnectorCredentials,
        working_zone: Optional[str] = None,
    ) -> List[str]:
        bucket_list = await self._connector.bucket_list(
            credentials=credentials,
            working_zone=working_zone,
        )

        return bucket_list

    async def get_preview_summary(
        self,
        tb_endpoint: str,
        tb_token: str,
        credentials: ConnectorCredentials,
        parameters: ConnectorParameters,
        workspace_id: str,
        working_zone: Optional[str] = None,
    ) -> dict[str, List[dict[str, Any]]]:
        preview_chunk = await self._connector.preview_summary(
            credentials=credentials,
            tb_token=tb_token,
            tb_endpoint=tb_endpoint,
            parameters=parameters,
            working_zone=working_zone,
            workspace_id=workspace_id,
        )

        return preview_chunk

    async def get_preview(
        self,
        tb_endpoint: str,
        tb_token: str,
        credentials: ConnectorCredentials,
        parameters: ConnectorParameters,
        workspace_id: str,
        working_zone: Optional[str] = None,
    ) -> dict[str, List[dict[str, Any]]]:
        preview_chunk, data_guessing = await self._connector.preview(
            credentials=credentials,
            tb_token=tb_token,
            tb_endpoint=tb_endpoint,
            parameters=parameters,
            working_zone=working_zone,
            workspace_id=workspace_id,
        )

        if not data_guessing or data_guessing.get("analysis") is None:
            data_guessing = await self._retrieve_preview(tb_endpoint, tb_token, preview_chunk)

        return data_guessing

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
        return await self._connector.link_connector(
            tb_token=tb_token,
            workspace_id=workspace_id,
            datasource_id=datasource_id,
            credentials=credentials,
            parameters=parameters,
            cron=cron,
            working_zone=working_zone,
            tb_endpoint=tb_endpoint,
        )

    async def execute_now(
        self,
        workspace_id: str,
        datasource_id: str,
    ) -> dict[Any, Any]:
        return await self._connector.execute_now(
            workspace_id=workspace_id,
            datasource_id=datasource_id,
        )

    async def remove_linker(
        self,
        workspace_id: str,
        datasource_id: str,
        job_executor: Optional[JobExecutor] = None,
    ) -> dict[Any, Any]:
        return await self._connector.remove_linker(
            workspace_id=workspace_id,
            datasource_id=datasource_id,
            job_executor=job_executor,
        )


@dataclass
class ConnectorException(Exception):
    message: str
