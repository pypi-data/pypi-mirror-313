import logging
from datetime import datetime
from urllib.parse import urlencode

from tinybird.views.aiohttp_shared_session import get_shared_session

SIGNUP_INFO_TIMEOUT: int = 1
SIGNUP_INFO_DATASOURCE: str = "signups_events"


class MarketingClient:
    async def _send_signup_info(self, append_token: str, email: str, referrer: str, session_id: str, utm: str) -> bool:
        try:
            timeout = SIGNUP_INFO_TIMEOUT
            params = {"name": SIGNUP_INFO_DATASOURCE, "token": append_token}
            url = f"https://api.tinybird.co/v0/events?{urlencode(params)}"

            send_data = {
                "email": email,
                "referrer": referrer,
                "session_id": session_id,
                "utm": utm,
                "timestamp": datetime.utcnow().isoformat(),
            }
            session = get_shared_session()
            async with session.post(url, json=send_data, timeout=timeout) as resp:
                await resp.content.read()
                if resp.status != 200 and resp.status != 202:
                    msg = await resp.text()
                    raise Exception(f"Http:{resp.status}, Text:{msg}")

            return True

        except Exception as e:
            logging.exception(f"Error sending the '{email}' signup info to {SIGNUP_INFO_DATASOURCE}: {e}")
            return False
