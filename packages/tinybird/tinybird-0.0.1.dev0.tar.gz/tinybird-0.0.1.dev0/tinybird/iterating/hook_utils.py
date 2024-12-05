import logging

from tinybird.feature_flags import FeatureFlagsWorkspaceService, FeatureFlagWorkspaces
from tinybird.user import User, Users


def allow_drop_table(workspace: User, name: str) -> bool:
    # allow to drop if not branches or releases
    if not workspace.origin:
        return True

    main_workspace = Users.get_by_id(workspace.origin)
    if not FeatureFlagsWorkspaceService.feature_for_id(
        FeatureFlagWorkspaces.VERSIONS_GA, "", main_workspace.feature_flags
    ):
        return True

    logging.warning(f"[DEPRECATED] Workspace {main_workspace.name} ({main_workspace.id}) is using VERSIONS_GA FF")
    if workspace.is_branch or workspace.is_release_in_branch:
        snapshot = workspace.get_snapshot()
        if snapshot and snapshot.get_resource(name):
            return False
    else:
        if main_workspace.get_resource(name):
            return False

    return True
