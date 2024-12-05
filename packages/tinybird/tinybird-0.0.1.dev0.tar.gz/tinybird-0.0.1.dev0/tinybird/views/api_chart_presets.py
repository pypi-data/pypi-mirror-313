from tornado.escape import json_decode
from tornado.web import url

from tinybird.chart import ChartPreset
from tinybird.views.api_errors.pipes import ChartPresetError

from .base import ApiHTTPError, BaseHandler, authenticated, requires_write_access


class APIChartPresetBaseHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass


class APIChartPresetsHandler(APIChartPresetBaseHandler):
    @authenticated
    async def get(self):
        workspace = self.get_workspace_from_db()
        presets = ChartPreset.get_all_by_owner(workspace.id)
        self.write_json({"presets": [p.to_json() for p in presets]})

    @authenticated
    @requires_write_access
    async def post(self):
        workspace = self.get_workspace_from_db()
        data = json_decode(self.request.body) or {}
        name = data.get("name", "")
        styles = data.get("styles", {})
        preset = ChartPreset(workspace_id=workspace.id, name=name, styles=styles)
        preset.save()
        self.write_json(preset.to_json())


class APIChartPresetHandler(APIChartPresetBaseHandler):
    @authenticated
    @requires_write_access
    async def put(self, preset_id):
        data = json_decode(self.request.body) or {}
        preset_props = ChartPreset.__props__
        preset_data = {k: v for k, v in data.items() if k in preset_props}
        preset = ChartPreset.get_by_id(preset_id)

        if not preset:
            raise ApiHTTPError.from_request_error(ChartPresetError.not_found(preset_id=preset_id))

        preset = await ChartPreset.update_preset(preset_id, preset_data)
        self.write_json(preset.to_json())

    @authenticated
    @requires_write_access
    async def delete(self, preset_id):
        preset = ChartPreset.get_by_id(preset_id)

        if not preset:
            raise ApiHTTPError.from_request_error(ChartPresetError.not_found(preset_id=preset_id))

        await ChartPreset.delete(preset_id)
        self.set_status(204)


def handlers():
    return [
        url(r"/v0/chart-presets/(.+)", APIChartPresetHandler),
        url(r"/v0/chart-presets/?", APIChartPresetsHandler),
    ]
