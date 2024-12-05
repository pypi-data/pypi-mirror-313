import json
from urllib.parse import urlencode

import tornado

from tinybird.token_scope import scopes
from tinybird.user import Users

from ..utils import HTTP_ADDRESS, exec_sql
from .base_test import BaseTest


class TestAPIDatasourceHooksDrive(BaseTest):
    async def _query(self, q):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        params = {"token": token, "q": q}
        response = await self.fetch_async(f"/v0/sql?{urlencode(params)}")
        self.assertEqual(response.code, 200)
        return json.loads(response.body)

    async def _make_endpoint(self, pipe_name, pipe_node):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        response = await self.fetch_async(
            f"/v0/pipes/{pipe_name}/nodes/{pipe_node['id']}/endpoint?token={token}", method="POST", body=b""
        )
        self.assertEqual(response.code, 200)

    async def create_pipe_with_view(self, pipe_name, view_sql, datasource=None, staging=False):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)
        node_params = {"name": f"{pipe_name}_view", "type": "materialized", "sql": view_sql}

        if datasource:
            node_params["datasource"] = datasource
        if staging:
            node_params["with_staging"] = "true"

        params = {"token": token}

        pipe_def = {"name": pipe_name, "nodes": [node_params]}
        pipe_def = json.dumps(pipe_def)

        response = await self.fetch_async(
            f"/v0/pipes?{urlencode(params)}", method="POST", body=pipe_def, headers={"Content-type": "application/json"}
        )
        self.assertEqual(response.code, 200)
        pipe_node = json.loads(response.body)["nodes"][0]
        return pipe_node

    @tornado.testing.gen_test
    async def test_drive_end_to_end(self):
        u = Users.get_by_id(self.WORKSPACE_ID)
        token = Users.get_token_for_scope(u, scopes.ADMIN)

        # 1. Create the landing datasource
        landing_name = "sales_rt_landing"
        params = {
            "token": token,
            "name": landing_name,
            "schema": """
                cod_brand Int8,
                local_timeplaced DateTime,
                cod_order_wcs Int64,
                client_id Int64,
                cod_status Nullable(String),
                replacement Int8,
                cod_order_type Int8,
                cod_shipping_method Int16,
                purchase_location Int16,
                device_location Int16,
                warehouse_location Int32,
                shipping_location Int32,
                return_location Nullable(Int32),
                cod_device LowCardinality(String),
                cod_category Int64,
                parent_catentry Int64,
                catentry Int64,
                sku String,
                cod_transaction Int16,
                units Int16,
                amount Float32,
                tax Float32
            """,
            "engine": "Null",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        # 2. Create the target datasource
        sales_name = "sales_rt"
        params = {
            "token": token,
            "name": sales_name,
            "schema": """
                pk UInt64,
                sku_product_type UInt16,
                sku_product_model UInt16,
                sku_product_quality UInt16,
                sku_product_color UInt16,
                sku_product_size UInt8,
                sku_product_campaign String,
                insert_date Date,
                cod_brand Int8,
                local_timeplaced DateTime,
                cod_order_wcs Int64,
                client_id Int64,
                cod_status Nullable(String),
                replacement Int8,
                cod_order_type Int8,
                cod_shipping_method Int16,
                purchase_location Int16,
                device_location Int16,
                warehouse_location Int32,
                shipping_location Int32,
                return_location Nullable(Int32),
                cod_device LowCardinality(String),
                cod_category Int64,
                parent_catentry Int64,
                catentry Int64,
                sku String,
                cod_transaction Int16,
                units Int16,
                amount Float32,
                tax Float32
            """,
            "engine": "ReplacingMergeTree",
            "engine_ver": "insert_date",
            "engine_sorting_key": "purchase_location, pk",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)
        sales_id = json.loads(response.body)["datasource"]["id"]

        # 3. Create a view to connect the 'sales_rt_landing' datasource with the 'sales_rt' datasource
        pipe_sales_rt_name = "sales_rt_pipe"
        replacing_view_sql = f"""
        SELECT
            cityHash64(cod_brand, cod_order_wcs, cod_transaction, replacement, catentry, parent_catentry, cod_category, sku, cod_order_type) as pk,
            toUInt16(substring(sku, 1, 1)) as sku_product_type,
            toUInt16(substring(sku, 2, 4)) as sku_product_model,
            toUInt16(substring(sku, 6, 3)) as sku_product_quality,
            toUInt16(substring(sku, 9, 3)) as sku_product_color,
            toUInt8(substring(sku, 12, 2)) as sku_product_size,
            substring(sku, 15, 5) as sku_product_campaign,
            toDate(now()) as insert_date,
            cod_brand,
            local_timeplaced,
            cod_order_wcs,
            client_id,
            cod_status,
            replacement,
            cod_order_type,
            cod_shipping_method,
            purchase_location,
            device_location,
            warehouse_location,
            shipping_location,
            return_location,
            cod_device,
            cod_category,
            parent_catentry,
            catentry,
            sku,
            cod_transaction,
            units,
            amount,
            tax
        FROM
            {landing_name}
        """
        sales_rt_pipe_node = await self.create_pipe_with_view(
            pipe_sales_rt_name, replacing_view_sql, datasource=sales_name, staging=True
        )

        # 4. Create the product rank datasource
        product_rank_name = "sales_product_rank_rt"
        params = {
            "token": token,
            "name": product_rank_name,
            "schema": """
                sku_rank_lc LowCardinality(String),
                purchase_location UInt16,
                date Date,
                amount_net Float32,
                amount_gross Float32,
                units_count UInt32
            """,
            "engine": "MergeTree",
            "engine_partition_key": "toYYYYMM(date)",
            "engine_sorting_key": "purchase_location, sku_rank_lc, date",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        # 6. Create view 'sales_product_rank_rt' that depends on view 'sales_rt'
        pipe_product_rank_name = "sales_product_rank_rt_pipe"
        view_sql = """
        SELECT
            CAST(
            (substring(sku, 1, 1) || '_' || substring(sku, 2, 4) || '_' || substring(sku, 9, 3) || '_' || substring(sku, 6, 3) || '-' || substring(sku, 15, 5))
            as LowCardinality(String)) as sku_rank_lc,
            toUInt16(purchase_location) purchase_location,
            toDate(local_timeplaced) date,
            toFloat32(sum(amount)) amount_net,
            toFloat32(sumIf(amount, cod_transaction IN (72, 772))) amount_gross,
            toUInt32(sum(units)) units_count
        FROM
            sales_rt
        GROUP BY
            date, purchase_location, sku_rank_lc
        """
        await self.create_pipe_with_view(pipe_product_rank_name, view_sql, datasource=product_rank_name)

        # Create another rank datasource
        product_rank_orders_name = "sales_product_rank_orders_rt"
        params = {
            "token": token,
            "name": product_rank_orders_name,
            "schema": """
                sku_rank_lc LowCardinality(String),
                purchase_location UInt16,
                date Date,
                line_orders UInt32
            """,
            "engine": "MergeTree",
            "engine_partition_key": "toYYYYMM(date)",
            "engine_sorting_key": "purchase_location, sku_rank_lc, date",
        }
        create_url = f"/v0/datasources?{urlencode(params)}"
        response = await self.fetch_async(create_url, method="POST", body="")
        self.assertEqual(response.code, 200)

        # Create another view that depends on view 'sales_rt'
        pipe_product_rank_orders_name = "sales_product_rank_orders_rt_pipe"
        view_sql = """
        SELECT
            CAST(
            (substring(sku, 1, 1) || '_' || substring(sku, 2, 4) || '_' || substring(sku, 9, 3) || '_' || substring(sku, 6, 3) || '-' || substring(sku, 15, 5))
            as LowCardinality(String)) as sku_rank_lc,
            toUInt16(purchase_location) purchase_location,
            toDate(local_timeplaced) date,
            toUInt32(count()) line_orders
        FROM
            sales_rt
        GROUP BY
            date, purchase_location, sku_rank_lc
        """
        await self.create_pipe_with_view(pipe_product_rank_orders_name, view_sql, datasource=product_rank_orders_name)

        # 5. Deduplication mechanism is ready
        async def append_data(url):
            params = {
                "token": token,
                "mode": "append",
                "name": landing_name,
                "url": url,
            }
            append_url = self.get_url(f"/v0/datasources?{urlencode(params)}")
            response = await self.fetch_async(append_url, method="POST", body="")
            self.assertEqual(response.code, 200)
            job = await self.get_finalised_job_async(
                json.loads(response.body)["id"], max_retries=600, elapsed_time_interval=0.5
            )
            self.assertEqual(job.status, "done", job.get("error", None))

        sales_query = f"""
        SELECT
            count() count,
            sum(units) sum_units,
            sum(amount) sum_amount
        FROM
            {sales_name}
        FORMAT JSON
        """

        sales_staging_query = f"""
        SELECT
            count() count,
            sum(units) sum_units,
            sum(amount) sum_amount
        FROM
            {sales_id}_staging
        FORMAT JSON
        """

        products_query = f"""
        SELECT
            *
        FROM
            {product_rank_name}
        ORDER BY date asc
        FORMAT JSON
        """

        await append_data(f"{HTTP_ADDRESS}/sales_0.csv")

        result = (await self._query(sales_query))["data"][0]
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["sum_units"], 2)
        self.assertEqual(result["sum_amount"], 30)

        # We want to keep staging table consistent
        extra_params = {"output_format_json_quote_64bit_integers": 0}
        result = exec_sql(u["database"], sales_staging_query, extra_params)["data"][0]
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["sum_units"], 2)
        self.assertEqual(result["sum_amount"], 30)

        result = (await self._query(products_query))["data"]
        self.assertEqual(len(result), 2)
        p = result[0]
        self.assertEqual(p["amount_net"], 10)
        self.assertEqual(p["units_count"], 1)
        p = result[1]
        self.assertEqual(p["amount_net"], 20)
        self.assertEqual(p["units_count"], 1)

        await append_data(f"{HTTP_ADDRESS}/sales_1.csv")

        result = (await self._query(sales_query))["data"][0]
        self.assertEqual(result["count"], 3)
        self.assertEqual(result["sum_units"], 4)
        self.assertEqual(result["sum_amount"], 45)

        result = (await self._query(products_query))["data"]
        self.assertEqual(len(result), 3)
        p = result[0]
        self.assertEqual(p["amount_net"], 10)
        self.assertEqual(p["units_count"], 1)
        p = result[1]
        self.assertEqual(p["amount_net"], 25)
        self.assertEqual(p["units_count"], 1)
        p = result[2]
        self.assertEqual(p["amount_net"], 10)
        self.assertEqual(p["units_count"], 2)

        await append_data(f"{HTTP_ADDRESS}/sales_2.csv")

        result = (await self._query(sales_query))["data"][0]
        self.assertEqual(result["count"], 4)
        self.assertEqual(result["sum_units"], 8)
        self.assertEqual(result["sum_amount"], 65)

        # We want to keep staging table consistent
        extra_params = {"output_format_json_quote_64bit_integers": 0}
        result = exec_sql(u["database"], sales_staging_query, extra_params)["data"][0]
        self.assertEqual(result["count"], 4)
        self.assertEqual(result["sum_units"], 8)
        self.assertEqual(result["sum_amount"], 65)

        result = (await self._query(products_query))["data"]
        self.assertEqual(len(result), 3)
        p = result[0]
        self.assertEqual(p["amount_net"], 10)
        self.assertEqual(p["units_count"], 1)
        p = result[1]
        self.assertEqual(p["amount_net"], 25)
        self.assertEqual(p["units_count"], 1)
        p = result[2]
        self.assertEqual(p["amount_net"], 30)
        self.assertEqual(p["units_count"], 6)

        await append_data(f"{HTTP_ADDRESS}/sales_3.csv")

        async def check_last_valid_state():
            result = (await self._query(sales_query))["data"][0]
            self.assertEqual(result["count"], 4)
            self.assertEqual(result["sum_units"], 8)
            self.assertEqual(result["sum_amount"], 65)

            result = (await self._query(products_query))["data"]
            self.assertEqual(len(result), 3)
            p = result[0]
            self.assertEqual(p["amount_net"], 10)
            self.assertEqual(p["units_count"], 1)
            p = result[1]
            self.assertEqual(p["amount_net"], 25)
            self.assertEqual(p["units_count"], 1)
            p = result[2]
            self.assertEqual(p["amount_net"], 30)
            self.assertEqual(p["units_count"], 6)

        await check_last_valid_state()

        ds_sales = Users.get_datasource(u, sales_name)

        # We can't delete landing as it is used in a materialized node
        params = {"token": token}
        delete_url = self.get_url(f"/v0/datasources/{landing_name}?{urlencode(params)}")
        response = await self.fetch_async(delete_url, method="DELETE", body=None)
        self.assertEqual(response.code, 409, response.body)
        await check_last_valid_state()  # no harm was done yet

        # Validate number of staging tables
        r = exec_sql(
            u["database"],
            f"""
            SELECT name
            FROM system.tables
            WHERE database = '{u['database']}' and name like '{ds_sales.id}%'
            FORMAT JSON
        """,
        )
        actual_tables = set([t["name"] for t in r["data"]])
        expected_tables = set([f"{ds_sales.id}{x}" for x in ("", "_quarantine", "_staging")])
        self.assertEqual(actual_tables, expected_tables)
        # Validate pipe sales_rt node exists
        r = exec_sql(
            u["database"],
            f"""
            SELECT name
            FROM system.tables
            WHERE database = '{u['database']}' and name = '{sales_rt_pipe_node['id']}'
            FORMAT JSON
        """,
        )
        actual_tables = set([t["name"] for t in r["data"]])
        expected_tables = set([sales_rt_pipe_node["id"]])
        self.assertEqual(actual_tables, expected_tables)

        # Delete the pipe to delete the staging table and the view
        params = {"token": token}
        delete_url = self.get_url(f"/v0/pipes/{pipe_sales_rt_name}?{urlencode(params)}")
        response = await self.fetch_async(delete_url, method="DELETE", body=None)
        self.assertEqual(response.code, 204)

        r = exec_sql(
            u["database"],
            f"""
            SELECT name
            FROM system.tables
            WHERE database = '{u['database']}' and name like '{ds_sales.id}%'
            FORMAT JSON
        """,
        )
        actual_tables = set([t["name"] for t in r["data"]])
        expected_tables = set([f"{ds_sales.id}{x}" for x in ("", "_quarantine", "_staging")])
        self.assertEqual(actual_tables, expected_tables)

        r = exec_sql(
            u["database"],
            f"""
            SELECT count() c
            FROM system.tables
            WHERE database = '{u['database']}' and name = '{sales_rt_pipe_node['id']}'
            FORMAT JSON
        """,
        )
        self.assertEqual(int(r["data"][0]["c"]), 0)

        # With the materialized node's pipe gone, delete landing
        params = {"token": token}
        delete_url = self.get_url(f"/v0/datasources/{landing_name}?{urlencode(params)}")
        response = await self.fetch_async(delete_url, method="DELETE", body=None)
        self.assertEqual(response.code, 204)
        await check_last_valid_state()  # no harm was done yet

        # Can not delete the target data source because is in use in a materialized noe
        params = {"token": token}
        delete_url = self.get_url(f"/v0/datasources/{sales_name}?{urlencode(params)}")
        response = await self.fetch_async(delete_url, method="DELETE", body=None)
        self.assertEqual(response.code, 409, response.body)

        # Delete the pipes to allow deleting the target data source
        params = {"token": token}
        delete_url = self.get_url(f"/v0/pipes/{pipe_product_rank_name}?{urlencode(params)}")
        response = await self.fetch_async(delete_url, method="DELETE", body=None)
        self.assertEqual(response.code, 204)
        delete_url = self.get_url(f"/v0/pipes/{pipe_product_rank_orders_name}?{urlencode(params)}")
        response = await self.fetch_async(delete_url, method="DELETE", body=None)
        self.assertEqual(response.code, 204)

        # Delete the target data source
        params = {"token": token}
        delete_url = self.get_url(f"/v0/datasources/{sales_name}?{urlencode(params)}")
        response = await self.fetch_async(delete_url, method="DELETE", body=None)
        self.assertEqual(response.code, 204, response.body)

        # All associated tables are gone now
        r = exec_sql(
            u["database"],
            f"""
            SELECT count() as c
            FROM system.tables
            WHERE database = '{u['database']}' and name like '{ds_sales.id}%'
            FORMAT JSON
        """,
        )
        self.assertEqual(int(r["data"][0]["c"]), 0)
