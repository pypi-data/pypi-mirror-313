import json
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlencode

import aiohttp

from tinybird.integrations.integration import IntegrationInfo
from tinybird.model import RedisModel, retry_transaction_in_case_of_concurrent_edition_error_async
from tinybird.user import UserAccount, UserAccounts, Users, WorkspaceName
from tinybird.views.aiohttp_shared_session import get_shared_session


class VercelIntegrationException(Exception):
    """Vercel integration related exception"""

    pass


class VercelIntegrationPhase:
    """Contains constants related with the integration lifecycle"""

    INSTALLING: int = 0
    CONFIGURED: int = 1


class VercelIntegrationPagination:
    """Default values for pagination used in Vercel API"""

    PROJECT_LIMIT: int = 40


@dataclass
class VercelIntegrationBindInfo:
    """Maps the binding of a Vercel environment variable with a specific TB token."""

    vercel_project_id: str
    vercel_env_key: str
    vercel_env_id: str
    workspace_id: str
    token: str
    created_at: datetime = field(default_factory=lambda: datetime.now())
    vercel_env_type: str = "encrypted"
    vercel_environments: List[str] = field(default_factory=lambda: ["production", "preview", "development"])


class VercelIntegrationDoesNotExist(Exception):
    pass


class VercelIntegration(RedisModel):
    __namespace__ = "integrations"
    __props__ = [
        "integration_user_id",
        "access_code",
        "integration_phase",
        "access_token",
        "token_type",
        "team_id",
        "installation_id",
        "bindings",
    ]

    __indexes__ = ["installation_id"]

    def __init__(self, **int_dict: Any) -> None:
        self.integration_user_id: str = ""
        self.access_code: Optional[str] = None
        self.integration_phase: int = VercelIntegrationPhase.INSTALLING
        self.access_token: str = ""
        self.token_type: str = "Bearer"
        self.team_id: Optional[str] = None
        # Choose a random installation_id because we use it as a secondary key and
        # don't want to have two different integrations sharing it.
        self.installation_id: str = str(uuid.uuid4())
        self.bindings: List[VercelIntegrationBindInfo] = []

        super().__init__(**int_dict)

    def get_bindings(
        self, by_project_id: Optional[str] = None, by_workspace_id: Optional[str] = None, by_token: Optional[str] = None
    ) -> List[VercelIntegrationBindInfo]:
        return [
            b
            for b in self.bindings
            if (not by_project_id or b.vercel_project_id == by_project_id)
            and (not by_workspace_id or b.workspace_id == by_workspace_id)
            and (not by_token or b.token == by_token)
        ]

    @staticmethod
    def get_by_installation_id(installation_id: str) -> "VercelIntegration":
        integration = VercelIntegration.get_by_index("installation_id", installation_id)
        if not integration:
            raise VercelIntegrationDoesNotExist(f"Integration ({installation_id}) does not exist")
        return integration


class VercelIntegrationService:
    _client_id: str = ""
    _client_secret: str = ""
    _redirect_uri: str = ""

    @staticmethod
    def get_default_env_name(workspace_id: str, token: str) -> str:
        workspace = Users.get_by_id(workspace_id)
        tinfo = workspace.get_token_access_info(token)
        if not tinfo:
            raise VercelIntegrationException(f"Unknown token for workspace {workspace_id}")
        env_name = WorkspaceName.create_from_not_normalized_name(f"TB_{workspace.name}_{tinfo.name}")
        return str(env_name).upper()

    @staticmethod
    async def get_integration_for_user(user: UserAccount, access_code: Optional[str] = None) -> VercelIntegration:
        result: Optional[VercelIntegration] = None

        info: Optional[IntegrationInfo] = next((i for i in user.get_integration_info_by_type("vercel")), None)
        if info:
            result = VercelIntegration.get_by_id(info.integration_id)
            if not result:
                user = await UserAccounts.remove_integration(user, info.integration_id)
            else:
                return result

        if not result:
            result = VercelIntegration()
            result.integration_user_id = user.id
            result.access_code = access_code
            result.save()

        return result

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def add_bindings(
        integration: VercelIntegration, project_id: str, workspace_id: str, tokens: List[str]
    ) -> VercelIntegration:
        bindings = [
            VercelIntegrationBindInfo(
                project_id, VercelIntegrationService.get_default_env_name(workspace_id, t), "", workspace_id, t
            )
            for t in tokens
        ]

        url: str = f"https://api.vercel.com/v10/projects/{project_id}/env"
        params = [
            {"key": b.vercel_env_key, "value": b.token, "type": b.vercel_env_type, "target": b.vercel_environments}
            for b in bindings
        ]

        _, response = await VercelIntegrationService._vercel_post(
            integration, url, params=json.dumps(params), expected_codes=[200, 201]
        )

        created: List[Dict[str, Any]] = json.loads(response).get("created", [])
        if len(created) != len(bindings):
            logging.warning(
                f"[Vercel integration] Returned env vars count differs (send {len(bindings)}, received {len(created)}): {response}"
            )

        def get_binding_by_env(env: str) -> Optional[VercelIntegrationBindInfo]:
            return next((b for b in bindings if b.vercel_env_key == env), None)

        for new_env in created:
            binding = get_binding_by_env(new_env.get("key", ""))
            if binding:
                binding.vercel_env_id = new_env.get("id", "")

        with VercelIntegration.transaction(integration.id) as vi:
            for b in bindings:
                vi.bindings.append(b)
            return vi

    @staticmethod
    async def _remove_remote_bindings(
        integration: VercelIntegration, project_id: str, bindings: List[VercelIntegrationBindInfo]
    ) -> None:
        for b in bindings:
            try:
                url: str = f"https://api.vercel.com/v9/projects/{project_id}/env/{b.vercel_env_id}"
                _, _ = await VercelIntegrationService._vercel_delete(integration, url, expected_codes=[200, 201])
            except Exception as ex:
                logging.warning(
                    f"[Vercel integration] Couldn't remove {b.vercel_env_key} from project {project_id}: {ex}"
                )

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def remove_bindings(integration: VercelIntegration, project_id: str, tokens: List[str]) -> VercelIntegration:
        to_delete = [b for b in integration.get_bindings(by_project_id=project_id) if b.token in tokens]
        await VercelIntegrationService._remove_remote_bindings(integration, project_id, to_delete)

        with VercelIntegration.transaction(integration.id) as vi:
            vi.bindings = [b for b in vi.bindings if b.token not in tokens]
            return vi

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def remove_binding(
        integration: VercelIntegration, project_id: str, workspace_id: str, token: str
    ) -> VercelIntegration:
        to_delete = [
            b
            for b in integration.get_bindings(by_project_id=project_id, by_workspace_id=workspace_id)
            if b.token == token
        ]
        await VercelIntegrationService._remove_remote_bindings(integration, project_id, to_delete)

        with VercelIntegration.transaction(integration.id) as vi:
            vi.bindings = [b for b in vi.bindings if b not in to_delete]
            return vi

    @staticmethod
    async def _update_remote_binding(
        integration: VercelIntegration, project_id: str, env_name: str, env_id: str, new_token: str
    ) -> None:
        try:
            url: str = f"https://api.vercel.com/v9/projects/{project_id}/env/{env_id}"
            params = {"value": new_token}
            _, _ = await VercelIntegrationService._vercel_patch(
                integration, url, params=json.dumps(params), expected_codes=[200, 201]
            )
        except Exception as ex:
            logging.warning(
                f"[Vercel integration] Couldn't update {env_id} ({env_name}) from project {project_id}: {ex}"
            )

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def update_bindings_token(
        integration: VercelIntegration, bindings: List[VercelIntegrationBindInfo], new_token: str
    ) -> VercelIntegration:
        with VercelIntegration.transaction(integration.id) as vi:
            for b in bindings:
                await VercelIntegrationService._update_remote_binding(
                    integration, b.vercel_project_id, b.vercel_env_key, b.vercel_env_id, new_token
                )
                b.token = new_token
            return vi

    @staticmethod
    async def get_integration_owner_info(integration: VercelIntegration) -> Dict[str, Any]:
        try:
            owner_id: Optional[str] = integration.team_id
            owner_api = f"teams/{owner_id}" if owner_id else "user"
            _, result = await VercelIntegrationService._vercel_get(
                integration, f"https://api.vercel.com/v2/{owner_api}"
            )
            return json.loads(result)
        except Exception as ex:
            logging.warning(f"[Vercel integration] Error fetching installation owner info: {ex}")

        return {"id": owner_id, "name": "<unknown>"}

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def finalize_install(integration: VercelIntegration) -> VercelIntegration:
        if integration.integration_phase == VercelIntegrationPhase.CONFIGURED:
            raise VercelIntegrationException(f"Vercel integration {integration.id} is already installed.")

        if not integration.access_code:
            raise VercelIntegrationException("Missing access_code.")

        url: str = "https://api.vercel.com/v2/oauth/access_token"

        params: Dict[str, Any] = {
            "redirect_uri": VercelIntegrationService._redirect_uri,
            "client_secret": VercelIntegrationService._client_secret,
            "client_id": VercelIntegrationService._client_id,
            "code": integration.access_code,
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        _, response = await VercelIntegrationService._vercel_post(
            integration, url, headers, params, expected_codes=[200]
        )
        data: Dict[str, Any] = json.loads(response)
        with VercelIntegration.transaction(integration.id) as vi:
            vi.access_code = ""
            vi.access_token = data.get("access_token", "")
            vi.token_type = data.get("token_type", "Bearer")
            vi.team_id = data.get("team_id", None)
            vi.installation_id = data.get("installation_id", "")
            vi.integration_phase = VercelIntegrationPhase.CONFIGURED
            return vi

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def get_projects(
        integration: VercelIntegration, next_timestamp: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        if integration.integration_phase != VercelIntegrationPhase.CONFIGURED:
            raise VercelIntegrationException(f"Vercel integration {integration.id} not installed.")

        url: str = "https://api.vercel.com/v9/projects"
        params: Dict[str, Any] = {"limit": VercelIntegrationPagination.PROJECT_LIMIT}

        if next_timestamp:
            params["until"] = next_timestamp

        _, response = await VercelIntegrationService._vercel_get(integration, url, params=params, expected_codes=[200])
        data: Dict[str, Any] = json.loads(response)
        projects = data.get("projects", [])
        pagination = data.get("pagination", {})
        return projects, pagination

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def get_project(integration: VercelIntegration, project_id: str) -> Dict[str, Any]:
        if integration.integration_phase != VercelIntegrationPhase.CONFIGURED:
            raise VercelIntegrationException(f"Vercel integration {integration.id} not installed.")

        url: str = f"https://api.vercel.com/v9/projects/{project_id}"
        _, response = await VercelIntegrationService._vercel_get(integration, url, expected_codes=[200])
        return json.loads(response)

    @staticmethod
    async def remove_integration(user: UserAccount, integration_id: str, remove_remote: bool = True) -> UserAccount:
        integration = VercelIntegration.get_by_id(integration_id)
        if integration and remove_remote:
            url: str = f"/v1/integrations/configuration/{integration.installation_id}"
            try:
                _, _ = await VercelIntegrationService._vercel_delete(integration, url, expected_codes=[204])
            except Exception as ex:
                logging.warning(f"[VercelIntegration] Error deleting remote integration {integration_id}: {ex}")
        result: UserAccount = await UserAccounts.remove_integration(user, integration_id)
        VercelIntegration._delete(integration_id)
        return result

    @staticmethod
    async def _handle_vercel_response(
        resp: aiohttp.ClientResponse, expected_codes: Optional[List[int]] = None
    ) -> Tuple[int, str]:
        """Handles a Vercel API response and returns a tuple containing the response code and the full response contents.

        Allows to raise an exception in the case of an unexpected response code.
        """

        content: str
        try:
            content = (await resp.content.read()).decode("utf-8")
        except Exception as ex:
            logging.warning(f"Error reading Vercel response: {ex}")
            content = ""

        if expected_codes and resp.status not in expected_codes:
            raise VercelIntegrationException(
                f"Vercel returned an unexpected HTTP {resp.status} response code: {content}"
            )
        return (resp.status, content)

    @staticmethod
    async def _vercel_request(
        integration: VercelIntegration,
        method: str,
        url: str,
        headers: Optional[Dict[str, Any]] = None,
        params: Any = None,
        expected_codes: Optional[List[int]] = None,
        timeout: Optional[int] = None,
    ) -> Tuple[int, str]:
        """Performs a request against the Vercel API"""

        timeout = timeout or 10

        if integration.team_id:
            separator = "?" if "?" not in url else "&"
            url = f"{url}{separator}{urlencode({'teamId': integration.team_id})}"

        request_headers = headers.copy() if headers else {}
        if integration.access_token:
            request_headers["Authorization"] = f"Bearer {integration.access_token}"

        session: aiohttp.ClientSession = get_shared_session()
        async with session.request(method, url, headers=request_headers, data=params, timeout=timeout) as resp:
            return await VercelIntegrationService._handle_vercel_response(resp, expected_codes)

    @staticmethod
    async def _vercel_post(
        integration: VercelIntegration,
        url: str,
        headers: Optional[Dict[str, Any]] = None,
        params: Any = None,
        expected_codes: Optional[List[int]] = None,
        timeout: Optional[int] = None,
    ) -> Tuple[int, str]:
        """Performs a POST request against the Vercel API"""
        return await VercelIntegrationService._vercel_request(
            integration, "post", url, headers, params, expected_codes, timeout
        )

    @staticmethod
    async def _vercel_get(
        integration: VercelIntegration,
        url: str,
        headers: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        expected_codes: Optional[List[int]] = None,
        timeout: Optional[int] = None,
    ) -> Tuple[int, str]:
        """Performs a GET request against the Vercel API"""
        query_params: Dict[str, Any] = params.copy() if params else {}
        if integration.team_id:
            query_params["teamId"] = integration.team_id

        if query_params:
            separator = "?" if "?" not in url else "&"
            url = f"{url}{separator}{urlencode(query_params)}"

        return await VercelIntegrationService._vercel_request(
            integration, "get", url, headers, None, expected_codes, timeout
        )

    @staticmethod
    async def _vercel_delete(
        integration: VercelIntegration,
        url: str,
        headers: Optional[Dict[str, Any]] = None,
        expected_codes: Optional[List[int]] = None,
        timeout: Optional[int] = 10,
    ) -> Tuple[int, str]:
        """Performs a GET request against the Vercel API"""
        return await VercelIntegrationService._vercel_request(
            integration, "delete", url, headers, None, expected_codes, timeout
        )

    @staticmethod
    async def _vercel_patch(
        integration: VercelIntegration,
        url: str,
        headers: Optional[Dict[str, Any]] = None,
        params: Any = None,
        expected_codes: Optional[List[int]] = None,
        timeout: Optional[int] = None,
    ) -> Tuple[int, str]:
        """Performs a POST request against the Vercel API"""
        return await VercelIntegrationService._vercel_request(
            integration, "patch", url, headers, params, expected_codes, timeout
        )

    @staticmethod
    def config(conf: Dict[str, Any]) -> None:
        """Configures the needed secrets for Vercel API interop."""
        VercelIntegrationService._client_id = conf.get("client_id", "")
        VercelIntegrationService._client_secret = conf.get("client_secret", "")
        VercelIntegrationService._redirect_uri = conf.get("redirect_uri", "")
