from typing import Any, Dict

from tinybird.constants import BillingPlans
from tinybird.plan_limits.limit import PlanBasedLimit


class MaxRowLimit(PlanBasedLimit):
    name: str = "cdk_max_row_limit"
    description: str = "Max number of rows for connecting an external data source, per workspace"
    prefix: str = "cdk"
    limits: Dict[str, int] = {
        BillingPlans.DEV: 50_000_000,
        BillingPlans.PRO: 50_000_000,
        BillingPlans.TINYBIRD: 50_000_000,
        BillingPlans.ENTERPRISE: 50_000_000,
        BillingPlans.BRANCH_ENTERPRISE: 50_000_000,
        BillingPlans.CUSTOM: 50_000_000,
    }

    def has_reached_limit_in(self, limit: int, extra_params: Dict[str, Any]) -> bool:
        return extra_params["rows"] > limit


class CDKLimits:
    max_row_limit = MaxRowLimit()
