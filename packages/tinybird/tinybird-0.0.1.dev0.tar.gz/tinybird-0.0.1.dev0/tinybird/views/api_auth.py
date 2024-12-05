from typing import Optional
from uuid import uuid4

from tornado.web import url

from tinybird.token_scope import scopes
from tinybird.useraccounts_service import UserAccountsService

from ..user import User as Workspace
from ..user import UserAccount, UserAccounts
from ..user import Users as Workspaces
from .base import ApiHTTPError, BaseHandler


async def get_tokens(user: UserAccount) -> list[str | None]:
    async def get_first_available_workspace():
        try:
            workspaces = await user.get_workspaces(with_environments=False)
            return workspaces[0]["id"] if len(workspaces) > 0 else None
        except Exception:
            return None

    user_token = user.get_token_for_scope(scopes.AUTH)
    workspace: Optional[Workspace] = None
    workspace_token: Optional[str] = None
    workspace_id_or_name: Optional[str] = await get_first_available_workspace()
    workspace_id: Optional[str] = None
    workspace_name: Optional[str] = None

    if workspace_id_or_name:
        workspace = Workspaces.get_by_id_or_name(workspace_id_or_name)

    if workspace:
        workspace_token = workspace.get_workspace_access_token(user.id)
        workspace_id = workspace.id
        workspace_name = workspace.name

    return [workspace_token, user_token, workspace_id, workspace_name]


class APIAuthHandlerBase(BaseHandler):
    def check_xsrf_cookie(self) -> None:
        pass


class APIAuthHandler(APIAuthHandlerBase):
    def get(self) -> None:
        """Checks if a token is valid for authentication purposes"""

        is_valid: bool = False
        is_user: bool = False

        # First we try to identify the workspace. If found, the token needs to be ADMIN or ADMIN_USER
        # to be valid

        try:
            workspace = self.get_current_workspace()
            if workspace and workspace.is_active and not workspace.deleted and not workspace.is_branch:
                token = self._get_access_info()
                if token:
                    is_valid = token.has_scope(scopes.ADMIN) or token.has_scope(scopes.ADMIN_USER)
                    is_user = False
        except Exception:
            pass

        try:
            user = self.get_current_user()
            if user and user.is_active:
                is_valid = True
                is_user = True
        except Exception:
            pass

        self.write_json({"is_valid": is_valid, "is_user": is_user})


class APIAuthFakeLoginHandler(BaseHandler):
    async def get(self) -> None:
        email = self.get_argument("email", "")

        try:
            user = UserAccounts.get_by_email(email)
            workspace_token, user_token, workspace_id, workspace_name = await get_tokens(user)

            self.write_json(
                {
                    "workspace_token": workspace_token,
                    "user_token": user_token,
                    "workspace_id": workspace_id,
                    "workspace_name": workspace_name,
                }
            )
        except Exception:
            raise ApiHTTPError(401, "Unauthorized.")


class APIAuthFakeSignupHandler(BaseHandler):
    async def get(self) -> None:
        email = self.get_argument("email", "")

        try:
            user = await UserAccountsService.register_user(
                email=email, password=str(uuid4()), confirmed_account=True, notify_user=False
            )
            workspace_token, user_token, workspace_id, workspace_name = await get_tokens(user)

            self.write_json(
                {
                    "workspace_token": workspace_token,
                    "user_token": user_token,
                    "workspace_id": workspace_id,
                    "workspace_name": workspace_name,
                }
            )
        except Exception:
            raise ApiHTTPError(401, "Unauthorized.")


def handlers():
    return [
        url(r"/v0/auth", APIAuthHandler),
    ]
