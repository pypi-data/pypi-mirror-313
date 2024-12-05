from multiprocessing.pool import ThreadPool
from bisect import bisect_left
import numpy as np
from ..io.reader import load_images_from_dataurl_dict
from ..utils import check_supported, deprecated_class, get_num_threads


class FlatFieldArrays:
    """
    A class for flat-field normalization
    """

    # the variable below will be True for the derived class
    # which is taylored for to helical case
    _full_shape = False

    _supported_interpolations = ["linear", "nearest"]

    def __init__(
        self,
        radios_shape: tuple,
        flats,
        darks,
        radios_indices=None,
        interpolation: str = "linear",
        distortion_correction=None,
        nan_value=1.0,
        radios_srcurrent=None,
        flats_srcurrent=None,
        n_threads=None,
    ):
        """
        Initialize a flat-field normalization process.

        Parameters
        ----------
        radios_shape: tuple
            A tuple describing the shape of the radios stack, in the form
            `(n_radios, n_z, n_x)`.
        flats: dict
            Dictionary where each key is the flat index, and the value is a
            numpy.ndarray of the flat image.
        darks: dict
            Dictionary where each key is the dark index, and the value is a
            numpy.ndarray of the dark image.
        radios_indices: array of int, optional
            Array containing the radios indices in the scan. `radios_indices[0]` is the index
            of the first radio, and so on.
        interpolation: str, optional
            Interpolation method for flat-field. See below for more details.
        distortion_correction: DistortionCorrection, optional
            A DistortionCorrection object. If provided, it is used to correct flat distortions based on each radio.
        nan_value: float, optional
            Which float value is used to replace nan/inf after flat-field.
        radios_srcurrent: array, optional
            Array with the same shape as radios_indices. Each item contains the synchrotron electric current.
            If not None, normalization with current is applied.
            Please refer to "Notes" for more information on this normalization.
        flats_srcurrent: array, optional
            Array with the same length as "flats". Each item is a measurement of the synchrotron electric current
            for the corresponding flat. The items must be ordered in the same order as the flats indices (`flats.keys()`).
            This parameter must be used along with 'radios_srcurrent'.
            Please refer to "Notes" for more information on this normalization.
        n_threads: int or None, optional
            Number of threads to use for flat-field correction. Default is to use half the threads.

        Important
        ----------
        `flats` and `darks` are expected to be a dictionary with integer keys (the flats/darks indices)
        and numpy array values.
        You can use the following helper functions: `nabu.io.reader.load_images_from_dataurl_dict`
        and `nabu.io.utils.create_dict_of_indices`


        Notes
        ------
        Usually, when doing a scan, only one or a few darks/flats are acquired.
        However, the flat-field normalization has to be performed on each radio,
        although incoming beam can fluctuate between projections.
        The usual way to overcome this is to interpolate between flats.
        If interpolation="nearest", the first flat is used for the first
        radios subset, the second flat is used for the second radios subset,
        and so on.
        If interpolation="linear", the normalization is done as a linear
        function of the radio index.

        The normalization with synchrotron electric current is done as follows.
        Let s = sr/sr_max denote the ratio between current and maximum current,
        D be the dark-current frame, and X' be the normalized frame. Then:
          srcurrent_normalization(X) = X' = (X - D)/s + D
          flatfield_normalization(X') = (X' - D)/(F' - D) = (X - D) / (F - D) * sF/sX
        So current normalization boils down to a scalar multiplication after flat-field.
        """
        if self._full_shape:
            # this is never going to happen in this base class. But in the derived class for helical
            # which needs to keep the full shape
            if radios_indices is not None:
                radios_shape = (len(radios_indices),) + radios_shape[1:]

        self._set_parameters(radios_shape, radios_indices, interpolation, nan_value)
        self._set_flats_and_darks(flats, darks)
        self._precompute_flats_indices_weights()
        self._configure_srcurrent_normalization(radios_srcurrent, flats_srcurrent)
        self.distortion_correction = distortion_correction
        self.n_threads = min(1, get_num_threads(n_threads) // 2)

    def _set_parameters(self, radios_shape, radios_indices, interpolation, nan_value):
        self._set_radios_shape(radios_shape)
        if radios_indices is None:
            radios_indices = np.arange(0, self.n_radios, dtype=np.int32)
        else:
            radios_indices = np.array(radios_indices, dtype=np.int32)
            self._check_radios_and_indices_congruence(radios_indices)

        self.radios_indices = radios_indices
        self.interpolation = interpolation
        check_supported(interpolation, self._supported_interpolations, "Interpolation mode")
        self.nan_value = nan_value
        self._radios_idx_to_pos = dict(zip(self.radios_indices, np.arange(self.radios_indices.size)))

    def _set_radios_shape(self, radios_shape):
        if len(radios_shape) == 2:
            self.radios_shape = (1,) + radios_shape
        elif len(radios_shape) == 3:
            self.radios_shape = radios_shape
        else:
            raise ValueError("Expected radios to have 2 or 3 dimensions")
        n_radios, n_z, n_x = self.radios_shape
        self.n_radios = n_radios
        self.n_angles = n_radios
        self.shape = (n_z, n_x)

    def _set_flats_and_darks(self, flats, darks):
        self._check_frames(flats, "flats", 1, 9999)
        self.n_flats = len(flats)
        self.flats = flats
        self._sorted_flat_indices = sorted(self.flats.keys())

        if self._full_shape:
            # this is never going to happen in this base class. But in the derived class for helical
            # which needs to keep the full shape
            self.shape = flats[self._sorted_flat_indices[0]].shape

        self._flat2arrayidx = dict(zip(self._sorted_flat_indices, np.arange(self.n_flats)))
        self.flats_arr = np.zeros((self.n_flats,) + self.shape, "f")
        for i, idx in enumerate(self._sorted_flat_indices):
            self.flats_arr[i] = self.flats[idx]

        self._check_frames(darks, "darks", 1, 1)
        self.darks = darks
        self.n_darks = len(darks)
        self._sorted_dark_indices = sorted(self.darks.keys())
        self._dark = None

    def _check_frames(self, frames, frames_type, min_frames_required, max_frames_supported):
        n_frames = len(frames)
        if n_frames < min_frames_required:
            raise ValueError("Need at least %d %s" % (min_frames_required, frames_type))
        if n_frames > max_frames_supported:
            raise ValueError(
                "Flat-fielding with more than %d %s is not supported" % (max_frames_supported, frames_type)
            )
        self._check_frame_shape(frames, frames_type)

    def _check_frame_shape(self, frames, frames_type):
        for frame_idx, frame in frames.items():
            if frame.shape != self.shape:
                raise ValueError(
                    "Invalid shape for %s %s: expected %s, but got %s"
                    % (frames_type, frame_idx, str(self.shape), str(frame.shape))
                )

    def _check_radios_and_indices_congruence(self, radios_indices):
        if radios_indices.size != self.n_radios:
            raise ValueError(
                "Expected radios_indices to have length %s = n_radios, but got length %d"
                % (self.n_radios, radios_indices.size)
            )

    def _precompute_flats_indices_weights(self):
        """
        Build two arrays: "indices" and "weights".
        These arrays contain pre-computed information so that the interpolated flat is obtained with

           flat_interpolated = weight_prev * flat_prev  + weight_next * flat_next

        where
           weight_prev, weight_next = weights[2*i], weights[2*i+1]
           idx_prev, idx_next = indices[2*i], indices[2*i+1]
           flat_prev, flat_next = flats[idx_prev], flats[idx_next]

        In words:
          - If a projection has an index between two flats, the equivalent flat is a linear interpolation
            between "previous flat" and "next flat".
          - If a projection has the same index as a flat, only this flat is used for normalization
            (this case normally never occurs, but it's handled in the code)
        """

        def _interp_linear(idx, prev_next):
            if len(prev_next) == 1:  # current index corresponds to an acquired flat
                weights = (1, 0)
                f_idx = (self._flat2arrayidx[prev_next[0]], -1)
            else:
                prev_idx, next_idx = prev_next
                delta = next_idx - prev_idx
                w1 = 1 - (idx - prev_idx) / delta
                w2 = 1 - (next_idx - idx) / delta
                weights = (w1, w2)
                f_idx = (self._flat2arrayidx[prev_idx], self._flat2arrayidx[next_idx])
            return f_idx, weights

        def _interp_nearest(idx, prev_next):
            if len(prev_next) == 1:  # current index corresponds to an acquired flat
                weights = (1, 0)
                f_idx = (self._flat2arrayidx[prev_next[0]], -1)
            else:
                prev_idx, next_idx = prev_next
                idx_to_take = prev_idx if abs(idx - prev_idx) < abs(idx - next_idx) else next_idx
                weights = (1, 0)
                f_idx = (self._flat2arrayidx[idx_to_take], -1)
            return f_idx, weights

        self.flats_idx = np.zeros((self.n_radios, 2), dtype=np.int32)
        self.flats_weights = np.zeros((self.n_radios, 2), dtype=np.float32)
        for i, idx in enumerate(self.radios_indices):
            prev_next = self.get_previous_next_indices(self._sorted_flat_indices, idx)
            if self.interpolation == "nearest":
                f_idx, weights = _interp_nearest(idx, prev_next)
            elif self.interpolation == "linear":
                f_idx, weights = _interp_linear(idx, prev_next)
            # pylint: disable=E0606
            self.flats_idx[i] = f_idx
            self.flats_weights[i] = weights

    # pylint: disable=E1307
    def _configure_srcurrent_normalization(self, radios_srcurrent, flats_srcurrent):
        self.normalize_srcurrent = False
        if radios_srcurrent is None or flats_srcurrent is None:
            return
        radios_srcurrent = np.array(radios_srcurrent)
        if radios_srcurrent.size != self.n_radios:
            raise ValueError(
                "Expected 'radios_srcurrent' to have %d elements but got %d" % (self.n_radios, radios_srcurrent.size)
            )
        flats_srcurrent = np.array(flats_srcurrent)
        if flats_srcurrent.size != self.n_flats:
            raise ValueError(
                "Expected 'flats_srcurrent' to have %d elements but got %d" % (self.n_flats, flats_srcurrent.size)
            )
        self.normalize_srcurrent = True
        self.radios_srcurrent = radios_srcurrent
        self.flats_srcurrent = flats_srcurrent
        self.srcurrent_ratios = np.zeros(self.n_radios, "f")
        # Flats SRCurrent is obtained with "nearest" interp, to emulate an already-done flats SR current normalization
        for i, radio_idx in enumerate(self.radios_indices):
            flat_idx = self.get_nearest_index(self._sorted_flat_indices, radio_idx)
            flat_srcurrent = self.flats_srcurrent[self._flat2arrayidx[flat_idx]]
            self.srcurrent_ratios[i] = flat_srcurrent / self.radios_srcurrent[i]

    @staticmethod
    def get_previous_next_indices(arr, idx):
        pos = bisect_left(arr, idx)
        if pos == len(arr):  # outside range
            return (arr[-1],)
        if arr[pos] == idx:
            return (idx,)
        if pos == 0:
            return (arr[0],)
        return arr[pos - 1], arr[pos]

    @staticmethod
    def get_nearest_index(arr, idx):
        pos = bisect_left(arr, idx)
        if pos == len(arr) or arr[pos] == idx:
            return arr[-1]
        return arr[pos - 1] if idx - arr[pos - 1] < arr[pos] - idx else arr[pos]

    @staticmethod
    def interp(pos, indices, weights, array, slice_y=slice(None, None), slice_x=slice(None, None)):
        """
        Interpolate between two values. The interpolator consists in pre-computed arrays such that

           prev, next = indices[pos]
           w1, w2 = weights[pos]
           interpolated_value = w1 * array[prev] + w2 * array[next]
        """
        prev_idx = indices[pos, 0]
        next_idx = indices[pos, 1]

        if slice_y != slice(None, None) or slice_x != slice(None, None):
            w1 = weights[pos, 0][slice_y, slice_x]
            w2 = weights[pos, 1][slice_y, slice_x]
        else:
            w1 = weights[pos, 0]
            w2 = weights[pos, 1]

        if next_idx == -1:
            val = array[prev_idx]
        else:
            val = w1 * array[prev_idx] + w2 * array[next_idx]
        return val

    def get_flat(self, pos, dtype=np.float32, slice_y=slice(None, None), slice_x=slice(None, None)):
        flat = self.interp(pos, self.flats_idx, self.flats_weights, self.flats_arr, slice_y=slice_y, slice_x=slice_x)
        if flat.dtype != dtype:
            flat = np.ascontiguousarray(flat, dtype=dtype)
        return flat

    def get_dark(self):
        if self._dark is None:
            first_dark_idx = self._sorted_dark_indices[0]
            dark = np.ascontiguousarray(self.darks[first_dark_idx], dtype=np.float32)
            self._dark = dark
        return self._dark

    def remove_invalid_values(self, img):
        if self.nan_value is None:
            return
        invalid_mask = np.logical_not(np.isfinite(img))
        img[invalid_mask] = self.nan_value

    def normalize_radios(self, radios):
        """
        Apply a flat-field normalization, with the current parameters, to a stack
        of radios.
        The processing is done in-place, meaning that the radios content is overwritten.

        Parameters
        -----------
        radios: numpy.ndarray
            Radios chunk
        """
        do_flats_distortion_correction = self.distortion_correction is not None
        dark = self.get_dark()

        def apply_flatfield(i):
            radio_data = radios[i]
            radio_data -= dark
            flat = self.get_flat(i)
            flat = flat - dark
            if do_flats_distortion_correction:
                flat = self.distortion_correction.estimate_and_correct(flat, radio_data)
            np.divide(radio_data, flat, out=radio_data)
            self.remove_invalid_values(radio_data)

        if self.n_threads > 2:
            with ThreadPool(self.n_threads) as tp:
                tp.map(apply_flatfield, range(self.n_radios))
        else:
            for i in range(self.n_radios):
                apply_flatfield(i)

        if self.normalize_srcurrent:
            radios *= self.srcurrent_ratios[:, np.newaxis, np.newaxis]
        return radios

    def normalize_single_radio(
        self, radio, radio_idx, dtype=np.float32, slice_y=slice(None, None), slice_x=slice(None, None)
    ):
        """
        Apply a flat-field normalization to a single projection image.
        """
        dark = self.get_dark()[slice_y, slice_x]
        radio -= dark
        radio_pos = self._radios_idx_to_pos[radio_idx]
        flat = self.get_flat(radio_pos, dtype=dtype, slice_y=slice_y, slice_x=slice_x)
        flat = flat - dark
        if self.distortion_correction is not None:
            flat = self.distortion_correction.estimate_and_correct(flat, radio)
        radio /= flat
        if self.normalize_srcurrent:
            radio *= self.srcurrent_ratios[radio_pos]
        self.remove_invalid_values(radio)
        return radio


FlatField = FlatFieldArrays


@deprecated_class(
    "FlatFieldDataUrls is deprecated since 2024.2.0 and will be removed in a future version", do_print=True
)
class FlatFieldDataUrls(FlatField):
    def __init__(
        self,
        radios_shape: tuple,
        flats: dict,
        darks: dict,
        radios_indices=None,
        interpolation: str = "linear",
        distortion_correction=None,
        nan_value=1.0,
        radios_srcurrent=None,
        flats_srcurrent=None,
        **chunk_reader_kwargs,
    ):
        """
        Initialize a flat-field normalization process with DataUrls.

        Parameters
        ----------
        radios_shape: tuple
            A tuple describing the shape of the radios stack, in the form
            `(n_radios, n_z, n_x)`.
        flats: dict
            Dictionary where the key is the flat index, and the value is a
            silx.io.DataUrl pointing to the flat.
        darks: dict
            Dictionary where the key is the dark index, and the value is a
            silx.io.DataUrl pointing to the dark.
        radios_indices: array, optional
            Array containing the radios indices. `radios_indices[0]` is the index
            of the first radio, and so on.
        interpolation: str, optional
            Interpolation method for flat-field. See below for more details.
        distortion_correction: DistortionCorrection, optional
            A DistortionCorrection object. If provided, it is used to correct flat distortions based on each radio.
        nan_value: float, optional
            Which float value is used to replace nan/inf after flat-field.


        Other Parameters
        ----------------
        The other named parameters are passed to ChunkReader(). Please read its
        documentation for more information.

        Notes
        ------
        Usually, when doing a scan, only one or a few darks/flats are acquired.
        However, the flat-field normalization has to be performed on each radio,
        although incoming beam can fluctuate between projections.
        The usual way to overcome this is to interpolate between flats.
        If interpolation="nearest", the first flat is used for the first
        radios subset, the second flat is used for the second radios subset,
        and so on.
        If interpolation="linear", the normalization is done as a linear
        function of the radio index.
        """

        flats_arrays_dict = load_images_from_dataurl_dict(flats, **chunk_reader_kwargs)
        darks_arrays_dict = load_images_from_dataurl_dict(darks, **chunk_reader_kwargs)
        super().__init__(
            radios_shape,
            flats_arrays_dict,
            darks_arrays_dict,
            radios_indices=radios_indices,
            interpolation=interpolation,
            distortion_correction=distortion_correction,
            nan_value=nan_value,
            radios_srcurrent=radios_srcurrent,
            flats_srcurrent=flats_srcurrent,
        )
