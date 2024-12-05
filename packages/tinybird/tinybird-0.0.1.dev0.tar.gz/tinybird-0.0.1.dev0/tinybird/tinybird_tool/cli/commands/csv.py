import click

from tinybird.ch import CHTable, CSVInfo
from tinybird.csv_importer import fetch_csv_extract, fetch_csv_range
from tinybird.csv_processing_queue import cut_csv_extract
from tinybird.timing import Timer

from ..cli_base import cli


@cli.command()
@click.argument("url")
def csv_info(url):
    """Prints information about a csv URL"""
    extracts, _ = fetch_csv_extract(url, max_parts=-1)
    info = CSVInfo.extract_from_csv_extract(extracts[0])
    print(info.to_json())


@cli.command()
@click.argument("path")
def file_guessing_info(path):
    """Prints information about a csv file"""
    with open(path) as file:
        d = file.read()
    info = CSVInfo.extract_from_csv_extract(d)
    print(info.to_json())


@cli.command()
@click.argument("path")
def debug_process_ch(path):
    "Test the CSV provessing of a file"
    with open(path) as file:
        d = file.read()
    info = CSVInfo.extract_from_csv_extract(cut_csv_extract(d[: 100 * 1024], 100 * 1024))
    print(info.to_json())
    encoded = d.encode()
    with Timer() as timing:
        CHTable(info.columns).query(
            data=encoded,
            query="select * from table",
            input_format="CSVWithNames" if info.dialect["has_header"] else "CSV",
            output_format="Native",
            dialect=info.dialect,
        )
    print(timing)


@cli.command()
@click.argument("offset_start")
@click.argument("offset_end")
@click.argument("url")
@click.argument("file_name")
def download_part(offset_start, offset_end, url, file_name):
    """Download a chunk of a remote file to local"""
    data, headers = fetch_csv_range(url, {}, int(offset_start), int(offset_end))
    with open(file_name, "wb") as file:
        file.write(data)
