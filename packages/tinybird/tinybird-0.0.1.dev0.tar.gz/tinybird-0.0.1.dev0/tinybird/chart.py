from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from .model import RedisModel, retry_transaction_in_case_of_concurrent_edition_error_async
from .resource import Resource


class Chart(RedisModel):
    __namespace__ = "chart"
    __props__ = [
        "pipe_id",
        "name",
        "type",
        "index",
        "categories",
        "description",
        "styles",
        "show_name",
        "show_legend",
        "group_by",
    ]
    __owners__ = {"pipe_id"}

    def __init__(
        self,
        pipe_id: str,
        name: str,
        type: str,
        index: int,
        categories: List[str],
        description: Optional[str] = "",
        styles: Optional[Dict[str, Any]] = None,
        show_name: Optional[bool] = True,
        show_legend: Optional[bool] = True,
        group_by: Optional[str] = None,
        **chart_dict: Union[str, Dict[str, Any], bool],
    ) -> None:
        self.id = Resource.guid()
        self.pipe_id = pipe_id
        self.name = name
        self.type = type
        self.index = index
        self.categories = categories
        self.description = description
        self.styles = styles
        self.show_name = show_name
        self.show_legend = show_legend
        self.group_by = group_by
        super().__init__(**chart_dict)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "index": self.index,
            "categories": self.categories,
            "group_by": self.group_by,
            "description": self.description,
            "styles": self.styles or {},
            "show_name": self.show_name,
            "show_legend": self.show_legend,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def update_name(chart_id: str, new_name: str) -> "Chart":
        with Chart.transaction(chart_id) as chart:
            chart.name = new_name
            chart.updated_at = datetime.now()
            return chart

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def update_chart(chart_id: str, data: Dict[str, Any]) -> "Chart":
        with Chart.transaction(chart_id) as chart:
            for key, value in data.items():
                setattr(chart, key, value)
            chart.updated_at = datetime.now()
            return chart

    @staticmethod
    async def delete(chart_id: str) -> None:
        Chart._delete(chart_id)


class ChartPreset(RedisModel):
    __namespace__ = "chart_preset"
    __props__ = ["workspace_id", "name", "styles"]
    __owners__ = {"workspace_id"}

    def __init__(
        self,
        workspace_id: str,
        name: str,
        styles: Dict[str, Any],
        **chart_preset_dict: Union[str, Dict[str, Any]],
    ) -> None:
        self.id = Resource.guid()
        self.workspace_id = workspace_id
        self.name = name
        self.styles = styles or {}
        super().__init__(**chart_preset_dict)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "styles": self.styles or {},
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }

    @staticmethod
    @retry_transaction_in_case_of_concurrent_edition_error_async()
    async def update_preset(preset_id: str, data: Dict[str, Any]) -> "ChartPreset":
        with ChartPreset.transaction(preset_id) as preset:
            for key, value in data.items():
                setattr(preset, key, value)
            preset.updated_at = datetime.now()
            return preset

    @staticmethod
    async def delete(preset_id: str) -> None:
        ChartPreset._delete(preset_id)
