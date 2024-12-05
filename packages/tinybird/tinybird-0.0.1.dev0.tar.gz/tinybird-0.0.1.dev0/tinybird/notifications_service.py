import logging
from typing import Any, Dict, List, Tuple

from tinybird.user import User, UserAccount
from tinybird.views.mailgun import MailgunService, NotificationResponse


class NotificationsService:
    _settings: Dict[str, Any] = {}

    @classmethod
    def init(cls, settings):
        cls._settings = settings

    @classmethod
    async def notify_new_account(cls, user_account: UserAccount) -> None:
        mailgun_service = MailgunService(cls._settings)
        result = await mailgun_service.send_notification_on_created_account(user_account)
        if result.status_code != 200:
            logging.error(
                f"Notification for New account not delivered to {user_account.email}, " f"reason: {result.content}"
            )

    @classmethod
    async def notify_workspace_invite(cls, admin: str, workspace: User, invitee_emails: List[str]) -> None:
        mailgun_service = MailgunService(cls._settings)
        result = await mailgun_service.send_add_to_workspace_emails(
            owner_name=admin, workspace=workspace, user_emails=invitee_emails
        )

        if result is not None and result.status_code != 200:
            logging.error(f"Addition to workspace was not delivered to {invitee_emails}, " f"reason: {result.content}")

    @classmethod
    async def notify_max_concurrent_queries_limit(
        cls, user_accounts: List[UserAccount], workspace: User, pipes_concurrency: List[Tuple[str, int]]
    ) -> NotificationResponse:
        mailgun_service = MailgunService(cls._settings)
        result = await mailgun_service.send_max_concurrent_queries_limit(
            user_accounts=user_accounts, workspace=workspace, pipes_concurrency=pipes_concurrency
        )

        if result is not None and result.status_code != 200:
            logging.exception(f"Max concurrent queries limit was not delivered, " f"reason: {result.content}")
        return result
