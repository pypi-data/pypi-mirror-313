import click

from tinybird.user import User as Workspace
from tinybird.user import UserDoesNotExist, Users

from ... import common
from ..cli_base import cli


@cli.command()
@click.option("--ws-name")
@click.option("--rl-name")
@click.option("--rl-count", type=int)
@click.option("--rl-period", type=int)
@click.option("--rl-max-burst", type=int)
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
def set_rate_limit_config(ws_name, rl_name, rl_count, rl_period, rl_max_burst, config):
    """Change rate limits from a workspace"""
    common.setup_redis_client(config)

    try:
        ws = Users.get_by_name(ws_name)
    except UserDoesNotExist:
        click.echo(f"Workspace {ws_name} doesn't exists")
    else:
        with Workspace.transaction(ws.id) as u:
            u.set_rate_limit_config(rl_name, rl_count, rl_period, rl_max_burst)


@cli.command()
@click.option("--ws-name")
@click.option("--limit-name")
@click.option("--limit-prefix")
@click.option("--limit-value")
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
def set_raw_limit(ws_name, limit_name, limit_prefix, limit_value, config):
    # Untested, don't use me in production
    """Change rate limits from a workspace"""
    common.setup_redis_client(config)

    try:
        ws = Users.get_by_name(ws_name)
    except UserDoesNotExist:
        click.echo(f"Workspace {ws_name} doesn't exists")
    else:
        with Workspace.transaction(ws.id) as u:
            u.set_user_limit(limit_name, float(limit_value), limit_prefix)
        click.echo(f"Workspace {ws_name} limit changed {(limit_name, limit_value, limit_prefix)}")
