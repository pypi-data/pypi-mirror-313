import ipaddress
import logging
import socket
from asyncio.exceptions import TimeoutError
from typing import Any, Dict, FrozenSet, List, Optional, Tuple
from urllib.parse import urlparse

import orjson
from aiohttp import ServerTimeoutError
from aiohttp.client_exceptions import ClientConnectorError, ClientResponseError, ServerDisconnectedError
from tornado.httputil import HTTPServerRequest
from yarl import URL

from tinybird.ch import extract_host
from tinybird.user import User as Workspace
from tinybird.views.aiohttp_shared_session import get_shared_session

from .api_errors.datasources import ClientErrorBadRequest
from .base import ApiHTTPError

SQL_API_PARAMS = (
    "q",
    "token",
    "from",
    "max_threads",
    "pipeline",
    "tag",
    "output_format_json_quote_64bit_integers",
    "output_format_parquet_string_as_string",
    "output_format_json_quote_denormals",
    "semver",
    "playground",
    "finalize_aggregations",
    "release_replacements",
    "time",
    "test",
    "__tb__semver",
)


DEFAULT_API_PARAMS = "token"


def split_ndjson(data: bytes) -> List[bytes]:
    lines = data.split(b"\n")
    # last json might be incomplete
    if not is_valid_json(lines[-1]):
        lines = lines[:-1]
    return lines


def is_valid_json(data: bytes, raise_errors: bool = False):
    """
    >>> is_valid_json(b'1')
    False
    >>> is_valid_json(b'1\\n')
    False
    >>> is_valid_json(b'1', raise_errors=True)
    Traceback (most recent call last):
    ...
    Exception: not a valid JSON
    >>> is_valid_json(b'')
    False
    >>> is_valid_json(b'  ')
    False
    >>> is_valid_json(b'1.5')
    False
    >>> is_valid_json(b'string')
    False
    >>> is_valid_json(b'{}')
    True
    >>> is_valid_json(b'{ }')
    True
    >>> is_valid_json(b'{"a"}')
    False
    >>> is_valid_json(b"{'a'}")
    False
    >>> is_valid_json(b"{'a': 1}")
    False
    >>> is_valid_json(b"{'a': 1}", raise_errors=True)
    Traceback (most recent call last):
    ...
    orjson.JSONDecodeError: unexpected character: line 1 column 2 (char 1)
    >>> is_valid_json(b'{"a": 1}')
    True
    >>> is_valid_json(b'{\"a\": 1}')
    True
    >>> is_valid_json(b'{"foo":[5,6.8],"foo":"bar"}')
    True
    """
    try:
        root_obj = type(orjson.loads(data))
        is_json = root_obj is dict or root_obj is list
        if raise_errors and not is_json:
            raise Exception("not a valid JSON")
        return is_json
    except Exception as e:
        if raise_errors:
            raise e
        return False


def is_host_in_networks(
    url: str,
    networks: Optional[Tuple[str, ...]],
    local_networks: bool,
    whitelist_local_networks: Optional[List[str]] = None,
) -> bool:
    p = urlparse(url)
    for addr in socket.getaddrinfo(p.hostname, p.port):
        ip = ipaddress.ip_address(addr[4][0])
        if local_networks and ip.is_private:
            return (
                not any(ip in ipaddress.ip_network(cidr, strict=False) for cidr in whitelist_local_networks)
                if whitelist_local_networks
                else True
            )
        if networks:
            for ip_range in networks:
                network = ipaddress.ip_network(ip_range)
                if ip in network:
                    return True
    return False


async def is_redirected_host_in_networks(url: str, networks: Optional[Tuple[str, ...]], local_networks: bool):
    async with get_shared_session().head(url=url, allow_redirects=True) as resp:
        # yarl's URL does not encode ",", "'", "(" or ")", while urllib does. So, we need to compare
        # yarl vs yarl to check whether the URL is the same. Apart from that, we need to return
        # exactly the same URL provided in case there's no redirection because some tests check
        # that the URL provided is exactly the same returned.
        real_url = str(resp.real_url)
        same_url = False
        if real_url == str(URL(url)):
            same_url = True
        if is_host_in_networks(real_url, networks, local_networks):
            raise Exception(f"Redirected URL {real_url} coming from {url} is in the deny list of networks")
        if same_url:
            return url
        return real_url


async def validate_redirects_and_internal_ip(url: str, settings: Dict[str, Any], add_protocol: bool = False) -> str:
    deny_networks: Optional[Tuple[str, ...]] = settings.get("deny_networks", None)
    deny_local_networks: bool = settings.get("deny_local_networks", False)

    if add_protocol and "://" not in url:
        url = "http://" + url

    try:
        # Avoid making a network call if the URL already doesn't satisfy the requirements
        if is_host_in_networks(url, deny_networks, deny_local_networks):
            raise Exception(f"URL {url} is in the deny list of networks")
        url = await is_redirected_host_in_networks(url, deny_networks, deny_local_networks)
        return url
    except (ServerTimeoutError, TimeoutError, ServerDisconnectedError, ClientConnectorError, ClientResponseError):
        # Return the original URL as it is. This is not a security concern because we're not
        # following redirects in the following GET requests anyway.
        return url
    except Exception as e:
        logging.warning(f"Exception in validate_redirects_and_internal_ip: {e}")
        raise ApiHTTPError.from_request_error(ClientErrorBadRequest.invalid_url())


KB = 1024
MAX_QUERY_SIZE_IN_KB = 8
MAX_QUERY_SIZE_IN_BYTES = MAX_QUERY_SIZE_IN_KB * KB


def validate_sql_parameter(q: str) -> None:
    """
    >>> validate_sql_parameter("c"*7*1024)

    >>> validate_sql_parameter("c"*10*1024)
    Traceback (most recent call last):
    ...
    tinybird.views.base.ApiHTTPError: HTTP 400: Bad Request (The maximum size for a SQL query is 8KB.)
    """
    if len(q.encode("utf-8")) > MAX_QUERY_SIZE_IN_BYTES:
        raise ApiHTTPError(400, f"The maximum size for a SQL query is {MAX_QUERY_SIZE_IN_KB}KB.")


def filter_query_variables(query_variables: Dict[str, str], filter_sql_params: bool) -> Dict[str, str]:
    params_to_filter = SQL_API_PARAMS if filter_sql_params else DEFAULT_API_PARAMS
    return {k: v for k, v in query_variables.items() if k not in params_to_filter}


def get_variables_for_query(
    request: HTTPServerRequest, from_param: Optional[str] = None, filter_sql_params: bool = True
) -> Tuple[Optional[str], Optional[Dict[str, str]]]:
    try:
        query_variables = {k: v[0].decode() for k, v in request.arguments.items()}
        request_body = request.body.decode()
        query = None

        # FIXME check request headers
        if request_body:
            try:
                body = orjson.loads(request_body)
                query_variables.update(body)
            except Exception:
                query = request_body
                pass

        query = query_variables.get("q", query)
        query_variables = filter_query_variables(query_variables, filter_sql_params)

        variables = None if query_variables == {} and from_param == "ui" else query_variables
        return query, variables
    except UnicodeDecodeError:
        raise ApiHTTPError.from_request_error(ClientErrorBadRequest.invalid_encoding())


async def validate_table_function_host(sql: str, app_settings: Dict[str, Any], ch_params: Optional[Dict[str, str]]):
    new_sql = sql
    # this is to validate the host in case it's behind a secret
    if ch_params:
        for k, v in ch_params.items():
            new_sql = new_sql.replace(f"{{{k.split('param_')[-1]}:String}}", f"'{v}'")

    host = extract_host(new_sql)
    if host is None:
        logging.warning(f"Cannot extract host from {sql}")
        return
    await validate_redirects_and_internal_ip(host, app_settings, add_protocol=True)


def is_table_function_in_error(
    workspace: Workspace, e: Exception, function_allow_list: Optional[FrozenSet[str]] = None
) -> bool:
    table_fns_in_error = [fn for fn in workspace.allowed_table_functions() if fn in str(e)]
    table_fns_in_function_allow_list = (
        [fn for fn in table_fns_in_error if fn in function_allow_list] if function_allow_list else None
    )
    return (
        any(table_fns_in_error) and any(table_fns_in_function_allow_list) if table_fns_in_function_allow_list else True
    )


async def validate_kafka_host(host: str, settings: Dict[str, Any]):
    deny_networks: Optional[Tuple[str, ...]] = settings.get("deny_networks", None)
    deny_local_networks: bool = settings.get("deny_local_networks", False)
    whitelist_local_networks: Optional[List[str]] = settings.get("whitelist_local_networks", None)

    try:
        # http used just for urlparse inside
        in_deny_network = is_host_in_networks(
            f"http://{host}", deny_networks, deny_local_networks, whitelist_local_networks
        )
    except socket.gaierror:
        raise Exception(f"Host '{host}' can't be resolved")
    except Exception as e:
        logging.exception(f"Exception in validate_kafka_host: {e}")
        raise Exception(f"Unexpected error validating Host '{host}'")
    else:
        if in_deny_network:
            raise Exception(f"Host '{host}' is in the deny list of networks")
