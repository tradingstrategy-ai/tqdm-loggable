"""The bag of utility functions."""

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

#: Stable Datalore environment markers seen in current notebook runtimes.
#:
#: `AGENT_MANAGER_HOST=datalore` was used by older environments, but newer
#: instances expose Datalore-specific variables instead.
DATALORE_ENV_VARS = [
    "DATALORE_AGENT_MODE",
    "DATALORE_HOME",
    "DATALORE_USER",
]


def get_forced_progress_mode() -> str | None:
    """Get forced progress rendering mode from environment.

    Supported values:

    - ``auto``: Use the normal automatic detection
    - ``stdout``: Force plain terminal/stdout tqdm
    - ``logging``: Force logging-based tqdm

    The value is case-insensitive.
    Invalid values are ignored.
    """

    # This override exists for mixed environments where auto-detection is
    # technically correct about "being in a notebook" but wrong about the
    # desired output channel.
    value = os.environ.get("TQDM_LOGGABLE_FORCE", None)
    if value is None:
        return None

    value = value.strip().lower()
    if value in {"auto", "stdout", "logging"}:
        return value

    return None


def is_interactive_session() -> bool:
    """Guess if we are an interactive session and can render real progress bars."""

    if is_notebook():
        return True

    if is_continous_integration():
        return False

    if not sys.stdout.isatty():
        return False

    term = os.environ.get("TERM", None)
    if term:
        term = term.lower()

    if term in NON_INTERACTIVE_TERM_VALUES:
        return False

    return True


def is_notebook() -> bool:
    """Guess if we are an in Jupyter notebook environment."""

    try:
        from IPython import get_ipython
        if "IPKernelApp" not in get_ipython().config:
            return False
    except ImportError:
        return False
    except AttributeError:
        return False
    return True


def is_continous_integration() -> bool:
    """Disable progress bars in continous integration systems.

    Github Actions (and other CI) may allocate an interactive
    terminal for a job. However, in case of Github,
    they do not seem to be able to refresh the progress bar correctly,
    floooding the CI log with progress bar lines.
    """
    # https://docs.github.com/en/actions/learn-github-actions/environment-variables#default-environment-variables
    return "CI" in os.environ


def is_stdout_only_session() -> bool:
    """Guess if we are in a session where only stdout is available.

    Datalore is an example of such environment. Datalore provides code autocompletion
    and documentation pop ups, as well as other features that make it desirable to use.
    See https://www.jetbrains.com/datalore/

    A code report has been privately logged to Datalore support for enquiring about the
    feature disparity between Datalore and Jupyter Notebooks.
    """
    if os.environ.get("AGENT_MANAGER_HOST", None) == "datalore":
        return True

    return any(os.environ.get(name) for name in DATALORE_ENV_VARS)
