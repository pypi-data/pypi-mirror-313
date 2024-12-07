import base64
import collections.abc
import dataclasses
import enum
import functools
import hashlib
import json
import logging
import os
import pathlib
import shlex
import shutil
import subprocess
import tempfile
from typing import Hashable, Literal, Mapping, Sequence

import jinja2 as j2
from xmanager import xm

from xm_slurm.executables import (
    Dockerfile,
    DockerImage,
    ImageURI,
    RemoteImage,
    RemoteRepositoryCredentials,
)
from xm_slurm.executors import SlurmSpec
from xm_slurm.packaging import registry
from xm_slurm.packaging import utils as packaging_utils
from xm_slurm.packaging.registry import IndexedContainer

logger = logging.getLogger(__name__)


def _hash_digest(obj: Hashable) -> str:
    return hashlib.sha256(repr(obj).encode()).hexdigest()


class DockerClient:
    class Builder(enum.Enum):
        BUILDKIT = enum.auto()
        BUILDAH = enum.auto()

    def __init__(self) -> None:
        if "XM_DOCKER_CLIENT" in os.environ:
            client_call = shlex.split(os.environ["XM_DOCKER_CLIENT"])
        elif shutil.which("docker"):
            client_call = ["docker"]
        elif shutil.which("podman"):
            client_call = ["podman"]
        else:
            raise RuntimeError("No Docker client found.")
        self._client_call = client_call

        backend_version = packaging_utils.run_command(
            xm.merge_args(self._client_call, ["buildx", "version"]), return_stdout=True
        )
        if backend_version.stdout.startswith("github.com/docker/buildx"):
            self._builder = DockerClient.Builder.BUILDKIT
        else:
            raise NotImplementedError(f"Unsupported Docker build backend: {backend_version}")

        self._credentials_cache: dict[str, RemoteRepositoryCredentials] = {}

    def credentials(self, hostname: str) -> RemoteRepositoryCredentials | None:
        """Fetch credentials from the local Docker configuration."""
        if hostname in self._credentials_cache:
            return self._credentials_cache[hostname]

        def _parse_docker_credentials(helper: str) -> RemoteRepositoryCredentials | None:
            """Parse credentials from a Docker credential helper."""
            if not shutil.which(f"docker-credential-{helper}"):
                return None
            returncode, output = subprocess.getstatusoutput(
                f"echo {hostname} | docker-credential-{helper} get",
            )

            if returncode == 0:
                credentials = json.loads(output)
                return RemoteRepositoryCredentials(
                    username=credentials["Username"], password=credentials["Secret"]
                )
            return None

        def _parse_credentials_from_config(
            config_path: pathlib.Path,
        ) -> RemoteRepositoryCredentials | None:
            """Parse credentials from the Docker configuration file."""
            if not config_path.exists():
                return None
            config = json.loads(config_path.read_text())

            # Attempt to parse from the global credential store
            if (creds_store := config.get("credsStore", None)) and (
                credentials := _parse_docker_credentials(creds_store)
            ):
                self._credentials_cache[hostname] = credentials
                return credentials
            # Attempt to parse from the credential helper for this registry
            if creds_helper := config.get("credHelpers", {}):
                for registry, helper in creds_helper.items():
                    registry = ImageURI(registry)
                    if registry.domain == hostname and (
                        credentials := _parse_docker_credentials(helper)
                    ):
                        self._credentials_cache[hostname] = credentials
                        return credentials
            # Last resort: attempt to parse raw auth
            if auths := config.get("auths", None):
                for registry, metadata in auths.items():
                    registry = ImageURI(registry)
                    if registry.domain == hostname:
                        auth = base64.b64decode(metadata["auth"]).decode("utf-8")
                        username, password = auth.split(":")
                        credentials = RemoteRepositoryCredentials(username, password)
                        self._credentials_cache[hostname] = credentials
                        return credentials
            return None

        # Attempt to parse credentials from the Docker or Podman configuration
        match self._builder:
            case DockerClient.Builder.BUILDKIT:
                docker_config_path = (
                    pathlib.Path(os.environ.get("DOCKER_CONFIG", "~/.docker")).expanduser()
                    / "config.json"
                )
                return _parse_credentials_from_config(docker_config_path)
            case DockerClient.Builder.BUILDAH:
                podman_config_path = (
                    pathlib.Path(os.environ.get("XDG_CONFIG_HOME", "~/.config")).expanduser()
                    / "containers"
                    / "auth.json"
                )
                return _parse_credentials_from_config(podman_config_path)

    @functools.cached_property
    def _bake_template(self) -> j2.Template:
        template_loader = j2.PackageLoader("xm_slurm", "templates/docker")
        template_env = j2.Environment(loader=template_loader, trim_blocks=True, lstrip_blocks=False)

        return template_env.get_template("docker-bake.hcl.j2")

    def _bake_args(
        self,
        *,
        targets: str | Sequence[str] | None = None,
        builder: str | None = None,
        files: str | os.PathLike[str] | Sequence[os.PathLike[str] | str] | None = None,
        load: bool = False,
        cache: bool = True,
        print: bool = False,
        pull: bool = False,
        push: bool = False,
        metadata_file: str | os.PathLike[str] | None = None,
        progress: Literal["auto", "plain", "tty"] = "auto",
        set: Mapping[str, str] | None = None,
    ) -> xm.SequentialArgs:
        files = files
        if files is None:
            files = []
        if not isinstance(files, collections.abc.Sequence):
            files = [files]

        targets = targets
        if targets is None:
            targets = []
        elif isinstance(targets, str):
            targets = [targets]
        assert isinstance(targets, collections.abc.Sequence)

        return xm.merge_args(
            ["buildx", "bake"],
            [f"--progress={progress}"],
            [f"--builder={builder}"] if builder else [],
            [f"--metadata-file={metadata_file}"] if metadata_file else [],
            ["--print"] if print else [],
            ["--push"] if push else [],
            ["--pull"] if pull else [],
            ["--load"] if load else [],
            ["--no-cache"] if not cache else [],
            [f"--file={file}" for file in files],
            [f"--set={key}={value}" for key, value in set.items()] if set else [],
            targets,
        )

    def bake(
        self,
        *,
        targets: Sequence[IndexedContainer[xm.Packageable]],
    ) -> list[IndexedContainer[RemoteImage]]:
        executors_by_executables = packaging_utils.collect_executors_by_executable(targets)
        for executable, executors in executors_by_executables.items():
            assert isinstance(
                executable, Dockerfile
            ), "All executables must be Dockerfiles when building Docker images."
            assert all(
                isinstance(executor, SlurmSpec) and executor.tag for executor in executors
            ), "All executors must be SlurmSpecs with tags when building Docker images."

        with tempfile.TemporaryDirectory() as tempdir:
            hcl_file = pathlib.Path(tempdir) / "docker-bake.hcl"
            metadata_file = pathlib.Path(tempdir) / "metadata.json"

            # Write HCL and bake it
            # TODO(jfarebro): Need a better way to hash the executables
            hcl = self._bake_template.render(
                executables=executors_by_executables,
                hash=_hash_digest,
            )
            hcl_file.write_text(hcl)
            logger.debug(hcl)

            try:
                bake_command = xm.merge_args(
                    self._client_call,
                    self._bake_args(
                        targets=list(
                            set([_hash_digest(target.value.executable_spec) for target in targets])
                        ),
                        files=[hcl_file],
                        metadata_file=metadata_file,
                        pull=False,
                        push=True,
                    ),
                )
                packaging_utils.run_command(bake_command.to_list(), tty=True, check=True)
            except Exception as ex:
                raise RuntimeError(f"Failed to build Dockerfiles: {ex}") from ex
            else:
                metadata = json.loads(metadata_file.read_text())

        images = []
        for target in targets:
            assert isinstance(target.value.executable_spec, Dockerfile)
            assert isinstance(target.value.executor_spec, SlurmSpec)
            assert target.value.executor_spec.tag

            executable_metadata = metadata[_hash_digest(target.value.executable_spec)]
            uri = ImageURI(target.value.executor_spec.tag).with_digest(
                executable_metadata["containerimage.digest"]
            )

            images.append(
                dataclasses.replace(
                    target,
                    value=RemoteImage(  # type: ignore
                        image=str(uri),
                        workdir=target.value.executable_spec.workdir,
                        args=target.value.args,
                        env_vars=target.value.env_vars,
                        credentials=self.credentials(uri.domain),
                    ),
                )
            )

        return images


@functools.cache
def docker_client() -> DockerClient:
    return DockerClient()


@registry.register(Dockerfile)
def _(
    targets: Sequence[IndexedContainer[xm.Packageable]],
) -> list[IndexedContainer[RemoteImage]]:
    return docker_client().bake(targets=targets)


@registry.register(DockerImage)
def _(
    targets: Sequence[IndexedContainer[xm.Packageable]],
) -> list[IndexedContainer[RemoteImage]]:
    """Build Docker images, this is essentially a passthrough."""
    images = []
    client = docker_client()
    for target in targets:
        assert isinstance(target.value.executable_spec, DockerImage)
        assert isinstance(target.value.executor_spec, SlurmSpec)
        if target.value.executor_spec.tag is not None:
            raise ValueError(
                "Executable `DockerImage` should not be tagged via `SlurmSpec`. "
                "The image URI is provided by the `DockerImage` itself."
            )

        uri = ImageURI(target.value.executable_spec.image)
        images.append(
            dataclasses.replace(
                target,
                value=RemoteImage(  # type: ignore
                    image=str(uri),
                    workdir=target.value.executable_spec.workdir,
                    args=target.value.args,
                    env_vars=target.value.env_vars,
                    credentials=client.credentials(hostname=uri.domain),
                ),
            )
        )

    return images
