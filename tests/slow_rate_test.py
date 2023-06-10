import time
import logging
from tqdm_loggable.auto import tqdm

logging.basicConfig(level=logging.INFO)


for i in tqdm(range(10)):
    time.sleep(5)
