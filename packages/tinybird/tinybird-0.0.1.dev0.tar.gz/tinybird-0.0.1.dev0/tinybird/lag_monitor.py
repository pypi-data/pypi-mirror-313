import asyncio
import logging
import sys
import threading
import time
import traceback
from typing import Optional

from tinybird_shared.metrics.statsd_client import statsd_client


class LagMonitor:
    # LagMonitor monitors asyncio event loop lag and GIL-provoked lag
    # It combines an asyncio task and an auxiliar thread to monitor them
    # Metrics are sent to statsd, and a traceback is generated if the lag is too high
    def __init__(self):
        self._lag = None
        self._num_asyncio_tasks = 0
        self._mutex = threading.Lock()
        self._exit_flag: Optional[asyncio.Event] = None

    async def init(self, threshold: float, is_debug: bool = False):
        self._exit_flag = asyncio.Event()
        self._future = asyncio.get_event_loop().run_in_executor(None, self._monitor_on_thread, threshold, is_debug)
        try:
            self._task = asyncio.create_task(self._monitor_on_loop())
        except Exception as e:
            logging.exception(f"Error on LagMonitor: {e}")

    async def stop(self):
        if self._exit_flag is None or self._exit_flag.is_set():
            return
        self._exit_flag.set()
        await self._task
        await self._future

    def _monitor_on_thread(self, threshold, is_debug):
        gil_lag_statsd_path = f"tinybird.{statsd_client.region_app_machine}.gil_lag"
        event_loop_lag_statsd_path = f"tinybird.{statsd_client.region_app_machine}.event_loop_lag"
        num_asyncio_tasks_statsd_path = f"tinybird.{statsd_client.region_app_machine}.num_asyncio_tasks"
        c = 0
        print_counter = 0
        gil_lag: float = 0
        time_since_last_loop_lag = time.monotonic()
        check_period = 0.08
        while not self._exit_flag or not self._exit_flag.is_set():
            c += 1
            prev_timestamp = time.monotonic()
            time.sleep(check_period)
            now = time.monotonic()

            # Monitor number of asyncio tasks
            if (c % 10) == 0:
                statsd_client.gauge(num_asyncio_tasks_statsd_path, self._num_asyncio_tasks)

            # Monitor GIL-provoked lag
            gil_lag = max(gil_lag, now - prev_timestamp - check_period)
            if (c % 10) == 0:
                # Return the max GIL lag of the last 200ms
                statsd_client.timing(gil_lag_statsd_path, gil_lag)
                gil_lag = 0

            # Monitor asyncio event loop lag
            with self._mutex:
                loop_lag = self._lag
                self._lag = None
            if loop_lag is None:
                # There is moderate or high lag and the lag is causing we don't get information
                # From the asyncio task about the lag
                # Let's approximate the lag with the time since the last check-in from the task
                loop_lag = now - time_since_last_loop_lag
            else:
                time_since_last_loop_lag = now
            if (c % 10) == 0:
                # Return the max loop lag of the last 200ms
                statsd_client.timing(event_loop_lag_statsd_path, loop_lag)
            if loop_lag > threshold:
                if print_counter % (50 if is_debug else 10) == 0:
                    main_thread_ident = threading.main_thread().ident
                    stack_str = (
                        "".join(traceback.format_stack(sys._current_frames()[main_thread_ident]))
                        if main_thread_ident is not None
                        else ""
                    )
                    logging.warning(f"asyncio main loop unresponsive for {loop_lag} seconds\n {stack_str}")
                print_counter += 1
            else:
                print_counter = 0

    async def _monitor_on_loop(self):
        check_frequency = 0.02
        c = 0
        num_tasks = 0
        while not self._exit_flag or not self._exit_flag.is_set():
            c += 1
            last_check = time.monotonic()
            await asyncio.sleep(check_frequency)
            lag = time.monotonic() - last_check - check_frequency
            if (c % 10) == 0:
                num_tasks = len(asyncio.all_tasks())
            with self._mutex:
                self._num_asyncio_tasks = num_tasks
                if self._lag is None:
                    self._lag = lag
                else:
                    self._lag = max(self._lag, lag)
