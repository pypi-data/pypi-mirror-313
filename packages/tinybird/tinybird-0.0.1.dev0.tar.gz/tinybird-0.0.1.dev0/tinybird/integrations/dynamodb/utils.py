import re
from typing import Any

PREDEFINED_DDB_JSONPATHS = ["$.eventName", "$.ApproximateCreationDateTime", "$.NewImage", "$.OldImage", "$._is_deleted"]


def add_item_prefix_to_jsonpath(jsonschema_definition: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for json_schema in jsonschema_definition:
        attribute_jsonpath = json_schema.get("jsonpath", "")

        if attribute_jsonpath.startswith("$.Item."):
            continue

        if attribute_jsonpath not in PREDEFINED_DDB_JSONPATHS:
            attribute_jsonpath_with_item = re.sub(r"\$\.([\w\[\]_-]+)", r"$.Item.\1", attribute_jsonpath)
            json_schema.update({"jsonpath": attribute_jsonpath_with_item})

    return jsonschema_definition
