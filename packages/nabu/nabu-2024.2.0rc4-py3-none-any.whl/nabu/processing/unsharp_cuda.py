from ..cuda.utils import __has_pycuda__
from ..processing.convolution_cuda import Convolution
from ..cuda.processing import CudaProcessing
from .unsharp import UnsharpMask

if __has_pycuda__:
    from pycuda.elementwise import ElementwiseKernel


class CudaUnsharpMask(UnsharpMask):
    def __init__(self, shape, sigma, coeff, mode="reflect", method="gaussian", **cuda_options):
        """
        Unsharp Mask, cuda backend.
        """
        super().__init__(shape, sigma, coeff, mode=mode, method=method)
        self.cuda_processing = CudaProcessing(**(cuda_options or {}))
        self._init_convolution()
        self._init_mad_kernel()
        self.cuda_processing.init_arrays_to_none(["_d_out"])

    def _init_convolution(self):
        self.convolution = Convolution(
            self.shape,
            self._gaussian_kernel,
            mode=self.mode,
            extra_options={  # Use the lowest amount of memory
                "allocate_input_array": False,
                "allocate_output_array": False,
                "allocate_tmp_array": True,
            },
        )

    def _init_mad_kernel(self):
        # garray.GPUArray.mul_add is out of place...
        self.mad_kernel = ElementwiseKernel(  # pylint: disable=E0606
            "float* array, float fac, float* other, float otherfac",
            "array[i] = fac * array[i] + otherfac * other[i]",
            name="mul_add",
        )

    def unsharp(self, image, output=None):
        if output is None:
            output = self.cuda_processing.allocate_array("_d_out", self.shape, "f")
        self.convolution(image, output=output)
        if self.method == "gaussian":
            self.mad_kernel(output, -self.coeff, image, 1.0 + self.coeff)
        elif self.method == "log":
            # output = output * coeff + image   where output was image_blurred
            self.mad_kernel(output, self.coeff, image, 1.0)
        else:  # "imagej":
            # output = (image - coeff*image_blurred)/(1-coeff)  where output was image_blurred
            self.mad_kernel(output, -self.coeff / (1 - self.coeff), image, 1.0 / (1 - self.coeff))
        return output
