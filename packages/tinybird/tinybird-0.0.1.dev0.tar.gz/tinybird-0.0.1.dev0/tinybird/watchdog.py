import asyncio
import logging
from typing import Optional

from systemd_watchdog import watchdog

MAX_PING_INTERVAL = 5


class TBWatchdog:
    """
    This class is responsible for sending heartbeats to the systemd watchdog.
    If the watchdog does not receive a heartbeat within the timeout period, the system will be rebooted.
    We have implemented this because we have experienced writers getting stucked and because writers share the same port, Nginx would keep sending requests if 1 writer keeps working fine.
    This would lead to requests not being handle by the writer and nginx returning a 504 error to the client, but still keep sending requests because the other writer is alive.
    For more information: https://gitlab.com/tinybird/analytics/-/issues/8631
    """

    def __init__(self) -> None:
        self._wd = watchdog()
        self._exit_flag: Optional[asyncio.Event] = None

        self._wd.ready()
        self._wd.notify()
        logging.info("Watchdog ready")

    def single_heartbeat(self) -> None:
        self._wd.ping()

    async def run(self):
        self._exit_flag = asyncio.Event()
        try:
            asyncio.create_task(self._constant_heartbeat())  # noqa: RUF006
        except Exception as e:
            logging.exception(f"Error on Watchdog: {e}")

    async def _constant_heartbeat(self) -> None:
        half_timeout_in_seconds = int(float(self._wd.timeout) / 2e6)
        heartbeat_time = min(half_timeout_in_seconds, MAX_PING_INTERVAL)

        while not self._exit_flag or not self._exit_flag.is_set():
            self._wd.ping()
            await asyncio.sleep(heartbeat_time)

    def terminate(self):
        if self._exit_flag is not None and not self._exit_flag.is_set():
            self._exit_flag.set()

        self._wd._send("STOPPING=1")
        logging.info("Watchdog stopped")
