import dataclasses
from typing import Dict, List, Optional, Sequence

from tinybird_cdk.schema import Column, Schema

from tinybird.ingest.external_datasources.connector import CDKConnector


async def list_resources(conn: CDKConnector, scope: Sequence[str]) -> List[Dict]:
    resources = await conn.list_resources(scope)
    return [dataclasses.asdict(r) for r in resources]


def column_to_dict(col: Column) -> Dict:
    return {
        "path": f"$.{col.name}",
        "present_pct": 1,  # 1 as we don't inspect the data
        "recommended_type": col.ch_type.name,
        "name": col.name,
    }


def schema_to_dict(schema: Schema) -> Dict:
    converted_cols = [column_to_dict(col) for col in schema.columns]
    converted_schema = ", ".join(f"{col.name} {col.ch_type.name} `json:$.{col.name}`" for col in schema.columns)
    return {"columns": converted_cols, "schema": converted_schema}


class ExternalTableDatasource:
    def __init__(self, conn: CDKConnector, fqn: Sequence[str]):
        self._conn = conn
        self._fqn = fqn
        # Cache to avoid repeated schema fetches
        self._schema: Optional[Schema] = None

    async def get_schema(self) -> Dict:
        schema = await self._get_schema()
        return schema_to_dict(schema)

    async def get_sample(self) -> List[Dict]:
        schema = await self._get_schema()
        return await self._conn.get_sample(schema)

    async def get_extraction_query(self) -> str:
        schema = await self._get_schema()
        return await self._conn.get_extraction_query(schema)

    async def _get_schema(self) -> Schema:
        if not self._schema:
            self._schema = await self._conn.get_schema(self._fqn)
        return self._schema
