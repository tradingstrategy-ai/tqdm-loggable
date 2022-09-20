#
# Build trade-executor as a Docker container
#
# See https://stackoverflow.com/a/71786211/315168 for the recipe
#
# Base image
#
FROM python:3.10.4

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1

# Install Poetry, with a specific version tag
RUN apt-get update \
    && apt-get install curl -y \
    && curl -sSL https://install.python-poetry.org | python - --version 1.2.1

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /usr/src/tqdm-loggablle

# package source code
COPY . .

# Instal our package
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

CMD ["poetry", "run", "manual-tests"]
