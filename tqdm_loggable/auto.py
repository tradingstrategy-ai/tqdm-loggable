"""Choose the best tqdm implementation for the current environment."""

from .utils import get_forced_progress_mode, is_interactive_session, is_stdout_only_session

# Allow callers to override auto-detection in cases like `jupyter execute`,
# where we are inside an IPython kernel but still want terminal progress.
forced_mode = get_forced_progress_mode()

if forced_mode == "stdout":
    from tqdm import tqdm
    INTERACTIVE_TQDM = False
elif forced_mode == "logging":
    from .tqdm_logging import tqdm_logging as tqdm
    INTERACTIVE_TQDM = False
elif is_interactive_session() and not is_stdout_only_session():
    # Notebook-like environments still default to tqdm's interactive frontend.
    from tqdm.auto import tqdm
    INTERACTIVE_TQDM = True
elif is_stdout_only_session():
    # Environments like Datalore need plain stdout output instead of widgets.
    from tqdm import tqdm
    INTERACTIVE_TQDM = False
else:
    # Fall back to logging when neither a TTY nor stdout-style progress is safe.
    from .tqdm_logging import tqdm_logging as tqdm
    INTERACTIVE_TQDM = False

__all__ = ["tqdm"]
