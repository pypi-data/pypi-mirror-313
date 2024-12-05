import logging
from enum import Enum
from typing import Dict, Optional, Tuple, cast
from urllib.parse import urlencode

from opentracing import Span, Tracer
from tornado.httputil import url_concat

from ..tokens import scopes
from ..user import User, UserAccount, UserAccountDoesNotExist, UserAccounts
from .aiohttp_shared_session import get_shared_session
from .base import BaseHandler, cookie_domain
from .mailgun import MailgunService

AUTH_LOGIN_COOKIE_NAME = "login"
AUTH_LOGIN_SESSION_COOKIE_NAME = "login_session"


def base_login(
    request: BaseHandler, user_account: UserAccount, workspace: Optional[User] = None, region_name: Optional[str] = None
) -> None:
    request.require_setting("jwt_secret", "secure jwt")
    request.clear_cookie("workspace_token")
    request.clear_cookie("token")

    domain = cookie_domain(request)
    is_https = request.application.settings.get("host", "").startswith("https")

    if user_account:
        user_token = user_account.get_token_for_scope(scopes.AUTH)
        if user_token:
            request.set_secure_cookie("token", user_token, domain=domain, secure=is_https, httponly=True)

    if workspace:
        workspace_token = workspace.get_unique_token_for_resource(user_account.id, scopes.ADMIN_USER)

        if workspace_token:
            request.set_secure_cookie("workspace_token", workspace_token, domain=domain, secure=is_https, httponly=True)

    if region_name:
        request.set_secure_cookie("region", region_name, domain=domain, secure=is_https, httponly=True)


def add_auth0_login_cookie(request: BaseHandler) -> None:
    domain = cookie_domain(request)
    request.set_cookie(AUTH_LOGIN_COOKIE_NAME, "auth0", domain=domain, secure=True)


def add_auth0_session_cookie(request: BaseHandler, refresh_token: str) -> None:
    domain = cookie_domain(request)
    is_https = request.application.settings.get("host", "").startswith("https")
    request.set_secure_cookie(
        AUTH_LOGIN_SESSION_COOKIE_NAME, refresh_token, domain=domain, secure=is_https, httponly=True
    )


class LoginHandler(BaseHandler):
    def get(self) -> None:
        current_region = self.get_current_region()
        region = self.get_secure_cookie("region")
        region_name = region.decode() if region else None
        region_config = {}
        error = self.get_argument("error", None)

        if region_name and current_region and region_name != current_region:
            region_config = self.get_region_config(region_name)

        if "host" in region_config:
            try:
                self.redirect(region_config["host"])
                return
            except Exception as e:
                logging.exception(e)
                self.clear_cookie("region")

        self.render(
            "login.html", github_login=self.application.settings.get("github_oauth")["id"], error=error, email=""
        )

    def post(self) -> None:
        email = self.get_argument("email", "")
        if not email:
            self.render(
                "login.html",
                github_login=self.application.settings.get("github_oauth")["id"],
                error="Email is mandatory",
                email=email,
            )
            return

        password = self.get_argument("password", "")
        if not password:
            self.render(
                "login.html",
                github_login=self.application.settings.get("github_oauth")["id"],
                error="Invalid credentials",
                email=email,
            )
            return

        try:
            user_account = UserAccounts.login(email, password)
        except UserAccountDoesNotExist:
            user_account = None

        if not user_account:
            self.render(
                "login.html",
                github_login=self.application.settings.get("github_oauth")["id"],
                error="Invalid credentials",
                email=email,
            )
            return

        tracer: Tracer = self.application.settings["opentracing_tracing"].tracer
        active_span: Optional[Span] = tracer.active_span
        if active_span:
            active_span.set_tag("user", user_account.id)
            active_span.set_tag("user_email", user_account.email)

        region_name = self.get_current_region()
        base_login(self, user_account, region_name=region_name)
        self.clear_cookie("next_url")
        self.redirect("/")


class SignupHandler(BaseHandler):
    def get(self) -> None:
        if self.application.settings.get("confirmed_account", True) is True:
            args = {"action": "signup"}
            referrer = self.get_argument("referrer", False)
            if referrer:
                args["referrer"] = referrer

            url = f"{self.reverse_url('login')}?{urlencode(args)}"
            self.redirect(url)
        else:
            self.render("404.html")


class UserViewBase(BaseHandler):
    def __init__(self, application, request, **kwargs):
        BaseHandler.__init__(self, application, request, **kwargs)
        self.mailgun_service = MailgunService(self.application.settings)


class LoginErrors(Enum):
    ACCESS_DENIED = "access_denied"
    CONNECTION_NOT_ALLOWED = "connection_not_allowed"


class LoginErrorHandler(BaseHandler):
    def get(self) -> None:
        self.clear_all_cookies()

        error = self.get_argument("error", None)
        filtered_error = "unknown"
        try:
            filtered_error = LoginErrors(error).value
        except ValueError:
            pass

        self.render("login_error.html", error=filtered_error)


class LogoutHandler(BaseHandler):
    def get(self) -> None:
        self.clear_cookie("token", domain=cookie_domain(self))
        self.clear_cookie("workspace_token", domain=cookie_domain(self))
        self.clear_cookie("region", domain=cookie_domain(self))
        self.clear_cookie(AUTH_LOGIN_SESSION_COOKIE_NAME, domain=cookie_domain(self))

        auth0_used = self.get_cookie(AUTH_LOGIN_COOKIE_NAME)

        if not auth0_used:
            self.redirect("/")
        else:
            self.clear_cookie(AUTH_LOGIN_COOKIE_NAME, domain=cookie_domain(self))

            auth0_config = self.settings.get("auth0_oauth", None)

            if not auth0_config:
                self.redirect("/")
                return

            args = {"client_id": auth0_config["client_id"], "returnTo": "%s/" % self.settings["host"]}
            self.redirect(url_concat(f'https://{auth0_config["domain"]}/v2/logout', args))


class CheckSessionHandler(BaseHandler):
    def check_xsrf_cookie(self) -> None:
        pass

    async def _async_request(
        self, url: str, params: Dict[str, str], headers: Dict[str, str]
    ) -> Tuple[int, Dict[str, str]]:
        session = get_shared_session()
        async with session.post(url, data=params, headers=headers) as resp:
            response = await resp.json()
            return resp.status, cast(Dict[str, str], response)

    async def _call_auth0_refresh_token(self, refresh_token: str) -> Tuple[int, Dict[str, str]]:
        auth0_config = self.settings.get("auth0_oauth", None)
        url = f'https://{auth0_config["domain"]}/oauth/token'
        params = {
            "grant_type": "refresh_token",
            "client_id": auth0_config["client_id"],
            "client_secret": auth0_config["client_secret"],
            "refresh_token": refresh_token,
            "scope": "profile email openid",
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        return await self._async_request(url, params, headers)

    async def get(self) -> None:
        refresh_token = self.get_secure_cookie(AUTH_LOGIN_SESSION_COOKIE_NAME)
        if refresh_token:
            refresh_token = refresh_token.decode()

        if not refresh_token:
            self.set_status(400)
            return

        try:
            status_code, response_content = await self._call_auth0_refresh_token(refresh_token)
            if status_code == 200:
                if "access_token" in response_content:
                    self.set_status(200)
                    return
                else:
                    raise Exception(
                        "check_session error: Auth0 returned 200 but the access token is not in the response"
                    )

            if status_code == 403 and response_content["error"] == "invalid_grant":
                self.set_status(401)
                return

            elif (
                status_code == 500
                and response_content["error"] == "access_denied"
                and response_content["error_description"] == "connection_not_allowed"
            ):
                logging.error(
                    "User logged out because of `connection_not_allowed`: This should only happen a few"
                    "times once a domain is limited to only use a single connection, but tracking it as"
                    "error in case it happens in other situations."
                )
                self.set_status(401)
                return
            else:
                for key in response_content:
                    if isinstance(response_content[key], str):
                        response_content[key] = response_content[key][:100]
                raise Exception("check_session error: ", status_code, response_content)
        except Exception as e:
            # In case of error, log the problem and return 200. That way we will avoid logging out a user if
            # the error is unrelated to its status.
            logging.exception(e)
            self.set_status(201)
            return
