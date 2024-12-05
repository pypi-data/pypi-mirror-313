from datetime import datetime
from typing import Any, Dict, Optional

from tinybird.exploration import Exploration, Explorations
from tinybird.model import retry_transaction_in_case_of_concurrent_edition_error_async
from tinybird.token_scope import scopes
from tinybird.user import ResourceDoesNotExist, User


class ExplorationsService:
    _settings: Dict[str, Any] = {}

    @classmethod
    def init(cls, settings):
        cls._settings = settings

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def add_and_save_workspace(
        workspace_id: str, title: str, description: str, configuration: Dict[str, Any], semver: Optional[str] = None
    ):
        exploration = Explorations.create(workspace_id, title, description, configuration, semver=semver)
        with User.transaction(workspace_id) as workspace:
            workspace.explorations_ids.append(exploration.id)
        return exploration

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def remove_and_save_workspace(exploration: Exploration):
        with User.transaction(exploration.workspace_id) as workspace:
            workspace.explorations_ids = [id for id in workspace.explorations_ids if id != exploration.id]
        exploration.delete()

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def _update_exploration_token(
        exploration: Exploration, old_resource_name_or_id: str, new_resource_name_or_id: str
    ) -> None:
        # Tokens are stored inside the Workspace (User) object.
        #
        # We need to open a transaction here in order to be able
        # to make changes on them.

        with User.transaction(exploration.workspace_id) as workspace:
            # Find the token with Origin == this Time Series:
            # - Remove DATASOURCES_READ scope for the old resource.
            # - Add DATASOURCES_READ scope for the new resource.

            t = workspace.get_token_for_exploration(exploration.id)
            if not t:
                return

            new_resource_id = workspace.get_resource_id(new_resource_name_or_id)
            if not new_resource_id:
                raise ResourceDoesNotExist(new_resource_name_or_id)

            old_resource_id = workspace.get_resource_id(old_resource_name_or_id)
            if old_resource_id:  # The old resource might not exist anymore
                t.remove_scope(scopes.DATASOURCES_READ, old_resource_id)

            t.add_scope(scopes.DATASOURCES_READ, new_resource_id)

    @staticmethod
    async def update_and_save_workspace(
        exploration: Exploration,
        title: Optional[str] = None,
        description: Optional[str] = None,
        configuration: Optional[Dict[str, Any]] = None,
    ) -> Exploration:
        # If the datasource change, we must update the default token for this Time Series
        if configuration and (exploration.configuration["name"] != configuration["name"]):
            await ExplorationsService._update_exploration_token(
                exploration, exploration.configuration["name"], configuration["name"]
            )

        return await Explorations.update(exploration.id, title, description, configuration)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def register_visit(exploration: Exploration, tstamp: Optional[datetime] = None):
        tstamp = tstamp or datetime.now()
        with Exploration.transaction(exploration.id) as exploration:
            exploration.metadata["visits"] = exploration.metadata.get("visits", 0) + 1
            exploration.metadata["last_visit"] = tstamp
