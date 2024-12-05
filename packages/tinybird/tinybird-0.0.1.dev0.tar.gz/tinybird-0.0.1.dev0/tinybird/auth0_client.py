import json
import logging
from asyncio import Lock
from typing import Any, Dict, List, Optional, Union, cast
from urllib.parse import urlencode

from tornado.httpclient import AsyncHTTPClient

from tinybird.views.aiohttp_shared_session import get_shared_session


class Auth0Client:
    def __init__(self, settings: Dict[str, Any]) -> None:
        self._token_lock = Lock()
        self._settings: Dict[str, Any] = dict(settings)
        self._enabled: bool = self._settings.get("enabled", True)
        self._token: Optional[str] = None
        self._http_client: AsyncHTTPClient = AsyncHTTPClient(defaults={"request_timeout": 1000.0})

    async def get_users_by_email(self, email: str) -> List[Dict[str, Any]]:
        """https://auth0.com/docs/api/management/v2/#!/Users_By_Email/get_users_by_email"""
        if not self._enabled:
            return []

        logging.info(f"Getting Auth0 users for {email}...")

        try:
            query_args = urlencode({"email": email})
            response = await self._fetch(f"/api/v2/users-by-email?{query_args}", method="GET")
            obj: Union[List[Dict[str, Any]], Dict[str, Any]] = json.loads(response)
            if "error" not in obj:
                return cast(List[Dict[str, Any]], obj)

            logging.exception(f"> Error retrieving Auth0 users with email '{email}': {response}")

        except Exception as e:
            logging.exception(f"> Error retrieving Auth0 users with email '{email}': {e}")

        return []

    async def get_connection_by_domain(self, email: str) -> Optional[str]:
        """https://auth0.com/docs/api/management/v2/#!/connections/get-connections"""
        if not self._enabled:
            return None
        if not email:
            return None

        logging.info(f"Getting Auth0 connection for {email}...")

        try:
            domain = email.split("@")[1]
            response = await self._fetch("/api/v2/connections", method="GET")
            obj = json.loads(response)

            if "error" not in obj:
                for item in obj:
                    if "domain_aliases" in item["options"] and domain in item["options"]["domain_aliases"]:
                        return item["name"]
                return None

            logging.exception(f"> Error retrieving Auth0 connections with email '{email}': {response}")

        except Exception as e:
            logging.exception(f"> Error retrieving Auth0 connections with email '{email}': {e}")

        return None

    async def _get_or_fetch_token(self, force_fetch: bool = False) -> Optional[str]:
        """Requests (and caches) a new token for accesing Auth0 API."""
        if self._token and not force_fetch:
            return self._token
        await self._token_lock.acquire()

        logging.info("Refreshing Auth0 API token...")

        data = {
            "client_id": self._settings["client_id"],
            "client_secret": self._settings["client_secret"],
            "audience": f"https://{self._settings['domain']}/api/v2/",
            "grant_type": "client_credentials",
        }

        response: Optional[Dict[str, Any]] = None

        try:
            response = json.loads(await self._fetch("/oauth/token", data=data, insert_token=False))
            assert isinstance(response, dict)
            self._token = response["access_token"]
            logging.info("> Success.")
        except Exception as e:
            self._token = None
            logging.exception(f"> Failed refreshing Auth0 token: {e} ({str(response)})")
        finally:
            self._token_lock.release()

        return self._token

    async def _fetch(
        self,
        path: str,
        data: Any = None,
        headers: Optional[Dict[str, Any]] = None,
        method: str = "POST",
        insert_token: bool = True,
    ) -> str:
        """Fetchs an API endpoint and returns the resulting HTTPResponse.
        It tries to gracefully manage the token acquisition/refresh cycle.
        """

        url = f"https://{self._settings['domain']}{path}"
        request_headers = {"content-type": "application/json"}

        if insert_token:
            token = await self._get_or_fetch_token()
            request_headers["authorization"] = f"Bearer {token}"

        if headers:
            request_headers.update(headers)

        session = get_shared_session()

        async def do_request():
            logging.info(f"> Fetching {url}...")
            return await session.request(url=url, method=method, json=data, headers=request_headers)

        result = await do_request()

        # Need to refresh the token?
        if (result.status == 401 or result.status == 403) and insert_token:
            logging.info("> Forbidden. Requesting a new token...")
            token = await self._get_or_fetch_token(force_fetch=True)
            if token:
                request_headers["authorization"] = f"Bearer {token}"
                result = await do_request()
            else:
                logging.warning("> Can't refresh token")

        return (await result.content.read()).decode()
