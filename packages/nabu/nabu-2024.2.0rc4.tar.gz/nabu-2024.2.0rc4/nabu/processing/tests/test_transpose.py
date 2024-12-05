import numpy as np
import pytest
from nabu.cuda.utils import get_cuda_context, __has_pycuda__
from nabu.opencl.utils import __has_pyopencl__, get_opencl_context
from nabu.testutils import get_data, generate_tests_scenarios, __do_long_tests__
from nabu.processing.transpose import CudaTranspose, OpenCLTranspose

configs = {
    "shape": [(300, 451), (300, 300), (255, 300)],
    "output_is_none": [True, False],
    "dtype_in_out": [(np.float32, np.float32)],
}

if __do_long_tests__:
    configs["dtype_in_out"].extend(
        [(np.float32, np.complex64), (np.complex64, np.complex64), (np.uint8, np.uint16), (np.uint8, np.int32)]
    )

scenarios = generate_tests_scenarios(configs)


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls
    cls.data = get_data("chelsea.npz")["data"]
    cls.tol = 1e-7
    if __has_pycuda__:
        cls.cu_ctx = get_cuda_context(cleanup_at_exit=False)
    if __has_pyopencl__:
        cls.cl_ctx = get_opencl_context(device_type="all")
    yield
    if __has_pycuda__:
        cls.cu_ctx.pop()


@pytest.mark.usefixtures("bootstrap")
class TestTranspose:
    def _do_test_transpose(self, config, transpose_cls):
        shape = config["shape"]
        dtype = config["dtype_in_out"][0]
        dtype_out = config["dtype_in_out"][1]
        data = np.ascontiguousarray(self.data[: shape[0], : shape[1]], dtype=dtype)

        backend = transpose_cls.backend
        if backend == "opencl" and not (np.iscomplexobj(dtype(1))) and np.iscomplexobj(dtype_out(1)):
            pytest.skip("pyopencl does not support real to complex scalar cast")
        ctx = self.cu_ctx if backend == "cuda" else self.cl_ctx
        backend_options = {"ctx": ctx}
        transpose = transpose_cls(data.shape, dtype, dst_dtype=dtype_out, **backend_options)

        d_data = transpose.processing.allocate_array("data", shape, dtype)
        d_data.set(data)
        if config["output_is_none"]:
            d_out = None
        else:
            d_out = transpose.processing.allocate_array("output", shape[::-1], dtype_out)

        d_res = transpose(d_data, dst=d_out)

        assert (
            np.max(np.abs(d_res.get() - data.T)) == 0
        ), "something wrong with transpose(shape=%s, dtype=%s, dtype_out=%s)" % (shape, dtype, dtype_out)

    @pytest.mark.skipif(not (__has_pycuda__), reason="Need pycuda for this test")
    @pytest.mark.parametrize("config", scenarios)
    def test_cuda_transpose(self, config):
        self._do_test_transpose(config, CudaTranspose)

    @pytest.mark.skipif(not (__has_pyopencl__), reason="Need pyopencl for this test")
    @pytest.mark.parametrize("config", scenarios)
    def test_opencl_transpose(self, config):
        self._do_test_transpose(config, OpenCLTranspose)
