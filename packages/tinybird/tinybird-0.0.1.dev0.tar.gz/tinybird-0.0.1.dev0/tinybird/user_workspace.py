import logging
import uuid
from typing import Any, List, Optional, Union, cast

from tinybird.constants import USER_WORKSPACE_NOTIFICATIONS, Relationships, user_workspace_relationships
from tinybird.token_scope import scopes

from .model import RedisModel


class UserWorkspaceRelationshipDoesNotExist(Exception):
    pass


class UserWorkspaceRelationshipAlreadyExists(Exception):
    pass


class UserWorkspaceRelationshipException(Exception):
    pass


class UserWorkspaceRelationships:
    @staticmethod
    def change_role(user_id: str, workspace: Any, new_role: str) -> None:
        from tinybird.user import User as Workspace

        workspace = cast(Workspace, workspace)

        if new_role not in user_workspace_relationships:
            raise UserWorkspaceRelationshipException(
                f"Role '{new_role}' is not valid. Roles available: {user_workspace_relationships}."
            )

        user_workspace_relationship = UserWorkspaceRelationship.get_by_user_and_workspace(user_id, workspace.id)
        if not user_workspace_relationship:
            raise UserWorkspaceRelationshipException(f"User '{user_id}' doesn't have access to this Workspace.")
        else:
            with UserWorkspaceRelationship.transaction(user_workspace_relationship.id) as uw:
                uw.relationship = new_role

        UserWorkspaceRelationships.rename_user_token_by_role(user_id, workspace, new_role)

    @staticmethod
    def rename_user_token_by_role(user_id: str, workspace: Any, role: Optional[str]) -> None:
        from tinybird.user import User as Workspace
        from tinybird.user import UserAccount

        workspace = cast(Workspace, workspace)

        # Update the admin token name based on the new role
        admin_user_tokens = workspace.get_access_tokens_for_resource(user_id, scope=scopes.ADMIN_USER)
        if not len(admin_user_tokens):
            logging.info(f"No tokens to rename on changing to role '{role}'")
            return

        for admin_user_token in admin_user_tokens:
            old_name: str = admin_user_token.name
            prefix: str = "viewer" if role and (role.lower() == Relationships.VIEWER) else "admin"
            user_account = UserAccount.get_by_id(user_id)
            if not user_account:
                logging.exception(f"User {user_id} not found")
                continue

            admin_user_token.name = f"{prefix} {user_account.email}"
            logging.info(
                f"Renamed token {old_name} ({admin_user_token.id}) to {admin_user_token.name} due to role '{role}'"
            )


class UserWorkspaceRelationship(RedisModel):
    __namespace__ = "user_workspace_relationship"

    __props__ = ["user_id", "workspace_id", "relationship"]

    __owners__ = {"user_id", "workspace_id"}

    def __init__(self, **user_workspace_relationship_dict: str):
        self.user_id: str = cast(str, user_workspace_relationship_dict.get("user_id"))
        self.workspace_id: str = cast(str, user_workspace_relationship_dict.get("workspace_id"))
        self.relationship: str = cast(str, user_workspace_relationship_dict.get("relationship"))

        super().__init__(**user_workspace_relationship_dict)

    def __getitem__(self, item):
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            raise AttributeError(f"'UserWorkspaceRelationship' does not contain the '{item}' attribute")

    @staticmethod
    def create_relationship(user_id, workspace_id, relationship):
        uid = str(uuid.uuid4())

        if UserWorkspaceRelationship.user_has_access(user_id, workspace_id):
            raise UserWorkspaceRelationshipAlreadyExists(f"User {user_id} already has access to {workspace_id}")

        config = {"id": uid, "user_id": user_id, "workspace_id": workspace_id, "relationship": relationship}

        user_workspace_relationship = UserWorkspaceRelationship(**config)
        user_workspace_relationship.save()

        return UserWorkspaceRelationship.get_by_id(uid)

    @staticmethod
    def get_by_user(user_id: str) -> List["UserWorkspaceRelationship"]:
        try:
            return UserWorkspaceRelationship.get_all_by_owner(user_id)
        except Exception:
            raise UserWorkspaceRelationshipDoesNotExist("The user does not have any workspace")

    @staticmethod
    def get_by_workspace(workspace_id: str, limit: int = 100) -> List["UserWorkspaceRelationship"]:
        try:
            return UserWorkspaceRelationship.get_all_by_owner(workspace_id, limit)
        except Exception:
            raise UserWorkspaceRelationshipDoesNotExist("The workspace can not be reached")

    @staticmethod
    def get_by_user_and_workspace(user_id: str, workspace_id: str) -> Optional["UserWorkspaceRelationship"]:
        user_workspaces = UserWorkspaceRelationship.get_by_user(user_id)
        return next((uw for uw in user_workspaces if uw.workspace_id == workspace_id), None)

    @staticmethod
    def get_user_workspaces_by_relationship(user_id: str, relationship: str) -> List["UserWorkspaceRelationship"]:
        user_workspaces = UserWorkspaceRelationship.get_by_user(user_id)
        return [user_workspace for user_workspace in user_workspaces if user_workspace.relationship == relationship]

    @staticmethod
    def user_is_admin(user_id: str, workspace_id: str) -> bool:
        user_workspaces = UserWorkspaceRelationship.get_by_user(user_id)
        return any(
            map(
                lambda user_workspace: user_workspace.workspace_id == workspace_id
                and user_workspace.relationship == Relationships.ADMIN,
                user_workspaces,
            )
        )

    @staticmethod
    def user_is_viewer(user_id: str, workspace_id: str) -> bool:
        user_workspaces = UserWorkspaceRelationship.get_by_user(user_id)
        return any(
            map(
                lambda user_workspace: user_workspace.workspace_id == workspace_id
                and user_workspace.relationship == Relationships.VIEWER,
                user_workspaces,
            )
        )

    @staticmethod
    def user_has_access(user_id: str, workspace_id: str) -> bool:
        user_workspaces = UserWorkspaceRelationship.get_by_user(user_id)
        return any(map(lambda user_workspace: user_workspace.workspace_id == workspace_id, user_workspaces))

    @staticmethod
    def user_can_write(user_id: str, workspace_id: str) -> bool:
        if not UserWorkspaceRelationship.user_has_access(user_id, workspace_id):
            return False

        user_workspaces = UserWorkspaceRelationship.get_by_user(user_id)
        return next(
            (
                True
                for w in user_workspaces
                if w.workspace_id == workspace_id and w.relationship != Relationships.VIEWER
            ),
            False,
        )


class UserWorkspaceNotificationsDoesNotExist(Exception):
    pass


class UserWorkspaceNotificationsException(Exception):
    pass


class UserWorkspaceNotificationsHandler:
    @staticmethod
    def change_notifications(user_id: str, workspace_id: str, notifications: List[str]):
        for notification in notifications:
            if notification != "" and notification not in USER_WORKSPACE_NOTIFICATIONS:
                raise UserWorkspaceNotificationsException(
                    f"Notification '{notification}' is not valid. Notifications available: {USER_WORKSPACE_NOTIFICATIONS}."
                )

        user_workspace_notifications = UserWorkspaceNotifications.get_by_user_and_workspace(user_id, workspace_id)
        if not user_workspace_notifications:
            UserWorkspaceNotifications.create_notifications(user_id, workspace_id, notifications)
        else:
            with UserWorkspaceNotifications.transaction(user_workspace_notifications.id) as uw:
                uw.notifications = notifications


class UserWorkspaceNotifications(RedisModel):
    __namespace__ = "user_workspace_notifications"

    __props__ = ["user_id", "workspace_id", "notifications"]

    __owners__ = {"user_id", "workspace_id"}

    def __init__(self, **user_workspace_notifications_dict: Union[str, List[str]]):
        self.user_id: str = cast(str, user_workspace_notifications_dict["user_id"])
        self.workspace_id: str = cast(str, user_workspace_notifications_dict["workspace_id"])
        self.notifications: List[str] = cast(List[str], user_workspace_notifications_dict["notifications"])

        super().__init__(**user_workspace_notifications_dict)

    @staticmethod
    def create_notifications(user_id, workspace_id, notifications):
        uid = str(uuid.uuid4())

        config = {"id": uid, "user_id": user_id, "workspace_id": workspace_id, "notifications": notifications}

        user_workspace_notifications = UserWorkspaceNotifications(**config)
        user_workspace_notifications.save()

        return UserWorkspaceNotifications.get_by_id(uid)

    @staticmethod
    def get_by_user(user_id: str) -> List["UserWorkspaceNotifications"]:
        try:
            return UserWorkspaceNotifications.get_all_by_owner(user_id)
        except Exception:
            raise UserWorkspaceNotificationsDoesNotExist("The user does not have any workspace")

    @staticmethod
    def get_by_user_and_workspace(user_id, workspace_id):
        user_notifications = UserWorkspaceNotifications.get_by_user(user_id)
        return next((uw for uw in user_notifications if uw.workspace_id == workspace_id), None)
