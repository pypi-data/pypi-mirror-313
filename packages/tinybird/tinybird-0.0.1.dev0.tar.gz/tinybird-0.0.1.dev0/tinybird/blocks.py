import datetime
from typing import Any, Dict, List, NamedTuple, Optional


class Block(NamedTuple):
    id: str
    table_name: str
    data: Any
    database_server: str
    database: str
    cluster: Optional[str]
    dialect: Dict[str, Any]
    import_id: Optional[str]
    max_execution_time: int
    csv_columns: List[Any]
    quarantine: bool


def blocks_json(block_log: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        {"block_id": x["block_id"], "status": x["status"], "timestamp": datetime.datetime.timestamp(x["timestamp"])}
        for x in block_log
    ]
