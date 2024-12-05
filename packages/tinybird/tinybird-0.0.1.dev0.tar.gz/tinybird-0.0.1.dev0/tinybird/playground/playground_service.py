from typing import Any, Dict, List, Optional, TypeGuard

from tinybird.model import retry_transaction_in_case_of_concurrent_edition_error_async
from tinybird.playground.playground import Playground, PlaygroundException, PlaygroundNotFoundException, Playgrounds
from tinybird.user import User, UserAccount


class PlaygroundService:
    @staticmethod
    def get_playgrounds(workspace_id: str, user_id: str, semver: Optional[str]) -> List[Playground]:
        return Playgrounds.get_playgrounds(workspace_id, user_id, semver)

    @staticmethod
    def get_playground(user_id: str, playground_id: Optional[str]) -> Playground:
        if not playground_id:
            raise PlaygroundNotFoundException()
        playground = Playgrounds.get_playground(playground_id)
        if not playground:
            raise PlaygroundNotFoundException()
        if not playground.has_access(user_id):
            raise PlaygroundNotFoundException()
        return playground

    @staticmethod
    def get_playground_by_workspace(
        workspace_id: str, playground_id: Optional[str], semver: Optional[str]
    ) -> Optional[Playground]:
        if not playground_id:
            return None
        workspace_playgrounds = Playgrounds.get_by_workspace(workspace_id, semver)

        def filter_func(
            playground: Playground,
        ) -> TypeGuard[Playground | None]:
            return playground.id == playground_id

        return next(
            filter(
                filter_func,
                workspace_playgrounds,
            ),
            None,
        )

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def create_playground(
        workspace_id: str,
        user_id: str,
        name: str,
        description: Optional[str],
        nodes: Optional[List[Dict[str, Any]]],
        semver: Optional[str] = None,
    ):
        playgrounds = Playgrounds.get_by_workspace(workspace_id=workspace_id, semver=semver)
        Playground.validate({"name": name, "nodes": nodes})
        if name in [playground.name for playground in playgrounds]:
            raise PlaygroundException("Playground with this name already exists")

        return Playgrounds.create_playground(
            workspace_id=workspace_id, user_id=user_id, name=name, description=description, nodes=nodes, semver=semver
        )

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def update_playground(workspace_id: str, user_id: str, playground: Playground, data: Dict[str, Any]):
        shared_with = data.get("shared_with", None)
        if shared_with is not None:
            if not playground.is_owner(user_id):
                raise PlaygroundException("Only owners can share Playgrounds")
            workspace = User.get_by_id(workspace_id)
            if not workspace:
                raise PlaygroundException("Workspace not found")
            all_users_exist = all(UserAccount.get_by_id(user_id) for user_id in shared_with)
            if not all_users_exist:
                raise PlaygroundException("Some users you are trying to share with do not exist")
        Playground.validate(data)
        return await Playgrounds.update_playground(playground.id, data)

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def delete_playground(user_id: str, playground: Playground):
        if not playground.is_owner(user_id):
            raise PlaygroundException("Only owners can delete Playgrounds")
        await Playgrounds.delete_playground(playground)
