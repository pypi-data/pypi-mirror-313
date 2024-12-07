import asyncio
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
                    entrypoint=xm.CommandList(["main.py"]),
                ),
            ],
        )

        executor = xm_slurm.Slurm(
            requirements=xm_slurm.JobRequirements(
                CPU=1,
                RAM=1 * xm.GiB,
                H100=2,
                cluster=xm_slurm.contrib.clusters.mila(),
            ),
            time=dt.timedelta(hours=1),
        )

        async def make_job(wu: xm.WorkUnit, args: xm.UserArgs) -> None:
            await wu.add(
                xm.Job(
                    executable=executable,
                    executor=executor,
                    args=xm.merge_args(
                        args,
                        {"workdir": f"/scratch/{wu.experiment_id}/{wu.work_unit_id}"},
                    ),
                )
            )

        args = [xm_slurm.JobArgs(args={"scale": scale}) for scale in range(3)]
        wus = await experiment.add(make_job, args)

        for wu, status in zip(wus, await asyncio.gather(*[wu.get_status() for wu in wus])):
            print(f"Work Unit {wu.work_unit_id} Status: {status}")

        await asyncio.gather(*[wu.wait_until_complete() for wu in wus])
        print("All jobs finished!")


if __name__ == "__main__":
    app.run(main)
