import time
from typing import Optional

from cachetools import TTLCache

TTL_CACHE = 10
TTL_ERROR_PERIOD = 0.05


def get_circuit_breaker_id(workspace_id: str, table_id: str) -> str:
    return f"{workspace_id}.{table_id}"


class CircuitBreakersException(Exception):
    pass


class CircuitBreakersRateLimit:
    def __init__(self):
        self._state: TTLCache = TTLCache(maxsize=1_000_000, ttl=TTL_CACHE)

    def is_rate_limited(self, id: str, timestamp: Optional[float] = None) -> bool:
        if timestamp is None:
            timestamp = time.monotonic()
        last_error = self._state.get(id, None)
        return last_error is not None and (timestamp - last_error < TTL_ERROR_PERIOD)

    def set_rate_limited(self, id: str, timestamp: Optional[float] = None) -> None:
        if timestamp is None:
            timestamp = time.monotonic()
        self._state[id] = timestamp


global_hfi_circuit_breakers_rate_limit = CircuitBreakersRateLimit()
