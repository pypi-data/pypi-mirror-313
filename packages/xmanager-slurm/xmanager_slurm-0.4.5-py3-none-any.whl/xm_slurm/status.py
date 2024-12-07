"""Implementation of Slurm work unit statuses."""

import enum
import re
from typing import Sequence

from xmanager import xm


class SlurmJobState(enum.Enum):
    BOOT_FAIL = enum.auto()
    CANCELLED = enum.auto()
    COMPLETED = enum.auto()
    DEADLINE = enum.auto()
    FAILED = enum.auto()
    NODE_FAIL = enum.auto()
    OUT_OF_MEMORY = enum.auto()
    PENDING = enum.auto()
    PREEMPTED = enum.auto()
    RUNNING = enum.auto()
    REQUEUED = enum.auto()
    RESIZING = enum.auto()
    REVOKED = enum.auto()
    SUSPENDED = enum.auto()
    TIMEOUT = enum.auto()

    @property
    def message(self) -> str:
        match self:
            case SlurmJobState.BOOT_FAIL:
                return (
                    "Job terminated due to launch failure, "
                    "typically due to a hardware failure (e.g. unable to boot "
                    "the node or block and the job can not be requeued)."
                )
            case SlurmJobState.CANCELLED:
                return (
                    "Job was explicitly cancelled by the user or "
                    "system administrator. The job may or may not have been "
                    "initiated."
                )
            case SlurmJobState.COMPLETED:
                return "Job has terminated all processes on all " "nodes with an exit code of zero."
            case SlurmJobState.DEADLINE:
                return "Job terminated on deadline."
            case SlurmJobState.FAILED:
                return "Job terminated with non-zero exit code or " "other failure condition."
            case SlurmJobState.NODE_FAIL:
                return "Job terminated due to failure of one or " "more allocated nodes."
            case SlurmJobState.OUT_OF_MEMORY:
                return "Job experienced out of memory error."
            case SlurmJobState.PENDING:
                return "Job is awaiting resource allocation."
            case SlurmJobState.PREEMPTED:
                return "Job terminated due to preemption."
            case SlurmJobState.RUNNING:
                return "Job currently has an allocation."
            case SlurmJobState.REQUEUED:
                return "Job was requeued."
            case SlurmJobState.RESIZING:
                return "Job is about to change size."
            case SlurmJobState.REVOKED:
                return "Sibling was removed from cluster due to " "other cluster starting the job."
            case SlurmJobState.SUSPENDED:
                return "Job has an allocation, but execution has been suspended."
            case SlurmJobState.TIMEOUT:
                return "Job terminated upon reaching its time limit."
            case _:
                raise ValueError(f"Invalid Slurm job state: {self}")

    def __str__(self) -> str:
        return f"{self.name}: {self.message}"

    @classmethod
    def from_str(cls, state: str) -> "SlurmJobState":
        return cls[state]

    @classmethod
    def from_slurm_str(cls, state: str) -> "SlurmJobState":
        _SLURM_JOB_STATE_REGEX = re.compile(f"({'|'.join(entry.name for entry in cls)})\\s?.*")
        match = _SLURM_JOB_STATE_REGEX.match(state)
        assert match and len(match.groups()) == 1, f"Failed to parse job state, {state!r}"
        return cls.from_str(match.group(1))


SlurmPendingJobStates = set([
    SlurmJobState.PENDING,
    SlurmJobState.REQUEUED,
    SlurmJobState.RESIZING,
])
SlurmRunningJobStates = set([
    SlurmJobState.RUNNING,
    SlurmJobState.SUSPENDED,
])
SlurmActiveJobStates = SlurmPendingJobStates | SlurmRunningJobStates
SlurmCompletedJobStates = set([SlurmJobState.COMPLETED])
SlurmFailedJobStates = set([
    SlurmJobState.BOOT_FAIL,
    SlurmJobState.DEADLINE,
    SlurmJobState.FAILED,
    SlurmJobState.NODE_FAIL,
    SlurmJobState.OUT_OF_MEMORY,
    SlurmJobState.PREEMPTED,
    SlurmJobState.REVOKED,
    SlurmJobState.TIMEOUT,
])
SlurmCancelledJobStates = set([SlurmJobState.CANCELLED])

assert (
    SlurmPendingJobStates
    | SlurmRunningJobStates
    | SlurmActiveJobStates
    | SlurmCompletedJobStates
    | SlurmFailedJobStates
    | SlurmCancelledJobStates
) == set(SlurmJobState.__members__.values()), "Slurm job states are not exhaustive."


class SlurmWorkUnitStatusEnum(enum.IntEnum):
    """Status of a local experiment job."""

    # Work unit was created, but has not started yet.
    PENDING = 0
    # Work unit was created, but has not terminated yet.
    RUNNING = 1
    # Work unit terminated and was successful.
    COMPLETED = 2
    # Work unit terminated and was not succesful.
    FAILED = 3
    # Work unit terminated because it was cancelled by the user.
    CANCELLED = 4

    @classmethod
    def from_job_state(cls, state: SlurmJobState) -> "SlurmWorkUnitStatusEnum":
        """Convert a Slurm job state to a SlurmWorkUnitStatusEnum."""
        if state in SlurmPendingJobStates:
            return cls.PENDING
        elif state in SlurmRunningJobStates:
            return cls.RUNNING
        elif state in SlurmCompletedJobStates:
            return cls.COMPLETED
        elif state in SlurmFailedJobStates:
            return cls.FAILED
        elif state in SlurmCancelledJobStates:
            return cls.CANCELLED
        else:
            raise ValueError(f"Invalid Slurm job state: {state}")


class SlurmWorkUnitStatus(xm.ExperimentUnitStatus):
    """Status of a Slurm experiment job."""

    @classmethod
    def aggregate(cls, states: Sequence[SlurmJobState]) -> "SlurmWorkUnitStatus":
        """Aggregate a sequence of statuses into a single status."""
        assert len(states) > 0, "Cannot aggregate empty sequence of statuses."
        max_error_state: SlurmJobState | None = None
        for state in states:
            if not max_error_state:
                max_error_state = state
            elif SlurmWorkUnitStatusEnum.from_job_state(
                state
            ) > SlurmWorkUnitStatusEnum.from_job_state(max_error_state):
                max_error_state = state
        assert max_error_state is not None
        return cls(max_error_state)

    def __init__(self, state: SlurmJobState) -> None:
        super().__init__()
        self._state = state
        self._status = SlurmWorkUnitStatusEnum.from_job_state(state)

    @property
    def is_active(self) -> bool:
        return (
            self._status == SlurmWorkUnitStatusEnum.RUNNING
            or self._status == SlurmWorkUnitStatusEnum.PENDING
        )

    @property
    def is_completed(self) -> bool:
        return self._status == SlurmWorkUnitStatusEnum.COMPLETED

    @property
    def is_failed(self) -> bool:
        return self._status == SlurmWorkUnitStatusEnum.FAILED

    @property
    def status(self) -> SlurmWorkUnitStatusEnum:
        return self._status

    @property
    def message(self) -> str:
        return str(self._state)

    def __repr__(self) -> str:
        return f"<SlurmWorkUnitStatus {self._state!r}>"
