# If you are searching for: time-series, timeseries or time series, this is your place...

import datetime
import json
from typing import Any, Dict, Optional, Union

import jsonschema

from tinybird.model import RedisModel, retry_transaction_in_case_of_concurrent_edition_error_async


class ExplorationDoesNotExist(Exception):
    pass


class Exploration(RedisModel):
    __namespace__ = "explorations"
    __props__ = [
        "title",
        "description",
        "configuration",
        "workspace_id",
        "published",
        "metadata",
        "updated_at",
        "semver",
    ]

    __config_schema__ = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "properties": {
            "type": {"type": "string"},
            "lastUpdated": {"type": "string"},
            "origin": {"type": "string"},
            "name": {"type": "string"},
            "columnName": {"type": "string"},
            "visualize": {"type": "string"},
            "where": {"type": "string"},
            "groupBy": {"type": "string"},
            "having": {"type": "string"},
            "visType": {"type": "string"},
            "granularity": {"type": "integer"},
            "lastMinutes": {"type": "integer"},
            "maxDimensions": {"type": "integer"},
            "startDateTime": {"type": "string"},
            "endDateTime": {"type": "string"},
            "realtime": {"type": "integer"},
        },
        "required": [
            "type",
            "lastUpdated",
            "origin",
            "name",
            "columnName",
            "visualize",
            "where",
            "groupBy",
            "having",
            "visType",
            "lastMinutes",
            "maxDimensions",
            "startDateTime",
            "endDateTime",
            "realtime",
        ],
    }

    def __init__(self, **expl_dict: Union[str, Dict[str, Any], bool, None]) -> None:
        self.workspace_id = ""
        self.title = ""
        self.description = ""
        self.configuration: Dict[str, Any] = {}
        self.published = False
        self.metadata: Dict[str, Any] = {"visits": 0, "last_visit": None}
        self.updated_at = None
        self.semver: Optional[str] = None
        super().__init__(**expl_dict)

    def delete(self):
        self._delete(self.id)

    @classmethod
    def parse_and_validate(cls, configuration: str) -> Optional[Dict[str, Any]]:
        """Parses and checks if the passed configuration is valid."""
        try:
            obj = json.loads(configuration)
            jsonschema.validate(obj, cls.__config_schema__)
            return obj
        except Exception:
            return None


class Explorations:
    @staticmethod
    def create(
        workspace_id: str, title: str, description: str, configuration: Dict[str, Any], semver: Optional[str]
    ) -> Exploration:
        """Inits and saves a new Exploration"""
        result = Exploration(
            workspace_id=workspace_id, title=title, description=description, configuration=configuration, semver=semver
        )
        result.save()
        return result

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def update(
        exploration_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        configuration: Optional[Dict[str, Any]] = None,
    ) -> Exploration:
        """Updates and saves an existing Exploration identified by ID"""
        result = None

        with Exploration.transaction(exploration_id) as expl:
            expl.title = title if title else expl.title
            expl.description = description if description is not None else expl.description
            expl.configuration = configuration if configuration else expl.configuration
            expl.updated_at = datetime.datetime.now()
            result = expl

        return result

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def publish(exploration_id: str) -> Exploration:
        """Updates and saves an existing Exploration identified by ID"""
        result = None

        with Exploration.transaction(exploration_id) as expl:
            expl.published = True
            result = expl

        return result

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def unpublish(exploration_id: str) -> Exploration:
        """Updates and saves an existing Exploration identified by ID"""
        result = None

        with Exploration.transaction(exploration_id) as expl:
            expl.published = False
            result = expl

        return result

    @staticmethod
    def get_by_id(id: str) -> Exploration:
        result = Exploration.get_by_id(id)
        if result is None:
            raise ExplorationDoesNotExist("Exploration does not exist")
        return result
