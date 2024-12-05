from csv_importer_find_endline import ffi, lib


class EncodingNotSupportedException(Exception):
    pass


# The list of encodings may not be complete. Feel free to add more encodings if their byte definition for the
# characters used for quotechar, scapechar and new_line have the same byte representation than ascii.
_encodings_supported = ("ascii", "utf-8", "windows-1252", "iso-8859-1", "latin-1")


# Find the last row-delimiting new line of a CSV buffer
def find_new_line_index_to_split_the_buffer(buffer_text_encoded, encoding: str, quotechar=None, escapechar=None):
    if encoding.lower() not in _encodings_supported:
        raise EncodingNotSupportedException(f"Encoding {encoding} is not supported by this method")

    if escapechar is None:
        escapechar = "\0"  # Set escapechar to '\0', to disable it

    if quotechar is None:
        quotechar = '"'

    if not buffer_text_encoded:
        return -1
    buffer = ffi.from_buffer(buffer_text_encoded)
    quotechar = bytes(quotechar, encoding)[0]
    escapechar = bytes(escapechar, encoding)[0]
    result = lib.find_new_line_index_to_split_the_buffer(buffer, len(buffer_text_encoded), quotechar, escapechar)
    return result
