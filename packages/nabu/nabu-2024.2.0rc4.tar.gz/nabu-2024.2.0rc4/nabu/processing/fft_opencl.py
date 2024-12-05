from multiprocessing import get_context
from multiprocessing.pool import Pool
from .fft_base import _BaseVKFFT
from ..opencl.processing import OpenCLProcessing

try:
    from pyvkfft.opencl import VkFFTApp as vk_clfft

    __has_vkfft__ = True
except (ImportError, OSError):
    __has_vkfft__ = False
    vk_clfft = None


class VKCLFFT(_BaseVKFFT):
    """
    OpenCL FFT, using VKFFT backend
    """

    implem = "vkfft"
    backend = "opencl"
    ProcessingCls = OpenCLProcessing
    vkffs_cls = vk_clfft

    def _init_backend(self, backend_options):
        super()._init_backend(backend_options)
        self._vkfft_other_init_kwargs = {"queue": self.processing.queue}


def _has_vkfft(x):
    # should be run from within a Process
    try:
        from nabu.processing.fft_opencl import VKCLFFT, __has_vkfft__

        if not __has_vkfft__:
            return False
        vk = VKCLFFT((16,), "f")
        avail = True
    except (RuntimeError, OSError):
        avail = False
    return avail


def has_vkfft(safe=True):
    """
    Determine whether pyvkfft is available.
    This function cannot be tested from a notebook/console, a proper entry point has to be created (if __name__ == "__main__").
    """
    if not safe:
        return _has_vkfft(None)
    ctx = get_context("spawn")
    with Pool(1, context=ctx) as p:
        v = p.map(_has_vkfft, [1])[0]
    return v
