import numpy as np
import time
from datetime import datetime, timedelta
from absl import app
from absl import flags

FLAGS = flags.FLAGS
flags.DEFINE_integer("time", 600, "The amount of time to run in seconds")


def main(argv):
    del argv  # Unused.

    print("Hello world!")
    print(f"numpy version: {np.__version__}")

    end_time = datetime.now() + timedelta(seconds=FLAGS.time)

    while datetime.now() < end_time:
        remaining_time = end_time - datetime.now()
        minutes, seconds = divmod(remaining_time.seconds, 60)
        print(f"Remaining time: {minutes:02d}:{seconds:02d}")
        time.sleep(10)

    print("Time's up!")


if __name__ == "__main__":
    app.run(main)
