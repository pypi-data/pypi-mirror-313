import json
import sys

import click

from tinybird.user import User as Workspace

from ... import common
from ..cli_base import cli


@cli.command()
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
@click.option("--token", type=str, help="Internal workspace token in eu-shared")
@click.option("--output-file", type=click.Path(exists=False), help="output file, example: --output-file=./nodes.json")
def get_all_nodes(config, token, output_file):
    """Gets the sql queries of all nodes"""
    common.setup_redis_client(config=config)

    if not token:
        click.secho("ERROR: Provide r@localhost Internal workspace token", fg="red")
        sys.exit(1)

    all_nodes = []
    for workspace in Workspace.get_all(include_branches=True, include_releases=True):
        try:
            pipes = workspace.get_pipes()
            click.secho(f"** Workspace '{workspace.id}' {len(pipes)} pipes", fg="blue")
            for pipe in pipes:
                for node in pipe.pipeline.nodes:
                    all_nodes.append(
                        {
                            "workspace_id": workspace.id,
                            "pipe_id": pipe.id,
                            "node_id": node.id,
                            "sql": node.sql,
                            "params": node.template_params,
                        }
                    )
        except Exception as e:
            import traceback

            traceback.print_exc()
            click.secho(f"** error: {e}")
    click.secho(f"** Collected '{len(all_nodes)}' nodes", fg="blue")
    with open(output_file, "a") as output:
        output.write("\n".join(json.dumps(n) for n in all_nodes))


@cli.command()
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
def get_multiple_output(config):
    """Lists pipes with more than one node materialized or more than one output (matview + endpoint)"""
    output_file_mat = "/tmp/get_multiple_mat"
    output_file_endpoint = "/tmp/get_multiple_endpoint"
    common.setup_redis_client(config=config)

    all_mat_nodes = []
    all_multiple_output_pipes = []

    for workspace in Workspace.get_all(include_branches=True, include_releases=True):
        try:
            pipes = workspace.get_pipes()
            click.secho(f"** Workspace '{workspace.id}' {len(pipes)} pipes", fg="blue")
            for pipe in pipes:
                count = 0
                for node in pipe.pipeline.nodes:
                    if node.materialized:
                        count += 1
                if count and pipe.is_published():
                    all_multiple_output_pipes.append(
                        {
                            "workspace_id": workspace.id,
                            "workspace_name": workspace.name,
                            "pipe_id": pipe.id,
                            "pipe_name": pipe.name,
                        }
                    )
                if count > 1:
                    all_mat_nodes.append(
                        {
                            "workspace_id": workspace.id,
                            "workspace_name": workspace.name,
                            "pipe_id": pipe.id,
                            "pipe_name": pipe.name,
                        }
                    )
        except Exception as e:
            import traceback

            traceback.print_exc()
            click.secho(f"** error: {e}")

    click.secho(f"** Collected '{len(all_mat_nodes)}' pipes with more than one matview", fg="blue")
    click.secho(
        f"** Collected '{len(all_multiple_output_pipes)}' pipes with more than one output (matview + endpoint)",
        fg="blue",
    )

    with open(output_file_mat, "a") as output:
        output.write("\n".join(json.dumps(n) for n in all_mat_nodes))
    with open(output_file_endpoint, "a") as output:
        output.write("\n".join(json.dumps(n) for n in all_multiple_output_pipes))
