import json
import re
from dataclasses import dataclass
from datetime import date
from typing import Any, Dict, List, NamedTuple, Optional, Tuple
from urllib.parse import urlencode

from tornado.simple_httpclient import SimpleAsyncHTTPClient

from tinybird.datasource import Datasource
from tinybird.resource import Resource
from tinybird.user import User, UserAccount, UserAccounts


@dataclass
class IngestionError:
    pattern: Optional[re.Pattern]
    header: str
    subheader: str
    text: str
    button_text: str


allowed_ingestion_errors = {
    "could_not_fetch_url": IngestionError(
        pattern=re.compile(".*Could not fetch URL.*"),
        header="Failed ingestion.",
        subheader="We could not fetch the URL you provided.",
        text="""Hello {user},

An error happened while trying to ingest data into {datasource}.

Please ensure the URL is valid an reachable and try again. If you are sure the URL is valid and reachable and the error persists after retrying, please contact <a href="mailto:support@tinybird.co">our support</a> team.""",
        button_text="Access your Data Source Operations logs",
    ),
    "ndjson_403": IngestionError(
        pattern=re.compile(".*NDJSON/Parquet import unhandled exception while streaming: HTTP GET.*status code.* 403"),
        header="Failed ingestion.",
        subheader="We were unable to handle your NDJSON/Parquet import.",
        text="""Hello {user},

An error happened while trying to ingest data into {datasource}. Your NDJSON/Parquet ingestion returned the following error:

{error}

Feel free to check the operations log or contact <a href="mailto:support@tinybird.co">our support</a> team.""",
        button_text="Access your Data Source Operations logs",
    ),
    "null_to_non_nullable": IngestionError(
        pattern=re.compile(".*Cannot convert NULL value to non-Nullable type.*"),
        header="Issues detected in your Data Source.",
        subheader="Please review your non-Nullable columns.",
        text="""Hello {user},

An error happened in your Data Source {datasource}.

We detected Null values trying to be inserted into non-Nullable columns:

Please see the full error below:
{error}

Of course, you can also <a href="mailto:support@tinybird.co">reach us</a> at anytime.""",
        button_text="Access your Data Source Operations logs",
    ),
    "check_partition_key": IngestionError(
        pattern=re.compile(".*Please make sure the ENGINE_PARTITION_KEY setting is correct.*"),
        header="Issues detected in your Data Source.",
        subheader="Please review ENGINE_PARTITION_KEY value.",
        text="""Hello {user},

An error happened in your Data Source {datasource}. We believe the issue was caused by your ENGINE_PARTITON_KEY setting.

Please follow our guide on how to <a href="https://www.tinybird.co/docs/concepts/data-sources.html#partitioning">set up partition keys</a> for your Data Sources and try again.

Our team has automatically been notified of the issue so the might contact you. Of course, you can also reach us at anytime.""",
        button_text="Access your Data Source Operations logs",
    ),
    "no_such_file_or_directory": IngestionError(
        pattern=re.compile(".*No such file or directory.*"),
        header="Failed ingestion.",
        subheader="No such file or directory.",
        text="""Hello {user},

An error happened while trying to ingest data into {datasource}.

Please ensure the URL is valid an reachable and try again. If you are sure the URL is valid and reachable and the error persists after retrying, please contact <a href="mailto:support@tinybird.co">our support team.</a>""",
        button_text="Access your Data Source Operations logs",
    ),
    "csv_separator_or_larger_20480": IngestionError(
        pattern=re.compile(".*CSV separator field not found, does the CSV have rows larger than 20480 bytes.*"),
        header="Some data was not ingested.",
        subheader="Please review separators and very large rows.",
        text="""Hello {user},

An error happened while trying to ingest data into {datasource}.

Please ensure the provided CSV file does not contain unexpected delimiter characters nor it has unusually large rows (+20Kb / row).

Should you have any doubt, please contact <a href="mailto:support@tinybird.co">our support team.</a>""",
        button_text="Access your Data Source Operations logs",
    ),
    "dynamodb_connector_user_configuration_error": IngestionError(
        pattern=re.compile(
            ".*An error occurred \((AccessDeniedException|ResourceNotFoundException|StreamNotEnabledException)\) when calling the (DescribeTable|DescribeStream|GetShardIterator|GetRecords) operation.*"
        ),
        header="Failed ingestion.",
        subheader="Error detected when ingesting DynamoDB updates.",
        text="""Hello {user},
An error happened while trying to ingest data into {datasource}.

Please ensure the DynamoDB table has a stream enabled and the correct permissions have been granted.

Should you have any doubt, please contact <a href="mailto:support@tinybird.co">our support team.</a>""",
        button_text="Access your Data Source Operations logs",
    ),
}

multiple_errors = IngestionError(
    pattern=None,
    header="Data Source Error.",
    subheader="We detected errors in your Data Source.",
    text="""Hello {user},

We detected errors in your Data Source {datasource}:

{error}

Feel free to check the operations log. If you your issues persist, please contact <a href="mailto:support@tinybird.co">our support team.""",
    button_text="Access your Data Source Operations logs",
)


def _extract_error_details(errors: list, user, datasource):
    """
    # Single errors allowed
    >>> _extract_error_details([{'timestamp': '2024-02-06 13:41:00', 'error': 'aaa Could not fetch URL eee'}], 'asd@asd.es', 'mec')
    ('Failed ingestion.', 'We could not fetch the URL you provided.', 'Hello asd@asd.es,<br><br>An error happened while trying to ingest data into mec.<br><br>Please ensure the URL is valid an reachable and try again. If you are sure the URL is valid and reachable and the error persists after retrying, please contact <a href="mailto:support@tinybird.co">our support</a> team.', 'Access your Data Source Operations logs')
    >>> _extract_error_details([{'timestamp': '2024-02-07 13:41:00', 'error': 'aaa NDJSON/Parquet import unhandled exception while streaming: HTTP GET mec status code 403 eee'}], 'asd@asd.es', 'mec')
    ('Failed ingestion.', 'We were unable to handle your NDJSON/Parquet import.', 'Hello asd@asd.es,<br><br>An error happened while trying to ingest data into mec. Your NDJSON/Parquet ingestion returned the following error:<br><br><b>2024-02-07 13:41:00 UTC</b> - aaa NDJSON/Parquet import unhandled exception while streaming: HTTP GET mec status code 403 eee<br><br>Feel free to check the operations log or contact <a href="mailto:support@tinybird.co">our support</a> team.', 'Access your Data Source Operations logs')
    >>> _extract_error_details([{'timestamp': '2024-02-08 13:41:00', 'error': 'aaa Cannot convert NULL value to non-Nullable type eee'}], 'asd@asd.es', 'mec')
    ('Issues detected in your Data Source.', 'Please review your non-Nullable columns.', 'Hello asd@asd.es,<br><br>An error happened in your Data Source mec.<br><br>We detected Null values trying to be inserted into non-Nullable columns:<br><br>Please see the full error below:<br><b>2024-02-08 13:41:00 UTC</b> - aaa Cannot convert NULL value to non-Nullable type eee<br><br>Of course, you can also <a href="mailto:support@tinybird.co">reach us</a> at anytime.', 'Access your Data Source Operations logs')
    >>> _extract_error_details([{'timestamp': '2024-02-09 13:41:00', 'error': 'aaa Please make sure the ENGINE_PARTITION_KEY setting is correct eee'}], 'asd@asd.es', 'mec')
    ('Issues detected in your Data Source.', 'Please review ENGINE_PARTITION_KEY value.', 'Hello asd@asd.es,<br><br>An error happened in your Data Source mec. We believe the issue was caused by your ENGINE_PARTITON_KEY setting.<br><br>Please follow our guide on how to <a href="https://www.tinybird.co/docs/concepts/data-sources.html#partitioning">set up partition keys</a> for your Data Sources and try again.<br><br>Our team has automatically been notified of the issue so the might contact you. Of course, you can also reach us at anytime.', 'Access your Data Source Operations logs')
    >>> _extract_error_details([{'timestamp': '2024-02-10 13:41:00', 'error': 'aaa No such file or directory eee'}], 'asd@asd.es', 'mec')
    ('Failed ingestion.', 'No such file or directory.', 'Hello asd@asd.es,<br><br>An error happened while trying to ingest data into mec.<br><br>Please ensure the URL is valid an reachable and try again. If you are sure the URL is valid and reachable and the error persists after retrying, please contact <a href="mailto:support@tinybird.co">our support team.</a>', 'Access your Data Source Operations logs')
    >>> _extract_error_details([{'timestamp': '2024-02-06 13:41:00', 'error': 'An error occurred (AccessDeniedException) when calling the DescribeTable operation: User: arn:aws:sts::819314934727:assumed-role/jvilaseca-test-dynamodb/c66133a4-2441-43b2-a18d-92b1a8a77770 is not authorized to perform: dynamodb:DescribeTable on resource: arn:aws:dynamodb:eu-west-3:819314934727:table/Table/stream/2024-09-26T11:44:27.478 because no identity-based policy allows the dynamodb:DescribeTable action'}], 'asd@asd.es', 'mec')
    ('Failed ingestion.', 'Error detected when ingesting DynamoDB updates.', 'Hello asd@asd.es,<br>An error happened while trying to ingest data into mec.<br><br>Please ensure the DynamoDB table has a stream enabled and the correct permissions have been granted.<br><br>Should you have any doubt, please contact <a href="mailto:support@tinybird.co">our support team.</a>', 'Access your Data Source Operations logs')
    >>> _extract_error_details([{'timestamp': '2024-02-06 13:41:00', 'error': 'An error occurred (AccessDeniedException) when calling the DescribeStream operation: User: arn:aws:sts::819314934727:assumed-role/jvilaseca-test-dynamodb/c66133a4-2441-43b2-a18d-92b1a8a77770 is not authorized to perform: dynamodb:DescribeStream on resource: arn:aws:dynamodb:eu-west-3:819314934727:table/Table/stream/2024-09-26T11:44:27.478 because no identity-based policy allows the dynamodb:DescribeStream action'}], 'asd@asd.es', 'mec')
    ('Failed ingestion.', 'Error detected when ingesting DynamoDB updates.', 'Hello asd@asd.es,<br>An error happened while trying to ingest data into mec.<br><br>Please ensure the DynamoDB table has a stream enabled and the correct permissions have been granted.<br><br>Should you have any doubt, please contact <a href="mailto:support@tinybird.co">our support team.</a>', 'Access your Data Source Operations logs')
    >>> _extract_error_details([{'timestamp': '2024-02-06 13:41:00', 'error': 'An error occurred (AccessDeniedException) when calling the GetShardIterator operation: User: arn:aws:sts::819314934727:assumed-role/jvilaseca-test-dynamodb/c66133a4-2441-43b2-a18d-92b1a8a77770 is not authorized to perform: dynamodb:GetShardIterator on resource: arn:aws:dynamodb:eu-west-3:819314934727:table/Table/stream/2024-09-26T11:44:27.478 because no identity-based policy allows the dynamodb:GetShardIterator action'}], 'asd@asd.es', 'mec')
    ('Failed ingestion.', 'Error detected when ingesting DynamoDB updates.', 'Hello asd@asd.es,<br>An error happened while trying to ingest data into mec.<br><br>Please ensure the DynamoDB table has a stream enabled and the correct permissions have been granted.<br><br>Should you have any doubt, please contact <a href="mailto:support@tinybird.co">our support team.</a>', 'Access your Data Source Operations logs')
    >>> _extract_error_details([{'timestamp': '2024-02-06 13:41:00', 'error': 'An error occurred (AccessDeniedException) when calling the GetRecords operation: User: arn:aws:sts::819314934727:assumed-role/jvilaseca-test-dynamodb/c66133a4-2441-43b2-a18d-92b1a8a77770 is not authorized to perform: dynamodb:GetRecords on resource: arn:aws:dynamodb:eu-west-3:819314934727:table/Table/stream/2024-09-26T11:44:27.478 because no identity-based policy allows the dynamodb:GetRecords action'}], 'asd@asd.es', 'mec')
    ('Failed ingestion.', 'Error detected when ingesting DynamoDB updates.', 'Hello asd@asd.es,<br>An error happened while trying to ingest data into mec.<br><br>Please ensure the DynamoDB table has a stream enabled and the correct permissions have been granted.<br><br>Should you have any doubt, please contact <a href="mailto:support@tinybird.co">our support team.</a>', 'Access your Data Source Operations logs')
    >>> _extract_error_details([{'timestamp': '2024-02-06 13:41:00', 'error': 'An error occurred (ResourceNotFoundException) when calling the DescribeTable operation: User: arn:aws:sts::819314934727:assumed-role/jvilaseca-test-dynamodb/c66133a4-2441-43b2-a18d-92b1a8a77770 is not authorized to perform: dynamodb:DescribeTable on resource: arn:aws:dynamodb:eu-west-3:819314934727:table/Table/stream/2024-09-26T11:44:27.478 because no identity-based policy allows the dynamodb:DescribeTable action'}], 'asd@asd.es', 'mec')
    ('Failed ingestion.', 'Error detected when ingesting DynamoDB updates.', 'Hello asd@asd.es,<br>An error happened while trying to ingest data into mec.<br><br>Please ensure the DynamoDB table has a stream enabled and the correct permissions have been granted.<br><br>Should you have any doubt, please contact <a href="mailto:support@tinybird.co">our support team.</a>', 'Access your Data Source Operations logs')

    # Any other error not allowed
    >>> _extract_error_details([{'timestamp': '2024-02-06 13:41:00', 'error': 'example error'}], 'asd@asd.es', 'mec')
    (None, None, None, None)
    >>> _extract_error_details([{'timestamp': '2024-02-06 13:41:00', 'error': 'example error'}, {'timestamp': '2024-02-06 13:41:00', 'error': 'another error'}], 'asd@asd.es', 'mec')
    (None, None, None, None)
    >>> _extract_error_details([{'timestamp': '2024-02-06 13:41:00', 'error': 'Too many simultaneous queries'}], 'asd@asd.es', 'mec')
    (None, None, None, None)
    >>> _extract_error_details([{'timestamp': '2024-02-06 13:41:00', 'error': 'Too many partitions'}], 'asd@asd.es', 'mec')
    (None, None, None, None)
    >>> _extract_error_details([{'timestamp': '2024-02-06 13:41:00', 'error': 'ClickHouse error, status=400'}], 'asd@asd.es', 'mec')
    (None, None, None, None)
    >>> _extract_error_details([{'timestamp': '2024-02-06 13:41:00', 'error': 'ClickHouse connection error'}], 'asd@asd.es', 'mec')
    (None, None, None, None)
    >>> _extract_error_details([{'timestamp': '2024-02-06 13:41:00', 'error': "Cannot parse string 'VALID' as UInt128"}], 'asd@asd.es', 'mec')
    (None, None, None, None)
    >>> _extract_error_details([{'timestamp': '2024-02-06 13:41:00', 'error': 'Memory limit'}], 'asd@asd.es', 'mec')
    (None, None, None, None)
    >>> _extract_error_details([{'timestamp': '2024-02-06 13:41:00', 'error': 'UNKNOWN_DATABASE'}], 'asd@asd.es', 'mec')
    (None, None, None, None)
    >>> _extract_error_details([{'timestamp': '2024-02-06 13:41:00', 'error': 'There was an error when attempting to import your data'}], 'asd@asd.es', 'mec')
    (None, None, None, None)
    >>> _extract_error_details([{'timestamp': '2024-02-06 13:41:00', 'error': 'UNKNOWN_TABLE'}], 'asd@asd.es', 'mec')
    (None, None, None, None)
    >>> _extract_error_details([{'timestamp': '2024-02-06 13:41:00', 'error': 'There are blocks with errors'}], 'asd@asd.es', 'mec')
    (None, None, None, None)
    >>> _extract_error_details([{'timestamp': '2024-02-06 13:41:00', 'error': 'deterministic functions'}], 'asd@asd.es', 'mec')
    (None, None, None, None)
    >>> _extract_error_details([{'timestamp': '2024-02-06 13:41:00', 'error': 'Invalid data source structure: MergeTree'}], 'asd@asd.es', 'mec')
    (None, None, None, None)
    >>> _extract_error_details([{'timestamp': '2024-02-06 13:41:00', 'error': 'The Materialized Node is using too much memory'}], 'asd@asd.es', 'mec')
    (None, None, None, None)

    # Multiple errors allowed
    >>> _extract_error_details([{'timestamp': '2024-02-06 13:41:00', 'error': 'aaa Could not fetch URL eee'}, {'timestamp': '2024-02-06 13:41:00', 'error': 'another error'}], 'asd@asd.es', 'mec')
    ('Failed ingestion.', 'We could not fetch the URL you provided.', 'Hello asd@asd.es,<br><br>An error happened while trying to ingest data into mec.<br><br>Please ensure the URL is valid an reachable and try again. If you are sure the URL is valid and reachable and the error persists after retrying, please contact <a href="mailto:support@tinybird.co">our support</a> team.', 'Access your Data Source Operations logs')
    >>> _extract_error_details([{'timestamp': '2024-02-06 13:41:00', 'error': 'aaa Could not fetch URL eee'}, {'timestamp': '2024-02-06 13:41:00', 'error': 'aaa NDJSON/Parquet import unhandled exception while streaming: HTTP GET mec status code 403 eee'}], 'asd@asd.es', 'mec')
    ('Data Source Error.', 'We detected errors in your Data Source.', 'Hello asd@asd.es,<br><br>We detected errors in your Data Source mec:<br><br><b>2024-02-06 13:41:00 UTC</b> - aaa Could not fetch URL eee<br><br><b>2024-02-06 13:41:00 UTC</b> - aaa NDJSON/Parquet import unhandled exception while streaming: HTTP GET mec status code 403 eee<br><br>Feel free to check the operations log. If you your issues persist, please contact <a href="mailto:support@tinybird.co">our support team.', 'Access your Data Source Operations logs')
    >>> _extract_error_details([{'timestamp': '2024-02-06 13:41:00', 'error': 'aaa Please make sure the ENGINE_PARTITION_KEY setting is correct eee'}, {'timestamp': '2024-02-06 13:41:00', 'error': 'aaa No such file or directory eee'}, {'timestamp': '2024-02-06 13:41:00', 'error': 'aaa Could not fetch URL eee'}], 'asd@asd.es', 'mec')
    ('Data Source Error.', 'We detected errors in your Data Source.', 'Hello asd@asd.es,<br><br>We detected errors in your Data Source mec:<br><br><b>2024-02-06 13:41:00 UTC</b> - aaa Please make sure the ENGINE_PARTITION_KEY setting is correct eee<br><br><b>2024-02-06 13:41:00 UTC</b> - aaa No such file or directory eee<br><br><b>2024-02-06 13:41:00 UTC</b> - aaa Could not fetch URL eee<br><br>Feel free to check the operations log. If you your issues persist, please contact <a href="mailto:support@tinybird.co">our support team.', 'Access your Data Source Operations logs')

    # Old incidents without timestamp not reported
    >>> _extract_error_details(['aaa Could not fetch URL eee'], 'asd@asd.es', 'mec')
    (None, None, None, None)
    >>> _extract_error_details(['aaa Could not fetch URL eee', 'another error'], 'asd@asd.es', 'mec')
    (None, None, None, None)
    """

    def _get_error_text(error):
        # Backward-compatible method to support older error types that were plain strings
        if type(error) is not dict:
            return None
        return f"<b>{error['timestamp']} UTC</b> - {error['error']}"

    def _get_allowed_ingestion_error(error):
        if error is None:
            return None
        for key, value in allowed_ingestion_errors.items():
            if value.pattern and value.pattern.match(error):
                return key
        return None

    errors_text = [_get_error_text(error) for error in errors]
    errors = [error for error in errors_text if _get_allowed_ingestion_error(error) is not None]
    if len(errors) == 1:
        key = _get_allowed_ingestion_error(errors[0])
        text = allowed_ingestion_errors[key].text.format(user=user, datasource=datasource, error=errors[0])
        ingestion_error = allowed_ingestion_errors[key]
    elif len(errors) > 1:
        ingestion_error = multiple_errors
        text = ingestion_error.text.format(user=user, datasource=datasource, error="<br><br>".join(errors))
    else:
        return None, None, None, None

    text = text.replace("\n", "<br>")
    header = ingestion_error.header
    subheader = ingestion_error.subheader
    button_text = ingestion_error.button_text

    return header, subheader, text, button_text


def _extract_quarantine_timeline(timeline: List[dict], imports: int) -> str:
    if len(timeline) == 0:
        return ""
    text = "<ul>"
    for entry in timeline:
        rows = entry["rows"]
        text += f"<li>{entry['timestamp']} UTC - {rows:,} {'row' if rows == 1 else 'rows'} in quarantine</li>"
    if imports > 10:
        text += "<li>...</li>"
    text += "</ul>"
    return text


class NotificationResponse(NamedTuple):
    status_code: int
    content: str = ""


class MailgunService:
    def __init__(self, settings):
        self._settings = settings
        self.__http_client = None

    @property
    def _http_client(self) -> SimpleAsyncHTTPClient:
        if not self.__http_client:
            self.__http_client = SimpleAsyncHTTPClient()
        return self.__http_client

    @property
    def _url(self) -> str:
        return f"{self._settings['mailgun']['domain']}/messages"

    @property
    def _auth(self) -> Tuple[str, str]:
        return ("api", self._settings["mailgun"]["api_key"])

    @property
    def _from_email(self) -> str:
        return f"Tinybird {self._settings['mailgun']['email']}"

    def _get_invitation_link(self, workspace_id: str) -> str:
        return f"{self._settings['host']}/v0/workspaces/{workspace_id}/invite"

    def _get_workspace_link(self, workspace_id: str) -> str:
        return f"{self._settings['host']}/{workspace_id}/dashboard"

    def _get_user_link(self, user_id: str) -> str:
        return f"{self._settings['host']}/{user_id}/dashboard"

    def _get_datasource_log_link(self, workspace_id, datasource_id: str) -> str:
        return f"{self._settings['host']}/{workspace_id}/datasource/{datasource_id}/log"

    def _get_datasource_link(self, workspace_id, datasource_id: str) -> str:
        return f"{self._settings['host']}/{workspace_id}/datasource/{datasource_id}"

    def _get_endpoint_link(self, workspace_name, pipe_name: str) -> str:
        return f"{self._settings['host']}/{workspace_name}/pipe/{pipe_name}/endpoint"

    def _get_workspace_settings_link(self, workspace_id: str) -> str:
        return f"{self._settings['host']}/{workspace_id}/settings"

    def _get_recipient_data(
        self,
        owner_name: str,
        workspace: User,
        user: UserAccount,
        invitation_url: Optional[str] = None,
        workspaces_empty: Optional[str] = None,
        new_role: Optional[str] = None,
        dashboard_url: Optional[str] = None,
    ) -> Dict[str, str]:
        todays_date = date.today()
        workspace_name = workspace.name or workspace.email

        data = {
            "user_email": user.email,
            "workspace_owner": owner_name,
            "workspace_name": workspace_name,
            "host": self._settings["host"],
            "year": todays_date.year,
        }

        if invitation_url:
            data.update({"invitation_url": invitation_url})

        if workspaces_empty:
            data.update({"workspaces_empty": workspaces_empty})

        if new_role:
            data.update({"new_role": new_role})

        if dashboard_url:
            data.update({"dashboard_url": dashboard_url})

        return data

    async def _send_email(self, data: Dict[str, Any]) -> NotificationResponse:
        body = urlencode(data)
        result = await self._http_client.fetch(
            self._url,
            method="POST",
            auth_username=self._auth[0],
            auth_password=self._auth[1],
            body=body,
            raise_error=False,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        return NotificationResponse(
            status_code=int(result.code), content=result.body.decode("utf-8") if result.body else ""
        )

    async def _send_sharing_data_source_changes(
        self,
        to: List[str],
        template: str,
        subject: str,
        data_source_name: str,
        workspace_name: str,
        workspace_url: str,
        data_source_owner_emails: str,
        new_data_source_name: str,
    ) -> NotificationResponse:
        todays_date = date.today()
        recipient_variables = {}
        for email in to:
            recipient_variables[email] = {
                "user_email": email,
                "data_source_name": Resource.sanitize_name(data_source_name),
                "workspace_name": workspace_name,
                "workspace_url": workspace_url,
                "data_source_owner_email": data_source_owner_emails,
                "new_data_source_name": Resource.sanitize_name(new_data_source_name),
                "host": self._settings["host"],
                "year": todays_date.year,
            }

        data = {
            "from": self._from_email,
            "to": ",".join(to),
            "subject": subject,
            "template": template,
            "recipient-variables": json.dumps(recipient_variables),
            "v:user_email": "%recipient.user_email%",
            "v:data_source_name": "%recipient.data_source_name%",
            "v:workspace_name": "%recipient.workspace_name%",
            "v:workspace_url": "%recipient.workspace_url%",
            "v:data_source_owner_email": "%recipient.data_source_owner_email%",
            "v:new_data_source_name": "%recipient.new_data_source_name%",
            "v:host": "%recipent.host%",
            "v:year": "%recipient.year%",
        }

        return await self._send_email(data)

    async def send_add_to_workspace_emails(
        self, owner_name: str, workspace: User, user_emails: List[str]
    ) -> Optional[NotificationResponse]:
        recipient_variables = {}
        workspace_name = workspace.name or workspace.email
        subject = f"{owner_name} has invited you to {workspace_name} at Tinybird"
        template = "workspace_invite"
        invitation_url = self._get_invitation_link(workspace.id)

        for user_email in user_emails:
            user = UserAccounts.get_by_email(user_email)
            recipient_variables[user_email] = self._get_recipient_data(owner_name, workspace, user, invitation_url)

        if not recipient_variables:
            return None

        data = {
            "from": self._from_email,
            "to": ",".join(user_emails),
            "subject": subject,
            "template": template,
            "recipient-variables": json.dumps(recipient_variables),
            "v:user_email": "%recipient.user_email%",
            "v:workspace_owner": "%recipient.workspace_owner%",
            "v:workspace_name": "%recipient.workspace_name%",
            "v:invitation_url": "%recipient.invitation_url%",
            "v:member_exists": "true",
            "v:host": "%recipient.host%",
            "v:year": "%recipient.year%",
        }

        return await self._send_email(data)

    async def send_remove_from_workspace_emails(
        self, owner_name, workspace, user_emails: List[str]
    ) -> NotificationResponse:
        recipient_variables = {}
        workspace_name = workspace.name or workspace.email
        subject = f"Workspace {workspace_name} no longer available"
        template = "workspace_not_available"

        for user_email in user_emails:
            user = UserAccounts.get_by_email(user_email)
            dashboard_url = self._get_user_link(user.id)
            recipient_variables[user_email] = self._get_recipient_data(
                owner_name=owner_name,
                workspace=workspace,
                user=user,
                workspaces_empty="false" if user.number_of_workspaces > 0 else "true",
                dashboard_url=dashboard_url,
            )

        data = {
            "from": self._from_email,
            "to": ",".join(user_emails),
            "subject": subject,
            "template": template,
            "recipient-variables": json.dumps(recipient_variables),
            "v:user_email": "%recipient.user_email%",
            "v:workspace_owner": "%recipient.workspace_owner%",
            "v:workspace_name": "%recipient.workspace_name%",
            "v:workspaces_empty": "%recipient.workspaces_empty%",
            "v:dashboard_url": "%recipient.dashboard_url%",
            "v:host": "%recipient.host%",
            "v:year": "%recipient.year%",
        }

        return await self._send_email(data)

    async def send_change_role_from_workspace_emails(
        self, owner_name, workspace, user_emails: List[str], new_role: str
    ) -> NotificationResponse:
        recipient_variables = {}
        workspace_name = workspace.name or workspace.email
        subject = f"Role changed to '{new_role}' in {workspace_name} Workspace"
        template = "workspace_role_changed"

        for user_email in user_emails:
            user = UserAccounts.get_by_email(user_email)
            dashboard_url = self._get_user_link(user.id)
            recipient_variables[user_email] = self._get_recipient_data(
                owner_name=owner_name, workspace=workspace, user=user, new_role=new_role, dashboard_url=dashboard_url
            )

        data = {
            "from": self._from_email,
            "to": ",".join(user_emails),
            "subject": subject,
            "template": template,
            "recipient-variables": json.dumps(recipient_variables),
            "v:user_email": "%recipient.user_email%",
            "v:workspace_owner": "%recipient.workspace_owner%",
            "v:workspace_name": "%recipient.workspace_name%",
            "v:dashboard_url": "%recipient.dashboard_url%",
            "v:new_role": "%recipient.new_role%",
            "v:host": "%recipient.host%",
            "v:year": "%recipient.year%",
        }

        return await self._send_email(data)

    async def send_notification_on_data_source_shared(
        self, send_to_emails: List[str], new_ds_name: str, dest_workspace_name: str, dest_workspace_id: str
    ) -> NotificationResponse:
        workspace_url = self._get_workspace_link(dest_workspace_id)
        return await self._send_sharing_data_source_changes(
            send_to_emails,
            "data_source_shared",
            f"New shared Data Source: {new_ds_name} is now accessible from your Workspace",
            new_ds_name,
            dest_workspace_name,
            workspace_url,
            "",
            "",
        )

    async def send_notification_on_shared_data_source_unshared(
        self,
        send_to_emails: List[str],
        ds_name: str,
        original_workspace_owner_emails: List[str],
        dest_workspace_id: str,
        dest_workspace_name: str,
    ) -> NotificationResponse:
        workspace_url = self._get_workspace_link(dest_workspace_id)
        owner_emails = ",".join(original_workspace_owner_emails)
        return await self._send_sharing_data_source_changes(
            send_to_emails,
            "data_source_unshared",
            f"Shared Data Source no longer available: {ds_name} is not accessible anymore from your Workspace",
            ds_name,
            dest_workspace_name,
            workspace_url,
            owner_emails,
            "",
        )

    async def send_notification_on_shared_data_source_renamed(
        self,
        send_to_emails: List[str],
        old_ds_name: str,
        new_ds_name: str,
        original_workspace_owner_emails: List[str],
        dest_workspace_id: str,
        dest_workspace_name: str,
    ) -> NotificationResponse:
        workspace_url = self._get_workspace_link(dest_workspace_id)
        owner_emails = ",".join(original_workspace_owner_emails)
        return await self._send_sharing_data_source_changes(
            send_to_emails,
            "data_source_shared_renamed",
            f"Shared Data Source renamed: {old_ds_name} has changed its name",
            old_ds_name,
            dest_workspace_name,
            workspace_url,
            owner_emails,
            new_ds_name,
        )

    async def send_notification_on_created_account(self, user: UserAccount) -> NotificationResponse:
        recipient_variables: Dict[str, Dict[str, Any]] = {}
        user_email = user.email
        todays_date = date.today()

        recipient_variables[user_email] = {
            "user_email": user_email,
            "host": self._settings["host"],
            "year": todays_date.year,
        }

        data = {
            "from": self._from_email,
            "to": user_email,
            "subject": f"Hi {user_email}, welcome to Tinybird!",
            "template": "new_account",
            "recipient-variables": json.dumps(recipient_variables),
            "h:Reply-To": "jorge@tinybird.co",
            "v:email": "%recipient.user_email%",
            "v:host": "%recipient.host%",
            "v:year": "%recipient.year%",
        }

        return await self._send_email(data)

    async def send_max_concurrent_queries_limit(
        self, user_accounts: List[UserAccount], workspace: User, pipes_concurrency: List[Tuple[str, int]]
    ) -> NotificationResponse:
        recipient_variables: Dict[str, Dict[str, Any]] = {}
        todays_date = date.today()
        host = self._settings["host"]
        api_host = self._settings["api_host"]

        def _get_link(pipe_name):
            if pipe_name != "query_api":
                return f"<a href='{self._get_endpoint_link(workspace.name, pipe_name)}' target='_blank'>{pipe_name}</a>"
            else:
                return pipe_name

        pipe_names = "<br>".join(
            set([f"&nbsp;&nbsp;&nbsp;&nbsp; · {_get_link(p[0])} - concurrency: {p[1]}" for p in pipes_concurrency])
        )

        subject = "Concurrent Requests Limited"
        header = "Server is over capacity"
        subheader = ""
        text = f"The {workspace.name} Workspace is experiencing increased timeouts and errors due to high memory usage.<br><br>Maximum concurrent requests have been limited for the following Pipe endpoints:<br><br> {pipe_names} <br><br>If your requests to {api_host}/v0/pipes return HTTP error 429, space your requests using longer intervals.<br><br> This limit will be automatically reversed after 5 minutes, if the issue persists contact us to upgrade your cluster."
        send_to_emails = []
        for user_account in user_accounts:
            user_email = user_account.email
            send_to_emails.append(user_email)
            recipient_variables[user_email] = {
                "text": text,
                "workspace_id": workspace.id,
                "button_text": "Go to Workspace",
                "button_url": self._get_workspace_settings_link(workspace.id),
                "workspace_settings_url": self._get_workspace_settings_link(workspace.id),
                "host": host,
                "year": todays_date.year,
            }

        data = {
            "from": self._from_email,
            "to": ",".join(send_to_emails),
            "subject": subject,
            "template": "ingestion_incident",
            "recipient-variables": json.dumps(recipient_variables),
            "v:header": header,
            "v:subheader": subheader,
            "v:text": "%recipient.text%",
            "v:button_text": "%recipient.button_text%",
            "v:button_url": "%recipient.button_url%",
            "v:workspace_settings_url": "%recipient.workspace_settings_url%",
            "v:host": "%recipient.host%",
            "v:year": "%recipient.year%",
        }

        return await self._send_email(data)

    async def _send_plan_changes(
        self,
        send_to_emails: List[str],
        workspace_id: str,
        workspace_name: str,
        new_plan_name: str,
        old_plan_name: str,
        subject: str,
        template: str,
    ) -> NotificationResponse:
        recipient_variables = {}
        todays_date = date.today()

        for user_email in send_to_emails:
            recipient_variables[user_email] = {
                "user_email": user_email,
                "workspace_id": workspace_id,
                "workspace_name": workspace_name,
                "current_plan_name": new_plan_name,
                "next_plan_name": old_plan_name,
                "host": self._settings["host"],
                "year": todays_date.year,
            }

        data = {
            "from": self._from_email,
            "to": ",".join(send_to_emails),
            "subject": subject,
            "template": template,
            "recipient-variables": json.dumps(recipient_variables),
            "v:user_email": "%recipient.user_email%",
            "v:workspace_id": "%recipient.workspace_id%",
            "v:workspace_name": "%recipient.workspace_name%",
            "v:current_plan_name": "%recipient.current_plan_name%",
            "v:next_plan_name": "%recipient.next_plan_name%",
            "v:host": "%recipient.host%",
            "v:year": "%recipient.year%",
        }
        return await self._send_email(data)

    async def send_notification_on_plan_upgraded(
        self, send_to_emails: List[str], workspace_name: str, workspace_id: str, new_plan_name: str, old_plan_name: str
    ) -> NotificationResponse:
        subject = f"Your account has been successfully upgraded to {new_plan_name}"
        template = "plan_upgrade"
        return await self._send_plan_changes(
            send_to_emails, workspace_id, workspace_name, new_plan_name, old_plan_name, subject, template
        )

    async def send_notification_on_plan_downgraded(
        self, send_to_emails: List[str], workspace_name: str, workspace_id: str, new_plan_name: str, old_plan_name: str
    ) -> NotificationResponse:
        subject = f"Your account has been successfully downgraded to {new_plan_name}"
        template = "plan_downgrade"
        return await self._send_plan_changes(
            send_to_emails, workspace_id, workspace_name, new_plan_name, old_plan_name, subject, template
        )

    async def send_notification_on_build_plan_limits(
        self,
        send_to_emails: List[str],
        workspace_id: str,
        workspace_name: str,
        quantity_api_requests_per_day: Optional[int],
        max_api_requests_per_day: int,
        quantity_gb_storage_used: Optional[float],
        max_gb_storage_used: int,
        processed_price: float,
        storage_price: float,
        exceeded: bool,
        quantity_gb_processed: Optional[int],
    ) -> NotificationResponse:
        if exceeded:
            subject = f"The workspace {workspace_name} has exceeded its limits."
            template = "exceeded_limits"
        else:
            subject = f"The workspace {workspace_name} is reaching its limits."
            template = "reaching_limits"

        recipient_variables = {}
        todays_date = date.today()

        quantity_gb_storage_used = round(quantity_gb_storage_used, 1) if quantity_gb_storage_used is not None else 0
        quantity_api_requests_per_day = quantity_api_requests_per_day or 0
        quantity_gb_processed = quantity_gb_processed or 0
        total_price = quantity_gb_processed * processed_price + quantity_gb_storage_used * storage_price
        workspace_url = self._get_workspace_link(workspace_id)

        for user_email in send_to_emails:
            recipient_variables[user_email] = {
                "user_email": user_email,
                "workspace_id": workspace_id,
                "workspace_name": workspace_name,
                "workspace_url": workspace_url,
                "max_api_requests_per_day": "{:,}".format(max_api_requests_per_day),
                "max_gb_storage_used": "{:,}".format(max_gb_storage_used),
                "processed_price": processed_price,
                "storage_price": storage_price,
                "host": self._settings["host"],
                "year": todays_date.year,
                "quantity_api_requests_per_day": "{:,}".format(quantity_api_requests_per_day),
                "quantity_gb_storage_used": "{:,}".format(quantity_gb_storage_used),
                "quantity_gb_processed": "{:,}".format(quantity_gb_processed),
                "total_price": "{:,.2f}".format(total_price),
            }

        data = {
            "from": self._from_email,
            "to": ",".join(send_to_emails),
            "subject": subject,
            "template": template,
            "recipient-variables": json.dumps(recipient_variables),
            "v:user_email": "%recipient.user_email%",
            "v:workspace_id": "%recipient.workspace_id%",
            "v:workspace_name": "%recipient.workspace_name%",
            "v:workspace_url": "%recipient.workspace_url%",
            "v:max_api_requests_per_day": "%recipient.max_api_requests_per_day%",
            "v:max_gb_storage_used": "%recipient.max_gb_storage_used%",
            "v:processed_price": "%recipient.processed_price%",
            "v:storage_price": "%recipient.storage_price%",
            "v:host": "%recipient.host%",
            "v:year": "%recipient.year%",
            "v:quantity_api_requests_per_day": "%recipient.quantity_api_requests_per_day%",
            "v:quantity_gb_storage_used": "%recipient.quantity_gb_storage_used%",
            "v:quantity_gb_processed": "%recipient.quantity_gb_processed%",
            "v:total_price": "%recipient.total_price%",
        }

        return await self._send_email(data)

    async def send_notification_on_ingestion_incident(
        self, send_to_emails: List[str], workspace: User, datasource: Datasource, incident: dict
    ) -> NotificationResponse:
        recipient_variables = {}
        todays_date = date.today()
        workspace_id = workspace.id
        datasource_id = datasource.id
        for user_email in send_to_emails:
            header, subheader, text, button_text = _extract_error_details(
                incident.get("errors", []), user_email, Resource.sanitize_name(datasource.name)
            )
            if not header or not subheader or not text or not button_text:
                return NotificationResponse(status_code=0, content="")
            subject = f"{header} {subheader}"
            recipient_variables[user_email] = {
                "text": text,
                "workspace_id": workspace_id,
                "button_text": button_text,
                "button_url": self._get_datasource_log_link(workspace_id, datasource_id),
                "workspace_settings_url": self._get_workspace_settings_link(workspace_id),
                "host": self._settings["host"],
                "year": todays_date.year,
            }

        data = {
            "from": self._from_email,
            "to": ",".join(send_to_emails),
            "subject": subject,
            "template": "ingestion_incident",
            "recipient-variables": json.dumps(recipient_variables),
            "v:header": header,
            "v:subheader": subheader,
            "v:text": "%recipient.text%",
            "v:button_text": "%recipient.button_text%",
            "v:button_url": "%recipient.button_url%",
            "v:workspace_settings_url": "%recipient.workspace_settings_url%",
            "v:host": "%recipient.host%",
            "v:year": "%recipient.year%",
        }

        return await self._send_email(data)

    async def send_notification_on_quarantine_incident(
        self, send_to_emails: List[str], workspace: User, datasource: Datasource, incident: dict
    ) -> NotificationResponse:
        recipient_variables = {}
        row_count = int(incident["rows"])
        import_count = int(incident["imports"])
        rows = f"{row_count:,}"
        imports = f"{import_count:,}"
        header = f"We quarantined {row_count:,} {'row' if row_count == 1 else 'rows'}"
        subheader = f" from your last {'import' if import_count == 1 else f'{import_count:,} imports'}"
        for user_email in send_to_emails:
            recipient_variables[user_email] = {
                "header": header,
                "subheader": subheader,
                "user_email": user_email,
                "data_source_name": Resource.sanitize_name(datasource.name),
                "data_source_url": self._get_datasource_link(workspace.id, datasource.id),
                "workspace_name": workspace.name,
                "workspace_initials": workspace.name[:2],
                "workspace_settings_url": self._get_workspace_settings_link(workspace.id),
                "workspace_color": workspace.color.replace("#", ""),
                "rows": rows,
                "imports": imports,
                "timeline": _extract_quarantine_timeline(incident.get("timeline", []), import_count),
            }

        data = {
            "from": self._from_email,
            "to": ",".join(send_to_emails),
            "subject": f"{header}{subheader}",
            "template": "quarantine_incident",
            "recipient-variables": json.dumps(recipient_variables),
            "v:header": "%recipient.header%",
            "v:subheader": "%recipient.subheader%",
            "v:user_email": "%recipient.user_email%",
            "v:data_source_name": "%recipient.data_source_name%",
            "v:data_source_url": "%recipient.data_source_url%",
            "v:workspace_settings_url": "%recipient.workspace_settings_url%",
            "v:workspace_name": "%recipient.workspace_name%",
            "v:workspace_initials": "%recipient.workspace_initials%",
            "v:workspace_color": "%recipient.workspace_color%",
            "v:rows": "%recipient.rows%",
            "v:imports": "%recipient.imports%",
            "v:timeline": "%recipient.timeline%",
        }

        return await self._send_email(data)
