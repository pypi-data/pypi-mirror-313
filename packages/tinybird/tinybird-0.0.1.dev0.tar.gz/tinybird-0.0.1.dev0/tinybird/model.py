import asyncio
import logging
import math
import pickle
import random
import time
import uuid
from collections import defaultdict
from contextlib import contextmanager
from datetime import datetime
from itertools import islice
from threading import RLock
from typing import Any, Callable, Coroutine, Dict, Iterator, List, Optional, Set, Tuple, Type, TypeVar, Union

import redis
from cachetools import LRUCache
from typing_extensions import ParamSpec

from tinybird_shared.redis_client.redis_client import FAILOVER_ERRORS, TBRedisClientSync, TBRedisReplicaClientSync
from tinybird_shared.retry.retry import retry_async, retry_sync

# We use a default batch count of 200 to avoid loading all models in memory and to reduce the number of Redis calls
# Also take into account that when we do a scan_iter we will get a batch of keys, so we will load the models in batches
# But we will be also fetching some keys like `:last_updated` and `:owner` keys that we are not interested in
DEFAULT_REDIS_BATCH_COUNT = 200


# TODO: Remove this function and use `itertools.batched` directly when we migrate to python 3.12
def batched(iterable: Iterator, n: int) -> Iterator[Tuple]:
    # batched('ABCDEFG', 3) → ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    iterator = iter(iterable)
    while batch := tuple(islice(iterator, n)):
        yield batch


class ConcurrentEditionException(RuntimeError):
    pass


class ModelLRUCache(LRUCache):
    # The timeout is used as a safety measure. If it's triggered it would be a logical error because either
    # an insert is super slow or, more likely, there is a bug in the caller and there we would rather throw
    # an exception instead of blocking forever
    MAX_LOCK_TIMEOUT = 3

    def __init__(self, maxsize):
        # This needs to be a re-entry lock since LRUCache call other functions to clean up on insertion
        self.Lock = RLock()
        self.hits = 0
        self.misses = 0
        super().__init__(maxsize, getsizeof=None)

    def __getitem__(self, key):
        if not self.Lock.acquire(blocking=True, timeout=ModelLRUCache.MAX_LOCK_TIMEOUT):
            raise Exception("ModelLRUCache.__getitem__ too long")
        try:
            # If the key is not found, super().__getitem__ will call __missing__ which will return None
            i = super().__getitem__(key)
            if i is not None:
                self.hits += 1
            else:
                self.misses += 1
        finally:
            self.Lock.release()
        return i

    def __setitem__(self, key, value):
        if not self.Lock.acquire(blocking=True, timeout=ModelLRUCache.MAX_LOCK_TIMEOUT):
            raise Exception("ModelLRUCache.__setitem__ too long")
        try:
            # We need to avoid counting the internal __getitem__ call that LRUCache does
            # Save current hits/misses
            current_hits = self.hits
            current_misses = self.misses
            super().__setitem__(key, value)
            # Restore hits/misses to what they were before the internal __getitem__
            self.hits = current_hits
            self.misses = current_misses
        finally:
            self.Lock.release()

    def __delitem__(self, key):
        if not self.Lock.acquire(blocking=True, timeout=ModelLRUCache.MAX_LOCK_TIMEOUT):
            raise Exception("ModelLRUCache.__delitem__ too long")
        try:
            super().__delitem__(key)
        finally:
            self.Lock.release()

    def popitem(self):
        if not self.Lock.acquire(blocking=True, timeout=ModelLRUCache.MAX_LOCK_TIMEOUT):
            raise Exception("ModelLRUCache.popitem too long")
        try:
            super().popitem()
        finally:
            self.Lock.release()

    def __missing__(self, key):
        """
        This is used to avoid calling the super class __missing__ method, which raises a KeyError
        If the key is not found, we return None, which is the expected behavior for a cache miss
        """
        return None


Retry_params = ParamSpec("Retry_params")
Retry_return = TypeVar("Retry_return")


def retry_transaction_in_case_of_concurrent_edition_error_sync(
    tries: int = 10, delay: float = 0.1, backoff: float = 1.1
) -> Callable[[Callable[Retry_params, Retry_return]], Callable[Retry_params, Retry_return]]:
    return retry_sync((ConcurrentEditionException, *FAILOVER_ERRORS), tries, delay, backoff)


def retry_transaction_in_case_of_concurrent_edition_error_async(
    tries: int = 10, delay: float = 0.1, backoff: float = 1.1
) -> Callable[
    [Callable[Retry_params, Coroutine[Any, Any, Retry_return]]],
    Callable[Retry_params, Coroutine[Any, Any, Retry_return]],
]:
    return retry_async((ConcurrentEditionException, *FAILOVER_ERRORS), tries, delay, backoff)


# To prevent stuck jobs, we need to leave enough time for a redis fail-over to happen (20 seconds should be enough)
def retry_job_transaction_in_case_of_error_sync(
    tries: int = 7, delay: float = 0.2, backoff: float = 2.5
) -> Callable[[Callable[Retry_params, Retry_return]], Callable[Retry_params, Retry_return]]:
    return retry_transaction_in_case_of_concurrent_edition_error_sync(tries, delay, backoff)


T = TypeVar("T", bound="RedisModel")


class RedisModel:
    """
    >>> from tinybird_shared.redis_client.redis_client import TBRedisClientSync, TBRedisConfig
    >>> client = TBRedisClientSync(TBRedisConfig())
    >>> class TestModel(RedisModel):
    ...     __namespace__ = 'tests'
    ...     __props__ = ['v']
    ...     __indexes__ = ['v']
    ...     __sets__ = ['v']
    ...     __fast_scan__ = True

    ...     def __init__(self, **model_dict):
    ...         self.v = None
    ...         super().__init__(**model_dict)

    >>> TestModel.config(client)
    >>> TestModel.__namespace__
    'tests'
    >>> TestModel.get_by_id(None)
    >>> TestModel.get_by_index('v', None)
    >>> t = TestModel(id='object_id', v='foo')
    >>> t.save()
    >>> len(TestModel._fast_scan())
    1
    >>> TestModel._fast_scan()[0].id == t.id
    True
    >>> t2 = TestModel.get_by_id(t.id)
    >>> t.id
    'object_id'
    >>> t.id == t2.id
    True
    >>> t2.v
    'foo'
    >>> TestModel.get_by_index('v', 'foo').id
    'object_id'
    >>> def add_name(d):
    ...     d['name'] = f"{d['v']}-bar"
    ...     return d
    >>> [x[0] for x in TestModel.get_items_for('v', 'foo')]
    ['object_id']
    >>> tn = TestModel(id='object_id2', v='foo')
    >>> tn.save()
    >>> [x[0] for x in TestModel.get_items_for('v', 'foo')]
    ['object_id', 'object_id2']
    >>> TestModel.get_items_count_for('v', 'foo')
    2
    >>> TestModel._delete(tn.id)
    3
    >>> [x[0] for x in TestModel.get_items_for('v', 'foo')]
    ['object_id']
    >>> TestModel.__props__.append('name')
    >>> RedisModel.__object_cache_by_id__['TestModel']['object_id'] is None
    False
    >>> list(RedisModel.__object_cache_by_id__['TestModel']['object_id'].keys())
    ['last_updated', 'python_object']
    >>> RedisModel.__object_cache_by_id__['TestModel']['missing_object_id'] is None
    True
    >>> TestModel.remove_from_cache('object_id')
    True
    >>> TestModel.remove_from_cache('missing_object_id')
    False
    >>> RedisModel.__object_cache_by_id__['TestModel'].clear()
    >>> TestModel.__migrations__ = {
    ...     1: add_name
    ... }
    >>> migrated = TestModel.get_by_id('object_id')
    >>> migrated.name
    'foo-bar'
    >>> with TestModel.transaction('object_id') as t:
    ...     t.v = 'bar'
    >>> t = TestModel.get_by_id('object_id')
    >>> t.v
    'bar'
    >>> other_instance = TestModel.get_by_id('object_id')
    >>> with TestModel.transaction('object_id') as t:
    ...     t.v = 'did_not_update'
    ...     other_instance.v = 'other_won'
    ...     other_instance.save()
    Traceback (most recent call last):
    ...
    tinybird.model.ConcurrentEditionException: Concurrent edition of model <TestModel>=object_id
    >>> t = TestModel.get_by_id('object_id')
    >>> t.v
    'other_won'
    >>> with TestModel.transaction('object_id') as t:
    ...     t.v = 'miss'
    ...     raise ValueError('error inside tx')
    Traceback (most recent call last):
    ...
    ValueError: error inside tx
    >>> t = TestModel.get_by_id('object_id')
    >>> t.v
    'other_won'
    """

    __namespace__: Optional[str] = None
    __props__: List[str] = []
    __owner__: Optional[str] = None
    __owner_max_children__: Union[float, int] = math.inf
    __old_owner__: Optional[str] = None
    __owners__: Set[str] = set()
    __indexes__: List[str] = []
    __ttl__: Optional[int] = None
    __migrations__: Dict[int, Callable[[Dict[Any, Any]], Dict[Any, Any]]] = {}
    __sets__: Set[str] = set()
    __fast_scan__: bool = False

    OWNER_SET_REMOVE_EVERY_X_ADD: int = 20

    # Set of caches per child class
    # This is done because the object is shared for all base classes, so the simple way to avoid sharing the cache
    # is to create a dictionary (ChildClass.__name__ -> Cache)
    __object_cache_by_id__: Dict[str, ModelLRUCache] = defaultdict(lambda: ModelLRUCache(128))

    redis_client: TBRedisClientSync
    redis_replica_client: TBRedisReplicaClientSync
    redis_last_error = 0

    @classmethod
    def config(cls, redis_client: TBRedisClientSync) -> None:
        cls.redis_client = redis_client

    @classmethod
    def config_replica(cls, redis_replica_client: TBRedisReplicaClientSync) -> None:
        cls.redis_replica_client = redis_replica_client

    def __init__(self, **model):
        self.id = model.get("id", str(uuid.uuid4()))
        self.db_version: int = model.get("db_version", 0)
        self.created_at: datetime = model.get("created_at", datetime.now())
        self.updated_at = model.get("updated_at", self.created_at)
        for prop in self.__props__:
            setattr(self, prop, model.get(prop, getattr(self, prop, None)))

    @classmethod
    # TODO: Change this Any for OptionalT] in a next MR improve typing strictness
    def get_by_id(cls: Type[T], _id: str, in_transaction: bool = False) -> Optional[T]:
        # We add an extra validation to make sure that _id is not None to avoid unnecessary calls to redis
        if _id is None:
            return None
        # get last updated first
        if not in_transaction:
            obj_cache = cls.__object_cache_by_id__[cls.__name__].get(_id, None)
            if obj_cache is not None:
                k = f"{cls.__namespace__}:{_id}:last_updated"
                last_updated = cls.redis_client.get(k)
                last_updated = float(last_updated) if last_updated is not None else time.time()
                if last_updated <= obj_cache["last_updated"]:
                    # reload it from redis
                    return obj_cache["python_object"]

        m, last_updated = cls._get_last_version_of_object_from_redis(_id)
        if not m:
            return None
        m = cls._run_migrations(m, in_transaction=in_transaction)
        if not m:
            return None

        # get last update and save into the cache
        if last_updated:
            last_updated = float(last_updated)
            cls.__object_cache_by_id__[cls.__name__][_id] = {"last_updated": last_updated, "python_object": m}
        return m

    @classmethod
    async def get_by_id_async(cls: Type[T], _id: str, in_transaction: bool = False) -> Optional[T]:
        return cls.get_by_id(_id, in_transaction)

    @classmethod
    def get_by_id_from_redis(cls: Type[T], redis_client: TBRedisClientSync, id: str) -> Optional[T]:
        b = redis_client.get(f"{cls.__namespace__}:{id}")

        if not b:
            return None

        pre_deserialize = getattr(cls, "__pre_deserialize__", lambda x: x)
        m = cls._from_storage(pickle.loads(pre_deserialize(b)))
        if not m:
            return None
        return m

    @classmethod
    def _get_last_version_of_object_from_redis(cls, _id: str) -> Tuple[Optional[T], Optional[float]]:
        if _id is None:
            return None, None

        b, last_updated = cls.redis_client.mget(
            [f"{cls.__namespace__}:{_id}", f"{cls.__namespace__}:{_id}:last_updated"]
        )
        if not b:
            return None, None
        pre_deserialize = getattr(cls, "__pre_deserialize__", lambda x: x)
        m = cls._from_storage(pickle.loads(pre_deserialize(b)))
        return m, last_updated

    @classmethod
    def remove_from_cache(cls, _id: str) -> bool:
        try:
            del cls.__object_cache_by_id__[cls.__name__][_id]
            return True
        except KeyError:
            return False

    @classmethod
    def get_by_index(cls, index, key):
        if key is None:
            return None
        _id = cls.redis_client.get(f"{cls.__namespace__}:{index}:{key}")
        if not _id:
            return None
        return cls.get_by_id(_id.decode())

    @classmethod
    def get_index_values(cls, index: str, count=1000) -> Dict[str, str]:
        index_keys = list(cls.redis_client.scan_iter(f"{cls.__namespace__}:{index}:*", count=count))
        index_values = cls.redis_client.mget(index_keys)
        result = {
            key.decode().split(":")[-1]: value.decode() for (key, value) in zip(index_keys, index_values, strict=True)
        }
        return result

    @classmethod
    def get_by_index_from_redis(cls: Type[T], redis_client: TBRedisClientSync, index: str, key: str) -> Optional[T]:
        _id = redis_client.get(f"{cls.__namespace__}:{index}:{key}")
        if not _id:
            return None
        return cls.get_by_id_from_redis(redis_client, _id.decode())

    @classmethod
    def _get_by_keys(cls: Type[T], keys: List[str], batch_count: int = DEFAULT_REDIS_BATCH_COUNT) -> List[T]:
        """
        Retrieves a list of model instances from Redis based on the given keys.

        Args:
        - keys (List[str]): The list of keys to retrieve the models.
        - batch_count (int, optional): The number of keys to retrieve in each batch. Defaults to `DEFAULT_REDIS_BATCH_COUNT`.
        """
        if not keys:
            return []

        results: List[T] = []

        def load_batch(batch_keys: List[str]):
            """Loads a batch of items from Redis and appends them to the local `results` list"""
            if not batch_keys:
                return

            models = cls.redis_client.mget(batch_keys)
            pre_deserialize = getattr(cls, "__pre_deserialize__", lambda x: x)
            for b in models:
                if b is None:
                    continue
                try:
                    m = cls._from_storage(pickle.loads(pre_deserialize(b)))
                    m = cls._run_migrations(m)
                    if m:
                        results.append(m)
                except Exception:
                    model_id: Optional[str] = None
                    try:
                        m = pickle.loads(pre_deserialize(b))
                        model_id = m.get("id", None)
                    except Exception:
                        pass
                    logging.exception(f"Failed to load model {model_id}")

        for i in range(math.ceil(len(keys) // batch_count) + 1):
            batch_start: int = i * batch_count
            load_batch(keys[batch_start : batch_start + batch_count])

        return results

    @classmethod
    def get_all(cls: Type[T], *args: Any, **kwargs: Any) -> List[T]:
        """
        Get all models from redis.
        You can pass a keyword argument `count` to limit the number of models returned.
        """
        count: Optional[int] = kwargs.get("count")
        batch_count: int = kwargs.get("batch_count", DEFAULT_REDIS_BATCH_COUNT)
        if count:
            batch_count = min(count, batch_count)

        if cls.__fast_scan__ and cls._is_fast_scan_enabled():
            return cls._fast_scan(count=count, batch_count=batch_count)

        keys: List[str] = []
        for k in cls.redis_client.scan_iter(f"{cls.__namespace__}:*", count=batch_count):
            # We filter out keys like `:last_updated` and `:owner` keys
            if k.count(b":") != 1:
                continue
            keys.append(k.decode())
            if count and len(keys) >= count:
                break

        result: List[T] = cls._get_by_keys(keys, batch_count=batch_count)

        if cls.__fast_scan__:
            # _get_by_keys should have migrated all instances and set up the fast_scan set
            cls._enable_fast_scan()

        return result

    @classmethod
    async def get_all_async(cls: Type[T], *args: Any, **kwargs: Any) -> List[T]:
        return cls.get_all(*args, **kwargs)

    @classmethod
    async def get_all_paginated(cls: Type[T], *args: Any, **kwargs: Any) -> List[T]:
        """
        ONLY USE THIS FOR CHERIFF. Get all models from redis paginated.
        - Pass a keyword argument `skip_count` to skip the first n-th elements.
        - Pass a keyword argument `count` to set the number of models returned per page.
        - Pass a keyword argument `batch_count` to limit the number of keys fetched from Redis in the same take.
        """
        skip_count: int = kwargs.get("skip_count", 0)
        page_size: int = kwargs.get("page_size", 50)
        batch_count: int = min(page_size, kwargs.get("batch_count", DEFAULT_REDIS_BATCH_COUNT))

        def get_all_keys() -> List[str]:
            # Prefetch all needed keys, order them and skipe the first skip_count items
            all_keys = list(cls.redis_client.scan_iter(f"{cls.__namespace__}:*"))

            # We filter out keys like `:last_updated` and `:owner` keys
            return [k.decode() for k in all_keys if k.count(b":") == 1]

        all_keys = await asyncio.to_thread(get_all_keys)
        # Sort by key. Not the best, but is deterministic across calls and maintain pagination predictable
        page_keys = sorted(all_keys)[skip_count : skip_count + page_size]

        return await asyncio.to_thread(cls._get_by_keys, page_keys, batch_count=batch_count)

    @classmethod
    def iterate(cls: Type[T], batch_count=DEFAULT_REDIS_BATCH_COUNT) -> Iterator[T]:
        """
        Return an iterator to iterate over all models in Redis.
        This is useful when you have a large number of models and you don't want to load all of them in memory.
        """

        if cls.__fast_scan__:
            raise NotImplementedError("Iterating over all models is not supported when fast scan is enabled")

        # The method `scan_iter` will return an iterator of batches of keys
        # Then we batch the keys and load the models in each batch to avoid loading all models in memory and to reduce the number of Redis calls
        for keys in batched(cls.redis_client.scan_iter(f"{cls.__namespace__}:*", count=batch_count), batch_count):
            # Remove keys that are from `:last_updated` keys or `:owner` keys
            # Therefore it's recommended to set a bigger batch_count as we will skip some keys
            cleaned_keys = [key.decode() for key in keys if key.count(b":") == 1]
            models = cls.redis_client.mget(cleaned_keys)
            pre_deserialize = getattr(cls, "__pre_deserialize__", lambda x: x)
            for b in models:
                if b is None:
                    continue
                try:
                    m = cls._from_storage(pickle.loads(pre_deserialize(b)))
                    m = cls._run_migrations(m)
                    if m:
                        yield m
                except Exception:
                    model_id: Optional[str] = None
                    try:
                        m = pickle.loads(pre_deserialize(b))
                        model_id = m.get("id", None)
                    except Exception:
                        pass
                    logging.exception(f"Failed to load model {model_id}")

    @classmethod
    def _is_fast_scan_enabled(cls):
        return bool(cls.redis_client.get(f"migration:fast_scan:{cls.__namespace__}"))

    @classmethod
    def _enable_fast_scan(cls):
        cls.redis_client.set(f"migration:fast_scan:{cls.__namespace__}", "1")

    @classmethod
    def _fast_scan(cls: Type[T], count: Optional[int] = None, batch_count: int = DEFAULT_REDIS_BATCH_COUNT) -> List[T]:
        """_Fast_ version of get_all"""

        if not cls.__fast_scan__:
            raise Exception(f"{cls.__namespace__} is not configured to support fast scans")

        ids: List[str]
        keys_iter = cls.redis_client.sscan_iter(f"{cls.__namespace__}:instances")

        if not count:
            ids = [f"{cls.__namespace__}:{key.decode()}" for key in keys_iter]
        else:
            ids = []
            for key in keys_iter:
                ids.append(f"{cls.__namespace__}:{key.decode()}")
                if len(ids) >= count:
                    break

        return cls._get_by_keys(ids, batch_count=batch_count)

    @classmethod
    def get_all_by_owner(
        cls: Type[T], owner: str, limit: int = 100, batch_count: int = DEFAULT_REDIS_BATCH_COUNT
    ) -> List[T]:
        how_many_to_retrieve: int = limit
        if cls.__owner_max_children__ < math.inf:
            how_many_to_retrieve = int(cls.__owner_max_children__)
        ids = cls.redis_client.zrange(f"{cls.__namespace__}:owner:{owner}", 0, how_many_to_retrieve - 1)
        if len(ids) >= cls.__owner_max_children__:
            ids = ids[:limit]
            cls.redis_client.zremrangebyrank(f"{cls.__namespace__}:owner:{owner}", cls.__owner_max_children__, -1)
        keys = [f"{cls.__namespace__}:{k.decode()}" for k in ids]
        return cls._get_by_keys(keys, batch_count=batch_count)

    @classmethod
    def is_owned_by(cls, object_id, owner):
        zscore = cls.redis_client.zscore(f"{cls.__namespace__}:owner:{owner}", object_id)
        return bool(zscore)

    @classmethod
    def _delete(cls: Type[T], _id: str) -> int:
        m: Optional[T] = cls.get_by_id(_id)
        if not m:
            cls.remove_from_cache(_id)
            return 0  # Redis will return the number of keys deleted, so we return 0 if the object doesn't exists

        model_keys = [f"{cls.__namespace__}:{_id}", f"{cls.__namespace__}:{_id}:last_updated"]
        for index in cls.__indexes__:
            index_value = cls._get_index_value(m, index)
            if index_value:
                model_keys.append(f"{cls.__namespace__}:{index}:{index_value}")
        for s in cls.__sets__:
            cls.redis_client.zrem(f"{cls.__namespace__}:items:{s}:{getattr(m, s)}", _id)
        if cls.__fast_scan__:
            cls.redis_client.srem(f"{cls.__namespace__}:instances", _id)
        if cls.__owner__:
            cls.redis_client.zrem(f"{cls.__namespace__}:owner:{getattr(m, cls.__owner__)}", _id)
        if cls.__owners__:
            for owner in cls.__owners__:
                cls.redis_client.zrem(f"{cls.__namespace__}:owner:{getattr(m, owner)}", _id)
        cls.remove_from_cache(_id)
        return cls.redis_client.delete(*model_keys)

    def _clean_index(self, index: str) -> None:
        if index not in self.__indexes__:
            raise ValueError(f"This model doesn't have '{index}' as index.")

        index_value = self._get_index_value(self, index)
        if index_value:
            key_to_remove = f"{self.__namespace__}:{index}:{index_value}"
            self.redis_client.delete(key_to_remove)

    def save(self) -> None:
        updated_at = self.__save(self.redis_client)
        RedisModel.__object_cache_by_id__[self.__class__.__name__][self.id] = {
            "last_updated": updated_at,
            "python_object": self,
        }

    @classmethod
    def save_to_redis(cls: Type[T], model: T, redis_client: TBRedisClientSync) -> None:
        model.__save(redis_client)

    @classmethod
    @contextmanager
    def transaction(cls: Type[T], _id: str) -> Iterator[T]:
        model_id = f"{cls.__namespace__}:{_id}"
        with cls.redis_client.pipeline() as p:
            p.watch(model_id)
            p.multi()

            # TODO: Change this Any for OptionalT] and change this method from `T` to `Optional[T]`
            m: Optional[T] = cls.get_by_id(_id, in_transaction=True)
            try:
                yield m  # type: ignore
                if not m:
                    cls.remove_from_cache(_id)
                    logging.warning(f"Model <{cls.__name__}>={_id} not found in transaction")
                else:
                    updated_at = m.__save(p)
                    p.execute()
                    RedisModel.__object_cache_by_id__[cls.__class__.__name__][_id] = {
                        "last_updated": updated_at,
                        "python_object": m,
                    }
            except redis.exceptions.WatchError as e:
                cls.remove_from_cache(_id)
                raise ConcurrentEditionException(f"Concurrent edition of model <{cls.__name__}>={_id}") from e
            except Exception as e:
                cls.remove_from_cache(_id)
                logging.debug(f"Failed to commit transaction at model <{cls.__name__}>={_id}. Reason: {e}")
                raise e

    @classmethod
    def _from_storage(cls, model_dict):
        return cls(**model_dict)

    def _to_storage(self):
        d = {}
        for prop in ["id", "db_version", "created_at", "updated_at"]:
            d[prop] = getattr(self, prop)
        for prop in self.__props__:
            d[prop] = getattr(self, prop)
        return d

    @staticmethod
    def _get_index_value(the_class: Any, index: str) -> Optional[str]:
        """
        Override in case you need to transform or skip an index value for some kind of instance.
        """
        return getattr(the_class, index)

    def __save(self, client: TBRedisClientSync) -> float:
        self.updated_at = datetime.now()
        k = f"{self.__namespace__}:{self.id}"
        post_serialize = getattr(self.__class__, "__post_serialize__", lambda x: x)
        v = post_serialize(pickle.dumps(self._to_storage()))
        updated_at = time.time()
        d = {k: v, f"{k}:last_updated": updated_at}
        for index in self.__indexes__:
            index_value = self._get_index_value(self, index)
            if index_value:
                d[f"{self.__namespace__}:{index}:{index_value}"] = self.id
        logging.debug(f"Commit model <{self.__class__.__name__}>={self.id}")
        client.mset(d)
        if self.__ttl__ and isinstance(self.__ttl__, int):
            for _k in d.keys():
                client.expire(_k, self.__ttl__)

        if self.__old_owner__:
            client.zrem(f"{self.__namespace__}:owner:{self.__old_owner__}", self.id)

        if self.__owner__:
            owner_key = f"{self.__namespace__}:owner:{getattr(self, self.__owner__)}"
            client.zadd(owner_key, {self.id: -updated_at})
            if (
                self.__owner_max_children__ < math.inf
                and random.randint(1, self.OWNER_SET_REMOVE_EVERY_X_ADD) % self.OWNER_SET_REMOVE_EVERY_X_ADD == 0
            ):
                client.zremrangebyrank(owner_key, int(self.__owner_max_children__), -1)

        for owner in self.__owners__:
            client.zadd(f"{self.__namespace__}:owner:{getattr(self, owner)}", {self.id: -updated_at})

        for s in self.__sets__:
            client.zadd(f"{self.__namespace__}:items:{s}:{getattr(self, s)}", {self.id: updated_at})
        if self.__fast_scan__:
            self.redis_client.sadd(f"{self.__namespace__}:instances", self.id)
        return updated_at

    @classmethod
    def get_items_for(cls, _set, attr, limit=-1):
        items = cls.redis_client.zrange(f"{cls.__namespace__}:items:{_set}:{attr}", 0, limit, withscores=True)
        return list(map(lambda x: (x[0].decode(), datetime.fromtimestamp(x[1])), items))

    @classmethod
    def get_items_count_for(cls, _set, attr):
        return cls.redis_client.zcount(f"{cls.__namespace__}:items:{_set}:{attr}", "-inf", "+inf")

    @classmethod
    def _run_migrations(cls: Type[T], model: T, in_transaction: bool = False) -> Optional[T]:
        migrations = cls.__migrations__
        migrations_to_run = cls.__filter_migrations_to_run(model, migrations)

        if len(migrations_to_run) == 0:
            return model

        if in_transaction:
            return cls.__run_pending_migrations(model, migrations, migrations_to_run)
        else:
            return cls.__run_migrations_in_transaction(model, migrations)

    @staticmethod
    def __filter_migrations_to_run(
        model: Optional[T], migrations: Dict[int, Callable[[Dict[Any, Any]], Dict[Any, Any]]]
    ) -> List[int]:
        db_version = getattr(model, "db_version", 0)
        return sorted([x for x in migrations.keys() if x > db_version])

    @classmethod
    @retry_transaction_in_case_of_concurrent_edition_error_sync(tries=3, delay=0.01, backoff=1)
    def __run_migrations_in_transaction(
        cls: Type[T], model: T, migrations: Dict[int, Callable[[Dict[Any, Any]], Dict[Any, Any]]]
    ) -> Optional[T]:
        most_recent_model_version, last_updated_at = cls._get_last_version_of_object_from_redis(model.id)
        migrations_to_run = cls.__filter_migrations_to_run(most_recent_model_version, migrations)
        if len(migrations_to_run) > 0:
            with cls.transaction(model.id) as model:
                if model is None:
                    return None
                migrations_to_run = cls.__filter_migrations_to_run(model, migrations)
                return cls.__run_pending_migrations(model, migrations, migrations_to_run)
        else:
            return most_recent_model_version

    @classmethod
    def __run_pending_migrations(
        cls: Type[T],
        model: T,
        migrations: Dict[int, Callable[[Dict[Any, Any]], Dict[Any, Any]]],
        migrations_to_run: List[int],
    ) -> T:
        for m in migrations_to_run:
            logging.info("running migration %s on %s" % (m, model))
            model = cls(**migrations[m](model._to_storage()))
            model.db_version = m
        return model

    @classmethod
    async def publish_with_retry(cls, channel: Any, message: Any) -> int:
        @retry_async(PublishedMessageNotReceived, tries=6, delay=0.5)
        async def publish():
            receivers = cls.redis_client.publish(channel, message)
            if receivers == 0:
                raise PublishedMessageNotReceived()
            return receivers

        try:
            received_by = await publish()
        except PublishedMessageNotReceived:
            received_by = 0
        return received_by


class PublishedMessageNotReceived(Exception):
    pass
