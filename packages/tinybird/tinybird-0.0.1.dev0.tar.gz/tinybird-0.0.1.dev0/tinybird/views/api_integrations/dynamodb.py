from typing import Optional

from tornado.web import URLSpec, url

from tinybird.integrations.dynamodb.policies import get_dynamodb_access_read_policy
from tinybird.integrations.s3 import get_assume_role_trust_policy, validate_s3_bucket_name
from tinybird.tokens import scopes
from tinybird.views.api_errors.data_connectors import DynamoDBConnectorError
from tinybird.views.base import ApiHTTPError, BaseHandler, authenticated, with_scope


class APIDynamoDBIntegrationTrustPolicy(BaseHandler):
    @authenticated
    @with_scope(scopes.ADMIN)
    async def get(self):
        policy = await get_assume_role_trust_policy(self.current_workspace)
        self.write_json(policy.render())


class APIDynamoDBIntegrationAccessReadPolicy(BaseHandler):
    @authenticated
    @with_scope(scopes.ADMIN)
    async def get(self):
        bucket: Optional[str] = self.get_argument("bucket", None)
        table_name: Optional[str] = self.get_argument("table_name", None)

        if bucket and not validate_s3_bucket_name(bucket):
            raise ApiHTTPError.from_request_error(DynamoDBConnectorError.invalid_bucket_name_error())

        policy = get_dynamodb_access_read_policy(bucket, table_name)
        self.write_json(policy.render())


def handlers() -> list[URLSpec]:
    return [
        url(r"/v0/integrations/dynamodb/policies/trust-policy", APIDynamoDBIntegrationTrustPolicy),
        url(r"/v0/integrations/dynamodb/policies/read-access-policy", APIDynamoDBIntegrationAccessReadPolicy),
    ]
