import dataclasses


@dataclasses.dataclass(frozen=True)
class AccessKeyCredentials:
    access_key_id: str
    secret_access_key: str


# Not a subclass of AccessKeyCredentials to avoid mistakes when resolving types
@dataclasses.dataclass(frozen=True)
class TemporaryAWSCredentials:
    access_key_id: str
    secret_access_key: str
    session_token: str
