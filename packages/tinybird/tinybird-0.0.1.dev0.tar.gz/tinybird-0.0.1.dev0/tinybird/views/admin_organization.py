import asyncio
import logging
from datetime import datetime
from typing import Tuple

import tornado.web

from tinybird.constants import CHCluster
from tinybird.organization.organization import (
    DedicatedCluster,
    DedicatedClusterNotFound,
    Organization,
    OrganizationCommitmentsPlans,
    OrganizationException,
    Organizations,
)
from tinybird.organization.organization_service import (
    ClusterHasOrgWorkspaces,
    ClusterHasWorkspacesNotInOrg,
    OrganizationService,
    UnreachableCluster,
)
from tinybird.user import User, UserAccountDoesNotExist, public
from tinybird.views.admin import WebCheriffBaseHandler, admin_authenticated


def _scale_value_from_bytes(value: int) -> Tuple[int, str]:
    """
    >>> _scale_value_from_bytes(5*1000**2)
    (5, 'mb')
    >>> _scale_value_from_bytes(6*1000**3)
    (6, 'gb')
    >>> _scale_value_from_bytes(7*1000**4)
    (7, 'tb')
    >>> _scale_value_from_bytes(7*1000**5)
    (7, 'pb')
    >>> _scale_value_from_bytes(7000*1000**5)
    (7000, 'pb')
    """
    value = int(value / (1000 * 1000))  # value always comes as bytes and minimun unit is MB
    for unit in ["mb", "gb", "tb", "pb"]:
        next_value = value / 1000
        if not next_value.is_integer():
            return int(value), unit
        value = int(next_value)
    return int(value * 1000), unit


class OrganizationsAdminHandler(WebCheriffBaseHandler):
    @tornado.web.authenticated
    @admin_authenticated
    async def get(self) -> None:
        def calculate_byte_commitment_value_to_show(org: Organization, commitment_concept: str) -> str:
            assert commitment_concept in ("processed", "storage")

            if not org.plan_details["commitment"][commitment_concept]:
                return ""

            value_scaled, unit = _scale_value_from_bytes(org.plan_details["commitment"][commitment_concept])

            return f"{value_scaled} {unit.upper()}"

        all_organizations = await asyncio.to_thread(Organization.get_all)

        organizations_values = [
            {
                "id": org.id,
                "name": org.name,
                "domain": org.domain or "",
                "dedicated_clusters": org.get_dedicated_clusters_name(),
                "billing_plan": org.plan_details["billing"],
                "contract_term": f"{org.plan_details['start_date']} - {org.plan_details['end_date']}",
                "processed_data": calculate_byte_commitment_value_to_show(org, "processed"),
                "storage": calculate_byte_commitment_value_to_show(org, "storage"),
            }
            for org in all_organizations
        ]

        self.render(
            "organizations_admin.html",
            organizations=organizations_values,
        )

    @admin_authenticated
    async def post(self) -> None:
        name = self.get_argument("name")
        if not name:
            raise tornado.web.HTTPError(400, "Name is required")

        new_organization = Organization.create(name)
        tracer = self.application.settings["opentracing_tracing"].tracer
        OrganizationService.trace_organization_operation(
            tracer, new_organization, "OrganizationCreated", self.current_user
        )

        return self.redirect(self.reverse_url("organization_admin", new_organization.id))


class OrganizationAdminHandler(WebCheriffBaseHandler):
    @tornado.web.authenticated
    @admin_authenticated
    async def get(self, organization_id: str) -> None:
        organization = Organization.get_by_id(organization_id)
        if not organization:
            raise tornado.web.HTTPError(404)

        # TODO use the cluster code from the WorkspaceAdminHandler. It doesn't use default values
        """
        client = HTTPClient(User.default_database_server, database=None)

        async def query(sql):
            _, body = await client.query(f'{sql} FORMAT JSON', max_execution_time=2)
            return json.loads(body)['data']

        try:
            results = await query("SELECT cluster FROM system.clusters")
            clusters = list(set([r['cluster'] for r in results]))
        except Exception as e:
            logging.warning(e)
            clusters = ['tinybird', 'thn', 'vercel', 'itxlive']
        """

        processed = organization.plan_details["commitment"]["processed"]
        processed_data, processed_data_unit = _scale_value_from_bytes(processed) if processed else ("", "mb")

        storage = organization.plan_details["commitment"]["storage"]
        storage_data, storage_data_unit = _scale_value_from_bytes(storage) if storage else ("", "mb")

        data_transfer_intra = organization.plan_details["commitment"].get("data_transfer_intra", None)
        data_transfer_intra_data, data_transfer_intra_data_unit = (
            _scale_value_from_bytes(data_transfer_intra) if data_transfer_intra else ("", "mb")
        )
        data_transfer_inter = organization.plan_details["commitment"].get("data_transfer_inter", None)
        data_transfer_inter_data, data_transfer_inter_data_unit = (
            _scale_value_from_bytes(data_transfer_inter) if data_transfer_inter else ("", "mb")
        )

        machine_size = organization.plan_details["commitment"].get("machine_size", None)

        def get_date(dt: str) -> str:
            if not dt:
                return ""
            try:
                return datetime.fromisoformat(dt).strftime("%Y-%m-%d")
            except Exception:
                return ""

        organization_dict = {
            "id": organization.id,
            "name": organization.name,
            "domain": organization.domain or "",
            "members": await organization.get_admins(),
            "workspaces": await organization.get_all_workspaces(),
            "plan_details": {
                "start_date": get_date(organization.plan_details.get("start_date", "")),
                "end_date": get_date(organization.plan_details.get("end_date", "")),
                "processed_data": processed_data,
                "processed_data_unit": processed_data_unit,
                "storage_data": storage_data,
                "storage_data_unit": storage_data_unit,
                "data_transfer_inter_data": data_transfer_inter_data,
                "data_transfer_inter_data_unit": data_transfer_inter_data_unit,
                "data_transfer_intra_data": data_transfer_intra_data,
                "data_transfer_intra_data_unit": data_transfer_intra_data_unit,
                "billing": organization.plan_details.get("billing", OrganizationCommitmentsPlans.TOTAL_USAGE),
                "machine_size": machine_size,
                "orb_external_customer_id": organization.orb_external_customer_id,
                "max_qps": organization.max_qps,
            },
            "dedicated_clusters": organization.get_dedicated_clusters(),
        }

        self.render(
            "organization_admin.html",
            organization=organization_dict,
            commitment_plans=OrganizationCommitmentsPlans._items,
            clusters=[],
        )

    @admin_authenticated
    async def post(self, organization_id: str) -> None:
        operation = self.get_argument("operation")
        org = Organization.get_by_id(organization_id)
        if not org:
            raise tornado.web.HTTPError(400, "Organization doesn't exist")

        tracer = self.application.settings["opentracing_tracing"].tracer

        if operation == "update_general_and_commitment":
            name = self.get_argument("name")
            domain = self.get_argument("domain")
            try:
                await OrganizationService.update_name_and_domain(org, name, domain, self.current_user, tracer)
            except OrganizationException as e:
                raise tornado.web.HTTPError(400, str(e)) from e

            start_commitment = self.get_argument("start_commitment")
            end_commitment = self.get_argument("end_commitment")
            processed_data = self.get_argument("processed_data")
            processed_data_unit = self.get_argument("processed_data_unit")
            storage_data = self.get_argument("storage_data")
            storage_data_unit = self.get_argument("storage_data_unit")
            data_transfer_intra_data = self.get_argument("data_transfer_intra_data")
            data_transfer_intra_data_unit = self.get_argument("data_transfer_intra_data_unit")
            data_transfer_inter_data = self.get_argument("data_transfer_inter_data")
            data_transfer_inter_data_unit = self.get_argument("data_transfer_inter_data_unit")
            billing_plan = self.get_argument("billing_plan")
            orb_external_customer_id = self.get_argument("orb_external_customer_id", "")
            max_qps = self.get_argument("max_qps", None)

            if orb_external_customer_id and billing_plan not in [
                OrganizationCommitmentsPlans.INFRASTRUCTURE_USAGE,
                OrganizationCommitmentsPlans.SHARED_INFRASTRUCTURE_USAGE,
            ]:
                raise tornado.web.HTTPError(400, "Orb external customer ID can only be set for infra-based plans")

            size_scale_to_bytes = {"mb": 1000**2, "gb": 1000**3, "tb": 1000**4, "pb": 1000**5}
            processed = int(processed_data) * size_scale_to_bytes[processed_data_unit] if processed_data else None
            storage = int(storage_data) * size_scale_to_bytes[storage_data_unit] if storage_data else None
            data_transfer_intra = (
                int(data_transfer_intra_data) * size_scale_to_bytes[data_transfer_intra_data_unit]
                if data_transfer_intra_data
                else None
            )
            data_transfer_inter = (
                int(data_transfer_inter_data) * size_scale_to_bytes[data_transfer_inter_data_unit]
                if data_transfer_inter_data
                else None
            )

            commitment_max_qps = int(max_qps) if max_qps else None

            updated_org = Organizations.update_commitment_information(
                org,
                start_date=start_commitment,
                end_date=end_commitment,
                commited_processed=processed,
                commited_storage=storage,
                commited_data_transfer_intra=data_transfer_intra,
                commited_data_transfer_inter=data_transfer_inter,
                commitment_billing=billing_plan,
                commitment_max_qps=commitment_max_qps,
            )

            if org.plan_details.get("billing") != billing_plan:
                OrganizationService.trace_organization_operation(
                    tracer, updated_org, "OrganizationPlanChanged", self.current_user
                )

            if org.orb_external_customer_id != orb_external_customer_id:
                updated_org = await Organizations.set_orb_external_customer_id(updated_org, orb_external_customer_id)
                OrganizationService.trace_organization_operation(
                    tracer, updated_org, "OrganizationOrbExternalCustomerIdChanged", self.current_user
                )

        elif operation == "add_admin":
            user_email = self.get_argument("user_email")
            try:
                await OrganizationService.add_admin(org, user_email, allow_external_users_as_admins=True)
            except UserAccountDoesNotExist:
                raise tornado.web.HTTPError(404, f"User {user_email} not found")
            except OrganizationException as e:
                raise tornado.web.HTTPError(400, str(e))

        elif operation == "remove_admin":
            user_email = self.get_argument("user_email")
            try:
                await OrganizationService.remove_admin(org, user_email)
            except UserAccountDoesNotExist:
                raise tornado.web.HTTPError(404, f"User {user_email} not found")

        elif operation == "add_workspace":
            workspace_id = self.get_argument("workspace_id")
            if workspace_id == public.get_public_user().id:
                raise tornado.web.HTTPError(400, "Please, don't add the public workspace to an organization")
            _ = OrganizationService.add_workspace_to_organization(org, workspace_id, self.current_user, tracer)

        elif operation == "remove_workspace":
            workspace_id = self.get_argument("workspace_id")
            if not User.get_by_id(workspace_id):
                raise tornado.web.HTTPError(404, f"Workspace {workspace_id} not found")
            _ = await OrganizationService.remove_workspace_from_organization(
                org, workspace_id, self.current_user, tracer
            )

        elif operation == "remove_organization":
            Organizations.remove_organization(org, self.current_user, tracer)
            OrganizationService.trace_organization_operation(tracer, org, "OrganizationDeleted", self.current_user)
            self.redirect(self.reverse_url("organizations_admin"))
            return

        elif operation == "add_dedicated_cluster":
            cluster_name = self.get_argument("cluster_name")
            server_url = self.get_argument("server_url")
            expose_metrics = self.get_argument("expose_metrics", "false").lower() == "true"
            try:
                cluster = CHCluster(name=cluster_name, server_url=server_url)
                await OrganizationService.add_dedicated_cluster(
                    org, DedicatedCluster(cluster=cluster, expose_metrics=expose_metrics), self.current_user, tracer
                )
            except (UnreachableCluster, ClusterHasWorkspacesNotInOrg) as e:
                raise tornado.web.HTTPError(400, f"Couldn't add dedicated cluster. {e}")
            except Exception as e:
                logging.exception(e)
                raise tornado.web.HTTPError(500, f"Couldn't add dedicated cluster. {e}")

        elif operation == "remove_dedicated_cluster":
            cluster_name = self.get_argument("cluster_name")
            server_url = self.get_argument("server_url")
            expose_metrics = self.get_argument("expose_metrics", "false").lower() == "true"
            try:
                cluster = CHCluster(name=cluster_name, server_url=server_url)
                await OrganizationService.remove_dedicated_cluster(
                    org, DedicatedCluster(cluster=cluster, expose_metrics=expose_metrics), self.current_user, tracer
                )
            except ClusterHasOrgWorkspaces as e:
                raise tornado.web.HTTPError(400, f"Couldn't remove dedicated cluster. {e}")
            except DedicatedClusterNotFound as e:
                raise tornado.web.HTTPError(400, f"Couldn't find dedicated cluster. {e}")
            except Exception as e:
                logging.exception(e)
                raise tornado.web.HTTPError(500, f"Couldn't remove dedicated cluster. {e}")
        elif operation == "toggle_cluster_expose_metrics":
            cluster_name = self.get_argument("cluster_name")
            server_url = self.get_argument("server_url")
            expose_metrics = self.get_argument("expose_metrics", "false").lower() == "true"

            try:
                cluster = CHCluster(name=cluster_name, server_url=server_url)
                await OrganizationService.toggle_dedicated_cluster_expose_metrics(
                    org, DedicatedCluster(cluster=cluster, expose_metrics=expose_metrics)
                )
            except DedicatedClusterNotFound as e:
                raise tornado.web.HTTPError(400, f"Couldn't find dedicated cluster. {e}")
            except Exception as e:
                logging.exception(e)
                raise tornado.web.HTTPError(500, f"Couldn't update dedicated cluster. {e}")

        self.redirect(self.reverse_url("organization_admin", organization_id))
