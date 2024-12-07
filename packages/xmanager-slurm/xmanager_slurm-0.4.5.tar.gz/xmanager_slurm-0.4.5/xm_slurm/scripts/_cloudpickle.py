import base64
import logging
import zlib

import cloudpickle
from absl import app, flags
from xmanager import xm

CLOUDPICKLED_FN = flags.DEFINE_string(
    "cloudpickled_fn", None, "Base64 encoded cloudpickled function", required=True
)

logger = logging.getLogger(__name__)


@xm.run_in_asyncio_loop
async def main(argv):
    del argv

    logger.info("Loading cloudpickled function...")
    cloudpickled_fn = zlib.decompress(base64.urlsafe_b64decode(CLOUDPICKLED_FN.value))
    function = cloudpickle.loads(cloudpickled_fn)
    logger.info("Running cloudpickled function...")
    await function()


if __name__ == "__main__":
    app.run(main)
