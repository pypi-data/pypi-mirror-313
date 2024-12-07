import datetime as dt
import logging
import os

from xmanager import xm

from xm_slurm import config, resources
from xm_slurm.contrib.clusters import drac
from xm_slurm.executors import Slurm

# ComputeCanada alias
cc = drac

__all__ = ["drac", "mila", "cc"]

logger = logging.getLogger(__name__)


def mila(
    *,
    user: str | None = None,
    partition: str | None = None,
    mounts: dict[os.PathLike[str] | str, os.PathLike[str] | str] | None = None,
) -> config.SlurmClusterConfig:
    """Mila Cluster (https://docs.mila.quebec/)."""
    if mounts is None:
        mounts = {
            "/network/scratch/${USER:0:1}/$USER": "/scratch",
            # TODO: move these somewhere common to all cluster configs.
            "/home/mila/${USER:0:1}/$USER/.local/state/xm-slurm": "/xm-slurm-state",
            "/home/mila/${USER:0:1}/$USER/.ssh": "/home/mila/${USER:0:1}/$USER/.ssh",
        }

    return config.SlurmClusterConfig(
        name="mila",
        ssh=config.SlurmSSHConfig(
            user=user,
            host="login.server.mila.quebec",
            host_public_key=config.PublicKey(
                "ssh-ed25519",
                "AAAAC3NzaC1lZDI1NTE5AAAAIBTPCzWRkwYDr/cFb4d2uR6rFlUtqfH3MoLMXPpJHK0n",
            ),
            port=2222,
        ),
        runtime=config.ContainerRuntime.SINGULARITY,
        partition=partition,
        prolog="module load singularity",
        environment={
            "SINGULARITY_CACHEDIR": "$SCRATCH/.apptainer",
            "SINGULARITY_TMPDIR": "$SLURM_TMPDIR",
            "SINGULARITY_LOCALCACHEDIR": "$SLURM_TMPDIR",
            "SCRATCH": "/scratch",
            # TODO: move this somewhere common to all cluster configs.
            "XM_SLURM_STATE_DIR": "/xm-slurm-state",
        },
        mounts=mounts,
        resources={
            resources.ResourceType.RTX8000: "rtx8000",
            resources.ResourceType.V100: "v100",
            resources.ResourceType.A100: "a100",
            resources.ResourceType.A100_80GIB: "a100l",
            resources.ResourceType.A6000: "a6000",
            resources.ResourceType.L40S: "l40s",
            resources.ResourceType.H100: "h100",
        },
        features={
            resources.FeatureType.NVIDIA_MIG: "mig",
            resources.FeatureType.NVIDIA_NVLINK: "nvlink",
        },
    )
