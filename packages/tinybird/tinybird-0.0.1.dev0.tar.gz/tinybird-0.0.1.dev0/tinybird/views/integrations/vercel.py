import json
import logging
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

import tornado.web

from tinybird.integrations.vercel import (
    VercelIntegration,
    VercelIntegrationDoesNotExist,
    VercelIntegrationPhase,
    VercelIntegrationService,
)
from tinybird.token_scope import scopes
from tinybird.user import UserAccount, UserAccounts
from tinybird.views.aiohttp_shared_session import get_shared_session
from tinybird.views.base import ApiHTTPError, WebBaseHandler, confirmed_account


class NewVercelIntegrationRedirectHandler(WebBaseHandler):
    def get_urlencoded_args(self, args: List[str], extra_args: Optional[Dict[str, Any]] = None) -> str:
        url_args: Dict[str, Any] = dict(
            (arg, self.get_argument(arg, "")) for arg in args if self.get_argument(arg, "") != ""
        )
        if extra_args:
            url_args.update(extra_args)
        return urlencode(url_args)

    @tornado.web.authenticated
    @confirmed_account
    async def get(self, *args):
        user: Optional[UserAccount] = self.get_current_user()
        assert isinstance(user, UserAccount)

        access_code: str = self.get_argument("code", "")
        region: Optional[str] = self.get_argument("region", None)
        current_region: Optional[str] = self.get_current_region()
        region_selected: bool

        # Hack for development environment
        if not current_region or region == "localhost":
            region = current_region = "localhost"
            region_selected = True
        else:
            available_regions: Dict[str, Any] = self.application.settings.get("available_regions", {})
            region_selected = region in available_regions and current_region == region

        if not region_selected:
            url: str = self.reverse_url("select_region_vercel_integration")
            args = self.get_urlencoded_args(["code", "next", "configurationId"])
            url = f"{url}&{args}" if "?" in url else f"{url}?{args}"
            self.redirect(url)
            return

        integration: Optional[VercelIntegration] = None
        existing = user.get_integration_info_by_type("vercel")
        if len(existing) > 0:
            integration = VercelIntegration.get_by_id(existing[0].integration_id)
        # Do we want to setup a new integration?
        # If so, let's reset the current one
        if (
            integration
            and self.get_argument("code", "")
            and integration.installation_id != self.get_argument("configurationId", "")
        ):
            # If we have bindings for this integration, let's raise an error warning the user about it.
            # If the integration is empty (i.e: no synced tokens) we can delete it as we're not breaking anything.
            if len(integration.get_bindings()) > 0:
                owner_info: Dict[str, Any] = await VercelIntegrationService.get_integration_owner_info(integration)
                self.render("integration_error.html", integration_type="vercel", owner_info=owner_info)
                return

            user = await VercelIntegrationService.remove_integration(user, integration.id, remove_remote=True)
            integration = None

        if not integration:
            integration = await VercelIntegrationService.get_integration_for_user(user, access_code)
            user = await UserAccounts.add_integration(user, "vercel", integration.id)

        url: str = self.reverse_url("configure_vercel_integration", integration.id)
        args = self.get_urlencoded_args(["code", "next", "configurationId"], {"region": region})
        url = f"{url}&{args}" if "?" in url else f"{url}?{args}"
        self.redirect(url)


class ConfigureVercelIntegrationRedirectHandler(WebBaseHandler):
    @tornado.web.authenticated
    @confirmed_account
    async def get(self, *args):
        user: Optional[UserAccount] = self.get_current_user()
        assert isinstance(user, UserAccount)

        if len(user.get_integration_info_by_type("vercel")) == 0:
            ApiHTTPError(400, "User doesn't have a pending Vercel integration")

        integration: VercelIntegration = await VercelIntegrationService.get_integration_for_user(user)
        if integration.integration_phase == VercelIntegrationPhase.INSTALLING:
            integration = await VercelIntegrationService.finalize_install(integration)

        user_account = self.get_user_from_db()
        region = self.get_current_region()
        user_token = user_account.get_token_for_scope(scopes.AUTH)
        token = user_token
        auth0_config = self.settings.get("auth0_oauth", {})

        self.render(
            "integrations.html",
            jwt=token,
            # User
            user_name=user_account["email"],
            user_id=user_account["id"],
            user_region_selected=user_account["region_selected"],
            feature_flags={},
            feature_flags_workspace={},
            user_token=user_token,
            # Settings
            host=self.application.settings["api_host"],
            region=region,
            plans_names={},
            GSHEETS_API_KEY=self.application.settings["google_api"]["api_key"],
            GSHEETS_CLIENT_ID=self.application.settings["google_api"]["client_id"],
            auth0_domain=auth0_config.get("domain", ""),
            auth0_client_id=auth0_config.get("client_id", ""),
        )


class SelectRegionVercelIntegrationRedirectHandler(WebBaseHandler):
    @tornado.web.authenticated
    @confirmed_account
    async def get(self, *args: Any) -> None:
        user: Optional[UserAccount] = self.get_current_user()
        assert isinstance(user, UserAccount)

        user_account = self.get_user_from_db()
        region = self.get_current_region()
        user_token = user_account.get_token_for_scope(scopes.AUTH)
        workspaces = await user_account.get_workspaces()
        token = user_token
        auth0_config = self.settings.get("auth0_oauth", {})

        self.render(
            "integrations_region.html",
            jwt=token,
            # User
            user_name=user_account["email"],
            user_id=user_account["id"],
            user_region_selected=user_account["region_selected"],
            feature_flags={},
            feature_flags_workspace={},
            user_token=user_token,
            workspaces=workspaces,
            # Settings
            host=self.application.settings["api_host"],
            region=region,
            plans_names={},
            GSHEETS_API_KEY=self.application.settings["google_api"]["api_key"],
            GSHEETS_CLIENT_ID=self.application.settings["google_api"]["client_id"],
            auth0_domain=auth0_config.get("domain", ""),
            auth0_client_id=auth0_config.get("client_id", ""),
            access_code=args,
        )


class VercelWebhookHandler(WebBaseHandler):
    """Handles requests made from Vercel API via Webhook."""

    def check_xsrf_cookie(self):
        pass

    async def post(self) -> None:
        """FIXME: We're not validating Vercel signature present in headers"""

        no_propagate: bool = self.get_argument("no_propagate", "") != ""

        body: Dict[str, Any] = json.loads(self.request.body)
        payload: Dict[str, Any] = body.get("payload", {})
        action: str = body.get("type", "")

        # Handle the incoming message

        handled: bool = False

        if action == "integration-configuration.removed":
            handled = await self.integration_configuration_removed(payload)
        else:
            logging.info(f"[Vercel Integration] Received an unsupported webhook event '{action}'")
            return

        if handled or no_propagate:
            return

        # Propagate the message to other TB regions

        try:
            available_regions: Dict[str, Any] = self.application.settings.get("available_regions", {})
            if len(available_regions) == 0:
                return

            current_region: str = self.application.settings.get("tb_region", "")
            current_host: str = available_regions[current_region]["host"] if current_region in available_regions else ""

            # Get availabele hosts, excluding the current one, to avoid flooding it with requests
            hosts: List[str] = [v["host"] for v in available_regions.values() if v["host"] != current_host]

            session = get_shared_session()
            for host in hosts:
                url: str = f"{host}/integrations/vercel/webhook?no_propagate=1"
                try:
                    _ = await session.post(url=url, data=self.request.body)
                except Exception as ex:
                    logging.warning(f"[Vercel Integration] Error propagating webhook request to {host}: {ex}")
        except Exception as ex:
            logging.exception(f"[Vercel Integration] Can't propagate message to other TB hosts: {ex}")

    async def integration_configuration_removed(self, payload: Dict[str, Any]) -> bool:
        """Handles the `integration-configuration.removed` message.

        See: https://vercel.com/docs/integrations/webhooks-overview/webhooks-api#integration-configuration.removed
        """
        config: Dict[str, Any] = payload.get("configuration", {})

        integration_id: str
        integration: VercelIntegration

        installation_id = config["id"]

        try:
            integration = VercelIntegration.get_by_installation_id(installation_id)
            integration_id = integration.id
            logging.info(
                f"[Vercel Integration] Starting the deletion of the integration {integration_id} (installation_id={installation_id})"
            )
        except VercelIntegrationDoesNotExist:
            logging.warning(f"[Vercel Integration] Integration with Vercel id {installation_id} does not exists")
            return False
        except Exception as ex:
            logging.warning(
                f"[Vercel Integration] Error removing local integration with Vercel id {installation_id} by webhook request: {ex}"
            )
            return False

        if config.get("projectSelection", "all") == "all":
            logging.info(f"[Vercel Integration] Removing all projects from the integration {integration_id}")
            user = UserAccount.get_by_id(integration.integration_user_id)
            if not user:
                logging.exception(f"Unexpected error: User {integration.integration_user_id} not found")
                return False
            await VercelIntegrationService.remove_integration(user, integration.id)
        else:
            projects: List[str] = config.get("projects", [])
            logging.info(
                f"[Vercel Integration] Removing the following projects from the integration {integration_id}: {','.join(projects)}"
            )
            for id in projects:
                all_tokens: List[str] = [b.token for b in integration.get_bindings(by_project_id=id)]
                integration = await VercelIntegrationService.remove_bindings(integration, id, all_tokens)
        return True


class FakeNewVercelIntegrationRedirectHandler(WebBaseHandler):
    @tornado.web.authenticated
    @confirmed_account
    async def get(self, *args: Any) -> None:
        user: Optional[UserAccount] = self.get_current_user()
        assert isinstance(user, UserAccount)

        user_account = self.get_user_from_db()
        region = self.get_current_region()
        user_token = user_account.get_token_for_scope(scopes.AUTH)
        workspaces = await user_account.get_workspaces()
        token = user_token
        auth0_config = self.settings.get("auth0_oauth", {})

        self.render(
            "integrations.html",
            jwt=token,
            # User
            user_name=user_account["email"],
            user_id=user_account["id"],
            user_region_selected=user_account["region_selected"],
            feature_flags={},
            feature_flags_workspace={},
            user_token=user_token,
            workspaces=workspaces,
            # Settings
            host=self.application.settings["api_host"],
            region=region,
            plans_names={},
            GSHEETS_API_KEY=self.application.settings["google_api"]["api_key"],
            GSHEETS_CLIENT_ID=self.application.settings["google_api"]["client_id"],
            auth0_domain=auth0_config.get("domain", ""),
            auth0_client_id=auth0_config.get("client_id", ""),
        )
