import dataclasses
import pathlib
import typing as tp

from xmanager import xm

from xm_slurm import constants
from xm_slurm.types import Descriptor


@dataclasses.dataclass(frozen=True, kw_only=True)
class Dockerfile(xm.ExecutableSpec):
    """A specification describing a Dockerfile to build.

    Args:
        dockerfile: The path to the Dockerfile.
        context: The path to the Docker context.
        target: The Docker build target.
        ssh: A list of docker SSH sockets/keys.
        build_args: Build arguments to docker.
        cache_from: Where to pull the BuildKit cache from. See `--cache-from` in `docker build`.
        workdir: The working directory in container.
        labels: The container labels.
        platforms: The target platform.
    """

    # Dockerfile
    dockerfile: pathlib.Path
    # Docker context
    context: pathlib.Path

    # Docker build target
    target: str | None = None

    # SSH sockets/keys for the docker build step.
    ssh: tp.Sequence[str] = dataclasses.field(default_factory=list)

    # Build arguments to docker
    build_args: tp.Mapping[str, str] = dataclasses.field(default_factory=dict)

    # --cache-from field in BuildKit
    cache_from: tp.Sequence[str] = dataclasses.field(default_factory=list)

    # Working directory in container
    workdir: pathlib.Path | None = None

    # Container labels
    labels: tp.Mapping[str, str] = dataclasses.field(default_factory=dict)

    # Target platform
    platforms: tp.Sequence[str] = dataclasses.field(default_factory=lambda: ["linux/amd64"])

    @property
    def name(self) -> str:
        name = self.dockerfile.stem
        if self.target is not None:
            name = f"{name}-{self.target}"
        return name

    def __hash__(self) -> int:
        return hash((
            type(self),
            self.dockerfile,
            self.context,
            self.target,
            tuple(sorted(self.ssh)),
            tuple(sorted(self.build_args.items())),
            tuple(sorted(self.cache_from)),
            self.workdir,
            tuple(sorted(self.labels.items())),
            tuple(sorted(self.platforms)),
        ))


@dataclasses.dataclass(frozen=True, kw_only=True)
class DockerImage(xm.ExecutableSpec):
    """A specification describing a pre-built Docker image.

    Args:
        image: The remote image URI.
        workdir: The working directory in container.

    """

    image: str

    # Working directory in container
    workdir: pathlib.Path | None = None

    @property
    def name(self) -> str:
        return self.image

    def __hash__(self) -> int:
        return hash((type(self), self.image, self.workdir))


@dataclasses.dataclass
class ImageURI:
    image: dataclasses.InitVar[str]

    scheme: str | None = dataclasses.field(init=False, default=None)
    domain: str = dataclasses.field(init=False)
    path: str = dataclasses.field(init=False)
    tag: str | None = dataclasses.field(init=False, default=None)
    digest: str | None = dataclasses.field(init=False, default=None)

    def __post_init__(self, image: str):
        match = constants.IMAGE_URI_REGEX.match(image)
        if not match:
            raise ValueError(f"Invalid OCI image URI: {image}")
        groups = {k: v for k, v in match.groupdict().items() if v is not None}
        for k, v in groups.items():
            setattr(self, k, v)

        if self.tag is None and self.digest is None:
            self.tag = "latest"

    @property
    def locator(self) -> str:
        """Unique locator for this image.

        Locator will return the digest if it exists otherwise the tag format.
        If neither are present, it will raise an AssertionError.
        """
        if self.digest is not None:
            return f"@{self.digest}"
        assert self.tag is not None
        return f":{self.tag}"

    @property
    def url(self) -> str:
        """URL for this image without the locator."""
        return f"{self.origin}{self.path}"

    @property
    def origin(self) -> str:
        return f"{self.scheme}{self.domain}"

    def with_tag(self, tag: str) -> "ImageURI":
        self.tag = tag
        return self

    def with_digest(self, digest: str) -> "ImageURI":
        self.digest = digest
        return self

    def __str__(self) -> str:
        return self.format("{url}{locator}")

    def __hash__(self) -> int:
        return hash((
            type(self),
            self.scheme,
            self.domain,
            self.path,
            self.tag,
            self.digest,
        ))

    def format(self, format: str) -> str:
        fields = {k: v for k, v in dataclasses.asdict(self).items() if v is not None}
        fields |= {"locator": self.locator, "url": self.url}
        return format.format(**fields)


class ImageDescriptor(Descriptor[ImageURI, str | ImageURI]):
    def __set_name__(self, owner: type, name: str):
        del owner
        self.image = f"_{name}"

    def __get__(self, instance: object | None, owner: tp.Type[object] | None = None) -> ImageURI:
        del owner
        return getattr(instance, self.image)

    def __set__(self, instance: object, value: str | ImageURI):
        _setattr = object.__setattr__ if not hasattr(instance, self.image) else setattr
        if isinstance(value, str):
            value = ImageURI(value)
        _setattr(instance, self.image, value)


class RemoteRepositoryCredentials(tp.NamedTuple):
    username: str
    password: str


@dataclasses.dataclass(frozen=True, kw_only=True)  # type: ignore
class RemoteImage(xm.Executable):
    # Remote base image
    image: Descriptor[ImageURI, str | ImageURI] = ImageDescriptor()

    # Working directory in container
    workdir: pathlib.Path | None = None

    # Container arguments
    args: xm.SequentialArgs = dataclasses.field(default_factory=xm.SequentialArgs)
    # Container environment variables
    env_vars: tp.Mapping[str, str] = dataclasses.field(default_factory=dict)

    # Remote repository credentials
    credentials: RemoteRepositoryCredentials | None = None

    @property
    def name(self) -> str:  # type: ignore
        return str(self.image)

    def __hash__(self) -> int:
        return hash(
            (
                type(self),
                self.image,
                self.workdir,
                tuple(sorted(self.args.to_list())),
                tuple(sorted(self.env_vars.items())),
                self.credentials,
            ),
        )
