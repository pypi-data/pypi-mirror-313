import numpy as np


try:
    import corrct as cct

    __have_corrct__ = True
except ImportError:
    __have_corrct__ = False


class MLEMReconstructor:
    """
    A reconstructor for MLEM reconstruction using the CorrCT toolbox.
    """

    default_extra_options = {
        "compute_shifts": False,
        "tomo_consistency": False,
        "v_min_for_v_shifts": 0,
        "v_max_for_v_shifts": None,
        "v_min_for_u_shifts": 0,
        "v_max_for_u_shifts": None,
    }

    def __init__(
        self,
        sinos_shape,
        angles_rad,
        shifts_uv=None,
        cor=None,
        n_iterations=50,
        extra_options=None,
    ):
        """ """
        if not (__have_corrct__):
            raise ImportError("Need corrct package")
        self.angles_rad = angles_rad
        self.n_iterations = n_iterations

        self._configure_extra_options(extra_options)
        self._set_sino_shape(sinos_shape)
        self._set_shifts(shifts_uv, cor)

    def _configure_extra_options(self, extra_options):
        self.extra_options = self.default_extra_options.copy()
        self.extra_options.update(extra_options or {})

    def _set_sino_shape(self, sinos_shape):
        if len(sinos_shape) != 3:
            raise ValueError("Expected a 3D shape")
        self.sinos_shape = sinos_shape
        self.n_sinos, self.n_angles, self.prj_width = sinos_shape
        if self.n_angles != len(self.angles_rad):
            raise ValueError(
                f"Number of angles ({len(self.angles_rad)}) does not match size of sinograms ({self.n_angles})."
            )

    def _set_shifts(self, shifts_uv, cor):
        if shifts_uv is None:
            self.shifts_uv = np.zeros([self.n_angles, 2])
        else:
            if shifts_uv.shape[0] != self.n_angles:
                raise ValueError(
                    f"Number of shifts given ({shifts_uv.shape[0]}) does not mathc the number of projections ({self.n_angles})."
                )
            self.shifts_uv = shifts_uv.copy()
        self.cor = cor

    def reconstruct(self, data_vwu):
        """
        data_align_vwu: numpy.ndarray or pycuda.gpuarray
            Raw data, with shape (n_sinograms, n_angles, width)
        output: optional
            Output array. If not provided, a new numpy array is returned
        """
        if not isinstance(data_vwu, np.ndarray):
            data_vwu = data_vwu.get()
        data_vwu /= data_vwu.mean()

        # MLEM recons
        self.vol_geom_align = cct.models.VolumeGeometry.get_default_from_data(data_vwu)
        self.prj_geom_align = cct.models.ProjectionGeometry.get_default_parallel()
        # Vertical shifts were handled in pipeline. Set them to ZERO
        self.shifts_uv[:, 1] = 0.0
        self.prj_geom_align.set_detector_shifts_vu(self.shifts_uv.T[::-1])

        variances_align = cct.processing.compute_variance_poisson(data_vwu)
        self.weights_align = cct.processing.compute_variance_weight(variances_align, normalized=True)  # , use_std=True
        self.data_term_align = cct.data_terms.DataFidelity_wl2(self.weights_align)
        solver = cct.solvers.MLEM(verbose=True, data_term=self.data_term_align)
        self.solver_opts = dict(lower_limit=0)  # , x_mask=cct.processing.circular_mask(vol_geom_align.shape_xyz[:-2])

        with cct.projectors.ProjectorUncorrected(
            self.vol_geom_align, self.angles_rad, rot_axis_shift_pix=self.cor, prj_geom=self.prj_geom_align
        ) as A:
            rec, _ = solver(A, data_vwu, iterations=self.n_iterations, **self.solver_opts)

        return rec
