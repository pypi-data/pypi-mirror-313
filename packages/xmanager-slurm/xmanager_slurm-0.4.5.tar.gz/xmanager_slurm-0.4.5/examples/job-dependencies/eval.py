import numpy as np
from absl import app, flags

INPUT_FILE = flags.DEFINE_string("input_file", "result.npy", "Input file path")


def main(_):
    result = np.load(INPUT_FILE.value)
    print(f"Received result: {result}")


if __name__ == "__main__":
    app.run(main)
