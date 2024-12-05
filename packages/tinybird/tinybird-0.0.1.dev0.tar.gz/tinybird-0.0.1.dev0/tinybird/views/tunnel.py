import json
import logging
from urllib.parse import urlparse

from tornado.web import url

from .aiohttp_shared_session import get_shared_session
from .base import ApiHTTPError, BaseHandler


class Tunnel(BaseHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

    async def post(self):
        try:
            sentry_host = self.application.settings.get("sentry", {}).get("tunnel_dsn", None)
            known_project_id = self.application.settings.get("sentry", {}).get("tunnel_known_project_id", None)

            if sentry_host is None:
                raise Exception("Sentry host not configured")

            if known_project_id is None:
                raise Exception("Sentry project id not configured")

            envelope = self.request.body.decode("utf-8")
            piece = envelope.split("\n")[0]
            header = json.loads(piece)
            dsn = urlparse(header.get("dsn"))

            if dsn.hostname != sentry_host:
                raise Exception(f"Invalid Sentry host: {dsn.hostname}")

            project_id = dsn.path.strip("/")
            if project_id != known_project_id:
                raise Exception(f"Invalid Project ID: {project_id}")

            url = f"https://{sentry_host}/api/{project_id}/envelope/"

            session = get_shared_session()
            async with session.post(url, data=envelope.encode("utf-8")) as resp:
                await resp.content.read()
                if resp.status != 200:
                    raise Exception(
                        f"Error found trying to send the Sentry errors from the UI: {resp.status}, {await resp.text()}"
                    )

            logging.debug("Event sent to Sentry through tunnel")

        except Exception as e:
            logging.exception(e)
            raise ApiHTTPError(500)

    def check_xsrf_cookie(self):
        pass


def handlers():
    return [
        url(r"/v0/tunnel", Tunnel),
    ]
