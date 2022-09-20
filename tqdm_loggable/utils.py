import os
import sys

#: List of possible non-interactive terminal values
#: for TERM environment variable.
#:
#: Further info:
#:
#: https://stackoverflow.com/questions/73433322/tqdm-progress-bar-with-docker-logs
#:
#: https://stackoverflow.com/questions/1512457/determining-if-stdout-for-a-python-process-is-redirected
#:
#: https://unix.stackexchange.com/questions/528323/what-uses-the-term-variable
#:
NON_INTERACTIVE_TERM_VALUES = ["dumb", "", None]


def is_interactive_session() -> bool:
    """Guess if we are an interactive session and can render real progress bars."""

    if not sys.stdout.isatty():
        return False

    term = os.environ.get("TERM", None)
    if term:
        term = term.lower()

    if term in NON_INTERACTIVE_TERM_VALUES:
        return False

    return True