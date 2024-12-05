import logging
import uuid
from typing import Any, Dict, List, Optional

from opentracing import Span

from tinybird.auth0_client import Auth0Client
from tinybird.datasource import Datasource, SharedDatasource
from tinybird.model import retry_transaction_in_case_of_concurrent_edition_error_async
from tinybird.token_scope import scopes
from tinybird.tracing import ClickhouseTracer
from tinybird.user import TokenUsedInConnector, User, UserAccount, UserAccountDoesNotExist, UserAccounts, Users
from tinybird.views.api_errors.workspaces import WorkspacesServerErrorInternal
from tinybird.views.base import ApiHTTPError
from tinybird_shared.redis_client.redis_client import TBRedisClientSync


class UserAccountsService:
    _settings: Dict[str, Any] = {}
    _auth0_client: Auth0Client

    @classmethod
    def init(cls, settings):
        cls._settings = settings
        cls._auth0_client = Auth0Client(settings["auth0_api"])

    @classmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def activate_user(cls, user: UserAccount) -> None:
        with UserAccount.transaction(user.id) as user_account:
            user_account["confirmed_account"] = True

    @classmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def enable_region_selected(cls, user_account: UserAccount) -> None:
        with UserAccount.transaction(user_account.id) as user_account:
            user_account["region_selected"] = True

    @classmethod
    async def register_user(
        cls,
        email: str,
        password: str,
        confirmed_account: bool = False,
        register_event: str = "NewUserRegistered",
        overwrriten_redis_Client: Optional[TBRedisClientSync] = None,
        region_selected: bool = False,
        notify_user: bool = False,
    ) -> UserAccount:
        if not email or not email.strip() or not password or not password.strip():
            raise Exception("Email or password are empty")

        user_account = UserAccount.register(email, password, overwrriten_redis_Client)

        if confirmed_account or UserAccounts.confirmed_account(user_account):
            if overwrriten_redis_Client:
                user_account["confirmed_account"] = True
                UserAccount.save_to_redis(user_account, overwrriten_redis_Client)
            else:
                await cls.activate_user(user_account)

        if region_selected:
            if overwrriten_redis_Client:
                user_account["region_selected"] = True
                UserAccount.save_to_redis(user_account, overwrriten_redis_Client)
            else:
                await cls.enable_region_selected(user_account)
        try:
            tracer: ClickhouseTracer = cls._settings["opentracing_tracing"].tracer
            span: Span = tracer.start_span()
            span.set_operation_name(register_event)
            span.set_tag("user_email", user_account.email)
            span.set_tag("user", user_account.id)
            span.set_tag("http.status_code", 200)
            tracer.record(span)

        except Exception as e:
            logging.exception(f"Could not record new registered user '{email}', reason: {e}")

        if overwrriten_redis_Client:
            account = UserAccount.get_by_id_from_redis(overwrriten_redis_Client, user_account.id)
        else:
            account = UserAccount.get_by_id(user_account.id)

        assert isinstance(account, UserAccount)

        # -- Welcome email being sent from Hubspot
        # if notify_user:
        #     await NotificationsService.notify_new_account(account)

        return account

    @classmethod
    async def register_users_if_dont_exist(cls, user_emails: List[str], notify_users: bool = False) -> None:
        for user_email in user_emails:
            try:
                invited_user = UserAccounts.get_by_email(user_email)
            except UserAccountDoesNotExist:
                invited_user = None

            if not invited_user:
                try:
                    await cls.register_user(
                        email=user_email,
                        password=str(uuid.uuid4()),
                        confirmed_account=True,
                        register_event="NewUserInvited",
                        notify_user=notify_users,
                    )
                except Exception as e:
                    logging.exception(e)
                    error = WorkspacesServerErrorInternal.failed_register_user(name=user_email, error=str(e))
                    raise ApiHTTPError.from_request_error(error)

    @classmethod
    async def get_auth_provider_info(cls, user: UserAccount) -> Optional[Dict[str, Any]]:
        logins_count = 0

        users = await cls._auth0_client.get_users_by_email(user["email"].lower())
        for u in users:
            logins_count = logins_count + u.get("logins_count", 0)

        # Construct an object with a custom, vendor-agnostic schema
        return {"logins_count": logins_count}

    @classmethod
    async def has_uniquely_shared_datasources(cls, user: UserAccount) -> bool:
        shared_ds = await cls.get_uniquely_shared_datasources(user)
        return len(shared_ds) > 0

    @classmethod
    async def get_uniquely_shared_datasources(cls, user: UserAccount) -> List[Datasource]:
        """Returns the list of the Datasource objects that this UserAccount uniquely shares with Workspaces owned by other UserAccounts"""
        result: List[Datasource] = []

        owned_workspaces: List[User] = [User.get_by_id(w.workspace_id) for w in user.owned_workspaces]
        for workspace in owned_workspaces:
            if workspace is None:
                logging.warning(f"Inconsistency: User {user.id}/{user.email} has bad workspace relationships")
                continue

            # Discard if there are more users in the Workspace
            if len(workspace.user_accounts) > 1:
                continue

            for datasource in workspace.get_datasources():
                # Discard 'incoming' shares
                if isinstance(datasource, SharedDatasource):
                    continue

                for dest_workspace_id in datasource.shared_with:
                    # Discard if both WS are owned by this UserAccount
                    if next((w for w in owned_workspaces if w.id == dest_workspace_id), None) is not None:
                        continue

                    result.append(datasource)
                    break

        return result

    @classmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def _mark_used_as_disabled(cls, user: UserAccount) -> UserAccount:
        with UserAccount.transaction(user.id) as user_account:
            user_account.confirmed_account = False
        return user

    @classmethod
    async def disable_user(cls, user: UserAccount, unshare_datasources: bool) -> None:
        user = await cls._mark_used_as_disabled(user)

        if unshare_datasources:
            workspaces = [User.get_by_id(w.workspace_id) for w in user.owned_workspaces]
            for wkspc in workspaces:
                await Users.unshare_all_data_sources_in_this_workspace(wkspc, user, True)

        user_workspaces = await user.get_relationships_and_workspaces()

        for _, workspace in user_workspaces:
            tokens = workspace.get_tokens_for_resource(user.id, scopes.ADMIN_USER)
            for token in tokens:
                try:
                    await Users.refresh_token(workspace, token)
                except TokenUsedInConnector as e:
                    raise Exception(
                        f"The admin token of user '{user.email}' is used in workspace '{workspace.name}' by 1 or more connectors: {str(e)}"
                    )

    @classmethod
    async def get_auth_connection_by_email(cls, email: str) -> Optional[str]:
        connection = await cls._auth0_client.get_connection_by_domain(email)
        if not connection:
            return None

        return connection
