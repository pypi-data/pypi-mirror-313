import json
import logging

import tornado

from ..ch import HTTPClient
from ..sql_template import SQLTemplateCustomError, SQLTemplateException, TemplateExecutionResults
from ..sql_toolset import sql_get_used_tables
from ..tokens import scopes
from ..user import Users, public
from .base import ApiHTTPError, BaseHandler, authenticated
from .utils import validate_sql_parameter


class DocsClientHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @tornado.web.authenticated
    def get(self):
        api_host = self.application.settings["api_host"]
        docs_host = self.application.settings["docs_host"]

        # check host header so we avoid XSS
        referrer = self.request.headers.get("Referer", "")
        if not referrer.startswith(docs_host):
            raise ApiHTTPError(403)

        # allow localhost:8000 to work in development mode
        self.set_header("Access-Control-Allow-Origin", "http://localhost:8001")

        u = self.get_workspace_from_db()
        self.write(
            """
        tinybird.HOST = '%(host)s';
        window.tinyb = tinybird('%(token)s')
        """
            % {"host": api_host, "token": Users.get_token_for_scope(u, scopes.ADMIN_USER)}
        )


class SnippetQueryHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    async def get(self):
        cdn_host = self.application.settings["cdn_host"]
        api_host = self.application.settings["api_host"]
        docs_host = self.application.settings["docs_host"]
        tinybird_js_version = self.application.settings["tinybird_js_version"]
        workspace_name = ""

        # check host header so we avoid XSS
        referrer = self.request.headers.get("Referer", "http://localhost:8000")
        if not referrer.startswith(docs_host):
            raise ApiHTTPError(403)

        # allow localhost:8000 to work in development mode
        self.set_header("Access-Control-Allow-Origin", "http://localhost:8000")

        # options
        code = self.get_argument("code")

        jwt, jwt_append, jwt_import, pipe_name, column = "", "", "", "", ""

        if code.find("<pipe>") > -1 or code.find("<token>") > -1:
            pipe = None

            u = self.get_workspace_from_db()

            if u:
                workspace_name = u["name"]
                datasources = Users.get_datasources(u)

                for ds in datasources:
                    used_bys = Users.get_datasource_used_by(u, ds)
                    published_pipes = [p for p in used_bys if p.is_published()]
                    if len(published_pipes) > 0:
                        pipe = published_pipes[0]
                        break

                if pipe:
                    try:
                        template_execution_results = TemplateExecutionResults()
                        readable_resources = None if self.is_admin() else self.get_readable_resources()
                        use_pipe_nodes = self.is_admin()
                        allow_direct_access_to_service_datasources_replacements = self.is_admin() or self.has_scope(
                            scopes.PIPES_CREATE
                        )
                        access_info = self._get_access_info()
                        assert access_info is not None
                        filters = access_info.get_filters()
                        q = f"select * from {pipe.name} limit 0 FORMAT JSON"
                        q, _ = await u.replace_tables_async(
                            q,
                            readable_resources=readable_resources,
                            pipe=pipe,
                            filters=filters,
                            use_pipe_nodes=use_pipe_nodes,
                            variables={},
                            template_execution_results=template_execution_results,
                            check_functions=True,
                            allow_direct_access_to_service_datasources_replacements=allow_direct_access_to_service_datasources_replacements,
                        )
                        client = HTTPClient(u["database_server"], database=u["database"])
                        _, body = await client.query(q)
                        column = json.loads(body)["meta"][0]["name"]
                    except (SQLTemplateException, SQLTemplateCustomError, ValueError) as e:
                        logging.warning(f"snippet sql template exception: {str(e)}")
                        pipe = None
                    except Exception as ex:
                        logging.exception(f"failed to query selected pipe: {ex}")
                        pipe = None  # use public user pipe

            if not pipe:
                u = public.get_public_user()
                workspace_name = "internal account"
                pipe = Users.get_pipe(u, "nyc_taxi_pipe")
                column = "passenger_count"

            if not pipe:
                raise ApiHTTPError(422, "Could not find pipe for example")

            pipe_name = pipe.name

            tokens = Users.get_tokens_for_resource(u, pipe.id, scopes.PIPES_READ)
            if tokens:
                jwt = tokens[0]
            else:
                raise ApiHTTPError(403, "Could not find valid token for snippet pipe")

        u = self.get_workspace_from_db()
        if code.find("<import_token>") > -1 and u:
            workspace_name = u["name"]
            jwt_import = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE) or ""
        else:
            jwt_import = "<DATASOURCES:CREATE token>"

        # replace pipe, token and some javascript escaping
        code = (
            code.replace("<pipe>", pipe_name)
            .replace("<token>", jwt)
            .replace("<jwt_append>", jwt_append)
            .replace("<import_token>", jwt_import)
            .replace("<column>", column)
            .replace("`", "\\`")
            .replace("${", "\\${")
        )

        self.render(
            "snippets/js_iframe.html",
            js=code,
            js_json_escaped=json.dumps(code),
            username=workspace_name,
            id=self.get_argument("id"),
            cdn_host=cdn_host,
            api_host=api_host,
            pipe=pipe_name,
            column="timestamp",
            jwt_read=jwt,
            jwt_import=jwt_import,
            jwt_append=jwt_append,
            tinybird_js_version=tinybird_js_version,
        )


class ExamplesQueryHandler(BaseHandler):
    # disable xsrf in api calls
    def check_xsrf_cookie(self):
        pass

    @authenticated
    def get(self, kind):
        cdn_host = self.application.settings["cdn_host"]
        api_host = self.application.settings["api_host"]
        tinybird_js_version = self.application.settings["tinybird_js_version"]
        token = self.get_argument("token", None, True)
        q = self.get_argument("q", None, True)
        validate_sql_parameter(q)
        pipe_name = self.get_argument("pipe", None, True)
        response_format = self.get_argument("format", "json", True)
        semver = self.get_argument("__tb__semver", None)
        params = []

        if not q and not pipe_name:
            raise ApiHTTPError(400, "argument q or pipe are required")

        u = self.get_workspace_from_db()
        if not pipe_name:
            # get tokens for the table
            tables = sql_get_used_tables(q)
            if len(tables) > 1:
                raise ApiHTTPError(400, "more than one table is not supported")
            if not len(tables[0][1]):
                raise ApiHTTPError(400, "no table found")
            pipe = Users.get_pipe(u, tables[0][1])
        else:
            pipe = Users.get_pipe(u, pipe_name)
            if pipe:
                params = [p for p in pipe.get_params()]
                for p in params:
                    p["default"] = self.get_argument(p["name"], p.get("default", None), True)
                params = [p for p in params if p["default"]]
        if not pipe:
            raise ApiHTTPError(404, f"pipe {pipe_name} not found")

        if not token:
            jwt_read = Users.get_tokens_for_resource(u, pipe.id, scopes.PIPES_READ)
            if not jwt_read:
                raise ApiHTTPError(
                    400, f"pipe {pipe_name} does not have read tokens. Add a new token with PIPES:READ scope"
                )

        self.set_header("content-type", "text/plain")
        self.render(
            "snippets/query." + kind,
            sql=q.replace("`", "\\`"),
            pipe=pipe_name,
            jwt_read=token if token else jwt_read[0],
            cdn_host=cdn_host,
            params=params,
            format=response_format,
            api_host=api_host,
            tinybird_js_version=tinybird_js_version,
            semver=semver,
        )
