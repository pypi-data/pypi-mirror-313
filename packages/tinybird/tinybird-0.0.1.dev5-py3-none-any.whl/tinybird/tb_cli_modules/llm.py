import asyncio
from datetime import datetime
from typing import Awaitable, Callable, List

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
        self, tb_client: TinyB, datasource_content: str, row_count: int = 20, context: str = ""
    ) -> str:
        async def action_fn():
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": sample_data_sql_prompt.format(
                            current_datetime=datetime.now().isoformat(), row_count=row_count, context=context
                        ),
                    },
                    {"role": "user", "content": datasource_content},
                ],
            )
            return response.choices[0].message.content or ""

        async def checker_fn(sql: str):
            try:
                result = await tb_client.query(f"DESCRIBE ({sql}) FORMAT JSON")
                return len(result.get("data", [])) > 0
            except Exception:
                return False

        return await self._execute(action_fn, checker_fn)
