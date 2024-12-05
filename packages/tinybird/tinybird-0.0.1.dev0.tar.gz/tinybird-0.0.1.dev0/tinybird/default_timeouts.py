DEFAULT_SOCKET_TOTAL_TIMEOUT: int = 30 * 60
DEFAULT_SOCKET_CONNECT_TIMEOUT: int = 60
DEFAULT_SOCKET_READ_TIMEOUT: int = 60


def set_socket_total_timeout(value: int) -> None:
    global DEFAULT_SOCKET_TOTAL_TIMEOUT
    DEFAULT_SOCKET_TOTAL_TIMEOUT = value


def socket_total_timeout() -> int:
    return DEFAULT_SOCKET_TOTAL_TIMEOUT


def set_socket_connect_timeout(value: int) -> None:
    global DEFAULT_SOCKET_CONNECT_TIMEOUT
    DEFAULT_SOCKET_CONNECT_TIMEOUT = value


def socket_connect_timeout() -> int:
    return DEFAULT_SOCKET_CONNECT_TIMEOUT


def set_socket_read_timeout(value: int) -> None:
    global DEFAULT_SOCKET_READ_TIMEOUT
    DEFAULT_SOCKET_READ_TIMEOUT = value


def socket_read_timeout() -> int:
    return DEFAULT_SOCKET_READ_TIMEOUT
