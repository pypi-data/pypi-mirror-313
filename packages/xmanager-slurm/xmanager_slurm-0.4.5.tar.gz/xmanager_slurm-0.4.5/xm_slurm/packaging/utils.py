import collections
import logging
import os
import pathlib
import pty
import re
import select
import shutil
import subprocess
from typing import ParamSpec, Sequence, TypeVar

from xmanager import xm

from xm_slurm.packaging.registry import IndexedContainer

T = TypeVar("T")
P = ParamSpec("P")
ReturnT = TypeVar("ReturnT")

logger = logging.getLogger(__name__)


def collect_executors_by_executable(
    targets: Sequence[IndexedContainer[xm.Packageable]],
) -> dict[xm.ExecutableSpec, set[xm.ExecutorSpec]]:
    executors_by_executable = collections.defaultdict(set)
    for target in targets:
        executors_by_executable[target.value.executable_spec].add(target.value.executor_spec)
    return executors_by_executable


# Cursor commands to filter out from the command data stream
_CURSOR_ESCAPE_SEQUENCES_REGEX = re.compile(
    rb"\x1b\[\?25[hl]"  # Matches cursor show/hide commands (CSI ?25h and CSI ?25l)
    rb"|\x1b\[[0-9;]*[Hf]"  # Matches cursor position commands (CSI n;mH and CSI n;mf)
    rb"|\x1b\[s"  # Matches cursor save position (CSI s)
    rb"|\x1b\[u"  # Matches cursor restore position (CSI u)
    rb"|\x1b\[2J"  # Matches clear screen (CSI 2J)
    rb"|\x1b\[K"  # Matches clear line (CSI K)
)


def run_command(
    args: Sequence[str] | xm.SequentialArgs,
    env: dict[str, str] | None = None,
    tty: bool = False,
    cwd: str | os.PathLike[str] | None = None,
    check: bool = False,
    return_stdout: bool = False,
    return_stderr: bool = False,
) -> subprocess.CompletedProcess[str]:
    if isinstance(args, xm.SequentialArgs):
        args = args.to_list()
    args = list(args)

    executable = shutil.which(args[0])
    if not executable:
        raise RuntimeError(f"Couldn't find executable {args[0]}")
    executable = pathlib.Path(executable)

    subprocess_env = os.environ.copy() | (env if env else {})
    if executable.name == "docker" and args[1] == "buildx":
        subprocess_env |= {"DOCKER_CLI_EXPERIMENTAL": "enabled"}

    logger.debug(f"env: {subprocess_env}")
    logger.debug(f"command: {' '.join(args)}")

    stdout_master, stdout_slave = pty.openpty()
    stderr_master, stderr_slave = pty.openpty()

    stdout_data, stderr_data = b"", b""
    with subprocess.Popen(
        executable=executable,
        args=args,
        shell=False,
        text=True,
        bufsize=0,
        stdout=stdout_slave,
        stderr=stderr_slave,
        start_new_session=True,
        close_fds=True,
        cwd=cwd,
        env=subprocess_env,
    ) as process:
        os.close(stdout_slave)
        os.close(stderr_slave)

        fds = [stdout_master, stderr_master]
        while fds:
            rlist, _, _ = select.select(fds, [], [])
            for fd in rlist:
                try:
                    data = os.read(fd, 1024)
                except OSError:
                    data = None

                if not data:
                    os.close(fd)
                    fds.remove(fd)
                    continue

                data = _CURSOR_ESCAPE_SEQUENCES_REGEX.sub(b"", data)

                if fd == stdout_master:
                    if return_stdout:
                        stdout_data += data
                    if tty:
                        os.write(pty.STDOUT_FILENO, data)
                elif fd == stderr_master:
                    if return_stderr:
                        stderr_data += data
                    if tty:
                        os.write(pty.STDERR_FILENO, data)
                else:
                    raise RuntimeError("Unexpected file descriptor")

    stdout = stdout_data.decode(errors="replace") if stdout_data else ""
    stderr = stderr_data.decode(errors="replace") if stderr_data else ""

    retcode = process.poll()
    assert retcode is not None

    if check and retcode:
        raise subprocess.CalledProcessError(retcode, process.args)
    return subprocess.CompletedProcess(
        process.args,
        retcode,
        stdout=stdout,
        stderr=stderr,
    )
