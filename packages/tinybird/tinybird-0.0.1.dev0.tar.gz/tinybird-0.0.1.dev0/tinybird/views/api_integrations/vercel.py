import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from tornado.web import url

from tinybird.integrations.vercel import (
    VercelIntegration,
    VercelIntegrationBindInfo,
    VercelIntegrationPhase,
    VercelIntegrationService,
)
from tinybird.tokens import AccessToken
from tinybird.user import User, UserAccount, UserAccounts

from ..base import ApiHTTPError, BaseHandler, requires_write_access, user_authenticated


class APIIntegrationsHandlerBase(BaseHandler):
    """Base handler class for all integrations"""

    def check_xsrf_cookie(self) -> None:
        pass


def vercel_project_to_api_dict(project: Dict[str, Any]) -> Dict[str, Any]:
    """Maps a Vercel API project response to an internal one.

    Vercel spec at https://vercel.com/docs/rest-api#endpoints/projects/find-a-project-by-id-or-name/response.
    """
    return {
        "vercel_project_id": project["id"],
        "vercel_project_name": project["name"],
    }


class APIVercelIntegrationHandlerBase(BaseHandler):
    def __init__(self, *args, **kwargs) -> None:
        self._remote_projects: Dict[str, Dict[str, Any]] = {}
        super().__init__(*args, **kwargs)

    async def _fetch_remote_projects(
        self, integration: VercelIntegration, next_timestamp: str
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """Fetches and caches all remote projects from Vercel"""
        return await VercelIntegrationService.get_projects(integration, next_timestamp)

    async def _get_remote_project(self, integration: VercelIntegration, project_id: str) -> Optional[Dict[str, Any]]:
        """Gets a Vercel project from local cache or directly from the Vercel API

        Updates the local cache accordingly.
        """
        result: Optional[Dict[str, Any]] = self._remote_projects.get(project_id, None)

        if not result:
            # Try to get directly from the Vercel API and update the cache
            result = await VercelIntegrationService.get_project(integration, project_id)
            if result and ("id" in result):
                self._remote_projects[result["id"]] = result

        return result

    @staticmethod
    def get_integration(integration_id: str) -> VercelIntegration:
        result = VercelIntegration.get_by_id(integration_id)
        if not result:
            raise ApiHTTPError(400, "Integration not found")
        return result


class APIVercelIntegrationProjectListHandler(APIVercelIntegrationHandlerBase):
    @user_authenticated
    async def get(self, integration_id: str) -> None:
        integration = self.get_integration(integration_id)
        next_timestamp = self.get_argument("next_timestamp", "")
        remote_projects, pagination = await self._fetch_remote_projects(integration, next_timestamp)
        return self.write_json(
            {"data": [vercel_project_to_api_dict(item) for item in remote_projects], "pagination": pagination}
        )


class APIVercelIntegrationProjectsHandler(APIVercelIntegrationHandlerBase):
    async def get_project(self, integration: VercelIntegration, project_id: str) -> Optional[Dict[str, Any]]:
        project = await self._get_remote_project(integration, project_id)
        if not project:
            return None

        return {"project_id": project_id, "bindings": integration.get_bindings(by_project_id=project_id)}

    @user_authenticated
    async def post(self, integration_id: str, project_id: str) -> None:
        integration = self.get_integration(integration_id)
        project = await self.get_project(integration, project_id)
        if not project:
            raise ApiHTTPError(404, "Project not found")

        body = json.loads(self.request.body)

        workspace_id: str = body.get("workspace_id", "")
        if not workspace_id:
            raise ApiHTTPError(400, "Missing workspace_id parameter")

        tokens: Optional[List[str]] = body.get("tokens", None)
        if not tokens:
            raise ApiHTTPError(400, "Missing tokens parameter")

        user: UserAccount = self.current_user
        if not user.has_access_to(workspace_id):
            raise ApiHTTPError(404, "Workspace not found")

        workspace = User.get_by_id(workspace_id)
        if not workspace:
            raise ApiHTTPError(404, "Workspace not found")

        # List of currently bound tokens for this (project_id, workspace_id)
        bound_tokens = [
            b.token for b in integration.get_bindings(by_project_id=project_id, by_workspace_id=workspace_id)
        ]

        safe_tokens = [t.token for t in workspace.get_safe_user_tokens(user.id) if not t.is_obfuscated()]
        tokens = [t for t in tokens if t in safe_tokens and t not in bound_tokens]
        if tokens:
            integration = await VercelIntegrationService.add_bindings(integration, project_id, workspace_id, tokens)

        self.set_status(201)

    @user_authenticated
    @requires_write_access
    async def delete(self, integration_id: str, project_id: str) -> None:
        integration = self.get_integration(integration_id)
        project = await self.get_project(integration, project_id)
        if not project:
            raise ApiHTTPError(404, "Project not found")

        # List of currently bound tokens for this (project_id, workspace_id)
        bound_tokens = [b.token for b in integration.get_bindings(by_project_id=project_id)]
        if bound_tokens:
            integration = await VercelIntegrationService.remove_bindings(integration, project_id, bound_tokens)

        self.set_status(201)


class APIVercelIntegrationLinkedProjectsListHandler(APIVercelIntegrationHandlerBase):
    @user_authenticated
    async def get(self, integration_id: str) -> None:
        integration = self.get_integration(integration_id)
        next_timestamp = self.get_argument("next_timestamp", "")
        # Prefetch all Vercel projects
        all_projects, pagination = await self._fetch_remote_projects(integration, next_timestamp)

        # For use in the inner function `get_workspace()`
        workspace_cache: Dict[str, Optional[User]] = {}

        def get_workspace(id: str) -> Optional[User]:
            result: Optional[User]
            if id not in workspace_cache:
                result = User.get_by_id(id)
                workspace_cache[id] = result
            else:
                result = workspace_cache[id]
            return result

        def make_env_dict(binding: VercelIntegrationBindInfo) -> Dict[str, Any]:
            workspace = get_workspace(binding.workspace_id)
            tinfo: Optional[AccessToken] = workspace.get_token_access_info(binding.token) if workspace else None
            return {
                "workspace_id": binding.workspace_id,
                "workspace_name": workspace.name if workspace else "",
                "token_name": tinfo.name if tinfo else "",
                "token_value": binding.token,
                "token_scopes": [{"type": scope[0]} for scope in tinfo.scopes] if tinfo else [],
                "vercel_key": binding.vercel_env_key,
                "created_at": binding.created_at.isoformat(),
            }

        def make_project_dict(project: Dict[str, Any]) -> Dict[str, Any]:
            id: str = project.get("id", "")
            if not id:
                return {}

            bindings = [make_env_dict(binding) for binding in integration.get_bindings(by_project_id=id)]
            if not bindings:
                return {}

            return {
                "vercel_project_name": project.get("name", ""),
                "vercel_project_id": id,
                "vercel_created_at": datetime.fromtimestamp(float(project.get("createdAt", 0)) / 1000).isoformat(),
                "env": [make_env_dict(binding) for binding in integration.get_bindings(by_project_id=id)],
            }

        items: List[Dict[str, Any]] = []
        for prj in all_projects:
            data = make_project_dict(prj)
            if data:
                items.append(data)

        self.write_json({"data": items, "pagination": pagination})


class APIVercelIntegrationResetHandler(APIVercelIntegrationHandlerBase):
    async def get(self, user_id: str, integration_id: str) -> None:
        user = UserAccount.get_by_id(user_id)
        if not user:
            raise ApiHTTPError(404, f"UserAccount {user_id} not found")
        await VercelIntegrationService.remove_integration(user, integration_id, remove_remote=True)


class APIVercelIntegrationHandler(APIVercelIntegrationHandlerBase):
    @user_authenticated
    @requires_write_access
    async def get(self) -> None:
        user: Optional[UserAccount] = self.get_current_user()
        assert isinstance(user, UserAccount)

        access_code: str = self.get_argument("code", "")
        integration: Optional[VercelIntegration] = None
        existing = user.get_integration_info_by_type("vercel")
        if len(existing) > 0:
            integration = VercelIntegration.get_by_id(existing[0].integration_id)
            if integration and access_code:
                # Reset the current integration if we provided a new access code
                user = await VercelIntegrationService.remove_integration(user, integration.id, remove_remote=True)
                integration = None

        if not integration:
            integration = await VercelIntegrationService.get_integration_for_user(user, access_code)
            user = await UserAccounts.add_integration(user, "vercel", integration.id)

        integration = await VercelIntegrationService.get_integration_for_user(user)
        if integration.integration_phase == VercelIntegrationPhase.INSTALLING:
            integration = await VercelIntegrationService.finalize_install(integration)
        self.write_json({"id": integration.id})


def handlers():
    return [
        url(r"/v0/integrations/vercel/?", APIVercelIntegrationHandler),
        url(r"/v0/integrations/vercel/(.+)/projects/?", APIVercelIntegrationProjectListHandler),
        url(r"/v0/integrations/vercel/(.+)/projects/(.+)/?", APIVercelIntegrationProjectsHandler),
        url(r"/v0/integrations/vercel/(.+)/linked_projects/?", APIVercelIntegrationLinkedProjectsListHandler),
        url(r"/v0/integrations/vercel/unlink/?", APIVercelIntegrationLinkedProjectsListHandler),
        url(r"/integrations/vercel/(.+)/(.+)/adm-reset-speed-wins/?", APIVercelIntegrationResetHandler),
    ]
