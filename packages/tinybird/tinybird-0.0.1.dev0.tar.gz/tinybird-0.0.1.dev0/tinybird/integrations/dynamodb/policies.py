import dataclasses
import re
from typing import Any, Optional

from tinybird.integrations.s3 import _render_aws_policy


@dataclasses.dataclass(frozen=True)
class AWSDynamoDBAccessReadPolicy:
    bucket: Optional[str] = None
    table_name: Optional[str] = None

    def render(self) -> dict[str, Any]:
        bucket = self.bucket or "<bucket>"
        table_name = self.table_name or "<table_name>"
        statements = [
            {
                "Effect": "Allow",
                "Action": [
                    "dynamodb:Scan",
                    "dynamodb:DescribeStream",
                    "dynamodb:DescribeExport",
                    "dynamodb:GetRecords",
                    "dynamodb:GetShardIterator",
                    "dynamodb:DescribeTable",
                    "dynamodb:DescribeContinuousBackups",
                    "dynamodb:ExportTableToPointInTime",
                    "dynamodb:UpdateTable",
                    "dynamodb:UpdateContinuousBackups",
                ],
                "Resource": [
                    f"arn:aws:dynamodb:*:*:table/{table_name}",
                    f"arn:aws:dynamodb:*:*:table/{table_name}/stream/*",
                    f"arn:aws:dynamodb:*:*:table/{table_name}/export/*",
                ],
            },
            {
                "Effect": "Allow",
                "Action": ["s3:PutObject", "s3:GetObject", "s3:ListBucket"],
                "Resource": [f"arn:aws:s3:::{bucket}", f"arn:aws:s3:::{bucket}/*"],
            },
        ]
        return _render_aws_policy(statements)


def get_dynamodb_access_read_policy(
    bucket: Optional[str] = None, table_name: Optional[str] = None
) -> AWSDynamoDBAccessReadPolicy:
    return AWSDynamoDBAccessReadPolicy(bucket, table_name)


def validate_table_arn(arn: str):
    arn_regex = r"arn:aws:dynamodb:[\w-]+:\d{12}:table/([\w-]+)"
    match = re.match(arn_regex, arn)
    return bool(match)
