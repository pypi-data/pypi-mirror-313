# First register our built-in packaging methods
import xm_slurm.packaging.docker  # noqa: F401
from xm_slurm.packaging import registry, router

package = router.package
register = registry.register

__all__ = ["package", "register"]
