from datetime import datetime
from typing import Any, Dict, Iterable, List

from tinybird.tracker import HookLogEntry


def hook_log_json(hook_log: Iterable[HookLogEntry]) -> List[Dict[str, Any]]:
    return [
        {
            "hook_id": entry.hook_id,
            "name": entry.name,
            "operation": entry.operation,
            "datasource_id": entry.datasource_id,
            "datasource_name": entry.datasource_name,
            "timestamp": datetime.fromtimestamp(entry.timestamp).isoformat(),
            "elapsed": entry.elapsed,
            "status": entry.status,
            "error": entry.error,
        }
        for entry in hook_log
    ]


class HookException(Exception):
    pass
