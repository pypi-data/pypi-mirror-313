import numpy as np
from ..utils import calc_padding_lengths, updiv, get_cuda_srcfile, docstring
from ..cuda.processing import CudaProcessing
from ..cuda.utils import __has_pycuda__
from ..processing.padding_cuda import CudaPadding
from ..processing.fft_cuda import get_fft_class
from .phase_cuda import CudaPaganinPhaseRetrieval
from .ctf import CTFPhaseRetrieval

if __has_pycuda__:
    from pycuda import gpuarray as garray


# TODO:
#  - better padding scheme (for now 2*shape)
#  - rework inheritance scheme ? (base class SingleDistancePhaseRetrieval and its cuda counterpart)
class CudaCTFPhaseRetrieval(CTFPhaseRetrieval):
    """
    Cuda back-end of CTFPhaseRetrieval
    """

    @docstring(CTFPhaseRetrieval)
    def __init__(
        self,
        shape,
        geo_pars,
        delta_beta,
        padded_shape="auto",
        padding_mode="reflect",
        translation_vh=None,
        normalize_by_mean=False,
        lim1=1.0e-5,
        lim2=0.2,
        use_rfft=True,
        fftw_num_threads=None,  # COMPAT.
        fft_num_threads=None,
        logger=None,
        cuda_options=None,
        fft_backend="vkfft",
    ):
        """
        Initialize a CudaCTFPhaseRetrieval.

        Parameters
        ----------
        shape: tuple
            Shape of the images to process
        padding_mode: str
            Padding mode. Default is "reflect".

        Other parameters
        -----------------
        Please refer to CTFPhaseRetrieval documentation.
        """
        if not use_rfft:
            raise ValueError("Only use_rfft=True is supported")
        self.cuda_processing = CudaProcessing(**(cuda_options or {}))
        super().__init__(
            shape,
            geo_pars,
            delta_beta,
            padded_shape=padded_shape,
            padding_mode=padding_mode,
            translation_vh=translation_vh,
            normalize_by_mean=normalize_by_mean,
            lim1=lim1,
            lim2=lim2,
            logger=logger,
            use_rfft=True,
            fft_num_threads=False,
        )
        self._init_ctf_filter()
        self._init_cuda_padding()
        self._init_fft(fft_backend)
        self._init_mult_kernel()

    def _init_ctf_filter(self):
        self._mean_scale_factor = self.unreg_filter_denom[0, 0] * np.prod(self.shape_padded)
        self._d_filter_num = self.cuda_processing.to_device("_d_filter_num", self.unreg_filter_denom).astype("f")
        self._d_filter_denom = self.cuda_processing.to_device(
            "_d_filter_denom", (1.0 / (2 * self.unreg_filter_denom * self.unreg_filter_denom + self.lim)).astype("f")
        )

    def _init_cuda_padding(self):
        pad_width = calc_padding_lengths(self.shape, self.shape_padded)
        # Custom coordinate transform to get directly FFT layout
        R, C = np.indices(self.shape, dtype=np.int32, sparse=True)
        coords_R = np.roll(np.pad(R.ravel(), pad_width[0], mode=self.padding_mode), -pad_width[0][0])
        coords_C = np.roll(np.pad(C.ravel(), pad_width[1], mode=self.padding_mode), -pad_width[1][0])
        self.cuda_padding = CudaPadding(
            self.shape,
            (coords_R, coords_C),
            mode=self.padding_mode,
            # propagate cuda options ?
        )

    def _init_fft(self, fft_backend):
        fft_cls = get_fft_class(backend=fft_backend)
        self.cufft = fft_cls(shape=self.shape_padded, dtype=np.float32, r2c=True)
        self.d_radio_padded = self.cuda_processing.allocate_array("d_radio_padded", self.shape_padded, "f")
        self.d_radio_f = self.cuda_processing.allocate_array("d_radio_f", self.cufft.shape_out, np.complex64)

    def _init_mult_kernel(self):
        self.cpxmult_kernel = self.cuda_processing.kernel(
            "CTF_kernel",
            filename=get_cuda_srcfile("ElementOp.cu"),
            signature="PPPfii",
        )
        Nx = np.int32(self.shape_padded[1] // 2 + 1)
        Ny = np.int32(self.shape_padded[0])
        self._cpxmult_kernel_args = [
            self.d_radio_f,
            self._d_filter_num,
            self._d_filter_denom,
            np.float32(self._mean_scale_factor),
            Nx,
            Ny,
        ]
        blk = (32, 32, 1)
        grd = (updiv(Nx, blk[0]), updiv(Ny, blk[1]))
        self._cpxmult_kernel_kwargs = {"grid": grd, "block": blk}

    set_input = CudaPaganinPhaseRetrieval.set_input

    def retrieve_phase(self, image, output=None):
        """
        Perform padding on an image. Please see the documentation of CTFPhaseRetrieval.retrieve_phase().
        """
        self.set_input(image)
        self.cuda_padding.pad(image, output=self.d_radio_padded)
        if self.normalize_by_mean:
            m = garray.sum(self.d_radio_padded).get() / np.prod(self.shape_padded)  # pylint: disable=E0606
            self.d_radio_padded /= m
        self.cufft.fft(self.d_radio_padded, output=self.d_radio_f)
        self.cpxmult_kernel(*self._cpxmult_kernel_args, **self._cpxmult_kernel_kwargs)
        self.cufft.ifft(self.d_radio_f, output=self.d_radio_padded)

        if output is None:
            output = self.cuda_processing.allocate_array("d_output", self.shape)
        output[:, :] = self.d_radio_padded[: self.shape[0], : self.shape[1]]
        return output
