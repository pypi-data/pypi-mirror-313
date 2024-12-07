import os
from typing import Literal

from xm_slurm import config
from xm_slurm.resources import FeatureType, ResourceType

__all__ = ["narval", "beluga", "cedar", "graham"]


def _drac_cluster(
    *,
    name: str,
    host: str,
    host_public_key: config.PublicKey,
    port: int = 22,
    user: str | None = None,
    account: str | None = None,
    modules: list[str] | None = None,
    proxy: Literal["submission-host"] | str | None = None,
    mounts: dict[os.PathLike[str] | str, os.PathLike[str] | str] | None = None,
    resources: dict[ResourceType, str] | None = None,
    features: dict[FeatureType, str] | None = None,
) -> config.SlurmClusterConfig:
    """DRAC Cluster."""
    if mounts is None:
        mounts = {
            "/scratch/$USER": "/scratch",
            # TODO: move these somewhere common to all cluster configs.
            "/home/$USER/.ssh": "/home/$USER/.ssh",
            "/home/$USER/.local/state/xm-slurm": "/xm-slurm-state",
        }

    return config.SlurmClusterConfig(
        name=name,
        ssh=config.SlurmSSHConfig(
            user=user,
            host=host,
            host_public_key=host_public_key,
            port=port,
        ),
        account=account,
        proxy=proxy,
        runtime=config.ContainerRuntime.APPTAINER,
        prolog=f"module load apptainer {' '.join(modules) if modules else ''}".rstrip(),
        environment={
            "APPTAINER_CACHEDIR": "$SCRATCH/.apptainer",
            "APPTAINER_TMPDIR": "$SLURM_TMPDIR",
            "APPTAINER_LOCALCACHEDIR": "$SLURM_TMPDIR",
            "_XDG_DATA_HOME": "$SLURM_TMPDIR/.local",
            "SCRATCH": "/scratch",
            # TODO: move this somewhere common to all cluster configs.
            "XM_SLURM_STATE_DIR": "/xm-slurm-state",
        },
        mounts=mounts,
        resources=resources or {},
        features=features or {},
    )


def narval(
    *,
    user: str | None = None,
    account: str | None = None,
    proxy: Literal["submission-host"] | str | None = None,
    mounts: dict[os.PathLike[str] | str, os.PathLike[str] | str] | None = None,
) -> config.SlurmClusterConfig:
    """DRAC Narval Cluster (https://docs.alliancecan.ca/wiki/Narval/en)."""
    modules = []
    if proxy != "submission-host":
        modules.append("httpproxy")

    return _drac_cluster(
        name="narval",
        host="robot.narval.alliancecan.ca",
        host_public_key=config.PublicKey(
            "ssh-ed25519",
            "AAAAC3NzaC1lZDI1NTE5AAAAILFxB0spH5RApc43sBx0zOxo1ARVH0ezU+FbQH95FW+h",
        ),
        user=user,
        account=account,
        mounts=mounts,
        proxy=proxy,
        modules=modules,
        resources={ResourceType.A100: "a100"},
        features={
            FeatureType.NVIDIA_MIG: "a100mig",
            FeatureType.NVIDIA_NVLINK: "nvlink",
        },
    )


def beluga(
    *,
    user: str | None = None,
    account: str | None = None,
    proxy: Literal["submission-host"] | str | None = None,
    mounts: dict[os.PathLike[str] | str, os.PathLike[str] | str] | None = None,
) -> config.SlurmClusterConfig:
    """DRAC Beluga Cluster (https://docs.alliancecan.ca/wiki/B%C3%A9luga/en)."""
    modules = []
    if proxy != "submission-host":
        modules.append("httpproxy")

    return _drac_cluster(
        name="beluga",
        host="robot.beluga.alliancecan.ca",
        host_public_key=config.PublicKey(
            "ssh-ed25519",
            "AAAAC3NzaC1lZDI1NTE5AAAAIOAzTHRerKjcFhDqqgRss7Sj4xePWVn1f1QvBfUmX6Pe",
        ),
        user=user,
        account=account,
        mounts=mounts,
        proxy=proxy,
        modules=modules,
        resources={ResourceType.V100: "tesla_v100-sxm2-16gb"},
        features={
            FeatureType.NVIDIA_NVLINK: "nvlink",
        },
    )


def cedar(
    *,
    user: str | None = None,
    account: str | None = None,
    mounts: dict[os.PathLike[str] | str, os.PathLike[str] | str] | None = None,
) -> config.SlurmClusterConfig:
    """DRAC Cedar Cluster (https://docs.alliancecan.ca/wiki/Cedar/en)."""
    return _drac_cluster(
        name="cedar",
        host="robot.cedar.alliancecan.ca",
        host_public_key=config.PublicKey(
            "ssh-ed25519",
            "AAAAC3NzaC1lZDI1NTE5AAAAIEsmR+vxeKYEDFIFj+nxlgp3ACs64VwVD5qBifQ2I5VS",
        ),
        user=user,
        account=account,
        mounts=mounts,
        resources={
            ResourceType.V100_32GIB: "v100l",
            ResourceType.P100: "p100",
            ResourceType.P100_16GIB: "p100l",
        },
    )


def graham(
    *,
    user: str | None = None,
    account: str | None = None,
    proxy: Literal["submission-host"] | str | None = "submission-host",
    mounts: dict[os.PathLike[str] | str, os.PathLike[str] | str] | None = None,
) -> config.SlurmClusterConfig:
    """DRAC Cedar Cluster (https://docs.alliancecan.ca/wiki/Graham/en)."""
    return _drac_cluster(
        name="graham",
        host="robot.graham.alliancecan.ca",
        host_public_key=config.PublicKey(
            "ssh-ed25519",
            "AAAAC3NzaC1lZDI1NTE5AAAAIDPcZ+yKur5GvPoisN2KjtEbrem/0j+JviMfAk7GVlL9",
        ),
        user=user,
        account=account,
        mounts=mounts,
        proxy=proxy,
        resources={
            ResourceType.V100: "v100",
            ResourceType.P100: "p100",
            ResourceType.A100: "a100",
            ResourceType.A5000: "a5000",
        },
    )


def all(
    user: str | None = None,
    account: str | None = None,
    mounts: dict[os.PathLike[str] | str, os.PathLike[str] | str] | None = None,
) -> list[config.SlurmClusterConfig]:
    """All DRAC clusters."""
    return [
        narval(user=user, account=account, mounts=mounts),
        beluga(user=user, account=account, mounts=mounts),
        cedar(user=user, account=account, mounts=mounts),
        graham(user=user, account=account, mounts=mounts),
    ]
