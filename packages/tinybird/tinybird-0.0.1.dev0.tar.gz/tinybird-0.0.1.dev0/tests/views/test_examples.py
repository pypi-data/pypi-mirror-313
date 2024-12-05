from urllib.parse import quote

from tornado.web import create_signed_value

from tinybird.token_scope import scopes
from tinybird.user import Users, public

from .base_test import BaseTest, create_test_datasource, drop_test_datasource

PUBLIC_PIPE = "nyc_taxi_pipe"
PIPE_AND_TOKEN_SNIPPET = """// tinybird.js constructor function requires an Auth token.
let tinyb = tinybird('<workspace_token>')
let res = await tinyb.query('select <column> from <pipe> LIMIT 3')
"""
IMPORT_TOKEN_SNIPPET = """//norun
let tinyb = tinybird('<import_token>')
"""


class TestExamples(BaseTest):
    def __get_secure_cookie(self):
        secure_cookie = create_signed_value(self.app.settings["cookie_secret"], "workspace_token", self.admin_token)
        return f"workspace_token={secure_cookie.decode()}"

    def __get_logged_in_headers(self, user):
        self.admin_token = Users.get_token_for_scope(user, scopes.ADMIN)
        docs_host = self.app.settings["docs_host"]
        return {"Cookie": self.__get_secure_cookie(), "Referer": docs_host}

    def __publish_pipe(self, user, pipe):
        pipe.endpoint = pipe.pipeline.nodes[0].id
        Users.update_pipe(user, pipe)

    def __get_public_user_pipe(self):
        # in production public user has a 'nyc_taxi_pipe', I simulate it here
        pu = public.get_public_user()
        nyc_pipe = Users.add_pipe_sync(pu, PUBLIC_PIPE, "select 1 as passenger_count")
        Users.add_token(pu, "nyc_pipe_token", scopes.PIPES_READ, nyc_pipe.id)
        self.__publish_pipe(pu, nyc_pipe)
        return pu, nyc_pipe

    def test_examples_use_public_pipe_if_user_has_no_published_pipe(self):
        self.create_test_datasource()
        u = Users.get_by_id(self.WORKSPACE_ID)
        pipes = Users.get_pipes(u)

        # only one pipe in account
        self.assertEqual(len(pipes), 1)
        # not published
        self.assertFalse(pipes[0].is_published())

        pu, nyc_pipe = self.__get_public_user_pipe()
        nyc_pipe_token = Users.get_tokens_for_resource(pu, nyc_pipe.id, scopes.PIPES_READ)[0]

        pipe_replacement = rf"replace(new RegExp(\'&lt;pipe&gt;\', \'g\'), \'{nyc_pipe.name}\')"
        token_replacement = rf"replace(\'&lt;token&gt;\', \'{nyc_pipe_token}\')"

        examples_url = f"/examples/snippet?code={quote(PIPE_AND_TOKEN_SNIPPET,safe='')}&id=snippet_1&run=true"
        response = self.fetch(examples_url, method="GET", headers=self.__get_logged_in_headers(u))

        body = str(response.body)

        self.assertGreater(body.find(pipe_replacement), -1)
        self.assertGreater(body.find(token_replacement), -1)

    def test_examples_use_published_used_by_pipe_of_datasource(self):
        self.create_test_datasource()
        u = Users.get_by_id(self.WORKSPACE_ID)

        u_datasources = Users.get_datasources(u)
        self.assertEqual(len(u_datasources), 1)

        ds = u_datasources[0]
        u_pipes = Users.get_datasource_used_by(u, ds)

        self.assertEqual(len(u_pipes), 1)
        self.assertFalse(u_pipes[0].is_published())

        second_pipe = Users.add_pipe_sync(u, "second_pipe", f"select * from {ds.name}")
        self.assertFalse(second_pipe.is_published())

        new_ds = Users.add_datasource_sync(u, "new_datasource")
        create_test_datasource(u, new_ds)
        Users.update_datasource(u, new_ds)

        third_pipe = Users.add_pipe_sync(u, "third_pipe", "select * from new_datasource")
        Users.add_token(u, "third_pipe_token", scopes.PIPES_READ, third_pipe.id)
        self.__publish_pipe(u, third_pipe)
        third_pipe_token = Users.get_tokens_for_resource(u, third_pipe.id, scopes.PIPES_READ)[0]

        headers = self.__get_logged_in_headers(u)

        examples_url = f"/examples/snippet?code={quote(PIPE_AND_TOKEN_SNIPPET,safe='')}&id=snippet_1&run=true"
        response = self.fetch(examples_url, method="GET", headers=headers)

        body = str(response.body)
        self.assertEqual(response.code, 200)

        pipe_replacement = rf"replace(new RegExp(\'&lt;pipe&gt;\', \'g\'), \'{third_pipe.name}\')"
        token_replacement = rf"replace(\'&lt;token&gt;\', \'{third_pipe_token}\')"
        column_replacement = rf"select a from {third_pipe.name} LIMIT 3"

        self.assertGreater(body.find(pipe_replacement), -1)
        self.assertGreater(body.find(token_replacement), -1)
        self.assertGreater(body.find(column_replacement), -1)
        drop_test_datasource(u, new_ds)

    def test_examples_use_datasource_create_for_import_token(self):
        u = Users.get_by_id(self.WORKSPACE_ID)

        import_token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        examples_url = f"/examples/snippet?code={quote(IMPORT_TOKEN_SNIPPET,safe='')}&id=snippet_1&run=true"
        response = self.fetch(examples_url, method="GET", headers=self.__get_logged_in_headers(u))
        self.assertEqual(response.code, 200)
        body = str(response.body)

        token_replacement = rf"replace(\'&lt;import_token&gt;\', \'{import_token}\')"
        self.assertGreater(body.find(token_replacement), -1)

    def test_examples_import_token_defaults_for_unlogged_users(self):
        examples_url = f"/examples/snippet?code={quote(IMPORT_TOKEN_SNIPPET,safe='')}&id=snippet_1&run=true"
        headers = {"Referer": self.app.settings["docs_host"]}

        response = self.fetch(examples_url, method="GET", headers=headers)

        token_replacement = r"replace(\'&lt;import_token&gt;\', \'&lt;DATASOURCES:CREATE token&gt;\')"
        body = str(response.body)
        self.assertGreater(body.find(token_replacement), -1)
