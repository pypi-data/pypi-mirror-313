import os
from nabu.misc.utils import rescale_data
from nabu.pipeline.params import files_formats
from tomoscan.volumebase import VolumeBase
from tomoscan.scanbase import TomoScanBase
from tomoscan.esrf.volume import (
    EDFVolume,
    HDF5Volume,
    JP2KVolume,
    MultiTIFFVolume,
    TIFFVolume,
)
from tomoscan.io import HDF5File
from silx.io.utils import get_data
from silx.utils.enum import Enum as _Enum
import numpy
from silx.io.url import DataUrl
from typing import Optional
import logging

_logger = logging.getLogger(__name__)


__all__ = ["get_default_output_volume", "cast_volume"]

_DEFAULT_OUTPUT_DIR = "vol_cast"


RESCALE_MIN_PERCENTILE = 10
RESCALE_MAX_PERCENTILE = 90


def get_default_output_volume(
    input_volume: VolumeBase, output_type: str, output_dir: str = _DEFAULT_OUTPUT_DIR
) -> VolumeBase:
    """
    For a given input volume and output type return output volume as an instance of VolumeBase

    :param VolumeBase intput_volume: volume for which we want to get the resulting output volume for a cast
    :param str output_type: output_type of the volume (edf, tiff, hdf5...)
    :param str output_dir: output dir to save the cast volume
    """
    if not isinstance(input_volume, VolumeBase):
        raise TypeError(f"input_volume is expected to be an instance of {VolumeBase}")
    valid_file_formats = set(files_formats.values())
    if not output_type in valid_file_formats:
        raise ValueError(f"output_type is not a valid value ({output_type}). Valid values are {valid_file_formats}")

    if isinstance(input_volume, (EDFVolume, TIFFVolume, JP2KVolume)):
        if output_type == "hdf5":
            file_path = os.path.join(
                input_volume.data_url.file_path(),
                output_dir,
                input_volume.get_volume_basename() + ".hdf5",
            )
            volume = HDF5Volume(
                file_path=file_path,
                data_path="/volume",
            )
            assert volume.get_identifier() is not None, "volume should be able to create an identifier"
            return volume
        elif output_type in ("tiff", "edf", "jp2"):
            if output_type == "tiff":
                Constructor = TIFFVolume
            elif output_type == "edf":
                Constructor = EDFVolume
            elif output_type == "jp2":
                Constructor = JP2KVolume
            return Constructor(  # pylint: disable=E0601
                folder=os.path.join(
                    os.path.dirname(input_volume.data_url.file_path()),
                    output_dir,
                ),
                volume_basename=input_volume.get_volume_basename(),
            )
        else:
            raise NotImplementedError(f"output volume format {output_type} is not handled")
    elif isinstance(input_volume, (HDF5Volume, MultiTIFFVolume)):
        if output_type == "hdf5":
            data_file_parent_path, data_file_name = os.path.split(input_volume.data_url.file_path())
            # replace extension:
            data_file_name = ".".join(
                [
                    os.path.splitext(data_file_name)[0],
                    "hdf5",
                ]
            )
            if isinstance(input_volume, HDF5Volume):
                data_data_path = input_volume.data_url.data_path()
                metadata_data_path = input_volume.metadata_url.data_path()
                try:
                    data_path = os.path.commonprefix([data_data_path, metadata_data_path])
                except Exception:
                    data_path = "volume"
            else:
                data_data_path = HDF5Volume.DATA_DATASET_NAME
                metadata_data_path = HDF5Volume.METADATA_GROUP_NAME
                file_path = data_file_name
                data_path = "volume"

            volume = HDF5Volume(
                file_path=os.path.join(data_file_parent_path, output_dir, data_file_name),
                data_path=data_path,
            )
            assert volume.get_identifier() is not None, "volume should be able to create an identifier"
            return volume
        elif output_type in ("tiff", "edf", "jp2"):
            if output_type == "tiff":
                Constructor = TIFFVolume
            elif output_type == "edf":
                Constructor = EDFVolume
            elif output_type == "jp2":
                Constructor = JP2KVolume
            file_parent_path, file_name = os.path.split(input_volume.data_url.file_path())
            file_name = os.path.splitext(file_name)[0]
            return Constructor(
                folder=os.path.join(
                    file_parent_path,
                    output_dir,
                    os.path.basename(file_name),
                )
            )
        else:
            raise NotImplementedError(f"output volume format {output_type} is not handled")
    else:
        raise NotImplementedError(f"input volume format {input_volume} is not handled")


def cast_volume(
    input_volume: VolumeBase,
    output_volume: VolumeBase,
    output_data_type: numpy.dtype,
    data_min=None,
    data_max=None,
    scan: Optional[TomoScanBase] = None,
    rescale_min_percentile=RESCALE_MIN_PERCENTILE,
    rescale_max_percentile=RESCALE_MAX_PERCENTILE,
    save=True,
    store=False,
) -> VolumeBase:
    """
    cast givent volume to output_volume of 'output_data_type' type

    :param VolumeBase input_volume:
    :param VolumeBase output_volume:
    :param numpy.dtype output_data_type: output data type
    :param number data_min: `data` min value to clamp to new_min. Any lower value will also be clamp to new_min.
    :param number data_max: `data` max value to clamp to new_max. Any hight value will also be clamp to new_max.
    :param TomoScanBase scan: source scan that produced input_volume. Can be used to find histogram for example.
    :param rescale_min_percentile: if `data_min` is None will set data_min to 'rescale_min_percentile'
    :param rescale_max_percentile: if `data_max` is None will set data_min to 'rescale_max_percentile'
    :param bool save: if True dump the slice on disk (one by one)
    :param bool store: if True once the volume is cast then set `output_volume.data`
    :return: output_volume with data and metadata set

    .. warning::
        the created will volume will not be saved in this processing. If you want
        to save the cast volume you must do it yourself.

    .. note::
        if you want to tune compression ratios (for jp2k) then please update the `cratios` attributes of the output volume

    """
    if not isinstance(input_volume, VolumeBase):
        raise TypeError(f"input_volume is expected to be a {VolumeBase}. {type(input_volume)} provided")

    if not isinstance(output_volume, VolumeBase):
        raise TypeError(f"output_volume is expected to be a {VolumeBase}. {type(output_volume)} provided")

    try:
        output_data_type = numpy.dtype(
            output_data_type
        )  # User friendly API in case user provides np.uint16 e.g. (see issue #482)
    except Exception:
        pass
    if not isinstance(output_data_type, numpy.dtype):
        raise TypeError(f"output_data_type is expected to be a {numpy.dtype}. {type(output_data_type)} provided")

    # start processing
    #  check for data_min and data_max
    if data_min is None or data_max is None:
        found_data_min, found_data_max = _try_to_find_min_max_from_histo(
            input_volume=input_volume,
            scan=scan,
            rescale_min_percentile=rescale_min_percentile,
            rescale_max_percentile=rescale_max_percentile,
        )
        if found_data_min is None or found_data_max is None:
            _logger.warning("couldn't find histogram, recompute volume min and max values")
            data_min, data_max = input_volume.get_min_max()
            _logger.info(f"min and max found ({data_min} ; {data_max})")

        data_min = data_min if data_min is not None else found_data_min
        data_max = data_max if data_max is not None else found_data_max

    data = []
    for input_slice, frame_dumper in zip(
        input_volume.browse_slices(),
        output_volume.data_file_saver_generator(
            input_volume.get_volume_shape()[0],
            data_url=output_volume.data_url,
            overwrite=output_volume.overwrite,
        ),
    ):
        if numpy.issubdtype(output_data_type, numpy.integer):
            new_min = numpy.iinfo(output_data_type).min
            new_max = numpy.iinfo(output_data_type).max
            output_slice = clamp_and_rescale_data(
                data=input_slice,
                new_min=new_min,
                new_max=new_max,
                data_min=data_min,
                data_max=data_max,
                rescale_min_percentile=rescale_min_percentile,
                rescale_max_percentile=rescale_max_percentile,
            ).astype(output_data_type)
        else:
            output_slice = input_slice.astype(output_data_type)
        if save:
            frame_dumper[:] = output_slice
        if store:
            # only keep data in cache if not dump to disk
            data.append(output_slice)

    if store:
        output_volume.data = numpy.asarray(data)

    # try also to append some metadata to it
    try:
        output_volume.metadata = input_volume.metadata or input_volume.load_metadata()
    except (OSError, KeyError):
        # if no metadata provided and or saved in disk or if some key are missing
        pass
    return output_volume


def clamp_and_rescale_data(
    data: numpy.ndarray,
    new_min,
    new_max,
    data_min=None,
    data_max=None,
    rescale_min_percentile=RESCALE_MIN_PERCENTILE,
    rescale_max_percentile=RESCALE_MAX_PERCENTILE,
):
    """
    rescale data to 'new_min', 'new_max'

    :param numpy.ndarray data: data to be rescaled
    :param dtype output_dtype: output dtype
    :param new_min: rescaled data new min (clamp min value)
    :param new_max: rescaled data new max (clamp max value)
    :param data_min: `data` min value to clamp to new_min. Any lower value will also be clamp to new_min.
    :param data_max: `data` max value to clamp to new_max. Any hight value will also be clamp to new_max.
    :param rescale_min_percentile: if `data_min` is None will set data_min to 'rescale_min_percentile'
    :param rescale_max_percentile: if `data_max` is None will set data_min to 'rescale_max_percentile'
    """
    if data_min is None:
        data_min = numpy.percentile(data, rescale_min_percentile)
    if data_max is None:
        data_max = numpy.percentile(data, rescale_max_percentile)
    # rescale data
    rescaled_data = rescale_data(data, new_min=new_min, new_max=new_max, data_min=data_min, data_max=data_max)
    # clamp data
    rescaled_data[rescaled_data < new_min] = new_min
    rescaled_data[rescaled_data > new_max] = new_max
    return rescaled_data


def find_histogram(volume: VolumeBase, scan: Optional[TomoScanBase] = None) -> Optional[DataUrl]:
    """
    Look for histogram of the provided url. If found one return the DataUrl of the nabu histogram
    """
    if not isinstance(volume, VolumeBase):
        raise TypeError(f"volume is expected to be an instance of {VolumeBase} not {type(volume)}")
    elif isinstance(volume, HDF5Volume):
        histogram_file = volume.data_url.file_path()
        if volume.url is not None:
            data_path = volume.url.data_path()
            if data_path.endswith("reconstruction"):
                data_path = "/".join(
                    [
                        *data_path.split("/")[:-1],
                        "histogram/results/data",
                    ]
                )
            else:
                data_path = "/".join((volume.url.data_path(), "histogram/results/data"))
        else:
            # TODO: FIXME: in some case (if the users provides the full data_url and if the 'DATA_DATASET_NAME' is not used we
            # will endup with an invalid data_path. Hope this case will not happen. Anyway this is a case that we can't handle.)
            # if trouble: check if data_path exists. If not raise an error saying this we can't find an histogram for this volume
            data_path = volume.data_url.data_path().replace(HDF5Volume.DATA_DATASET_NAME, "histogram/results/data")
    elif isinstance(volume, (EDFVolume, JP2KVolume, TIFFVolume, MultiTIFFVolume)):
        if isinstance(volume, (EDFVolume, JP2KVolume, TIFFVolume)):
            histogram_file = os.path.join(
                volume.data_url.file_path(),
                volume.get_volume_basename() + "_histogram.hdf5",
            )
            if not os.path.exists(histogram_file):
                # legacy location
                legacy_histogram_file = os.path.join(
                    volume.data_url.file_path(),
                    volume.get_volume_basename() + "histogram.hdf5",
                )
                if os.path.exists(legacy_histogram_file):
                    # only overwrite if exists. Else keep the older one to get a clearer information
                    histogram_file = legacy_histogram_file
        else:
            file_path, _ = os.path.splitext(volume.data_url.file_path())
            histogram_file = file_path + "_histogram.hdf5"

        if scan is not None:
            data_path = getattr(scan, "entry/histogram/results/data", "entry/histogram/results/data")
        else:

            def get_file_entries(file_path: str) -> Optional[tuple]:
                if os.path.exists(file_path):
                    with HDF5File(file_path, mode="r") as h5s:
                        return tuple(h5s.keys())
                else:
                    return None

            # in the case we only know about the volume to cast.
            # in most of the cast the histogram.hdf5 file will only get a single entry. The exception could be
            # for HDF5 if the user save volumes into the same file.
            # we can find back the histogram
            entries = get_file_entries(histogram_file)
            if entries is not None and len(entries) == 1:
                data_path = "/".join((entries[0], "histogram/results/data"))
            else:
                # TODO: FIXME: how to get the entry name in every case ?
                # what to do if the histogram file has more than one entry.
                # one option could be to request the entry from the user...
                # or keep as today (in this case it will be recomputed)
                _logger.info("histogram file found but unable to find relevant histogram")
                return None
    else:
        raise NotImplementedError(f"volume {type(volume)} not handled")

    if not os.path.exists(histogram_file):
        _logger.info(f"{histogram_file} not found")
        return None

    with HDF5File(histogram_file, mode="r") as h5f:
        if not data_path in h5f:
            _logger.info(f"{data_path} in {histogram_file} not found")
            return None
        else:
            _logger.info(f"Found histogram {histogram_file}::/{data_path}")
            return DataUrl(
                file_path=histogram_file,
                data_path=data_path,
                scheme="silx",
            )


def _get_hst_saturations(hist, bins, rescale_min_percentile: numpy.float32, rescale_max_percentile: numpy.float32):
    hist_cum = numpy.cumsum(hist)
    bin_index_min = numpy.searchsorted(hist_cum, numpy.percentile(hist_cum, rescale_min_percentile))
    bin_index_max = numpy.searchsorted(hist_cum, numpy.percentile(hist_cum, rescale_max_percentile))
    return bins[bin_index_min], bins[bin_index_max]


def _try_to_find_min_max_from_histo(
    input_volume: VolumeBase, rescale_min_percentile, rescale_max_percentile, scan=None
) -> tuple:
    """
    util to interpret nabu histogram and deduce data_min and data_max to be used for
    rescaling a volume
    """
    histogram_res_url = find_histogram(input_volume, scan=scan)
    if histogram_res_url is not None:
        return _min_max_from_histo(
            url=histogram_res_url,
            rescale_min_percentile=rescale_min_percentile,
            rescale_max_percentile=rescale_max_percentile,
        )
    else:
        return None, None


def _min_max_from_histo(url: DataUrl, rescale_min_percentile: int, rescale_max_percentile: int) -> tuple:
    try:
        histogram = get_data(url)
    except Exception as e:
        _logger.error(f"Fail to load histogram from {url.path()}. Reason is {e}")
        return None, None
    else:
        bins = histogram[1]
        hist = histogram[0]
        return _get_hst_saturations(
            hist, bins, numpy.float32(rescale_min_percentile), numpy.float32(rescale_max_percentile)
        )
