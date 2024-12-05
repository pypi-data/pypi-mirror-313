import logging
from typing import Any, Dict, List, Set

from tinybird.hubspot_client import HubSpotClient
from tinybird.model import retry_transaction_in_case_of_concurrent_edition_error_async
from tinybird.user import UserAccount
from tinybird.useraccounts_service import UserAccountsService


async def welcome_form_check(u: UserAccount) -> bool:
    """Display a form for collecting information about the customer (https://gitlab.com/tinybird/analytics/-/issues/3243)"""
    info = await UserAccountsService.get_auth_provider_info(u)
    return info is not None and info.get("logins_count", 0) > 2


async def welcome_form_close(u: UserAccount, data: Dict[str, Any]) -> bool:
    """Display a form for collecting information about the customer (https://gitlab.com/tinybird/analytics/-/issues/3243)"""
    hb = HubSpotClient()
    return await hb.send_welcome_form(data.get("hubspotutk", None), {**data, "email": u["email"]})


class CampaignsService:
    # Each campaign needs 2 methods:
    # - A test method, that checks if the user is apt for the campaign
    # - A close method, that makes the operations needed to close the campaign (i.e: send data to Hubspot and so)

    __campaigns__ = {"welcome-form": (welcome_form_check, welcome_form_close)}

    _settings: Dict[str, Any] = {}
    _enabled_campaigns: Set[str] = set()

    @classmethod
    def init(cls, settings):
        cls._settings = settings
        cls._enabled_campaigns = set(settings.get("enabled_campaigns", []))

    @classmethod
    def get_names(cls) -> List[str]:
        return list(cls.__campaigns__.keys())

    @classmethod
    async def check_campaign_for_user(cls, campaign: str, user: UserAccount) -> bool:
        """Checks if the user must view the specified campaign."""
        methods = cls.__campaigns__.get(campaign, None)
        if methods is None:
            logging.warning(f"check_campaign_for_user(): Unknown campaign '{campaign}'")
            return False

        try:
            return await methods[0](user)
        except Exception as e:
            logging.exception(f"check_campaign_for_user(): Error checking '{campaign}' for user '{user.email}': {e}")
            return False

    @classmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def close_campaign_for_user(cls, campaign: str, data: Dict[str, Any], user: UserAccount) -> bool:
        """Closes the campaign for the user."""

        # Mark campaign as vewed, no matter the closing operation result
        # We don't want to bother our customers in case of internal errors
        with UserAccount.transaction(user["id"]) as u:
            u.viewed_campaigns.add(campaign)

        methods = cls.__campaigns__.get(campaign, None)
        if methods is None:
            logging.warning(f"close_campaign_for_user(): Unknown campaign '{campaign}'")
            return False

        try:
            return await methods[1](user, data)
        except Exception as e:
            logging.exception(f"close_campaign_for_user(): Error closing '{campaign}' for user '{user.email}': {e}")
            return False

    @classmethod
    async def get_campaigns_for_user(cls, user: UserAccount) -> List[str]:
        """Get all active campaigns for the user."""
        viewed = user.viewed_campaigns or set()
        result = []

        for k in cls._enabled_campaigns:
            if k in viewed:
                continue
            if await cls.check_campaign_for_user(k, user):
                result.append(k)
        return result
