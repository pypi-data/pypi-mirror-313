import numpy as np
import pytest
from nabu.testutils import get_data
from nabu.cuda.utils import __has_pycuda__

if __has_pycuda__:
    import pycuda.gpuarray as garray

    # from pycuda.cumath import fabs
    from pycuda.elementwise import ElementwiseKernel
    from nabu.cuda.utils import get_cuda_context
    from nabu.reconstruction.projection import Projector
    from nabu.reconstruction.fbp import Backprojector
try:
    import astra

    __has_astra__ = True
except ImportError:
    __has_astra__ = False


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls
    cls.image = get_data("brain_phantom.npz")["data"]
    cls.sino_ref = get_data("mri_sino500.npz")["data"]
    cls.n_angles, cls.dwidth = cls.sino_ref.shape
    cls.rtol = 1e-3
    if __has_pycuda__:
        cls.ctx = get_cuda_context()


@pytest.mark.skipif(not (__has_pycuda__), reason="Need pycuda for this test")
@pytest.mark.usefixtures("bootstrap")
class TestProjection:
    def check_result(self, img1, img2, err_msg):
        max_diff = np.max(np.abs(img1 - img2))
        assert max_diff / img1.max() < self.rtol, err_msg + " : max diff = %.3e" % max_diff

    def test_proj_simple(self):
        P = Projector(self.image.shape, self.n_angles)
        res = P(self.image)
        self.check_result(res, self.sino_ref, "Something wrong with simple projection")

    def test_input_output_kinds(self):
        P = Projector(self.image.shape, self.n_angles)

        # input on GPU, output on CPU
        d_img = garray.to_gpu(self.image)
        res = P(d_img)
        self.check_result(res, self.sino_ref, "Something wrong: input GPU, output CPU")

        # input on CPU, output on GPU
        out = garray.zeros(P.sino_shape, "f")
        res = P(self.image, output=out)
        self.check_result(out.get(), self.sino_ref, "Something wrong: input CPU, output GPU")

        # input and output on GPU
        out.fill(0)
        P(d_img, output=out)
        self.check_result(out.get(), self.sino_ref, "Something wrong: input GPU, output GPU")

    def test_odd_size(self):
        image = self.image[:511, :]
        P = Projector(image.shape, self.n_angles - 1)
        res = P(image)

    @pytest.mark.skipif(not (__has_astra__), reason="Need astra-toolbox for this test")
    def test_against_astra(self):
        def proj_astra(img, angles, rot_center=None):
            vol_geom = astra.create_vol_geom(img.shape)
            if np.isscalar(angles):
                angles = np.linspace(0, np.pi, angles, False)
            proj_geom = astra.create_proj_geom("parallel", 1.0, img.shape[-1], angles)
            if rot_center is not None:
                cor_shift = (img.shape[-1] - 1) / 2.0 - rot_center
                proj_geom = astra.geom_postalignment(proj_geom, cor_shift)

            projector_id = astra.create_projector("cuda", proj_geom, vol_geom)
            sinogram_id, sinogram = astra.create_sino(img, projector_id)

            astra.data2d.delete(sinogram_id)
            astra.projector.delete(projector_id)
            return sinogram

        # Center of rotation to test
        cors = [None, 255.5, 256, 260, 270.2, 300, 150]

        for cor in cors:
            res_astra = proj_astra(self.image, 500, rot_center=cor)
            res_nabu = Projector(self.image.shape, 500, rot_center=cor).projection(self.image)
            self.check_result(res_nabu, res_astra, "Projection with CoR = %s" % str(cor))

    @pytest.mark.skipif(not (__has_astra__), reason="Need astra-toolbox for this test")
    def test_em_reconstruction(self):
        """
        Test iterative reconstruction: Maximum Likelyhood Expectation Maximization (MLEM)
        """

        subsampling = 5
        sino = self.sino_ref[::subsampling, :]

        P = Projector(self.image.shape, sino.shape[0])
        B = Backprojector(sino.shape, padding_mode="edge", extra_options={"centered_axis": True})

        d_sino = garray.to_gpu(np.ascontiguousarray(sino))

        def EM(sino, P, B, n_it, eps=1e-6):
            ones = np.ones(sino.shape, "f")
            oinv = garray.to_gpu((1.0 / B.backproj(ones)).astype("f"))
            x = garray.ones_like(oinv)
            y = garray.zeros_like(x)
            proj = garray.zeros_like(sino)
            proj_inv = sino.copy()

            update_projection = ElementwiseKernel(
                "float* proj_inv, float* proj, float* proj_data, float eps",
                "proj_inv[i] = proj_data[i] / ((fabsf(proj[i]) > eps) ? (proj[i]) : (1.0f))",
                "update_projection",
            )
            for k in range(n_it):
                # proj = P(x)
                P.projection(x, output=proj)

                update_projection(proj_inv, proj, sino, eps)

                # x *= B(proj_inv) * oinv
                B.backproj(proj_inv, output=y)
                x *= y
                x *= oinv
            return x

        rec = EM(d_sino, P, B, 50)

        def EM_astra(sino, rec_shape, n_it):
            vol_geom = astra.create_vol_geom(rec_shape)
            proj_geom = astra.create_proj_geom(
                "parallel", 1.0, sino.shape[-1], np.linspace(0, np.pi, sino.shape[0], False)
            )

            rec_id = astra.data2d.create("-vol", vol_geom)
            sinogram_id = astra.data2d.create("-sino", proj_geom)
            astra.data2d.store(sinogram_id, sino)
            astra.data2d.store(rec_id, np.ones(rec_shape, "f"))  # !

            cfg = astra.astra_dict("EM_CUDA")
            cfg["ReconstructionDataId"] = rec_id
            cfg["ProjectionDataId"] = sinogram_id

            alg_id = astra.algorithm.create(cfg)
            astra.algorithm.run(alg_id, n_it)

            rec = astra.data2d.get(rec_id)

            astra.algorithm.delete(alg_id)
            astra.data2d.delete(rec_id)
            astra.data2d.delete(sinogram_id)

            return rec

        ref = EM_astra(sino, self.image.shape, 50)

        err_max = np.max(np.abs(rec.get() - ref))
        assert err_max < 0.2, "Discrepancy between EM and EM_astra"
