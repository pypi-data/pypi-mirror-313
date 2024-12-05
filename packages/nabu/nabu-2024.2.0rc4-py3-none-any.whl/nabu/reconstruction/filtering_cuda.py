import numpy as np
from ..cuda.processing import CudaProcessing
from ..utils import get_cuda_srcfile
from ..processing.padding_cuda import CudaPadding
from ..processing.fft_cuda import get_fft_class
from .filtering import SinoFilter


class CudaSinoFilter(SinoFilter):
    default_extra_options = {**SinoFilter.default_extra_options, **{"fft_backend": "vkfft"}}

    def __init__(
        self,
        sino_shape,
        filter_name=None,
        padding_mode="zeros",
        extra_options=None,
        cuda_options=None,
    ):
        self._cuda_options = cuda_options or {}
        self.cuda = CudaProcessing(**self._cuda_options)
        super().__init__(sino_shape, filter_name=filter_name, padding_mode=padding_mode, extra_options=extra_options)
        self._init_kernels()

    def _init_fft(self):
        fft_cls = get_fft_class(self.extra_options["fft_backend"])
        self.fft = fft_cls(
            self.sino_padded_shape,
            dtype=np.float32,
            axes=(-1,),
        )

    def _allocate_memory(self):
        self.d_filter_f = self.cuda.allocate_array("d_filter_f", (self.sino_f_shape[-1],), dtype=np.complex64)
        self.d_sino_padded = self.cuda.allocate_array("d_sino_padded", self.fft.shape)
        self.d_sino_f = self.cuda.allocate_array("d_sino_f", self.fft.shape_out, dtype=np.complex64)

    def set_filter(self, h_filt, normalize=True):
        super().set_filter(h_filt, normalize=normalize)
        self.d_filter_f[:] = self.filter_f[:]

    def _init_kernels(self):
        # pointwise complex multiplication
        fname = get_cuda_srcfile("ElementOp.cu")
        if self.ndim == 2:
            kernel_name = "inplace_complex_mul_2Dby1D"
            kernel_sig = "PPii"
        else:
            kernel_name = "inplace_complex_mul_3Dby1D"
            kernel_sig = "PPiii"
        self.mult_kernel = self.cuda.kernel(kernel_name, filename=fname, signature=kernel_sig)
        self.kern_args = (self.d_sino_f, self.d_filter_f)
        self.kern_args += self.d_sino_f.shape[::-1]
        # padding
        self.padding_kernel = CudaPadding(
            self.sino_shape,
            ((0, 0), (self.pad_left, self.pad_right)),
            mode=self.padding_mode,
            cuda_options=self._cuda_options,
        )

    def filter_sino(self, sino, output=None):
        """
        Perform the sinogram siltering.

        Parameters
        ----------
        sino: numpy.ndarray or pycuda.gpuarray.GPUArray
            Input sinogram (2D or 3D)
        output: pycuda.gpuarray.GPUArray, optional
            Output array.
        no_output: bool, optional
            If set to True, no copy is be done. The resulting data lies
            in self.d_sino_padded.
        """
        self._check_array(sino)
        if not (isinstance(sino, self.cuda.array_class)):
            sino = self.cuda.set_array("sino", sino)
        elif not (sino.flags.c_contiguous):
            # Transfer the device array into another, c-contiguous, device array
            # We can throw an error as well in this case, but often we so something like fbp(radios[:, i, :])
            sino_tmp = self.cuda.allocate_array("sino_contig", sino.shape)
            sino_tmp.set(sino)
            sino = sino_tmp

        # Padding
        self.padding_kernel(sino, output=self.d_sino_padded)

        # FFT
        self.fft.fft(self.d_sino_padded, output=self.d_sino_f)

        # multiply padded sinogram with filter in the Fourier domain
        self.mult_kernel(*self.kern_args)  # TODO tune block size ?

        # iFFT
        self.fft.ifft(self.d_sino_f, output=self.d_sino_padded)

        # return
        if output is None:
            res = self.cuda.allocate_array("output", self.sino_shape)
        else:
            res = output
        if self.ndim == 2:
            res[:] = self.d_sino_padded[:, self.pad_left : self.pad_left + self.dwidth]
        else:
            res[:] = self.d_sino_padded[:, :, self.pad_left : self.pad_left + self.dwidth]
        return res

    __call__ = filter_sino
