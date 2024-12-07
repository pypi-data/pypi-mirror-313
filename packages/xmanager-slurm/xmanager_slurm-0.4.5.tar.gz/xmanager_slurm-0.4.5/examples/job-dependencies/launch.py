import asyncio
import datetime as dt
import pathlib

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
        [train_executable, eval_executable] = experiment.package(
            [
                xm_slurm.uv_container(
                    executor_spec=executor_spec,
                    entrypoint=xm.CommandList(["train.py"]),
                ),
                xm_slurm.uv_container(
                    executor_spec=executor_spec,
                    entrypoint=xm.CommandList(["eval.py"]),
                ),
            ],
        )

        workdir = pathlib.Path(f"/scratch/xm-slurm-examples/{experiment.experiment_id}")

        # Step 4: Schedule train job
        train_executor = xm_slurm.Slurm(
            requirements=xm_slurm.JobRequirements(
                CPU=1,
                RAM=1.0 * xm.GiB,
                GPU=1,
                replicas=1,
                cluster=xm_slurm.contrib.clusters.mila(),
            ),
            time=dt.timedelta(hours=1),
        )

        async def make_train_job(wu: xm.WorkUnit, args):
            await wu.add(
                xm.Job(
                    executable=train_executable,
                    executor=train_executor,
                    args=xm.merge_args(
                        [
                            "--output_file",
                            (workdir / f"{wu.work_unit_id}" / "result.npy").as_posix(),
                        ],
                        args,
                    ),
                ),
            )

        train_wus = await experiment.add(
            make_train_job,
            args=[xm_slurm.JobArgs(args=["--seed", seed]) for seed in range(5)],
        )

        # Step 5: Schedule eval job
        eval_executor = xm_slurm.Slurm(
            requirements=xm_slurm.JobRequirements(
                CPU=1,
                RAM=1.0 * xm.GiB,
                GPU=1,
                replicas=1,
                cluster=xm_slurm.contrib.clusters.mila(),
            ),
            time=dt.timedelta(hours=1),
        )

        eval_wus = await experiment.add(
            xm.Job(
                executable=eval_executable,
                executor=eval_executor,
            ),
            args=[
                xm_slurm.JobArgs(
                    args=[
                        "--input_file",
                        (workdir / f"{wu.work_unit_id}" / "result.npy").as_posix(),
                    ]
                )
                for wu in train_wus
            ],
            dependency=[train_wu.after_completed() for train_wu in train_wus],
        )

        for wu in asyncio.as_completed([
            *[train_wu.wait_until_complete() for train_wu in train_wus],
            *[eval_wu.wait_until_complete() for eval_wu in eval_wus],
        ]):
            wu = await wu
            print(f"Work Unit {wu!r} finished executing with status {await wu.get_status()}")


if __name__ == "__main__":
    app.run(main)
