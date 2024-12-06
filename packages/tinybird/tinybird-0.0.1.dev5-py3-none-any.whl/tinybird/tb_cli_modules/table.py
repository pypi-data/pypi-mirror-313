# Standard library modules.
import collections
import re

# Modules included in our package.
from humanfriendly.compat import coerce_string
from humanfriendly.tables import format_robust_table
from humanfriendly.terminal import (
    ansi_strip,
    ansi_width,
    ansi_wrap,
    find_terminal_size,
    terminal_supports_colors,
)

from tinybird.feedback_manager import bcolors

NUMERIC_DATA_PATTERN = re.compile(r"^\d+(\.\d+)?$")


def format_table(data, columns):
    """
    Render tabular data using the most appropriate representation.

    :param data: An iterable (e.g. a :func:`tuple` or :class:`list`)
                 containing the rows of the table, where each row is an
                 iterable containing the columns of the table (strings).
    :param column_names: An iterable of column names (strings).
    :returns: The rendered table (a string).

    If you want an easy way to render tabular data on a terminal in a human
    friendly format then this function is for you! It works as follows:

    - If the input data doesn't contain any line breaks the function
      :func:`format_pretty_table()` is used to render a pretty table. If the
      resulting table fits in the terminal without wrapping the rendered pretty
      table is returned.

    - If the input data does contain line breaks or if a pretty table would
      wrap (given the width of the terminal) then the function
      :func:`format_robust_table()` is used to render a more robust table that
      can deal with data containing line breaks and long text.
    """
    # Normalize the input in case we fall back from a pretty table to a robust
    # table (in which case we'll definitely iterate the input more than once).
    data = [normalize_columns(r) for r in data]

    column_names = []
    column_types = []

    for c in columns:
        column_names.append(c["name"])
        column_types.append(c["type"])

    column_names = normalize_columns(column_names)
    # Make sure the input data doesn't contain any line breaks (because pretty
    # tables break horribly when a column's text contains a line break :-).
    if not any(any("\n" in c for c in r) for r in data):
        # Render a pretty table.
        pretty_table = format_pretty_table(data, column_names, column_types)
        # Check if the pretty table fits in the terminal.
        table_width = max(map(ansi_width, pretty_table.splitlines()))
        num_rows, num_columns = find_terminal_size()
        if table_width <= num_columns:
            # The pretty table fits in the terminal without wrapping!
            return pretty_table
    # Fall back to a robust table when a pretty table won't work.
    return format_robust_table(data, column_names)


def format_pretty_table(data, column_names=None, column_types=None, horizontal_bar="─", vertical_bar=" "):
    """
    Render a table using characters like dashes and vertical bars to emulate borders.

    :param data: An iterable (e.g. a :func:`tuple` or :class:`list`)
                 containing the rows of the table, where each row is an
                 iterable containing the columns of the table (strings).
    :param column_names: An iterable of column names (strings).
    :param column_types: An iterable of column types (strings).
    :param horizontal_bar: The character used to represent a horizontal bar (a
                           string).
    :param vertical_bar: The character used to represent a vertical bar (a
                         string).
    :returns: The rendered table (a string).

    Here's an example:

    >>> from humanfriendly.tables import format_pretty_table
    >>> column_names = ['Version', 'Uploaded on', 'Downloads']
    >>> humanfriendly_releases = [
    ... ['1.23', '2015-05-25', '218'],
    ... ['1.23.1', '2015-05-26', '1354'],
    ... ['1.24', '2015-05-26', '223'],
    ... ['1.25', '2015-05-26', '4319'],
    ... ['1.25.1', '2015-06-02', '197'],
    ... ]
    >>> print(format_pretty_table(humanfriendly_releases, column_names))
    -------------------------------------
    | Version | Uploaded on | Downloads |
    -------------------------------------
    | 1.23    | 2015-05-25  |       218 |
    | 1.23.1  | 2015-05-26  |      1354 |
    | 1.24    | 2015-05-26  |       223 |
    | 1.25    | 2015-05-26  |      4319 |
    | 1.25.1  | 2015-06-02  |       197 |
    -------------------------------------

    Notes about the resulting table:

    - If a column contains numeric data (integer and/or floating point
      numbers) in all rows (ignoring column names of course) then the content
      of that column is right-aligned, as can be seen in the example above. The
      idea here is to make it easier to compare the numbers in different
      columns to each other.

    - The column names are highlighted in color so they stand out a bit more
      (see also :data:`.HIGHLIGHT_COLOR`). The following screen shot shows what
      that looks like (my terminals are always set to white text on a black
      background):

      .. image:: images/pretty-table.png
    """
    # Normalize the input because we'll have to iterate it more than once.
    data = [normalize_columns(r, expandtabs=True) for r in data]
    if column_names is not None:
        column_names = normalize_columns(column_names)
        if column_names:
            if terminal_supports_colors():
                column_names = [highlight_column_name(n) for n in column_names]
            data.insert(0, column_names)
            if column_types is not None:
                column_types = normalize_columns(column_types)
                column_types = [highlight_column_type(t) for t in column_types]
                data.insert(1, column_types)
    # Calculate the maximum width of each column.
    widths = collections.defaultdict(int)
    numeric_data = collections.defaultdict(list)
    for row_index, row in enumerate(data):
        for column_index, column in enumerate(row):
            widths[column_index] = max(widths[column_index], ansi_width(column))
            if not (column_names and row_index <= 1):  # Skip both header rows for numeric check
                numeric_data[column_index].append(bool(NUMERIC_DATA_PATTERN.match(ansi_strip(column))))

    horizontal_bar = highlight_horizontal_bar(horizontal_bar)
    # Create a horizontal bar of dashes as a delimiter.
    line_delimiter = horizontal_bar * (sum(widths.values()) + len(widths) * 3 + 1)
    # Start the table with a vertical bar.
    lines = []
    # Format the rows and columns.
    for row_index, row in enumerate(data):
        line = [vertical_bar]
        for column_index, column in enumerate(row):
            padding = " " * (widths[column_index] - ansi_width(column))
            if all(numeric_data[column_index]):
                line.append(" " + padding + column + " ")
            else:
                line.append(" " + column + padding + " ")
            line.append(vertical_bar)
        lines.append("".join(line))
        if column_names and column_types and row_index > 0 and row_index < len(data) - 1:
            lines.append(line_delimiter)
    # Join the lines, returning a single string.
    return "\n".join(lines)


def normalize_columns(row, expandtabs=False):
    results = []
    for value in row:
        text = coerce_string(value)
        if expandtabs:
            text = text.expandtabs()
        results.append(text)
    return results


def highlight_column_name(name):
    return ansi_wrap(name)


def highlight_column_type(type):
    return f"{bcolors.CGREY}\033[3m{type}\033[23m{bcolors.ENDC}"


def highlight_horizontal_bar(horizontal_bar):
    return f"{bcolors.CGREY}\033[3m{horizontal_bar}\033[23m{bcolors.ENDC}"
