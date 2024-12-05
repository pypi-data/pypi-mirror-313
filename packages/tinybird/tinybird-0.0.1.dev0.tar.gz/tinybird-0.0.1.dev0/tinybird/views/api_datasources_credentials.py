from tinybird.ingest.external_datasources.admin import get_or_create_workspace_service_account
from tinybird.tokens import scopes
from tinybird.views.base import BaseHandler, URLMethodSpec, authenticated, with_scope


class APIDatasourcesBigQuery(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @authenticated
    @with_scope(scopes.ADMIN)
    async def get(self):
        workspace = self.get_workspace_from_db()
        account_info = await get_or_create_workspace_service_account(workspace)
        response = {"account": account_info["service_account_id"]}
        self.write_json(response)


def handlers():
    return [
        URLMethodSpec(
            "GET", r"/v0/datasources-bigquery-credentials", APIDatasourcesBigQuery
        ),  # TODO: remove once frontend migrates
        URLMethodSpec("GET", r"/v0/datasources-credentials", APIDatasourcesBigQuery),
    ]
