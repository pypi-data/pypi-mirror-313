import asyncio
import logging
from datetime import datetime
from enum import StrEnum
from typing import Any, Dict, List, Optional, Set, Tuple
from urllib.parse import unquote

import tornado
from opentracing import Span, Tracer
from tornado.routing import URLSpec
from tornado.web import url

from tinybird.constants import BillingPlans, Relationships
from tinybird.model import retry_transaction_in_case_of_concurrent_edition_error_async
from tinybird.orb_service import OrbAPIException, OrbCustomerNotFound, OrbService
from tinybird.organization.organization import AsyncMetric, Organization, OrganizationException, Organizations
from tinybird.organization.organization_service import OrganizationService
from tinybird.plans import PlansService
from tinybird.token_scope import scopes
from tinybird.tracing import ClickhouseTracer
from tinybird.user import User as Workspace
from tinybird.user import UserAccount, UserAccountDoesNotExist, public
from tinybird.user import Users as Workspaces
from tinybird.user_workspace import UserWorkspaceRelationship
from tinybird.workspace_service import WorkspaceService

from .base import ApiHTTPError, BaseHandler, user_authenticated


def organization_authenticated(method):
    def wrapper(self: "APIOrganizationsHandlerBase", *args, **kwargs):
        if not self.get_current_organization():
            e = ApiHTTPError(
                403,
                "invalid organization authentication",
                documentation="/api-reference/overview#authentication",
            )
            return self.write_error(e.status_code, error=e.log_message, documentation=e.documentation)
        return method(self, *args, **kwargs)

    return wrapper


class APIOrganizationsHandlerBase(BaseHandler):
    def __init__(self, application, request, **kwargs) -> None:
        self._db_organization: Optional[Organization] = None
        super().__init__(application, request, **kwargs)

    def check_xsrf_cookie(self) -> None:
        pass

    def get_date_arg(self, name: str, default: Optional[str] = None) -> datetime:
        """Gets a datetime argument, validating it's contents."""
        try:
            v: str = self.get_argument(name) if default is None else self.get_argument(name, default)
            return datetime.fromisoformat(v)
        except ValueError:
            raise ApiHTTPError(400, f"Invalid {name} '{v}'")

    @staticmethod
    def reorder_interval(_from: datetime, to: datetime) -> Tuple[datetime, datetime]:
        """Returns a tuple with the correct order for the passed dates."""
        return (_from, to) if _from < to else (to, _from)

    @staticmethod
    async def _get_workspaces(organization: Organization) -> List[Dict[str, Any]]:
        dedicated_clusters_url = organization.get_dedicated_clusters_url()

        return [
            {
                "id": w.id,
                "name": w.name,
                "in_dedicated_cluster": w.database_server in dedicated_clusters_url,
            }
            for w in await organization.get_all_workspaces()
        ]

    def get_current_organization(self) -> Optional[Organization]:
        token = self.get_user_token_from_request_or_cookie()
        if not token:
            return None

        token_data, _ = self._decode_and_authenticate_token(token)
        if not token_data:
            return None

        if not self._db_organization:
            organization_token = token_data.get("o", None)
            self._db_organization = Organization.get_by_id(organization_token) if organization_token else None

        try:
            tracer: Tracer = self.application.settings["opentracing_tracing"].tracer
            active_span: Optional[Span] = tracer.active_span
            if active_span:
                if self._db_organization:
                    active_span.set_tag("organization", self._db_organization.id)
                active_span.set_tag("token", token_data["id"])
                if "name" in token_data:
                    active_span.set_tag("token_name", token_data["name"])
        except Exception as ex:
            logging.error(f"Error saving spans data: {ex}.")

        return self._db_organization


class APIOrganizationsHandler(APIOrganizationsHandlerBase):
    @user_authenticated
    async def post(self) -> None:
        name = self.get_argument("name")
        if not name:
            raise ApiHTTPError(400, "Name is required")

        current_user: UserAccount = self.current_user
        # If the user is already an admin of an organization, we don't allow them to create a new one
        if current_user.organization_id:
            raise ApiHTTPError(400, "User is already an admin of an organization")

        # For big clients, we will set the domain in Cheriff, so new users do not create new organizations
        # Forcing them to be invited to the existing organization
        org = await Organizations.get_by_email(current_user.email)
        if org:
            raise ApiHTTPError(400, "There is already an organization with this domain")

        try:
            new_organization = Organization.create(name)
            new_organization = await OrganizationService.add_admin(
                new_organization, current_user.email, allow_external_users_as_admins=True
            )

            tracer = self.application.settings["opentracing_tracing"].tracer
            OrganizationService.trace_organization_operation(
                tracer, new_organization, "OrganizationCreated", current_user
            )
            self.write_json({"id": new_organization.id})
        except Exception as e:
            raise ApiHTTPError(500, str(e))


class APIOrganizationsInfoHandler(APIOrganizationsHandlerBase):
    @user_authenticated
    async def get(self, organization_id: str) -> None:
        organization = self._get_safe_organization(organization_id)
        api_host: str = self.application.settings["api_host"]
        with_stripe = self.get_argument("with_stripe", "false") == "true"

        workspaces = []
        for w in await organization.get_all_workspaces():
            json_value = await asyncio.to_thread(w.to_json, with_token=False)
            workspaces.append(json_value)

        # TODO: Move this to the organization.to_json() method
        response = {
            "name": organization.name,
            "creation_date": organization.created_at.isoformat(),
            "plan": {
                "name": organization.plan_details.get("name", ""),
                "start_date": organization.plan_details["start_date"],
                "end_date": organization.plan_details["end_date"],
                "commitment": organization.plan_details["commitment"],
                "billing": organization.plan_details.get("billing", ""),
            },
            "workspaces": workspaces,
            "observability": {
                "token": organization.token_observability.token,
                "storage_comsumption_url": f"{api_host}/v0/organizations/{organization.id}/metrics/storage/",
                "processed_comsumption_url": f"{api_host}/v0/organizations/{organization.id}/metrics/processed/",
            },
        }

        if with_stripe:
            response["stripe"] = {
                "api_key": self.application.settings["stripe"]["us_public_api_key"],
                "client_secret": organization.stripe_setup_intent_client_secret,
            }

        self.write_json(response)


class APIOrganizationsConsumptionHandler(APIOrganizationsHandlerBase):
    @user_authenticated
    async def get(self, organization_id: str) -> None:
        organization = self._get_safe_organization(organization_id)

        billable_only: bool = self.get_argument("billable_only", "0") == "1"
        _from, to = self.reorder_interval(self.get_date_arg("start_date"), self.get_date_arg("end_date"))

        ids: Set[str] = organization.workspace_ids

        rows = (await PlansService.get_workspaces_metrics(ids, _from, to, billable_only)).values()
        data = [
            {
                "workspace_id": r.workspace_id,
                "workspace_name": r.workspace_name,
                "processed": r.processed,
                "storage": r.storage,
                "is_billable": r.is_billable,
            }
            for r in rows
        ]

        self.write_json({"data": data})


class APIOrganizationsMetricsProcessedHandler(APIOrganizationsHandlerBase):
    @organization_authenticated
    async def get(self, organization_id: str) -> None:
        organization = self.get_current_organization()
        if not organization or organization.id != organization_id:
            raise ApiHTTPError(404, "Organization not found")

        # In case no `start_date`/`end_date` we choose a default interval
        default_start = organization.plan_details["start_date"]
        default_end = datetime.today().strftime("%Y-%m-%d 23:59:59")
        _from, to = self.reorder_interval(
            self.get_date_arg("start_date", default_start), self.get_date_arg("end_date", default_end)
        )

        ids: Set[str] = organization.workspace_ids
        workspaces: Dict[str, Workspace] = dict(
            (w.id, w) for w in (Workspace.get_by_id(id) for id in ids) if w is not None
        )

        rows = await PlansService.get_workspaces_processed_by_day(ids, _from, to)
        data = [
            {
                "day": r.day,
                "workspace_id": r.workspace_id,
                "workspace_name": workspaces[r.workspace_id].name if r.workspace_id in workspaces else "",
                "read_bytes": r.read_bytes,
                "written_bytes": r.written_bytes,
            }
            for r in rows
        ]

        self.write_json({"data": data})


class APIOrganizationsMetricsStorageHandler(APIOrganizationsHandlerBase):
    @organization_authenticated
    async def get(self, organization_id: str) -> None:
        organization = self.get_current_organization()
        if not organization or organization.id != organization_id:
            raise ApiHTTPError(404, "Organization not found")

        # In case no `start_date`/`end_date` we choose a default interval
        default_start = organization.plan_details["start_date"]
        default_end = datetime.today().strftime("%Y-%m-%d 23:59:59")
        _from, to = self.reorder_interval(
            self.get_date_arg("start_date", default_start), self.get_date_arg("end_date", default_end)
        )

        ids: Set[str] = organization.workspace_ids
        workspaces: Dict[str, Workspace] = dict(
            (w.id, w) for w in (Workspace.get_by_id(id) for id in ids) if w is not None
        )

        rows = await PlansService.get_workspaces_storage_by_day(ids, _from, to)
        data = [
            {
                "day": r.day,
                "workspace_id": r.workspace_id,
                "workspace_name": workspaces[r.workspace_id].name if r.workspace_id in workspaces else "",
                "bytes": r.bytes,
                "bytes_quarantine": r.bytes_quarantine,
            }
            for r in rows
        ]

        self.write_json({"data": data})


class UpdateMemberOperations(StrEnum):
    ADD_ADMIN = "add_admin"
    REMOVE_ADMIN = "remove_admin"


class APIOrganizationsMembersHandler(APIOrganizationsHandlerBase):
    @user_authenticated
    async def get(self, organization_id: str) -> None:
        """Returns a list of members of the Organization

        Arguments:
            only_admins: Optional. When "true", only return the organization admins
            include_workspaces: Optional. When "true", also include the list of workspaces of each org member.
        """
        organization = self._get_safe_organization(organization_id)
        only_admins = self.get_argument("only_admins", False) == "true"
        include_workspaces = self.get_argument("include_workspaces", "true") == "true"
        members = await organization.get_admins() if only_admins else await organization.get_members()
        user_data = []
        # We're not including users without workspaces in the response. This is a shortcut that we took when
        # working on the removal of users from an organization initiative. Removing a user from an org currently
        # just means that they'll be removed from all workspaces, and they will stop showing up in the org
        # members list because of this check.
        # TODO: give org admins a proper way of disabling user accounts of members of their org
        # issue: https://gitlab.com/tinybird/analytics/-/issues/14822
        members = list(u for u in members if u.is_member_of_any_workspaces)

        if include_workspaces:
            # Gather all get_workspaces calls concurrently
            # TODO: We should use optimize the `get_workspaces`` method to speed up the response
            workspaces_tasks = [u.get_workspaces(with_environments=False) for u in members]
            all_workspaces = await asyncio.gather(*workspaces_tasks)

            for u, user_workspaces in zip(members, all_workspaces):
                workspaces = [
                    {"workspace_id": w["id"], "workspace_name": w["name"], "role": w["role"]}
                    for w in user_workspaces
                    if w["id"] in organization.workspace_ids
                ]

                user_data.append(
                    {
                        "id": u.id,
                        "email": u.email,
                        "workspaces": workspaces,
                        "is_admin": organization.user_is_admin(u),
                    }
                )
        else:
            for u in members:
                user_data.append(
                    {
                        "id": u.id,
                        "email": u.email,
                        "is_admin": organization.user_is_admin(u),
                    }
                )

        self.write_json({"data": user_data})

    @user_authenticated
    async def put(self, organization_id: str) -> None:
        """Add or remove an admin to an Organization

        Arguments:
            operation: "add_admin" or "remove_admin".
            member_email: email of the member to be given or revoked org admin privileges.
        """
        organization = self._get_safe_organization(organization_id)

        valid_operations = [str(val) for val in UpdateMemberOperations]
        operation: Optional[str] = self.get_argument("operation", None)

        if not operation or operation not in valid_operations:
            raise tornado.web.HTTPError(
                400,
                f'Invalid operation "{operation}", valid operations are {[str(option) for option in UpdateMemberOperations]}',
            )

        member_email: str = self.get_argument("member_email")
        if operation == UpdateMemberOperations.ADD_ADMIN:
            try:
                await OrganizationService.add_admin(organization, member_email)
            except UserAccountDoesNotExist:
                raise tornado.web.HTTPError(404, f"User {member_email} not found")
            except OrganizationException as e:
                raise tornado.web.HTTPError(400, str(e))

        elif operation == UpdateMemberOperations.REMOVE_ADMIN:
            try:
                await OrganizationService.remove_admin(organization, member_email)
            except UserAccountDoesNotExist:
                raise tornado.web.HTTPError(404, f"User {member_email} not found")
            except OrganizationException as e:
                raise tornado.web.HTTPError(400, str(e))

        self.write_json({})


class APIOrganizationsMembersWorkspacesHandler(APIOrganizationsHandlerBase):
    @user_authenticated
    async def get(self, organization_id: str, member_id: str) -> None:
        """Returns the workspaces of another member of the org

        Only org admins can get the workspaces of other users in their org
        """
        response: dict[Any, Any] = {}

        requested_user = UserAccount.get_by_id(member_id)

        org = self._get_safe_organization(organization_id)

        if requested_user is None:
            raise ApiHTTPError(404, "User not found")

        # Check if requested user is in org
        if not await org.user_is_member(requested_user):
            raise ApiHTTPError(404, "User not found")

        workspaces = await requested_user.get_workspaces(
            with_token=False, with_environments=False, with_members_and_owner=False
        )
        response["workspaces"] = list()
        for ws in workspaces:
            if ws["id"] not in org.workspace_ids:
                continue
            relationship = UserWorkspaceRelationship.get_by_user_and_workspace(requested_user.id, ws["id"])
            assert relationship is not None
            response["workspaces"].append(
                {"workspace_id": ws["id"], "workspace_name": ws["name"], "role": relationship.relationship}
            )
        self.write_json(response)
        return

    async def get_tokens_last_activity(
        self, token_ids: list[str], period_in_days: Optional[int] = None
    ) -> List[Dict[str, str]]:
        """Gets tokens last activity from the tokens_last_usage datasource in Internal"""
        admin_user_tokens_ids_str = ", ".join([f"'{id}'" for id in token_ids])
        tokens_last_usage_ds = Workspaces.get_datasource(public.get_public_user(), "tokens_last_usage")
        if tokens_last_usage_ds is None:
            logging.exception("tokens_last_usage datasource not found in Internal")
            raise ApiHTTPError(500)
        period_frag = (
            "" if period_in_days is None else f"AND last_request_time >= now() - INTERVAL {period_in_days} DAY"
        )
        internal_tokens_last_usage_query = f"""
        SELECT
            workspace,
            token,
            maxIf(toString(last_request_time), request_origin = 'ui') as ui,
            maxIf(toString(last_request_time), request_origin = 'cli') as cli,
            maxIf(toString(last_request_time), request_origin not in ('ui', 'cli')) as other
        FROM {tokens_last_usage_ds.id}
        WHERE token IN ({admin_user_tokens_ids_str})
        {period_frag}
        GROUP BY token, workspace
        """
        tokens_last_activity = await public.query_internal(query=internal_tokens_last_usage_query)
        return tokens_last_activity["data"]

    @user_authenticated
    async def delete(self, organization_id: str, member_id: str) -> None:
        """Removes a user from a list of workspaces

        Only Organization admins can perform this action, and only for members of their org. If the user is the only
        admin in any of the workspaces, the org admin is added as an admin to not leave the workspaces empty.

        Arguments:
            workspace_ids: comma-separated list of workspace IDs from which the user will be removed.
            dry_run: if "true", we only return the info of the changes that would take place.
        """
        org_member = UserAccount.get_by_id(member_id)
        org = self._get_safe_organization(organization_id)

        if org_member is None:
            raise ApiHTTPError(404, "User not found")

        # Check if requested user is in org
        if not org.contains_email(org_member.email):
            raise ApiHTTPError(404, "User not found")

        workspace_ids = self.get_argument("workspace_ids").split(",")
        dry_run = self.get_argument("dry_run", "false") == "true"
        # We'll report back the workspace_ids that fall in each of the two possible outcomes:
        #   1. user removed, no side effects
        #   2. user removed, org admin made workspace admin
        user_removed_workspaces: List[Dict[str, str]] = []
        user_removed_and_org_admin_added_workspaces: List[Dict[str, str]] = []
        result = {
            "user_removed": user_removed_workspaces,
            "user_removed_and_org_admin_added": user_removed_and_org_admin_added_workspaces,
        }

        admin_user_tokens_ids: list[str] = []
        for ws_id in set(workspace_ids):
            workspace = Workspace.get_by_id(ws_id)
            if workspace is None:
                continue
            if workspace.id not in org.workspace_ids:
                continue
            if not UserWorkspaceRelationship.user_has_access(member_id, workspace.id):
                continue
            admin_user_tokens_ids.append(
                workspace.get_access_tokens_for_resource(member_id, scope=scopes.ADMIN_USER)[0].id
            )
            admins = list(filter(lambda u: u["role"] == Relationships.ADMIN, workspace.members))
            # Check if we're trying to remove the only admin, and add Org admin to workspace as admin if yes
            will_make_org_admin_workspace_admin = False
            if len(admins) == 1 and admins[0]["id"] == org_member.id:
                will_make_org_admin_workspace_admin = True
                user_removed_and_org_admin_added_workspaces.append({"id": workspace.id, "name": workspace.name})
            else:
                user_removed_workspaces.append({"id": workspace.id, "name": workspace.name})

            if not dry_run:
                if will_make_org_admin_workspace_admin:
                    await Workspaces.add_users_to_workspace_async(
                        workspace_id=ws_id, users_emails=[self.current_user.email], role="admin"
                    )
                workspace.remove_users_from_workspace(user_emails=[org_member.email], allow_removing_admins=True)

        if not admin_user_tokens_ids:
            self.write_json(result)
            return

        # Get tokens last activity in the last 7 days
        tokens_last_activity = await self.get_tokens_last_activity(admin_user_tokens_ids, period_in_days=7)

        # Merge operations that will be performed with token activity info
        last_activity_per_workspace: Dict[str, Dict[str, str]] = {}
        for x in tokens_last_activity:
            assert x["workspace"] not in last_activity_per_workspace
            last_activity_per_workspace[x["workspace"]] = {k: x[k] for k in ("ui", "cli", "other")}
        for _, workspaces in result.items():
            for workspace in workspaces:  # type: ignore
                workspace["token_last_usage"] = last_activity_per_workspace.get(workspace["id"], {})

        self.write_json(result)


class APIOrganizationsWorkspacesHandler(APIOrganizationsHandlerBase):
    @user_authenticated
    async def get(self, organization_id: str) -> None:
        organization = self._get_safe_organization(organization_id)
        self.write_json({"workspaces": await self._get_workspaces(organization)})


class APIOrganizationsCommitmentHandler(APIOrganizationsHandlerBase):
    @user_authenticated
    async def put(self, organization_id: str) -> None:
        assert isinstance(self.current_user, UserAccount)

        workspace_id: str = self.get_argument("workspace_id")

        organization = self._get_safe_organization(organization_id)
        if workspace_id not in organization.workspace_ids:
            raise ApiHTTPError(400, f"The workspace {workspace_id} doesn't belong to this organization")

        workspace: Optional[Workspace] = Workspace.get_by_id(workspace_id)
        if not workspace:
            raise ApiHTTPError(404, "Workspace not found")

        workspace = await Workspaces.change_workspace_plan(workspace, BillingPlans.CUSTOM)
        logging.info(
            f"User {self.current_user.email} changed workspace {workspace.name} ({workspace_id}) plan to 'custom' for organization {organization.name} ({organization_id})"
        )

        tracer: ClickhouseTracer = self.application.settings["opentracing_tracing"].tracer
        WorkspaceService.trace_workspace_operation(tracer, workspace, "PlanChanged", self.current_user)

        self.write_json({"workspaces": await self._get_workspaces(organization)})


class APIOrganizationsTokensHandler(APIOrganizationsHandlerBase):
    @user_authenticated
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def post(self, organization_id: str, refresh_token_name_or_token: str) -> None:
        organization = self._get_safe_organization(organization_id)

        unquoted_token_name_or_token = unquote(refresh_token_name_or_token)
        organization, refreshed = Organizations.refresh_token(organization, unquoted_token_name_or_token)
        if not refreshed:
            raise ApiHTTPError(404, "Token not found")

        self.write_json({"token": refreshed})


class APIOrganizationsCreditHandler(APIOrganizationsHandlerBase):
    @user_authenticated
    async def get(self, organization_id: str) -> None:
        organization = self._get_safe_organization(organization_id)

        if not organization.in_dedicated_infra_pricing:
            raise tornado.web.HTTPError(405, "Organization not in a dedicated infra-based pricing")

        try:
            credit_balance = await OrbService.get_organization_credit_balance(organization)
            data = {
                "total_credits": credit_balance.total_credits,
                "current_balance": credit_balance.current_balance,
                "commitment_start_date": self.optional_date_to_str(credit_balance.subscription.commitment_start_date),
                "commitment_end_date": self.optional_date_to_str(credit_balance.subscription.commitment_end_date),
                "customer_portal": credit_balance.subscription.customer_portal,
            }

            self.write_json({"data": data})
        except OrbCustomerNotFound as e:
            raise ApiHTTPError(404, f"Orb customer not found for Organization {organization.id}. Error: {e}")
        except OrbAPIException as e:
            raise ApiHTTPError(502, str(e))
        except Exception as e:
            raise ApiHTTPError(500, str(e))


class APIClusterMetricsHandler(APIOrganizationsHandlerBase):
    @staticmethod
    def json_to_prometheus(metrics: List[AsyncMetric], organization: Organization) -> str:
        prometheus_output = []

        for metric in metrics:
            prometheus_output.append(f"# HELP {metric.metric} {metric.description}.")
            prometheus_output.append(f"# TYPE {metric.metric} gauge")
            metric_labels = f'{{cluster="{metric.cluster}", host="{metric.host}"}}'
            prometheus_output.append(f"{metric.metric}{metric_labels} {metric.value}")
        return "\n".join(prometheus_output)

    @organization_authenticated
    async def get(self) -> None:
        organization = self.get_current_organization()
        if not organization:
            raise ApiHTTPError(404, "Organization not found")

        if not organization.in_dedicated_infra_pricing:
            raise ApiHTTPError(403, "Organization does not have any infrastructure commitment")

        # TODO(eclbg): we shouldn't expose to clients an endpoint that uses clusterAllReplicas internally, as we know
        # that it has poor performance because of how it handles connections. We use it in other places of the app where
        # we more or less control the volume of queries.
        metrics = await organization.get_cluster_metrics()
        prometheus_output = self.json_to_prometheus(metrics, organization)
        self.set_header("Content-Type", "text/plain")
        self.write(prometheus_output)


def handlers() -> List[URLSpec]:
    return [
        url(r"/v0/organizations/(.+)/tokens/(.+)/refresh/?", APIOrganizationsTokensHandler),
        url(r"/v0/organizations/(.+)/metrics/processed/?", APIOrganizationsMetricsProcessedHandler),
        url(r"/v0/organizations/(.+)/metrics/storage/?", APIOrganizationsMetricsStorageHandler),
        url(r"/v0/organizations/(.+)/members/?", APIOrganizationsMembersHandler),
        url(r"/v0/organizations/(.+)/members/(.*)/workspaces?", APIOrganizationsMembersWorkspacesHandler),
        url(r"/v0/organizations/(.+)/workspaces/?", APIOrganizationsWorkspacesHandler),
        url(r"/v0/organizations/(.+)/commitment/?", APIOrganizationsCommitmentHandler),
        url(r"/v0/organizations/(.+)/consumption/?", APIOrganizationsConsumptionHandler),
        url(r"/v0/organizations/(.+)/credit/?", APIOrganizationsCreditHandler),
        url(r"/v0/organizations/(.+)/?", APIOrganizationsInfoHandler),
        url(r"/v0/organizations/?", APIOrganizationsHandler),
        url(r"/v0/metrics?", APIClusterMetricsHandler),
    ]
