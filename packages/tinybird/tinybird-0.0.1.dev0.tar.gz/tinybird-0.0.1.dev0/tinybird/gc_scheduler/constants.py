from dataclasses import dataclass

DEFAULT_TIMEZONE = "Etc/UTC"


@dataclass
class SchedulerJobActions:
    DELETE = "delete"
    CREATE = "create"
    PAUSE = "pause"
    RESUME = "resume"
    UPDATE = "update"


@dataclass
class SchedulerJobStatus:
    RUNNING = "running"
    PAUSED = "paused"
    SHUTDOWN = "shutdown"


class GCloudScheduleException(Exception):
    def __init__(self, status: int = 500, *args: object) -> None:
        super().__init__(*args)
        self.status = status


class ExistingSinkException(GCloudScheduleException):
    def __init__(self, *args: object) -> None:
        super().__init__(409, *args)


class ErrorCreatingScheduleException(GCloudScheduleException):
    def __init__(self, *args: object) -> None:
        super().__init__(500, *args)
