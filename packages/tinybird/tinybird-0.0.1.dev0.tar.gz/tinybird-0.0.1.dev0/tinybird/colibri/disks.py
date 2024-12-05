from dataclasses import astuple, dataclass, field
from typing import Iterator, TypeVar

T = TypeVar("T", bound="ServerDisk")


@dataclass
class ServerDisk:
    server: str
    name: str
    fstype: str
    size: int
    mountpoint: str
    used: float
    cloud_id: str
    cloud_project_id: str = field(init=False)
    cloud_size: int = field(init=False)
    cloud_disk_name: str = field(init=False)
    cloud_disk_zone: str = field(init=False)
    perc_used: float = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.perc_used = round((self.used * 100 / self.size), 2) if self.size > 0 else 0
        return

    def __iter__(self) -> Iterator[T]:
        return iter(astuple(self))

    def add_cloud_project_id(self, project_id: str) -> None:
        self.cloud_project_id = project_id

    def add_cloud_size(self, size: int) -> None:
        self.cloud_size = size

    def add_cloud_disk_name(self, name: str) -> None:
        self.cloud_disk_name = name

    def add_cloud_disk_zone(self, zone: str) -> None:
        self.cloud_disk_zone = zone
