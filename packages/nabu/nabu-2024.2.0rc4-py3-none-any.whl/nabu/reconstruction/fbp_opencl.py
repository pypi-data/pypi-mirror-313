import pyopencl as cl
from ..utils import get_opencl_srcfile
from ..opencl.processing import OpenCLProcessing
from ..opencl.kernel import OpenCLKernel
from ..opencl.utils import allocate_texture, check_textures_availability, copy_to_texture
from .filtering_opencl import OpenCLSinoFilter
from .sinogram_opencl import OpenCLSinoMult
from .fbp_base import BackprojectorBase


class OpenCLBackprojector(BackprojectorBase):
    default_extra_options = {**BackprojectorBase.default_extra_options, "use_textures": True}
    backend = "opencl"
    kernel_filename = "backproj.cl"
    backend_processing_class = OpenCLProcessing
    SinoFilterClass = OpenCLSinoFilter
    SinoMultClass = OpenCLSinoMult

    def _check_textures_availability(self):
        self._use_textures = self.extra_options.get("use_textures", True) and check_textures_availability(
            self._processing.ctx
        )

    def _get_kernel_options(self):
        super()._get_kernel_options()
        self._kernel_options.update(
            {
                "file_name": get_opencl_srcfile(self.kernel_filename),
            }
        )

    def _prepare_kernel_args(self):
        super()._prepare_kernel_args()
        block = self.kern_proj_kwargs.pop("block")
        local_size = block
        grid = self.kern_proj_kwargs.pop("grid")
        global_size = (grid[0] * block[0], grid[1] * block[1])
        # global_size = (updiv(self.n_x, 2), updiv(self.n_y, 2))
        self.kern_proj_args.insert(0, self._processing.queue)  # OpenCLProcessing.__call__ expects first arg to be queue
        self.kern_proj_kwargs.update(
            {
                "global_size": global_size,
                "local_size": local_size,
            }
        )

    def _prepare_textures(self):
        if self._use_textures:
            d_sino_ref = self.d_sino_tex = allocate_texture(self._processing.ctx, self.sino_shape)
            self._kernel_options["sourcemodule_options"].append("-DUSE_TEXTURES")
        else:
            self._d_sino = self._processing.allocate_array("_d_sino", self.sino_shape)
            d_sino_ref = self._d_sino.data
        self.kern_proj_args[2] = d_sino_ref

    def _compile_kernels(self):
        self._prepare_kernel_args()
        self._prepare_textures()  # has to be done before compilation for OpenCL (to pass -DUSE_TEXTURES)
        self.kern_proj_args.append(cl.LocalMemory(self._kernel_options["shared_size"]))
        self.gpu_projector = OpenCLKernel(
            self._kernel_options["kernel_name"],
            self._processing.ctx,
            filename=self._kernel_options["file_name"],
            options=self._kernel_options["sourcemodule_options"],
        )
        if self.halftomo and self.rot_center < self.dwidth:
            self.sino_mult = OpenCLSinoMult(self.sino_shape, self.rot_center, ctx=self._processing.ctx)

    def _transfer_to_texture(self, sino, do_checks=True):
        if self._use_textures:
            return copy_to_texture(self._processing.queue, self.d_sino_tex, sino)
        else:
            if id(self._d_sino) == id(sino):
                return
            return cl.enqueue_copy(self._processing.queue, self._d_sino.data, sino.data)

    def _set_kernel_slice_arg(self, d_slice):
        self.kern_proj_args[1] = d_slice
