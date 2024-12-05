from operator import xor
from typing import Union

# Fowler-Noll-Vo hash function
# See https://en.wikipedia.org/wiki/Fowler%E2%80%93Noll%E2%80%93Vo_hash_function#FNV-1a_hash
#
# FNV hash functions are fast, simple, non-cryptographic hash functions


def fnv_1a(data: Union[bytes, str, list]) -> int:
    data = _data_to_bytes(data)
    offset64 = 14695981039346656037
    prime64 = 1099511628211
    max_uint64 = 2**64 - 1
    h = offset64
    for byte in data:
        h = xor(h, byte) % max_uint64
        h = h * prime64 % max_uint64
    return h


def _data_to_bytes(data: Union[bytes, str, list]) -> bytes:
    if isinstance(data, bytes):
        return data
    elif isinstance(data, str):
        return data.encode("utf-8", "replace")
    try:
        return b"".join([_data_to_bytes(x) for x in data])
    except Exception:
        raise Exception("fnv_1a() only accepts types 'bytes', 'str', and 'Iterable'")
