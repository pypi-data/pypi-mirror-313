from ..processing.padding_opencl import *
from ..utils import deprecation_warning

deprecation_warning(
    "nabu.opencl.padding has been moved to nabu.processing.padding_opencl", do_print=True, func_name="padding_opencl"
)
