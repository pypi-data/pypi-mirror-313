from nabu.processing.kernel_base import KernelBase
from ..utils import deprecated_class

KernelBase = deprecated_class("KernelBase has been moved to nabu.processing", do_print=True)(KernelBase)
