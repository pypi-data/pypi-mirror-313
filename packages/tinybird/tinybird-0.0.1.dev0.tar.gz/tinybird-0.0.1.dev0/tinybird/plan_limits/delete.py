from typing import Any, Dict

# Needed to import this way to bypass circular dependencies
import tinybird.job as Jobs
from tinybird.constants import BillingPlans
from tinybird.plan_limits.limit import PlanBasedLimit


class MaxActiveDeleteJobsLimit(PlanBasedLimit):
    name: str = "delete_max_jobs"
    description: str = "Max number of active delete jobs (running or queued) per workspace"
    prefix: str = "delete"
    limits: Dict[str, int] = {
        BillingPlans.DEV: 1,
        BillingPlans.PRO: 3,
        BillingPlans.TINYBIRD: 3,
        BillingPlans.ENTERPRISE: 6,
        BillingPlans.BRANCH_ENTERPRISE: 6,
        BillingPlans.CUSTOM: 6,
    }

    def has_reached_limit_in(self, limit: int, extra_params: Dict[str, Any]) -> bool:
        workspace = extra_params["workspace"]
        workspace_delete_active_jobs = [
            job
            for job in Jobs.DeleteJob.get_all_by_owner(workspace.id)
            if job.status in {Jobs.JobStatus.WAITING, Jobs.JobStatus.WORKING} and job.kind == Jobs.JobKind.DELETE_DATA
        ]

        return len(workspace_delete_active_jobs) >= limit


class DeleteLimits:
    max_active_delete_jobs = MaxActiveDeleteJobsLimit()
