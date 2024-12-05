from ..processing.rotation_cuda import *
from ..utils import deprecation_warning

deprecation_warning(
    "nabu.misc.rotation_cuda has been moved to nabu.processing.rotation_cuda", do_print=True, func_name="rotation_cuda"
)
