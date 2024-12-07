import dataclasses
import enum
import functools
import getpass
import json
import os
import pathlib
from typing import Callable, Literal, Mapping, NamedTuple

import asyncssh
from xmanager import xm

from xm_slurm import constants


class ContainerRuntime(enum.Enum):
    """The container engine to use."""

    SINGULARITY = enum.auto()
    APPTAINER = enum.auto()
    DOCKER = enum.auto()
    PODMAN = enum.auto()

    @classmethod
    def from_string(
        cls, runtime: Literal["singularity", "apptainer", "docker", "podman"]
    ) -> "ContainerRuntime":
        return {
            "singularity": cls.SINGULARITY,
            "apptainer": cls.APPTAINER,
            "docker": cls.DOCKER,
            "podman": cls.PODMAN,
        }[runtime]

    def __str__(self):
        if self is self.SINGULARITY:
            return "singularity"
        elif self is self.APPTAINER:
            return "apptainer"
        elif self is self.DOCKER:
            return "docker"
        elif self is self.PODMAN:
            return "podman"
        else:
            raise NotImplementedError


class PublicKey(NamedTuple):
    algorithm: str
    key: str


@dataclasses.dataclass
class SlurmSSHConfig:
    host: str
    host_public_key: PublicKey | None = None
    user: str | None = None
    port: int | None = None

    @functools.cached_property
    def known_hosts(self) -> asyncssh.SSHKnownHosts | None:
        if self.host_public_key is None:
            return None

        return asyncssh.import_known_hosts(
            f"[{self.host}]:{self.port} {self.host_public_key.algorithm} {self.host_public_key.key}"
        )

    @functools.cached_property
    def config(self) -> asyncssh.config.SSHConfig:
        ssh_config_paths = []
        if (ssh_config := pathlib.Path.home() / ".ssh" / "config").exists():
            ssh_config_paths.append(ssh_config)
        if (xm_ssh_config_var := os.environ.get("XM_SLURM_SSH_CONFIG")) and (
            xm_ssh_config := pathlib.Path(xm_ssh_config_var).expanduser()
        ).exists():
            ssh_config_paths.append(xm_ssh_config)

        config = asyncssh.config.SSHClientConfig.load(
            None,
            ssh_config_paths,
            False,
            getpass.getuser(),
            self.user or (),
            self.host,
            self.port or (),
        )
        if config.get("Hostname") is None and (
            constants.DOMAIN_NAME_REGEX.match(self.host)
            or constants.IPV4_REGEX.match(self.host)
            or constants.IPV6_REGEX.match(self.host)
        ):
            config._options["Hostname"] = self.host
        elif config.get("Hostname") is None:
            raise RuntimeError(
                f"Failed to parse hostname from host `{self.host}` using "
                f"SSH configs: {', '.join(map(str, ssh_config_paths))} and "
                f"provided hostname `{self.host}` isn't a valid domain name "
                "or IPv{4,6} address."
            )

        if config.get("User") is None:
            raise RuntimeError(
                f"We could not find a user for the cluster configuration: `{self.host}`. "
                "No user was specified in the configuration and we could not parse "
                f"any users for host `{config.get('Hostname')}` from the SSH configs: "
                f"{', '.join(map(lambda h: f'`{h}`', ssh_config_paths))}. Please either specify a user "
                "in the configuration or add a user to your SSH configuration under the block "
                f"`Host {config.get('Hostname')}`."
            )

        return config

    @functools.cached_property
    def connection_options(self) -> asyncssh.SSHClientConnectionOptions:
        options = asyncssh.SSHClientConnectionOptions(config=None)
        options.prepare(last_config=self.config, known_hosts=self.known_hosts)
        return options

    def serialize(self):
        return json.dumps({
            "host": self.host,
            "host_public_key": self.host_public_key,
            "user": self.user,
            "port": self.port,
        })

    @classmethod
    def deserialize(cls, data):
        data = json.loads(data)
        return cls(
            host=data["host"],
            host_public_key=PublicKey(*data["host_public_key"])
            if data["host_public_key"]
            else None,
            user=data["user"],
            port=data["port"],
        )

    def __hash__(self):
        return hash((type(self), self.host, self.host_public_key, self.user, self.port))


@dataclasses.dataclass(frozen=True, kw_only=True)
class SlurmClusterConfig:
    name: str

    ssh: SlurmSSHConfig

    # Job submission directory
    cwd: str | None = None

    # Additional scripting
    prolog: str | None = None
    epilog: str | None = None

    # Job scheduling
    account: str | None = None
    partition: str | None = None
    qos: str | None = None

    # If true, a reverse proxy is initiated via the submission host.
    proxy: Literal["submission-host"] | str | None = None

    runtime: ContainerRuntime

    # Environment variables
    environment: Mapping[str, str] = dataclasses.field(default_factory=dict)

    # Mounts
    mounts: Mapping[os.PathLike[str] | str, os.PathLike[str] | str] = dataclasses.field(
        default_factory=dict
    )

    # Resource mapping
    resources: Mapping["xm_slurm.ResourceType", str] = dataclasses.field(default_factory=dict)  # type: ignore # noqa: F821

    features: Mapping["xm_slurm.FeatureType", str] = dataclasses.field(default_factory=dict)  # type: ignore # noqa: F821

    # Function to validate the Slurm executor config
    validate: Callable[[xm.Job], None] | None = None

    def __post_init__(self) -> None:
        for src, dst in self.mounts.items():
            if not isinstance(src, (str, os.PathLike)):
                raise TypeError(
                    f"Mount source must be a string or path-like object, not {type(src)}"
                )
            if not isinstance(dst, (str, os.PathLike)):
                raise TypeError(
                    f"Mount destination must be a string or path-like object, not {type(dst)}"
                )

            if not pathlib.Path(src).is_absolute():
                raise ValueError(f"Mount source must be an absolute path: {src}")
            if not pathlib.Path(dst).is_absolute():
                raise ValueError(f"Mount destination must be an absolute path: {dst}")

    def __hash__(self):
        return hash((
            type(self),
            self.ssh,
            self.cwd,
            self.prolog,
            self.epilog,
            self.account,
            self.partition,
            self.qos,
            self.proxy,
            self.runtime,
            frozenset(self.environment.items()),
        ))
