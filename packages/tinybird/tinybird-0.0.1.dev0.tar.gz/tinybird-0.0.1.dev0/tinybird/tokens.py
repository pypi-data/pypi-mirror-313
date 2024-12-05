"""
this is a JWT token based system

jwt library is used but we are not using fully funcionallity just a few interesting parts
"""

import json
import logging
import typing
import uuid
from collections import deque
from typing import Any, Dict, List, Optional, Tuple, Union

import jwt
from jwt.exceptions import DecodeError, InvalidSignatureError

from tinybird.token_origin import Origins, TokenOrigin
from tinybird.token_scope import ScopeException, scope_codes, scope_names, scope_prefixes, scopes

if typing.TYPE_CHECKING:
    from tinybird.user import User


class key_type:
    PUBLIC = "p"

    # TODO: Review if we need are still using this typee
    PRIVATE = "s"


class ResourcePrefix:
    ORGANIZATION = "o"
    USER_OR_WORKSPACE = "u"

    # For jwt tokens, we use the workspace_id as the resource id
    JWT = "workspace_id"


class AccessToken:
    """
    >>> at = AccessToken('a', "name", 'b', resource_prefix=ResourcePrefix.ORGANIZATION)
    >>> at.to_dict()['token'] != ''
    True
    >>> at = AccessToken('a', "name", 'b', resource_prefix=ResourcePrefix.USER_OR_WORKSPACE)
    >>> at.to_dict()['token'] != ''
    True
    >>> at = AccessToken('a', "name", 'b', resource_prefix='x')  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    AssertionError: Valid resource types are u and o
    >>> at = AccessToken('a', "name", 'b')
    >>> at.add_scope(scopes.DATASOURCES_READ, 'table1')
    >>> at.to_dict()['token'] != ''
    True
    >>> at.to_dict()['scopes']
    [{'type': 'DATASOURCES:READ', 'resource': 'table1', 'filter': ''}]
    >>> at.add_scope(scopes.DATASOURCES_READ, 'table2')
    >>> at.add_scope(scopes.DATASOURCES_READ, 'table2')
    >>> at.scopes
    [('DR', 'table1', None), ('DR', 'table2', None)]
    >>> at.remove_scope('DR', 'table1')
    >>> at.scopes
    [('DR', 'table2', None)]
    >>> at.get_resources_for_scope(scopes.DATASOURCES_READ)
    ['table2']
    >>> at.get_resources_for_scope(scopes.DATASOURCES_APPEND)
    []
    >>> t = AccessToken('a', "name", 'b')
    >>> t.add_scope(scopes.DATASOURCES_READ, 'd1')
    >>> t.add_scope(scopes.DATASOURCES_APPEND, 'd2')
    >>> t.add_scope(scopes.PIPES_READ, 'p1')
    >>> t.get_resources_for_scope(scopes.DATASOURCES_READ)
    ['d1']
    >>> t.get_resources_for_scope(scopes.DATASOURCES_APPEND)
    ['d2']
    >>> t.get_resources_for_scope(scopes.DATASOURCES_READ, scopes.PIPES_READ)
    ['d1', 'p1']
    >>> AccessToken('a', "name", 'b').token != AccessToken('a', "name", 'b').token
    True
    >>> t = AccessToken('s', 'resources_are_mandatory', 'b')
    >>> t.add_scope(scopes.DATASOURCES_CREATE)
    >>> t.add_scope(scopes.DATASOURCES_READ, 'd1')
    >>> t.add_scope(scopes.DATASOURCES_APPEND, 'd1')
    >>> t.add_scope(scopes.DATASOURCES_DROP, 'd1')
    >>> t.add_scope(scopes.PIPES_CREATE)
    >>> t.add_scope(scopes.PIPES_READ, 'p1')
    >>> t.add_scope(scopes.PIPES_DROP, 'p1')
    >>> t.add_scope(scopes.DATASOURCES_DROP)
    Traceback (most recent call last):
    ...
    tinybird.token_scope.ScopeException: scope 'DATASOURCES:DROP' requires a resource
    >>> t.add_scope(scopes.PIPES_DROP)
    Traceback (most recent call last):
    ...
    tinybird.token_scope.ScopeException: scope 'PIPES:DROP' requires a resource
    >>> AccessToken('ss', 'resorces_mandatory_from_ctor', 'b', [(scopes.DATASOURCES_DROP)])
    Traceback (most recent call last):
    ...
    tinybird.token_scope.ScopeException: scope 'DATASOURCES:DROP' requires a resource
    >>> AccessToken('ss', 'resorces_mandatory_from_ctor', 'b', [(scopes.PIPES_DROP)])
    Traceback (most recent call last):
    ...
    tinybird.token_scope.ScopeException: scope 'PIPES:DROP' requires a resource
    """

    _defaults: Dict[str, Any] = {}

    def __init__(
        self,
        resource_id: str,
        name: str,
        secret: str,
        scopes: Optional[List[Any]] = None,
        origin: Optional[TokenOrigin] = None,
        description: Optional[str] = None,
        resource_prefix: str = ResourcePrefix.USER_OR_WORKSPACE,
        host: Optional[str] = None,
    ) -> None:
        assert (
            resource_prefix
            in (
                ResourcePrefix.USER_OR_WORKSPACE,
                ResourcePrefix.ORGANIZATION,
                ResourcePrefix.JWT,
            )
        ), f"Valid resource types are {ResourcePrefix.USER_OR_WORKSPACE}, {ResourcePrefix.ORGANIZATION} and {ResourcePrefix.JWT}"

        # Note there's not id initialization here. It will be generated in the call
        # to refresh()

        self.resource_prefix = resource_prefix
        self.user_id = resource_id  # Legacy property. Use AccessToken::resource_id instead
        self.resource_id = resource_id
        self.host = host or AccessToken._defaults.get("host")
        self.scopes: List[Any] = []
        self.name = name
        if scopes:
            for s in scopes:
                self.add_scope(s)
        self.refresh(secret, resource_id, resource_prefix)
        assert self.id  # Just to be on the safe side
        self.origin = origin or TokenOrigin(Origins.CUSTOM)
        self.description = description or ""
        self._is_obfuscated = False

    def __getattribute__(self, name: str) -> Any:
        # Some properties were added later to the class. As we don't want to launch a migration
        # on the User model, we use __getattribute__ to control the defaults here.

        # AccessToken::origin
        if name == "origin" and "origin" not in self.__dict__:
            self.origin = TokenOrigin(Origins.LEGACY)
            return self.origin

        # AccessToken::description
        if name == "description" and "description" not in self.__dict__:
            self.description = ""
            return ""

        # AccessToken::resource_prefix
        elif name == "resource_prefix" and "resource_prefix" not in self.__dict__:
            self.resource_prefix = ResourcePrefix.USER_OR_WORKSPACE
            return self.resource_prefix

        # AccessToken::resource_id --> Resource associated with this token (previously was AccessToken::user_id)
        elif name == "resource_id" and "resource_id" not in self.__dict__:
            return self.user_id

        # AccessToken::host
        elif name == "host" and "host" not in self.__dict__:
            self.host = AccessToken._defaults.get("host")
            return self.host

        return super().__getattribute__(name)

    def __repr__(self) -> str:
        return f"token: {self.name}"

    def __eq__(self, other: Union["AccessToken", Any]) -> bool:
        return other is not None and isinstance(self, type(other)) and (self.name == other.name)

    @classmethod
    def init_defaults(cls, settings: Dict[str, Any]) -> None:
        region_id: Optional[str] = settings.get("tb_region")
        cls._defaults["host"] = region_id

    @staticmethod
    def parse(s: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        >>> AccessToken.parse("DATASOURCES:READ:test")
        ('DR', 'test', None)
        >>> AccessToken.parse("TOKENS")
        ('TK', None, None)
        >>> AccessToken.parse("NONVALID")
        (None, None, None)
        >>> AccessToken.parse("DATASOURCES:READ:test:columna > 1 and columnb == 2")
        ('DR', 'test', 'columna > 1 and columnb == 2')
        >>> AccessToken.parse("DATASOURCES:READ:test:columna > 'foo:bar'")
        ('DR', 'test', "columna > 'foo:bar'")
        >>> AccessToken.parse("PIPES:READ:test_pipe")
        ('PR', 'test_pipe', None)
        >>> AccessToken.parse("READ:test_pipe")  # Invalid token, previously valid
        (None, None, None)
        >>> AccessToken.parse("DATASOURCES:CREATE")
        ('DC', None, None)
        >>> AccessToken.parse("PIPES:CREATE")
        ('PC', None, None)
        >>> AccessToken.parse("ADMIN_USER:test")
        ('ADMU', 'test', None)
        """
        args = deque(s.split(":"))

        # Scope
        prefix = args.popleft()
        scope = f"{prefix}:{args.popleft()}" if prefix in scope_prefixes else prefix

        # Check before continuing
        code = scope_codes.get(scope, None)
        if code is None:
            return (None, None, None)

        # Resource
        resource = args.popleft() if len(args) else None

        # Filter (rest of the input, if any)
        # TODO check SQL
        _filter = ":".join(args) if len(args) else None

        return code, resource, _filter

    @property
    def visible_token(self) -> str:
        """This is what we must use to show tokens to the outside world"""
        if getattr(self, "_is_obfuscated", False):
            return "*" * len(self.token)
        return self.token

    def is_obfuscated(self) -> bool:
        return getattr(self, "_is_obfuscated", False)

    def obfuscate(self):
        setattr(self, "_is_obfuscated", True)  # noqa: B010

    def add_scope(self, scope: str, resource: Optional[str] = None, filters: Optional[str | Dict[str, Any]] = None):
        try:
            if filters:
                self.scopes.index((scope, resource, filters))
            else:
                try:
                    self.scopes.index((scope, resource))
                except ValueError:
                    self.scopes.index((scope, resource, None))
        except ValueError:
            # validate
            if not scopes.can_have_filter(scope) and filters is not None:
                raise ScopeException("filters can't only be applied to READ scope")
            if scopes.is_resource_mandatory(scope) and not resource:
                raise ScopeException(f"scope '{scope_names.get(scope)}' requires a resource")
            self.scopes.append((scope, resource, filters))

    def clean_scopes(self):
        self.scopes = []

    def remove_scope(self, scope, args):
        self.scopes = [x for x in self.scopes if x[0] != scope or x[1] != args]

    def remove_scope_with_resource(self, resource):
        """
        >>> at = AccessToken('a', "name", 'b')
        >>> at.add_scope(scopes.DATASOURCES_READ, 'table1')
        >>> at.add_scope(scopes.DATASOURCES_READ, 'table2')
        >>> at.add_scope(scopes.DATASOURCES_APPEND, 'table2')
        >>> at.remove_scope_with_resource('table2')
        >>> at.get_resources()
        ['table1']
        """
        self.scopes = [x for x in self.scopes if resource != x[1]]

    def has_scope(self, scope: str) -> bool:
        return any(x[0] == scope for x in self.scopes)

    def get_resources(self):
        """
        >>> at = AccessToken('a', "name", 'b')
        >>> at.add_scope(scopes.DATASOURCES_READ, 'table1')
        >>> at.add_scope(scopes.DATASOURCES_READ, 'table2')
        >>> at.add_scope(scopes.ADMIN)
        >>> 'table1' in at.get_resources()
        True
        >>> 'table2' in at.get_resources()
        True
        """
        resources = []
        for x in self.scopes:
            if len(x) > 1:
                resources.append(x[1])
        return list(set(filter(None, resources)))

    def get_resources_for_scope(self, *scopes: str) -> List[str]:
        """
        >>> at = AccessToken('a', "name", 'b')
        >>> at.add_scope(scopes.ADMIN_USER, 'user_id_1')
        >>> at.add_scope(scopes.ADMIN, 'user_id_2')
        >>> at.get_resources_for_scope(scopes.ADMIN_USER)
        ['user_id_1']
        >>> at.get_resources_for_scope(scopes.ADMIN_USER, scopes.ADMIN)
        ['user_id_1', 'user_id_2']
        """
        resources = []
        for x in self.scopes:
            if x[0] in scopes and x[1]:
                resources.append(x[1])
        return resources

    def may_append_ds(self, ds_id):
        def scope_enables_append_ds(scope, ds_id):
            # This "scopes.DATASOURCES_CREATE" means "DS control" or "DS management"
            if scope[0] in [scopes.ADMIN, scopes.ADMIN_USER, scopes.DATASOURCES_CREATE]:
                return True
            if scope[0] == scopes.DATASOURCES_APPEND and scope[1] in (None, ds_id):
                return True
            return False

        return any(scope_enables_append_ds(scope, ds_id) for scope in self.scopes)

    def may_create_ds(self, ds_name: str):
        def scope_enables_create_ds(scope, ds_name: str):
            if scope[0] in [scopes.ADMIN, scopes.ADMIN_USER]:
                return True
            # This "scopes.DATASOURCES_CREATE" means "DS control" or "DS management"
            # TODO: have a dedicated, real, CREATE_ONLY scope
            if scope[0] == scopes.DATASOURCES_CREATE:
                return True
            return False

        return any(scope_enables_create_ds(scope, ds_name) for scope in self.scopes)

    def get_filters(self) -> Dict[str, str]:
        """
        return filters for add readable tables
        >>> at = AccessToken('a', "name", 'b')
        >>> at.add_scope(scopes.DATASOURCES_READ, 'table1', 'a > 1')
        >>> at.add_scope(scopes.DATASOURCES_READ, 'table2', 'b < 2')
        >>> at.get_filters()
        {'table1': 'a > 1', 'table2': 'b < 2'}
        """
        filters = {}
        for x in self.scopes:
            # Only DATASOURCES_READ and PIPES_READ scopes can have filters. The filter is the third element in the tuple
            # If it's a string, it's a filter. If it's a dict, it's a fixed_params
            if x[0] in (scopes.DATASOURCES_READ, scopes.PIPES_READ) and len(x) > 2 and x[2] and isinstance(x[2], str):
                filters[x[1]] = x[2]
        return filters

    def get_fixed_params(self) -> Dict[str, Dict[str, Any]]:
        """
        return fixed_params for add readable tables
        >>> at = AccessToken
        >>> at = AccessToken('a', "name", 'b')
        >>> at.add_scope(scopes.DATASOURCES_READ, 'table1', {'a': 1})
        >>> at.add_scope(scopes.DATASOURCES_READ, 'table2', {'b': 2})
        >>> at.get_fixed_params()
        {'table1': {'a': 1}, 'table2': {'b': 2}}
        """
        fixed_params = {}
        for x in self.scopes:
            # Only DATASOURCES_READ and PIPES_READ scopes can have filters. The filter is the third element in the tuple
            # If it's a string, it's a filter. If it's a dict, it's a fixed_params
            if x[0] in (scopes.DATASOURCES_READ, scopes.PIPES_READ) and len(x) > 2 and x[2] and isinstance(x[2], dict):
                fixed_params[x[1]] = x[2]
        return fixed_params

    def refresh(self, secret: Any, resource_id: str, resource_prefix: Optional[str] = None) -> None:
        prefix = resource_prefix or self.resource_prefix

        self.id = str(uuid.uuid4())
        payload = {prefix: resource_id, "id": self.id, "host": self.host or AccessToken._defaults.get("host")}

        self.token = self.token_generate(
            payload,
            secret,
        )

    def to_dict(self):
        list_scopes = []
        for scope in self.scopes:
            if scope[0] not in scope_names:
                continue
            scope_data = {"type": scope_names[scope[0]]}
            if scope[0] in (
                scopes.PIPES_READ,
                scopes.PIPES_DROP,
                scopes.DATASOURCES_READ,
                scopes.DATASOURCES_APPEND,
                scopes.DATASOURCES_DROP,
            ):
                scope_data["resource"] = scope[1]
            if scope[0] in (scopes.DATASOURCES_READ, scopes.PIPES_READ):
                scope_data["filter"] = "" if len(scope) <= 2 else (scope[2] or "")
            list_scopes.append(scope_data)

        return {
            "id": self.id,
            "token": self.visible_token,
            "scopes": list_scopes,
            "name": self.name,
            "description": self.description,
            "origin": {"type": self.origin.origin_code, "resource_id": self.origin.resource_id}
            if self.origin.resource_id
            else {"type": self.origin.origin_code},
            "host": self.host or AccessToken._defaults.get("host"),
        }

    def token_generate(self, info: Dict[str, Any], secret: Any, kind: str = key_type.PUBLIC) -> str:
        """
        >>> access_token = AccessToken('a', "name", 'b')
        >>> tk = access_token.token_generate({'hola': "caracola"}, 'secret')
        >>> tk
        'p.eyJob2xhIjogImNhcmFjb2xhIn0.DEweFC5jGRdh3UFK0fDw6RfXQRXwsK3lKTLfc1V87CM'
        >>> tk2 = access_token.token_generate({'hola': "caracola", 'id': 1}, 'secret')
        >>> tk != tk2
        True
        """
        algo = jwt.algorithms.get_default_algorithms()["HS256"]
        msg = json.dumps(info)
        msg_base64 = jwt.utils.base64url_encode(msg.encode())
        sign_key = algo.prepare_key(secret)
        signature = algo.sign(msg_base64, sign_key)
        token = msg_base64 + b"." + jwt.utils.base64url_encode(signature)
        return kind + "." + token.decode()


def token_decode(token: str, secret: str) -> Dict[str, Any]:
    """
    >>> access_token = AccessToken('a', "name", 'b')
    >>> t = access_token.token_generate({'hola': "caracola"}, 'secret')
    >>> t
    'p.eyJob2xhIjogImNhcmFjb2xhIn0.DEweFC5jGRdh3UFK0fDw6RfXQRXwsK3lKTLfc1V87CM'
    >>> token_decode(t, 'secret')
    {'hola': 'caracola'}
    >>> token_decode("jajaj" + t, 'secret')
    {'hola': 'caracola'}
    >>> token_decode('p_testing.eyJob2xhIjogImNhcmFjb2xhIn0.DEweFC5jGRdh3UFK0fDw6RfXQRXwsK3lKTLfc1V87CM', 'secret')
    {'hola': 'caracola'}
    >>> token_decode('asdasd', 'secret')
    Traceback (most recent call last):
    ...
    jwt.exceptions.DecodeError
    >>> t = access_token.token_generate({'hola': "carócola"}, 'secret')
    >>> token_decode(t, 'secret')
    {'hola': 'carócola'}
    """
    fields = token.split(".")
    if len(fields) == 3:
        _, payload_encoded, signature = fields
    else:
        raise DecodeError()

    algo = jwt.algorithms.get_default_algorithms()["HS256"]

    decoded_signature: bytes = jwt.utils.base64url_decode(signature)

    if not algo.verify(payload_encoded.encode(), algo.prepare_key(secret), decoded_signature):
        raise InvalidSignatureError("Signature verification failed")
    payload = json.loads(jwt.utils.base64url_decode(payload_encoded))
    return payload


def token_decode_unverify(token: str) -> Dict[str, Any]:
    fields = token.split(".")
    if len(fields) == 3:
        _, payload, _ = fields
    else:
        raise DecodeError()
    return json.loads(jwt.utils.base64url_decode(payload))


def is_jwt_token(token: str) -> bool:
    return token[:2] != key_type.PUBLIC + "."


class JWTAccessToken(AccessToken):
    def __init__(
        self,
        workspace: "User",
        name: str,
        secret: str,
        expiration_time: int,
        limit_rps: Optional[int] = None,
    ) -> None:
        # TODO: No need to pass the secret if we have the workspace
        if secret[:1] != key_type.PUBLIC:
            raise ValueError("JWT tokens must be generated wih the workspace admin token")

        self.expiration_time = expiration_time
        self.workspace = workspace
        self.limit_rps = limit_rps
        super().__init__(
            workspace.id,
            name,
            secret,
            scopes=[],
            origin=None,
            description=None,
            resource_prefix=ResourcePrefix.JWT,
            host=None,
        )

    def get_resource_name(self, resource_id: str) -> str:
        resource = self.workspace.get_resource(resource_id)
        if not resource:
            return resource_id
        return resource.name

    @classmethod
    def get_resource_id(cls, workspace: "User", resource_name: str) -> str:
        resource = workspace.get_resource(resource_name)
        if not resource:
            return resource_name
        return resource.id

    def refresh(self, secret: str, resource_id: str, resource_prefix: Optional[str] = None) -> None:
        self.id = str(uuid.uuid4())
        payload = {
            self.resource_prefix: resource_id,
            "exp": self.expiration_time,
            "name": self.name,
            "scopes": [
                {
                    "type": scope_names[scope[0]],
                    "resource": self.get_resource_name(scope[1]) if len(scope) > 1 else None,
                    "fixed_params": scope[2] if len(scope) > 2 else None,
                }
                for scope in self.scopes
            ],
        }

        # If we have a requests_per_second limit, we add it to the payload
        if self.limit_rps:
            payload["limits"] = {"rps": self.limit_rps}

        self.token = self.token_generate(
            payload,
            secret,
        )

    @classmethod
    def token_decode_unverify(cls, token: str) -> Dict[str, Any]:
        return jwt.decode(
            token, options={"verify_signature": False, "require": ["exp"]}, verify=False, algorithms=["HS256"]
        )

    def token_generate(self, info: Dict[str, Any], secret: str, kind: str = "") -> str:
        if "exp" not in info:
            raise ValueError("Jwt tokens must have an expiration time")
        return jwt.encode(info, secret, algorithm="HS256")

    @classmethod
    def token_decode(cls, token: str, secret: str) -> Dict[str, Any]:
        """
        >>> from tinybird.user import User
        >>> workspace = User(id='abcd')
        >>> tmp_token = JWTAccessToken(workspace, "name", 'p.b', 12312313)
        >>> t = tmp_token.token_generate({'hola': "caracola", "exp": 12312313}, 'secret')
        >>> t
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJob2xhIjoiY2FyYWNvbGEiLCJleHAiOjEyMzEyMzEzfQ.5R8SgceydaC2lxLbPnT98hWIBhB4SLltIDvww7NgYXI'
        >>> is_jwt_token(t)
        True
        >>> JWTAccessToken.token_decode(t, 'secret')
        Traceback (most recent call last):
        ...
        jwt.exceptions.ExpiredSignatureError: Signature has expired
        """
        # We have disabled the verification of the iat claim because it can happens it can happen that iat > now()
        # This can happens if iat is a float number while current time is an integer
        # https://github.com/jpadilla/pyjwt/issues/814
        return jwt.decode(token, secret, options={"verify_iat": False, "verify_aud": False}, algorithms=["HS256"])

    @classmethod
    def generate_jwt_access_from_token(cls, token: str, workspace: "User") -> Optional["JWTAccessToken"]:
        workspace_token = workspace.get_token_for_scope(scopes.ADMIN)
        if not workspace_token:
            logging.warning(f"Admin workspace token not found for workspace {workspace.id}")
            return None

        try:
            payload = cls.token_decode(token, workspace_token)
            access_token = JWTAccessToken(
                workspace,
                payload["name"],
                workspace_token,
                payload["exp"],
                payload.get("limits", {}).get("rps"),
            )

            # TODO: We should add a validation to make sure inform the user if the payload is not correct
            for scope in payload["scopes"]:
                # We are already checking to only be able to process requests that reach APIPipeDataHandler
                # But let's be safe and add a check here
                resource_name = scope.get("resource")
                if scope["type"] != scope_names[scopes.PIPES_READ] or not resource_name:
                    return None

                access_token.add_scope(
                    scope_codes[scope["type"]],
                    cls.get_resource_id(workspace, resource_name),
                    scope.get("fixed_params"),
                )
            return access_token
        except Exception as e:
            logging.warning(f"Error generating access token from jwt token: {e} {payload}")
            return None

    def to_json(self):
        return {
            "token": self.token,
            "name": self.name,
            "exp": self.expiration_time,
            "scopes": [
                {
                    "type": scope_names[scope[0]],
                    "resource": self.get_resource_name(scope[1]) if len(scope) > 1 else None,
                    "fixed_params": scope[2] if len(scope) > 2 else None,
                }
                for scope in self.scopes
            ],
            "limits": {"rps": self.limit_rps},
        }
