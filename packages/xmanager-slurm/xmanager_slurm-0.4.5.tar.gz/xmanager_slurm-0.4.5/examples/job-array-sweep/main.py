import argparse
import pathlib

import numpy as np


def main(workdir: pathlib.Path, scale: float):
    rng = np.random.default_rng()

    s = rng.random() * scale

    with (workdir / "scale.npz").open("wb") as fp:
        np.savez(fp, s)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--workdir", type=pathlib.Path, default=pathlib.Path("."))
    parser.add_argument("--scale", type=float, default=1.0)
    args = parser.parse_args()

    args.workdir.mkdir(parents=True, exist_ok=True)

    main(args.workdir, args.scale)
