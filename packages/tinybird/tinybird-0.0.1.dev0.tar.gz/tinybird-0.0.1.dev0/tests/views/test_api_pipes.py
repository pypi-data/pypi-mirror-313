import asyncio
import json
import re
import uuid
from datetime import datetime
from functools import partial
from io import StringIO
from unittest import mock
from unittest.mock import AsyncMock, MagicMock, patch
from urllib.parse import urlencode

import pkg_resources
import pytest
import requests
import tornado
from _pytest.monkeypatch import MonkeyPatch
from chtoolset import query as chquery
from mock import Mock
from prometheus_client.parser import text_string_to_metric_families

from tests.populates.test_pool_replica import CI_JOBS_CLUSTER_NAME, CI_JOBS_REPLICA, set_dynamic_disk_settings
from tests_e2e.aux import numericRange
from tinybird.ch import HTTPClient, _get_query_log, _get_query_status, ch_flush_logs_on_all_replicas
from tinybird.ch_utils.exceptions import CHException
from tinybird.ch_utils.user_profiles import WorkspaceUserProfiles
from tinybird.cluster_settings import ClusterSettings, ClusterSettingsOperations
from tinybird.constants import BillingPlans
from tinybird.data_connector import DataConnector, DataSink
from tinybird.feature_flags import FeatureFlagWorkspaces
from tinybird.gc_scheduler.constants import SchedulerJobActions
from tinybird.gc_scheduler.scheduler_jobs import GCloudSchedulerJobs
from tinybird.internal_thread import WorkspaceDatabaseUsageTracker
from tinybird.job import JobKind, JobStatus
from tinybird.limits import EndpointLimits
from tinybird.model import retry_transaction_in_case_of_concurrent_edition_error_async
from tinybird.monitor import EndpointMonitorTask, OldAndStuckJobsMetricsMonitorTask
from tinybird.organization.organization import OrganizationCommitmentsPlans, Organizations
from tinybird.pg import PGService
from tinybird.pipe import PipeNode, PipeNodeTypes, PipeTypes
from tinybird.populates.cluster import get_pool_replicas
from tinybird.populates.job import PopulateJob
from tinybird.syncasync import async_to_sync
from tinybird.token_scope import scopes
from tinybird.user import QueryNotAllowed, User, UserAccount, Users, public
from tinybird.user_workspace import UserWorkspaceRelationships
from tinybird.views.api_pipes import PipeUtils
from tinybird.views.api_query import max_threads_by_endpoint
from tinybird.views.base import QUERY_API, QUERY_API_FROM_UI, ApiHTTPError
from tinybird_shared.clickhouse.errors import CHErrors
from tinybird_shared.metrics.statsd_client import statsd_client

from ..conftest import (
    CH_ADDRESS,
    CH_HOST,
    CH_HTTP_PORT,
    KAFKA_MIN_CH_VERSION_NEEDED,
    OTHER_USER_PROFILE,
    ClusterPatches,
    HTTPClient_query_original,
    get_min_clickhouse_version,
)
from ..utils import CsvIO, exec_sql, poll, poll_async, wait_until_job_is_in_expected_status_async
from .base_test import BaseTest, TBApiProxyAsync, create_test_datasource, drop_test_datasource, matches, mock_retry_sync


class TestAPIPipeStats(BaseTest):
    def setUp(self):
        self.mpatch = MonkeyPatch()
        super().setUp()

    def tearDown(self):
        self._drop_token()
        self.mpatch.undo()
        super().tearDown()

    async def assert_stats(self, datasource_id, token, expected_row_count, expected_bytes):
        ds_url = f"/v0/datasources/{datasource_id}?token={token}"
        response = await self.fetch_async(ds_url)
        self.__assert_stats_response(response, expected_row_count, expected_bytes)

    def __assert_stats_response(self, response, expected_row_count, expected_bytes):
        self.assertEqual(response.code, 200)
        payload = json.loads(response.body)
        statistics = payload["statistics"]
        self.assertEqual(statistics["row_count"], expected_row_count)
        # 50% margin
        self.assertAlmostEqual(statistics["bytes"], expected_bytes, delta=expected_bytes * 0.5)

    async def create_population_for_cancellation(self, pipe_name, ds_name_source, target_ds_name):
        # we've tried to fix flakyness by making the populate job run on several partitions
        # among other things => https://gitlab.com/tinybird/analytics/-/merge_requests/4493
        # if tests depending on this method continue to be flaky we should opt for following a similar
        # approach as in `test_jobs.py` using semaphores to have more control on the job execution
        Users.add_pipe_sync(self.base_workspace, pipe_name, "select * from test_table")

        params = {
            "token": self.admin_token,
            "name": ds_name_source,
            "mode": "create",
            "schema": "number UInt64, key String",
            "engine": "MergeTree",
            "engine_partition_key": "key",
        }
        response = await self.fetch_async(f"/v0/datasources?{urlencode(params)}", method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        params = {
            "token": self.admin_token,
            "name": ds_name_source,
            "mode": "append",
            "url": self.get_url_for_sql(
                "select 1 as number, toString(number % 3) as key from numbers(100000000) format CSVWithNames"
            ),
        }
        response = await self.fetch_async(f"/v0/datasources?{urlencode(params)}", method="POST", body="")
        self.assertEqual(response.code, 200, response.body)
        response = json.loads(response.body)
        job = await self.get_finalised_job_async(response["job_id"])
        self.assertEqual(job.get("status"), "done", job)

        # create a pipe's node with a view to that datasource
        params = {
            "token": self.admin_token,
            "name": target_ds_name,
            "mode": "create",
            "schema": "number UInt64, key  String",
            "engine": "MergeTree",
            "engine_sorting_key": "key",
        }
        response = await self.fetch_async(f"/v0/datasources?{urlencode(params)}", method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        params = {
            "token": self.admin_token,
            "name": f"{pipe_name}_node",
            "type": "materialized",
            "datasource": target_ds_name,
            "populate": "true",
        }
        query = f"SELECT * FROM {ds_name_source}"
        response = await self.fetch_async(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(pipe_node["name"], f"{pipe_name}_node")
        ds = Users.get_datasource(self.base_workspace, target_ds_name)
        self.assertEqual(pipe_node["materialized"], ds.id)
        self.assertIn("job", pipe_node)
        job_response = pipe_node["job"]
        self.assertEqual(job_response["id"], job_response["job_id"])
        self.assertEqual(job_response["kind"], JobKind.POPULATE)
        return job_response

    def _drop_token(self):
        try:
            u = Users.get_by_id(self.WORKSPACE_ID)
            token = Users.get_token(u, "test")
            if token:
                Users.drop_token(u, token)
        except Exception:
            pass

    async def make_endpoint(self, pipe_name, pipe_node, expected_code=200):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{pipe_node['id']}/endpoint?token={token}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, expected_code)


class APIDataTableBaseTest(BaseTest):
    def setUp(self):
        self.endpoint_node = None
        super().setUp()
        self.create_test_datasource()

    def tearDown(self):
        self._drop_token()
        super().tearDown()

    async def _get_pipe_data(self, fmt, expected_code=200, params=None, token_name="test_2", token=None, headers=False):
        u = Users.get_by_id(self.WORKSPACE_ID)
        if token is None:
            token = Users.add_token(u, token_name, scopes.ADMIN)
        _params = {"token": token}
        if params is not None:
            _params.update(params)

        response = await self.fetch_async(f"/v0/pipes/test_pipe.{fmt}?{urlencode(_params)}")
        self.assertEqual(response.code, expected_code)
        if headers:
            return response.body, response.headers
        return response.body

    async def _make_endpoint(self, node_id=None, token_name="test"):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, token_name, scopes.ADMIN, self.USER_ID)
        if not node_id:
            self.endpoint_node = Users.get_pipe(u, "test_pipe").pipeline.nodes[0]
            node_id = self.endpoint_node.id
        else:
            self.endpoint_node = Users.get_node(u, node_id)
        response = await self.fetch_async(
            f"/v0/pipes/test_pipe/nodes/{node_id}/endpoint?token={token}", method="POST", body=b""
        )
        self.assertEqual(response.code, 200, response.body)

    def _drop_token(self):
        try:
            u = Users.get_by_id(self.WORKSPACE_ID)
            token = Users.get_token(u, "test")

            if token:
                Users.drop_token(u, token)

            token_2 = Users.get_token(u, "test_2")

            if token_2:
                Users.drop_token(u, token_2)
        except Exception:
            pass


class TestAPIDataTable(APIDataTableBaseTest):
    @tornado.testing.gen_test
    async def test_pipe_data_json_with_no_endpoint(self):
        payload = await self._get_pipe_data("json", 404)
        payload = json.loads(payload)
        self.assertEqual(payload["error"], "The pipe 'test_pipe' does not have an endpoint yet")

    @tornado.testing.gen_test
    async def test_pipe_data_json_with_endpoint(self):
        await self._make_endpoint()
        payload = await self._get_pipe_data("json")
        payload = json.loads(payload)
        self.assertTrue("statistics" in payload)
        self.assertTrue("meta" in payload)
        self.assertEqual(len(payload["data"]), 6)

    @tornado.testing.gen_test
    async def test_pipe_data_prometheus_with_endpoint(self):
        pipe = Users.add_pipe_sync(
            self.base_workspace, "prometheus_pipe", "select 'metric' as name, 'counter' as type, 1 as value"
        )
        token = Users.add_token(self.base_workspace, "token", scopes.ADMIN, self.USER_ID)
        response = await self.fetch_async(
            f"/v0/pipes/prometheus_pipe/nodes/{pipe.pipeline.nodes[0].id}/endpoint?token={token}",
            method="POST",
            body=b"",
        )
        self.assertEqual(response.code, 200, response.body)
        _params = {"token": token}
        response = await self.fetch_async(f"/v0/pipes/prometheus_pipe.prometheus?{urlencode(_params)}")
        self.assertEqual(response.code, 200)
        parsed_metrics = text_string_to_metric_families(response.body.decode())
        for metric in parsed_metrics:
            self.assertEqual(metric.name, "metric", metric)
            self.assertEqual(metric.type, "counter", metric)

    @tornado.testing.gen_test
    async def test_pipe_data_prometheus_with_endpoint_not_valid(self):
        await self._make_endpoint()
        with patch("tinybird.ch.HTTPClient.query") as query_patch:
            query_patch.side_effect = CHException(
                "Code: 36. DB::Exception: Column 'name' is required for output format 'Prometheus'. (BAD_ARGUMENTS)"
            )
            await self._get_pipe_data("prometheus", expected_code=400)

    @tornado.testing.gen_test
    async def test_pipe_spans_with_query_id(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "token_for_spans", scopes.ADMIN)
        await self._make_endpoint()
        await self._get_pipe_data("json", token=token)
        span = await self.get_span_async(f"/v0/pipes/test_pipe.json?token={token}")
        query_id = span["span_id"]

        requests_tags = json.loads(span["tags"])
        self.assertEqual(requests_tags["result_rows"], "6", span)

        if get_min_clickhouse_version() >= pkg_resources.parse_version("24.6.10.2"):
            self.assertGreater(int(requests_tags["virtual_cpu_time_microseconds"]), 0, span)

        pipe = Users.get_pipe(u, "test_pipe")
        query_logs = await self.get_query_logs_async(query_id, u.database)
        self.assertEqual(len(query_logs), 2)
        expected_query = (
            f"SELECT * FROM (SELECT * FROM {u.database}.{self.datasource.id} AS test_table) as {pipe.name} FORMAT JSON"
        )
        for query_log in query_logs:
            self.assertEqual(chquery.format(query_log["query"]), chquery.format(expected_query))

    @tornado.testing.gen_test
    async def test_pipe_data_csv_no_endpoint(self):
        payload = await self._get_pipe_data("csv", 404)
        payload = json.loads(payload)
        self.assertEqual(payload["error"], "The pipe 'test_pipe' does not have an endpoint yet")

    @tornado.testing.gen_test
    async def test_pipe_data_csv(self):
        await self._make_endpoint()
        payload = await self._get_pipe_data("csv")
        self.assertEqual(len(list(filter(None, payload.split(b"\n")))), 1 + 6)  # header + data

    @tornado.testing.gen_test
    async def test_pipe_data_with_post_request(self):
        await self._make_endpoint()
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test_2", scopes.ADMIN, self.USER_ID)

        url = f"/v0/pipes/test_pipe.json?token={token}"
        response = await self.fetch_async(url, method="POST", body="asdf")
        self.assertEqual(response.code, 200)
        payload = response.body
        payload = json.loads(payload)
        self.assertEqual(payload["rows"], 6)

        span = await self.get_span_async(url)
        requests_tags = json.loads(span["tags"])
        self.assertEqual(requests_tags["result_rows"], "6", span)
        if get_min_clickhouse_version() >= pkg_resources.parse_version("24.6.10.2"):
            self.assertGreater(int(requests_tags["virtual_cpu_time_microseconds"]), 0, span)

    @tornado.testing.gen_test
    async def test_pipe_data_with_post_request_using_profile_limits(self):
        await self._make_endpoint()
        u = Users.get_by_id(self.WORKSPACE_ID)
        u = Users.add_profile(u, WorkspaceUserProfiles.ENDPOINT_USER_PROFILE.value, OTHER_USER_PROFILE)
        token = Users.add_token(u, "test_profile_limits_1", scopes.ADMIN, self.USER_ID)

        url = f"/v0/pipes/test_pipe.json?token={token}"
        response = {}

        with patch.object(HTTPClient, "query", side_effect=HTTPClient_query_original, autospec=True) as mock_query:
            response = await self.fetch_async(url, method="POST", body="asdf")
            self.assertEqual(len(mock_query.call_args_list), 1, mock_query.call_args_list)
            self.assertEqual(mock_query.call_args_list[0].kwargs.get("user"), OTHER_USER_PROFILE)
            self.assertEqual(mock_query.call_args_list[0].kwargs.get("fallback_user_auth"), True)

        self.assertEqual(response.code, 200)
        payload = response.body
        payload = json.loads(payload)
        self.assertEqual(payload["rows"], 6)

        span = await self.get_span_async(url)
        requests_tags = json.loads(span["tags"])
        self.assertEqual(requests_tags["result_rows"], "6", span)

        if get_min_clickhouse_version() >= pkg_resources.parse_version("24.6.10.2"):
            self.assertGreater(int(requests_tags["virtual_cpu_time_microseconds"]), 0, span)
        self.assertEqual(requests_tags["user_profile"], OTHER_USER_PROFILE, span)
        Users.delete_profile(u, WorkspaceUserProfiles.ENDPOINT_USER_PROFILE.value)

    @tornado.testing.gen_test
    async def test_pipe_data_with_post_request_using_profile_limits_fallback(self):
        await self._make_endpoint()
        WRONG_USER_PROFILE = "wrong_user_profile"
        u = Users.get_by_id(self.WORKSPACE_ID)
        u = Users.add_profile(u, WorkspaceUserProfiles.ENDPOINT_USER_PROFILE.value, WRONG_USER_PROFILE)
        token = Users.add_token(u, "test_profile_limits_2", scopes.ADMIN, self.USER_ID)

        url = f"/v0/pipes/test_pipe.json?token={token}"
        response = {}

        with patch.object(HTTPClient, "query", side_effect=HTTPClient_query_original, autospec=True) as mock_query:
            response = await self.fetch_async(url, method="POST", body="asdf")
            self.assertEqual(len(mock_query.call_args_list), 2)
            # First query fails
            self.assertEqual(mock_query.call_args_list[0].kwargs.get("user"), WRONG_USER_PROFILE)
            self.assertEqual(mock_query.call_args_list[0].kwargs.get("fallback_user_auth"), True)
            # Second query works with no user/profile
            self.assertIsNone(mock_query.call_args_list[1].kwargs.get("user"))
            self.assertEqual(mock_query.call_args_list[1].kwargs.get("fallback_user_auth"), False)

        self.assertEqual(response.code, 200)
        payload = response.body
        payload = json.loads(payload)
        self.assertEqual(payload["rows"], 6)

        span = await self.get_span_async(url)
        requests_tags = json.loads(span["tags"])
        self.assertEqual(requests_tags["result_rows"], "6", span)
        if get_min_clickhouse_version() >= pkg_resources.parse_version("24.6.10.2"):
            self.assertGreater(int(requests_tags["virtual_cpu_time_microseconds"]), 0, span)
        self.assertEqual(requests_tags["user_profile"], WRONG_USER_PROFILE, span)

        Users.delete_profile(u, WorkspaceUserProfiles.ENDPOINT_USER_PROFILE.value)

    @tornado.testing.gen_test
    async def test_pipe_data_too_many_simultaneous_queries(self):
        await self._make_endpoint()
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "token_too_many_queries", scopes.ADMIN)
        url = f"/v0/pipes/test_pipe.json?token={token}"

        with patch(
            "tinybird.ch.HTTPClient.query",
            side_effect=CHException(
                "Code: 202. DB::Exception: Too many simultaneous queries. Maximum: 250. (TOO_MANY_SIMULTANEOUS_QUERIES) (version x.x.x)\n"
            ),
        ):
            response = await self.fetch_async(url)
            self.assertEqual(response.code, 500)
            payload = response.body
            payload = json.loads(payload)
            self.assertTrue("" in payload["error"])
            self.assertTrue(
                "The server is processing too many queries at the same time. This could be because there are more requests than usual, because they are taking longer, or because the server is overloaded. Please check your requests or contact us at support@tinybird.co"
                in payload["error"],
                payload,
            )
            self.assertEqual(payload["documentation"], "")

    def test_pipe_data_json_with_query_no_endpoint(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)

        url = f"/v0/pipes/test_pipe.json?token={token}&q=select+count()+c+from+_"
        response = self.fetch(url)
        self.assertEqual(response.code, 404)
        payload = json.loads(response.body)
        self.assertEqual(payload["error"], "The pipe 'test_pipe' does not have an endpoint yet")

        span = self.get_span(url)
        requests_tags = json.loads(span["tags"])
        self.assertTrue("result_rows" not in requests_tags)
        self.assertTrue("virtual_cpu_time_microseconds" not in requests_tags)

    @tornado.testing.gen_test
    async def test_pipe_data_json_with_query(self):
        await self._make_endpoint(token_name="test_3")
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)

        url = f"/v0/pipes/test_pipe.json?token={token}&q=select+count()+c+from+_"
        response = await self.fetch_async(url)
        self.assertEqual(response.code, 200)
        payload = json.loads(response.body)
        self.assertEqual(payload["data"][0]["c"], 6)

        span = await self.get_span_async(url)
        requests_tags = json.loads(span["tags"])
        self.assertEqual(requests_tags["result_rows"], "1", span)

        if get_min_clickhouse_version() >= pkg_resources.parse_version("24.6.10.2"):
            self.assertGreater(int(requests_tags["virtual_cpu_time_microseconds"]), 0, span)

        response = await self.fetch_async(
            f"/v0/pipes/test_pipe.json?token={token}", method="POST", body="q=select+count()+c+from+_"
        )
        self.assertEqual(response.code, 200)
        payload = response.body
        payload = json.loads(payload)
        self.assertEqual(payload["data"][0]["c"], 6)

    @tornado.testing.gen_test
    async def test_pipe_data_json_with_query_template(self):
        await self._make_endpoint(token_name="test_3")
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)
        response = await self.fetch_async(f"/v0/pipes/test_pipe.json?token={token}&q=%select+count()+c+from+_")
        self.assertEqual(response.code, 400)
        body = json.loads(response.body)
        self.assertEqual(body["error"], "'q' parameter doesn't support templates")

    @tornado.testing.gen_test
    async def test_pipe_node_validate_name(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        data = json.dumps({"name": "111", "nodes": [{"name": "node_111", "sql": "select 1"}]})
        response = await self.fetch_async(
            f"/v0/pipes?token={token}", headers={"Content-type": "application/json"}, method="POST", body=data
        )
        self.assertEqual(response.code, 400)
        result = json.loads(response.body)
        self.assertTrue("Invalid pipe name" in result["error"])

    def test_pipe_name_with_invalid_chars_dashes(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
        }

        data = {"name": "-pipe-name-with-dashes", "nodes": [{"sql": "select 1", "name": "node_00"}]}

        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        response_body = json.loads(response.body)
        self.assertEqual(response.code, 400, response.body)
        self.assertTrue("Invalid pipe name" in response_body["error"])

    # This test is representative of some pipe names that can be found in production (even though the documentation says
    # they are not valid). Removing or modifying this test will almost certainly break some endpoints for some customers in production.
    def test_pipe_name_with_valid_chars_starting_underscore(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
        }

        data = {"name": "_pipe_name_with_starting_underscore", "nodes": [{"sql": "select 1", "name": "node_00"}]}

        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

    @tornado.testing.gen_test
    async def test_pipe_validate_forbidden_name(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        data = json.dumps({"name": "FROM", "nodes": [{"name": "node_111", "sql": "select 1"}]})
        response = await self.fetch_async(
            f"/v0/pipes?token={token}", headers={"Content-type": "application/json"}, method="POST", body=data
        )
        self.assertEqual(response.code, 400)
        result = json.loads(response.body)
        self.assertTrue(
            "FROM is a reserved word. Name must start with a letter and contain only letters, numbers, and underscores. Hint: use FROM_."
            in result["error"]
        )
        self.assertEqual(
            result["documentation"], "https://docs.tinybird.co/api-reference/api-reference.html#forbidden-names"
        )

    @tornado.testing.gen_test
    async def test_pipe_create_with_node_validate_forbidden_name(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        data = json.dumps({"name": "pipe_validate_forbidden_name", "nodes": [{"name": "FROM", "sql": "select 1"}]})
        response = await self.fetch_async(
            f"/v0/pipes?token={token}", headers={"Content-type": "application/json"}, method="POST", body=data
        )
        self.assertEqual(response.code, 400)
        result = json.loads(response.body)
        self.assertTrue(
            "FROM is a reserved word. Name must start with a letter and contain only letters, numbers, and underscores. Hint: use FROM_."
            in result["error"]
        )
        self.assertEqual(
            result["documentation"], "https://docs.tinybird.co/api-reference/api-reference.html#forbidden-names"
        )

    @tornado.testing.gen_test
    async def test_pipe_append_node_validate_forbidden_name(self):
        pipe_name = "pipe_append_node_validate_forbidden_name"
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        data = json.dumps({"name": pipe_name, "nodes": [{"name": "test", "sql": "select 1"}]})
        response = await self.fetch_async(
            f"/v0/pipes?token={token}", headers={"Content-type": "application/json"}, method="POST", body=data
        )
        self.assertEqual(response.code, 200)

        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes?token={token}&name=FROM",
            headers={"Content-type": "application/json"},
            method="POST",
            body="select 1",
        )
        self.assertEqual(response.code, 400)

        result = json.loads(response.body)
        self.assertTrue(
            "FROM is a reserved word. Name must start with a letter and contain only letters, numbers, and underscores. Hint: use FROM_."
            in result["error"]
        )
        self.assertEqual(
            result["documentation"], "https://docs.tinybird.co/api-reference/api-reference.html#forbidden-names"
        )

    @tornado.testing.gen_test
    async def test_pipe_append_node_allows_alias_matching_other_resource(self):
        pipe_name = "pipe_append_node_allows_alias_matching_other_resource"
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        data = json.dumps({"name": pipe_name, "nodes": [{"name": "test", "sql": "select 1"}]})
        response = await self.fetch_async(
            f"/v0/pipes?token={token}", headers={"Content-type": "application/json"}, method="POST", body=data
        )
        self.assertEqual(response.code, 200)

        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes?token={token}&name=test_1",
            headers={"Content-type": "application/json"},
            method="POST",
            body=f"select 1 as {pipe_name}",
        )
        self.assertEqual(response.code, 200)

    @tornado.testing.gen_test
    async def test_pipe_append_node_validate_forbidden_alias_different_pipe(self):
        pipe_name = "pipe_append_node_validate_forbidden_alias"
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        data = json.dumps({"name": pipe_name, "nodes": [{"name": "test", "sql": "select 1"}]})
        response = await self.fetch_async(
            f"/v0/pipes?token={token}", headers={"Content-type": "application/json"}, method="POST", body=data
        )
        self.assertEqual(response.code, 200)

        data = json.dumps({"name": f"{pipe_name}_2", "nodes": [{"name": "test2", "sql": "select 1"}]})
        response = await self.fetch_async(
            f"/v0/pipes?token={token}", headers={"Content-type": "application/json"}, method="POST", body=data
        )
        self.assertEqual(response.code, 200)

        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes?token={token}&name=test_2",
            headers={"Content-type": "application/json"},
            method="POST",
            body="select 1 as test2",
        )
        self.assertEqual(response.code, 200)

    @tornado.testing.gen_test
    async def test_pipe_update_node_validate_forbidden_name(self):
        pipe_name = "pipe_append_node_validate_forbidden_name"
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        data = json.dumps({"name": pipe_name, "nodes": [{"name": "test", "sql": "select 1"}]})
        response = await self.fetch_async(
            f"/v0/pipes?token={token}", headers={"Content-type": "application/json"}, method="POST", body=data
        )
        self.assertEqual(response.code, 200)

        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes?token={token}&name=anode",
            headers={"Content-type": "application/json"},
            method="POST",
            body="select 1",
        )
        self.assertEqual(response.code, 200)

        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/anode?token={token}&name=FROM",
            headers={"Content-type": "application/json"},
            method="PUT",
            body="",
        )
        self.assertEqual(response.code, 400)

        result = json.loads(response.body)
        self.assertTrue(
            "FROM is a reserved word. Name must start with a letter and contain only letters, numbers, and underscores. Hint: use FROM_."
            in result["error"]
        )
        self.assertEqual(
            result["documentation"], "https://docs.tinybird.co/api-reference/api-reference.html#forbidden-names"
        )

    @tornado.testing.gen_test
    async def test_append_node(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        response = await self.fetch_async(
            f"/v0/pipes/test_pipe/nodes?token={token}&name=pipe_append_node",
            method="POST",
            body="select count() c from test_table where a > 4",
        )
        self.assertEqual(response.code, 200)
        pipe_node = json.loads(response.body)
        self.assertEqual(pipe_node["name"], "pipe_append_node")
        self.assertEqual(pipe_node["sql"], "select count() c from test_table where a > 4")

        payload = await self._get_pipe_data("json", 404, token_name="test_append_node_2")
        payload = json.loads(payload)
        self.assertEqual(payload["error"], "The pipe 'test_pipe' does not have an endpoint yet")

        await self._make_endpoint(pipe_node["id"], token_name="test_append_node_3")
        payload = await self._get_pipe_data("json", token_name="test_append_node_4")
        payload = json.loads(payload)
        self.assertEqual(payload["data"][0]["c"], 1)

    def test_append_node_wrong_sql(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        response = self.fetch(
            f"/v0/pipes/test_pipe/nodes?token={token}&name=pipe_append_node&ignore_sql_errors=true",
            method="POST",
            body="invalid sql",
        )
        self.assertEqual(response.code, 200)
        pipe_node = json.loads(response.body)
        self.assertEqual(pipe_node["name"], "pipe_append_node")
        self.assertEqual(pipe_node["sql"], "invalid sql")
        self.assertEqual(pipe_node["ignore_sql_errors"], True)

    def test_append_fails_with_wrong_sql(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        response = self.fetch(
            f"/v0/pipes/test_pipe/nodes?token={token}&name=pipe_append_node&ignore_sql_errors=false",
            method="POST",
            body="SELECT toUInt32('asd') FROM test_table",
        )
        result = json.loads(response.body)
        self.assertEqual(response.code, 400)
        self.assertTrue(
            "[Error] Cannot parse string 'asd' as UInt32: syntax error at begin of string" in result["error"]
        )

    def test_append_succeeds_with_complex_and_slow_sql(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        query = """
            SELECT a from
                (SELECT max(number) a from numbers(10000000000)) _a,
                (SELECT max(number) b from numbers(5000000000)) _b
            WHERE a = b
            """
        response = self.fetch(
            f"/v0/pipes/test_pipe/nodes?token={token}&name=pipe_append_node&ignore_sql_errors=false",
            method="POST",
            body=query,
        )
        self.assertEqual(response.code, 200)
        pipe_node = json.loads(response.body)
        self.assertEqual(pipe_node["name"], "pipe_append_node")
        self.assertEqual(pipe_node["sql"], query)

    def test_template_wrong_template(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        template = """%
        SELECT count() c FROM test_table
            where a > {{Float32(myvar)}}
            {% if defined(my_condition) %}
                and c = {{Int32(my_condition)}}
            {% endif %}
        """
        response = self.fetch(
            f"/v0/pipes/test_pipe/nodes?token={token}&name=pipe_append_node", method="POST", body=template
        )
        self.assertEqual(response.code, 400)

    @tornado.testing.gen_test
    async def test_template_syntax_error(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_template_syntax_error"
        node_0_name = f"node_0_{pipe_name}"
        node_1_name = f"node_1_{pipe_name}"

        params = {"token": token}

        data = {
            "name": pipe_name,
            "nodes": [
                {"name": node_0_name, "sql": "% SELECT 1 {% if defined((passenger_count) %} WHERE 1=1 {% end %}"},
                {"name": node_1_name, "sql": f"SELECT * FROM {node_0_name}"},
            ],
        }

        response = await self.fetch_async(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )
        result = json.loads(response.body)

        self.assertEqual(response.code, 400)
        self.assertEqual(
            result.get("error"),
            f"Syntax error: invalid syntax, line 1 (in node '{node_0_name}' from pipe '{pipe_name}')",
        )

    @tornado.testing.gen_test
    async def test_template_parse_error(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_template_parse_error"
        node_0_name = f"node_0_{pipe_name}"
        node_1_name = f"node_1_{pipe_name}"

        params = {"token": token}

        data = {
            "name": pipe_name,
            "nodes": [
                {"name": node_0_name, "sql": "% SELECT * FROM {% import os %}{{ os.popen('ls').read() }}"},
                {"name": node_1_name, "sql": f"SELECT * FROM {node_0_name}"},
            ],
        }

        response = await self.fetch_async(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )

        result = json.loads(response.body)
        self.assertEqual(response.code, 400)

        self.assertEqual(
            result.get("error"),
            f"Syntax error: import is forbidden at line 1 (in node '{node_0_name}' from pipe '{pipe_name}')",
        )

    @tornado.testing.gen_test
    async def test_template_unclosedif_error(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_template_unclosedif_error_pipe"
        node_0_name = f"node_0_{pipe_name}"
        node_1_name = f"node_1_{pipe_name}"

        params = {"token": token}

        data = {
            "name": pipe_name,
            "nodes": [
                {"name": node_0_name, "sql": "% SELECT {% if defined(x) %} x, 1"},
                {"name": node_1_name, "sql": f"SELECT * FROM {node_0_name}"},
            ],
        }

        response = await self.fetch_async(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )

        result = json.loads(response.body)

        self.assertEqual(response.code, 400)
        self.assertTrue("Syntax error: Missing {% end %} block for if at line 1" in result.get("error"))
        self.assertTrue(f"(in node '{node_0_name}' from pipe '{pipe_name}')" in result.get("error"))

    @tornado.testing.gen_test
    async def test_template_params(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        template = """%
        SELECT count() count FROM test_table
            where b > {{Float32(myvar)}}
            {% if defined(my_condition) %}
                and a = {{Int32(my_condition)}}
            {% end %}
        """

        response = await self.fetch_async(
            f"/v0/pipes/test_pipe/nodes?token={token}&name=pipe_append_node", method="POST", body=template
        )
        self.assertEqual(response.code, 200)
        pipe_node = json.loads(response.body)
        await self._make_endpoint(pipe_node["id"])
        payload = await self._get_pipe_data("csv", params={"myvar": 1.5}, token_name="test_pipe_data_1")
        self.assertEqual(payload, b'"count"\n4\n')
        payload = await self._get_pipe_data(
            "csv", params={"myvar": 1.5, "my_condition": 3}, token_name="test_pipe_data_2"
        )
        self.assertEqual(payload, b'"count"\n1\n')
        await self._get_pipe_data("csv", 400, token_name="test_pipe_data_3")

    @tornado.testing.gen_test
    async def test_template_params_with_quoted_string(self):
        tb_api_proxy_async = TBApiProxyAsync(self)

        workspace = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(workspace, "test_template_params_with_quoted_string", scopes.ADMIN)

        datasource_name = "datasource_with_quoted_data_in_columns"
        datasource_response = await tb_api_proxy_async.create_datasource(
            token=token, ds_name=datasource_name, schema="a Int32,text String"
        )

        await self._insert_data_in_datasource(token=token, ds_name=datasource_name, data='1,{"action": "test run"}')

        response = await self.fetch_async(
            f"/v0/pipes/test_pipe/nodes?token={token}&name=pipe_node_params",
            method="POST",
            body=f"""%
            SELECT * FROM {datasource_name} WHERE text={{{{String(text, 'action."test run"')}}}}
            """,
        )

        self.assertEqual(response.code, 200)

        pipe_node = json.loads(response.body)
        await self._make_endpoint(pipe_node["id"])

        self.wait_for_datasource_replication(workspace, datasource_response.get("datasource"))

        response = await self._get_pipe_data("json", params={"text": '{"action": "test run"}'}, token=token)
        parsed_body = json.loads(response)

        self.assertEqual(parsed_body["data"], [{"a": 1, "text": '{"action": "test run"}'}])

    @tornado.testing.gen_test
    async def test_template_datediff_exception(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        template = """%
        SELECT count() count FROM test_table
            {% if day_diff(date_end, date_start) < 7 %}
                where 1
            {% end %}
        """

        response = await self.fetch_async(
            f"/v0/pipes/test_pipe/nodes?token={token}&name=pipe_append_node", method="POST", body=template
        )
        self.assertEqual(response.code, 200)
        pipe_node = json.loads(response.body)
        await self._make_endpoint(pipe_node["id"])
        payload = await self._get_pipe_data("csv", 400, token_name="test_pipe_data_1")
        assert (
            json.loads(payload)["error"]
            == "Template Syntax Error: invalid date format in function `day_diff`, it must be ISO format date YYYY-MM-DD, e.g. 2018-09-26. For other fotmats, try `date_diff_in_days`"
        )

    @tornado.testing.gen_test
    async def test_template_params_can_access_user_resources(self):
        from ..utils import fixture_file

        u = User.get_by_name(self.WORKSPACE)
        token_admin = Users.get_token_for_scope(u, scopes.ADMIN)

        name = "should_reach_this_ds"
        params = {
            "token": token_admin,
            "name": name,
        }
        create_url = self.get_url(f"/v0/datasources?{urlencode(params)}")
        with fixture_file("sales_0.csv", mode="rb") as fd:
            response = await self.fetch_full_body_upload_async(create_url, fd)
        self.assertEqual(response.code, 200, response.body)

        ds = Users.get_datasource(u, "test_table")
        test_pipe = Users.get_pipe(u, "test_pipe")
        token = Users.add_token(u, "test_read_templates", scopes.DATASOURCES_READ, ds.id)
        token = Users.add_scope_to_token(u, token, scopes.PIPES_READ, test_pipe.id)
        template = """%
            SELECT * FROM
            {% if defined(test_param) %}
                should_reach_this_ds
            {% else %}
                test_table
            {% end %}
        """

        response = await self.fetch_async(
            f"/v0/pipes/test_pipe/nodes?token={token_admin}&name=pipe_append_other_db", method="POST", body=template
        )
        self.assertEqual(response.code, 200)
        pipe_node = json.loads(response.body)
        await self._make_endpoint(pipe_node["id"])

        await self._get_pipe_data("csv", expected_code=200, params={}, token=token)
        await self._get_pipe_data("json", expected_code=200, params={"test_param": 1}, token=token)

    def test_template_query_without_params(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        template = """%
        SELECT * FROM test_table LIMIT 1
        """

        response = self.fetch(
            f"/v0/pipes/test_pipe/nodes?token={token}&name=pipe_append_node", method="POST", body=template
        )
        self.assertEqual(response.code, 200)
        pipe_node = json.loads(response.body)
        self.assertEqual(pipe_node["params"], [])

    def test_pipe_list_with_wrong_sql_node_validate_sql(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        query = """%
            select * from test_table
            {% if defined(whatever) %}
            where 2
            {% else %}
        """

        params = {"token": token, "name": "pipe_append_wrong_sql"}
        response = self.fetch(f"/v0/pipes/test_pipe/nodes?{urlencode(params)}", method="POST", body=query)
        self.assertEqual(response.code, 400, response.body)
        result = json.loads(response.body)
        self.assertEqual(result["error"], "Syntax error: Missing {% end %} block for if at line 5")

        response = self.fetch(f"/v0/pipes?token={token}")
        parsed = json.loads(response.body)
        test_pipe = next((x for x in parsed["pipes"] if x["name"] == "test_pipe"), None)
        self.assertIsNotNone(test_pipe)
        self.assertEqual(len(test_pipe["nodes"]), 1)
        self.assertEqual(test_pipe["nodes"][0]["name"], "test_pipe_0")

    def test_pipe_list_with_wrong_sql_node_ignore_sql_errors(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        query = """%
            select * from test_table
            {% if defined(whatever) %}
            where 2
            {% else %}
        """

        params = {"token": token, "name": "pipe_append_wrong_sql_ignored", "ignore_sql_errors": "true"}
        response = self.fetch(f"/v0/pipes/test_pipe/nodes?{urlencode(params)}", method="POST", body=query)
        self.assertEqual(response.code, 200, response.body)
        pipe_node = json.loads(response.body)
        self.assertEqual(pipe_node["name"], "pipe_append_wrong_sql_ignored")
        self.assertEqual(pipe_node["sql"], query)
        self.assertEqual(pipe_node["ignore_sql_errors"], True)

        response = self.fetch(f"/v0/pipes?token={token}")
        parsed = json.loads(response.body)
        test_pipe = next((x for x in parsed["pipes"] if x["name"] == "test_pipe"), None)
        self.assertIsNotNone(test_pipe)
        self.assertEqual(len(test_pipe["nodes"]), 2)
        self.assertEqual(test_pipe["nodes"][0]["name"], "test_pipe_0")
        self.assertEqual(test_pipe["nodes"][1]["name"], "pipe_append_wrong_sql_ignored")
        self.assertTrue(test_pipe["nodes"][1]["ignore_sql_errors"])

    def test_query_params_affect_all_pipes(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
        }

        data = {
            "name": "pipe_name",
            "nodes": [
                {
                    "sql": """%
                        SELECT * FROM test_table WHERE a = {{Int32(x)}}
                    """,
                    "name": "node_00",
                }
            ],
        }

        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        node_id = json.loads(response.body)["nodes"][0]["id"]
        response = self.fetch(
            f"/v0/pipes/pipe_name/nodes/{node_id}/endpoint?{urlencode(params)}",
            method="POST",
            headers={"Content-type": "application/json"},
            body=b"",
        )
        self.assertEqual(response.code, 200, response.body)

        data = {
            "name": "pipe_name_1",
            "description": "my first pipe",
            "nodes": [
                {
                    "sql": """%
                        SELECT * FROM pipe_name
                    """,
                    "name": "node_00",
                }
            ],
        }
        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        node_id = json.loads(response.body)["nodes"][0]["id"]
        response = self.fetch(
            f"/v0/pipes/pipe_name_1/nodes/{node_id}/endpoint?{urlencode(params)}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        response = self.fetch(f"/v0/pipes/pipe_name_1.json?x=1&{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        self.assertEqual(result["data"][0]["a"], 1, response.body)

    def test_calls_to_pipe_are_being_filter_by_the_token(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
        }

        data = {
            "name": "pipe_name_1",
            "description": "my first pipe",
            "nodes": [
                {
                    "sql": """%
                        SELECT *
                        FROM (
                            SELECT 1 as x
                            UNION ALL
                            SELECT 2 as x
                        )
                        WHERE 1
                        {% if defined(y) %}
                            AND x = {{Int32(y)}}
                        {% end %}
                    """,
                    "name": "node_00",
                }
            ],
        }
        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )

        self.assertEqual(response.code, 200, response.body)

        node_id = json.loads(response.body)["nodes"][0]["id"]
        response = self.fetch(
            f"/v0/pipes/pipe_name_1/nodes/{node_id}/endpoint?{urlencode(params)}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        response = self.fetch(
            "/v0/tokens?token=%s&name=filtered_token&scope=PIPES:READ:pipe_name_1:x+=+1" % token, method="POST", body=""
        )
        res = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(res["token"] != "", True)
        self.assertEqual(res["name"], "filtered_token")
        self.assertEqual(res["scopes"], [{"type": "PIPES:READ", "resource": "pipe_name_1", "filter": "x = 1"}])

        response = self.fetch(
            f"/v0/pipes/pipe_name_1.json?token={res['token']}",
            method="GET",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200)
        res = json.loads(response.body)
        self.assertEqual(len(res["data"]), 1, res["data"])

    def test_query_params_using_multiple_pipes_with_same_name_and_different_types_will_fail(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
        }

        data = {
            "name": "pipe_name",
            "nodes": [
                {
                    "sql": """%
                        SELECT * FROM test_table WHERE c = {{String(x)}}
                    """,
                    "name": "node_00",
                }
            ],
        }

        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        node_id = json.loads(response.body)["nodes"][0]["id"]
        response = self.fetch(
            f"/v0/pipes/pipe_name/nodes/{node_id}/endpoint?{urlencode(params)}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        response = self.fetch(f"/v0/pipes/pipe_name.json?x=one&{urlencode(params)}")
        self.assertEqual(response.code, 200, response)
        result = json.loads(response.body)
        self.assertEqual(result["data"][0]["a"], 1, response)

        data = {
            "name": "pipe_name_1",
            "nodes": [
                {
                    "sql": """%
                        SELECT * FROM test_table WHERE a = {{Int32(x)}}
                    """,
                    "name": "node_00",
                }
            ],
        }
        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        node_id = json.loads(response.body)["nodes"][0]["id"]
        response = self.fetch(
            f"/v0/pipes/pipe_name_1/nodes/{node_id}/endpoint?{urlencode(params)}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        response = self.fetch(f"/v0/pipes/pipe_name_1.json?x=one&{urlencode(params)}")
        self.assertEqual(response.code, 400, response)
        result = json.loads(response.body)
        self.assertEqual(result["error"], """Template Syntax Error: Error validating 'one' to type Int32""", response)

    def test_same_query_params_used_in_two_pipes(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
        }

        data = {
            "name": "pipe_name",
            "nodes": [
                {
                    "sql": """%
                        SELECT * FROM test_table WHERE a = {{Int32(x)}}
                    """,
                    "name": "node_00",
                }
            ],
        }

        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        node_id = json.loads(response.body)["nodes"][0]["id"]
        response = self.fetch(
            f"/v0/pipes/pipe_name/nodes/{node_id}/endpoint?{urlencode(params)}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        data = {
            "name": "pipe_name_1",
            "description": "my first pipe",
            "nodes": [
                {
                    "sql": """%
                        SELECT * FROM pipe_name WHERE a = {{Int32(x)}}
                    """,
                    "name": "node_00",
                }
            ],
        }
        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        node_id = json.loads(response.body)["nodes"][0]["id"]
        response = self.fetch(
            f"/v0/pipes/pipe_name_1/nodes/{node_id}/endpoint?{urlencode(params)}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        response = self.fetch(f"/v0/pipes/pipe_name_1.json?x=1&{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        self.assertEqual(result["data"][0]["a"], 1, response.body)

    def test_required_params_in_child_pipe_throws_exception_if_not_pass(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
        }

        data = {
            "name": "pipe_name",
            "nodes": [
                {
                    "sql": """%
                        SELECT * FROM test_table WHERE a = {{Int32(x, required=True)}}
                    """,
                    "name": "node_00",
                }
            ],
        }

        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        node_id = json.loads(response.body)["nodes"][0]["id"]
        response = self.fetch(
            f"/v0/pipes/pipe_name/nodes/{node_id}/endpoint?{urlencode(params)}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        data = {
            "name": "pipe_name_1",
            "description": "my first pipe",
            "nodes": [
                {
                    "sql": """%
                        SELECT * FROM pipe_name
                    """,
                    "name": "node_00",
                }
            ],
        }
        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        node_id = json.loads(response.body)["nodes"][0]["id"]
        response = self.fetch(
            f"/v0/pipes/pipe_name_1/nodes/{node_id}/endpoint?{urlencode(params)}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        response = self.fetch(f"/v0/pipes/pipe_name_1.json?{urlencode(params)}")
        self.assertEqual(response.code, 400, response.body)
        result = json.loads(response.body)
        self.assertIn("Template Syntax Error: Required parameter is not defined", result["error"])

    def test_child_query_params_listed_in_parent_pipe(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
        }

        data = {
            "name": "pipe_name",
            "nodes": [
                {
                    "sql": """%
                        SELECT * FROM test_table WHERE a = {{Int32(x, required=True)}}
                    """,
                    "name": "node_00",
                }
            ],
        }

        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        node_id = json.loads(response.body)["nodes"][0]["id"]
        response = self.fetch(
            f"/v0/pipes/pipe_name/nodes/{node_id}/endpoint?{urlencode(params)}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        data = {
            "name": "pipe_name_1",
            "description": "my first pipe",
            "nodes": [
                {
                    "sql": """%
                        SELECT * FROM pipe_name
                    """,
                    "name": "node_00",
                }
            ],
        }
        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        node_id = json.loads(response.body)["nodes"][0]["id"]
        response = self.fetch(
            f"/v0/pipes/pipe_name_1/nodes/{node_id}/endpoint?{urlencode(params)}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        response = self.fetch(
            f"/v0/pipes/pipe_name_1?{urlencode(params)}", method="GET", headers={"Content-type": "application/json"}
        )
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(len(json.loads(response.body)["nodes"][0]["params"]) > 0, False, response.body)

    def test_custom_child_error_being_catch_by_parent_pipe(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
        }

        data = {
            "name": "pipe_name",
            "nodes": [
                {
                    "sql": """%
                        {% if not defined(x) %}
                            {{ error('x (Int32) query param is required') }}
                        {% end %}
                        SELECT * FROM test_table WHERE a = {{Int32(x)}}
                    """,
                    "name": "node_00",
                }
            ],
        }

        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        node_id = json.loads(response.body)["nodes"][0]["id"]
        response = self.fetch(
            f"/v0/pipes/pipe_name/nodes/{node_id}/endpoint?{urlencode(params)}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        data = {
            "name": "pipe_name_1",
            "description": "my first pipe",
            "nodes": [
                {
                    "sql": """%
                        SELECT * FROM pipe_name
                    """,
                    "name": "node_00",
                }
            ],
        }
        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        node_id = json.loads(response.body)["nodes"][0]["id"]
        response = self.fetch(
            f"/v0/pipes/pipe_name_1/nodes/{node_id}/endpoint?{urlencode(params)}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        response = self.fetch(f"/v0/pipes/pipe_name_1.json?{urlencode(params)}")
        self.assertEqual(response.code, 400, response.body)
        result = json.loads(response.body)
        self.assertEqual(result["error"], "x (Int32) query param is required", response.body)

    def test_parent_defined_value_used_in_child_pipe(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
        }

        data = {
            "name": "pipe_name",
            "nodes": [
                {
                    "sql": """%
                        SELECT * FROM test_table WHERE a = {{Int32(x)}}
                    """,
                    "name": "node_00",
                }
            ],
        }

        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        node_id = json.loads(response.body)["nodes"][0]["id"]
        response = self.fetch(
            f"/v0/pipes/pipe_name/nodes/{node_id}/endpoint?{urlencode(params)}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        data = {
            "name": "pipe_name_1",
            "description": "my first pipe",
            "nodes": [
                {
                    "sql": """%
                        {% set x = 1 %}
                        SELECT * FROM pipe_name
                    """,
                    "name": "node_00",
                }
            ],
        }
        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        node_id = json.loads(response.body)["nodes"][0]["id"]
        response = self.fetch(
            f"/v0/pipes/pipe_name_1/nodes/{node_id}/endpoint?{urlencode(params)}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        response = self.fetch(f"/v0/pipes/pipe_name_1.json?x=1&{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        self.assertEqual(result["data"][0]["a"], 1, response.body)
        self.assertEqual(len(result["data"]), 1, response.body)

    def test_pipe_creation_given_negative_params(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
        }

        data = {
            "name": "pipe_name_with_params",
            "nodes": [
                {
                    "sql": """%
                        SELECT * FROM test_table WHERE a = {{Float64(x, -2.0)}}
                    """,
                    "name": "node_00",
                }
            ],
        }

        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        payload = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(payload["nodes"][0]["params"][0]["name"], "x")
        self.assertEqual(payload["nodes"][0]["params"][0]["default"], -2.0)

    def test_pipe_creation_given_zero_as_params(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
        }

        data = {
            "name": "pipe_name_with_params",
            "nodes": [
                {
                    "sql": """%
                        SELECT * FROM test_table WHERE a = {{Float64(x, 0)}}
                    """,
                    "name": "node_00",
                }
            ],
        }

        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        payload = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(payload["nodes"][0]["params"][0]["name"], "x")
        self.assertEqual(payload["nodes"][0]["params"][0]["default"], 0)

    def test_pipe_creation_given_positive_params(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
        }

        data = {
            "name": "pipe_name_with_params",
            "nodes": [
                {
                    "sql": """%
                        SELECT * FROM test_table WHERE a = {{Float64(x, 2.0)}}
                    """,
                    "name": "node_00",
                }
            ],
        }

        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        payload = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(payload["nodes"][0]["params"][0]["name"], "x")
        self.assertEqual(payload["nodes"][0]["params"][0]["default"], 2.0)

    @tornado.testing.gen_test
    async def test_post_pipe_with_endpoint_overwrite(self):
        pipe_name = "test_pipe"
        base_name = "test_post_pipe_with_endpoint_overwrite"
        workspace = Users.get_by_id(self.WORKSPACE_ID)
        await self._make_endpoint()
        admin_token = Users.add_token(workspace, f"{base_name}_admin", scopes.ADMIN, self.USER_ID)
        await self._get_pipe_data("json", expected_code=200, token=admin_token)

        workspace = Users.get_by_id(self.WORKSPACE_ID)
        params = {"token": admin_token, "force": "true"}
        body = {
            "name": pipe_name,
            "description": "this is a test",
            "nodes": [{"sql": "select 1 as a", "name": self.endpoint_node.name}],
        }
        response = await self.fetch_async(
            f"/v0/pipes?{urlencode(params)}",
            headers={"Content-Type": "application/json"},
            method="POST",
            body=json.dumps(body),
        )
        self.assertEqual(response.code, 200)
        payload = json.loads(response.body)
        returned_endpoint_name = [node["name"] for node in payload["nodes"] if node["id"] == payload["endpoint"]][0]
        self.assertEqual(returned_endpoint_name, self.endpoint_node.name)
        self.assertEqual(payload["description"], "this is a test")
        await self._get_pipe_data("json", expected_code=200, token=admin_token)

    @tornado.testing.gen_test
    async def test_post_pipe_with_endpoint_then_override_to_set_another_node_as_endpoint(self):
        test_name = "test_post_pipe_with_endpoint_then_override_to_set_another_node_as_endpoint"
        pipe_name = f"pipe_{test_name}"
        workspace = Users.get_by_id(self.WORKSPACE_ID)
        admin_token = Users.add_token(workspace, f"{test_name}_admin", scopes.ADMIN, self.USER_ID)
        nodes = [
            {"sql": "select 1 as a", "name": f"{pipe_name}_0"},
            {"sql": "select * from numbers(100)", "name": f"{pipe_name}_1", "type": "endpoint"},
        ]

        params = {
            "token": admin_token,
        }
        body = {
            "name": pipe_name,
            "description": "this is a test",
            "nodes": nodes,
        }
        response = await self.fetch_async(
            f"/v0/pipes?{urlencode(params)}",
            headers={"Content-Type": "application/json"},
            method="POST",
            body=json.dumps(body),
        )
        self.assertEqual(response.code, 200)
        payload = json.loads(response.body)
        self.assertEqual(payload.get("type"), PipeTypes.ENDPOINT)
        self.assertEqual(payload.get("nodes")[0].get("node_type"), PipeNodeTypes.STANDARD)
        self.assertEqual(payload.get("nodes")[1].get("node_type"), PipeNodeTypes.ENDPOINT)

        nodes = [
            {"sql": "select 1 as a", "name": f"{pipe_name}_0", "type": "endpoint"},
            {"sql": "select * from numbers(100)", "name": f"{pipe_name}_1"},
        ]

        params = {"token": admin_token, "force": "true"}
        body = {
            "name": pipe_name,
            "description": "this is a test",
            "nodes": nodes,
        }
        response = await self.fetch_async(
            f"/v0/pipes?{urlencode(params)}",
            headers={"Content-Type": "application/json"},
            method="POST",
            body=json.dumps(body),
        )
        self.assertEqual(response.code, 200)
        payload = json.loads(response.body)
        self.assertEqual(payload.get("type"), PipeTypes.ENDPOINT)
        self.assertEqual(payload.get("nodes")[0].get("node_type"), PipeNodeTypes.ENDPOINT)
        self.assertEqual(payload.get("nodes")[1].get("node_type"), PipeNodeTypes.STANDARD)

    @mock.patch("tinybird.limits.Limits.rate_limit", return_value=[1, 1000, 0, 3600, 3600])
    @tornado.testing.gen_test
    async def test_build_plan_pipe_data_with_endpoint_check_limit(self, mock_rate_limit: AsyncMock):
        u = Users.get_by_id(self.WORKSPACE_ID)
        u.plan = BillingPlans.DEV
        u.save()
        await self._make_endpoint()
        response = await self._get_pipe_data("json", expected_code=429)
        mock_rate_limit.assert_awaited_once()
        args, _ = mock_rate_limit.call_args
        rate_limit = args[0]
        assert rate_limit.key == f'{self.WORKSPACE_ID}:build_plan_api_requests_{datetime.now().strftime("%Y%m%d")}'
        assert f"Too many requests: {u.name} quota exceeded. Learn more " in json.loads(response)["error"]
        assert f"/{u.id}/settings" in json.loads(response)["error"]
        assert json.loads(response)["documentation"] is not None

    @mock.patch("tinybird.limits.Limits.rate_limit", return_value=[1, 1000, 0, 3600, 3600])
    @tornado.testing.gen_test
    async def test_pipe_data_with_endpoint_with_no_explicit_workspace_request_check_limit(
        self, mock_rate_limit: AsyncMock
    ):
        u = Users.get_by_id(self.WORKSPACE_ID)
        u.plan = BillingPlans.CUSTOM
        u.save()
        await self._make_endpoint()
        await self._get_pipe_data("json", expected_code=200)
        mock_rate_limit.assert_not_awaited()

    @mock.patch("tinybird.limits.Limits.rate_limit", return_value=[1, 1000, 0, 3600, 3600])
    @tornado.testing.gen_test
    async def test_pipe_data_with_endpoint_with_explicit_workspace_request_check_limit(
        self, mock_rate_limit: AsyncMock
    ):
        u = Users.get_by_id(self.WORKSPACE_ID)
        u.plan = BillingPlans.CUSTOM
        u.limits = {"workspace_api_requests": ("rl", 1, 1000, 0, 1)}
        u.save()
        await self._make_endpoint()
        await self._get_pipe_data("json", expected_code=429)
        mock_rate_limit.assert_awaited_once()

    @tornado.testing.gen_test
    @patch("tinybird.monitor.statsd_client.incr")
    async def test_endpoint_max_rps_limit(self, mock_incr: Mock):
        u = Users.get_by_id(self.WORKSPACE_ID)
        u.plan = BillingPlans.CUSTOM
        u.save()

        with User.transaction(self.WORKSPACE_ID) as w:
            w.feature_flags[FeatureFlagWorkspaces.DISTRIBUTED_ENDPOINT_CONCURRENCY.value] = True

        await self._make_endpoint()
        token = Users.add_token(u, "test_2", scopes.ADMIN)

        # Limit RPS in endpoint
        TINYBIRD_WORKSPACE = f"test_tinybird{uuid.uuid4().hex}"
        TINYBIRD_USER = f"{TINYBIRD_WORKSPACE}@tinybird.co"
        tinybird_user_account = UserAccount.register(TINYBIRD_USER, "pass")
        tinybird_user_account_token = UserAccount.get_token_for_scope(tinybird_user_account, scopes.AUTH)
        self.users_to_delete.append(tinybird_user_account)

        params = {
            "operation": "change_endpoint_limit",
            "limit_name": EndpointLimits.get_limit_key("test_pipe", EndpointLimits.max_rps),
            "limit_value": 1,
            "limit_setting": EndpointLimits.max_rps.name,
            "endpoint_name": "test_pipe",
        }
        headers = {"Authorization": f"Bearer {tinybird_user_account_token}"}
        r = await self.fetch_async(
            f"/cheriff/workspace/{u.id}?{urlencode(params)}", method="POST", body="", headers=headers
        )
        self.assertEqual(r.code, 200, r.body)

        result = await asyncio.gather(
            *[self.fetch_async(f"/v0/pipes/test_pipe.json?token={token}&i={i}", method="GET") for i in range(10)]
        )
        self.assertTrue(all(r for r in result if r.code == 200))
        self.assertTrue(any(r for r in result if r.code == 429))
        endpoint_limit = EndpointLimits.get_limit_key("test_pipe", EndpointLimits.max_rps)
        self.assertFalse(
            any(
                f"tinybird.{statsd_client.region_machine}.rate_limit.{self.base_workspace.id}.{endpoint_limit}"
                in call.args
                for call in mock_incr.call_args_list
            ),
            mock_incr.call_args_list,
        )

        # Let's increase the limit to make sure we do not rate limit
        params = {
            "operation": "change_endpoint_limit",
            "limit_name": EndpointLimits.get_limit_key("test_pipe", EndpointLimits.max_rps),
            "limit_value": 100,
            "limit_setting": EndpointLimits.max_concurrent_queries.name,
            "endpoint_name": "test_pipe",
        }
        headers = {"Authorization": f"Bearer {tinybird_user_account_token}"}
        r = await self.fetch_async(
            f"/cheriff/workspace/{u.id}?{urlencode(params)}", method="POST", body="", headers=headers
        )
        self.assertEqual(r.code, 200, r.body)

        # Even through we set a limit of 100. We are just tracking the dry_run
        result = await asyncio.gather(
            *[self.fetch_async(f"/v0/pipes/test_pipe.json?token={token}&i={i}", method="GET") for i in range(10)]
        )
        self.assertTrue(all(r for r in result if r.code == 200))
        endpoint_limit = EndpointLimits.get_limit_key("test_pipe", EndpointLimits.max_rps)
        self.assertFalse(
            any(
                f"tinybird.{statsd_client.region_machine}.rate_limit.{self.base_workspace.id}.{endpoint_limit}"
                in call.args
                for call in mock_incr.call_args_list
            ),
            mock_incr.call_args_list,
        )

    @tornado.testing.gen_test
    async def test_organization_qps_limit(self):
        """Test that organization QPS limits are enforced on endpoints"""
        self.tb_api = TBApiProxyAsync(self)
        await self.enable_shared_infra_billing_ff(self.user_account)

        @retry_transaction_in_case_of_concurrent_edition_error_async()
        async def enable_org_qps_limit(workspace: User) -> None:
            with User.transaction(workspace.id) as w:
                w.feature_flags[FeatureFlagWorkspaces.ORG_RATE_LIMIT.value] = True

        await enable_org_qps_limit(self.base_workspace)

        # Create organization with QPS limit using helper method
        org_name = f"org_{uuid.uuid4().hex}"
        organization = await self.tb_api.create_organization(
            org_name, self.user_token, workspace_ids=[self.WORKSPACE_ID]
        )
        organization = Organizations.update_commitment_information(
            organization,
            commitment_billing=OrganizationCommitmentsPlans.SHARED_INFRASTRUCTURE_USAGE,
            commitment_max_qps=2,  # Set low QPS limit for testing
        )

        # Validate workspace has organization_id set
        workspace = Users.get_by_id(self.WORKSPACE_ID)
        self.assertIsNotNone(workspace.organization_id, "Workspace should have organization_id set")
        self.assertEqual(workspace.organization_id, organization.id)

        # Create pipe with endpoint node
        pipe_name = "test_pipe"
        await self._make_endpoint()
        # Run 10 concurrent requests
        results = await asyncio.gather(
            *[self.fetch_async(f"/v0/pipes/{pipe_name}.json?token={self.admin_token}&i={i}") for i in range(10)]
        )

        # Validate that at least one request got a 429 error
        has_429 = any(r.code == 429 for r in results)
        self.assertTrue(has_429, "Expected at least one request to get a 429 error")

        # Validate that at least one request succeeded with 200
        has_200 = any(r.code == 200 for r in results)
        self.assertTrue(has_200, "Expected at least one request to succeed with 200")
        error_response = next(r for r in results if r.code == 429)
        error = json.loads(error_response.body)
        self.assertIn("Organization QPS limit exceeded (2 requests/second)", error["error"])

        # Wait 1 second and try again - should succeed
        await asyncio.sleep(1)
        response = await self.fetch_async(f"/v0/pipes/{pipe_name}.json?token={self.admin_token}")
        self.assertEqual(response.code, 200)

        # We should have a span with a 429 error
        span_logs = await self.get_span_async(url=error_response.effective_url)
        self.assertIn("Organization QPS limit exceeded (2 requests/second)", span_logs["error"])
        self.assertEqual(span_logs["status_code"], 429, span_logs)

    @tornado.testing.gen_test
    @patch("tinybird.monitor.statsd_client.incr")
    async def test_endpoint_reach_limit_for_dev_workspace(self, mock_incr: Mock):
        u = Users.get_by_id(self.WORKSPACE_ID)
        u.plan = BillingPlans.DEV
        u.created_at = datetime(2024, 8, 13)
        u.save()

        await self._make_endpoint()
        token = Users.add_token(u, "test_dev", scopes.ADMIN)

        # For DEV workspaces, we are tracking with 20 QPS
        result = await asyncio.gather(
            *[self.fetch_async(f"/v0/pipes/test_pipe.json?token={token}&i={i}", method="GET") for i in range(100)]
        )
        self.assertTrue(any(r.code == 429 for r in result))
        self.assertTrue(any(r.code == 200 for r in result))
        error_response = next(r for r in result if r.code == 429)
        self.assertEqual(
            json.loads(error_response.body)["error"],
            "Workspaces created since 2024-08-12 have a limit of 20 requests per second by default. Please contact support@tinybird.co if you need to increase the limit.",
        )
        self.assertFalse(
            any(
                f"tinybird.{statsd_client.region_machine}.rate_limit.{self.base_workspace.id}.workspace_api_requests"
                in call.args
                for call in mock_incr.call_args_list
            ),
            mock_incr.call_args_list,
        )

    @tornado.testing.gen_test
    @patch("tinybird.monitor.statsd_client.incr")
    async def test_endpoint_reach_limit_for_pro_workspace(self, mock_incr: Mock):
        u = Users.get_by_id(self.WORKSPACE_ID)
        u.plan = BillingPlans.PRO
        u.created_at = datetime(2024, 8, 12, 0, 0, 1)
        u.save()

        await self._make_endpoint()
        token = Users.add_token(u, "test_dev", scopes.ADMIN)

        # For DEV workspaces, we are tracking with 20 QPS
        result = await asyncio.gather(
            *[self.fetch_async(f"/v0/pipes/test_pipe.json?token={token}&i={i}", method="GET") for i in range(100)]
        )
        self.assertTrue(any(r.code == 429 for r in result))
        self.assertTrue(any(r.code == 200 for r in result))
        error_response = next(r for r in result if r.code == 429)
        self.assertEqual(
            json.loads(error_response.body)["error"],
            "Workspaces created since 2024-08-12 have a limit of 20 requests per second by default. Please contact support@tinybird.co if you need to increase the limit.",
        )

        self.assertFalse(
            any(
                f"tinybird.{statsd_client.region_machine}.rate_limit.{self.base_workspace.id}.workspace_api_requests"
                in call.args
                for call in mock_incr.call_args_list
            ),
            mock_incr.call_args_list,
        )

    @tornado.testing.gen_test
    async def test_endpoint_tracking_without_dry_run_feature_flag(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        u.plan = BillingPlans.CUSTOM
        u.save()

        await self._make_endpoint()
        token = Users.add_token(u, "test_2", scopes.ADMIN)

        result = await asyncio.gather(
            *[self.fetch_async(f"/v0/pipes/test_pipe.json?token={token}&i={i}", method="GET") for i in range(10)]
        )
        self.assertTrue(all(r.code == 200 for r in result))

    @tornado.testing.gen_test
    async def test_pipe_data_with_endpoint_with_explicit_endpoint_request_check_limit(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        u.plan = BillingPlans.CUSTOM
        u.save()

        with User.transaction(self.WORKSPACE_ID) as w:
            w.feature_flags[FeatureFlagWorkspaces.DISTRIBUTED_ENDPOINT_CONCURRENCY.value] = True

        await self._make_endpoint()

        # Limit concurrency in endpoint
        TINYBIRD_WORKSPACE = f"test_tinybird{uuid.uuid4().hex}"
        TINYBIRD_USER = f"{TINYBIRD_WORKSPACE}@tinybird.co"
        tinybird_user_account = UserAccount.register(TINYBIRD_USER, "pass")
        tinybird_user_account_token = UserAccount.get_token_for_scope(tinybird_user_account, scopes.AUTH)
        self.users_to_delete.append(tinybird_user_account)
        params = {
            "operation": "change_endpoint_limit",
            "limit_name": EndpointLimits.get_limit_key("test_pipe", EndpointLimits.max_concurrent_queries),
            "limit_value": 1,
            "limit_setting": EndpointLimits.max_concurrent_queries.name,
            "endpoint_name": "test_pipe",
        }
        headers = {"Authorization": f"Bearer {tinybird_user_account_token}"}
        r = await self.fetch_async(
            f"/cheriff/workspace/{u.id}?{urlencode(params)}", method="POST", body="", headers=headers
        )
        self.assertEqual(r.code, 200, r.body)

        params = {
            "operation": "change_endpoint_limit",
            "limit_name": EndpointLimits.get_limit_key("test_pipe", EndpointLimits.max_threads),
            "limit_value": 2,
            "limit_setting": EndpointLimits.max_threads.name,
            "endpoint_name": "test_pipe",
        }
        headers = {"Authorization": f"Bearer {tinybird_user_account_token}"}
        r = await self.fetch_async(
            f"/cheriff/workspace/{u.id}?{urlencode(params)}", method="POST", body="", headers=headers
        )
        self.assertEqual(r.code, 200, r.body)

        token = Users.add_token(u, "test_2", scopes.ADMIN)
        result = await asyncio.gather(
            *[self.fetch_async(f"/v0/pipes/test_pipe.json?token={token}&i={i}", method="GET") for i in range(10)]
        )
        self.assertTrue(any([r.code == 429 for r in result]))
        successful_request = next(r for r in result if r.code == 200)
        query_id_sucessful_execution = successful_request.headers["X-Request-Id"]

        query_log = await self.get_query_logs_by_where_async(f"query_id = '{query_id_sucessful_execution}'")
        self.assertTrue(all(log["Settings"]["max_threads"] == "2" for log in query_log), query_log)

        span_logs = await self.get_span_async(url=successful_request.effective_url)
        span_log_tags = json.loads(span_logs["tags"])
        self.assertEqual(span_log_tags.get("max_threads"), 2, span_logs)

        # Let's increase the limit to make sure the semaphore will be updated
        params = {
            "operation": "change_endpoint_limit",
            "limit_name": EndpointLimits.get_limit_key("test_pipe", EndpointLimits.max_concurrent_queries),
            "limit_value": 10,
            "limit_setting": EndpointLimits.max_concurrent_queries.name,
            "endpoint_name": "test_pipe",
        }
        headers = {"Authorization": f"Bearer {tinybird_user_account_token}"}
        r = await self.fetch_async(
            f"/cheriff/workspace/{u.id}?{urlencode(params)}", method="POST", body="", headers=headers
        )
        self.assertEqual(r.code, 200, r.body)

        # Let's remove the limits
        params = {
            "operation": "change_endpoint_limit",
            "limit_name": EndpointLimits.get_limit_key("test_pipe", EndpointLimits.max_concurrent_queries),
            "limit_value": 0,
            "endpoint_name": "test_pipe",
            "limit_setting": EndpointLimits.max_concurrent_queries.name,
        }
        headers = {"Authorization": f"Bearer {tinybird_user_account_token}"}
        r = await self.fetch_async(
            f"/cheriff/workspace/{u.id}?{urlencode(params)}", method="POST", body="", headers=headers
        )
        self.assertEqual(r.code, 200, r.body)

        params = {
            "operation": "change_endpoint_limit",
            "limit_name": EndpointLimits.get_limit_key("test_pipe", EndpointLimits.max_threads),
            "limit_value": 0,
            "endpoint_name": "test_pipe",
            "limit_setting": EndpointLimits.max_threads.name,
        }
        r = await self.fetch_async(
            f"/cheriff/workspace/{u.id}?{urlencode(params)}", method="POST", body="", headers=headers
        )
        self.assertEqual(r.code, 200, r.body)

        result = await asyncio.gather(
            *[self.fetch_async(f"/v0/pipes/test_pipe.json?token={token}&i={i}", method="GET") for i in range(10, 12)]
        )
        self.assertTrue(all([r.code == 200 for r in result]))
        first_sucessfull = next(r for r in result if r.code == 200)

        query_log = await self.get_query_logs_by_where_async(f"query_id = '{query_id_sucessful_execution}'")
        self.assertFalse(all(log["Settings"]["max_threads"] == "1" for log in query_log), query_log)

        span_logs = await self.get_span_async(url=first_sucessfull.effective_url)
        span_log_tags = json.loads(span_logs["tags"])
        self.assertNotEqual(span_log_tags.get("max_threads"), 2, span_logs)

    @tornado.testing.gen_test
    async def test_pipe_data_with_endpoint_with_not_limited_when_max_concurrent_queries_is_zero(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        u.plan = BillingPlans.CUSTOM
        u.save()

        with User.transaction(self.WORKSPACE_ID) as w:
            w.feature_flags[FeatureFlagWorkspaces.DISTRIBUTED_ENDPOINT_CONCURRENCY.value] = True

        await self._make_endpoint()

        # Limit concurrency in endpoint
        TINYBIRD_WORKSPACE = f"test_tinybird{uuid.uuid4().hex}"
        TINYBIRD_USER = f"{TINYBIRD_WORKSPACE}@tinybird.co"
        tinybird_user_account = UserAccount.register(TINYBIRD_USER, "pass")
        tinybird_user_account_token = UserAccount.get_token_for_scope(tinybird_user_account, scopes.AUTH)
        self.users_to_delete.append(tinybird_user_account)
        params = {
            "operation": "change_endpoint_limit",
            "limit_name": EndpointLimits.get_limit_key("test_pipe", EndpointLimits.max_concurrent_queries),
            "limit_value": 0,
            "endpoint_name": "test_pipe",
            "limit_setting": EndpointLimits.max_concurrent_queries.name,
        }
        headers = {"Authorization": f"Bearer {tinybird_user_account_token}"}
        r = await self.fetch_async(
            f"/cheriff/workspace/{u.id}?{urlencode(params)}", method="POST", body="", headers=headers
        )
        self.assertEqual(r.code, 200, r.body)

        params = {
            "operation": "change_endpoint_limit",
            "limit_name": EndpointLimits.get_limit_key("test_pipe", EndpointLimits.max_threads),
            "limit_value": 0,
            "endpoint_name": "test_pipe",
            "limit_setting": EndpointLimits.max_threads.name,
        }
        headers = {"Authorization": f"Bearer {tinybird_user_account_token}"}
        r = await self.fetch_async(
            f"/cheriff/workspace/{u.id}?{urlencode(params)}", method="POST", body="", headers=headers
        )
        self.assertEqual(r.code, 200, r.body)

        token = Users.add_token(u, "test_2", scopes.ADMIN)

        result = await asyncio.gather(
            *[self.fetch_async(f"/v0/pipes/test_pipe.json?token={token}&i={i}", method="GET") for i in range(2)]
        )
        self.assertFalse(any([r.code == 429 for r in result]))
        successful_request = next(r for r in result if r.code == 200)
        query_id_sucessful_execution = successful_request.headers["X-Request-Id"]

        # Check that the query was executed with the default max_threads
        query_log = await self.get_query_logs_by_where_async(f"query_id = '{query_id_sucessful_execution}'")
        self.assertTrue(all(log["Settings"]["max_threads"] != "1" for log in query_log), query_log)

        # Check that the span logs doesnt have the max_threads tag
        span_logs = await self.get_span_async(url=successful_request.effective_url)
        span_log_tags = json.loads(span_logs["tags"])
        self.assertEqual(span_log_tags.get("max_threads"), None, span_logs)

    @tornado.testing.gen_test
    async def test_enable_analyzer_in_cheriff_for_endpoint(self):
        await self._make_endpoint()

        # Limit concurrency in endpoint
        TINYBIRD_WORKSPACE = f"test_tinybird{uuid.uuid4().hex}"
        TINYBIRD_USER = f"{TINYBIRD_WORKSPACE}@tinybird.co"
        tinybird_user_account = UserAccount.register(TINYBIRD_USER, "pass")
        tinybird_user_account_token = UserAccount.get_token_for_scope(tinybird_user_account, scopes.AUTH)
        self.users_to_delete.append(tinybird_user_account)
        params = {
            "operation": "change_endpoint_limit",
            "limit_name": EndpointLimits.get_limit_key("test_pipe", EndpointLimits.analyzer),
            "limit_value": 1,
            "limit_setting": EndpointLimits.analyzer.name,
            "endpoint_name": "test_pipe",
        }
        headers = {"Authorization": f"Bearer {tinybird_user_account_token}"}
        r = await self.fetch_async(
            f"/cheriff/workspace/{self.WORKSPACE_ID}?{urlencode(params)}", method="POST", body="", headers=headers
        )
        self.assertEqual(r.code, 200, r.body)

        response = await self.fetch_async(f"/v0/pipes/test_pipe.json?token={self.admin_token}", method="GET")
        self.assertEqual(response.code, 200, response.body)
        query_id_sucessful_execution = response.headers["X-Request-Id"]

        # Check that the query was executed with the default max_threads
        query_log = await self.get_query_logs_by_where_async(f"query_id = '{query_id_sucessful_execution}'")
        self.assertTrue(all(log["Settings"]["allow_experimental_analyzer"] == "1" for log in query_log), query_log)

    @tornado.testing.gen_test
    async def test_backend_hint_default_query_hash_sticky_behaviour(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        response = await self.fetch_async(
            f"/v0/pipes/test_pipe/nodes?token={token}&name=dummy_node", method="POST", body="SELECT 1"
        )
        self.assertEqual(response.code, 200)
        pipe_node = json.loads(response.body)
        await self._make_endpoint(pipe_node["id"])

        with patch.object(HTTPClient, "query", side_effect=HTTPClient_query_original, autospec=True) as mock_query:
            await self.fetch_async(f"/v0/pipes/test_pipe.json?token={self.admin_token}", method="GET")
            mock_query.assert_called_once()
            self.assertEqual(
                mock_query.call_args_list[0].kwargs.get("backend_hint"),
                f"{self.WORKSPACE_ID}:6813d4bdb65b8b222514eb8b1e8a7d11",
            )

    @tornado.testing.gen_test
    async def test_max_bytes_before_external_group_by_status_in_cheriff_for_endpoint(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        response = await self.fetch_async(
            f"/v0/pipes/test_pipe/nodes?token={token}&name=dummy_node", method="POST", body="SELECT 1"
        )
        self.assertEqual(response.code, 200)
        pipe_node = json.loads(response.body)
        await self._make_endpoint(pipe_node["id"])

        TINYBIRD_WORKSPACE = f"test_tinybird{uuid.uuid4().hex}"
        TINYBIRD_USER = f"{TINYBIRD_WORKSPACE}@tinybird.co"
        tinybird_user_account = UserAccount.register(TINYBIRD_USER, "pass")
        tinybird_user_account_token = UserAccount.get_token_for_scope(tinybird_user_account, scopes.AUTH)
        self.users_to_delete.append(tinybird_user_account)
        params = {
            "operation": "change_endpoint_limit",
            "limit_name": EndpointLimits.get_limit_key("test_pipe", EndpointLimits.max_bytes_before_external_group_by),
            "limit_value": 23622320130,
            "limit_setting": EndpointLimits.max_bytes_before_external_group_by.name,
            "endpoint_name": "test_pipe",
        }
        headers = {"Authorization": f"Bearer {tinybird_user_account_token}"}
        r = await self.fetch_async(
            f"/cheriff/workspace/{self.WORKSPACE_ID}?{urlencode(params)}", method="POST", body="", headers=headers
        )
        self.assertEqual(r.code, 200, r.body)

        with patch.object(HTTPClient, "query", side_effect=HTTPClient_query_original, autospec=True) as mock_query:
            await self.fetch_async(f"/v0/pipes/test_pipe.json?token={self.admin_token}", method="GET")
            mock_query.assert_called_once()
            self.assertEqual(mock_query.call_args_list[0].kwargs.get("max_bytes_before_external_group_by"), 23622320130)

    @tornado.testing.gen_test
    async def test_backend_hint_disabled_in_cheriff_for_endpoint(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        response = await self.fetch_async(
            f"/v0/pipes/test_pipe/nodes?token={token}&name=dummy_node", method="POST", body="SELECT 1"
        )
        self.assertEqual(response.code, 200)
        pipe_node = json.loads(response.body)
        await self._make_endpoint(pipe_node["id"])

        TINYBIRD_WORKSPACE = f"test_tinybird{uuid.uuid4().hex}"
        TINYBIRD_USER = f"{TINYBIRD_WORKSPACE}@tinybird.co"
        tinybird_user_account = UserAccount.register(TINYBIRD_USER, "pass")
        tinybird_user_account_token = UserAccount.get_token_for_scope(tinybird_user_account, scopes.AUTH)
        self.users_to_delete.append(tinybird_user_account)
        params = {
            "operation": "change_endpoint_limit",
            "limit_name": EndpointLimits.get_limit_key("test_pipe", EndpointLimits.backend_hint),
            "limit_value": 1,
            "limit_setting": EndpointLimits.backend_hint.name,
            "endpoint_name": "test_pipe",
        }
        headers = {"Authorization": f"Bearer {tinybird_user_account_token}"}
        r = await self.fetch_async(
            f"/cheriff/workspace/{self.WORKSPACE_ID}?{urlencode(params)}", method="POST", body="", headers=headers
        )
        self.assertEqual(r.code, 200, r.body)

        with patch.object(HTTPClient, "query", side_effect=HTTPClient_query_original, autospec=True) as mock_query:
            await self.fetch_async(f"/v0/pipes/test_pipe.json?token={self.admin_token}", method="GET")
            mock_query.assert_called_once()
            self.assertEqual(mock_query.call_args_list[0].kwargs.get("backend_hint"), None)

    @tornado.testing.gen_test
    async def test_backend_hint_enabled_in_cheriff_for_endpoint(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        response = await self.fetch_async(
            f"/v0/pipes/test_pipe/nodes?token={token}&name=dummy_node", method="POST", body="SELECT 1"
        )
        self.assertEqual(response.code, 200)
        pipe_node = json.loads(response.body)
        await self._make_endpoint(pipe_node["id"])

        TINYBIRD_WORKSPACE = f"test_tinybird{uuid.uuid4().hex}"
        TINYBIRD_USER = f"{TINYBIRD_WORKSPACE}@tinybird.co"
        tinybird_user_account = UserAccount.register(TINYBIRD_USER, "pass")
        tinybird_user_account_token = UserAccount.get_token_for_scope(tinybird_user_account, scopes.AUTH)
        self.users_to_delete.append(tinybird_user_account)
        params = {
            "operation": "change_endpoint_limit",
            "limit_name": EndpointLimits.get_limit_key("test_pipe", EndpointLimits.backend_hint),
            "limit_value": 0,
            "limit_setting": EndpointLimits.backend_hint.name,
            "endpoint_name": "test_pipe",
        }
        headers = {"Authorization": f"Bearer {tinybird_user_account_token}"}
        r = await self.fetch_async(
            f"/cheriff/workspace/{self.WORKSPACE_ID}?{urlencode(params)}", method="POST", body="", headers=headers
        )
        self.assertEqual(r.code, 200, r.body)

        with patch.object(HTTPClient, "query", side_effect=HTTPClient_query_original, autospec=True) as mock_query:
            await self.fetch_async(f"/v0/pipes/test_pipe.json?token={self.admin_token}", method="GET")
            mock_query.assert_called_once()
            self.assertEqual(
                mock_query.call_args_list[0].kwargs.get("backend_hint"),
                f"{self.WORKSPACE_ID}:6813d4bdb65b8b222514eb8b1e8a7d11",
            )

    @tornado.testing.gen_test
    async def test_backend_hint_query_template_overwrites_cheriff_and_default(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        template = """%
        {{backend_hint('aaaaa')}}
        SELECT 1
        """
        response = await self.fetch_async(
            f"/v0/pipes/test_pipe/nodes?token={token}&name=dummy_node", method="POST", body=template
        )
        self.assertEqual(response.code, 200)
        pipe_node = json.loads(response.body)
        await self._make_endpoint(pipe_node["id"])

        TINYBIRD_WORKSPACE = f"test_tinybird{uuid.uuid4().hex}"
        TINYBIRD_USER = f"{TINYBIRD_WORKSPACE}@tinybird.co"
        tinybird_user_account = UserAccount.register(TINYBIRD_USER, "pass")
        tinybird_user_account_token = UserAccount.get_token_for_scope(tinybird_user_account, scopes.AUTH)
        self.users_to_delete.append(tinybird_user_account)
        params = {
            "operation": "change_endpoint_limit",
            "limit_name": EndpointLimits.get_limit_key("test_pipe", EndpointLimits.backend_hint),
            "limit_value": 1,
            "limit_setting": EndpointLimits.backend_hint.name,
            "endpoint_name": "test_pipe",
        }
        headers = {"Authorization": f"Bearer {tinybird_user_account_token}"}
        r = await self.fetch_async(
            f"/cheriff/workspace/{self.WORKSPACE_ID}?{urlencode(params)}", method="POST", body="", headers=headers
        )
        self.assertEqual(r.code, 200, r.body)

        with patch.object(HTTPClient, "query", side_effect=HTTPClient_query_original, autospec=True) as mock_query:
            await self.fetch_async(f"/v0/pipes/test_pipe.json?token={self.admin_token}", method="GET")
            mock_query.assert_called_once()
            self.assertEqual(mock_query.call_args_list[0].kwargs.get("backend_hint"), "aaaaa")

    @tornado.testing.gen_test
    async def test_endpoint_monitor_tasks_works_as_expected(self):
        await self._make_endpoint()
        self.workspace = Users.get_by_id(self.WORKSPACE_ID)
        pipe = self.workspace.get_pipe("test_pipe")

        response = await self.fetch_async(f"/v0/pipes/test_pipe.json?token={self.admin_token}", method="GET")
        self.assertEqual(response.code, 200, response.body)

        # Populate workspaces_all and pipe_stats_rt
        data_tracker = WorkspaceDatabaseUsageTracker(exit_queue_timeout=1)
        data_tracker.start()
        data_tracker.terminate()
        data_tracker.join()
        self.force_flush_of_span_records()
        self.wait_for_public_table_replication("pipe_stats_rt")
        self.wait_for_public_table_replication("workspaces_all")

        # Added fake pipe_id that should be removed once the endpoint monitor task is executed
        max_threads_by_endpoint["random_id"] = 1
        # Run endpoint monitor task
        endpoint_monitor = EndpointMonitorTask()
        endpoint_monitor.clusters = ["ci_ch"]
        await endpoint_monitor.action()

        self.assertIsNone(max_threads_by_endpoint.get("random_id"))
        self.assertEqual(max_threads_by_endpoint.get(pipe.id), 1, max_threads_by_endpoint)
        response = await self.fetch_async(
            f"/v0/pipes/test_pipe.json?token={self.admin_token}&new_execution", method="GET"
        )
        self.assertEqual(response.code, 200, response.body)
        query_id = response.headers["X-Request-Id"]

        # Check that the query was executed with the default max_threads
        query_log = await self.get_query_logs_by_where_async(f"query_id = '{query_id}'")
        self.assertTrue(all(log["Settings"]["max_threads"] == "1" for log in query_log), query_log)

        # Check that the span logs doesnt have the max_threads tag
        span_logs = await self.get_span_async(url=response.effective_url)
        span_log_tags = json.loads(span_logs["tags"])
        self.assertEqual(span_log_tags.get("max_threads"), 1, span_logs)


class TestAPIQueryConcurrency(APIDataTableBaseTest):
    @tornado.testing.gen_test
    async def test_api_query_check_distributed_concurrency_limit(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        u.plan = BillingPlans.CUSTOM
        u.save()

        with User.transaction(self.WORKSPACE_ID) as w:
            w.feature_flags[FeatureFlagWorkspaces.DISTRIBUTED_ENDPOINT_CONCURRENCY.value] = True

        # Limit concurrency in query_api
        TINYBIRD_WORKSPACE = f"test_tinybird{uuid.uuid4().hex}"
        TINYBIRD_USER = f"{TINYBIRD_WORKSPACE}@tinybird.co"
        tinybird_user_account = UserAccount.register(TINYBIRD_USER, "pass")
        tinybird_user_account_token = UserAccount.get_token_for_scope(tinybird_user_account, scopes.AUTH)
        self.users_to_delete.append(tinybird_user_account)
        for method in ["GET", "POST"]:
            for api in [QUERY_API, QUERY_API_FROM_UI]:
                params = {
                    "operation": "change_query_api_limit",
                    "limit_name": EndpointLimits.get_limit_key(api, EndpointLimits.max_concurrent_queries),
                    "limit_value": 1,
                    "limit_setting": EndpointLimits.max_concurrent_queries.name,
                    "endpoint_name": api,
                }
                headers = {"Authorization": f"Bearer {tinybird_user_account_token}"}
                r = await self.fetch_async(
                    f"/cheriff/workspace/{u.id}?{urlencode(params)}", method="POST", body="", headers=headers
                )
                self.assertEqual(r.code, 200, r.body)

                token = Users.get_token_for_scope(u, scopes.ADMIN)
                params = {"token": token}
                body = None
                if api == QUERY_API_FROM_UI:
                    params["from"] = "ui"
                if method == "GET":
                    params["q"] = "select avg(number) from numbers(1000000)"
                else:
                    body = json.dumps({"q": "select avg(number) from numbers(1000000)"})

                result = await asyncio.gather(
                    *[self.fetch_async(f"/v0/sql?{urlencode(params)}", method=method, body=body) for _ in range(10)]
                )
                self.assertTrue(any([r.code == 429 for r in result]))
                self.assertTrue(any([r.code == 200 for r in result]))

                response = await self.fetch_async(f"/v0/sql?{urlencode(params)}", method=method, body=body)
                self.assertEqual(response.code, 200, response.body)


class TestAPIDataTableConcurrency(APIDataTableBaseTest):
    @tornado.testing.gen_test
    async def test_pipe_data_with_endpoint_with_explicit_endpoint_request_check_distributed_concurrency_limit(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        u.plan = BillingPlans.CUSTOM
        u.save()

        with User.transaction(self.WORKSPACE_ID) as w:
            w.feature_flags[FeatureFlagWorkspaces.DISTRIBUTED_ENDPOINT_CONCURRENCY.value] = True

        pipe_name = "concurrent_pipe"
        data = {"name": pipe_name, "nodes": [{"sql": "select avg(number) from numbers(1000000)", "name": "node_00"}]}
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {"token": token}
        response = await self.fetch_async(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/node_00/endpoint?token={token}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200)

        # Limit concurrency in endpoint
        TINYBIRD_WORKSPACE = f"test_tinybird{uuid.uuid4().hex}"
        TINYBIRD_USER = f"{TINYBIRD_WORKSPACE}@tinybird.co"
        tinybird_user_account = UserAccount.register(TINYBIRD_USER, "pass")
        tinybird_user_account_token = UserAccount.get_token_for_scope(tinybird_user_account, scopes.AUTH)
        self.users_to_delete.append(tinybird_user_account)
        params = {
            "operation": "change_endpoint_limit",
            "limit_name": EndpointLimits.get_limit_key(pipe_name, EndpointLimits.max_concurrent_queries),
            "limit_value": 1,
            "limit_setting": EndpointLimits.max_concurrent_queries.name,
            "endpoint_name": pipe_name,
        }
        headers = {"Authorization": f"Bearer {tinybird_user_account_token}"}
        r = await self.fetch_async(
            f"/cheriff/workspace/{u.id}?{urlencode(params)}", method="POST", body="", headers=headers
        )
        self.assertEqual(r.code, 200, r.body)

        token = Users.add_token(u, "test_2", scopes.ADMIN)
        result = await asyncio.gather(
            *[self.fetch_async(f"/v0/pipes/{pipe_name}.json?token={token}&i={i}", method="GET") for i in range(10)]
        )
        self.assertTrue(any([r.code == 429 for r in result]))
        self.assertTrue(any([r.code == 200 for r in result]))

        response = await self.fetch_async(f"/v0/pipes/{pipe_name}.json?token={token}", method="GET")
        self.assertEqual(response.code, 200, response.body)

    @patch("tinybird_shared.redis_client.redis_client.DEFAULT_LIMITS_MAX_CONNECTIONS", 1)
    @tornado.testing.gen_test
    async def test_pipe_data_with_endpoint_with_explicit_endpoint_request_check_distributed_concurrency_limit_platform_limit(
        self,
    ):
        u = Users.get_by_id(self.WORKSPACE_ID)
        u.plan = BillingPlans.CUSTOM
        u.save()

        with User.transaction(self.WORKSPACE_ID) as w:
            w.feature_flags[FeatureFlagWorkspaces.DISTRIBUTED_ENDPOINT_CONCURRENCY.value] = True

        pipe_name = "concurrent_pipe"
        data = {"name": pipe_name, "nodes": [{"sql": "select avg(number) from numbers(1000000)", "name": "node_00"}]}
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {"token": token}
        response = await self.fetch_async(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/node_00/endpoint?token={token}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200)

        # Limit concurrency in endpoint
        TINYBIRD_WORKSPACE = f"test_tinybird{uuid.uuid4().hex}"
        TINYBIRD_USER = f"{TINYBIRD_WORKSPACE}@tinybird.co"
        tinybird_user_account = UserAccount.register(TINYBIRD_USER, "pass")
        tinybird_user_account_token = UserAccount.get_token_for_scope(tinybird_user_account, scopes.AUTH)
        self.users_to_delete.append(tinybird_user_account)
        params = {
            "operation": "change_endpoint_limit",
            "limit_name": EndpointLimits.get_limit_key(pipe_name, EndpointLimits.max_concurrent_queries),
            "limit_value": 10,
            "limit_setting": EndpointLimits.max_concurrent_queries.name,
            "endpoint_name": pipe_name,
        }
        headers = {"Authorization": f"Bearer {tinybird_user_account_token}"}
        r = await self.fetch_async(
            f"/cheriff/workspace/{u.id}?{urlencode(params)}", method="POST", body="", headers=headers
        )
        self.assertEqual(r.code, 200, r.body)

        token = Users.add_token(u, "test_2", scopes.ADMIN)
        result = await asyncio.gather(
            *[self.fetch_async(f"/v0/pipes/{pipe_name}.json?token={token}&i={i}", method="GET") for i in range(10)]
        )
        self.assertTrue(any([r.code == 500 for r in result]))
        self.assertTrue(any([r.code == 200 for r in result]))

        response = await self.fetch_async(f"/v0/pipes/{pipe_name}.json?token={token}", method="GET")
        self.assertEqual(response.code, 200, response.body)


class TestAPIDataTableDifferentCluster(APIDataTableBaseTest):
    def setUp(self):
        super().setUp()
        self.workspace = Users.get_by_id(self.WORKSPACE_ID)
        self.token = Users.get_token_for_scope(self.workspace, scopes.ADMIN)
        with User.transaction(self.workspace.id) as workspace:
            self.ds = workspace.database_server
            workspace.database_server = CH_ADDRESS

    def tearDown(self):
        with User.transaction(self.workspace.id) as workspace:
            workspace.database_server = self.ds
        super().tearDown()

    def test_user_from_different_cluster_cannot_use_remote_with_restricted_tables(self):
        params = {"token": self.token, "ignore_sql_errors": "true"}

        data = {"name": "pipe_name", "nodes": []}

        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        response = self.fetch(
            f"/v0/pipes/pipe_name/nodes?{urlencode(params)}",
            method="POST",
            body="""%
                    SELECT
                        'hello' AS hola,
                        *
                    FROM cluster('127.0.0.1', 'system.parts')
                """,
            headers={"Content-type": "application/json"},
        )

        response = self.fetch(
            f"/v0/pipes/pipe_name/nodes?{urlencode(params)}",
            method="POST",
            body="SELECT * FROM pipe_name_0",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        node_id = json.loads(response.body)["id"]
        response = self.fetch(
            f"/v0/pipes/pipe_name/nodes/{node_id}/endpoint?{urlencode(params)}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        response = self.fetch(f"/v0/pipes/pipe_name.json?token={self.token}")
        self.assertEqual(response.code, 403, response.body)
        self.assertEqual(
            "The query uses disabled table functions: 'cluster'" in json.loads(response.body)["error"], True
        )

        response = self.fetch(f"/v0/pipes/pipe_name.json?token={self.token}&debug=query")
        self.assertEqual(response.code, 403, response.body)
        self.assertEqual("The query uses disabled table functions: 'cluster'" in response.body.decode(), True)


class TestAPITable(BaseTest):
    def setUp(self):
        super().setUp()
        self.create_test_datasource()
        self.tb_api_proxy_async = TBApiProxyAsync(self)

    def tearDown(self):
        self._drop_token()
        super().tearDown()

    def _drop_token(self):
        try:
            u = Users.get_by_id(self.WORKSPACE_ID)
            token = Users.get_token(u, "test")
            if token:
                Users.drop_token(u, token)
        except Exception:
            pass

    async def _append_node(
        self, sql, name=None, description=None, expected_code=200, pipe_name="test_pipe", node_type=None
    ):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        url_parts = [f"/v0/pipes/{pipe_name}/nodes?token={token}"]
        if name:
            url_parts += [f"name={name}"]
        if description:
            url_parts += [f"description={description}"]
        if node_type:
            url_parts += [f"type={node_type}"]
        url = "&".join(url_parts)
        response = await self.fetch_async(url, method="POST", body=sql)
        self.assertEqual(response.code, expected_code)
        return json.loads(response.body)

    async def _make_endpoint(self, pipe_name_or_id="test_pipe", node_name_or_id=None, token_name="test"):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, token_name, scopes.ADMIN)
        if not node_name_or_id:
            node = Users.get_pipe(u, pipe_name_or_id).pipeline.nodes[0]
            node_name_or_id = node.id

        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name_or_id}/nodes/{node_name_or_id}/endpoint?token={token}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200)

    def test_non_auth(self):
        self.check_non_auth_responses(["/v0/pipes", "/v0/pipes?token=fake"])

    def test_pipe_list(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)
        response = self.fetch("/v0/pipes?token=%s" % token)
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body)["pipes"][0]["name"], "test_pipe")
        self.assertEqual("dependencies" not in json.loads(response.body)["pipes"][0]["nodes"][0], True)

    def test_pipe_list_with_attrs(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)
        response = self.fetch(f"/v0/pipes?token={token}&attrs=name,type")
        self.assertEqual(response.code, 200)
        self.assertEqual(
            json.loads(response.body),
            {
                "pipes": [
                    {"name": "test_pipe", "url": "http://localhost:8889/v0/pipes/test_pipe.json", "type": "default"}
                ]
            },
        )

    def test_pipe_list_with_node_attrs(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)
        response = self.fetch(f"/v0/pipes?token={token}&attrs=name,nodes")
        self.assertEqual(response.code, 200)
        self.assertEqual(
            json.loads(response.body),
            {
                "pipes": [
                    {
                        "name": "test_pipe",
                        "nodes": [
                            {
                                "id": mock.ANY,
                                "name": "test_pipe_0",
                                "sql": "select * from test_table",
                                "description": None,
                                "materialized": None,
                                "cluster": None,
                                "tags": {},
                                "created_at": matches(r"2\d+-\d+-\d+ \d+:\d+:\d+"),
                                "updated_at": matches(r"2\d+-\d+-\d+ \d+:\d+:\d+"),
                                "version": 0,
                                "project": None,
                                "result": None,
                                "ignore_sql_errors": False,
                                "node_type": "standard",
                            }
                        ],
                        "url": "http://localhost:8889/v0/pipes/test_pipe.json",
                    }
                ]
            },
        )

    def test_pipe_list_with_attrs_and_node_attrs(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)
        response = self.fetch(f"/v0/pipes?token={token}&attrs=name,nodes&node_attrs=name")
        self.assertEqual(response.code, 200)
        self.assertEqual(
            json.loads(response.body),
            {
                "pipes": [
                    {
                        "name": "test_pipe",
                        "nodes": [{"name": "test_pipe_0"}],
                        "url": "http://localhost:8889/v0/pipes/test_pipe.json",
                    }
                ]
            },
        )

    def test_pipe_list_with_attrs_and_node_attrs2(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)
        response = self.fetch(f"/v0/pipes?token={token}&attrs=name&node_attrs=name")
        self.assertEqual(response.code, 200)
        self.assertEqual(
            json.loads(response.body),
            {
                "pipes": [
                    {
                        "name": "test_pipe",
                        "nodes": [{"name": "test_pipe_0"}],
                        "url": "http://localhost:8889/v0/pipes/test_pipe.json",
                    }
                ]
            },
        )

    def test_pipe_list_dependencies(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)
        response = self.fetch("/v0/pipes?token=%s&dependencies=true" % token)
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body)["pipes"][0]["name"], "test_pipe")
        self.assertEqual("dependencies" in json.loads(response.body)["pipes"][0]["nodes"][0], True, response.body)

    def test_pipe_list_dependencies_error(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)
        response = self.fetch("/v0/pipes?token=%s&dependencies=wadus" % token)
        self.assertEqual(response.code, 400)
        self.assertEqual(
            json.loads(response.body)["error"],
            """The parameter "dependencies" value "wadus" is invalid. Valid values are: 'true', 'false'""",
        )

    def test_pipe_list_with_token(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        test_pipe_2 = Users.add_pipe_sync(u, "test_pipe_2", "select * from test_table")

        def get_pipes(token):
            response = self.fetch("/v0/pipes?token=%s" % token)
            self.assertEqual(response.code, 200)
            return json.loads(response.body)["pipes"]

        test_pipe = Users.get_pipe(u, "test_pipe")
        read_token = Users.add_token(u, "read token", scopes.PIPES_READ, test_pipe.id)
        pipes = get_pipes(read_token)
        self.assertEqual(pipes[0]["name"], "test_pipe")
        self.assertEqual(len(pipes), 1)

        read_token = Users.add_scope_to_token(u, read_token, scopes.PIPES_READ, test_pipe_2.id)
        pipes = get_pipes(read_token)
        self.assertEqual(len(pipes), 2)

        create_token = Users.add_token(u, "create token", scopes.PIPES_CREATE)
        pipes = get_pipes(create_token)
        self.assertEqual(len(pipes), 2)

    @tornado.testing.gen_test
    async def test_pipe_list_with_pipe_read_token_returns_limited_result(self):
        pipe_name = "the_pipe_name"
        await self.tb_api_proxy_async.create_pipe(
            token=self.admin_token,
            pipe_name=pipe_name,
            queries=["select * from test_table"],
        )

        list_with_admin = await self.tb_api_proxy_async.list_pipes(self.admin_token, dependencies=True)
        list_with_admin_json = json.loads(list_with_admin.body)

        the_pipe_json = next((pipe for pipe in list_with_admin_json["pipes"] if pipe["name"] == pipe_name), None)
        assert the_pipe_json["edited_by"] == self.USER
        assert the_pipe_json["nodes"][0]["sql"] == "select * from test_table"
        assert the_pipe_json["nodes"][0]["dependencies"] == ["test_table"]

        workspace = User.get_by_id(self.WORKSPACE_ID)
        pipe = workspace.get_pipe(pipe_name)
        read_token = Users.add_token(workspace, "read token", scopes.PIPES_READ, pipe.id)
        list_with_read = await self.tb_api_proxy_async.list_pipes(read_token, dependencies=True)
        list_with_read_json = json.loads(list_with_read.body)

        the_pipe_json = next((pipe for pipe in list_with_read_json["pipes"] if pipe["name"] == pipe_name), None)
        assert the_pipe_json["edited_by"] == ""
        assert the_pipe_json["nodes"][0]["sql"] == ""
        assert the_pipe_json["nodes"][0]["dependencies"] == []

    def test_pipe_detail(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)
        response = self.fetch("/v0/pipes/test_pipe?token=%s" % token)
        payload = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(payload["name"], "test_pipe")
        self.assertEqual(len(payload["nodes"]), 1)
        self.assertEqual(payload["nodes"][0]["sql"], "select * from test_table")

    @tornado.testing.gen_test
    async def test_pipe_details_with_pipe_read_token_returns_limited_result(self):
        pipe_name = "the_pipe_name"
        await self.tb_api_proxy_async.create_pipe(
            token=self.admin_token,
            pipe_name=pipe_name,
            queries=["select * from test_table"],
        )

        details_with_admin = await self.tb_api_proxy_async.get_pipe_details(pipe_name, self.admin_token)
        details_with_admin_json = json.loads(details_with_admin.body)

        assert details_with_admin_json["edited_by"] == self.USER
        assert details_with_admin_json["nodes"][0]["sql"] == "select * from test_table"
        assert details_with_admin_json["nodes"][0]["dependencies"] == ["test_table"]

        workspace = User.get_by_id(self.WORKSPACE_ID)
        pipe = workspace.get_pipe(pipe_name)
        read_token = Users.add_token(workspace, "read token", scopes.PIPES_READ, pipe.id)
        details_with_read = await self.tb_api_proxy_async.get_pipe_details(pipe_name, read_token)
        details_with_read_json = json.loads(details_with_read.body)

        assert details_with_read_json["edited_by"] == ""
        assert details_with_read_json["nodes"][0]["sql"] == ""
        assert details_with_read_json["nodes"][0]["dependencies"] == []

    def test_pipe_detail_with_other_pipe_token(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        t = Users.add_token(u, "test", scopes.PIPES_CREATE)
        test_pipe = Users.get_pipe(u, "test_pipe")
        test_pipe_2 = Users.add_pipe_sync(u, "test_pipe_2", "select * from test_table")

        t = Users.add_token(u, "test_pipes_read_test_pipe", scopes.PIPES_READ, test_pipe.id)
        response = self.fetch(f"/v0/pipes/{test_pipe.id}?token=%s" % t)
        self.assertEqual(response.code, 200)
        response = self.fetch(f"/v0/pipes/{test_pipe_2.id}?token=%s" % t)
        self.assertEqual(response.code, 403)

    def test_pipe_pipefile(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)
        response = self.fetch("/v0/pipes/test_pipe.pipe?token=%s" % token)
        self.assertEqual(response.code, 200)
        self.assertEqual(response.headers["content-type"], "text/plain")
        self.assertEqual(response.body.decode(), "NODE test_pipe_0\nSQL >\n\n    select * from test_table\n\n\n")

    def test_pipe_last_update(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)
        response = self.fetch("/v0/pipes/test_pipe/last_update?token=%s" % token)
        payload = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(payload["name"], "test_pipe")
        self.assertIn("edited_by", payload)
        self.assertIn("updated_at", payload)
        self.assertNotIn("nodes", payload)

    @tornado.testing.gen_test
    async def test_pipe_change_name(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.PIPES_CREATE)
        old_id = Users.get_pipe(u, "test_pipe").id
        response = await self.fetch_async("/v0/pipes/test_pipe?name=new_name&token=%s" % token, method="PUT", body="")
        self.assertEqual(response.code, 200)
        body = json.loads(response.body)
        self.assertEqual(body["name"], "new_name")
        self.assertEqual(body["id"], old_id)

    @tornado.testing.gen_test
    async def test_pipe_change_name_viewer(self):
        user_b_email = f"user_b_{uuid.uuid4().hex}@example.com"

        await self.tb_api_proxy_async.invite_user_to_workspace(
            token=self.user_token, workspace_id=self.WORKSPACE_ID, user_to_invite_email=user_b_email, role="viewer"
        )

        workspace = User.get_by_id(self.WORKSPACE_ID)

        user_b = UserAccount.get_by_email(user_b_email)
        UserWorkspaceRelationships.change_role(user_b.id, workspace, "viewer")
        token = Users.get_token_for_scope(workspace, scopes.ADMIN_USER, user_b.id)

        response = await self.fetch_async("/v0/pipes/test_pipe?name=new_name&token=%s" % token, method="PUT", body="")

        assert response.code == 403, response.code
        assert "Viewer" in response.body.decode(), response.body.decode()

    @tornado.testing.gen_test
    async def test_pipe_change_forbidden_name(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.PIPES_CREATE)
        response = await self.fetch_async("/v0/pipes/test_pipe?name=FROM&token=%s" % token, method="PUT", body="")
        self.assertEqual(response.code, 400)
        result = json.loads(response.body)
        self.assertTrue(
            "FROM is a reserved word. Name must start with a letter and contain only letters, numbers, and underscores. Hint: use FROM_."
            in result["error"],
            result,
        )

    def test_pipe_change_description(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.PIPES_CREATE)
        pipe = Users.get_pipe(u, "test_pipe")

        response = self.fetch("/v0/pipes/test_pipe?description=wadus&token=%s" % token, method="PUT", body="")
        self.assertEqual(response.code, 200)
        body = json.loads(response.body)
        self.assertEqual(body["name"], pipe.name)
        self.assertEqual(body["description"], "wadus")
        self.assertEqual(body["id"], pipe.id)

        response = self.fetch("/v0/pipes/test_pipe?description=&token=%s" % token, method="PUT", body="")
        self.assertEqual(response.code, 200)
        body = json.loads(response.body)
        self.assertEqual(body["name"], pipe.name)
        self.assertEqual(body["description"], "")
        self.assertEqual(body["id"], pipe.id)

    def test_pipe_change_name_clash_with_datasource(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.PIPES_CREATE)
        response = self.fetch("/v0/pipes/test_pipe?name=test_table&token=%s" % token, method="PUT", body="")
        self.assertEqual(response.code, 409)
        body = json.loads(response.body)
        self.assertEqual(
            body["error"],
            'There is already a Data Source with name "test_table". Pipe names must be globally unique',
        )

    def test_pipe_change_name_clash_with_node_name(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.PIPES_CREATE)
        pipe = Users.add_pipe_sync(u, "test_rename_pipe_clash_node_name", "select 1")
        node = pipe.pipeline.last()
        response = self.fetch(f"/v0/pipes/test_pipe?name={node.name}&token={token}", method="PUT", body="")
        self.assertEqual(response.code, 409)
        body = json.loads(response.body)
        self.assertEqual(
            body["error"],
            f'There is already a Node in Pipe "test_rename_pipe_clash_node_name" with name "{node.name}". Pipe names must be globally unique',
        )

    def test_pipe_change_name_clash_with_node_name_in_same_pipe(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.PIPES_CREATE)
        pipe = Users.add_pipe_sync(u, "test_rename_pipe_clash_node_name", "select 1")
        node = pipe.pipeline.last()
        response = self.fetch(f"/v0/pipes/{pipe.name}?name={node.name}&token={token}", method="PUT", body="")
        self.assertEqual(response.code, 409)
        body = json.loads(response.body)
        self.assertEqual(
            body["error"],
            f'There is already a Node in this Pipe with name "{node.name}". Pipe names must be globally unique',
        )

    @tornado.testing.gen_test
    async def test_pipe_drop(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)
        token_with_no_permissions = Users.add_token(u, "create_pipe", scopes.PIPES_CREATE)
        response = await self.fetch_async("/v0/pipes/test_pipe?token=%s" % token_with_no_permissions, method="DELETE")
        self.assertEqual(response.code, 403)
        self.assertEqual(
            json.loads(response.body)["error"], "user does not have permissions to drop pipes, set DROP scope"
        )
        response = await self.fetch_async("/v0/pipes/test_pipe?token=%s" % token, method="DELETE")
        self.assertEqual(response.code, 204)
        self.assertIsNone(Users.get_pipe(u, "test_pipe"))
        response = await self.fetch_async("/v0/pipes/test_pipe?token=%s" % token, method="DELETE")
        self.assertEqual(response.code, 404)
        self.assertEqual(json.loads(response.body)["error"], "Pipe 'test_pipe' not found")

    def test_pipe_drop_with_drop_scope(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        pipe_name = "test_pipe_to_drop"
        pipe = Users.add_pipe_sync(u, pipe_name, "select * from test_table")
        token = Users.add_token(u, "test", scopes.PIPES_DROP, pipe.id)
        response = self.fetch(f"/v0/pipes/{pipe_name}?token={token}", method="DELETE")
        self.assertEqual(response.code, 204)
        self.assertIsNone(Users.get_pipe(u, pipe_name))

    @patch.object(GCloudSchedulerJobs, "manage_job")
    @patch.object(GCloudSchedulerJobs, "update_job_status")
    def test_pipe_copy_drop(self, _mock_update_job, _mock_manage_job):
        u = Users.get_by_id(self.WORKSPACE_ID)

        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_pipe_copy_drop"
        node_name = "test_pipe_copy_drop_0"
        ds_a_name = "test_pipe_copy_drop_a_ds"
        ds_b_name = "test_pipe_copy_drop_b_ds"

        test_a_ds = Users.add_datasource_sync(u, ds_a_name)
        create_test_datasource(u, test_a_ds)
        test_b_ds = Users.add_datasource_sync(u, ds_b_name)
        create_test_datasource(u, test_b_ds)

        pipe = Users.add_pipe_sync(u, pipe_name, nodes=[{"name": node_name, "sql": f"select * from {ds_a_name}"}])

        expected_job_name = GCloudSchedulerJobs.generate_job_name(self.WORKSPACE_ID, pipe.id)

        params = {"token": token, "target_datasource": ds_b_name, "schedule_cron": "0 * * * *"}

        response = self.fetch(
            path=f"/v0/pipes/{pipe_name}/nodes/{node_name}/copy?{urlencode(params)}", method="POST", body=""
        )
        self.assertEqual(response.code, 200, response.body)

        pipe = Users.get_pipe(u, pipe_name)
        test_b_ds = Users.get_datasource(u, ds_b_name)
        self.assertIsNotNone(test_b_ds.tags.get("source_copy_pipes").get(pipe.id))

        data_sink = DataSink.get_by_resource_id(pipe.id, u.id)
        self.assertIsNotNone(data_sink)

        response = self.fetch(f"/v0/pipes/{pipe_name}?token={token}", method="DELETE")
        self.assertEqual(response.code, 204)
        self.assertIsNone(Users.get_pipe(u, pipe_name))

        test_b_ds = Users.get_datasource(u, ds_b_name)
        self.assertIsNone(test_b_ds.tags.get("source_copy_pipes").get(pipe.id))

        _mock_update_job.assert_called_with(SchedulerJobActions.DELETE, expected_job_name)

        try:
            data_sink = DataSink.get_by_resource_id(pipe.id, u.id)
        except Exception:
            data_sink = None
        self.assertIsNone(data_sink)

    def test_pipe_copy_drop_several_nodes(self):
        u = Users.get_by_id(self.WORKSPACE_ID)

        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_pipe_copy_drop_several_nodes"
        ds_a_name = "test_pipe_copy_drop_several_nodes_a_ds"
        ds_b_name = "test_pipe_copy_drop_several_nodes_b_ds"
        node_name = "copy_node"

        test_a_ds = Users.add_datasource_sync(u, ds_a_name)
        create_test_datasource(u, test_a_ds)
        test_b_ds = Users.add_datasource_sync(u, ds_b_name)
        create_test_datasource(u, test_b_ds)

        Users.add_pipe_sync(
            u,
            pipe_name,
            nodes=[
                {"name": f"{node_name}_0", "sql": f"select count() from {ds_b_name}"},
                {"name": node_name, "sql": f"select * from {ds_a_name}"},
                {"name": f"{node_name}_2", "sql": f"select count() from {ds_b_name}"},
            ],
        )

        params = {"token": token, "target_datasource": ds_b_name}

        response = self.fetch(
            path=f"/v0/pipes/{pipe_name}/nodes/{node_name}/copy?{urlencode(params)}", method="POST", body=""
        )
        self.assertEqual(response.code, 200, response.body)
        pipe = Users.get_pipe(u, pipe_name)

        # Remove Default Node
        response = self.fetch(path=f"/v0/pipes/{pipe_name}/nodes/{node_name}_0?token={token}", method="DELETE")
        self.assertEqual(response.code, 204, response.body)

        # Remove Pipe
        response = self.fetch(f"/v0/pipes/{pipe_name}?token={token}", method="DELETE")
        self.assertEqual(response.code, 204)
        self.assertIsNone(Users.get_pipe(u, pipe_name))

        test_b_ds = Users.get_datasource(u, ds_b_name)
        self.assertIsNone(test_b_ds.tags.get("source_copy_pipes").get(pipe.id))

    def test_pipe_copy_drop_exception(self):
        u = Users.get_by_id(self.WORKSPACE_ID)

        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_pipe_copy_drop_exception"
        ds_a_name = "test_pipe_copy_drop_exception_a_ds"
        ds_b_name = "test_pipe_copy_drop_exception_b_ds"
        node_name = "copy_node"

        test_a_ds = Users.add_datasource_sync(u, ds_a_name)
        create_test_datasource(u, test_a_ds)
        test_b_ds = Users.add_datasource_sync(u, ds_b_name)
        create_test_datasource(u, test_b_ds)

        Users.add_pipe_sync(
            u,
            pipe_name,
            nodes=[
                {"name": node_name, "sql": f"select * from {ds_a_name}"},
            ],
        )

        params = {"token": token, "target_datasource": ds_b_name}

        response = self.fetch(
            path=f"/v0/pipes/{pipe_name}/nodes/{node_name}/copy?{urlencode(params)}", method="POST", body=""
        )
        self.assertEqual(response.code, 200, response.body)

        # Remove Copy Node
        with patch("tinybird.user.Users.drop_copy_of_pipe_node_async", side_effect=Exception()):
            response = self.fetch(path=f"/v0/pipes/{pipe_name}/nodes/{node_name}?token={token}", method="DELETE")
            error = json.loads(response.body).get("error", None)
            self.assertEqual(response.code, 409, response.body)
            self.assertEqual(error, "Could not delete copy node, please retry or contact us at support@tinybird.co")

    def test_create_pipe_same_name_than_datasource(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.PIPES_CREATE)
        response = self.fetch(
            f"/v0/pipes?token={token}&name=test_table&sql=select+*+from+test_pipe+limit+10", method="POST", body=""
        )
        self.assertEqual(response.code, 409)
        res = json.loads(response.body)
        self.assertEqual(
            res["error"],
            'There is already a Data Source with name "test_table". Pipe names must be globally unique',
        )

    # https://gitlab.com/tinybird/analytics/-/issues/1164
    def test_create_pipe_with_a_public_datasource(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.PIPES_CREATE)
        response = self.fetch(
            f"/v0/pipes?token={token}&name=endpoint_errors&sql=select+*+from+tinybird.endpoint_errors+limit+10",
            method="POST",
            body="",
        )
        self.assertEqual(response.code, 200)

    # https://gitlab.com/tinybird/analytics/-/issues/1177
    def test_create_pipe_with_ops_log(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.PIPES_CREATE)
        response = self.fetch(
            f"/v0/pipes?token={token}&name=endpoint_errors&sql=select+count()+from+tinybird.datasources_ops_log",
            method="POST",
            body="",
        )
        self.assertEqual(response.code, 200)

    @tornado.testing.gen_test
    async def test_create_pipe_params(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        await self._make_endpoint(
            "test_pipe", token_name="test_create_pipe_params"
        )  # make test_pipe available for other pipes
        token = Users.add_token(u, "test_pipe_params", scopes.PIPES_CREATE)
        response = await self.fetch_async(
            f"/v0/pipes?token={token}&name=test_pipe2&sql=select+*+from+test_pipe+limit+10", method="POST", body=""
        )
        self.assertEqual(response.code, 200)

        res = json.loads(response.body)
        for x in ["id", "name", "nodes"]:
            self.assertIn(x, res)
            self.assertIsNotNone(res[x], x)
        self.assertEqual(len(res["nodes"]), 1)
        node = res["nodes"][0]
        self.assertEqual(node["name"], "test_pipe2_0")
        self.assertEqual(node["sql"], "select * from test_pipe limit 10")
        self.assertEqual(node["dependencies"], ["test_pipe"])
        self.assertEqual(node["materialized"], None)

        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)
        response = await self.fetch_async("/v0/sql?q=select+count()+c+from+test_pipe2+format+JSON&token=%s" % token)
        self.assertEqual(response.code, 400)
        # The SQL endpoint should return a better error when accessing it as ADMIN.
        # res = json.loads(response.body)
        # self.assertEqual(res['error'], 'Pipe does not have an endpoint yet')

        await self._make_endpoint("test_pipe2", node["name"], token_name="test_create_pipe_params_2")

        response = await self.fetch_async(f"/v0/sql?q=select+count()+c+from+test_pipe2+format+JSON&token={token}")
        res = json.loads(response.body)
        row = res["data"][0]
        self.assertEqual(int(row["c"]), 6)

    def test_pipe_query_with_defined_params_not_provided_raises_custom_error(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
        }

        data = {
            "name": "pipe_name",
            "nodes": [
                {
                    "sql": """%
                        {% if not defined(x) %}
                            {{ error('x (Int32) query param is required') }}
                        {% end %}
                        SELECT * FROM test_table WHERE a = {{Int32(x)}}
                    """,
                    "name": "node_00",
                }
            ],
        }

        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        node_id = json.loads(response.body)["nodes"][0]["id"]
        response = self.fetch(
            f"/v0/pipes/pipe_name/nodes/{node_id}/endpoint?{urlencode(params)}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        response = self.fetch("/v0/sql?q=select+count()+c+from+pipe_name+format+JSON&token=%s" % token)
        self.assertEqual(response.code, 400)
        result = json.loads(response.body)
        self.assertEqual(result["error"], "x (Int32) query param is required", response.body)

        params = {
            "pipeline": "pipe_name",
            "token": token,
        }
        response = self.fetch(
            f"/v0/sql?{urlencode(params)}",
            method="POST",
            body="SELECT * FROM pipe_name Format JSON",
            headers={"Content-type": "text/plain"},
        )

        self.assertEqual(response.code, 400)
        result = json.loads(response.body)
        self.assertEqual(result["error"], "x (Int32) query param is required", response.body)

        response = self.fetch(
            f"/v0/sql?{urlencode(params)}",
            method="POST",
            body=json.dumps({"q": "SELECT * FROM pipe_name Format JSON"}),
            headers={"Content-type": "application/json"},
        )

        self.assertEqual(response.code, 400)
        result = json.loads(response.body)
        self.assertEqual(result["error"], "x (Int32) query param is required", response.body)

    def test_pipe_query_required_params_not_provided_raises_error(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
        }

        data = {
            "name": "pipe_name",
            "nodes": [
                {
                    "sql": """%
                        SELECT * FROM test_table WHERE a = {{Int32(x, required=True)}}
                    """,
                    "name": "node_00",
                }
            ],
        }

        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        node_id = json.loads(response.body)["nodes"][0]["id"]
        response = self.fetch(
            f"/v0/pipes/pipe_name/nodes/{node_id}/endpoint?{urlencode(params)}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        response = self.fetch("/v0/sql?q=select+count()+c+from+pipe_name+format+JSON&token=%s" % token)
        self.assertEqual(response.code, 400)
        result = json.loads(response.body)
        self.assertIn("Template Syntax Error: Required parameter is not defined", result.get("error"))

        params = {
            "token": token,
        }
        response = self.fetch(
            f"/v0/sql?{urlencode(params)}",
            method="POST",
            body="SELECT * FROM pipe_name Format JSON",
            headers={"Content-Type": "text/plain"},
        )

        self.assertEqual(response.code, 400)
        result = json.loads(response.body)
        self.assertIn("Template Syntax Error: Required parameter is not defined", result.get("error"))

        response = self.fetch(
            f"/v0/sql?{urlencode(params)}",
            method="POST",
            headers={"Content-Type": "application/json"},
            body=json.dumps(
                {
                    "q": "SELECT * FROM pipe_name Format JSON",
                }
            ),
        )

        self.assertEqual(response.code, 400)
        result = json.loads(response.body)
        self.assertIn("Template Syntax Error: Required parameter is not defined", result.get("error"))

    def test_pipe_query_with_params_substituted_from_default(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
        }

        data = {
            "name": "pipe_name",
            "nodes": [
                {
                    "sql": """%
                        SELECT * FROM test_table WHERE a = {{Int32(x, 1)}}
                    """,
                    "name": "node_00",
                }
            ],
        }

        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        node_id = json.loads(response.body)["nodes"][0]["id"]
        response = self.fetch(
            f"/v0/pipes/pipe_name/nodes/{node_id}/endpoint?{urlencode(params)}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        response = self.fetch("/v0/sql?q=select+*+from+pipe_name+format+JSON&token=%s&x=2" % token)
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertEqual(result["data"][0], {"a": 2, "b": 2, "c": "two"})
        params = {
            "pipeline": "pipe_name",
            "x": 2,
            "token": token,
        }
        response = self.fetch(
            f"/v0/sql?{urlencode(params)}",
            method="POST",
            body="SELECT * FROM pipe_name Format JSON",
            headers={"Content-Type": "text/plain"},
        )
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertEqual(result["data"][0], {"a": 2, "b": 2, "c": "two"})

        # custom variables passed in the request body instead of as query parameters
        body = {"x": 2, "q": "SELECT * FROM _ Format JSON"}
        params = {
            "pipeline": "pipe_name",
            "token": token,
        }
        response = self.fetch(
            f"/v0/sql?{urlencode(params)}",
            method="POST",
            body=json.dumps(body),
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertEqual(result["data"][0], {"a": 2, "b": 2, "c": "two"})

    def test_pipe_query_with_defined_params_provided(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
        }

        data = {
            "name": "pipe_name",
            "nodes": [
                {
                    "sql": """%
                        {% if not defined(x) %}
                            {{ error('x (Int32) query param is required') }}
                        {% end %}
                        SELECT * FROM test_table WHERE a = {{Int32(x)}}
                    """,
                    "name": "node_00",
                }
            ],
        }

        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        node_id = json.loads(response.body)["nodes"][0]["id"]
        response = self.fetch(
            f"/v0/pipes/pipe_name/nodes/{node_id}/endpoint?{urlencode(params)}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        response = self.fetch("/v0/sql?q=select+count()+c+from+pipe_name+format+JSON&token=%s&x=1" % token)
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertEqual(result["data"][0], {"c": 1})

        params = {
            "pipeline": "pipe_name",
            "x": 1,
            "token": token,
        }
        response = self.fetch(
            f"/v0/sql?{urlencode(params)}",
            method="POST",
            body="SELECT * FROM pipe_name Format JSON",
            headers={"Content-Type": "text/plain"},
        )
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertEqual(result["data"][0], {"a": 1, "b": 1, "c": "one"})

        # custom variables passed in the request body instead of as query parameters
        body = {"x": 1, "q": "SELECT * FROM pipe_name Format JSON"}

        params = {
            "pipeline": "pipe_name",
            "token": token,
        }
        response = self.fetch(
            f"/v0/sql?{urlencode(params)}",
            method="POST",
            body=json.dumps(body),
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertEqual(result["data"][0], {"a": 1, "b": 1, "c": "one"})

    def test_pipe_query_without_required_params_from_ui_does_not_raise_custom_error(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
        }

        data = {
            "name": "pipe_name",
            "nodes": [
                {
                    "sql": """%
                        {% if not defined(x) %}
                            {{ error('x (String) query param is required') }}
                        {% end %}
                        SELECT * FROM test_table WHERE c = {{String(x)}}
                    """,
                    "name": "node_00",
                }
            ],
        }

        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        node_id = json.loads(response.body)["nodes"][0]["id"]
        response = self.fetch(
            f"/v0/pipes/pipe_name/nodes/{node_id}/endpoint?{urlencode(params)}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        sql = """%select * from ({% if not defined(x) %} {{ error('x (String) query param is required') }} {% end %} SELECT * FROM test_table WHERE c = {{String(x)}}) format JSON"""
        params = {"token": token, "q": sql, "pipeline": "pipe_name", "from": "ui"}
        response = self.fetch(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertEqual(result["data"], [])

        params = {"token": token, "pipeline": "pipe_name", "from": "ui"}
        response = self.fetch(
            f"/v0/sql?{urlencode(params)}", method="POST", body=sql, headers={"Content-Type": "text/plain"}
        )
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertEqual(result["data"], [])

        body = {
            "q": sql,
        }
        response = self.fetch(
            f"/v0/sql?{urlencode(params)}",
            method="POST",
            body=json.dumps(body),
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertEqual(result["data"], [])

    def test_pipe_query_without_required_params_raises_custom_error(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
        }

        data = {
            "name": "pipe_name",
            "nodes": [
                {
                    "sql": """%
                        {% if not defined(x) %}
                            {{ error('x (String) query param is required') }}
                        {% end %}
                        SELECT * FROM test_table WHERE c = {{String(x)}}
                    """,
                    "name": "node_00",
                }
            ],
        }

        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        node_id = json.loads(response.body)["nodes"][0]["id"]
        response = self.fetch(
            f"/v0/pipes/pipe_name/nodes/{node_id}/endpoint?{urlencode(params)}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        sql = """%select * from _ format JSON"""
        params = {
            "token": token,
            "q": sql,
            "pipeline": "pipe_name",
        }
        response = self.fetch(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400)
        result = json.loads(response.body)
        self.assertEqual(result["error"], "x (String) query param is required", response.body)

        response = self.fetch(
            f"/v0/sql?{urlencode(params)}", method="POST", body=sql, headers={"Content-Type": "text/plain"}
        )
        self.assertEqual(response.code, 400)
        result = json.loads(response.body)
        self.assertEqual(result["error"], "x (String) query param is required", response.body)

        body = {
            "q": sql,
        }

        params = {
            "token": token,
            "pipeline": "pipe_name",
        }
        response = self.fetch(
            f"/v0/sql?{urlencode(params)}",
            method="POST",
            body=json.dumps(body),
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(response.code, 400)
        result = json.loads(response.body)
        self.assertEqual(result["error"], "x (String) query param is required", response.body)

    def test_pipe_query_without_required_params_from_ui_does_not_raise_error_with_FF_set_to_false_then_true(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
        }

        data = {
            "name": "pipe_name",
            "nodes": [
                {
                    "sql": """%
                        {% if not defined(x) %}
                            {{ error('x (String) query param is required') }}
                        {% end %}
                        SELECT * FROM test_table WHERE c = {{String(x)}}
                    """,
                    "name": "node_00",
                }
            ],
        }

        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        node_id = json.loads(response.body)["nodes"][0]["id"]
        response = self.fetch(
            f"/v0/pipes/pipe_name/nodes/{node_id}/endpoint?{urlencode(params)}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        sql = "select * from pipe_name FORMAT JSON"
        params = {"token": token, "q": sql, "pipeline": "pipe_name", "from": "ui"}
        response = self.fetch(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertEqual(result["data"], [])

        params = {"token": token, "pipeline": "pipe_name", "from": "ui"}
        response = self.fetch(
            f"/v0/sql?{urlencode(params)}", method="POST", body=sql, headers={"Content-type": "text/plain"}
        )
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertEqual(result["data"], [])

        body = {"q": sql}
        response = self.fetch(
            f"/v0/sql?{urlencode(params)}",
            method="POST",
            body=json.dumps(body),
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertEqual(result["data"], [])

    def test_pipe_query_with_params_provided(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
        }

        data = {
            "name": "pipe_name",
            "nodes": [
                {
                    "sql": """%
                        {% if not defined(x) %}
                            {{ error('x (Int32) query param is required') }}
                        {% end %}
                        SELECT * FROM test_table WHERE a = {{Int32(x)}}
                    """,
                    "name": "node_00",
                }
            ],
        }

        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        node_id = json.loads(response.body)["nodes"][0]["id"]
        response = self.fetch(
            f"/v0/pipes/pipe_name/nodes/{node_id}/endpoint?{urlencode(params)}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        sql = "select * from pipe_name format JSON"
        params = {"token": token, "q": sql, "pipeline": "pipe_name", "from": "ui", "x": 2}
        response = self.fetch(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertEqual(result["data"][0], {"a": 2, "b": 2, "c": "two"})

        params = {"token": token, "pipeline": "pipe_name", "from": "ui", "x": 2}
        # query string passed as text
        response = self.fetch(
            f"/v0/sql?{urlencode(params)}", method="POST", body=sql, headers={"Content-Type": "text/plain"}
        )
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertEqual(result["data"][0], {"a": 2, "b": 2, "c": "two"})

        # custom variables passed in the request body instead of as query parameters
        body = {"q": sql, "x": 2}
        response = self.fetch(
            f"/v0/sql?{urlencode(params)}",
            method="POST",
            body=json.dumps(body),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertEqual(result["data"][0], {"a": 2, "b": 2, "c": "two"})

    def test_pipe_query_with_substituted_params_provided(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
        }

        data = {
            "name": "pipe_name",
            "nodes": [
                {
                    "sql": """%
                        SELECT * FROM test_table WHERE a = {{Int32(x, 1)}}
                    """,
                    "name": "node_00",
                }
            ],
        }

        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        node_id = json.loads(response.body)["nodes"][0]["id"]
        response = self.fetch(
            f"/v0/pipes/pipe_name/nodes/{node_id}/endpoint?{urlencode(params)}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        sql = "SELECT * FROM _ format JSON"
        params = {"token": token, "q": sql, "pipeline": "pipe_name", "from": "ui", "x": 2}
        response = self.fetch(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertEqual(result["data"][0], {"a": 2, "b": 2, "c": "two"})

    def test_pipe_query_with_default_params_provided(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
        }

        data = {
            "name": "pipe_name",
            "nodes": [
                {
                    "sql": """%
                        SELECT * FROM test_table WHERE a = {{Int32(x, 2)}}
                    """,
                    "name": "node_00",
                }
            ],
        }

        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        node_id = json.loads(response.body)["nodes"][0]["id"]
        response = self.fetch(
            f"/v0/pipes/pipe_name/nodes/{node_id}/endpoint?{urlencode(params)}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        sql = "select * from pipe_name format JSON"
        params = {
            "token": token,
            "q": sql,
            "pipeline": "pipe_name",
            "from": "ui",
        }
        response = self.fetch(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertEqual(result["data"][0], {"a": 2, "b": 2, "c": "two"})

        params = {
            "token": token,
            "pipeline": "pipe_name",
            "from": "ui",
        }
        response = self.fetch(
            f"/v0/sql?{urlencode(params)}", method="POST", body=sql, headers={"Content-Type": "text/plain"}
        )
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertEqual(result["data"][0], {"a": 2, "b": 2, "c": "two"})

        body = {
            "q": sql,
        }
        response = self.fetch(
            f"/v0/sql?{urlencode(params)}",
            method="POST",
            body=json.dumps(body),
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertEqual(result["data"][0], {"a": 2, "b": 2, "c": "two"})

    def test_pipe_query_with_multiple_params(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
        }

        data = {
            "name": "pipe_name",
            "nodes": [
                {
                    "sql": """%
                        SELECT * FROM test_table WHERE a = {{Int32(x, 2)}} OR b = {{Int32(b)}} OR c = {{String(c)}}
                    """,
                    "name": "node_00",
                }
            ],
        }

        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        node_id = json.loads(response.body)["nodes"][0]["id"]
        response = self.fetch(
            f"/v0/pipes/pipe_name/nodes/{node_id}/endpoint?{urlencode(params)}",
            method="POST",
            body=b"",
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        sql = "select * from pipe_name format JSON"
        params = {
            "token": token,
            "q": sql,
            "pipeline": "pipe_name",
            "b": 3,
            "c": "one",
        }
        response = self.fetch(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertEqual(result["data"][0], {"a": 1, "b": 1, "c": "one"})
        self.assertEqual(result["data"][1], {"a": 2, "b": 2, "c": "two"})
        self.assertEqual(result["data"][2], {"a": 3, "b": 3, "c": "three"})

        params = {
            "token": token,
            "pipeline": "pipe_name",
            "b": 3,
            "c": "one",
        }

        response = self.fetch(
            f"/v0/sql?{urlencode(params)}", method="POST", body=sql, headers={"Content-Type": "text/plain"}
        )
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertEqual(result["data"][0], {"a": 1, "b": 1, "c": "one"})
        self.assertEqual(result["data"][1], {"a": 2, "b": 2, "c": "two"})
        self.assertEqual(result["data"][2], {"a": 3, "b": 3, "c": "three"})

        params = {
            "token": token,
            "pipeline": "pipe_name",
        }
        # custom variables passed in the request body instead of as query parameters
        body = {
            "q": sql,
            "b": 3,
            "c": "one",
        }
        response = self.fetch(
            f"/v0/sql?{urlencode(params)}",
            method="POST",
            body=json.dumps(body),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertEqual(result["data"][0], {"a": 1, "b": 1, "c": "one"})
        self.assertEqual(result["data"][1], {"a": 2, "b": 2, "c": "two"})
        self.assertEqual(result["data"][2], {"a": 3, "b": 3, "c": "three"})

    def test_query_as_post_sql_given_as_json_text(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
        }

        data = {
            "name": "pipe_name",
            "nodes": [
                {
                    "sql": """%
                        SELECT * FROM test_table WHERE a = {{Int32(x, 1)}}
                    """,
                    "name": "node_00",
                }
            ],
        }

        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        node_id = json.loads(response.body)["nodes"][0]["id"]
        response = self.fetch(
            f"/v0/pipes/pipe_name/nodes/{node_id}/endpoint?{urlencode(params)}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        params = {
            "pipeline": "pipe_name",
            "token": token,
        }
        response = self.fetch(
            f"/v0/sql?{urlencode(params)}",
            method="POST",
            body='{"q":"%SELECT * FROM test_table WHERE a = {{Int32(x, 1)}} FORMAT JSON","x":2}',
            headers={"Content-Type": "text/plain"},
        )
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertEqual(result["data"][0], {"a": 2, "b": 2, "c": "two"})

    def test_pipe_query_with_array_with_default_params(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_pipe_query_array_params"

        params = {
            "token": token,
        }

        data = {
            "name": pipe_name,
            "nodes": [
                {
                    "sql": """%
                        SELECT * FROM test_table
                        WHERE 1=1
                        {% if not defined(x) %}
                            AND 'a' in {{Array(x, 'String', [default])}}
                        {% end %}
                    """,
                    "name": "node_00",
                    "type": "endpoint",
                }
            ],
        }

        response = self.fetch(
            f"/v0/pipes?{urlencode(params)}",
            method="POST",
            body=json.dumps(data),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        params = {"token": token, "default": "b"}

        response = self.fetch(
            f"/v0/pipes/{pipe_name}.json?{urlencode(params)}", headers={"Content-type": "application/json"}
        )
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        self.assertTrue(len(result.get("data")) == 0)

        params = {"token": token, "default": "a"}

        response = self.fetch(
            f"/v0/pipes/{pipe_name}.json?{urlencode(params)}", headers={"Content-type": "application/json"}
        )
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        self.assertTrue(len(result.get("data")) > 0)

    def test_no_endpoint_error(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        pipe = Users.get_pipe(u, "test_pipe")
        token = Users.add_token(u, "test_no_endpoint_error", scopes.PIPES_READ, pipe.id)
        response = self.fetch(f"/v0/sql?q=select+count()+c+from+test_pipe+format+JSON&token={token}")
        self.assertEqual(response.code, 400)
        payload = json.loads(response.body)
        self.assertEqual(payload["error"], f"The pipe '{pipe.name}' does not have an endpoint yet")

    def test_pipe_query_given_params_output_format_json_quote_denormals(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        pipe = Users.get_pipe(u, "test_pipe")
        token = Users.add_token(u, "test_no_endpoint_error", scopes.PIPES_READ, pipe.id)
        output_format_json_quote_denormals = 1
        response = self.fetch(
            f"/v0/sql?q=select+1/0,0/0,NULL+format+JSON&token={token}&output_format_json_quote_denormals={output_format_json_quote_denormals}"
        )
        self.assertEqual(response.code, 200)
        payload = json.loads(response.body)
        self.assertEqual(payload["data"][0]["divide(1, 0)"], "inf")
        self.assertEqual(payload["data"][0]["divide(0, 0)"], "-nan")
        self.assertEqual(payload["data"][0]["NULL"], None)

    def test_pipe_query_given_params_output_format_json_quote_denormals_through_post(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        pipe = Users.get_pipe(u, "test_pipe")
        token = Users.add_token(u, "test_no_endpoint_error", scopes.PIPES_READ, pipe.id)
        output_format_json_quote_denormals = 1
        response = self.fetch(
            path=f"/v0/sql?token={token}&output_format_json_quote_denormals={output_format_json_quote_denormals}",
            method="POST",
            body="select 1/0, 0/0, NULL format JSON",
        )
        self.assertEqual(response.code, 200)
        payload = json.loads(response.body)
        self.assertEqual(payload["data"][0]["divide(1, 0)"], "inf")
        self.assertEqual(payload["data"][0]["divide(0, 0)"], "-nan")
        self.assertEqual(payload["data"][0]["NULL"], None)

    def test_pipe_query_given_invalid_params_output_format_json_quote_denormals(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        pipe = Users.get_pipe(u, "test_pipe")
        token = Users.add_token(u, "test_no_endpoint_error", scopes.PIPES_READ, pipe.id)
        output_format_json_quote_denormals = "true"
        response = self.fetch(
            f"/v0/sql?q=select+1/0,0/0,NULL+format+JSON&token={token}&output_format_json_quote_denormals={output_format_json_quote_denormals}"
        )
        self.assertEqual(response.code, 400)
        payload = json.loads(response.body)
        self.assertEqual(payload["error"], "output_format_json_quote_denormals must be an integer value")

    def test_pipe_query_without_params_output_format_json_quote_denormals(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        pipe = Users.get_pipe(u, "test_pipe")
        token = Users.add_token(u, "test_no_endpoint_error", scopes.PIPES_READ, pipe.id)
        response = self.fetch(f"/v0/sql?q=select+1/0,0/0,NULL+format+JSON&token={token}")
        self.assertEqual(response.code, 200)
        payload = json.loads(response.body)
        self.assertEqual(payload["data"][0]["divide(1, 0)"], None)
        self.assertEqual(payload["data"][0]["divide(0, 0)"], None)
        self.assertEqual(payload["data"][0]["NULL"], None)

    @tornado.testing.gen_test
    async def test_create_pipe_copy_from_non_accesible_pipe(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.PIPES_CREATE)
        await self._make_endpoint(
            "test_pipe", token_name="test_create_pipe_copy_from_non_accesible_pipe"
        )  # make test_pipe available for other pipes
        response = await self.fetch_async(
            f"/v0/pipes?token={token}&name=copy_pipe&from=test_pipe", method="POST", body=""
        )

        self.assertEqual(response.code, 403)
        res = json.loads(response.body)
        self.assertEqual(res["error"], "token has no READ scope for test_pipe")

    @tornado.testing.gen_test
    async def test_create_pipe_copy(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        test_pipe = Users.get_pipe(u, "test_pipe")
        token = Users.add_token(u, "test", scopes.PIPES_CREATE)
        Users.add_scope_to_token(u, token, scopes.PIPES_READ, test_pipe.id)
        await self._make_endpoint(
            "test_pipe", token_name="test_create_pipe_copy"
        )  # make test_pipe available for other pipes
        response = await self.fetch_async(
            f"/v0/pipes?token={token}&name=copy_pipe&from=test_pipe", method="POST", body=""
        )

        self.assertEqual(response.code, 200)
        res = json.loads(response.body)

        for x in ["id", "name", "nodes", "parent"]:
            self.assertIn(x, res)
            self.assertIsNotNone(res[x], x)

        self.assertEqual(res["parent"], test_pipe.id)

        token = Users.add_token(u, "test_2", scopes.PIPES_CREATE)

        test_pipe = test_pipe.to_json()
        self.assertEqual(len(res["nodes"]), len(test_pipe["nodes"]))
        for i, node in enumerate(res["nodes"]):
            test_node = test_pipe["nodes"][i]
            self.assertEqual(node["name"], test_node["name"])
            self.assertEqual(node["sql"], test_node["sql"])
            self.assertEqual(node["description"], test_node["description"])
            self.assertEqual(node["dependencies"], test_node["dependencies"])
            self.assertEqual(node["ignore_sql_errors"], test_node["ignore_sql_errors"])
            self.assertEqual(node["cluster"], None)
            self.assertNotEqual(node["id"], test_node["id"])

    @tornado.testing.gen_test
    async def test_create_pipe_copy_from_materialized_view(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test_copy_materialized", scopes.ADMIN)

        test_materialized_pipe_name = "test_copy_materialized_pipe_name"
        test_materialized_pipe_copy_name = f"{test_materialized_pipe_name}_copy"

        test_ds_name = "test_copy_materialized_ds_name"
        test_ds = Users.add_datasource_sync(u, test_ds_name)
        create_test_datasource(u, test_ds)

        response = await self.fetch_async(
            f"/v0/pipes?token={token}",
            method="POST",
            body=json.dumps(
                {
                    "name": test_materialized_pipe_name,
                    "nodes": [
                        {
                            "name": "node_00",
                            "sql": f"select * from {test_ds.name}",
                            "id": "foo",
                            "datasource": f"{test_ds_name}_mv",
                            "type": "materialized",
                        }
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200)

        response = await self.fetch_async(
            f"/v0/pipes?token={token}&name={test_materialized_pipe_copy_name}&from={test_materialized_pipe_name}",
            method="POST",
            body="",
        )

        self.assertEqual(response.code, 200)
        res = json.loads(response.body)

        for x in ["id", "name", "nodes", "parent"]:
            self.assertIn(x, res)
            self.assertIsNotNone(res[x], x)

        test_pipe_copy = Users.get_pipe(u, test_materialized_pipe_copy_name)
        test_pipe = Users.get_pipe(u, test_materialized_pipe_name)
        test_pipe_copy = test_pipe_copy.to_json()
        test_pipe = test_pipe.to_json()

        for i, node in enumerate(test_pipe["nodes"]):
            node_copy = test_pipe_copy["nodes"][i]
            self.assertEqual(node["name"], node_copy["name"])
            self.assertEqual(node["sql"], node_copy["sql"])
            self.assertEqual(node["description"], node_copy["description"])
            self.assertEqual(node["dependencies"], node_copy["dependencies"])
            self.assertEqual(node["ignore_sql_errors"], node_copy["ignore_sql_errors"])
            self.assertIsNone(node_copy["materialized"])
            self.assertIsNotNone(node["materialized"])
            self.assertTrue(node["cluster"] in ["tinybird"])
            self.assertNotEqual(node["id"], node_copy["id"])

    def test_create_pipe_copy_with_wrong_sql_in_node(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        test_name = "test_create_pipe_copy_with_wrong_sql_in_node"
        test_ds_name = f"{test_name}_test_ds"
        test_pipe_name = f"{test_name}_pipe"
        token = Users.add_token(u, f"{test_name}_token_sql", scopes.ADMIN, self.USER_ID)
        test_ds = Users.add_datasource_sync(u, test_ds_name)
        create_test_datasource(u, test_ds)
        test_pipe = Users.add_pipe_sync(u, test_pipe_name, f"select * from {test_ds_name}")

        try:
            node = test_pipe.pipeline.nodes[0]
            response = self.fetch(
                f"/v0/pipes/{test_pipe_name}/nodes/{node.id}?token={token}&ignore_sql_errors=true",
                method="PUT",
                body=node.sql,
            )
            self.assertEqual(response.code, 200)

            token = Users.add_token(u, f"{test_name}_token_pipes", scopes.PIPES_CREATE)
            Users.add_scope_to_token(u, token, scopes.PIPES_READ, test_pipe.id)
            response = self.fetch(
                f"/v0/pipes?token={token}&name=copy_pipe&from={test_pipe_name}&ignore_sql_errors=true",
                method="POST",
                body="",
            )
            self.assertEqual(response.code, 200)
            res = json.loads(response.body)

            def _check_response(res, test_pipe):
                for x in ["id", "name", "nodes", "parent"]:
                    self.assertIn(x, res)
                    self.assertIsNotNone(res[x], x)

                self.assertEqual(res["parent"], test_pipe.id)

                test_pipe = test_pipe.to_json()
                self.assertEqual(len(res["nodes"]), len(test_pipe["nodes"]))
                for i, node in enumerate(res["nodes"]):
                    test_node = test_pipe["nodes"][i]
                    self.assertEqual(node["name"], test_node["name"])
                    self.assertEqual(node["sql"], test_node["sql"])
                    self.assertEqual(node["description"], test_node["description"])
                    self.assertEqual(node["ignore_sql_errors"], True)
                    self.assertNotEqual(node["id"], test_node["id"])

            _check_response(res, test_pipe)

            Users.add_scope_to_token(u, token, scopes.PIPES_READ, res["id"])
            response = self.fetch(f"/v0/pipes/{res['id']}?token={token}", method="GET")
            self.assertEqual(response.code, 200)
            res = json.loads(response.body)

            _check_response(res, test_pipe)
        finally:
            Users.drop_pipe(u, test_pipe_name)
            drop_test_datasource(u, test_ds)

    @tornado.testing.gen_test
    async def test_create_pipe_body(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.PIPES_CREATE)
        await self._make_endpoint(
            "test_pipe", token_name="test_create_pipe_body_1"
        )  # make test_pipe available for other pipes
        response = await self.fetch_async(
            f"/v0/pipes?token={token}",
            method="POST",
            body=json.dumps(
                {
                    "name": "pipe3",
                    "description": "my first pipe",
                    "nodes": [
                        {"sql": "select * from test_pipe limit 1", "name": "node_00", "description": "sampled data"},
                        {"sql": "select count() from node_00", "name": "node_01"},
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        res = json.loads(response.body)
        for x in ["id", "name", "nodes"]:
            self.assertIn(x, res)
            self.assertIsNotNone(res[x], x)

        self.assertIn("parent", res)
        self.assertIsNone(res["parent"])
        self.assertEqual(res["name"], "pipe3")
        self.assertEqual(res["description"], "my first pipe")

        self.assertEqual(len(res["nodes"]), 2)
        node = res["nodes"][0]
        self.assertEqual(node["name"], "node_00")
        self.assertEqual(node["sql"], "select * from test_pipe limit 1")
        self.assertEqual(node["description"], "sampled data")
        self.assertEqual(node["dependencies"], ["test_pipe"])
        self.assertEqual(node["materialized"], None)
        self.assertEqual(node["node_type"], "standard")

        token = Users.add_token(u, "test_2", scopes.ADMIN)
        response = await self.fetch_async(f"/v0/sql?q=select+count()+c+from+pipe3+format+JSON&token={token}")
        self.assertEqual(response.code, 400)
        # The SQL endpoint should return a better error when using an ADMIN token.
        res = json.loads(response.body)
        self.assertEqual(res["error"], "The pipe 'pipe3' does not have an endpoint yet")

        await self._make_endpoint("pipe3", "node_00", token_name="test_create_pipe_body")

        response = await self.fetch_async(f"/v0/sql?q=select+count()+c+from+pipe3+format+JSON&token={token}")
        res = json.loads(response.body)
        row = res["data"][0]
        self.assertEqual(int(row["c"]), 1)

    @tornado.testing.gen_test
    async def test_create_pipe_body_with_node_as_endpoint(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.PIPES_CREATE)
        await self._make_endpoint(
            "test_pipe", token_name="test_create_pipe_body_1"
        )  # make test_pipe available for other pipes
        response = await self.fetch_async(
            f"/v0/pipes?token={token}",
            method="POST",
            body=json.dumps(
                {
                    "name": "pipe3",
                    "description": "my first pipe",
                    "nodes": [
                        {"sql": "select * from test_pipe limit 1", "name": "node_00", "description": "sampled data"},
                        {"sql": "select count() from node_00", "name": "node_01", "type": "endpoint"},
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        res = json.loads(response.body)
        for x in ["id", "name", "nodes"]:
            self.assertIn(x, res)
            self.assertIsNotNone(res[x], x)

        self.assertIn("parent", res)
        self.assertIsNone(res["parent"])
        self.assertEqual(res["name"], "pipe3")
        self.assertEqual(res["description"], "my first pipe")

        self.assertEqual(len(res["nodes"]), 2)
        node = res["nodes"][0]
        self.assertEqual(node["name"], "node_00")
        self.assertEqual(node["sql"], "select * from test_pipe limit 1")
        self.assertEqual(node["description"], "sampled data")
        self.assertEqual(node["dependencies"], ["test_pipe"])
        self.assertEqual(node["materialized"], None)
        self.assertEqual(node["node_type"], "standard")
        node = res["nodes"][1]
        self.assertEqual(node["name"], "node_01")
        self.assertEqual(node["sql"], "select count() from node_00")
        self.assertEqual(node["materialized"], None)
        self.assertEqual(node["node_type"], "endpoint")
        token = Users.add_token(u, "test_2", scopes.ADMIN)
        response = await self.fetch_async(f"/v0/sql?q=select+count()+c+from+pipe3+format+JSON&token={token}")
        self.assertEqual(response.code, 200)

    @tornado.testing.gen_test
    async def test_create_pipe_body_with_multiple_nodes(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.PIPES_CREATE)
        pipe_name = "pipe3"
        response = await self.fetch_async(
            f"/v0/pipes?token={token}",
            method="POST",
            body=json.dumps(
                {
                    "name": pipe_name,
                    "description": "my first pipe",
                    "nodes": [
                        {"sql": "select * from numbers(10)", "name": "node_00", "description": "sampled data"},
                        {"sql": "select count() from node_00", "name": "node_01", "type": "endpoint"},
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        res = json.loads(response.body)
        for x in ["id", "name", "nodes"]:
            self.assertIn(x, res)
            self.assertIsNotNone(res[x], x)

        self.assertIn("parent", res)
        self.assertIsNone(res["parent"])
        self.assertEqual(res["name"], pipe_name)
        self.assertEqual(res["description"], "my first pipe")

        self.assertEqual(len(res["nodes"]), 2)
        node = res["nodes"][0]
        self.assertEqual(node["name"], "node_00")
        self.assertEqual(node["sql"], "select * from numbers(10)")
        self.assertEqual(node["description"], "sampled data")
        self.assertEqual(node["materialized"], None)
        self.assertEqual(node["node_type"], "standard")
        node = res["nodes"][1]
        self.assertEqual(node["name"], "node_01")
        self.assertEqual(node["sql"], "select count() from node_00")
        self.assertEqual(node["materialized"], None)
        self.assertEqual(node["node_type"], "endpoint")
        await self._make_endpoint(pipe_name, "node_00", token_name="test_create_pipe_body")
        token = Users.add_token(u, "test_2", scopes.ADMIN)
        pipe_res = json.loads((await self.fetch_async(f"/v0/pipes/{pipe_name}?token={token}")).body)
        self.assertEqual(pipe_res["endpoint"], pipe_res["nodes"][0]["name"])
        self.assertEqual(pipe_res["nodes"][0]["node_type"], "endpoint")
        self.assertEqual(pipe_res["nodes"][1]["node_type"], "standard")

    @tornado.testing.gen_test
    async def test_create_pipe_body_with_single_node_as_endpoint(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.PIPES_CREATE)
        await self._make_endpoint(
            "test_pipe", token_name="test_create_pipe_body_1"
        )  # make test_pipe available for other pipes
        response = await self.fetch_async(
            f"/v0/pipes?token={token}",
            method="POST",
            body=json.dumps(
                {
                    "name": "pipe3",
                    "description": "my first pipe",
                    "nodes": [
                        {
                            "sql": "select * from test_pipe limit 1",
                            "name": "node_00",
                            "description": "sampled data",
                            "type": "endpoint",
                        },
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        res = json.loads(response.body)
        for x in ["id", "name", "nodes"]:
            self.assertIn(x, res)
            self.assertIsNotNone(res[x], x)

        self.assertIn("parent", res)
        self.assertIsNone(res["parent"])
        self.assertEqual(res["name"], "pipe3")
        self.assertEqual(res["description"], "my first pipe")

        self.assertEqual(len(res["nodes"]), 1)
        node = res["nodes"][0]
        self.assertEqual(node["name"], "node_00")
        self.assertEqual(node["sql"], "select * from test_pipe limit 1")
        self.assertEqual(node["description"], "sampled data")
        self.assertEqual(node["dependencies"], ["test_pipe"])
        self.assertEqual(node["materialized"], None)
        self.assertEqual(node["node_type"], "endpoint")

    @tornado.testing.gen_test
    async def test_create_pipe_body_with_single_node_as_endpoint_append_node_as_endpoint(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.PIPES_CREATE)
        response = await self.fetch_async(
            f"/v0/pipes?token={token}",
            method="POST",
            body=json.dumps(
                {
                    "name": "pipe3",
                    "description": "my first pipe",
                    "nodes": [
                        {
                            "sql": "select * from numbers(10)",
                            "name": "node_00",
                            "description": "sampled data",
                            "type": "endpoint",
                        }
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        res = json.loads(response.body)
        for x in ["id", "name", "nodes"]:
            self.assertIn(x, res)
            self.assertIsNotNone(res[x], x)

        self.assertIn("parent", res)
        self.assertIsNone(res["parent"])
        self.assertEqual(res["name"], "pipe3")
        self.assertEqual(res["description"], "my first pipe")

        self.assertEqual(len(res["nodes"]), 1)
        node = res["nodes"][0]
        self.assertEqual(node["name"], "node_00")
        self.assertEqual(node["sql"], "select * from numbers(10)")
        self.assertEqual(node["description"], "sampled data")
        self.assertEqual(node["materialized"], None)
        self.assertEqual(node["node_type"], "endpoint")
        pipe_node = await self._append_node(
            "select * from numbers(20)", name="node_01", pipe_name="pipe3", node_type="endpoint"
        )
        self.assertEqual(pipe_node["node_type"], "endpoint")
        token = Users.add_token(u, "test_2", scopes.ADMIN)
        pipe_res = json.loads((await self.fetch_async(f"/v0/pipes/pipe3?token={token}")).body)
        self.assertEqual(pipe_res["endpoint"], pipe_res["nodes"][1]["name"])
        self.assertEqual(pipe_res["nodes"][0]["node_type"], "standard")

    @tornado.testing.gen_test
    async def test_create_pipe_body_with_single_node_then_append_node(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.PIPES_CREATE)
        response = await self.fetch_async(
            f"/v0/pipes?token={token}",
            method="POST",
            body=json.dumps(
                {
                    "name": "pipe3",
                    "description": "my first pipe",
                    "nodes": [{"sql": "select * from numbers(10)", "name": "node_00", "description": "sampled data"}],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        res = json.loads(response.body)
        for x in ["id", "name", "nodes"]:
            self.assertIn(x, res)
            self.assertIsNotNone(res[x], x)

        self.assertIn("parent", res)
        self.assertIsNone(res["parent"])
        self.assertEqual(res["name"], "pipe3")
        self.assertEqual(res["description"], "my first pipe")

        self.assertEqual(len(res["nodes"]), 1)
        node = res["nodes"][0]
        self.assertEqual(node["name"], "node_00")
        self.assertEqual(node["sql"], "select * from numbers(10)")
        self.assertEqual(node["description"], "sampled data")
        self.assertEqual(node["materialized"], None)
        self.assertEqual(node["node_type"], "standard")
        await self._append_node("select * from numbers(20)", name="node_01", pipe_name="pipe3")
        token = Users.add_token(u, "test_2", scopes.ADMIN)
        pipe_res = json.loads((await self.fetch_async(f"/v0/pipes/pipe3?token={token}")).body)
        self.assertEqual(pipe_res["nodes"][0]["node_type"], "standard")
        self.assertEqual(pipe_res["nodes"][1]["node_type"], "standard")
        self.assertEqual(pipe_res["type"], "default")

    @tornado.testing.gen_test
    async def test_create_pipe_body_with_multiple_endpoint_nodes(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.PIPES_CREATE)
        await self._make_endpoint(
            "test_pipe", token_name="test_create_pipe_body_1"
        )  # make test_pipe available for other pipes
        response = await self.fetch_async(
            f"/v0/pipes?token={token}",
            method="POST",
            body=json.dumps(
                {
                    "name": "pipe3",
                    "description": "my first pipe",
                    "nodes": [
                        {"sql": "select * from test_pipe limit 1", "name": "node_00", "description": "sampled data"},
                        {"sql": "select count() from node_00", "name": "node_01", "type": "endpoint"},
                        {"sql": "select count() from node_01", "name": "node_02", "type": "endpoint"},
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 403)
        result = json.loads(response.body)
        self.assertEqual(
            result.get("error"),
            "There is more than one endpoint node. Pipes can only have one output. Set only one node to be an endpoint node and try again.",
        )

    @tornado.testing.gen_test
    async def test_create_pipe_body_no_node_name(self):
        await self._make_endpoint(
            "test_pipe", token_name="test_create_pipe_body_no_node_name"
        )  # make test_pipe available for other pipes
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.PIPES_CREATE)
        response = await self.fetch_async(
            f"/v0/pipes?token={token}",
            method="POST",
            body=json.dumps(
                {
                    "name": "pipe_no_node_name",
                    "nodes": [
                        {"sql": "select * from test_pipe limit 1"},
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200)

        res = json.loads(response.body)
        for x in ["id", "name", "nodes"]:
            self.assertIn(x, res)
            self.assertIsNotNone(res[x], x)
        self.assertEqual(len(res["nodes"]), 1)
        node = res["nodes"][0]
        self.assertEqual(node["name"], "pipe_no_node_name_0")

    @tornado.testing.gen_test
    async def test_create_pipe_body_skips_invalid_keys(self):
        await self._make_endpoint(
            "test_pipe", token_name="test_create_pipe_body_skips_invalid_keys"
        )  # make test_pipe available for other pipes
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.PIPES_CREATE)
        Users.add_scope_to_token(u, token, scopes.DATASOURCES_CREATE)

        ds_name = "test_materialized"

        response = await self.fetch_async(
            f"/v0/pipes?token={token}",
            method="POST",
            body=json.dumps(
                {
                    "name": "pipe_invalid_keys",
                    "nodes": [
                        {
                            "name": "node_00",
                            "sql": "select * from test_pipe",
                            "description": "skip invalid keys",
                            # Skip the following keys
                            "id": "foo",
                            "materialized": "true",  # not necessary, it checks it does not break anything
                            "datasource": ds_name,
                            "type": "materialized",
                            "dependencies": ["foo"],
                            "created_at": "0",
                            "updated_at": "1",
                            "foo": "bar",
                        }
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200)

        res = json.loads(response.body)
        self.assertEqual(len(res["nodes"]), 1)
        node = res["nodes"][0]

        self.assertEqual(node["name"], "node_00")
        self.assertEqual(node["sql"], "select * from test_pipe")
        self.assertEqual(node["description"], "skip invalid keys")
        self.assertEqual(node["dependencies"], ["test_pipe"])
        self.assertEqual(node["node_type"], "materialized")

        # Skipped
        self.assertNotEqual(node["id"], "foo")
        self.assertNotEqual(node["created_at"], "0")
        self.assertNotEqual(node["updated_at"], "1")
        self.assertNotEqual(node.get("foo"), "bar")

        response = await self.fetch_async(f"/v0/datasources/{ds_name}?token={token}")
        self.assertEqual(response.code, 200)
        datasource = json.loads(response.body)
        self.assertEqual(node["materialized"], datasource.get("id"))

    def test_create_pipe_body_name_clash(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.PIPES_CREATE)
        name = "pipe_body_name_clash"
        Users.add_pipe_sync(u, name, "select 1")
        response = self.fetch(
            f"/v0/pipes?token={token}",
            method="POST",
            body=json.dumps({"name": name, "nodes": [{"sql": "select * from test_pipe limit 1"}]}),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 409)
        res = json.loads(response.body)
        self.assertEqual(
            res["error"],
            'There is already a Pipe with name "pipe_body_name_clash". Pipe names must be globally unique',
        )

    def test_create_pipe_body_node_name_clash(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.PIPES_CREATE)

        def pipe_body(node_name):
            return json.dumps(
                {
                    "name": "pipe_with_node_name_clash",
                    "nodes": [{"name": node_name, "sql": "select * from test_pipe limit 1"}],
                }
            )

        response = self.fetch(
            f"/v0/pipes?token={token}",
            method="POST",
            body=pipe_body("test_pipe"),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 400)
        res = json.loads(response.body)
        self.assertEqual(
            res["error"],
            'Error with node at position 0, there is already a Pipe with name "test_pipe". Pipe names must be globally unique',
        )

        response = self.fetch(
            f"/v0/pipes?token={token}",
            method="POST",
            body=pipe_body("test_table"),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 400)
        res = json.loads(response.body)
        self.assertEqual(
            res["error"],
            'Error with node at position 0, there is already a Datasource with name "test_table". Pipe names must be globally unique',
        )

    def test_create_pipe_wrong_body(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.PIPES_CREATE)
        response = self.fetch(
            f"/v0/pipes?token={token}",
            method="POST",
            body=json.dumps(
                {
                    "name": "pipe3",
                    "nodes": [
                        {"sql": "select * from test_pipeasdasd limit 1", "name": "node_00"},
                        {"sql": "select count() from node_00", "name": "node_01"},
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 400)
        result = json.loads(response.body)
        self.assertEqual(result["error"], "Resource 'test_pipeasdasd' not found")

    def test_create_pipe_body_empty_nodes(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.PIPES_CREATE)
        response = self.fetch(
            f"/v0/pipes?token={token}",
            method="POST",
            body=json.dumps({"name": "pipe_no_nodes", "nodes": []}),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)
        pipe = json.loads(response.body)
        self.assertEqual(pipe["nodes"], [])

    @tornado.testing.gen_test
    async def test_create_and_override_materialized_view_from_nodes(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)

        ds_name_source = "ds_create_materialized_view_from_nodes"
        params = {
            "token": token,
            "name": ds_name_source,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        s = StringIO("d,sales\n2019-01-01,2\n2019-01-02,3")
        response = await self.fetch_full_body_upload_async(create_url, s)
        self.assertEqual(response.code, 200, response.body)

        target_ds_name = "mv_create_materialized_view_from_nodes"

        pipe_name = "pipe_materialized_from_nodes"
        response = await self.fetch_async(
            f"/v0/pipes?token={token}",
            method="POST",
            body=json.dumps(
                {
                    "name": pipe_name,
                    "nodes": [
                        {
                            "name": "mv",
                            "type": "materialized",
                            "sql": f"SELECT toDate(d) AS d, sales * 10 AS fake_sales FROM {ds_name_source}",
                            "datasource": target_ds_name,
                            "populate": "true",
                        }
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        pipe_node = result["nodes"][0]
        self.assertEqual(pipe_node["name"], "mv")
        ds = Users.get_datasource(u, target_ds_name)
        result_datasource = result["datasource"]
        self.assertEqual(result_datasource["id"], ds.id)
        self.assertEqual(result_datasource["engine"]["engine"], "MergeTree")
        self.assertIn("job", result)
        job_response = result["job"]
        self.assertEqual(job_response["id"], job_response["job_id"])
        self.assertEqual(job_response["kind"], JobKind.POPULATE)
        await self.get_finalised_job_async(job_response["id"])

        # override matview
        user_name = "test_user_from_nodes"
        new_token = Users.add_token(u, user_name, scopes.ADMIN)
        response = await self.fetch_async(
            f"/v0/pipes?force=true&token={new_token}",
            method="POST",
            body=json.dumps(
                {
                    "name": pipe_name,
                    "nodes": [
                        {
                            "name": "mv",
                            "type": "materialized",
                            "sql": f"SELECT toDate(d) AS d, sales * 11 AS fake_sales FROM {ds_name_source}",
                            "datasource": target_ds_name,
                        }
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)

        # check pipe is edited by new token
        self.assertTrue(user_name in result["edited_by"], f"Should be edited by {user_name}")

        # check existing matview is not dropped, but the sql has changed
        existing_node_id = pipe_node["id"]
        existing_matview = exec_sql(
            u["database"], f"select * from system.tables where name = '{existing_node_id}' FORMAT JSON"
        )
        self.assertEqual(len(existing_matview["data"]), 1, existing_matview)
        self.assertTrue(
            "SELECT toDate(d) AS d, sales * 11 AS fake_sales" in existing_matview["data"][0]["create_table_query"],
            existing_matview,
        )

        # check new matview equals old matview
        new_pipe_node = result["nodes"][0]
        new_node_id = new_pipe_node["id"]
        self.assertEqual(
            existing_node_id, new_node_id, f"New node id {new_node_id} should equal existing {existing_node_id}"
        )

        # check the target datasource which was created on pipe creation was not dropped (i.e. it has data)
        rr = await self.fetch_async(f"/v0/datasources/{target_ds_name}?token={token}")
        self.assertTrue("created_by_pipe" in json.loads(rr.body)["tags"], rr.body)

        async def check():
            ds_not_dropped = await self.fetch_async(
                f"/v0/sql?q=select+count()+c+from+{target_ds_name}+format+JSON&token={token}"
            )
            self.assertEqual(json.loads(ds_not_dropped.body)["rows"], 1, ds_not_dropped.body)

        await poll_async(check)

        redis_pipe = Users.get_pipe(u, pipe_name)
        self.assertEqual(len(redis_pipe.pipeline.nodes), 1, "Pipe should have one node")
        redis_node = redis_pipe.pipeline.nodes[0]
        self.assertTrue(ds_name_source in redis_node.sql, "SQL should contain datasource name")
        self.assertTrue("SELECT toDate(d) AS d, sales * 11" in redis_node.sql, "SQL should contain modified query")
        self.assertTrue(".t_" not in redis_node.sql, "SQL should not leak internal table name")

    @tornado.testing.gen_test
    async def test_create_and_override_materialized_view_with_error(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)

        ds_name_source = "ds_create_materialized_view_with_error"
        params = {
            "token": token,
            "name": ds_name_source,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        s = StringIO("d,sales\n2019-01-01,2\n2019-01-02,3")
        response = await self.fetch_full_body_upload_async(create_url, s)
        self.assertEqual(response.code, 200, response.body)

        target_ds_name = "mv_create_materialized_view_with_error"

        pipe_name = "pipe_materialized_with_error"
        response = await self.fetch_async(
            f"/v0/pipes?token={token}",
            method="POST",
            body=json.dumps(
                {
                    "name": pipe_name,
                    "nodes": [
                        {
                            "name": "mv",
                            "type": "materialized",
                            "sql": f"SELECT toDate(d) AS d, sales * 10 AS fake_sales FROM {ds_name_source}",
                            "datasource": target_ds_name,
                        }
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        pipe_node = result["nodes"][0]
        self.assertEqual(pipe_node["name"], "mv")
        ds = Users.get_datasource(u, target_ds_name)
        result_datasource = result["datasource"]
        self.assertEqual(result_datasource["id"], ds.id)
        self.assertEqual(result_datasource["engine"]["engine"], "MergeTree")

        # override matview with error
        response = await self.fetch_async(
            f"/v0/pipes?force=true&token={token}",
            method="POST",
            body=json.dumps(
                {
                    "name": pipe_name,
                    "nodes": [
                        {
                            "name": "mv",
                            "type": "materialized",
                            "sql": f"SELECT toDate(d) AS d, sales * 11 AS fake_sales, sales FROM {ds_name_source}",
                            "datasource": target_ds_name,
                        }
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 400, response.body)
        result = json.loads(response.body)
        self.assertTrue("error" in result, "Should have returned an error")
        self.assertTrue("sales" in result["error"], "Error should mention the 'sales' column")

        # check existing matview is not dropped, and the sql has not changed
        existing_node_id = pipe_node["id"]
        existing_matview = exec_sql(
            u["database"], f"select * from system.tables where name = '{existing_node_id}' FORMAT JSON"
        )
        self.assertEqual(len(existing_matview["data"]), 1, existing_matview)
        self.assertTrue(
            "SELECT toDate(d) AS d, sales * 10 AS fake_sales" in existing_matview["data"][0]["create_table_query"],
            existing_matview,
        )

        # check the target datasource which was created on pipe creation was not dropped (i.e. it has data)
        rr = await self.fetch_async(f"/v0/datasources/{target_ds_name}?token={token}")
        self.assertTrue("created_by_pipe" in json.loads(rr.body)["tags"], rr.body)

    @tornado.testing.gen_test
    async def test_create_and_override_materialized_view_with_new_name(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)

        ds_name_source = "ds_create_materialized_view_with_new_name"
        params = {
            "token": token,
            "name": ds_name_source,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        s = StringIO("d,sales\n2019-01-01,2\n2019-01-02,3")
        response = await self.fetch_full_body_upload_async(create_url, s)
        self.assertEqual(response.code, 200, response.body)

        target_ds_name = "mv_create_materialized_view_with_new_name"

        pipe_name = "pipe_materialized_with_new_name"
        response = await self.fetch_async(
            f"/v0/pipes?token={token}",
            method="POST",
            body=json.dumps(
                {
                    "name": pipe_name,
                    "nodes": [
                        {
                            "name": "mv",
                            "type": "materialized",
                            "sql": f"SELECT toDate(d) AS d, sales * 10 AS fake_sales FROM {ds_name_source}",
                            "datasource": target_ds_name,
                        },
                        {
                            "name": "node_1",
                            "sql": "SELECT * from mv",
                            "datasource": target_ds_name,
                        },
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        pipe_node = result["nodes"][0]
        self.assertEqual(pipe_node["name"], "mv")
        ds = Users.get_datasource(u, target_ds_name)
        result_datasource = result["datasource"]
        self.assertEqual(result_datasource["id"], ds.id)
        self.assertEqual(result_datasource["engine"]["engine"], "MergeTree")

        # override matview
        response = await self.fetch_async(
            f"/v0/pipes?force=true&token={token}",
            method="POST",
            body=json.dumps(
                {
                    "name": pipe_name,
                    "nodes": [
                        {
                            "name": "renamed_mv",
                            "type": "materialized",
                            "sql": f"SELECT toDate(d) AS d, sales * 11 AS fake_sales FROM {ds_name_source}",
                            "datasource": target_ds_name,
                        },
                        {
                            "name": "node_1",
                            "sql": "SELECT * from renamed_mv",
                            "datasource": target_ds_name,
                        },
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        pipe_node = result["nodes"][0]
        self.assertEqual(pipe_node["name"], "renamed_mv")

        # check existing matview is not dropped, but the sql has changed
        existing_node_id = pipe_node["id"]
        existing_matview = exec_sql(
            u["database"], f"select * from system.tables where name = '{existing_node_id}' FORMAT JSON"
        )
        self.assertEqual(len(existing_matview["data"]), 1, existing_matview)
        self.assertTrue(
            "SELECT toDate(d) AS d, sales * 11 AS fake_sales" in existing_matview["data"][0]["create_table_query"],
            existing_matview,
        )

        # check the target datasource which was created on pipe creation was not be dropped (i.e. it has data)
        rr = await self.fetch_async(f"/v0/datasources/{target_ds_name}?token={token}")
        self.assertTrue("created_by_pipe" in json.loads(rr.body)["tags"], rr.body)

        async def check():
            ds_not_dropped = await self.fetch_async(
                f"/v0/sql?q=select+count()+c+from+{target_ds_name}+format+JSON&token={token}"
            )
            self.assertEqual(json.loads(ds_not_dropped.body)["rows"], 1, ds_not_dropped.body)

        await poll_async(check)

    @tornado.testing.gen_test
    async def test_create_and_override_materialized_view_with_new_datasource(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)

        ds_name_source = "ds_create_materialized_view_with_new_datasource"
        params = {
            "token": token,
            "name": ds_name_source,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        s = StringIO("d,sales\n2019-01-01,2\n2019-01-02,3")
        response = await self.fetch_full_body_upload_async(create_url, s)
        self.assertEqual(response.code, 200, response.body)

        target_ds_name = "mv_create_materialized_view_with_new_datasource"

        pipe_name = "pipe_materialized_with_new_datasource"
        response = await self.fetch_async(
            f"/v0/pipes?token={token}",
            method="POST",
            body=json.dumps(
                {
                    "name": pipe_name,
                    "nodes": [
                        {
                            "name": "mv",
                            "type": "materialized",
                            "sql": f"SELECT toDate(d) AS d, sales * 10 AS fake_sales FROM {ds_name_source}",
                            "datasource": target_ds_name,
                        },
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        pipe_node = result["nodes"][0]
        self.assertEqual(pipe_node["name"], "mv")
        ds = Users.get_datasource(u, target_ds_name)
        result_datasource = result["datasource"]
        self.assertEqual(result_datasource["id"], ds.id)
        self.assertEqual(result_datasource["engine"]["engine"], "MergeTree")

        # override matview
        new_target_ds_name = "mv_create_materialized_view_with_new_datasource_new"
        response = await self.fetch_async(
            f"/v0/pipes?force=true&token={token}",
            method="POST",
            body=json.dumps(
                {
                    "name": pipe_name,
                    "nodes": [
                        {
                            "name": "mv",
                            "type": "materialized",
                            "sql": f"SELECT toDate(d) AS d, sales * 11 AS fake_sales FROM {ds_name_source}",
                            "datasource": new_target_ds_name,
                        },
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)

        # check old matview was dropped it does not exist in CH or the sql has changed
        # TODO: there should be no data loss nor duplication, we are not checking that
        old_node_id = pipe_node["id"]
        old_matview_was_dropped = exec_sql(
            u["database"], f"select * from system.tables where name = '{old_node_id}' FORMAT JSON"
        )
        self.assertEqual(len(old_matview_was_dropped["data"]), 0, old_matview_was_dropped)

        # check there's a new matview with the new query
        result = json.loads(response.body)
        new_pipe_node = result["nodes"][0]
        new_node_id = new_pipe_node["id"]
        new_matview = exec_sql(u["database"], f"select * from system.tables where name = '{new_node_id}' FORMAT JSON")
        self.assertEqual(len(new_matview["data"]), 1, new_matview)
        self.assertTrue(
            "SELECT toDate(d) AS d, sales * 11 AS fake_sales" in new_matview["data"][0]["create_table_query"],
            new_matview,
        )

        # check the target datasource which was created on pipe creation was not be dropped (i.e. it has data)
        rr = await self.fetch_async(f"/v0/datasources/{target_ds_name}?token={token}")
        self.assertTrue("created_by_pipe" in json.loads(rr.body)["tags"], rr.body)

        async def check():
            ds_not_dropped = await self.fetch_async(
                f"/v0/sql?q=select+count()+c+from+{target_ds_name}+format+JSON&token={token}"
            )
            self.assertEqual(json.loads(ds_not_dropped.body)["rows"], 1, ds_not_dropped.body)

        await poll_async(check)

    @tornado.testing.gen_test
    async def test_create_and_override_materialized_view_change_nodes(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)

        ds_name_source = "ds_create_materialized_view_change_nodes"
        params = {
            "token": token,
            "name": ds_name_source,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        s = StringIO("d,sales\n2019-01-01,2\n2019-01-02,3")
        response = await self.fetch_full_body_upload_async(create_url, s)
        self.assertEqual(response.code, 200, response.body)

        target_ds_name = "mv_create_materialized_view_change_nodes"

        pipe_name = "pipe_materialized_change_nodes"
        response = await self.fetch_async(
            f"/v0/pipes?token={token}",
            method="POST",
            body=json.dumps(
                {
                    "name": pipe_name,
                    "nodes": [
                        {
                            "name": "mv",
                            "type": "materialized",
                            "sql": f"SELECT toDate(d) AS d, sales * 10 AS fake_sales FROM {ds_name_source}",
                            "datasource": target_ds_name,
                        },
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        pipe_node = result["nodes"][0]
        self.assertEqual(pipe_node["name"], "mv")
        ds = Users.get_datasource(u, target_ds_name)
        result_datasource = result["datasource"]
        self.assertEqual(result_datasource["id"], ds.id)
        self.assertEqual(result_datasource["engine"]["engine"], "MergeTree")

        async def check_matview_modified(existing_node_id: str, query: str):
            # check existing matview is not dropped, but the sql has changed
            existing_matview = exec_sql(
                u["database"], f"select * from system.tables where name = '{existing_node_id}' FORMAT JSON"
            )
            self.assertEqual(len(existing_matview["data"]), 1, existing_matview)
            self.assertTrue(
                query in existing_matview["data"][0]["create_table_query"],
                existing_matview,
            )

        # override matview with new query and description
        query = "SELECT toDate(d) AS d, sales * 11 AS fake_sales"
        response = await self.fetch_async(
            f"/v0/pipes?force=true&token={token}",
            method="POST",
            body=json.dumps(
                {
                    "name": pipe_name,
                    "nodes": [
                        {
                            "name": "mv",
                            "type": "materialized",
                            "description": "a materialized view",
                            "sql": f"{query} FROM {ds_name_source}",
                            "datasource": target_ds_name,
                        },
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)
        await check_matview_modified(pipe_node["id"], query)

        # override matview with new query and new node
        query = "SELECT toDate(d) AS d, sales * 12 AS fake_sales"
        response = await self.fetch_async(
            f"/v0/pipes?force=true&token={token}",
            method="POST",
            body=json.dumps(
                {
                    "name": pipe_name,
                    "nodes": [
                        {
                            "name": "mv",
                            "type": "materialized",
                            "description": "a materialized view",
                            "sql": f"{query} FROM {ds_name_source}",
                            "datasource": target_ds_name,
                        },
                        {
                            "name": "new_node",
                            "sql": "SELECT * from mv",
                            "datasource": target_ds_name,
                        },
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)
        await check_matview_modified(pipe_node["id"], query)

        # override matview with new nodes
        query = "SELECT toDate(d) AS d, sales * 13 AS fake_sales"
        response = await self.fetch_async(
            f"/v0/pipes?force=true&token={token}",
            method="POST",
            body=json.dumps(
                {
                    "name": pipe_name,
                    "nodes": [
                        {
                            "name": "chain_0",
                            "description": "a materialized view",
                            "sql": f"{query} FROM {ds_name_source}",
                        },
                        {
                            "name": "chain_1",
                            "sql": "SELECT * from chain_0",
                            "datasource": target_ds_name,
                            "type": "materialized",
                        },
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)
        await check_matview_modified(pipe_node["id"], query)

        # override matview with new nodes
        query = "SELECT toDate(d) AS d, sales * 13 AS fake_sales"
        response = await self.fetch_async(
            f"/v0/pipes?force=true&token={token}",
            method="POST",
            body=json.dumps(
                {
                    "name": pipe_name,
                    "nodes": [
                        {
                            "name": "chain_0",
                            "description": "a materialized view",
                            "sql": f"{query} FROM {ds_name_source}",
                        },
                        {
                            "name": "chain_1",
                            "sql": "SELECT * from chain_0",
                            "datasource": target_ds_name,
                            "type": "materialized",
                        },
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)
        await check_matview_modified(pipe_node["id"], query)

    @tornado.testing.gen_test
    async def test_create_and_override_materialized_view_with_ch_errors(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)

        ds_name_source = "ds_create_materialized_view_with_ch_error"
        params = {
            "token": token,
            "name": ds_name_source,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        s = StringIO("d,sales\n2019-01-01,2\n2019-01-02,3")
        response = await self.fetch_full_body_upload_async(create_url, s)
        self.assertEqual(response.code, 200, response.body)

        target_ds_name = "mv_create_materialized_view_with_ch_error"
        original_query = "SELECT toDate(d) AS d, sales * 10 AS fake_sales"

        pipe_name = "pipe_materialized_with_ch_error"
        response = await self.fetch_async(
            f"/v0/pipes?token={token}",
            method="POST",
            body=json.dumps(
                {
                    "name": pipe_name,
                    "nodes": [
                        {
                            "name": "mv",
                            "type": "materialized",
                            "sql": f"{original_query} FROM {ds_name_source}",
                            "datasource": target_ds_name,
                        }
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        pipe_node = result["nodes"][0]
        self.assertEqual(pipe_node["name"], "mv")
        ds = Users.get_datasource(u, target_ds_name)
        result_datasource = result["datasource"]
        self.assertEqual(result_datasource["id"], ds.id)
        self.assertEqual(result_datasource["engine"]["engine"], "MergeTree")
        existing_node_id = pipe_node["id"]

        async def check_existing_matview_not_modified(existing_node_id: str, query: str):
            existing_matview = exec_sql(
                u["database"], f"select * from system.tables where name = '{existing_node_id}' FORMAT JSON"
            )
            self.assertEqual(len(existing_matview["data"]), 1, existing_matview)
            self.assertTrue(query in existing_matview["data"][0]["create_table_query"])

        # override matview with FAKE query
        response = await self.fetch_async(
            f"/v0/pipes?force=true&token={token}&ignore_sql_errors=false",
            method="POST",
            body=json.dumps(
                {
                    "name": pipe_name,
                    "nodes": [
                        {
                            "name": "mv",
                            "type": "materialized",
                            "sql": f"SELECT toDate(d) AS d, sales * 11 AS fake_sales FROM {ds_name_source} FAKE FAKE FAKE",
                            "datasource": target_ds_name,
                        }
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 400, response.body)
        await check_existing_matview_not_modified(existing_node_id, original_query)

        # override matview with UNION ALL
        response = await self.fetch_async(
            f"/v0/pipes?force=true&token={token}&ignore_sql_errors=false",
            method="POST",
            body=json.dumps(
                {
                    "name": pipe_name,
                    "nodes": [
                        {
                            "name": "mv",
                            "type": "materialized",
                            "sql": f"SELECT toDate(d) AS d, sales * 12 AS fake_sales FROM {ds_name_source} UNION ALL SELECT toDate(d) AS d, sales * 13 AS fake_sales FROM {ds_name_source}",
                            "datasource": target_ds_name,
                        }
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 400, response.body)
        await check_existing_matview_not_modified(existing_node_id, original_query)

        # override matview with value error
        with mock.patch(
            "tinybird.views.shared.utils.NodeUtils.validate_node_sql",
            side_effect=ValueError("mock failure"),
        ):
            response = await self.fetch_async(
                f"/v0/pipes?force=true&token={token}&ignore_sql_errors=false",
                method="POST",
                body=json.dumps(
                    {
                        "name": pipe_name,
                        "nodes": [
                            {
                                "name": "mv",
                                "type": "materialized",
                                "sql": f"SELECT toDate(d) AS d, sales * 14 AS fake_sales FROM {ds_name_source}",
                                "datasource": target_ds_name,
                            }
                        ],
                    }
                ),
                headers={"Content-type": "application/json"},
            )
            self.assertEqual(response.code, 400, response.body)
            await check_existing_matview_not_modified(existing_node_id, original_query)

        # override matview with query not allowed error
        with mock.patch(
            "tinybird.views.shared.utils.NodeUtils.validate_node_sql",
            side_effect=QueryNotAllowed("mocked exception"),
        ):
            response = await self.fetch_async(
                f"/v0/pipes?force=true&token={token}&ignore_sql_errors=false",
                method="POST",
                body=json.dumps(
                    {
                        "name": pipe_name,
                        "nodes": [
                            {
                                "name": "mv",
                                "type": "materialized",
                                "sql": f"SELECT toDate(d) AS d, sales * 15 AS fake_sales FROM {ds_name_source}",
                                "datasource": target_ds_name,
                            }
                        ],
                    }
                ),
                headers={"Content-type": "application/json"},
            )
            self.assertEqual(response.code, 400, response.body)
            await check_existing_matview_not_modified(existing_node_id, original_query)

        # override matview with generic CH error
        with mock.patch(
            "tinybird.views.api_pipes.ch_alter_table_modify_query",
            side_effect=CHException("Code: 181, e.displayText = DB::Exception: Illegal FINAL mocked."),
        ):
            response = await self.fetch_async(
                f"/v0/pipes?force=true&token={token}&ignore_sql_errors=false",
                method="POST",
                body=json.dumps(
                    {
                        "name": pipe_name,
                        "nodes": [
                            {
                                "name": "mv",
                                "type": "materialized",
                                "sql": f"SELECT toDate(d) AS d, sales * 15 AS fake_sales FROM {ds_name_source}",
                                "datasource": target_ds_name,
                            }
                        ],
                    }
                ),
                headers={"Content-type": "application/json"},
            )
            self.assertEqual(response.code, 400, response.body)
            await check_existing_matview_not_modified(existing_node_id, original_query)

    @tornado.testing.gen_test
    async def test_override_pipe_body(self):
        await self._make_endpoint(
            "test_pipe", token_name="test_create_pipe_body_skips_invalid_keys"
        )  # make test_pipe available for other pipes
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.PIPES_CREATE)
        pipe_name = "pipe_override"
        response = await self.fetch_async(
            f"/v0/pipes?token={token}",
            method="POST",
            body=json.dumps(
                {"name": pipe_name, "nodes": [{"name": "node_0", "sql": "select * from test_pipe limit 1"}]}
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)
        pipe_first = json.loads(response.body)
        pipe_token = Users.add_token(u, "pipe_token", scopes.PIPES_READ, pipe_first["id"])

        response = await self.fetch_async(
            f"/v0/pipes?token={token}&force=true",
            method="POST",
            body=json.dumps(
                {"name": pipe_name, "nodes": [{"name": "node_new", "sql": "select * from test_pipe limit 5"}]}
            ),
            headers={"Content-type": "application/json"},
        )

        self.assertEqual(response.code, 200, response.body)
        pipe_override = json.loads(response.body)

        self.assertEqual(len(pipe_override["nodes"]), 1)

        node = pipe_override["nodes"][0]
        self.assertEqual(node["name"], "node_new")
        self.assertEqual(node["sql"], "select * from test_pipe limit 5")
        self.assertEqual(pipe_override["id"], pipe_first["id"])

        # __override is deleted
        response = await self.fetch_async(f"/v0/pipes/{pipe_name}__override?token={pipe_token}", method="GET")

        result = json.loads(response.body)
        self.assertEqual(response.code, 404, response.body)
        self.assertEqual(result.get("error"), "Pipe 'pipe_override__override' not found")

        # pipe_token has permissions over overriden pipe
        response = await self.fetch_async(f"/v0/pipes/{pipe_name}?token={pipe_token}", method="GET")

        self.assertEqual(response.code, 200, response.body)

    @tornado.testing.gen_test
    async def test_override_pipe_body_fails(self):
        await self._make_endpoint(
            "test_pipe", token_name="test_create_pipe_body_skips_invalid_keys"
        )  # make test_pipe available for other pipes
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.PIPES_CREATE)
        pipe_name = "pipe_override"
        response = await self.fetch_async(
            f"/v0/pipes?token={token}",
            method="POST",
            body=json.dumps(
                {"name": pipe_name, "nodes": [{"name": "node_0", "sql": "select * from test_pipe limit 1"}]}
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)
        pipe = json.loads(response.body)

        wrong_ds_does_not_exist = "wrong_ds_does_not_exist"
        response = await self.fetch_async(
            f"/v0/pipes?token={token}&force=true",
            method="POST",
            body=json.dumps(
                {
                    "name": pipe_name,
                    "nodes": [{"name": "node_new", "sql": f"select * from {wrong_ds_does_not_exist} limit 5"}],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        error = json.loads(response.body).get("error")
        self.assertEqual(response.code, 400, response.body)
        self.assertEqual(error, f"Resource '{wrong_ds_does_not_exist}' not found")

        pipe_token = Users.add_token(u, "pipe_token", scopes.PIPES_READ, pipe["id"])

        response = await self.fetch_async(f"/v0/pipes/{pipe_name}__override?token={pipe_token}", method="GET")
        result = json.loads(response.body)
        self.assertEqual(response.code, 404, response.body)
        self.assertEqual(result.get("error"), "Pipe 'pipe_override__override' not found")

        response = await self.fetch_async(f"/v0/pipes/{pipe_name}?token={token}", method="GET")
        self.assertEqual(response.code, 200, response.body)
        pipe = json.loads(response.body)

        node = pipe["nodes"][0]
        self.assertEqual(node["name"], "node_0")
        self.assertEqual(node["sql"], "select * from test_pipe limit 1")

    @tornado.testing.gen_test
    async def test_add_endpoint_to_materializing_pipe(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_add_endpoint_to_materializing_pipe"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        with User.transaction(self.WORKSPACE_ID) as w:
            w.feature_flags[FeatureFlagWorkspaces.PIPE_ENDPOINT_RESTRICTIONS.value] = True

        # 1. create a datasource
        ds_name = "test_ds_add_endpoint_to_materializing_pipe"
        params = {
            "token": token,
            "name": ds_name,
            "schema": "a UInt64",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        node_name = "mat_view_node"
        params = {"token": token, "name": node_name}
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}",
            method="POST",
            body=f"select a * 2 as b, a * 3 as c from {ds_name}",
        )
        self.assertEqual(response.code, 200)

        # 2. materialize view
        target_ds_name = "mat_view_node_ds"
        params = {"token": token, "datasource": target_ds_name, "engine": "MergeTree"}
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}/materialization?{urlencode(params)}", method="POST", body=""
        )
        self.assertEqual(response.code, 200, response.body)

        # 3. try to create endpoint
        params = {"token": token}
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}/endpoint?{urlencode(params)}", method="POST", body=""
        )

        result = json.loads(response.body)
        self.assertEqual(response.code, 403, response.body)
        self.assertEqual(
            result.get("error"), f"Pipe {pipe_name} cannot be an endpoint because it already has a materialized view."
        )

        with User.transaction(self.WORKSPACE_ID) as w:
            w.feature_flags[FeatureFlagWorkspaces.PIPE_ENDPOINT_RESTRICTIONS.value] = False

    @tornado.testing.gen_test
    async def test_should_not_add_node_with_wrong_sql_template_to_copy_pipe(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_add_node_to_copy_pipe"
        node_name = "test_node_to_copy_pipe_0"
        ds_name = "test_add_node_to_copy_pipe_ds"
        Users.add_pipe_sync(
            u,
            pipe_name,
            nodes=[
                {
                    "name": node_name,
                    "sql": """%
                        SELECT start_datetime, pipe_name FROM test_add_node_to_copy_pipe_ds WHERE start_datetime = {{DateTime(start_time, 2023-03-01)}}
                    """,
                }
            ],
        )

        await self.tb_api_proxy_async.create_datasource(
            token=token,
            ds_name=ds_name,
            schema="start_datetime DateTime, pipe_name String",
            engine_params={
                "engine": "MergeTree",
                "engine_sorting_key": "pipe_name, start_datetime",
            },
        )

        params = {"token": token, "target_datasource": ds_name}

        response = await self.fetch_async(
            path=f"/v0/pipes/{pipe_name}/nodes/{node_name}/copy?{urlencode(params)}", method="POST", body=""
        )
        result = json.loads(response.body)
        self.assertEqual(response.code, 400, response.body)
        self.assertEqual(
            result.get("error"),
            f"leading zeros in decimal integer literals are not permitted; use an 0o prefix for octal integers (<unknown>, line 1) (in node '{node_name}' from pipe '{pipe_name}')",
        )

    @tornado.testing.gen_test
    async def test_should_not_add_node_with_wrong_sql_type_to_copy_pipe(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_add_node_to_copy_pipe"
        node_name = "test_node_to_copy_pipe_0"
        ds_name = "test_add_node_to_copy_pipe_ds"
        Users.add_pipe_sync(
            u,
            pipe_name,
            nodes=[
                {
                    "name": node_name,
                    "sql": """%
                            SELECT start_datetime, pipe_name FROM test_add_node_to_copy_pipe_ds WHERE start_datetime = {{DateTime(start_time, '2023-03-01')}}
                        """,
                }
            ],
        )

        await self.tb_api_proxy_async.create_datasource(
            token=token,
            ds_name=ds_name,
            schema="start_datetime DateTime, pipe_name String",
            engine_params={
                "engine": "MergeTree",
                "engine_sorting_key": "pipe_name, start_datetime",
            },
        )

        params = {"token": token, "target_datasource": ds_name}

        response = await self.fetch_async(
            path=f"/v0/pipes/{pipe_name}/nodes/{node_name}/copy?{urlencode(params)}", method="POST", body=""
        )
        result = json.loads(response.body)
        self.assertEqual(response.code, 400, response.body)
        self.assertEqual(result.get("error"), "Template Syntax Error: Error validating '2023-03-01' to type DateTime")

    @tornado.testing.gen_test
    async def test_should_not_add_node_with_wrong_sql_type_when_updating_copy_pipe(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_add_node_to_copy_pipe"
        node_name = "test_node_to_copy_pipe_0"
        ds_name = "test_add_node_to_copy_pipe_ds"
        Users.add_pipe_sync(
            u,
            pipe_name,
            nodes=[
                {
                    "name": node_name,
                    "sql": """%
                        SELECT start_datetime, pipe_name FROM test_add_node_to_copy_pipe_ds WHERE start_datetime = {{DateTime(start_time, '2023-03-01')}}
                    """,
                }
            ],
        )

        await self.tb_api_proxy_async.create_datasource(
            token=token,
            ds_name=ds_name,
            schema="start_datetime DateTime, pipe_name String",
            engine_params={
                "engine": "MergeTree",
                "engine_sorting_key": "pipe_name, start_datetime",
            },
        )

        params = {"token": token, "target_datasource": ds_name}

        response = await self.fetch_async(
            path=f"/v0/pipes/{pipe_name}/nodes/{node_name}/copy?{urlencode(params)}", method="PUT", body=""
        )
        self.assertEqual(response.code, 400, response.body)

    @tornado.testing.gen_test
    async def test_add_endpoint_to_copy_pipe(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_add_endpoint_to_copy_pipe"
        node_name = "test_add_endpoint_to_copy_pipe_0"
        ds_name = "test_add_endpoint_to_copy_pipe_ds"
        Users.add_pipe_sync(
            u, pipe_name, nodes=[{"name": node_name, "sql": "select now() as date, a as number from test_table"}]
        )

        await self.tb_api_proxy_async.create_datasource(
            token=token,
            ds_name=ds_name,
            schema="date DateTime, number UInt64",
            engine_params={
                "engine": "MergeTree",
                "engine_sorting_key": "date",
            },
        )

        params = {"token": token, "target_datasource": ds_name}

        response = await self.fetch_async(
            path=f"/v0/pipes/{pipe_name}/nodes/{node_name}/copy?{urlencode(params)}", method="POST", body=""
        )
        self.assertEqual(response.code, 200, response.body)

        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}/endpoint?{urlencode(params)}", method="POST", body=""
        )

        result = json.loads(response.body)
        self.assertEqual(response.code, 403, response.body)
        self.assertEqual(
            result.get("error"), f"Pipe {pipe_name} cannot be an endpoint because it is already set as copy."
        )

    @tornado.testing.gen_test
    async def test_materialize_in_pipe_with_endpoint(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_materialize_in_pipe_with_endpoint"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        with User.transaction(self.WORKSPACE_ID) as w:
            w.feature_flags[FeatureFlagWorkspaces.PIPE_ENDPOINT_RESTRICTIONS.value] = True

        # 1. create a datasource
        ds_name = "test_ds_materialize_in_pipe_with_endpoint"
        params = {
            "token": token,
            "name": ds_name,
            "schema": "a UInt64",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        node_name = "mat_view_node"
        params = {"token": token, "name": node_name}
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}",
            method="POST",
            body=f"select a * 2 as b, a * 3 as c from {ds_name}",
        )
        self.assertEqual(response.code, 200)

        # 2. create endpoint
        params = {"token": token}
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}/endpoint?{urlencode(params)}", method="POST", body=""
        )

        self.assertEqual(response.code, 200, response.body)

        # 3. try to materialize view
        target_ds_name = "mat_view_node_ds"
        params = {"token": token, "datasource": target_ds_name, "engine": "MergeTree"}
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}/materialization?{urlencode(params)}", method="POST", body=""
        )

        result = json.loads(response.body)
        self.assertEqual(response.code, 403, response.body)
        self.assertEqual(
            result.get("error"),
            f"Pipe {pipe_name} cannot be materialized because it is an endpoint. Pipes can only have one output: endpoint or materialized node. You can copy the pipe and publish it as an endpoint, or unlink the materialized view.",
        )

        with User.transaction(self.WORKSPACE_ID) as w:
            w.feature_flags[FeatureFlagWorkspaces.PIPE_ENDPOINT_RESTRICTIONS.value] = False

    @tornado.testing.gen_test
    async def test_push_multiple_nodes_materializing(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_push_multiple_nodes_materializing_pipe"

        with User.transaction(self.WORKSPACE_ID) as w:
            w.feature_flags[FeatureFlagWorkspaces.PIPE_NODE_RESTRICTIONS.value] = True

        # 1. create a datasource
        ds_name = "test_ds_push_multiple_nodes_materializing"
        params = {
            "token": token,
            "name": ds_name,
            "schema": "a UInt64",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        test_ds_name = "test_copy_materialized_ds_name"
        test_ds = Users.add_datasource_sync(u, test_ds_name)
        create_test_datasource(u, test_ds)

        response = await self.fetch_async(
            f"/v0/pipes?token={token}",
            method="POST",
            body=json.dumps(
                {
                    "name": pipe_name,
                    "nodes": [
                        {
                            "name": "node_00",
                            "sql": f"select * from {test_ds.id}",
                            "id": "foo",
                            "datasource": f"{test_ds_name}_mv",
                            "type": "materialized",
                        },
                        {
                            "name": "node_01",
                            "sql": f"select * from {test_ds.id}",
                            "id": "foo",
                            "datasource": f"{test_ds_name}_mv",
                            "type": "materialized",
                        },
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )

        result = json.loads(response.body)
        self.assertEqual(response.code, 403)
        self.assertEqual(
            result.get("error"),
            "There is more than one materialized node. Pipes can only have one output. Set only one node to be a materialized node and try again.",
        )

        with User.transaction(self.WORKSPACE_ID) as w:
            w.feature_flags[FeatureFlagWorkspaces.PIPE_NODE_RESTRICTIONS.value] = False

    @pytest.mark.skipif(
        get_min_clickhouse_version() < KAFKA_MIN_CH_VERSION_NEEDED,
        reason="ClickHouse Kafka authentication is not available",
    )
    @tornado.testing.gen_test
    async def test_create_and_override_data_sink_from_nodes(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)

        with User.transaction(self.WORKSPACE_ID) as workspace:
            workspace.set_user_limit("sinks_max_pipes", 2, "sinks")
            workspace.set_user_limit("sinks_max_jobs", 2, "sinks")

        DataConnector.add_connector(
            u,
            "example_kafka",
            "kafka",
            {
                "kafka_bootstrap_servers": "kafka:9092",
                "kafka_security_protocol": "plaintext",
                "kafka_sasl_plain_username": "",
                "kafka_sasl_plain_password": "",
            },
        )

        pipe_name = "pipe_data_sink_from_nodes"
        response = await self.fetch_async(
            f"/v0/pipes?token={token}",
            method="POST",
            body=json.dumps(
                {
                    "name": pipe_name,
                    "service": "kafka",
                    "connection": "example_kafka",
                    "kafka_topic": "topic_data_sink_from_nodes",
                    "nodes": [
                        {
                            "name": "sink",
                            "type": PipeNodeTypes.DATA_SINK,
                            "sql": "select * from test_table",
                        }
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        result = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        pipe_node = result["nodes"][0]
        self.assertEqual(pipe_node["name"], "sink")

        # override kafka sink
        response = await self.fetch_async(
            f"/v0/pipes?force=true&token={token}",
            method="POST",
            body=json.dumps(
                {
                    "name": pipe_name,
                    "service": "kafka",
                    "connection": "example_kafka",
                    "kafka_topic": "topic_data_sink_from_nodes",
                    "nodes": [
                        {
                            "name": "sink",
                            "type": PipeNodeTypes.DATA_SINK,
                            "sql": "select * from test_table LIMIT 10",
                        }
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )

        # check old kafka table was dropped it does not exist in CH or the sql has changed
        # TODO: there should be no data loss nor duplication, we are not checking that
        old_node_id = pipe_node["id"]
        old_kafka_ds_was_dropped = exec_sql(
            u["database"], f"select * from system.tables where name = '{old_node_id}_kafka_events' FORMAT JSON"
        )
        self.assertEqual(len(old_kafka_ds_was_dropped["data"]), 0, old_kafka_ds_was_dropped)

        # check there's a new kafka datasource
        result = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        new_pipe_node = result["nodes"][0]
        new_node_id = new_pipe_node["id"]
        new_kafka_ds = exec_sql(
            u["database"], f"select * from system.tables where name = '{new_node_id}_kafka_events' FORMAT JSON"
        )
        self.assertEqual(len(new_kafka_ds["data"]), 1, new_kafka_ds)

    @pytest.mark.skipif(
        get_min_clickhouse_version() < KAFKA_MIN_CH_VERSION_NEEDED,
        reason="ClickHouse Kafka authentication is not available",
    )
    @tornado.testing.gen_test
    async def test_cannot_update_kafka_sink_node(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)

        with User.transaction(self.WORKSPACE_ID) as workspace:
            workspace.set_user_limit("sinks_max_pipes", 2, "sinks")
            workspace.set_user_limit("sinks_max_jobs", 2, "sinks")

        DataConnector.add_connector(
            u,
            "example_kafka",
            "kafka",
            {
                "kafka_bootstrap_servers": "kafka:9092",
                "kafka_security_protocol": "plaintext",
                "kafka_sasl_plain_username": "",
                "kafka_sasl_plain_password": "",
            },
        )

        pipe_name = "pipe_kafka_sink_node"
        response = await self.fetch_async(
            f"/v0/pipes?token={token}",
            method="POST",
            body=json.dumps(
                {
                    "name": pipe_name,
                    "service": "kafka",
                    "connection": "example_kafka",
                    "kafka_topic": "topic_kafka_sink_node",
                    "nodes": [
                        {
                            "name": "sink",
                            "type": PipeNodeTypes.DATA_SINK,
                            "sql": "select * from test_table",
                        }
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        result = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        pipe_node = result["nodes"][0]
        self.assertEqual(pipe_node["name"], "sink")

        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{pipe_node['id']}?token={token}",
            method="PUT",
            body="select * from test_table LIMIT 10",
        )
        payload = json.loads(response.body)
        self.assertEqual(response.code, 403)
        self.assertEqual(payload["error"], "Cannot modify a Kafka Sink Node")

    def test_custom_error(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        pipe = Users.add_pipe_sync(
            u,
            "test_custom_error",
            """%
            {{ custom_error({'err_id': 1, 'err': 'test'}, 408) }}
            select 1
        """,
        )

        pipe.endpoint = pipe.pipeline.nodes[0].name
        Users.update_pipe(u, pipe)

        pipe_token = Users.add_token(u, "pipe_token", scopes.PIPES_READ, pipe.id)

        response = self.fetch(f"/v0/pipes/test_custom_error.json?token={pipe_token}")
        result = json.loads(response.body)
        self.assertEqual(result, {"err_id": 1, "err": "test"})
        self.assertEqual(response.code, 408)

    # https://gitlab.com/tinybird/analytics/-/issues/1492
    def test_create_pipe_with_asterisk_and_extra_columns(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.PIPES_CREATE)
        response = self.fetch(
            f"/v0/pipes?token={token}&name=endpoint_errors&sql=select+result,error,*+from+tinybird.datasources_ops_log",
            method="POST",
            body="",
        )
        self.assertEqual(response.code, 200)

    def test_change_node_position(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)

        Users.add_pipe_sync(
            u,
            "test_pipe_reorder",
            nodes=[
                {"name": "node_a", "sql": "Select 1"},
                {"name": "node_b", "sql": "Select 1"},
                {"name": "node_c", "sql": "Select 1"},
            ],
        )

        params = {"token": token, "position": 2}
        response = self.fetch(f"/v0/pipes/test_pipe_reorder/nodes/node_b?{urlencode(params)}", method="PUT", body="")
        self.assertEqual(response.code, 200, response.body)

        response = self.fetch("/v0/pipes/test_pipe_reorder?token=%s" % token)
        payload = json.loads(response.body)
        self.assertEqual(response.code, 200)
        node_positions = [node["name"] for node in payload["nodes"]]
        self.assertEqual(node_positions, ["node_a", "node_c", "node_b"])

        params = {"token": token, "position": 0}
        response = self.fetch(f"/v0/pipes/test_pipe_reorder/nodes/node_b?{urlencode(params)}", method="PUT", body="")
        self.assertEqual(response.code, 200, response.body)

        response = self.fetch("/v0/pipes/test_pipe_reorder?token=%s" % token)
        payload = json.loads(response.body)
        self.assertEqual(response.code, 200)
        node_positions = [node["name"] for node in payload["nodes"]]
        self.assertEqual(node_positions, ["node_b", "node_a", "node_c"])

    def test_change_node_position_raises_error_for_positions_out_of_supported_range(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)

        Users.add_pipe_sync(
            u,
            "test_pipe_reorder",
            nodes=[
                {"name": "node_a", "sql": "Select 1"},
                {"name": "node_b", "sql": "Select 1"},
                {"name": "node_c", "sql": "Select 1"},
            ],
        )

        params = {"token": token, "position": 4}
        response = self.fetch(f"/v0/pipes/test_pipe_reorder/nodes/node_b?{urlencode(params)}", method="PUT", body="")
        self.assertEqual(response.code, 400, response.body)
        payload = json.loads(response.body)
        self.assertTrue(
            "Nodes can only be moved to positions already in use by other nodes." in payload.get("error", "")
        )


class TestAPITablePipeline(BaseTest):
    def setUp(self):
        super().setUp()
        self.create_test_datasource()

    def tearDown(self):
        self._drop_token()
        super().tearDown()

    def _drop_token(self):
        try:
            u = Users.get_by_id(self.WORKSPACE_ID)
            token = Users.get_token(u, "test")
            if token:
                Users.drop_token(u, token)
        except Exception:
            pass

    def test_non_auth(self):
        self.check_non_auth_responses(
            [
                "/v0/pipes/test_pipe/append",
                "/v0/pipes/test_pipe/append?token=append",
            ]
        )

    def test_method_not_allowed(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_pipe"
        url_parts = [f"/v0/pipes/{pipe_name}/nodes?token={token}"]
        url = "&".join(url_parts)
        response = self.fetch(url, method="PUT", body="select 1")
        self.assertEqual(response.code, 405)
        self.assertEqual(json.loads(response.body)["error"], "HTTP 405: Method Not Allowed")

    async def __append_node(self, sql, name=None, description=None, expected_code=200, pipe_name="test_pipe"):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        url_parts = [f"/v0/pipes/{pipe_name}/nodes?token={token}"]
        if name:
            url_parts += [f"name={name}"]
        if description:
            url_parts += [f"description={description}"]
        url = "&".join(url_parts)
        response = await self.fetch_async(url, method="POST", body=sql)
        self.assertEqual(response.code, expected_code)
        return json.loads(response.body)

    async def __make_endpoint_node(self, pipe_name, pipe_node, expected_code=200):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{pipe_node['id']}/endpoint?token={token}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, expected_code)
        return json.loads(response.body)

    async def __make_endpoint(self, pipe_node, expected_code=200):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        response = await self.fetch_async(
            f"/v0/pipes/test_pipe/nodes/{pipe_node['id']}/endpoint?token={token}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, expected_code)
        return response

    async def __make_endpoint_and_get_node_count(self, pipe_node):
        await self.__make_endpoint(pipe_node)
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        response = await self.fetch_async(f"/v0/sql?q=select+count()+c+from+test_pipe+format+JSON&token={token}")
        self.assertEqual(response.code, 200, response.body)
        data = json.loads(response.body)
        row = data["data"][0]
        return int(row["c"])

    @tornado.testing.gen_test
    async def test_append_node(self):
        pipe_node = await self.__append_node("select * from test_pipe_0 where a > 4")
        self.assertEqual(pipe_node["name"], "test_pipe_1")
        self.assertEqual(pipe_node["sql"], "select * from test_pipe_0 where a > 4")
        self.assertEqual(pipe_node["description"], None)
        self.assertEqual(pipe_node["dependencies"], ["test_pipe_0"])
        self.assertEqual(pipe_node["materialized"], None)
        self.assertIn("id", pipe_node)
        self.assertEqual(await self.__make_endpoint_and_get_node_count(pipe_node), 1)

    @tornado.testing.gen_test
    async def test_endpoint_with_comments(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_node = await self.__append_node("select * from numbers(10) --limit 10")
        endpoint = await self.__append_node(f"select count() as total from {pipe_node['name']}")
        await self.__make_endpoint(endpoint)
        response = await self.fetch_async(f"/v0/pipes/test_pipe.json?token={token}")
        self.assertEqual(response.code, 200, response.body)
        data = json.loads(response.body)
        self.assertEqual(int(data["data"][0]["total"]), 10)

    @tornado.testing.gen_test
    async def test_endpoint_with_length_function(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        endpoint = await self.__append_node(
            "% SELECT * FROM numbers(10) {% if defined(search) and length(String(search)) > 0 %} WHERE 1=1 {% end %} LIMIT 10"
        )
        await self.__make_endpoint(endpoint)
        response = await self.fetch_async(f"/v0/pipes/test_pipe.json?token={token}&search=anything")
        self.assertEqual(response.code, 400, response.body)
        data = json.loads(response.body)
        self.assertEqual(
            "length cannot be used as a variable name or as a function inside of a template" in data["error"], True
        )

    @tornado.testing.gen_test
    async def test_append_node_name_description(self):
        pipe_node = await self.__append_node(
            "select * from test_pipe_0 where a > 4", "test_pipe_node_name", "test_description"
        )
        self.assertEqual(pipe_node["name"], "test_pipe_node_name")
        self.assertEqual(pipe_node["sql"], "select * from test_pipe_0 where a > 4")
        self.assertEqual(pipe_node["description"], "test_description")
        self.assertEqual(pipe_node["dependencies"], ["test_pipe_0"])
        self.assertEqual(pipe_node["materialized"], None)
        self.assertIn("id", pipe_node)
        self.assertEqual(await self.__make_endpoint_and_get_node_count(pipe_node), 1)

    @tornado.testing.gen_test
    async def test_append_node_name_clash(self):
        name = "test_pipe_node_name"
        pipe_node = await self.__append_node("select * from test_pipe_0 where a > 4", name)

        result = await self.__append_node("select * from test_pipe_0 where a < 100", name, expected_code=400)
        self.assertEqual(
            result["error"],
            'Node name "test_pipe_node_name" already exists in pipe. Node names must be unique within a given pipe.',
        )

        # pipe continues to work
        self.assertEqual(await self.__make_endpoint_and_get_node_count(pipe_node), 1)

    @tornado.testing.gen_test
    async def test_different_nodes_output(self):
        n0 = await self.__append_node("select * from test_pipe_0 where a > 2")
        n1 = await self.__append_node("select * from test_pipe_1 limit 1")
        self.assertEqual(await self.__make_endpoint_and_get_node_count(n0), 3)
        self.assertEqual(await self.__make_endpoint_and_get_node_count(n1), 1)

    @tornado.testing.gen_test
    async def test_edit_node(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)
        response = await self.fetch_async(
            "/v0/pipes/test_pipe/nodes?token=%s" % token, method="POST", body="select * from test_pipe_0 where a > 4"
        )
        node = json.loads(response.body)
        self.assertEqual(await self.__make_endpoint_and_get_node_count(node), 1)

        response = await self.fetch_async(
            f"/v0/pipes/test_pipe/nodes/{node['id']}?token={token}",
            method="PUT",
            body="select * from test_pipe_0 where a > 1",
        )
        payload = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(payload["name"], "test_pipe_1")
        self.assertEqual(await self.__make_endpoint_and_get_node_count(node), 4)

    @tornado.testing.gen_test
    async def test_edit_node_with_wrong_sql(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)
        response = await self.fetch_async(
            "/v0/pipes/test_pipe/nodes?token=%s" % token, method="POST", body="select * from test_pipe_0 where a > 4"
        )
        node = json.loads(response.body)
        self.assertEqual(await self.__make_endpoint_and_get_node_count(node), 1)

        response = await self.fetch_async(
            f"/v0/pipes/test_pipe/nodes/{node['id']}?token={token}&ignore_sql_errors=true",
            method="PUT",
            body="wrong sql",
        )
        payload = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(payload["name"], "test_pipe_1")
        self.assertEqual(payload["ignore_sql_errors"], True)
        self.assertEqual(payload["sql"], "wrong sql")
        # a wrong node should not be endpoint
        await self.__make_endpoint(node, 400)

    @tornado.testing.gen_test
    async def test_edit_node_name_and_description(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)

        response = await self.fetch_async(
            "/v0/pipes/test_pipe/nodes?token=%s" % token, method="POST", body="select * from test_pipe_0 where a > 4"
        )
        node = json.loads(response.body)
        self.assertEqual(node["name"], "test_pipe_1")
        self.assertEqual(node["description"], None)
        self.assertEqual(await self.__make_endpoint_and_get_node_count(node), 1)

        new_name = "edited_node_name"
        description = "explanation"
        response = await self.fetch_async(
            f"/v0/pipes/test_pipe/nodes/{node['name']}?name={new_name}&description={description}&token={token}",
            method="PUT",
            body="select * from test_pipe_0 where a > 1",
        )
        node = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(node["name"], new_name)
        self.assertEqual(node["description"], description)
        self.assertEqual(await self.__make_endpoint_and_get_node_count(node), 4)

    def test_reset_node_description(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)

        params = {
            "token": token,
            "description": "my description",
        }
        response = self.fetch(
            f"/v0/pipes/test_pipe/nodes?{urlencode(params)}", method="POST", body="select * from test_pipe_0"
        )
        node = json.loads(response.body)
        self.assertEqual(node["name"], "test_pipe_1")
        self.assertEqual(node["sql"], "select * from test_pipe_0")
        self.assertEqual(node["description"], "my description")

        params = {
            "token": token,
            "description": "",
        }
        response = self.fetch(f"/v0/pipes/test_pipe/nodes/{node['name']}?{urlencode(params)}", method="PUT", body="")
        self.assertEqual(response.code, 200, response.body)
        node = json.loads(response.body)
        self.assertEqual(node["name"], "test_pipe_1")
        self.assertEqual(node["sql"], "select * from test_pipe_0")
        self.assertEqual(node["description"], "")

    @tornado.testing.gen_test
    async def test_edit_node_name_errors(self):
        first_node_name = "test_pipe_node_name"
        pipe_node = await self.__append_node("select * from test_pipe_0 where a > 4", first_node_name)
        self.assertEqual(pipe_node["name"], first_node_name)
        pipe_node = await self.__append_node("select * from test_pipe_0 where a > 4", "node_001")
        self.assertEqual(pipe_node["name"], "node_001")

        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)

        response = await self.fetch_async(
            f"/v0/pipes/test_pipe/nodes/{pipe_node['name']}?name=5555&token={token}", method="PUT", body=""
        )
        payload = json.loads(response.body)
        self.assertEqual(response.code, 400)
        self.assertEqual(
            payload["error"],
            'Invalid pipe name "5555". Name must start with a letter and contain only letters, numbers, and underscores. Hint: use t_5555_.',
        )

        response = await self.fetch_async(
            f"/v0/pipes/test_pipe/nodes/{pipe_node['name']}?name={first_node_name}&token={token}", method="PUT", body=""
        )
        payload = json.loads(response.body)
        self.assertEqual(response.code, 400)
        self.assertEqual(
            payload["error"],
            'Node name "test_pipe_node_name" already exists in pipe. Node names must be unique within a given pipe.',
        )

    @tornado.testing.gen_test
    async def test_edit_node_name_clash_with_other_pipe(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        test_pipe_node = await self.__append_node("select * from test_pipe_0 where a > 10")
        pipe = Users.add_pipe_sync(u, "test_pipe_node_clash_with_other_pipe_name", "select 1")
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)

        response = await self.fetch_async(
            f"/v0/pipes/test_pipe/nodes/{test_pipe_node['name']}?name={pipe.name}&token={token}", method="PUT", body=""
        )
        payload = json.loads(response.body)
        self.assertEqual(response.code, 409)
        self.assertEqual(
            payload["error"],
            f'There is already a Pipe with name "{pipe.name}". Pipe and Data Source names must be globally unique',
        )

        # if should work good with pipe
        node = pipe.pipeline.last()
        response = await self.fetch_async(
            f"/v0/pipes/test_pipe/nodes/{test_pipe_node['name']}?name={node.name}&token={token}", method="PUT", body=""
        )
        payload = json.loads(response.body)
        self.assertEqual(response.code, 200)

    def test_add_and_edit_node_with_params(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)

        response = self.fetch(
            "/v0/pipes/test_pipe/nodes?token=%s" % token, method="POST", body="% select * from test_pipe_0 LIMIT 1"
        )
        self.assertEqual(response.code, 200)
        node = json.loads(response.body)
        self.assertEqual(node["params"], [])

        new_sql = "% select *, {{String(my_filter, 'hello world')}} from test_pipe_0 LIMIT 1"
        expected_params = [{"name": "my_filter", "type": "String", "default": "hello world"}]
        response = self.fetch(f"/v0/pipes/test_pipe/nodes/{node['name']}?token={token}", method="PUT", body=new_sql)
        node = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(node["params"], expected_params)

        new_sql = "% select * from test_pipe_0 LIMIT {{Int8(hey, 0)}}"
        expected_params = [{"name": "hey", "type": "Int8", "default": 0}]
        response = self.fetch(f"/v0/pipes/test_pipe/nodes/{node['name']}?token={token}", method="PUT", body=new_sql)
        node = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(node["params"], expected_params)

    def test_drop_node(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)
        response = self.fetch(
            "/v0/pipes/test_pipe/nodes?token=%s" % token, method="POST", body="select * from test_pipe_0 where a > 4"
        )
        self.fetch(
            "/v0/pipes/test_pipe/nodes?token=%s" % token, method="POST", body="select * from test_pipe_1 where a > 5"
        )

        node = json.loads(response.body)

        res = self.fetch("/v0/pipes/test_pipe/nodes/%s?token=%s" % (node["id"], token), method="DELETE", body=None)

        self.assertEqual(res.code, 204)
        self.assertEqual(len(Users.get_pipe(u, "test_pipe").pipeline), 2)

    @patch.object(GCloudSchedulerJobs, "manage_job")
    @patch.object(GCloudSchedulerJobs, "update_job_status")
    def test_drop_copy_node(self, _mock_update_job, _mock_manage_job):
        u = Users.get_by_id(self.WORKSPACE_ID)

        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_drop_copy_node"
        node_name = "test_drop_copy_node_0"
        ds_a_name = "test_drop_copy_node_a_ds"
        ds_b_name = "test_drop_copy_node_b_ds"

        test_a_ds = Users.add_datasource_sync(u, ds_a_name)
        create_test_datasource(u, test_a_ds)
        test_b_ds = Users.add_datasource_sync(u, ds_b_name)
        create_test_datasource(u, test_b_ds)

        pipe = Users.add_pipe_sync(u, pipe_name, nodes=[{"name": node_name, "sql": f"select * from {ds_a_name}"}])

        params = {"token": token, "target_datasource": ds_b_name, "schedule_cron": "0 * * * *"}

        expected_job_name = GCloudSchedulerJobs.generate_job_name(self.WORKSPACE_ID, pipe.id)

        response = self.fetch(
            path=f"/v0/pipes/{pipe_name}/nodes/{node_name}/copy?{urlencode(params)}", method="POST", body=""
        )
        self.assertEqual(response.code, 200, response.body)

        pipe = Users.get_pipe(u, pipe_name)

        test_b_ds = Users.get_datasource(u, ds_b_name)
        self.assertIsNotNone(test_b_ds.tags.get("source_copy_pipes").get(pipe.id))

        data_sink = DataSink.get_by_resource_id(pipe.id, u.id)
        self.assertIsNotNone(data_sink)

        response = self.fetch(path=f"/v0/pipes/{pipe_name}/nodes/{node_name}?{urlencode(params)}", method="DELETE")

        self.assertEqual(response.code, 204)

        pipe = Users.get_pipe(u, pipe_name)
        self.assertIsNone(pipe.pipeline.get_node(node_name))

        test_b_ds = Users.get_datasource(u, ds_b_name)
        self.assertIsNone(test_b_ds.tags.get("source_copy_pipes").get(pipe.id))

        _mock_update_job.assert_called_with(SchedulerJobActions.DELETE, expected_job_name)

        try:
            data_sink = DataSink.get_by_resource_id(pipe.id, u.id)
        except Exception:
            data_sink = None
        self.assertIsNone(data_sink)

    @tornado.testing.gen_test
    async def test_do_not_drop_endpoint_node(self):
        node = await self.__append_node("select * from test_pipe_0 where a > 10")
        u = Users.get_by_id(self.WORKSPACE_ID)
        pipe = Users.get_pipe(u, "test_pipe")
        token = Users.add_token(u, "test_drop_endpoint", scopes.PIPES_READ, pipe.id)
        admin_token = Users.get_token_for_scope(u, scopes.ADMIN)

        async def query_pipe(expected_code):
            response = await self.fetch_async(f"/v0/sql?q=select+count()+c+from+test_pipe+format+JSON&token={token}")
            self.assertEqual(response.code, expected_code)
            payload = json.loads(response.body)
            return payload

        payload = await query_pipe(400)
        self.assertEqual(payload["error"], "The pipe 'test_pipe' does not have an endpoint yet")

        await self.__make_endpoint(node)
        payload = await query_pipe(200)
        self.assertEqual(payload["data"][0]["c"], 1)

        response = await self.fetch_async(
            f"/v0/pipes/test_pipe/nodes/{node['id']}?token={admin_token}", method="DELETE", body=None
        )
        self.assertEqual(response.code, 400)
        payload = json.loads(response.body)
        self.assertEqual(
            payload["error"], f"Node '{node['id']}' is an endpoint, unpublish the endpoint before removing the node"
        )

        # pipe's endpoint continues to work
        payload = await query_pipe(200)
        self.assertEqual(payload["data"][0]["c"], 1)

    @tornado.testing.gen_test
    async def test_publish_endpoint_in_pipe_with_read_token(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        pipe = Users.add_pipe_sync(u, "pipe_with_read_token", "select * from test_table")
        node = await self.__append_node("select count(*) from pipe_with_read_token_0", pipe_name="pipe_with_read_token")
        _ = Users.add_token(u, "pipe_read_token", scopes.PIPES_READ, pipe.id)
        response = await self.__make_endpoint_node("pipe_with_read_token", node)
        self.assertTrue(response["token"])

    @tornado.testing.gen_test
    async def test_publish_endpoint_in_pipe_without_read_token(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        _ = Users.add_pipe_sync(u, "pipe_with_read_token", "select * from test_table")
        node = await self.__append_node("select count(*) from pipe_with_read_token_0", pipe_name="pipe_with_read_token")
        response = await self.__make_endpoint_node("pipe_with_read_token", node)
        self.assertFalse("token" in response)

    @tornado.testing.gen_test
    async def test_publish_endpoint_in_pipe_without_unique_read_token(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        pipe = Users.add_pipe_sync(u, "pipe_with_read_token", "select * from test_table")
        pipe_2 = Users.add_pipe_sync(u, "extra_pipe", "select count(*) from test_table")
        node = await self.__append_node("select count(*) from pipe_with_read_token_0", pipe_name="pipe_with_read_token")
        token = Users.add_token(u, "pipe_read_token", None)
        Users.add_scope_to_token(u, token, scopes.PIPES_READ, pipe.id)
        Users.add_scope_to_token(u, token, scopes.PIPES_READ, pipe_2.id)
        response = await self.__make_endpoint_node("pipe_with_read_token", node)
        self.assertFalse("token" in response)

    @tornado.testing.gen_test
    async def test_unpublish_endpoint(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)

        # Endpoint not defined by default
        pipe_res = json.loads((await self.fetch_async(f"/v0/pipes/test_pipe?token={token}")).body)
        self.assertIsNone(pipe_res["endpoint"])

        # Enable endpoint
        await self.__make_endpoint(pipe_res["nodes"][0])
        pipe_res = json.loads((await self.fetch_async(f"/v0/pipes/test_pipe?token={token}")).body)
        self.assertEqual(pipe_res["endpoint"], pipe_res["nodes"][0]["id"])

        # Drop endpoint
        node_id = pipe_res["nodes"][0]["id"]
        response = await self.fetch_async(
            f"/v0/pipes/test_pipe/nodes/{node_id}/endpoint?token={token}", method="DELETE"
        )

        self.assertEqual(response.code, 200)
        pipe_res = json.loads((await self.fetch_async(f"/v0/pipes/test_pipe?token={token}")).body)
        self.assertIsNone(pipe_res["endpoint"])

    def test_drop_node_error(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)

        response = self.fetch(
            f"/v0/pipes/test_pipe/nodes/WADUS/endpoint?token={token}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )

        self.assertEqual(response.code, 400)
        payload = json.loads(response.body)
        self.assertEqual(payload["error"], "Pipe 'test_pipe' does not contain the 'WADUS' node")
        pipe_res = json.loads(self.fetch(f"/v0/pipes/test_pipe?token={token}").body)
        self.assertIsNone(pipe_res["endpoint"])

    def test_append_wrong_query(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)
        response = self.fetch(
            "/v0/pipes/test_pipe/nodes?token=%s" % token, method="POST", body="select count() from test_table_00"
        )
        payload = json.loads(response.body)
        self.assertEqual(response.code, 400)
        self.assertEqual(payload["error"], "Resource 'test_table_00' not found")

    @tornado.testing.gen_test
    async def test_append_node_prewhere(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)

        # let's create a datasource with some data
        ds_name_source = "ds_for_prewhere"
        params = {
            "token": token,
            "name": ds_name_source,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        s = StringIO("d,sales\n2019-01-01,2\n2019-01-02,3")
        response = await self.fetch_full_body_upload_async(create_url, s)
        self.assertEqual(response.code, 200, response.body)

        pipe_node = await self.__append_node(f"select * from {ds_name_source} prewhere sales > 1")
        self.assertEqual(pipe_node["name"], "test_pipe_1")
        self.assertEqual(pipe_node["sql"], f"select * from {ds_name_source} prewhere sales > 1")
        self.assertEqual(pipe_node["dependencies"], [ds_name_source])

    @tornado.testing.gen_test
    async def test_append_node_mat_column_access(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)

        # let's create a datasource
        ds_name_source = "ds_for_engine"
        params = {
            "token": token,
            "name": ds_name_source,
            "schema": "a UInt32, b UInt64 MATERIALIZED a * 2",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        first_node_query = f"""
            SELECT t.a, t.b
            FROM {ds_name_source} as t
            WHERE t.a >= 10
        """
        first_node = await self.__append_node(first_node_query)
        self.assertEqual(first_node["name"], "test_pipe_1")
        self.assertEqual(first_node["sql"], first_node_query)
        self.assertEqual(first_node["dependencies"], [ds_name_source])

        second_node_query = "select * from test_pipe_1"
        second_node = await self.__append_node(second_node_query)
        self.assertEqual(second_node["name"], "test_pipe_2")
        self.assertEqual(second_node["sql"], second_node_query)


class TestAPIPipesMaterializedViewsBatch(TestAPIPipeStats):
    async def check(self, token: str, job_id: str):
        params = {
            "token": token,
            "q": f"select * from tinybird.datasources_ops_log where job_id = '{job_id}' and event_type = 'populateview' FORMAT JSON",
        }
        status_check = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertTrue(len(json.loads(status_check.body)["data"]) > 0)
        for row in json.loads(status_check.body)["data"]:
            self.assertTrue(row["result"] != "ok")

    @tornado.testing.gen_test
    async def test_delete_mat_node_population_is_cancelled_or_errors(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_delete_mat_node_population_is_cancelled"
        ds_name_source = "ds_cancel_population_npde"
        target_ds_name = "mat_view_node_ds_node"

        job_response = await self.create_population_for_cancellation(pipe_name, ds_name_source, target_ds_name)
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{pipe_name}_node?token={token}", method="DELETE"
        )
        self.assertEqual(response.code, 204)

        # we await for either a cancel status or error because we dropped a related resource needed for the population
        job = await wait_until_job_is_in_expected_status_async(
            job_response["id"],
            [JobStatus.CANCELLED, JobStatus.CANCELLING, JobStatus.ERROR],
            max_retries=400,
            elapsed_time_interval=0.1,
        )
        self.assertTrue(job.status in ["cancelled", "cancelling", "error"], job.status)
        self.assertEqual(job.kind, "populateview")

        check_fn = partial(self.check, token, job.id)
        await poll_async(check_fn)

    # TODO: Run this sequentially until we fix https://gitlab.com/tinybird/analytics/-/issues/14668
    @pytest.mark.serial
    @tornado.testing.gen_test
    async def test_unlink_mat_node_population_is_cancelled_or_errors(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_unlink_mat_node_population_is_cancelled"
        ds_name_source = "ds_cancel_population_unlink"
        target_ds_name = "mat_view_node_ds_unlink"

        job_response = await self.create_population_for_cancellation(pipe_name, ds_name_source, target_ds_name)
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{pipe_name}_node/materialization?token={token}", method="DELETE"
        )
        self.assertEqual(response.code, 204)

        # we await for either a cancel status or error because we dropped a related resource needed for the population
        job = await wait_until_job_is_in_expected_status_async(
            job_response["id"],
            [JobStatus.CANCELLED, JobStatus.CANCELLING, JobStatus.ERROR],
            max_retries=400,
            elapsed_time_interval=0.1,
        )
        self.assertTrue(job.status in ["cancelled", "cancelling", "error"], job.status)
        self.assertEqual(job.kind, "populateview")

        check_fn = partial(self.check, token, job.id)
        await poll_async(check_fn)

    @tornado.testing.gen_test
    async def test_delete_pipe_population_is_cancelled_or_errors(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_delete_pipe_population_is_cancelled"
        ds_name_source = "ds_cancel_population"
        target_ds_name = "mat_view_node_ds"

        job_response = await self.create_population_for_cancellation(pipe_name, ds_name_source, target_ds_name)
        response = await self.fetch_async(f"/v0/pipes/{pipe_name}?token={token}", method="DELETE")
        self.assertEqual(response.code, 204)

        # we await for either a cancel status or error because we dropped a related resource needed for the population
        job = await wait_until_job_is_in_expected_status_async(
            job_response["id"],
            [JobStatus.CANCELLED, JobStatus.CANCELLING, JobStatus.ERROR],
            max_retries=400,
            elapsed_time_interval=0.1,
        )
        self.assertTrue(job.status in ["cancelled", "cancelling", "error"], job.status)
        self.assertEqual(job.kind, "populateview")

        check_fn = partial(self.check, token, job.id)
        await poll_async(check_fn)

    @tornado.testing.gen_test
    async def test_alter_landing_datasource_while_populate_is_running(self):
        pipe_name = "test_alter_landing_datasource_while_populate_is_running" + uuid.uuid4().hex
        ds_name_source = "ds_alter_landing_datasource_while_populate_is_running" + uuid.uuid4().hex
        target_ds_name = "mat_view_node_ds_alter_landing_datasource_while_populate_is_running" + uuid.uuid4().hex

        # Let's force a CHException to simulate the number of rows doesn't match
        real_query_sync = HTTPClient.query_sync

        def fake_query_sync(self, *args, **kwargs):
            if "populate" in args[0] and "INSERT INTO" in args[0]:
                query = args[0].split("FROM")[0] + "FROM numbers(100000)"
                return real_query_sync(self, query, **kwargs)
            return real_query_sync(self, *args, **kwargs)

        self.mpatch.setattr(HTTPClient, "query_sync", fake_query_sync)
        job_response = await self.create_population_for_cancellation(pipe_name, ds_name_source, target_ds_name)

        # alter the landing datasource
        params = {
            "token": self.admin_token,
            "schema": "number UInt64, new String, key String",
        }
        response = await self.fetch_async(
            f"/v0/datasources/{ds_name_source}/alter?{urlencode(params)}", method="POST", body=""
        )
        self.assertEqual(response.code, 200, response.body)
        await wait_until_job_is_in_expected_status_async(
            job_response["id"],
            [JobStatus.ERROR],
            max_retries=400,
            elapsed_time_interval=0.1,
        )

    @tornado.testing.gen_test
    async def test_stuck_monitor_task_detects_job_no_marked_as_error(self):
        pipe_name = "test_stuck_monitor_task_detects_job_no_marked_as_error" + uuid.uuid4().hex
        ds_name_source = "ds_stuck_monitor_task_detects_job_no_marked_as_error" + uuid.uuid4().hex
        target_ds_name = "mat_view_node_ds_stuck_monitor_task_detects_job_no_marked_as_error" + uuid.uuid4().hex
        real_query_sync = HTTPClient.query_sync
        real_query = HTTPClient.query

        # Let's force the INSERT query to raise a NUMBER_OF_COLUMNS_DOESNT_MATCH
        everything_prepare = asyncio.Event()

        def fake_query_sync(self, *args, **kwargs):
            if "populate" in args[0] and "INSERT INTO" in args[0]:
                query = args[0].split("FROM")[0] + "FROM numbers(100000)"
                return real_query_sync(self, query, **kwargs)
            return real_query_sync(self, *args, **kwargs)

        async def fake_query(self, *args, **kwargs):
            # Let's force the wait_for_query to not detect the error
            if re.search(r"event_date >= toDate\(now\(\) - INTERVAL \d+ (HOUR|DAY)\)", args[0]):
                everything_prepare.set()
                query = args[0].replace("FORMAT JSON", "LIMIT 0 FORMAT JSON")
                return await real_query(self, query, **kwargs)

            # The monitor task skips the last 5 minutes of logs to make sure we don't detect a false positive
            # For the tests, let's remove that condition
            elif "AND event_time < now() - INTERVAL 5 MINUTE" in args[0] and "exception" in args[0]:
                query = args[0].replace("AND event_time < now() - INTERVAL 5 MINUTE", "")
                return await real_query(self, query, **kwargs)

            return await real_query(self, *args, **kwargs)

        self.mpatch.setattr(HTTPClient, "query_sync", fake_query_sync)
        self.mpatch.setattr(HTTPClient, "query", fake_query)

        job_response = await self.create_population_for_cancellation(pipe_name, ds_name_source, target_ds_name)
        job_id = job_response["id"]
        await everything_prepare.wait()
        self.assertEqual(everything_prepare.is_set(), True)

        # Let's flush the logs to make sure the logs are there for the monitor task
        await ch_flush_logs_on_all_replicas(self.base_workspace.database_server, "tinybird")

        with self.assertLogs(level="WARNING") as mock_logs:
            task = OldAndStuckJobsMetricsMonitorTask()
            await task.action()

            self.assertIn(
                f"[JOB MONITOR] Job {job_id} is working but raised an exception in CH", " ".join(mock_logs.output)
            )

    @tornado.testing.gen_test
    async def test_slow_view_is_warning(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        # the setup of this test needs some ingestion so we are testing three scenarios in one test
        # materialize a node
        # append a materialize node
        # push a pipe with a materialize node
        # in the three scenarios there should be a warning in the response
        base_datasource_name = "landing_ds"
        csv_url = self.get_url_for_sql("SELECT number FROM numbers(100000) format CSVWithNames")
        params = {
            "token": token,
            "name": base_datasource_name,
            "mode": "append",
            "url": csv_url,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done")

        # create a pipe's node with a view to that datasource
        pipe_name = "slow_mat_view_pipe"
        Users.add_pipe_sync(u, pipe_name, "select * from landing_ds")
        node_name = "slow_mat_view_node"
        node_params = {"token": token, "name": node_name}
        node_sql = "SELECT count() as s FROM (SELECT * FROM landing_ds, landing_ds as a1, landing_ds as a2)"
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(node_params)}", method="POST", body=node_sql
        )
        self.assertEqual(response.code, 200)

        # materialize view
        target_ds_name = "slow_mat_view_node_ds"
        params = {"token": token, "datasource": target_ds_name}

        # materialization
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}/materialization?{urlencode(params)}", method="POST", body=""
        )
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        self.assertEqual(
            result.get("warnings")[0]["text"],
            "The performance of this query is not compatible with realtime ingestion.",
        )
        self.assertEqual(
            result.get("warnings")[0]["documentation"],
            "https://www.tinybird.co/docs/publish/materialized-views#why-am-i-getting-a-ui-error-message",
        )

        # delete materialization
        params = {"token": token}
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}?{urlencode(params)}", method="DELETE", body=None
        )
        self.assertEqual(response.code, 204, response.body)

        # append a materialized node
        node_params["type"] = "materialized"
        node_params["datasource"] = target_ds_name
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(node_params)}", method="POST", body=node_sql
        )
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        self.assertEqual(
            result.get("warnings")[0]["text"],
            "The performance of this query is not compatible with realtime ingestion.",
        )
        self.assertEqual(
            result.get("warnings")[0]["documentation"],
            "https://www.tinybird.co/docs/publish/materialized-views#why-am-i-getting-a-ui-error-message",
        )

        # delete the pipe
        response = await self.fetch_async(f"/v0/pipes/{pipe_name}?{urlencode(params)}", method="DELETE", body=None)

        # push the whole pipe
        node_params = {
            "name": f"{pipe_name}_view",
            "type": "materialized",
            "sql": node_sql,
            "datasource": target_ds_name,
        }

        params = {"token": token}

        pipe_def = {"name": pipe_name, "nodes": [node_params]}
        pipe_def = json.dumps(pipe_def)

        response = await self.fetch_async(
            f"/v0/pipes?{urlencode(params)}", method="POST", body=pipe_def, headers={"Content-type": "application/json"}
        )
        self.assertEqual(response.code, 200)
        pipe_node = json.loads(response.body)["nodes"][0]
        self.assertEqual(
            pipe_node.get("warnings")[0]["text"],
            "The performance of this query is not compatible with realtime ingestion.",
        )
        self.assertEqual(
            pipe_node.get("warnings")[0]["documentation"],
            "https://www.tinybird.co/docs/publish/materialized-views#why-am-i-getting-a-ui-error-message",
        )

    @patch("logging.error")
    @patch("logging.exception")
    @tornado.testing.gen_test
    async def test_view_creation_populate_on_cluster_with_query_log(self, mock_logging_error, mock_logging_exception):
        tb_api_proxy_async = TBApiProxyAsync(self)
        workspace_name = f"test_mat_batch3_ws_{uuid.uuid4().hex}"
        email = f"{workspace_name}@example.com"
        workspace = await tb_api_proxy_async.register_user_and_workspace(email, workspace_name)
        self.WORKSPACE_ID = workspace.id
        self.workspaces_to_delete.append(workspace)

        u = workspace
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_populate_on_cluster"
        Users.add_pipe_sync(u, pipe_name, "select 1")

        # let's create a datasource with some data
        ds_name_source = "ds_for_view_populate_on_cluster"
        params = {
            "token": token,
            "name": ds_name_source,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        s = StringIO("d,sales\n2019-01-01,2\n2019-01-02,3")
        response = await self.fetch_full_body_upload_async(create_url, s)
        self.assertEqual(response.code, 200, response.body)

        # create a pipe's node with a view to that datasource
        target_ds_name = "mat_view_node_ds"
        params = {
            "token": token,
            "name": "mat_view_node",
            "type": "materialized",
            "datasource": target_ds_name,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
            "populate": "true",
        }

        real_query_sync = HTTPClient.query_sync

        def fake_query_sync(self, *args, **kwargs):
            result = real_query_sync(self, *args, **kwargs)
            if kwargs.get("user_agent", "") == "no-tb-populate-query" and "SELECT DISTINCT partition" not in args[0]:
                raise CHException(
                    f"Code: {CHErrors.TIMEOUT_EXCEEDED}, e.displayText() = DB::Exception: Timeout exceeded: elapsed 10 seconds",
                    fatal=False,
                )

            return result

        self.mpatch.setattr(HTTPClient, "query_sync", fake_query_sync)

        real_query = HTTPClient.query
        test = self

        async def fake_query(self, *args, **kwargs):
            result = await real_query(self, *args, **kwargs)
            if (
                "system.query_log" in args[0]
                and "AND event_time > now()" in args[0]
                and kwargs.get("log_comment") != "QUERY_TRIGGERED_VIEWS"
            ):
                test.assertTrue("INTERVAL 1 HOUR" in args[0])
            return result

        self.mpatch.setattr(HTTPClient, "query", fake_query)

        async def mock_get_query_log(database_server, database, query_id, cluster="tinybird", elapsed=0):
            return await _get_query_log(database_server, database, query_id, cluster=cluster, elapsed=elapsed)

        with patch("tinybird.ch._get_query_log", side_effect=mock_get_query_log) as mock_query_log:
            query = f"SELECT toDate(d) AS d, sales * 10 AS fake_sales FROM {ds_name_source}"
            response = await self.fetch_async(
                f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query
            )
            pipe_node = json.loads(response.body)
            self.assertEqual(response.code, 200)
            self.assertEqual(pipe_node["name"], "mat_view_node")
            ds = Users.get_datasource(u, target_ds_name)
            self.assertEqual(pipe_node["materialized"], ds.id)
            self.assertIn("job", pipe_node)
            job_response = pipe_node["job"]
            self.assertEqual(job_response["id"], job_response["job_id"])
            self.assertEqual(job_response["kind"], JobKind.POPULATE)

            datasource = Users.get_datasource(u, target_ds_name)
            self.assertEqual(job_response["datasource"]["id"], datasource.id)

            # validate the view is there and returns correct schema and data
            job = await self.get_finalised_job_async(job_response["id"])
            self.assertEqual(job.status, "done", job.get("error", None))
            self.assertEqual(job.kind, "populateview")
            self.assertEqual(len(job.queries) > 0, True)
            self.assertEqual(job.queries[0]["query_id"] is not None, True, job.queries[0])
            for query in job.queries:
                self.assertEqual(query["status"], "done", query)
            self.assertEqual(job["datasource"]["name"], target_ds_name)

            # validate populate is being tracked on cluster
            self.assertGreaterEqual(mock_query_log.call_count, 1)
            mock_query_log.assert_called_with(mock.ANY, mock.ANY, mock.ANY, mock.ANY, elapsed=mock.ANY)

            self.assertEqual(mock_logging_error.call_count, 0, mock_logging_error.call_args_list)
            self.assertEqual(mock_logging_exception.call_count, 0, mock_logging_exception.call_args_list)

            initial_data = [{"d": "2019-01-01", "fake_sales": 20}, {"d": "2019-01-02", "fake_sales": 30}]

            async def assert_datasource():
                expected_schema = [{"name": "d", "type": "Date"}, {"name": "fake_sales", "type": "Int32"}]
                params = {
                    "token": token,
                    "q": f"SELECT * FROM {target_ds_name} ORDER BY d FORMAT JSON",
                }
                response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
                self.assertEqual(response.code, 200)
                payload = json.loads(response.body)
                self.assertEqual(payload["meta"], expected_schema)
                self.assertEqual(payload["data"], initial_data)

            await poll_async(assert_datasource)

            # add some data to the original datasource
            params = {
                "token": token,
                "name": ds_name_source,
                "mode": "append",
            }
            response = await self.fetch_async(
                f"/v0/datasources?{urlencode(params)}", method="POST", body="2019-01-03,10"
            )

            async def final_assert():
                # validate the view is there and returns the existing and the new data
                params = {
                    "token": token,
                    "q": f"SELECT * FROM {target_ds_name} ORDER BY d FORMAT JSON",
                }
                response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
                self.assertEqual(response.code, 200)
                payload = json.loads(response.body)
                self.assertEqual(payload["data"], [*initial_data, {"d": "2019-01-03", "fake_sales": 100}])

            await poll_async(final_assert)

    @tornado.testing.gen_test
    @patch("tinybird.ch.MAX_CRASH_COUNTER", 1)
    async def test_populate_marked_as_error_if_no_finish_in_query_log(self):
        tb_api_proxy_async = TBApiProxyAsync(self)
        rand = uuid.uuid4().hex
        workspace_name = f"test_mat_batch3_ws_{rand}"
        email = f"{workspace_name}@example.com"
        workspace = await tb_api_proxy_async.register_user_and_workspace(email, workspace_name)
        self.WORKSPACE_ID = workspace.id
        self.workspaces_to_delete.append(workspace)

        u = workspace
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = f"test_mat_view_populate_on_cluster_{rand[0:3]}"
        Users.add_pipe_sync(u, pipe_name, "select 1")

        # let's create a datasource with some data
        ds_name_source = f"ds_for_view_populate_on_cluster_{rand[0:3]}"
        params = {
            "token": token,
            "name": ds_name_source,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        s = StringIO("d,sales\n2019-01-01,2\n2019-01-02,3")
        response = await self.fetch_full_body_upload_async(create_url, s)
        self.assertEqual(response.code, 200, response.body)

        # create a pipe's node with a view to that datasource
        target_ds_name = f"mat_view_node_ds_{rand[0:3]}"
        params = {
            "token": token,
            "name": f"mat_view_node_{rand[0:3]}",
            "type": "materialized",
            "datasource": target_ds_name,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
            "populate": "true",
        }

        real_query_sync = HTTPClient.query_sync

        def fake_query_sync(self, *args, **kwargs):
            result = real_query_sync(self, *args, **kwargs)
            if kwargs.get("user_agent", "") == "no-tb-populate-query" and "SELECT DISTINCT partition" not in args[0]:
                raise CHException(
                    f"Code: {CHErrors.TIMEOUT_EXCEEDED}, e.displayText() = DB::Exception: Timeout exceeded: elapsed 10 seconds",
                    fatal=False,
                )

            return result

        self.mpatch.setattr(HTTPClient, "query_sync", fake_query_sync)

        async def mock_ch_get_query_status(database_server, cluster, query_id, is_first=True):
            return await _get_query_status(database_server, cluster, query_id, is_first=True)

        async def mock_get_query_log(database_server, database, query_id, cluster=None, elapsed=0):
            return ([{"type": "QueryStart", "event_time": "", "exception": ""}], {})

        with patch("tinybird.ch._get_query_status", side_effect=mock_ch_get_query_status) as mock_query_status:
            with patch("tinybird.ch._get_query_log", side_effect=mock_get_query_log) as mock_query_log:
                query = f"SELECT toDate(d) AS d, sales * 10 AS fake_sales FROM {ds_name_source}"
                response = await self.fetch_async(
                    f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query
                )
                self.assertEqual(response.code, 200)

                pipe_node = json.loads(response.body)
                job_response = pipe_node["job"]

                # validate the view is there and returns correct schema and data
                job = await self.get_finalised_job_async(job_response["id"])
                self.assertEqual(job.status, "error")
                self.assertEqual(
                    job.get("error"),
                    "Job failed due to an internal error: 00, try it again. If the problem persists, please contact us at support@tinybird.co",
                )

                # validate populate is being tracked on cluster
                self.assertGreaterEqual(mock_query_log.call_count, 1)
                self.assertGreaterEqual(mock_query_status.call_count, 1)
                mock_query_log.assert_called_with(mock.ANY, mock.ANY, mock.ANY, mock.ANY, elapsed=mock.ANY)

                # validate populate actually finished even when it was marked as error because the status couldn't be retrieved
                expected_schema = [{"name": "d", "type": "Date"}, {"name": "fake_sales", "type": "Int32"}]

                async def final_assert():
                    params = {
                        "token": token,
                        "q": f"SELECT * FROM {target_ds_name} ORDER BY d FORMAT JSON",
                    }
                    response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
                    self.assertEqual(response.code, 200)
                    payload = json.loads(response.body)
                    self.assertEqual(payload["meta"], expected_schema)
                    # we want to check there is no data if the populated failed
                    self.assertEqual(payload["data"], [])

                await poll_async(final_assert)

    @tornado.testing.gen_test
    @patch("tinybird.ch.MAX_QUERY_LOG_EMPTY_COUNTER", 1)
    async def test_populate_marked_as_error_if_no_query_log(self):
        tb_api_proxy_async = TBApiProxyAsync(self)
        rand = uuid.uuid4().hex
        workspace_name = f"test_mat_batch3_ws_{rand}"
        email = f"{workspace_name}@example.com"
        workspace = await tb_api_proxy_async.register_user_and_workspace(email, workspace_name)
        self.WORKSPACE_ID = workspace.id
        self.workspaces_to_delete.append(workspace)

        u = workspace
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = f"test_mat_view_populate_on_cluster_{rand[0:3]}"
        Users.add_pipe_sync(u, pipe_name, "select 1")

        # let's create a datasource with some data
        ds_name_source = f"ds_for_view_populate_on_cluster_{rand[0:3]}"
        params = {
            "token": token,
            "name": ds_name_source,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        s = StringIO("d,sales\n2019-01-01,2\n2019-01-02,3")
        response = await self.fetch_full_body_upload_async(create_url, s)
        self.assertEqual(response.code, 200, response.body)

        # create a pipe's node with a view to that datasource
        target_ds_name = f"mat_view_node_ds_{rand[0:3]}"
        params = {
            "token": token,
            "name": f"mat_view_node_{rand[0:3]}",
            "type": "materialized",
            "datasource": target_ds_name,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
            "populate": "true",
        }

        real_query_sync = HTTPClient.query_sync

        def fake_query_sync(self, *args, **kwargs):
            result = real_query_sync(self, *args, **kwargs)
            if kwargs.get("user_agent", "") == "no-tb-populate-query" and "SELECT DISTINCT partition" not in args[0]:
                raise CHException(
                    f"Code: {CHErrors.TIMEOUT_EXCEEDED}, e.displayText() = DB::Exception: Timeout exceeded: elapsed 10 seconds",
                    fatal=False,
                )

            return result

        self.mpatch.setattr(HTTPClient, "query_sync", fake_query_sync)

        async def mock_ch_get_query_status(database_server, cluster, query_id, is_first=True):
            return await _get_query_status(database_server, cluster, query_id, is_first=True)

        async def mock_get_query_log(database_server, database, query_id, cluster=None, elapsed=0):
            return ([], {})

        with patch("tinybird.ch._get_query_status", side_effect=mock_ch_get_query_status) as mock_query_status:
            with patch("tinybird.ch._get_query_log", side_effect=mock_get_query_log) as mock_query_log:
                query = f"SELECT toDate(d) AS d, sales * 10 AS fake_sales FROM {ds_name_source}"
                response = await self.fetch_async(
                    f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query
                )
                self.assertEqual(response.code, 200)

                pipe_node = json.loads(response.body)
                job_response = pipe_node["job"]

                # validate the view is there and returns correct schema and data
                job = await self.get_finalised_job_async(job_response["id"])
                self.assertEqual(job.status, "error")
                self.assertEqual(
                    job.get("error"),
                    "Job failed due to an internal error: 01, try it again. If the problem persists, please contact us at support@tinybird.co",
                )

                # validate populate is being tracked on cluster
                self.assertGreaterEqual(mock_query_log.call_count, 1)
                self.assertGreaterEqual(mock_query_status.call_count, 1)
                mock_query_log.assert_called_with(mock.ANY, mock.ANY, mock.ANY, mock.ANY, elapsed=mock.ANY)

                # validate populate actually finished even when it was marked as error because the status couldn't be retrieved
                expected_schema = [{"name": "d", "type": "Date"}, {"name": "fake_sales", "type": "Int32"}]

                async def final_assert():
                    params = {
                        "token": token,
                        "q": f"SELECT * FROM {target_ds_name} ORDER BY d FORMAT JSON",
                    }
                    response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
                    self.assertEqual(response.code, 200)
                    payload = json.loads(response.body)
                    self.assertEqual(payload["meta"], expected_schema)
                    # we want to check there is no data if the populated failed
                    self.assertEqual(payload["data"], [])

                await poll_async(final_assert)


class TestAPIPipesMaterializedViews(TestAPIPipeStats):
    def setUp(self):
        super().setUp()
        self.create_test_datasource()

    def test_invalid_params(self):
        invalid_params_scenarios = [
            (
                {"type": "invalid_type"},
                "Invalid node type: 'invalid_type', valid types are: materialized, endpoint, standard, copy, sink, stream",
            ),
            ({"type": "materialized"}, "The 'datasource' parameter is mandatory."),
        ]
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_errors"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")
        for params, expected_error in invalid_params_scenarios:
            with self.subTest(params=params, expected_error=expected_error):
                params["token"] = token
                response = self.fetch(
                    f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}",
                    method="POST",
                    body="select count() c from test_table where a > 4",
                )
                result = json.loads(response.body)
                self.assertEqual(response.code, 400)
                self.assertEqual(result["error"], expected_error)

    def test_appending_materialized_node_fails_if_sql_is_a_template(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_happy_case"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # let's create a datasource
        ds_name = "ds_for_view_engine"
        params = {
            "token": token,
            "name": ds_name,
            "schema": "a UInt64",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        # create a pipe's node with a view to that datasource
        target_ds_name = "mat_view_node_ds"
        params = {
            "token": token,
            "name": "mat_view_node",
            "type": "materialized",
            "datasource": target_ds_name,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
        }
        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}",
            method="POST",
            body=f"% select a * 2 as b, a * 3 as c from {ds_name}",
        )
        result = json.loads(response.body)

        self.assertEqual(response.code, 400)
        self.assertTrue(
            "Materialized nodes don't support templates. Please remove any `{% ... %}` template code or the `%` mark from this pipe node."
            in result.get("error")
        )
        self.assertIsNotNone(result.get("documentation"))

    def test_appending_materialized_node_targeting_a_non_existing_datasource_requires_token_with_datasource_create(
        self,
    ):
        u = Users.get_by_id(self.WORKSPACE_ID)

        pipe_name = "test_mat_view_happy_case"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # let's create a datasource
        ds_name = "ds_for_view_engine"
        params = {
            "token": Users.get_token_for_scope(u, scopes.ADMIN),
            "name": ds_name,
            "schema": "a UInt64",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        # Create token with just PIPES_CREATE scope
        token = Users.add_token(u, "pipe_with_materialized_node", scopes.PIPES_CREATE)

        # create a pipe's node with a view to that datasource
        target_ds_name = "mat_view_node_ds"
        params = {
            "token": token,
            "name": "mat_view_node",
            "type": "materialized",
            "datasource": target_ds_name,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
        }
        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}",
            method="POST",
            body=f"select a * 2 as b, a * 3 as c from {ds_name}",
        )
        result = json.loads(response.body)
        self.assertEqual(response.code, 403)
        self.assertEqual(
            result.get("error"),
            "Forbidden. Provided token doesn't have permissions to create the datasource "
            "required in the materialized node, it also needs ``ADMIN`` or "
            "``DATASOURCES:CREATE`` scope.",
        )
        self.assertIsNotNone(result.get("documentation"))

    @tornado.testing.gen_test
    async def test_view_creation_engine_happy_case(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_happy_case"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # let's create a datasource
        ds_name = "ds_for_view_engine"
        params = {
            "token": token,
            "name": ds_name,
            "schema": "a UInt64",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        # create a pipe's node with a view to that datasource
        target_ds_name = "mat_view_node_ds"
        params = {
            "token": token,
            "name": "mat_view_node",
            "type": "materialized",
            "datasource": target_ds_name,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
        }
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}",
            method="POST",
            body=f"select a * 2 as b, a * 3 as c from {ds_name}",
        )
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(pipe_node["name"], "mat_view_node")
        ds = Users.get_datasource(u, target_ds_name)
        self.assertEqual(pipe_node["materialized"], ds.id)
        self.assertEqual(pipe_node["cluster"], pipe_node["cluster"])

        # validate the view is there and returns correct schema
        expected_schema = [{"name": "b", "type": "UInt64"}, {"name": "c", "type": "UInt64"}]
        params = {
            "token": token,
            "q": f"SELECT * FROM {target_ds_name} FORMAT JSON",
        }
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200)
        payload = json.loads(response.body)
        self.assertEqual(payload["meta"], expected_schema)
        self.assertEqual(payload["data"], [])

        # add some data to the original datasource
        data = [1, 2, 3]
        params = {
            "token": token,
            "name": ds_name,
            "mode": "append",
        }
        response = await self.fetch_async(
            f"/v0/datasources?{urlencode(params)}", method="POST", body="\n".join([str(d) for d in data])
        )

        # validate the view is there and returns new data
        async def assert_datasource():
            params = {
                "token": token,
                "q": f"SELECT * FROM {target_ds_name} FORMAT JSON",
            }
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            self.assertEqual(response.code, 200)
            payload = json.loads(response.body)
            self.assertEqual(payload["data"], [{"b": d * 2, "c": d * 3} for d in data])

        await poll_async(assert_datasource)

        # add extra node using the previous node
        params = {
            "token": token,
            "name": "read_from_mat_view",
        }
        query = "select * from mat_view_node"
        response = await self.fetch_async(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)

    @tornado.testing.gen_test
    async def test_view_creation_then_update_pipe_name_with_materialized_nodes(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "_test_mat_view_original_name"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # let's create a datasource
        ds_name = "ds_for_view_engine"
        params = {
            "token": token,
            "name": ds_name,
            "schema": "a UInt64",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        # create a pipe's node with a view to that datasource
        target_ds_name = "mat_view_node_ds"
        params = {
            "token": token,
            "name": "mat_view_node",
            "type": "materialized",
            "datasource": target_ds_name,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
        }
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}",
            method="POST",
            body=f"select a * 2 as b, a * 3 as c from {ds_name}",
        )
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(pipe_node["name"], "mat_view_node")
        ds = Users.get_datasource(u, target_ds_name)
        self.assertEqual(pipe_node["materialized"], ds.id)
        self.assertEqual(pipe_node["cluster"], pipe_node["cluster"])

        # update pipe with materialized node
        new_pipe_name = "test_mat_view_updated_name"
        params = {"token": token, "name": new_pipe_name}
        response = await self.fetch_async(f"/v0/pipes/{pipe_name}?{urlencode(params)}", method="PUT", body=b"")
        _ = json.loads(response.body)
        self.assertEqual(response.code, 200)

        # validate the view is there and returns correct schema
        async def assert_datasource():
            expected_schema = [{"name": "b", "type": "UInt64"}, {"name": "c", "type": "UInt64"}]
            params = {
                "token": token,
                "q": f"SELECT * FROM {target_ds_name} FORMAT JSON",
            }
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            self.assertEqual(response.code, 200)
            payload = json.loads(response.body)
            self.assertEqual(payload["meta"], expected_schema)
            self.assertEqual(payload["data"], [])

        await poll_async(assert_datasource)
        # add extra node using the previous node
        params = {
            "token": token,
            "name": "read_from_mat_view",
        }
        query = "select * from mat_view_node"
        response = await self.fetch_async(
            f"/v0/pipes/{new_pipe_name}/nodes?{urlencode(params)}", method="POST", body=query
        )
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)

    def test_view_creation_engine_deletion_exception_raises_error(self):
        u, token, pipe_name, pipe_node, ds = self._prepare_test_view_creation_engine_deletes_mat_view()

        # delete node
        params = {"token": token}
        with mock.patch("tinybird.ch.HTTPClient.query", side_effect=Exception("timeout")):
            response = self.fetch(
                f"/v0/pipes/{pipe_name}/nodes/{pipe_node['name']}?{urlencode(params)}", method="DELETE", body=None
            )
        self.assertEqual(response.code, 409)

        # materialized view is not gone
        self._check_table_in_database(u.database, pipe_node["id"], exists=True)
        # Data Source is not gone
        self._check_table_in_database(u.database, ds.id, exists=True)

        with mock.patch("tinybird.ch.HTTPClient.query", side_effect=Exception("timeout")):
            response = self.fetch(
                f"/v0/pipes/{pipe_name}/nodes/{pipe_node['name']}/materialization?{urlencode(params)}",
                method="DELETE",
                body=None,
            )
        self.assertEqual(response.code, 409)

        # materialized view is not gone
        self._check_table_in_database(u.database, pipe_node["id"], exists=True)
        # Data Source is not gone
        self._check_table_in_database(u.database, ds.id, exists=True)

        with mock.patch("tinybird.ch.HTTPClient.query", side_effect=Exception("timeout")):
            response = self.fetch(f"/v0/pipes/{pipe_name}?{urlencode(params)}", method="DELETE", body=None)
        self.assertEqual(response.code, 409)

        # materialized view is not gone
        self._check_table_in_database(u.database, pipe_node["id"], exists=True)
        # Data Source is not gone
        self._check_table_in_database(u.database, ds.id, exists=True)

    @tornado.testing.gen_test
    async def test_view_creation_populate_source_ttl(self):
        """
        source (with data out of ttl) -> mv -> target (no data because of ttl)
        """
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        rdm = uuid.uuid4().hex[0:4]
        base = f"test_view_creation_populate_source_ttl{rdm}"
        pipe_name = f"p_{base}"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # let's create a datasource with some data
        ds_name_source = f"ds_{base}"
        params = {
            "token": token,
            "name": ds_name_source,
            "schema": "date DateTime, number Int32",
            "engine": "MergeTree",
            "engine_sorting_key": "date",
            "engine_ttl": "toDate(date) + interval 1 day",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        params = {
            "token": token,
            "name": ds_name_source,
            "mode": "append",
            "url": self.get_url_for_sql("select now() - interval 1 month as date, number from numbers(100)"),
        }
        append_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(append_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)
        job = await self.get_finalised_job_async(json.loads(response.body)["job_id"])
        self.assertEqual(job.status, "done", job.get("error", None))

        params = {
            "token": token,
            "name": ds_name_source,
            "mode": "append",
            "url": self.get_url_for_sql("select now() - interval 2 month as date, number from numbers(100)"),
        }
        append_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(append_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)
        job = await self.get_finalised_job_async(json.loads(response.body)["job_id"])
        self.assertEqual(job.status, "done", job.get("error", None))

        u = Users.get_by_id(self.WORKSPACE_ID)
        ds = Users.get_datasource(u, ds_name_source)
        self.wait_for_datasource_replication(u, ds)
        exec_sql(
            u.database,
            f"OPTIMIZE TABLE {u.database}.{ds.id} ON CLUSTER {u.cluster} FINAL",
            extra_params={"alter_sync": 2},
        )

        async def check_rows():
            params = {
                "token": token,
                "q": f"SELECT count() c FROM {ds_name_source} FORMAT JSON",
            }
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            self.assertEqual(response.code, 200)
            self.assertEqual(json.loads(response.body)["data"][0]["c"], 0, response.body)

        await poll_async(check_rows)

        # create a pipe's node with a view to that datasource
        target_ds_name = f"t_{base}"
        params = {
            "token": token,
            "name": f"n_{base}",
            "type": "materialized",
            "datasource": target_ds_name,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
            "populate": "true",
        }
        query = f"SELECT * FROM {ds_name_source}"
        response = await self.fetch_async(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)
        job_response = pipe_node["job"]
        job = await self.get_finalised_job_async(job_response["id"])
        self.assertEqual(job.status, "done", job.get("error", None))
        self.assertEqual(job.kind, "populateview")
        self.assertEqual(len(job.queries) > 0, True)
        self.assertEqual(job.queries[0]["query_id"] is not None, True, job.queries[0])
        for query in job.queries:
            self.assertEqual(query["status"], "done", query)

        r = await self.get_query_logs_async(job.queries[0]["query_id"], u.database)

        self.assertTrue("toDate(date) >= (now() - toIntervalDay(1))" in r[0]["query"])

        # validate the view is there and returns nothing due to data filtered by the TTL expression on the source table
        async def assert_datasource():
            params = {
                "token": token,
                "q": f"SELECT count() c FROM {target_ds_name} FORMAT JSON",
            }
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            self.assertEqual(response.code, 200)
            self.assertEqual(json.loads(response.body)["data"][0]["c"], 0, response.body)

        await poll_async(assert_datasource)

    @tornado.testing.gen_test
    async def test_populate_itx_stock(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        ds_source_name = "ds_stock"
        tb_api_proxy_async = TBApiProxyAsync(self)
        ds = await tb_api_proxy_async.create_datasource(
            token=token,
            ds_name="ds_stock",
            schema="`snapshot_id` DateTime, `EVENT_DATE` DateTime64(3), `EVENT_PK` String, `FECHA_MODIFICACION` String, `ID_LOCALIZACION` Int32, `ID_INSTALACION_RFID` Int32, `UBICACION_RFID` Int16, `COD_PRODUCTO_AS400` Int16, `MODELO` Int32, `CALIDAD` Int32, `COLOR` Int32, `TALLA` Int16, `OP` String, `UNIDADES` Int32",
            engine_params={
                "engine": "MergeTree",
                "engine_sorting_key": "snapshot_id, ID_LOCALIZACION, ID_INSTALACION_RFID, COD_PRODUCTO_AS400, MODELO, CALIDAD, COLOR, TALLA, UBICACION_RFID",
                "engine_ttl": "snapshot_id + toIntervalHour(1)",
                "engine_partition_key": "toStartOfHour(snapshot_id)",
            },
        )

        # Add the settings manually so the end up in the end of the settings declaration
        table = f'{u.database}.{ds["datasource"]["id"]}'
        client = HTTPClient(host=CH_ADDRESS, database=u.database)
        await client.query(
            f"ALTER TABLE {table} ON CLUSTER tinybird modify setting ttl_only_drop_parts = 1", read_only=False
        )
        await client.query(
            f"ALTER TABLE {table} ON CLUSTER tinybird modify setting merge_with_ttl_timeout = 1800", read_only=False
        )

        csv_url = self.get_url_for_sql(
            """
            SELECT  now() - INTERVAL number MINUTE as snapshot_id,
                    now()::DateTime64(3) as `EVENT_DATE`,
                    '1' as `EVENT_PK`,
                    now()::String as `FECHA_MODIFICACION`,
                    1 as `ID_LOCALIZACION`,
                    1 as `ID_INSTALACION_RFID`,
                    1 as `UBICACION_RFID`,
                    1 as `COD_PRODUCTO_AS400`,
                    1 as `MODELO`,
                    1 as `CALIDAD`,
                    1 as `COLOR`,
                    1 as `TALLA`,
                    'op' as `OP`,
                    number as `UNIDADES`
            FROM numbers(1000)
            """
        )

        params = {
            "token": token,
            "name": ds_source_name,
            "mode": "append",
            "url": csv_url,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done")

        ds_target_name = "tb_stock_mv_0_mv"
        pipe_name = "tb_stock_mv"
        Users.add_pipe_sync(u, pipe_name, nodes=[])

        node_sql = """
            SELECT snapshot_id, COD_PRODUCTO_AS400, MODELO, CALIDAD, sumSimpleState(UNIDADES) AS UNIDADES
            FROM ds_stock
            GROUP BY snapshot_id, COD_PRODUCTO_AS400, MODELO, CALIDAD
        """
        node_name = "tb_stock_mv_0"
        params = {
            "token": token,
            "name": node_name,
            "type": "materialized",
            "datasource": ds_target_name,
            "populate": "true",
            "override_datasource": "true",
        }
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=node_sql
        )
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(pipe_node["name"], node_name)
        job_response = pipe_node["job"]
        self.assertEqual(job_response["id"], job_response["job_id"])
        self.assertEqual(job_response["kind"], JobKind.POPULATE)
        job_end = await self.get_finalised_job_async(job_response["id"])
        self.assertEqual(job_end["status"], "done", job_end)

    @tornado.testing.gen_test
    async def test_view_creation_populate_shared_source_ttl(self):
        """
        a.source (with data out of ttl) -> b.mv -> b.target (no data because of ttl)
        """
        tb_api_proxy_async = TBApiProxyAsync(self)
        workspace_a = Users.get_by_id(self.WORKSPACE_ID)
        user_a = UserAccount.get_by_id(self.USER_ID)
        token_workspace_a = Users.get_token_for_scope(workspace_a, scopes.ADMIN_USER)
        token_user_a = UserAccount.get_token_for_scope(user_a, scopes.AUTH)

        ws_b_email = f"test_view_with_shared_{uuid.uuid4().hex}@example.com"
        workspace_b = await tb_api_proxy_async.register_user_and_workspace(
            ws_b_email, workspace_a.name, normalize_name_and_try_different_on_collision=True
        )
        workspace_a = Users.get_by_id(self.WORKSPACE_ID)
        user_b = UserAccount.get_by_email(ws_b_email)
        token_user_b = UserAccount.get_token_for_scope(user_b, scopes.AUTH)
        token_workspace_b = Users.get_token_for_scope(workspace_b, scopes.ADMIN)

        await tb_api_proxy_async.invite_user_to_workspace(
            token=token_user_b, workspace_id=workspace_b.id, user_to_invite_email=user_a.email
        )

        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        rdm = uuid.uuid4().hex[0:4]
        base = f"test_view_creation_populate_shared_source_ttl{rdm}"
        pipe_name = f"p_{base}"
        Users.add_pipe_sync(workspace_b, pipe_name, "select * from test_table")

        ds_name_source = f"ds_{base}"

        datasource_a_in_workspace_a = await tb_api_proxy_async.create_datasource(
            token=token_workspace_a,
            ds_name=ds_name_source,
            schema="date DateTime, number Int32",
            engine_params={
                "engine": "MergeTree",
                "engine_sorting_key": "date",
                "engine_ttl": "toDate(date) + interval 1 day",
            },
        )

        datasource_a_in_workspace_b = await tb_api_proxy_async.share_datasource_with_another_workspace(
            token=token_user_a,
            datasource_id=datasource_a_in_workspace_a["datasource"]["id"],
            origin_workspace_id=workspace_a.id,
            destination_workspace_id=workspace_b.id,
        )

        params = {
            "token": token,
            "name": ds_name_source,
            "mode": "append",
            "url": self.get_url_for_sql("select now() - interval 1 month as date, number from numbers(100)"),
        }
        append_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(append_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)
        job = await self.get_finalised_job_async(json.loads(response.body)["job_id"])
        self.assertEqual(job.status, "done", job.get("error", None))

        params = {
            "token": token,
            "name": ds_name_source,
            "mode": "append",
            "url": self.get_url_for_sql("select now() - interval 2 month as date, number from numbers(100)"),
        }
        append_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(append_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)
        job = await self.get_finalised_job_async(json.loads(response.body)["job_id"])
        self.assertEqual(job.status, "done", job.get("error", None))

        u = Users.get_by_id(self.WORKSPACE_ID)
        ds = Users.get_datasource(u, ds_name_source)
        self.wait_for_datasource_replication(u, ds)

        exec_sql(
            u.database,
            f"OPTIMIZE TABLE {u.database}.{ds.id} ON CLUSTER {u.cluster} FINAL",
            extra_params={"alter_sync": 2},
        )

        async def check_rows():
            params = {
                "token": token,
                "q": f"SELECT count() c FROM {ds_name_source} FORMAT JSON",
            }
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            self.assertEqual(response.code, 200)
            self.assertEqual(json.loads(response.body)["data"][0]["c"], 0, response.body)

        await poll_async(check_rows)

        # create a pipe's node with a view to that datasource
        target_ds_name = f"t_{base}"
        params = {
            "token": token_workspace_b,
            "name": f"n_{base}",
            "type": "materialized",
            "datasource": target_ds_name,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
            "populate": "true",
        }
        query = f"SELECT * FROM {datasource_a_in_workspace_b.name}"
        response = await self.fetch_async(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)
        job_response = pipe_node["job"]
        self.WORKSPACE_ID = workspace_b.id
        job = await self.get_finalised_job_async(job_response["id"])
        self.assertEqual(job.status, "done", job.get("error", None))
        self.assertEqual(job.kind, "populateview")
        self.assertEqual(len(job.queries) > 0, True)
        self.assertEqual(job.queries[0]["query_id"] is not None, True, job.queries[0])
        for query in job.queries:
            self.assertEqual(query["status"], "done", query)

        r = await self.get_query_logs_by_where_async(f"query_id = '{job.queries[0]['query_id']}'")

        self.assertTrue("toDate(date) >= (now() - toIntervalDay(1))" in r[0]["query"])

        # validate the view is there and returns nothing due to data filtered by the TTL expression on the source table
        async def assert_datasource():
            params = {
                "token": token_workspace_b,
                "q": f"SELECT count() c FROM {target_ds_name} FORMAT JSON",
            }
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            self.assertEqual(response.code, 200)
            self.assertEqual(json.loads(response.body)["data"][0]["c"], 0, response.body)

        await poll_async(assert_datasource)

    @tornado.testing.gen_test
    async def test_view_creation_populate_target_ttl(self):
        """
        source (with data) -> mv -> target (no data because of target ttl)
        """
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        rdm = uuid.uuid4().hex[0:4]
        base = f"test_view_creation_populate_target_ttl{rdm}"
        pipe_name = f"p_{base}"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # let's create a datasource with some data
        ds_name_source = f"ds_{base}"
        params = {
            "token": token,
            "name": ds_name_source,
            "schema": "date DateTime, number Int32",
            "engine": "MergeTree",
            "engine_sorting_key": "date",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        params = {
            "token": token,
            "name": ds_name_source,
            "mode": "append",
            "url": self.get_url_for_sql("select now() - interval 1 month as date, number from numbers(100)"),
        }
        append_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(append_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)
        job = await self.get_finalised_job_async(json.loads(response.body)["job_id"])
        self.assertEqual(job.status, "done", job.get("error", None))

        async def check_rows():
            params = {
                "token": token,
                "q": f"SELECT count() c FROM {ds_name_source} FORMAT JSON",
            }
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            self.assertEqual(response.code, 200)
            self.assertEqual(json.loads(response.body)["data"][0]["c"], 100, response.body)

        await poll_async(check_rows)

        # create a pipe's node with a view to that datasource
        target_ds_name = f"t_{base}"
        params = {
            "token": token,
            "name": f"n_{base}",
            "type": "materialized",
            "datasource": target_ds_name,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
            "engine_ttl": "toDate(date) + interval 1 day",
            "populate": "true",
        }
        query = f"SELECT * FROM {ds_name_source}"
        response = await self.fetch_async(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)
        job_response = pipe_node["job"]
        job = await self.get_finalised_job_async(job_response["id"])
        self.assertEqual(job.status, "done", job.get("error", None))
        self.assertEqual(job.kind, "populateview")
        self.assertEqual(len(job.queries) > 0, True)
        self.assertEqual(job.queries[0]["query_id"] is not None, True, job.queries[0])
        for query in job.queries:
            self.assertEqual(query["status"], "done", query)
        self.assertEqual(job["datasource"]["name"], target_ds_name)

        r = await self.get_query_logs_by_where_async(
            f"""query like 'CREATE MATERIALIZED%' AND splitByChar(' ', query)[7] in
                                                        (
                                                            SELECT views[1]
                                                            FROM system.query_log
                                                            WHERE
                                                                query_id = '{job.queries[0]["query_id"]}'
                                                            LIMIT 1
                                                        )"""
        )

        self.assertTrue("toDate(date) >= now() - toIntervalDay(1)" in r[0]["query"])

        # validate the view is there and returns nothing due to data filtered by the TTL expression on the target table
        async def assert_datasource():
            params = {
                "token": token,
                "q": f"SELECT count() c FROM {target_ds_name} FORMAT JSON",
            }
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            self.assertEqual(response.code, 200)
            self.assertEqual(json.loads(response.body)["data"][0]["c"], 0, response.body)

        await poll_async(assert_datasource)

    @tornado.testing.gen_test
    async def test_view_creation_populate_query_ttl(self):
        """
        source (with data), source_2 (with data out of ttl) -> mv -> target (no data because of source_2 ttl)
        """
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        rdm = uuid.uuid4().hex[0:4]
        base = f"test_view_creation_populate_query_ttl{rdm}"
        pipe_name = f"p_{base}"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # let's create a datasource with some data
        ds_name_source = f"ds_{base}"
        params = {
            "token": token,
            "name": ds_name_source,
            "schema": "date DateTime, number Int32",
            "engine": "MergeTree",
            "engine_sorting_key": "date",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        params = {
            "token": token,
            "name": ds_name_source,
            "mode": "append",
            "url": self.get_url_for_sql("select now() - interval 1 month as date, number from numbers(100)"),
        }
        append_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(append_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)
        job = await self.get_finalised_job_async(json.loads(response.body)["job_id"])
        self.assertEqual(job.status, "done", job.get("error", None))

        params = {
            "token": token,
            "q": f"SELECT count() c FROM {ds_name_source} FORMAT JSON",
        }
        self.wait_for_datasource_replication(u, ds_name_source)
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body)["data"][0]["c"], 100, response.body)

        # let's create a datasource with some data
        ds_name_source_2 = f"ds_{base}_2"
        params = {
            "token": token,
            "name": ds_name_source_2,
            "schema": "date DateTime, number Int32",
            "engine": "MergeTree",
            "engine_sorting_key": "date",
            "engine_ttl": "toDate(date) + interval 1 day",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        params = {
            "token": token,
            "name": ds_name_source_2,
            "mode": "append",
            "url": self.get_url_for_sql("select now() - interval 1 month as date, number from numbers(100)"),
        }
        append_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(append_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)
        job = await self.get_finalised_job_async(json.loads(response.body)["job_id"])
        self.assertEqual(job.status, "done", job.get("error", None))

        params = {
            "token": token,
            "name": ds_name_source_2,
            "mode": "append",
            "url": self.get_url_for_sql("select now() - interval 1 month as date, number from numbers(100)"),
        }
        append_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(append_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)
        job = await self.get_finalised_job_async(json.loads(response.body)["job_id"])
        self.assertEqual(job.status, "done", job.get("error", None))

        u = Users.get_by_id(self.WORKSPACE_ID)
        ds = Users.get_datasource(u, ds_name_source_2)
        self.wait_for_datasource_replication(u, ds)
        exec_sql(
            u.database,
            f"OPTIMIZE TABLE {u.database}.{ds.id} ON CLUSTER {u.cluster} FINAL",
            extra_params={"alter_sync": 2},
        )

        async def check_rows():
            params = {
                "token": token,
                "q": f"SELECT count() c FROM {ds_name_source_2} FORMAT JSON",
            }
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            self.assertEqual(response.code, 200)
            self.assertEqual(json.loads(response.body)["data"][0]["c"], 0, response.body)

        await poll_async(check_rows)

        # create a pipe's node with a view to that datasource
        target_ds_name = f"t_{base}"
        params = {
            "token": token,
            "name": f"n_{base}",
            "type": "materialized",
            "datasource": target_ds_name,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
            "populate": "true",
        }
        query = f"SELECT * FROM {ds_name_source} where number in (SELECT number FROM {ds_name_source_2})"
        response = await self.fetch_async(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)
        job_response = pipe_node["job"]
        job = await self.get_finalised_job_async(job_response["id"])
        self.assertEqual(job.status, "done", job.get("error", None))
        self.assertEqual(job.kind, "populateview")
        self.assertEqual(len(job.queries) > 0, True)
        self.assertEqual(job.queries[0]["query_id"] is not None, True, job.queries[0])
        for query in job.queries:
            self.assertEqual(query["status"], "done", query)
        self.assertEqual(job["datasource"]["name"], target_ds_name)

        await ch_flush_logs_on_all_replicas(u.database_server, "tinybird")
        query = f"""SELECT
                        query
                    FROM clusterAllReplicas(tinybird, system.query_log)
                    WHERE
                        query like 'CREATE MATERIALIZED%' AND splitByChar(' ', query)[7] in
                        (
                            SELECT views[1]
                            FROM system.query_log
                            WHERE
                                query_id = '{job.queries[0]["query_id"]}'
                            LIMIT 1
                        )
                    FORMAT JSON"""
        r = exec_sql(u.database, query)
        self.assertTrue("toDate(date) >= (now() - toIntervalDay(1))" in r["data"][0]["query"])

        # validate the view is there and returns nothing due to data filtered by the TTL expression on one table in the query
        async def assert_datasource():
            params = {
                "token": token,
                "q": f"SELECT count() c FROM {target_ds_name} FORMAT JSON",
            }
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            self.assertEqual(response.code, 200)
            self.assertEqual(json.loads(response.body)["data"][0]["c"], 0, response.body)

        await poll_async(assert_datasource)

    @tornado.testing.gen_test
    async def test_view_creation_populate_shared_query_ttl(self):
        """
        a.source (with data), a.source_2 (with data out of ttl) -> b.mv -> b.target (no data because of source_2 ttl)
        """
        tb_api_proxy_async = TBApiProxyAsync(self)
        workspace_a = Users.get_by_id(self.WORKSPACE_ID)
        user_a = UserAccount.get_by_id(self.USER_ID)
        token_workspace_a = Users.get_token_for_scope(workspace_a, scopes.ADMIN_USER)
        token_user_a = UserAccount.get_token_for_scope(user_a, scopes.AUTH)

        ws_b_email = f"test_view_with_shared_{uuid.uuid4().hex}@example.com"
        workspace_b = await tb_api_proxy_async.register_user_and_workspace(
            ws_b_email, workspace_a.name, normalize_name_and_try_different_on_collision=True
        )
        workspace_a = Users.get_by_id(self.WORKSPACE_ID)
        user_b = UserAccount.get_by_email(ws_b_email)
        token_user_b = UserAccount.get_token_for_scope(user_b, scopes.AUTH)
        token_workspace_b = Users.get_token_for_scope(workspace_b, scopes.ADMIN)

        await tb_api_proxy_async.invite_user_to_workspace(
            token=token_user_b, workspace_id=workspace_b.id, user_to_invite_email=user_a.email
        )

        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        rdm = uuid.uuid4().hex[0:4]
        base = f"test_view_creation_populate_shared_query_ttl{rdm}"
        pipe_name = f"p_{base}"
        Users.add_pipe_sync(workspace_b, pipe_name, "select * from test_table")

        ds_name_source = f"ds_{base}"

        datasource_a_in_workspace_a = await tb_api_proxy_async.create_datasource(
            token=token_workspace_a,
            ds_name=ds_name_source,
            schema="date DateTime, number Int32",
            engine_params={
                "engine": "MergeTree",
                "engine_sorting_key": "date",
            },
        )

        datasource_a_in_workspace_b = await tb_api_proxy_async.share_datasource_with_another_workspace(
            token=token_user_a,
            datasource_id=datasource_a_in_workspace_a["datasource"]["id"],
            origin_workspace_id=workspace_a.id,
            destination_workspace_id=workspace_b.id,
        )

        ds_name_source_2 = f"{ds_name_source}_2"
        datasource_a_2_in_workspace_a = await tb_api_proxy_async.create_datasource(
            token=token_workspace_a,
            ds_name=ds_name_source_2,
            schema="date DateTime, number Int32",
            engine_params={
                "engine": "MergeTree",
                "engine_sorting_key": "date",
                "engine_ttl": "toDate(date) + interval 1 day",
            },
        )

        datasource_a_2_in_workspace_b = await tb_api_proxy_async.share_datasource_with_another_workspace(
            token=token_user_a,
            datasource_id=datasource_a_2_in_workspace_a["datasource"]["id"],
            origin_workspace_id=workspace_a.id,
            destination_workspace_id=workspace_b.id,
        )

        params = {
            "token": token,
            "name": ds_name_source,
            "mode": "append",
            "url": self.get_url_for_sql("select now() - interval 1 month as date, number from numbers(100)"),
        }
        append_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(append_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)
        job = await self.get_finalised_job_async(json.loads(response.body)["job_id"])
        self.assertEqual(job.status, "done", job.get("error", None))

        async def check_row_count():
            params = {
                "token": token,
                "q": f"SELECT count() c FROM {ds_name_source} FORMAT JSON",
            }
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            self.assertEqual(response.code, 200)
            self.assertEqual(json.loads(response.body)["data"][0]["c"], 100, response.body)

        await poll_async(check_row_count)

        params = {
            "token": token,
            "name": ds_name_source_2,
            "mode": "append",
            "url": self.get_url_for_sql("select now() - interval 2 month as date, number from numbers(100)"),
        }
        append_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(append_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)
        job = await self.get_finalised_job_async(json.loads(response.body)["job_id"])
        self.assertEqual(job.status, "done", job.get("error", None))

        params = {
            "token": token,
            "name": ds_name_source_2,
            "mode": "append",
            "url": self.get_url_for_sql("select now() - interval 1 month as date, number from numbers(100)"),
        }
        append_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(append_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)
        job = await self.get_finalised_job_async(json.loads(response.body)["job_id"])
        self.assertEqual(job.status, "done", job.get("error", None))

        u = Users.get_by_id(self.WORKSPACE_ID)
        ds = Users.get_datasource(u, ds_name_source_2)
        self.wait_for_datasource_replication(u, ds)

        exec_sql(
            u.database,
            f"OPTIMIZE TABLE {u.database}.{ds.id} ON CLUSTER {u.cluster} FINAL",
            extra_params={"alter_sync": 2},
        )

        async def check_row_count():
            params = {
                "token": token,
                "q": f"SELECT count() c FROM {ds_name_source_2} FORMAT JSON",
            }
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            self.assertEqual(response.code, 200)
            self.assertEqual(json.loads(response.body)["data"][0]["c"], 0, response.body)

        await poll_async(check_row_count)

        # create a pipe's node with a view to that datasource
        target_ds_name = f"t_{base}"
        params = {
            "token": token_workspace_b,
            "name": f"n_{base}",
            "type": "materialized",
            "datasource": target_ds_name,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
            "populate": "true",
        }
        query = f"SELECT * FROM {datasource_a_in_workspace_b.name} where number in (select number from {datasource_a_2_in_workspace_b.name})"
        response = await self.fetch_async(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)
        job_response = pipe_node["job"]
        self.WORKSPACE_ID = workspace_b.id
        job = await self.get_finalised_job_async(job_response["id"])
        self.assertEqual(job.status, "done", job.get("error", None))
        self.assertEqual(job.kind, "populateview")
        self.assertEqual(len(job.queries) > 0, True)
        self.assertEqual(job.queries[0]["query_id"] is not None, True, job.queries[0])
        for query in job.queries:
            self.assertEqual(query["status"], "done", query)

        r = await self.get_query_logs_by_where_async(
            f"""query like 'CREATE MATERIALIZED%' AND splitByChar(' ', query)[7] in
                                                        (
                                                            SELECT views[1]
                                                            FROM system.query_log
                                                            WHERE
                                                                query_id = '{job.queries[0]["query_id"]}'
                                                            LIMIT 1
                                                        )"""
        )

        self.assertTrue("toDate(date) >= (now() - toIntervalDay(1))" in r[0]["query"])

        # validate the view is there and returns nothing due to data filtered by the TTL expression on one table in the query
        params = {
            "token": token_workspace_b,
            "q": f"SELECT count() c FROM {target_ds_name} FORMAT JSON",
        }
        self.wait_for_datasource_replication(workspace_b, target_ds_name)
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body)["data"][0]["c"], 0, response.body)

    @tornado.testing.gen_test
    async def test_invalid_populate_condition_drops_the_created_matview(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_drops_the_created_matview"
        ds_name_source = "ds_drops_the_created_matview"
        target_ds_name = "mat_view_drops_the_created_matview"

        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        params = {
            "token": token,
            "name": ds_name_source,
            "mode": "append",
            "url": self.get_url_for_sql("select 1 as number from numbers(100) format CSVWithNames"),
        }
        response = await self.fetch_async(f"/v0/datasources?{urlencode(params)}", method="POST", body="")
        self.assertEqual(response.code, 200, response.body)
        response = json.loads(response.body)
        table_name = Users.get_datasource(u, ds_name_source).id
        job = await self.get_finalised_job_async(response["job_id"])
        self.assertEqual(job.get("status"), "done")

        # create a pipe's node with a view to that datasource
        params = {
            "token": token,
            "name": target_ds_name,
            "mode": "create",
            "schema": "number Int32",
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
        }
        response = await self.fetch_async(f"/v0/datasources?{urlencode(params)}", method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        self.wait_for_datasource_replication(u, ds_name_source)
        self.wait_for_datasource_replication(u, target_ds_name)

        params = {
            "token": token,
            "name": f"{pipe_name}_node",
            "type": "materialized",
            "datasource": target_ds_name,
            "populate": "true",
            "populate_condition": "wrong_column = 1",
        }
        query = f"SELECT * FROM {ds_name_source}"
        response = await self.fetch_async(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)
        response = json.loads(response.body)
        self.assertTrue(
            "Cannot apply SQL condition, make sure the syntax is valid and the condition can be applied to the ds_drops_the_created_matview Data Source"
            in response["error"]
        )

        query = f"""SELECT count() as c
                    FROM system.tables
                    WHERE
                        database = '{u.database}'
                        and create_table_query LIKE '%{u.database}.{table_name}%'
                    FORMAT JSON"""
        r = exec_sql(u.database, query)
        # make sure the matview was not left orphan
        self.assertEquals(int(r["data"][0]["c"]), 2)

    @tornado.testing.gen_test
    @mock.patch("tinybird.ch.ch_get_replicas_for_table_sync", return_value=None)
    @mock.patch("tinybird.populates.job.replicate_populate_manually", return_value=True)
    async def test_view_creation_populate_one_replica(self, mock_replicas, mock_is_replicated):
        rdm = uuid.uuid4().hex[0:4]
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = f"test_view_creation_populate_one_replica{rdm}"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # let's create a datasource with some data
        ds_name_source = f"ds_for_view_engine_source_populate{rdm}"
        params = {
            "token": token,
            "name": ds_name_source,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        s = StringIO("d,sales\n2019-01-01,2\n2019-01-02,3")
        response = await self.fetch_full_body_upload_async(create_url, s)
        self.assertEqual(response.code, 200, response.body)

        # create a pipe's node with a view to that datasource
        target_ds_name = f"mat_view_node_ds{rdm}"
        params = {
            "token": token,
            "name": "mat_view_node",
            "type": "materialized",
            "datasource": target_ds_name,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
            "populate": "true",
        }
        query = f"SELECT toDate(d) AS d, sales * 10 AS fake_sales FROM {ds_name_source}"
        response = await self.fetch_async(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(pipe_node["name"], "mat_view_node")
        ds = Users.get_datasource(u, target_ds_name)
        self.assertEqual(pipe_node["materialized"], ds.id)
        self.assertIn("job", pipe_node)
        job_response = pipe_node["job"]
        self.assertEqual(job_response["id"], job_response["job_id"])
        self.assertEqual(job_response["kind"], JobKind.POPULATE)

        datasource = Users.get_datasource(u, target_ds_name)
        self.assertEqual(job_response["datasource"]["id"], datasource.id)

        job = await self.get_finalised_job_async(job_response["id"])
        self.assertEqual(job.status, "done", job.get("error", None))
        self.assertEqual(job.kind, "populateview")
        self.assertEqual(len(job.queries) > 0, True)
        self.assertEqual(job.queries[0]["query_id"] is not None, True, job.queries[0])
        for query in job.queries:
            self.assertEqual(query["status"], "done", query)
        self.assertEqual(job["datasource"]["name"], target_ds_name)

    def _prepare_test_view_creation_engine_deletes_mat_view(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_engine_delete"
        Users.add_pipe_sync(u, pipe_name, nodes=[])

        node_name = "mat_view_node"
        target_ds_name = "test_mat_view_engine_delete_ds"
        params = {
            "token": token,
            "name": node_name,
            "type": "materialized",
            "datasource": target_ds_name,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
        }
        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body="select * from test_table"
        )
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(pipe_node["name"], node_name)
        ds = Users.get_datasource(u, target_ds_name)
        self.assertEqual(pipe_node["materialized"], ds.id)

        # validate the view exists
        r = exec_sql(
            u["database"],
            f"SELECT count() as c FROM system.tables WHERE database = '{u['database']}' and name = '{pipe_node['id']}' FORMAT JSON",
        )
        self.assertEqual(int(r["data"][0]["c"]), 1)

        return u, token, pipe_name, pipe_node, ds

    @tornado.testing.gen_test
    async def test_view_populate_with_shared_join_get(self):
        tb_api_proxy_async = TBApiProxyAsync(self)
        workspace_a = Users.get_by_id(self.WORKSPACE_ID)
        user_a = UserAccount.get_by_id(self.USER_ID)
        token_workspace_a = Users.get_token_for_scope(workspace_a, scopes.ADMIN_USER)
        token_user_a = UserAccount.get_token_for_scope(user_a, scopes.AUTH)

        ws_b_email = f"test_view_with_shared_{uuid.uuid4().hex}@example.com"
        workspace_b = await tb_api_proxy_async.register_user_and_workspace(
            ws_b_email, workspace_a.name, normalize_name_and_try_different_on_collision=True
        )
        workspace_a = Users.get_by_id(self.WORKSPACE_ID)
        user_b = UserAccount.get_by_email(ws_b_email)
        token_user_b = UserAccount.get_token_for_scope(user_b, scopes.AUTH)
        token_workspace_b = Users.get_token_for_scope(workspace_b, scopes.ADMIN)

        await tb_api_proxy_async.invite_user_to_workspace(
            token=token_user_b, workspace_id=workspace_b.id, user_to_invite_email=user_a.email
        )

        datasource_a_in_workspace_a = await tb_api_proxy_async.create_datasource(
            token=token_workspace_a,
            ds_name="test_view_populate_with_shared_join_get_a",
            schema="col_a Int32,col_b Int32,col_c Int32",
            engine_params={
                "engine": "Join",
                "engine_join_strictness": "ANY",
                "engine_join_type": "LEFT",
                "engine_key_columns": "col_a",
            },
        )

        await tb_api_proxy_async.create_datasource(
            token=token_workspace_b,
            ds_name="source_b",
            schema="col_a Int32,col_b Int32,col_c Int32",
            engine_params={
                "engine": "MergeTree",
                "engine_sorting_key": "col_a",
                "engine_partition_key": "col_a",
            },
        )

        datasource_a_in_workspace_b = await tb_api_proxy_async.share_datasource_with_another_workspace(
            token=token_user_a,
            datasource_id=datasource_a_in_workspace_a["datasource"]["id"],
            origin_workspace_id=workspace_a.id,
            destination_workspace_id=workspace_b.id,
        )

        self.assertEqual(
            datasource_a_in_workspace_b.name, f"{workspace_a.name}.test_view_populate_with_shared_join_get_a"
        )

        pipe_name = "test_mat_view_engine_delete"
        Users.add_pipe_sync(workspace_b, pipe_name, nodes=[])

        node_name = "mat_view_node"
        target_ds_name = "test_mat_view_engine_delete_ds"
        params = {
            "token": token_workspace_b,
            "name": node_name,
            "type": "materialized",
            "datasource": target_ds_name,
            "populate": "true",
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
        }
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}",
            method="POST",
            body=f"SELECT joinGet('{datasource_a_in_workspace_b.name}', 'col_b', col_a) t FROM source_b",
        )
        response = json.loads(response.body)
        job = await self.get_finalised_job_async(response["job"]["id"], token=token_workspace_b)
        self.assertEqual(job.status, "done", job.get("error", None))

    @tornado.testing.gen_test
    async def test_view_populate_with_shared_join_get_no_permission(self):
        tb_api_proxy_async = TBApiProxyAsync(self)
        workspace_a = Users.get_by_id(self.WORKSPACE_ID)
        user_a = UserAccount.get_by_id(self.USER_ID)
        token_workspace_a = Users.get_token_for_scope(workspace_a, scopes.ADMIN_USER)
        token_user_a = UserAccount.get_token_for_scope(user_a, scopes.AUTH)

        ws_b_email = f"test_view_populate_with_shared_join_get_no_permission{uuid.uuid4().hex}@example.com"
        workspace_b = await tb_api_proxy_async.register_user_and_workspace(
            ws_b_email, workspace_a.name, normalize_name_and_try_different_on_collision=True
        )
        workspace_a = Users.get_by_id(self.WORKSPACE_ID)
        user_b = UserAccount.get_by_email(ws_b_email)
        token_user_b = UserAccount.get_token_for_scope(user_b, scopes.AUTH)

        token_workspace_b = Users.get_token_for_scope(workspace_b, scopes.ADMIN)

        await tb_api_proxy_async.invite_user_to_workspace(
            token=token_user_b, workspace_id=workspace_b.id, user_to_invite_email=user_a.email
        )

        datasource_a_in_workspace_a = await tb_api_proxy_async.create_datasource(
            token=token_workspace_a,
            ds_name="test_view_populate_with_shared_join_get_no_permission_a",
            schema="col_a Int32,col_b Int32,col_c Int32",
            engine_params={
                "engine": "Join",
                "engine_join_strictness": "ANY",
                "engine_join_type": "LEFT",
                "engine_key_columns": "col_a",
            },
        )

        await tb_api_proxy_async.create_datasource(
            token=token_workspace_b,
            ds_name="source_b",
            schema="col_a Int32,col_b Int32,col_c Int32",
            engine_params={
                "engine": "MergeTree",
                "engine_sorting_key": "col_a",
                "engine_partition_key": "col_a",
            },
        )

        datasource_a_in_workspace_b = await tb_api_proxy_async.share_datasource_with_another_workspace(
            token=token_user_a,
            datasource_id=datasource_a_in_workspace_a["datasource"]["id"],
            origin_workspace_id=workspace_a.id,
            destination_workspace_id=workspace_b.id,
        )

        self.assertEqual(
            datasource_a_in_workspace_b.name,
            f"{workspace_a.name}.test_view_populate_with_shared_join_get_no_permission_a",
        )

        pipe_name = "test_mat_view_engine_delete"
        Users.add_pipe_sync(workspace_b, pipe_name, nodes=[])

        node_name = "mat_view_node"
        target_ds_name = "test_mat_view_engine_delete_ds"
        params = {
            "token": token_workspace_b,
            "name": node_name,
            "type": "materialized",
            "datasource": target_ds_name,
            "populate": "true",
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
        }

        await self.fetch_async(
            f"/v0/datasources/{datasource_a_in_workspace_a['datasource']['id']}/share?"
            + urlencode(
                {
                    "token": token_user_a,
                    "datasource_id": datasource_a_in_workspace_a["datasource"]["id"],
                    "origin_workspace_id": workspace_a.id,
                    "destination_workspace_id": workspace_b.id,
                }
            ),
            method="DELETE",
        )

        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}",
            method="POST",
            body=f"SELECT joinGet('{datasource_a_in_workspace_b.name}', 'col_b', col_a) t FROM source_b",
        )
        self.assertEqual(response.code, 400)
        self.assertEqual(
            f"Resource '{workspace_a.name}.test_view_populate_with_shared_join_get_no_permission_a' not found"
            in response.body.decode(),
            True,
        )

    def test_view_creation_engine_deleting_node_deletes_mat_view_keeps_ds(self):
        u, token, pipe_name, pipe_node, ds = self._prepare_test_view_creation_engine_deletes_mat_view()

        # Create another Pipe pointing to the same data source
        other_pipe_name = "test_mat_view_engine_delete_other"
        Users.add_pipe_sync(u, other_pipe_name, nodes=[])
        params = {
            "token": token,
            "name": "mat_view_node",
            "type": "materialized",
            "datasource": ds.name,
        }
        response = self.fetch(
            f"/v0/pipes/{other_pipe_name}/nodes?{urlencode(params)}", method="POST", body="select * from test_table"
        )
        other_pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(other_pipe_node["materialized"], ds.id)

        # delete node
        params = {"token": token}
        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes/{pipe_node['name']}?{urlencode(params)}", method="DELETE", body=None
        )
        self.assertEqual(response.code, 204)

        # materialized view is gone
        self._check_table_in_database(u.database, pipe_node["id"], exists=False)
        # Data Source is alive as there is another Pipe pointing to it
        self._check_table_in_database(u.database, ds.id, exists=True)

    def test_view_creation_engine_deleting_pipe_deletes_mat_view_keeps_ds(self):
        u, token, pipe_name, pipe_node, ds = self._prepare_test_view_creation_engine_deletes_mat_view()

        # Create another Pipe pointing to the same data source
        other_pipe_name = "test_mat_view_engine_delete_other"
        Users.add_pipe_sync(u, other_pipe_name, nodes=[])
        params = {
            "token": token,
            "name": "mat_view_node",
            "type": "materialized",
            "datasource": ds.name,
        }
        response = self.fetch(
            f"/v0/pipes/{other_pipe_name}/nodes?{urlencode(params)}", method="POST", body="select * from test_table"
        )
        other_pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(other_pipe_node["materialized"], ds.id)

        # delete pipe
        params = {"token": token}
        response = self.fetch(f"/v0/pipes/{pipe_name}?{urlencode(params)}", method="DELETE", body=None)
        self.assertEqual(response.code, 204)

        # materialized view is gone
        self._check_table_in_database(u.database, pipe_node["id"], exists=False)

        # Data Source is alive as there is another Pipe pointing to it
        self._check_table_in_database(u.database, ds.id, exists=True)

    def test_view_creation_to_happy_case(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_creation_to_happy_case"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # let's create a landing datasource
        ds_name_source = "test_ds_for_view_to_source"
        params = {"token": token, "name": ds_name_source, "schema": "a UInt64", "engine": "Null"}

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")

        self.assertEqual(response.code, 200)

        # let's create a datasource
        ds_name_target = "test_ds_for_view_to_target"
        params = {
            "token": token,
            "name": ds_name_target,
            "schema": "x UInt64, y UInt64",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        ds_target = json.loads(response.body)

        # create a pipe's node with a view to proxy from source to target
        params = {"token": token, "name": "mat_view_node_to", "type": "materialized", "datasource": ds_name_target}
        query = f"select a * 10 as x, a * 100 as y from {ds_name_source}"
        response = self.fetch(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(pipe_node["name"], "mat_view_node_to")
        self.assertEqual(pipe_node["materialized"], ds_target["datasource"]["id"])

        # add some data to the source datasource
        data = [1, 2, 3]
        params = {
            "token": token,
            "name": ds_name_source,
            "mode": "append",
        }
        response = self.fetch(
            f"/v0/datasources?{urlencode(params)}", method="POST", body="\n".join([str(d) for d in data])
        )

        def assert_datasource():
            params = {
                "token": token,
                "q": f"SELECT * FROM {ds_name_target} ORDER BY x FORMAT JSON",
            }
            response = self.fetch(f"/v0/sql?{urlencode(params)}")
            self.assertEqual(response.code, 200)
            payload = json.loads(response.body)
            self.assertEqual(payload["data"], [{"x": d * 10, "y": d * 100} for d in data])

        poll(assert_datasource)

    @pytest.mark.skip("Skipping to avoid hiding other CH errors, leaving the test for reference.")
    def test_view_creation_with_wrong_data_type(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_view_creation_with_wrong_data_type"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        ds_name_source = "ds_test_view_creation_with_wrong_data_type"

        params = {
            "token": token,
            "name": ds_name_source,
            "schema": "a UInt64, b DateTime, c Int64",
            "engine": "MergeTree",
            "engine_sorting_key": "(a, b)",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        params = {
            "token": token,
            "name": "mat_view_node_without_group_by",
            "type": "materialized",
            "datasource": ds_name_source,
        }

        query = """
            SELECT
                a,
                now() as b,
                NULL as c
            FROM test_table
        """

        response = self.fetch(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)

        result = json.loads(response.body)
        self.assertEqual(response.code, 400, response.body)
        self.assertTrue(
            "Error when creating the Materialized View, make sure there is no column with type `Nullable(Nothing)`"
            in result["error"]
        )

    def test_view_creation_with_wrong_group_by(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_invalid_groupby"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        ds_name_source = "ds_dist_agg_test_groupby"

        params = {
            "token": token,
            "name": ds_name_source,
            "schema": "a UInt64, b DateTime, c Int64",
            "engine": "SummingMergeTree",
            "engine_sorting_key": "(a, b)",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        params = {
            "token": token,
            "name": "mat_view_node_without_group_by",
            "type": "materialized",
            "datasource": ds_name_source,
        }

        query = """
            SELECT
                a,
                now() as b,
                toInt64(cityHash64(a)) as c
            FROM test_table
        """

        response = self.fetch(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)

        result = json.loads(response.body)
        self.assertEqual(response.code, 400, response.body)
        self.assertTrue("GROUP BY is missing, sorting keys are: ['a', 'b']." in result["error"])

        datasource = Users.get_datasource(u, ds_name_source)
        self.assertEqual(datasource.name, ds_name_source)

    def test_view_and_ds_creation_with_wrong_group_by(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_invalid_groupby"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        ds_name_source = "ds_dist_agg_test_groupby"

        params = {
            "token": token,
            "name": "mat_view_node_without_group_by",
            "type": "materialized",
            "datasource": ds_name_source,
            "schema": "a UInt64, b DateTime, c Int64",
            "engine": "SummingMergeTree",
            "engine_sorting_key": "(a, b)",
        }

        query = """
            SELECT
                a,
                now() as b,
                toInt64OrZero(c) as c
            FROM test_table
        """

        response = self.fetch(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)

        self.assertEqual(response.code, 400, response.body)
        result = json.loads(response.body)
        self.assertTrue("GROUP BY is missing, sorting keys are: ['a', 'b']." in result["error"])
        datasource = Users.get_datasource(u, ds_name_source)
        self.assertEqual(datasource, None)

    def test_view_and_ds_creation_with_wrong_partition_key(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        test_landing_datasource = Users.add_datasource_sync(u, "test_view_and_ds_creation_with_wrong_partition_key")

        def create_test_datasource(u, datasource):
            url = f"http://{CH_ADDRESS}/?database={u['database']}"
            requests.post(
                url,
                data="create table `%s` (number UInt64, id String) Engine = MergeTree() ORDER BY tuple()"
                % datasource.id,
            )
            # add some data
            requests.post(
                url,
                data="""
                insert into `%s` SELECT number, toString(generateUUIDv4()) AS id FROM numbers(1000)
            """
                % datasource.id,
            )
            requests.post(
                url,
                data="create table `%s_quarantine` (number String, id String) Engine = MergeTree() ORDER BY tuple()"
                % datasource.id,
            )

        create_test_datasource(u, test_landing_datasource)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_invalid_partition_key"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        ds_name_source = "ds_dist_agg_test_partition_key"

        params = {
            "token": token,
            "name": "mat_view_node_without_group_by",
            "type": "materialized",
            "datasource": ds_name_source,
            "schema": "id2 String",
            "engine": "MergeTree",
            "engine_sorting_key": "id2",
            "engine_partition_key": "id2",
        }

        query = """
            SELECT
                substring(id, 1, 5) as id2
            FROM test_view_and_ds_creation_with_wrong_partition_key
        """

        response = self.fetch(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)

        self.assertEqual(response.code, 400, response.body)
        result = json.loads(response.body)
        self.assertTrue(
            "The engine partition key would result in creating too many parts under current ingestion. Please, review your partition key"
            in result["error"]
        )
        datasource = Users.get_datasource(u, ds_name_source)
        self.assertEqual(datasource, None)

    def test_view_and_ds_creation_with_wrong_sorting_key(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_invalid_groupby"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        ds_name_source = "ds_dist_agg_test_sorting_key"

        params = {
            "token": token,
            "name": "mat_view_node_without_group_by",
            "type": "materialized",
            "datasource": ds_name_source,
            "schema": "b DateTime, avgState(a) AggregateFunction(avg, Nullable(Int64))",
            "engine": "AggregatingMergeTree",
            "engine_sorting_key": "b, avgState(a)",
        }

        query = """
            SELECT
                toStartOfDay(now()) as b,
                avgState(a)
            FROM test_table
            GROUP BY b
        """

        response = self.fetch(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)

        result = json.loads(response.body)
        self.assertEqual(response.code, 400, response.body)
        self.assertTrue(
            "Column 'avgState(a)' should have an alias. Change the query and try it again. i.e: avgState(a) avgState_a"
            in result["error"]
        )
        datasource = Users.get_datasource(u, ds_name_source)
        self.assertEqual(datasource, None)

    def test_view_creation_with_wrong_dist_columns(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_to"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # let's create a target datasource
        ds_name_target = "ds_for_view_to_target_wrong_columns"
        params = {
            "token": token,
            "name": ds_name_target,
            "schema": "x UInt64, y UInt64",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")

        # create a pipe's node with a view to proxy from source to target
        node_name = "mat_view_node_to_create_error"
        params = {"token": token, "name": node_name, "type": "materialized", "datasource": ds_name_target}
        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body="select * from test_table"
        )
        result = json.loads(response.body)
        self.assertEqual(response.code, 400)
        self.assertTrue(
            "The pipe has columns ['a', 'b', 'c'] not found in the destination Data Source." in result["error"]
        )

        params["skip-materialized-checks"] = "true"

        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body="select * from test_table"
        )
        result = json.loads(response.body)
        self.assertEqual(response.code, 400)

    def test_view_creation_with_wrong_dist_columns_from_ui(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_to"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # let's create a target datasource
        ds_name_target = "ds_for_view_to_target_wrong_columns"
        params = {
            "token": token,
            "name": ds_name_target,
            "schema": "x UInt64, y UInt64",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")

        # create a pipe's node with a view to proxy from source to target
        node_name = "mat_view_node_to_create_error"
        params = {"token": token, "name": node_name, "type": "materialized", "datasource": ds_name_target, "from": "ui"}
        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body="select * from test_table"
        )
        result = json.loads(response.body)
        self.assertEqual(response.code, 400)
        self.assertTrue(
            "The pipe has columns ['a', 'b', 'c'] not found in the destination Data Source." in result["error"]
        )

        params["skip-materialized-checks"] = "true"

        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body="select * from test_table"
        )
        result = json.loads(response.body)
        self.assertEqual(response.code, 400)
        self.assertTrue(
            "The pipe has columns ['a', 'b', 'c'] not found in the destination Data Source.", result["error"]
        )

    @tornado.testing.gen_test
    async def test_view_creation_populate_to_happy_case(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_to_populate_happy_case"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # let's create a source datasource
        ds_name_source = "ds_for_view_to_source_populate_happy_case"
        params = {
            "token": token,
            "name": ds_name_source,
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        s = StringIO("d,sales\n2019-01-01,2\n2019-01-02,3")
        response = await self.fetch_full_body_upload_async(create_url, s)
        self.assertEqual(response.code, 200, response.body)

        # let's create a datasource
        ds_name_target = "ds_for_view_to_target_2"
        params = {"token": token, "name": ds_name_target, "schema": "d Date, fake_sales Int32", "replicated": "true"}

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)
        ds_target = json.loads(response.body)

        # create a pipe's node with a view to proxy from source to target
        params = {
            "token": token,
            "name": "mat_view_node_to",
            "type": "materialized",
            "datasource": ds_name_target,
            "populate": "true",
        }

        query = f"SELECT toDate(d) AS d, sales * 10 AS fake_sales FROM {ds_name_source}"
        response = await self.fetch_async(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(pipe_node["name"], "mat_view_node_to")
        self.assertEqual(pipe_node["materialized"], ds_target["datasource"]["id"])
        self.assertEqual(pipe_node["cluster"], "tinybird")
        self.assertIn("job", pipe_node)
        job_response = pipe_node["job"]
        self.assertEqual(job_response["id"], job_response["job_id"])
        self.assertEqual(job_response["kind"], JobKind.POPULATE)

        # validate the target data source returns from the existing data
        job = await self.get_finalised_job_async(job_response["id"])
        self.assertEqual(job.status, "done", job.get("error", None))

        initial_data = [{"d": "2019-01-01", "fake_sales": 20}, {"d": "2019-01-02", "fake_sales": 30}]

        async def assert_datasource():
            params = {
                "token": token,
                "q": f"SELECT * FROM {ds_name_target} ORDER BY d FORMAT JSON",
            }
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            self.assertEqual(response.code, 200)
            payload = json.loads(response.body)
            self.assertEqual(payload["data"], initial_data)

        await poll_async(assert_datasource)

        # Replacing data in the source data source propagates to target
        csv_url = self.get_url_for_sql("SELECT toDate('2019-01-03') AS d, 1 AS sales format CSV")
        params = {
            "token": token,
            "name": ds_name_source,
            "mode": "replace",
            "url": csv_url,
        }
        response = await self.fetch_async(f"/v0/datasources?{urlencode(params)}", method="POST", body="")
        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done")

        async def assert_datasource():
            params = {
                "token": token,
                "q": f"SELECT * FROM {ds_name_target} ORDER BY d FORMAT JSON",
            }
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            self.assertEqual(response.code, 200)
            payload = json.loads(response.body)
            self.assertEqual(payload["data"], [{"d": "2019-01-03", "fake_sales": 10}])

        await poll_async(assert_datasource)

    @tornado.testing.gen_test
    async def test_view_populate_join_tables(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_view_populate_join_tables"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # let's create a source data source
        ds_name_source = "ds_for_view_to_source_populate_and_replace"
        params = {
            "token": token,
            "name": ds_name_source,
            "schema": "d DateTime, sales Int32",
            "engine_partition_key": "toHour(d)",
            "engine": "MergeTree",
            "engine_sorting_key": "d",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        # fill with 1.5M rows
        fill_url = self.get_url_for_sql(
            f"insert into {json.loads(response.body)['datasource']['id']} SELECT toDateTime('2018-01-01 00:00:00') + number AS d, 1 AS sales from numbers(1500000)"
        )
        response = await self.fetch_async(fill_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        # let's create a target datasource
        ds_name_target = "ds_for_view_to_target_join"
        params = {
            "token": token,
            "name": ds_name_target,
            "schema": "d Int32, count UInt64",
            "engine": "Join",
            "engine_join_strictness": "ANY",
            "engine_join_type": "LEFT",
            "engine_key_columns": "d",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        ds_target = json.loads(response.body)

        # create a pipe's node with a view to proxy from source to target
        node_name = "mat_view_node_to"
        params = {
            "token": token,
            "name": node_name,
            "type": "materialized",
            "datasource": ds_name_target,
            "populate": "true",
        }
        # the aggregation does not make any sense but it's important
        # to run a query with aggregation to test the insert
        query = f"SELECT toInt32(d)%2 as d, count() as count FROM {ds_name_source} group by d"
        response = await self.fetch_async(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(pipe_node["name"], node_name)
        self.assertEqual(pipe_node["materialized"], ds_target["datasource"]["id"])
        self.assertIn("job", pipe_node)
        job_response = pipe_node["job"]
        self.assertEqual(job_response["id"], job_response["job_id"])
        self.assertEqual(job_response["kind"], JobKind.POPULATE)
        _ = await self.get_finalised_job_async(job_response["id"])

        async def get_target_ds_result():
            params = {
                "token": token,
                "q": f"SELECT * FROM {ds_name_target} format JSON",
            }
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            self.assertEqual(response.code, 200)
            value = json.loads(response.body)["data"]
            self.assertEqual(value, [{"count": 750000, "d": 0}, {"count": 750000, "d": 1}], value)

        await poll_async(get_target_ds_result)

    @tornado.testing.gen_test
    async def test_view_creation_populate_replacing_datasource(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_to_populate"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # let's create a source data source
        ds_name_source = "ds_for_view_to_source_populate_and_replace"
        params = {"token": token, "name": ds_name_source, "schema": "d Date, sales UInt16"}
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")

        # Append some initial data
        csv_url = self.get_url_for_sql("SELECT toDate('2018-01-01') AS d, 1 AS sales format CSVWithNames")
        params = {
            "token": token,
            "name": ds_name_source,
            "mode": "append",
            "url": csv_url,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done")

        # let's create a target datasource
        ds_name_target = "ds_for_view_to_target"
        params = {
            "token": token,
            "name": ds_name_target,
            "schema": "y UInt16, fake_sales UInt16",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        ds_target = json.loads(response.body)
        ds_target_id = ds_target["datasource"]["id"]

        # create a pipe's node with a view to proxy from source to target
        node_name = "mat_view_node_to"
        params = {
            "token": token,
            "name": node_name,
            "type": "materialized",
            "datasource": ds_name_target,
            "populate": "true",
        }
        query = f"""SELECT
            toUInt16(sales * 10) AS fake_sales,
            toYear(d) AS y
        FROM {ds_name_source} as t
        where t.sales > 0"""
        response = await self.fetch_async(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(pipe_node["name"], node_name)
        self.assertEqual(pipe_node["materialized"], ds_target_id)
        self.assertIn("job", pipe_node)
        job_response = pipe_node["job"]
        self.assertEqual(job_response["id"], job_response["job_id"])
        self.assertEqual(job_response["kind"], JobKind.POPULATE)
        job = await self.get_finalised_job_async(job_response["id"])
        self.assertEqual(job.status, "done", job)

        def get_target_ds_result(expected_data):
            async def _f():
                params = {
                    "token": token,
                    "q": f"SELECT * FROM {ds_name_target} ORDER BY y, fake_sales FORMAT JSON",
                }
                response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
                self.assertEqual(response.code, 200)
                value = json.loads(response.body)["data"]
                self.assertEqual(value, expected_data)

            return _f

        await poll_async(get_target_ds_result([{"y": 2018, "fake_sales": 10}]))

        # validate data source statistics have been updated
        await self.assert_stats(ds_name_source, token, expected_row_count=1, expected_bytes=155)
        await self.assert_stats(ds_name_target, token, expected_row_count=1, expected_bytes=155)

        # appending new data to the data source should feed the target data source
        csv_url = self.get_url_for_sql("SELECT toDate('2018-01-02') AS d, 2 AS sales format CSVWithNames")
        params = {
            "token": token,
            "name": ds_name_source,
            "mode": "append",
            "url": csv_url,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done")
        await poll_async(get_target_ds_result([{"y": 2018, "fake_sales": 10}, {"y": 2018, "fake_sales": 20}]))

        await self.assert_stats(ds_name_source, token, expected_row_count=2, expected_bytes=310)

        # let's replace the source data source
        csv_url = self.get_url_for_sql("SELECT toDate('2019-01-01') AS d, 5 AS sales format CSVWithNames")
        params = {
            "token": token,
            "name": ds_name_source,
            "url": csv_url,
            "mode": "replace",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done")

        # validate the target data source returns the new data
        await poll_async(get_target_ds_result([{"y": 2019, "fake_sales": 50}]))

        await self.assert_stats(ds_name_source, token, expected_row_count=1, expected_bytes=151)
        await self.assert_stats(ds_name_target, token, expected_row_count=1, expected_bytes=155)

        # appending new data to the new data source should keep feeding the views/target datasources
        csv_url = self.get_url_for_sql("SELECT toDate('2019-01-02') AS d, 10 AS sales format CSVWithNames")
        params = {
            "token": token,
            "name": ds_name_source,
            "mode": "append",
            "url": csv_url,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done")
        await poll_async(get_target_ds_result([{"y": 2019, "fake_sales": 50}, {"y": 2019, "fake_sales": 100}]))
        await self.assert_stats(ds_name_source, token, expected_row_count=2, expected_bytes=310)

    def test_view_creation_to_deleting_node_does_not_delete_to_table(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_to"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # let's create a target datasource
        ds_name_target = "ds_for_view_to_target_to_delete"
        params = {
            "token": token,
            "name": ds_name_target,
            "schema": "a UInt64, b Float32, c String",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        ds_target = json.loads(response.body)

        # create a pipe's node with a view to proxy from source to target
        node_name = "mat_view_node_to_to_delete"
        params = {"token": token, "name": node_name, "type": "materialized", "datasource": ds_name_target}
        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body="select * from test_table"
        )
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(pipe_node["name"], node_name)
        self.assertEqual(pipe_node["materialized"], ds_target["datasource"]["id"])

        def get_node_associated_tables(pipe_node):
            r = exec_sql(
                u["database"],
                f"SELECT * FROM system.tables WHERE database = '{u['database']}' and name IN ('{pipe_node['id']}', '{pipe_node['materialized']}') FORMAT JSON",
            )
            return r["data"]

        # validate the view and the data source table exists
        tables = get_node_associated_tables(pipe_node)
        self.assertEqual(len(tables), 2)

        # delete node
        params = {"token": token}
        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}?{urlencode(params)}", method="DELETE", body=None
        )
        self.assertEqual(response.code, 204)

        # materialized view is gone, but the data source table still exists
        tables = {t["name"]: t for t in get_node_associated_tables(pipe_node)}
        self.assertEqual(len(tables), 1)
        self.assertIn(ds_target["datasource"]["id"], tables)

    def test_view_creation_to_deleting_datasource_requires_deleting_pipes_node(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_to"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # let's create a target datasource
        ds_name_target = "ds_for_view_to_target_to_delete_datasource"
        params = {
            "token": token,
            "name": ds_name_target,
            "schema": "a UInt64, b Float32, c String",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        ds_target = json.loads(response.body)

        # create a pipe's node with a view to proxy from source to target
        node_name = "mat_view_node_to_to_delete"
        params = {"token": token, "name": node_name, "type": "materialized", "datasource": ds_name_target}
        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body="select * from test_table"
        )
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(pipe_node["name"], node_name)
        self.assertEqual(pipe_node["materialized"], ds_target["datasource"]["id"])

        def get_node_associated_tables(pipe_node):
            r = exec_sql(
                u["database"],
                f"SELECT * FROM system.tables WHERE database = '{u['database']}' and name IN ('{pipe_node['id']}', '{pipe_node['materialized']}') FORMAT JSON",
            )
            return r["data"]

        # validate the view and the data source table exists
        tables = get_node_associated_tables(pipe_node)
        self.assertEqual(len(tables), 2)

        # Trying to delete the Data Source
        params = {
            "token": token,
        }
        response = self.fetch(f"/v0/datasources/{ds_name_target}?{urlencode(params)}", method="DELETE")
        self.assertEqual(response.code, 409, response.body)
        result = json.loads(response.body)
        self.assertEqual(
            result["error"],
            f'The Data Source is the target of a Materialized View. Deleting it may break your data ingestion. Set the `force` parameter to `true` to unlink the dependent Materialized Nodes and delete the Data Source. Affected upstream materializations => Pipes="{pipe_name}", nodes="{node_name}". The Data Source is used in => Pipes="{pipe_name}", nodes="{node_name}"',
        )

        # delete node
        params = {"token": token}
        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}?{urlencode(params)}", method="DELETE", body=None
        )
        self.assertEqual(response.code, 204)

        # materialized view is gone, but the data source table still exists
        tables = {t["name"]: t for t in get_node_associated_tables(pipe_node)}
        self.assertEqual(len(tables), 1)
        self.assertIn(ds_target["datasource"]["id"], tables)

        # Delete the Data Source works
        params = {
            "token": token,
        }
        response = self.fetch(f"/v0/datasources/{ds_name_target}?{urlencode(params)}", method="DELETE")
        self.assertEqual(response.code, 204, response.body)

    def test_view_creation_to_renaming_datasource_is_not_allowed(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_rename"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        ds_name_target = "ds_for_view_to_target_to_rename"
        params = {
            "token": token,
            "name": ds_name_target,
            "schema": "a UInt64, b Float32, c String",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        # create a pipe's node with a view to proxy from source to target
        node_name = "mat_view_node_using_ds_target"
        params = {"token": token, "name": node_name, "type": "materialized", "datasource": ds_name_target}

        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body="select * from test_table"
        )
        self.assertEqual(response.code, 200)

        # Trying to rename the Data Source
        params = {"token": token, "name": "ds_for_view_to_target_renamed"}
        response = self.fetch(f"/v0/datasources/{ds_name_target}?{urlencode(params)}", method="PUT", body=b"")
        self.assertEqual(response.code, 200, response.body)

    def test_regression_delete_materialized_datasource_after_duplicating_the_pipe_is_not_allowed(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_rename"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        ds_name_target = "ds_for_view_to_target_to_delete"
        params = {
            "token": token,
            "name": ds_name_target,
            "schema": "a UInt64, b Float32, c String",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        # create a pipe's node with a view to proxy from source to target
        node_name = "mat_view_node_using_ds_target"
        params = {"token": token, "name": node_name, "type": "materialized", "datasource": ds_name_target}

        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body="select * from test_table"
        )
        self.assertEqual(response.code, 200)

        # create a pipe with the same node name
        Users.add_pipe_sync(u, f"{pipe_name}_copy", "select * from test_table")
        params = {"token": token, "name": node_name}

        response = self.fetch(
            f"/v0/pipes/{pipe_name}_copy/nodes?{urlencode(params)}", method="POST", body="select * from test_table"
        )
        self.assertEqual(response.code, 200)

        # Trying to delete the materialized Data Source
        params = {"token": token, "name": ds_name_target}
        response = self.fetch(f"/v0/datasources/{ds_name_target}?{urlencode(params)}", method="DELETE")
        self.assertEqual(response.code, 409, response.body)

    @tornado.testing.gen_test
    async def test_drop_materialized_pipe_is_forbidden_if_target_datasource_is_shared(self):
        rand_id = uuid.uuid4().hex[0:6]
        tb_api_proxy_async = TBApiProxyAsync(self)
        workspace_a = Users.get_by_id(self.WORKSPACE_ID)
        user_a = UserAccount.get_by_id(self.USER_ID)
        token_a = Users.get_token_for_scope(workspace_a, scopes.ADMIN)
        token_user_a = UserAccount.get_token_for_scope(user_a, scopes.AUTH)

        ws_b_email = f"test_drop_materialized_pipe_is_forbidden_{uuid.uuid4().hex}@example.com"
        workspace_b = await tb_api_proxy_async.register_user_and_workspace(
            ws_b_email, workspace_a.name, normalize_name_and_try_different_on_collision=True
        )
        user_b = UserAccount.get_by_email(ws_b_email)
        token_user_b = UserAccount.get_token_for_scope(user_b, scopes.AUTH)
        token_b = Users.get_token_for_scope(workspace_b, scopes.ADMIN)

        pipe_name = f"test_mat_view_{rand_id}"
        # Users.add_pipe_sync(workspace_a, pipe_name, 'select * from test_table')

        node_name = f"mat_view_node_using_ds_target{rand_id}"
        target = f"ds_name_target{rand_id}"
        params = {
            "token": token_a,
        }

        body = json.dumps(
            {
                "name": pipe_name,
                "nodes": [
                    {
                        "sql": "select 1",
                        "name": f"node_00{rand_id}",
                    }
                ],
            }
        )

        response = await self.fetch_async(
            f"/v0/pipes?{urlencode(params)}", method="POST", body=body, headers={"Content-type": "application/json"}
        )
        pipe = json.loads(response.body)

        node_name = f"mat_view_node_using_ds_target{rand_id}"
        target = f"ds_name_target{rand_id}"
        params = {
            "token": token_a,
            "name": node_name,
            "type": "materialized",
            "datasource": target,
            "engine": "MergeTree",
        }
        response = await self.fetch_async(
            f"/v0/pipes/{pipe['id']}/nodes?{urlencode(params)}", method="POST", body="select * from test_table"
        )
        self.assertEqual(response.code, 200)

        await tb_api_proxy_async.invite_user_to_workspace(
            token=token_user_b, workspace_id=workspace_b.id, user_to_invite_email=user_a.email
        )

        ds = Users.get_datasource(workspace_a, target)
        await tb_api_proxy_async.share_datasource_with_another_workspace(
            token=token_user_a,
            datasource_id=ds.id,
            origin_workspace_id=workspace_a.id,
            destination_workspace_id=workspace_b.id,
        )

        params = {
            "token": token_a,
        }
        response = await self.fetch_async(f"/v0/pipes/{pipe_name}?{urlencode(params)}", method="DELETE")
        self.assertEqual(response.code, 204, response.body)

        get_url = f"/v0/datasources/{target}?{urlencode(params)}"
        response = await self.fetch_async(get_url)
        self.assertEqual(response.code, 200)

        params = {
            "token": token_b,
        }
        get_url = f"/v0/datasources/{workspace_a.name}.{target}?{urlencode(params)}"
        response = await self.fetch_async(get_url)
        self.assertEqual(response.code, 200)

    @tornado.testing.gen_test
    async def test_query_a_shared_ds_pipe_with_filter(self):
        """Added after https://gitlab.com/tinybird/analytics/-/issues/4513"""
        from ..utils import fixture_file

        tb_api_proxy_async = TBApiProxyAsync(self)

        # Source workspace and user
        workspace1 = Users.get_by_id(self.WORKSPACE_ID)
        user1 = UserAccount.get_by_id(self.USER_ID)
        workspace1_admin_token = Users.get_token_for_scope(workspace1, scopes.ADMIN)
        user1_auth_token = UserAccount.get_token_for_scope(user1, scopes.AUTH)

        # Destination workspace and user
        workspace2_name = self.gen_random_id("workspace2_")
        user2_email = self.gen_random_email()
        workspace2 = await tb_api_proxy_async.register_user_and_workspace(
            user2_email, workspace2_name, normalize_name_and_try_different_on_collision=True
        )
        user2 = UserAccount.get_by_email(user2_email)
        workspace2_admin_token = Users.get_token_for_scope(workspace2, scopes.ADMIN)
        user2_auth_token = UserAccount.get_token_for_scope(user2, scopes.AUTH)

        # 1. Invite user1 to workspace2 to be able to share datasources between the two workspaces
        await tb_api_proxy_async.invite_user_to_workspace(user2_auth_token, workspace2.id, user1.email)

        # 2. Create 'shared_ds' datasource
        shared_ds_name = "shared_ds"
        create_ds_url = self.get_url(f"/v0/datasources?token={workspace1_admin_token}&name={shared_ds_name}")
        with fixture_file("sales_0.csv", mode="rb") as fd:
            response = await self.fetch_full_body_upload_async(create_ds_url, fd)
        self.assertEqual(response.code, 200, response.body)
        shared_ds_id = json.loads(response.body)["datasource"]["id"]

        # 3. Share workspace1's 'shared_ds' with workspace2
        shared_ds_in_workspace2 = await tb_api_proxy_async.share_datasource_with_another_workspace(  # noqa: F841
            token=user1_auth_token,
            datasource_id=shared_ds_id,
            origin_workspace_id=workspace1.id,
            destination_workspace_id=workspace2.id,
        )

        # 4. Create 'test_pipe_over_shared_ds' pipe in workspace2
        pipe_name = "test_pipe_over_shared_ds"
        create_pipe_url = self.get_url(
            f"/v0/pipes?token={workspace2_admin_token}&name={pipe_name}&sql=select+*+from+{workspace1.name}.{shared_ds_name}+limit+10"
        )
        response = await self.fetch_async(create_pipe_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)
        pipe_def = json.loads(response.body)

        # 5.a Create a token with scope PIPES:READ on 'test_pipe_over_shared_ds' and DATASOURCES:READ on 'shared_ds'
        create_token_url = self.get_url(
            f"/v0/tokens?token={workspace2_admin_token}&name=read_{pipe_name}&scope=DATASOURCES:READ:{workspace1.name}.{shared_ds_name}&scope=PIPES:READ:{pipe_name}"
        )
        response = await self.fetch_async(create_token_url, method="POST", body="")
        read_token = json.loads(response.body)["token"]

        # 5.b Create a token with scope PIPES:READ on 'test_pipe_over_shared_ds' and DATASOURCES:READ on 'shared_ds' with filter 'cod_order_wcs = 2'
        token_filter = "cod_order_wcs%20%3D%202"
        create_token_url = self.get_url(
            f"/v0/tokens?token={workspace2_admin_token}&name=read_{pipe_name}_filtered&scope=DATASOURCES:READ:{workspace1.name}.{shared_ds_name}:{token_filter}&scope=PIPES:READ:{pipe_name}"
        )
        response = await self.fetch_async(create_token_url, method="POST", body="")
        read_token_filtered = json.loads(response.body)["token"]

        # 6. Publish the endpoint
        make_endpoint_url = (
            f"/v0/pipes/{pipe_name}/nodes/{pipe_def['nodes'][0]['id']}/endpoint?token={workspace2_admin_token}"
        )
        response = await self.fetch_async(
            make_endpoint_url, method="POST", body=b"", headers={"Content-type": "application/json"}
        )
        endpoint_def = json.loads(response.body)  # noqa: F841

        # 7.a Fetch data without filters
        async def check_fetch_data_without_filters():
            fetch_pipe_url = self.get_url(f"/v0/pipes/{pipe_name}.json?token={read_token}")
            response = await self.fetch_async(fetch_pipe_url)
            result = json.loads(response.body)
            self.assertEqual(result["rows"], 2)

        await poll_async(check_fetch_data_without_filters)

        # 7.b Fetch data with token filters
        async def check_fetch_data_with_filters():
            fetch_pipe_url = self.get_url(f"/v0/pipes/{pipe_name}.json?token={read_token_filtered}")
            response = await self.fetch_async(fetch_pipe_url)
            result = json.loads(response.body)
            self.assertEqual(result["rows"], 1)

        await poll_async(check_fetch_data_with_filters)

    @tornado.testing.gen_test
    async def test_query_a_ds_pipe_with_filter(self):
        """Added after https://gitlab.com/tinybird/analytics/-/issues/4513"""
        from ..utils import fixture_file

        # Source workspace and user
        workspace1 = Users.get_by_id(self.WORKSPACE_ID)
        # user1 = UserAccount.get_by_id(self.USER_ID)
        workspace1_admin_token = Users.get_token_for_scope(workspace1, scopes.ADMIN)
        # user1_auth_token = UserAccount.get_token_for_scope(user1, scopes.AUTH)

        # 2. Create datasource
        datasource_name = "test_datasource"
        create_ds_url = self.get_url(f"/v0/datasources?token={workspace1_admin_token}&name={datasource_name}")
        with fixture_file("sales_0.csv", mode="rb") as fd:
            response = await self.fetch_full_body_upload_async(create_ds_url, fd)
        self.assertEqual(response.code, 200, response.body)
        # datasource_id = json.loads(response.body)['datasource']['id']

        # 3. Create 'test_pipe_over_datasource' pipe
        pipe_name = "test_pipe_over_datasource"
        create_pipe_url = self.get_url(
            f"/v0/pipes?token={workspace1_admin_token}&name={pipe_name}&sql=select+*+from+{datasource_name}+limit+10"
        )
        response = await self.fetch_async(create_pipe_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)
        pipe_def = json.loads(response.body)

        # 4.a Create a token with scope PIPES:READ on 'test_pipe_over_datasource' and DATASOURCES:READ on 'test_datasource'
        create_token_url = self.get_url(
            f"/v0/tokens?token={workspace1_admin_token}&name=read_{pipe_name}&scope=DATASOURCES:READ:{datasource_name}&scope=PIPES:READ:{pipe_name}"
        )
        response = await self.fetch_async(create_token_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)
        read_token = json.loads(response.body)["token"]

        # 4.b Create a token with scope PIPES:READ on 'test_pipe_over_datasource' and DATASOURCES:READ on 'test_datasource' with filter 'cod_order_wcs = 2'
        token_filter = "cod_order_wcs%20%3D%202"
        create_token_url = self.get_url(
            f"/v0/tokens?token={workspace1_admin_token}&name=read_{pipe_name}_filtered&scope=DATASOURCES:READ:{datasource_name}:{token_filter}&scope=PIPES:READ:{pipe_name}"
        )
        response = await self.fetch_async(create_token_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)
        read_token_filtered = json.loads(response.body)["token"]

        # 5. Publish the endpoint
        make_endpoint_url = (
            f"/v0/pipes/{pipe_name}/nodes/{pipe_def['nodes'][0]['id']}/endpoint?token={workspace1_admin_token}"
        )
        response = await self.fetch_async(
            make_endpoint_url, method="POST", body=b"", headers={"Content-type": "application/json"}
        )
        self.assertEqual(response.code, 200, response.body)
        endpoint_def = json.loads(response.body)  # noqa: F841

        # 6.a Fetch data without filters
        async def check_fetch_data_without_filters():
            fetch_pipe_url = self.get_url(f"/v0/pipes/{pipe_name}.json?token={read_token}")
            response = await self.fetch_async(fetch_pipe_url)
            self.assertEqual(response.code, 200, response.body)
            result = json.loads(response.body)
            self.assertEqual(result["rows"], 2)

        await poll_async(check_fetch_data_without_filters)

        # 6.b Fetch data with token filters

        async def check_fetch_data_with_filters():
            fetch_pipe_url = self.get_url(f"/v0/pipes/{pipe_name}.json?token={read_token_filtered}")
            response = await self.fetch_async(fetch_pipe_url)
            result = json.loads(response.body)
            self.assertEqual(result["rows"], 1)

        await poll_async(check_fetch_data_with_filters)

    def test_modify_dependent_ds_used_in_mv_is_forbidden(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        rand_id = f"{uuid.uuid4().hex[0:3]}"
        base_name = f"test_modify_dependent_ds_used_in_mv_is_forbidden{rand_id}"
        ds1 = f"ds_{base_name}"
        ds2 = f"mv_{base_name}"
        ds3 = f"dep_{base_name}"
        mv1 = f"p_{base_name}"

        # source
        params = {"mode": "create", "name": ds1, "schema": "number Int32", "token": token}
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        # target
        params = {"mode": "create", "name": ds2, "schema": "number Int32", "token": token}
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        # dependent
        params = {"mode": "create", "name": ds3, "schema": "number Int32", "token": token}
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        Users.add_pipe_sync(u, mv1, "SELECT 1")

        # materialize a node with no other dependent nodes
        params = {
            "token": token,
            "name": f"{mv1}_view",
            "type": "materialized",
            "datasource": ds2,
            "skip_table_checks": "true",
        }

        data = f"""
            SELECT
                number
            FROM {ds1}
            WHERE number in (SELECT number FROM {ds3})
        """

        response = self.fetch(f"/v0/pipes/{mv1}/nodes?{urlencode(params)}", method="POST", body=data)
        self.assertEqual(response.code, 200)

        # deletion of a dependent datasource is forbidden
        params = {"token": token}
        response = self.fetch(f"/v0/datasources/{ds3}?{urlencode(params)}", method="DELETE")
        self.assertEqual(response.code, 409, response.body)
        result = json.loads(response.body)
        self.assertEqual(
            result["error"],
            f'This operation will break ingestion due to broken Materialized Views, unlink the Materialized Nodes or remove the dependency with the Data Source. Affected downstream materializations => Pipes="{mv1}", nodes="{mv1}_view". The Data Source is used in => Pipes="{mv1}", nodes="{mv1}_view"',
        )

        params = {"token": token, "name": f"{ds3}_{rand_id}"}
        response = self.fetch(f"/v0/datasources/{ds3}?{urlencode(params)}", method="PUT", body=b"")
        self.assertEqual(response.code, 200, response.body)

        # pipe is updated as well
        response = self.fetch(f"/v0/pipes/{mv1}?token={token}")
        node = json.loads(response.body)["nodes"][1]
        self.assertEqual(f"{ds3}_{rand_id}" in node["sql"], True, response.body)
        self.assertEqual(f"{ds3}_{rand_id}" in node["dependencies"], True, response.body)

    def test_modify_dependent_ds_used_in_another_mv_node_is_forbidden(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        rand_id = f"{uuid.uuid4().hex[0:3]}"
        base_name = f"test_modify_dependent_ds_used_in_another_mv_node_is_forbidden{rand_id}"
        ds1 = f"ds_{base_name}"
        ds2 = f"mv_{base_name}"
        ds3 = f"dep_{base_name}"
        mv1 = f"p_{base_name}"

        # source
        params = {"mode": "create", "name": ds1, "schema": "number Int32", "token": token}
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        # target
        params = {"mode": "create", "name": ds2, "schema": "number Int32", "token": token}
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        # dependent
        params = {"mode": "create", "name": ds3, "schema": "number Int32", "token": token}
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        Users.add_pipe_sync(u, mv1, f"SELECT number FROM {ds1} WHERE number in (SELECT number FROM {ds3})")

        # materialize a node that depends on other node
        params = {
            "token": token,
            "name": f"{mv1}_view",
            "type": "materialized",
            "datasource": ds2,
            "skip_table_checks": "true",
        }

        data = f"SELECT * FROM {mv1}_0"

        response = self.fetch(f"/v0/pipes/{mv1}/nodes?{urlencode(params)}", method="POST", body=data)
        self.assertEqual(response.code, 200)

        # deletion of a dependent datasource is forbidden
        params = {"token": token}
        response = self.fetch(f"/v0/datasources/{ds3}?{urlencode(params)}", method="DELETE")
        self.assertEqual(response.code, 409, response.body)
        result = json.loads(response.body)
        self.assertEqual(
            result["error"],
            f'This operation will break ingestion due to broken Materialized Views, unlink the Materialized Nodes or remove the dependency with the Data Source. Affected downstream materializations => Pipes="{mv1}", nodes="{mv1}_view". The Data Source is used in => Pipes="{mv1}", nodes="{mv1}_0,{mv1}_view"',
        )

        params = {"token": token, "name": f"{ds3}_{rand_id}"}
        response = self.fetch(f"/v0/datasources/{ds3}?{urlencode(params)}", method="PUT", body=b"")
        self.assertEqual(response.code, 200, response.body)

        # pipe is updated as well
        response = self.fetch(f"/v0/pipes/{mv1}?token={token}")
        node = json.loads(response.body)["nodes"][0]
        self.assertEqual(f"{ds3}_{rand_id}" in node["sql"], True, response.body)
        self.assertEqual(f"{ds3}_{rand_id}" in node["dependencies"], True, response.body)

    def test_modify_dependent_ds_mv_recursive_is_forbidden(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        rand_id = f"{uuid.uuid4().hex[0:3]}"
        base_name = f"test_modify_dependent_ds_mv_recursive_is_forbidden{rand_id}"
        ds1 = f"ds_{base_name}"
        ds2 = f"mv_{base_name}"
        ds3 = f"dep_{base_name}"
        mv1 = f"p_{base_name}"

        # source
        params = {"mode": "create", "name": ds1, "schema": "number Int32", "token": token}
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        # target
        params = {"mode": "create", "name": ds2, "schema": "number Int32", "token": token}
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        # dependent
        params = {"mode": "create", "name": ds3, "schema": "number Int32", "token": token}
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        Users.add_pipe_sync(u, mv1, f"SELECT number FROM {ds1} WHERE number in (SELECT number FROM {ds3})")

        params = {"token": token, "name": f"{mv1}_1", "datasource": ds2, "skip_table_checks": "true"}

        data = f"SELECT * FROM {mv1}_0"

        response = self.fetch(f"/v0/pipes/{mv1}/nodes?{urlencode(params)}", method="POST", body=data)
        self.assertEqual(response.code, 200)

        # materialize a node that depends on other node
        params = {
            "token": token,
            "name": f"{mv1}_view",
            "type": "materialized",
            "datasource": ds2,
            "skip_table_checks": "true",
        }

        data = f"SELECT * FROM {mv1}_1"

        response = self.fetch(f"/v0/pipes/{mv1}/nodes?{urlencode(params)}", method="POST", body=data)
        self.assertEqual(response.code, 200)

        # deletion of a dependent datasource is forbidden
        params = {"token": token}
        response = self.fetch(f"/v0/datasources/{ds3}?{urlencode(params)}", method="DELETE")
        self.assertEqual(response.code, 409, response.body)
        result = json.loads(response.body)
        self.assertEqual(
            result["error"],
            f'This operation will break ingestion due to broken Materialized Views, unlink the Materialized Nodes or remove the dependency with the Data Source. Affected downstream materializations => Pipes="{mv1}", nodes="{mv1}_view". The Data Source is used in => Pipes="{mv1}", nodes="{mv1}_0,{mv1}_1,{mv1}_view"',
        )

        params = {"token": token, "name": f"{ds3}_{rand_id}"}
        response = self.fetch(f"/v0/datasources/{ds3}?{urlencode(params)}", method="PUT", body=b"")
        self.assertEqual(response.code, 200, response.body)

        # pipe is updated as well
        response = self.fetch(f"/v0/pipes/{mv1}?token={token}")
        node = json.loads(response.body)["nodes"][0]
        self.assertEqual(f"{ds3}_{rand_id}" in node["sql"], True, response.body)
        self.assertEqual(f"{ds3}_{rand_id}" in node["dependencies"], True, response.body)

    @tornado.testing.gen_test
    async def test_modify_dependent_ds_mv_cascade_with_endpoint(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        rand_id = f"{uuid.uuid4().hex[0:3]}"
        base_name = f"test_modify_dependent_ds_mv_cascade_with_endpoint{rand_id}"
        ds1 = f"ds_{base_name}"
        ds2 = f"mv2_{base_name}"
        ds3 = f"mv3_{base_name}"
        mv1 = f"p1_{base_name}"
        mv2 = f"p2_{base_name}"
        api1 = f"api_{base_name}"

        # source
        params = {"mode": "create", "name": ds1, "schema": "number Int32", "token": token}
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        Users.add_pipe_sync(u, mv1, f"SELECT * FROM {ds1}")

        params = {
            "token": token,
            "name": f"{mv1}_view",
            "type": "materialized",
            "datasource": ds2,
            "engine": "MergeTree",
        }

        data = f"SELECT * FROM {mv1}_0"

        response = await self.fetch_async(f"/v0/pipes/{mv1}/nodes?{urlencode(params)}", method="POST", body=data)
        self.assertEqual(response.code, 200)

        pipe = Users.add_pipe_sync(u, mv2, f"SELECT * FROM {ds2}")

        params = {
            "token": token,
            "name": f"{mv2}_view",
            "type": "materialized",
            "datasource": ds3,
            "engine": "MergeTree",
        }

        data = f"SELECT * FROM {mv2}_0"

        response = await self.fetch_async(f"/v0/pipes/{mv2}/nodes?{urlencode(params)}", method="POST", body=data)
        self.assertEqual(response.code, 200)

        pipe = Users.add_pipe_sync(u, api1, f"SELECT * FROM {ds3}")
        node = pipe.pipeline.nodes[0].to_dict()
        await self.make_endpoint(api1, node)

        # deletion of a dependent datasource is forbidden
        params = {"token": token}
        response = await self.fetch_async(f"/v0/datasources/{ds3}?{urlencode(params)}", method="DELETE")
        self.assertEqual(response.code, 409, response.body)
        result = json.loads(response.body)
        expected_error = f"The Data Source is the target of a Materialized View. Deleting it may break your data ingestion. Set the `force` parameter to `true` to unlink the dependent Materialized Nodes and delete the Data Source. Affected upstream materializations => Pipes=\"{mv2}\", nodes=\"{mv2}_view\". The Data Source is used in => Pipes=\"{mv2},{pipe.name}\", nodes=\"{mv2}_0,{mv2}_view,{node['name']}\""
        self.assertEqual(result["error"], expected_error)

        params = {"token": token, "name": f"{ds3}_{rand_id}"}
        response = await self.fetch_async(f"/v0/datasources/{ds3}?{urlencode(params)}", method="PUT", body=b"")
        self.assertEqual(response.code, 200, response.body)

        # pipe is updated as well
        response = await self.fetch_async(f"/v0/pipes/{api1}?token={token}")
        node = json.loads(response.body)["nodes"][0]
        self.assertEqual(f"{ds3}_{rand_id}" in node["sql"], True, response.body)
        self.assertEqual(f"{ds3}_{rand_id}" in node["dependencies"], True, response.body)

    def test_modify_dependent_ds_mv_endpoint_is_forbidden(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        rand_id = f"{uuid.uuid4().hex[0:3]}"
        base_name = f"test_modify_dependent_ds_mv_endpoint_is_forbidden{rand_id}"
        ds1 = f"ds_{base_name}"
        ds2 = f"mv_{base_name}"
        ds3 = f"dep_{base_name}"
        mv1 = f"p_{base_name}"
        endpoint = f"e_{base_name}"
        endpoint2 = f"e2_{base_name}"

        # source
        params = {"mode": "create", "name": ds1, "schema": "number Int32", "token": token}
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        # target
        params = {"mode": "create", "name": ds2, "schema": "number Int32", "token": token}
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        # dependent
        params = {"mode": "create", "name": ds3, "schema": "number Int32", "token": token}
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        Users.add_pipe_sync(u, endpoint, f"SELECT number FROM {ds1} WHERE number in (SELECT number FROM {ds3})")

        response = self.fetch(
            f"/v0/pipes/{endpoint}/nodes/{endpoint}_0/endpoint?token={token}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        Users.add_pipe_sync(u, endpoint2, f"SELECT * FROM {endpoint}")

        response = self.fetch(
            f"/v0/pipes/{endpoint2}/nodes/{endpoint2}_0/endpoint?token={token}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        Users.add_pipe_sync(u, mv1, f"SELECT * FROM {endpoint2}")

        # materialize a node that depends on a node that depends on an endpoint
        params = {
            "token": token,
            "name": f"{mv1}_view",
            "type": "materialized",
            "datasource": ds2,
            "skip_table_checks": "true",
        }

        data = f"SELECT * FROM {mv1}_0"

        response = self.fetch(f"/v0/pipes/{mv1}/nodes?{urlencode(params)}", method="POST", body=data)
        self.assertEqual(response.code, 200)

        # deletion of a dependent datasource of the endpoint is forbidden
        params = {"token": token}
        response = self.fetch(f"/v0/datasources/{ds3}?{urlencode(params)}", method="DELETE")
        self.assertEqual(response.code, 409, response.body)
        result = json.loads(response.body)
        self.assertEqual(
            result["error"],
            f'This operation will break ingestion due to broken Materialized Views, unlink the Materialized Nodes or remove the dependency with the Data Source. Affected downstream materializations => Pipes="{mv1}", nodes="{mv1}_view". The Data Source is used in => Pipes="{endpoint}", nodes="{endpoint}_0"',
        )

        params = {"token": token, "name": f"{ds3}_{rand_id}"}
        response = self.fetch(f"/v0/datasources/{ds3}?{urlencode(params)}", method="PUT", body=b"")
        self.assertEqual(response.code, 200, response.body)

        # pipe is updated as well
        response = self.fetch(f"/v0/pipes/{endpoint}?token={token}")
        node = json.loads(response.body)["nodes"][0]
        self.assertEqual(f"{ds3}_{rand_id}" in node["sql"], True, response.body)
        self.assertEqual(f"{ds3}_{rand_id}" in node["dependencies"], True, response.body)

    def test_cannot_update_materialized_node(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_error_on_update"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # create a pipe's node with a view to that datasource
        target_ds = "datasource_mat_view_error_on_update"
        params = {
            "token": token,
            "name": "mat_view_node",
            "type": "materialized",
            "datasource": target_ds,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
        }
        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body="select * from test_table"
        )
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(pipe_node["name"], "mat_view_node")
        ds = Users.get_datasource(u, pipe_node["materialized"])
        self.assertEqual(ds.name, target_ds)

        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes/{pipe_node['id']}?token={token}",
            method="PUT",
            body="select * from test_table LIMIT 10",
        )
        payload = json.loads(response.body)
        self.assertEqual(response.code, 403)
        self.assertEqual(payload["error"], "Cannot modify a Materialized Node")

    @tornado.testing.gen_test
    async def test_can_unlink_self_referencing_mv(self):
        workspace = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(workspace, scopes.ADMIN)
        rand_id = f"{uuid.uuid4().hex[0:3]}"
        base_name = f"test_can_unlink_self_referencing_mv_{rand_id}"
        ds1 = f"ds_{base_name}"
        pipe_name = f"p_{base_name}"
        node_name = f"n_{base_name}"

        # 1. create a datasource (which will be the source and target of the materialized view)
        params = {"mode": "create", "name": ds1, "schema": "number Int32", "token": token}
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        # 2. create a pipe with a materialized view
        Users.add_pipe_sync(workspace, pipe_name, "select * from test_table")
        params = {
            "token": token,
            "name": node_name,
            "type": "materialized",
            "datasource": ds1,
            "skip_table_checks": "true",
        }
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=f"SELECT * FROM {ds1}"
        )
        self.assertEqual(response.code, 200)

        # 3. unlink the materialized view
        params = {"token": token}
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}/materialization?{urlencode(params)}", method="DELETE"
        )
        self.assertEqual(response.code, 204)

    @tornado.testing.gen_test
    async def test_cannot_update_node_used_in_materialized_node(self):
        rand_id = uuid.uuid4().hex[0:6]
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = f"cannot_update_{rand_id}"
        node_name = f"node_1{rand_id}"

        another_pipe_name = f"another_pipe_{rand_id}"
        data = json.dumps(
            {
                "name": pipe_name,
                "nodes": [
                    {"name": node_name, "sql": "select * from test_table"},
                    {
                        "name": f"node_2{rand_id}",
                        "sql": f"select * from {node_name}",
                        "type": "materialized",
                        "datasource": f"ds_{node_name}",
                        "engine": "MergeTree",
                    },
                ],
            }
        )
        response = await self.fetch_async(
            f"/v0/pipes?token={token}", headers={"Content-type": "application/json"}, method="POST", body=data
        )
        self.assertEqual(response.code, 200)

        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}?token={token}",
            headers={"Content-type": "application/json"},
            method="PUT",
            body="select * from test_table where a > 1",
        )
        self.assertEqual(response.code, 403)

        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}?token={token}",
            headers={"Content-type": "application/json"},
            method="DELETE",
            body=None,
        )
        self.assertEqual(response.code, 403)

        # create a different pipe with the same node_name and try to edit
        another_pipe_name = f"another_pipe_{rand_id}"
        data = json.dumps(
            {
                "name": another_pipe_name,
                "nodes": [
                    {"name": node_name, "sql": "select * from test_table"},
                    {"name": f"node_2{rand_id}", "sql": f"select * from {node_name}"},
                ],
            }
        )
        response = await self.fetch_async(
            f"/v0/pipes?token={token}", headers={"Content-type": "application/json"}, method="POST", body=data
        )
        self.assertEqual(response.code, 200)

        # editing another_pipe_name works
        response = await self.fetch_async(
            f"/v0/pipes/{another_pipe_name}/nodes/{node_name}?token={token}",
            headers={"Content-type": "application/json"},
            method="PUT",
            body="select * from test_table where a > 0",
        )
        self.assertEqual(response.code, 200)

        # editing pipe_name does not work as expected
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}?token={token}",
            headers={"Content-type": "application/json"},
            method="PUT",
            body="select * from test_table where a > {i}",
        )
        self.assertEqual(response.code, 403)

    @tornado.testing.gen_test
    async def test_cannot_update_endpoint_used_in_materialized_node(self):
        rand_id = uuid.uuid4().hex[0:6]
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = f"cannot_update_{rand_id}"
        node_name = f"node_1{rand_id}"
        endpoint_name = f"e_{pipe_name}"

        endpoint_data = json.dumps(
            {
                "name": endpoint_name,
                "nodes": [
                    {"name": f"{node_name}_0", "sql": "select * from test_table"},
                    {"name": node_name, "sql": f"select * from {node_name}_0"},
                ],
            }
        )
        response = await self.fetch_async(
            f"/v0/pipes?token={token}", headers={"Content-type": "application/json"}, method="POST", body=endpoint_data
        )
        self.assertEqual(response.code, 200)

        response = await self.fetch_async(
            f"/v0/pipes/{endpoint_name}/nodes/{node_name}/endpoint?token={token}",
            headers={"Content-type": "application/json"},
            method="POST",
            body=b"",
        )
        self.assertEqual(response.code, 200)

        data = json.dumps(
            {
                "name": pipe_name,
                "nodes": [
                    {"name": node_name, "sql": f"select * from {endpoint_name}"},
                    {
                        "name": f"node_2{rand_id}",
                        "sql": f"select * from {node_name}",
                        "type": "materialized",
                        "datasource": f"ds_{node_name}",
                        "engine": "MergeTree",
                    },
                ],
            }
        )
        response = await self.fetch_async(
            f"/v0/pipes?token={token}", headers={"Content-type": "application/json"}, method="POST", body=data
        )
        self.assertEqual(response.code, 200)

        response = await self.fetch_async(
            f"/v0/pipes/{endpoint_name}/nodes/{node_name}?token={token}",
            headers={"Content-type": "application/json"},
            method="PUT",
            body="select * from test_table where a > 1",
        )
        self.assertEqual(response.code, 403)

        response = await self.fetch_async(
            f"/v0/pipes/{endpoint_name}/nodes/{node_name}/endpoint?token={token}",
            headers={"Content-type": "application/json"},
            method="DELETE",
            body=None,
        )
        self.assertEqual(response.code, 403)
        self.assertTrue("Cannot modify the node" in json.loads(response.body)["error"], response.body)

        response = await self.fetch_async(
            f"/v0/pipes/{endpoint_name}/nodes/{node_name}_0/endpoint?token={token}",
            headers={"Content-type": "application/json"},
            method="POST",
            body=b"",
        )
        self.assertEqual(response.code, 403)
        self.assertTrue("Cannot modify the node" in json.loads(response.body)["error"], response.body)

        # cannot force push the endpoint
        response = await self.fetch_async(
            f"/v0/pipes?token={token}&force=true",
            headers={"Content-type": "application/json"},
            method="POST",
            body=endpoint_data,
        )
        self.assertEqual(response.code, 403)
        self.assertTrue("Cannot modify the node" in json.loads(response.body)["error"], response.body)

        # cannot delete the pipe
        response = await self.fetch_async(
            f"/v0/pipes/{endpoint_name}?token={token}", headers={"Content-type": "application/json"}, method="DELETE"
        )
        self.assertEqual(response.code, 403)
        self.assertTrue("Cannot modify the node" in json.loads(response.body)["error"], response.body)

        # cannot rename the pipe
        response = await self.fetch_async(
            f"/v0/pipes/{endpoint_name}?token={token}&name=new_{endpoint_name}", method="PUT", body=b""
        )
        self.assertEqual(response.code, 403)
        self.assertTrue("Cannot modify the node" in json.loads(response.body)["error"], response.body)

        # create a different pipe with the same node_name and try to edit
        another_endpoint_name = f"can_update{endpoint_name}"
        data = json.dumps(
            {"name": another_endpoint_name, "nodes": [{"name": node_name, "sql": "select * from test_table"}]}
        )
        response = await self.fetch_async(
            f"/v0/pipes?token={token}", headers={"Content-type": "application/json"}, method="POST", body=data
        )
        self.assertEqual(response.code, 200)

        response = await self.fetch_async(
            f"/v0/pipes/{another_endpoint_name}/nodes/{node_name}/endpoint?token={token}",
            headers={"Content-type": "application/json"},
            method="POST",
            body=b"",
        )
        self.assertEqual(response.code, 200)

        # can edit another_endpoint_name
        response = await self.fetch_async(
            f"/v0/pipes/{another_endpoint_name}/nodes/{node_name}?token={token}",
            headers={"Content-type": "application/json"},
            method="PUT",
            body="select * from test_table where a > 0",
        )
        self.assertEqual(response.code, 200)

        # cannot edit endpoint_name
        response = await self.fetch_async(
            f"/v0/pipes/{endpoint_name}/nodes/{node_name}?token={token}",
            headers={"Content-type": "application/json"},
            method="PUT",
            body="select * from test_table where a > 0",
        )
        self.assertEqual(response.code, 403)
        self.assertTrue("Cannot modify the node" in json.loads(response.body)["error"], response.body)

    def test_view_creation_calculates_engine(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_to_invalid_datasource"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # let's create a landing datasource
        ds_name_source = "ds_to_source"
        params = {"token": token, "name": ds_name_source, "schema": "a UInt64", "engine": "Null"}
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        ds_name_missing_target = "ds_for_view_to_missing_target"

        # create a pipe's node with a view to proxy from source to target
        params = {
            "token": token,
            "name": "mat_view_node_to",
            "type": "materialized",
            "datasource": ds_name_missing_target,
        }
        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}",
            method="POST",
            body=f"select a * 10 as x, a * 100 as y from {ds_name_source}",
        )
        result = json.loads(response.body)
        self.assertEqual(response.code, 200, result)
        self.assertEqual(result.get("datasource", {}).get("engine", {}).get("engine"), "MergeTree")
        self.assertTrue(result["created_datasource"])

    def test_view_creation_with_same_engine_settings(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_different_engine_settings"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        ds_name_source = "ds_for_view_with_same_engine_settings"

        params = {
            "token": token,
            "name": ds_name_source,
            "schema": "d DateTime, b String, sum_units AggregateFunction(sum, Int32)",
            "engine": "AggregatingMergeTree",
            "engine_partition_key": "toHour(d)",
            "engine_sorting_key": "(d, b)",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        params = {
            "token": token,
            "type": "materialized",
            "datasource": ds_name_source,
            "engine": "AggregatingMergeTree",
            "engine_partition_key": "toHour(d)",
            "engine_sorting_key": "(d, b)",
        }

        query = """
            SELECT
                toDateTime(a) AS d,
                toString(a) AS b,
                sumState(toInt32(a)) AS sum_units
            FROM test_table as t
            GROUP BY
                d, b
        """

        response = self.fetch(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)
        self.assertEqual(response.code, 200, response.body)

    def test_view_creation_to_fail_on_different_engine_settings(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_different_engine_settings"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        ds_name_source = "ds_for_view_with_defined_engine_settings"

        params = {
            "token": token,
            "name": ds_name_source,
            "schema": "d DateTime, b String, sum_units AggregateFunction(sum, Int32)",
            "engine": "AggregatingMergeTree",
            "engine_partition_key": "toHour(d)",
            "engine_sorting_key": "(d, b)",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        params = {
            "token": token,
            "type": "materialized",
            "datasource": ds_name_source,
            "engine": "AggregatingMergeTree",
            "engine_partition_key": "toYYYYMM(d)",
            "engine_sorting_key": "(d, b)",
        }

        query = """
            SELECT
                toDateTime(a) AS d,
                toString(a) AS b,
                sumState(toInt32(a)) AS sum_units
            FROM test_table as t
            GROUP BY
                d, b
        """

        response = self.fetch(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)
        self.assertEqual(response.code, 400, response.body)
        result = json.loads(response.body)

        self.assertTrue(
            "The engine settings are already configured for 'ds_for_view_with_defined_engine_settings' Data Source, and are not compatible with the engine settings used to materialize ('ENGINE_PARTITION_KEY \"toHour(d)\"' and 'ENGINE_PARTITION_KEY \"toYYYYMM(d)\"' don't match). Either you remove the settings to materialize or choose a different Data Source and try again."
            in result.get("error")
        )

    @tornado.testing.gen_test
    async def test_datasource_override_is_forbidden_if_target_datasource_is_shared(self):
        rand_id = uuid.uuid4().hex[0:6]
        tb_api_proxy_async = TBApiProxyAsync(self)
        workspace_a = Users.get_by_id(self.WORKSPACE_ID)
        user_a = UserAccount.get_by_id(self.USER_ID)
        token_a = Users.get_token_for_scope(workspace_a, scopes.ADMIN)
        token_user_a = UserAccount.get_token_for_scope(user_a, scopes.AUTH)

        ws_b_email = f"test_datasource_override_is_forbidden_{uuid.uuid4().hex}@example.com"
        workspace_b = await tb_api_proxy_async.register_user_and_workspace(
            ws_b_email, workspace_a.name, normalize_name_and_try_different_on_collision=True
        )
        user_b = UserAccount.get_by_email(ws_b_email)
        token_user_b = UserAccount.get_token_for_scope(user_b, scopes.AUTH)

        ds_name_source = f"ds_{rand_id}"
        pipe_name = f"p_{rand_id}"
        Users.add_pipe_sync(workspace_a, pipe_name, "select * from test_table")

        params = {
            "token": token_a,
            "name": ds_name_source,
            "schema": "d DateTime, b String, sum_units AggregateFunction(sum, Int32)",
            "engine": "AggregatingMergeTree",
            "engine_partition_key": "toHour(d)",
            "engine_sorting_key": "(d, b)",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        await tb_api_proxy_async.invite_user_to_workspace(
            token=token_user_b, workspace_id=workspace_b.id, user_to_invite_email=user_a.email
        )

        ds = Users.get_datasource(workspace_a, ds_name_source)
        await tb_api_proxy_async.share_datasource_with_another_workspace(
            token=token_user_a,
            datasource_id=ds.id,
            origin_workspace_id=workspace_a.id,
            destination_workspace_id=workspace_b.id,
        )

        params = {
            "token": token_a,
            "type": "materialized",
            "datasource": ds_name_source,
            "override_datasource": "true",
            "engine": "AggregatingMergeTree",
            "engine_partition_key": "toHour(d)",
            "engine_sorting_key": "(d, b)",
        }

        query = """
            SELECT
                toDateTime(a) AS d,
                toString(a) AS b,
                sumState(toInt32(a)) AS sum_units
            FROM test_table as t
            GROUP BY
                d, b
        """

        response = await self.fetch_async(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)
        self.assertEqual(response.code, 409, response.body)
        self.assertTrue(
            "Cannot override Materialized View because it's shared with other Workspaces. If you want to perform that operation you can work with versions"
            in json.loads(response.body)["error"]
        )

    @tornado.testing.gen_test
    async def test_node_append_with_override_on_different_engine_settings(self):
        suffix = "test_node_append_with_override_on_different_engine_settings"
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = f"p_{suffix}"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        ds_name_source = f"ds_{suffix}"

        params = {
            "token": token,
            "name": ds_name_source,
            "schema": "d DateTime, b String, sum_units AggregateFunction(sum, Int32)",
            "engine": "AggregatingMergeTree",
            "engine_partition_key": "toHour(d)",
            "engine_sorting_key": "(d, b)",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        params = {
            "token": token,
            "type": "materialized",
            "datasource": ds_name_source,
            "override_datasource": "false",
            "engine": "AggregatingMergeTree",
            "engine_partition_key": "toYYYYMM(d)",
            "engine_sorting_key": "(d, b)",
        }

        query = """
            SELECT
                toDateTime(a) AS d,
                toString(a) AS b,
                sumState(toInt32(a)) AS sum_units
            FROM test_table as t
            GROUP BY
                d, b
        """

        response = await self.fetch_async(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)
        self.assertEqual(response.code, 400, response.body)
        self.assertTrue(
            "please send `override_datasource=true` as a node parameter in the request"
            in json.loads(response.body)["error"]
        )

        params = {
            "token": token,
            "type": "materialized",
            "datasource": ds_name_source,
            "override_datasource": "true",
            "engine": "AggregatingMergeTree",
            "engine_partition_key": "toYYYYMM(d)",
            "engine_sorting_key": "(d, b)",
        }

        query = """
            SELECT
                toDateTime(a) AS d,
                toString(a) AS b,
                sumState(toInt32(a)) AS sum_units
            FROM test_table as t
            GROUP BY
                d, b
        """

        response = await self.fetch_async(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        engine = {"engine": "AggregatingMergeTree", "partition_key": "toYYYYMM(d)", "sorting_key": "d, b"}

        self.assertEqual(result["datasource"]["engine"], engine, result)

    @tornado.testing.gen_test
    async def test_node_materialize_with_override_on_different_engine_settings(self):
        suffix = "test_node_materialize_with_override_on_different_engine_settings"
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = f"p_{suffix}"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        ds_name_source = f"ds_{suffix}"

        params = {
            "token": token,
            "name": ds_name_source,
            "schema": "d DateTime, b String, sum_units AggregateFunction(sum, Int32)",
            "engine": "AggregatingMergeTree",
            "engine_partition_key": "toHour(d)",
            "engine_sorting_key": "(d, b)",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        params = {
            "token": token,
            "datasource": ds_name_source,
        }

        query = """
            SELECT
                toDateTime(a) AS d,
                toString(a) AS b,
                sumState(toInt32(a)) AS sum_units
            FROM test_table as t
            GROUP BY
                d, b
        """

        response = await self.fetch_async(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)
        self.assertEqual(response.code, 200, response.body)
        node = json.loads(response.body)["id"]

        params = {
            "token": token,
            "datasource": ds_name_source,
            "override_datasource": "false",
            "engine": "AggregatingMergeTree",
            "engine_partition_key": "toYYYYMM(d)",
            "engine_sorting_key": "(d, b)",
        }

        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{node}/materialization?{urlencode(params)}", method="POST", body=query
        )
        self.assertEqual(response.code, 400, response.body)
        self.assertTrue(
            "please send `override_datasource=true` as a node parameter in the request"
            in json.loads(response.body)["error"]
        )

        params = {
            "token": token,
            "datasource": ds_name_source,
            "override_datasource": "true",
            "engine": "AggregatingMergeTree",
            "engine_partition_key": "toYYYYMM(d)",
            "engine_sorting_key": "(d, b)",
        }

        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{node}/materialization?{urlencode(params)}", method="POST", body=query
        )
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        engine = {"engine": "AggregatingMergeTree", "partition_key": "toYYYYMM(d)", "sorting_key": "d, b"}

        self.assertEqual(result["datasource"]["engine"], engine, result)

    @tornado.testing.gen_test
    async def test_node_append_with_override_on_different_nodes_with_same_name(self):
        suffix = "test_node_append_with_override_on_different_nodes_with_same_name"
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = f"p_{suffix}"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        pipe_name2 = f"p_{suffix}_2"
        Users.add_pipe_sync(u, pipe_name2, "select * from test_table")

        pipe_name3 = f"p_{suffix}_3"
        Users.add_pipe_sync(u, pipe_name3, "select * from test_table")

        ds_name_source = f"ds_{suffix}"

        params = {
            "token": token,
            "name": ds_name_source,
            "schema": "d DateTime, b String, sum_units AggregateFunction(sum, Int32)",
            "engine": "AggregatingMergeTree",
            "engine_partition_key": "toHour(d)",
            "engine_sorting_key": "(d, b)",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        params = {"token": token, "type": "materialized", "name": "test", "datasource": ds_name_source}

        query = """
            SELECT
                toDateTime(a) AS d,
                toString(a) AS b,
                sumState(toInt32(a)) AS sum_units
            FROM test_table as t
            GROUP BY
                d, b
        """

        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name2}/nodes?{urlencode(params)}", method="POST", body=query
        )
        self.assertEqual(response.code, 200, response.body)

        params = {"token": token, "type": "materialized", "name": "test", "datasource": ds_name_source}

        query = """
            SELECT
                toDateTime(a) AS d,
                toString(a) AS b,
                sumState(toInt32(a)) AS sum_units
            FROM test_table as t
            GROUP BY
                d, b
        """

        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name3}/nodes?{urlencode(params)}", method="POST", body=query
        )
        self.assertEqual(response.code, 200, response.body)

        params = {
            "token": token,
            "type": "materialized",
            "datasource": ds_name_source,
            "override_datasource": "true",
            "engine": "AggregatingMergeTree",
            "engine_partition_key": "toYYYYMM(d)",
            "engine_sorting_key": "(d, b)",
        }

        query = """
            SELECT
                toDateTime(a) AS d,
                toString(a) AS b,
                sumState(toInt32(a)) AS sum_units
            FROM test_table as t
            GROUP BY
                d, b
        """

        response = await self.fetch_async(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)
        self.assertEqual(response.code, 409, response.body)

    @tornado.testing.gen_test
    async def test_pipe_with_override_on_different_engine_settings(self):
        suffix = "test_pipe_with_override_on_different_engine_settings"
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = f"p_{suffix}"

        ds_name_source = f"ds_{suffix}"

        params = {
            "token": token,
            "name": ds_name_source,
            "schema": "d DateTime, b String, sum_units AggregateFunction(sum, Int32)",
            "engine": "AggregatingMergeTree",
            "engine_partition_key": "toHour(d)",
            "engine_sorting_key": "(d, b)",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        node_params = {
            "type": "materialized",
            "datasource": ds_name_source,
            "override_datasource": "false",
            "engine": "AggregatingMergeTree",
            "engine_partition_key": "toYYYYMM(d)",
            "engine_sorting_key": "(d, b)",
        }

        query = """
            SELECT
                toDateTime(a) AS d,
                toString(a) AS b,
                sumState(toInt32(a)) AS sum_units
            FROM test_table as t
            GROUP BY
                d, b
        """

        data = json.dumps({"name": pipe_name, "nodes": [{"name": f"{pipe_name}_1", "sql": query, **node_params}]})

        params = {"token": token}

        response = await self.fetch_async(
            f"/v0/pipes?{urlencode(params)}", headers={"Content-type": "application/json"}, method="POST", body=data
        )
        self.assertEqual(response.code, 400, response.body)
        self.assertTrue(
            "please send `override_datasource=true` as a node parameter in the request"
            in json.loads(response.body)["error"]
        )

        node_params["override_datasource"] = "true"
        data = json.dumps({"name": pipe_name, "nodes": [{"name": f"{pipe_name}_1", "sql": query, **node_params}]})
        response = await self.fetch_async(
            f"/v0/pipes?{urlencode(params)}", headers={"Content-type": "application/json"}, method="POST", body=data
        )
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        engine = {"engine": "AggregatingMergeTree", "partition_key": "toYYYYMM(d)", "sorting_key": "d, b"}

        self.assertEqual(result["datasource"]["engine"], engine, result)

        # let's override also the whole pipe and check there are no leftovers from previous pipe instance
        mat_view_id = result["nodes"][0]["id"]
        target_datasource_id = result["nodes"][0]["materialized"]

        node_params = {
            "type": "materialized",
            "datasource": ds_name_source,
            "override_datasource": "true",
            "engine": "AggregatingMergeTree",
            "engine_partition_key": "toYYYYMM(d)",
            "engine_sorting_key": "(d)",
        }

        query = """
            SELECT
                toDateTime(a) AS d,
                sumState(toInt32(a)) AS sum_units
            FROM test_table as t
            GROUP BY
                d
        """

        data = json.dumps({"name": pipe_name, "nodes": [{"name": f"{pipe_name}_1", "sql": query, **node_params}]})

        params = {"token": token, "force": "true", "populate": "true"}

        response = await self.fetch_async(
            f"/v0/pipes?{urlencode(params)}", headers={"Content-type": "application/json"}, method="POST", body=data
        )
        self.assertEqual(response.code, 200, response.body)

        result = json.loads(response.body)
        new_mat_view_id = result["nodes"][0]["id"]
        new_target_datasource_id = result["nodes"][0]["materialized"]

        self.assertTrue(mat_view_id != new_mat_view_id)
        self.assertTrue(new_target_datasource_id != target_datasource_id)

        self._check_table_in_database(u.database, mat_view_id, exists=False)
        self._check_table_in_database(u.database, target_datasource_id, exists=False)
        self.assertTrue(Users.get_datasource(u, target_datasource_id) is None)

        job = await self.get_finalised_job_async(result["job"]["id"])
        self.assertEqual(job.status, "done")

        self.expect_ops_log(
            [
                {"event_type": "create", "datasource_name": ds_name_source},
                {"event_type": "delete", "datasource_name": ds_name_source},
                {"event_type": "delete", "datasource_name": ds_name_source},
                {
                    "event_type": "populateview-queued",
                    "datasource_name": ds_name_source,
                    "pipe_name": f"{pipe_name}__override",
                    "result": "ok",
                },
                {
                    "event_type": "populateview",
                    "datasource_name": ds_name_source,
                    "result": "ok",
                    "pipe_name": f"{pipe_name}__override",
                    "read_rows": 6,
                    "written_rows": 6,
                    "cpu_time": numericRange(0.00001, 10),
                },
            ]
        )

    @tornado.testing.gen_test
    async def test_pipe_cascade_with_override_on_different_engine_settings(self):
        suffix = "test_pipe_cascade_with_override_on_different_engine_settings"
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name_0 = f"p_{suffix}_0"
        pipe_name = f"p_{suffix}"

        # test_table -> pipe_name_0 -> ds_name_source_0 -> pipe_name -> ds_name_source
        # then try to override ds_name_source_0

        # create ds_name_source_0
        ds_name_source_0 = f"ds_{suffix}_0"
        params = {
            "token": token,
            "name": ds_name_source_0,
            "schema": "a Int32",
            "engine": "MergeTree",
            "engine_partition_key": "tuple()",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        # create ds_name_source
        ds_name_source = f"ds_{suffix}"
        params = {
            "token": token,
            "name": ds_name_source,
            "schema": "d DateTime, b String, sum_units AggregateFunction(sum, Int32)",
            "engine": "AggregatingMergeTree",
            "engine_partition_key": "toHour(d)",
            "engine_sorting_key": "(d, b)",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        # create test_table -> pipe_name_0 -> ds_name_source_0
        node_params = {"type": "materialized", "datasource": ds_name_source_0}

        query = """ SELECT toInt32(a) as a FROM test_table"""

        data = json.dumps({"name": pipe_name_0, "nodes": [{"name": f"{pipe_name_0}_1", "sql": query, **node_params}]})

        params = {"token": token}

        response = await self.fetch_async(
            f"/v0/pipes?{urlencode(params)}", headers={"Content-type": "application/json"}, method="POST", body=data
        )
        self.assertEqual(response.code, 200, response.body)

        # create ds_name_source_0 -> pipe_name -> ds_name_source
        node_params = {"type": "materialized", "datasource": ds_name_source}

        query = f"""
            SELECT
                toDateTime(a) AS d,
                toString(a) AS b,
                sumState(toInt32(a)) AS sum_units
            FROM {ds_name_source_0} as t
            GROUP BY
                d, b
        """

        data = json.dumps({"name": pipe_name, "nodes": [{"name": f"{pipe_name}_1", "sql": query, **node_params}]})

        params = {"token": token}

        response = await self.fetch_async(
            f"/v0/pipes?{urlencode(params)}", headers={"Content-type": "application/json"}, method="POST", body=data
        )
        self.assertEqual(response.code, 200, response.body)

        # try to override ds_name_source_0
        node_params = {
            "type": "materialized",
            "datasource": ds_name_source_0,
            "engine": "MergeTree",
            "engine_partition_key": "a",
        }

        query = """ SELECT toInt32(a) as a FROM test_table"""

        data = json.dumps({"name": pipe_name_0, "nodes": [{"name": f"{pipe_name_0}_1", "sql": query, **node_params}]})

        params = {"token": token, "force": "true"}

        response = await self.fetch_async(
            f"/v0/pipes?{urlencode(params)}", headers={"Content-type": "application/json"}, method="POST", body=data
        )
        self.assertEqual(response.code, 400, response.body)

        node_params["override_datasource"] = "true"
        data = json.dumps({"name": pipe_name, "nodes": [{"name": f"{pipe_name_0}_1", "sql": query, **node_params}]})
        response = await self.fetch_async(
            f"/v0/pipes?{urlencode(params)}", headers={"Content-type": "application/json"}, method="POST", body=data
        )
        # since there are dependent matviews you cannot replace
        self.assertEqual(response.code, 409, response.body)
        self.assertTrue(
            "If you want to perform that operation you can work with versions" in json.loads(response.body)["error"]
        )

    def test_view_creation_to_fail_on_invalid_dist_sorting_keys(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_to_invalid_agg_datasource"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        ds_name_source = "ds_for_view_to_source_populate_and_replace"

        params = {
            "token": token,
            "name": ds_name_source,
            "schema": "d DateTime, b String, sum_units AggregateFunction(sum, Int32)",
            "engine": "AggregatingMergeTree",
            "engine_partition_key": "toHour(d)",
            "engine_sorting_key": "(d, b)",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        params = {
            "token": token,
            "name": "mat_view_node_with_wrong_types",
            "type": "materialized",
            "datasource": ds_name_source,
        }

        query = """
            SELECT
                now() as d,
                toString(a) as b,
                sumState(a) AS sum_units
            FROM test_table
            GROUP BY d, b
        """

        response = self.fetch(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)

        result = json.loads(response.body)
        self.assertEqual(response.code, 400, response.body)
        self.assertTrue(
            "Incompatible column types {'sum_units': 'AggregateFunction(sum, Int32)'} "
            "(Data Source) != {'sum_units': 'AggregateFunction(sum, UInt64)'} (pipe): "
            "Automatic conversion from AggregateFunction(sum, UInt64) to "
            "AggregateFunction(sum, Int32) is not supported: "
            "Different #0 argument: UInt64 vs Int32." in result["error"]
        )

        name = "mat_view_node_with_wrong_group_by_keys"
        params = {"token": token, "name": name, "type": "materialized", "datasource": ds_name_source}

        query = """
            SELECT
                toDateTime(a) AS d,
                toString(a) AS b,
                sumState(toInt32(a)) AS sum_units
            FROM test_table as t
            GROUP BY
                a
        """

        response = self.fetch(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)

        result = json.loads(response.body)

        self.assertEqual(response.code, 400, response.body)
        # FIXME: remove comment when upgrading to CH 22+
        # self.assertTrue("Column 'a' is present in the GROUP BY but not in the SELECT clause" in result['error'])
        self.assertTrue(
            "Columns used in GROUP BY do not match the columns from the ENGINE_SORTING_KEY in the destination Data Source. Please, make sure columns present in the ENGINE_SORTING_KEY (d, b) are the same than the ones used in the GROUP BY (a)"
            in result["error"]
        )

        query = """
            SELECT
                toDateTime(a) AS d,
                sumState(toInt32(a)) AS sum_units
            FROM test_table as t
            GROUP BY
                d
        """

        response = self.fetch(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)

        result = json.loads(response.body)

        self.assertEqual(response.code, 400, response.body)
        self.assertTrue(
            "Columns used in GROUP BY do not match the columns from the ENGINE_SORTING_KEY in the destination Data Source. Please, make sure columns present in the ENGINE_SORTING_KEY (d, b) are the same than the ones used in the GROUP BY (d)"
            in result["error"]
        )

        name = "mat_view_node_with_right_keys"
        params = {"token": token, "name": name, "type": "materialized", "datasource": ds_name_source}

        query = """
            SELECT
                toDateTime(a) AS d,
                toString(a) AS b,
                sumState(toInt32(a)) AS sum_units
            FROM test_table as t
            GROUP BY
                d, b
        """

        response = self.fetch(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)

        result = json.loads(response.body)

        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(result["name"], name)

    def test_view_creation_to_fail_on_invalid_dist_sorting_keys_using_simple_agg_function(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_to_invalid_agg_datasource"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        ds_name_source = "ds_for_view_to_source_populate_and_replace"

        params = {
            "token": token,
            "name": ds_name_source,
            "schema": "d DateTime, b String, any_a SimpleAggregateFunction(any, Nullable(Int32)), group_b SimpleAggregateFunction(groupArrayArray, Array(String))",
            "engine": "AggregatingMergeTree",
            "engine_partition_key": "toHour(d)",
            "engine_sorting_key": "(d, b)",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        params = {
            "token": token,
            "name": "mat_view_node_with_wrong_types_simple_agg",
            "type": "materialized",
            "datasource": ds_name_source,
        }

        query = """
            SELECT
                now() as d,
                toString(a) as b,
                any(a) AS any_a,
                groupArray(b) as group_b
            FROM test_table
            GROUP BY d, b
        """

        response = self.fetch(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)

        result = json.loads(response.body)
        self.assertEqual(response.code, 400, response.body)
        self.assertTrue(
            """Incompatible column types {'any_a': 'SimpleAggregateFunction(any, Nullable(Int32))'} (Data Source) != {'any_a': 'UInt64'} (pipe): Automatic conversion from UInt64 to SimpleAggregateFunction(any, Nullable(Int32)) is not supported: UInt64 might contain values that won't fit inside a column of type SimpleAggregateFunction(any, Nullable(Int32))"""
            in result["error"]
        )

        name = "mat_view_node_with_right_simple_agg"
        params = {"token": token, "name": name, "type": "materialized", "datasource": ds_name_source}

        query = """
            SELECT
                now() as d,
                toString(a) as b,
                any(a) AS any_a,
                groupArray(b) as group_b
            FROM (
                SELECT
                    toInt32(a) as a
                FROM test_table
            )
            GROUP BY d, b
        """

        response = self.fetch(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)

        result = json.loads(response.body)

        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(result["name"], name)

    def test_view_creation_using_check_explain(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_check_explains"

        ds_name_origin_source = "origin_test_table"

        params = {"token": token, "name": ds_name_origin_source, "schema": "a UInt64, b DateTime, c Int64"}

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        pipe = Users.add_pipe_sync(
            u,
            pipe_name,
            f"""
            SELECT
                toStartOfDay(b) as b,
                countState() as c
            FROM {ds_name_origin_source}
            GROUP BY b
            """,
        )

        first_node = pipe.pipeline.nodes[0].name

        ds_name_source = "ds_for_view_to_source_populate_and_replace"

        params = {
            "token": token,
            "name": "mat_view_node_with_function_over_sorting_key",
            "type": "materialized",
            "datasource": ds_name_source,
            "engine": "AggregatingMergeTree",
            "engine_sorting_key": "b",
        }

        query = f"""
            SELECT * FROM {first_node}
        """

        response = self.fetch(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)

        self.assertEqual(response.code, 200, response.body)

    @tornado.testing.gen_test
    async def test_delete_and_rename_join_ds_used_in_view(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        async def create_datasource(name, schema, engine=None):
            params = {
                "token": token,
                "name": name,
                "schema": schema,
            }
            if engine:
                params.update(engine)
            create_url = f"/v0/datasources?{urlencode(params)}"
            response = await self.fetch_async(create_url, method="POST", body="")
            self.assertEqual(response.code, 200, response.body)
            return json.loads(response.body)

        async def append_to_ds(name, data):
            params = {"token": token, "name": name, "mode": "replace"}
            create_url = f"/v0/datasources?{urlencode(params)}"
            response = await self.fetch_full_body_upload_async(create_url, data)
            self.assertEqual(response.code, 200, response.body)
            return json.loads(response.body)

        customers_ds = "customers"
        await create_datasource(
            customers_ds,
            "customer_id UInt64, country String",
            engine={
                "engine": "Join",
                "engine_join_strictness": "ANY",
                "engine_join_type": "LEFT",
                "engine_key_columns": "customer_id",
            },
        )

        landing_ds = "visits"
        await create_datasource(landing_ds, "customer_id UInt64, date Date")
        destination_ds = "visits_augmented"
        await create_datasource(destination_ds, "customer_id UInt64, date Date, customer_country String")

        pipe_name = "etl_augment_visits"
        Users.add_pipe_sync(u, pipe_name, nodes=[])
        node_name = "augment_visits"
        params = {"token": token, "name": node_name, "type": "materialized", "datasource": destination_ds}
        node_sql = """SELECT
            customer_id,
            date,
            joinGet('customers', 'country', customer_id) as customer_country
        FROM visits"""
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=node_sql
        )
        self.assertEqual(response.code, 200, response.body)

        await append_to_ds(customers_ds, StringIO("1,Spain\n2,Portugal"))
        await append_to_ds(landing_ds, StringIO("1,2020-01-01\n1,2020-02-01\n2,2020-06-01"))

        async def get_result():
            params = {
                "token": token,
                "q": f"""SELECT
                        customer_country,
                        count() c
                    FROM {destination_ds}
                    GROUP BY customer_country
                    ORDER BY c DESC
                    FORMAT JSON""",
            }
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            self.assertEqual(response.code, 200)
            result = json.loads(response.body)
            self.assertEqual(
                result["data"], [{"customer_country": "Spain", "c": 2}, {"customer_country": "Portugal", "c": 1}]
            )

        await poll_async(get_result)

        response = await self.fetch_async(f"/v0/datasources/{customers_ds}?token={token}", method="DELETE")
        self.assertEqual(response.code, 409, response.body)
        self.assertEqual(
            json.loads(response.body)["error"],
            'This operation will break ingestion due to broken Materialized Views, unlink the Materialized Nodes or remove the dependency with the Data Source. Affected downstream materializations => Pipes="etl_augment_visits", nodes="augment_visits". The Data Source is used in => Pipes="etl_augment_visits", nodes="augment_visits"',
        )

        response = await self.fetch_async(
            f"/v0/datasources/{customers_ds}?token={token}&name={customers_ds}_renamed", method="PUT", body=b""
        )
        self.assertEqual(response.code, 200, response.body)

        # pipe is updated as well
        response = await self.fetch_async(f"/v0/pipes/{pipe_name}?token={token}")
        node = json.loads(response.body)["nodes"][0]
        self.assertEqual("customers_renamed" in node["sql"], True, response.body)
        self.assertEqual("customers_renamed" in node["dependencies"], True, response.body)

        await append_to_ds(landing_ds, StringIO("2,2020-07-01\n1,2020-08-01"))

        response = await self.fetch_async(f"/v0/pipes/{pipe_name}?token={token}", method="DELETE")
        self.assertEqual(response.code, 204, response.body)

        response = await self.fetch_async(f"/v0/datasources/{customers_ds}_renamed?token={token}", method="DELETE")
        self.assertEqual(response.code, 204, response.body)

        await append_to_ds(landing_ds, StringIO("2,2020-07-01\n1,2020-08-01"))

    def test_raise_error_on_invalid_engine_in_builtin_target_datasource(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_to_invalid_datasource_engine"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        target_ds_name = "ds_invalid_engine"
        params = {
            "token": token,
            "name": "mat_view_node_to_create_new_ds_wrong_engine",
            "type": "materialized",
            "datasource": target_ds_name,
            "engine": "AggregatingMergeTree",
        }

        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}",
            method="POST",
            body="SELECT a, uniqState(c) as c FROM test_table GROUP BY a",
        )
        result = json.loads(response.body)
        self.assertEqual(response.code, 400, response.body)
        self.assertTrue("Missing required option 'sorting_key'" in result["error"])

        datasource = Users.get_datasource(u, target_ds_name)
        self.assertEqual(datasource, None)

    @tornado.testing.gen_test
    async def test_invalid_engine_is_rejected(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        base_datasource_name = "landing_ds"
        csv_url = self.get_url_for_sql("SELECT 'a' as a format CSVWithNames")
        params = {
            "token": token,
            "name": base_datasource_name,
            "mode": "append",
            "url": csv_url,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done")

        # create a pipe's node with a view to that datasource
        pipe_name = "test_invalid_engine_is_rejected"
        Users.add_pipe_sync(u, pipe_name, "select * from landing_ds")
        node_name = "test_invalid_engine_is_rejected_node"
        params = {"token": token, "name": node_name}
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body="select * from landing_ds"
        )
        self.assertEqual(response.code, 200)

        # materialize view
        target_ds_name = "test_invalid_engine_is_rejected_ds"
        params = {"token": token, "datasource": target_ds_name, "engine": "Distributed"}
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}/materialization?{urlencode(params)}", method="POST", body=""
        )
        result = json.loads(response.body)

        self.assertEqual(response.code, 400, response.body)
        self.assertTrue("Engine Distributed is not supported" in result.get("error"))
        self.assertIsNotNone(result.get("documentation"))

    @tornado.testing.gen_test
    async def test_invalid_source_view_is_rejected(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        base_datasource_name = "landing_ds"
        csv_url = self.get_url_for_sql("SELECT number FROM numbers(1) format CSVWithNames")
        params = {
            "token": token,
            "name": base_datasource_name,
            "mode": "append",
            "url": csv_url,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done")

        # create a pipe's node with a view to that datasource
        pipe_name = "mv_from_table_function"
        Users.add_pipe_sync(u, pipe_name, "select * from landing_ds")
        node_name = "node"
        params = {"token": token, "name": node_name}
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body="SELECT * from numbers(1000)"
        )
        self.assertEqual(response.code, 200, response.body)

        target_ds_name = "target_ds"
        params = {"token": token, "datasource": target_ds_name}
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}/materialization?{urlencode(params)}", method="POST", body=""
        )

        result = json.loads(response.body)

        self.assertEqual(response.code, 400, response.body)
        self.assertEqual(
            result.get("error"),
            "There was an error (DB::Exception: StorageMaterializedView cannot be created "
            "from table functions (numbers(1000))) when getting the Data Source form the "
            "query. Please, check you are using a valid Data Source",
        )
        self.assertIsNotNone(result.get("documentation"))


class TestAPIOpenAPI(BaseTest):
    def tearDown(self):
        super().tearDown()

    def test_endpoints_by_token(self):
        self.create_test_datasource()
        u = Users.get_by_id(self.WORKSPACE_ID)
        admin_token = Users.get_token_for_scope(u, scopes.ADMIN)

        pipe_1 = Users.add_pipe_sync(
            u,
            "pipe_endpoint_1",
            "select *, toDateTime('2020-01-01 00:00:00') as datetime, toDate(datetime) as date, [1, 2, 3] arr, [(2, 3)] as arr_tup from test_table where c = 'one'",
        )
        pipe_1.endpoint = pipe_1.pipeline.nodes[0].name
        pipe_2 = Users.add_pipe_sync(u, "pipe_endpoint_2", "select * from test_table where c = 'two'")
        pipe_2.endpoint = pipe_2.pipeline.nodes[0].name
        pipe_3 = Users.add_pipe_sync(u, "pipe_endpoint_3", "select * from test_table where c = 'three'")
        pipe_3.endpoint = pipe_3.pipeline.nodes[0].name

        Users.update_pipe(u, pipe_1)
        Users.update_pipe(u, pipe_2)
        Users.update_pipe(u, pipe_3)

        pipes_scopes = (
            "scope=PIPES:READ:pipe_endpoint_1&scope=PIPES:READ:pipe_endpoint_2&scope=PIPES:READ:pipe_endpoint_3"
        )
        response = self.fetch(
            f"/v0/tokens?token={admin_token}&name=endpoints_token&{pipes_scopes}", method="POST", body=""
        )
        self.assertEqual(response.code, 200)

        response = self.fetch(f"/v0/tokens/endpoints_token?token={admin_token}")
        result = json.loads(response.body)
        token = result["token"]
        self.assertEqual(response.code, 200)

        response = self.fetch(f"/v0/pipes/openapi.json?examples=show&token={token}")
        result = json.loads(response.body)
        self.assertEqual(result["info"]["title"], "endpoints_token")
        self.assertTrue("security" in result)
        self.assertEqual(len(result["paths"]), 3)

        path_1 = result["paths"]["/pipes/pipe_endpoint_1.{format}"]
        example_json = path_1["get"]["responses"]["200"]["content"]["application/json"]["example"]["meta"]

        self.assertEqual(
            example_json,
            [
                {"name": "a", "type": "UInt64"},
                {"name": "b", "type": "Float32"},
                {"name": "c", "type": "String"},
                {"name": "datetime", "type": "DateTime"},
                {"name": "date", "type": "Date"},
                {"name": "arr", "type": "Array(UInt8)"},
                {"name": "arr_tup", "type": "Array(Tuple(UInt8, UInt8))"},
            ],
        )

        data_json = path_1["get"]["responses"]["200"]["content"]["application/json"]["example"]["data"]
        self.assertEqual(
            data_json,
            [
                {
                    "a": 1,
                    "b": 1,
                    "c": "one",
                    "datetime": "2020-01-01 00:00:00",
                    "date": "2020-01-01",
                    "arr": [1, 2, 3],
                    "arr_tup": [[2, 3]],
                }
            ],
        )

        example_csv = path_1["get"]["responses"]["200"]["content"]["text/csv"]["example"]
        self.assertEqual(example_csv, '1,1,"one","2020-01-01 00:00:00","2020-01-01","[1,2,3]","[(2,3)]"\n')

        self.assertEqual(11, len(result["components"]["schemas"].keys()))

        schema = "#/components/schemas/ApiQueryJSONResponse__pipe_endpoint_1"
        self.assertEqual(schema, path_1["get"]["responses"]["200"]["content"]["application/json"]["schema"]["$ref"])

        data_schema = {
            "type": "object",
            "properties": {
                "a": {"type": "integer", "format": "int64"},
                "b": {"type": "number", "format": "float"},
                "c": {"type": "string"},
                "datetime": {"type": "string", "format": "date-time"},
                "date": {"type": "string", "format": "date"},
                "arr": {"type": "array", "items": {"type": "integer", "format": "uint8"}},
                "arr_tup": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {"type": "integer", "format": "uint8"},
                        "minItems": 2,
                        "maxItems": 2,
                    },
                },
            },
        }
        self.assertEqual(data_schema, result["components"]["schemas"]["ApiQueryJSONResponseDataItem__pipe_endpoint_1"])

        query_response = {
            "type": "object",
            "properties": {
                "meta": {"type": "array", "items": {"$ref": "#/components/schemas/ApiQueryJSONResponseMetaItem"}},
                "data": {
                    "type": "array",
                    "items": {"$ref": "#/components/schemas/ApiQueryJSONResponseDataItem__pipe_endpoint_1"},
                },
                "rows": {"type": "number"},
                "rows_before_limit_at_least": {"type": "number"},
                "statistics": {"$ref": "#/components/schemas/ApiQueryJSONResponseStatistics"},
            },
            "required": ["meta", "data", "rows", "statistics"],
        }
        self.assertEqual(query_response, result["components"]["schemas"]["ApiQueryJSONResponse__pipe_endpoint_1"])

    def test_endpoints_examples(self):
        self.create_test_datasource()

        u = Users.get_by_id(self.WORKSPACE_ID)

        pipe = Users.add_pipe_sync(
            u,
            "test_examples",
            """%
            SELECT sum(a) sum_a, count() as count
            FROM test_table
            WHERE
                a = {{UInt64(numeric, 2)}} AND
                b = {{Float32(float_value, 2.3)}} AND
                c = {{String(category, 'one')}}
        """,
        )

        pipe.endpoint = pipe.pipeline.nodes[0].name
        Users.update_pipe(u, pipe)

        pipe_token = Users.add_token(u, "pipe_token", scopes.PIPES_READ, pipe.id)

        response = self.fetch(f"/v0/pipes/openapi.json?examples=hide&token={pipe_token}")
        result = json.loads(response.body)

        path = result["paths"]["/pipes/test_examples.{format}"]
        example_json = path["get"]["responses"]["200"]["content"]["application/json"]["example"]
        example_csv = path["get"]["responses"]["200"]["content"]["text/csv"]["example"]

        self.assertEqual(len(example_json), 0)
        self.assertEqual(len(example_csv), 0)

    def test_endpoints_fake_examples(self):
        self.create_test_datasource()

        u = Users.get_by_id(self.WORKSPACE_ID)

        pipe = Users.add_pipe_sync(
            u,
            "test_fake_examples",
            """%
            SELECT sum(a) sum_a, count() as count
            FROM test_table
            WHERE
                a = {{UInt64(numeric, 2)}} AND
                b = {{Float32(float_value, 2.3)}} AND
                c = {{String(category, 'one')}}
        """,
        )

        pipe.endpoint = pipe.pipeline.nodes[0].name
        Users.update_pipe(u, pipe)

        pipe_token = Users.add_token(u, "pipe_token", scopes.PIPES_READ, pipe.id)

        response = self.fetch(f"/v0/pipes/openapi.json?token={pipe_token}")
        result = json.loads(response.body)

        path = result["paths"]["/pipes/test_fake_examples.{format}"]
        example_json = path["get"]["responses"]["200"]["content"]["application/json"]["example"]
        example_csv = path["get"]["responses"]["200"]["content"]["text/csv"]["example"]

        self.assertNotEqual(len(example_json), 0)
        self.assertEqual(
            example_json["data"],
            [
                {"sum_a": 2804162938822577320, "count": 5935810273536892891},
                {"sum_a": 7885388429666205427, "count": 368066018677693974},
                {"sum_a": 4357435422797280898, "count": 8124171311239967992},
            ],
        )
        self.assertNotEqual(len(example_csv), 0)
        self.assertEqual(
            example_csv,
            "2804162938822577320,5935810273536892891\n7885388429666205427,368066018677693974\n4357435422797280898,8124171311239967992\n",
        )

    def test_endpoints_public(self):
        self.create_test_datasource()
        u = Users.get_by_id(self.WORKSPACE_ID)

        pipe = Users.add_pipe_sync(
            u,
            "test_endpoints_public",
            """%
            SELECT sum(a) sum_a, count() as count
            FROM test_table
            WHERE
                a = {{UInt64(numeric, 2)}} AND
                b = {{Float32(float_value, 2.3)}} AND
                c = {{String(category, 'one')}}
        """,
        )

        pipe.endpoint = pipe.pipeline.nodes[0].name
        Users.update_pipe(u, pipe)

        response = self.fetch("/endpoints?token=blabla")
        assert "HTTP 403: Forbidden" in str(response.error)
        assert response.code == 403

        response = self.fetch("/endpoint/test_endpoints_public?token=blabla")
        assert "HTTP 403: Forbidden" in str(response.error)
        assert response.code == 403

        pipe_token = Users.add_token(u, "pipe_token_test_endpoints_public_wrong", scopes.DATASOURCES_READ, pipe.id)
        response = self.fetch(f"/endpoints?token={pipe_token}")
        assert "HTTP 403: Forbidden" in str(response.error)
        assert response.code == 403

        response = self.fetch(f"/endpoint/test_endpoints_public?token={pipe_token}")
        assert "HTTP 403: Forbidden" in str(response.error)
        assert response.code == 403

        admin_token = Users.get_token_for_scope(u, scopes.ADMIN)
        response = self.fetch(f"/endpoints?token={admin_token}")
        assert response.code == 200

        response = self.fetch(f"/endpoint/test_endpoints_public?token={admin_token}")
        assert response.code == 200

        pipe_token = Users.add_token(u, "pipe_token_test_endpoints_public", scopes.PIPES_READ, pipe.id)
        response = self.fetch(f"/endpoints?token={admin_token}")
        assert response.code == 200

        response = self.fetch(f"/endpoint/test_endpoints_public?token={admin_token}")
        assert response.code == 200

    def test_empty_variables(self):
        self.create_test_datasource()

        u = Users.get_by_id(self.WORKSPACE_ID)
        pipe = Users.add_pipe_sync(
            u,
            "test_parameter",
            """%
            {% set _i = 2 %}
            SELECT sum(a) sum_a, count() as count
            FROM test_table
            WHERE
                a = {{_i}} AND
                b = {{Float32(float_value, 2.3)}} AND
                c = {{String(category, 'one')}}
        """,
        )

        pipe.endpoint = pipe.pipeline.nodes[0].name
        Users.update_pipe(u, pipe)

        pipe_token = Users.add_token(u, "pipe_token", scopes.PIPES_READ, pipe.id)

        response = self.fetch(f"/v0/pipes/openapi.json?token={pipe_token}")
        result = json.loads(response.body)

        path = result["paths"]["/pipes/test_parameter.{format}"]
        self.assertEqual(len(path["get"]["parameters"]), 4)

    def test_endpoints_parameters(self):
        self.create_test_datasource()

        u = Users.get_by_id(self.WORKSPACE_ID)

        pipe = Users.add_pipe_sync(
            u,
            "test_parameter",
            """%
            SELECT sum(a) sum_a, count() as count
            FROM test_table
            WHERE
                a = {{UInt64(numeric, 2, description="this is a numeric parameter", example="1", format="number")}} AND
                b = {{Float32(float_value, 2.3, enum=["1.1", "2.3", "3.2"])}} AND
                c = {{String(category, 'one', required=True)}} AND
                c IN {{Array(categories, String, 'one,two', required=True)}} AND
                C IN {{Array(categories_enum, String, '', enum=["one", "two", "three"])}}
                {% if defined(categories_n) %} AND c IN {{Array(categories_n, 'String')}} {% end %}
        """,
        )

        pipe.endpoint = pipe.pipeline.nodes[0].name
        Users.update_pipe(u, pipe)

        pipe_token = Users.add_token(u, "pipe_token", scopes.PIPES_READ, pipe.id)

        response = self.fetch(f"/v0/pipes/openapi.json?token={pipe_token}")
        result = json.loads(response.body)

        path = result["paths"]["/pipes/test_parameter.{format}"]
        expected_params = [
            {
                "in": "query",
                "name": "categories",
                "description": "",
                "required": True,
                "example": None,
                "schema": {"type": "array", "default": "one,two", "items": {"type": "string"}},
            },
            {
                "in": "query",
                "name": "categories_enum",
                "description": "",
                "required": False,
                "example": None,
                "schema": {
                    "type": "array",
                    "items": {"type": "string", "enum": ["one", "two", "three"]},
                },
            },
            {
                "in": "query",
                "name": "categories_n",
                "description": "",
                "required": False,
                "example": None,
                "schema": {"type": "array", "items": {"type": "string"}},
            },
            {
                "in": "query",
                "name": "category",
                "description": "",
                "required": True,
                "example": None,
                "schema": {
                    "type": "string",
                    "default": "one",
                },
            },
            {
                "in": "query",
                "name": "float_value",
                "description": "",
                "required": False,
                "example": None,
                "schema": {"type": "number", "format": "float", "default": 2.3, "enum": ["1.1", "2.3", "3.2"]},
            },
            {
                "in": "query",
                "name": "numeric",
                "description": "this is a numeric parameter",
                "required": False,
                "example": "1",
                "schema": {"type": "integer", "default": 2, "format": "number"},
            },
            {
                "name": "format",
                "required": True,
                "in": "path",
                "description": "Response format: `json` or `csv`",
                "schema": {"type": "string", "default": "json", "enum": ["json", "csv"]},
            },
            {
                "name": "q",
                "required": False,
                "in": "query",
                "description": "SQL statement to run a query against the data returned by the endpoint (e.g SELECT count() FROM _)",
                "schema": {"type": "string"},
            },
        ]

        self.assertEqual(len(path["get"]["parameters"]), len(expected_params))

        for p in expected_params:
            self.assertIn(p, path["get"]["parameters"])

    def test_endpoints_post_parameters(self):
        self.create_test_datasource()

        u = Users.get_by_id(self.WORKSPACE_ID)

        pipe = Users.add_pipe_sync(
            u,
            "test_parameter",
            """%
            SELECT sum(a) sum_a, count() as count
            FROM test_table
            WHERE
                a = {{UInt64(numeric, 2, description="this is a numeric parameter", example="1", format="number")}} AND
                b = {{Float32(float_value, 2.3, enum=["1.1", "2.3", "3.2"])}} AND
                c = {{String(category, 'one', required=True)}} AND
                c IN {{Array(categories, String, 'one,two', required=True)}}
                {% if defined(categories_n) %} AND c IN {{Array(categories_n, 'String')}} {% end %}
        """,
        )

        pipe.endpoint = pipe.pipeline.nodes[0].name
        Users.update_pipe(u, pipe)

        pipe_token = Users.add_token(u, "pipe_token", scopes.PIPES_READ, pipe.id)

        response = self.fetch(f"/v0/pipes/openapi.json?token={pipe_token}")
        result = json.loads(response.body)

        content_schema = {
            "schema": {
                "type": "object",
                "properties": {
                    "categories": {
                        "type": "array",
                        "default": "one,two",
                        "items": {"type": "string"},
                        "description": "",
                    },
                    "category": {"type": "string", "default": "one", "description": ""},
                    "categories_n": {"type": "array", "items": {"type": "string"}, "description": ""},
                    "float_value": {
                        "type": "number",
                        "format": "float",
                        "enum": ["1.1", "2.3", "3.2"],
                        "default": 2.3,
                        "description": "",
                    },
                    "numeric": {
                        "type": "integer",
                        "format": "number",
                        "default": 2,
                        "description": "this is a numeric parameter",
                    },
                },
                "required": ["categories", "category"],
            }
        }
        path = result["paths"]["/pipes/test_parameter.{format}"]
        expected_request_body = {
            "content": {"application/json": content_schema, "application/x-www-form-urlencoded": content_schema}
        }

        self.assertEqual(expected_request_body, path["post"]["requestBody"])

    def test_endpoints_parameters_dependecy_graph(self):
        self.create_test_datasource()

        u = Users.get_by_id(self.WORKSPACE_ID)

        pipe = Users.add_pipe_sync(
            u,
            "test_parameter",
            """%
            SELECT sum(a) sum_a, count() as c
            FROM test_table
            WHERE
                a = {{UInt64(good_parameter, 2)}}
        """,
        )

        pipe.append_node(
            PipeNode(
                "node_test_another_parameter",
                """%
            SELECT c
            FROM test_parameter_0
            WHERE
                c > {{UInt64(another_good_parameter, 3)}}
        """,
            )
        )

        pipe.append_node(
            PipeNode(
                "node_test_bad_parameter",
                """%
            SELECT sum(a) sum_a, count() as count
            FROM test_table
            WHERE
                a = {{UInt64(bad_parameter, 2)}}
        """,
            )
        )

        pipe.endpoint = pipe.pipeline.nodes[1].name
        Users.update_pipe(u, pipe)
        pipe_token = Users.add_token(u, "pipe_token", scopes.PIPES_READ, pipe.id)

        response = self.fetch(f"/v0/pipes/openapi.json?token={pipe_token}")
        result = json.loads(response.body)

        path = result["paths"]["/pipes/test_parameter.{format}"]
        expected_params = [
            {
                "in": "query",
                "name": "another_good_parameter",
                "description": "",
                "required": False,
                "example": None,
                "schema": {"type": "integer", "format": "int64", "default": 3},
            },
            {
                "in": "query",
                "name": "good_parameter",
                "description": "",
                "required": False,
                "example": None,
                "schema": {"type": "integer", "format": "int64", "default": 2},
            },
            {
                "name": "format",
                "required": True,
                "in": "path",
                "description": "Response format: `json` or `csv`",
                "schema": {"type": "string", "default": "json", "enum": ["json", "csv"]},
            },
            {
                "name": "q",
                "required": False,
                "in": "query",
                "description": "SQL statement to run a query against the data returned by the endpoint (e.g SELECT count() FROM _)",
                "schema": {"type": "string"},
            },
        ]

        self.assertEqual(len(path["get"]["parameters"]), len(expected_params))
        for p in expected_params:
            self.assertIn(p, path["get"]["parameters"])

    def test_endpoint_conditional_selects(self):
        self.create_test_datasource()

        u = Users.get_by_id(self.WORKSPACE_ID)

        pipe = Users.add_pipe_sync(
            u,
            "test_conditional_selects",
            """%
            {% if defined(my_param_1) %} SELECT 'my_field' as field_1
            {% elif defined(my_param_2) %}
                SELECT
                    'my_field' as field_2
                    {% if defined(my_param_3) %}, 'my_field' as field_4
                    {% end %}
            {% else %} SELECT 'my_field' as field_3
            {% end %}
        """,
        )

        pipe.endpoint = pipe.pipeline.nodes[0].name
        Users.update_pipe(u, pipe)

        pipe_token = Users.add_token(u, "pipe_token", scopes.PIPES_READ, pipe.id)

        response = self.fetch(f"/v0/pipes/openapi.json?token={pipe_token}&optional_fields=true")
        result = json.loads(response.body)

        properties = result["components"]["schemas"][f"ApiQueryJSONOptionalResponseDataItem__{pipe.name}"]["properties"]
        expected_properties = {
            "field_1": {"type": "string"},
            "field_2": {"type": "string"},
            "field_3": {"type": "string"},
        }
        self.assertEqual(properties, expected_properties)


class TestAPIPipesSyncPG(BaseTest):
    def setUp(self):
        super().setUp()
        self.create_test_datasource()
        self.u = Users.get_by_id(self.WORKSPACE_ID)
        self.u["enabled_pg"] = True
        self.u["pg_server"] = "127.0.0.1"
        self.u["pg_foreign_server"] = CH_HOST
        self.u["pg_foreign_server_port"] = CH_HTTP_PORT
        self.u.save()
        self.pg_service = PGService(self.u)
        self.pg_service.drop_database()
        self.pg_service.setup_database()
        self.pipe_name = "test_pipe"

    def tearDown(self):
        self.u["enabled_pg"] = True
        self.pg_service.drop_database()
        self.u["enabled_pg"] = False
        self._drop_token()
        super().tearDown()

    def _drop_token(self):
        try:
            u = Users.get_by_id(self.WORKSPACE_ID)
            token = Users.get_token(u, "test")
            if token:
                Users.drop_token(u, token)
        except Exception:
            pass

    async def __make_endpoint(self, pipe_name, pipe_node, expected_code=200):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        node_id = pipe_node.id if not isinstance(pipe_node, dict) else pipe_node["id"]

        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{node_id}/endpoint?token={token}",
            method="POST",
            body=b"",
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, expected_code)

    async def __append_node(self, sql, name=None, description=None, expected_code=200):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        url_parts = ["/v0/pipes/test_pipe/nodes?token=%s" % token]
        if name:
            url_parts += [f"name={name}"]
        if description:
            url_parts += [f"description={description}"]
        url = "&".join(url_parts)
        response = await self.fetch_async(url, method="POST", body=sql)
        self.assertEqual(response.code, expected_code)
        return json.loads(response.body)

    @tornado.testing.gen_test
    async def test_on_publish_endpoint(self):
        u = self.u
        pipe_name = self.pipe_name
        node = Users.get_pipe(u, pipe_name).pipeline.nodes[0]
        await self.__make_endpoint(pipe_name, node)

        sql = f"SELECT * FROM pg_views WHERE viewname = '{pipe_name}' AND schemaname = 'public';"
        res = PGService(self.u).execute(sql, role="user")
        self.assertEqual(len(res), 1)

        sql = f"SELECT count(*) FROM {pipe_name};"
        res = PGService(self.u).execute(sql, role="user")
        self.assertEqual(res[0]["count"], 6)

    @tornado.testing.gen_test
    async def test_append_node(self):
        pipe_name = self.pipe_name
        count_rows = 3
        pipe_node = await self.__append_node(f"select * from test_pipe_0 limit {count_rows}")
        await self.__make_endpoint(pipe_name, pipe_node)

        sql = f"SELECT * FROM pg_views WHERE viewname = '{pipe_name}' AND schemaname = 'public';"
        res = PGService(self.u).execute(sql, role="user")
        self.assertEqual(len(res), 1)

        sql = f"SELECT count(*) FROM {pipe_name};"
        res = PGService(self.u).execute(sql, role="user")
        self.assertEqual(res[0]["count"], count_rows)

    @tornado.testing.gen_test
    async def test_edit_node(self):
        u = self.u
        pipe_name = self.pipe_name

        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)
        response = await self.fetch_async(
            "/v0/pipes/test_pipe/nodes?token=%s" % token, method="POST", body="select * from test_pipe_0 where a > 4"
        )
        node = json.loads(response.body)
        await self.__make_endpoint(pipe_name, node)

        sql = f"SELECT * FROM pg_views WHERE viewname = '{pipe_name}' AND schemaname = 'public';"
        res = PGService(self.u).execute(sql, role="user")
        self.assertEqual(len(res), 1)

        sql = f"SELECT count(*) FROM {pipe_name};"
        res = PGService(self.u).execute(sql, role="user")
        self.assertEqual(res[0]["count"], 1)

        response = await self.fetch_async(
            f"/v0/pipes/test_pipe/nodes/{node['id']}?token={token}",
            method="PUT",
            body="select * from test_pipe_0 where a > 1",
        )
        payload = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(payload["name"], "test_pipe_1")

        sql = f"SELECT count(*) FROM {pipe_name};"
        res = PGService(self.u).execute(sql, role="user")
        self.assertEqual(res[0]["count"], 4)

    @tornado.testing.gen_test
    async def test_unpublish_endpoint(self):
        u = self.u
        pipe_name = self.pipe_name
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)

        # Endpoint not defined by default
        pipe_res = json.loads((await self.fetch_async(f"/v0/pipes/{pipe_name}?token={token}")).body)
        self.assertIsNone(pipe_res["endpoint"])

        sql = f"SELECT * FROM pg_views WHERE viewname = '{pipe_name}' AND schemaname = 'public';"
        res = PGService(self.u).execute(sql, role="user")
        self.assertEqual(len(res), 0)

        # Enable endpoint
        await self.__make_endpoint(pipe_name, pipe_res["nodes"][0])
        pipe_res = json.loads((await self.fetch_async(f"/v0/pipes/{pipe_name}?token={token}")).body)
        self.assertEqual(pipe_res["endpoint"], pipe_res["nodes"][0]["id"])

        sql = f"SELECT * FROM pg_views WHERE viewname = '{pipe_name}' AND schemaname = 'public';"
        res = PGService(self.u).execute(sql, role="user")
        self.assertEqual(len(res), 1)

        sql = f"SELECT count(*) FROM {pipe_name};"
        res = PGService(self.u).execute(sql, role="user")
        self.assertEqual(res[0]["count"], 6)

        # Drop endpoint
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{pipe_res['nodes'][0]['id']}/endpoint?token={token}", method="DELETE"
        )
        self.assertEqual(response.code, 200)
        pipe_res = json.loads((await self.fetch_async(f"/v0/pipes/{pipe_name}?token={token}")).body)
        self.assertIsNone(pipe_res["endpoint"])

        sql = f"SELECT * FROM pg_views WHERE viewname = '{pipe_name}' AND schemaname = 'public';"
        res = PGService(self.u).execute(sql, role="user")
        self.assertEqual(len(res), 0)

    @tornado.testing.gen_test
    async def test_pipe_change_name(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.PIPES_CREATE)
        old_id = Users.get_pipe(u, "test_pipe").id
        response = await self.fetch_async("/v0/pipes/test_pipe?name=new_name&token=%s" % token, method="PUT", body="")
        self.assertEqual(response.code, 200)
        body = json.loads(response.body)
        self.assertEqual(body["name"], "new_name")
        self.assertEqual(body["id"], old_id)

        u = self.u
        pipe_name = self.pipe_name
        new_name = "new_name"

        node = Users.get_pipe(u, new_name).pipeline.nodes[0]
        await self.__make_endpoint(new_name, node)

        sql = f"SELECT * FROM pg_views WHERE viewname = '{pipe_name}' AND schemaname = 'public';"
        res = PGService(self.u).execute(sql, role="user")
        self.assertEqual(len(res), 0)

        sql = f"SELECT * FROM pg_views WHERE viewname = '{new_name}' AND schemaname = 'public';"
        res = PGService(self.u).execute(sql, role="user")
        self.assertEqual(len(res), 1)

        sql = f"SELECT count(*) FROM {new_name};"
        res = PGService(self.u).execute(sql, role="user")
        self.assertEqual(res[0]["count"], 6)

    @tornado.testing.gen_test
    async def test_pipe_drop(self):
        u = self.u
        pipe_name = self.pipe_name
        node = Users.get_pipe(u, pipe_name).pipeline.nodes[0]
        await self.__make_endpoint(pipe_name, node)

        sql = f"SELECT * FROM pg_views WHERE viewname = '{pipe_name}' AND schemaname = 'public';"
        res = PGService(self.u).execute(sql, role="user")
        self.assertEqual(len(res), 1)

        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN, self.USER_ID)
        response = await self.fetch_async("/v0/pipes/test_pipe?token=%s" % token, method="DELETE")
        self.assertEqual(response.code, 204)
        self.assertIsNone(Users.get_pipe(u, "test_pipe"))

        sql = f"SELECT * FROM pg_views WHERE viewname = '{pipe_name}' AND schemaname = 'public';"
        res = PGService(self.u).execute(sql, role="user")
        self.assertEqual(len(res), 0)


class TestAPIPipesMaterializedViewsHandler(TestAPIPipeStats):
    def setUp(self):
        self.mpatch = MonkeyPatch()
        super().setUp()
        self.original_get_by_cluster = ClusterSettings.get_by_cluster

    def tearDown(self):
        self._drop_token()
        self.mpatch.undo()
        super().tearDown()

    def _drop_token(self):
        try:
            u = Users.get_by_id(self.WORKSPACE_ID)
            token = Users.get_token(u, "test")
            if token:
                Users.drop_token(u, token)
        except Exception:
            pass

    async def _unset_cluster_replicas(self, cluster: ClusterSettings) -> None:
        await ClusterSettings.delete_replicas(cluster, ClusterSettingsOperations.POPULATE)
        await ClusterSettings.delete_replicas(cluster, ClusterSettingsOperations.POOL)

    async def _set_cluster_replicas(self, workspace: User) -> ClusterSettings:
        cluster_settings = await ClusterSettings.add_cluster(workspace.id, ClusterSettingsOperations.POPULATE)
        cluster_settings = await ClusterSettings.update_replica(
            cluster_settings,
            ClusterSettingsOperations.POPULATE,
            "clickhouse-01:8123",
            1,
        )
        cluster_settings = await ClusterSettings.add_operation(cluster_settings, ClusterSettingsOperations.POOL)
        cluster_settings = await ClusterSettings.update_replica(
            cluster_settings,
            ClusterSettingsOperations.POOL,
            CI_JOBS_REPLICA,
            1,
        )
        cluster_settings = await set_dynamic_disk_settings(cluster_settings)
        patcher = patch(
            "tinybird.populates.cluster.ClusterSettings.get_by_cluster",
            side_effect=lambda cluster: self.original_get_by_cluster(workspace.id),
        )
        patcher.start()
        self.addCleanup(patcher.stop)
        ch_pool_cluster_patcher = patch(
            "tinybird.populates.cluster.get_pool_cluster",
            side_effect=lambda: self.original_get_by_cluster(workspace.id),
        )
        ch_pool_cluster_patcher.start()
        self.addCleanup(ch_pool_cluster_patcher.stop)
        self.assertEquals(
            cluster_settings.settings[ClusterSettingsOperations.POOL]["replicas"][CI_JOBS_REPLICA],
            1,
        )
        pool_replica = get_pool_replicas()
        self.assertEquals(pool_replica, [CI_JOBS_REPLICA])

        pool_cluster_name_patcher = patch(
            "tinybird.populates.job.get_pool_cluster_name",
            return_value=CI_JOBS_CLUSTER_NAME,
        )
        pool_cluster_name_patcher.start()
        self.addCleanup(pool_cluster_name_patcher.stop)
        return cluster_settings

    def test_materialize_from_node_fails_if_sql_is_a_template(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_happy_case"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # let's create a datasource
        ds_name = "ds_for_view_engine"
        params = {
            "token": token,
            "name": ds_name,
            "schema": "a UInt64",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        node_name = "mat_view_node"

        # create a pipe's node with a template
        params = {"token": token, "name": node_name}
        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}",
            method="POST",
            body=f"% select a * 2 as b, a * 3 as c from {ds_name}",
        )
        self.assertEqual(response.code, 200)

        # materialize view
        target_ds_name = "mat_view_node_ds"
        params = {"token": token, "datasource": target_ds_name, "engine": "MergeTree", "engine_sorting_key": "tuple()"}
        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}/materialization?{urlencode(params)}", method="POST", body=""
        )
        result = json.loads(response.body)

        self.assertEqual(response.code, 400, response.body)
        self.assertEqual(
            result.get("error"),
            "Materialized nodes don't support templates. Please remove any `{% ... %}` template code or the `%` mark from this pipe node.",
        )
        self.assertIsNotNone(result.get("documentation"))

    def test_materialize_from_node_targeting_a_non_existing_datasource_requires_token_with_datasource_create(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_happy_case"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # let's create a datasource
        ds_name = "ds_for_view_engine"
        params = {
            "token": Users.get_token_for_scope(u, scopes.ADMIN),
            "name": ds_name,
            "schema": "a UInt64",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        # create a pipe's node with a view to that datasource
        node_name = "mat_view_node"
        params = {"token": token, "name": node_name}
        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}",
            method="POST",
            body=f"select a * 2 as b, a * 3 as c from {ds_name}",
        )
        self.assertEqual(response.code, 200)

        # Create token with just PIPES_CREATE scope
        token = Users.add_token(u, "pipe_with_materialized_node", scopes.PIPES_CREATE)

        # materialize view
        target_ds_name = "mat_view_node_ds"
        params = {
            "token": token,
            "datasource": target_ds_name,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
        }
        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}/materialization?{urlencode(params)}", method="POST", body=""
        )
        result = json.loads(response.body)

        self.assertEqual(response.code, 403)
        self.assertEqual(
            result.get("error"),
            "Forbidden. Provided token doesn't have permissions to create the datasource "
            "required in the materialized node, it also needs ``ADMIN`` or "
            "``DATASOURCES:CREATE`` scope.",
        )
        self.assertIsNotNone(result.get("documentation"))

    @tornado.testing.gen_test
    async def test_materialize_from_node_view_creation_engine_happy_case(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_happy_case"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # let's create a datasource
        ds_name = "ds_for_view_engine"
        params = {
            "token": token,
            "name": ds_name,
            "schema": "a UInt64",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        # create a pipe's node
        node_name = "mat_view_node"
        params = {"token": token, "name": node_name}
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}",
            method="POST",
            body=f"select a * 2 as b, a * 3 as c from {ds_name}",
        )
        pipe_node = json.loads(response.body)

        # materialize view
        target_ds_name = "mat_view_node_ds"
        params = {
            "token": token,
            "datasource": target_ds_name,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
        }
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}/materialization?{urlencode(params)}", method="POST", body=""
        )
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(pipe_node["name"], node_name)
        ds = Users.get_datasource(u, target_ds_name)
        self.assertEqual(pipe_node["materialized"], ds.id)
        self.assertEqual(pipe_node["cluster"], pipe_node["cluster"])

        # validate the view is there and returns correct schema
        async def assert_datasource():
            expected_schema = [{"name": "b", "type": "UInt64"}, {"name": "c", "type": "UInt64"}]
            params = {
                "token": token,
                "q": f"SELECT * FROM {target_ds_name} FORMAT JSON",
            }
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            self.assertEqual(response.code, 200)
            payload = json.loads(response.body)
            self.assertEqual(payload["meta"], expected_schema)
            self.assertEqual(payload["data"], [])

        await poll_async(assert_datasource)

        # add some data to the original datasource
        data = [1, 2, 3]
        params = {
            "token": token,
            "name": ds_name,
            "mode": "append",
        }
        response = await self.fetch_async(
            f"/v0/datasources?{urlencode(params)}", method="POST", body="\n".join([str(d) for d in data])
        )

        # validate the view is there and returns new data
        async def assert_datasource():
            params = {
                "token": token,
                "q": f"SELECT * FROM {target_ds_name} FORMAT JSON",
            }
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            self.assertEqual(response.code, 200)
            payload = json.loads(response.body)
            self.assertEqual(payload["data"], [{"b": d * 2, "c": d * 3} for d in data])

        await poll_async(assert_datasource)

        # add extra node using the previous node
        params = {
            "token": token,
            "name": "read_from_mat_view",
        }
        query = "select * from mat_view_node"
        response = await self.fetch_async(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)

    @tornado.testing.gen_test
    async def test_materialize_from_node_sending_new_sql_happy_case(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_happy_case"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # let's create a datasource
        ds_name = "ds_for_view_engine"
        params = {
            "token": token,
            "name": ds_name,
            "schema": "a UInt64",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        # create a pipe's node
        node_name = "mat_view_node"
        params = {"token": token, "name": node_name}
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}",
            method="POST",
            body=f"select a * 2 as b, a * 3 as c from {ds_name}",
        )
        self.assertEqual(response.code, 200)
        pipe_node = json.loads(response.body)

        # materialize view
        target_ds_name = "mat_view_node_ds"
        params = {
            "token": token,
            "datasource": target_ds_name,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
        }

        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}/materialization?{urlencode(params)}",
            method="POST",
            body=f"select a * 2 as d, a * 3 as e from {ds_name}",
        )
        self.assertEqual(response.code, 200)
        ds = Users.get_datasource(u, target_ds_name)

        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(pipe_node["name"], node_name)
        self.assertEqual(pipe_node["materialized"], ds.id)
        self.assertEqual(pipe_node["cluster"], pipe_node["cluster"])

        async def assert_datasource():
            params = {
                "token": token,
                "q": f"SELECT * FROM {target_ds_name} ORDER BY d FORMAT JSON",
            }

            # validate the view is there
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            self.assertEqual(response.code, 200)

            payload = json.loads(response.body)

            # validate the view returns correct schema
            expected_schema = [{"name": "d", "type": "UInt64"}, {"name": "e", "type": "UInt64"}]
            self.assertEqual(payload["meta"], expected_schema)

        await poll_async(assert_datasource)

        # add some data to the original datasource
        data = [1, 2, 3]
        params = {
            "token": token,
            "name": ds_name,
            "mode": "append",
        }
        response = await self.fetch_async(
            f"/v0/datasources?{urlencode(params)}", method="POST", body="\n".join([str(d) for d in data])
        )
        self.assertEqual(response.code, 200, response)

        # validate the view is there and returns new data
        async def assert_datasource():
            params = {
                "token": token,
                "q": f"SELECT * FROM {target_ds_name} ORDER BY d FORMAT JSON",
            }
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            self.assertEqual(response.code, 200)

            payload = json.loads(response.body)

            self.assertEqual(payload["data"], [{"d": d * 2, "e": d * 3} for d in data])

        await poll_async(assert_datasource)
        # add extra node using the previous node
        params = {
            "token": token,
            "name": "read_from_mat_view",
        }
        query = "select * from mat_view_node"
        response = await self.fetch_async(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)

    @tornado.testing.gen_test
    async def test_materialize_from_node_populate_engine_happy_case(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_happy_case_populate"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # let's create a datasource with some data
        ds_name_source = "ds_for_view_engine_source_populate"
        params = {
            "token": token,
            "name": ds_name_source,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        s = StringIO("d,sales\n2019-01-01,2\n2019-01-02,3")
        response = await self.fetch_full_body_upload_async(create_url, s)
        self.assertEqual(response.code, 200, response.body)
        parsed_response = json.loads(response.body)
        origin_datasource_id = parsed_response.get("datasource").get("id")

        self.wait_for_datasource_replication(u, ds_name_source)
        # create a pipe
        node_name = "mat_view_node"
        params = {"token": token, "name": node_name}
        query = f"SELECT toDate(d) AS d, sales * 10 AS fake_sales FROM {ds_name_source}"
        response = await self.fetch_async(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(pipe_node["name"], node_name)

        # materialize with populate
        target_ds_name = "mat_view_node_ds"

        params = {
            "token": token,
            "datasource": target_ds_name,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
            "populate": "true",
        }

        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}/materialization?{urlencode(params)}", method="POST", body=""
        )
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)

        destination_datasource = Users.get_datasource(u, target_ds_name)
        self.assertEqual(pipe_node["materialized"], destination_datasource.id)
        self.assertIn("job", pipe_node)
        job_response = pipe_node["job"]
        self.assertEqual(job_response["id"], job_response["job_id"])
        self.assertEqual(job_response["kind"], JobKind.POPULATE)

        # validate the view is there and returns correct schema and data

        job = await self.get_finalised_job_async(job_response["id"])
        self.assertEqual(job.status, "done", job.get("error", None))
        expected_schema = [{"name": "d", "type": "Date"}, {"name": "fake_sales", "type": "Int32"}]
        initial_data = [{"d": "2019-01-01", "fake_sales": 20}, {"d": "2019-01-02", "fake_sales": 30}]

        async def assert_datasource():
            params = {
                "token": token,
                "q": f"SELECT * FROM {target_ds_name} ORDER BY d FORMAT JSON",
            }
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            self.assertEqual(response.code, 200)
            payload = json.loads(response.body)
            self.assertEqual(payload["meta"], expected_schema)
            self.assertEqual(payload["data"], initial_data)

            # Assert that the Materialized View between
            # the source table and the first destination
            # table is created in the user's database but
            # not in the auxiliary database is not created
            where_clause = f"""
            query_kind='Create' AND
            query LIKE '%CREATE MATERIALIZED VIEW IF NOT EXISTS %' AND
            query LIKE '%{origin_datasource_id}%' AND
            query LIKE '%{destination_datasource.id}%' AND
            query NOT LIKE '%__populate_%' AND
            query NOT LIKE '%ddl_entry=query-%'
            """
            await self.get_query_logs_by_where_async(where_clause=where_clause)

            where_clause = f"""
            query_kind='Create' AND
            query LIKE '%CREATE MATERIALIZED VIEW IF NOT EXISTS %' AND
            query LIKE '%{origin_datasource_id}%' AND
            query LIKE '%{destination_datasource.id}%' AND
            query LIKE '%__populate_%' AND
            query NOT LIKE '%ddl_entry=query-%'
            """
            await self.get_query_logs_by_where_async(where_clause=where_clause, exists=False)

        await poll_async(assert_datasource)

        # add some data to the original datasource
        params = {
            "token": token,
            "name": ds_name_source,
            "mode": "append",
        }
        response = await self.fetch_async(f"/v0/datasources?{urlencode(params)}", method="POST", body="2019-01-03,10")

        # validate the view is there and returns the existing and the new data
        async def assert_datasource():
            params = {
                "token": token,
                "q": f"SELECT * FROM {target_ds_name} ORDER BY d FORMAT JSON",
            }
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            self.assertEqual(response.code, 200)
            payload = json.loads(response.body)
            self.assertEqual(payload["data"], [*initial_data, {"d": "2019-01-03", "fake_sales": 100}])

            self.expect_ops_log(
                [
                    {"event_type": "create", "datasource_name": ds_name_source},
                    {
                        "event_type": "append",
                        "datasource_name": ds_name_source,
                    },
                    {"event_type": "create", "datasource_name": target_ds_name},
                    {
                        "event_type": "populateview-queued",
                        "datasource_name": target_ds_name,
                        "pipe_name": pipe_name,
                        "result": "ok",
                    },
                    {
                        "event_type": "populateview",
                        "datasource_name": target_ds_name,
                        "result": "ok",
                        "pipe_name": pipe_name,
                        "read_rows": 2,
                        "read_bytes": 8,
                        "written_rows": 2,
                        "written_bytes": 12,
                    },
                    {"event_type": "append", "datasource_name": ds_name_source},
                    {"event_type": "append", "datasource_name": target_ds_name},
                ]
            )

        await poll_async(assert_datasource)

    def test_remove_materialized_view_from_node(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_happy_case"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # let's create a datasource
        ds_name = "ds_for_view_engine"
        params = {
            "token": token,
            "name": ds_name,
            "schema": "a UInt64",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        # create a pipe's node
        node_name = "mat_view_node"
        params = {"token": token, "name": node_name}
        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}",
            method="POST",
            body=f"select a * 2 as b, a * 3 as c from {ds_name}",
        )

        # materialize view
        target_ds_name = "mat_view_node_ds"
        params = {
            "token": token,
            "datasource": target_ds_name,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
        }
        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}/materialization?{urlencode(params)}", method="POST", body=""
        )
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)

        # Refresh Workspace to get updated tags
        u = Users.get_by_id(self.WORKSPACE_ID)
        origin_datasource = Users.get_datasource(u, ds_name)
        destination_datasource = Users.get_datasource(u, target_ds_name)
        self.assertEqual(pipe_node["materialized"], destination_datasource.id)
        self.assertTrue(destination_datasource.id in origin_datasource.tags.get("dependent_datasources", {}))

        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}/materialization?{urlencode(params)}", method="DELETE"
        )
        self.assertEqual(response.code, 204)

        # materialized view is gone
        self._check_table_in_database(u.database, pipe_node["id"], exists=False)
        # Data Source is not gone
        self._check_table_in_database(u.database, destination_datasource.id, exists=True)

        # Refresh Workspace to get updated tags
        u = Users.get_by_id(self.WORKSPACE_ID)
        origin_datasource = Users.get_datasource(u, ds_name)
        pipe = Users.get_pipe(u, pipe_name)
        node = pipe.pipeline.get_node(node_name)
        self.assertEqual(node.materialized, None)
        self.assertTrue(destination_datasource.id not in origin_datasource.tags.get("dependent_datasources", {}))

        target_ds = Users.get_datasource(u, target_ds_name)
        self.assertEqual(target_ds.name, target_ds_name)

    def test_materialize_from_node_with_wrong_dist_columns_skip(self):
        self.create_test_datasource()
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_to"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # let's create a target datasource
        ds_name_target = "ds_for_view_to_target_wrong_columns"
        params = {
            "token": token,
            "name": ds_name_target,
            "schema": "x UInt64, y UInt64",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")

        # create a pipe's node
        node_name = "mat_view_node"
        params = {"token": token, "name": node_name}
        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body="select * from test_table"
        )

        # materialize view
        params = {"token": token, "datasource": ds_name_target}

        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}/materialization?{urlencode(params)}", method="POST", body=""
        )
        result = json.loads(response.body)

        self.assertEqual(response.code, 400)
        self.assertTrue(
            "The pipe has columns ['a', 'b', 'c'] not found in the destination Data Source." in result["error"]
        )

        # If it comes from the UI, we don't show the 'skip' message
        params = {"token": token, "datasource": ds_name_target, "from": "ui"}

        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}/materialization?{urlencode(params)}", method="POST", body=""
        )
        result = json.loads(response.body)

        self.assertEqual(response.code, 400)
        self.assertTrue(
            "Cannot materialize node: The pipe has columns ['a', 'b', 'c'] not found in the destination Data Source."
            in result["error"]
        )

    @mock.patch("tinybird.user.Users.mark_node_as_materializing", return_value={})
    @mock.patch("tinybird.user.Users.unmark_node_as_materializing", return_value={})
    def test_materialize_materializing_checks(self, unmark_node_as_materializing_mock, mark_node_as_materializing_mock):
        self.create_test_datasource()
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_node_checks"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # let's create a target datasource
        ds_name_target = "ds_for_view_to_target_node_checks"
        params = {"token": token, "name": ds_name_target, "schema": "a UInt64, b Float32, c String"}
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")

        # create a pipe's node
        node_name = "node_mat_view_node_checks"
        params = {"token": token, "name": node_name}
        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body="select * from test_table"
        )

        params = {"token": token, "datasource": ds_name_target}

        # materialize view
        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}/materialization?{urlencode(params)}", method="POST", body=""
        )

        self.assertEqual(response.code, 200)
        mark_node_as_materializing_mock.assert_called_once_with(u, pipe_name, node_name, "token: 'admin token'")
        unmark_node_as_materializing_mock.assert_called_once_with(u, pipe_name, node_name, "token: 'admin token'")

        mark_node_as_materializing_mock.reset_mock()
        unmark_node_as_materializing_mock.reset_mock()

        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}/materialization?{urlencode(params)}", method="DELETE"
        )

        self.assertEqual(response.code, 204)

        with mock.patch(
            "tinybird.views.api_pipes.NodeMaterializationBaseHandler.create_materialized_view",
            side_effect=ApiHTTPError(400, "Error"),
        ):
            params = {"token": token, "datasource": ds_name_target}

            # materialize
            response = self.fetch(
                f"/v0/pipes/{pipe_name}/nodes/{node_name}/materialization?{urlencode(params)}", method="POST", body=""
            )

            self.assertEqual(response.code, 400)
            mark_node_as_materializing_mock.assert_called_once_with(u, pipe_name, node_name, "token: 'admin token'")
            unmark_node_as_materializing_mock.assert_called_once_with(u, pipe_name, node_name, "token: 'admin token'")

    def test_materialize_while_it_is_already_materializing(self):
        self.create_test_datasource()
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_to_materializing"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")
        mark_node_as_materializing = async_to_sync(Users.mark_node_as_materializing)

        # let's create a target datasource
        ds_name_target = "ds_for_view_to_target_materializing"
        params = {
            "token": token,
            "name": ds_name_target,
            "schema": "x UInt64, y UInt64",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")

        # create a pipe's node
        node_name = "mat_view_node_materializing"
        params = {"token": token, "name": node_name}
        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body="select * from test_table"
        )

        mark_node_as_materializing(u, pipe_name, node_name, "")

        params = {"token": token, "datasource": ds_name_target}

        # materialize
        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}/materialization?{urlencode(params)}", method="POST", body=""
        )

        result = json.loads(response.body)

        self.assertEqual(response.code, 400)
        self.assertEqual(result["error"], f"Node {node_name} is already being materialized")

    @mock.patch("tinybird.ch._create_materialized_view_query", return_value=None)
    @mock.patch(
        "tinybird.views.api_pipes.NodeMaterializationBaseHandler._drop_created_data_source_on_failed_materialization",
        return_value=None,
    )
    @mock.patch("tinybird.ch.ch_drop_table", return_value=True)
    def test_materialize_no_orphan_matview(self, mock_drop_table, mock_drop_datasource, mock_create_matview):
        self.create_test_datasource()
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_materialize_no_orphan_matview"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        ds_name_target = f"ds_{pipe_name}"

        node_name = f"node_{pipe_name}"
        params = {"token": token, "name": node_name}
        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body="select * from test_table"
        )

        params = {"token": token, "datasource": ds_name_target}

        response = self.fetch(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}/materialization?{urlencode(params)}", method="POST", body=""
        )

        mock_create_matview.assert_called_once_with(
            u["database"],
            mock.ANY,
            mock.ANY,
            target_table=mock.ANY,
            target_database=mock.ANY,
            engine=None,
            cluster="tinybird",
            if_not_exists=False,
        )
        mock_drop_table.assert_called_once_with(
            u["database_server"],
            u["database"],
            mock.ANY,
            cluster="tinybird",
            **u.ddl_parameters(skip_replica_down=True),
        )
        mock_drop_datasource.assert_called_once_with(mock.ANY, mock.ANY)

        self.assertEqual(response.code, 500)

    @tornado.testing.gen_test
    async def test_materialize_error_using_service_data_sources(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_mat_view_service_data_sources"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        target_ds_name = "mat_view_node_ds"
        node_name = "mat_view_node"
        params = {"token": token, "name": node_name, "datasource": target_ds_name, "type": "materialized"}
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}",
            method="POST",
            body="select * from tinybird.datasources_ops_log where datasource_id = '1234'",
        )

        result = json.loads(response.body)
        self.assertEqual(response.code, 403)
        self.assertTrue('This query uses Service Data Sources: "tinybird.datasources_ops_log"' in result["error"])
        self.assertIsNotNone(result.get("documentation"))

    async def _test_materialize_populate_when_table_to_truncate_is_too_big_base(self, suffix="base"):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = f"test_materialize_populate_truncate_too_big_{suffix}"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # let's create a datasource with some data
        ds_name_source = f"ds_for_view_engine_source_populate_{suffix}"
        params = {
            "token": token,
            "name": ds_name_source,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        s = StringIO("d,sales\n2019-01-01,2\n2019-01-02,3")
        response = await self.fetch_full_body_upload_async(create_url, s)
        self.assertEqual(response.code, 200, response.body)

        # create a pipe
        node_name = "mat_view_node"
        params = {"token": token, "name": node_name}
        query = f"SELECT toDate(d) AS d, sales * 10 AS fake_sales FROM {ds_name_source}"
        response = await self.fetch_async(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(pipe_node["name"], node_name)

        # materialize with populate
        target_ds_name = f"mat_view_node_ds_{suffix}"

        params = {
            "token": token,
            "datasource": target_ds_name,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
        }

        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}/materialization?{urlencode(params)}", method="POST", body=""
        )
        pipe_node = json.loads(response.body)

        params = {"token": token, "truncate": True, "populate_condition": "sales = 2"}

        ch_exception = CHException(
            "Code: 359, e.displayText = DB::Exception: Table or Partition in table_name was not dropped."
        )
        with mock.patch("tinybird.ch.ch_truncate_table", side_effect=ch_exception):
            response = await self.fetch_async(
                f"/v0/pipes/{pipe_name}/nodes/{node_name}/population?{urlencode(params)}", method="POST", body=""
            )

        population_response = json.loads(response.body)
        job_response = population_response["job"]
        job = await self.get_finalised_job_async(job_response["id"])
        self.assertEqual(job.status, "done", job.get("error", None))

        async def assert_datasource():
            params = {"token": token, "q": f"SELECT * FROM {target_ds_name} FORMAT JSON"}
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            target_ds_content = json.loads(response.body)
            self.assertEqual(response.code, 200)
            self.assertEqual(target_ds_content["rows"], 1)
            self.assertEqual(target_ds_content["data"][0], {"d": "2019-01-01", "fake_sales": 20})

        await poll_async(assert_datasource)

    @tornado.testing.gen_test
    async def test_materialize_populate_when_table_to_truncate_is_too_big(self):
        await self._test_materialize_populate_when_table_to_truncate_is_too_big_base()

    @tornado.testing.gen_test
    async def test_populate_job_unlink_error_ends_up_in_datasources_ops_log_having_2_partitions(self, suffix="base"):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = f"test_unlink_on_populate_error_fills_ds_ops_log_{suffix}"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # let's create a datasource with some data
        tb_api_proxy_async = TBApiProxyAsync(self)

        ds_name_source = f"ds_test_on_populate_error_fills_ds_ops_log_{suffix}"
        await tb_api_proxy_async.create_datasource(
            ds_name=ds_name_source,
            token=token,
            schema="day DateTime, sales Int32, guarantee String",
            engine_params={"engine": "MergeTree", "engine_sorting_key": "day", "engine_partition_key": "toYear(day)"},
        )
        await tb_api_proxy_async.append_data_to_datasource(
            token,
            ds_name_source,
            CsvIO(
                "2019-01-01,1,2029-01-01", "2020-01-02,2,invalid"
            ),  # notice how the invalid will cause an issue in mv toDate cast
        )

        # create a pipe
        node_name = "mat_view_node"
        params = {"token": token, "name": node_name}
        query = f"SELECT day AS d, sales * 10 AS fake_sales, toDate(guarantee) as g FROM {ds_name_source}"
        response = await self.fetch_async(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(pipe_node["name"], node_name)

        # materialize with populate and implicit unlink_on_populate_error
        target_ds_name = "mat_view_node_ds"

        params = {
            "token": token,
            "datasource": target_ds_name,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
            "populate": "true",
            "unlink_on_populate_error": "true",
        }

        # force a exception due to wrong content in the 'guarantee' field
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}/materialization?{urlencode(params)}", method="POST", body=""
        )
        self.assertEqual(response.code, 200, response)

        # wait for the populate job to raise the error
        job = await self.get_finalised_job_async(json.loads(response.body)["job"]["job_id"])
        self.assertEqual(job.get("status"), "error", job)
        job_error_content = job.get("error")
        self.assertIn(PopulateJob.UNLINK_ERROR_MESSAGE, job_error_content)

        # the materialized view is unlinked
        response = await self.fetch_async(f"/v0/pipes/{pipe_name}?{urlencode(params)}")
        pipe_response = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(pipe_response["nodes"][-1]["materialized"], None)
        self._check_table_in_database(u.database, pipe_response["nodes"][-1]["id"], exists=False)

        # double check: population fails because the matview was unlinked
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}/population?{urlencode(params)}", method="POST", body=""
        )

        response = json.loads(response.body)
        self.assertEqual(response["error"], "Node 'mat_view_node' is not materialized")
        self.expect_ops_log(
            [
                {"event_type": "create", "datasource_name": ds_name_source},
                {"event_type": "append", "datasource_name": ds_name_source},
                {"event_type": "create", "datasource_name": target_ds_name},
                {
                    "event_type": "populateview-queued",
                    "datasource_name": target_ds_name,
                    "pipe_name": pipe_name,
                    "result": "ok",
                },
                {
                    "event_type": "populateview",
                    "datasource_name": target_ds_name,
                    "result": "error",
                    "error": job_error_content,
                    "pipe_name": pipe_name,
                },
            ]
        )

    @tornado.testing.gen_test
    async def test_unlink_on_populate_error(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_unlink_on_populate_error"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # let's create a datasource with some data
        ds_name_source = "ds_for_view_test_unlink_on_populate_error"
        params = {
            "token": token,
            "name": ds_name_source,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        s = StringIO("d,sales\n2019-01-01,2\n2019-01-02,3")
        response = await self.fetch_full_body_upload_async(create_url, s)
        self.assertEqual(response.code, 200, response.body)

        # create a pipe
        node_name = "mat_view_node"
        params = {"token": token, "name": node_name}
        query = f"SELECT toDate(d) AS d, sales * 10 AS fake_sales FROM {ds_name_source}"
        response = await self.fetch_async(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(pipe_node["name"], node_name)

        # materialize with populate and implicit unlink_on_populate_error
        target_ds_name = "mat_view_node_ds"

        params = {
            "token": token,
            "datasource": target_ds_name,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
        }

        # materialize with success
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}/materialization?{urlencode(params)}", method="POST", body=""
        )
        pipe_node = json.loads(response.body)
        self.assertTrue(pipe_node["materialized"] is not None)

        params = {
            "token": token,
        }

        # populate it
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}/population?{urlencode(params)}", method="POST", body=""
        )
        self.assertEqual(response.code, 200)

        # wait for the populate job
        job = await self.get_finalised_job_async(json.loads(response.body)["job"]["job_id"])
        self.assertEqual(job.get("status"), "done")

        # wait some seconds for the datasources_ops_log tracker
        await asyncio.sleep(3)
        with patch.object(PopulateJob, "mark_as_working", side_effect=Exception("side effect error")):
            # populate again forcing an error
            response = await self.fetch_async(
                f"/v0/pipes/{pipe_name}/nodes/{node_name}/population?{urlencode(params)}", method="POST", body=""
            )
            self.assertEqual(response.code, 200)

            # wait for the populate job
            job = await self.get_finalised_job_async(json.loads(response.body)["job"]["job_id"])
            self.assertEqual(job.get("status"), "error")
            error = "side effect error"
            self.assertEqual(job.get("error"), error)

            # check matview is not unlinked
            response = await self.fetch_async(f"/v0/pipes/{pipe_name}?{urlencode(params)}")
            pipe_response = json.loads(response.body)
            self.assertEqual(response.code, 200)
            self.assertTrue(pipe_response["nodes"][-1]["materialized"] is not None)
            self._check_table_in_database(u.database, pipe_response["nodes"][-1]["id"], exists=True)

            params = {"token": token, "unlink_on_populate_error": "true"}

            # force an error on population with unlink_on_populate_error
            response = await self.fetch_async(
                f"/v0/pipes/{pipe_name}/nodes/{node_name}/population?{urlencode(params)}", method="POST", body=""
            )
            self.assertEqual(response.code, 200)

            # wait for the populate job to raise the error
            job = await self.get_finalised_job_async(json.loads(response.body)["job"]["job_id"])
            error = "side effect error: the Materialized View has been unlinked and it's not materializing data. Fix the issue in the Materialized View and create it again. See https://www.tinybird.co/docs/api-reference/pipe-api.html#post--v0-pipes-(.+)-nodes-(.+)-population to learn how to check the status of the Job"
            self.assertEqual(job.get("error"), error)

            # check the matview is unlinked
            response = await self.fetch_async(f"/v0/pipes/{pipe_name}?{urlencode(params)}")
            pipe_response = json.loads(response.body)
            self.assertEqual(response.code, 200)
            self.assertEqual(pipe_response["nodes"][-1]["materialized"], None)
            self._check_table_in_database(u.database, pipe_response["nodes"][-1]["id"], exists=False)

    @tornado.testing.gen_test
    async def test_materialize_existing_datasource_override(self):
        self.create_test_datasource()
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_materialize_existing_datasource_override"
        datasource_name = "ds_test_materialize_existing_datasource_override"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        # 1. Create pipe
        params = {"token": token, "name": "mv"}

        query = """
            SELECT
                toDateTime(a) AS d,
                toString(a) AS b,
                sumState(toInt32(a)) AS sum_units
            FROM test_table as t
            GROUP BY
                d, b
        """

        response = await self.fetch_async(f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=query)
        self.assertEqual(response.code, 200, response.body)

        # 2. Materialize view from node
        params = {"token": token, "datasource": datasource_name}

        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/mv/materialization?{urlencode(params)}", method="POST", body=b""
        )

        self.assertEqual(response.code, 200, response.body)

        # 3. Unlink materialized view
        params = {"token": token}

        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/mv/materialization?{urlencode(params)}", method="DELETE", body=None
        )

        self.assertEqual(response.code, 204, response.body)

        # 4. Reset node's SQL
        params = {"token": token}

        response = await self.fetch_async(f"/v0/pipes/{pipe_name}/nodes/mv?token={token}", method="PUT", body=query)

        # 5. Materialize again using the existing Data Source
        params = {"token": token, "datasource": datasource_name}

        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/mv/materialization?{urlencode(params)}", method="POST", body=b""
        )

        self.assertEqual(response.code, 200, response.body)

    @patch.object(ClusterPatches, "ENABLED", False)
    async def _populate_revamp_with_shared_datasources(self):
        tb_api_proxy_async = TBApiProxyAsync(self)
        # First Workspace
        first_workspace = Users.get_by_id(self.WORKSPACE_ID)
        cluster = await self._set_cluster_replicas(first_workspace)
        first_workspace_token = Users.get_token_for_scope(first_workspace, scopes.ADMIN)
        test_name = f"populate_revamp_with_shared_datasources_{uuid.uuid4().hex}"

        # Second Workspace
        SECOND_WORKSPACE_NAME = f"second_ws_{test_name}"
        second_workspace = User.register(SECOND_WORKSPACE_NAME, self.USER_ID)
        self.create_database(second_workspace.database)
        second_workspace_token = Users.get_token_for_scope(second_workspace, scopes.ADMIN)
        self.workspaces_to_delete.append(second_workspace)

        # 1. Create Origin Datasource and insert example data
        origin_ds_name = f"origin_ds_{test_name}"
        origin_datasource_data = await self.create_datasource_with_schema(
            datasource_name=origin_ds_name, schema="a UInt64", token=first_workspace_token
        )
        await self._insert_data_in_datasource(
            token=self.admin_token, ds_name=origin_datasource_data.get("datasource").get("id"), data="1\n2\n3\n4"
        )

        # 2. Create destination datasource
        destination_ds_name = f"destination_ds_{test_name}"
        destination_datasource_data = await self.create_datasource_with_schema(
            datasource_name=destination_ds_name,
            schema="b UInt64, c UInt64",
            token=first_workspace_token,
        )

        # 3. Share Datasource with Second Workspace
        await tb_api_proxy_async.share_datasource_with_another_workspace(
            token=self.user_token,
            datasource_id=destination_datasource_data.get("datasource").get("id"),
            origin_workspace_id=first_workspace.id,
            destination_workspace_id=second_workspace.id,
            expect_notification=False,
        )

        # 4. Create Pipe and Pipe Node for later materialization in First Workspace
        pipe_name = f"pipe_{test_name}"
        origin_ds_id = origin_datasource_data.get("datasource").get("name")
        await tb_api_proxy_async.create_pipe(
            token=first_workspace_token,
            pipe_name=pipe_name,
            queries=[f"select a * 2 as b, a * 3 as c from {origin_ds_id}"],
        )

        # 5. Create Second Pipe and Pipe Node with Shared Datasource as FROM table
        second_pipe_name = f"second_pipe_{test_name}"
        await tb_api_proxy_async.create_pipe(
            token=second_workspace_token,
            pipe_name=second_pipe_name,
            queries=[
                f'select b * 2 as b, c * 3 as c from {first_workspace.name}.{destination_datasource_data.get("datasource").get("name")}'
            ],
        )

        # 6. Create Materialized View in Second Workspace
        second_workspace_materialization = await tb_api_proxy_async.make_materialized_view(
            second_workspace_token, second_pipe_name, f"{second_pipe_name}_0", "test_cascade_populate_revamp_ds_final"
        )
        second_workspace_materialization_response = json.loads(second_workspace_materialization.body)

        # 7. Create Materialized View in Main Workspace
        materialization = await tb_api_proxy_async.make_materialized_view(
            first_workspace_token,
            pipe_name,
            f"{pipe_name}_0",
            destination_datasource_data.get("datasource").get("id"),
            populate="true",
        )
        materialization_response = json.loads(materialization.body)

        # 8. Assertions
        job_response = materialization_response.get("job")
        job = await self.get_finalised_job_async(job_response.get("id"))
        self.assertEqual(job.status, "done", job.get("error", None))

        async def run_validation():
            populated_data_in_shared_ds = await self._query(
                second_workspace_token,
                f'SELECT * FROM {second_workspace_materialization_response.get("datasource").get("name")} FORMAT JSON',
            )

            sorted_results = sorted(populated_data_in_shared_ds.get("data"), key=lambda x: x.get("b"))
            self.assertEqual(
                sorted_results,
                [
                    {"b": 4, "c": 9},
                    {"b": 8, "c": 18},
                    {"b": 12, "c": 27},
                    {"b": 16, "c": 36},
                ],
            )

        await poll_async(run_validation)
        await self._unset_cluster_replicas(cluster)

    @tornado.testing.gen_test
    async def test_populate_revamp_with_shared_datasources(self):
        await self._populate_revamp_with_shared_datasources()

    @tornado.testing.gen_test
    async def test_populate_revamp_with_shared_datasources_with_job_replica(self):
        self.set_feature_flag(
            feature_flag=FeatureFlagWorkspaces.POOL_REPLICA_FOR_POPULATES, value=True, workspace_id=self.WORKSPACE_ID
        )
        await self._populate_revamp_with_shared_datasources()
        self.set_feature_flag(
            feature_flag=FeatureFlagWorkspaces.POOL_REPLICA_FOR_POPULATES, value=False, workspace_id=self.WORKSPACE_ID
        )

    @tornado.testing.gen_test
    @patch.object(ClusterPatches, "ENABLED", False)
    async def test_populate_revamp_multiple_datasources_in_mv_with_job_replica(self):
        self.set_feature_flag(
            feature_flag=FeatureFlagWorkspaces.POOL_REPLICA_FOR_POPULATES, value=True, workspace_id=self.WORKSPACE_ID
        )
        tb_api_proxy_async = TBApiProxyAsync(self)
        ws = Users.get_by_id(self.WORKSPACE_ID)
        cluster = await self._set_cluster_replicas(ws)
        test_name = f"test_populate_revamp_multiple_datasources_in_mv_with_job_replica_{uuid.uuid4().hex}"

        # 1. Create Trigger Datasource and insert example data
        trigger_ds_name = f"{test_name}_trigger_ds"
        trigger_ds = await self.create_datasource_with_schema(
            datasource_name=trigger_ds_name, schema="a UInt64", token=self.admin_token
        )
        await self._insert_data_in_datasource(
            token=self.admin_token, ds_name=trigger_ds.get("datasource").get("id"), data="4\n5\n6\n7"
        )

        second_ds_name = f"{test_name}_second_ds"
        second_ds = await self.create_datasource_with_schema(
            datasource_name=second_ds_name, schema="b UInt64", token=self.admin_token
        )
        await self._insert_data_in_datasource(
            token=self.admin_token, ds_name=second_ds.get("datasource").get("id"), data="1\n2\n3\n4"
        )

        # 2. Create Pipe and Pipe Node for later materialization in First Workspace
        pipe_name = f"{test_name}_pipe"
        await tb_api_proxy_async.create_pipe(
            token=self.admin_token,
            pipe_name=pipe_name,
            queries=[f"select a from {trigger_ds_name} where a > (select max(b) from {second_ds_name})"],
        )

        # 3. Wait for Data Source Replication
        self.wait_for_datasource_replication(ws, trigger_ds.get("datasource", {}).get("id"))
        self.wait_for_datasource_replication(ws, second_ds.get("datasource", {}).get("id"))

        # 4. Create Materialized View in Main Workspace
        materialization = await tb_api_proxy_async.make_materialized_view(
            self.admin_token, pipe_name, f"{pipe_name}_0", pipe_name, populate="true"
        )
        materialization_response = json.loads(materialization.body)

        job_response = materialization_response.get("job")
        job = await self.get_finalised_job_async(job_response.get("id"))
        self.assertEqual(job.status, "done", job.get("error", None))
        self.set_feature_flag(
            feature_flag=FeatureFlagWorkspaces.POOL_REPLICA_FOR_POPULATES, value=False, workspace_id=self.WORKSPACE_ID
        )

        # select data from materialized view
        populated_data = await self._query(
            self.admin_token, f'SELECT * FROM {materialization_response.get("datasource").get("name")} FORMAT JSON'
        )
        self.assertEqual(populated_data.get("data"), [{"a": 5}, {"a": 6}, {"a": 7}])
        await self._unset_cluster_replicas(cluster)

    @patch.object(ClusterPatches, "ENABLED", False)
    async def _test_populate_revamp_with_ttl(self):
        rnd = uuid.uuid4().hex
        tb_api_proxy_async = TBApiProxyAsync(self)
        # First Workspace
        first_workspace = Users.get_by_id(self.WORKSPACE_ID)
        cluster = await self._set_cluster_replicas(first_workspace)
        first_workspace_token = Users.get_token_for_scope(first_workspace, scopes.ADMIN)

        # 1. Create Origin Datasource and insert example data
        origin_ds_name = f"origin_ds_{rnd}"
        origin_datasource_data = await self.create_datasource_with_schema(
            datasource_name=origin_ds_name, schema="a UInt64", token=first_workspace_token
        )
        await self._insert_data_in_datasource(
            token=self.admin_token, ds_name=origin_datasource_data.get("datasource").get("id"), data="1\n2\n3\n4"
        )
        self.wait_for_datasource_replication(first_workspace, origin_datasource_data.get("datasource"))

        # 2. Create destination datasource
        destination_datasource_data = await self.create_datasource_with_schema(
            datasource_name=f"test_populate_revamp_ds_destination_{rnd}",
            schema="b UInt64, c UInt64, d DateTime",
            token=first_workspace_token,
            engine_ttl="d + interval 1 month",
        )

        # 4. Create Pipe and Pipe Node for later materialization in First Workspace
        pipe_name = f"test_populate_{rnd}"
        await tb_api_proxy_async.create_pipe(
            token=first_workspace_token,
            pipe_name=pipe_name,
            queries=[f"select a * 2 as b, a * 3 as c, toDateTime('2050-01-01 00:00:00') as d from {origin_ds_name}"],
        )

        # 5. Create Materialized View in Main Workspace
        materialization = await tb_api_proxy_async.make_materialized_view(
            first_workspace_token,
            pipe_name,
            f"{pipe_name}_0",
            destination_datasource_data.get("datasource").get("id"),
            populate="true",
        )
        materialization_response = json.loads(materialization.body)

        # 6. Assertions
        job_response = materialization_response.get("job")
        job = await self.get_finalised_job_async(job_response.get("id"))
        self.assertEqual(job.status, "done", job.get("error", None))
        self.wait_for_datasource_replication(first_workspace, destination_datasource_data.get("datasource"))

        async def run_validation():
            populated_data = await self._query(
                first_workspace_token,
                f'SELECT * FROM {destination_datasource_data.get("datasource").get("name")} FORMAT JSON',
            )

            sorted_results = sorted(populated_data.get("data"), key=lambda x: x.get("b"))
            self.assertEqual(
                sorted_results,
                [
                    {"b": 2, "c": 3, "d": "2050-01-01 00:00:00"},
                    {"b": 4, "c": 6, "d": "2050-01-01 00:00:00"},
                    {"b": 6, "c": 9, "d": "2050-01-01 00:00:00"},
                    {"b": 8, "c": 12, "d": "2050-01-01 00:00:00"},
                ],
            )

        async def check_partitions_ttl():
            ds_id = destination_datasource_data.get("datasource").get("id")
            response = exec_sql(
                first_workspace["database"],
                f"select table, partition, delete_ttl_info_max from system.parts where table = '{ds_id}' and active FORMAT JSON",
            )
            for r in response["data"]:
                self.assertTrue(r["delete_ttl_info_max"] != "1970-01-01 00:00:00", r)

        await poll_async(run_validation)
        await check_partitions_ttl()
        await self._unset_cluster_replicas(cluster)

    @tornado.testing.gen_test
    async def test_populate_revamp_with_ttl(self):
        await self._test_populate_revamp_with_ttl()

    @tornado.testing.gen_test
    async def test_populate_revamp_with_ttl_with_job_replica(self):
        self.set_feature_flag(
            feature_flag=FeatureFlagWorkspaces.POOL_REPLICA_FOR_POPULATES, value=True, workspace_id=self.WORKSPACE_ID
        )
        await self._test_populate_revamp_with_ttl()
        self.set_feature_flag(
            feature_flag=FeatureFlagWorkspaces.POOL_REPLICA_FOR_POPULATES, value=False, workspace_id=self.WORKSPACE_ID
        )

    @patch.object(ClusterPatches, "ENABLED", False)
    async def _test_populate_revamp_with_null_engines(self):
        name = f"test_populate_revamp_null_{uuid.uuid4().hex}"
        tb_api_proxy_async = TBApiProxyAsync(self)
        workspace = Users.get_by_id(self.WORKSPACE_ID)
        cluster = await self._set_cluster_replicas(workspace)
        workspace_token = Users.get_token_for_scope(workspace, scopes.ADMIN)

        # 1. Create Origin Datasource and insert example data
        origin_datasource_data = await self.create_datasource_with_schema(
            datasource_name=f"{name}_origin_datasource", schema="a UInt64", token=workspace_token
        )

        await self._insert_data_in_datasource(
            token=self.admin_token, ds_name=origin_datasource_data.get("datasource").get("id"), data="1\n2\n3\n4"
        )

        # 2. Create destination datasource
        destination_datasource_data = await self.create_datasource_with_schema(
            datasource_name=f"{name}_destination_datasource",
            schema="b UInt64, c UInt64",
            engine="Null",
            token=workspace_token,
        )

        # 4. Create Pipe and Pipe Node for later materialization
        pipe_name = f"{name}_pipe"
        await tb_api_proxy_async.create_pipe(
            token=workspace_token,
            pipe_name=pipe_name,
            queries=[f'select a * 2 as b, a * 3 as c from {origin_datasource_data.get("datasource").get("name")}'],
        )

        # 5. Create Materialized View
        materialization = await tb_api_proxy_async.make_materialized_view(
            workspace_token,
            pipe_name,
            f"{pipe_name}_0",
            destination_datasource_data.get("datasource").get("id"),
            populate="true",
        )
        materialization_response = json.loads(materialization.body)

        # 6. Assertions
        job_response = materialization_response.get("job")
        job = await self.get_finalised_job_async(job_response.get("id"))
        self.assertEqual(job.status, "done", job.get("error", None))

        await self._unset_cluster_replicas(cluster)

    @tornado.testing.gen_test
    async def test_populate_revamp_with_null_engines(self):
        await self._test_populate_revamp_with_null_engines()

    @tornado.testing.gen_test
    async def test_populate_revamp_with_null_engines_with_job_replica(self):
        self.set_feature_flag(
            feature_flag=FeatureFlagWorkspaces.POOL_REPLICA_FOR_POPULATES, value=True, workspace_id=self.WORKSPACE_ID
        )
        await self._test_populate_revamp_with_null_engines()
        self.set_feature_flag(
            feature_flag=FeatureFlagWorkspaces.POOL_REPLICA_FOR_POPULATES, value=False, workspace_id=self.WORKSPACE_ID
        )

    @patch.object(ClusterPatches, "ENABLED", False)
    async def _test_populate_revamp_with_joined_data(self):
        """
         +---------+  MV       +-------+  MV    +---------+
        |  OG DS   | --------> | MD DS |-----> | DEST DS |
        +---------+  POPULATE +------+   ^    +---------+
                                         |
                                +---------+
                               | JOIN DS |
                               +---------+

        """
        suffix = uuid.uuid4().hex
        tb_api_proxy_async = TBApiProxyAsync(self)
        workspace = Users.get_by_id(self.WORKSPACE_ID)
        cluster = await self._set_cluster_replicas(workspace)
        workspace_token = Users.get_token_for_scope(workspace, scopes.ADMIN)

        # 1. Create origin datasource and insert data
        origin_datasource_data = await tb_api_proxy_async.create_datasource(
            token=workspace_token,
            ds_name=f"origin_datasource_name_{suffix}",
            schema="a UInt64, date Date",
            engine_params={"engine": "MergeTree", "engine_sorting_key": "a", "engine_partition_key": "toYear(date)"},
        )
        await self._insert_data_in_datasource(
            token=self.admin_token,
            ds_name=origin_datasource_data.get("datasource").get("id"),
            data="1,2023-01-01\n2,2024-01-01\n3,2025-01-01\n4,2026-01-01",
        )

        # 2. Create middle datasource, no data
        middle_datasource_data = await tb_api_proxy_async.create_datasource(
            token=workspace_token,
            ds_name=f"middle_datasource_name_{suffix}",
            schema="a UInt64, date Date",
            engine_params={"engine": "MergeTree", "engine_sorting_key": "a", "engine_partition_key": "toYear(date)"},
        )

        # 3. Create datasource to join and insert data
        join_datasource_data = await tb_api_proxy_async.create_datasource(
            token=workspace_token,
            ds_name=f"join_datasource_name_{suffix}",
            schema="a UInt64, b UInt64",
            engine_params={"engine": "MergeTree", "engine_sorting_key": "a"},
        )

        await self._insert_data_in_datasource(
            token=self.admin_token,
            ds_name=join_datasource_data.get("datasource").get("id"),
            data="1,1\n2,2\n3,3",
        )

        # 4. Create destination datasource
        destination_datasource_data = await tb_api_proxy_async.create_datasource(
            token=workspace_token,
            ds_name=f"test_cascade_populate_revamp_joined_data_{suffix}",
            schema="a UInt64, b UInt64, date Date",
            engine_params={"engine": "MergeTree", "engine_sorting_key": "a", "engine_partition_key": "toYear(date)"},
        )

        # 5. Create first pipe
        pipe_name_1 = f"test_populate_revamp_join_mv_1_{suffix}"
        await tb_api_proxy_async.create_pipe(
            token=workspace_token,
            pipe_name=pipe_name_1,
            queries=[f"SELECT a, date FROM {origin_datasource_data.get('datasource').get('name')}"],
        )

        # 6. Create second pipe
        pipe_name_2 = f"test_populate_revamp_join_mv_2_{suffix}"
        await tb_api_proxy_async.create_pipe(
            token=workspace_token,
            pipe_name=pipe_name_2,
            queries=[
                f"SELECT a, b, date FROM {middle_datasource_data.get('datasource').get('name')} LEFT JOIN {join_datasource_data.get('datasource').get('name')} USING a"
            ],
        )

        # 7. Create materialization middle to destination, no populate
        materialization = await tb_api_proxy_async.make_materialized_view(
            workspace_token,
            pipe_name_2,
            f"{pipe_name_2}_0",
            destination_datasource_data.get("datasource").get("id"),
            populate="false",
        )
        materialization_response = json.loads(materialization.body)

        # 8. Create materialization origin to middle, populate
        materialization = await tb_api_proxy_async.make_materialized_view(
            workspace_token,
            pipe_name_1,
            f"{pipe_name_1}_0",
            middle_datasource_data.get("datasource").get("id"),
            populate="true",
        )
        materialization_response = json.loads(materialization.body)

        # 8. Assertions
        job_response = materialization_response.get("job")
        job = await self.get_finalised_job_async(job_response.get("id"))
        self.assertEqual(job.status, "done", job.get("error", None))

        async def run_validation():
            populated_data_in_final_ds = await self._query(
                workspace_token,
                f'SELECT * FROM {destination_datasource_data.get("datasource").get("name")} FORMAT JSON',
            )

            sorted_results = sorted(populated_data_in_final_ds.get("data"), key=lambda x: x.get("b"))
            self.assertEqual(
                sorted_results,
                [
                    {"a": 4, "b": 0, "date": "2026-01-01"},
                    {"a": 1, "b": 1, "date": "2023-01-01"},
                    {"a": 2, "b": 2, "date": "2024-01-01"},
                    {"a": 3, "b": 3, "date": "2025-01-01"},
                ],
            )

        await poll_async(run_validation)
        await self._unset_cluster_replicas(cluster)

    @tornado.testing.gen_test
    async def test_populate_revamp_with_joined_data(self):
        await self._test_populate_revamp_with_joined_data()

    @tornado.testing.gen_test
    async def test_populate_revamp_with_joined_data_with_job_replica(self):
        self.set_feature_flag(
            feature_flag=FeatureFlagWorkspaces.POOL_REPLICA_FOR_POPULATES, value=True, workspace_id=self.WORKSPACE_ID
        )
        await self._test_populate_revamp_with_joined_data()
        self.set_feature_flag(
            feature_flag=FeatureFlagWorkspaces.POOL_REPLICA_FOR_POPULATES, value=False, workspace_id=self.WORKSPACE_ID
        )

    @patch.object(ClusterPatches, "ENABLED", False)
    async def _test_populate_revamp_with_incompatible_partitions(self):
        tb_api_proxy_async = TBApiProxyAsync(self)
        name = f"test_populate_revamp_with_incompatible_partitions_{uuid.uuid4().hex}"
        # First Workspace
        first_workspace = Users.get_by_id(self.WORKSPACE_ID)
        cluster = await self._set_cluster_replicas(first_workspace)
        first_workspace_token = Users.get_token_for_scope(first_workspace, scopes.ADMIN)

        # 1. Create Origin Datasource and insert example data
        origin_datasource_name = f"origin_datasource_{name}"
        origin_datasource_data = await tb_api_proxy_async.create_datasource(
            token=first_workspace_token,
            ds_name=origin_datasource_name,
            schema="a UInt64, date Date",
            engine_params={"engine": "MergeTree", "engine_sorting_key": "a", "engine_partition_key": "toYear(date)"},
        )
        await self._insert_data_in_datasource(
            token=self.admin_token,
            ds_name=origin_datasource_data.get("datasource").get("id"),
            data="1,2023-01-01\n2,2024-01-01\n3,2025-01-01\n4,2026-01-01",
        )

        # 2. Create destination datasource
        destination_datasource_name = f"destination_datasource_{name}"
        destination_datasource_data = await tb_api_proxy_async.create_datasource(
            token=first_workspace_token,
            ds_name=destination_datasource_name,
            schema="b UInt64, c UInt64, date Date",
            engine_params={"engine": "MergeTree", "engine_sorting_key": "b", "engine_partition_key": "toYear(date)"},
        )

        # 3. Create additional datasource
        datasource_with_incompatible_partition_key = await tb_api_proxy_async.create_datasource(
            token=first_workspace_token,
            ds_name="test_incompatible_partitions",
            schema="b UInt64, c UInt64, str String",
            engine_params={"engine": "MergeTree", "engine_sorting_key": "b", "engine_partition_key": "tuple()"},
        )

        # 4. Create Pipe and Pipe Node for later materialization in First Workspace
        pipe_name = f"pipe_{name}"
        await tb_api_proxy_async.create_pipe(
            token=first_workspace_token,
            pipe_name=pipe_name,
            queries=[f"select a * 2 as b, a * 3 as c from {origin_datasource_data.get('datasource').get('name')}"],
        )

        # 5. Create Second Pipe and Pipe Node with Additional Datasource as FROM table
        second_pipe_name = f"second_pipe_{name}"
        await tb_api_proxy_async.create_pipe(
            token=first_workspace_token,
            pipe_name=second_pipe_name,
            queries=[
                f"select b * 2 as b, c * 3 as c, 'b' as str from {destination_datasource_data.get('datasource').get('name')}"
            ],
        )

        # 6. Create Materialized View in Second Workspace
        await tb_api_proxy_async.make_materialized_view(
            first_workspace_token,
            second_pipe_name,
            f"{second_pipe_name}_0",
            datasource_with_incompatible_partition_key.get("datasource").get("id"),
        )

        # 7. Create Materialized View in Main Workspace
        materialization = await tb_api_proxy_async.make_materialized_view(
            first_workspace_token,
            pipe_name,
            f"{pipe_name}_0",
            destination_datasource_data.get("datasource").get("id"),
            populate="true",
        )
        materialization_response = json.loads(materialization.body)

        # 8. Assertions
        job_response = materialization_response.get("job")
        job = await self.get_finalised_job_async(job_response.get("id"))
        self.assertEqual(job.status, "done", job.get("error", None))

        async def run_validation():
            populated_data_in_final_ds = await self._query(
                first_workspace_token,
                f'SELECT * FROM {datasource_with_incompatible_partition_key.get("datasource").get("name")} FORMAT JSON',
            )

            sorted_results = sorted(populated_data_in_final_ds.get("data"), key=lambda x: x.get("b"))
            self.assertEqual(
                sorted_results,
                [
                    {"b": 4, "c": 9, "str": "b"},
                    {"b": 8, "c": 18, "str": "b"},
                    {"b": 12, "c": 27, "str": "b"},
                    {"b": 16, "c": 36, "str": "b"},
                ],
            )

        await poll_async(run_validation)
        await self._unset_cluster_replicas(cluster)

    @tornado.testing.gen_test
    async def test_populate_revamp_with_incompatible_partitions(self):
        await self._test_populate_revamp_with_incompatible_partitions()

    @tornado.testing.gen_test
    async def test_populate_revamp_with_incompatible_partitions_with_job_replica(self):
        self.set_feature_flag(
            feature_flag=FeatureFlagWorkspaces.POOL_REPLICA_FOR_POPULATES, value=True, workspace_id=self.WORKSPACE_ID
        )
        await self._test_populate_revamp_with_incompatible_partitions()
        self.set_feature_flag(
            feature_flag=FeatureFlagWorkspaces.POOL_REPLICA_FOR_POPULATES, value=False, workspace_id=self.WORKSPACE_ID
        )

    @patch.object(ClusterPatches, "ENABLED", False)
    @patch("tinybird_shared.retry.retry.retry_sync", side_effect=mock_retry_sync)
    async def _test_populate_revamp_with_failing_drop_partition(self, _mock_retry_sync):
        tb_api_proxy_async = TBApiProxyAsync(self)
        workspace = Users.get_by_id(self.WORKSPACE_ID)
        cluster = await self._set_cluster_replicas(workspace)
        workspace_token = Users.get_token_for_scope(workspace, scopes.ADMIN)
        test_name = f"populate_revamp_with_failing_drop_partition_{uuid.uuid4().hex}"

        # 1. Create Partitioned Origin Datasource and insert example data
        origin_ds_name = f"origin_ds_{test_name}"
        origin_datasource_data = await self.create_datasource_with_schema(
            datasource_name=origin_ds_name,
            schema="a UInt64",
            token=workspace_token,
            engine="MergeTree",
            engine_partition_key="a",
        )
        await self._insert_data_in_datasource(
            token=self.admin_token, ds_name=origin_datasource_data.get("datasource").get("id"), data="1\n2\n3\n4"
        )

        # 2. Create Partitioned Destination Datasource
        destination_ds_name = f"destination_ds_{test_name}"
        destination_datasource_data = await self.create_datasource_with_schema(
            datasource_name=destination_ds_name,
            schema="b UInt64, c UInt64",
            token=workspace_token,
            engine="MergeTree",
            engine_partition_key="b",
        )

        # 4. Create Pipe and Pipe Node for later materialization in Workspace
        pipe_name = f"pipe_{test_name}"
        await tb_api_proxy_async.create_pipe(
            token=workspace_token,
            pipe_name=pipe_name,
            queries=[f"select a * 2 as b, a * 3 as c from {origin_ds_name}"],
        )

        real_query_sync = HTTPClient.query_sync

        def fake_query_sync(self, *args, **kwargs):
            if kwargs.get("user_agent", "") == "no-tb-populate-alter-query" and "DROP PARTITION" in args[0]:
                raise CHException(f"Code: {CHErrors.TIMEOUT_EXCEEDED}, couldn't execute drop partition", fatal=False)

            return real_query_sync(self, *args, **kwargs)

        self.mpatch.setattr(HTTPClient, "query_sync", fake_query_sync)

        # 7. Create Materialized View in Workspace
        materialization = await tb_api_proxy_async.make_materialized_view(
            workspace_token,
            pipe_name,
            f"{pipe_name}_0",
            destination_datasource_data.get("datasource").get("id"),
            populate="true",
        )
        materialization_response = json.loads(materialization.body)

        # 8. Assertions
        job_response = materialization_response.get("job")
        job = await self.get_finalised_job_async(job_response.get("id"))

        self.assertEqual(job.status, "cancelled")
        cancelled_queries = [q for q in job.queries if q.get("status") == "cancelled"]
        done_queries = [q for q in job.queries if q.get("status") == "done"]
        self.assertEqual(len(cancelled_queries), 3)
        self.assertEqual(len(done_queries), 1)
        self.assertEqual(done_queries[0].get("total_steps"), 1)
        self.assertEqual(done_queries[0].get("remaining_steps"), 0)
        await self._unset_cluster_replicas(cluster)

    @tornado.testing.gen_test
    async def test_populate_revamp_with_failing_drop_partition(self):
        await self._test_populate_revamp_with_failing_drop_partition()

    @tornado.testing.gen_test
    async def test_populate_revamp_with_failing_drop_partition_with_job_replica(self):
        self.set_feature_flag(
            feature_flag=FeatureFlagWorkspaces.POOL_REPLICA_FOR_POPULATES, value=True, workspace_id=self.WORKSPACE_ID
        )
        await self._test_populate_revamp_with_failing_drop_partition()
        self.set_feature_flag(
            feature_flag=FeatureFlagWorkspaces.POOL_REPLICA_FOR_POPULATES, value=False, workspace_id=self.WORKSPACE_ID
        )

    @patch.object(ClusterPatches, "DDL_CHECKS", False)
    @patch.object(ClusterPatches, "ENABLED", False)
    async def _test_populate_revamp_with_non_replicated_table(self):
        tb_api_proxy_async = TBApiProxyAsync(self)
        name = f"test_populate_revamp_with_non_replicated_table_{uuid.uuid4().hex}"
        workspace = Users.get_by_id(self.WORKSPACE_ID)
        cluster = await self._set_cluster_replicas(workspace)
        workspace_token = Users.get_token_for_scope(workspace, scopes.ADMIN)

        # 1. Create Partitioned Origin Datasource and insert example data
        origin_datasource_name = f"origin_datasource_{name}"
        origin_datasource_data = await self.create_datasource_with_schema(
            datasource_name=origin_datasource_name,
            schema="a UInt64",
            token=workspace_token,
            engine="MergeTree",
            engine_partition_key="a",
        )

        await self._insert_data_in_datasource(
            token=self.admin_token, ds_name=origin_datasource_data.get("datasource").get("id"), data="1\n2\n3\n4"
        )

        # 2. Create Partitioned Destination Datasource
        destination_datasource_name = f"destination_datasource_{name}"
        destination_datasource_data = await self.create_datasource_with_schema(
            datasource_name=destination_datasource_name,
            schema="b UInt64, c UInt64",
            token=workspace_token,
            engine="MergeTree",
            engine_partition_key="b",
        )

        # 3. Create auxiliar non-replicated table
        client = HTTPClient(host=CH_ADDRESS, database=workspace.database)
        table_name = f"{workspace.database}.replacingmergetree_datasource_name_{name}"
        await client.query(
            f"""
            CREATE TABLE {table_name} ON CLUSTER tinybird (
                `environmentId` LowCardinality(String)
            )
            ENGINE=ReplacingMergeTree()
            ORDER BY (environmentId)
        """,
            read_only=False,
        )

        # 4. Create Pipe and Pipe Node for later materialization in Workspace
        pipe_name = f"pipe_{name}"
        await tb_api_proxy_async.create_pipe(
            token=workspace_token,
            pipe_name=pipe_name,
            queries=[f'select a * 2 as b, a * 3 as c from {origin_datasource_data.get("datasource").get("name")}'],
        )

        # 5. Create Materialized View in Workspace
        materialization = await tb_api_proxy_async.make_materialized_view(
            workspace_token,
            pipe_name,
            f"{pipe_name}_0",
            destination_datasource_data.get("datasource").get("id"),
            populate="true",
        )
        materialization_response = json.loads(materialization.body)

        # 6. Assertions
        job_response = materialization_response.get("job")
        job = await self.get_finalised_job_async(job_response.get("id"))

        self.assertEqual(job.status, "done")
        self.assertEqual(
            sorted(job.queries, key=lambda x: x.get("partition")),
            [
                {
                    "query_id": mock.ANY,
                    "status": "done",
                    "partition": "1",
                    "total_steps": 1,
                    "remaining_steps": 0,
                },
                {
                    "query_id": mock.ANY,
                    "status": "done",
                    "partition": "2",
                    "total_steps": 1,
                    "remaining_steps": 0,
                },
                {
                    "query_id": mock.ANY,
                    "status": "done",
                    "partition": "3",
                    "total_steps": 1,
                    "remaining_steps": 0,
                },
                {
                    "query_id": mock.ANY,
                    "status": "done",
                    "partition": "4",
                    "total_steps": 1,
                    "remaining_steps": 0,
                },
            ],
        )
        await client.query(
            f"""
            DROP TABLE {table_name} ON CLUSTER tinybird
        """,
            read_only=False,
        )

        await self._unset_cluster_replicas(cluster)

    @tornado.testing.gen_test
    async def test_populate_revamp_with_non_replicated_table(self):
        await self._test_populate_revamp_with_non_replicated_table()

    @tornado.testing.gen_test
    async def test_populate_revamp_with_non_replicated_table_with_job_replica(self):
        self.set_feature_flag(
            feature_flag=FeatureFlagWorkspaces.POOL_REPLICA_FOR_POPULATES, value=True, workspace_id=self.WORKSPACE_ID
        )
        await self._test_populate_revamp_with_non_replicated_table()
        self.set_feature_flag(
            feature_flag=FeatureFlagWorkspaces.POOL_REPLICA_FOR_POPULATES, value=False, workspace_id=self.WORKSPACE_ID
        )

    @mock.patch("tinybird.ch.ch_explain_query", return_value=[])
    async def _test_populate_revamp_with_materialized_view_skip_error_on_non_dependent_view(
        self, _mock_ch_explain_query
    ):
        tb_api_proxy_async = TBApiProxyAsync(self)
        workspace = Users.get_by_id(self.WORKSPACE_ID)
        cluster = await self._set_cluster_replicas(workspace)

        workspace_token = Users.get_token_for_scope(workspace, scopes.ADMIN)
        prefix = uuid.uuid4().hex
        origin_datasource_name = f"origin_datasource_{prefix}"
        origin_datasource_name2 = f"origin_datasource2_{prefix}"
        origin_datasource_name3 = f"origin_datasource3_{prefix}"
        destination_datasource_name = f"destination_datasource_{prefix}"
        destination_datasource_name2 = f"destination_datasource2_{prefix}"

        # in this text we create a dataflow with two branches
        # origin_datasource2, origin_datasource3 -> mv -> destination_datasource
        # origin_datasource -> mv2 -> destination_datasource2
        # when populating origin_datasource: mv raises a "Scalar subquery returned empty result" b/c tables are empty
        # since mv is not dependent of origin_datasource, it's skipped and the populate finishes

        # 1. Create Origin data source and insert example data
        origin_datasource_data = await self.create_datasource_with_schema(
            datasource_name=origin_datasource_name, schema="`name` String", token=workspace_token, engine="MergeTree"
        )

        await self._insert_data_in_datasource(
            token=self.admin_token, ds_name=origin_datasource_data.get("datasource").get("id"), data="aaa"
        )

        # 1. Create Origin2 data source and insert example data
        origin_datasource_data2 = await self.create_datasource_with_schema(
            datasource_name=origin_datasource_name2,
            schema="`filters` Array(String), `pattern_regex` Nullable(String), `names` Tuple(Array(String), Array(String))",
            token=workspace_token,
            engine="MergeTree",
        )

        url = f"http://{CH_ADDRESS}/?database={workspace.database}"
        # add some data (using this method to insert a tuple easily)
        requests.post(  # noqa: ASYNC210
            url,
            data="""
            insert into `%s` SELECT ['aaa'] as filters, 'bbb' as pattern_regex, (['aaa'], ['bbb']) as names
        """
            % origin_datasource_data2.get("datasource").get("id"),
        )

        # 1. Create Origin3 data source and insert example data
        origin_datasource_data3 = await self.create_datasource_with_schema(
            datasource_name=origin_datasource_name3, schema="`name` String", token=workspace_token, engine="MergeTree"
        )

        await self._insert_data_in_datasource(
            token=self.admin_token, ds_name=origin_datasource_data3.get("datasource").get("id"), data="aaa"
        )

        # 2. Create destination data source
        destination_datasource_data = await self.create_datasource_with_schema(
            datasource_name=destination_datasource_name,
            schema="`full_name` LowCardinality(String)",
            token=workspace_token,
            engine="MergeTree",
        )

        destination_datasource_data2 = await self.create_datasource_with_schema(
            datasource_name=destination_datasource_name2,
            schema="`full_name` LowCardinality(String)",
            token=workspace_token,
            engine="MergeTree",
        )

        # 3. Create Pipe and Pipe Node using the offending query, not used in the populate
        pipe_name = f"mv_pipe_{prefix}"
        mv_query = f"""
            WITH
                (
                    SELECT names
                    FROM {origin_datasource_name2}
                ) AS bot_names
                SELECT
                    transform(
                        name,
                        bot_names.1,
                        bot_names.2
                    ) AS full_name
                FROM {origin_datasource_name3}
        """

        await tb_api_proxy_async.create_pipe(
            token=workspace_token,
            pipe_name=pipe_name,
            queries=[mv_query],
        )

        # 3. Create Pipe and Pipe Node for later materialization in Workspace
        pipe_name2 = f"mv_pipe2_{prefix}"
        mv_query2 = f"""
            SELECT
                name as full_name
            FROM {origin_datasource_name}
        """

        await tb_api_proxy_async.create_pipe(
            token=workspace_token,
            pipe_name=pipe_name2,
            queries=[mv_query2],
        )

        job = None
        datasource_id = destination_datasource_data.get("datasource").get("id")
        datasource_id2 = destination_datasource_data2.get("datasource").get("id")

        # 7. Create Materialized View in Workspace
        await tb_api_proxy_async.make_materialized_view(
            workspace_token,
            pipe_name,
            f"{pipe_name}_0",
            datasource_id,
            populate="false",
        )

        materialization = await tb_api_proxy_async.make_materialized_view(
            workspace_token,
            pipe_name2,
            f"{pipe_name2}_0",
            datasource_id2,
            populate="true",
        )
        materialization_response = json.loads(materialization.body)

        # 8. Assertions
        job_response = materialization_response.get("job")
        job = await self.get_finalised_job_async(job_response.get("id"))

        self.assertEqual(job.status, "done")

        await self._unset_cluster_replicas(cluster)

    @tornado.testing.gen_test
    async def test_populate_revamp_with_materialized_view_skip_error_on_non_dependent_view(self):
        await self._test_populate_revamp_with_materialized_view_skip_error_on_non_dependent_view()

    @patch.object(ClusterPatches, "ENABLED", False)
    @tornado.testing.gen_test
    async def test_populate_revamp_with_materialized_view_skip_error_on_non_dependent_view_with_job_replica(self):
        self.set_feature_flag(
            feature_flag=FeatureFlagWorkspaces.POOL_REPLICA_FOR_POPULATES, value=True, workspace_id=self.WORKSPACE_ID
        )
        await self._test_populate_revamp_with_materialized_view_skip_error_on_non_dependent_view()
        self.set_feature_flag(
            feature_flag=FeatureFlagWorkspaces.POOL_REPLICA_FOR_POPULATES, value=False, workspace_id=self.WORKSPACE_ID
        )

    @mock.patch("tinybird.ch.ch_explain_query", return_value=[])
    async def _test_populate_revamp_with_materialized_view_error_on_empty_data(self, _mock_ch_explain_query):
        tb_api_proxy_async = TBApiProxyAsync(self)
        workspace = Users.get_by_id(self.WORKSPACE_ID)
        cluster = await self._set_cluster_replicas(workspace)
        workspace_token = Users.get_token_for_scope(workspace, scopes.ADMIN)
        prefix = uuid.uuid4().hex
        origin_datasource_name = f"origin_datasource_{prefix}"
        destination_datasource_name = f"destination_datasource_{prefix}"

        # 1. Create Origin data source and insert example data
        origin_datasource_data = await self.create_datasource_with_schema(
            datasource_name=origin_datasource_name, schema="`name` String", token=workspace_token, engine="MergeTree"
        )

        await self._insert_data_in_datasource(
            token=self.admin_token, ds_name=origin_datasource_data.get("datasource").get("id"), data="aaa"
        )

        # 2. Create destination data source
        destination_datasource_data = await self.create_datasource_with_schema(
            datasource_name=destination_datasource_name,
            schema="`name` LowCardinality(String)",
            token=workspace_token,
            engine="MergeTree",
        )

        # 3. Create Pipe and Pipe Node for later materialization in Workspace
        pipe_name = f"mv_pipe_{prefix}"
        mv_query = f"""
            SELECT
                name
            FROM {origin_datasource_name}
        """

        await tb_api_proxy_async.create_pipe(
            token=workspace_token,
            pipe_name=pipe_name,
            queries=[mv_query],
        )

        job = None
        datasource_id = destination_datasource_data.get("datasource").get("id")

        ch_exception = CHException(
            f"Code: 125. DB::Exception: [Custom] Scalar subquery returned empty result of type Tuple(Array(String), Array(String)) which cannot be Nullable: While processing (SELECT names FROM {workspace.database}.{datasource_id} AS bot_names_tuple) AS bot_names. (INCORRECT_RESULT_OF_SCALAR_SUBQUERY) (version x.x.x)\n"
        )

        with patch("tinybird.populates.job.ch_create_temporary_databases_sync", side_effect=ch_exception):
            # 7. Create Materialized View in Workspace
            materialization = await tb_api_proxy_async.make_materialized_view(
                workspace_token,
                pipe_name,
                f"{pipe_name}_0",
                datasource_id,
                populate="true",
            )
            materialization_response = json.loads(materialization.body)

            # 8. Assertions
            job_response = materialization_response.get("job")
            job = await self.get_finalised_job_async(job_response.get("id"))

        self.assertEqual(job.status, "error")
        self.assertTrue(
            f"[Custom] Scalar subquery returned empty result of type Tuple(Array(String), Array(String)) which cannot be Nullable: While processing (SELECT names FROM {workspace.name}.{destination_datasource_name} AS bot_names_tuple) AS bot_names."
            in job.error
        )

        await self._unset_cluster_replicas(cluster)

    @tornado.testing.gen_test
    async def test_populate_revamp_with_materialized_view_error_on_empty_data(self):
        await self._test_populate_revamp_with_materialized_view_error_on_empty_data()

    @tornado.testing.gen_test
    @patch.object(ClusterPatches, "ENABLED", False)
    async def test_populate_revamp_with_materialized_view_error_on_empty_data_with_job_replica(self):
        self.set_feature_flag(
            feature_flag=FeatureFlagWorkspaces.POOL_REPLICA_FOR_POPULATES, value=True, workspace_id=self.WORKSPACE_ID
        )
        await self._test_populate_revamp_with_materialized_view_error_on_empty_data()
        self.set_feature_flag(
            feature_flag=FeatureFlagWorkspaces.POOL_REPLICA_FOR_POPULATES, value=False, workspace_id=self.WORKSPACE_ID
        )

    @tornado.testing.gen_test
    async def test_analyze_pipe_to_materialize_with_sum_and_avg_in_query_should_raise_warning(self):
        self.create_test_datasource()
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_analyze_pipe_to_materialize"
        Users.add_pipe_sync(
            u,
            pipe_name,
            """
                        SELECT
                            toDateTime(a) AS d,
                            toString(a) AS b,
                            sum(toInt32(a)) AS sum_units,
                            avg(toInt32(a)) AS avg_units
                        FROM test_table as t
                        GROUP BY
                            d, b
                    """,
        )

        params = {
            "token": token,
        }

        response = await self.fetch_async(f"/v0/pipes/{pipe_name}/nodes/{pipe_name}_0/analysis?{urlencode(params)}")
        result = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(
            result.get("warnings")[0]["text"],
            "The query will be rewritten adding the -State modifier for the Materialized View to work properly. Rewritten functions: avg -> avgState, sum -> sumState.",
        )
        self.assertEqual(
            result.get("warnings")[0]["documentation"],
            "https://www.tinybird.co/docs/concepts/materialized-views.html#what-should-i-use" "-materialized-views-for",
        )

    @tornado.testing.gen_test
    async def test_analyze_pipe_to_materialize_with_sum_in_query_should_raise_warning(self):
        self.create_test_datasource()
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_analyze_pipe_to_materialize"
        Users.add_pipe_sync(
            u,
            pipe_name,
            """
                    SELECT
                        toDateTime(a) AS d,
                        toString(a) AS b,
                        sum(toInt32(a)) AS sum_units
                    FROM test_table as t
                    GROUP BY
                        d, b
                """,
        )

        # 1. Create pipe
        params = {
            "token": token,
        }

        response = await self.fetch_async(f"/v0/pipes/{pipe_name}/nodes/{pipe_name}_0/analysis?{urlencode(params)}")
        result = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(
            result.get("warnings")[0]["text"],
            "The query will be rewritten adding the -State modifier for the Materialized View to work properly. Rewritten functions: sum -> sumState.",
        )
        self.assertEqual(
            result.get("warnings")[0]["documentation"],
            "https://www.tinybird.co/docs/concepts/materialized" "-views.html#what-should-i-use-materialized-views-for",
        )

    @tornado.testing.gen_test
    async def test_analyze_pipe_to_materialize_with_function_in_query_should_raise_warning_without_warn_about_already_present_states(
        self,
    ):
        self.create_test_datasource()
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_analyze_pipe_to_materialize"
        Users.add_pipe_sync(
            u,
            pipe_name,
            """
                        SELECT
                            toDateTime(a) AS d,
                            toString(a) AS b,
                            avgState(toInt32(a)) AS avg_units,
                            exponentialMovingAverage(2)(toInt32(a), toInt32(a) / 5) as empireState
                        FROM test_table as t
                        GROUP BY
                            d, b
                    """,
        )

        params = {
            "token": token,
        }

        response = await self.fetch_async(f"/v0/pipes/{pipe_name}/nodes/{pipe_name}_0/analysis?{urlencode(params)}")
        result = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(
            result.get("warnings")[0]["text"],
            "The query will be rewritten adding the -State modifier for the Materialized View to work properly. Rewritten functions: exponentialMovingAverage -> exponentialMovingAverageState.",
        )
        self.assertEqual(
            result.get("warnings")[0]["documentation"],
            "https://www.tinybird.co/docs/concepts/materialized-views.html#what-should-i-use" "-materialized-views-for",
        )

    @tornado.testing.gen_test
    async def test_analyze_pipe_to_materialize_without_avg_or_sum_in_query_should_not_raise_warning(self):
        self.create_test_datasource()
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = "test_analyze_pipe_to_materialize"
        Users.add_pipe_sync(u, pipe_name, "select * from test_table")

        params = {
            "token": token,
        }

        response = await self.fetch_async(f"/v0/pipes/{pipe_name}/nodes/{pipe_name}_0/analysis?{urlencode(params)}")
        result = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(result.get("warnings"), [])


class TestPipeStatsRt(APIDataTableBaseTest):
    @tornado.testing.gen_test
    async def test_types_used_to_create_the_datasource_are_the_expected(self):
        public_user = public.get_public_user()
        token = public_user.get_token_for_scope(scopes.ADMIN)
        types_used = await self._query(token=token, sql="select * from pipe_stats_rt limit 1 Format JSON")
        self.assertEquals(
            [
                {"name": "start_datetime", "type": "DateTime"},
                {"name": "user_id", "type": "String"},
                {"name": "request_id", "type": "String"},
                {"name": "url", "type": "Nullable(String)"},
                {"name": "pipe_id", "type": "String"},
                {"name": "pipe_name", "type": "String"},
                {"name": "status_code", "type": "Int32"},
                {"name": "error", "type": "UInt8"},
                {"name": "token", "type": "String"},
                {"name": "token_name", "type": "String"},
                {"name": "duration", "type": "Float32"},
                {"name": "read_bytes", "type": "UInt64"},
                {"name": "read_rows", "type": "UInt64"},
                {"name": "billable", "type": "UInt8"},
                {"name": "result_rows", "type": "UInt64"},
                {"name": "parameters", "type": "Map(String, String)"},
                {"name": "method", "type": "LowCardinality(String)"},
                {"name": "release", "type": "String"},
                {"name": "user_agent", "type": "Nullable(String)"},
                {"name": "resource_tags", "type": "Array(String)"},
                {"name": "cpu_time", "type": "Float64"},
            ],
            types_used["meta"],
        )

    @tornado.testing.gen_test
    async def test_a_pipe_call_fills_the_pipe_stats_rt_data(self):
        await self._make_endpoint()

        u = Users.get_by_id(self.WORKSPACE_ID)
        request_token = Users.add_token(u, f"request_token_{uuid.uuid4().hex}", scopes.ADMIN)
        await self._get_pipe_data("csv", token=request_token)

        self.force_flush_of_span_records()

        public_user = public.get_public_user()
        token = public_user.get_token_for_scope(scopes.ADMIN)

        u = Users.get_by_id(self.WORKSPACE_ID)
        request_token_details = u.get_token_access_info(request_token)

        async def run_validation():
            content_inside_pipe_stats_rt = await self._query(
                token=token,
                sql=f"select * from pipe_stats_rt where user_id = '{self.WORKSPACE_ID}' order by start_datetime Format JSON",
            )

            self.assertEqual(
                {
                    "start_datetime": mock.ANY,
                    "user_id": self.WORKSPACE_ID,
                    "request_id": mock.ANY,
                    "url": matches(
                        r"/v0/pipes/test_pipe\.csv\?test=test_a_pipe_call_fills_the_pipe_stats_rt_data&time=[0-9]*"
                    ),
                    "pipe_id": matches(r"t_*"),
                    "pipe_name": "test_pipe",
                    "status_code": 200,
                    "token": request_token_details.id,
                    "token_name": request_token_details.name,
                    "error": 0,
                    "duration": mock.ANY,
                    "read_bytes": mock.ANY,
                    "read_rows": 6,
                    "billable": 1,
                    "result_rows": 6,
                    "parameters": mock.ANY,
                    "method": "GET",
                    "release": mock.ANY,
                    "user_agent": mock.ANY,
                    "cpu_time": numericRange(0.0, 0.1)
                    if get_min_clickhouse_version() >= pkg_resources.parse_version("24.6.10.2")
                    else mock.ANY,
                    "resource_tags": [],
                },
                content_inside_pipe_stats_rt["data"][0],
            )

        await poll_async(run_validation)

    @tornado.testing.gen_test
    async def test_a_pipe_call_only_billable_exposed_in_pipe_stats_rt_data(self):
        await self._make_endpoint()

        u = Users.get_by_id(self.WORKSPACE_ID)
        request_token = Users.add_token(u, f"request_token_{uuid.uuid4().hex}", scopes.ADMIN)
        _, headers = await self._get_pipe_data("csv", token=request_token, params={"from": "ui"}, headers=True)
        request_id_not_billable = headers.get("x-request-id")
        _, headers = await self._get_pipe_data("csv", token=request_token, headers=True)
        request_id_billable = headers.get("x-request-id")

        self.force_flush_of_span_records()

        async def run_validation():
            params = {
                "from": "ui",
                "token": request_token,
                "q": f"% SELECT * from tinybird.pipe_stats_rt where request_id = '{request_id_not_billable}' FORMAT JSON",
            }

            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            self.assertEqual(response.code, 200)
            payload = json.loads(response.body)
            self.assertEqual(len(payload["data"]), 0)

            params = {
                "from": "ui",
                "token": request_token,
                "q": f"% SELECT * from tinybird.pipe_stats_rt where request_id = '{request_id_billable}' FORMAT JSON",
            }
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            self.assertEqual(response.code, 200)
            payload = json.loads(response.body)
            self.assertEqual(len(payload["data"]), 1)

        await poll_async(run_validation)


class TestPipeStats(APIDataTableBaseTest):
    @tornado.testing.gen_test
    async def test_types_used_to_create_the_datasource_are_the_expected(self):
        self.maxDiff = None
        public_user = public.get_public_user()
        token = public_user.get_token_for_scope(scopes.ADMIN)
        types_used = await self._query(token=token, sql="select * from pipe_stats limit 1 Format JSON")
        self.assertEquals(
            [
                {"name": "date", "type": "Date"},
                {"name": "user_id", "type": "String"},
                {"name": "pipe_id", "type": "String"},
                {"name": "billable", "type": "UInt8"},
                {"name": "pipe_name", "type": "String"},
                {"name": "error_count", "type": "UInt64"},
                {"name": "view_count", "type": "UInt64"},
                {"name": "avg_duration_state", "type": "AggregateFunction(avg, Float32)"},
                {
                    "name": "quantile_timing_state",
                    "type": "AggregateFunction(quantilesTiming(0.9, 0.95, 0.99), Float64)",
                },
                {"name": "read_bytes_sum", "type": "UInt64"},
                {"name": "read_rows_sum", "type": "UInt64"},
                {"name": "resource_tags", "type": "Array(String)"},
                {"name": "resource_tags_total", "type": "Array(String)"},
            ],
            types_used["meta"],
        )

    @tornado.testing.gen_test
    async def test_a_pipe_call_fills_the_pipe_stats_data(self):
        await self._make_endpoint()
        await self._get_pipe_data("csv")
        self.force_flush_of_span_records()

        public_user = public.get_public_user()
        public_user_token = public_user.get_token_for_scope(scopes.ADMIN)

        async def run_validation():
            content_inside_pipe_stats_rt = await self._query(
                token=public_user_token,
                sql=f"select * from pipe_stats where user_id = '{self.WORKSPACE_ID}' order by date Format JSON",
            )

            self.assertEqual(
                {
                    "avg_duration_state": mock.ANY,
                    "billable": 1,
                    "date": matches(r"2\d+-\d+-\d+"),
                    "error_count": 0,
                    "pipe_id": matches(r"t_*"),
                    "pipe_name": "test_pipe",
                    "quantile_timing_state": mock.ANY,
                    "read_bytes_sum": mock.ANY,
                    "read_rows_sum": 6,
                    "resource_tags": [],
                    "resource_tags_total": [],
                    "user_id": self.WORKSPACE_ID,
                    "view_count": 1,
                },
                content_inside_pipe_stats_rt["data"][0],
            )

        await poll_async(run_validation)

    @tornado.testing.gen_test
    async def test_a_sql_call_fills_the_pipe_stats_data(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        request_token = Users.add_token(u, f"request_token_{uuid.uuid4().hex}", scopes.ADMIN)

        # Random query to see the results in spans
        await self._query(token=request_token, sql="select 1 Format JSON")
        self.force_flush_of_span_records()

        public_user = public.get_public_user()
        public_user_token = public_user.get_token_for_scope(scopes.ADMIN)

        async def run_validation():
            content_inside_pipe_stats_rt = await self._query(
                token=public_user_token,
                sql=f"select * from pipe_stats where user_id = '{self.WORKSPACE_ID}' order by date Format JSON",
            )

            self.assertEqual(
                {
                    "avg_duration_state": mock.ANY,
                    "billable": 1,
                    "date": matches(r"2\d+-\d+-\d+"),
                    "error_count": 0,
                    "pipe_id": "query_api",
                    "pipe_name": "query_api",
                    "quantile_timing_state": mock.ANY,
                    "read_bytes_sum": mock.ANY,
                    "read_rows_sum": 1,
                    "resource_tags": [],
                    "resource_tags_total": [],
                    "user_id": self.WORKSPACE_ID,
                    "view_count": 1,
                },
                content_inside_pipe_stats_rt["data"][0],
            )

        await poll_async(run_validation)


class TestAPIPipeEndpointCharts(BaseTest):
    def setUp(self):
        super().setUp()
        self.create_test_datasource()

    def tearDown(self):
        self._drop_token()
        super().tearDown()

    def _drop_token(self):
        try:
            u = Users.get_by_id(self.WORKSPACE_ID)
            token = Users.get_token(u, "test")
            if token:
                Users.drop_token(u, token)
        except Exception:
            pass

    async def _generate_pipe_and_chart(self, pipe_name, chart_name, token_name="test_charts_token"):
        u = Users.get_by_id(self.WORKSPACE_ID)
        pipe = await Users.add_pipe_async(
            u, pipe_name, edited_by=self.USER, sql="select 2 as visits, 'iphone' as device"
        )
        token = Users.add_token(u, token_name, scopes.ADMIN, self.USER_ID)
        node_id = pipe.pipeline.nodes[0].id
        await self.fetch_async(f"/v0/pipes/{pipe.name}/nodes/{node_id}/endpoint?token={token}", method="POST", body=b"")

        res = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/endpoint/charts?token={token}",
            method="POST",
            body=json.dumps({"type": "bar", "categories": ["visits"], "index": "device", "name": chart_name}),
        )

        return res

    @tornado.testing.gen_test
    async def test__create_chart(self):
        pipe_name = f"test_endpoint_{uuid.uuid4().hex}"
        chart_name = f"test_chart_{uuid.uuid4().hex}"
        response = await self._generate_pipe_and_chart(pipe_name, chart_name)
        result = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(result["name"], chart_name)
        self.assertEqual(result["type"], "bar")
        self.assertEqual(result["categories"], ["visits"])
        self.assertEqual(result["index"], "device")

    @tornado.testing.gen_test
    async def test__update_chart_name(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = f"test_charts_{uuid.uuid4().hex}"
        chart_name = f"test_chart_{uuid.uuid4().hex}"
        response = await self._generate_pipe_and_chart(pipe_name, chart_name)
        r = json.loads(response.body)

        params = {"token": token}
        new_chart_name = "new name"
        # update the chart name
        res = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/endpoint/charts/{r['id']}?{urlencode(params)}",
            method="PUT",
            body=json.dumps({"name": new_chart_name}),
        )

        self.assertEqual(res.code, 200)

        res = await self.fetch_async(f"/v0/pipes/{pipe_name}?{urlencode(params)}")
        data = json.loads(res.body)
        chart = data["endpoint_charts"][0]
        self.assertEqual(chart["name"], "new name")

    @tornado.testing.gen_test
    async def test_delete_chart(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = f"test_charts_{uuid.uuid4().hex}"
        chart_name = f"test_chart_{uuid.uuid4().hex}"
        response = await self._generate_pipe_and_chart(pipe_name, chart_name)
        chart = json.loads(response.body)
        params = {
            "token": token,
        }
        res = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/endpoint/charts/{chart['id']}?{urlencode(params)}", method="DELETE"
        )
        self.assertEqual(res.code, 204, res.body)


class TestPipeUtils(BaseTest):
    def setUp(self):
        super().setUp()
        self.tb_api_proxy_async = TBApiProxyAsync(self)

    @tornado.testing.gen_test
    @patch("tinybird.views.api_pipes.Users.check_dependent_nodes_by_materialized_node")
    async def test_delete_pipe_skip_checks_when_hard_delete(self, endpoint_check_mock: MagicMock):
        workspace = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(workspace, scopes.ADMIN)

        pipe_name = f"test_delete_pipe_{uuid.uuid4().hex}"
        await self.tb_api_proxy_async.create_pipe_endpoint(
            workspace, token, pipe_name, "select count() from numbers(1,10)"
        )
        pipe = Users.get_pipe(workspace, pipe_name)

        await PipeUtils.delete_pipe(workspace, pipe, None, edited_by=None, hard_delete=True)
        endpoint_check_mock.assert_called_once()  # Called during the endpoint creation only
