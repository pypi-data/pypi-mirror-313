import argparse
import sys

from xmanager import xm

import xm_slurm
from xm_slurm.console import console


async def logs(
    experiment_id: int,
    *,
    wid: int | None,
    identity: str | None,
    follow: bool = True,
    num_lines: int = 10,
    block_size: int = 1024,
):
    xp = xm_slurm.get_experiment(experiment_id)

    if wid is not None:
        wu = xp.work_units()[wid]
    elif identity is not None:
        wu = xp._get_work_unit_by_identity(identity)
        if wu is None:
            console.print(f"[red]Work Unit with identity {identity} not found.[/red]")
            sys.exit(1)
    else:
        raise ValueError("Must specify either wid or identity.")
    assert wu is not None

    async for log in wu.logs(num_lines=num_lines, block_size=block_size, wait=True, follow=follow):
        console.print(log, end="\n")


@xm.run_in_asyncio_loop
async def main():
    parser = argparse.ArgumentParser(description="XManager.")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    logs_parser = subparsers.add_parser("logs", help="Display logs for a specific experiment.")
    logs_parser.add_argument("xid", type=int, help="Experiment ID.")

    # Create a mutually exclusive group for wid and identity
    group = logs_parser.add_mutually_exclusive_group()
    group.add_argument("--wid", type=int, help="Work Unit ID.")
    group.add_argument("--identity", type=str, help="Work Unit identity.")

    logs_parser.add_argument(
        "-n",
        "--n-lines",
        type=int,
        default=50,
        help="Number of lines to display from the end of the log file.",
    )
    logs_parser.add_argument(
        "-f",
        "--follow",
        default=True,
        action="store_true",
        help="Follow the log file as it is updated.",
    )

    args = parser.parse_args()
    match args.subcommand:
        case "logs":
            await logs(
                args.xid,
                wid=args.wid,
                identity=args.identity,
                follow=args.follow,
                num_lines=args.n_lines,
            )


if __name__ == "__main__":
    main()  # type: ignore
