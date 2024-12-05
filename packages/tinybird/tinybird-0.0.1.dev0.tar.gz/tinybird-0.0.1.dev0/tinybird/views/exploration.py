from typing import Optional

from tinybird.exploration import Exploration
from tinybird.explorations_service import ExplorationsService
from tinybird.token_origin import Origins
from tinybird.user import User
from tinybird.views.base import ApiHTTPError, WebBaseHandler


class ExplorationHandler(WebBaseHandler):
    async def get(self, exploration_id: str) -> None:
        exploration: Optional[Exploration] = Exploration.get_by_id(exploration_id)
        if not exploration or not exploration.published:
            raise ApiHTTPError(404, "Not found")

        workspace: Optional[User] = User.get_by_id(exploration.workspace_id)
        if not workspace:
            raise ApiHTTPError(404, "Not found")

        token: Optional[str] = workspace.get_token_for_origin(Origins.TIMESERIES, exploration_id)
        if not token:
            raise ApiHTTPError(404, "Not found")

        await ExplorationsService.register_visit(exploration)

        self.render("timeseries_public.html")
