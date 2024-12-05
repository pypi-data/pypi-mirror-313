from typing import Optional

import tornado.auth
import tornado.web
from tornado.web import url

from tinybird.limits import Limit
from tinybird.user import CreateSecretError, SecretNotFound
from tinybird.user import Users as Workspaces
from tinybird.views.base import (
    ApiHTTPError,
    BaseHandler,
    _calculate_edited_by,
    authenticated,
    check_rate_limit,
    with_scope_admin,
)


class APIVariablesHandlerBase(BaseHandler):
    def check_xsrf_cookie(self) -> None:
        pass


def validate_size(value: str):
    value_bytes = value.encode("utf-8")
    value_kb_size = len(value_bytes) / 1024

    max_size_kb = 8
    if value_kb_size > max_size_kb:
        raise ApiHTTPError(400, "Variable maximum size is 8KB")


def validate_type(value: str):
    if value not in ["secret"]:
        raise ApiHTTPError(400, "Supported variable types are: secret")


class APIVariablesHandler(APIVariablesHandlerBase):
    @authenticated
    @with_scope_admin
    @check_rate_limit(Limit.api_variables_list)
    async def get(self) -> None:
        workspace = self.get_workspace_from_db()
        if not workspace:
            raise ApiHTTPError(404, "Not found")

        secrets = [secret.to_json() for secret in workspace.get_secrets()]

        self.write_json({"variables": secrets})

    @authenticated
    @with_scope_admin
    @check_rate_limit(Limit.api_variables)
    async def post(self) -> None:
        try:
            workspace = self.get_workspace_from_db()
            if not workspace:
                raise ApiHTTPError(404, "Not found")

            if workspace.is_branch_or_release_from_branch:
                raise ApiHTTPError(
                    403,
                    "Variables cannot be created in branches. Create the Variable in the main Workspace and it'll be inherited in branches.",
                )

            edited_by = _calculate_edited_by(self._get_access_info())

            name: str = self.get_argument("name")
            value: str = self.get_argument("value", None)
            _type: str = self.get_argument("type", "secret")

            if not value:
                raise ApiHTTPError(400, "missing value")

            if not name:
                raise ApiHTTPError(400, "missing name")

            validate_size(value)
            validate_type(_type)

            secret = await Workspaces.add_secret(workspace, name, value, edited_by)
            self.write_json(secret.to_json())
        except CreateSecretError as e:
            raise ApiHTTPError(400, str(e))


class APIVariableHandler(APIVariablesHandlerBase):
    @authenticated
    @with_scope_admin
    @check_rate_limit(Limit.api_variables)
    async def delete(self, secret_name: str) -> None:
        workspace = self.get_workspace_from_db()
        if not workspace:
            raise ApiHTTPError(404, "Not found")

        if workspace.is_branch_or_release_from_branch:
            raise ApiHTTPError(
                403, "Variables cannot be deleted in branches. Delete the Variable in the main Workspace."
            )

        ok = await Workspaces.drop_secret_async(workspace, secret_name)

        if not ok:
            raise ApiHTTPError(404, "Variable not found")
        self.write_json({"ok": True})

    @authenticated
    @with_scope_admin
    @check_rate_limit(Limit.api_variables_list)
    async def get(self, secret_name: str) -> None:
        workspace = self.get_workspace_from_db()
        if not workspace:
            raise ApiHTTPError(404, "Not found")

        secret = workspace.get_secret(secret_name)
        if not secret:
            raise ApiHTTPError(404, "Not found")

        self.write_json(secret.to_json())

    @authenticated
    @with_scope_admin
    @check_rate_limit(Limit.api_variables)
    @tornado.web.removeslash
    async def put(self, secret_name: str) -> None:
        try:
            workspace = self.get_workspace_from_db()
            if not workspace:
                raise ApiHTTPError(404, "Not found")

            if workspace.is_branch_or_release_from_branch:
                raise ApiHTTPError(
                    403,
                    "Variables cannot be updated in branches. Update the Variable in the main Workspace and it'll be inherited in branches.",
                )

            _type: Optional[str] = self.get_argument("type", None)
            if _type is not None:
                raise ApiHTTPError(400, "Variable type cannot be changed")

            value: Optional[str] = self.get_argument("value", None)
            if not value:
                raise ApiHTTPError(400, "missing value")

            if not workspace.get_secret(secret_name):
                raise ApiHTTPError(404, "Variable not found")

            validate_size(value)
            edited_by = _calculate_edited_by(self._get_access_info())

            secret = await Workspaces.update_secret(workspace, secret_name, value, edited_by)

            self.write_json(secret.to_json())
        except SecretNotFound as e:
            raise ApiHTTPError(404, str(e))


def handlers():
    return [
        url(r"/v0/variables/?", APIVariablesHandler),
        url(r"/v0/variables/(.+)", APIVariableHandler),
    ]
