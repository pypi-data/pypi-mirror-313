import logging
import time
from collections import defaultdict
from typing import Optional, Self


class Profiler:
    def __init__(self):
        self._timers = defaultdict(list)

    def time(self, name):
        timer = Timer(name)
        self._timers[name].append(timer)
        return timer

    @property
    def results(self):
        return {name: sum(map(lambda timer: timer.elapsed, timers)) for name, timers in self._timers.items()}

    def reset(self):
        for name, timers in self._timers.items():
            self._timers[name] = list(
                map(lambda timer: timer.restart(), filter(lambda timer: not timer.finished, timers))
            )


class Timer:
    def __init__(self, msg: Optional[str] = None) -> None:
        self.msg = msg
        self.start: float = 0
        self.end: float = 0
        # tracing is disabled because there is a memory leak
        """
        tracer = get_tracer()
        span = tracer.start_span(operation_name='timing')
        self.scope = tracer.scope_manager.activate(span, True)
        self.scope.span.set_tag("component", "timer")
        self.scope.span.set_tag("kind", "server")
        self.scope.span.set_tag("measure", msg)
        """

    def __enter__(self) -> Self:
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.interval = self.end - self.start
        if self.msg:
            logging.debug("[timing] %s time %f" % (self.msg, self.interval))
        """
        self.scope.span.log_kv({"time": self.interval})
        self.scope.span.finish()
        self.scope = None
        """

    def __str__(self) -> str:
        return "[timing] %s time %f" % (self.msg, self.interval)

    def restart(self):
        self.start = time.time()
        return self

    @property
    def elapsed(self) -> float:
        if self.end:
            return self.interval
        return time.time() - self.start

    @property
    def finished(self) -> bool:
        return bool(self.end)

    # Deprecated
    def elapsed_seconds(self):
        return self.interval
