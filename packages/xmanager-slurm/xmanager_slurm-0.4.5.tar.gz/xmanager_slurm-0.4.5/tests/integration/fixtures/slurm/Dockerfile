# syntax=docker/dockerfile:1.4
FROM ubuntu:mantic AS slurm-base

# Install common dependencies and Slurm
RUN --mount=type=cache,target=/var/cache/apt,rw \
    apt-get update && \
    apt-get install -y slurm-wlm munge gosu && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /run/munge && chown munge:munge /run/munge \
    && mkdir -p /var/run/munge && chown munge:munge /var/run/munge \
    && mkdir -p /var/{spool,run}/{slurmd,slurmctl,slurmdbd}/ \
    && mkdir -p /var/lib/slurmd \
    && mkdir -p /var/log/{slurm,slurmctl,slurmdbd}/ \
    && chown -R slurm:slurm /var/*/slurm*

COPY --link --chown=slurm:slurm slurm.conf cgroup.conf /etc/slurm/

COPY --link docker-entrypoint.sh /docker-entrypoint.sh
ENTRYPOINT [ "/docker-entrypoint.sh" ]

FROM slurm-base AS slurm-db

RUN --mount=type=cache,target=/var/cache/apt,rw \
    apt-get update && \
    apt-get install -y slurmdbd && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY --link --chown=slurm:slurm --chmod=0600 slurmdbd.conf /etc/slurm/slurmdbd.conf

FROM slurm-base AS slurm-login

RUN --mount=type=cache,target=/var/cache/apt,rw \
    apt-get update && \
    apt-get install -y vim man-db openssh-server openssh-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY --link --chown=0600 id_ed25519.pub /root/.ssh/
RUN cat /root/.ssh/id_ed25519.pub >> /root/.ssh/authorized_keys

COPY --link --chown=0600 host_ed25519 /etc/ssh/ssh_host_ed25519_key 
COPY --link --chown=0644 host_ed25519.pub /etc/ssh/ssh_host_ed25519_key.pub

COPY --link --chown=0600 sshd_config /etc/ssh/sshd_config