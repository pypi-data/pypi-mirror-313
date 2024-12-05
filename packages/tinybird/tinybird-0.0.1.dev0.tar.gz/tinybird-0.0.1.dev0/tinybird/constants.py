from dataclasses import dataclass

from tinybird.ch_utils import constants
from tinybird.datatypes import nullable_types
from tinybird.sql_template import function_list, parameter_types


class BillingPlans:
    DEV = "dev"
    PRO = "pro"
    ENTERPRISE = "enterprise"
    BRANCH_ENTERPRISE = "branch_enterprise"
    TINYBIRD = "tinybird"  # TODO pending to be defined: would be some kind of free plan for the Internal WS or @tinybird workspaces with no limits and free usage.
    CUSTOM = (
        "custom"  # TODO pending to be defined: would be used for old clients that doesn't match the enterprise plan.
    )


BILLING_PLANS = {
    BillingPlans.DEV,
    BillingPlans.PRO,
    BillingPlans.ENTERPRISE,
    BillingPlans.BRANCH_ENTERPRISE,
    BillingPlans.TINYBIRD,
    BillingPlans.CUSTOM,
}


class StripePrices:
    PRO_STORAGE = "pro_plan_storage_base"
    PRO_PROCESSED = "pro_plan_processed_base"


class BillingTypes:
    STORAGE = "storage"
    PROCESSED = "processed"
    TRANSFERRED_INTER = "transferred_inter"
    TRANSFERRED_INTRA = "transferred_intra"


class StripeEvents:
    SUBSCRIPTION_DELETED = "customer.subscription.deleted"
    SUBSCRIPTION_CREATED = "customer.subscription.created"
    SUBSCRIPTION_UPDATED = "customer.subscription.updated"


@dataclass
class CHCluster:
    name: str
    server_url: str


class Relationships:
    ADMIN = "admin"
    GUEST = "guest"
    VIEWER = "viewer"


user_workspace_relationships = [Relationships.ADMIN, Relationships.GUEST, Relationships.VIEWER]


class Notifications:
    INGESTION_ERRORS = "ingestion_errors"


USER_WORKSPACE_NOTIFICATIONS = [Notifications.INGESTION_ERRORS]


class Incidents:
    ERROR = "incidents"
    QUARANTINE = "quarantine"


INCIDENT_TYPES = [Incidents.ERROR, Incidents.QUARANTINE]


ALLOWED_WORDS = ["numbers", "values", "zeros", "materialized", "totals"]
ALL_WORDS = list(
    {
        x.lower()
        for x in set(
            list(constants.ENABLED_TABLE_FUNCTIONS)
            + list(constants.ENABLED_SYSTEM_TABLES)
            + list(constants.RESERVED_DATABASE_NAMES)
            + list(constants.FORBIDDEN_SQL_KEYWORDS)
            + nullable_types
            + parameter_types
            + list(function_list.keys())
        )
    }
)
FORBIDDEN_WORDS = list(filter(lambda x: x not in ALLOWED_WORDS, ALL_WORDS))

WORKSPACE_COLORS = [
    "#f94144",
    "#f3722c",
    "#f8961e",
    "#f9844a",
    "#f9c74f",
    "#90be6d",
    "#43aa8b",
    "#4d908e",
    "#577590",
    "#277da1",
]

# This list of bootstrap_server and server_group pairs stablish a match between user's bootstrap servers to our internal server_groups
# This can be override via Cheriff per-linker
# Defaults to "tbakafka" which is the shared server_group
KAFKA_BOOTSTRAP_SERVER_TO_SERVER_GROUP = [
    {
        "bootstrap_server": "p547qg.us-east-1.aws.confluent.cloud",
        "server_group": "fanduel",
    }
]

MATVIEW_BACKFILL_VALUE_WAIT = 30


class ExecutionTypes:
    MANUAL = "manual"
    SCHEDULED = "scheduled"
