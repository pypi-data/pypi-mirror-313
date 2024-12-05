import uuid
from urllib.parse import urlencode

import tornado.web

from tinybird.user import User
from tinybird.views.api_workspaces import STARTER_KIT_PARAMS
from tinybird.views.base import WebBaseHandler, user_authenticated
from tinybird.views.login import base_login


class WorkspacesLoginHandler(WebBaseHandler):
    @tornado.web.authenticated
    @user_authenticated
    async def post(self):
        user = self.get_user_from_db()

        if not user:
            self.redirect("/login")

        workspace_id = self.get_argument("workspace_id")

        region_name = self.get_current_region()

        if not user.has_access_to(workspace_id):
            base_login(self, user, region_name=region_name)
            self.render("404.html", current_user=user)
            return

        workspace = User.get_by_id(workspace_id)

        base_login(self, user, workspace, region_name)
        self.redirect(self.reverse_url("workspace_dashboard", workspace_id))


class WorkspaceStarterKitRedirectHandler(WebBaseHandler):
    @tornado.web.authenticated
    @user_authenticated
    def get(self):
        url = None
        get_params = dict((k, self.get_argument(k, "")) for k in STARTER_KIT_PARAMS)

        # Make an unique name
        desired_name = get_params.get("name", "workspace")
        suffix = str(uuid.uuid4())[:4]
        get_params["name"] = f"{desired_name}_{suffix}"

        params = urlencode(dict((k, v) for k, v in get_params.items() if v))

        user = self.get_user_from_db()
        if user:
            url = self.reverse_url("new_workspace", user.id)

        if url is None:
            workspace = self.get_workspace_from_db()
            if workspace:
                url = self.reverse_url("new_workspace", workspace.id)

        if url is None:
            self.redirect("/login")
        else:
            self.redirect(f"{url}?{params}")
