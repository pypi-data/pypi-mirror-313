import logging
import re
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

from packaging import version

if TYPE_CHECKING:
    from tinybird.datasource import Datasource
    from tinybird.user import ReleaseWorkspace, User

SEMVER_REGEX = r"^\d+\.\d+\.\d+(-(\d+|snapshot))?$"


class ReleaseStatus(Enum):
    live = "live"
    preview = "preview"
    rollback = "rollback"
    deploying = "deploying"
    failed = "failed"
    # This is a transient status, it is used it to avoid having two "live" releases when doing a rollback and before deleting the previous live release
    deleting = "deleting"


class ReleaseStatusException(Exception):
    pass


class LiveReleaseProtectedException(ReleaseStatusException):
    pass


class MaxNumberOfReleasesReachedException(ReleaseStatusException):
    pass


class DeleteRemoteException(Exception):
    pass


class Release:
    def __init__(
        self,
        commit: str,
        semver: str,
        id: str,
        status: ReleaseStatus,
        created_at: Optional[datetime] = None,
    ) -> None:
        self.commit = commit
        self.id: str = id
        self.created_at = created_at or datetime.now()
        self.semver = semver
        self.status: ReleaseStatus = status

    def __repr__(self) -> str:
        return f"{self.__class__}({self.id}/{self.commit}/{self.semver}/{self.status.value})"

    def to_dict(self) -> Dict[str, Any]:
        obj = {
            "id": str(self.id),
            "commit": self.commit,
            "created_at": self.created_at,
            "semver": self.semver,
            "status": self.status.value,
        }
        return obj

    def to_json(self) -> Dict[str, Any]:
        release = self.to_dict()
        release["created_at"] = release["created_at"].isoformat()
        return release

    async def get_resources_to_delete(self, releases: List["Release"]) -> Tuple[List[str], List[str]]:
        try:
            wmv = self.metadata
            if not wmv:
                raise AttributeError("Release metadata is None")
        except AttributeError as e:
            logging.exception(
                f"Cannot find metadata for release {self.semver} - id: {self.id} - commit: {self.commit} - {str(e)}"
            )
            return [], []

        # only clickhouse resources
        rs: Dict[str, Dict[str, Dict[str, str]]] = {
            "used": {"datasources": {}, "pipes": {}, "nodes": {}},
            "unused": {"datasources": {}, "pipes": {}},
        }
        for other_release in releases:
            if other_release.id != self.id:
                try:
                    other_wmv = other_release.metadata
                    if other_wmv is None:
                        raise AttributeError("Release metadata is None")
                except AttributeError as e:
                    logging.exception(
                        f"Cannot find metadata for release {other_release.semver} - id: {other_release.id} - commit: {other_release.commit} - {str(e)}"
                    )
                    continue
                for ds in wmv.get_datasources():
                    if other_wmv.get_datasource(ds.id):
                        rs["used"]["datasources"][ds.name] = other_release.semver
                for pipe in wmv.get_pipes():
                    for node in pipe.pipeline.nodes:
                        if node.materialized:
                            for other_pipe in other_wmv.get_pipes():
                                for other_node in other_pipe.pipeline.nodes:
                                    if other_node.materialized and other_node.id == node.id:
                                        rs["used"]["pipes"][pipe.name] = other_release.semver
                                        rs["used"]["nodes"][node.id] = other_release.semver
                                        if other_ds := other_wmv.get_datasource(node.materialized):
                                            rs["used"]["datasources"][other_ds.name] = other_release.semver
        for ds in wmv.get_datasources():
            if ds.name not in rs["used"]["datasources"]:
                rs["unused"]["datasources"][ds.name] = self.semver
        for pipe in wmv.get_pipes():
            if pipe.name not in rs["used"]["pipes"]:
                rs["unused"]["pipes"][pipe.name] = self.semver
        return list(rs["unused"]["datasources"].keys()), list(rs["unused"]["pipes"].keys())

    @property
    def is_post(self) -> bool:
        return is_post(self.semver)

    @property
    def is_rollback(self) -> bool:
        return self.status == ReleaseStatus.rollback

    @property
    def is_live(self) -> bool:
        return self.status == ReleaseStatus.live

    @property
    def is_deploying(self) -> bool:
        return self.status == ReleaseStatus.deploying

    @property
    def is_preview(self) -> bool:
        return self.status == ReleaseStatus.preview

    @property
    def metadata(self) -> Optional["ReleaseWorkspace"]:
        from tinybird.user import ReleaseWorkspace, User

        workspace: Optional["User"] = User.get_by_id(self.id)

        if workspace is None:
            logging.warning(f"Workspace is None while getting metadata release: {self.to_json()}")
            return None

        # Use the origin resources when the release is "live" because resources can be deployed directly to the workspace
        # https://gitlab.com/tinybird/analytics/-/issues/10665
        if workspace.origin:
            workspace_origin: Optional["User"] = User.get_by_id(workspace.origin)
            is_live_release_main = self.is_live and not workspace.is_branch and workspace_origin
            is_live_release_branch = (
                self.is_live and workspace.is_branch and workspace_origin and workspace_origin.origin
            )

            if is_live_release_main or is_live_release_branch:
                assert workspace_origin
                return ReleaseWorkspace(workspace_origin)

        return ReleaseWorkspace(workspace)

    def get_datasource(self, id_or_name: str) -> Optional["Datasource"]:
        return self.metadata.get_datasource(id_or_name) if self.metadata else None

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> "Release":
        return Release(
            commit=dict["commit"],
            id=dict["id"],
            created_at=dict["created_at"],
            semver=dict.get("semver", "0.0.0"),
            status=ReleaseStatus(dict.get("status", "live")),
        )

    @classmethod
    def sort_by_date(cls, releases: List["Release"], reverse: bool = True) -> List["Release"]:
        return sorted(releases, key=lambda x: x.created_at, reverse=reverse)


def validate_release_semver(semver_str: str, release: "Release") -> bool:
    """
    Validates if the provided semver_str is less than the Release's semver.

    The function returns False if the Release.semver is greater than or equal to the semver_str,
    and True otherwise. If the release's semver contains '-snapshot', it is ignored in the comparison.

    Args:
    semver_str (str): A semantic version string to compare.
    release (Release): An instance of Release with a semver attribute.

    Returns:
    bool: False if semver_str is less than release's semver, True otherwise.

    Examples:
        >>> r1 = Release("commit", "1.0.0", "1", "live")
        >>> validate_release_semver("0.9.0", r1)
        False

        >>> r2 = Release("commit", "1.0.0-snapshot", "1", "live")
        >>> validate_release_semver("1.0.0", r2)
        True

        >>> r3 = Release("commit", "2.0.0-snapshot", "1", "live")
        >>> validate_release_semver("1.0.0", r3)
        False

        >>> r4 = Release("commit", "1.0.0-snapshot", "1", "live")
        >>> validate_release_semver("1.0.1", r4)
        True

        >>> r5 = Release("commit", "2.0.0", "1", "live")
        >>> validate_release_semver("2.1.0", r5)
        True

        >>> r6 = Release("commit", "2.0.0", "1", "live")
        >>> validate_release_semver("2.0.0", r6)
        False

        >>> r7 = Release("commit", "2.0.0-snapshot", "1", "live")
        >>> validate_release_semver("2.0.0", r7)
        True

        >>> r8 = Release("commit", None, "1", "live")
        >>> validate_release_semver("1.0.0", r8)
        Traceback (most recent call last):
        ...
        tinybird.iterating.release.ReleaseStatusException: VERSION is required

        >>> r9 = Release("commit", "invalid-semver", "1", "live")
        >>> validate_release_semver("1.0.0", r9) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        ReleaseStatusException: invalid-semver is not a valid semver format

    Note: The doctests assume the 'packaging' module is installed and available.
    """
    try:
        if not release.semver:
            raise ReleaseStatusException("VERSION is required")
        if "snapshot" in release.semver and "snapshot" not in semver_str:
            return version.parse(release.semver.split("-snapshot")[0]) <= version.parse(semver_str)
        if "snapshot" in semver_str and "snapshot" not in release.semver:
            return version.parse(release.semver) <= version.parse(semver_str.split("-snapshot")[0])
        return version.parse(release.semver.split("-snapshot")[0]) < version.parse(semver_str.split("-snapshot")[0])
    except ReleaseStatusException:
        raise
    except version.InvalidVersion:
        raise ReleaseStatusException(f"{release.semver} is not a valid semver format")
    except Exception:
        return False


def validate_semver_greater_than_workspace_releases(workspace: "User", semver: str) -> "User":
    releases = workspace.get_releases()
    previews = [r for r in releases if r.is_preview]
    if is_post(semver) and any(previews):
        raise ReleaseStatusException(
            f"Cannot create post Release {semver} in {workspace.name}. There's a Release {previews[0].semver} in Preview. Promote it to live first."
        )
    for r in releases:
        if not validate_release_semver(semver, r):
            raise ReleaseStatusException(
                f"Cannot create Release in {workspace.name}. There's a Release in '{r.status.value}' status with a higher or equal version '{semver}'. Bump the VERSION and try again."
            )
    return workspace


def validate_semver(semver_str: str) -> bool:
    """
    Validates a semver string.

    Args:
        semver_str (str): The semver string to validate.

    Returns:
        bool: True if the semver string is valid, False otherwise.

    Examples:
        >>> validate_semver('1.0.0')
        True

        >>> validate_semver('1.2.3-alpha')
        False

        >>> validate_semver('1.2.3-snapshot')
        True

        >>> validate_semver('1.0')
        False

        >>> validate_semver('1.2.3.')
        False

        >>> validate_semver('invalid')
        False

        >>> validate_semver('0.0.1-2')
        True

        >>> validate_semver('0.0.1-1')
        True

        >>> validate_semver('0.0.1-whatever')
        False
    """
    pattern = r"^\d+\.\d+\.\d+(-\d+)?$|^.*-snapshot$"
    match = re.match(pattern, semver_str)
    return match is not None


def is_post(semver: str) -> bool:
    if semver and "-" in semver and semver.split("-")[-1] != "snapshot":
        return True
    return False
