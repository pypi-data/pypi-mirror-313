import google.auth.exceptions
import google.auth.impersonated_credentials
import google.auth.transport.requests
from google.auth import compute_engine

from tinybird.providers.gcp.exceptions import AuthenticationFailed


# This tries to connect to the metadata provider of the instance so it won't run in local. Needs to be patched out.
def get_id_token_from_metadata_server(target_audience: str) -> str:
    request = google.auth.transport.requests.Request()
    try:
        credentials = compute_engine.IDTokenCredentials(
            request=request,
            target_audience=target_audience,
            use_metadata_identity_endpoint=True,
        )
        credentials.refresh(request)
    except (ValueError, google.auth.exceptions.GoogleAuthError) as err:
        raise AuthenticationFailed(err) from err
    return credentials.token
