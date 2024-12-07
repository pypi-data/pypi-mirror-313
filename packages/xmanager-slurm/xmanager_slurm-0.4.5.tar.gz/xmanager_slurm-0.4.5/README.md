# 👨‍🔬 XManager Slurm

<p align="center">
    <em><a href="https://jessefarebro.github.io/xm-slurm">Documentation</a></em>
    &nbsp;&nbsp;&bull;&nbsp;&nbsp;
    <em><code>pip install xmanager-slurm</code></em>
</p>

<!--
Badges
<p align="center">
    <img alt="build" src="https://github.com/jessefarebro/xm-slurm/actions/workflows/build.yml/badge.svg" />
    <img alt="mypy" src="https://github.com/jessefarebro/xm-slurm/actions/workflows/mypy.yml/badge.svg" />
    <img alt="pyright" src="https://github.com/jessefarebro/xm-slurm/actions/workflows/pyright.yml/badge.svg" />
    <img alt="ruff" src="https://github.com/jessefarebro/xm-slurm/actions/workflows/ruff.yml/badge.svg" />
    <a href="https://codecov.io/gh/jessefarebro/xm-slurm">
        <img alt="codecov" src="https://codecov.io/gh/jessefarebro/xm-slurm/branch/main/graph/badge.svg" />
    </a>
    <a href="https://pypi.org/project/xmanager-slurm/">
        <img alt="codecov" src="https://img.shields.io/pypi/pyversions/xmanager-slurm" />
    </a>
</p>
-->

This project implements Slurm support for the XManager experiment launcher.
The aim is to support a general workflow for idempotent launching of experiments to many Slurm clusters
through the use of containerization.
This can provide the following benefits which eliminates various sharp edges of using Slurm for both new and experienced users alike:

1. All development can be done locally and launched on any Slurm cluster without ever interacting with the cluster.
2. Reproducible experiments (e.g., containerized runtime, code checkpointing, etc.)
3. Launch scripts are written in __Python__ which makes it easy to perform complex launch configurations like distributed training or job orchestration.
4. Full control over resource scheduling, choose the cluster that meets your requirements and will schedule your job the fastest.

The following diagram illustrates the general workflow achieved by using XManager Slurm.


<picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/workflow-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="docs/assets/workflow-light.svg">
    <img alt="XManager workflow with the Slurm executor." src="docs/assets/workflow-light.svg">
</picture>

## Alternatives

This project was spawned from what I perceived as a lack of unoppiniated infrastructure for scheduling jobs.
Contrasting with the most popular libraries here's what XManager + Slurm provides:

* [submitit](https://github.com/facebookincubator/submitit): The submitit plugin is quite popular alongside of the [Hydra](https://hydra.cc/) configuration library. Although these work well in conjunction this might not meet your requirements if and you may consider XMangaer + Slurm if:
    * You don't want to use Hydra.
    * You have more complex needs for sweeps beyond the most common usecases of taking the caretesian product amongst a grid of parameters.
    * You want to schedule jobs on multiple clusters without having to re-configure your development environment.
    * You want better control over resource scheduling beyond what Slurm can provide.
    * You want more control over launch configurations / parameter sweeps by being able to write them in Python.
    * You require launch configurations that go beyond simple single job configurations, e.g., job orchestration, distributed training, etc.

## License

This work is dual-licensed under Apache 2.0 and MIT License.
You can choose between one of them if you use this work.
See [LICENSE.md](./LICENSE.md) for more information.

## Disclaimer

This project is not an official Google project. It is not supported by Google and Google specifically disclaims all warranties as to its quality, merchantability, or fitness for a particular purpose.