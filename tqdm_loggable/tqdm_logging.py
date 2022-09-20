import logging

from tqdm.auto import tqdm as tqdm_auto


logger = logging.getLogger(__name__)


class tqdm_logging(tqdm_auto):
    """A tqdm implementation that outputs to Python logger.

    - Any postfix progress bar arguments are passed as `extras` to the logging system

    See also

    - `Implementing structured logging <https://docs.python.org/3/howto/logging-cookbook.html#implementing-structured-logging>`_.
    """

    log_level = logging.INFO

    @classmethod
    def set_level(cls, log_level: int):
        """Set log level to all tqdm_logging instances.

        Currently we do not support per-instance logging level
        to maintain argument compatibility with std.tqdm constructor.
        """
        cls.log_level = log_level

    def set_postfix(self, ordered_dict=None, refresh=True, **kwargs):
        """Overloaded to store the raw post-fix"""
        self.raw_postfix = ordered_dict
        super(tqdm_logging, self).set_postfix(ordered_dict, refresh, **kwargs)


    def display(self, **kwargs):

        # super(tqdm_logging, self).display(**kwargs)

        # {'n': 0, 'total': 60, 'elapsed': 0, 'ncols': 344, 'nrows': 15, 'prefix': 'Sample progress', 'ascii': False, 'unit': 'it', 'unit_scale': False, 'rate': None, 'bar_format': None, 'postfix': None, 'unit_divisor': 1000, 'initial': 0, 'colour': None}
        # {'n': 7, 'total': 60, 'elapsed': 3.032935857772827, 'ncols': 344, 'nrows': 15, 'prefix': 'Sample progress', 'ascii': False, 'unit': 'it', 'unit_scale': False, 'rate': 2.0927977450656536, 'bar_format': None, 'postfix': 'Currently time=2022-09-20 21:08:26.951320', 'unit_divisor': 1000, 'initial': 0, 'colour': None}
        # ^C{'n': 3000, 'total': 60000, 'elapsed': 1.089920997619629, 'ncols': 344, 'nrows': 15, 'prefix': 'Sample progress', 'ascii': False, 'unit': 'it', 'unit_scale': True, 'rate': None, 'bar_format': None, 'postfix': 'Currently time=2022-09-20 21:10:24.377513', 'unit_divisor': 1000, 'initial': 0, 'colour': None}
        format_dict = self.format_dict
        name = format_dict.get("prefix", "unknown")
        postfix = format_dict.get("postfix", None)
        rate = format_dict.get("rate", 0)
        unit = format_dict.get("unit", "-")
        elapsed = format_dict.get("elapsed", 0)
        n = format_dict.get("n", 0)
        total = format_dict.get("total", -1)

        # Include any postfix variables in extra logging
        raw_postfix = getattr(self, "raw_postfix", {})

        # Structured log to be passed to Sentry / LogStash
        extra = {
            "progass_bar_name": name,
            "rate": rate,
            "unit": unit,
            "elapsed": elapsed,
            "n": n,
            "total": total,
            "postfix": raw_postfix,
        }

        logger.log(
            self.log_level,
            "Progress on:%s %f/%f rate:%s %s/s elapsed:%.4f postfix:%s",
            name,
            n,
            total,
            rate,
            unit,
            elapsed,
            postfix,
            extra=extra,
        )


