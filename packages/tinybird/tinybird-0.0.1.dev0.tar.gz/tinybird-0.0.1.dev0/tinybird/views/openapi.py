import json
import logging
from collections import Counter
from enum import Enum
from typing import Any, Dict

from tinybird.ch import CHException, HTTPClient, ch_get_columns_from_query, table_structure
from tinybird.token_scope import scopes
from tinybird.user import Users


class OpenAPIExampleTypes(str, Enum):
    SHOW = "show"
    HIDE = "hide"
    FAKE = "fake"


DEFAULT_PARAMS = [
    {
        "name": "format",
        "required": True,
        "in": "path",
        "description": "Response format: `json` or `csv`",
        "schema": {"type": "string", "default": "json", "enum": ["json", "csv"]},
    },
    {
        "name": "q",
        "required": False,
        "in": "query",
        "description": (
            "SQL statement to run a query against the data returned by the endpoint (e.g SELECT count() FROM _)"
        ),
        "schema": {"type": "string"},
    },
]


def openapi_response(settings, paths, token, base_schema):
    info = {
        "version": "1.0.0",
        "title": token.name,
        "termsOfService": f"{settings['host']}/terms",
        "contact": {"email": "support@tinybird.co"},
    }

    return {
        "openapi": "3.0.0",
        "info": info,
        "servers": [{"url": f"{settings['api_host']}/v0"}],
        "externalDocs": {"description": "Tinybird Analytics documentation", "url": f"{settings['docs_host']}"},
        "security": [{"TokenBearerHeader": [token.token]}, {"TokenQueryString": [token.token]}],
        "paths": paths,
        "components": {
            "securitySchemes": {
                "TokenBearerHeader": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                },
                "TokenQueryString": {
                    "type": "apiKey",
                    "in": "query",
                    "name": "token",
                },
            },
            "responses": {
                "BadRequestError": {
                    "description": "Invalid or malformed user input: check your SQL, parameters, and encoding"
                },
                "UnauthorizedError": {"description": "Unauthorized request"},
                "ForbiddenError": {
                    "description": (
                        "Access token is missing or invalid: the request does not have enough permissions to be"
                        " completed"
                    )
                },
                "NotFoundError": {"description": "Resource not found: the data source, pipe, or endpoint is missing"},
                "MethodNotAllowedError": {"description": "The method is not allowed in this resource"},
                "InternalServerError": {
                    "description": (
                        "Server could not fulfill the request due to an internal problem: contact support@tinybird.co"
                    )
                },
            },
            "schemas": base_schema,
        },
    }


def ch_type_to_openapi_type(param_type: str) -> dict:
    nullable = False
    if param_type.startswith("Nullable(") and param_type.endswith(")"):
        nullable = True
        param_type = param_type[9:-1]

    if param_type.startswith("Array(") and param_type.endswith(")"):
        inner_type = ch_type_to_openapi_type(param_type[6:-1])
        return {"type": "array", "items": inner_type}

    if param_type.startswith("Tuple(") and param_type.endswith(")"):
        inner_types = param_type[6:-1].split(", ")
        _inner_types = [ch_type_to_openapi_type(t) for t in inner_types]
        items = _inner_types[0] if len(set(inner_types)) == 1 else {"oneOf": _inner_types}
        return {"type": "array", "items": items, "minItems": len(_inner_types), "maxItems": len(_inner_types)}

    # Map ClickHouse types to OpenAPI types
    openapi_type = {
        "UInt8": {"type": "integer", "format": "uint8"},
        "UInt16": {"type": "integer", "format": "uint16"},
        "UInt32": {"type": "integer", "format": "int32"},
        "UInt64": {"type": "integer", "format": "int64"},
        "UInt128": {"type": "integer", "format": "uint128"},
        "UInt256": {"type": "integer", "format": "uint256"},
        "Int8": {"type": "integer", "format": "int8"},
        "Int16": {"type": "integer", "format": "int16"},
        "Int32": {"type": "integer", "format": "int32"},
        "Int64": {"type": "integer", "format": "int64"},
        "Int128": {"type": "integer", "format": "int128"},
        "Int256": {"type": "integer", "format": "int256"},
        "Float32": {"type": "number", "format": "float"},
        "Float64": {"type": "number", "format": "double"},
        "String": {"type": "string"},
        "LowCardinality(String)": {"type": "string"},
        "Date": {"type": "string", "format": "date"},
        "DateTime": {"type": "string", "format": "date-time"},
        "DateTime64": {"type": "string", "format": "date-time"},
        "UUID": {"type": "string", "format": "uuid"},
        "Boolean": {"type": "boolean"},
    }.get(param_type)

    if openapi_type is None:
        return {"type": "string", "nullable": True} if nullable else {"type": "string"}

    _format = openapi_type.get("format")

    res = {"type": openapi_type["type"], "nullable": True} if nullable else {"type": openapi_type["type"]}
    if _format:
        res["format"] = _format
    return res


def get_param_type(param_type, count):
    if count > 1:
        return {"type": "string"}
    if param_type.startswith("Array"):
        return {"type": "array"}
    return ch_type_to_openapi_type(param_type)


def get_params(pipe):
    """
    >>> from tinybird.pipe import Pipe
    >>> pipe = Pipe('test', [{'name': 'test_0', 'sql': "% SELECT * FROM test_table WHERE a == {{Int8(param1, 1)}}"}])
    >>> n0 = pipe.pipeline.nodes[0]
    >>> pipe.endpoint = n0.id
    >>> parameters, post_parameters = get_params(pipe)
    >>> parameters
    [{'in': 'query', 'name': 'param1', 'description': '', 'required': False, 'example': None, 'schema': {'type': 'integer', 'format': 'int8', 'default': 1}}]
    >>> post_parameters
    {'specification': {'param1': {'type': 'integer', 'format': 'int8', 'default': 1, 'description': ''}}, 'required': []}
    >>> pipe = Pipe('test', [{'name': 'test_1', 'sql': "% SELECT * FROM test_table WHERE c == {{String(param1, 'one')}}"}])
    >>> n0 = pipe.pipeline.nodes[0]
    >>> pipe.endpoint = n0.id
    >>> parameters, post_parameters = get_params(pipe)
    >>> parameters
    [{'in': 'query', 'name': 'param1', 'description': '', 'required': False, 'example': None, 'schema': {'type': 'string', 'default': 'one'}}]
    >>> post_parameters
    {'specification': {'param1': {'type': 'string', 'default': 'one', 'description': ''}}, 'required': []}
    >>> pipe = Pipe('test', [{'name': 'test_0', 'sql': "% SELECT * FROM test_table WHERE a == {{Int8(param1, 1)}} AND b < {{Int8(param1, 1)}}"}])
    >>> n0 = pipe.pipeline.nodes[0]
    >>> pipe.endpoint = n0.id
    >>> parameters, post_parameters = get_params(pipe)
    >>> parameters
    [{'in': 'query', 'name': 'param1', 'description': '', 'required': False, 'example': None, 'schema': {'type': 'integer', 'format': 'int8', 'default': 1}}]
    >>> post_parameters
    {'specification': {'param1': {'type': 'integer', 'format': 'int8', 'default': 1, 'description': ''}}, 'required': []}
    >>> pipe = Pipe('test', [{'name': 'test_0', 'sql': "% SELECT * FROM test_table WHERE a == {{Int8(param1, 1)}} AND b < {{Int8(param1, 2)}}"}])
    >>> n0 = pipe.pipeline.nodes[0]
    >>> pipe.endpoint = n0.id
    >>> paramenters, _ = get_params(pipe)
    >>> parameters[0]['name']
    'param1'
    >>> parameters[0]['schema']['type']
    'integer'
    >>> pipe = Pipe('test', [{'name': 'test_0', 'sql': "% SELECT * FROM test_table WHERE a in {{Array('test')}}"}])
    >>> n0 = pipe.pipeline.nodes[0]
    >>> pipe.endpoint = n0.id
    >>> parameters, post_parameters = get_params(pipe)
    >>> parameters
    [{'in': 'query', 'name': 'test', 'description': '', 'required': False, 'example': None, 'schema': {'type': 'array', 'items': {'type': 'string'}}}]
    >>> post_parameters
    {'specification': {'test': {'type': 'array', 'items': {'type': 'string'}, 'description': ''}}, 'required': []}
    >>> pipe = Pipe('test', [{'name': 'test_0', 'sql': "% SELECT * FROM test_table WHERE now() < {{DateTime(param1, '2019-02-02')}}"}])
    >>> n0 = pipe.pipeline.nodes[0]
    >>> pipe.endpoint = n0.id
    >>> parameters, post_parameters = get_params(pipe)
    >>> parameters
    [{'in': 'query', 'name': 'param1', 'description': '', 'required': False, 'example': None, 'schema': {'type': 'string', 'format': 'date-time', 'default': '2019-02-02'}}]
    >>> post_parameters
    {'specification': {'param1': {'type': 'string', 'format': 'date-time', 'default': '2019-02-02', 'description': ''}}, 'required': []}
    >>> pipe = Pipe('test', [{'name': 'test_0', 'sql': "% SELECT * FROM test_table WHERE a == {{Int8(param1, 1)}} {% if defined(param2) %} AND c IN {{Array(param2)}} {% end %}"}])
    >>> n0 = pipe.pipeline.nodes[0]
    >>> pipe.endpoint = n0.id
    >>> parameters, post_parameters = get_params(pipe)
    >>> parameters
    [{'in': 'query', 'name': 'param1', 'description': '', 'required': False, 'example': None, 'schema': {'type': 'integer', 'format': 'int8', 'default': 1}}, {'in': 'query', 'name': 'param2', 'description': '', 'required': False, 'example': None, 'schema': {'type': 'array', 'items': {'type': 'string'}}}]
    >>> post_parameters
    {'specification': {'param1': {'type': 'integer', 'format': 'int8', 'default': 1, 'description': ''}, 'param2': {'type': 'array', 'items': {'type': 'string'}, 'description': ''}}, 'required': []}
    >>> pipe = Pipe('test', [{'name': 'test_0', 'sql': "% SELECT * FROM test_table WHERE a in {{Array('test', 'Int32')}}"}])
    >>> n0 = pipe.pipeline.nodes[0]
    >>> pipe.endpoint = n0.id
    >>> parameters, post_parameters = get_params(pipe)
    >>> parameters
    [{'in': 'query', 'name': 'test', 'description': '', 'required': False, 'example': None, 'schema': {'type': 'array', 'items': {'type': 'integer', 'format': 'int32'}}}]
    >>> post_parameters
    {'specification': {'test': {'type': 'array', 'items': {'type': 'integer', 'format': 'int32'}, 'description': ''}}, 'required': []}
    >>> pipe = Pipe('test', [{'name': 'test_0', 'sql': "% SELECT * FROM test_table WHERE a in {{Array('test', 'Float32')}}"}])
    >>> n0 = pipe.pipeline.nodes[0]
    >>> pipe.endpoint = n0.id
    >>> parameters, post_parameters = get_params(pipe)
    >>> parameters
    [{'in': 'query', 'name': 'test', 'description': '', 'required': False, 'example': None, 'schema': {'type': 'array', 'items': {'type': 'number', 'format': 'float'}}}]
    >>> post_parameters
    {'specification': {'test': {'type': 'array', 'items': {'type': 'number', 'format': 'float'}, 'description': ''}}, 'required': []}
    >>> pipe = Pipe('test', [{'name': 'test_0', 'sql': "% SELECT * FROM test_table WHERE a = {{Int32('test_a', 2)}} or b in {{Array('test_b', 'Float32', required=True)}}"}])
    >>> n0 = pipe.pipeline.nodes[0]
    >>> pipe.endpoint = n0.id
    >>> parameters, post_parameters = get_params(pipe)
    >>> parameters
    [{'in': 'query', 'name': 'test_b', 'description': '', 'required': True, 'example': None, 'schema': {'type': 'array', 'items': {'type': 'number', 'format': 'float'}}}, {'in': 'query', 'name': 'test_a', 'description': '', 'required': False, 'example': None, 'schema': {'type': 'integer', 'format': 'int32', 'default': 2}}]
    >>> post_parameters
    {'specification': {'test_b': {'type': 'array', 'items': {'type': 'number', 'format': 'float'}, 'description': ''}, 'test_a': {'type': 'integer', 'format': 'int32', 'default': 2, 'description': ''}}, 'required': ['test_b']}
    >>> pipe = Pipe('test', [{'name': 'test_0', 'sql': "% {% if not defined(param1) %}{{ error('param1 (Int8) query param is required') }}{% end %}SELECT * FROM test_table WHERE a == {{Int8(param1, 1)}} AND b < {{Int8(param1, 2)}}"}])
    >>> n0 = pipe.pipeline.nodes[0]
    >>> pipe.endpoint = n0.id
    >>> parameters, post_parameters = get_params(pipe)
    >>> parameters
    [{'in': 'query', 'name': 'param1', 'description': '', 'required': False, 'example': None, 'schema': {'type': 'integer', 'format': 'int8', 'default': 2}}]
    >>> post_parameters
    {'specification': {'param1': {'type': 'integer', 'format': 'int8', 'default': 2, 'description': ''}}, 'required': []}
    >>> pipe = Pipe('test', [{'name': 'test_0', 'sql': "% {% if not defined({{Int8(param1, 0)}}) %}{{ error('param1 (Int8) query param is required') }}{% end %}SELECT * FROM test_table WHERE a == {{Int8(param1, 1)}} AND b < {{Int8(param1, 2)}}"}])
    >>> n0 = pipe.pipeline.nodes[0]
    >>> pipe.endpoint = n0.id
    >>> parameters, post_parameters = get_params(pipe)
    >>> parameters
    [{'in': 'query', 'name': 'param1', 'description': '', 'required': False, 'example': None, 'schema': {'type': 'integer', 'format': 'int8', 'default': 2}}]
    >>> post_parameters
    {'specification': {'param1': {'type': 'integer', 'format': 'int8', 'default': 2, 'description': ''}}, 'required': []}
    >>> pipe = Pipe('test1', [{'name': 'test_0', 'sql': "% {% if not {{defined(Int8(param1, 0))}} %}{{ error('param1 (Int8) query param is required') }}{% end %}SELECT * FROM test_table WHERE a == {{Int8(param1, 1)}} AND b < {{Int8(param1, 2)}}"}])
    >>> n0 = pipe.pipeline.nodes[0]
    >>> pipe.endpoint = n0.id
    >>> parameters, post_parameters = get_params(pipe)
    >>> parameters
    [{'in': 'query', 'name': 'param1', 'description': '', 'required': False, 'example': None, 'schema': {'type': 'integer', 'format': 'int8', 'default': 2}}]
    >>> post_parameters
    {'specification': {'param1': {'type': 'integer', 'format': 'int8', 'default': 2, 'description': ''}}, 'required': []}
    >>> pipe = Pipe('test2', [{'name': 'test_0', 'sql': "% {% if not defined(Array(param1, 'Int8')) %}{{ error('param1 (Int8) query param is required') }}{% end %}SELECT * FROM test_table WHERE a == {{Int8(param1, 1, description='Parameter Description')}} AND b < {{Array(param1, 'Int8')}}"}])
    >>> n0 = pipe.pipeline.nodes[0]
    >>> pipe.endpoint = n0.id
    >>> parameters, post_parameters = get_params(pipe)
    >>> parameters
    [{'in': 'query', 'name': 'param1', 'description': 'Parameter Description', 'required': False, 'example': None, 'schema': {'type': 'array', 'default': 1, 'items': {'type': 'integer', 'format': 'int8'}}}]
    >>> post_parameters
    {'specification': {'param1': {'type': 'array', 'default': 1, 'items': {'type': 'integer', 'format': 'int8'}, 'description': 'Parameter Description'}}, 'required': []}
    >>> pipe = Pipe('test', [{'name': 'test_0', 'sql': "% SELECT * FROM test_table {% if defined(Int8(param1)) %} where 1 {% end %}"}])
    >>> n0 = pipe.pipeline.nodes[0]
    >>> pipe.endpoint = n0.id
    >>> parameters, post_parameters = get_params(pipe)
    >>> parameters
    [{'in': 'query', 'name': 'param1', 'description': '', 'required': False, 'example': None, 'schema': {'type': 'integer', 'format': 'int8'}}]
    >>> post_parameters
    {'specification': {'param1': {'type': 'integer', 'format': 'int8', 'description': ''}}, 'required': []}
    >>> pipe = Pipe('test', [{'name': 'test_0', 'sql': "% SELECT * FROM test_table WHERE salary > {{Int32(min_salary)}} AND salary > {{Int32(min_salary, 10000)}} AND salary <= {{Int32(min_salary, 100, description='salary')}}"}])
    >>> n0 = pipe.pipeline.nodes[0]
    >>> pipe.endpoint = n0.id
    >>> parameters, post_parameters = get_params(pipe)
    >>> parameters
    [{'in': 'query', 'name': 'min_salary', 'description': 'salary', 'required': False, 'example': None, 'schema': {'type': 'integer', 'format': 'int32', 'default': 100}}]
    >>> post_parameters
    {'specification': {'min_salary': {'type': 'integer', 'format': 'int32', 'default': 100, 'description': 'salary'}}, 'required': []}
    """

    params = pipe.get_params()
    # first required, then alphabetically
    params.sort(key=lambda x: (0 if x.get("required", False) else 1, x.get("name", ""), str(x.get("default", ""))))

    params_counter = Counter([param["name"] for param in params])
    openapi_params = []
    request_body_params: Dict[str, Any] = {"specification": {}, "required": []}

    for name, count in params_counter.items():
        param = next(param for param in params if param["name"] == name)

        # Generate OpenAPI query parameter
        openapi_param = {
            "in": "query",
            "name": name,
            "description": param.get("description", ""),
            "required": param.get("required", False),
            "example": param.get("example", None),
            "schema": get_param_type(param["type"], count),
        }

        if _format := param.get("format", None):
            openapi_param["schema"]["format"] = _format

        if _default := param.get("default"):
            openapi_param["schema"]["default"] = _default

        parameter_format_openapi = {"Date": "date", "DateTime": "date-time", "DateTime64": "date-time"}
        if param["type"] in parameter_format_openapi:
            openapi_param["schema"]["format"] = parameter_format_openapi[param["type"]]

        if is_array := param["type"].startswith("Array"):
            item_type = param["type"][6:-1]
            openapi_param["schema"]["items"] = get_param_type(item_type, 1)

        if enum := param.get("enum", None):
            if is_array:
                openapi_param["schema"]["items"]["enum"] = enum
            else:
                openapi_param["schema"]["enum"] = enum

        openapi_params.append(openapi_param)

        # Generate OpenAPI Request Body parameter
        request_body_params["specification"][name] = {
            **openapi_param.get("schema", {}),
            "description": param.get("description", ""),
        }

        if param.get("required"):
            request_body_params["required"].append(name)

    return openapi_params, request_body_params


async def get_fake_examples(pipe, workspace, format="JSON", num_examples=3):
    try:
        database = workspace["database"]
        database_server = workspace["database_server"]

        client = HTTPClient(database_server, database)

        sql = f"SELECT * FROM {pipe.name}"
        query = Users.replace_tables(workspace, sql, pipe=pipe, use_pipe_nodes=True)

        columns = await ch_get_columns_from_query(database_server, database, query)
        schema = table_structure(columns)

        random_data_query = f"SELECT * FROM generateRandom('{schema}', 1, 10, 3) LIMIT {num_examples} FORMAT {format}"

        _, body = await client.query(random_data_query)
        if format == "JSON":
            return json.loads(body)
        else:
            return body.decode()
    except CHException as e:
        logging.warning(str(e))
        return None
    except ValueError as e:
        logging.warning(str(e))
        return None
    except Exception as e:
        logging.exception(f"openapi endpoint failed creating example: {e}")
        return None


async def get_examples(pipe, workspace, format="JSON", num_examples=3):
    try:
        client = HTTPClient(workspace["database_server"], database=workspace["database"])
        sql = f"SELECT * FROM {pipe.name} LIMIT {num_examples} FORMAT {format}"
        query = Users.replace_tables(workspace, sql, pipe=pipe, use_pipe_nodes=True)
        _, body = await client.query(query)
        if format == "JSON":
            response = json.loads(body)
        else:
            response = body.decode()
    except CHException as e:
        logging.warning(str(e))
        return None
    except ValueError as e:
        logging.warning(str(e))
        return None
    except Exception as e:
        logging.exception(f"openapi endpoint failed creating example: {e}")
        return None

    return response


async def get_meta(pipe, workspace, variables=None):
    try:
        client = HTTPClient(workspace["database_server"], database=workspace["database"])
        sql = f"DESCRIBE (SELECT * FROM {pipe.name}) FORMAT JSON"
        query = Users.replace_tables(workspace, sql, pipe=pipe, use_pipe_nodes=True, variables=variables)
        _, body = await client.query(query)

        response = json.loads(body)
    except CHException as e:
        logging.warning(str(e))
        return None
    except ValueError as e:
        logging.warning(str(e))
        return None
    except Exception as e:
        logging.exception(f"openapi endpoint failed creating example: {e}")
        return None

    return [{k: obj[k] for k in ("name", "type")} for obj in response["data"]]


async def generate_openapi_endpoints_response(
    settings, workspace, pipes, token, show_examples=OpenAPIExampleTypes.FAKE, optional_fields=False
):
    paths = {}
    base_schema = get_base_schema()

    is_admin = token.has_scope(scopes.ADMIN) or token.has_scope(scopes.ADMIN_USER)
    resources = token.get_resources_for_scope(scopes.PIPES_READ)

    for pipe in pipes:
        if not is_admin and pipe.id not in resources:
            continue
        if not pipe.endpoint:
            continue

        endpoint_node = pipe.pipeline.get_node(pipe.endpoint)

        if not endpoint_node:
            continue

        parameters, post_parameters = get_params(pipe)
        parameters.extend(DEFAULT_PARAMS)

        if show_examples == OpenAPIExampleTypes.SHOW:
            example_json = await get_examples(pipe, workspace=workspace)
            example_csv = await get_examples(pipe, workspace=workspace, format="CSV")
        elif show_examples == OpenAPIExampleTypes.FAKE:
            example_json = await get_fake_examples(pipe, workspace=workspace)
            if not example_json:
                example_json = await get_examples(pipe, workspace=workspace)
            example_csv = await get_fake_examples(pipe, workspace=workspace, format="CSV")
            if not example_csv:
                example_csv = await get_examples(pipe, workspace=workspace, format="CSV")
        else:
            example_json = {}
            example_csv = {}

        path = f"/pipes/{pipe.name}.{{format}}"
        meta = (example_json or {}).get("meta", [])
        optional_meta = None
        if optional_fields:
            optional_meta = []
            for param in parameters:
                meta_by_param = await get_meta(pipe, workspace, variables={param["name"]: "dummy"})
                if meta_by_param:
                    optional_meta.extend(meta_by_param)
            optional_meta = list({v["name"]: v for v in optional_meta}.values())
        base_schema, path_schema = get_schema(pipe, meta, base_schema, optional_meta=optional_meta)

        pipe_endpoint_definition_base = {
            "tags": ["Pipes"],
            "summary": pipe.name,
            "description": pipe.description or "",
            "parameters": parameters,
            "security": [
                {
                    "TokenBearerHeader": [f"PIPES:READ:{pipe.name}", "ADMIN"],
                },
                {"TokenQueryString": [f"PIPES:READ:{pipe.name}", "ADMIN"]},
            ],
            "responses": {
                "200": {
                    "description": "Endpoint result",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": f"#/components/schemas/{path_schema}"},
                            "example": example_json,
                        },
                        "text/csv": {
                            "schema": {"$ref": "#/components/schemas/ApiQueryCSVResponse"},
                            "example": example_csv,
                        },
                    },
                },
                "400": {
                    "$ref": "#/components/responses/BadRequestError",
                },
                "401": {
                    "$ref": "#/components/responses/UnauthorizedError",
                },
                "403": {
                    "$ref": "#/components/responses/ForbiddenError",
                },
                "404": {
                    "$ref": "#/components/responses/NotFoundError",
                },
                "405": {
                    "$ref": "#/components/responses/MethodNotAllowedError",
                },
                "500": {
                    "$ref": "#/components/responses/InternalServerError",
                },
            },
        }

        request_body_content = {
            "schema": {
                "type": "object",
                "properties": post_parameters.get("specification"),
            }
        }

        required = post_parameters.get("required")
        if len(required) > 0:
            request_body_content["schema"]["required"] = required

        paths[path] = {
            "get": {**pipe_endpoint_definition_base, "operationId": f"{pipe.name}_get", "parameters": parameters},
            "post": {
                **pipe_endpoint_definition_base,
                "operationId": f"{pipe.name}_post",
                "parameters": DEFAULT_PARAMS,
                "requestBody": {
                    "content": {
                        "application/json": request_body_content,
                        "application/x-www-form-urlencoded": request_body_content,
                    },
                },
            },
        }

    return openapi_response(settings, paths, token, base_schema)


def get_base_schema():
    return {
        "ApiQueryJSONResponseMetaItem": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "type": {
                    "type": "string",
                },
            },
        },
        "ApiQueryJSONResponseStatistics": {
            "type": "object",
            "properties": {
                "elapsed": {
                    "type": "number",
                },
                "rows_read": {
                    "type": "number",
                },
                "bytes_read": {
                    "type": "number",
                },
            },
        },
        "ApiQueryJSONResponseDataItem": {"type": "object", "additionalProperties": {"type": "string"}},
        "ApiQueryJSONResponse": {
            "type": "object",
            "properties": {
                "meta": {"type": "array", "items": {"$ref": "#/components/schemas/ApiQueryJSONResponseMetaItem"}},
                "data": {"type": "array", "items": {"$ref": "#/components/schemas/ApiQueryJSONResponseDataItem"}},
                "rows": {
                    "type": "number",
                },
                "rows_before_limit_at_least": {
                    "type": "number",
                },
                "statistics": {
                    "$ref": "#/components/schemas/ApiQueryJSONResponseStatistics",
                },
            },
            "required": ["meta", "data", "rows", "statistics"],
        },
        "ApiQueryCSVResponse": {"type": "string", "format": "csv"},
    }


def get_schema(pipe, meta, base_schema, optional_meta=None):
    def get_json_response(meta):
        if meta:
            props = {}
            for elem in meta:
                props[elem["name"]] = ch_type_to_openapi_type(elem["type"])
            return {"type": "object", "properties": props}

    props = get_json_response(meta)
    path_schema = "ApiQueryJSONResponseDataItem"
    if props:
        path_schema = f"ApiQueryJSONResponse__{pipe.name}"
        base_schema[f"ApiQueryJSONResponseDataItem__{pipe.name}"] = props
        base_schema[path_schema] = {
            "type": "object",
            "properties": {
                "meta": {"type": "array", "items": {"$ref": "#/components/schemas/ApiQueryJSONResponseMetaItem"}},
                "data": {
                    "type": "array",
                    "items": {"$ref": f"#/components/schemas/ApiQueryJSONResponseDataItem__{pipe.name}"},
                },
                "rows": {
                    "type": "number",
                },
                "rows_before_limit_at_least": {
                    "type": "number",
                },
                "statistics": {
                    "$ref": "#/components/schemas/ApiQueryJSONResponseStatistics",
                },
            },
            "required": ["meta", "data", "rows", "statistics"],
        }
        if optional_meta:
            optional_props = get_json_response(optional_meta)
            optional_path_schema = f"ApiQueryJSONOptionalResponse_{pipe.name}"
            base_schema[f"ApiQueryJSONOptionalResponseDataItem__{pipe.name}"] = optional_props
            base_schema[optional_path_schema] = {
                "type": "object",
                "properties": {
                    "meta": {"type": "array", "items": {"$ref": "#/components/schemas/ApiQueryJSONResponseMetaItem"}},
                    "data": {
                        "type": "array",
                        "items": {"$ref": f"#/components/schemas/ApiQueryJSONOptionalResponseDataItem__{pipe.name}"},
                    },
                    "rows": {
                        "type": "number",
                    },
                    "rows_before_limit_at_least": {
                        "type": "number",
                    },
                    "statistics": {
                        "$ref": "#/components/schemas/ApiQueryJSONResponseStatistics",
                    },
                },
                "required": ["meta", "data", "rows", "statistics"],
            }

    return base_schema, path_schema
