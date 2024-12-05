import asyncio
import logging
import math
import random
import time
import traceback
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, List, Tuple

from tinybird.fnv import fnv_1a
from tinybird_shared.redis_client.redis_client import async_redis, async_redis_limits


class LockTimeoutError(Exception):
    pass


@asynccontextmanager
async def distributed_lock(mutex_path: str, ttl: int = 30, acquire_timeout: int = 3) -> AsyncGenerator[str, None]:
    lock_time = time.time()
    while True:
        acquired = await async_redis.set(mutex_path, "lock_acquired", ex=ttl, nx=True)
        if acquired:
            break
        if time.time() - lock_time > acquire_timeout:
            raise LockTimeoutError(f"Timeout while acquiring mutex at path {mutex_path}")
        await asyncio.sleep(0.3)
    try:
        yield "lock_acquired"
    finally:
        now = time.time()
        spent_time = now - lock_time
        remaining_time = ttl - spent_time
        threshold = 1
        if remaining_time < threshold:
            logging.error(
                f"distributed_lock(): lock expired before completion, spent_time: {spent_time}.\nTraceback: {traceback.format_exc()}"
            )
        elif spent_time > acquire_timeout:
            logging.warning(
                f"distributed_lock(): lock was held for more than acquire_timeout, spent_time: {spent_time}.\nTraceback: {traceback.format_exc()}"
            )
            await async_redis.delete(mutex_path)
        else:
            await async_redis.delete(mutex_path)


class WorkingGroup:
    def __init__(
        self, group_id: str, worker_id: str, ttl: int = 30, delete_ttl: int = 360, keepalive_interval: int = 5
    ) -> None:
        self.group_id: str = group_id
        self.worker_id: str = worker_id
        self.ttl: int = ttl
        self.delete_ttl: int = delete_ttl
        self.keepalive_interval: int = keepalive_interval
        self._workers: List[str] = []
        self._becomes_stable = time.time() + 15

    async def init(self) -> "WorkingGroup":
        self._should_exit = asyncio.Event()
        await self._update()
        self._task = asyncio.create_task(self._loop())
        return self

    async def _loop(self) -> None:
        while not self._should_exit.is_set():
            try:
                try:
                    await asyncio.wait_for(self._should_exit.wait(), timeout=self.keepalive_interval)
                except asyncio.TimeoutError:
                    await self._update()
            except Exception as e:
                logging.error(f"Unexpected exception {e}\nTraceback: {traceback.format_exc()}")

    async def _update(self) -> None:
        previous_workers = self._workers

        time_since_epoch = int(time.time())
        redis_group_id = f"working_group:{self.group_id}"
        await async_redis.zadd(redis_group_id, {self.worker_id: time_since_epoch})
        workers = await async_redis.zrangebyscore(redis_group_id, time_since_epoch - self.ttl, math.inf)
        self._workers = [x.decode("utf-8", "replace") for x in workers]
        await async_redis.zremrangebyscore(redis_group_id, -math.inf, time_since_epoch - self.delete_ttl)

        if sorted(previous_workers) != sorted(self._workers):
            self._becomes_stable = time.time() + 15

    async def exit(self) -> None:
        self._should_exit.set()
        await self._task

    def is_stable(self) -> bool:
        return self._becomes_stable < time.time()

    def score_index(self, key: str) -> int:
        """
        `score_index` scores the priority of all workers in the working_group
        towards `key`, and returns the index of this worker in the group

        0 => this is the worker with the highest priority for key
        1 => this is the second worker by priority for key
        2 => this is the third worker by priority for key
        num_workers => this is the worker with the least priority for key
        """
        # Rendezvous hashing (aka HRW hashing)
        # See https://en.wikipedia.org/wiki/Rendezvous_hashing

        # Avoid using built-in hash() function to ensure the same hashing on different
        # Python processes and Python versions
        assert isinstance(self._workers, list)
        workers_ordered_by_score = sorted(self._workers, key=lambda worker_id: fnv_1a([worker_id, key]))
        return workers_ordered_by_score.index(self.worker_id)


# https://gist.github.com/ptarjan/e38f45f2dfe601419ca3af937fff574d#concurrent-requests-limiter
CONCURRENT_REQUESTS_LIMITER_LUA = """local key = KEYS[1]
local capacity = tonumber(ARGV[1])
local timestamp = tonumber(ARGV[2])
local id = ARGV[3]
local ttl = tonumber(ARGV[4])
local random_number = tonumber(ARGV[5])

if random_number % 100 < 10 then
    redis.call("zremrangebyscore", key, "-inf", timestamp - ttl)
end

if redis.call("zcard", key) < capacity then
    redis.call("zadd", key, timestamp, id)
    return { 1, capacity - 1 }
else
    return { 0, capacity }
end"""


async def before_start_concurrent_process(
    key: str, timestamp: int, ttl: int, max_concurrency: int, process_id: str
) -> Tuple[int, int]:
    keys = [key]
    redis_args = [max_concurrency, timestamp, process_id, ttl, random.randint(1, 100)]
    allowed, count = await async_redis_limits.eval(CONCURRENT_REQUESTS_LIMITER_LUA, len(keys), *keys, *redis_args)
    return allowed, count


async def after_finish_concurrent_process(key: str, process_id: str, redis_client: Any):
    redis_client.zrem(key, process_id)
