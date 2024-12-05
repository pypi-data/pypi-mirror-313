import io
import logging
import os
import shutil
import tempfile
import uuid
import zipfile
from dataclasses import asdict
from typing import Any, Dict, List, Never, Optional

import orjson
from tornado.web import url

from tinybird.client import TinyB
from tinybird.config import VERSION
from tinybird.constants import CHCluster
from tinybird.datafile import folder_push
from tinybird.datasource import SharedDatasource
from tinybird.feature_flags import FeatureFlagsWorkspaceService, FeatureFlagWorkspaces
from tinybird.git_settings import AVAILABLE_GIT_PROVIDERS, GitHubSettings, SemverVersions
from tinybird.iterating.compare import Compare, CompareException, CompareExceptionNotFound
from tinybird.iterating.release import (
    DeleteRemoteException,
    MaxNumberOfReleasesReachedException,
    Release,
    ReleaseStatus,
)
from tinybird.limits import Limit
from tinybird.organization.organization import Organizations
from tinybird.token_scope import scopes
from tinybird.tracing import ClickhouseTracer
from tinybird.user_workspace import (
    UserWorkspaceNotificationsHandler,
    UserWorkspaceRelationship,
    UserWorkspaceRelationshipException,
    UserWorkspaceRelationships,
)
from tinybird.views.aiohttp_shared_session import get_shared_session
from tinybird.views.api_templates import AVAILABLE_TEMPLATES
from tinybird.views.base import INVALID_AUTH_MSG, requires_write_access
from tinybird.views.git_integrations.github import GitHubInterface, GitHubWorkspaceSettings

from ..organization.organization_service import Organization, OrganizationService
from ..user import (
    DataSourceNotFound,
    NameAlreadyTaken,
    PipeNotFound,
    ReleaseStatusException,
    UnreachableOrgCluster,
    UserAccount,
    UserAccounts,
    UserDoesNotExist,
    WorkspaceException,
    WorkspaceName,
    WorkspaceNameIsNotValid,
)
from ..user import User as Workspace
from ..user import Users as Workspaces
from ..workspace_service import MaxOwnedWorkspacesLimitReached, WorkspaceService
from .api_errors.branches import BranchesClientErrorBadRequest
from .api_errors.workspaces import (
    WorkspacesClientErrorBadRequest,
    WorkspacesClientErrorForbidden,
    WorkspacesClientErrorNotFound,
    WorkspacesClientRemoteError,
    WorkspacesServerErrorInternal,
)
from .base import (
    ApiHTTPError,
    BaseHandler,
    authenticated,
    is_workspace_admin,
    user_authenticated,
    user_or_workspace_authenticated,
    with_scope_admin,
)
from .login import UserViewBase, base_login
from .mailgun import MailgunService

valid_operations = ["add", "remove", "change_role", "change_notifications"]

STARTER_KIT_PARAMS = ["name", "starter_kit", "repository_url", "repository_branch", "root_directory"]


class BaseBranchHandler(BaseHandler):
    def check_xsrf_cookie(self) -> None:
        pass

    def check_versions_ga_is_enabled(self, workspace: Workspace) -> None:
        if not FeatureFlagsWorkspaceService.feature_for_id(
            FeatureFlagWorkspaces.VERSIONS_GA, "", workspace.feature_flags
        ):
            error = BranchesClientErrorBadRequest.remote_disabled()
            raise ApiHTTPError.from_request_error(error)

    def get_branch(self, branch_id_or_name: str, workspace: Optional[Workspace] = None) -> Workspace:
        branch: Optional[Workspace] = None
        main: Optional[Workspace] = None

        try:
            # both main and branch workspace can access
            main_or_branch: Workspace = workspace if workspace else self.get_workspace_from_db()
            if branch_id_or_name not in [main_or_branch.id, main_or_branch.name]:
                main = main_or_branch
                try:
                    branch = Workspaces.get_by_id_or_name(branch_id_or_name)
                except UserDoesNotExist:
                    branch = Workspace.get_by_name(f"{main.name}_{branch_id_or_name}")
            else:
                branch = main_or_branch

                assert isinstance(branch.origin, str)
                main = Workspaces.get_by_id(branch.origin)
        except (UserDoesNotExist, AssertionError):
            pass

        def raise_err() -> Never:
            error = BranchesClientErrorBadRequest.branch_not_found(name=branch_id_or_name)
            raise ApiHTTPError.from_request_error(error)

        if not branch or not main:
            raise_err()

        # Make sure is a proper branch
        if not branch.origin:
            raise_err()

        # Make sure `branch` comes from (or is) `main`
        if branch.id != main.id and branch.origin != main.id:
            raise_err()

        return branch


class APIWorkspaceCreationBaseHandler(UserViewBase):
    def check_xsrf_cookie(self):
        pass

    async def _register_workspace(
        self,
        user_creating_it: UserAccount,
        name: Optional[str],
        origin: Optional[Workspace] = None,
        cluster: Optional[CHCluster] = None,
    ) -> Workspace:
        if not name:
            error = WorkspacesClientErrorBadRequest.invalid_workspace_name()
            raise ApiHTTPError.from_request_error(error)

        try:
            workspace = await WorkspaceService.register_and_initialize_workspace(
                name=name,
                user_creating_it=user_creating_it,
                tracer=self.application.settings["opentracing_tracing"].tracer,
                origin=origin,
                cluster=cluster,
            )
        except NameAlreadyTaken as err:
            if origin:
                error = BranchesClientErrorBadRequest.name_already_taken(name=name, main_name=origin.name)
            else:
                error = WorkspacesClientErrorBadRequest.name_already_taken(name=err.name_taken)
            raise ApiHTTPError.from_request_error(error)

        except WorkspaceNameIsNotValid as validation_error:
            if origin:
                error = BranchesClientErrorBadRequest.name_is_not_valid(validation_error=str(validation_error))
            else:
                error = WorkspacesClientErrorBadRequest.name_is_not_valid(validation_error=str(validation_error))
            raise ApiHTTPError.from_request_error(error)

        except MaxOwnedWorkspacesLimitReached as err:
            raise ApiHTTPError.from_request_error(
                WorkspacesClientErrorBadRequest.max_owned_workspaces(email=err.email, workspaces=err.max_owned_limit)
            )

        except UnreachableOrgCluster as e:
            logging.info(
                f"User {user_creating_it.id} ({user_creating_it.email}) attempted to create a workspace: {str(e)}"
            )
            raise ApiHTTPError(400, str(e)) from e

        except Exception as e:
            logging.exception(e)
            error = WorkspacesServerErrorInternal.failed_register(name=name, error=str(e))
            raise ApiHTTPError.from_request_error(error)

        return workspace


class APIWorkspaceCreationHandler(APIWorkspaceCreationBaseHandler):
    @staticmethod
    def download_error(
        starter_kit: Optional[str],
        repository_url: Optional[str],
        repository_branch: Optional[str],
        catched_exception: Optional[Exception],
    ) -> ApiHTTPError:
        msg = None
        if starter_kit:
            msg = f"Starter kit '{starter_kit}' not found"
        else:
            msg = f"Can't fetch branch '{repository_branch}' from {repository_url}"

        if catched_exception:
            msg += f": {str(catched_exception)}"

        return ApiHTTPError(500, msg)

    @staticmethod
    async def download_blob_bytes(blob_url: str) -> io.BytesIO:
        # TODO list:
        # - Get a first chunk to identify magic bytes and stop download if not a zip file
        # - Get file size and cancel download y bigger than `download_limit` (limit to be defined)

        # Download file
        session = get_shared_session()
        async with session.get(blob_url) as resp:
            if resp.status == 200:
                return io.BytesIO(await resp.read())
            else:
                raise ApiHTTPError(resp.status, await resp.text())

    @staticmethod
    def unzip_bytes(contents: io.BytesIO, destination_path: str) -> None:
        logging.info(f"Unzipping bytes to {destination_path}...")
        with zipfile.ZipFile(contents) as zf:
            zf.extractall(destination_path)

    @staticmethod
    def get_download_url_for_repo(repository_url: str, repository_branch: str) -> str:
        # HACK specific to Github
        # TODO make generic for other providers

        if repository_url[-1] == "/":
            repository_url = repository_url[0:-1]

        return f"{repository_url}/archive/refs/heads/{repository_branch}.zip"

    async def push_project(self, project_path: str, token: str) -> None:
        region = self.get_current_region()
        tb_host = (
            self.get_region_config(region)["api_host"] if region is not None else self.application.settings.get("host")
        )

        tb_client = TinyB(token, tb_host, VERSION)

        # Mimic `tb push`
        # Default values extracted from click parameters config in tb_cli::push()
        filenames = None
        dry_run = False
        check = False
        push_deps = True
        debug = False
        force = False
        populate = False
        populate_subset = None
        populate_condition = None
        upload_fixtures = False
        wait = False
        ignore_sql_errors = True
        skip_confirmation = True
        only_response_times = False
        workspace_map = None
        workspace_lib_paths = None
        no_versions = True
        run_tests = False
        tests_to_run = 0
        tests_sample_by_params = 1
        tests_failfast = False
        tests_ignore_order = False

        await folder_push(
            tb_client,
            filenames=filenames,
            dry_run=dry_run,
            check=check,
            push_deps=push_deps,
            only_changes=False,
            debug=debug,
            force=force,
            folder=project_path,
            populate=populate,
            populate_subset=populate_subset,
            populate_condition=populate_condition,
            upload_fixtures=upload_fixtures,
            wait=wait,
            ignore_sql_errors=ignore_sql_errors,
            skip_confirmation=skip_confirmation,
            only_response_times=only_response_times,
            workspace_map=workspace_map,
            workspace_lib_paths=workspace_lib_paths,
            no_versions=no_versions,
            run_tests=run_tests,
            tests_to_run=tests_to_run,
            tests_sample_by_params=tests_sample_by_params,
            tests_failfast=tests_failfast,
            tests_ignore_order=tests_ignore_order,
        )

    async def create_workspace_using_remote(self) -> Workspace:
        workspace_desired_name = self.get_argument("name")

        # First of all, ensure the desired name is valid and unique
        try:
            WorkspaceName.validate(workspace_desired_name)
            _ = Workspace.get_by_name(workspace_desired_name)
            raise ApiHTTPError(400, f"Name '{workspace_desired_name}' already taken.")
        except WorkspaceNameIsNotValid as ex:
            raise ApiHTTPError(400, str(ex))
        except UserDoesNotExist:
            pass

        workspace_name = f"{workspace_desired_name}_{str(uuid.uuid4())[:4]}"

        starter_kit = self.get_argument("starter_kit", None)
        repository_url = self.get_argument("repository_url", None)
        repository_branch = self.get_argument("repository_branch", None)
        root_directory = self.get_argument("root_directory", "tinybird")

        if starter_kit:
            template = next(
                (
                    tpl
                    for tpl in AVAILABLE_TEMPLATES
                    if tpl.friendly_name == starter_kit or tpl.repository_name == starter_kit
                ),
                None,
            )
            if template is None:
                raise ApiHTTPError(400, f"Unknown starter kit '{starter_kit}'.")

            gh_user = self.application.settings["github_user"]
            repository_url = f"https://github.com/{gh_user}/{template.repository_name}"

        if not repository_branch:
            session = get_shared_session()
            github_token = self.application.settings["github_api"].get("sk_read_token", "")
            repository_branch = await GitHubInterface.get_default_branch_for_repo(
                repository_url=repository_url, github_token=github_token, session=session
            )
            if not repository_branch:
                raise ApiHTTPError(400, f"Unable to retrieve default branch for {repository_url}. Is your repo public?")

        blob_url = self.get_download_url_for_repo(repository_url, repository_branch)
        logging.info(f"Blobl url = {blob_url}")

        user = self.get_user_from_db()

        workspace = await self._register_workspace(user, workspace_name)

        # Prefix each temp directory with 'sk-<user_id>-' to be able to track abuse
        with tempfile.TemporaryDirectory(prefix=f"sk-{user.id}-") as temp_path:
            logging.info(f"Starter kit temporary workdir created at {temp_path}")

            workdir_root = os.path.join(temp_path, workspace_name)

            try:
                zip_bytes = await self.download_blob_bytes(blob_url)
            except Exception as ex:
                raise self.download_error(
                    starter_kit=starter_kit,
                    repository_url=repository_url,
                    repository_branch=repository_branch,
                    catched_exception=ex,
                )

            try:
                self.unzip_bytes(zip_bytes, workdir_root)
            except Exception as ex:
                logging.exception(ex)
                raise ApiHTTPError(500, f"Error unzipping blob: {str(ex)}")

            # Find the first non empty dir
            depth = 0
            while True:
                dirs = os.listdir(workdir_root)
                if len(dirs) == 0:
                    raise ApiHTTPError(500, "Empty repository")

                if len(dirs) > 1:
                    break
                workdir_root = os.path.join(workdir_root, dirs[0])

                depth += 1
                if depth == 10:
                    raise ApiHTTPError(500, "Invalid repository")

            project_root = os.path.join(workdir_root, root_directory)

            admin_tk = workspace.get_token_for_scope(scopes.ADMIN)

            if not admin_tk:
                raise ApiHTTPError(500, "ADMIN token not found in this repository")

            try:
                logging.info("Pushing project...")
                await self.push_project(project_root, admin_tk)
            except Exception as ex:
                await Workspaces.delete(workspace)
                raise ApiHTTPError(500, f"Error pushing data project to Tinybird: {str(ex)}")
            finally:
                logging.info("Cleaning up...")
                # Try some cleanup before exit, but let's not be too picky with IO errors
                shutil.rmtree(temp_path, ignore_errors=True)

        # Try to rename, or return the old one
        try:
            workspace = Workspaces.set_name(workspace, WorkspaceName(workspace_desired_name))

            tracer = self.application.settings["opentracing_tracing"].tracer
            WorkspaceService.trace_workspace_operation(tracer, workspace, "WorkspaceRenamed")
            return workspace
        except Exception:
            return workspace

    async def create_workspace(self) -> Workspace:
        user = self.get_user_from_db()
        name = self.get_argument("name", None)

        return await self._register_workspace(user, name)

    @user_authenticated
    async def post(self):
        workspace = None
        use_remote = self.get_argument("starter_kit", None) or self.get_argument("repository_url", None)
        assign_to_organization_id: Optional[str] = self.get_argument("assign_to_organization_id", None)
        current_user = self.get_user_from_db()
        organization: Optional[Organization] = None
        if assign_to_organization_id:
            organization = Organization.get_by_id(assign_to_organization_id)
            if organization is None:
                raise ApiHTTPError(400, f"Organization with id {assign_to_organization_id} not found")

            # The user has to be a member of the organization to assign a workspace to it
            # If you try to assign a workspace to an organization with domain, you need to have the same domain
            # If you try to assign a workspace to an organization without domain, you need to belong to at least one of the workspaces in the organization
            organization_members = await organization.get_members()
            organization_admins = await organization.get_admins()
            if current_user.id not in [member.id for member in [*organization_members, *organization_admins]]:
                raise ApiHTTPError(400, "You need to be a member of the organization to assign a workspace to it.")

        if use_remote:
            workspace = await self.create_workspace_using_remote()
        else:
            workspace = await self.create_workspace()

        if workspace is None:
            raise ApiHTTPError(500, "Unknown error registering workspace.")

        if organization:
            OrganizationService.add_workspace_to_organization(
                organization, workspace.id, current_user, self.application.settings["opentracing_tracing"].tracer
            )

        # Handle SessionRewind enable/disable
        enabling_sessionrewind = self.get_argument("enabling_sessionrewind", None)
        if enabling_sessionrewind:
            value = enabling_sessionrewind == "true"
            await UserAccounts.set_enable_sessionrewind_value(self.get_user_from_db().id, value)

        self.write_json(workspace.to_json())


class APIWorkspaceInvite(UserViewBase):
    async def get(self, workspace_id):
        if not self.get_user_from_db():
            self.set_cookie("next_url", self.request.path)
            self.redirect("/login")
        else:
            user = self.get_user_from_db()

            try:
                with UserAccount.transaction(user.id) as user_account:
                    workspace = Workspaces.get_by_id(workspace_id)

                    if not workspace.is_active:
                        self.render("404.html", current_user=user_account)
                        return

                    if UserWorkspaceRelationship.user_has_access(user_id=user_account.id, workspace_id=workspace.id):
                        if not user_account.confirmed_account:
                            user_account.confirmed_account = True

                        region_name = self.get_current_region()
                        base_login(self, user, workspace, region_name=region_name)
                        self.redirect(self.reverse_url("workspace_dashboard", workspace.id))
                    else:
                        self.redirect("/dashboard")
            except Exception:
                self.render("404.html", current_user=user)
                return


class APIWorkspaceHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        BaseHandler.__init__(self, application, request, **kwargs)
        self.mailgun_service = MailgunService(self.application.settings)

    def check_xsrf_cookie(self):
        pass

    @user_authenticated
    async def get(self, workspace_id):
        """
        Get workspace info
        """

        with_token = self.get_argument("with_token", "false") == "true"
        with_feature_flags = self.get_argument("with_feature_flags", "false") == "true"
        with_bi_enabled = self.get_argument("with_bi_enabled", "false") == "true"
        with_stripe = self.get_argument("with_stripe", "false") == "true"
        with_organization = self.get_argument("with_organization", "false") == "true"

        async def add_organization_info(response: Dict[str, Any], organization_id: str | None) -> None:
            if organization_id:
                organization = Organization.get_by_id(organization_id)
                if organization:
                    response["organization"] = {
                        "id": organization.id,
                        "name": organization.name,
                        "plan": {
                            "billing": organization.plan_details["billing"],
                            "commitment": organization.plan_details["commitment"],
                        },
                    }

        user = self.get_user_from_db()

        if not user.has_access_to(workspace_id):
            error = WorkspacesClientErrorForbidden.not_allowed()
            raise ApiHTTPError.from_request_error(error)

        workspace = Workspaces.get_by_id(workspace_id)
        response = workspace.to_json(
            with_token=with_token,
            with_feature_flags=with_feature_flags,
            with_bi_enabled=with_bi_enabled,
            with_stripe=with_stripe,
        )
        if with_organization:
            await add_organization_info(response, workspace.organization_id)
        if with_stripe:
            response["stripe"]["api_key"] = self.application.settings["stripe"]["public_api_key"]

        self.write_json(response)

    @user_authenticated
    @requires_write_access
    @is_workspace_admin
    async def delete(self, workspace_id):
        user = self.get_user_from_db()
        workspace = Workspaces.get_by_id(workspace_id)
        # this is for hard delete double confirmation
        workspace_name: Optional[str] = self.get_argument("confirmation", None)

        hard_delete: bool

        if workspace.is_branch:
            hard_delete = True
        else:
            if workspace_name and workspace_name != workspace.name:
                raise ApiHTTPError.from_request_error(WorkspacesClientErrorBadRequest.confirmation_is_not_valid())
            hard_delete = workspace_name == workspace.name

        try:
            user_emails = workspace.get_user_emails_that_have_access_to_this_workspace()
            tracer: ClickhouseTracer = self.application.settings["opentracing_tracing"].tracer

            await UserAccount.delete_workspace(
                user,
                workspace,
                hard_delete=hard_delete,
                job_executor=self.application.job_executor,
                request_id=self._request_id,
                tracer=tracer,
            )

            mailgun_response = await self.mailgun_service.send_remove_from_workspace_emails(
                owner_name=user.email, workspace=workspace, user_emails=user_emails
            )
            if mailgun_response.status_code != 200:
                logging.error(
                    f"Removal from workspace was not delivered to {user_emails}, "
                    f"code: {mailgun_response.status_code}, reason: {mailgun_response.content}"
                )
        except WorkspaceException as e:
            error = WorkspacesClientErrorForbidden.no_workspace_deletion_allowed(error=str(e))
            raise ApiHTTPError.from_request_error(error)
        except Exception as e:
            error = WorkspacesServerErrorInternal.failed_delete(name=workspace.name, error=str(e))
            raise ApiHTTPError.from_request_error(error)

        try:
            response = Workspaces.get_by_id(workspace_id).to_json()
        except UserDoesNotExist:
            response = {"result": "Workspace deleted"}
        self.write_json(response)

    @staticmethod
    async def rename_shared_data_sources_on_workspace_name_change(
        modified_workspace: Workspace, new_workspace_name: WorkspaceName, email: str
    ):
        for ds in modified_workspace.get_datasources():
            try:
                for shared_with_ws_id in ds.shared_with:
                    await Workspaces.alter_shared_datasource_name(
                        shared_with_ws_id, ds.id, modified_workspace.id, str(new_workspace_name), ds.name, email
                    )
            except Exception as e:
                logging.exception(f"Couldn't update shared Data Source name on workspace name change: {e}")

    async def validate_rename_in_branching(self, workspace: "Workspace"):
        if workspace.is_branch:
            error = WorkspacesClientErrorBadRequest.no_branch_rename()
            raise ApiHTTPError.from_request_error(error)
        else:
            info = workspace.get_workspace_info()
            owner = UserAccount.get_by_id(info["owner"])
            if not owner:
                raise ApiHTTPError(404, f"Owner of workspace {workspace.id} not found")

            if await owner.get_workspaces(
                with_token=False, with_environments=True, only_environments=True, filter_by_workspace=workspace.id
            ):
                error = WorkspacesClientErrorBadRequest.no_workspace_with_branches_rename()
                raise ApiHTTPError.from_request_error(error)

    @user_authenticated
    @requires_write_access
    @is_workspace_admin
    async def put(self, workspace_id):
        """
        Update Workspace name. To be able to change it, you should take into consideration these things:

        - The name should be normalized: names supported only allows letters, numbers and underscores.
        - The name should be globally unique: We will check if the name used is unique. If the name is already
        in use, please use another one.
        - You can only execute this operation if you are the owner of the Workspace.

        .. container:: hint

            Caution: if this Workspace owns shared Data Sources, the name of these Data Sources will also be renamed at
            the destination Workspaces. This will break the pipes and queries using it.

        .. sourcecode:: bash
            :caption: Updating the name of a Workspace

            curl \\
            -H "Authorization: Bearer <token>" \\
            -X PUT "https://api.tinybird.co/v0/workspaces/:workspace_id?name=new_name"

        .. csv-table:: Request parameters
            :header: "Key", "Type", "Description"
            :widths: 20, 20, 60

            "name", "String", "new name for the Workspace"
            "token", "String", "Auth token. Only required if no Bearer Authorization header is sent. It should have the ownership of the Workspace."
        """

        name = self.get_argument("name", None)
        is_read_only = self.get_argument("is_read_only", None)
        user = self.get_user_from_db()

        if not name and not is_read_only:
            error = WorkspacesClientErrorBadRequest.invalid_workspace_name()
            raise ApiHTTPError.from_request_error(error)

        try:
            workspace = Workspaces.get_by_id(workspace_id)
        except UserDoesNotExist:
            error = WorkspacesClientErrorNotFound.no_workspace()
            raise ApiHTTPError.from_request_error(error)

        modified_workspace = workspace

        if name:
            await self.validate_rename_in_branching(workspace)

            try:
                workspace_name = WorkspaceName(name)
                modified_workspace = Workspaces.set_name(workspace, workspace_name)

                tracer: ClickhouseTracer = self.application.settings["opentracing_tracing"].tracer
                WorkspaceService.trace_workspace_operation(tracer, modified_workspace, "WorkspaceRenamed", user)

            except WorkspaceNameIsNotValid as validation_error:
                raise ApiHTTPError.from_request_error(
                    WorkspacesClientErrorBadRequest.name_is_not_valid(validation_error=str(validation_error))
                )

            except NameAlreadyTaken as error:
                raise ApiHTTPError.from_request_error(
                    WorkspacesClientErrorBadRequest.name_already_taken(name=error.name_taken)
                )

            await self.rename_shared_data_sources_on_workspace_name_change(
                modified_workspace, workspace_name, email=user.email
            )

        if is_read_only is not None:
            is_read_only = is_read_only.lower()

            if is_read_only not in ["true", "false"]:
                raise ApiHTTPError.from_request_error(WorkspacesClientErrorBadRequest.invalid_read_only_value())

            is_read_only = is_read_only == "true"
            modified_workspace = Workspaces.set_is_read_only(workspace, is_read_only)

        response = modified_workspace.to_json()
        self.write_json(response)


class APIWorkspaceRemoteHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @user_authenticated
    @requires_write_access
    @is_workspace_admin
    async def get(self, workspace_id: str) -> None:
        user = self.get_user_from_db()
        if not user.has_access_to(workspace_id):
            error = WorkspacesClientErrorForbidden.not_allowed()
            raise ApiHTTPError.from_request_error(error)

        workspace: Workspace = Workspaces.get_by_id(workspace_id)

        if not workspace.remote.get("provider"):
            error = WorkspacesClientRemoteError.not_connected()
            raise ApiHTTPError.from_request_error(error)

        try:
            github_settings = GitHubWorkspaceSettings(
                owner=workspace.remote.get("owner", ""),
                remote=workspace.remote.get("remote", ""),
                access_token=workspace.remote.get("access_token", ""),
            )
        except Exception as e:
            raise ApiHTTPError(400, str(e))

        session = get_shared_session()

        account_information = await GitHubInterface.get_account_information(
            workspace=workspace, github_settings=github_settings, session=session
        )

        self.write_json(account_information)

    @user_authenticated
    @is_workspace_admin
    async def post(self, workspace_id: str) -> None:
        user = self.get_user_from_db()
        if not user.has_access_to(workspace_id):
            error = WorkspacesClientErrorForbidden.not_allowed()
            raise ApiHTTPError.from_request_error(error)

        access_token: str = self.get_argument("access_token")
        owner: str = self.get_argument("owner")
        owner_type: str = self.get_argument("owner_type")
        remote_provider: str = self.get_argument("provider")
        remote: str = self.get_argument("remote", "")
        remote_branch: str = self.get_argument("branch", "")
        project_path: str = self.get_argument("project_path", "")

        workspace: Workspace = Workspaces.get_by_id(workspace_id)

        if remote_provider not in AVAILABLE_GIT_PROVIDERS:
            error = WorkspacesClientRemoteError.invalid_provider()
            raise ApiHTTPError.from_request_error(error)

        if workspace.remote.get("provider"):
            error = WorkspacesClientRemoteError.already_connected()
            raise ApiHTTPError.from_request_error(error)

        # FIXME: change settings depending on the provider
        remote_settings = GitHubSettings(
            provider=remote_provider,
            owner=owner,
            owner_type=owner_type,
            remote=remote,
            access_token=access_token,
            branch=remote_branch,
            project_path=project_path,
        )

        workspace = await Workspaces.update_remote(workspace, remote=remote_settings)

        self.write_json(workspace.to_json())

    @user_authenticated
    @requires_write_access
    @is_workspace_admin
    async def put(self, workspace_id: str) -> None:
        user = self.get_user_from_db()
        if not user.has_access_to(workspace_id):
            error = WorkspacesClientErrorForbidden.not_allowed()
            raise ApiHTTPError.from_request_error(error)

        remote: str = self.get_argument("remote")
        remote_branch: str = self.get_argument("branch", "")
        project_path: str = self.get_argument("project_path", "")
        owner: str = self.get_argument("owner", "")
        owner_type: str = self.get_argument("owner_type", "")
        status: str = self.get_argument("status", "")

        workspace: Workspace = Workspaces.get_by_id(workspace_id)

        if not workspace.remote.get("provider"):
            error = WorkspacesClientRemoteError.not_connected()
            raise ApiHTTPError.from_request_error(error)

        remote_settings = GitHubSettings(
            remote=remote,
            branch=remote_branch,
            project_path=project_path,
            owner=owner,
            owner_type=owner_type,
            status=status,
        )

        workspace = await Workspaces.update_remote(workspace, remote=remote_settings)
        self.write_json(workspace.to_json())

    @user_authenticated
    @requires_write_access
    @is_workspace_admin
    async def delete(self, workspace_id: str) -> None:
        user = self.get_user_from_db()
        force = self.get_argument("force", "false") == "true"
        if not user.has_access_to(workspace_id):
            error = WorkspacesClientErrorForbidden.not_allowed()
            raise ApiHTTPError.from_request_error(error)

        workspace: Workspace = Workspaces.get_by_id(workspace_id)

        if not workspace.remote.get("provider"):
            error = WorkspacesClientRemoteError.not_connected()
            raise ApiHTTPError.from_request_error(error)

        try:
            workspace = await Workspaces.delete_remote(workspace, force=force)
            self.set_status(204)
        except DeleteRemoteException:
            error = WorkspacesClientErrorForbidden.delete_remote_forbidden(name=workspace.name)
            raise ApiHTTPError.from_request_error(error)
        except Exception as e:
            error = WorkspacesServerErrorInternal.failed_unlink(name=workspace.name, error=str(e))
            raise ApiHTTPError.from_request_error(error)


class APIWorkspaceRemoteReposHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @user_authenticated
    @is_workspace_admin
    async def get(self, workspace_id: str):
        user = self.get_user_from_db()
        if not user.has_access_to(workspace_id):
            error = WorkspacesClientErrorForbidden.not_allowed()
            raise ApiHTTPError.from_request_error(error)

        workspace: Workspace = Workspaces.get_by_id(workspace_id)

        if not workspace.remote.get("provider"):
            error = WorkspacesClientRemoteError.not_connected()
            raise ApiHTTPError.from_request_error(error)

        try:
            github_workspace_settings = GitHubWorkspaceSettings(
                access_token=workspace.remote.get("access_token", ""),
                owner=self.get_argument("owner", workspace.remote.get("owner", "")),
                owner_type=self.get_argument("owner_type", workspace.remote.get("owner_type", "")),
            )
        except Exception as e:
            raise ApiHTTPError(400, str(e))

        try:
            sort: str = self.get_argument("sort")
            order: str = self.get_argument("order")
            session = get_shared_session()

            repositories = await GitHubInterface.get_repositories(
                github_settings=github_workspace_settings,
                session=session,
                sort=sort,
                order=order,
            )
        except Exception as e:
            raise ApiHTTPError(422, str(e))

        self.write_json(repositories)


class APIWorkspaceRemoteChangesHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @user_authenticated
    async def get(self, workspace_id: str) -> None:
        user = self.get_user_from_db()
        if not user.has_access_to(workspace_id):
            error = WorkspacesClientErrorForbidden.not_allowed()
            raise ApiHTTPError.from_request_error(error)

        workspace: Workspace = Workspaces.get_by_id(workspace_id)

        if not workspace.remote.get("provider"):
            error = WorkspacesClientRemoteError.not_connected()
            raise ApiHTTPError.from_request_error(error)

        changed_pipes: List[Dict[str, Any]] = []
        changed_datasources: List[Dict[str, Any]] = []
        response: Dict[str, Any] = {
            "pipes": changed_pipes,
            "datasources": changed_datasources,
            "commit": "",
            "commit_message": "",
            "updated_at": "",
            "updated_by": "",
        }
        # 1. Get last commit
        try:
            github_workspace_settings = GitHubWorkspaceSettings(
                owner=workspace.remote.get("owner", ""),
                access_token=workspace.remote.get("access_token", ""),
                remote=workspace.remote.get("remote", ""),
                branch=workspace.remote.get("branch", ""),
                project_path=workspace.remote.get("project_path", ""),
                last_commit_sha=workspace.remote.get("last_commit_sha"),
            )
        except Exception as e:
            raise ApiHTTPError(400, str(e))

        session = get_shared_session()

        try:
            commit = await GitHubInterface.get_last_commit(github_settings=github_workspace_settings, session=session)
        except Exception as e:
            raise ApiHTTPError(422, str(e))
        last_commit_sha = commit.get("sha", "")

        datasources = workspace.get_datasources()
        pipes = workspace.get_pipes()

        if not last_commit_sha:
            changed_pipes = [{"id": p.id, "name": p.name} for p in pipes]
            changed_datasources = [{"id": d.id, "name": d.name} for d in datasources]
            response = {
                **response,
                "pipes": changed_pipes,
                "datasources": changed_datasources,
            }
            self.write_json(response)
            return

        shas: List[str] = []
        paths: List[str] = []

        datasources_files_shas: List[str] = [
            d.last_commit.get("content_sha", "") for d in datasources if d.last_commit.get("content_sha")
        ]
        pipes_files_shas: List[str] = [
            p.last_commit.get("content_sha", "") for p in pipes if p.last_commit.get("content_sha")
        ]

        # 2. If commit is different or not all files have shas, request the blob sha
        check_all_shas = len(datasources_files_shas) < len(datasources) or len(pipes_files_shas) < len(pipes)

        if check_all_shas or (last_commit_sha and last_commit_sha != github_workspace_settings.last_commit_sha):
            remote_files_shas = await GitHubInterface.get_files_sha_for_commit(
                github_settings=github_workspace_settings,
                commit_sha=last_commit_sha,
                session=session,
            )
            shas = list(remote_files_shas.values())
            paths = list(remote_files_shas.keys())
        else:
            datasources_files_paths: List[str] = [
                d.last_commit.get("path", "") for d in datasources if d.last_commit.get("path")
            ]
            pipes_files_paths: List[str] = [p.last_commit.get("path", "") for p in pipes if p.last_commit.get("path")]
            shas = datasources_files_shas + pipes_files_shas
            paths = datasources_files_paths + pipes_files_paths

        # 3. Compare blob shas and paths
        # datasource_resources = [d.id for d in datasources]
        # pipe_resources = [p.id for p in pipes]

        current_token = self._get_access_info()

        # 3.1 First, calculate local shas without saving it to the model
        new_resources = await GitHubInterface.generate_resources(
            workspace,
            github_settings=github_workspace_settings,
            pipes=pipes,
            datasources=datasources,
            session=session,
            tinybird_token=current_token,
            extra_files=None,
        )

        shared_workspaces: Dict[str, Workspace] = {}
        for resource in new_resources:
            if resource.resource_type == "datasource":
                if resource.origin and resource.origin != workspace.name:
                    shared_workspace = shared_workspaces.get(resource.origin, Workspaces.get_by_name(resource.origin))
                    shared_workspaces[resource.origin] = shared_workspace
                    shared_datasource = shared_workspace.get_datasource(resource.resource_name.split(".")[1])
                    if not shared_datasource:
                        continue
                    if resource.sha not in shas or resource.path not in paths:
                        changed_datasources.append(
                            {"id": shared_datasource.id, "name": shared_datasource.name, "workspace": resource.origin}
                        )
                else:
                    datasource = workspace.get_datasource(resource.resource_name)
                    if not datasource:
                        continue
                    if resource.sha not in shas or resource.path not in paths:
                        changed_datasources.append(
                            {"id": datasource.id, "name": datasource.name, "workspace": resource.origin}
                        )

            elif resource.resource_type == "pipe":
                pipe = workspace.get_pipe(resource.resource_name)
                if not pipe:
                    continue
                if resource.sha not in shas or resource.path not in paths:
                    changed_pipes.append({"id": pipe.id, "name": pipe.name, "workspace": resource.origin})

        last_commit_updated_at = commit.get("updated_at", "")
        last_commit_updated_by = commit.get("updated_by", "")
        last_commit_message = commit.get("message", "")

        response = {
            "pipes": changed_pipes,
            "datasources": changed_datasources,
            "commit": last_commit_sha,
            "commit_message": last_commit_message,
            "updated_at": last_commit_updated_at,
            "updated_by": last_commit_updated_by,
        }

        self.write_json(response)


class APIWorkspaceRemotePushHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @user_authenticated
    @requires_write_access
    async def post(self, workspace_id: str):
        user = self.get_user_from_db()
        if not user.has_access_to(workspace_id):
            error = WorkspacesClientErrorForbidden.not_allowed()
            raise ApiHTTPError.from_request_error(error)

        workspace: Workspace = Workspaces.get_by_id(workspace_id)
        if not workspace.remote.get("provider"):
            error = WorkspacesClientRemoteError.not_connected()
            raise ApiHTTPError.from_request_error(error)

        message: str = self.get_argument("message", "")
        pipes = self.get_argument("pipes", "")
        datasources = self.get_argument("datasources", "")
        include_templates = self.get_argument("include_templates", "false") == "true"
        extra_files = self.get_argument("extra_files", "{}")
        tinyenv_version = self.get_argument("tinyenv_version", SemverVersions.CURRENT.value)

        try:
            extra_files = orjson.loads(extra_files)
        except Exception:
            pass

        if not message:
            error = WorkspacesClientRemoteError.no_message()
            raise ApiHTTPError.from_request_error(error)

        pipes_names_or_ids: List[str] = pipes.split(",") if pipes else []
        datasources_names_or_ids: List[str] = datasources.split(",") if datasources else []

        try:
            github_workspace_settings = GitHubWorkspaceSettings(
                owner=workspace.remote.get("owner", ""),
                access_token=workspace.remote.get("access_token", ""),
                remote=workspace.remote.get("remote", ""),
                branch=self.get_argument("target_branch", workspace.remote.get("branch", "")),
                project_path=workspace.remote.get("project_path", ""),
            )
        except Exception as e:
            raise ApiHTTPError(400, str(e))

        session = get_shared_session()

        all_datasources = workspace.get_datasources()
        datasources = []

        shared_workspaces: Dict[str, Workspace] = {}  # to avoid requesting workspaces more than once
        for datasource in all_datasources:
            if isinstance(datasource, SharedDatasource):
                shared_workspace = shared_workspaces.get(
                    datasource.original_workspace_id, Workspaces.get_by_id(datasource.original_workspace_id)
                )
                shared_workspaces[datasource.original_workspace_id] = shared_workspace
                shared_datasource = shared_workspace.get_datasource(datasource.original_ds_name)
                if shared_datasource and (
                    shared_datasource.id in datasources_names_or_ids
                    or shared_datasource.name in datasources_names_or_ids
                ):
                    datasources.append(datasource)
            else:
                if datasource.id in datasources_names_or_ids or datasource.name in datasources_names_or_ids:
                    datasources.append(datasource)

        all_pipes = workspace.get_pipes()
        pipes = []
        for pipe in all_pipes:
            if pipe.id in pipes_names_or_ids or pipe.name in pipes_names_or_ids:
                pipes.append(pipe)

        try:
            commit = await GitHubInterface.get_last_commit(github_settings=github_workspace_settings, session=session)
        except Exception as e:
            raise ApiHTTPError(422, str(e))
        last_commit_sha = commit.get("sha", None)
        current_token = self._get_access_info()

        try:
            response = await GitHubInterface.push_multiple_files(
                workspace=workspace,
                user=user,
                github_settings=github_workspace_settings,
                host=self.application.settings.get("host"),
                pipes=pipes,
                datasources=datasources,
                session=session,
                include_templates=include_templates,
                last_commit_sha=last_commit_sha,
                extra_files=extra_files,
                message=message,
                tinybird_token=current_token,
                tinyenv_version=tinyenv_version,
            )
        except (PipeNotFound, DataSourceNotFound) as e:
            raise ApiHTTPError(404, str(e))
        except Exception as e:
            logging.warning(f"Failed push to GitHub exception: {e}")
            raise ApiHTTPError.from_request_error(WorkspacesClientRemoteError.failed_push(message=str(e), error=str(e)))

        self.write_json(response)


class APIWorkspaceRemoteCheckHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @user_authenticated
    async def get(self, workspace_id: str) -> None:
        user = self.get_user_from_db()
        if not user.has_access_to(workspace_id):
            error = WorkspacesClientErrorForbidden.not_allowed()
            raise ApiHTTPError.from_request_error(error)

        workspace: Workspace = Workspaces.get_by_id(workspace_id)
        if not workspace.remote.get("provider"):
            error = WorkspacesClientRemoteError.not_connected()
            raise ApiHTTPError.from_request_error(error)

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

        session = get_shared_session()

        try:
            commit = await GitHubInterface.get_last_commit(github_settings=github_workspace_settings, session=session)
        except Exception as e:
            raise ApiHTTPError(422, str(e))
        last_commit_sha = commit.get("sha", "")

        if not last_commit_sha:
            return self.write_json({})

        files = await GitHubInterface.get_files_sha_for_commit(
            github_settings=github_workspace_settings,
            commit_sha=last_commit_sha,
            session=session,
        )
        return self.write_json(files)


class APIWorkspaceRemoteAccessHandler(BaseHandler):
    @user_authenticated
    @requires_write_access
    @is_workspace_admin
    async def post(self, workspace_id: str) -> None:
        user = self.get_user_from_db()

        if not user.has_access_to(workspace_id):
            error = WorkspacesClientErrorForbidden.not_allowed()
            raise ApiHTTPError.from_request_error(error)

        workspace: Workspace = Workspaces.get_by_id(workspace_id)
        if not workspace.remote.get("provider"):
            error = WorkspacesClientRemoteError.not_connected()
            raise ApiHTTPError.from_request_error(error)

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

        session = get_shared_session()
        secret_name = f"TB_{workspace.name.upper()}_ADMIN_TOKEN"
        secret_token = Workspaces.get_token_for_scope(workspace, scopes.ADMIN_USER)
        if not secret_token:
            error = WorkspacesClientRemoteError.not_connected()
            raise ApiHTTPError.from_request_error(error)

        await GitHubInterface.create_secret_in_repo(
            github_settings=github_workspace_settings,
            session=session,
            secret_name=secret_name,
            secret_value=secret_token,
        )
        self.write_json({"response": "ok"})


class APIWorkspaceRemotePullRequestHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    @user_authenticated
    async def get(self, workspace_id: str) -> None:
        user = self.get_user_from_db()
        session = get_shared_session()

        if not user.has_access_to(workspace_id):
            error = WorkspacesClientErrorForbidden.not_allowed()
            raise ApiHTTPError.from_request_error(error)

        workspace: Workspace = Workspaces.get_by_id(workspace_id)
        if not workspace.remote.get("provider"):
            error = WorkspacesClientRemoteError.not_connected()
            raise ApiHTTPError.from_request_error(error)

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

        origin = Workspaces.get_by_id(workspace.origin) if workspace.origin else None
        if not origin:
            all_pull_requests = await GitHubInterface.get_pull_request(
                github_settings=github_workspace_settings, session=session
            )

            branches = await user.get_workspaces(
                with_token=False, with_environments=True, only_environments=True, filter_by_workspace=workspace.id
            )

            response = []
            for branch in branches:
                branch_name = branch.get("name")
                pull_request = all_pull_requests.get(branch_name, "") if branch_name else ""
                if pull_request:
                    response.append(pull_request)
            self.write_json({"pull_requests": response})
        else:
            base_branch = origin.remote.get("branch", None)
            if not base_branch:
                error = WorkspacesClientRemoteError.main_has_no_branch()
                raise ApiHTTPError.from_request_error(error)

            single_pull_request = await GitHubInterface.get_pull_request(
                github_settings=github_workspace_settings, session=session, base_branch=base_branch
            )

            self.write_json({"pull_requests": [single_pull_request]})

    @user_authenticated
    @requires_write_access
    async def post(self, workspace_id: str) -> None:
        user = self.get_user_from_db()
        if not user.has_access_to(workspace_id):
            error = WorkspacesClientErrorForbidden.not_allowed()
            raise ApiHTTPError.from_request_error(error)

        workspace: Workspace = Workspaces.get_by_id(workspace_id)
        if not workspace.remote.get("provider"):
            error = WorkspacesClientRemoteError.not_connected()
            raise ApiHTTPError.from_request_error(error)

        origin = Workspaces.get_by_id(workspace.origin) if workspace.origin else None
        if not origin:
            error = WorkspacesClientRemoteError.pull_request_from_main_not_allowed()
            raise ApiHTTPError.from_request_error(error)

        base_branch = origin.remote.get("branch", None)
        if not base_branch:
            error = WorkspacesClientRemoteError.main_has_no_branch()
            raise ApiHTTPError.from_request_error(error)

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

        title = self.get_argument("title", f"Merge {github_workspace_settings.branch} into {base_branch}")
        description = self.get_argument("description", "Your description here")

        session = get_shared_session()
        pull_request = await GitHubInterface.create_pull_request(
            github_settings=github_workspace_settings,
            session=session,
            base_branch=base_branch,
            title=title,
            description=description,
        )

        self.write_json(pull_request)


class APIWorkspaceRemoteBranchHandler(BaseBranchHandler):
    def check_xsrf_cookie(self):
        pass

    @user_authenticated
    @requires_write_access
    async def post(self, workspace_id: str) -> None:
        user = self.get_user_from_db()
        if not user.has_access_to(workspace_id):
            error = WorkspacesClientErrorForbidden.not_allowed()
            raise ApiHTTPError.from_request_error(error)

        workspace: Workspace = Workspaces.get_by_id(workspace_id)
        if not workspace.remote.get("provider"):
            error = WorkspacesClientRemoteError.not_connected()
            raise ApiHTTPError.from_request_error(error)

        origin = Workspaces.get_by_id(workspace.origin) if workspace.origin else None
        target_branch = self.get_argument("branch", "")
        base_branch = origin.remote.get("branch", None) if origin else workspace.remote.get("branch")

        if origin and not target_branch:
            error = WorkspacesClientRemoteError.pull_request_from_main_not_allowed()
            raise ApiHTTPError.from_request_error(error)

        if not base_branch and not target_branch:
            error = WorkspacesClientRemoteError.main_has_no_branch()
            raise ApiHTTPError.from_request_error(error)

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

            branch = await GitHubInterface.create_branch(
                github_settings=github_workspace_settings,
                session=session,
                base_branch=base_branch,
                target_branch=target_branch,
            )
        except Exception as e:
            raise ApiHTTPError(422, str(e))

        self.write_json(branch)


class APIWorkspace(BaseHandler):
    @authenticated
    async def get(self):
        """
        Get workspace info from token
        """

        workspace = self.get_workspace_from_db()

        response: Dict[str, Any] = {
            "id": workspace.id,
            "name": workspace.name,
            "releases": [release.to_json() for release in workspace.get_releases()],
        }

        access_info = workspace.get_token_access_info(self.get_workspace_token_from_request_or_cookie().decode())
        if not access_info:
            raise ApiHTTPError(401, "Invalid workspace token")

        resources = access_info.get_resources_for_scope(scopes.ADMIN_USER)

        if resources:
            user_id = resources[0]
            user_account = UserAccount.get_by_id(user_id)
            if not user_account:
                raise ApiHTTPError(404, f"User {user_id} not found")
            response["user_id"] = user_account.id
            response["user_email"] = user_account.email
            response["scope"] = "user"
            response["main"] = workspace.origin
        else:
            response["scope"] = "admin" if access_info.has_scope(scopes.ADMIN) else None

        self.write_json(response)


class APIUserWorkspaces(UserViewBase):
    @user_or_workspace_authenticated
    async def get(self):
        user = self.get_user_from_db()
        with_environments = self.get_argument("with_environments", "true") == "true"
        only_environments = self.get_argument("only_environments", "false") == "true"
        with_feature_flags = self.get_argument("with_feature_flags", "false") == "true"
        with_integrations = self.get_argument("with_integrations", "false") == "true"
        with_organization = self.get_argument("with_organization", "false") == "true"
        with_tracking = self.get_argument("with_tracking", "false") == "true"
        with_members_and_owner = self.get_argument("with_members_and_owner", "true") == "true"

        # TODO: Why this is not included inside the get_user_info?
        async def add_organization_info(response: Dict[str, Any]) -> None:
            """
            If the user is part of an organization, add the organization name to the response.
            If the user is not part of an organization, add the list of admins to the response to it can contact them to requires access to an organization cluster
            """
            org_id = response.get("organization_id")
            if org_id:
                organization = Organization.get_by_id(org_id)
                if organization:
                    response["organization_name"] = organization.name

            else:
                possible_organization = await Organizations.get_by_email(user.email)
                if possible_organization:
                    response["organization_by_domain"] = possible_organization.name

        if user:
            response = user.get_user_info(
                with_feature_flags=with_feature_flags,
                with_integrations=with_integrations,
                with_organization=with_organization,
                with_tracking=with_tracking,
            )

            if with_organization:
                await add_organization_info(response)

            response["dedicated_cluster"] = await user.has_organization_cluster()
            response["workspaces"] = await user.get_workspaces(
                with_token=True,
                with_environments=with_environments,
                only_environments=only_environments,
                with_members_and_owner=with_members_and_owner,
            )
            response["scope"] = "user"
            self.write_json(response)
            return

        if not self.is_admin():
            raise ApiHTTPError(
                403, "Token does not have ADMIN scope.", documentation="/api-reference/token-api.html#scopes-and-tokens"
            )

        workspace = self.get_workspace_from_db()
        resources = self.get_resources_for_scope(scopes.ADMIN_USER)

        if resources:
            admin_user = UserAccount.get_by_id(resources[0])
            if not admin_user:
                raise ApiHTTPError(404, f"User {resources[0]} not found")
            response = admin_user.get_user_info(
                with_feature_flags=with_feature_flags,
                with_integrations=with_integrations,
                with_organization=with_organization,
                with_tracking=with_tracking,
            )

            if with_organization:
                await add_organization_info(response)

            response["dedicated_cluster"] = await admin_user.has_organization_cluster()
            response["workspaces"] = await admin_user.get_workspaces(
                with_token=True,
                with_environments=with_environments,
                only_environments=only_environments,
                with_members_and_owner=with_members_and_owner,
            )
            response["scope"] = "user"
            self.write_json(response)
            return

        workspace_info = workspace.get_workspace_info(with_token=True, with_members_and_owner=with_members_and_owner)
        response = {"id": workspace["id"], "name": workspace["name"], "workspaces": [workspace_info], "scope": "admin"}
        self.write_json(response)


class APIWorkspaceUsers(UserViewBase):
    def check_xsrf_cookie(self):
        pass

    async def check_rate_limit_for_invitations(self, workspace_id: str) -> None:
        workspace = Workspace.get_by_id(workspace_id)
        if not workspace:
            raise ApiHTTPError(404, "workspace not found")
        await self.check_rate_limit(Limit.api_workspace_users_invite, workspace=workspace)

    @user_authenticated
    @requires_write_access
    @is_workspace_admin
    async def post(self, workspace_id: str) -> None:
        """
        Send invitation links
        """

        users = self.get_argument("users", None)

        await self.check_rate_limit_for_invitations(workspace_id)

        if not users:
            error = WorkspacesClientErrorBadRequest.no_users()
            raise ApiHTTPError.from_request_error(error)

        user = self.get_user_from_db()
        workspace = Workspaces.get_by_id(workspace_id)

        user_emails = users.split(",")

        mailgun_response = await self.mailgun_service.send_add_to_workspace_emails(
            owner_name=user.email, workspace=workspace, user_emails=user_emails
        )

        if not mailgun_response:
            logging.warning("Emails couldn't be sent. Users not found")

        elif mailgun_response.status_code != 200:
            logging.error(
                f"Addition to workspace was not delivered to {user_emails}, "
                f"code: {mailgun_response.status_code}, reason: {mailgun_response.content}"
            )

        response = workspace.to_json()
        self.write_json(response)

    @user_authenticated
    @requires_write_access
    @is_workspace_admin
    async def put(self, workspace_id: str) -> None:
        """
        Expected parameters:
        operation: one of the values in ['add', 'remove', 'change_role', 'change_notifications'].
        users: comma separated list of user emails where the operation will be executed.

        Special parameter for 'change_relation':
        - 'new_role': new role assigned to the users: guest or admin.
        """
        operation: Optional[str] = self.get_argument("operation", None)
        users: Optional[str] = self.get_argument("users", None)

        if not users:
            error = WorkspacesClientErrorBadRequest.no_users()
            raise ApiHTTPError.from_request_error(error)

        if not operation or operation not in valid_operations:
            error = WorkspacesClientErrorBadRequest.invalid_operation(
                operation=operation, valid_operations=valid_operations
            )
            raise ApiHTTPError.from_request_error(error)

        user = self.get_user_from_db()
        workspace = Workspaces.get_by_id(workspace_id)
        users_emails = users.lower().split(",")

        try:
            if operation == "add":
                await self.check_rate_limit_for_invitations(workspace_id)
                role = self.get_argument("role", None)
                await WorkspaceService.invite_users_to_workspace(
                    user.email, workspace_id, users_emails=users_emails, notify_users=True, role=role
                )

            elif operation == "remove":
                removed_users = []
                with Workspace.transaction(workspace_id) as workspace:
                    removed_users = workspace.remove_users_from_workspace(users_emails)

                if len(removed_users):
                    mailgun_response = await self.mailgun_service.send_remove_from_workspace_emails(
                        owner_name=user.email, workspace=workspace, user_emails=users_emails
                    )
                    if mailgun_response.status_code != 200:
                        logging.error(
                            f"Removal from workspace was not delivered to {users_emails}, "
                            f"code: {mailgun_response.status_code}, reason: {mailgun_response.content}"
                        )

            elif operation == "change_role":
                new_role = self.get_argument("new_role")

                for email in users_emails:
                    user_to_modify = UserAccount.get_by_email(email)
                    UserWorkspaceRelationships.change_role(user_to_modify.id, workspace, new_role)

                # Redundant loop to ensure we rename the token after the role change
                with Workspace.transaction(workspace_id) as workspace:
                    for email in users_emails:
                        user_to_modify = UserAccount.get_by_email(email)
                        UserWorkspaceRelationships.rename_user_token_by_role(user_to_modify.id, workspace, new_role)

                mailgun_response = await self.mailgun_service.send_change_role_from_workspace_emails(
                    owner_name=user.email, workspace=workspace, user_emails=users_emails, new_role=new_role
                )
                if mailgun_response.status_code != 200:
                    logging.error(
                        f"Role change in workspace was not delivered to {users_emails}, "
                        f"code: {mailgun_response.status_code}, reason: {mailgun_response.content}"
                    )

            if operation == "change_notifications":
                notifications = (
                    self.get_argument("notifications").split(",") if len(self.get_argument("notifications")) > 0 else []
                )
                for email in users_emails:
                    user_to_modify = UserAccount.get_by_email(email)
                    UserWorkspaceNotificationsHandler.change_notifications(
                        user_to_modify.id, workspace.id, notifications
                    )

        except (WorkspaceException, UserWorkspaceRelationshipException) as e:
            error = WorkspacesClientErrorBadRequest.failed_operation(operation=operation, error=str(e))
            raise ApiHTTPError.from_request_error(error)
        except ApiHTTPError as e:
            raise e
        except Exception as e:
            logging.exception(e)
            error = WorkspacesClientErrorBadRequest.failed_operation(operation=operation, error=str(e))
            raise ApiHTTPError.from_request_error(error)

        response = workspace.to_json()
        self.write_json(response)


class APIWorkspaceReleaseOldestRollbackHandler(UserViewBase):
    def prepare(self) -> None:
        main_or_branch = self.get_current_workspace()
        if not main_or_branch:
            raise ApiHTTPError(
                403,
                INVALID_AUTH_MSG,
                documentation="/api-reference/overview#authentication",
            )

    @authenticated
    @with_scope_admin
    async def get(self, workspace_id):
        workspace = Workspace.get_by_id(workspace_id)

        if workspace.is_branch:
            self.set_status(204)
            return

        release = workspace.release_oldest_rollback()
        if not release:
            self.set_status(204)
            return
        else:
            self.write_json(release.to_json())


class APIWorkspaceReleaseHandler(UserViewBase):
    def prepare(self) -> None:
        main_or_branch = self.get_current_workspace()
        if not main_or_branch:
            raise ApiHTTPError(
                403,
                INVALID_AUTH_MSG,
                documentation="/api-reference/overview#authentication",
            )

    @authenticated
    @requires_write_access
    @with_scope_admin
    async def put(self, workspace_id, semver):
        commit = self.get_argument("commit", None)
        status = self.get_argument("status", None)
        new_semver = self.get_argument("new_semver", None)
        w = Workspace.get_by_id(workspace_id)
        release = w.get_release_by_semver(semver)
        if not release:
            raise ApiHTTPError(404, f"Release {semver} not found")

        try:
            w = await Workspaces.update_release(
                w, release, commit=commit, status=ReleaseStatus(status) if status else None, semver=new_semver
            )
        except ReleaseStatusException as e:
            raise ApiHTTPError(400, str(e))
        except Exception as e:
            raise ApiHTTPError(500, str(e))

        try:
            updated_release = w.get_release_by_semver(semver)
            if updated_release:
                response = updated_release.to_json()
                self.write_json(response)
            else:
                current_release = w.current_release
                assert current_release is not None
                self.set_span_tag({"new_release": current_release.semver})
                self.write_json(current_release.to_json())
        except Exception as e:
            logging.exception(f"Error updating release {semver} on workspace {w.name} ({w.id}): {e}")
            raise ApiHTTPError(500, f"Error updating release {semver}")

    @authenticated
    @requires_write_access
    @with_scope_admin
    async def delete(self, workspace_id, semver):
        force = self.get_argument("force", "false") == "true"
        dry_run = self.get_argument("dry_run", "false") == "true"
        workspace_name = self.get_argument("confirmation", None)
        workspace = Workspace.get_by_id(workspace_id)
        if not workspace.is_branch and workspace_name != workspace.name:
            raise ApiHTTPError.from_request_error(WorkspacesClientErrorBadRequest.confirmation_is_not_valid())

        # TODO: kept "oldest_rollback" for CLI backwards compatible < 3.2.1
        oldest_rollback = semver == "oldest_rollback"
        release = None
        if oldest_rollback:
            if workspace.is_branch:
                self.set_status(204)
                return
            release = workspace.release_oldest_rollback()
            if not release:
                self.set_status(204)
                return
        else:
            release = workspace.get_release_by_semver(semver)
        if not release:
            if oldest_rollback:
                raise ApiHTTPError(404, "Release in rollback status not found")
            else:
                raise ApiHTTPError(404, f"Release {semver} not found")

        try:
            ds, pipes, notes = await workspace.delete_release(release, force=force, dry_run=dry_run)
            if dry_run:
                self.write_json(
                    {
                        "datasources": ds,
                        "pipes": pipes,
                        "notes": notes,
                        "message": "Dry run successful",
                        "semver": release.semver,
                    }
                )
                self.set_status(200)
            else:
                self.write_json(release.to_json())
        except ReleaseStatusException as e:
            raise ApiHTTPError(400, str(e))
        except Exception as e:
            raise ApiHTTPError(500, str(e))


class APIWorkspaceReleaseDiffHandler(UserViewBase, BaseBranchHandler):
    def prepare(self) -> None:
        workspace = self.get_workspace_from_db()

        if not workspace:
            raise ApiHTTPError(
                403,
                INVALID_AUTH_MSG,
                documentation="/api-reference/overview#authentication",
            )

    @authenticated
    @with_scope_admin
    async def get(self, workspace_id, semver):
        """
        Get release diff
        """
        workspace = Workspace.get_by_id(workspace_id)
        try:
            compare_response = await Compare().release_to_live(workspace, semver)
        except CompareException as e:
            raise ApiHTTPError(400, str(e))
        except CompareExceptionNotFound as e:
            raise ApiHTTPError(404, str(e))
        except Exception as e:
            raise ApiHTTPError(500, str(e))

        self.write_json(asdict(compare_response.diff))


class APIWorkspaceRelease(UserViewBase):
    def prepare(self) -> None:
        main_or_branch = self.get_current_workspace()
        if not main_or_branch:
            raise ApiHTTPError(
                403,
                INVALID_AUTH_MSG,
                documentation="/api-reference/overview#authentication",
            )

    @authenticated
    @requires_write_access
    @with_scope_admin
    async def post(self, workspace_id: str) -> None:
        commit = self.get_argument("commit", None)
        semver = self.get_argument("semver", None)
        force = self.get_argument("force", "false") == "true"
        w = Workspace.get_by_id(workspace_id)
        if not w:
            raise ApiHTTPError(404, "Workspace not found")
        try:
            release = w.current_release
            if semver:
                release = await Workspaces.add_release(
                    workspace=w, commit=commit, semver=semver, status=ReleaseStatus.deploying, force=force
                )
            else:
                # no semver => update live Release
                if release:
                    # Require a special token scope for this. Releases should be immutable unless in "deploying" state.
                    await Workspaces.update_release(
                        w,
                        release,
                        commit=commit,
                        metadata=w,
                        status=ReleaseStatus.live,
                        force=force,
                        update_created_at=True,
                    )
                # no semver and no current release => create the first Release
                else:
                    release = await Workspaces.add_release(
                        workspace=w, commit=commit, semver="0.0.0", status=ReleaseStatus.live, force=force
                    )

        except MaxNumberOfReleasesReachedException as e:
            error_message = str(e)
            is_cli = self.get_argument("cli_version", False) is not False
            if is_cli:
                oldest_release = Release.sort_by_date(w.get_releases())[-1]
                error_message = f"{str(e)} To delete your oldest Release you can use 'tb release rm --semver {oldest_release.semver} --force'."
            raise ApiHTTPError(400, error_message)

        except ReleaseStatusException as e:
            raise ApiHTTPError(400, str(e))
        except NameAlreadyTaken:
            raise ApiHTTPError(
                400,
                "There's an internal name collission, please try with a different 'semver' or contact us at support@tinybird.co if the problem persists. ",
            )
        except Exception as e:
            raise ApiHTTPError(500, str(e))
        response = release.to_json()
        self.write_json(response)

    @authenticated
    @with_scope_admin
    async def get(self, workspace_id: str) -> None:
        """
        List releases of a workspace
        """
        workspace = Workspaces.get_by_id(workspace_id)
        releases = [r.to_json() for r in Release.sort_by_date(workspace.get_releases())]
        for r in releases:
            try:
                rollback_release = workspace.get_rollback_release_candidate(Release.from_dict(r))
                r["rollback"] = rollback_release.semver
            except ReleaseStatusException:
                r["rollback"] = ""
        self.write_json({"releases": releases})


def handlers():
    return [
        url(r"/v0/workspaces/(.+)/remote/?", APIWorkspaceRemoteHandler),
        url(r"/v0/workspaces/(.+)/remote/repos?", APIWorkspaceRemoteReposHandler),
        url(r"/v0/workspaces/(.+)/remote/changes?", APIWorkspaceRemoteChangesHandler),
        url(r"/v0/workspaces/(.+)/remote/push?", APIWorkspaceRemotePushHandler),
        url(r"/v0/workspaces/(.+)/remote/check?", APIWorkspaceRemoteCheckHandler),
        url(r"/v0/workspaces/(.+)/remote/branch?", APIWorkspaceRemoteBranchHandler),
        url(r"/v0/workspaces/(.+)/remote/access?", APIWorkspaceRemoteAccessHandler),
        url(r"/v0/workspaces/(.+)/remote/pull-request?", APIWorkspaceRemotePullRequestHandler),
        url(r"/v0/workspaces/(.+)/users/?", APIWorkspaceUsers),
        url(r"/v0/workspaces/(.+)/invite/?", APIWorkspaceInvite),
        url(r"/v0/workspaces/(.+)/releases/oldest-rollback?", APIWorkspaceReleaseOldestRollbackHandler),
        url(r"/v0/workspaces/(.+)/releases/?", APIWorkspaceRelease),
        url(r"/v0/workspaces/(.+)/releases/(.+)/diff?", APIWorkspaceReleaseDiffHandler),
        url(r"/v0/workspaces/(.+)/releases/(.+)/?", APIWorkspaceReleaseHandler),
        url(r"/v0/workspaces/(.+)/?", APIWorkspaceHandler),
        url(r"/v0/workspaces/?", APIWorkspaceCreationHandler),
        url(r"/v0/user/workspaces/?", APIUserWorkspaces),
        url(r"/v0/workspace", APIWorkspace),
    ]
