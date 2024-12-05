import itertools
import math
from typing import Any

from croniter import croniter

from tinybird.constants import BillingPlans
from tinybird.datafile import PipeTypes
from tinybird.plan_limits.limit import PlanBasedLimit
from tinybird.user import User as Workspace


class MaxSinkPipes(PlanBasedLimit):
    name = "sinks_max_pipes"
    description = "Maximum number of sink pipes allowed per workspace."
    prefix = "sinks"
    limits = {
        BillingPlans.DEV: 0,
        BillingPlans.PRO: 3,
        BillingPlans.TINYBIRD: 3,
        BillingPlans.ENTERPRISE: 10,
        BillingPlans.BRANCH_ENTERPRISE: 10,
        BillingPlans.CUSTOM: 10,
    }

    def _has_reached_limit_in(self, limit: int, extra_params: dict[str, Any]) -> bool:
        pipes = extra_params["workspace"].get_pipes()
        sink_pipes = [pipe for pipe in pipes if pipe.pipe_type == PipeTypes.DATA_SINK]

        return len(sink_pipes) >= limit

    def is_limit_reached(self, workspace: Workspace) -> bool:
        max_pipes = self.get_limit_for(workspace)
        return self._has_reached_limit_in(max_pipes, {"workspace": workspace})


class MaxActiveSinkJobsLimit(PlanBasedLimit):
    name = "sinks_max_jobs"
    description = "Max number of active sink jobs (running or queued) per workspace"
    prefix = "sinks"
    limits = {
        BillingPlans.DEV: 0,
        BillingPlans.PRO: 3,
        BillingPlans.TINYBIRD: 3,
        BillingPlans.ENTERPRISE: 6,
        BillingPlans.BRANCH_ENTERPRISE: 6,
        BillingPlans.CUSTOM: 6,
    }

    def _has_reached_limit_in(self, limit: int, extra_params: dict[str, Any]) -> bool:
        from tinybird.data_sinks.job import DataSinkBaseJob  # Avoid circular dependency
        from tinybird.job import JobKind, JobStatus

        workspace = extra_params["workspace"]
        workspace_copy_active_jobs = [
            job
            for job in DataSinkBaseJob.get_all_by_owner(workspace.id, limit=400)
            if job.status in {JobStatus.WAITING, JobStatus.WORKING} and job.kind == JobKind.SINK
        ]

        return len(workspace_copy_active_jobs) >= limit

    def evaluate(self, workspace: Workspace) -> None:
        max_active_jobs = self.get_limit_for(workspace)
        if self._has_reached_limit_in(max_active_jobs, {"workspace": workspace}):
            raise MaxActiveSinkJobsLimitReached(max_active_jobs)


class MaxSinkJobExecutionTimeLimit(PlanBasedLimit):
    name: str = "sinks_max_execution_time"
    description: str = "Maximum execution time for queries within sink jobs."
    prefix: str = "sinks"
    limits: dict[str, int] = {
        BillingPlans.DEV: 20,
        BillingPlans.PRO: 30,
        BillingPlans.TINYBIRD: 30,
        BillingPlans.ENTERPRISE: 300,
        BillingPlans.BRANCH_ENTERPRISE: 300,
        BillingPlans.CUSTOM: 300,
    }


class MinPeriodBetweenScheduledSinkJobs(PlanBasedLimit):
    name: str = "sinks_min_period_jobs"
    description: str = "Min. period for scheduling sink jobs. Minimum number of seconds allowed between scheduled jobs."
    prefix: str = "sinks"
    limits: dict[str, int] = {
        BillingPlans.DEV: 3600,
        BillingPlans.PRO: 600,
        BillingPlans.TINYBIRD: 600,
        BillingPlans.ENTERPRISE: 60,
        BillingPlans.BRANCH_ENTERPRISE: 60,
        BillingPlans.CUSTOM: 60,
    }

    def evaluate(self, workspace: Workspace, cron: str) -> None:
        limit = self.get_limit_for(workspace)
        execution_pairs = self._get_next_5_executions(cron)
        min_difference = min(abs(last - first) for first, last in execution_pairs)
        if int(min_difference) < limit:
            err = SinkScheduleFrequencyLimitExceeded()
            err.add_note(f"Limit of {limit} seconds between sink jobs exceeded.")
            raise err

    def get_error_message_params(self, workspace: Workspace) -> dict[str, Any]:
        limit = self.get_limit_for(workspace)
        return {"cron_schedule_limit": limit, "cron_recommendation": self._get_recommended_cron(limit)}

    @staticmethod
    def _get_next_5_executions(cron_schedule: str) -> list[tuple[float, float]]:
        job_cron_schedule = croniter(cron_schedule)
        next_executions = (job_cron_schedule.next() for _ in range(5))
        return list(itertools.pairwise(next_executions))

    def has_reached_limit_in(self, limit: int, extra_params: dict[str, Any]) -> bool:
        executions = self._get_next_5_executions(extra_params["cron_schedule"])
        intervals = (last - first for first, last in executions)
        return min(intervals) < limit

    @staticmethod
    def _get_recommended_cron(workspace_limit: int) -> str:
        period_in_minutes = math.ceil(workspace_limit / 60)

        if 1 < period_in_minutes < 60:
            return f"*/{period_in_minutes} * * * *"

        if period_in_minutes == 1:
            return "* * * * *"

        period_in_hours = math.ceil(workspace_limit / 3600)
        return f"0 */{period_in_hours} * * *"


class SinkLimitReached(Exception):
    pass


class MaxActiveSinkJobsLimitReached(SinkLimitReached):
    def __init__(self, max_active_jobs: int):
        msg = f"You have reached the maximum number of sink jobs ({max_active_jobs})."
        super().__init__(msg)


class SinkScheduleFrequencyLimitExceeded(SinkLimitReached):
    pass


class SinkLimits:
    max_sink_pipes = MaxSinkPipes()
    max_active_jobs = MaxActiveSinkJobsLimit()
    max_execution_time = MaxSinkJobExecutionTimeLimit()
    max_scheduled_job_frequency = MinPeriodBetweenScheduledSinkJobs()
