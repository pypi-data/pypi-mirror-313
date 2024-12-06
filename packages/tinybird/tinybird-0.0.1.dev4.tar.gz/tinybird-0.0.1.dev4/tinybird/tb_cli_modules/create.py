import os
from os import getcwd
from pathlib import Path
from typing import Any, Dict, List, Optional

import click
from click import Context

from tinybird.client import TinyB
from tinybird.datafile import folder_build
from tinybird.feedback_manager import FeedbackManager
from tinybird.tb_cli_modules.cli import cli
from tinybird.tb_cli_modules.common import _generate_datafile, coro, generate_datafile, push_data
from tinybird.tb_cli_modules.config import CLIConfig
from tinybird.tb_cli_modules.exceptions import CLIDatasourceException
from tinybird.tb_cli_modules.llm import LLM
from tinybird.tb_cli_modules.local import (
    get_tinybird_local_client,
)


@cli.command()
@click.option(
    "--data",
    type=click.Path(exists=True),
    default=None,
    help="Initial data to be used to create the project",
)
@click.option(
    "--prompt",
    type=str,
    default=None,
    help="Prompt to be used to create the project",
)
@click.option(
    "--folder",
    default=None,
    type=click.Path(exists=True, file_okay=False),
    help="Folder where datafiles will be placed",
)
@click.pass_context
@coro
async def create(
    ctx: Context,
    data: Optional[str],
    prompt: Optional[str],
    folder: Optional[str],
) -> None:
    """Initialize a new project."""
    click.echo(FeedbackManager.gray(message="Setting up Tinybird Local"))
    folder = folder or getcwd()
    try:
        tb_client = get_tinybird_local_client()
        click.echo(FeedbackManager.gray(message="Creating new project structure..."))
        await project_create(tb_client, data, prompt, folder)
        click.echo(FeedbackManager.success(message="✓ Scaffolding completed!\n"))
        workspaces: List[Dict[str, Any]] = (await tb_client.user_workspaces()).get("workspaces", [])
        datasources = await tb_client.datasources()
        pipes = await tb_client.pipes(dependencies=True)
        await folder_build(
            tb_client,
            workspaces,
            datasources,
            pipes,
        )
        if data:
            ds_name = os.path.basename(data.split(".")[0])
            await append_datasource(ctx, tb_client, ds_name, data, None, None, False, 1)
        elif prompt:
            datasource_files = [f for f in os.listdir(Path(folder) / "datasources") if f.endswith(".datasource")]
            for datasource_file in datasource_files:
                datasource_path = Path(folder) / "datasources" / datasource_file
                llm_config = CLIConfig.get_llm_config()
                llm = LLM(key=llm_config["api_key"])
                datasource_name = datasource_path.stem
                datasource_content = datasource_path.read_text()
                has_json_path = "`json:" in datasource_content
                if has_json_path:
                    await llm.generate_sql_sample_data(tb_client, datasource_name, datasource_content)
        click.echo(FeedbackManager.success(message="\n✓ Tinybird Local is ready!"))
    except Exception as e:
        click.echo(FeedbackManager.error(message=f"Error: {str(e)}"))


async def project_create(
    client: TinyB,
    data: Optional[str],
    prompt: Optional[str],
    folder: str,
):
    project_paths = ["datasources", "endpoints", "materializations", "copies", "sinks"]
    force = True
    for x in project_paths:
        try:
            f = Path(folder) / x
            f.mkdir()
            click.echo(FeedbackManager.info_path_created(path=x))
        except FileExistsError:
            click.echo(FeedbackManager.info_path_created(path=x))

    def generate_pipe_file(name: str, content: str):
        base = Path("endpoints")
        if not base.exists():
            base = Path()
        f = base / (f"{name}.pipe")
        with open(f"{f}", "w") as file:
            file.write(content)
        click.echo(FeedbackManager.info_file_created(file=f))

    if data:
        path = Path(folder) / data
        format = path.suffix.lstrip(".")
        await _generate_datafile(str(path), client, format=format, force=force)
        name = data.split(".")[0]
        generate_pipe_file(
            f"{name}_endpoint",
            f"""
NODE endpoint
SQL >
    SELECT * from {name}
TYPE ENDPOINT
            """,
        )
    elif prompt:
        try:
            llm_config = CLIConfig.get_llm_config()
            llm = LLM(key=llm_config["api_key"])
            result = await llm.create_project(prompt)
            for ds in result.datasources:
                content = ds.content.replace("```", "")
                generate_datafile(content, filename=f"{ds.name}.datasource", data=None, _format="ndjson", force=force)

            for pipe in result.pipes:
                content = pipe.content.replace("```", "")
                generate_pipe_file(pipe.name, content)
        except Exception as e:
            click.echo(FeedbackManager.error(message=f"Error: {str(e)}"))
    else:
        events_ds = """
SCHEMA >
    `age` Int16 `json:$.age`,
    `airline` String `json:$.airline`,
    `email` String `json:$.email`,
    `extra_bags` Int16 `json:$.extra_bags`,
    `flight_from` String `json:$.flight_from`,
    `flight_to` String `json:$.flight_to`,
    `meal_choice` String `json:$.meal_choice`,
    `name` String `json:$.name`,
    `passport_number` Int32 `json:$.passport_number`,
    `priority_boarding` UInt8 `json:$.priority_boarding`,
    `timestamp` DateTime `json:$.timestamp`,
    `transaction_id` String `json:$.transaction_id`

ENGINE "MergeTree"
ENGINE_PARTITION_KEY "toYear(timestamp)"
ENGINE_SORTING_KEY "airline, timestamp"
"""
        top_airlines = """
NODE endpoint
SQL >
    SELECT airline, count() as bookings FROM events
    GROUP BY airline
    ORDER BY bookings DESC
    LIMIT 5
TYPE ENDPOINT
"""
        generate_datafile(events_ds, filename="events.datasource", data=None, _format="ndjson", force=force)
        generate_pipe_file("top_airlines", top_airlines)


async def append_datasource(
    ctx: Context,
    tb_client: TinyB,
    datasource_name: str,
    url: str,
    sql: Optional[str],
    incremental: Optional[str],
    ignore_empty: bool,
    concurrency: int,
):
    if incremental:
        date = None
        source_column = incremental.split(":")[0]
        dest_column = incremental.split(":")[-1]
        result = await tb_client.query(f"SELECT max({dest_column}) as inc from {datasource_name} FORMAT JSON")
        try:
            date = result["data"][0]["inc"]
        except Exception as e:
            raise CLIDatasourceException(f"{str(e)}")
        if date:
            sql = f"{sql} WHERE {source_column} > '{date}'"
    await push_data(
        ctx,
        tb_client,
        datasource_name,
        url,
        None,
        sql,
        mode="append",
        ignore_empty=ignore_empty,
        concurrency=concurrency,
    )
