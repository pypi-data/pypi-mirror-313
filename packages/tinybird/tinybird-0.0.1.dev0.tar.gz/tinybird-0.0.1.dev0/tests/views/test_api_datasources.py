import asyncio
import base64
import json
import math
import os
import re
import time
import uuid
from abc import abstractmethod
from datetime import datetime
from io import StringIO
from statistics import mean
from typing import Dict, Optional, Tuple
from unittest import mock
from unittest.mock import AsyncMock, MagicMock, Mock, patch
from urllib.parse import quote, urlencode

import googleapiclient.errors
import pytest
import requests
import snowflake.connector.errors
import tornado
from tinybird_cdk.connectors.snowflake import Integration
from tornado.httpclient import AsyncHTTPClient

from tinybird import app
from tinybird.ch import (
    CHParquetMetadata,
    HTTPClient,
    ch_get_cluster_instances,
    ch_table_details_async,
    host_port_from_url,
)
from tinybird.csv_importer import CSVImporterSettings
from tinybird.csv_processing_queue import CsvChunkQueue
from tinybird.data_connector import DataConnector, DataConnectorChannels, DataConnectors, DataLinker
from tinybird.feature_flags import FeatureFlagWorkspaces
from tinybird.ingest.cdk_utils import CDK_IMAGE_REGISTRY, CDKUtils
from tinybird.ingest.data_connectors import ConnectorException
from tinybird.ingest.external_datasources.connector import (
    SNOWFLAKE_TINYBIRD_INTEGRATION_FORMAT,
    CDKConnector,
    InvalidGCPCredentials,
)
from tinybird.internal_thread import WorkspaceDatabaseUsageTracker
from tinybird.limits import DEFAULT_CDK_VERSION, RateLimitConfig
from tinybird.model import retry_transaction_in_case_of_concurrent_edition_error_sync
from tinybird.pg import PGService
from tinybird.syncasync import sync_to_async
from tinybird.token_scope import scopes
from tinybird.user import User, UserAccount, UserAccounts, Users, get_token_name, public
from tinybird.views.api_datasources_import import STREAM_BACKPRESSURE_MAX_WAIT, STREAM_BACKPRESSURE_WAIT
from tinybird.views.api_errors.data_connectors import DataConnectorsUnprocessable
from tinybird.views.api_errors.datasources import ClientErrorBadRequest
from tinybird_shared.redis_client.redis_client import TBRedisClientSync

from ..conftest import CH_HOST, CH_HTTP_PORT, OTHER_STORAGE_POLICY, get_app_settings, get_redis_config, is_main_process
from ..utils import (
    HTTP_ADDRESS,
    CsvIO,
    e2e_fixture_data,
    exec_sql,
    fixture_data,
    fixture_file,
    get_db_size_records,
    get_finalised_job_async,
    poll,
    poll_async,
    start_http_redirect_server,
    start_http_slow_server,
)
from .base_test import BaseTest, TBApiProxyAsync


class TestAPIDatasourceBase(BaseTest):
    async def timeout_job(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        slow_http_server = start_http_slow_server()

        params = {
            "token": token,
            "mode": "create",
            "name": "test_import_ndjson_with_timeout",
            "format": "ndjson",
            "schema": """
            audienceId String `json:$.audienceId`
            """,
            "url": f"{slow_http_server}/events.ndjson",
        }
        post = sync_to_async(requests.post, thread_sensitive=False)
        create_url = self.get_url("/v0/datasources")
        response = await post(create_url, params=params)

        self.assertEqual(response.status_code, 200, response.text)

        job = await get_finalised_job_async(json.loads(response.text)["id"])
        return job

    def check_count(self, expected_value, table_name):
        a = exec_sql(self.u["database"], f"SELECT count() c FROM {table_name} FORMAT JSON")
        row = a["data"][0]
        self.assertEqual(int(row["c"]), expected_value)

    async def assert_stats_async(self, datasource_id, token, count, _bytes):
        ds_url = f"/v0/datasources/{datasource_id}?token={token}"
        response = await self.fetch_async(self.get_url(ds_url))
        self.__assert_stats_response(response, count, _bytes)

    def assert_stats(self, datasource_id, token, count, _bytes):
        ds_url = f"/v0/datasources/{datasource_id}?token={token}"
        response = self.fetch(ds_url)
        self.__assert_stats_response(response, count, _bytes)

    def __assert_stats_response(self, response, count, _bytes):
        self.assertEqual(response.code, 200)
        payload = json.loads(response.body)
        statistics = payload["statistics"]

        # NOTE: this two test could fail because stats are calculated
        # with clickhouse parts table.
        # change by the lines below
        self.assertEqual(statistics["row_count"], count)
        # 50% margin
        self.assertAlmostEqual(statistics["bytes"], _bytes, delta=_bytes * 0.5)
        # self.assertTrue(statistics['row_count'] > 0)
        # self.assertTrue(statistics['bytes'] > 1175)

    async def _query(self, table=None, query=None, token=None):
        if not token:
            u = Users.get_by_id(self.WORKSPACE_ID)
            token = Users.get_token_for_scope(u, scopes.ADMIN)

        params = {"token": token, "q": f"SELECT * FROM {table} FORMAT JSON" if table else query}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)
        return json.loads(response.body)

    def setUp(self):
        self.tables_to_delete = []
        self.pipe_id = 0
        super().setUp()
        self.tb_api_proxy_async = TBApiProxyAsync(self)

    def tearDown(self):
        # We want to stop the server + threads first
        super().tearDown()

    def delete_table(self, database, table_name):
        self.tables_to_delete.append((database, table_name))

    async def create_datasource_async(self, token, datasource_name, schema, engine_params, expect_ops_log=True):
        response = await self.tb_api_proxy_async.create_datasource(
            token, datasource_name, schema, engine_params=engine_params
        )
        if expect_ops_log:
            self.expect_ops_log(
                {"event_type": "create", "datasource_name": datasource_name, "options": {"source": "schema"}}
            )
        return response

    async def append_data_to_datasource(self, token, datasource_name, data, extra_expected_ops_logs=None):
        response = await self.tb_api_proxy_async.append_data_to_datasource(token, datasource_name, data)
        self.expect_ops_log(
            {"event_type": "append", "datasource_name": datasource_name, "options": {"source": "full_body"}}
        )

        if extra_expected_ops_logs:
            for log in extra_expected_ops_logs:
                self.expect_ops_log(log)

        return response

    async def replace_data_to_datasource(
        self, token, datasource_name, data, expect_logs=True, replace_truncate_when_empty=None
    ):
        response = await self.tb_api_proxy_async.replace_data_to_datasource(
            token, datasource_name, data, replace_truncate_when_empty
        )

        if expect_logs:
            self.expect_ops_log(
                {"event_type": "replace", "datasource_name": datasource_name, "options": {"source": "full_body"}}
            )
        return response

    async def expected_data_in_datasource(
        self, token, datasource_name, data, order_by_columns=None, add_final=False
    ) -> None:
        async def _expected_data_in_datasource():
            final = "final" if add_final else ""
            order_clause = f"ORDER BY {order_by_columns}" if order_by_columns else ""
            params = {"token": token, "q": f"SELECT * FROM {datasource_name} {final} {order_clause} FORMAT CSV"}
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            self.assertEqual(response.code, 200, response.body)
            self.assertEqual(response.body.decode(), data)

        await poll_async(_expected_data_in_datasource)

    async def expected_data_in_join_datasource(self, token, datasource_name, columns, key, data):
        select_join_get_columns = ", ".join(
            [f"joinGet('{datasource_name}', '{column}', '{key}') as {column}" for column in columns]
        )

        params = {"token": token, "q": f"SELECT {select_join_get_columns} FORMAT CSV"}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(response.body.decode(), data)
        return response

    def _create_view_shared_code(
        self, user, token, target_datasource_name, source_datasource_name="test_table", populate=False, pipe_name=None
    ):
        if pipe_name is None:
            self.pipe_id += 1
            pipe_name = f"{target_datasource_name}_pipe_{self.pipe_id}"
        Users.add_pipe_sync(user, pipe_name, f"select * from {source_datasource_name}")
        params = {
            "token": token,
            "name": f"{pipe_name}_view",
            "type": "materialized",
            "datasource": target_datasource_name,
            "populate": "true" if populate else "false",
        }
        return f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}"

    def create_view(
        self,
        user,
        token,
        target_datasource_name,
        pipe_sql,
        source_datasource_name="test_table",
        populate=False,
        pipe_name=None,
    ):
        url = self._create_view_shared_code(
            user, token, target_datasource_name, source_datasource_name, populate, pipe_name
        )
        response = self.fetch(url, method="POST", body=pipe_sql)
        self.assertEqual(response.code, 200, response.body)
        return json.loads(response.body)

    async def create_view_async(
        self,
        user,
        token,
        target_datasource_name,
        pipe_sql,
        source_datasource_name="test_table",
        populate=False,
        pipe_name=None,
    ):
        url = self._create_view_shared_code(
            user, token, target_datasource_name, source_datasource_name, populate, pipe_name
        )
        response = await self.tb_api_proxy_async._fetch(url, method="POST", data=pipe_sql)
        self.assertEqual(response.status_code, 200, response.content)
        return response.json()

    async def create_pipe_copy_async(
        self, user, token, target_datasource_name, pipe_name, source_datasource_name="test_table", sql=None
    ):
        node_name = f"{pipe_name}_0"
        nodes = [{"name": node_name, "sql": sql if sql else f"SELECT * FROM {source_datasource_name}"}]

        Users.add_pipe_sync(user, pipe_name, nodes=nodes)

        params = {"token": token, "target_datasource": target_datasource_name}

        response = await self.tb_api_proxy_async._fetch(
            f"/v0/pipes/{pipe_name}/nodes/{node_name}/copy?{urlencode(params)}", method="POST", data=""
        )
        self.assertEqual(response.status_code, 200, response.content)
        return response.json()

    async def run_sql(self, token, sql):
        params = {"token": token, "q": sql}
        response = await self.tb_api_proxy_async._fetch(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.status_code, 200, response.content)
        return response

    async def replace_data_with_condition_to_datasource(
        self, token, landing_datasource_name, replace_condition, data: CsvIO, replace_options=""
    ):
        params = {
            "token": token,
            "mode": "replace",
            "replace_condition": replace_condition,
            "name": landing_datasource_name,
        }
        if replace_options and isinstance(replace_options, list):
            for option in replace_options:
                params[option] = "true"
        replace_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_full_body_upload_async(replace_url, data)
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        self.assertFalse(result["error"])
        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": landing_datasource_name,
                "options": {
                    "source": "full_body",
                    "replace_condition": replace_condition,
                },
            }
        )

    async def replace_with_data_in_sql_async(
        self,
        token,
        landing_datasource_name,
        replace_condition=None,
        data_query="",
        replace_options="",
        expect_error=False,
        extra_expected_ops_logs=None,
        max_retries=600,
        elapsed_time_interval=0.2,
        expect_logs=True,
    ):
        csv_url = self.get_url_for_sql(data_query)

        params = {"token": token, "mode": "replace", "name": landing_datasource_name, "url": csv_url}

        if replace_condition:
            params["replace_condition"] = replace_condition

        if replace_options and isinstance(replace_options, list):
            for option in replace_options:
                params[option] = "true"

        replace_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(replace_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        job = await self.get_finalised_job_async(
            json.loads(response.body)["id"], max_retries=max_retries, elapsed_time_interval=elapsed_time_interval
        )

        if not expect_error:
            self.assertEqual(job["status"], "done", job)

        if expect_logs:
            expected_ops_log = {
                "event_type": "replace",
                "datasource_name": landing_datasource_name,
                "options": {"source": csv_url},
            }

            if replace_condition:
                expected_ops_log["options"]["replace_condition"] = replace_condition

            if expect_error:
                expected_ops_log["result"] = "error"
            self.expect_ops_log(expected_ops_log)

        if extra_expected_ops_logs:
            for log in extra_expected_ops_logs:
                self.expect_ops_log(log)

        return job

    async def create_tag(self, token, tag_name, datasources, pipes):
        tag = {
            "name": tag_name,
            "resources": [{"id": ds_name, "name": ds_name, "type": "datasource"} for ds_name in datasources or []]
            + [{"id": pipe_name, "name": pipe_name, "type": "pipe"} for pipe_name in pipes or []],
        }
        tags_url = f"/v0/tags?token={token}"
        await self.fetch_async(tags_url, method="POST", body=json.dumps(tag))


class TestAPIDatasourceList(TestAPIDatasourceBase):
    @tornado.testing.gen_test
    async def test_datasource_list(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        ds_name = "test_ds_list"
        await self.create_datasource_async(
            token,
            ds_name,
            """
            dt Date,
            country String,
            product String,
            units Int32
        """,
            {"engine": "MergeTree", "engine_partition_key": "dt", "engine_sorting_key": "dt, product"},
        )

        await self.append_data_to_datasource(
            token,
            ds_name,
            CsvIO(
                "2020-01-01,ES,A,1",
                "2020-01-02,ES,A,1",
            ),
        )

        params = {
            "token": token,
        }
        list_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(list_url)
        self.assertEqual(response.code, 200)
        parsed = json.loads(response.body)
        self.assertEqual(len(parsed["datasources"]), 1)  # test_table is added in all tests

        imported_data = parsed["datasources"][0]
        self.assertTrue(imported_data is not None, parsed)
        self.assertEqual(imported_data["statistics"]["row_count"], 2, imported_data)
        self.assertNotEqual(imported_data["statistics"]["bytes"], 0, imported_data)

        frontend_url_params = {
            "token": token,
            "attrs": "id,name,description,cluster,tags,created_at,updated_at,replicated,version,project,headers,shared_with,shared_from,engine,columns,type,statistics,new_columns_detected,kafka_topic,kafka_group_id,kafka_auto_offset_reset,kafka_store_raw_value,kafka_target_partitions,service,connector,quarantine_rows",
            "from": "ui",
        }
        list_url = f"/v0/datasources?{urlencode(frontend_url_params)}"
        response = await self.fetch_async(list_url)
        self.assertEqual(response.code, 200)
        parsed = json.loads(response.body)
        self.assertEqual(len(parsed["datasources"]), 1)  # test_table is added in all tests

        imported_data = parsed["datasources"][0]
        self.assertTrue(imported_data is not None, parsed)
        self.assertEqual(imported_data["statistics"]["row_count"], 2, imported_data)
        self.assertNotEqual(imported_data["statistics"]["bytes"], 0, imported_data)


class TestAPIDatasourceImportNoTypeGuessing(TestAPIDatasourceBase):
    @pytest.mark.serial  # Better to test this serially (better to move it elsewhere too)
    @pytest.mark.skipif(not is_main_process(), reason="Serial test")
    @pytest.mark.xfail(
        reason="Allowing to fail this test until we fix the issue. https://gitlab.com/tinybird/analytics/-/issues/10238"
    )
    @tornado.testing.gen_test
    async def test_import_performance(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        name = "test_import_performance"
        params = {"token": token, "name": name}
        create_url = f"/v0/datasources?{urlencode(params)}"
        with fixture_file("medium.csv") as fd:
            response = await self.fetch_full_body_upload_async(create_url, fd)
        self.assertEqual(response.code, 200, response.body)

        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": name,
                },
                {
                    "event_type": "append",
                    "datasource_name": name,
                    "options": {
                        "source": "full_body",
                    },
                },
            ]
        )

        append_url = f"/v0/datasources?token={token}&name={name}&mode=append"

        async def work():
            with fixture_file("medium.csv") as fd:
                response = await self.fetch_full_body_upload_async(append_url, fd)
            self.assertEqual(response.code, 200, response.body)

        def postWork():
            self.expect_ops_log(
                {
                    "event_type": "append",
                    "datasource_name": name,
                    "options": {
                        "source": "full_body",
                    },
                }
            )

        await self.time_check(work, 10, 0.8, 0.8, postWork=postWork)

    async def time_check(self, work, iterations, max_mean, max_p90, postWork=None):
        IS_CI = os.environ.get("CI", False)

        def check_timings(timings, max_mean, max_p90):
            if IS_CI:
                max_mean *= 1.5
                max_p90 *= 1.5
            else:
                max_mean *= 1.6
                max_p90 *= 1.6
            mean_timings = mean(timings)
            p90_timings = sorted(timings)[math.ceil(iterations * 0.9) - 1]
            self.assertLess(mean_timings, max_mean, f"Invalid mean time performance: {mean_timings}")
            self.assertLess(p90_timings, max_p90, f"Invalid P90 time performance: {mean_timings}")

        await work()  # warm up
        postWork()
        timings = []
        for _i in range(iterations):
            start = time.monotonic()
            await work()
            timings.append(time.monotonic() - start)
            postWork()
        check_timings(timings, max_mean=max_mean, max_p90=max_p90)

    @tornado.testing.gen_test
    async def test_import_body(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        with fixture_file("yt_1000.csv") as fd:
            response = await self.fetch_full_body_upload_async(
                "/v0/datasources?token=%s&name=test_import_body&type_guessing=false" % token, fd
            )
        self.assertEqual(response.code, 200)
        b = json.loads(response.body)
        self.assertEqual(b["datasource"]["name"], "test_import_body")

        expected_rows = 998
        expected_rows_quarantine = 0

        self.assertEqual(b["invalid_lines"], 0)
        self.assertEqual(b["quarantine_rows"], expected_rows_quarantine)

        a = exec_sql(u["database"], "select * from `%s` FORMAT JSON" % b["datasource"]["id"])
        meta = a["meta"]
        meta_types = set(list([x["type"] for x in meta]))
        self.assertEqual(meta_types, {"String"})

        a = exec_sql(u["database"], "select count(1) c from `%s` FORMAT JSON" % b["datasource"]["id"])
        row = a["data"][0]
        self.assertEqual(int(row["c"]), expected_rows)

        a = exec_sql(u["database"], "select count(1) c from `%s_quarantine` FORMAT JSON" % b["datasource"]["id"])
        row = a["data"][0]
        self.assertEqual(int(row["c"]), expected_rows_quarantine)
        self.delete_table(u["database"], b["datasource"]["id"])

        await self.assert_stats_async("test_import_body", token, expected_rows, 67157)
        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": "test_import_body",
                },
                {
                    "event_type": "append",
                    "datasource_name": "test_import_body",
                    "rows": expected_rows,
                    "rows_quarantine": expected_rows_quarantine,
                    "options": {
                        "source": "full_body",
                    },
                },
            ]
        )

    @tornado.testing.gen_test
    async def test_import_url_from_body_params(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        name = "test_import_url_body_param"
        params = {"token": token, "name": name, "type_guessing": "false"}
        csv_url = self.get_url_for_sql("select 1, 2, 3, 4 format CSV")
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body=urlencode({"url": csv_url}))
        self.assertEqual(response.code, 200, response.body)

        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done", str(job))

        a = exec_sql(u["database"], f"SELECT * FROM {job['datasource']['id']} FORMAT JSON")
        meta = a["meta"]
        meta_types = set(list([x["type"] for x in meta]))
        self.assertEqual(meta_types, {"String"})

        self.expect_ops_log(
            [
                {"event_type": "create", "datasource_name": name, "options": {"source": csv_url}},
                {"event_type": "append", "datasource_name": name, "options": {"source": csv_url}},
            ]
        )

    @tornado.testing.gen_test
    async def test_append_and_create(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.DATASOURCES_CREATE)
        csv_url = self.get_url_for_sql("select '1,2,3,4' format CSV")

        async def _send_data():
            import_url = f"/v0/datasources?token={token}&name=test_append_and_create&url={quote(csv_url,safe='')}&mode=append&type_guessing=false"

            response = await self.fetch_async(import_url, method="POST", body="")
            self.assertEqual(response.code, 200)

            job = await self.get_finalised_job_async(json.loads(response.body)["id"])
            self.assertEqual(job.status, "done")
            return job

        # create
        job = await _send_data()
        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": "test_append_and_create",
                },
                {
                    "event_type": "append",
                    "datasource_name": "test_append_and_create",
                    "rows": 1,
                    "options": {
                        "source": csv_url,
                    },
                },
            ]
        )
        # append
        await _send_data()
        self.expect_ops_log(
            {
                "event_type": "append",
                "datasource_name": "test_append_and_create",
                "rows": 1,
                "options": {
                    "source": csv_url,
                },
            },
        )

        a = exec_sql(u["database"], f"SELECT * FROM {job['datasource']['id']} FORMAT JSON")
        meta = a["meta"]
        meta_types = set(list([x["type"] for x in meta]))
        self.assertEqual(meta_types, {"String"})

    @tornado.testing.gen_test
    async def test_create_streaming(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        url = self.get_url(f"/v0/datasources?token={token}&type_guessing=false&name=test_create_streaming")

        with fixture_file("yt_1000.csv", mode="rb") as fd:
            response = await self.fetch_stream_upload_async(url, fd)
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)

        expected_rows = 998
        expected_rows_quarantine = 0

        datasource_id = result["datasource"]["id"]
        a = exec_sql(u["database"], f"SELECT count() c FROM {datasource_id} FORMAT JSON")
        row = a["data"][0]
        self.assertEqual(int(row["c"]), expected_rows)
        a = exec_sql(u["database"], f"SELECT count() c FROM {datasource_id}_quarantine FORMAT JSON")
        row = a["data"][0]
        self.assertEqual(int(row["c"]), expected_rows_quarantine)

        a = exec_sql(u["database"], f"select * from {datasource_id} FORMAT JSON")
        meta = a["meta"]
        meta_types = set(list([x["type"] for x in meta]))
        self.assertEqual(meta_types, {"String"})

        # statistics
        await self.assert_stats_async(datasource_id, token, expected_rows, 67157)

        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": result["datasource"]["name"],
                },
                {
                    "event_type": "append",
                    "datasource_name": result["datasource"]["name"],
                    "rows": expected_rows,
                    "rows_quarantine": expected_rows_quarantine,
                    "options": {
                        "source": "stream",
                    },
                },
            ]
        )


class TestAPIDatasourceImportUrl(TestAPIDatasourceBase):
    @tornado.testing.gen_test
    async def test_import_parquet_url_not_download_metadata_if_not_head(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.DATASOURCES_CREATE)
        ds_name = "test_append_messy" + str(uuid.uuid4())[:8]
        params = {
            "token": token,
            "name": ds_name,
            "schema": "id UInt32 `json:$.id`, name String `json:$.name`, date DateTime `json:$.date`",
            "format": "parquet",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"

        response = await self.fetch_async(create_url, method="POST", body="")
        result = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(result["datasource"]["name"], ds_name)
        self.expect_ops_log(
            {"event_type": "create", "datasource_name": ds_name, "options": {"source": "schema", "format": "parquet"}},
        )

        with patch(
            "tinybird.views.shared.utils.UrlUtils.check_file_size_limit", return_value=AsyncMock
        ) as mock_check_file_size_limit:
            with patch(
                "tinybird.job.ch_get_parquet_metadata_from_url", return_value=AsyncMock
            ) as mock_ch_get_parquet_metadata_from_url:
                url = f"{HTTP_ADDRESS}/hello_world.parquet"
                mock_check_file_size_limit.return_value = (1, False)
                mock_ch_get_parquet_metadata_from_url.return_value = CHParquetMetadata(0, 0, 0, 0)
                import_url = f"/v0/datasources?token={token}&name={ds_name}&url={quote(url,safe='')}&mode=append&type_guessing=false&format=parquet"
                response = await self.fetch_async(import_url, method="POST", body="")
                self.assertEqual(response.code, 200)
                job = await self.get_finalised_job_async(json.loads(response.body)["id"])
                self.assertEqual(job.status, "done")
                assert not mock_ch_get_parquet_metadata_from_url.called

        self.expect_ops_log(
            [
                {"event_type": "append", "datasource_name": ds_name, "options": {"source": url, "format": "parquet"}},
            ]
        )


class TestAPIDatasourceImportBatch(TestAPIDatasourceBase):
    @patch.object(CSVImporterSettings, "CHUNK_SIZE", 1024 * 1024 * 32)
    @patch.object(CSVImporterSettings, "MIN_PARTS", 4)
    @patch.object(CSVImporterSettings, "MAX_MEMORY_IN_PROCESS_QUEUE", 1024 * 1024 * 32)
    @patch.object(CSVImporterSettings, "MAX_WAIT_TO_EMPTY_QUEUE_TIME_SECONDS", 3)
    @patch.object(CsvChunkQueue, "blocks_waiting", return_value=10)
    @tornado.testing.gen_test
    @pytest.mark.xfail(reason="Need to fix issue https://gitlab.com/tinybird/analytics/-/issues/10418")
    async def test_max_time_waiting_for_process_queue_reached(self, blocks_waiting_mock):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        csv_url = "https://storage.googleapis.com/tinybird-demo/stock_prices_800K.csv"

        import_url = f"/v0/datasources?token={token}&url={csv_url}&name=import_1"
        response = await self.fetch_async(import_url, method="POST", body="")
        result = json.loads(response.body)
        job1_id = result["id"]

        import_url = f"/v0/datasources?token={token}&url={csv_url}&name=import_2"
        response = await self.fetch_async(import_url, method="POST", body="")
        result = json.loads(response.body)
        job2_id = result["id"]

        self.assertEqual(response.code, 200)

        await self.get_finalised_job_async(job1_id)
        job2 = await self.get_finalised_job_async(job2_id)

        self.assertEqual(response.code, 200)
        self.assertEqual(job2.status, "error", str(job2))
        expected_errors = ["Max time waiting for process queue to be reduced reached (3 seconds)"]
        self.assertIn(job2["errors"][0], expected_errors)

    @patch("tinybird.default_timeouts.DEFAULT_SOCKET_CONNECT_TIMEOUT", 1)
    @patch("tinybird.default_timeouts.DEFAULT_SOCKET_READ_TIMEOUT", 1)
    @tornado.testing.gen_test
    async def test_import_ndjson_with_read_timeout(self):
        job = await self.timeout_job()
        self.assertEqual(job.status, "error")
        self.assertTrue("Timeout" in job._result["error"])
        self.assertTrue(job.id in job._result["error"])
        self.assertRegex(job._result["error"], r"http://.*/events.ndjson")

    @patch("tinybird.default_timeouts.DEFAULT_SOCKET_TOTAL_TIMEOUT", 1)
    @tornado.testing.gen_test
    async def test_import_ndjson_with_total_timeout(self):
        job = await self.timeout_job()
        self.assertEqual(job.status, "error")
        self.assertTrue("Timeout" in job._result["error"])
        self.assertTrue(job.id in job._result["error"])
        self.assertRegex(job._result["error"], r"http://.*/events.ndjson")

    @patch.object(CSVImporterSettings, "MAX_MEMORY_IN_PROCESS_QUEUE", 1024 * 1024 * 56)
    @patch.object(CSVImporterSettings, "MAX_WAIT_TO_EMPTY_QUEUE_TIME_SECONDS", 0)
    @tornado.testing.gen_test
    async def test_max_time_waiting_to_reduce_fetch_reached(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        csv_url = "https://storage.googleapis.com/tinybird-demo/stock_prices_800K.csv"
        import_url = f"/v0/datasources?token={token}&url={csv_url}"

        response = await self.fetch_async(import_url, method="POST", body="")
        result = json.loads(response.body)
        job_id = result["id"]

        self.assertEqual(response.code, 200)

        job = await self.get_finalised_job_async(job_id)

        self.assertEqual(response.code, 200)
        self.assertEqual(job.status, "error", str(job))
        expected_error = "Max time waiting to reduce to fetch more items reached (0 seconds)"
        self.assertEqual(job["errors"], [expected_error])

    @patch("tinybird.csv_importer.fetch_csv_range", side_effect=Exception("Fetch Exception"))
    @tornado.testing.gen_test
    async def test_multiple_blocks_error_fetch(self, exception_mock):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        csv_url = "https://storage.googleapis.com/tinybird-demo/stock_prices_800K.csv"
        import_url = f"/v0/datasources?token={token}&url={csv_url}"

        response = await self.fetch_async(import_url, method="POST", body="")
        result = json.loads(response.body)
        job_id = result["id"]

        job = await self.get_finalised_job_async(job_id, debug="blocks, hook_log")

        self.assertEqual(response.code, 200)
        self.assertEqual(job.status, "error", str(job))

        self.assertEqual(
            job["error"], "There was an error when attempting to import your data. Check 'errors' for more information."
        )
        self.assertEqual(job["errors"], ["There are blocks with errors", "Fetch Exception"])

    @patch("tinybird.csv_importer.fetch_csv_block_stream", side_effect=Exception("Fetch Exception"))
    @tornado.testing.gen_test
    async def test_single_block_error_fetch(self, exception_mock):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        csv_url = f"{HTTP_ADDRESS}/trans.csv"
        import_url = f"/v0/datasources?token={token}&url={csv_url}"

        response = await self.fetch_async(import_url, method="POST", body="")
        result = json.loads(response.body)
        job_id = result["id"]

        job = await self.get_finalised_job_async(job_id, debug="blocks, hook_log")

        self.assertEqual(response.code, 200)
        self.assertEqual(job.status, "error", str(job))

        self.assertEqual(
            job["error"], "There was an error when attempting to import your data. Check 'errors' for more information."
        )
        self.assertEqual(job["errors"], ["There are blocks with errors", "Fetch Exception"])

    @tornado.testing.gen_test
    async def test_url_existing_datasource(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        csv_url = f"{HTTP_ADDRESS}/trans.csv"
        import_url = f"/v0/datasources?token={token}&url={csv_url}"

        response = await self.fetch_async(import_url, method="POST", body="")
        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(response.code, 200)

        response = await self.fetch_async(import_url, method="POST", body="")
        err_response = json.loads(response.body)
        self.assertEqual(response.code, 400)
        self.assertEqual(err_response["error"], 'Data Source "trans" already exists, use mode=append')

        self.delete_table(u["database"], job["datasource"]["id"])

    @tornado.testing.gen_test
    async def test_wrong_scheme(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        response = await self.fetch_async(
            "/v0/datasources?token=%s&url=test://example.com" % token, method="POST", body=""
        )
        self.assertTrue("error" in json.loads(response.body))
        self.assertEqual(response.code, 400)

    @tornado.testing.gen_test
    async def test_invalid_mode_handling(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        response = await self.fetch_async("/v0/datasources?token=%s&mode=invalid" % token, method="POST", body="")
        self.assertTrue("error" in json.loads(response.body))
        self.assertEqual(response.code, 400)

    @tornado.testing.gen_test
    async def test_import_body_compressed(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        name = "test_import_body_compressed"
        with fixture_file("yt_1000.csv.gz", mode="rb") as fd:
            response = await self.fetch_full_body_upload_async(
                f"/v0/datasources?token=%s&name={name}" % token, fd, _headers={"Content-Encoding": "gzip"}
            )
        self.assertEqual(response.code, 200)
        b = json.loads(response.body)
        self.assertEqual(b["datasource"]["name"], name)

        expected_rows = 328
        expected_rows_quarantine = 1000 - expected_rows - 1 - 1  # 1000 - imported - empty - header

        self.assertEqual(b["invalid_lines"], 0)
        self.assertEqual(b["quarantine_rows"], expected_rows_quarantine)

        a = exec_sql(u["database"], "select count(1) c from `%s` FORMAT JSON" % b["datasource"]["id"])
        row = a["data"][0]
        self.assertEqual(int(row["c"]), expected_rows)

        a = exec_sql(u["database"], "select count(1) c from `%s_quarantine` FORMAT JSON" % b["datasource"]["id"])
        row = a["data"][0]
        self.assertEqual(int(row["c"]), expected_rows_quarantine)

        await self.assert_stats_async(name, token, expected_rows, 13278)

        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": name,
                },
                {
                    "event_type": "append",
                    "datasource_name": name,
                    "rows": expected_rows,
                    "rows_quarantine": expected_rows_quarantine,
                    "options": {
                        "source": "full_body",
                    },
                },
            ]
        )

    @tornado.testing.gen_test
    async def test_import_body(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        name = "true_test_import_body"
        with fixture_file("yt_1000.csv") as fd:
            response = await self.fetch_full_body_upload_async(f"/v0/datasources?token=%s&name={name}" % token, fd)
        self.assertEqual(response.code, 200)
        b = json.loads(response.body)
        self.assertEqual(b["datasource"]["name"], name)

        expected_rows = 328
        expected_rows_quarantine = 1000 - expected_rows - 1 - 1  # 1000 - imported - empty - header

        self.assertEqual(b["invalid_lines"], 0)
        self.assertEqual(b["quarantine_rows"], expected_rows_quarantine)

        a = exec_sql(u["database"], "select count(1) c from `%s` FORMAT JSON" % b["datasource"]["id"])
        row = a["data"][0]
        self.assertEqual(int(row["c"]), expected_rows)

        a = exec_sql(u["database"], "select count(1) c from `%s_quarantine` FORMAT JSON" % b["datasource"]["id"])
        row = a["data"][0]
        self.assertEqual(int(row["c"]), expected_rows_quarantine)
        self.delete_table(u["database"], b["datasource"]["id"])

        await self.assert_stats_async(name, token, expected_rows, 13278)
        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": name,
                },
                {
                    "event_type": "append",
                    "datasource_name": name,
                    "rows": expected_rows,
                    "rows_quarantine": expected_rows_quarantine,
                    "options": {
                        "source": "full_body",
                    },
                },
            ]
        )

    @tornado.testing.gen_test
    async def test_import_body_limit(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        row = '"2020-01-01 00:00:00","test","3e25a061-63d1-41bb-8e80-d2e5fb034b1e"\n'
        target_size = 8 * (1024**2)
        how_many_rows = (target_size // len(row)) + 1
        s = StringIO(row * how_many_rows)

        params = {"mode": "create", "token": token, "name": "test_import_body_limit"}
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_full_body_upload_async(create_url, s)

        self.assertEqual(response.code, 413, str(response))
        result = json.loads(response.body)
        self.assertRegex(
            result["error"],
            r"The message-body is too large\. For requests larger than 8MB, you should use a multipart\/form-data request. Use curl -F csv=@file\.csv.*",
        )

        span = self.get_span(create_url)
        self.assertEqual(span.get("status_code"), 413)
        self.assertEqual(span.get("method"), "POST")
        self.assertRegex(span.get("error"), "The message-body is too large.*")

    @tornado.testing.gen_test
    async def test_quarantine_format(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        with fixture_file("yt_1000.csv") as fd:
            response = await self.fetch_full_body_upload_async(
                "/v0/datasources?token=%s&name=test_quarantine_format" % token, fd
            )
        self.assertEqual(response.code, 200)
        b = json.loads(response.body)
        self.assertTrue(b["datasource"]["name"], "test")

        quarantine_result = exec_sql(
            u["database"],
            f"SELECT * FROM `{b['datasource']['id']}_quarantine` WHERE vendor_id like '%VTS%' FORMAT JSON",
        )
        meta = quarantine_result["meta"]
        quarantine_columns = ("c__error_column", "c__error", "insertion_date")
        for c in quarantine_columns:
            self.assertIn(c, [c["name"] for c in meta])
        for c in meta:
            if c["name"] not in quarantine_columns:
                self.assertEqual(c["type"], "Nullable(String)")
        row = quarantine_result["data"][0]
        self.assertEqual(row["vendor_id"], "VTS")

    @tornado.testing.gen_test
    async def test_import_body_no_datasource_name(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        with fixture_file("yt_1000.csv") as fd:
            response = await self.fetch_full_body_upload_async("/v0/datasources?token=%s" % token, fd)
        b = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertTrue("imported_" in b["datasource"]["name"])
        expected_rows = 328
        expected_rows_quarantine = 1000 - expected_rows - 1 - 1  # 1000 - imported - empty - header

        a = exec_sql(u["database"], "select count(1) c from %s FORMAT JSON" % b["datasource"]["id"])
        row = a["data"][0]
        self.assertEqual(int(row["c"]), expected_rows)

        a = exec_sql(u["database"], "select count(1) c from `%s_quarantine` FORMAT JSON" % b["datasource"]["id"])
        row = a["data"][0]
        self.assertEqual(int(row["c"]), expected_rows_quarantine)

        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": b["datasource"]["name"],
                },
                {
                    "event_type": "append",
                    "datasource_name": b["datasource"]["name"],
                    "rows": expected_rows,
                    "rows_quarantine": expected_rows_quarantine,
                    "options": {
                        "source": "full_body",
                    },
                },
            ]
        )

        self.delete_table(u["database"], b["datasource"]["id"])

    @tornado.testing.gen_test
    async def test_import_body_trans(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        with fixture_file("trans.csv") as fd:
            response = await self.fetch_full_body_upload_async(
                "/v0/datasources?token=%s&name=test_import_body_trans" % token, fd
            )
        b = json.loads(response.body)
        self.assertEqual(response.code, 200)

        self.assertEqual(b["invalid_lines"], 0)
        self.assertEqual(b["quarantine_rows"], 0)

        expected_rows = 7

        a = exec_sql(u["database"], "select count(1) c from %s FORMAT JSON" % b["datasource"]["id"])
        row = a["data"][0]
        self.assertEqual(int(row["c"]), expected_rows)
        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": b["datasource"]["name"],
                },
                {
                    "event_type": "append",
                    "datasource_name": b["datasource"]["name"],
                    "rows": expected_rows,
                    "options": {
                        "source": "full_body",
                    },
                },
            ]
        )
        self.delete_table(u["database"], b["datasource"]["id"])

    @tornado.testing.gen_test
    async def test_import_can_handle_404_urls(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        urls = [
            f"{HTTP_ADDRESS}/jorgesancha/0.csv",
            f"{HTTP_ADDRESS}/jorgesancha/3dad2c4f9f03edc2f5d9d6d7d3a56a35/raw/af563cd31ad4b8142d5b8ff43d0ed14e09aeb8d6/s.csv",
        ]
        for i, url_404 in enumerate(urls):
            response = await self.fetch_async(url_404)
            self.assertEqual(response.code, 404)

            ds_name = f"places_{i}"
            import_url = f"/v0/datasources?token={token}&name={ds_name}&url={quote(url_404,safe='')}"

            response = await self.fetch_async(import_url, method="POST", body="")
            # self.assertEqual(response.body, '')
            self.assertEqual(response.code, 200)

            job = await self.get_finalised_job_async(json.loads(response.body)["id"])
            self.assertEqual(job["kind"], "import")
            self.assertEqual(job["id"], job["job_id"])
            self.assertEqual(job["id"], job["import_id"])
            self.assertEqual(job["status"], "error")
            expected_error = rf"Could not fetch URL. 404 Client Error:.*{url_404}"
            self.assertEqual(
                job["error"],
                "There was an error when attempting to import your data. Check 'errors' for more information.",
            )
            self.assertRegex(job["errors"][0], expected_error)
            self.expect_ops_log(
                {
                    "event_type": "create",
                    "datasource_name": ds_name,
                    "result": "error",
                    "error": job["errors"][0],
                    "options": {"source": url_404},
                },
            )

    @tornado.testing.gen_test
    async def test_import_empty_csv_body(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        import_url = f"/v0/datasources?token={token}&name=test_import_empty_csv_body"

        response = await self.fetch_async(import_url, method="POST", body="")
        self.assertEqual(response.code, 400)
        import_response = json.loads(response.body)
        self.assertEqual(import_response["error"], "cannot create table with empty file")

    @tornado.testing.gen_test
    async def test_import_empty_csv(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        csv_url = self.get_url_for_sql("select ''")
        response = await self.fetch_async(csv_url)

        import_url = f"/v0/datasources?token={token}&name=test_empty_url&url={quote(csv_url,safe='')}"

        response = await self.fetch_async(import_url, method="POST", body="")
        # self.assertEqual(response.body, '')
        self.assertEqual(response.code, 200)
        import_response = json.loads(response.body)
        self.assertEqual(import_response["job_id"], import_response["id"])
        self.assertEqual(import_response["id"], import_response["import_id"])
        job_response = import_response["job"]
        self.assertEqual(job_response["kind"], "import")

        job = await self.get_finalised_job_async(import_response["job_id"])

        self.assertEqual(job.status, "error")
        self.expect_ops_log(
            {
                "event_type": "create",
                "datasource_name": "test_empty_url",
                "result": "error",
                "options": {"source": csv_url},
            },
        )

    @tornado.testing.gen_test
    async def test_import_empty_csv_from_200(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        name = "test_create_empty_url"
        csv_url = f"{HTTP_ADDRESS}/empty.csv"
        params = {
            "token": token,
            "name": name,
            "url": csv_url,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        job = await self.get_finalised_job_async(json.loads(response.body)["id"])

        self.assertEqual(job.status, "error")

        response = await self.fetch_async(f"/v0/jobs?token={token}")
        jobs = json.loads(response.body)["jobs"]
        j = next((j for j in jobs if j["id"] == job.id), None)
        self.assertIsNotNone(j)
        self.assertEqual(j["status"], "error")

        self.expect_ops_log(
            {"event_type": "create", "datasource_name": name, "result": "error", "options": {"source": csv_url}},
        )

    @tornado.testing.gen_test
    async def test_import_with_pipe_name(self):
        self.create_test_datasource()
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        csv_url = self.get_url_for_sql("select '1,2,3,4' format CSV")
        import_url = f"/v0/datasources?token={token}&name=test_pipe&url={quote(csv_url,safe='')}"

        response = await self.fetch_async(import_url, method="POST", body="")
        self.assertEqual(response.code, 400)

    @tornado.testing.gen_test
    async def test_import_with_admin_token(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        csv_url = self.get_url_for_sql("select '1,2,3,4' format CSV")
        import_url = f"/v0/datasources?token={token}&name=test_import_with_admin_token&url={quote(csv_url,safe='')}"

        response = await self.fetch_async(import_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        import_response = json.loads(response.body)
        self.assertEqual(import_response["job_id"], import_response["id"])
        self.assertEqual(import_response["id"], import_response["import_id"])
        job_response = import_response["job"]
        self.assertEqual(job_response["kind"], "import")

        job = await self.get_finalised_job_async(import_response["job_id"])
        self.assertEqual(job.status, "done")
        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": "test_import_with_admin_token",
                },
                {
                    "event_type": "append",
                    "datasource_name": "test_import_with_admin_token",
                    "rows": 1,
                    "options": {
                        "source": csv_url,
                    },
                },
            ]
        )

        # append
        csv_url = self.get_url_for_sql("select '1,2,3,4' format CSV")
        import_url = (
            f"/v0/datasources?token={token}&name=test_import_with_admin_token&url={quote(csv_url,safe='')}&mode=append"
        )

        response = await self.fetch_async(import_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done")
        self.expect_ops_log(
            {
                "event_type": "append",
                "datasource_name": "test_import_with_admin_token",
                "rows": 1,
                "options": {
                    "source": csv_url,
                },
            },
        )

    @tornado.testing.gen_test
    async def test_import_invalid_url(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        csv_url = "invalid_url"
        import_url = f"/v0/datasources?token={token}&name=trans&url={csv_url}"

        response = await self.fetch_async(import_url, method="POST", body="")
        self.assertEqual(response.code, 400)
        self.assertEqual(response.body, b'{"error": "Invalid url"}')

    @tornado.testing.gen_test
    async def test_import_url(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        csv_url = f"{HTTP_ADDRESS}/trans.csv"
        import_url = f"/v0/datasources?token={token}&name=trans&url={csv_url}"

        response = await self.fetch_async(import_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        import_response = json.loads(response.body)
        self.assertEqual(import_response["job_id"], import_response["id"])
        self.assertEqual(import_response["id"], import_response["import_id"])
        job_response = import_response["job"]
        self.assertEqual(job_response["kind"], "import")

        job = await self.get_finalised_job_async(import_response["job_id"], debug="blocks, hook_log")
        self.assertEqual(job.status, "done")
        expected_rows = 7
        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": "trans",
                },
                {
                    "event_type": "append",
                    "datasource_name": "trans",
                    "rows": expected_rows,
                    "options": {
                        "source": csv_url,
                    },
                },
            ]
        )

        # asset blocks
        blocks = job["blocks"]
        self.assertEqual(len(blocks), 1)
        block = blocks[0]
        self.assertEqual(block["process_return"][0]["parser"], "clickhouse")

        # check hooks
        self.assertIn("hook_log", job)
        expected_hook_operations = ("before_create", "after_create", "before_append", "after_append")
        for entry in job["hook_log"]:
            self.assertTrue(entry["operation"] in expected_hook_operations)
            self.assertNotIn("user_id", entry)
            self.assertNotIn("user_email", entry)

        # counts
        a = exec_sql(u["database"], f"SELECT count() c FROM {job['datasource']['id']} FORMAT JSON")
        row = a["data"][0]
        self.assertEqual(int(row["c"]), expected_rows)
        self.delete_table(u["database"], job["datasource"]["id"])
        # statistics
        await self.assert_stats_async("trans", token, expected_rows, 1872)

    @tornado.testing.gen_test
    async def test_import_url_yt(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        csv_url = f"{HTTP_ADDRESS}/yt_1000.csv"
        import_url = f"/v0/datasources?token={token}&name=yt_1000&url={csv_url}"

        response = await self.fetch_async(import_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        job = await self.get_finalised_job_async(json.loads(response.body)["id"], debug="blocks")
        self.assertEqual(job.status, "done")
        expected_rows = 328
        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": "yt_1000",
                },
                {
                    "event_type": "append",
                    "datasource_name": "yt_1000",
                    "rows": expected_rows,
                    "options": {
                        "source": csv_url,
                    },
                },
            ]
        )
        blocks = job["blocks"]
        self.assertEqual(len(blocks), 1)
        a = exec_sql(u["database"], f"SELECT count() c FROM {job['datasource']['id']} FORMAT JSON")
        row = a["data"][0]
        self.assertEqual(int(row["c"]), expected_rows)
        self.delete_table(u["database"], job["datasource"]["id"])

    @tornado.testing.gen_test
    async def test_import_with_errors(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        csv_url = f"{HTTP_ADDRESS}/user_events.csv"
        import_url = f"/v0/datasources?token={token}&name=user_events&url={csv_url}"

        response = await self.fetch_async(import_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        job = await self.get_finalised_job_async(json.loads(response.body)["id"], debug="blocks")

        self.assertEqual(job.status, "error")
        self.assertEqual(
            job.error, "There was an error when attempting to import your data. Check 'errors' for more information."
        )
        self.assertTrue("There are blocks with errors" in job.errors[0])
        self.assertTrue("CANNOT_PARSE_DATETIME" in job.errors[0])
        self.assertTrue("[Error]" in job.errors[1])

    @tornado.testing.gen_test
    async def test_import_url_from_body_params(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        name = "test_import_url_body_param"
        params = {
            "token": token,
            "name": name,
        }
        csv_url = self.get_url_for_sql("select 1, 2, 3, 4 format CSV")
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body=urlencode({"url": csv_url}))
        self.assertEqual(response.code, 200, response.body)

        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done", str(job))

        response = await self.fetch_async(f"/v0/jobs?token={token}")
        jobs = json.loads(response.body)["jobs"]
        j = next((j for j in jobs if j["id"] == job.id), None)
        self.assertIsNotNone(j)
        self.assertEqual(j["status"], "done")

        self.expect_ops_log(
            [
                {"event_type": "create", "datasource_name": name, "options": {"source": csv_url}},
                {"event_type": "append", "datasource_name": name, "options": {"source": csv_url}},
            ]
        )

    @tornado.testing.gen_test
    async def test_append_and_create(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.DATASOURCES_CREATE)
        csv_url = self.get_url_for_sql("select '1,2,3,4' format CSV")

        async def _send_data():
            import_url = (
                f"/v0/datasources?token={token}&name=test_append_and_create&url={quote(csv_url,safe='')}&mode=append"
            )

            response = await self.fetch_async(import_url, method="POST", body="")
            self.assertEqual(response.code, 200)

            job = await self.get_finalised_job_async(json.loads(response.body)["id"])
            self.assertEqual(job.status, "done")

        # create
        await _send_data()
        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": "test_append_and_create",
                },
                {
                    "event_type": "append",
                    "datasource_name": "test_append_and_create",
                    "rows": 1,
                    "options": {
                        "source": csv_url,
                    },
                },
            ]
        )
        # append
        await _send_data()
        self.expect_ops_log(
            {
                "event_type": "append",
                "datasource_name": "test_append_and_create",
                "rows": 1,
                "options": {
                    "source": csv_url,
                },
            },
        )

    @tornado.testing.gen_test
    async def test_append_and_create_no_autoguess_headers_second_time(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.DATASOURCES_CREATE)

        async def _send_data(first=True):
            if first:
                with fixture_file("pedro_prods.csv") as fd:
                    response = await self.fetch_full_body_upload_async(
                        "/v0/datasources?token=%s&name=test_append_and_create&mode=create" % token, fd
                    )
            else:
                with fixture_file("maicop_prods.csv") as fd:
                    response = await self.fetch_full_body_upload_async(
                        "/v0/datasources?token=%s&name=test_append_and_create2&mode=append" % token, fd
                    )

            self.assertEqual(response.code, 200)

        # create
        await _send_data()
        expected_rows_without_header = 94
        expected_appended_rows_without_header = 811
        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": "test_append_and_create",
                },
                {
                    "event_type": "append",
                    "datasource_name": "test_append_and_create",
                    "rows": expected_rows_without_header,
                    "options": {
                        "source": "full_body",
                    },
                },
            ]
        )

        # rename dataset to avoid race condition when running ops log expectations
        old_id = Users.get_datasource(u, "test_append_and_create").id
        await self.fetch_async(
            "/v0/datasources/test_append_and_create?name=test_append_and_create2&token=%s" % token,
            method="PUT",
            body="",
        )
        self.expect_ops_log(
            {
                "event_type": "rename",
                "datasource_id": old_id,
                "datasource_name": "test_append_and_create2",
                "options": {
                    "old_name": "test_append_and_create",
                    "new_name": "test_append_and_create2",
                },
            }
        )

        # append second time
        await _send_data(first=False)
        self.expect_ops_log(
            {
                "event_type": "append",
                "datasource_name": "test_append_and_create2",
                "rows": expected_appended_rows_without_header,
                "options": {
                    "source": "full_body",
                },
            },
        )

    @tornado.testing.gen_test
    async def test_append_and_create_no_autoguess_headers_different_schema(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(u, "test", scopes.DATASOURCES_CREATE)

        async def _send_data(first=True):
            if first:
                with fixture_file("pedro_prods2.csv") as fd:
                    response = await self.fetch_full_body_upload_async(
                        "/v0/datasources?token=%s&name=test_append_and_create&mode=create" % token, fd
                    )
            else:
                with fixture_file("maicop_prods2.csv") as fd:
                    response = await self.fetch_full_body_upload_async(
                        "/v0/datasources?token=%s&name=test_append_and_create2&mode=append" % token, fd
                    )

            self.assertEqual(response.code, 200)

        # create
        await _send_data()
        expected_rows_without_header = 14
        expected_appended_rows_without_header = 4
        expected_rows_quarantine = 1
        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": "test_append_and_create",
                },
                {
                    "event_type": "append",
                    "datasource_name": "test_append_and_create",
                    "rows": expected_rows_without_header,
                    "options": {
                        "source": "full_body",
                    },
                },
            ]
        )

        # rename dataset to avoid race condition when running ops log expectations
        old_id = Users.get_datasource(u, "test_append_and_create").id
        await self.fetch_async(
            "/v0/datasources/test_append_and_create?name=test_append_and_create2&token=%s" % token,
            method="PUT",
            body="",
        )
        self.expect_ops_log(
            {
                "event_type": "rename",
                "datasource_id": old_id,
                "datasource_name": "test_append_and_create2",
                "options": {
                    "old_name": "test_append_and_create",
                    "new_name": "test_append_and_create2",
                },
            }
        )

        # append second time
        await _send_data(first=False)
        self.expect_ops_log(
            {
                "event_type": "append",
                "datasource_name": "test_append_and_create2",
                "rows": expected_appended_rows_without_header,
                "rows_quarantine": expected_rows_quarantine,
                "options": {
                    "source": "full_body",
                },
            },
        )

    @tornado.testing.gen_test
    async def test_append_and_create_with_just_append_permissions(self):
        self.create_test_datasource()
        u = Users.get_by_id(self.WORKSPACE_ID)
        ds = Users.get_datasource(u, "test_table")
        token = Users.add_token(u, "test", scopes.DATASOURCES_APPEND, ds.id)
        csv_url = self.get_url_for_sql("select '1,2,3,4' format CSV")
        import_url = (
            f"/v0/datasources?token={token}&name=test_append_and_create&url={quote(csv_url,safe='')}&mode=append"
        )

        response = await self.fetch_async(import_url, method="POST", body="")
        self.assertEqual(response.code, 403)

    @tornado.testing.gen_test
    async def test_import_fails_for_same_url_guessed_name(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        def validate_imported_rows(datasource):
            a = exec_sql(u["database"], f"SELECT count() c FROM {datasource} FORMAT JSON")
            row = a["data"][0]
            self.assertEqual(int(row["c"]), 7)

        csv_url = f"{HTTP_ADDRESS}/trans.csv"
        import_url = f"/v0/datasources?token={token}&url={csv_url}"
        response = await self.fetch_async(import_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done")
        datasource = job["datasource"]["id"]
        validate_imported_rows(datasource)

        response = await self.fetch_async(import_url, method="POST", body="")
        self.assertEqual(response.code, 400)
        self.assertEqual(json.loads(response.body)["error"], 'Data Source "trans" already exists, use mode=append')
        validate_imported_rows(datasource)
        self.delete_table(u["database"], datasource)

    # user db sizes tracking
    @tornado.testing.gen_test
    async def test_import_body_and_drop_track_user_db_size(self):
        u = Users.get_by_id(self.WORKSPACE_ID)

        initial_sizes = get_db_size_records(u)
        self.assertEqual(initial_sizes, [])

        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        with fixture_file("trans.csv") as fd:
            response = await self.fetch_full_body_upload_async(
                "/v0/datasources?token=%s&name=test_import_body" % token, fd
            )
        self.assertEqual(response.code, 200)
        b = json.loads(response.body)
        datasource_name = b["datasource"]["name"]
        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": "test_import_body",
                },
                {
                    "event_type": "append",
                    "datasource_name": "test_import_body",
                    "rows": 7,
                    "options": {
                        "source": "full_body",
                    },
                },
            ]
        )

        t = WorkspaceDatabaseUsageTracker()
        t.track_database_usage([u])
        sizes_after_import = get_db_size_records(u)
        self.assertEqual(sizes_after_import[0]["database"], u.database)
        self.assertEqual(sizes_after_import[0]["rows"], 7)
        self.assertAlmostEqual(sizes_after_import[0]["bytes_on_disk"], 1216, delta=1216 * 0.2)

        with fixture_file("trans.csv") as fd:
            response = await self.fetch_full_body_upload_async(
                "/v0/datasources?token=%s&name=test_import_2" % token, fd
            )
        self.assertEqual(response.code, 200)
        b = json.loads(response.body)
        datasource_name = b["datasource"]["name"]
        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": datasource_name,
                },
                {
                    "event_type": "append",
                    "datasource_name": datasource_name,
                    "rows": 7,
                    "options": {
                        "source": "full_body",
                    },
                },
            ]
        )

        t = WorkspaceDatabaseUsageTracker()
        t.track_database_usage([u])
        sizes_after_import = get_db_size_records(u)
        self.assertEqual(sizes_after_import[0]["database"], u.database)
        self.assertEqual(sizes_after_import[0]["rows"], 14)
        self.assertAlmostEqual(sizes_after_import[0]["bytes_on_disk"], 2432, delta=2432 * 0.2)

        token = Users.add_token(u, "test", scopes.ADMIN)
        response = await self.fetch_async(f"/v0/datasources/{datasource_name}?token={token}", method="DELETE")
        self.assertEqual(response.code, 204)
        self.assertEqual(None, Users.get_datasource(u, datasource_name))
        self.expect_ops_log(
            {
                "event_type": "delete",
                "datasource_name": datasource_name,
                "rows": 7,
            },
        )

        public_user = public.get_public_user()
        ds = Users.get_datasource(public_user, "db_usage")

        def assert_usage():
            query = f"""select
                timestamp, max(rows) max_rows, max(bytes_on_disk) max_total_bytes
            from {ds.id}
            where database = '{u.database}'
            group by timestamp
            order by max_rows desc limit 1
            FORMAT JSON"""
            results = exec_sql(public_user.database, query, database_server=public_user.database_server)["data"]
            self.assertEqual(results[0]["max_rows"], "14")
            self.assertLessEqual(int(results[0]["max_total_bytes"]), 3744)

        poll(assert_usage)

    @tornado.testing.gen_test
    async def test_import_url_tracks_user_db_size(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        sizes = get_db_size_records(u)
        self.assertEqual(sizes, [])

        csv_url = f"{HTTP_ADDRESS}/trans.csv"
        import_url = f"/v0/datasources?token={token}&url={csv_url}"
        response = await self.fetch_async(import_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done")

        t = WorkspaceDatabaseUsageTracker()
        t.track_database_usage([u])
        sizes_after_import = get_db_size_records(u)
        self.assertNotEqual(sizes, sizes_after_import)
        self.assertEqual(sizes_after_import[0]["rows"], 7)

    @tornado.testing.gen_test
    async def test_create_streaming2(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        url = self.get_url(f"/v0/datasources?token={token}")

        with fixture_file("yt_1000.csv", mode="rb") as fd:
            response = await self.fetch_stream_upload_async(url, fd)
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)

        expected_rows = 328
        expected_rows_quarantine = 1000 - expected_rows - 1 - 1  # 1000 - imported - empty - header

        datasource_id = result["datasource"]["id"]
        a = exec_sql(u["database"], f"SELECT count() c FROM {datasource_id} FORMAT JSON")
        row = a["data"][0]
        self.assertEqual(int(row["c"]), expected_rows)
        a = exec_sql(u["database"], f"SELECT count() c FROM {datasource_id}_quarantine FORMAT JSON")
        row = a["data"][0]
        self.assertEqual(int(row["c"]), expected_rows_quarantine)

        # statistics
        await self.assert_stats_async(datasource_id, token, expected_rows, 13278)

        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": result["datasource"]["name"],
                },
                {
                    "event_type": "append",
                    "datasource_name": result["datasource"]["name"],
                    "rows": expected_rows,
                    "rows_quarantine": expected_rows_quarantine,
                    "options": {
                        "source": "stream",
                    },
                },
            ]
        )

    @tornado.testing.gen_test
    async def test_create_csv_with_quoted_linebreaks(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        url = self.get_url(f"/v0/datasources?token={token}")

        with fixture_file("shopify_export.csv", mode="rb") as fd:
            response = await self.fetch_stream_upload_async(url, fd)
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)

        expected_rows = 183
        expected_rows_quarantine = 0

        datasource_id = result["datasource"]["id"]
        a = exec_sql(u["database"], f"SELECT count() c FROM {datasource_id} FORMAT JSON")
        row = a["data"][0]
        self.assertEqual(int(row["c"]), expected_rows)
        a = exec_sql(u["database"], f"SELECT count() c FROM {datasource_id}_quarantine FORMAT JSON")
        row = a["data"][0]
        self.assertEqual(int(row["c"]), expected_rows_quarantine)

        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": result["datasource"]["name"],
                },
                {
                    "event_type": "append",
                    "datasource_name": result["datasource"]["name"],
                    "rows": expected_rows,
                    "rows_quarantine": expected_rows_quarantine,
                    "options": {
                        "source": "stream",
                    },
                },
            ]
        )

        a = exec_sql(u["database"], f"SELECT * FROM {datasource_id} FORMAT JSON")
        meta = a["meta"]
        names = [c["name"] for c in meta]
        types = [c["type"] for c in meta]

        self.assertEqual(
            names,
            [
                "sku",
                "title",
                "description",
                "link",
                "image_link",
                "brand",
                "body_html",
                "created_at",
                "product_id",
                "updated_at",
                "redirect_url",
                "condition",
                "slug",
                "availability",
                "price",
                "sale_price",
                "image_link1",
                "image_link2",
                "image_link3",
                "image_link4",
            ],
        )
        self.assertEqual(
            types,
            [
                "String",
                "String",
                "String",
                "String",
                "String",
                "String",
                "String",
                "DateTime",
                "Int64",
                "DateTime",
                "String",
                "String",
                "String",
                "String",
                "String",
                "Nullable(String)",
                "Nullable(String)",
                "Nullable(String)",
                "Nullable(String)",
                "Nullable(String)",
            ],
        )

    @tornado.testing.gen_test
    async def test_create_streaming_compressed(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        url = self.get_url(f"/v0/datasources?token={token}")

        with fixture_file("yt_1000.csv.gz", mode="rb") as fd:
            response = await self.fetch_stream_upload_async(url, fd, _headers={"Content-Encoding": "gzip"})
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)

        expected_rows = 328
        expected_rows_quarantine = 1000 - expected_rows - 1 - 1  # 1000 - imported - empty - header

        datasource_id = result["datasource"]["id"]
        a = exec_sql(u["database"], f"SELECT count() c FROM {datasource_id} FORMAT JSON")
        row = a["data"][0]
        self.assertEqual(int(row["c"]), expected_rows)
        a = exec_sql(u["database"], f"SELECT count() c FROM {datasource_id}_quarantine FORMAT JSON")
        row = a["data"][0]
        self.assertEqual(int(row["c"]), expected_rows_quarantine)  # 1000 lines - 1 header - 1 emtpy

        # statistics
        await self.assert_stats_async(datasource_id, token, expected_rows, 13278)

        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": result["datasource"]["name"],
                },
                {
                    "event_type": "append",
                    "datasource_name": result["datasource"]["name"],
                    "rows": expected_rows,
                    "rows_quarantine": expected_rows_quarantine,
                    "options": {
                        "source": "stream",
                    },
                },
            ]
        )

    @tornado.testing.gen_test
    async def test_append_to_tracker(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        ds_name = "test_append_to_tracker"

        params = {
            "token": token,
            "name": ds_name,
            "schema": """timestamp DateTime,
                         session DateTime,
                         account_name String,
                         user_id String,
                         location String,
                         attr0 Nullable(String),
                         attr1 Nullable(String),
                         attr2 Nullable(String),
                         attr3 Nullable(String),
                         attr4 Nullable(String),
                         attr5 Nullable(String),
                         attr6 Nullable(String),
                         attr7 Nullable(String),
                         attr8 Nullable(String)""",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        result = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(result["datasource"]["name"], ds_name)

        params = {"mode": "append", "token": token, "name": ds_name}

        workspace_agents = (
            (
                "desktop",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
                {},
            ),
            (
                "ios",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/80.0.3987.95 Mobile/15E148 Safari/604.1",
                {},
            ),
            (
                "android",
                "Mozilla/5.0 (Linux; Android 10; SM-N960U Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.138 Mobile Safari/537.36",
                {},
            ),
            (
                "instagram",
                "Mozilla/5.0 (Linux; Android 9; SM-A505GT Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36 Instagram 93.1.0.19.102 Android (28/9; 420dpi; 1080x2218; samsung; SM-A505GT; a50; exynos9610; pt_BR; 154400383)",
                {"dialect_delimiter": ","},
            ),
        )

        for platform, ua, extra_params in workspace_agents:
            with self.subTest(platform=platform):
                s = StringIO(
                    '"2020-04-23 14:09:42","2020-04-23 14:09:42",'
                    '"main","3e25a061-63d1-41bb-8e80-d2e5fb034b1e",'
                    '"http://192.168.1.51:8080/",'
                    f'"{ua}",'
                    '"pageload","","","","","","",""'
                )
                extra_params.update(params)
                append_url = f"/v0/datasources?{urlencode(extra_params)}"
                response = await self.fetch_full_body_upload_async(append_url, s)
                self.assertEqual(response.code, 200, response.body)
                result = json.loads(response.body)
                self.assertFalse(result["error"])

    @tornado.testing.gen_test
    async def test_create_streaming_with_invalid_token(self):
        Users.get_by_id(self.WORKSPACE_ID)
        url = self.get_url("/v0/datasources?token=INVALID")

        with fixture_file("yt_1000.csv", mode="rb") as fd:
            response = await self.fetch_stream_upload_async(url, fd)
        self.assertEqual(response.code, 403)

    @tornado.testing.gen_test
    async def test_import_reports_bad_url_input(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        datasource_url = self.get_url_for_sql("select 1 FORMAT CSV")
        # don't encode the URL on purpose
        import_url = f"/v0/datasources?token={token}&name=bad_url_test&url={datasource_url}"
        response = await self.fetch_async(import_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        job = await self.get_finalised_job_async(json.loads(response.body)["id"])

        response = await self.fetch_async(f"/v0/jobs/{job.id}?token={token}")
        self.assertEqual(response.code, 200)
        job_result = json.loads(response.body)
        self.assertEqual(job_result["kind"], "import")
        self.assertEqual(job_result["id"], job_result["job_id"])
        self.assertEqual(job_result["id"], job_result["import_id"])
        self.assertEqual(job_result["status"], "error")
        self.assertTrue("error" in job_result)
        # As url wasn't encoded, it gets cut after the first ampersand
        expected_error = f"Could not fetch URL. 400 Client Error: Bad Request for url: {datasource_url.split('&')[0]}"
        self.assertEqual(job_result["errors"], [expected_error])
        self.expect_ops_log(
            {
                "event_type": "create",
                "datasource_name": "bad_url_test",
                "result": "error",
                "error": expected_error,
            },
        )

    @tornado.testing.gen_test
    @pytest.mark.skip(
        "Google might block the url so it will fail. https://gitlab.com/tinybird/analytics/-/issues/10179"
    )
    async def test_import_google_spreadsheet(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        name = "test_create_with_spreadsheet"
        # The spreadsheet is https://docs.google.com/spreadsheets/d/16FO9DQws6G-FiqsVkMiJQV-J33O6Z9QMd9y8FRrDFWI/edit
        csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQB2E9pE9-qTHkoimd19G2fer8ANn-NmTXK9S2QKutso5UNNyxcVy-BV7apPHckZVoUA0Sb65yOY_y_/pub?gid=0&single=true&output=csv"
        params = {
            "token": token,
            "name": name,
            "url": csv_url,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")

        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done")
        self.assertEqual(job.get("errors"), None)
        expected_rows = 6
        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": name,
                },
                {
                    "event_type": "append",
                    "datasource_name": name,
                    "rows": expected_rows,
                    "options": {
                        "source": re.compile("https://.*"),
                    },
                },
            ]
        )

        name_id = Users.get_datasource(u, name).id
        self.wait_for_datasource_replication(u, name_id)

        async def _query(q):
            params = {"token": token, "q": q}
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            self.assertEqual(response.code, 200)
            result = json.loads(response.body)
            return result

        result = await _query(f"SELECT * FROM {name} ORDER BY a ASC FORMAT JSON")
        self.assertEqual(list(result["data"][0].values()), [1, 2, 3])
        result = await _query(f"SELECT count() rows_count FROM {name} FORMAT JSON")
        self.assertEqual(result["data"][0]["rows_count"], expected_rows)
        result = await _query(f"SELECT sum(a) sum_a FROM {name} FORMAT JSON")
        self.assertEqual(result["data"][0]["sum_a"], 21)

    @tornado.testing.gen_test
    async def test_create_url_with_messy_headers(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        csv_url = f"{HTTP_ADDRESS}/messy_headers.csv"
        import_url = f"/v0/datasources?token={token}&name=messy_headers_url&url={csv_url}"

        response = await self.fetch_async(import_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "error")
        expected_error = "Invalid column name 'index' at position 15, 'index' is a reserved keyword"
        self.assertEqual(
            job["error"], "There was an error when attempting to import your data. Check 'errors' for more information."
        )
        self.assertEqual(job["errors"], [expected_error])
        self.expect_ops_log(
            {
                "event_type": "create",
                "datasource_name": "messy_headers_url",
                "result": "error",
                "error": expected_error,
                "options": {
                    "source": csv_url,
                },
            },
        )

    @tornado.testing.gen_test
    async def test_create_streaming_with_messy_headers(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        url = self.get_url(f"/v0/datasources?token={token}&name=messy_headers_stream")
        with fixture_file("messy_headers.csv", mode="rb") as fd:
            response = await self.fetch_stream_upload_async(url, fd)
        self.assertEqual(response.code, 400)
        result = json.loads(response.body)
        expected_error = "Invalid column name 'index' at position 15, 'index' is a reserved keyword"
        self.assertEqual(result["error"], expected_error)
        self.expect_ops_log(
            {
                "event_type": "create",
                "datasource_name": "messy_headers_stream",
                "result": "error",
                "error": expected_error,
                "options": {
                    "source": "stream",
                },
            },
        )

    @tornado.testing.gen_test
    async def test_create_body_with_messy_headers(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        url = self.get_url(f"/v0/datasources?token={token}&name=messy_headers_body")
        with fixture_file("messy_headers.csv") as fd:
            response = await self.fetch_full_body_upload_async(url, fd)
        self.assertEqual(response.code, 400)
        result = json.loads(response.body)
        expected_error = "Invalid column name 'index' at position 15, 'index' is a reserved keyword"
        self.assertEqual(result["error"], expected_error)
        self.expect_ops_log(
            {
                "event_type": "create",
                "datasource_name": "messy_headers_body",
                "result": "error",
                "error": expected_error,
                "options": {
                    "source": "body",
                },
            },
        )

    @tornado.testing.gen_test
    async def test_append_with_messy_headers(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        ds_name = "test_append_messy"

        params = {
            "token": token,
            "name": ds_name,
            "schema": "VendorID Int32, tpep_pickup_datetime DateTime",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        result = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(result["datasource"]["name"], ds_name)
        self.expect_ops_log(
            {"event_type": "create", "datasource_name": ds_name, "options": {"source": "schema"}},
        )

        params = {
            "token": token,
            "name": ds_name,
            "mode": "append",
        }
        append_url = f"/v0/datasources?{urlencode(params)}"
        with fixture_file("messy_headers.csv") as fd:
            response = await self.fetch_full_body_upload_async(append_url, fd)
        self.assertEqual(response.code, 400)
        result = json.loads(response.body)
        expected_error = "Invalid column name 'index' at position 15, 'index' is a reserved keyword"
        self.assertEqual(result["error"], expected_error)
        self.expect_ops_log(
            {
                "event_type": "append",
                "datasource_name": ds_name,
                "result": "error",
                "error": expected_error,
                "options": {
                    "source": "body",
                },
            },
        )

    @tornado.testing.gen_test
    async def test_null_int16_in_quarantine(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        ds_name = "ds_processing_error_message"
        params = {
            "token": token,
            "name": ds_name,
            "schema": """
                dt Date,
                sku String,
                units Int16,
                price Float32
            """,
            "engine": "Null",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        params = {"token": token, "mode": "append", "debug": "blocks,hook_log", "name": ds_name}
        append_url = f"/v0/datasources?{urlencode(params)}"
        s = StringIO("2019-01-01,bar,,29.95")
        response = await self.fetch_full_body_upload_async(append_url, s)
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertIn("blocks", result)
        self.assertIn("process_return", result["blocks"][0])
        process_return = result["blocks"][0]["process_return"][0]
        self.assertEqual(process_return["quarantine"], 1)
        self.assertRegex(
            process_return["db_parse_error"],
            r"^\[Error\] Attempt to read after eof: Cannot parse Int16 from String, because value is too short",
        )

        self.assertIn("hook_log", result)
        expected_hook_operations = ("before_append", "after_append", "tear_down")
        for entry in result["hook_log"]:
            self.assertTrue(entry["operation"] in expected_hook_operations)
            self.assertNotIn("user_id", entry)
            self.assertNotIn("user_email", entry)

        self.expect_ops_log(
            [
                {"event_type": "create", "datasource_name": ds_name, "options": {"source": "schema"}},
                {
                    "event_type": "append",
                    "datasource_name": ds_name,
                    "rows_quarantine": 1,
                    "options": {
                        "source": "full_body",
                    },
                },
            ]
        )

    @tornado.testing.gen_test
    async def test_create_url_with_no_headers_column_names(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        csv_url = f"{HTTP_ADDRESS}/no_headers_column_names.csv"
        import_url = f"/v0/datasources?token={token}&url={csv_url}"

        response = await self.fetch_async(import_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done")
        self.expect_ops_log(
            [
                {"event_type": "create", "datasource_name": job["datasource"]["name"], "options": {"source": csv_url}},
                {
                    "event_type": "append",
                    "datasource_name": job["datasource"]["name"],
                    "rows": 10,
                    "options": {"source": csv_url},
                },
            ]
        )

    @tornado.testing.gen_test
    async def test_zero_uint_is_valid(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        ds_name = "ds_zero_uint_is_valid"
        params = {
            "token": token,
            "name": ds_name,
            "debug": "blocks",
            "schema": """
                dt Date,
                v_uint32 UInt32,
                v_uint64 UInt64
            """,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        self.expect_ops_log(
            {"event_type": "create", "datasource_name": ds_name, "options": {"source": "schema"}},
        )

        params = {"token": token, "mode": "append", "debug": "blocks", "name": ds_name}
        append_url = f"/v0/datasources?{urlencode(params)}"
        # We use an invalid row to force the processing with Python
        s = StringIO("2019-01-01,0,1\n2019-01-02,1,0\ninvalid-row,a,b")
        response = await self.fetch_full_body_upload_async(append_url, s)
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.expect_ops_log(
            {
                "event_type": "append",
                "datasource_name": ds_name,
                "rows": 2,
                "rows_quarantine": 1,
                "options": {"source": "full_body"},
            },
        )

        self.assertIn("blocks", result)
        blocks = result["blocks"]
        self.assertEqual(len(blocks), 1)
        block = blocks[0]
        self.assertIn("process_return", block)
        process_return = block["process_return"][0]
        self.assertEqual(process_return["parser"], "python")
        self.assertEqual(process_return["quarantine"], 1)
        self.assertRegex(process_return["db_parse_error"], r"^\[Error\] Cannot read DateTime: unexpected word")

    @tornado.testing.gen_test
    async def test_new_line_after_header(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        ds_name = "ds_new_line_after_header"
        url = self.get_url(f"/v0/datasources?token={token}&name={ds_name}&debug=blocks")
        with fixture_file("empty_lines_after_header.csv", mode="rb") as fd:
            response = await self.fetch_stream_upload_async(url, fd)

        self.assertEqual(response.code, 200)
        self.expect_ops_log(
            [
                {"event_type": "create", "datasource_name": ds_name, "options": {"source": "stream"}},
                {"event_type": "append", "datasource_name": ds_name, "rows": 8, "options": {"source": "stream"}},
            ]
        )
        result = json.loads(response.body)
        self.assertIn("blocks", result)
        blocks = result["blocks"]
        self.assertEqual(len(blocks), 1)
        block = blocks[0]
        self.assertIn("process_return", block)
        process_return = block["process_return"][0]
        self.assertEqual(process_return["parser"], "clickhouse")

    @tornado.testing.gen_test
    async def test_nested_columns(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        ds_name = "ds_nested_column"
        params = {
            "token": token,
            "name": ds_name,
            "schema": """
                d Date,
                event_type String,
                Options Nested(
                    Names String,
                    Values String
                )
            """,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        async def get_result():
            name_id = Users.get_datasource(u, ds_name).id
            self.wait_for_datasource_replication(u, name_id)

            params = {"token": token, "q": f"SELECT * FROM {ds_name} ORDER BY d FORMAT JSON"}
            response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
            self.assertEqual(response.code, 200)
            result = json.loads(response.body)
            return result

        result = await get_result()
        names_column = next((c for c in result["meta"] if c["name"] == "Options.Names"), None)
        self.assertIsNotNone(names_column)
        self.assertEqual(names_column["type"], "Array(String)")

        params = {"token": token, "mode": "append", "name": ds_name}
        append_url = f"/v0/datasources?{urlencode(params)}"
        s = StringIO("2019-01-01,create,['url'],['example.com']\n2019-01-02,replace,['condition'],['1=1']")
        response = await self.fetch_full_body_upload_async(append_url, s)
        self.assertEqual(response.code, 200, response.body)
        append_result = json.loads(response.body)
        self.assertFalse(append_result["error"])

        result = await get_result()
        self.assertEqual(len(result["data"]), 2)
        self.assertEqual(result["data"][0]["Options.Names"], ["url"])
        self.assertEqual(result["data"][0]["Options.Values"], ["example.com"])

    @tornado.testing.gen_test
    async def test_float_no_quarantine(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        ds_name = "ds_f32_f64"
        params = {
            "token": token,
            "name": ds_name,
            "schema": """
                d Date,
                v_f32 Float32,
                v_f64 Float64
            """,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        self.expect_ops_log(
            {"event_type": "create", "datasource_name": ds_name, "options": {"source": "schema"}},
        )

        params = {"token": token, "mode": "append", "debug": "blocks", "name": ds_name}
        append_url = f"/v0/datasources?{urlencode(params)}"
        # We use an invalid row to force the processing with Python
        s = StringIO(f"2019-01-01,{float(2**24)},1.0\n2019-01-02,1,{float(2**53)}\ninvalid-row,a,b")
        response = await self.fetch_full_body_upload_async(append_url, s)
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.expect_ops_log(
            {
                "event_type": "append",
                "datasource_name": ds_name,
                "rows": 2,
                "rows_quarantine": 1,
                "options": {"source": "full_body"},
            },
        )

        self.assertIn("blocks", result)
        blocks = result["blocks"]
        self.assertEqual(len(blocks), 1)
        block = blocks[0]
        self.assertIn("process_return", block)
        process_return = block["process_return"][0]
        self.assertEqual(process_return["parser"], "python")
        self.assertEqual(process_return["quarantine"], 1)
        self.assertRegex(process_return["db_parse_error"], r"^\[Error\] Cannot read DateTime: unexpected word")

    @tornado.testing.gen_test
    async def test_import_uses_default_values_at_load_time(self):
        # Create schema with default values
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        ds_name = "datasource_with_default_values"
        params = {
            "token": token,
            "name": ds_name,
            "schema": """
               `no_nullable_string` String,
               `no_nullable_with_default` String DEFAULT 'bla',
               `no_nullable_with_default_and_cast` String DEFAULT CAST(123, 'String'),
               `nullable_column` Nullable(Int64),
               `nullable_column_with_default_cast_null` Nullable(Int64) DEFAULT CAST(NULL, 'Nullable(Int64)'),
               `nullable_column_with_default_null` Nullable(Int64) DEFAULT NULL,
               `nullable_column_with_default_value` Nullable(Int64) DEFAULT 'bla'
            """,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        ds_create_response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(ds_create_response.code, 200, ds_create_response.body)

        # Import data to that schema with empty values, so that the default value will apply
        params = {"token": token, "mode": "append", "debug": "blocks", "name": ds_name}
        append_url = f"/v0/datasources?{urlencode(params)}"
        s = StringIO(",,,,,,")
        response = await self.fetch_full_body_upload_async(append_url, s)
        self.assertEqual(response.code, 200, response.body)

        # query the DS and assert the default values are pressent.
        datasource_id = Users.get_datasource(u, ds_name).id
        datasource_content = exec_sql(u["database"], f"select * from {datasource_id} FORMAT JSON")

        self.assertEqual(
            datasource_content["data"],
            [
                {
                    "no_nullable_string": "",
                    "no_nullable_with_default": "bla",
                    "no_nullable_with_default_and_cast": "123",
                    "nullable_column": None,
                    "nullable_column_with_default_cast_null": None,
                    "nullable_column_with_default_null": None,
                    "nullable_column_with_default_value": None,
                }
            ],
        )

    @tornado.testing.gen_test
    async def test_full_body_import_stores_first_delimiter_used(self):
        ds_name = "test_store_delimiter"
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        with fixture_file("simple.csv") as fd:
            response = await self.fetch_full_body_upload_async(f"/v0/datasources?token=%s&name={ds_name}" % token, fd)
        self.assertEqual(response.code, 200)
        b = json.loads(response.body)
        self.assertEqual(b["datasource"]["name"], ds_name)

        response = await self.fetch_async(f"/v0/datasources/{ds_name}?{urlencode({'token': token})}")
        self.assertEqual(response.code, 200, response.body)
        ds = json.loads(response.body)
        self.assertEqual(",", ds["headers"]["cached_delimiter"])

    @tornado.testing.gen_test
    async def test_stream_import_stores_first_delimiter_used(self):
        ds_name = "test_store_delimiter"
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
            "name": ds_name,
        }
        create_url = self.get_url(f"/v0/datasources?{urlencode(params)}")
        with fixture_file("simple.csv", mode="rb") as fd:
            response = await self.fetch_stream_upload_async(create_url, fd)
        self.assertEqual(response.code, 200)

        get = sync_to_async(requests.get, thread_sensitive=False)
        url = self.get_url(f"/v0/datasources/{ds_name}?{urlencode({'token': token})}")
        response = await get(url)
        self.assertEqual(response.status_code, 200, response.json())
        ds = response.json()
        self.assertEqual(",", ds["headers"]["cached_delimiter"])

    @tornado.testing.gen_test
    async def test_url_job_import_stores_first_delimiter_used(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        csv_url = f"{HTTP_ADDRESS}/simple.csv"
        import_url = f"/v0/datasources?token={token}&url={csv_url}"

        response = await self.fetch_async(import_url, method="POST", body="")
        result = json.loads(response.body)
        job_id = result["id"]

        await self.get_finalised_job_async(job_id, debug="blocks, hook_log")
        self.assertEqual(response.code, 200)

        response = await self.fetch_async(f"/v0/datasources/simple?{urlencode({'token': token})}")
        self.assertEqual(response.code, 200, response.body)
        ds = json.loads(response.body)
        self.assertEqual(",", ds["headers"]["cached_delimiter"])

    @tornado.testing.gen_test
    async def test_share_datasource_same_workspace(self):
        tb_api_proxy_async = TBApiProxyAsync(self)

        random_id = uuid.uuid4().hex
        ws_name = f"workspace_{random_id}"
        user_email = f"{random_id}@example.com"
        workspace = await tb_api_proxy_async.register_user_and_workspace(user_email, ws_name)
        user = UserAccount.get_by_email(user_email)
        token_workspace = Users.get_token_for_scope(workspace, scopes.ADMIN)
        token_user = UserAccount.get_token_for_scope(user, scopes.AUTH)

        datasource_in_workspace = await tb_api_proxy_async.create_datasource(
            token=token_workspace, ds_name="d", schema="col_a Int32,col_b Int32,col_c Int32"
        )

        with pytest.raises(Exception) as exc:
            await tb_api_proxy_async.share_datasource_with_another_workspace(
                token=token_user,
                datasource_id=datasource_in_workspace["datasource"]["id"],
                origin_workspace_id=workspace.id,
                destination_workspace_id=workspace.id,
                expect_notification=False,
            )
        assert "parent workspace" in str(exc), "Should break because of parent workspace error"

    @tornado.testing.gen_test
    async def test_a_shared_datasource_can_not_receive_data_from_the_destination_workspace(self):
        tb_api_proxy_async = TBApiProxyAsync(self)

        workspace_a = Users.get_by_id(self.WORKSPACE_ID)
        user_a = UserAccount.get_by_id(self.USER_ID)
        token_workspace_a = Users.get_token_for_scope(workspace_a, scopes.ADMIN)
        token_user_a = UserAccount.get_token_for_scope(user_a, scopes.AUTH)
        # Test a long ws name to check sharing and looking for it works
        ws_a_name = f"ws_{uuid.uuid4().hex}_{uuid.uuid4().hex}_{uuid.uuid4().hex}"
        await tb_api_proxy_async.rename_workspace(workspace_a.id, token_user_a, ws_a_name)

        ws_name = f"user_b_{uuid.uuid4().hex}"
        workspace_b = await tb_api_proxy_async.register_user_and_workspace(
            f"{ws_name}@example.com", f"{ws_name}_workspace"
        )
        user_b = UserAccount.get_by_email(f"{ws_name}@example.com")
        token_workspace_b = Users.get_token_for_scope(workspace_b, scopes.ADMIN)
        token_user_b = UserAccount.get_token_for_scope(user_b, scopes.AUTH)

        datasource_a_in_workspace_a = await tb_api_proxy_async.create_datasource(
            token=token_workspace_a, ds_name="d", schema="col_a Int32,col_b Int32,col_c Int32"
        )

        await tb_api_proxy_async.invite_user_to_workspace(
            token=token_user_b, workspace_id=workspace_b.id, user_to_invite_email=user_a.email
        )

        datasource_a_in_workspace_b = await tb_api_proxy_async.share_datasource_with_another_workspace(
            token=token_user_a,
            datasource_id=datasource_a_in_workspace_a["datasource"]["id"],
            origin_workspace_id=workspace_a.id,
            destination_workspace_id=workspace_b.id,
        )

        params = {
            "mode": "append",
            "token": token_workspace_b,
            "name": datasource_a_in_workspace_b.name,
        }

        s = StringIO("1,2,3\n4,5,6\n7,8,9\n")
        import_response = await self.fetch_full_body_upload_async(f"/v0/datasources?{urlencode(params)}", s)
        self.assertEqual(import_response.code, 400, import_response.body)
        self.assertEqual(
            json.loads(import_response.body),
            {
                "error": f'Data Source "{datasource_a_in_workspace_b.name}" is read-only so it can\'t be modified.'
                " If it's a shared Data Source, the operations available in this endpoint should be"
                " done from the origin Workspace."
            },
        )

    @tornado.testing.gen_test
    async def test_import_custom_ttl(self):
        workspace = Users.get_by_id(self.WORKSPACE_ID)

        @retry_transaction_in_case_of_concurrent_edition_error_sync()
        def setting_limits(value):
            with User.transaction(workspace.id) as user:
                user.set_user_limit("import_max_job_ttl_in_hours", value, "import")

        setting_limits(1)

        csv_url = self.get_url_for_sql("select '1,2,3,4' format CSV")
        import_url = (
            f"/v0/datasources?token={self.admin_token}&name=test_import_custom_ttl&url={quote(csv_url,safe='')}"
        )

        response = await self.fetch_async(import_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        import_response = json.loads(response.body)
        self.assertEqual(import_response["job_id"], import_response["id"])

        job = await self.get_finalised_job_async(import_response["job_id"])
        self.assertEqual(job.status, "done")
        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": "test_import_custom_ttl",
                },
                {
                    "event_type": "append",
                    "datasource_name": "test_import_custom_ttl",
                    "rows": 1,
                    "options": {
                        "source": csv_url,
                    },
                },
            ]
        )

        redis_client = TBRedisClientSync(get_redis_config())
        job_ttl = redis_client.ttl(f"jobs:{import_response['job_id']}")

        assert job_ttl < 3600

        setting_limits(None)


class TestAPIDatasourceStoragePolicy(TestAPIDatasourceBase):
    def setUp(self):
        super().setUp()
        with User.transaction(self.WORKSPACE_ID) as w:
            w.storage_policies = {OTHER_STORAGE_POLICY: 0}
            w.feature_flags[FeatureFlagWorkspaces.ENABLE_STORAGE_POLICY.value] = True

    def tearDown(self):
        with User.transaction(self.WORKSPACE_ID) as w:
            w.feature_flags[FeatureFlagWorkspaces.ENABLE_STORAGE_POLICY.value] = False
            w.storage_policies = {}
        super().tearDown()

    @tornado.testing.gen_test
    async def test_create_data_source_using_storage_policy(self):
        workspace = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.add_token(workspace, "test", scopes.DATASOURCES_CREATE)
        datasource_name = "test_data_source_storage_policy"

        params = {
            "token": token,
            "name": datasource_name,
            "mode": "create",
        }

        await self.fetch_async(f"/v0/datasources?{urlencode(params)}", method="POST", body="2019-01-03,10")
        datasource = Users.get_datasource(workspace, datasource_name)
        table_details = await ch_table_details_async(
            datasource.id, workspace.database_server, database=workspace.database
        )

        # The exposed settings should not include `storage_policy`
        # We hide the storage_policy and then the default index_granularity is also removed
        self.assertEqual(table_details.settings, None)
        self.assertTrue("storage_policy" not in table_details.engine_full, table_details.engine_full)

        # Although we don't expose it to the customer, the table in CH should have the proper policy
        client = HTTPClient(workspace.database_server, database=workspace.database)
        sql = f"SELECT create_table_query FROM system.tables WHERE database = '{workspace.database}' and name = '{datasource.id}' FORMAT CSV"
        _, body = await client.query(sql)
        real_definition = str(body)
        self.assertTrue("storage_policy" in real_definition, real_definition)
        self.assertTrue(OTHER_STORAGE_POLICY in real_definition, real_definition)
        self.assertTrue("index_granularity" in real_definition, real_definition)  # CH adds this by default


class TestAPIDatasourceImportTracker(TestAPIDatasourceBase):
    def assert_block_ch_stats(
        self,
        block,
        db_stats_written_rows_min=None,
        db_stats_written_bytes_min=None,
        quarantine_db_stats_written_rows_min=None,
        quarantine_db_stats_written_bytes_min=None,
    ):
        if db_stats_written_rows_min is not None:
            self.assertIn("db_stats", block["process_return"][0])
            self.assertEqual(1, len(block["process_return"][0]["db_stats"]))
            self.assertIn("query_id", block["process_return"][0]["db_stats"][0])
            self.assertGreaterEqual(
                int(block["process_return"][0]["db_stats"][0]["summary"]["written_rows"]), db_stats_written_rows_min
            )
            if db_stats_written_bytes_min is not None:
                self.assertGreaterEqual(
                    int(block["process_return"][0]["db_stats"][0]["summary"]["written_bytes"]),
                    db_stats_written_bytes_min,
                )
        else:
            self.assertEqual(0, len(block["process_return"][0]["db_stats"]))

        if quarantine_db_stats_written_rows_min is not None:
            self.assertEqual(1, len(block["process_return"][0]["quarantine_db_stats"]))
            self.assertIn("query_id", block["process_return"][0]["quarantine_db_stats"][0])
            self.assertGreaterEqual(
                int(block["process_return"][0]["quarantine_db_stats"][0]["summary"]["written_rows"]),
                quarantine_db_stats_written_rows_min,
            )
            if quarantine_db_stats_written_bytes_min is not None:
                self.assertGreaterEqual(
                    int(block["process_return"][0]["quarantine_db_stats"][0]["summary"]["written_bytes"]),
                    quarantine_db_stats_written_bytes_min,
                )
        else:
            self.assertEqual(0, len(block["process_return"][0]["quarantine_db_stats"]))

    @tornado.testing.gen_test
    async def test_db_stats_in_blocks_import_url_csv(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        name = "test_db_stats_in_blocks_csv"

        params = {
            "token": token,
            "name": name,
            "schema": """
                    d Int32
                """,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        params = {
            "token": token,
            "name": name,
            "mode": "append",
            "format": "csv",
            "debug": "blocks",
            "url": self.get_url_for_sql("select 1 format CSV"),
        }
        with patch("tinybird.tracker.track_blocks") as mock_track_blocks:
            create_url = f"/v0/datasources?{urlencode(params)}"
            response = await self.fetch_async(create_url, method="POST", body="")
            self.assertEqual(response.code, 200)

            job = await self.get_finalised_job_async(json.loads(response.body)["id"], debug="blocks")
            self.assertEqual(job.status, "done")
        self.assertEqual(1, len(mock_track_blocks.call_args.kwargs["blocks"]))
        self.assert_block_ch_stats(
            block=mock_track_blocks.call_args.kwargs["blocks"][0],
            db_stats_written_rows_min=1,
            db_stats_written_bytes_min=4,
            quarantine_db_stats_written_rows_min=None,
        )

        params = {
            "token": token,
            "name": name,
            "mode": "append",
            "format": "csv",
            "debug": "blocks",
            "url": self.get_url_for_sql("select 'x' as a format CSV"),
        }

        with patch("tinybird.tracker.track_blocks") as mock_quarantine_track_blocks:
            create_url = f"/v0/datasources?{urlencode(params)}"
            response = await self.fetch_async(create_url, method="POST", body="")
            self.assertEqual(response.code, 200)

            job = await self.get_finalised_job_async(json.loads(response.body)["id"], debug="blocks")
            self.assertEqual(job.status, "done")
            self.assertEqual(job["quarantine_rows"], 1)

        self.assertEqual(1, len(mock_track_blocks.call_args.kwargs["blocks"]))
        self.assert_block_ch_stats(
            block=mock_quarantine_track_blocks.call_args.kwargs["blocks"][0],
            db_stats_written_rows_min=None,
            quarantine_db_stats_written_rows_min=1,
            quarantine_db_stats_written_bytes_min=128,
        )

    @tornado.testing.gen_test
    async def test_db_stats_in_blocks_import_body(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        name = "true_test_import_body"
        with fixture_file("yt_1000.csv") as fd:
            with patch("tinybird.tracker.track_blocks") as mock_track_blocks:
                response = await self.fetch_full_body_upload_async(f"/v0/datasources?token=%s&name={name}" % token, fd)
        self.assertEqual(response.code, 200)
        b = json.loads(response.body)
        self.assertEqual(b["datasource"]["name"], name)

        expected_rows = 328
        expected_rows_quarantine = 1000 - expected_rows - 1 - 1  # 1000 - imported - empty - header

        self.assertEqual(b["invalid_lines"], 0)
        self.assertEqual(b["quarantine_rows"], expected_rows_quarantine)

        a = exec_sql(u["database"], "select count(1) c from `%s` FORMAT JSON" % b["datasource"]["id"])
        row = a["data"][0]
        self.assertEqual(int(row["c"]), expected_rows)

        a = exec_sql(u["database"], "select count(1) c from `%s_quarantine` FORMAT JSON" % b["datasource"]["id"])
        row = a["data"][0]
        self.assertEqual(int(row["c"]), expected_rows_quarantine)
        self.delete_table(u["database"], b["datasource"]["id"])

        # app stats
        await self.assert_stats_async(name, token, expected_rows, 13278)

        # block ch stats
        self.assert_block_ch_stats(
            block=mock_track_blocks.call_args.kwargs["blocks"][0],
            db_stats_written_rows_min=expected_rows,
            db_stats_written_bytes_min=10000,
            quarantine_db_stats_written_rows_min=expected_rows_quarantine,
            quarantine_db_stats_written_bytes_min=10000,
        )

    @tornado.testing.gen_test
    async def test_db_stats_in_blocks_import_streaming(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        url = self.get_url(f"/v0/datasources?token={token}&type_guessing=false&name=test_create_streaming")

        with fixture_file("yt_1000.csv", mode="rb") as fd:
            with patch("tinybird.tracker.track_blocks") as mock_track_blocks:
                response = await self.fetch_stream_upload_async(url, fd)
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)

        expected_rows = 998
        expected_rows_quarantine = 0

        datasource_id = result["datasource"]["id"]
        a = exec_sql(u["database"], f"SELECT count() c FROM {datasource_id} FORMAT JSON")
        row = a["data"][0]
        self.assertEqual(int(row["c"]), expected_rows)
        a = exec_sql(u["database"], f"SELECT count() c FROM {datasource_id}_quarantine FORMAT JSON")
        row = a["data"][0]
        self.assertEqual(int(row["c"]), expected_rows_quarantine)

        a = exec_sql(u["database"], f"select * from {datasource_id} FORMAT JSON")
        meta = a["meta"]
        meta_types = set(list([x["type"] for x in meta]))
        self.assertEqual(meta_types, {"String"})

        # app statistics
        await self.assert_stats_async(datasource_id, token, expected_rows, 67157)

        # block ch stats
        self.assertEqual(2, len(mock_track_blocks.call_args.kwargs["blocks"]))
        # block ch stats
        self.assert_block_ch_stats(
            block=mock_track_blocks.call_args.kwargs["blocks"][0],
            db_stats_written_rows_min=200,
            db_stats_written_bytes_min=10000,
            quarantine_db_stats_written_rows_min=None,
        )
        # block ch stats
        self.assert_block_ch_stats(
            block=mock_track_blocks.call_args.kwargs["blocks"][1],
            db_stats_written_rows_min=200,
            db_stats_written_bytes_min=10000,
            quarantine_db_stats_written_rows_min=None,
        )

    @tornado.testing.gen_test
    async def test_db_stats_in_blocks_import_url_ndjson(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        name = "test_db_stats_in_blocks_ndsjon" + uuid.uuid4().hex
        with patch("tinybird.tracker.track_blocks") as mock_track_blocks:
            params = {
                "token": token,
                "name": name,
                "mode": "create",
                "format": "ndjson",
                "debug": "blocks",
                "schema": "`a` String `json:$.a`",
                "url": self.get_url_for_sql("select '1,2,3,4' as a format JSONEachRow"),
            }
            create_url = f"/v0/datasources?{urlencode(params)}"
            response = await self.fetch_async(create_url, method="POST", body="")
            self.assertEqual(response.code, 200)

            job = await self.get_finalised_job_async(json.loads(response.body)["id"], debug="blocks")
            self.assertEqual(job.status, "done", job)

            def assert_track_blocks():
                mock_track_blocks.assert_called_once()
                self.assertEqual(2, len(mock_track_blocks.call_args.kwargs["blocks"]))
                self.assert_block_ch_stats(
                    block=mock_track_blocks.call_args.kwargs["blocks"][0],
                    db_stats_written_rows_min=1,
                    db_stats_written_bytes_min=16,
                    quarantine_db_stats_written_rows_min=None,
                )

            poll(assert_track_blocks)
            mock_track_blocks.reset_mock()
            params = {
                "token": token,
                "name": name,
                "mode": "append",
                "format": "ndjson",
                "debug": "blocks",
                "url": self.get_url_for_sql("select 1 as a format JSONEachRow"),
            }

            create_url = f"/v0/datasources?{urlencode(params)}"
            response = await self.fetch_async(create_url, method="POST", body="")
            self.assertEqual(response.code, 200)

            job = await self.get_finalised_job_async(json.loads(response.body)["id"], debug="blocks")
            self.assertEqual(job.status, "error")
            self.assertEqual(job["quarantine_rows"], 1)

            def assert_track_blocks_quarantine():
                mock_track_blocks.assert_called_once()
                self.assertEqual(2, len(mock_track_blocks.call_args.kwargs["blocks"]))
                self.assert_block_ch_stats(
                    block=mock_track_blocks.call_args.kwargs["blocks"][0],
                    db_stats_written_rows_min=None,
                    quarantine_db_stats_written_rows_min=1,
                    quarantine_db_stats_written_bytes_min=183,
                )

            poll(assert_track_blocks_quarantine)

    @tornado.testing.gen_test
    async def test_datasource_ops_log_append_without_materializations_csv_url(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        rand = str(uuid.uuid4())[:8]
        name = f"test_ops_logs_tracker_csv_{rand}"

        params = {
            "token": token,
            "name": name,
            "schema": """
                        d Int32
                    """,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        params = {
            "token": token,
            "name": name,
            "mode": "append",
            "format": "csv",
            "debug": "blocks",
            "url": self.get_url_for_sql("select 1 format CSV"),
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        job = await self.get_finalised_job_async(json.loads(response.body)["id"], debug="blocks")
        self.assertEqual(job.status, "done")

        self.expect_ops_log(
            [
                {"event_type": "create", "datasource_name": name, "options": {"source": "schema"}, "result": "ok"},
                {
                    "event_type": "append",
                    "datasource_name": name,
                    "rows": 1,
                    "rows_quarantine": 0,
                    "result": "ok",
                    "read_rows": 0,
                    "read_bytes": 0,
                    "written_rows": 1,
                    "written_bytes": 4,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "pipe_id": "",
                    "pipe_name": "",
                    "release": "",
                },
            ]
        )

    @tornado.testing.gen_test
    async def test_datasource_ops_log_append_without_materializations_body(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        name = "test_ops_logs_tracker_body"

        with fixture_file("yt_1000.csv") as fd:
            response = await self.fetch_full_body_upload_async(f"/v0/datasources?token=%s&name={name}" % token, fd)
        self.assertEqual(response.code, 200)

        expected_rows = 328
        expected_rows_quarantine = 1000 - expected_rows - 1 - 1  # 1000 - imported - empty - header

        self.expect_ops_log(
            [
                {"event_type": "create", "datasource_name": name, "options": {"source": "full_body"}, "result": "ok"},
                {
                    "event_type": "append",
                    "datasource_name": name,
                    "rows": expected_rows,
                    "rows_quarantine": expected_rows_quarantine,
                    "result": "ok",
                    "read_rows": 0,
                    "read_bytes": 0,
                    "written_rows": expected_rows,
                    "written_bytes": 26896,
                    "written_rows_quarantine": expected_rows_quarantine,
                    "written_bytes_quarantine": 324462,
                    "pipe_id": "",
                    "pipe_name": "",
                    "release": "",
                },
            ]
        )

    @tornado.testing.gen_test
    async def test_datasource_ops_log_append_with_failed_materializations_body(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        name = "test_ops_logs_tracker_body_with_failed"

        with fixture_file("yt_1000.csv") as fd:
            response = await self.fetch_full_body_upload_async(f"/v0/datasources?token=%s&name={name}" % token, fd)
        self.assertEqual(response.code, 200)

        params = {"token": token}
        response = await self.fetch_async(
            f"/v0/datasources/{name}/truncate?{urlencode(params)}", method="POST", body=""
        )
        self.assertEqual(response.code, 205)

        # create a pipe's node with a view to that datasource
        rand = str(uuid.uuid4())[:8]
        pipe_name = f"test_mat_view_{rand}"
        pipe = Users.add_pipe_sync(u, pipe_name, "select * from test_table")
        target_ds_name = f"mat_view_node_ds_{rand}"
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
            body=f"select throwIf(vendor_id = 'CMT', 'Error') as d from {name}",
        )
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(pipe_node["name"], "mat_view_node")
        ds = Users.get_datasource(u, target_ds_name)
        self.assertEqual(pipe_node["materialized"], ds.id)

        with fixture_file("yt_1000.csv") as fd:
            response = await self.fetch_full_body_upload_async(
                f"/v0/datasources?token=%s&mode=append&name={name}" % token, fd
            )
        self.assertEqual(response.code, 400, response.body)
        self.assertIn("There was an error when attempting to import your data", json.loads(response.body)["error"])

        expected_rows = 328
        expected_rows_quarantine = 1000 - expected_rows - 1 - 1  # 1000 - imported - empty - header

        self.expect_ops_log(
            [
                {"event_type": "create", "datasource_name": name, "options": {"source": "full_body"}, "result": "ok"},
                {
                    "event_type": "append",
                    "datasource_name": name,
                    "rows": expected_rows,
                    "rows_quarantine": expected_rows_quarantine,
                    "result": "ok",
                    "read_rows": 0,
                    "read_bytes": 0,
                    "written_rows": expected_rows,
                    "written_bytes": 26896,
                    "written_rows_quarantine": expected_rows_quarantine,
                    "written_bytes_quarantine": 324462,
                    "pipe_id": "",
                    "pipe_name": "",
                    "release": "",
                },
                {"event_type": "truncate", "datasource_name": name, "result": "ok"},
                {"event_type": "create", "datasource_name": target_ds_name, "result": "ok"},
                {
                    "event_type": "append",
                    "datasource_name": name,
                    "rows": expected_rows,
                    "rows_quarantine": 0,
                    "result": "error",
                    "error": re.compile(".*Please review the Materialized Views linked.*"),
                    "read_rows": 0,
                    "read_bytes": 0,
                    "written_rows": expected_rows,
                    "written_bytes": 26896,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "pipe_id": "",
                    "pipe_name": "",
                    "release": "",
                },
                {
                    "event_type": "append",
                    "datasource_name": target_ds_name,
                    "rows": 0,
                    "rows_quarantine": 0,
                    "result": "error",
                    "error": re.compile(".*Error: while executing 'FUNCTION throwIf.*"),
                    "read_rows": 328,
                    "read_bytes": 3936,
                    "written_rows": 0,
                    "written_bytes": 0,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "pipe_id": pipe.id,
                    "pipe_name": pipe_name,
                    "release": "",
                },
            ]
        )

    @tornado.testing.gen_test
    async def test_datasource_ops_log_append_with_failed_materializations_ndjson_body(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        rand = str(uuid.uuid4())[:8]
        ds_name = f"test_ops_logs_tracker_ndjson_body_{rand}"

        params = {
            "token": token,
            "name": ds_name,
            "format": "ndjson",
            "schema": """
                        `date` DateTime `json:$.date`, `event` String `json:$.event`
                        """,
            "mode": "create",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response)

        target_ds_name = f"mat_view_node_ds_{rand}"

        # create a pipe's node with a view to that datasource
        pipe_name = f"test_mat_view_{rand}"
        pipe = Users.add_pipe_sync(u, pipe_name, "select * from test_table")
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
            body=f"select throwIf(event = 'buy', 'Error') as d from {ds_name}",
        )
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200, response)
        self.assertEqual(pipe_node["name"], "mat_view_node")
        ds = Users.get_datasource(u, target_ds_name)
        self.assertEqual(pipe_node["materialized"], ds.id)

        params = {
            "token": token,
            "name": ds_name,
            "mode": "append",
            "format": "ndjson",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(
            create_url,
            method="POST",
            body=e2e_fixture_data("events.ndjson", mode="rb"),
            headers={"Content-Type": "application/octet-stream"},
        )
        self.assertEqual(response.code, 422, response.body)

        expected_rows = 10
        expected_rows_quarantine = 0

        self.expect_ops_log(
            [
                {"event_type": "create", "datasource_name": ds_name, "options": {"source": "schema"}, "result": "ok"},
                {
                    "event_type": "create",
                    "datasource_name": target_ds_name,
                    "options": {"source": "pipe"},
                    "result": "ok",
                },
                {
                    "event_type": "append",
                    "datasource_name": ds_name,
                    "rows": expected_rows,
                    "rows_quarantine": expected_rows_quarantine,
                    "result": "error",
                    "error": re.compile(".*Error: while executing 'FUNCTION.*"),
                    "read_rows": 0,
                    "read_bytes": 0,
                    "written_rows": expected_rows,
                    "written_bytes": 265,
                    "written_rows_quarantine": expected_rows_quarantine,
                    "written_bytes_quarantine": 0,
                    "pipe_id": "",
                    "pipe_name": "",
                    "release": "",
                },
                {
                    "event_type": "append",
                    "datasource_name": target_ds_name,
                    "rows": 0,
                    "rows_quarantine": expected_rows_quarantine,
                    "result": "error",
                    "error": re.compile(".*Code: 395. DB::Exception: Error: while executing 'FUNCTION.*"),
                    "read_rows": 10,
                    "read_bytes": 225,
                    "written_rows": 0,
                    "written_bytes": 0,
                    "written_rows_quarantine": expected_rows_quarantine,
                    "written_bytes_quarantine": 0,
                    "pipe_id": pipe.id,
                    "pipe_name": pipe_name,
                    "release": "",
                },
            ]
        )

    @tornado.testing.gen_test
    async def test_datasource_ops_log_append_without_materializations_streaming(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        name = "test_ops_logs_tracker_streaming"

        url = self.get_url(f"/v0/datasources?token={token}&type_guessing=false&name={name}")
        with fixture_file("yt_1000.csv", mode="rb") as fd:
            response = await self.fetch_stream_upload_async(url, fd)
        self.assertEqual(response.code, 200, response.body)

        expected_rows = 998
        expected_rows_quarantine = 0

        self.expect_ops_log(
            [
                {"event_type": "create", "datasource_name": name, "options": {"source": "stream"}, "result": "ok"},
                {
                    "event_type": "append",
                    "datasource_name": name,
                    "rows": expected_rows,
                    "rows_quarantine": expected_rows_quarantine,
                    "result": "ok",
                    "read_rows": 0,
                    "read_bytes": 0,
                    "written_rows": expected_rows,
                    "written_bytes": 326208,
                    "written_rows_quarantine": expected_rows_quarantine,
                    "written_bytes_quarantine": 0,
                    "pipe_id": "",
                    "pipe_name": "",
                    "release": "",
                },
            ]
        )

    @tornado.testing.gen_test
    async def test_datasource_ops_log_append_with_failed_materializations_streaming(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        name = "test_ops_logs_tracker_streaming_with_failed"

        url = self.get_url(f"/v0/datasources?token={token}&type_guessing=false&name={name}")
        with fixture_file("yt_1000.csv", mode="rb") as fd:
            response = await self.fetch_stream_upload_async(url, fd)
        self.assertEqual(response.code, 200, response.body)

        params = {"token": token}
        response = await self.fetch_async(
            f"/v0/datasources/{name}/truncate?{urlencode(params)}", method="POST", body=""
        )
        self.assertEqual(response.code, 205)

        # create a pipe's node with a view to that datasource
        rand = str(uuid.uuid4())[:8]
        pipe_name = f"test_mat_view_{rand}"
        pipe = Users.add_pipe_sync(u, pipe_name, "select * from test_table")
        target_ds_name = f"mat_view_node_ds_{rand}"
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
            body=f"select throwIf(vendor_id = 'CMT', 'Error') as d from {name}",
        )
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(pipe_node["name"], "mat_view_node")
        ds = Users.get_datasource(u, target_ds_name)
        self.assertEqual(pipe_node["materialized"], ds.id)

        url = self.get_url(f"/v0/datasources?token={token}&mode=append&type_guessing=false&name={name}")
        with fixture_file("yt_1000.csv", mode="rb") as fd:
            response = await self.fetch_stream_upload_async(url, fd)
        self.assertEqual(response.code, 400, response.body)

        expected_rows = 998
        expected_rows_quarantine = 0

        self.expect_ops_log(
            [
                {"event_type": "create", "datasource_name": name, "options": {"source": "stream"}, "result": "ok"},
                {
                    "event_type": "append",
                    "datasource_name": name,
                    "rows": expected_rows,
                    "rows_quarantine": expected_rows_quarantine,
                    "result": "ok",
                    "read_rows": 0,
                    "read_bytes": 0,
                    "written_rows": expected_rows,
                    "written_bytes": 326208,
                    "written_rows_quarantine": expected_rows_quarantine,
                    "written_bytes_quarantine": 0,
                    "pipe_id": "",
                    "pipe_name": "",
                    "release": "",
                },
                {"event_type": "truncate", "datasource_name": name, "result": "ok"},
                {"event_type": "create", "datasource_name": target_ds_name, "result": "ok"},
                {
                    "event_type": "append",
                    "datasource_name": name,
                    "rows": expected_rows,
                    "rows_quarantine": 0,
                    "result": "error",
                    "error": re.compile(".*Please review the Materialized Views linked to the Data Source.*"),
                    "read_rows": 0,
                    "read_bytes": 0,
                    "written_rows": expected_rows,
                    "written_bytes": 326208,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "pipe_id": "",
                    "pipe_name": "",
                    "release": "",
                },
                {
                    "event_type": "append",
                    "datasource_name": target_ds_name,
                    "rows": 650,
                    "rows_quarantine": 0,
                    "result": "error",
                    "error": re.compile("Code: 395. DB::Exception: Error: while executing 'FUNCTION.*"),
                    "read_rows": expected_rows,
                    "read_bytes": 11976,
                    "written_rows": 650,
                    "written_bytes": 650,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "pipe_id": pipe.id,
                    "pipe_name": pipe_name,
                    "release": "",
                },
            ]
        )

    @tornado.testing.gen_test
    async def test_datasource_ops_log_append_without_materializations_ndjson_url(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        name = "test_ops_logs_tracker_ndjson_url"

        name = "test_db_stats_in_blocks_ndsjon"
        params = {
            "token": token,
            "name": name,
            "mode": "create",
            "format": "ndjson",
            "debug": "blocks",
            "schema": "`a` String `json:$.a`",
            "url": self.get_url_for_sql("select '1,2,3,4' as a format JSONEachRow"),
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        job = await self.get_finalised_job_async(json.loads(response.body)["id"], debug="blocks")
        self.assertEqual(job.status, "done")

        expected_rows = 1
        expected_rows_quarantine = 0

        self.expect_ops_log(
            [
                {"event_type": "create", "datasource_name": name, "options": {"source": "schema"}, "result": "ok"},
                {
                    "event_type": "append",
                    "datasource_name": name,
                    "rows": expected_rows,
                    "rows_quarantine": expected_rows_quarantine,
                    "result": "ok",
                    "read_rows": 0,
                    "read_bytes": 0,
                    "written_rows": expected_rows,
                    "written_bytes": 16,
                    "written_rows_quarantine": expected_rows_quarantine,
                    "written_bytes_quarantine": 0,
                    "pipe_id": "",
                    "pipe_name": "",
                    "release": "",
                },
            ]
        )

    @tornado.testing.gen_test
    async def test_datasource_ops_log_append_with_failed_materializations_ndjson_url(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        rand = str(uuid.uuid4())[:8]
        ds_name = f"test_ops_logs_tracker_ndjson_url_{rand}"

        params = {
            "token": token,
            "name": ds_name,
            "format": "ndjson",
            "schema": """
                        `date` DateTime `json:$.date`, `event` String `json:$.event`
                        """,
            "mode": "create",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response)

        target_ds_name = f"mat_view_node_ds_{rand}"
        params = {
            "token": token,
            "name": target_ds_name,
            "mode": "create",
            "format": "ndjson",
            "schema": """
                        `date` DateTime `json:$.date`, `event` String `json:$.event`
                      """,
            "engine_partition_key": "toYYYYMMDDhhmmss(date)",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        # create a pipe's node with a view to that datasource
        pipe_name = f"test_mat_view_{rand}"
        pipe = Users.add_pipe_sync(u, pipe_name, "select * from test_table")
        params = {
            "token": token,
            "name": "mat_view_node",
            "type": "materialized",
            "datasource": target_ds_name,
        }
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=f"select * from {ds_name}"
        )
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200, response)
        self.assertEqual(pipe_node["name"], "mat_view_node")
        ds = Users.get_datasource(u, target_ds_name)
        self.assertEqual(pipe_node["materialized"], ds.id)

        params = {
            "token": token,
            "name": ds_name,
            "mode": "append",
            "format": "ndjson",
            "debug": "blocks",
            "url": "https://storage.googleapis.com/tb-tests/events_12.ndjson",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        job = await self.get_finalised_job_async(json.loads(response.body)["id"], debug="blocks")
        self.assertEqual(job.status, "error")

        expected_rows = 13
        expected_rows_quarantine = 0

        self.expect_ops_log(
            [
                {"event_type": "create", "datasource_name": ds_name, "options": {"source": "schema"}, "result": "ok"},
                {
                    "event_type": "create",
                    "datasource_name": target_ds_name,
                    "options": {"source": "schema"},
                    "result": "ok",
                },
                {
                    "event_type": "append",
                    "datasource_name": ds_name,
                    "rows": expected_rows,
                    "rows_quarantine": expected_rows_quarantine,
                    "result": "error",
                    "read_rows": 0,
                    "read_bytes": 0,
                    "written_rows": expected_rows,
                    "written_bytes": 322,
                    "written_rows_quarantine": expected_rows_quarantine,
                    "written_bytes_quarantine": 0,
                    "pipe_id": "",
                    "pipe_name": "",
                    "release": "",
                },
                {
                    "event_type": "append",
                    "datasource_name": target_ds_name,
                    "rows": expected_rows,
                    "rows_quarantine": expected_rows_quarantine,
                    "result": "error",
                    "read_rows": 13,
                    "read_bytes": 322,
                    "written_rows": expected_rows,
                    "written_bytes": 322,
                    "written_rows_quarantine": expected_rows_quarantine,
                    "written_bytes_quarantine": 0,
                    "pipe_id": pipe.id,
                    "pipe_name": pipe_name,
                    "release": "",
                },
            ]
        )

    @tornado.testing.gen_test
    async def test_datasource_ops_log_append_with_materializations_csv_url(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        rand = str(uuid.uuid4())[:8]
        ds_name = f"test_ops_logs_tracker_csv_{rand}"

        params = {
            "token": token,
            "name": ds_name,
            "schema": """
                            d Int32
                        """,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        # create a pipe's node with a view to that datasource
        pipe_name = f"test_mat_view_{rand}"
        pipe = Users.add_pipe_sync(u, pipe_name, "select * from test_table")
        target_ds_name = f"mat_view_node_ds_{rand}"
        params = {
            "token": token,
            "name": "mat_view_node",
            "type": "materialized",
            "datasource": target_ds_name,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
        }
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}", method="POST", body=f"select d * 2 as b from {ds_name}"
        )
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(pipe_node["name"], "mat_view_node")
        ds = Users.get_datasource(u, target_ds_name)
        self.assertEqual(pipe_node["materialized"], ds.id)

        # first append
        params = {
            "token": token,
            "name": ds_name,
            "mode": "append",
            "format": "csv",
            "debug": "blocks",
            "url": self.get_url_for_sql("select 1 format CSV"),
        }
        append_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(append_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job_1 = await self.get_finalised_job_async(json.loads(response.body)["id"], debug="blocks")
        self.assertEqual(job_1.status, "done")

        self.expect_ops_log(
            [
                {"event_type": "create", "datasource_name": ds_name, "options": {"source": "schema"}, "result": "ok"},
                {
                    "event_type": "create",
                    "datasource_name": target_ds_name,
                    "options": {"source": "pipe"},
                    "result": "ok",
                },
                {
                    "event_type": "append",
                    "datasource_name": ds_name,
                    "operation_id": job_1.id,
                    "rows": 1,
                    "rows_quarantine": 0,
                    "result": "ok",
                    "read_rows": 0,
                    "read_bytes": 0,
                    "written_rows": 1,
                    "written_bytes": 4,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "pipe_id": "",
                    "pipe_name": "",
                    "release": "",
                },
                {
                    "event_type": "append",
                    "datasource_name": target_ds_name,
                    "operation_id": job_1.id,
                    "rows": 1,
                    "rows_quarantine": 0,
                    "result": "ok",
                    "read_rows": 1,
                    "read_bytes": 4,
                    "written_rows": 1,
                    "written_bytes": 8,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "pipe_id": pipe.id,
                    "pipe_name": pipe_name,
                    "release": "",
                },
            ]
        )

    @tornado.testing.gen_test
    async def test_datasource_ops_log_append_with_failed_materializations_csv_url(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        rand = str(uuid.uuid4())[:8]
        ds_name = f"test_ops_logs_tracker_csv_{rand}"

        params = {
            "token": token,
            "name": ds_name,
            "schema": """
                            d Int32
                        """,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        # create a pipe's node with a view to that datasource
        pipe_name = f"test_mat_view_{rand}"
        pipe = Users.add_pipe_sync(u, pipe_name, "select * from test_table")
        target_ds_name = f"mat_view_node_ds_{rand}"
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
            body=f"select throwIf(d = 1, 'Error') as b from {ds_name}",
        )
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(pipe_node["name"], "mat_view_node")
        ds = Users.get_datasource(u, target_ds_name)
        self.assertEqual(pipe_node["materialized"], ds.id)

        # first append
        params = {
            "token": token,
            "name": ds_name,
            "mode": "append",
            "format": "csv",
            "debug": "blocks",
            "url": self.get_url_for_sql("select 1 format CSV"),
        }
        append_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(append_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job_1 = await self.get_finalised_job_async(json.loads(response.body)["id"], debug="blocks")
        self.assertEqual(job_1.status, "error")

        self.expect_ops_log(
            [
                {"event_type": "create", "datasource_name": ds_name, "options": {"source": "schema"}, "result": "ok"},
                {
                    "event_type": "create",
                    "datasource_name": target_ds_name,
                    "options": {"source": "pipe"},
                    "result": "ok",
                },
                {
                    "event_type": "append",
                    "datasource_name": ds_name,
                    "operation_id": job_1.id,
                    "rows": 1,
                    "rows_quarantine": 0,
                    "result": "error",
                    "error": "There are blocks with errors",
                    "read_rows": 0,
                    "read_bytes": 0,
                    "written_rows": 1,
                    "written_bytes": 4,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "pipe_id": "",
                    "pipe_name": "",
                    "release": "",
                },
                {
                    "event_type": "append",
                    "datasource_name": target_ds_name,
                    "operation_id": job_1.id,
                    "rows": 0,
                    "rows_quarantine": 0,
                    "result": "error",
                    "error": re.compile("Code: 395.*"),
                    "read_rows": 1,
                    "read_bytes": 4,
                    "written_rows": 0,
                    "written_bytes": 0,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "pipe_id": pipe.id,
                    "pipe_name": pipe_name,
                    "release": "",
                },
            ]
        )

    @tornado.testing.gen_test
    async def test_datasource_ops_log_append_with_materializations_from_shared_workspace(self):
        # workspace_a -> ds_name
        # workspace_b -> ds_name (shared_from workspace_a), test_mat_view, target_ds_name
        workspace_a = Users.get_by_id(self.WORKSPACE_ID)
        user_a = UserAccount.get_by_id(self.USER_ID)
        token_a = Users.get_token_for_scope(workspace_a, scopes.ADMIN)
        token_user_a = UserAccount.get_token_for_scope(user_a, scopes.AUTH)
        rand = str(uuid.uuid4())[:8]
        ds_name = f"test_ops_logs_tracker_csv_{rand}"

        params = {
            "token": token_a,
            "name": ds_name,
            "schema": """
                            d Int32
                        """,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        ws_name = f"user_b_{uuid.uuid4().hex}"
        workspace_b = await self.tb_api_proxy_async.register_user_and_workspace(
            f"{ws_name}@example.com", f"{ws_name}_workspace"
        )
        user_b = UserAccount.get_by_email(f"{ws_name}@example.com")
        token_workspace_b = Users.get_token_for_scope(workspace_b, scopes.ADMIN)
        token_user_b = UserAccount.get_token_for_scope(user_b, scopes.AUTH)

        landing_ds = Users.get_datasource(workspace_a, ds_name)

        await self.tb_api_proxy_async.invite_user_to_workspace(
            token=token_user_b, workspace_id=workspace_b.id, user_to_invite_email=user_a.email
        )

        await self.tb_api_proxy_async.share_datasource_with_another_workspace(
            token=token_user_a,
            datasource_id=landing_ds.id,
            origin_workspace_id=workspace_a.id,
            destination_workspace_id=workspace_b.id,
        )

        # create a pipe's node with a view to that datasource
        pipe_name = "test_mat_view"
        pipe = Users.add_pipe_sync(workspace_b, pipe_name, "select * from test_table")
        target_ds_name = "mat_view_node_ds"
        params = {
            "token": token_workspace_b,
            "name": "mat_view_node",
            "type": "materialized",
            "datasource": target_ds_name,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
        }
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}",
            method="POST",
            body=f"select d * 2 as b from {workspace_a.name}.{ds_name}",
        )
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(pipe_node["name"], "mat_view_node")
        target_ds = Users.get_datasource(workspace_b, target_ds_name)
        self.assertEqual(pipe_node["materialized"], target_ds.id)

        # first append
        params = {
            "token": token_a,
            "name": ds_name,
            "mode": "append",
            "format": "csv",
            "debug": "blocks",
            "url": self.get_url_for_sql("select 1 format CSV"),
        }
        append_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(append_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"], debug="blocks")
        self.assertEqual(job.status, "done")

        # second append
        params = {
            "token": token_a,
            "name": ds_name,
            "mode": "append",
            "format": "csv",
            "debug": "blocks",
            "url": self.get_url_for_sql("select 2 format CSV"),
        }
        append_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(append_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"], debug="blocks")
        self.assertEqual(job.status, "done")

        self.expect_ops_log(
            [
                {"event_type": "create", "datasource_name": ds_name, "options": {"source": "schema"}, "result": "ok"},
                {
                    "event_type": "append",
                    "datasource_name": ds_name,
                    "rows": 1,
                    "rows_quarantine": 0,
                    "result": "ok",
                    "read_rows": 0,
                    "read_bytes": 0,
                    "written_rows": 1,
                    "written_bytes": 4,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "pipe_id": "",
                    "pipe_name": "",
                    "release": "",
                },
                {
                    "event_type": "append",
                    "datasource_name": ds_name,
                    "rows": 1,
                    "rows_quarantine": 0,
                    "result": "ok",
                    "read_rows": 0,
                    "read_bytes": 0,
                    "written_rows": 1,
                    "written_bytes": 4,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "pipe_id": "",
                    "pipe_name": "",
                    "release": "",
                },
            ]
        )

        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": target_ds_name,
                    "options": {"source": "pipe"},
                    "result": "ok",
                },
                {
                    "event_type": "append",
                    "datasource_name": target_ds_name,
                    "rows": 1,
                    "rows_quarantine": 0,
                    "result": "ok",
                    "read_rows": 1,
                    "read_bytes": 4,
                    "written_rows": 1,
                    "written_bytes": 8,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "pipe_id": pipe.id,
                    "pipe_name": pipe_name,
                    "release": "",
                },
                {
                    "event_type": "append",
                    "datasource_name": target_ds_name,
                    "rows": 1,
                    "rows_quarantine": 0,
                    "result": "ok",
                    "read_rows": 1,
                    "read_bytes": 4,
                    "written_rows": 1,
                    "written_bytes": 8,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "pipe_id": pipe.id,
                    "pipe_name": pipe_name,
                    "release": "",
                },
            ],
            workspace=workspace_b,
        )

    @tornado.testing.gen_test
    async def test_datasource_ops_log_append_with_materializations_from_shared_workspace_more_than_one_level(self):
        # workspace_a -> ds_name
        # workspace_b -> ds_name (shared_from workspace_a), test_mat_view_b, target_ds_name_b
        # workspace_c -> target_ds_name_b (shared_from workspace_b), test_mat_view_c, target_ds_name_c
        workspace_a = Users.get_by_id(self.WORKSPACE_ID)
        user_a = UserAccount.get_by_id(self.USER_ID)
        token_a = Users.get_token_for_scope(workspace_a, scopes.ADMIN)
        token_user_a = UserAccount.get_token_for_scope(user_a, scopes.AUTH)
        rand = str(uuid.uuid4())[:8]
        ds_name = f"test_ops_logs_tracker_csv_{rand}"

        params = {
            "token": token_a,
            "name": ds_name,
            "schema": """
                            d Int32
                        """,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        ws_name = f"user_b_{uuid.uuid4().hex}"
        workspace_b = await self.tb_api_proxy_async.register_user_and_workspace(
            f"{ws_name}@example.com", f"{ws_name}_workspace"
        )
        user_b = UserAccount.get_by_email(f"{ws_name}@example.com")
        token_workspace_b = Users.get_token_for_scope(workspace_b, scopes.ADMIN)
        token_user_b = UserAccount.get_token_for_scope(user_b, scopes.AUTH)

        landing_ds = Users.get_datasource(workspace_a, ds_name)

        await self.tb_api_proxy_async.invite_user_to_workspace(
            token=token_user_b, workspace_id=workspace_b.id, user_to_invite_email=user_a.email
        )

        await self.tb_api_proxy_async.share_datasource_with_another_workspace(
            token=token_user_a,
            datasource_id=landing_ds.id,
            origin_workspace_id=workspace_a.id,
            destination_workspace_id=workspace_b.id,
        )

        # create a pipe's node with a view to that datasource
        pipe_name_b = "test_mat_view_b"
        pipe_b = Users.add_pipe_sync(workspace_b, pipe_name_b, "select * from test_table")
        target_ds_name_b = "mat_view_node_ds_b"
        params = {
            "token": token_workspace_b,
            "name": "mat_view_node_b",
            "type": "materialized",
            "datasource": target_ds_name_b,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
        }
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name_b}/nodes?{urlencode(params)}",
            method="POST",
            body=f"select d * 2 as b from {workspace_a.name}.{ds_name}",
        )
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(pipe_node["name"], "mat_view_node_b")
        target_ds_b = Users.get_datasource(workspace_b, target_ds_name_b)
        self.assertEqual(pipe_node["materialized"], target_ds_b.id)

        ws_name = f"user_c_{uuid.uuid4().hex}"
        workspace_c = await self.tb_api_proxy_async.register_user_and_workspace(
            f"{ws_name}@example.com", f"{ws_name}_workspace"
        )
        user_c = UserAccount.get_by_email(f"{ws_name}@example.com")
        token_workspace_c = Users.get_token_for_scope(workspace_c, scopes.ADMIN)
        token_user_c = UserAccount.get_token_for_scope(user_c, scopes.AUTH)

        await self.tb_api_proxy_async.invite_user_to_workspace(
            token=token_user_c, workspace_id=workspace_c.id, user_to_invite_email=user_b.email
        )

        await self.tb_api_proxy_async.share_datasource_with_another_workspace(
            token=token_user_b,
            datasource_id=target_ds_b.id,
            origin_workspace_id=workspace_b.id,
            destination_workspace_id=workspace_c.id,
        )

        # create a pipe's node with a view to that datasource
        pipe_name_c = "test_mat_view_c"
        pipe_c = Users.add_pipe_sync(workspace_c, pipe_name_c, "select * from test_table")
        target_ds_name_c = "mat_view_node_ds_c"
        params = {
            "token": token_workspace_c,
            "name": "mat_view_node_c",
            "type": "materialized",
            "datasource": target_ds_name_c,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
        }
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name_c}/nodes?{urlencode(params)}",
            method="POST",
            body=f"select b * 2 as c from {workspace_b.name}.{target_ds_name_b}",
        )
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(pipe_node["name"], "mat_view_node_c")
        target_ds_c = Users.get_datasource(workspace_c, target_ds_name_c)
        self.assertEqual(pipe_node["materialized"], target_ds_c.id)

        # first append
        params = {
            "token": token_a,
            "name": ds_name,
            "mode": "append",
            "format": "csv",
            "debug": "blocks",
            "url": self.get_url_for_sql("select 1 format CSV"),
        }
        append_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(append_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"], debug="blocks")
        self.assertEqual(job.status, "done")

        # second append
        params = {
            "token": token_a,
            "name": ds_name,
            "mode": "append",
            "format": "csv",
            "debug": "blocks",
            "url": self.get_url_for_sql("select 2 format CSV"),
        }
        append_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(append_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done")

        self.expect_ops_log(
            [
                {"event_type": "create", "datasource_name": ds_name, "options": {"source": "schema"}, "result": "ok"},
                {
                    "event_type": "append",
                    "datasource_name": ds_name,
                    "rows": 1,
                    "rows_quarantine": 0,
                    "result": "ok",
                    "read_rows": 0,
                    "read_bytes": 0,
                    "written_rows": 1,
                    "written_bytes": 4,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "pipe_id": "",
                    "pipe_name": "",
                    "release": "",
                },
                {
                    "event_type": "append",
                    "datasource_name": ds_name,
                    "rows": 1,
                    "rows_quarantine": 0,
                    "result": "ok",
                    "read_rows": 0,
                    "read_bytes": 0,
                    "written_rows": 1,
                    "written_bytes": 4,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "pipe_id": "",
                    "pipe_name": "",
                    "release": "",
                },
            ],
            workspace=workspace_a,
        )

        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": target_ds_name_b,
                    "options": {"source": "pipe"},
                    "result": "ok",
                },
                {
                    "event_type": "append",
                    "datasource_name": target_ds_name_b,
                    "rows": 1,
                    "rows_quarantine": 0,
                    "result": "ok",
                    "read_rows": 1,
                    "read_bytes": 4,
                    "written_rows": 1,
                    "written_bytes": 8,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "pipe_id": pipe_b.id,
                    "pipe_name": pipe_name_b,
                    "release": "",
                },
                {
                    "event_type": "append",
                    "datasource_name": target_ds_name_b,
                    "rows": 1,
                    "rows_quarantine": 0,
                    "result": "ok",
                    "read_rows": 1,
                    "read_bytes": 4,
                    "written_rows": 1,
                    "written_bytes": 8,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "pipe_id": pipe_b.id,
                    "pipe_name": pipe_name_b,
                    "release": "",
                },
            ],
            workspace=workspace_b,
        )

        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": target_ds_name_c,
                    "options": {"source": "pipe"},
                    "result": "ok",
                },
                {
                    "event_type": "append",
                    "datasource_name": target_ds_name_c,
                    "rows": 1,
                    "rows_quarantine": 0,
                    "result": "ok",
                    "read_rows": 1,
                    "read_bytes": 8,
                    "written_rows": 1,
                    "written_bytes": 8,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "pipe_id": pipe_c.id,
                    "pipe_name": pipe_name_c,
                    "release": "",
                },
                {
                    "event_type": "append",
                    "datasource_name": target_ds_name_c,
                    "rows": 1,
                    "rows_quarantine": 0,
                    "result": "ok",
                    "read_rows": 1,
                    "read_bytes": 8,
                    "written_rows": 1,
                    "written_bytes": 8,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "pipe_id": pipe_c.id,
                    "pipe_name": pipe_name_c,
                    "release": "",
                },
            ],
            workspace=workspace_c,
        )

    @tornado.testing.gen_test
    async def test_datasource_ops_log_append_with_materializations_from_shared_workspace_several_per_level(self):
        # workspace_a -> ds_name
        # workspace_b -> ds_name (shared_from workspace_a), test_mat_view_b, target_ds_name_b
        # workspace_c -> target_ds_name_b (shared_from workspace_b), test_mat_view_c, target_ds_name_c
        # workspace_d -> ds_name (shared_from workspace_a), test_mat_view_d, target_ds_name_d
        # workspace_e -> target_ds_name_b (shared_from workspace_b), test_mat_view_e, target_ds_name_e
        workspace_a = Users.get_by_id(self.WORKSPACE_ID)
        user_a = UserAccount.get_by_id(self.USER_ID)
        token_a = Users.get_token_for_scope(workspace_a, scopes.ADMIN)
        token_user_a = UserAccount.get_token_for_scope(user_a, scopes.AUTH)
        rand = str(uuid.uuid4())[:8]
        ds_name = f"test_ops_logs_tracker_csv_{rand}"

        params = {
            "token": token_a,
            "name": ds_name,
            "schema": """
                            d Int32
                        """,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        ws_name = f"user_b_{uuid.uuid4().hex}"
        workspace_b = await self.tb_api_proxy_async.register_user_and_workspace(
            f"{ws_name}@example.com", f"{ws_name}_workspace"
        )
        user_b = UserAccount.get_by_email(f"{ws_name}@example.com")
        token_workspace_b = Users.get_token_for_scope(workspace_b, scopes.ADMIN)
        token_user_b = UserAccount.get_token_for_scope(user_b, scopes.AUTH)

        landing_ds = Users.get_datasource(workspace_a, ds_name)

        await self.tb_api_proxy_async.invite_user_to_workspace(
            token=token_user_b, workspace_id=workspace_b.id, user_to_invite_email=user_a.email
        )

        await self.tb_api_proxy_async.share_datasource_with_another_workspace(
            token=token_user_a,
            datasource_id=landing_ds.id,
            origin_workspace_id=workspace_a.id,
            destination_workspace_id=workspace_b.id,
        )

        # create a pipe's node with a view to that datasource
        pipe_name_b = "test_mat_view_b"
        pipe_b = Users.add_pipe_sync(workspace_b, pipe_name_b, "select * from test_table")
        target_ds_name_b = "mat_view_node_ds_b"
        params = {
            "token": token_workspace_b,
            "name": "mat_view_node_b",
            "type": "materialized",
            "datasource": target_ds_name_b,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
        }
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name_b}/nodes?{urlencode(params)}",
            method="POST",
            body=f"select d * 2 as b from {workspace_a.name}.{ds_name}",
        )
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(pipe_node["name"], "mat_view_node_b")
        target_ds_b = Users.get_datasource(workspace_b, target_ds_name_b)
        self.assertEqual(pipe_node["materialized"], target_ds_b.id)

        ws_name = f"user_c_{uuid.uuid4().hex}"
        workspace_c = await self.tb_api_proxy_async.register_user_and_workspace(
            f"{ws_name}@example.com", f"{ws_name}_workspace"
        )
        user_c = UserAccount.get_by_email(f"{ws_name}@example.com")
        token_workspace_c = Users.get_token_for_scope(workspace_c, scopes.ADMIN)
        token_user_c = UserAccount.get_token_for_scope(user_c, scopes.AUTH)

        await self.tb_api_proxy_async.invite_user_to_workspace(
            token=token_user_c, workspace_id=workspace_c.id, user_to_invite_email=user_b.email
        )

        await self.tb_api_proxy_async.share_datasource_with_another_workspace(
            token=token_user_b,
            datasource_id=target_ds_b.id,
            origin_workspace_id=workspace_b.id,
            destination_workspace_id=workspace_c.id,
        )

        # create a pipe's node with a view to that datasource
        pipe_name_c = "test_mat_view_c"
        pipe_c = Users.add_pipe_sync(workspace_c, pipe_name_c, "select * from test_table")
        target_ds_name_c = "mat_view_node_ds_c"
        params = {
            "token": token_workspace_c,
            "name": "mat_view_node_c",
            "type": "materialized",
            "datasource": target_ds_name_c,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
        }
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name_c}/nodes?{urlencode(params)}",
            method="POST",
            body=f"select b * 2 as c from {workspace_b.name}.{target_ds_name_b}",
        )
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(pipe_node["name"], "mat_view_node_c")
        target_ds_c = Users.get_datasource(workspace_c, target_ds_name_c)
        self.assertEqual(pipe_node["materialized"], target_ds_c.id)

        ws_name = f"user_d_{uuid.uuid4().hex}"
        workspace_d = await self.tb_api_proxy_async.register_user_and_workspace(
            f"{ws_name}@example.com", f"{ws_name}_workspace"
        )
        user_d = UserAccount.get_by_email(f"{ws_name}@example.com")
        token_workspace_d = Users.get_token_for_scope(workspace_d, scopes.ADMIN)
        token_user_d = UserAccount.get_token_for_scope(user_d, scopes.AUTH)

        landing_ds = Users.get_datasource(workspace_a, ds_name)

        await self.tb_api_proxy_async.invite_user_to_workspace(
            token=token_user_d, workspace_id=workspace_d.id, user_to_invite_email=user_a.email
        )

        await self.tb_api_proxy_async.share_datasource_with_another_workspace(
            token=token_user_a,
            datasource_id=landing_ds.id,
            origin_workspace_id=workspace_a.id,
            destination_workspace_id=workspace_d.id,
        )

        # create a pipe's node with a view to that datasource
        pipe_name_d = "test_mat_view_d"
        pipe_d = Users.add_pipe_sync(workspace_d, pipe_name_d, "select * from test_table")
        target_ds_name_d = "mat_view_node_ds_d"
        params = {
            "token": token_workspace_d,
            "name": "mat_view_node_d",
            "type": "materialized",
            "datasource": target_ds_name_d,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
        }
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name_d}/nodes?{urlencode(params)}",
            method="POST",
            body=f"select d * 2 as b from {workspace_a.name}.{ds_name}",
        )
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(pipe_node["name"], "mat_view_node_d")
        target_ds_d = Users.get_datasource(workspace_d, target_ds_name_d)
        self.assertEqual(pipe_node["materialized"], target_ds_d.id)

        ws_name = f"user_e_{uuid.uuid4().hex}"
        workspace_e = await self.tb_api_proxy_async.register_user_and_workspace(
            f"{ws_name}@example.com", f"{ws_name}_workspace"
        )
        user_e = UserAccount.get_by_email(f"{ws_name}@example.com")
        token_workspace_e = Users.get_token_for_scope(workspace_e, scopes.ADMIN)
        token_user_e = UserAccount.get_token_for_scope(user_e, scopes.AUTH)

        await self.tb_api_proxy_async.invite_user_to_workspace(
            token=token_user_e, workspace_id=workspace_e.id, user_to_invite_email=user_b.email
        )

        await self.tb_api_proxy_async.share_datasource_with_another_workspace(
            token=token_user_b,
            datasource_id=target_ds_b.id,
            origin_workspace_id=workspace_b.id,
            destination_workspace_id=workspace_e.id,
        )

        # create a pipe's node with a view to that datasource
        pipe_name_e = "test_mat_view_e"
        pipe_e = Users.add_pipe_sync(workspace_e, pipe_name_e, "select * from test_table")
        target_ds_name_e = "mat_view_node_ds_e"
        params = {
            "token": token_workspace_e,
            "name": "mat_view_node_e",
            "type": "materialized",
            "datasource": target_ds_name_e,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
        }
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name_e}/nodes?{urlencode(params)}",
            method="POST",
            body=f"select b * 2 as c from {workspace_b.name}.{target_ds_name_b}",
        )
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(pipe_node["name"], "mat_view_node_e")
        target_ds_e = Users.get_datasource(workspace_e, target_ds_name_e)
        self.assertEqual(pipe_node["materialized"], target_ds_e.id)

        # append
        params = {
            "token": token_a,
            "name": ds_name,
            "mode": "append",
            "format": "csv",
            "debug": "blocks",
            "url": self.get_url_for_sql("select 1 format CSV"),
        }
        append_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(append_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"], debug="blocks")
        self.assertEqual(job.status, "done")

        self.expect_ops_log(
            [
                {"event_type": "create", "datasource_name": ds_name, "options": {"source": "schema"}, "result": "ok"},
                {
                    "event_type": "append",
                    "datasource_name": ds_name,
                    "rows": 1,
                    "rows_quarantine": 0,
                    "result": "ok",
                    "read_rows": 0,
                    "read_bytes": 0,
                    "written_rows": 1,
                    "written_bytes": 4,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "pipe_id": "",
                    "pipe_name": "",
                    "release": "",
                },
            ]
        )

        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": target_ds_name_b,
                    "options": {"source": "pipe"},
                    "result": "ok",
                },
                {
                    "event_type": "append",
                    "datasource_name": target_ds_name_b,
                    "rows": 1,
                    "rows_quarantine": 0,
                    "result": "ok",
                    "read_rows": 1,
                    "read_bytes": 4,
                    "written_rows": 1,
                    "written_bytes": 8,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "pipe_id": pipe_b.id,
                    "pipe_name": pipe_name_b,
                    "release": "",
                },
            ],
            workspace=workspace_b,
        )

        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": target_ds_name_c,
                    "options": {"source": "pipe"},
                    "result": "ok",
                },
                {
                    "event_type": "append",
                    "datasource_name": target_ds_name_c,
                    "rows": 1,
                    "rows_quarantine": 0,
                    "result": "ok",
                    "read_rows": 1,
                    "read_bytes": 8,
                    "written_rows": 1,
                    "written_bytes": 8,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "pipe_id": pipe_c.id,
                    "pipe_name": pipe_name_c,
                    "release": "",
                },
            ],
            workspace=workspace_c,
        )

        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": target_ds_name_d,
                    "options": {"source": "pipe"},
                    "result": "ok",
                },
                {
                    "event_type": "append",
                    "datasource_name": target_ds_name_d,
                    "rows": 1,
                    "rows_quarantine": 0,
                    "result": "ok",
                    "read_rows": 1,
                    "read_bytes": 4,
                    "written_rows": 1,
                    "written_bytes": 8,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "pipe_id": pipe_d.id,
                    "pipe_name": pipe_name_d,
                    "release": "",
                },
            ],
            workspace=workspace_d,
        )

        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": target_ds_name_e,
                    "options": {"source": "pipe"},
                    "result": "ok",
                },
                {
                    "event_type": "append",
                    "datasource_name": target_ds_name_e,
                    "rows": 1,
                    "rows_quarantine": 0,
                    "result": "ok",
                    "read_rows": 1,
                    "read_bytes": 8,
                    "written_rows": 1,
                    "written_bytes": 8,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "pipe_id": pipe_e.id,
                    "pipe_name": pipe_name_e,
                    "release": "",
                },
            ],
            workspace=workspace_e,
        )

    @tornado.testing.gen_test
    async def test_datasource_ops_log_append_with_materialization_from_quarantine(self):
        """Test that datasource_ops_log records exist when materializing from a datasource's quarantine"""
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        # Create a datasource
        ds_name = "test_ops_logs_tracker_quarantine"
        params = {
            "token": token,
            "name": ds_name,
            "mode": "create",
            "format": "ndjson",
            "debug": "blocks",
            "schema": "`a` String `json:$.a`",
            # 'url': self.get_url_for_sql("select '1,2,3,4' as a format JSONEachRow"),
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        # job = await self.get_finalised_job_async(json.loads(response.body)['id'], debug='blocks')
        # self.assertEqual(job.status, 'done')

        # create a materialized view from the above datasource's quarantine table.
        # It materializes to a new datasource
        pipe_name = "test_mat_view"
        pipe = Users.add_pipe_sync(u, pipe_name, "select * from test_table")
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
            body=f"select c__error_column as error_column from {ds_name}_quarantine",
        )
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(pipe_node["name"], "mat_view_node")
        ds = Users.get_datasource(u, target_ds_name)
        self.assertEqual(pipe_node["materialized"], ds.id)

        # append that will send rows to quarantine
        params = {
            "token": token,
            "name": ds_name,
            "mode": "append",
            "format": "ndjson",
            "debug": "blocks",
            "url": self.get_url_for_sql("select 1 as a format JSONEachRow"),
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        job = await self.get_finalised_job_async(json.loads(response.body)["id"], debug="blocks")
        self.assertEqual(job.status, "error")
        self.assertEqual(job["quarantine_rows"], 1)

        self.expect_ops_log(
            [
                {"event_type": "create", "datasource_name": ds_name, "options": {"source": "schema"}, "result": "ok"},
                {
                    "event_type": "create",
                    "datasource_name": target_ds_name,
                    "options": {"source": "pipe"},
                    "result": "ok",
                },
                {
                    "event_type": "append",
                    "datasource_name": ds_name,
                    "rows": 0,
                    "rows_quarantine": 1,
                    "result": "ok",
                    "read_rows": 0,
                    "read_bytes": 0,
                    "written_rows": 0,
                    "written_bytes": 0,
                    "written_rows_quarantine": 1,
                    "written_bytes_quarantine": 183,
                    "pipe_id": "",
                    "pipe_name": "",
                    "release": "",
                },
                {
                    "event_type": "append",
                    "datasource_name": target_ds_name,
                    "rows": 1,
                    "rows_quarantine": 0,
                    "result": "ok",
                    "read_rows": 1,
                    "read_bytes": 18,
                    "written_rows": 1,
                    "written_bytes": 18,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "pipe_id": pipe.id,
                    "pipe_name": pipe_name,
                    "release": "",
                },
            ]
        )

    @tornado.testing.gen_test
    async def test_datasource_ops_log_append_with_materialization_in_shared_quarantine(self):
        workspace_a = Users.get_by_id(self.WORKSPACE_ID)
        user_a = UserAccount.get_by_id(self.USER_ID)
        token_a = Users.get_token_for_scope(workspace_a, scopes.ADMIN)
        token_user_a = UserAccount.get_token_for_scope(user_a, scopes.AUTH)

        ds_name = "test_tracker_shared_quarantine"
        params = {
            "token": token_a,
            "name": ds_name,
            "mode": "create",
            "format": "ndjson",
            "debug": "blocks",
            "schema": "`a` String `json:$.a`",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        ws_name = f"user_b_{uuid.uuid4().hex}"
        workspace_b = await self.tb_api_proxy_async.register_user_and_workspace(
            f"{ws_name}@example.com", f"{ws_name}_workspace"
        )
        user_b = UserAccount.get_by_email(f"{ws_name}@example.com")
        token_workspace_b = Users.get_token_for_scope(workspace_b, scopes.ADMIN)
        token_user_b = UserAccount.get_token_for_scope(user_b, scopes.AUTH)

        landing_ds = Users.get_datasource(workspace_a, ds_name)

        await self.tb_api_proxy_async.invite_user_to_workspace(
            token=token_user_b, workspace_id=workspace_b.id, user_to_invite_email=user_a.email
        )

        await self.tb_api_proxy_async.share_datasource_with_another_workspace(
            token=token_user_a,
            datasource_id=landing_ds.id,
            origin_workspace_id=workspace_a.id,
            destination_workspace_id=workspace_b.id,
        )

        # create a pipe's node with a view to that datasource
        pipe_name = "test_mat_view"
        pipe = Users.add_pipe_sync(workspace_b, pipe_name, "select * from test_table")
        target_ds_name = "mat_view_node_ds"
        params = {
            "token": token_workspace_b,
            "name": "mat_view_node",
            "type": "materialized",
            "datasource": target_ds_name,
            "engine": "MergeTree",
            "engine_sorting_key": "tuple()",
        }
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes?{urlencode(params)}",
            method="POST",
            body=f"select c__error_column as error_column from {workspace_a.name}.{ds_name}_quarantine",
        )
        pipe_node = json.loads(response.body)
        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(pipe_node["name"], "mat_view_node")
        ds = Users.get_datasource(workspace_b, target_ds_name)
        self.assertEqual(pipe_node["materialized"], ds.id)

        # append with quarantine
        params = {
            "token": token_a,
            "name": ds_name,
            "mode": "append",
            "format": "ndjson",
            "debug": "blocks",
            "url": self.get_url_for_sql("select 1 as a format JSONEachRow"),
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        job = await self.get_finalised_job_async(json.loads(response.body)["id"], debug="blocks")
        self.assertEqual(job.status, "error")
        self.assertEqual(job["quarantine_rows"], 1)

        self.expect_ops_log(
            [
                {"event_type": "create", "datasource_name": ds_name, "options": {"source": "schema"}, "result": "ok"},
                {
                    "event_type": "append",
                    "datasource_name": ds_name,
                    "rows": 0,
                    "rows_quarantine": 1,
                    "result": "ok",
                    "read_rows": 0,
                    "read_bytes": 0,
                    "written_rows": 0,
                    "written_bytes": 0,
                    "written_rows_quarantine": 1,
                    "written_bytes_quarantine": 183,
                    "pipe_id": "",
                    "pipe_name": "",
                    "release": "",
                },
            ]
        )

        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": target_ds_name,
                    "options": {"source": "pipe"},
                    "result": "ok",
                },
                {
                    "event_type": "append",
                    "datasource_name": target_ds_name,
                    "rows": 1,
                    "rows_quarantine": 0,
                    "result": "ok",
                    "read_rows": 1,
                    "read_bytes": 18,
                    "written_rows": 1,
                    "written_bytes": 18,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "pipe_id": pipe.id,
                    "pipe_name": pipe_name,
                    "release": "",
                },
            ],
            workspace=workspace_b,
        )


class TestAPIDatasourceImportNetwork(TestAPIDatasourceBase):
    def get_app(self):
        settings = get_app_settings()
        settings["deny_local_networks"] = True
        settings["deny_networks"] = ("1.2.3.4",)
        self.app = app.make_app(settings)
        return self.app

    @tornado.testing.gen_test
    async def test_import_denied_url(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        csv_url = "http://1.2.3.4/test.csv"
        import_url = f"/v0/datasources?token={token}&url={csv_url}"

        response = await self.fetch_async(import_url, method="POST", body="")
        self.assertEqual(response.code, 400)

    @tornado.testing.gen_test
    async def test_import_denied_private(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        csv_url = "http://169.254.169.254/test.csv"
        import_url = f"/v0/datasources?token={token}&url={csv_url}"

        response = await self.fetch_async(import_url, method="POST", body="")
        self.assertEqual(response.code, 400)

    @tornado.testing.gen_test
    async def test_import_denied_url_after_redirection(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        http_server = start_http_redirect_server("https://1.1.1.1")
        self.app.settings["deny_local_networks"] = False
        self.app.settings["deny_networks"] = ("1.1.1.1",)
        import_url = f"/v0/datasources?token={token}&url={http_server}/test.csv"

        response = await self.fetch_async(import_url, method="POST", body="")
        self.assertEqual(response.code, 400)

    @tornado.testing.gen_test
    async def test_import_redirected_url_is_used(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        http_server = start_http_redirect_server(HTTP_ADDRESS)
        self.app.settings["deny_local_networks"] = False
        import_url = f"/v0/datasources?token={token}&url={http_server}/small.csv"

        response = await self.fetch_async(import_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done")
        self.assertIn(HTTP_ADDRESS, job.url)
        self.assertNotIn(http_server, job.url)


class TestAPIDatasourceResponse(TestAPIDatasourceBase):
    def setUp(self):
        super().setUp()
        self.u = Users.get_by_id(self.WORKSPACE_ID)
        self.token = Users.get_token_for_scope(self.u, scopes.ADMIN)

    @tornado.testing.gen_test
    async def test_debug_parameters_present(self):
        params = {"token": self.token, "name": "yt_1000", "mode": "create", "debug": "blocks, block_log, hook_log"}

        create_url = f"/v0/datasources?{urlencode(params)}"

        with fixture_file("yt_1000.csv") as fd:
            response = await self.fetch_full_body_upload_async(create_url, fd)

        result = json.loads(response.body)

        self.assertIn("blocks", result)
        self.assertIn("block_log", result)
        self.assertIn("hook_log", result)

    @tornado.testing.gen_test
    async def test_default_parameters(self):
        params = {"token": self.token, "name": "yt_1000", "mode": "create"}

        create_url = f"/v0/datasources?{urlencode(params)}"

        with fixture_file("yt_1000.csv") as fd:
            response = await self.fetch_full_body_upload_async(create_url, fd)

        result = json.loads(response.body)

        self.assertNotIn("blocks", result)
        self.assertNotIn("block_log", result)
        self.assertNotIn("hook_log", result)

    @tornado.testing.gen_test
    async def test_quarantine_error_response(self):
        params = {"token": self.token, "name": "test_import_body"}

        create_url = f"/v0/datasources?{urlencode(params)}"

        with fixture_file("yt_1000.csv") as fd:
            response = await self.fetch_full_body_upload_async(create_url, fd)

        result = json.loads(response.body)

        self.assertEqual(result["invalid_lines"], 0)
        self.assertEqual(result["quarantine_rows"], 670)
        self.assertEqual(result["error"], "There was an error with file contents: 670 rows in quarantine.")

    @tornado.testing.gen_test
    async def test_invalid_lines_quarantine_singular_error_response(self):
        SCHEMA = "foo String, bar String"

        params = {"token": self.token, "schema": SCHEMA, "name": "invalid_lines_ds", "mode": "create"}

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")

        append_params = {"token": self.token, "name": "invalid_lines_ds", "mode": "append"}

        append_url = f"/v0/datasources?{urlencode(append_params)}"

        with fixture_file("invalid_lines.csv") as fd:
            response = await self.fetch_full_body_upload_async(append_url, fd)

        result = json.loads(response.body)

        self.assertEqual(result["invalid_lines"], 1)
        self.assertEqual(result["quarantine_rows"], 1)
        self.assertEqual(
            result["error"], "There was an error with file contents: 1 row in quarantine and 1 invalid line."
        )

    @tornado.testing.gen_test
    async def test_invalid_lines_quarantine_plural_error_response(self):
        SCHEMA = "foo String, bar Int8"

        params = {"token": self.token, "schema": SCHEMA, "name": "invalid_lines_ds", "mode": "create"}

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")

        append_params = {"token": self.token, "name": "invalid_lines_ds", "mode": "append"}

        append_url = f"/v0/datasources?{urlencode(append_params)}"

        with fixture_file("invalid_lines_and_quarantine.csv") as fd:
            response = await self.fetch_full_body_upload_async(append_url, fd)

        result = json.loads(response.body)

        self.assertEqual(result["invalid_lines"], 2)
        self.assertEqual(result["quarantine_rows"], 4)
        self.assertEqual(
            result["error"], "There was an error with file contents: 4 rows in quarantine and 2 invalid lines."
        )


class TestAPIDatasourceDialectOverride(TestAPIDatasourceBase):
    def setUp(self):
        super().setUp()
        u = Users.get_by_id(self.WORKSPACE_ID)
        self.token = Users.get_token_for_scope(u, scopes.ADMIN)
        self.ds_name = "test_dialect_override"

        params = {
            "token": self.token,
            "name": self.ds_name,
            "schema": """
                a Int32,
                b String,
                c String,
                d Date,
                e String,
                f Float32
            """,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

    @tornado.testing.gen_test
    async def test_dialect_override_url(self):
        csv_url = f"{HTTP_ADDRESS}/dialect_escapechar.csv"
        params = {
            "mode": "append",
            "token": self.token,
            "name": self.ds_name,
            "dialect_escapechar": "\\",
            "url": csv_url,
        }
        append_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(append_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done")

    @tornado.testing.gen_test
    async def test_dialect_override_full_body(self):
        params = {
            "mode": "append",
            "token": self.token,
            "name": self.ds_name,
            "dialect_escapechar": "\\",
        }
        append_url = f"/v0/datasources?{urlencode(params)}"
        with fixture_file("dialect_escapechar.csv", mode="r") as fd:
            response = await self.fetch_full_body_upload_async(append_url, fd)
            self.assertEqual(response.code, 200, response.body)
            result = json.loads(response.body)
            self.assertFalse(result["error"])

    @tornado.testing.gen_test
    async def test_dialect_override_stream(self):
        params = {
            "token": self.token,
            "name": self.ds_name,
            "mode": "append",
            "dialect_escapechar": "\\",
        }
        append_url = f"/v0/datasources?{urlencode(params)}"

        url = self.get_url(append_url)
        post = sync_to_async(requests.post, thread_sensitive=False)
        r = await post(url, files=dict(csv=fixture_data("dialect_escapechar.csv", mode="rb")))
        self.assertEqual(r.status_code, 200, r.content)
        self.assertEqual(r.json()["error"], False)

    @tornado.testing.gen_test
    async def test_dialect_override_invalid_length_delimiter(self):
        csv_url = f"{HTTP_ADDRESS}/dialect_tab_delimiter.csv"
        params = {
            "mode": "append",
            "token": self.token,
            "name": self.ds_name,
            "dialect_delimiter": ",,",
            "url": csv_url,
        }
        append_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(append_url, method="POST", body="")
        self.assertEqual(response.code, 400, response.body)
        result = json.loads(response.body)
        self.assertEqual(result["error"], "The dialect delimiter must be a 1-character string")

    @tornado.testing.gen_test
    async def test_dialect_override_invalid_length_escapechar(self):
        params = {
            "mode": "append",
            "token": self.token,
            "name": self.ds_name,
            "dialect_escapechar": "\\\\",
        }
        append_url = f"/v0/datasources?{urlencode(params)}"
        with fixture_file("dialect_tab_delimiter.tsv", mode="r") as fd:
            response = await self.fetch_full_body_upload_async(append_url, fd)
            self.assertEqual(response.code, 400, response.body)
            result = json.loads(response.body)
            self.assertEqual(result["error"], "The dialect escapechar must be a 1-character string")

    @tornado.testing.gen_test
    async def test_dialect_override_tab_suggestion(self):
        params = {
            "mode": "append",
            "token": self.token,
            "name": self.ds_name,
            "dialect_delimiter": "\\t",
        }
        append_url = f"/v0/datasources?{urlencode(params)}"
        with fixture_file("dialect_tab_delimiter.tsv", mode="r") as fd:
            response = await self.fetch_full_body_upload_async(append_url, fd)
            self.assertEqual(response.code, 400, response.body)
            result = json.loads(response.body)
            self.assertEqual(
                result["error"],
                "The dialect delimiter must be a 1-character string. If you are trying to set a TAB delimiter, review your backslash-escaped characters. In bash-like environments, you can get ANSI C escape sequences using something like $'\t', for instance `curl -d dialect_delimiter=$'\t' ...`.",
            )

        params = {
            "mode": "append",
            "token": self.token,
            "name": self.ds_name,
            "dialect_delimiter": "\t",
        }
        append_url = f"/v0/datasources?{urlencode(params)}"
        with fixture_file("dialect_tab_delimiter.tsv", mode="r") as fd:
            response = await self.fetch_full_body_upload_async(append_url, fd)
            self.assertEqual(response.code, 200, response.body)
            result = json.loads(response.body)
            self.assertFalse(result["error"])


class TestAPIDatasourceSchemaCreation(TestAPIDatasourceBase):
    SCHEMA = "VendorID Int32, tpep_pickup_datetime DateTime"
    ENGINE = "Null"

    @tornado.testing.gen_test
    async def test_create_from_schema_name_required(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
            "schema": self.SCHEMA,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        result = json.loads(response.body)
        self.assertEqual(response.code, 400)
        self.assertEqual(result["error"], "Data Source name must be set when creating with schema")

    @tornado.testing.gen_test
    async def test_create_from_schema(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
            "name": "t_from_schema",
            "schema": self.SCHEMA,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        result = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(result["datasource"]["name"], "t_from_schema")
        self.expect_ops_log(
            {"event_type": "create", "datasource_name": "t_from_schema", "options": {"source": "schema"}},
        )

    @tornado.testing.gen_test
    async def test_create_from_schema_with_default_cast(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
            "name": "t_from_schema_cast",
            "schema": "VendorID Nullable(String) DEFAULT CAST(NULL, 'Nullable(String)'), tpep_pickup_datetime DateTime",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        result = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(result["datasource"]["name"], "t_from_schema_cast")
        self.expect_ops_log(
            {"event_type": "create", "datasource_name": "t_from_schema_cast", "options": {"source": "schema"}},
        )

    @tornado.testing.gen_test
    async def test_create_from_schema_with_cluster(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
            "name": "t_from_schema",
            "schema": self.SCHEMA,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        result = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(result["datasource"]["name"], "t_from_schema")
        self.assertEqual(result["datasource"]["cluster"], "tinybird")

    @tornado.testing.gen_test
    async def test_create_from_schema_with_cluster_error(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        params = {
            "token": token,
            "name": "t_from_schema_error",
            "schema": "owner_id String, bad_sum SimpleAggregateFunction(sum, Float32)",
            "engine": "AggregatingMergeTree",
            "engine_primary_key": "owner_id",
            "engine_sorting_key": "owner_id",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        result = json.loads(response.body)
        self.assertEqual(response.code, 400)
        self.assertRegexpMatches(
            result["error"],
            "Incompatible data types between aggregate function 'sum'"
            " which returns Float64 and column storage type Float32.*",
        )

    @tornado.testing.gen_test
    async def test_create_from_schema_with_replica(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
            "name": "t_from_schema",
            "schema": self.SCHEMA,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        result = json.loads(response.body)

        self.assertEqual(response.code, 200)
        self.assertEqual(result["datasource"]["name"], "t_from_schema")
        ds = Users.get_datasource(u, "t_from_schema")
        self.assertEqual(ds.cluster, "tinybird")
        self.assertEqual(ds.replicated, True)

        response = await self.fetch_async("/v0/datasources/t_from_schema.datasource?token=%s" % token)
        self.assertEqual(response.code, 200)
        self.assertEqual(response.headers["content-type"], "text/plain")
        self.assertEqual(
            response.body.decode(),
            """
SCHEMA >
    `VendorID` Int32,
    `tpep_pickup_datetime` DateTime

ENGINE "MergeTree"
ENGINE_PARTITION_KEY "toYear(tpep_pickup_datetime)"
ENGINE_SORTING_KEY "tpep_pickup_datetime, VendorID"
""",
        )

    @tornado.testing.gen_test
    async def test_create_with_invalid_schema(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
            "name": "t_from_schema",
            "schema": "INVALID SCHEMA",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 400)
        result = json.loads(response.body)
        self.assertEqual(result["error"], "Unknown data type family: SCHEMA")

    @tornado.testing.gen_test
    async def test_create_with_engine(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
            "name": "t_w_engine",
            "schema": self.SCHEMA,
            "engine": self.ENGINE,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        result = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(result["datasource"]["name"], "t_w_engine")

    @tornado.testing.gen_test
    async def test_create_with_invalid_engine(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
            "name": "foo",
            "schema": self.SCHEMA,
            "engine": "INVALID_ENGINE",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        result = json.loads(response.body)
        self.assertEqual(response.code, 400)
        self.assertEqual(
            result["error"],
            "Engine INVALID_ENGINE is not supported, supported engines include: MergeTree, ReplacingMergeTree, SummingMergeTree, AggregatingMergeTree, CollapsingMergeTree, VersionedCollapsingMergeTree, Join, Null",
        )

    @tornado.testing.gen_test
    async def test_create_with_wrong_engine_key(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
            "name": "foo",
            "schema": "VendorID Int32, test Int32",
            "engine": "replacingmergetree",
            "engine_sorting_key": "VendorID",
            "engine_wrong_key": "test",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        result = json.loads(response.body)
        self.assertEqual(response.code, 400)
        self.assertEqual(result["error"], "Invalid data source structure: engine_wrong_key is not a valid option")

    @tornado.testing.gen_test
    async def test_create_with_forbidden_name(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
            "name": "from",
            "schema": "VendorID Int32, test Int32",
            "engine": "replacingmergetree",
            "engine_sorting_key": "VendorID",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        result = json.loads(response.body)
        self.assertEqual(response.code, 400)
        self.assertTrue("Forbidden Data Source name" in result["error"])

    @tornado.testing.gen_test
    async def test_create_with_invalid_aggregating_function(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
            "name": "foo_agg_function",
            "schema": """
                start_of_month Date,
                year UInt16,
                month UInt8,
                country String,
                sum_units AggregateFunction(sum, Int32)
            """,
            "engine": "MergeTree",
            "engine_partition_key": "toYYYYMM(start_of_month)",
            "engine_sorting_key": "year, start_of_month, month, country",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        result = json.loads(response.body)
        self.assertEqual(response.code, 400)

        self.assertEqual(
            result["error"],
            "Invalid data source structure: MergeTree() PARTITION BY (toYYYYMM(start_of_month)) ORDER BY (year, start_of_month, month, country) might not support Aggregate Functions.",
        )

    @tornado.testing.gen_test
    async def test_create_with_boolean_type_in_schema_with_jsonpaths(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
            "name": "foo_agg_function",
            "schema": """
                start_of_month Date `json:$.start_of_month`,
                year UInt16 `json:$.year`,
                month UInt8 `json:$.month`,
                country String `json:$.country`,
                some_boolean Boolean `json:$.some_boolean`
            """,
            "format": "ndjson",
            "engine": "MergeTree",
            "engine_partition_key": "toYYYYMM(start_of_month)",
            "engine_sorting_key": "year, start_of_month, month, country",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

    @tornado.testing.gen_test
    async def test_create_with_unsupported_type_in_schema_with_jsonpaths(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
            "name": "foo_agg_function",
            "schema": """
                start_of_month Date `json:$.start_of_month`,
                year UInt16 `json:$.year`,
                month UInt8 `json:$.month`,
                country String `json:$.country`,
                some_geom Point `json:$.some_geom`
            """,
            "format": "ndjson",
            "engine": "MergeTree",
            "engine_partition_key": "toYYYYMM(start_of_month)",
            "engine_sorting_key": "year, start_of_month, month, country",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        result = json.loads(response.body)
        self.assertEqual(response.code, 400)

        self.assertEqual(
            result["error"],
            "Unsupported type: Point",
        )

    @tornado.testing.gen_test
    async def test_create_aggregating_function_summing_merge_tree(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
            "name": "foo_agg_function_summing",
            "schema": """
                start_of_month Date,
                year UInt16,
                month UInt8,
                country String,
                sum_units AggregateFunction(sum, Int32)
            """,
            "engine": "SummingMergeTree",
            "engine_partition_key": "toYYYYMM(start_of_month)",
            "engine_sorting_key": "year, start_of_month, month, country",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        self.expect_ops_log(
            {"event_type": "create", "datasource_name": "foo_agg_function_summing", "options": {"source": "schema"}},
        )

    @tornado.testing.gen_test
    async def test_create_replacingmergetree_empty_sorting_key(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {"token": token, "name": "foo", "schema": "VendorID Int32, test Int32", "engine": "replacingmergetree"}
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        result = json.loads(response.body)
        assert response.code == 200, result
        assert result == {
            "datasource": {
                "id": mock.ANY,
                "name": "foo",
                "cluster": "tinybird",
                "tags": {},
                "created_at": mock.ANY,
                "updated_at": mock.ANY,
                "replicated": True,
                "version": 0,
                "project": None,
                "errors_discarded_at": None,
                "headers": {},
                "shared_with": [],
                "description": "",
                "engine": {"engine": "ReplacingMergeTree", "sorting_key": "VendorID, test"},
                "last_commit": {"content_sha": "", "status": "ok", "path": ""},
                "used_by": [],
                "type": "csv",
            }
        }

    @tornado.testing.gen_test
    async def test_create_replacingmergetree_invalid_sorting_key(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
            "name": "foo",
            "schema": "VendorID Int32, test Int32",
            "engine": "replacingmergetree",
            "engine_sorting_key": "tuple()",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        result = json.loads(response.body)
        self.assertEqual(response.code, 400)
        self.assertEqual(
            result["error"],
            "Invalid data source structure: Invalid value 'tuple()' for option 'engine_sorting_key', reason: 'tuple()' is not a valid sorting key",
        )

    @tornado.testing.gen_test
    async def test_create_from_schema_with_join_table_MATERIALIZED(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        legacy_engine_full_params = {
            "token": token,
            "name": "test_join_legacy",
            "schema": "VendorID Int32, test Int32",
            "engine": "Join",
            "engine_join_strictness": "ANY",
            "engine_join_type": "LEFT",
            "engine_key_columns": "VendorID",
        }
        engine_params = {
            "token": token,
            "name": "test_join",
            "schema": "VendorID Int32, test Int32",
            "engine": "join",
            "engine_join_strictness": "ANY",
            "engine_join_type": "LEFT",
            "engine_key_columns": "VendorID",
        }
        for params in [legacy_engine_full_params, engine_params]:
            with self.subTest(params=params):
                create_url = f"/v0/datasources?{urlencode(params)}"
                response = await self.fetch_async(create_url, method="POST", body="")
                self.assertEqual(response.code, 200, response.body)
                self.expect_ops_log(
                    {"event_type": "create", "datasource_name": params["name"], "options": {"source": "schema"}},
                )

                name = f"t_from_schema_with_{params['name']}"
                params = {
                    "token": token,
                    "name": name,
                    "schema": f"VendorID Int32, tpep_pickup_datetime DateTime, test String MATERIALIZED joinGet('{params['name']}', 'test', VendorID)",
                }
                create_url = f"/v0/datasources?{urlencode(params)}"
                response = await self.fetch_async(create_url, method="POST", body="")
                result = json.loads(response.body)
                self.assertEqual(response.code, 200, response.body)
                self.assertEqual(result["datasource"]["name"], name)
                self.expect_ops_log(
                    {"event_type": "create", "datasource_name": name, "options": {"source": "schema"}},
                )

    @tornado.testing.gen_test
    async def test_create_from_schema_with_join_table_DEFAULT(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        legacy_engine_full_params = {
            "token": token,
            "name": "test_join_legacy",
            "schema": "VendorID Int32, test Int32",
            "engine": "Join",
            "engine_join_strictness": "ANY",
            "engine_join_type": "LEFT",
            "engine_key_columns": "VendorID",
        }
        engine_params = {
            "token": token,
            "name": "test_join",
            "schema": "VendorID Int32, test Int32",
            "engine": "join",
            "engine_join_strictness": "ANY",
            "engine_join_type": "LEFT",
            "engine_key_columns": "VendorID",
        }
        for params in [legacy_engine_full_params, engine_params]:
            with self.subTest(params=params):
                create_url = f"/v0/datasources?{urlencode(params)}"
                response = await self.fetch_async(create_url, method="POST", body="")
                self.assertEqual(response.code, 200, response.body)
                self.expect_ops_log(
                    {"event_type": "create", "datasource_name": params["name"], "options": {"source": "schema"}},
                )

                name = f"t_from_schema_with_{params['name']}"
                params = {
                    "token": token,
                    "name": name,
                    "schema": f"VendorID Int32, tpep_pickup_datetime DateTime, test String DEFAULT joinGet('{params['name']}', 'test', VendorID)",
                }
                create_url = f"/v0/datasources?{urlencode(params)}"
                response = await self.fetch_async(create_url, method="POST", body="")
                result = json.loads(response.body)
                self.assertEqual(response.code, 200, response.body)
                self.assertEqual(result["datasource"]["name"], name)
                self.expect_ops_log(
                    {"event_type": "create", "datasource_name": name, "options": {"source": "schema"}},
                )

    @tornado.testing.gen_test
    async def test_create_from_schema_with_join_table_ALIAS(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        legacy_engine_full_params = {
            "token": token,
            "name": "test_join_legacy",
            "schema": "VendorID Int32, test Int32",
            "engine": "Join",
            "engine_join_strictness": "ANY",
            "engine_join_type": "LEFT",
            "engine_key_columns": "VendorID",
        }
        engine_params = {
            "token": token,
            "name": "test_join",
            "schema": "VendorID Int32, test Int32",
            "engine": "join",
            "engine_join_strictness": "ANY",
            "engine_join_type": "LEFT",
            "engine_key_columns": "VendorID",
        }
        for params in [legacy_engine_full_params, engine_params]:
            with self.subTest(params=params):
                create_url = f"/v0/datasources?{urlencode(params)}"
                response = await self.fetch_async(create_url, method="POST", body="")
                self.assertEqual(response.code, 200, response.body)
                self.expect_ops_log(
                    {"event_type": "create", "datasource_name": params["name"], "options": {"source": "schema"}},
                )

                name = f"t_from_schema_with_{params['name']}"
                params = {
                    "token": token,
                    "name": name,
                    "schema": f"VendorID Int32, tpep_pickup_datetime DateTime, test String ALIAS joinGet('{params['name']}', 'test', VendorID)",
                }
                create_url = f"/v0/datasources?{urlencode(params)}"
                response = await self.fetch_async(create_url, method="POST", body="")
                self.assertEqual(response.code, 400, response.body)
                result = json.loads(response.body)
                self.assertRegex(result["error"], "ALIAS not supported.*")

    @tornado.testing.gen_test
    async def test_create_from_schema_with_mergetree_table(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        legacy_engine_full_params = {
            "token": token,
            "name": "test_mergetree",
            "schema": "date DateTime, VendorID Int32, test Int32",
            "engine": "MergeTree",
            "engine_partition_key": "date",
            "engine_sorting_key": "date, test",
            "engine_ttl": "toDate(date) + INTERVAL 1 DAY",
            "engine_settings": "index_granularity=32",
        }
        engine_params = {
            "token": token,
            "name": "test_join",
            "schema": "date DateTime, VendorID Int32, test Int32",
            "engine": "MergeTree",
            "engine_partition_key": "date",
            "engine_sorting_key": "date, test",
            "engine_settings": "index_granularity=32",
            "engine_ttl": "toDate(date) + interval 1 day",
        }
        for params in [legacy_engine_full_params, engine_params]:
            with self.subTest(params=params):
                create_url = f"/v0/datasources?{urlencode(params)}"
                response = await self.fetch_async(create_url, method="POST", body="")
                self.assertEqual(response.code, 200, response.body)
                self.expect_ops_log(
                    {"event_type": "create", "datasource_name": params["name"], "options": {"source": "schema"}},
                )

        response = await self.fetch_async("/v0/datasources/test_mergetree.datasource?token=%s" % token)
        self.assertEqual(response.code, 200)
        self.assertEqual(response.headers["content-type"], "text/plain")
        self.assertEqual(
            response.body.decode(),
            """
SCHEMA >
    `date` DateTime,
    `VendorID` Int32,
    `test` Int32

ENGINE "MergeTree"
ENGINE_PARTITION_KEY "date"
ENGINE_SORTING_KEY "date, test"
ENGINE_SETTINGS "index_granularity = 32"
ENGINE_TTL "toDate(date) + toIntervalDay(1)"
""",
        )

    @tornado.testing.gen_test
    async def test_create_schema_with_blocked_settings_should_fail(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        engine_params = {
            "token": token,
            "name": "test_blocked_setting",
            "schema": "test Int64",
            "engine": "MergeTree",
            "engine_sorting_key": "test",
            "engine_settings": "index_granularity=1",
        }

        create_url = f"/v0/datasources?{urlencode(engine_params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 400, response.body)
        self.expect_ops_log(
            {
                "event_type": "create",
                "datasource_name": engine_params["name"],
                "result": "error",
                "error": "Invalid data source structure: The value for 'index_granularity' is too small (1 < 32). Contact support@tinybird.co if you require access to this feature",
                "options": {"source": "schema"},
            },
        )

    @tornado.testing.gen_test
    async def test_get_datasource_with_internal_settings_should_not_show_them(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        # Force the user to use a different storage policy
        u.storage_policies = {OTHER_STORAGE_POLICY: 0}
        u.feature_flags[FeatureFlagWorkspaces.ENABLE_STORAGE_POLICY.value] = True

        token = Users.get_token_for_scope(u, scopes.ADMIN)
        engine_params = {
            "token": token,
            "name": "test_show_setting",
            "schema": "test Int64",
            "engine": "MergeTree",
            "engine_sorting_key": "test",
            "engine_settings": "min_rows_for_wide_part=1000",
        }

        create_url = f"/v0/datasources?{urlencode(engine_params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        result = json.loads(response.body)
        datasource = result["datasource"]

        cli = HTTPClient(host=u.database_server, database=u.database)
        _, result = cli.query_sync(
            f"SELECT engine_full FROM system.tables where database = '{u.database}' and name = '{datasource['id']}' FORMAT CSV",
            read_only=False,
        )
        self.assertTrue("storage_policy" in str(result), str(result))

        response = await self.fetch_async("/v0/datasources/test_show_setting.datasource?token=%s" % token)
        self.assertEqual(response.code, 200)
        self.assertEqual(response.headers["content-type"], "text/plain")
        self.assertEqual(
            response.body.decode(),
            """
SCHEMA >
    `test` Int64

ENGINE "MergeTree"
ENGINE_SORTING_KEY "test"
ENGINE_SETTINGS "min_rows_for_wide_part = 1000, index_granularity = 8192"
""",
        )

    @tornado.testing.gen_test
    async def test_create_from_schema_with_engine_body_params(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        name = "test_join_body"
        schema = "`VendorID` Int32, `test` Int32"
        params = {
            "token": token,
            "name": name,
            "engine": "join",
            "engine_join_strictness": "ANY",
            "engine_key_columns": "VendorID",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body=f"schema={schema}&engine_join_type=LEFT")
        self.assertEqual(response.code, 200, response.body)
        self.expect_ops_log(
            {"event_type": "create", "datasource_name": name, "options": {"source": "schema"}},
        )
        params = {
            "token": token,
        }
        response = await self.fetch_async(f"/v0/datasources/{name}?{urlencode(params)}")
        self.assertEqual(response.code, 200, response.body)
        ds = json.loads(response.body)
        self.assertEqual(ds["name"], name)
        self.assertEqual(ds["engine"]["engine_full"], "Join(ANY, LEFT, VendorID)")
        self.assertEqual(ds["schema"]["sql_schema"], schema)

    def test_create_with_engine_null(self):
        pass

    @tornado.testing.gen_test
    async def test_columns_with_dots(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        ds_name = "ds_column_with_dot"
        params = {
            "token": token,
            "name": ds_name,
            "schema": """
                d Date,
                event_type String,
                `foo.bar` Int32
            """,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        params = {"token": token, "q": f"SELECT * FROM {ds_name} FORMAT JSON"}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        dot_column = next((c for c in result["meta"] if c["name"] == "foo.bar"), None)
        self.assertIsNotNone(dot_column)
        self.assertEqual(dot_column["type"], "Int32")

    @tornado.testing.gen_test
    async def test_columns_with_dots_no_backquote(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        ds_name = "ds_column_with_dot"
        params = {
            "token": token,
            "name": ds_name,
            "schema": """
                d Date,
                event_type String,
                foo.bar Int32
            """,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        params = {"token": token, "q": f"SELECT * FROM {ds_name} FORMAT JSON"}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        dot_column = next((c for c in result["meta"] if c["name"] == "foo.bar"), None)
        self.assertIsNotNone(dot_column)
        self.assertEqual(dot_column["type"], "Int32")

    @tornado.testing.gen_test
    async def test_failed_creation_no_ds_behind(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        ds_name = "ds_invalid_schema"
        params = {
            "token": token,
            "name": ds_name,
            "schema": """
                d Date,
                -invalid_here Int32
            """,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 400, response.body)
        result = json.loads(response.body)
        expected_error = "Invalid data source structure: Column '-invalid_here' should have an alias and start by a character. Change the query and try it again."
        self.assertEquals(result["error"], expected_error)
        self.expect_ops_log(
            {
                "event_type": "create",
                "datasource_name": "ds_invalid_schema",
                "result": "error",
                "error": expected_error,
                "options": {"source": "schema"},
            },
        )
        ds_url = f"/v0/datasources/{ds_name}?token={token}"
        response = await self.fetch_async(ds_url)
        self.assertEqual(response.code, 404, response.body)


class TestAPIDatasourceSchemaAppend(TestAPIDatasourceBase):
    def setUp(self):
        super().setUp()
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        self.datasource_name = "test_schema_and_append"
        schema = "checkout Date, numnights Int8, checkin Date, reservationid String, unifiedid String, reservationdate Date, totalnightlyprice Float32, currency String"
        params = {"token": token, "name": self.datasource_name, "engine": "MergeTree"}
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body=f"schema={schema}")
        self.assertEqual(response.code, 200, response.body)
        self.expect_ops_log(
            {"event_type": "create", "datasource_name": self.datasource_name, "options": {"source": "schema"}},
        )

    @tornado.testing.gen_test
    async def test_append_full_body(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
            "name": self.datasource_name,
            "mode": "append",
        }
        append_url = f"/v0/datasources?{urlencode(params)}"

        with fixture_file("trans.csv", mode="rb") as fd:
            response = await self.fetch_full_body_upload_async(append_url, fd)
            self.expect_ops_log(
                {"event_type": "append", "datasource_name": self.datasource_name, "options": {"source": "full_body"}},
            )
            self.assertEqual(response.code, 200, response.body)
            self.assertEqual(json.loads(response.body)["error"], False)

    @tornado.testing.gen_test
    async def test_append_stream(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
            "name": self.datasource_name,
            "mode": "append",
        }
        append_url = f"/v0/datasources?{urlencode(params)}"

        url = self.get_url(append_url)
        # Use requests to emulate curl content-length in multipart requests
        post = sync_to_async(requests.post, thread_sensitive=False)
        r = await post(url, files=dict(csv=fixture_data("trans.csv", mode="rb")))
        self.expect_ops_log(
            {"event_type": "append", "datasource_name": self.datasource_name, "options": {"source": "stream"}},
        )
        self.assertEqual(r.status_code, 200, r.content)
        self.assertEqual(r.json()["error"], False)


class TestAPIDatasourceSchemaAppendWithError(TestAPIDatasourceBase):
    def setUp(self):
        super().setUp()
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        self.datasource_name = "test_schema_and_append_error"
        schema = "id Int16, date DateTime, event String, created_at String, updated_at DateTime, user_id String"
        params = {"token": token, "name": self.datasource_name}
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = self.fetch(create_url, method="POST", body=f"schema={schema}")
        self.assertEqual(response.code, 200, response.body)
        self.expect_ops_log(
            {"event_type": "create", "datasource_name": self.datasource_name, "options": {"source": "schema"}},
        )

    @tornado.testing.gen_test
    async def test_append_log_error(self):
        self.maxDiff = None
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
            "name": self.datasource_name,
            "mode": "append",
        }
        append_url = f"/v0/datasources?{urlencode(params)}"

        url = self.get_url(append_url)
        # Use requests to emulate curl content-length in multipart requests
        post = sync_to_async(requests.post, thread_sensitive=False)
        r = await post(url, files=dict(csv=fixture_data("parsing_error.csv", mode="rb")))
        ds_ops_log_expected_error = (
            "There was an error when attempting to import your data. failed to normalize the CSV chunk: "
            "[Error] Cannot read DateTime: unexpected number of decimal digits for time zone offset: 6: while executing "
            "'FUNCTION parseDateTimeBestEffort(toString(__table1.updated_at) :: 2) -> parseDateTimeBestEffort(toString(__table1.updated_at)) DateTime : 6'. (CANNOT_PARSE_DATETIME)"
        )
        api_expected_error = (
            "There was an error when attempting to import your data. Check 'errors' for more information."
        )
        self.expect_ops_log(
            {
                "event_type": "append",
                "datasource_name": self.datasource_name,
                "result": "error",
                "error": ds_ops_log_expected_error,
                "options": {"source": "stream"},
            },
        )
        self.assertEqual(r.status_code, 400, r.content)
        resp = r.json()
        self.assertEqual(resp["error"], api_expected_error)
        self.assertRegex(
            resp["errors"][0],
            r"failed to normalize the CSV chunk: \[Error\] Cannot read DateTime: unexpected number of decimal digits for time zone offset: 6.*",
        )


class TestAPIDatasourceHooksLastDate(TestAPIDatasourceBase):
    async def create_datasource_async(self, name, schema, with_last_date=False):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
            "mode": "create",
            "name": name,
            "with_last_date": "true" if with_last_date else "false",
            "schema": schema,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, json.loads(response.body))
        return json.loads(response.body)["datasource"]

    @tornado.testing.gen_test
    async def test_create_last_update(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        datasources_to_test = [
            ("sales", "sales_last_date", None),
            ("sales", "sales_last_date", "sales_landing"),
            ("sales__dev", "sales_last_date__dev", None),
            ("sales__dev", "sales_last_date__dev", "sales_landing__dev"),
            ("sales__v0", "sales_last_date__v0", None),
            ("sales__v0", "sales_last_date__v0", "sales_landing__v0"),
            ("sales__v1", "sales_last_date__dev", "sales_landing__v1"),
            ("sales__dev", "sales_last_date__dev", "sales_landing__v1"),
        ]

        for data_ds_name, last_date_ds_name, landing_ds_name in datasources_to_test:
            with self.subTest(data_ds_name=data_ds_name, last_date_ds_name=last_date_ds_name):
                ds = await self.create_datasource_async(data_ds_name, "date Date, a Int32", with_last_date=True)
                last_date_ds = await self.create_datasource_async(
                    last_date_ds_name, "last_date Date, insert_datetime DateTime"
                )

                if landing_ds_name:
                    ds = await self.create_datasource_async(landing_ds_name, "date Date, a Int32", with_last_date=True)

                params = {"token": token, "name": ds["name"], "mode": "append"}
                create_url = self.get_url(f"/v0/datasources?{urlencode(params)}")
                s = StringIO("2019-01-02,2\n2018-01-02,2")
                response = await self.fetch_full_body_upload_async(create_url, s)
                self.assertEqual(response.code, 200)

                a = exec_sql(
                    u["database"],
                    f"SELECT   insert_datetime > (now() - INTERVAL 5 MINUTE) as insert_ok,"
                    f"         toDate(last_date) = toDate('2019-01-02') as date_ok,"
                    f"         *"
                    f"FROM {last_date_ds['id']} FORMAT JSON",
                )
                self.assertEqual(len(a["data"]), 1)
                self.assertEqual(a["data"][0]["insert_ok"], True, a)

                # This currently does not work as the date inserted is the one from the source table (which is empty)
                # not from the landing (which would be '2019-01-02')
                if not landing_ds_name:
                    self.assertEqual(a["data"][0]["date_ok"], True, a)

                await Users.drop_datasource_async(u, data_ds_name)
                await Users.drop_datasource_async(u, last_date_ds_name)
                if landing_ds_name:
                    await Users.drop_datasource_async(u, landing_ds_name)

    @tornado.testing.gen_test
    async def test_does_not_fail_on_missing_last_date_ds(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        ds = await self.create_datasource_async("sales_to_delete", "date Date, a Int32", with_last_date=True)
        params = {"token": token, "name": ds["name"], "mode": "append"}
        create_url = self.get_url(f"/v0/datasources?{urlencode(params)}")
        s = StringIO("2019-01-02,2\n2018-01-02,2")
        response = await self.fetch_full_body_upload_async(create_url, s)
        self.assertEqual(response.code, 200)


class TestAPIDatasourceHooksReplacePartialBase(TestAPIDatasourceBase):
    initial_data_query = """
        SELECT
            (toDate('2019-01-30') + dc.d) + toIntervalHour(h.number) AS dt,
            dc.country,
            1 AS units
        FROM
        (
            SELECT * FROM
            (
                SELECT number AS d
                FROM system.numbers
                LIMIT 4
            )
            CROSS JOIN
            (
                SELECT if(number = 1, 'ES', 'US') as country
                FROM system.numbers
                LIMIT 2
            )
        ) AS dc
        CROSS JOIN
        (
            SELECT number
            FROM system.numbers
            LIMIT 24
        ) AS h
        FORMAT CSVWithNames
    """

    replace_data_query = """
        SELECT
            (toDate('2019-01-31') + dc.d) + toIntervalHour(h.number) AS dt,
            dc.country,
            2 AS units -- changing units
        FROM
        (
            SELECT * FROM
            (
                SELECT number AS d
                FROM system.numbers
                LIMIT 2
            )
            CROSS JOIN
            (
                SELECT if(number = 1, 'ES', 'PT') as country
                FROM system.numbers
                LIMIT 2
            )
        ) AS dc
        CROSS JOIN
        (
            SELECT number
            FROM system.numbers
            LIMIT 24
        ) AS h
        FORMAT CSVWithNames
    """

    def setUp(self):
        super().setUp()
        u = Users.get_by_id(self.WORKSPACE_ID)
        self.u = Users.get_by_id(self.WORKSPACE_ID)
        self.token = Users.get_token_for_scope(u, scopes.ADMIN)


class TestAPIDatasourceHooksReplacePartialBatch(TestAPIDatasourceHooksReplacePartialBase):
    @tornado.testing.gen_test
    async def test_replace_partial_happy_case(self):
        rand = str(uuid.uuid4())[:8]
        landing_name = f"sales_landing_{rand}"
        await self.create_datasource_async(
            self.token,
            landing_name,
            """
            dt DateTime,
            country String,
            units Int32
        """,
            {"engine": "MergeTree", "engine_partition_key": "toYYYYMM(dt)", "engine_sorting_key": "country, dt"},
        )

        # Create a couple of dependent data sources
        daily_ds_name = f"sales_daily_{rand}"
        await self.create_datasource_async(
            self.token,
            daily_ds_name,
            """
            d Date,
            country String,
            sum_units AggregateFunction(sum, Int32)
        """,
            {
                "engine": "AggregatingMergeTree",
                "engine_partition_key": "toYYYYMM(d)",
                "engine_sorting_key": "d, country",
            },
        )

        monthly_ds_name = f"sales_monthly_{rand}"
        await self.create_datasource_async(
            self.token,
            monthly_ds_name,
            """
            start_of_month Date,
            year UInt16,
            month UInt8,
            country String,
            sum_units AggregateFunction(sum, Int32)
        """,
            {
                "engine": "AggregatingMergeTree",
                "engine_partition_key": "toYYYYMM(start_of_month)",
                "engine_sorting_key": "year, start_of_month, month, country",
            },
        )

        # Create the views to connect them
        await self.create_view_async(
            self.u,
            self.token,
            daily_ds_name,
            f"""
        SELECT
            toDate(dt) AS d,
            country,
            sumState(units) AS sum_units
        FROM {landing_name}
        GROUP BY d, country
        """,
        )

        await self.create_view_async(
            self.u,
            self.token,
            monthly_ds_name,
            f"""
        SELECT
            toStartOfMonth(dt) as start_of_month,
            toYear(dt) as year,
            toMonth(dt) as month,
            country,
            sumState(units) as sum_units
        FROM
            {landing_name}
        GROUP BY start_of_month, year, month, country
        """,
        )

        # Insert new data
        csv_url = self.get_url_for_sql(self.initial_data_query)
        params = {
            "token": self.token,
            "name": landing_name,
            "mode": "append",
            "url": csv_url,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done")
        self.expect_ops_log(
            [
                {"event_type": "append", "datasource_name": landing_name, "options": {"source": csv_url}},
                {"event_type": "append", "datasource_name": daily_ds_name},
                {"event_type": "append", "datasource_name": monthly_ds_name},
            ]
        )

        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": daily_ds_name,
                "options": {
                    "replace_condition": "toDate(dt) == '2019-01-31'",
                },
            }
        )

        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": monthly_ds_name,
                "options": {
                    "replace_condition": "toDate(dt) == '2019-01-31'",
                },
            }
        )

        await self.assert_stats_async(landing_name, self.token, 192, 902)

        days = hours = countries = sales = lambda x: x

        async def get_views_results():
            daily_results = await self._query(
                query=f"SELECT d, sumMerge(sum_units) as sum_units FROM {daily_ds_name} FINAL GROUP BY d ORDER BY d ASC FORMAT JSON"
            )
            monthly_results = await self._query(
                query=f"SELECT year, month, sumMerge(sum_units) as sum_units FROM {monthly_ds_name} FINAL GROUP BY year, month ORDER BY year ASC, month ASC FORMAT JSON"
            )
            daily_results_from_landing = await self._query(
                query=f"""
            SELECT
                toDate(dt) AS d,
                sum(units) AS sum_units
            FROM {landing_name}
            GROUP BY d
            ORDER BY d ASC
            FORMAT JSON
            """
            )
            monthly_results_from_landing = await self._query(
                query=f"""
            SELECT
                toYear(dt) as year,
                toMonth(dt) as month,
                sum(units) as sum_units
            FROM
                {landing_name}
            GROUP BY year, month
            ORDER BY year ASC, month ASC
            FORMAT JSON
            """
            )
            self.assertEqual(daily_results_from_landing["data"], daily_results["data"])
            self.assertEqual(monthly_results_from_landing["data"], monthly_results["data"])
            return daily_results, monthly_results

        async def assert_views_results():
            # Validate current data
            daily_results, monthly_results = await get_views_results()
            self.assertEqual(len(daily_results["data"]), 4)
            daily_sales = days(1) * hours(24) * countries(2) * sales(1)
            self.assertEqual(list(daily_results["data"][0].values()), ["2019-01-30", daily_sales])
            self.assertEqual(list(daily_results["data"][1].values()), ["2019-01-31", daily_sales])
            self.assertEqual(list(daily_results["data"][2].values()), ["2019-02-01", daily_sales])
            self.assertEqual(list(daily_results["data"][3].values()), ["2019-02-02", daily_sales])
            self.assertEqual(len(monthly_results["data"]), 2)
            montly_sales = days(2) * daily_sales
            self.assertEqual(list(monthly_results["data"][0].values()), [2019, 1, montly_sales])
            self.assertEqual(list(monthly_results["data"][1].values()), [2019, 2, montly_sales])

        await poll_async(assert_views_results)

        # Replace just part of the data
        csv_url = self.get_url_for_sql(self.replace_data_query)
        params = {
            "token": self.token,
            "mode": "replace",
            "replace_condition": "toDate(dt) == '2019-01-31'",
            "name": landing_name,
            "url": csv_url,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done", str(job))
        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": landing_name,
                "options": {
                    "source": csv_url,
                    "replace_condition": "toDate(dt) == '2019-01-31'",
                },
            }
        )
        await self.assert_stats_async(landing_name, self.token, 192, 902)

        # Validate data after replacing just one day
        async def validate_replaced():
            daily_results, monthly_results = await get_views_results()
            self.assertEqual(len(daily_results["data"]), 4)
            daily_sales = days(1) * hours(24) * countries(2) * sales(1)
            self.assertEqual(list(daily_results["data"][0].values()), ["2019-01-30", daily_sales])
            self.assertEqual(list(daily_results["data"][1].values()), ["2019-01-31", sales(2) * daily_sales])
            self.assertEqual(list(daily_results["data"][2].values()), ["2019-02-01", daily_sales])
            self.assertEqual(list(daily_results["data"][3].values()), ["2019-02-02", daily_sales])
            self.assertEqual(len(monthly_results["data"]), 2)
            january_sales = (days(1) * daily_sales) + (days(1) * sales(2) * daily_sales)
            februay_sales = days(2) * daily_sales
            self.assertEqual(list(monthly_results["data"][0].values()), [2019, 1, january_sales])
            self.assertEqual(list(monthly_results["data"][1].values()), [2019, 2, februay_sales])

        await poll_async(validate_replaced)

        quarantine_result = await self._query(query=f"SELECT count() c FROM {landing_name}_quarantine FORMAT JSON")
        self.assertEqual(quarantine_result["data"][0]["c"], 0)

        # Replace just part of the data with quarantine
        # units is a string instead of a number
        replace_data_quarantine_query = """
            SELECT
                (toDate('2019-01-31') + dc.d) + toIntervalHour(h.number) AS dt,
                dc.country,
                'a' AS units -- changing type
            FROM
            (
                SELECT * FROM
                (
                    SELECT number AS d
                    FROM system.numbers
                    LIMIT 1
                )
                CROSS JOIN
                (
                    SELECT if(number = 1, 'ES', 'US') as country
                    FROM system.numbers
                    LIMIT 2
                )
            ) AS dc
            CROSS JOIN
            (
                SELECT number
                FROM system.numbers
                LIMIT 24
            ) AS h
            FORMAT CSVWithNames
        """
        csv_url = self.get_url_for_sql(replace_data_quarantine_query)
        params = {
            "token": self.token,
            "mode": "replace",
            "replace_condition": "toDate(dt) == '2019-01-31'",
            "name": landing_name,
            "url": csv_url,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done", str(job))
        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": landing_name,
                "options": {
                    "source": csv_url,
                    "replace_condition": "toDate(dt) == '2019-01-31'",
                },
            }
        )

        await poll_async(validate_replaced)
        quarantine_result = await self._query(query=f"SELECT count() c FROM {landing_name}_quarantine FORMAT JSON")
        daily_sales = days(1) * hours(24) * countries(2) * sales(1)
        self.assertEqual(quarantine_result["data"][0]["c"], daily_sales)

    @tornado.testing.gen_test
    async def test_replace_partial_shared_datasource_happy_case(self):
        workspace_a = Users.get_by_id(self.WORKSPACE_ID)
        user_a = UserAccount.get_by_id(self.USER_ID)
        token_workspace_a = Users.get_token_for_scope(workspace_a, scopes.ADMIN)
        token_user_a = UserAccount.get_token_for_scope(user_a, scopes.AUTH)

        user_b_name = f"user_b_{uuid.uuid4().hex}"
        workspace_b = await self.tb_api_proxy_async.register_user_and_workspace(
            f"{user_b_name}@example.com", user_b_name
        )
        user_b = UserAccount.get_by_email(f"{user_b_name}@example.com")
        token_workspace_b = Users.get_token_for_scope(workspace_b, scopes.ADMIN)
        token_user_b = UserAccount.get_token_for_scope(user_b, scopes.AUTH)

        self.workspaces_to_delete.append(workspace_b)
        self.users_to_delete.append(UserAccount.get_by_email(f"{user_b_name}@example.com"))

        # Create a couple of dependent data sources
        daily_ds_name = "sales_daily_b"
        monthly_ds_name = "sales_monthly_b"
        # Create a dependent non-MergeTree data source
        join_ds_name = "tt_join_b"

        await asyncio.gather(
            *[
                self.create_datasource_async(
                    token_workspace_b,
                    daily_ds_name,
                    """
                d Date,
                country String,
                sum_units AggregateFunction(sum, Int32)
            """,
                    {
                        "engine": "AggregatingMergeTree",
                        "engine_partition_key": "toYYYYMM(d)",
                        "engine_sorting_key": "d, country",
                    },
                ),
                self.create_datasource_async(
                    token_workspace_b,
                    monthly_ds_name,
                    """
                start_of_month Date,
                year UInt16,
                month UInt8,
                country String,
                sum_units AggregateFunction(sum, Int32)
            """,
                    {
                        "engine": "AggregatingMergeTree",
                        "engine_partition_key": "toYYYYMM(start_of_month)",
                        "engine_sorting_key": "year, start_of_month, month, country",
                    },
                ),
                self.create_datasource_async(
                    token_workspace_b,
                    join_ds_name,
                    """
                country String
            """,
                    {
                        "engine": "Join",
                        "engine_join_strictness": "ANY",
                        "engine_join_type": "LEFT",
                        "engine_key_columns": "country",
                    },
                ),
            ]
        )

        self.ops_log_expectations = {self.WORKSPACE_ID: []}

        landing_name = "sales_landing_a_shared"
        datasource_a_in_workspace_a = await self.tb_api_proxy_async.create_datasource(
            token_workspace_a,
            landing_name,
            """
                dt DateTime,
                country String,
                units Int32
            """,
            engine_params={
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(dt)",
                "engine_sorting_key": "country, dt",
            },
        )
        self.expect_ops_log({"event_type": "create", "datasource_name": landing_name, "options": {"source": "schema"}})

        await self.tb_api_proxy_async.invite_user_to_workspace(
            token=token_user_b, workspace_id=workspace_b.id, user_to_invite_email=user_a.email
        )

        datasource_a_in_workspace_b = await self.tb_api_proxy_async.share_datasource_with_another_workspace(
            token=token_user_a,
            datasource_id=datasource_a_in_workspace_a["datasource"]["id"],
            origin_workspace_id=workspace_a.id,
            destination_workspace_id=workspace_b.id,
        )

        # Create the views to connect them
        await asyncio.gather(
            *[
                self.create_view_async(
                    workspace_b,
                    token_workspace_b,
                    daily_ds_name,
                    f"""
                SELECT
                    toDate(dt) AS d,
                    country,
                    sumState(units) AS sum_units
                FROM {datasource_a_in_workspace_b.name}
                GROUP BY d, country
                """,
                ),
                self.create_view_async(
                    workspace_b,
                    token_workspace_b,
                    monthly_ds_name,
                    f"""
                SELECT
                    toStartOfMonth(dt) as start_of_month,
                    toYear(dt) as year,
                    toMonth(dt) as month,
                    country,
                    sumState(units) as sum_units
                FROM
                    {datasource_a_in_workspace_b.name}
                GROUP BY start_of_month, year, month, country
                """,
                ),
                self.create_view_async(
                    workspace_b,
                    token_workspace_b,
                    join_ds_name,
                    f"""
                SELECT
                    country
                FROM {datasource_a_in_workspace_b.name}
                GROUP BY country
            """,
                ),
            ]
        )

        # Insert new data
        csv_url = self.get_url_for_sql(self.initial_data_query)
        params = {
            "token": token_workspace_a,
            "name": landing_name,
            "mode": "replace",
            "replace_condition": "1=1",
            "url": csv_url,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done")
        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": landing_name,
                "options": {"replace_condition": "1=1", "rows_before_replace": "0"},
            }
        )
        await self.assert_stats_async(landing_name, token_workspace_a, 192, 902)

        async def get_views_results():
            result = await asyncio.gather(
                *[
                    self._query(
                        query=f"""
                    SELECT d, sumMerge(sum_units) as sum_units
                    FROM {daily_ds_name} FINAL
                    GROUP BY d
                    ORDER BY d ASC
                    FORMAT JSON""",
                        token=token_workspace_b,
                    ),
                    self._query(
                        query=f"""
                    SELECT year, month, sumMerge(sum_units) as sum_units
                    FROM {monthly_ds_name} FINAL
                    GROUP BY year, month
                    ORDER BY year ASC, month ASC
                    FORMAT JSON""",
                        token=token_workspace_b,
                    ),
                    self._query(
                        query=f"""
                    SELECT country
                    FROM {join_ds_name}
                    GROUP BY country
                    ORDER BY country ASC
                    FORMAT JSON""",
                        token=token_workspace_b,
                    ),
                    self._query(
                        query=f"""
                    SELECT
                        toDate(dt) AS d,
                        sum(units) AS sum_units
                    FROM {landing_name}
                    GROUP BY d
                    ORDER BY d ASC
                    FORMAT JSON
                    """
                    ),
                    self._query(
                        query=f"""
                    SELECT
                        toYear(dt) as year,
                        toMonth(dt) as month,
                        sum(units) as sum_units
                    FROM
                        {landing_name}
                    GROUP BY year, month
                    ORDER BY year ASC, month ASC
                    FORMAT JSON
                    """
                    ),
                    self._query(
                        query=f"""
                    SELECT
                        country
                    FROM
                        {landing_name}
                    GROUP BY country
                    ORDER BY country ASC
                    FORMAT JSON
                    """
                    ),
                ]
            )

            daily_results = result[0]
            monthly_results = result[1]
            join_results = result[2]
            daily_results_from_landing = result[3]
            monthly_results_from_landing = result[4]
            join_results_from_landing = result[5]
            self.assertEqual(daily_results_from_landing["data"], daily_results["data"])
            self.assertEqual(monthly_results_from_landing["data"], monthly_results["data"])
            self.assertEqual(join_results_from_landing["data"], join_results["data"])
            return daily_results, monthly_results, join_results

        # Validate current data
        days = hours = countries = sales = lambda x: x
        daily_results, monthly_results, join_results = await get_views_results()
        self.assertEqual(len(daily_results["data"]), 4)
        daily_sales = days(1) * hours(24) * countries(2) * sales(1)
        self.assertEqual(list(daily_results["data"][0].values()), ["2019-01-30", daily_sales])
        self.assertEqual(list(daily_results["data"][1].values()), ["2019-01-31", daily_sales])
        self.assertEqual(list(daily_results["data"][2].values()), ["2019-02-01", daily_sales])
        self.assertEqual(list(daily_results["data"][3].values()), ["2019-02-02", daily_sales])
        self.assertEqual(len(monthly_results["data"]), 2)
        montly_sales = days(2) * daily_sales
        self.assertEqual(list(monthly_results["data"][0].values()), [2019, 1, montly_sales])
        self.assertEqual(list(monthly_results["data"][1].values()), [2019, 2, montly_sales])
        self.assertEqual(join_results["data"][0], {"country": "ES"})
        self.assertEqual(join_results["data"][1], {"country": "US"})

        # Replace just part of the data
        csv_url = self.get_url_for_sql(self.replace_data_query)
        params = {
            "token": token_workspace_a,
            "mode": "replace",
            "replace_condition": "toDate(dt) == '2019-01-31'",
            "name": landing_name,
            "url": csv_url,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done", str(job))
        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": landing_name,
                "options": {"replace_condition": "toDate(dt) == '2019-01-31'", "rows_before_replace": "192"},
            }
        )
        await self.assert_stats_async(landing_name, token_workspace_a, 192, 902)

        # Validate data after replacing just one day
        async def validate_replaced():
            daily_results, monthly_results, join_results = await get_views_results()
            self.assertEqual(len(daily_results["data"]), 4)
            daily_sales = days(1) * hours(24) * countries(2) * sales(1)
            self.assertEqual(list(daily_results["data"][0].values()), ["2019-01-30", daily_sales])
            self.assertEqual(list(daily_results["data"][1].values()), ["2019-01-31", sales(2) * daily_sales])
            self.assertEqual(list(daily_results["data"][2].values()), ["2019-02-01", daily_sales])
            self.assertEqual(list(daily_results["data"][3].values()), ["2019-02-02", daily_sales])
            self.assertEqual(len(monthly_results["data"]), 2)
            january_sales = (days(1) * daily_sales) + (days(1) * sales(2) * daily_sales)
            februay_sales = days(2) * daily_sales
            self.assertEqual(list(monthly_results["data"][0].values()), [2019, 1, january_sales])
            self.assertEqual(list(monthly_results["data"][1].values()), [2019, 2, februay_sales])
            self.assertEqual(join_results["data"][0], {"country": "ES"})
            self.assertEqual(join_results["data"][1], {"country": "PT"})

        await validate_replaced()

        quarantine_result = await self._query(query=f"SELECT count() c FROM {landing_name}_quarantine FORMAT JSON")
        self.assertEqual(quarantine_result["data"][0]["c"], 0)

        # Replace just part of the data with quarantine
        # units is a string instead of a number
        replace_data_quarantine_query = """
            SELECT
                (toDate('2019-01-31') + dc.d) + toIntervalHour(h.number) AS dt,
                dc.country,
                'a' AS units -- changing type
            FROM
            (
                SELECT * FROM
                (
                    SELECT number AS d
                    FROM system.numbers
                    LIMIT 1
                )
                CROSS JOIN
                (
                    SELECT if(number = 1, 'ES', 'US') as country
                    FROM system.numbers
                    LIMIT 2
                )
            ) AS dc
            CROSS JOIN
            (
                SELECT number
                FROM system.numbers
                LIMIT 24
            ) AS h
            FORMAT CSVWithNames
        """
        csv_url = self.get_url_for_sql(replace_data_quarantine_query)
        params = {
            "token": token_workspace_a,
            "mode": "replace",
            "replace_condition": "toDate(dt) == '2019-01-31'",
            "name": landing_name,
            "url": csv_url,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done", str(job))
        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": landing_name,
                "options": {"replace_condition": "toDate(dt) == '2019-01-31'", "rows_before_replace": "192"},
            }
        )

        await validate_replaced()
        quarantine_result = await self._query(query=f"SELECT count() c FROM {landing_name}_quarantine FORMAT JSON")
        daily_sales = days(1) * hours(24) * countries(2) * sales(1)
        self.assertEqual(quarantine_result["data"][0]["c"], daily_sales)

    @tornado.testing.gen_test
    async def test_replace_partial_with_new_partition(self):
        landing_name = "sales_landing"
        await self.create_datasource_async(
            self.token,
            landing_name,
            """
            dt DateTime,
            country String,
            units Int32
        """,
            {"engine": "MergeTree", "engine_partition_key": "toYYYYMM(dt)", "engine_sorting_key": "country, dt"},
        )

        monthly_ds_name = "sales_monthly"
        await self.create_datasource_async(
            self.token,
            monthly_ds_name,
            """
            start_of_month Date,
            year UInt16,
            month UInt8,
            country String,
            sum_units AggregateFunction(sum, Int32)
        """,
            {
                "engine": "AggregatingMergeTree",
                "engine_partition_key": "toYYYYMM(start_of_month)",
                "engine_sorting_key": "year, start_of_month, month, country",
            },
        )

        await self.create_view_async(
            self.u,
            self.token,
            monthly_ds_name,
            f"""
        SELECT
            toStartOfMonth(dt) as start_of_month,
            toMonth(dt) as month,
            toYear(dt) as year,
            country,
            sumState(units) as sum_units
        FROM
            {landing_name}
        GROUP BY start_of_month, year, month, country
        """,
        )

        # Insert new data
        csv_url = self.get_url_for_sql(self.initial_data_query)
        params = {
            "token": self.token,
            "name": landing_name,
            "mode": "append",
            "url": csv_url,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")

        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done")
        self.expect_ops_log(
            {
                "event_type": "append",
                "datasource_name": landing_name,
                "options": {
                    "source": csv_url,
                },
            }
        )

        self.expect_ops_log({"event_type": "append", "datasource_name": monthly_ds_name})

        async def get_results():
            u = Users.get_by_id(self.WORKSPACE_ID)
            self.wait_for_datasource_replication(u, monthly_ds_name)
            return await self._query(
                query=f"SELECT year, month, sumMerge(sum_units) as sum_units FROM {monthly_ds_name} FINAL GROUP BY year, month ORDER BY year ASC, month ASC FORMAT JSON"
            )

        # Validate current data
        monthly_results = await get_results()
        self.assertEqual(len(monthly_results["data"]), 2)
        self.assertEqual(list(monthly_results["data"][0].values()), [2019, 1, 2 * 2 * 24])
        self.assertEqual(list(monthly_results["data"][1].values()), [2019, 2, 2 * 2 * 24])

        # Replace just part of the data
        csv_url = self.get_url_for_sql(
            """
            SELECT
                (toDate('2019-01-31') + dc.d) + toIntervalHour(h.number) AS dt,
                dc.country,
                2 AS units -- changing units
            FROM
            (
                SELECT * FROM
                (
                    SELECT number AS d
                    FROM system.numbers
                    LIMIT 30 -- 30 days = 1 day in January, 28 days in February, 1 day in March.
                )
                CROSS JOIN
                (
                    SELECT if(number = 1, 'ES', 'US') as country
                    FROM system.numbers
                    LIMIT 2
                )
            ) AS dc
            CROSS JOIN
            (
                SELECT number
                FROM system.numbers
                LIMIT 24
            ) AS h
            FORMAT CSVWithNames
        """
        )
        params = {
            "token": self.token,
            "mode": "replace",
            "replace_condition": "toDate(dt) == '2019-01-31' or toMonth(dt) IN (2, 3)",
            "name": landing_name,
            "url": csv_url,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done", str(job))
        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": landing_name,
                "options": {
                    "source": csv_url,
                    "replace_condition": "toDate(dt) == '2019-01-31' or toMonth(dt) IN (2, 3)",
                },
            }
        )
        self.expect_ops_log({"event_type": "replace", "datasource_name": monthly_ds_name})

        # Validate data after adding data to new partitions
        monthly_results = await get_results()
        self.assertEqual(len(monthly_results["data"]), 3)
        days = hours = countries = sales = lambda x: x
        january_sales = (days(1) * hours(24) * countries(2) * sales(1)) + (
            days(1) * hours(24) * countries(2) * sales(2)
        )
        februay_sales = days(28) * hours(24) * countries(2) * sales(2)
        march_sales = days(1) * hours(24) * countries(2) * sales(2)
        self.assertEqual(list(monthly_results["data"][0].values()), [2019, 1, january_sales])
        self.assertEqual(list(monthly_results["data"][1].values()), [2019, 2, februay_sales])
        self.assertEqual(list(monthly_results["data"][2].values()), [2019, 3, march_sales])
        await self.assert_stats_async(landing_name, self.token, 1488, 4096)

    @tornado.testing.gen_test
    async def test_replace_partial_invalid_condition(self):
        landing_name = "sales_landing_test_replace_partial_invalid_condition"
        await self.create_datasource_async(
            self.token,
            landing_name,
            """
            dt DateTime,
            country String,
            units Int32
        """,
            {"engine": "MergeTree", "engine_partition_key": "toYYYYMM(dt)", "engine_sorting_key": "country, dt"},
        )

        # Insert new data
        csv_url = self.get_url_for_sql(self.initial_data_query)
        params = {
            "token": self.token,
            "name": landing_name,
            "mode": "append",
            "url": csv_url,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"])

        self.assertEqual(job.status, "done")
        self.expect_ops_log(
            {
                "event_type": "append",
                "datasource_name": landing_name,
                "options": {
                    "source": csv_url,
                },
            }
        )

        # Replace just part of the data
        csv_url = self.get_url_for_sql(self.replace_data_query)
        replace_condition = "1=1 UNION ALL SELECT now(), name, toInt32(1) FROM system.tables"
        params = {
            "token": self.token,
            "mode": "replace",
            "replace_condition": replace_condition,
            "name": landing_name,
            "url": csv_url,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "error", str(job))
        self.maxDiff = None
        expected_error = re.compile(
            "Failed to apply replace_condition='1=1 UNION ALL SELECT now\(\), name, toInt32\(1\) FROM system.tables': DB::Exception: Syntax error:.*"
        )
        self.assertEqual(len(job["errors"]), 1)
        self.assertRegexpMatches(job["errors"][0], expected_error)
        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": landing_name,
                "result": "error",
                "error": expected_error,
                "options": {
                    "source": csv_url,
                    "replace_condition": replace_condition,
                },
            }
        )

    @tornado.testing.gen_test
    async def test_replace_partial_sql_injection(self):
        landing_name = "sales_landing"
        await self.create_datasource_async(
            self.token,
            landing_name,
            """
            dt DateTime,
            country String,
            units Int32
        """,
            {"engine": "MergeTree", "engine_partition_key": "toYYYYMM(dt)", "engine_sorting_key": "country, dt"},
        )

        # Replace just part of the data
        csv_url = self.get_url_for_sql(self.replace_data_query)
        replace_condition = "1=1 AND dt NOT IN (SELECT modification_time FROM remote('127.0.0.1', 'system.parts'))"
        params = {
            "token": self.token,
            "mode": "replace",
            "replace_condition": replace_condition,
            "name": landing_name,
            "url": csv_url,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "error", str(job))
        expected_error = "Failed to apply replace_condition='1=1 AND dt NOT IN (SELECT modification_time FROM remote('127.0.0.1', 'system.parts'))': DB::Exception: Usage of function remote is restricted. Contact support@tinybird.co if you require access to this feature"
        self.assertEqual(job["errors"], [expected_error])
        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": landing_name,
                "result": "error",
                "error": expected_error,
                "options": {
                    "source": csv_url,
                    "replace_condition": replace_condition,
                },
            }
        )

    @tornado.testing.gen_test
    async def test_replace_regression_partition_types(self):
        schema = """
            `checkout` Date,
            `numnights` Int8,
            `checkin` Date,
            `reservationid` String,
            `unifiedid` String,
            `reservationdate` DateTime,
            `totalnightlyprice` Float32,
            `currency` LowCardinality(String)
        """
        partitions = (
            "checkout",
            "reservationdate",
            "currency",
            "(currency, toYYYYMM(checkout))",
        )
        for i, partition in enumerate(partitions):
            with self.subTest(partition=partition):
                rand = str(uuid.uuid4())[:8]
                landing_name = f"trans_replace_{rand}_{i}"
                engine = {"engine": "MergeTree", "engine_partition_key": partition, "engine_sorting_key": "checkout"}
                await self.create_datasource_async(self.token, landing_name, schema, engine)

                # Insert new data
                csv_url = f"{HTTP_ADDRESS}/trans.csv"
                params = {
                    "token": self.token,
                    "name": landing_name,
                    "mode": "append",
                    "url": csv_url,
                }
                create_url = f"/v0/datasources?{urlencode(params)}"
                response = await self.fetch_async(create_url, method="POST", body="")
                self.assertEqual(response.code, 200)
                job = await self.get_finalised_job_async(json.loads(response.body)["id"])
                self.assertEqual(job.status, "done")
                self.expect_ops_log(
                    {
                        "event_type": "append",
                        "datasource_name": landing_name,
                        "options": {
                            "source": csv_url,
                        },
                    }
                )

                # Replace just part of the data
                csv_url = f"{HTTP_ADDRESS}/trans.csv"
                replace_condition = "currency = 'USD' and checkout between '2018-10-01' and '2018-10-31'"
                params = {
                    "token": self.token,
                    "mode": "replace",
                    "replace_condition": replace_condition,
                    "name": landing_name,
                    "url": csv_url,
                }
                create_url = f"/v0/datasources?{urlencode(params)}"
                response = await self.fetch_async(create_url, method="POST", body="")
                self.assertEqual(response.code, 200)
                job = await self.get_finalised_job_async(
                    json.loads(response.body)["id"], max_retries=600, elapsed_time_interval=0.5
                )
                self.assertEqual(job.status, "done", str(job))
                self.expect_ops_log(
                    {
                        "event_type": "replace",
                        "datasource_name": landing_name,
                        "options": {
                            "source": csv_url,
                            "replace_condition": replace_condition,
                        },
                    }
                )

    @tornado.testing.gen_test
    async def test_replace_cond_vs_partitions(self):
        schema = """
            `account_id` Int16,
            `channel_id` String,
            `name` String,
            `urls` Array(String)
        """
        partitions = (
            "account_id",
            "tuple()",
            # 'substring(toString(account_id), 1, 1)',
        )
        for i, partition in enumerate(partitions):
            with self.subTest(partition=partition):
                rand = str(uuid.uuid4())[:8]
                landing_name = f"replace_condition_not_partition_{rand}_{i}"
                engine = {
                    "engine": "MergeTree",
                    "engine_partition_key": partition,
                    "engine_sorting_key": "account_id, channel_id",
                }
                await self.create_datasource_async(self.token, landing_name, schema, engine)

                # Insert new data
                s = CsvIO(
                    '''40,58fd8bf-453d-4c81-88fe-7ab0a21932c3,plp 40,"['http://site40.com', 'https://site40.com']"''',
                    '''41,0becd4c9-833b-44d5-8d1d-b8e8bb83bb10,plp 41,"['http://site41.com', 'https://site41.com']"''',
                    '''42,eb6f5f00-fd09-4967-97fe-0070ff792e38,plp 42,"['http://site42.com', 'https://site42.com']"''',
                )
                params = {
                    "token": self.token,
                    "name": landing_name,
                    "mode": "append",
                }
                append_url = f"/v0/datasources?{urlencode(params)}"
                response = await self.fetch_full_body_upload_async(append_url, s)
                self.assertEqual(response.code, 200, response.body)
                result = json.loads(response.body)
                self.assertFalse(result["error"])
                self.expect_ops_log(
                    {
                        "event_type": "append",
                        "datasource_name": landing_name,
                        "options": {
                            "source": "full_body",
                        },
                    }
                )

                # Replace just part of the data
                replace_condition = "account_id = 0"
                params = {
                    "token": self.token,
                    "mode": "replace",
                    "replace_condition": replace_condition,
                    "name": landing_name,
                }
                s = CsvIO(
                    '''0,8edf5548-311d-44c0-b6e6-1cef6e3369ef,new dos,"['http://example.com/bait/believe?anger=apparatus', 'https://example.com/', 'http://www.example.com/', 'http://www.example.com/brother/baby.htm?beef=apparatus&bone=anger']"''',
                    '''0,68921a32-138f-4887-a2fe-3c84766a921f,new cinco,"['https://plytix.com']"''',
                    '''0,cb8f4e32-16dd-48a1-b558-3d1e0b47df9f,new uno,"['http://bait.example.org/believe?airplane=board&airport=attraction', 'http://www.example.com/achiever/blow', 'https://example.com/', 'https://example.edu/behavior.php?bell=blade&birthday=bedroom', 'http://example.com/baseball/argument', 'http://advice.example.com']"''',
                    '''0,591396c4-23bd-4ae4-96e2-4f4d64ffa84d,new cuatro,"['https://plytix.com']"''',
                    '''0,191c3ecc-09fc-4729-841d-ed988e361a48,new tres,"['https://plytix.com']"''',
                )
                replace_url = f"/v0/datasources?{urlencode(params)}"
                response = await self.fetch_full_body_upload_async(replace_url, s)
                self.assertEqual(response.code, 200, response.body)
                result = json.loads(response.body)
                self.assertFalse(result["error"])
                self.expect_ops_log(
                    {
                        "event_type": "replace",
                        "datasource_name": landing_name,
                        "options": {
                            "source": "full_body",
                            "replace_condition": replace_condition,
                        },
                    }
                )
                datasource = Users.get_datasource(self.u, landing_name)
                a = exec_sql(
                    self.u.database,
                    f"SELECT account_id, count() c FROM {datasource.id} GROUP BY account_id ORDER BY account_id FORMAT JSON",
                )
                expected_data = [
                    {"account_id": 0, "c": "5"},
                    {"account_id": 40, "c": "1"},
                    {"account_id": 41, "c": "1"},
                    {"account_id": 42, "c": "1"},
                ]
                self.assertEqual(a["data"], expected_data)

    @tornado.testing.gen_test
    async def test_replace_cond_not_in_partition_simple(self):
        schema = """
            `date` Date,
            `event` String,
            `count` UInt16
        """
        rand = str(uuid.uuid4())[:8]
        # NOTE: Add restriction when partition is not defined in replace with condition https://gitlab.com/tinybird/analytics/-/issues/3210
        landing_name = f"replace_condition_fails_{rand}"
        engine = {"engine": "MergeTree", "engine_partition_key": "toYYYYMM(date)", "engine_sorting_key": "event, date"}
        await self.create_datasource_async(self.token, landing_name, schema, engine)

        # Insert new data
        first_data = CsvIO(
            "2020-01-01,click,10",
            "2020-01-02,pv,20",
            "2020-12-01,pv,50",
        )

        params = {
            "token": self.token,
            "name": landing_name,
            "mode": "append",
        }
        append_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_full_body_upload_async(append_url, first_data)
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        self.assertFalse(result["error"])
        self.expect_ops_log(
            {
                "event_type": "append",
                "datasource_name": landing_name,
                "options": {
                    "source": "full_body",
                },
            }
        )

        # Replace just part of the data
        replace_condition = "toYYYYMM(date) IN (202001, 202012) AND event = 'pv'"

        params = {
            "token": self.token,
            "mode": "replace",
            "replace_condition": replace_condition,
            "name": landing_name,
        }
        replace_data = CsvIO(
            "2020-01-02,pv,25",
            "2020-01-03,pv,30",
            "2020-02-01,pv,60",
            "2020-01-04,click,5",
        )
        replace_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_full_body_upload_async(replace_url, replace_data)
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        self.assertFalse(result["error"])
        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": landing_name,
                "options": {
                    "source": "full_body",
                    "replace_condition": replace_condition,
                },
            }
        )
        datasource = Users.get_datasource(self.u, landing_name)
        a = exec_sql(self.u.database, f"SELECT * FROM {datasource.id} ORDER BY event, date FORMAT JSON")

        expected_data = [
            {"date": "2020-01-01", "event": "click", "count": 10},
            {"date": "2020-01-02", "event": "pv", "count": 25},
            {"date": "2020-01-03", "event": "pv", "count": 30},
            {"date": "2020-12-01", "event": "pv", "count": 50},
        ]

        self.assertEqual(a["data"], expected_data)

    async def prepare_replace_partial_dependent_non_mergetree_view(self, landing_name, tags_ds_name):
        await self.create_datasource_async(
            self.token,
            landing_name,
            """
            campaign LowCardinality(String),
            cod_brand Int8,
            country LowCardinality(String),
            partnumber String,
            date_start Date,
            date_end Date,
            type String
        """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "campaign",
                "engine_sorting_key": "cod_brand, country, date_start",
            },
        )

        # Create a dependent non-MergeTree data source
        await self.create_datasource_async(
            self.token,
            tags_ds_name,
            """
            partnumber String,
            country_tags Array(String),
            date_tags Array(Date),
            tags Array(String)
        """,
            {
                "engine": "Join",
                "engine_join_strictness": "ANY",
                "engine_join_type": "LEFT",
                "engine_key_columns": "partnumber",
            },
        )

        # Create the view to connect them
        await self.create_view_async(
            self.u,
            self.token,
            tags_ds_name,
            f"""
            SELECT
                partnumber,
                groupArray(date_start) date_tags,
                groupArray(country) country_tags,
                groupArray(type) tags
            FROM {landing_name}
            GROUP BY partnumber
        """,
        )

        # Insert new data
        csv = CsvIO(
            '"I2021",16,"AU","00000000001-I2021","2020-01-01","2020-01-31","NEW"',
            '"I2021",16,"AU","00000000001-I2021","2020-04-30","2020-04-30","SPRING"',
            '"I2021",16,"AU","00000000003-I2021","2020-06-01","2020-06-30","NEW"',
        )
        params = {"token": self.token, "name": landing_name, "mode": "replace", "replace_condition": "1=1"}

        replace_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_full_body_upload_async(replace_url, csv)

        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        self.assertFalse(result["error"])
        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": landing_name,
                "options": {
                    "source": "full_body",
                    "replace_condition": "1=1",
                },
            }
        )

        datasource = Users.get_datasource(self.u, tags_ds_name)

        a = exec_sql(
            self.u.database,
            f"""
            SELECT
                joinGet('{datasource.id}', 'tags', '00000000001-I2021') tags,
                joinGet('{datasource.id}', 'date_tags', '00000000001-I2021') date_tags
            FORMAT JSON
        """,
        )
        expected_data = [
            {"tags": ["NEW", "SPRING"], "date_tags": ["2020-01-01", "2020-04-30"]},
        ]
        self.assertEqual(a["data"], expected_data)

    async def _test_replace_partial_dependent_non_mergetree_view_body(self, use_database_server):
        original_database_server = self.u.database_server
        host, port = host_port_from_url(original_database_server)

        rand = str(uuid.uuid4())[:8]

        with User.transaction(self.u.id) as u:
            if use_database_server:
                u.database_server = f"http://{host}:{port}"
            else:
                u.database_server = original_database_server

        landing_name = f"articles_commercial_tags_{rand}"
        tags_ds_name = f"commercial_tags_{rand}"

        await self.prepare_replace_partial_dependent_non_mergetree_view(landing_name, tags_ds_name)

        # Replace just part of the data
        csv = CsvIO(
            '"I2021",16,"AU","00000000001-I2021","2020-01-15","2020-01-31","NEW"',
        )
        replace_condition = "type = 'NEW' AND date_start BETWEEN '2020-01-01' AND '2020-01-31'"
        params = {
            "token": self.token,
            "name": landing_name,
            "mode": "replace",
            "replace_condition": replace_condition,
        }
        replace_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_full_body_upload_async(replace_url, csv)
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        self.assertFalse(result["error"])
        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": landing_name,
                "options": {
                    "source": "full_body",
                    "replace_condition": replace_condition,
                },
            }
        )
        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": tags_ds_name,
                "options": {
                    "source": "full_body",
                    "replace_condition": replace_condition,
                },
            }
        )
        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": tags_ds_name,
                "options": {
                    "source": "full_body",
                    "replace_condition": "1=1",
                },
            }
        )

        datasource = Users.get_datasource(self.u, tags_ds_name)
        a = exec_sql(
            self.u.database,
            f"""
            SELECT
                joinGet('{datasource.id}', 'tags', '00000000001-I2021') tags,
                joinGet('{datasource.id}', 'date_tags', '00000000001-I2021') date_tags
            ORDER BY tags, date_tags
            FORMAT JSON
        """,
        )
        expected_data = [
            {"tags": ["NEW", "SPRING"], "date_tags": ["2020-01-15", "2020-04-30"]},
        ]
        self.assertCountEqual(a["data"][0]["tags"], expected_data[0]["tags"])
        self.assertCountEqual(a["data"][0]["date_tags"], expected_data[0]["date_tags"])

    @tornado.testing.gen_test
    async def test_replace_partial_dependent_non_mergetree_view_body(self):
        await self._test_replace_partial_dependent_non_mergetree_view_body(False)

    @tornado.testing.gen_test
    async def test_replace_partial_dependent_non_mergetree_view_body_using_database_server(self):
        await self._test_replace_partial_dependent_non_mergetree_view_body(True)


class TestAPIDatasourceHooksReplacePartialBatch3(TestAPIDatasourceHooksReplacePartialBase):
    async def prepare_replace_partial_dependent_unsupported_view(self, landing_name, tags_ds_name):
        await self.create_datasource_async(
            self.token,
            landing_name,
            """
            campaign LowCardinality(String),
            cod_brand Int8,
            country LowCardinality(String),
            partnumber String,
            date_start Date,
            date_end Date,
            type String
        """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "campaign",
                "engine_sorting_key": "cod_brand, country, date_start",
            },
        )

        # Create a dependent non-MergeTree data source
        await self.create_datasource_async(
            self.token,
            tags_ds_name,
            """
            partnumber String,
            country_tags Array(String),
            date_tags Array(Date),
            tags Array(String)
        """,
            {"engine": "Null"},
        )

        # Create the view to connect them
        await self.create_view_async(
            self.u,
            self.token,
            tags_ds_name,
            f"""
            SELECT
                partnumber,
                groupArray(country) country_tags,
                groupArray(date_start) date_tags,
                groupArray(type) tags
            FROM {landing_name}
            GROUP BY partnumber""",
        )

        # Insert new data
        csv = CsvIO(
            '"I2021",16,"AU","00000000001-I2021","2020-01-01","2020-01-31","NEW"',
            '"I2021",16,"AU","00000000001-I2021","2020-04-30","2020-04-30","SPRING"',
            '"I2021",16,"AU","00000000003-I2021","2020-06-01","2020-06-30","NEW"',
        )
        params = {
            "token": self.token,
            "name": landing_name,
            "mode": "append",
        }
        append_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_full_body_upload_async(append_url, csv)
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        self.assertFalse(result["error"])
        self.expect_ops_log(
            [
                {"event_type": "append", "datasource_name": landing_name, "options": {"source": "full_body"}},
                {"event_type": "append", "datasource_name": tags_ds_name},
            ]
        )

    @tornado.testing.gen_test
    async def test_replace_partial_dependent_unsupported_view_with_hook_error(self):
        rand = str(uuid.uuid4())[:8]
        landing_name = f"articles_commercial_tags_{rand}"
        tags_ds_name = f"commercial_tags_{rand}"

        await self.prepare_replace_partial_dependent_unsupported_view(landing_name, tags_ds_name)

        # Replace just part of the data
        csv = CsvIO(
            '"I2021",16,"AU","00000000001-I2021","2020-01-15","2020-01-31","NEW"',
        )
        replace_condition = "type = 'NEW' AND date_start BETWEEN '2020-01-01' AND '2020-01-31'"
        params = {
            "token": self.token,
            "name": landing_name,
            "mode": "replace",
            "replace_condition": replace_condition,
        }
        replace_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_full_body_upload_async(replace_url, csv)
        self.assertEqual(response.code, 400, response.body)
        result = json.loads(response.body)

        err = re.compile(
            f".*Partial replace can't be executed as at least one of the Data Sources involved \({tags_ds_name}\) has incompatible partitions.*"
        )
        self.assertRegexpMatches(result["errors"][0], err)

        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": landing_name,
                "result": "error",
                "error": err,
                "options": {
                    "source": "full_body",
                    "replace_condition": replace_condition,
                },
            }
        )

    @tornado.testing.gen_test
    async def test_replace_partial_with_multiple_sources(self):
        rand = str(uuid.uuid4())[:8]
        landing_name = f"sales_landing_{rand}"
        await self.create_datasource_async(
            self.token,
            landing_name,
            """
            dt DateTime,
            country String,
            units Int32
        """,
            {"engine": "MergeTree", "engine_partition_key": "toYYYYMM(dt)", "engine_sorting_key": "country, dt"},
        )

        # Create a dependent data source
        daily_ds_name = f"sales_daily_{rand}"
        await self.create_datasource_async(
            self.token,
            daily_ds_name,
            """
            d Date,
            country String,
            sum_units AggregateFunction(sum, Int32)
        """,
            {
                "engine": "AggregatingMergeTree",
                "engine_partition_key": "toYYYYMM(d)",
                "engine_sorting_key": "d, country",
            },
        )

        # Create the view to connect them
        await self.create_view_async(
            self.u,
            self.token,
            daily_ds_name,
            f"""
        SELECT
            toDate(dt) AS d,
            country,
            sumState(units) AS sum_units
        FROM {landing_name}
        GROUP BY d, country
        """,
        )

        # Extra landing that will push to daily
        other_landing_name = f"other_sales_landing_{rand}"
        await self.create_datasource_async(
            self.token,
            other_landing_name,
            """
            dt DateTime,
            country String,
            units Int32
        """,
            {"engine": "MergeTree", "engine_partition_key": "toYYYYMM(dt)", "engine_sorting_key": "country, dt"},
        )
        # Create the view to connect it to the daily
        await self.create_view_async(
            self.u,
            self.token,
            daily_ds_name,
            f"""
        SELECT
            toDate(dt) AS d,
            sumState(units) AS sum_units,
            country
        FROM {other_landing_name}
        GROUP BY d, country
        """,
        )

        # Insert new data in the landing
        csv_url = self.get_url_for_sql(self.initial_data_query)
        params = {
            "token": self.token,
            "name": landing_name,
            "mode": "append",
            "url": csv_url,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done")

        self.expect_ops_log({"event_type": "append", "datasource_name": landing_name, "options": {"source": csv_url}})
        self.expect_ops_log([{"event_type": "append", "datasource_name": daily_ds_name}])

        # Insert new data in the other landing

        csv_url = self.get_url_for_sql(self.initial_data_query)
        params = {
            "token": self.token,
            "name": other_landing_name,
            "mode": "append",
            "url": csv_url,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done")

        self.expect_ops_log(
            {"event_type": "append", "datasource_name": other_landing_name, "options": {"source": csv_url}}
        )
        self.expect_ops_log([{"event_type": "append", "datasource_name": daily_ds_name}])

        async def get_views_results():
            self.wait_for_datasource_replication(self.u, daily_ds_name)
            self.wait_for_datasource_replication(self.u, landing_name)
            self.wait_for_datasource_replication(self.u, other_landing_name)

            daily_results = await self._query(
                query=f"""
                SELECT d, sumMerge(sum_units) as sum_units
                FROM {daily_ds_name}
                FINAL
                GROUP BY d
                ORDER BY d ASC
                FORMAT JSON"""
            )

            await asyncio.sleep(0.5)

            daily_results_from_landings = await self._query(
                query=f"""
                SELECT
                    toDate(dt) AS d,
                    sum(units) AS sum_units
                FROM (
                    SELECT * FROM {landing_name}
                    UNION ALL
                    SELECT * FROM {other_landing_name}
                )
                GROUP BY d
                ORDER BY d ASC
                FORMAT JSON"""
            )

            self.assertEqual(daily_results_from_landings["data"], daily_results["data"])
            return daily_results

        # Validate current data
        days = hours = countries = sales = sources = lambda x: x
        daily_results = await get_views_results()
        self.assertEqual(len(daily_results["data"]), 4)
        daily_sales = days(1) * hours(24) * countries(2) * sales(1) * sources(2)
        self.assertEqual(list(daily_results["data"][0].values()), ["2019-01-30", daily_sales])
        self.assertEqual(list(daily_results["data"][1].values()), ["2019-01-31", daily_sales])
        self.assertEqual(list(daily_results["data"][2].values()), ["2019-02-01", daily_sales])
        self.assertEqual(list(daily_results["data"][3].values()), ["2019-02-02", daily_sales])

        # Replace just part of the data in the first landing
        csv_url = self.get_url_for_sql(self.replace_data_query)
        params = {
            "token": self.token,
            "mode": "replace",
            "replace_condition": "toDate(dt) == '2019-01-31'",
            "name": landing_name,
            "url": csv_url,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done", str(job))
        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": landing_name,
                "options": {
                    "source": csv_url,
                    "replace_condition": "toDate(dt) == '2019-01-31'",
                },
            }
        )
        self.expect_ops_log({"event_type": "replace", "datasource_name": daily_ds_name})
        self.expect_ops_log({"event_type": "replace", "datasource_name": daily_ds_name})

        # Validate data after replacing just one day
        daily_results = await get_views_results()
        self.assertEqual(len(daily_results["data"]), 4)
        daily_sales = days(1) * hours(24) * countries(2) * sales(1) * sources(2)
        daily_replaced_sales = days(1) * hours(24) * countries(2) * sales(2) + days(1) * hours(24) * countries(
            2
        ) * sales(1)  # The other landing with its existing sales.
        self.assertEqual(list(daily_results["data"][0].values()), ["2019-01-30", daily_sales])
        self.assertEqual(list(daily_results["data"][1].values()), ["2019-01-31", daily_replaced_sales])
        self.assertEqual(list(daily_results["data"][2].values()), ["2019-02-01", daily_sales])
        self.assertEqual(list(daily_results["data"][3].values()), ["2019-02-02", daily_sales])

    @tornado.testing.gen_test
    async def test_replace_partial_dependent_invalid_partition_error_message(self):
        rand = str(uuid.uuid4())[:8]
        landing_name = f"visits_raw_{rand}"
        target_name = f"visits_daily_{rand}"

        await self.create_datasource_async(
            self.token,
            landing_name,
            """
            timestamp DateTime,
            country String
        """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "country, timestamp",
            },
        )
        await self.create_datasource_async(
            self.token,
            target_name,
            """
            date Date,
            country String,
            visits UInt64
        """,
            {"engine": "MergeTree", "engine_partition_key": "tuple()", "engine_sorting_key": "country, date"},
        )

        # Create the view to connect them
        await self.create_view_async(
            self.u,
            self.token,
            target_name,
            f"""
            SELECT
                toDate(timestamp) date,
                country,
                count() as visits
            FROM {landing_name}
            GROUP BY date, country
        """,
        )

        # Insert new data
        csv = CsvIO(
            '"2020-01-01 00:00:00","ES"',
            '"2020-01-01 00:00:01","FR"',
            '"2020-01-01 00:00:02","ES"',
            '"2020-01-02 00:00:00","ES"',
            '"2020-01-02 00:00:01","PT"',
            '"2020-01-02 00:00:02","FR"',
        )
        params = {
            "token": self.token,
            "name": landing_name,
            "mode": "append",
        }
        append_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_full_body_upload_async(append_url, csv)
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        self.assertFalse(result["error"])
        self.expect_ops_log(
            {"event_type": "append", "datasource_name": landing_name, "options": {"source": "full_body"}}
        )

        self.expect_ops_log({"event_type": "append", "datasource_name": target_name})

        datasource = Users.get_datasource(self.u, target_name)

        a = exec_sql(
            self.u.database,
            f"""
            SELECT
                *
            FROM {datasource.id}
            ORDER BY date, country
            FORMAT JSON
        """,
        )
        expected_data = [
            {"country": "ES", "date": "2020-01-01", "visits": "2"},
            {"country": "FR", "date": "2020-01-01", "visits": "1"},
            {"country": "ES", "date": "2020-01-02", "visits": "1"},
            {"country": "FR", "date": "2020-01-02", "visits": "1"},
            {"country": "PT", "date": "2020-01-02", "visits": "1"},
        ]
        self.assertEqual(a["data"], expected_data)

        # Replace with job URL
        csv_url = self.get_url_for_sql("SELECT '2020-01-01 00:00:00' as timestamp, 'PT' as country")
        replace_condition = "toDate(timestamp) == '2020-01-01'"
        params = {
            "token": self.token,
            "mode": "replace",
            "replace_condition": replace_condition,
            "name": landing_name,
            "url": csv_url,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        job_id = json.loads(response.body)["id"]
        job = await self.get_finalised_job_async(job_id)
        self.maxDiff = None
        self.expect_ops_log(
            {
                "result": "error",
                "event_type": "replace",
                "datasource_name": landing_name,
                "options": {
                    "source": csv_url,
                    "replace_condition": replace_condition,
                },
            }
        )

        expected_error_message_20 = f"Partial replace can't be executed as at least one of the Data Sources involved ({datasource.name}) has incompatible partitions. Check the PARTITION KEY is present and it's the same in both Data Sources. e.g. both Data Sources are partitions using toYYYYMM or toDate, as opposed to one having toYYMMMM and the other tuple(). If you want to ignore all the Data Sources with incompatible partitions in the replace operation, please use the option 'skip_incompatible_partition_key' to skip them."
        expected_error_message_21 = f"{expected_error_message_20}. (INVALID_PARTITION_VALUE)"

        self.assertEqual(job.status, "error", str(job))
        self.assertEqual(
            job.error, "There was an error when attempting to import your data. Check 'errors' for more information."
        )

        self.assertIn(
            job.errors[0],
            [
                f"Error when running after import tasks on job {job_id}: {expected_error_message_20}",
                f"Error when running after import tasks on job {job_id}: {expected_error_message_21}",
            ],
        )

        # Replace with direct request
        # Insert new data
        s = CsvIO(
            "2020-01-01 00:00:00,PT",
        )
        params = {"token": self.token, "name": landing_name, "mode": "replace", "replace_condition": replace_condition}
        append_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_full_body_upload_async(append_url, s)
        self.assertEqual(response.code, 400, response.body)
        result = json.loads(response.body)
        self.assertTrue(result["error"])
        self.assertIn(result["errors"][0], [expected_error_message_20, expected_error_message_21])
        self.expect_ops_log(
            {
                "result": "error",
                "event_type": "replace",
                "datasource_name": landing_name,
                "options": {
                    "replace_condition": replace_condition,
                },
            }
        )

    @tornado.testing.gen_test
    async def test_replace_partial_going_down_multiple_levels_of_mvs(self):
        """
        +------+  insert/replace   +---------+  MV1to2   +-----+  MV2to3   +-----+
        |  ws  | ----------------> |   DS1   | --------> | DS2 | --------> | DS3 |
        +------+                   +---------+           +-----+           +-----+
        """

        rand = str(uuid.uuid4())[:8]
        ds1 = f"DS1_{rand}"
        await self.create_datasource_async(
            self.token,
            ds1,
            """
            dt Date,
            country String,
            product String,
            units Int32
        """,
            {"engine": "MergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        ds2 = f"DS2_{rand}"
        await self.create_datasource_async(
            self.token,
            ds2,
            """
            dt Date,
            country String,
            product String,
            sum_units Int32
        """,
            {"engine": "SummingMergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds2,
            f"""
        SELECT
            dt,
            country,
            product,
            toInt32(sum(units)) AS sum_units
        FROM {ds1}
        GROUP BY dt, country, product
        """,
            pipe_name="MV1to2",
        )

        ds3 = f"DS3_{rand}"
        await self.create_datasource_async(
            self.token,
            ds3,
            """
            dt Date,
            country String,
            sum_per_country Int32
        """,
            {"engine": "SummingMergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds3,
            f"""
        SELECT
            dt,
            country,
            toInt32(sum(sum_units)) AS sum_per_country
        FROM {ds2}
        GROUP BY dt, country
        """,
            pipe_name="MV2to3",
        )

        extra_expected_ops_logs = [
            {"event_type": "replace", "datasource_name": ds2, "result": "ok"},
            {"event_type": "replace", "datasource_name": ds3, "result": "ok"},
        ]

        await self.append_data_to_datasource(
            self.token,
            ds1,
            CsvIO(
                "2020-01-01,ES,A,1",
                "2020-01-01,ES,A,1",
                "2020-01-01,ES,B,1",
                "2020-01-02,ES,A,1",
                "2020-01-02,ES,A,1",
                "2020-01-02,ES,B,1",
            ),
            extra_expected_ops_logs=extra_expected_ops_logs,
        )

        self.expect_ops_log(
            [{"event_type": "append", "datasource_name": ds2}, {"event_type": "append", "datasource_name": ds3}]
        )

        await self.expected_data_in_datasource(
            self.token,
            ds1,
            """"2020-01-01","ES","A",1
"2020-01-01","ES","A",1
"2020-01-01","ES","B",1
"2020-01-02","ES","A",1
"2020-01-02","ES","A",1
"2020-01-02","ES","B",1
""",
            "dt, country, product",
        )
        await self.expected_data_in_datasource(
            self.token,
            ds2,
            """"2020-01-01","ES","A",2
"2020-01-01","ES","B",1
"2020-01-02","ES","A",2
"2020-01-02","ES","B",1
""",
            "dt, country, product",
        )

        await self.expected_data_in_datasource(
            self.token,
            ds3,
            """"2020-01-01","ES",3
"2020-01-02","ES",3
""",
            "dt, country",
        )

        await self.replace_with_data_in_sql_async(
            self.token,
            ds1,
            "dt = '2020-01-02'",
            """
        SELECT row[1], row[2], row[3], row[4]
        FROM ( SELECT arrayJoin([
        ['2020-01-02', 'ES', 'A', '5'],
        ['2020-01-02', 'ES', 'A', '5'],
        ['2020-01-02', 'ES', 'B', '5']
        ]) as row) format CSV;
        """,
        )

        await self.expected_data_in_datasource(
            self.token,
            ds1,
            """"2020-01-01","ES","A",1
"2020-01-01","ES","A",1
"2020-01-01","ES","B",1
"2020-01-02","ES","A",5
"2020-01-02","ES","A",5
"2020-01-02","ES","B",5
""",
            "dt, country, product",
        )
        await self.expected_data_in_datasource(
            self.token,
            ds2,
            """"2020-01-01","ES","A",2
"2020-01-01","ES","B",1
"2020-01-02","ES","A",10
"2020-01-02","ES","B",5
""",
            "dt, country, product",
        )

        await self.expected_data_in_datasource(
            self.token,
            ds3,
            """"2020-01-01","ES",3
"2020-01-02","ES",15
""",
            "dt, country",
        )

    @tornado.testing.gen_test
    async def test_replace_partial_with_two_mvs_writting_to_the_same_final_ds(self):
        """
                                           MV1to2b
                                     +------------------+
                                     |                  v
        +------+  insert/replace   +-----+  MV1to2a   +-----+
        |  ws  | ----------------> | DS1 | ---------> | DS2 |
        +------+                   +-----+            +-----+
        """
        rand = str(uuid.uuid4())[:8]
        ds1 = f"DS1_{rand}"
        await self.create_datasource_async(
            self.token,
            ds1,
            """
            dt Date,
            country String,
            product String,
            units Int32
        """,
            {"engine": "MergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        ds2 = f"DS2_{rand}"
        await self.create_datasource_async(
            self.token,
            ds2,
            """
            dt Date,
            country String,
            product String,
            sum_units Int32
        """,
            {"engine": "SummingMergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds2,
            f"""
        SELECT
            dt,
            country,
            concat(product, '-A') as product,
            toInt32(sum(units)) AS sum_units
        FROM (
            SELECT *
            FROM {ds1}
            WHERE product = 'A'
        )
        GROUP BY dt, country, product
        """,
            pipe_name="MV1to2a",
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds2,
            f"""
        SELECT
            dt,
            country,
            concat(product, '-B') as product,
            toInt32(sum(units)) AS sum_units
        FROM (
            SELECT *
            FROM {ds1}
            WHERE product = 'B'
        )
        GROUP BY dt, country, product
        """,
            pipe_name="MV1to2b",
        )

        await self.append_data_to_datasource(
            self.token,
            ds1,
            CsvIO(
                "2020-01-01,ES,A,1",
                "2020-01-01,ES,A,1",
                "2020-01-01,ES,B,1",
                "2020-01-02,ES,A,1",
                "2020-01-02,ES,A,1",
                "2020-01-02,ES,B,1",
            ),
        )

        self.expect_ops_log(
            [{"event_type": "append", "datasource_name": ds2}, {"event_type": "append", "datasource_name": ds2}]
        )

        await self.expected_data_in_datasource(
            self.token,
            ds1,
            """"2020-01-01","ES","A",1
"2020-01-01","ES","A",1
"2020-01-01","ES","B",1
"2020-01-02","ES","A",1
"2020-01-02","ES","A",1
"2020-01-02","ES","B",1
""",
            "dt, country, product",
        )

        await self.expected_data_in_datasource(
            self.token,
            ds2,
            """"2020-01-01","ES","A-A",2
"2020-01-01","ES","B-B",1
"2020-01-02","ES","A-A",2
"2020-01-02","ES","B-B",1
""",
            "dt, country, product",
        )

        extra_expected_ops_logs = [
            {"event_type": "replace", "datasource_name": ds2},
            {"event_type": "replace", "datasource_name": ds2},
        ]
        await self.replace_with_data_in_sql_async(
            self.token,
            ds1,
            "dt = '2020-01-02'",
            """
        SELECT row[1], row[2], row[3], row[4]
        FROM ( SELECT arrayJoin([
        ['2020-01-02', 'ES', 'A', '5'],
        ['2020-01-02', 'ES', 'A', '5'],
        ['2020-01-02', 'ES', 'B', '5']
        ]) as row) format CSV;
                """,
            expect_logs=True,
            extra_expected_ops_logs=extra_expected_ops_logs,
        )

        await self.expected_data_in_datasource(
            self.token,
            ds1,
            """"2020-01-01","ES","A",1
"2020-01-01","ES","A",1
"2020-01-01","ES","B",1
"2020-01-02","ES","A",5
"2020-01-02","ES","A",5
"2020-01-02","ES","B",5
""",
            "dt, country, product",
        )
        await self.expected_data_in_datasource(
            self.token,
            ds2,
            """"2020-01-01","ES","A-A",2
"2020-01-01","ES","B-B",1
"2020-01-02","ES","A-A",10
"2020-01-02","ES","B-B",5
""",
            "dt, country, product",
        )

    @tornado.testing.gen_test
    async def test_replace_partial_to_a_mv_that_writes_to_a_ds_where_other_two_mvs_are_writing(self):
        """
        +------+  MV2to4           +---------+  MV3to4   +-----+
        | DS2  | ----------------> |   DS4   | <-------- | DS3 |
        +------+                   +---------+           +-----+
                                     ^
                                     | MV1to4
                                     |
        +------+  insert/replace   +---------+
        |  ws  | ----------------> |   DS1   |
        +------+                   +---------+
        """
        rand = str(uuid.uuid4())[:8]
        ds1 = f"DS1_{rand}"
        await self.create_datasource_async(
            self.token,
            ds1,
            """
            dt Date,
            country String,
            product String,
            units Int32
        """,
            {"engine": "MergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        ds2 = f"DS2_{rand}"
        await self.create_datasource_async(
            self.token,
            ds2,
            """
            dt Date,
            country String,
            product String,
            units Int32
        """,
            {"engine": "MergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        ds3 = f"DS3_{rand}"
        await self.create_datasource_async(
            self.token,
            ds3,
            """
            dt Date,
            country String,
            product String,
            units Int32
        """,
            {"engine": "MergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        ds4 = f"DS4_{rand}"
        await self.create_datasource_async(
            self.token,
            ds4,
            """
            dt Date,
            country String,
            product String,
            sum_units Int32
        """,
            {"engine": "SummingMergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds4,
            f"""
        SELECT
            dt,
            country,
            product,
            toInt32(sum(units)) AS sum_units
        FROM {ds1}
        GROUP BY dt, country, product
        """,
            pipe_name="MV1to4",
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds4,
            f"""
        SELECT
            dt,
            country,
            product,
            toInt32(sum(units)) AS sum_units
        FROM {ds2}
        GROUP BY dt, country, product
        """,
            pipe_name="MV2to4",
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds4,
            f"""
        SELECT
            dt,
            country,
            product,
            toInt32(sum(units)) AS sum_units
        FROM {ds3}
        GROUP BY dt, country, product
        """,
            pipe_name="MV3to4",
        )

        await self.append_data_to_datasource(
            self.token,
            ds1,
            CsvIO(
                "2020-01-01,ES,A,1",
                "2020-01-02,ES,A,1",
            ),
        )
        self.expect_ops_log({"event_type": "append", "datasource_name": ds4})

        await self.append_data_to_datasource(
            self.token,
            ds2,
            CsvIO(
                "2020-01-01,ES,A,1",
                "2020-01-02,ES,A,1",
            ),
        )
        self.expect_ops_log({"event_type": "append", "datasource_name": ds4})
        await self.append_data_to_datasource(
            self.token,
            ds3,
            CsvIO(
                "2020-01-01,ES,A,1",
                "2020-01-02,ES,A,1",
            ),
        )
        self.expect_ops_log({"event_type": "append", "datasource_name": ds4})

        u = Users.get_by_id(self.WORKSPACE_ID)
        ds4_id = Users.get_datasource(u, ds4).id
        self.wait_for_datasource_replication(u, ds4_id)

        await self.expected_data_in_datasource(
            self.token,
            ds4,
            """"2020-01-01","ES","A",3
"2020-01-02","ES","A",3
""",
            "dt, country, product",
            add_final=True,
        )

        await self.replace_with_data_in_sql_async(
            self.token,
            ds1,
            "dt = '2020-01-02'",
            """
        SELECT row[1], row[2], row[3], row[4]
        FROM ( SELECT arrayJoin([
        ['2020-01-02', 'ES', 'A', '5'],
        ['2020-01-02', 'ES', 'B', '5']
        ]) as row) format CSV;
""",
        )

        self.expect_ops_log({"event_type": "replace", "datasource_name": ds4})
        self.expect_ops_log({"event_type": "replace", "datasource_name": ds4})
        self.expect_ops_log({"event_type": "replace", "datasource_name": ds4})
        await self.expected_data_in_datasource(
            self.token,
            ds1,
            """"2020-01-01","ES","A",1
"2020-01-02","ES","A",5
"2020-01-02","ES","B",5
""",
            "dt, country, product",
        )

        await self.expected_data_in_datasource(
            self.token,
            ds2,
            """"2020-01-01","ES","A",1
"2020-01-02","ES","A",1
""",
            "dt, country, product",
        )

        await self.expected_data_in_datasource(
            self.token,
            ds3,
            """"2020-01-01","ES","A",1
"2020-01-02","ES","A",1
""",
            "dt, country, product",
        )

        await self.expected_data_in_datasource(
            self.token,
            ds4,
            """"2020-01-01","ES","A",3
"2020-01-02","ES","A",7
"2020-01-02","ES","B",5
""",
            "dt, country, product",
            add_final=True,
        )

    @tornado.testing.gen_test
    async def test_replace_partial_where_the_execution_is_divided_in_two_branches(self):
        """
        +------+  insert/replace   +---------+  MV1to2   +-----+  MV2to4   +-----+
        |  ws  | ----------------> |   DS1   | --------> | DS2 | --------> | DS4 |
        +------+                   +---------+           +-----+           +-----+
                                     |
                                     | MV1to3
                                     v
                                   +---------+  MV3to5   +-----+
                                   |   DS3   | --------> | DS5 |
                                   +---------+           +-----+
        """
        rand = str(uuid.uuid4())[:8]
        ds1 = f"DS1_{rand}"
        await self.create_datasource_async(
            self.token,
            ds1,
            """
                    dt Date,
                    country String,
                    product String,
                    units Int32
                """,
            {"engine": "MergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        ds2 = f"DS2_{rand}"
        await self.create_datasource_async(
            self.token,
            ds2,
            """
                    dt Date,
                    country String,
                    product String,
                    sum_units Int32
                """,
            {"engine": "SummingMergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds2,
            f"""
                SELECT
                    dt,
                    country,
                    product,
                    toInt32(sum(units)) AS sum_units
                FROM {ds1}
                WHERE product = 'A'
                GROUP BY dt, country, product
                """,
            pipe_name="MV1to2",
        )

        ds4 = f"DS4_{rand}"
        await self.create_datasource_async(
            self.token,
            ds4,
            """
                    dt Date,
                    country String,
                    sum_per_country Int32
                """,
            {"engine": "SummingMergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds4,
            f"""
                SELECT
                    dt,
                    country,
                    toInt32(sum(sum_units)) AS sum_per_country
                FROM {ds2}
                GROUP BY dt, country
                """,
            pipe_name="MV2to4",
        )

        ds3 = f"DS3_{rand}"
        await self.create_datasource_async(
            self.token,
            ds3,
            """
                    dt Date,
                    country String,
                    product String,
                    sum_units Int32
                """,
            {"engine": "SummingMergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds3,
            f"""
                SELECT
                    dt,
                    country,
                    product,
                    toInt32(sum(units)) AS sum_units
                FROM {ds1}
                WHERE product = 'B'
                GROUP BY dt, country, product
                """,
            pipe_name="MV1to3",
        )

        ds5 = f"DS5_{rand}"
        await self.create_datasource_async(
            self.token,
            ds5,
            """
                    dt Date,
                    country String,
                    sum_per_country Int32
                """,
            {"engine": "MergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds5,
            f"""
                SELECT
                    dt,
                    country,
                    toInt32(sum(sum_units)) AS sum_per_country
                FROM {ds3}
                GROUP BY dt, country
                """,
            pipe_name="MV3to5",
        )

        await self.append_data_to_datasource(
            self.token,
            ds1,
            CsvIO(
                "2020-01-01,ES,A,1",
                "2020-01-01,ES,A,1",
                "2020-01-01,ES,B,1",
                "2020-01-02,ES,A,1",
                "2020-01-02,ES,A,1",
                "2020-01-02,ES,B,1",
            ),
        )

        self.expect_ops_log(
            [
                {"event_type": "append", "datasource_name": ds2},
                {"event_type": "append", "datasource_name": ds3},
                {"event_type": "append", "datasource_name": ds4},
                {"event_type": "append", "datasource_name": ds5},
            ]
        )

        u = Users.get_by_id(self.WORKSPACE_ID)
        ds4_id = Users.get_datasource(u, ds4).id
        self.wait_for_datasource_replication(u, ds4_id)

        ds5_id = Users.get_datasource(u, ds5).id
        self.wait_for_datasource_replication(u, ds5_id)

        await self.expected_data_in_datasource(
            self.token,
            ds1,
            """"2020-01-01","ES","A",1
"2020-01-01","ES","A",1
"2020-01-01","ES","B",1
"2020-01-02","ES","A",1
"2020-01-02","ES","A",1
"2020-01-02","ES","B",1
""",
            "dt, country, product",
        )
        await self.expected_data_in_datasource(
            self.token,
            ds2,
            """"2020-01-01","ES","A",2
"2020-01-02","ES","A",2
""",
            "dt, country, product",
        )

        await self.expected_data_in_datasource(
            self.token,
            ds3,
            """"2020-01-01","ES","B",1
"2020-01-02","ES","B",1
""",
            "dt, country, product",
        )

        await self.expected_data_in_datasource(
            self.token,
            ds4,
            """"2020-01-01","ES",2
"2020-01-02","ES",2
""",
            "dt, country",
        )

        await self.expected_data_in_datasource(
            self.token,
            ds5,
            """"2020-01-01","ES",1
"2020-01-02","ES",1
""",
            "dt, country",
        )
        extra_expected_ops_logs = [
            {"event_type": "replace", "datasource_name": ds3},
            {"event_type": "replace", "datasource_name": ds5},
            {"event_type": "replace", "datasource_name": ds2},
            {"event_type": "replace", "datasource_name": ds4},
        ]
        await self.replace_with_data_in_sql_async(
            self.token,
            ds1,
            "dt = '2020-01-02'",
            """
        SELECT row[1], row[2], row[3], row[4]
        FROM ( SELECT arrayJoin([
        ['2020-01-02', 'ES', 'A', '5'],
        ['2020-01-02', 'ES', 'A', '5'],
        ['2020-01-02', 'ES', 'B', '5']
        ]) as row) format CSV;
""",
            extra_expected_ops_logs=extra_expected_ops_logs,
            expect_logs=True,
        )

        await self.expected_data_in_datasource(
            self.token,
            ds1,
            """"2020-01-01","ES","A",1
"2020-01-01","ES","A",1
"2020-01-01","ES","B",1
"2020-01-02","ES","A",5
"2020-01-02","ES","A",5
"2020-01-02","ES","B",5
""",
            "dt, country, product",
        )
        await self.expected_data_in_datasource(
            self.token,
            ds2,
            """"2020-01-01","ES","A",2
"2020-01-02","ES","A",10
""",
            "dt, country, product",
        )

        await self.expected_data_in_datasource(
            self.token,
            ds3,
            """"2020-01-01","ES","B",1
"2020-01-02","ES","B",5
""",
            "dt, country, product",
        )

        await self.expected_data_in_datasource(
            self.token,
            ds4,
            """"2020-01-01","ES",2
"2020-01-02","ES",10
""",
            "dt, country",
        )

        await self.expected_data_in_datasource(
            self.token,
            ds5,
            """"2020-01-01","ES",1
"2020-01-02","ES",5
""",
            "dt, country",
        )

    @tornado.testing.gen_test
    async def test_replace_partial_where_the_execution_is_divided_in_two_branches_and_then_their_results_are_mixed(
        self,
    ):
        """
                                           MV1to3
                                     +-----------------------------------+
                                     |                                   v
        +------+  insert/replace   +-----+  MV1to2   +-----+  MV2to3   +-----+  MV3to4   +-----+
        |  ws  | ----------------> | DS1 | --------> | DS2 | --------> | DS3 | --------> | DS4 |
        +------+                   +-----+           +-----+           +-----+           +-----+
        """
        rand = str(uuid.uuid4())[:8]
        ds1 = f"DS1_{rand}"
        await self.create_datasource_async(
            self.token,
            ds1,
            """
                            dt Date,
                            country String,
                            product String,
                            units Int32
                        """,
            {"engine": "MergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        ds2 = f"DS2_{rand}"
        await self.create_datasource_async(
            self.token,
            ds2,
            """
                            dt Date,
                            country String,
                            product String,
                            sum_units Int32
                        """,
            {"engine": "SummingMergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds2,
            f"""
                        SELECT
                            dt,
                            country,
                            product,
                            toInt32(sum(units)) AS sum_units
                        FROM {ds1}
                        WHERE product = 'A'
                        GROUP BY dt, country, product
                        """,
            pipe_name="MV1to2",
        )
        ds3 = f"DS3_{rand}"
        await self.create_datasource_async(
            self.token,
            ds3,
            """
                            dt Date,
                            country String,
                            product String,
                            sum_units Int32
                        """,
            {"engine": "SummingMergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds3,
            f"""
                        SELECT
                            dt,
                            country,
                            product,
                            toInt32(sum(units)) AS sum_units
                        FROM {ds1}
                        WHERE product = 'B'
                        GROUP BY dt, country, product
                        """,
            pipe_name="MV1to3",
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds3,
            f"""
                        SELECT
                            dt,
                            country,
                            concat(product, '-A') as product,
                            toInt32(sum(sum_units)) AS sum_units
                        FROM {ds2}
                        GROUP BY dt, country, product
                        """,
            pipe_name="MV2to3",
        )

        ds4 = f"DS4_{rand}"
        await self.create_datasource_async(
            self.token,
            ds4,
            """
                            dt Date,
                            country String,
                            sum_per_country Int32
                        """,
            {"engine": "SummingMergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds4,
            f"""
                        SELECT
                            dt,
                            country,
                            toInt32(sum(sum_units)) AS sum_per_country
                        FROM {ds3}
                        GROUP BY dt, country
                        """,
            pipe_name="MV3to4",
        )

        await self.append_data_to_datasource(
            self.token,
            ds1,
            CsvIO(
                "2020-01-01,ES,A,1",
                "2020-01-01,ES,A,1",
                "2020-01-01,ES,B,1",
                "2020-01-02,ES,A,1",
                "2020-01-02,ES,A,1",
                "2020-01-02,ES,B,1",
            ),
        )

        self.expect_ops_log(
            [
                {"event_type": "append", "datasource_name": ds2},
                {"event_type": "append", "datasource_name": ds3},
                {"event_type": "append", "datasource_name": ds3},
                {"event_type": "append", "datasource_name": ds4},
            ]
        )

        await self.expected_data_in_datasource(
            self.token,
            ds1,
            """"2020-01-01","ES","A",1
"2020-01-01","ES","A",1
"2020-01-01","ES","B",1
"2020-01-02","ES","A",1
"2020-01-02","ES","A",1
"2020-01-02","ES","B",1
""",
            "dt, country, product",
        )
        await self.expected_data_in_datasource(
            self.token,
            ds2,
            """"2020-01-01","ES","A",2
"2020-01-02","ES","A",2
""",
            "dt, country, product",
            add_final=True,
        )

        await self.expected_data_in_datasource(
            self.token,
            ds3,
            """"2020-01-01","ES","A-A",2
"2020-01-01","ES","B",1
"2020-01-02","ES","A-A",2
"2020-01-02","ES","B",1
""",
            "dt, country, product",
            add_final=True,
        )

        await self.expected_data_in_datasource(
            self.token,
            ds4,
            """"2020-01-01","ES",3
"2020-01-02","ES",3
""",
            "dt, country",
            add_final=True,
        )
        extra_expected_ops_logs = [
            {"event_type": "replace", "datasource_name": ds2},
            {"event_type": "replace", "datasource_name": ds3},
            {"event_type": "replace", "datasource_name": ds3},
            {"event_type": "replace", "datasource_name": ds4},
        ]
        await self.replace_with_data_in_sql_async(
            self.token,
            ds1,
            "dt = '2020-01-02'",
            """
        SELECT row[1], row[2], row[3], row[4]
        FROM ( SELECT arrayJoin([
        ['2020-01-02', 'ES', 'A', '5'],
        ['2020-01-02', 'ES', 'A', '5'],
        ['2020-01-02', 'ES', 'B', '5']
        ]) as row) format CSV;
""",
            extra_expected_ops_logs=extra_expected_ops_logs,
            expect_logs=True,
        )

        await self.expected_data_in_datasource(
            self.token,
            ds1,
            """"2020-01-01","ES","A",1
"2020-01-01","ES","A",1
"2020-01-01","ES","B",1
"2020-01-02","ES","A",5
"2020-01-02","ES","A",5
"2020-01-02","ES","B",5
""",
            "dt, country, product",
        )
        await self.expected_data_in_datasource(
            self.token,
            ds2,
            """"2020-01-01","ES","A",2
"2020-01-02","ES","A",10
""",
            "dt, country, product",
            add_final=True,
        )

        await self.expected_data_in_datasource(
            self.token,
            ds3,
            """"2020-01-01","ES","A-A",2
"2020-01-01","ES","B",1
"2020-01-02","ES","A-A",10
"2020-01-02","ES","B",5
""",
            "dt, country, product",
            add_final=True,
        )

        await self.expected_data_in_datasource(
            self.token,
            ds4,
            """"2020-01-01","ES",3
"2020-01-02","ES",15
""",
            "dt, country",
            add_final=True,
        )

    @tornado.testing.gen_test
    async def test_replace_partial_with_a_join_at_the_end(self):
        """
        +------+  insert/replace   +-----+  MV1to2   +-----+  MV2to3   +----------+
        |  ws  | ----------------> | DS1 | --------> | DS2 | --------> | DS3_join |
        +------+                   +-----+           +-----+           +----------+
        """
        rand = str(uuid.uuid4())[:8]
        ds1 = f"DS1_{rand}"
        await self.create_datasource_async(
            self.token,
            ds1,
            """
                                    dt Date,
                                    country String,
                                    product String,
                                    units Int32
                                """,
            {"engine": "MergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        ds2 = f"DS2_{rand}"
        await self.create_datasource_async(
            self.token,
            ds2,
            """
                                    dt Date,
                                    country String,
                                    product String,
                                    sum_units Int32
                                """,
            {"engine": "SummingMergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds2,
            f"""
                                SELECT
                                    dt,
                                    country,
                                    product,
                                    toInt32(sum(units)) AS sum_units
                                FROM {ds1}
                                GROUP BY dt, country, product
                                """,
            pipe_name="MV1to2",
        )
        ds3 = f"DS3_{rand}"
        await self.create_datasource_async(
            self.token,
            ds3,
            """
                                    dt Date,
                                    sum_units Int32
                                """,
            {"engine": "Join", "engine_join_strictness": "ANY", "engine_join_type": "LEFT", "engine_key_columns": "dt"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds3,
            f"""
                                SELECT
                                    dt,
                                    toInt32(sum(sum_units)) AS sum_units
                                FROM {ds2}
                                GROUP BY dt
                                """,
            pipe_name="MV2to3",
        )

        await self.replace_data_with_condition_to_datasource(
            self.token,
            ds1,
            "1=1",
            CsvIO(  # FIXME using a replace condition is a *hack*
                "2020-01-01,ES,A,1",
                "2020-01-01,ES,A,1",
                "2020-01-01,ES,B,1",
                "2020-01-02,ES,A,1",
                "2020-01-02,ES,A,1",
                "2020-01-02,ES,B,1",
            ),
        )
        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": ds2,
                "options": {
                    "replace_condition": "1=1",
                },
            }
        )
        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": ds3,
                "options": {
                    "replace_condition": "1=1",
                },
            }
        )
        await self.expected_data_in_datasource(
            self.token,
            ds1,
            """"2020-01-01","ES","A",1
"2020-01-01","ES","A",1
"2020-01-01","ES","B",1
"2020-01-02","ES","A",1
"2020-01-02","ES","A",1
"2020-01-02","ES","B",1
""",
            "dt, country, product",
        )
        await self.expected_data_in_datasource(
            self.token,
            ds2,
            """"2020-01-01","ES","A",2
"2020-01-01","ES","B",1
"2020-01-02","ES","A",2
"2020-01-02","ES","B",1
""",
            "dt, country, product",
            add_final=True,
        )
        await self.expected_data_in_datasource(
            self.token,
            ds3,
            """"2020-01-01",3
"2020-01-02",3
""",
        )
        extra_expected_ops_logs = [
            {
                "event_type": "replace",
                "datasource_name": ds2,
                "options": {
                    "replace_condition": "dt = '2020-01-02'",
                },
            },
            {
                "event_type": "replace",
                "datasource_name": ds3,
                "options": {
                    "replace_condition": "dt = '2020-01-02'",
                },
            },
        ]
        await self.replace_with_data_in_sql_async(
            self.token,
            ds1,
            "dt = '2020-01-02'",
            """
        SELECT row[1], row[2], row[3], row[4]
        FROM ( SELECT arrayJoin([
        ['2020-01-02', 'ES', 'A', '5'],
        ['2020-01-02', 'ES', 'A', '5'],
        ['2020-01-02', 'ES', 'B', '5']
        ]) as row) format CSV;
""",
            expect_logs=True,
            extra_expected_ops_logs=extra_expected_ops_logs,
        )

        await self.expected_data_in_datasource(
            self.token,
            ds1,
            """"2020-01-01","ES","A",1
"2020-01-01","ES","A",1
"2020-01-01","ES","B",1
"2020-01-02","ES","A",5
"2020-01-02","ES","A",5
"2020-01-02","ES","B",5
""",
            "dt, country, product",
        )
        await self.expected_data_in_datasource(
            self.token,
            ds2,
            """"2020-01-01","ES","A",2
"2020-01-01","ES","B",1
"2020-01-02","ES","A",10
"2020-01-02","ES","B",5
""",
            "dt, country, product",
            add_final=True,
        )

        await self.expected_data_in_datasource(
            self.token,
            ds3,
            """"2020-01-01",3
"2020-01-02",15
""",
        )

    @pytest.mark.skip("Send a replace operation to a Join table not supported.")
    @tornado.testing.gen_test
    async def test_replace_partial_starting_in_a_join_table(self):
        """
        +------+  insert/replace   +----------+     MV1to2    +----------+
        |  ws  | ----------------> | DS1_join | ------------> | DS3_join |
        +------+                   +----------+               +----------+
        """
        rand = str(uuid.uuid4())[:8]
        ds1 = f"DS1_{rand}"
        await self.create_datasource_async(
            self.token,
            ds1,
            """
                                    dt Date,
                                    product String
                                """,
            {"engine": "Join", "engine_join_strictness": "ANY", "engine_join_type": "LEFT", "engine_key_columns": "dt"},
        )

        ds2 = f"DS2_{rand}"
        await self.create_datasource_async(
            self.token,
            ds2,
            """
                                    dt Date,
                                    product String
                                """,
            {"engine": "Join", "engine_join_strictness": "ANY", "engine_join_type": "LEFT", "engine_key_columns": "dt"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds2,
            f"""
                                SELECT
                                    dt,
                                    concat(product, '-A') as product
                                FROM {ds1}
                                """,
            pipe_name="MV1to2",
        )

        await self.replace_data_with_condition_to_datasource(
            self.token,
            ds1,
            "1=1",
            CsvIO(
                "2020-01-01,A",
                "2020-01-02,A",
            ),
        )

        await self.expected_data_in_datasource(
            self.token,
            ds1,
            """"2020-01-01","A"
"2020-01-02","A"
""",
        )
        await self.expected_data_in_datasource(
            self.token,
            ds2,
            """"2020-01-01","A-A"
"2020-01-02","A-A"
""",
        )

        await self.replace_with_data_in_sql_async(
            self.token,
            ds1,
            "dt = '2020-01-02'",
            """
        SELECT row[1], row[2]
        FROM ( SELECT arrayJoin([

        ['2020-01-02', 'B']
        ]) as row) format CSV;
""",
        )

        await self.expected_data_in_datasource(
            self.token,
            ds1,
            """"2020-01-01","A"
"2020-01-02","B"
""",
        )
        await self.expected_data_in_datasource(
            self.token,
            ds2,
            """"2020-01-01","A-A"
"2020-01-02","B"
""",
        )


class TestAPIDatasourceHooksReplacePartialBatch5(TestAPIDatasourceHooksReplacePartialBase):
    @tornado.testing.gen_test
    async def test_replace_partial_reaches_joins_and_data_is_replaced_in_all_cluster_instances(self):
        """
        +------+  insert/replace   +-----+  MV1to2   +----------+  MV2to3   +----------+
        |  ws  | ----------------> | DS1 | --------> | DS2_join | --------> | DS3_join |
        +------+                   +-----+           +----------+           +----------+
        """

        replicas = await ch_get_cluster_instances(self.u.database_server, self.u.database, "tinybird")
        replicas_for_cluster = list(filter(lambda replica: replica[1] == self.u.cluster, replicas))
        rand = str(uuid.uuid4())[:8]
        ds1 = f"DS1_{rand}"
        await self.create_datasource_async(
            self.token,
            ds1,
            """
                                    dt Date,
                                    country String,
                                    product String,
                                    units Int32
                                """,
            {"engine": "MergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        ds2 = f"DS2_join_{rand}"
        ds2_meta = await self.create_datasource_async(
            self.token,
            ds2,
            """
                                    dt Date,
                                    product String,
                                    sum_units Int32
                                """,
            {"engine": "Join", "engine_join_strictness": "ANY", "engine_join_type": "LEFT", "engine_key_columns": "dt"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds2,
            f"""
                                SELECT
                                    dt,
                                    product,
                                    toInt32(sum(units)) AS sum_units
                                FROM {ds1}
                                GROUP BY dt, product
                                """,
            pipe_name="MV1to2",
        )

        ds3 = f"DS3_join_{rand}"
        ds3_meta = await self.create_datasource_async(
            self.token,
            ds3,
            """
                                    dt Date,
                                    product String
                                """,
            {"engine": "Join", "engine_join_strictness": "ANY", "engine_join_type": "LEFT", "engine_key_columns": "dt"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds3,
            f"""
                                SELECT
                                    dt,
                                    concat(product, '-A') as product
                                FROM {ds2}
                                """,
            pipe_name="MV2to3",
        )

        await self.replace_data_to_datasource(
            self.token,
            ds1,
            CsvIO(
                "2020-01-01,ES,A,1",
                "2020-01-01,ES,A,1",
                "2020-01-02,ES,A,1",
                "2020-01-02,ES,A,1",
            ),
        )

        def expected_data_replicated_in_datasource(database, datasource_id, data):
            sql = f"SELECT * FROM {database}.{datasource_id} FORMAT CSV"

            for replica in replicas_for_cluster:
                res = HTTPClient(replica[0], self.u.database).query_sync(sql)
                data_returned = res[1].decode()
                self.assertEqual(data_returned, data)

        await self.expected_data_in_datasource(
            self.token,
            ds1,
            """"2020-01-01","ES","A",1
"2020-01-01","ES","A",1
"2020-01-02","ES","A",1
"2020-01-02","ES","A",1
""",
            "dt, country, product",
        )

        await self.expected_data_in_datasource(
            self.token,
            ds2,
            """"2020-01-01","A",2
"2020-01-02","A",2
""",
        )
        await self.expected_data_in_datasource(
            self.token,
            ds3,
            """"2020-01-01","A-A"
"2020-01-02","A-A"
""",
        )
        extra_expected_ops_logs = [
            {
                "event_type": "replace",
                "datasource_name": ds2,
                "options": {
                    "source": "full_body",
                },
            },
            {
                "event_type": "replace",
                "datasource_name": ds2,
                "options": {
                    "replace_condition": "dt = '2020-01-02'",
                },
            },
            {
                "event_type": "replace",
                "datasource_name": ds3,
                "options": {
                    "source": "full_body",
                },
            },
            {
                "event_type": "replace",
                "datasource_name": ds3,
                "options": {
                    "replace_condition": "dt = '2020-01-02'",
                },
            },
        ]

        await self.replace_with_data_in_sql_async(
            self.token,
            ds1,
            "dt = '2020-01-02'",
            """
        SELECT row[1], row[2], row[3], row[4]
        FROM ( SELECT arrayJoin([
        ['2020-01-02', 'ES', 'B', '5'],
        ['2020-01-02', 'ES', 'B', '5']
        ]) as row) format CSV;
""",
            extra_expected_ops_logs=extra_expected_ops_logs,
            expect_logs=True,
        )

        expected_data_replicated_in_datasource(
            self.u.database,
            ds2_meta["datasource"]["id"],
            """"2020-01-01","A",2
"2020-01-02","B",10
""",
        )
        await self.expected_data_in_datasource(
            self.token,
            ds2,
            """"2020-01-01","A",2
"2020-01-02","B",10
""",
        )

        expected_data_replicated_in_datasource(
            self.u.database,
            ds3_meta["datasource"]["id"],
            """"2020-01-01","A-A"
"2020-01-02","B-A"
""",
        )
        await self.expected_data_in_datasource(
            self.token,
            ds3,
            """"2020-01-01","A-A"
"2020-01-02","B-A"
""",
        )

    @tornado.testing.gen_test
    async def test_replace_partial_with_a_shared_mv_down_the_line(self):
        """
        +------+  insert/replace   +-----+  MV1to2   +-----+  MV2to3   +-----+
        |  ws  | ----------------> | DS1 | --------> | DS2 | --------> | DS3 |
        +------+                   +-----+           +-----+           +-----+
        - DS2 is shared
        - MV2to3 and DS3 lives in the other Workspace.
        """
        rand = str(uuid.uuid4())[:8]
        user_a = UserAccount.get_by_id(self.USER_ID)
        token_user_a = UserAccount.get_token_for_scope(user_a, scopes.AUTH)

        ws_b_name = f"user_b_partial_{uuid.uuid4().hex}"
        workspace_b = await self.tb_api_proxy_async.register_user_and_workspace(f"{ws_b_name}@example.com", ws_b_name)
        user_b = UserAccount.get_by_email(f"{ws_b_name}@example.com")
        token_workspace_b = Users.get_token_for_scope(workspace_b, scopes.ADMIN)
        token_user_b = UserAccount.get_token_for_scope(user_b, scopes.AUTH)
        ds1 = f"DS1_{rand}"
        await self.create_datasource_async(
            self.token,
            ds1,
            """
                                    dt Date,
                                    country String,
                                    product String,
                                    units Int32
                                """,
            {"engine": "MergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        ds2 = f"DS2_{rand}"
        ds2_meta = await self.create_datasource_async(
            self.token,
            ds2,
            """
                                    dt Date,
                                    country String,
                                    product String,
                                    sum_units Int32
                                """,
            {"engine": "SummingMergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds2,
            f"""
                                SELECT
                                    dt,
                                    country,
                                    product,
                                    toInt32(sum(units)) AS sum_units
                                FROM {ds1}
                                GROUP BY dt, country, product
                                """,
            pipe_name="MV1to2",
        )

        await self.tb_api_proxy_async.invite_user_to_workspace(
            token=token_user_b, workspace_id=workspace_b.id, user_to_invite_email=user_a.email
        )

        await self.tb_api_proxy_async.share_datasource_with_another_workspace(
            token=token_user_a,
            datasource_id=ds2_meta["datasource"]["id"],
            origin_workspace_id=self.WORKSPACE_ID,
            destination_workspace_id=workspace_b.id,
        )

        ds3 = f"DS3_{rand}"
        await self.create_datasource_async(
            token_workspace_b,
            ds3,
            """
                                    dt Date,
                                    country String,
                                    product String,
                                    sum_units Int32
                                """,
            {"engine": "SummingMergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
            expect_ops_log=False,
        )

        await self.create_view_async(
            workspace_b,
            token_workspace_b,
            ds3,
            f"""
                                SELECT
                                    dt,
                                    country,
                                    product,
                                    toInt32(sum(sum_units)) AS sum_units
                                FROM {self.u.name}.{ds2}
                                GROUP BY dt, country, product
                                """,
            pipe_name="MV2to3",
        )

        await self.append_data_to_datasource(
            self.token,
            ds1,
            CsvIO(
                "2020-01-01,ES,A,1",
                "2020-01-01,ES,A,1",
                "2020-01-01,ES,B,1",
                "2020-01-02,ES,A,1",
                "2020-01-02,ES,A,1",
                "2020-01-02,ES,B,1",
            ),
        )

        self.expect_ops_log([{"event_type": "append", "datasource_name": ds2}])

        await self.expected_data_in_datasource(
            self.token,
            ds1,
            """"2020-01-01","ES","A",1
"2020-01-01","ES","A",1
"2020-01-01","ES","B",1
"2020-01-02","ES","A",1
"2020-01-02","ES","A",1
"2020-01-02","ES","B",1
""",
            "dt, country, product",
        )
        await self.expected_data_in_datasource(
            self.token,
            ds2,
            """"2020-01-01","ES","A",2
"2020-01-01","ES","B",1
"2020-01-02","ES","A",2
"2020-01-02","ES","B",1
""",
            "dt, country, product",
            add_final=True,
        )

        await self.expected_data_in_datasource(
            token_workspace_b,
            ds3,
            """"2020-01-01","ES","A",2
"2020-01-01","ES","B",1
"2020-01-02","ES","A",2
"2020-01-02","ES","B",1
""",
            "dt, country, product",
            add_final=True,
        )
        extra_expected_ops_logs = [
            {
                "event_type": "replace",
                "datasource_name": ds1,
                "rows": 6,
                "written_rows": 6,
                "written_bytes": 162,
                "written_rows_quarantine": 0,
                "written_bytes_quarantine": 0,
            },
            {
                "event_type": "replace",
                "datasource_name": ds2,
                "rows": 4,
                "written_rows": 0,
                "written_bytes": 0,
                "written_rows_quarantine": 0,
                "written_bytes_quarantine": 0,
            },
        ]
        await self.replace_with_data_in_sql_async(
            self.token,
            ds1,
            "dt = '2020-01-02'",
            """
        SELECT row[1], row[2], row[3], row[4]
        FROM ( SELECT arrayJoin([
        ['2020-01-02', 'ES', 'A', '5'],
        ['2020-01-02', 'ES', 'A', '5'],
        ['2020-01-02', 'ES', 'B', '5']
        ]) as row) format CSV;
""",
            expect_logs=False,
            extra_expected_ops_logs=extra_expected_ops_logs,
        )

        await self.expected_data_in_datasource(
            self.token,
            ds1,
            """"2020-01-01","ES","A",1
"2020-01-01","ES","A",1
"2020-01-01","ES","B",1
"2020-01-02","ES","A",5
"2020-01-02","ES","A",5
"2020-01-02","ES","B",5
""",
            "dt, country, product",
        )
        await self.expected_data_in_datasource(
            self.token,
            ds2,
            """"2020-01-01","ES","A",2
"2020-01-01","ES","B",1
"2020-01-02","ES","A",10
"2020-01-02","ES","B",5
""",
            "dt, country, product",
            add_final=True,
        )
        self.expect_ops_log({"event_type": "create", "datasource_name": ds3}, workspace=workspace_b)
        self.expect_ops_log({"event_type": "append", "datasource_name": ds3}, workspace=workspace_b)
        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": ds3,
                "written_rows": 0,
                "written_bytes": 0,
                "written_rows_quarantine": 0,
                "written_bytes_quarantine": 0,
            },
            workspace=workspace_b,
        )
        await self.expected_data_in_datasource(
            token_workspace_b,
            ds3,
            """"2020-01-01","ES","A",2
"2020-01-01","ES","B",1
"2020-01-02","ES","A",10
"2020-01-02","ES","B",5
""",
            "dt, country, product",
            add_final=True,
        )

    @tornado.testing.gen_test
    async def test_replace_partial_with_skip_option_will_ignore_tables_with_different_partition(self):
        """
        +------+  insert/replace   +---------+  MV1to2   +-----+  MV2to3   +-----+
        |  ws  | ----------------> |   DS1   | --------> | DS2 | --------> | DS3 |
        +------+                   +---------+           +-----+           +-----+
        - DS3 with different partition.
        """
        rand = str(uuid.uuid4())[:8]
        ds1 = f"DS1_{rand}"
        await self.create_datasource_async(
            self.token,
            ds1,
            """
                dt Date,
                country String,
                product String,
                units Int32
            """,
            {"engine": "MergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        ds2 = f"DS2_{rand}"
        await self.create_datasource_async(
            self.token,
            ds2,
            """
                dt Date,
                country String,
                product String,
                sum_units Int32
            """,
            {"engine": "SummingMergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds2,
            f"""
            SELECT
                dt,
                country,
                product,
                toInt32(sum(units)) AS sum_units
            FROM {ds1}
            GROUP BY dt, country, product
            """,
            pipe_name="MV1to2",
        )

        ds3 = f"DS3_{rand}"
        await self.create_datasource_async(
            self.token,
            ds3,
            """
                dt Date,
                country String,
                sum_per_country Int32
            """,
            {"engine": "SummingMergeTree", "engine_sorting_key": "country, dt"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds3,
            f"""
            SELECT
                dt,
                country,
                toInt32(sum(sum_units)) AS sum_per_country
            FROM {ds2}
            GROUP BY dt, country
            """,
            pipe_name="MV2to3",
        )

        await self.append_data_to_datasource(
            self.token,
            ds1,
            CsvIO(
                "2020-01-01,ES,A,1",
                "2020-01-01,ES,A,1",
                "2020-01-01,ES,B,1",
                "2020-01-02,ES,A,1",
                "2020-01-02,ES,A,1",
                "2020-01-02,ES,B,1",
            ),
        )

        self.expect_ops_log(
            [{"event_type": "append", "datasource_name": ds2}, {"event_type": "append", "datasource_name": ds3}]
        )

        await self.expected_data_in_datasource(
            self.token,
            ds1,
            """"2020-01-01","ES","A",1
"2020-01-01","ES","A",1
"2020-01-01","ES","B",1
"2020-01-02","ES","A",1
"2020-01-02","ES","A",1
"2020-01-02","ES","B",1
""",
            "dt, country, product",
        )
        await self.expected_data_in_datasource(
            self.token,
            ds2,
            """"2020-01-01","ES","A",2
"2020-01-01","ES","B",1
"2020-01-02","ES","A",2
"2020-01-02","ES","B",1
""",
            "dt, country, product",
        )

        await self.expected_data_in_datasource(
            self.token,
            ds3,
            """"2020-01-01","ES",3
"2020-01-02","ES",3
""",
            "dt, country",
        )
        extra_expected_ops_logs = [{"event_type": "replace", "datasource_name": ds2}]
        await self.replace_with_data_in_sql_async(
            self.token,
            ds1,
            "dt = '2020-01-02'",
            """
        SELECT row[1], row[2], row[3], row[4]
        FROM ( SELECT arrayJoin([
        ['2020-01-02', 'ES', 'A', '5'],
        ['2020-01-02', 'ES', 'A', '5'],
        ['2020-01-02', 'ES', 'B', '5']
        ]) as row) format CSV;
        """,
            ["skip_incompatible_partition_key"],
            expect_logs=True,
            extra_expected_ops_logs=extra_expected_ops_logs,
        )

        await self.expected_data_in_datasource(
            self.token,
            ds1,
            """"2020-01-01","ES","A",1
"2020-01-01","ES","A",1
"2020-01-01","ES","B",1
"2020-01-02","ES","A",5
"2020-01-02","ES","A",5
"2020-01-02","ES","B",5
""",
            "dt, country, product",
        )
        await self.expected_data_in_datasource(
            self.token,
            ds2,
            """"2020-01-01","ES","A",2
"2020-01-01","ES","B",1
"2020-01-02","ES","A",10
"2020-01-02","ES","B",5
""",
            "dt, country, product",
        )

        await self.expected_data_in_datasource(
            self.token,
            ds3,
            """"2020-01-01","ES",3
"2020-01-02","ES",3
""",
            "dt, country",
        )

    @tornado.testing.gen_test
    async def test_replace_partial_will_fail_if_there_are_tables_with_different_partition(self):
        """
        +------+  insert/replace   +---------+  MV1to2   +-----+  MV2to3   +-----+
        |  ws  | ----------------> |   DS1   | --------> | DS2 | --------> | DS3 |
        +------+                   +---------+           +-----+           +-----+
        - DS3 with different partition.
        """
        rand = str(uuid.uuid4())[:8]
        ds1 = f"DS1_{rand}"
        await self.create_datasource_async(
            self.token,
            ds1,
            """
                dt Date,
                country String,
                product String,
                units Int32
            """,
            {"engine": "MergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        ds2 = f"DS2_{rand}"
        await self.create_datasource_async(
            self.token,
            ds2,
            """
                dt Date,
                country String,
                product String,
                sum_units Int32
            """,
            {"engine": "SummingMergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds2,
            f"""
            SELECT
                dt,
                country,
                product,
                toInt32(sum(units)) AS sum_units
            FROM {ds1}
            GROUP BY dt, country, product
            """,
            pipe_name="MV1to2",
        )

        ds3 = f"DS3_{rand}"
        await self.create_datasource_async(
            self.token,
            ds3,
            """
                dt Date,
                country String,
                sum_per_country Int32
            """,
            {"engine": "SummingMergeTree", "engine_sorting_key": "country, dt"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds3,
            f"""
            SELECT
                dt,
                country,
                toInt32(sum(sum_units)) AS sum_per_country
            FROM {ds2}
            GROUP BY dt, country
            """,
            pipe_name="MV2to3",
        )

        await self.append_data_to_datasource(
            self.token,
            ds1,
            CsvIO(
                "2020-01-01,ES,A,1",
                "2020-01-01,ES,A,1",
                "2020-01-01,ES,B,1",
                "2020-01-02,ES,A,1",
                "2020-01-02,ES,A,1",
                "2020-01-02,ES,B,1",
            ),
        )

        self.expect_ops_log(
            [{"event_type": "append", "datasource_name": ds2}, {"event_type": "append", "datasource_name": ds3}]
        )

        result = await self.replace_with_data_in_sql_async(
            self.token,
            ds1,
            "dt = '2020-01-02'",
            """
        SELECT row[1], row[2], row[3], row[4]
        FROM ( SELECT arrayJoin([
        ['2020-01-02', 'ES', 'A', '5'],
        ['2020-01-02', 'ES', 'A', '5'],
        ['2020-01-02', 'ES', 'B', '5']
        ]) as row) format CSV;
        """,
            expect_error=True,
        )

        self.assertIn(
            f"Error when running after import tasks on job {result['job_id']}: Partial replace can't be executed as at least one of the Data Sources involved (DS3_{rand}) has incompatible partitions. Check the PARTITION KEY is present and it's the same in both Data Sources. e.g. both Data Sources are partitions using toYYYYMM or toDate, as opposed to one having toYYMMMM and the other tuple(). If you want to ignore all the Data Sources with incompatible partitions in the replace operation, please use the option 'skip_incompatible_partition_key' to skip them.",
            result["errors"],
        )

    @tornado.testing.gen_test
    async def test_replace_partial_supported_with_null_tables_but_does_nothing(self):
        """
        Partial replaces starting on a DS with a Null() engine will return 200 but will fnot replace anything.

        +------+  insert/replace   +---------+  MV1to2   +-----+  MV2to3   +-----+
        |  ws  | ----------------> |   DS1   | --------> | DS2 | --------> | DS3 |
        +------+                   +---------+           +-----+           +-----+
        - DS1 has Null() engine
        """
        rand = str(uuid.uuid4())[:8]
        ds1 = f"DS1_{rand}"
        await self.create_datasource_async(
            self.token,
            ds1,
            """
                dt Date,
                country String,
                product String,
                units Int32
            """,
            {"engine": "Null"},
        )

        ds2 = f"DS2_{rand}"
        await self.create_datasource_async(
            self.token,
            ds2,
            """
                dt Date,
                country String,
                product String,
                sum_units Int32
            """,
            {"engine": "SummingMergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds2,
            f"""
            SELECT
                dt,
                country,
                product,
                toInt32(sum(units)) AS sum_units
            FROM {ds1}
            GROUP BY dt, country, product
            """,
        )

        ds3 = f"DS3_{rand}"
        await self.create_datasource_async(
            self.token,
            ds3,
            """
                dt Date,
                country String,
                sum_per_country Int32
            """,
            {"engine": "SummingMergeTree", "engine_sorting_key": "country, dt"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds3,
            f"""
            SELECT
                dt,
                country,
                toInt32(sum(sum_units)) AS sum_per_country
            FROM {ds2}
            GROUP BY dt, country
            """,
        )

        await self.append_data_to_datasource(
            self.token,
            ds1,
            CsvIO(
                "2020-01-01,ES,A,1",
                "2020-01-01,ES,A,1",
                "2020-01-01,ES,B,1",
                "2020-01-02,ES,A,1",
                "2020-01-02,ES,A,1",
                "2020-01-02,ES,B,1",
            ),
        )

        u = Users.get_by_id(self.WORKSPACE_ID)
        ds2_id = Users.get_datasource(u, ds2).id
        self.wait_for_datasource_replication(u, ds2_id)

        ds3_id = Users.get_datasource(u, ds3).id
        self.wait_for_datasource_replication(u, ds3_id)

        self.expect_ops_log(
            [{"event_type": "append", "datasource_name": ds2}, {"event_type": "append", "datasource_name": ds3}]
        )

        await self.expected_data_in_datasource(
            self.token,
            ds2,
            """"2020-01-01","ES","A",2
"2020-01-01","ES","B",1
"2020-01-02","ES","A",2
"2020-01-02","ES","B",1
""",
            "dt, country, product",
        )

        await self.expected_data_in_datasource(
            self.token,
            ds3,
            """"2020-01-01","ES",3
"2020-01-02","ES",3
""",
            "dt, country",
        )

        # Replace day 2020-01-02
        await self.replace_data_with_condition_to_datasource(
            self.token,
            ds1,
            "dt = '2020-01-02'",
            CsvIO(
                "2020-01-02,ES,A,5",
                "2020-01-02,ES,A,5",
                "2020-01-02,ES,B,5",
            ),
        )

        await self.expected_data_in_datasource(
            self.token,
            ds2,
            """"2020-01-01","ES","A",2
"2020-01-01","ES","B",1
"2020-01-02","ES","A",2
"2020-01-02","ES","B",1
""",
            "dt, country, product",
        )

        await self.expected_data_in_datasource(
            self.token,
            ds3,
            """"2020-01-01","ES",3
"2020-01-02","ES",3
""",
            "dt, country",
        )

    @tornado.testing.gen_test
    async def test_cascade_supported_for_full_body_imports(self):
        """
        +------+  insert/replace   +---------+  MV1to2   +-----+  MV2to3   +-----+
        |  ws  | ----------------> |   DS1   | --------> | DS2 | --------> | DS3 |
        +------+                   +---------+           +-----+           +-----+
        - Replace done with a full-body import.
        """
        rand = str(uuid.uuid4())[:8]
        ds1 = f"DS1_{rand}"
        await self.create_datasource_async(
            self.token,
            ds1,
            """
                dt Date,
                country String,
                product String,
                units Int32
            """,
            {"engine": "MergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        ds2 = f"DS2_{rand}"
        await self.create_datasource_async(
            self.token,
            ds2,
            """
                dt Date,
                country String,
                product String,
                sum_units Int32
            """,
            {"engine": "SummingMergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds2,
            f"""
            SELECT
                dt,
                country,
                product,
                toInt32(sum(units)) AS sum_units
            FROM {ds1}
            GROUP BY dt, country, product
            """,
            pipe_name="MV1to2",
        )

        ds3 = f"DS3_{rand}"
        await self.create_datasource_async(
            self.token,
            ds3,
            """
                dt Date,
                country String,
                sum_per_country Int32
            """,
            {"engine": "SummingMergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds3,
            f"""
            SELECT
                dt,
                country,
                toInt32(sum(sum_units)) AS sum_per_country
            FROM {ds2}
            GROUP BY dt, country
            """,
            pipe_name="MV2to3",
        )

        extra_expected_ops_logs = [
            {"event_type": "replace", "datasource_name": ds2},
            {"event_type": "replace", "datasource_name": ds3},
        ]

        await self.append_data_to_datasource(
            self.token,
            ds1,
            CsvIO(
                "2020-01-01,ES,A,1",
                "2020-01-01,ES,A,1",
                "2020-01-01,ES,B,1",
                "2020-01-02,ES,A,1",
                "2020-01-02,ES,A,1",
                "2020-01-02,ES,B,1",
            ),
            extra_expected_ops_logs=extra_expected_ops_logs,
        )

        self.expect_ops_log(
            [{"event_type": "append", "datasource_name": ds2}, {"event_type": "append", "datasource_name": ds3}]
        )

        ds2_id = Users.get_datasource(self.u, ds2).id
        self.wait_for_datasource_replication(self.u, ds2_id)
        ds3_id = Users.get_datasource(self.u, ds3).id
        self.wait_for_datasource_replication(self.u, ds3_id)

        await self.expected_data_in_datasource(
            self.token,
            ds1,
            """"2020-01-01","ES","A",1
"2020-01-01","ES","A",1
"2020-01-01","ES","B",1
"2020-01-02","ES","A",1
"2020-01-02","ES","A",1
"2020-01-02","ES","B",1
""",
            "dt, country, product",
        )
        await self.expected_data_in_datasource(
            self.token,
            ds2,
            """"2020-01-01","ES","A",2
"2020-01-01","ES","B",1
"2020-01-02","ES","A",2
"2020-01-02","ES","B",1
""",
            "dt, country, product",
        )
        await self.expected_data_in_datasource(
            self.token,
            ds3,
            """"2020-01-01","ES",3
"2020-01-02","ES",3
""",
            "dt, country",
        )
        await self.replace_data_with_condition_to_datasource(
            self.token,
            ds1,
            "dt = '2020-01-02'",
            CsvIO(
                "2020-01-02,ES,A,5",
                "2020-01-02,ES,A,5",
                "2020-01-02,ES,B,5",
            ),
        )

        await self.expected_data_in_datasource(
            self.token,
            ds1,
            """"2020-01-01","ES","A",1
"2020-01-01","ES","A",1
"2020-01-01","ES","B",1
"2020-01-02","ES","A",5
"2020-01-02","ES","A",5
"2020-01-02","ES","B",5
""",
            "dt, country, product",
        )
        await self.expected_data_in_datasource(
            self.token,
            ds2,
            """"2020-01-01","ES","A",2
"2020-01-01","ES","B",1
"2020-01-02","ES","A",10
"2020-01-02","ES","B",5
""",
            "dt, country, product",
        )
        await self.expected_data_in_datasource(
            self.token,
            ds3,
            """"2020-01-01","ES",3
"2020-01-02","ES",15
""",
            "dt, country",
        )

    @tornado.testing.gen_test
    async def test_cascade_supported_for_stream_imports(self):
        rand = str(uuid.uuid4())[:8]
        ds1 = f"DS1_{rand}"
        await self.create_datasource_async(
            self.token,
            ds1,
            """
                dt Date,
                country String,
                product String,
                units Int32
            """,
            {"engine": "MergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        ds2 = f"DS2_{rand}"
        await self.create_datasource_async(
            self.token,
            ds2,
            """
                dt Date,
                country String,
                product String,
                sum_units Int32
            """,
            {"engine": "SummingMergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds2,
            f"""
            SELECT
                dt,
                country,
                product,
                toInt32(sum(units)) AS sum_units
            FROM {ds1}
            GROUP BY dt, country, product
            """,
            pipe_name="MV1to2",
        )

        ds3 = f"DS3_{rand}"
        await self.create_datasource_async(
            self.token,
            ds3,
            """
                dt Date,
                country String,
                sum_per_country Int32
            """,
            {"engine": "SummingMergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds3,
            f"""
            SELECT
                dt,
                country,
                toInt32(sum(sum_units)) AS sum_per_country
            FROM {ds2}
            GROUP BY dt, country
            """,
            pipe_name="MV2to3",
        )
        # Append data:
        params = {
            "token": self.token,
            "mode": "append",
            "name": ds1,
        }
        replace_url = self.get_url(f"/v0/datasources?{urlencode(params)}")
        with fixture_file("replace_simple_base_data.csv", mode="rb") as fd:
            response = await self.fetch_stream_upload_async(replace_url, fd)
        self.assertEqual(response.code, 200, response.body)
        self.expect_ops_log({"event_type": "append", "datasource_name": ds1, "options": {"source": "stream"}})

        self.expect_ops_log(
            [{"event_type": "append", "datasource_name": ds2}, {"event_type": "append", "datasource_name": ds3}]
        )

        # Replace operation
        params = {"token": self.token, "mode": "replace", "replace_condition": "dt = '2020-01-02'", "name": ds1}
        replace_url = self.get_url(f"/v0/datasources?{urlencode(params)}")
        with fixture_file("replace_simple_data_replaced.csv", mode="rb") as fd:
            response = await self.fetch_stream_upload_async(replace_url, fd)
        self.assertEqual(response.code, 200, response.body)
        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": ds1,
                "options": {
                    "source": "stream",
                    "replace_condition": "dt = '2020-01-02'",
                },
            }
        )
        self.expect_ops_log({"event_type": "replace", "datasource_name": ds2})
        self.expect_ops_log({"event_type": "replace", "datasource_name": ds3})

        await self.expected_data_in_datasource(
            self.token,
            ds1,
            """"2020-01-01","ES","A",1
"2020-01-01","ES","A",1
"2020-01-01","ES","B",1
"2020-01-02","ES","A",5
"2020-01-02","ES","A",5
"2020-01-02","ES","B",5
""",
            "dt, country, product",
        )

        await self.expected_data_in_datasource(
            self.token,
            ds2,
            """"2020-01-01","ES","A",2
"2020-01-01","ES","B",1
"2020-01-02","ES","A",10
"2020-01-02","ES","B",5
""",
            "dt, country, product",
        )

        await self.expected_data_in_datasource(
            self.token,
            ds3,
            """"2020-01-01","ES",3
"2020-01-02","ES",15
""",
            "dt, country",
        )


class TestAPIDatasourceHooksReplaceCompleteBase(TestAPIDatasourceBase):
    def setUp(self):
        super().setUp()
        u = Users.get_by_id(self.WORKSPACE_ID)
        self.user_account = UserAccounts.get_by_id(self.USER_ID)
        self.u = Users.get_by_id(self.WORKSPACE_ID)
        self.token = Users.get_token_for_scope(u, scopes.ADMIN)


class TestAPIDatasourceHooksReplaceCompleteBatch1(TestAPIDatasourceHooksReplaceCompleteBase):
    @tornado.testing.gen_test
    async def test_full_replace_cascade_happy_one_level(self):
        """
        +------+  insert/replace   +-----+  MV1to2   +-----+
        |  ws  | ----------------> | DS1 | --------> | DS2 |
        +------+                   +-----+           +-----+
        """
        rand = str(uuid.uuid4())[:8]
        ds1 = f"DS1_{rand}"
        ds2 = f"DS2_{rand}"
        mv1 = f"MV1to2_{rand}"

        await self.create_datasource_async(
            self.token,
            ds1,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        ds1_datasource = Users.get_datasource(self.u, ds1)

        await self.create_datasource_async(
            self.token,
            ds2,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds2,
            f"""
                SELECT
                    id,
                    timestamp,
                    category
                FROM {ds1}
                WHERE category = 'B'
            """,
            pipe_name=mv1,
        )

        async def _test_expected():
            await self.expected_data_in_datasource(
                self.token,
                ds1,
                """1,"2020-01-01","A"
1,"2020-01-01","B"
1,"2020-01-02","A"
1,"2020-01-02","B"
""",
            )

            await self.expected_data_in_datasource(
                self.token,
                ds2,
                """1,"2020-01-01","B"
1,"2020-01-02","B"
""",
            )

            self.expect_ops_log(
                {
                    "event_type": "replace",
                    "datasource_name": ds1,
                    "rows": 2,
                    "written_rows": 4,
                    "written_bytes": 64,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                }
            )

            self.expect_ops_log(
                {
                    "event_type": "replace",
                    "rows": 2,
                    "written_rows": 0,
                    "written_bytes": 0,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "datasource_name": ds2,
                    "options": {"replace_origin_datasource": ds1_datasource.id, "replace_origin_workspace": self.u.id},
                }
            )

        # 1. Initial replace

        await self.replace_data_to_datasource(
            self.token,
            ds1,
            CsvIO("1,2020-01-01,A", "1,2020-01-01,B", "1,2020-01-02,A", "1,2020-01-02,B"),
            expect_logs=False,
        )

        await _test_expected()

        # 2. Replace after append

        await self.append_data_to_datasource(
            self.token,
            ds1,
            CsvIO(
                "1,2020-01-01,A",
                "1,2020-01-01,A",
                "1,2020-01-01,B",
                "8,2020-01-01,B",
                "8,2020-01-02,B",
                "9,2020-03-02,B",
                "1,2020-01-02,A",
                "5,2020-01-02,A",
                "1,2020-01-02,B",
            ),
        )

        self.expect_ops_log({"event_type": "append", "datasource_name": ds2})

        await self.replace_data_to_datasource(
            self.token,
            ds1,
            CsvIO("1,2020-01-01,A", "1,2020-01-01,B", "1,2020-01-02,A", "1,2020-01-02,B"),
            expect_logs=False,
        )

        await _test_expected()

    @tornado.testing.gen_test
    async def test_full_replace_cascade_happy_one_level_not_allow_truncate_when_empty_is_false(self):
        """
        +------+  insert/replace   +-----+  MV1to2   +-----+
        |  ws  | ----------------> | DS1 | --------> | DS2 |
        +------+                   +-----+           +-----+
        """
        rand = str(uuid.uuid4())[:8]
        ds1 = f"DS1_{rand}"
        ds2 = f"DS2_{rand}"
        mv1 = f"MV1to2_{rand}"

        await self.create_datasource_async(
            self.token,
            ds1,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        ds1_datasource = Users.get_datasource(self.u, ds1)

        await self.create_datasource_async(
            self.token,
            ds2,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds2,
            f"""
                SELECT
                    id,
                    timestamp,
                    category
                FROM {ds1}
                WHERE category = 'B'
            """,
            pipe_name=mv1,
        )

        async def _test_expected(cascade, d1_rows, d1_written_rows, d1_written_bytes, d1_rows_before_replace):
            await self.expected_data_in_datasource(
                self.token,
                ds1,
                """1,"2020-01-01","A"
1,"2020-01-01","B"
1,"2020-01-02","A"
1,"2020-01-02","B"
""",
                order_by_columns="id, timestamp, category",
            )

            await self.expected_data_in_datasource(
                self.token,
                ds2,
                """1,"2020-01-01","B"
1,"2020-01-02","B"
""",
                order_by_columns="id, timestamp, category",
            )

            self.expect_ops_log(
                {
                    "event_type": "replace",
                    "datasource_name": ds1,
                    "rows": d1_rows,
                    "written_rows": d1_written_rows,
                    "written_bytes": d1_written_bytes,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "options": {"rows_before_replace": d1_rows_before_replace},
                }
            )

            if not cascade:
                self.expect_ops_log(
                    {
                        "event_type": "replace",
                        "rows": 2,
                        "written_rows": 0,
                        "written_bytes": 0,
                        "written_rows_quarantine": 0,
                        "written_bytes_quarantine": 0,
                        "datasource_name": ds2,
                        "options": {
                            "replace_origin_datasource": ds1_datasource.id,
                            "replace_origin_workspace": self.u.id,
                        },
                    }
                )

        # 1. Initial replace

        await self.replace_data_to_datasource(
            self.token,
            ds1,
            CsvIO("1,2020-01-01,A", "1,2020-01-01,B", "1,2020-01-02,A", "1,2020-01-02,B"),
            expect_logs=False,
            replace_truncate_when_empty=False,
        )

        await _test_expected(False, 2, 4, 64, 0)

        await self.replace_data_to_datasource(
            self.token,
            ds1,
            CsvIO(),
            expect_logs=False,
            replace_truncate_when_empty=False,
        )

        await _test_expected(True, 4, 0, 0, 4)

    @tornado.testing.gen_test
    async def test_full_replace_cascade_happy_one_level_not_allow_truncate_when_empty_is_none(self):
        """
        +------+  insert/replace   +-----+  MV1to2   +-----+
        |  ws  | ----------------> | DS1 | --------> | DS2 |
        +------+                   +-----+           +-----+
        """
        rand = str(uuid.uuid4())[:8]
        ds1 = f"DS1_{rand}"
        ds2 = f"DS2_{rand}"
        mv1 = f"MV1to2_{rand}"

        await self.create_datasource_async(
            self.token,
            ds1,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        ds1_datasource = Users.get_datasource(self.u, ds1)

        await self.create_datasource_async(
            self.token,
            ds2,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds2,
            f"""
                SELECT
                    id,
                    timestamp,
                    category
                FROM {ds1}
                WHERE category = 'B'
            """,
            pipe_name=mv1,
        )

        async def _test_expected(cascade, d1_rows, d1_written_rows, d1_written_bytes, d1_rows_before_replace):
            await self.expected_data_in_datasource(
                self.token,
                ds1,
                """1,"2020-01-01","A"
1,"2020-01-01","B"
1,"2020-01-02","A"
1,"2020-01-02","B"
""",
                order_by_columns="id, timestamp, category",
            )

            await self.expected_data_in_datasource(
                self.token,
                ds2,
                """1,"2020-01-01","B"
1,"2020-01-02","B"
""",
                order_by_columns="id, timestamp, category",
            )

            self.expect_ops_log(
                {
                    "event_type": "replace",
                    "datasource_name": ds1,
                    "rows": d1_rows,
                    "written_rows": d1_written_rows,
                    "written_bytes": d1_written_bytes,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "options": {"rows_before_replace": d1_rows_before_replace},
                }
            )

            if not cascade:
                self.expect_ops_log(
                    {
                        "event_type": "replace",
                        "rows": 2,
                        "written_rows": 0,
                        "written_bytes": 0,
                        "written_rows_quarantine": 0,
                        "written_bytes_quarantine": 0,
                        "datasource_name": ds2,
                        "options": {
                            "replace_origin_datasource": ds1_datasource.id,
                            "replace_origin_workspace": self.u.id,
                        },
                    }
                )

        # 1. Initial replace

        await self.replace_data_to_datasource(
            self.token,
            ds1,
            CsvIO("1,2020-01-01,A", "1,2020-01-01,B", "1,2020-01-02,A", "1,2020-01-02,B"),
            expect_logs=False,
            replace_truncate_when_empty=None,
        )

        await _test_expected(False, 2, 4, 64, 0)

        await self.replace_data_to_datasource(
            self.token,
            ds1,
            CsvIO(),
            expect_logs=False,
            replace_truncate_when_empty=None,
        )

        await _test_expected(True, 4, 0, 0, 4)

    @tornado.testing.gen_test
    async def test_full_replace_cascade_happy_one_level_allow_truncate_when_empty_is_true(self):
        """
        +------+  insert/replace   +-----+  MV1to2   +-----+
        |  ws  | ----------------> | DS1 | --------> | DS2 |
        +------+                   +-----+           +-----+
        """
        rand = str(uuid.uuid4())[:8]
        ds1 = f"DS1_{rand}"
        ds2 = f"DS2_{rand}"
        mv1 = f"MV1to2_{rand}"

        await self.create_datasource_async(
            self.token,
            ds1,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        ds1_datasource = Users.get_datasource(self.u, ds1)

        await self.create_datasource_async(
            self.token,
            ds2,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds2,
            f"""
                SELECT
                    id,
                    timestamp,
                    category
                FROM {ds1}
                WHERE category = 'B'
            """,
            pipe_name=mv1,
        )

        async def _test_expected():
            await self.expected_data_in_datasource(
                self.token,
                ds1,
                "",
            )

            await self.expected_data_in_datasource(
                self.token,
                ds2,
                "",
            )

            self.expect_ops_log(
                {
                    "event_type": "replace",
                    "datasource_name": ds1,
                    "rows": 0,
                    "written_rows": 0,
                    "written_bytes": 0,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                }
            )

            self.expect_ops_log(
                {
                    "event_type": "replace",
                    "rows": 0,
                    "written_rows": 0,
                    "written_bytes": 0,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "datasource_name": ds2,
                    "options": {"replace_origin_datasource": ds1_datasource.id, "replace_origin_workspace": self.u.id},
                }
            )

        # 1. Initial replace

        await self.replace_data_to_datasource(
            self.token,
            ds1,
            CsvIO(),
            expect_logs=False,
            replace_truncate_when_empty=True,
        )

        await _test_expected()

        # 2. Replace after append

        await self.append_data_to_datasource(
            self.token,
            ds1,
            CsvIO(
                "1,2020-01-01,A",
                "1,2020-01-01,A",
                "1,2020-01-01,B",
                "8,2020-01-01,B",
                "8,2020-01-02,B",
                "9,2020-03-02,B",
                "1,2020-01-02,A",
                "5,2020-01-02,A",
                "1,2020-01-02,B",
            ),
        )

        self.expect_ops_log({"event_type": "append", "datasource_name": ds2})

        await self.replace_data_to_datasource(
            self.token,
            ds1,
            CsvIO(),
            expect_logs=False,
            replace_truncate_when_empty=True,
        )

        await _test_expected()

    @tornado.testing.gen_test
    async def test_full_replace_cascade_happy_one_level_ds_mv_created_by_pipe(self):
        """
        +------+  insert/replace   +-----+  MV1to2   +-----+
        |  ws  | ----------------> | DS1 | --------> | DS2 |
        +------+                   +-----+           +-----+
        """

        rand = str(uuid.uuid4())[:8]
        ds1 = f"DS1_{rand}"
        ds2 = f"DS2_{rand}"
        mv1 = f"MV1to2_{rand}"

        await self.create_datasource_async(
            self.token,
            ds1,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        response = await self.fetch_async(
            f"/v0/pipes?token={self.token}",
            method="POST",
            body=json.dumps(
                {
                    "name": mv1,
                    "nodes": [
                        {
                            "name": "mv",
                            "type": "materialized",
                            "sql": f"SELECT category AS c, id AS fake_id FROM {ds1}",
                            "datasource": ds2,
                            "populate": "true",
                        }
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)
        content = json.loads(response.body)
        job = await self.get_finalised_job_async(content["job"]["job_id"])
        self.assertEqual(job["status"], "done")

        ds2_datasource = Users.get_datasource(self.u, ds2)

        self.expect_ops_log(
            {
                "event_type": "create",
                "datasource_name": ds2,
            }
        )

        await self.append_data_to_datasource(
            self.token,
            ds1,
            CsvIO(
                "1,2020-01-01,A",
                "1,2020-01-01,A",
                "1,2020-01-01,B",
                "8,2020-01-01,B",
                "8,2020-01-02,B",
                "9,2020-03-02,B",
                "1,2020-01-02,A",
                "5,2020-01-02,A",
                "1,2020-01-02,B",
            ),
        )

        self.expect_ops_log(
            {
                "event_type": "append",
                "datasource_name": ds2,
            }
        )

        self.expect_ops_log(
            {
                "event_type": "populateview-queued",
                "datasource_name": ds2,
            }
        )

        self.expect_ops_log(
            {
                "event_type": "populateview",
                "datasource_name": ds2,
            }
        )

        await self.replace_data_to_datasource(
            self.token,
            ds1,
            CsvIO("1,2020-01-01,A", "1,2020-01-01,B", "1,2020-01-02,A", "1,2020-01-02,B"),
            expect_logs=False,
        )

        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": ds1,
            }
        )

        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": ds2,
                "pipe_id": ds2_datasource.tags.get("created_by_pipe"),
                "pipe_name": mv1,
            }
        )

    @tornado.testing.gen_test
    async def test_full_replace_cascade_happy_case(self):
        """
        +------+  insert/replace   +-----+  MV1to2   +-----+  MV2to3   +-----+
        |  ws  | ----------------> | DS1 | --------> | DS2 | --------> | DS3 |
        +------+                   +-----+           +-----+           +-----+
        """
        rand = str(uuid.uuid4())[:8]
        ds1 = f"DS1_{rand}"
        ds2 = f"DS2_{rand}"
        ds3 = f"DS3_{rand}"
        mv1 = f"MV1to2_{rand}"
        mv2 = f"MV2to3_{rand}"

        await self.create_datasource_async(
            self.token,
            ds1,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        ds1_datasource = Users.get_datasource(self.u, ds1)

        await self.create_datasource_async(
            self.token,
            ds2,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        await self.create_datasource_async(
            self.token,
            ds3,
            """
                id Int32,
                timestamp Date,
                total UInt64
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds2,
            f"""
                SELECT
                    id,
                    timestamp,
                    category
                FROM {ds1}
                WHERE category = 'B'
            """,
            pipe_name=mv1,
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds3,
            f"""
                SELECT
                    id,
                    timestamp,
                    count() as total
                FROM {ds2}
                GROUP BY id, timestamp
            """,
            pipe_name=mv2,
        )

        async def _test_expected():
            await self.expected_data_in_datasource(
                self.token,
                ds1,
                """1,"2020-01-01","A"
1,"2020-01-01","B"
1,"2020-01-02","A"
1,"2020-01-02","B"
""",
            )

            await self.expected_data_in_datasource(
                self.token,
                ds2,
                """1,"2020-01-01","B"
1,"2020-01-02","B"
""",
            )

            await self.expected_data_in_datasource(
                self.token,
                ds3,
                """1,"2020-01-01",1
1,"2020-01-02",1
""",
            )

            self.expect_ops_log(
                {
                    "event_type": "replace",
                    "datasource_name": ds1,
                    "rows": 2,
                    "written_rows": 4,
                    "written_bytes": 64,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                }
            )

            self.expect_ops_log(
                {
                    "event_type": "replace",
                    "rows": 2,
                    "written_rows": 0,
                    "written_bytes": 0,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "datasource_name": ds2,
                    "options": {"replace_origin_datasource": ds1_datasource.id, "replace_origin_workspace": self.u.id},
                }
            )

            self.expect_ops_log(
                {
                    "event_type": "replace",
                    "datasource_name": ds3,
                    "rows": 2,
                    "written_rows": 0,
                    "written_bytes": 0,
                    "written_rows_quarantine": 0,
                    "written_bytes_quarantine": 0,
                    "options": {"replace_origin_datasource": ds1_datasource.id, "replace_origin_workspace": self.u.id},
                }
            )

        # 1. Initial replace

        await self.replace_data_to_datasource(
            self.token,
            ds1,
            CsvIO("1,2020-01-01,A", "1,2020-01-01,B", "1,2020-01-02,A", "1,2020-01-02,B"),
            expect_logs=False,
        )

        await _test_expected()

        # 2. Replace after append

        await self.append_data_to_datasource(
            self.token,
            ds1,
            CsvIO(
                "1,2020-01-01,A",
                "1,2020-01-01,A",
                "1,2020-01-01,B",
                "8,2020-01-01,B",
                "8,2020-01-02,B",
                "9,2020-03-02,B",
                "1,2020-01-02,A",
                "5,2020-01-02,A",
                "1,2020-01-02,B",
            ),
        )

        self.expect_ops_log(
            [{"event_type": "append", "datasource_name": ds3}, {"event_type": "append", "datasource_name": ds2}]
        )

        await self.replace_data_to_datasource(
            self.token,
            ds1,
            CsvIO("1,2020-01-01,A", "1,2020-01-01,B", "1,2020-01-02,A", "1,2020-01-02,B"),
            expect_logs=False,
        )

        await _test_expected()

    @tornado.testing.gen_test
    async def test_full_replace_cascade_join_id_cast_two_levels(self):
        """
        +------+  insert/replace   +-----+  MV1to2   +-----+  MV2to3  +----------+
        |  ws  | ----------------> | DS1 | --------> | DS2 | -------->| DS3_join |
        +------+                   +-----+           +-----+          +----------+
        """
        rand = str(uuid.uuid4())[:8]
        ds1 = f"DS1_{rand}"
        ds2 = f"DS2_{rand}"
        ds3 = f"DS3_join_{rand}"
        mv1 = f"MV1to2_{rand}"
        mv2 = f"MV2to3_{rand}"

        await self.create_datasource_async(
            self.token,
            ds1,
            """
                id String,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        ds1_datasource = Users.get_datasource(self.u, ds1)

        await self.create_datasource_async(
            self.token,
            ds2,
            """
                id String,
                timestamp Date,
                category String
            """,
            {"engine": "Join", "engine_join_strictness": "ANY", "engine_join_type": "LEFT", "engine_key_columns": "id"},
        )

        await self.create_datasource_async(
            self.token,
            ds3,
            """
                id LowCardinality(String),
                timestamp Date,
                total UInt64
            """,
            {"engine": "Join", "engine_join_strictness": "ANY", "engine_join_type": "LEFT", "engine_key_columns": "id"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds2,
            f"""
                SELECT
                    id,
                    timestamp,
                    category
                FROM {ds1}
                WHERE category != 'B'
            """,
            pipe_name=mv1,
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds3,
            f"""
                SELECT
                    CAST(id, 'LowCardinality(String)') as id,
                    timestamp,
                    count() as total
                FROM {ds2}
                GROUP BY id, timestamp
            """,
            pipe_name=mv2,
        )

        async def _test_expected():
            await self.expected_data_in_datasource(
                self.token,
                ds1,
                """"1","2020-01-01","A"
"1","2020-01-01","B"
"1","2020-01-02","A"
"1","2020-01-02","B"
""",
            )

            await self.expected_data_in_datasource(
                self.token,
                ds2,
                """"1","2020-01-01","A"
""",
            )

            await self.expected_data_in_join_datasource(
                self.token,
                ds3,
                ["timestamp", "total"],
                "1",
                """"2020-01-01",1
""",
            )

            self.expect_ops_log({"event_type": "replace", "datasource_name": ds1, "options": {"source": "full_body"}})

            self.expect_ops_log(
                {
                    "event_type": "replace",
                    "datasource_name": ds2,
                    "options": {"replace_origin_datasource": ds1_datasource.id, "replace_origin_workspace": self.u.id},
                }
            )

            self.expect_ops_log(
                {
                    "event_type": "replace",
                    "datasource_name": ds3,
                    "options": {"replace_origin_datasource": ds1_datasource.id, "replace_origin_workspace": self.u.id},
                }
            )

        # 1. Initial replace

        await self.replace_data_to_datasource(
            self.token, ds1, CsvIO("1,2020-01-01,A", "1,2020-01-01,B", "1,2020-01-02,A", "1,2020-01-02,B")
        )

        await _test_expected()

        # 2. Replace after append

        await self.replace_data_to_datasource(
            self.token,
            ds1,
            CsvIO(
                "1,2020-01-01,A",
                "1,2020-01-01,A",
                "1,2020-01-01,B",
                "8,2020-01-01,B",
                "8,2020-01-02,B",
                "9,2020-03-02,B",
                "1,2020-01-02,A",
                "5,2020-01-02,A",
                "1,2020-01-02,B",
            ),
        )

        await self.replace_data_to_datasource(
            self.token, ds1, CsvIO("1,2020-01-01,A", "1,2020-01-01,B", "1,2020-01-02,A", "1,2020-01-02,B")
        )

        await _test_expected()


class TestAPIDatasourceHooksReplaceCompleteBatch(TestAPIDatasourceHooksReplaceCompleteBase):
    @tornado.testing.gen_test
    async def test_full_replace_cascade_join_id_cast_one_level(self):
        """
        +------+  insert/replace   +-----+  MV1to2   +----------+
        |  ws  | ----------------> | DS1 | --------> | DS2_join |
        +------+                   +-----+           +----------+
        """
        rand = str(uuid.uuid4())[:8]
        ds1 = f"DS1_{rand}"
        ds2 = f"DS2_{rand}"
        mv1 = f"MV1to2_{rand}"

        await self.create_datasource_async(
            self.token,
            ds1,
            """
                id String,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        ds1_datasource = Users.get_datasource(self.u, ds1)

        await self.create_datasource_async(
            self.token,
            ds2,
            """
                id LowCardinality(String),
                timestamp Date,
                total UInt64
            """,
            {"engine": "Join", "engine_join_strictness": "ANY", "engine_join_type": "LEFT", "engine_key_columns": "id"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds2,
            f"""
                SELECT
                    CAST(id, 'LowCardinality(String)') as id,
                    timestamp,
                    count() as total
                FROM {ds1}
                GROUP BY id, timestamp
            """,
            pipe_name=mv1,
        )

        async def _test_expected():
            await self.expected_data_in_datasource(
                self.token,
                ds1,
                """"1","2020-01-01","A"
"1","2020-01-01","B"
"1","2020-01-02","A"
"1","2020-01-02","B"
""",
            )

            await self.expected_data_in_join_datasource(
                self.token,
                ds2,
                ["timestamp", "total"],
                "1",
                """"2020-01-02",2
""",
            )

            self.expect_ops_log(
                [
                    {"event_type": "replace", "datasource_name": ds1, "options": {"source": "full_body"}},
                    {
                        "event_type": "replace",
                        "datasource_name": ds2,
                        "options": {
                            "replace_origin_datasource": ds1_datasource.id,
                            "replace_origin_workspace": self.u.id,
                        },
                    },
                ]
            )

        # 1. Initial replace

        await self.replace_data_to_datasource(
            self.token, ds1, CsvIO("1,2020-01-01,A", "1,2020-01-01,B", "1,2020-01-02,A", "1,2020-01-02,B")
        )

        await _test_expected()

        # 2. Replace after append

        await self.replace_data_to_datasource(
            self.token,
            ds1,
            CsvIO(
                "1,2020-01-01,A",
                "1,2020-01-01,A",
                "1,2020-01-01,B",
                "8,2020-01-01,B",
                "8,2020-01-02,B",
                "9,2020-03-02,B",
                "1,2020-01-02,A",
                "5,2020-01-02,A",
                "1,2020-01-02,B",
            ),
        )

        await self.replace_data_to_datasource(
            self.token,
            ds1,
            CsvIO("1,2020-01-01,A", "1,2020-01-01,B", "1,2020-01-02,A", "1,2020-01-02,B"),
            expect_logs=False,
        )

        await _test_expected()

    @tornado.testing.gen_test
    async def test_full_replace_cascade_with_join(self):
        """
        +------+  insert/replace   +-----+  MV1to2   +-----+  MV2to3   +----------+
        |  ws  | ----------------> | DS1 | --------> | DS2 | --------> | DS3_join |
        +------+                   +-----+           +-----+           +----------+
        """
        rand = str(uuid.uuid4())[:8]
        ds1 = f"DS1_{rand}"
        ds2 = f"DS2_{rand}"
        ds3 = f"DS3_join_{rand}"
        mv1 = f"MV1to2_{rand}"
        mv2 = f"MV2to3_{rand}"

        await self.create_datasource_async(
            self.token,
            ds1,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        ds1_datasource = Users.get_datasource(self.u, ds1)

        await self.create_datasource_async(
            self.token,
            ds2,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        await self.create_datasource_async(
            self.token,
            ds3,
            """
                id Int32,
                timestamp Date,
                total UInt64
            """,
            {"engine": "Join", "engine_join_strictness": "ANY", "engine_join_type": "LEFT", "engine_key_columns": "id"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds2,
            f"""
                SELECT
                    id,
                    timestamp,
                    category
                FROM {ds1}
                WHERE category = 'B'
            """,
            pipe_name=mv1,
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds3,
            f"""
                SELECT
                    id,
                    timestamp,
                    count() as total
                FROM {ds2}
                GROUP BY id, timestamp
            """,
            pipe_name=mv2,
        )

        async def _test_expected():
            await self.expected_data_in_datasource(
                self.token,
                ds1,
                """1,"2020-01-01","A"
1,"2020-01-01","B"
1,"2020-01-02","A"
5,"2020-01-02","B"
""",
            )

            await self.expected_data_in_datasource(
                self.token,
                ds2,
                """1,"2020-01-01","B"
5,"2020-01-02","B"
""",
            )

            await self.expected_data_in_datasource(
                self.token,
                ds3,
                """5,"2020-01-02",1
1,"2020-01-01",1
""",
            )

            self.expect_ops_log({"event_type": "replace", "datasource_name": ds1, "options": {"source": "full_body"}})

            self.expect_ops_log(
                {
                    "event_type": "replace",
                    "datasource_name": ds2,
                    "options": {"replace_origin_datasource": ds1_datasource.id, "replace_origin_workspace": self.u.id},
                }
            )

            self.expect_ops_log(
                {
                    "event_type": "replace",
                    "datasource_name": ds3,
                    "options": {"replace_origin_datasource": ds1_datasource.id, "replace_origin_workspace": self.u.id},
                }
            )

        # 1. Initial replace

        await self.replace_data_to_datasource(
            self.token, ds1, CsvIO("1,2020-01-01,A", "1,2020-01-01,B", "1,2020-01-02,A", "5,2020-01-02,B")
        )

        await _test_expected()

        # 2. Replace after append

        await self.replace_data_to_datasource(
            self.token,
            ds1,
            CsvIO(
                "1,2020-01-01,A",
                "3,2020-01-01,A",
                "2,2020-01-01,B",
                "3,2020-01-02,A",
                "1,2020-01-02,A",
                "1,2020-01-02,B",
            ),
        )

        await self.replace_data_to_datasource(
            self.token, ds1, CsvIO("1,2020-01-01,A", "1,2020-01-01,B", "1,2020-01-02,A", "5,2020-01-02,B")
        )

        await _test_expected()

    @tornado.testing.gen_test
    async def test_full_replace_cascade_with_middle_join(self):
        """
        +------+  insert/replace   +-----+  MV1to2   +----------+  MV2to3   +-----+
        |  ws  | ----------------> | DS1 | --------> | DS2_join | --------> | DS3 |
        +------+                   +-----+           +----------+           +-----+
        """
        rand = str(uuid.uuid4())[:8]
        ds1 = f"DS1_{rand}"
        ds2 = f"DS2_join_{rand}"
        ds3 = f"DS3_{rand}"
        mv1 = f"MV1to2_{rand}"
        mv2 = f"MV2to3_{rand}"

        await self.create_datasource_async(
            self.token,
            ds1,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        ds1_datasource = Users.get_datasource(self.u, ds1)

        await self.create_datasource_async(
            self.token,
            ds2,
            """
                id Int32,
                timestamp Date,
                total UInt64
            """,
            {"engine": "Join", "engine_join_strictness": "ANY", "engine_join_type": "LEFT", "engine_key_columns": "id"},
        )

        await self.create_datasource_async(
            self.token,
            ds3,
            """
                id Int32,
                timestamp Date,
                total UInt64
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds2,
            f"""
                SELECT
                    id,
                    timestamp,
                    count() as total
                FROM {ds1}
                WHERE category = 'B'
                GROUP BY id, timestamp
            """,
            pipe_name=mv2,
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds3,
            f"""
                SELECT
                    id,
                    timestamp,
                    total
                FROM {ds2}
            """,
            pipe_name=mv1,
        )

        async def _test_expected():
            await self.expected_data_in_datasource(
                self.token,
                ds1,
                """1,"2020-01-01","A"
1,"2020-01-01","B"
1,"2020-01-02","A"
1,"2020-01-02","B"
""",
            )

            await self.expected_data_in_datasource(
                self.token,
                ds2,
                """1,"2020-01-01",1
""",
            )

            await self.expected_data_in_datasource(
                self.token,
                ds3,
                """1,"2020-01-01",1
""",
            )

            self.expect_ops_log({"event_type": "replace", "datasource_name": ds1, "options": {"source": "full_body"}})

            self.expect_ops_log(
                {
                    "event_type": "replace",
                    "datasource_name": ds2,
                    "options": {"replace_origin_datasource": ds1_datasource.id, "replace_origin_workspace": self.u.id},
                }
            )

            self.expect_ops_log(
                {
                    "event_type": "replace",
                    "datasource_name": ds3,
                    "options": {"replace_origin_datasource": ds1_datasource.id, "replace_origin_workspace": self.u.id},
                }
            )

        # 1. Initial replace

        await self.replace_data_to_datasource(
            self.token, ds1, CsvIO("1,2020-01-01,A", "1,2020-01-01,B", "1,2020-01-02,A", "1,2020-01-02,B")
        )

        await _test_expected()

        # 2. Replace after append

        await self.replace_data_to_datasource(
            self.token,
            ds1,
            CsvIO(
                "1,2020-01-01,A",
                "3,2020-01-01,A",
                "2,2020-01-01,B",
                "3,2020-01-02,A",
                "1,2020-01-02,A",
                "1,2020-01-02,B",
            ),
        )

        await self.replace_data_to_datasource(
            self.token, ds1, CsvIO("1,2020-01-01,A", "1,2020-01-01,B", "1,2020-01-02,A", "1,2020-01-02,B")
        )

        await _test_expected()

    @tornado.testing.gen_test
    async def test_full_replace_cascade_with_two_branches(self):
        """
        +------+  insert/replace   +---------+  MV1to2   +-----+  MV2to4   +-----+
        |  ws  | ----------------> |   DS1   | --------> | DS2 | --------> | DS4 |
        +------+                   +---------+           +-----+           +-----+
                                     |
                                     | MV1to3
                                     v
                                   +---------+  MV3to5   +-----+
                                   |   DS3   | --------> | DS5 |
                                   +---------+           +-----+
        """
        rand = str(uuid.uuid4())[:8]
        ds1 = f"DS1_{rand}"
        ds2 = f"DS2_{rand}"
        ds3 = f"DS3_{rand}"
        ds4 = f"DS4_{rand}"
        ds5 = f"DS5_{rand}"
        mv1 = f"MV1to2_{rand}"
        mv2 = f"MV2to4_{rand}"
        mv3 = f"MV1to3_{rand}"
        mv4 = f"MV3to5_{rand}"

        await self.create_datasource_async(
            self.token,
            ds1,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        ds1_datasource = Users.get_datasource(self.u, ds1)

        await self.create_datasource_async(
            self.token,
            ds2,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        await self.create_datasource_async(
            self.token,
            ds3,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        await self.create_datasource_async(
            self.token,
            ds4,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        await self.create_datasource_async(
            self.token,
            ds5,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds2,
            f"""
                SELECT
                    id,
                    timestamp,
                    category
                FROM {ds1}
                WHERE category != 'B'
            """,
            pipe_name=mv1,
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds3,
            f"""
                SELECT
                    id,
                    timestamp,
                    category
                FROM {ds1}
                WHERE category != 'C'
            """,
            pipe_name=mv2,
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds4,
            f"""
                SELECT
                    id,
                    timestamp,
                    category
                FROM {ds2}
                WHERE category == 'A'
            """,
            pipe_name=mv3,
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds5,
            f"""
                SELECT
                    id,
                    timestamp,
                    category
                FROM {ds3}
                WHERE category == 'A'
            """,
            pipe_name=mv4,
        )

        async def _test_expected():
            await self.expected_data_in_datasource(
                self.token,
                ds1,
                """1,"2020-01-01","B"
1,"2020-01-01","C"
1,"2020-01-02","B"
2,"2020-01-01","A"
2,"2020-01-01","C"
2,"2020-01-01","A"
""",
            )

            await self.expected_data_in_datasource(
                self.token,
                ds2,
                """1,"2020-01-01","C"
2,"2020-01-01","A"
2,"2020-01-01","C"
2,"2020-01-01","A"
""",
            )

            await self.expected_data_in_datasource(
                self.token,
                ds3,
                """1,"2020-01-01","B"
1,"2020-01-02","B"
2,"2020-01-01","A"
2,"2020-01-01","A"
""",
            )

            await self.expected_data_in_datasource(
                self.token,
                ds4,
                """2,"2020-01-01","A"
2,"2020-01-01","A"
""",
            )

            await self.expected_data_in_datasource(
                self.token,
                ds5,
                """2,"2020-01-01","A"
2,"2020-01-01","A"
""",
            )

            self.expect_ops_log({"event_type": "replace", "datasource_name": ds1})

            self.expect_ops_log(
                {
                    "event_type": "replace",
                    "datasource_name": ds2,
                    "options": {"replace_origin_datasource": ds1_datasource.id, "replace_origin_workspace": self.u.id},
                }
            )

            self.expect_ops_log(
                {
                    "event_type": "replace",
                    "datasource_name": ds3,
                    "options": {"replace_origin_datasource": ds1_datasource.id, "replace_origin_workspace": self.u.id},
                }
            )

            self.expect_ops_log(
                {
                    "event_type": "replace",
                    "datasource_name": ds4,
                    "options": {"replace_origin_datasource": ds1_datasource.id, "replace_origin_workspace": self.u.id},
                }
            )

            self.expect_ops_log(
                {
                    "event_type": "replace",
                    "datasource_name": ds5,
                    "options": {"replace_origin_datasource": ds1_datasource.id, "replace_origin_workspace": self.u.id},
                }
            )

        # 1. Initial replace

        await self.replace_data_to_datasource(
            self.token,
            ds1,
            CsvIO(
                "2,2020-01-01,A",
                "1,2020-01-01,B",
                "2,2020-01-01,C",
                "1,2020-01-02,B",
                "2,2020-01-01,A",
                "1,2020-01-01,C",
            ),
            expect_logs=False,
        )

        await _test_expected()

        # 2. Replace after append

        await self.append_data_to_datasource(
            self.token,
            ds1,
            CsvIO(
                "1,2020-01-01,A",
                "2,2020-01-01,B",
                "1,2020-01-01,C",
                "2,2020-01-01,A",
                "1,2020-01-01,B",
                "2,2020-01-02,C",
                "1,2020-01-02,A",
                "2,2020-01-02,B",
                "1,2020-01-02,C",
            ),
        )

        #  materializations
        self.expect_ops_log(
            [
                {"event_type": "append", "datasource_name": ds2, "pipe_name": mv1},
                {"event_type": "append", "datasource_name": ds3, "pipe_name": mv2},
                {"event_type": "append", "datasource_name": ds4, "pipe_name": mv3},
                {"event_type": "append", "datasource_name": ds5, "pipe_name": mv4},
            ]
        )

        await self.replace_data_to_datasource(
            self.token,
            ds1,
            CsvIO(
                "2,2020-01-01,A",
                "1,2020-01-01,B",
                "2,2020-01-01,C",
                "1,2020-01-02,B",
                "2,2020-01-01,A",
                "1,2020-01-01,C",
            ),
            expect_logs=False,
        )

        await _test_expected()

    @pytest.mark.skip("Not common case for a full replace")
    @tornado.testing.gen_test
    async def test_full_replace_cascade_with_two_mixed_branches(self):
        """
                                           MV1to3
                                     +-----------------------------------+
                                     |                                   v
        +------+  insert/replace   +-----+  MV1to2   +-----+  MV2to3   +-----+  MV3to4   +-----+
        |  ws  | ----------------> | DS1 | --------> | DS2 | --------> | DS3 | --------> | DS4 |
        +------+                   +-----+           +-----+           +-----+           +-----+

        Note: this is a weird use case for a full replace and probably in this case the user
        doesn't want to do a full replace. Ideally, we should return an error instead if there is
        a full replace with this data flow
        """
        rand = str(uuid.uuid4())[:8]
        ds1 = f"DS1_{rand}"
        ds2 = f"DS2_{rand}"
        ds3 = f"DS3_{rand}"
        ds4 = f"DS4_{rand}"
        mv1 = f"MV1to2_{rand}"
        mv2 = f"MV2to3_{rand}"
        mv3 = f"MV3to4_{rand}"
        mv4 = f"MV1to3_{rand}"

        await self.create_datasource_async(
            self.token,
            ds1,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        await self.create_datasource_async(
            self.token,
            ds2,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        await self.create_datasource_async(
            self.token,
            ds3,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        await self.create_datasource_async(
            self.token,
            ds4,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds2,
            f"""
                SELECT
                    id,
                    timestamp,
                    category
                FROM {ds1}
                WHERE category != 'A'
            """,
            pipe_name=mv1,
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds3,
            f"""
                SELECT
                    id,
                    timestamp,
                    category
                FROM {ds2}
                WHERE category != 'B'
            """,
            pipe_name=mv2,
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds4,
            f"""
                SELECT
                    id,
                    timestamp,
                    category
                FROM {ds3}
                WHERE id == 2
            """,
            pipe_name=mv3,
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds3,
            f"""
                SELECT
                    id,
                    timestamp,
                    category
                FROM {ds1}
                WHERE category = 'A'
            """,
            pipe_name=mv4,
        )

        async def _test_expected(is_first_time=True):
            await self.expected_data_in_datasource(
                self.token,
                ds1,
                """1,"2020-01-01","B"
1,"2020-01-01","A"
1,"2020-01-02","C"
1,"2020-01-02","B"
2,"2020-01-01","A"
2,"2020-01-01","C"
2,"2020-01-01","B"
3,"2020-01-02","A"
3,"2020-01-02","C"
""",
                order_by_columns="id",
            )

            await self.expected_data_in_datasource(
                self.token,
                ds2,
                """1,"2020-01-01","B"
1,"2020-01-02","C"
1,"2020-01-02","B"
2,"2020-01-01","C"
2,"2020-01-01","B"
3,"2020-01-02","C"
""",
                order_by_columns="id",
            )

            if is_first_time:
                await self.expected_data_in_datasource(
                    self.token,
                    ds3,
                    """1,"2020-01-01","A"
2,"2020-01-01","A"
3,"2020-01-02","A"
""",
                    order_by_columns="id",
                )
            else:
                await self.expected_data_in_datasource(
                    self.token,
                    ds3,
                    """1,"2020-01-01","A"
1,"2020-01-02","C"
2,"2020-01-01","A"
2,"2020-01-01","C"
3,"2020-01-02","A"
3,"2020-01-02","C"
""",
                    order_by_columns="id",
                )

            if is_first_time:
                await self.expected_data_in_datasource(
                    self.token,
                    ds4,
                    """2,"2020-01-01","A"
""",
                    order_by_columns="id",
                )
            else:
                await self.expected_data_in_datasource(
                    self.token,
                    ds4,
                    """2,"2020-01-01","C"
2,"2020-01-01","A"
""",
                    order_by_columns="id",
                )

            self.expect_ops_log({"event_type": "replace", "datasource_name": ds1})

            self.expect_ops_log({"event_type": "replace", "datasource_name": ds2})

            self.expect_ops_log({"event_type": "replace", "datasource_name": ds3})

            self.expect_ops_log({"event_type": "replace", "datasource_name": ds3})

            self.expect_ops_log({"event_type": "replace", "datasource_name": ds4})

            self.expect_ops_log({"event_type": "replace", "datasource_name": ds4})

        # 1. Initial replace

        await self.replace_data_to_datasource(
            self.token,
            ds1,
            CsvIO(
                "2,2020-01-01,A",
                "1,2020-01-01,B",
                "2,2020-01-01,C",
                "1,2020-01-01,A",
                "2,2020-01-01,B",
                "1,2020-01-02,C",
                "3,2020-01-02,A",
                "1,2020-01-02,B",
                "3,2020-01-02,C",
            ),
            expect_logs=False,
        )

        await _test_expected()

        # 2. Replace after append

        await self.append_data_to_datasource(
            self.token,
            ds1,
            CsvIO("8,2020-01-01,A", "2,2020-01-01,B", "1,2020-01-02,E", "2,2020-01-02,B", "1,2020-01-02,C"),
        )

        await self.replace_data_to_datasource(
            self.token,
            ds1,
            CsvIO(
                "2,2020-01-01,A",
                "1,2020-01-01,B",
                "2,2020-01-01,C",
                "1,2020-01-01,A",
                "2,2020-01-01,B",
                "1,2020-01-02,C",
                "3,2020-01-02,A",
                "1,2020-01-02,B",
                "3,2020-01-02,C",
            ),
            expect_logs=False,
        )

        _test_expected(is_first_time=False)

    @tornado.testing.gen_test
    async def test_full_replace_to_common_destination_data_source(self):
        """
        +------+  insert/replace   +---------+  MV1to3   +-----+  MV3to4   +-----+
        |  ws  | ----------------> |   DS1   | --------> | DS3 | --------> | DS4 |
        +------+                   +---------+           +-----+           +-----+
            |                                               ^
            |                                               |
            v                                               |
        +-----+               MV2to3                        |
        | DS2 | --------------------------------------------+
        +-----+
        """
        rand = str(uuid.uuid4())[:8]
        ds1 = f"DS1_{rand}"
        ds2 = f"DS2_{rand}"
        ds3 = f"DS3_{rand}"
        ds4 = f"DS4_{rand}"

        mv1 = f"MV1to3_{rand}"
        mv2 = f"MV2to3_{rand}"
        mv3 = f"MV3to4_{rand}"

        await self.create_datasource_async(
            self.token,
            ds1,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        ds1_datasource = Users.get_datasource(self.u, ds1)

        await self.create_datasource_async(
            self.token,
            ds2,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        await self.create_datasource_async(
            self.token,
            ds3,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        await self.create_datasource_async(
            self.token,
            ds4,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds3,
            f"""
                SELECT
                    id,
                    timestamp,
                    category
                FROM {ds1}
                WHERE category != 'A'
            """,
            pipe_name=mv1,
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds3,
            f"""
                SELECT
                    id,
                    timestamp,
                    category
                FROM {ds2}
                WHERE category != 'B'
            """,
            pipe_name=mv2,
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds4,
            f"""
                SELECT
                    id,
                    timestamp,
                    category
                FROM {ds3}
                WHERE category == 'A'
            """,
            pipe_name=mv3,
        )

        await self.append_data_to_datasource(
            self.token, ds2, CsvIO("8,2020-01-01,A", "9,2020-01-01,B", "10,2020-01-01,C")
        )

        self.expect_ops_log(
            [
                {"event_type": "append", "datasource_name": ds3},
                {"event_type": "append", "datasource_name": ds4},
            ]
        )

        async def _test_expected():
            await self.expected_data_in_datasource(
                self.token,
                ds1,
                """1,"2020-01-01","A"
2,"2020-01-01","A"
2,"2020-01-01","A"
""",
            )

            await self.expected_data_in_datasource(
                self.token,
                ds3,
                """8,"2020-01-01","A"
10,"2020-01-01","C"
""",
            )

            await self.expected_data_in_datasource(
                self.token,
                ds4,
                """8,"2020-01-01","A"
""",
            )

            self.expect_ops_log({"event_type": "replace", "datasource_name": ds1})

            self.expect_ops_log(
                {
                    "event_type": "replace",
                    "datasource_name": ds3,
                    "options": {"replace_origin_datasource": ds1_datasource.id, "replace_origin_workspace": self.u.id},
                }
            )
            self.expect_ops_log(
                {
                    "event_type": "replace",
                    "datasource_name": ds3,
                    "options": {"replace_origin_datasource": ds1_datasource.id, "replace_origin_workspace": self.u.id},
                }
            )

            self.expect_ops_log(
                {
                    "event_type": "replace",
                    "datasource_name": ds4,
                    "options": {"replace_origin_datasource": ds1_datasource.id, "replace_origin_workspace": self.u.id},
                }
            )

        await self.replace_data_to_datasource(
            self.token, ds1, CsvIO("2,2020-01-01,A", "1,2020-01-01,A", "2,2020-01-01,A"), expect_logs=False
        )

        await _test_expected()

        await self.append_data_to_datasource(
            self.token, ds1, CsvIO("1,2020-01-01,A", "2,2020-01-01,B", "5,2020-01-01,C")
        )

        self.expect_ops_log(
            [{"event_type": "append", "datasource_name": ds3}, {"event_type": "append", "datasource_name": ds4}]
        )

        await self.replace_data_to_datasource(
            self.token, ds1, CsvIO("2,2020-01-01,A", "1,2020-01-01,A", "2,2020-01-01,A"), expect_logs=False
        )

        await _test_expected()

    @tornado.testing.gen_test
    async def test_cascade_replace_cascade_stream_import(self):
        """
        +------+  insert/replace   +---------+  MV1to2   +-----+  MV2to3   +-----+
        |  ws  | ----------------> |   DS1   | --------> | DS2 | --------> | DS3 |
        +------+                   +---------+           +-----+           +-----+
        - Replace done with a full-body import.
        """
        rand = str(uuid.uuid4())[:8]
        ds1 = f"DS1_{rand}"
        ds2 = f"DS2_{rand}"
        ds3 = f"DS3_{rand}"
        mv1 = f"MV1to2_{rand}"
        mv2 = f"MV2to3_{rand}"

        await self.create_datasource_async(
            self.token,
            ds1,
            """
                dt Date,
                country String,
                product String,
                units Int32
            """,
            {"engine": "MergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        await self.create_datasource_async(
            self.token,
            ds2,
            """
                dt Date,
                country String,
                product String,
                sum_units Int32
            """,
            {"engine": "SummingMergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt, product"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds2,
            f"""
            SELECT
                dt,
                country,
                product,
                toInt32(sum(units)) AS sum_units
            FROM {ds1}
            GROUP BY dt, country, product
            """,
            pipe_name=mv1,
        )

        await self.create_datasource_async(
            self.token,
            ds3,
            """
                dt Date,
                country String,
                sum_per_country Int32
            """,
            {"engine": "SummingMergeTree", "engine_partition_key": "dt", "engine_sorting_key": "country, dt"},
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds3,
            f"""
            SELECT
                dt,
                country,
                toInt32(sum(sum_units)) AS sum_per_country
            FROM {ds2}
            GROUP BY dt, country
            """,
            pipe_name=mv2,
        )

        params = {
            "token": self.token,
            "mode": "append",
            "name": ds1,
        }

        append_url = self.get_url(f"/v0/datasources?{urlencode(params)}")
        with fixture_file("replace_simple_base_data.csv", mode="rb") as fd:
            response = await self.fetch_stream_upload_async(append_url, fd)
        self.assertEqual(response.code, 200, response.body)

        self.expect_ops_log({"event_type": "append", "datasource_name": ds1, "options": {"source": "stream"}})

        self.expect_ops_log(
            [{"event_type": "append", "datasource_name": ds2}, {"event_type": "append", "datasource_name": ds3}]
        )

        # Replace operation
        params = {"token": self.token, "mode": "replace", "name": ds1}
        replace_url = self.get_url(f"/v0/datasources?{urlencode(params)}")
        with fixture_file("replace_simple_data_replaced.csv", mode="rb") as fd:
            response = await self.fetch_stream_upload_async(replace_url, fd)

        self.assertEqual(response.code, 200, response.body)
        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": ds1,
                "options": {
                    "source": "stream",
                },
            }
        )

        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": ds2,
                "options": {
                    "source": "stream",
                },
            }
        )

        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": ds3,
                "options": {
                    "source": "stream",
                },
            }
        )

        await self.expected_data_in_datasource(
            self.token,
            ds1,
            """"2020-01-02","ES","A",5
"2020-01-02","ES","A",5
"2020-01-02","ES","B",5
""",
            "dt, country, product",
        )

        await self.expected_data_in_datasource(
            self.token,
            ds2,
            """"2020-01-02","ES","A",10
"2020-01-02","ES","B",5
""",
            "dt, country, product",
        )

        await self.expected_data_in_datasource(
            self.token,
            ds3,
            """"2020-01-02","ES",15
""",
            "dt, country",
        )

    @tornado.testing.gen_test
    async def test_full_replace_cascade_different_workspaces(self):
        """
        +------+  insert/replace   +-----+  MV1to2   +-----+   share   +-----+     +-----+  MV2to3   +-----+
        |  ws  | ----------------> | DS1 | --------> | DS2 | --------> | ws2 | --> | DS2 | --------> | DS3 |
        +------+                   +-----+           +-----+           +-----+     +-----+           +-----+
        """
        rand = str(uuid.uuid4())[:8]
        ds1 = f"DS1_{rand}"
        ds2 = f"DS2_{rand}"
        ds3 = f"DS3_{rand}"
        mv1 = f"MV1to2_{rand}"
        mv2 = f"MV2to3_{rand}"
        ws2 = f"dev_workspace_{uuid.uuid4().hex}"
        ws1 = self.u.name

        workspace_1 = self.u
        auth_token = UserAccount.get_token_for_scope(self.user_account, scopes.AUTH)
        workspace_2 = await self.tb_api_proxy_async.register_workspace(ws2, self.user_account)
        workspace_2 = User.get_by_id(workspace_2["id"])
        token_workspace_2 = Users.get_token_for_scope(workspace_2, scopes.ADMIN_USER)
        self.workspaces_to_delete.append(workspace_2)

        await self.create_datasource_async(
            self.token,
            ds1,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        ds1_datasource = Users.get_datasource(self.u, ds1)

        await self.create_datasource_async(
            self.token,
            ds2,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        ds2_shared = Users.get_datasource(workspace_1, ds2)

        await self.create_datasource_async(
            token_workspace_2,
            ds3,
            """
                id Int32,
                timestamp Date,
                total UInt64
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
            expect_ops_log=False,
        )

        await self.tb_api_proxy_async.share_datasource_with_another_workspace(
            token=auth_token,
            datasource_id=ds2_shared.id,
            origin_workspace_id=workspace_1.id,
            destination_workspace_id=workspace_2.id,
            expect_notification=False,
        )

        await self.create_view_async(
            self.u,
            self.token,
            ds2,
            f"""
                SELECT
                    id,
                    timestamp,
                    category
                FROM {ds1}
                WHERE category = 'B'
            """,
            pipe_name=mv1,
        )

        await self.create_view_async(
            workspace_2,
            token_workspace_2,
            ds3,
            f"""
                SELECT
                    id,
                    timestamp,
                    count() as total
                FROM {ws1}.{ds2}
                GROUP BY id, timestamp
            """,
            pipe_name=mv2,
        )

        async def _test_expected():
            await self.expected_data_in_datasource(
                self.token,
                ds1,
                """1,"2020-01-01","A"
1,"2020-01-01","B"
1,"2020-01-02","A"
1,"2020-01-02","B"
""",
            )

            await self.expected_data_in_datasource(
                self.token,
                ds2,
                """1,"2020-01-01","B"
1,"2020-01-02","B"
""",
            )

            await self.expected_data_in_datasource(
                token_workspace_2,
                ds3,
                """1,"2020-01-01",1
1,"2020-01-02",1
""",
            )

            self.expect_ops_log({"event_type": "replace", "datasource_name": ds1})

            self.expect_ops_log(
                {
                    "event_type": "replace",
                    "datasource_name": ds2,
                    "options": {"replace_origin_datasource": ds1_datasource.id, "replace_origin_workspace": self.u.id},
                }
            )

            # TODO expect_ops_log are only checked in the same workspace
            # self.expect_ops_log({
            #     'event_type': 'replace',
            #     'datasource_name': ds3
            # })

        # 1. Initial replace

        await self.replace_data_to_datasource(
            self.token,
            ds1,
            CsvIO("1,2020-01-01,A", "1,2020-01-01,B", "1,2020-01-02,A", "1,2020-01-02,B"),
            expect_logs=False,
        )

        await _test_expected()

        # 2. Replace after append

        await self.append_data_to_datasource(
            self.token,
            ds1,
            CsvIO(
                "1,2020-01-01,A",
                "1,2020-01-01,A",
                "1,2020-01-01,B",
                "1,2020-01-02,A",
                "1,2020-01-02,A",
                "1,2020-01-02,B",
            ),
        )

        self.expect_ops_log([{"event_type": "append", "datasource_name": ds2}])

        await self.replace_data_to_datasource(
            self.token,
            ds1,
            CsvIO("1,2020-01-01,A", "1,2020-01-01,B", "1,2020-01-02,A", "1,2020-01-02,B"),
            expect_logs=False,
        )

        await _test_expected()


class TestAPIDatasourceRateLimits(TestAPIDatasourceBase):
    @tornado.testing.gen_test
    async def test_headers(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        url = self.get_url(f"/v0/datasources?token={token}")

        with fixture_file("yt_1000.csv", mode="rb") as fd:
            response = await self.fetch_stream_upload_async(url, fd)
        self.assertEqual(response.code, 200)
        self.assertIn("X-Ratelimit-Limit", response.headers)
        self.assertIn("X-Ratelimit-Remaining", response.headers)
        self.assertIn("X-Ratelimit-Reset", response.headers)

    @tornado.testing.gen_test
    async def test_429_stream(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        url = self.get_url(f"/v0/datasources?token={token}")
        url_first = url + "&n=1"
        url_second = url + "&n=2"

        with User.transaction(u.id) as user:
            user.set_rate_limit_config("api_datasources_create_append_replace", 1, 60, 0)

        with fixture_file("yt_1000.csv", mode="rb") as fd:
            response = await self.fetch_stream_upload_async(url_first, fd)
        self.assertEqual(response.code, 200)
        self.assertIn("X-Ratelimit-Limit", response.headers)
        self.assertIn("X-Ratelimit-Remaining", response.headers)
        self.assertIn("X-Ratelimit-Reset", response.headers)
        self.assertNotIn("Retry-After", response.headers)
        span = self.get_span(url_first)
        self.assertEqual(span.get("status_code"), 200)
        self.assertEqual(span.get("method"), "POST")
        self.assertEqual(span.get("error"), None)

        with fixture_file("yt_1000.csv", mode="rb") as fd:
            response = await self.fetch_stream_upload_async(url_second, fd)

        self.assertEqual(response.code, 429, response.body)
        response_json = json.loads(response.body)
        self.assertEqual(
            f"Too many requests: retry after {response.headers['Retry-After']} seconds", response_json["error"]
        )
        self.assertIn("/api-reference/api-reference.html#limits", response_json["documentation"])
        self.assertIn("X-Ratelimit-Limit", response.headers)
        self.assertIn("X-Ratelimit-Remaining", response.headers)
        self.assertIn("X-Ratelimit-Reset", response.headers)
        self.assertIn("Retry-After", response.headers)
        span = self.get_span(url_second)
        self.assertEqual(span.get("status_code"), 429)
        self.assertEqual(span.get("method"), "POST")
        self.assertRegex(span.get("error"), "Too many requests: .*")

    @tornado.testing.gen_test
    async def test_429_full_body(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        url = self.get_url(f"/v0/datasources?token={token}")
        url_first = url + "&n=1"
        url_second = url + "&n=2"

        with User.transaction(u.id) as user:
            user.set_rate_limit_config("api_datasources_create_append_replace", 1, 60, max_burst=0)

        with fixture_file("yt_1000.csv", mode="rb") as fd:
            response = await self.fetch_full_body_upload_async(url_first, fd)
        self.assertEqual(response.code, 200)
        span = await self.get_span_async(url_first)
        self.assertEqual(span.get("status_code"), 200)
        self.assertEqual(span.get("method"), "POST")
        self.assertEqual(span.get("error"), None)
        self.assertIn("X-Ratelimit-Limit", response.headers)
        self.assertIn("X-Ratelimit-Remaining", response.headers)
        self.assertNotIn("Retry-After", response.headers)

        with fixture_file("yt_1000.csv", mode="rb") as fd:
            response = await self.fetch_full_body_upload_async(url_second, fd)
        span = await self.get_span_async(url_second)
        self.assertEqual(span.get("status_code"), 429)
        self.assertEqual(span.get("method"), "POST")
        self.assertRegex(span.get("error"), "Too many requests: .*")
        self.assertEqual(response.code, 429, response.body)
        self.assertIn("X-Ratelimit-Limit", response.headers)
        self.assertIn("X-Ratelimit-Remaining", response.headers)
        self.assertIn("X-Ratelimit-Reset", response.headers)
        self.assertIn("Retry-After", response.headers)

    @tornado.testing.gen_test
    async def test_429_url(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)

        with User.transaction(u.id) as user:
            user.set_rate_limit_config("api_datasources_create_append_replace", 1, 60, 0)

        csv_url = f"{HTTP_ADDRESS}/yt_1000.csv"
        params = {"token": token, "url": csv_url, "call": "first"}
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)
        self.assertIn("X-Ratelimit-Limit", response.headers)
        self.assertIn("X-Ratelimit-Remaining", response.headers)
        self.assertIn("X-Ratelimit-Reset", response.headers)
        self.assertNotIn("Retry-After", response.headers)
        span = self.get_span(create_url)
        self.assertEqual(span.get("status_code"), 200)
        self.assertEqual(span.get("method"), "POST")
        self.assertEqual(span.get("error"), None)

        _ = await self.get_finalised_job_async(json.loads(response.body)["id"])

        csv_url = f"{HTTP_ADDRESS}/yt_1000.csv"
        params = {"token": token, "url": csv_url, "call": "second"}
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 429, response.body)
        self.assertIn("X-Ratelimit-Limit", response.headers)
        self.assertIn("X-Ratelimit-Remaining", response.headers)
        self.assertIn("X-Ratelimit-Reset", response.headers)
        self.assertIn("Retry-After", response.headers)
        span = self.get_span(create_url)
        self.assertEqual(span.get("status_code"), 429)
        self.assertEqual(span.get("method"), "POST")
        self.assertRegex(span.get("error"), "Too many requests: .*")

    @tornado.testing.gen_test
    async def test_429_schema(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)

        with User.transaction(u.id) as user:
            user.set_rate_limit_config("api_datasources_create_schema", 1, 60, 0)

        params = {
            "token": token,
            "name": "test_429_schema",
            "schema": """
                d DateTime,
                event_type String
            """,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)
        self.assertIn("X-Ratelimit-Limit", response.headers)
        self.assertIn("X-Ratelimit-Remaining", response.headers)
        self.assertIn("X-Ratelimit-Reset", response.headers)
        self.assertNotIn("Retry-After", response.headers)

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 429, response.body)
        self.assertIn("X-Ratelimit-Limit", response.headers)
        self.assertIn("X-Ratelimit-Remaining", response.headers)
        self.assertIn("X-Ratelimit-Reset", response.headers)
        self.assertIn("Retry-After", response.headers)

    @tornado.testing.gen_test
    async def test_429_schema_body(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)

        with User.transaction(u.id) as user:
            user.set_rate_limit_config("api_datasources_create_schema", 1, 60, 0)

        post = sync_to_async(requests.post, thread_sensitive=False)

        params = {
            "token": token,
        }
        data = {
            "name": "test_429_schema_body",
            "schema": """
                d DateTime,
                event_type String
            """,
        }

        create_url = self.get_url("/v0/datasources")
        response = await post(create_url, params=params, data=data)
        self.assertEqual(response.status_code, 200, response.content)
        self.assertIn("X-Ratelimit-Limit", response.headers)
        self.assertIn("X-Ratelimit-Remaining", response.headers)
        self.assertIn("X-Ratelimit-Reset", response.headers)
        self.assertNotIn("Retry-After", response.headers)

        create_url = self.get_url("/v0/datasources")
        response = await post(create_url, params=params, data=data)
        self.assertEqual(response.status_code, 429, response.content)
        self.assertIn("X-Ratelimit-Limit", response.headers)
        self.assertIn("X-Ratelimit-Remaining", response.headers)
        self.assertIn("X-Ratelimit-Reset", response.headers)
        self.assertIn("Retry-After", response.headers)

    @tornado.testing.gen_test
    async def test_429_ndjson(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)

        with User.transaction(u.id) as user:
            user.set_rate_limit_config("api_datasources_create_schema", 1, 60, 0)

        post = sync_to_async(requests.post, thread_sensitive=False)

        params = {
            "token": token,
            "name": "test_429_ndjson",
            "format": "ndjson",
            "schema": "id String `json:$.id`",
        }

        create_url = self.get_url("/v0/datasources")
        response = await post(create_url, params=params)
        self.assertEqual(response.status_code, 200, response.content)
        self.assertIn("X-Ratelimit-Limit", response.headers)
        self.assertIn("X-Ratelimit-Remaining", response.headers)
        self.assertIn("X-Ratelimit-Reset", response.headers)
        self.assertNotIn("Retry-After", response.headers)

        params = {
            "token": token,
            "name": "test_429_ndjson2",
            "format": "ndjson",
            "schema": "id String `json:$.id`",
        }
        response = await post(create_url, params=params)
        self.assertEqual(response.status_code, 429, response.content)
        self.assertIn("X-Ratelimit-Limit", response.headers)
        self.assertIn("X-Ratelimit-Remaining", response.headers)
        self.assertIn("X-Ratelimit-Reset", response.headers)
        self.assertIn("Retry-After", response.headers)

    @tornado.testing.gen_test
    async def test_429_ndjson_body(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)

        with User.transaction(u.id) as user:
            user.set_rate_limit_config("api_datasources_create_schema", 1, 60, 0)

        post = sync_to_async(requests.post, thread_sensitive=False)

        params = {
            "token": token,
        }
        data = {
            "name": "test_429_ndjson",
            "format": "ndjson",
            "schema": "id String `json:$.id`",
        }

        create_url = self.get_url("/v0/datasources")
        response = await post(create_url, params=params, data=data)
        self.assertEqual(response.status_code, 200, response.content)
        self.assertIn("X-Ratelimit-Limit", response.headers)
        self.assertIn("X-Ratelimit-Remaining", response.headers)
        self.assertIn("X-Ratelimit-Reset", response.headers)
        self.assertNotIn("Retry-After", response.headers)

        params = {
            "token": token,
            "name": "test_429_ndjson2",
            "format": "ndjson",
            "schema": "id String `json:$.id`",
        }
        response = await post(create_url, params=params)
        self.assertEqual(response.status_code, 429, response.content)
        self.assertIn("X-Ratelimit-Limit", response.headers)
        self.assertIn("X-Ratelimit-Remaining", response.headers)
        self.assertIn("X-Ratelimit-Reset", response.headers)
        self.assertIn("Retry-After", response.headers)

    @tornado.testing.gen_test
    async def test_429_analyze(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)

        with User.transaction(u.id) as user:
            user.set_rate_limit_config("api_datasources_create_schema", 1, 60, 0)

        post = sync_to_async(requests.post, thread_sensitive=False)

        params = {
            "token": token,
            "format": "ndjson",
        }

        analyze_url = self.get_host() + "/v0/analyze"
        response = await post(analyze_url, params=params, data=e2e_fixture_data("events.ndjson", mode="rb"))
        self.assertEqual(response.status_code, 200, response.content)
        self.assertIn("X-Ratelimit-Limit", response.headers)
        self.assertIn("X-Ratelimit-Remaining", response.headers)
        self.assertIn("X-Ratelimit-Reset", response.headers)
        self.assertNotIn("Retry-After", response.headers)

        response = await post(analyze_url, params=params, data=e2e_fixture_data("events.ndjson", mode="rb"))
        self.assertEqual(response.status_code, 429, response.content)
        self.assertIn("X-Ratelimit-Limit", response.headers)
        self.assertIn("X-Ratelimit-Remaining", response.headers)
        self.assertIn("X-Ratelimit-Reset", response.headers)
        self.assertIn("Retry-After", response.headers)

    @tornado.testing.gen_test
    async def test_429_stream_concurrently_rate_limit(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        url = self.get_url(f"/v0/datasources?token={token}")
        rate_limit_config = RateLimitConfig("api_datasources_create_append_replace", 5, 60, 3)
        with User.transaction(u.id) as user:
            user.set_rate_limit_config(
                rate_limit_config.key,
                rate_limit_config.count_per_period,
                rate_limit_config.period,
                rate_limit_config.max_burst,
            )
        rejected = 0
        success = 0

        async def stream_upload(i):
            nonlocal rejected, success
            with fixture_file("yt_1000.csv", mode="rb") as fd:
                response = await self.fetch_stream_upload_async(f"{url}&n={i}", fd)
            assert response.code == 200 or response.code == 429, response.text
            if response.code == 200:
                success += 1
            if response.code == 429:
                rejected += 1

        concurrency = 5
        await asyncio.gather(*[stream_upload(index) for index in range(concurrency)], return_exceptions=False)
        self.assertEqual(success, 4)
        self.assertEqual(rejected, 1)

        rejected = 0
        success = 0
        concurrency = 4
        await asyncio.gather(*[stream_upload(index) for index in range(concurrency)], return_exceptions=False)
        self.assertEqual(success, 0)
        self.assertEqual(rejected, 4)


class TestAPIDatasourceSyncPostgres(TestAPIDatasourceBase):
    def setUp(self):
        super().setUp()
        self.u = Users.get_by_id(self.WORKSPACE_ID)
        self.u["enabled_pg"] = True
        self.u["pg_server"] = "127.0.0.1"
        self.u["pg_foreign_server"] = CH_HOST
        self.u["pg_foreign_server_port"] = CH_HTTP_PORT
        self.u.save()

    def tearDown(self):
        self.u = Users.get_by_id(self.WORKSPACE_ID)
        PGService(self.u).drop_database()
        self.u["enabled_pg"] = False
        self.u.save()
        super().tearDown()

    @tornado.testing.gen_test
    async def test_datasource_change_name_syncs_pg(self):
        self.create_test_datasource()
        self.u = Users.get_by_id(self.WORKSPACE_ID)
        PGService(self.u).setup_database(sync=True)
        token = Users.add_token(self.u, "test", scopes.DATASOURCES_CREATE)
        old_id = Users.get_datasource(self.u, "test_table").id
        response = await self.fetch_async(
            "/v0/datasources/test_table?name=new_ds_name&token=%s" % token, method="PUT", body=""
        )
        self.assertEqual(response.code, 200)
        body = json.loads(response.body)
        self.assertEqual(body["name"], "new_ds_name")
        self.assertEqual(body["id"], old_id)
        self.expect_ops_log(
            {
                "event_type": "rename",
                "datasource_id": old_id,
                "datasource_name": "new_ds_name",
                "options": {
                    "old_name": "test_table",
                    "new_name": "new_ds_name",
                },
            }
        )

        sql = "SELECT * FROM pg_views WHERE viewname = 'new_ds_name' AND schemaname = 'public';"
        res = PGService(self.u).execute(sql, role="user")
        self.assertEqual(len(res), 1)

        sql = "SELECT count(*) FROM new_ds_name;"
        res = PGService(self.u).execute(sql, role="user")
        self.assertEqual(res[0]["count"], 6)

        sql = "SELECT * FROM pg_views WHERE viewname = 'test_table' AND schemaname = 'public';"
        res = PGService(self.u).execute(sql, role="user")
        self.assertEqual(len(res), 0)

    @tornado.testing.gen_test
    async def test_datasource_drop_syncs_pg(self):
        self.create_test_datasource()
        self.u = Users.get_by_id(self.WORKSPACE_ID)
        PGService(self.u).setup_database(sync=True)
        u = self.u

        ds = Users.add_datasource_sync(u, "test_table")
        sql = "SELECT * FROM pg_views WHERE viewname = 'test_table' AND schemaname = 'public';"
        res = PGService(u).execute(sql, role="user")
        self.assertEqual(len(res), 1)

        sql = "SELECT count(*) FROM test_table;"
        res = PGService(u).execute(sql, role="user")
        self.assertEqual(res[0]["count"], 6)

        token = Users.add_token(u, "test", scopes.ADMIN)
        response = await self.fetch_async("/v0/datasources/test_table?token=%s" % token, method="DELETE")

        self.assertEqual(response.code, 204)
        self.assertEqual(None, Users.get_datasource(u, "test_table"))

        sql = "SELECT * FROM pg_views WHERE viewname = 'test_table' AND schemaname = 'public';"
        res = PGService(u).execute(sql, role="user")
        self.assertEqual(len(res), 0)

        self.expect_ops_log(
            [
                {
                    "event_type": "delete",
                    "datasource_id": ds.id,
                    "datasource_name": ds.name,
                },
                {
                    "event_type": "drop foreign table",
                    "datasource_id": ds.id,
                    "datasource_name": ds.name,
                },
            ]
        )

    @tornado.testing.gen_test
    async def test_append_and_create_sync_pg(self):
        PGService(self.u).setup_database(sync=True)
        u = self.u
        token = Users.add_token(u, "test", scopes.DATASOURCES_CREATE)

        url_and_mode = [
            (self.get_url_for_sql("select '1,2,3,4' as a format CSV"), "csv", "`a` String"),
            (self.get_url_for_sql("select '1,2,3,4' as a format JSONEachRow"), "ndjson", "`a` String `json:$.a`"),
        ]

        for url, format, schema in url_and_mode:
            ds_name = f"test_append_and_create_sync_pg_{format}"

            async def _create_with_data(datasource, schema, format, url, mode="create"):
                if mode == "create":
                    params = {
                        "token": token,
                        "name": datasource,
                        "mode": mode,
                        "schema": schema,
                        "format": format,
                    }
                elif mode == "append":
                    params = {
                        "token": token,
                        "name": datasource,
                        "mode": mode,
                        "url": url,
                        "format": format,
                    }
                else:
                    raise Exception("Unknown mode")

                api_url = f"/v0/datasources?{urlencode(params)}"
                client = AsyncHTTPClient()
                response = await client.fetch(self.get_url(api_url), method="POST", body="")

                self.assertEqual(response.code, 200, response)

                data = json.loads(response.body)

                if mode == "append":
                    job = await get_finalised_job_async(data["id"])
                    self.assertEqual(job.status, "done")

                if "datasource" in data:
                    ds_id = data["datasource"]["id"]
                else:
                    ds_id = Users.get_datasource(u, datasource).id

                self.wait_for_datasource_replication(u, ds_id)

            # FIXME ndjson and csv varies on how they are created
            # csv allows create with schema but not URL
            # ndjson allows create with schema and URL
            # csv allows append without schema and URL and auto-guesses the schema
            # make ndjson behave the same as csv mode=create&schema or mode=append&url
            await _create_with_data(ds_name, schema, format, url)
            await _create_with_data(ds_name, schema, format, url, mode="append")

            sql = f"SELECT * FROM pg_views WHERE viewname = '{ds_name}' AND schemaname = 'public';"
            res = PGService(u).execute(sql, role="user")
            self.assertEqual(len(res), 1)

            expected_rows = 1

            sql = f"SELECT count(*) FROM {ds_name};"
            res = PGService(u).execute(sql, role="user")
            self.assertEqual(res[0]["count"], expected_rows)

            self.expect_ops_log(
                [
                    {
                        "event_type": "create",
                        "datasource_name": ds_name,
                    },
                    {
                        "event_type": "append",
                        "datasource_name": ds_name,
                        "rows": 1,
                        "options": {
                            "source": url,
                        },
                    },
                    {
                        "event_type": "create foreign table",
                        "datasource_name": ds_name,
                    },
                ]
            )

    @tornado.testing.gen_test
    async def test_replace_with_full_body_sync_pg(self):
        PGService(self.u).setup_database(sync=True)
        u = self.u
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        name = "test_create_with_replace_full_body"
        params = {
            "token": token,
            "name": name,
        }
        create_url = self.get_url(f"/v0/datasources?{urlencode(params)}")
        with fixture_file("yt_1000.csv", mode="rb") as fd:
            response = await self.fetch_full_body_upload_async(create_url, fd)

        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)

        self.wait_for_datasource_replication(u, result["datasource"]["id"])
        datasource_id = result["datasource"]["id"]
        result = exec_sql(u["database"], f"SELECT count() c FROM {datasource_id} FORMAT JSON")
        self.assertEqual(int(result["data"][0]["c"]), 328)
        self.expect_ops_log(
            [
                {"event_type": "create", "datasource_name": name, "options": {"source": "full_body"}},
                {"event_type": "append", "datasource_name": name, "rows": 328, "options": {"source": "full_body"}},
                {
                    "event_type": "create foreign table",
                    "datasource_id": datasource_id,
                    "datasource_name": name,
                },
            ]
        )

        sql = f"SELECT * FROM pg_views WHERE viewname = '{name}' AND schemaname = 'public';"
        res = PGService(u).execute(sql, role="user")
        self.assertEqual(len(res), 1)

        sql = f"SELECT count(*) FROM {name};"
        res = PGService(u).execute(sql, role="user")
        self.assertEqual(res[0]["count"], 328)

        # load a file with less registers but same schema
        params = {
            "token": token,
            "mode": "replace",
            "name": name,
        }
        create_url = self.get_url(f"/v0/datasources?{urlencode(params)}")
        with fixture_file("yt_100.csv", mode="rb") as fd:
            response = await self.fetch_full_body_upload_async(create_url, fd)
        self.assertEqual(response.code, 200, response.body)
        result = json.loads(response.body)
        datasource_id = result["datasource"]["id"]
        result = exec_sql(u["database"], f"SELECT count() c FROM {datasource_id} FORMAT JSON")
        self.assertEqual(int(result["data"][0]["c"]), 98)
        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": name,
                "rows": 98,
                "options": {
                    "source": "full_body",
                    "rows_before_replace": 328,
                },
            }
        )

        sql = f"SELECT * FROM pg_views WHERE viewname = '{name}' AND schemaname = 'public';"
        res = PGService(u).execute(sql, role="user")
        self.assertEqual(len(res), 1)

        sql = f"SELECT count(*) FROM {name};"
        res = PGService(u).execute(sql, role="user")
        self.assertEqual(res[0]["count"], 98)


class TestAPIKafkaDatasource(TestAPIDatasourceBase):
    def setUp(self):
        super().setUp()

        self.user = Users.get_by_id(self.WORKSPACE_ID)
        self.token = Users.get_token_for_scope(self.user, scopes.ADMIN)
        self.host = self.get_host()
        self.connector_id = None

    def tearDown(self):
        if self.connector_id:
            params = {
                "token": self.token,
            }

            url = f"/v0/connectors/{self.connector_id}?{urlencode(params)}"
            self.fetch(url, method="DELETE")
        super().tearDown()

    async def _add_kafka_connector(self, settings, response_code=200):
        params = {
            "token": self.token,
            "kafka_bootstrap_servers": "localhost:9093",
            "kafka_security_protocol": "plaintext",
            "kafka_sasl_plain_username": "",
            "kafka_sasl_plain_password": "",
        }

        params.update(settings)

        url = f"/v0/connectors?{urlencode(params)}"
        response = await self.fetch_async(url, method="POST", body="")
        self.assertEqual(response.code, response_code)

        result = json.loads(response.body)

        return result

    @pytest.mark.serial  # Test impacted by https://github.com/pytest-dev/pytest-xdist/issues/620
    @pytest.mark.skipif(not is_main_process(), reason="Serial test")
    @patch("tinybird.kafka_utils.KafkaUtils.get_kafka_topic_group", return_value={"response": "ok"})
    @patch("tinybird.data_connector.DataLinker.redis_client.publish", return_value=None)
    @tornado.testing.gen_test
    async def test_add_linker_when_adding_a_datasource_happy_case(self, publish_mock, _kafka_utils_mock):
        connector = await self._add_kafka_connector({"name": "kafka_connector_1", "service": "kafka"})
        self.connector_id = connector["id"]

        params = {
            "token": self.token,
            "name": "kafka_datasource_1",
            "connector": connector["id"],
            "kafka_topic": "topic_1",
            "kafka_group_id": "kafka_group",
            "kafka_auto_offset_reset": "latest",
        }

        publish_mock.assert_called_once_with(DataConnectorChannels.TBAKAFKA_CONNECTOR, connector["id"])

        publish_mock.reset_mock()

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")

        result = json.loads(response.body)
        datasource = result["datasource"]
        self.assertEqual(datasource["service"], "kafka")
        self.assertEqual(datasource["kafka_topic"], "topic_1")
        self.assertEqual(datasource["kafka_group_id"], "kafka_group")

        linker = DataLinker.get_by_datasource_id(datasource["id"])

        publish_mock.assert_called_once_with(DataConnectorChannels.TBAKAFKA_LINKER, linker.id)

        self.assertEqual(linker.name, f"linker_{datasource['id']}")
        self.assertEqual(linker.data_connector_id, connector["id"])
        self.assertEqual(linker.service, "kafka")
        self.assertEqual(linker.settings["tb_datasource"], datasource["id"])

        self.expect_ops_log(
            {
                "event_type": "create",
                "datasource_name": datasource["name"],
                "options": {"source": "schema", "service": "kafka", "connector": connector["id"]},
            }
        )

    @patch("tinybird.kafka_utils.KafkaUtils.get_kafka_topic_group", return_value={"response": "ok"})
    @tornado.testing.gen_test
    async def test_linker_validation_schema(self, _mock):
        connector = await self._add_kafka_connector({"name": "kafka_connector_1", "service": "kafka"})
        self.connector_id = connector["id"]

        params = {
            "token": self.token,
            "name": "kafka_datasource_1",
            "connector": connector["id"],
            "kafka_topic": "topic_1",
            "kafka_group_id": "kafka_group",
            "kafka_auto_offset_reset": "latest",
            "schema": "mycolumn Int16",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 400, response.body)

    @tornado.testing.gen_test
    async def test_linker_validation_settings_missing_topic(self):
        connector = await self._add_kafka_connector({"name": "kafka_connector_1", "service": "kafka"})
        self.connector_id = connector["id"]

        params = {
            "token": self.token,
            "name": "kafka_datasource_1",
            "connector": connector["id"],
            "group_id": "group1",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        result = json.loads(response.body)

        self.assertEqual(response.code, 400)
        self.assertEqual(ClientErrorBadRequest.required_setting(setting="topic").message, result["error"])

    @tornado.testing.gen_test
    async def test_linker_validation_settings_missing_group_id(self):
        connector = await self._add_kafka_connector({"name": "kafka_connector_1", "service": "kafka"})
        self.connector_id = connector["id"]

        params = {
            "token": self.token,
            "name": "kafka_datasource_1",
            "connector": connector["id"],
            "kafka_topic": "topic_1",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        result = json.loads(response.body)

        self.assertEqual(response.code, 400)
        self.assertEqual(ClientErrorBadRequest.required_setting(setting="group_id").message, result["error"])

    @patch("tinybird.kafka_utils.KafkaUtils.get_kafka_topic_group", return_value={"response": "ok"})
    @tornado.testing.gen_test
    async def test_linker_validation_max_topics(self, _mock):
        u = Users.get_by_id(self.WORKSPACE_ID)
        u.set_user_limit("max_topics", 1, "kafka")
        u.save()

        connector = await self._add_kafka_connector({"name": "kafka_connector_1", "service": "kafka"})
        self.connector_id = connector["id"]

        params = {
            "token": self.token,
            "name": "kafka_datasource_1",
            "connector": connector["id"],
            "kafka_topic": "topic_1",
            "kafka_group_id": "group_id_1",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        result = json.loads(response.body)

        self.assertEqual(response.code, 200)

        params = {
            "token": self.token,
            "name": "kafka_datasource_2",
            "connector": connector["id"],
            "kafka_topic": "topic_2",
            "kafka_group_id": "group_id_2",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        result = json.loads(response.body)

        self.assertEqual(response.code, 400)
        self.assertEqual(ClientErrorBadRequest.max_topics_limit(max_topics=1).message, result["error"])

    @patch("tinybird.kafka_utils.KafkaUtils.get_kafka_topic_group", return_value={"response": "ok"})
    @tornado.testing.gen_test
    async def test_linker_validation_use_topic_once_per_workspace(self, _mock):
        connector = await self._add_kafka_connector({"name": "kafka_connector_1", "service": "kafka"})
        self.connector_id = connector["id"]
        topic = "topic_1"

        params = {
            "token": self.token,
            "name": "kafka_datasource_1",
            "connector": connector["id"],
            "kafka_topic": "topic_1",
            "kafka_group_id": "group_id_1",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        result = json.loads(response.body)

        self.assertEqual(response.code, 200)

        params = {
            "token": self.token,
            "name": "kafka_datasource_2",
            "connector": connector["id"],
            "kafka_topic": "topic_1",
            "kafka_group_id": "group_id_1",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        result = json.loads(response.body)

        self.assertEqual(response.code, 400)
        self.assertEqual(
            ClientErrorBadRequest.topic_repeated_in_workspace(topic=topic, workspace=self.WORKSPACE).message,
            result["error"],
        )

    @patch(
        "tinybird.kafka_utils.KafkaUtils.get_kafka_topic_group",
        return_value={"error": "group_id_already_active_for_topic"},
    )
    @tornado.testing.gen_test
    async def test_linker_validation_consumer_group_cannot_be_used(self, _mock):
        connector = await self._add_kafka_connector({"name": "kafka_connector_1", "service": "kafka"})
        self.connector_id = connector["id"]
        params = {
            "token": self.token,
            "name": "kafka_datasource_1",
            "connector": connector["id"],
            "kafka_topic": "topic_1",
            "kafka_group_id": "group_id_1",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        result = json.loads(response.body)

        self.assertEqual(response.code, 422)
        self.assertEqual(DataConnectorsUnprocessable.auth_groupid_in_use().message, result["error"])

    @patch("tinybird.kafka_utils.KafkaUtils.get_kafka_topic_group", return_value={"response": "ok"})
    @tornado.testing.gen_test
    async def test_linker_validation_settings_auto_offset_reset(self, _mock):
        connector = await self._add_kafka_connector({"name": "kafka_connector_1", "service": "kafka"})
        self.connector_id = connector["id"]

        params = {
            "token": self.token,
            "name": "kafka_datasource_1",
            "connector": connector["id"],
            "kafka_topic": "topic_1",
            "kafka_group_id": "kafka_group",
            "kafka_auto_offset_reset": "wrong",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        result = json.loads(response.body)

        self.assertEqual(response.code, 400)
        self.assertIn("earliest", result["error"])
        self.assertIn("latest", result["error"])

    @patch("tinybird.kafka_utils.KafkaUtils.get_kafka_topic_group", return_value={"response": "ok"})
    @tornado.testing.gen_test
    async def test_linker_datasource_defaults(self, _mock):
        connector = await self._add_kafka_connector({"name": "kafka_connector_1", "service": "kafka"})
        self.connector_id = connector["id"]

        params = {
            "token": self.token,
            "name": "kafka_datasource_1",
            "connector": connector["id"],
            "kafka_topic": "topic_1",
            "kafka_group_id": "kafka_group",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        response = await self.fetch_async(f"/v0/datasources/kafka_datasource_1?token={self.token}")
        self.assertEqual(response.code, 200, response.body)
        datasource = json.loads(response.body)

        columns = datasource["schema"]["columns"]
        datasource_columns = ",".join([f"{column['name']} {column['type']}" for column in columns])
        expected_columns = "__value String,__topic LowCardinality(String),__partition Int16,__offset Int64,__timestamp DateTime,__key String"

        self.assertEqual(datasource_columns, expected_columns)
        self.assertEqual(datasource["engine"]["engine"], "MergeTree")
        self.assertEqual(datasource["engine"]["sorting_key"], "__timestamp")
        self.assertEqual(datasource["engine"]["partition_key"], "toYYYYMM(__timestamp)")
        self.assertEqual(datasource["service"], "kafka")
        self.assertEqual(datasource["kafka_topic"], "topic_1")
        self.assertEqual(datasource["kafka_group_id"], "kafka_group")
        self.assertEqual(datasource["connector"], connector["id"])

        response = await self.fetch_async(f"/v0/datasources?token={self.token}")
        self.assertEqual(response.code, 200, response.body)
        datasources = json.loads(response.body)["datasources"]
        datasource = next((ds for ds in datasources if ds["id"] == datasource["id"]), None)

        self.assertEqual(datasource["service"], "kafka")
        self.assertEqual(datasource["kafka_topic"], "topic_1")
        self.assertEqual(datasource["kafka_group_id"], "kafka_group")
        self.assertEqual(datasource["connector"], connector["id"])

        params = {
            "token": self.token,
            "name": "kafka_datasource_2",
            "persistent": "false",
            "connector": connector["id"],
            "kafka_topic": "topic2",
            "kafka_group_id": "kafka_group2",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        response = await self.fetch_async(f"/v0/datasources/kafka_datasource_2?token={self.token}")
        self.assertEqual(response.code, 200, response.body)
        datasource = json.loads(response.body)

        self.assertEqual(datasource["engine"]["engine"], "Null")

    @patch("tinybird.kafka_utils.KafkaUtils.get_kafka_topic_group", return_value={"response": "ok"})
    @tornado.testing.gen_test
    async def test_linker_datasource_with_headers(self, _mock):
        connector = await self._add_kafka_connector({"name": "kafka_connector_1", "service": "kafka"})
        self.connector_id = connector["id"]

        params = {
            "token": self.token,
            "name": "kafka_datasource_1",
            "connector": connector["id"],
            "kafka_topic": "topic_1",
            "kafka_group_id": "kafka_group",
            "kafka_store_headers": True,
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        response = await self.fetch_async(f"/v0/datasources/kafka_datasource_1?token={self.token}")
        self.assertEqual(response.code, 200, response.body)
        datasource = json.loads(response.body)

        linker = DataLinker.get_by_datasource_id(datasource["id"])
        self.assertEqual(linker.settings["kafka_store_headers"], True)
        self.assertEqual(linker.settings["kafka_store_binary_headers"], True)

        columns = datasource["schema"]["columns"]
        datasource_columns = ",".join([f"{column['name']} {column['type']}" for column in columns])
        expected_columns = "__value String,__topic LowCardinality(String),__partition Int16,__offset Int64,__timestamp DateTime,__key String,__headers Map(String, String)"

        self.assertEqual(datasource_columns, expected_columns)
        self.assertEqual(datasource["engine"]["engine"], "MergeTree")
        self.assertEqual(datasource["engine"]["sorting_key"], "__timestamp")
        self.assertEqual(datasource["engine"]["partition_key"], "toYYYYMM(__timestamp)")
        self.assertEqual(datasource["service"], "kafka")
        self.assertEqual(datasource["kafka_topic"], "topic_1")
        self.assertEqual(datasource["kafka_group_id"], "kafka_group")
        self.assertEqual(datasource["connector"], connector["id"])

        response = await self.fetch_async(f"/v0/datasources?token={self.token}")
        self.assertEqual(response.code, 200, response.body)
        datasources = json.loads(response.body)["datasources"]
        datasource = next((ds for ds in datasources if ds["id"] == datasource["id"]), None)

        self.assertEqual(datasource["service"], "kafka")
        self.assertEqual(datasource["kafka_topic"], "topic_1")
        self.assertEqual(datasource["kafka_group_id"], "kafka_group")
        self.assertEqual(datasource["connector"], connector["id"])

        params = {
            "token": self.token,
            "name": "kafka_datasource_2",
            "persistent": "false",
            "connector": connector["id"],
            "kafka_topic": "topic2",
            "kafka_group_id": "kafka_group2",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        response = await self.fetch_async(f"/v0/datasources/kafka_datasource_2?token={self.token}")
        self.assertEqual(response.code, 200, response.body)
        datasource = json.loads(response.body)

        self.assertEqual(datasource["engine"]["engine"], "Null")

    @patch("tinybird.kafka_utils.KafkaUtils.get_kafka_topic_group", return_value={"response": "ok"})
    @tornado.testing.gen_test
    async def test_linker_datasource_set_engine_settings_noheaders(self, _mock):
        connector = await self._add_kafka_connector({"name": "kafka_connector_1", "service": "kafka"})
        self.connector_id = connector["id"]

        params = {
            "token": self.token,
            "name": "kafka_datasource_1",
            "connector": connector["id"],
            "kafka_topic": "topic_1",
            "kafka_group_id": "kafka_group",
            "engine_sorting_key": "__key",
            "engine_partition_key": "__partition",
            "engine": "ReplacingMergeTree",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        response = await self.fetch_async(f"/v0/datasources/kafka_datasource_1?token={self.token}")
        self.assertEqual(response.code, 200, response.body)
        datasource = json.loads(response.body)

        columns = datasource["schema"]["columns"]
        datasource_columns = ",".join([f"{column['name']} {column['type']}" for column in columns])
        expected_columns = "__value String,__topic LowCardinality(String),__partition Int16,__offset Int64,__timestamp DateTime,__key String"

        self.assertEqual(datasource_columns, expected_columns)
        self.assertEqual(datasource["engine"]["engine"], "ReplacingMergeTree")
        self.assertEqual(datasource["engine"]["sorting_key"], "__key")
        self.assertEqual(datasource["engine"]["partition_key"], "__partition")
        self.assertEqual(datasource["service"], "kafka")
        self.assertEqual(datasource["kafka_topic"], "topic_1")
        self.assertEqual(datasource["kafka_group_id"], "kafka_group")
        self.assertEqual(datasource["connector"], connector["id"])

    @patch("tinybird.kafka_utils.KafkaUtils.get_kafka_topic_group", return_value={"response": "ok"})
    @tornado.testing.gen_test
    async def test_linker_datasource_set_engine_settings_headers(self, _mock):
        connector = await self._add_kafka_connector({"name": "kafka_connector_1", "service": "kafka"})
        self.connector_id = connector["id"]

        params = {
            "token": self.token,
            "name": "kafka_datasource_1",
            "connector": connector["id"],
            "kafka_topic": "topic_1",
            "kafka_group_id": "kafka_group",
            "engine_sorting_key": "__key",
            "engine_partition_key": "__partition",
            "engine": "ReplacingMergeTree",
            "kafka_store_headers": True,
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        response = await self.fetch_async(f"/v0/datasources/kafka_datasource_1?token={self.token}")
        self.assertEqual(response.code, 200, response.body)
        datasource = json.loads(response.body)

        columns = datasource["schema"]["columns"]
        datasource_columns = ",".join([f"{column['name']} {column['type']}" for column in columns])
        expected_columns = "__value String,__topic LowCardinality(String),__partition Int16,__offset Int64,__timestamp DateTime,__key String,__headers Map(String, String)"

        self.assertEqual(datasource_columns, expected_columns)
        self.assertEqual(datasource["engine"]["engine"], "ReplacingMergeTree")
        self.assertEqual(datasource["engine"]["sorting_key"], "__key")
        self.assertEqual(datasource["engine"]["partition_key"], "__partition")
        self.assertEqual(datasource["service"], "kafka")
        self.assertEqual(datasource["kafka_topic"], "topic_1")
        self.assertEqual(datasource["kafka_group_id"], "kafka_group")
        self.assertEqual(datasource["connector"], connector["id"])

    @patch("tinybird.kafka_utils.KafkaUtils.get_kafka_topic_group", return_value={"response": "ok"})
    @tornado.testing.gen_test
    async def test_get_datasource_linker_info(self, _mock):
        connector = await self._add_kafka_connector({"name": "kafka_connector_1", "service": "kafka"})
        self.connector_id = connector["id"]

        params = {
            "token": self.token,
            "name": "kafka_datasource_1",
            "connector": connector["id"],
            "kafka_topic": "topic_1",
            "kafka_group_id": "kafka_group",
            "kafka_auto_offset_reset": "latest",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        response = await self.fetch_async(f"/v0/datasources/kafka_datasource_1?token={self.token}")
        self.assertEqual(response.code, 200, response.body)
        datasource = json.loads(response.body)

        self.assertEqual(datasource["kafka_topic"], "topic_1")
        self.assertEqual(datasource["kafka_group_id"], "kafka_group")
        self.assertEqual(datasource["kafka_auto_offset_reset"], "latest")

    @patch("tinybird.kafka_utils.KafkaUtils.get_kafka_topic_group", return_value={"response": "ok"})
    @patch("tinybird.data_connector.DataLinker.redis_client.publish", return_value=None)
    @tornado.testing.gen_test
    async def test_delete_datasource_deletes_the_linker(self, publish_mock, kafka_utils_mock):
        connector = await self._add_kafka_connector({"name": "kafka_connector_1", "service": "kafka"})
        self.connector_id = connector["id"]

        params = {
            "token": self.token,
            "name": "kafka_datasource_1",
            "connector": connector["id"],
            "kafka_topic": "topic_1",
            "kafka_group_id": "kafka_group",
            "kafka_auto_offset_reset": "latest",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        result = json.loads(response.body)
        datasource = result.get("datasource", None)

        linker = DataLinker.get_by_datasource_id(datasource["id"])
        self.assertIsNotNone(linker)
        publish_mock.reset_mock()

        response = await self.fetch_async(f"/v0/datasources/kafka_datasource_1?token={self.token}", method="DELETE")
        self.assertEqual(response.code, 204, response.body)

        publish_mock.assert_called_once_with(DataConnectorChannels.TBAKAFKA_LINKER, linker.id)

        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": "kafka_datasource_1",
                    "options": {"source": "schema", "service": "kafka", "connector": connector["id"]},
                },
                {
                    "event_type": "delete",
                    "datasource_name": "kafka_datasource_1",
                    "options": {"service": "kafka", "connector": connector["id"]},
                },
            ]
        )

        linker = None

        try:
            linker = DataLinker.get_by_datasource_id(datasource["id"])
        except Exception:
            pass

        self.assertEqual(linker, None)

        response = await self.fetch_async(f"/v0/datasources/kafka_datasource_1?token={self.token}")
        self.assertEqual(response.code, 404)

    @patch("tinybird.kafka_utils.KafkaUtils.get_kafka_topic_group", return_value={"error": "connection_error"})
    @tornado.testing.gen_test
    async def test_add_linker_when_adding_a_datasource_no_broker_connection(self, _mock):
        connector = await self._add_kafka_connector({"name": "kafka_connector_1", "service": "kafka"})
        self.connector_id = connector["id"]
        params = {
            "token": self.token,
            "name": "kafka_datasource_1",
            "connector": connector["id"],
            "kafka_topic": "topic_1",
            "kafka_group_id": "group_id_1",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        result = json.loads(response.body)

        self.assertEqual(response.code, 422)
        self.assertEqual(
            DataConnectorsUnprocessable.unable_to_connect(error="connection_error").message, result["error"]
        )

    @pytest.mark.serial
    @pytest.mark.skipif(not is_main_process(), reason="Serial test")
    @patch("tinybird.kafka_utils.KafkaUtils.get_kafka_topic_group", return_value={"response": "ok"})
    @patch("tinybird.data_connector.DataLinker.redis_client.publish", return_value=None)
    @tornado.testing.gen_test
    async def test_create_kafka_ds_supported_engine_types(self, publish_mock, _kafka_utils_mock):
        connector = await self._add_kafka_connector(
            {
                "name": "kafka_connector_1",
                "service": "kafka",
            }
        )
        self.connector_id = connector["id"]

        async def create_ds(engine: str, engine_ops: Dict[str, str]):
            random_name = f"test_add_kafka_ds_engine_types_{str(uuid.uuid4())[:8]}"
            params = {
                "token": self.token,
                "name": random_name,
                "connector": connector["id"],
                "kafka_topic": random_name,
                "kafka_group_id": "kafka_group",
                "kafka_auto_offset_reset": "latest",
                "engine": engine,
                "schema": "id Int8 `json:$.id`, other Int8 `json:$.other`",
            }
            for k in engine_ops:
                params[k] = engine_ops[k]

            create_url = f"/v0/datasources?{urlencode(params)}"
            response = await self.fetch_async(create_url, method="POST", body="")
            self.assertEqual(response.code, 200, response.body)

            result = json.loads(response.body)
            datasource = result["datasource"]
            self.assertEqual(datasource["service"], "kafka")
            self.assertEqual(datasource["kafka_topic"], random_name)
            self.assertEqual(datasource["kafka_group_id"], "kafka_group")
            self.assertEqual(datasource["engine"]["engine"], engine)
            for k in engine_ops:
                option = k.removeprefix("engine_")
                self.assertEqual(datasource["engine"][option], engine_ops[k])

        await create_ds("MergeTree", {})
        await create_ds("VersionedCollapsingMergeTree", {"engine_sign": "id", "engine_version": "other"})
        await create_ds("CollapsingMergeTree", {"engine_sign": "id"})
        await create_ds("ReplacingMergeTree", {"engine_ver": "id"})

    @pytest.mark.serial
    @pytest.mark.skipif(not is_main_process(), reason="Serial test")
    @patch("tinybird.kafka_utils.KafkaUtils.get_kafka_topic_group", return_value={"response": "ok"})
    @tornado.testing.gen_test
    async def test_add_same_kafka_linker_in_branch(self, _kafka_utils_mock):
        child_workspace, child_token = await self._create_branch()
        connector = await self._add_kafka_connector({"name": "kafka_connector_1", "service": "kafka"})
        self.connector_id = connector["id"]

        # Create Kafka data source in main workspace
        params = {
            "token": self.token,
            "name": "kafka_datasource_1",
            "connector": connector["id"],
            "kafka_topic": "topic_1",
            "kafka_group_id": "kafka_group",
            "kafka_auto_offset_reset": "earliest",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(200, response.code, response.body)

        # Create Kafka data source in branch
        params = {
            "token": child_token,
            "name": "kafka_datasource_1",
            "connector": connector["id"],
            "kafka_topic": "topic_1",
            "kafka_group_id": "kafka_group",
            "kafka_auto_offset_reset": "earliest",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(200, response.code, response.body)

        result = json.loads(response.body)
        datasource = result["datasource"]

        linker = DataLinker.get_by_datasource_id(f"{child_workspace['id']}_{datasource['id']}")

        self.assertEqual("topic_1", linker.settings["kafka_topic"])
        self.assertEqual(f"kafka_group_{child_workspace.name}", linker.settings["kafka_group_id"])
        self.assertEqual("latest", linker.settings["kafka_auto_offset_reset"])
        self.assertEqual(child_workspace.id, linker.settings["branch"])

        self.expect_ops_log(
            {
                "event_type": "create",
                "datasource_name": datasource["name"],
                "options": {"source": "schema", "service": "kafka", "connector": connector["id"]},
            }
        )

    @patch("tinybird.kafka_utils.KafkaUtils.get_kafka_topic_group", return_value={"response": "ok"})
    @tornado.testing.gen_test
    async def test_linker_validation_use_topic_once_per_branch(self, _mock):
        child_workspace, child_token = await self._create_branch()
        connector = await self._add_kafka_connector({"name": "kafka_connector_1", "service": "kafka"})
        self.connector_id = connector["id"]
        topic = "topic_1"

        params = {
            "token": child_token,
            "name": "kafka_datasource_1",
            "connector": connector["id"],
            "kafka_topic": topic,
            "kafka_group_id": "group_id_1",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")

        self.assertEqual(200, response.code, response.body)

        params = {
            "token": child_token,
            "name": "kafka_datasource_2",
            "connector": connector["id"],
            "kafka_topic": topic,
            "kafka_group_id": "group_id_1",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        result = json.loads(response.body)

        self.assertEqual(400, response.code, response.body)
        self.assertEqual(
            ClientErrorBadRequest.topic_repeated_in_branch(topic=topic, branch=child_workspace.name).message,
            result["error"],
        )

    async def _create_branch(self) -> Tuple[User, str]:
        params = {"token": self.token, "name": f"dev_{uuid.uuid4().hex}"}
        url = f"/v0/environments?{urlencode(params)}"
        response = await self.fetch_async(url, method="POST", body="")
        self.assertEqual(200, response.code, response.body)

        job_response = json.loads(response.body)
        job_id = job_response["job"]["id"]
        job = await self.get_finalised_job_async(job_id, token=self.token)
        self.assertEqual(job["progress_percentage"], 100, job)
        self.assertEqual(job["status"], "done", job)

        branch_workspace = User.get_by_id(job["branch_workspace"])

        self.workspaces_to_delete.append(branch_workspace)
        branch_admin_token = branch_workspace.get_token_for_scope(scopes.ADMIN_USER)
        return branch_workspace, branch_admin_token


@pytest.fixture
def use_fake_account_info():
    mock_path = "tinybird.ingest.external_datasources.admin._provision_workspace_service_account"
    fake_account_info = {"service_account_id": "test@project.gserviceaccount.com", "key": "key"}
    with patch(mock_path, return_value=fake_account_info):
        yield


@pytest.mark.usefixtures("use_fake_account_info")
class TestAPISnowflakeDatasource(TestAPIDatasourceBase):
    default_settings = {
        "account": "sf_account",
        "username": "sf_username",
        "password": "sf_password$",
        "role": "sf_role",
        "warehouse": "sf_warehouse",
    }

    def setUp(self):
        super().setUp()

        self.user = Users.get_by_id(self.WORKSPACE_ID)
        self.token = Users.get_token_for_scope(self.user, scopes.ADMIN)
        self.host = self.get_host()
        self.connector_id = None

        CDKUtils.config(
            "export-bucket",
            "composer-bucket",
            "tb-host",
            "test-project",
            "webserver-url",
            "key-location",
            "group-email@tinybird.co",
        )

    def tearDown(self):
        if self.connector_id:
            params = {
                "token": self.token,
            }

            url = f"/v0/connectors/{self.connector_id}?{urlencode(params)}"
            self.fetch(url, method="DELETE")
        super().tearDown()

    async def _add_sf_connector(self, settings=default_settings, response_code=200, token: Optional[str] = None):
        params = {"token": token or self.token, "name": uuid.uuid4().hex, "service": DataConnectors.SNOWFLAKE}

        params.update(settings)

        url = f"/v0/connectors?{urlencode(params)}"
        with patch(
            "tinybird.ingest.external_datasources.connector.CDKConnector.get_integrations",
            return_value=[Integration(SNOWFLAKE_TINYBIRD_INTEGRATION_FORMAT.format(role="sf_role"), "mec")],
        ):
            response = await self.fetch_async(url, method="POST", body="")
            self.assertEqual(response.code, response_code)

            result = json.loads(response.body)
            if response.code == 200:
                self.connector_id = result["id"]

            return result

    async def _create_ds_without_checks(
        self, ds_name_prefix, params=None, response_code=200, token: Optional[str] = None
    ):
        ds_name = f"{ds_name_prefix}_{uuid.uuid4().hex}"
        ds_params = {
            "name": ds_name,
            "schema": "`date` DateTime,`product_id` String,`user_id` Int64,`event` String,`extra_data` String",
            "engine_partition_key": "toYear(date)",
            "engine_sorting_key": "date, extra_data",
            "token": token or self.token,
            "service": DataConnectors.SNOWFLAKE,
            "connector": self.connector_id,
            "cron": "*/60 * * * *",
            "query": "SELECT `date`, `orders.product_id`, someFunction(my_user_id) as `user_id`, IF(`some_field` IS NULL, NULL, TO_JSON(`some_field`, stringify_wide_numbers=>FALSE)) AS `event`, TO_JSON(`some_field`, stringify_wide_numbers=>FALSE) AS `extra_data` FROM orders LIMIT 100",
            "external_data_source": "sf_database.sf_schema.sf_table",
        }

        if params:
            ds_params.update(params)
            # Ugly hack to remove parameters set to None. Otherwise, they'll be translated into
            # the string 'None'
            for key, value in params.items():
                if value is None:
                    del ds_params[key]

        response = await self.fetch_async(f"/v0/datasources?{urlencode(ds_params)}", method="POST", body="")
        self.assertEqual(response.code, response_code)
        return ds_name, response

    async def _create_ds(self, ds_name_prefix, params=None, response_code=200, token: Optional[str] = None):
        ds_name, response = await self._create_ds_without_checks(ds_name_prefix, params, response_code, token)

        if response_code == 200:
            workspace = User.get_by_id(self.WORKSPACE_ID)
            ds = Users.get_datasource(workspace, ds_name).to_json()
            self.assertEqual(ds["connector"], self.connector_id)
            self.assertEqual(ds["service"], DataConnectors.SNOWFLAKE)

            assert response.body

            self.expect_ops_log(
                {
                    "event_type": "create",
                    "datasource_name": ds_name,
                    "options": {
                        "source": "schema",
                        "service": DataConnectors.SNOWFLAKE,
                        "connector": self.connector_id,
                    },
                }
            )

        return json.loads(response.body)

    @tornado.testing.gen_test
    async def test_snowflake_datasource_succeeds(self):
        await self._add_sf_connector()
        with patch(
            "tinybird.ingest.external_datasources.connector.CDKConnector.create_stage",
            return_value={"stage": "sf_stage", "gcp_account": "gcp_account"},
        ):
            with patch("tinybird.views.api_data_linkers.grant_bucket_write_permissions_to_account", return_value=None):
                with patch("tinybird.ingest.cdk_utils.CDKUtils.upload_dag", return_value=None):
                    response = await self._create_ds("test_snowflake_datasource_succeeds")
                    datasource = response["datasource"]
                    self.assertEqual(datasource["service_conf"], None)

                    linker = DataLinker.get_by_datasource_id(datasource["id"])

                    self.assertEqual(linker.name, f"linker_{datasource['id']}")
                    self.assertEqual(linker.data_connector_id, self.connector_id)
                    self.assertEqual(linker.service, DataConnectors.SNOWFLAKE)

    @tornado.testing.gen_test
    async def test_snowflake_datasource_succeeds_with_cron_once(self):
        await self._add_sf_connector()
        with patch(
            "tinybird.ingest.external_datasources.connector.CDKConnector.create_stage",
            return_value={"stage": "sf_stage", "gcp_account": "gcp_account"},
        ):
            with patch("tinybird.views.api_data_linkers.grant_bucket_write_permissions_to_account", return_value=None):
                with patch("tinybird.ingest.cdk_utils.CDKUtils.upload_dag", return_value=None):
                    response = await self._create_ds(
                        "test_snowflake_datasource_succeeds_with_cron_once", {"cron": "@on-demand"}
                    )
                    datasource = response["datasource"]

                    linker = DataLinker.get_by_datasource_id(datasource["id"])

                    self.assertEqual(linker.name, f"linker_{datasource['id']}")
                    self.assertEqual(linker.data_connector_id, self.connector_id)
                    self.assertEqual(linker.service, DataConnectors.SNOWFLAKE)

    @tornado.testing.gen_test
    async def test_snowflake_private_details_are_base64_encoded(self):
        await self._add_sf_connector()
        with patch(
            "tinybird.ingest.external_datasources.connector.CDKConnector.create_stage",
            return_value={"stage": "sf_stage", "gcp_account": "gcp_account"},
        ):
            with patch("tinybird.views.api_data_linkers.grant_bucket_write_permissions_to_account", return_value=None):
                with patch("tinybird.ingest.cdk_utils.CDKUtils.upload_dag", return_value=None):
                    with patch("tinybird.ingest.cdk_utils.CDKUtils.prepare_dag") as mock_prepare_dag:
                        await self._create_ds("test_snowflake_private_details_are_base64_encoded")
                        sf_env = mock_prepare_dag.call_args.args[4]
                        self.assertEqual(
                            base64.b64decode(sf_env["SF_ACCOUNT"]).decode("ascii"),
                            TestAPISnowflakeDatasource.default_settings["account"],
                        )
                        self.assertEqual(
                            base64.b64decode(sf_env["SF_USER"]).decode("ascii"),
                            TestAPISnowflakeDatasource.default_settings["username"],
                        )
                        self.assertEqual(
                            base64.b64decode(sf_env["SF_PWD"]).decode("ascii"),
                            TestAPISnowflakeDatasource.default_settings["password"],
                        )

    @tornado.testing.gen_test
    async def test_snowflake_env_has_all_expected_variables(self):
        await self._add_sf_connector()
        with patch(
            "tinybird.ingest.external_datasources.connector.CDKConnector.create_stage",
            return_value={"stage": "sf_stage", "gcp_account": "gcp_account"},
        ):
            with patch("tinybird.views.api_data_linkers.grant_bucket_write_permissions_to_account", return_value=None):
                with patch("tinybird.ingest.cdk_utils.CDKUtils.upload_dag", return_value=None):
                    with patch("tinybird.ingest.cdk_utils.CDKUtils.prepare_dag") as mock_prepare_dag:
                        await self._create_ds("test_snowflake_env_has_all_expected_variables")
                        sf_env = mock_prepare_dag.call_args.args[4]
                        _ = sf_env["CRON"]
                        _ = sf_env["MODE"]
                        _ = sf_env["SQL_QUERY"]
                        _ = sf_env["SQL_QUERY_AUTOGENERATED"]
                        _ = sf_env["SF_ACCOUNT"]
                        _ = sf_env["SF_USER"]
                        _ = sf_env["SF_PWD"]
                        _ = sf_env["SF_ROLE"]
                        _ = sf_env["SF_WAREHOUSE"]
                        _ = sf_env["SF_DATABASE"]
                        _ = sf_env["SF_SCHEMA"]
                        _ = sf_env["TB_WORKSPACE_ID"]
                        _ = sf_env["SF_STAGE"]
                        _ = sf_env["GCP_SA_KEY"]

    @patch(
        "tinybird.ingest.external_datasources.connector.CDKConnector.create_stage",
        return_value={"stage": "sf_stage", "gcp_account": "gcp_account"},
    )
    @patch("tinybird.views.api_data_linkers.grant_bucket_write_permissions_to_account", return_value=None)
    @patch("tinybird.ingest.cdk_utils.CDKUtils.upload_dag", return_value=None)
    @patch("tinybird.ingest.cdk_utils.datetime")
    @tornado.testing.gen_test
    async def test_snowflake_check_prepare_dag_result(self, mock_datetime, _, __, ___):
        await self._add_sf_connector()
        mock_datetime.now = Mock(return_value=datetime(2024, 1, 1, 9, 0, 0))

        with patch("tinybird.ingest.cdk_utils.CDKUtils.prepare_dag") as mock_prepare_dag:
            ds = await self._create_ds("test_snowflake_check_prepare_dag_result")
            prepare_dag_args = mock_prepare_dag.call_args.args

        expected = f"""
import datetime
import json
import base64

from kubernetes.client import models as k8s
from airflow import models
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from kubernetes.client import models as k8s_models
from datetime import timedelta

with models.DAG(
        dag_id="{self.WORKSPACE_ID}_{ds['datasource']['id']}",
        description="dev DAG",
        default_args={{
            \'depends_on_past\': False,
            \'email_on_failure\': False,
            \'email_on_retry\': False,
            \'retries\': 2,
            \'retry_delay\': timedelta(seconds=60),
            \'retry_exponential_backoff\': True,
            \'max_retry_delay\': timedelta(seconds=300),
            \'task_concurrency\': 1
        }},
        concurrency=1,
        max_active_tasks=1,
        max_active_runs=1,
        schedule_interval="*/60 * * * *",
        tags=["snowflake"],
    ) as dag:

    kubernetes_min_pod = KubernetesPodOperator(
        task_id=\'replace_task\',
        name=\'replace_task\',
        namespace=\'composer-user-workloads\',
        image=\'{CDK_IMAGE_REGISTRY}:{DEFAULT_CDK_VERSION}\',
        # image_pull_secrets=[k8s.V1LocalObjectReference(\'gitlab\')],
        start_date=datetime.datetime.strptime("2024-01-01 07:59:59", "%Y-%m-%d %H:%M:%S"),
        # This two configs below are required since cncf v 5.0.
        # See: https://cloud.google.com/composer/docs/composer-2/use-kubernetes-pod-operator#version-5-0-0
        kubernetes_conn_id=\'kubernetes_default\',
        config_file="/home/airflow/composer_kube_config",
        image_pull_policy="IfNotPresent",
        startup_timeout_seconds=300,
        container_resources=k8s_models.V1ResourceRequirements(
            requests={{"cpu": "100m", "memory": "250M"}},
            limits={{"cpu": "100m", "memory": "250M"}},
        ),
        labels={{"workspace_id": "{self.WORKSPACE_ID}", "datasource_id": "{ds['datasource']['id']}", "external_datasource_kind": "snowflake"}},
        pool="{self.WORKSPACE_ID}_pool",
        env_vars={{
            \'ENVIRONMENT\': "{{{{ var.value.environment }}}}",
            \'SENTRY_DSN\': "{{{{ conn.tb_sentry_dsn.get_uri() }}}}",
            \'TB_WORKSPACE_ID\': "{self.WORKSPACE_ID}",
            \'TB_DATASOURCE_ID\': "{ds['datasource']['id']}",
            \'TB_CDK_TOKEN\': "{prepare_dag_args[3]}",
            \'GCS_BUCKET\': "export-bucket",
            \'TB_CDK_TAG\': "{self.WORKSPACE_ID}_{ds['datasource']['id']}",
            \'GOOGLE_APPLICATION_CREDENTIALS_JSON\': "a2V5",
            \'TB_CDK_ENDPOINT\': "tb-host",
            \'CONNECTOR\': "snowflake",
            \'COMMAND\': "replace",
            \'TB_LOGS_ENDPOINT\': "{{{{ conn.get(\'logs-\').host }}}}",
            \'TB_LOGS_TOKEN\': "{{{{ conn.get(\'logs-\').password }}}}",
            \'TB_LOGS_DATASOURCE\': "{{{{ conn.get(\'logs-\').extra_dejson.datasource_id }}}}",
            \'SQL_QUERY\': "U0VMRUNUIGBkYXRlYCwgYG9yZGVycy5wcm9kdWN0X2lkYCwgc29tZUZ1bmN0aW9uKG15X3VzZXJfaWQpIGFzIGB1c2VyX2lkYCwgSUYoYHNvbWVfZmllbGRgIElTIE5VTEwsIE5VTEwsIFRPX0pTT04oYHNvbWVfZmllbGRgLCBzdHJpbmdpZnlfd2lkZV9udW1iZXJzPT5GQUxTRSkpIEFTIGBldmVudGAsIFRPX0pTT04oYHNvbWVfZmllbGRgLCBzdHJpbmdpZnlfd2lkZV9udW1iZXJzPT5GQUxTRSkgQVMgYGV4dHJhX2RhdGFgIEZST00gb3JkZXJzIExJTUlUIDEwMA==",
            \'SQL_QUERY_AUTOGENERATED\': "False",
            \'ROW_LIMIT\': "50000000",
            \'SF_ACCOUNT\': base64.b64decode("c2ZfYWNjb3VudA==").decode(\'ascii\').replace(\'$\', \'$$\'),
            \'SF_USER\': base64.b64decode("c2ZfdXNlcm5hbWU=").decode(\'ascii\').replace(\'$\', \'$$\'),
            \'SF_PWD\': base64.b64decode("c2ZfcGFzc3dvcmQk").decode(\'ascii\').replace(\'$\', \'$$\'),
            \'SF_ROLE\': "sf_role",
            \'SF_WAREHOUSE\': "sf_warehouse",
            \'SF_DATABASE\': "sf_database",
            \'SF_SCHEMA\': "sf_schema",
            \'SF_STAGE\': "sf_stage",
       }},
    )
"""
        result = CDKUtils.prepare_dag(*prepare_dag_args)
        self.assertEquals(expected, result)

    @patch(
        "tinybird.ingest.external_datasources.connector.CDKConnector.create_stage",
        return_value={"stage": "sf_stage", "gcp_account": "gcp_account"},
    )
    @patch("tinybird.views.api_data_linkers.grant_bucket_write_permissions_to_account", return_value=None)
    @patch("tinybird.ingest.cdk_utils.CDKUtils.upload_dag", return_value=None)
    @patch("tinybird.ingest.cdk_utils.datetime")
    @tornado.testing.gen_test
    async def test_parent_workspace_is_used_in_pool_name_if_branch(self, mock_datetime, _, __, ___):
        child_workspace = self.base_workspace.clone("0.0.0")
        child_token = Users.get_token_for_scope(child_workspace, scopes.ADMIN)
        await self._add_sf_connector(token=child_token)
        mock_datetime.now = Mock(return_value=datetime.strptime("Dec 03 2015", "%b %d %Y"))

        with patch("tinybird.ingest.cdk_utils.CDKUtils.prepare_dag") as mock_prepare_dag:
            await self._create_ds_without_checks("test_snowflake_check_prepare_dag_result", token=child_token)
            prepare_dag_args = mock_prepare_dag.call_args.args

        dag_code = CDKUtils.prepare_dag(*prepare_dag_args)
        assert f'pool="{self.WORKSPACE_ID}_pool"' in dag_code

    @tornado.testing.gen_test
    async def test_snowflake_datasource_fails_with_wrong_mode(self):
        await self._add_sf_connector()
        response = await self._create_ds("test_snowflake_datasource_fails_with_wrong_mode", {"mode": "yijah!"}, 400)
        self.assertEqual(response["error"], ClientErrorBadRequest.service_invalid_mode().message)

    @tornado.testing.gen_test
    async def test_snowflake_datasource_succeeds_without_query(self):
        await self._add_sf_connector()
        with patch("tinybird.views.api_data_linkers.grant_bucket_write_permissions_to_account", return_value=None):
            with patch("tinybird.ingest.cdk_utils.CDKUtils.upload_dag", return_value=None):
                with patch(
                    "tinybird.views.api_data_linkers.get_connector", return_value=AsyncMock
                ) as mock_get_connector:
                    cdk_mock = mock.create_autospec(CDKConnector)
                    mock_get_connector.return_value = cdk_mock
                    cdk_mock.get_extraction_query.return_value = "SELECT `date`, `orders.product_id`, someFunction(my_user_id) as `user_id`, IF(`some_field` IS NULL, NULL, TO_JSON(`some_field`, stringify_wide_numbers=>FALSE)) AS `event`, TO_JSON(`some_field`, stringify_wide_numbers=>FALSE) AS `extra_data` FROM orders LIMIT 100"
                    cdk_mock.create_stage.return_value = {"stage": "sf_stage", "gcp_account": "gcp_account"}

                    response = await self._create_ds(
                        "test_snowflake_datasource_succeeds_without_query", {"query": None}
                    )
                    datasource = response["datasource"]
                    linker = DataLinker.get_by_datasource_id(datasource["id"])
                    self.assertEqual(linker.name, f"linker_{datasource['id']}")
                    self.assertTrue(linker.settings["query_autogenerated"])

    @tornado.testing.gen_test
    async def test_snowflake_datasource_fails_with_credentials_error(self):
        await self._add_sf_connector()
        error = "Invalid credentials"
        with patch(
            "tinybird.ingest.external_datasources.connector.CDKConnector.create_stage",
            side_effect=InvalidGCPCredentials,
        ):
            response = await self._create_ds("test_snowflake_datasource_fails_with_snowflake_error", None, 401)
            self.assertEqual(response["error"], error)

    @tornado.testing.gen_test
    async def test_snowflake_datasource_fails_with_wrong_query(self):
        await self._add_sf_connector()
        response = await self._create_ds(
            "test_snowflake_datasource_fails_with_wrong_query", {"query": "yoqsétio xDxD"}, 400
        )
        self.assertIn("Invalid extraction SQL query", response["error"])

    @tornado.testing.gen_test
    async def test_snowflake_datasource_fails_with_query_and_schema_mismatch(self):
        await self._add_sf_connector()
        response = await self._create_ds(
            "test_snowflake_datasource_fails_with_query_and_schema_mismatch", {"query": "SELECT a, b from pepe"}, 400
        )
        self.assertIn(
            '''Invalid extraction SQL query: Provided query fields "[\'a\', \'b\']" are not a subset of datasource schema "[\'date\', \'product_id\', \'user_id\', \'event\', \'extra_data\']"''',
            response["error"],
        )

    @tornado.testing.gen_test
    async def test_snowflake_datasource_fails_without_external_datasource(self):
        await self._add_sf_connector()
        response = await self._create_ds(
            "test_snowflake_datasource_fails_without_external_datasource", {"external_data_source": None}, 400
        )
        self.assertEqual(response["error"], ClientErrorBadRequest.external_datasource_required().message)

    @tornado.testing.gen_test
    async def test_snowflake_datasource_fails_with_invalid_gcp_credentials(self):
        await self._add_sf_connector()
        with patch("tinybird.views.api_data_linkers.get_connector", side_effect=InvalidGCPCredentials):
            response = await self._create_ds("test_snowflake_datasource_fails_with_invalid_gcp_credentials", None, 401)
            self.assertEqual(response["error"], "Invalid credentials")

    @tornado.testing.gen_test
    async def test_snowflake_datasource_fails_with_snowflake_error(self):
        await self._add_sf_connector()
        error = "my own error"
        with patch(
            "tinybird.ingest.external_datasources.connector.CDKConnector.create_stage",
            side_effect=snowflake.connector.errors.Error(msg=error),
        ):
            response = await self._create_ds("test_snowflake_datasource_fails_with_snowflake_error", None, 403)
            self.assertEqual(response["error"], error)

    @tornado.testing.gen_test
    async def test_snowflake_datasource_fails_with_snowflake_grant_access_error(self):
        await self._add_sf_connector()
        error = "SQL access control error:\Insufficient privileges to operate on schema 'PUBLIC'"
        with patch(
            "tinybird.ingest.external_datasources.connector.CDKConnector.create_stage",
            side_effect=snowflake.connector.errors.Error(msg=error),
        ):
            response = await self._create_ds("test_snowflake_datasource_fails_with_snowflake_error", None, 403)
            self.assertIn(error, response["error"])
            self.assertIn(
                "Try granting access to the database for your role executing 'grant create stage on all schemas in database sf_database to role sf_role;'",
                response["error"],
            )

    @tornado.testing.gen_test
    async def test_snowflake_datasource_fails_granting_access_to_gcp_bucket(self):
        await self._add_sf_connector()
        with patch(
            "tinybird.ingest.external_datasources.connector.CDKConnector.create_stage",
            return_value={"stage": "sf_stage", "gcp_account": "gcp_account"},
        ):
            with patch("tinybird.views.api_data_linkers.grant_bucket_write_permissions_to_account") as gcp_mock:
                error = "my own error"
                status_code = 401

                # We can't create a mock of an exception because it wouldn't inherit from a base
                # exception and Python complains about it when trying to catch it. So, alternatively we
                # create a fake exception to be thrown that uses internally something that we can easily
                # mock.
                resp = MagicMock()
                exception = googleapiclient.errors.HttpError(resp, b"")
                exception.reason = error
                resp.status = status_code
                gcp_mock.side_effect = exception
                response = await self._create_ds(
                    "test_snowflake_datasource_fails_granting_access_to_gcp_bucket", None, status_code
                )
                self.assertEqual(response["error"], error)

    @tornado.testing.gen_test
    async def test_snowflake_datasource_fails_with_invalid_role(self):
        connector = await self._add_sf_connector()

        # Update with an invalid role in Redis' DB directly to bypass the security
        # check included in the connectors API.
        with DataConnector.transaction(connector["id"]) as data_connector:
            data_connector.update_settings({"role": "invalid role"})

        response = await self._create_ds("test_snowflake_datasource_fails_with_invalid_role", None, 403)
        self.assertEqual(
            response["error"], 'Invalid role "invalid role". Only alphanumeric and underscore characters allowed'
        )


class TestBackPressureControlImportUrl(TestAPIDatasourceBase):
    async def _send_simple_multipart_file(self, ds_name, file_name=None, mode="create"):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.DATASOURCES_CREATE)
        url = self.get_url(f"/v0/datasources?token={token}&name={ds_name}&mode={mode}")
        if not file_name:
            file_name = "simple.csv"
        with fixture_file(file_name, mode="rb") as fd:
            response = await self.fetch_stream_upload_async(url, fd)
        return response

    @tornado.testing.gen_test
    @patch("tinybird.csv_processing_queue.CsvChunkQueue.blocks_waiting", return_value=0)
    @patch("asyncio.sleep")
    async def test_backpressure_multipart_queue_empty_must_not_wait(self, sleep_mock, blocks_waiting_mock):
        response = await self._send_simple_multipart_file("test_backpressure_multipart_queue_empty_must_not_wait")
        self.assertEqual(response.code, 200, response.body)
        sleep_mock.assert_not_called()

    @tornado.testing.gen_test
    @patch("tinybird.csv_processing_queue.CsvChunkQueue.blocks_waiting")
    @patch("asyncio.sleep")
    @patch("streaming_form_data.StreamingFormDataParser.data_received")
    async def test_backpressure_multipart_queue_almostfull_wait_one_time_per_chunk(
        self, mock_chunk_received, sleep_mock, blocks_waiting_mock
    ):
        queue_size = CSVImporterSettings.MAX_MEMORY_IN_PROCESS_QUEUE // CSVImporterSettings.CHUNK_SIZE
        blocks_waiting_mock.return_value = queue_size
        response = await self._send_simple_multipart_file(
            "test_backpressure_multipart_queue_almostfull_wait_one_time_per_chunk"
        )
        self.assertEqual(response.code, 200, response.body)
        sleep_mock.assert_called_with(STREAM_BACKPRESSURE_WAIT)
        assert sleep_mock.call_count == mock_chunk_received.call_count

    @tornado.testing.gen_test
    @patch("tinybird.csv_processing_queue.CsvChunkQueue.blocks_waiting")
    @patch("asyncio.sleep")
    @patch("streaming_form_data.StreamingFormDataParser.data_received")
    async def test_backpressure_multipart_queue_full_wait_max_time_time_per_chunk(
        self, mock_chunk_received, sleep_mock, blocks_waiting_mock
    ):
        queue_size = 1 + CSVImporterSettings.MAX_MEMORY_IN_PROCESS_QUEUE // CSVImporterSettings.CHUNK_SIZE
        blocks_waiting_mock.return_value = queue_size
        response = await self._send_simple_multipart_file(
            "test_backpressure_multipart_queue_full_wait_max_time_time_per_chunk"
        )
        self.assertEqual(response.code, 200, response.body)
        # the comprarison is not exact due to float limitations
        assert sleep_mock.call_count >= mock_chunk_received.call_count * (
            STREAM_BACKPRESSURE_MAX_WAIT / STREAM_BACKPRESSURE_WAIT
        )

    @tornado.testing.gen_test
    @patch("tinybird.views.api_datasources_import.CustomTarget.first_block_finished", return_value=False)
    @patch("tinybird.views.api_datasources_import.CustomTarget.table_exists", return_value=False)
    @patch("tinybird.views.api_datasources_import.MAX_WAITING_BLOCKS", new=0)
    async def test_backpressure_error_creating_ds(self, _, __):
        ds_name = "test_backpressure_creating_ds"
        response = await self._send_simple_multipart_file(ds_name, "stock_prices_800K.csv")
        self.assertEqual(response.code, 500, response.body)
        assert "Max queued blocks on stream uploading" in json.loads(response.body)["error"]
        self.expect_ops_log(
            [
                {"event_type": "create", "datasource_name": ds_name, "result": "ok"},
                {
                    "event_type": "append",
                    "datasource_name": ds_name,
                    "result": "error",
                    "error": "Max queued blocks on stream uploading",
                },
            ]
        )

    @tornado.testing.gen_test
    async def test_not_wait_to_first_block_if_ds_exists(self):
        ds_name = "test_not_wait_to_first_block_if_ds_exists"

        response = await self._send_simple_multipart_file(ds_name, "stock_prices_800K.csv", mode="create")
        self.assertEqual(response.code, 200, response.body)

        response = await self._send_simple_multipart_file(ds_name, "stock_prices_800K.csv", mode="append")
        self.assertEqual(response.code, 200, response.body)

        self.expect_ops_log(
            [
                {"event_type": "create", "datasource_name": ds_name, "result": "ok"},
                {
                    "event_type": "append",
                    "datasource_name": ds_name,
                    "result": "ok",
                    "rows": 800000,
                },
                {
                    "event_type": "append",
                    "datasource_name": ds_name,
                    "result": "ok",
                    "rows": 800000,
                },
            ]
        )


class TestAPIDatasourceImportBatchMaxSize(TestAPIDatasourceBase):
    @tornado.testing.gen_test
    async def test_max_size_ndjson_url_dev_plan(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        ndjson_url = "https://storage.googleapis.com/tb-tests/events.ndjson"

        import_url = f"/v0/datasources?token={token}&url={ndjson_url}&name=import_ndjson"
        response = await self.fetch_async(import_url, method="POST", body="")

        result = json.loads(response.body)
        job1_id = result["id"]
        job1 = await self.get_finalised_job_async(job1_id)

        self.assertEqual(job1.status, "error", str(job1))
        expected_error = "the limit is 10.00 GB."
        self.assertIn(expected_error, job1["errors"][0])

    @tornado.testing.gen_test
    async def test_max_size_csv_url_dev_plan(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        csv_url = "https://storage.googleapis.com/tb-tests/events_100.csv"

        import_url = f"/v0/datasources?token={token}&url={csv_url}&name=import_csv"
        response = await self.fetch_async(import_url, method="POST", body="")

        result = json.loads(response.body)
        job1_id = result["id"]
        job1 = await self.get_finalised_job_async(job1_id)
        self.assertEqual(job1.status, "error", str(job1))
        expected_error = "the limit is 10.00 GB."
        self.assertIn(expected_error, job1["errors"][0])


class TestUTCTimeZone(TestAPIDatasourceBase):
    def setUp(self):
        super().setUp()
        self.u = Users.get_by_id(self.WORKSPACE_ID)
        self.token = Users.get_token_for_scope(self.u, scopes.ADMIN)
        self.initial_data_query = """
            SELECT
                (toDate('2019-01-30') + dc.d) + toIntervalHour(h.number) AS dt,
                dc.country,
                1 AS units
            FROM
            (
                SELECT * FROM
                (
                    SELECT number AS d
                    FROM system.numbers
                    LIMIT 4
                )
                CROSS JOIN
                (
                    SELECT if(number = 1, 'ES', 'US') as country
                    FROM system.numbers
                    LIMIT 2
                )
            ) AS dc
            CROSS JOIN
            (
                SELECT number
                FROM system.numbers
                LIMIT 24
            ) AS h
            FORMAT CSVWithNames
        """

    @tornado.testing.gen_test
    async def test_insert_csv_through_clickhouse_local(self):
        rand = str(uuid.uuid4())[:8]
        landing_name = f"sales_landing_{rand}"
        await self.create_datasource_async(
            self.token,
            landing_name,
            """
            dt DateTime,
            country String,
            units Int32
        """,
            {"engine": "MergeTree", "engine_partition_key": "toYYYYMM(dt)", "engine_sorting_key": "country, dt"},
        )

        csv_url = self.get_url_for_sql(self.initial_data_query)
        params = {
            "token": self.token,
            "name": landing_name,
            "mode": "append",
            "url": csv_url,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done")

        self.expect_ops_log({"event_type": "append", "datasource_name": landing_name, "options": {"source": csv_url}})

        self.wait_for_datasource_replication(self.u, landing_name)

        landing_results = await self._query(
            query=f"""
            SELECT
                toDate(dt) as d,
                sum(units) as sum_units
            FROM {landing_name}
            GROUP BY d
            ORDER BY d ASC
            FORMAT JSON
        """
        )

        # Validate current data
        self.assertEqual(len(landing_results["data"]), 4)
        self.assertEqual(list(landing_results["data"][0].values()), ["2019-01-30", 48])
        self.assertEqual(list(landing_results["data"][1].values()), ["2019-01-31", 48])
        self.assertEqual(list(landing_results["data"][2].values()), ["2019-02-01", 48])
        self.assertEqual(list(landing_results["data"][3].values()), ["2019-02-02", 48])


class TestAPIPreviewXXXDatasource(TestAPIDatasourceBase):
    def setUp(self):
        super().setUp()

        self.user = Users.get_by_id(self.WORKSPACE_ID)
        self.token = Users.get_token_for_scope(self.user, scopes.ADMIN)
        self.host = self.get_host()
        self.connector_id = None

    def tearDown(self):
        if self.connector_id:
            params = {
                "token": self.token,
            }

            url = f"/v0/connectors/{self.connector_id}?{urlencode(params)}"
            self.fetch(url, method="DELETE")
        super().tearDown()

    @abstractmethod
    def _create_connector_params(
        self,
        settings,
    ):
        pass

    async def _add_connector(
        self,
        settings,
        response_code=200,
    ):
        params = self._create_connector_params(settings)

        url = f"/v0/connectors?{urlencode(params)}"
        response = await self.fetch_async(url, method="POST", body="")
        self.assertEqual(response.code, response_code)

        result = json.loads(response.body)

        return result

    async def _create_preview_datasource_happy_case(
        self,
        service,
        connector_name,
        params,
    ):
        settings = {
            "name": connector_name,
            "service": service,
        }
        connector = await self._add_connector(settings)
        self.connector_id = connector["id"]

        params["connector"] = connector["id"]
        params["schema"] = "column1 String `json:$.column1`, column2 Int32 `json:$.column2`"

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body=json.dumps(params).encode("utf-8"))

        result = json.loads(response.body)
        datasource_id = result["datasource"]["id"]
        self.assertEqual(response.code, 200)
        self.assertIsNotNone(datasource_id)

        linker = DataLinker.get_by_datasource_id(datasource_id)
        self.assertEqual(linker.service, service)

        datasource = result["datasource"]
        return datasource, linker, connector

    async def _create_preview_datasource_with_schema_happy_case(
        self,
        service,
        connector_name,
        params,
    ):
        settings = {
            "name": connector_name,
            "service": service,
        }
        connector = await self._add_connector(settings)
        self.connector_id = connector["id"]

        params["connector"] = connector["id"]
        params["schema"] = "column1 String `json:$.column1`, column2 Int32 `json:$.column2`"

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body=json.dumps(params).encode("utf-8"))

        result = json.loads(response.body)

        self.assertEqual(response.code, 200)

        linker = DataLinker.get_by_datasource_id(result["datasource"]["id"])
        self.assertEqual(result["datasource"]["name"], params["name"])
        self.assertEqual(linker.service, service)

    async def _create_preview_datasource_missing_parameter(
        self,
        service,
        connector_name,
        params,
        param_to_remove,
        expected_error_code,
        expected_error_message,
    ):
        settings = {
            "name": connector_name,
            "service": service,
        }
        connector = await self._add_connector(settings)
        self.connector_id = connector["id"]

        params["connector"] = connector["id"]
        params_copy = params.copy()
        del params_copy[param_to_remove]

        create_url = f"/v0/datasources?{urlencode(params_copy)}"
        response = await self.fetch_async(create_url, method="POST", body="")

        result = json.loads(response.body)

        self.assertEqual(response.code, expected_error_code)
        self.assertEqual(result, expected_error_message)

    async def _create_preview_datasource_file_extension_not_supported(self, service, connector_name, params):
        settings = {
            "name": connector_name,
            "service": service,
        }
        connector = await self._add_connector(settings)
        self.connector_id = connector["id"]

        params["connector"] = connector["id"]

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")

        result = json.loads(response.body)

        self.assertEqual(response.code, 400)
        self.assertEqual(
            result,
            {
                "error": "File extension not supported. Valid extensions are: ['csv', 'csv.gz', 'ndjson', 'ndjson.gz', 'jsonl', 'jsonl.gz', 'json', 'json.gz', 'parquet', 'parquet.gz']. Valid data formats are: ['csv', 'ndjson', 'parquet']"
            },
        )

    async def _create_preview_datasource_invalid_from_time(self, service, connector_name, params):
        settings = {
            "name": connector_name,
            "service": service,
        }
        connector = await self._add_connector(settings)
        self.connector_id = connector["id"]

        params["connector"] = connector["id"]

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")

        result = json.loads(response.body)

        self.assertEqual(response.code, 400)
        self.assertEqual(
            result,
            {"error": f"'{params['from_time']}' isn't a valid value for parameter 'from_time'"},
        )

    async def _create_preview_datasource_not_all_required_params_from_yepcode(
        self,
        service,
        connector_name,
        params,
    ):
        settings = {
            "name": connector_name,
            "service": service,
        }
        connector = await self._add_connector(settings)
        self.connector_id = connector["id"]

        params["connector"] = connector["id"]

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body=json.dumps(params).encode("utf-8"))

        result = json.loads(response.body)

        self.assertEquals(response.code, 400)
        self.assertEquals(result, {"error": "Missing params"})

    async def _create_preview_datasource_unknown_error_from_yepcode(
        self,
        service,
        connector_name,
        params,
    ):
        settings = {
            "name": connector_name,
            "service": service,
        }
        connector = await self._add_connector(settings)
        self.connector_id = connector["id"]

        params["connector"] = connector["id"]

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body=json.dumps(params).encode("utf-8"))

        result = json.loads(response.body)

        self.assertEquals(response.code, 400)
        self.assertEquals(result, {"error": "Unknown error"})


class TestAPIPreviewS3Datasource(TestAPIPreviewXXXDatasource):
    def _create_connector_params(self, settings):
        connector_settings = {
            "s3_access_key_id": "mock_s3_access_key_id",
            "s3_secret_access_key": "mock_s3_secret_access_key",
            "s3_region": "mock_s3_region",
        }

        params = {"token": self.token}

        params.update(settings | connector_settings)

        return params

    @patch(
        "tinybird.ingest.preview_connectors.amazon_s3_connector.S3PreviewConnector.link_connector",
        return_value={"message": "Datasource is being created"},
    )
    @patch("tinybird.ingest.preview_connectors.amazon_s3_connector.S3PreviewConnector.execute_now", return_value={})
    @tornado.testing.gen_test
    async def test_create_s3_preview_datasource_happy_case(self, _, __):
        connector_name = "test_create_s3_preview_datasource_happy_case"

        params = {
            "token": self.token,
            "bucket_uri": "bucket_uri.csv",
            "name": "s3_datasource_1",
            "service": DataConnectors.AMAZON_S3,
        }

        datasource, linker, connector = await self._create_preview_datasource_happy_case(
            service=DataConnectors.AMAZON_S3,
            connector_name=connector_name,
            params=params,
        )

        s3_token_name = get_token_name(connector.get("name"), datasource.get("name"))
        workspace = Users.get_by_id(self.WORKSPACE_ID)
        s3_token = Users.get_token(workspace, s3_token_name)
        self.assertTrue(s3_token)

    @patch(
        "tinybird.ingest.preview_connectors.amazon_s3_connector.S3PreviewConnector.link_connector",
        return_value={"message": "Datasource is being created"},
    )
    @patch("tinybird.ingest.preview_connectors.amazon_s3_connector.S3PreviewConnector.execute_now", return_value={})
    @tornado.testing.gen_test
    async def test_create_s3_preview_datasource_drop_token(self, _, __):
        connector_name = "test_create_s3_preview_datasource_drop_token"

        params = {
            "token": self.token,
            "bucket_uri": "bucket_uri.csv",
            "name": "s3_datasource_1",
            "service": DataConnectors.AMAZON_S3,
        }

        datasource, linker, connector = await self._create_preview_datasource_happy_case(
            service=DataConnectors.AMAZON_S3,
            connector_name=connector_name,
            params=params,
        )

        datasource_name = datasource.get("name")
        s3_token_name = get_token_name(connector.get("name"), datasource_name)
        workspace = Users.get_by_id(self.WORKSPACE_ID)
        s3_token = Users.get_token(workspace, s3_token_name)
        self.assertTrue(s3_token)

        admin_token = Users.get_token_for_scope(workspace, scopes.ADMIN)

        params = {"token": admin_token, "new_name": "whatever"}
        response = await self.fetch_async(f"/v0/tokens/{s3_token_name}?{urlencode(params)}", method="PUT", body="")
        self.assertEqual(response.code, 403)
        self.assertEqual(
            json.loads(response.body).get("error"),
            f"Forbidden: token {s3_token_name} is being used in s3 Data Source '{datasource_name}'",
        )

        params = {"token": admin_token}
        response = await self.fetch_async(f"/v0/tokens/{s3_token_name}?{urlencode(params)}", method="DELETE")
        self.assertEqual(response.code, 403)
        self.assertEqual(
            json.loads(response.body).get("error"),
            f"Forbidden: token {s3_token_name} is being used in s3 Data Source '{datasource_name}'",
        )

        params = {"token": admin_token}
        response = await self.fetch_async(
            f"/v0/tokens/{s3_token_name}/refresh?{urlencode(params)}", method="POST", body=""
        )
        self.assertEqual(response.code, 403)
        self.assertEqual(
            json.loads(response.body).get("error"),
            f"Forbidden: token {s3_token_name} is being used in s3 Data Source '{datasource_name}'",
        )

    @patch(
        "tinybird.ingest.preview_connectors.amazon_s3_connector.S3PreviewConnector.link_connector",
        return_value={"message": "Datasource is being created"},
    )
    @patch("tinybird.ingest.preview_connectors.amazon_s3_connector.S3PreviewConnector.execute_now", return_value={})
    @tornado.testing.gen_test
    async def test_s3_datasource_drop_user_token_regression(self, _, __):
        connector_name = "test_s3_datasource_drop_token_regression"
        new_user = UserAccount.register(f"test{uuid.uuid4().hex}@developeruser.co")
        self.users_to_delete.append(new_user)
        await Users.add_users_to_workspace_async(self.WORKSPACE_ID, [new_user.email], None)

        workspace = Users.get_by_id(self.WORKSPACE_ID)
        admin_token = Users.get_token_for_scope(workspace, scopes.ADMIN)
        new_user_token = workspace.get_tokens_for_resource(new_user.id, scopes.ADMIN_USER)[0]

        with patch("tinybird.user.Users.add_data_source_connector_token_async", return_value=new_user_token):
            params = {
                "token": self.token,
                "bucket_uri": "bucket_uri.csv",
                "name": "s3_datasource_1",
                "service": DataConnectors.AMAZON_S3,
            }

            datasource, linker, connector = await self._create_preview_datasource_happy_case(
                service=DataConnectors.AMAZON_S3,
                connector_name=connector_name,
                params=params,
            )

        params = {"token": admin_token, "new_name": "whatever"}
        response = await self.fetch_async(f"/v0/tokens/{new_user_token}?{urlencode(params)}", method="PUT", body="")
        self.assertEqual(response.code, 403)
        self.assertEqual(
            json.loads(response.body).get("error"),
            f"Forbidden: token admin {new_user.email} is being used in one or more connected Data Sources.",
        )

        params = {"token": admin_token}
        response = await self.fetch_async(f"/v0/tokens/{new_user_token}?{urlencode(params)}", method="DELETE")
        self.assertEqual(response.code, 403)
        self.assertEqual(
            json.loads(response.body).get("error"),
            f"Forbidden: token admin {new_user.email} is being used in one or more connected Data Sources.",
        )

        params = {"token": admin_token}
        response = await self.fetch_async(
            f"/v0/tokens/{new_user_token}/refresh?{urlencode(params)}", method="POST", body=""
        )
        self.assertEqual(response.code, 403)
        self.assertEqual(
            json.loads(response.body).get("error"),
            f"Forbidden: token admin {new_user.email} is being used in one or more connected Data Sources.",
        )

        user_account = UserAccount.get_by_id(self.USER_ID)
        user_account_token = UserAccounts.get_token_for_scope(user_account, scopes.AUTH)
        params = {"token": user_account_token, "operation": "remove", "users": new_user.email}
        url = f"/v0/workspaces/{workspace.id}/users?{urlencode(params)}"
        response = await self.fetch_async(url, method="PUT", body="")
        self.assertEqual(response.code, 200)

        # Token remains
        workspace = Users.get_by_id(self.WORKSPACE_ID)
        new_user_token_check = workspace.get_tokens_for_resource(new_user.id, scopes.ADMIN_USER)[0]
        self.assertEqual(new_user_token, new_user_token_check)

    @patch(
        "tinybird.ingest.preview_connectors.amazon_s3_connector.S3PreviewConnector.link_connector",
        return_value={"message": "Datasource is being created"},
    )
    @patch("tinybird.ingest.preview_connectors.amazon_s3_connector.S3PreviewConnector.execute_now", return_value={})
    @tornado.testing.gen_test
    async def test_create_s3_preview_datasource_with_schema_happy_case(self, _, __):
        connector_name = "test_create_s3_preview_datasource_with_schema_happy_case"

        params = {
            "token": self.token,
            "bucket_uri": "bucket_uri.csv",
            "name": "s3_datasource_1",
            "service": DataConnectors.AMAZON_S3,
        }

        await self._create_preview_datasource_with_schema_happy_case(
            service=DataConnectors.AMAZON_S3,
            connector_name=connector_name,
            params=params,
        )

    @patch(
        "tinybird.ingest.preview_connectors.amazon_s3_connector.S3PreviewConnector.link_connector",
        return_value={"message": "Datasource is being created"},
    )
    @patch("tinybird.ingest.preview_connectors.amazon_s3_connector.S3PreviewConnector.execute_now", return_value={})
    @tornado.testing.gen_test
    async def test_create_s3_preview_datasource_with_schema_upper_case(self, _, __):
        connector_name = "test_create_s3_preview_datasource_with_schema_upper_case"

        params = {
            "token": self.token,
            "bucket_uri": "bucket_uri.csv",
            "name": f"S3_datasource_1{uuid.uuid4().hex}",
            "service": DataConnectors.AMAZON_S3,
        }

        await self._create_preview_datasource_with_schema_happy_case(
            service=DataConnectors.AMAZON_S3,
            connector_name=connector_name,
            params=params,
        )

    @patch(
        "tinybird.ingest.preview_connectors.amazon_s3_connector.S3PreviewConnector.link_connector",
        return_value={"message": "Datasource is being created"},
    )
    @patch("tinybird.ingest.preview_connectors.amazon_s3_connector.S3PreviewConnector.execute_now", return_value={})
    @tornado.testing.gen_test
    async def test_create_s3_preview_datasource_with_sorting_key_happy_case(self, _, __):
        connector_name = "test_create_s3_preview_datasource_with_engine_happy_case"

        settings = {
            "name": connector_name,
            "service": DataConnectors.AMAZON_S3,
        }

        connector = await self._add_connector(settings)
        self.connector_id = connector["id"]

        params = {
            "connector": connector["id"],
            "schema": "column1 String `json:$.column1`, column2 Int32 `json:$.column2`",
            "token": self.token,
            "bucket_uri": "bucket_uri.csv",
            "name": "s3_datasource__with_sorting_key_1",
            "service": DataConnectors.AMAZON_S3,
            "engine_sorting_key": "column1",
        }

        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body=json.dumps(params).encode("utf-8"))

        result = json.loads(response.body)

        self.assertEqual(response.code, 200)

        self.assertEqual(result["datasource"]["engine"]["sorting_key"], "column1")

        linker = DataLinker.get_by_datasource_id(result["datasource"]["id"])
        self.assertEqual(linker.service, DataConnectors.AMAZON_S3)

    @tornado.testing.gen_test
    async def test_create_s3_preview_datasource_missing_parameter(self):
        params = {
            "token": self.token,
            "bucket_uri": "bucket_uri.csv",
            "name": "s3_datasource_1",
            "service": DataConnectors.AMAZON_S3,
            "schema": "test String `json:$.test`",
        }
        params_to_remove = [
            ("bucket_uri", 400, {"error": "Missing param: bucket_uri"}),
            ("name", 400, {"error": "Missing param: name"}),
        ]

        for n, row in enumerate(params_to_remove):
            connector_name = f"test_create_s3_preview_datasource_missing_parameter_{n}"
            param_to_remove, expected_error_code, expected_error_message = row
            await self._create_preview_datasource_missing_parameter(
                service=DataConnectors.AMAZON_S3,
                connector_name=connector_name,
                params=params,
                param_to_remove=param_to_remove,
                expected_error_code=expected_error_code,
                expected_error_message=expected_error_message,
            )

    @tornado.testing.gen_test
    async def test_create_s3_preview_datasource_file_extension_not_supported(self):
        connector_name = "test_create_s3_preview_datasource_file_extension_not_supported"
        params = {
            "token": self.token,
            "bucket_uri": "bucket_uri.whatever",
            "name": "s3_datasource_1",
            "service": DataConnectors.AMAZON_S3,
            "schema": "test String `json:$.test`",
        }

        await self._create_preview_datasource_file_extension_not_supported(
            service=DataConnectors.AMAZON_S3, connector_name=connector_name, params=params
        )

    @patch(
        "tinybird.ingest.preview_connectors.amazon_s3_connector.S3PreviewConnector.link_connector",
        return_value={"message": "Datasource is being created"},
    )
    @patch("tinybird.ingest.preview_connectors.amazon_s3_connector.S3PreviewConnector.execute_now", return_value={})
    @tornado.testing.gen_test
    async def test_create_s3_preview_datasource_extensions_supported(self, _, __):
        params = {
            "token": self.token,
            "service": DataConnectors.AMAZON_S3,
        }

        valid_extensions = [
            "csv",
            "csv.gz",
            "ndjson",
            "ndjson.gz",
            "jsonl",
            "jsonl.gz",
            "json",
            "json.gz",
            "parquet",
            "parquet.gz",
        ]

        with User.transaction(self.WORKSPACE_ID) as user:
            limit = len(valid_extensions) * 2
            user.set_rate_limit_config("api_datasources_create_append_replace", limit, 60, limit)
            user.set_rate_limit_config("api_connectors_create", limit, 60, limit)

        for extension in valid_extensions:
            connector_name = f"test_create_s3_preview_datasource_extension_{extension}"
            params_copy = params.copy()
            params_copy["bucket_uri"] = f"bucket_uri.{extension}"
            params_copy["name"] = f"s3_datasource_1_{extension}"
            await self._create_preview_datasource_happy_case(
                service=DataConnectors.AMAZON_S3, connector_name=connector_name, params=params_copy
            )

    @tornado.testing.gen_test
    async def test_create_s3_preview_datasource_invalid_from_time(self):
        connector_name = "test_create_s3_preview_datasource_invalid_from_time"
        params = {
            "token": self.token,
            "bucket_uri": "bucket_uri.csv",
            "name": "s3_datasource_1",
            "service": DataConnectors.AMAZON_S3,
            "schema": "test String `json:$.test`",
            "from_time": "fake",
        }

        await self._create_preview_datasource_invalid_from_time(
            service=DataConnectors.AMAZON_S3, connector_name=connector_name, params=params
        )

    @patch(
        "tinybird.ingest.preview_connectors.amazon_s3_connector.S3PreviewConnector.link_connector",
        side_effect=ConnectorException("Not all required params"),
    )
    @tornado.testing.gen_test
    async def test_create_s3_preview_datasource_not_all_required_params_from_yepcode(self, _):
        connector_name = "test_create_s3_preview_datasource_not_all_required_params_from_yepcode"
        params = {
            "token": self.token,
            "bucket_uri": "bucket_uri.csv",
            "name": "s3_datasource_1",
            "service": DataConnectors.AMAZON_S3,
            "schema": "test String `json:$.test`",
        }

        await self._create_preview_datasource_not_all_required_params_from_yepcode(
            service=DataConnectors.AMAZON_S3,
            connector_name=connector_name,
            params=params,
        )

    @patch(
        "tinybird.ingest.preview_connectors.amazon_s3_connector.S3PreviewConnector.link_connector",
        side_effect=ConnectorException("Wadus"),
    )
    @tornado.testing.gen_test
    async def test_create_s3_preview_datasource_unknown_error_from_yepcode(self, _):
        connector_name = "test_create_s3_preview_datasource_unknown_error_from_yepcode"
        params = {
            "token": self.token,
            "bucket_uri": "bucket_uri.csv",
            "name": "s3_datasource_1",
            "service": DataConnectors.AMAZON_S3,
            "schema": "test String `json:$.test`",
        }

        await self._create_preview_datasource_unknown_error_from_yepcode(
            service=DataConnectors.AMAZON_S3,
            connector_name=connector_name,
            params=params,
        )


class TestAPIPreviewGCSSADatasource(TestAPIPreviewXXXDatasource):
    def _create_connector_params(self, settings):
        connector_settings = {
            "gcs_private_key_id": "mock_gcs_private_key_id",
            "gcs_client_x509_cert_url": "mock_gcs_client_x509_cert_url",
            "gcs_project_id": "mock_gcs_project_id",
            "gcs_client_id": "mock_gcs_client_id",
            "gcs_client_email": "mock_gcs_client_email",
            "gcs_private_key": "mock_gcs_private_key",
        }

        params = {"token": self.token}

        params.update(settings | connector_settings)

        return params

    @patch(
        "tinybird.ingest.preview_connectors.gcs_sa_connector.GCSSAPreviewConnector.link_connector",
        return_value={"message": "Datasource is being created"},
    )
    @patch("tinybird.ingest.preview_connectors.gcs_sa_connector.GCSSAPreviewConnector.execute_now", return_value={})
    @tornado.testing.gen_test
    async def test_create_gcssa_preview_datasource_happy_case(self, _, __):
        connector_name = "test_create_gcssa_preview_datasource_happy_case"

        params = {
            "token": self.token,
            "bucket_uri": "bucket_uri.csv",
            "name": "gcssa_datasource_1",
            "service": DataConnectors.GCLOUD_STORAGE,
        }

        await self._create_preview_datasource_happy_case(
            service=DataConnectors.GCLOUD_STORAGE,
            connector_name=connector_name,
            params=params,
        )

    @patch(
        "tinybird.ingest.preview_connectors.gcs_sa_connector.GCSSAPreviewConnector.link_connector",
        return_value={"message": "Datasource is being created"},
    )
    @patch("tinybird.ingest.preview_connectors.gcs_sa_connector.GCSSAPreviewConnector.execute_now", return_value={})
    @tornado.testing.gen_test
    async def test_create_gcssa_preview_datasource_with_schema_happy_case(self, _, __):
        connector_name = "test_create_gcssa_preview_datasource_with_schema_happy_case"

        params = {
            "token": self.token,
            "bucket_uri": "bucket_uri.csv",
            "name": "gcssa_datasource_1",
            "service": DataConnectors.GCLOUD_STORAGE,
            "schema": "test String `json:$.test`",
        }

        await self._create_preview_datasource_with_schema_happy_case(
            service=DataConnectors.GCLOUD_STORAGE,
            connector_name=connector_name,
            params=params,
        )

    @tornado.testing.gen_test
    async def test_create_gcssa_preview_datasource_missing_parameter(self):
        params = {
            "token": self.token,
            "bucket_uri": "bucket_uri.csv",
            "name": "gcssa_datasource_1",
            "service": DataConnectors.GCLOUD_STORAGE,
            "schema": "test String `json:$.test`",
        }
        params_to_remove = [
            ("bucket_uri", 400, {"error": "Missing param: bucket_uri"}),
            ("name", 400, {"error": "Missing param: name"}),
        ]

        for n, row in enumerate(params_to_remove):
            connector_name = f"test_create_gcssa_preview_datasource_missing_parameter_{n}"
            param_to_remove, expected_error_code, expected_error_message = row
            await self._create_preview_datasource_missing_parameter(
                service=DataConnectors.GCLOUD_STORAGE,
                connector_name=connector_name,
                params=params,
                param_to_remove=param_to_remove,
                expected_error_code=expected_error_code,
                expected_error_message=expected_error_message,
            )

    @tornado.testing.gen_test
    async def test_create_gcssa_preview_datasource_file_extension_not_supported(self):
        connector_name = "test_create_gcssa_preview_datasource_file_extension_not_supported"
        params = {
            "token": self.token,
            "bucket_uri": "bucket_uri.whatever",
            "name": "gcssa_datasource_1",
            "service": DataConnectors.GCLOUD_STORAGE,
            "schema": "test String `json:$.test`",
        }

        await self._create_preview_datasource_file_extension_not_supported(
            service=DataConnectors.GCLOUD_STORAGE, connector_name=connector_name, params=params
        )

    @patch(
        "tinybird.ingest.preview_connectors.gcs_sa_connector.GCSSAPreviewConnector.link_connector",
        return_value={"message": "Datasource is being created"},
    )
    @patch("tinybird.ingest.preview_connectors.gcs_sa_connector.GCSSAPreviewConnector.execute_now", return_value={})
    @tornado.testing.gen_test
    async def test_create_gcssa_preview_datasource_extensions_supported(self, _, __):
        params = {
            "token": self.token,
            "service": DataConnectors.GCLOUD_STORAGE,
        }

        valid_extensions = [
            "csv",
            "csv.gz",
            "ndjson",
            "ndjson.gz",
            "jsonl",
            "jsonl.gz",
            "json",
            "json.gz",
            "parquet",
            "parquet.gz",
        ]

        with User.transaction(self.WORKSPACE_ID) as user:
            limit = len(valid_extensions) * 2
            user.set_rate_limit_config("api_datasources_create_append_replace", limit, 60, limit)
            user.set_rate_limit_config("api_connectors_create", limit, 60, limit)

        for extension in valid_extensions:
            connector_name = f"test_create_gcssa_preview_datasource_extension_{extension}"
            params_copy = params.copy()
            params_copy["bucket_uri"] = f"bucket_uri.{extension}"
            params_copy["name"] = f"gcssa_datasource_1_{extension}"
            await self._create_preview_datasource_happy_case(
                service=DataConnectors.GCLOUD_STORAGE, connector_name=connector_name, params=params_copy
            )

    @tornado.testing.gen_test
    async def test_create_gcssa_preview_datasource_invalid_from_time(self):
        connector_name = "test_create_gcssa_preview_datasource_invalid_from_time"
        params = {
            "token": self.token,
            "bucket_uri": "bucket_uri.csv",
            "name": "gcssa_datasource_1",
            "service": DataConnectors.GCLOUD_STORAGE,
            "schema": "test String `json:$.test`",
            "from_time": "fake",
        }

        await self._create_preview_datasource_invalid_from_time(
            service=DataConnectors.GCLOUD_STORAGE, connector_name=connector_name, params=params
        )

    @patch(
        "tinybird.ingest.preview_connectors.gcs_sa_connector.GCSSAPreviewConnector.link_connector",
        side_effect=ConnectorException("Not all required params"),
    )
    @tornado.testing.gen_test
    async def test_create_gcssa_preview_datasource_not_all_required_params_from_yepcode(self, _):
        connector_name = "test_create_gcssa_preview_datasource_not_all_required_params_from_yepcode"
        params = {
            "token": self.token,
            "bucket_uri": "bucket_uri.csv",
            "name": "gcssa_datasource_1",
            "service": DataConnectors.GCLOUD_STORAGE,
            "schema": "test String `json:$.test`",
        }

        await self._create_preview_datasource_not_all_required_params_from_yepcode(
            service=DataConnectors.GCLOUD_STORAGE,
            connector_name=connector_name,
            params=params,
        )

    @patch(
        "tinybird.ingest.preview_connectors.gcs_sa_connector.GCSSAPreviewConnector.link_connector",
        side_effect=ConnectorException("Wadus"),
    )
    @tornado.testing.gen_test
    async def test_create_gcssa_preview_datasource_unknown_error_from_yepcode(self, _):
        connector_name = "test_create_gcssa_preview_datasource_unknown_error_from_yepcode"
        params = {
            "token": self.token,
            "bucket_uri": "bucket_uri.csv",
            "name": "gcssa_datasource_1",
            "service": DataConnectors.GCLOUD_STORAGE,
            "schema": "test String `json:$.test`",
        }

        await self._create_preview_datasource_unknown_error_from_yepcode(
            service=DataConnectors.GCLOUD_STORAGE,
            connector_name=connector_name,
            params=params,
        )


class TestLimitDatasourceNumber(TestAPIDatasourceBase):
    @tornado.testing.gen_test
    async def test_datasource_limit(self):
        workspace_name = f"workspace_{uuid.uuid4().hex}"
        user_account = UserAccounts.get_by_id(self.USER_ID)
        workspace = await self.tb_api_proxy_async.register_workspace(workspace_name, user_account)
        workspace = User.get_by_id(workspace["id"])
        workspace_token = Users.get_token_for_scope(workspace, scopes.ADMIN_USER)
        self.workspaces_to_delete.append(workspace)

        workspace.set_user_limit("max_datasources", 1, "workspace")
        workspace.save()

        async def create_ds(ds_name):
            params = {
                "token": workspace_token,
                "name": ds_name,
                "schema": """timestamp DateTime,
                            value String""",
            }
            create_url = f"/v0/datasources?{urlencode(params)}"
            response = await self.fetch_async(create_url, method="POST", body="")
            return (response.code, json.loads(response.body))

        ds_name_1 = f"ds_limit_1_{uuid.uuid4().hex}"
        response_code, result = await create_ds(ds_name_1)
        self.assertEqual(response_code, 200)
        self.assertEqual(result["datasource"]["name"], ds_name_1)

        response_code, result = await create_ds(f"ds_limit_2_{uuid.uuid4().hex}")
        self.assertEqual(response_code, 400)
        self.assertEqual(result["error"], "The maximum number of datasources for this workspace is 1.")


class TestAPIDataSourceExchangeHandler(TestAPIDatasourceBase):
    def setUp(self):
        super().setUp()

        self.u = Users.get_by_id(self.WORKSPACE_ID)
        self.token = Users.get_token_for_scope(self.u, scopes.DATASOURCES_CREATE)

    @tornado.testing.gen_test
    async def test_exchange_not_ff_not_activated(self):
        with User.transaction(self.WORKSPACE_ID) as w:
            w.feature_flags[FeatureFlagWorkspaces.EXCHANGE_API.value] = False
        response = await self.fetch_async(
            "/v0/datasources/exchange", method="POST", body="", headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.code, 404)

        error_response = json.loads(response.body)
        self.assertIn("internal usage", error_response["error"])

    @tornado.testing.gen_test
    async def test_exchange_data_sources_successful(self):
        ds_a_name = "ds_a"
        ds_b_name = "ds_b"

        # Data Sources creation
        await asyncio.gather(self.create_datasource(ds_a_name, "a"), self.create_datasource(ds_b_name, "b"))

        params = {"datasource_a": ds_a_name, "datasource_b": ds_b_name}
        body = urlencode(params)

        response = await self.fetch_async(
            "/v0/datasources/exchange", method="POST", body=body, headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.code, 200)

        # Check the exchange was successful
        ds_a = Users.get_datasource(self.u, ds_a_name)
        ds_b = Users.get_datasource(self.u, ds_b_name)

        (_, schema_md_a), (_, schema_md_b) = await asyncio.gather(
            ds_a.table_metadata(self.u), ds_b.table_metadata(self.u)
        )

        self.assertIsNotNone(ds_a)
        self.assertIsNotNone(ds_b)

        # Check quarantine also exchanged
        ds_quarantine_a = exec_sql(self.u.database, f"SELECT * FROM {ds_a.id}_quarantine FORMAT JSON")
        ds_quarantine_b = exec_sql(self.u.database, f"SELECT * FROM {ds_b.id}_quarantine FORMAT JSON")

        self.assertIn({"name": "b", "type": "Nullable(String)"}, ds_quarantine_a["meta"])
        self.assertIn({"name": "a", "type": "Nullable(String)"}, ds_quarantine_b["meta"])

        # Assert redis cached properties
        self.assertEqual(ds_a.engine["sorting_key"], "b")
        self.assertEqual(ds_b.engine["sorting_key"], "a")

        self.assertEqual(ds_a.json_deserialization[0]["name"], "b")
        self.assertEqual(ds_b.json_deserialization[0]["name"], "a")

        # Assert CH info
        self.assertEqual(schema_md_a[0]["name"], "b")
        self.assertEqual(schema_md_b[0]["name"], "a")

        # Assert datasources_ops_log
        expect_ops_log = {
            "event_type": "exchange",
            "datasource_id": ds_a.id,
            "datasource_name": ds_a.name,
            "result": "ok",
            "options": {"datasource_a": ds_a.name, "datasource_b": ds_b.name},
        }
        self.assert_datasources_ops_log(self.u, count=1, **expect_ops_log)

    @tornado.testing.gen_test
    async def test_exchange_non_existing_datasource_A_returns_error(self):
        ds_a_name = "non_existing_ds"
        ds_b_name = "ds_b"

        params = {"datasource_a": ds_a_name, "datasource_b": ds_b_name}
        body = urlencode(params)

        response = await self.fetch_async(
            "/v0/datasources/exchange", method="POST", body=body, headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.code, 404)

        error_response = json.loads(response.body)
        self.assertEqual(error_response["error"], f'Data Source "{ds_a_name}" does not exist')

    @tornado.testing.gen_test
    async def test_exchange_non_existing_datasource_B_returns_error(self):
        ds_a_name = "ds"
        ds_b_name = "non_existing_ds"

        await self.create_datasource(ds_a_name)

        params = {"datasource_a": ds_a_name, "datasource_b": ds_b_name}
        body = urlencode(params)

        response = await self.fetch_async(
            "/v0/datasources/exchange", method="POST", body=body, headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.code, 404)

        error_response = json.loads(response.body)
        self.assertEqual(error_response["error"], f'Data Source "{ds_b_name}" does not exist')

    @tornado.testing.gen_test
    async def test_missing_datasource_A_parameter(self):
        params = {"datasource_b": "ds_b"}
        body = urlencode(params)

        response = await self.fetch_async(
            "/v0/datasources/exchange", method="POST", body=body, headers={"Authorization": f"Bearer {self.token}"}
        )

        self.assertEqual(response.code, 400)

        error_response = json.loads(response.body)
        self.assertEqual(error_response["error"], 'The parameter "datasource_a" is required in this endpoint')

    @tornado.testing.gen_test
    async def test_missing_datasource_B_parameter(self):
        params = {"datasource_a": "ds_a"}
        body = urlencode(params)

        response = await self.fetch_async(
            "/v0/datasources/exchange", method="POST", body=body, headers={"Authorization": f"Bearer {self.token}"}
        )

        self.assertEqual(response.code, 400)

        error_response = json.loads(response.body)
        self.assertEqual(error_response["error"], 'The parameter "datasource_b" is required in this endpoint')

    @tornado.testing.gen_test
    async def test_exchange_data_sources_revert_when_alter_operation_fails(self):
        ds_a_name = "ds_a"
        ds_b_name = "ds_b"

        # Data Sources creation
        await asyncio.gather(self.create_datasource(ds_a_name, "a"), self.create_datasource(ds_b_name, "b"))

        params = {"datasource_a": ds_a_name, "datasource_b": ds_b_name}
        body = urlencode(params)

        # Mock the alter_datasource operation to fail
        with mock.patch(
            "tinybird.user.Users.alter_datasource_json_deserialization", side_effect=[Exception("Simulated Failure")]
        ):
            response = await self.fetch_async(
                "/v0/datasources/exchange", method="POST", body=body, headers={"Authorization": f"Bearer {self.token}"}
            )
            self.assertNotEqual(response.code, 200)

        ds_a = Users.get_datasource(self.u, ds_a_name)
        ds_b = Users.get_datasource(self.u, ds_b_name)

        (_, schema_md_a), (_, schema_md_b) = await asyncio.gather(
            ds_a.table_metadata(self.u), ds_b.table_metadata(self.u)
        )

        # Assert everything have been correctly reverted
        self.assertEqual(schema_md_a[0]["name"], "a")
        self.assertEqual(schema_md_b[0]["name"], "b")

        self.assertEqual(ds_a.engine["sorting_key"], "a")
        self.assertEqual(ds_b.engine["sorting_key"], "b")

        self.assertEqual(ds_a.json_deserialization[0]["name"], "a")
        self.assertEqual(ds_b.json_deserialization[0]["name"], "b")

        expect_ops_log = {
            "event_type": "exchange",
            "datasource_id": ds_a.id,
            "datasource_name": ds_a.name,
            "result": "error",
            "error": "Simulated Failure",
            "options": {"datasource_a": ds_a.name, "datasource_b": ds_b.name},
            "cpu_time": 0,
            "resource_tags": [],
        }
        self.assert_datasources_ops_log(self.u, count=1, **expect_ops_log)

    @tornado.testing.gen_test
    async def test_exchange_revert_logs_exception_and_continue_reverting_when_an_op_fails(self):
        ds_a_name = "ds_a"
        ds_b_name = "ds_b"

        # Data Sources creation
        await asyncio.gather(self.create_datasource(ds_a_name, "a"), self.create_datasource(ds_b_name, "b"))

        params = {"datasource_a": ds_a_name, "datasource_b": ds_b_name}
        body = urlencode(params)

        # Mock the alter_datasource operation to fail
        with (
            mock.patch(
                "tinybird.user.Users.alter_datasource_json_deserialization",
                side_effect=[None, Exception("Alter Failure"), Exception("Revert Failure")],
            ),
            patch("logging.exception") as mock_logging,
        ):
            response = await self.fetch_async(
                "/v0/datasources/exchange", method="POST", body=body, headers={"Authorization": f"Bearer {self.token}"}
            )
            self.assertNotEqual(response.code, 200)
            self.assertIn("Failed to revert", str(mock_logging.call_args))

        ds_a = Users.get_datasource(self.u, ds_a_name)
        ds_b = Users.get_datasource(self.u, ds_b_name)

        (_, schema_md_a), (_, schema_md_b) = await asyncio.gather(
            ds_a.table_metadata(self.u), ds_b.table_metadata(self.u)
        )

        # Assert almost everything have been correctly reverted dispite the exception reverting deserialization
        self.assertEqual(schema_md_a[0]["name"], "a")
        self.assertEqual(schema_md_b[0]["name"], "b")

        self.assertEqual(ds_a.engine["sorting_key"], "a")
        self.assertEqual(ds_b.engine["sorting_key"], "b")

    async def create_datasource(self, ds_name, column_name: str = "x"):
        params = {
            "token": self.token,
            "name": ds_name,
            "format": "ndjson",
            "schema": f"""
                    {column_name} Int32 `json:$.{column_name}`
                """,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        return json.loads(response.body)


class TestAPIDataSourceResourceTags(TestAPIDatasourceBase):
    def setUp(self):
        super().setUp()
        u = Users.get_by_id(self.WORKSPACE_ID)
        self.user_account = UserAccounts.get_by_id(self.USER_ID)
        self.u = u
        self.token = Users.get_token_for_scope(u, scopes.ADMIN)

    async def create_datasource(self, ds_name, column_name: str = "x"):
        params = {
            "token": self.token,
            "name": ds_name,
            "format": "ndjson",
            "schema": f"""
                    {column_name} Int32 `json:$.{column_name}`
                """,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        return json.loads(response.body)

    async def append_data(self, ds_name, data):
        params = {"mode": "append", "name": ds_name, "format": "ndjson", "token": self.token}
        await self.fetch_async(
            f"/v0/datasources?{urlencode(params)}",
            method="POST",
            headers={"Content-type": "application/json"},
            body=json.dumps(data),
        )

    async def truncate_datasource(self, ds_name):
        params = {"token": self.token}
        await self.fetch_async(f"/v0/datasources/{ds_name}/truncate?{urlencode(params)}", method="POST", body="")

    @tornado.testing.gen_test
    async def test_tags_create_append_truncate_ops_logs(self):
        ds_name = "test_populate_resource_tags_from_datasource"
        tag_name = "tag_1"
        await self.create_tag(token=self.token, tag_name=tag_name, datasources=[ds_name], pipes=[])
        await self.create_datasource(ds_name)
        await self.append_data(ds_name, {"x": 1})
        await self.truncate_datasource(ds_name)
        self.expect_ops_log(
            [
                {
                    "event_type": "create",
                    "datasource_name": ds_name,
                    "resource_tags": [tag_name],
                },
                {
                    "event_type": "append",
                    "datasource_name": ds_name,
                    "resource_tags": [tag_name],
                },
                {
                    "event_type": "truncate",
                    "datasource_name": ds_name,
                    "resource_tags": [tag_name],
                },
            ]
        )

    @tornado.testing.gen_test
    async def test_tags_populate_ops_log(self):
        rand = str(uuid.uuid4())[:8]
        ds1 = f"DS1_{rand}"
        ds2 = f"DS2_{rand}"
        mv1 = f"MV1to2_{rand}"
        tag_name_ds_1 = "tag_1"
        tag_name_ds_2 = "tag_2"
        await self.create_tag(token=self.token, tag_name=tag_name_ds_1, datasources=[ds1], pipes=[])
        await self.create_tag(token=self.token, tag_name=tag_name_ds_2, datasources=[ds2], pipes=[])
        await self.create_datasource_async(
            self.token,
            ds1,
            """
                id Int32,
                timestamp Date,
                category String
            """,
            {
                "engine": "MergeTree",
                "engine_partition_key": "toYYYYMM(timestamp)",
                "engine_sorting_key": "id, timestamp",
            },
        )

        response = await self.fetch_async(
            f"/v0/pipes?token={self.token}",
            method="POST",
            body=json.dumps(
                {
                    "name": mv1,
                    "nodes": [
                        {
                            "name": "mv",
                            "type": "materialized",
                            "sql": f"SELECT category AS c, id AS fake_id FROM {ds1}",
                            "datasource": ds2,
                            "populate": "true",
                        }
                    ],
                }
            ),
            headers={"Content-type": "application/json"},
        )
        self.assertEqual(response.code, 200, response.body)
        content = json.loads(response.body)
        job = await self.get_finalised_job_async(content["job"]["job_id"])
        self.assertEqual(job["status"], "done")

        ds2_datasource = Users.get_datasource(self.u, ds2)

        self.expect_ops_log(
            {
                "event_type": "create",
                "datasource_name": ds2,
                "resource_tags": [tag_name_ds_2],
            }
        )

        await self.append_data_to_datasource(
            self.token,
            ds1,
            CsvIO(
                "1,2020-01-01,A",
                "1,2020-01-01,A",
                "1,2020-01-01,B",
                "8,2020-01-01,B",
                "8,2020-01-02,B",
                "9,2020-03-02,B",
                "1,2020-01-02,A",
                "5,2020-01-02,A",
                "1,2020-01-02,B",
            ),
        )

        self.expect_ops_log(
            {
                "event_type": "append",
                "datasource_name": ds2,
                "resource_tags": [tag_name_ds_2],
            }
        )

        self.expect_ops_log(
            {
                "event_type": "populateview-queued",
                "datasource_name": ds2,
                "resource_tags": [tag_name_ds_2],
            }
        )

        self.expect_ops_log(
            {
                "event_type": "populateview",
                "datasource_name": ds2,
                "resource_tags": [tag_name_ds_2],
            }
        )

        await self.replace_data_to_datasource(
            self.token,
            ds1,
            CsvIO("1,2020-01-01,A", "1,2020-01-01,B", "1,2020-01-02,A", "1,2020-01-02,B"),
            expect_logs=False,
        )

        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": ds1,
                "resource_tags": [tag_name_ds_1],
            }
        )

        self.expect_ops_log(
            {
                "event_type": "replace",
                "datasource_name": ds2,
                "pipe_id": ds2_datasource.tags.get("created_by_pipe"),
                "pipe_name": mv1,
                "resource_tags": [tag_name_ds_2],
            }
        )
