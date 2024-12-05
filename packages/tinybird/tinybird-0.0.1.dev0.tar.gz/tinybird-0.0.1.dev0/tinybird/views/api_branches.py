import json
import logging
import re
from asyncio import sleep as sleep_async
from dataclasses import asdict
from typing import Any, Dict, List, Optional, TypedDict

from tornado.escape import json_decode
from tornado.web import url

from tinybird.constants import CHCluster
from tinybird.git_settings import GitHubSettings
from tinybird.iterating.compare import Compare
from tinybird.iterating.data_branch import (
    DATA_BRANCH_MODES,
    DataBranchConflictError,
    DataBranchJob,
    DataBranchMode,
    new_data_branch_job,
)
from tinybird.iterating.regression import RegressionTestError, RegressionTestsCommand, new_regression_tests_job
from tinybird.job import JobExecutor
from tinybird.limits import Limit
from tinybird.plans import PlansService
from tinybird.tokens import scopes
from tinybird.tracing import ClickhouseTracer
from tinybird.user import User as Workspace
from tinybird.user import UserAccount, UserDoesNotExist, WorkspaceException
from tinybird.user import Users as Workspaces
from tinybird.views.aiohttp_shared_session import get_shared_session
from tinybird.views.base import check_rate_limit
from tinybird.views.git_integrations.github import GitHubInterface, GitHubWorkspaceSettings

from ..workspace_service import CreateBranchResourceError
from .api_errors.branches import (
    BranchesClientErrorBadRequest,
    BranchesClientErrorForbidden,
    BranchesServerErrorInternal,
)
from .api_errors.workspaces import WorkspacesClientRemoteError
from .api_workspaces import APIWorkspaceCreationBaseHandler, BaseBranchHandler
from .base import ApiHTTPError, authenticated, with_scope_admin, with_scope_admin_user


class CreateBranchErrors(TypedDict):
    datasources: List[CreateBranchResourceError]
    pipes: List[CreateBranchResourceError]
    tokens: List[CreateBranchResourceError]


class APIBranchCreationHandler(BaseBranchHandler, APIWorkspaceCreationBaseHandler):
    async def validate_remote_branch_creation(self, workspace: Workspace, branch: str):
        self.check_versions_ga_is_enabled(workspace)
        if not workspace.remote.get("provider"):
            error = WorkspacesClientRemoteError.not_connected()
            raise ApiHTTPError.from_request_error(error)

    async def create_remote_branch(self, workspace: Workspace, branch_name: str):
        try:
            github_workspace_settings = GitHubWorkspaceSettings(
                owner=workspace.remote.get("owner", ""),
                access_token=workspace.remote.get("access_token", ""),
                remote=workspace.remote.get("remote", ""),
                branch=workspace.remote.get("branch", ""),
                project_path=workspace.remote.get("project_path", ""),
            )
        except Exception as e:
            raise ApiHTTPError(400, str(e))

        try:
            session = get_shared_session()

            await GitHubInterface.create_branch(
                github_settings=github_workspace_settings,
                session=session,
                base_branch=workspace.remote.get("branch"),
                target_branch=branch_name,
            )
        except Exception as e:
            raise ApiHTTPError(422, str(e))

    @authenticated
    @with_scope_admin
    @check_rate_limit(Limit.api_branches_create)
    async def post(self):
        branch_name: Optional[str] = self.get_argument("name", None)
        if not branch_name:
            error = BranchesClientErrorBadRequest.no_branch_name()
            raise ApiHTTPError.from_request_error(error)

        data_branch_mode: Optional[str] = self.get_argument("data", None)
        validate_data_branch_modes(data_branch_mode, required=False)

        workspace: Workspace = self.get_workspace_from_db()
        if workspace.is_branch:
            error = BranchesClientErrorBadRequest.create_from_branch_not_allowed(name=workspace.name)
            raise ApiHTTPError.from_request_error(error)

        branches = await workspace.get_branches()
        if len(branches) >= workspace.get_limits(prefix="iterating").get(
            "iterating_max_branches", Limit.iterating_max_branches
        ):
            error = BranchesClientErrorBadRequest.max_number_of_branches(name=workspace.name)
            raise ApiHTTPError.from_request_error(error)

        ignore_datasources: Optional[List[str]] = (
            self.get_argument("ignore_datasources").split(",")
            if self.get_argument("ignore_datasources", None)
            else None
        )

        info = workspace.get_workspace_info()
        user_creating_it = UserAccount.get_by_id(info["owner"])
        if not user_creating_it:
            raise ApiHTTPError(404, f"User {info['owner']} not found")

        workspace = Workspaces.get_by_id(workspace.id)

        branch_cluster = (
            CHCluster(name=workspace.cluster, server_url=workspace.database_server) if workspace.cluster else None
        )
        branch_workspace = await self._register_workspace(
            user_creating_it=user_creating_it, name=branch_name, origin=workspace, cluster=branch_cluster
        )
        if self.get_argument("create_remote_branch", "false").lower() == "true":
            try:
                await self.validate_remote_branch_creation(workspace, branch_name)
                await self.create_remote_branch(workspace, branch_name)
            except Exception as exc:
                await UserAccount.delete_workspace(
                    None, branch_workspace, hard_delete=True, job_executor=self.application.job_executor
                )
                raise exc

        result: Dict[str, Any] = await data_branch(
            self.application.job_executor,
            branch_workspace,
            data_branch_mode,
            workspace,
            True,
            ignore_datasources,
            api_host=self.application.settings["api_host"],
        )

        # HACK: Please, let's try to Remove this ASAP
        is_legacy: bool = False

        try:
            cli_version: str = self.get_argument("cli_version", "")
            if cli_version:
                m: Optional[re.Match] = re.match(r"1\.0\.0b(\d+)", cli_version)
                if m:
                    version: int = int(m.group(1))
                    is_legacy = version < 428  # CLI version at the time of release
        except Exception as e:
            logging.warning(f"Error parsing cli_version='{cli_version}': {e}")

        # Legacy CLI versions expect the job info when ALL_PARTITIONS
        # and the complete result else.
        if is_legacy and data_branch_mode != DataBranchMode.ALL_PARTITIONS.value:
            job_id: str = result["job"]["id"]
            backoff_time: float = 0.1

            while True:
                # If we reach this stage, we probably have a problem.
                # Let's return the job info anyway.
                if backoff_time > 60:
                    break

                job: Optional[DataBranchJob] = DataBranchJob.get_by_id(job_id)
                if not job:
                    break

                if job.status in ("done", "error"):
                    result = job.result
                    break

                await sleep_async(backoff_time)
                backoff_time = backoff_time * 2

        # Make sure we update the remote properly using the new branch
        origin_remote = dict(workspace.remote)

        remote_settings = GitHubSettings(
            provider=origin_remote.get("provider"),
            owner=origin_remote.get("owner"),
            owner_type=origin_remote.get("owner_type"),
            remote=origin_remote.get("remote"),
            access_token=origin_remote.get("access_token"),
            branch=branch_name,
            project_path=origin_remote.get("project_path"),
        )

        await Workspaces.update_remote(branch_workspace, remote=remote_settings)
        self.write_json(result)

    @authenticated
    @with_scope_admin
    async def get(self) -> None:
        workspace = self.get_workspace_from_db()
        if workspace.is_branch:
            self.write_json({"environments": []})
            return

        if workspace.is_release:
            workspace = workspace.get_main_workspace()

        branches = await workspace.get_branches()
        self.write_json({"environments": branches})


class APIBranchHandler(BaseBranchHandler):
    @authenticated
    @with_scope_admin
    async def get(self, branch_id_or_name):
        """
        Get branch info
        """

        with_token = self.get_argument("with_token", "false") == "true"
        branch = self.get_branch(branch_id_or_name)

        response = branch.to_json(with_token=with_token)
        self.write_json(response)

    @authenticated
    @with_scope_admin
    @check_rate_limit(Limit.api_branches_delete)
    async def delete(self, branch_id_or_name):
        workspace: Workspace = self.get_workspace_from_db()
        if workspace.is_branch and branch_id_or_name not in [workspace.id, workspace.name]:
            error = BranchesClientErrorBadRequest.delete_from_another_not_allowed(name=workspace.name, hint="main")
            raise ApiHTTPError.from_request_error(error)
        branch = self.get_branch(branch_id_or_name)

        try:
            await PlansService.cancel_subscription(branch)
            info = branch.get_workspace_info()
            owner = UserAccount.get_by_id(info["owner"])
            tracer: ClickhouseTracer = self.application.settings["opentracing_tracing"].tracer

            await UserAccount.delete_workspace(
                owner, branch, hard_delete=True, job_executor=self.application.job_executor, tracer=tracer
            )
        except WorkspaceException as e:
            error = BranchesClientErrorForbidden.no_branch_deletion_allowed(error=str(e))
            raise ApiHTTPError.from_request_error(error)
        except Exception as e:
            logging.exception(e)
            error = BranchesServerErrorInternal.failed_delete(name=branch.name, error=str(e))
            raise ApiHTTPError.from_request_error(error)

        self.write_json({"result": "Branch deleted"})


class APIBranchData(BaseBranchHandler):
    def check_xsrf_cookie(self):
        pass

    @authenticated
    @with_scope_admin
    @check_rate_limit(Limit.api_branches_data)
    async def post(self, branch_id_or_name):
        """
        Iterating MSP, this method is for experimentation purposes
        """
        data_branch_mode = self.get_argument("mode", None)
        ignore_datasources: Optional[List[str]] = (
            self.get_argument("ignore_datasources").split(",")
            if self.get_argument("ignore_datasources", None)
            else None
        )
        validate_data_branch_modes(data_branch_mode)
        try:
            branch_workspace = self.get_branch(branch_id_or_name)
            origin_workspace_id = branch_workspace.origin

            if not origin_workspace_id:
                raise ApiHTTPError(400, "Make sure the Workspace is a Branch")

            try:
                origin_workspace = Workspaces.get_by_id(origin_workspace_id)
            except UserDoesNotExist:
                raise ApiHTTPError(
                    400,
                    f"There is no Workspace with ID `{origin_workspace_id}`, please send a valid Workspace ID or make sure the Workspace is not Main",
                )
            attach_response = await data_branch(
                self.application.job_executor,
                branch_workspace,
                data_branch_mode,
                origin_workspace,
                False,
                ignore_datasources,
                api_host=self.application.settings["api_host"],
            )

            self.write_json(attach_response)
        except DataBranchConflictError as e:
            raise ApiHTTPError(409, str(e))
        except Exception as e:
            logging.exception(e)
            raise ApiHTTPError(500, f"Error copying data: {str(e)}")


async def data_branch(
    job_executor: JobExecutor,
    branch_workspace: Workspace,
    data_branch_mode: Optional[str],
    origin_workspace: Workspace,
    clone_resources: bool,
    ignore_datasources: Optional[List[str]],
    api_host: str,
) -> Dict[str, Any]:
    branch_workspace = Workspace.get_by_id(branch_workspace.id)
    origin_workspace = Workspace.get_by_id(origin_workspace.id)

    job = new_data_branch_job(
        job_executor, origin_workspace, branch_workspace, clone_resources, data_branch_mode, ignore_datasources
    )
    result = {"job": job.to_json(), "workspace": {"id": branch_workspace.id}}
    result["job"]["job_url"] = f"{api_host}/v0/jobs/{job.id}"
    return result


def validate_data_branch_modes(data_branch_mode: Optional[str], required=True) -> None:
    if data_branch_mode and data_branch_mode == DataBranchMode.ALL_PARTITIONS.value:
        raise ApiHTTPError(403, "`all_partitions` is disabled")

    if not data_branch_mode and required:
        raise ApiHTTPError(400, f'`mode` argument is required, available modes: {", ".join(DATA_BRANCH_MODES)}')

    if data_branch_mode and data_branch_mode not in DATA_BRANCH_MODES:
        raise ApiHTTPError(400, f'`mode` argument is not valid, available modes: {", ".join(DATA_BRANCH_MODES)}')


class APIBranchDiff(BaseBranchHandler):
    @authenticated
    @with_scope_admin
    async def get(self, branch_id_or_name):
        """
        Get branch diff
        """
        branch = self.get_branch(branch_id_or_name)
        compare_response = await Compare().env_to_prod(branch)
        if compare_response.outdated:
            self.write_json({"error": f"Branch '{branch.name}' outdated from 'main'"})
        else:
            self.write_json(asdict(compare_response.diff))


class APIBranchPipeRegression(BaseBranchHandler):
    def prepare(self):
        self.regression_commands = []
        if self.request.headers.get("Content-Type", None) == "application/json":
            try:
                self.regression_commands = json_decode(self.request.body)
            except json.JSONDecodeError as e:
                raise ApiHTTPError(400, f"invalid JSON line {e.lineno}, column {e.colno}: {e.msg}")

    def build_regression_commands(self) -> List[RegressionTestsCommand]:
        try:
            return [RegressionTestsCommand.from_dict(command) for command in self.regression_commands]
        except RegressionTestError as e:
            raise ApiHTTPError(400, f"Incorrect regression tests request: {e}")

        except Exception as e:
            logging.exception(f"Error building regression commands {e}")
            raise ApiHTTPError(500, "Unexpected error validating regression test request")

    @authenticated
    @with_scope_admin_user
    async def post(self, branch_id_or_name: str):
        """
        Branch regression tests
        """
        branch = self.get_branch(branch_id_or_name)
        api_host = self.application.settings["api_host"]
        job_executor = self.application.job_executor

        resources = self.get_resources_for_scope(scopes.ADMIN_USER)
        user_account = UserAccount.get_by_id(resources[0])
        commands = self.build_regression_commands()
        job = self.create_job(job_executor, branch, user_account, api_host, commands)
        response = {"job": job.to_json()}
        response["job"]["job_url"] = api_host + "/v0/jobs/" + job.id
        self.write_json(response)

    def create_job(self, job_executor, branch, user_account, api_host, commands):
        return new_regression_tests_job(job_executor, branch, user_account, api_host, commands)


class APIBranchPipeRegressionMain(APIBranchPipeRegression):
    def create_job(self, job_executor, branch, user_account, api_host, commands):
        return new_regression_tests_job(job_executor, branch, user_account, api_host, commands, True)


def handlers():
    return [
        url(r"/v0/environments/(.+)/regression", APIBranchPipeRegression),
        url(r"/v0/environments/(.+)/regression/main", APIBranchPipeRegressionMain),
        url(r"/v0/environments/(.+)/diff/?", APIBranchDiff),
        url(r"/v0/environments/(.+)/data/?", APIBranchData),
        url(r"/v0/environments/(.+)/?", APIBranchHandler),
        url(r"/v0/environments/?", APIBranchCreationHandler),
    ]
