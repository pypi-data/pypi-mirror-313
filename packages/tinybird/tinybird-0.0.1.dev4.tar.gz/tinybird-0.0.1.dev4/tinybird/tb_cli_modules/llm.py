import asyncio
import json
from typing import Any, Awaitable, Callable, Dict, List

from openai import OpenAI
from pydantic import BaseModel

from tinybird.client import TinyB
from tinybird.tb_cli_modules.prompts import create_project_prompt, sample_data_sql_prompt


class DataFile(BaseModel):
    name: str
    content: str


class DataProject(BaseModel):
    datasources: List[DataFile]
    pipes: List[DataFile]


class LLM:
    def __init__(self, key: str):
        self.client = OpenAI(api_key=key)

    async def _execute(self, action_fn: Callable[[], Awaitable[str]], checker_fn: Callable[[str], bool]):
        is_valid = False
        times = 0

        while not is_valid and times < 5:
            result = await action_fn()
            if asyncio.iscoroutinefunction(checker_fn):
                is_valid = await checker_fn(result)
            else:
                is_valid = checker_fn(result)
            times += 1

        return result

    async def create_project(self, prompt: str) -> DataProject:
        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": create_project_prompt}, {"role": "user", "content": prompt}],
            response_format=DataProject,
        )
        return completion.choices[0].message.parsed or DataProject(datasources=[], pipes=[])

    async def generate_sql_sample_data(
        self, tb_client: TinyB, datasource_name: str, datasource_content: str, row_count: int = 20
    ) -> str:
        async def action_fn():
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": sample_data_sql_prompt.format(row_count=row_count)},
                    {"role": "user", "content": datasource_content},
                ],
            )

            sql = response.choices[0].message.content or ""
            result = await tb_client.query(f"{sql} FORMAT JSON")
            return result.get("data", [])

        async def checker_fn(sample_data: List[Dict[str, Any]]):
            ndjson_data = "\n".join([json.dumps(row) for row in sample_data])
            try:
                result = await tb_client.datasource_events(datasource_name, ndjson_data)
                return result.get("successful_rows", 0) > 0
            except Exception:
                return False

        return await self._execute(action_fn, checker_fn)
