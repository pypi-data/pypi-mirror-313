# syntax=docker/dockerfile:1.4
ARG BASE_IMAGE=gcr.io/distroless/base-debian10

FROM docker.io/mambaorg/micromamba:bookworm-slim as mamba
ARG CONDA_ENVIRONMENT=environment.yml

USER root

COPY $CONDA_ENVIRONMENT /tmp/

# Setup mamba environment
RUN --mount=type=cache,target=/opt/conda/pkgs \
    --mount=type=cache,target=/root/.cache/pip \
    --mount=type=ssh \
    micromamba create --yes --always-copy --no-pyc --prefix /opt/env --file /tmp/environment.yml

RUN find /opt/env/ -follow -type f -name '*.a' -delete && \
    find /opt/env/ -follow -type f -name '*.js.map' -delete

FROM $BASE_IMAGE

COPY --link --from=mamba /opt/env /opt/env

ENV PATH=$PATH:/opt/env/bin

WORKDIR /workspace
COPY --link . /workspace

ENTRYPOINT ["/opt/env/bin/python"]