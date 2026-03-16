# 0.4

- Fix: Restore Datalore stdout-only detection for current runtimes that expose `DATALORE_*` environment variables instead of `AGENT_MANAGER_HOST=datalore` (2026-03-16)
- Add: `TQDM_LOGGABLE_FORCE=stdout|logging|auto` environment override for deterministic progress rendering in notebook kernels and batch runners like `jupyter execute` (2026-03-15)
- Add: tests covering forced stdout and logging selection in `tqdm_loggable.auto` (2026-03-15)
- Docs: document the override for notebook kernels that should render progress in the calling TTY instead of widget/HTML output (2026-03-15)

# 0.3

- Add: Python 3.14 compatibility (2026-02-10)
- Fix: Replace deprecated `datetime.utcfromtimestamp()` and `datetime.utcnow()` calls (2026-02-10)
- Add: GitHub Actions CI workflow for Python 3.10-3.14 (2026-02-10)
- Add: pytest test suite (2026-02-10)
- Change: Bump minimum Python version to 3.10 (2026-02-10)

# 0.2

- Add: Invert rate display to s/it if rate is less than 1 by https://github.com/elephantum
- Fix: Do not add extra new line when closing progress bar by https://github.com/danielnelson
- Fix: Unpin dependencies

# 0.1.4

- Fix [TQDM auto compatibility with Datalore](https://github.com/tradingstrategy-ai/tqdm-loggable/pull/4)

# 0.1.3

- Fix compatibility with python-logstash

# 0.1.2

- Do not attempt to display progress bar in Github Actions continous integration jobs

# 0.1.1

- Fix displaying progress bars in the use case "running Jupyter notebook inside Docker"
