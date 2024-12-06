import json
from pathlib import Path

import click

from tinybird.feedback_manager import FeedbackManager
from tinybird.tb_cli_modules.cli import cli
from tinybird.tb_cli_modules.common import CLIException, coro
from tinybird.tb_cli_modules.config import CLIConfig
from tinybird.tb_cli_modules.llm import LLM
from tinybird.tb_cli_modules.local import get_tinybird_local_client


@cli.command()
@click.argument("datasource", type=str)
@click.option("--rows", type=int, default=10, help="Number of events to send")
@click.option("--context", type=str, default="", help="Extra context to use for data generation")
@coro
async def mock(datasource: str, rows: int, context: str) -> None:
    """Load sample data into a datasource.

    Args:
        ctx: Click context object
        datasource_file: Path to the datasource file to load sample data into
    """
    import llm

    try:
        datasource_path = Path(datasource)
        datasource_name = datasource
        if datasource_path.suffix == ".datasource":
            datasource_name = datasource_path.stem
        else:
            datasource_path = Path("datasources", f"{datasource}.datasource")

        datasource_content = datasource_path.read_text()
        llm_config = CLIConfig.get_llm_config()
        llm = LLM(key=llm_config["api_key"])
        tb_client = get_tinybird_local_client()
        sql = await llm.generate_sql_sample_data(tb_client, datasource_content, rows, context)
        result = await tb_client.query(f"{sql} FORMAT JSON")
        data = result.get("data", [])
        max_rows_per_request = 100
        sent_rows = 0
        for i in range(0, len(data), max_rows_per_request):
            batch = data[i : i + max_rows_per_request]
            ndjson_data = "\n".join([json.dumps(row) for row in batch])
            await tb_client.datasource_events(datasource_name, ndjson_data)
            sent_rows += len(batch)
        click.echo(f"Sent {sent_rows} events to datasource '{datasource_name}'")

    except Exception as e:
        raise CLIException(FeedbackManager.error_exception(error=str(e)))
