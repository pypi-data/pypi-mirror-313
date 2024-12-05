from typing import Optional, Tuple

from tinybird.token_scope import scopes


class Origins:
    """Possible token origins.

    Just don't change any value here but, if you do, pretty-please,
    remember to update literals "C", "P" and "DS" in tb_cli.py and client.py.

    I put them as-is there to avoid leaking additional code defined here. // luis.medel
    """

    # Legacy tokens: those created before we started to track origin
    LEGACY = "L"

    # Token created by a user
    CUSTOM = "C"

    # Token created for a pipe
    PIPE = "P"

    # Token created for a datasource
    DATASOURCE = "DS"

    # Token created for an exploration
    TIMESERIES = "TS"

    __scopes__ = {
        LEGACY: None,
        CUSTOM: None,
        PIPE: scopes.PIPES_READ,
        DATASOURCE: scopes.DATASOURCES_READ,
        TIMESERIES: scopes.DATASOURCES_READ,
    }

    @classmethod
    def is_valid_scope_for_origin(cls, scope: str, origin: str) -> bool:
        return scope == cls.__scopes__.get(origin, None)

    @classmethod
    def origin_needs_resource(cls, origin: str) -> bool:
        return origin != cls.LEGACY and origin != cls.CUSTOM


class TokenOrigin:
    __valid_origins__: Tuple[str, ...] = (
        Origins.LEGACY,
        Origins.CUSTOM,
        Origins.PIPE,
        Origins.DATASOURCE,
        Origins.TIMESERIES,
    )

    def __init__(self, origin_code: str, resource_id: Optional[str] = None):
        if origin_code not in self.__valid_origins__:
            raise ValueError(f"Invalid origin_code: '{origin_code}'")
        self.origin_code = origin_code
        self.resource_id = resource_id
