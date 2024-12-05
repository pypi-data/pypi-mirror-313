import asyncio
import functools
import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Dict, List, Optional, Sequence, TypeVar

import google.api_core.exceptions
import google.auth.exceptions
import tinybird_cdk
import tinybird_cdk.errors
from tinybird_cdk.connector import Scope, SQLConnector
from tinybird_cdk.connectors.snowflake import Integration, Role, Warehouse
from tinybird_cdk.schema import Schema

# Initialized to None to avoid messing with the event loop
_CDK_LOCK: Optional[asyncio.Lock] = None
DUMMY_VARS = ["TB_CDK_TOKEN", "TB_CDK_TAG", "TB_CDK_ENDPOINT", "GCS_BUCKET"]
T = TypeVar("T")
SNOWFLAKE_TINYBIRD_INTEGRATION_FORMAT = "tinybird_integration_{role}"


class InvalidGCPCredentials(Exception):
    pass


class UnknownCDKError(Exception):
    pass


async def get_cdk_lock() -> asyncio.Lock:
    # Lazily build and return the cdk lock. Made async to
    # ensure it's run inside a loop
    global _CDK_LOCK
    if not _CDK_LOCK:
        _CDK_LOCK = asyncio.Lock()
    return _CDK_LOCK


def unset_envvar(key: str) -> None:
    try:
        del os.environ[key]
    except KeyError:
        pass  # If the variable already doesn't exist then we're good
    except Exception:  # Catch-all as we don't want to block the lock cleanup
        logging.exception("Failed to unset environment variable '%s'", key)


def _promote_gcp_errors(err: google.api_core.exceptions.ClientError) -> Exception:
    msg = err.errors[0].get("message")
    if isinstance(err, google.api_core.exceptions.NotFound):
        return NameError(msg)
    if isinstance(err, google.api_core.exceptions.Forbidden):
        return PermissionError(msg)
    if isinstance(err, google.api_core.exceptions.BadRequest):
        return ValueError(msg)
    # If something we don't control happens
    return UnknownCDKError("An unexpected error has occurred")


def handle_cdk_errors(func):  # The type support seems to work better without hints :shrug:
    @functools.wraps(func)
    async def inner(*args, **kwargs):
        try:
            # Await here to raise any potential exceptions within the try-catch block
            return await func(*args, **kwargs)
        except google.auth.exceptions.RefreshError as err:
            logging.exception("Invalid GCP Credentials")
            raise InvalidGCPCredentials("GCP Authentication failed") from err
        except google.api_core.exceptions.ClientError as err:
            logging.exception("CDK GCP Error")
            raise _promote_gcp_errors(err) from err

    return inner


class CDKConnector:
    def __init__(self, conn: SQLConnector, kind: str):
        self._conn = conn
        self.kind = kind
        self._namespace_hierarchy = [level.value for level in self._conn.get_scopes()]
        self._pool = ThreadPoolExecutor(1)

    def get_namespace_hierarchy(self) -> List[Scope]:
        return self._conn.get_scopes()

    @handle_cdk_errors
    async def list_resources(self, scope: Sequence[str]) -> List[Scope]:
        if len(scope) >= len(self._namespace_hierarchy):
            errmsg = f"Maximum scope length is {len(self._namespace_hierarchy)-1}, got {len(scope)}"
            raise ValueError(errmsg)
        scope_map = {level: val for level, val in zip(self._namespace_hierarchy, scope)}
        return await self._run_async(self._conn.list_scope, scope_map)

    @handle_cdk_errors
    async def get_schema(self, fqn: Sequence[str]) -> Schema:
        if len(fqn) != len(self._namespace_hierarchy):
            _hierarchy = ".".join(f"<{level}>" for level in self._namespace_hierarchy)
            _fqn = ".".join(str(segment) for segment in fqn)
            errmsg = f"Invalid Fully Qualified Name. Expected '{_hierarchy}', got '{_fqn}'"
            raise ValueError(errmsg)
        scope_map = {level: val for level, val in zip(self._namespace_hierarchy, fqn)}
        return await self._run_async(self._conn.suggest_schema, scope_map)

    @handle_cdk_errors
    async def get_sample(self, schema: Schema) -> List[Dict]:
        return await self._run_async(self._conn.sample, schema, [col.name for col in schema.columns])

    @handle_cdk_errors
    async def get_extraction_query(self, schema: Schema) -> str:
        return await self._run_async(self._conn.ingest_query, schema, [col.name for col in schema.columns])

    @handle_cdk_errors
    async def get_roles(self) -> List[Role]:
        return await self._run_async(self._conn.get_roles)

    @handle_cdk_errors
    async def get_warehouses(self) -> List[Warehouse]:
        return await self._run_async(self._conn.get_warehouses)

    @handle_cdk_errors
    async def create_stage(
        self, allowed_location: str, integration_name: str, stage_name: Optional[str] = None
    ) -> Dict:
        return await self._run_async(self._conn.create_stage, allowed_location, integration_name, stage_name)

    @handle_cdk_errors
    async def get_integrations(self) -> List[Integration]:
        return await self._run_async(self._conn.get_integrations)

    @handle_cdk_errors
    async def get_integration_query(self, allowed_location: str, integration_name: str) -> str:
        return await self._run_async(self._conn.get_integration_query, allowed_location, integration_name)

    def shutdown(self) -> None:
        self._pool.shutdown()

    async def _run_async(self, func: Callable[..., T], *args, **kwargs) -> T:
        loop = asyncio.get_running_loop()
        prepared_func = functools.partial(func, *args, **kwargs)
        return await loop.run_in_executor(self._pool, prepared_func)


# Exception handling done separately for readability
def _get_raw_connector(kind: str) -> SQLConnector:
    try:
        return tinybird_cdk.connector_for(kind)
    except json.decoder.JSONDecodeError as err:
        logging.exception("Invalid GCPCredentials")
        raise InvalidGCPCredentials("Provided account info is not valid JSON") from err
    except ValueError as err:
        logging.exception("Invalid GCPCredentials")
        raise InvalidGCPCredentials(f"GCP Authentication failed: {err.args[0]}") from err
    except tinybird_cdk.errors.UnknownConnectorError as err:
        raise NotImplementedError(err.args[0]) from err


async def get_connector(kind: str, env: Dict[str, str]) -> CDKConnector:
    return await _get_connector(kind, env)


# Hook for patching
async def _get_connector(kind: str, env: Dict[str, str]) -> CDKConnector:
    lock = await get_cdk_lock()
    async with lock:
        os.environ.update({key: "DUMMY" for key in DUMMY_VARS})
        for key, value in env.items():
            os.environ[key] = value if value is not None else ""
        try:
            return CDKConnector(_get_raw_connector(kind), kind)
        finally:
            unset_envvar("GOOGLE_APPLICATION_CREDENTIALS_JSON")
            for key in DUMMY_VARS:
                unset_envvar(key)
