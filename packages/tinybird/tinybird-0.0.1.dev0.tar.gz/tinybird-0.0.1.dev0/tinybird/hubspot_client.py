import logging
from copy import deepcopy
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from tinybird.views.aiohttp_shared_session import get_shared_session


class HubSpotClient:
    async def _send_form(
        self,
        portal_id: str,
        form_guid: str,
        data: Dict[str, Any],
        hubspot_usertoken: Optional[str] = None,
        human_identifier: Optional[str] = None,
    ) -> bool:
        try:
            url = f"https://api.hsforms.com/submissions/v3/integration/submit/{portal_id}/{form_guid}"

            send_data = deepcopy(data)

            if hubspot_usertoken is not None:
                ctx = send_data.get("context", {})
                ctx.update({"hutk": hubspot_usertoken})
                send_data["context"] = ctx

            if "legalConsentOptions" not in send_data:
                send_data["legalConsentOptions"] = {
                    "consent": {
                        "consentToProcess": True,
                        "text": "I agree to allow Tinybird to store and process my personal data.",
                        "communications": [
                            {
                                "value": True,
                                "subscriptionTypeId": 999,
                                "text": "I agree to receive marketing communications from Tinybird.",
                            }
                        ],
                    }
                }

            headers = {"Content-Type": "application/json"}

            session = get_shared_session()
            async with session.post(url, json=send_data, headers=headers) as resp:
                await resp.content.read()
                if resp.status != 200:
                    msg = await resp.text()
                    raise Exception(f"Http:{resp.status}, Text:{msg}")

            return True

        except Exception as e:
            if human_identifier:
                logging.exception(
                    f"Error sending the '{human_identifier}' form to Hubspot (portal:{portal_id}, form:{form_guid}): {e}"
                )
            else:
                logging.exception(f"Error sending a form to Hubspot (portal:{portal_id}, form:{form_guid}): {e}")
            return False

    async def send_welcome_form(self, hubspot_usertoken: str, data: Dict[str, Any]) -> bool:
        what_are_you_building = data.get("what_are_you_building__free_text__", "")
        how_did_you_hear = data.get("how_did_you_hear", "")

        if len(what_are_you_building) == 0 and len(how_did_you_hear) == 0:
            return False

        portal_id = "25625634"
        form_guid = "16c32236-6b72-4007-a9e6-a34dd9ea0fcd"

        data = {
            "fields": [
                {"objectTypeId": "0-1", "name": "what_are_you_building__free_text__", "value": what_are_you_building},
                {"objectTypeId": "0-1", "name": "how_did_you_hear_about_us_", "value": how_did_you_hear},
                {"objectTypeId": "0-1", "name": "email", "value": data.get("email", None)},
            ]
        }

        return await self._send_form(
            portal_id, form_guid, data, hubspot_usertoken=hubspot_usertoken, human_identifier="Welcome"
        )

    async def send_form_to_associate_cookie_with_email(
        self,
        user_email: str,
        first_name: str,
        last_name: str,
        hubspot_usertoken: Optional[str] = None,
        referrer: Optional[str] = None,
    ) -> bool:
        if not referrer:
            referrer = "https://tinybird.co/signup"
        portal_id = "25625634"
        form_guid = "885e95b7-d481-4cfe-9bfb-55b4d1fc7db1"
        now_utc = datetime.utcnow()
        midnight_utc = datetime(now_utc.year, now_utc.month, now_utc.day, 0, 0, 0, tzinfo=timezone.utc)
        timestamp_midnight_utc = int(midnight_utc.timestamp() * 1000)

        fields = [
            {"objectTypeId": "0-1", "name": "email", "value": user_email},
            {"objectTypeId": "0-1", "name": "Product sign up", "value": timestamp_midnight_utc},
            {"objectTypeId": "0-1", "name": "Product Sign Up Date", "value": timestamp_midnight_utc},
            {"objectTypeId": "0-1", "name": "Email verified", "value": True},
            {
                "objectTypeId": "0-1",
                "name": "subscribe_to_the_tinytales_newsletter_for_musings_on_transformations___tables__and_everything_in_be",
                "value": False,
            },
        ]
        if first_name is not None:
            fields.append({"objectTypeId": "0-1", "name": "First name", "value": first_name})
        if last_name is not None:
            fields.append({"objectTypeId": "0-1", "name": "Last name", "value": last_name})

        data = {
            "fields": fields,
            "context": {
                "pageUri": referrer,
                "pageName": "Sign up · Tinybird",
            },
        }

        return await self._send_form(
            portal_id, form_guid, data, hubspot_usertoken=hubspot_usertoken, human_identifier="Update contact email"
        )
