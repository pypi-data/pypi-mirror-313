import asyncio
import json
import logging
import math
import uuid
from collections import defaultdict, namedtuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple, cast
from zoneinfo import ZoneInfo

import stripe
from stripe import Price, Product, Subscription, SubscriptionItem

from tinybird.data_sinks.limits import SinkLimits
from tinybird.datasource import Datasource
from tinybird.pipe import PipeTypes

from .ch import HTTPClient
from .ch_utils.exceptions import CHException
from .constants import BillingPlans, BillingTypes
from .internal import get_by_pipe_endpoint
from .model import retry_transaction_in_case_of_concurrent_edition_error_async
from .syncasync import async_to_sync
from .user import User, Users, public


class PlanConfigConcepts(Enum):
    DEV_MAX_API_REQUESTS_PER_DAY = "dev_max_api_requests_per_day"
    DEV_MAX_GB_STORAGE_USED = "dev_max_gb_storage_used"


DEFAULT_PLAN_CONFIG = {
    PlanConfigConcepts.DEV_MAX_API_REQUESTS_PER_DAY: 1000,
    PlanConfigConcepts.DEV_MAX_GB_STORAGE_USED: 10,
}

PRICES_LIMIT = 100

WorkspaceMetricsInfo = namedtuple(
    "WorkspaceMetricsInfo", ("workspace_id", "workspace_name", "processed", "storage", "is_billable")
)

WorkspaceStorageByDayInfo = namedtuple(
    "WorkspaceStorageByDayInfo", ("workspace_id", "day", "bytes", "bytes_quarantine")
)

WorkspaceProcessedByDayInfo = namedtuple(
    "WorkspaceProcessedByDayInfo", ("workspace_id", "day", "read_bytes", "written_bytes")
)


class PlansException(Exception):
    pass


class PlanName(Enum):
    DEV = "Build"
    PRO = "Pro"
    ENTERPRISE = "Enterprise"
    BRANCH_ENTERPRISE = "Enterprise"


class PackageType(Enum):
    DEV = "dev"
    FREE = "free"
    COMMITTED = "committed"
    EXTRA = "extra"


class PlansStatisticsErrors:
    STATS_QUERY = "Can't get statistics right now, try again in a few minutes or contact us at support@tinybird.co"


class StripeSettings:
    DASHBOARD_SUBSCRIPTIONS_TEST_URL = "https://dashboard.stripe.com/test/subscriptions"
    DASHBOARD_SUBSCRIPTIONS_URL = "https://dashboard.stripe.com/subscriptions"
    DASHBOARD_CUSTOMER_TEST_URL = "https://dashboard.stripe.com/test/customers"
    DASHBOARD_CUSTOMER_URL = "https://dashboard.stripe.com/customers"
    LATEST_INVOICE_TEST_URL = "https://dashboard.stripe.com/test/invoices"
    LATEST_INVOICE_URL = "https://dashboard.stripe.com/invoices"
    PRODUCT_TEST_URL = "https://dashboard.stripe.com/test/products"
    PRODUCT_URL = "https://dashboard.stripe.com/products"


def configure_stripe(app_config):
    stripe_api_key = app_config.get("stripe", {}).get("api_key", None)
    if stripe_api_key:
        stripe.api_key = stripe_api_key
    stripe.max_network_retries = 1
    stripe.client = stripe.http_client.RequestsClient()

    stripe_default_products = app_config.get("stripe", {}).get("default_products", None)
    if stripe_default_products:
        PlansService.PRO = stripe_default_products.get("pro", None)


class PlansService:
    """
    >>> from tinybird.user import UserAccount
    >>> u = UserAccount.register('test_change_workspace_plan@example.com', 'pass')
    >>> w = User.register('test_change_workspace_plan', admin=u.id)
    >>> w.plan
    'dev'
    >>> import asyncio
    >>> w = asyncio.run(Users.change_workspace_plan(w, BillingPlans.PRO))
    >>> w.plan
    'pro'
    >>> PlansService._get_value_for_config(w, PlanConfigConcepts.DEV_MAX_API_REQUESTS_PER_DAY)
    1000
    >>> asyncio.run(PlansService.override_default_config(w, PlanConfigConcepts.DEV_MAX_API_REQUESTS_PER_DAY, 10000))
    >>> w = User.get_by_id(w.id)
    >>> PlansService._get_value_for_config(w, PlanConfigConcepts.DEV_MAX_API_REQUESTS_PER_DAY)
    10000
    >>> asyncio.run(PlansService.override_default_config(w, PlanConfigConcepts.DEV_MAX_API_REQUESTS_PER_DAY, None))
    >>> w = User.get_by_id(w.id)
    >>> PlansService._get_value_for_config(w, PlanConfigConcepts.DEV_MAX_API_REQUESTS_PER_DAY)
    1000
    """

    PRO = None

    @classmethod
    def get_default_prices_by_plan(cls, plan: str, workspace: Optional[User] = None) -> List[Dict[str, Any]]:
        try:
            if plan == BillingPlans.PRO:
                prices = Price.list(product=cls.PRO, active=True)

                return [
                    {
                        "id": price.get("id"),
                        "type": price.get("metadata").get("billing_type"),
                        "amount": price.get("unit_amount"),
                    }
                    for price in prices
                ]
        except Exception as e:
            raise Exception(f"Stripe: prices for plan {plan} could not be retrieved, error {e}")

        return []

    @staticmethod
    def get_plans_names():
        return {plan.name: plan.value for plan in PlanName}

    @staticmethod
    def get_plan_name_to_render(plan):
        """
        >>> PlansService.get_plan_name_to_render(BillingPlans.DEV)
        'Build'
        >>> PlansService.get_plan_name_to_render(BillingPlans.PRO)
        'Pro'
        >>> PlansService.get_plan_name_to_render(BillingPlans.ENTERPRISE)
        'Enterprise'
        >>> PlansService.get_plan_name_to_render(BillingPlans.BRANCH_ENTERPRISE)
        'Enterprise'
        >>> PlansService.get_plan_name_to_render('other_plan')
        'Custom'
        """
        if plan == BillingPlans.DEV:
            return PlanName.DEV.value
        if plan == BillingPlans.PRO:
            return PlanName.PRO.value
        if plan in (BillingPlans.ENTERPRISE, BillingPlans.BRANCH_ENTERPRISE):
            return PlanName.ENTERPRISE.value
        return "Custom"

    @classmethod
    async def get_workspace_limits(cls, workspace: User, metrics_cluster: Optional[str] = None):
        limits = {}
        if workspace.plan == BillingPlans.DEV:
            plan_details = await PlansService.get_workspace_plan_info(
                workspace=workspace, metrics_cluster=metrics_cluster
            )

            for concept in plan_details["packages"][0]["concepts"]:
                limit_key = concept.pop("name")
                limits[limit_key] = concept

        pipe_limits = await cls.get_pipe_limits(workspace)
        return {**limits, **pipe_limits}

    @classmethod
    async def get_pipe_limits(cls, workspace: User):
        from tinybird.plan_limits.copy import CopyLimits  # Avoid circular dependency

        pipes = workspace.get_pipes()
        copy_pipes = 0
        sink_pipes = 0

        for pipe in pipes:
            if pipe.pipe_type == PipeTypes.COPY:
                copy_pipes += 1
            elif pipe.pipe_type == PipeTypes.DATA_SINK:
                sink_pipes += 1

        limits = {
            "copy_pipes": {"quantity": copy_pipes, "max": CopyLimits.max_copy_pipes.get_limit_for(workspace)},
            "sink_pipes": {"quantity": sink_pipes, "max": SinkLimits.max_sink_pipes.get_limit_for(workspace)},
        }

        return limits

    @classmethod
    async def get_workspace_plan_info(
        cls,
        workspace: User,
        year: Optional[str] = None,
        month: Optional[str] = None,
        metrics_cluster: Optional[str] = None,
    ):
        if workspace.plan == BillingPlans.DEV:
            packages = await cls._get_packages_for_dev_plan(workspace, year, month)
        elif workspace.plan == BillingPlans.PRO:
            packages = await cls._get_packages_for_pro_plan(workspace, year, month, metrics_cluster)
        elif workspace.plan == BillingPlans.ENTERPRISE:
            packages = await cls._get_packages_for_enterprise_plan(workspace, year, month, metrics_cluster)
        else:
            packages = []
        return {"plan": workspace.plan, "packages": packages}

    @classmethod
    async def _get_packages_for_dev_plan(cls, workspace: User, year: Optional[str], month: Optional[str]):
        total_stored_bytes = await cls.get_storage_bytes_used_total_month(workspace, year, month)

        return [
            {
                "type": "dev",
                "concepts": [
                    {
                        "name": "max_api_requests_per_day",
                        "quantity": await cls.get_today_api_requests(workspace),
                        "max": cls._get_value_for_config(workspace, PlanConfigConcepts.DEV_MAX_API_REQUESTS_PER_DAY),
                    },
                    {
                        "name": "max_gb_storage_used",
                        "quantity": round(total_stored_bytes / (1000**3), 3),
                        "max": cls._get_value_for_config(workspace, PlanConfigConcepts.DEV_MAX_GB_STORAGE_USED),
                    },
                ],
                "notifications": workspace.billing_details.get("notifications", {}),
            }
        ]

    @classmethod
    def get_pro_plan_prices(cls) -> Tuple[Optional[float], Optional[float]]:
        processed_price = None
        storage_price = None
        for price in cls.get_default_prices_by_plan(BillingPlans.PRO):
            if price["type"] == BillingTypes.PROCESSED:
                processed_price = price["amount"] / 100
            elif price["type"] == BillingTypes.STORAGE:
                storage_price = price["amount"] / 100
        return processed_price, storage_price

    @classmethod
    async def _get_packages_for_pro_plan(
        cls, workspace: User, year: Optional[str], month: Optional[str], metrics_cluster: Optional[str]
    ):
        current_processed_bytes = await cls.get_processed_bytes_used_total_month(
            workspace, year, month, metrics_cluster
        )
        current_stored_bytes = await cls.get_storage_bytes_used_total_month(workspace, year, month)

        price_per_processed_gb_pro, price_per_stored_gb_pro = cls.get_pro_plan_prices()

        return [
            cls._calculate_extra_package_and_return_final_json(
                current_processed_bytes, current_stored_bytes, price_per_processed_gb_pro, price_per_stored_gb_pro
            )
        ]

    @classmethod
    async def _get_packages_for_enterprise_plan(
        cls, workspace: User, year: Optional[str], month: Optional[str], metrics_cluster: Optional[str]
    ):
        remaining_processed_bytes = await cls.get_processed_bytes_used_total_month(
            workspace, year, month, metrics_cluster
        )
        remaining_stored_bytes = await cls.get_storage_bytes_used_total_month(workspace, year, month)

        packages_json = []

        user_packages = workspace.billing_details["packages"]
        user_packages.sort(key=lambda package: 0 if package["type"] == PackageType.FREE.value else 1)

        for package in user_packages:
            if package["type"] == PackageType.FREE.value:
                (
                    remaining_processed_bytes,
                    remaining_stored_bytes,
                    new_json,
                ) = cls._calculate_free_package_and_return_final_json(
                    remaining_processed_bytes,
                    remaining_stored_bytes,
                    package["processed_gb_included"],
                    package["stored_gb_included"],
                )
            elif package["type"] == PackageType.COMMITTED.value:
                (
                    remaining_processed_bytes,
                    remaining_stored_bytes,
                    new_json,
                ) = cls._calculate_committed_package_and_return_final_json(
                    remaining_processed_bytes,
                    remaining_stored_bytes,
                    package["price_per_processed_gb"],
                    package["price_per_stored_gb"],
                    package["processed_gb_included"],
                    package["stored_gb_included"],
                )
            else:
                raise PlansException(f"Package type '{package['type']}' not supported.")
            packages_json.append(new_json)

        # TODO define the logic prices for enterprise
        price_per_processed_gb_pro = 0.07
        price_per_stored_gb_pro = 0.34

        packages_json.append(
            cls._calculate_extra_package_and_return_final_json(
                remaining_processed_bytes, remaining_stored_bytes, price_per_processed_gb_pro, price_per_stored_gb_pro
            )
        )

        return packages_json

    @staticmethod
    def _calculate_how_much_quantity_fits_in_bucket(quantity, bucket_size):
        """
        >>> PlansService._calculate_how_much_quantity_fits_in_bucket(5, 10)
        (5, 0)
        >>> PlansService._calculate_how_much_quantity_fits_in_bucket(15, 10)
        (10, 5)
        >>> PlansService._calculate_how_much_quantity_fits_in_bucket(0, 10)
        (0, 0)
        """
        if quantity > bucket_size:
            return bucket_size, quantity - bucket_size
        else:
            return quantity, 0

    @classmethod
    def _calculate_free_package_and_return_final_json(
        cls, current_processed_bytes, current_stored_bytes, free_processed_gb, free_stored_gb
    ):
        (
            included_processed_bytes_in_package,
            remaining_processed_bytes,
        ) = PlansService._calculate_how_much_quantity_fits_in_bucket(
            current_processed_bytes, free_processed_gb * (1000**3)
        )
        (
            included_stored_bytes_in_package,
            remaining_stored_bytes,
        ) = PlansService._calculate_how_much_quantity_fits_in_bucket(current_stored_bytes, free_stored_gb * (1000**3))

        return (
            remaining_processed_bytes,
            remaining_stored_bytes,
            {
                "type": PackageType.FREE.value,
                "concepts": [
                    {
                        "name": "processed_gb",
                        "quantity": round(included_processed_bytes_in_package / (1000**3), 3),
                        "included": free_processed_gb,
                    },
                    {
                        "name": "storage_gb",
                        "quantity": round(included_stored_bytes_in_package / (1000**3), 3),
                        "included": free_stored_gb,
                    },
                ],
            },
        )

    @classmethod
    def _calculate_committed_package_and_return_final_json(
        cls,
        current_processed_bytes,
        current_stored_bytes,
        price_per_processed_gb,
        price_per_stored_gb,
        included_processed_gb,
        included_stored_gb,
    ):
        (
            included_processed_bytes_in_package,
            remaining_processed_bytes,
        ) = PlansService._calculate_how_much_quantity_fits_in_bucket(
            current_processed_bytes, included_processed_gb * (1000**3)
        )
        (
            included_stored_bytes_in_package,
            remaining_stored_bytes,
        ) = PlansService._calculate_how_much_quantity_fits_in_bucket(
            current_stored_bytes, included_stored_gb * (1000**3)
        )

        return (
            remaining_processed_bytes,
            remaining_stored_bytes,
            {
                "type": PackageType.COMMITTED.value,
                "concepts": [
                    {
                        "name": "processed_gb",
                        "quantity": round(included_processed_bytes_in_package / (1000**3), 3),
                        "included": included_processed_gb,
                        "price_per_unit": price_per_processed_gb,
                    },
                    {
                        "name": "storage_gb",
                        "quantity": round(included_stored_bytes_in_package / (1000**3), 3),
                        "included": included_stored_gb,
                        "price_per_unit": price_per_stored_gb,
                    },
                ],
            },
        )

    @classmethod
    def _calculate_extra_package_and_return_final_json(
        cls, current_processed_bytes, remaining_stored_bytes, price_per_processed_gb, price_per_stored_gb
    ):
        return {
            "type": PackageType.EXTRA.value,
            "concepts": [
                {
                    "name": "processed_gb",
                    "quantity": round(current_processed_bytes / (1000**3), 3),
                    "price_per_unit": price_per_processed_gb,
                },
                {
                    "name": "storage_gb",
                    "quantity": round(remaining_stored_bytes / (1000**3), 3),
                    "price_per_unit": price_per_stored_gb,
                },
            ],
        }

    @staticmethod
    def _bytes_to_gb(amount) -> int:
        return int(math.floor(float(amount) / 1000.0**3))

    @staticmethod
    def _gb_to_bytes(amount):
        return amount * (1000.0**3)

    @classmethod
    def _try_get_datasource(
        cls, workspace: User, datasource_name: str, raise_on_not_found: bool = False
    ) -> Optional[Datasource]:
        """Tries to get the specified datasource from the passed workspace.

        If not found, logs an exception for us to be able to get the alert and, optionally, raises an exception."""
        result = workspace.get_datasource(datasource_name)
        if not result:
            msg = f"{datasource_name} data source not found in the {workspace.name} workspace (id: {workspace.id})"
            logging.exception(msg)
            if raise_on_not_found:
                raise Exception(msg)
        return result

    @classmethod
    async def get_upgrade_info(cls, workspace: User, metrics_cluster: Optional[str]):
        max_api_requests_per_day_dev = cls._get_value_for_config(
            workspace, PlanConfigConcepts.DEV_MAX_API_REQUESTS_PER_DAY
        )
        max_gb_storage_used_dev = cls._get_value_for_config(workspace, PlanConfigConcepts.DEV_MAX_GB_STORAGE_USED)

        price_per_processed_gb_pro, price_per_stored_gb_pro = cls.get_pro_plan_prices()

        if price_per_processed_gb_pro is None or price_per_stored_gb_pro is None:
            raise Exception(f"Stripe: prices for plan {BillingPlans.PRO} could not be retrieved")

        if workspace.plan == BillingPlans.DEV:
            storage = await cls.get_storage_bytes_used_total_month(workspace)
            processed = await cls.get_processed_bytes_used_total_month(workspace, metrics_cluster=metrics_cluster)

            storage_gb = PlansService._bytes_to_gb(storage)
            processed_gb = PlansService._bytes_to_gb(processed)

            storage_price = price_per_stored_gb_pro * storage_gb
            processed_price = price_per_processed_gb_pro * processed_gb

            estimation_based_on_current_usage = round(storage_price + processed_price, 2)
        else:
            estimation_based_on_current_usage = 0

        response = {
            "current_plan": workspace.plan,
            "options": {
                BillingPlans.DEV: {
                    "max_api_requests_per_day": max_api_requests_per_day_dev,
                    "max_gb_storage_used": max_gb_storage_used_dev,
                },
                BillingPlans.PRO: {
                    "price_per_processed_gb": price_per_processed_gb_pro,
                    "price_per_stored_gb": price_per_stored_gb_pro,
                    "estimation_based_on_current_usage": estimation_based_on_current_usage,
                },
            },
        }

        return response

    @classmethod
    def _get_value_for_config(cls, workspace: User, config_value: PlanConfigConcepts) -> float:
        return workspace.billing_details["prices_overrides"].get(config_value.value, DEFAULT_PLAN_CONFIG[config_value])

    @classmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def override_default_config(
        cls, workspace: User, config: PlanConfigConcepts, new_value: Optional[float] = None
    ):
        with User.transaction(workspace.id) as workspace:
            if new_value is None:
                if config.value in workspace.billing_details["prices_overrides"]:
                    del workspace.billing_details["prices_overrides"][config.value]
            else:
                workspace.billing_details["prices_overrides"][config.value] = new_value

    @classmethod
    async def get_today_api_requests(cls, workspace: User):
        pu = public.get_public_user()
        pipe_stats_rt = pu.get_datasource("pipe_stats_rt")
        if not pipe_stats_rt:
            raise Exception("pipe_stats Data Source not found in the public user")
        client = HTTPClient(pu.database_server)
        # TODO pending to filter for the correct requests being billed.
        _, result = await client.query(
            f"""
        SELECT count(*) as api_request_done
        FROM {pu.database}.{pipe_stats_rt.id}
        WHERE
            start_datetime >= today()
            AND user_id = '{workspace.id}'
            AND billable = 1
        FORMAT JSON
        """
        )
        query_result = json.loads(result).get("data")[0]["api_request_done"]
        return query_result

    @classmethod
    async def get_workspaces_metrics(
        cls, workspaces_ids: Iterable[str], _from: datetime, to: datetime, billable_only: bool
    ) -> Dict[str, WorkspaceMetricsInfo]:
        """Gets processed and storage metrics for a list of workspaces ids.

        The result is an Dict[<workspace_id:str>, WorkspaceMetricsInfo].
        """
        if not workspaces_ids:
            return {}

        pu = public.get_public_user()

        workspaces_all = cls._try_get_datasource(pu, "workspaces_all", raise_on_not_found=True)
        assert isinstance(workspaces_all, Datasource)

        usage_metrics_storage__v2 = cls._try_get_datasource(pu, "usage_metrics_storage__v2", raise_on_not_found=True)
        assert isinstance(usage_metrics_storage__v2, Datasource)

        distributed_billing_processed_usage_log = cls._try_get_datasource(
            pu, "distributed_billing_processed_usage_log", raise_on_not_found=True
        )
        assert isinstance(distributed_billing_processed_usage_log, Datasource)

        ids = "'" + "','".join(workspaces_ids) + "'"

        #
        # SQL explanation:
        #
        # - sql_calendar:   All days in the selected period. Used to ensure we hav records for all days, even when
        #                   no data in the database.
        # - sql_workspaces: Workspace name and billing info. Also maps between workspace id and database.
        # - sql_processed:  Processing data aggregated by day and database.
        # - sql_storage:    Storage data aggregated by day and workspace id.
        # - sql:            Where we do the actual work.
        #
        # Notes:
        # - We try yo minimize scanned data as much as possible. That's the reason you see user_id and database
        #   filters by workspace ids.
        #

        billable_filter = "AND lower(plan) != 'dev'" if billable_only else ""

        sql_workspaces = f"""
            SELECT id, name, database, plan
            FROM {pu.database}.{workspaces_all.id} FINAL
            WHERE id IN ({ids})
            {billable_filter}
        """

        # We're interested in the maximum storage used in the last hour
        # available on the interval
        end_date_storage = f"toDate('{to.strftime('%Y-%m-%d')}')"

        # Get storage aggregated by workspace.
        # Note: We aggregate by datasource first to avoid getting duplicate data
        #       in the case the ReplaceMergeTree hasn't finished working yet.

        sql_storage_by_datasource = f"""
            SELECT st.user_id               AS id,
                   st.datasource_id         AS ds_id,
                   max(st.bytes)            AS bytes,
                   max(st.bytes_quarantine) AS bytes_quarantine
            FROM {pu.database}.{usage_metrics_storage__v2.id} AS st
            WHERE toDate(timestamp) == {end_date_storage}
              AND user_id IN ({ids})
            GROUP BY st.user_id, st.datasource_id
        """

        sql_storage_by_workspace = f"""
            SELECT id,
                   sum(bytes)            AS bytes,
                   sum(bytes_quarantine) AS bytes_quarantine
            FROM ({sql_storage_by_datasource})
            GROUP BY id
        """

        # Get processed data by workspace

        start_date_processed = f"toDate('{_from.strftime('%Y-%m-%d')}')"
        end_date_processed = f"toDate('{to.strftime('%Y-%m-%d')}')"
        sql_processed = f"""
            SELECT database,
                   sum(read_bytes)    AS read_bytes,
                   sum(written_bytes) AS written_bytes
            FROM {pu.database}.{distributed_billing_processed_usage_log.id}
            WHERE date >= {start_date_processed}
              AND date <= {end_date_processed}
              AND database GLOBAL IN (SELECT database FROM {pu.database}.{workspaces_all.id} FINAL WHERE id IN ({ids}))
            GROUP BY database
        """

        # Final query

        sql = f"""
            SELECT workspace.id                                           AS workspace_id,
                   workspace.name                                         AS workspace_name,
                   (ds_processed.read_bytes + ds_processed.written_bytes) AS processed,
                   (ds_storage.bytes + ds_storage.bytes_quarantine)       AS storage,
                   (lower(workspace.plan) != 'dev')                       AS is_billable
            FROM ({sql_workspaces}) as workspace
            LEFT JOIN ({sql_storage_by_workspace}) AS ds_storage ON workspace.id = ds_storage.id
            LEFT JOIN ({sql_processed}) AS ds_processed ON workspace.database = ds_processed.database
            ORDER BY workspace.id
            FORMAT JSON
            """

        try:
            client = HTTPClient(pu.database_server)
            _, query_result = await client.query(sql)
        except CHException as e:
            logging.exception(f"Failed to get metrics for workspaces {ids}. Error: {e}")
            raise PlansException(PlansStatisticsErrors.STATS_QUERY)

        return dict(
            (row["workspace_id"], WorkspaceMetricsInfo(**row)) for row in json.loads(query_result).get("data", [])
        )

    @classmethod
    async def get_workspaces_storage_by_day(
        cls, workspaces_ids: Iterable[str], _from: datetime, to: datetime
    ) -> Iterable[WorkspaceStorageByDayInfo]:
        """Gets storage for a list of workspaces ids aggregated by day.

        The result is an iterable of WorkspaceSingleMetricByDayInfo.
        """
        if not workspaces_ids:
            return {}

        pu = public.get_public_user()

        workspaces_all = cls._try_get_datasource(pu, "workspaces_all", raise_on_not_found=True)
        assert isinstance(workspaces_all, Datasource)

        usage_metrics_storage__v2 = cls._try_get_datasource(pu, "usage_metrics_storage__v2", raise_on_not_found=True)
        assert isinstance(usage_metrics_storage__v2, Datasource)

        start_date = f"toDate('{_from.strftime('%Y-%m-%d')}')"
        end_date = f"toDate('{to.strftime('%Y-%m-%d')}')"

        ids = "'" + "','".join(workspaces_ids) + "'"

        sql_workspaces = f"""
            SELECT id, database
            FROM {pu.database}.{workspaces_all.id} FINAL
            WHERE lower(plan) != 'dev'
              AND id GLOBAL IN ({ids})
        """

        sql_workspaces_and_dates = f"""
            SELECT day, id, database
            FROM ({sql_workspaces})
            CROSS JOIN (
                SELECT *
                FROM (
                    SELECT arrayJoin(
                        arrayMap(
                            x -> toDate(x),
                            range(toUInt32({start_date}), toUInt32(toDate({end_date} + INTERVAL 1 DAY)), 1)
                        )
                    ) AS day
                )
            )
        """

        # Get storage aggregated by workspace.
        # Note: We aggregate by datasource first to avoid getting duplicate data
        #       in the case the ReplaceMergeTree hasn't finished working yet.

        sql = f"""
            SELECT day,
                   workspace_id,
                   sum(bytes)               AS bytes,
                   sum(bytes_quarantine)    AS bytes_quarantine
            FROM ({sql_workspaces_and_dates}) AS workspace
            JOIN (
                SELECT toDate(timestamp)        AS day,
                       user_id                  AS workspace_id,
                       datasource_id            AS datasource_id,
                       max(bytes)               AS bytes,
                       max(bytes_quarantine)    AS bytes_quarantine
                FROM {pu.database}.{usage_metrics_storage__v2.id} AS storage
                WHERE timestamp >= {start_date}
                  AND timestamp < {end_date} + INTERVAL 1 DAY
                  AND user_id in (SELECT id FROM ({sql_workspaces}))
                GROUP BY day, workspace_id, datasource_id
            ) AS result
                ON workspace.day == result.day
               AND workspace.id  == result.workspace_id
            GROUP BY day, workspace_id
            ORDER BY day ASC, workspace_id
            FORMAT JSON
        """

        try:
            client = HTTPClient(pu.database_server)
            _, query_result = await client.query(sql)
        except CHException as e:
            logging.exception(f"Failed to get storage info for workspaces {ids}. Error: {e}")
            raise PlansException(PlansStatisticsErrors.STATS_QUERY)

        return tuple(WorkspaceStorageByDayInfo(**row) for row in json.loads(query_result).get("data", []))

    @classmethod
    async def get_workspaces_processed_by_day(
        cls, workspaces_ids: Iterable[str], _from: datetime, to: datetime
    ) -> Iterable[WorkspaceProcessedByDayInfo]:
        """Gets storage for a list of workspaces ids aggregated by day.

        The result is an Dict[<workspace_id:str>, WorkspaceSingleMetricInfo].
        """
        if not workspaces_ids:
            return {}

        pu = public.get_public_user()

        workspaces_all = cls._try_get_datasource(pu, "workspaces_all", raise_on_not_found=True)
        assert isinstance(workspaces_all, Datasource)

        distributed_billing_processed_usage_log = cls._try_get_datasource(
            pu, "distributed_billing_processed_usage_log", raise_on_not_found=True
        )
        assert isinstance(distributed_billing_processed_usage_log, Datasource)

        ids = "'" + "','".join(workspaces_ids) + "'"
        start_date = f"toDate('{_from.strftime('%Y-%m-%d')}')"
        end_date = f"toDate('{to.strftime('%Y-%m-%d')}')"

        sql_workspaces = f"""
            SELECT id, database
            FROM {pu.database}.{workspaces_all.id} FINAL
            WHERE lower(plan) != 'dev'
              AND id GLOBAL IN ({ids})
        """

        sql_workspaces_and_dates = f"""
            SELECT day, id, database
            FROM ({sql_workspaces})
            CROSS JOIN (
                SELECT *
                FROM (
                    SELECT arrayJoin(
                        arrayMap(
                            x -> toDate(x),
                            range(toUInt32({start_date}), toUInt32(toDate({end_date} + INTERVAL 1 DAY)), 1)
                        )
                    ) AS day
                )
            )
        """

        #
        # SQL explanation:
        #
        # - sql_calendar:   All days in the selected period. Used to ensure we hav records for all days, even when
        #                   no data in the database.
        # - sql_workspaces: Workspace name and billing info. Also maps between workspace id and database.
        # - sql_processed:  Processing data aggregated by day and database.
        # - sql:            Where we do the actual work.
        #
        # Notes:
        # - We try yo minimize scanned data as much as possible. That's the reason you see user_id and database
        #   filters by workspace ids.
        #

        sql_processed = f"""
            SELECT toDate(date)         AS day,
                   database,
                   sum(read_bytes)      AS read_bytes,
                   sum(written_bytes)   AS written_bytes
            FROM {pu.database}.{distributed_billing_processed_usage_log.id}
            WHERE date >= {start_date}
              AND date <= {end_date}
              AND database GLOBAL IN (SELECT database FROM ({sql_workspaces}))
            GROUP BY day, database
        """

        sql = f"""
            SELECT day,
                   id as workspace_id,
                   read_bytes,
                   written_bytes
            FROM ({sql_workspaces_and_dates}) AS workspace
            LEFT JOIN ({sql_processed}) AS processed
                   ON workspace.day      == processed.day
                  AND workspace.database == processed.database
            ORDER BY day ASC
            FORMAT JSON
            """

        try:
            client = HTTPClient(pu.database_server)
            _, query_result = await client.query(sql)
        except CHException as e:
            logging.exception(f"Failed to get processed info for workspaces {ids}. Error: {e}")
            raise PlansException(PlansStatisticsErrors.STATS_QUERY)

        return tuple(WorkspaceProcessedByDayInfo(**row) for row in json.loads(query_result).get("data", []))

    @classmethod
    async def get_cumulative_request_along_the_month(
        cls, workspace: User, _from: datetime, to: datetime, metrics_cluster: Optional[str] = None
    ) -> Dict[str, Any]:
        pu = public.get_public_user()

        pipe_stats = cls._try_get_datasource(pu, "pipe_stats", raise_on_not_found=True)
        assert isinstance(pipe_stats, Datasource)

        bi_stats = (
            cls._try_get_datasource(pu, "distributed_bi_connector_stats")
            if metrics_cluster
            else cls._try_get_datasource(pu, "bi_connector_stats")
        )

        client = HTTPClient(pu.database_server)

        start_date = f"toDate('{_from.strftime('%Y-%m-%d')}')"
        end_date = f"toDate('{to.strftime('%Y-%m-%d')}')"
        date_filter = f"(date >= {start_date} AND date <= {end_date})"

        inner_tables_list: List[str] = []

        inner_tables_list.append(
            f"""
            (SELECT
                date AS day,
                sumIf(view_count, pipe_id != 'query_api') AS api_endpoints,
                sumIf(view_count, pipe_id == 'query_api') AS sql,
                0 as bi_connector
            FROM {pu.database}.{pipe_stats.id}
            WHERE
                {date_filter}
                AND user_id = '{workspace.id}'
                AND billable = 1
            GROUP BY day
            ORDER BY day ASC)
            """
        )

        if bi_stats:
            inner_tables_list.append(
                f"""
                (SELECT
                    date AS day,
                    0 AS api_endpoints,
                    0 AS sql,
                    sum(view_count) AS bi_connector
                FROM {pu.database}.{bi_stats.id}
                WHERE
                    {date_filter}
                    AND database = '{workspace.database}'
                GROUP BY day
                ORDER BY day ASC)
                """
            )

        assert len(inner_tables_list) > 0
        inner_tables = " UNION ALL ".join(inner_tables_list)

        sql = f"""
            SELECT day,
                   api_endpoints,
                   sql,
                   bi_connector,
                   api_endpoints + sql + bi_connector AS total
            FROM (
                SELECT
                    groupArray(day) AS day,
                    groupArrayMovingSum(api_endpoints) AS api_endpoints,
                    groupArrayMovingSum(sql) AS sql,
                    groupArrayMovingSum(bi_connector) AS bi_connector
                FROM (
                    SELECT *
                    FROM (
                        SELECT arrayJoin(arrayMap(x -> toDate(x), range(toUInt32({start_date}), toUInt32({end_date} + INTERVAL 1 DAY), 1))) day
                    )
                    LEFT JOIN (
                        {inner_tables}
                    ) USING day
                )
            ) ARRAY JOIN day, api_endpoints, sql, bi_connector
            ORDER BY day ASC
            FORMAT JSON
        """

        try:
            _, result = await client.query(sql)
        except CHException as e:
            logging.exception(
                f"Failed to get stats for get_cumulative_request_along_the_month. Workspace: {workspace.id}. Error: {e}"
            )
            raise PlansException(PlansStatisticsErrors.STATS_QUERY)

        return {"data": json.loads(result).get("data", [])}

    @classmethod
    async def get_daily_request_along_the_month(
        cls, workspace: User, _from: datetime, to: datetime, metrics_cluster: Optional[str] = None
    ) -> Dict[str, Any]:
        pu = public.get_public_user()

        pipe_stats = cls._try_get_datasource(pu, "pipe_stats", raise_on_not_found=True)
        assert isinstance(pipe_stats, Datasource)

        bi_stats = (
            cls._try_get_datasource(pu, "distributed_bi_connector_stats")
            if metrics_cluster
            else cls._try_get_datasource(pu, "bi_connector_stats")
        )

        client = HTTPClient(pu.database_server)

        start_date = f"toDate('{_from.strftime('%Y-%m-%d')}')"
        end_date = f"toDate('{to.strftime('%Y-%m-%d')}')"
        date_filter = f"(date >= {start_date} AND date <= {end_date})"

        inner_tables_list: List[str] = []

        inner_tables_list.append(
            f"""
            (SELECT toDate(date)                                AS day,
                    sumIf(view_count, pipe_id != 'query_api')   AS api_endpoints,
                    sumIf(view_count, pipe_id == 'query_api')   AS sql,
                    0                                           AS bi_connector
            FROM {pu.database}.{pipe_stats.id}
            WHERE {date_filter}
              AND user_id = '{workspace.id}'
              AND billable = 1
            GROUP BY day)
            """
        )

        if bi_stats:
            inner_tables_list.append(
                f"""
                (SELECT toDate(date)    AS day,
                        0               AS api_endpoints,
                        0               AS sql,
                        sum(view_count) AS bi_connector
                FROM {pu.database}.{bi_stats.id}
                WHERE {date_filter}
                  AND database = '{workspace.database}'
                GROUP BY day)
                """
            )

        assert len(inner_tables_list) > 0
        inner_tables = " UNION ALL ".join(inner_tables_list)

        sql_days = f"""
            SELECT arrayJoin(arrayMap(x -> toDate(x), range(toUInt32({start_date}), toUInt32({end_date} + INTERVAL 1 DAY), 1))) day
        """

        sql = f"""
            SELECT day                      AS day,
                   sum(inner.api_endpoints) AS api_endpoints,
                   sum(inner.sql)           AS sql,
                   sum(inner.bi_connector)  AS bi_connector,
                   api_endpoints + sql + bi_connector AS total
            FROM ({sql_days})
            LEFT JOIN ({inner_tables}) AS inner USING day
            GROUP BY day
            ORDER BY day ASC
            FORMAT JSON
            """

        try:
            _, result = await client.query(sql)
        except CHException as e:
            logging.exception(
                f"Failed to get stats for get_daily_request_along_the_month. Workspace: {workspace.id}. Error: {e}"
            )
            raise PlansException(PlansStatisticsErrors.STATS_QUERY)

        return {"data": json.loads(result).get("data", [])}

    @classmethod
    async def get_storage_bytes_used_along_the_month(
        cls, workspace: User, _from: datetime, to: datetime
    ) -> Dict[str, Any]:
        pu = public.get_public_user()
        usage_metrics_storage = cls._try_get_datasource(pu, "usage_metrics_storage__v2")

        if not usage_metrics_storage:
            return {"data": []}

        client = HTTPClient(pu.database_server)
        # TODO Pending to use the correct usage_metrics_storage that just track datasources and not orphan tables
        # TODO usage_metrics_storage may contain more than one row for the same database as the same database may have data
        # in different instances. Pending to define if we want to bill for replicated data.

        start_date = f"toDateTime('{_from.strftime('%Y-%m-%d %H:%M:%S')}')"
        end_date = f"toDateTime('{to.strftime('%Y-%m-%d %H:%M:%S')}')"
        date_filter = f"(timestamp >= {start_date} AND timestamp <= {end_date})"

        sql = f"""
                SELECT day,
                       sum(max_bytes) + sum(max_bytes_quarantine) AS total
                FROM (
                    SELECT day,
                           datasource_id,
                           max(bytes) as max_bytes,
                           max(bytes_quarantine) as max_bytes_quarantine
                    FROM {pu.database}.{usage_metrics_storage.id}
                    WHERE {date_filter}
                      AND user_id = '{workspace.id}'
                    GROUP BY toDate(timestamp) as day, datasource_id
                    ORDER BY day DESC
                )
                GROUP BY day
                ORDER BY day ASC
            FORMAT JSON
        """

        try:
            _, result = await client.query(sql)
        except CHException as e:
            logging.exception(
                f"Failed to get stats for get_storage_bytes_used_along_the_month. Workspace: {workspace.id}. Error: {e}"
            )
            raise PlansException(PlansStatisticsErrors.STATS_QUERY)

        return {"data": json.loads(result).get("data", [])}

    @classmethod
    async def get_storage_bytes_used_total_month(
        cls, workspace: User, year: Optional[str] = None, month: Optional[str] = None
    ) -> int:
        # TODO Same problems as with the query for stored GB used along the month
        pu = public.get_public_user()
        usage_metrics_storage = pu.get_datasource("usage_metrics_storage__v2")

        if not usage_metrics_storage:
            return 0

        if month and year:
            start_date = f"toDate('{year}-{month}-1')"
        else:
            start_date = "toStartOfMonth(today())"

        sql = f"""
                    SELECT sum(max_bytes) + sum(max_bytes_quarantine) as total FROM (
                        SELECT day,
                               datasource_id,
                               max(bytes) as max_bytes,
                               max(bytes_quarantine) as max_bytes_quarantine
                        FROM {pu.database}.{usage_metrics_storage.id}
                        WHERE toStartOfMonth(timestamp) = {start_date}
                        AND user_id = '{workspace.id}'
                        GROUP BY toStartOfDay(timestamp) as day, datasource_id
                        ORDER BY day DESC
                        )
                    GROUP BY day
                    ORDER BY day DESC
                    LIMIT 1
                    FORMAT JSON
                """
        client = HTTPClient(pu.database_server)

        try:
            _, result = await client.query(sql)
        except CHException as e:
            logging.exception(
                f"Failed to get stats for get_storage_bytes_used_total_month. Workspace: {workspace.id}. Error: {e}"
            )
            raise PlansException(PlansStatisticsErrors.STATS_QUERY)

        storage_used = json.loads(result)["data"]
        if not len(storage_used):
            return 0
        return storage_used[0]["total"]

    @classmethod
    def get_storage_bytes_used_total_date_sync(
        cls, workspace: User, year: Optional[str] = None, month: Optional[str] = None, day: Optional[str] = None
    ) -> int:
        pu = public.get_public_user()
        usage_metrics_storage = pu.get_datasource("usage_metrics_storage__v2")

        if not usage_metrics_storage:
            return 0

        if month and year:
            date_filter = f"toStartOfDay(timestamp) == toDate('{year}-{month}-{day}')"
        else:
            date_filter = "toStartOfDay(timestamp) == today()"

        sql = f"""
                SELECT sum(total_bytes+total_bytes_quarantine) as total_bytes
                FROM
                    (SELECT max(bytes) as total_bytes, max(bytes_quarantine) as total_bytes_quarantine
                     FROM {pu.database}.{usage_metrics_storage.id}
                     WHERE {date_filter}
                     AND user_id = '{workspace.id}'
                     GROUP BY  toStartOfDay(timestamp), datasource_id)
                FORMAT JSON
            """

        client = HTTPClient(pu.database_server)

        try:
            _, result = client.query_sync(sql)
        except CHException as e:
            logging.exception(f"Failed to get stats for get_storage_bytes_used_total_date_sync: {e}")
            raise PlansException(PlansStatisticsErrors.STATS_QUERY)

        storage_used = json.loads(result)["data"]

        if not len(storage_used):
            return 0
        return storage_used[0]["total_bytes"]

    @classmethod
    async def get_processed_bytes_used_total_month(
        cls,
        workspace: User,
        year: Optional[str] = None,
        month: Optional[str] = None,
        metrics_cluster: Optional[str] = None,
    ) -> int:
        pu = public.get_public_user()
        client = HTTPClient(pu.database_server)
        usage_metrics_processed = None

        if metrics_cluster:
            try:
                usage_metrics_processed = pu.get_datasource("distributed_billing_processed_usage_log")
            except Exception:
                pass

        if not usage_metrics_processed:
            return 0

        if month and year:
            date_filter = f"date >= toDate('{year}-{month}-1') AND date < toDate('{year}-{month}-1') + INTERVAL 1 MONTH"
        else:
            date_filter = "date >= toStartOfMonth(today())"

        sql = f"""
            SELECT
                sum(read_bytes) as read_bytes,
                sum(written_bytes) as written_bytes
            FROM {pu.database}.{usage_metrics_processed.id}
            WHERE database = '{workspace.database}'
                AND {date_filter}
            FORMAT JSON
        """

        try:
            _, result = await client.query(sql)
        except CHException as e:
            logging.exception(
                f"Failed to get stats for processed_bytes_used_total_month. Workspace: {workspace.id}. Error: {e}"
            )
            raise PlansException(PlansStatisticsErrors.STATS_QUERY)

        query_result = json.loads(result).get("data")

        if not len(query_result):
            return 0
        else:
            return int(query_result[0]["read_bytes"]) + int(query_result[0]["written_bytes"])

    @classmethod
    def get_processed_bytes_used_total_date_sync(
        cls,
        workspace: User,
        year: Optional[str] = None,
        month: Optional[str] = None,
        day: Optional[str] = None,
        metrics_cluster: Optional[str] = None,
    ) -> int:
        pu = public.get_public_user()
        client = HTTPClient(pu.database_server)
        usage_metrics_processed = None

        if metrics_cluster:
            try:
                usage_metrics_processed = pu.get_datasource("distributed_billing_processed_usage_log")
            except Exception:
                pass

        if not usage_metrics_processed:
            return 0

        if month and year and day:
            date_filter = f"date = toDate('{year}-{month}-{day}')"
        else:
            date_filter = "date = today()"

        sql = f"""
            SELECT
                sum(read_bytes) as read_bytes,
                sum(written_bytes) as written_bytes
            FROM {pu.database}.{usage_metrics_processed.id}
            WHERE database = '{workspace.database}'
                AND {date_filter}
            FORMAT JSON
        """

        try:
            _, result = client.query_sync(sql)
        except CHException as e:
            logging.exception(f"Failed to get stats for get_processed_bytes_used_total_date_sync: {e}")
            raise PlansException(PlansStatisticsErrors.STATS_QUERY)

        query_result = json.loads(result).get("data")

        if not len(query_result):
            return 0
        else:
            return int(query_result[0]["read_bytes"]) + int(query_result[0]["written_bytes"])

    @classmethod
    async def get_processed_bytes_used_along_the_month(
        cls, workspace: User, _from: datetime, to: datetime, metrics_cluster: Optional[str] = None
    ):
        pu = public.get_public_user()
        client = HTTPClient(pu.database_server)
        usage_metrics_processed = None

        if metrics_cluster:
            try:
                usage_metrics_processed = pu.get_datasource("distributed_billing_processed_usage_log")
            except Exception:
                pass

        if not usage_metrics_processed:
            return {"data": []}

        start_date = f"toDate('{_from.strftime('%Y-%m-%d')}')"
        end_date = f"toDate('{to.strftime('%Y-%m-%d')}')"
        date_filter = f"(date >= {start_date} AND date <= {end_date})"

        sql = f"""
            SELECT array_days AS day, array_cumulative_processed_bytes AS total
            FROM (
                SELECT
                    groupArray(date) as array_days,
                    groupArrayMovingSum(processed_bytes) as array_cumulative_processed_bytes
                FROM (
                    SELECT
                        date,
                        sum(read_bytes + written_bytes) processed_bytes
                    FROM {pu.database}.{usage_metrics_processed.id}
                    WHERE {date_filter}
                      AND database = '{workspace.database}'
                    GROUP BY date
                    ORDER BY date ASC
                )
            )
            ARRAY JOIN array_days, array_cumulative_processed_bytes
            FORMAT JSON
        """

        try:
            _, result = await client.query(sql)
        except CHException as e:
            logging.exception(
                f"Failed to get stats for get_processed_bytes_used_along_the_month. Workspace: {workspace.id}. Error: {e}"
            )
            raise PlansException(PlansStatisticsErrors.STATS_QUERY)

        return {"data": json.loads(result).get("data", [])}

    @classmethod
    async def get_cumulative_processed_bytes_along_the_month(cls, workspace: User, _from: datetime, to: datetime):
        pu = public.get_public_user()
        client = HTTPClient(pu.database_server)

        pipe_stats = cls._try_get_datasource(pu, "pipe_stats")
        usage_metrics_processed = cls._try_get_datasource(pu, "distributed_billing_processed_usage_log")
        bi_stats = cls._try_get_datasource(pu, "distributed_bi_connector_stats")

        start_date = f"toDate('{_from.strftime('%Y-%m-%d')}')"
        end_date = f"toDate('{to.strftime('%Y-%m-%d')}')"
        date_filter = f"(date >= {start_date} AND date <= {end_date})"

        inner_tables_list: List[str] = []

        if pipe_stats:
            inner_tables_list.append(
                f"""
                        (SELECT
                            date AS day,
                            sumIf(read_bytes_sum, pipe_id != 'query_api') AS api_endpoints,
                            sumIf(read_bytes_sum, pipe_id == 'query_api') AS sql,
                            0 AS bi_connector,
                            0 AS read_and_write
                        FROM {pu.database}.{pipe_stats.id}
                        WHERE
                            {date_filter}
                            AND user_id = '{workspace.id}'
                            AND billable = 1
                        GROUP BY day
                        ORDER BY day ASC)"""
            )

        if usage_metrics_processed:
            inner_tables_list.append(
                f"""
                        (SELECT
                            date AS day,
                            0 AS api_endpoints,
                            0 AS sql,
                            0 AS bi_connector,
                            sum(read_bytes + written_bytes) AS read_and_write
                        FROM {pu.database}.{usage_metrics_processed.id}
                        WHERE
                            {date_filter}
                            AND database = '{workspace.database}'
                        GROUP BY day
                        ORDER BY day ASC)"""
            )

        if bi_stats:
            inner_tables_list.append(
                f"""
                        (SELECT
                            date AS day,
                            0 AS api_endpoints,
                            0 AS sql,
                            sum(read_bytes_sum) AS bi_connector,
                            0 AS read_and_write
                        FROM {pu.database}.{bi_stats.id}
                        WHERE
                            {date_filter}
                            AND database = '{workspace.database}'
                        GROUP BY day
                        ORDER BY day ASC)"""
            )

        assert len(inner_tables_list) > 0
        inner_tables = " UNION ALL ".join(inner_tables_list)

        sql = f"""
            SELECT day,
                   api_endpoints,
                   sql,
                   bi_connector,
                   (read_and_write_total - api_endpoints - sql - bi_connector) AS read_and_write,
                   api_endpoints + sql + bi_connector + read_and_write AS total
            FROM (
                SELECT
                    groupArray(day) as day,
                    groupArrayMovingSum(api_endpoints) as api_endpoints,
                    groupArrayMovingSum(sql) as sql,
                    groupArrayMovingSum(bi_connector) as bi_connector,
                    groupArrayMovingSum(read_and_write) as read_and_write_total
                FROM (
                    SELECT *
                    FROM (
                        SELECT arrayJoin(arrayMap(x -> toDate(x), range(toUInt32({start_date}), toUInt32({end_date} + INTERVAL 1 DAY), 1))) day
                    )
                    LEFT JOIN (
                        SELECT day,
                               sum(api_endpoints) as api_endpoints,
                               sum(sql) as sql,
                               sum(bi_connector) as bi_connector,
                               sum(read_and_write) as read_and_write
                        FROM ({inner_tables})
                        GROUP BY day
                    ) USING day
                )
            ) ARRAY JOIN day, api_endpoints, sql, bi_connector, read_and_write_total
            ORDER BY day ASC
            FORMAT JSON
        """

        try:
            _, result = await client.query(sql)
        except CHException as e:
            logging.exception(
                f"Failed to get stats for get_cumulative_processed_bytes_along_the_month. Workspace: {workspace.id}. Error: {e}"
            )
            raise PlansException(PlansStatisticsErrors.STATS_QUERY)

        return {"data": json.loads(result).get("data", [])}

    @classmethod
    async def get_date_range(cls, workspace: User):
        pu = public.get_public_user()
        client = HTTPClient(pu.database_server)
        usage_metrics_processed = pu.get_datasource("usage_metrics_processed")
        usage_metrics_storage = pu.get_datasource("usage_metrics_storage__v2")

        if not usage_metrics_processed or not usage_metrics_storage:
            return {"data": []}

        sql = f"""
            SELECT
                toMonth(max) as max_month,
                toMonth(min) as min_month,
                toYear(max) as max_year,
                toYear(min) as min_year

            FROM (
                SELECT
                    max(max_date) as max,
                    min(min_date) as min
                FROM (
                    SELECT 'processed' as type, maxOrNull(date) as max_date, minOrNull(date) as min_date
                    FROM {pu.database}.{usage_metrics_processed.id}
                    WHERE database = '{workspace.database}'

                    UNION ALL

                    SELECT 'storage' as type, maxOrNull(toDate(timestamp)) as max_date, minOrNull(toDate(timestamp)) as min_date
                    FROM {pu.database}.{usage_metrics_storage.id}
                    WHERE user_id = '{workspace.id}'
                )
            )
            WHERE min_year IS NOT NULL and max_year IS NOT NULL
            FORMAT JSON
        """

        try:
            _, result = await client.query(sql)
        except CHException as e:
            logging.exception(f"Failed to get stats for get_date_range. Workspace: {workspace.id}. Error: {e}")
            raise PlansException(PlansStatisticsErrors.STATS_QUERY)

        return {"data": json.loads(result).get("data", [])}

    @classmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def add_free_package(cls, workspace: User, processed_gb_included: float, stored_gb_included: float):
        with User.transaction(workspace.id) as workspace:
            workspace.billing_details["packages"].append(
                {
                    "id": str(uuid.uuid4()),
                    "type": PackageType.FREE.value,
                    "processed_gb_included": processed_gb_included,
                    "stored_gb_included": stored_gb_included,
                }
            )

    @classmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def add_committed_package(
        cls,
        workspace: User,
        processed_gb_included: float,
        stored_gb_included: float,
        price_per_processed_gb: float,
        price_per_stored_gb: float,
    ):
        with User.transaction(workspace.id) as workspace:
            workspace.billing_details["packages"].append(
                {
                    "id": str(uuid.uuid4()),
                    "type": PackageType.COMMITTED.value,
                    "processed_gb_included": processed_gb_included,
                    "stored_gb_included": stored_gb_included,
                    "price_per_processed_gb": price_per_processed_gb,
                    "price_per_stored_gb": price_per_stored_gb,
                }
            )

    @classmethod
    async def update_product_prices(cls, product_id: str, price_per_stored_gb: str, price_per_processed_gb: str):
        logging.info(
            f"Updating product prices for product id {product_id}: storage {price_per_stored_gb}, processed: {price_per_processed_gb}"
        )

        try:
            product = Product.retrieve(product_id)

            plan_type = product.get("metadata", {}).get("plan_type", BillingPlans.CUSTOM)
            current_prices = Price.list(product=product_id, active=True, limit=PRICES_LIMIT).get("data")

            new_storage_price = cls._add_new_storage_price(
                plan_type=plan_type, product_id=product_id, price=float(price_per_stored_gb)
            )

            new_processed_price = cls._add_new_processed_price(
                plan_type=plan_type, product_id=product_id, price=float(price_per_processed_gb)
            )

            await cls.replace_product_prices(
                prices=[
                    {"price_id": new_storage_price.id, "plan_type": plan_type, "billing_type": BillingTypes.STORAGE},
                    {
                        "price_id": new_processed_price.id,
                        "plan_type": plan_type,
                        "billing_type": BillingTypes.PROCESSED,
                    },
                ],
                product_id=product_id,
            )

            cls.deactivate_prices(prices=current_prices)
        except Exception as e:
            logging.exception(e)
            raise Exception(f"Stripe: could not update prices for product {product_id}, error {e}")

    @classmethod
    def _get_datetime_from_stripe_timestamp(cls, timestamp: float) -> datetime:
        # This is used only for PRO workspaces, which use ES Stripe account set to Europe/Madrid
        return datetime.fromtimestamp(timestamp, tz=ZoneInfo(key="Europe/Madrid"))

    @classmethod
    def _billing_datetime(cls, current_datetime: datetime, subscription: Subscription) -> datetime:
        current_date = current_datetime.date()
        if cls._get_datetime_from_stripe_timestamp(subscription["created"]).date() == current_date:
            return cls._get_datetime_from_stripe_timestamp(subscription["created"] + 1)

        if cls._get_datetime_from_stripe_timestamp(subscription["current_period_start"]).date() == current_date:
            return cls._get_datetime_from_stripe_timestamp(subscription["current_period_start"] + 1)

        return datetime.combine(current_datetime, datetime.min.time(), tzinfo=ZoneInfo(key="Europe/Madrid"))

    @classmethod
    def _today_billing_datetime(cls, subscription: Subscription) -> datetime:
        # This is used only for PRO workspaces, which use ES Stripe account set to Europe/Madrid
        today_datetime = datetime.now(ZoneInfo("Europe/Madrid"))
        return cls._billing_datetime(today_datetime, subscription)

    @classmethod
    def _yesterday_billing_datetime(cls, subscription: Subscription) -> Optional[datetime]:
        # This is used only for PRO workspaces, which use ES Stripe account set to Europe/Madrid
        today_datetime = datetime.now(ZoneInfo("Europe/Madrid"))
        if (
            cls._get_datetime_from_stripe_timestamp(subscription["current_period_start"]).date()
            == today_datetime.date()
        ):
            return None
        yesterday = today_datetime - timedelta(days=1)
        return cls._billing_datetime(yesterday, subscription)

    @classmethod
    def _track_storage(
        cls, workspace: User, storage_subscription_item_id: int, subscription: Subscription
    ) -> List[Dict]:
        today_billing_datetime = cls._today_billing_datetime(subscription)
        quantity_today = PlansService.get_storage_bytes_used_total_date_sync(
            workspace=workspace,
            year=str(today_billing_datetime.year),
            month=str(today_billing_datetime.month),
            day=str(today_billing_datetime.day),
        )
        usage_record_today = SubscriptionItem.create_usage_record(
            id=storage_subscription_item_id,
            quantity=PlansService._bytes_to_gb(quantity_today),
            action="set",
            timestamp=today_billing_datetime,
        )
        return [usage_record_today]

    @classmethod
    def _track_processed(
        cls, workspace: User, processed_subscription_id: int, subscription: Subscription, metrics_cluster: Optional[str]
    ) -> List[Dict]:
        today_billing_datetime = cls._today_billing_datetime(subscription)
        quantity_today = PlansService.get_processed_bytes_used_total_date_sync(
            workspace=workspace,
            metrics_cluster=metrics_cluster,
            year=str(today_billing_datetime.year),
            month=str(today_billing_datetime.month),
            day=str(today_billing_datetime.day),
        )

        usage_record_today = SubscriptionItem.create_usage_record(
            id=processed_subscription_id,
            quantity=PlansService._bytes_to_gb(quantity_today),
            action="set",
            timestamp=today_billing_datetime,
        )
        usage_records = [usage_record_today]
        yesterday_billing_datetime = cls._yesterday_billing_datetime(subscription)
        if yesterday_billing_datetime is not None:
            quantity_yesterday = PlansService.get_processed_bytes_used_total_date_sync(
                workspace=workspace,
                metrics_cluster=metrics_cluster,
                year=str(yesterday_billing_datetime.year),
                month=str(yesterday_billing_datetime.month),
                day=str(yesterday_billing_datetime.day),
            )
            usage_record_yesterday = SubscriptionItem.create_usage_record(
                id=processed_subscription_id,
                quantity=PlansService._bytes_to_gb(quantity_yesterday),
                action="set",
                timestamp=yesterday_billing_datetime,
            )
            usage_records.append(usage_record_yesterday)
        return usage_records

    @classmethod
    def _call_get_by_pipe_endpoint(
        cls, api_host: Optional[str], pipe_endpoint_name: str, **params: Any
    ) -> Dict[str, Any]:
        result = async_to_sync(get_by_pipe_endpoint)(api_host, pipe_endpoint_name, **params)
        if not result:
            logging.exception(
                f"track_usage_records failed while calling get_by_pipe_id for {api_host}, {pipe_endpoint_name}, {params}"
            )
            return {}
        return result

    @classmethod
    def _track_data_transfer(
        cls, workspace: User, data_transfer_subscription_id: int, subscription: Subscription, api_host: str, kind: str
    ) -> List[Dict]:
        today_billing_datetime = cls._today_billing_datetime(subscription)
        params = {"workspace": workspace.id, "date": today_billing_datetime.strftime("%Y-%m-%d"), "kind": kind}
        data_transfer = cls._call_get_by_pipe_endpoint(api_host, "data_transfer_per_day", **params)
        data_transfer_values = data_transfer.get("data", [])
        usage_record_today = SubscriptionItem.create_usage_record(
            id=data_transfer_subscription_id,
            quantity=PlansService._bytes_to_gb(data_transfer_values[0]["bytes"] if data_transfer_values else 0),
            action="set",
            timestamp=today_billing_datetime,
        )
        usage_records = [usage_record_today]
        yesterday_billing_datetime = cls._yesterday_billing_datetime(subscription)
        if yesterday_billing_datetime is not None:
            params = {"workspace": workspace.id, "date": yesterday_billing_datetime.strftime("%Y-%m-%d"), "kind": kind}
            data_transfer_yesterday = cls._call_get_by_pipe_endpoint(api_host, "data_transfer_per_day", **params)
            data_transfer_yesterday_values = data_transfer_yesterday.get("data", [])
            usage_record_yesterday = SubscriptionItem.create_usage_record(
                id=data_transfer_subscription_id,
                quantity=PlansService._bytes_to_gb(
                    data_transfer_yesterday_values[0]["bytes"] if data_transfer_yesterday_values else 0
                ),
                action="set",
                timestamp=yesterday_billing_datetime,
            )
            usage_records.append(usage_record_yesterday)
        return usage_records

    @classmethod
    def track_usage_records(
        cls,
        workspace: User,
        subscription: Subscription,
        metrics_cluster: Optional[str],
        api_host: str,
    ) -> Optional[List[Dict[str, Any]]]:
        stripe_customer_id = workspace.stripe.get("customer_id")

        if not stripe_customer_id:
            return None

        usage_records = []
        price_items = PlansService.get_subscription_items(subscription)
        for item in price_items:
            billing_type = item.get("billing_type", None)

            if not billing_type:
                continue

            if billing_type == BillingTypes.STORAGE:
                usage_records += cls._track_storage(workspace, cast(int, item.get("id")), subscription)

            elif billing_type == BillingTypes.PROCESSED:
                usage_records += cls._track_processed(
                    workspace, cast(int, item.get("id")), subscription, metrics_cluster
                )
            elif billing_type == BillingTypes.TRANSFERRED_INTER:
                usage_records += cls._track_data_transfer(
                    workspace, cast(int, item.get("id")), subscription, api_host, "inter"
                )
            elif billing_type == BillingTypes.TRANSFERRED_INTRA:
                usage_records += cls._track_data_transfer(
                    workspace, cast(int, item.get("id")), subscription, api_host, "intra"
                )

        return usage_records

    @classmethod
    def is_subscription_usage_trackable(cls, subscription: Subscription) -> bool:
        contains_price_billable = any(
            [
                item.get("billing_type") in [BillingTypes.STORAGE, BillingTypes.PROCESSED]  # TODO add new concepts
                for item in cls.get_subscription_items(subscription)
            ]
        )
        return contains_price_billable

    @classmethod
    def _add_new_processed_price(cls, plan_type: str, product_id: str, price: float) -> Price:
        new_price = Price.create(
            billing_scheme="per_unit",
            currency="usd",
            nickname=BillingTypes.PROCESSED,
            metadata={"billing_type": BillingTypes.PROCESSED, "plan_type": plan_type},
            product=product_id,
            recurring={"aggregate_usage": "sum", "interval": "month", "interval_count": 1, "usage_type": "metered"},
            unit_amount_decimal=str(round(price * 100, 5)),
        )
        logging.info(f"Added new processed price for plan {plan_type}, product {product_id} with id {new_price['id']}")

        return new_price

    @classmethod
    def _add_new_storage_price(cls, plan_type: str, product_id: str, price: float) -> Price:
        new_price = Price.create(
            billing_scheme="per_unit",
            currency="usd",
            nickname=BillingTypes.STORAGE,
            metadata={"billing_type": BillingTypes.STORAGE, "plan_type": plan_type},
            product=product_id,
            recurring={
                "aggregate_usage": "last_during_period",
                "interval": "month",
                "interval_count": 1,
                "usage_type": "metered",
            },
            unit_amount_decimal=str(round(price * 100, 5)),
        )
        logging.info(f"Added new storage price for plan {plan_type}, product {product_id} with id {new_price['id']}")

        return new_price

    @classmethod
    def create_new_pro_plan(
        cls,
        price_per_stored_gb: str,
        price_per_processed_gb: str,
        force: bool = False,
        name_override: Optional[str] = None,
    ) -> Product:
        if cls.PRO is not None and not force:
            raise Exception("Pro plan is already configured. Are you sure you want to recreate the Pro plan?")

        name = name_override if name_override is not None else "Professional Plan"

        new_product = Product.create(
            name=name,
            description="Your pay as you grow plan",
            metadata={
                "plan_type": BillingPlans.PRO,
            },
        )
        logging.info(f"New Pro plan created with id {new_product.id}")

        cls._add_new_storage_price(
            plan_type=BillingPlans.PRO, product_id=new_product.id, price=float(price_per_stored_gb)
        )

        cls._add_new_processed_price(
            plan_type=BillingPlans.PRO, product_id=new_product.id, price=float(price_per_processed_gb)
        )

        return Product.retrieve(new_product.id)

    @classmethod
    def add_sink_prices(cls, dry_run: bool = True) -> None:
        pro_plan_product = Product.retrieve(cls.PRO)
        if not pro_plan_product:
            raise Exception(f"{'[DRY RUN] ' if dry_run else ''}Product with id {cls.PRO} not found.")

        pro_plan_prices = stripe.Price.list(product=cls.PRO, active=True)

        existing_inter_price = next(
            filter(
                lambda price: price["metadata"].get("billing_type", None) == BillingTypes.TRANSFERRED_INTER,
                pro_plan_prices,
            ),
            None,
        )
        existing_intra_price = next(
            filter(
                lambda price: price["metadata"].get("billing_type", None) == BillingTypes.TRANSFERRED_INTRA,
                pro_plan_prices,
            ),
            None,
        )

        if existing_inter_price:
            logging.info(f"{'[DRY RUN] ' if dry_run else ''}Transferred Inter already created.")
        else:
            new_inter_price_id = None
            if not dry_run:
                new_inter_price = Price.create(
                    billing_scheme="per_unit",
                    currency="usd",
                    nickname=BillingTypes.TRANSFERRED_INTER,
                    metadata={"billing_type": BillingTypes.TRANSFERRED_INTER, "plan_type": BillingPlans.PRO},
                    product=cls.PRO,
                    recurring={
                        "aggregate_usage": "sum",
                        "interval": "month",
                        "interval_count": 1,
                        "usage_type": "metered",
                    },
                    unit_amount_decimal=str(round(0.10 * 100, 5)),
                )
                new_inter_price_id = new_inter_price["id"]
            logging.info(
                f"{'[DRY RUN] ' if dry_run else ''}Added new transferred intra price for plan {BillingPlans.PRO}, product {cls.PRO} with id {new_inter_price_id}"
            )

        if existing_intra_price:
            logging.info(f"{'[DRY RUN] ' if dry_run else ''}Transferred Intra already created.")
        else:
            new_intra_price_id = None
            if not dry_run:
                new_intra_price = Price.create(
                    billing_scheme="per_unit",
                    currency="usd",
                    nickname=BillingTypes.TRANSFERRED_INTRA,
                    metadata={"billing_type": BillingTypes.TRANSFERRED_INTRA, "plan_type": BillingPlans.PRO},
                    product=cls.PRO,
                    recurring={
                        "aggregate_usage": "sum",
                        "interval": "month",
                        "interval_count": 1,
                        "usage_type": "metered",
                    },
                    unit_amount_decimal=str(round(0.01 * 100, 5)),
                )
                new_intra_price_id = new_intra_price["id"]
            logging.info(
                f"{'[DRY RUN] ' if dry_run else ''}Added new transferred intra price for plan {BillingPlans.PRO}, product {cls.PRO} with id {new_intra_price_id}"
            )

    @classmethod
    def _update_subscription_item_with_storage_price(
        cls, subscription: Subscription, subscription_item: str, price_id: str
    ) -> None:
        stripe.Subscription.modify(
            subscription.id,
            proration_behavior="none",  # restarts the subscription item with the new price.
            items=[{"id": subscription_item, "price": price_id}],
        )

    @classmethod
    def _update_subscription_item_with_processed_price(
        cls, subscription: Subscription, subscription_item: str, price_id: str
    ) -> None:
        stripe.Subscription.modify(
            subscription.id,
            proration_behavior="create_prorations",  # 'create_prorations' looks like would just add the actual consumption to the invoice.
            items=[{"id": subscription_item, "price": price_id}],
        )

    @classmethod
    async def replace_product_prices(cls, prices: List[Dict[str, Any]], product_id: str) -> None:
        subs = stripe.Subscription.list()
        for sub in subs.auto_paging_iter():
            subscription_items = sub["items"]["data"]

            for item in subscription_items:
                for new_price in prices:
                    if (
                        item["price"]["product"] == product_id
                        and item["price"]["metadata"].get("billing_type") == new_price["billing_type"]
                        and item["price"]["metadata"].get("plan_type") == new_price["plan_type"]
                    ):
                        logging.info(
                            f"Replacing price for subscription '{sub['id']}', subscription item '{item['id']}' will have a nive price with id '{new_price['price_id']}'"
                        )
                        if item["price"]["metadata"]["billing_type"] == BillingTypes.STORAGE:
                            cls._update_subscription_item_with_storage_price(sub, item["id"], new_price["price_id"])
                        elif item["price"]["metadata"]["billing_type"] == BillingTypes.PROCESSED:
                            cls._update_subscription_item_with_processed_price(sub, item["id"], new_price["price_id"])
                        else:
                            raise Exception(
                                f"Price can't be replaced in the product because the billing type '{item['price']['metadata']['billing_type']}' is not configured"
                            )

    @classmethod
    def list_product_prices(cls, limit: int = 100) -> List[Dict[str, Any]]:
        all_products = Product.list(active=True, limit=limit).get("data", {})
        all_products_with_prices = []

        for product in all_products:
            plan_type = product.get("metadata", {}).get("plan_type", None)
            if plan_type is None:
                continue

            price_list = Price.list(product=product.id, active=True, limit=limit)

            prices = [cls.get_price_details(price) for price in price_list.get("data")]

            if len(prices):
                product.update(
                    {
                        "product_url": f"{StripeSettings.PRODUCT_TEST_URL}/{product.get('id', '')}",
                        "prices": prices,
                        "plan_type": plan_type,
                    }
                )
                all_products_with_prices.append(product)

        all_products_with_prices.sort(key=lambda product: 0 if product["plan_type"] == BillingPlans.CUSTOM else 1)
        return all_products_with_prices

    @classmethod
    def list_active_subscriptions(cls) -> Iterator[Any]:
        return stripe.Subscription.list().auto_paging_iter()

    @staticmethod
    def get_price_details(price: Dict[str, Any]) -> Dict[str, Any]:
        price_unit_amount_decimal = price.get("unit_amount_decimal", None)
        price_unit_amount_decimal = float(price_unit_amount_decimal) / 100 if price_unit_amount_decimal else None

        return {
            "price_id": price.get("id", None),
            "price_currency": price.get("currency", None),
            "price_unit_amount_decimal": price_unit_amount_decimal,
            "billing_type": price.get("metadata", {}).get("billing_type", None),
            "product_id": price.get("product"),
            "plan_type": price.get("metadata", {}).get("plan_type", None),
        }

    @staticmethod
    def get_subscription_items(stripe_subscription: Dict[str, Any]) -> List[Dict[str, Any]]:
        items = stripe_subscription.get("items", {}).get("data", [])
        return [
            {
                "id": item.get("id", None),
                "price_id": item.get("price", {}).get("id", None),
                "billing_type": item.get("price", {}).get("metadata", {}).get("billing_type", None),
            }
            for item in items
            if item.get("price", False).get("active", False)
        ]

    @classmethod
    def deactivate_prices(cls, prices: List[Dict[str, Any]]) -> None:
        for price in prices:
            logging.info(f"Deactivating price {price['id']}")
            try:
                Price.modify(price.get("id"), active=False)
            except Exception as e:
                logging.exception(f"Stripe: product prices could not be deactivated ({price}), error {e}")

    @staticmethod
    def get_card_info_dict(card: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "brand": card.get("brand", ""),
            "country": card.get("country", ""),
            "exp_month": card.get("exp_month", None),
            "exp_year": card.get("exp_year", None),
            "last4": card.get("last4", ""),
        }

    @staticmethod
    def get_charge_info(charge: Any) -> Dict[str, Any]:
        created = datetime.fromtimestamp(charge.created).strftime("%d/%m/%Y")
        return {
            "status": charge.status,
            "card": PlansService.get_card_info_dict(charge.payment_method_details.card),
            "amount": charge.amount,
            "created": created,
        }

    @classmethod
    async def cancel_subscription(cls, workspace: User) -> None:
        subscription_id = workspace.stripe.get("subscription_id", None)
        if subscription_id:
            stripe.Subscription.delete(subscription_id, invoice_now=True)
            await Users.remove_stripe_subscription(workspace)

    @staticmethod
    def get_invoice_info(invoice: Any) -> Dict[str, Any]:
        created = datetime.fromtimestamp(invoice.created).strftime("%d/%m/%Y")
        return {"status": invoice.status, "total": invoice.total, "created": created}

    @classmethod
    def track_build_plan_limits(cls, api_host: str, metrics_cluster: Optional[str]) -> None:
        BuildPlanTracker.track_limits(api_host, metrics_cluster)


@dataclass
class StatsLimit:
    storage: Optional[float] = None
    requests: Optional[int] = None


class BuildPlanTracker:
    MAX_API_REQUESTS_PER_DAY_LIMIT = DEFAULT_PLAN_CONFIG[PlanConfigConcepts.DEV_MAX_API_REQUESTS_PER_DAY]
    MAX_STORAGE_USED_LIMIT = DEFAULT_PLAN_CONFIG[PlanConfigConcepts.DEV_MAX_GB_STORAGE_USED]
    LIMIT_THRESHOLD = 0.75

    @classmethod
    def workspaces_reaching_or_exceeding_storage_limits(cls, api_host: str) -> List[Dict[str, Any]]:
        pu = public.get_public_user()
        usage_metrics_storage = pu.get_datasource("usage_metrics_storage__v2")
        workspaces_all = pu.get_datasource("workspaces_all")

        # The table might exist in redis but not yet in CH (because the init_tables is in progress)
        if not workspaces_all or not usage_metrics_storage:
            return []

        params = {
            "threshold_limit": cls.LIMIT_THRESHOLD,
            "max_storage_limit": int(PlansService._gb_to_bytes(cls.MAX_STORAGE_USED_LIMIT)),
        }
        try:
            result = async_to_sync(get_by_pipe_endpoint)(api_host, "build_plan_tracker_storage_limits", **params)
        except Exception as e:
            logging.exception(f"Failed to get stats for workspaces_reaching_or_exceeding_storage_limits. Error: {e}")
            raise PlansException()

        if result is None:
            return []
        return result.get("data", [])

    @classmethod
    def workspaces_reaching_or_exceeding_requests_limits(cls, api_host: str) -> List[Dict[str, Any]]:
        pu = public.get_public_user()

        pipe_stats = pu.get_datasource("pipe_stats")
        if not pipe_stats:
            return []

        workspaces_all = pu.get_datasource("workspaces_all")
        if not workspaces_all:
            return []

        params = {
            "threshold_limit": cls.LIMIT_THRESHOLD,
            "max_requests_per_day_limit": cls.MAX_API_REQUESTS_PER_DAY_LIMIT,
        }
        try:
            result = async_to_sync(get_by_pipe_endpoint)(api_host, "build_plan_tracker_requests_limits", **params)

        except Exception as e:
            logging.exception(
                f"Failed to get stats for workspaces_reaching_or_exceeding_api_requests_limits. Error: {e}"
            )
            raise PlansException()

        if result is None:
            return []
        return result.get("data", [])

    @classmethod
    async def send_limits_email(
        cls,
        workspace_id: str,
        stats_limits: StatsLimit,
        processed_price: float,
        storage_price: float,
        exceeded: bool,
        processed: int,
    ) -> None:
        await Users.notify_build_plan_limits(
            workspace_id,
            cls.MAX_API_REQUESTS_PER_DAY_LIMIT,
            cls.MAX_STORAGE_USED_LIMIT,
            processed_price,
            storage_price,
            exceeded,
            stats_limits.requests,
            stats_limits.storage,
            processed,
        )

    @classmethod
    def workspace_limits_candidates(cls, api_host: str) -> Dict[str, StatsLimit]:
        workspace_candidates: Dict[str, StatsLimit] = defaultdict(lambda: StatsLimit())
        for workspace_storage in cls.workspaces_reaching_or_exceeding_storage_limits(api_host):
            workspace_candidates[workspace_storage["workspace_id"]].storage = PlansService._bytes_to_gb(
                workspace_storage["total_bytes"]
            )

        for workspace_requests in cls.workspaces_reaching_or_exceeding_requests_limits(api_host):
            workspace_candidates[workspace_requests["workspace_id"]].requests = workspace_requests["api_request_done"]

        return workspace_candidates

    @classmethod
    def track_limits(cls, api_host: str, metrics_cluster: Optional[str] = None) -> None:
        processed_price, storage_price = PlansService.get_pro_plan_prices()
        if not processed_price or not storage_price:
            logging.exception("Pro price plans can't be found. Emails are not going to contain the price values.")
            processed_price = cast(float, processed_price)
            storage_price = cast(float, storage_price)

        for workspace_id, stats_limits in cls.workspace_limits_candidates(api_host).items():
            exceeded = False
            if (stats_limits.storage is not None and stats_limits.storage > cls.MAX_STORAGE_USED_LIMIT) or (
                stats_limits.requests is not None and stats_limits.requests > cls.MAX_API_REQUESTS_PER_DAY_LIMIT
            ):
                exceeded = True

            workspace: Optional[User] = User.get_by_id(workspace_id)
            if not workspace:
                logging.exception(f"Inconsistency: workspace {workspace_id} not found for limit tracking.")
                continue

            processed_bytes = asyncio.run(
                PlansService.get_processed_bytes_used_total_month(workspace=workspace, metrics_cluster=metrics_cluster)
            )
            processed = PlansService._bytes_to_gb(processed_bytes)
            asyncio.run(
                cls.send_limits_email(workspace_id, stats_limits, processed_price, storage_price, exceeded, processed)
            )
