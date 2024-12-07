import datetime as dt

from absl import app
from xmanager import xm

import xm_slurm
import xm_slurm.contrib.clusters


@xm.run_in_asyncio_loop
async def main(_):
    async with xm_slurm.create_experiment("My Experiment") as experiment:
        # Step 1: Specify the executor specification
        executor_spec = xm_slurm.Slurm.Spec(tag="ghcr.io/jessefarebro/xm-slurm/test:latest")

        # Step 2: Specify the executable and package it
        [executable] = experiment.package(
            [
                xm_slurm.uv_container(
                    executor_spec=executor_spec,
                    # Equivalent of `-m rich.status`
                    entrypoint=xm.ModuleName("rich.status"),
                ),
            ],
        )

        # Step 3: Construct requirements & executor
        requirements = xm_slurm.JobRequirements(
            CPU=1,
            RAM=1.0 * xm.GiB,
            GPU=1,
            replicas=1,
            cluster=xm_slurm.contrib.clusters.mila(),
        )
        executor = xm_slurm.Slurm(
            requirements=requirements,
            time=dt.timedelta(hours=1),
        )

        # Step 4: Schedule job
        wu = await experiment.add(
            xm.Job(
                executable=executable,
                executor=executor,
            )
        )

        await wu.wait_until_complete()
        print(f"Job finished executing with status {await wu.get_status()}")


if __name__ == "__main__":
    app.run(main)
