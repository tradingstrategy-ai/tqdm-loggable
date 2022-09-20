from .utils import is_interactive_session

if is_interactive_session():
    from tqdm.auto import tqdm
    INTERACTIVE_TQDM = True
else:
    from .tqdm_logging import tqdm_logging as tqdm
    INTERACTIVE_TQDM = False

__all__ = ["tqdm"]