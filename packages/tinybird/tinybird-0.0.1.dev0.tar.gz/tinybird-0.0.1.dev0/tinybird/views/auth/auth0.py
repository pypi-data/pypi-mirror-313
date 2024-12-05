import json
import logging
from typing import Optional
from urllib.parse import quote, urlencode

import tornado.auth
from tornado.httputil import url_concat

from tinybird.user import UserAccounts
from tinybird.views.auth.oauth_base import OauthBase
from tinybird.views.login import LoginErrors, add_auth0_login_cookie, add_auth0_session_cookie, base_login

from ..base import get_workspace_to_redirect


class Auth0OAuth2LoginHandler(OauthBase, tornado.auth.OAuth2Mixin):
    _OAUTH_AUTHORIZE_URL = ""
    _OAUTH_ACCESS_TOKEN_URL = ""

    async def get(self) -> None:
        auth0_config = self.settings.get("auth0_oauth", None)

        if not auth0_config:
            self.set_status(404)
            self.render("404.html")
            return

        Auth0OAuth2LoginHandler._OAUTH_AUTHORIZE_URL = f'https://{auth0_config["domain"]}/authorize'
        Auth0OAuth2LoginHandler._OAUTH_ACCESS_TOKEN_URL = f'https://{auth0_config["domain"]}/oauth/token'

        redirect_uri = "%s/login" % self.settings["host"]

        if self.get_argument("error", False):
            error = self.get_argument("error")
            error_description = self.get_argument("error_description", None)

            if error == "unauthorized":
                self.show_login_error(LoginErrors.ACCESS_DENIED)
                return
            elif error == "access_denied" and error_description == "connection_not_allowed":
                self.show_login_error(LoginErrors.CONNECTION_NOT_ALLOWED)
                return
            else:
                logging.exception(f"Failed to login using Auth0: {error}, {error_description}")
                self.show_login_error()
                return

        if self.get_argument("code", False):
            http_client = self.get_auth_http_client()

            params = {
                "grant_type": "authorization_code",
                "client_id": auth0_config["client_id"],
                "client_secret": auth0_config["client_secret"],
                "code": self.get_argument("code", False),
                "redirect_uri": redirect_uri,
            }

            code_validation_response = await http_client.fetch(
                self._OAUTH_ACCESS_TOKEN_URL,
                method="POST",
                headers={"content-type": "application/x-www-form-urlencoded;charset=utf-8"},
                body=urlencode(params).encode("utf-8"),
            )

            code_validation_json = json.loads(code_validation_response.body)
            if code_validation_response.code != 200 or "error" in code_validation_json:
                logging.exception(f"Error validating the Auth0' code: {code_validation_json}")
                self.show_login_error()
                return

            access_token = code_validation_json["access_token"]

            user_info_response = await http_client.fetch(
                f'https://{auth0_config["domain"]}/userinfo', headers={"Authorization": f"Bearer {access_token}"}
            )

            if user_info_response.code != 200:
                logging.exception(f"Error fetching user info: {user_info_response.code}{user_info_response.body}")
                self.show_login_error()
                return

            user = json.loads(user_info_response.body)

            if "email_verified" in user and not user["email_verified"]:
                self.redirect(f'{self.application.settings["commercial_host"]}/waiting?{user["email"]}')
                return

            add_auth0_login_cookie(self)
            add_auth0_session_cookie(self, code_validation_json["refresh_token"])

            u = await self.get_or_register_user_and_refresh_data(user)
            region_name = self.get_current_region()
            workspaces = await u.get_workspaces()
            workspace = get_workspace_to_redirect(self, workspaces, None)

            base_login(self, u, workspace=workspace, region_name=region_name)

            redirect_url = self.reverse_url("workspace_dashboard", u.id)
            if workspace:
                redirect_url = self.reverse_url("workspace_dashboard", workspace.id)

            next_url = self.get_cookie("next_url", "")
            if UserAccounts.confirmed_account(u) or "/invite" in next_url:
                self.clear_cookie("next_url")
                self.clear_cookie("referrer")
                self.redirect(next_url or redirect_url)
            else:
                self.show_login_error(LoginErrors.ACCESS_DENIED)
                return

        else:
            next_url = self.get_argument("next_url", None) or self.get_argument("next", None)
            if next_url:
                self.set_cookie("next_url", next_url)

            if self.get_argument("referrer", False):
                referrer = self.get_argument("referrer")
                self.set_cookie("referrer", quote(referrer, safe=""))
            extra_params = {"approval_prompt": "auto"}

            # This is how we tell Auth0 to land into the signup page
            if self.get_argument("action", "login") == "signup":
                extra_params["screen_hint"] = "signup"

            await self.authorize_redirect(
                redirect_uri=redirect_uri,
                client_id=auth0_config["client_id"],
                scope=["profile", "email", "openid", "offline_access"],
                response_type="code",
                extra_params=extra_params,
            )

    def show_login_error(self, error: Optional[LoginErrors] = None) -> None:
        self.clear_all_cookies()

        auth0_config = self.settings.get("auth0_oauth", None)

        error_arg = f"?error={error.value}" if error else ""
        args = {
            "client_id": auth0_config["client_id"],
            "returnTo": f"{self.settings['host']}{self.reverse_url('login_error')}{error_arg}",
        }
        self.redirect(url_concat(f'https://{auth0_config["domain"]}/v2/logout', args))
