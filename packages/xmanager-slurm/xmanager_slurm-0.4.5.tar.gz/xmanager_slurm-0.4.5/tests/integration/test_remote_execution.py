import pytest
from xmanager import xm
from xmanager.xm import utils as xm_utils

from xm_slurm import config, execution


@pytest.mark.asyncio
async def test_ssh_connection(cluster_config: config.SlurmClusterConfig):
    client = execution.Client()
    await client.connection(cluster_config.ssh_connection_options)


@pytest.mark.asyncio
async def test_xm_slurm_setup(cluster_config: config.SlurmClusterConfig) -> None:
    client = execution.Client()
    conn = await client.connection(cluster_config.ssh_connection_options)

    async with conn.start_sftp_client() as sftp_client:
        await sftp_client.isdir(".local/state/xm-slurm")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command,expected",
    [
        ("echo 'Hello, world!'", "Hello, world!\n"),
        (["echo", "Hello, world!"], "Hello, world!\n"),
        (
            xm.SequentialArgs.from_collection(["echo", "Hello, world!"]),
            "'Hello, world!'\n",
        ),
        (
            xm.SequentialArgs.from_collection(["echo", xm_utils.ShellSafeArg("Hello, world!")]),
            "Hello, world!\n",
        ),
    ],
)
async def test_run_command(cluster_config: config.SlurmClusterConfig, command: str, expected: str):
    client = execution.Client()
    result = await client.run(cluster_config.ssh_connection_options, command)
    assert result.returncode == 0
    assert result.stdout == expected
    assert result.stderr == ""
