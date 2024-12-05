import click

# isort: off
# initialize_ansible_environment must be imported before any ansible modules are imported!
from .initialize_ansible_environment import initialize_ansible_environment  # noqa: F401

# isort: on

from .clickhouse.cli import clickhouse_group
from .main import (
    deprovision_alerts,
    fix_zk_metadata,
    gatherer_apply_config,
    platform_lock,
    provision_alerts,
    resize_aws_server_disk,
    resize_azure_server_disk,
    resize_gcp_server_disk,
    restart_vm,
)
from .utils import CONTEXT_SETTINGS


@click.group(context_settings=CONTEXT_SETTINGS)
def cli() -> None:
    """
    A colibri to help with your Tinybird plataforming tasks
    """
    pass


cli.add_command(clickhouse_group, name="clickhouse")
cli.add_command(deprovision_alerts, name="deprovision-alerts")
cli.add_command(provision_alerts, name="provision-alerts")
cli.add_command(restart_vm, name="restart-vm")
cli.add_command(fix_zk_metadata, name="fix-zk-metadata")
cli.add_command(resize_aws_server_disk, name="resize-aws-server-disk")
cli.add_command(resize_gcp_server_disk, name="resize-gcp-server-disk")
cli.add_command(resize_azure_server_disk, name="resize-azure-server-disk")
cli.add_command(gatherer_apply_config, name="gatherer-apply-config")
cli.add_command(platform_lock, name="platform-lock")


if __name__ == "__main__":
    cli()
