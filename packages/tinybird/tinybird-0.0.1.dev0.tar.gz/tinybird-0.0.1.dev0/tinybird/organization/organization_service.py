import logging
from datetime import datetime
from typing import Dict, List, Optional, Union

from tinybird.ch import ch_get_databases_metadata, ch_server_is_reachable_and_has_cluster
from tinybird.model import retry_transaction_in_case_of_concurrent_edition_error_sync
from tinybird.organization.organization import DedicatedCluster, Organization, OrganizationException, Organizations
from tinybird.tracing import ClickhouseTracer
from tinybird.user import User as Workspace
from tinybird.user import (
    UserAccount,
    UserAccountAlreadyBelongsToOrganization,
    UserAccounts,
    WorkspaceAlreadyBelongsToOrganization,
)
from tinybird.user import UserDoesNotExist as WorkspaceDoesNotExist
from tinybird.workspace_service import WorkspaceService


class UnreachableCluster(Exception):
    pass


class ClusterHasWorkspacesNotInOrg(Exception):
    pass


class ClusterHasOrgWorkspaces(Exception):
    pass


class OrganizationService:
    @staticmethod
    async def remove_workspace_from_organization(
        organization: Union[Organization, str],
        workspace_id: str,
        user: Optional[UserAccount] = None,
        tracer: Optional[ClickhouseTracer] = None,
    ) -> Organization:
        org = organization if isinstance(organization, Organization) else Organization.get_by_id(organization)
        assert isinstance(org, Organization)

        workspace = Workspace.get_by_id(workspace_id)
        assert isinstance(workspace, Workspace)

        org = Organizations.remove_workspace(org, Workspace.get_by_id(workspace_id))

        if tracer:
            workspace = Workspace.get_by_id(workspace_id)
            WorkspaceService.trace_workspace_operation(tracer, workspace, "WorkspaceOrgChanged", user)

        return org

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def add_workspace_to_organization(
        org: Organization,
        workspace_id: str,
        user: Optional[UserAccount] = None,
        tracer: Optional[ClickhouseTracer] = None,
    ) -> Organization:
        workspace = Workspace.get_by_id(workspace_id)
        if not workspace:
            raise WorkspaceDoesNotExist(f"Workspace {workspace_id} not found")

        try:
            org = Organizations.add_workspace(org, workspace)

            if tracer:
                workspace = Workspace.get_by_id(workspace_id)
                WorkspaceService.trace_workspace_operation(tracer, workspace, "WorkspaceOrgChanged", user)

            return org
        except WorkspaceAlreadyBelongsToOrganization as ex:
            prev_org = Organization.get_by_id(ex.organization_id)
            if prev_org:
                msg = f"Workspace {workspace.name} ({workspace.id}) already belongs to organization {prev_org.name} ({prev_org.id})"
            else:
                msg = f"Workspace {workspace.name} ({workspace.id}) already belongs to organization {ex.organization_id} but the organization doesn't exist"
                logging.warning(f"Inconsistency: {msg}")
            raise OrganizationException(msg)

    @staticmethod
    async def update_name_and_domain(
        organization: Organization,
        name: str,
        domain: str,
        user: Optional[UserAccount] = None,
        tracer: Optional[ClickhouseTracer] = None,
    ) -> Organization:
        """Updates an org's name and domain, and adds existing workspaces that belong to the org's domain."""
        org = Organizations.update_name_and_domain(organization, name, domain)
        if tracer:
            if organization.name != name:
                OrganizationService.trace_organization_operation(tracer, org, "OrganizationRenamed", user)

            if organization.domain != domain:
                OrganizationService.trace_organization_operation(tracer, org, "OrganizationDomainChanged", user)

        existing_workspaces = await OrganizationService.get_existing_workspaces_outside_organization(org)
        for workspace in existing_workspaces:
            try:
                org = Organizations.add_workspace(org, workspace)

                if tracer:
                    workspace = Workspace.get_by_id(workspace.id)
                    WorkspaceService.trace_workspace_operation(tracer, workspace, "WorkspaceOrgChanged", user)
            except Exception as e:
                logging.exception(e)
        return org

    @staticmethod
    async def get_existing_workspaces_outside_organization(organization: Organization) -> List[Workspace]:
        """Returns a list of workspaces that belong to the organization (by admin email domain) but aren't part of the org"""
        result: List[Workspace] = []

        for user in await organization.get_members():
            owned_relationship = user.owned_workspaces
            for ws_user_relationship in owned_relationship:
                workspace = Workspace.get_by_id(ws_user_relationship.workspace_id)
                if (
                    not workspace
                    or workspace.organization_id
                    or workspace.origin  # both, branches and releases have origin
                    or workspace.name.lower() == "internal"
                ):
                    continue

                result.append(workspace)
        return result

    @staticmethod
    async def add_admin(
        organization: Organization, user_email: str, allow_external_users_as_admins: bool = False
    ) -> Organization:
        user = UserAccount.get_by_email(user_email)

        if not allow_external_users_as_admins and not (await organization.user_is_member(user)):
            raise OrganizationException(f"User '{user_email}' is not a member of the Organization")

        try:
            UserAccounts.set_organization_id(user, organization.id)
            organization = await Organizations.add_admin(organization, user)
        except UserAccountAlreadyBelongsToOrganization as ex:
            prev_org = Organization.get_by_id(ex.organization_id)
            if prev_org:
                msg = f"User {user.email} ({user.id}) already belongs to organization {prev_org.name} ({prev_org.id})"
            else:
                msg = f"User {user.email} ({user.id}) already belongs to organization {ex.organization_id} but the organization doesn't exist"
                logging.warning(f"Inconsistency: {msg}")
            raise OrganizationException(msg)
        return organization

    @staticmethod
    async def remove_admin(organization: Organization, user_email: str) -> Organization:
        user = UserAccount.get_by_email(user_email)

        if not organization.user_is_admin(user):
            raise OrganizationException(f"User '{user_email}' is not an admin of the Organization")

        user = UserAccount.get_by_email(user_email)
        organization = await Organizations.remove_admin(organization, user)
        UserAccounts.set_organization_id(user, None)
        return organization

    @staticmethod
    async def add_dedicated_cluster(
        organization: Organization,
        dedicated_cluster: DedicatedCluster,
        user: Optional[UserAccount],
        tracer: Optional[ClickhouseTracer],
    ) -> Organization:
        # Check that the cluster is reachable
        cluster = dedicated_cluster.cluster
        if not await ch_server_is_reachable_and_has_cluster(server_url=cluster.server_url, cluster_name=cluster.name):
            raise UnreachableCluster(f"Cluster unreachable: {cluster = }")

        # TODO(eclbg): this check made a lot of sense, but wasn't practical as most client clusters have workspaces that
        # don't belong to their org. We should investigate why is that so we can bring the check back. And reenable the
        # tests.
        # Check that the cluster doesn't have any workspaces that don't belong to the org
        # databases_in_cluster = await ch_get_databases_metadata(
        #     database_servers=[(cluster.server_url, cluster.name)],
        #     skip_unavailable_replicas=False,
        # )
        # for database in databases_in_cluster.get(cluster.name, []):
        #     try:
        #         workspace = Workspace.get_by_database(database)
        #     except WorkspaceDoesNotExist:
        #         logging.warning(f"Orphan database {database} in cluster {cluster}")
        #         continue
        #     if not workspace.deleted and workspace.origin is None and workspace.organization_id != organization.id:
        #         raise ClusterHasWorkspacesNotInOrg(
        #             f"{workspace} {workspace.name = } is in cluster {cluster} and does not belong to org"
        #         )

        organization = Organizations.add_dedicated_cluster(organization, dedicated_cluster)

        if tracer:
            OrganizationService.trace_organization_operation(
                tracer, organization, "OrganizationDedicatedClusterAdded", user
            )

        return organization

    @staticmethod
    async def remove_dedicated_cluster(
        organization: Organization,
        dedicated_cluster: DedicatedCluster,
        user: Optional[UserAccount],
        tracer: Optional[ClickhouseTracer],
    ) -> Organization:
        cluster = dedicated_cluster.cluster
        if await ch_server_is_reachable_and_has_cluster(server_url=cluster.server_url, cluster_name=cluster.name):
            # Check that the cluster doesn't have workspaces of the org
            databases_in_cluster = await ch_get_databases_metadata(
                database_servers=[(cluster.server_url, cluster.name)],
                skip_unavailable_replicas=False,
            )
            for database in databases_in_cluster.get(cluster.name, []):
                try:
                    workspace = Workspace.get_by_database(database)
                except WorkspaceDoesNotExist:
                    logging.warning(f"Orphan database {database} in cluster {cluster}")
                    continue
                if workspace.organization_id == organization.id:
                    raise ClusterHasOrgWorkspaces(
                        f"The org still has workspaces in this cluster. Found {workspace} {workspace.name = }"
                    )
        organization = Organizations.remove_dedicated_cluster(organization, dedicated_cluster)

        if tracer:
            OrganizationService.trace_organization_operation(
                tracer, organization, "OrganizationDedicatedClusterRemoved", user
            )

        return organization

    @staticmethod
    async def toggle_dedicated_cluster_expose_metrics(
        organization: Organization, dedicated_cluster: DedicatedCluster
    ) -> Organization:
        cluster = dedicated_cluster.cluster
        if not await ch_server_is_reachable_and_has_cluster(server_url=cluster.server_url, cluster_name=cluster.name):
            raise UnreachableCluster(f"Cluster unreachable: {cluster = }")

        return Organizations.toggle_dedicated_cluster_expose_metrics(organization, dedicated_cluster)

    @classmethod
    def trace_organization_operation(
        cls,
        tracer: ClickhouseTracer,
        organization: Organization,
        operation: str,
        user: Optional[UserAccount] = None,
        extra: Optional[Dict[str, str]] = None,
    ):
        span = None

        try:
            span = tracer.start_span()
            span.set_operation_name(operation)
            span.set_tag("organization", organization.id)
            span.set_tag("organization_name", organization.name)
            span.set_tag("organization_domain", organization.domain)
            span.set_tag("billing_plan", organization.plan_details.get("billing", ""))
            span.set_tag("orb_external_customer_id", organization.orb_external_customer_id)
            span.set_tag("dedicated_clusters", organization.get_dedicated_clusters_url())
            span.set_tag("created_at", organization.created_at.strftime("%Y-%m-%d %H:%M:%S"))
            span.set_tag("cpus", str(organization.commitment_cpu or "unknown"))
            if user:
                span.set_tag("user", user.id)
                span.set_tag("user_email", user.email)

            if operation == "OrganizationDeleted":
                span.set_tag("deleted_at", datetime.fromtimestamp(int(span.start_time)).strftime("%Y-%m-%d %H:%M:%S"))

            span.set_tag("http.status_code", 200)
            if extra is not None:
                for k, v in extra.items():
                    span.set_tag(k, v)
            tracer.record(span)

        except Exception as e:
            extra = {"span": span.tags} if span else {}
            logging.exception(
                f"Could not record operation '{operation}' for organization '{organization.id}', reason: {e}",
                extra=extra,
            )
