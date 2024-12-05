import logging
import os
import socket
import traceback
from typing import Any, Dict, Optional

import sentry_sdk
import statsd


class StatsdClient:
    # StatsdClient allows to have a module-level global statsd client
    # with lazy initialization
    def __init__(self):
        # Use a dummy UDP client to a random-ish port
        # Using a real client implies CI and local testing check types
        self._statsd_client = statsd.StatsClient(host="localhost", port=4242)
        self._region = f"{os.getenv('TB_REGION', 'unknown')}"
        if os.getenv("KUBERNETES_PORT"):
            self._region_machine = f"{self._region}.pod"
        else:
            self._region_machine = f"{self._region}.{socket.gethostname()}"
        self._region_app_machine = f"{self._region_machine}.{os.getenv('TB_APP_NAME', 'unknown')}"

    def init(self, settings: Dict[str, Any]):
        statsd_conf: Optional[Dict[str, str]] = settings.get("statsd_server", None)
        if statsd_conf:
            if statsd_conf.get("type", "udp") == "udp":
                self._statsd_client = statsd.StatsClient(host=statsd_conf["host"])
            else:
                self._statsd_client = statsd.TCPStatsClient(host=statsd_conf["host"])

        # For analytics, use the configuration from the settings rather than the env vars
        if settings.get("tb_region", None):
            self._region = f"{settings.get('tb_region', 'unknown')}"
            if os.getenv("KUBERNETES_PORT"):
                self._region_machine = f"{self._region}.pod"
            else:
                self._region_machine = f"{self._region}.{socket.gethostname()}"
        if settings.get("app_name", None):
            app_name = settings.get("app_name", "unknown")
            self._region_app_machine = f"{self._region_machine}.{app_name}"
            os.environ["TB_APP_NAME"] = app_name

    @property
    def region(self):
        return self._region

    @property
    def region_machine(self):
        return self._region_machine

    @property
    def region_app_machine(self):
        return self._region_app_machine

    def __getattr__(self, attr):
        method = getattr(self._statsd_client, attr)

        def fn(*args, **kwargs):
            try:
                return method(*args, **kwargs)
            except Exception as e:
                trace = traceback.format_stack(limit=4)
                sentry_sdk.set_context("Tinybird", {"stacktrace": trace})
                logging.error(f"{e} {''.join(trace)}")

        return fn


statsd_client: statsd.StatsClient = StatsdClient()
