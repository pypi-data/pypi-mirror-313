import functools

from tinybird.data_connector import DataConnectors
from tinybird.ingest.cdk_utils import CDKUtils
from tinybird.ingest.external_datasources.admin import get_or_create_workspace_service_account
from tinybird.ingest.external_datasources.connector import InvalidGCPCredentials, UnknownCDKError, get_connector
from tinybird.ingest.external_datasources.inspection import ExternalTableDatasource, list_resources
from tinybird.limits import Limit
from tinybird.plan_limits.cdk import CDKLimits
from tinybird.tokens import scopes
from tinybird.user import User as Workspace
from tinybird.views.base import ApiHTTPError, BaseHandler, URLMethodSpec, authenticated, check_rate_limit, with_scope

SUPPORTED_CONNECTOR_TYPES = [DataConnectors.BIGQUERY]
# During testing both the admin SA & BQ environment live in the same account
# so we need to skip the project filter
GCP_PROJECT_WHITELIST = ["development-353413"]


async def _get_service_account_info(workspace: Workspace) -> str:
    account_info = await get_or_create_workspace_service_account(workspace)
    return account_info["key"]


def cdk_to_http_errors(func):
    @functools.wraps(func)
    async def inner(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except (UnknownCDKError, InvalidGCPCredentials) as err:
            raise ApiHTTPError(503, "Something went terribly wrong. Please try again later.") from err
        except NameError as err:
            raise ApiHTTPError(404, err.args[0]) from err
        except PermissionError as err:
            raise ApiHTTPError(403, err.args[0]) from err
        except ValueError as err:
            raise ApiHTTPError(400, err.args[0]) from err

    return inner


class APIListSupportedConnectorsHandler(BaseHandler):
    def check_xsrf_cookie(self, *_):
        pass

    @authenticated
    @with_scope(scopes.ADMIN)
    @check_rate_limit(Limit.api_connectors_list)
    async def get(self):
        payload = {"connectors": SUPPORTED_CONNECTOR_TYPES}
        self.write_json(payload)


class BaseExternalDatasourceInspectionHandler(BaseHandler):
    async def prepare(self):
        super().prepare()
        kind = self.path_args[0]
        gapp_credentials = await _get_service_account_info(self.current_workspace)
        env = {"GOOGLE_APPLICATION_CREDENTIALS_JSON": gapp_credentials}

        try:
            self._cdk_connector = await get_connector(kind, env)
        except NotImplementedError as err:
            raise ApiHTTPError(501, err.args[0]) from err
        except InvalidGCPCredentials as err:
            # If we get here something has gone terribly wrong and the credentials might be invalid/corrupted
            raise ApiHTTPError(503, "Something went terribly wrong. Please try again later") from err

    def on_finish(self):
        super().on_finish()
        if hasattr(self, "_cdk_connector"):
            self._cdk_connector.shutdown()


class APIListResourcesHandler(BaseExternalDatasourceInspectionHandler):
    @authenticated
    @with_scope(scopes.ADMIN)
    @cdk_to_http_errors
    @check_rate_limit(Limit.api_connectors_list)
    async def get(self, kind: str, *scope: str):
        resources = await list_resources(self._cdk_connector, scope)
        # If we're requesting the projects using bigquery we want to filter out the cdk project
        # Unless it's the dev one as we might have both bigquery & the admin account in it
        if kind == "bigquery" and not scope and CDKUtils.project_id not in GCP_PROJECT_WHITELIST:
            resources = [r for r in resources if r["value"] != CDKUtils.project_id]
        self.write_json({"items": resources})


class APIListTablesHandler(BaseExternalDatasourceInspectionHandler):
    @authenticated
    @with_scope(scopes.ADMIN)
    @cdk_to_http_errors
    @check_rate_limit(Limit.api_connectors_list)
    async def get(self, kind: str, *scope: str):
        tables = await list_resources(self._cdk_connector, scope)
        # If we're requesting the projects using bigquery we want to filter out the cdk project
        # Unless it's the dev one as we might have both bigquery & the admin account in it
        row_limit = CDKLimits.max_row_limit.get_limit_for(self.current_workspace)

        output = [
            {
                **table,
                "row_limit": row_limit,
                "row_limit_exceeded": CDKLimits.max_row_limit.has_reached_limit_in(
                    row_limit, {"rows": table["num_rows"]}
                ),
            }
            for table in tables
        ]
        self.write_json({"items": output})


class APIInspectTableHandler(BaseExternalDatasourceInspectionHandler):
    @authenticated
    @with_scope(scopes.ADMIN)
    @cdk_to_http_errors
    @check_rate_limit(Limit.api_connectors_list)
    async def get(self, _: str, *fqn: str):
        table = ExternalTableDatasource(self._cdk_connector, fqn)
        schema = await table.get_schema()
        sample = await table.get_sample()
        query = await table.get_extraction_query()
        preview_metadata = [{"name": col["name"], "type": col["recommended_type"]} for col in schema["columns"]]
        analyze_results = {
            "analysis": schema,
            "query": query,
            "preview": {"meta": preview_metadata, "data": sample},
        }
        self.write_json(analyze_results, default_serializer=str)


def handlers():
    base_path = r"/v0/connections/([^/]+)"
    return [
        URLMethodSpec("GET", "/v0/connections", APIListSupportedConnectorsHandler),
        URLMethodSpec("GET", base_path, APIListResourcesHandler),
        URLMethodSpec("GET", base_path + r"/([^/]+)", APIListResourcesHandler),
        URLMethodSpec(
            "GET",
            base_path + r"/([^/]+)" * 2,
            APIListTablesHandler,
        ),
        URLMethodSpec("GET", base_path + r"/([^/]+)" * 3, APIInspectTableHandler),
    ]
