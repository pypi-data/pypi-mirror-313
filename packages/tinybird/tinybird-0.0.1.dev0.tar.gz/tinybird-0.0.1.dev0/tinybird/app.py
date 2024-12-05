import asyncio
import errno
import logging
import multiprocessing
import os
import re
import signal
import socket
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from multiprocessing.process import current_process
from typing import Any, Optional

import click
import requests
import sentry_sdk
import tornado.autoreload
import tornado.ioloop
import tornado.web
import tornado_opentracing
from sentry_sdk import Hub
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.tornado import TornadoIntegration
from tornado.httpserver import HTTPServer
from tornado.netutil import _ERRNO_WOULDBLOCK
from tornado.platform.auto import set_close_exec
from tornado.util import errno_from_exception
from tornado.web import url

from tinybird.bi_connector.services import set_bi_management_password
from tinybird.campaigns_service import CampaignsService
from tinybird.copy_pipes.services import set_predefined_replicas_configuration_for_copy
from tinybird.data_sinks.tracker import get_sinks_append_token, sinks_tracker
from tinybird.gc_scheduler.scheduler_jobs import GCloudScheduler
from tinybird.hfi.hfi_settings import hfi_settings
from tinybird.ingest.cdk_utils import CDKUtils
from tinybird.ingest.preview_connectors.yepcode_utils import set_yepcode_configuration
from tinybird.ingestion_observer import IngestionObserver
from tinybird.integrations.vercel import VercelIntegrationService
from tinybird.internal_thread import (
    PlanLimitsTracker,
    UsageMetricsTracker,
    UsageRecordsTracker,
    WorkspaceDatabaseUsageTracker,
)
from tinybird.kafka_utils import KafkaServerGroupsConfig
from tinybird.lag_monitor import LagMonitor
from tinybird.notifications_service import NotificationsService
from tinybird.orb_service import OrbService
from tinybird.organization.organization import Organization
from tinybird.providers.auth import (
    AuthenticationProvider,
    AWSAuthenticationProvider,
    GCPAuthenticationProvider,
    register_auth_provider,
)
from tinybird.raw_events.raw_events_batcher import raw_events_batcher
from tinybird.redis_config import get_redis_config
from tinybird.regions_service import RegionsService
from tinybird.tokens import AccessToken
from tinybird.tracker import DatasourceOpsTrackerRegistry
from tinybird.useraccounts_service import UserAccountsService
from tinybird.views import (
    api_active_campaigns,
    api_auth,
    api_data_linkers,
    api_explorations,
    api_integrations,
    api_organizations,
    api_templates,
)
from tinybird.views.aiohttp_shared_session import get_shared_session_task
from tinybird.views.exploration import ExplorationHandler
from tinybird.views.git_integrations.github import (
    GitHubIntegrationAuthorizeHandler,
    GitHubIntegrationInitHandler,
    GitHubIntegrationRedirectHandler,
)
from tinybird.views.integrations.vercel import (
    ConfigureVercelIntegrationRedirectHandler,
    NewVercelIntegrationRedirectHandler,
    SelectRegionVercelIntegrationRedirectHandler,
    VercelWebhookHandler,
)
from tinybird.watchdog import TBWatchdog
from tinybird_shared.metrics.statsd_client import statsd_client
from tinybird_shared.redis_client.redis_client import TBRedisClientSync, async_redis, async_redis_limits

from .csv_processing_queue import CsvChunkQueueRegistry
from .default_tables import (
    DEFAULT_METRICS_CLUSTER_TABLES,
    DEFAULT_METRICS_CLUSTER_VIEWS,
    DEFAULT_METRICS_TABLES,
    DEFAULT_METRICS_VIEWS,
    DEFAULT_TABLES,
)
from .default_timeouts import (
    set_socket_connect_timeout,
    set_socket_read_timeout,
    set_socket_total_timeout,
    socket_connect_timeout,
    socket_read_timeout,
    socket_total_timeout,
)
from .feature_flags import FeatureFlagsService
from .internal_resources import CH_INTERNAL_ADDRESS, INTERNAL_CLUSTER, init_internal_tables, init_metrics_tables
from .job import Job, JobExecutor, WipJobsQueueRegistry
from .limits import Limit, Limits
from .model import RedisModel
from .monitor import Monitor
from .pg import PGPool
from .plans import configure_stripe
from .shutdown import ShutdownApplicationStatus
from .tracing import ClickhouseTracer
from .tracker import QueryLogTracker
from .user import User, UserAccount, Users, public
from .views import (
    api_auth_connections,
    api_billing,
    api_branches,
    api_chart_presets,
    api_data_connections,
    api_data_connectors,
    api_datafiles,
    api_datasources_admin,
    api_datasources_credentials,
    api_datasources_import,
    api_datasources_scheduling,
    api_internals,
    api_jobs,
    api_meta,
    api_pipes,
    api_playground,
    api_query,
    api_regions,
    api_tags,
    api_tokens,
    api_variables,
    api_workspaces,
    tunnel,
)
from .views.admin import (
    ActivateUserAccountAdminHandler,
    AdminHandler,
    BranchesAdminHandler,
    DebugImports,
    DebugQueues,
    DebugStatus,
    RegisterUserAdminHandler,
    RegisterWorkspaceAdminHandler,
    ReplicasStatus,
    UserAccountAdminHandler,
    UserAccountsAdminHandler,
    WorkspaceAdminHandler,
    WorkspacesAdminHandler,
)
from .views.admin_clusters import ClusterSettingsAdminHandler
from .views.admin_organization import OrganizationAdminHandler, OrganizationsAdminHandler
from .views.app import AppHtmlHandler
from .views.auth.auth0 import Auth0OAuth2LoginHandler
from .views.auth.workspaces import WorkspacesLoginHandler, WorkspaceStarterKitRedirectHandler
from .views.base import CustomStaticHandler, WebBaseHandler
from .views.endpoint import EndpointHtmlHandler, EndpointsHtmlHandler
from .views.examples import DocsClientHandler, ExamplesQueryHandler, SnippetQueryHandler
from .views.login import CheckSessionHandler, LoginErrorHandler, LogoutHandler, SignupHandler
from .views.mailgun import MailgunService
from .views.pipeline import PipeMdHandler, PipeStaticHtmlHandler

UUID_REGEX = r"(\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b)"
SEMVER_REGEX = r"(\d+\.\d+\.\d+(-(snapshot|\d+))?)"
DEFAULT_APP_NAME = "unknown"
LAG_MONITOR_THRESHOLD_RELEASE_IN_SECS = 0.15
LAG_MONITOR_THRESHOLD_DEBUG_IN_SECS = 1

monitor: Monitor
monitor_task = None
query_log_tracker_task: Optional[asyncio.Task] = None
lag_monitor: LagMonitor
query_log_tracker: Optional[QueryLogTracker] = None
ingestion_observer = None
watchdog: Optional[TBWatchdog] = None


class TinybirdHTTPServer(HTTPServer):
    def stop(self):
        """Stops listening for new connections.

        Requests currently in progress may still continue after the
        server is stopped.
        """
        if self._stopped:
            return
        self._stopped = True

        # The idea is to drain the sockets' connections queue by:
        # (1) accept all pending connections in the sockets and save them for later processing,
        # (2) close the sockets to not receive new connections,
        # (3) and, finally, process the outstading connections after we have closed the sockets.

        pending_conn = []

        # See https://github.com/tornadoweb/tornado/blob/v5.1.1/tornado/tcpserver.py#L224
        for fd, sock in self._sockets.items():
            assert sock.fileno() == fd

            # See https://github.com/tornadoweb/tornado/blob/v5.1.1/tornado/netutil.py#L211
            # The MAGIC NUMBER represents a high enough number to drain the sockets under normal circumstances. We want
            # to avoid a while True condition just in case there is a flood of new connections and we can't exit the
            # condition/loop.
            for _ in range(128):  # MAGIC NUMBER
                try:
                    pending_conn.append(sock.accept())
                except socket.error as e:
                    # _ERRNO_WOULDBLOCK indicate we have accepted every
                    # connection that is available.
                    if errno_from_exception(e) in _ERRNO_WOULDBLOCK:
                        break
                    # ECONNABORTED indicates that there was a connection
                    # but it was closed while still in the accept queue.
                    # (observed on FreeBSD).
                    if errno_from_exception(e) == errno.ECONNABORTED:
                        continue
                    raise

            # Unregister socket from IOLoop
            self._handlers.pop(fd)()
            sock.close()

        for connection, address in pending_conn:
            logging.info(f"processing connection from address {address}")
            set_close_exec(connection.fileno())
            self._handle_connection(connection, address)


def uri_is_interna_or_from_api(uri: str) -> bool:
    if uri is None:
        return False

    api_regex = re.compile(r"^/v[0-9]*/")
    if api_regex.match(uri):
        return True

    if uri.startswith("/internal"):
        return True

    return False


# https://docs.python-requests.org/en/master/user/quickstart/#timeouts
old_send = requests.Session.send


def global_patch_for_requests_timeout(timeout=None):
    # We can't use default values for the timeout var because they're evaluated at the very beginning, not every single
    # call. Thus, if we want to have updated values, we need to make sure we actually read them just in time.
    if not timeout:
        timeout = (socket_connect_timeout(), socket_read_timeout())

    def new_send(*args, **kwargs):
        if kwargs.get("timeout", None) is None:
            # (connect_timeout, between bytes timeout)
            kwargs["timeout"] = timeout
        return old_send(*args, **kwargs)

    # Allow calling the patch method multiple times without incurring into recursion
    if requests.Session.send != new_send:
        global old_send
        requests.Session.send = new_send

    Limit.requests_connect_timeout = timeout[0]
    Limit.requests_bytes_between_timeout = timeout[1]


class ErrorHandler(WebBaseHandler):
    def get(self, *args, **kwargs):
        if uri_is_interna_or_from_api(self.request.uri):
            self.set_status(404)
            self.write(
                {
                    "error": "API method not found, check the API reference for available methods",
                    "documentation": "https://docs.tinybird.co/api-reference/api-reference.html",
                }
            )
        else:
            self.set_status(404)
            self.render("404.html")


class RedirectDashboardHandler(WebBaseHandler):
    def get(self):
        workspace = self.get_workspace_from_db()
        if workspace:
            self.redirect(self.reverse_url("workspace_dashboard", workspace.id))
            return

        user = self.get_user_from_db()
        if user:
            self.redirect(self.reverse_url("workspace_dashboard", user.id))
            return

        self.redirect("/login")
        return


class RedirectTimeseriesHandler(WebBaseHandler):
    def get(self):
        workspace = self.get_workspace_from_db()
        if not workspace:
            self.redirect("/login")
            return
        self.redirect(self.reverse_url("workspace_timeseries_all", workspace.id))


class RedirectTokensHandler(WebBaseHandler):
    def get(self):
        workspace = self.get_workspace_from_db()
        if not workspace:
            self.redirect("/login")
            return
        self.redirect(self.reverse_url("workspace_tokens_all", workspace.id))


class RedirectResourcesHandler(WebBaseHandler):
    def get(self, id):
        user = self.get_user_from_db()
        if not user:
            self.redirect("/login")
            return
        self.redirect(f"/{user.id}{self.request.path}")


class DocsHandler(WebBaseHandler):
    def get(self):
        docs_host = self.application.settings["docs_host"]
        self.redirect(docs_host)


class ChangelogHandler(WebBaseHandler):
    def get(self):
        self.redirect("https://www.tinybird.co/changelog")


class OpenapiHandler(WebBaseHandler):
    def get(self, *args, **kwargs):
        self.render("openapi.html")


class Application(tornado.web.Application):
    def __init__(self, conf=None, tracer=None) -> None:
        settings = {}
        if conf:
            settings.update(conf)
        self.tracer = tracer

        if settings.get("enable_tracing", False):
            if not tracer:
                logging.fatal("Application tracing requested without passing a tracer")
            u = public.get_public_user()
            if u is None:
                raise Exception("Could not get the internal user")
            t = Users.get_datasource(u, "spans")
            if t is None:
                raise Exception(f"Could not get the spans table for Workspace {u.name}")
            self.tracer.set_logging_clickhouse(
                host=u["database_server"],
                database=u["database"],
                table=t.id,
                async_insert=settings.get("async_insert_internal", False),
            )

        try:
            if public.get_public_user().organization_id:
                logging.error("Public user should not have an organization_id")
        except Exception as ex:
            logging.exception(f"Error while checking public user organization: {str(ex)}")

        settings["static_handler_class"] = CustomStaticHandler

        handlers = []

        handlers += api_internals.handlers()

        # API
        handlers += api_playground.handlers()
        handlers += api_datafiles.handlers()
        handlers += api_organizations.handlers()
        handlers += api_tokens.handlers()
        handlers += api_variables.handlers()
        handlers += api_query.handlers()
        handlers += api_datasources_scheduling.handlers()
        handlers += api_datasources_import.handlers()
        handlers += api_datasources_admin.handlers()
        handlers += api_datasources_credentials.handlers()
        handlers += api_jobs.handlers()
        handlers += api_pipes.handlers()
        handlers += api_workspaces.handlers()
        handlers += api_branches.handlers()
        handlers += api_explorations.handlers()
        handlers += api_integrations.handlers()
        handlers += api_data_connections.handlers()
        handlers += api_data_connectors.handlers()
        handlers += api_data_linkers.handlers()
        handlers += api_regions.handlers()
        handlers += api_billing.handlers()
        handlers += api_active_campaigns.handlers()
        handlers += api_auth_connections.handlers()
        handlers += api_templates.handlers()
        handlers += api_auth.handlers()
        handlers += api_chart_presets.handlers()
        handlers += api_meta.handlers()
        handlers += api_tags.handlers()
        handlers += tunnel.handlers()

        workspace_handlers = [
            url(rf"/{UUID_REGEX}/dashboard", AppHtmlHandler, name="workspace_dashboard"),
            url(rf"/{UUID_REGEX}/datasource/(.*)", AppHtmlHandler, name="workspace_datasource"),
            url(rf"/{UUID_REGEX}/datasource-preview/(.*)", AppHtmlHandler, name="workspace_datasource_preview"),
            url(rf"/{UUID_REGEX}/pipe/(.*)", AppHtmlHandler, name="workspace_pipe"),
            url(rf"/{UUID_REGEX}/pipes", AppHtmlHandler, name="workspace_pipes_all"),
            url(rf"/{UUID_REGEX}/pipe/(.*)/nodes/(.*)", AppHtmlHandler, name="workspace_pipe_node"),
            url(rf"/{UUID_REGEX}/pipes/(.*)", AppHtmlHandler, name="workspace_pipes"),
            url(rf"/{UUID_REGEX}/datasources", AppHtmlHandler, name="workspace_datasources_all"),
            url(rf"/{UUID_REGEX}/datasources/(.*)", AppHtmlHandler, name="workspace_datasources"),
            url(rf"/{UUID_REGEX}/releases", AppHtmlHandler, name="workspace_releases"),
            url(rf"/{UUID_REGEX}/diffs", AppHtmlHandler, name="workspace_changes"),
            url(rf"/{UUID_REGEX}/tokens", AppHtmlHandler, name="workspace_tokens_all"),
            url(rf"/{UUID_REGEX}/tokens/(.*)", AppHtmlHandler, name="workspace_tokens"),
            url(rf"/{UUID_REGEX}/graph", AppHtmlHandler, name="workspace_graph"),
            url(rf"/{UUID_REGEX}/playground", AppHtmlHandler, name="workspace_playground_all"),
            url(rf"/{UUID_REGEX}/playground/(.*)", AppHtmlHandler, name="workspace_playground"),
            url(rf"/{UUID_REGEX}/timeseries", AppHtmlHandler, name="workspace_timeseries_all"),
            url(rf"/{UUID_REGEX}/timeseries/(.*)", AppHtmlHandler, name="workspace_timeseries"),
            url(rf"/{UUID_REGEX}/timeseries/onboarding", AppHtmlHandler, name="workspace_timeseries_onboarding"),
            url(rf"/{UUID_REGEX}/timeseries/new", AppHtmlHandler, name="workspace_timeseries_new"),
            url(rf"/{UUID_REGEX}/settings", AppHtmlHandler, name="workspace_settings"),
            url(rf"/{UUID_REGEX}/settings/(.*)", AppHtmlHandler, name="workspace_settings_option"),
            url(rf"/{UUID_REGEX}/git", AppHtmlHandler, name="workspace_git"),
            url(rf"/{UUID_REGEX}/git-settings", AppHtmlHandler, name="workspace_git_settings"),
            url(rf"/{UUID_REGEX}/new-workspace", AppHtmlHandler, name="new_workspace"),
            url(rf"/{UUID_REGEX}/region", AppHtmlHandler, name="workspace_region"),
            url(rf"/{UUID_REGEX}/upgrade", AppHtmlHandler, name="workspace_upgrade"),
        ]

        workspace_semver_handlers = [
            url(rf"/{UUID_REGEX}/{SEMVER_REGEX}/dashboard", AppHtmlHandler, name="workspace_semver_dashboard"),
            url(rf"/{UUID_REGEX}/{SEMVER_REGEX}/datasource/(.*)", AppHtmlHandler, name="workspace_semver_datasource"),
            url(
                rf"/{UUID_REGEX}/{SEMVER_REGEX}/datasource-preview/(.*)",
                AppHtmlHandler,
                name="workspace_semver_datasource_preview",
            ),
            url(rf"/{UUID_REGEX}/{SEMVER_REGEX}/pipe/(.*)", AppHtmlHandler, name="workspace_semver_pipe"),
            url(rf"/{UUID_REGEX}/{SEMVER_REGEX}/pipes", AppHtmlHandler, name="workspace_semver_pipes_all"),
            url(
                rf"/{UUID_REGEX}/{SEMVER_REGEX}/pipe/(.*)/nodes/(.*)", AppHtmlHandler, name="workspace_semver_pipe_node"
            ),
            url(rf"/{UUID_REGEX}/{SEMVER_REGEX}/pipes/(.*)", AppHtmlHandler, name="workspace_semver_pipes"),
            url(rf"/{UUID_REGEX}/{SEMVER_REGEX}/datasources", AppHtmlHandler, name="workspace_semver_datasources_all"),
            url(rf"/{UUID_REGEX}/{SEMVER_REGEX}/datasources/(.*)", AppHtmlHandler, name="workspace_semver_datasources"),
            url(rf"/{UUID_REGEX}/{SEMVER_REGEX}/releases", AppHtmlHandler, name="workspace_semver_releases"),
            url(rf"/{UUID_REGEX}/{SEMVER_REGEX}/diffs", AppHtmlHandler, name="workspace_semver_changes"),
            url(rf"/{UUID_REGEX}/{SEMVER_REGEX}/tokens", AppHtmlHandler, name="workspace_semver_tokens_all"),
            url(rf"/{UUID_REGEX}/{SEMVER_REGEX}/tokens/(.*)", AppHtmlHandler, name="workspace_semver_tokens"),
            url(rf"/{UUID_REGEX}/{SEMVER_REGEX}/graph", AppHtmlHandler, name="workspace_semver_graph"),
            url(rf"/{UUID_REGEX}/{SEMVER_REGEX}/playground", AppHtmlHandler, name="workspace_semver_playground_all"),
            url(rf"/{UUID_REGEX}/{SEMVER_REGEX}/playground/(.*)", AppHtmlHandler, name="workspace_semver_playground"),
            url(rf"/{UUID_REGEX}/{SEMVER_REGEX}/timeseries", AppHtmlHandler, name="workspace_semver_timeseries_all"),
            url(rf"/{UUID_REGEX}/{SEMVER_REGEX}/timeseries/(.*)", AppHtmlHandler, name="workspace_semver_timeseries"),
            url(
                rf"/{UUID_REGEX}/{SEMVER_REGEX}/timeseries/onboarding",
                AppHtmlHandler,
                name="workspace_semver_timeseries_onboarding",
            ),
            url(
                rf"/{UUID_REGEX}/{SEMVER_REGEX}/timeseries/new", AppHtmlHandler, name="workspace_semver_timeseries_new"
            ),
            url(rf"/{UUID_REGEX}/{SEMVER_REGEX}/settings", AppHtmlHandler, name="workspace_semver_settings"),
            url(
                rf"/{UUID_REGEX}/{SEMVER_REGEX}/settings/(.*)",
                AppHtmlHandler,
                name="workspace_semver_settings_option",
            ),
            url(rf"/{UUID_REGEX}/{SEMVER_REGEX}/git", AppHtmlHandler, name="workspace_semver_git"),
            url(rf"/{UUID_REGEX}/{SEMVER_REGEX}/git-settings", AppHtmlHandler, name="workspace_semver_git_settings"),
            url(rf"/{UUID_REGEX}/{SEMVER_REGEX}/region", AppHtmlHandler, name="workspace_semver_region"),
        ]

        handlers += workspace_handlers
        handlers += workspace_semver_handlers

        handlers += [
            # commercial web
            url(r"/", RedirectDashboardHandler),
            (r"/cheriff", AdminHandler),
            url(r"/cheriff/queues", DebugQueues, name="queues_debug"),
            url(r"/cheriff/imports", DebugImports, name="imports_debug"),
            url(r"/cheriff/status", DebugStatus, name="status_debug"),
            url(r"/cheriff/replicas", ReplicasStatus, name="replicas_status"),
            url(r"/cheriff/branches/(.+)?", BranchesAdminHandler, name="branches_admin"),
            url(r"/cheriff/users/register", RegisterUserAdminHandler, name="users_admin_register"),
            url(r"/cheriff/users/activate", ActivateUserAccountAdminHandler, name="user_account_admin_activate"),
            url(r"/cheriff/users/(.+)?", UserAccountsAdminHandler, name="user_accounts_admin"),
            url(r"/cheriff/user/(.+)", UserAccountAdminHandler, name="user_account_admin"),
            url(r"/cheriff/workspaces/register", RegisterWorkspaceAdminHandler, name="workspaces_admin_register"),
            url(r"/cheriff/workspaces/(.+)?", WorkspacesAdminHandler, name="workspaces_admin"),
            url(r"/cheriff/workspace/(.+)", WorkspaceAdminHandler, name="workspace_admin"),
            url(r"/cheriff/organizations", OrganizationsAdminHandler, name="organizations_admin"),
            url(r"/cheriff/organization/(.+)", OrganizationAdminHandler, name="organization_admin"),
            url(r"/cheriff/clusters", ClusterSettingsAdminHandler, name="clusters_admin"),
            url(r"/login", Auth0OAuth2LoginHandler, name="login"),
            url(r"/login_error", LoginErrorHandler, name="login_error"),
            url(r"/check_session", CheckSessionHandler, name="check_session"),
            url(r"/signup", SignupHandler, name="signup"),
            url(r"/logout", LogoutHandler, name="logout"),
            url(r"/docs", DocsHandler),
            url(r"/changelog", ChangelogHandler),
            url(r"/openapi", OpenapiHandler),
            url(r"/workspaces/new", WorkspaceStarterKitRedirectHandler, name="workspace_starter_kit_redirect"),
            url(r"/workspaces", WorkspacesLoginHandler, name="workspaces"),
            # Vercel integration
            url(
                r"/integrations/vercel/new", NewVercelIntegrationRedirectHandler, name="new_vercel_integration_redirect"
            ),
            url(
                r"/integrations/vercel/(.+)/new",
                ConfigureVercelIntegrationRedirectHandler,
                name="configure_vercel_integration",
            ),
            url(r"/integrations/vercel/webhook", VercelWebhookHandler, name="integrations_vercel_webhook"),
            url(r"/integrations/vercel", AppHtmlHandler, name="integrations_vercel_projects"),
            url(
                r"/integrations/vercel/region",
                SelectRegionVercelIntegrationRedirectHandler,
                name="select_region_vercel_integration",
            ),
            # ui
            url(r"/dashboard", RedirectDashboardHandler, name="dashboard"),
            url(r"/datasource/(.*)", RedirectResourcesHandler, name="datasource"),
            url(r"/endpoints", EndpointsHtmlHandler, name="pipe_endpoints"),
            url(r"/endpoint/(.*)", EndpointHtmlHandler, name="pipe_endpoint"),
            url(r"/pipe/(.+\.md)", PipeMdHandler),
            url(r"/pipe/(.+)/static", PipeStaticHtmlHandler),
            url(r"/pipe/(.*)", RedirectResourcesHandler, name="pipe"),
            url(r"/tokens", RedirectTokensHandler, name="tokens"),
            url(r"/organizations/(.*)/overview", AppHtmlHandler, name="organization_overview"),
            url(r"/organizations/(.*)/commitment", AppHtmlHandler, name="organization_commitment"),
            url(r"/organizations/(.*)/workspaces", AppHtmlHandler, name="organization_workspaces"),
            url(r"/organizations/(.*)/members", AppHtmlHandler, name="organization_members"),
            url(r"/organizations/(.*)/monitoring", AppHtmlHandler, name="organization_monitoring"),
            url(r"/stripe", api_billing.APIStripeWebhook, name="stripe_webhook"),
            url(r"/orb", api_billing.APIOrbWebhook, name="orb_webhook"),
            url(r"/timeseries", RedirectTimeseriesHandler, name="timeseries"),
            url(r"/timeseries/(.+)", ExplorationHandler, name="public_timeseries"),
            # Git integrations
            url(r"/git-integrations/github", GitHubIntegrationRedirectHandler, name="github_integration_redirect"),
            url(r"/git-integrations/github-init", GitHubIntegrationInitHandler, name="github_integration_init"),
            url(
                r"/git-integrations/github-authorize",
                GitHubIntegrationAuthorizeHandler,
                name="github_integration_authorize",
            ),
            (r"/examples/query\.(.*)", ExamplesQueryHandler),
            # user management
            (r"/examples/snippet", SnippetQueryHandler),
            (r"/docs/client.js", DocsClientHandler),
            # CDN
            url(
                r"/v1/(tinybird\.js)", tornado.web.StaticFileHandler, kwargs=dict(path=settings["static_path"] + "/js")
            ),
            # local docs
            # url(r"/docs/(.*)", tornado.web.StaticFileHandler, kwargs=dict(
            # path=os.path.join(os.path.dirname(__file__), "..", "docs", "build", "html"),
            # default_filename="index.html"
            # ))
        ]

        if settings.get("e2e_ui_tests") == "speedwins":
            from tinybird.views.api_auth import APIAuthFakeLoginHandler, APIAuthFakeSignupHandler
            from tinybird.views.integrations.vercel import FakeNewVercelIntegrationRedirectHandler

            handlers += [
                url(r"/v0/auth/fake_login", APIAuthFakeLoginHandler),
                url(r"/v0/auth/fake_signup", APIAuthFakeSignupHandler),
                url(
                    r"/fake_integrations/vercel/new/(.+)",
                    FakeNewVercelIntegrationRedirectHandler,
                    name="fake_integrations_vercel_new",
                ),
            ]

        super().__init__(handlers, **settings)

    def log_request(self, handler: tornado.web.RequestHandler) -> None:
        """
        Override tornado's log_request function to write to our dedicated logger & inject labels.
        """

        tb_webserver_access_logger = logging.getLogger("tb.web.access")

        if "log_function" in self.settings:
            self.settings["log_function"](handler)
            return
        if handler.get_status() < 400:
            log_method = tb_webserver_access_logger.info
        elif handler.get_status() < 500:
            log_method = tb_webserver_access_logger.warning
        else:
            log_method = tb_webserver_access_logger.error
        log_labels = dict(
            method=handler.request.method,
            status_code=handler.get_status(),
            remote_ip=handler.request.remote_ip,
            endpoint=handler.request.path,
            # We are not 100% sure all handlers here extend basehandler so we need to check if the fields exist
            request_id=handler._request_id if hasattr(handler, "_request_id") else None,
            nginx_request_id=handler._nginx_request_id if hasattr(handler, "_nginx_request_id") else None,
        )
        request_time = 1000.0 * handler.request.request_time()
        log_method("%d %s %.2fms", handler.get_status(), handler._request_summary(), request_time, extra=log_labels)


def make_app_dummy():
    """
    create a dummy app just to introspect endpoints for documentation
    """
    tracer = ClickhouseTracer()
    conf = {
        "port": 8000,
        "enable_tracing": False,
        "default_handler_class": ErrorHandler,
        "opentracing_tracing": tornado_opentracing.TornadoTracing(tracer),
    }
    import tinybird.default_secrets

    conf.update(tinybird.default_secrets.conf(conf))
    return Application(conf, tracer)


def make_app(settings=None):
    if settings is None:
        settings = {"port": 8000}

    def start_span_cb(span, request):
        request_id = request.headers.get("x-request-id", None)
        if request_id:
            span.context.span_id = request_id

    tracer = ClickhouseTracer()
    conf = settings
    conf.update(
        {
            "default_handler_class": ErrorHandler,
            "opentracing_tracing": tornado_opentracing.TornadoTracing(tracer),
            "opentracing_start_span_cb": start_span_cb,  # This overrides the TornadoTracing constructor
        }
    )
    # Initialize tracing before creating the Application object
    if settings.get("enable_tracing", False):
        tornado_opentracing.init_tracing()

    FeatureFlagsService.configured_domain = conf["domain"]
    return Application(conf, tracer)


def get_config(config_file=None, port=None, app_name=None):
    conf = {
        "port": port,
        "enable_tracing": True,
        "app_name": app_name,
    }
    import tinybird.default_secrets

    conf.update(tinybird.default_secrets.conf(conf))

    import importlib.util

    if config_file:
        try:
            spec = importlib.util.spec_from_file_location("tinybird.settings", config_file)
            settings = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(settings)
        except Exception as e:
            logging.error("failed to load configuration: %s" % e)
        conf.update(settings.conf(conf))
    return conf


def warm_up_processes(x):
    return x * x


def conf_sentry(conf, server):
    sentry_conf = conf.get("sentry")
    if sentry_conf and sentry_conf.get("analytics_dsn"):
        sentry_logging = LoggingIntegration(
            level=logging.INFO,  # Capture info and above as breadcrumbs
            event_level=logging.ERROR,  # Send errors as events
        )
        # Get release version
        try:
            from . import revision

            release = revision
        except ImportError:
            logging.warning("Release tag not found")
            release = sentry_conf.get("revision", "unknown_release")

        # set service tag to all events
        service = "server" if server else "job"

        def before_send(event, hint):
            event.setdefault("tags", {})["service"] = service
            return event

        def traces_sampler(sampling_context):
            return float(sentry_conf.get("traces_sample_rate", 0))

        sentry_sdk.init(
            sentry_conf.get("analytics_dsn"),
            environment=sentry_conf.get("environment"),
            release=release,
            before_send=before_send,
            traces_sampler=traces_sampler,
            integrations=[sentry_logging, TornadoIntegration(), RedisIntegration(), AioHttpIntegration()],
        )


def shutdown_sentry():
    client = Hub.current.client
    if client is not None:
        client.close(timeout=2.0)


def is_reader(app_name):
    return "read" in app_name


def setup(conf, start_tb_service):
    from tinybird.utils.log import configure_logging

    # Readers are single-process, so there's no need to have the extra coordinator process:
    # multiprocessing.resource_tracker import main;main(11)
    if not is_reader(conf["app_name"]):
        multiprocessing.set_start_method("spawn")

    is_debug = conf.get("debug", False)

    configure_logging(conf["app_name"], is_debug)
    conf_sentry(conf, start_tb_service)
    configure_stripe(conf)


@click.command()
@click.option("--config", type=click.Path(exists=True), help="configuration file.")
@click.option("--port", default=8000, help="listen port")
@click.option("--consumer/--no-consumer", is_flag=True, default=True, help="Set server as a Job Consumer")
@click.option(
    "--start-tb-service/--no-start-tb-service",
    is_flag=True,
    default=True,
    help="Start the HTTP server to handle Tinybird Analytics requests",
)
@click.option("--multi-port", default=1, help="Listen in n consecutive ports")
@click.option("--app-name", default=DEFAULT_APP_NAME, help="application name used for statsd reports")
@click.option("--dev/--no-dev", default=True, help="Development mode: Create internal tables")
@click.option("--test/--no-test", default=False, help="Test mode: Use separate port for internal HFI calls")
@click.option(
    "--send-batched-records/--no-send-batched-records",
    default=True,
    help="Do not send batched records in DataSourceRecordsBatcher implementations",
)
def run(config, port, consumer, start_tb_service, multi_port, app_name, dev, test, send_batched_records):
    conf = get_config(config_file=config, port=port, app_name=app_name)
    setup(conf, start_tb_service)

    is_debug = conf.get("debug", False)

    # load models before doing any logic
    if "default_database_server" in conf:
        User.default_database_server = conf["default_database_server"]

    if "internal_database_server" in conf:
        User.internal_database_server = conf["internal_database_server"]

    if "default_cluster" in conf:
        User.default_cluster = conf["default_cluster"]

    if "default_plan" in conf:
        User.default_plan = conf["default_plan"]

    # Override Owner Max. Children for DataSink Jobs from config value
    Job.override_owner_max_children(conf.get("jobs_ownermaxchildren", 100))

    redis_config = get_redis_config(conf)

    redis_client = TBRedisClientSync(redis_config)

    RedisModel.config(redis_client)

    # If not defined `replace_executor_max_workers`, we let the ThreadPoolExecutor to decide the number of max_workers needed.
    max_workers = conf.get("replace_executor_max_workers", None)
    replace_queries_executor = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="replace_query")
    logging.info(
        f"The replace queries executor is configured to use {replace_queries_executor._max_workers} max workers"
    )

    executors_to_shutdown = [replace_queries_executor]
    Organization.config(redis_client, conf["jwt_secret"])
    User.config(
        redis_client, conf["jwt_secret"], secrets_key=conf["secrets_key"], replace_executor=replace_queries_executor
    )
    UserAccount.config(
        redis_client,
        conf["jwt_secret"],
        conf.get("confirmed_account", True),
        {},
    )
    Limits.config(disable_rate_limits=conf["disable_rate_limits"])
    Users.config(MailgunService(conf))

    VercelIntegrationService.config(conf["vercel_integration"])

    CDKUtils.config(
        conf["cdk_gcs_export_bucket"],
        conf["cdk_gcs_composer_bucket"],
        conf["api_host"],
        conf["cdk_project_id"],
        conf["cdk_webserver_url"],
        conf["cdk_service_account_key_location"],
        conf["cdk_group_email"],
    )
    GCloudScheduler.config(
        conf.get("gcscheduler_project_id", ""),
        conf.get("gcscheduler_region", ""),
        conf.get("gcscheduler_service_account_key_location", ""),
    )
    KafkaServerGroupsConfig.config(conf.get("kafka_server_groups", {}))
    Limit.set_max_datasources(conf.get("max_datasources", None))
    init_services(conf)

    csv_workers = conf.get("csv_workers", CsvChunkQueueRegistry.DEFAULT_WORKERS)
    if is_reader(app_name):
        # If the app is a reader, we don't need any CSV worker
        csv_workers = 0
    statsd_client.init(conf)
    csv_queue = CsvChunkQueueRegistry.get_or_create(csv_workers, app_name, is_debug)

    loop = tornado.ioloop.IOLoop.current()
    loop.asyncio_loop.set_debug(is_debug)

    if dev:
        # When doing local development, create internal tables automatically
        # In production we have external tasks (in tinybird_tool) to do this properly (and only in the proper clusters)

        # tinybird_tool create-internal-user
        loop.asyncio_loop.run_until_complete(
            init_internal_tables(
                DEFAULT_TABLES,
                read_only=False,
                populate_views=False,
                job_executor=None,
                clickhouse_cluster=INTERNAL_CLUSTER,
            )
        )  # Note that we are not populating views, so we don't need a job_executor

        # tinybird_tool init-metrics-cluster-and-internal
        metrics_database_server = conf.get("metrics_database_server", User.default_database_server)
        loop.asyncio_loop.run_until_complete(
            init_metrics_tables(
                host=CH_INTERNAL_ADDRESS,
                metrics_cluster=conf.get("metrics_cluster", None),
                metrics_database_server=metrics_database_server,
                metrics_cluster_tables=DEFAULT_METRICS_CLUSTER_TABLES,
                metrics_cluster_views=DEFAULT_METRICS_CLUSTER_VIEWS,
                metrics_tables=DEFAULT_METRICS_TABLES,
                metrics_views=DEFAULT_METRICS_VIEWS,
                add_datasources=True,
            )
        )

    # set a reference of metrics cluster
    public.set_metrics_cluster(
        conf.get("metrics_cluster", None), conf.get("metrics_database_server", User.default_database_server)
    )

    datasources_ops_log_delay = conf.get("datasources_ops_log_delay", DatasourceOpsTrackerRegistry.DEFAULT_DELAY)
    if is_reader(app_name):
        datasources_ops_log_delay = 0.0
    DatasourceOpsTrackerRegistry.create(
        datasources_ops_log_delay, sleep_time=conf.get("datasources_ops_log_sleep_time", 4.0)
    )

    # Socket timeouts
    set_socket_total_timeout(conf.get("socket_total_timeout", socket_total_timeout()))
    set_socket_connect_timeout(conf.get("socket_connect_timeout", socket_connect_timeout()))
    set_socket_read_timeout(conf.get("socket_read_timeout", socket_read_timeout()))
    logging.info(
        f"Setting socket timeouts: total {socket_total_timeout()}s, connect {socket_connect_timeout()}s, read {socket_read_timeout()}s"
    )

    async_redis.init(redis_config)
    async_redis_limits.init(redis_config)
    _register_authentication_provider(conf.get("billing_provider"), conf)
    set_predefined_replicas_configuration_for_copy(conf.get("predefined_replicas_for_copy"))
    set_yepcode_configuration(conf.get("yepcode_environment"), conf.get("yepcode_token"))

    try:
        # This section is for the new CH BI Connector. Needs a
        # password for a user to have access management in the machine
        logging.info("Setting BI Connector Management Password")
        set_bi_management_password(conf.get("ch_bi_management_password", ""))
    except Exception as e:
        logging.error(f"Cannot set BI Management password: {str(e)}")

    threads_to_terminate = []
    job_executor = None
    if not consumer:
        # We need to have a working version of JobExecutor because it includes the logic to cope with the jobs Redis
        # queue. So, even if we're not setting a server with a working consumer, we still need to be able to put new
        # jobs into queue
        job_executor = JobExecutor(
            redis_client=redis_client,
            redis_config=redis_config,
            consumer=False,
            import_workers=0,
            import_workers_per_database={},
            import_parquet_workers=0,
            import_parquet_workers_per_database={},
            query_workers=0,
            populate_workers=0,
            populate_workers_per_database={},
            copy_workers=0,
            copy_workers_per_database={},
            sink_workers=0,
            sink_workers_per_database={},
            branching_workers=0,
            branching_workers_per_database={},
            dynamodb_sync_workers=0,
            dynamodb_sync_workers_per_database={},
            billing_provider=conf.get("billing_provider"),
            billing_region=conf.get("billing_region"),
        )
    else:
        job_executor = JobExecutor(
            redis_client=redis_client,
            redis_config=redis_config,
            consumer=consumer,
            import_workers=conf.get("import_workers", 1),
            import_workers_per_database=conf.get("import_workers_per_database", {}),
            import_parquet_workers=conf.get("import_parquet_workers", 1),
            import_parquet_workers_per_database=conf.get("import_parquet_workers_per_database", {}),
            query_workers=conf.get("query_workers", 1),
            query_workers_per_database=conf.get("query_workers_per_database", {}),
            populate_workers=conf.get("populate_workers", 1),
            populate_workers_per_database=conf.get("populate_workers_per_database", {}),
            copy_workers=conf.get("copy_workers", 1),
            copy_workers_per_database=conf.get("copy_workers_per_database", {}),
            sink_workers=conf.get("sink_workers", 1),
            sink_workers_per_database=conf.get("sink_workers_per_database", {}),
            branching_workers=conf.get("branching_workers", 1),
            branching_workers_per_database=conf.get("branching_workers_per_database", {}),
            dynamodb_sync_workers=conf.get("dynamodb_sync_workers", 1),
            dynamodb_sync_workers_per_database=conf.get("dynamodb_sync_workers_per_database", {}),
            billing_provider=conf.get("billing_provider"),
            billing_region=conf.get("billing_region"),
        )

        job_processor_thread = job_executor.start_consumer()
        threads_to_terminate.append(job_processor_thread)

        ws_db_usage_tracker = WorkspaceDatabaseUsageTracker()
        ws_db_usage_tracker.start()
        threads_to_terminate.append(ws_db_usage_tracker)

        usage_metrics_tracker = UsageMetricsTracker()
        usage_metrics_tracker.start()
        threads_to_terminate.append(usage_metrics_tracker)

        metrics_cluster = conf.get("metrics_cluster", None)

        if not dev:
            # Don't start the records tracker for local env as we won't be sending anything to stripe and slows things down quite a bit.
            usage_records_tracker = UsageRecordsTracker(api_host=conf["api_host"], metrics_cluster=metrics_cluster)
            usage_records_tracker.start()
            threads_to_terminate.append(usage_records_tracker)

        plan_limits_tracker = PlanLimitsTracker(api_host=conf["api_host"], metrics_cluster=metrics_cluster)
        plan_limits_tracker.start()
        threads_to_terminate.append(plan_limits_tracker)

        # Feeds the ops tracker directly from the query_log
        if conf.get("track_query_log", False):
            global query_log_tracker
            query_log_tracker = QueryLogTracker(
                redis_config=redis_config,
                clusters=conf.get("clickhouse_clusters", {}),
                start_timestamp=datetime.fromtimestamp(0),
                read_batch_limit=conf.get("track_query_log_batch_limit", None),
            )
            # Keep a reference to the task due to https://bugs.python.org/issue21163
            query_log_tracker_task = loop.asyncio_loop.create_task(query_log_tracker.init())  # noqa: F841

    # again, in local dev, api host and hfi host are not the same, so we use the hfi_host, in prod, we use the api_host
    hfi_host = conf.get("hfi_host") if dev or test else conf.get("api_host", "")

    if hfi_settings is not None:
        hfi_settings["allow_json_type"] = str(conf.get("allow_json_type", False)).lower() == "true"

    sinks_tracker.init(tb_api_host=hfi_host, token=get_sinks_append_token())
    # we start the thread if the app is not a reader (job processors and writers)
    if sinks_tracker.is_enabled() and not is_reader(app_name):
        sinks_tracker.start()

    # Raw Events Batcher (Only available in Writer apps and Job Processors)
    raw_events_batcher.init(api_host=hfi_host, send_batched_records=send_batched_records)
    if not is_reader(app_name) and raw_events_batcher.is_enabled():
        raw_events_batcher.start()

    global monitor, monitor_task, lag_monitor
    monitor = Monitor(
        conf=conf, is_executed_inside_job_processor=consumer, is_reader=is_reader(app_name), hfi_host=hfi_host
    )
    lag_monitor = LagMonitor()
    shutdown_tracker = ShutdownStatusTracker(app_name)

    if start_tb_service:
        # Only patch requests for analytics and not for Job Processor for now. The reason is that the Job Processor
        # runs long queries where the HTTP connection is kept open until they finish. e.g. populate, replaces
        global_patch_for_requests_timeout()
        global ingestion_observer
        mailgun_service = None if conf.get("debug", False) or os.environ.get("GITLAB_CI") else MailgunService(conf)
        ingestion_observer = IngestionObserver(mailgun_service)
        loop = tornado.ioloop.IOLoop.current()
        logging.getLogger("asyncio").setLevel(logging.WARNING)
        logging.getLogger("stripe").setLevel(logging.WARNING)
        loop.asyncio_loop.set_debug(is_debug)

        # Keep a reference to the task due to https://bugs.python.org/issue21163
        monitor_task = loop.asyncio_loop.create_task(monitor.init())

        app = make_app(conf)
        app.job_executor = job_executor

        server_ip = "0.0.0.0"
        server_url = f"{server_ip}:{port}"

        http_server = TinybirdHTTPServer(app, xheaders=True, idle_connection_timeout=conf["idle_connection_timeout"])
        safe_tornado_shutdown(
            loop,
            http_server,
            conf["max_seconds_before_timeout_on_application_shutdown"],
            threads_to_terminate,
            executors_to_shutdown,
            conf,
            server_url,
            job_executor,
            shutdown_tracker,
        )
        # Adjust the backlog size with the amount of listening ports
        backlog = max(10, 256 // multi_port)
        logging.info(f"Adjusting backlog to {backlog}")
        for p in range(port, port + multi_port):
            logging.info(f"Listening on {server_ip}:{p}")
            http_server.bind(p, address=server_ip, reuse_port=True, backlog=backlog)
        http_server.start(1)

        queue_pids = [p.pid for p in csv_queue.processes]
        logging.info(f"listening on {server_url} (consumer={consumer}) PID={os.getpid()}, QUEUE_PIDS={queue_pids}")

        threshold = LAG_MONITOR_THRESHOLD_RELEASE_IN_SECS if not is_debug else LAG_MONITOR_THRESHOLD_DEBUG_IN_SECS
        loop.add_callback(lag_monitor.init, threshold=threshold, is_debug=is_debug)

        loop.add_callback(ingestion_observer.run)

        global watchdog
        watchdog = TBWatchdog()
        loop.add_callback(watchdog.run)

        logging.info(f"Startup finished (consumer={consumer}) PID={os.getpid()}, QUEUE_PIDS={queue_pids}")

        # This will start the event loop and keep running until the event loop is marked to be stopped.  https://www.tornadoweb.org/en/branch5.1/ioloop.html#tornado.ioloop.IOLoop.start
        # Once we stop the event loop, we will continue the execution and shutdown internal
        # Keep in mind that even though we run `loop.stop()`, the event loop is still running until
        loop.start()

        # At this point, the server is no longer accepting more requests, the event loop is marked to stop
        # We are going to stop all the remaining processes
        shut_down_internals(threads_to_terminate, executors_to_shutdown, loop, job_executor, shutdown_tracker)
    else:
        asyncio_loop = asyncio.get_event_loop()
        set_safe_shutdown_for_just_internals(
            threads_to_terminate, executors_to_shutdown, asyncio_loop, job_executor, shutdown_tracker
        )
        # Keep a reference to the task due to https://bugs.python.org/issue21163
        monitor_task = asyncio_loop.create_task(monitor.init())
        asyncio_loop.run_forever()


def init_services(conf):
    # Put your service classes setup here (if needed)

    UserAccountsService.init(conf)
    NotificationsService.init(conf)
    CampaignsService.init(conf)
    RegionsService.init(conf)
    OrbService.init(conf)

    # Not a service itself, but it needs some config values too
    AccessToken.init_defaults(conf)


# TODO: Review if someone is actually using the data from this class
class ShutdownStatusTracker:
    def __init__(self, app_name):
        self._start_time = None
        self._app_name = app_name
        self._started = False

    def _main_key(self):
        return f"tinybird.{statsd_client.region_machine}.shutdown_tracker.{self._app_name}"

    def start(self, sig):
        logging.info("Caught signal: %s, shutdown process started", sig)
        self._start_time = time.time()
        self._started = True
        statsd_client.incr(f"{self._main_key()}.started")

    def completed(self):
        if not self._started:
            logging.exception(
                "ShutdownStatusTracker::completed() called without prior call to ShutdownStatusTracker::start()"
            )
            logging.warning("Internal Shutdown completed in unknown time")
        else:
            timing = time.time() - self._start_time
            logging.info("Internal Shutdown completed in %s seconds", timing)
            statsd_client.timing(f"{self._main_key()}.completed", timing)


def safe_tornado_shutdown(
    current_ioloop,
    server: TinybirdHTTPServer,
    max_seconds_before_timeout: int,
    threads_to_terminate,
    executors_to_shutdown,
    conf,
    server_url,
    job_executor,
    shutdown_tracker: ShutdownStatusTracker,
):
    def force_shutdown():
        shut_down_internals(threads_to_terminate, executors_to_shutdown, current_ioloop, job_executor, shutdown_tracker)

    def sig_handler(sig=None, frame=None):
        if current_process().name != "MainProcess":
            logging.error("Child process %s has caught a SIGING/SIGTERM signal.", current_process().name)
            return

        async def shutdown_ioloop_gracefully_finishing_running_requests():
            shutdown_tracker.start(sig)
            logging.warning("Stopping http server")
            server.stop()
            await ingestion_observer.terminate()
            global monitor, lag_monitor, query_log_tracker, watchdog
            monitor.terminate()
            await lag_monitor.stop()
            if query_log_tracker:
                query_log_tracker.terminate()
            if watchdog:
                watchdog.terminate()

            logging.warning("IO Loop will shutdown before %s seconds ...", max_seconds_before_timeout)

            # This is the time when the shutdown will be forced if there are still tasks running
            # At the moment, we are waiting 120 seconds, but `systemctl restart` will wait 20 seconds before
            # forcefully killing the process.
            # Therefore, we are actually waiting 20 seconds
            # TODO: Reduce this timeout to < 20 seconds or increase the timeout in `systemctl restart` to > 120 seconds
            deadline = time.monotonic() + max_seconds_before_timeout

            # Get a reference of the current shared session task
            # to ignore it if is the last running task.
            shared_session_task = get_shared_session_task()

            shutting_down_httpserver_ongoing = True
            while shutting_down_httpserver_ongoing:
                now = time.monotonic()

                tasks = [
                    t
                    for t in asyncio.all_tasks()
                    if t is not asyncio.current_task() and t is not shared_session_task and not t.done()
                ]
                for task in tasks[:1000]:
                    logging.info(f"Waiting for task: {repr(task)}")
                running_tasks = len(tasks)
                pending_connections = len(server._connections)

                if now < deadline and (running_tasks + pending_connections) > 0:
                    logging.warning(
                        "Waiting for %s pending connection/s and %s running task/s or %s seconds " "before shutdown...",
                        pending_connections,
                        running_tasks,
                        round(deadline - now),
                    )
                    await asyncio.sleep(0.5)
                else:
                    if (running_tasks + pending_connections) > 0:
                        logging.error(
                            "Timeout reached, %s task/s and %s connection/s will get interrupted",
                            running_tasks,
                            pending_connections,
                        )
                    shutting_down_httpserver_ongoing = False

            # After waiting for the timeout, we indicate the IO loop to stop.
            # This will not immediately stop the IO loop, but it will indicate the loop that should continue the execution of `loop.start`
            # Once all the callbacks in the event loop are finished.
            # Therefore, even after stopping the event loop. The event loop is still running
            # https://www.tornadoweb.org/en/branch5.1/ioloop.html#tornado.ioloop.IOLoop.stop
            current_ioloop.stop()
            logging.warning("IO Loop shutdown finally")

        # This is only used when running Tinybird locally, you can force a faster shutdown by pressing Ctrl+C twice.
        # In the CI/CD pipeline, the shutdown is done using `systemctl restart` which will wait 20 seconds before
        # forcefully killing the process.
        if ShutdownApplicationStatus.is_application_exiting():
            force_shutdown()
            sys.exit(1)
        else:
            ShutdownApplicationStatus.mark_application_as_exiting()

            # This will create a task to stop gracefully in the background
            # TODO: Why are we not waiting for this task to finished?
            # TODO: Why are we not keeping the reference of the task. https://bugs.python.org/issue21163
            current_ioloop.asyncio_loop.create_task(shutdown_ioloop_gracefully_finishing_running_requests())

            # TODO: Still need to fully understand why we need this
            # I guess we wait 2 seconds as we assume it would only take 2 seconds for the previous task to reach the infinite loop
            # Then, we make the request to unstuck the infinite loop
            # But why do we need to do this?
            def force_a_server_call_to_unstuck_the_shutdown_task_that_stops_the_ioloop():
                time.sleep(2)
                try:
                    requests.get(f"http://{server_url}/v0/health")
                except Exception as e:
                    logging.warning("Internal call to force the shutdown to continue finished with error: %s", str(e))

            threading.Thread(
                target=force_a_server_call_to_unstuck_the_shutdown_task_that_stops_the_ioloop, daemon=True
            ).start()

    if conf.get("debug", False):
        tornado.autoreload.add_reload_hook(force_shutdown)

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)


def set_safe_shutdown_for_just_internals(
    threads_to_terminate, executors_to_shutdown, asyncio_loop, job_executor, shutdown_tracker: ShutdownStatusTracker
):
    def sig_handler(sig, _):
        if current_process().name != "MainProcess":
            logging.error("Child process %s has caught a SIGING/SIGTERM signal.", current_process().name)
            return

        shutdown_tracker.start(sig)
        shut_down_internals(threads_to_terminate, executors_to_shutdown, asyncio_loop, job_executor, shutdown_tracker)

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)


def shut_down_internals(
    threads_to_terminate, executors_to_shutdown, asyncio_loop, job_executor, shutdown_tracker: ShutdownStatusTracker
):
    # For the writers/readers, the event loop is already stopped
    # Please be careful when doing any coroutine call

    global monitor, lag_monitor, query_log_tracker, watchdog
    monitor.terminate()
    if query_log_tracker:
        query_log_tracker.terminate()
    if watchdog:
        watchdog.terminate()
    if isinstance(asyncio_loop, tornado.ioloop.IOLoop):
        loop = asyncio_loop.asyncio_loop
    else:
        loop = asyncio_loop

    # This will try to try to create a task in the event loop
    # In the case of the writers/readers, the event loop is already stopped. So the coroutine will not run
    # Please do try to get the result of the coroutine or it will get stuck
    # TODO: We should validate that the event loop not stop before doing this
    asyncio.run_coroutine_threadsafe(lag_monitor.stop(), loop=loop)

    logging.warning("Terminating asyncio loop")
    asyncio_loop.stop()

    for thread_to_terminate in threads_to_terminate:
        logging.warning(f"Terminating thread {thread_to_terminate}")
        thread_to_terminate.terminate()
        thread_to_terminate.join()
        logging.warning(f"Thread {thread_to_terminate} terminated")

    logging.warning("Terminating jobs queue")
    WipJobsQueueRegistry.stop()

    if job_executor.is_consumer():
        logging.warning("Terminating job executors and waiting for them to finish")
        job_executor.join()
        logging.warning("All jobs finished")

    logging.warning("Terminating Datasources ops log tracker")
    DatasourceOpsTrackerRegistry.stop(20.0)

    logging.warning("Terminating csv processing queue")
    CsvChunkQueueRegistry.stop()

    logging.warning("Stop postgres connection pool")
    PGPool().close_all()

    if sinks_tracker.is_enabled() and sinks_tracker.is_alive():
        try:
            sinks_tracker.shutdown()
        except Exception:
            logging.exception("Sinks tracker shutdown failed")

    if raw_events_batcher.is_enabled() and raw_events_batcher.is_alive():
        try:
            raw_events_batcher.shutdown()
        except Exception:
            logging.exception("raw_events_batcher shutdown failed")

    for executor in executors_to_shutdown:
        logging.warning(f"Shutting down executor {executor}")
        try:
            executor.shutdown(wait=True)
        except Exception as e:
            logging.warning(e)

    logging.warning("Stop sentry")
    shutdown_sentry()

    shutdown_tracker.completed()


def _register_authentication_provider(platform: str, config: dict[str, Any]) -> None:
    provider = _get_auth_provider(platform, config)
    register_auth_provider(provider)
    logging.info("Authentication provider: Initialized for platform '%s'.", platform)


def _get_auth_provider(platform: str, config: dict[str, Any]) -> AuthenticationProvider:
    if platform in ("gcp", "gcs"):
        if (deputy_role_arn := config.get("aws_deputy_role_arn", "UNSET")) == "UNSET":
            msg = "Deputy role ARN not configured. Services depending on federated authentication will malfunction."
            logging.warning(msg)
        service_account_credentials_file = config.get("cdk_service_account_key_location", "not found")
        return GCPAuthenticationProvider(deputy_role_arn, service_account_credentials_file)
    else:  # Default to AWS
        return AWSAuthenticationProvider()


if __name__ == "__main__":
    run()
