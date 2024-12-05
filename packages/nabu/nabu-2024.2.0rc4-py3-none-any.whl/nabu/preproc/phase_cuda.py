import numpy as np
import pycuda.driver as cuda
from ..utils import get_cuda_srcfile, check_supported, docstring
from ..cuda.processing import CudaProcessing
from ..processing.fft_cuda import get_fft_class
from .phase import PaganinPhaseRetrieval


class CudaPaganinPhaseRetrieval(PaganinPhaseRetrieval):
    supported_paddings = ["zeros", "constant", "edge"]

    @docstring(PaganinPhaseRetrieval)
    def __init__(
        self,
        shape,
        distance=0.5,
        energy=20,
        delta_beta=250.0,
        pixel_size=1e-6,
        padding="edge",
        cuda_options=None,
        fftw_num_threads=None,  # COMPAT.
        fft_num_threads=None,
        fft_backend="vkfft",
    ):
        """
        Please refer to the documentation of
        nabu.preproc.phase.PaganinPhaseRetrieval
        """
        padding = self._check_padding(padding)
        self.cuda_processing = CudaProcessing(**(cuda_options or {}))
        super().__init__(
            shape,
            distance=distance,
            energy=energy,
            delta_beta=delta_beta,
            pixel_size=pixel_size,
            padding=padding,
            use_rfft=True,
            fft_num_threads=False,
        )
        self._init_gpu_arrays()
        self._init_fft(fft_backend)
        self._init_padding_kernel()
        self._init_mult_kernel()

    def _check_padding(self, padding):
        check_supported(padding, self.supported_paddings, "padding")
        if padding == "zeros":
            padding = "constant"
        return padding

    def _init_gpu_arrays(self):
        self.d_paganin_filter = self.cuda_processing.to_device(
            "d_paganin_filter", np.ascontiguousarray(self.paganin_filter, dtype=np.float32)
        )

    # overwrite parent method, don't initialize any FFT plan
    def _get_fft(self, use_rfft, fft_num_threads):
        self.use_rfft = use_rfft

    def _init_fft(self, fft_backend):
        fft_cls = get_fft_class(backend=fft_backend)
        self.cufft = fft_cls(shape=self.data_padded.shape, dtype=np.float32, r2c=True)
        self.d_radio_padded = self.cuda_processing.allocate_array("d_radio_padded", self.cufft.shape, "f")
        self.d_radio_f = self.cuda_processing.allocate_array("d_radio_f", self.cufft.shape_out, np.complex64)

    def _init_padding_kernel(self):
        kern_signature = {"constant": "Piiiiiiiiffff", "edge": "Piiiiiiii"}
        self.padding_kernel = self.cuda_processing.kernel(
            "padding_%s" % self.padding,
            filename=get_cuda_srcfile("padding.cu"),
            signature=kern_signature[self.padding],
        )
        Ny, Nx = self.shape
        Nyp, Nxp = self.shape_padded
        self.padding_kernel_args = [
            self.d_radio_padded,
            Nx,
            Ny,
            Nxp,
            Nyp,
            self.pad_left_len,
            self.pad_right_len,
            self.pad_top_len,
            self.pad_bottom_len,
        ]
        # TODO configurable constant values
        if self.padding == "constant":
            self.padding_kernel_args.extend([0, 0, 0, 0])

    def _init_mult_kernel(self):
        self.cpxmult_kernel = self.cuda_processing.kernel(
            "inplace_complexreal_mul_2Dby2D",
            filename=get_cuda_srcfile("ElementOp.cu"),
            signature="PPii",
        )
        self.cpxmult_kernel_args = [
            self.d_radio_f,
            self.d_paganin_filter,
            self.shape_padded[1] // 2 + 1,
            self.shape_padded[0],
        ]

    def set_input(self, data):
        assert data.shape == self.shape
        assert data.dtype == np.float32
        # Rectangular memcopy
        # TODO profile, and if needed include this copy in the padding kernel
        if isinstance(data, np.ndarray) or isinstance(data, self.cuda_processing.array_class):
            self.d_radio_padded[: self.shape[0], : self.shape[1]] = data[:, :]
        elif isinstance(data, cuda.DeviceAllocation):
            # TODO manual memcpy2D
            raise NotImplementedError("pycuda buffers are not supported yet")
        else:
            raise ValueError("Expected either numpy array, pycuda array or pycuda buffer")

    def get_output(self, output):
        s0, s1 = self.shape
        if output is None:
            # copy D2H
            return self.d_radio_padded[:s0, :s1].get()
        assert output.shape == self.shape
        assert output.dtype == np.float32
        output[:, :] = self.d_radio_padded[:s0, :s1]
        return output

    def apply_filter(self, radio, output=None):
        self.set_input(radio)

        self.padding_kernel(*self.padding_kernel_args)
        self.cufft.fft(self.d_radio_padded, output=self.d_radio_f)
        self.cpxmult_kernel(*self.cpxmult_kernel_args)
        self.cufft.ifft(self.d_radio_f, output=self.d_radio_padded)

        return self.get_output(output)

    __call__ = apply_filter

    retrieve_phase = apply_filter
