tqam_loggable
=============

Logging friendly TQDM progress bars.

If your Python code has `tqdm` progress bars and you use them in a non-interactive session like 

- Background worker
- Docker container
- Edge computing
- Logstash or other external logs
- Long running machine learning tasks
- ...or [Stdout](https://en.wikipedia.org/wiki/Standard_streams) is otherwise not available or redirected

...you cannot have nice ANSI coloured progress bar. 

In these situations `tqdm-loggable` will automatically turn your `tqdm` progress bars to loggable progress messages
that can be read in headless systems.


`tqdm-loggable` will

- Use Python [logging](https://docs.python.org/3/library/logging.html) subsystem to report status instead of terminal
- Print a log line for every X seconds
- [The logging messages are structured](https://docs.python.org/3/howto/logging-cookbook.html#implementing-structured-logging), so they work with Sentry, LogStash, etc. rich logging services
  which provide advanced searching and tagging by variables

Here is a sample `tqdm` log message output in plain text logs:

```
tqdm_logging.py     :66   2022-09-20 23:30:48,667 Progress on:Sample progress 0.000000/60000.000000 rate:None it/s elapsed:0.0000 postfix:None
tqdm_logging.py     :66   2022-09-20 23:30:48,667 Progress on:Sample progress 1000.000000/60000.000000 rate:None it/s elapsed:0.0002 postfix:Current time=2022-09-20 21:30:48.667763
tqdm_logging.py     :66   2022-09-20 23:30:49,175 Progress on:Sample progress 2000.000000/60000.000000 rate:3944.6880828079934 it/s elapsed:0.5071 postfix:Current time=2022-09-20 21:30:48.667763
tqdm_logging.py     :66   2022-09-20 23:30:49,176 Progress on:Sample progress 2000.000000/60000.000000 rate:3944.6880828079934 it/s elapsed:0.5086 postfix:Current time=2022-09-20 21:30:49.175720
tqdm_logging.py     :66   2022-09-20 23:30:49,676 Progress on:Sample progress 3000.000000/60000.000000 rate:2800.3272375400925 it/s elapsed:1.0092 postfix:Current time=2022-09-20 21:30:49.175720
tqdm_logging.py     :66   2022-09-20 23:30:49,677 Progress on:Sample progress 3000.000000/60000.000000 rate:2800.3272375400925 it/s elapsed:1.0095 postfix:Current time=2022-09-20 21:30:49.677158
tqdm_logging.py     :66   2022-09-20 23:30:50,182 Progress on:Sample progress 4000.000000/60000.000000 rate:2423.8261963519526 it/s elapsed:1.5151 postfix:Current time=2022-09-20 21:30:49.677158
tqdm_logging.py     :66   2022-09-20 23:30:50,183 Progress on:Sample progress 4000.000000/60000.000000 rate:2423.8261963519526 it/s elapsed:1.5160 postfix:Current time=2022-09-20 21:30:50.183488
tqdm_logging.py     :66   2022-09-20 23:30:50,687 Progress on:Sample progress 5000.000000/60000.000000 rate:2249.4302448431927 it/s elapsed:2.0196 postfix:Current time=2022-09-20 21:30:50.183488
tqdm_logging.py     :66   2022-09-20 23:30:50,688 Progress on:Sample progress 5000.000000/60000.000000 rate:2249.4302448431927 it/s elapsed:2.0205 postfix:Current time=2022-09-20 21:30:50.688095
```

Note that `tqdm-loggable` is not to be confused with [tqdm.contrib.logging](https://tqdm.github.io/docs/contrib.logging/) 
that is very different approach for a different problem.

Installation
------------

The package name is `tqdm-loggable.` [Read Python packaging manual](https://packaging.python.org/en/latest/) on how to install packages
on your system.

Usage
-----

The only things you need to do

- Change import from `from tqdm.auto import tqdm` to `from tqdm_loggable.auto import tqdm`
- Optionally call `tqdm_logging.set_level()`

Here is [an example script](./tqdm_loggable/manual_tests.py): 


```python
import datetime
import logging
import time

from tqdm_loggable.auto import tqdm
from tqdm_loggable.tqdm_logging import tqdm_logging


logger = logging.getLogger(__name__)


def main():
    fmt = f"%(filename)-20s:%(lineno)-4d %(asctime)s %(message)s"
    logging.basicConfig(level=logging.INFO, format=fmt, handlers=[logging.StreamHandler()])

    # Set the log level to all tqdm-logging progress bars.
    # Defaults to info - no need to set if you do not want to change the level
    tqdm_logging.set_level(logging.INFO)

    logger.info("This is an INFO test message using Python logging")

    with tqdm(total=60_000, desc="Sample progress", unit_scale=True) as progress_bar:
        for i in range(60_000):
            progress_bar.update(1000)

            # Test postfix output
            progress_bar.set_postfix({"Current time": datetime.datetime.utcnow()})

            time.sleep(0.5)

```

`tqdm_loggable` will detect non-interactive sessions.
If the application is running without a proper terminal, non-interactive progress messages will be used.
Otherwise progress bar is delegated `tqdm.auto` module to maintain the compatibility
with any `tqdm` system without any changes to code.

Development
-----------

You can use [tqdm_loggable/manual_tests.py](./tqdm_loggable/manual_tests.py) to run the various checks 
to see what different interactive and non-interactive sessions give for you.

```shell
# Normal interactive terminal run
poetry run manual-tests 
```

or

```shell
# Disable interactive terminal by fiddling with TERM environment variable
TERM=dumb poetry run manual-tests 
```

or

```shell
docker build -t manual-tests . && docker run manual-tests
docker build -t manual-tests . && docker run -ti manual-tests
```

or

```shell
poetry run manual-tests > output.txt
cat output.txt
```

These will output our terminal detection info and draw a progress bar, total 30 seconds.

```
tqdm-loggable manual tests
sys.stdout.isatty(): False
TERM: -
is_interactive_session(): False
```

and further progress bar or progress messages will follow depending
if you run the manual test interactively or not.

See also
--------

- [python-discord-logging-handler](https://github.com/tradingstrategy-ai/python-logging-discord-handler)
- [python-logstash](https://github.com/tradingstrategy-ai/python-logstash)

Kudos
-----

Originally build for [Trading Strategy blockchain trade automation](https://tradingstrategy.ai/docs/).

[See the original StackOverflow question](https://stackoverflow.com/questions/73433322/tqdm-progress-bar-with-docker-logs).

License
-------

MIT