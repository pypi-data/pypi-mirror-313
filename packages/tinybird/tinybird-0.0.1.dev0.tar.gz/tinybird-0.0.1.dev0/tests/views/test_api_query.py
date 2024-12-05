import json
import re
import time
import uuid
from datetime import datetime
from functools import partial
from io import StringIO
from unittest.mock import patch
from urllib.parse import quote, urlencode

import pytest
import tornado
from chtoolset import query as chquery
from mock import Mock
from prometheus_client.parser import text_string_to_metric_families

from tests.conftest import DEFAULT_CLUSTER
from tests.utils import exec_sql, poll_async
from tests.views.base_test import AsyncMock, BaseTest, TBApiProxyAsync, create_test_datasource
from tinybird.ch import HTTPClient, UserAgents, ch_flush_logs_on_all_replicas
from tinybird.ch_utils.exceptions import CHException
from tinybird.constants import BillingPlans
from tinybird.csv_tools import csv_from_python_object
from tinybird.feature_flags import FeatureFlagWorkspaces
from tinybird.limits import Limit
from tinybird.model import retry_transaction_in_case_of_concurrent_edition_error_sync
from tinybird.pipe import PipeNode
from tinybird.token_scope import scopes
from tinybird.user import User, UserAccount, Users, public
from tinybird.views.base import INVALID_AUTH_MSG
from tinybird_shared.clickhouse.errors import CHErrors
from tinybird_shared.metrics.statsd_client import statsd_client


class TestAPIQuery(BaseTest):
    def setUp(self):
        super().setUp()
        self.create_test_datasource()

    async def __make_first_node_endpoint(self, pipe):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}/nodes/{pipe.pipeline.nodes[0].id}/endpoint?token={token}", method="POST", body=b""
        )
        self.assertEqual(response.code, 200, response.body)

    def test_non_auth_batch(self):
        self.check_non_auth_responses(["/v0/sql?q=select%201" "/v0/sql?q=select%201&token=fake"])

    @tornado.testing.gen_test
    async def test_auth(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)
        response = await self.fetch_async("/v0/sql?q=select%%201&token=%s" % token)
        self.assertEqual(response.body, b"1\n")
        self.assertEqual(response.code, 200)

    @tornado.testing.gen_test
    async def test_wrong_auth(self):
        token = b"random"
        response = await self.fetch_async("/v0/sql?q=select%%201&token=%s" % token)
        self.assertEqual(response.code, 403)
        result = json.loads(response.body)
        self.assertIn(INVALID_AUTH_MSG, result["error"])
        self.assertEqual(result["documentation"], "https://docs.tinybird.co/api-reference/overview#authentication")

    @tornado.testing.gen_test
    async def test_wrong_auth_with_post(self):
        body = json.dumps({"q": "select 1"})

        response = await self.fetch_async("/v0/sql", method="POST", body=body)

        self.assertEqual(response.code, 403)
        result = json.loads(response.body)
        self.assertEqual(result["error"], INVALID_AUTH_MSG)
        self.assertEqual(result["documentation"], "https://docs.tinybird.co/api-reference/overview#authentication")

    @tornado.testing.gen_test
    async def test_auth_read(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        datasource = Users.get_datasource(u, "test_table")
        token = Users.add_token(u, "test", scopes.DATASOURCES_READ, datasource.id)
        response = await self.fetch_async("/v0/sql?q=select+*+from+test_table&token=%s" % token)
        self.assertEqual(response.code, 200)

    @tornado.testing.gen_test
    async def test_auth_read_by_id(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        datasource = Users.get_datasource(u, "test_table")
        token = Users.add_token(u, "test", scopes.DATASOURCES_READ, datasource.id)
        response = await self.fetch_async("/v0/sql?q=select+*+from+%s&token=%s" % (datasource.id, token))
        self.assertEqual(response.code, 200)
        response = await self.fetch_async("/v0/sql?q=select+*+from+`%s`&token=%s" % (datasource.id, token))
        self.assertEqual(response.code, 200)

    @tornado.testing.gen_test
    async def test_auth_read_non_existing_datasource(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.DATASOURCES_READ, "test_table")
        response = await self.fetch_async("/v0/sql?q=select+*+from+test_table2&token=%s" % token)
        self.assertEqual(response.code, 403)
        result = json.loads(response.body)
        self.assertEqual(result["error"], "Resource 'test_table2' not found")

    @tornado.testing.gen_test
    async def test_auth_read_on_system_numbers(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.DATASOURCES_READ, "test_table")
        params = {
            "token": token,
            "q": "SELECT number FROM system.numbers LIMIT 10 FORMAT JSON",
        }
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertEqual(result["data"][0]["number"], 0)

    @tornado.testing.gen_test
    async def test_auth_read_on_system_tables(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.DATASOURCES_READ, "test_table")
        params = {
            "token": token,
            "q": "SELECT * FROM system.tables FORMAT JSON",
        }
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 403)
        result = json.loads(response.body)
        self.assertEqual(result["error"], """Resource 'system.tables' not found""")

    @tornado.testing.gen_test
    async def test_auth_read_on_numbers_table_function(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.DATASOURCES_READ, "test_table")
        params = {
            "token": token,
            "q": "SELECT number FROM numbers(10, 10) LIMIT 10 FORMAT JSON",
        }
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertEqual(result["data"][0]["number"], 10)

    @tornado.testing.gen_test
    async def test_auth_read_bad_token(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.DATASOURCES_APPEND, "test_table")
        response = await self.fetch_async("/v0/sql?q=select+*+from+test_table&token=%s" % token)
        self.assertEqual(response.code, 403)

    @tornado.testing.gen_test
    async def test_auth_read_service_data_sources_accessible_for_admins_even_under_a_pipe(self):
        u = Users.get_by_id(self.WORKSPACE_ID)

        pipe_name = "pipe_with_service_data_sources"
        pipe = Users.add_pipe_sync(u, pipe_name, "select * from tinybird.datasources_ops_log")

        await self.__make_first_node_endpoint(pipe)

        admin_token = Users.add_token(u, "test", scopes.ADMIN)

        response = await self.fetch_async(
            f"/v0/sql?q=select+count()+c+from+{pipe.name}+format+JSON&token={admin_token}"
        )
        self.assertEqual(response.code, 200, response.body)

    @tornado.testing.gen_test
    async def test_auth_read_service_data_sources_accessible_for_non_admins_if_it_is_under_a_pipe(self):
        u = Users.get_by_id(self.WORKSPACE_ID)

        pipe_name = "pipe_with_service_data_sources"
        pipe = Users.add_pipe_sync(u, pipe_name, "select * from tinybird.datasources_ops_log")

        await self.__make_first_node_endpoint(pipe)

        token = Users.add_token(u, "test_pipe_token", scopes.PIPES_READ, pipe.id)

        response = await self.fetch_async(f"/v0/sql?q=select+count()+c+from+{pipe.name}+format+JSON&token={token}")
        self.assertEqual(response.code, 200, response.body)

    @tornado.testing.gen_test
    async def test_auth_read_service_data_sources_not_accessible_for_non_admins(self):
        u = Users.get_by_id(self.WORKSPACE_ID)

        token = Users.add_token(
            u, "test_no_admin_token_with_unknown_resource", scopes.PIPES_READ, "not_existing_pipe_id"
        )

        response = await self.fetch_async(
            f"/v0/sql?q=select+count()+c+from+tinybird.datasources_ops_log+format+JSON&token={token}"
        )
        self.assertEqual(response.code, 403, response.body)
        result = json.loads(response.body)
        self.assertEqual(
            result["error"],
            "Services Data Sources like 'tinybird.datasources_ops_log' can't be directly accessed without an ADMIN token. If you need to access it with a non ADMIN token you can read it from a Pipe and create a token with just read access to that Pipe",
        )

    @tornado.testing.gen_test
    async def test_auth_read_service_data_sources_accessible_for_non_admins_if_included_as_readable_resource(self):
        u = Users.get_by_id(self.WORKSPACE_ID)

        token = Users.add_token(
            u, "test_non_admin_but_resource_in_token", scopes.DATASOURCES_READ, "tinybird.datasources_ops_log"
        )

        response = await self.fetch_async(
            f"/v0/sql?q=select+count()+c+from+tinybird.datasources_ops_log+format+JSON&token={token}"
        )
        self.assertEqual(response.code, 200, response.body)

    @tornado.testing.gen_test
    async def test_read_token_with_filter_applies_to_service_data_sources_as_well(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)

        pu = public.get_public_user()
        datasources_ops_log = pu.get_datasource("datasources_ops_log")

        filter_name = f"event_{uuid.uuid4().hex}"
        Users.add_scope_to_token(
            u,
            token,
            scopes.DATASOURCES_READ,
            f"{pu.database}.{datasources_ops_log.id}",
            filters=f"event_type == '{filter_name}'",
        )

        # Just add some random data to the DS to test that the filter is applied
        rows = [
            ["2000-01-01 00:00:00", "create", self.WORKSPACE_ID],
            ["2000-01-01 00:00:00", filter_name, self.WORKSPACE_ID],
            ["2000-01-01 00:00:00", filter_name, self.WORKSPACE_ID],
        ]

        client = HTTPClient(pu.database_server, database=pu.database)
        client.insert_chunk(
            f"INSERT INTO {datasources_ops_log.id} (timestamp, event_type, user_id) FORMAT CSV",
            csv_from_python_object(rows).encode("utf-8"),
        )
        self.wait_for_public_table_replication("datasources_ops_log")

        response = await self.fetch_async(
            "/v0/sql?q=select+count()+c+from+tinybird.datasources_ops_log+format+JSON&token=%s" % token
        )

        res = json.loads(response.body)
        row = res["data"][0]
        self.assertEqual(response.code, 200)
        self.assertEqual(int(row["c"]), 2)

    @tornado.testing.gen_test
    async def test_read_token_with_filter(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)
        datasource = Users.get_datasource(u, "test_table")
        Users.add_scope_to_token(u, token, scopes.DATASOURCES_READ, datasource.id, filters="a == 1")
        response = await self.fetch_async("/v0/sql?q=select+count()+c+from+test_table+format+JSON&token=%s" % token)

        res = json.loads(response.body)
        row = res["data"][0]
        self.assertEqual(response.code, 200)
        self.assertEqual(int(row["c"]), 1)

    @tornado.testing.gen_test
    async def test_read_quarantine_datasource(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        datasource = Users.get_datasource(u, "test_table")
        token = Users.add_token(u, "test", scopes.DATASOURCES_READ, datasource.id)
        response = await self.fetch_async("/v0/sql?q=select+*+from+test_table_quarantine&token=%s" % token)
        self.assertEqual(response.code, 200)

    @tornado.testing.gen_test
    async def test_read_token_with_complex_filter(self):
        """
        this query creates a new table that is joined with the test one having filters on both tables
        """
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)
        datasource = Users.get_datasource(u, "test_table")
        joined_datasource = Users.add_datasource_sync(u, "joined")
        create_test_datasource(u, joined_datasource)
        Users.add_scope_to_token(u, token, scopes.DATASOURCES_READ, datasource.id, filters="a < 4")
        Users.add_scope_to_token(u, token, scopes.DATASOURCES_READ, joined_datasource.id, filters="b > 3.0")
        response = await self.fetch_async(
            "/v0/sql?q=select+count()+c+from+test_table+inner+join+joined+using+a+format+JSON&token=%s" % token
        )

        self.assertEqual(response.code, 200)
        res = json.loads(response.body)
        row = res["data"][0]
        self.assertEqual(int(row["c"]), 1)

    @tornado.testing.gen_test
    async def test_read_pipe_wrong_token(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        pipe = Users.get_pipe(u, "test_pipe")
        _ = Users.add_pipe_sync(u, "test_pipe_2", "select * from test_table")
        token = Users.add_token(u, "test", scopes.PIPES_READ, pipe.id)

        response = await self.fetch_async("/v0/sql?q=select+count()+c+from+test_pipe_2+JSON&token=%s" % token)

        self.assertEqual(response.code, 403)
        res = json.loads(response.body)
        self.assertRegex(res["error"], r"^Not enough permissions for pipe 'test_pipe_2'")

    @tornado.testing.gen_test
    async def test_read_pipe_no_endpoint(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        pipe = Users.get_pipe(u, "test_pipe")
        token = Users.add_token(u, "test", scopes.PIPES_READ, pipe.id)
        response = await self.fetch_async(f"/v0/sql?q=select+count()+c+from+{pipe.name}+format+JSON&token={token}")
        self.assertEqual(response.code, 400)
        payload = json.loads(response.body)
        self.assertEqual(payload["error"], f"The pipe '{pipe.name}' does not have an endpoint yet")

    @tornado.testing.gen_test
    async def test_read_pipe(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        pipe = Users.get_pipe(u, "test_pipe")
        await self.__make_first_node_endpoint(pipe)  # Make the pipe available by defining its endpoint
        token = Users.add_token(u, "test", scopes.PIPES_READ, pipe.id)
        response = await self.fetch_async(f"/v0/sql?q=select+count()+c+from+{pipe.name}+format+JSON&token={token}")
        self.assertEqual(response.code, 200)
        res = json.loads(response.body)
        row = res["data"][0]
        self.assertEqual(int(row["c"]), 6)

    @tornado.testing.gen_test
    async def test_read_pipe_with_syntax_error_on_node(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        pipe_name = "syntax_error_settings_pipe"
        pipe = Users.add_pipe_sync(u, pipe_name, "SELECT 1")

        wrong_node_name = f"{pipe_name}_n1"
        pipe.append_node(
            PipeNode(wrong_node_name, "% SELECT * FROM test_table WHERE a = toInt32OrZero({{%String(n, 1)}})")
        )

        endpoint_node_name = f"{pipe_name}_n2"
        pipe.append_node(PipeNode(endpoint_node_name, f"SELECT * FROM {wrong_node_name}"))
        pipe.endpoint = endpoint_node_name

        Users.update_pipe(u, pipe)
        token = Users.add_token(u, f"{pipe_name}_token", scopes.PIPES_READ, pipe.id)

        response = await self.fetch_async(f"/v0/sql?q=select+*+from+{pipe_name}&pipeline={pipe_name}&token={token}")
        self.assertEqual(response.code, 400)
        body = json.loads(response.body)
        self.assertEqual(
            body.get("error"), f"Syntax error: invalid syntax (in node '{wrong_node_name}' from pipe '{pipe_name}')"
        )

        response = await self.fetch_async(f"/v0/sql?q=select+*+from+{pipe_name}&token={token}")
        self.assertEqual(response.code, 400)
        body = json.loads(response.body)
        self.assertEqual(
            body.get("error"), f"Syntax error: invalid syntax (in node '{wrong_node_name}' from pipe '{pipe_name}')"
        )

    @tornado.testing.gen_test
    async def test_read_pipe_spans_associated_to_query_log(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        pipe = Users.get_pipe(u, "test_pipe")
        await self.__make_first_node_endpoint(pipe)  # Make the pipe available by defining its endpoint
        pipe = Users.get_pipe(u, "test_pipe")
        token = Users.add_token(u, "test", scopes.PIPES_READ, pipe.id)
        url = f"/v0/sql?q=select+count()+c+from+{pipe.name}+format+JSON&token={token}"
        response = await self.fetch_async(url)
        self.assertEqual(response.code, 200)
        span = await self.get_span_async(url)
        requests_tags = json.loads(span["tags"])
        self.assertEqual(requests_tags["result_rows"], "1", span)

        query_id = span["span_id"]
        query_logs = await self.get_query_logs_async(query_id, u.database)
        self.assertEqual(len(query_logs), 2)
        expected_query = f"SELECT count() AS c FROM (SELECT * FROM {u.database}.{self.datasource.id} AS test_table) as {pipe.name} FORMAT JSON"
        for query_log in query_logs:
            self.assertEqual(chquery.format(query_log["query"]), chquery.format(expected_query))

    @tornado.testing.gen_test
    async def test_read_pipes_with_nodes_with_same_name(self):
        """
        test the case where two pipes have a node with the same name
        """
        u = Users.get_by_id(self.WORKSPACE_ID)

        pipe1 = Users.add_pipe_sync(u, "test_pipe_same_name_1", "select 0 as a")
        pipe2 = Users.add_pipe_sync(u, "test_pipe_same_name_2", "select 0 as a")

        pipe1.append_node(PipeNode("nn", "select 1 as a"))
        pipe2.append_node(PipeNode("nn", "select 2 as a"))
        pipe1.endpoint = "nn"
        pipe2.endpoint = "nn"

        Users.update_pipe(u, pipe1)
        Users.update_pipe(u, pipe2)

        token = Users.add_token(u, "test", scopes.PIPES_READ, pipe1.id)
        Users.add_scope_to_token(u, token, scopes.PIPES_READ, pipe2.id)

        response = await self.fetch_async(f"/v0/sql?q=select+*+from+test_pipe_same_name_1+format+JSON&token={token}")
        self.assertEqual(response.code, 200)
        res = json.loads(response.body)
        row = res["data"][0]
        self.assertEqual(int(row["a"]), 1)

        response = await self.fetch_async(f"/v0/sql?q=select+*+from+test_pipe_same_name_2+format+JSON&token={token}")
        self.assertEqual(response.code, 200)
        res = json.loads(response.body)
        row = res["data"][0]
        self.assertEqual(int(row["a"]), 2)

        pipe2.append_node(
            PipeNode("last_node", "with (select * from nn) as rambo select rambo,* from test_pipe_same_name_1")
        )

        pipe2.endpoint = "last_node"
        Users.update_pipe(u, pipe2)
        response = await self.fetch_async(f"/v0/sql?q=select+*+from+test_pipe_same_name_2+format+JSON&token={token}")
        self.assertEqual(response.code, 200)
        res = json.loads(response.body)
        row = res["data"][0]
        self.assertEqual(int(row["a"]), 1)
        self.assertEqual(int(row["rambo"]), 2)

    @tornado.testing.gen_test
    async def test_read_pipe_and_datasource(self):
        """
        even if the query has access to test_table through test_pipe query
        should not allow to read data from test_table if there are no
        explicit permissions
        """
        u = Users.get_by_id(self.WORKSPACE_ID)
        pipe = Users.get_pipe(u, "test_pipe")
        await self.__make_first_node_endpoint(pipe)  # Make the pipe available by defining its endpoint

        token = Users.add_token(u, "test", scopes.PIPES_READ, pipe.id)
        response = await self.fetch_async(
            "/v0/sql?q=select+count()+c+from+test_pipe+union+all+select+*+from+test_table+format+JSON&token=%s" % token
        )

        self.assertEqual(response.code, 403)

    @tornado.testing.gen_test
    async def test_read_pipe_with_settings(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        pipe = Users.add_pipe_sync(u, "settings_pipe", "SELECT 1")
        pipe.append_node(
            PipeNode("n1", "SELECT sum(a) as total FROM test_table WHERE c = 'Not Present' SETTINGS join_use_nulls=1")
        )
        pipe.endpoint = "n1"
        Users.update_pipe(u, pipe)
        token = Users.add_token(u, "test", scopes.PIPES_READ, pipe.id)
        response = await self.fetch_async(
            f"/v0/sql?q=select+*+from+settings_pipe+SETTINGS+aggregate_functions_null_for_empty%3D0+format+JSON&token={token}"
        )
        self.assertEqual(response.code, 200)
        body = json.loads(response.body)
        self.assertEqual(body["data"][0]["total"], 0, response.body.decode("utf-8"))

        response = await self.fetch_async(
            f"/v0/sql?q=select+*+from+settings_pipe+SETTINGS+aggregate_functions_null_for_empty%3D1+format+JSON&token={token}"
        )
        self.assertEqual(response.code, 200)
        body = json.loads(response.body)
        self.assertEqual(body["data"][0]["total"], None, response.body.decode("utf-8"))  # null is transformed to None

    @tornado.testing.gen_test
    async def test_read_pipe_and_datasource_with_access(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        pipe = Users.get_pipe(u, "test_pipe")
        await self.__make_first_node_endpoint(pipe)  # Make the pipe available by defining its endpoint

        datasource = Users.get_datasource(u, "test_table")
        token = Users.add_token(u, "test", scopes.PIPES_READ, pipe.id)
        Users.add_scope_to_token(u, token, scopes.DATASOURCES_READ, datasource.id)
        response = await self.fetch_async(
            "/v0/sql?q=select+count()+c+from+test_pipe+union+all+select+count()+from+test_table+format+JSON&token=%s"
            % token
        )

        self.assertEqual(response.code, 200)
        res = json.loads(response.body)
        row = res["data"][0]
        self.assertEqual(int(row["c"]), 6)
        row = res["data"][1]
        self.assertEqual(int(row["c"]), 6)

    @tornado.testing.gen_test
    async def test_read_pipe_no_endpoint_and_datasource_with_access(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        pipe = Users.get_pipe(u, "test_pipe")
        datasource = Users.get_datasource(u, "test_table")
        token = Users.add_token(u, "test", scopes.PIPES_READ, pipe.id)
        Users.add_scope_to_token(u, token, scopes.DATASOURCES_READ, datasource.id)
        response = await self.fetch_async(
            f"/v0/sql?q=select+count()+c+from+{pipe.id}+union+all+select+count()+from+test_table+format+JSON&token={token}"
        )
        self.assertEqual(response.code, 400)
        payload = json.loads(response.body)
        self.assertEqual(payload["error"], f"The pipe '{pipe.name}' does not have an endpoint yet")

    @tornado.testing.gen_test
    async def test_read_pipe_and_datasource_with_filters_on_datasource(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        pipe = Users.get_pipe(u, "test_pipe")
        await self.__make_first_node_endpoint(pipe)  # Make the pipe available by defining its endpoint

        datasource = Users.get_datasource(u, "test_table")
        token = Users.add_token(u, "test", scopes.PIPES_READ, pipe.id)
        Users.add_scope_to_token(u, token, scopes.DATASOURCES_READ, datasource.id, filters="a == 1")
        response = await self.fetch_async(
            "/v0/sql?q=select+count()+c+from+test_pipe+union+all+select+count()+from+test_table+format+JSON&token=%s"
            % token
        )

        self.assertEqual(response.code, 200)
        res = json.loads(response.body)
        row = res["data"][0]
        self.assertEqual(int(row["c"]), 1)
        row = res["data"][1]
        self.assertEqual(int(row["c"]), 1)

    @tornado.testing.gen_test
    async def test_read_pipe_and_datasource_with_filters_on_pipe(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        pipe = Users.get_pipe(u, "test_pipe")
        await self.__make_first_node_endpoint(pipe)  # Make the pipe available by defining its endpoint
        datasource = Users.get_datasource(u, "test_table")
        token = Users.add_token(u, "test", scopes.DATASOURCES_READ, datasource.id)
        Users.add_scope_to_token(u, token, scopes.PIPES_READ, pipe.id, filters="a == 1")
        query = """select * from (
            select count() c, 0 as n
            from test_pipe
            union all
            select count(), 1 as n
            from test_table
        ) order by n format JSON
        """
        response = await self.fetch_async("/v0/sql?q=%s&token=%s" % (quote(query, safe=""), token))

        self.assertEqual(response.code, 200)
        res = json.loads(response.body)
        row = res["data"][0]
        self.assertEqual(int(row["c"]), 1)
        row = res["data"][1]
        self.assertEqual(int(row["c"]), 6)

    @tornado.testing.gen_test
    async def test_admin_accessing_other_database(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)
        response = await self.fetch_async("/v0/sql?q=select+*+from+system.parts&token=%s" % token)
        result = json.loads(response.body)
        self.assertEqual(response.code, 403)
        self.assertTrue("error" in result)
        self.assertEqual(result["error"], "Resource 'system.parts' not found")

    @tornado.testing.gen_test
    async def test_allowed_table_functions_from_ui(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)

        @retry_transaction_in_case_of_concurrent_edition_error_sync()
        def set_user_limit(u: User):
            with User.transaction(u.id) as workspace:
                workspace.set_user_limit("allowed_table_functions", "url", "workspace")

        set_user_limit(u)

        query = """SELECT * FROM url('https://storage.googleapis.com/tinybird-demo/stock_prices_h.csv', CSV) LIMIT 1"""
        response = await self.fetch_async(f"/v0/sql?q={quote(query, '')}&token={token}&from=ui")
        self.assertEqual(response.code, 200)

    @tornado.testing.gen_test
    async def test_restricted_table_functions(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)
        query = """SELECT * FROM url('http://localhost:8123/?query=select+1+FORMAT+CSV', CSV, 'n Int64')"""
        response = await self.fetch_async(f"/v0/sql?q={quote(query, '')}&token={token}")
        result = json.loads(response.body)
        self.assertEqual(response.code, 403)
        self.assertTrue("error" in result)
        self.assertTrue(
            "The url table function is only allowed in Copy Pipes" in result["error"],
        )

        query = """SELECT * from db.numbers"""
        response = await self.fetch_async(f"/v0/sql?q={quote(query, '')}&token={token}")
        result = json.loads(response.body)
        self.assertEqual(response.code, 403)
        self.assertTrue("error" in result)
        self.assertEqual(result["error"], "Resource 'db.numbers' not found")

        query = """SELECT * FROM generateRandom('a Int8, c String', 0, 5) LIMIT 3 FORMAT JSON"""
        response = await self.fetch_async(f"/v0/sql?q={quote(query, '')}&token={token}")
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertEqual(len(result["data"]), 3)
        self.assertTrue("a" in result["data"][0])
        self.assertTrue("c" in result["data"][0])

    @tornado.testing.gen_test
    async def test_invalid_sql_not_as_resource_not_found(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.DATASOURCES_READ, "test_table")
        params = {
            "token": token,
            "q": "SELECT * FROM test_table)",
        }
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400)
        result = json.loads(response.body)
        self.assertEqual(
            result["error"], "DB::Exception: Syntax error: failed at position 25 (')'): ). Unmatched parentheses: )"
        )

    @tornado.testing.gen_test
    async def test_gzip_encoding(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)
        response = await self.fetch_async(
            "/v0/sql?q=select+1&token=%s" % token, headers={"accept-encoding": "gzip"}, decompress_response=False
        )

        self.assertEqual(response.code, 200)
        self.assertEqual(response.headers["Content-Encoding"], "gzip")
        response = await self.fetch_async("/v0/sql?q=select+1&token=%s" % token, headers={"accept-encoding": ""})
        self.assertEqual(response.code, 200)
        self.assertEqual(response.headers.get("Content-Encoding", None), None)

    @tornado.testing.gen_test
    async def test_post_query_request(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)
        response = await self.fetch_async(f"/v0/sql?token={token}", method="POST", body="SELECT 1 FORMAT JSON")
        self.assertEqual(response.code, 200)

    @tornado.testing.gen_test
    async def test_post_query_request_spans_with_query_id(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)
        url = f"/v0/sql?token={token}"
        response = await self.fetch_async(url, method="POST", body="SELECT 1 FORMAT JSON")
        self.assertEqual(response.code, 200)
        span = await self.get_span_async(url)
        requests_tags = json.loads(span["tags"])
        self.assertEqual(requests_tags["result_rows"], "1", span)

        query_id = span["span_id"]
        query_logs = await self.get_query_logs_async(query_id, u.database)
        self.assertEqual(len(query_logs), 2)
        for query_log in query_logs:
            self.assertIn("SELECT 1 FORMAT JSON", query_log["query"])

    @tornado.testing.gen_test
    async def test_post_query_request_with_params(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)
        response = await self.fetch_async(
            f"/v0/sql?token={token}", method="POST", body="%SELECT {{String('s', 'wadus')}} as a FORMAT JSON"
        )
        self.assertEqual(response.code, 200, response.body)

    @tornado.testing.gen_test
    async def test_get_query_request_with_quoted_default_param(self):
        tb_api_proxy_async = TBApiProxyAsync(self)

        workspace = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(workspace, "test", scopes.ADMIN)

        datasource_name = "datasource_with_quoted_data_in_columns"
        datasource_response = await tb_api_proxy_async.create_datasource(
            token=token, ds_name=datasource_name, schema="a Int32,text String"
        )

        await self._insert_data_in_datasource(
            token=token, ds_name=datasource_name, data='1,action."test run"\n2,no quotes'
        )

        self.wait_for_datasource_replication(workspace, datasource_response.get("datasource"))

        result = await self._query(
            token=token,
            sql=f"""
            %
            SELECT * FROM {datasource_name} WHERE text={{{{String(text, 'action."test run"')}}}} Format JSON
            """,
        )

        self.assertEqual(result["data"], [{"a": 1, "text": 'action."test run"'}])

    @tornado.testing.gen_test
    async def test_get_query_request_with_template_params(self):
        tb_api_proxy_async = TBApiProxyAsync(self)

        workspace = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(workspace, "test", scopes.ADMIN)

        datasource_name = "test_get_query_request_with_template_params"
        datasource_response = await tb_api_proxy_async.create_datasource(
            token=token, ds_name=datasource_name, schema="a Int32,text String"
        )

        await self._insert_data_in_datasource(
            token=token, ds_name=datasource_name, data='1,action."test run"\n2,no quotes'
        )

        self.wait_for_datasource_replication(workspace, datasource_response.get("datasource"))

        extra_params = {"template_parameters": json.dumps({"text": 'action."test run"'})}

        result = await self._query(
            token=token,
            sql=f"""
            %
            SELECT * FROM {datasource_name} WHERE text={{{{String(text)}}}} Format JSON
            """,
            extra_params=extra_params,
        )

        self.assertEqual(result["data"], [{"a": 1, "text": 'action."test run"'}])

    @tornado.testing.gen_test
    async def test_post_query_request_with_template_params(self):
        tb_api_proxy_async = TBApiProxyAsync(self)

        workspace = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(workspace, "test", scopes.ADMIN)

        datasource_name = "test_post_query_request_with_template_params"
        datasource_response = await tb_api_proxy_async.create_datasource(
            token=token, ds_name=datasource_name, schema="a Int32,text String"
        )

        await self._insert_data_in_datasource(
            token=token, ds_name=datasource_name, data='1,action."test run"\n2,no quotes'
        )

        self.wait_for_datasource_replication(workspace, datasource_response.get("datasource"))

        params = {"token": token, "template_parameters": json.dumps({"text": 'action."test run"'})}

        result = await self.fetch_async(
            f"/v0/sql?{urlencode(params)}",
            method="POST",
            body=f"""
                %
                SELECT * FROM {datasource_name} WHERE text={{{{String(text)}}}} Format JSON
            """,
        )

        result_body = json.loads(result.body)
        self.assertEqual(result_body["data"], [{"a": 1, "text": 'action."test run"'}])

    @tornado.testing.gen_test
    async def test_get_query_request_with_invalid_template_params(self):
        workspace = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(workspace, "test", scopes.ADMIN)

        params = {
            "token": token,
            "template_parameters": "invalid params",
            "q": """
                %
                SELECT * FROM fake_table WHERE text={{String(text)}} Format JSON
            """,
        }

        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")

        self.assertEqual(response.code, 400)
        self.assertEqual(
            response.body.decode("utf-8"),
            '{"error": "template_parameters must be a well-formed JSON", '
            '"documentation": "https://docs.tinybird.co/api-reference/query-api.html#get--v0-sql"}',
        )

    @tornado.testing.gen_test
    async def test_post_query_request_with_invalid_template_params(self):
        workspace = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(workspace, "test", scopes.ADMIN)

        params = {"token": token, "template_parameters": "invalid params"}

        response = await self.fetch_async(
            f"/v0/sql?{urlencode(params)}",
            method="POST",
            body="""
                %
                SELECT * FROM fake_table WHERE text={{String(text)}} Format JSON
            """,
        )

        self.assertEqual(response.code, 400)
        self.assertEqual(
            response.body.decode("utf-8"),
            '{"error": "template_parameters must be a well-formed JSON", '
            '"documentation": "https://docs.tinybird.co/api-reference/query-api.html#post--v0-sql"}',
        )

    @tornado.testing.gen_test
    async def test_post_query_request_with_restricted_template_params(self):
        tb_api_proxy_async = TBApiProxyAsync(self)

        workspace = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(workspace, "test", scopes.ADMIN)

        datasource_name = "test_post_query_request_with_restricted_template_params"
        datasource_response = await tb_api_proxy_async.create_datasource(
            token=token, ds_name=datasource_name, schema="a Int32,text String, text2 String"
        )

        await self._insert_data_in_datasource(
            token=token, ds_name=datasource_name, data='1,action."test run",action."test run"\n2,no quotes,no quotes'
        )

        self.wait_for_datasource_replication(workspace, datasource_response.get("datasource"))

        params = {"token": token, "template_parameters": json.dumps({"pipeline": 'action."test run"'})}
        result = await self.fetch_async(
            f"/v0/sql?{urlencode(params)}",
            method="POST",
            body=f"""
                %
                SELECT * FROM {datasource_name} WHERE text={{{{String(pipeline)}}}} Format JSON
            """,
        )

        result_body = json.loads(result.body)
        self.assertEqual(
            result.headers["X-Tb-Warning"],
            '["The parameter name \\"pipeline\\" is a reserved word. Please, choose another name or the pipe will not work as expected."]',
        )
        self.assertEqual(result_body["data"], [{"a": 1, "text": 'action."test run"', "text2": 'action."test run"'}])

        params = {
            "token": token,
            "template_parameters": json.dumps({"pipeline": 'action."test run"', "playground": 'action."test run"'}),
        }
        result = await self.fetch_async(
            f"/v0/sql?{urlencode(params)}",
            method="POST",
            body=f"""
                %
                SELECT * FROM {datasource_name} WHERE text={{{{String(pipeline)}}}} AND text2={{{{String(playground)}}}} Format JSON
            """,
        )

        result_body = json.loads(result.body)
        self.assertEqual(
            result.headers["X-Tb-Warning"],
            '["The parameter names \\"pipeline\\" and \\"playground\\" are reserved words. Please, choose another name or the pipe will not work as expected."]',
        )
        self.assertEqual(result_body["data"], [{"a": 1, "text": 'action."test run"', "text2": 'action."test run"'}])

    @tornado.testing.gen_test
    async def test_post_query_request_with_empty_body(self):
        workspace = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(workspace, "test", scopes.ADMIN)

        params = {"token": token}

        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}", method="POST", body="")

        self.assertEqual(response.code, 400)
        self.assertEqual(
            response.body.decode("utf-8"),
            '{"error": "The request body should contain a query", '
            '"documentation": "https://docs.tinybird.co/api-reference/query-api.html#post--v0-sql"}',
        )

    @tornado.testing.gen_test
    async def test_large_query(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)
        sql = f"select sum(arrayJoin([{','.join([str(x) for x in range(1500)])}]))"
        params = {"token": token, "q": sql}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(int(response.body), 1124250)

    @tornado.testing.gen_test
    async def test_large_query_avoid_insert(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)
        sql = f"create table testing engine=Log as select arrayJoin([{','.join([str(x) for x in range(300)])}])"
        params = {"token": token, "q": sql}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400, response.body)
        self.assertEqual(
            response.body.decode("utf-8"),
            '{"error": "DB::Exception: Only SELECT or DESCRIBE queries are supported. Got: CreateQuery", '
            '"documentation": "https://docs.tinybird.co/query/query-parameters.html"}',
        )

    @tornado.testing.gen_test
    async def test_avoid_show_commands(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)

        async def _check_query(sql):
            params = {"token": token, "q": sql}
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            self.assertEqual(response.code, 400, response.body)
            res = json.loads(response.body.decode("utf-8"))
            self.assertEqual(res["documentation"], "https://docs.tinybird.co/query/query-parameters.html")
            self.assertRegex(res["error"], "DB::Exception: Only SELECT or DESCRIBE queries are supported. Got: *")

        await _check_query("show tables")
        await _check_query("    show processlist")
        await _check_query("\tset max_block_size = 0")
        await _check_query("\nshow processlist")

    @tornado.testing.gen_test
    async def test_read_pipe_node_with_comments(self):
        u = Users.get_by_id(self.WORKSPACE_ID)

        pipe_name = "pipe_with_comments"
        pipe = Users.add_pipe_sync(u, pipe_name, "select * from numbers(10) --limit 1")
        n0 = pipe.pipeline.nodes[0]
        pipe.append_node(PipeNode("t", f"SELECT count() as total FROM {n0.name}"))
        pipe.endpoint = "t"
        Users.update_pipe(u, pipe)

        token = Users.add_token(u, "test_pipe_token", scopes.PIPES_READ, pipe.id)

        query = "SELECT * FROM _ format JSON"
        params = {
            "token": token,
            "q": query,
            "pipeline": pipe_name,
        }
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)
        res = json.loads(response.body)
        self.assertEqual(res["data"], [{"total": 10}])

    @tornado.testing.gen_test
    async def test_read_pipe_no_read_on_nodes(self):
        u = Users.get_by_id(self.WORKSPACE_ID)

        pipe_name = "pipe_with_endpoint"
        pipe = Users.add_pipe_sync(u, pipe_name, "select * from test_table")
        n0 = pipe.pipeline.nodes[0]
        pipe.append_node(PipeNode("t", f"SELECT c, count() as total FROM {n0.name} GROUP BY c"))
        pipe.endpoint = "t"
        Users.update_pipe(u, pipe)

        token = Users.add_token(u, "test_pipe_token", scopes.PIPES_READ, pipe.id)

        query = "SELECT * FROM _ WHERE c = 'test' format JSON"
        params = {
            "token": token,
            "q": query,
            "pipeline": pipe_name,
        }
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)
        res = json.loads(response.body)
        self.assertEqual(res["data"], [{"c": "test", "total": 2}])

        query = f"SELECT * FROM {n0.name} WHERE c = 'test' format JSON"
        params = {
            "token": token,
            "q": query,
            "pipeline": pipe_name,
        }
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 403, response.body)

    @tornado.testing.gen_test
    async def test_read_pipe_validates_pipename(self):
        u = Users.get_by_id(self.WORKSPACE_ID)

        pipe_name = "pipe_with_endpoint"
        pipe = Users.add_pipe_sync(u, pipe_name, "select * from test_table")
        n0 = pipe.pipeline.nodes[0]
        pipe.append_node(PipeNode("t", f"SELECT c, count() as total FROM {n0.name} GROUP BY c"))
        pipe.endpoint = "t"
        Users.update_pipe(u, pipe)

        token = Users.add_token(u, "test_pipe_token", scopes.PIPES_READ, pipe.id)

        query = "SELECT * FROM _ WHERE c = 'test' format JSON"
        params = {
            "token": token,
            "q": query,
            "pipeline": "random_pipe_name",
        }
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 403, response.body)
        res = json.loads(response.body)
        self.assertEqual(res["error"], "Resource 'random_pipe_name' not found")

    @tornado.testing.gen_test
    async def test_read_pipe_validates_pipeline(self):
        u = Users.get_by_id(self.WORKSPACE_ID)

        pipe_name = "pipe_with_endpoint"
        pipe = Users.add_pipe_sync(u, pipe_name, "select * from test_table")
        n0 = pipe.pipeline.nodes[0]
        pipe.append_node(PipeNode("t", f"SELECT c, count() as total FROM {n0.name} GROUP BY c"))
        pipe.endpoint = "t"
        Users.update_pipe(u, pipe)

        token = Users.add_token(u, "test_pipe_token", scopes.PIPES_READ, pipe.id)

        query = "SELECT * FROM pipe_with_endpoint WHERE c = 'test' format JSON"
        params = {
            "token": token,
            "q": query,
            "pipeline": "random_pipe_name",
        }
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 403, response.body)
        res = json.loads(response.body)
        self.assertEqual(res["error"], "Resource 'random_pipe_name' not found")

    @tornado.testing.gen_test
    async def test_regression_missing_variables(self):
        u = Users.get_by_id(self.WORKSPACE_ID)

        pipe_name = "pipe_with_params"
        pipe = Users.add_pipe_sync(
            u,
            pipe_name,
            """%
            SELECT sum(a) sum_a, count() as count
            FROM test_table
            WHERE c = {{String(category, 'one')}}
        """,
        )
        n0 = pipe.pipeline.nodes[0]
        pipe.endpoint = n0.id
        Users.update_pipe(u, pipe)

        admin_token = Users.add_token(u, "test", scopes.ADMIN)
        pipe_token = Users.add_token(u, "pipe_with_params", scopes.PIPES_READ, pipe.id)

        async def assert_pipe_with_token(token, category, expected_result):
            params = {
                "token": token,
                "pipeline": pipe_name,
            }
            if category:
                params["category"] = category
            response = await self.fetch_async(f"/v0/pipes/{pipe.name}.json?{urlencode(params)}")
            self.assertEqual(response.code, 200, response.body)
            res = json.loads(response.body)
            self.assertEqual(res["data"], [expected_result])

        for t in [admin_token, pipe_token]:
            await assert_pipe_with_token(t, None, {"sum_a": 1, "count": 1})
            await assert_pipe_with_token(t, "four", {"sum_a": 4, "count": 1})
            await assert_pipe_with_token(t, "test", {"sum_a": 100, "count": 2})

    @tornado.testing.gen_test
    async def test_user_agent_sent_to_ch(self):
        u = Users.get_by_id(self.WORKSPACE_ID)

        pipe_name = "pipe_from_ui"
        pipe = Users.add_pipe_sync(u, pipe_name, "select * from test_table")
        n0 = pipe.pipeline.nodes[0]
        pipe.endpoint = n0.id
        Users.update_pipe(u, pipe)

        token = Users.add_token(u, "test_pipe_ui_token", scopes.PIPES_READ, pipe.id)

        headers = {"content-type": "application/json"}

        with patch.object(HTTPClient, "query", return_value=(headers, b"")) as client_query:
            params = {"token": token}

            await self.fetch_async(f"/v0/pipes/{pipe.name}.json?{urlencode(params)}")
            _, kwargs = client_query.call_args
            self.assertEqual(kwargs.get("user_agent"), UserAgents.API_QUERY.value)

        with patch.object(HTTPClient, "query", return_value=(headers, b"")) as client_query:
            params = {"token": token, "q": f"select * from {pipe_name} FORMAT JSON"}

            await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            _, kwargs = client_query.call_args
            self.assertEqual(kwargs.get("user_agent"), UserAgents.API_QUERY.value)

        with patch.object(HTTPClient, "query", return_value=(headers, b"")) as client_query:
            params = {"token": token, "from": "ui"}
            await self.fetch_async(f"/v0/pipes/{pipe.name}.json?{urlencode(params)}")
            _, kwargs = client_query.call_args
            self.assertEqual(kwargs.get("user_agent"), "tb-ui-query")

        with patch.object(HTTPClient, "query", return_value=(headers, b"")) as client_query:
            params = {"token": token, "q": f"select * from {pipe_name} FORMAT JSON", "from": "ui"}

            await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            _, kwargs = client_query.call_args
            self.assertEqual(kwargs.get("user_agent"), "tb-ui-query")

        with patch.object(HTTPClient, "query", return_value=(headers, b"")) as client_query:
            params = {"token": token, "from": "karman"}
            await self.fetch_async(f"/v0/pipes/{pipe.name}.json?{urlencode(params)}")
            _, kwargs = client_query.call_args
            self.assertEqual(kwargs.get("user_agent"), "tb-karman-query")

        with patch.object(HTTPClient, "query", return_value=(headers, b"")) as client_query:
            params = {"token": token, "q": f"select * from {pipe_name} FORMAT JSON", "from": "karman"}

            await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            _, kwargs = client_query.call_args
            self.assertEqual(kwargs.get("user_agent"), "tb-karman-query")

        with patch.object(HTTPClient, "query", return_value=(headers, b"")) as client_query:
            params = {"token": token, "from": "karman"}

            await self.fetch_async(
                f"/v0/sql?{urlencode(params)}", body=f"select * from {pipe_name} FORMAT JSON", method="POST"
            )
            _, kwargs = client_query.call_args
            self.assertEqual(kwargs.get("user_agent"), "tb-karman-query")

        with patch.object(HTTPClient, "query", return_value=(headers, b"")) as client_query:
            params = {"token": token, "from": "ui"}

            await self.fetch_async(
                f"/v0/sql?{urlencode(params)}", body=f"select * from {pipe_name} FORMAT JSON", method="POST"
            )
            _, kwargs = client_query.call_args
            self.assertEqual(kwargs.get("user_agent"), "tb-ui-query")

    @tornado.testing.gen_test
    async def test_output_format_json(self):
        # We check if it returns a string or a number, since this json library
        # parses the value correctly

        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)

        query = """%
            select 123456789123456789 as output FORMAT JSON
        """
        params = {"token": token, "q": query}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        res = json.loads(response.body)
        self.assertEqual(res["data"][0]["output"], 123456789123456789)

        query = """%
            select 123456789123456789 as output FORMAT JSON
        """
        params = {"token": token, "q": query, "output_format_json_quote_64bit_integers": 1}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        res = json.loads(response.body)
        self.assertEqual(res["data"][0]["output"], "123456789123456789")

    @tornado.testing.gen_test
    async def test_output_format_json_quote_64bit_integers_through_post(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)

        query = """%
            select 123456789123456789 as output FORMAT JSON
        """
        params = {"token": token, "q": query}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        res = json.loads(response.body)
        self.assertEqual(res["data"][0]["output"], 123456789123456789)

        query = """%
            select 123456789123456789 as output FORMAT JSON
        """
        params = {"token": token, "output_format_json_quote_64bit_integers": 1}
        response = await self.fetch_async(path=f"/v0/sql?{urlencode(params)}", method="POST", body=query)
        res = json.loads(response.body)
        self.assertEqual(res["data"][0]["output"], "123456789123456789")

    @tornado.testing.gen_test
    async def test_output_format_parquet(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)

        query = """%
            select '123456789123456789' as output FORMAT JSON
        """
        params = {"token": token, "q": query}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        res = json.loads(response.body)
        self.assertEqual(res["data"][0]["output"], "123456789123456789")

        query = """%
            select '123456789123456789' as output FORMAT Parquet
        """
        params = {"token": token, "q": query, "output_format_parquet_string_as_string": 1}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")

        params = {"token": token, "q": query, "output_format_parquet_string_as_string": 0}
        response2 = await self.fetch_async(f"/v0/sql?{urlencode(params)}")

        # just assert the param produces different output
        self.assertNotEqual(len(response.body), len(response2.body))

    @tornado.testing.gen_test
    async def test_output_format_parquet_string_as_string_through_post(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)

        query = """%
            select '123456789123456789' as output FORMAT Parquet
        """
        params = {"token": token, "output_format_parquet_string_as_string": 1}
        response = await self.fetch_async(path=f"/v0/sql?{urlencode(params)}", method="POST", body=query)

        params = {"token": token, "output_format_parquet_string_as_string": 0}
        response2 = await self.fetch_async(path=f"/v0/sql?{urlencode(params)}", method="POST", body=query)

        # just assert the param produces different output
        self.assertNotEqual(len(response.body), len(response2.body))

    @tornado.testing.gen_test
    async def test_output_format_prometheus(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)

        query = """%
            select 'tinybird_count' as name, 'counter' as type, 'help desc' as help, 1234 as value FORMAT Prometheus
        """
        params = {"token": token, "q": query}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")

        parsed_metrics = text_string_to_metric_families(response.body.decode())
        for metric in parsed_metrics:
            self.assertEqual(metric.name, "tinybird_count", metric)
            self.assertEqual(metric.type, "counter", metric)

    @tornado.testing.gen_test
    async def test_output_format_prometheus_bad_structure(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)

        query = """%
            select 'tinybird_total' as no_name, 'counter' as type, 'help desc' as help, 1234 as value FORMAT Prometheus
        """
        params = {"token": token, "q": query}
        with patch("tinybird.ch.HTTPClient.query") as query_patch:
            query_patch.side_effect = CHException(
                "Code: 36. DB::Exception: Column 'name' is required for output format 'Prometheus'. (BAD_ARGUMENTS)"
            )
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400)
        result = json.loads(response.body)
        self.assertIn("Prometheus requires the query output to conform", result["error"])

    @tornado.testing.gen_test
    async def test_raise_template_parse_error(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)

        query = """%
            select * from test_table
            {% if defined(whatever) %}
            where 2
            {% else %}
        """
        params = {"token": token, "q": query}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400, response.body)
        res = json.loads(response.body)
        self.assertEqual(res["error"], "Syntax error: Missing {% end %} block for if at line 5")

    @tornado.testing.gen_test
    async def test_raise_value_error(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)

        query = """%
            select * from test_table
            {% if whatever(whatever) %}
            where 2
            {% end %}
        """
        params = {"token": token, "q": query}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400, response.body)
        res = json.loads(response.body)
        self.assertEqual(res["error"], "Template Syntax Error: 'whatever' is not a valid function, line 3")

    @tornado.testing.gen_test
    async def test_raise_template_syntax_error(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)

        query = "% SELECT 1 {% if defined((passenger_count) %} WHERE 1=1 {% end %}"

        params = {"token": token, "q": query}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400, response.body)
        res = json.loads(response.body)
        self.assertEqual(res["error"], "Syntax error: invalid syntax, line 1")

    @tornado.testing.gen_test
    async def test_raise_template_syntax_error_on_pipe(self):
        rand_id = uuid.uuid4().hex[0:6]
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = f"invalid_resource_{rand_id}"
        node_name = f"node_1{rand_id}"

        data = json.dumps(
            {
                "name": pipe_name,
                "nodes": [
                    {"name": node_name, "sql": "% SELECT 1 {% if defined((passenger_count) %} WHERE 1=1 {% end %}"},
                    {"name": f"{node_name}_0", "sql": f"select * from {node_name}", "type": "endpoint"},
                ],
            }
        )
        response = await self.fetch_async(
            f"/v0/pipes?token={token}&ignore_sql_errors=true",
            headers={"Content-type": "application/json"},
            method="POST",
            body=data,
        )
        self.assertEqual(response.code, 200)

        query = f"SELECT * FROM {pipe_name}"

        params = {"token": token, "q": query}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400)
        res = json.loads(response.body)
        self.assertEqual(
            res["error"], f"Syntax error: invalid syntax, line 1 (in node '{node_name}' from pipe '{pipe_name}')"
        )

    @tornado.testing.gen_test
    async def test_raise_template_syntax_error_on_another_pipe(self):
        rand_id = uuid.uuid4().hex[0:6]
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = f"invalid_resource_{rand_id}"
        another_pipe_name = f"{pipe_name}_0"
        node_name = f"node_1{rand_id}"

        data = json.dumps(
            {
                "name": pipe_name,
                "nodes": [
                    {"name": node_name, "sql": "% SELECT 1 {% if defined((passenger_count) %} WHERE 1=1 {% end %}"},
                    {"name": f"{node_name}_0", "sql": f"select * from {node_name}", "type": "endpoint"},
                ],
            }
        )
        response = await self.fetch_async(
            f"/v0/pipes?token={token}&ignore_sql_errors=true",
            headers={"Content-type": "application/json"},
            method="POST",
            body=data,
        )
        self.assertEqual(response.code, 200)

        data = json.dumps(
            {
                "name": another_pipe_name,
                "nodes": [{"name": f"{node_name}_1", "sql": f"select * from {pipe_name}", "type": "endpoint"}],
            }
        )
        response = await self.fetch_async(
            f"/v0/pipes?token={token}&ignore_sql_errors=true",
            headers={"Content-type": "application/json"},
            method="POST",
            body=data,
        )
        self.assertEqual(response.code, 200)

        # Templated
        query = f"% SELECT * FROM {another_pipe_name}"

        params = {"token": token, "q": query}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400)
        res = json.loads(response.body)
        self.assertEqual(
            res["error"], f"Syntax error: invalid syntax, line 1 (in node '{node_name}' from pipe '{pipe_name}')"
        )

        # Non-templated
        query = f"SELECT * FROM {another_pipe_name}"

        params = {"token": token, "q": query}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400)
        res = json.loads(response.body)
        self.assertEqual(
            res["error"], f"Syntax error: invalid syntax, line 1 (in node '{node_name}' from pipe '{pipe_name}')"
        )

    @tornado.testing.gen_test
    async def test_raise_template_parse_error_on_pipe(self):
        rand_id = uuid.uuid4().hex[0:6]
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = f"invalid_resource_{rand_id}"
        node_name = f"node_1{rand_id}"

        data = json.dumps(
            {
                "name": pipe_name,
                "nodes": [
                    {"name": node_name, "sql": "% SELECT * FROM {% import os %}{{ os.popen('ls').read() }}"},
                    {"name": f"{node_name}_0", "sql": f"select * from {node_name}", "type": "endpoint"},
                ],
            }
        )
        response = await self.fetch_async(
            f"/v0/pipes?token={token}&ignore_sql_errors=true",
            headers={"Content-type": "application/json"},
            method="POST",
            body=data,
        )
        self.assertEqual(response.code, 200)

        query = f"SELECT * FROM {pipe_name}"

        params = {"token": token, "q": query}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400)
        res = json.loads(response.body)
        self.assertEqual(
            res["error"], f"Syntax error: import is forbidden at line 1 (in node '{node_name}' from pipe '{pipe_name}')"
        )

    @tornado.testing.gen_test
    async def test_raise_template_unclosedif_error_on_pipe(self):
        rand_id = uuid.uuid4().hex[0:6]
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = f"invalid_resource_{rand_id}"
        node_name = f"node_1{rand_id}"

        data = json.dumps(
            {
                "name": pipe_name,
                "nodes": [
                    {"name": node_name, "sql": "% SELECT {% if defined(x) %} x, 1"},
                    {"name": f"{node_name}_0", "sql": f"select * from {node_name}", "type": "endpoint"},
                ],
            }
        )
        response = await self.fetch_async(
            f"/v0/pipes?token={token}&ignore_sql_errors=true",
            headers={"Content-type": "application/json"},
            method="POST",
            body=data,
        )
        self.assertEqual(response.code, 200)

        query = f"SELECT * FROM {pipe_name}"
        params = {"token": token, "q": query}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400)
        res = json.loads(response.body)
        self.assertTrue("Syntax error: Missing {% end %} block for if at line 1" in res.get("error"))
        self.assertTrue(f"(in node '{node_name}' from pipe '{pipe_name}')" in res.get("error"))

    @tornado.testing.gen_test
    async def test_raise_invalid_syntax_error(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)

        query = """%
            select * from test_table
            {% if whatever( %}
            where 2
            {% end %}
        """
        params = {"token": token, "q": query}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400, response.body)
        res = json.loads(response.body)
        self.assertEqual(res["error"], "Syntax error: invalid syntax, line 3")

    @tornado.testing.gen_test
    @patch("tinybird.monitor.statsd_client.incr")
    async def test_read_memory_for_query_limit(self, mock_incr: Mock):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)
        with patch(
            "tinybird.ch.HTTPClient.query",
            side_effect=CHException(
                f"Code: {CHErrors.MEMORY_LIMIT_EXCEEDED}, e.displayText() = DB::Exception: "
                "Memory limit (for query) exceeded: would use 4.66 GiB (attempt to "
                "allocate chunk of 4503240 bytes), maximum: 4.66 GiB"
            ),
        ):
            response = await self.fetch_async(
                f"/v0/sql?q=select+avg(number)+c+from+numbers(10000000000)+format+JSON&token={token}"
            )
            self.assertEqual(response.code, 400)
            res = json.loads(response.body)
            self.assertEqual(response.headers.get("X-DB-Exception-Code"), str(CHErrors.MEMORY_LIMIT_EXCEEDED))
            self.assertTrue(
                "Memory limit (for query) exceeded. Make sure the query just process the required data" in res["error"]
            )
            self.assertTrue("4.66 GiB" not in res["error"])
            self.assertTrue(
                "https://tinybird.co/docs/guides/best-practices-for-faster-sql.html#memory-limit-reached-title"
                in res["documentation"]
            )
            with self.assertRaises(AssertionError):
                mock_incr.assert_any_call(f"tinybird.{statsd_client.region_machine}.ch_errors.MEMORY_LIMIT_EXCEEDED")

    @tornado.testing.gen_test
    @patch("tinybird.monitor.statsd_client.incr")
    async def test_read_memory_total_limit(self, mock_incr: Mock):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)
        with patch(
            "tinybird.ch.HTTPClient.query",
            side_effect=CHException(
                f"Code: {CHErrors.MEMORY_LIMIT_EXCEEDED}, e.displayText() = DB::Exception: "
                "Memory limit (total) exceeded: would use 4.66 GiB (attempt to "
                "allocate chunk of 4503240 bytes), maximum: 4.66 GiB"
            ),
        ):
            response = await self.fetch_async(
                f"/v0/sql?q=select+avg(number)+c+from+numbers(10000000000)+format+JSON&token={token}"
            )
            self.assertEqual(response.headers.get("X-DB-Exception-Code"), str(CHErrors.MEMORY_LIMIT_EXCEEDED))
            self.assertEqual(response.code, 500)
            res = json.loads(response.body)
            self.assertTrue("Memory limit (total) exceeded" in res["error"])
            mock_incr.assert_any_call(f"tinybird.{statsd_client.region_machine}.ch_errors.MEMORY_LIMIT_EXCEEDED")

    @patch.object(Limit, "ch_max_execution_time", 1)
    @tornado.testing.gen_test
    async def test_read_respects_timeouts(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)
        response = await self.fetch_async(
            f"/v0/sql?q=select+avg(number)+c+from+numbers(10000000000)+format+JSON&token={token}"
        )
        self.assertEqual(response.code, 408)
        res = json.loads(response.body)
        self.assertTrue("contact us at support@tinybird.co to raise limits" in res["error"])
        self.assertTrue("While executing" not in res["error"])
        self.assertRegex(res["error"], "\\[Error\\] Timeout exceeded: elapsed 1.* seconds")

    @patch.object(Limit, "ch_max_execution_time", 1)
    @tornado.testing.gen_test
    async def test_read_respects_timeouts_on_cluster(self):
        tb_api_proxy = TBApiProxyAsync(self)
        user_b_name = f"user_b_{uuid.uuid4().hex}"
        workspace_b = await tb_api_proxy.register_user_and_workspace(f"{user_b_name}@example.com", user_b_name)
        token_workspace_b = Users.get_token_for_scope(workspace_b, scopes.ADMIN)

        self.workspaces_to_delete.append(workspace_b)

        response = await self.fetch_async(
            f"/v0/sql?q=select+avg(number)+c+from+numbers(10000000000)+format+JSON&token={token_workspace_b}"
        )
        self.assertEqual(response.code, 408)
        res = json.loads(response.body)
        self.assertTrue("contact us at support@tinybird.co to raise limits" in res["error"])
        self.assertTrue("While executing" not in res["error"])
        self.assertRegex(res["error"], "\\[Error\\] Timeout exceeded: elapsed 1.* seconds")

    @tornado.testing.gen_test
    async def test_read_respects_max_estimated_execution_time(self):
        u = Users.get_by_id(self.WORKSPACE_ID)

        # Override max_estimated_execution_time limit
        self.base_workspace.set_user_limit("max_estimated_execution_time", 2, "ch")
        self.base_workspace.set_user_limit("timeout_before_checking_execution_speed", 1, "ch")
        self.base_workspace.save()

        token = Users.add_token(u, "test", scopes.ADMIN)
        response = await self.fetch_async(f"/v0/sql?q=select+avg(number)+c+from+numbers(10000000000)&token={token}")
        self.assertEqual(response.code, 400)
        res = json.loads(response.body)
        self.assertRegex(
            res["error"], "\[Error\] Estimated query execution time \(.* seconds\) is too long.*\(TOO_SLOW\)"
        )

        # Reset max_estimated_execution_time limit
        self.base_workspace.delete_limit_config("max_estimated_execution_time")
        self.base_workspace.delete_limit_config("timeout_before_checking_execution_speed")
        self.base_workspace.save()

    @tornado.testing.gen_test
    @pytest.mark.skip("")
    async def test_query_cancelled_on_clickhouse_on_connection_closed(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        rand_id = uuid.uuid4().hex[0:6]
        token = Users.add_token(u, "test", scopes.ADMIN)

        # Simulate the client closing connection after 1s
        t1 = time.monotonic()

        response = await self.fetch_async(
            f"/v0/sql?q=select+avg(number)+c_{rand_id}+from+numbers({1000000*1000000})&token={token}",
            request_timeout=2.0,
            connect_timeout=2.0,
        )
        t2 = time.monotonic() - t1
        self.assertTrue(t2 < 10)
        self.assertTrue(response.code == 599)

        async def get_query_log(u: User, rand_id: str):
            cluster_host = u.database_server
            await ch_flush_logs_on_all_replicas(cluster_host, "tinybird")
            client = HTTPClient(cluster_host, database=None)
            headers, body = client.query_sync(
                f"""
                    SELECT query, query_id, exception_code
                    FROM clusterAllReplicas(tinybird, system.query_log)
                    WHERE
                        event_time > (now() - INTERVAL 10 SECONDS)
                        and type >= 2
                        and query not like '%system.query_log%'
                        and (query like '%KILL%' or query like '%{rand_id}%')
                    order by exception_code LIMIT 1 by exception_code
                    FORMAT JSON
                """
            )
            res = json.loads(body)
            # this might indicate the kill query timed out, maybe we have to mock
            self.assertTrue(len(res["data"]) == 2)
            return res

        get_query_log_fn = partial(get_query_log, u, rand_id)
        res = await poll_async(get_query_log_fn)

        # query was killed on connection close
        kill_query = next(row for row in res["data"] if "KILL" in row["query"])
        self.assertTrue(kill_query is not None)

        cancelled_query = next(row for row in res["data"] if str(rand_id) in row["query"])
        self.assertTrue(CHErrors.QUERY_WAS_CANCELLED == cancelled_query["exception_code"])
        self.assertTrue(cancelled_query["query_id"] in kill_query["query"])

        query_id = cancelled_query["query_id"]

        async def get_spans():
            params = {
                "token": token,
                "q": f"select * from tinybird.pipe_stats_rt where request_id = '{query_id}' and start_datetime > now() - interval 1 minute FORMAT JSON",
            }
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            res = json.loads(response.body)
            self.assertTrue(len(res["data"]) == 1)
            return res

        res = await poll_async(get_spans)
        self.assertTrue(res["data"][0]["status_code"] == 499)

    @tornado.testing.gen_test
    async def test_invalid_sql(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)
        response = await self.fetch_async(
            f"/v0/sql?q=select+sleepEachRow2222222(2)+c+from+numbers(10)+format+JSON&token={token}"
        )
        self.assertEqual(response.code, 400)
        res = json.loads(response.body)
        self.assertRegex(res["error"], ".*Unknown function sleepEachRow2222222.*")

    @tornado.testing.gen_test
    async def test_query_error_message_replacement(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)

        ds_name = "ds_query_error"
        params = {
            "token": token,
            "name": ds_name,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        s = StringIO("d,sales\n2019-01-01,2\n2019-01-02,3")
        response = await self.fetch_full_body_upload_async(create_url, s)
        self.assertEqual(response.code, 200, response.body)

        params = {
            "q": """
                SELECT ds_query_error.sales, ds_query_error.whatever as c FROM ds_query_error
            """,
            "token": token,
        }
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400)
        res = json.loads(response.body)
        self.assertRegex(
            res["error"],
            f"\[Error\] .* '({self.WORKSPACE}\.)?ds_query_error.whatever' .* Data Source .*ds_query_error.*",
        )

    @tornado.testing.gen_test
    async def test_query_error_message_replacement_with_multiples_datasources(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)

        ds_name_1 = "ds_query_error_1"
        params = {
            "token": token,
            "name": ds_name_1,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        s = StringIO("column_a,column_b\n2019-01-01,2\n2019-01-02,3")
        response = await self.fetch_full_body_upload_async(create_url, s)
        self.assertEqual(response.code, 200, response.body)

        ds_name_2 = "ds_query_error_2"
        params = {
            "token": token,
            "name": ds_name_2,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        s = StringIO("column_a,column_b\n2019-01-01,2\n2019-01-02,3")
        response = await self.fetch_full_body_upload_async(create_url, s)
        self.assertEqual(response.code, 200, response.body)

        params = {
            "q": """
                SELECT column_a, ds_query_error_2.column_b, ds_query_error_2.column_c
                FROM ds_query_error_2
                JOIN ds_query_error_1 USING column_a
            """,
            "token": token,
        }
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400)
        res = json.loads(response.body)
        self.assertRegex(
            res["error"],
            f"\[Error\] .* '({self.WORKSPACE}\.)?ds_query_error_2.column_c' .* Data Source .*ds_query_error_2.*",
        )

    @tornado.testing.gen_test
    async def test_query_missing_column_error_doesnt_expose_service_datasources_internals(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)

        query = "SELECT potato from tinybird.pipe_stats_rt"
        params = {
            "q": query,
            "token": token,
        }
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400, response.body)
        res = json.loads(response.body)
        self.assertIn(
            query,
            res["error"],
        )

    @tornado.testing.gen_test
    async def test_query_missing_columns_error_doesnt_expose_service_datasources_internals(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)

        query = "SELECT badcolumn1, badcolumn2 from tinybird.pipe_stats_rt"
        params = {
            "q": query,
            "token": token,
        }
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400, response.body)
        res = json.loads(response.body)
        self.assertIn(
            query,
            res["error"],
        )

    @tornado.testing.gen_test
    async def test_query_on_shared_datasource(self):
        workspace_a = Users.get_by_id(self.WORKSPACE_ID)
        user = UserAccount.get_by_id(self.USER_ID)
        token = UserAccount.get_token_for_scope(user, scopes.AUTH)

        tb_api_proxy = TBApiProxyAsync(self)
        workspace_b_id = (await tb_api_proxy.create_workspace(token, f"another_workspace_{uuid.uuid4().hex}"))["id"]
        workspace_b = Users.get_by_id(workspace_b_id)
        token_workspace_b = Users.get_token_for_scope(workspace_b, scopes.ADMIN)
        self.workspaces_to_delete.append(workspace_b)

        await tb_api_proxy.share_datasource_with_another_workspace(
            token=token,
            datasource_id=self.datasource.id,
            origin_workspace_id=workspace_a.id,
            destination_workspace_id=workspace_b.id,
            expect_notification=False,
        )

        response = await self.fetch_async(
            f"/v0/sql?q=select+*+from+{workspace_a.name}.test_table&token={token_workspace_b}"
        )
        self.assertEqual(response.code, 200)

        response = await self.fetch_async(
            f"/v0/sql?q=%select+*+from+{{{{TABLE('{workspace_a.name}.test_table')}}}}&token={token_workspace_b}"
        )
        self.assertEqual(response.code, 200)

    async def fetch_datasources_ops_log(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)

        query = """%  SELECT count() FROM tinybird.datasources_ops_log FORMAT JSON """
        params = {"token": token, "q": query}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)

    @tornado.testing.gen_test
    async def test_datasources_ops_log(self):
        await self.fetch_datasources_ops_log()

    @patch("tinybird.ch.HTTPClient.MAX_GET_LENGTH", 0)  # Force to test with post
    @tornado.testing.gen_test
    async def test_datasources_ops_log_post(self):
        await self.fetch_datasources_ops_log()

    @patch("tinybird.limits.Limits.rate_limit", return_value=[1, 1000, 0, 3600, 3600])
    @tornado.testing.gen_test
    async def test_build_plan_get_query_check_rate_limit(self, mock_rate_limit: AsyncMock):
        u = Users.get_by_id(self.WORKSPACE_ID)
        u.plan = BillingPlans.DEV
        u.save()
        token = Users.add_token(u, "test", scopes.DATASOURCES_READ, "test_table")
        params = {
            "token": token,
            "q": "SELECT number FROM system.numbers LIMIT 10 FORMAT JSON",
        }
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 429)
        mock_rate_limit.assert_called_once()
        args, _ = mock_rate_limit.call_args
        rate_limit = args[0]
        assert rate_limit.key == f'{self.WORKSPACE_ID}:build_plan_api_requests_{datetime.now().strftime("%Y%m%d")}'

    @patch("tinybird.limits.Limits.rate_limit", return_value=[1, 1000, 0, 3600, 3600])
    @tornado.testing.gen_test
    async def test_build_plan_get_query_from_ui_no_check_rate_limit(self, mock_rate_limit: AsyncMock):
        u = Users.get_by_id(self.WORKSPACE_ID)
        u.plan = BillingPlans.DEV
        u.save()
        token = Users.add_token(u, "test", scopes.DATASOURCES_READ, "test_table")
        params = {"token": token, "q": "SELECT number FROM system.numbers LIMIT 10 FORMAT JSON", "from": "ui"}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200)
        mock_rate_limit.assert_not_called()

    @patch("tinybird.limits.Limits.rate_limit", return_value=[1, 1000, 0, 3600, 3600])
    @tornado.testing.gen_test
    async def test_build_plan_post_query_request(self, mock_rate_limit: AsyncMock):
        u = Users.get_by_id(self.WORKSPACE_ID)
        u.plan = BillingPlans.DEV
        u.save()
        token = Users.add_token(u, "test", scopes.ADMIN)
        response = await self.fetch_async(f"/v0/sql?token={token}", method="POST", body="SELECT 1 FORMAT JSON")
        self.assertEqual(response.code, 429)
        mock_rate_limit.assert_called_once()
        args, _ = mock_rate_limit.call_args
        rate_limit = args[0]
        assert rate_limit.key == f'{self.WORKSPACE_ID}:build_plan_api_requests_{datetime.now().strftime("%Y%m%d")}'

    @tornado.testing.gen_test
    async def test_validate_closed_parenthesis(self):
        user = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(user, scopes.ADMIN)

        params = {
            "token": token,
            "q": """%
                    {% if definedtest) %}
                        SELECT 1
                    {% end %}
            """,
        }

        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400, response.body)
        self.assertEqual("Syntax error: unmatched ')', line 2" in json.loads(response.body)["error"], True)

    @tornado.testing.gen_test
    async def test_validate_keyword(self):
        user = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(user, scopes.ADMIN)

        params = {
            "token": token,
            "q": """%
                SELECT {{String(default=1, 'test')}}
            """,
        }

        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400, response.body)
        self.assertEqual(
            "Syntax error: positional argument follows keyword argument" in json.loads(response.body)["error"], True
        )

    @tornado.testing.gen_test
    async def test_validate_missing_end(self):
        user = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(user, scopes.ADMIN)

        params = {
            "token": token,
            "q": """%
                {% if defined(test) %}
                SELECT 1
            """,
        }

        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400, response.body)
        self.assertEqual(
            "Syntax error: Missing {% end %} block for if at line 2" in json.loads(response.body)["error"], True
        )

    @tornado.testing.gen_test
    async def test_validate_placeholder_compare_to_int(self):
        user = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(user, scopes.ADMIN)

        params = {
            "token": token,
            "q": """%
                {% if days > 90 %}
                select 1
                {% end %}
            """,
        }

        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400, response.body)
        self.assertEqual(
            "If you are using a dynamic parameter, you need to wrap it around a valid Data Type (e.g. Int8(placeholder))"
            in json.loads(response.body)["error"],
            True,
        )
        self.assertEqual("/query/query-parameters.html" in json.loads(response.body)["documentation"], True)

    @tornado.testing.gen_test
    async def test_split_to_array_with_placeholder(self):
        user = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(user, scopes.ADMIN)

        params = {
            "token": token,
            "q": """%
                {% for _last, _x in enumerate_with_last(split_to_array(attr, cols)) %}
                    _x
                    {% if not _last %}, {% end %}
                {% end %}
            """,
        }

        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400, response.body)
        self.assertEqual(
            "Template Syntax Error: First argument of split_to_array has to be a value that can be split to a list of elements, but found a PlaceHolder with no value instead"
            in json.loads(response.body)["error"],
            True,
        )
        self.assertEqual("split_to_array" in json.loads(response.body)["documentation"], True)

    @tornado.testing.gen_test
    async def test_validate_placeholder_compare_to_int_2(self):
        user = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(user, scopes.ADMIN)

        params = {
            "token": token,
            "q": """%
                {% if int(days) > 90 %}
                select 1
                {% end %}
            """,
        }

        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400, response.body)
        self.assertEqual("/query/query-parameters.html" in json.loads(response.body)["documentation"], True)

    @tornado.testing.gen_test
    async def test_split_to_array_with_separator(self):
        user = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(user, scopes.ADMIN)

        params = {
            "token": token,
            "q": """% SELECT {{split_to_array(String(test, 'hola,que tal|como va la vida|todo fenomenal|ah, muy bien'), separator='|')}} as text FORMAT JSONEachRow""",
        }

        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(len(json.loads(response.body)["text"]), 4, response.body)

    @tornado.testing.gen_test
    async def test_columns_array(self):
        user = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(user, scopes.ADMIN)

        params = {
            "token": token,
            "q": """% SELECT {{columns(split_to_array(String(test, 'hola,que tal|como va la vida|todo fenomenal|ah, muy bien'), separator='|'))}} as text FORMAT JSONEachRow""",
        }

        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400, response.body)
        self.assertEqual(
            json.loads(response.body)["error"],
            "Template Syntax Error: The 'columns' function expects a String not an Array",
            response.body,
        )
        self.assertEqual(
            json.loads(response.body)["documentation"],
            "https://docs.tinybird.co/cli/advanced-templates.html#columns",
            response.body,
        )

    @tornado.testing.gen_test
    async def test_parameter_not_defined(self):
        user = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(user, scopes.ADMIN)

        params = {
            "token": token,
            "q": """% {% set fieldslist = {{split_to_array(String(alrocar))}} %} select fieldslist""",
        }

        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400, response.body)
        self.assertEqual(
            json.loads(response.body)["error"], "Template Syntax Error: name 'alrocar' is not defined", response.body
        )
        self.assertEqual(
            json.loads(response.body)["documentation"],
            "https://docs.tinybird.co/cli/advanced-templates.html#defined",
            response.body,
        )

    @tornado.testing.gen_test
    async def test_parameter_missing_args(self):
        user = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(user, scopes.ADMIN)

        params = {"token": token, "q": """% {% set fieldslist = {{split_to_array(String())}} %} select fieldslist"""}

        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400, response.body)
        self.assertEqual(
            json.loads(response.body)["error"],
            "Template Syntax Error: one of the transform type functions is missing an argument",
            response.body,
        )
        self.assertEqual(
            json.loads(response.body)["documentation"],
            "https://docs.tinybird.co/cli/advanced-templates.html#transform-types-functions",
            response.body,
        )

    @tornado.testing.gen_test
    async def test_parameter_wrong_array(self):
        user = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(user, scopes.ADMIN)

        params = {"token": token, "q": """% SELECT {{Array(test, 1, 2, 3, 4)}}"""}

        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400, response.body)
        self.assertEqual(
            json.loads(response.body)["error"],
            "Template Syntax Error: transform type function Array is not well defined",
            response.body,
        )
        self.assertEqual(
            json.loads(response.body)["documentation"],
            "https://docs.tinybird.co/cli/advanced-templates.html",
            response.body,
        )

    @tornado.testing.gen_test
    async def test_parameter_wrong_function(self):
        user = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(user, scopes.ADMIN)

        params = {"token": token, "q": """% {% if defined(param) or  open('/etc/passwd') %} select 1 {% end %}"""}

        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400, response.body)
        self.assertEqual(
            json.loads(response.body)["error"],
            "Template Syntax Error: wrong syntax, you might be using a not valid function inside a control block",
            response.body,
        )
        self.assertEqual(
            json.loads(response.body)["documentation"],
            "https://docs.tinybird.co/cli/advanced-templates.html",
            response.body,
        )

    @tornado.testing.gen_test
    async def test_parameter_wrong_control_block(self):
        user = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(user, scopes.ADMIN)

        params = {"token": token, "q": """% {% if {{Int(days, 50)}} > 90 %} select 1 {% end %}"""}

        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400, response.body)
        self.assertEqual(
            json.loads(response.body)["error"],
            "Template Syntax Error: wrong syntax, you might be using a not valid function inside a control block",
            response.body,
        )
        self.assertEqual(
            json.loads(response.body)["documentation"],
            "https://docs.tinybird.co/cli/advanced-templates.html",
            response.body,
        )

    @tornado.testing.gen_test
    async def test_cache_ttl_directive(self):
        tb_api_proxy = TBApiProxyAsync(self)

        workspace_name = f"test_cache_ttl_directive_{uuid.uuid4().hex}"
        email = f"{workspace_name}@example.com"
        workspace = await tb_api_proxy.register_user_and_workspace(email, workspace_name, DEFAULT_CLUSTER)
        workspace_token = Users.get_token_for_scope(workspace, scopes.ADMIN)

        other_workspace_name = f"test_cache_ttl_directive_other_{uuid.uuid4().hex}"
        other_email = f"{other_workspace_name}@example.com"
        other_workspace = await tb_api_proxy.register_user_and_workspace(
            other_email, other_workspace_name, DEFAULT_CLUSTER
        )
        other_workspace_token = Users.get_token_for_scope(other_workspace, scopes.ADMIN)

        def get_params(token, query="select 1"):
            return {"token": token, "q": "% {{ cache_ttl('1m') }} " + query}

        for i in range(2):
            response = await self.fetch_async(f"/v0/sql?{urlencode(get_params(workspace_token))}")
            self.assertEqual(response.code, 200, response.body)
            self.assertEqual(response.headers["X-Cache-Hits"], str(i), response.headers)

        # Same query in other workspace don't share the cache key
        response = await self.fetch_async(f"/v0/sql?{urlencode(get_params(other_workspace_token))}")
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(response.headers["X-Cache-Hits"], "0", response.headers)

        # Original workspace keep getting a cached result
        response = await self.fetch_async(f"/v0/sql?{urlencode(get_params(workspace_token))}")
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(response.headers["X-Cache-Hits"], "2", response.headers)

        pipe_name = "pipe_with_cached_result"
        pipe = Users.add_pipe_sync(
            workspace,
            pipe_name,
            """%
            {{ cache_ttl('1m') }}
            SELECT sum(number) sum_a, count() as count
            FROM numbers(100000)
        """,
        )
        n0 = pipe.pipeline.nodes[0]
        pipe.endpoint = n0.id
        Users.update_pipe(workspace, pipe)

        params = {
            "token": workspace_token,
        }

        for i in range(3):
            response = await self.fetch_async(f"/v0/pipes/{pipe.name}.json?{urlencode(params)}")
            self.assertEqual(response.code, 200, response.body)
            results = json.loads(response.body)
            self.assertEqual(results["data"], [{"sum_a": 4999950000, "count": 100000}])
            self.assertEqual(response.headers["X-Cache-Hits"], str(i), response.headers)

        new_query = """%
            {{ cache_ttl('1m') }}
            SELECT sum(number) sum_a, count() as count
            FROM numbers(1000)
        """

        response = await self.fetch_async(
            f"/v0/pipes/{pipe.name}/nodes/{n0.name}?{urlencode(params)}", method="PUT", body=new_query
        )
        self.assertEqual(response.code, 200, response.body)

        for i in range(3):
            response = await self.fetch_async(f"/v0/pipes/{pipe.name}.json?{urlencode(params)}")
            self.assertEqual(response.code, 200, response.body)
            results = json.loads(response.body)
            self.assertEqual(results["data"], [{"sum_a": 499500, "count": 1000}])
            self.assertEqual(response.headers["X-Cache-Hits"], str(i), response.headers)

        invalid_query = "select toInt32('a')"
        for _ in range(3):
            response = await self.fetch_async(f"/v0/sql?{urlencode(get_params(workspace_token, invalid_query))}")
            self.assertEqual(response.code, 400, response.body)
            self.assertEqual(response.headers["X-Cache-Hits"], "0", response.headers)

    @tornado.testing.gen_test
    async def test_activate_directive_invalid(self):
        user = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(user, scopes.ADMIN)

        params = {"token": token, "q": "% {{ activate('invalid') }} select 1"}

        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400, response.body)
        self.assertEqual(
            json.loads(response.body)["error"],
            "Template Syntax Error: 'invalid' is not a valid 'activate' argument",
            response.body,
        )
        self.assertEqual(
            json.loads(response.body)["documentation"],
            "https://docs.tinybird.co/api-reference/query-api.html#get--v0-sql",
            response.body,
        )

    @tornado.testing.gen_test
    async def test_activate_directive_analyzer(self):
        user = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(user, scopes.ADMIN)

        params = {"token": token, "q": "% {{ activate('analyzer') }} select 1"}

        # Tests are running on versions that don't support 'allow_experimental_analyzer' settings.
        # Let's just check that the setting is passed through when is set in the template
        with patch("tinybird.ch.HTTPClient.query") as query_patch:
            await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            _, kwargs = query_patch.call_args

            self.assertEqual(kwargs["allow_experimental_analyzer"], 1)

    @tornado.testing.gen_test
    async def test_aggregation_warning(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        params = {"token": token, "q": "SELECT avg(a) FROM test_table"}

        with patch(
            "tinybird.ch.HTTPClient.query",
            side_effect=CHException(
                "Code: 43. DB::Exception: Illegal type AggregateFunction(avg, UInt64) of argument for aggregate function avg. (ILLEGAL_TYPE_OF_ARGUMENT) (version x.x.x)\n"
            ),
        ):
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            result = json.loads(response.body)
            self.assertEqual(response.headers.get("X-DB-Exception-Code"), str(CHErrors.ILLEGAL_TYPE_OF_ARGUMENT))
            self.assertTrue(
                "Some columns need to be aggregated by using the -Merge suffix. Use 'avgMerge'. Make sure you do this as late in the pipeline as possible for better performance"
                in result["error"],
                response.body,
            )
            self.assertTrue(
                "https://tinybird.co/docs/guides/best-practices-for-faster-sql.html#merging-aggregate-functions"
                in result["documentation"],
                response.body,
            )

    @tornado.testing.gen_test
    async def test_too_many_simultaneous_queries_message(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        params = {"token": token, "q": "SELECT avg(a) FROM test_table"}

        with patch(
            "tinybird.ch.HTTPClient.query",
            side_effect=CHException(
                "Code: 202. DB::Exception: Too many simultaneous queries. Maximum: 250. (TOO_MANY_SIMULTANEOUS_QUERIES) (version x.x.x)\n"
            ),
        ):
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            result = json.loads(response.body)
            self.assertEqual(response.headers.get("X-DB-Exception-Code"), str(CHErrors.TOO_MANY_SIMULTANEOUS_QUERIES))
            self.assertEqual(response.code, 500)
            self.assertTrue(
                "The server is processing too many queries at the same time. This could be because there are more requests than usual, because they are taking longer, or because the server is overloaded. Please check your requests or contact us at support@tinybird.co"
                in result["error"],
                response.body,
            )
            self.assertEqual(result["documentation"], "")

    @tornado.testing.gen_test
    async def test_replace_unknown_table_from_dependent_node_does_not_reach_clickhouse(self):
        rand_id = uuid.uuid4().hex[0:6]
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = f"invalid_resource_{rand_id}"
        node_name = f"node_1{rand_id}"

        data = json.dumps(
            {
                "name": pipe_name,
                "nodes": [
                    {"name": node_name, "sql": "select * from whatever"},
                    {"name": f"{node_name}_0", "sql": f"select * from {node_name}"},
                ],
            }
        )
        response = await self.fetch_async(
            f"/v0/pipes?token={token}&ignore_sql_errors=true",
            headers={"Content-type": "application/json"},
            method="POST",
            body=data,
        )
        self.assertEqual(response.code, 200)

        params = {"token": token, "q": f"SELECT * FROM {node_name}_0", "pipeline": pipe_name}

        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 403)
        self.assertEqual("Resource 'whatever' not found", json.loads(response.body)["error"])

    @tornado.testing.gen_test
    async def test_api_pipe_dependent_nodes_sql_happy_case(self):
        rand_id = uuid.uuid4().hex[0:6]
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        pipe_name = f"test_pipe_{rand_id}"
        node_name = f"node_1{rand_id}"
        node_name_0 = f"{node_name}_0"
        node_name_1 = f"{node_name}_1"
        node_name_2 = f"{node_name}_2"
        data = json.dumps(
            {
                "name": pipe_name,
                "nodes": [
                    {"name": node_name, "sql": "select * from numbers(100)"},
                    {"name": node_name_0, "sql": f"select * from {node_name}"},
                    {"name": node_name_1, "sql": f"select * from {node_name_0} where number > 10"},
                    {"name": node_name_2, "sql": f"select * from {node_name_1} where number > 20"},
                ],
            }
        )
        response = await self.fetch_async(
            f"/v0/pipes?token={token}&ignore_sql_errors=true",
            headers={"Content-type": "application/json"},
            method="POST",
            body=data,
        )
        self.assertEqual(response.code, 200)

        params = {"token": token, "q": f"SELECT * FROM {node_name_2} FORMAT JSON", "pipeline": pipe_name}

        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200)

    @tornado.testing.gen_test
    async def test_api_pipe_dependent_nodes_sql_unknown_clickhouse_table(self):
        rand_id = uuid.uuid4().hex[0:6]
        workspace = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(workspace, scopes.ADMIN)
        pipe_name = "test_query_with_unreachable_table_in_sql"
        node_name = f"node_1{rand_id}"
        node_name_0 = f"{node_name}_0"
        data = json.dumps(
            {
                "name": pipe_name,
                "nodes": [
                    {"name": node_name, "sql": "select * from test_table"},
                    {"name": node_name_0, "sql": f"select * from {node_name}"},
                ],
            }
        )
        response = await self.fetch_async(
            f"/v0/pipes?token={token}&ignore_sql_errors=true",
            headers={"Content-type": "application/json"},
            method="POST",
            body=data,
        )
        self.assertEqual(response.code, 200)

        with patch(
            "tinybird.ch.HTTPClient.query",
            side_effect=CHException(
                f"Code: 60. DB::Exception: Table {workspace.database}.{workspace.get_datasource('test_table').id} doesn't exist. (UNKNOWN_TABLE)"
            ),
        ):
            params = {"token": token, "q": f"SELECT count() FROM {node_name_0}", "pipeline": pipe_name}

            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            payload = json.loads(response.body)
            self.assertEqual(response.headers.get("X-DB-Exception-Code"), str(CHErrors.UNKNOWN_TABLE))
            self.assertEqual(response.code, 409)
            self.assertEqual(
                payload["error"], "Datasource 'test_table' not available at this time, you should retry the request"
            )

    @tornado.testing.gen_test
    async def test_debug_analyze_using_query_params(self):
        workspace = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(workspace, scopes.ADMIN)
        params = {"token": token, "q": "% {{ activate('analyzer') }} select 1", "debug": "analyze"}

        # Tests are running on versions that don't support 'allow_experimental_analyzer' settings.
        # Let's just check that the setting is passed through when is set in the template
        # TODO: Do a proper tests that it's working once we have latest version
        with (
            patch("clickhouse_driver.client.Client.execute") as trace_logs_patch,
            patch("tinybird.views.api_query.get_query_explain") as explain_patch,
        ):
            await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            _, kwargs = trace_logs_patch.call_args

            self.assertEqual(explain_patch.call_count, 1)
            self.assertEqual(kwargs["settings"]["allow_experimental_analyzer"], 1)

    @tornado.testing.gen_test
    async def test_explain_on_shared_datasource(self):
        workspace_a = Users.get_by_id(self.WORKSPACE_ID)
        user = UserAccount.get_by_id(self.USER_ID)
        token = UserAccount.get_token_for_scope(user, scopes.AUTH)

        tb_api_proxy = TBApiProxyAsync(self)
        workspace_b_id = (await tb_api_proxy.create_workspace(token, f"another_workspace_{uuid.uuid4().hex}"))["id"]
        workspace_b = Users.get_by_id(workspace_b_id)
        token_workspace_b = Users.get_token_for_scope(workspace_b, scopes.ADMIN)
        self.workspaces_to_delete.append(workspace_b)

        await tb_api_proxy.share_datasource_with_another_workspace(
            token=token,
            datasource_id=self.datasource.id,
            origin_workspace_id=workspace_a.id,
            destination_workspace_id=workspace_b.id,
            expect_notification=False,
        )

        table_name = f"{workspace_a.name}.test_table"
        response = await self.fetch_async(
            f"/v0/sql?q=select+*+from+{table_name}&token={token_workspace_b}&explain=true"
        )
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        expected_debug_query = re.compile(
            rf"^SELECT\s+\*\s+FROM\s+`{re.escape(table_name)}`", flags=re.MULTILINE | re.IGNORECASE
        )
        expected_query_explain = re.compile(
            rf"ReadFromMergeTree\s*\({re.escape(table_name)}\)", flags=re.MULTILINE | re.IGNORECASE
        )
        self.assertRegex(result["debug_query"], expected_debug_query)
        self.assertRegex(result["query_explain"], expected_query_explain)

    @tornado.testing.gen_test
    async def test_explain_on_nonshared_datasource(self):
        user = Users.get_by_id(self.WORKSPACE_ID)
        table_name = "test_table"
        datasource = Users.get_datasource(user, table_name)
        token = Users.add_token(user, "test", scopes.DATASOURCES_READ, datasource.id)
        response = await self.fetch_async(f"/v0/sql?q=select+*+from+{table_name}&token={token}&explain=true")
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        expected_debug_query = re.compile(
            rf"^SELECT\s+\*\s+FROM\s+{re.escape(table_name)}", flags=re.MULTILINE | re.IGNORECASE
        )
        expected_query_explain = re.compile(
            rf"ReadFromMergeTree\s*\({re.escape(table_name)}\)", flags=re.MULTILINE | re.IGNORECASE
        )
        self.assertRegex(result["debug_query"], expected_debug_query)
        self.assertRegex(result["query_explain"], expected_query_explain)

    @tornado.testing.gen_test
    async def test_log_more_http_insights(self):
        user = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(user, scopes.ADMIN)

        with User.transaction(self.WORKSPACE_ID) as w:
            w.feature_flags[FeatureFlagWorkspaces.LOG_MORE_HTTP_INSIGHTS.value] = True

        params = {"token": token, "q": "select 1"}

        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)

        self.force_flush_of_span_records()

        internal_user = public.get_public_user()
        spans = internal_user.get_datasource("spans")
        result = exec_sql(
            internal_user.database,
            f"SELECT tags FROM {internal_user.database}.{spans.id} WHERE workspace = '{self.WORKSPACE_ID}'",
            database_server=internal_user.database_server,
        )
        tags = json.loads(result)
        self.assertTrue("appconnect" in tags)
        self.assertTrue("connect" in tags)

    @tornado.testing.gen_test
    async def test_log_comment_query(self):
        user = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(user, scopes.ADMIN)

        random_uuid = uuid.uuid4().hex
        random_query = f"select '{random_uuid}' as x"
        params = {"token": token, "q": random_query}

        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)

        async def assert_log_comment():
            rows = await self.get_query_logs_by_where_async(
                f"query LIKE '%{random_uuid}%' AND http_user_agent = 'tb-api-query' "
            )

            log_comment = json.loads(rows[0]["log_comment"])
            self.assertEqual(log_comment["workspace"], user.name)

        await poll_async(assert_log_comment)


class TestAPISQLTables(BaseTest):
    def setUp(self):
        super().setUp()
        self.user = Users.get_by_id(self.WORKSPACE_ID)
        self.token = Users.get_token_for_scope(self.user, scopes.ADMIN)

    @tornado.testing.gen_test
    async def test_sql_tables_with_sql_with_database(self):
        params = {"token": self.token, "q": "SELECT * FROM system.csv_external", "raising": "true"}
        response = await self.fetch_async(f"/v0/sql_tables?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)
        res = json.loads(response.body)
        self.assertEqual(res, {"tables": [["system", "csv_external"]]})

    @tornado.testing.gen_test
    async def test_sql_tables_with_sql_without_database(self):
        params = {"token": self.token, "q": "SELECT * FROM csv_external", "raising": "true"}
        response = await self.fetch_async(f"/v0/sql_tables?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)
        res = json.loads(response.body)
        self.assertEqual(res, {"tables": [["", "csv_external"]]})


class TestAPISQLReplaces(BaseTest):
    def setUp(self):
        super().setUp()
        self.user = Users.get_by_id(self.WORKSPACE_ID)
        self.token = Users.get_token_for_scope(self.user, scopes.ADMIN)

    @tornado.testing.gen_test
    async def test_replaces_for_single_table_replacements(self):
        params = {
            "token": self.token,
            "q": "select * from csv_external",
            "replacements": json.dumps({"csv_external": "dev__asystem_csv_external"}),
        }
        response = await self.fetch_async(f"/v0/sql_replace?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)
        res = json.loads(response.body)
        self.assertEqual(res, {"query": "SELECT *\nFROM dev__asystem_csv_external AS csv_external"})

    @tornado.testing.gen_test
    async def test_replaces_where_it_has_database_and_table_to_be_replaced_for_a_single_table(self):
        params = {
            "token": self.token,
            "q": "select * from asystem.csv_external",
            "replacements": json.dumps({"asystem.csv_external": "dev__asystem_csv_external"}),
        }
        response = await self.fetch_async(f"/v0/sql_replace?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)
        res = json.loads(response.body)
        self.assertEqual(res, {"query": "SELECT *\nFROM dev__asystem_csv_external AS csv_external"})

    @tornado.testing.gen_test
    async def test_replaces_where_it_has_database_and_table_to_be_replaced_for_a_database_and_a_table(self):
        params = {
            "token": self.token,
            "q": "select * from asystem.csv_external",
            "replacements": json.dumps({"asystem.csv_external": "another_db.another_table"}),
        }
        response = await self.fetch_async(f"/v0/sql_replace?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)
        res = json.loads(response.body)
        self.assertEqual(res, {"query": "SELECT *\nFROM another_db.another_table AS csv_external"})


class TestAPISQLRemote(BaseTest):
    def setUp(self):
        super().setUp()
        self.workspace = Users.get_by_id(self.WORKSPACE_ID)
        self.token = Users.get_token_for_scope(self.workspace, scopes.ADMIN)
        with User.transaction(self.workspace.id) as workspace:
            self.ds = workspace.database_server
            workspace.database_server = "bla"

    def tearDown(self):
        with User.transaction(self.workspace.id) as workspace:
            workspace.database_server = self.ds
        super().tearDown()

    @tornado.testing.gen_test
    async def test_user_from_different_cluster_can_use_cluster_to_access_public_tables_and_are_filtered(self):
        params = {"token": self.token, "q": "select * from tinybird.datasources_ops_log", "debug": "query"}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(f"WHERE user_id = '{self.WORKSPACE_ID}'" in response.body.decode(), True, response.body)
        self.assertEqual("cluster" in response.body.decode(), True, response.body)

    @tornado.testing.gen_test
    async def test_internal_user_does_not_add_user_id_filter(self):
        pu = public.get_public_user()
        pu_token = Users.get_token_for_scope(pu, scopes.ADMIN)
        params = {"token": pu_token, "q": "select * from tinybird.datasources_ops_log", "debug": "query"}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(f"WHERE user_id = '{self.WORKSPACE_ID}'" not in response.body.decode(), True, response.body)

    @tornado.testing.gen_test
    async def test_direct_use_of_remote_is_forbidden(self):
        params = {
            "token": self.token,
            "q": "select * from remote('test_public', 'kafka_ops_log') UNION ALL select * from tinybird.kafka_ops_log",
            "debug": "query",
        }

        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 403, response.body)
        self.assertEqual(
            "DB::Exception: Usage of function remote is restricted" in json.loads(response.body)["error"], True
        )

    @tornado.testing.gen_test
    async def test_py_import_is_forbidden(self):
        params = {
            "token": self.token,
            "q": '% SELECT * FROM {% import os %}{{ os.popen("ls").read() }}',
            "debug": "query",
        }

        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400, response.body)
        self.assertIn("Syntax error: import is forbidden at line 1", json.loads(response.body)["error"])

    @tornado.testing.gen_test
    async def test_py_includes_is_forbidden(self):
        params = {"token": self.token, "q": '% SELECT * FROM {% include "/etc/passwd" %} %} }}', "debug": "query"}

        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400, response.body)
        self.assertIn("Syntax error: include is forbidden at line 1", json.loads(response.body)["error"])

    @tornado.testing.gen_test
    async def test_py_extends_is_forbidden(self):
        params = {"token": self.token, "q": '% SELECT * FROM {% extends "/etc/passwd" %} %} }}', "debug": "query"}

        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400, response.body)
        self.assertIn("Syntax error: extends is forbidden at line 1", json.loads(response.body)["error"])


class TestAPISQLFormat(BaseTest):
    def setUp(self):
        super().setUp()
        self.workspace = Users.get_by_id(self.WORKSPACE_ID)
        self.token = Users.get_token_for_scope(self.workspace, scopes.ADMIN)

    @tornado.testing.gen_test
    async def test_template_sign_format(self):
        params = {
            "token": self.token,
            "q": "% SELECT * FROM table",
        }

        response = await self.fetch_async(f"/v0/sql_format?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(json.loads(response.body)["q"], "%\nSELECT * FROM table")

        response = await self.fetch_async(f"/v0/sql_format?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(json.loads(response.body)["q"], "%\nSELECT * FROM table")

    @tornado.testing.gen_test
    async def test_template_clickhouse_format(self):
        params = {"token": self.token, "q": "SELECT timestamp + interval 1 day", "with_clickhouse_format": "true"}

        response = await self.fetch_async(f"/v0/sql_format?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(json.loads(response.body)["q"], "SELECT timestamp + toIntervalDay(1)")

    @tornado.testing.gen_test
    async def test_template_python_format(self):
        params = {
            "token": self.token,
            "q": """%
                {% if ( defined(cod_device) or defined(cod_device_not_in)
                    or defined(cod_order_type)
                    or defined(cod_brand) or defined(purchase_location)
                    or defined(campaign_period)
                    or defined(campaign_period_not_in)
                ) %} select 1 {% else %} select 2 {% end %}""",
        }

        response = await self.fetch_async(f"/v0/sql_format?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)
        expected = """%
{% if (
    defined(cod_device)
    or defined(cod_device_not_in)
    or defined(cod_order_type)
    or defined(cod_brand)
    or defined(purchase_location)
    or defined(campaign_period)
    or defined(campaign_period_not_in)
) %} select 1 {% else %} select 2 {% end %}"""
        self.assertEqual(json.loads(response.body)["q"], expected, json.loads(response.body)["q"])


class TestAPISQLCTE(BaseTest):
    def setUp(self):
        super().setUp()
        u = Users.get_by_id(self.WORKSPACE_ID)
        self.token = Users.get_token_for_scope(u, scopes.ADMIN)
        self.ds_name = "test_aliases"
        self.ds_name_1 = "test_aliases_1"
        params = {
            "token": self.token,
            "name": self.ds_name,
            "schema": """
                a Int32
            """,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        params["name"] = self.ds_name_1
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        self.datasource = Users.get_datasource(u, self.ds_name)
        self.datasource_1 = Users.get_datasource(u, self.ds_name_1)
        self.unpriv_token = Users.add_token(u, "test", scopes.DATASOURCES_READ, self.datasource_1.id)

    @tornado.testing.gen_test
    async def test_cte_in_operator(self):
        params = {"token": self.token, "q": "WITH [1, 2] AS a SELECT 1 as v WHERE v in a"}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200)

    @tornado.testing.gen_test
    async def test_cte_same_name(self):
        params = {
            "token": self.unpriv_token,
            "q": f"WITH {self.datasource.id} AS (SELECT * FROM {self.datasource.id}) SELECT * FROM {self.datasource.id}",
        }
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 403)

    @tornado.testing.gen_test
    async def test_cte_same_name_nested(self):
        params = {
            "token": self.unpriv_token,
            "q": f"WITH {self.datasource.id} AS (WITH {self.ds_name_1} AS (SELECT * FROM {self.datasource.id}) SELECT * FROM {self.ds_name_1}) SELECT * from {self.datasource.id}",
        }
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 403)

    @tornado.testing.gen_test
    async def test_cte_same_name_scalar(self):
        params = {
            "token": self.unpriv_token,
            "q": f"WITH (SELECT COUNT(*) FROM {self.datasource.id}) as {self.datasource.id} SELECT {self.datasource.id}",
        }
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 403)

    @tornado.testing.gen_test
    async def test_cte_siblings(self):
        params = {
            "token": self.unpriv_token,
            "q": f"WITH {self.ds_name} as (select * from {self.ds_name_1}), alias2 as (select * from {self.ds_name}) select * from alias2",
        }
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)


class TestAPISQLSecrets(BaseTest):
    def setUp(self):
        super().setUp()
        self.workspace = Users.get_by_id(self.WORKSPACE_ID)
        self.token = Users.get_token_for_scope(self.workspace, scopes.ADMIN)

    @tornado.testing.gen_test
    async def test_query_request_with_secret_only_admin_scope(self):
        name = f"test_with_secret_{uuid.uuid4().hex}"
        await Users.add_secret(self.workspace, name, "1234", None)

        # OK with admin token and SQL API
        response = await self.fetch_async(
            f"/v0/sql?token={self.token}", method="POST", body="%SELECT {{tb_secret('" + name + "')}} as a FORMAT JSON"
        )
        self.assertEqual(response.code, 200, response.body)
        self.assertTrue("1234" in json.loads(response.body)["data"][0]["a"])
        pipe = Users.add_pipe_sync(
            self.workspace,
            name,
            "%SELECT {{tb_secret('" + name + "')}}",
        )

        pipe.endpoint = pipe.pipeline.nodes[0].name
        Users.update_pipe(self.workspace, pipe)

        # ERROR with read token and SQL API
        pipe_token = Users.add_token(self.workspace, f"pipe_token_{name}", scopes.PIPES_READ, pipe.id)
        response = await self.fetch_async(
            f"/v0/sql?token={pipe_token}", method="POST", body="%SELECT {{tb_secret('" + name + "')}} as a FORMAT JSON"
        )
        self.assertEqual(response.code, 400, response.body)
        self.assertTrue(f"Cannot access secret '{name}'" in json.loads(response.body)["error"])

        params = {"token": pipe_token, "q": "%SELECT {{tb_secret('" + name + "')}} as a FORMAT JSON"}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400, response.body)
        self.assertTrue(f"Cannot access secret '{name}'" in json.loads(response.body)["error"])

        params = {
            "token": pipe_token,
            "q": "%SELECT {{tb_secret('" + name + "')}} as a FORMAT JSON",
            "pipeline": pipe.name,
        }
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 400, response.body)
        self.assertTrue(f"Cannot access secret '{name}'" in json.loads(response.body)["error"])

        # ERROR with read token and Pipe Data API with query param
        params = {"token": pipe_token, "q": "SELECT * FROM _", "pipeline": pipe.name}
        response = await self.fetch_async(f"/v0/pipes/{name}.json?{urlencode(params)}")
        self.assertEqual(response.code, 400, response.body)
        self.assertTrue(f"Cannot access secret '{name}'" in json.loads(response.body)["error"])

        params = {"token": pipe_token, "q": "SELECT * FROM _", "pipeline": pipe.name}
        response = await self.fetch_async(f"/v0/pipes/{name}.json?{urlencode(params)}", method="POST", body="")
        self.assertEqual(response.code, 400, response.body)
        self.assertTrue(f"Cannot access secret '{name}'" in json.loads(response.body)["error"])

    @tornado.testing.gen_test
    async def test_post_query_request_with_secret(self):
        name = f"test_with_secret_{uuid.uuid4().hex}"
        await Users.add_secret(self.workspace, name, "1234", None)

        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)
        response = await self.fetch_async(
            f"/v0/sql?token={token}", method="POST", body="%SELECT {{tb_secret('unknown')}} as a FORMAT JSON"
        )
        self.assertEqual(response.code, 400, response.body)
        self.assertTrue("Cannot access secret 'unknown'" in json.loads(response.body)["error"])

        response = await self.fetch_async(
            f"/v0/sql?token={token}", method="POST", body="%SELECT tb_secret('unknown') as a FORMAT JSON"
        )
        self.assertEqual(response.code, 403, response.body)
        self.assertTrue("Unknown function tb_secret" in json.loads(response.body)["error"])

        response = await self.fetch_async(
            f"/v0/sql?token={token}", method="POST", body="%SELECT {{tb_secret('" + name + "')}} as a FORMAT JSON"
        )
        self.assertEqual(response.code, 200, response.body)
        self.assertTrue("1234" in json.loads(response.body)["data"][0]["a"])

    @tornado.testing.gen_test
    async def test_get_query_request_with_secret(self):
        name = f"test_with_secret_{uuid.uuid4().hex}"
        await Users.add_secret(self.workspace, name, "1234", None)

        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.ADMIN)
        params = {
            "token": token,
            "q": """%
            SELECT {{tb_secret('unknown')}} as a FORMAT JSON""",
        }
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")

        self.assertEqual(response.code, 400, response.body)
        self.assertTrue("Cannot access secret 'unknown'" in json.loads(response.body)["error"])

        params = {
            "token": token,
            "q": """%
            SELECT {{tb_secret('"""
            + name
            + """')}} as a FORMAT JSON""",
        }
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)
        self.assertTrue("1234" in json.loads(response.body)["data"][0]["a"])

    @tornado.testing.gen_test
    async def test_api_pipe_with_tb_secret(self):
        name = f"test_with_secret_{uuid.uuid4().hex}"
        await Users.add_secret(self.workspace, name, "1234", None)
        pipe = Users.add_pipe_sync(
            self.workspace,
            name,
            "%SELECT {{tb_secret('" + name + "')}} as a",
        )

        pipe.endpoint = pipe.pipeline.nodes[0].name
        Users.update_pipe(self.workspace, pipe)

        pipe_token = Users.add_token(self.workspace, "pipe_token", scopes.PIPES_READ, pipe.id)

        response = await self.fetch_async(f"/v0/pipes/{name}.json?token={pipe_token}")
        result = json.loads(response.body)
        self.assertTrue(result["data"][0]["a"] == "1234")
        self.assertEqual(response.code, 200)

    @tornado.testing.gen_test
    async def test_api_pipe_with_unknown_tb_secret(self):
        name = f"test_with_secret_{uuid.uuid4().hex}"
        pipe = Users.add_pipe_sync(
            self.workspace,
            name,
            "%SELECT {{tb_secret('unknown')}} as a",
        )

        pipe.endpoint = pipe.pipeline.nodes[0].name
        Users.update_pipe(self.workspace, pipe)

        pipe_token = Users.add_token(self.workspace, "pipe_token", scopes.PIPES_READ, pipe.id)

        response = await self.fetch_async(f"/v0/pipes/{name}.json?token={pipe_token}")
        result = json.loads(response.body)
        self.assertTrue("Cannot access secret 'unknown'" in result["error"])
        self.assertEqual(response.code, 400)


class TestAPISQLInheritedVariables(BaseTest):
    def setUp(self):
        super().setUp()
        self.workspace = Users.get_by_id(self.WORKSPACE_ID)
        self.token = Users.get_token_for_scope(self.workspace, scopes.ADMIN)

    @tornado.testing.gen_test
    async def test_query_inherited_variables_from_endpoint(self):
        with User.transaction(self.WORKSPACE_ID) as w:
            w.feature_flags[FeatureFlagWorkspaces.INHERITED_TEMPLATING_VARIABLES.value] = True

        name = f"test_with_variable_{uuid.uuid4().hex}"
        pipe = Users.add_pipe_sync(
            self.workspace,
            name,
            "%SELECT {{ String(my_param, default='a') }} as col",
        )
        pipe.endpoint = pipe.pipeline.nodes[0].name
        Users.update_pipe(self.workspace, pipe)
        expression = "{% set my_param = 'b' %}"
        params = {"token": self.token, "q": f"%{expression}SELECT * FROM {name} FORMAT JSON", "pipeline": pipe.name}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(json.loads(response.body)["data"][0]["col"], "b")

    @tornado.testing.gen_test
    async def test_query_inherited_variables_from_endpoint_with_variables(self):
        with User.transaction(self.WORKSPACE_ID) as w:
            w.feature_flags[FeatureFlagWorkspaces.INHERITED_TEMPLATING_VARIABLES.value] = True

        name = f"test_with_variable_{uuid.uuid4().hex}"
        pipe = Users.add_pipe_sync(
            self.workspace,
            name,
            nodes=[
                {"name": "node_1", "sql": "%SELECT {{ String(my_param, default='a') }} as col"},
                {"name": "endpoint", "sql": "%{% set my_param = 'b' %}SELECT * FROM node_1"},
            ],
        )
        pipe.endpoint = "endpoint"
        Users.update_pipe(self.workspace, pipe)
        expression = "{% set my_param = 'c' %}"
        params = {"token": self.token, "q": f"%{expression}SELECT * FROM {name} FORMAT JSON", "pipeline": pipe.name}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(json.loads(response.body)["data"][0]["col"], "c")

    @tornado.testing.gen_test
    async def test_query_no_inherited_variables_from_endpoint_with_variables(self):
        with User.transaction(self.WORKSPACE_ID) as w:
            w.feature_flags[FeatureFlagWorkspaces.INHERITED_TEMPLATING_VARIABLES.value] = True

        name = f"test_with_variable_{uuid.uuid4().hex}"
        pipe = Users.add_pipe_sync(
            self.workspace,
            name,
            nodes=[
                {"name": "node_1", "sql": "%SELECT {{ String(my_param, default='a') }} as col"},
                {"name": "endpoint", "sql": "%{% set my_param = 'b' %}SELECT * FROM node_1"},
            ],
        )
        pipe.endpoint = "endpoint"
        Users.update_pipe(self.workspace, pipe)
        new_pipe = Users.add_pipe_sync(
            self.workspace,
            f"new_pipe_{uuid.uuid4().hex}",
            f"SELECT * FROM {name}",
        )
        params = {
            "token": self.token,
            "q": f"SELECT * FROM {new_pipe.pipeline.nodes[0].name} FORMAT JSON",
            "pipeline": new_pipe.name,
        }
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(json.loads(response.body)["data"][0]["col"], "b")

    @tornado.testing.gen_test
    async def test_query_no_inherited_variables_from_endpoint_with_no_variables(self):
        with User.transaction(self.WORKSPACE_ID) as w:
            w.feature_flags[FeatureFlagWorkspaces.INHERITED_TEMPLATING_VARIABLES.value] = True

        name = f"test_with_variable_{uuid.uuid4().hex}"
        pipe = Users.add_pipe_sync(
            self.workspace,
            name,
            nodes=[
                {"name": "node_1", "sql": "%SELECT {{ String(my_param, default='a') }} as col"},
                {"name": "endpoint", "sql": "SELECT * FROM node_1"},
            ],
        )
        pipe.endpoint = "endpoint"
        Users.update_pipe(self.workspace, pipe)
        new_pipe = Users.add_pipe_sync(
            self.workspace,
            f"new_pipe_{uuid.uuid4().hex}",
            f"SELECT * FROM {name}",
        )
        params = {
            "token": self.token,
            "q": f"SELECT * FROM {new_pipe.pipeline.nodes[0].name} FORMAT JSON",
            "pipeline": new_pipe.name,
        }
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(json.loads(response.body)["data"][0]["col"], "a")

    @tornado.testing.gen_test
    async def test_query_inherited_variables_from_endpoint_without_ff(self):
        name = f"test_with_variable_{uuid.uuid4().hex}"
        pipe = Users.add_pipe_sync(
            self.workspace,
            name,
            "%SELECT {{ String(my_param, default='a') }} as col",
        )
        pipe.endpoint = pipe.pipeline.nodes[0].name
        Users.update_pipe(self.workspace, pipe)
        expression = "{% set my_param = 'b' %}"
        params = {"token": self.token, "q": f"%{expression}SELECT * FROM {name} FORMAT JSON", "pipeline": pipe.name}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(json.loads(response.body)["data"][0]["col"], "a")

    @tornado.testing.gen_test
    async def test_query_inherited_variables_from_endpoint_with_url_variables(self):
        with User.transaction(self.WORKSPACE_ID) as w:
            w.feature_flags[FeatureFlagWorkspaces.INHERITED_TEMPLATING_VARIABLES.value] = True

        name = f"test_with_variable_{uuid.uuid4().hex}"
        pipe = Users.add_pipe_sync(
            self.workspace,
            name,
            "%SELECT {{ String(my_param, default='a') }} as col",
        )
        pipe.endpoint = pipe.pipeline.nodes[0].name
        Users.update_pipe(self.workspace, pipe)
        expression = "{% set my_param = 'b' %}"
        params = {
            "token": self.token,
            "q": f"%{expression}SELECT * FROM {name} FORMAT JSON",
            "pipeline": pipe.name,
            "my_param": "c",
        }
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(json.loads(response.body)["data"][0]["col"], "c")
