import numpy as np
from nabu.utils import get_cuda_srcfile, updiv
from .muladd import MulAdd
from ..cuda.utils import __has_pycuda__
from ..cuda.processing import CudaProcessing

if __has_pycuda__:
    import pycuda.gpuarray as garray


class CudaMulAdd(MulAdd):
    processing_cls = CudaProcessing

    def _init_finalize(self):
        self._init_kernel()

    def _init_kernel(self):
        self.muladd_kernel = self.processing.kernel(
            "mul_add",
            filename=get_cuda_srcfile("ElementOp.cu"),  # signature="PPiiffiiii"
        )

    def mul_add(self, dst, other, fac_dst, fac_other, dst_region=None, other_region=None):
        """
        'region' should be a tuple (slice(y_start, y_end), slice(x_start, x_end))
        """

        if dst_region is None:
            dst_coords = (0, dst.shape[1], 0, dst.shape[0])
        else:
            dst_coords = (dst_region[1].start, dst_region[1].stop, dst_region[0].start, dst_region[0].stop)
        if other_region is None:
            other_coords = (0, other.shape[1], 0, other.shape[0])
        else:
            other_coords = (other_region[1].start, other_region[1].stop, other_region[0].start, other_region[0].stop)

        delta_x = np.diff(dst_coords[:2])
        delta_y = np.diff(dst_coords[2:])
        if delta_x != np.diff(other_coords[:2]) or delta_y != np.diff(other_coords[2:]):
            raise ValueError("Invalid dst_region and other_region provided. Regions must have the same size")
        if delta_x == 0 or delta_y == 0:
            raise ValueError("delta_x or delta_y is 0")

        # can't use "int4" in pycuda ? int2 seems fine. Go figure
        # pylint: disable=E0606
        dst_x_range = np.array(dst_coords[:2], dtype=garray.vec.int2)
        dst_y_range = np.array(dst_coords[2:], dtype=garray.vec.int2)
        other_x_range = np.array(other_coords[:2], dtype=garray.vec.int2)
        other_y_range = np.array(other_coords[2:], dtype=garray.vec.int2)

        block = (32, 32, 1)
        grid = [updiv(length, b) for (length, b) in zip((delta_x[0], delta_y[0]), block)]

        self.muladd_kernel(
            dst,
            other,
            np.int32(dst.shape[1]),
            np.int32(other.shape[1]),
            np.float32(fac_dst),
            np.float32(fac_other),
            dst_x_range,
            dst_y_range,
            other_x_range,
            other_y_range,
            grid=grid,
            block=block,
        )

    __call__ = mul_add
