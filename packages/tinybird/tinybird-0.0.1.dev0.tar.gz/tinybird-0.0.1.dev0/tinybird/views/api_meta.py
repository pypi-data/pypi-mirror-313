from tornado.web import url

from tinybird.ch import ch_get_version

from .base import BaseHandler, authenticated


class APIMetaBaseHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass


class APIMetaVersionHandler(APIMetaBaseHandler):
    @authenticated
    async def get(self):
        workspace = self.get_workspace_from_db()
        version = await ch_get_version(database_server=workspace.database_server)
        self.write_json({"version": version})


def handlers():
    return [
        url(r"/v0/meta/version", APIMetaVersionHandler),
    ]
