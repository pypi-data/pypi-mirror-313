from .base import BaseHandler


class GoogleDocs(BaseHandler):
    def get(self):
        token = self.get_secure_cookie("token")
        self.render("gdocs.html", token=token, table="")


class GoogleDocsFilter(BaseHandler):
    def get(self, table):
        token = self.get_secure_cookie("token")
        self.render("gdocs.html", token=token, table=table)
