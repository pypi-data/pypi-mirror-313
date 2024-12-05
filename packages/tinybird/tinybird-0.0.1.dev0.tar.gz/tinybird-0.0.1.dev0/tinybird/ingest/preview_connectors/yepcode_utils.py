import asyncio
import json
import logging
from datetime import timezone
from enum import Enum
from pathlib import PurePosixPath
from typing import Any, Optional
from urllib.parse import urljoin

import orjson
from dateutil import parser
from pydantic import BaseModel, SecretStr
from tornado.httpclient import AsyncHTTPClient, HTTPError, HTTPResponse

from tinybird.data_connector import DataConnectors
from tinybird.datasource import Datasource
from tinybird.job import (
    Job,
    JobAlreadyBeingCancelledException,
    JobExecutor,
    JobKind,
    JobNotInCancellableStatusException,
)
from tinybird.user import User, UserDoesNotExist
from tinybird.views.api_errors.data_connectors import PreviewConnectorError

BASE_API_URL: str = "https://cloud.yepcode.io/api"


class YepCodeEnvironments(str, Enum):
    PRODUCTION = "tinybird"
    STAGING = "tinybird-staging"


class YepCodeSettings(BaseModel):
    environment: YepCodeEnvironments
    token: SecretStr = SecretStr("")

    def uri(self, endpoint: str) -> str:
        path = PurePosixPath().joinpath("api", self.environment.value, "webhooks", endpoint)
        return urljoin(BASE_API_URL, path.as_posix())

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.token.get_secret_value()}",
        }


yepcode_configuration = YepCodeSettings(environment=YepCodeEnvironments("tinybird"), token=SecretStr(""))


def set_yepcode_configuration(environment: str, token: str):
    global yepcode_configuration

    try:
        yepcode_configuration = YepCodeSettings(environment=YepCodeEnvironments(environment), token=SecretStr(token))
        logging.info("YepCode Connectors: Initialized for environment '%s'.", environment or "")
    except Exception as e:
        logging.exception("Error while configuring settings for YepCode", str(e))


AVAILABLE_CONNECTORS_ENDPOINT: str = "bef2777b-f423-44ed-929d-de9000a553db"
GET_CONNECTOR_DETAILS_ENDPOINT: str = "35548f24-4642-4b2b-b809-9859812b3fdc"
GET_PREVIEW_ENDPOINT: str = "525c9e16-94fb-44fc-adcb-b8b1e7eda7c8"
GET_BUCKET_LIST_ENDPOINT: str = "2d7203c5-97bc-4205-8b61-ea08e4265409"
CREATE_CONNECTOR_ENDPOINT: str = "e48f3f4d-d1b6-44d0-a94b-5214b44e2341"
GET_EXECUTIONS_ENDPOINT: str = "2d3cd642-e5ce-4c22-b726-c14474e4f83d"
GET_EXECUTION_DETAILS_ENDPOINT: str = "f6b04905-6d92-4c70-a692-d79ba506d3f4"
TRIGGER_EXECUTION_ENDPOINT: str = "06074248-6be6-4a8c-b0b1-d2f9cdb18d03"
PAUSE_EXECUTIONS_ENDPOINT: str = "146c48d5-89c2-4e4a-9429-f5411ffb14fd"
RESUME_EXECUTIONS_ENDPOINT: str = "0a6432b9-721f-47a3-9255-36867fff20f3"
REMOVE_DATASOURCE_ENDPOINT: str = "4a52e2f9-62e9-4888-a45d-a45a84019ae8"
GET_DATASOURCE_DETAILS_ENDPOINT: str = "datasources-getone"

DATASOURCES_ENDPOINT = "/v0/datasources"
ANALYZE_ENDPOINT = "/v0/analyze"
TB_ENDPOINT: str = "api.tinybird.co"

DATA_CONNECTORS: dict[DataConnectors, str] = {
    DataConnectors.AMAZON_S3: "aws-s3",
    DataConnectors.AMAZON_S3_IAMROLE: "aws-s3",
    DataConnectors.GCLOUD_STORAGE: "google-storage",
}

DEFAULT_TIMEOUT: float = 65.0

http_client = AsyncHTTPClient(defaults=dict(request_timeout=DEFAULT_TIMEOUT))


def get_error_message(response: HTTPResponse) -> Any:
    def extract_error_from_body(response_body):
        error_message = PreviewConnectorError.connection_error().message

        if response_body:
            error_message = response_body.get("error", {}).get(
                "message", PreviewConnectorError.connection_error().message
            )

        return error_message

    def extract_error_from_error(response_body):
        error_message = PreviewConnectorError.connection_error().message

        if response_body:
            error_message = response_body.get("error", PreviewConnectorError.connection_error().message)

        return error_message

    error_message = PreviewConnectorError.connection_error().message

    if response.code and response.code == 408:
        error_message = PreviewConnectorError.timeout_error().message
    elif response.body:
        try:
            response_body = orjson.loads(response.body)
            logging.warning(f"Error received from YepCode in Response Body: {response_body}")
            error_message = extract_error_from_body(response_body)
        except Exception:
            pass
    elif response.error:
        try:
            response_error = orjson.loads(response.error)
            error_message = extract_error_from_error(response_error)
        except Exception:
            pass

    return error_message


async def get_available_connectors(
    timeout: float = DEFAULT_TIMEOUT,
) -> dict:
    try:
        response: HTTPResponse = await http_client.fetch(
            f"{yepcode_configuration.uri(AVAILABLE_CONNECTORS_ENDPOINT)}",
            method="GET",
            headers=yepcode_configuration.headers,
            request_timeout=timeout,
        )
    except HTTPError as e:
        logging.error(f'Error fetching from YepCode "available connectors" endpoint: {str(e)}')
        return {"error": e.message}
    except Exception as e:
        logging.error(f'Error fetching from YepCode "available connectors" endpoint: {str(e)}')
        return {"error": PreviewConnectorError.connection_error().message}

    if response.code != 200:
        error_message = get_error_message(response)
        logging.error(
            f'Error received from YepCode "available connectors" endpoint: {str(response.error)} / {error_message}'
        )
        return {"error": error_message}

    return json.loads(response.body)


async def get_connector_details(
    connector: DataConnectors,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict:
    try:
        response: HTTPResponse = await http_client.fetch(
            f"{yepcode_configuration.uri(GET_CONNECTOR_DETAILS_ENDPOINT)}?connector={DATA_CONNECTORS[connector]}",
            method="GET",
            headers=yepcode_configuration.headers,
            request_timeout=timeout,
        )
    except HTTPError as e:
        logging.error(f'Error fetching from YepCode "get connector details" endpoint: {str(e)}')
        return {"error": e.message}
    except Exception as e:
        logging.error(f'Error fetching from YepCode "get connector details" endpoint: {str(e)}')
        return {"error": PreviewConnectorError.connection_error().message}

    if response.code != 200:
        error_message = get_error_message(response)
        logging.error(
            f'Error received from YepCode "get connector details" endpoint: {str(response.error)} / {error_message}'
        )
        return {"error": error_message}

    return json.loads(response.body)


async def get_preview(
    connector: DataConnectors,
    tb_token: str,
    tb_endpoint: str,
    credentials: dict[str, str],
    params: dict[str, str],
    workspace_id: str,
    zone_id: Optional[str],
    timeout: float = DEFAULT_TIMEOUT,
) -> dict:
    headers = {
        "accept": "application/json",
        "Yep-Comment": workspace_id,
    }

    ingestion_domain = tb_endpoint
    assert tb_endpoint
    ingestion_endpoint = urljoin(f"https://{tb_endpoint}", ANALYZE_ENDPOINT)

    json_data = {
        "zoneId": zone_id,
        "connector": DATA_CONNECTORS[connector],
        "credentials": credentials,
        "ingestionDomain": ingestion_domain,
        "ingestionEndpoint": ingestion_endpoint,
        "apiToken": tb_token,
        "params": params,
    }

    try:
        response: HTTPResponse = await http_client.fetch(
            yepcode_configuration.uri(GET_PREVIEW_ENDPOINT),
            method="POST",
            headers=yepcode_configuration.headers | headers,
            body=json.dumps(json_data).encode("utf-8"),
            request_timeout=timeout,
            raise_error=False,
        )
    except HTTPError as e:
        logging.error(f'Error fetching from YepCode "get preview" endpoint: {str(e)}')
        return {"error": e.message}
    except Exception as e:
        logging.error(f'Error fetching from YepCode "get preview" endpoint: {str(e)}')
        return {"error": PreviewConnectorError.connection_error().message}

    if response.code != 200:
        error_message = get_error_message(response)
        logging.error(f'Error received from YepCode "get preview" endpoint: {str(response.error)} / {error_message}')
        return {"error": error_message}

    return json.loads(response.body)


async def get_bucket_list(
    connector: DataConnectors,
    credentials: dict[str, str],
    zone_id: Optional[str],
    timeout: float = DEFAULT_TIMEOUT,
) -> dict:
    headers = {
        "accept": "application/json",
    }

    json_data = {
        "zoneId": zone_id,
        "connector": DATA_CONNECTORS[connector],
        "credentials": credentials,
    }

    try:
        response: HTTPResponse = await http_client.fetch(
            yepcode_configuration.uri(GET_BUCKET_LIST_ENDPOINT),
            method="POST",
            headers=yepcode_configuration.headers | headers,
            body=json.dumps(json_data).encode("utf-8"),
            request_timeout=timeout,
            raise_error=False,
        )
    except HTTPError as e:
        logging.error(f'Error fetching from YepCode "get preview dry run" endpoint: {str(e)}')
        return {"error": e.message}
    except Exception as e:
        logging.error(f'Error fetching from YepCode "get preview dry run" endpoint: {str(e)}')
        return {"error": PreviewConnectorError.connection_error().message}

    if response.code != 200:
        error_message = get_error_message(response)
        logging.error(
            f'Error received from YepCode "get preview dry run" endpoint: {str(response.error)} / {error_message}'
        )
        return {"error": error_message}

    return json.loads(response.body)


async def create_connector(
    connector: DataConnectors,
    tb_token: str,
    workspace_id: str,
    datasource_id: str,
    credentials: dict[str, str],
    params: dict[str, str],
    cron: Optional[str],
    zone_id: Optional[str],
    timeout: float = DEFAULT_TIMEOUT,
    tb_endpoint: Optional[str] = TB_ENDPOINT,
) -> dict:
    ingestion_domain = tb_endpoint
    assert tb_endpoint
    ingestion_endpoint = urljoin(f"https://{tb_endpoint}", DATASOURCES_ENDPOINT)
    json_data = {
        "zoneId": zone_id,
        "ingestionEndpoint": ingestion_endpoint,
        "ingestionDomain": ingestion_domain,
        "workspace": workspace_id,
        "datasource": datasource_id,
        "apiToken": tb_token,
        "connector": DATA_CONNECTORS[connector],
        "cron": cron,
        "credentials": credentials,
        "params": params,
    }

    workspace = None
    is_branch = False
    try:
        workspace = User.get_by_id(workspace_id)
        is_branch = workspace.is_branch
    except UserDoesNotExist:
        logging.warning(f"Workspace {workspace_id} does not exist")

    headers = {"Yep-Comment": f"{workspace_id}__##__{datasource_id}"}
    try:
        response: HTTPResponse = await http_client.fetch(
            yepcode_configuration.uri(CREATE_CONNECTOR_ENDPOINT),
            method="POST",
            headers=yepcode_configuration.headers | headers,
            body=json.dumps(json_data).encode("utf-8"),
            request_timeout=timeout,
        )
    except HTTPError as e:
        log_exception(f'Error fetching from YepCode "create connector" endpoint: {str(e)}', is_branch)
        return {"error": e.message}
    except Exception as e:
        log_exception(f'Error fetching from YepCode "create connector" endpoint: {str(e)}', is_branch)
        return {"error": PreviewConnectorError.connection_error().message}

    if response.code != 200:
        error_message = get_error_message(response)
        log_exception(
            f'Error received from YepCode "create connector" endpoint: {str(response.error)} / {error_message}',
            is_branch,
        )
        return {"error": error_message}

    return json.loads(response.body)


async def get_executions(
    workspace_id: str,
    datasource_id: str,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict:
    json_data = {
        "workspace": workspace_id,
        "datasource": datasource_id,
    }

    workspace = None
    is_branch = False
    try:
        workspace = User.get_by_id(workspace_id)
        is_branch = workspace.is_branch
    except UserDoesNotExist:
        logging.warning(f"Workspace {workspace_id} does not exist")

    try:
        response: HTTPResponse = await http_client.fetch(
            yepcode_configuration.uri(GET_EXECUTIONS_ENDPOINT),
            method="POST",
            headers=yepcode_configuration.headers,
            body=json.dumps(json_data).encode("utf-8"),
            request_timeout=timeout,
        )
    except HTTPError as e:
        log_exception(f'Error fetching from YepCode "get executions" endpoint: {str(e)}', is_branch)
        return {"error": e.message}
    except Exception as e:
        log_exception(f'Error fetching from YepCode "get executions" endpoint: {str(e)}', is_branch)
        return {"error": PreviewConnectorError.connection_error().message}

    if response.code != 200:
        error_message = get_error_message(response)
        log_exception(
            f'Error fetching from YepCode "get executions" endpoint: {str(response.error)} / {error_message}',
            is_branch,
        )
        return {"error": error_message}

    return json.loads(response.body)


async def get_execution_details(
    workspace_id: str,
    datasource_id: str,
    execution_id: str,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict:
    json_data = {
        "workspace": workspace_id,
        "datasource": datasource_id,
        "executionId": execution_id,
    }

    workspace = None
    is_branch = False
    try:
        workspace = User.get_by_id(workspace_id)
        is_branch = workspace.is_branch
    except UserDoesNotExist:
        logging.warning(f"Workspace {workspace_id} does not exist")

    try:
        response: HTTPResponse = await http_client.fetch(
            yepcode_configuration.uri(GET_EXECUTION_DETAILS_ENDPOINT),
            method="POST",
            headers=yepcode_configuration.headers,
            body=json.dumps(json_data).encode("utf-8"),
            request_timeout=timeout,
        )
    except HTTPError as e:
        log_exception(f'Error fetching from YepCode "get execution details" endpoint: {str(e)}', is_branch)
        return {"error": e.message}
    except Exception as e:
        log_exception(f'Error fetching from YepCode "get execution details" endpoint: {str(e)}', is_branch)
        return {"error": PreviewConnectorError.connection_error().message}

    if response.code != 200:
        error_message = get_error_message(response)
        log_exception(
            f'Error received from YepCode "get execution details" endpoint: {str(response.error)} / {error_message}',
            is_branch,
        )
        return {"error": error_message}

    return json.loads(response.body)


async def trigger_execution(
    workspace_id: str,
    datasource_id: str,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict:
    json_data = {
        "workspace": workspace_id,
        "datasource": datasource_id,
    }

    workspace = None

    workspace = None
    is_branch = False
    try:
        workspace = User.get_by_id(workspace_id)
        is_branch = workspace.is_branch
    except UserDoesNotExist:
        logging.warning(f"Workspace {workspace_id} does not exist")

    headers = {"Yep-Comment": f"{workspace_id}__##__{datasource_id}"}
    try:
        response: HTTPResponse = await http_client.fetch(
            yepcode_configuration.uri(TRIGGER_EXECUTION_ENDPOINT),
            method="POST",
            headers=yepcode_configuration.headers | headers,
            body=json.dumps(json_data).encode("utf-8"),
            request_timeout=timeout,
        )
    except HTTPError as e:
        log_exception(f'Error fetching from YepCode "trigger execution" endpoint: {str(e)}', is_branch)
        return {"error": e.message}
    except Exception as e:
        log_exception(f'Error fetching from YepCode "trigger execution" endpoint: {str(e)}', is_branch)
        return {"error": PreviewConnectorError.connection_error().message}

    if response.code != 200:
        error_message = get_error_message(response)
        log_exception(
            f'Error received from YepCode "trigger execution" endpoint: {str(response.error)} / {error_message}',
            is_branch,
        )
        return {"error": error_message}

    return json.loads(response.body)


async def pause_executions(
    workspace_id: str,
    datasource_id: str,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict:
    json_data = {
        "workspace": workspace_id,
        "datasource": datasource_id,
    }

    workspace = None
    is_branch = False
    try:
        workspace = User.get_by_id(workspace_id)
        is_branch = workspace.is_branch
    except UserDoesNotExist:
        logging.warning(f"Workspace {workspace_id} does not exist")

    try:
        response: HTTPResponse = await http_client.fetch(
            yepcode_configuration.uri(PAUSE_EXECUTIONS_ENDPOINT),
            method="POST",
            headers=yepcode_configuration.headers,
            body=json.dumps(json_data).encode("utf-8"),
            request_timeout=timeout,
        )
    except HTTPError as e:
        log_exception(f'Error fetching from YepCode "pause execution" endpoint: {str(e)}', is_branch)
        return {"error": e.message}
    except Exception as e:
        log_exception(f'Error fetching from YepCode "pause execution" endpoint: {str(e)}', is_branch)
        return {"error": PreviewConnectorError.connection_error().message}

    if response.code != 200:
        error_message = get_error_message(response)
        log_exception(
            f'Error received from YepCode "pause execution" endpoint: {str(response.error)} / {error_message}',
            is_branch,
        )
        return {"error": error_message}

    return {}


async def resume_executions(
    workspace_id: str,
    datasource_id: str,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict:
    json_data = {
        "workspace": workspace_id,
        "datasource": datasource_id,
    }

    workspace = None
    is_branch = False
    try:
        workspace = User.get_by_id(workspace_id)
        is_branch = workspace.is_branch
    except UserDoesNotExist:
        logging.warning(f"Workspace {workspace_id} does not exist")

    try:
        response: HTTPResponse = await http_client.fetch(
            yepcode_configuration.uri(RESUME_EXECUTIONS_ENDPOINT),
            method="POST",
            headers=yepcode_configuration.headers,
            body=json.dumps(json_data).encode("utf-8"),
            request_timeout=timeout,
        )
    except HTTPError as e:
        log_exception(f'Error fetching from YepCode "resume execution" endpoint: {str(e)}', is_branch)
        return {"error": e.message}
    except Exception as e:
        log_exception(f'Error fetching from YepCode "resume execution" endpoint: {str(e)}', is_branch)
        return {"error": PreviewConnectorError.connection_error().message}

    if response.code != 200:
        error_message = get_error_message(response)
        log_exception(
            f'Error received from YepCode "resume execution" endpoint: {str(response.error)} / {error_message}',
            is_branch,
        )
        return {"error": error_message}

    return {}


async def get_datasource_details(
    workspace_id: str,
    datasource_id: str,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict:
    json_data = {
        "workspace": workspace_id,
        "datasource": datasource_id,
    }

    is_branch = False
    try:
        workspace = User.get_by_id(workspace_id)
        is_branch = workspace.is_branch
    except UserDoesNotExist:
        logging.warning(f"Workspace {workspace_id} does not exist")

    try:
        response: HTTPResponse = await http_client.fetch(
            yepcode_configuration.uri(GET_DATASOURCE_DETAILS_ENDPOINT),
            method="POST",
            headers=yepcode_configuration.headers,
            body=json.dumps(json_data).encode("utf-8"),
            request_timeout=timeout,
        )
    except HTTPError as e:
        log_exception(f'Error fetching from YepCode "get datasource details" endpoint: {str(e)}', is_branch)
        return {"error": e.message}
    except Exception as e:
        log_exception(f'Error fetching from YepCode "get datasource details" endpoint: {str(e)}', is_branch)
        return {"error": PreviewConnectorError.connection_error().message}

    if response.code != 200:
        error_message = get_error_message(response)
        log_exception(
            f'Error received from YepCode "get datasource details" endpoint: {str(response.error)} / {error_message}',
            is_branch,
        )
        return {"error": error_message}

    return json.loads(response.body)


class YepCodeDatasourceNotFound(Exception):
    pass


class YepCodeRemoveDatasourceError(Exception):
    pass


async def remove_datasource(
    workspace_id: str,
    datasource_id: str,
    timeout: float = DEFAULT_TIMEOUT,
) -> None:
    json_data = {
        "workspace": workspace_id,
        "datasource": datasource_id,
    }

    workspace = None
    is_branch = False
    try:
        workspace = User.get_by_id(workspace_id)
        is_branch = workspace.is_branch
    except UserDoesNotExist:
        logging.warning(f"Workspace {workspace_id} does not exist")

    headers = {"Yep-Comment": f"{workspace_id}__##__{datasource_id}"}
    try:
        await http_client.fetch(
            yepcode_configuration.uri(REMOVE_DATASOURCE_ENDPOINT),
            method="POST",
            headers=yepcode_configuration.headers | headers,
            body=json.dumps(json_data).encode("utf-8"),
            request_timeout=timeout,
        )
    except HTTPError as e:
        http_response: HTTPResponse = e.response
        response_code = http_response.code
        error_message = get_error_message(http_response)

        log_exception(f'Error fetching from YepCode "remove datasource" endpoint: {str(e)}', is_branch)

        if response_code == 404 and error_message.startswith("Datasource not found"):
            raise YepCodeDatasourceNotFound(error_message) from e

        raise YepCodeRemoveDatasourceError(PreviewConnectorError.connection_error().message) from e
    except Exception as e:
        log_exception(f'Error fetching from YepCode "remove datasource" endpoint: {str(e)}', is_branch)
        raise YepCodeRemoveDatasourceError(PreviewConnectorError.connection_error().message) from e


async def cancel_datasource_jobs(datasource_id: str, job_executor: Optional[JobExecutor] = None) -> None:
    """
    Cancel Datasource jobs
    """
    if not job_executor:
        logging.error("No job_executor present. Can't cancel datasource jobs.")
        return

    def is_job_to_cancel(job: Job) -> bool:
        if not hasattr(job, "datasource"):
            return False
        if not isinstance(job.datasource, Datasource):
            return False

        is_import = job.kind == JobKind.IMPORT
        is_datasource = job.datasource.id == datasource_id
        return bool(is_import and is_datasource)

    def cancel_jobs() -> None:
        jobs = job_executor.get_pending_jobs()
        for job in filter(is_job_to_cancel, jobs):
            if job.can_be_mark_as_cancelled:
                job.mark_as_cancelled()
            elif job.is_cancellable:
                try:
                    job.try_to_cancel(job_executor=job_executor)
                except (JobNotInCancellableStatusException, JobAlreadyBeingCancelledException):
                    pass

    await asyncio.get_running_loop().run_in_executor(None, cancel_jobs)


def log_exception(error: str, is_branch: Optional[bool] = False):
    if not is_branch:
        logging.warning(error)
    else:
        logging.warning(error)


def format_date_to_iso_utc(date_string):
    """
    Convert various datetime string formats to UTC ISO 8601 format with 'Z' suffix.

    >>> format_date_to_iso_utc('2021-09-01 00:00:00')
    '2021-09-01T00:00:00Z'
    >>> format_date_to_iso_utc('2021-09-01T00:00:00')
    '2021-09-01T00:00:00Z'
    >>> format_date_to_iso_utc('2021-09-01T00:00:00Z')
    '2021-09-01T00:00:00Z'
    >>> format_date_to_iso_utc('2021-09-01T00:00:00+02:00')
    '2021-08-31T22:00:00Z'
    >>> format_date_to_iso_utc('2021-09-01')
    '2021-09-01T00:00:00Z'
    >>> format_date_to_iso_utc('09/01/2021 15:30:45')
    '2021-09-01T15:30:45Z'
    >>> format_date_to_iso_utc('01-Sep-2021 15:30:45')
    '2021-09-01T15:30:45Z'
    >>> format_date_to_iso_utc('2021-09-01T00:00:00.123456')
    '2021-09-01T00:00:00Z'
    >>> format_date_to_iso_utc('2021-09-01T00:00:00.123456Z')
    '2021-09-01T00:00:00Z'
    >>> format_date_to_iso_utc('2021-09-01T00:00:00.123456+02:00')
    '2021-08-31T22:00:00Z'
    >>> format_date_to_iso_utc('invalid date')
    Traceback (most recent call last):
        ...
    ValueError: Invalid date format: invalid date
    """
    try:
        dt = parser.parse(date_string)
        # If the datetime is naive (no timezone info), assume it's in UTC
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            # Convert to UTC
            dt = dt.astimezone(timezone.utc)

        # Format to ISO 8601 with 'Z' suffix and return
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        raise ValueError(f"Invalid date format: {date_string}")
