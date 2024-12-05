from urllib.parse import quote_plus

from ..tokens import scopes
from ..user import Users
from . import template_utils
from .base import WebBaseHandler, authenticated, with_scope
from .openapi import generate_openapi_endpoints_response


class EndpointHtmlHandler(WebBaseHandler):
    @authenticated
    @with_scope(scopes.PIPES_READ)
    async def get(self, pipe_name_or_id=""):
        workspace = self.get_workspace_from_db()
        pipe = workspace.get_pipe(pipe_name_or_id)
        token = self._get_access_info()

        if not self.is_admin():
            resources = self.get_readable_resources()
            pipe = pipe if pipe and pipe.id in resources else None

        if not pipe:
            self.set_status(404)
            self.render("404.html")
            return
        if not pipe.endpoint:
            self.set_status(404)
            self.render("404.html")
            return
        if not token:
            self.set_status(404)
            self.render("404.html")
            return

        openapi_response = await generate_openapi_endpoints_response(
            self.application.settings, pipes=[pipe], workspace=workspace, token=token
        )

        params = openapi_response["paths"][f"/pipes/{pipe.name}" + ".{format}"]["get"]["parameters"]

        pipe_json = pipe.to_json()
        pipe_json["description"] = pipe_json["description"] if pipe_json["description"] else ""

        host = self.application.settings["api_host"]
        openapi_url = quote_plus(f'{host}{self.reverse_url("pipes_openapi")}?token={token.token}')
        docs_url = self.application.settings["docs_host"]

        self.render(
            "pipe_public.html",
            pipe=pipe_json,
            raw_pipe=pipe,
            params=params,
            workspace_name=workspace["name"],
            host=host,
            token=token.token,
            openapi_url=openapi_url,
            docs_url=docs_url,
            markdown=template_utils.to_md,
        )


class EndpointsHtmlHandler(WebBaseHandler):
    @authenticated
    @with_scope(scopes.PIPES_READ)
    async def get(self, id=""):
        workspace = self.get_workspace_from_db()
        if not workspace:
            self.set_status(404)
            self.render("404.html")
            return
        pipes = Users.get_pipes(workspace)
        filtered_pipes = [t for t in pipes if t.endpoint]

        if not self.is_admin():
            resources = self.get_readable_resources()
            filtered_pipes = [pipe for pipe in filtered_pipes if pipe.id in resources]

        self.render(
            "pipes_public.html",
            pipes=filtered_pipes,
            workspace_name=workspace["name"],
            token=self.get_workspace_token_from_request_or_cookie().decode(),
            markdown=template_utils.to_md,
        )
