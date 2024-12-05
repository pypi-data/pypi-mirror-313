from tinybird.views.api_errors import request_error


class JobFilterError:
    invalid_date_format = request_error(400, "The date provided is an {error}")
