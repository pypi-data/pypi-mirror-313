_predefined_replicas_for_copy: dict[str, list[str]] = {}


def get_predefined_replicas_configuration_for_copy(cluster: str) -> list[str]:
    global _predefined_replicas_for_copy
    return _predefined_replicas_for_copy.get(cluster, [])


def set_predefined_replicas_configuration_for_copy(predefined_replicas: dict[str, list[str]] | None = None):
    global _predefined_replicas_for_copy
    if not predefined_replicas:
        predefined_replicas = {}
    _predefined_replicas_for_copy = predefined_replicas
