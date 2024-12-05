from collections import namedtuple

from tinybird.views.api_errors.datasources import ClientErrorBadRequest
from tinybird.views.base import ApiHTTPError

CSVDialect = namedtuple(
    "CSVDialect",
    [
        "delimiter",
        "escapechar",
        "new_line",
    ],
)


def dialect_from_handler(handler):
    delimiter = handler.get_argument("dialect_delimiter", None, strip=False)
    escapechar = handler.get_argument("dialect_escapechar", None, strip=False)
    new_line = handler.get_argument("dialect_new_line", None, strip=False)
    if delimiter is not None and len(delimiter) != 1:
        if "t" in delimiter:
            raise ApiHTTPError.from_request_error(
                ClientErrorBadRequest.dialect_invalid_delimiter_tab_suggestion(component="delimiter")
            )
        raise ApiHTTPError.from_request_error(ClientErrorBadRequest.dialect_invalid_length(component="delimiter"))

    if escapechar is not None and len(escapechar) != 1:
        raise ApiHTTPError.from_request_error(ClientErrorBadRequest.dialect_invalid_length(component="escapechar"))

    if new_line is not None and len(new_line) > 2:
        raise ApiHTTPError.from_request_error(ClientErrorBadRequest.dialect_invalid_length(component="new_line"))

    return CSVDialect(delimiter=delimiter, escapechar=escapechar, new_line=new_line)
