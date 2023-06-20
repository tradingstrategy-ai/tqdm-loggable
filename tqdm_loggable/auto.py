from .utils import is_interactive_session, is_stdout_only_session

if is_interactive_session() and not is_stdout_only_session():
    from tqdm.auto import tqdm
    INTERACTIVE_TQDM = True
elif is_stdout_only_session():
    from tqdm import tqdm
    INTERACTIVE_TQDM = False
else:
    from .tqdm_logging import tqdm_logging as tqdm
    INTERACTIVE_TQDM = False

__all__ = ["tqdm"]