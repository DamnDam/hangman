FROM python:3.13-slim

RUN mkdir /app
WORKDIR /app

COPY pyproject.toml uv.lock .

RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    uv sync

ADD ./hangman /app/hangman

COPY words.txt .

CMD ["uv", "run", "online-hangman/cli.py"]