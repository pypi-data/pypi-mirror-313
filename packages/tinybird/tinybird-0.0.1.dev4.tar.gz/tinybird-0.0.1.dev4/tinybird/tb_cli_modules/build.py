import asyncio
import os
import random
import time
from pathlib import Path
from typing import Any, Awaitable, Callable, Dict, List, Union

import click
import humanfriendly
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
from tinybird.feedback_manager import FeedbackManager, bcolors
from tinybird.tb_cli_modules.cli import cli
from tinybird.tb_cli_modules.common import (
    coro,
)
from tinybird.tb_cli_modules.config import CLIConfig
from tinybird.tb_cli_modules.llm import LLM
from tinybird.tb_cli_modules.local import (
    get_tinybird_local_client,
)
from tinybird.tb_cli_modules.table import format_table


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, filenames: List[str], process: Callable[[List[str]], None]):
        self.filenames = filenames
        self.process = process

    def on_modified(self, event: Any) -> None:
        if not event.is_directory and any(event.src_path.endswith(ext) for ext in [".datasource", ".pipe"]):
            filename = event.src_path.split("/")[-1]
            click.echo(FeedbackManager.highlight(message=f"\n⟲ Changes detected in {filename}\n"))
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
        click.echo(
            FeedbackManager.success(message="\n✓ ")
            + FeedbackManager.gray(message=f"Rebuild completed in {elapsed_time:.1f}s")
        )

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
    "--skip-datasources",
    is_flag=True,
    help="Skip rebuilding datasources.",
)
@coro
async def build(
    folder: str,
    watch: bool,
    skip_datasources: bool,
) -> None:
    """
    Watch for changes in the files and re-check them.
    """
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
            if filename.endswith(".datasource") and not skip_datasources:
                ds_path = Path(filename)
                ds_name = ds_path.stem
                datasource_content = ds_path.read_text()
                llm_config = CLIConfig.get_llm_config()
                llm = LLM(key=llm_config["api_key"])
                has_json_path = "`json:" in datasource_content

                if has_json_path:
                    await llm.generate_sql_sample_data(
                        tb_client=tb_client,
                        datasource_name=ds_name,
                        datasource_content=datasource_content,
                    )

        if watch:
            filename = filenames[0]
            if filename.endswith(".pipe"):
                await build_and_print_pipe(tb_client, filename)

    filenames = get_project_filenames(folder)

    async def build_once(filenames: List[str]):
        try:
            click.echo("⚡ Building project...")
            time_start = time.time()
            await process(filenames=filenames, watch=False, only_pipes=skip_datasources)
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
    rebuild_colors = [bcolors.FAIL, bcolors.OKBLUE, bcolors.WARNING, bcolors.OKGREEN, bcolors.HEADER]
    rebuild_index = random.randint(0, len(rebuild_colors) - 1)
    rebuild_color = rebuild_colors[rebuild_index % len(rebuild_colors)]
    pipe_name = Path(filename).stem
    res = await tb_client.query(f"SELECT * FROM {pipe_name} FORMAT JSON", pipeline=pipe_name)
    data = []
    limit = 5
    for d in res["data"][:5]:
        data.append(d.values())
    meta = res["meta"]
    row_count = res.get("rows", 0)
    stats = res.get("statistics", {})
    elapsed = stats.get("elapsed", 0)
    node_name = "endpoint"
    cols = len(meta)
    try:

        def print_message(message: str, color=bcolors.CGREY):
            return f"{color}{message}{bcolors.ENDC}"

        table = format_table(data, meta)
        colored_char = print_message("│", rebuild_color)
        table_with_marker = "\n".join(f"{colored_char} {line}" for line in table.split("\n"))
        click.echo(f"\n{colored_char} {print_message('⚡', rebuild_color)} Running {pipe_name} → {node_name}")
        click.echo(colored_char)
        click.echo(table_with_marker)
        click.echo(colored_char)
        rows_read = humanfriendly.format_number(stats.get("rows_read", 0))
        bytes_read = humanfriendly.format_size(stats.get("bytes_read", 0))
        elapsed = humanfriendly.format_timespan(elapsed) if elapsed >= 1 else f"{elapsed * 1000:.2f}ms"
        stats_message = f"» {bytes_read} ({rows_read} rows x {cols} cols) in {elapsed}"
        rows_message = f"» Showing {limit} first rows" if row_count > limit else "» Showing all rows"
        click.echo(f"{colored_char} {print_message(stats_message, bcolors.OKGREEN)}")
        click.echo(f"{colored_char} {print_message(rows_message, bcolors.CGREY)}")
    except ValueError as exc:
        if str(exc) == "max() arg is an empty sequence":
            click.echo("------------")
            click.echo("Empty")
            click.echo("------------")
        else:
            raise exc
