from cffi import FFI

ffibuilder = FFI()

ffibuilder.set_source(
    "fast_leb128_c",
    """

int leb_encode(unsigned char *p, int x) {
    int carry = 0;
    for (int j=0; j<8; j++){
        int byte = x & 0x7f;
        x = x >> 7;
        if (x == 0) {
            p[carry] = byte;
            return carry + 1;
        }
        p[carry] = 0x80 | byte;
        carry++;
    }
    return 0;
}

""",
    extra_compile_args=["-std=c99", "-O3"],
)

ffibuilder.cdef("""int leb_encode(unsigned char*, int);""")
ffibuilder.compile()

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
