import numpy as np
import pycuda.driver as cuda
from ..utils import updiv, get_cuda_srcfile
from ..cuda.utils import copy_array, check_textures_availability
from ..cuda.processing import CudaProcessing
from ..cuda.kernel import CudaKernel
from .filtering_cuda import CudaSinoFilter
from .sinogram_cuda import CudaSinoMult
from .fbp_base import BackprojectorBase


class CudaBackprojector(BackprojectorBase):
    backend = "cuda"
    kernel_filename = "backproj.cu"
    backend_processing_class = CudaProcessing
    SinoFilterClass = CudaSinoFilter
    SinoMultClass = CudaSinoMult

    def _check_textures_availability(self):
        self._use_textures = self.extra_options.get("use_textures", True) and check_textures_availability()

    def _get_kernel_signature(self):
        kern_full_sig = list("PPiifiiffPPPf")
        if self._axis_correction is None:
            kern_full_sig[11] = ""
        if self._use_textures:
            # texture references - no object is passed (deprecated, removed in Cuda 12)
            kern_full_sig[1] = ""
        return "".join(kern_full_sig)

    def _get_kernel_options(self):
        super()._get_kernel_options()
        self._kernel_options.update(
            {
                "file_name": get_cuda_srcfile(self.kernel_filename),
                "kernel_signature": self._get_kernel_signature(),
                "texture_name": "tex_projections",
            }
        )

    def _prepare_kernel_args(self):
        super()._prepare_kernel_args()
        self.kern_proj_kwargs.update(
            {
                "shared_size": self._kernel_options["shared_size"],
            }
        )
        # texture references - no object is passed (deprecated, removed in Cuda 12)
        if self._use_textures:
            self.kern_proj_args.pop(1)
        else:
            self._d_sino = self._processing.allocate_array("_d_sino", self.sino_shape)
            self.kern_proj_args[1] = self._d_sino.gpudata

    def _prepare_textures(self):
        if self._use_textures:
            self.texref_proj = self.gpu_projector.module.get_texref(self._kernel_options["texture_name"])
            self.texref_proj.set_filter_mode(cuda.filter_mode.LINEAR)
            self.gpu_projector.prepare(self._kernel_options["kernel_signature"], [self.texref_proj])
            # Bind texture
            self._d_sino_cua = cuda.np_to_array(np.zeros(self.sino_shape, "f"), "C")
            self.texref_proj.set_array(self._d_sino_cua)
        else:
            # d_sino_ref = self._d_sino.gpudata
            # self.kern_proj_args.insert(2, d_sino_ref)
            self.gpu_projector.prepare(self._kernel_options["kernel_signature"], [])

    def _compile_kernels(self):
        self._prepare_kernel_args()
        if self._use_textures:
            self._kernel_options["sourcemodule_options"].append("-DUSE_TEXTURES")
        self.gpu_projector = CudaKernel(
            self._kernel_options["kernel_name"],
            filename=self._kernel_options["file_name"],
            options=self._kernel_options["sourcemodule_options"],
            silent_compilation_warnings=True,  # textures and Cuda 11
        )
        if self.halftomo and self.rot_center < self.dwidth:
            self.sino_mult = CudaSinoMult(self.sino_shape, self.rot_center, ctx=self._processing.ctx)
        self._prepare_textures()  # has to be done after compilation for Cuda (to bind texture to built kernel)

    def _transfer_to_texture(self, sino, do_checks=True):
        if do_checks and not (sino.flags.c_contiguous):
            raise ValueError("Expected C-Contiguous array")
        if self._use_textures:
            copy_array(self._d_sino_cua, sino, check=do_checks)
        else:
            if id(self._d_sino) == id(sino):
                return
            self._d_sino[:] = sino[:]


# COMPAT.
Backprojector = CudaBackprojector


class PolarBackprojector(Backprojector):
    """
    Cuda Backprojector with output in polar coordinates.
    """

    cuda_fname = "backproj_polar.cu"
    cuda_kernel_name = "backproj_polar"

    # patch parent method: force slice_shape to (n_angles, n_x)
    def _set_angles(self, angles, n_angles):
        Backprojector._set_angles(self, angles, n_angles)
        self.slice_shape = (self.n_angles, self.n_x)

    # patch parent method:
    def _set_slice_roi(self, slice_roi):
        if slice_roi is not None:
            raise ValueError("slice_roi is not supported with this class")
        Backprojector._set_slice_roi(self, slice_roi)

    # patch parent method: don't do the 4X compute-workload optimization for this kernel
    def _get_kernel_options(self):
        Backprojector._get_kernel_options(self)
        block = self._kernel_options["block"]
        self._kernel_options["grid"] = (updiv(self.n_x, block[0]), updiv(self.n_y, block[1]))

    # patch parent method: update kernel args
    def _compile_kernels(self):
        n_y = self.n_y
        self.n_y = self.n_angles
        Backprojector._compile_kernels(self)
        self.n_y = n_y
