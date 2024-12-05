import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from .model import RedisModel
from .resource import Resource


class TagValidationException(Exception):
    pass


class TagResourceType:
    DATASOURCE = "datasource"
    PIPE = "pipe"


class Tag(RedisModel):
    __namespace__ = "resource_tag"
    __props__ = ["workspace_id", "name", "resources"]
    __owners__ = {"workspace_id"}

    def __init__(
        self,
        workspace_id: str,
        name: str,
        resources: List[Any],
        **tag_dict: Union[str, Dict[str, Any]],
    ):
        self.workspace_id = workspace_id
        self.name = name
        self.resources = resources
        super().__init__(**tag_dict)


class ResourceTag:
    __valid_resource_types = (
        TagResourceType.PIPE,
        TagResourceType.DATASOURCE,
    )

    def __init__(
        self,
        name: str,
        resources: List[Any],
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = Resource.guid()
        self.name = name
        self.resources = [self.build_resource(r) for r in resources]
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "resources": self.resources,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def to_json(self):
        tag = self.to_dict()
        tag["created_at"] = tag["created_at"].isoformat()
        tag["updated_at"] = tag["updated_at"].isoformat()
        return tag

    @classmethod
    def from_dict(cls, tag: Dict[str, Any]) -> "ResourceTag":
        return ResourceTag(
            name=tag["name"],
            resources=tag["resources"],
            created_at=tag["created_at"],
            updated_at=tag["updated_at"],
        )

    def build_resource(self, resource: Dict[str, Any]):
        resource_id = resource.get("id", None)
        resource_name = resource.get("name", None)
        if not resource_name:
            raise ValueError("Resource name is mandatory")
        resource_type = resource.get("type", None)
        if resource_type not in self.__valid_resource_types:
            raise ValueError(f"Invalid resource type: {resource_type}")

        return {
            "id": resource_id,
            "name": resource_name,
            "type": resource_type,
        }

    @staticmethod
    def validate_name(name: str) -> str:
        """
        Validates the given tag name.

        Examples:

        >>> ResourceTag.validate_name('ValidName123')
        'ValidName123'

        >>> ResourceTag.validate_name('Valid Name With Spaces')
        'Valid Name With Spaces'

        >>> ResourceTag.validate_name('Valid-Name-With-Dashes')
        'Valid-Name-With-Dashes'

        >>> ResourceTag.validate_name('Valid_Name_With_Underscores')
        'Valid_Name_With_Underscores'

        """

        if not name:
            raise TagValidationException("Tag name is required.")

        name = name.strip()

        if len(name) > 100:
            raise TagValidationException("Tag name must be less than 100 characters.")

        # allowed only spaces and alphanumeric
        if not bool(re.fullmatch(r"[A-Za-z0-9 _-]+", name)):
            raise TagValidationException("Tag name must be alphanumeric.")

        return name
