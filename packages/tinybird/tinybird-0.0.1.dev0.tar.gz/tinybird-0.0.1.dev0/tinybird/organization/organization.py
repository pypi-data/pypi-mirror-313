from __future__ import annotations  # TODO(eclbg): default behaviour in 3.11

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple

from tinybird.ch import HTTPClient
from tinybird.constants import CHCluster
from tinybird.model import (
    RedisModel,
    retry_transaction_in_case_of_concurrent_edition_error_async,
    retry_transaction_in_case_of_concurrent_edition_error_sync,
)
from tinybird.tokens import AccessToken, ResourcePrefix
from tinybird.tracing import ClickhouseTracer
from tinybird.user import User as Workspace
from tinybird.user import UserAccount, UserAccounts
from tinybird.user import Users as Workspaces
from tinybird_shared.metrics.statsd_client import statsd_client


class OrganizationCommitmentsPlans:
    TOTAL_USAGE = "total_usage"
    MONTHLY_USAGE = "monthly_usage"
    # We will use this to indicate that the organization has a dedicated cluster and they pay according to the size of their cluster
    INFRASTRUCTURE_USAGE = "infrastructure_usage"
    # We will use this to indicate that the organization is inside a shared cluster and they are paying according to the number of CPUs
    SHARED_INFRASTRUCTURE_USAGE = "shared_infrastructure_usage"
    NO_USAGE_COMMITMENT = "no_usage"

    _items = {
        TOTAL_USAGE: "Total usage",
        MONTHLY_USAGE: "Monthly usage",
        INFRASTRUCTURE_USAGE: "Infra usage",
        SHARED_INFRASTRUCTURE_USAGE: "Shared infra usage",
        NO_USAGE_COMMITMENT: "No usage commitment",
    }


class MachineSize:
    CUSTOM = "custom"
    XS = "XS"
    S1 = "S1"
    S2 = "S2"
    M1 = "M1"
    M2 = "M2"
    L = "L"
    XL = "XL"
    _2XL = "2XL"
    _3XL = "3XL"
    _4XL = "4XL"
    _5XL = "5XL"

    _items = {
        CUSTOM: "Custom",
        XS: "XS",
        S1: "S1",
        S2: "S2",
        M1: "M1",
        M2: "M2",
        L: "L",
        XL: "XL",
        _2XL: "2XL",
        _3XL: "3XL",
        _4XL: "4XL",
        _5XL: "5XL",
    }

    @staticmethod
    def validate(machine_size: str) -> None:
        if machine_size not in MachineSize._items:
            raise ValueError(f"Machine size {machine_size} not supported")

    @staticmethod
    def all_sizes() -> List[str]:
        return list(MachineSize._items.keys())


@dataclass
class DedicatedCluster:
    cluster: CHCluster
    expose_metrics: Optional[bool]


@dataclass
class AsyncMetric:
    timestamp: datetime
    host: str
    cluster: str
    metric: str
    value: str
    description: str


class OrganizationException(Exception):
    pass


class DedicatedClusterNotFound(Exception):
    pass


class Organizations:
    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def update_name_and_domain(organization: Organization, name: str, domain: str) -> Organization:
        """Do not call this method directly unless it's from OrganizationService.

        Changing the domain should trigger some other operations that are handled by OrganizationService, like adding workspaces that should belong to the org based on the new domain.
        """
        with Organization.transaction(organization.id) as organization:
            organization.set_domain(domain)
            organization.set_name(name)
        return organization

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def update_commitment_information(
        organization: Organization,
        *,
        start_date: str = "",
        end_date: str = "",
        commited_processed: Optional[int] = None,
        commited_storage: Optional[int] = None,
        commited_data_transfer_intra: Optional[int] = None,
        commited_data_transfer_inter: Optional[int] = None,
        commitment_billing: str,
        commitment_machine_size: str = "",
        commitment_cpu: Optional[int] = None,
        commitment_max_qps: Optional[int] = None,
    ) -> Organization:
        with Organization.transaction(organization.id) as organization:
            organization.set_plan_details(
                start_date,
                end_date,
                commited_processed,
                commited_storage,
                commited_data_transfer_intra,
                commited_data_transfer_inter,
                commitment_billing,
                commitment_machine_size,
                commitment_cpu,
                commitment_max_qps,
            )
        return organization

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def add_admin(organization: Organization, user: UserAccount) -> Organization:
        with Organization.transaction(organization.id) as organization:
            organization.user_account_ids.add(user.id)
        return organization

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def remove_admin(organization: Organization, user: UserAccount) -> Organization:
        with Organization.transaction(organization.id) as organization:
            if len(organization.user_account_ids) == 1:
                raise OrganizationException(
                    "Organization can't be left without administrators. Add another administrator "
                    "before removing the last one"
                )
            organization.user_account_ids.remove(user.id)
        return organization

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def add_workspace(organization: Organization, workspace: Workspace) -> Organization:
        """
        >>> from uuid import uuid4
        >>> uuid = str(uuid4().hex)
        >>> org = Organization.create("add_workspace")
        >>> u = UserAccount.register(f'add_workspace@{uuid}-example.com', 'pass')
        >>> w1 = Workspace.register('add_workspace_ws', admin=u.id)
        >>> w2 = Workspace.register('add_workspace_ws2', admin=u.id)
        >>> org = Organizations.add_workspace(org, w1)
        >>> org = Organizations.add_workspace(org, w2)
        >>> assert isinstance(org.workspace_ids, set)
        >>> assert len(org.workspace_ids) == 2
        >>> assert len(org.databases) == 2
        >>> assert {w1.id, w2.id} == org.workspace_ids
        """
        Workspaces.set_organization_id(workspace, organization.id)
        with Organization.transaction(organization.id) as organization:
            if isinstance(organization.workspace_ids, list):
                organization.workspace_ids = set(organization.workspace_ids)
            organization.workspace_ids.add(workspace.id)
            organization.databases.add(workspace.database)
        return organization

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def remove_workspace(organization: Organization, workspace: Workspace) -> Organization:
        """
        >>> from uuid import uuid4
        >>> uuid = str(uuid4().hex)
        >>> org = Organization.create("add_workspace")
        >>> u = UserAccount.register(f'add_workspace@{uuid}-example.com', 'pass')
        >>> w1 = Workspace.register('remove_workspace_ws', admin=u.id)
        >>> w2 = Workspace.register('remove_workspace_ws2', admin=u.id)
        >>> org = Organizations.add_workspace(org, w1)
        >>> org = Organizations.add_workspace(org, w2)
        >>> org = Organizations.remove_workspace(org, w1)
        >>> assert len(org.workspace_ids) == 1
        >>> assert len(org.databases) == 1
        >>> assert {w2.id} == org.workspace_ids
        """
        Workspaces.set_organization_id(workspace, None)
        with Organization.transaction(organization.id) as organization:
            try:
                if isinstance(organization.workspace_ids, list):
                    organization.workspace_ids = set(organization.workspace_ids)
                organization.workspace_ids.discard(workspace.id)
                organization.databases.discard(workspace.database)
            except KeyError:
                pass
        return organization

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def remove_organization(
        organization: Organization, user: Optional[UserAccount] = None, tracer: Optional[ClickhouseTracer] = None
    ) -> None:
        # unlink all users
        for user_account_id in organization.user_account_ids:
            user_account = UserAccount.get_by_id(user_account_id)
            if not user_account:
                logging.exception(f"Unexpected error: User {user_account_id} not found")
                continue
            UserAccounts.set_organization_id(user_account, None)
        # unlink all workspaces
        for workspace_id in organization.workspace_ids:
            workspace = Workspace.get_by_id(workspace_id)
            Workspaces.set_organization_id(workspace, None)

            if tracer:
                from tinybird.workspace_service import WorkspaceService

                workspace = Workspace.get_by_id(workspace_id)
                WorkspaceService.trace_workspace_operation(tracer, workspace, "WorkspaceOrgChanged", user)

        Organization._delete(organization.id)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def refresh_token(organization: Organization, token_name_or_token: str) -> Tuple[Organization, Optional[str]]:
        with Organization.transaction(organization.id) as org:
            return org, org.refresh_token(token_name_or_token)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def add_dedicated_cluster(organization: Organization, dedicated_cluster: DedicatedCluster) -> Organization:
        """Do not call this method directly unless it's from OrganizationService.

        We must do additional checks that are handled there, like checking if there are workspaces in that cluster that
        don't belong to the org.
        """
        with Organization.transaction(organization.id) as organization:
            organization._add_dedicated_cluster(dedicated_cluster)
        return organization

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def remove_dedicated_cluster(organization: Organization, dedicated_cluster: DedicatedCluster) -> Organization:
        """Do not call this method directly unless it's from OrganizationService.

        We must do additional checks that are handled there, like ensuring that there are no workspaces in the cluster
        we're about to remove as dedicated
        """
        with Organization.transaction(organization.id) as organization:
            organization._remove_dedicated_cluster(dedicated_cluster.cluster)
        return organization

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync()
    def toggle_dedicated_cluster_expose_metrics(
        organization: Organization, dedicated_cluster: DedicatedCluster
    ) -> Organization:
        """Do not call this method directly unless it's from OrganizationService.

        We must do additional checks that are handled there, like ensuring that the cluster is reachable
        """
        with Organization.transaction(organization.id) as organization:
            organization._remove_dedicated_cluster(dedicated_cluster.cluster)
            organization._add_dedicated_cluster(dedicated_cluster)
        return organization

    @staticmethod
    async def get_by_email(email: str) -> Optional[Organization]:
        """This is horrible. It checks every organization. Try to avoid calling this"""
        # TODO: create an index on domain. Careful, an org can have multiple domains!
        mail_domain: str = email.split("@", maxsplit=1)[1]
        for org in Organization.iterate():
            if mail_domain in org.domains:
                return org
        return None

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def set_stripe_customer_id(organization: Organization, stripe_customer_id: str) -> Organization:
        with Organization.transaction(organization.id) as organization:
            organization.stripe_customer_id = stripe_customer_id
            return organization

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def set_orb_external_customer_id(organization: Organization, orb_external_customer_id: str) -> Organization:
        with Organization.transaction(organization.id) as organization:
            organization.orb_external_customer_id = orb_external_customer_id
            return organization

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def set_setup_intent_id(
        organization: Organization, stripe_setup_intent_id: str, stripe_client_secret: str
    ) -> Organization:
        with Organization.transaction(organization.id) as organization:
            organization.stripe_setup_intent_id = stripe_setup_intent_id
            organization.stripe_setup_intent_client_secret = stripe_client_secret
            return organization


class Organization(RedisModel):
    """
    >>> o = Organization.create('New Org')
    >>> o is not None
    True
    >>> updated_o = Organization.get_by_id(o.id)
    >>> o.id == updated_o.id
    True
    >>> o.token_observability.token == updated_o.token_observability.token
    True
    >>> o.workspace_ids
    set()
    """

    __namespace__ = "organizatinos"
    __props__ = [
        "name",
        "workspace_ids",
        "user_account_ids",
        "token_observability",
        "domain",
        "plan_details",
        "databases",
        "dedicated_clusters",
        "orb_external_customer_id",
        "stripe_customer_id",
        "stripe_setup_intent_id",
        "stripe_setup_intent_client_secret",
    ]

    secret: str = ""

    def __repr__(self) -> str:
        return f"Organization(id='{self.id}', name='{self.name}')"

    @classmethod
    def config(cls, redis_client: Any, secret: str) -> None:  # type: ignore
        super().config(redis_client)
        cls.secret = secret

    @staticmethod
    def create(name: str) -> Organization:
        Organization._validate_name(name)

        organization = Organization(name)
        organization.save()

        org = Organization.get_by_id(organization.id)
        assert org is not None
        return org

    def __init__(
        self,
        name: str,
        token_observability: Optional[AccessToken] = None,
        **org_dict: Any,
    ) -> None:
        self.name: str = name
        self.workspace_ids: Set[str] = set()
        self.databases: Set[str] = set()
        self.user_account_ids: Set[str] = (
            set()
        )  # This is the list of Admins. To get all users with the org's domain use `get_members`
        self.token_observability: AccessToken
        self.domain: Optional[str] = None  # Can contain multiple, comma-separated domains
        self.plan_details: Dict[str, Any] = {
            "name": "",
            "start_date": datetime.today().isoformat(),
            "end_date": "",
            "commitment": {
                "storage": 0,
                "processed": 0,
                "data_transfer_intra": 0,
                "data_transfer_inter": 0,
                "machine_size": "",
                "cpu": None,
                "max_qps": None,
            },
            "billing": OrganizationCommitmentsPlans.NO_USAGE_COMMITMENT,
        }
        self.dedicated_clusters: Set[Tuple[str, str, Optional[bool]]] = set()
        self.stripe_customer_id: Optional[str] = None
        self.orb_external_customer_id: str = ""
        self.stripe_setup_intent_id: Optional[str] = None
        self.stripe_setup_intent_client_secret: Optional[str] = None
        super().__init__(**org_dict)

        # We need the `id` to create an AccessToken
        self.token_observability = token_observability or AccessToken(
            self.id,
            "Observability (builtin)",
            Organization.secret,
            description="Observability token (automatically created by Tinybird)",
            resource_prefix=ResourcePrefix.ORGANIZATION,
        )

    @staticmethod
    def _validate_name(name: str) -> None:
        if len(name) > 100:  # TODO move to "limits" section
            raise OrganizationException("Name too long")

    @staticmethod
    def _validate_domain(domain: str) -> None:
        if len(domain) > 100:  # TODO move to "limits" section
            raise OrganizationException("domain too long")
        if "@" in domain:
            raise OrganizationException("domain can't include the `@` character")

    def _add_dedicated_cluster(self, dedicated_cluster: DedicatedCluster) -> None:
        cluster = dedicated_cluster.cluster
        self.dedicated_clusters.add((cluster.name, cluster.server_url, dedicated_cluster.expose_metrics))

    def _remove_dedicated_cluster(self, cluster: CHCluster) -> None:
        # We use only CHCluster for backwards compatibility with old Redis entries without expose_metrics
        current_entry = None
        for entry in self.dedicated_clusters:
            if entry[0] == cluster.name and entry[1] == cluster.server_url:
                current_entry = entry
                break

        if current_entry is None:
            raise DedicatedClusterNotFound()

        self.dedicated_clusters.remove(current_entry)

    def set_domain(self, domain: str) -> None:
        self._validate_domain(domain)
        self.domain = domain  # TODO validate is domain hasn't been already assigned.
        # TODO: add existing Workspaces with this domain to the Org

    @property
    def domains(self) -> List[str]:
        if self.domain is None:
            return []
        return self.domain.replace(" ", "").split(",")

    def set_name(self, name: str) -> None:
        self._validate_name(name)
        self.name = name

    @property
    def commitment_start_date(self) -> str:
        return self.plan_details.get("start_date", datetime.today().isoformat())

    @property
    def commitment_end_date(self) -> str:
        return self.plan_details.get("end_date", "")

    @property
    def commitment_processed(self) -> Optional[int]:
        return self.plan_details.get("commitment", {}).get("processed")

    @property
    def commitment_storage(self) -> Optional[int]:
        return self.plan_details.get("commitment", {}).get("storage")

    @property
    def commitment_data_transfer_intra(self) -> Optional[int]:
        return self.plan_details.get("commitment", {}).get("data_transfer_intra")

    @property
    def commitment_data_transfer_inter(self) -> Optional[int]:
        return self.plan_details.get("commitment", {}).get("data_transfer_inter")

    @property
    def commitment_machine_size(self) -> str:
        return self.plan_details.get("commitment", {}).get("machine_size", "")

    @property
    def commitment_cpu(self) -> Optional[int]:
        return self.plan_details.get("commitment", {}).get("cpu")

    @property
    def commitment_billing(self) -> str:
        return self.plan_details.get("billing", "")

    @property
    def max_qps(self) -> Optional[int]:
        """Get the maximum QPS limit for the organization"""
        return self.plan_details.get("commitment", {}).get("max_qps")

    def set_plan_details(
        self,
        start_date: Optional[str],
        end_date: Optional[str],
        commited_processed: Optional[int],
        commited_storage: Optional[int],
        commited_data_transfer_intra: Optional[int],
        commited_data_transfer_inter: Optional[int],
        commitment_billing: Optional[str],
        commitment_machine_size: Optional[str],
        commitment_cpu: Optional[int],
        commitment_max_qps: Optional[int] = None,
    ) -> None:
        self.plan_details = {
            "start_date": start_date,
            "end_date": end_date,
            "commitment": {
                "processed": commited_processed,
                "storage": commited_storage,
                "data_transfer_intra": commited_data_transfer_intra,
                "data_transfer_inter": commited_data_transfer_inter,
                "machine_size": commitment_machine_size,
                "cpu": commitment_cpu,
                "max_qps": commitment_max_qps,
            },
            "billing": commitment_billing,
        }

    async def get_all_workspaces(self) -> List[Workspace]:
        all_workspaces: List[Optional[Workspace]] = [await Workspace.get_by_id_async(id) for id in self.workspace_ids]
        return [w for w in all_workspaces if w is not None]

    async def get_admins(self) -> List[UserAccount]:
        """Get all Organization admins (those directly assigned in Cheriff)"""
        all_users: List[Optional[UserAccount]] = [await UserAccount.get_by_id_async(id) for id in self.user_account_ids]
        return [user for user in all_users if user is not None]

    async def get_members(self) -> Set[UserAccount]:
        """Gets all Organization members
        If the organization has a domain, those that share the organization's email domain
        Otherwise, all users that are members of the workspaces in the organization
        """
        if self.domains:
            return set(
                u for u in await UserAccount.get_all_async() if self.contains_email(u.email) and u.confirmed_account
            )
        else:
            workspaces = await self.get_all_workspaces()
            members = await self.get_admins()
            for w in workspaces:
                members.extend(await w.get_simple_members())
            return set(members)

    def user_is_admin(self, user: UserAccount) -> bool:
        return user.id in self.user_account_ids

    async def user_is_member(self, user: UserAccount) -> bool:
        return user.id in [u.id for u in await self.get_members()]

    def contains_email(self, email: str) -> bool:
        """Check if email matches any of the organization's domains"""
        parts = email.lower().split("@", maxsplit=1)
        if len(parts) < 2:
            return False

        return parts[1] in self.domains

    def get_token_access_info(self, token_name_or_token: str) -> Optional[AccessToken]:
        """Mimics User::get_token_access_info() and UserAccount::get_token_access_info()"""
        if (
            self.token_observability.name == token_name_or_token
            or self.token_observability.token == token_name_or_token
        ):
            return self.token_observability
        return None

    def refresh_token(self, token_name_or_token: str) -> Optional[str]:
        tk = self.get_token_access_info(token_name_or_token)
        if not tk:
            return None

        self.token_observability.refresh(Organization.secret, self.id, resource_prefix="o")
        return self.token_observability.token

    def get_orb_external_customer_id(self):
        return self.orb_external_customer_id if self.orb_external_customer_id else self.id

    @property
    def in_dedicated_infra_pricing(self) -> bool:
        return self.plan_details.get("billing") == OrganizationCommitmentsPlans.INFRASTRUCTURE_USAGE

    @property
    def instance_type(self) -> str:
        return self.plan_details.get("commitment", {}).get("machine_size", "")

    @property
    def in_shared_infra_pricing(self) -> bool:
        return self.plan_details.get("billing") == OrganizationCommitmentsPlans.SHARED_INFRASTRUCTURE_USAGE

    def get_dedicated_clusters(self) -> List[DedicatedCluster]:
        """Get org's dedicated clusters. Defined in Cheriff."""
        dedicated_clusters: List[DedicatedCluster] = []

        for cluster in self.dedicated_clusters:
            # If the Redis model doesn't have the new field then default to the org's billing plan as before
            expose_metrics: bool = (
                cluster[2] if len(cluster) > 2 and cluster[2] is not None else self.in_dedicated_infra_pricing
            )
            ch_cluster = CHCluster(name=cluster[0], server_url=cluster[1])
            dedicated_clusters.append(DedicatedCluster(cluster=ch_cluster, expose_metrics=expose_metrics))

        return dedicated_clusters

    def get_dedicated_clusters_name(self) -> List[str]:
        return [dc.cluster.name for dc in self.get_dedicated_clusters()]

    def get_dedicated_clusters_url(self) -> List[str]:
        return [dc.cluster.server_url for dc in self.get_dedicated_clusters()]

    def get_dedicated_clusters_exposing_metrics(self) -> List[CHCluster]:
        return [dc.cluster for dc in self.get_dedicated_clusters() if dc.expose_metrics]

    async def get_cluster_metrics(self) -> List[AsyncMetric]:
        org_clusters = [(c.name, c.server_url) for c in self.get_dedicated_clusters_exposing_metrics()]

        if not org_clusters:
            return []

        metrics = []
        # This description is a combination of OSSystemTime and OSUserTime, as we're exposing both added up.
        # https://clickhouse.com/docs/en/operations/system-tables/asynchronous_metrics
        cpu_usage_description = (
            "The ratio of time the CPU core was running OS kernel (system) code or userspace code. This is a "
            "system-wide metric, it includes all the processes on the host machine, not just clickhouse-server. "
            "This includes also the time when the CPU was under-utilized due to the reasons internal to the CPU "
            "(memory loads, pipeline stalls, branch mispredictions, running another SMT core)."
        )
        for cluster, database_server in org_clusters:
            try:
                client = HTTPClient(database_server)
                query = f"""
                    SELECT
                        now() as timestamp,
                        metrics_enriched.safe_host as host,
                        metrics_enriched.metric,
                        metrics_enriched.value,
                        metrics_enriched.description
                    FROM (
                        SELECT
                            concat('{cluster}', '_', shard_num) as safe_host,
                            metric,
                            value,
                            description
                        FROM (
                            SELECT
                                hostName() as host,
                                metric,
                                toString(value) as value,
                                description
                            FROM clusterAllReplicas('{cluster}',system.asynchronous_metrics)
                            WHERE metric IN ('LoadAverage1', 'LoadAverage15', 'OSMemoryTotal')
                            UNION ALL
                            SELECT
                                hostName() as host,
                                metric,
                                toString(value) as value,
                                description
                            FROM clusterAllReplicas('{cluster}',system.metrics)
                            WHERE metric IN ('Query', 'MemoryTracking')
                            UNION ALL
                            SELECT
                                host,
                                'CPUUsage' as metric,
                                toString(sum(value)) as value,
                                '{cpu_usage_description}' as description
                            FROM (
                                SELECT
                                    hostName() as host,
                                    metric,
                                    value
                                FROM clusterAllReplicas('{cluster}',system.asynchronous_metrics)
                                WHERE metric IN ('OSSystemTimeNormalized', 'OSUserTimeNormalized')
                            )
                            GROUP BY host
                            UNION ALL
                            SELECT
                                host,
                                'NumberCPU' as metric,
                                toString(number_cpus) as value,
                                'Number of CPUs' as description
                            FROM (
                                SELECT
                                    hostName() as host,
                                    count() as number_cpus
                                FROM clusterAllReplicas('{cluster}', system.asynchronous_metrics)
                                -- Clickhouse reports the metric OSUserTimeN for each core of a host
                                WHERE metric like 'OSUserTimeCPU%'
                                GROUP BY host
                            )
                        ) metrics
                        JOIN (
                            SELECT
                                hostName() as host,
                                shardNum() as shard_num
                            from clusterAllReplicas('{cluster}', system.one)
                        ) shard_nums
                        ON metrics.host = shard_nums.host
                    ) metrics_enriched
                    FORMAT JSON
                """
                _, body = await client.query(
                    query,
                    read_only=True,
                    max_execution_time=30,
                    skip_unavailable_shards=True,
                )
                metrics.extend([AsyncMetric(**x | {"cluster": cluster}) for x in json.loads(body)["data"]])
                statsd_client.incr(f"tinybird.{statsd_client.region}.{cluster}.cluster_metrics_collection.success")
            except Exception as e:
                logging.warning(
                    f"Exception getting asynchronous metrics from {database_server} cluster: {cluster} error: {e}"
                )
                statsd_client.incr(f"tinybird.{statsd_client.region}.{cluster}.cluster_metrics_collection.failure")
        return metrics


def migration_add_databases(u: dict) -> dict:
    """Adds the databases for the current workspaces to the organization object."""
    databases = set()
    workspace_ids = u["workspace_ids"]

    for workspace_id in workspace_ids:
        workspace = Workspace.get_by_id(workspace_id)
        if workspace:
            databases.add(workspace.database)

    u["databases"] = databases
    return u


def migration_remove_orphan_workspaces(u: dict) -> dict:
    """Removes any non existant workspace id in the org."""
    workspace_ids = u["workspace_ids"]

    existing_workspaces = set(workspace_ids)
    for workspace_id in workspace_ids:
        workspace = Workspace.get_by_id(workspace_id)
        if not workspace:
            existing_workspaces.discard(workspace_id)

    u["workspace_ids"] = existing_workspaces
    return u


def migration_remove_branches_and_releases_old(u: dict) -> dict:
    """Bad migration, kept for reference"""
    return u


def migration_remove_branches_and_releases(u: dict) -> dict:
    """Removes branches from the org."""
    workspace_ids = u["workspace_ids"]
    databases = u["databases"]

    non_branches = set(workspace_ids)
    for workspace_id in workspace_ids:
        workspace = Workspace.get_by_id(workspace_id)
        if workspace and workspace.origin:
            non_branches.discard(workspace_id)
            databases.discard(workspace.database)

    u["workspace_ids"] = non_branches
    u["databases"] = databases
    return u


Organization.__migrations__ = {
    1: migration_add_databases,
    2: migration_remove_orphan_workspaces,
    3: migration_remove_branches_and_releases_old,
    4: migration_remove_branches_and_releases,
}
