import logging
import re
from datetime import datetime
from typing import Dict, List, Optional

import markdown


def time_ago(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    Modified from: http://stackoverflow.com/a/1551394/141084
    """

    now = datetime.now()
    if isinstance(time, int):
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = now - now
    else:
        raise ValueError("invalid date %s of type %s" % (time, type(time)))
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ""

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(int(second_diff / 60)) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(int(second_diff / 3600)) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(int(day_diff / 7)) + " weeks ago"
    if day_diff < 365:
        return str(int(day_diff / 30)) + " months ago"
    return str(int(day_diff / 365)) + " years ago"


def to_md(x):
    return markdown.markdown(x.decode())


def format_size(size, precision=2):
    suffixes = ["B", "KB", "MB", "GB", "TB"]
    suffixIndex = 0
    while size > 1024 and suffixIndex < 4:
        suffixIndex += 1  # increment the index of the suffix
        size = size / 1024.0  # apply the division
    return "%.*f%s" % (precision, size, suffixes[suffixIndex])


def remove_comments_from_line(line):
    pattern = r"#.*|(\'\'\'(.*?)\'\'\'|\"\"\"(.*?)\"\"\")"
    line_without_comments = re.sub(pattern, "", line)

    return line_without_comments


def get_error_text_from_exception(exception):
    """
    >>> from tinybird.tornado_template import ParseError, UnClosedIfError
    >>> syntax_error = SyntaxError('invalid syntax', ('<string>.generated.py', 5, 33, '    if defined((passenger_count):  # <string>:1'))
    >>> error = get_error_text_from_exception(syntax_error)
    >>> error
    'if defined((passenger_count)'
    >>> parse_error = ParseError('invalid template', '<string>.generated.py', 2, "{% import os %}{{ os.popen('ls').read()")
    >>> error = get_error_text_from_exception(parse_error)
    >>> error
    "{% import os %}{{ os.popen('ls').read("
    >>> unclosedif_error = UnClosedIfError('node', 3, "SELECT {% if defined(x) %} x, 1")
    >>> error = get_error_text_from_exception(unclosedif_error)
    >>> error
    'SELECT {% if defined(x) %} x, '
    """
    try:
        if hasattr(exception, "text"):
            text = remove_comments_from_line(exception.text)
            return text.strip()[:-1]
        if hasattr(exception, "_text"):
            text = remove_comments_from_line(exception._text)
            return text.strip()[:-1]
        if hasattr(exception, "sql"):
            text = remove_comments_from_line(exception.sql)
            return text.strip()[:-1]
    except Exception:
        pass
    return ""


def get_node_from_syntax_error(exception, pipes: Optional[List] = None, pipe_def: Optional[Dict] = None):
    """
    >>> from tinybird.user import User, Users, UserAccount
    >>> from tinybird.tornado_template import ParseError, UnClosedIfError
    >>> email = 'test_node_error@example.com'
    >>> name = 'test_node_error'
    >>> u = UserAccount.register(email, 'pass')
    >>> w = User.register(name, admin=u.id)
    >>> _ = Users.add_pipe_sync(w, 'test_pipe_with_node_error', nodes=[{'name': 'n_0', 'sql': "% SELECT 1 {% if defined((passenger_count) %} WHERE 1=1 {% end %}"}, {'name': 'n_1', 'sql': f"SELECT * FROM n_0"}])
    >>> w = Users.get_by_id(w.id)
    >>> pipes = w.get_pipes()
    >>> syntax_error = SyntaxError('invalid syntax', ('<string>.generated.py', 5, 33, '    if defined((passenger_count):  # <string>:1'))
    >>> error = get_node_from_syntax_error(syntax_error, pipes=pipes)
    >>> error
    ('test_pipe_with_node_error', 'n_0')
    >>> pipe_def = {"name": "pipe_def_name", "nodes": [{"name": "n_2", "sql":  "% SELECT * FROM {% import os %}{{ os.popen('ls').read() }}"}, {"name": "n_3", "sql": f"SELECT * FROM n_2"}]}
    >>> parse_error = ParseError('invalid template', '<string>.generated.py', 2, "{% import os %}{{ os.popen('ls').read()")
    >>> error = get_node_from_syntax_error(parse_error, pipe_def=pipe_def)
    >>> error
    ('pipe_def_name', 'n_2')
    >>> error = get_node_from_syntax_error(parse_error)
    >>> error
    (None, None)
    """

    if not pipes and not pipe_def:
        return None, None

    error = get_error_text_from_exception(exception)
    if not error:
        return None, None

    pipe_name = None
    node_name = None

    if pipes:
        try:
            for pipe in pipes:
                for node in pipe.pipeline.nodes:
                    if error in node._sql.strip():
                        pipe_name = pipe.name
                        node_name = node.name
        except Exception as e:
            logging.warning(f"Error while checking syntax error on pipe {pipe.name}: {e}")

    if pipe_def:
        try:
            for node in pipe_def.get("nodes", []):
                if error in node.get("sql"):
                    pipe_name = pipe_def.get("name")
                    node_name = node.get("name")
        except Exception as e:
            logging.warning(f"Error while checking syntax error on pipe def {pipe_def.get('name')}: {e}")

    return pipe_name, node_name


def parse_syntax_error(e) -> str:
    """
    >>> syntax_error = SyntaxError('invalid syntax', ('<string>.generated.py', 5, 33, '    if defined((passenger_count):  # <string>:1'))
    >>> e = parse_syntax_error(syntax_error)
    >>> str(e)
    'Syntax error: invalid syntax, line 1'
    """
    try:
        message = getattr(e, "msg", str(e)).split("(<string>.generated.py")[0].strip()
        text = getattr(e, "text", message)
        line = None
        try:
            line = re.findall(r"\<string\>:(\d*)", text)
            message = re.sub(r"\<string\>:(\d*)", "", message)
        except TypeError:
            pass

        message = message.strip()
        if line:
            comma = " " if message.endswith("at") else ", "
            error = f"Syntax error: {message}{comma}line {line[0]}"
            return error
        else:
            error = f"Syntax error: {message}"
            return error
    except Exception as e:
        logging.exception(f"Error while parsing syntax error: {e}")
        error = f"Syntax error: {str(e)}"
        return error
