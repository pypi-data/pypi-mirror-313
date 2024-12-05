import numpy as np
import pytest
from nabu.cuda.utils import get_cuda_context, __has_pycuda__
from nabu.opencl.utils import __has_pyopencl__, get_opencl_context
from nabu.processing.padding_cuda import CudaPadding
from nabu.processing.padding_opencl import OpenCLPadding
from nabu.utils import calc_padding_lengths, get_cuda_srcfile
from nabu.testutils import __do_long_tests__
from nabu.testutils import get_data, generate_tests_scenarios

scenarios = {
    "shape": [(511, 512), (512, 511)],
    "pad_width": [((256, 255), (128, 127))],
    "mode_cuda": CudaPadding.supported_modes[:2] if __has_pycuda__ else [],
    "mode_opencl": OpenCLPadding.supported_modes[:2] if __has_pyopencl__ else [],
    "constant_values": [0, ((1.0, 2.0), (3.0, 4.0))],
    "output_is_none": [True, False],
    "backend": ["cuda", "opencl"],
}


if __do_long_tests__:
    scenarios["mode_cuda"] = CudaPadding.supported_modes if __has_pycuda__ else []
    scenarios["mode_opencl"] = OpenCLPadding.supported_modes if __has_pyopencl__ else []
    scenarios["pad_width"].extend([((0, 0), (6, 7))])

scenarios = generate_tests_scenarios(scenarios)


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls
    cls.data = get_data("brain_phantom.npz")["data"]
    cls.tol = 1e-7
    if __has_pycuda__:
        cls.cu_ctx = get_cuda_context(cleanup_at_exit=False)
    if __has_pyopencl__:
        cls.cl_ctx = get_opencl_context(device_type="all")
    yield
    if __has_pycuda__:
        cls.cu_ctx.pop()


@pytest.mark.usefixtures("bootstrap")
class TestPadding:
    @pytest.mark.parametrize("config", scenarios)
    def test_padding(self, config):
        backend = config["backend"]
        shape = config["shape"]
        padding_mode = config["mode_%s" % backend]
        data = self.data[: shape[0], : shape[1]]
        kwargs = {}
        if padding_mode == "constant":
            kwargs["constant_values"] = config["constant_values"]
        ref = np.pad(data, config["pad_width"], mode=padding_mode, **kwargs)

        PaddingCls = CudaPadding if backend == "cuda" else OpenCLPadding
        if backend == "cuda":
            backend_options = {"cuda_options": {"ctx": self.cu_ctx}}
        else:
            backend_options = {"opencl_options": {"ctx": self.cl_ctx}}

        padding = PaddingCls(
            config["shape"],
            config["pad_width"],
            mode=padding_mode,
            constant_values=config["constant_values"],
            **backend_options,
        )
        if config["output_is_none"]:
            output = None
        else:
            output = padding.processing.allocate_array("output", ref.shape, dtype="f")

        d_img = padding.processing.allocate_array("d_img", data.shape, dtype="f")
        d_img.set(np.ascontiguousarray(data, dtype="f"))
        res = padding.pad(d_img, output=output)

        err_max = np.max(np.abs(res.get() - ref))
        assert err_max < self.tol, str("Something wrong with padding for configuration %s" % (str(config)))

    @pytest.mark.skipif(not (__has_pycuda__) and not (__has_pyopencl__), reason="need pycuda or pyopencl")
    def test_custom_coordinate_transform(self):
        data = self.data
        R, C = np.indices(data.shape, dtype=np.int32)

        pad_width = ((256, 255), (254, 251))
        mode = "reflect"

        coords_R = np.pad(R, pad_width[0], mode=mode)[:, 0]
        coords_C = np.pad(C, pad_width[1], mode=mode)[0, :]

        # Further transform of coordinates - here FFT layout
        coords_R = np.roll(coords_R, -pad_width[0][0])
        coords_C = np.roll(coords_C, -pad_width[1][0])

        padding_classes_to_test = []
        if __has_pycuda__:
            padding_classes_to_test.append(CudaPadding)
        if __has_pyopencl__:
            padding_classes_to_test.append(OpenCLPadding)

        for padding_cls in padding_classes_to_test:
            ctx = self.cl_ctx if padding_cls.backend == "opencl" else self.cu_ctx
            padding = padding_cls(data.shape, (coords_R, coords_C), mode=mode, ctx=ctx)

            d_img = padding.processing.allocate_array("d_img", data.shape, dtype="f")
            d_img.set(data)
            d_out = padding.processing.allocate_array("d_out", padding.padded_shape, dtype="f")

            res = padding.pad(d_img, output=d_out)

            ref = np.roll(np.pad(data, pad_width, mode=mode), (-pad_width[0][0], -pad_width[1][0]), axis=(0, 1))

            err_max = np.max(np.abs(d_out.get() - ref))
            assert err_max < self.tol, "Something wrong with custom padding"


#
# The following is testing a previous version of padding kernels
# They use specific code (instead of a generic coordinate transform)
#

if __has_pycuda__:
    from nabu.cuda.kernel import CudaKernel
    import pycuda.gpuarray as garray


scenarios_legacy = [
    {
        "shape": (512, 501),
        "shape_padded": (1023, 1022),
        "constant_values": ((1.0, 2.0), (3.0, 4.0)),
    },
]


# parametrize with fixture and "params=" will launch a new class for each scenario.
# the attributes set to "cls" will remain for all the tests done in this class
# with the current scenario.
@pytest.fixture(scope="class", params=scenarios_legacy)
def bootstrap_legacy(request):
    cls = request.cls
    cls.data = get_data("mri_proj_astra.npz")["data"]
    cls.tol = 1e-7
    cls.params = request.param
    cls.ctx = get_cuda_context(cleanup_at_exit=False)
    cls._calc_pad()
    cls._init_kernels()
    yield
    cls.ctx.pop()


@pytest.mark.skipif(not (__has_pycuda__), reason="Need Cuda and pycuda for this test")
@pytest.mark.usefixtures("bootstrap_legacy")
class TestPaddingLegacy:
    @classmethod
    def _calc_pad(cls):
        cls.shape = cls.params["shape"]
        cls.data = np.ascontiguousarray(cls.data[: cls.shape[0], : cls.shape[1]])
        cls.shape_padded = cls.params["shape_padded"]
        ((pt, pb), (pl, pr)) = calc_padding_lengths(cls.shape, cls.shape_padded)
        cls.pad_top_len = pt
        cls.pad_bottom_len = pb
        cls.pad_left_len = pl
        cls.pad_right_len = pr

    @classmethod
    def _init_kernels(cls):
        cls.pad_kern = CudaKernel(
            "padding_constant",
            filename=get_cuda_srcfile("padding.cu"),
            signature="Piiiiiiiiffff",
        )
        cls.pad_edge_kern = CudaKernel(
            "padding_edge",
            filename=get_cuda_srcfile("padding.cu"),
            signature="Piiiiiiii",
        )
        cls.d_data_padded = garray.zeros(cls.shape_padded, "f")

    def _init_padding(self, arr=None):
        arr = arr or self.data
        self.d_data_padded.fill(0)
        Ny, Nx = self.shape
        self.d_data_padded[:Ny, :Nx] = self.data

    def _pad_numpy(self, arr=None, **np_pad_kwargs):
        arr = arr or self.data
        data_padded_ref = np.pad(
            arr, ((self.pad_top_len, self.pad_bottom_len), (self.pad_left_len, self.pad_right_len)), **np_pad_kwargs
        )
        # Put in the FFT layout
        data_padded_ref = np.roll(data_padded_ref, (-self.pad_top_len, -self.pad_left_len), axis=(0, 1))
        return data_padded_ref

    def test_constant_padding(self):
        self._init_padding()
        # Pad using the cuda kernel
        ((val_top, val_bottom), (val_left, val_right)) = self.params["constant_values"]
        Ny, Nx = self.shape
        Nyp, Nxp = self.shape_padded

        self.pad_kern(
            self.d_data_padded,
            Nx,
            Ny,
            Nxp,
            Nyp,
            self.pad_left_len,
            self.pad_right_len,
            self.pad_top_len,
            self.pad_bottom_len,
            val_left,
            val_right,
            val_top,
            val_bottom,
        )
        # Pad using numpy
        data_padded_ref = self._pad_numpy(mode="constant", constant_values=self.params["constant_values"])
        # Compare
        errmax = np.max(np.abs(self.d_data_padded.get() - data_padded_ref))
        assert errmax < self.tol, "Max error is too high"

    def test_edge_padding(self):
        self._init_padding()
        # Pad using the cuda kernel
        ((val_top, val_bottom), (val_left, val_right)) = self.params["constant_values"]
        Ny, Nx = self.shape
        Nyp, Nxp = self.shape_padded

        self.pad_edge_kern(
            self.d_data_padded,
            Nx,
            Ny,
            Nxp,
            Nyp,
            self.pad_left_len,
            self.pad_right_len,
            self.pad_top_len,
            self.pad_bottom_len,
        )
        # Pad using numpy
        data_padded_ref = self._pad_numpy(mode="edge")
        # Compare
        errmax = np.max(np.abs(self.d_data_padded.get() - data_padded_ref))
        assert errmax < self.tol, "Max error is too high"
