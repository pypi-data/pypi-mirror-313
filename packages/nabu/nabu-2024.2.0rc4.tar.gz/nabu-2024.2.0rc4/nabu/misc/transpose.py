from ..processing.transpose import *
from ..utils import deprecation_warning

deprecation_warning(
    "nabu.misc.transpose has been moved to nabu.processing.transpose", do_print=True, func_name="transpose"
)
