import enum
import logging
from typing import Callable, Dict, List, Optional, Protocol, TypeVar

from aiohttp import client_exceptions
from dateutil.parser import isoparse
from google.auth._default_async import default_async as _default_credentials_async
from google.auth.transport._aiohttp_requests import AuthorizedSession
from google.oauth2.credentials import Credentials

DEFAULT_RUNS_TO_FETCH = 50
T = TypeVar("T")


class ScheduleState(str, enum.Enum):
    RUNNING = "running"
    PAUSED = "paused"


class SchedulerRequestFailed(RuntimeError):
    pass


SCHEDULER_EMPTY_RESPONSE = "Received unexpected empty reponse from scheduler"
IS_PAUSED_KEY = "is_paused"


def _format_datetime(dt_str: Optional[str]) -> Optional[str]:
    # end_date & start_date can be None when the run is in flight and crash
    # the parsing so we need to check fo that
    if dt_str:
        return isoparse(dt_str).strftime("%Y-%m-%dT%H:%M:%SZ")
    return None


def _format_run_object(run: Dict) -> Dict:
    return {
        "id": run["dag_run_id"],
        "execution_date": _format_datetime(run["logical_date"]),
        "start_date": _format_datetime(run["start_date"]),
        "end_date": _format_datetime(run["end_date"]),
        "state": run["state"],
    }


class IngestionSchedule(Protocol):
    async def get_state(self) -> ScheduleState: ...

    async def pause(self) -> None: ...

    async def unpause(self) -> None: ...

    async def trigger(self) -> Dict: ...

    async def list_runs(self, limit: int = DEFAULT_RUNS_TO_FETCH) -> List[Dict]: ...

    def shutdown(self) -> None: ...


class ComposerIngestionSchedule(IngestionSchedule):
    _AUTH_SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

    def __init__(
        self,
        credentials: Credentials,
        webserver_url: str,
        workspace_id: str,
        datasource_id: str,
        timeout: int = 5,
    ):
        self._credentials = credentials
        self._webserver_url = webserver_url.rstrip("/")
        self._workspace_id = workspace_id
        self._datasource_id = datasource_id
        self._timeout = timeout

    async def get_state(self) -> ScheduleState:
        # https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/get_dag
        res = await self._send("GET", self._dag_path)
        if res is None or not res or IS_PAUSED_KEY not in res:
            logging.warning(f"{SCHEDULER_EMPTY_RESPONSE} for dag {self._dag_id} in workspace {self._workspace_id}")
            raise SchedulerRequestFailed(SCHEDULER_EMPTY_RESPONSE)
        paused = res[IS_PAUSED_KEY]
        return ScheduleState.PAUSED if paused else ScheduleState.RUNNING

    async def pause(self) -> None:
        # https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/patch_dag
        await self._patch(self._dag_path, json={IS_PAUSED_KEY: True})

    async def unpause(self) -> None:
        # https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/patch_dag
        await self._patch(self._dag_path, json={IS_PAUSED_KEY: False})

    async def trigger(self) -> Dict:
        # https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/post_dag_run
        res = await self._send("POST", self._dagrun_path, json={"conf": {}})
        if res is None:
            raise SchedulerRequestFailed(SCHEDULER_EMPTY_RESPONSE)
        if not res:
            raise SchedulerRequestFailed(
                "The service is being provisioned. It might take a while, please retry in a few seconds."
            )
        return {"run_id": res["dag_run_id"], "state": res["state"]}

    async def list_runs(self, limit: int = DEFAULT_RUNS_TO_FETCH) -> List[Dict]:
        # https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/get_dag_runs
        res = await self._send("GET", self._dagrun_path, params={"order_by": "-start_date", "limit": limit})
        if res is None:
            raise SchedulerRequestFailed(SCHEDULER_EMPTY_RESPONSE)
        if not res:
            return []
        return list(reversed([_format_run_object(run) for run in res["dag_runs"]]))

    def shutdown(self):
        pass

    @property
    def _dag_id(self) -> str:
        return f"{self._workspace_id}_{self._datasource_id}"

    @property
    def _dag_path(self) -> str:
        return f"dags/{self._dag_id}"

    @property
    def _dagrun_path(self) -> str:
        return f"dags/{self._dag_id}/dagRuns"

    async def _patch(self, path: str, json: Dict, **kwargs) -> Optional[Dict]:
        params = kwargs.pop("params", {})
        params["update_mask"] = ",".join(json.keys())
        return await self._send("PATCH", path, json=json, params=params, **kwargs)

    async def _send(self, method: str, path: str, **kwargs) -> Optional[Dict]:
        url = self._render_full_url(path)
        try:
            async with AuthorizedSession(self._credentials) as authed_session:
                res = await authed_session.request(method=method, url=url, timeout=self._timeout, **kwargs)
                res.raise_for_status()
                return await res.json() if res.content else None
        except client_exceptions.ClientResponseError as err:
            if err.status == 404:
                # This is the expected response when the DAG doesn't exist yet
                logging.info(f"404 received from Cloud Composer when calling {url}")
                return {}
            else:
                # Log the Requests exception so we can trace it and raise a generic one
                # so the downstream doesn't need to know about Requests
                logging.exception("The request to Cloud Composer failed")
                raise SchedulerRequestFailed() from err

    def _render_full_url(self, path: str) -> str:
        return f"{self._webserver_url}/api/v1/{path.lstrip('/')}"


def default_credentials_async(scopes: List[str]):
    return _default_credentials_async(scopes=scopes)[0]


async def get_schedule(
    webserver_url: str,
    workspace_id: str,
    datasource_id: str,
    credentials_provider: Callable = default_credentials_async,
    timeout: int = 3,
) -> IngestionSchedule:
    scopes = ComposerIngestionSchedule._AUTH_SCOPES
    credentials = credentials_provider(scopes=scopes)
    return ComposerIngestionSchedule(credentials, webserver_url, workspace_id, datasource_id, timeout)
