import enum
import itertools
import math
from typing import Mapping

import immutabledict

from xm_slurm import config


class ResourceType(enum.IntEnum):
    CPU = 1

    MEMORY = 2
    RAM = 2

    EPHEMERAL_STORAGE = 3
    DISK = 3

    GPU = 1000
    RTX8000 = 1001
    P4 = 1010

    P100 = 1011
    P100_16GIB = 1012

    V100 = 1020
    V100_32GIB = 1021

    A100 = 1030
    A100_80GIB = 1031
    A5000 = 1032
    A6000 = 1033

    H100 = 1040
    L40S = 1041


AcceleratorType = set([
    ResourceType.RTX8000,
    ResourceType.P4,
    ResourceType.P100,
    ResourceType.P100_16GIB,
    ResourceType.V100,
    ResourceType.V100_32GIB,
    ResourceType.A100,
    ResourceType.A100_80GIB,
    ResourceType.A5000,
    ResourceType.A6000,
    ResourceType.H100,
    ResourceType.L40S,
])

assert AcceleratorType | {
    ResourceType.CPU,
    ResourceType.MEMORY,
    ResourceType.DISK,
    ResourceType.GPU,
} == set(ResourceType.__members__.values()), "Resource types are not exhaustive."


ResourceQuantity = int | float


class FeatureType(enum.IntEnum):
    NVIDIA_MIG = 1
    NVIDIA_NVLINK = 2


class JobRequirements:
    replicas: int
    location: str | None
    accelerator: ResourceType | None
    cluster: config.SlurmClusterConfig | None = None

    def __init__(
        self,
        *,
        resources: Mapping[ResourceType | str, ResourceQuantity] = immutabledict.immutabledict(),
        replicas: int = 1,
        location: str | None = None,
        cluster: config.SlurmClusterConfig | None = None,
        **kw_resources: ResourceQuantity,
    ):
        self.replicas = replicas or 1
        self.location = location
        self.accelerator = None
        self.cluster = cluster

        self.task_requirements: dict[ResourceType | str, ResourceQuantity] = {}
        for resource_name, value in itertools.chain(resources.items(), kw_resources.items()):
            match resource_name:
                case str() if resource_name.upper() in ResourceType.__members__:
                    resource = ResourceType[resource_name.upper()]
                case ResourceType():
                    resource = resource_name
                case str():
                    resource = resource_name

            if (
                resource in AcceleratorType
                or resource == ResourceType.GPU
                or (isinstance(resource, str) and resource.startswith("gpu"))
            ):
                if self.accelerator is not None:
                    raise ValueError("Accelerator already set.")
                self.accelerator = resource  # type: ignore

            if resource in self.task_requirements:
                raise ValueError(f"{resource} has been specified twice.")
            self.task_requirements[resource] = value

    def to_directives(self) -> list[str]:
        if self.cluster is None:
            raise ValueError("Cannnot derive Slurm directives for requirements without a cluster.")
        directives = []

        for resource, value in self.task_requirements.items():
            match resource:
                case ResourceType.EPHEMERAL_STORAGE | ResourceType.DISK:
                    assert isinstance(value, int), "Disk space must be an integer"
                    directives.append(f"--tmp={math.ceil(value / 2**20)}M")
                case ResourceType.MEMORY | ResourceType.RAM:
                    num_cpus = self.task_requirements.get(ResourceType.CPU, 1)
                    assert isinstance(value, (int, float)), "Memory must be an integer or float"
                    assert isinstance(num_cpus, int), "CPU must be an integer"
                    directives.append(f"--mem-per-cpu={math.ceil(value / num_cpus / 2**20)}M")
                case ResourceType.CPU:
                    assert isinstance(value, int), "CPU must be an integer"
                    directives.append(f"--cpus-per-task={value}")
                case ResourceType.GPU:
                    assert isinstance(value, int), "GPU must be an integer"
                    directives.append(f"--gpus-per-task={value}")
                case ResourceType() if resource in AcceleratorType:
                    assert isinstance(value, int), "Accelerator must be an integer"
                    resource_type = self.cluster.resources.get(resource, None)
                    if resource_type is None:
                        raise ValueError(
                            f"Cluster {self.cluster.name} does not map resource type {resource!r}."
                        )
                    directives.append(f"--gpus-per-task={resource_type}:{value}")
                case str():
                    directives.append(f"--gres={resource}:{value}")

        directives.append(f"--ntasks={self.replicas}")
        if self.location:
            directives.append(f"--nodelist={self.location}")

        return directives

    def replace(
        self,
        cluster: config.SlurmClusterConfig | None,
        **kw_resources: ResourceQuantity,
    ) -> "JobRequirements":
        return JobRequirements(
            resources=self.task_requirements | kw_resources,  # type: ignore
            replicas=self.replicas,
            cluster=cluster or self.cluster,
        )

    def __repr__(self) -> str:
        args = []

        for resource, value in self.task_requirements.items():
            if isinstance(resource, ResourceType):
                resource = resource.name
            args.append(f"{resource.lower()}={value!r}")

        if self.replicas != 1:
            args.append(f"replicas={self.replicas}")

        if self.cluster is not None:
            args.append(f"cluster={self.cluster!r}")

        return f'xm_slurm.JobRequirements({", ".join(args)})'
