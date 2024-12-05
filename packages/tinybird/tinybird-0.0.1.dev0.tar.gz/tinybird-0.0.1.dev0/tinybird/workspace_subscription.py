import uuid
from typing import Union, cast

from tinybird.model import RedisModel


class WorkspaceSubscriptionAlreadyExists(Exception):
    pass


class WorkspaceSubscriptionDoesNotExist(Exception):
    pass


class WorkspaceSubscription(RedisModel):
    __namespace__ = "subscription"

    __props__ = ["workspace_id", "subscription_id", "settings"]
    # settings:
    # - subscription_items
    # - last_date_usage_record

    __owners__ = {"workspace_id", "subscription_id"}

    def __init__(self, **workspace_subscription: Union[str, dict]) -> None:
        self.workspace_id: str = cast(str, workspace_subscription.get("workspace_id"))
        self.subscription_id: str = cast(str, workspace_subscription.get("subscription_id"))
        self.settings: dict = cast(dict, workspace_subscription.get("settings", {}))

        super().__init__(**workspace_subscription)

    def __getitem__(self, item):
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            raise AttributeError(f"'WorkspaceSubscription' does not contain the '{item}' attribute")

    @staticmethod
    def create(workspace_id: str, subscription_id: str) -> "WorkspaceSubscription":
        uid = str(uuid.uuid4())

        if WorkspaceSubscription.get_by_workspace(workspace_id):
            raise WorkspaceSubscriptionAlreadyExists(f"Workspace {workspace_id} already has a subscription")

        if WorkspaceSubscription.get_by_subscription(subscription_id):
            raise WorkspaceSubscriptionAlreadyExists(f"Subscription {subscription_id} is already registered")

        config = {"id": uid, "workspace_id": workspace_id, "subscription_id": subscription_id}

        workspace_subscription = WorkspaceSubscription(**config)
        workspace_subscription.save()

        created_subscription = WorkspaceSubscription.get_by_id(uid)
        if not created_subscription:
            raise WorkspaceSubscriptionDoesNotExist(f"WorkspaceSubscription {uid} does not exist")
        return created_subscription

    @staticmethod
    def get_by_workspace(workspace_id):
        try:
            subscription = WorkspaceSubscription.get_all_by_owner(workspace_id)
            if subscription:
                return subscription[0]
            return None
        except Exception:
            raise WorkspaceSubscriptionDoesNotExist("This workspace does not have any subscription")

    @staticmethod
    def get_by_subscription(subscription_id):
        try:
            subscription = WorkspaceSubscription.get_all_by_owner(subscription_id)
            if subscription:
                return subscription[0]
            return None
        except Exception:
            raise WorkspaceSubscriptionDoesNotExist("There is no workspace with this subscription")
