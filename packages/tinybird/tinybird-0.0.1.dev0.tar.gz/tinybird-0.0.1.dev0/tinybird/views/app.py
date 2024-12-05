import logging

import tornado.web

from .base import WebBaseHandler, confirmed_account, get_workspace_to_redirect
from .login import base_login


class AppHtmlHandler(WebBaseHandler):
    @tornado.web.authenticated
    @confirmed_account
    async def get(self, *args):
        user_account = self.get_user_from_db()
        region = self.get_current_region()
        workspaces = await user_account.get_workspaces()
        id_from_url = args[0] if args else None
        workspace = get_workspace_to_redirect(self, workspaces, id_from_url)

        # Login
        try:
            if workspaces and workspace:
                if user_account.has_access_to(workspace.id):
                    base_login(self, user_account, workspace, region_name=region)
                else:
                    base_login(self, user_account, region_name=region)
                    self.render("404.html", current_user=user_account)
                    return

            else:
                base_login(self, user_account, None, region_name=region)

        except Exception:
            base_login(self, user_account, region_name=region)
            self.render("404.html", current_user=user_account)
            return

        app_host = self.application.settings.get("app_host", None)
        params = f"from={self.request.full_url()}"

        path = self.request.uri
        if path.find("/dashboard") != -1:
            if workspace:
                new_path = path.replace(id_from_url, workspace.name)
                full_url = self.request.protocol + "://" + self.request.host + new_path
                params = f"from={full_url}"
            else:
                params = ""

        redirect_url = app_host
        if params != "":
            redirect_url = f"{app_host}?{params}"
        logging.info(f"Redirecting to {redirect_url}")

        return self.redirect(f"{redirect_url}")
