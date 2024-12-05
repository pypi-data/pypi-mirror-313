import json
from http.client import HTTPException

from tinybird.campaigns_service import CampaignsService

from .base import BaseHandler, URLMethodSpec, user_authenticated


class APIActiveCampaigns(BaseHandler):
    def __init__(self, application, request, **kwargs):
        BaseHandler.__init__(self, application, request, **kwargs)

    def check_xsrf_cookie(self):
        pass


class APIGetActiveCampaigns(APIActiveCampaigns):
    def __init__(self, application, request, **kwargs):
        APIActiveCampaigns.__init__(self, application, request, **kwargs)

    @user_authenticated
    async def get(self):
        user = self.get_user_from_db()
        pending_campaigns = await CampaignsService.get_campaigns_for_user(user)
        self.write_json({"campaigns": pending_campaigns})


class APICloseActiveCampaigns(APIActiveCampaigns):
    def __init__(self, application, request, **kwargs):
        APIActiveCampaigns.__init__(self, application, request, **kwargs)

    @user_authenticated
    async def post(self, campaign: str):
        user = self.get_user_from_db()
        try:
            data = json.loads(self.get_argument("data"))
        except Exception as e:
            raise HTTPException(400, f"Error decoding input data: {e}")

        cookie = self.get_cookie("hubspotutk", "")
        if cookie:
            data["hubspotutk"] = cookie

        result = await CampaignsService.close_campaign_for_user(campaign, data, user)
        self.write_json({"ok": result})


def handlers():
    return [
        URLMethodSpec("GET", r"/v0/active-campaigns/?", APIGetActiveCampaigns),
        URLMethodSpec("POST", r"/v0/active-campaigns/(.*)/?", APICloseActiveCampaigns),
    ]
