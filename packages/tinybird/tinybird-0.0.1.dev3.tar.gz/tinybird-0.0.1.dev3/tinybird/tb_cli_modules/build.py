import asyncio
import json
import os
import time
from pathlib import Path
from typing import Any, Awaitable, Callable, Dict, List, Union

import click
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

import tinybird.context as context
from tinybird.client import TinyB
from tinybird.config import FeatureFlags
from tinybird.datafile import (
    ParseException,
    folder_build,
    get_project_filenames,
    has_internal_datafiles,
    parse_datasource,
    parse_pipe,
)
from tinybird.feedback_manager import FeedbackManager, info_highlight_message, success_message
from tinybird.tb_cli_modules.cli import cli
from tinybird.tb_cli_modules.common import (
    coro,
    echo_safe_humanfriendly_tables_format_smart_table,
)
from tinybird.tb_cli_modules.create import generate_sample_data_from_columns
from tinybird.tb_cli_modules.local import (
    get_docker_client,
    get_tinybird_local_client,
    remove_tinybird_local,
    start_tinybird_local,
    stop_tinybird_local,
)


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, filenames: List[str], process: Callable[[List[str]], None]):
        self.filenames = filenames
        self.process = process

    def on_modified(self, event: Any) -> None:
        if not event.is_directory and any(event.src_path.endswith(ext) for ext in [".datasource", ".pipe"]):
            filename = event.src_path.split("/")[-1]
            click.echo(info_highlight_message(f"\n⟲ Changes detected in {filename}\n")())
            try:
                self.process([event.src_path])
            except Exception as e:
                click.echo(FeedbackManager.error_exception(error=e))


def watch_files(
    filenames: List[str],
    process: Union[Callable[[List[str]], None], Callable[[List[str]], Awaitable[None]]],
) -> None:
    # Handle both sync and async process functions
    async def process_wrapper(files: List[str]) -> None:
        click.echo("⚡ Rebuilding...")
        time_start = time.time()
        if asyncio.iscoroutinefunction(process):
            await process(files, watch=True)
        else:
            process(files, watch=True)
        time_end = time.time()
        elapsed_time = time_end - time_start
        click.echo(success_message(f"\n✓ Rebuild completed in {elapsed_time:.1f}s")())

    event_handler = FileChangeHandler(filenames, lambda f: asyncio.run(process_wrapper(f)))
    observer = Observer()

    # Watch each provided path
    for filename in filenames:
        path = filename if os.path.isdir(filename) else os.path.dirname(filename)
        observer.schedule(event_handler, path=path, recursive=True)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


@cli.command()
@click.option(
    "--folder",
    default=".",
    help="Folder from where to execute the command. By default the current folder",
    hidden=True,
    type=click.types.STRING,
)
@click.option(
    "--watch",
    is_flag=True,
    help="Watch for changes in the files and re-check them.",
)
@click.option(
    "--restart",
    is_flag=True,
    help="Restart the Tinybird development environment before building the first time.",
)
@coro
async def build(
    folder: str,
    watch: bool,
    restart: bool,
) -> None:
    """
    Watch for changes in the files and re-check them.
    """
    docker_client = get_docker_client()
    if restart:
        remove_tinybird_local(docker_client)
        start_tinybird_local(docker_client)
    ignore_sql_errors = FeatureFlags.ignore_sql_errors()
    context.disable_template_security_validation.set(True)
    is_internal = has_internal_datafiles(folder)
    tb_client = get_tinybird_local_client()
    workspaces: List[Dict[str, Any]] = (await tb_client.user_workspaces_and_branches()).get("workspaces", [])
    datasources: List[Dict[str, Any]] = await tb_client.datasources()
    pipes: List[Dict[str, Any]] = await tb_client.pipes(dependencies=True)

    def check_filenames(filenames: List[str]):
        parser_matrix = {".pipe": parse_pipe, ".datasource": parse_datasource}
        incl_suffix = ".incl"

        for filename in filenames:
            if os.path.isdir(filename):
                process(filenames=get_project_filenames(filename))

            file_suffix = Path(filename).suffix
            if file_suffix == incl_suffix:
                continue

            parser = parser_matrix.get(file_suffix)
            if not parser:
                raise ParseException(FeedbackManager.error_unsupported_datafile(extension=file_suffix))

            parser(filename)

    async def process(filenames: List[str], watch: bool = False, only_pipes: bool = False):
        check_filenames(filenames=filenames)
        await folder_build(
            tb_client,
            workspaces,
            datasources,
            pipes,
            filenames,
            ignore_sql_errors=ignore_sql_errors,
            is_internal=is_internal,
            only_pipes=only_pipes,
        )

        for filename in filenames:
            if filename.endswith(".datasource"):
                ds_path = Path(filename)
                ds_name = ds_path.stem
                datasource_content = ds_path.read_text()
                sample_data = await generate_sample_data_from_columns(tb_client, datasource_content)
                ndjson_data = "\n".join([json.dumps(row) for row in sample_data])
                await tb_client.datasource_events(ds_name, ndjson_data)

        if watch:
            filename = filenames[0]
            if filename.endswith(".pipe"):
                await build_and_print_pipe(tb_client, filename)

    filenames = get_project_filenames(folder)

    async def build_once(filenames: List[str]):
        try:
            click.echo("⚡ Building project...")
            time_start = time.time()
            await process(filenames=filenames, watch=False)
            time_end = time.time()
            elapsed_time = time_end - time_start
            click.echo(FeedbackManager.success(message=f"\n✓ Build completed in {elapsed_time:.1f}s\n"))
        except Exception as e:
            click.echo(FeedbackManager.error(message=str(e)))

    await build_once(filenames)

    if watch:
        click.echo(FeedbackManager.highlight(message="◎ Watching for changes..."))
        watch_files(filenames, process)


async def build_and_print_pipe(tb_client: TinyB, filename: str):
    pipe_name = os.path.basename(filename.split(".")[0])
    res = await tb_client.query(f"SELECT * FROM {pipe_name} LIMIT 5 FORMAT JSON", pipeline=pipe_name)
    data = []
    for d in res["data"]:
        data.append(d.values())
    meta = res["meta"]
    column_names = [col["name"] for col in meta]
    echo_safe_humanfriendly_tables_format_smart_table(data, column_names=column_names)


@cli.command()
@coro
async def stop() -> None:
    """Stop Tinybird development environment"""
    click.echo(FeedbackManager.info(message="Shutting down Tinybird development environment..."))
    docker_client = get_docker_client()
    stop_tinybird_local(docker_client)
    click.echo(FeedbackManager.success(message="Tinybird development environment stopped"))


@cli.command()
@coro
async def start() -> None:
    """Start Tinybird development environment"""
    click.echo(FeedbackManager.info(message="Starting Tinybird development environment..."))
    docker_client = get_docker_client()
    start_tinybird_local(docker_client)
    click.echo(FeedbackManager.success(message="Tinybird development environment started"))
