import asyncio
import json
import logging
import os
import re
import time
import unittest
import uuid
from dataclasses import dataclass
from datetime import datetime
from io import StringIO
from typing import Any, Callable, Dict, Iterable, List, Optional, ParamSpec, Tuple, Type, TypeVar, Union
from unittest import mock
from unittest.mock import patch
from urllib.parse import quote, urlencode

import requests
from tornado import httpclient
from tornado.simple_httpclient import SimpleAsyncHTTPClient
from tornado.testing import AsyncHTTPTestCase
from tornado.web import RequestHandler

import tinybird.default_secrets
import tinybird.hfi.ch_multiplexer
from tinybird import app
from tinybird.ch import (
    CHReplication,
    HTTPClient,
    ch_flush_logs_on_all_replicas,
    ch_get_cluster_instances,
    ch_get_data_from_all_replicas,
    ch_insert_rows_sync,
)
from tinybird.ch_utils.ddl import DDL_OUTPUT_MODE_NULL_STATUS_ON_TIMEOUT
from tinybird.ch_utils.engine import engine_local_to_replicated
from tinybird.constants import CHCluster, Relationships
from tinybird.csv_processing_queue import CsvChunkQueueRegistry
from tinybird.datasource import Datasource
from tinybird.feature_flags import FeatureFlag, FeatureFlagWorkspaces
from tinybird.job import JobExecutor
from tinybird.model import (
    retry_transaction_in_case_of_concurrent_edition_error_async,
    retry_transaction_in_case_of_concurrent_edition_error_sync,
)
from tinybird.organization.organization import Organization, Organizations
from tinybird.organization.organization_service import OrganizationService
from tinybird.pg import PGPool
from tinybird.plans import BillingPlans
from tinybird.syncasync import sync_to_async
from tinybird.token_scope import scopes
from tinybird.tokens import token_decode
from tinybird.tracker import DatasourceOpsTrackerRegistry
from tinybird.user import User, UserAccount, UserAccounts, Users, public
from tinybird.user_workspace import UserWorkspaceRelationship
from tinybird.views.aiohttp_shared_session import reset_shared_session
from tinybird.views.base import BaseHandler
from tinybird.views.mailgun import MailgunService, NotificationResponse
from tinybird_shared.redis_client.redis_client import TBRedisClientSync
from tinybird_shared.retry.retry import retry_sync

from ..conftest import CH_ADDRESS, DEFAULT_CLUSTER, METRICS_DATABASE_NAME, get_app_settings, get_redis_config
from ..utils import (
    CsvIO,
    exec_sql,
    get_finalised_job_async,
    get_ops_log_records,
    get_releases_log_records,
    poll,
    poll_async,
)

RT = TypeVar("RT")
P = ParamSpec("P")


@dataclass
class DynamoDBConnector:
    name: str
    dynamodb_iamrole_region: str
    dynamodb_iamrole_arn: str
    dynamodb_iamrole_external_id: str

    def params(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "service": "dynamodb",
            "dynamodb_iamrole_region": self.dynamodb_iamrole_region,
            "dynamodb_iamrole_arn": self.dynamodb_iamrole_arn,
            "dynamodb_iamrole_external_id": self.dynamodb_iamrole_external_id,
        }


class UsageMetricsTestMixin:
    def insert_row_storage_metrics_using_usage_metrics_storage__v2(
        self, workspace, date_metric, rows, bytes, rows_quarantine, bytes_quarantine
    ):
        public_workspace = public.get_public_user()
        usage_metrics_storage = public_workspace.get_datasource("usage_metrics_storage__v2")
        usage_metrics_storage_row = [
            str(date_metric),
            workspace.id,
            "ds_id",
            "ds_name",
            rows,
            bytes,
            rows_quarantine,
            bytes_quarantine,
        ]
        ch_insert_rows_sync(
            public_workspace.database_server,
            public_workspace.database,
            usage_metrics_storage.id,
            [usage_metrics_storage_row],
        )

        if not CHReplication.ch_wait_for_replication_sync(
            public_workspace.database_server,
            public_workspace.cluster,
            public_workspace.database,
            usage_metrics_storage.id,
        ):
            raise RuntimeError("Replication of usage_metrics_storage__v2 failed")

    def insert_row_processed_metrics(self, workspace, date_metric, read_bytes, written_bytes):
        if METRICS_DATABASE_NAME is None:
            raise Exception("METRICS_DATABASE_NAME is not defined")

        public_workspace = public.get_public_user()

        usage_metrics_processed_row = [
            str(date_metric),
            workspace.database,
            read_bytes,
            written_bytes,
            "maxState(now64(6))",
        ]
        ch_insert_rows_sync(
            public_workspace.database_server,
            METRICS_DATABASE_NAME,
            "billing_processed_usage_log",
            [usage_metrics_processed_row],
        )

    def insert_row_sinks_billing_intra(self, workspace: User, date_metric: str, bytes: int) -> None:
        if METRICS_DATABASE_NAME is None:
            raise Exception("METRICS_DATABASE_NAME is not defined")

        public_workspace = public.get_public_user()

        sinks_ops_log_row = [
            date_metric,
            workspace.id,
            workspace.name,
            "gcs",
            "pipe_id",
            "pipe_name",
            "ok",
            None,
            1.0,
            "job_id",
            1,
            2,
            3,
            bytes,
            [],
            {},
            {
                "origin_provider": "aws",
                "origin_region": "us-east-1",
                "destination_provider": "s3",
                "destination_region": "us-east-1",
            },
            "token_name",
            23.8,
            ["tag1", "tag2"],
        ]
        ch_insert_rows_sync(
            public_workspace.database_server,
            public_workspace.database,
            public_workspace.get_datasource("sinks_ops_log").id,
            [sinks_ops_log_row],
        )

    def insert_row_sinks_billing_inter(self, workspace, date_metric, bytes):
        if METRICS_DATABASE_NAME is None:
            raise Exception("METRICS_DATABASE_NAME is not defined")

        public_workspace = public.get_public_user()

        sinks_ops_log_row = [
            date_metric,
            workspace.id,
            workspace.name,
            "gcs",
            "pipe_id",
            "pipe_name",
            "ok",
            None,
            1.0,
            "job_id",
            1,
            2,
            3,
            bytes,
            [],
            {},
            {
                "origin_provider": "aws",
                "origin_region": "us-east-1",
                "destination_provider": "s3",
                "destination_region": "distinct-one",
            },
            "token_name",
            23.8,
            ["tag1", "tag2"],
        ]

        ch_insert_rows_sync(
            public_workspace.database_server,
            public_workspace.database,
            public_workspace.get_datasource("sinks_ops_log").id,
            [sinks_ops_log_row],
        )


class matches:
    def __init__(self, pattern, flags=0):
        self._regex = re.compile(pattern, flags=flags)

    def __eq__(self, actual):
        return bool(self._regex.match(actual))

    def __repr__(self):
        return f"r'{self._regex.pattern}'"


class AsyncMock(mock.MagicMock):
    async def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


class StripeSessionMock:
    url = "portal-url"


def create_test_datasource(u, datasource, partition_key=""):
    url = f"http://{CH_ADDRESS}/?database={u['database']}"
    cluster = f"ON CLUSTER {u.cluster}" if u.cluster else ""

    engine = engine_local_to_replicated("MergeTree()", u["database"], datasource.id)
    res = requests.post(
        url,
        data=f"""create table {u['database']}.{datasource.id} {cluster} (a UInt64, b Float32, c String) Engine = {engine} {partition_key} ORDER BY tuple()""",
    )
    assert res.status_code == 200

    res = requests.post(
        url,
        data=f"""INSERT INTO {u['database']}.{datasource.id}
     SELECT * FROM values(
            (1, 1.0, 'one'),
            (2, 2.0, 'two'),
            (3, 3.0, 'three'),
            (4, 4.0, 'four'),
            (0, 123.56, 'test'),
            (100, -20.45, 'test')
        )
    """,
    )
    assert res.status_code == 200

    engine = engine_local_to_replicated("MergeTree()", u["database"], f"{datasource.id}_quarantine")
    res = requests.post(
        url,
        data=f"create table `{datasource.id}_quarantine` {cluster} (a String, b String, c String) Engine = {engine} ORDER BY tuple()",
    )
    assert res.status_code == 200
    if not CHReplication.ch_wait_for_replication_sync(u.database_server, u.cluster, u.database, datasource.id):
        raise RuntimeError(f"Failed to wait for replication sync: {u.database}.{datasource.id}")


def create_test_datasource_dup_data(u, datasource, partition_key=""):
    url = f"http://{CH_ADDRESS}/?database={u['database']}&insert_deduplicate=0"
    cluster = f"ON CLUSTER {u.cluster}" if u.cluster else ""

    engine = "MergeTree()"
    if u.cluster:
        engine = engine_local_to_replicated(engine, u["database"], datasource.id)

    requests.post(
        url,
        data=f"create table `{datasource.id}` {cluster} (a UInt64, b Float32, c String) Engine = {engine} {partition_key} ORDER BY tuple()",
    )
    # add some data
    data = (
        """
        insert into `%s` values
            (1, 1.0, 'one'),
    """
        % datasource.id
    )
    requests.post(url, data=data)

    # dup data
    requests.post(url, data=data)

    engine = "MergeTree()"
    if u.cluster:
        engine = engine_local_to_replicated(engine, u["database"], f"{datasource.id}_quarantine")

    requests.post(
        url,
        data=f"create table `{datasource.id}_quarantine` {cluster} (a String, b String, c String) Engine = {engine} ORDER BY tuple()",
    )

    if not CHReplication.ch_wait_for_replication_sync(u.database_server, u.cluster, u.database, datasource.id):
        raise RuntimeError(f"Failed to wait for replication sync: {u.database}.{datasource.id}")


def create_test_datasource_with_mat_and_codec(u, datasource, partition_key=""):
    url = f"http://{CH_ADDRESS}/?database={u['database']}"
    cluster = f"ON CLUSTER {u.cluster}" if u.cluster else ""

    engine = "MergeTree()"
    if u.cluster:
        engine = engine_local_to_replicated(engine, u["database"], datasource.id)

    requests.post(
        url,
        data=f"create table `{datasource.id}` {cluster} (a UInt64, b Float32, c String CODEC(ZSTD), d DateTime MATERIALIZED now()) Engine = {engine} {partition_key} ORDER BY tuple()",
    )
    # add some data
    requests.post(
        url,
        data="""
        insert into `%s` values
            (1, 1.0, 'one'),
            (2, 2.0, 'two'),
            (3, 3.0, 'three'),
            (4, 4.0, 'four'),
            (0, 123.56, 'test'),
            (100, -20.45, 'test')
    """
        % datasource.id,
    )

    engine = "MergeTree()"
    if u.cluster:
        engine = engine_local_to_replicated(engine, u["database"], f"{datasource.id}_quarantine")

    requests.post(
        url,
        data=f"create table `{datasource.id}_quarantine` {cluster} (a String, b String, c String, d String) Engine = {engine} ORDER BY tuple()",
    )

    if not CHReplication.ch_wait_for_replication_sync(u.database_server, u.cluster, u.database, datasource.id):
        raise RuntimeError(f"Failed to wait for replication sync: {u.database}.{datasource.id}")


async def create_join_datasource(u, datasource):
    replicas = [x[0] for x in await ch_get_cluster_instances(u["database_server"], u["database"], u.cluster)]

    for replica in replicas:
        url = f"{replica}?database={u['database']}"
        requests.post(  # noqa: ASYNC210
            url, data=f"create table `{datasource.id}` (a UInt64, b Float32, c String) Engine = Join(ANY, LEFT, a)"
        )
        # add some data
        requests.post(  # noqa: ASYNC210
            url,
            data=f"""
            insert into `{datasource.id}` values
                (1, 1.0, 'one'),
                (2, 2.0, 'two'),
                (3, 3.0, 'three'),
                (4, 4.0, 'four'),
                (0, 123.56, 'test'),
                (100, -20.45, 'test')
        """,
        )


def drop_test_datasource(u, datasource):
    cluster = f"ON CLUSTER {u.cluster}" if u.cluster else ""
    url = f"http://{CH_ADDRESS}/?database={u['database']}"
    requests.post(url, data=f"DROP TABLE IF EXISTS `{datasource.id}` {cluster}")
    requests.post(url, data=f"DROP TABLE IF EXISTS `{datasource.id}_quarantine` {cluster}")


def create_projection(u, datasource, projection_sql="(SELECT * ORDER BY a)", rand_id=None):
    if rand_id is None:
        rand_id = f"{uuid.uuid4().hex}"

    url = f"http://{CH_ADDRESS}/?database={u['database']}"

    res = requests.post(
        url,
        data=f"""alter table {u['database']}.{datasource.id} add projection {u['database']}_{datasource.id}_normal_{rand_id} {projection_sql}""",
    )
    assert res.text == ""
    assert res.status_code == 200

    res = requests.post(
        url,
        data=f"""alter table {u['database']}.{datasource.id} materialize projection {u['database']}_{datasource.id}_normal_{rand_id}""",
    )
    assert res.text == ""
    assert res.status_code == 200

    def check_mutation():
        res = requests.post(
            url,
            data=f"""select count() from system.mutations where database='{u['database']}' and table='{datasource.id}' and command like '%MATERIALIZE PROJECTION {u['database']}_{datasource.id}_normal_{rand_id}%' and is_done=1""",
        )
        assert res.text == "1\n"

    poll(check_mutation, timeout=20)


def drop_projection(u, datasource, rand_id):
    url = f"http://{CH_ADDRESS}/?database={u['database']}"

    res = requests.post(
        url,
        data=f"""alter table {u['database']}.{datasource.id} drop projection {u['database']}_{datasource.id}_normal_{rand_id}""",
    )
    assert res.text == ""
    assert res.status_code == 200

    def check_mutation():
        res = requests.post(
            url,
            data=f"""select count() from system.mutations where database='{u['database']}' and table='{datasource.id}' and command like '%DROP PROJECTION {u['database']}_{datasource.id}_normal_{rand_id}%' and is_done=1""",
        )
        assert res.text == "1\n"

    poll(check_mutation, timeout=20)


STRIPE_SUBSCRIPTION_MOCK = {
    "id": "sub_1234",
    "created": datetime.timestamp(datetime.utcnow()),
    "current_period_start": datetime.timestamp(datetime.utcnow()),
    "metadata": {"workspace_id": "workspaceid", "plan_type": BillingPlans.PRO},
    "items": {
        "data": [
            {
                "id": "sub_it_1234",
                "price": {"id": "price_1234", "active": True, "metadata": {"billing_type": "processed"}},
            },
            {
                "id": "sub_it_5678",
                "price": {"id": "price_5678", "active": True, "metadata": {"billing_type": "storage"}},
            },
            {
                "id": "sub_it_archived",
                "price": {"id": "price_archived", "active": False, "metadata": {"billing_type": "storage"}},
            },
        ]
    },
}


class BaseTest(AsyncHTTPTestCase, unittest.TestCase):
    def fetch(self, *args, **kwargs) -> httpclient.HTTPResponse:
        # this allows to use pdb while debugging source code from pytest
        timeout = int(os.getenv("ASYNC_TEST_TIMEOUT", 10))
        kwargs["raise_error"] = kwargs.get("raise_error", False)
        kwargs["request_timeout"] = timeout
        kwargs["connect_timeout"] = timeout
        return super().fetch(*args, **kwargs)

    async def fetch_async(
        self, path, move_http_test_parameters_to_body: bool = False, **kwargs
    ) -> httpclient.HTTPResponse:
        # this allows to use pdb while debugging source code from pytest
        timeout = int(os.getenv("ASYNC_TEST_TIMEOUT", 10))
        raise_error = kwargs.get("raise_error", False)
        kwargs["request_timeout"] = kwargs.get("request_timeout", timeout)
        kwargs["connect_timeout"] = kwargs.get("connect_timeout", timeout)

        if path.lower().startswith(("http://", "https://")):
            url = path
        else:
            if move_http_test_parameters_to_body:
                url = super().get_url(path)
                body_content = json.loads(kwargs.get("body", "{}"))
                body_content.update(self.get_test_http_parameters())
                kwargs["body"] = json.dumps(body_content)
            else:
                url = self.get_url(path)

        return await self.http_client.fetch(url, raise_error=raise_error, **kwargs)

    # Force the use of SimpleAsyncHTTPClient so that it doesn't reuse connections
    # It causes issues when the server closes the connection unexpectedly (to cancel an upload for example)
    def get_http_client(self):
        return SimpleAsyncHTTPClient()

    def get_app(self):
        self.app = app.make_app(get_app_settings())
        return self.app

    @staticmethod
    def create_database(database_name):
        cluster_host = User.default_database_server
        client = HTTPClient(cluster_host, database=None)
        client.query_sync(
            f"CREATE DATABASE IF NOT EXISTS `{database_name}` on cluster tinybird",
            read_only=False,
            max_execution_time=30,
            distributed_ddl_task_timeout=28,
            distributed_ddl_output_mode=DDL_OUTPUT_MODE_NULL_STATUS_ON_TIMEOUT,
        )

    @staticmethod
    def drop_database(workspace: User):
        client = HTTPClient(workspace.database_server)
        client.query_sync(
            f"DROP DATABASE IF EXISTS `{workspace.database}` ON CLUSTER {workspace.cluster}",
            read_only=False,
            **workspace.ddl_parameters(skip_replica_down=True),
        )

    def register_workspace(
        self,
        name: str,
        admin: str,
        cluster: Optional[CHCluster] = DEFAULT_CLUSTER,
        normalize_name_and_try_different_on_collision: bool = False,
        origin: Optional[User] = None,
    ) -> User:
        workspace = User.register(name, admin, cluster, normalize_name_and_try_different_on_collision, origin)
        self.workspaces_to_delete.append(workspace)
        return workspace

    def register_user(self, email: str, password: str = "pass") -> UserAccount:
        user_account = UserAccount.register(email, password)
        self.users_to_delete.append(user_account)
        return user_account

    def create_test_datasource(
        self, datasource_name: str = "test_table", pipe_name: str = "test_pipe", partition_key: str = ""
    ):
        if hasattr(self, "datasource"):
            raise Exception("Test datasource has already been created")
        self.datasource_name = datasource_name
        self.partition_key = partition_key
        self.pipe_name = pipe_name

        self.datasource = Users.add_datasource_sync(self.base_workspace, self.datasource_name)
        create_test_datasource(self.base_workspace, self.datasource, self.partition_key)
        Users.add_pipe_sync(self.base_workspace, self.pipe_name, f"select * from {self.datasource_name}")

    async def create_datasource_with_schema(
        self,
        datasource_name: str = "test_table",
        schema: str = "",
        token: Optional[str] = None,
        engine: Optional[str] = None,
        **kwargs,
    ):
        params = {"token": token or self.token, "name": datasource_name, "schema": schema}
        if engine:
            params["engine"] = engine

        if kwargs:
            params = {**params, **kwargs}

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)
        return json.loads(response.body)

    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def set_feature_flag(
        self, feature_flag, value: bool = True, workspace: Optional[User] = None, workspace_id: Optional[str] = None
    ) -> None:
        if workspace and workspace_id:
            raise ValueError("Cannot specify both workspace and workspace_id")

        workspace_to_use = workspace if workspace else self.base_workspace
        workspace_id_to_use = workspace_id if workspace_id else workspace_to_use.id

        with User.transaction(workspace_id_to_use) as w:
            w.feature_flags.update({feature_flag.value: value})

    def setUp(self):
        rand_id = f"{uuid.uuid4().hex}"
        self.WORKSPACE = f"tes_33t_{rand_id}"
        self.USER_DOMAIN = f"{uuid.uuid4().hex}example.com"
        self.USER = f"{self.WORKSPACE}@{self.USER_DOMAIN}"
        self.database_name = f"d_test_{rand_id}"

        logging.warning(f"Database {self.database_name} was created in {self._testMethodName}")

        super().setUp()

        logging.getLogger("tornado.curl_httpclient").setLevel(logging.WARNING)

        redis_config = get_redis_config()
        self.job_executor = JobExecutor(
            redis_client=TBRedisClientSync(redis_config),
            redis_config=redis_config,
            consumer=True,
            import_workers=1,
            import_parquet_workers=1,
            query_workers=1,
            populate_workers=1,
            copy_workers=1,
            sink_workers=1,
            branching_workers=1,
            dynamodb_sync_workers=1,
            billing_provider="aws",
            billing_region="us-east-1",
        )
        self.app.job_executor = self.job_executor
        self.job_consumer = self.job_executor.start_consumer()

        self.users_to_delete = []
        self.user_account = self.register_user(self.USER)
        self.USER_ID = self.user_account.id

        self.workspaces_to_delete = []
        self.base_workspace = self.register_workspace(self.WORKSPACE, self.USER_ID)
        self.WORKSPACE_ID = self.base_workspace.id
        self.user_token = self.user_account.get_token_for_scope(scopes.AUTH)
        self.admin_token = Users.get_token_for_scope(self.base_workspace, scopes.ADMIN_USER)
        self.ops_log_expectations = {}

        self.organizations_to_delete: List[str] = []

        self.base_workspace.confirmed_account = True

        # FIXME https://gitlab.com/tinybird/analytics/-/issues/7772
        # if random() < 0.5:
        #     # We enable a different storage policy randomly across the tests
        #     self.base_workspace.storage_policies = {
        #         OTHER_STORAGE_POLICY: 0
        #     }
        #     self.base_workspace.feature_flags[FeatureFlagWorkspaces.ENABLE_STORAGE_POLICY.value] = True
        #     logging.warning(f'The workspace for this test is using storage_policy: {OTHER_STORAGE_POLICY}')

        self.create_database(self.database_name)
        self.base_workspace["database"] = self.database_name
        self.base_workspace.save()

        self.reset_user_rate_limit()
        self.sample_tasks = []

        # We collect all the coroutines created by the sampler so we can wait for them before dropping the databases
        def send_sample_save_tasks(sampler):
            if not sampler._guess_list:
                return
            # we store the event loop after move parquet to job and create task in a different one.
            self.sample_tasks.append((asyncio.get_event_loop(), asyncio.create_task(sampler._send_sample_coro())))

        self.sample_patch = patch(
            target="tinybird.views.ndjson_importer.AsyncSampler.send_sample", new=send_sample_save_tasks
        )
        self.sample_patch.start()

    def reset_user_rate_limit(self):
        Users.set_rate_limit_config(self.WORKSPACE_ID, "api_datasources_create_append_replace", 20, 1, 20)
        Users.set_rate_limit_config(self.WORKSPACE_ID, "api_datasources_create_schema", 20, 1, 20)

    def tearDown(self):
        current_test = os.environ.get("PYTEST_CURRENT_TEST").split(":")[-1].split(" ")[0]
        logging.warning(f"teardown start {current_test}")
        self.sample_patch.stop()
        PGPool().close_all()
        self.job_consumer.terminate()
        self.job_consumer.join()
        self.job_executor.join()
        self.job_executor._clean()

        # Let's remove all the pending spans to be flushed
        # If a tests needs it, it will use self.force_flush_of_span_records()
        # Otherwise there will be attempts to write to it later
        if self.app and self.app.tracer and self.app.tracer.recorder:
            self.app.tracer.recorder.clear()

        # Wait for datasource ops logs pending
        DatasourceOpsTrackerRegistry.flush(timeout=10)

        # Same for the CSV queue
        # TODO: Ideally we should only wait for blocks generated in this test
        CsvChunkQueueRegistry.get_or_create().wait_for_queue()

        # And finally wait for all data_guess coroutines to be done
        for event_loop, task in self.sample_tasks:
            if not task.done() and not event_loop.is_closed():
                event_loop.run_until_complete(task)

        self.io_loop.asyncio_loop.run_until_complete(tinybird.hfi.ch_multiplexer.force_flush_ch_multiplexer())

        # Tornado doesn't close the ioloop properly
        # This is a workaround to avoid asyncio warnings
        reset_shared_session()

        for org_id in self.organizations_to_delete:
            org = Organization.get_by_id(org_id)
            if org:
                Organizations.remove_organization(org)

        for workspace in reversed(self.workspaces_to_delete):
            workspace = User.get_by_id(workspace.id)
            if workspace is None:
                continue
            user_workspaces = UserWorkspaceRelationship.get_by_workspace(workspace.id, workspace.max_seats_limit)

            for uw in user_workspaces:
                if uw.relationship == Relationships.ADMIN:
                    if uw.user_id not in self.users_to_delete:
                        self.users_to_delete.append(uw)
                    UserWorkspaceRelationship._delete(uw.id)
            for release in workspace.get_releases():
                if release.id != workspace.id:
                    try:
                        User._delete(release.id)
                    except Exception:
                        pass
            User._delete(workspace.id)
            self.drop_database(workspace)

        try:
            User._delete(self.WORKSPACE_ID)
        except Exception:
            pass

        for user in self.users_to_delete:
            try:
                UserAccount._delete(user.id)
            except Exception:
                pass

        def check_datasource_ops_log():
            if not hasattr(self, "ops_log_expectations") or not self.ops_log_expectations:
                return

            for workspace_id in self.ops_log_expectations:
                if self.ops_log_expectations.get(workspace_id):
                    workspace_ops_log_records = get_ops_log_records(workspace_id)
                    workspace_ops_log_expectations = self.ops_log_expectations[workspace_id]
                    self.assertEqual(
                        len(workspace_ops_log_records),
                        len(workspace_ops_log_expectations),
                        f"Unexpected amount of records. Expected {len(workspace_ops_log_expectations)}. "
                        f"Got {len(workspace_ops_log_records)}\n"
                        f"Expected: \n{workspace_ops_log_expectations}\nGot:\n{workspace_ops_log_records}",
                    )

                    remaining_records = []
                    found_ops_log = []
                    for record in workspace_ops_log_records:
                        found = False
                        for ops_log_expectation in workspace_ops_log_expectations:
                            if (
                                record["event_type"] == ops_log_expectation.get("event_type", None)
                                and record["datasource_name"] == ops_log_expectation.get("datasource_name", None)
                                and record["result"] == ops_log_expectation.get("result", "ok")
                            ):
                                found = True
                                # use options as key to check existance
                                if "options" in ops_log_expectation:
                                    for n, _v in ops_log_expectation["options"].items():
                                        if isinstance(ops_log_expectation["options"][n], re.Pattern):
                                            if not ops_log_expectation["options"][n].search(record["options"][n]):
                                                found = False
                                                break
                                        else:
                                            if record["options"][n] != str(ops_log_expectation["options"][n]):
                                                found = False
                                                break
                                if found:
                                    for k in ops_log_expectation.keys():
                                        if isinstance(ops_log_expectation[k], dict):
                                            for n, _v in ops_log_expectation[k].items():
                                                if isinstance(ops_log_expectation[k][n], re.Pattern):
                                                    self.assertRegex(record[k][n], ops_log_expectation[k][n])
                                                else:
                                                    self.assertEqual(record[k][n], str(ops_log_expectation[k][n]))
                                        else:
                                            if isinstance(ops_log_expectation[k], re.Pattern):
                                                self.assertRegex(record[k], ops_log_expectation[k])
                                            else:
                                                self.assertEqual(
                                                    record[k],
                                                    ops_log_expectation[k],
                                                    f"{k}: from {ops_log_expectation}",
                                                )
                                    if not ops_log_expectation.get("result", None):
                                        self.assertEqual(record["result"], "ok")
                            if found:
                                found_ops_log.append(ops_log_expectation)
                                break
                        if not found:
                            remaining_records.append(record)

                    if remaining_records:
                        raise ValueError(f"Leftover Ops Log entries: {remaining_records}")

                    not_found = []
                    for x in workspace_ops_log_expectations:
                        if x not in found_ops_log:
                            not_found.append(x)
                    if len(not_found):
                        raise ValueError(f"Expected ops log not found: {not_found}")

        poll(check_datasource_ops_log, timeout=20)
        super().tearDown()
        logging.warning(f"teardown end {current_test}")

    def expect_ops_log(self, ops_log_expectations, workspace=None):
        workspace_id = workspace.id if workspace else self.WORKSPACE_ID
        ops_log_expectations = (
            [ops_log_expectations] if isinstance(ops_log_expectations, dict) else ops_log_expectations
        )
        if self.ops_log_expectations.get(workspace_id):
            self.ops_log_expectations[workspace_id].extend(ops_log_expectations)
        else:
            self.ops_log_expectations[workspace_id] = ops_log_expectations

    def gen_random_id(self, prefix: str = "", suffix: str = "") -> str:
        """Generates a new randomized identifier"""
        return f"{prefix}{uuid.uuid4().hex}{suffix}"

    def gen_random_email(self, prefix: str = "", domain: Optional[str] = None) -> str:
        """Generates a new randomized email address"""
        if domain is None:
            domain = f"{uuid.uuid4().hex}example.com"
        return self.gen_random_id(prefix=prefix, suffix=f"@{domain}")

    def get_url_for_sql(self, sql):
        u = Users.get_by_id(self.WORKSPACE_ID)
        return f"http://{CH_ADDRESS}/?database={u['database']}&query={quote(sql,safe='')}&wait_end_of_query=1"

    async def fetch_stream_upload_async(self, url, fd, _headers=None, name="csv"):
        boundary = uuid.uuid4().hex
        headers = {"content-type": f"multipart/form-data; boundary={boundary}"}
        if _headers:
            headers.update(_headers)

        async def producer(write):
            write(b"--%s\r\n" % boundary.encode())
            write(
                b'Content-Disposition: form-data; name="%s"; filename="%s"\r\n'
                % (name.encode("ascii"), fd.name.encode())
            )
            write(b"Content-Type: %s\r\n" % "text/csv".encode())
            write(b"\r\n")
            while True:
                chunk = fd.read(32 * 1024)
                if not chunk:
                    break
                write(chunk)
            write(b"\r\n")
            write(b"--%s--\r\n" % boundary.encode())

        return await self.fetch_async(url, method="POST", headers=headers, body_producer=producer)

    def fetch_full_body_upload(self, url, fd, _headers=None):
        headers = {"content-type": "text/csv"}
        if _headers:
            headers.update(_headers)
        return self.fetch(url, method="POST", headers=headers, body=fd.read())

    async def fetch_full_body_upload_async(self, url, fd, _headers=None):
        headers = {"content-type": "text/csv"}
        if _headers:
            headers.update(_headers)
        return await self.fetch_async(url, method="POST", headers=headers, body=fd.read())

    def check_non_auth_responses(self, urls):
        for x in urls:
            for method in ["GET", "POST", "PUT", "DELETE"]:
                try:
                    response = self.fetch(
                        x, method=method, body=None if method in ("GET", "DELETE") else "", raise_error=True
                    )
                except httpclient.HTTPClientError as e:
                    if e.response.code != 405:
                        self.assertEqual(e.response.code, 403)
                else:
                    self.assertEqual(response.code, 403)

    async def get_finalised_job_async(self, job_id, max_retries=600, elapsed_time_interval=0.2, debug=None, token=None):
        job_internal = await get_finalised_job_async(job_id, max_retries, elapsed_time_interval)
        u = Users.get_by_id(self.WORKSPACE_ID)
        if not token:
            token = Users.get_token_for_scope(u, scopes.ADMIN)

        params = {
            "token": token,
        }
        if debug:
            params["debug"] = debug
        response = await self.fetch_async(f"/v0/jobs/{job_id}?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)
        job_response = json.loads(response.body)

        class JobHolder:
            def __getattr__(self, attr):
                if attr == "get":
                    return job_response.get
                try:
                    return job_response[attr]
                except Exception:
                    attr_in_internal_object = False
                    try:
                        getattr(job_internal, attr)
                        attr_in_internal_object = True
                    finally:
                        if attr_in_internal_object:
                            raise AttributeError(
                                f"Job has no attribute '{attr}', but the internal Job object contains it. You need to fix the problem"
                            )
                        raise AttributeError(f"Job response has no key '{attr}', neither the internal Job object does")

            def __getitem__(self, item):
                return job_response[item]

            def __contains__(self, item):
                return item in job_response

            def __str__(self):
                return json.dumps(job_response)

        return JobHolder()

    def get_host(self):
        return super().get_url("")

    def get_test_http_parameters(self):
        return {"test": self._testMethodName, "time": int(time.time())}

    def get_url(self, url: str, clean_params: bool = False) -> str:
        return f"{super().get_url(url)}{'&' if '?' in url else '?'}{urlencode(self.get_test_http_parameters() if not clean_params else {})}"

    def force_flush_of_span_records(self):
        buffer = self.app.tracer.recorder.buffer
        self.app.tracer.recorder.flush()
        if not CHReplication.ch_wait_for_replication_sync(
            buffer.host, "tinybird", buffer.database, buffer.table, wait=20
        ):
            logging.warning(
                "Waiting for spans replication took more that 20 seconds. We assume flushed data is already replicated"
            )

    def wait_for_public_table_replication(self, table):
        public_user = public.get_public_user()
        ds = Users.get_datasource(public_user, table)

        if ds:
            tableid = ds.id
        else:
            pipe = Users.get_pipe(public_user, table)
            if not pipe:
                raise Exception(f"Could not find public table {table} in the public user")
            else:
                node = pipe.pipeline.last()
                if not node or not node.id:
                    raise Exception(f"Could not find node from pipe {table} in the public user")
                tableid = node.id

        if not CHReplication.ch_wait_for_replication_sync(
            public_user.database_server, public_user.cluster, public_user.database, tableid
        ):
            raise Exception(f"Could not wait for replication of table {table} in the public user")

    def _get_datasource_id(self, workspace: User, datasource: Union[str, Dict[str, Any]], quarantine: bool = False):
        id = None
        if isinstance(datasource, str):
            ds = Users.get_datasource(workspace, datasource)
            id = ds.id

        if isinstance(datasource, dict):
            id = datasource.get("id")

        if not id:
            id = datasource.id
        if quarantine:
            return f"{id}_quarantine"
        return id

    def wait_for_datasource_replication(
        self, workspace: User, datasource: Union[str, Dict[str, Any]], quarantine: bool = False
    ):
        ds_id = self._get_datasource_id(workspace, datasource, quarantine)

        if not CHReplication.ch_wait_for_replication_sync(
            workspace.database_server, workspace.cluster, workspace.database, ds_id
        ):
            raise Exception(f"Could not wait for replication of datasource {datasource.name} quarantine: {quarantine}")

    async def get_data_from_all_replicas(
        self, workspace, datasource, before_from: Optional[str] = None, after_from: Optional[str] = None
    ):
        ds_id = self._get_datasource_id(workspace, datasource)
        return await ch_get_data_from_all_replicas(
            workspace.database_server, workspace.cluster, workspace.database, ds_id, before_from, after_from
        )

    # TODO: Use the async method when possible
    def get_span(self, url):
        self.force_flush_of_span_records()

        # Remove protocol
        url = re.sub(r"^.*?/v", "/v", url)
        public_workspace = public.get_public_user()
        spans_ds = Users.get_datasource(public_workspace, "spans")
        q = f"""
                SELECT
                    *
                FROM {public_workspace['database']}.{spans_ds.id}
                WHERE
                    start_datetime > (now() - INTERVAL 5 MINUTE) AND
                    url LIKE '%{url}%' AND
                    kind = 'server'
                ORDER BY start_datetime DESC
                FORMAT JSON
            """
        client = HTTPClient(public_workspace["database_server"], database=public_workspace["database"])
        _, body = client.query_sync(q, read_only=True)

        try:
            result = json.loads(body)
        except ValueError:
            raise Exception(f"Could not parse body as JSON: {body}") from None

        # There should only be one row, otherwise the url is not unique enough (or we didn't store it properly)
        self.assertEqual(result.get("rows"), 1, f"Could not find the span for {url}")
        return result.get("data")[0]

    async def get_span_async(self, url):
        self.force_flush_of_span_records()

        # Remove protocol
        url = re.sub(r"^.*?/v", "/v", url)
        public_workspace = public.get_public_user()
        spans_ds = Users.get_datasource(public_workspace, "spans")
        q = f"""
                SELECT
                    *
                FROM {public_workspace['database']}.{spans_ds.id}
                WHERE
                    start_datetime > (now() - INTERVAL 5 MINUTE) AND
                    url LIKE '%{url}%' AND
                    kind = 'server'
                ORDER BY start_datetime DESC
                FORMAT JSON
            """
        client = HTTPClient(public_workspace["database_server"], database=public_workspace["database"])
        _, body = await client.query(q, read_only=True)

        try:
            result = json.loads(body)
        except ValueError:
            raise Exception(f"Could not parse body as JSON: {body}") from None

        # There should only be one row, otherwise the url is not unique enough (or we didn't store it properly)
        self.assertEqual(result.get("rows"), 1, f"Could not find the span for {url}")
        return result.get("data")[0]

    async def _get_span_operation(self, operation: str, condition: str, span_expected: bool = True):
        async def _get_spans():
            self.force_flush_of_span_records()

            public_workspace = public.get_public_user()
            spans_ds = Users.get_datasource(public_workspace, "spans")
            q = f"""
                SELECT
                    *
                FROM {public_workspace['database']}.{spans_ds.id}
                WHERE
                    start_datetime > (now() - INTERVAL 5 MINUTE) AND
                    operation_name = '{operation}' AND
                    {condition}
                ORDER BY start_datetime DESC
                FORMAT JSON
            """
            client = HTTPClient(public_workspace["database_server"], database=public_workspace["database"])
            _, body = await client.query(q, read_only=True)

            try:
                result = json.loads(body)
            except ValueError:
                raise Exception(f"Could not parse body as JSON: {body}") from None

            span = result.get("data")
            if span_expected:
                self.assertEqual(len(span), 1)
            else:
                self.assertEqual(len(span), 0)
            return span

        return await poll_async(_get_spans)

    async def assert_workspace_span(
        self,
        workspace: User,
        operation: str,
        user: Optional[UserAccount] = None,
        organization_id: Optional[str] = None,
        deleted: bool = False,
        span_expected: bool = True,
    ) -> None:
        condition = f"workspace = '{workspace.id}'"
        spans = await self._get_span_operation(operation, condition, span_expected)

        if span_expected:
            self.assertEqual(spans[0]["workspace_name"], workspace.name)

            tags = json.loads(spans[0]["tags"])
            self.assertEqual(tags.get("plan"), workspace.plan)
            self.assertEqual(tags.get("database"), workspace.database)
            self.assertEqual(tags.get("database_server"), workspace.database_server)
            self.assertEqual(tags.get("origin"), workspace.origin)
            self.assertEqual(tags.get("organization_id"), organization_id)
            self.assertEqual(tags.get("created_at"), workspace.created_at.strftime("%Y-%m-%d %H:%M:%S"))

            if user:
                self.assertEqual(spans[0]["user"], user.id)

            deleted_at_found = tags.get("deleted_at", None) is not None
            self.assertEqual(deleted_at_found, deleted)

    async def assert_organization_span(
        self,
        organization: Organization,
        operation: str,
        user: Optional[UserAccount] = None,
        deleted: bool = False,
        span_expected: bool = True,
        extra: Optional[Dict[str, str]] = None,
    ) -> None:
        condition = f"JSONHas(tags, 'organization') AND JSONExtractString(tags, 'organization') = '{organization.id}'"
        spans = await self._get_span_operation(operation, condition, span_expected)

        if span_expected:
            tags = json.loads(spans[0]["tags"])
            self.assertEqual(tags.get("organization"), organization.id)
            self.assertEqual(tags.get("organization_name"), organization.name)
            self.assertEqual(tags.get("organization_domain"), organization.domain)
            self.assertEqual(tags.get("billing_plan"), organization.plan_details.get("billing"))
            self.assertEqual(tags.get("dedicated_clusters"), organization.get_dedicated_clusters_url())
            self.assertEqual(tags.get("created_at"), organization.created_at.strftime("%Y-%m-%d %H:%M:%S"))
            self.assertEqual(tags.get("cpus"), str(organization.commitment_cpu or "unknown"))
            if extra is not None:
                for k, v in extra.items():
                    self.assertEqual(tags.get(k), v)

            if organization.orb_external_customer_id:
                self.assertEqual(tags.get("orb_external_customer_id"), organization.orb_external_customer_id)

            if user:
                self.assertEqual(spans[0]["user"], user.id)

            deleted_at_found = tags.get("deleted_at", None) is not None
            self.assertEqual(deleted_at_found, deleted)

    # TODO: Use the async method when possible
    def flush_system_logs(self):
        cluster_host = User.default_database_server
        asyncio.run(ch_flush_logs_on_all_replicas(cluster_host, "tinybird"))

    async def flush_system_logs_async(self):
        cluster_host = User.default_database_server
        await ch_flush_logs_on_all_replicas(cluster_host, "tinybird")

    # TODO: Use the async method when possible
    def get_query_logs(self, query_id, current_database):
        cluster_host = User.default_database_server
        asyncio.run(ch_flush_logs_on_all_replicas(cluster_host, "tinybird"))
        client = HTTPClient(cluster_host, database=None)

        headers, body = client.query_sync(
            f"""
                SELECT query
                FROM clusterAllReplicas(tinybird, system.query_log)
                WHERE
                    event_time > (now() - INTERVAL 1 MINUTE) AND
                    query_id = '{query_id}' AND
                    current_database LIKE '{current_database}%'
                FORMAT JSON
            """
        )
        res = json.loads(body)

        self.assertEqual(res["rows"], 2, f"Could not find query_logs for {query_id}")
        return res.get("data")

    async def get_query_logs_async(self, query_id, current_database):
        cluster_host = User.default_database_server
        await ch_flush_logs_on_all_replicas(cluster_host, "tinybird")
        client = HTTPClient(cluster_host, database=None)
        headers, body = client.query_sync(
            f"""
                SELECT query
                FROM clusterAllReplicas(tinybird, system.query_log)
                WHERE
                    event_time > (now() - INTERVAL 1 MINUTE) AND
                    query_id = '{query_id}' AND
                    current_database LIKE '{current_database}%'
                FORMAT JSON
            """
        )
        res = json.loads(body)

        self.assertEqual(res["rows"], 2, f"Could not find query_logs for {query_id}")
        return res.get("data")

    async def get_log_comment_async(self, query_id, current_database):
        cluster_host = User.default_database_server
        await ch_flush_logs_on_all_replicas(cluster_host, "tinybird")
        client = HTTPClient(cluster_host, database=None)
        headers, body = client.query_sync(
            f"""
                SELECT query, log_comment
                FROM clusterAllReplicas(tinybird, system.query_log)
                WHERE
                    event_time > (now() - INTERVAL 1 MINUTE) AND
                    query_id = '{query_id}' AND
                    current_database LIKE '{current_database}%'
                FORMAT JSON
            """
        )
        res = json.loads(body)
        self.assertEqual(res["rows"], 2, f"Could not find log_comment for {query_id}")
        return res.get("data")

    async def get_query_logs_by_where_async(self, where_clause, exists=True):
        cluster_host = User.default_database_server
        await ch_flush_logs_on_all_replicas(cluster_host, "tinybird")
        client = HTTPClient(cluster_host, database=None)
        headers, body = client.query_sync(
            f"""
                        SELECT query, http_user_agent, current_database, log_comment, Settings
                        FROM clusterAllReplicas(tinybird, system.query_log)
                        WHERE
                            event_time > (now() - INTERVAL 1 MINUTE) AND
                            {where_clause}
                        FORMAT JSON
                    """
        )
        res = json.loads(body)
        self.assertEqual(res["rows"], 2 if exists else 0, f"Could not find query_logs for {where_clause}")
        return res.get("data")

    def get_query_logs_by_where(self, where_clause, exists=True):
        self.flush_system_logs()
        cluster_host = User.default_database_server
        client = HTTPClient(cluster_host, database=None)

        headers, body = client.query_sync(
            f"""
                        SELECT query, http_user_agent, current_database, log_comment
                        FROM clusterAllReplicas(tinybird, system.query_log)
                        WHERE
                            event_time > (now() - INTERVAL 1 MINUTE) AND
                            {where_clause}
                        FORMAT JSON
                    """
        )
        res = json.loads(body)
        num_logs = 2 if exists else 0
        self.assertEqual(res["rows"], num_logs, f"Could not find query_logs for {where_clause}")
        return res.get("data")

    def assert_datasources_ops_log(self, workspace, count=None, timeout=5, **datasource_ops_log):
        def _assert():
            appareances = 0
            workspace_ops_log_records = get_ops_log_records(workspace.id)
            for record in workspace_ops_log_records:
                if datasource_ops_log.items() <= record.items():
                    if count:
                        appareances += 1
                    else:
                        return
            if count and appareances:
                if appareances != count:
                    raise AssertionError(
                        f"{datasource_ops_log} found {appareances} expected {count} in {workspace_ops_log_records}"
                    )
            else:
                raise AssertionError(f"{datasource_ops_log} not found in {workspace_ops_log_records}")

        poll(_assert, timeout=timeout)

    def assert_releases_log(self, workspace, count=None, timeout=10, **releases_log):
        self.force_flush_of_span_records()

        def _assert():
            appareances = 0
            workspace_releases_log_records = get_releases_log_records(workspace.id)
            for record in workspace_releases_log_records:
                if releases_log.items() <= record.items():
                    if count:
                        appareances += 1
                    else:
                        return
            if count and appareances:
                if appareances != count:
                    raise AssertionError(
                        f"{releases_log} found {appareances} expected {count} in {workspace_releases_log_records}"
                    )
            else:
                raise AssertionError(f"{releases_log} not found in {workspace_releases_log_records}")

        poll(_assert, timeout=timeout)

    async def _insert_data_in_datasource(self, token, ds_name, data, assert_response=True):
        params = {
            "mode": "append",
            "token": token,
            "name": ds_name,
        }
        s = StringIO(data)
        import_response = await self.fetch_full_body_upload_async(f"/v0/datasources?{urlencode(params)}", s)
        if assert_response:
            self.assertEqual(import_response.code, 200, import_response.body)
        else:
            return import_response
        ds = json.loads(import_response.body)
        u_id = token_decode(token, "abcd")["u"]
        u = Users.get_by_id(u_id)

        self.wait_for_datasource_replication(u, ds["datasource"]["id"])

        return ds

    async def _insert_replace_data_in_datasource(self, token, ds_name, data, assert_response=True):
        params = {
            "mode": "replace",
            "token": token,
            "name": ds_name,
        }
        s = StringIO(data)
        import_response = await self.fetch_full_body_upload_async(f"/v0/datasources?{urlencode(params)}", s)
        if assert_response:
            self.assertEqual(import_response.code, 200, import_response.body)
        else:
            return import_response
        ds = json.loads(import_response.body)
        return ds

    async def _query(self, token: str, sql: str, extra_params: Optional[Dict] = None, expected_status_code: int = 200):
        params = {"token": token, "q": sql}

        if extra_params:
            params.update(extra_params)

        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, expected_status_code, response.body)
        try:
            return json.loads(response.body) if expected_status_code == 200 and response.body else None
        except Exception as ex:
            raise AssertionError(str(ex), response.body)

    def _check_table_in_database(self, database, table, exists=True, database_server=CH_ADDRESS):
        query = f"""SELECT count() as c
                    FROM system.tables
                    WHERE
                        database = '{database}'
                        and name = '{table}'
                    FORMAT JSON"""
        r = exec_sql(database, query, database_server=database_server)
        table_exists = int(r["data"][0]["c"]) == 1
        self.assertEqual(table_exists, exists)

    def _setup_cheriff_user(self):
        self.cheriff_user_admin_email = f"admin_{uuid.uuid4().hex}@tinybird.co"
        self.cheriff_workspace_admin_name = f"admin_ws_{uuid.uuid4().hex}"

        self.cheriff_user_admin = UserAccount.register(self.cheriff_user_admin_email, "pass")
        self.users_to_delete.append(self.cheriff_user_admin)
        self.cheriff_user_admin_token = UserAccount.get_token_for_scope(self.cheriff_user_admin, scopes.AUTH)

        self.cheriff_workspace_admin = self.register_workspace(
            self.cheriff_workspace_admin_name, admin=self.cheriff_user_admin.id
        )
        self.cheriff_workspace_admin_token = Users.get_token_for_scope(self.cheriff_workspace_admin, scopes.ADMIN)

    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def activate_prod_read_only(self, workspace: User):
        with User.transaction(workspace.id) as w:
            w.feature_flags[FeatureFlagWorkspaces.PROD_READ_ONLY.value] = True

    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def enable_shared_infra_billing_ff(self, user: UserAccount) -> UserAccount:
        with UserAccount.transaction(user.id) as user:
            user.feature_flags[FeatureFlag.SHARED_INFRA_FLOW.value] = True
            return user


class TBApiProxy:
    def __init__(self, test_instance: BaseTest):
        self._test_instance = test_instance

    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def activate_account(self, user_account: "UserAccount"):
        with UserAccount.transaction(user_account.id) as user_account:
            user_account["confirmed_account"] = True

    def register_user_and_workspace(
        self,
        email: str,
        workspace_name: str,
        cluster: CHCluster = DEFAULT_CLUSTER,
        normalize_name_and_try_different_on_collision: bool = False,
    ) -> User:
        user_account = self._test_instance.register_user(email, "pass")
        workspace = self._test_instance.register_workspace(
            workspace_name,
            user_account.id,
            cluster=cluster,
            normalize_name_and_try_different_on_collision=normalize_name_and_try_different_on_collision,
        )
        self.activate_account(user_account)

        asyncio.run(Users.create_database(workspace))
        return workspace

    def register_workspace(self, name: str, user_account: "UserAccount", cluster: CHCluster = DEFAULT_CLUSTER) -> User:
        workspace = User.register(name, admin=user_account.id, cluster=cluster)
        asyncio.run(Users.create_database(workspace))
        self._test_instance.workspaces_to_delete.append(workspace)
        return workspace

    def create_workspace(self, token: str, workspace_name: str):
        params = {
            "token": token,
            "name": workspace_name,
        }

        url = f"/v0/workspaces?{urlencode(params)}"
        response = self._test_instance.fetch(url, method="POST", body="")
        self._test_instance.assertEqual(response.code, 200, response.body)
        return json.loads(response.body)

    def create_datasource(self, token, ds_name, schema, engine_params=None, create_join_with_column=None):
        params = {"mode": "create", "token": token, "cluster": "tinybird", "name": ds_name, "schema": schema}

        if create_join_with_column:
            params.update(
                {
                    "engine_join_strictness": "ANY",
                    "engine_join_type": "INNER",
                    "engine_key_columns": create_join_with_column,
                }
            )

        if engine_params is not None:
            params.update(engine_params)

        ds_response = self._test_instance.fetch(f"/v0/datasources?{urlencode(params)}", method="POST", body="")

        self._test_instance.assertEqual(ds_response.code, 200, ds_response.body)
        ds = json.loads(ds_response.body)
        return ds

    def truncate_datasource(self, token, ds_name):
        params = {"token": token}

        ds_response = self._test_instance.fetch(
            f"/v0/datasources/{ds_name}/truncate?{urlencode(params)}", method="POST", body=""
        )
        self._test_instance.assertEqual(ds_response.code, 205, ds_response.body)

    def rename_workspace(self, workspace_id: str, token: str, workspace_name: str):
        url = f"/v0/workspaces/{workspace_id}?" + urlencode({"token": token, "name": workspace_name})
        response = self._test_instance.fetch(url, method="PUT", body="")
        self._test_instance.assertEqual(response.code, 200, response.body)

    def share_datasource_with_another_workspace(
        self, token, datasource_id, origin_workspace_id, destination_workspace_id, expect_notification: bool = True
    ) -> Datasource:
        MailgunService.send_notification_on_data_source_shared = AsyncMock(return_value=NotificationResponse(200))

        params = {
            "token": token,
            "origin_workspace_id": origin_workspace_id,
            "destination_workspace_id": destination_workspace_id,
        }
        response = self._test_instance.fetch(
            f"/v0/datasources/{datasource_id}/share?{urlencode(params)}", method="POST", body=""
        )
        self._test_instance.assertEqual(response.code, 200, response.body)

        destination_workspace = Users.get_by_id(destination_workspace_id)
        shared_data_source = destination_workspace.get_datasource(datasource_id, include_read_only=True)

        user_workspaces = UserWorkspaceRelationship.get_by_workspace(
            destination_workspace_id, destination_workspace.max_seats_limit
        )
        user_id = next((uw.user_id for uw in user_workspaces if uw.relationship == Relationships.ADMIN), None)
        user_receiving_the_email = UserAccounts.get_by_id(user_id).email

        if expect_notification:
            MailgunService.send_notification_on_data_source_shared.assert_called_with(
                [user_receiving_the_email],
                shared_data_source.name,
                destination_workspace.name,
                destination_workspace_id,
            )
        else:
            MailgunService.send_notification_on_data_source_shared.assert_not_called()

        return shared_data_source

    def invite_user_to_workspace(self, token, workspace_id, user_to_invite_email, role: str = "guest"):
        params = {"token": token, "operation": "add", "users": user_to_invite_email, "role": role}
        url = f"/v0/workspaces/{workspace_id}/users?{urlencode(params)}"

        response = self._test_instance.fetch(url, method="PUT", body="")
        self._test_instance.assertEqual(response.code, 200, response.body)

    @patch("stripe.Customer.create", return_value={"id": "cus_1234"})
    def create_customer(self, token, workspace_id, _create):
        params = {"token": token, "email": "random@email.com"}
        url = f"/v0/billing/{workspace_id}/customer?{urlencode(params)}"

        response = self._test_instance.fetch(url, method="POST", body="")
        self._test_instance.assertEqual(response.code, 200, response.body)
        _create.assert_called()

    @patch("stripe.SetupIntent.create", return_value={"client_secret": "secret_1234", "id": "setupintentid"})
    def setup_payment_intent(self, token, workspace_id, _create):
        params = {"token": token}
        url = f"/v0/billing/{workspace_id}/payment?{urlencode(params)}"

        response = self._test_instance.fetch(url, method="POST", body="")
        self._test_instance.assertEqual(response.code, 200, response.body)
        _create.assert_called()

    @patch("stripe.PaymentMethod.attach", return_value=None)
    @patch("stripe.Customer.modify", return_value=None)
    @patch("stripe.Subscription.create", return_value=STRIPE_SUBSCRIPTION_MOCK)
    @patch("stripe.SetupIntent.confirm", return_value=None)
    @patch("stripe.SetupIntent.retrieve", return_value={"status": "succeeded"})
    def subscribe_to_pro(self, token, workspace_id, _attach, _modify, _create, _confirm, _retrieve):
        params = {"token": token, "email": "random@email.com", "payment_method_id": "1234", "plan": "pro"}
        url = f"/v0/billing/{workspace_id}/subscription?{urlencode(params)}"

        response = self._test_instance.fetch(url, method="POST", body="")
        self._test_instance.assertEqual(response.code, 200, response.body)


class TBApiProxyAsync:
    def __init__(self, test_instance: BaseTest):
        self._test_instance = test_instance

    async def _fetch(self, path, method="get", **kwargs) -> requests.Response:
        get = sync_to_async(getattr(requests, method.lower()), thread_sensitive=False)
        response = await get(self._test_instance.get_host() + path, **kwargs)
        return response

    async def create_organization(
        self,
        name: str,
        user_token: str,
        domain: Optional[str] = None,
        workspace_ids: Optional[Iterable[str]] = None,
        admin_ids: Optional[Iterable[str]] = None,
        *,
        start_date: str = "",
        end_date: str = "",
        commited_processed: int = 0,
        commited_storage: int = 0,
        commited_data_transfer_intra: int = 0,
        commited_data_transfer_inter: int = 0,
        commitment_billing: str = "",
        commitment_machine_size: str = "",
    ) -> Organization:
        """This method shouldn't really be here. The only thing it does with the API is creating the org with the name"""
        params = {"token": user_token, "name": name}
        response = await self._test_instance.fetch_async(
            f"/v0/organizations?{urlencode(params)}", method="POST", body=b""
        )
        assert response.code == 200, response.body
        content = json.loads(response.body)
        self._test_instance.organizations_to_delete.append(content["id"])

        org = Organization.get_by_id(content["id"])
        if domain:
            org = await OrganizationService.update_name_and_domain(org, name, domain)

        if (
            start_date
            or end_date
            or commited_processed
            or commited_storage
            or commited_data_transfer_intra
            or commited_data_transfer_inter
            or commitment_billing
            or commitment_machine_size
        ):
            org = Organizations.update_commitment_information(
                org,
                start_date=start_date,
                end_date=end_date,
                commited_processed=commited_processed,
                commited_storage=commited_storage,
                commited_data_transfer_intra=commited_data_transfer_intra,
                commited_data_transfer_inter=commited_data_transfer_inter,
                commitment_billing=commitment_billing,
                commitment_machine_size=commitment_machine_size,
            )

        if workspace_ids:
            for id in workspace_ids:
                org = Organizations.add_workspace(org, User.get_by_id(id))

        if admin_ids:
            for id in admin_ids:
                org = await OrganizationService.add_admin(org, UserAccount.get_by_id(id).email)

        # Let's remove the organization once the test is done
        self._test_instance.organizations_to_delete.append(org.id)
        return org

    async def get_organization_info(self, token: str, organization_id: str):
        params = urlencode({"token": token})
        return await self._fetch(f"/v0/organizations/{organization_id}?{params}", method="GET")

    async def get_organization_consumption(self, token: str, organization_id: str, _from: str, to: str):
        params = urlencode({"token": token, "start_date": _from, "end_date": to})
        return await self._fetch(f"/v0/organizations/{organization_id}/consumption?{params}", method="GET")

    async def get_organization_metric(self, token: str, organization_id: str, metric: str, _from: str, to: str):
        params = urlencode({"token": token, "start_date": _from, "end_date": to})
        return await self._fetch(f"/v0/organizations/{organization_id}/metrics/{metric}?{params}", method="GET")

    async def get_organization_members(self, token: str, organization_id: str, include_workspaces: bool):
        params = urlencode({"token": token, "include_workspaces": "true" if include_workspaces else "false"})
        return await self._fetch(f"/v0/organizations/{organization_id}/members?{params}", method="GET")

    async def put_organization_members(
        self, token: str, organization_id: str, endpoint_parameters: Dict[str, str], assert_status_code: int = 200
    ) -> Dict[str, str]:
        endpoint_parameters["token"] = token
        params = urlencode(endpoint_parameters)
        response = await self._fetch(f"/v0/organizations/{organization_id}/members?{params}", method="PUT")
        self._test_instance.assertEqual(response.status_code, assert_status_code, response.content)
        return response.json()

    async def get_organization_workspaces(self, token: str, organization_id: str):
        params = urlencode({"token": token})
        return await self._fetch(f"/v0/organizations/{organization_id}/workspaces?{params}", method="GET")

    async def add_organization_workspace_to_commitment(self, token: str, organization_id: str, workspace_id: str):
        params = urlencode({"token": token, "workspace_id": workspace_id})
        return await self._fetch(f"/v0/organizations/{organization_id}/commitment?{params}", method="PUT")

    async def refresh_organization_token(self, token: str, organization_id: str, refresh_token: str):
        params = urlencode({"token": token})
        return await self._fetch(
            f"/v0/organizations/{organization_id}/tokens/{refresh_token}/refresh?{params}", method="POST"
        )

    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def activate_account(self, user_account: "UserAccount"):
        with UserAccount.transaction(user_account.id) as user_account:
            user_account["confirmed_account"] = True

    async def register_user_and_workspace(
        self,
        email: str,
        workspace_name: str,
        cluster: CHCluster = DEFAULT_CLUSTER,
        normalize_name_and_try_different_on_collision: bool = False,
    ) -> User:
        user_account = self._test_instance.register_user(email)
        workspace = self._test_instance.register_workspace(
            workspace_name,
            user_account.id,
            cluster,
            normalize_name_and_try_different_on_collision=normalize_name_and_try_different_on_collision,
        )
        self.activate_account(user_account)
        await Users.create_database(workspace)
        return workspace

    async def register_workspace(
        self, name: str, user_account: "UserAccount", cluster: CHCluster = DEFAULT_CLUSTER
    ) -> User:
        workspace = User.register(name, admin=user_account.id, cluster=cluster)
        await Users.create_database(workspace)
        self._test_instance.workspaces_to_delete.append(workspace)
        return workspace

    async def create_workspace(self, token: str, workspace_name: str, assign_to_organization: bool = False):
        params = {"token": token, "name": workspace_name}
        if assign_to_organization:
            params["assign_to_organization"] = "true"

        url = f"/v0/workspaces?{urlencode(params)}"
        response = await self._fetch(url, method="POST", data="")
        self._test_instance.assertEqual(response.status_code, 200, response.content)
        return response.json()

    async def delete_workspace(
        self, workspace_id: str, token: str, status: int = 200, hard_delete: bool = False
    ) -> Dict[str, Any]:
        params = {"token": token}
        if hard_delete:
            params["confirmation"] = User.get_by_id(workspace_id)["name"]
        url = f"/v0/workspaces/{workspace_id}?" + urlencode(params)
        response = await self._fetch(url, method="DELETE")
        self._test_instance.assertEqual(response.status_code, status, response.content)
        return response.json()

    async def create_branch(self, workspace_token: str, name: str) -> User:
        params = {"token": workspace_token, "name": name}
        url = f"/v0/environments?{urlencode(params)}"
        response = await self._fetch(url, method="POST")
        self._test_instance.assertEqual(response.status_code, 200, response.content)

        job_response = response.json()
        job_id = job_response["job"]["id"]
        job = await self._test_instance.get_finalised_job_async(job_id, token=workspace_token)
        self._test_instance.assertEqual(job["progress_percentage"], 100, job)
        self._test_instance.assertEqual(job["status"], "done", job)

        branch = User.get_by_id(job["branch_workspace"])
        self._test_instance.workspaces_to_delete.append(branch)

        return branch

    async def delete_branch(self, branch_id: str, token: str) -> None:
        url = f"/v0/environments/{branch_id}?" + urlencode({"token": token})
        response = await self._fetch(url, method="DELETE")
        self._test_instance.assertEqual(response.status_code, 200, response.content)
        return response.json()

    async def create_datasource(
        self, token, ds_name, schema, engine_params=None, create_join_with_column=None, format=None, branch_mode=None
    ):
        params = {"mode": "create", "token": token, "name": ds_name, "schema": schema, "branch_mode": branch_mode}

        if format:
            params.update({"format": format})

        if create_join_with_column:
            params.update(
                {
                    "engine_join_strictness": "ANY",
                    "engine_join_type": "INNER",
                    "engine_key_columns": create_join_with_column,
                }
            )

        if engine_params is not None:
            params.update(engine_params)

        ds_response = await self._fetch(f"/v0/datasources?{urlencode(params)}", method="POST", data="")

        self._test_instance.assertEqual(ds_response.status_code, 200, ds_response.content)
        return ds_response.json()

    async def create_connector(self, token: str, connector: DynamoDBConnector):
        params = connector.params()
        params["token"] = token

        ds_response = await self._fetch(f"/v0/connectors?{urlencode(params)}", method="POST", data="")

        self._test_instance.assertEqual(ds_response.status_code, 200, ds_response.content)
        return ds_response.json()

    async def get_datasource(self, token: str, ds_name_or_id: str) -> dict:
        params = {"token": token}
        ds_response = await self._fetch(f"/v0/datasources/{ds_name_or_id}?{urlencode(params)}")
        self._test_instance.assertEqual(ds_response.status_code, 200, ds_response.content)
        return ds_response.json()

    async def get_job(self, job_id: str, token: str) -> dict:
        params = {"token": token}
        job_response = await self._fetch(f"/v0/jobs/{job_id}?{urlencode(params)}", method="GET")
        self._test_instance.assertEqual(job_response.status_code, 200, job_response.content)
        return job_response.json()

    async def create_token(self, token: str, name: str, scope: str, status: int = 200) -> Dict[str, Any]:
        params = {"token": token, "name": name, "scope": scope}
        response = await self._test_instance.fetch_async(f"/v0/tokens?{urlencode(params)}", method="POST", body="")
        self._test_instance.assertEqual(response.code, status, response.body)
        return json.loads(response.body)

    async def invite_user_to_workspace(
        self, token, workspace_id, user_to_invite_email, role: str = "guest", assert_status_code: int = 200
    ):
        params = {"token": token, "operation": "add", "users": user_to_invite_email, "role": role}
        url = f"/v0/workspaces/{workspace_id}/users?{urlencode(params)}"

        response = await self._fetch(url, method="PUT", data="")
        self._test_instance.assertEqual(response.status_code, assert_status_code, response.content)

    async def make_user_workspace_admin(self, token, workspace_id, user_email):
        params = {
            "token": token,
            "operation": "change_role",
            "users": user_email,
            "new_role": "admin",
        }
        url = f"/v0/workspaces/{workspace_id}/users?{urlencode(params)}"

        response = await self._fetch(url, method="PUT", data="")
        self._test_instance.assertEqual(response.status_code, 200, response.content)

    async def update_user_workspace_role(self, token, workspace_id, user_email, new_role):
        params = {
            "token": token,
            "operation": "change_role",
            "users": user_email,
            "new_role": new_role,
        }
        url = f"/v0/workspaces/{workspace_id}/users?{urlencode(params)}"

        response = await self._fetch(url, method="PUT", data="")
        self._test_instance.assertEqual(response.status_code, 200, response.content)

    async def append_data_to_datasource(self, token: str, datasource: str, data: CsvIO):
        params = {
            "token": token,
            "name": datasource,
            "mode": "append",
        }
        append_url = f"/v0/datasources?{urlencode(params)}"
        response = await self._test_instance.fetch_full_body_upload_async(append_url, data)
        self._test_instance.assertEqual(response.code, 200, response.body)
        return json.loads(response.body)

    async def launch_import_job(
        self,
        token: str,
        datasource: str,
        format: str,
        url: str,
        mode: str = "append",
        expected_status_code: int = 200,
    ) -> httpclient.HTTPResponse:
        params = {"token": token, "name": datasource, "mode": mode, "format": format, "url": url}
        append_url = f"/v0/datasources?{urlencode(params)}"
        response = await self._test_instance.fetch_async(append_url, method="POST", body="")
        self._test_instance.assertEqual(response.code, expected_status_code)
        return response

    async def append_data_to_datasource_from_url(self, token: str, datasource: str, format: str, url: str):
        response = await self.launch_import_job(token=token, datasource=datasource, format=format, url=url)
        job_1 = await self._test_instance.get_finalised_job_async(json.loads(response.body)["id"], token=token)
        self._test_instance.assertEqual(job_1.status, "done", job_1)
        return job_1

    async def list_pipes(self, token: str, dependencies: Optional[bool] = None) -> httpclient.HTTPResponse:
        params = {"token": token}
        if dependencies is not None:
            params["dependencies"] = dependencies
        response = await self._test_instance.fetch_async(f"/v0/pipes?{urlencode(params)}")
        self._test_instance.assertEqual(response.code, 200)
        return response

    async def get_pipe_details(self, pipe_name: str, token: str) -> httpclient.HTTPResponse:
        params = {"token": token}
        response = await self._test_instance.fetch_async(f"/v0/pipes/{pipe_name}?{urlencode(params)}")
        return response

    async def create_pipe(
        self,
        token: str,
        pipe_name: str,
        queries: List[str],
        force: bool = False,
        extra_pipe_params: Optional[Dict[str, Any]] = None,
        assert_code: int = 200,
    ) -> httpclient.HTTPResponse:
        params = {"token": token, "force": "true" if force else "false"}

        nodes = [{"sql": query, "name": f"{pipe_name}_{i}"} for i, query in enumerate(queries)]

        pipe_def = {"token": token, "name": pipe_name, "nodes": nodes}

        if extra_pipe_params is not None:
            pipe_def.update(extra_pipe_params)

        pipe_def = json.dumps(pipe_def)
        response = await self._test_instance.fetch_async(
            f"/v0/pipes?{urlencode(params)}", method="POST", body=pipe_def, headers={"Content-type": "application/json"}
        )
        self._test_instance.assertEqual(response.code, assert_code)
        return response

    async def add_node_to_pipe(
        self, token: str, pipe_name: str, query: str, node_name: Optional[str] = None, assert_code: int = 200
    ) -> httpclient.HTTPResponse:
        params = {"token": token, "name": node_name if node_name else f"{pipe_name}_{uuid.uuid4().hex[:8]}"}
        response = await self._test_instance.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query
        )
        self._test_instance.assertEqual(response.code, assert_code)
        return response

    async def create_pipe_mv(
        self,
        workspace: User,
        token: str,
        pipe_name: str,
        view_name: str,
        target_ds_name: str,
        query: str,
        engine: Optional[str] = None,
        engine_sorting_key: Optional[str] = None,
        populate: Optional[str] = None,
        status_code: Optional[int] = 200,
        branch_mode: Optional[str] = None,
    ):
        if engine is None:
            engine = "MergeTree"
        if engine_sorting_key is None:
            engine_sorting_key = "tuple()"
        Users.add_pipe_sync(workspace, pipe_name, "select * from test_table")
        params = {
            "token": token,
            "name": view_name,
            "type": "materialized",
            "datasource": target_ds_name,
            "engine": engine,
            "engine_sorting_key": engine_sorting_key,
            "branch_mode": branch_mode,
        }
        if populate is not None:
            params.update({"populate": populate})
        response = await self._test_instance.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query
        )
        pipe_node = json.loads(response.body)
        self._test_instance.assertEqual(response.code, status_code)
        if status_code == 200:
            self._test_instance.assertEqual(pipe_node["name"], view_name)
            ds = Users.get_datasource(workspace, target_ds_name)
            self._test_instance.assertEqual(pipe_node["materialized"], ds.id)
        return pipe_node

    async def create_pipe_endpoint(
        self,
        workspace: User,
        token: str,
        pipe_name: str,
        query: str,
        assert_code: Optional[int] = 200,
        from_ui: Optional[bool] = False,
    ) -> None:
        Users.add_pipe_sync(workspace, pipe_name, query)
        node = Users.get_pipe(workspace, pipe_name).pipeline.nodes[0]
        node_id = node.id

        url = f"/v0/pipes/{pipe_name}/nodes/{node_id}/endpoint?token={token}"

        if from_ui:
            url = f"{url}&from=ui"

        response = await self._test_instance.fetch_async(url, method="POST", body=b"")
        self._test_instance.assertEqual(response.code, assert_code, response.body)

    async def create_pipe_copy(
        self,
        workspace: User,
        token: str,
        pipe_name: str,
        query: str,
        target_datasource: str,
        schedule_cron: Optional[str] = None,
    ):
        Users.add_pipe_sync(workspace, pipe_name, query)
        node = Users.get_pipe(workspace, pipe_name).pipeline.nodes[0]
        node_id = node.id

        params = {"token": token, "target_datasource": target_datasource}

        if schedule_cron:
            params["schedule_cron"] = schedule_cron

        response = await self._test_instance.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{node_id}/copy?{urlencode(params)}", method="POST", body=b""
        )
        self._test_instance.assertEqual(response.code, 200)

    async def make_endpoint(self, token: str, pipe_name_or_id: str, node_name_or_id: str):
        return await self._test_instance.fetch_async(
            f"/v0/pipes/{pipe_name_or_id}/nodes/{node_name_or_id}/endpoint?token={token}", method="POST", body=b""
        )

    async def make_materialized_view(
        self, token: str, pipe_name_or_id: str, node_name_or_id: str, datasource: str, populate: str = "false"
    ):
        params = {"token": token, "datasource": datasource, "engine": "MergeTree", "populate": populate}
        return await self._test_instance.fetch_async(
            f"/v0/pipes/{pipe_name_or_id}/nodes/{node_name_or_id}/materialization?{urlencode(params)}",
            method="POST",
            body="",
        )

    async def remove_pipe(self, token: str, pipe_name: str):
        params = {
            "token": token,
        }
        update_response = await self._fetch(f"/v0/pipes/{pipe_name}?{urlencode(params)}", method="DELETE")
        self._test_instance.assertEqual(update_response.status_code, 204, update_response.content)

    async def remove_datasource(
        self, token: str, ds_name: str, branch_mode: Optional[str] = None, force: Optional[bool] = False
    ):
        params = {"token": token, "branch_mode": branch_mode, "force": "true" if force else "false"}
        delete_response = await self._fetch(f"/v0/datasources/{ds_name}?{urlencode(params)}", method="DELETE")
        self._test_instance.assertEqual(delete_response.status_code, 204, delete_response.content)

    async def rename_datasource(self, token, datasource_name, new_name):
        params = {"token": token, "name": new_name}

        ds_response = await self._fetch(f"/v0/datasources/{datasource_name}?{urlencode(params)}", method="PUT")

        ds = json.loads(ds_response.content)
        self._test_instance.assertEqual(ds_response.status_code, 200, ds_response.content)
        return ds

    async def rename_workspace(self, workspace_id: str, token: str, workspace_name: str):
        url = f"/v0/workspaces/{workspace_id}?" + urlencode({"token": token, "name": workspace_name})
        response = await self._fetch(url, method="PUT", data="")
        self._test_instance.assertEqual(response.status_code, 200, response.content)

    async def replace_data_to_datasource(
        self, token: str, datasource: str, data: CsvIO, replace_truncate_when_empty: bool
    ):
        params = {"token": token, "name": datasource, "mode": "replace"}
        if replace_truncate_when_empty is not None:
            if replace_truncate_when_empty is True:
                params["replace_truncate_when_empty"] = "true"
            else:
                params["replace_truncate_when_empty"] = "false"

        replace_url = f"/v0/datasources?{urlencode(params)}"
        response = await self._test_instance.fetch_full_body_upload_async(replace_url, data)
        self._test_instance.assertEqual(response.code, 200, response.body)
        return json.loads(response.body)

    async def share_datasource_with_another_workspace(
        self, token, datasource_id, origin_workspace_id, destination_workspace_id, expect_notification: bool = True
    ) -> Datasource:
        MailgunService.send_notification_on_data_source_shared = AsyncMock(return_value=NotificationResponse(200))

        params = {
            "token": token,
            "origin_workspace_id": origin_workspace_id,
            "destination_workspace_id": destination_workspace_id,
        }
        response = await self._fetch(
            f"/v0/datasources/{datasource_id}/share?{urlencode(params)}", method="POST", data=""
        )
        self._test_instance.assertEqual(response.status_code, 200, response.content)

        destination_workspace = Users.get_by_id(destination_workspace_id)
        shared_data_source = destination_workspace.get_datasource(datasource_id, include_read_only=True)

        user_workspaces = UserWorkspaceRelationship.get_by_workspace(
            destination_workspace_id, destination_workspace.max_seats_limit
        )

        if expect_notification:
            user_making_the_request_id = token_decode(token, "abcd")["u"]

            user_id = next((uw.user_id for uw in user_workspaces if uw.user_id != user_making_the_request_id), None)
            user_receiving_the_email = UserAccounts.get_by_id(user_id).email

            MailgunService.send_notification_on_data_source_shared.assert_called_with(
                [user_receiving_the_email],
                shared_data_source.name,
                destination_workspace.name,
                destination_workspace_id,
            )
        else:
            MailgunService.send_notification_on_data_source_shared.assert_not_called()

        return shared_data_source

    async def create_datasource_from_data(self, token, ds_name, data, extra_params=None):
        params = {"token": token, "name": ds_name}
        if extra_params is not None:
            params.update(extra_params)

        ds_response = await self._test_instance.fetch_full_body_upload_async(
            f"/v0/datasources?{urlencode(params)}", data
        )

        ds = json.loads(ds_response.body)
        self._test_instance.assertEqual(ds_response.code, 200, ds_response.body)
        return ds

    @patch("stripe.Customer.create", return_value={"id": "cus_1234"})
    async def create_customer(self, token, workspace_id, _create):
        params = {"token": token, "email": "random@email.com"}
        url = f"/v0/billing/{workspace_id}/customer?{urlencode(params)}"

        response = await self._fetch(url, method="POST", data="")
        self._test_instance.assertEqual(response.status_code, 200, response.content)
        _create.assert_called()

    @patch("stripe.SetupIntent.create", return_value={"client_secret": "secret_1234", "id": "setupintentid"})
    async def setup_payment_intent(self, token, workspace_id, _create):
        params = {"token": token}
        url = f"/v0/billing/{workspace_id}/payment?{urlencode(params)}"

        response = await self._fetch(url, method="POST", data="")
        self._test_instance.assertEqual(response.status_code, 200, response.content)
        _create.assert_called()

    @patch("stripe.PaymentMethod.attach", return_value=None)
    @patch("stripe.Customer.modify", return_value=None)
    @patch("stripe.Subscription.create", return_value=STRIPE_SUBSCRIPTION_MOCK)
    @patch("stripe.SetupIntent.confirm", return_value=None)
    @patch("stripe.SetupIntent.retrieve", return_value={"status": "succeeded"})
    async def subscribe_to_pro(self, token, workspace_id, _attach, _modify, _create, _confirm, _retrieve):
        params = {"token": token, "email": "random@email.com", "payment_method_id": "1234", "plan": "pro"}
        url = f"/v0/billing/{workspace_id}/subscription?{urlencode(params)}"

        response = await self._fetch(url, method="POST", data="")
        self._test_instance.assertEqual(response.status_code, 200, response.content)

    async def cheriff(
        self,
        path: str,
        params: Dict[str, str],
        expected_code: int = 200,
        cookies: Optional[Dict[str, str]] = None,
        request_method: str = "POST",
        follow_redirects: bool = True,
        user_token: str = "",
        workspace_token: str = "",
    ) -> httpclient.HTTPResponse:
        cookies = cookies or {
            "token": user_token.encode(),
            "workspace_token": workspace_token.encode(),
        }

        def side_effect(token_cookie_name):
            return cookies[token_cookie_name]

        with patch.object(BaseHandler, "get_secure_cookie", side_effect=side_effect):
            with patch.object(RequestHandler, "check_xsrf_cookie", side_effect=lambda: None):
                body = urlencode(params) if params else None
                response = await self._test_instance.fetch_async(
                    f"/cheriff{path}", method=request_method, body=body, follow_redirects=follow_redirects
                )
                self._test_instance.assertEqual(response.code, expected_code, response.body)
                return response

    async def _create_datasource_for_playground(
        self, workspace_id: str, name: str, schema: str, with_last_date: bool = False
    ) -> Dict[str, Any]:
        u = Users.get_by_id(workspace_id)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
            "mode": "create",
            "name": name,
            "with_last_date": "true" if with_last_date else "false",
            "schema": schema,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self._fetch(create_url, method="POST", data="")
        self._test_instance.assertEqual(response.status_code, 200, response.json())
        return response.json()["datasource"]

    async def create_playground(
        self,
        workspace_id: str,
        token: str,
        name: Optional[str] = None,
        sql: Optional[str] = None,
        semver: Optional[str] = None,
    ):
        ds_name = f"{name}_datasource"
        _ = await self._create_datasource_for_playground(workspace_id, ds_name, "date Date, a Int32")
        params = {
            "token": token,
            "workspace_id": workspace_id,
        }
        if semver:
            params["__tb__semver"] = semver
        response = await self._fetch(
            f"/v0/playgrounds?{urlencode(params)}",
            method="POST",
            data=json.dumps(
                {
                    "name": name,
                    "nodes": [
                        {
                            "name": f"{name}_0",
                            "sql": sql or f"select * from {ds_name}",
                        }
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self._test_instance.assertEqual(response.status_code, 200, json.loads(response.content))
        return response

    async def modify_playground(
        self,
        workspace_id: str,
        token: str,
        playground_id: str,
        config: Optional[Dict[str, Any]] = None,
    ):
        params = {
            "token": token,
            "workspace_id": workspace_id,
        }
        response = await self._fetch(
            f"/v0/playgrounds/{playground_id}?{urlencode(params)}",
            method="PUT",
            data=json.dumps(config or {}),
        )
        self._test_instance.assertEqual(response.status_code, 200, json.loads(response.content))
        return response

    async def delete_playground(self, workspace_id: str, token: str, playground_id: str):
        params = {
            "token": token,
            "workspace_id": workspace_id,
        }
        response = await self._fetch(f"/v0/playgrounds/{playground_id}?{urlencode(params)}", method="DELETE")
        self._test_instance.assertEqual(response.status_code, 200, json.loads(response.content))
        return response


def mock_retry_sync(
    exception_to_check: Union[Type[Exception], Tuple[Type[Exception], ...]],
    tries: int = 10,
    delay: float = 1,
    backoff: float = 1.5,
    ch_error_codes: Optional[List[int]] = None,
) -> Callable[[Callable[P, RT]], Callable[P, RT]]:
    return retry_sync(
        exception_to_check=exception_to_check,
        tries=1,
        delay=0.01,
        backoff=1.0,
        ch_error_codes=ch_error_codes,
    )
