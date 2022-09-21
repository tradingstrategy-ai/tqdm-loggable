"""Manual tests.

See README how to run.
"""
import datetime
import logging
import os
import sys
import time

from .utils import is_interactive_session

from tqdm_loggable.auto import tqdm
from tqdm_loggable.tqdm_logging import tqdm_logging


logger = logging.getLogger(__name__)


def main():
    fmt = f"%(filename)-20s:%(lineno)-4d %(asctime)s %(message)s"
    logging.basicConfig(level=logging.INFO, format=fmt, handlers=[logging.StreamHandler()])

    # Set the log level to all tqdm-logging progress bars
    tqdm_logging.set_level(logging.INFO)

    # Set the rate how often we update logs
    tqdm_logging.set_log_rate(datetime.timedelta(seconds=10))

    print("tqdm-loggable manual tests")
    print("sys.stdout.isatty():", sys.stdout.isatty())
    print("TERM:", os.environ.get("TERM", "-"))
    print("is_interactive_session():", is_interactive_session())

    logger.info("This is an INFO test message using Python logging")

    with tqdm(desc="Progress bar without total") as progress_bar:
        for i in range(20):
            progress_bar.update(500)
            time.sleep(0.1)

    with tqdm(total=60_000, desc="Sample progress", unit_scale=True) as progress_bar:
        for i in range(60):
            progress_bar.update(1000)

            # Test postfix output
            progress_bar.set_postfix({"Current time": datetime.datetime.utcnow()})

            time.sleep(0.5)
