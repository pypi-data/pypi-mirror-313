import asyncio
import contextlib
import datetime as dt
import random
import signal
import sys

from absl import app, flags
from xmanager import xm

import xm_slurm
import xm_slurm.contrib.clusters
import xm_slurm.experimental.parameter_controller as parameter_controller

GHCR_USER = flags.DEFINE_string("ghcr_user", "jessefarebro", "GitHub Container Registry user")
RESTORE_FROM = flags.DEFINE_integer("restore_from", None, "Experiment id")


@xm.run_in_asyncio_loop
async def main(_):
    async with contextlib.AsyncExitStack() as stack:
        if RESTORE_FROM.value is not None:
            experiment = await stack.enter_async_context(
                xm_slurm.get_experiment(RESTORE_FROM.value)
            )
        else:
            experiment = await stack.enter_async_context(
                xm_slurm.create_experiment("My Experiment")
            )
        # Step 1: Specify the executor specification
        executor_spec = xm_slurm.Slurm.Spec(tag=f"ghcr.io/{GHCR_USER.value}/xm-slurm/test:latest")

        # Step 2: Specify the executable and package it
        [executable] = experiment.package(
            [
                xm_slurm.python_container(
                    executor_spec=executor_spec,
                    entrypoint=xm.CommandList(["main.py"]),
                ),
            ],
        )

        cluster = xm_slurm.contrib.clusters.mila()

        @parameter_controller.parameter_controller(
            executable=executable,
            executor=xm_slurm.Slurm(
                requirements=xm_slurm.JobRequirements(
                    CPU=1,
                    RAM=1 * xm.GiB,
                    cluster=cluster,
                ),
                time=dt.timedelta(minutes=6),  # 3 minutes to test requeuing / readding inner job.
                timeout_signal_grace_period=dt.timedelta(seconds=10),
                requeue_max_attempts=1000,
                requeue_on_exit_code=42,
                partition="long",
            ),
        )
        async def parameter_controller_fn(experiment: xm_slurm.SlurmExperiment):
            print("Parameter controller is running...")

            def signal_handler(signum, frame):
                del frame
                if signum == signal.SIGUSR2:
                    print("Caught SIGUSR2, exiting with requeue exit code...")
                    sys.exit(42)

            signal.signal(signal.SIGUSR2, signal_handler)

            executor = xm_slurm.Slurm(
                requirements=xm_slurm.JobRequirements(
                    CPU=1,
                    RAM=1 * xm.GiB,
                    cluster=cluster,
                ),
                time=dt.timedelta(minutes=20),  # 7 minutes to test timeouts.
                partition="long",
            )

            async def make_job(wu: xm.WorkUnit, args: dict):
                await wu.add(
                    xm.Job(
                        executable=executable,
                        executor=executor,
                        args=args,
                    )
                )

            wus = await experiment.add(
                make_job,
                args=[{"args": {"time": random.randint(300, 600)}} for _ in range(5)],
                identity="job",
            )

            # Wait for a little for the job to be created.
            await asyncio.sleep(5)

            futures = [wu.wait_until_complete() for wu in wus]

            for wu_future in asyncio.as_completed(futures):
                wu = await wu_future
                print(f"Job {wu.work_unit_id} finished")

            print("Job finished!")

        await experiment.add(parameter_controller_fn(), identity="parameter_controller")


if __name__ == "__main__":
    app.run(main)
