from math import ceil
from typing import Any, Dict

from croniter import croniter

from tinybird.constants import BillingPlans
from tinybird.data_connector import DataSink
from tinybird.pipe import PipeTypes
from tinybird.plan_limits.limit import PlanBasedLimit
from tinybird.user import User as Workspace


class MaxActiveCopyJobsLimit(PlanBasedLimit):
    name: str = "copy_max_jobs"
    description: str = "Max number of active jobs (running or queued) per workspace"
    prefix: str = "copy"
    limits: Dict[str, int] = {
        BillingPlans.DEV: 1,
        BillingPlans.PRO: 3,
        BillingPlans.TINYBIRD: 3,
        BillingPlans.ENTERPRISE: 6,
        BillingPlans.BRANCH_ENTERPRISE: 6,
        BillingPlans.CUSTOM: 6,
    }

    def has_reached_limit_in(self, limit: int, extra_params: Dict[str, Any]) -> bool:
        from tinybird.copy_pipes.job import CopyJob  # Avoid circular dependency
        from tinybird.job import JobKind, JobStatus

        workspace = extra_params["workspace"]
        workspace_copy_active_jobs = [
            job
            for job in CopyJob.get_all_by_owner(workspace.id)
            if job.status in {JobStatus.WAITING, JobStatus.WORKING} and job.kind == JobKind.COPY
        ]

        return len(workspace_copy_active_jobs) >= limit


class MinPeriodBetweenCopyJobs(PlanBasedLimit):
    name: str = "copy_min_period_jobs"
    description: str = "Min. period for scheduling copy jobs. Minimum number of seconds allowed between scheduled jobs."
    prefix: str = "copy"
    limits: Dict[str, int] = {
        BillingPlans.DEV: 3600,
        BillingPlans.PRO: 600,
        BillingPlans.TINYBIRD: 600,
        BillingPlans.ENTERPRISE: 60,
        BillingPlans.BRANCH_ENTERPRISE: 60,
        BillingPlans.CUSTOM: 60,
    }

    def has_reached_limit_in(self, limit: int, extra_params: Dict[str, Any]) -> bool:
        execution_pairs = self._get_next_5_executions(extra_params["schedule_cron"])
        min_difference = min(abs(last - first) for first, last in execution_pairs)

        # Check if minimum difference between executions goes over workspace limit
        return int(min_difference) < limit

    def get_error_message_params(self, limit: int) -> Dict[str, Any]:
        return {"cron_schedule_limit": limit, "cron_recommendation": self._get_recommended_cron(limit)}

    @staticmethod
    def _get_next_5_executions(cron_schedule: str) -> list:
        job_cron_schedule = croniter(cron_schedule)
        next_executions = [
            job_cron_schedule.next(),
            job_cron_schedule.next(),
            job_cron_schedule.next(),
            job_cron_schedule.next(),
            job_cron_schedule.next(),
        ]
        return [(next_executions[i], next_executions[i + 1]) for i in range(4)]

    @staticmethod
    def _get_recommended_cron(workspace_limit: int) -> str:
        period_in_minutes = ceil(workspace_limit / 60)

        if 1 < period_in_minutes < 60:
            return f"*/{period_in_minutes} * * * *"

        if period_in_minutes == 1:
            return "* * * * *"

        period_in_hours = ceil(workspace_limit / 3600)
        return f"0 */{period_in_hours} * * *"


class MaxExecutionTimeCopyJobs(PlanBasedLimit):
    name: str = "copy_max_execution_time"
    description: str = (
        "Maximum execution time for queries within copy jobs. For Atomic Copy Jobs, this limit will apply to individual"
        " INSERT INTO queries."
    )
    prefix: str = "copy"
    limits: Dict[str, int] = {
        BillingPlans.DEV: 20,
        BillingPlans.PRO: 30,
        BillingPlans.TINYBIRD: 30,
        BillingPlans.ENTERPRISE: 1800,
        BillingPlans.BRANCH_ENTERPRISE: 1800,
        BillingPlans.CUSTOM: 1800,
    }

    def get_limit_for(self, workspace: Workspace, job=None) -> int:
        if (workspace.plan == BillingPlans.ENTERPRISE or workspace.plan == BillingPlans.CUSTOM) and job is not None:
            max_workspace_execution_time = super().get_limit_for(workspace)

            # Always return workspace_execution_time if differs from the
            # defined limit for the plan. This way we'll return the overriden one.
            if max_workspace_execution_time != self.limits.get(workspace.plan):
                return max_workspace_execution_time

            cron_period = self._get_cron_execution_period(pipe_id=job.pipe_id, workspace_id=workspace.id)
            if cron_period:
                # Half of the cron job period in seconds
                half_cron_period = int(cron_period / 2)
                return min(half_cron_period, max_workspace_execution_time)
            else:
                return max_workspace_execution_time

        return super().get_limit_for(workspace)

    @staticmethod
    def _get_cron_execution_period(pipe_id: str, workspace_id: str):
        try:
            data_sink = DataSink.get_by_resource_id(pipe_id, workspace_id)
            cron_expression = data_sink.settings.get("cron", "")
            schedule_cron = croniter(cron_expression)

            first_execution, second_execution = schedule_cron.next(), schedule_cron.next()

            return abs(second_execution - first_execution)
        except Exception:
            return False


class MaxCopyPipes(PlanBasedLimit):
    name = "copy_max_pipes"
    description = "Maximum number of copy pipes per workspace."
    prefix = "copy"
    limits: Dict[str, int] = {
        BillingPlans.DEV: 1,
        BillingPlans.PRO: 3,
        BillingPlans.TINYBIRD: 3,
        BillingPlans.ENTERPRISE: 10,
        BillingPlans.BRANCH_ENTERPRISE: 10,
        BillingPlans.CUSTOM: 10,
    }

    def has_reached_limit_in(self, limit: int, extra_params: Dict[str, Any]) -> bool:
        pipes = extra_params["workspace"].get_pipes()
        workspace_copy_active_pipes = [
            pipe for pipe in pipes if pipe.pipe_type == PipeTypes.COPY or pipe.copy_node is not None
        ]

        return len(workspace_copy_active_pipes) >= limit


class CopyLimits:
    max_active_copy_jobs = MaxActiveCopyJobsLimit()
    min_period_between_copy_jobs = MinPeriodBetweenCopyJobs()
    max_job_execution_time = MaxExecutionTimeCopyJobs()
    max_copy_pipes = MaxCopyPipes()


class BranchCopyLimits(CopyLimits):
    pass
