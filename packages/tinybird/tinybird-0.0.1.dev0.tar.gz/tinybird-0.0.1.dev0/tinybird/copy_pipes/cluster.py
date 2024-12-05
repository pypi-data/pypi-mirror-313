from tinybird.copy_pipes.services import get_predefined_replicas_configuration_for_copy
from tinybird.user import User as Workspace


def get_clickhouse_replicas_for_copy(workspace: Workspace) -> list[str]:
    # Getting Predefined Replicas
    # 1. If defined in Cheriff, predefined replicas in there would be used
    predefined_replicas = workspace.get_limits(prefix="copy").get("copy_predefined_replicas", None)
    predefined_replicas_cheriff = predefined_replicas.split(",") if predefined_replicas else []
    if predefined_replicas_cheriff and len(predefined_replicas_cheriff):
        return predefined_replicas_cheriff

    # 2. If not defined in Cheriff, there is a default value for predefined replicas per cluster within region config
    predefined_replica_config = get_predefined_replicas_configuration_for_copy(workspace.cluster or "")
    if predefined_replica_config and len(predefined_replica_config):
        return predefined_replica_config

    # 3. If there is no configuration in the region, return the default database_server to get a random one from Varnish
    return [workspace.database_server]
