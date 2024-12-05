"""
this file contains tests with CSV files that raised problems when importing
"""

import json
import uuid
from urllib.parse import urlencode

import tornado

from tinybird.token_scope import scopes
from tinybird.user import Users

from ..utils import HTTP_ADDRESS, exec_sql, fixture_file
from .base_test import BaseTest


class TestCSVSamples(BaseTest):
    @tornado.testing.gen_test
    async def test_import_delimiter_space(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        csv_url = f"{HTTP_ADDRESS}/nginx_log.csv"
        import_url = f"/v0/datasources?token={token}&name=nginx_log&url={csv_url}"

        response = await self.fetch_async(import_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        job = await self.get_finalised_job_async(json.loads(response.body)["id"], debug="blocks")
        self.assertEqual(job.status, "done")
        parser = job["blocks"][0]["process_return"][0]["parser"]
        self.assertEqual(parser, "clickhouse")

    @tornado.testing.gen_test
    async def test_import_url_yt(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        csv_url = f"{HTTP_ADDRESS}/serie_historica_acumulados.csv"
        import_url = f"/v0/datasources?token={token}&name=serie_historica_acumulados&url={csv_url}"

        response = await self.fetch_async(import_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        job = await self.get_finalised_job_async(json.loads(response.body)["id"], debug="blocks")
        self.assertEqual(job.status, "done")
        blocks = job["blocks"]
        self.assertEqual(len(blocks), 1)
        datasource_id = job["datasource"]["id"]
        a = exec_sql(u["database"], f"SELECT count() c FROM {datasource_id} FORMAT JSON")
        row = a["data"][0]
        self.assertEqual(int(row["c"]), 875)
        exec_sql(u["database"], "drop table IF EXISTS `%s`" % datasource_id)

    @tornado.testing.gen_test
    async def test_wrong_quoted_string(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {
            "token": token,
            "mode": "create",
            "schema": "a Int8,b String,c Int32",
            "name": "test_wrong_quoted_string",
        }
        import_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(import_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)
        params = {"token": token, "mode": "append", "name": "test_wrong_quoted_string"}
        with fixture_file("wrong_quote.csv") as fd:
            response = await self.fetch_full_body_upload_async(f"/v0/datasources?{urlencode(params)}", fd)
        self.assertEqual(response.code, 200, response.body)
        d = json.loads(response.body)

        a = exec_sql(u["database"], f"SELECT count() c FROM {d['datasource']['id']}_quarantine FORMAT JSON")
        self.assertEqual(a["data"][0]["c"], "4")
        a = exec_sql(u["database"], f"SELECT count() c FROM {d['datasource']['id']} FORMAT JSON")
        self.assertEqual(a["data"][0]["c"], "1")

    @tornado.testing.gen_test
    async def test_column_with_table_in_row_name(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        csv_url = f"{HTTP_ADDRESS}/yt_1000_table_in_column.csv"
        import_url = f"/v0/datasources?token={token}&name=yt_1000&url={csv_url}"

        response = await self.fetch_async(import_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        job = await self.get_finalised_job_async(json.loads(response.body)["id"])
        self.assertEqual(job.status, "done")

    @tornado.testing.gen_test
    async def test_import_csv_all_types_happy_case(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        ds_name = f"test_import_csv_all_types_happy_case_{uuid.uuid4().hex}"

        schema = ""
        with fixture_file("all_types_schema.txt") as fd:
            for line in fd.readlines():
                schema += line

        params = {
            "token": token,
            "name": ds_name,
            "schema": schema,
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200, response.body)

        params = {"token": token, "mode": "append", "name": ds_name}
        with fixture_file("all_types.csv") as fd:
            response = await self.fetch_full_body_upload_async(f"/v0/datasources?{urlencode(params)}", fd)

        self.assertEqual(response.code, 200, response.body)
        d = json.loads(response.body)

        self.assertEqual(d["quarantine_rows"], 0)
        self.assertEqual(d["invalid_lines"], 0)
