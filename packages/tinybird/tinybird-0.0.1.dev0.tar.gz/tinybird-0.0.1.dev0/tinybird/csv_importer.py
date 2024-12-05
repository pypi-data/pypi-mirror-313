import logging
import math
import queue
import string
import time
import uuid
import zlib
from datetime import datetime, timezone
from io import BytesIO
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from typing import Any, Callable, Dict, List, Optional
from urllib.parse import urlparse

import requests
from requests import Session

from tinybird.datasource import Datasource
from tinybird.default_timeouts import socket_connect_timeout, socket_read_timeout
from tinybird_shared.retry.retry import retry_sync

from . import text_encoding_guessing
from .blocks import Block
from .ch import CSVInfo, ch_table_exists_sync, table_stats
from .csv_guess import guess_new_line
from .csv_importer_find_endline_wrapper import EncodingNotSupportedException, find_new_line_index_to_split_the_buffer
from .csv_processing_queue import CsvChunkQueueRegistry
from .limits import GB, FileSizeException, Limit, get_url_file_size_checker
from .syncasync import async_to_sync
from .table import analyze_csv_and_create_tables_if_dont_exist
from .timing import Timer
from .user import User, Users
from .views.api_errors.utils import get_errors
from .views.gzip_utils import has_gzip_magic_code, is_gzip_file


class CSVImporterSettings:
    CHUNK_SIZE = 64 * 1024 * 1024
    MIN_PARTS = 2
    MAX_PARTS = 512
    RANGE_HEADER = "Accept-Ranges"
    BYTES_TO_FETCH = Limit.import_csv_bytes_to_fetch
    BYTES_TO_GUESS_CSV = 1024 * 50
    MAX_MEMORY_IN_PROCESS_QUEUE = CHUNK_SIZE * 8
    MAX_WAIT_TO_EMPTY_QUEUE_TIME_SECONDS = 120
    FETCH_PROCESS_RATIO = 4


@retry_sync(requests.exceptions.RequestException, tries=4)
def fetch_csv_range(url: str, headers: Dict[str, str], start: int, end: int, decompressor: Any = None):
    # dont send headers if not needed
    if start > 0 or end != -1:
        range_headers = {"Range": "bytes=%d-%d" % (start, end)}
        range_headers.update(headers)
    else:
        range_headers = headers
    t = requests.get(
        url, headers=range_headers, timeout=(socket_connect_timeout(), socket_read_timeout()), allow_redirects=False
    )
    t.raise_for_status()

    return t.content, t.headers


def is_gzip(chunk: bytes, url: str, http_headers: dict):
    return (
        has_gzip_magic_code(chunk)
        or is_gzip_file(url)
        or "gzip" in http_headers.get("Content-Encoding", "")
        or "gzip" in http_headers.get("Content-Type", "")
    )


class BufferedCSVProcessor:
    """
    >>> chunk_0 = b"a,b,c\\n1,2,3\\n4"
    >>> chunk_1 = b",5,6\\n7,8,9"
    >>> c = BufferedCSVProcessor()
    >>> def a(csv): print(csv)
    >>> c.process_csv_chunk = a
    >>> c.chunk_size = len(chunk_0)
    >>> c.write(chunk_0)
    b'a,b,c\\n1,2,3\\n'
    >>> c.write(chunk_1)
    >>> c.flush()
    b'4,5,6\\n7,8,9'
    """

    def __init__(self, dialect: Optional[Dict[str, Any]] = None, encoding: Optional[str] = None):
        self.buffer = BytesIO()
        self.dialect = dialect or {}
        self.chunk_size = CSVImporterSettings.CHUNK_SIZE
        self.encoding = encoding

    def process_csv_chunk(self, csv_chunk):
        pass

    def write(self, chunk: bytes):
        self.buffer.write(chunk)
        if len(self.buffer.getbuffer()) >= self.chunk_size:
            buff = self.buffer.getvalue()
            if not self.dialect.get("new_line", None):
                sample = buff[: CSVImporterSettings.BYTES_TO_GUESS_CSV]
                extract, encoding = text_encoding_guessing.decode_with_guess(sample)
                if not self.encoding:
                    self.encoding = encoding
                self.dialect["new_line"] = guess_new_line(extract)
            if not self.encoding:
                _, encoding = text_encoding_guessing.decode_with_guess(buff[: CSVImporterSettings.BYTES_TO_GUESS_CSV])
                self.encoding = encoding

            try:
                new_line_idx = find_new_line_index_to_split_the_buffer(
                    buff, self.encoding, escapechar=self.dialect.get("escapechar", None)
                )
                split_position = new_line_idx + 1 if new_line_idx != -1 else None
            except EncodingNotSupportedException:
                logging.warning(
                    f"New line split position couldn't be calculated with the improved algorithm. Encoding used: {self.encoding}"
                )
                split_position = buff.rindex(self.dialect["new_line"].encode()) + len(self.dialect["new_line"])

            if not split_position:
                return

            process = buff[:split_position]
            self.process_csv_chunk(process)

            # reset buffer
            self.buffer = BytesIO()
            # write remaining bytes
            if split_position <= len(buff) - 1:
                self.buffer.write(buff[split_position:])

    def flush(self):
        if len(self.buffer.getbuffer()) > 0:
            self.process_csv_chunk(self.buffer.getvalue())


def csv_offsets_url(
    session: Session,
    url: str,
    part_size: int,
    max_parts=CSVImporterSettings.MAX_PARTS,
    min_parts: int = 2,
    file_size_checker: Optional[Callable[[int], None]] = None,
    bytes_to_fetch=CSVImporterSettings.BYTES_TO_FETCH,
):
    supports_range = False
    headers = {"Range": "bytes=%d-%d" % (0, 1)}
    decompressor = None

    try:
        head = session.head(
            url, headers=headers, timeout=(socket_connect_timeout(), socket_read_timeout()), allow_redirects=False
        )
        head.raise_for_status()
        supports_range = CSVImporterSettings.RANGE_HEADER in head.headers
    except requests.exceptions.RequestException:
        # some servers raise exceptions when try to send range headers
        supports_range = False

    if not supports_range and max_parts > 1:
        # give it the last chance
        # sometimes head is not allowed, to know if the server supports range, requests first 100 bytes
        # set stream=True to avoid reading the body
        try:
            res = requests.get(
                url,
                stream=True,
                headers={"Range": "bytes=0-99"},
                timeout=(socket_connect_timeout(), socket_read_timeout()),
                allow_redirects=False,
            )
            res.raise_for_status()
            supports_range = "Content-Length" in res.headers and res.headers["Content-Length"] == "100"
        except requests.exceptions.RequestException:
            supports_range = False

    # next request, this time with the full range
    # range_headers = {"Range": "bytes=0--1"}
    # don't request compressed content because some servers don't
    # send the content-length.
    headers_no_gzip = {"Accept-Encoding": "identity"}
    content_length = None
    try:
        head = session.get(
            url,
            stream=True,
            headers=headers_no_gzip,
            timeout=(socket_connect_timeout(), socket_read_timeout()),
            allow_redirects=False,
        )
        head.raise_for_status()
        if "Content-Length" in head.headers:
            content_length = head.headers["Content-Length"]
        else:
            supports_range = False
    except requests.exceptions.RequestException:
        supports_range = False

    file_size = int(content_length) if content_length is not None else None
    if file_size_checker and file_size is not None:
        file_size_checker(file_size)

    # server does not support HEAD so file length and 'accept-range' capabilities
    # can't be known
    if max_parts == 1 or not supports_range or file_size is None:
        # read the first bytes and return it as extract
        logging.info("server does not support ranges")

        @retry_sync(requests.exceptions.RequestException, tries=4)
        def f():
            decompressor = None
            with requests.get(
                url,
                stream=True,
                timeout=(socket_connect_timeout(), socket_read_timeout()),
                allow_redirects=False,
            ) as r:
                r.raise_for_status()
                try:
                    extract = next(r.iter_content(chunk_size=bytes_to_fetch))
                    if has_gzip_magic_code(extract):
                        decompressor = zlib.decompressobj(wbits=16 + 15)
                        extract = decompressor.decompress(extract)
                        extract, encoding = text_encoding_guessing.decode_with_guess(extract)
                    else:
                        # sometimes it's not possible for requests to guess the type and extract is a 'bytes'
                        extract, encoding = text_encoding_guessing.decode_with_guess(extract)
                except StopIteration:
                    logging.warning("Not enough bytes to read from the response")
                    return [{"start_offset": 0, "end_offset": -1}], [], None, None, decompressor
            newline = guess_new_line(extract)
            fixed_extract = extract[: extract.rindex(newline)] if newline else extract[:]
            return [{"start_offset": 0, "end_offset": -1}], [fixed_extract], encoding, newline, decompressor

        return f()

    # fetch the first range
    headers = {"Range": "bytes=%d-%d" % (0, bytes_to_fetch)}

    @retry_sync(requests.exceptions.RequestException, tries=4)
    def retry_get(url: str, headers: Dict[str, str]):
        try:
            r = session.get(
                url, headers=headers, timeout=(socket_connect_timeout(), socket_read_timeout()), allow_redirects=False
            )
            r.raise_for_status()
            return r
        except requests.exceptions.RequestException as e:
            logging.warning("Error in retry_get for %s. Headers:%s. Exception:%s", url, str(headers), str(e))
            raise e

    r = retry_get(url, headers)

    content = r.content
    if is_gzip(content, url, r.headers):
        try:
            decompressor = zlib.decompressobj(wbits=16 + 15)
            content = decompressor.decompress(r.content)
            # calc the part size compressed to download BYTES_TO_FETCH uncompressed
            part_size = int(part_size * bytes_to_fetch / len(content))
        except Exception:
            decompressor = None

    if file_size < part_size:
        min_parts = 1
    N = max(min_parts, int(math.floor(file_size / part_size)))
    if N > max_parts:
        logging.warning(f"The URL '{url}' should use {N} chunks but will use {max_parts} chunks")
    N = min(N, max_parts)
    partition = [0]
    csv_extracts = []

    # guess encoding. requests assumes latin-1 if the content type is text
    # that's not generally true so use response encoding if present if not guess it
    if "charset" in r.headers["content-type"]:
        encoding = r.encoding
        data_decoded = text_encoding_guessing.try_decode_block(content, encoding)
    else:
        data_decoded, encoding = text_encoding_guessing.decode_with_guess(content)
    newline = guess_new_line(data_decoded)
    csv_extracts.append(data_decoded[: data_decoded.rindex(newline)] if newline else data_decoded)

    if decompressor:
        # Not analyze chunks if the file is compressed
        for x in range(1, N):
            start = int(x * (file_size / N))
            partition.append(start)
    else:
        # if not decompress
        # next ones
        for x in range(1, N):
            start = int(x * (file_size / N))
            # fetch a portion of the file
            # Adding Accept-Encoding because Requests try to decode the file
            # and fails because we're not getting the header check correctly
            headers = {"Range": "bytes=%d-%d" % (start, start + bytes_to_fetch), "Accept-Encoding": "identity"}
            data = retry_get(url, headers).content
            if decompressor:
                data = decompressor.decompress(data)

            if not newline:
                raise Exception(f"Line separator not found, does the CSV have rows larger than {bytes_to_fetch} bytes?")

            # this doesn't take into account there could be new line inside fields (quoted)
            try:
                c = data.index(newline.encode())
            except ValueError as e:
                logging.exception(e)
                raise Exception(
                    f"CSV separator field not found, does the CSV have rows larger than {bytes_to_fetch} bytes?"
                )

            partition.append(start + c + len(newline.encode()))
            # save csv extract so types can be guess using parts of the file
            csv_extracts.append(
                text_encoding_guessing.try_decode_block(data[c + 1 : data.rindex(newline.encode())], encoding)
            )
    partition.append(file_size + 1)
    partitions = [{"start_offset": partition[x], "end_offset": partition[x + 1] - 1} for x in range(len(partition) - 1)]
    logging.info("%s: partitions %d" % (url, len(partitions)))
    return partitions, csv_extracts, encoding, newline, decompressor


def fetch_csv_block(args):
    block_id, request_with_range = args
    error = None
    data = None
    with Timer("fetch_csv_block %s" % block_id) as t:
        logging.info(
            f"fetching block {block_id}, ({request_with_range['start_offset']}-{request_with_range['end_offset']})"
        )
        try:
            data = fetch_csv_range(
                request_with_range["url"],
                request_with_range["headers"],
                request_with_range["start_offset"],
                request_with_range["end_offset"],
            )[0]
        except Exception as e:
            # TODO: meaningful error
            logging.exception(f"error fetching block {block_id}: {str(e)}")
            error = e

    logging.info(f"finished fetching block {block_id}")

    response = {
        "block_id": block_id,
        "fetch_time": t.interval,
        "fetch_bytes": len(data) if data else 0,
        "fetch_url": request_with_range["url"],
        "fetch_bytes_per_second": len(data) / t.interval if t.interval and data else 0,
    }

    if error:
        response["fetch_error"] = str(error)

    return block_id, data, response


@retry_sync(requests.exceptions.RequestException, tries=4)
def fetch_csv_block_stream(block_id, request_with_range: Dict[str, Any]):
    t = requests.get(
        request_with_range["url"],
        headers=request_with_range["headers"],
        stream=True,
        timeout=(socket_connect_timeout(), socket_read_timeout()),
        allow_redirects=False,
    )
    t.raise_for_status()
    return t


def datasource_name_default():
    return "imported_" + datetime.now(timezone.utc).strftime("%Y_%m_%d__%H_%M_%S")


def datasource_name_from_url(url: str):
    """
    >>> datasource_name_from_url('http://localhost:8000/SacramentocrimeJanuary2006.csv')
    'SacramentocrimeJanuary2006'
    >>> datasource_name_from_url('http://localhost:8000/sacramentocrimejanuary2006')
    'sacramentocrimejanuary2006'
    >>> datasource_name_from_url('http://localhost:8000/SacramentocrimeJanuary2006/')
    'SacramentocrimeJanuary2006'
    >>> datasource_name_from_url('https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2015-06.csv')
    'yellow_tripdata_2015_06'
    >>> name = datasource_name_from_url('http://example.com/?no_path=true')
    >>> name.startswith('imported_')
    True
    """
    if url[-1] == "/":
        url = url[:-1]
    p = urlparse(url)
    table_name = p.path[1:].rsplit("/", 1)[-1].split(".")[0].replace("/", "").replace("-", "_")
    if not table_name:
        return datasource_name_default()
    if table_name[0] in string.digits:
        table_name = "t_" + table_name
    return table_name


def adjust_offsets(csv_info: CSVInfo, requests_with_range):
    """depending on the csv structure some offsets need to be fixed, for example to skip the header"""
    # skip header moving the first start offset
    block = requests_with_range[0][1]
    block["start_offset"] = block["start_offset"] + csv_info.header_len()


def import_csv(
    user: User,
    datasource: Datasource,
    url: str,
    headers: Dict[str, Any],
    existing_block_status_log: Optional[List[Dict]] = None,
    dialect_overrides: Optional[Dict[str, Any]] = None,
    type_guessing: bool = True,
    import_id=None,
):
    """
    imports a csv file from an url
    """
    logging.getLogger().setLevel(logging.INFO)

    database_server = user.database_server
    database = user.database
    cluster = user.cluster
    table_name = datasource.id
    file_limit_gb = user.get_limits(prefix="import").get("import_max_url_file_size_gb", None)
    file_limit = file_limit_gb * GB if file_limit_gb is not None else None
    file_size_checker = get_url_file_size_checker(file_limit, user.plan, user.id, table_name)
    bytes_to_fetch = user.get_limits(prefix="import").get(
        "import_csv_bytes_to_fetch", CSVImporterSettings.BYTES_TO_FETCH
    )

    block_status_log = existing_block_status_log or []

    stats = {}
    with Timer() as timing:
        logging.info("importing %s" % url)

        try:
            with requests.Session() as session:
                session.headers.update(headers)
                offsets, csv_extracts, encoding, _, decompressor = csv_offsets_url(
                    session,
                    url,
                    CSVImporterSettings.CHUNK_SIZE,
                    min_parts=CSVImporterSettings.MIN_PARTS,
                    file_size_checker=file_size_checker,
                    bytes_to_fetch=bytes_to_fetch,
                )
                if not "".join(csv_extracts).strip():
                    # The file is empty
                    try:
                        # This is needed for the Replace Hook to work for empty files
                        if not ch_table_exists_sync(table_name, database_server, database):
                            table_created = False
                            for hook in datasource.hooks:
                                table_created = table_created or hook.before_create(datasource)
                            if not table_created:
                                return {"error": "cannot create table with empty file"}
                            for hook in datasource.hooks:
                                hook.after_create(datasource)
                    except Exception as e:
                        return {"error": str(e)}
                    for hook in datasource.hooks:
                        hook.before_append(datasource)
                    stats = table_stats(table_name, database_server, database)
                    return {"blocks": [], "time": 0, "table": table_name, "stats": stats}
        except requests.exceptions.RequestException as e:
            return {"error": f"Could not fetch URL. {e}"}
        except FileSizeException as err:
            return {"error": str(err)}

        try:
            info = analyze_csv_and_create_tables_if_dont_exist(
                user,
                datasource,
                "\n".join(csv_extracts),
                dialect_overrides=dialect_overrides,
                type_guessing=type_guessing,
            )
        except Exception as e:
            return {"error": str(e)}

        try:
            for hook in datasource.hooks:
                hook.before_append(datasource)
        except Exception as e:
            logging.exception(e)
            return {"error": "failed to execute before append hooks"}

        # add fetching information
        for x in offsets:
            x["url"] = url
            x["headers"] = headers
        requests_with_range = [(str(uuid.uuid4()), offset) for offset in offsets]
        if not decompressor:
            adjust_offsets(info, requests_with_range)

        for block_id, _ in requests_with_range:
            block_status_log.append({"block_id": block_id, "status": "idle", "timestamp": datetime.now(timezone.utc)})

        q: queue.Queue[Optional[Block]] = queue.Queue()
        process_result: List[Any] = []
        logging.info(f"[csv_importer] csv_process_queue Queue={id(q)}, len(offsets)={len(offsets)}")
        CsvChunkQueueRegistry.get_or_create().process_queue(q, process_result, block_status_log)

        fetch_stats = {}

        # utility function to know block status and do some throttling
        def block_generator(requests_with_range):
            in_flight = 0
            for request_with_range in requests_with_range:
                block_status_log.append(
                    {"block_id": request_with_range[0], "status": "fetching", "timestamp": datetime.now(timezone.utc)}
                )
                # check queue to see if the processing queue is too big
                # if the thread pool continues fetching data and processor is stopped there will be a OOM
                waiting_time: float = 0
                queue_size = CsvChunkQueueRegistry.get_or_create().blocks_waiting()
                logging.debug(
                    f"queue_size: {queue_size}, block_avg_size: {block_avg_size}, MAX_MEMORY_IN_PROCESS_QUEUE: {CSVImporterSettings.MAX_MEMORY_IN_PROCESS_QUEUE}"
                )

                if queue_size * block_avg_size > CSVImporterSettings.MAX_MEMORY_IN_PROCESS_QUEUE:
                    # give time to process blocks until we have just two blocks
                    estimated_blocks = int(CSVImporterSettings.MAX_MEMORY_IN_PROCESS_QUEUE / block_avg_size)
                    logging.info("waiting for queue to reduce, estimated items: %d" % estimated_blocks)

                    while queue_size > CSVImporterSettings.FETCH_PROCESS_RATIO * estimated_blocks:
                        time.sleep(1.0)
                        waiting_time += 1.0
                        if waiting_time > CSVImporterSettings.MAX_WAIT_TO_EMPTY_QUEUE_TIME_SECONDS:
                            error = f"Max time waiting for process queue to be reduced reached ({CSVImporterSettings.MAX_WAIT_TO_EMPTY_QUEUE_TIME_SECONDS} seconds)"
                            logging.error(error)
                            raise Exception(error)
                        queue_size = CsvChunkQueueRegistry.get_or_create().blocks_waiting()

                estimated_fetching = in_flight - len(process_result)
                logging.debug("estimated fetching: %d" % estimated_fetching)

                while (
                    estimated_fetching * CSVImporterSettings.CHUNK_SIZE
                    > CSVImporterSettings.MAX_MEMORY_IN_PROCESS_QUEUE
                ):
                    logging.info(
                        f"waiting for queue to reduce to fetch more items, estimated items: {estimated_fetching}, waiting_time: {waiting_time}, max: {CSVImporterSettings.MAX_WAIT_TO_EMPTY_QUEUE_TIME_SECONDS}"
                    )
                    time.sleep(1.0)
                    waiting_time += 1.0
                    if waiting_time > CSVImporterSettings.MAX_WAIT_TO_EMPTY_QUEUE_TIME_SECONDS:
                        error = f"Max time waiting to reduce to fetch more items reached ({CSVImporterSettings.MAX_WAIT_TO_EMPTY_QUEUE_TIME_SECONDS} seconds)"
                        logging.error(error)
                        raise Exception(error)

                    estimated_fetching = in_flight - len(process_result)

                in_flight += 1
                yield request_with_range

        # In case a decompressor was used when getting the offsets, it means it's a GZIP and we need a new one,
        # since we are going to fetch all chunks from the very beginning
        if decompressor:
            decompressor = zlib.decompressobj(wbits=16 + 15)

        if len(offsets) > 1:
            block_avg_size: float = 0
            block_count = 0

            # there is usually a relation of 4x between fetching and processing time
            # so there should be 4x threads per core. Obviously this could change with
            # the setup/network speed and so on and might be dynamic. Enough for the moment

            # back pressure mechanism only allows downloading this number of chunks at the same time, so we limit the number of threads
            max_simultaneous_downloads = max(
                1, math.ceil(CSVImporterSettings.MAX_MEMORY_IN_PROCESS_QUEUE / CSVImporterSettings.CHUNK_SIZE)
            )

            with ThreadPool(
                min(len(offsets), cpu_count() * CSVImporterSettings.FETCH_PROCESS_RATIO, max_simultaneous_downloads)
            ) as executor:
                try:
                    prev_chunk_part = None
                    last_block_id = requests_with_range[-1][0]

                    def fetch_fun():
                        return executor.imap_unordered if not decompressor else executor.imap

                    for block_id, data, stats in fetch_fun()(fetch_csv_block, block_generator(requests_with_range)):
                        if data:
                            if decompressor:
                                data = decompressor.decompress(data)
                            # cumulative moving average
                            block_avg_size = (len(data) + block_count * block_avg_size) / (block_count + 1)
                            block_count += 1

                        else:
                            logging.info(f"block {block_id} fetched: No data")

                        if data:
                            block_status_log.append(
                                {"block_id": block_id, "status": "queued", "timestamp": datetime.now(timezone.utc)}
                            )
                            with_quarantine = True
                            data_decoded = text_encoding_guessing.try_decode_block(data, encoding)
                            if not decompressor:
                                # Not compressed data is received in correct chunks delimited by '\n'
                                block_data = data_decoded
                            else:
                                # With compressed data we need to correct block data
                                # removing the last partial line of each block
                                # and processing with the next one.
                                # Note: Compresed block are processed in order
                                if last_block_id == block_id:
                                    block_data = prev_chunk_part + data_decoded if prev_chunk_part else data_decoded
                                else:
                                    last_newline_position = data_decoded.rfind(info.dialect["new_line"])
                                    current_data = data_decoded[: last_newline_position + 1]
                                    block_data = prev_chunk_part + current_data if prev_chunk_part else current_data
                                    prev_chunk_part = data_decoded[last_newline_position + 1 :]
                            q.put(
                                Block(
                                    id=block_id,
                                    table_name=table_name,
                                    data=block_data,
                                    database_server=database_server,
                                    database=database,
                                    cluster=cluster,
                                    dialect=info.dialect,
                                    import_id=import_id,
                                    max_execution_time=user.get_limits(prefix="ch").get(
                                        "chunk_max_execution_time", Limit.ch_chunk_max_execution_time
                                    ),
                                    csv_columns=info.columns,
                                    quarantine=with_quarantine,
                                )
                            )
                        else:
                            block_status_log.append(
                                {
                                    "block_id": block_id,
                                    "status": "fetched_no_data",
                                    "timestamp": datetime.now(timezone.utc),
                                }
                            )

                        fetch_stats[block_id] = stats
                except Exception as e:
                    logging.exception(e)
                    raise e
                finally:
                    # wait for all the blocks to be processed and remove it from main queue
                    q.join()
                    CsvChunkQueueRegistry.get_or_create().remove_queue(q)

        elif len(offsets) == 1:
            block_id = requests_with_range[0][0]
            url = requests_with_range[0][1]
            error = None
            data = None

            # define the processor
            class T(BufferedCSVProcessor):
                def __init__(self):
                    BufferedCSVProcessor.__init__(self, dialect=info.dialect)
                    self.block_count = 0

                def process_csv_chunk(self, data):
                    block_status_log.append(
                        {"block_id": block_id, "status": "queued", "timestamp": datetime.now(timezone.utc)}
                    )
                    with_quarantine = True
                    q.put(
                        Block(
                            id=block_id,
                            table_name=table_name,
                            data=text_encoding_guessing.try_decode_block(data, encoding),
                            database_server=database_server,
                            database=database,
                            cluster=cluster,
                            dialect=info.dialect,
                            import_id=import_id,
                            max_execution_time=user.get_limits(prefix="ch").get(
                                "chunk_max_execution_time", Limit.ch_chunk_max_execution_time
                            ),
                            csv_columns=info.columns,
                            quarantine=with_quarantine,
                        )
                    )
                    self.block_count += 1

            fetch_bytes = 0

            max_unfinished_tasks_in_queue = max(
                1, math.ceil(CSVImporterSettings.MAX_MEMORY_IN_PROCESS_QUEUE / CSVImporterSettings.CHUNK_SIZE)
            )

            with Timer("fetch_csv_block_stream %s" % block_id) as t:
                logging.info(f"fetching block {block_id}")

                try:
                    processor = T()
                    res = fetch_csv_block_stream(*requests_with_range[0])
                    pending_header_bytes = info.header_len()

                    for data in res.iter_content(CSVImporterSettings.CHUNK_SIZE):
                        while q.unfinished_tasks >= max_unfinished_tasks_in_queue:
                            time.sleep(0.5)

                        fetch_bytes += len(data)
                        if decompressor:
                            data = decompressor.decompress(data)
                        if pending_header_bytes:
                            skip_bytes = min(len(data), pending_header_bytes)
                            pending_header_bytes -= skip_bytes
                            data = data[skip_bytes:]
                        processor.write(data)

                except Exception as e:
                    logging.exception(f"error fetching block {block_id}: {e}")
                    error = Exception(e)
                finally:
                    processor.flush()
                    # wait for all the blocks to be processed and remove it from main queue
                    q.join()
                    CsvChunkQueueRegistry.get_or_create().remove_queue(q)

            logging.info(f"finished fetching block {block_id}")

            stats = {
                "block_id": block_id,
                "fetch_time": t.interval,
                "fetch_url": url,
                "fetch_bytes": fetch_bytes,
                "fetch_bytes_per_second": fetch_bytes / t.interval if t.interval and fetch_bytes else 0,
            }

            if error:
                stats["fetch_error"] = str(error)

            fetch_stats[block_id] = stats

        # merge stats for blocks
        blocks = []
        for block_id, offsets in requests_with_range:
            s = {
                "block_id": block_id,
                "url": url,
                "headers": headers,
                "start_offset": offsets["start_offset"],
                "end_offset": offsets["end_offset"],
            }
            s.update(fetch_stats.get(block_id, {}))
            s.update(next((x for x in process_result if x["block_id"] == block_id), {}))
            blocks.append(s)

        stats = table_stats(table_name, database_server, database)

    ret = {"blocks": blocks, "time": timing.interval, "table": table_name, "stats": stats}

    errors, _, _ = get_errors(blocks)

    if len(errors):
        ret["errors"] = errors
        ret["error"] = "There are blocks with errors"
    else:
        async_to_sync(Users.cache_delimiter_used_in_datasource_async)(user, datasource, info.dialect["delimiter"])

    return ret


# TODO: this should be async
def fetch_csv_extract(url: str, headers: Optional[Dict[str, str]] = None, max_parts: int = 1):
    session = requests.Session()
    if headers:
        session.headers.update(headers)
    _, csv_extracts, _, newline, _ = csv_offsets_url(session, url, CSVImporterSettings.CHUNK_SIZE, max_parts=max_parts)
    return csv_extracts, newline
