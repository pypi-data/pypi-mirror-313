import json
import logging
import textwrap
import time
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import parse_qs

import tornado.auth
import tornado.web
from tornado import escape
from tornado.web import url

from tinybird.default_secrets import DEFAULT_DOMAIN
from tinybird.integrations.integration import IntegrationInfo
from tinybird.integrations.vercel import VercelIntegration, VercelIntegrationService

from ..model import retry_transaction_in_case_of_concurrent_edition_error_async
from ..token_origin import Origins, TokenOrigin
from ..tokens import AccessToken, JWTAccessToken, ScopeException, scope_codes, scope_names, scopes
from ..user import CreateTokenError, TokenNotFound, TokenUsedInConnector, UserAccount, UserAccounts, WorkspaceException
from ..user import User as Workspace
from ..user import Users as Workspaces
from .api_errors.datasources import ClientErrorBadRequest
from .auth.oauth_base import OauthBase
from .base import ApiHTTPError, BaseHandler, authenticated, requires_write_access, user_authenticated, with_scope


def format_token(
    workspace: Workspace, token: AccessToken, resources: Optional[Dict[str, Any]] = None, hide_tokens: bool = False
) -> Dict[str, Any]:
    resources = resources or {
        **{ds.id: ds for ds in workspace.get_datasources()},
        **{p.id: p for p in workspace.get_pipes()},
    }

    t = token.to_dict()

    for scope in t["scopes"]:
        if "resource" in scope and scope["resource"] in resources:
            resource = resources[scope["resource"]]
            scope["resource"] = resource.name

    # Additional control in case our ACL logic leaks tokens
    if hide_tokens or t["token"][0] == "*":
        if not hide_tokens:
            logging.warning(f"Unexpected obfuscated token passed to format_tokens(): {t['name']}.")
        del t["token"]

    return t


async def generate_token_datafile(workspace: Workspace, token: AccessToken) -> str:
    resources = {
        **{ds.id: ds.name for ds in workspace.get_datasources()},
        **{p.id: p.name for p in workspace.get_pipes()},
    }

    t = token.to_dict()
    scopes_by_resource = {}

    for scope in t["scopes"]:
        if "resource" in scope and scope["resource"] in resources:
            resource_name = resources[scope["resource"]]
            scope["resource"] = resource_name
            if resource_name not in scopes_by_resource:
                scopes_by_resource[resource_name] = [scope["type"]]
            else:
                scopes_by_resource[resource_name].append(scope["type"])

    doc = []

    if token.description:
        doc.append(f"DESCRIPTION >\n\t{token.description}\n\n")

    for scope in t["scopes"]:
        resource = scope.get("resource", None)
        if resource and resource in scopes_by_resource:
            if f"RESOURCE {resource}\n" not in doc:
                node = f"SCOPE '{(', ').join(scopes_by_resource[resource])}'\n"
                node += f"RESOURCE {resource}\n"
                if scope.get("filter", None):
                    sql = textwrap.indent(scope["filter"], " " * 4)
                    node += f"FILTER >\n\n{sql}"
                    node += "\n\n\n"
        else:
            node = f"SCOPE '{scope['type']}'\n"

        if node and node not in doc:
            doc.append(node)

    return "\n".join(doc)


def format_tokens(workspace: Workspace, tokens: List[AccessToken], hide_tokens: bool = False) -> List[Dict[str, Any]]:
    resources = {
        **{ds.id: ds for ds in workspace.get_datasources()},
        **{p.id: p for p in workspace.get_pipes()},
    }

    return list(map(lambda t: format_token(workspace, t, resources, hide_tokens), tokens))


def validate_scopes(handler: BaseHandler, new_scopes: List[str]) -> None:
    if len(new_scopes) == 0:
        raise ApiHTTPError(400, "scope is mandatory")

    # Clean any resource ids from the scopes
    clean_scopes = tuple(":".join(s.split(":")[0:2]) if ":" in s else s for s in new_scopes)

    valid_scopes = tuple(scope_names.values())
    invalid = next((s for s in clean_scopes if s not in valid_scopes), None)
    if invalid:
        raise ApiHTTPError(400, f"Unknown scope {invalid}")

    # Disallow the use of the following scopes for new tokens
    disallowed_scopes = {scope_names.get(scopes.ADMIN_USER), scope_names.get(scopes.AUTH)}
    disallowed = next((s for s in clean_scopes if s in disallowed_scopes), None)
    if disallowed:
        raise ApiHTTPError(400, f"Cannot set {disallowed} scope, please provide a different target scope")

    # Allow these scopes only if the caller is an admin
    only_admin_scopes = {scope_names.get(scopes.ADMIN)}
    adm = next((s for s in clean_scopes if s in only_admin_scopes), None)
    if adm and not handler.is_admin():
        raise ApiHTTPError(400, f"Cannot set {adm} scope, please provide a different target scope")


def ensure_resource_id(items: Union[List[Dict[str, Any]], List[str]], resource_id: str) -> str:
    for item in items:
        if isinstance(item, str):
            if item == resource_id:
                return item

        elif item.get("id", None) == resource_id or item.get("name", None) == resource_id:
            return item["id"]

    raise ApiHTTPError(400, f"Unknown resource '{resource_id}'")


class APITokensHandlerBase(BaseHandler):
    def check_xsrf_cookie(self) -> None:
        pass

    def can_admin_workspace_tokens(self, workspace: Workspace) -> bool:
        """This method name is a bit misleading. It returns true for Viewer users, who can't admin tokens"""
        # First see if there's a workspace token in the request
        raw_token = self.get_workspace_token_from_request_or_cookie()
        token = workspace.get_token_access_info(raw_token.decode()) if raw_token else None

        if token:
            return token.has_scope(scopes.ADMIN) or token.has_scope(scopes.ADMIN_USER) or token.has_scope(scopes.TOKENS)
        else:
            # If it's not a workspace token, it must be a user token (AUTH). Let's check that said user has an
            # ADMIN_USER token in the workspace. This is really a check for workspace membership.
            user = self.get_user_from_db()
            if not user:
                return False

            return bool(workspace.get_token_for_scope(scopes.ADMIN_USER, user.id))

    def get_safe_tokens(
        self, workspace: Optional[Workspace] = None, user: Optional[UserAccount] = None
    ) -> List[AccessToken]:
        """Return all available tokens for the current user/token. It obfuscates sensitive tokens, if any"""

        try:
            workspace = workspace or self.get_workspace_from_db()
        except Exception:
            workspace = None

        if workspace:
            raw_token = self.get_workspace_token_from_request_or_cookie()
            token = workspace.get_token_access_info(raw_token.decode()) if raw_token and workspace else None
            if token:
                if token.has_scope(scopes.ADMIN) or token.has_scope(scopes.TOKENS):
                    token_info = self._get_access_info()
                    if not token_info:
                        raise Exception("Token not found")
                    return workspace.get_safe_tokens_for_token_admin(token_info)
                elif token.has_scope(scopes.ADMIN_USER):
                    for user_id in token.get_resources_for_scope(scopes.ADMIN_USER):
                        # There's only one resource
                        return workspace.get_safe_user_tokens(user_id)

            user = user or self.get_user_from_db()
            if user:
                return workspace.get_safe_user_tokens(user.id)
        return []


class APITokensHandler(APITokensHandlerBase):
    @authenticated
    def get(self) -> None:
        """
        Retrieves all workspace Static Tokens.

        .. sourcecode:: bash
            :caption: Get all tokens

            curl -X GET \\
                -H "Authorization: Bearer <ADMIN token>" \\
                "https://api.tinybird.co/v0/tokens"

        A list of your Static Tokens and their scopes will be sent in the response.

        .. sourcecode:: json
            :caption: Successful response

            {
                "tokens": [
                    {
                        "name": "admin token",
                        "description": "",
                        "scopes": [
                            { "type": "ADMIN" }
                        ],
                        "token": "p.token"
                    },
                    {
                        "name": "import token",
                        "description": "",
                        "scopes": [
                            { "type": "DATASOURCES:CREATE" }
                        ],
                        "token": "p.token0"
                    },
                    {
                        "name": "token name 1",
                        "description": "",
                        "scopes": [
                            { "type": "DATASOURCES:READ", "resource": "table_name_1" },
                            { "type": "DATASOURCES:APPEND", "resource": "table_name_1" }
                        ],
                        "token": "p.token1"
                    },
                    {
                        "name": "token name 2",
                        "description": "",
                        "scopes": [
                            { "type": "PIPES:READ", "resource": "pipe_name_2" }
                        ],
                        "token": "p.token2"
                    }
                ]
            }

        """

        workspace = self.get_workspace_from_db()
        if not workspace:
            raise ApiHTTPError(404, "Not found")

        if not self.can_admin_workspace_tokens(workspace):
            raise ApiHTTPError(403, "Token has not enough permissions to get information about Tokens")

        tokens = self.get_safe_tokens()

        self.write_json({"tokens": format_tokens(workspace, tokens)})

    @authenticated
    @requires_write_access
    async def post(self) -> None:
        """
        Creates a new Token: Static or JWT

        .. sourcecode:: bash
            :caption: Creating a new Static Token

            curl -X POST \\
                -H "Authorization: Bearer <ADMIN token>" \\
                "https://api.tinybird.co/v0/tokens/" \\
                -d "name=test&scope=DATASOURCES:APPEND:table_name&scope=DATASOURCES:READ:table_name"

        .. csv-table:: Request parameters
            :header: "Key", "Type", "Description"
            :widths: 20, 20, 60

            "name", "String", "Name of the token"
            "description", "String", "Optional. Markdown text with a description of the token."
            "scope", "String", "Scope(s) to set. Format is `SCOPE:TYPE[:arg][:filter] <#id2>`_. This is only used for the Static Tokens"

        .. sourcecode:: json
            :caption: Successful response

            {
                "name": "token_name",
                "description": "",
                "scopes": [
                    { "type": "DATASOURCES:APPEND", "resource": "table_name" }
                    { "type": "DATASOURCES:READ", "resource": "table_name", "filter": "department = 1"},
                ],
                "token": "p.token"
            }


        When creating a token with ``filter`` whenever you use the token to read the table, it will be filtered. For example, if table is ``events_table`` and ``filter`` is ``date > '2018-01-01' and type == 'foo'`` a query like ``select count(1) from events_table`` will become ``select count(1) from events_table where date > '2018-01-01' and type == 'foo'``

        .. sourcecode:: bash
            :caption: Creating a new token with filter

            curl -X POST \\
                -H "Authorization: Bearer <ADMIN token>" \\
                "https://api.tinybird.co/v0/tokens/" \\
                -d "name=test&scope=DATASOURCES:READ:table_name:column==1"

        If we provide an ``expiration_time`` in the URL, the token will be created as a JWT Token.

        .. sourcecode:: bash
            :caption: Creating a new JWT Token

            curl -X POST \\
                -H "Authorization: Bearer <ADMIN token>" \\
                "https://api.tinybird.co/v0/tokens?name=jwt_token&expiration_time=1710000000" \\
                -d '{"scopes": [{"type": "PIPES:READ", "resource": "requests_per_day", "fixed_params": {"user_id": 3}}]}'

        .. container:: hint

            In multi-tenant applications, you can use this endpoint to create a JWT token for a specific tenant where each user has their own token with a fixed set of scopes and parameters
        """

        workspace = self.get_workspace_from_db()
        if not workspace:
            raise ApiHTTPError(404, "Not found")

        if not self.can_admin_workspace_tokens(workspace):
            raise ApiHTTPError(403, "Token has not enough permissions to create an Token")

        # TODO: We should add support for all the arguments to be passed in the body as JSON
        name: str = self.get_argument("name")
        description: str = self.get_argument("description", "")

        origin_code = self.get_argument("origin", Origins.CUSTOM)
        # LEGACY is for internal use only
        if origin_code == Origins.LEGACY:
            raise ApiHTTPError(400, "invalid origin")

        # `resource_identifier` could be the resouce's `id` or `name`
        resource_identifier = self.get_argument("resource_id", None)
        if Origins.origin_needs_resource(origin_code) and not resource_identifier:
            raise ApiHTTPError(400, "missing resource_id")

        # Ensure we always get an id
        if resource_identifier:
            if origin_code == Origins.DATASOURCE:
                resource_identifier = ensure_resource_id(workspace.datasources, resource_identifier)
            elif origin_code == Origins.PIPE:
                resource_identifier = ensure_resource_id(workspace.pipes, resource_identifier)
            elif origin_code == Origins.TIMESERIES:
                resource_identifier = ensure_resource_id(workspace.explorations_ids, resource_identifier)
            else:
                # This should never happen, but...
                raise ApiHTTPError(400, "invalid origin")

        # These parameters are used to create jwt tokens
        expiration_time = self.get_argument("expiration_time", None)
        if expiration_time:
            try:
                expiration_time = int(expiration_time)
            except ValueError:
                raise ApiHTTPError(
                    400,
                    f"The specified expiration time: '{expiration_time}' is invalid, must be a future unix epoch timestamp indicating the token expiration time",
                    documentation="/api-reference/token-api.html#post--v0-tokens-?",
                )

            if expiration_time < int(time.time()):
                raise ApiHTTPError(
                    400,
                    f"The specified expiration time: '{expiration_time}' is invalid, must be a future unix epoch timestamp indicating the token expiration time",
                    documentation="/api-reference/token-api.html#post--v0-tokens-?",
                )

            try:
                body = self.request.body.decode()
                content = json.loads(body)
                new_scopes = content.get("scopes", [])
                limits = content.get("limits", {})
                limit_rps = limits.get("rps")
                if not isinstance(new_scopes, list):
                    raise ApiHTTPError(
                        400,
                        "Invalid body, scopes must be a list of scope",
                        documentation="/api-reference/token-api.html#post--v0-tokens-?",
                    )

            except UnicodeDecodeError as e:
                raise ApiHTTPError.from_request_error(ClientErrorBadRequest.invalid_encoding()) from e
            except json.JSONDecodeError as e:
                raise ApiHTTPError(400, f"Invalid body : {e.msg}") from e

            # We will only generate the token, we will not store it in the Workspace
            # TODO: IDK why are we not passing the scopes when creating the accessToken in other parts
            workspace_access_token = workspace.get_access_token_for_scope(scopes.ADMIN)
            if not workspace_access_token:
                raise ApiHTTPError(
                    403,
                    "Token has not enough permissions to create jwt tokens",
                    documentation="/api-reference/token-api.html#post--v0-tokens-?",
                )

            # We use the workspace token as secret to generate the jwt token
            jwt_token = JWTAccessToken(
                workspace=workspace,
                name=name,
                secret=workspace_access_token.token,
                expiration_time=expiration_time,
                limit_rps=limit_rps,
            )

            for scope in new_scopes:
                type = scope.get("type")
                resource_name = scope.get("resource")
                _filters = scope.get("fixed_params")

                if not type or type != scope_names[scopes.PIPES_READ]:
                    raise ApiHTTPError(
                        400,
                        "Invalid scope, only PIPES:READ is allowed",
                        documentation="/api-reference/token-api.html#post--v0-tokens-?",
                    )
                if not resource_name:
                    raise ApiHTTPError(
                        400,
                        "When creating a jwt token for PIPES:READ, a resource name is required",
                        documentation="/api-reference/token-api.html#post--v0-tokens-?",
                    )

                # Ensure the resource exists
                resource = workspace.get_resource(resource_name)
                if not resource:
                    raise ApiHTTPError(
                        400,
                        f"Resource '{resource_name}' not found",
                        documentation="/api-reference/token-api.html#post--v0-tokens-?",
                    )

                try:
                    jwt_token.add_scope(scope_codes[type], resource.id, _filters)
                except ScopeException as e:
                    raise ApiHTTPError(400, str(e))

            # Refresh again to include the scopes in the token
            jwt_token.refresh(workspace_access_token.token, workspace.id)
            self.write_json(jwt_token.to_json())
            return
        try:
            new_scopes = self.get_arguments("scope", True)
            validate_scopes(self, new_scopes)
            origin = TokenOrigin(origin_code, resource_identifier)
            new_token = await Workspaces.create_new_token(workspace, name, new_scopes, origin, description=description)
            access_token = Workspaces.get_token_access_info(workspace, new_token)
            assert isinstance(access_token, AccessToken)

            # Last check to avoid leaking unauthorized ADMIN_USER tokens
            # In theory, we can't create ADMIN_USER, but just in case...
            # TODO: move this logic to the future tokens service
            if access_token.has_scope(scopes.ADMIN_USER):
                user = self.get_user_from_db()
                if not user or (user in access_token.get_resources_for_scope(scopes.ADMIN_USER)):
                    access_token.obfuscate()

            self.write_json(format_token(workspace, access_token))
        except CreateTokenError as e:
            raise ApiHTTPError(400, str(e))


class APITokensRefreshHandler(APITokensHandlerBase):
    @authenticated
    def get(self, token_id: str) -> None:
        raise ApiHTTPError(405, "refresh must be done with POST")

    async def update_integrations_tokens(self, workspace: Workspace, old_token: str, new_token: str) -> None:
        """Refreshes any workspace tokens used in a third party integration (only Vercel at this moment)"""

        # As we don't have a relational model and we don't want to overload the AccessToken class
        # with specific per-integration metadata, we have to do some manual search.

        for u in workspace.get_user_accounts():
            integrations: List[IntegrationInfo] = u.get("integrations", [])
            if not integrations:
                continue

            for i in integrations:
                if i.integration_type != "vercel":
                    continue
                integration = VercelIntegration.get_by_id(i.integration_id)
                if not integration:
                    continue

                bindings = integration.get_bindings(by_workspace_id=workspace.id, by_token=old_token)
                if bindings:
                    await VercelIntegrationService.update_bindings_token(integration, bindings, new_token)

    @authenticated
    @requires_write_access
    @with_scope(scopes.TOKENS)
    async def post(self, token_id: str) -> None:
        """
        Refresh the Static Token without modifying name, scopes or any other attribute. Specially useful when a Token is leaked, or when you need to rotate a Token.

        .. sourcecode:: bash
            :caption: Refreshing a Static Token

            curl -X POST \\
                -H "Authorization: Bearer <ADMIN token>" \\
                "https://api.tinybird.co/v0/tokens/:token_name/refresh"

        When successfully refreshing a token, new information will be sent in the response

        .. sourcecode:: json
            :caption: Successful response

            {
                "name": "token name",
                "description": "",
                "scopes": [
                    { "type": "DATASOURCES:READ", "resource": "table_name" }
                ],
                "token": "NEW_TOKEN"
            }

        .. csv-table:: Request parameters
            :header: "Key", "Type", "Description"
            :widths: 20, 20, 60

            "auth_token", "String", "Token. Ensure it has the ``TOKENS`` scope on it"

        .. csv-table:: Response codes
            :header: "Code", "Description"
            :widths: 20, 80

            "200", "No error"
            "403", "Forbidden. Provided token doesn't have permissions to drop the token. A token is not allowed to remove itself, it needs ``ADMIN`` or ``TOKENS`` scope"

        """

        workspace = self.get_workspace_from_db()
        if not workspace:
            raise ApiHTTPError(404, "Not found")

        safe_tokens = self.get_safe_tokens()

        # Find the requested token in the list of available tokens for the current user/token
        refresh_tk = workspace.get_token_access_info(token_id, safe_tokens)
        if not refresh_tk:
            raise ApiHTTPError(404, "Token not found")

        try:
            tk = await Workspaces.refresh_token(workspace, token_id)
            await self.update_integrations_tokens(workspace, refresh_tk.token, tk.token)

            if refresh_tk.is_obfuscated():
                tk.obfuscate()

            # If refresh_tk was obfuscated, it means the user can't view it's contents (set hide_tokens parameter accordingly)
            self.write_json(format_token(workspace, tk, hide_tokens=refresh_tk.is_obfuscated()))
        except TokenUsedInConnector as e:
            raise ApiHTTPError(403, str(e))
        except TokenNotFound as e:
            raise ApiHTTPError(404, str(e))


class APITokenHandler(APITokensHandlerBase):
    @authenticated
    @requires_write_access
    async def delete(self, token_id: str) -> None:
        """
        Deletes a Static Token .

        .. sourcecode:: bash
            :caption: Deleting a token

            curl -X DELETE \\
                -H "Authorization: Bearer <ADMIN token>" \\
                "https://api.tinybird.co/v0/tokens/:token"

        """

        workspace = self.get_workspace_from_db()
        if not workspace:
            raise ApiHTTPError(404, "Not found")

        if not self.can_admin_workspace_tokens(workspace):
            raise ApiHTTPError(403, "Token has not enough permissions to delete a Token")

        try:
            ok = await Workspaces.drop_token_async(workspace, token_id)
        except TokenNotFound as e:
            raise ApiHTTPError(404, str(e))
        except TokenUsedInConnector as e:
            raise ApiHTTPError(403, str(e))

        if not ok:
            raise ApiHTTPError(404, "Static Token not found")
        self.write_json({"ok": True})

    @authenticated
    async def get(self, token_name_or_id: str) -> None:
        """
        Fetches information about a particular Static Token.

        .. sourcecode:: bash
            :caption: Getting token info

            curl -X GET \\
                -H "Authorization: Bearer <ADMIN token>" \\
                "https://api.tinybird.co/v0/tokens/:token"

        Returns a json with name and scopes.

        .. sourcecode:: json
            :caption: Successful response

            {
                "name": "token name",
                "description": "",
                "scopes": [
                    { "type": "DATASOURCES:READ", "resource": "table_name" }
                ],
                "token": "p.TOKEN"
            }
        """
        DATAFILE_EXTENSION = ".token"
        is_datafile = token_name_or_id.endswith(DATAFILE_EXTENSION)
        if is_datafile:
            token_name_or_id = token_name_or_id[: -len(DATAFILE_EXTENSION)]

        workspace = self.get_workspace_from_db()
        if not workspace:
            raise ApiHTTPError(404, "Not found")

        if not self.can_admin_workspace_tokens(workspace):
            raise ApiHTTPError(403, "Token has not enough permissions to get information about Tokens")

        safe_tokens = self.get_safe_tokens()

        tk = Workspaces.get_token_access_info(workspace, token_name_or_id, safe_tokens)
        if not tk:
            # Two reasons the token was not found:

            # 1) The token doesn't exist -> 404
            if Workspaces.get_token_access_info(workspace, token_name_or_id):
                raise ApiHTTPError(404, "Token not found")
            # 2) Exists, but not in the safe_tokens list --> 403
            else:
                raise ApiHTTPError(403, "Token has not enough permissions to get information about this token")

        if is_datafile:
            self.set_header("Content-Type", "text/plain")
            content = await generate_token_datafile(workspace, tk)
            self.write(content)
            return

        self.write_json(format_token(workspace, tk, hide_tokens=tk.is_obfuscated()))

    @authenticated
    @requires_write_access
    @tornado.web.removeslash
    async def put(self, token_id: str) -> None:
        """
        Modifies a Static Token. More than one scope can be sent per request, all of them will be added as Token scopes. Every time a Token scope is modified, it overrides the existing one(s).

        .. sourcecode:: bash
            :caption: editing a token

            curl -X PUT \\
                -H "Authorization: Bearer <ADMIN token>" \\
                "https://api.tinybird.co/v0/tokens/<Token>?" \\
                -d "name=test_new_name&description=this is a test token&scope=PIPES:READ:test_pipe&scope=DATASOURCES:CREATE"

        .. csv-table:: Request parameters
            :header: "Key", "Type", "Description"
            :widths: 20, 20, 60

            "token", "String", "Token. Ensure it has the ``TOKENS`` scope on it"
            "name", "String", "Optional. Name of the token."
            "description", "String", "Optional. Markdown text with a description of the token."
            "scope", "String", "Optional. Scope(s) to set. Format is `SCOPE:TYPE[:arg][:filter] <#id2>`_. New scope(s) will override existing ones."

        .. sourcecode:: json
            :caption: Successful response

            {
              "name": "test",
              "description": "this is a test token",
              "scopes": [
                { "type": "PIPES:READ", "resource": "test_pipe" },
                { "type": "DATASOURCES:CREATE" }
              ]
            }
        """

        workspace = self.get_workspace_from_db()
        if not workspace:
            raise ApiHTTPError(404, "Not found")

        if not self.can_admin_workspace_tokens(workspace):
            raise ApiHTTPError(403, "Token has not enough permissions to change a Token")

        name: Optional[str] = self.get_argument("name", None, True)
        description: Optional[str] = self.get_argument("description", None)

        new_scopes = self.get_arguments("scope", True)
        if not new_scopes and not name and not description:
            try:
                body_params = self.request.body.decode()
            except UnicodeDecodeError:
                raise ApiHTTPError.from_request_error(ClientErrorBadRequest.invalid_encoding())
            if body_params:
                parameters: Dict[str, Any] = parse_qs(body_params)
                new_scopes = parameters.get("scope", [])
                name_param: Optional[Union[str, List[str]]] = parameters.get("name", None)
                desc_param: Optional[Union[str, List[str]]] = parameters.get("description", None)

                name = name_param[0] if isinstance(name_param, list) else name_param
                description = desc_param[0] if isinstance(desc_param, list) else desc_param

        workspace, token = await self._update_token(workspace, token_id, name, description, new_scopes)

        self.write_json(format_token(workspace, token))

    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def _update_token(
        self,
        workspace: Workspace,
        token_id: str,
        name: Optional[str],
        description: Optional[str],
        new_scopes: List[str],
    ) -> Tuple[Workspace, AccessToken]:
        if new_scopes:
            validate_scopes(self, new_scopes)

        try:
            workspace.check_connector_token(token=token_id)
        except TokenUsedInConnector as e:
            raise ApiHTTPError(403, str(e))

        safe_tokens = self.get_safe_tokens()

        with Workspace.transaction(workspace.id) as workspace:
            if not workspace.get_token_access_info(token_id, safe_tokens):
                raise ApiHTTPError(404, "Static Token not found")

            # Get the object reference from workspace's list, not from safe_tokens
            token = workspace.get_token_access_info(token_id)
            assert isinstance(token, AccessToken)

            if name:
                token.name = name

            if description is not None:
                token.description = description

            token.clean_scopes()

            if new_scopes:
                for s in new_scopes:
                    scope, name_or_uid, _filters = AccessToken.parse(s)
                    if scope:
                        resource = None
                        if name_or_uid:
                            try:
                                resource = workspace.get_resource_id_for_scope(scope, name_or_uid)
                            except CreateTokenError as ex:
                                raise ApiHTTPError(400, str(ex))
                        try:
                            token.add_scope(scope, resource, _filters)
                        except ScopeException as e:
                            raise ApiHTTPError(400, str(e))
                    else:
                        raise ApiHTTPError(
                            400, "Invalid provided scope, valid ones are: %s" % ", ".join(scope_names.values())
                        )
        return workspace, token


class APITokensWorkspaces(APITokensHandlerBase):
    @user_authenticated
    async def get(self, workspace_id: str) -> None:
        workspace = Workspace.get_by_id(workspace_id)
        if not workspace:
            raise ApiHTTPError(404, "Not found")

        # In this case, this method only really checks that the request user is a member of the workspace. It returns
        # True for Viewer users
        if not self.can_admin_workspace_tokens(workspace):
            raise ApiHTTPError(403, "Token has not enough permissions to get information about Tokens")

        safe_tokens = self.get_safe_tokens(workspace)

        self.write_json({"tokens": format_tokens(workspace, safe_tokens)})


class APITokensUserRefreshHandler(APITokensHandlerBase):
    @authenticated
    def get(self, token_id: str) -> None:
        raise ApiHTTPError(405, "refresh must be done with POST")

    @user_authenticated
    @requires_write_access
    async def post(self, refresh_token: str) -> None:
        # TODO do we want to publish this endpoint as "Public"? In that case we should add documentation as with "APITokensRefreshHandler"

        user = self.get_user_from_db()
        try:
            refreshed = await UserAccounts.refresh_token(user, refresh_token)
            self.write_json({"token": refreshed.token})
        except TokenUsedInConnector as e:
            raise ApiHTTPError(403, str(e))
        except TokenNotFound as e:
            raise ApiHTTPError(404, str(e))


class APITokensUserHandler(APITokensHandlerBase, OauthBase, tornado.auth.OAuth2Mixin):
    _auth0_user_info_cache: Dict[str, Any] = {}

    async def get(self) -> None:
        async def get_first_available_workspace():
            try:
                workspaces = await user.get_workspaces(with_environments=False)
                return workspaces[0]["id"] if len(workspaces) > 0 else None
            except Exception:
                return None

        def get_safe_workspace(workspace_id_or_name: str) -> Optional[Workspace]:
            try:
                workspace = Workspaces.get_by_id_or_name(workspace_id_or_name)
                if not user.has_access_to(workspace.id):
                    # If we are impersonating a user as @tinybird.co, we should allow the user to access the workspace
                    if email and email != user_info_email and user_info_email.split("@")[1] == DEFAULT_DOMAIN:
                        return None
                    raise WorkspaceException("Workspace not found")
                return workspace
            except Exception:
                raise ApiHTTPError(404, "Workspace not found")

        auth0_config = self.settings.get("auth0_oauth", None)
        access_token_bytes = self.get_user_token_from_request_or_cookie()

        if not access_token_bytes:
            raise ApiHTTPError(401, "Unauthorized. Token is not valid")

        access_token = access_token_bytes.decode()
        email = self.get_argument("email", None)

        user_info: Optional[Dict[str, Any]] = None
        cache_key = access_token

        if cache_key in self._auth0_user_info_cache:
            user_info = self._auth0_user_info_cache[cache_key]
        else:
            http_client = self.get_auth_http_client()
            user_info_response = await http_client.fetch(
                f'https://{auth0_config["domain"]}/userinfo', headers={"Authorization": f"Bearer {access_token}"}
            )

            if user_info_response.code != 200:
                logging.exception(f"Error fetching user info: {user_info_response.code}{user_info_response.body}")
                raise ApiHTTPError(401, "Unauthorized. Error fetching user info")

            user_info = json.loads(user_info_response.body)

            if user_info and "email_verified" in user_info and not user_info["email_verified"]:
                self.write_json(
                    {
                        "workspace_token": None,
                        "user_token": None,
                        "workspace_id": None,
                        "workspace_name": None,
                        "email_verified": False,
                    }
                )
                return

            self._auth0_user_info_cache[cache_key] = user_info

        if not user_info:
            raise ApiHTTPError(401, "Unauthorized. Token does not have an associated user")

        user_info_email = user_info["email"]
        hubspotutk = self.get_argument("hubspotutk", None)

        try:
            user = await self.get_or_register_user_and_refresh_data(user_info, hubspotutk)
        except Exception:
            raise ApiHTTPError(401, f"Unauthorized. User not found for email {user_info_email}")

        if email and email != user_info_email:
            if not user.is_tinybird:
                raise ApiHTTPError(401, "Unauthorized. Requested email doesn't match the logged in user")
            else:
                try:
                    user = UserAccounts.get_by_email(email)
                except Exception:
                    raise ApiHTTPError(401, f"Unauthorized. User not found for email {email}")

        user_token = user.get_token_for_scope(scopes.AUTH)
        workspace: Optional[Workspace] = None
        workspace_token: Optional[str] = None
        workspace_id_or_name = self.get_argument("workspace_id", None)
        workspace_id: Optional[str] = None
        workspace_name: Optional[str] = None
        signed_workspace_token: Optional[str] = None
        signed_user_token: Optional[str] = None

        if not workspace_id_or_name:
            workspace_id_or_name = await get_first_available_workspace()

        if workspace_id_or_name:
            workspace = get_safe_workspace(workspace_id_or_name)
            if not workspace:
                first_available_ws = await get_first_available_workspace()
                if first_available_ws:
                    workspace = get_safe_workspace(first_available_ws)

        if workspace:
            workspace_token = workspace.get_workspace_access_token(user.id)
            workspace_id = workspace.id
            workspace_name = workspace.name

        if workspace_token:
            signed_workspace_token = escape.native_str(self.create_signed_value("workspace_token", workspace_token))

        if user_token:
            signed_user_token = escape.native_str(self.create_signed_value("token", user_token))

        self.write(
            {
                "workspace_token": workspace_token,
                "user_token": user_token,
                "workspace_id": workspace_id,
                "workspace_name": workspace_name,
                "signed_workspace_token": signed_workspace_token,
                "signed_user_token": signed_user_token,
            }
        )


def handlers():
    return [
        # these ones should be in this order
        url(r"/v0/tokens/?", APITokensHandler),
        url(r"/v0/tokens/(.+)/refresh", APITokensRefreshHandler),
        url(r"/v0/tokens/(.+)", APITokenHandler),
        url(r"/v0/workspaces/(.+)/tokens/?", APITokensWorkspaces),
        url(r"/v0/user/tokens/(.+)/refresh/?", APITokensUserRefreshHandler),
        url(r"/v0/user/tokens/?", APITokensUserHandler),
    ]
