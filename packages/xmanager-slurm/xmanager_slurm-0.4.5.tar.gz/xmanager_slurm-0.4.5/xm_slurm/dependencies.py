import abc
import dataclasses
import datetime as dt
from typing import Callable, Sequence


class SlurmDependencyException(Exception): ...


NoChainingException = SlurmDependencyException(
    "Slurm only supports chaining dependencies with the same logical operator. "
    "For example, `dep1 & dep2 | dep3` is not supported but `dep1 & dep2 & dep3` is."
)


class SlurmJobDependency(abc.ABC):
    @abc.abstractmethod
    def to_dependency_str(self) -> str: ...

    def to_directive(self) -> str:
        return f"--dependency={self.to_dependency_str()}"

    def __and__(self, other_dependency: "SlurmJobDependency") -> "SlurmJobDependencyAND":
        if isinstance(self, SlurmJobDependencyOR):
            raise NoChainingException
        return SlurmJobDependencyAND(self, other_dependency)

    def __or__(self, other_dependency: "SlurmJobDependency") -> "SlurmJobDependencyOR":
        if isinstance(other_dependency, SlurmJobDependencyAND):
            raise NoChainingException
        return SlurmJobDependencyOR(self, other_dependency)

    def flatten(self) -> tuple["SlurmJobDependency", ...]:
        if isinstance(self, SlurmJobDependencyAND) or isinstance(self, SlurmJobDependencyOR):
            return self.first_dependency.flatten() + self.second_dependency.flatten()
        return (self,)

    def traverse(
        self, mapper: Callable[["SlurmJobDependency"], "SlurmJobDependency"]
    ) -> "SlurmJobDependency":
        if isinstance(self, SlurmJobDependencyAND) or isinstance(self, SlurmJobDependencyOR):
            return type(self)(
                first_dependency=self.first_dependency.traverse(mapper),
                second_dependency=self.second_dependency.traverse(mapper),
            )
        return mapper(self)


@dataclasses.dataclass(frozen=True)
class SlurmJobDependencyAND(SlurmJobDependency):
    first_dependency: SlurmJobDependency
    second_dependency: SlurmJobDependency

    def to_dependency_str(self) -> str:
        return f"{self.first_dependency.to_dependency_str()},{self.second_dependency.to_dependency_str()}"

    def __or__(self, other_dependency: SlurmJobDependency):
        del other_dependency
        raise NoChainingException

    def __hash__(self) -> int:
        return hash((type(self), self.first_dependency, self.second_dependency))


@dataclasses.dataclass(frozen=True)
class SlurmJobDependencyOR(SlurmJobDependency):
    first_dependency: SlurmJobDependency
    second_dependency: SlurmJobDependency

    def to_dependency_str(self) -> str:
        return f"{self.first_dependency.to_dependency_str()}?{self.second_dependency.to_dependency_str()}"

    def __and__(self, other_dependency: SlurmJobDependency):
        del other_dependency
        raise NoChainingException

    def __hash__(self) -> int:
        return hash((type(self), self.first_dependency, self.second_dependency))


@dataclasses.dataclass(frozen=True)
class SlurmJobDependencyAfter(SlurmJobDependency):
    handles: Sequence["xm_slurm.execution.SlurmHandle"]  # type: ignore # noqa: F821
    time: dt.timedelta | None = None

    def __post_init__(self):
        if len(self.handles) == 0:
            raise SlurmDependencyException("Dependency doesn't have any handles.")
        if self.time is not None and self.time.total_seconds() % 60 != 0:
            raise SlurmDependencyException("Time must be specified in exact minutes")

    def to_dependency_str(self) -> str:
        directive = "after"

        for handle in self.handles:
            directive += f":{handle.slurm_job.job_id}"
            if self.time is not None:
                directive += f"+{self.time.total_seconds() // 60:.0f}"
        return directive

    def __hash__(self) -> int:
        return hash((type(self),) + tuple([handle.slurm_job for handle in self.handles]))


@dataclasses.dataclass(frozen=True)
class SlurmJobDependencyAfterAny(SlurmJobDependency):
    handles: Sequence["xm_slurm.execution.SlurmHandle"]  # type: ignore # noqa: F821

    def __post_init__(self):
        if len(self.handles) == 0:
            raise SlurmDependencyException("Dependency doesn't have any handles.")

    def to_dependency_str(self) -> str:
        return ":".join(["afterany"] + [handle.slurm_job.job_id for handle in self.handles])

    def __hash__(self) -> int:
        return hash((type(self),) + tuple([handle.slurm_job for handle in self.handles]))


@dataclasses.dataclass(frozen=True)
class SlurmJobDependencyAfterNotOK(SlurmJobDependency):
    handles: Sequence["xm_slurm.execution.SlurmHandle"]  # type: ignore # noqa: F821

    def __post_init__(self):
        if len(self.handles) == 0:
            raise SlurmDependencyException("Dependency doesn't have any handles.")

    def to_dependency_str(self) -> str:
        return ":".join(["afternotok"] + [handle.slurm_job.job_id for handle in self.handles])

    def __hash__(self) -> int:
        return hash((type(self),) + tuple([handle.slurm_job for handle in self.handles]))


@dataclasses.dataclass(frozen=True)
class SlurmJobDependencyAfterOK(SlurmJobDependency):
    handles: Sequence["xm_slurm.execution.SlurmHandle"]  # type: ignore # noqa: F821

    def __post_init__(self):
        if len(self.handles) == 0:
            raise SlurmDependencyException("Dependency doesn't have any handles.")

    def to_dependency_str(self) -> str:
        return ":".join(["afterok"] + [handle.slurm_job.job_id for handle in self.handles])

    def __hash__(self) -> int:
        return hash((type(self),) + tuple([handle.slurm_job for handle in self.handles]))


@dataclasses.dataclass(frozen=True)
class SlurmJobArrayDependencyAfterOK(SlurmJobDependency):
    handles: Sequence["xm_slurm.execution.SlurmHandle[SlurmJob]"]  # type: ignore # noqa: F821

    def __post_init__(self):
        if len(self.handles) == 0:
            raise SlurmDependencyException("Dependency doesn't have any handles.")

    def to_dependency_str(self) -> str:
        job_ids = []
        for handle in self.handles:
            job = handle.slurm_job
            if job.is_array_job:
                job_ids.append(job.array_job_id)
            elif job.is_heterogeneous_job:
                job_ids.append(job.het_job_id)
            else:
                job_ids.append(job.job_id)
        return ":".join(["aftercorr"] + job_ids)

    def __hash__(self) -> int:
        return hash((type(self),) + tuple([handle.slurm_job for handle in self.handles]))
