import asyncio
import base64
import dataclasses
import enum
import functools
import logging
import zlib
from typing import Awaitable, Callable, Concatenate, Coroutine, Mapping, ParamSpec, TypeVar

import backoff
import cloudpickle
from xmanager import xm

import xm_slurm
from xm_slurm import job_blocks, status
from xm_slurm.experiment import SlurmAuxiliaryUnit, SlurmExperiment

P = ParamSpec("P")
T = TypeVar("T")

logger = logging.getLogger(__name__)


async def _monitor_parameter_controller(
    aux_unit: SlurmAuxiliaryUnit,
    local_parameter_controller_coro: Coroutine[None, None, T],
    *,
    poll_interval: float = 30.0,
) -> None:
    local_controller_finished = asyncio.Event()
    local_parameter_controller = asyncio.create_task(local_parameter_controller_coro)

    @local_parameter_controller.add_done_callback
    def _(future: asyncio.Task[T]) -> None:
        try:
            _ = future.result()
        except asyncio.CancelledError:
            logger.info("Local parameter controller was cancelled, resuming on remote controller.")
            pass
        except Exception:
            logger.error("Local parameter controller failed, stopping remote controller.")
            aux_unit.stop(
                mark_as_failed=True, mark_as_completed=False, message="Local controller failed."
            )
            raise
        else:
            logger.info(
                "Local parameter controller finished before remote controller started, "
                "stopping remote controller."
            )
            local_controller_finished.set()
            aux_unit.stop(mark_as_completed=True, message="Local parameter controller finished.")

    @backoff.on_predicate(
        backoff.constant,
        lambda aux_unit_status: aux_unit_status is status.SlurmWorkUnitStatusEnum.PENDING,
        jitter=None,
        interval=poll_interval,
    )
    async def wait_for_remote_controller() -> status.SlurmWorkUnitStatusEnum:
        logger.info("Waiting for remote parameter controller to start.")
        if local_controller_finished.is_set():
            return status.SlurmWorkUnitStatusEnum.COMPLETED
        return (await aux_unit.get_status()).status

    logger.info("Monitoring remote parameter controller.")
    # TODO(jfarebro): make get_status() more resiliant to errors when initially scheduling.
    # We run into issues if we call get_status() too quickly when Slurm hasn't ingested the job.
    await asyncio.sleep(15)
    match await wait_for_remote_controller():
        case status.SlurmWorkUnitStatusEnum.RUNNING:
            logger.info("Remote parameter controller started.")
            local_parameter_controller.cancel("Remote parameter controller started.")
        case status.SlurmWorkUnitStatusEnum.COMPLETED:
            if local_parameter_controller.done():
                logger.info("Local parameter controller finished, stopping remote controller.")
                aux_unit.stop(
                    mark_as_completed=True, message="Local parameter controller finished."
                )
            else:
                logger.info("Remote parameter controller finished, stopping local controller.")
                local_parameter_controller.cancel()
        case status.SlurmWorkUnitStatusEnum.FAILED:
            logger.error("Remote parameter controller failed, stopping local controller.")
            local_parameter_controller.cancel()
        case status.SlurmWorkUnitStatusEnum.CANCELLED:
            logger.info("Remote parameter controller was cancelled, stopping local controller.")
            local_parameter_controller.cancel()
        case status.SlurmWorkUnitStatusEnum.PENDING:
            raise RuntimeError("Remote parameter controller is still pending, invalid state.")


class ParameterControllerMode(enum.Enum):
    AUTO = enum.auto()
    REMOTE_ONLY = enum.auto()
    # TODO(jfarebro): is it possible to get LOCAL_ONLY?
    # We'd need to have a dummy job type as we need to return a JobType?


def parameter_controller(
    *,
    executable: xm.Executable,
    executor: xm.Executor,
    controller_mode: ParameterControllerMode = ParameterControllerMode.AUTO,
    controller_name: str = "parameter_controller",
    controller_args: xm.UserArgs | None = None,
    controller_env_vars: Mapping[str, str] | None = None,
) -> Callable[
    [
        Callable[Concatenate[SlurmExperiment, P], T]
        | Callable[Concatenate[SlurmExperiment, P], Awaitable[T]],
    ],
    Callable[P, xm.AuxiliaryUnitJob],
]:
    """Converts a function to a controller which can be added to an experiment.

    Calling the wrapped function would return an xm.JobGenerator which would run
    it as auxiliary unit on the specified executor.

    Args:
        executable: An executable that has a Python entrypoint with all the necesarry dependencies.
        executor: The executor to launch the controller job on.
        controller_name: Name of the parameter controller job.
        controller_args: Mapping of flag names and values to be used by the XM
          client running inside the parameter controller job.
        controller_env_vars: Mapping of env variable names and values to be passed
          to the parameter controller job.

    Returns:
        A decorator to be applied to the function.
    """

    def decorator(
        f: Callable[Concatenate[SlurmExperiment, P], T]
        | Callable[Concatenate[SlurmExperiment, P], Awaitable[T]],
    ) -> Callable[P, xm.AuxiliaryUnitJob]:
        @functools.wraps(f)
        def make_controller(*args: P.args, **kwargs: P.kwargs) -> xm.AuxiliaryUnitJob:
            # Modify the function to read the experiment from the API so that it can be pickled.

            async def job_generator(aux_unit: SlurmAuxiliaryUnit) -> None:
                experiment_id = aux_unit.experiment.experiment_id

                async def local_controller(*args: P.args, **kwargs: P.kwargs) -> T | Awaitable[T]:
                    if asyncio.iscoroutinefunction(f):
                        return await f(aux_unit.experiment, *args, **kwargs)
                    else:
                        return f(aux_unit.experiment, *args, **kwargs)

                async def remote_controller(*args: P.args, **kwargs: P.kwargs) -> T | Awaitable[T]:
                    async with xm_slurm.get_experiment(experiment_id=experiment_id) as exp:
                        if asyncio.iscoroutinefunction(f):
                            return await f(exp, *args, **kwargs)
                        else:
                            return f(exp, *args, **kwargs)

                remote_controller_serialized = base64.urlsafe_b64encode(
                    zlib.compress(
                        cloudpickle.dumps(
                            functools.partial(remote_controller, *args, **kwargs),
                        )
                    )
                )

                parameter_controller_executable = dataclasses.replace(
                    executable,
                    args=xm.merge_args(
                        job_blocks.get_args_for_python_entrypoint(
                            xm.ModuleName("xm_slurm.scripts._cloudpickle")
                        ),
                        xm.SequentialArgs.from_collection({
                            "cloudpickled_fn": remote_controller_serialized.decode("ascii"),
                        }),
                        xm.SequentialArgs.from_collection(controller_args),
                    ),
                    env_vars=controller_env_vars or {},
                )

                await aux_unit.add(
                    xm.Job(
                        executor=executor,
                        executable=parameter_controller_executable,
                        name=controller_name,
                    )
                )

                # Launch local parameter controller and monitor for when it starts running
                # so we can kill the local controller.
                if controller_mode is ParameterControllerMode.AUTO:
                    aux_unit._create_task(
                        _monitor_parameter_controller(aux_unit, local_controller(*args, **kwargs))
                    )

            return xm.AuxiliaryUnitJob(
                job_generator,
                importance=xm.Importance.HIGH,
                termination_delay_secs=0,  # TODO: add support for termination delay.?
            )

        return make_controller

    return decorator
