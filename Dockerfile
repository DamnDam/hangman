FROM python:3.13-slim

RUN mkdir /app
WORKDIR /app

COPY pyproject.toml uv.lock .

ENV UV_PROJECT_ENVIRONMENT=/usr/local
RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    uv sync --locked --no-install-project --no-editable

ADD ./hangman /app/hangman

COPY data /app/data

CMD ["python", "hangman/cli.py"]