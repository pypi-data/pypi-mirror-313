import pickle
from typing import Any, Callable, List, Optional, cast

from tinybird_shared.redis_client.redis_client import TBRedisClientSync, TBRedisConfig


class RedisQueue:
    """Simple Queue with Redis Backend"""

    NAMESPACE = "queue"
    WIP_KEY_NAME = "wip_items"

    def __init__(
        self,
        name: str,
        namespace: str,
        redis_config: TBRedisConfig,
        serializer: Optional[Callable] = None,
        deserializer: Optional[Callable] = None,
    ) -> None:
        if (serializer and not deserializer) or (deserializer and not serializer):
            raise ValueError("Both serializer and deserializer are needed")

        self.db: TBRedisClientSync = TBRedisClientSync(redis_config)
        self.waiting_queue_key: str = "%s:%s" % (namespace, name)
        self.finished_items_count_key: str = "%s:items_processed" % (self.waiting_queue_key)
        self.wip_set_key: str = "%s:%s" % (self.waiting_queue_key, self.WIP_KEY_NAME)
        self._serialize: Callable[[Any], bytes] = serializer or pickle.dumps
        self._deserialize: Callable[[bytes], Any] = deserializer or cast(Callable[[bytes], Any], pickle.loads)

    def put_queue(self, item: Any) -> None:
        self.db.rpush(self.waiting_queue_key, self._serialize(item))

    def pop_queue(self) -> Any:
        item = self.db.lpop(self.waiting_queue_key)
        if item:
            decoded_item = self._deserialize(item)
            return decoded_item
        return None

    def get_queued(self) -> List[Any]:
        items = self.db.lrange(self.waiting_queue_key, 0, -1)
        return [self._deserialize(item) for item in items]

    def rem_queue(self, item: Any) -> None:
        self.db.lrem(self.waiting_queue_key, 0, self._serialize(item))

    def put_wip(self, item: Any) -> None:
        self.db.sadd(self.wip_set_key, self._serialize(item))

    def get_wip(self) -> List[Any]:
        items = self.db.smembers(self.wip_set_key)
        return [self._deserialize(item) for item in items]

    def rem_wip(self, item: Any) -> None:
        self.db.srem(self.wip_set_key, self._serialize(item))

    def task_done(self, item: Any) -> None:
        serialized_item = self._serialize(item)
        with self.db.pipeline() as pipe:
            pipe.multi()
            pipe.incr(self.finished_items_count_key)
            pipe.srem(self.wip_set_key, serialized_item)
            pipe.execute()

    def pop_queue_and_add_to_wip(self) -> Any:
        """
        We need to atomically pop an item from the queue and add it to
        the work-in-progress set to avoid race conditions.

        We are not watching the queue key (see WATCH in Redis docs https://redis.io/docs/latest/develop/interact/transactions/#watch-explained):
        - We are already using a lock to avoid concurrent access to POP items from the queue. (see JobThreadPoolExecutor.get_job())
        - We want to avoid blocking access for adding new items to the queue.
        """
        serialized_item = self.db.lindex(self.waiting_queue_key, 0)
        if not serialized_item:
            return None
        with self.db.pipeline() as pipe:
            pipe.multi()
            pipe.lrem(self.waiting_queue_key, 1, serialized_item)
            pipe.sadd(self.wip_set_key, serialized_item)
            pipe.execute()
            return self._deserialize(serialized_item)
