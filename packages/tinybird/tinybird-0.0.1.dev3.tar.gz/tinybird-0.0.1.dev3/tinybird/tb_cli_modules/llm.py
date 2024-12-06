from typing import List, Optional

from openai import OpenAI
from pydantic import BaseModel

from tinybird.tb_cli_modules.prompts import create_project_prompt


class DataFile(BaseModel):
    name: str
    content: str


class DataProject(BaseModel):
    datasources: List[DataFile]
    pipes: List[DataFile]


class LLM:
    def __init__(self, model: Optional[str] = None, key: Optional[str] = None):
        self.model = model
        self.key = key

    async def create_project(self, prompt: str) -> DataProject:
        client = OpenAI(api_key=self.key)
        completion = client.beta.chat.completions.parse(
            model=self.model,
            messages=[{"role": "system", "content": create_project_prompt}, {"role": "user", "content": prompt}],
            response_format=DataProject,
        )
        return completion.choices[0].message.parsed or DataProject(datasources=[], pipes=[])
