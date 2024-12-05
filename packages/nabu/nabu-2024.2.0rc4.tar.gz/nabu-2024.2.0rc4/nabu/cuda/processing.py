from ..utils import MissingComponentError
from ..processing.processing_base import ProcessingBase
from .utils import get_cuda_context, __has_pycuda__

if __has_pycuda__:
    import pycuda.driver as cuda
    import pycuda.gpuarray as garray
    from ..cuda.kernel import CudaKernel

    dev_attrs = cuda.device_attribute
    GPUArray = garray.GPUArray
    from pycuda.tools import dtype_to_ctype
else:
    GPUArray = MissingComponentError("pycuda")
    dtype_to_ctype = MissingComponentError("pycuda")


# NB: we must detach from a context before creating another context
class CudaProcessing(ProcessingBase):
    array_class = GPUArray if __has_pycuda__ else None
    dtype_to_ctype = dtype_to_ctype

    def __init__(self, device_id=None, ctx=None, stream=None, cleanup_at_exit=True):
        """
        Initialie a CudaProcessing instance.

        CudaProcessing is a base class for all CUDA-based processings.
        This class provides utilities for context/device management, and
        arrays allocation.

        Parameters
        ----------
        device_id: int, optional
            ID of the cuda device to use (those of the `nvidia-smi` command).
            Ignored if ctx is not None.
        ctx: pycuda.driver.Context, optional
            Existing context to use. If provided, do not create a new context.
        stream: pycudacuda.driver.Stream, optional
            Cuda stream. If not provided, will use the default stream
        cleanup_at_exit: bool, optional
            Whether to clean-up the context at exit.
            Ignored if ctx is not None.
        """
        super().__init__()
        if ctx is None:
            self.ctx = get_cuda_context(device_id=device_id, cleanup_at_exit=cleanup_at_exit)
        else:
            self.ctx = ctx
        self.stream = stream
        self.device = self.ctx.get_device()
        self.device_name = self.device.name()
        self.device_id = self.device.get_attribute(dev_attrs.MULTI_GPU_BOARD_GROUP_ID)  # pylint: disable=E0606

    def push_context(self):
        self.ctx.push()
        return self.ctx

    def pop_context(self):
        self.ctx.pop()

    def _allocate_array_mem(self, shape, dtype):
        return garray.zeros(shape, dtype)

    def kernel(
        self, kernel_name, filename=None, src=None, signature=None, texrefs=None, automation_params=None, **build_kwargs
    ):
        return CudaKernel(  # pylint: disable=E0606
            kernel_name,
            filename=filename,
            src=src,
            signature=signature,
            texrefs=texrefs,
            automation_params=automation_params,
            **build_kwargs,
        )
