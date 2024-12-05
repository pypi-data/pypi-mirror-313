import time

from cachetools import TTLCache

from tinybird_shared.metrics.statsd_client import statsd_client

MAX_CONSECUTIVE_ERRORS = 3
INITIAL_WAIT = 0.125
EXPONENTIAL_RAMP = 2
MAX_WAIT = 60


def get_circuit_breaker_id(workspace_id: str, table_id: str) -> str:
    return f"{workspace_id}.{table_id}"


class CircuitBreakersException(Exception):
    pass


class CircuitBreakers:
    def __init__(self):
        self._state: TTLCache = TTLCache(maxsize=1_000_000, ttl=(MAX_WAIT + 60))

    def check(self, id: str, now=None):
        if now is None:
            now = time.monotonic()
        state = self._state.get(id, None)
        if state is None:
            return
        time_since_last_try = now - state["last_try"]

        if state["failed_times"] <= MAX_CONSECUTIVE_ERRORS:
            statsd_client.incr(f"tinybird-hfi.circuit_breakers.opened_with_errors.{statsd_client.region_machine}.{id}")
            state["last_try"] = now
            return

        if time_since_last_try > state["wait"]:
            statsd_client.incr(f"tinybird-hfi.circuit_breakers.half_opened.{statsd_client.region_machine}.{id}")
            state["last_try"] = now
            state["wait"] = min(state["wait"] * EXPONENTIAL_RAMP, MAX_WAIT)
            return
        statsd_client.incr(f"tinybird-hfi.circuit_breakers.closed.{statsd_client.region_machine}.{id}")
        raise CircuitBreakersException(state["error"])

    def succeeded(self, id: str):
        statsd_client.incr(f"tinybird-hfi.circuit_breakers.succeeded.{statsd_client.region_machine}.{id}")
        if id in self._state:
            del self._state[id]

    def failed(self, id: str, err: str):
        statsd_client.incr(f"tinybird-hfi.circuit_breakers.failed.{statsd_client.region_machine}.{id}")
        previous_state = self._state.get(id, {"failed_times": 0, "last_try": 0, "wait": INITIAL_WAIT})
        self._state[id] = {
            "failed_times": previous_state["failed_times"] + 1,
            "last_try": previous_state["last_try"],
            "error": err,
            "wait": previous_state["wait"],
        }


global_hfi_circuit_breakers = CircuitBreakers()
