import asyncio
import collections.abc
import dataclasses
import functools
import hashlib
import logging
import operator
import shlex
import typing as tp

import asyncssh
import backoff
import jinja2 as j2
import more_itertools as mit
from asyncssh.auth import KbdIntPrompts, KbdIntResponse
from asyncssh.misc import MaybeAwait
from rich.console import ConsoleRenderable
from rich.rule import Rule
from xmanager import xm

from xm_slurm import batching, config, constants, dependencies, executors, status
from xm_slurm.console import console
from xm_slurm.job_blocks import JobArgs
from xm_slurm.types import Descriptor

SlurmClusterConfig = config.SlurmClusterConfig
ContainerRuntime = config.ContainerRuntime

logger = logging.getLogger(__name__)

"""
=== Runtime Configurations ===
With RunC:
    skopeo copy --dest-creds=<username>:<secret> docker://<image>@<digest> oci:<image>:<digest>

    pushd $SLURM_TMPDIR

    umoci raw unpack --rootless --image <image>:<digest> bundle/<digest>
    umoci raw runtime-config --image <image>:<digest> bundle/<digest>/config.json

    runc run -b bundle/<digest> <container-id>

With Singularity / Apptainer:

    apptainer build --fix-perms --sandbox <digest> docker://<image>@<digest>
    apptainer run --compat <digest>
"""

_POLL_INTERVAL = 30.0
_BATCHED_BATCH_SIZE = 16
_BATCHED_TIMEOUT = 0.2


class SlurmExecutionError(Exception): ...


class NoKBAuthSSHClient(asyncssh.SSHClient):
    """SSHClient that does not prompt for keyboard-interactive authentication."""

    def kbdint_auth_requested(self) -> MaybeAwait[str | None]:
        return ""

    def kbdint_challenge_received(
        self, name: str, instructions: str, lang: str, prompts: KbdIntPrompts
    ) -> MaybeAwait[KbdIntResponse | None]:
        del name, instructions, lang, prompts
        return []


@dataclasses.dataclass(frozen=True, kw_only=True)
class SlurmJob:
    job_id: str

    @property
    def is_array_job(self) -> bool:
        return isinstance(self, SlurmArrayJob)

    @property
    def is_heterogeneous_job(self) -> bool:
        return isinstance(self, SlurmHeterogeneousJob)

    def __hash__(self) -> int:
        return hash((type(self), self.job_id))


@dataclasses.dataclass(frozen=True, kw_only=True)
class SlurmArrayJob(SlurmJob):
    array_job_id: str
    array_task_id: str


@dataclasses.dataclass(frozen=True, kw_only=True)
class SlurmHeterogeneousJob(SlurmJob):
    het_job_id: str
    het_component_id: str


SlurmJobT = tp.TypeVar("SlurmJobT", bound=SlurmJob, covariant=True)


class SlurmJobDescriptor(Descriptor[SlurmJobT, str]):
    def __set_name__(self, owner: type, name: str):
        del owner
        self.job = f"_{name}"

    def __get__(self, instance: object | None, owner: tp.Type[object] | None = None) -> SlurmJobT:
        del owner
        return getattr(instance, self.job)

    def __set__(self, instance: object, value: str):
        _setattr = object.__setattr__ if not hasattr(instance, self.job) else setattr

        match = constants.SLURM_JOB_ID_REGEX.match(value)
        if match is None:
            raise ValueError(f"Invalid Slurm job ID: {value}")
        groups = match.groupdict()

        job_id = groups["jobid"]
        if array_task_id := groups.get("arraytaskid", None):
            _setattr(
                instance,
                self.job,
                SlurmArrayJob(job_id=value, array_job_id=job_id, array_task_id=array_task_id),
            )
        elif het_component_id := groups.get("componentid", None):
            _setattr(
                instance,
                self.job,
                SlurmHeterogeneousJob(
                    job_id=value, het_job_id=job_id, het_component_id=het_component_id
                ),
            )
        else:
            _setattr(instance, self.job, SlurmJob(job_id=value))


def _group_by_ssh_configs(
    ssh_configs: tp.Sequence[config.SlurmSSHConfig], slurm_jobs: tp.Sequence[SlurmJob]
) -> dict[config.SlurmSSHConfig, list[SlurmJob]]:
    jobs_by_cluster = collections.defaultdict(list)
    for ssh_config, slurm_job in zip(ssh_configs, slurm_jobs):
        jobs_by_cluster[ssh_config].append(slurm_job)
    return jobs_by_cluster


class _BatchedSlurmHandle:
    @functools.partial(
        batching.batch,
        max_batch_size=_BATCHED_BATCH_SIZE,
        batch_timeout=_BATCHED_TIMEOUT,
    )
    @staticmethod
    @backoff.on_exception(backoff.expo, SlurmExecutionError, max_tries=5, max_time=60.0)
    async def _batched_get_state(
        ssh_configs: tp.Sequence[config.SlurmSSHConfig],
        slurm_jobs: tp.Sequence[SlurmJob],
    ) -> tp.Sequence[status.SlurmJobState]:
        async def _get_state(
            options: config.SlurmSSHConfig, slurm_jobs: tp.Sequence[SlurmJob]
        ) -> tp.Sequence[status.SlurmJobState]:
            result = await get_client().run(
                options,
                [
                    "sacct",
                    "--jobs",
                    ",".join([slurm_job.job_id for slurm_job in slurm_jobs]),
                    "--format",
                    "JobID,State",
                    "--allocations",
                    "--noheader",
                    "--parsable2",
                ],
                check=True,
            )

            assert isinstance(result.stdout, str)
            states_by_job_id = {}
            for line in result.stdout.splitlines():
                job_id, state = line.split("|")
                states_by_job_id[job_id] = status.SlurmJobState.from_slurm_str(state)

            job_states = []
            for slurm_job in slurm_jobs:
                if slurm_job.job_id in states_by_job_id:
                    job_states.append(states_by_job_id[slurm_job.job_id])
                # This is a stupid hack around sacct's inability to display state information for
                # array job elements that haven't begun. We'll assume that if the job ID is not found,
                # and it's an array job, then it's pending.
                elif slurm_job.is_array_job:
                    job_states.append(status.SlurmJobState.PENDING)
                else:
                    raise SlurmExecutionError(f"Failed to find job state info for {slurm_job!r}")
            return job_states

        # Group Slurm jobs by their cluster so we can batch requests
        jobs_by_cluster = _group_by_ssh_configs(ssh_configs, slurm_jobs)

        # Async get state for each cluster
        job_states_per_cluster = await asyncio.gather(*[
            _get_state(options, jobs) for options, jobs in jobs_by_cluster.items()
        ])

        # Reconstruct the job states by cluster
        job_states_by_cluster = {}
        for ssh_config, job_states in zip(ssh_configs, job_states_per_cluster):
            job_states_by_cluster[ssh_config] = dict(zip(jobs_by_cluster[ssh_config], job_states))

        # Reconstruct the job states in the original order
        job_states = []
        for ssh_config, slurm_job in zip(ssh_configs, slurm_jobs):
            job_states.append(job_states_by_cluster[ssh_config][slurm_job])
        return job_states

    @functools.partial(
        batching.batch,
        max_batch_size=_BATCHED_BATCH_SIZE,
        batch_timeout=_BATCHED_TIMEOUT,
    )
    @staticmethod
    async def _batched_cancel(
        ssh_configs: tp.Sequence[config.SlurmSSHConfig],
        slurm_jobs: tp.Sequence[SlurmJob],
    ) -> tp.Sequence[None]:
        async def _cancel(
            options: config.SlurmSSHConfig, slurm_jobs: tp.Sequence[SlurmJob]
        ) -> None:
            await get_client().run(
                options,
                ["scancel", " ".join([slurm_job.job_id for slurm_job in slurm_jobs])],
                check=True,
            )

        jobs_by_cluster = _group_by_ssh_configs(ssh_configs, slurm_jobs)
        return await asyncio.gather(*[
            _cancel(options, job_ids) for options, job_ids in jobs_by_cluster.items()
        ])


@dataclasses.dataclass(frozen=True, kw_only=True)
class SlurmHandle(_BatchedSlurmHandle, tp.Generic[SlurmJobT]):
    """A handle for referring to the launched container."""

    experiment_id: int
    ssh: config.SlurmSSHConfig
    slurm_job: Descriptor[SlurmJobT, str] = SlurmJobDescriptor[SlurmJobT]()
    job_name: str  # XManager job name associated with this handle

    @backoff.on_predicate(
        backoff.constant,
        lambda state: state in status.SlurmActiveJobStates,
        jitter=None,
        interval=_POLL_INTERVAL,
    )
    async def wait(self) -> status.SlurmJobState:
        return await self.get_state()

    async def stop(self) -> None:
        await self._batched_cancel(self.ssh, self.slurm_job)

    async def get_state(self) -> status.SlurmJobState:
        return await self._batched_get_state(self.ssh, self.slurm_job)

    async def logs(
        self, *, num_lines: int, block_size: int, wait: bool, follow: bool
    ) -> tp.AsyncGenerator[ConsoleRenderable, None]:
        file = f".local/state/xm-slurm/{self.experiment_id}/slurm-{self.slurm_job.job_id}.out"
        conn = await get_client().connection(self.ssh)
        async with conn.start_sftp_client() as sftp:
            if wait:
                while not (await sftp.exists(file)):
                    await asyncio.sleep(5)

            async with sftp.open(file, "rb") as remote_file:
                file_stat = await remote_file.stat()
                file_size = file_stat.size
                assert file_size is not None

                data = b""
                lines = []
                position = file_size

                while len(lines) <= num_lines and position > 0:
                    read_size = min(block_size, position)
                    position -= read_size
                    await remote_file.seek(position)
                    chunk = await remote_file.read(read_size)
                    data = chunk + data
                    lines = data.splitlines()

                if position <= 0:
                    yield Rule("[bold red]BEGINNING OF FILE[/bold red]")
                for line in lines[-num_lines:]:
                    yield line.decode("utf-8", errors="replace")

                if (await self.get_state()) not in status.SlurmActiveJobStates:
                    yield Rule("[bold red]END OF FILE[/bold red]")
                    return

                if not follow:
                    return

                await remote_file.seek(file_size)
                while True:
                    if new_data := (await remote_file.read(block_size)):
                        yield new_data.decode("utf-8", errors="replace")
                    else:
                        await asyncio.sleep(0.25)


@functools.cache
def get_template_env(container_runtime: ContainerRuntime) -> j2.Environment:
    template_loader = j2.PackageLoader("xm_slurm", "templates/slurm")
    template_env = j2.Environment(loader=template_loader, trim_blocks=True, lstrip_blocks=False)

    def _raise_template_exception(msg: str) -> None:
        raise j2.TemplateRuntimeError(msg)

    template_env.globals["raise"] = _raise_template_exception
    template_env.globals["operator"] = operator

    match container_runtime:
        case ContainerRuntime.SINGULARITY | ContainerRuntime.APPTAINER:
            runtime_template = template_env.get_template("runtimes/apptainer.bash.j2")
        case ContainerRuntime.PODMAN:
            runtime_template = template_env.get_template("runtimes/podman.bash.j2")
        case _:
            raise NotImplementedError(f"Container runtime {container_runtime} is not implemented.")
    # Update our global env with the runtime template's exported globals
    template_env.globals.update(runtime_template.module.__dict__)

    return template_env


@functools.cache
def get_client() -> "Client":
    return Client()


class Client:
    def __init__(self) -> None:
        self._connections = dict[config.SlurmSSHConfig, asyncssh.SSHClientConnection]()
        self._connection_lock = asyncio.Lock()

    @backoff.on_exception(backoff.expo, asyncssh.Error, max_tries=5, max_time=60.0)
    async def _setup_remote_connection(self, conn: asyncssh.SSHClientConnection) -> None:
        # Make sure the xm-slurm state directory exists
        async with conn.start_sftp_client() as sftp_client:
            await sftp_client.makedirs(".local/state/xm-slurm", exist_ok=True)

    async def connection(self, ssh_config: config.SlurmSSHConfig) -> asyncssh.SSHClientConnection:
        if ssh_config not in self._connections:
            async with self._connection_lock:
                try:
                    conn, _ = await asyncssh.create_connection(
                        NoKBAuthSSHClient, options=ssh_config.connection_options
                    )
                    await self._setup_remote_connection(conn)
                    self._connections[ssh_config] = conn
                except asyncssh.misc.PermissionDenied as ex:
                    raise SlurmExecutionError(
                        f"Permission denied connecting to {ssh_config.host}"
                    ) from ex
                except asyncssh.misc.ConnectionLost as ex:
                    raise SlurmExecutionError(f"Connection lost to host {ssh_config.host}") from ex
                except asyncssh.misc.HostKeyNotVerifiable as ex:
                    raise SlurmExecutionError(
                        f"Cannot verify the public key for host {ssh_config.host}"
                    ) from ex
                except asyncssh.misc.KeyExchangeFailed as ex:
                    raise SlurmExecutionError(
                        f"Failed to exchange keys with host {ssh_config.host}"
                    ) from ex
                except asyncssh.Error as ex:
                    raise SlurmExecutionError(
                        f"SSH connection error when connecting to {ssh_config.host}"
                    ) from ex

        return self._connections[ssh_config]

    @backoff.on_exception(backoff.expo, asyncssh.Error, max_tries=5, max_time=60.0)
    async def run(
        self,
        ssh_config: config.SlurmSSHConfig,
        command: xm.SequentialArgs | str | tp.Sequence[str],
        *,
        check: bool = False,
        timeout: float | None = None,
    ) -> asyncssh.SSHCompletedProcess:
        client = await self.connection(ssh_config)
        if isinstance(command, xm.SequentialArgs):
            command = command.to_list()
        if not isinstance(command, str) and isinstance(command, collections.abc.Sequence):
            command = shlex.join(command)
        assert isinstance(command, str)
        logger.debug("Running command on %s: %s", ssh_config.host, command)

        return await client.run(command, check=check, timeout=timeout)

    async def template(
        self,
        *,
        job: xm.Job | xm.JobGroup,
        dependency: dependencies.SlurmJobDependency | None = None,
        cluster: SlurmClusterConfig,
        args: tp.Mapping[str, tp.Any] | tp.Sequence[tp.Mapping[str, tp.Any]] | None,
        experiment_id: int,
        identity: str | None,
    ) -> str:
        if args is None:
            args = {}

        template_env = get_template_env(cluster.runtime)

        # Sanitize job groups
        if isinstance(job, xm.JobGroup) and len(job.jobs) == 1:
            job = tp.cast(xm.Job, list(job.jobs.values())[0])
        elif isinstance(job, xm.JobGroup) and len(job.jobs) == 0:
            raise ValueError("Job group must have at least one job")

        match job:
            case xm.Job() as job_array if isinstance(args, collections.abc.Sequence):
                template = template_env.get_template("job-array.bash.j2")
                sequential_args = [
                    xm.SequentialArgs.from_collection(trial.get("args", None)) for trial in args
                ]
                env_vars = [trial.get("env_vars") for trial in args]
                if any(env_vars):
                    raise NotImplementedError(
                        "Job arrays over environment variables are not yet supported."
                    )

                return template.render(
                    job=job_array,
                    dependency=dependency,
                    cluster=cluster,
                    args=sequential_args,
                    env_vars=env_vars,
                    experiment_id=experiment_id,
                    identity=identity,
                )
            case xm.Job() if isinstance(args, collections.abc.Mapping):
                template = template_env.get_template("job.bash.j2")
                sequential_args = xm.SequentialArgs.from_collection(args.get("args", None))
                env_vars = args.get("env_vars", None)
                return template.render(
                    job=job,
                    dependency=dependency,
                    cluster=cluster,
                    args=sequential_args,
                    env_vars=env_vars,
                    experiment_id=experiment_id,
                    identity=identity,
                )
            case xm.JobGroup() as job_group if isinstance(args, collections.abc.Mapping):
                template = template_env.get_template("job-group.bash.j2")
                sequential_args = {
                    job_name: {
                        "args": args.get(job_name, {}).get("args", None),
                    }
                    for job_name in job_group.jobs.keys()
                }
                env_vars = {
                    job_name: args.get(job_name, {}).get("env_vars", None)
                    for job_name in job_group.jobs.keys()
                }
                return template.render(
                    job_group=job_group,
                    dependency=dependency,
                    cluster=cluster,
                    args=sequential_args,
                    env_vars=env_vars,
                    experiment_id=experiment_id,
                    identity=identity,
                )
            case _:
                raise ValueError(f"Unsupported job type: {type(job)}")

    @tp.overload
    async def launch(
        self,
        *,
        cluster: SlurmClusterConfig,
        job: xm.JobGroup,
        dependency: dependencies.SlurmJobDependency | None = None,
        args: tp.Mapping[str, JobArgs] | None,
        experiment_id: int,
        identity: str | None = ...,
    ) -> SlurmHandle: ...

    @tp.overload
    async def launch(
        self,
        *,
        cluster: SlurmClusterConfig,
        job: xm.Job,
        dependency: dependencies.SlurmJobDependency | None = None,
        args: tp.Sequence[JobArgs],
        experiment_id: int,
        identity: str | None = ...,
    ) -> list[SlurmHandle]: ...

    @tp.overload
    async def launch(
        self,
        *,
        cluster: SlurmClusterConfig,
        job: xm.Job,
        dependency: dependencies.SlurmJobDependency | None = None,
        args: JobArgs,
        experiment_id: int,
        identity: str | None = ...,
    ) -> SlurmHandle: ...

    async def launch(
        self,
        *,
        cluster: SlurmClusterConfig,
        job: xm.Job | xm.JobGroup,
        dependency: dependencies.SlurmJobDependency | None = None,
        args: tp.Mapping[str, JobArgs] | tp.Sequence[JobArgs] | JobArgs | None,
        experiment_id: int,
        identity: str | None = None,
    ):
        template = await self.template(
            job=job,
            dependency=dependency,
            cluster=cluster,
            args=args,
            experiment_id=experiment_id,
            identity=identity,
        )
        logger.debug("Slurm submission script:\n%s", template)

        # Hash submission script
        template_hash = hashlib.blake2s(template.encode()).hexdigest()[:8]

        conn = await self.connection(cluster.ssh)
        async with conn.start_sftp_client() as sftp:
            # Write the submission script to the cluster
            # TODO(jfarebro): SHOULD FIND A WAY TO GET THE HOME DIRECTORY
            # INSTEAD OF ASSUMING SFTP PUTS US IN THE HOME DIRECTORY
            await sftp.makedirs(f".local/state/xm-slurm/{experiment_id}", exist_ok=True)
            async with sftp.open(
                f".local/state/xm-slurm/{experiment_id}/submission-script-{template_hash}.sh", "w"
            ) as fp:
                await fp.write(template)

        # Construct and run command on the cluster
        command = f"sbatch --chdir .local/state/xm-slurm/{experiment_id} --parsable submission-script-{template_hash}.sh"
        result = await self.run(cluster.ssh, command)
        if result.returncode != 0:
            raise RuntimeError(f"Failed to schedule job on {cluster.ssh.host}: {result.stderr}")

        assert isinstance(result.stdout, str)
        slurm_job_id, *_ = result.stdout.split(",")
        slurm_job_id = slurm_job_id.strip()

        console.log(
            f"[magenta]:rocket: Job [cyan]{slurm_job_id}[/cyan] will be launched on "
            f"[cyan]{cluster.name}[/cyan] "
        )

        # If we scheduled an array job make sure to return a list of handles
        # The indexing is always sequential in 0, 1, ..., n - 1
        if isinstance(job, xm.Job) and isinstance(args, collections.abc.Sequence):
            assert job.name is not None
            return [
                SlurmHandle(
                    experiment_id=experiment_id,
                    ssh=cluster.ssh,
                    slurm_job=f"{slurm_job_id}_{array_index}",
                    job_name=job.name,
                )
                for array_index in range(len(args))
            ]
        elif isinstance(job, xm.Job):
            assert job.name is not None
            return SlurmHandle(
                experiment_id=experiment_id,
                ssh=cluster.ssh,
                slurm_job=slurm_job_id,
                job_name=job.name,
            )
        elif isinstance(job, xm.JobGroup):
            # TODO: make this work for actual job groups.
            job = tp.cast(xm.Job, mit.one(job.jobs.values()))
            assert isinstance(job, xm.Job)
            assert job.name is not None
            return SlurmHandle(
                experiment_id=experiment_id,
                ssh=cluster.ssh,
                slurm_job=slurm_job_id,
                job_name=job.name,
            )
        else:
            raise ValueError(f"Unsupported job type: {type(job)}")

    def __del__(self):
        for conn in self._connections.values():
            conn.close()


@tp.overload
async def launch(
    *,
    job: xm.JobGroup,
    dependency: dependencies.SlurmJobDependency | None = None,
    args: tp.Mapping[str, JobArgs],
    experiment_id: int,
    identity: str | None = ...,
) -> SlurmHandle: ...


@tp.overload
async def launch(
    *,
    job: xm.Job,
    dependency: dependencies.SlurmJobDependency | None = None,
    args: tp.Sequence[JobArgs],
    experiment_id: int,
    identity: str | None = ...,
) -> list[SlurmHandle]: ...


@tp.overload
async def launch(
    *,
    job: xm.Job,
    dependency: dependencies.SlurmJobDependency | None = None,
    args: JobArgs,
    experiment_id: int,
    identity: str | None = ...,
) -> SlurmHandle: ...


async def launch(
    *,
    job: xm.Job | xm.JobGroup,
    dependency: dependencies.SlurmJobDependency | None = None,
    args: tp.Mapping[str, JobArgs] | tp.Sequence[JobArgs] | JobArgs,
    experiment_id: int,
    identity: str | None = None,
) -> SlurmHandle | list[SlurmHandle]:
    match job:
        case xm.Job() as job:
            if not isinstance(job.executor, executors.Slurm):
                raise ValueError("Job must have a Slurm executor")
            job_requirements = job.executor.requirements
            cluster = job_requirements.cluster
            if cluster is None:
                raise ValueError("Job must have a cluster requirement")
            if cluster.validate is not None:
                cluster.validate(job)

            return await get_client().launch(
                cluster=cluster,
                job=job,
                dependency=dependency,
                args=tp.cast(JobArgs | tp.Sequence[JobArgs], args),
                experiment_id=experiment_id,
                identity=identity,
            )
        case xm.JobGroup() as job_group:
            job_group_executors = set()
            job_group_clusters = set()
            for job_item in job_group.jobs.values():
                if not isinstance(job_item, xm.Job):
                    raise ValueError("Job group must contain only jobs")
                if not isinstance(job_item.executor, executors.Slurm):
                    raise ValueError("Job must have a Slurm executor")
                if job_item.executor.requirements.cluster is None:
                    raise ValueError("Job must have a cluster requirement")
                if job_item.executor.requirements.cluster.validate is not None:
                    job_item.executor.requirements.cluster.validate(job_item)
                job_group_clusters.add(job_item.executor.requirements.cluster)
                job_group_executors.add(id(job_item.executor))
            if len(job_group_executors) != 1:
                raise ValueError("Job group must have the same executor for all jobs")
            if len(job_group_clusters) != 1:
                raise ValueError("Job group must have the same cluster for all jobs")

            return await get_client().launch(
                cluster=job_group_clusters.pop(),
                job=job_group,
                dependency=dependency,
                args=tp.cast(tp.Mapping[str, JobArgs], args),
                experiment_id=experiment_id,
                identity=identity,
            )
