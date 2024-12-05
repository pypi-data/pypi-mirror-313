import json
import logging
from typing import Any, Dict, List

from tornado.web import create_signed_value

from tinybird.token_scope import scopes
from tinybird.user import UserAccounts
from tinybird.user import Users as Workspaces
from tinybird.views.base import INVALID_AUTH_MSG

from .base_test import BaseTest


class TestAPIAuthentication(BaseTest):
    urls = [
        ["/sql", "q", "select+count()+c+from+test_table"],
        ["/datasources"],
        ["/pipes"],
        ["/tokens"],
    ]

    def setUp(self):
        super().setUp()
        self.u = Workspaces.get_by_id(self.WORKSPACE_ID)
        self.admin_token = Workspaces.get_token_for_scope(self.u, scopes.ADMIN)
        self.admin_user_token = Workspaces.get_token_for_scope(self.u, scopes.ADMIN_USER)

    def __get_api_url(self, url_parts):
        partial_path, *_ = url_parts
        parameters = "&".join(["=".join(x) for x in zip(_[::2], _[1::2])])
        return f"/v0{partial_path}?{parameters}"

    def test_header_auth(self):
        self.create_test_datasource()
        for url_parts in self.urls:
            url = self.__get_api_url(url_parts)
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = self.fetch(url, headers=headers)
            self.assertEqual(response.code, 200)

    def test_parameter_auth(self):
        self.create_test_datasource()
        for url_parts in self.urls:
            url = self.__get_api_url([*url_parts, "token", self.admin_token])
            response = self.fetch(url)
            self.assertEqual(response.code, 200)

    def test_non_auth(self):
        self.create_test_datasource()
        for url_parts in self.urls:
            url = self.__get_api_url(url_parts)
            response = self.fetch(url)
            self.assertEqual(response.code, 403)

    def test_invalid_auth_header(self):
        url = "/v0/datasources"
        invalid_headers = [
            f"Other {self.admin_token}",
            f"Bearer {self.admin_token} other",
            "Bearer ",
            "Other ",
        ]
        for invalid_header in invalid_headers:
            with self.subTest(invalid_header=invalid_header):
                headers = {"Authorization": invalid_header}
                response = self.fetch(url, headers=headers)
                self.assertEqual(response.code, 403)
                result = json.loads(response.body)
                self.assertEqual(result["error"], INVALID_AUTH_MSG)

    def test_invalid_regions(self):
        url = "/v0/datasources"

        self.app.settings["available_regions"] = {
            "local": {
                "host": "http://localhost:9999",
                "api_host": "http://localhost:9999",
                "name": "local",
            }
        }

        # workspace not found in the region, might exist in other
        token = Workspaces.add_token(self.u, "test_token", scopes.DATASOURCES_CREATE)
        Workspaces.drop_token(self.u, token)
        headers = {"Authorization": f"Bearer {token}"}
        response = self.fetch(url, headers=headers)
        self.assertEqual(response.code, 403)
        result = json.loads(response.body)
        self.assertTrue(
            "Workspace not found, make sure you use the token host http://localhost:9999" in result["error"]
        )

        self.app.settings["available_regions"] = {
            "local": {
                "host": "http://localhost:8889",
                "api_host": "http://localhost:8889",
                "name": "local",
            }
        }

        # workspace not found in the region
        token = Workspaces.add_token(self.u, "test_token", scopes.DATASOURCES_CREATE)
        Workspaces.drop_token(self.u, token)
        headers = {"Authorization": f"Bearer {token}"}
        response = self.fetch(url, headers=headers)
        self.assertEqual(response.code, 403)
        result = json.loads(response.body)
        self.assertTrue("Workspace not found in region" in result["error"])

        # no token
        response = self.fetch(url)
        self.assertEqual(response.code, 403)
        result = json.loads(response.body)
        self.assertTrue(INVALID_AUTH_MSG in result["error"])

    def test_empty_auth_header(self):
        url = "/v0/datasources"
        headers = {"Authorization": " "}
        response = self.fetch(url, headers=headers)
        self.assertEqual(response.code, 403)
        result = json.loads(response.body)
        self.assertEqual(result["error"], INVALID_AUTH_MSG)

    def test_valid_auth_token_trailing_space(self):
        url = "/v0/datasources"
        headers = {"Authorization": f"Bearer {self.admin_token} "}
        response = self.fetch(url, headers=headers)
        self.assertEqual(response.code, 200)

    def __validate_cors_headers(self, response):
        self.assertEqual(response.code, 204)
        self.assertEqual(response.headers.get("Access-Control-Allow-Origin"), "*")
        self.assertEqual(
            response.headers.get("Access-Control-Allow-Headers"),
            "Authorization, Content-Type, X-Requested-With, X-Tb-Warning",
        )
        self.assertEqual(response.headers.get("Access-Control-Allow-Methods"), "GET, POST, PUT, DELETE, OPTIONS")
        self.assertEqual(response.headers.get("Access-Control-Max-Age"), "86400")

    def __validate_no_cors_headers(self, response):
        self.assertEqual(response.code, 204)
        self.assertIsNone(response.headers.get("Access-Control-Allow-Origin"))
        self.assertIsNone(response.headers.get("Access-Control-Allow-Headers"))
        self.assertIsNone(response.headers.get("Access-Control-Allow-Methods"))
        self.assertIsNone(response.headers.get("Access-Control-Max-Age"))

    def test_cors_not_present_by_default(self):
        url = "/v0/pipes"
        response = self.fetch(url, method="OPTIONS")
        self.__validate_cors_headers(response)

    def test_cors_with_auth_header(self):
        url = "/v0/pipes"
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = self.fetch(url, headers=headers, method="OPTIONS")
        self.__validate_cors_headers(response)

    def test_cors_with_parameter(self):
        url = f"/v0/pipes?token={self.admin_token}"
        response = self.fetch(url, method="OPTIONS")
        self.__validate_cors_headers(response)

    def __get_secure_workspace_cookie(self):
        token_secure_cookie = create_signed_value(
            self.app.settings["cookie_secret"], "workspace_token", self.admin_token
        )
        return f"workspace_token={token_secure_cookie.decode()}"

    def __get_secure_user_cookie(self):
        token_secure_cookie = create_signed_value(self.app.settings["cookie_secret"], "token", self.admin_token)
        return f"token={token_secure_cookie.decode()}"

    def test_cors_not_present_with_cookie(self):
        url = "/v0/pipes"
        cookie = self.__get_secure_workspace_cookie()
        headers = {"Cookie": cookie}
        # validate cookie works and returns pipes
        response = self.fetch(url, headers=headers)
        self.assertEqual(response.code, 200)
        pipes = json.loads(response.body)
        self.assertIsInstance(pipes["pipes"], list)
        # Validate no CORS
        response = self.fetch(url, method="OPTIONS", headers=headers)
        self.__validate_cors_headers(response)

    def test_cors_with_cookie_and_token(self):
        url = f"/v0/pipes?token={self.admin_token}"
        headers = {"Cookie": self.__get_secure_workspace_cookie()}
        response = self.fetch(url, method="OPTIONS", headers=headers)
        self.__validate_cors_headers(response)

    def test_cors_with_path(self):
        self.create_test_datasource()
        url = "/v0/pipes/test_pipe"
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = self.fetch(url, headers=headers, method="OPTIONS")
        self.__validate_cors_headers(response)

    def test_undefined_token_doesnt_raise_errors(self):
        url = self.__get_api_url(["/datasources", "token", "BAD_TOKEN"])
        with self.assertRaises(AssertionError):
            with self.assertLogs(level=logging.ERROR):
                response = self.fetch(url)
        self.assertEqual(response.code, 403)

    def _get_auth_login_response(self, url_parts: List[str], assert_http_status: int = 200) -> Dict[str, Any]:
        url = self.__get_api_url(url_parts)
        response = self.fetch(url)
        self.assertEqual(response.code, assert_http_status)
        return json.loads(response.body)

    def test_auth_login_forbidden(self):
        response = self._get_auth_login_response(["/auth", "token", "BAD_TOKEN"])
        assert response.get("is_valid") is False, response
        assert response.get("is_user") is False, response

    def test_auth_login_with_admin_token(self):
        w = Workspaces.get_by_id(self.WORKSPACE_ID)
        token = w.get_token_for_scope(scopes.ADMIN)

        response = self._get_auth_login_response(["/auth", "token", token])
        assert response.get("is_valid") is True, response
        assert response.get("is_user") is False, response

    def test_auth_login_with_admin_user_token(self):
        w = Workspaces.get_by_id(self.WORKSPACE_ID)
        token = w.get_token_for_scope(scopes.ADMIN_USER)

        response = self._get_auth_login_response(["/auth", "token", token])
        assert response.get("is_valid") is True, response
        assert response.get("is_user") is False, response

    def test_auth_login_with_user_token(self):
        u = UserAccounts.get_by_id(self.USER_ID)
        token = u.get_token_for_scope(scopes.AUTH)

        response = self._get_auth_login_response(["/auth", "token", token])
        assert response.get("is_valid") is True, response
        assert response.get("is_user") is True, response

    def test_auth_login_with_other_token(self):
        w = Workspaces.get_by_id(self.WORKSPACE_ID)
        token = Workspaces.add_token(w, "test_token", scopes.DATASOURCES_CREATE)

        response = self._get_auth_login_response(["/auth", "token", token])
        assert response.get("is_valid") is False, response
        assert response.get("is_user") is False, response
