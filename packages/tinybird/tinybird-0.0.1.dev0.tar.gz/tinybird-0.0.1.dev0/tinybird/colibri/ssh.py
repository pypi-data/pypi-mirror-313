import pathlib
import random
import time
from functools import cache

from ansible.inventory.host import Host
from fabric import Config, Connection
from fabric.config import SSHConfig
from paramiko import ChannelException


@cache
def get_ssh_config() -> SSHConfig:
    return SSHConfig.from_path(pathlib.Path.home() / ".ssh/bastion_ssh_config")


@cache
def get_connection(host: Host | str) -> Connection:
    conn = Connection(str(host), config=Config(ssh_config=get_ssh_config()))
    # https://github.com/pyinvoke/invoke/issues/774#issuecomment-2023810087
    # remove when https://github.com/pyinvoke/invoke/pull/983 is merged
    conn.config.runners.remote.input_sleep = 0
    return conn


def run_ssh_command(host: Host | str, cmd: str, timeout: int = 300) -> tuple[int, str, str]:
    conn = get_connection(host)

    # run command with exponential backoff
    retry_delay = 1.0
    for _attempt in range(5):
        try:
            result = conn.run(cmd, timeout=timeout, hide="both", warn=True)
            break  # https://gitlab.com/tinybird/analytics/-/issues/16274
        except ChannelException as exception:
            if exception.text == "Connect failed":
                time.sleep(retry_delay)
                retry_delay *= 2
                retry_delay += random.uniform(0, 1)
            else:
                raise exception

    return result.return_code, result.stdout, result.stderr
