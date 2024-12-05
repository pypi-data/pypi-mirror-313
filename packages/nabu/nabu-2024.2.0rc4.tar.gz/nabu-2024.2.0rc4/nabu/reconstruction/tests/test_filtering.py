import numpy as np
import pytest
from nabu.reconstruction.filtering import SinoFilter, filter_sinogram
from nabu.cuda.utils import __has_pycuda__
from nabu.opencl.utils import __has_pyopencl__
from nabu.testutils import get_data, generate_tests_scenarios, __do_long_tests__

if __has_pycuda__:
    from nabu.cuda.utils import get_cuda_context
    from nabu.reconstruction.filtering_cuda import CudaSinoFilter
    import pycuda.gpuarray as garray
if __has_pyopencl__:
    import pyopencl.array as parray
    from nabu.opencl.processing import OpenCLProcessing
    from nabu.reconstruction.filtering_opencl import OpenCLSinoFilter, __has_vkfft__

filters_to_test = ["ramlak", "shepp-logan", "tukey"]
padding_modes_to_test = ["constant", "edge"]
if __do_long_tests__:
    filters_to_test = ["ramlak", "shepp-logan", "cosine", "hamming", "hann", "tukey", "lanczos"]
    padding_modes_to_test = SinoFilter.available_padding_modes

tests_scenarios = generate_tests_scenarios(
    {
        "filter_name": filters_to_test,
        "padding_mode": padding_modes_to_test,
        "output_provided": [True, False],
        "truncated_sino": [True, False],
    }
)


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls
    cls.sino = get_data("mri_sino500.npz")["data"]
    cls.sino_truncated = np.ascontiguousarray(cls.sino[:, 160:-160])

    if __has_pycuda__:
        cls.ctx_cuda = get_cuda_context(cleanup_at_exit=False)
        cls.sino_cuda = garray.to_gpu(cls.sino)
        cls.sino_truncated_cuda = garray.to_gpu(cls.sino_truncated)
    if __has_pyopencl__:
        cls.cl = OpenCLProcessing(device_type="all")
        cls.sino_cl = parray.to_device(cls.cl.queue, cls.sino)
        cls.sino_truncated_cl = parray.to_device(cls.cl.queue, cls.sino_truncated)

    yield

    if __has_pycuda__:
        cls.ctx_cuda.pop()


@pytest.mark.usefixtures("bootstrap")
class TestSinoFilter:
    @pytest.mark.parametrize("config", tests_scenarios)
    def test_filter(self, config):
        sino = self.sino if not (config["truncated_sino"]) else self.sino_truncated

        sino_filter = SinoFilter(
            sino.shape,
            filter_name=config["filter_name"],
            padding_mode=config["padding_mode"],
        )
        if config["output_provided"]:
            output = np.zeros_like(sino)
        else:
            output = None
        res = sino_filter.filter_sino(sino, output=output)
        if output is not None:
            assert id(res) == id(output), "when providing output, return value must not change"

        ref = filter_sinogram(
            sino, sino_filter.dwidth_padded, filter_name=config["filter_name"], padding_mode=config["padding_mode"]
        )

        assert np.allclose(res, ref, atol=4e-6)

    @pytest.mark.skipif(not (__has_pycuda__), reason="Need Cuda + pycuda to use CudaSinoFilter")
    @pytest.mark.parametrize("config", tests_scenarios)
    def test_cuda_filter(self, config):
        sino = self.sino_cuda if not (config["truncated_sino"]) else self.sino_truncated_cuda
        h_sino = self.sino if not (config["truncated_sino"]) else self.sino_truncated

        sino_filter = CudaSinoFilter(
            sino.shape,
            filter_name=config["filter_name"],
            padding_mode=config["padding_mode"],
            cuda_options={"ctx": self.ctx_cuda},
        )
        if config["output_provided"]:
            output = garray.zeros(sino.shape, "f")
        else:
            output = None
        res = sino_filter.filter_sino(sino, output=output)
        if output is not None:
            assert id(res) == id(output), "when providing output, return value must not change"

        ref = filter_sinogram(
            h_sino, sino_filter.dwidth_padded, filter_name=config["filter_name"], padding_mode=config["padding_mode"]
        )

        assert np.allclose(res.get(), ref, atol=6e-5), "test_cuda_filter: something wrong with config=%s" % (
            str(config)
        )

    @pytest.mark.skipif(
        not (__has_pyopencl__ and __has_vkfft__), reason="Need OpenCL + pyopencl + pyvkfft to use OpenCLSinoFilter"
    )
    @pytest.mark.parametrize("config", tests_scenarios)
    def test_opencl_filter(self, config):
        sino = self.sino_cl if not (config["truncated_sino"]) else self.sino_truncated_cl
        h_sino = self.sino if not (config["truncated_sino"]) else self.sino_truncated

        sino_filter = OpenCLSinoFilter(
            sino.shape,
            filter_name=config["filter_name"],
            padding_mode=config["padding_mode"],
            opencl_options={"ctx": self.cl.ctx},
        )
        if config["output_provided"]:
            output = parray.zeros(self.cl.queue, sino.shape, "f")
        else:
            output = None
        res = sino_filter.filter_sino(sino, output=output)
        if output is not None:
            assert id(res) == id(output), "when providing output, return value must not change"

        ref = filter_sinogram(
            h_sino, sino_filter.dwidth_padded, filter_name=config["filter_name"], padding_mode=config["padding_mode"]
        )

        assert np.allclose(res.get(), ref, atol=6e-5), "test_opencl_filter: something wrong with config=%s" % (
            str(config)
        )
