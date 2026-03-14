"""Test tqdm_logging produces no deprecation warnings and works correctly."""

import importlib
import logging
import sys
import warnings
from datetime import timedelta

from tqdm_loggable.tqdm_logging import tqdm_logging, _utc_epoch


def test_no_deprecation_warnings(caplog):
    """Ensure tqdm_logging emits no DeprecationWarning on Python 3.12+."""
    with warnings.catch_warnings():
        warnings.filterwarnings("error", category=DeprecationWarning)
        tqdm_logging.set_log_rate(timedelta(seconds=0))

        with caplog.at_level(logging.INFO):
            with tqdm_logging(total=5, desc="Test") as t:
                for _ in range(5):
                    t.update(1)


def test_utc_epoch():
    """Ensure _utc_epoch returns the Unix epoch as a naive datetime."""
    epoch = _utc_epoch()
    assert epoch.year == 1970
    assert epoch.month == 1
    assert epoch.day == 1
    assert epoch.tzinfo is None


def test_progress_bar_without_total(caplog):
    """Ensure progress bar works without a total."""
    tqdm_logging.set_log_rate(timedelta(seconds=0))

    with caplog.at_level(logging.INFO):
        with tqdm_logging(desc="No total") as t:
            for _ in range(3):
                t.update(1)

    assert any("No total" in record.message for record in caplog.records)


def test_auto_import():
    """Ensure the auto module imports without error."""
    from tqdm_loggable.auto import tqdm
    assert tqdm is not None


def _reload_auto_module():
    """Reload auto selection after environment changes."""
    sys.modules.pop("tqdm_loggable.auto", None)
    return importlib.import_module("tqdm_loggable.auto")


def test_force_stdout_mode(monkeypatch):
    """Ensure stdout mode can be forced explicitly."""
    from tqdm import tqdm as terminal_tqdm

    monkeypatch.setenv("TQDM_LOGGABLE_FORCE", "stdout")
    auto_module = _reload_auto_module()

    assert auto_module.tqdm is terminal_tqdm
    assert auto_module.INTERACTIVE_TQDM is False


def test_force_logging_mode(monkeypatch):
    """Ensure logging mode can be forced explicitly."""
    monkeypatch.setenv("TQDM_LOGGABLE_FORCE", "logging")
    auto_module = _reload_auto_module()

    assert auto_module.tqdm is tqdm_logging
    assert auto_module.INTERACTIVE_TQDM is False


def test_invalid_force_mode_is_ignored(monkeypatch):
    """Ensure invalid override values fall back to auto detection."""
    monkeypatch.setenv("TQDM_LOGGABLE_FORCE", "bad-value")
    auto_module = _reload_auto_module()

    assert auto_module.tqdm is not None
