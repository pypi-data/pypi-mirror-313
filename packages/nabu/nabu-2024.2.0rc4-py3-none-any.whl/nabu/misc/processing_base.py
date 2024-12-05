from nabu.processing.processing_base import ProcessingBase
from ..utils import deprecated_class

ProcessingBase = deprecated_class("ProcessingBase has been moved to nabu.processing", do_print=True)(ProcessingBase)
