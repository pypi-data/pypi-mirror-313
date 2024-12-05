class ScopeException(Exception):
    pass


class scopes:
    # These are the tokens that can be set by the user.
    # They are documented externally in our docs https://docs.tinybird.co/api-reference/token-api.html#scopes-and-tokens
    DATASOURCES_CREATE = "DC"
    DATASOURCES_APPEND = "DA"
    DATASOURCES_READ = "DR"
    DATASOURCES_DROP = "DD"
    PIPES_CREATE = "PC"
    PIPES_READ = "PR"
    PIPES_DROP = "PD"
    TOKENS = "TK"
    ADMIN = "ADM"

    # These are internal tokens that we use for internal purposes, not exposed to the user
    ADMIN_USER = "ADMU"
    AUTH = "AUTH"

    # ADMIN_USER:
    # - this token belongs to a *workspace* (User class)
    # - must be always associated with a user account id, by setting this id as a token resource
    # - this scope allows us to identify the user account by using the token's resource
    # - there's and ADMIN_USER token for each user per workspace
    # - guest users can only see their own internal admin user token, while admin users can see
    #   the whole list of internal admin user tokens
    # - when a user is removed from a workspace, their internal admin user token is removed
    #
    # AUTH:
    # - this token belongs to a *user_account* (UserAccount classs)
    # - it's used to get the user account that is currently logged in (see 'get_current_user' method)
    # - in order to keep using the same authentication method that we used when login as a 'workspace' in the past,
    #   we kept the authentication via token, but we created a new scope, AUTH, only for this use case
    # - it's only used from operations that can *only* be done in the UI, like inviting someone to a workspace. It's used
    #   in the endpoints that are not exposed to the user, but that we use from the UI, like the example above:
    #   inviting someone to a workspace or sharing a data source to a different workspace. These operations, that are internal,
    #   can not be done with an 'ADMIN' token. Since they are internal operations, we can decide to change this behaviour
    #   when we consider it necessary, because it won't affect our users since they're not using these endpoints.
    # - you can check where the '@user_authenticated' decorator is being used to see which endpoints are we using
    #   only from the UI with an 'AUTH' token

    __valid_scopes__ = (
        DATASOURCES_CREATE,
        DATASOURCES_APPEND,
        DATASOURCES_READ,
        DATASOURCES_DROP,
        PIPES_CREATE,
        PIPES_READ,
        PIPES_DROP,
        TOKENS,
        ADMIN,
        ADMIN_USER,
        AUTH,
    )

    @staticmethod
    def is_resource_mandatory(s: str) -> bool:
        return s in (
            scopes.DATASOURCES_READ,
            scopes.DATASOURCES_APPEND,
            scopes.DATASOURCES_DROP,
            scopes.PIPES_READ,
            scopes.PIPES_DROP,
            scopes.ADMIN_USER,
        )

    @staticmethod
    def can_have_filter(s: str) -> bool:
        return s in (scopes.DATASOURCES_READ, scopes.PIPES_READ)

    @classmethod
    def is_valid(cls, s: str) -> bool:
        """
        >>> scopes.is_valid(scopes.ADMIN)
        True
        >>> scopes.is_valid('asdasd')
        False
        """
        return s in cls.__valid_scopes__


scope_names = {
    scopes.DATASOURCES_READ: "DATASOURCES:READ",
    scopes.DATASOURCES_APPEND: "DATASOURCES:APPEND",
    scopes.DATASOURCES_CREATE: "DATASOURCES:CREATE",
    scopes.DATASOURCES_DROP: "DATASOURCES:DROP",
    scopes.PIPES_CREATE: "PIPES:CREATE",
    scopes.PIPES_READ: "PIPES:READ",
    scopes.PIPES_DROP: "PIPES:DROP",
    scopes.TOKENS: "TOKENS",
    scopes.ADMIN: "ADMIN",
    scopes.AUTH: "AUTH",
    scopes.ADMIN_USER: "ADMIN_USER",
}

scope_codes = dict(zip(scope_names.values(), scope_names.keys(), strict=True))

scope_prefixes = ["DATASOURCES", "PIPES"]
