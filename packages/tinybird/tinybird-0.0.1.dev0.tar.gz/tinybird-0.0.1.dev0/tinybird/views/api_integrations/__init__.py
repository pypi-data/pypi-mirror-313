from tinybird.views.api_integrations.dynamodb import handlers as dynamodb_handlers
from tinybird.views.api_integrations.s3 import handlers as s3_handlers
from tinybird.views.api_integrations.vercel import handlers as vercel_handlers


def handlers() -> list:
    return [
        *vercel_handlers(),
        *s3_handlers(),
        *dynamodb_handlers(),
    ]
