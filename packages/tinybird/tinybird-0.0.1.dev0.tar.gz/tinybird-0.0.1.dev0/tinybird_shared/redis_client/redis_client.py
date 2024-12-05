#! /usr/bin/env python
import logging
from dataclasses import dataclass, field
from typing import Any, Iterable, Tuple

from async_timeout import asyncio
from redis import Redis
from redis import asyncio as aioredis
from redis.asyncio import sentinel as aiosentinel
from redis.exceptions import ConnectionError, ReadOnlyError, ResponseError
from redis.sentinel import MasterNotFoundError, Sentinel

from tinybird_shared.retry.retry import retry_async, retry_sync

"""
Default Redis configuration
"""
DEFAULT_REDIS_BD: int = 0
DEFAULT_LIMITS_MAX_CONNECTIONS: int = 30
DEFAULT_SENTINEL_ADDRESSES: Iterable[Tuple[str, int]] = [
    ("sentinel1", 26379),
    ("sentinel2", 26380),
    ("sentinel3", 26381),
]
DEFAULT_SENTINEL_ADDRESSES_SET_NAME: str = "tb_redis_sentinel"
DEFAULT_REDIS_CONFIG: dict = {
    "instances_set_name": DEFAULT_SENTINEL_ADDRESSES_SET_NAME,
    "sentinels": [
        {"host": address[0], "port": address[1]} for address in DEFAULT_SENTINEL_ADDRESSES
    ],  # this is the way it is received from pro.py
    "db": DEFAULT_REDIS_BD,
}


"""
Retryable errors:

- "ConnectionError": Happens when the connection to the Redis fails. For example if the Redis instance suddenly stops.
Sentinel will take some seconds to select the new Master and after that the connection will reconnect to the new
master and continue working.

- "MasterNotFoundError": During a Failover, Sentinel needs have some time between the confirmation that the old master
was down until a new one is selected. If we require a master during that time, this error will be raised.

- "ReadOnlyError": Happens if a write operation is sent to a replica. That may happen because we were connected to a
Master that recently has been changed to a replica and the connection has not been renewed to point to the new master.
If the connection was retried with the Sentinel's `master_for` command, that connection will automatically change to the
new master.

- "ResponseError: NOREPLICAS Not enough good replicas to write": Master is still receiving writes but no replicas are
available to synchronize those writes. May happen because the master got disconnected from the rest of the cluster.
In that situation one of the replicas instances may be selected as new master, so the writes accepted by the old
master during the disconnection time may be lost.
"""
FAILOVER_ERRORS = (ConnectionError, MasterNotFoundError, ReadOnlyError, ResponseError)


@dataclass
class TBRedisConfig:
    sentinels: Iterable[Tuple[str, int]] = field(default_factory=lambda: DEFAULT_SENTINEL_ADDRESSES)
    instances_set_name: str = DEFAULT_SENTINEL_ADDRESSES_SET_NAME
    db: int = DEFAULT_REDIS_BD
    limits_max_connections: int = 0


class TBRedisClientSync:
    def __init__(self, tb_redis_config: TBRedisConfig) -> None:
        self._redis_client: Redis

        if isinstance(tb_redis_config, TBRedisConfig):
            self.__service_name = tb_redis_config.instances_set_name
            self._redis_client = Sentinel(tb_redis_config.sentinels).master_for(
                self.__service_name, db=tb_redis_config.db
            )
            logging.info(f"Redis client connected to Sentinel service {self.__service_name}")

        else:
            raise Exception("TBRedisClientSync needs configuration to be initialized.")

    def __getattr__(self, name: str) -> Any:
        if self._redis_client:

            @retry_sync(FAILOVER_ERRORS, tries=4, delay=0.2, backoff=2.5)
            def execute_command(*args, **kwargs):
                return getattr(self._redis_client, name)(*args, **kwargs)

            return execute_command
        else:
            raise Exception("TBRedisClientSync was not correctly initialized.")


class TBRedisReplicaClientSync:
    def __init__(self, tb_redis_config: TBRedisConfig) -> None:
        self._redis_client: Redis

        if isinstance(tb_redis_config, TBRedisConfig):
            self.__service_name = tb_redis_config.instances_set_name
            self._redis_client = Sentinel(tb_redis_config.sentinels).slave_for(
                self.__service_name, db=tb_redis_config.db
            )
            logging.info(f"Redis client connected to Sentinel replica service {self.__service_name}")

        else:
            raise Exception("TBRedisClientSync needs configuration to be initialized.")

    def __getattr__(self, name: str) -> Any:
        if self._redis_client:

            @retry_sync(FAILOVER_ERRORS, tries=4, delay=0.2, backoff=2.5)
            def execute_command(*args, **kwargs):
                return getattr(self._redis_client, name)(*args, **kwargs)

            return execute_command
        else:
            raise Exception("TBRedisClientSync was not correctly initialized.")


class TBRedisClientAsync:
    # TBRedisClientAsync allows to have a module-level global Redis client
    # with lazy initialization
    def __init__(self):
        self._async_redis = {}
        self.redis_config = None

    def init(self, tb_redis_config: TBRedisConfig) -> None:
        self.redis_config = tb_redis_config

    def get_redis_client(self) -> aioredis.Redis:
        """
        >>> import pytest
        >>> import asyncio
        >>> from tinybird_shared.redis_client.redis_client import TBRedisClientAsync, TBRedisConfig
        >>> redis_wrapper = TBRedisClientAsync()
        >>> tb_redis_config = TBRedisConfig(sentinels=[('sentinel1', 26379)], instances_set_name='tb_redis_sentinel')
        >>> redis_wrapper.init(tb_redis_config)
        >>> redis_wrapper.get_redis_client()
        Redis<SentinelConnectionPool<service=tb_redis_sentinel(master)>>
        >>> redis_wrapper_custom_db = TBRedisClientAsync()
        >>> tb_redis_config_custom_db = TBRedisConfig(sentinels=[('sentinel1', 26379)], instances_set_name='tb_redis_sentinel', db=7)
        >>> redis_wrapper_custom_db.init(tb_redis_config)
        >>> client_custom_db = redis_wrapper_custom_db.get_redis_client()
        >>> loop = asyncio.get_event_loop()
        >>> loop.run_until_complete(client_custom_db.set('test', 'test'))
        True
        >>> loop.run_until_complete(client_custom_db.get('test'))
        b'test'
        >>> client_info = loop.run_until_complete(client_custom_db.info())
        >>> client_info['db7']['keys']
        1
        >>> loop.run_until_complete(client_custom_db.flushdb())
        True
        >>> uninit_redis_wrapper = TBRedisClientAsync()
        >>> with pytest.raises(Exception):
        ...     uninit_redis_wrapper.get_redis_client()
        """
        if isinstance(self.redis_config, TBRedisConfig):
            return aiosentinel.Sentinel(self.redis_config.sentinels).master_for(
                self.redis_config.instances_set_name, db=self.redis_config.db
            )
        else:
            raise Exception("TBRedisClientAsync needs configuration to be initialized.")

    def __getattr__(self, attr):
        if not self.redis_config:
            return None
        try:
            loop = asyncio.get_running_loop()
        except Exception:
            return None
        if attr == "reset":

            async def reset():
                if loop in self._async_redis:
                    await self._async_redis[loop].close()
                    del self._async_redis[loop]

            return reset
        if loop not in self._async_redis:
            # Lazy initialization of aioredis to ensure there is an asyncio event loop
            self._async_redis[loop] = self.get_redis_client()

        @retry_async(FAILOVER_ERRORS, tries=4, delay=0.2, backoff=2.5)
        def execute_command(*args, **kwargs):
            return getattr(self._async_redis[loop], attr)(*args, **kwargs)

        return execute_command


class TBRedisClientLimitsAsync:
    # Same as TBRedisClientAsync to be used for the concurrency limiter
    # TODO: Use only TBRedisClientAsync
    def __init__(self):
        self._async_redis = {}
        self.redis_config = None

    def init(self, tb_redis_config: TBRedisConfig) -> None:
        self.redis_config = tb_redis_config

    def get_redis_client(self) -> aioredis.Redis:
        """
        >>> import pytest
        >>> import asyncio
        >>> from tinybird_shared.redis_client.redis_client import TBRedisClientLimitsAsync, TBRedisConfig
        >>> redis_wrapper = TBRedisClientLimitsAsync()
        >>> tb_redis_config = TBRedisConfig(sentinels=[('sentinel1', 26379)], instances_set_name='tb_redis_sentinel', 'limits_max_connections': 20)
        >>> redis_wrapper.init(tb_redis_config)
        >>> redis_wrapper.get_redis_client()
        Redis<SentinelConnectionPool<service=tb_redis_sentinel(master)>>
        >>> redis_wrapper.get_redis_client().connection_pool.max_connections
        20
        >>> redis_wrapper_custom_db = TBRedisClientLimitsAsync()
        >>> tb_redis_config_custom_db = TBRedisConfig(sentinels=[('sentinel1', 26379)], instances_set_name='tb_redis_sentinel', db=7)
        >>> redis_wrapper_custom_db.init(tb_redis_config)
        >>> client_custom_db = redis_wrapper_custom_db.get_redis_client()
        >>> loop = asyncio.get_event_loop()
        >>> loop.run_until_complete(client_custom_db.set('test', 'test'))
        True
        >>> loop.run_until_complete(client_custom_db.get('test'))
        b'test'
        >>> redis_wrapper.get_redis_client().connection_pool.max_connections
        30
        >>> client_info = loop.run_until_complete(client_custom_db.info())
        >>> client_info['db7']['keys']
        1
        >>> loop.run_until_complete(client_custom_db.flushdb())
        True
        >>> uninit_redis_wrapper = TBRedisClientLimitsAsync()
        >>> with pytest.raises(Exception):
        ...     uninit_redis_wrapper.get_redis_client()
        """
        if isinstance(self.redis_config, TBRedisConfig):
            return aiosentinel.Sentinel(self.redis_config.sentinels).master_for(
                self.redis_config.instances_set_name,
                db=self.redis_config.db,
                max_connections=self.redis_config.limits_max_connections or DEFAULT_LIMITS_MAX_CONNECTIONS,
            )
        else:
            raise Exception("TBRedisClientLimitsAsync needs configuration to be initialized.")

    def __getattr__(self, attr):
        if not self.redis_config:
            return None
        try:
            loop = asyncio.get_running_loop()
        except Exception:
            return None
        if attr == "reset":

            async def reset():
                if loop in self._async_redis:
                    await self._async_redis[loop].close()
                    del self._async_redis[loop]

            return reset
        if loop not in self._async_redis:
            # Lazy initialization of aioredis to ensure there is an asyncio event loop
            self._async_redis[loop] = self.get_redis_client()

        @retry_async(FAILOVER_ERRORS, tries=4, delay=0.2, backoff=2.5)
        def execute_command(*args, **kwargs):
            return getattr(self._async_redis[loop], attr)(*args, **kwargs)

        return execute_command


async_redis: TBRedisClientAsync = TBRedisClientAsync()
async_redis_limits: TBRedisClientLimitsAsync = TBRedisClientLimitsAsync()
