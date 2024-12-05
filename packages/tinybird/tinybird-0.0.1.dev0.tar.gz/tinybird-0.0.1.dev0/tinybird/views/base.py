import asyncio
import binascii
import cgi
import functools
import inspect
import json
import logging
import re
import sys
import traceback
from asyncio import Future
from dataclasses import dataclass
from datetime import datetime, timezone
from math import ceil
from typing import Any, Callable, Dict, List, Never, Optional, Pattern, Tuple, Union
from urllib.parse import urlparse

import jwt
import tornado.web
import ulid
from opentracing import Span, Tracer
from packaging import version
from tornado.httputil import HTTPServerRequest
from tornado.routing import PathMatches, Rule
from tornado.web import Application, HTTPError
from tornado_opentracing import TornadoTracing

from tinybird import context
from tinybird.ch_utils.exceptions import SQL_TIP_TAG
from tinybird.constants import BillingPlans, ExecutionTypes
from tinybird.distributed import after_finish_concurrent_process, before_start_concurrent_process
from tinybird.feature_flags import FeatureFlagsWorkspaceService, FeatureFlagWorkspaces
from tinybird.organization.organization import Organization
from tinybird.user_workspace import UserWorkspaceRelationship
from tinybird.views.api_errors.datasources import ClientErrorBadRequest
from tinybird_shared.metrics.statsd_client import statsd_client
from tinybird_shared.retry.retry import TooManyRedisConnections

from ..limits import EndpointLimits, Limits, PlanRateLimitConfig, RateLimitConfig
from ..shutdown import ShutdownApplicationStatus
from ..tokens import AccessToken, JWTAccessToken, ResourcePrefix, is_jwt_token, scope_names, scopes, token_decode
from ..user import User, UserAccount, UserAccountDoesNotExist, UserAccounts, UserDoesNotExist, Users, public
from .api_errors import RequestError
from .api_errors.utils import replace_table_id_with_datasource_id
from .api_errors.workspaces import WorkspacesClientErrorForbidden, WorkspacesClientErrorNotFound

try:
    from .. import revision  # type: ignore
except Exception:
    revision = None


HANDLERS_NOT_SUPPORTED_WITH_SEMVER = ["APIWorkspaceReleaseHandler", "APIWorkspaceRelease", "APIUserWorkspaces"]
HANDLERS_SUPPORTING_JWT_TOKENS = ["APIPipeDataHandler", "APIPipeEndpointChartHandler", "APIChartPresetsHandler"]

CLI_TAG_PARAM = "cli_version"
UI_TAG_PARAM = "tag"
TAG_PARAMS = [CLI_TAG_PARAM, UI_TAG_PARAM]

BAD_REQUEST_CODE = 400
FORBIDDEN_CODE = 403
NOT_FOUND_CODE = 404
METHOD_NOT_ALLOWED_CODE = 405
TIMEOUT_CODE = 408
INVALID_CONTENT_LENGTH_CODE = 411
BODY_TOO_LARGE_CODE = 413
TOO_MANY_REQUESTS_CODE = 429

INVALID_AUTH_MSG = "invalid authentication token"
QUERY_API = "__query_api"
QUERY_API_FROM_UI = "__query_api_from_ui"


class ApiHTTPError(HTTPError):
    def __init__(
        self,
        status_code: int = 500,
        log_message: Optional[str] = None,
        documentation: Optional[str] = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(status_code, log_message, *args, **kwargs)
        self.error_message = log_message
        self.documentation = documentation
        self.extra_headers = kwargs.get("extra_headers", {})

    @staticmethod
    def from_request_error(request_error: RequestError, **kwargs: Any) -> "ApiHTTPError":
        return ApiHTTPError(request_error.status_code, request_error.message, **kwargs)


def authenticated(method: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(method)
    def wrapper(self: "BaseHandler", *args: Any, **kwargs: Any) -> Any:
        if not self.current_workspace:
            try:
                tok = self.get_workspace_token_from_request_or_cookie()
                if not tok:
                    e = ApiHTTPError(
                        403,
                        INVALID_AUTH_MSG,
                        documentation="/api-reference/overview#authentication",
                    )
                else:
                    extra = ""
                    token_data, error = self._decode_and_authenticate_token(tok)
                    if token_data:
                        app_host = self.application.settings.get("api_host")
                        if token_host := token_data.get("host"):
                            try:
                                region_config = self.get_region_config(token_host)
                                if app_host != region_config.get("api_host"):
                                    extra = f". Workspace not found, make sure you use the token host {region_config.get('api_host', '')}"
                                else:
                                    extra = ". Workspace not found in region"
                            except Exception:
                                # this should not happen
                                extra = f". Host {token_host} not found"
                                pass
                    else:
                        extra = f". {error}"
                    e = ApiHTTPError(
                        403,
                        INVALID_AUTH_MSG + extra,
                        documentation="/api-reference/overview#authentication",
                    )
            except Exception as ex:
                logging.exception(str(ex))
                e = ApiHTTPError(
                    403,
                    INVALID_AUTH_MSG,
                    documentation="/api-reference/overview#authentication",
                )
            return self.write_error(e.status_code, error=e.log_message, documentation=e.documentation)
        if self.current_workspace.deleted:
            e = ApiHTTPError(404, "workspace not found")
            return self.write_error(e.status_code, error=e.log_message, documentation=None)
        return method(self, *args, **kwargs)

    return wrapper


def user_authenticated(method: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(method)
    def wrapper(self: "BaseHandler", *args: Any, **kwargs: Any) -> Any:
        if not self.current_user:
            e = ApiHTTPError(403, "invalid user authentication", documentation="/api-reference/overview#authentication")
            return self.write_error(e.status_code, error=e.log_message, documentation=e.documentation)
        return method(self, *args, **kwargs)

    return wrapper


def user_or_workspace_authenticated(method: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(method)
    def wrapper(self: "BaseHandler", *args: Any, **kwargs: Any) -> Any:
        if not self.current_user and not self.current_workspace:
            e = ApiHTTPError(403, "invalid user authentication", documentation="/api-reference/overview#authentication")
            return self.write_error(e.status_code, error=e.log_message, documentation=e.documentation)
        if self.current_workspace and self.current_workspace.deleted:
            e = ApiHTTPError(404, "workspace not found")
            return self.write_error(e.status_code, error=e.log_message, documentation=None)
        return method(self, *args, **kwargs)

    return wrapper


def is_workspace_admin(method: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(method)
    def wrapper(self: "BaseHandler", *args: Any, **kwargs: Any) -> Any:
        def raise_access_error() -> Never:
            error = WorkspacesClientErrorNotFound.no_workspace()
            raise ApiHTTPError.from_request_error(error)

        user = self.get_user_from_db()
        if not user:
            raise_access_error()

        index = inspect.getfullargspec(method).args.index("workspace_id") - 1
        workspace_id = args[index]

        validated: bool = False

        if user.organization_id:
            # If the user belongs to an organization,  check if the workspace belongs to the
            # organization and the user is an admin of the organization
            org: Optional[Organization] = Organization.get_by_id(user.organization_id)
            if not org:
                raise_access_error()

            if user.id in org.user_account_ids and workspace_id in org.workspace_ids:
                validated = True
        # The user wasn't validated as an organization admin.
        # Let's check if the user is an admin of the workspace.
        if not validated and not UserWorkspaceRelationship.user_is_admin(user_id=user.id, workspace_id=workspace_id):
            raise_access_error()

        return method(self, *args, **kwargs)

    return wrapper


def has_workspace_access(method: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(method)
    def wrapper(self: "BaseHandler", *args: Any, **kwargs: Any) -> Any:
        index = inspect.getfullargspec(method).args.index("workspace_id") - 1
        workspace_id = args[index]
        user = self.get_user_from_db()
        if not UserWorkspaceRelationship.user_has_access(user_id=user.id, workspace_id=workspace_id):
            error = WorkspacesClientErrorNotFound.no_workspace()
            raise ApiHTTPError.from_request_error(error)
        return method(self, *args, **kwargs)

    return wrapper


def get_workspace_to_redirect(self, workspaces: List[Dict[str, Any]], requested_id: Optional[str]) -> Optional[User]:
    workspace: Optional[User] = self.get_workspace_from_db()

    if requested_id and (not workspace or (workspace.id != requested_id)):
        try:
            workspace = Users.get_by_id(requested_id)
        except Exception:
            pass

    # We consider that a workspace is not redirectable if:
    # - it doesn't exist
    # - it is deleted
    # - it is a branch and the main workspace is deleted
    def is_workspace_redirectable(workspace: Optional[User]) -> bool:
        if not workspace:
            return False
        if workspace.deleted:
            return False
        if workspace.is_branch and workspace.origin:
            return is_workspace_redirectable(Users.get_by_id(workspace.origin))
        return True

    if is_workspace_redirectable(workspace):
        return workspace

    # If the requested workspace is not redirectable,
    # we look for the first workspace that fulfills the following conditions:
    # - we are admin
    # - the workspace is not a branch or the main workspace is not deleted
    def get_first_redirectable_workspace(workspaces: List[Dict[str, Any]], only_admin=bool) -> Optional[User]:
        if not workspaces or len(workspaces) == 0:
            return None

        def has_enough_permissions(workspace: Dict[str, Any]) -> bool:
            return not only_admin or workspace["role"] == "admin"

        workspace_id = next(
            (
                workspace["id"]
                for workspace in workspaces
                if has_enough_permissions(workspace) and is_workspace_redirectable(Users.get_by_id(workspace["id"]))
            ),
            workspaces[0]["id"],
        )
        return Users.get_by_id(workspace_id)

    workspace = get_first_redirectable_workspace(workspaces, only_admin=True)

    if is_workspace_redirectable(workspace):
        return workspace

    # If we don't find any admin workspaces to redirect, we try with non-admin workspaces
    return get_first_redirectable_workspace(workspaces, only_admin=False)


def requires_write_access(method: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(method)
    def inner(self: "BaseHandler", *args: Any, **kwargs: Any) -> Any:
        # We need both workspace and user to check if the user has write access

        workspace: Optional[User] = None
        workspace_id: Optional[str] = None

        # Get the workspace by id if it's passed as an argument
        # If not, get the workspace from the db

        try:
            index: int = inspect.getfullargspec(method).args.index("workspace_id") - 1
            if index >= 0:
                workspace_id = args[index]
        except Exception:
            pass
        workspace = User.get_by_id(workspace_id) if workspace_id else self.get_workspace_from_db()

        # Enforce the check only if the workspace exists and is the main branch
        if workspace and not workspace.origin:
            current_token = self._get_token()
            access_tok: Optional[AccessToken] = next(
                (t for t in workspace.get_tokens() if t.token == current_token and t.has_scope(scopes.ADMIN_USER)),
                None,
            )
            if access_tok:
                user_id: Optional[str] = next((r for r in access_tok.get_resources_for_scope(scopes.ADMIN_USER)), None)
                user: Optional[UserAccount] = UserAccount.get_by_id(user_id) if user_id else self.get_user_from_db()

                if user and not UserWorkspaceRelationship.user_can_write(user_id=user.id, workspace_id=workspace.id):
                    error = WorkspacesClientErrorForbidden.user_is_read_only()
                    raise ApiHTTPError.from_request_error(error)

        return method(self, *args, **kwargs)

    return inner


def save_rate_limit_info_in_spans(handler, *args):
    try:
        class_name = "APIPipeDataHandler"
        if handler.__class__.__name__ != class_name:
            return

        pipe_id_or_name = args[0] if args and len(args) else None
        if pipe_id_or_name:
            if pipe_id_or_name.startswith("t_"):
                handler.set_span_tag({"pipe_id": pipe_id_or_name})
            else:
                handler.set_span_tag({"pipe_name": pipe_id_or_name})
    except Exception as e:
        logging.exception(e)


def check_rate_limit(rl_config: RateLimitConfig):
    def inner(method):
        @functools.wraps(method)
        async def wrapper(self, *args, **kwargs):
            try:
                await self.check_rate_limit(rl_config)
            except Exception:
                save_rate_limit_info_in_spans(self, *args)
                raise
            return await method(self, *args, **kwargs)

        return wrapper

    return inner


def check_plan_limit(rl_config: PlanRateLimitConfig) -> Callable[..., Any]:
    def inner(method: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(method)
        async def wrapper(self: "BaseHandler", *args: Any, **kwargs: Any) -> Any:
            try:
                await self.check_plan_rate_limit(rl_config)
            except Exception:
                save_rate_limit_info_in_spans(self, *args)
                raise
            return await method(self, *args, **kwargs)

        return wrapper

    return inner


def check_workspace_limit(rl_config: RateLimitConfig) -> Callable[..., Any]:
    def inner(method: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(method)
        async def wrapper(self: "BaseHandler", *args: Any, **kwargs: Any) -> Any:
            try:
                # TODO: Should we skip the rate limit check if the query is from the regression-tests
                await self.check_workspace_rate_limit(rl_config)
            except Exception:
                save_rate_limit_info_in_spans(self, *args)
                raise
            return await method(self, *args, **kwargs)

        return wrapper

    return inner


@dataclass
class ConcurrentRequestsLimiter:
    semaphore: asyncio.Semaphore
    max_concurrent_requests: int


concurrency_for_endpoint: Dict[str, ConcurrentRequestsLimiter] = {}


async def _check_jwt_rps_limit(
    handler: "BaseHandler", access_token: JWTAccessToken, workspace: Optional["User"], pipe_name_or_id: str
):
    if not workspace:
        return

    rps_limit = access_token.limit_rps
    if rps_limit and rps_limit > 0:
        key = f"jwt_endpoint_qps_limits_{workspace.id}_{pipe_name_or_id}_{access_token.name}"
        rate_limit = RateLimitConfig(
            key=key,
            count_per_period=rps_limit,
            period=1,
            max_burst=rps_limit,
        )
        try:
            await handler.check_rate_limit(rate_limit, workspace)
        except Exception:
            save_rate_limit_info_in_spans(handler, pipe_name_or_id)
            raise


async def _check_endpoint_rps_limit(handler: "BaseHandler", workspace: Optional["User"], pipe_name_or_id: str):
    if not workspace:
        return

    max_rps = workspace.get_endpoint_limit(pipe_name_or_id, EndpointLimits.max_rps)
    if max_rps:
        max_rps_key = EndpointLimits.get_limit_key(pipe_name_or_id, EndpointLimits.max_rps)
        rate_limit = RateLimitConfig(
            key=max_rps_key,
            count_per_period=max_rps,
            period=1,
            max_burst=0,  # https://gitlab.com/tinybird/analytics/-/issues/15825#note_2174129752
        )

        try:
            await handler.check_rate_limit(rate_limit, workspace)
        except Exception:
            save_rate_limit_info_in_spans(handler, pipe_name_or_id)
            raise


def check_endpoint_concurrency_limit(query_api: bool = False) -> Callable[..., Any]:
    def inner(method: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(method)
        async def wrapper(self: "BaseHandler", *args: Any, **kwargs: Any) -> Any:
            key = None
            workspace = self.current_workspace
            query_id = self._request_id

            flag = FeatureFlagsWorkspaceService.feature_for_id(
                FeatureFlagWorkspaces.DISTRIBUTED_ENDPOINT_CONCURRENCY, "", workspace.feature_flags
            )
            if not flag:
                return await method(self, *args, **kwargs)

            if query_api:
                if self.get_argument("from", None) == "ui":
                    pipe_name_or_id = QUERY_API_FROM_UI
                else:
                    pipe_name_or_id = QUERY_API
            else:
                pipe_name_or_id = args[0]

            max_concurrent_queries: Optional[int] = workspace.get_endpoint_limit(
                pipe_name_or_id, EndpointLimits.max_concurrent_queries
            )
            if not max_concurrent_queries or max_concurrent_queries == 0:
                return await method(self, *args, **kwargs)

            try:
                timestamp = int(datetime.now(timezone.utc).timestamp())
                max_execution_time = workspace.get_max_execution_time(is_admin=self.is_admin())
                key = EndpointLimits.get_limit_key(
                    f"{workspace.id}:{pipe_name_or_id}", EndpointLimits.max_concurrent_queries
                )

                allowed, count = await before_start_concurrent_process(
                    key, timestamp, max_execution_time, max_concurrent_queries, query_id
                )

                if not allowed:
                    save_rate_limit_info_in_spans(self, *args)
                    if pipe_name_or_id == QUERY_API:
                        msg = "for Query API"
                    elif pipe_name_or_id == QUERY_API_FROM_UI:
                        msg = "from the UI"
                    else:
                        msg = f"for Pipe {pipe_name_or_id}"

                    raise ApiHTTPError(
                        TOO_MANY_REQUESTS_CODE,
                        f"You have reached the maximum number of concurrent requests ({count}) {msg}. Retry or contact us at support@tinybird.co",
                    )
            except TooManyRedisConnections as e:
                logging.exception(
                    f"check_endpoint_concurrency_limit: before_start_concurrent_process: {key} - {query_id} - {e}"
                )
                raise ApiHTTPError(500, "Platform limit reached")
            except ApiHTTPError:
                try:
                    if key and query_id:
                        await after_finish_concurrent_process(key, query_id, User.redis_client)
                except TooManyRedisConnections as e:
                    logging.exception(
                        f"check_endpoint_concurrency_limit: after_finish_concurrent_process: {key} - {query_id} - {e}"
                    )
                    raise ApiHTTPError(500, "Platform limit reached")
                except Exception as e:
                    logging.exception(
                        f"check_endpoint_concurrency_limit: after_finish_concurrent_process: {key} - {query_id} - {e}"
                    )
                raise
            except Exception as e:
                logging.exception(f"check_endpoint_concurrency_limit: after_finish_concurrent_process: {e}")

            try:
                return await method(self, *args, **kwargs)
            finally:
                try:
                    if key and query_id:
                        await after_finish_concurrent_process(key, query_id, User.redis_client)
                except TooManyRedisConnections as e:
                    logging.exception(
                        f"check_endpoint_concurrency_limit: after_finish_concurrent_process: {key} - {query_id} - {e}"
                    )
                    raise ApiHTTPError(500, "Platform limit reached")
                except Exception as e:
                    logging.exception(
                        f"check_endpoint_concurrency_limit: after_finish_concurrent_process: {key} - {query_id} - {e}"
                    )

        return wrapper

    return inner


def check_endpoint_rps_limit() -> Callable[..., Any]:
    """
    Check if the endpoint RPS limit has been reached for JWT tokens or for a given endpoint.
    Return a 429 error if the limit is exceeded.
    """

    def inner(method: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(method)
        async def wrapper(self: "BaseHandler", *args: Any, **kwargs: Any) -> Any:
            try:
                pipe_name_or_id = args[0]
                workspace = self.current_workspace
                access_token = self._get_access_info()

                # TODO: In case of JWT token with limit and endpoint with limits, we should check the lowest limit
                # and run the rate limit check to avoid hitting twice Redis
                if isinstance(access_token, JWTAccessToken):
                    await _check_jwt_rps_limit(self, access_token, workspace, pipe_name_or_id)

                await _check_endpoint_rps_limit(self, workspace, pipe_name_or_id)

                return await method(self, *args, **kwargs)

            except (ApiHTTPError, HTTPError):
                raise
            except Exception as e:
                logging.exception(e)
                return await method(self, *args, **kwargs)

        return wrapper

    return inner


def check_organization_limit() -> Callable[..., Any]:
    """
    Check if the organization has reached its QPS limit.
    Uses Redis to track request rates at the organization level.
    Return a 429 error if the limit is exceeded.
    Only applies to workspaces that have the ORG_RATE_LIMIT feature flag enabled.
    """

    def inner(method: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(method)
        async def wrapper(self: "BaseHandler", *args: Any, **kwargs: Any) -> Any:
            try:
                workspace = self.current_workspace
                if workspace and workspace.organization_id:
                    # Check if the feature flag is enabled for this workspace
                    flag = FeatureFlagsWorkspaceService.feature_for_id(
                        FeatureFlagWorkspaces.ORG_RATE_LIMIT, "", workspace.feature_flags
                    )

                    if flag:
                        # TODO: Cache organization object in the handler as we do self.current_user and self.current_workspace
                        organization = Organization.get_by_id(workspace.organization_id)
                        if organization and organization.max_qps and organization.in_shared_infra_pricing:
                            org_rate_limit = RateLimitConfig(
                                key=f"org_qps_limit_{organization.id}",
                                count_per_period=organization.max_qps,
                                period=1,  # 1 second period for QPS
                                max_burst=ceil(organization.max_qps / 2),
                                msg_error=f"Organization QPS limit exceeded ({organization.max_qps} requests/second)",
                            )
                            try:
                                await self.check_rate_limit(org_rate_limit)
                            except Exception:
                                save_rate_limit_info_in_spans(self, *args)
                                raise

                return await method(self, *args, **kwargs)

            except (ApiHTTPError, HTTPError):
                raise
            except Exception as e:
                logging.exception(e)
                return await method(self, *args, **kwargs)

        return wrapper

    return inner


def confirmed_account(method: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(method)
    def wrapper(self: "BaseHandler", *args: Any, **kwargs: Any) -> Any:
        u: Optional[UserAccount] = self.get_user_from_db()
        if not u or not UserAccounts.confirmed_account(u):
            self.redirect("/login")
            return
        return method(self, *args, **kwargs)

    return wrapper


def with_scope_admin(method: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(method)
    def wrapper(self: "BaseHandler", *args: Any, **kwargs: Any) -> Any:
        if not self.is_admin():
            raise ApiHTTPError(
                403, "token needs scope admin", documentation="/api-reference/token-api.html#scopes-and-tokens"
            )
        return method(self, *args, **kwargs)

    return wrapper


def with_scope_admin_user(method: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(method)
    def wrapper(self: "BaseHandler", *args: Any, **kwargs: Any) -> Any:
        if not self.is_admin_user():
            raise ApiHTTPError(
                403,
                "token needs scope admin associated with your account",
                documentation="/api-reference/token-api.html#scopes-and-tokens",
            )
        return method(self, *args, **kwargs)

    return wrapper


def with_scope(scope: str) -> Callable[..., Any]:
    def _inner(method: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(method)
        async def wrapper(self: "BaseHandler", *args: Any, **kwargs: Any) -> Any:
            extra = ""
            if not self.has_scope(scope) and not self.is_admin():
                if self.__class__.__name__ == "APIPipeCopyHandler":
                    execution_type = self.get_argument("_execution_type", None)
                    if execution_type == ExecutionTypes.SCHEDULED and hasattr(self, "_delete_scheduled_sink"):
                        deleted = await self._delete_scheduled_sink(*args, **kwargs)
                        if deleted:
                            extra = ". The copy Pipe schedule was removed. Recreate the copy Pipe if you need to schedule it again."
                raise ApiHTTPError(
                    403,
                    f"token needs scope {scope_names[scope]}{extra}",
                    documentation="/api-reference/token-api.html#scopes-and-tokens",
                )
            return await method(self, *args, **kwargs)

        return wrapper

    return _inner


def read_only_from_ui(method: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(method)
    def wrapper(self: "BaseHandler", *args: Any, **kwargs: Any) -> Any:
        workspace = self.get_workspace_from_db()
        if workspace.is_read_only and not workspace.is_branch and self.is_from_ui():
            raise ApiHTTPError(403, "Operation not allowed for read-only Main Branch")
        return method(self, *args, **kwargs)

    return wrapper


class MethodAndPathMatches(PathMatches):
    def __init__(self, method, path_pattern):
        super().__init__(path_pattern)
        self.method = method

    def match(self, request):
        if request.method != self.method:
            return None

        return super().match(request)


class URLMethodSpec(Rule):
    def __init__(
        self,
        method: str,
        pattern: Union[str, Pattern],
        handler: Any,
        kwargs: Optional[Dict[str, Any]] = None,
        name: Optional[str] = None,
    ) -> None:
        matcher = MethodAndPathMatches(method, pattern)
        super().__init__(matcher, handler, kwargs, name)

        self.regex = matcher.regex
        self.handler_class = self.target
        self.kwargs = kwargs


def custom_handler_initialize_to_stop_serving_keep_alive_connections_on_app_shutdown(handler_internals):
    if ShutdownApplicationStatus.is_application_exiting():
        handler_internals.set_header("Connection", "close")
        handler_internals.request.connection.no_keep_alive = True


class CustomStaticHandler(tornado.web.StaticFileHandler):
    def initialize(self, path, default_filename=None):
        super().initialize(path, default_filename)
        custom_handler_initialize_to_stop_serving_keep_alive_connections_on_app_shutdown(self)


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, application: Application, request: HTTPServerRequest, **kwargs: Any) -> None:
        self._db_user: Optional[UserAccount] = None
        self._db_workspace: Optional[User] = None
        self._current_workspace: Optional[User] = None
        self._access_token: Optional[AccessToken] = None
        self._public_user: Optional[User] = None
        request_id = ulid.new().str
        self._request_id = request_id
        self._nginx_request_id = request.headers.get("X-Request-ID", None)
        request.headers["X-Request-ID"] = request_id
        self.rate_limit: Optional[Tuple[int, int, int, int, int]] = None
        self._is_organization_admin: Optional[bool] = None
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)

    def initialize(self):
        custom_handler_initialize_to_stop_serving_keep_alive_connections_on_app_shutdown(self)

    def get_bool_argument(self, name: str, default_value: Optional[bool] = None, true_values=("true", "1")) -> bool:
        v: str

        if default_value is None:
            # Allow to raise a 400 if not present
            v = self.get_argument(name)
        else:
            v = self.get_argument(name, None)

        if v is None:
            if default_value is None:
                raise tornado.web.MissingArgumentError(name)
            return default_value

        return v.lower() in true_values

    def get_api_option(self, parameter, valid_options, default_option=None):
        option = self.get_argument(parameter, default_option)
        if option is None:
            err = ClientErrorBadRequest.missing_parameter(parameter=parameter)
            raise ApiHTTPError.from_request_error(err)
        if option not in valid_options:
            err = ClientErrorBadRequest.invalid_value_for_argument(
                argument=parameter, value=option, valid=str(valid_options)
            )
            raise ApiHTTPError.from_request_error(err)
        return option

    def check_api_options(self, valid_argument_names):
        valid_argument_names = set(valid_argument_names)
        valid_argument_names.add("token")
        invalid_args = [x for x in self.request.arguments if x not in valid_argument_names.union(set(TAG_PARAMS))]
        if invalid_args:
            err = ClientErrorBadRequest.invalid_arguments(
                invalid_args=invalid_args, valid_argument_names=sorted(valid_argument_names)
            )
            raise ApiHTTPError.from_request_error(err)

    def check_xsrf_cookie(self) -> None:
        # if the token is not passed using a cookie, don't check XSRF token
        self.require_setting("jwt_secret", "secure jwt")
        secret = self.application.settings["jwt_secret"]
        token = self.__get_token_from_params_or_header()

        if token:
            try:
                # If the token is jwt, let's just check it's a valid token. We will check if it's valid later
                if is_jwt_token(token):
                    JWTAccessToken.token_decode_unverify(token)
                    return
                token_decode(token, secret)
                return
            except jwt.exceptions.DecodeError:
                pass
            except jwt.exceptions.MissingRequiredClaimError:
                self.write_error(
                    403,
                    error="JWT tokens is missing the 'exp' claim",
                    documentation="/api-reference/token-api.html#post--v0-tokens-?",
                )
                return

        super().check_xsrf_cookie()

    def write_json(self, chunk: Dict[Any, Any], default_serializer: Optional[Callable] = None) -> None:
        """Pretty print JSON response
        See:
         - https://github.com/tornadoweb/tornado/blob/b120df9b584dc59881b72854a4b8e73b16b25159/tornado/web.py#L812-L842
         - https://github.com/tornadoweb/tornado/blob/b120df9b584dc59881b72854a4b8e73b16b25159/tornado/escape.py#L64-L75
        """
        if not isinstance(chunk, dict):
            message = "write_json() only accepts dict objects"
            if isinstance(chunk, list):
                message += ", lists not accepted for security reasons; see http://www.tornadoweb.org/en/stable/web.html#tornado.web.RequestHandler.write"
            raise TypeError(message)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(json.dumps(chunk, indent=4, default=default_serializer).replace("</", "<\\/"))

    def write_error(self, status_code: int, **kwargs: Any) -> Future:
        self.set_header("Content-Type", "application/json")
        # Doing it again because the headers set in check_rate_limit are missing when reaching this.
        self.set_rate_limit_headers()

        self.set_status(status_code)
        payload = {"error": kwargs.get("error", self._reason)}
        if "documentation" in kwargs:
            doc = kwargs["documentation"]
            if isinstance(doc, str) and len(doc):
                payload["documentation"] = doc
        else:
            try:
                if status_code in [BAD_REQUEST_CODE, NOT_FOUND_CODE]:
                    method = self.request.method.lower()
                    doc = self.doc_path(method)
                    payload["documentation"] = doc
                elif status_code == FORBIDDEN_CODE:
                    payload["documentation"] = "/api-reference/overview#authentication"
                elif status_code == METHOD_NOT_ALLOWED_CODE:
                    doc = self.doc_path(None)
                    payload["documentation"] = doc
                elif status_code in [
                    TIMEOUT_CODE,
                    INVALID_CONTENT_LENGTH_CODE,
                    BODY_TOO_LARGE_CODE,
                    TOO_MANY_REQUESTS_CODE,
                ]:
                    payload["documentation"] = "/api-reference/api-reference.html#limits"
            except Exception:
                payload["documentation"] = "/api-reference/api-reference.html"

        exc_info = kwargs["exc_info"] if "exc_info" in kwargs else sys.exc_info()
        etype, value, tb = exc_info
        if isinstance(value, HTTPError):
            payload["error"] = value.log_message or str(value)
        if isinstance(value, ApiHTTPError):
            payload["error"] = value.error_message
            for k, v in value.extra_headers.items():
                self.set_header(k, v)
            if value.documentation:
                payload["documentation"] = value.documentation

        if "documentation" in payload:
            payload["documentation"] = f'https://docs.tinybird.co{payload["documentation"]}'

        try:
            doc_idx = payload["error"].index(SQL_TIP_TAG)
            payload["documentation"] = payload["error"][doc_idx + len(SQL_TIP_TAG) :].strip()
            payload["error"] = payload["error"][:doc_idx].strip()
        except Exception:
            pass

        if self.settings.get("serve_traceback") and value is not None:
            payload["traceback"] = [line for line in traceback.format_exception(etype, value, tb)]

        self.set_span_tag({"error": payload["error"], "http.status_code": status_code})

        try:
            payload["error"] = replace_table_id_with_datasource_id(
                ws=self.get_workspace_from_db(),
                error=payload["error"],
                error_datasource_id=self.application.settings["host"],
            )
        except ApiHTTPError as exc:
            # In case error was raised in self.get_workspace_from_db() ignore exception
            logging.warning(exc)

        tracer: Tracer = self.application.settings["opentracing_tracing"].tracer
        span: Optional[Span] = self.get_span()
        if span is None or tracer.scope_manager.active:
            return self.finish(payload)
        else:
            # If the tracer scope isn't active, activate it before finishing
            # to make sure the span is logged at on_finish() call
            with tracer.scope_manager.activate(span, True):
                return self.finish(payload)

    def doc_path(self, method):
        url = None
        for rule in self.application.default_router.rules[0].target.rules:
            if rule.target.__name__ == type(self).__name__:
                url = rule.matcher.regex.pattern.rstrip("$")
                break
        doc = doc_path_from_url(method, url)
        return doc

    @staticmethod
    def optional_date_to_str(date: Optional[datetime]) -> Optional[str]:
        if date is None:
            return None

        return date.isoformat()

    def get_template_namespace(self):
        template_vars = super().get_template_namespace()
        user_id = "anon"
        workspace_id = "anon"

        if self.current_user:
            u = self.get_user_from_db()
            if u:
                user_id = u["id"]

        if self.current_workspace:
            w = self.current_workspace
            if w:
                workspace_id = w["id"]

        u = self.public_user
        global_admin_token = None

        if u:
            global_admin_token = u.get_token_for_scope(scopes.ADMIN)

        template_vars.update(
            {
                "year": datetime.now().strftime("%Y"),
                "contact_email": "hi@tinybird.co",
                "twitter": "@tinybirdco",
                "user_id": user_id,
                "workspace_id": workspace_id,
                "arengu_form_id": "157297379846654567",
                "blog_host": "https://blog.tinybird.co",
                "support_url": "https://spectrum.chat/tinybird",
                "support_email": "support@tinybird.co",
                "cdn_host": self.application.settings["cdn_host"],
                "api_host": self.application.settings["api_host"],
                "docs_host": self.application.settings["docs_host"],
                "commercial_host": self.application.settings["commercial_host"],
                "host": self.application.settings["host"],
                "global_admin_token": global_admin_token,
            }
        )
        return template_vars

    @property
    def public_user(self):
        if self._public_user is None:
            self._public_user = public.get_public_user()
        return self._public_user

    def __get_token_from_params_or_header(self):
        token = self.get_argument("token", None)
        if not token:
            auth_header = self.request.headers.get("Authorization", None)
            if auth_header:
                auth_header_parts = auth_header.split(" ")

                if auth_header_parts and len(auth_header_parts) == 2 and auth_header_parts[0] == "Bearer":
                    token = auth_header_parts[1]
        return token

    def get_user_from_db(self) -> UserAccount:
        """you might be thinking why get_current_user method does not return the actual user.
        The idea is to not use get_user since it requires access to storage unless get_current_user which gets
        information from the jwt token.
        "_from_db" is added to the name so it's explicit
        """
        return self.current_user

    def get_workspace_from_db(self) -> User:
        """you might be thinking why get_current_user method does not return the actual user.
        The idea is to not use get_user since it requires access to storage unless get_current_user which gets
        information from the jwt token.
        "_from_db" is added to the name so it's explicit
        """
        return self.current_workspace

    def get_user_token_from_request_or_cookie(self) -> Optional[bytes]:
        tk = self.__get_token_from_params_or_header()
        if tk:
            return tk.encode()

        return self.get_secure_cookie("token")

    def get_workspace_token_from_request_or_cookie(self) -> bytes:
        tk = self.__get_token_from_params_or_header()
        if tk:
            return tk.encode()

        token = self.get_secure_cookie("workspace_token")
        return token

    @property
    def current_workspace(self):
        """
        Mimics current_user from tornado.web.RequestHandler
        """
        context.api_host.set(self.application.settings["api_host"])
        if not self._current_workspace:
            self._current_workspace = self.get_current_workspace()
        if self._current_workspace:
            flag = FeatureFlagsWorkspaceService.feature_for_id(
                FeatureFlagWorkspaces.DISABLE_TEMPLATE_SECURITY_VALIDATION, "", self._current_workspace.feature_flags
            )
            context.disable_template_security_validation.set(flag)

            split_to_array_escape = FeatureFlagsWorkspaceService.feature_for_id(
                FeatureFlagWorkspaces.SPLIT_TO_ARRAY_ESCAPE, "", self._current_workspace.feature_flags
            )
            context.ff_split_to_array_escape.set(split_to_array_escape)

            preprocess_parameters_circuit_breaker = FeatureFlagsWorkspaceService.feature_for_id(
                FeatureFlagWorkspaces.PREPROCESS_PARAMETERS_CIRCUIT_BREAKER, "", self._current_workspace.feature_flags
            )
            context.ff_preprocess_parameters_circuit_breaker.set(preprocess_parameters_circuit_breaker)

            handler_name = self.__class__.__name__

            semver = self.get_argument("__tb__semver", None)
            # `"regression" in semver`` is a temporary HACK for split to run regression tests. If they don't implement them let's deprecate and remove that functionality
            if not semver or "regression" in semver:
                return self._current_workspace

            if handler_name in HANDLERS_NOT_SUPPORTED_WITH_SEMVER:
                return self._current_workspace

            if len(self._current_workspace.releases):
                if semver == "snapshot":
                    self._current_workspace = self._current_workspace.get_snapshot()
                else:
                    release = self._current_workspace.get_release_by_semver(semver)
                    if not release:
                        # FIXME: add documentation link to explain releases and semver
                        raise ApiHTTPError(404, f"Release {semver} not found")
                    self._current_workspace = release.metadata
                    if active_span := self.get_active_span():
                        active_span.set_tag("release", release.semver)
        return self._current_workspace

    def _decode_and_authenticate_token(self, token: Optional[bytes]) -> Tuple[Optional[Dict[str, str]], Optional[str]]:
        """
        Decodes and authenticates a JWT token.

        It safely catches any internal exception that might happen in the process, while providing
        optional information about the internal error in the 2nd returned value

        Returns:
            Tuple[Optional[Dict[str, str]], Optional[str]]:
            - token_data: Decoded token data if valid, otherwise None.
            - error: Description of the error encountered, if any, otherwise None.
        """
        self.require_setting("jwt_secret", "secure jwt")
        secret = self.application.settings["jwt_secret"]

        if not token:
            return None, "No token provided"

        try:
            token_as_string = token.decode()
            # If the token is jwt, we need to decode the token with the workspace access token
            if is_jwt_token(token_as_string):
                handler_name = self.__class__.__name__
                if handler_name not in HANDLERS_SUPPORTING_JWT_TOKENS:
                    return None, f"Handler {handler_name} does not support JWT tokens"

                # We need to decode the token to get the workspace id and then get the workspace
                # to get the workspace access token
                payload = JWTAccessToken.token_decode_unverify(token_as_string)
                workspace_id = payload.get(ResourcePrefix.JWT, None)
                if not workspace_id:
                    return None, "Workspace ID missing in JWT token"

                workspace = User.get_by_id(workspace_id)
                if not workspace:
                    return None, f"Workspace with ID {workspace_id} not found"
                self._db_workspace = workspace
                workspace_token = workspace.get_token_for_scope(scopes.ADMIN)
                if not workspace_token:
                    return None, "Workspace token for admin scope not found"

                token_data = JWTAccessToken.token_decode(token_as_string, workspace_token)
                return token_data, None

            token_data = token_decode(token_as_string, secret)
            return token_data, None

        except (
            binascii.Error,
            jwt.exceptions.DecodeError,
            jwt.InvalidSignatureError,
            jwt.ExpiredSignatureError,
        ) as exc:
            error_message = f"Invalid token {token!r}: {exc}"
            logging.warning(error_message)
            return None, error_message
        except Exception as exc:
            error_message = f"Unexpected error decoding / validating token {token!r}: {exc}"
            logging.exception(error_message)
            return None, error_message

    def get_current_workspace(self) -> Optional[User]:
        token = self.get_workspace_token_from_request_or_cookie()
        if not token:
            return None

        token_data, _ = self._decode_and_authenticate_token(token)
        if not token_data:
            return None

        try:
            if not self._db_workspace:
                try:
                    workspace = Users.get_by_id(token_data["u"])
                except UserDoesNotExist:
                    return None
                self._db_workspace = workspace
            else:
                workspace = self._db_workspace

            token_decoded = token.decode()
            is_jwt = is_jwt_token(token_decoded)

            # We don't store the token in the workspace if it's a jwt token
            token_id = None
            token_name = None
            if is_jwt:
                token_id = ""  # Jwt tokens don't have an id
                token_name = token_data["name"]
            else:
                token_access_info = workspace.get_token_access_info(token_decoded)
                if not token_access_info:
                    return None
                token_id = token_access_info.id
                token_name = token_access_info.name

            if active_span := self.get_active_span():
                active_span.set_tag("workspace", workspace["id"])
                active_span.set_tag("workspace_name", workspace["name"])
                active_span.set_tag("token", token_id)
                active_span.set_tag("token_name", token_name)
                active_span.set_tag("user_agent", self.request.headers.get("User-Agent"))
                current_release = workspace.current_release
                if current_release:
                    active_span.set_tag("release", current_release.semver)

            return workspace
        except Exception:
            raise ApiHTTPError(503)

    def get_current_user(self) -> Optional[UserAccount]:
        token = self.get_user_token_from_request_or_cookie()
        if not token:
            return None

        token_data, _ = self._decode_and_authenticate_token(token)
        if not token_data:
            return None

        try:
            if not self._db_user:
                try:
                    user = UserAccounts.get_by_id(token_data["u"])
                except UserAccountDoesNotExist:
                    return None
                self._db_user = user
            else:
                user = self._db_user

            if not user.confirmed_account:
                return None

            user_token_decoded = token.decode()
            token_access_info = user.get_token_access_info(user_token_decoded)
            if not token_access_info:
                return None

            if active_span := self.get_active_span():
                active_span.set_tag("user", user["id"])
                active_span.set_tag("user_email", user["email"])
                active_span.set_tag("token", token_access_info.id)
                active_span.set_tag("token_name", token_access_info.name)
                active_span.set_tag("user_agent", self.request.headers.get("User-Agent"))
            return user
        except Exception:
            raise ApiHTTPError(503)

    async def check_rate_limit(
        self, rl_config: RateLimitConfig, workspace: Optional["User"] = None, dry_run: bool = False
    ) -> None:
        workspace = workspace if workspace else self.current_workspace
        if workspace:
            rl_config = workspace.rate_limit_config(rl_config)
            self.rate_limit = await Limits.rate_limit(rl_config)

            if not dry_run:
                self.set_rate_limit_headers()

            limited, _, _, retry, _ = self.rate_limit
            if limited and not dry_run:
                host = self.application.settings["host"]
                workspace_settings = self.reverse_url("workspace_settings", workspace.id)
                raise ApiHTTPError(
                    TOO_MANY_REQUESTS_CODE,
                    rl_config.msg_error.format(
                        retry=retry, workspace_name=workspace.name, workspace_settings_url=f"{host}{workspace_settings}"
                    ),
                    documentation=rl_config.documentation,
                )
            elif limited and dry_run:
                try:
                    # We need to replace the ":" with "." because it is not allowed in statsd and we will be storing
                    # the key in redis with the ":"
                    rate_limit_key = rl_config.key.replace(":", ".")
                    statsd_client.incr(f"tinybird.{statsd_client.region_machine}.rate_limit.{rate_limit_key}")
                except Exception:
                    logging.error(f"Error incrementing rate limit counter for key={rl_config.key}")

    async def check_workspace_rate_limit(self, rl_config: RateLimitConfig) -> None:
        workspace = self.current_workspace
        limit_workspace = workspace and workspace.limits.get(rl_config.key, None)
        if limit_workspace:
            await self.check_rate_limit(rl_config)

        elif workspace and workspace.plan in [BillingPlans.DEV, BillingPlans.PRO] and not self.is_from_ui():
            default_rate_limit_config = RateLimitConfig(
                key=rl_config.key,
                count_per_period=20,
                period=1,
                max_burst=20,
                msg_error="Workspaces created since 2024-08-12 have a limit of 20 requests per second by default. Please contact support@tinybird.co if you need to increase the limit.",
            )
            # If the workspace was created before 2024-08-12, we don't want to apply the rate limit by default
            # TODO: Remove validation `workspace.created_at` is not None after adding type hint to `workspace`
            dry_run = workspace.created_at < datetime(2024, 8, 12) if workspace.created_at else True
            await self.check_rate_limit(default_rate_limit_config, workspace, dry_run)

    async def check_plan_rate_limit(self, prl_config: PlanRateLimitConfig):
        workspace = self.current_workspace
        if workspace and prl_config.is_applicable(workspace, self.is_from_ui()):
            await self.check_rate_limit(prl_config)

    def _get_access_info(self) -> Optional[AccessToken | JWTAccessToken]:
        if self._access_token:
            return self._access_token

        workspace = self.get_workspace_from_db()
        if not workspace:
            return None
        tok = self.get_workspace_token_from_request_or_cookie()
        if not tok:
            return None

        token_decoded = tok.decode()
        # If the token is jwt, we need to decode the token with the workspace access token
        if is_jwt_token(token_decoded):
            self._access_token = JWTAccessToken.generate_jwt_access_from_token(token_decoded, workspace)
            return self._access_token
        access_token = workspace.get_token_access_info(token_decoded)
        if access_token:
            self._access_token = access_token
            return access_token

        # We are not caching the token because I am not sure if it is safe to do so
        # TODO: Validate if it is safe to cache the token
        if workspace.origin and (origin := User.get_by_id(workspace.origin)):
            return origin.get_token_access_info(tok.decode())
        return None

    def _get_token(self) -> Optional[str]:
        access_info = self._get_access_info()

        if access_info is None:
            return None

        return access_info.token

    def get_readable_resources(self) -> List[str]:
        access_info = self._get_access_info()
        readable_resources = (
            access_info.get_resources_for_scope(scopes.DATASOURCES_READ, scopes.PIPES_READ) if access_info else []
        )
        return readable_resources

    def get_dropable_resources(self) -> List[str]:
        access_info = self._get_access_info()
        dropable_resources = (
            access_info.get_resources_for_scope(scopes.DATASOURCES_DROP, scopes.PIPES_DROP) if access_info else []
        )
        return dropable_resources

    def get_appendable_resources(self) -> List[str]:
        access_info = self._get_access_info()
        appendable_resources = access_info.get_resources_for_scope(scopes.DATASOURCES_APPEND) if access_info else []
        return appendable_resources

    def is_admin(self) -> bool:
        return self.has_scope(scopes.ADMIN) or self.has_scope(scopes.ADMIN_USER)

    def get_user_id_from_token(self) -> Optional[str]:
        user_id = None
        access_info: Optional[AccessToken] = self._get_access_info()
        if access_info:
            user_id = next((r for r in access_info.get_resources_for_scope(scopes.ADMIN_USER)), None)
        return user_id

    @property
    def is_organization_admin(self) -> bool:
        if self._is_organization_admin is None:
            workspace = self.get_workspace_from_db()
            workspace = workspace if not workspace.is_branch_or_release_from_branch else workspace.get_main_workspace()
            user_id = self.get_user_id_from_token()
            if not user_id or not workspace or not workspace.organization_id:
                self._is_organization_admin = False
            else:
                org = Organization.get_by_id(workspace.organization_id)
                self._is_organization_admin = (
                    False if (not org or not org.user_account_ids) else user_id in org.user_account_ids
                )
        return self._is_organization_admin

    def is_admin_user(self) -> bool:
        return self.has_scope(scopes.ADMIN_USER)

    def has_scope(self, scope) -> bool:
        access_info = self._get_access_info()
        has_scope = access_info.has_scope(scope) if access_info else False
        return has_scope

    def get_resources_for_scope(self, scope) -> List[str]:
        access_info = self._get_access_info()
        resources_for_scope = access_info.get_resources_for_scope(scope) if access_info else []
        return resources_for_scope

    def options(self, *args):
        self.set_status(204)

    def set_rate_limit_headers(self):
        if self.rate_limit:
            limited, limit, remaining, retry, reset = self.rate_limit
            self.set_header("X-RateLimit-Limit", limit)
            self.set_header("X-RateLimit-Remaining", remaining)
            self.set_header("X-RateLimit-Reset", reset)
            if limited:
                self.set_header("Retry-After", retry)

    def set_default_headers(self, *args, **kwargs):
        self.set_header("X-Request-ID", str(self._request_id))
        if revision:
            self.set_header("X-Tb-R", revision)

        self.set_header("X-Frame-Options", "sameorigin")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Authorization, Content-Type, X-Requested-With, X-Tb-Warning")
        self.set_header("Access-Control-Expose-Headers", "X-Tb-Warning")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.set_header("Access-Control-Max-Age", "86400")

    def get_span(self):
        return TornadoTracing.get_span(None, self.request)

    def get_active_span(self) -> Optional[Span]:
        tracer: Tracer = self.application.settings["opentracing_tracing"].tracer
        active_span: Optional[Span] = tracer.active_span
        return active_span

    def set_span_tag(self, tags):
        span = self.get_span()
        if span:
            for k, v in tags.items():
                span.set_tag(k, v)

    def log(self, msg):
        if active_span := self.get_active_span():
            active_span.log_event(msg)

    def get_headers(self):
        headers = self.get_arguments("headers")
        headers = dict(map(str.strip, x.split(":", 1)) for x in headers)  # type: ignore[misc]
        return headers

    def get_job_output(self, job, user, debug=False):
        return {
            "id": job.id,  # For backwards compatible API
            "job_id": job.id,
            "job_url": self.application.settings["api_host"] + "/v0/jobs/" + job.id,
            "job": job.to_json(user, debug=debug),
            "status": job.status,
        }

    def get_charset_from_req_headers(self) -> Optional[str]:
        _, content_parsed = cgi.parse_header(self.request.headers.get("content-type", ""))
        return content_parsed.get("charset", None)

    def get_current_region(self) -> Optional[str]:
        available_regions = self.application.settings.get("available_regions", {}).items()
        host = self.application.settings.get("host")
        return next(
            (
                region_name
                for region_name, region_config in available_regions
                if "host" in region_config and region_config["host"] == host
            ),
            None,
        )

    def get_region_config(self, region: str) -> Dict[str, Any]:
        available_regions = self.application.settings.get("available_regions", {}).items()
        config: Dict[str, Any] = next(
            (region_config for region_name, region_config in available_regions if region_name == region), {}
        )
        region_config: dict = config.copy()
        region_config.update({"key": region})
        if "redis" in region_config:
            region_config.pop("redis")
        return region_config

    def is_from_ui(self) -> bool:
        return self.get_argument("from", None) == "ui"

    def on_connection_close(self):
        from tornado.web import _has_stream_request_body, access_log, iostream

        if _has_stream_request_body(self.__class__) and not self.request.body.done():
            self.request.body.set_exception(iostream.StreamClosedError())
            self.request.body.exception()
            request_time = 1000.0 * self.request.request_time()
            access_log.warning("%s %s %.2fms", "Conn closed", self._request_summary(), request_time)

    def _get_cli_version(self) -> Optional[version.Version]:
        cli_version = None
        argument = self.get_argument(CLI_TAG_PARAM, "")
        match = re.search(r"(\d+\.\d+\.\d+)", argument)
        if match:
            version_number = match.group()
            cli_version = version.parse(version_number)
        return cli_version

    def get_secure_cookie(self, name, value=None, max_age_days=31, min_version=None):
        self.require_setting("cookie_secret", "secure cookies")
        if value is None:
            value = self.get_cookie(name)
            # decode the value just in case it is URL-encoded
            if value:
                try:
                    value = tornado.escape.url_unescape(value)
                except Exception:
                    pass
        return super().get_secure_cookie(name, value, max_age_days, min_version)

    def _get_safe_organization(self, organization_id: str) -> Organization:
        """Gets a safe instance of the specified organization.

        Secure means: the current user has legitimate access to the org.
        """
        organization: Optional[Organization] = Organization.get_by_id(organization_id)
        assert isinstance(self.current_user, UserAccount)

        if not organization:
            raise ApiHTTPError(404, "Organization not found")

        if organization.contains_email(self.current_user.email) and not organization.user_is_admin(self.current_user):
            raise ApiHTTPError(403, "Only Organization Admins can execute this operation")

        if not organization.user_is_admin(self.current_user):
            raise ApiHTTPError(404, "Organization not found")

        return organization


class WebBaseHandler(BaseHandler):
    def write_error(self, status_code, **kwargs):
        self.set_status(status_code)
        if status_code == 403:
            self.render("403.html", status_code=status_code)
        elif status_code == 404:
            self.render("404.html", status_code=status_code)
        else:
            self.render("500.html", status_code=status_code)

    def set_default_headers(self, *args, **kwargs):
        self.set_header("X-Frame-Options", "sameorigin")
        # debug = self.application.settings["debug"]
        # self.set_header("Content-Security-Policy", ';'.join([
        #   "default-src *",
        #   # when in local webpack build uses eval for development and unsafe-inline is needed
        #   # apis.google.com -> spreadsheet export
        #   "script-src 'self' cdn.tinybird.co apis.google.com" + " 'unsafe-eval' 'unsafe-inline'" if debug else '',
        #   "object-src cdn.tinybird.co",
        #   "style-src 'self' 'unsafe-inline' 'unsafe-eval' cdn.tinybird.co fonts.googleapis.com",
        #   # googleusercontent -> avatars
        #   "img-src 'self' cdn.tinybird.co *.googleusercontent.com" ,
        #   "media-src 'none'",
        #   "frame-src 'self'",
        #   "font-src 'self' data: cdn.tinybird.co fonts.googleapis.com fonts.gstatic.com",
        #   "connect-src 'self' api.tinybird.co", #ajax to tinybird api and local
        #   "base-uri 'self'",
        #   "form-action 'self'",
        #   "frame-ancestors 'none'" # do not allow iframes or any embed
        # ]))


def doc_path_from_url(method, handler_url):
    """
    >>> doc_path_from_url('post', '/v0/datasources/?')
    '/api-reference/datasource-api.html#post--v0-datasources-?'
    >>> doc_path_from_url('get', '/v0/datasources/?')
    '/api-reference/datasource-api.html#get--v0-datasources-?'
    >>> doc_path_from_url('post', '/v0/datasources/(.+)/alter')
    '/api-reference/datasource-api.html#post--v0-datasources-(.+)-alter'
    >>> doc_path_from_url('post', '/v0/datasources/(.+)/truncate')
    '/api-reference/datasource-api.html#post--v0-datasources-(.+)-truncate'
    >>> doc_path_from_url('post', '/v0/datasources/(.+)/delete')
    '/api-reference/datasource-api.html#post--v0-datasources-(.+)-delete'
    >>> doc_path_from_url('get', '/v0/datasources/(.+)')
    '/api-reference/datasource-api.html#get--v0-datasources-(.+)'
    >>> doc_path_from_url('delete', '/v0/datasources/(.+)')
    '/api-reference/datasource-api.html#delete--v0-datasources-(.+)'
    >>> doc_path_from_url('post', '/v0/analyze/?')
    '/api-reference/datasource-api.html#post--v0-analyze-?'
    >>> doc_path_from_url('get', '/v0/pipes/?')
    '/api-reference/pipe-api.html#get--v0-pipes-?'
    >>> doc_path_from_url('post', '/v0/pipes/?')
    '/api-reference/pipe-api.html#post--v0-pipes-?'
    >>> doc_path_from_url('delete', '/v0/pipes/(.+)/nodes/(.+)')
    '/api-reference/pipe-api.html#delete--v0-pipes-(.+)-nodes-(.+)'
    >>> doc_path_from_url('put', '/v0/pipes/(.+)/nodes/(.+)')
    '/api-reference/pipe-api.html#put--v0-pipes-(.+)-nodes-(.+)'
    >>> doc_path_from_url('post', '/v0/pipes/(.+)/nodes')
    '/api-reference/pipe-api.html#post--v0-pipes-(.+)-nodes'
    >>> doc_path_from_url('put', '/v0/pipes/(.+)/endpoint')
    '/api-reference/pipe-api.html#put--v0-pipes-(.+)-endpoint'
    >>> doc_path_from_url('get', '/v0/pipes/(.+)\.(json|csv)')
    '/api-reference/pipe-api.html#get--v0-pipes-(.+)\\\\.(json|csv)'
    >>> doc_path_from_url('get', '/v0/pipes/(.+\.pipe)')
    '/api-reference/pipe-api.html#get--v0-pipes-(.+\\\\.pipe)'
    >>> doc_path_from_url('delete', '/v0/pipes/(.+\.pipe)')
    '/api-reference/pipe-api.html#delete--v0-pipes-(.+\\\\.pipe)'
    >>> doc_path_from_url('put', '/v0/pipes/(.+\.pipe)')
    '/api-reference/pipe-api.html#put--v0-pipes-(.+\\\\.pipe)'
    >>> doc_path_from_url('get', '/v0/pipes/(.+)')
    '/api-reference/pipe-api.html#get--v0-pipes-(.+)'
    >>> doc_path_from_url('delete', '/v0/pipes/(.+)')
    '/api-reference/pipe-api.html#delete--v0-pipes-(.+)'
    >>> doc_path_from_url('put', '/v0/pipes/(.+)')
    '/api-reference/pipe-api.html#put--v0-pipes-(.+)'
    >>> doc_path_from_url('get', '/v0/sql')
    '/api-reference/query-api.html#get--v0-sql'
    >>> doc_path_from_url('get', '/v0/tokens/?')
    '/api-reference/token-api.html#get--v0-tokens-?'
    >>> doc_path_from_url('post', '/v0/tokens/?')
    '/api-reference/token-api.html#post--v0-tokens-?'
    >>> doc_path_from_url('post', '/v0/tokens/(.+)/refresh')
    '/api-reference/token-api.html#post--v0-tokens-(.+)-refresh'
    >>> doc_path_from_url('get', '/v0/tokens/(.+)')
    '/api-reference/token-api.html#get--v0-tokens-(.+)'
    >>> doc_path_from_url('delete', '/v0/tokens/(.+)')
    '/api-reference/token-api.html#delete--v0-tokens-(.+)'
    >>> doc_path_from_url('put', '/v0/tokens/(.+)')
    '/api-reference/token-api.html#put--v0-tokens-(.+)'
    >>> doc_path_from_url('get', '/v0/jobs/?')
    '/api-reference/jobs-api.html#get--v0-jobs-?'
    >>> doc_path_from_url('post', '/v0/jobs/(.+)/cancel')
    '/api-reference/jobs-api.html#post--v0-jobs-(.+)-cancel'
    >>> doc_path_from_url('get', '/v0/jobs/(.+)')
    '/api-reference/jobs-api.html#get--v0-jobs-(.+)'
    >>> doc_path_from_url('get', None)
    '/api-reference/api-reference.html'

    >>> doc_path_from_url(None, '/v0/datasources/?')
    '/api-reference/datasource-api.html'
    >>> doc_path_from_url(None, '/v0/datasources/?')
    '/api-reference/datasource-api.html'
    >>> doc_path_from_url(None, '/v0/datasources/(.+)/alter')
    '/api-reference/datasource-api.html'
    >>> doc_path_from_url(None, '/v0/datasources/(.+)/truncate')
    '/api-reference/datasource-api.html'
    >>> doc_path_from_url(None, '/v0/datasources/(.+)/delete')
    '/api-reference/datasource-api.html'
    >>> doc_path_from_url(None, '/v0/datasources/(.+)')
    '/api-reference/datasource-api.html'
    >>> doc_path_from_url(None, '/v0/datasources/(.+)')
    '/api-reference/datasource-api.html'
    >>> doc_path_from_url(None, '/v0/analyze/?')
    '/api-reference/datasource-api.html'
    >>> doc_path_from_url(None, '/v0/pipes/?')
    '/api-reference/pipe-api.html'
    >>> doc_path_from_url(None, '/v0/pipes/?')
    '/api-reference/pipe-api.html'
    >>> doc_path_from_url(None, '/v0/pipes/(.+)/nodes/(.+)')
    '/api-reference/pipe-api.html'
    >>> doc_path_from_url(None, '/v0/pipes/(.+)/nodes/(.+)')
    '/api-reference/pipe-api.html'
    >>> doc_path_from_url(None, '/v0/pipes/(.+)/nodes')
    '/api-reference/pipe-api.html'
    >>> doc_path_from_url(None, '/v0/pipes/(.+)/endpoint')
    '/api-reference/pipe-api.html'
    >>> doc_path_from_url(None, '/v0/pipes/(.+)\.(json|csv)')
    '/api-reference/pipe-api.html'
    >>> doc_path_from_url(None, '/v0/pipes/(.+\.pipe)')
    '/api-reference/pipe-api.html'
    >>> doc_path_from_url(None, '/v0/pipes/(.+\.pipe)')
    '/api-reference/pipe-api.html'
    >>> doc_path_from_url(None, '/v0/pipes/(.+\.pipe)')
    '/api-reference/pipe-api.html'
    >>> doc_path_from_url(None, '/v0/pipes/(.+)')
    '/api-reference/pipe-api.html'
    >>> doc_path_from_url(None, '/v0/pipes/(.+)')
    '/api-reference/pipe-api.html'
    >>> doc_path_from_url(None, '/v0/pipes/(.+)')
    '/api-reference/pipe-api.html'
    >>> doc_path_from_url(None, '/v0/sql')
    '/api-reference/query-api.html'
    >>> doc_path_from_url(None, '/v0/tokens/?')
    '/api-reference/token-api.html'
    >>> doc_path_from_url(None, '/v0/tokens/?')
    '/api-reference/token-api.html'
    >>> doc_path_from_url(None, '/v0/tokens/(.+)/refresh')
    '/api-reference/token-api.html'
    >>> doc_path_from_url(None, '/v0/tokens/(.+)')
    '/api-reference/token-api.html'
    >>> doc_path_from_url(None, '/v0/tokens/(.+)')
    '/api-reference/token-api.html'
    >>> doc_path_from_url(None, '/v0/tokens/(.+)')
    '/api-reference/token-api.html'
    >>> doc_path_from_url(None, '/v0/jobs/?')
    '/api-reference/jobs-api.html'
    >>> doc_path_from_url(None, '/v0/jobs/(.+)/cancel')
    '/api-reference/jobs-api.html'
    >>> doc_path_from_url(None, '/v0/jobs/(.+)')
    '/api-reference/jobs-api.html'
    >>> doc_path_from_url(None, None)
    '/api-reference/api-reference.html'
    """
    try:
        url = urlparse(handler_url)

        api_map = {"events": "datasource", "analyze": "datasource", "sql": "query", "job": "jobs"}

        api = f"{url.path.split('/')[2].rstrip('/').rstrip('s')}"
        api = api_map.get(api, api)

        path_parts = handler_url.split("/")
        path = "-".join(path_parts)

        if method:
            doc = f"/api-reference/{api}-api.html#{method.lower()}-{path}"
        else:
            doc = f"/api-reference/{api}-api.html"
        return doc
    except Exception:
        return "/api-reference/api-reference.html"


def cookie_domain(request: BaseHandler) -> str:
    if "//" not in request.application.settings["host"]:
        return request.application.settings["host"]

    domain = request.application.settings["host"].split("//")[1]
    # remove port
    if ":" in domain:
        domain = domain.split(":")[0]
    # remove subdomain
    if "." in domain:
        domain = ".".join(domain.split(".")[-2:])
    # allow to access form subdomains
    return domain


def _calculate_edited_by(access_token: Optional[AccessToken]) -> Optional[str]:
    if not access_token:
        return None

    if access_token.has_scope(scopes.ADMIN_USER):
        return access_token.name.split(" ")[1]
    else:
        return f"token: '{access_token.name}'"
