import pathlib
import socket
import time
from typing import Iterator
from unittest.mock import PropertyMock, patch

import pytest
from testcontainers.compose import DockerCompose

from xm_slurm import config


def wait_for_ssh_server(host: str, port: int, *, timeout: float = 180.0) -> None:
    start_time = time.monotonic()
    while time.monotonic() - start_time < timeout:
        try:
            # Try to create a socket and connect to the specified host and port
            with socket.create_connection((host, port)) as sock:
                # Send a newline to prompt the SSH server to respond with its version
                sock.sendall(b"\n")
                # Wait to receive the SSH protocol version string
                response = sock.recv(1024).decode("utf-8")

                # Check if the response contains the SSH version string
                if response.startswith("SSH-"):
                    return

        except (ConnectionRefusedError, ConnectionResetError, socket.timeout):
            # If the connection is refused or times out, wait for a while and try again
            time.sleep(1)

    raise TimeoutError(f"Failed to connect to SSH server at {host}:{port} after {timeout} seconds")


@pytest.fixture(scope="session")
def cluster_config() -> Iterator[config.SlurmClusterConfig]:
    slurmdir = pathlib.Path(__file__).parent / "fixtures" / "slurm"
    cluster = DockerCompose(slurmdir, build=True)
    cluster.start()

    login_host, login_port = cluster.get_service_host_and_port("slurm-login")
    assert login_host is not None, "Failed to get login host"
    assert login_port is not None, "Failed to get login port"
    login_port = int(login_port)

    # Wait until the SSH server is online
    wait_for_ssh_server(login_host, login_port)

    login_host_pk_alg, login_host_pk = (slurmdir / "host_ed25519.pub").read_text().split()

    test_config = config.SlurmClusterConfig(
        name="test-cluster",
        host=login_host,
        host_public_key=config.PublicKey(algorithm=login_host_pk_alg, key=login_host_pk),
        port=login_port,
        user="root",
        runtime=config.ContainerRuntime.PODMAN,
    )

    # Monkey patch the private key as an absolute path
    ssh_config = test_config.ssh_config
    ssh_config._options["IdentityFile"] = [(slurmdir / "id_ed25519").resolve().as_posix()]

    with patch.object(
        config.SlurmClusterConfig, "ssh_config", new_callable=PropertyMock
    ) as mock_ssh_config:
        mock_ssh_config.return_value = ssh_config

        yield test_config

    cluster.stop()
