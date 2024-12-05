import pytest
import numpy as np
from nabu.testutils import get_data, __do_long_tests__

from nabu.cuda.utils import __has_pycuda__
from nabu.reconstruction.mlem import MLEMReconstructor, __have_corrct__


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls
    datafile = get_data("sl_mlem.npz")
    cls.data = datafile["data"]
    cls.angles_rad = datafile["angles_rad"]
    cls.random_u_shifts = datafile["random_u_shifts"]
    cls.ref_rec_noshifts = datafile["ref_rec_noshifts"]
    cls.ref_rec_shiftsu = datafile["ref_rec_shiftsu"]
    cls.ref_rec_u_rand = datafile["ref_rec_u_rand"]
    cls.ref_rec_shiftsv = datafile["ref_rec_shiftsv"]
    # cls.ref_rec_v_rand = datafile["ref_rec_v_rand"]
    cls.tol = 2e-4


@pytest.mark.skipif(not (__has_pycuda__ and __have_corrct__), reason="Need pycuda and corrct for this test")
@pytest.mark.usefixtures("bootstrap")
class TestMLEM:
    """These tests test the general MLEM reconstruction algorithm
    and the behavior of the reconstruction with respect to horizontal shifts.
    Only horizontal shifts are tested here because vertical shifts are handled outside
    the reconstruction object, but in the embedding reconstruction pipeline. See FullFieldReconstructor"""

    def _create_MLEM_reconstructor(self, shifts_uv=None):
        return MLEMReconstructor(
            self.data.shape, -self.angles_rad, shifts_uv, cor=0.0, n_iterations=10  # mind the sign
        )

    def test_simple_mlem_recons(self):
        R = self._create_MLEM_reconstructor()
        rec = R.reconstruct(self.data)
        delta = np.abs(rec[:, ::-1, :] - self.ref_rec_noshifts)
        assert np.max(delta) < self.tol

    def test_mlem_recons_with_u_shifts(self):
        shifts = np.zeros((len(self.angles_rad), 2))
        shifts[:, 0] = -5
        R = self._create_MLEM_reconstructor(shifts)
        rec = R.reconstruct(self.data)
        delta = np.abs(rec[:, ::-1] - self.ref_rec_shiftsu)
        assert np.max(delta) < self.tol

    def test_mlem_recons_with_random_u_shifts(self):
        R = self._create_MLEM_reconstructor(self.random_u_shifts)
        rec = R.reconstruct(self.data)
        delta = np.abs(rec[:, ::-1] - self.ref_rec_u_rand)
        assert np.max(delta) < self.tol

    def test_mlem_recons_with_constant_v_shifts(self):
        from nabu.preproc.shift import VerticalShift

        shifts = np.zeros((len(self.angles_rad), 2))
        shifts[:, 1] = -20

        nv, n_angles, nu = self.data.shape
        radios_movements = VerticalShift(
            (n_angles, nv, nu), -shifts[:, 1]
        )  # Minus sign here mimics what is  done in the pipeline.
        tmp_in = np.swapaxes(self.data, 0, 1).copy()
        tmp_out = np.zeros_like(tmp_in)
        radios_movements.apply_vertical_shifts(tmp_in, list(range(n_angles)), output=tmp_out)
        data = np.swapaxes(tmp_out, 0, 1).copy()

        R = self._create_MLEM_reconstructor(shifts)
        rec = R.reconstruct(data)

        axslice = 120
        trslice = 84
        axslice1 = self.ref_rec_shiftsv[axslice]
        axslice2 = rec[axslice, ::-1]
        trslice1 = self.ref_rec_shiftsv[trslice]
        trslice2 = rec[trslice, ::-1]
        # delta = np.abs(rec[:, ::-1] - self.ref_rec_shiftsv)
        delta_ax = np.abs(axslice1 - axslice2)
        delta_tr = np.abs(trslice1 - trslice2)
        assert max(np.max(delta_ax), np.max(delta_tr)) < self.tol

    @pytest.mark.skip(reason="No valid reference reconstruction for this test.")
    def test_mlem_recons_with_random_v_shifts(self):
        """NOT YET IMPLEMENTED.
        This is a temporary version due to unpexcted behavior of CorrCT/Astra to
        compute a reference implementation. See [question on Astra's github](https://github.com/astra-toolbox/astra-toolbox/discussions/520).
        """
