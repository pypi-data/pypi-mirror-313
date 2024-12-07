import datetime as dt

from absl import app
from xmanager import xm

import xm_slurm
import xm_slurm.contrib.clusters


def main(_):
    with xm_slurm.create_experiment("My Experiment") as experiment:
        # Step 1: Specify the executor specification
        executor_spec = xm_slurm.Slurm.Spec(tag="ghcr.io/jessefarebro/xm-slurm/test:latest")

        # Step 2: Specify the executable and package it
        [executable] = experiment.package(
            [
                xm_slurm.python_container(
                    executor_spec=executor_spec,
                    entrypoint=xm.CommandList(["main.py"]),
                ),
            ],
        )

        experiment.add(
            xm.Job(
                executable=executable,
                executor=xm_slurm.Slurm(
                    requirements=xm_slurm.JobRequirements(
                        CPU=1,
                        RAM=1 * xm.GiB,
                        cluster=xm_slurm.contrib.clusters.mila(),
                    ),
                    time=dt.timedelta(hours=1),
                ),
            )
        )


if __name__ == "__main__":
    app.run(main)
