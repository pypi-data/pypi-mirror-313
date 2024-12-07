import pathlib

import numpy as np
from absl import app, flags

OUTPUT_FILE = flags.DEFINE_string("output_file", "result.npy", "Output file path")
SEED = flags.DEFINE_integer("seed", 0, "Random seed")


def main(_):
    np.random.seed(SEED.value)

    pathlib.Path(OUTPUT_FILE.value).parent.mkdir(parents=True, exist_ok=True)
    result = np.random.random((32,))
    np.save(OUTPUT_FILE.value, result)


if __name__ == "__main__":
    app.run(main)
