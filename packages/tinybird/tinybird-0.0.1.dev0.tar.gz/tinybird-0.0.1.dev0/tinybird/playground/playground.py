import textwrap
from typing import Any, Dict, List, Optional, Union

from tinybird.model import RedisModel
from tinybird.pipe import PipeNode, TransformationPipeline
from tinybird.resource import Resource


class PlaygroundException(Exception):
    pass


class PlaygroundNotFoundException(Exception):
    pass


class PlaygroundValidationException(Exception):
    pass


PLAYGROUND_EXAMPLE = {
    "name": "playground_name",
    "nodes": [
        {"sql": "select * from datasource_foo limit 1", "name": "node_00"},
        {"sql": "select count() from node_00", "name": "node_01"},
    ],
}


class Playground(RedisModel):
    __namespace__ = "playground"
    __props__ = ["user_id", "workspace_id", "name", "description", "pipeline", "shared_with", "shared_by", "semver"]
    __owners__ = {"user_id", "workspace_id", "semver"}

    def __init__(
        self,
        user_id: str,
        workspace_id: str,
        name: str,
        description: Optional[str] = None,
        nodes: Optional[List[Dict[str, Any]]] = None,
        shared_with: Optional[List[str]] = None,
        shared_by: Optional[List[str]] = None,
        semver: Optional[str] = None,
        **playground_dict: Union[str, Dict[str, Any], bool],
    ) -> None:
        self.user_id = user_id
        self.workspace_id = workspace_id
        self.name = name
        self.description = description
        self.pipeline: TransformationPipeline = TransformationPipeline()
        self.shared_with = shared_with
        self.shared_by = shared_by
        self.semver = semver
        if nodes:
            self.set_nodes(nodes)
        super().__init__(**playground_dict)

    def set_nodes(
        self,
        nodes: List[Dict[str, Any]],
    ) -> None:
        for x in nodes:
            node = PipeNode.from_dict({**x, "ignore_sql_errors": True})
            self.pipeline.append(node)

    def delete(self):
        self._delete(self.id)

    def to_json(self, attrs: Optional[List[str]] = None) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if not attrs or "nodes" in attrs:
            nodes = []
            for n in self.pipeline.nodes:
                n.ignore_sql_errors = True
                nodes.append(n.to_json())
            result["nodes"] = nodes
        attributes = attrs or [
            "id",
            "name",
            "description",
            "created_at",
            "updated_at",
            "shared_with",
            "shared_by",
            "user_id",
        ]
        for attr in attributes:
            try:
                result[attr] = getattr(self, attr)
            except AttributeError:
                pass
        if "created_at" in result:
            result["created_at"] = str(result["created_at"])
        if "updated_at" in result:
            result["updated_at"] = str(result["updated_at"])

        return result

    def generate_datafile(self) -> str:
        doc = []
        if self.description:
            doc.append(f"DESCRIPTION >\n\t{self.description}\n\n")
        for x in self.pipeline.to_dict():
            sql = textwrap.indent(x["sql"], " " * 4)
            node = f"NODE {x['name']}\n"
            if x.get("description", None):
                desc = textwrap.indent(x["description"], " " * 4)
                node += f"DESCRIPTION >\n{desc}\n\n"
            node += f"SQL >\n\n{sql}"
            node += "\n\n\n"
            doc.append(node)
        return "\n".join(doc)

    def is_owner(self, user_id: str) -> bool:
        return self.user_id == user_id

    def is_shared_with(self, user_id: str) -> bool:
        return self.shared_with is not None and user_id in self.shared_with

    def has_access(self, user_id: str) -> bool:
        return self.is_owner(user_id) or self.is_shared_with(user_id)

    @staticmethod
    def validate(playground_obj: Dict[str, Any]) -> None:
        if "name" in playground_obj and not Resource.validate_name(playground_obj["name"]):
            raise PlaygroundValidationException(
                f'Invalid Playground name "{playground_obj["name"]}". {Resource.name_help(playground_obj["name"])}'
            )
        if "nodes" in playground_obj:
            # check nodes have different names
            names = [x.get("name", None) for x in playground_obj["nodes"]]
            if len(set(names)) != len(names):
                raise PlaygroundValidationException(
                    "every node must have a unique name, there are nodes with the same name"
                )


class Playgrounds:
    @staticmethod
    def get_by_workspace(workspace_id: str, semver: Optional[str]) -> List[Playground]:
        playgrounds_by_workspace = Playground.get_all_by_owner(workspace_id)
        return [x for x in playgrounds_by_workspace if x.semver == semver]

    @staticmethod
    def get_playgrounds(workspace_id: str, user_id: str, semver: Optional[str]) -> List[Playground]:
        playgrounds_by_workspace = Playgrounds.get_by_workspace(workspace_id, semver)
        return [
            x
            for x in playgrounds_by_workspace
            if (x.shared_with is not None and user_id in x.shared_with) or x.user_id == user_id
        ]

    @staticmethod
    def get_playground(playground_id: str) -> Optional[Playground]:
        return Playground.get_by_id(playground_id)

    @staticmethod
    def create_playground(
        workspace_id: str,
        user_id: str,
        name: str,
        description: Optional[str],
        nodes: Optional[List[Dict[str, Any]]],
        semver: Optional[str] = None,
    ) -> Playground:
        playground = Playground(
            workspace_id=workspace_id,
            user_id=user_id,
            name=name,
            description=description,
            nodes=nodes,
            semver=semver,
        )
        playground.save()
        return playground

    @staticmethod
    async def delete_playground(playground: Playground) -> None:
        playground.delete()

    @staticmethod
    async def update_playground(playground_id: str, data: Dict[str, Any]) -> Playground:
        result = None
        with Playground.transaction(playground_id) as playground:
            playground.name = data.get("name", playground.name)
            playground.description = data.get("description", playground.description)
            playground.shared_with = data.get("shared_with", playground.shared_with)
            nodes = data.get("nodes", None)
            if nodes is not None:
                updated_nodes = []
                for node in nodes:
                    updated_nodes.append(PipeNode.from_dict(node))
                playground.pipeline.nodes = updated_nodes
            result = playground
        return result

    @staticmethod
    async def share_playground(playground_id: str, user_id: str) -> Playground:
        playground = Playground.get_by_id(playground_id)
        if not playground:
            raise PlaygroundNotFoundException(f"Playground {playground_id} does not exist")

        if playground.shared_with is None:
            playground.shared_with = []
        playground.shared_with.append(user_id)
        playground.save()
        return playground

    @staticmethod
    async def unshare_playground(playground_id: str, user_id: str) -> Playground:
        playground = Playground.get_by_id(playground_id)
        if not playground:
            raise PlaygroundNotFoundException(f"Playground {playground_id} does not exist")

        if playground.shared_with is None:
            playground.shared_with = []
        playground.shared_with.remove(user_id)
        playground.save()
        return playground
