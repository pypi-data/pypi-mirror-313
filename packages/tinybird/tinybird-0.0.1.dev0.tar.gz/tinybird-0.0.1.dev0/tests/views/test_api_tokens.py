import asyncio
import json
import uuid
from datetime import datetime, timedelta
from http.client import HTTPResponse
from time import time
from unittest.mock import AsyncMock, patch
from urllib.parse import quote, urlencode

import jwt
import requests
import tornado.testing
import tornado.web

from tests.utils import CsvIO
from tinybird.token_scope import scope_codes, scopes
from tinybird.tokens import is_jwt_token
from tinybird.user import User, UserAccount, Users
from tinybird.views.api_tokens import APITokensUserHandler
from tinybird.views.base import INVALID_AUTH_MSG

from .base_test import BaseTest, TBApiProxyAsync


class TestAPIToken(BaseTest):
    def setUp(self):
        super().setUp()

        self.tb_api_proxy = TBApiProxyAsync(self)

    async def __get_num_tokens(self, admin_token):
        response = await self.fetch_async("/v0/tokens/?token=%s" % admin_token, method="GET")
        result = json.loads(response.body)
        return len(result["tokens"])

    def test_non_auth(self):
        self.check_non_auth_responses(["/v0/tokens", "/v0/tokens?token=fake"])

    @tornado.testing.gen_test
    async def test_list_tokens_auth(self):
        u = Users.get_by_id(self.WORKSPACE_ID)

        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        response = await self.fetch_async("/v0/tokens/?token=%s" % token, method="GET")
        self.assertEqual(response.code, 403)

        response = await self.fetch_async("/v0/tokens/", method="GET")
        self.assertEqual(response.code, 403)

        token = Users.get_token_for_scope(u, scopes.ADMIN)
        response = await self.fetch_async("/v0/tokens/?token=%s" % token, method="GET")
        self.assertEqual(response.code, 200, response.body)

        token = Users.add_token(u, "tokens_admin", scopes.TOKENS)
        response = await self.fetch_async("/v0/tokens/?token=%s" % token, method="GET")
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        self.assertIn("tokens", result)
        for token in result["tokens"]:
            for scope in token["scopes"]:
                self.assertIn(scope["type"], scope_codes)

    @tornado.testing.gen_test
    async def test_list_tokens_admin(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN_USER)
        response = await self.fetch_async("/v0/tokens/?token=%s" % token, method="GET")
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        # Expected 3:
        #  Workspace admin
        #  User admin
        #  Create datasources
        self.assertEqual(len(result["tokens"]), 3, result)
        # Now add a guest member
        guest = self.register_user(email=f"guest_{uuid.uuid4().hex}@example.com")
        self.users_to_delete.append(guest)
        await Users.add_users_to_workspace_async(
            workspace_id=self.WORKSPACE_ID, users_emails=[guest.email], role="guest"
        )
        response = await self.fetch_async("/v0/tokens?token=%s" % token, method="GET")
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        # Expected 4:
        #  Workspace admin
        #  User admin
        #  Guest admin
        #  Create datasources
        self.assertEqual(len(result["tokens"]), 4, result)

    @tornado.testing.gen_test
    async def test_list_tokens_guest(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        guest = self.register_user(email=f"guest_{uuid.uuid4().hex}@example.com")
        await Users.add_users_to_workspace_async(
            workspace_id=self.WORKSPACE_ID, users_emails=[guest.email], role="guest"
        )
        guest_token = Users.get_token_for_scope(u, scopes.ADMIN_USER, resource_id=guest.id)
        response = await self.fetch_async("/v0/tokens/?token=%s" % guest_token, method="GET")
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        # Expected 2:
        #  Guest admin
        #  Create datasources
        self.assertEqual(len(result["tokens"]), 2, result)

    @tornado.testing.gen_test
    async def test_list_tokens_viewer(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        viewer = self.register_user(email=f"guest_{uuid.uuid4().hex}@example.com")
        self.users_to_delete.append(viewer)
        u = await Users.add_users_to_workspace_async(
            workspace_id=self.WORKSPACE_ID, users_emails=[viewer.email], role="viewer"
        )
        viewer_token = Users.get_token_for_scope(u, scopes.ADMIN_USER, resource_id=viewer.id)
        response = await self.fetch_async(f"/v0/tokens?token={viewer_token}", method="GET")
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        # Expected 2:
        #  viewer admin + create ds
        self.assertEqual(len(result["tokens"]), 2, result)
        non_obfuscated_tokens = [t for t in result["tokens"] if "token" in t]
        self.assertEqual(len(non_obfuscated_tokens), 1)

    @tornado.testing.gen_test
    async def test__create_token(self):
        self.create_test_datasource()
        u = Users.get_by_id(self.WORKSPACE_ID)
        pipe = Users.add_pipe_sync(u, f"pipe_{uuid.uuid4().hex}", "select * from test_table where city = 'Madrid'")
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        async def test_token(origin: str, resource_id: str, scope: str, expectedStatus: int) -> HTTPResponse:
            tokenName = f"test{uuid.uuid4().hex}"
            params = f"token={token}&name={tokenName}"
            if scope:
                params = params + f"&scope={scope}"
            if origin:
                params = params + f"&origin={origin}"
            if resource_id:
                params = params + f"&resource_id={resource_id}"

            response = await self.fetch_async(f"/v0/tokens?{params}", method="POST", body="")
            self.assertEqual(response.code, expectedStatus)

            if response.code == 200:
                body = json.loads(response.body)
                self.assertEqual(body["token"] != "", True)
                self.assertEqual(body["name"], tokenName)
                self.assertEqual(body["host"], self.app.settings.get("tb_region"), body)

            return response

        # Empty origin (backwards compatibility)
        response = await test_token("", "", "DATASOURCES:READ:test_table", 200)
        body = json.loads(response.body)
        self.assertEqual(body["scopes"], [{"type": "DATASOURCES:READ", "resource": "test_table", "filter": ""}])

        # Origin DS
        await test_token("DS", "test_table", "DATASOURCES:READ:test_table", 200)
        await test_token("DS", "", "DATASOURCES:READ:test_table", 400)

        # Origin P
        await test_token("P", pipe.name, f"PIPES:READ:{pipe.id}", 200)
        await test_token("P", pipe.id, f"PIPES:READ:{pipe.id}", 200)
        await test_token("P", "", f"PIPES:READ:{pipe.id}", 400)

        # Origin C
        await test_token("C", "", f"PIPES:DROP:{pipe.id}", 200)

    @tornado.testing.gen_test
    async def test__create_token_for_service_datasource(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        # READ scope (the only allowed)
        response = await self.fetch_async(
            f"/v0/tokens?token={token}&name=test_read&scope=DATASOURCES:READ:tinybird.pipe_stats",
            method="POST",
            body="",
        )
        self.assertEqual(response.code, 200, response.body)

        # APPEND scope
        response = await self.fetch_async(
            f"/v0/tokens?token={token}&name=test_append&scope=DATASOURCES:APPEND:tinybird.pipe_stats",
            method="POST",
            body="",
        )
        self.assertEqual(response.code, 400)

    @tornado.testing.gen_test
    async def test__create_not_allowed_token(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        response = await self.fetch_async(f"/v0/tokens?token={token}&name=test&scope=AUTH", method="POST", body="")
        self.assertEqual(response.code, 400)

        response = await self.fetch_async(
            f"/v0/tokens?token={token}&name=test&scope=ADMIN_USER", method="POST", body=""
        )
        self.assertEqual(response.code, 400)

    @tornado.testing.gen_test
    async def test__create_token_already_exists(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        response = await self.fetch_async(
            "/v0/tokens/?token=%s&name=unique_name&scope=ADMIN" % token, method="POST", body=""
        )
        self.assertEqual(response.code, 200, response.body)

        response = await self.fetch_async(
            "/v0/tokens/?token=%s&name=unique_name&scope=ADMIN" % token, method="POST", body=""
        )
        res = json.loads(response.body)
        self.assertEqual(response.code, 400)
        self.assertEqual(res["error"], 'Auth token with name "unique_name" already exists')

    @tornado.testing.gen_test
    async def test__modify_token(self):
        self.create_test_datasource()
        workspace = Users.get_by_id(self.WORKSPACE_ID)
        adm_token = Users.get_token_for_scope(workspace, scopes.ADMIN)

        original_token = Users.get_token_access_info(workspace, adm_token)
        self.assertEqual(original_token.description, "")

        response = await self.fetch_async(
            "/v0/tokens/%s?token=%s&name=test&scope=DATASOURCES:READ:test_table&scope=PIPES:READ:test_pipe&description=updated"
            % (adm_token, adm_token),
            method="PUT",
            body="",
        )

        self.assertEqual(response.code, 200, response.body)

        updated_token = Users.get_token_access_info(workspace, adm_token)
        self.assertFalse(updated_token.has_scope(scopes.ADMIN))
        self.assertEqual(updated_token.name, "test")
        self.assertEqual(updated_token.description, "updated")

        resources = updated_token.get_resources_for_scope(scopes.DATASOURCES_READ)
        self.assertEqual(resources, [Users.get_datasource(workspace, "test_table").id])

        resources = updated_token.get_resources_for_scope(scopes.PIPES_READ)
        self.assertEqual(resources, [Users.get_pipe(workspace, "test_pipe").id])

    @tornado.testing.gen_test
    async def test__modify_token_body(self):
        self.create_test_datasource()
        workspace = Users.get_by_id(self.WORKSPACE_ID)
        adm_token = Users.get_token_for_scope(workspace, scopes.ADMIN)

        original_token = Users.get_token_access_info(workspace, adm_token)
        self.assertEqual(original_token.description, "")

        response = await self.fetch_async(
            "/v0/tokens/%s?token=%s" % (adm_token, adm_token),
            method="PUT",
            body="name=test&scope=DATASOURCES:READ:test_table&scope=PIPES:READ:test_pipe&description=updated",
        )

        self.assertEqual(response.code, 200, response.body)

        updated_token = Users.get_token_access_info(workspace, adm_token)
        self.assertFalse(updated_token.has_scope(scopes.ADMIN))
        self.assertEqual(updated_token.name, "test")
        self.assertEqual(updated_token.description, "updated")

        resources = updated_token.get_resources_for_scope(scopes.DATASOURCES_READ)
        self.assertEqual(resources, [Users.get_datasource(workspace, "test_table").id])

        resources = updated_token.get_resources_for_scope(scopes.PIPES_READ)
        self.assertEqual(resources, [Users.get_pipe(workspace, "test_pipe").id])

    @tornado.testing.gen_test
    async def test__modify_token_bad_auth(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.DATASOURCES_READ, "test")
        response = await self.fetch_async(
            "/v0/tokens/%s?token=%s&name=test&scope=READ:test" % (token, token), method="PUT", body=""
        )
        self.assertEqual(response.code, 403)

    @tornado.testing.gen_test
    async def test__delete_token(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        response = await self.fetch_async("/v0/tokens/%s?token=%s" % (token, token), method="DELETE")
        self.assertEqual(response.code, 200, response.body)
        t = Users.get_token_access_info(u, token)
        self.assertEqual(t, None)

    @tornado.testing.gen_test
    async def test__delete_token_by_id(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        t = u.get_token_access_info(token)
        response = await self.fetch_async(f"/v0/tokens/{t.id}?token={token}", method="DELETE")
        self.assertEqual(response.code, 200, response.body)
        t = Users.get_token_access_info(u, token)
        self.assertEqual(t, None)

    @tornado.testing.gen_test
    async def test__delete_token_by_name(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        t = Users.get_token_access_info(u, token)
        response = await self.fetch_async(f"/v0/tokens/{quote(t.name)}?token={token}", method="DELETE")
        self.assertEqual(response.code, 200, response.body)
        t = Users.get_token_access_info(u, token)
        self.assertEqual(t, None)

    @tornado.testing.gen_test
    async def test__refresh_token(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        response = await self.fetch_async("/v0/tokens/%s/refresh?token=%s" % (token, token), method="POST", body="")
        self.assertEqual(response.code, 200, response.body)
        new_token = json.loads(response.body)
        self.assertNotEqual(token, new_token["token"])
        response = await self.fetch_async("/v0/tokens/%s?token=%s" % (new_token["token"], new_token["token"]))
        self.assertEqual(response.code, 200, response.body)

    @tornado.testing.gen_test
    async def test__refresh_token_called_with_non_autorised_token_returns_403(self):
        w = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(w, "datasource_create_token", scopes.DATASOURCES_CREATE)
        response = await self.fetch_async("/v0/tokens/%s/refresh?token=%s" % (token, token), method="POST", body="")
        self.assertEqual(response.code, 403)

    @tornado.testing.gen_test
    async def test__refresh_other_users_admin_token(self):
        new_name = f"test_33a_{uuid.uuid4().hex}@example.com"
        new_user = UserAccount.register(new_name, "pass")
        self.users_to_delete.append(new_user)

        user = UserAccount.get_by_id(self.USER_ID)
        user_token = UserAccount.get_token_for_scope(user, scopes.AUTH)

        await self.tb_api_proxy.invite_user_to_workspace(user_token, self.WORKSPACE_ID, new_name)

        wk_temp = Users.get_by_id(self.WORKSPACE_ID)

        tokens = [tk for tk in wk_temp.tokens if tk.has_scope(scopes.ADMIN_USER)]

        # Own admin token: we can refresh and view it
        response = await self.fetch_async(
            "/v0/tokens/%s/refresh?token=%s" % (tokens[0].token, tokens[0].token), method="POST", body=""
        )
        self.assertEqual(response.code, 200, response.body)
        new_token = json.loads(response.body)
        test_token = new_token["token"]
        self.assertNotEqual(tokens[0].token, test_token)
        response = await self.fetch_async("/v0/tokens/%s?token=%s" % (test_token, test_token))
        self.assertEqual(response.code, 200, response.body)

        # Reload tokens
        wk_temp = Users.get_by_id(self.WORKSPACE_ID)
        other_token = next(
            (tk for tk in wk_temp.tokens if tk.has_scope(scopes.ADMIN_USER) and tk.token != test_token), None
        )

        # Other user's admin token: we can refresh but can't view it
        response = await self.fetch_async(
            "/v0/tokens/%s/refresh?token=%s" % (other_token.token, test_token), method="POST", body=""
        )
        self.assertEqual(response.code, 200, response.body)
        new_token = json.loads(response.body)
        self.assertNotIn("token", new_token)

    @tornado.testing.gen_test
    async def test__add_token_with_filters(self):
        self.create_test_datasource()
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        response = await self.fetch_async(
            '/v0/tokens?token=%s&name=test_table&scope=DATASOURCES:READ:test_table:a+>+1+and+column+==+"test"' % token,
            method="POST",
            body="",
        )
        res = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(res["token"] != "", True)
        self.assertEqual(res["name"], "test_table")
        self.assertEqual(
            res["scopes"],
            [{"type": "DATASOURCES:READ", "resource": "test_table", "filter": 'a > 1 and column == "test"'}],
        )

    @tornado.testing.gen_test
    async def test__create_token_invalid_scope(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        response = await self.fetch_async(
            "/v0/tokens?token=%s&name=invalid_token&scope=INVALID:SCOPE" % token, method="POST", body=""
        )
        self.assertEqual(response.code, 400)
        response = await self.fetch_async(
            "/v0/tokens?token=%s&name=invalid_token&scope=ANOTHERINVALIDSCOPE" % token, method="POST", body=""
        )
        self.assertEqual(response.code, 400)

    @tornado.testing.gen_test
    async def test__add_admin_token(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        response = await self.fetch_async(
            "/v0/tokens?token=%s&name=new_admin_token&scope=ADMIN" % token, method="POST", body=""
        )
        self.assertEqual(response.code, 200, response.body)
        res = json.loads(response.body)
        self.assertEqual(res["token"] != "", True)
        self.assertEqual(res["name"], "new_admin_token")
        self.assertEqual(res["scopes"], [{"type": "ADMIN"}])

    @tornado.testing.gen_test
    async def test__add_append_token_with_filters(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        response = await self.fetch_async(
            '/v0/tokens?token=%s&name=test_table&scope=DATASOURCES:APPEND:test2:a+>+1+and+column+==+"test"' % token,
            method="POST",
            body="",
        )
        self.assertEqual(response.code, 400)

    @tornado.testing.gen_test
    async def test__add_token_with_complex_filter(self):
        self.create_test_datasource()
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        response = await self.fetch_async(
            '/v0/tokens?token=%s&name=token_name&scope=DATASOURCES:READ:test_table:a+>+1+and+column+==+"test"+AND+column3+in+(select+id+from+another+table)'
            % token,
            method="POST",
            body="",
        )
        res = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(res["token"] != "", True)
        self.assertEqual(res["name"], "token_name")
        self.assertEqual(
            res["scopes"],
            [
                {
                    "type": "DATASOURCES:READ",
                    "resource": "test_table",
                    "filter": 'a > 1 and column == "test" AND column3 in (select id from another table)',
                }
            ],
        )
        response = await self.fetch_async("/v0/tokens/%s?token=%s" % (res["token"], token))
        res = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(
            res["scopes"],
            [
                {
                    "type": "DATASOURCES:READ",
                    "resource": "test_table",
                    "filter": 'a > 1 and column == "test" AND column3 in (select id from another table)',
                }
            ],
        )

    @tornado.testing.gen_test
    async def test__modify_token_with_filters(self):
        self.create_test_datasource()
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        response = await self.fetch_async(
            "/v0/tokens/%s?token=%s&name=test&scope=DATASOURCES:READ:test_table:a+>+1" % (token, token),
            method="PUT",
            body="",
        )
        t = Users.get_token_access_info(u, token)
        resources = t.get_resources_for_scope(scopes.DATASOURCES_READ)
        resource_id = Users.get_datasource(u, "test_table").id

        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(t.has_scope(scopes.ADMIN), False)
        self.assertEqual(t.has_scope(scopes.DATASOURCES_READ), True)
        self.assertEqual(t.get_filters(), {resource_id: "a > 1"})
        self.assertEqual(t.name, "test")
        self.assertEqual(resources, [resource_id])

    @tornado.testing.gen_test
    async def test__create_token_with_pipe_scope(self):
        u = Users.get_by_id(self.WORKSPACE_ID)

        pipe = Users.add_pipe_sync(u, "pipe_for_my_dashboard", "select * from test_table where city = 'Madrid'")

        my_token_name = "my_token"
        with User.transaction(u.id) as user:
            my_token = user.add_token(my_token_name, None)
            t = user.get_token_access_info(my_token)
            t.add_scope(scopes.PIPES_READ, pipe.id)

        admin_token = Users.get_token_for_scope(u, scopes.ADMIN)
        response = await self.fetch_async("/v0/tokens/%s?token=%s" % (my_token, admin_token), method="GET")
        self.assertEqual(response.code, 200, response.body)
        token = json.loads(response.body)
        self.assertEqual(token["name"], my_token_name)
        self.assertEqual(token["scopes"], [{"filter": "", "resource": "pipe_for_my_dashboard", "type": "PIPES:READ"}])

    @tornado.testing.gen_test
    async def test__create_token_with_datasources_create_scope(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        response = await self.fetch_async(
            "/v0/tokens?token=%s&name=test-datasources-create&scope=DATASOURCES:CREATE" % token, method="POST", body=""
        )

        self.assertEqual(response.code, 200, response.body)
        res = json.loads(response.body)
        self.assertEqual(res["token"] != "", True)
        self.assertEqual(res["name"], "test-datasources-create")
        self.assertEqual(res["scopes"], [{"type": "DATASOURCES:CREATE"}])

    @tornado.testing.gen_test
    async def test__modify_token_with_create_scope(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test_datasources_create_to_modify", scopes.DATASOURCES_CREATE)
        admin_token = Users.get_token_for_scope(u, scopes.ADMIN)
        response = await self.fetch_async(
            f"/v0/tokens/{token}?token={admin_token}&name=test_datasources_create_to_modify_new_name&scope=DATASOURCES:CREATE",
            method="PUT",
            body="",
        )

        self.assertEqual(response.code, 200, response.body)

        t = Users.get_token_access_info(u, token)
        self.assertEqual(t.has_scope(scopes.DATASOURCES_CREATE), True)
        self.assertEqual(t.name, "test_datasources_create_to_modify_new_name")

    @tornado.testing.gen_test
    async def test__drop_resource(self):
        self.create_test_datasource()
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test_resource_drop", None)
        Users.add_scope_to_token(u, token, scopes.DATASOURCES_DROP, "test")
        Users.add_scope_to_token(u, token, scopes.PIPES_DROP, "test_pipe")
        admin_token = Users.get_token_for_scope(u, scopes.ADMIN)

        response = await self.fetch_async(f"/v0/tokens/{token}?token={admin_token}")

        self.assertEqual(response.code, 200, response.body)

        result = json.loads(response.body)
        s = result["scopes"]
        self.assertEqual(len(s), 2)
        self.assertEqual(s[0]["type"], "DATASOURCES:DROP")
        self.assertEqual(s[0]["resource"], "test")
        self.assertEqual(s[1]["type"], "PIPES:DROP")
        self.assertEqual(s[1]["resource"], "test_pipe")

    @tornado.testing.gen_test
    async def test__create_token_without_resource(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        response = await self.fetch_async(
            "/v0/tokens?token=%s&name=test&scope=DATASOURCES:DROP" % token, method="POST", body=""
        )
        res = json.loads(response.body)
        self.assertEqual(response.code, 400)
        self.assertEqual(res["error"], "scope 'DATASOURCES:DROP' requires a resource")

    @tornado.testing.gen_test
    async def test__create_token_with_nonexistent_datasource(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        prev_tokens_count = await self.__get_num_tokens(token)

        response = await self.fetch_async(
            "/v0/tokens?token=%s&name=test&scope=DATASOURCES:READ:nonexistent" % token, method="POST", body=""
        )
        res = json.loads(response.body)
        self.assertEqual(response.code, 400)
        self.assertEqual(res["error"], "datasource or pipe nonexistent does not exist")

        after_tokens_count = await self.__get_num_tokens(token)
        self.assertEqual(prev_tokens_count, after_tokens_count)

    @tornado.testing.gen_test
    async def test__get_token_by_id_or_name(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        admin_token = Users.get_token_for_scope(u, scopes.ADMIN)
        token = Users.add_token(u, "test_name", None)

        response = await self.fetch_async(f"/v0/tokens/test_name?token={admin_token}", method="GET")
        res = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(res["token"], token)

        response = await self.fetch_async(f"/v0/tokens/{token}?token={admin_token}", method="GET")
        res = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(res["name"], "test_name")

    @tornado.testing.gen_test
    async def test__get_other_users_admin_token(self):
        new_name = f"test_33a_{uuid.uuid4().hex}@example.com"
        new_user = UserAccount.register(new_name, "pass")
        self.users_to_delete.append(new_user)

        user = UserAccount.get_by_id(self.USER_ID)
        user_token = UserAccount.get_token_for_scope(user, scopes.AUTH)

        await self.tb_api_proxy.invite_user_to_workspace(user_token, self.WORKSPACE_ID, new_name)

        wk_temp = Users.get_by_id(self.WORKSPACE_ID)

        tokens = [tk for tk in wk_temp.tokens if tk.has_scope(scopes.ADMIN_USER)]

        # Own admin_user token: we can view it
        response = await self.fetch_async(
            "/v0/tokens/%s?token=%s" % (tokens[0].token, tokens[0].token), method="GET", body=None
        )
        self.assertEqual(response.code, 200, response.body)
        response_json = json.loads(response.body)
        self.assertEqual(tokens[0].token, response_json["token"])

        # Other user's admin_user token: we can't view it
        response = await self.fetch_async(
            "/v0/tokens/%s?token=%s" % (tokens[1].token, tokens[0].token), method="GET", body=None
        )
        self.assertEqual(response.code, 200, response.body)
        response_json = json.loads(response.body)
        self.assertNotIn("token", response_json)

    @tornado.testing.gen_test
    async def test__token_scope_cannot_create_token_with_admin_scope(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "tokens_admin", scopes.TOKENS)
        response = await self.fetch_async("/v0/tokens/?token=%s" % token, method="GET")
        self.assertEqual(response.code, 200, response.body)
        prev_tokens_count = await self.__get_num_tokens(token)

        response = await self.fetch_async(
            "/v0/tokens?token=%s&name=test_new_admin&scope=ADMIN" % token, method="POST", body=""
        )
        res = json.loads(response.body)
        self.assertEqual(response.code, 400)
        self.assertEqual(res["error"], "Cannot set ADMIN scope, please provide a different target scope")

        after_tokens_count = await self.__get_num_tokens(token)
        self.assertEqual(prev_tokens_count, after_tokens_count)

    @tornado.testing.gen_test
    async def test__token_scope_cannot_assign_admin_scope(self):
        self.create_test_datasource()
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "tokens_admin", scopes.TOKENS)
        response = await self.fetch_async("/v0/tokens/?token=%s" % token, method="GET")
        self.assertEqual(response.code, 200, response.body)

        response = await self.fetch_async(
            "/v0/tokens?token=%s&name=test_target_token&scope=DATASOURCES:READ:test_table" % token,
            method="POST",
            body="",
        )
        res = json.loads(response.body)

        self.assertEqual(response.code, 200, response.body)
        prev_tokens_count = await self.__get_num_tokens(token)

        response = await self.fetch_async(
            f"/v0/tokens/{token}?token={token}&name=test_target_token&scope=ADMIN", method="PUT", body=""
        )
        res = json.loads(response.body)
        self.assertEqual(response.code, 400)
        self.assertEqual(res["error"], "Cannot set ADMIN scope, please provide a different target scope")

        after_tokens_count = await self.__get_num_tokens(token)
        self.assertEqual(prev_tokens_count, after_tokens_count)

    @tornado.testing.gen_test
    async def test__remove_scopes_if_not_arguments_present(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token_name = "test_scopes_delete"
        token = Users.add_token(u, token_name, scopes.DATASOURCES_CREATE)
        admin_token = Users.get_token_for_scope(u, scopes.ADMIN)
        response = await self.fetch_async(
            f"/v0/tokens/{token}?token={admin_token}&name={token_name}", method="PUT", body=""
        )

        self.assertEqual(response.code, 200, response.body)

        t = Users.get_token_access_info(u, token)
        self.assertEqual(t.has_scope(scopes.DATASOURCES_CREATE), False)

    @tornado.testing.gen_test
    async def test__get_tokens_using_admin_token_with_user_resource(self):
        user = UserAccount.get_by_id(self.USER_ID)
        new_name = f"test_33a_{uuid.uuid4().hex}"
        new_workspace = await self.tb_api_proxy.register_user_and_workspace(f"{new_name}@example.com", new_name)
        self.workspaces_to_delete.append(new_workspace)

        with User.transaction(new_workspace.id) as workspace:
            workspace.add_token("admin-with-user", scopes.ADMIN, user.id)

        # Refresh the workspace instance
        new_workspace = Users.get_by_id(new_workspace.id)

        admin_with_user_token = new_workspace.get_tokens_for_resource(user.id, scopes.ADMIN)[0]
        admin_token = new_workspace.get_token_for_scope(scopes.ADMIN)

        response = await self.fetch_async(f"/v0/tokens?token={admin_with_user_token}", method="GET")
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)

        self.assertEqual(
            next((token["token"] for token in result["tokens"] if token["name"] == "admin token"), None), admin_token
        )

        self.assertEqual(
            next((token["token"] for token in result["tokens"] if token["name"] == "admin-with-user"), None),
            admin_with_user_token,
        )

        response = await self.fetch_async(f"/v0/tokens?token={admin_token}", method="GET")
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        self.assertEqual(len(result["tokens"]), 4)

    @tornado.testing.gen_test
    async def test__cannot_create_a_token_for_a_shared_ds_that_is_not_a_read_scope(self):
        user_account = UserAccount.get_by_id(self.USER_ID)
        user_token = UserAccount.get_token_for_scope(user_account, scopes.AUTH)
        workspace = Users.get_by_id(self.WORKSPACE_ID)
        workspace_token = Users.get_token_for_scope(workspace, scopes.ADMIN)

        extra_workspace_id = (
            await self.tb_api_proxy.create_workspace(user_token, f"extra_workspace_token{uuid.uuid4().hex}")
        )["id"]
        self.workspaces_to_delete.append(Users.get_by_id(extra_workspace_id))
        extra_workspace_token = Users.get_token_for_scope(User.get_by_id(extra_workspace_id), scopes.ADMIN)

        datasource_in_user = await self.tb_api_proxy.create_datasource(
            token=workspace_token, ds_name="datasource_in_user", schema="col_a Int32,col_b Int32,col_c Int32"
        )

        datasource_from_base_in_extra_workspace = await self.tb_api_proxy.share_datasource_with_another_workspace(
            token=user_token,
            datasource_id=datasource_in_user["datasource"]["id"],
            origin_workspace_id=workspace.id,
            destination_workspace_id=extra_workspace_id,
            expect_notification=False,
        )

        async def create_with_scope(scope):
            params = {
                "token": extra_workspace_token,
                "name": "append_to_shared_ds",
                "scope": f"DATASOURCES:{scope}:{datasource_from_base_in_extra_workspace.name}",
            }
            return await self.fetch_async(f"/v0/tokens/?{urlencode(params)}", method="POST", body="")

        response = await create_with_scope("APPEND")
        res = json.loads(response.body)
        self.assertEqual(response.code, 400, res)
        self.assertEqual(
            res["error"],
            f'Data source "{datasource_from_base_in_extra_workspace.name}" is a Shared Data Source. As it\'s read-only, it only supports READ scope tokens.',
        )

        response = await create_with_scope("READ")
        res = json.loads(response.body)
        self.assertEqual(response.code, 200, res)

    @tornado.testing.gen_test
    async def test_token_with_scope_datasources_create_can_append_any_datasource(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token_name = "can_append_any_datasource"
        token = Users.add_token(u, token_name, scopes.DATASOURCES_CREATE, "whatever")

        t = Users.get_token_access_info(u, token)
        self.assertEqual(t.has_scope(scopes.DATASOURCES_CREATE), True, t)
        self.assertEqual(t.scopes[0][1], "whatever", t.__dict__)

        # Even if the token has a resouce defined. A token with scope DATASOURCES_CREATE can append any datasource
        params = {"token": token, "name": "test_table"}
        response = await self.fetch_full_body_upload_async(
            f"/v0/datasources?{urlencode(params)}", CsvIO("1, 1.0, 'one'")
        )
        self.assertEqual(response.code, 200, response.body)

    @tornado.testing.gen_test
    async def test_try_to_create_admin_token_from_admin_token(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        workspace_access_token = Users.get_token_for_scope(u, scopes.ADMIN)
        response = await self.fetch_async(
            "/v0/tokens?token=%s&name=test&scope=ADMIN" % workspace_access_token, method="POST", body=""
        )
        self.assertEqual(response.code, 200)
        res = json.loads(response.body)

        response = await self.fetch_async(f"/v0/tokens?token={workspace_access_token}", method="GET")
        self.assertEqual(response.code, 200)
        res = json.loads(response.body)

        # Check token information from existing admin token
        workspace_access_token = next((t for t in res["tokens"] if t["token"] == workspace_access_token), None)
        self.assertEqual(workspace_access_token["scopes"][0]["type"], "ADMIN")

        # Check token information from new admin token
        new_admin_access_token = next((t for t in res["tokens"] if t["name"] == "test"), None)
        self.assertEqual(new_admin_access_token["scopes"][0]["type"], "ADMIN")
        self.assertEqual(len(res["tokens"]), 4, res)

        # Check that the new token can create a datasource
        response = await self.fetch_full_body_upload_async(
            f"/v0/datasources?token={new_admin_access_token['token']}&name=test_table",
            CsvIO("1, 1.0, 'one'"),
        )
        self.assertEqual(response.code, 200, response.body)


class TestAPITokensWorkspaces(BaseTest):
    def setUp(self):
        super().setUp()
        self.tb_api_proxy = TBApiProxyAsync(self)

    @tornado.testing.gen_test
    async def test__get_user_tokens_admin(self):
        guest_user = UserAccount.get_by_id(self.USER_ID)
        admin_user = UserAccount.register(f"new_user_{uuid.uuid4().hex}@example.com", "pass")
        self.users_to_delete.append(admin_user)

        workspace_name = f"test_{uuid.uuid4().hex}"
        workspace = User.register(workspace_name, admin=admin_user.id)
        self.workspaces_to_delete.append(workspace)

        admin_user_auth = admin_user.get_token_for_scope(scopes.AUTH)

        await self.tb_api_proxy.invite_user_to_workspace(admin_user_auth, workspace.id, guest_user.email)

        # `admin_user` and `guest_user` are workspace members
        response = await self.fetch_async(f"/v0/workspaces/{workspace.id}/tokens?token={admin_user_auth}", method="GET")
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        # Expected 4:
        #  Workspace admin
        #  User admin
        #  Guest admin
        #  Create datasources
        self.assertEqual(len(result["tokens"]), 4)
        non_obfuscated_tokens = [t for t in result["tokens"] if "token" in t]
        self.assertEqual(len(non_obfuscated_tokens), 3)

    @tornado.testing.gen_test
    async def test__get_user_tokens_guest(self):
        guest_user = UserAccount.get_by_id(self.USER_ID)
        admin_user = UserAccount.register(f"new_user_{uuid.uuid4().hex}@example.com", "pass")
        self.users_to_delete.append(admin_user)

        workspace_name = f"test_{uuid.uuid4().hex}"
        workspace = User.register(workspace_name, admin=admin_user.id)
        self.workspaces_to_delete.append(workspace)

        guest_user_auth = guest_user.get_token_for_scope(scopes.AUTH)
        admin_user_auth = admin_user.get_token_for_scope(scopes.AUTH)

        await self.tb_api_proxy.invite_user_to_workspace(admin_user_auth, workspace.id, guest_user.email)

        response = await self.fetch_async(f"/v0/workspaces/{workspace.id}/tokens?token={guest_user_auth}", method="GET")
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        # Expected 2:
        #  Guest admin
        #  Create datasources
        self.assertEqual(len(result["tokens"]), 2)
        non_obfuscated_tokens = [t for t in result["tokens"] if "token" in t]
        self.assertEqual(len(non_obfuscated_tokens), 2)

    @tornado.testing.gen_test
    async def test__get_user_tokens_viewer(self):
        viewer_user = UserAccount.get_by_id(self.USER_ID)
        admin_user = UserAccount.register(f"new_user_{uuid.uuid4().hex}@example.com", "pass")
        self.users_to_delete.append(admin_user)

        workspace_name = f"test_{uuid.uuid4().hex}"
        workspace = User.register(workspace_name, admin=admin_user.id)
        self.workspaces_to_delete.append(workspace)

        viewer_user_auth = viewer_user.get_token_for_scope(scopes.AUTH)
        admin_user_auth = admin_user.get_token_for_scope(scopes.AUTH)

        await self.tb_api_proxy.invite_user_to_workspace(
            admin_user_auth, workspace.id, viewer_user.email, role="viewer"
        )

        response = await self.fetch_async(
            f"/v0/workspaces/{workspace.id}/tokens?token={viewer_user_auth}", method="GET"
        )
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        # Expected 2:
        #  viewer admin + create ds
        self.assertEqual(len(result["tokens"]), 2)
        non_obfuscated_tokens = [t for t in result["tokens"] if "token" in t]
        self.assertEqual(len(non_obfuscated_tokens), 1)

    @tornado.testing.gen_test
    async def test__tokens_from_another_workspace_show_correctly_their_names(self):
        workspace = Users.get_by_id(self.WORKSPACE_ID)

        new_name = f"test_33a_{uuid.uuid4().hex}"
        new_user = UserAccount.register(f"{new_name}@example.com", "pass")
        self.users_to_delete.append(new_user)
        new_workspace = self.register_workspace(new_name, new_user.id)

        Users.add_token(workspace, "admin-ws", scopes.ADMIN, new_user.id)

        admin_token = new_user.get_token_for_scope(scopes.AUTH)

        pipe = Users.add_pipe_sync(
            new_workspace, "pipe_for_my_dashboard", "select * from test_table where city = 'Madrid'"
        )

        my_token_name = "my_token"
        Users.add_token(new_workspace, my_token_name, scopes.PIPES_READ, pipe.id)

        response = await self.fetch_async(f"/v0/workspaces/{new_workspace.id}/tokens?token={admin_token}", method="GET")
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        self.assertEqual(len(result["tokens"]), 4)
        pipe_token = next((token for token in result["tokens"] if token["name"] == "my_token"), None)
        self.assertEqual(pipe_token["scopes"][0]["resource"], "pipe_for_my_dashboard")


class TestAPITokensUserRefresh(BaseTest):
    @tornado.testing.gen_test
    async def test__refresh_token(self):
        u = UserAccount.get_by_id(self.USER_ID)
        old_token = u.get_token_for_scope(scopes.AUTH)

        response = await self.fetch_async(
            "/v0/user/tokens/%s/refresh/?token=%s" % (old_token, old_token), method="POST", body=""
        )
        self.assertEqual(response.code, 200, response.body)
        new_token = json.loads(response.body)
        self.assertNotEqual(old_token, new_token["token"])

        response = await self.fetch_async("/v0/workspaces/%s/tokens?token=%s" % (self.WORKSPACE_ID, old_token))
        self.assertEqual(response.code, 403)

        response = await self.fetch_async("/v0/workspaces/%s/tokens?token=%s" % (self.WORKSPACE_ID, new_token["token"]))
        self.assertEqual(response.code, 200, response.body)


class TestAPIJWTTokens(BaseTest):
    @tornado.testing.gen_test
    async def test_creation_jwt_token(self):
        pipe = Users.add_pipe_sync(self.base_workspace, f"pipe_{uuid.uuid4().hex}", "select 1")
        pipe_node = pipe.pipeline.nodes[0]
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}/nodes/{pipe_node.id}/endpoint?token={self.admin_token}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        future_expire_time = int(time()) + 60
        params = {"token": self.admin_token, "name": "test", "expiration_time": future_expire_time}
        body = json.dumps({"scopes": [{"type": "PIPES:READ", "resource": pipe.name}]})
        response = await self.fetch_async(f"/v0/tokens?{urlencode(params)}", method="POST", body=body)
        res = json.loads(response.body)
        self.assertEqual(response.code, 200, res)
        jwt_token = res["token"]
        self.assertTrue(is_jwt_token(jwt_token))

        # We have permissions to read the pipe
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}.json?token={jwt_token}",
            method="GET",
        )
        self.assertEqual(response.code, 200, response.body)

        # We don't have any token with the same name in the workspace
        response = await self.fetch_async(
            f"/v0/tokens?token={self.admin_token}",
            method="GET",
        )
        res = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        self.assertFalse(any(t["name"] == "test" for t in res["tokens"]), res)

        already_expired_time = int((datetime.now() + timedelta(days=-1)).timestamp())
        params = {"token": self.admin_token, "name": "test", "expiration_time": already_expired_time}
        body = json.dumps({"scopes": [{"type": "PIPES:READ", "resource": pipe.name}]})
        response = await self.fetch_async(f"/v0/tokens?{urlencode(params)}", method="POST", body=body)
        res = json.loads(response.body)
        self.assertEqual(response.code, 400, response.body)
        self.assertEqual(
            res["error"],
            f"The specified expiration time: '{already_expired_time}' is invalid, must be a future unix epoch timestamp indicating the token expiration time",
            res,
        )
        self.assertEqual(
            res["documentation"],
            "https://docs.tinybird.co/api-reference/token-api.html#post--v0-tokens-?",
            res,
        )

    @tornado.testing.gen_test
    async def test_creation_jwt_token_with_fixed_params(self):
        pipe = Users.add_pipe_sync(
            self.base_workspace,
            f"pipe_{uuid.uuid4().hex}",
            """%
                SELECT *
                FROM (
                    SELECT 2 as x
                    UNION ALL
                    SELECT 1 as x
                )
                WHERE {{Int32(col_a)}} = x
            """,
        )
        pipe_node = pipe.pipeline.nodes[0]
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}/nodes/{pipe_node.id}/endpoint?token={self.admin_token}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        future_expire_time = int(time()) + 60
        params = {
            "token": self.admin_token,
            "name": "test",
            "expiration_time": future_expire_time,
        }
        body = json.dumps(
            {
                "scopes": [
                    {
                        "type": "PIPES:READ",
                        "resource": pipe.name,
                        "fixed_params": {"col_a": 2},
                    }
                ]
            }
        )
        response = await self.fetch_async(f"/v0/tokens?{urlencode(params)}", method="POST", body=body)
        res = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        jwt_token = res["token"]
        self.assertTrue(is_jwt_token(jwt_token))

        # We have permissions to read the pipe
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}.json?token={jwt_token}",
            method="GET",
        )
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(json.loads(response.body)["data"], [{"x": 2}])

    @tornado.testing.gen_test
    async def test_generate_jwt_token_without_needing_to_call_tinybird(self):
        pipe = Users.add_pipe_sync(self.base_workspace, f"pipe_{uuid.uuid4().hex}", "select 1")
        pipe_node = pipe.pipeline.nodes[0]
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}/nodes/{pipe_node.id}/endpoint?token={self.admin_token}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        future_expire_time = int(time()) + 60
        params = {"token": self.admin_token, "name": "test", "expiration_time": future_expire_time}
        body = json.dumps({"scopes": [{"type": "PIPES:READ", "resource": pipe.name}]})
        # Generate jwt token using the API
        response = await self.fetch_async(f"/v0/tokens?{urlencode(params)}", method="POST", body=body)
        res = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        jwt_token = res["token"]
        self.assertTrue(is_jwt_token(jwt_token))

        # We have permissions to read the pipe
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}.json?token={jwt_token}",
            method="GET",
        )
        self.assertEqual(response.code, 200, response.body)

        # We can generate a JWT token without using the API
        workspace_access_token = Users.get_token_for_scope(self.base_workspace, scopes.ADMIN)
        info = {
            "workspace_id": self.WORKSPACE_ID,
            "exp": future_expire_time,
            "scopes": [
                {
                    "type": "PIPES:READ",
                    "resource": pipe.name,
                    "fixed_params": "",
                }
            ],
            "name": "jwt_token_alex",
        }
        generated_token = jwt.encode(info, workspace_access_token, algorithm="HS256")
        self.assertTrue(is_jwt_token(generated_token))
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}.json?token={generated_token}",
            method="GET",
        )
        self.assertEqual(response.code, 200, response.body)

        # The fixed params is optional
        workspace_access_token = Users.get_token_for_scope(self.base_workspace, scopes.ADMIN)
        info = {
            "workspace_id": self.WORKSPACE_ID,
            "exp": future_expire_time,
            "scopes": [
                {
                    "type": "PIPES:READ",
                    "resource": pipe.name,
                }
            ],
            "name": "jwt_token_alex",
        }
        generated_token = jwt.encode(info, workspace_access_token, algorithm="HS256")
        self.assertTrue(is_jwt_token(generated_token))
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}.json?token={generated_token}",
            method="GET",
        )
        self.assertEqual(response.code, 200, response.body)

    @tornado.testing.gen_test
    async def test_filter_parameter_of_jwt_token_applied(self):
        pipe = Users.add_pipe_sync(
            self.base_workspace,
            f"pipe_{uuid.uuid4().hex}",
            """%
                SELECT *
                FROM (
                    SELECT 2 as x
                    UNION ALL
                    SELECT 1 as x
                )
                WHERE {{Int32(col_a)}} = x
            """,
        )
        pipe_node = pipe.pipeline.nodes[0]
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}/nodes/{pipe_node.id}/endpoint?token={self.admin_token}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        future_expire_time = int(time()) + 60
        # Filter is not needed to access the pipe if the token has the correct scope
        workspace_access_token = Users.get_token_for_scope(self.base_workspace, scopes.ADMIN)
        info = {
            "workspace_id": self.WORKSPACE_ID,
            "exp": future_expire_time,
            "scopes": [{"type": "PIPES:READ", "resource": pipe.name, "fixed_params": {"col_a": 2}}],
            "name": "jwt_token_alex",
        }
        generated_token = jwt.encode(info, workspace_access_token, algorithm="HS256")
        self.assertTrue(is_jwt_token(generated_token))

        # Filter is applied
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}.json?token={generated_token}",
            method="GET",
        )
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(json.loads(response.body)["data"], [{"x": 2}])

        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}.json?token={generated_token}",
            method="POST",
            body="",
        )
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(json.loads(response.body)["data"], [{"x": 2}])

        # Filter is applied even if we explicitly pass it the same parameter by url
        params = {"token": generated_token}
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}.json?{urlencode(params)}",
            method="GET",
        )
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(json.loads(response.body)["data"], [{"x": 2}])

        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}.json?token={generated_token}",
            method="POST",
            body=json.dumps({"col_a": 1}),
        )
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(json.loads(response.body)["data"], [{"x": 2}])

    @tornado.testing.gen_test
    async def test_jwt_tokens_can_only_read_endpoints(self):
        future_expire_time = int(time()) + 60
        workspace_access_token = Users.get_token_for_scope(self.base_workspace, scopes.ADMIN)
        info = {
            "workspace_id": self.WORKSPACE_ID,
            "exp": future_expire_time,
            "scopes": [{"type": "PIPES:READ"}],
            "name": "jwt_token_alex",
        }
        generated_token = jwt.encode(info, workspace_access_token, algorithm="HS256")
        self.assertTrue(is_jwt_token(generated_token))

        # The token can only be used to read the endpoints
        response = await self.fetch_async(
            f"/v0/pipes?token={generated_token}",
            method="GET",
        )
        self.assertEqual(response.code, 403, response.body)
        content = json.loads(response.body)

        expected_message = f"{INVALID_AUTH_MSG}. Handler APIPipeListHandler does not support JWT tokens"
        self.assertEqual(
            content["error"],
            expected_message,
            content,
        )

        response = await self.fetch_async(
            f"/v0/pipes?token={generated_token}&name=endpoint_errors&sql=select+*+from+tinybird.endpoint_errors+limit+10",
            method="POST",
            body="",
        )
        self.assertEqual(response.code, 403, response.body)
        content = json.loads(response.body)
        expected_message = f"{INVALID_AUTH_MSG}. Handler APIPipeListHandler does not support JWT tokens"
        self.assertEqual(
            content["error"],
            expected_message,
            content,
        )

        params = {"q": "select 1", "token": generated_token}
        response = await self.fetch_async(
            f"/v0/sql?{urlencode(params)}",
            method="GET",
        )
        self.assertEqual(response.code, 403, response.body)
        content = json.loads(response.body)
        expected_message = f"{INVALID_AUTH_MSG}. Handler APIQueryHandler does not support JWT tokens"
        self.assertEqual(
            content["error"],
            expected_message,
            content,
        )

        params = {"token": self.admin_token, "name": "test_table"}
        response = await self.fetch_full_body_upload_async(
            f"/v0/datasources?{urlencode(params)}", CsvIO("1, 1.0, 'one'")
        )
        self.assertEqual(response.code, 200, response.body)

    @tornado.testing.gen_test
    async def test_jwt_tokens_with_scope_for_multiple_endpoints(self):
        pipe1 = Users.add_pipe_sync(self.base_workspace, f"pipe_{uuid.uuid4().hex}", "select 1")
        pipe2 = Users.add_pipe_sync(self.base_workspace, f"pipe_{uuid.uuid4().hex}", "select 2")
        pipe_node1 = pipe1.pipeline.nodes[0]
        pipe_node2 = pipe2.pipeline.nodes[0]
        response = await self.fetch_async(
            f"/v0/pipes/{pipe1.name}/nodes/{pipe_node1.id}/endpoint?token={self.admin_token}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)
        response = await self.fetch_async(
            f"/v0/pipes/{pipe2.name}/nodes/{pipe_node2.id}/endpoint?token={self.admin_token}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        future_expire_time = int(time()) + 60
        params = {"token": self.admin_token, "name": "test", "expiration_time": future_expire_time}
        body = json.dumps(
            {
                "scopes": [
                    {"type": "PIPES:READ", "resource": pipe1.name},
                    {"type": "PIPES:READ", "resource": pipe2.name},
                ]
            }
        )
        response = await self.fetch_async(f"/v0/tokens?{urlencode(params)}", method="POST", body=body)
        res = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)

        # We have permissions to read the pipe1
        response = await self.fetch_async(
            f"/v0/pipes/{pipe1.name}.json?token={res['token']}",
            method="GET",
        )
        self.assertEqual(response.code, 200, response.body)

        # We have permissions to read the pipe2
        response = await self.fetch_async(
            f"/v0/pipes/{pipe2.name}.json?token={res['token']}",
            method="GET",
        )
        self.assertEqual(response.code, 200, response.body)

    @tornado.testing.gen_test
    async def test_jwt_tokens_with_scope_for_multiple_endpoints_with_fixed_params(self):
        pipe1 = Users.add_pipe_sync(
            self.base_workspace,
            f"pipe_{uuid.uuid4().hex}",
            """%
                SELECT *
                FROM (
                    SELECT 2 as x
                    UNION ALL
                    SELECT 1 as x
                )
                WHERE {{Int32(col_a)}} = x
            """,
        )
        pipe2 = Users.add_pipe_sync(
            self.base_workspace,
            f"pipe_{uuid.uuid4().hex}",
            """%
                SELECT *
                FROM (
                    SELECT 2 as x
                    UNION ALL
                    SELECT 1 as x
                )
                WHERE {{Int32(col_a)}} = x
            """,
        )
        pipe_node1 = pipe1.pipeline.nodes[0]
        pipe_node2 = pipe2.pipeline.nodes[0]
        response = await self.fetch_async(
            f"/v0/pipes/{pipe1.name}/nodes/{pipe_node1.id}/endpoint?token={self.admin_token}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)
        response = await self.fetch_async(
            f"/v0/pipes/{pipe2.name}/nodes/{pipe_node2.id}/endpoint?token={self.admin_token}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        future_expire_time = int(time()) + 60
        params = {"token": self.admin_token, "name": "test", "expiration_time": future_expire_time}
        body = json.dumps(
            {
                "scopes": [
                    {
                        "type": "PIPES:READ",
                        "resource": pipe1.name,
                        "fixed_params": {"col_a": 2},
                    },
                    {
                        "type": "PIPES:READ",
                        "resource": pipe2.name,
                        "fixed_params": {"col_a": 1},
                    },
                ]
            }
        )
        response = await self.fetch_async(f"/v0/tokens?{urlencode(params)}", method="POST", body=body)
        res = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)

        # We have permissions to read the pipe1
        response = await self.fetch_async(
            f"/v0/pipes/{pipe1.name}.json?token={res['token']}",
            method="GET",
        )
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(json.loads(response.body)["data"], [{"x": 2}])

        # Try to override the fixed parameter
        response = await self.fetch_async(
            f"/v0/pipes/{pipe1.name}.json?token={res['token']}",
            method="POST",
            body=json.dumps({"col_a": 1}),
        )
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(json.loads(response.body)["data"], [{"x": 2}])

        # We have permissions to read the pipe2
        response = await self.fetch_async(
            f"/v0/pipes/{pipe2.name}.json?token={res['token']}",
            method="GET",
        )
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(json.loads(response.body)["data"], [{"x": 1}])

        # Try to override the fixed parameter
        response = await self.fetch_async(
            f"/v0/pipes/{pipe2.name}.json?token={res['token']}",
            method="POST",
            body=json.dumps({"col_a": 2}),
        )
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(json.loads(response.body)["data"], [{"x": 1}])

    @tornado.testing.gen_test
    async def test_jwt_tokens_using_endpoint_id_instead_of_name(self):
        pipe = Users.add_pipe_sync(self.base_workspace, f"pipe_{uuid.uuid4().hex}", "select 1")
        pipe_node = pipe.pipeline.nodes[0]
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}/nodes/{pipe_node.id}/endpoint?token={self.admin_token}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        future_expire_time = int(time()) + 60

        # Generate jwt token using the API
        params = {"token": self.admin_token, "name": "test", "expiration_time": future_expire_time}
        body = json.dumps({"scopes": [{"type": "PIPES:READ", "resource": pipe.id}]})
        response = await self.fetch_async(f"/v0/tokens?{urlencode(params)}", method="POST", body=body)
        res = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        jwt_token = res["token"]
        self.assertTrue(is_jwt_token(jwt_token))

        # We have permissions to read the pipe
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}.json?token={jwt_token}",
            method="GET",
        )
        self.assertEqual(response.code, 200, response.body)

        # We can generate a JWT token without using the API
        workspace_access_token = Users.get_token_for_scope(self.base_workspace, scopes.ADMIN)
        info = {
            "workspace_id": self.WORKSPACE_ID,
            "exp": future_expire_time,
            "scopes": [
                {
                    "type": "PIPES:READ",
                    "resource": pipe.id,
                }
            ],
            "name": "jwt_token_alex",
        }
        generated_token = jwt.encode(info, workspace_access_token, algorithm="HS256")
        self.assertTrue(is_jwt_token(generated_token))
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}.json?token={generated_token}",
            method="GET",
        )
        self.assertEqual(response.code, 200, response.body)

    @tornado.testing.gen_test
    async def test_using_jwt_token_with_a_workspace_with_a_custom_admin_token(self):
        # Create a new token with ADMIN scope using the API
        u = Users.get_by_id(self.WORKSPACE_ID)
        admin_token = u.get_token_for_scope(scopes.ADMIN)
        response = await self.fetch_async(
            "/v0/tokens?token=%s&name=test&scope=ADMIN" % admin_token, method="POST", body=""
        )
        self.assertEqual(response.code, 200)
        res = json.loads(response.body)

        # Create a jwt token and fetch an endpoint
        pipe = Users.add_pipe_sync(self.base_workspace, f"pipe_{uuid.uuid4().hex}", "select 1")
        pipe_node = pipe.pipeline.nodes[0]
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}/nodes/{pipe_node.id}/endpoint?token={admin_token}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        future_expire_time = int(time()) + 60
        params = {"token": admin_token, "name": "test", "expiration_time": future_expire_time}
        body = json.dumps({"scopes": [{"type": "PIPES:READ", "resource": pipe.name}]})
        response = await self.fetch_async(f"/v0/tokens?{urlencode(params)}", method="POST", body=body)
        res = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        jwt_token = res["token"]
        self.assertTrue(is_jwt_token(jwt_token))

        # We have permissions to read the pipe
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}.json?token={jwt_token}",
            method="GET",
        )
        self.assertEqual(response.code, 200, response.body)

        # We can generate a JWT token without using the API
        workspace_access_token = Users.get_token_for_scope(self.base_workspace, scopes.ADMIN)
        info = {
            "workspace_id": self.WORKSPACE_ID,
            "exp": future_expire_time,
            "scopes": [
                {
                    "type": "PIPES:READ",
                    "resource": pipe.name,
                }
            ],
            "name": "jwt_token_alex",
        }
        generated_token = jwt.encode(info, workspace_access_token, algorithm="HS256")
        self.assertTrue(is_jwt_token(generated_token))
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}.json?token={generated_token}",
            method="GET",
        )
        self.assertEqual(response.code, 200, response.body)

    @tornado.testing.gen_test
    async def test_jwt_token_unauthorize_after_refreshing_admin_token(self):
        pipe = Users.add_pipe_sync(self.base_workspace, f"pipe_{uuid.uuid4().hex}", "select 1")
        pipe_node = pipe.pipeline.nodes[0]
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}/nodes/{pipe_node.id}/endpoint?token={self.admin_token}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        future_expire_time = int(time()) + 60
        params = {"token": self.admin_token, "name": "test", "expiration_time": future_expire_time}
        body = json.dumps({"scopes": [{"type": "PIPES:READ", "resource": pipe.name}]})
        response = await self.fetch_async(f"/v0/tokens?{urlencode(params)}", method="POST", body=body)
        res = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        jwt_token = res["token"]
        self.assertTrue(is_jwt_token(jwt_token))

        # We have permissions to read the pipe
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}.json?token={jwt_token}",
            method="GET",
        )
        self.assertEqual(response.code, 200, response.body)

        # Refresh the admin token
        u = Users.get_by_id(self.WORKSPACE_ID)
        admin_access_token = u.get_access_token_for_scope(scopes.ADMIN)
        response = await self.fetch_async(
            "/v0/tokens/%s/refresh?token=%s" % (admin_access_token.id, admin_access_token.token), method="POST", body=""
        )
        self.assertEqual(response.code, 200, response.body)
        content = json.loads(response.body)
        new_admin_token = content["token"]

        # We don't have permissions to read the pipe anymore
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}.json?token={jwt_token}",
            method="GET",
        )
        self.assertEqual(response.code, 403, response.body)

        # We can generate a new JWT token with the new admin token without using the API
        info = {
            "workspace_id": self.WORKSPACE_ID,
            "exp": future_expire_time,
            "scopes": [
                {
                    "type": "PIPES:READ",
                    "resource": pipe.name,
                }
            ],
            "name": "jwt_token_alex",
        }
        generated_token = jwt.encode(info, new_admin_token, algorithm="HS256")
        self.assertTrue(is_jwt_token(generated_token))
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}.json?token={generated_token}",
            method="GET",
        )
        self.assertEqual(response.code, 200, response.body)

    @tornado.testing.gen_test
    async def test_token_with_tokens_scope_can_not_generate_jwt_token(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        admin_token = u.get_token_for_scope(scopes.ADMIN)
        response = await self.fetch_async(
            "/v0/tokens?token=%s&name=test&scope=TOKENS" % admin_token, method="POST", body=""
        )
        self.assertEqual(response.code, 200, response.body)
        res = json.loads(response.body)
        new_token = res["token"]

        # Generate jwt token using the API and the new token
        pipe = Users.add_pipe_sync(self.base_workspace, f"pipe_{uuid.uuid4().hex}", "select 1")

        future_expire_time = int(time()) + 60
        params = {"token": new_token, "name": "test", "expiration_time": future_expire_time}
        body = json.dumps({"scopes": [{"type": "PIPES:READ", "resource": pipe.name}]})
        response = await self.fetch_async(f"/v0/tokens?{urlencode(params)}", method="POST", body=body)
        res = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        jwt_token = res["token"]
        self.assertTrue(is_jwt_token(jwt_token))

    @tornado.testing.gen_test
    async def test_trying_to_delete_a_datasource(self):
        # Let's create a datasource using the admin token
        params = {"token": self.admin_token, "name": "test_table"}
        response = await self.fetch_full_body_upload_async(
            f"/v0/datasources?{urlencode(params)}", CsvIO("1, 1.0, 'one'")
        )
        self.assertEqual(response.code, 200, response.body)

        # We can generate a new JWT token without `exp` claim
        info = {
            "workspace_id": self.WORKSPACE_ID,
            "scopes": [
                {
                    "type": "DATASOURCES:CREATE",
                    "resource": "test_table",
                }
            ],
            "name": "temporal_token_alex",
        }
        generated_token = jwt.encode(info, self.admin_token, algorithm="HS256")
        self.assertTrue(is_jwt_token(generated_token))

        # We can't use the token to delete a datasource
        params = {"token": generated_token}
        response = await self.fetch_async(
            f"/v0/datasources/test_tables/delete?{urlencode(params)}", method="POST", body=""
        )
        self.assertEqual(response.code, 403, response.body)
        content = json.loads(response.body)
        self.assertEqual(content["error"], "JWT tokens is missing the 'exp' claim", content)

        # We generate a new JWT token with the `exp` claim
        info = {
            "workspace_id": self.WORKSPACE_ID,
            "exp": int(time()) + 60,
            "scopes": [
                {
                    "type": "DATASOURCES:CREATE",
                    "resource": "test_table",
                }
            ],
            "name": "temporal_token_alex",
        }
        generated_token = jwt.encode(info, self.admin_token, algorithm="HS256")
        self.assertTrue(is_jwt_token(generated_token))

        # Even with the `exp` claim we can't use the token to delete a datasource
        params = {"token": generated_token}
        response = await self.fetch_async(
            f"/v0/datasources/test_table/delete?{urlencode(params)}", method="POST", body=""
        )
        self.assertEqual(response.code, 403, response.body)

    @tornado.testing.gen_test
    async def test_jwt_token_with_qps_limit(self):
        pipe = Users.add_pipe_sync(self.base_workspace, f"pipe_{uuid.uuid4().hex}", "select 1")
        pipe_node = pipe.pipeline.nodes[0]
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}/nodes/{pipe_node.id}/endpoint?token={self.admin_token}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        future_expire_time = int(time()) + 60
        params = {"token": self.admin_token, "name": "test", "expiration_time": future_expire_time}
        body = json.dumps({"scopes": [{"type": "PIPES:READ", "resource": pipe.name}], "limits": {"rps": 1}})
        response = await self.fetch_async(f"/v0/tokens?{urlencode(params)}", method="POST", body=body)
        res = json.loads(response.body)
        self.assertEqual(response.code, 200, res)
        jwt_token = res["token"]
        self.assertTrue(is_jwt_token(jwt_token))

        response = await self.fetch_async(f"/v0/pipes/{pipe.name}.json?token={jwt_token}", method="GET")
        self.assertEqual(response.code, 200, response)

        # Run 10 requests using a loop and detect if any request returns a 429
        tasks = [self.fetch_async(f"/v0/pipes/{pipe.name}.json?token={jwt_token}", method="GET") for _ in range(10)]

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        # Check if any response returns a 429
        self.assertTrue(
            any(response.code == 429 for response in responses if not isinstance(response, Exception)), responses
        )

    @tornado.testing.gen_test
    async def test_jwt_token_with_qps_limit_using_post(self):
        pipe = Users.add_pipe_sync(
            self.base_workspace, f"pipe_{uuid.uuid4().hex}", "% select {{Int32(param, 1)}} as result"
        )
        pipe_node = pipe.pipeline.nodes[0]
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}/nodes/{pipe_node.id}/endpoint?token={self.admin_token}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        future_expire_time = int(time()) + 60
        params = {"token": self.admin_token, "name": "test", "expiration_time": future_expire_time}
        body = json.dumps(
            {
                "scopes": [{"type": "PIPES:READ", "resource": pipe.name, "fixed_params": {"param": 42}}],
                "limits": {"rps": 1},
            }
        )
        response = await self.fetch_async(f"/v0/tokens?{urlencode(params)}", method="POST", body=body)
        res = json.loads(response.body)
        self.assertEqual(response.code, 200, res)
        jwt_token = res["token"]
        self.assertTrue(is_jwt_token(jwt_token))

        # Test a single POST request
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}.json?token={jwt_token}", method="POST", body=json.dumps({"param": 100})
        )
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        self.assertEqual(result["data"], [{"result": 42}])  # Should always be 42 due to fixed parameter

        # Run 10 POST requests using a loop and detect if any request returns a 429
        tasks = [
            self.fetch_async(
                f"/v0/pipes/{pipe.name}.json?token={jwt_token}", method="POST", body=json.dumps({"param": i})
            )
            for i in range(10)
        ]

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        # Check if any response returns a 429
        self.assertTrue(
            any(response.code == 429 for response in responses if not isinstance(response, Exception)),
            f"Expected at least one 429 response, but got: {[r.code for r in responses if not isinstance(r, Exception)]}",
        )

        # Verify that at least one request succeeded
        successful_responses = [r for r in responses if not isinstance(r, Exception) and r.code == 200]
        self.assertTrue(len(successful_responses) > 0, "Expected at least one successful request")

        # Verify the content of all successful responses
        for response in successful_responses:
            content = json.loads(response.body)
            self.assertIn("data", content)
            self.assertEqual(len(content["data"]), 1)
            self.assertIn("result", content["data"][0])
            self.assertEqual(content["data"][0]["result"], 42)  # Should always be 42 due to fixed parameter

    @tornado.testing.gen_test
    async def test_jwt_token_without_qps_limit(self):
        pipe = Users.add_pipe_sync(self.base_workspace, f"pipe_{uuid.uuid4().hex}", "select 1")
        pipe_node = pipe.pipeline.nodes[0]
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}/nodes/{pipe_node.id}/endpoint?token={self.admin_token}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        future_expire_time = int(time()) + 60
        params = {"token": self.admin_token, "name": "test", "expiration_time": future_expire_time}
        body = json.dumps({"scopes": [{"type": "PIPES:READ", "resource": pipe.name}]})
        response = await self.fetch_async(f"/v0/tokens?{urlencode(params)}", method="POST", body=body)
        res = json.loads(response.body)
        self.assertEqual(response.code, 200, res)
        jwt_token = res["token"]
        self.assertTrue(is_jwt_token(jwt_token))

        # Multiple requests should succeed without QPS limit
        tasks = [
            self.fetch_async(
                f"/v0/pipes/{pipe.name}.json?token={jwt_token}",
                method="GET",
            )
            for _ in range(5)
        ]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        self.assertTrue(all(response.code == 200 for response in responses), responses)

    @tornado.testing.gen_test
    async def test_jwt_token_with_and_without_qps_limit(self):
        pipe = Users.add_pipe_sync(self.base_workspace, f"pipe_{uuid.uuid4().hex}", "select 1")
        pipe_node = pipe.pipeline.nodes[0]
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}/nodes/{pipe_node.id}/endpoint?token={self.admin_token}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        future_expire_time = int(time()) + 60

        # Create token with QPS limit
        params = {"token": self.admin_token, "name": "test_with_limit", "expiration_time": future_expire_time}
        body = json.dumps({"scopes": [{"type": "PIPES:READ", "resource": pipe.name}], "limits": {"rps": 1}})
        response = await self.fetch_async(f"/v0/tokens?{urlencode(params)}", method="POST", body=body)
        res = json.loads(response.body)
        self.assertEqual(response.code, 200, res)
        jwt_token_with_limit = res["token"]
        self.assertTrue(is_jwt_token(jwt_token_with_limit))

        # Create token without QPS limit
        params = {"token": self.admin_token, "name": "test_without_limit", "expiration_time": future_expire_time}
        body = json.dumps({"scopes": [{"type": "PIPES:READ", "resource": pipe.name}]})
        response = await self.fetch_async(f"/v0/tokens?{urlencode(params)}", method="POST", body=body)
        res = json.loads(response.body)
        self.assertEqual(response.code, 200, res)
        jwt_token_without_limit = res["token"]
        self.assertTrue(is_jwt_token(jwt_token_without_limit))

        # Run 10 requests using both tokens concurrently
        tasks_with_limit = [
            self.fetch_async(f"/v0/pipes/{pipe.name}.json?token={jwt_token_with_limit}", method="GET")
            for _ in range(10)
        ]
        tasks_without_limit = [
            self.fetch_async(f"/v0/pipes/{pipe.name}.json?token={jwt_token_without_limit}", method="GET")
            for _ in range(10)
        ]

        responses_with_limit = await asyncio.gather(*tasks_with_limit, return_exceptions=True)
        responses_without_limit = await asyncio.gather(*tasks_without_limit, return_exceptions=True)

        # Check if any response with limit returns a 429
        self.assertTrue(
            any(response.code == 429 for response in responses_with_limit if not isinstance(response, Exception)),
            responses_with_limit,
        )

        # Check if all responses without limit are 200
        self.assertTrue(
            all(response.code == 200 for response in responses_without_limit if not isinstance(response, Exception)),
            responses_without_limit,
        )

    @tornado.testing.gen_test
    async def test_jwt_token_with_high_rps_limit(self):
        pipe = Users.add_pipe_sync(self.base_workspace, f"pipe_{uuid.uuid4().hex}", "select 1")
        pipe_node = pipe.pipeline.nodes[0]
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}/nodes/{pipe_node.id}/endpoint?token={self.admin_token}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        future_expire_time = int(time()) + 60

        # Create token with QPS limit of 1
        params = {"token": self.admin_token, "name": "test_with_limit", "expiration_time": future_expire_time}
        body = json.dumps({"scopes": [{"type": "PIPES:READ", "resource": pipe.name}], "limits": {"rps": 1}})
        response = await self.fetch_async(f"/v0/tokens?{urlencode(params)}", method="POST", body=body)
        res = json.loads(response.body)
        self.assertEqual(response.code, 200, res)
        jwt_token_with_limit = res["token"]
        self.assertTrue(is_jwt_token(jwt_token_with_limit))

        # Create token with QPS limit of 200
        params = {"token": self.admin_token, "name": "test_with_high_limit", "expiration_time": future_expire_time}
        body = json.dumps({"scopes": [{"type": "PIPES:READ", "resource": pipe.name}], "limits": {"rps": 200}})
        response = await self.fetch_async(f"/v0/tokens?{urlencode(params)}", method="POST", body=body)
        res = json.loads(response.body)
        self.assertEqual(response.code, 200, res)
        jwt_token_with_high_limit = res["token"]
        self.assertTrue(is_jwt_token(jwt_token_with_high_limit))

        # Run 10 requests using both tokens concurrently
        tasks_with_limit = [
            self.fetch_async(f"/v0/pipes/{pipe.name}.json?token={jwt_token_with_limit}", method="GET")
            for _ in range(10)
        ]
        tasks_with_high_limit = [
            self.fetch_async(f"/v0/pipes/{pipe.name}.json?token={jwt_token_with_high_limit}", method="GET")
            for _ in range(10)
        ]

        responses_with_limit = await asyncio.gather(*tasks_with_limit, return_exceptions=True)
        responses_with_high_limit = await asyncio.gather(*tasks_with_high_limit, return_exceptions=True)

        # Check if any response with limit returns a 429
        self.assertTrue(
            any(response.code == 429 for response in responses_with_limit if not isinstance(response, Exception)),
            responses_with_limit,
        )

        # Check if all responses with high limit are 200
        self.assertTrue(
            all(response.code == 200 for response in responses_with_high_limit if not isinstance(response, Exception)),
            responses_with_high_limit,
        )

    @tornado.testing.gen_test
    async def test_jwt_token_with_qps_limit_direct_generation(self):
        pipe = Users.add_pipe_sync(self.base_workspace, f"pipe_{uuid.uuid4().hex}", "select 1")
        pipe_node = pipe.pipeline.nodes[0]
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}/nodes/{pipe_node.id}/endpoint?token={self.admin_token}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        future_expire_time = int(time()) + 60

        # Generate JWT token directly
        workspace_access_token = Users.get_token_for_scope(self.base_workspace, scopes.ADMIN)
        info = {
            "workspace_id": self.WORKSPACE_ID,
            "exp": future_expire_time,
            "scopes": [
                {
                    "type": "PIPES:READ",
                    "resource": pipe.name,
                }
            ],
            "limits": {
                "rps": 1,
            },
            "name": "jwt_token_alex",
        }
        jwt_token = jwt.encode(info, workspace_access_token, algorithm="HS256")
        self.assertTrue(is_jwt_token(jwt_token))

        response = await self.fetch_async(f"/v0/pipes/{pipe.name}.json?token={jwt_token}", method="GET")
        self.assertEqual(response.code, 200, response)

        # Run 10 requests using a loop and detect if any request returns a 429
        tasks = [self.fetch_async(f"/v0/pipes/{pipe.name}.json?token={jwt_token}", method="GET") for _ in range(10)]

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        # Check if any response returns a 429
        self.assertTrue(
            any(response.code == 429 for response in responses if not isinstance(response, Exception)), responses
        )

    @tornado.testing.gen_test
    async def test_endpoint_replace_parameters(self):
        datasource_name = f"datasource_{uuid.uuid4().hex}"
        params = {
            "name": datasource_name,
            "schema": "`click_time` DateTime64(3) `json:$.click_time`,`correct` UInt8 `json:$.correct`,`duration` Int32 `json:$.duration`,`event_type` String `json:$.event_type`,`game_id` String `json:$.game_id`,`start_time` DateTime64(3) `json:$.start_time`,`target_index` Int16 `json:$.target_index`,`timestamp` DateTime64(3) `json:$.timestamp`,`username` String `json:$.username`",
            "engine": "MergeTree",
            "engine_partition_key": "toYear(click_time)",
            "engine_sorting_key": "click_time, game_id, target_index, username",
            "token": self.admin_token,
            "format": "ndjson",
        }
        response = await self.fetch_async(f"/v0/datasources?{urlencode(params)}", method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        pipe = Users.add_pipe_sync(
            self.base_workspace,
            f"pipe_{uuid.uuid4().hex}",
            """%
            SELECT
            duration
            FROM """
            + datasource_name
            + """
            WHERE username = {{String(user)}}
            AND correct = 1
            ORDER BY duration ASC limit 1
            """,
        )
        pipe_node = pipe.pipeline.nodes[0]
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}/nodes/{pipe_node.id}/endpoint?token={self.admin_token}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        # Generate JWT token directly
        future_expire_time = int(time()) + 60
        workspace_access_token = Users.get_token_for_scope(self.base_workspace, scopes.ADMIN)
        info = {
            "workspace_id": self.WORKSPACE_ID,
            "exp": future_expire_time,
            "scopes": [{"type": "PIPES:READ", "resource": pipe.name, "fixed_params": {"user": "hello"}}],
            "name": "jwt_token_alex",
        }
        jwt_token = jwt.encode(info, workspace_access_token, algorithm="HS256")
        self.assertTrue(is_jwt_token(jwt_token))
        response = await asyncio.to_thread(
            requests.get, self.get_url(f"/v0/pipes/{pipe.name}.json?token={jwt_token}", clean_params=True)
        )
        self.assertEqual(response.status_code, 200, response)

        span_logs = await self.get_span_async(response.url)
        span_log_tags = json.loads(span_logs["tags"])
        self.assertEqual(span_log_tags.get("parameters", {}).get("user"), "hello", span_log_tags)

        response = await asyncio.to_thread(
            requests.post, self.get_url(f"/v0/pipes/{pipe.name}.json?token={jwt_token}", clean_params=True)
        )
        self.assertEqual(response.status_code, 200, response)

    @tornado.testing.gen_test
    async def test_we_not_validate_iat_claim(self):
        pipe = Users.add_pipe_sync(self.base_workspace, f"pipe_{uuid.uuid4().hex}", "select 1")
        pipe_node = pipe.pipeline.nodes[0]
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}/nodes/{pipe_node.id}/endpoint?token={self.admin_token}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        future_expire_time = int(time()) + 60

        # IAT is less than the exp claim, but more than current time
        workspace_access_token = Users.get_token_for_scope(self.base_workspace, scopes.ADMIN)
        info = {
            "workspace_id": self.WORKSPACE_ID,
            "exp": future_expire_time,
            "iat": future_expire_time - 1,
            "scopes": [
                {
                    "type": "PIPES:READ",
                    "resource": pipe.name,
                }
            ],
            "name": "jwt_token_alex",
        }
        jwt_token = jwt.encode(info, workspace_access_token, algorithm="HS256")
        self.assertTrue(is_jwt_token(jwt_token))

        response = await self.fetch_async(f"/v0/pipes/{pipe.name}.json?token={jwt_token}", method="GET")
        self.assertEqual(response.code, 200, response)

        # IAT is greater than current time
        workspace_access_token = Users.get_token_for_scope(self.base_workspace, scopes.ADMIN)
        info = {
            "workspace_id": self.WORKSPACE_ID,
            "exp": future_expire_time,
            "iat": int(time()) + 1,
            "scopes": [
                {
                    "type": "PIPES:READ",
                    "resource": pipe.name,
                }
            ],
            "name": "jwt_token_alex",
        }
        jwt_token = jwt.encode(info, workspace_access_token, algorithm="HS256")
        self.assertTrue(is_jwt_token(jwt_token))

        response = await self.fetch_async(f"/v0/pipes/{pipe.name}.json?token={jwt_token}", method="GET")
        self.assertEqual(response.code, 200, response)


class TestAPITokensUser(BaseTest):
    _mock_access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    maxDiff = None

    def setUp(self):
        super().setUp()
        APITokensUserHandler._auth0_user_info_cache = {}

    def assert_result(self, result, expected):
        result = {
            "user_token": result["user_token"],
            "workspace_token": result["workspace_token"],
            "workspace_id": result["workspace_id"],
            "workspace_name": result["workspace_name"],
        }
        self.assertEqual(result, expected)

    @tornado.testing.gen_test
    @patch("tornado.auth.OAuth2Mixin.get_auth_http_client")
    async def test__get_user_and_workspace_tokens(self, mock_get_auth_http_client):
        new_name = f"test_33a_{uuid.uuid4().hex}"
        user = UserAccount.register(f"{new_name}@example.com", "pass")
        self.users_to_delete.append(user)
        workspace = self.register_workspace(new_name, user.id)
        mock_http_client = AsyncMock()
        mock_get_auth_http_client.return_value = mock_http_client
        mock_response = AsyncMock()
        mock_response.code = 200
        mock_response.body = json.dumps({"email": user.email})
        mock_http_client.fetch.return_value = mock_response
        workspace_token = workspace.get_workspace_access_token(user.id)
        user_token = user.get_token_for_scope(scopes.AUTH)
        response = await self.fetch_async("/v0/user/tokens?token=%s" % self._mock_access_token, method="GET")
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assert_result(
            result,
            {
                "user_token": user_token,
                "workspace_token": workspace_token,
                "workspace_id": workspace.id,
                "workspace_name": workspace.name,
            },
        )

    @tornado.testing.gen_test
    @patch("tornado.auth.OAuth2Mixin.get_auth_http_client")
    async def test__get_user_and_workspace_tokens_with_wrong_workspace_id(self, mock_get_auth_http_client):
        new_name = f"test_33a_{uuid.uuid4().hex}"
        user = UserAccount.register(f"{new_name}@example.com", "pass")
        self.users_to_delete.append(user)
        mock_http_client = AsyncMock()
        mock_get_auth_http_client.return_value = mock_http_client
        mock_response = AsyncMock()
        mock_response.code = 200
        mock_response.body = json.dumps({"email": user.email})
        mock_http_client.fetch.return_value = mock_response
        response = await self.fetch_async(
            f"/v0/user/tokens?token={self._mock_access_token}&workspace_id=non_existing_workspace_id", method="GET"
        )
        self.assertEqual(response.code, 404)
        result = json.loads(response.body)
        self.assertEqual(result["error"], "Workspace not found")

    @tornado.testing.gen_test
    @patch("tornado.auth.OAuth2Mixin.get_auth_http_client")
    async def test__get_user_and_workspace_tokens_with_other_user_workspace_id(self, mock_get_auth_http_client):
        user = UserAccount.register(f"user_{uuid.uuid4().hex}@example.com", "pass")
        self.users_to_delete.append(user)

        workspace_name = f"test_{uuid.uuid4().hex}"
        workspace = self.register_workspace(workspace_name, user.id)

        mock_http_client = AsyncMock()
        mock_get_auth_http_client.return_value = mock_http_client
        mock_response = AsyncMock()
        mock_response.code = 200
        mock_response.body = json.dumps({"email": user.email})
        mock_http_client.fetch.return_value = mock_response
        workspace_token = workspace.get_workspace_access_token(user.id)
        user_token = user.get_token_for_scope(scopes.AUTH)
        response = await self.fetch_async(
            f"/v0/user/tokens?token={self._mock_access_token}&workspace_id={workspace.id}", method="GET"
        )

        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assert_result(
            result,
            {
                "user_token": user_token,
                "workspace_token": workspace_token,
                "workspace_id": workspace.id,
                "workspace_name": workspace.name,
            },
        )

        other_user = UserAccount.register(f"other_user_{uuid.uuid4().hex}@example.com", "pass")
        self.users_to_delete.append(other_user)

        other_workspace_name = f"test_{uuid.uuid4().hex}"
        other_workspace = self.register_workspace(other_workspace_name, other_user.id)

        other_response = await self.fetch_async(
            f"/v0/user/tokens?token={self._mock_access_token}&workspace_id={other_workspace.id}", method="GET"
        )

        self.assertEqual(other_response.code, 404)
        other_result = json.loads(other_response.body)
        self.assertEqual(other_result["error"], "Workspace not found")

    @tornado.testing.gen_test
    @patch("tornado.auth.OAuth2Mixin.get_auth_http_client")
    async def test__get_user_and_workspace_tokens_with_existing_workspace_id(self, mock_get_auth_http_client):
        new_name = f"test_33a_{uuid.uuid4().hex}"
        user = UserAccount.register(f"{new_name}@example.com", "pass")
        self.users_to_delete.append(user)
        workspace = self.register_workspace(new_name, user.id)
        mock_http_client = AsyncMock()
        mock_get_auth_http_client.return_value = mock_http_client
        mock_response = AsyncMock()
        mock_response.code = 200
        mock_response.body = json.dumps({"email": user.email})
        mock_http_client.fetch.return_value = mock_response
        workspace_token = workspace.get_workspace_access_token(user.id)
        user_token = user.get_token_for_scope(scopes.AUTH)
        response = await self.fetch_async(
            f"/v0/user/tokens?token={self._mock_access_token}&workspace_id={workspace.id}", method="GET"
        )
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assert_result(
            result,
            {
                "user_token": user_token,
                "workspace_token": workspace_token,
                "workspace_id": workspace.id,
                "workspace_name": workspace.name,
            },
        )

    @tornado.testing.gen_test
    @patch("tornado.auth.OAuth2Mixin.get_auth_http_client")
    async def test__get_user_and_workspace_tokens_with_not_verified_email(self, mock_get_auth_http_client):
        new_name = f"test_33a_{uuid.uuid4().hex}"
        user = UserAccount.register(f"{new_name}@example.com", "pass")
        self.users_to_delete.append(user)
        mock_http_client = AsyncMock()
        mock_get_auth_http_client.return_value = mock_http_client
        mock_response = AsyncMock()
        mock_response.code = 200
        mock_response.body = json.dumps({"email": user.email, "email_verified": False})
        mock_http_client.fetch.return_value = mock_response
        response = await self.fetch_async(f"/v0/user/tokens?token={self._mock_access_token}", method="GET")
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertEqual(
            result,
            {
                "workspace_token": None,
                "user_token": None,
                "workspace_id": None,
                "workspace_name": None,
                "email_verified": False,
            },
        )

    @tornado.testing.gen_test
    @patch("tornado.auth.OAuth2Mixin.get_auth_http_client")
    async def test__get_user_and_workspace_tokens_with_different_email_and_non_tinybird_member(
        self, mock_get_auth_http_client
    ):
        mock_http_client = AsyncMock()
        mock_get_auth_http_client.return_value = mock_http_client
        mock_response = AsyncMock()
        mock_response.code = 200
        mock_response.body = json.dumps({"email": "hey@gmail.com"})
        mock_http_client.fetch.return_value = mock_response
        response = await self.fetch_async(
            f"/v0/user/tokens?token={self._mock_access_token}&email=hey@tinybird.co", method="GET"
        )
        self.assertEqual(response.code, 401)

    @tornado.testing.gen_test
    @patch("tornado.auth.OAuth2Mixin.get_auth_http_client")
    async def test__get_user_and_workspace_tokens_with_different_email_and_tinybird_member(
        self, mock_get_auth_http_client
    ):
        new_name = f"test_33a_{uuid.uuid4().hex}"
        user = UserAccount.register(f"{new_name}@example.com", "pass")
        self.users_to_delete.append(user)
        workspace = self.register_workspace(new_name, user.id)
        mock_http_client = AsyncMock()
        mock_get_auth_http_client.return_value = mock_http_client
        mock_response = AsyncMock()
        mock_response.code = 200
        tinybird_user_email = f"test_user_tokens_{uuid.uuid4().hex}@tinybird.co"
        tinybird_user = UserAccount.register(tinybird_user_email, "pass")
        self.users_to_delete.append(tinybird_user)
        mock_response.body = json.dumps({"email": tinybird_user_email})
        mock_http_client.fetch.return_value = mock_response
        response = await self.fetch_async(
            f"/v0/user/tokens?token={self._mock_access_token}&email={user.email}", method="GET"
        )
        result = json.loads(response.body)
        workspace_token = workspace.get_workspace_access_token(user.id)
        user_token = user.get_token_for_scope(scopes.AUTH)
        self.assertEqual(response.code, 200)
        self.assert_result(
            result,
            {
                "user_token": user_token,
                "workspace_token": workspace_token,
                "workspace_id": workspace.id,
                "workspace_name": workspace.name,
            },
        )

    @tornado.testing.gen_test
    @patch("tornado.auth.OAuth2Mixin.get_auth_http_client")
    async def test__get_user_and_workspace_tokens_with_cache(self, mock_get_auth_http_client):
        new_name = f"test_33a_{uuid.uuid4().hex}"
        user = UserAccount.register(f"{new_name}@example.com", "pass")
        self.users_to_delete.append(user)
        workspace = self.register_workspace(new_name, user.id)
        mock_http_client = AsyncMock()
        mock_get_auth_http_client.return_value = mock_http_client
        mock_response = AsyncMock()
        mock_response.code = 200
        mock_response.body = json.dumps({"email": user.email})
        mock_http_client.fetch.return_value = mock_response
        workspace_token = workspace.get_workspace_access_token(user.id)
        user_token = user.get_token_for_scope(scopes.AUTH)
        response = await self.fetch_async("/v0/user/tokens?token=%s" % self._mock_access_token, method="GET")
        result = json.loads(response.body)
        self.assert_result(
            result,
            {
                "user_token": user_token,
                "workspace_token": workspace_token,
                "workspace_id": workspace.id,
                "workspace_name": workspace.name,
            },
        )
        response = await self.fetch_async("/v0/user/tokens?token=%s" % self._mock_access_token, method="GET")
        result = json.loads(response.body)
        self.assert_result(
            result,
            {
                "user_token": user_token,
                "workspace_token": workspace_token,
                "workspace_id": workspace.id,
                "workspace_name": workspace.name,
            },
        )
        mock_http_client.fetch.assert_called_once()

    @tornado.testing.gen_test
    @patch("tornado.auth.OAuth2Mixin.get_auth_http_client")
    async def test__get_user_and_workspace_tokens_with_cache_not_verified_email(self, mock_get_auth_http_client):
        new_name = f"test_33a_{uuid.uuid4().hex}"
        user = UserAccount.register(f"{new_name}@example.com", "pass")
        self.users_to_delete.append(user)
        workspace = self.register_workspace(new_name, user.id)
        mock_http_client = AsyncMock()
        mock_get_auth_http_client.return_value = mock_http_client
        mock_response = AsyncMock()
        mock_response.code = 200
        mock_response.body = json.dumps({"email": user.email, "email_verified": False})
        mock_http_client.fetch.return_value = mock_response
        response = await self.fetch_async(f"/v0/user/tokens?token={self._mock_access_token}", method="GET")
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertEqual(
            result,
            {
                "workspace_token": None,
                "user_token": None,
                "workspace_id": None,
                "workspace_name": None,
                "email_verified": False,
            },
        )
        mock_response.body = json.dumps({"email": user.email})
        mock_http_client.fetch.return_value = mock_response
        workspace_token = workspace.get_workspace_access_token(user.id)
        user_token = user.get_token_for_scope(scopes.AUTH)
        response = await self.fetch_async("/v0/user/tokens?token=%s" % self._mock_access_token, method="GET")
        result = json.loads(response.body)
        self.assert_result(
            result,
            {
                "user_token": user_token,
                "workspace_token": workspace_token,
                "workspace_id": workspace.id,
                "workspace_name": workspace.name,
            },
        )
        self.assertEqual(mock_http_client.fetch.call_count, 2)

    @tornado.testing.gen_test
    @patch("tornado.auth.OAuth2Mixin.get_auth_http_client")
    async def test__get_user_and_workspace_tokens_with_no_workspaces_created(self, mock_get_auth_http_client):
        new_name = f"test_33a_{uuid.uuid4().hex}"
        user = UserAccount.register(f"{new_name}@example.com", "pass")
        self.users_to_delete.append(user)
        mock_http_client = AsyncMock()
        mock_get_auth_http_client.return_value = mock_http_client
        mock_response = AsyncMock()
        mock_response.code = 200
        mock_response.body = json.dumps({"email": user.email})
        mock_http_client.fetch.return_value = mock_response
        user_token = user.get_token_for_scope(scopes.AUTH)
        response = await self.fetch_async(f"/v0/user/tokens?token={self._mock_access_token}", method="GET")
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assert_result(
            result,
            {"user_token": user_token, "workspace_token": None, "workspace_id": None, "workspace_name": None},
        )
