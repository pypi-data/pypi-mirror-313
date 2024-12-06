import time

import click
import requests

import docker
from tinybird.feedback_manager import FeedbackManager
from tinybird.tb_cli_modules.common import CLIException
from tinybird.tb_cli_modules.config import CLIConfig

# TODO: Use the official Tinybird image once it's available 'tinybirdco/tinybird-local:latest'
TB_IMAGE_NAME = "registry.gitlab.com/tinybird/analytics/tinybird-local-jammy-3.11:latest"
TB_CONTAINER_NAME = "tinybird-local"
TB_LOCAL_PORT = 80
TB_LOCAL_HOST = f"http://localhost:{TB_LOCAL_PORT}"


def start_tinybird_local(
    docker_client,
):
    """Start the Tinybird container."""
    containers = docker_client.containers.list(all=True, filters={"name": TB_CONTAINER_NAME})
    if containers:
        # Container `start` is idempotent. It's safe to call it even if the container is already running.
        container = containers[0]
        container.start()
    else:
        pull_required = False
        try:
            local_image = docker_client.images.get(TB_IMAGE_NAME)
            local_image_id = local_image.attrs["RepoDigests"][0].split("@")[1]
            remote_image = docker_client.images.get_registry_data(TB_IMAGE_NAME)
            pull_required = local_image_id != remote_image.id
        except Exception:
            pull_required = True

        if pull_required:
            click.echo(
                FeedbackManager.info(message="** Downloading latest version of Tinybird development environment...")
            )
            docker_client.images.pull(TB_IMAGE_NAME, platform="linux/amd64")

        container = docker_client.containers.run(
            TB_IMAGE_NAME,
            name=TB_CONTAINER_NAME,
            detach=True,
            ports={"80/tcp": TB_LOCAL_PORT},
            remove=False,
            platform="linux/amd64",
        )

    click.echo(FeedbackManager.info(message="** Waiting for Tinybird development environment to be ready..."))
    for attempt in range(10):
        try:
            run = container.exec_run("tb --no-version-warning sql 'SELECT 1 AS healthcheck' --format json").output
            # dont parse the json as docker sometimes returns warning messages
            # todo: rafa, make this rigth
            if b'"healthcheck": 1' in run:
                break
            raise RuntimeError("Unexpected response from Tinybird")
        except Exception:
            if attempt == 9:  # Last attempt
                raise CLIException("Tinybird local environment not ready yet. Please try again in a few seconds.")
            time.sleep(5)  # Wait 5 seconds before retrying


def get_docker_client():
    """Check if Docker is installed and running."""
    try:
        client = docker.from_env()
        client.ping()
        return client
    except Exception:
        raise CLIException("Docker is not running or installed. Please ensure Docker is installed and running.")


def stop_tinybird_local(docker_client):
    """Stop the Tinybird container."""
    try:
        container = docker_client.containers.get(TB_CONTAINER_NAME)
        container.stop()
    except Exception:
        pass


def remove_tinybird_local(docker_client):
    """Remove the Tinybird container."""
    try:
        container = docker_client.containers.get(TB_CONTAINER_NAME)
        container.remove(force=True)
    except Exception:
        pass


def set_up_tinybird_local(docker_client):
    """Set up the Tinybird local environment."""
    start_tinybird_local(docker_client)
    return get_tinybird_local_client()


def get_tinybird_local_client():
    """Get a Tinybird client connected to the local environment."""
    config = CLIConfig.get_project_config()
    tokens = requests.get(f"{TB_LOCAL_HOST}/tokens").json()
    token = tokens["workspace_admin_token"]
    config.set_token(token)
    config.set_host(TB_LOCAL_HOST)
    return config.get_client(host=TB_LOCAL_HOST, token=token)
