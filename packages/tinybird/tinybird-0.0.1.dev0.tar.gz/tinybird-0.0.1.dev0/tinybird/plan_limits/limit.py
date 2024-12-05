from typing import Any, Dict, Optional

from tinybird.constants import BILLING_PLANS
from tinybird.user import User as Workspace


class PlanBasedLimit:
    """
    >>> limit = PlanBasedLimit("plan_based_limit", "plan_based_limit_description", {"custom": 1, "pro": 1, "tinybird": 1, "enterprise": 1, "branch_enterprise": 1, "dev": 1})
    >>> (limit.name, limit.description, limit.limits)
    ('plan_based_limit', 'plan_based_limit_description', {'custom': 1, 'pro': 1, 'tinybird': 1, 'enterprise': 1, 'branch_enterprise': 1, 'dev': 1})
    >>> PlanBasedLimit("")
    Traceback (most recent call last):
    ...
    Exception: PlanBasedLimit: Plan-based limit name is not provided
    >>> PlanBasedLimit(name="plan_based_limit", description="")
    Traceback (most recent call last):
    ...
    Exception: PlanBasedLimit: Plan-based limit description is not provided
    >>> PlanBasedLimit(name="plan_based_limit", description="plan_based_limit_desc")
    Traceback (most recent call last):
    ...
    Exception: PlanBasedLimit: Missing plan limits for ['branch_enterprise', 'custom', 'dev', 'enterprise', 'pro', 'tinybird']
    >>> PlanBasedLimit(name="plan_based_limit", description="plan_based_limit_description", limits={"custom": 1, "pro": 1, "enterprise": 1, "branch_enterprise": 1, "dev": 1, "non_defined_plan": 1})
    Traceback (most recent call last):
    ...
    Exception: PlanBasedLimit: Missing plan limits for ['tinybird']
    """

    name: str = ""
    description: str = ""
    prefix: str = ""
    limits: Dict[str, int] = {}
    limit_dependencies: Dict[str, Any] = {}

    def __init__(
        self,
        name: str = "",
        description: str = "",
        limits: Optional[Dict] = None,
        limit_dependencies: Optional[Dict] = None,
        prefix: str = "",
    ):
        # Fallback for limit properties in case
        # class inheritance is not used
        self.name = name if name else self.name
        self.description = description if description else self.description
        self.prefix = prefix if prefix else self.prefix
        self.limits = dict(limits if limits else self.limits)
        self.limit_dependencies = dict(limit_dependencies if limit_dependencies else self.limit_dependencies)

        self._check_limit_definition()

    def get_limit_for(self, workspace: Workspace) -> int:
        # Current plan-based limits need a workaround
        # for workspaces with versions. Branches have
        # DEV price plan and limits are much lower than expected.
        # copy and sinks limits are inherited from the main workspace otherwise branch creation might fail
        if self.prefix and self.prefix in ["copy", "sinks"]:
            workspace_main = workspace.get_main_workspace()
        else:
            workspace_main = Workspace.get_by_id(workspace.origin) if workspace.origin else workspace

        limit_name = self.name
        workspace_plan = workspace_main.plan
        workspace_has_limit_property = hasattr(workspace_main, limit_name)
        current_limit = None

        if self.prefix:
            # Get Limit from Cheriff for Workspace or default from plan
            current_limit = workspace_main.get_limits(self.prefix).get(self.name, self.limits.get(workspace_plan))
        elif workspace_has_limit_property and isinstance(workspace_main[limit_name], int):
            # Get limit from Workspace property
            current_limit = workspace_main[limit_name]
        else:
            # Get default limit for workspace plan
            current_limit = self.limits.get(workspace_plan, 0)

        if self.has_custom_compute_function:
            self.compute_limit(workspace_main, current_limit, self.limit_dependencies)

        return current_limit

    def has_reached_limit_in(self, limit: int, extra_params: Dict[str, Any]) -> bool:
        raise NotImplementedError("Method has_reached_limit_in has not been implemented")

    def compute_limit(self, workspace: Workspace, default_limit: int, limit_dependencies: Dict[str, Any]):
        raise NotImplementedError("Method compute_limit has not been implemented")

    def _check_limit_definition(self):
        class_name = self.__class__.__name__

        if not self.name or not isinstance(self.name, str):
            raise Exception(f"{class_name}: Plan-based limit name is not provided")

        if not self.description or not isinstance(self.description, str):
            raise Exception(f"{class_name}: Plan-based limit description is not provided")

        defined_plan_limits = self.limits.keys()
        missing_plans = BILLING_PLANS - defined_plan_limits

        if len(missing_plans):
            missing_plans_list = sorted(list(missing_plans))
            raise Exception(f"{class_name}: Missing plan limits for {missing_plans_list}")

        # Check if limit has own compute limit function
        self.has_custom_compute_function = type(self).compute_limit != PlanBasedLimit.compute_limit
