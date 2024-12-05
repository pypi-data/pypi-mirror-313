from tornado.web import url

from tinybird.useraccounts_service import UserAccountsService
from tinybird.views.base import ApiHTTPError

from .base import BaseHandler


class APIAuthConnectionHandler(BaseHandler):
    async def get(self):
        email = self.get_argument("email", None)

        try:
            connection = await UserAccountsService.get_auth_connection_by_email(email)
            self.write_json({"connection": connection})

        except Exception as e:
            raise ApiHTTPError(400, str(e))


def handlers():
    return [
        url(r"/v0/auth_connection/?", APIAuthConnectionHandler),
    ]
