from ..processing.fft_cuda import *
from ..utils import deprecation_warning

deprecation_warning("nabu.cuda.fft has been moved to nabu.processing.fft_cuda", do_print=True, func_name="fft_cuda")
