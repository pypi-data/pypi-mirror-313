from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal, Optional

import orb
from orb.pagination import AsyncPage
from orb.types.customer import Customer
from orb.types.customer_create_params import BillingAddress
from orb.types.invoice_fetch_upcoming_response import InvoiceFetchUpcomingResponse
from orb.types.plan import Plan
from orb.types.price import MatrixPrice, TieredPrice, UnitPrice
from orb.types.subscription import Subscription
from orb.types.subscription_fetch_costs_response import SubscriptionFetchCostsResponse
from orb.types.subscription_fetch_schedule_response import SubscriptionFetchScheduleResponse

from tinybird.organization.organization import Organization


class OrbAPIException(Exception):
    pass


class OrbCustomerNotFound(Exception):
    pass


class OrbSubscriptionNotFound(Exception):
    pass


@dataclass
class OrganizationOrbSubscription:
    id: str
    commitment_start_date: datetime
    commitment_end_date: Optional[datetime]
    customer_portal: Optional[str]
    plan_id: str
    current_billing_period_start_date: Optional[datetime]
    current_billing_period_end_date: Optional[datetime]

    @classmethod
    def from_subscription(cls, subscription: Subscription) -> OrganizationOrbSubscription:
        return OrganizationOrbSubscription(
            id=subscription.id,
            commitment_start_date=subscription.start_date,
            commitment_end_date=subscription.end_date,
            customer_portal=subscription.customer.portal_url,
            plan_id=subscription.plan.id,
            current_billing_period_start_date=subscription.current_billing_period_start_date,
            current_billing_period_end_date=subscription.current_billing_period_end_date,
        )


@dataclass
class OrganizationCreditBalance:
    total_credits: float
    current_balance: float
    subscription: OrganizationOrbSubscription


@dataclass
class OrganizationInvoice:
    id: str
    status: str
    total: str
    amount_due: str
    subtotal: str
    currency: str
    issued_at: Optional[datetime]
    due_date: datetime
    invoice_date: datetime
    scheduled_issue_at: Optional[datetime]
    invoice_number: str
    hosted_invoice_url: Optional[str]
    invoice_pdf: Optional[str]


@dataclass
class LineItem:
    name: str
    amount: str
    quantity: float


@dataclass
class UpcomingInvoiceUsage:
    line_items: List[LineItem]

    @staticmethod
    def from_upcoming_invoice(invoice: InvoiceFetchUpcomingResponse) -> UpcomingInvoiceUsage:
        line_items = []
        for line_item in invoice.line_items:
            line_items.append(LineItem(amount=line_item.amount, name=line_item.name, quantity=line_item.quantity))
        return UpcomingInvoiceUsage(line_items=line_items)


@dataclass
class SharedInfraBillingPlan:
    plan_id: str
    t_shirt_size: str
    number_of_cpus: int
    number_of_max_qps: int
    number_of_max_threads: int
    number_of_max_copies: int
    number_of_max_sinks: int
    fixed_monthly_fee: float
    fixed_monthly_fee_yearly_commitment: float
    included_storage_in_gb: int
    cost_of_additional_gb_storage: Optional[float]
    cost_of_egress_gb_intra: float
    cost_of_egress_gb_inter: float

    @staticmethod
    def from_plan(plan: Plan) -> SharedInfraBillingPlan:
        fixed_monthly_fee = None
        included_storage = None
        cost_additional_storage = None
        cost_egress_intra = None
        cost_egress_inter = None

        for price in plan.prices:
            # CPUs/time
            if isinstance(price, UnitPrice) and price.price_type == "fixed_price":
                fixed_monthly_fee = float(price.unit_config.unit_amount)

            # Storage GB
            elif isinstance(price, TieredPrice) and price.price_type == "usage_price":
                for tier in price.tiered_config.tiers:
                    if tier.first_unit == 0 and float(tier.unit_amount) == 0 and tier.last_unit is not None:
                        included_storage = int(tier.last_unit)
                    else:
                        cost_additional_storage = float(tier.unit_amount)

            # Data Transfer GB
            elif isinstance(price, MatrixPrice) and price.price_type == "usage_price":
                for values in price.matrix_config.matrix_values:
                    if "intra" in values.dimension_values:
                        cost_egress_intra = float(values.unit_amount)
                    elif "inter" in values.dimension_values:
                        cost_egress_inter = float(values.unit_amount)

        if fixed_monthly_fee is None:
            raise OrbAPIException(f"No CPUs/time fee found for plan {plan.id}")

        if included_storage is None or cost_additional_storage is None:
            raise OrbAPIException(f"No storage fee found for plan {plan.id}")

        if cost_egress_intra is None or cost_egress_inter is None:
            raise OrbAPIException(f"No egress fee found for plan {plan.id}")

        return SharedInfraBillingPlan(
            plan_id=plan.id,
            t_shirt_size=plan.metadata.get("tshirt_size", ""),
            number_of_cpus=int(plan.metadata.get("n_cpus", 0)),
            number_of_max_qps=int(plan.metadata.get("max_qps", 0)),
            number_of_max_threads=int(plan.metadata.get("max_threads", 0)),
            number_of_max_copies=int(plan.metadata.get("max_copies", 0)),
            number_of_max_sinks=int(plan.metadata.get("max_sinks", 0)),
            fixed_monthly_fee=fixed_monthly_fee,
            fixed_monthly_fee_yearly_commitment=float(plan.metadata.get("fixed_monthly_fee_yearly_commitment", 0)),
            included_storage_in_gb=included_storage,
            cost_of_additional_gb_storage=cost_additional_storage,
            cost_of_egress_gb_intra=cost_egress_intra,
            cost_of_egress_gb_inter=cost_egress_inter,
        )


@dataclass
class ScheduledSubscriptionChange:
    plan: SharedInfraBillingPlan
    start_date: datetime


class PlanKind(Enum):
    SHARED = "shared"
    DEDICATED = "dedicated"


@dataclass
class CostEntry:
    amount: str
    timeframe_end: datetime
    timeframe_start: datetime
    currency: str


@dataclass
class Cost:
    name: str
    costs: List[CostEntry]


@dataclass
class SubscriptionCosts:
    data: Dict[str, Cost]

    @staticmethod
    def from_costs(consts_response: SubscriptionFetchCostsResponse) -> SubscriptionCosts:
        mapped_costs: Dict[str, Cost] = {}

        for data in consts_response.data:
            timeframe_start = data.timeframe_start

            for per_price_cost in data.per_price_costs:
                price_name = per_price_cost.price.name

                if price_name not in mapped_costs:
                    mapped_costs[price_name] = Cost(name=price_name, costs=[])

                cost_entry = CostEntry(
                    amount=per_price_cost.total,
                    timeframe_start=timeframe_start,
                    timeframe_end=data.timeframe_end,
                    currency=per_price_cost.price.currency,
                )
                mapped_costs[price_name].costs.append(cost_entry)

        return SubscriptionCosts(data=mapped_costs)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "data": {
                name: {
                    "name": cost.name,
                    "costs": [
                        {
                            "amount": entry.amount,
                            "timeframe_start": entry.timeframe_start.isoformat(),
                            "timeframe_end": entry.timeframe_end.isoformat(),
                            "currency": entry.currency,
                        }
                        for entry in cost.costs
                    ],
                }
                for name, cost in self.data.items()
            }
        }


def orb_exception_handler(func):
    async def inner_function(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except orb.NotFoundError as e:
            err_msg = f"Organization not found as Customer in Orb: {e.message}"
            logging.warning(err_msg)
            raise OrbCustomerNotFound(err_msg)
        except orb.APIStatusError as e:
            err_msg = f"Orb API error with status {e.status_code}. Detail: {e.message}"
            logging.warning(err_msg)
            raise OrbAPIException(err_msg)

    return inner_function


class OrbService:
    _settings: Dict[str, Any] = {}
    _client: orb.AsyncOrb
    _billing_region: str

    @classmethod
    def init(cls, settings: Dict[str, Any]) -> None:
        cls._settings = settings

        orb_api_key = settings.get("orb", {}).get("api_key", None)
        orb_webhook_secret = settings.get("orb", {}).get("webhook_secret", None)
        cls._billing_region = f"{settings.get('billing_region_orb', '')}"
        cls._client = orb.AsyncOrb(api_key=orb_api_key, webhook_secret=orb_webhook_secret)

    @classmethod
    @orb_exception_handler
    async def get_subscription(cls, organization: Organization) -> OrganizationOrbSubscription:
        """Returns an active subscription

        If multiple subscriptions are found, the most recently created one is returned, as that's Orb's default ordering
        """
        subscriptions_page: AsyncPage[Subscription] = await cls._client.subscriptions.list(
            external_customer_id=organization.get_orb_external_customer_id(), status="active"
        )

        if len(subscriptions_page.data) == 0:
            err_msg = f"No active subscription found in Orb for organization {organization.id}"
            logging.warning(err_msg)
            raise OrbSubscriptionNotFound(err_msg)

        if len(subscriptions_page.data) > 1:
            logging.warning(f"Multiple active subscriptions found in Orb for {organization}. Using the first one.")

        subscription = subscriptions_page.data[0]  # Orb returns most recently created subscriptions first

        return OrganizationOrbSubscription.from_subscription(subscription)

    @classmethod
    @orb_exception_handler
    async def get_organization_credit_balance(cls, organization: Organization) -> OrganizationCreditBalance:
        subscription_task = cls.get_subscription(organization)
        credits_task = cls._client.customers.credits.list_by_external_id(organization.get_orb_external_customer_id())

        [subscription, credits_paginated_data] = await asyncio.gather(subscription_task, credits_task)

        total_credits = 0.0
        current_balance = 0.0

        async for credit_block in credits_paginated_data:
            if not credit_block.effective_date or credit_block.effective_date < subscription.commitment_start_date:
                continue

            total_credits += credit_block.maximum_initial_balance if credit_block.maximum_initial_balance else 0
            current_balance += credit_block.balance

        return OrganizationCreditBalance(total_credits, current_balance, subscription)

    @classmethod
    @orb_exception_handler
    async def get_organization_invoices(cls, organization: Organization) -> List[OrganizationInvoice]:
        statuses = ["draft", "issued", "paid", "synced"]

        # Orb uses auto-paginating iterators on its list calls, we need to iterate with async for to use them
        invoices_auto_paginated_list = cls._client.invoices.list(
            external_customer_id=organization.get_orb_external_customer_id(),
            status=statuses,  # type: ignore
            limit=500,
        )

        invoices = []
        async for invoice_data in invoices_auto_paginated_list:
            invoice = OrganizationInvoice(
                id=invoice_data.id,
                status=invoice_data.status,
                total=invoice_data.total,
                amount_due=invoice_data.amount_due,
                subtotal=invoice_data.subtotal,
                currency=invoice_data.currency,
                issued_at=invoice_data.issued_at,
                due_date=invoice_data.due_date,
                invoice_date=invoice_data.invoice_date,
                scheduled_issue_at=invoice_data.scheduled_issue_at,
                invoice_number=invoice_data.invoice_number,
                hosted_invoice_url=invoice_data.hosted_invoice_url,
                invoice_pdf=invoice_data.invoice_pdf,
            )
            invoices.append(invoice)

        return invoices

    @classmethod
    @orb_exception_handler
    async def unwrap_webhook(cls, body: str, headers: Dict[str, str]) -> Dict[str, Any]:
        return cls._client.webhooks.unwrap(body, headers)  # type: ignore

    @classmethod
    @orb_exception_handler
    async def create_customer(
        cls, organization: Organization, notification_email: str, address: BillingAddress
    ) -> Customer:
        return await cls._client.customers.create(
            external_customer_id=organization.get_orb_external_customer_id(),
            email=notification_email,
            name=organization.name,
            payment_provider_id=organization.stripe_customer_id,
            # We use `stripe_charge` as we only want to use Stripe for doing the payment processing
            # and Orb for managing the subscription and invoicing.
            payment_provider="stripe_charge",
            billing_address=address,
            timezone="UTC",
            metadata={"region": cls._billing_region},
        )

    @classmethod
    @orb_exception_handler
    async def create_shared_infra_subscription(cls, customer: Customer, shared_billing_plan: SharedInfraBillingPlan):
        """
        Create a subscription to one of the shared infra plans for the given customer.
        At the moment, we have N plans for region and for T-shirt sizes.
        """
        return await cls._client.subscriptions.create(
            customer_id=customer.id,
            plan_id=shared_billing_plan.plan_id,
            # This will cause to always bill the user the same day of the month as the subscription start date
            align_billing_with_subscription_start_date=True,
            # This will automatically charge the customer for the current period
            auto_collection=True,
            # We need to indicate when the subscription started if not we will charge from the 1st day of the next month
            start_date=datetime.now().isoformat(),
        )

    @classmethod
    @orb_exception_handler
    async def change_subscription_plan(cls, organization: Organization, new_plan: SharedInfraBillingPlan) -> None:
        """
        Change the plan of the given subscription to the new plan.
        We will change the plan immediately if the new plan has more CPUs than the current one.
        If the new plan has less CPUs, the downgrade will happen at the next billing period.
        """
        subscription = await cls.get_subscription(organization)
        current_plan = await cls.get_subscription_plan(subscription.id)
        when_scheduled: Literal["end_of_subscription_term", "immediate"] = (
            "immediate" if new_plan.number_of_cpus > current_plan.number_of_cpus else "end_of_subscription_term"
        )

        await cls._client.subscriptions.schedule_plan_change(
            subscription_id=subscription.id,
            change_option=when_scheduled,
            plan_id=new_plan.plan_id,
        )

    @classmethod
    @orb_exception_handler
    async def cancel_subscription(cls, organization: Organization) -> OrganizationOrbSubscription:
        subscription = await OrbService.get_subscription(organization)
        await cls._client.subscriptions.cancel(subscription.id, cancel_option="end_of_subscription_term")
        cancelled_subscription = await cls._client.subscriptions.fetch(subscription_id=subscription.id)
        return OrganizationOrbSubscription.from_subscription(cancelled_subscription)

    @classmethod
    @orb_exception_handler
    async def unschedule_subscription_cancellation(cls, organization: Organization) -> None:
        subscription = await OrbService.get_subscription(organization)
        await cls._client.subscriptions.unschedule_cancellation(subscription.id)

    @classmethod
    @orb_exception_handler
    async def get_scheduled_downgrade(cls, organization: Organization) -> Optional[ScheduledSubscriptionChange]:
        """
        Get the next scheduled downgrade for the given subscription.
        We filter the scheduled changes to get only those whose start date is greater or equal than the end of the
        current billing period. We then get the one that starts right after the end of the current billing period if it
        hasn't been cancelled.
        """
        subscription = await cls.get_subscription(organization)
        scheduled_changes_paginated_list = cls._client.subscriptions.fetch_schedule(
            subscription_id=subscription.id, start_date_gte=subscription.current_billing_period_end_date
        )

        def _is_change_cancelled(scheduled_change: SubscriptionFetchScheduleResponse) -> bool:
            return scheduled_change.start_date == scheduled_change.end_date

        next_scheduled_change = None
        async for change in scheduled_changes_paginated_list:
            if change.start_date == subscription.current_billing_period_end_date and not _is_change_cancelled(change):
                next_scheduled_change = change
                break

        if not next_scheduled_change:
            return None

        downgrade_plan = await cls.get_shared_infra_plan(next_scheduled_change.plan.id)

        return ScheduledSubscriptionChange(plan=downgrade_plan, start_date=next_scheduled_change.start_date)

    @classmethod
    @orb_exception_handler
    async def cancel_scheduled_downgrade(cls, organization: Organization) -> None:
        subscription = await cls.get_subscription(organization)
        await cls._client.subscriptions.unschedule_pending_plan_changes(subscription_id=subscription.id)

    @classmethod
    @orb_exception_handler
    async def get_shared_infra_plans(cls) -> List[SharedInfraBillingPlan]:
        """
        Get the shared infra billing plan for the given region.
        We are going to have N plans in Orb for the shared infra plan, one for each region.
        Each plan will have a fixed fee price for the number of CPUs.

        Plans have a metadata 'available' to mark those plans that are available for the users.
        """
        shared_plans_by_region = []
        # Orb uses auto-paginating iterators on its list calls, we need to iterate with async for to use them
        async for plan in cls._client.plans.list(status="active"):
            if (
                plan.metadata.get("available", "false") == "true"
                and plan.metadata.get("region") == cls._billing_region
                and plan.metadata.get("kind") == PlanKind.SHARED.value
            ):
                shared_plans_by_region.append(plan)

        try:
            if len(shared_plans_by_region) == 0:
                raise OrbAPIException(f"No available shared infra plans found for region {cls._billing_region}")

            return [SharedInfraBillingPlan.from_plan(p) for p in shared_plans_by_region]
        except Exception as e:
            logging.error(f"Error getting shared infra plans: {e}")
            raise OrbAPIException(f"Error getting shared infra plans: {e}")

    @classmethod
    @orb_exception_handler
    async def get_subscription_plan(cls, subscription_id: str) -> SharedInfraBillingPlan:
        subscription = await cls._client.subscriptions.fetch(subscription_id=subscription_id)
        return SharedInfraBillingPlan.from_plan(subscription.plan)

    @classmethod
    @orb_exception_handler
    async def get_shared_infra_plan(cls, plan_id: str) -> SharedInfraBillingPlan:
        plan = await cls._client.plans.fetch(plan_id=plan_id)
        return SharedInfraBillingPlan.from_plan(plan)

    @classmethod
    @orb_exception_handler
    async def get_upcoming_invoice_usage(cls, organization: Organization) -> UpcomingInvoiceUsage:
        """Returns the upcoming invoice for the current billing cycle"""
        subscription = await cls.get_subscription(organization)
        upcoming_invoice = await cls._client.invoices.fetch_upcoming(subscription_id=subscription.id)
        return UpcomingInvoiceUsage.from_upcoming_invoice(upcoming_invoice)

    @classmethod
    @orb_exception_handler
    async def get_subscription_costs(
        cls, organization: Organization, timeframe_end: str, timeframe_start: str
    ) -> SubscriptionCosts:
        """Returns the subscription costs"""
        subscription = await cls.get_subscription(organization)
        costs_data = await cls._client.subscriptions.fetch_costs(
            subscription_id=subscription.id,
            timeframe_end=timeframe_end,
            timeframe_start=timeframe_start,
            view_mode="periodic",
        )
        return SubscriptionCosts.from_costs(costs_data)
