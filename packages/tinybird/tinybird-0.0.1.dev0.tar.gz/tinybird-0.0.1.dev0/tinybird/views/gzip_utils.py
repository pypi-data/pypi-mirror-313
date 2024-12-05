from urllib.parse import urlparse

GZIP_MAGIC_CODE = bytes([0x1F, 0x8B])


def has_gzip_magic_code(chunk: bytes) -> bool:
    return chunk[: len(GZIP_MAGIC_CODE)] == GZIP_MAGIC_CODE


def is_gzip_file(url):
    try:
        # rstrip is to support URLs such as https://storage.cloud.google.com/pmarcos/events.ndjson.gz\?authuser\=0,
        # that return a path='/pmarcos/events.ndjson.gz\\'
        return urlparse(url).path.rstrip("\\").endswith(".gz")
    except Exception:
        return False
