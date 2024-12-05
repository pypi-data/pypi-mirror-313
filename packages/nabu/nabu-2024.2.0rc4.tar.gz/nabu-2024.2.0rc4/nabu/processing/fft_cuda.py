import os
import warnings
from multiprocessing import get_context
from multiprocessing.pool import Pool
import numpy as np
from ..utils import check_supported
from .fft_base import _BaseFFT, _BaseVKFFT

try:
    from pyvkfft.cuda import VkFFTApp as vk_cufft

    __has_vkfft__ = True
except (ImportError, OSError):
    __has_vkfft__ = False
    vk_cufft = None
from ..cuda.processing import CudaProcessing

Plan = None
cu_fft = None
cu_ifft = None
__has_skcuda__ = None


def init_skcuda():
    # This needs to be done here, because scikit-cuda creates a Cuda context at import,
    # which can mess things up in some cases.
    # Ugly solution to an ugly problem.
    global __has_skcuda__, Plan, cu_fft, cu_ifft
    try:
        from skcuda.fft import Plan
        from skcuda.fft import fft as cu_fft
        from skcuda.fft import ifft as cu_ifft

        __has_skcuda__ = True
    except ImportError:
        __has_skcuda__ = False


class SKCUFFT(_BaseFFT):
    implem = "skcuda"
    backend = "cuda"
    ProcessingCls = CudaProcessing

    def _configure_batched_transform(self):
        if __has_skcuda__ is None:
            init_skcuda()
        if not (__has_skcuda__):
            raise ImportError("Please install pycuda and scikit-cuda to use the CUDA back-end")

        self.cufft_batch_size = 1
        self.cufft_shape = self.shape
        self._cufft_plan_kwargs = {}
        if (self.axes is not None) and (len(self.axes) < len(self.shape)):
            # In the easiest case, the transform is computed along the fastest dimensions:
            #  - 1D transforms of lines of 2D data
            #  - 2D transforms of images of 3D data (stacked along slow dim)
            #  - 1D transforms of 3D data along fastest dim
            # Otherwise, we have to configure cuda "advanced memory layout".
            data_ndims = len(self.shape)

            if data_ndims == 2:
                n_y, n_x = self.shape
                along_fast_dim = self.axes[0] == 1
                self.cufft_shape = n_x if along_fast_dim else n_y
                self.cufft_batch_size = n_y if along_fast_dim else n_x
                if not (along_fast_dim):
                    # Batched vertical 1D FFT on 2D data need advanced data layout
                    # http://docs.nvidia.com/cuda/cufft/#advanced-data-layout
                    self._cufft_plan_kwargs = {
                        "inembed": np.int32([0]),
                        "istride": n_x,
                        "idist": 1,
                        "onembed": np.int32([0]),
                        "ostride": n_x,
                        "odist": 1,
                    }

            if data_ndims == 3:
                # TODO/FIXME - the following work for C2C but not R2C ?!
                # fast_axes = [(1, 2), (2, 1), (2,)]
                fast_axes = [(2,)]
                if self.axes not in fast_axes:
                    raise NotImplementedError(
                        "With the CUDA backend, batched transform on 3D data is only supported along fastest dimensions"
                    )
                self.cufft_batch_size = self.shape[0]
                self.cufft_shape = self.shape[1:]
                if len(self.axes) == 1:
                    # 1D transform on 3D data: here only supported along fast dim, so batch_size is Nx*Ny
                    self.cufft_batch_size = np.prod(self.shape[:2])
                    self.cufft_shape = (self.shape[-1],)
                if len(self.cufft_shape) == 1:
                    self.cufft_shape = self.cufft_shape[0]

    def _configure_normalization(self, normalize):
        self.normalize = normalize
        if self.normalize == "ortho":
            # TODO
            raise NotImplementedError("Normalization mode 'ortho' is not implemented with CUDA backend yet.")
        self.cufft_scale_inverse = self.normalize == "rescale"

    def _compute_fft_plans(self):
        self.plan_forward = Plan(  # pylint: disable = E1102
            self.cufft_shape,
            self.dtype,
            self.dtype_out,
            batch=self.cufft_batch_size,
            stream=self.processing.stream,
            **self._cufft_plan_kwargs,
            # cufft extensible plan API is only supported after 0.5.1
            # (commit 65288d28ca0b93e1234133f8d460dc6becb65121)
            # but there is still no official 0.5.2
            # ~ auto_allocate=True # cufft extensible plan API
        )
        self.plan_inverse = Plan(  # pylint: disable = E1102
            self.cufft_shape,  # not shape_out
            self.dtype_out,
            self.dtype,
            batch=self.cufft_batch_size,
            stream=self.processing.stream,
            **self._cufft_plan_kwargs,
            # cufft extensible plan API is only supported after 0.5.1
            # (commit 65288d28ca0b93e1234133f8d460dc6becb65121)
            # but there is still no official 0.5.2
            # ~ auto_allocate=True
        )

    def fft(self, array, output=None):
        if output is None:
            output = self.output_fft = self.processing.allocate_array(
                "output_fft", self.shape_out, dtype=self.dtype_out
            )
        cu_fft(array, output, self.plan_forward, scale=False)  # pylint: disable = E1102
        return output

    def ifft(self, array, output=None):
        if output is None:
            output = self.output_ifft = self.processing.allocate_array("output_ifft", self.shape, dtype=self.dtype)
        cu_ifft(  # pylint: disable = E1102
            array,
            output,
            self.plan_inverse,
            scale=self.cufft_scale_inverse,
        )
        return output


class VKCUFFT(_BaseVKFFT):
    """
    Cuda FFT, using VKFFT backend
    """

    implem = "vkfft"
    backend = "cuda"
    ProcessingCls = CudaProcessing
    vkffs_cls = vk_cufft

    def _init_backend(self, backend_options):
        super()._init_backend(backend_options)
        self._vkfft_other_init_kwargs = {"stream": self.processing.stream}


def _has_vkfft(x):
    # should be run from within a Process
    try:
        from nabu.processing.fft_cuda import VKCUFFT, __has_vkfft__

        if not __has_vkfft__:
            return False
        vk = VKCUFFT((16,), "f")
        avail = True
    except (ImportError, RuntimeError, OSError, NameError):
        avail = False
    return avail


def has_vkfft(safe=True):
    """
    Determine whether pyvkfft is available.
    For Cuda GPUs, vkfft relies on nvrtc which supports a narrow range of Cuda devices.
    Unfortunately, it's not possible to determine whether vkfft is available before creating a Cuda context.
    So we create a process (from scratch, i.e no fork), do the test within, and exit.
    This function cannot be tested from a notebook/console, a proper entry point has to be created (if __name__ == "__main__").
    """
    if not safe:
        return _has_vkfft(None)
    ctx = get_context("spawn")
    with Pool(1, context=ctx) as p:
        v = p.map(_has_vkfft, [1])[0]
    return v


def _has_skfft(x):
    # should be run from within a Process
    try:
        from nabu.processing.fft_cuda import SKCUFFT

        sk = SKCUFFT((16,), "f")
        avail = True
    except (ImportError, RuntimeError, OSError, NameError):
        avail = False
    return avail


def has_skcuda(safe=True):
    """
    Determine whether scikit-cuda/CUFFT is available.
    Currently, scikit-cuda will create a Cuda context for Cublas, which can mess up the current execution.
    Do it in a separate thread.
    """
    if not safe:
        return _has_skfft(None)
    ctx = get_context("spawn")
    with Pool(1, context=ctx) as p:
        v = p.map(_has_skfft, [1])[0]
    return v


def get_fft_class(backend="vkfft"):
    backends = {
        "scikit-cuda": SKCUFFT,
        "skcuda": SKCUFFT,
        "cufft": SKCUFFT,
        "scikit": SKCUFFT,
        "vkfft": VKCUFFT,
        "pyvkfft": VKCUFFT,
    }

    def get_fft_cls(asked_fft_backend):
        asked_fft_backend = asked_fft_backend.lower()
        check_supported(asked_fft_backend, list(backends.keys()), "Cuda FFT backend name")
        return backends[asked_fft_backend]

    asked_fft_backend_env = os.environ.get("NABU_FFT_BACKEND", "")
    if asked_fft_backend_env != "":
        return get_fft_cls(asked_fft_backend_env)

    avail_fft_implems = get_available_fft_implems()
    if len(avail_fft_implems) == 0:
        raise RuntimeError("Could not any Cuda FFT implementation. Please install either scikit-cuda or pyvkfft")
    if backend not in avail_fft_implems:
        warnings.warn("Could not get FFT backend '%s'" % backend, RuntimeWarning)
        backend = avail_fft_implems[0]

    return get_fft_cls(backend)


def get_available_fft_implems():
    avail_implems = []
    if has_vkfft(safe=True):
        avail_implems.append("vkfft")
    if has_skcuda(safe=True):
        avail_implems.append("skcuda")
    return avail_implems
