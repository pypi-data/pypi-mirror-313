import functools
import json
import logging
from datetime import datetime
from typing import Any, Callable, Optional, Tuple, cast

import stripe
import tornado
from dateutil.relativedelta import relativedelta
from orb.types.customer_create_params import BillingAddress
from stripe import Card, Charge, Customer, Invoice, PaymentMethod, SetupIntent, Subscription, Webhook, billing_portal
from tornado.escape import json_decode
from tornado.web import url

from tinybird.feature_flags import FeatureFlag, FeatureFlagsService
from tinybird.orb_integration.events import (
    OrbInvoicePaymentFailed,
    OrbInvoicePaymentSucceeded,
    OrbSubscriptionEnded,
    OrbSubscriptionPlanChanged,
    OrbWebhookEvent,
)
from tinybird.orb_service import OrbAPIException, OrbCustomerNotFound, OrbService, OrbSubscriptionNotFound
from tinybird.organization.organization import OrganizationCommitmentsPlans, Organizations
from tinybird.organization.organization_service import OrganizationService
from tinybird.tracing import ClickhouseTracer
from tinybird.workspace_service import WorkspaceService

from ..constants import BillingPlans, StripeEvents
from ..plans import PlansService
from ..user import User, Users
from .api_errors import RequestError
from .base import (
    ApiHTTPError,
    BaseHandler,
    has_workspace_access,
    is_workspace_admin,
    requires_write_access,
    user_authenticated,
)
from .mailgun import MailgunService


def is_shared_infra_ff_enabled(method: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(method)
    def wrapper(self: "BaseHandler", *args: Any, **kwargs: Any) -> Any:
        current_user = self.get_user_from_db()
        if not current_user:
            raise ApiHTTPError.from_request_error(RequestError(403, "User not found"))
        if not FeatureFlagsService.feature_for_email(
            FeatureFlag.SHARED_INFRA_FLOW, current_user.email, current_user.feature_flags
        ):
            raise ApiHTTPError.from_request_error(RequestError(403, "New billing is not enabled for this user"))
        return method(self, *args, **kwargs)

    return wrapper


def validate_date(year: Optional[str], month: Optional[str]):
    """
    >>> validate_date("2021", None)
    >>> validate_date("somestring", None)
    Traceback (most recent call last):
    ...
    tinybird.views.base.ApiHTTPError: HTTP 400: Bad Request (Parameter 'year' needs to be a number.)
    >>> validate_date("1", None)
    Traceback (most recent call last):
    ...
    tinybird.views.base.ApiHTTPError: HTTP 400: Bad Request (Parameter 'year' out of range.)
    >>> validate_date(None, "14")
    Traceback (most recent call last):
    ...
    tinybird.views.base.ApiHTTPError: HTTP 400: Bad Request (Parameter 'month' out of range.)
    """

    def validate_range(value_name, value, min, max):
        try:
            value = int(value)
        except ValueError:
            raise ApiHTTPError.from_request_error(RequestError(400, f"Parameter '{value_name}' needs to be a number."))
        if value < min or value > max:
            raise ApiHTTPError.from_request_error(RequestError(400, f"Parameter '{value_name}' out of range."))

    if year:
        validate_range("year", year, 2021, 2030)
    if month:
        validate_range("month", month, 1, 12)


class APIBillingHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @user_authenticated
    @is_workspace_admin
    async def get(self, workspace_id: str):
        """
        Get billing info for a workspace info

        Example: GET /v0/billing/{workspace-id} for a dev plan:

        ```json
        {
            'plan': 'dev',
            'packages': [
                {
                    'type': 'dev',
                    'concepts': [
                        {
                            'name': 'max_api_requests_per_day',
                            'quantity': 0,
                            'max': 1000
                        },
                        {
                            'name': 'max_gb_storage_used',
                            'quantity': 0,
                            'max': 10
                        }
                    ]
                }
            ]
        }
        ```

        For a Pro Plan:
        ```json
        {
            'plan': 'pro',
            'packages': [
                {
                    'type': 'extra',
                    'concepts': [
                        {
                            'name': 'processed_gb',
                            'quantity': 0.0,
                            'price_per_unit': 0.07
                        },
                        {
                            'name': 'storage_gb',
                            'quantity': 0.0,
                            'price_per_unit': 0.34
                        }
                    ]
                }
            ]
        }
        ```

        Enterprise plan with a free and a committed packages (extra one for the rest of the consumption):

        ```json
        {
            'plan': 'enterprise',
            'packages': [
                {
                    'type': 'free',
                    'concepts': [
                        {
                            'name': 'processed_gb',
                            'quantity': 0,
                            'included': 40
                        },
                        {
                            'name': 'storage_gb',
                            'quantity': 0,
                            'included': 80
                        }
                    ]
                },
                {
                    'type': 'committed',
                    'concepts': [
                        {
                            'name': 'processed_gb',
                            'quantity': 0.0,
                            'included': 120,
                            'price_per_unit': 0.1
                        },
                        {
                            'name': 'storage_gb',
                            'quantity': 0.0,
                            'included': 300,
                            'price_per_unit': 0.3
                        }
                    ],
                },
                {
                    'type': 'extra',
                    'concepts': [
                        {
                            'name': 'processed_gb',
                            'quantity': 0.0,
                            'price_per_unit': 0.07
                        },
                        {
                            'name': 'storage_gb',
                            'quantity': 0.0,
                            'price_per_unit': 0.34
                        }
                    ]
                }
            ]
        }
        ```

        """

        month = self.get_argument("month", None)
        year = self.get_argument("year", None)

        validate_date(year, month)

        workspace = User.get_by_id(workspace_id)
        metrics_cluster = self.application.settings.get("metrics_cluster", None)

        try:
            response = await PlansService.get_workspace_plan_info(workspace, year, month, metrics_cluster)
            self.write_json(response)
        except Exception as e:
            raise e


class APIBillingOrganizationHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @user_authenticated
    @is_shared_infra_ff_enabled
    async def get(self, organization_id: str):
        """
        Get billing info for an organization
        This endpoint will return the billing information (billing address, credit card, etc)
        Also if you have requested a downgrade, it will return the information about the downgrade.
        """
        organization = self._get_safe_organization(organization_id)

        # TODO: Return the billing info for the organization
        # TODO: Return the current expenses
        # TODO: Return current plan

        if not organization.in_shared_infra_pricing:
            raise ApiHTTPError.from_request_error(RequestError(400, "Organization is not on a shared infra plan"))

        try:
            us_stripe_api_key = self.application.settings.get("stripe", {}).get("us_api_key", None)
            stripe_customer = stripe.Customer.retrieve(organization.stripe_customer_id, api_key=us_stripe_api_key)
            response = {
                "address": stripe_customer.address,
            }

            self.write_json(
                {
                    **response,
                }
            )
        except Exception as e:
            logging.error(f"Error getting billing information: {e}")
            self.write_json({"error": str(e)})


class APIBillingUpgradeInfoHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @user_authenticated
    @is_workspace_admin
    async def get(self, workspace_id: str):
        """
        Get billing upgrade info for a workspace

        Example: GET /v0/billing/{workspace-id}/upgrade for a Dev plan:
        ```json
        {
              'current_plan': 'dev',
              'options': {
                  'dev': {
                      'max_api_requests_per_day': 1000,
                      'max_gb_storage_used': 10
                  },
                  'pro': {
                      'estimation_based_on_current_usage': 0,
                      'price_per_processed_gb': 0.07,
                      'price_per_stored_gb': 0.34
                  }
              }
          },
        ```
        Example for a Pro Plan:
        ```json
          {
              'current_plan': 'pro',
              'options': {
                  'dev': {
                      'max_api_requests_per_day': 1000,
                      'max_gb_storage_used': 10
                  },
                  'pro': {
                      'price_per_processed_gb': 0.07,
                      'price_per_stored_gb': 0.34
                  }
              }
          },
        ```
        """
        workspace = User.get_by_id(workspace_id)
        metrics_cluster = self.application.settings.get("metrics_cluster", None)
        upgrade_info = await PlansService.get_upgrade_info(workspace, metrics_cluster)
        self.write_json(upgrade_info)


class APIBillingOrganizationSharedPlansInfoHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @user_authenticated
    @is_shared_infra_ff_enabled
    async def get(self, organization_id: str):
        """
        Get shared infra plans info available for organizations

        Example: GET /v1/billing/{organization-id}/plans :
        ```json
        [
            {
                "plan_id": "XXXX",
                "number_of_cpus": 12,
                "number_of_max_qps": 480,
                "number_of_max_threads": 12,
                "number_of_max_copies": 36,
                "number_of_max_sinks": 36,
                "fixed_monthly_fee": 1094.04,
                "fixed_monthly_fee_yearly_commitment": 946.73,
                "included_storage_in_gb": 100,
                "cost_of_additional_gb_storage": 0.058,
                "cost_of_egress_gb_intra": 0.01,
                "cost_of_egress_gb_inter": 0.1,
            }
        ]
        """
        _ = self._get_safe_organization(organization_id)
        try:
            plans = await OrbService.get_shared_infra_plans()
            self.write_json(
                {
                    "plans": [
                        {
                            "plan_id": plan.plan_id,
                            "number_of_cpus": plan.number_of_cpus,
                            "number_of_max_qps": plan.number_of_max_qps,
                            "number_of_max_threads": plan.number_of_max_threads,
                            "number_of_max_copies": plan.number_of_max_copies,
                            "number_of_max_sinks": plan.number_of_max_sinks,
                            "fixed_monthly_fee": plan.fixed_monthly_fee,
                            "fixed_monthly_fee_yearly_commitment": plan.fixed_monthly_fee_yearly_commitment,
                            "included_storage_in_gb": plan.included_storage_in_gb,
                            "cost_of_additional_gb_storage": plan.cost_of_additional_gb_storage,
                            "cost_of_egress_gb_intra": plan.cost_of_egress_gb_intra,
                            "cost_of_egress_gb_inter": plan.cost_of_egress_gb_inter,
                        }
                        for plan in plans
                    ]
                }
            )
        except Exception as e:
            raise ApiHTTPError.from_request_error(RequestError(400, str(e)))


class APIBillingOrganizationSubscriptionChangeHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @user_authenticated
    @is_shared_infra_ff_enabled
    async def get(self, organization_id: str):
        """
        Get downgrade scheduled for the next billing period if any

        Example: GET /v1/billing/{organization-id}/subscription/change/
        ```json
        {
            "plan_id": "XXXX",
            "number_of_cpus": 1,
            "start_date": 1000,
        }
        ```
        """
        organization = self._get_safe_organization(organization_id)
        if not organization.stripe_customer_id or not organization.in_shared_infra_pricing:
            raise ApiHTTPError(400, "Organization does not have a shared infra plan")

        try:
            downgrade = await OrbService.get_scheduled_downgrade(organization)

            if downgrade is None:
                self.write_json({})
            else:
                self.write_json(
                    {
                        "plan_id": downgrade.plan.plan_id,
                        "number_of_cpus": downgrade.plan.number_of_cpus,
                        "start_date": downgrade.start_date.isoformat(),
                    }
                )
        except Exception as e:
            raise ApiHTTPError.from_request_error(RequestError(400, str(e)))

    @user_authenticated
    @is_shared_infra_ff_enabled
    async def post(self, organization_id: str):
        """
        Change the plan of an organization that already has a shared infra plan. Once the change is done Orb sends an
        event `OrbSubscriptionPlanChanged` to our webhook and then we update the commitment details.
        """
        organization = self._get_safe_organization(organization_id)

        if not organization.stripe_customer_id or not organization.in_shared_infra_pricing:
            raise ApiHTTPError(400, "Organization does not have a shared infra plan")

        plan_id = self.get_argument("plan_id")
        if not plan_id:
            raise ApiHTTPError(400, "No plan ID received")

        try:
            new_plan = await OrbService.get_shared_infra_plan(plan_id)
            await OrbService.change_subscription_plan(organization, new_plan)
            self.write_json({"response": "ok"})
        except Exception as e:
            raise ApiHTTPError.from_request_error(RequestError(400, str(e)))

    @user_authenticated
    @is_shared_infra_ff_enabled
    async def delete(self, organization_id: str):
        """
        Cancel any scheduled downgrade of an organization.
        """
        organization = self._get_safe_organization(organization_id)

        if not organization.stripe_customer_id or not organization.in_shared_infra_pricing:
            raise ApiHTTPError(400, "Organization does not have a shared infra plan")

        try:
            await OrbService.cancel_scheduled_downgrade(organization)
            self.write_json({"response": "ok"})
        except Exception as e:
            raise ApiHTTPError.from_request_error(RequestError(400, str(e)))


class APIBillinStatsHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @user_authenticated
    @has_workspace_access
    async def get(self, workspace_id: str):
        """
        Get billing stats info for a workspace

        Expects `stat` as query parameter with one of these values:
        - cumulative_request_along_the_month
        - daily_request_along_the_month
        - storage_bytes_used_along_the_month
        - processed_bytes_along_the_month
        - cumulative_processed_bytes_along_the_month
        - date_range
        """

        def get_date_arg(name: str) -> datetime:
            try:
                v = self.get_argument(name)
                return datetime.fromisoformat(v)
            except ValueError:
                raise ApiHTTPError(400, f"Invalid {name} '{v}'")

        def sort_dates(_from: datetime, to: datetime) -> Tuple[datetime, datetime]:
            return (_from, to) if _from < to else (to, _from)

        workspace = User.get_by_id(workspace_id)

        stat = self.get_argument("stat")
        if stat == "date_range":
            self.write_json(await PlansService.get_date_range(workspace))
            return

        _from, to = sort_dates(get_date_arg("start_date"), get_date_arg("end_date"))

        metrics_cluster = self.application.settings.get("metrics_cluster", None)

        if stat == "cumulative_request_along_the_month":
            self.write_json(
                await PlansService.get_cumulative_request_along_the_month(workspace, _from, to, metrics_cluster)
            )
        elif stat == "daily_request_along_the_month":
            self.write_json(await PlansService.get_daily_request_along_the_month(workspace, _from, to, metrics_cluster))
        elif stat == "storage_bytes_used_along_the_month":
            self.write_json(await PlansService.get_storage_bytes_used_along_the_month(workspace, _from, to))
        elif stat == "processed_bytes_along_the_month":
            self.write_json(
                await PlansService.get_processed_bytes_used_along_the_month(workspace, _from, to, metrics_cluster)
            )
        elif stat == "cumulative_processed_bytes_along_the_month":
            self.write_json(await PlansService.get_cumulative_processed_bytes_along_the_month(workspace, _from, to))
        else:
            self.write_json({"error": "stat not found"})


class APIBillingStripePortal(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @user_authenticated
    @is_workspace_admin
    def get(self, workspace_id: str):
        workspace = User.get_by_id(workspace_id)
        stripe_customer_id = workspace.stripe.get("customer_id", None)
        stripe_subscription_id = workspace.stripe.get("subscription_id", None)
        host = self.application.settings.get("host")

        if stripe_customer_id:
            session = billing_portal.Session.create(customer=stripe_customer_id, return_url=host)
            self.write_json({"url": session.url, "subscription_id": stripe_subscription_id})
        else:
            raise ApiHTTPError.from_request_error(RequestError(400, "No stripe config"))


def get_card_info_dict(card: Card) -> dict:
    return {
        "brand": card.get("brand", ""),
        "country": card.get("country", ""),
        "exp_month": card.get("exp_month", None),
        "exp_year": card.get("exp_year", None),
        "last4": card.get("last4", ""),
    }


class APIBillingChargesHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @user_authenticated
    @is_workspace_admin
    def get(self, workspace_id: str):
        """
        Get charges status. It returns a limit (defaults to 3) of charges in the last n months (defaults to 3).
        Status can be: succeeded, pending, or failed.

        Example: GET /v0/billing/{workspace-id}/charges?limit=2&months=4

        Sample response:

        {
            "charges": [
                {
                    "status": "succeeded"
                    "created": "21/12/2021",
                    "amount": 123,
                    "card": {
                        "brand": "visa",
                        "country": "US",
                        "exp_month": 4,
                        "exp_year": 2024,
                        "last4": "4242"
                    }
                },{
                    "status": "pending",
                    "created": "21/12/2021",
                    "amount": 123,
                    "card": {
                        "brand": "visa",
                        "country": "US",
                        "exp_month": 4,
                        "exp_year": 2024,
                        "last4": "4242"
                    }
                }
            ]
        }

        We could retrieve more information about the charge, see stripe docs: https://stripe.com/docs/api/charges/object?lang=python
        """

        workspace = User.get_by_id(workspace_id)
        stripe_customer_id = workspace.stripe.get("customer_id", None)

        months = self.get_argument("months", 3)
        limit = self.get_argument("limit", 3)

        from_charge_date = int(datetime.timestamp(datetime.today() - relativedelta(months=int(months))))

        if stripe_customer_id:
            charges = Charge.list(customer=stripe_customer_id, created={"gt": from_charge_date}, limit=limit)

            charges = list(map(lambda charge: self._get_charge_info(charge), charges))
            self.write_json({"charges": charges})
        else:
            self.write_json({"charges": []})

    @staticmethod
    def _get_charge_info(charge: Charge) -> dict:
        created = datetime.fromtimestamp(charge.created).strftime("%d/%m/%Y")

        card = {}
        try:
            card = get_card_info_dict(charge.payment_method_details.card)
        except AttributeError:
            # Some charges do not have a card object so it's expected to fail
            pass

        return {
            "status": charge.status,
            "card": card,
            "amount": charge.amount,
            "created": created,
        }


class APIBillingInvoicesHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @user_authenticated
    @is_workspace_admin
    def get(self, workspace_id: str):
        """
        Get invoices. It returns a limit (defaults to 3) of invoices.
        Status can be: draft, open, paid, uncollectible, or void.

        Example: GET /v0/billing/{workspace-id}/invoices?limit=2&months=4

        Sample response:

        {
            "invoices": [
                {
                    "status": "paid"
                    "created": "21/12/2021",
                    "total": 123
                },{
                    "status": "paid"
                    "created": "21/12/2021",
                    "total": 123
                }
            ]
        }

        We could retrieve more information about the charge, see stripe docs: https://stripe.com/docs/api/invoices/object?lang=python
        """

        workspace = User.get_by_id(workspace_id)
        stripe_customer_id = workspace.stripe.get("customer_id", None)

        limit = self.get_argument("limit", 3)

        if stripe_customer_id:
            invoices = Invoice.list(customer=stripe_customer_id, limit=limit)

            invoices = list(map(lambda invoice: self._get_invoice_info(invoice), invoices))
            self.write_json({"invoices": invoices})
        else:
            self.write_json({"invoices": []})

    @staticmethod
    def _get_invoice_info(invoice: Invoice) -> dict:
        created = datetime.fromtimestamp(invoice.created).strftime("%d/%m/%Y")
        return {"status": invoice.status, "total": invoice.total, "created": created}


class APIBillingSetupIntentHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @user_authenticated
    @is_workspace_admin
    async def post(self, workspace_id: str):
        workspace = User.get_by_id(workspace_id)
        stripe_client_secret = workspace.stripe.get("client_secret", None)

        if stripe_client_secret:
            raise ApiHTTPError(400, "Already exists")  # FIXME

        stripe_customer_id = workspace.stripe.get("customer_id", None)

        try:
            stripe_setup_intent = SetupIntent.create(payment_method_types=["card"], customer=stripe_customer_id)

            stripe_client_secret = stripe_setup_intent.get("client_secret", None)

            await Users.set_stripe_settings(workspace, stripe_client_secret=stripe_client_secret)
        except Exception as e:
            raise ApiHTTPError(400, str(e))  # FIXME

        self.write_json({"response": "ok"})  # FIXME

    @user_authenticated
    @is_workspace_admin
    def put(self, workspace_id: str):
        workspace = User.get_by_id(workspace_id)
        stripe_client_secret = workspace.stripe.get("client_secret", None)

        if not stripe_client_secret:
            raise ApiHTTPError(400, "Does not exists")  # FIXME

        payment_method_id = self.get_argument("payment_method_id", None)

        if not payment_method_id:
            raise ApiHTTPError(400, "Incorrect payment method id")  # FIXME

        try:
            SetupIntent.confirm(stripe_client_secret, payment_method=payment_method_id)
        except Exception as e:
            raise ApiHTTPError(400, str(e))  # FIXME

        self.write_json({"response": "ok"})  # FIXME

    @user_authenticated
    @requires_write_access
    @is_workspace_admin
    async def delete(self, workspace_id: str):
        workspace = User.get_by_id(workspace_id)
        stripe_client_secret = workspace.stripe.get("client_secret", None)

        if not stripe_client_secret:
            raise ApiHTTPError(400, "Does not exists")  # FIXME

        try:
            SetupIntent.cancel(stripe_client_secret)
            await Users.set_stripe_settings(workspace, stripe_client_secret="")
        except Exception as e:
            raise ApiHTTPError(400, str(e))  # FIXME

        self.write_json({"response": "ok"})  # FIXME


class APIBillingPaymentHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @user_authenticated
    @is_workspace_admin
    def get(self, workspace_id: str):
        """
        Get payment information:

        Example: GET /v0/billing/{workspace-id}/payment

        Sample response:
            {
                "payment_method": {
                    "billing_details": {
                        "address": {
                            "city": "City Name",
                            "country": "ES",
                            "line1": "Address 1",
                            "line2": "Address 2",
                            "postal_code": "12345",
                            "state": "State"
                        },
                        "email": "payment@email.co",
                        "name": "Full Name",
                        "phone": null
                    },
                    "card": {
                        "brand": "visa",
                        "country": "US",
                        "exp_month": 4,
                        "exp_year": 2024,
                        "last4": "4242"
                    }
                },
                "invoice": {
                    "amount_due": 43,
                    "period_end": "21/01/2022"
                }
            }
        """

        workspace = User.get_by_id(workspace_id)

        stripe_customer_id = workspace.stripe.get("customer_id", None)

        if not stripe_customer_id:
            raise ApiHTTPError(400, f"There is no customer configured for the Workspace {workspace.name}")  # FIXME

        try:
            stripe_customer = Customer.retrieve(stripe_customer_id)
            payment_method_id = stripe_customer.get("invoice_settings", {}).get("default_payment_method", None)
            payment_method = PaymentMethod.retrieve(payment_method_id)
            upcoming_invoice = Invoice.upcoming(customer=stripe_customer_id)
            card = payment_method.get("card", {})
            period_end = datetime.fromtimestamp(upcoming_invoice.period_end).strftime("%m/%d/%Y")

            subscription_id = workspace.stripe.get("subscription_id", None)
            if subscription_id:
                subscription = Subscription.retrieve(subscription_id)
                subscription_start = datetime.fromtimestamp(subscription.created).strftime("%m/%d/%Y")
            else:
                subscription_start = None

            self.write_json(
                {
                    "payment_method": {
                        "billing_details": payment_method.billing_details,
                        "card": get_card_info_dict(card),
                    },
                    "invoice": {"amount_due": upcoming_invoice.amount_due * 0.01, "period_end": period_end},
                    "subscription_start": subscription_start,
                }
            )
        except Exception as e:
            raise ApiHTTPError(400, str(e))  # FIXME

    @user_authenticated
    @is_workspace_admin
    async def post(self, workspace_id: str):
        workspace = User.get_by_id(workspace_id)
        stripe_setup_intent_id = workspace.stripe.get("setup_intent_id", None)

        # 1. Cancel payment intent if exists
        if stripe_setup_intent_id:
            try:
                SetupIntent.cancel(stripe_setup_intent_id)
            # TODO manage possible errors when the SetupIntent is already cancelled or in a non cancellable state
            except Exception as e:
                logging.exception(e)
            stripe_setup_intent_id = ""

        # 2. Create customer if does not exist
        stripe_customer_id = workspace.stripe.get("customer_id", None)
        if not stripe_customer_id:
            try:
                stripe_customer = Customer.create(name=workspace.id)
                stripe_customer_id = stripe_customer.get("id", None)
            except Exception as e:
                raise ApiHTTPError(400, str(e))  # FIXME

        # 3. Create new payment intent
        try:
            stripe_setup_intent = SetupIntent.create(payment_method_types=["card"], customer=stripe_customer_id)
            stripe_client_secret = stripe_setup_intent["client_secret"]
            stripe_setup_intent_id = stripe_setup_intent["id"]
        except Exception as e:
            raise ApiHTTPError(400, str(e))  # FIXME

        # 4. Save stripe settings
        await Users.set_stripe_settings(
            workspace=workspace,
            stripe_customer_id=stripe_customer_id,
            stripe_client_secret=stripe_client_secret,
            stripe_setup_intent=stripe_setup_intent_id,
        )

        self.write_json({"response": "ok"})  # FIXME


class APIBillingOrganizationPaymentHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @user_authenticated
    @is_shared_infra_ff_enabled
    def get(self, organization_id: str):
        """
        Get payment information:

        Example: GET /v0/billing/{organization-id}/payment

        Sample response:
            {
            }
        """
        organization = self._get_safe_organization(organization_id)
        stripe_customer_id = organization.stripe_customer_id

        if not stripe_customer_id:
            raise ApiHTTPError(400, f"There is no customer configured for the Organization {organization.name}")

        try:
            us_stripe_api_key = self.application.settings.get("stripe", {}).get("us_api_key", None)
            if not us_stripe_api_key:
                logging.error("No Stripe API key configured for the US account")
                raise ApiHTTPError(400, "No Stripe API key configured for the US account")

            # By default, the Stripe API key is configured for the Spanish account
            # But all the new shared infra billing is using the US account
            stripe_customer = Customer.retrieve(stripe_customer_id, api_key=us_stripe_api_key)
            payment_method_id = stripe_customer.get("invoice_settings", {}).get("default_payment_method", None)
            payment_method = PaymentMethod.retrieve(payment_method_id, api_key=us_stripe_api_key)
            card = payment_method.get("card", {})

            self.write_json(
                {
                    "payment_method": {
                        "billing_details": payment_method.billing_details,
                        "card": get_card_info_dict(card),
                    },
                    "invoice": {"amount_due": 0, "period_end": None},
                    "subscription_start": None,
                }
            )
        except Exception as e:
            raise ApiHTTPError(400, str(e))

    @user_authenticated
    @is_shared_infra_ff_enabled
    async def post(self, organization_id: str):
        organization = self._get_safe_organization(organization_id)
        stripe_setup_intent_id = organization.stripe_setup_intent_id

        us_stripe_api_key = self.application.settings.get("stripe", {}).get("us_api_key", None)
        if not us_stripe_api_key:
            logging.error("No Stripe API key configured for the US account")
            raise ApiHTTPError(400, "No Stripe API key configured for the US account")

        # 1. Cancel payment intent if exists
        if stripe_setup_intent_id:
            try:
                SetupIntent.cancel(stripe_setup_intent_id, api_key=us_stripe_api_key)
            # TODO manage possible errors when the SetupIntent is already cancelled or in a non cancellable state
            except Exception as e:
                logging.exception(e)

        # 2. Create customer if it does not exist
        stripe_customer_id = organization.stripe_customer_id
        if not stripe_customer_id:
            try:
                stripe_customer = Customer.create(name=organization.id, api_key=us_stripe_api_key)
                stripe_customer_id = stripe_customer.get("id")
                assert isinstance(stripe_customer_id, str)
            except Exception as e:
                raise ApiHTTPError(400, str(e))

        # 3. Create new payment intent
        try:
            stripe_setup_intent = SetupIntent.create(
                payment_method_types=["card"], customer=stripe_customer_id, api_key=us_stripe_api_key
            )
            stripe_client_secret = stripe_setup_intent["client_secret"]
            assert isinstance(stripe_client_secret, str)
            stripe_setup_intent_id = stripe_setup_intent["id"]
            assert isinstance(stripe_setup_intent_id, str)
        except Exception as e:
            raise ApiHTTPError(400, str(e))

        # 4. Save stripe settings
        await Organizations.set_stripe_customer_id(organization, stripe_customer_id)
        await Organizations.set_setup_intent_id(organization, stripe_setup_intent_id, stripe_client_secret)
        self.write_json({"response": "ok"})


class APIBillingCustomerHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @user_authenticated
    @is_workspace_admin
    async def post(self, workspace_id: str):
        workspace = User.get_by_id(workspace_id)

        stripe_customer_id = workspace.stripe.get("customer_id", None)
        stripe_email = workspace.stripe.get("email", None)

        email = self.get_argument("email", stripe_email)

        if not email:
            raise ApiHTTPError(400, "no email")  # FIXME

        if stripe_customer_id:
            raise ApiHTTPError(400, "Customer already exists")  # FIXME

        try:
            stripe_customer = Customer.create(email=email, name=workspace.id)
            stripe_customer_id = stripe_customer.get("id", None)

            await Users.set_stripe_settings(
                workspace=workspace, stripe_customer_id=stripe_customer_id, stripe_email=email
            )
        except Exception as e:
            raise ApiHTTPError(400, str(e))  # FIXME

        self.write_json({"response": "ok"})  # FIXME

    @user_authenticated
    @is_workspace_admin
    def put(self, workspace_id: str):
        workspace = User.get_by_id(workspace_id)

        stripe_customer_id = workspace.stripe.get("customer_id", None)
        stripe_email = workspace.stripe.get("email", None)

        email = self.get_argument("email", stripe_email)
        address = None

        try:
            extra_info = json_decode(self.request.body)
            if "address" in extra_info:
                address = extra_info["address"]
        except json.JSONDecodeError as e:
            raise ApiHTTPError(400, f"Invalid address: {e.msg}")  # FIXME

        if not stripe_customer_id:
            raise ApiHTTPError(400, "No customer")  # FIXME

        try:
            Customer.modify(stripe_customer_id, email=email, address=address)
        except Exception as e:
            raise ApiHTTPError(400, str(e))  # FIXME

        self.write_json({"response": "ok"})  # FIXME


class APIBillingSubscriptionHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.mailgun_service = MailgunService(self.application.settings)

    async def _send_notification_on_plan_upgraded(self, workspace: User, current_plan: str, previous_plan: str):
        send_to_emails = workspace.get_user_emails_that_have_access_to_this_workspace()

        if len(send_to_emails) != 0:
            notification_result = await self.mailgun_service.send_notification_on_plan_upgraded(
                send_to_emails,
                workspace.name,
                workspace.id,
                PlansService.get_plan_name_to_render(current_plan),
                PlansService.get_plan_name_to_render(previous_plan),
            )

            if notification_result.status_code != 200:
                logging.error(
                    f"Notification for Workspace upgraded was not delivered to {send_to_emails}, "
                    f"code: {notification_result.status_code} reason: {notification_result.content}"
                )

    @user_authenticated
    @is_workspace_admin
    async def post(self, workspace_id: str):
        workspace = User.get_by_id(workspace_id)

        stripe_email = workspace.stripe.get("email", None)
        email = self.get_argument("email", stripe_email)
        coupon_id = self.get_argument("coupon", None)

        if not email:
            raise ApiHTTPError(400, "No email")  # FIXME

        stripe_customer_id = workspace.stripe.get("customer_id", None)
        if not stripe_customer_id:
            raise ApiHTTPError(400, "No customer")  # FIXME

        stripe_subscription_id = workspace.stripe.get("subscription_id", None)
        if stripe_subscription_id:
            raise ApiHTTPError(400, "Already subscribed")  # FIXME

        setup_intent_id = workspace.stripe.get("setup_intent_id", None)
        if not setup_intent_id:
            raise ApiHTTPError(400, "No Setup Intent")  # FIXME

        payment_method_id = self.get_argument("payment_method_id", None)
        if not payment_method_id:
            raise ApiHTTPError(400, "Incorrect payment method id")  # FIXME

        if setup_intent_id:
            confirmation = SetupIntent.retrieve(setup_intent_id)
            if confirmation["status"] != "succeeded":
                logging.error("Error confirming paymeny method: ", confirmation)
                raise ApiHTTPError(400, "Payment method requires additional validation steps")

        plan = self.get_argument("plan")

        if plan is None or plan != BillingPlans.PRO:
            raise ApiHTTPError(400, f"Workspace can't be subscribed to plan {plan}")

        if workspace.plan == BillingPlans.PRO:
            raise ApiHTTPError(400, "The Workspace is already subscribed to the plan Pro")

        prices = PlansService.get_default_prices_by_plan(plan, workspace)
        assert isinstance(prices, list)

        prices_id = [{"price": price.get("id")} for price in prices]

        try:
            PaymentMethod.attach(payment_method_id, customer=stripe_customer_id)

            Customer.modify(
                stripe_customer_id, email=email, invoice_settings={"default_payment_method": payment_method_id}
            )

            start_date = datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            backdate_start_date = int(datetime.timestamp(start_date))
            billing_cycle_anchor = int(datetime.timestamp(start_date + relativedelta(months=1)))

            stripe_subscription = Subscription.create(
                customer=stripe_customer_id,
                default_payment_method=payment_method_id,
                items=prices_id,
                billing_cycle_anchor=billing_cycle_anchor,
                backdate_start_date=backdate_start_date,
                expand=["latest_invoice.payment_intent"],
                metadata={"workspace_id": workspace_id, "plan_type": BillingPlans.PRO},
                coupon=coupon_id,
            )
            stripe_subscription_id = stripe_subscription.get("id", None)
        except Exception as e:
            raise ApiHTTPError(400, str(e))  # FIXME

        await Users.set_stripe_settings(
            workspace=workspace, stripe_email=email, stripe_subscription_id=stripe_subscription_id
        )

        old_plan = workspace.plan

        updated_workspace = await Users.change_workspace_plan(workspace=workspace, new_plan=plan)

        tracer: ClickhouseTracer = self.application.settings["opentracing_tracing"].tracer
        WorkspaceService.trace_workspace_operation(tracer, updated_workspace, "PlanChanged", self.current_user)

        await self._send_notification_on_plan_upgraded(workspace, plan, old_plan)

        self.write_json({"response": "ok"})  # FIXME


class APIBillingSubscriptionCancellationHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

    def check_xsrf_cookie(self):
        pass

    @user_authenticated
    @is_shared_infra_ff_enabled
    async def post(self, organization_id: str):
        """
        Cancel an organization's subscription in Orb
        """
        organization = self._get_safe_organization(organization_id)

        if not organization.in_shared_infra_pricing:
            raise ApiHTTPError.from_request_error(RequestError(400, "Organization has not a shared infra plan"))

        try:
            # Cancel the subscription. This is most likely not immediate and will happen at the end of the current
            # billing cycle. We will receive a subscription.ended webhook event from Orb when the cancellation
            # is effective
            subscription = await OrbService.cancel_subscription(organization)

            tracer: ClickhouseTracer = self.application.settings["opentracing_tracing"].tracer
            OrganizationService.trace_organization_operation(
                tracer,
                organization,
                "OrganizationSubscriptionCancellationScheduled",
                self.current_user,
                extra={"subscription_end_date": subscription.commitment_end_date.isoformat()},
            )
            self.write_json({"response": "ok"})
        except Exception as e:
            logging.exception(e)
            raise ApiHTTPError(400, str(e))

    @user_authenticated
    @is_shared_infra_ff_enabled
    async def delete(self, organization_id: str):
        organization = self._get_safe_organization(organization_id)

        if not organization.in_shared_infra_pricing:
            raise ApiHTTPError.from_request_error(RequestError(400, "Organization is not on a shared infra plan"))

        try:
            await OrbService.unschedule_subscription_cancellation(organization)
            tracer: ClickhouseTracer = self.application.settings["opentracing_tracing"].tracer
            OrganizationService.trace_organization_operation(
                tracer, organization, "OrganizationSubscriptionCancellationUnscheduled", self.current_user
            )
            self.write_json({"response": "ok"})
        except (OrbCustomerNotFound, OrbSubscriptionNotFound) as e:
            logging.warning(f"Error unscheduling subscription cancellation: {e}")
            raise ApiHTTPError.from_request_error(RequestError(404, str(e))) from e
        except OrbAPIException as e:
            logging.warning(f"Error unscheduling subscription cancellation: {e}")
            raise ApiHTTPError.from_request_error(RequestError(400, str(e))) from e
        except Exception as e:
            logging.error(f"Error unscheduling subscription cancellation: {e}")
            raise ApiHTTPError.from_request_error(RequestError(500, str(e))) from e


class APIBillingOrganizationSubscriptionHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

    def check_xsrf_cookie(self):
        pass

    @user_authenticated
    @is_shared_infra_ff_enabled
    async def get(self, organization_id: str):
        """Return the current subscription"""
        organization = self._get_safe_organization(organization_id)
        if not organization.in_shared_infra_pricing:
            raise ApiHTTPError.from_request_error(RequestError(400, "Organization is not on a shared infra plan"))
        try:
            subscription = await OrbService.get_subscription(organization)
            response_data = {
                "start_date": self.optional_date_to_str(subscription.commitment_start_date),
                # If end_date is not None, it means the subscription has been cancelled
                "end_date": self.optional_date_to_str(subscription.commitment_end_date),
                "customer_portal": subscription.customer_portal,
                "current_billing_period_start_date": self.optional_date_to_str(
                    subscription.current_billing_period_start_date
                ),
                "current_billing_period_end_date": self.optional_date_to_str(
                    subscription.current_billing_period_end_date
                ),
            }
            self.write_json({"data": response_data})
        except (OrbCustomerNotFound, OrbSubscriptionNotFound) as e:
            logging.warning(f"Error getting subscription: {e}")
            raise ApiHTTPError.from_request_error(RequestError(404, str(e))) from e
        except Exception as e:
            logging.error(e)
            raise ApiHTTPError(500, "Errors getting subscription") from e

    @user_authenticated
    @is_shared_infra_ff_enabled
    async def post(self, organization_id: str):
        organization = self._get_safe_organization(organization_id)

        if organization.in_shared_infra_pricing:
            raise ApiHTTPError(400, "Organization already has a shared infra plan")

        notification_email = self.get_argument("email")
        if not notification_email:
            raise ApiHTTPError(400, "No email was provided")

        plan_id = self.get_argument("plan_id")
        if not plan_id:
            raise ApiHTTPError(400, "No plan ID was provided")

        stripe_customer_id = organization.stripe_customer_id
        if not stripe_customer_id:
            raise ApiHTTPError(400, "The organization has no Stripe customer ID")

        setup_intent_id = organization.stripe_setup_intent_id
        if not setup_intent_id:
            raise ApiHTTPError(400, "The organization has no Setup Intent")

        payment_method_id = self.get_argument("payment_method_id", None)
        if not payment_method_id:
            raise ApiHTTPError(400, "Incorrect payment method id")

        us_stripe_api_key = self.application.settings.get("stripe", {}).get("us_api_key", None)
        if not us_stripe_api_key:
            logging.error("No Stripe API key configured for the US account")
            raise ApiHTTPError(400, "No Stripe API key configured for the US account")

        confirmation = SetupIntent.retrieve(setup_intent_id, api_key=us_stripe_api_key)
        if confirmation["status"] != "succeeded":
            logging.error(
                f"Error confirming payment method: {confirmation['status']} {confirmation['last_setup_error']}"
            )
            raise ApiHTTPError(400, "Payment method requires additional validation steps")

        try:
            extra_info = json_decode(self.request.body)
            if "address" in extra_info:
                address_dict = extra_info["address"]
        except json.JSONDecodeError as e:
            raise ApiHTTPError(400, f"Invalid address: {e.msg}")  # FIXME

        try:
            plan = await OrbService.get_shared_infra_plan(plan_id)
            PaymentMethod.attach(payment_method_id, customer=stripe_customer_id, api_key=us_stripe_api_key)
            organization = await Organizations.set_stripe_customer_id(organization, stripe_customer_id)
            orb_customer = await OrbService.create_customer(
                organization, notification_email, cast(BillingAddress, address_dict)
            )
            Customer.modify(stripe_customer_id, address=address_dict, api_key=us_stripe_api_key)
            await OrbService.create_shared_infra_subscription(orb_customer, plan)

            # When we do the upgrade let's update the number of CPUs in the commitment.
            # We will consume the events of Orb to know if the subscription and payment was successful or not and update accordingly.
            # TODO: We need to include also the max QPS, max copies, ...
            organization = Organizations.update_commitment_information(
                organization,
                start_date=organization.commitment_start_date,
                end_date=organization.commitment_end_date,
                commited_processed=organization.commitment_processed,
                commited_storage=organization.commitment_storage,
                commited_data_transfer_intra=organization.commitment_data_transfer_intra,
                commited_data_transfer_inter=organization.commitment_data_transfer_inter,
                commitment_machine_size=organization.commitment_machine_size,
                commitment_billing=OrganizationCommitmentsPlans.SHARED_INFRASTRUCTURE_USAGE,
                commitment_cpu=plan.number_of_cpus,
                commitment_max_qps=plan.number_of_max_qps,
            )

            # Let's indicate in Spans that the organization has upgraded to PRO with a number of CPUs
            tracer: ClickhouseTracer = self.application.settings["opentracing_tracing"].tracer
            OrganizationService.trace_organization_operation(
                tracer, organization, "OrganizationPlanChanged", self.current_user
            )
        except Exception as e:
            logging.exception(e)
            raise ApiHTTPError(400, str(e))

        self.write_json({"response": "ok"})

    @user_authenticated
    @is_shared_infra_ff_enabled
    async def delete(self, organization_id: str):
        """
        Cancel an organization's subscription in Orb
        """
        organization = self._get_safe_organization(organization_id)

        if not organization.in_shared_infra_pricing:
            raise ApiHTTPError.from_request_error(RequestError(400, "Organization is not on a shared infra plan"))

        try:
            # Cancel the subscription. This is most likely not immediate and will happen at the end of the current
            # billing cycle. We will receive a subscription.ended webhook event from Orb when the cancellation
            # is effective
            subscription = await OrbService.cancel_subscription(organization)

            tracer: ClickhouseTracer = self.application.settings["opentracing_tracing"].tracer
            OrganizationService.trace_organization_operation(
                tracer,
                organization,
                "OrganizationSubscriptionCancellationScheduled",
                self.current_user,
                extra={"subscription_end_date": subscription.commitment_end_date.isoformat()},
            )
            self.write_json({"response": "ok"})
        except Exception as e:
            logging.exception(e)
            raise ApiHTTPError(400, str(e))


class APIStripeWebhook(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.mailgun_service = MailgunService(self.application.settings)

    async def _send_notification_on_plan_downgraded(self, workspace: User, current_plan: str, previous_plan: str):
        send_to_emails = workspace.get_user_emails_that_have_access_to_this_workspace()

        if len(send_to_emails) != 0:
            notification_result = await self.mailgun_service.send_notification_on_plan_downgraded(
                send_to_emails,
                workspace.name,
                workspace.id,
                PlansService.get_plan_name_to_render(current_plan),
                PlansService.get_plan_name_to_render(previous_plan),
            )

            if notification_result.status_code != 200:
                logging.error(
                    f"Notification for Workspace downgraded was not delivered to {send_to_emails}, "
                    f"code: {notification_result.status_code} reason: {notification_result.content}"
                )

    def check_xsrf_cookie(self):
        pass

    async def post(self):
        payload = self.request.body
        signature = self.request.headers.get("Stripe-Signature", "")
        webhook_endpoint_secret = self.application.settings.get("stripe", {}).get("webhook_endpoint_secret")

        event_type = None

        try:
            event = Webhook.construct_event(payload=payload, sig_header=signature, secret=webhook_endpoint_secret)
            event_type = event.get("type")
            logging.info(f"Stripe: {event_type} received")
        except ValueError as e:
            logging.exception(e)
            raise ApiHTTPError.from_request_error(RequestError(400, f"Stripe webhook error: {e}"))
        except stripe.error.SignatureVerificationError as e:
            logging.exception(e)
            raise ApiHTTPError.from_request_error(RequestError(400, f"Stripe signature webhook error: {e}"))

        if not event_type:
            raise ApiHTTPError.from_request_error(RequestError(400, "There has been a problem"))

        # TODO idea: save event using NDJSON and HFI
        if event_type == StripeEvents.SUBSCRIPTION_DELETED:
            workspace_id = event["data"]["object"]["metadata"].get("workspace_id", None)

            try:
                workspace = User.get_by_id(workspace_id) if workspace_id is not None else None
                if not workspace:
                    self.set_status(202)
                elif workspace.stripe.get("subscription_id", None):
                    previous_plan = workspace.plan

                    await Users.remove_stripe_subscription(workspace)
                    updated_workspace = await Users.change_workspace_plan(workspace, BillingPlans.DEV)

                    tracer: ClickhouseTracer = self.application.settings["opentracing_tracing"].tracer
                    WorkspaceService.trace_workspace_operation(
                        tracer, updated_workspace, "PlanChanged", self.current_user
                    )

                    await self._send_notification_on_plan_downgraded(workspace, BillingPlans.DEV, previous_plan)

                    logging.info(f"Stripe: successfully handled {event_type}")

            except Exception as e:
                logging.exception(e)
                raise ApiHTTPError.from_request_error(
                    RequestError(400, f"Could not handle Stripe '{event_type}' event: {e}")
                )
        else:
            logging.info(f"Stripe: event not handled: {event_type}")

        logging.info(f"Stripe: finished {event_type}")
        self.write("ok")


class APIOrbWebhook(tornado.web.RequestHandler):
    def check_xsrf_cookie(self):
        pass

    async def post(self):
        body = self.request.body
        try:
            payload = await OrbService.unwrap_webhook(body, self.request.headers)
            event_type = payload.get("type")

            event: OrbWebhookEvent | None = None
            match event_type:
                case OrbInvoicePaymentSucceeded.EVENT_TYPE:
                    event = OrbInvoicePaymentSucceeded(payload)
                case OrbInvoicePaymentFailed.EVENT_TYPE:
                    event = OrbInvoicePaymentFailed(payload)
                case OrbSubscriptionPlanChanged.EVENT_TYPE:
                    event = OrbSubscriptionPlanChanged(payload)
                case OrbSubscriptionEnded.EVENT_TYPE:
                    event = OrbSubscriptionEnded(payload)
                case _:
                    logging.info(f"Orb: event not handled: {event_type}")

            if event:
                tracer: ClickhouseTracer = self.application.settings["opentracing_tracing"].tracer
                await event.process(tracer)
                logging.info(f"Orb: successfully processed {event_type} webhook")

            self.write("ok")
        except Exception as e:
            logging.exception(e)
            raise ApiHTTPError.from_request_error(RequestError(400, f"Could not handle Orb webhook: {e}"))


class APIBillingPlanLimitsHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @user_authenticated
    @has_workspace_access
    async def get(self, workspace_id: str):
        """
        Get billing plan limits info for a workspace

        Example: GET /v0/billing/{workspace-id}/plan-limits for a Dev plan:
        ```json
        {
              'limits': {
                  'max_api_requests_per_day': {
                      'max': 1000,
                      'quantity': 123
                  },
                  'max_gb_storage_used': {
                      'max': 10,
                      'quantity': 4,
                  }
              }
          },
        ```
        """
        workspace = User.get_by_id(workspace_id)
        metrics_cluster = self.application.settings.get("metrics_cluster", None)
        limits = await PlansService.get_workspace_limits(workspace=workspace, metrics_cluster=metrics_cluster)
        self.write_json({"limits": limits})


class InvalidPromotionCodeError(Exception):
    pass


class APIBillingCouponHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @staticmethod
    def get_coupon_from_promotion_code(promotion_code) -> dict:
        """Get Stripe coupon from a Promotion Code

        promotion_code is the code, not the id, of the promotion_code.
        """
        promo_codes = stripe.PromotionCode.list(code=promotion_code)
        if len(promo_codes) == 0:
            raise InvalidPromotionCodeError("No matching active promotion code")
        active_promo_codes = list(filter(lambda x: x["active"], promo_codes))
        if len(active_promo_codes) == 0:
            raise InvalidPromotionCodeError("No matching active promotion code")
        # Promotion codes aren't totally unique, but there can only be 1 active one with a given code
        assert len(active_promo_codes) == 1, "There shouldn't be multiple active promo codes with the same code"
        coupon = stripe.Coupon.retrieve(active_promo_codes[0]["coupon"]["id"])
        return coupon

    def get(self):
        promotion_code = self.get_argument("promotion_code", None)

        if promotion_code:
            try:
                coupon = self.get_coupon_from_promotion_code(promotion_code)
                # Sending minimal fields to avoid exposing internal information.
                coupon_response = {
                    "id": coupon["id"],
                    "amount_off": coupon["amount_off"],
                    "percent_off": coupon["percent_off"],
                }
                self.write_json({"coupon": coupon_response})
            except InvalidPromotionCodeError as e:
                logging.warning(e)
                raise ApiHTTPError.from_request_error(RequestError(404, str(e)))
            except Exception as e:
                logging.exception(e)
                raise ApiHTTPError.from_request_error(RequestError(500, "Unexpected error"))
        else:
            raise ApiHTTPError.from_request_error(RequestError(400, "Missing promotion code"))


class APIBillingOrganizationSubscriptionCurrentUsageHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

    def check_xsrf_cookie(self):
        pass

    @user_authenticated
    @is_shared_infra_ff_enabled
    async def get(self, organization_id: str):
        """Get current billing cycle usage

        We're getting the usage from the upcoming invoice of the current billing cycle.
        """
        organization = self._get_safe_organization(organization_id)
        if not organization.in_shared_infra_pricing:
            raise ApiHTTPError.from_request_error(RequestError(400, "Organization is not on a shared infra plan"))
        try:
            upcoming_invoice_usage = await OrbService.get_upcoming_invoice_usage(organization)
            response_data = [
                {"name": li.name, "quantity": li.quantity, "amount": li.amount}
                for li in upcoming_invoice_usage.line_items
            ]
            self.write_json({"data": response_data})
        except (OrbCustomerNotFound, OrbSubscriptionNotFound) as e:
            logging.warning(f"Error getting upcoming invoice usage: {e}")
            raise ApiHTTPError.from_request_error(RequestError(404, str(e))) from e
        except Exception as e:
            logging.error(f"Error getting upcoming invoice usage: {e}")
            raise ApiHTTPError.from_request_error(RequestError(500, str(e))) from e


class APIBillingSubscriptionCostsHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

    def check_xsrf_cookie(self):
        pass

    @user_authenticated
    async def get(self, organization_id: str):
        """Get subscription costs"""
        timeframe_start = self.get_argument("timeframe_start", default=None, strip=True)
        timeframe_end = self.get_argument("timeframe_end", default=None, strip=True)
        organization = self._get_safe_organization(organization_id)

        if not (organization.in_shared_infra_pricing or organization.in_dedicated_infra_pricing):
            raise ApiHTTPError.from_request_error(
                RequestError(400, "Organization is not in an infra-based pricing plan")
            )
        try:
            subscription_costs = await OrbService.get_subscription_costs(
                organization, timeframe_end=timeframe_end, timeframe_start=timeframe_start
            )
            self.write_json(subscription_costs.to_dict())
        except (OrbCustomerNotFound, OrbSubscriptionNotFound) as e:
            logging.warning(f"Error getting subscription costs: {e}")
            raise ApiHTTPError.from_request_error(RequestError(404, str(e))) from e
        except Exception as e:
            logging.error(f"Error getting subscription costs: {e}")
            raise ApiHTTPError.from_request_error(RequestError(500, str(e))) from e


class APIBillingOrganizationsInvoicesHandler(BaseHandler):
    @user_authenticated
    async def get(self, organization_id: str) -> None:
        organization = self._get_safe_organization(organization_id)

        if not (organization.in_dedicated_infra_pricing or organization.in_shared_infra_pricing):
            raise tornado.web.HTTPError(400, "Organization not in an infra-based pricing plan")

        try:
            response = await OrbService.get_organization_invoices(organization)
            invoices = [
                {
                    "id": invoice.id,
                    "status": invoice.status,
                    "total": invoice.total,
                    "amount_due": invoice.amount_due,
                    "subtotal": invoice.subtotal,
                    "currency": invoice.currency,
                    "issued_at": self.optional_date_to_str(invoice.issued_at),
                    "scheduled_issue_at": self.optional_date_to_str(invoice.scheduled_issue_at),
                    "invoice_date": invoice.invoice_date.isoformat(),
                    "due_date": invoice.due_date.isoformat(),
                    "hosted_invoice_url": invoice.hosted_invoice_url,
                    "invoice_pdf": invoice.invoice_pdf,
                    "invoice_number": invoice.invoice_number,
                }
                for invoice in response
            ]

            self.write_json({"data": invoices})
        except OrbCustomerNotFound as e:
            raise ApiHTTPError(404, f"Orb customer not found for Organization {organization.id}. Error: {e}")
        except OrbAPIException as e:
            raise ApiHTTPError(502, str(e))
        except Exception as e:
            raise ApiHTTPError(500, str(e))


def handlers():
    return [
        url(r"/v0/billing/(.+)/plan-limits/?", APIBillingPlanLimitsHandler),
        url(r"/v0/billing/(.+)/portal-session/?", APIBillingStripePortal),
        url(r"/v0/billing/(.+)/stats/?", APIBillinStatsHandler),
        url(r"/v0/billing/(.+)/upgrade/?", APIBillingUpgradeInfoHandler),
        url(r"/v1/billing/(.+)/plans/?", APIBillingOrganizationSharedPlansInfoHandler),
        url(r"/v0/billing/(.+)/intent/?", APIBillingSetupIntentHandler),
        url(r"/v0/billing/(.+)/payment/?", APIBillingPaymentHandler),
        url(r"/v1/billing/(.+)/payment/?", APIBillingOrganizationPaymentHandler),
        url(r"/v0/billing/(.+)/customer/?", APIBillingCustomerHandler),
        url(r"/v0/billing/(.+)/subscription/?", APIBillingSubscriptionHandler),
        url(r"/v1/billing/(.+)/subscription/?", APIBillingOrganizationSubscriptionHandler),
        url(r"/v1/billing/(.+)/subscription/cancel?", APIBillingSubscriptionCancellationHandler),
        url(r"/v1/billing/(.+)/subscription/change?", APIBillingOrganizationSubscriptionChangeHandler),
        url(
            r"/v1/billing/(.+)/subscription/current_billing_cycle_usage?",
            APIBillingOrganizationSubscriptionCurrentUsageHandler,
        ),
        url(r"/v1/billing/(.+)/subscription/costs/?", APIBillingSubscriptionCostsHandler),
        url(r"/v0/billing/(.+)/charges/?", APIBillingChargesHandler),
        url(r"/v0/billing/(.+)/invoices/?", APIBillingInvoicesHandler),
        url(r"/v1/billing/(.+)/invoices/?", APIBillingOrganizationsInvoicesHandler),
        url(r"/v0/billing/coupon/?", APIBillingCouponHandler),
        url(r"/v0/billing/(.+)/?", APIBillingHandler),
        url(r"/v1/billing/(.+)/?", APIBillingOrganizationHandler),
    ]
