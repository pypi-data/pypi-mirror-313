from collections import namedtuple
from typing import Callable

RequestError = namedtuple("RequestError", ("status_code", "message"))


class RequestErrorException(Exception):
    def __init__(self, request_error: RequestError):
        self.request_error = request_error
        super().__init__(request_error.message)


def request_error(status_code: int, message: str) -> Callable[..., RequestError]:
    def formatter(**kwargs):
        return RequestError(status_code, message.format(**kwargs))

    return formatter


def parse_error(message: str) -> Callable[..., str]:
    def formatter(**kwargs):
        return f"{message.format(**kwargs)}"

    return formatter


def parse_api_cli_error(api_message, cli_message, ui_message):
    def formatter(**kwargs):
        is_cli = kwargs.get("is_cli", False)
        is_from_ui = kwargs.get("is_from_ui", False)
        message = ui_message if is_from_ui else cli_message if is_cli else api_message
        return f"{message.format(**kwargs)}"

    return formatter
