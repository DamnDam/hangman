FROM python:3.13

RUN mkdir /app
WORKDIR /app

ENV UV_PROJECT_ENVIRONMENT=/usr/local
ENV UV_COMPILE_BYTECODE=1
ENV UV_NO_CACHE=1
RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    --mount=type=bind,source=./,target=/app,readonly \
    uv sync --locked --no-editable

COPY words.txt ./

ENTRYPOINT ["hangman"]