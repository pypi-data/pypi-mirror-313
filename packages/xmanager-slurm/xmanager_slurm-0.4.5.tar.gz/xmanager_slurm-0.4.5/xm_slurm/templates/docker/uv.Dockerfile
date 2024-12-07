# syntax=docker/dockerfile:1.4
ARG BASE_IMAGE=docker.io/python:3.10-slim-bookworm
FROM $BASE_IMAGE
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ARG EXTRA_SYSTEM_PACKAGES=""
ARG EXTRA_PYTHON_PACKAGES=""

WORKDIR /workspace

ENV UV_PYTHON_DOWNLOADS=0
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    git $EXTRA_SYSTEM_PACKAGES \
    && rm -rf /var/lib/apt/lists/*

RUN uv pip install --system pysocks $EXTRA_PYTHON_PACKAGES

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=ssh \
    uv sync --frozen --no-install-project --no-dev --no-editable

COPY --link . /workspace
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=ssh \
    uv sync --frozen --no-dev

ENV PATH="/workspace/.venv/bin:$PATH"

ENTRYPOINT [ "python" ]