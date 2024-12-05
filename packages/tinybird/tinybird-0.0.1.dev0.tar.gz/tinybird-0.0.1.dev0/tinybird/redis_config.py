from typing import Any, Dict, Optional

from tinybird_shared.redis_client.redis_client import (
    DEFAULT_LIMITS_MAX_CONNECTIONS,
    DEFAULT_REDIS_BD,
    TBRedisClientSync,
    TBRedisConfig,
)


def get_redis_config(conf: Dict[Any, Any]) -> TBRedisConfig:
    """
    >>> conf = {'redis': {'sentinels': [{'host': 'sentinel5', 'port': 12345},
    ...                                          {'host': 'sentinel6', 'port': 23456}],
    ...                             'instances_set_name': 'redis_set_name',
    ...                             'db': 1,
    ...                             'limits_max_connections': 20}}
    >>> redis_config = get_redis_config(conf)
    >>> assert isinstance(redis_config, TBRedisConfig)
    >>> ('sentinel5', 12345) in redis_config.sentinels
    True
    >>> ('sentinel6', 23456) in redis_config.sentinels
    True
    >>> redis_config.limits_max_connections
    20
    >>> redis_config.instances_set_name
    'redis_set_name'
    >>> redis_config.db
    1
    >>> conf = {'redis': {'sentinels': [{'host': 'sentinel5', 'port': 12345},
    ...                                          {'host': 'sentinel6', 'port': 23456}],
    ...                             'instances_set_name': 'redis_set_name',
    ...                             'db': 0},
    ...           'redis_sentinel': {'sentinels': [{'host': 'wrong_address', 'port': 12345}],
    ...           'instances_set_name': 'wrong_thing',
    ...           'db': 5}}
    >>> redis_config = get_redis_config(conf)
    >>> assert isinstance(redis_config, TBRedisConfig)
    >>> ('sentinel5', 12345) in redis_config.sentinels
    True
    >>> ('sentinel6', 23456) in redis_config.sentinels
    True
    >>> redis_config.limits_max_connections
    30
    >>> redis_config.instances_set_name
    'redis_set_name'
    >>> redis_config.db
    0
    >>> conf = {'other_config': 'redis2'}
    >>> get_redis_config(conf)
    Traceback (most recent call last):
    ...
    Exception: Redis configuration not found.

    """
    redis_key = "redis"
    if redis_key not in conf:
        raise Exception("Redis configuration not found.")
    if "sentinels" not in conf[redis_key] or "instances_set_name" not in conf[redis_key]:
        raise Exception("Sentinel configuration missing.")

    sentinel_addresses = set(
        (sentinel_address["host"], sentinel_address["port"]) for sentinel_address in conf[redis_key]["sentinels"]
    )
    redis_config = TBRedisConfig(
        sentinels=sentinel_addresses,
        instances_set_name=conf[redis_key]["instances_set_name"],
        db=conf[redis_key].get("db", DEFAULT_REDIS_BD),
        limits_max_connections=conf[redis_key].get("limits_max_connections", DEFAULT_LIMITS_MAX_CONNECTIONS),
    )

    return redis_config


def get_redis_client_from_regions_config(settings: Dict[str, Any], region_name: Optional[str]) -> TBRedisClientSync:
    available_regions = settings.get("available_regions", {})
    config = available_regions.get(region_name, settings)
    redis_config = get_redis_config(config)
    return TBRedisClientSync(redis_config)
