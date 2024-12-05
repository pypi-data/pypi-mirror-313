from ..processing.medfilt_cuda import *
from ..utils import deprecation_warning

deprecation_warning(
    "nabu.cuda.medfilt has been moved to nabu.processing.medfilt_cuda", do_print=True, func_name="medfilt_cuda"
)
