from typing import List

from tornado.escape import json_decode
from tornado.web import url

from tinybird.playground.playground import PlaygroundNotFoundException
from tinybird.playground.playground_service import PlaygroundService
from tinybird.user import UserDoesNotExist, Users

from .base import ApiHTTPError, BaseHandler, user_authenticated


class APIPlaygroundBaseHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass


class APIPlaygroundsHandler(APIPlaygroundBaseHandler):
    @user_authenticated
    async def get(self):
        workspace_id = self.get_argument("workspace_id", None)
        semver = self.get_argument("__tb__semver", None)
        if not workspace_id:
            raise ApiHTTPError(404, "Workspace not found")

        user = self.get_user_from_db()
        playgrounds = PlaygroundService.get_playgrounds(workspace_id, user.id, semver)

        try:
            workspace = Users.get_by_id(workspace_id)
        except UserDoesNotExist:
            raise ApiHTTPError(404, "Workspace not found")

        workspace_info = workspace.get_workspace_info() or {}
        workspace_members: List[str] = [member.get("id") for member in workspace_info.get("members", []) or []]

        for playground in playgrounds:
            shared_with = playground.shared_with or []
            filtered_members = [member for member in shared_with if member in workspace_members]
            playground.shared_with = filtered_members

        self.write_json({"playgrounds": [play.to_json() for play in playgrounds]})

    @user_authenticated
    async def post(self):
        semver = self.get_argument("__tb__semver", None)
        workspace_id = self.get_argument("workspace_id", None)
        if not workspace_id:
            raise ApiHTTPError(404, "Workspace not found")

        user = self.get_user_from_db()
        data = json_decode(self.request.body) or {}
        name = data.get("name", None)
        description = data.get("description", None)
        nodes = data.get("nodes", None)

        if not name:
            raise ApiHTTPError(400, "Playground name is required")

        try:
            playground = await PlaygroundService.create_playground(
                workspace_id=workspace_id,
                user_id=user.id,
                name=name,
                description=description,
                nodes=nodes,
                semver=semver,
            )
            response = playground.to_json()
            self.write_json(response)
        except Exception as e:
            raise ApiHTTPError(400, str(e))


class APIPlaygroundHandler(APIPlaygroundBaseHandler):
    @user_authenticated
    async def get(self, playground_id):
        workspace_id = self.get_argument("workspace_id", None)
        if not workspace_id:
            raise ApiHTTPError(404, "Workspace not found")

        user = self.get_user_from_db()
        try:
            playground = PlaygroundService.get_playground(
                user.id,
                playground_id,
            )
        except PlaygroundNotFoundException:
            raise ApiHTTPError(404, "Playground not found")

        if self.get_argument("datafile", None) == "true":
            self.set_header("content-type", "text/plain")
            content = playground.generate_datafile()
            self.write(content)
            return

        self.write_json(playground.to_json())

    @user_authenticated
    async def put(self, playground_id):
        workspace_id = self.get_argument("workspace_id", None)
        if not workspace_id:
            raise ApiHTTPError(404, "Workspace not found")

        user = self.get_user_from_db()
        try:
            playground = PlaygroundService.get_playground(user.id, playground_id)
        except PlaygroundNotFoundException:
            raise ApiHTTPError(404, "Playground not found")

        try:
            playground = await PlaygroundService.update_playground(
                workspace_id=workspace_id,
                user_id=user.id,
                playground=playground,
                data=json_decode(self.request.body),
            )
        except Exception as e:
            raise ApiHTTPError(400, str(e))
        self.write_json(playground.to_json())

    @user_authenticated
    async def delete(self, playground_id):
        workspace_id = self.get_argument("workspace_id", None)
        if not workspace_id:
            raise ApiHTTPError(404, "Workspace not found")

        user = self.get_user_from_db()
        try:
            playground = PlaygroundService.get_playground(user.id, playground_id)
        except PlaygroundNotFoundException:
            raise ApiHTTPError(404, "Playground not found")

        await PlaygroundService.delete_playground(
            user_id=user.id,
            playground=playground,
        )
        self.write_json({})


class APIPlaygroundLastUpdateHandler(APIPlaygroundBaseHandler):
    @user_authenticated
    async def get(self, playground_id):
        workspace_id = self.get_argument("workspace_id", None)
        allowed_attrs = ["id", "name", "edited_by", "updated_at"]
        if not workspace_id:
            raise ApiHTTPError(404, "Workspace not found")

        user = self.get_user_from_db()
        try:
            playground = PlaygroundService.get_playground(
                user.id,
                playground_id,
            )
        except PlaygroundNotFoundException:
            raise ApiHTTPError(404, "Playground not found")

        self.write_json(playground.to_json(attrs=allowed_attrs))


def handlers():
    return [
        url(r"/v0/playgrounds/(.+)/last_update", APIPlaygroundLastUpdateHandler),
        url(r"/v0/playgrounds/(.+)", APIPlaygroundHandler),
        url(r"/v0/playgrounds/?", APIPlaygroundsHandler),
    ]
