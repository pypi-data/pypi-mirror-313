from itertools import permutations
import pytest
import numpy as np
from scipy.fft import fftn, ifftn, rfftn, irfftn
from nabu.testutils import generate_tests_scenarios, get_data, get_array_of_given_shape, __do_long_tests__
from nabu.cuda.utils import get_cuda_context, __has_pycuda__
from nabu.processing.fft_cuda import SKCUFFT, VKCUFFT, get_available_fft_implems
from nabu.opencl.utils import __has_pyopencl__, get_opencl_context
from nabu.processing.fft_opencl import VKCLFFT, has_vkfft as has_cl_vkfft
from nabu.processing.fft_base import is_fast_axes

available_cuda_fft = get_available_fft_implems()
__has_vkfft__ = "vkfft" in available_cuda_fft
__has_skcuda__ = "skcuda" in available_cuda_fft


scenarios = {
    "shape": [(256,), (300,), (300, 301), (300, 302)],
    "r2c": [True, False],
    "precision": ["simple"],
    "backend": ["cuda", "opencl"],
}

if __do_long_tests__:
    scenarios["shape"].extend([(307,), (125, 126, 260)])
    scenarios["precision"].append("double")

scenarios = generate_tests_scenarios(scenarios)


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls

    cls.data = get_data("chelsea.npz")["data"]
    cls.abs_tol = {
        "simple": {
            1: 5e-3,
            2: 1.0e0,
            3: 5e2,  # !
        },
        "double": {
            1: 1e-10,
            2: 1e-9,
            3: 1e-7,
        },
    }
    if __has_pycuda__:
        cls.cu_ctx = get_cuda_context(cleanup_at_exit=False)
    if __has_pyopencl__:
        cls.cl_ctx = get_opencl_context("all")
    yield
    if __has_pycuda__:
        cls.cu_ctx.pop()


def _get_fft_cls(backend):
    fft_cls = None
    if backend == "cuda":
        if not (__has_vkfft__ and __has_pycuda__):
            pytest.skip("Need vkfft and pycuda to use VKCUFFT")
        fft_cls = VKCUFFT
    if backend == "opencl":
        if not (has_cl_vkfft() and __has_pyopencl__):
            pytest.skip("Need vkfft and pyopencl to use VKCLFFT")
        fft_cls = VKCLFFT
    return fft_cls


@pytest.mark.usefixtures("bootstrap")
class TestFFT:
    def _get_data_array(self, config):
        r2c = config["r2c"]
        shape = config["shape"]
        precision = config["precision"]
        dtype = {
            True: {"simple": np.float32, "double": np.float64},
            False: {"simple": np.complex64, "double": np.complex128},
        }[r2c][precision]
        data = get_array_of_given_shape(self.data, shape, dtype)
        return data

    @staticmethod
    def check_result(res, ref, config, tol, name=""):
        err_max = np.max(np.abs(res - ref))
        err_msg = "%s FFT(%s, r2c=%s): tol=%.2e, but max error = %.2e" % (
            name,
            str(config["shape"]),
            str(config["r2c"]),
            tol,
            err_max,
        )
        assert np.allclose(res, ref, atol=tol), err_msg

    def _do_fft(self, data, r2c, axes=None, return_fft_obj=False, backend_cls=None):
        ctx = self.cu_ctx if backend_cls.backend == "cuda" else self.cl_ctx
        fft = backend_cls(data.shape, data.dtype, r2c=r2c, axes=axes, ctx=ctx)
        d_data = fft.processing.allocate_array("_data", data.shape, dtype=data.dtype)
        d_data.set(data)
        d_out = fft.fft(d_data)
        res = d_out.get()
        return (res, fft) if return_fft_obj else res

    @staticmethod
    def _do_reference_fft(data, r2c, axes=None):
        ref_fft_func = rfftn if r2c else fftn
        ref = ref_fft_func(data, axes=axes)
        return ref

    @staticmethod
    def _do_reference_ifft(data, r2c, axes=None):
        ref_ifft_func = irfftn if r2c else ifftn
        ref = ref_ifft_func(data, axes=axes)
        return ref

    @pytest.mark.skipif(
        not (__has_skcuda__ and __has_pycuda__), reason="Need pycuda and (scikit-cuda or vkfft) for this test"
    )
    @pytest.mark.parametrize("config", scenarios)
    def test_sckcuda(self, config):
        r2c = config["r2c"]
        shape = config["shape"]
        precision = config["precision"]
        ndim = len(shape)
        if ndim == 3 and not (__do_long_tests__):
            pytest.skip("3D FFTs are done only for long tests - use NABU_LONG_TESTS=1")

        data = self._get_data_array(config)

        res, cufft = self._do_fft(data, r2c, return_fft_obj=True, backend_cls=SKCUFFT)
        ref = self._do_reference_fft(data, r2c)

        tol = self.abs_tol[precision][ndim]
        self.check_result(res, ref, config, tol, name="skcuda")

        # Complex-to-complex can also be performed on real data (as in numpy.fft.fft(real_data))
        if not (r2c):
            res = self._do_fft(data, False, backend_cls=SKCUFFT)
            ref = self._do_reference_fft(data, False)
            self.check_result(res, ref, config, tol, name="skcuda")

        # IFFT
        res = cufft.ifft(cufft.output_fft).get()
        self.check_result(res, data, config, tol, name="skcuda")
        # Perhaps we should also check against numpy/scipy ifft,
        # but it does not yield the good shape for R2C on odd-sized data

    @pytest.mark.skipif(
        not (__has_skcuda__ and __has_pycuda__), reason="Need pycuda and (scikit-cuda or vkfft) for this test"
    )
    @pytest.mark.parametrize("config", scenarios)
    def test_skcuda_batched(self, config):
        shape = config["shape"]
        if len(shape) == 1:
            return
        elif len(shape) == 3 and not (__do_long_tests__):
            pytest.skip("3D FFTs are done only for long tests - use NABU_LONG_TESTS=1")
        r2c = config["r2c"]
        tol = self.abs_tol[config["precision"]][len(shape)]

        data = self._get_data_array(config)

        if data.ndim == 2:
            axes_to_test = [(0,), (1,)]
        elif data.ndim == 3:
            # axes_to_test = [(1, 2), (2, 1), (2,)] # See fft.py: works for C2C but not R2C ?
            axes_to_test = [(2,)]

        for axes in axes_to_test:
            res, cufft = self._do_fft(data, r2c, axes=axes, return_fft_obj=True, backend_cls=SKCUFFT)
            ref = self._do_reference_fft(data, r2c, axes=axes)
            self.check_result(res, ref, config, tol, name="skcuda batched axes=%s" % (str(axes)))
            # IFFT
            res = cufft.ifft(cufft.output_fft).get()
            self.check_result(res, data, config, tol, name="skcuda")

    @pytest.mark.parametrize("config", scenarios)
    def test_vkfft(self, config):
        backend = config["backend"]
        fft_cls = _get_fft_cls(backend)

        r2c = config["r2c"]
        shape = config["shape"]
        precision = config["precision"]
        ndim = len(shape)
        if ndim == 3 and not (__do_long_tests__):
            pytest.skip("3D FFTs are done only for long tests - use NABU_LONG_TESTS=1")

        if ndim >= 2 and r2c and shape[-1] & 1:
            pytest.skip("R2C with odd-sized fast dimension is not supported in VKFFT")

        # FIXME - vkfft + POCL fail for R2C in one dimension
        if config["backend"] == "opencl" and r2c and ndim == 1:
            if self.cl_ctx.devices[0].platform.name.strip().lower() == "portable computing language":
                pytest.skip("Something wrong with vkfft + pocl for R2C 1D")
        # ---

        data = self._get_data_array(config)

        res, fft_obj = self._do_fft(data, r2c, return_fft_obj=True, backend_cls=fft_cls)
        ref = self._do_reference_fft(data, r2c)

        tol = self.abs_tol[precision][ndim]
        self.check_result(res, ref, config, tol, name="vkfft_%s" % backend)

        # Complex-to-complex can also be performed on real data (as in numpy.fft.fft(real_data))
        if not (r2c):
            res = self._do_fft(data, False, backend_cls=fft_cls)
            ref = self._do_reference_fft(data, False)
            self.check_result(res, ref, config, tol, name="vkfft_%s" % backend)

        # IFFT
        res = fft_obj.ifft(fft_obj.output_fft).get()
        self.check_result(res, data, config, tol, name="vkfft_%s" % backend)

    @pytest.mark.parametrize("config", scenarios)
    def test_vkfft_batched(self, config):
        backend = config["backend"]
        fft_cls = _get_fft_cls(backend)
        shape = config["shape"]
        if len(shape) == 1:
            return
        elif len(shape) == 3 and not (__do_long_tests__):
            pytest.skip("3D FFTs are done only for long tests - use NABU_LONG_TESTS=1")
        r2c = config["r2c"]
        tol = self.abs_tol[config["precision"]][len(shape)]

        data = self._get_data_array(config)

        if data.ndim >= 2 and r2c and shape[-1] & 1:
            pytest.skip("R2C with odd-sized fast dimension is not supported in VKFFT")

        # For R2C, only fastest axes are supported by vkfft
        if data.ndim == 2:
            axes_to_test = [(1,)]
        elif data.ndim == 3:
            axes_to_test = [
                (1, 2),
                (2,),
            ]
        for axes in axes_to_test:
            res, cufft = self._do_fft(data, r2c, axes=axes, return_fft_obj=True, backend_cls=fft_cls)
            ref = self._do_reference_fft(data, r2c, axes=axes)
            self.check_result(res, ref, config, tol, name="vkfft_%s batched axes=%s" % (backend, str(axes)))
            # IFFT
            res = cufft.ifft(cufft.output_fft).get()
            self.check_result(res, data, config, tol, name="vkfft_%s" % backend)

    @pytest.mark.skipif(not (__do_long_tests__), reason="Use NABU_LONG_TESTS=1 for this test")
    def test_fast_axes_utility_function(self):
        axes_to_test = {
            2: {
                (0, 1): True,
                (1,): True,
                (-1,): True,
                (-2,): False,
                (0,): False,
            },
            3: {
                (0, 1, 2): True,
                (0, 1): False,
                (1, 2): True,
                (2, 1): True,
                (-2, -1): True,
                (2,): True,
                (-1,): True,
            },
        }
        for ndim, axes_ in axes_to_test.items():
            for axes, is_fast in axes_.items():
                possible_axes = [axes]
                if len(axes) > 1:
                    possible_axes = list(permutations(axes, len(axes)))
                for ax in possible_axes:
                    assert is_fast_axes(ndim, ax) is is_fast
