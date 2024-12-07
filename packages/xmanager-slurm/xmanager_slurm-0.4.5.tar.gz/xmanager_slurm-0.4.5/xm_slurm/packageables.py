import importlib.resources as resources
import pathlib
import sys
from typing import Literal, Mapping, Sequence

import immutabledict
from xmanager import xm

from xm_slurm import job_blocks, utils
from xm_slurm.executables import Dockerfile, DockerImage
from xm_slurm.executors import SlurmSpec


def docker_image(
    *,
    image: str,
    args: xm.UserArgs | None = None,
    env_vars: Mapping[str, str] = immutabledict.immutabledict(),
) -> xm.Packageable:
    """Creates a packageable for a pre-built Docker image.

    Args:
        image: The remote image URI.
        args: The user arguments to pass to the executable.
        env_vars: The environment variables to pass to the executable.

    Returns: A packageable for a pre-built Docker image.
    """
    return xm.Packageable(
        executor_spec=SlurmSpec(),
        executable_spec=DockerImage(image=image),
        args=xm.SequentialArgs.from_collection(args),
        env_vars=dict(env_vars),
    )


def docker_container(
    *,
    executor_spec: xm.ExecutorSpec,
    dockerfile: pathlib.Path | None = None,
    context: pathlib.Path | None = None,
    target: str | None = None,
    ssh: Sequence[str] | Literal[True] | None = None,
    build_args: Mapping[str, str] = immutabledict.immutabledict(),
    cache_from: str | Sequence[str] | None = None,
    labels: Mapping[str, str] = immutabledict.immutabledict(),
    workdir: pathlib.Path | None = None,
    args: xm.UserArgs | None = None,
    env_vars: Mapping[str, str] = immutabledict.immutabledict(),
) -> xm.Packageable:
    """Creates a Docker container packageable from a dockerfile.

    Args:
        executor_spec: The executor specification, where will the container be stored at.
        dockerfile: The path to the dockerfile.
        context: The path to the docker context.
        target: The docker build target.
        ssh: A list of SSH sockets/keys for the docker build step or `True` to use the default SSH agent.
        build_args: Build arguments to docker.
        cache_from: Where to pull the BuildKit cache from. See `--cache-from` in `docker build`.
        labels: The container labels.
        workdir: The working directory in container.
        args: The user arguments to pass to the executable.
        env_vars: The environment variables to pass to the executable.

    Returns: A Docker container packageable.
    """
    if context is None:
        context = utils.find_project_root()
    context = context.resolve()
    if dockerfile is None:
        dockerfile = context / "Dockerfile"
    dockerfile = dockerfile.resolve()

    if ssh is None:
        ssh = []
    elif ssh is True:
        ssh = ["default"]

    if cache_from is None and isinstance(executor_spec, SlurmSpec):
        cache_from = executor_spec.tag
    if cache_from is None:
        cache_from = []
    elif isinstance(cache_from, str):
        cache_from = [cache_from]

    return xm.Packageable(
        executor_spec=executor_spec,
        executable_spec=Dockerfile(
            dockerfile=dockerfile,
            context=context,
            target=target,
            ssh=ssh,
            build_args=build_args,
            cache_from=cache_from,
            workdir=workdir,
            labels=labels,
        ),
        args=xm.SequentialArgs.from_collection(args),
        env_vars=dict(env_vars),
    )


def python_container(
    *,
    executor_spec: xm.ExecutorSpec,
    entrypoint: xm.ModuleName | xm.CommandList,
    context: pathlib.Path | None = None,
    requirements: pathlib.Path | None = None,
    base_image: str = "docker.io/python:{major}.{minor}-slim",
    extra_system_packages: Sequence[str] = (),
    extra_python_packages: Sequence[str] = (),
    cache_from: str | Sequence[str] | None = None,
    labels: Mapping[str, str] = immutabledict.immutabledict(),
    ssh: Sequence[str] | Literal[True] | None = None,
    args: xm.UserArgs | None = None,
    env_vars: Mapping[str, str] = immutabledict.immutabledict(),
) -> xm.Packageable:
    """Creates a Python container from a base image using pip from a `requirements.txt` file.

    NOTE: The base image will use the Python version of the current interpreter.
    NOTE: uv is used to install packages from `requirements`.

    Args:
        executor_spec: The executor specification, where will the container be stored at.
        entrypoint: The entrypoint to run in the container.
        context: The path to the docker context.
        requirements: The path to the pip requirements file.
        base_image: The base image to use. NOTE: The base image must contain the Python runtime.
        extra_system_packages: Additional system packages to install. NOTE: These are installed via `apt-get`.
        extra_python_packages: Additional Python packages to install. NOTE: These are installed via `uv pip`.
        cache_from: Where to pull the BuildKit cache from. See `--cache-from` in `docker build`.
        labels: The container labels.
        ssh: A list of SSH sockets/keys for the docker build step or `True` to use the default SSH agent.
        args: The user arguments to pass to the executable.
        env_vars: The environment variables to pass to the executable.

    Returns: A Python container packageable.
    """
    entrypoint_args = job_blocks.get_args_for_python_entrypoint(entrypoint)
    args = xm.merge_args(entrypoint_args, args or {})

    if context is None:
        context = utils.find_project_root()
    context = context.resolve()
    if requirements is None:
        requirements = context / "requirements.txt"
    requirements = requirements.resolve()
    if not requirements.exists():
        raise ValueError(f"Pip requirements `{requirements}` doesn't exist.")
    if not requirements.is_relative_to(context):
        raise ValueError(
            f"Pip requirements `{requirements}` must be relative to context: `{context}`"
        )

    with resources.as_file(
        resources.files("xm_slurm.templates").joinpath("docker/python.Dockerfile")
    ) as dockerfile:
        return docker_container(
            executor_spec=executor_spec,
            dockerfile=dockerfile,
            context=context,
            ssh=ssh,
            build_args={
                "PIP_REQUIREMENTS": requirements.relative_to(context).as_posix(),
                "EXTRA_SYSTEM_PACKAGES": " ".join(extra_system_packages),
                "EXTRA_PYTHON_PACKAGES": " ".join(extra_python_packages),
                "BASE_IMAGE": base_image.format_map({
                    "major": sys.version_info.major,
                    "minor": sys.version_info.minor,
                    "micro": sys.version_info.micro,
                }),
            },
            cache_from=cache_from,
            labels=labels,
            # We must specify the workdir manually for apptainer support
            workdir=pathlib.Path("/workspace"),
            args=args,
            env_vars=env_vars,
        )


def mamba_container(
    *,
    executor_spec: xm.ExecutorSpec,
    entrypoint: xm.ModuleName | xm.CommandList,
    context: pathlib.Path | None = None,
    environment: pathlib.Path | None = None,
    base_image: str = "gcr.io/distroless/base-debian10",
    cache_from: str | Sequence[str] | None = None,
    labels: Mapping[str, str] = immutabledict.immutabledict(),
    ssh: Sequence[str] | Literal[True] | None = None,
    args: xm.UserArgs | None = None,
    env_vars: Mapping[str, str] = immutabledict.immutabledict(),
) -> xm.Packageable:
    """Creates a Conda container from a base image using mamba from a `environment.yml` file.

    Note: The base image *doesn't* need to contain the Python runtime.

    Args:
        executor_spec: The executor specification, where will the container be stored at.
        entrypoint: The entrypoint to run in the container.
        context: The path to the docker context.
        environment: The path to the conda environment file.
        base_image: The base image to use.
        cache_from: Where to pull the BuildKit cache from. See `--cache-from` in `docker build`.
        labels: The container labels.
        ssh: A list of SSH sockets/keys for the docker build step or `True` to use the default SSH agent.
        args: The user arguments to pass to the executable.
        env_vars: The environment variables to pass to the executable.

    Returns: A Conda container packageable.
    """
    entrypoint_args = job_blocks.get_args_for_python_entrypoint(entrypoint)
    args = xm.merge_args(entrypoint_args, args or {})

    if context is None:
        context = utils.find_project_root()
    context = context.resolve()
    if environment is None:
        environment = context / "environment.yml"
    environment = environment.resolve()
    if not environment.exists():
        raise ValueError(f"Conda environment manifest `{environment}` doesn't exist.")
    if not environment.is_relative_to(context):
        raise ValueError(
            f"Conda environment manifest `{environment}` must be relative to context: `{context}`"
        )

    with resources.as_file(
        resources.files("xm_slurm.templates").joinpath("docker/mamba.Dockerfile")
    ) as dockerfile:
        return docker_container(
            executor_spec=executor_spec,
            dockerfile=dockerfile,
            context=context,
            ssh=ssh,
            build_args={
                "CONDA_ENVIRONMENT": environment.relative_to(context).as_posix(),
                "BASE_IMAGE": base_image,
            },
            cache_from=cache_from,
            labels=labels,
            # We must specify the workdir manually for apptainer support
            workdir=pathlib.Path("/workspace"),
            args=args,
            env_vars=env_vars,
        )


conda_container = mamba_container


def uv_container(
    *,
    executor_spec: xm.ExecutorSpec,
    entrypoint: xm.ModuleName | xm.CommandList,
    context: pathlib.Path | None = None,
    base_image: str = "docker.io/python:{major}.{minor}-slim-bookworm",
    extra_system_packages: Sequence[str] = (),
    extra_python_packages: Sequence[str] = (),
    cache_from: str | Sequence[str] | None = None,
    labels: Mapping[str, str] = immutabledict.immutabledict(),
    ssh: Sequence[str] | Literal[True] | None = None,
    args: xm.UserArgs | None = None,
    env_vars: Mapping[str, str] = immutabledict.immutabledict(),
) -> xm.Packageable:
    """Creates a Python container from a base image using uv from a `uv.lock` file.

    Args:
        executor_spec: The executor specification, where will the container be stored at.
        entrypoint: The entrypoint to run in the container.
        context: The path to the docker context.
        base_image: The base image to use. NOTE: The base image must contain the Python runtime.
        extra_system_packages: Additional system packages to install. NOTE: These are installed via `apt-get`.
        extra_python_packages: Additional Python packages to install. NOTE: These are installed via `uv pip`.
        cache_from: Where to pull the BuildKit cache from. See `--cache-from` in `docker build`.
        labels: The container labels.
        ssh: A list of SSH sockets/keys for the docker build step or `True` to use the default SSH agent.
        args: The user arguments to pass to the executable.
        env_vars: The environment variables to pass to the executable.

    Returns: A Python container packageable.
    """
    entrypoint_args = job_blocks.get_args_for_python_entrypoint(entrypoint)
    args = xm.merge_args(entrypoint_args, args or {})

    if context is None:
        context = utils.find_project_root()
    context = context.resolve()
    if not (context / "pyproject.toml").exists():
        raise ValueError(f"Python project file `{context / 'pyproject.toml'}` doesn't exist.")
    if not (context / "uv.lock").exists():
        raise ValueError(f"UV lock file `{context / 'uv.lock'}` doesn't exist.")

    with resources.as_file(
        resources.files("xm_slurm.templates").joinpath("docker/uv.Dockerfile")
    ) as dockerfile:
        return docker_container(
            executor_spec=executor_spec,
            dockerfile=dockerfile,
            context=context,
            ssh=ssh,
            build_args={
                "EXTRA_SYSTEM_PACKAGES": " ".join(extra_system_packages),
                "EXTRA_PYTHON_PACKAGES": " ".join(extra_python_packages),
                "BASE_IMAGE": base_image.format_map({
                    "major": sys.version_info.major,
                    "minor": sys.version_info.minor,
                    "micro": sys.version_info.micro,
                }),
            },
            cache_from=cache_from,
            labels=labels,
            # We must specify the workdir manually for apptainer support
            workdir=pathlib.Path("/workspace"),
            args=args,
            env_vars=env_vars,
        )
