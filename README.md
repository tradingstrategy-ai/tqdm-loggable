tqdm-loggable
=============

`tqdm-loggable` is a petite Python package providing logging friendly TQDM progress bars.

If your Python application has [tqdm](https://tqdm.github.io/) progress bars and you use them in a non-interactive session like... 

- Background worker
- Docker container
- Edge computing
- [Logstash](https://www.elastic.co/logstash/), [Sentry](https://docs.sentry.io/platforms/python/), [Datadog](https://docs.datadoghq.com/logs/log_collection/python/?tab=jsonlogformatter) or other external log tools
- Long-running machine learning tasks
- ...or [stdout](https://en.wikipedia.org/wiki/Standard_streams) stream is otherwise not available or redirected

...you cannot have interactive progress bar. What happens is that if you are observing
your application using monitoring tools, you usually do not see anything happening while your
application is having`tqdm` progress ongoing. If the progress bar'ed operation takes few minutes your appliaction
may appear frozen. This is  fixed by `tqdm-logging` by sending a regular reports about your progress to logging backend like files and log monitoring
tools.

In these situations `tqdm-loggable` will automatically turn your `tqdm` progress bars to loggable progress messages
that can be read in headless systems.

`tqdm-loggable`... 

- Is a drop-in replacement for the normal `tqdm` - nothing changes unless non-interactive session is detected
- Uses Python [logging](https://docs.python.org/3/library/logging.html) subsystem to report status instead of terminal
- Print a log line for every X seconds
- [The logging messages are structured](https://docs.python.org/3/howto/logging-cookbook.html#implementing-structured-logging), so they work with Sentry, LogStash, etc. rich logging services
  which provide advanced searching and tagging by variables
- Special support for Github Actions and other continous integration environments

Here is a sample `tqdm` log message output in plain text logs:

```
tqdm_logging.py     :139  2022-09-21 12:13:44,138 Progress on:Progress bar without total -/- rate:- remaining:? elapsed:00:00 postfix:-
tqdm_logging.py     :139  2022-09-21 12:13:46,225 Progress on:Progress bar without total 10000/- rate:- remaining:? elapsed:00:02 postfix:-

tqdm_logging.py     :139  2022-09-21 12:13:46,225 Progress on:Sample progress -/60000 rate:- remaining:? elapsed:00:00 postfix:-
tqdm_logging.py     :139  2022-09-21 12:13:56,307 Progress on:Sample progress 21.0kit/60.0kit rate:1,982.9it/s remaining:00:19 elapsed:00:10 postfix:Current time=2022-09-21 10:13:55.801787
tqdm_logging.py     :139  2022-09-21 12:14:06,392 Progress on:Sample progress 41.0kit/60.0kit rate:1,984.1it/s remaining:00:09 elapsed:00:20 postfix:Current time=2022-09-21 10:14:05.890220
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

- Make sure your [Python logging system is properly configured](https://docs.python.org/3/howto/logging.html)
- Change import from `from tqdm.auto import tqdm` to `from tqdm_loggable.auto import tqdm`
- Optionally call `tqdm_logging.set_level()` at the init of your application
- Optionally call `tqdm_logging.set_log_rate()` at the init of your application

Search and replace instructions for your Python codebase:

```
from tqdm import tqdm -> from tqdm_loggable.auto import tqdm 
from tqdm.auto import tqdm -> from tqdm_loggable.auto import tqdm
```

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
    
    # Set the rate how often we update logs
    # Defaults to 10 seconds - optional
    tqdm_logging.set_log_rate(datetime.timedelta(seconds=10))    

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

`tqdm_loggable` has also progress bar workarounds for [Jupyter Notebook environments](https://jupyter.org/)
like [Datalore](https://www.jetbrains.com/datalore/) which [are not 100% compatible](https://jupyter.org/) with the original Jupyter Notebook.

The Python logger instance used to log the messages is named `tqqm_loggable.tqm_logging`.

Development
-----------

You can use [tqdm_loggable/manual_tests.py](./tqdm_loggable/manual_tests.py) to run the various checks 
to see what different interactive and non-interactive sessions give for you.

```shell
# Normal interactive terminal run
poetry run manual-tests 
```

Because this is a normal shell session you will get a normal progress bar:

```
Sample progress:  20%|████████▏                                | 12.0k/60.0k [00:05<00:24, 1.98kit/s, Current time=2022-09-21 15:40:24.274670]
```

...then test without without a proper [TERM environment variable](https://unix.stackexchange.com/questions/528323/what-uses-the-term-variable):

```shell
# Disable interactive terminal by fiddling with TERM environment variable
TERM=dumb poetry run manual-tests 
```

You get log messages:

```
tqdm_logging.py     :139  2022-09-21 17:41:20,720 Progress on:Sample progress -/60000 rate:- remaining:? elapsed:00:00 postfix:-
tqdm_logging.py     :139  2022-09-21 17:41:30,803 Progress on:Sample progress 21.0kit/60.0kit rate:1,984.7it/s remaining:00:19 elapsed:00:10 postfix:Current time=2022-09-21 15:41:30.300714
```

...or with different Docker sessions:

```shell
# This will display process as log messages
docker build -t manual-tests . && docker run manual-tests

# This will allocate a terminal and display progress as a normal tqdm progress bar
docker build -t manual-tests . && docker run -ti manual-tests
```

or with redirected stdout:

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

See other relevant logging packages:

- [tqdm-loggable on PyPi](https://pypi.org/project/tqdm-loggable/)
- [python-discord-logging-handler](https://github.com/tradingstrategy-ai/python-logging-discord-handler)
- [python-logstash](https://github.com/tradingstrategy-ai/python-logstash)

Kudos
-----

Originally build for [Trading Strategy blockchain trade automation](https://tradingstrategy.ai/docs/).

[See the original StackOverflow question](https://stackoverflow.com/questions/73433322/tqdm-progress-bar-with-docker-logs).

License
-------

MIT