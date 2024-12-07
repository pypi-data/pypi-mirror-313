# XManager Slurm


XManager Slurm is a Slurm executor for the [XManager](https://github.com/google-deepmind/xmanager) library.
Typical HPC development on Slurm clusters can have various sharp edges that this project seeks to resolve.
The main goals of the project are:

1. __Provide reproducable and reliable experiment launching.__
    - This is primarily accomplished by using containers, we leverage Docker for building containers and support Singularity / Apptainer as well as Podman as container runtimes.
    - Packaging code in containers guarantees jobs run exactly as is when the job was scheduled.
2. __Write powerful and flexible job / launch scripts entirely in Python.__
    - No more bash scripting.
    - Ability to schedule groups of jobs with different resource requirements that all run concurrently.
    - Ability to easily create job pipelines, e.g., running evaluation jobs after a training job completes.
3. __Schedule across multiple clusters.__
    - Schedule jobs agaisnt multiple clusters choosing the cluster that'll begin your job first.

---

## Workflow

The general workflow of using xm-slurm generally looks like this:

<br>

```{image} assets/workflow-light.svg
:class: only-light
```
```{image} assets/workflow-dark.svg
:class: only-dark
```

<br>

This breaks down into three steps:

1. Build & Push your runtime and code to a remote registry like [Docker Hub](https://hub.docker.com) or the [Github Container Registry](ghcr.io).
2. Schedule a job on the target Slurm cluster.
3. Once the job is running your code and runtime are pulled from the container registry and your code is run within the container.


## FAQ

__My cluster doesn't have Docker, how can I use xm-slurm?__

Your cluster doesn't need to have Docker but it must have some OCI-compatible container runtime like [Singularity](https://sylabs.io/) / [Apptainer](https://apptainer.org/) or [Podman](https://podman.io/).

---

__Isn't this wasteful / won't it be burdensome to build & pull a container whenever I want to launch a job?__

No. OCI containers perform deduplication via layers, the build process will cache expensive operations like downloading dependencies and only cheaper operations have to be performed between launches like copying your code. The same goes for the container runtime, expensive layers will already be cached so startup time is minimal.

---

__I can't access the internet from compute nodes on my cluster, will xm-slurm work for me?__

It can. One workaround we have implemented is the ability to proxy requests through the node that submitted the job. The proper long term solution is to work with your cluster admin to put a container registry on the firewall allowlist.

```{toctree}
:caption: Getting Started 
:hidden:
:maxdepth: 1
:titlesonly:

getting-started/xmanager
```

```{toctree}
:caption: Guides
:hidden:
:maxdepth: 1
:titlesonly:

guides/remote-dev
```

```{toctree}
:caption: API Documentation
:hidden:
:maxdepth: 5
:titlesonly:

api/executors
api/executables
api/packageables

```