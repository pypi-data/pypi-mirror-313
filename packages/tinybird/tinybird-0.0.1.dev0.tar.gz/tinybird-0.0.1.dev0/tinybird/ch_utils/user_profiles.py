from enum import Enum


class WorkspaceUserProfiles(Enum):
    ENDPOINT_USER_PROFILE = "endpoint_user_profile"


WORKSPACE_PROFILES_AVAILABLE = [WorkspaceUserProfiles.ENDPOINT_USER_PROFILE.value]
