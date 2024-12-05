from cffi import FFI

ffibuilder = FFI()

ffibuilder.set_source(
    "csv_importer_find_endline",
    r"""

#include <stdlib.h>

static const int NORMAL = 0;

#if defined(__x86_64__)
#include <immintrin.h>
#endif

int find_new_line_index_to_split_the_buffer(unsigned char *buffer, int buffer_size,
                                unsigned char quotechar, unsigned char escapechar)
{
    size_t state = NORMAL;
    int last_new_line_found = -1;

    int i = 1;
    if (buffer[0] == quotechar)
    {
        state = 1;
    }else if (buffer[0] == '\n')
    {
        last_new_line_found = 0;
    }else if (buffer[0] == escapechar){
        i = 2;
    }

#if defined(__x86_64__)
    __m128i sse_newline = _mm_set1_epi8('\n');
    __m128i sse_quotechar = _mm_set1_epi8(quotechar);
    __m128i sse_escapechar = _mm_set1_epi8(escapechar);
    int max_simd = buffer_size - 16;
#endif

    for (; i < buffer_size; i++)
    {
#if defined(__x86_64__)
        for (; i < max_simd; i += 16)
        {
            __m128i *sse_p = (__m128i *)&buffer[i];
            __m128i sse_a = _mm_loadu_si128(sse_p);
            int mask_quoted = _mm_movemask_epi8(_mm_cmpeq_epi8(sse_quotechar, sse_a));
            int mask_newline = _mm_movemask_epi8(_mm_cmpeq_epi8(sse_newline, sse_a));
            int mask = mask_quoted | mask_newline;
            if (escapechar)
            {
                mask |= _mm_movemask_epi8(_mm_cmpeq_epi8(sse_escapechar, sse_a));
            }
            if (mask != 0)
            {
                if (mask == mask_quoted)
                {
                    int quotes = __builtin_popcount(mask_quoted);
                    state = (state + quotes) % 2;
                }
                else if (mask == mask_newline)
                {
                    if (state == NORMAL)
                    {
                        last_new_line_found = i + (31 - __builtin_clz(mask));
                    }
                }
                else
                {
                    i += __builtin_ctz(mask);
                    break;
                }
            }
        }
#endif
        if (buffer[i] == quotechar)
        {
            state = !state;
        }
        else if (state == NORMAL && buffer[i] == '\n')
        {
            last_new_line_found = i;
        }
        else if (buffer[i] == escapechar)
        {
            i++;
        }
    }

    return last_new_line_found;
}


""",
    extra_compile_args=["-Wall", "-std=c99", "-O3"],
)

ffibuilder.cdef("int find_new_line_index_to_split_the_buffer(unsigned char *, int, unsigned char, unsigned char);")
ffibuilder.compile(verbose=True)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
