from typing import Any, List

from tinybird.cluster_settings import ClusterSettings, ClusterSettingsOperations
from tinybird.user import User as Workspace

DYNAMIC_DISK_SETTINGS_PREFIX = "dynamic_disk_"


def get_clickhouse_replicas_for_populates(workspace: Workspace) -> List[str]:
    # Getting Predefined Replica with precedence workspace > cluster > none preferred
    # 1. Check if defined in Cheriff by Workspace
    ws_replicas = workspace.get_limits(prefix=ClusterSettingsOperations.POPULATE).get(
        "populate_predefined_replicas", None
    )
    cluster_replicas = ws_replicas.split(",") if ws_replicas else []
    if cluster_replicas and len(cluster_replicas):
        return cluster_replicas

    # 2. Check if defined in Cheriff by Cluster
    cluster_settings = ClusterSettings.get_by_cluster(workspace.cluster or "")
    if cluster_settings:
        populate = cluster_settings.settings.get(ClusterSettingsOperations.POPULATE, {})
        cluster_replicas = list(populate.get("replicas", {}).keys())

        # Note: We're discarding the weights for now
        return cluster_replicas

    # 3. If there is no configuration in the region, return [] to use the default config
    return []


def get_clickhouse_settings_for_populates(workspace: Workspace) -> dict[str, Any]:
    cluster_settings = ClusterSettings.get_by_cluster(workspace.cluster or "")
    if cluster_settings:
        # TODO validate settings
        populate = cluster_settings.settings.get(ClusterSettingsOperations.POPULATE, {})
        settings = populate.get("settings", {})
        return {k: v for k, v in settings.items() if not k.startswith(DYNAMIC_DISK_SETTINGS_PREFIX)}
    return {}


def get_dynamic_disk_settings_for_populates(workspace: Workspace) -> dict[str, Any]:
    cluster_settings = ClusterSettings.get_by_cluster(workspace.cluster or "")
    if cluster_settings:
        populate = cluster_settings.settings.get(ClusterSettingsOperations.POPULATE, {})
        settings = populate.get("settings", {})
        return {
            k.replace(DYNAMIC_DISK_SETTINGS_PREFIX, ""): v
            for k, v in settings.items()
            if k.startswith(DYNAMIC_DISK_SETTINGS_PREFIX)
        }
    return {}


def get_pool_replicas() -> List[str]:
    cluster_settings = get_pool_cluster()
    if cluster_settings:
        jobs = cluster_settings.settings.get(ClusterSettingsOperations.POOL, {})
        cluster_replicas = list(jobs.get("replicas", {}).keys())
        return cluster_replicas
    raise ValueError("No Pool replicas found")


def get_pool_cluster() -> ClusterSettings:
    cluster_settings: List[ClusterSettings] = ClusterSettings.get_by_operation(ClusterSettingsOperations.POOL)
    if len(cluster_settings) > 1:
        raise ValueError("More than one cluster found for pool")
    if not cluster_settings or not isinstance(cluster_settings[0], ClusterSettings):
        raise ValueError("No cluster found for pool")
    return cluster_settings[0]


def get_pool_cluster_name() -> str:
    cluster_settings = get_pool_cluster()
    return cluster_settings.cluster_name  # type: ignore
