from dataclasses import asdict, dataclass, field
from typing import Optional

from packaging import version

from tinybird.iterating.release import Release
from tinybird.user import User, Users
from tinybird.workspace_service import WorkspaceDiff, WorkspaceService


@dataclass
class SemverDiff(WorkspaceDiff):
    semver: str

    @classmethod
    def build_from_workspacediff(cls, semver: str, workspacediff: WorkspaceDiff) -> "SemverDiff":
        return SemverDiff(semver=semver, **asdict(workspacediff))


@dataclass
class CompareResponse:
    outdated: bool = False
    diff: SemverDiff = field(default_factory=SemverDiff.build_empty)


class CompareException(Exception):
    pass


class CompareExceptionNotFound(Exception):
    pass


class Compare:
    async def env_to_prod(cls, env: User) -> CompareResponse:
        main_workspace = Users.get_by_id(env.origin) if env.origin else None
        if main_workspace is None:
            raise CompareException(f"Branch {env.id} with no 'main' Workspace")
        if main_workspace.current_release and not env.get_release_by_semver(main_workspace.current_release.semver):
            return CompareResponse(outdated=True)
        else:
            snapshot = env.get_snapshot()
            # fallback
            prod_env = snapshot if snapshot and hasattr(snapshot, "_database") else main_workspace
            diff = await WorkspaceService.compare_workspaces(prod_env, env)
            semver_diff = SemverDiff.build_from_workspacediff(
                env.current_release.semver if env.current_release else "", diff
            )
            return CompareResponse(diff=semver_diff)

    async def release_to_live(cls, workspace: User, semver: str) -> CompareResponse:
        release: Optional[Release] = workspace.get_release_by_semver(semver)
        if not release:
            raise CompareExceptionNotFound(f"Release {semver} not found in Workspace {workspace.name}")

        if release.is_live:
            raise CompareException(f"Release {semver} is already Live")

        release_workspace = Users.get_by_id(release.id)
        if not release_workspace:
            raise CompareExceptionNotFound(f"Release {semver} not found")

        live_release = workspace.current_release
        if not live_release:
            raise CompareExceptionNotFound(f"Live release not found on Workspace {workspace.name}")

        live_release_workspace = Users.get_by_id(live_release.id)
        if not live_release_workspace:
            raise CompareExceptionNotFound(f"Live release not found on Workspace {workspace.name}")

        live_release_version = version.parse(live_release.semver)
        release_version = version.parse(semver)

        if live_release_version < release_version:
            diff = await WorkspaceService.compare_workspaces(live_release_workspace, release_workspace)
            release_ref = str(release_version)
        else:
            diff = await WorkspaceService.compare_workspaces(release_workspace, live_release_workspace)
            release_ref = str(live_release_version)
        return CompareResponse(diff=SemverDiff.build_from_workspacediff(release_ref, diff))
