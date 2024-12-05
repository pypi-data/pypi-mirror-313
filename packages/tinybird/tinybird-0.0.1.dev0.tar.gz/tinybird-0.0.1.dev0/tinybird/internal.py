from typing import Any, Dict, Optional


async def get_by_pipe_endpoint(
    api_host: Optional[str], pipe_endpoint_name: str, **params: Any
) -> Optional[Dict[str, Any]]:
    # avoid circular import
    from tinybird.client import TinyB
    from tinybird.config import VERSION
    from tinybird.tokens import scopes
    from tinybird.user import public

    if not api_host:
        return None

    pu = public.get_public_user()
    pipe = pu.get_pipe(pipe_endpoint_name)
    if not pipe:
        raise Exception(f"pipe {pipe_endpoint_name} not found")
    tokens = pu.get_tokens_for_resource(pipe.id, scopes.PIPES_READ)
    if not tokens:
        raise Exception(f"read token for {pipe_endpoint_name} not found")
    tb_client = TinyB(tokens[0], api_host, VERSION)
    return await tb_client.pipe_data(pipe.name, format="json", params=params)
