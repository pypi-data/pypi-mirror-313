from typing import Any, Dict, List, Optional

from tornado.web import url

from tinybird.regions_service import Region, RegionsService

from .base import ApiHTTPError, BaseHandler


class APIAllRegionsHandler(BaseHandler):
    async def get(self):
        regions: List[Region] = []
        regions = RegionsService.get_regions()
        self.write({"regions": regions})


class APIRegionResolverHandler(BaseHandler):
    async def get(self, region_id: str):
        region: Optional[Dict[str, Any]] = RegionsService.get_region_by_id(region_id)
        if not region:
            raise ApiHTTPError(404, "Not found")

        self.write({"region": region})


def handlers():
    return [
        url(r"/v0/regions/?", APIAllRegionsHandler),
        url(r"/v0/region/(.+)/?", APIRegionResolverHandler),
    ]
