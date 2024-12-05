import pytest
import numpy as np
import scipy.ndimage
from scipy import sparse
from nabu.io.detector_distortion import DetectorDistortionBase
from nabu.processing.rotation import Rotation, __have__skimage__

if __have__skimage__:
    import skimage


@pytest.mark.skipif(not (__have__skimage__), reason="Need scikit-image for rotation")
def test_detector_distortion():
    image = scipy.ndimage.gaussian_filter(np.random.random([379, 1357]), 3.0)
    center_xz = ((image.shape[1] - 1) / 2, (image.shape[0] - 1) / 2)

    part_to_be_retrieved = image[100:279]

    rotated_image = skimage.transform.rotate(image, angle=5.0, center=center_xz[::])

    corrector = DetectorDistortionRotation(detector_full_shape_vh=image.shape, center_xz=center_xz, angle_deg=-5.0)
    start_x, end_x, start_z, end_z = corrector.set_sub_region_transformation(
        target_sub_region=(
            None,
            None,
            100,
            279,
        )
    )

    source = rotated_image[start_z:end_z, start_x:end_x]

    retrieved = corrector.transform(source)

    diff = (retrieved - part_to_be_retrieved)[:, 20:-20]

    assert abs(diff).std() < 1e-3


class DetectorDistortionRotation(DetectorDistortionBase):
    """ """

    def __init__(self, detector_full_shape_vh=(0, 0), center_xz=(0, 0), angle_deg=0.0):
        """This is the basis class.
        A simple identity transformation which has the only merit to show
        how it works.Reimplement this function to have more parameters for other
        transformations
        """
        self._build_full_transformation(detector_full_shape_vh, center_xz, angle_deg)

    def _build_full_transformation(self, detector_full_shape_vh, center_xz, angle_deg):
        """A simple identity.
        Reimplement this function to have more parameters for other
        transformations
        """

        indices = np.indices(detector_full_shape_vh)
        center_x, center_z = center_xz
        coordinates = (indices.T - np.array([center_z, center_x])).T

        c = np.cos(np.deg2rad(angle_deg))
        s = np.sin(np.deg2rad(angle_deg))

        rot_mat = np.array([[c, s], [-s, c]])

        coordinates = np.tensordot(rot_mat, coordinates, axes=[1, 0])

        # padding
        sz, sx = detector_full_shape_vh
        total_detector_npixs = sz * sx
        xs = np.clip(np.array(coordinates[1].flat) + center_x, [[0]], [[sx - 1]])
        zs = np.clip(np.array(coordinates[0].flat) + center_z, [[0]], [[sz - 1]])

        ix0s = np.floor(xs)
        ix1s = np.ceil(xs)
        fx = xs - ix0s

        iz0s = np.floor(zs)
        iz1s = np.ceil(zs)
        fz = zs - iz0s

        I_tmp = np.empty([4 * sz * sx], np.int64)
        J_tmp = np.empty([4 * sz * sx], np.int64)
        V_tmp = np.ones([4 * sz * sx], "f")

        I_tmp[:] = np.arange(sz * sx * 4) // 4

        J_tmp[0::4] = iz0s * sx + ix0s
        J_tmp[1::4] = iz0s * sx + ix1s
        J_tmp[2::4] = iz1s * sx + ix0s
        J_tmp[3::4] = iz1s * sx + ix1s

        V_tmp[0::4] = (1 - fz) * (1 - fx)
        V_tmp[1::4] = (1 - fz) * fx
        V_tmp[2::4] = fz * (1 - fx)
        V_tmp[3::4] = fz * fx

        self.detector_full_shape_vh = detector_full_shape_vh

        coo_tmp = sparse.coo_matrix((V_tmp.astype("f"), (I_tmp, J_tmp)), shape=(sz * sx, sz * sx))

        csr_tmp = coo_tmp.tocsr()

        self.full_csr_data = csr_tmp.data
        self.full_csr_indices = csr_tmp.indices
        self.full_csr_indptr = csr_tmp.indptr

        ## This will be used to save time if the same sub_region argument is requested several time in a row
        self._status = None

    def _set_sub_region_transformation(
        self,
        target_sub_region=(
            (
                None,
                None,
                0,
                0,
            ),
        ),
    ):
        (x_start, x_end, z_start, z_end) = target_sub_region

        if z_start is None:
            z_start = 0
        if z_end is None:
            z_end = self.detector_full_shape_vh[0]

        if (x_start, x_end) not in [(None, None), (0, None), (0, self.detector_full_shape_vh[1])]:
            message = f""" In the base class DetectorDistortionRotation only vertical slicing is accepted.
            The sub_region contained (x_start, x_end)={(x_start, x_end)} which would slice the 
            full horizontal size which is {self.detector_full_shape_vh[1]}
            """
            raise ValueError()

        x_start, x_end = 0, self.detector_full_shape_vh[1]

        row_ptr_start = z_start * self.detector_full_shape_vh[1]
        row_ptr_end = z_end * self.detector_full_shape_vh[1]

        indices_start = self.full_csr_indptr[row_ptr_start]
        indices_end = self.full_csr_indptr[row_ptr_end]

        data_tmp = self.full_csr_data[indices_start:indices_end]

        target_offset = self.full_csr_indptr[row_ptr_start]
        indptr_tmp = self.full_csr_indptr[row_ptr_start : row_ptr_end + 1] - target_offset

        indices_tmp = self.full_csr_indices[indices_start:indices_end]

        iz_source = (indices_tmp) // self.detector_full_shape_vh[1]

        z_start_source = iz_source.min()
        z_end_source = iz_source.max() + 1
        source_offset = z_start_source * self.detector_full_shape_vh[1]
        indices_tmp = indices_tmp - source_offset

        target_size = (z_end - z_start) * self.detector_full_shape_vh[1]
        source_size = (z_end_source - z_start_source) * self.detector_full_shape_vh[1]

        self.transformation_matrix = sparse.csr_matrix(
            (data_tmp, indices_tmp, indptr_tmp), shape=(target_size, source_size)
        )

        self.target_shape = ((z_end - z_start), self.detector_full_shape_vh[1])

        ## For the identity matrix the source and the target have the same size.
        ## The two following lines are trivial.
        ## For this identity transformation only the slicing of the appropriate part
        ## of the identity sparse matrix is slightly laborious.
        ## Practical case will be more complicated and source_sub_region
        ## will be in general larger than the target_sub_region
        self._status = {
            "target_sub_region": ((x_start, x_end, z_start, z_end)),
            "source_sub_region": ((x_start, x_end, z_start_source, z_end_source)),
        }

        return self._status["source_sub_region"]
