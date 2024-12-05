from .reader import *


class ChunkReaderHelical(ChunkReader):
    """implements reading by projections subsets"""

    def _set_subregion(self, sub_region):
        super()._set_subregion(sub_region)
        ###########
        # undo the chun_size setting of the base class
        # to avoid allocation of Tera bytes in the helical case
        self.chunk_shape = (1,) + self.shape

    def set_data_buffer(self, data_buffer, pre_allocate=False):
        if data_buffer is not None:
            # overwrite out_dtype
            self.files_data = data_buffer
            self.out_dtype = data_buffer.dtype
            if data_buffer.shape[1:] != self.shape:
                raise ValueError("Expected shape %s but got %s" % (self.shape, data_buffer.shape))
        if pre_allocate:
            self.files_data = np.zeros(self.chunk_shape, dtype=self.out_dtype)

        if (self.binning is not None) and (np.dtype(self.out_dtype).kind in ["u", "i"]):
            raise ValueError(
                "Output datatype cannot be integer when using binning. Please set the 'convert_float' parameter to True or specify a 'data_buffer'."
            )

    def get_binning(self):
        if self.binning is None:
            return 1, 1
        else:
            return self.binning

    def _load_single(self, sub_total_prange_slice=slice(None, None)):
        if sub_total_prange_slice == slice(None, None):
            sorted_files_indices = self._sorted_files_indices
        else:
            sorted_files_indices = self._sorted_files_indices[sub_total_prange_slice]

        for i, fileidx in enumerate(sorted_files_indices):
            file_url = self.files[fileidx]
            self.files_data[i] = self.get_data(file_url)
            self._fileindex_to_idx[fileidx] = i

    def _apply_subsample_fact(self, t):
        if t is not None:
            t = t * self.dataset_subsampling
        return t

    def _load_multi(self, sub_total_prange_slice=slice(None, None)):
        if sub_total_prange_slice == slice(None, None):
            files_to_be_compacted_dict = self.files
            sorted_files_indices = self._sorted_files_indices
        else:
            if self.dataset_subsampling > 1:
                start, stop, step = list(
                    map(
                        self._apply_subsample_fact,
                        [sub_total_prange_slice.start, sub_total_prange_slice.stop, sub_total_prange_slice.step],
                    )
                )
                sub_total_prange_slice = slice(start, stop, step)

            sorted_files_indices = self._sorted_files_indices[sub_total_prange_slice]
            files_to_be_compacted_dict = dict(
                zip(sorted_files_indices, [self.files[idx] for idx in sorted_files_indices])
            )

        urls_compacted = get_compacted_dataslices(files_to_be_compacted_dict, subsampling=self.dataset_subsampling)
        loaded = {}
        start_idx = 0
        for idx in sorted_files_indices:
            url = urls_compacted[idx]
            url_str = str(url)
            is_loaded = loaded.get(url_str, False)
            if is_loaded:
                continue
            ds = url.data_slice()
            delta_z = ds.stop - ds.start
            if ds.step is not None and ds.step > 1:
                delta_z //= ds.step
            end_idx = start_idx + delta_z
            self.files_data[start_idx:end_idx] = self.get_data(url)
            start_idx += delta_z
            loaded[url_str] = True

    def load_files(self, overwrite: bool = False, sub_total_prange_slice=slice(None, None)):
        """
        Load the files whose links was provided at class instantiation.

        Parameters
        -----------
        overwrite: bool, optional
            Whether to force reloading the files if already loaded.
        """

        if self._loaded and not (overwrite):
            raise ValueError("Radios were already loaded. Call load_files(overwrite=True) to force reloading")
        if self.file_reader.multi_load:
            self._load_multi(sub_total_prange_slice)
        else:
            if self.dataset_subsampling > 1:
                assert (
                    False
                ), " in helica pipeline, load file _load_single has not yet been adapted to angular subsampling "
            self._load_single(sub_total_prange_slice)
        self._loaded = True

    load_data = load_files

    @property
    def data(self):
        return self.files_data
