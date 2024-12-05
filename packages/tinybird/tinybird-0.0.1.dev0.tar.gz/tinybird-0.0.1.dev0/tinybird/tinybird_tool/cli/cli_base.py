import logging

import click

logger = logging.getLogger(__name__)
log_formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
log_handler = logging.StreamHandler()
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)
logger.setLevel(logging.DEBUG)


@click.group()
@click.version_option()
def cli():
    """
    tinybird
    """
