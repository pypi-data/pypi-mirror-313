from datetime import datetime

from click import secho, style


def preprocess_message(msg: str, color: str | None = None, bgColor: str | None = None) -> str:
    """Adds bold style to strings"""
    if not isinstance(msg, str):
        msg = str(msg)

    parts = msg.split("**")

    i = 0
    while i < len(parts):
        if i % 2 == 1:
            parts[i] = style(parts[i], bold=True, reset=False)
        else:
            parts[i] = style(parts[i], bold=False, reset=False)
        i += 1
    log_time = datetime.now().strftime("%H:%M:%S") + "  "
    return style(log_time + "".join(parts), fg=color, bg=bgColor)


def log_info(msg: str, color: str | None = None) -> None:
    secho(f"* {preprocess_message(msg, color)}")


def log_header(msg: str) -> None:
    secho(f"# {preprocess_message(msg, 'bright_blue')}")


def log_success(msg: str) -> None:
    secho(f"# {preprocess_message(msg, 'green')}")


def log_warning(msg: str) -> None:
    secho(f"[WARNING] {preprocess_message(msg, 'yellow', 'black')}", err=True)


def log_error(msg: str) -> None:
    if "**" not in msg:
        msg = f"**{msg}**"

    secho(f"[ERROR] {preprocess_message(msg, 'red')}", err=True)
