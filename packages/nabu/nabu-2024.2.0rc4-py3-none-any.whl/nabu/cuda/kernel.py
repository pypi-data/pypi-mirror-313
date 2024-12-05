import pycuda.gpuarray as garray
from pycuda.compiler import SourceModule
from ..processing.kernel_base import KernelBase
from ..utils import catch_warnings  # TODO use warnings.catch_warnings once python < 3.11 is dropped


class CudaKernel(KernelBase):
    """
    Helper class that wraps CUDA kernel through pycuda SourceModule.

    Parameters
    -----------
    kernel_name: str
        Name of the CUDA kernel.
    filename: str, optional
        Path to the file name containing kernels definitions
    src: str, optional
        Source code of kernels definitions
    signature: str, optional
        Signature of kernel function. If provided, pycuda will not guess the types
        of kernel arguments, making the calls slightly faster.
        For example, a function acting on two pointers, an integer and a float32
        has the signature "PPif".
    texrefs: list, optional
        List of texture references, if any
    automation_params: dict, optional
        Automation parameters, see below
    sourcemodule_kwargs: optional
        Extra arguments to provide to pycuda.compiler.SourceModule(),

    """

    def __init__(
        self,
        kernel_name,
        filename=None,
        src=None,
        signature=None,
        texrefs=None,
        automation_params=None,
        silent_compilation_warnings=False,
        **sourcemodule_kwargs,
    ):
        super().__init__(
            kernel_name,
            filename=filename,
            src=src,
            automation_params=automation_params,
            silent_compilation_warnings=silent_compilation_warnings,
        )
        self.compile_kernel_source(kernel_name, sourcemodule_kwargs)
        self.prepare(signature, texrefs)

    def compile_kernel_source(self, kernel_name, sourcemodule_kwargs):
        self.sourcemodule_kwargs = sourcemodule_kwargs
        self.kernel_name = kernel_name
        with catch_warnings(action=("ignore" if self.silent_compilation_warnings else None)):  # pylint: disable=E1123
            self.module = SourceModule(self.src, **self.sourcemodule_kwargs)
        self.func = self.module.get_function(kernel_name)

    def prepare(self, kernel_signature, texrefs):
        self.prepared = False
        self.kernel_signature = kernel_signature
        self.texrefs = texrefs or []
        if kernel_signature is not None:
            self.func.prepare(self.kernel_signature, texrefs=self.texrefs)
            self.prepared = True

    def follow_device_arr(self, args):
        args = list(args)
        # Replace GPUArray with GPUArray.gpudata
        for i, arg in enumerate(args):
            if isinstance(arg, garray.GPUArray):
                args[i] = arg.gpudata
        return tuple(args)

    def get_last_kernel_time(self):
        """
        Return the execution time (in seconds) of the last called kernel.
        The last called kernel should have been called with time_kernel=True.
        """
        if self.last_kernel_time is not None:
            return self.last_kernel_time()
        else:
            return None

    def call(self, *args, **kwargs):
        grid, block, args, kwargs = self._prepare_call(*args, **kwargs)

        if self.prepared:
            func_call = self.func.prepared_call
            if "time_kernel" in kwargs:
                func_call = self.func.prepared_timed_call
                kwargs.pop("time_kernel")
            if "block" in kwargs:
                kwargs.pop("block")
            if "grid" in kwargs:
                kwargs.pop("grid")
            t = func_call(grid, block, *args, **kwargs)
        else:
            kwargs["block"] = block
            kwargs["grid"] = grid
            t = self.func(*args, **kwargs)
        self.last_kernel_time = t  # list ?

    __call__ = call
