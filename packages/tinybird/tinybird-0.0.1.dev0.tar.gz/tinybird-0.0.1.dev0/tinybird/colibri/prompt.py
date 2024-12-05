import logging
import sys
from typing import Any, Generator, Optional

from click import prompt
from click.termui import confirm, style

# Modules included in our package.
from humanfriendly.terminal import warning
from humanfriendly.text import concatenate, format

MAX_ATTEMPTS = 10
"""The number of times an interactive prompt is shown on invalid input (an integer)."""

# Initialize a logger for this module.
logger = logging.getLogger(__name__)


def prompt_for_confirmation(question: str, default: Optional[bool] = None) -> bool:
    prompt_text = question
    prompt_text = prepare_prompt_text(prompt_text, bold=True)
    return confirm(prompt_text, default=default)


def prompt_for_choice(
    choices: list[str], default: Optional[str] = None, padding: Optional[bool] = True
) -> str | Any | None:
    indent = " " if padding else ""
    # Make sure we can use 'choices' more than once (i.e. not a generator).
    choices = list(choices)
    if len(choices) == 1:
        # If there's only one option there's no point in prompting the user.
        logger.debug("Skipping interactive prompt because there's only option (%r).", choices[0])
        return choices[0]
    elif not choices:
        # We can't render a choice prompt without any options.
        raise ValueError("Can't prompt for choice without any options!")
    # Generate the prompt text.
    prompt_text = ("\n\n" if padding else "\n").join(
        [
            # Present the available choices in a user friendly way.
            "\n".join(
                [
                    " %i. %s" % (i, choice) + (" (default choice)" if choice == default else "")
                    for i, choice in enumerate(choices, start=1)
                ]
            ),
            # Instructions for the user.
            "Enter your choice as a number or unique substring (Control-C aborts)",
        ]
    )
    # Loop until a valid choice is made.
    logger.debug("Requesting interactive choice on terminal (options are %s) ..", concatenate(map(repr, choices)))
    for attempt in retry_limit():
        reply = prompt_for_input(prompt_text, "", padding=padding)
        if not reply and default is not None:
            logger.debug("Default choice selected by empty reply (%r).", default)
            return default
        elif reply.isdigit():
            index = int(reply) - 1
            if 0 <= index < len(choices):
                logger.debug("Option (%r) selected by numeric reply (%s).", choices[index], reply)
                return choices[index]
        # Check for substring matches.
        matches = []
        for choice in choices:
            lower_reply = reply.lower()
            lower_choice = choice.lower()
            if lower_reply == lower_choice:
                # If we have an 'exact' match we return it immediately.
                logger.debug("Option (%r) selected by reply (exact match).", choice)
                return choice
            elif lower_reply in lower_choice and len(lower_reply) > 0:
                # Otherwise we gather substring matches.
                matches.append(choice)
        if len(matches) == 1:
            # If a single choice was matched we return it.
            logger.debug("Option (%r) selected by reply (substring match on %r).", matches[0], reply)
            return matches[0]
        else:
            # Give the user a hint about what went wrong.
            if matches:
                details = format("text '%s' matches more than one choice: %s", reply, concatenate(matches))
            elif reply.isdigit():
                details = format("number %i is not a valid choice", int(reply))
            elif reply and not reply.isspace():
                details = format("text '%s' doesn't match any choices", reply)
            else:
                details = "there's no default choice"
            logger.debug(
                "Got %s reply (%s), retrying (%i/%i) ..",
                "invalid" if reply else "empty",
                details,
                attempt,
                MAX_ATTEMPTS,
            )
            warning("%sError: Invalid input (%s).", indent, details)
    return None


def prompt_for_input(question: str, default: Optional[str] = None, padding: Optional[bool] = True) -> str:
    reply = None
    try:
        # Prefix an empty line to the text and indent by one space?
        if padding:
            question = "\n" + question
            question = question.replace("\n", "\n ")
        # Render the prompt and wait for the user's reply.
        try:
            reply = prompt(prepare_prompt_text(question))
        finally:
            if reply is None:
                # If the user terminated the prompt using Control-C or
                # Control-D instead of pressing Enter no newline will be
                # rendered after the prompt's text. The result looks kind of
                # weird:
                #
                #   $ python -c 'print(raw_input("Are you sure? "))'
                #   Are you sure? ^CTraceback (most recent call last):
                #     File "<string>", line 1, in <module>
                #   KeyboardInterrupt
                #
                # We can avoid this by emitting a newline ourselves if an
                # exception was raised (signaled by `reply' being None).
                sys.stderr.write("\n")
            if padding:
                # If the caller requested (didn't opt out of) `padding' then we'll
                # emit a newline regardless of whether an exception is being
                # handled. This helps to make interactive prompts `stand out' from
                # a surrounding `wall of text' on the terminal.
                sys.stderr.write("\n")
    except BaseException as e:
        if isinstance(e, EOFError) and default is not None:
            # If standard input isn't connected to an interactive terminal
            # but the caller provided a default we'll return that.
            logger.debug("Got EOF from terminal, returning default value (%r) ..", default)
            return default
        else:
            # Otherwise we log that the prompt was interrupted but propagate
            # the exception to the caller.
            logger.warning("Interactive prompt was interrupted by exception!", exc_info=True)
            raise
    if default is not None and not reply:
        # If the reply is empty and `default' is None we don't want to return
        # None because it's nicer for callers to be able to assume that the
        # return value is always a string.
        return default
    elif reply is None:
        sys.exit()
    else:
        return str(reply).strip()


def prepare_prompt_text(prompt_text: str, blink: Optional[bool] = False, bold: Optional[bool] = True) -> str:
    return style(prompt_text, blink=blink, bold=bold)


def retry_limit(limit: int = MAX_ATTEMPTS) -> Generator[int, Any, None]:
    for i in range(limit):
        yield i + 1
    msg = "Received too many invalid replies on interactive prompt, giving up! (tried %i times)"
    formatted_msg = msg % limit
    # Make sure the event is logged.
    logger.warning(formatted_msg)
    # Force the caller to decide what to do now.
    raise TooManyInvalidReplies(formatted_msg)


class TooManyInvalidReplies(Exception):
    """Raised by interactive prompts when they've received too many invalid inputs."""
