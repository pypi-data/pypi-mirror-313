import dataclasses
import datetime as dt
import signal

from xmanager import xm

from xm_slurm import resources


@dataclasses.dataclass(frozen=True, kw_only=True)
class SlurmSpec(xm.ExecutorSpec):
    """Slurm executor specification that describes the location of the container runtime.

    Args:
        tag: The Image URI to push and pull the container image from.
            For example, using the GitHub Container Registry: `ghcr.io/my-project/my-image:latest`.
    """

    tag: str | None = None


@dataclasses.dataclass(frozen=True, kw_only=True)
class Slurm(xm.Executor):
    """Slurm Executor describing the runtime environment.

    Args:
        requirements: The requirements for the job.
        time: The maximum time to run the job.
        account: The account to charge the job to.
        partition: The partition to run the job in.
        qos: The quality of service to run the job with.
        priority: The priority of the job.
        timeout_signal: The signal to send to the job when it runs out of time.
        timeout_signal_grace_period: The time to wait before sending `timeout_signal`.
        requeue: Whether or not the job is eligible for requeueing.
        requeue_on_exit_code: The exit code that triggers requeueing.
        requeue_max_attempts: The maximum number of times to attempt requeueing.

    """

    # Job requirements
    requirements: resources.JobRequirements
    time: dt.timedelta

    # Placement
    account: str | None = None
    partition: str | None = None
    qos: str | None = None
    priority: int | None = None

    # Job dependency handling
    kill_on_invalid_dependencies: bool = True

    # Job rescheduling
    timeout_signal: signal.Signals = signal.SIGUSR2
    timeout_signal_grace_period: dt.timedelta = dt.timedelta(seconds=90)

    requeue: bool = True  # Is this job ellible for requeueing?
    requeue_on_exit_code: int = 42  # The exit code that triggers requeueing
    requeue_max_attempts: int = 5  # How many times to attempt requeueing

    def __post_init__(self) -> None:
        if not isinstance(self.time, dt.timedelta):
            raise TypeError(f"time must be a `datetime.timedelta`, got {type(self.time)}")
        if not isinstance(self.requirements, resources.JobRequirements):
            raise TypeError(
                f"requirements must be a `xm_slurm.JobRequirements`, got {type(self.requirements)}. "
                "If you're still using `xm.JobRequirements`, please update to `xm_slurm.JobRequirements`."
            )
        if not isinstance(self.timeout_signal, signal.Signals):
            raise TypeError(
                f"termination_signal must be a `signal.Signals`, got {type(self.timeout_signal)}"
            )
        if not isinstance(self.timeout_signal_grace_period, dt.timedelta):
            raise TypeError(
                f"termination_signal_delay_time must be a `datetime.timedelta`, got {type(self.timeout_signal_grace_period)}"
            )
        if self.requeue_max_attempts < 0:
            raise ValueError(
                f"requeue_max_attempts must be greater than or equal to 0, got {self.requeue_max_attempts}"
            )
        if self.requeue_on_exit_code == 0:
            raise ValueError("requeue_on_exit_code should not be 0 to avoid unexpected behavior.")

    @classmethod
    def Spec(cls, tag: str | None = None) -> SlurmSpec:
        return SlurmSpec(tag=tag)

    def to_directives(self) -> list[str]:
        # Job requirements
        directives = self.requirements.to_directives()

        # Time
        days = self.time.days
        hours, remainder = divmod(self.time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        directives.append(f"--time={days}-{hours:02}:{minutes:02}:{seconds:02}")

        # Job dependency handling
        directives.append(
            f"--kill-on-invalid-dep={'yes' if self.kill_on_invalid_dependencies else 'no'}"
        )

        # Placement
        if self.account:
            directives.append(f"--account={self.account}")
        if self.partition:
            directives.append(f"--partition={self.partition}")
        if self.qos:
            directives.append(f"--qos={self.qos}")
        if self.priority:
            directives.append(f"--priority={self.priority}")

        # Job rescheduling
        directives.append(
            f"--signal={self.timeout_signal.name.removeprefix('SIG')}@{self.timeout_signal_grace_period.seconds}"
        )
        if self.requeue and self.requeue_max_attempts > 0:
            directives.append("--requeue")
        else:
            directives.append("--no-requeue")

        return directives
