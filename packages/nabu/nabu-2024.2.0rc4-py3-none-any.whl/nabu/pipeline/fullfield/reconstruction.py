from os import environ
from os.path import join, isfile, basename, dirname
from math import ceil
import gc
from psutil import virtual_memory
from silx.io import get_data
from silx.io.url import DataUrl
from tomoscan.esrf.volume.singleframebase import VolumeSingleFrameBase
from ... import version as nabu_version
from ...utils import check_supported, subdivide_into_overlapping_segment
from ...resources.logger import LoggerOrPrint
from ...resources.utils import is_hdf5_extension
from ...io.writer import merge_hdf5_files, NXProcessWriter
from ...cuda.utils import collect_cuda_gpus, __has_pycuda__
from ...preproc.phase import compute_paganin_margin
from ...processing.histogram import PartialHistogram, add_last_bin, hist_as_2Darray
from .chunked import ChunkedPipeline
from .computations import estimate_max_chunk_size

if __has_pycuda__:
    from .chunked_cuda import CudaChunkedPipeline


def variable_idxlen_sort(fname):
    return int(fname.split("_")[-1].split(".")[0])


class FullFieldReconstructor:
    """
    A reconstructor spawns and manages Pipeline objects, depending on the current chunk/group size.
    """

    _available_backends = ["cuda", "numpy"]

    _process_name = "reconstruction"

    default_advanced_options = {
        "gpu_mem_fraction": 0.9,
        "cpu_mem_fraction": 0.9,
        "chunk_size": None,
        "margin": None,
        "force_grouped_mode": False,
    }

    def __init__(self, process_config, logger=None, backend="cuda", extra_options=None, cuda_options=None):
        """
        Initialize a Reconstructor object.
        This class is used for managing pipelines.

        Parameters
        ----------
        process_config: ProcessConfig object
            Data structure with process configuration
        logger: Logger, optional
            logging object
        backend: str, optional
            Which backend to use. Available are: "cuda", "numpy".
        extra_options: dict, optional
            Dictionary with advanced options. Please see 'Other parameters' below
        cuda_options: dict, optional
            Dictionary with cuda options passed to `nabu.cuda.processing.CudaProcessing`


        Other parameters
        -----------------
        Advanced options can be passed in the 'extra_options' dictionary. These can be:

           - cpu_mem_fraction: 0.9,
           - gpu_mem_fraction: 0.9,
           - chunk_size: None,
           - margin: None,
           - force_grouped_mode: False
        """
        self.logger = LoggerOrPrint(logger)
        self.process_config = process_config
        self._set_extra_options(extra_options)
        self._get_reconstruction_range()
        self._get_resources()
        self._get_backend(backend, cuda_options)
        self._compute_margin()
        self._compute_max_chunk_size()
        self._get_pipeline_mode()
        self._build_tasks()

        self._do_histograms = self.process_config.nabu_config["postproc"]["output_histogram"]
        self._reconstruction_output_format_is_hdf5 = is_hdf5_extension(
            self.process_config.nabu_config["output"]["file_format"]
        )
        self._histogram_merged = False
        self.pipeline = None
        self._histogram_merged = False

    #
    # Initialization
    #

    def _set_extra_options(self, extra_options):
        self.extra_options = self.default_advanced_options.copy()
        self.extra_options.update(extra_options or {})
        self.gpu_mem_fraction = self.extra_options["gpu_mem_fraction"]
        self.cpu_mem_fraction = self.extra_options["cpu_mem_fraction"]

    def _get_reconstruction_range(self):
        rec_region = self.process_config.rec_region  # without binning
        self.z_min = rec_region["start_z"]
        # In the user configuration, the upper bound is included: [start_z, end_z].
        # In python syntax, the upper bound is not: [start_z, end_z[
        self.z_max = rec_region["end_z"] + 1
        self.delta_z = self.z_max - self.z_min
        # Cache some volume info
        self.n_angles = self.process_config.n_angles(subsampling=False)
        self.n_z, self.n_x = self.process_config.radio_shape(binning=False)

    def _get_resources(self):
        self.resources = {}
        self._get_gpu()
        self._get_memory()

    def _get_memory(self):
        vm = virtual_memory()
        self.resources["mem_avail_GB"] = vm.available / 1e9
        # Account for other memory constraints. There might be a better way
        slurm_mem_constraint_MB = int(environ.get("SLURM_MEM_PER_NODE", 0))
        if slurm_mem_constraint_MB > 0:
            self.resources["mem_avail_GB"] = slurm_mem_constraint_MB / 1e3
        #
        self.cpu_mem = self.resources["mem_avail_GB"] * self.cpu_mem_fraction

    def _get_gpu(self):
        avail_gpus = collect_cuda_gpus() or {}
        self.resources["gpus"] = avail_gpus
        if len(avail_gpus) == 0:
            return
        # pick first GPU by default. TODO: handle user's nabu_config["resources"]["gpu_id"]
        self.resources["gpu_id"] = self._gpu_id = list(avail_gpus.keys())[0]

    def _get_backend(self, backend, cuda_options):
        self._pipeline_cls = ChunkedPipeline
        check_supported(backend, self._available_backends, "backend")
        if backend == "cuda":
            self.cuda_options = cuda_options
            if len(self.resources["gpus"]) == 0:
                # Not sure if an error should be raised in this case
                self.logger.error("Could not find any cuda device. Falling back on numpy/CPU backend.")
                backend = "numpy"
            else:
                self.gpu_mem = self.resources["gpus"][self._gpu_id]["memory_GB"] * self.gpu_mem_fraction
        if backend == "cuda":
            if not (__has_pycuda__):
                raise RuntimeError("pycuda not avilable")
            self._pipeline_cls = CudaChunkedPipeline  # pylint: disable=E0606
        self.backend = backend

    def _compute_max_chunk_size(self):
        """
        Compute the maximum number of (partial) radios that can be processed in memory.
        Ideally, the processing is done by reading N lines of all the projections.
        This function estimates max_chunk_size = N_max, the maximum number of lines that can be read
        in all the projections while still fitting the memory.
        On the other hand, if a "processing margin" is needed (eg. phase retrieval), then we need to read
        at least N_min = 2 * margin_v + n_slices lines of each image.
        For large datasets, we have N_min > max_chunk_size, so we can't read lines from all the projections.
        """
        user_chunk_size = self.extra_options["chunk_size"]
        if user_chunk_size is not None:
            self.chunk_size = user_chunk_size
        else:
            self.cpu_max_chunk_size = estimate_max_chunk_size(
                self.cpu_mem, self.process_config, pipeline_part="all", step=5
            )
            self.chunk_size = self.cpu_max_chunk_size
            if self.backend == "cuda":
                self.gpu_max_chunk_size = estimate_max_chunk_size(
                    self.gpu_mem,
                    self.process_config,
                    pipeline_part="all",
                    step=5,
                )
                self.chunk_size = min(self.gpu_max_chunk_size, self.cpu_max_chunk_size)
        self.chunk_size = min(self.chunk_size, self.n_z)

    def _compute_max_group_size(self):
        """
        Compute the maximum number of (partial) images that can be processed in memory
        """

        #
        # "Group size" (i.e, how many radios can be processed in one pass for the first part of the pipeline)
        #
        user_group_size = self.extra_options.get("chunk_size", None)
        if user_group_size is not None:
            self.group_size = user_group_size
        else:
            self.cpu_max_group_size = estimate_max_chunk_size(
                self.cpu_mem,
                self.process_config,
                pipeline_part="radios",
                n_rows=min(2 * self._margin_v + self.delta_z, self.n_z),
                step=10,
            )
            self.group_size = self.cpu_max_group_size
            if self.backend == "cuda":
                self.gpu_max_group_size = estimate_max_chunk_size(
                    self.gpu_mem,
                    self.process_config,
                    pipeline_part="radios",
                    n_rows=min(2 * self._margin_v + self.delta_z, self.n_z),
                    step=10,
                )
                self.group_size = min(self.gpu_max_group_size, self.cpu_max_group_size)
        self.group_size = min(self.group_size, self.n_angles)

        #
        # "sinos chunk size" (i.e, how many sinograms can be processed in one pass for the second part of the pipeline)
        #
        self.cpu_max_chunk_size_sinos = estimate_max_chunk_size(
            self.cpu_mem,
            self.process_config,
            pipeline_part="sinos",
            step=10,
        )
        if self.backend == "cuda":
            self.gpu_max_chunk_size_sinos = estimate_max_chunk_size(
                self.gpu_mem,
                self.process_config,
                pipeline_part="sinos",
                step=5,
            )
            self.chunk_size_sinos = min(self.gpu_max_chunk_size_sinos, self.cpu_max_chunk_size_sinos)
        self.chunk_size_sinos = min(self.chunk_size_sinos, self.delta_z)

    def _get_pipeline_mode(self):
        # "Pipeline mode" means we either process data chunks of type [:, delta_z, :] or [delta_theta, :, :].
        # The first case is better in terms of performances and should be preferred.
        # However, in some cases, it's not possible to use it (eg. high "delta_z" because of margin)
        chunk_size_for_one_slice = 1 + 2 * self._margin_v  # TODO ignore margin when resuming from sinogram ?
        chunk_is_too_small = False
        if chunk_size_for_one_slice > self.chunk_size:
            msg = str(
                "Margin is %d, so we need to process at least %d detector rows. However, the available memory enables to process only %d rows at once"
                % (self._margin_v, chunk_size_for_one_slice, self.chunk_size)
            )
            chunk_is_too_small = True
        if self._margin_v > self.chunk_size // 3:
            n_slices = max(1, self.chunk_size - (2 * self._margin_v))
            n_stages = ceil(self.delta_z / n_slices)
            if n_stages > 1:
                msg = str("Margin (%d) is too big for chunk size (%d)" % (self._margin_v, self.chunk_size))
                chunk_is_too_small = True
        force_grouped_mode = self.extra_options.get("force_grouped_mode", False)
        if force_grouped_mode:
            msg = "Forcing grouped mode"
        if self.process_config.processing_options.get("phase", {}).get("method", None) == "CTF":
            force_grouped_mode = True
            msg = "CTF phase retrieval needs to process full radios"
        if self.process_config.processing_options.get("tilt_correction", {}).get("angle", 0) > 15:
            force_grouped_mode = True
            msg = "Radios rotation with a large angle needs to process full radios"
        if self.process_config.resume_from_step == "sinogram" and force_grouped_mode:
            self.logger.warning("Cannot use grouped-radios processing when resuming from sinogram")
            force_grouped_mode = False
        if not (chunk_is_too_small or force_grouped_mode):
            # Default case (preferred)
            self._pipeline_mode = "chunked"
            self.chunk_shape = (self.n_angles, self.chunk_size, self.n_x)
        else:
            # Fall-back mode (slower)
            self.logger.warning(msg)  # pylint: disable=E0606
            self._pipeline_mode = "grouped"
            self._compute_max_group_size()
            self.chunk_shape = (self.group_size, self.delta_z, self.n_x)
            self.logger.info("Using 'grouped' pipeline mode")

    #
    # "Margin"
    #

    def _compute_margin(self):
        user_margin = self.extra_options.get("margin", None)
        if self.process_config.resume_from_step == "sinogram":
            self.logger.debug("Margin not needed when resuming from sinogram")
            margin_v, margin_h = 0, 0
        elif user_margin is not None and user_margin > 0:
            margin_v, margin_h = user_margin, user_margin
            self.logger.info("Using user-defined margin: %d" % user_margin)
        else:
            unsharp_margin = self._compute_unsharp_margin()
            phase_margin = self._compute_phase_margin()
            translations_margin = self._compute_translations_margin()
            cone_margin = self._compute_cone_overlap()
            rot_margin = self._compute_rotation_margin()
            # TODO radios rotation/movements
            margin_v = max(unsharp_margin[0], phase_margin[0], translations_margin[0], cone_margin[0], rot_margin[0])
            margin_h = max(unsharp_margin[1], phase_margin[1], translations_margin[1], cone_margin[1], rot_margin[1])
            if margin_v > 0:
                self.logger.info("Estimated margin: %d pixels" % margin_v)

        margin_v = min(margin_v, self.n_z)
        margin_h = min(margin_h, self.n_x)
        self._margin = margin_v, margin_h
        self._margin_v = margin_v

    def _compute_unsharp_margin(self):
        if "unsharp_mask" not in self.process_config.processing_steps:
            return (0, 0)
        opts = self.process_config.processing_options["unsharp_mask"]
        sigma = opts["unsharp_sigma"]
        # nabu uses cutoff = 4
        cutoff = 4
        gaussian_kernel_size = int(ceil(2 * cutoff * sigma + 1))
        self.logger.debug("Unsharp mask margin: %d pixels" % gaussian_kernel_size)
        return (gaussian_kernel_size, gaussian_kernel_size)

    def _compute_phase_margin(self):
        phase_options = self.process_config.processing_options.get("phase", None)
        if phase_options is None:
            margin_v, margin_h = (0, 0)
        elif phase_options["method"] == "paganin":
            radio_shape = self.process_config.dataset_info.radio_dims[::-1]
            margin_v, margin_h = compute_paganin_margin(
                radio_shape,
                distance=phase_options["distance_m"],
                energy=phase_options["energy_kev"],
                delta_beta=phase_options["delta_beta"],
                pixel_size=phase_options["pixel_size_m"],
                padding=phase_options["padding_type"],
            )
        elif phase_options["method"] == "CTF":
            # The whole projection has to be processed!
            margin_v = ceil(
                (self.n_z - self.delta_z) / 2
            )  # not so elegant. Use a dedicated flag eg. _process_whole_image ?
            margin_h = 0  # unused for now
        else:
            margin_v, margin_h = (0, 0)
        return (margin_v, margin_h)

    def _compute_translations_margin(self):
        translations = self.process_config.dataset_info.translations
        if translations is None:
            return (0, 0)
        margin_h_v = []
        for i in range(2):
            transl = translations[:, i]
            margin_h_v.append(ceil(max([transl.max(), (-transl).max()])))
        self.logger.debug("Maximum vertical displacement: %d pixels" % margin_h_v[1])
        return tuple(margin_h_v[::-1])

    def _compute_cone_overlap(self):
        rec_cfg = self.process_config.processing_options.get("reconstruction", {})
        rec_method = rec_cfg.get("method", None)
        if rec_method != "cone":
            return (0, 0)
        d1 = rec_cfg["source_sample_dist"]
        d2 = rec_cfg["sample_detector_dist"]
        n_z, _ = self.process_config.radio_shape(binning=True)

        delta_z = self.process_config.rec_delta_z  # accounts_for_binning
        overlap = ceil(delta_z * d2 / (d1 + d2))  # sqrt(2) missing ?

        max_overlap = ceil(n_z * d2 / (d1 + d2))  # sqrt(2) missing ?

        return (max_overlap, 0)

    def _compute_rotation_margin(self):
        if "tilt_correction" in self.process_config.processing_steps:
            # Partial radios rotation yields too much error in single-slice mode
            # Forcing a big margin circumvents the problem
            # This is likely to trigger the 'grouped mode', but perhaps grouped mode should always be used when rotating radios
            nz, nx = self.process_config.radio_shape(binning=True)
            return nz // 3, nx // 3
        else:
            return 0, 0

    def _ensure_good_chunk_size_and_margin(self):
        """
        Check that "chunk_size" and "margin" (if any) are a multiple of binning factor.
        See nabu:!208
        After that, all subregion lengths of _build_tasks_chunked() should be multiple of the binning factor,
        because "delta_z" itself was checked to be a multiple in DatasetValidator._handle_binning()
        """
        bin_z = self.process_config.binning_z
        if bin_z <= 1:
            return
        self.chunk_size -= self.chunk_size % bin_z
        if self._margin_v > 0 and (self._margin_v % bin_z) > 0:
            self._margin_v += bin_z - (self._margin_v % bin_z)  # i.e margin = ((margin % bin_z) + 1) * bin_z

    #
    # Tasks management
    #

    def _modify_processconfig_stage_1(self):
        # Modify the "process_config" object to dump sinograms
        proc = self.process_config
        self._old_steps_to_save = proc.steps_to_save.copy()
        if "sinogram" in proc.steps_to_save:
            return
        proc._configure_save_steps(self._old_steps_to_save + ["sinogram"])

    def _undo_modify_processconfig_stage_1(self):
        self.process_config.steps_to_save = self._old_steps_to_save
        if "sinogram" not in self._old_steps_to_save:
            self.process_config.dump_sinogram = False

    def _modify_processconfig_stage_2(self):
        # Modify the "process_config" object to resume from sinograms
        proc = self.process_config
        self._old_resume_from = proc.resume_from_step
        self._old_proc_steps = proc.processing_steps.copy()
        self._old_proc_options = proc.processing_options.copy()
        proc._configure_resume(resume_from="sinogram")

    def _undo_modify_processconfig_stage_2(self):
        self.process_config.resume_from_step = self._old_resume_from
        self.process_config.processing_steps = self._old_proc_steps
        self.process_config.processing_options = self._old_proc_options

    def _build_tasks_grouped(self):
        tasks = []
        segments = subdivide_into_overlapping_segment(self.n_angles, self.group_size, 0)
        for segment in segments:
            _, start_angle, end_angle, _ = segment
            z_min = max(self.z_min - self._margin_v, 0)
            z_max = min(self.z_max + self._margin_v, self.n_z)
            sub_region = ((start_angle, end_angle), (z_min, z_max), (0, self.chunk_shape[-1]))
            tasks.append({"sub_region": sub_region, "margin": (self.z_min - z_min, z_max - self.z_max)})
        self.tasks = tasks
        # Build tasks for stage 2 (sinogram processing + reconstruction)
        segments = subdivide_into_overlapping_segment(self.delta_z, self.chunk_size_sinos, 0)
        self._sino_tasks = []
        for segment in segments:
            _, start_z, end_z, _ = segment
            z_min = self.z_min + start_z
            z_max = min(self.z_min + end_z, self.n_z)
            sub_region = ((0, self.n_angles), (z_min, z_max), (0, self.chunk_shape[-1]))
            self._sino_tasks.append({"sub_region": sub_region, "margin": None})

    def _build_tasks_chunked(self):
        margin_v = self._margin_v
        if self.chunk_size >= self.delta_z and self.z_min == 0 and self.z_max == self.n_z:
            # In this case we can do everything in a single stage, without margin
            self.tasks = [
                {
                    "sub_region": ((0, self.n_angles), (self.z_min, self.z_max), (0, self.chunk_shape[-1])),
                    "margin": None,
                }
            ]
            return
        if self.chunk_size - (2 * margin_v) >= self.delta_z:
            # In this case we can do everything in a single stage
            n_slices = self.delta_z
            (margin_up, margin_down) = (min(margin_v, self.z_min), min(margin_v, self.n_z - self.z_max))
            self.tasks = [
                {
                    "sub_region": (
                        (0, self.n_angles),
                        (self.z_min - margin_up, self.z_max + margin_down),
                        (0, self.chunk_shape[-1]),
                    ),
                    "margin": ((margin_up, margin_down), (0, 0)),
                }
            ]
            return
        # In this case there are at least two stages
        n_slices = self.chunk_size - (2 * margin_v)
        n_stages = ceil(self.delta_z / n_slices)
        self.tasks = []
        curr_z_min = self.z_min
        curr_z_max = self.z_min + n_slices
        for i in range(n_stages):
            margin_up = min(margin_v, curr_z_min)
            margin_down = min(margin_v, max(self.n_z - curr_z_max, 0))
            if curr_z_max + margin_down >= self.z_max:
                curr_z_max -= curr_z_max - (self.z_max + 0)
                margin_down = min(margin_v, max(self.n_z - 1 - curr_z_max, 0))
            self.tasks.append(
                {
                    "sub_region": (
                        (0, self.n_angles),
                        (curr_z_min - margin_up, curr_z_max + margin_down),
                        (0, self.chunk_shape[-1]),
                    ),
                    "margin": ((margin_up, margin_down), (0, 0)),
                }
            )
            if curr_z_max == self.z_max:
                # No need for further tasks
                break
            curr_z_min += n_slices
            curr_z_max += n_slices

    def _build_tasks(self):
        if self._pipeline_mode == "grouped":
            self._build_tasks_grouped()
        else:
            self._ensure_good_chunk_size_and_margin()
            self._build_tasks_chunked()

    def _print_tasks_chunked(self):
        for task in self.tasks:
            margin_up, margin_down = task["margin"][0]
            s_u, s_d = task["sub_region"][1]
            print(
                "Top Margin: [%04d, %04d[  |  Slices: [%04d, %04d[  |  Bottom Margin: [%04d, %04d["
                % (s_u, s_u + margin_up, s_u + margin_up, s_d - margin_down, s_d - margin_down, s_d)
            )

    def _print_tasks(self):
        for task in self.tasks:
            margin_up, margin_down = task["margin"][0]
            s_u, s_d = task["sub_region"][1]
            print(
                "Top Margin: [%04d, %04d[  |  Slices: [%04d, %04d[  |  Bottom Margin: [%04d, %04d["  # pylint: disable=E1307
                % (s_u, s_u + margin_up, s_u + margin_up, s_d - margin_down, s_d - margin_down, s_d)
            )

    def _get_chunk_length(self, task):
        if self._pipeline_mode == "helical":
            (start_z, end_z) = task["sub_region"]
            return end_z - start_z

        else:
            (start_angle, end_angle), (start_z, end_z), _ = task["sub_region"]

            if self._pipeline_mode == "chunked":
                return end_z - start_z
            else:
                return end_angle - start_angle

    def _give_progress_info(self, task):
        self.logger.info("Processing sub-volume %s" % (str(task["sub_region"][:-1])))

    #
    # Reconstruction
    #

    def _instantiate_pipeline(self, task):
        self.logger.debug("Creating a new pipeline object")
        chunk_shape = tuple(s[1] - s[0] for s in task["sub_region"])
        args = [self.process_config, chunk_shape]
        kwargs = {}
        if self.backend == "cuda":
            kwargs["cuda_options"] = self.cuda_options
        kwargs["use_grouped_mode"] = self._pipeline_mode == "grouped"
        pipeline = self._pipeline_cls(*args, logger=self.logger, margin=task["margin"], **kwargs)
        self.pipeline = pipeline

    def _instantiate_pipeline_if_necessary(self, current_task, other_task):
        """
        Instantiate a pipeline only if current_task has a different "delta z" than other_task
        """
        if self.pipeline is None:
            self._instantiate_pipeline(current_task)
            return
        length_cur = self._get_chunk_length(current_task)
        length_other = self._get_chunk_length(other_task)
        if length_cur != length_other:
            self.logger.debug("Destroying pipeline instance and releasing memory")
            self._destroy_pipeline()
            self._instantiate_pipeline(current_task)

    def _destroy_pipeline(self):
        self.pipeline = None
        # Not elegant, but for now the only way to release Cuda memory
        gc.collect()

    def _reconstruct_chunked(self, tasks=None):
        self.results = {}
        self._histograms = {}
        self._data_dumps = {}
        tasks = tasks or self.tasks
        prev_task = tasks[0]
        for task in tasks:
            self.logger.info("Processing sub-volume %s" % (str(task["sub_region"])))
            self._instantiate_pipeline_if_necessary(task, prev_task)
            self.pipeline.process_chunk(task["sub_region"])
            task_key = self.pipeline.sub_region
            task_result = self.pipeline.writer.fname
            self.results[task_key] = task_result
            if self.pipeline.writer.histogram:
                self._histograms[task_key] = self.pipeline.writer.histogram_writer.fname
            if len(self.pipeline.datadump_manager.data_dump) > 0:
                self._data_dumps[task_key] = {}
                for step_name, writer in self.pipeline.datadump_manager.data_dump.items():
                    self._data_dumps[task_key][step_name] = writer.fname
            prev_task = task

    def _reconstruct_grouped(self):
        self.results = {}
        # self._histograms = {}
        self._data_dumps = {}
        prev_task = self.tasks[0]

        # Stage 1: radios processing
        self._modify_processconfig_stage_1()
        for task in self.tasks:
            self.logger.info("Processing sub-volume %s" % (str(task["sub_region"])))
            self._instantiate_pipeline_if_necessary(task, prev_task)
            self.pipeline.process_chunk(task["sub_region"])
            task_key = self.pipeline.sub_region
            task_result = self.pipeline.datadump_manager.data_dump["sinogram"].fname
            self.results[task_key] = task_result
            if len(self.pipeline.datadump_manager.data_dump) > 0:
                self._data_dumps[task_key] = {}
                for step_name, writer in self.pipeline.datadump_manager.data_dump.items():
                    self._data_dumps[task_key][step_name] = writer.fname
            prev_task = task

        self.merge_data_dumps(axis=0)
        self._destroy_pipeline()
        self.logger.info("End of first stage of processing. Will now process sinograms saved on disk")
        self._undo_modify_processconfig_stage_1()

        # Stage 2: sinograms processing and reconstruction
        self._modify_processconfig_stage_2()
        self._pipeline_mode = "chunked"
        self._reconstruct_chunked(tasks=self._sino_tasks)
        self._pipeline_mode = "grouped"
        self._undo_modify_processconfig_stage_2()

    def reconstruct(self):
        if self._pipeline_mode == "chunked":
            self._reconstruct_chunked()
        else:
            self._reconstruct_grouped()

    #
    # Writing data
    #

    def get_relative_files(self, files=None):
        out_cfg = self.process_config.nabu_config["output"]
        if files is None:
            files = list(self.results.values())
        try:
            files.sort(key=variable_idxlen_sort)
        except:
            self.logger.error(
                "Lexical ordering failed, falling back to default sort - it will fail for more than 10k projections"
            )
            files.sort()
        local_files = [join(out_cfg["file_prefix"], basename(fname)) for fname in files]
        return local_files

    def _get_reconstruction_metadata(self, partial_volumes_files=None):
        metadata = {
            "nabu_config": self.process_config.nabu_config,
            "processing_options": self.process_config.processing_options,
        }
        if self._reconstruction_output_format_is_hdf5 and partial_volumes_files is not None:
            metadata[self._process_name + "_stages"] = {
                str(k): v for k, v in zip(self.results.keys(), partial_volumes_files)
            }
        if not (self._reconstruction_output_format_is_hdf5):
            metadata["process_info"] = {
                "process_name": "reconstruction",
                "processing_index": 0,
                "nabu_version": nabu_version,
            }
        return metadata

    def merge_hdf5_reconstructions(
        self,
        output_file=None,
        prefix=None,
        files=None,
        process_name=None,
        axis=0,
        merge_histograms=True,
        output_dir=None,
    ):
        """
        Merge existing hdf5 files by creating a HDF5 virtual dataset.

        Parameters
        ----------
        output_file: str, optional
            Output file name. If not given, the file prefix in section "output"
            of nabu config will be taken.
        """
        out_cfg = self.process_config.nabu_config["output"]
        out_dir = output_dir or out_cfg["location"]
        prefix = prefix or ""
        # Prevent issue when out_dir is empty, which happens only if dataset/location is a relative path.
        # TODO this should be prevented earlier
        if out_dir is None or len(out_dir.strip()) == 0:
            out_dir = dirname(dirname(self.results[list(self.results.keys())[0]]))
        #
        if output_file is None:
            output_file = join(out_dir, prefix + out_cfg["file_prefix"]) + ".hdf5"
        if isfile(output_file):
            msg = str("File %s already exists" % output_file)
            if out_cfg["overwrite_results"]:
                msg += ". Overwriting as requested in configuration file"
                self.logger.warning(msg)
            else:
                msg += ". Set overwrite_results to True in [output] to overwrite existing files."
                self.logger.fatal(msg)
                raise ValueError(msg)

        local_files = files
        if local_files is None:
            local_files = self.get_relative_files()
        if local_files == []:
            self.logger.error("No files to merge")
            return
        entry = getattr(self.process_config.dataset_info.dataset_scanner, "entry", "entry")
        process_name = process_name or self._process_name
        h5_path = join(entry, *[process_name, "results", "data"])
        #
        self.logger.info("Merging %ss to %s" % (process_name, output_file))
        #
        # When dumping to disk an intermediate step taking place before cropping the radios,
        # 'start_z' and 'end_z' found in nabu config have to be augmented with margin_z.
        # (these values are checked in ProcessConfig._configure_resume())
        #
        patched_start_end_z = False
        if (
            self._margin_v > 0
            and process_name != "reconstruction"
            and self.process_config.is_before_radios_cropping(process_name)
            and "reconstruction" in self.process_config.processing_steps
        ):
            user_rec_config = self.process_config.processing_options["reconstruction"]
            patched_start_end_z = True
            old_start_z = user_rec_config["start_z"]
            old_end_z = user_rec_config["end_z"]
            user_rec_config["start_z"] = max(0, old_start_z - self._margin_v)
            user_rec_config["end_z"] = min(self.n_z, old_end_z + self._margin_v)
        #
        merge_hdf5_files(
            local_files,
            h5_path,
            output_file,
            process_name,
            output_entry=entry,
            output_filemode="a",
            processing_index=0,
            config=self._get_reconstruction_metadata(local_files),
            base_dir=out_dir,
            axis=axis,
            overwrite=out_cfg["overwrite_results"],
        )
        if merge_histograms:
            self.merge_histograms(output_file=output_file)
        if patched_start_end_z:
            user_rec_config["start_z"] = old_start_z
            user_rec_config["end_z"] = old_end_z
        return output_file

    def merge_histograms(self, output_file=None, force_merge=False):
        """
        Merge the partial histograms
        """
        if not (self._do_histograms):
            return
        if self._histogram_merged and not (force_merge):
            return
        self.logger.info("Merging histograms")

        masterfile_entry = getattr(self.process_config.dataset_info.dataset_scanner, "entry", "entry")
        masterfile_process_name = "histogram"  # TODO don't hardcode process name
        output_entry = masterfile_entry

        out_cfg = self.process_config.nabu_config["output"]
        if output_file is None:
            output_file = (
                join(dirname(list(self._histograms.values())[0]), out_cfg["file_prefix"] + "_histogram") + ".hdf5"
            )
        local_files = self.get_relative_files(files=list(self._histograms.values()))
        #
        h5_path = join(masterfile_entry, *[masterfile_process_name, "results", "data"])
        #

        try:
            files = sorted(self._histograms.values(), key=variable_idxlen_sort)
        except:
            self.logger.error(
                "Lexical ordering of histogram failed, falling back to default sort - it will fail for more than 10k projections"
            )
            files = sorted(self._histograms.values())
        data_urls = []
        for fname in files:
            url = DataUrl(file_path=fname, data_path=h5_path, data_slice=None, scheme="silx")
            data_urls.append(url)
        histograms = []
        for data_url in data_urls:
            h2D = get_data(data_url)
            histograms.append((h2D[0], add_last_bin(h2D[1])))
        histograms_merger = PartialHistogram(method="fixed_bins_number", num_bins=histograms[0][0].size)
        merged_hist = histograms_merger.merge_histograms(histograms)

        rec_region = self.process_config.rec_region
        # Not sure if we should account for binning here.
        # (note that "rec_region" does not account for binning).
        # Anyway the histogram has little use when using binning
        volume_shape = (
            rec_region["end_z"] - rec_region["start_z"] + 1,
            rec_region["end_y"] - rec_region["start_y"] + 1,
            rec_region["end_x"] - rec_region["start_x"] + 1,
        )
        writer = NXProcessWriter(output_file, entry=output_entry, filemode="a", overwrite=True)
        writer.write(
            hist_as_2Darray(merged_hist),
            "histogram",
            processing_index=1,
            config={
                "files": local_files,
                "bins": self.process_config.nabu_config["postproc"]["histogram_bins"],
                "volume_shape": volume_shape,
            },
            is_frames_stack=False,
            direct_access=False,
        )
        self._histogram_merged = True

    def merge_data_dumps(self, axis=1):
        # Collect in a dict where keys are step names (instead of task keys)
        dumps = {}
        for task_key, data_dumps in self._data_dumps.items():
            for step_name, fname in data_dumps.items():
                fname = join(basename(dirname(fname)), basename(fname))
                if step_name not in dumps:
                    dumps[step_name] = [fname]
                else:
                    dumps[step_name].append(fname)
        # Merge HDF5 files
        for step_name, files in dumps.items():
            dump_file = self.process_config.get_save_steps_file(step_name=step_name)
            self.merge_hdf5_reconstructions(
                output_file=dump_file,
                output_dir=dirname(dump_file),
                files=files,
                process_name=step_name,
                axis=axis,
                merge_histograms=False,
            )

    def write_metadata_file(self):
        metadata = self._get_reconstruction_metadata()
        save_options = self.process_config.processing_options["save"]
        # Perhaps there is more elegant
        metadata_writer = VolumeSingleFrameBase(
            url=DataUrl(file_path=save_options["location"], data_path="/"),
            volume_basename=save_options["file_prefix"],
            overwrite=True,
            metadata=metadata,
        )
        metadata_writer.save_metadata()

    def finalize_files_saving(self):
        """
        Last step to save data. This will do several things:
          - Merge data dumps (which are always HDF5 files): create a master file for all data-dump sub-volumes
          - Merge HDF5 reconstruction (if output format is HDF5)
          - Create a "metadata file" (if output format is not HDF5)
          - Merge histograms (if output format is not HDF5)
        """
        self.merge_data_dumps()
        if self._reconstruction_output_format_is_hdf5:
            self.merge_hdf5_reconstructions()
        else:
            self.merge_histograms()
            self.write_metadata_file()
