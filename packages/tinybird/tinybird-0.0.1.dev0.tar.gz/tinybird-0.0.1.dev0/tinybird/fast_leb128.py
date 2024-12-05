from cffi import FFI
from fast_leb128_c import lib

ffi = FFI()


def create_buffer():
    buffer_py = memoryview(bytearray(16))
    buffer_ffi = ffi.from_buffer(buffer_py, require_writable=True)
    return (buffer_py, buffer_ffi)


def encode(leb_buffer, x: int):
    size = lib.leb_encode(leb_buffer[1], x)
    return leb_buffer[0][:size]
