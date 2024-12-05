# If you are searching for: time-series, timeseries or time series, this is your place...

from datetime import datetime
from typing import Any, Dict, Optional

from tornado.web import url

from tinybird.exploration import Exploration, ExplorationDoesNotExist, Explorations
from tinybird.explorations_service import ExplorationsService
from tinybird.token_origin import Origins
from tinybird.user import User

from .base import ApiHTTPError, BaseHandler, authenticated, with_scope_admin


def format_exploration(exploration: Exploration, full_detail: bool = True) -> Dict[str, Any]:
    last_visit: Optional[datetime] = exploration.metadata.get("last_visit", None)

    return {
        "id": exploration.id,
        "title": exploration.title,
        "description": exploration.description,
        "configuration": exploration.configuration if full_detail else {},
        "published": exploration.published,
        "updated_at": exploration.updated_at.isoformat() if exploration.updated_at else None,
        "metadata": {
            "visits": exploration.metadata["visits"],
            "last_visit": last_visit.isoformat() if last_visit else None,
        },
    }


class ExplAPIBase(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    def _check_exploration_acces(self, exploration_id: str) -> Exploration:
        """Gets the requested Exploration object and validates it belongs to the current Workspace.

        Raises an HTTP 404 error on any access issue.
        """
        if not exploration_id:
            raise ApiHTTPError(404, "Not found")

        workspace = self.get_workspace_from_db()
        if exploration_id not in workspace.explorations_ids:
            raise ApiHTTPError(404, "Not found")

        try:
            return Explorations.get_by_id(exploration_id)
        except ExplorationDoesNotExist:
            raise ApiHTTPError(404, "Not found")


class APIExplorationsHandler(ExplAPIBase):
    @authenticated
    @with_scope_admin
    async def get(self):
        workspace = self.get_workspace_from_db()
        full_detail = str(self.get_argument("full", "true")).lower() == "true"
        semver: Optional[str] = self.get_argument("__tb__semver", None)

        def fmt(expl):
            return format_exploration(expl, full_detail=full_detail)

        self.write_json({"timeseries": tuple(map(fmt, workspace.get_explorations(semver=semver)))})

    @authenticated
    @with_scope_admin
    async def post(self):
        title = self.get_argument("title")
        description = self.get_argument("description", None)
        raw_configuration = self.get_argument("configuration")
        semver: Optional[str] = self.get_argument("__tb__semver", None)
        configuration = Exploration.parse_and_validate(raw_configuration)
        if configuration is None:
            raise ApiHTTPError(400, "Invalid JSON blob")

        workspace = self.get_workspace_from_db()
        if workspace.is_release:
            workspace = workspace.get_main_workspace()

        exploration = await ExplorationsService.add_and_save_workspace(
            workspace.id, title, description, configuration, semver
        )

        self.write_json(format_exploration(exploration, full_detail=True))


class APISingleExplorationHandler(ExplAPIBase):
    @authenticated
    @with_scope_admin
    async def get(self, exploration_id):
        exploration = self._check_exploration_acces(exploration_id)
        self.write_json(format_exploration(exploration, full_detail=True))

    @authenticated
    @with_scope_admin
    async def put(self, exploration_id):
        exploration = self._check_exploration_acces(exploration_id)

        # We need at least one of those
        title = self.get_argument("title", None)
        description = self.get_argument("description", None)
        raw_configuration = self.get_argument("configuration", {})

        if not title and not description and not raw_configuration:
            raise ApiHTTPError(400, "Missing mandatory fields")

        configuration = Exploration.parse_and_validate(raw_configuration)
        if configuration is None:
            raise ApiHTTPError(400, "Invalid JSON blob")

        expl = await ExplorationsService.update_and_save_workspace(
            exploration, title=title, description=description, configuration=configuration
        )

        self.write_json(format_exploration(expl))

    @authenticated
    @with_scope_admin
    async def delete(self, exploration_id):
        exploration = self._check_exploration_acces(exploration_id)

        try:
            await ExplorationsService.remove_and_save_workspace(exploration)
            self.write_json({"ok": True})
        except Exception as e:
            raise ApiHTTPError(400, str(e))


class APIPublishExplorationHandler(ExplAPIBase):
    @authenticated
    @with_scope_admin
    async def post(self, exploration_id):
        _ = self._check_exploration_acces(exploration_id)

        try:
            await Explorations.publish(exploration_id)
            self.write_json({"ok": True})
        except Exception as e:
            raise ApiHTTPError(400, str(e))


class APIUnpublishExplorationHandler(ExplAPIBase):
    @authenticated
    @with_scope_admin
    async def post(self, exploration_id):
        _ = self._check_exploration_acces(exploration_id)

        try:
            await Explorations.unpublish(exploration_id)
            self.write_json({"ok": True})
        except Exception as e:
            raise ApiHTTPError(400, str(e))


class APIPublicTimeSeriesHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    async def get(self, exploration_id: str) -> None:
        if not exploration_id:
            raise ApiHTTPError(404, "Not found")
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
        self.write_json({"token": token, "timeseries": format_exploration(exploration, full_detail=True)})


def handlers():
    return [
        url(r"/v0/public-timeseries/(.+)", APIPublicTimeSeriesHandler),
        url(r"/v0/timeseries/(.+)/publish/?", APIPublishExplorationHandler),
        url(r"/v0/timeseries/(.+)/unpublish/?", APIUnpublishExplorationHandler),
        url(r"/v0/timeseries/(.+)", APISingleExplorationHandler),
        url(r"/v0/timeseries/?", APIExplorationsHandler),
    ]
