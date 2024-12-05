from tornado.escape import json_decode
from tornado.web import url

from tinybird.user import Users as Workspaces
from tinybird.views.api_errors.tags import TagClientErrorBadRequest, TagClientErrorNotFound

from .base import ApiHTTPError, BaseHandler, authenticated, requires_write_access


class APITagBaseHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass


class APITagsHandler(APITagBaseHandler):
    @authenticated
    async def get(self):
        workspace = self.get_workspace_from_db()
        main_workspace = workspace.get_main_workspace()
        self.write_json({"tags": [tag.to_json() for tag in main_workspace.get_tags()]})

    @authenticated
    @requires_write_access
    async def post(self):
        workspace = self.get_workspace_from_db()
        main_workspace = workspace.get_main_workspace()
        data = json_decode(self.request.body) or {}
        name = data.get("name", None)
        resources = data.get("resources", [])

        if not name:
            raise ApiHTTPError.from_request_error(TagClientErrorBadRequest.name_is_required())

        if main_workspace.get_tag(name):
            raise ApiHTTPError.from_request_error(TagClientErrorBadRequest.name_already_taken(name=name))

        try:
            tag = await Workspaces.add_tag(main_workspace, name, resources)
            self.write_json(tag.to_json())
        except Exception as e:
            raise ApiHTTPError(400, str(e))


class APITagHandler(APITagBaseHandler):
    @authenticated
    @requires_write_access
    async def put(self, tag_id_or_name):
        body = json_decode(self.request.body) or {}
        workspace = self.get_workspace_from_db()
        main_workspace = workspace.get_main_workspace()
        tag = main_workspace.get_tag(tag_id_or_name)

        if not tag:
            raise ApiHTTPError.from_request_error(TagClientErrorNotFound.no_tag(name=tag_id_or_name))

        name = body.get("name", None)

        if name is not None:
            if len(name) == 0:
                raise ApiHTTPError.from_request_error(TagClientErrorBadRequest.name_is_required())
            if main_workspace.get_tag(name):
                raise ApiHTTPError.from_request_error(TagClientErrorBadRequest.name_already_taken(name=name))

        resources = body.get("resources", None)

        if resources is not None and not isinstance(resources, list):
            raise ApiHTTPError.from_request_error(TagClientErrorBadRequest.resources_must_be_list())

        try:
            tag = await Workspaces.update_tag(main_workspace, tag_id_or_name, name, resources)
            self.write_json(tag.to_json())
        except Exception as e:
            raise ApiHTTPError(400, str(e))

    @authenticated
    @requires_write_access
    async def delete(self, tag_id_or_name):
        workspace = self.get_workspace_from_db()
        main_workspace = workspace.get_main_workspace()
        tag = main_workspace.get_tag(tag_id_or_name)

        if not tag:
            raise ApiHTTPError.from_request_error(TagClientErrorNotFound.no_tag(name=tag_id_or_name))
        try:
            await Workspaces.drop_tag_async(main_workspace, tag_id_or_name)
            self.set_status(204)
        except Exception as e:
            raise ApiHTTPError(400, str(e))


def handlers():
    return [
        url(r"/v0/tags/(.+)", APITagHandler),
        url(r"/v0/tags/?", APITagsHandler),
    ]
