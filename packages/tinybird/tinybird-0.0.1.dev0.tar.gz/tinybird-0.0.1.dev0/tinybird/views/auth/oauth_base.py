import uuid
from typing import Optional, Tuple
from urllib.parse import unquote

from tinybird.hubspot_client import HubSpotClient
from tinybird.marketing_client import MarketingClient
from tinybird.redis_config import get_redis_client_from_regions_config
from tinybird.useraccounts_service import UserAccountsService
from tinybird_shared.redis_client.redis_client import TBRedisClientSync

from ...user import UserAccount, UserAccountDoesNotExist, UserAccounts
from ..login import UserViewBase


class OauthBase(UserViewBase):
    def get_user_account(self, email: str) -> Optional[UserAccount]:
        user_account = None

        try:
            user_account = UserAccounts.get_by_email(email)
        except UserAccountDoesNotExist:
            pass

        return user_account

    async def get_or_register_user_and_refresh_data(self, user, hubspotutk=None) -> UserAccount:
        user_account = None
        email = user["email"]
        first_name = user.get("given_name", None)
        last_name = user.get("family_name", None)

        try:
            user_account = UserAccounts.get_by_email(email)
        except UserAccountDoesNotExist:
            pass

        if user_account:
            return user_account

        new_user = await UserAccountsService.register_user(email, str(uuid.uuid4()), notify_user=True)
        if self.application.settings.get("hubspot_integration", False):
            await self._hubspot_send_form_to_associate_cookie_with_email(email, first_name, last_name, hubspotutk)
        if self.application.settings.get("marketing_integration_token", ""):
            await self._marketing_send_signup_info(email)

        return new_user

    async def get_or_register_user_and_refresh_data_in_region(
        self, email: str, region_redis_client: TBRedisClientSync
    ) -> UserAccount:
        user_account = None

        try:
            user_account = UserAccount.get_by_index_from_redis(region_redis_client, "email", email)
        except UserAccountDoesNotExist:
            pass

        if user_account:
            if not user_account.confirmed_account:
                user_account.confirmed_account = True
                UserAccount.save_to_redis(user_account, region_redis_client)
            return user_account

        return await UserAccountsService.register_user(
            email,
            str(uuid.uuid4()),
            confirmed_account=True,
            overwrriten_redis_Client=region_redis_client,
            region_selected=True,
            notify_user=True,
        )

    def get_user_from_other_regions(self, email: str) -> Tuple[Optional[UserAccount], Optional[str], Optional[str]]:
        available_regions = self.application.settings.get("available_regions", {})

        for region_name, region_config in available_regions.items():
            region_redis_client = get_redis_client_from_regions_config(self.application.settings, region_name)

            user_account = UserAccount.get_by_index_from_redis(region_redis_client, "email", email)

            if user_account:
                return user_account, region_name, region_config["host"]

        return None, None, None

    async def _hubspot_send_form_to_associate_cookie_with_email(
        self, user_email: str, first_name: str, last_name: str, hubspotutk=None
    ) -> None:
        referrer = self.get_cookie("referrer")
        if referrer:
            referrer = unquote(referrer)
        await HubSpotClient().send_form_to_associate_cookie_with_email(
            user_email,
            first_name,
            last_name,
            hubspot_usertoken=hubspotutk or self.get_cookie("hubspotutk"),
            referrer=referrer,
        )

    async def _marketing_send_signup_info(self, user_email: str) -> None:
        referrer = self.get_cookie("referrer")
        utm = self.get_cookie("utm")
        session_id = self.get_cookie("session-id")
        append_token = self.application.settings.get("marketing_integration_token", "")

        if referrer:
            referrer = unquote(referrer)
        await MarketingClient()._send_signup_info(
            append_token, email=user_email, referrer=referrer, session_id=session_id, utm=utm
        )
