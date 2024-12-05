import asyncio
import logging
import os
import tempfile
from pathlib import Path

from tinybird.ch import get_processor_path
from tinybird.ch_utils.exceptions import CHLocalException

# Execute a query on clickhouse-local
#
# CH-local restricts the usage of data passed using "--file" to sequential access
# To overcome that limitation, set 'input_random_access_table' to the name of
# a randomly-accessible table that ch_local_query will create as a workaround


async def ch_local_query(
    query,
    data,
    input_format,
    input_structure,
    output_format="JSON",
    timeout=5,
    max_retries=1,
    input_random_access_table=None,
    dialect=None,
):
    tmp_ch_local_dir = "/tmp/tinybird/ch_local"
    # Store clickhouse-local temporal files on its own folder to avoid permissions issues
    Path(tmp_ch_local_dir).mkdir(parents=True, exist_ok=True)

    # Avoid using pipes, as tinybird_server forks, leaving the stdin FD open from our side
    # Resulting in never ending clickhouse-local invocations
    with tempfile.NamedTemporaryFile(mode="wb", delete=False, prefix="data_", dir=tmp_ch_local_dir) as f:
        try:
            f.write(data)
            f.close()

            if input_random_access_table:
                query = f"""CREATE TABLE {input_random_access_table}({input_structure}) ENGINE = Memory;
                            INSERT INTO {input_random_access_table} SELECT * FROM table;
                            {query}"""

            if dialect and "delimiter" in dialect and dialect["delimiter"] == "\t":
                input_format = "CustomSeparated" if dialect["delimiter"] == "\t" else "CSV"
            if dialect and "has_header" in dialect and dialect["has_header"] and not input_format.endswith("WithNames"):
                input_format = f"{input_format}WithNames"

            ch_args = [
                "--query",
                query,
                "--file",
                f.name,
                "--input-format",
                input_format,
                "--output-format",
                output_format,
                "--structure",
                input_structure,
                "--input_format_defaults_for_omitted_fields",
                "1",
                "--format_csv_delimiter",
                "," if not dialect else dialect.get("delimiter", ","),
                "--date_time_input_format",
                "best_effort",
                "--format_csv_allow_single_quotes",
                "1",  # Changed default in CH 22.7
                "--max_query_size",
                "1000000",
                "-mn",
            ]
            if dialect and "delimiter" in dialect and dialect["delimiter"] == "\t":
                ch_args += ["--format_custom_escaping_rule", "CSV", "--format_custom_field_delimiter", "\t"]

            # Retries can be used to workaround Clickhouse-local random deadlock
            retries = 0

            env = os.environ.copy()
            env["TZ"] = "UTC"
            env["TMP"] = tmp_ch_local_dir

            while True:
                ch_local = await asyncio.create_subprocess_exec(
                    get_processor_path(),
                    "local",
                    *ch_args,
                    stdin=asyncio.subprocess.DEVNULL,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    env=env,
                    start_new_session=True,
                )

                async def work():
                    stdout, stderr = await ch_local.communicate()  # noqa: B023
                    if ch_local.returncode:  # noqa: B023
                        error = CHLocalException(ch_local.returncode, stderr, query)  # noqa: B023
                        logging.warning(str(error))
                        raise error
                    return stdout

                ch_task = asyncio.shield(asyncio.create_task(work()))
                try:
                    await asyncio.wait_for(ch_task, timeout=timeout)
                    return ch_task.result()
                except asyncio.TimeoutError:
                    err = f"Clickhouse-local timeout after {timeout} seconds and {retries} retries."
                    logging.error(err)
                    ch_local.kill()
                    try:
                        await ch_task
                    except Exception:
                        pass
                    retries += 1
                    if retries > max_retries:
                        raise Exception(err)
        finally:
            os.unlink(f.name)
