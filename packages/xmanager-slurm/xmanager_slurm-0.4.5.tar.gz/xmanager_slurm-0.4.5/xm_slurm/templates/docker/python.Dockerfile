# syntax=docker/dockerfile:1.4
ARG BASE_IMAGE=docker.io/python:3.10-slim-bookworm
FROM $BASE_IMAGE as builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ARG EXTRA_SYSTEM_PACKAGES=""
ARG EXTRA_PYTHON_PACKAGES=""

ENV UV_PYTHON_DOWNLOADS=0
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /workspace

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    git $EXTRA_SYSTEM_PACKAGES \
    && rm -rf /var/lib/apt/lists/*

# Install and update necesarry global Python packages
RUN uv pip install --system pysocks $EXTRA_PYTHON_PACKAGES

ARG PIP_REQUIREMENTS=requirements.txt

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=$PIP_REQUIREMENTS,target=requirements.txt \
    --mount=type=ssh \
    uv pip install --system --requirement requirements.txt

COPY --link . /workspace

ENTRYPOINT [ "python" ]