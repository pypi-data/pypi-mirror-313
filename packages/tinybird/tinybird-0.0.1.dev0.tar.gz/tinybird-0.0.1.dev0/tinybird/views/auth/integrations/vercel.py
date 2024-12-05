import uuid
from typing import Dict, List, Optional
from urllib.parse import urlencode

import tornado.web

from tinybird.views.base import WebBaseHandler, user_authenticated

"""Params we need to preserve for the Vercel integration
"""
VERCEL_INTEGRATION_PARAMS: List[str] = ["source", "code", "configurationId", "next"]


class VercelIntegrationRedirectHandler(WebBaseHandler):
    @tornado.web.authenticated
    @user_authenticated
    def get(self):
        url: Optional[str] = None
        get_params: Dict[str, str] = dict((k, self.get_argument(k, "")) for k in VERCEL_INTEGRATION_PARAMS)

        # Make an unique name
        desired_name: str = get_params.get("name", "workspace")
        suffix: str = str(uuid.uuid4())[:4]
        get_params["name"] = f"{desired_name}_{suffix}"

        params: str = urlencode(dict((k, v) for k, v in get_params.items() if v))

        user = self.get_user_from_db()
        if user:
            url = self.reverse_url("new_vercel_integration_redirect", user.id)

        if url:
            workspace = self.get_workspace_from_db()
            if workspace:
                url = self.reverse_url("new_vercel_integration_redirect", workspace.id)

        if url is None:
            self.redirect("/login")
        else:
            self.redirect(f"{url}?{params}")
