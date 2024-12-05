import asyncio
import functools
import json
import logging
import re
import threading
from collections import defaultdict
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import psutil
import tornado.web
from opentracing import Tracer

from tinybird.bi_connector.database import CHBIServer
from tinybird.bi_connector.services import initialize_bi_connector
from tinybird.bi_connector.users import CHBIConnectorUser, PlainTextPassword
from tinybird.campaigns_service import CampaignsService
from tinybird.ch_utils.user_profiles import WORKSPACE_PROFILES_AVAILABLE
from tinybird.connector_settings import DATA_CONNECTOR_SETTINGS, DataConnectorType
from tinybird.constants import BILLING_PLANS, BillingPlans, CHCluster, user_workspace_relationships
from tinybird.data_sinks.job import S3Defaults
from tinybird.data_sinks.limits import SinkLimits
from tinybird.hfi.hfi_defaults import (
    DEFAULT_HFI_MAX_REQUEST_MB,
    DEFAULT_HFI_SEMAPHORE_COUNTER,
    DEFAULT_HFI_SEMAPHORE_TIMEOUT,
    HfiDefaults,
)
from tinybird.ingest.external_datasources.admin import delete_workspace_service_account
from tinybird.integrations.dynamodb.limits import DynamoDBLimit
from tinybird.integrations.vercel import VercelIntegrationService
from tinybird.model import retry_transaction_in_case_of_concurrent_edition_error_async
from tinybird.organization.organization import Organization
from tinybird.plan_limits.cdk import CDKLimits
from tinybird.plan_limits.copy import BranchCopyLimits, CopyLimits
from tinybird.plan_limits.delete import DeleteLimits
from tinybird.tracing import ClickhouseTracer
from tinybird.useraccounts_service import UserAccountsService
from tinybird.views import loginas_config
from tinybird_shared.gatherer_settings import (
    DEFAULT_PUSH_QUERY_SETTINGS,
    OPTIONAL_PUSH_QUERY_SETTINGS,
    PREFIX_FLUSH_INTERVAL_DS,
    GathererDefaults,
)

from ..ch import (
    HTTPClient,
    ch_check_user_profile_exists,
    ch_get_replicas_with_problems_per_cluster_host,
    ch_get_zookeeper_replicas_with_problems,
    ch_server_is_reachable,
    ch_storage_policies,
)
from ..csv_processing_queue import CsvChunkQueueRegistry
from ..data_connector import DataConnector, DataLinker
from ..datasource import Datasource
from ..feature_flags import FeatureFlag, FeatureFlagsService, FeatureFlagsWorkspaceService, FeatureFlagWorkspaces
from ..git_settings import GitHubSettings, GitHubSettingsStatus
from ..iterating.release import ReleaseStatus
from ..job import Job
from ..limits import EndpointLimits, Limit, RateLimitConfig
from ..pg import PGService
from ..pipe import Pipe
from ..plans import DEFAULT_PLAN_CONFIG, PlanConfigConcepts, PlansService
from ..tokens import DecodeError, scopes, token_decode_unverify
from ..user import (
    ReleaseStatusException,
    User,
    UserAccount,
    UserAccountDoesNotExist,
    UserAccounts,
    UserDoesNotExist,
    Users,
    WorkspaceException,
    public,
)
from ..user_workspace import UserWorkspaceRelationships
from ..workspace_service import WorkspaceService
from .base import QUERY_API, QUERY_API_FROM_UI, WebBaseHandler
from .login import UserViewBase, base_login

ITEMS_PER_PAGE = 50


def admin_authenticated(method):
    """
    only allows account with @tinybird.co
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        u = self.current_user
        if u is None or not FeatureFlagsService.feature_for_email(
            FeatureFlag.FULL_ACCESS_ACCOUNT, u.email, u.feature_flags
        ):
            # avoid 403
            raise tornado.web.HTTPError(404)
        return method(self, *args, **kwargs)

    return wrapper


class WebCheriffBaseHandler(WebBaseHandler):
    def write_error(self, status_code, **kwargs):
        self.set_status(status_code)
        error_message = f"{status_code} - {kwargs.get('error', self._reason)}"
        if "exc_info" in kwargs:
            _, value, _ = kwargs["exc_info"]
            error_message = str(value)
        self.render("cheriff_error.html", status_code=status_code, error_message=error_message)


class AdminHandler(WebBaseHandler):
    @tornado.web.authenticated
    @admin_authenticated
    def get(self):
        self.render("admin.html")


class DebugImports(WebBaseHandler):
    @tornado.web.authenticated
    @admin_authenticated
    def get(self):
        ds = Users.get_datasource(public.get_public_user(), "block_log")
        if ds is None:
            raise tornado.web.HTTPError(404, "Data source not found")
        self.render("imports_debug.html", blocks_table=ds.id)


class DebugStatus(WebBaseHandler):
    @tornado.web.authenticated
    @admin_authenticated
    def get(self):
        ds = Users.get_datasource(public.get_public_user(), "spans")
        if ds is None:
            raise tornado.web.HTTPError(404, "Data source not found")
        self.render("status_debug.html", spans_table=ds.id)


class DebugQueues(WebBaseHandler):
    @tornado.web.authenticated
    @admin_authenticated
    def get(self):
        csv_chunk_queue = CsvChunkQueueRegistry.get_or_create()
        processes = [p.pid for p in csv_chunk_queue.processes]
        if processes:
            processes = [psutil.Process(processes[0]).ppid(), *processes]

        pid = self.get_argument("pid", None)
        if pid:
            pid = int(pid)
            if pid in processes:
                p = psutil.Process(int(pid))
                d = p.as_dict()
                if "environ" in d:
                    del d["environ"]
                return self.finish(d)

        queues: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"size": 0, "results": []})
        for block_id, queue in csv_chunk_queue.queues_blocks.items():
            queue_id = hex(id(queue))
            queues[queue_id]["size"] += 1
            queues[queue_id]["results"].append(csv_chunk_queue.blocks_results.get(block_id))

        wip_jobs, queued_jobs = self.application.job_executor.get_wip_and_queued_jobs()
        job_id = self.get_argument("job_id", None)
        job = Job.get_by_id(job_id) if job_id is not None else None

        self.render(
            "queues_debug.html",
            processes=[psutil.Process(pid) for pid in processes],
            threads=threading.enumerate(),
            queues=queues,
            blocks_waiting=csv_chunk_queue.blocks_waiting(),
            wip_jobs=wip_jobs,
            queued_jobs=queued_jobs,
            job=job,
        )

    @admin_authenticated
    async def post(self) -> None:
        job_id = self.get_argument("job_id")

        try:
            if not job_id:
                raise tornado.web.HTTPError(400, "Missing job_id to cancel")

            j = Job.get_by_id(job_id)
            if j is None:
                raise tornado.web.HTTPError(404, f"Job {job_id} not found")

            j.mark_as_error({"error": "Job cancelled by operator"})
            executor = self.application.job_executor.get_job_executor(j)
            executor._redis_queue.task_done(job_id)
            executor._redis_queue.rem_queue(job_id)
            logging.info(f"Job {job_id} marked as error with Cheriff")
        except tornado.web.HTTPError as e:
            logging.warning(e)
            raise e
        except Exception as e:
            logging.exception(f"Can't mark as error {job_id}", e)
            raise tornado.web.HTTPError(500, str(e))

        return self.redirect(self.reverse_url("queues_debug"))


class ReplicasStatus(WebBaseHandler):
    @tornado.web.authenticated
    @admin_authenticated
    async def get(self):
        u = public.get_public_user()
        replicas_problems = await ch_get_replicas_with_problems_per_cluster_host(database_server=u["database_server"])
        zookeeper_replicas_problems = await ch_get_zookeeper_replicas_with_problems(
            database_server=u["database_server"]
        )

        self.render(
            "replicas_status.html",
            replicas_problems=replicas_problems,
            zookeeper_replicas_problems=zookeeper_replicas_problems,
        )


class RegisterUserAdminHandler(UserViewBase):
    @admin_authenticated
    async def post(self) -> None:
        email = self.get_argument("email")
        workspace_name = self.get_argument("workspace_name")
        password = self.get_argument("password")
        password_confirm = self.get_argument("password_confirm")
        database_server = self.get_argument("database_server")
        cluster = self.get_argument("cluster", None)

        if not email:
            raise tornado.web.HTTPError(400, "Missing email field")
        if not workspace_name:
            raise tornado.web.HTTPError(400, "Missing workspace_name field")
        try:
            user_account = UserAccounts.get_by_email(email)

            if user_account:
                raise tornado.web.HTTPError(400, "User account already exists")

        except UserAccountDoesNotExist:
            pass

        if len(password) < 4:
            raise tornado.web.HTTPError(400, "Password too short, min 4 chars")
        if password != password_confirm:
            raise tornado.web.HTTPError(400, "Passwords do not match")

        user_account = await UserAccountsService.register_user(
            email=email, password=password, confirmed_account=True, notify_user=True
        )
        if database_server:
            cluster = CHCluster(name=cluster, server_url=database_server)

        try:
            await WorkspaceService.register_and_initialize_workspace(
                name=workspace_name,
                user_creating_it=user_account,
                cluster=cluster,
                tracer=self.application.settings["opentracing_tracing"].tracer,
            )
        except Exception as e:
            raise tornado.web.HTTPError(400, str(e))

        u = UserAccounts.get_by_email(email)

        return self.redirect(self.reverse_url("user_accounts_admin") + f"#user-{u['id']}")


class RegisterWorkspaceAdminHandler(UserViewBase):
    @admin_authenticated
    async def post(self) -> None:
        email = self.get_argument("email")
        workspace_name = self.get_argument("workspace_name")
        database_server = self.get_argument("database_server")
        cluster = self.get_argument("cluster")

        if not email:
            raise tornado.web.HTTPError(400, "Missing email field")
        if not workspace_name:
            raise tornado.web.HTTPError(400, "Missing workspace_name field")
        if not database_server:
            raise tornado.web.HTTPError(400, "Missing database_server field")
        if not cluster:
            raise tornado.web.HTTPError(400, "Missing cluster field")
        try:
            user_account = UserAccounts.get_by_email(email)

        except UserAccountDoesNotExist:
            raise tornado.web.HTTPError(400, "User account doesn't exist")

        try:
            workspace = await WorkspaceService.register_and_initialize_workspace(
                name=workspace_name,
                user_creating_it=user_account,
                cluster=CHCluster(name=cluster, server_url=database_server),
                tracer=self.application.settings["opentracing_tracing"].tracer,
            )
        except Exception as e:
            raise tornado.web.HTTPError(400, str(e))

        return self.redirect(self.reverse_url("workspace_admin", workspace.id))


class ActivateUserAccountAdminHandler(UserViewBase):
    @admin_authenticated
    async def post(self) -> None:
        id = self.get_argument("id")

        if not id:
            raise tornado.web.HTTPError(400, "Missing id field")

        u = await UserAccounts.confirm_account(id)

        user_account = UserAccount.get_by_id(u.id)
        if not user_account:
            raise tornado.web.HTTPError(404, f"UserAccount {id} not found")
        tracer: ClickhouseTracer = self.application.settings["opentracing_tracing"].tracer
        _trace_user_activation(tracer, user_account, enable=True)

        return self.redirect(self.reverse_url("user_account_admin", user_account.id))


class WorkspacesAdminHandler(WebBaseHandler):
    @tornado.web.authenticated
    @admin_authenticated
    async def get(self, page: Optional[str] = None) -> None:
        page_number: int = max(0, int(page or 0))
        items_per_page: int = int(self.get_argument("items_per_page", ITEMS_PER_PAGE))
        search: str = self.get_argument("q", "").lower()

        workspaces: List[User]

        if search:
            workspaces = list(
                filter(
                    lambda w: (w.database is not None and search in w.database)
                    or (search in w.database_server)
                    or (w.cluster and search in w.cluster)
                    or (search in w.id)
                    or (search in w.name.lower()),
                    await asyncio.to_thread(User.get_all, include_releases=False, include_branches=False),
                )
            )
        else:
            workspaces = await User.get_all_paginated(
                include_releases=False,
                include_branches=False,
                skip_count=items_per_page * page_number,
                page_size=items_per_page,
            )

        active_workspaces = [workspace for workspace in workspaces if not workspace.deleted and not workspace.origin]
        deleted_workspaces = [workspace for workspace in workspaces if workspace.deleted and not workspace.origin]

        sorted_workspaces = {
            workspace.id: workspace
            for workspace in sorted(
                active_workspaces,
                key=lambda workspace: workspace.created_at,
                reverse=True,
            )
        }

        async def query(sql: str, database_server: str):
            client = HTTPClient(database_server, database=None)
            _, body = await client.query(f"{sql} FORMAT JSON", max_execution_time=2)
            return json.loads(body)["data"]

        try:
            results = await query("SELECT cluster FROM system.clusters", User.default_database_server)
            possible_clusters: Set[str] = set([r["cluster"] for r in results])

            internal_server = public.get_public_user().database_server
            response = await query("SELECT cluster FROM system.clusters", internal_server)
            clusters_visible_from_internal: Set[str] = set([r["cluster"] for r in response])
            possible_clusters.update(clusters_visible_from_internal)
            available_clusters: List[str] = list(possible_clusters)

        except Exception as e:
            logging.warning(e)
            available_clusters = ["tinybird", "thn", "vercel", "itxlive"]

        self.render(
            "workspaces_admin.html",
            workspaces=sorted_workspaces,
            deleted_workspaces=deleted_workspaces,
            available_clusters=available_clusters,
            current_page=page_number,
            prev_page=-1 if page_number == 0 or search else (page_number - 1),
            next_page=-1 if len(workspaces) < items_per_page or search else (page_number + 1),
            q=search,
        )


class BranchesAdminHandler(WebBaseHandler):
    @tornado.web.authenticated
    @admin_authenticated
    async def get(self, page: Optional[str] = None) -> None:
        page_number: int = max(0, int(page or 0))
        items_per_page: int = int(self.get_argument("items_per_page", ITEMS_PER_PAGE))
        search: str = self.get_argument("q", "").lower()

        workspaces: List[User]
        all_workspaces = await asyncio.to_thread(User.get_all, include_releases=False, include_branches=True)

        if search:
            workspaces = list(
                filter(
                    lambda w: (search in w.database)
                    or (search in w.database_server)
                    or (w.cluster and search in w.cluster)
                    or (search in w.id)
                    or (search in w.name.lower()),
                    all_workspaces,
                )
            )
        else:
            # Let's just keep branches and releases
            workspaces = [workspace for workspace in all_workspaces if workspace.is_branch and len(workspace.releases)]

            # Let's paginate
            workspaces = workspaces[items_per_page * page_number : items_per_page * (page_number + 1)]

        # add origin deleted
        active_workspaces = [
            workspace
            for workspace in workspaces
            if not workspace.deleted and workspace.is_branch and len(workspace.releases)
        ]
        deleted_workspaces = [
            workspace
            for workspace in workspaces
            if workspace.deleted and workspace.is_branch and len(workspace.releases)
        ]

        orphan_branches_and_releases = [
            workspace
            for workspace in workspaces
            if not workspace.deleted
            and workspace.origin
            and not any(
                ws.id == workspace.origin and not ws.deleted for ws in all_workspaces
            )  # Not active origins found
        ]

        orphan_branches: list[User] = []
        orphan_releases: list[User] = []

        for workspace in orphan_branches_and_releases:
            if len(workspace.releases):
                orphan_branches.append(workspace)
            else:
                orphan_releases.append(workspace)

        sorted_workspaces = {
            workspace.id: workspace
            for workspace in sorted(
                active_workspaces,
                key=lambda workspace: workspace.created_at,
                reverse=True,
            )
        }

        client = HTTPClient(User.default_database_server, database=None)

        async def query(sql):
            _, body = await client.query(f"{sql} FORMAT JSON", max_execution_time=2)
            return json.loads(body)["data"]

        try:
            results = await query("SELECT cluster FROM system.clusters")
            available_clusters = list(set([r["cluster"] for r in results]))
        except Exception as e:
            logging.warning(e)
            available_clusters = ["tinybird", "thn", "vercel", "itxlive"]

        self.render(
            "branches_admin.html",
            workspaces=sorted_workspaces,
            deleted_workspaces=deleted_workspaces,
            available_clusters=available_clusters,
            orphan_branches=orphan_branches,
            orphan_releases=orphan_releases,
            current_page=page_number,
            prev_page=-1 if page_number == 0 or search else (page_number - 1),
            next_page=-1 if len(workspaces) < items_per_page or search else (page_number + 1),
            q=search,
        )


class UserAccountsAdminHandler(WebBaseHandler):
    @tornado.web.authenticated
    @admin_authenticated
    async def get(self, page: Optional[str] = None) -> None:
        page_number: int = max(0, int(page or 0))
        items_per_page: int = int(self.get_argument("items_per_page", ITEMS_PER_PAGE))
        search: str = self.get_argument("q", "").lower()

        user_accounts: List[UserAccount]

        if search:
            all_accounts = await asyncio.to_thread(UserAccount.get_all)
            user_accounts = list(
                filter(
                    lambda u: search in u.id or search in u.email.lower(),
                    all_accounts,
                )
            )
        else:
            user_accounts = await UserAccount.get_all_paginated(
                skip_count=items_per_page * page_number, page_size=items_per_page
            )

        active_user_accounts = [user for user in user_accounts if not user.deleted]
        deleted_user_accounts = [user for user in user_accounts if user.deleted]
        sorted_user_accounts = sorted(active_user_accounts, key=lambda user: user.created_at, reverse=True)
        all_ff = {ff["name"]: ff for ff in FeatureFlagsService.to_json()}

        self.render(
            "user_accounts_admin.html",
            current_user=self.current_user,
            user_accounts=sorted_user_accounts,
            deleted_user_accounts=deleted_user_accounts,
            domain=self.settings["domain"],
            all_feature_flags=all_ff,
            allowed_loginas_users=loginas_config.allowed_users,
            current_page=page_number,
            prev_page=-1 if page_number == 0 or search else (page_number - 1),
            next_page=-1 if len(user_accounts) < items_per_page or search else (page_number + 1),
            q=search,
        )


class UserAccountAdminHandler(WebCheriffBaseHandler):
    @tornado.web.authenticated
    @admin_authenticated
    async def get(self, user_id: str) -> None:
        user_account = UserAccount.get_by_id(user_id)
        if not user_account:
            raise tornado.web.HTTPError(404, f"UserAccount {user_id} not found")
        user_ff = user_account["feature_flags"] or {}
        all_ff = FeatureFlagsService.to_json()

        def flag_is_applied(flag_name: str) -> bool:
            return FeatureFlagsService.feature_for_email(FeatureFlag(flag_name), user_account.email, user_ff)

        # user_feature_flags is a tuple of (flag_details, current_value, is_override)
        user_feature_flags = tuple((ff, flag_is_applied(ff["name"]), ff["name"] in user_ff) for ff in all_ff)

        all_campaigns = CampaignsService.get_names()
        user_campaigns = ((c, c in user_account.viewed_campaigns) for c in all_campaigns)

        organization_name = ""
        if user_account.organization_id:
            org = Organization.get_by_id(user_account.organization_id)
            if org:
                organization_name = org.name

        self.render(
            "user_account_admin.html",
            current_user=self.current_user,
            user_account=user_account,
            admin_token=user_account.get_token_for_scope(scopes.AUTH),
            workspaces=await user_account.get_workspaces(with_token=True),
            user_feature_flags=user_feature_flags,
            user_campaigns=user_campaigns,
            allowed_loginas_users=loginas_config.allowed_users,
            has_uniquely_shared_datasources=await UserAccountsService.has_uniquely_shared_datasources(user_account),
            organization_name=organization_name,
            integrations=user_account.integrations or [],
        )

    @admin_authenticated
    async def post(self, user_account_id: str) -> None:
        operation = self.get_argument("operation")
        region_name = self.get_current_region()

        with UserAccount.transaction(user_account_id) as target_user_account:
            if operation == "enable_sessionrewind":
                enable = self.get_argument("enabling_sessionrewind", "Deactivate") == "Activate"
                target_user_account["enabled_sessionrewind"] = enable
                target_user_account["enabled_fullstory"] = enable

            elif operation == "change_max_owned_workspaces":
                max_owned_workspaces = self.get_argument("max_owned_workspaces")
                target_user_account.set_max_owned_workspaces(max_owned_workspaces)

            elif operation == "login_as":
                if self.current_user.email not in loginas_config.allowed_users:
                    raise tornado.web.HTTPError(403, "Forbidden")

                workspaces = await target_user_account.get_workspaces()
                workspace_id = next(
                    (workspace["id"] for workspace in workspaces if workspace["role"] == "admin"),
                    workspaces[0]["id"],
                )

                user = self.get_user_from_db()
                tracer: Tracer = self.application.settings["opentracing_tracing"].tracer
                _trace_user_impersonation(tracer, user, target_user_account)

                base_login(self, target_user_account, region_name=region_name)
                self.redirect(self.reverse_url("workspace_dashboard", workspace_id))
                return

            elif operation == "activate_feature_flag":
                feature_flag_name = self.get_argument("feature_flag_name")
                target_user_account["feature_flags"][feature_flag_name] = True

            elif operation == "deactivate_feature_flag":
                feature_flag_name = self.get_argument("feature_flag_name")
                target_user_account["feature_flags"][feature_flag_name] = False

            elif operation == "remove_feature_flag":
                feature_flag_name = self.get_argument("feature_flag_name")
                if feature_flag_name in target_user_account["feature_flags"]:
                    del target_user_account["feature_flags"][feature_flag_name]

            elif operation == "unview_campaign":
                campaign = self.get_argument("campaign")
                target_user_account.viewed_campaigns.remove(campaign)

            elif operation == "view_campaign":
                campaign = self.get_argument("campaign")
                target_user_account.viewed_campaigns.add(campaign)

        if operation == "unlink_integration":
            possible_user = UserAccount.get_by_id(user_account_id)
            if not possible_user:
                raise tornado.web.HTTPError(404, f"UserAccount {user_account_id} not found")
            integration_type: str = self.get_argument("integration_type")
            integration_id: str = self.get_argument("integration_id")

            if integration_type == "vercel":
                await VercelIntegrationService.remove_integration(user, integration_id, remove_remote=True)

        elif operation == "disable_account":
            unshare_ds = self.get_argument("unshare_datasources", "false") == "true"
            await UserAccountsService.disable_user(target_user_account, unshare_datasources=unshare_ds)

            tracer = self.application.settings["opentracing_tracing"].tracer
            _trace_user_activation(tracer, target_user_account, enable=False)

        self.redirect(self.reverse_url("user_account_admin", user_account_id))


class WorkspaceAdminHandler(WebCheriffBaseHandler):
    @tornado.web.authenticated
    @admin_authenticated
    async def get(self, workspace_id: str) -> None:
        try:
            workspace = Users.get_by_id(workspace_id)
        except UserDoesNotExist:
            raise tornado.web.HTTPError(404)

        workspace_info = workspace.to_dict()

        client = HTTPClient(workspace.database_server)

        async def query(sql):
            _, body = await client.query(f"{sql} FORMAT JSON", max_execution_time=2)
            return json.loads(body)["data"]

        clusters: Dict[str, Any] = {}
        available_hosts = set()

        if workspace["clusters"]:
            for c in workspace["clusters"]:
                clusters[c] = {"replicas": [], "tables": []}
            clusters_query = f"""
                    SELECT
                        cluster,
                        replica_num as replica,
                        host_name,
                        host_address,
                        port
                    FROM system.clusters
                    WHERE cluster in ({','.join([f"'{c}'" for c in workspace['clusters']])})
                """
        else:
            database_host, database_port = workspace.database_host_ip_port().split(":")
            clusters["none"] = {"replicas": [], "tables": []}
            clusters_query = f"""
                    SELECT
                        'none' as cluster,
                        1 as replica,
                        '{database_host}' as host_name,
                        '{database_host}' as host_address,
                        '{database_port}' as port
                """
        try:
            results = await query(clusters_query)
            for r in results:
                clusters[r["cluster"]]["replicas"].append(r)
                available_hosts.add(r["host_name"])
        except Exception as e:
            logging.warning(e)

        tables: Dict[str, Any] = defaultdict(lambda: {"clusters": set(), "hosts": set()})

        for cluster_name, cluster in clusters.items():
            if not cluster["replicas"]:
                continue
            remote_hosts = [r["host_address"] for r in cluster["replicas"]] * 2
            tables_query = "UNION ALL".join(
                [
                    f"""
                SELECT
                    '{host}' as host,
                    name,
                    engine,
                    any(dependencies_table) as dependencies_table,
                    if(engine like '%MergeTree', formatReadableSize(sum(bytes_on_disk)), 'Unknown') as disk_usage
                FROM remote('{host}', system.tables) t LEFT JOIN remote('{host}', system.parts) p
                    ON (t.name = p.table AND t.database = p.database)
                WHERE database = '{workspace.database}' AND engine <> 'View'
                GROUP BY name, engine
            """
                    for host in remote_hosts
                ]
            )
            try:
                results = await query(tables_query)
                for t in results:
                    name = t["name"]
                    tables[name]["name"] = name
                    if cluster_name != "none":
                        tables[name]["clusters"].add(cluster_name)
                    tables[name]["hosts"].add(t["host"])
                    tables[name]["engine"] = t["engine"]
                    tables[name]["dependencies_table"] = t["dependencies_table"]
                    tables[name]["disk_usage"] = t["disk_usage"]
            except Exception as e:
                logging.warning(e)

        class OrphanTable:
            def __init__(self, name):
                self.id = name
                self.name = name
                self.resource = "OrphanTable"

        class MaterializedNode:
            def __init__(self, node_id: str, node_name: str, pipe_name: str):
                self.id = node_id
                self.name = f"[MV] {node_name} ( Pipe: {pipe_name} )"
                self.resource = "MaterializedNode"

        resources: List[Union[Datasource, OrphanTable, MaterializedNode, Pipe]] = []
        datasources = workspace.get_datasources()
        resources += datasources
        known_resources = set([d.id for d in datasources] + [f"{d.id}_quarantine" for d in datasources])

        edges = []
        for p in workspace.get_pipes():
            include_pipe = False
            for n in p.pipeline.nodes:
                n.ignore_sql_errors = True  # Force ignore SQL errors so we can access in any case
                if n.materialized:
                    known_resources.add(n.id)
                    if n.tags.get("staging", False) is True:
                        known_resources.add(n.materialized)
                    include_pipe = True
                    r = workspace.get_resource(n.materialized)
                    if not r:
                        logging.warning(f"orphan materialized view detected in cheriff {n.materialized}")
                        resources.append(OrphanTable(n.materialized))
                        continue
                    r_id = f".inner.{r.id}" if n == r else r.id
                    known_resources.add(r_id)
                    resources.append(MaterializedNode(n.id, n.name, p.name))
                    edges.append(((p.id, n.id), (r_id, "head"), False))
                    for d in n.dependencies:
                        r = workspace.get_resource(d)
                        if r:
                            is_source = n.id in tables.get(r.id, {}).get("dependencies_table", [])
                            origin = (r.id, "head")
                            if r.resource == "Node":
                                origin_pipe = workspace.get_pipe_by_node(r.id)
                                assert isinstance(origin_pipe, Pipe)
                                origin = (origin_pipe.id, r.id)
                            edges.append((origin, (p.id, n.id), is_source))
                else:
                    # This covers nodes used by other materialized nodes
                    for d in n.dependencies:
                        ds = workspace.get_datasource(d)
                        if ds:
                            for dt in tables.get(ds.id, {}).get("dependencies_table", []):
                                if workspace.get_pipe_by_node(dt) == p:
                                    edges.append(((ds.id, "head"), (p.id, n.id), True))
            if include_pipe:
                resources.append(p)

        for t in tables.keys():
            if t not in known_resources:
                _, datasource = workspace.find_datasource_in_releases_metadata_by_datasource_id(t)
                if not datasource:
                    _, pipe = workspace.find_pipe_in_releases_metadata_by_pipe_node_id(t)
                    if not pipe:
                        resources.append(OrphanTable(t))

        graph = (resources, edges)

        available_rate_limits = {}
        for k, rl_config in Limit.__dict__.items():
            if not isinstance(rl_config, RateLimitConfig) or workspace.has_limit(k):
                continue
            available_rate_limits[k] = rl_config

        query_apis = [QUERY_API, QUERY_API_FROM_UI]
        endpoint_names = [pipe.name for pipe in workspace.get_pipes() if pipe.is_published()]
        current_endpoint_limits = {
            k: {
                "endpoint_name": v[0],
                "limit_setting": v[1],
                "limit_value": v[2],
            }
            for k, v in workspace.limits.items()
            if EndpointLimits.prefix() in k and v[0] not in query_apis
        }

        available_endpoint_limits = {}
        for endpoint_name in endpoint_names:
            for possible_limit in EndpointLimits.get_all_settings():
                limit = EndpointLimits.get_limit_key(endpoint_name, possible_limit)
                if not workspace.has_limit(limit):
                    available_endpoint_limits[limit] = {
                        "endpoint_name": endpoint_name,
                        "limit_setting": possible_limit.name,
                        "limit_value": possible_limit.default_value,
                    }

        current_query_api_limits = {
            k: {
                "endpoint_name": v[0],
                "limit_setting": v[1],
                "limit_value": v[2],
            }
            for k, v in workspace.limits.items()
            if EndpointLimits.prefix() in k and v[0] in query_apis
        }
        available_query_api_limits = {}
        for api in query_apis:
            limit = EndpointLimits.get_limit_key(api, EndpointLimits.max_concurrent_queries)
            if not workspace.has_limit(limit):
                available_query_api_limits[limit] = {
                    "endpoint_name": api,
                    "limit_setting": EndpointLimits.max_concurrent_queries.name,
                    "limit_value": EndpointLimits.max_concurrent_queries.default_value,
                }

        ch_limits = {
            "admin_max_execution_time": (Limit.ch_max_execution_time, "seconds"),
            "max_execution_time": (Limit.ch_max_execution_time, "seconds"),
            "max_estimated_execution_time": (Limit.ch_max_estimated_execution_time, "seconds"),
            "timeout_before_checking_execution_speed": (Limit.ch_timeout_before_checking_execution_speed, "seconds"),
            "max_threads": (Limit.ch_max_threads, "number"),
            "max_result_bytes": (Limit.ch_max_result_bytes, "bytes"),
            "max_memory_usage": (Limit.ch_max_memory_usage, "bytes"),
            "chunk_max_execution_time": (Limit.ch_chunk_max_execution_time, "seconds"),
            "max_insert_threads": (Limit.ch_max_insert_threads, "number"),
            "max_mutations_seconds_to_wait": (
                Limit.ch_max_mutations_seconds_to_wait,
                "seconds",
            ),
            "max_execution_time_replace_partitions": (
                Limit.ch_max_execution_time_replace_partitions,
                "seconds",
            ),
            "max_wait_for_replication_seconds": (
                Limit.ch_max_wait_for_replication_seconds,
                "seconds",
            ),
            # 'max_bytes_before_external_group_by': (6 * (1024 ** 3), 'bytes'),
            "materialize_performance_validation_limit": (
                Limit.materialize_performance_validation_limit,
                "rows",
            ),
            "materialize_performance_validation_seconds": (
                Limit.materialize_performance_validation_seconds,
                "seconds",
            ),
            "materialize_performance_validation_threads": (
                Limit.materialize_performance_validation_threads,
                "threads",
            ),
            "lock_acquire_timeout": (Limit.ch_lock_acquire_timeout, "seconds"),
            "ddl_max_execution_time": (Limit.ch_ddl_max_execution_time, "seconds"),
        }
        current_ch_limits, available_ch_limits = _get_limits_by_prefix(workspace, "ch", ch_limits)

        kafka_limits = {"max_topics": Limit.kafka_max_topics}
        current_kafka_limits, available_kafka_limits = _get_limits_by_prefix(workspace, "kafka", kafka_limits)

        gatherer_ch_limits = {
            item[0]: (item[1], item[2]) for item in DEFAULT_PUSH_QUERY_SETTINGS + OPTIONAL_PUSH_QUERY_SETTINGS
        }

        current_gatherer_ch_limits, available_gatherer_ch_limits = _get_limits_by_prefix(
            workspace, "gatherer_ch", gatherer_ch_limits
        )
        current_gatherer_flush_time_ds, _ = _get_limits_by_prefix(
            workspace, "gatherer_flush_time_ds", gatherer_ch_limits
        )

        gatherer_multiwriter_limits = {
            "multiwriter_enabled": (Limit.gatherer_multiwriter_enabled, "boolean"),
            "multiwriter_type": (Limit.gatherer_multiwriter_type, "type (random, hint)"),
            "multiwriter_tables": ("Comma-Separated String without spaces for tables list", "string"),
            "multiwriter_tables_excluded": ("Comma-Separated String without spaces for excluded tables list", "string"),
            "multiwriter_hint_backend_ws": (
                "The name of the Varnish backend to use for the whole Workspace",
                "string",
            ),
            "multiwriter_hint_backend_tables": (
                "A string 'table1:backend1,table2:backend2' representing the Varnish backends to use for each table",
                "string",
            ),
        }
        current_gatherer_multiwriter_limits, available_gatherer_multiwriter_limits = _get_limits_by_prefix(
            workspace, "gatherer_multiwriter", gatherer_multiwriter_limits
        )

        iterating_limits = {
            "iterating_max_branches": Limit.iterating_max_branches,
            "iterating_attach_max_part_size": Limit.iterating_attach_max_part_size,
            "iterating_attach_parts_batch_number": Limit.iterating_attach_parts_batch_number,
            "iterating_creation_concurrency": Limit.iterating_creation_concurrency,
        }
        current_iterating_limits, available_iterating_limits = _get_limits_by_prefix(
            workspace, "iterating", iterating_limits
        )

        current_rate_limit_config = workspace.get_rate_limit_all_configs().items()

        data_connectors = DataConnector.get_user_data_connectors(workspace.id)
        for data_connector in data_connectors:
            if connector_settings := DATA_CONNECTOR_SETTINGS.get(data_connector["service"]):
                default_settings = {x: "" for x in connector_settings.model_fields.keys()}
                data_connector["settings"] = default_settings | data_connector["settings"]

        available_clusters = []
        available_clusters_error = None
        try:
            results = await query("SELECT cluster FROM system.clusters")
            available_clusters = list(set([r["cluster"] for r in results]))
        except Exception as e:
            available_clusters_error = str(e)
            logging.warning(e)
        metrics_cluster = self.application.settings.get("metrics_cluster", None)
        plan_details = await PlansService.get_workspace_plan_info(workspace=workspace, metrics_cluster=metrics_cluster)
        current_billing_config_overrides = workspace.billing_details["prices_overrides"].items()

        available_billing_config_overrides = {}
        for billing_config_available in PlanConfigConcepts:
            if billing_config_available.value not in workspace.billing_details["prices_overrides"]:
                available_billing_config_overrides[billing_config_available.value] = (
                    DEFAULT_PLAN_CONFIG[billing_config_available],
                    "dollars",
                )

        wksp_ff = workspace["feature_flags"] or {}
        all_ff = FeatureFlagsWorkspaceService.to_json()

        def flag_is_applied(flag_name: str) -> bool:
            return FeatureFlagsWorkspaceService.feature_for_id(FeatureFlagWorkspaces(flag_name), workspace.id, wksp_ff)

        # wksp_feature_flags is a tuple of (flag_details, current_value, is_override)
        wksp_feature_flags = tuple((ff, flag_is_applied(ff["name"]), ff["name"] in wksp_ff) for ff in all_ff)

        if FeatureFlagsWorkspaceService.feature_for_id(
            FeatureFlagWorkspaces.ENABLE_STORAGE_POLICY, "", workspace.feature_flags
        ):
            all_storage_policies = await ch_storage_policies(
                database=workspace.database, database_server=workspace.database_server
            )

            storage_policies = list(
                set(
                    [
                        storage_policy["policy_name"]
                        for storage_policy in all_storage_policies
                        if storage_policy["policy_name"] != "default"
                    ]
                )
            )
        else:
            storage_policies = []

        populate_limits = {
            "populate_max_threads": (Limit.populate_max_threads, "number"),
            "populate_max_insert_threads": (Limit.ch_max_insert_threads, "number"),
            "populate_move_parts_max_execution_time": (Limit.populate_move_parts_max_execution_time, "seconds"),
            "populate_max_insert_block_size": (
                Limit.populate_max_insert_block_size,
                "rows",
            ),
            "populate_min_insert_block_size_rows": (
                Limit.populate_min_insert_block_size_rows,
                "rows",
            ),
            "populate_min_insert_block_size_bytes": (
                Limit.populate_min_insert_block_size_bytes,
                "bytes",
            ),
            "populate_preferred_block_size_bytes": (
                Limit.populate_preferred_block_size_bytes,
                "bytes",
            ),
            "populate_max_memory_usage": (Limit.populate_max_memory_usage, "bytes"),
            "populate_max_memory_usage_percentage": (Limit.populate_max_memory_usage_percentage, "number"),
            "populate_max_concurrent_queries": (
                Limit.populate_max_concurrent_queries,
                "number",
            ),
            "populate_max_job_ttl_in_hours": (
                Limit.populate_max_job_ttl_in_hours,
                "number",
            ),
            "populate_max_estimated_execution_time": (Limit.populate_max_estimated_execution_time, "seconds"),
            "populate_timeout_before_checking_execution_speed": (
                Limit.populate_timeout_before_checking_execution_speed,
                "seconds",
            ),
            "populate_max_memory_threshold": (Limit.populate_max_memory_threshold, "number"),
            "populate_min_memory_threshold": (Limit.populate_min_memory_threshold, "number"),
            "populate_max_cpu_threshold": (Limit.populate_max_cpu_threshold, "number"),
            "populate_min_cpu_threshold": (Limit.populate_min_cpu_threshold, "number"),
            "populate_predefined_replicas": ("Comma-Separated String without spaces for replica list", "string"),
        }

        current_populate_limits, available_populate_limits = _get_limits_by_prefix(
            workspace, "populate", populate_limits
        )

        copy_limits = {
            "copy_join_algorithm": (Limit.copy_join_algorithm, "string"),
            "copy_max_threads": (Limit.ch_max_threads, "number"),
            "copy_max_insert_threads": (Limit.ch_max_insert_threads, "number"),
            "copy_max_execution_time": (
                CopyLimits.max_job_execution_time.get_limit_for(workspace),
                "seconds",
            ),
            "copy_max_jobs": (
                CopyLimits.max_active_copy_jobs.get_limit_for(workspace),
                "number",
            ),
            "copy_max_pipes": (
                CopyLimits.max_copy_pipes.get_limit_for(workspace),
                "number",
            ),
            "copy_max_bytes_before_external_group_by": (
                Limit.copy_max_bytes_before_external_group_by,
                "bytes",
            ),
            "copy_min_period_jobs": (
                CopyLimits.min_period_between_copy_jobs.get_limit_for(workspace),
                "seconds",
            ),
            "copy_max_memory_usage": (Limit.copy_max_memory_usage, "bytes"),
            "copy_max_job_ttl_in_hours": (
                Limit.copy_max_job_ttl_in_hours,
                "number",
            ),
            "copy_predefined_replicas": ("Comma-Separated String without spaces for replica list", "string"),
            "copy_max_threads_query_limit_per_replica": (Limit.copy_max_threads_query_limit_per_replica, "number"),
        }
        current_copy_limits, available_copy_limits = _get_limits_by_prefix(workspace, "copy", copy_limits)

        branchcopy_limits = {
            "branchcopy_max_threads": (Limit.ch_max_threads, "number"),
            "branchcopy_max_insert_threads": (Limit.ch_max_insert_threads, "number"),
            "branchcopy_max_execution_time": (
                BranchCopyLimits.max_job_execution_time.get_limit_for(workspace),
                "seconds",
            ),
            "branchcopy_max_jobs": (
                BranchCopyLimits.max_active_copy_jobs.get_limit_for(workspace),
                "number",
            ),
            "branchcopy_max_pipes": (
                BranchCopyLimits.max_copy_pipes.get_limit_for(workspace),
                "number",
            ),
            "branchcopy_max_bytes_before_external_group_by": (
                Limit.branchcopy_max_bytes_before_external_group_by,
                "bytes",
            ),
            "branchcopy_min_period_jobs": (
                BranchCopyLimits.min_period_between_copy_jobs.get_limit_for(workspace),
                "seconds",
            ),
            "branchcopy_max_memory_usage": (Limit.branchcopy_max_memory_usage, "bytes"),
            "branchcopy_max_job_ttl_in_hours": (
                Limit.branchcopy_max_job_ttl_in_hours,
                "number",
            ),
            "branchcopy_predefined_replicas": ("Comma-Separated String without spaces for replica list", "string"),
            "branchcopy_max_threads_query_limit_per_replica": (
                Limit.branchcopy_max_threads_query_limit_per_replica,
                "number",
            ),
        }
        current_copy_branch_limits, available_copy_branch_limits = _get_limits_by_prefix(
            workspace, "branchcopy", branchcopy_limits
        )

        sinks_limits = {
            "sinks_max_execution_time": (SinkLimits.max_execution_time.get_limit_for(workspace), "seconds"),
            "sinks_s3_max_inflight_parts_for_one_file": (S3Defaults.max_inflight_parts_for_one_file, "number"),
            "sinks_s3_allow_parallel_part_upload": (S3Defaults.allow_parallel_part_upload, "0 or 1"),
            "sinks_max_threads": (Limit.ch_max_threads, "number"),
            "sinks_max_insert_threads": (0, "number"),
            "sinks_max_result_bytes": (Limit.ch_max_result_bytes, "bytes"),
            "sinks_max_memory_usage": (Limit.ch_max_memory_usage, "number"),
            "sinks_max_bytes_before_external_group_by": (
                Limit.sinks_max_bytes_before_external_group_by,
                "number",
            ),
            "sinks_max_insert_delayed_streams_for_parallel_write": (
                Limit.sinks_max_insert_delayed_streams_for_parallel_write,
                "bytes",
            ),
            "sinks_max_bytes_before_external_sort": (
                Limit.sinks_max_bytes_before_external_sort,
                "bytes",
            ),
            "sinks_max_pipes": (SinkLimits.max_sink_pipes.get_limit_for(workspace), "number"),
            "sinks_max_jobs": (SinkLimits.max_active_jobs.get_limit_for(workspace), "number"),
            "sinks_min_period_jobs": (SinkLimits.max_scheduled_job_frequency.get_limit_for(workspace), "number"),
            "sinks_cluster": (workspace.database_server, "string"),
            "sinks_output_format_parallel_formatting": (Limit.sinks_output_format_parallel_fomatting, "0 or 1"),
            "sinks_output_format_parquet_string_as_string": (
                Limit.sinks_output_format_parquet_string_as_string,
                "0 or 1",
            ),
            "sinks_render_internal_compression_in_binary_formats": (
                Limit.sinks_render_internal_compression_in_binary_formats,
                "0 or 1",
            ),
            "sinks_max_job_ttl_in_hours": (
                Limit.sinks_max_job_ttl_in_hours,
                "number",
            ),
        }
        current_sinks_limits, available_sinks_limits = _get_limits_by_prefix(workspace, "sinks", sinks_limits)

        delete_limits = {
            "delete_max_jobs": (
                DeleteLimits.max_active_delete_jobs.get_limit_for(workspace),
                "number",
            ),
        }
        current_delete_limits, available_delete_limits = _get_limits_by_prefix(workspace, "delete", delete_limits)

        limit_url_file_size_plan, limit_url_parquet_file_size_plan = (
            (Limit.import_max_url_file_size_no_dev_gb, Limit.import_max_url_parquet_file_size_no_dev_gb)
            if workspace.plan != "dev"
            else (Limit.import_max_url_file_size_dev_gb, Limit.import_max_url_parquet_file_size_dev_gb)
        )

        import_limits = {
            "import_max_url_file_size_gb": (limit_url_file_size_plan, "number"),
            "import_csv_bytes_to_fetch": (Limit.import_csv_bytes_to_fetch, "number"),
            "import_max_url_parquet_file_size_gb": (limit_url_parquet_file_size_plan, "number"),
            "import_parquet_url_max_threads": (Limit.import_parquet_url_max_threads, "number"),
            "import_parquet_url_max_insert_threads": (Limit.import_parquet_url_max_insert_threads, "number"),
            "import_parquet_url_max_insert_block_size": (Limit.import_parquet_url_max_insert_block_size, "number"),
            "import_parquet_url_min_insert_block_size_rows": (
                Limit.import_parquet_url_min_insert_block_size_rows,
                "number",
            ),
            "import_parquet_url_min_insert_block_size_bytes": (
                Limit.import_parquet_url_min_insert_block_size_bytes,
                "number",
            ),
            "import_parquet_url_max_memory_usage": (Limit.import_parquet_url_max_memory_usage, "number"),
            "import_parquet_url_max_execution_time": (Limit.import_parquet_url_max_execution_time, "number"),
            "import_parquet_url_input_format_parquet_max_block_size": (
                Limit.import_parquet_url_input_format_parquet_max_block_size,
                "number",
            ),
            "import_parquet_url_input_format_parquet_allow_missing_columns": (
                Limit.import_parquet_url_input_format_parquet_allow_missing_columns,
                "0 or 1",
            ),
            "import_parquet_url_input_format_null_as_default": (
                Limit.import_parquet_url_input_format_null_as_default,
                "0 or 1",
            ),
            "import_parquet_url_max_partitions_per_insert_block": (
                Limit.import_parquet_url_max_partitions_per_insert_block,
                "number",
            ),
            "import_parquet_url_date_time_overflow_behavior": (
                Limit.import_parquet_url_date_time_overflow_behavior,
                "string",
            ),
            "import_parquet_url_input_format_parquet_skip_columns_with_unsupported_types_in_schema_inference": (
                Limit.import_parquet_url_input_format_parquet_skip_columns_with_unsupported_types_in_schema_inference,
                "0 or 1",
            ),
            "import_max_job_ttl_in_hours": (
                Limit.import_max_job_ttl_in_hours,
                "number",
            ),
        }
        current_import_limits, available_import_limits = _get_limits_by_prefix(workspace, "import", import_limits)

        cdk_limits = {
            "cdk_max_row_limit": (
                CDKLimits.max_row_limit.get_limit_for(workspace),
                "number",
            ),
            "cdk_version": (
                Limit.cdk_version,
                "string",
            ),
        }
        current_cdk_limits, available_cdk_limits = _get_limits_by_prefix(workspace, "cdk", cdk_limits)

        workspace_limits = {
            "max_datasources": (Limit.max_datasources, "number"),
            "max_tokens": (Limit.max_tokens, "number"),
            "allowed_table_functions": (
                "subset of => postgresql,mysql,mongodb,url,azureBlobStorage,gcs,iceberg,s3",
                "string",
            ),
        }
        current_workspace_limits, available_workspace_limits = _get_limits_by_prefix(
            workspace, "workspace", workspace_limits
        )

        release_limits = {
            "max_number_of_total_releases": (Limit.release_max_number_of_total_releases, "number"),
            "max_number_of_rollback_releases": (Limit.release_max_number_of_rollback_releases, "number"),
            "max_number_of_preview_releases": (Limit.release_max_number_of_preview_releases, "number"),
        }

        current_release_limits, available_release_limits = _get_limits_by_prefix(workspace, "release", release_limits)

        dynamodb_limits = {
            "dynamodb_max_table_size_bytes": (DynamoDBLimit.max_table_size_bytes, "bytes"),
            "dynamodb_max_table_write_capacity_units": (DynamoDBLimit.max_table_write_capacity_units, "number"),
            "dynamodb_max_threads": (DynamoDBLimit.max_threads, "number"),
            "dynamodb_max_insert_threads": (DynamoDBLimit.max_insert_threads, "number"),
            "dynamodb_max_insert_block_size": (DynamoDBLimit.max_insert_block_size, "number"),
            "dynamodb_min_insert_block_size_rows": (DynamoDBLimit.min_insert_block_size_rows, "number"),
            "dynamodb_min_insert_block_size_bytes": (DynamoDBLimit.min_insert_block_size_bytes, "number"),
            "dynamodb_max_memory_usage": (DynamoDBLimit.max_memory_usage, "number"),
            "dynamodb_max_execution_time": (DynamoDBLimit.max_execution_time, "number"),
            "dynamodb_max_partitions_per_insert_block": (
                DynamoDBLimit.max_partitions_per_insert_block,
                "number",
            ),
            "dynamodb_input_format_try_infer_datetimes": (
                DynamoDBLimit.input_format_try_infer_datetimes,
                "1 or 0",
            ),
            "dynamodb_file_processing_workers_in_ddb_sync": (
                DynamoDBLimit.file_processing_workers_in_ddb_sync,
                "number",
            ),
        }
        current_dynamodb_limits, available_dynamodb_limits = _get_limits_by_prefix(
            workspace, "dynamodb", dynamodb_limits
        )

        info = workspace.get_workspace_info()
        owner: Optional["UserAccount"] = UserAccount.get_by_id(info["owner"])
        if owner is not None:
            branches = await owner.get_workspaces(
                with_token=True,
                with_environments=True,
                only_environments=True,
                filter_by_workspace=workspace.id,
                additional_attrs=["database"],
            )
        else:
            branches = []

        releases = [
            {
                "id": r.id,
                "semver": r.semver,
                "commit": r.commit,
                "metadata_id": r.metadata.id if r.metadata else "Unknown",
                "status": r.status.value,
            }
            for r in workspace.get_releases()
        ]

        organization_name = ""
        if workspace.organization_id:
            org: Optional["Organization"] = Organization.get_by_id(workspace.organization_id)
            if org:
                organization_name = org.name

        profiles = workspace.profiles

        tags = []
        tags_error = ""
        try:
            tags = [tag.to_json() for tag in workspace.get_tags()]
        except Exception as e:
            tags_error = f"exception {e}"

        self.render(
            "workspace_admin.html",
            workspace=workspace,
            billing_plans=BILLING_PLANS,
            plan_details=json.dumps(plan_details, indent=4, sort_keys=True, default=str),
            current_billing_config_overrides=current_billing_config_overrides,
            available_billing_config_overrides=available_billing_config_overrides,
            users=workspace_info["members"],
            user_workspace_relationships=user_workspace_relationships,
            domain=self.settings["domain"],
            admin_token=workspace.get_token_for_scope(scopes.ADMIN),
            available_rate_limits=available_rate_limits,
            available_ch_limits=available_ch_limits,
            current_ch_limits=current_ch_limits,
            available_populate_limits=available_populate_limits,
            current_populate_limits=current_populate_limits,
            available_copy_limits=available_copy_limits,
            current_copy_limits=current_copy_limits,
            available_copy_branch_limits=available_copy_branch_limits,
            current_copy_branch_limits=current_copy_branch_limits,
            available_sinks_limits=available_sinks_limits,
            current_sinks_limits=current_sinks_limits,
            available_delete_limits=available_delete_limits,
            current_delete_limits=current_delete_limits,
            available_kafka_limits=available_kafka_limits,
            current_kafka_limits=current_kafka_limits,
            current_rate_limit_config=current_rate_limit_config,
            current_iterating_limits=current_iterating_limits,
            available_iterating_limits=available_iterating_limits,
            current_import_limits=current_import_limits,
            available_cdk_limits=available_cdk_limits,
            current_cdk_limits=current_cdk_limits,
            available_workspace_limits=available_workspace_limits,
            current_workspace_limits=current_workspace_limits,
            available_release_limits=available_release_limits,
            current_release_limits=current_release_limits,
            available_dynamodb_limits=available_dynamodb_limits,
            current_dynamodb_limits=current_dynamodb_limits,
            available_import_limits=available_import_limits,
            available_clusters=available_clusters,
            available_clusters_error=available_clusters_error,
            available_hosts=available_hosts,
            current_endpoint_limits=current_endpoint_limits,
            available_endpoint_limits=available_endpoint_limits,
            current_query_api_limits=current_query_api_limits,
            available_query_api_limits=available_query_api_limits,
            tables=tables,
            data_connectors=data_connectors,
            graph=graph,
            workspace_feature_flags=wksp_feature_flags,
            storage_policies=storage_policies,
            default_hfi_semaphore_counter=DEFAULT_HFI_SEMAPHORE_COUNTER,
            default_hfi_semaphore_timeout=DEFAULT_HFI_SEMAPHORE_TIMEOUT,
            default_hfi_frequency=HfiDefaults.CH_INGESTION_TOKENS_PER_SECOND_DEFAULT,
            default_hfi_frequency_gatherer=HfiDefaults.CH_INGESTION_TOKENS_PER_SECOND_GATHERER_DEFAULT,
            default_hfi_max_request_mb=DEFAULT_HFI_MAX_REQUEST_MB,
            branches=branches,
            releases=releases,
            organization_name=organization_name,
            main=User.get_by_id(workspace.origin) if workspace.origin else "",
            profiles=profiles,
            workspace_profiles_available=WORKSPACE_PROFILES_AVAILABLE,
            default_gatherer_flush_interval=GathererDefaults.FLUSH_INTERVAL,
            default_gatherer_deduplication=GathererDefaults.DEDUPLICATION,
            default_gatherer_wait_false_traffic=HfiDefaults.WAIT_FALSE_TRAFFIC_THROUGH_GATHERER,
            default_gatherer_wait_true_traffic=HfiDefaults.WAIT_TRUE_TRAFFIC_THROUGH_GATHERER,
            available_gatherer_ch_limits=available_gatherer_ch_limits,
            current_gatherer_ch_limits=current_gatherer_ch_limits,
            current_gatherer_flush_time_ds=current_gatherer_flush_time_ds,
            available_gatherer_multiwriter_limits=available_gatherer_multiwriter_limits,
            current_gatherer_multiwriter_limits=current_gatherer_multiwriter_limits,
            remote=workspace.remote or {},
            remote_statuses=[status.value for status in GitHubSettingsStatus],
            is_branch=workspace.is_branch,
            is_release=workspace.is_release,
            tags=tags,
            tags_error=tags_error,
        )

    @admin_authenticated
    async def post(self, workspace_id: str) -> None:
        operation = self.get_argument("operation")
        tracer: ClickhouseTracer = self.application.settings["opentracing_tracing"].tracer
        if operation == "add_user_to_workspace":
            users_emails = [self.get_argument("user_email")]
            admin_name = self.get_argument("admin_name", "Tinybird")
            try:
                await WorkspaceService.invite_users_to_workspace(admin_name, workspace_id, users_emails, True)
            except WorkspaceException as exc:
                raise tornado.web.HTTPError(400, str(exc))

        elif operation == "update_release":
            target_workspace = User.get_by_id(workspace_id)
            status = self.get_argument("status", None)
            semver = self.get_argument("semver")
            release = target_workspace.get_release_by_semver(semver)
            if not release:
                raise tornado.web.HTTPError(404, f"release {semver} not found")

            if status == "delete":
                await target_workspace.delete_release(release, force=True, dry_run=False)
            else:
                try:
                    await Users.update_release(
                        target_workspace,
                        release,
                        commit=release.commit,
                        status=ReleaseStatus(status) if status else None,
                    )
                except ReleaseStatusException as e:
                    raise tornado.web.HTTPError(400, str(e))
                except Exception as e:
                    raise tornado.web.HTTPError(500, str(e))

        else:
            # TODO: Put this transaction where needed and not at this level
            with User.transaction(workspace_id) as target_workspace:
                if operation == "remove_user_from_workspace":
                    user_email = self.get_argument("user_email")
                    try:
                        target_workspace.remove_users_from_workspace([user_email])
                    except WorkspaceException as exc:
                        raise tornado.web.HTTPError(400, str(exc))

                elif operation == "set_max_seats":
                    max_seats = int(self.get_argument("max_seats"))
                    target_workspace.set_max_seats_limit(max_seats)

                elif operation == "change_hfi_frequency":
                    if (
                        self.get_argument("hfi_frequency").lower() == "none"
                        or self.get_argument("hfi_frequency").strip() == ""
                    ):
                        target_workspace.hfi_frequency = None
                    else:
                        target_workspace.hfi_frequency = float(self.get_argument("hfi_frequency"))

                elif operation == "change_hfi_frequency_gatherer":
                    if (
                        self.get_argument("hfi_frequency_gatherer").lower() == "none"
                        or self.get_argument("hfi_frequency_gatherer").strip() == ""
                    ):
                        target_workspace.hfi_frequency_gatherer = None
                    else:
                        target_workspace.hfi_frequency_gatherer = float(self.get_argument("hfi_frequency_gatherer"))

                elif operation == "change_hfi_database_server":
                    target_workspace.hfi_database_server = self.get_argument("hfi_database_server")

                elif operation == "change_hfi_concurrency_limit":
                    if (
                        self.get_argument("hfi_concurrency_limit").lower() == "none"
                        or self.get_argument("hfi_concurrency_limit").strip() == ""
                    ):
                        target_workspace.hfi_concurrency_limit = None
                    else:
                        value = int(self.get_argument("hfi_concurrency_limit"))
                        target_workspace.hfi_concurrency_limit = value if value > 0 else None
                elif operation == "change_hfi_concurrency_timeout":
                    if (
                        self.get_argument("hfi_concurrency_timeout").lower() == "none"
                        or self.get_argument("hfi_concurrency_timeout").strip() == ""
                    ):
                        target_workspace.hfi_concurrency_timeout = None
                    else:
                        value = int(self.get_argument("hfi_concurrency_timeout"))
                        target_workspace.hfi_concurrency_timeout = value if value > 0 else None
                elif operation == "change_hfi_max_request_mb":
                    if (
                        self.get_argument("hfi_max_request_mb").lower() == "none"
                        or self.get_argument("hfi_max_request_mb").strip() == ""
                    ):
                        target_workspace.hfi_max_request_mb = None
                    else:
                        value = int(self.get_argument("hfi_max_request_mb"))
                        target_workspace.hfi_max_request_mb = value if value > 0 else None
                elif operation == "set_storage_policy":
                    change_action = self.get_argument("change_action", "Update").lower()
                    if change_action == "update":
                        target_workspace.storage_policies = {self.get_argument("storage_policy"): 0}
                    elif change_action == "delete":
                        target_workspace.storage_policies = {}

                elif operation == "enable_sessionrewind":
                    enable = self.get_argument("enabling_sessionrewind", "Deactivate") == "Activate"
                    target_workspace["enabled_sessionrewind"] = enable
                    target_workspace["enabled_fullstory"] = enable

                elif operation == "enable_pg":
                    enable = self.get_argument("enabling_pg", "Deactivate") == "Activate"
                    target_workspace["enabled_pg"] = enable

                elif operation == "drop_pg_database":
                    try:
                        PGService(target_workspace).drop_database()
                    except Exception as e:
                        raise tornado.web.HTTPError(500, str(e))

                elif operation == "create_pg_database":
                    try:
                        pg_service = PGService(target_workspace)
                        pg_service.setup_database()
                        await pg_service.sync_foreign_tables_async()
                        for pipe in target_workspace.get_pipes():
                            await pg_service.on_endpoint_changed(pipe)
                    except Exception as e:
                        raise tornado.web.HTTPError(500, str(e))

                elif operation == "sync_pg_database":
                    try:
                        pg_service = PGService(target_workspace)
                        await pg_service.sync_foreign_tables_async()
                        for pipe in target_workspace.get_pipes():
                            await pg_service.on_endpoint_changed(pipe)
                    except Exception as e:
                        raise tornado.web.HTTPError(500, str(e))

                elif operation == "enable_clickhouse_bi_connector":
                    try:
                        source_workspace = Users.get_by_id(workspace_id)
                        user_name = f"user_{source_workspace.name}"
                        bi_user = CHBIConnectorUser(
                            name=user_name,
                            password=PlainTextPassword(password=self.get_argument("ch_bi_user_password")),
                        )
                        bi_server = CHBIServer(
                            address=self.get_argument("ch_bi_server_address"),
                            port=self.get_argument("ch_bi_server_port"),
                        )

                        await initialize_bi_connector(source_workspace, bi_server, bi_user)
                    except Exception as e:
                        raise tornado.web.HTTPError(500, str(e))

                elif operation == "enable_clusters":
                    enabled_clusters = self.get_arguments("enabled_clusters")
                    target_workspace["clusters"] = enabled_clusters
                    await Users.create_database(target_workspace)
                    await Users.sync_resources_cluster(target_workspace)

                elif operation == "change_database_server":
                    new_db_server = self.get_argument("new_database_server")
                    new_db_server_confirm = self.get_argument("new_database_server_confirm")
                    if new_db_server != new_db_server_confirm:
                        raise tornado.web.HTTPError(400, "database servers do not match")
                    is_reachable = await ch_server_is_reachable(new_db_server)
                    if not is_reachable:
                        raise tornado.web.HTTPError(400, "new database server is not reachable")
                    target_workspace["database_server"] = new_db_server
                    # Refresh all connectors so agents are recreated with the correct server
                    for udc in DataConnector.get_user_data_connectors(workspace_id):
                        with DataConnector.transaction(udc["id"]) as data_connector:
                            await DataConnector.publish(data_connector.id, data_connector.service)

                elif operation == "change_pg_server":
                    new_pg_server = self.get_argument("new_pg_database_server")
                    new_pg_foreign_server = self.get_argument("new_pg_foreign_database_server")
                    new_pg_foreign_server_port = self.get_argument("new_pg_foreign_database_server_port")
                    target_workspace["pg_server"] = new_pg_server
                    target_workspace["pg_foreign_server"] = new_pg_foreign_server
                    target_workspace["pg_foreign_server_port"] = new_pg_foreign_server_port

                elif operation == "change_pg_password":
                    new_password = self.get_argument("new_pg_password")
                    new_password_confirm = self.get_argument("new_pg_password_confirm")
                    if len(new_password) < 4:
                        raise tornado.web.HTTPError(400, "password too short, min 4 chars")
                    if new_password != new_password_confirm:
                        raise tornado.web.HTTPError(400, "passwords do not match")
                    Users.change_pg_password(target_workspace, new_password)

                elif operation == "update_profile":
                    change_action = self.get_argument("change_action").lower()
                    profile_name = self.get_argument("profile_name", None)
                    profile_value = self.get_argument("profile_value", None)

                    if change_action in ("update", "create"):
                        try:
                            await ch_check_user_profile_exists(
                                database_server=target_workspace.database_server,
                                user=profile_value,
                            )
                        except Exception as e:
                            raise tornado.web.HTTPError(500, str(e))

                    if change_action == "delete":
                        target_workspace.delete_profile(profile_name)
                    elif change_action == "update":
                        target_workspace.update_profile(profile_name, profile_value)
                    else:
                        target_workspace.add_profile(profile_name, profile_value)

                elif operation == "enable_use_gatherer":
                    enable = self.get_argument("use_gatherer", "Disable") == "Enable"
                    target_workspace.use_gatherer = enable

                elif operation == "enable_allow_gatherer_fallback":
                    enable = self.get_argument("allow_gatherer_fallback", "Disable") == "Enable"
                    target_workspace.allow_gatherer_fallback = enable

                elif operation == "enable_gatherer_allow_s3_backup_on_user_errors":
                    enable = self.get_argument("gatherer_allow_s3_backup_on_user_errors", "Disable") == "Enable"
                    target_workspace.gatherer_allow_s3_backup_on_user_errors = enable

                elif operation == "change_gatherer_flush_interval":
                    if (
                        self.get_argument("gatherer_flush_interval").lower() == "none"
                        or self.get_argument("gatherer_flush_interval").strip() == ""
                    ):
                        target_workspace.gatherer_flush_interval = None
                    else:
                        target_workspace.gatherer_flush_interval = float(self.get_argument("gatherer_flush_interval"))  # type: ignore
                elif operation == "change_gatherer_deduplication":
                    if (
                        self.get_argument("gatherer_deduplication").lower() == "none"
                        or self.get_argument("gatherer_deduplication").strip() == ""
                    ):
                        target_workspace.gatherer_deduplication = None
                    else:
                        target_workspace.gatherer_deduplication = (
                            self.get_argument("gatherer_deduplication", "false").lower() == "true"
                        )
                elif operation == "change_gatherer_wait_false_traffic":
                    if (
                        self.get_argument("gatherer_wait_false_traffic").lower() == "none"
                        or self.get_argument("gatherer_wait_false_traffic").strip() == ""
                    ):
                        target_workspace.gatherer_wait_false_traffic = None
                    else:
                        target_workspace.gatherer_wait_false_traffic = float(
                            self.get_argument("gatherer_wait_false_traffic")
                        )  # type: ignore
                elif operation == "change_gatherer_wait_true_traffic":
                    if (
                        self.get_argument("gatherer_wait_true_traffic").lower() == "none"
                        or self.get_argument("gatherer_wait_true_traffic").strip() == ""
                    ):
                        target_workspace.gatherer_wait_true_traffic = None
                    else:
                        target_workspace.gatherer_wait_true_traffic = float(
                            self.get_argument("gatherer_wait_true_traffic")
                        )  # type: ignore
                elif operation == "change_workspace_remote":
                    remote = GitHubSettings(
                        remote=self.get_argument("remote_remote"),
                        branch=self.get_argument("remote_branch"),
                        project_path=self.get_argument("remote_project_path"),
                        owner=self.get_argument("remote_owner"),
                        owner_type=self.get_argument("remote_owner_type"),
                        status=self.get_argument("remote_status"),
                    )
                    await target_workspace.update_remote(remote)

                elif operation in [
                    "change_ch_limit",
                    "change_kafka_limit",
                    "change_copy_limit",
                    "change_copy_branch_limit",
                    "change_delete_limit",
                    "change_populate_limit",
                    "change_iterating_limit",
                    "change_import_limit",
                    "change_sinks_limit",
                    "change_workspace_limit",
                    "change_gatherer_ch_limit",
                    "change_gatherer_multiwriter_limit",
                    "change_gatherer_flush_time_ds",
                    "change_cdk_limit",
                    "change_release_limit",
                    "change_endpoint_limit",
                    "change_query_api_limit",
                    "change_dynamodb_limit",
                ]:
                    change_action = self.get_argument("change_action", "Update").lower()
                    limit_name = self.get_argument("limit_name", None)
                    if not limit_name:
                        raise tornado.web.HTTPError(400, "Limit name is required")
                    if change_action == "delete":
                        target_workspace.delete_limit_config(limit_name)
                    else:
                        try:
                            is_sinks_cluster_limit = limit_name == "sinks_cluster" and operation == "change_sinks_limit"
                            is_copy_predefined_replicas = (
                                limit_name == "copy_predefined_replicas" and operation == "change_copy_limit"
                            )
                            is_join_algorithm_limit = (
                                limit_name == "copy_join_algorithm" and operation == "change_copy_limit"
                            )
                            is_populate_predefined_replicas = (
                                limit_name == "populate_predefined_replicas" and operation == "change_populate_limit"
                            )
                            is_populate_predefined_clusters = (
                                limit_name == "populate_predefined_clusters" and operation == "change_populate_limit"
                            )
                            is_allow_table_functions = (
                                limit_name == "allowed_table_functions" and operation == "change_workspace_limit"
                            )
                            is_cdk_version_limit = limit_name == "cdk_version"
                            is_gatherer_multiwriter = operation == "change_gatherer_multiwriter_limit"
                            if (
                                is_sinks_cluster_limit
                                or is_join_algorithm_limit
                                or is_copy_predefined_replicas
                                or is_populate_predefined_replicas
                                or is_populate_predefined_clusters
                                or is_cdk_version_limit
                                or is_allow_table_functions
                                or is_gatherer_multiwriter
                            ):
                                v = self.get_argument("limit_value")
                            else:
                                v = float(self.get_argument("limit_value"))
                                if v.is_integer():
                                    v = int(v)
                                if v < 0:
                                    raise tornado.web.HTTPError(400, "value should be greater or equal to 0")

                            if operation == "change_ch_limit":
                                target_workspace.set_user_limit(limit_name, v, "ch")
                            elif operation == "change_populate_limit":
                                target_workspace.set_user_limit(limit_name, v, "populate")
                            elif operation == "change_copy_limit":
                                target_workspace.set_user_limit(limit_name, v, "copy")
                            elif operation == "change_copy_branch_limit":
                                target_workspace.set_user_limit(limit_name, v, "branchcopy")
                            elif operation == "change_sinks_limit":
                                target_workspace.set_user_limit(limit_name, v, "sinks")
                            elif operation == "change_delete_limit":
                                target_workspace.set_user_limit(limit_name, v, "delete")
                            elif operation == "change_iterating_limit":
                                target_workspace.set_user_limit(limit_name, v, "iterating")
                            elif operation == "change_import_limit":
                                target_workspace.set_user_limit(limit_name, v, "import")
                            elif operation == "change_workspace_limit":
                                target_workspace.set_user_limit(limit_name, v, "workspace")
                            elif operation == "change_gatherer_ch_limit":
                                target_workspace.set_user_limit(limit_name, v, "gatherer_ch")
                            elif operation == "change_gatherer_multiwriter_limit":
                                target_workspace.set_user_limit(limit_name, v, "gatherer_multiwriter")
                            elif operation == "change_gatherer_flush_time_ds":
                                if limit_name.startswith(PREFIX_FLUSH_INTERVAL_DS):
                                    ds_id = limit_name[len(PREFIX_FLUSH_INTERVAL_DS) :]
                                else:
                                    ds_id = limit_name
                                target_workspace.set_user_limit(
                                    f"{PREFIX_FLUSH_INTERVAL_DS}{ds_id}", v, "gatherer_flush_time_ds"
                                )
                            elif operation == "change_cdk_limit":
                                target_workspace.set_user_limit(limit_name, v, "cdk")
                            elif operation == "change_release_limit":
                                target_workspace.set_user_limit(limit_name, v, "release")
                            elif operation == "change_dynamodb_limit":
                                target_workspace.set_user_limit(limit_name, v, "dynamodb")
                            elif operation in ["change_endpoint_limit", "change_query_api_limit"]:
                                endpoint_name = self.get_argument("endpoint_name", None)
                                limit_setting = self.get_argument("limit_setting", None)
                                if not endpoint_name:
                                    raise tornado.web.HTTPError(400, "Endpoint name is required")
                                if not limit_setting:
                                    raise tornado.web.HTTPError(400, "Limit Setting is required")
                                target_workspace.set_endpoint_limit(limit_name, v, endpoint_name, limit_setting)
                            else:
                                target_workspace.set_user_limit(limit_name, v, "kafka")
                        except tornado.web.HTTPError as e:
                            raise e
                        except Exception:
                            raise tornado.web.HTTPError(400, "value should be an integer")

                elif operation == "change_rate_limit":
                    change_action = self.get_argument("change_action", "Update").lower()
                    limit_name = self.get_argument("limit_name", None)
                    if not limit_name:
                        raise tornado.web.HTTPError(400, "Limit name is required")
                    if change_action == "delete":
                        target_workspace.delete_limit_config(limit_name)
                    else:
                        limit_config = [limit_name]
                        for x, min_value in (
                            ("limit_count", 1),
                            ("limit_period", 1),
                            ("limit_max_burst", 0),
                        ):
                            try:
                                v = int(self.get_argument(x, None))
                                if v < min_value:
                                    raise tornado.web.HTTPError(
                                        400,
                                        f"Value for {x} should be greater or equal to {min_value}",
                                    )
                                limit_config.append(v)
                            except Exception:
                                raise tornado.web.HTTPError(400, f"Value for {x} should be an integer")
                        limit_config.append(1)  # quantity
                        if change_action == "create" and target_workspace.has_limit(limit_name):
                            raise tornado.web.HTTPError(400, f"Limit for '{limit_name}' already exists")
                        target_workspace.set_rate_limit_config(*limit_config)

                elif operation == "change_user_workspace_relationship":
                    relationship = self.get_argument("relationship")
                    user_id = self.get_argument("user_id")
                    UserWorkspaceRelationships.change_role(user_id, target_workspace, relationship)

                elif operation == "activate_feature_flag":
                    feature_flag_name = self.get_argument("feature_flag_name")
                    target_workspace["feature_flags"][feature_flag_name] = True

                elif operation == "deactivate_feature_flag":
                    feature_flag_name = self.get_argument("feature_flag_name")
                    target_workspace["feature_flags"][feature_flag_name] = False

                elif operation == "remove_feature_flag":
                    feature_flag_name = self.get_argument("feature_flag_name")
                    if feature_flag_name in target_workspace["feature_flags"]:
                        del target_workspace["feature_flags"][feature_flag_name]

        if operation == "delete_workspace":
            workspace_id = self.get_argument("workspace_id")
            workspace = Users.get_by_id(workspace_id)
            if workspace.is_release:
                raise tornado.web.HTTPError(400, "Hard delete forbidden for a release")
            else:
                info = workspace.get_workspace_info()
                owner = UserAccount.get_by_id(info["owner"])
                await UserAccount.delete_workspace(
                    owner, workspace, hard_delete=True, job_executor=self.application.job_executor
                )
                self.redirect(self.reverse_url("workspaces_admin", 0))
                return

        if operation == "change_plan":
            new_plan = self.get_arguments("plan")[0]
            current_plan = target_workspace.plan

            if new_plan == BillingPlans.BRANCH_ENTERPRISE:
                raise tornado.web.HTTPError(400, f"The plan {BillingPlans.BRANCH_ENTERPRISE} is just internal")
            elif current_plan == BillingPlans.DEV and new_plan == BillingPlans.PRO:
                raise tornado.web.HTTPError(400, "Upgrade from DEV to PRO has to be done by the users")

            if (current_plan == BillingPlans.PRO and new_plan == BillingPlans.DEV) or (
                current_plan == BillingPlans.PRO and new_plan in [BillingPlans.CUSTOM, BillingPlans.ENTERPRISE]
            ):
                await PlansService.cancel_subscription(target_workspace)
                await Users.change_workspace_plan(target_workspace, new_plan)
            else:
                await Users.change_workspace_plan(target_workspace, new_plan)

            updated_workspace = User.get_by_id(target_workspace.id)
            WorkspaceService.trace_workspace_operation(tracer, updated_workspace, "PlanChanged", self.current_user)

        if operation == "change_billing_config":
            change_action = self.get_argument("change_action", "Update").lower()
            limit_name = self.get_argument("limit_name")
            billing_config_name = PlanConfigConcepts(limit_name)
            if change_action == "update":
                limit_value = float(self.get_argument("limit_value"))
                await PlansService.override_default_config(target_workspace, billing_config_name, limit_value)
            elif change_action == "delete":
                await PlansService.override_default_config(target_workspace, billing_config_name, None)
            elif change_action == "create":
                limit_value = float(self.get_argument("limit_value"))
                await PlansService.override_default_config(target_workspace, billing_config_name, limit_value)

        if operation == "create_database":
            workspace = User.get_by_id(workspace_id)
            await Users.create_database(workspace)

        if operation == "update_linker_settings":
            linker_id = self.get_argument("linker_id")
            server_group = self.get_argument("server_group", "").strip()
            tb_message_limit_value = self.get_argument("message_size_limit", None)
            tb_message_size_limit = (
                int(tb_message_limit_value) if tb_message_limit_value not in (None, "None", "") else None
            )
            data_linker_to_update = DataLinker.get_by_id(linker_id)
            if data_linker_to_update is None:
                raise tornado.web.HTTPError(404, f"Data linker {linker_id} not found")
            settings = None
            if data_linker_to_update.service == DataConnectorType.KAFKA:
                settings = {
                    "tb_datasource": self.get_argument("datasource", None),
                    "tb_token": self.get_argument("token", None),
                    "tb_clickhouse_table": self.get_argument("clickhouse_table", None),
                    "tb_clickhouse_host": self.get_argument("clickhouse_host", None),
                    "tb_max_wait_seconds": self.get_argument("max_wait_seconds", None),
                    "tb_max_wait_records": self.get_argument("max_wait_records", None),
                    "tb_max_wait_bytes": self.get_argument("max_wait_bytes", None),
                    "tb_max_partition_lag": self.get_argument("max_partition_lag", None),
                    "kafka_topic": self.get_argument("kafka_topic", None),
                    "kafka_group_id": self.get_argument("kafka_group_id", None),
                    "kafka_auto_offset_reset": self.get_argument("kafka_auto_offset_reset", None),
                    "kafka_target_partitions": self.get_argument("kafka_target_partitions", None),
                    "kafka_store_raw_value": self.get_argument("kafka_store_raw_value", "true").lower() != "false",
                    "kafka_store_headers": self.get_argument("kafka_store_headers", "false").lower() != "false",
                    "kafka_store_binary_headers": self.get_argument("kafka_store_binary_headers", "false").lower()
                    != "false",
                    "json_deserialization": json.loads(self.get_argument("json_deserialization", "[]")),
                    "linker_workers": self.get_argument("linker_workers", 24),
                    "data_connector_id": self.get_argument("data_connector_id", ""),
                    "kafka_key_avro_deserialization": self.get_argument("kafka_key_avro_deserialization", ""),
                    "server_group": server_group if server_group != "None" else "",
                    "tb_message_size_limit": tb_message_size_limit,
                }
            elif data_linker_to_update.service == DataConnectorType.AMAZON_DYNAMODB:
                settings = {
                    "tb_clickhouse_table": self.get_argument("tb_clickhouse_table", None),
                    "tb_datasource": self.get_argument("tb_datasource", None),
                    "json_deserialization": json.loads(self.get_argument("json_deserialization", "[]")),
                    "data_connector_id": self.get_argument("data_connector_id", ""),
                    "server_group": server_group if server_group != "None" else "",
                    "tb_message_size_limit": tb_message_size_limit,
                    "linker_workers": self.get_argument("linker_workers", 1),
                    "dynamodb_export_time": self.get_argument("dynamodb_export_time"),
                    "dynamodb_min_time_between_iterations": self.get_argument(
                        "dynamodb_min_time_between_iterations", 1.5
                    ),
                    "dynamodb_sleep_closed_shards": self.get_argument("dynamodb_sleep_closed_shards", 0.1),
                    "dynamodb_sleep_open_shards": self.get_argument("dynamodb_sleep_open_shards", 0.1),
                    "dynamodb_sleep_closed_shard_cursor": self.get_argument("dynamodb_sleep_closed_shard_cursor", 0),
                    "dynamodb_sleep_open_shard_cursor": self.get_argument("dynamodb_sleep_open_shard_cursor", 0),
                    "dynamodb_max_records_read": self.get_argument("dynamodb_max_records_read", 1000),
                    "dynamodb_max_shards_read_from_redis": self.get_argument(
                        "dynamodb_max_shards_read_from_redis", 15000
                    ),
                }
            if settings:
                with DataLinker.transaction(linker_id) as data_linker:
                    data_linker.update_settings(settings)
                await DataLinker.publish(linker_id)

        if operation == "update_all_linkers":
            connector_id: str = self.get_argument("connector_id")

            dc: Optional[Dict[str, Any]] = next(
                (dc for dc in DataConnector.get_user_data_connectors(workspace_id) if dc["id"] == connector_id),
                None,
            )
            if not dc:
                raise tornado.web.HTTPError(404, f"Data connector {connector_id} not found")

            lnk: Dict[str, str]
            for lnk in dc["linkers"]:
                await DataLinker.publish(lnk["id"])

        if operation == "update_connector_settings":
            connector_id = self.get_argument("connector_id")
            connector_to_update = DataConnector.get_by_id(connector_id)
            if connector_to_update is None:
                raise tornado.web.HTTPError(404, f"Data connector {connector_id} not found")
            settings = None
            if connector_to_update.service == DataConnectorType.KAFKA:
                if ssl_ca_pem := self.get_argument("kafka_ssl_ca_pem", None):
                    ssl_ca_pem = re.sub(r"\\n", r"\n", ssl_ca_pem)
                settings = {
                    "tb_endpoint": self.get_argument("endpoint", None),
                    "kafka_bootstrap_servers": self.get_argument("kafka_bootstrap_servers", None),
                    "kafka_sasl_plain_username": self.get_argument("kafka_sasl_plain_username", None),
                    "kafka_sasl_plain_password": self.get_argument("kafka_sasl_plain_password", None),
                    "kafka_security_protocol": self.get_argument("kafka_security_protocol", None),
                    "kafka_sasl_mechanism": self.get_argument("kafka_sasl_mechanism", None),
                    "kafka_schema_registry_url": self.get_argument("kafka_schema_registry_url", None),
                    "kafka_ssl_ca_pem": ssl_ca_pem,
                    "tag": self.get_argument("tag", None),
                    "from": self.get_argument("from", None),
                }
            elif connector_to_update.service == DataConnectorType.AMAZON_DYNAMODB:
                settings = {
                    "dynamodb_iamrole_arn": self.get_argument("dynamodb_iamrole_arn", None),
                    "dynamodb_iamrole_external_id": self.get_argument("dynamodb_iamrole_external_id", None),
                    "dynamodb_iamrole_region": self.get_argument("dynamodb_iamrole_region", None),
                    "tb_endpoint": self.get_argument("tb_endpoint", None),
                }

            if settings:

                @retry_transaction_in_case_of_concurrent_edition_error_async()
                async def update_settings(connector_id: str) -> DataConnector:
                    with DataConnector.transaction(connector_id) as data_connector:
                        data_connector.update_settings(settings)
                        return data_connector

                data_connector = await update_settings(connector_id)
                await DataConnector.publish(data_connector.id, data_connector.service)

        if operation == "restore_token":
            await self.restore_token(workspace_id)

        if operation == "delete_gcp_account":
            workspace = User.get_by_id(workspace_id)
            await delete_workspace_service_account(workspace)

        if operation == "update_kafka_server_group":
            server_group_tmp = self.get_argument("kafka_server_group", None)
            server_group = server_group_tmp if server_group_tmp and server_group_tmp.strip() != "" else None
            workspace = User.get_by_id(workspace_id)
            if workspace.kafka_server_group != server_group:
                Users.alter_kafka_server_group(workspace, server_group)

        self.redirect(self.reverse_url("workspace_admin", workspace_id))

    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def restore_token(self, workspace_id: str) -> None:
        workspace_name = self.get_argument("workspace_name")
        current_token = self.get_argument("current_token")
        restore_token = self.get_argument("old_token")

        try:
            current_info = token_decode_unverify(current_token)
        except (DecodeError, ValueError):
            raise tornado.web.HTTPError(400, f"Invalid token: {current_token}")

        try:
            restore_info = token_decode_unverify(restore_token)
        except (DecodeError, ValueError):
            raise tornado.web.HTTPError(400, f"Invalid token: {restore_token}")

        if current_token == restore_token:
            raise tornado.web.HTTPError(400, "Both tokens are the same")

        # Require that both tokens belong to the current workspace
        if current_info["u"] != workspace_id:
            raise tornado.web.HTTPError(
                400,
                f"Token workspace mismatch with current token's ({current_info['u']} != {workspace_id})",
            )
        if restore_info["u"] != workspace_id:
            raise tornado.web.HTTPError(
                400,
                f"Token workspace mismatch with to be restored token's ({current_info['u']} != {workspace_id})",
            )

        with User.transaction(workspace_id) as target_workspace:
            # Require that the name matches
            # We do this as an additional security measure, to avoid errors from the employee part
            if workspace_name != target_workspace.name:
                raise tornado.web.HTTPError(400, "Workspace name mismatch")

            # Check if the token to restore already exists
            if next((t for t in target_workspace.tokens if t.token == restore_token), None):
                raise tornado.web.HTTPError(400, "Token already exists")

            # Find the token to be replaced
            existing = next((t for t in target_workspace.tokens if t.token == current_token), None)
            if not existing:
                raise tornado.web.HTTPError(400, "Token not found in workspace")

            # Ok, let's do it
            existing.token = restore_token

            user = self.get_user_from_db()
            tracer: ClickhouseTracer = self.application.settings["opentracing_tracing"].tracer
            _trace_token_restoration(tracer, user, target_workspace, current_token, restore_token)


def _get_limits_by_prefix(workspace: User, prefix, limits) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    current_limits = workspace.get_limits(prefix=prefix).items()

    available_limits = {}
    for k, v in limits.items():
        if workspace.has_limit(k):
            continue
        available_limits[k] = v

    return current_limits, available_limits


def _trace_user_impersonation(tracer: ClickhouseTracer, user: UserAccount, target_user: UserAccount) -> None:
    try:
        span = tracer.start_span()
        span.set_operation_name("AccountImpersonated")
        span.set_tag("user_email", user.email)
        span.set_tag("user", user.id)
        span.set_tag("target_user_email", target_user.email)
        span.set_tag("target_user", target_user.id)
        span.set_tag("http.status_code", 200)
        tracer.record(span)
    except Exception as e:
        logging.exception(f"Could not record account impersonation {user.email} -> {target_user.email}, reason: {e}")


def _trace_user_activation(tracer: ClickhouseTracer, user: UserAccount, enable: bool) -> None:
    try:
        span = tracer.start_span()
        op_name = "AccountActivated" if enable else "AccountDeactivated"
        span.set_operation_name(op_name)
        span.set_tag("user_email", user.email)
        span.set_tag("user", user.id)
        span.set_tag("http.status_code", 200)
        tracer.record(span)
    except Exception as e:
        logging.exception(f"Could not record account activation/deactivation for user '{user.email}', reason: {e}")


def _trace_token_restoration(
    tracer: ClickhouseTracer,
    user: UserAccount,
    workspace: User,
    current_token: str,
    restored_token: str,
) -> None:
    try:
        span = tracer.start_span()
        span.set_operation_name("TokenRestored")
        span.set_tag("user", user.id)
        span.set_tag("user_email", user.email)
        span.set_tag("workspace", workspace.id)
        span.set_tag("current_token", current_token)
        span.set_tag("restored_token", restored_token)
        span.set_tag("http.status_code", 200)
        tracer.record(span)
    except Exception as e:
        logging.exception(
            f"Could not record token restoration for user '{user.email}' at workspace '{workspace.id}', reason: {e}"
        )
