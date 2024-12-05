from typing import Optional

from tornado.web import URLSpec, url

from tinybird.integrations.s3 import (
    get_assume_role_trust_policy,
    get_s3_access_read_policy,
    get_s3_access_write_policy,
    get_s3_role_settings,
    validate_s3_bucket_name,
)
from tinybird.tokens import scopes
from tinybird.views.api_errors.data_connectors import S3SourceError
from tinybird.views.base import ApiHTTPError, BaseHandler, authenticated, with_scope


class APIS3IntegrationTrustPolicy(BaseHandler):
    @authenticated
    @with_scope(scopes.ADMIN)
    async def get(self):
        policy = await get_assume_role_trust_policy(self.current_workspace)
        self.write_json(policy.render())


class APIS3IntegrationAccessWritePolicy(BaseHandler):
    @authenticated
    @with_scope(scopes.ADMIN)
    async def get(self):
        bucket: Optional[str] = self.get_argument("bucket", None)
        if bucket and not validate_s3_bucket_name(bucket):
            raise ApiHTTPError.from_request_error(S3SourceError.invalid_bucket_name_error())
        policy = get_s3_access_write_policy(bucket)
        self.write_json(policy.render())


class APIS3IntegrationAccessReadPolicy(BaseHandler):
    @authenticated
    @with_scope(scopes.ADMIN)
    async def get(self):
        bucket: Optional[str] = self.get_argument("bucket", None)
        if bucket and not validate_s3_bucket_name(bucket):
            raise ApiHTTPError.from_request_error(S3SourceError.invalid_bucket_name_error())
        policy = get_s3_access_read_policy(bucket)
        self.write_json(policy.render())


class APIS3IntegrationSettings(BaseHandler):
    @authenticated
    @with_scope(scopes.ADMIN)
    async def get(self):
        role_settings = await get_s3_role_settings(self.current_workspace)
        self.write_json(role_settings.to_dict())


def handlers() -> list[URLSpec]:
    return [
        url(r"/v0/integrations/s3/policies/trust-policy", APIS3IntegrationTrustPolicy),
        url(r"/v0/integrations/s3/policies/write-access-policy", APIS3IntegrationAccessWritePolicy),
        url(r"/v0/integrations/s3/policies/read-access-policy", APIS3IntegrationAccessReadPolicy),
        url(r"/v0/integrations/s3/settings", APIS3IntegrationSettings),
    ]
