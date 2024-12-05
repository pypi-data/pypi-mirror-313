import re
from enum import Enum


class ExportFormat(str, Enum):
    CSV = "csv"
    NDJSON = "ndjson"
    PARQUET = "parquet"
    ORC = "orc"
    AVRO = "avro"


SUPPORTED_EXPORT_FORMATS_MAPPING = {
    ExportFormat.CSV: "CSVWithNames",
    ExportFormat.NDJSON: "JSONEachRow",
    ExportFormat.PARQUET: "Parquet",
    ExportFormat.AVRO: "Avro",
    ExportFormat.ORC: "ORC",
}

FILE_TEMPLATE_PROPERTIES_REGEX = re.compile(
    r"\{\s*(?P<column_name>.*?)\s*(,\s*[\"'](?P<date_format>.*?)[\"'])?\s*\}(?P<separator>[^{]*)?"
)

COMPRESSION_CODEC_ALIASES = {
    "gz": "gzip",
    "br": "brotli",
    "zst": "zstd",
    "bz2": "bzip2",
}


class WriteStrategy(str, Enum):
    NEW = "new"
    TRUNCATE = "truncate"


SUPPORTED_WRITE_STRATEGIES = {WriteStrategy.NEW: True, WriteStrategy.TRUNCATE: True}


class UnknownCompressionCodecAlias(Exception):
    pass


class UnknownCompressionCodec(Exception):
    pass


def expand_compression_codec_alias(alias: str) -> str:
    try:
        return COMPRESSION_CODEC_ALIASES[alias]
    except KeyError:
        raise UnknownCompressionCodecAlias(alias)


COMPRESSION_CODEC_EXTENSIONS = {
    "gzip": "gz",
    "brotli": "br",
    "zstd": "zst",
    "bzip2": "bz2",
    "xz": "xz",
    "lz4": "lz4",
    "lzma": "lzma",
    "snappy": "snappy",
    "deflate": "deflate",
    "zlib": "zlib",
}


def get_compression_codec_extension(codec: str) -> str:
    try:
        return COMPRESSION_CODEC_EXTENSIONS[codec]
    except KeyError:
        raise UnknownCompressionCodec(codec)


SUPPORTED_COMPRESSION_CODECS = [
    "gz",
    "br",
    "bz2",
    "bzip2",
    "xz",
    "lz4",
    "brotli",
    "gzip",
    "lzma",
    "zst",
    "zstd",
    "deflate",
    "none",
]

SUPPORTED_PARQUET_COMPRESSION_CODECS = ["lz4", "gzip", "zstd", "snappy", "brotli", "none"]
DEFAULT_PARQUET_COMPRESSON_CODEC = "lz4"
SUPPORTED_ORC_COMPRESSION_CODECS = ["lz4", "snappy", "zlib", "zstd", "none"]
DEFAULT_ORC_COMPRESSON_CODEC = "none"
SUPPORTED_AVRO_COMPRESSION_CODECS = ["snappy", "deflate", "none"]
DEFAULT_AVRO_COMPRESSON_CODEC = "snappy"

SUPPORTED_REGION_PREFIXES = [
    "ap-east-1",  # Hong Kong only
    "us-east-",
    "us-west-",
    "eu-central-",
    "eu-west-",
    "eu-south-",
    "eu-north-",
]
