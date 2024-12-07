import datetime as dt

from absl import app
from xmanager import xm

import xm_slurm
import xm_slurm.contrib.clusters


@xm.run_in_asyncio_loop
async def main(_):
    async with xm_slurm.create_experiment("My Experiment") as experiment:
        [status_executable, echo_executable] = experiment.package(
            [
                xm_slurm.uv_container(
                    executor_spec=xm_slurm.Slurm.Spec(
                        tag="ghcr.io/jessefarebro/xm-slurm/test:latest"
                    ),
                    entrypoint=xm.ModuleName("rich.status"),
                ),
                xm_slurm.docker_container(
                    executor_spec=xm_slurm.Slurm.Spec(
                        tag="ghcr.io/jessefarebro/xm-slurm/test-echo:latest"
                    ),
                ),
            ],
        )

        time = dt.timedelta(hours=1)
        wu = await experiment.add(
            xm.JobGroup(
                status=xm.Job(
                    executable=status_executable,
                    executor=xm_slurm.Slurm(
                        requirements=xm_slurm.JobRequirements(
                            CPU=1,
                            RAM=1.0 * xm.GiB,
                            cluster=xm_slurm.contrib.clusters.mila(),
                        ),
                        time=time,
                    ),
                ),
                echo=xm.Job(
                    executable=echo_executable,
                    executor=xm_slurm.Slurm(
                        requirements=xm_slurm.JobRequirements(
                            CPU=4,
                            RAM=8.0 * xm.GiB,
                            cluster=xm_slurm.contrib.clusters.mila(),
                        ),
                        time=time,
                    ),
                ),
            )
        )

        print(wu.launched_jobs)


if __name__ == "__main__":
    app.run(main)
