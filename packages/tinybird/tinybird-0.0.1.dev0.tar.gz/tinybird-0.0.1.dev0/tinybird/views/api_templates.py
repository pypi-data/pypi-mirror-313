from dataclasses import dataclass
from typing import Any, Dict, Tuple

from tornado.web import url

from .base import BaseHandler


@dataclass
class Template:
    friendly_name: str
    repository_name: str
    description: str


AVAILABLE_TEMPLATES: Tuple[Template, Template] = (
    Template(
        friendly_name="web-analytics",
        repository_name="web-analytics-starter-kit",
        description="Starting workspace ready to track visits and custom events",
    ),
    Template(
        friendly_name="log-analytics",
        repository_name="log-analytics-starter-kit",
        description="Build your own logging & telemetry solution",
    ),
)


def format_starter_kit(sk: Template) -> Dict[str, Any]:
    return {"friendly_name": sk.friendly_name, "description": sk.description}


class APITemplateHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass

    def get(self):
        self.write_json({"templates": tuple(map(format_starter_kit, AVAILABLE_TEMPLATES))})


def handlers():
    return [
        url(r"/v0/templates/?", APITemplateHandler),
    ]
