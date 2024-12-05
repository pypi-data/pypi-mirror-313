import os
import pytest
import numpy as np
from nabu.testutils import utilstest, __do_long_tests__
from nabu.resources.dataset_analyzer import HDF5DatasetAnalyzer, analyze_dataset
from nabu.resources.nxflatfield import update_dataset_info_flats_darks
from nabu.resources.utils import extract_parameters
from nabu.pipeline.estimators import CompositeCOREstimator
from nabu.pipeline.config import parse_nabu_config_file
from nabu.pipeline.estimators import SinoCORFinder, CORFinder


#
# Test CoR estimation with "composite-coarse-to-fine" (aka "near" in the legacy system vocable)
#


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls

    dataset_downloaded_path = utilstest.getfile("test_composite_cor_finder_data.h5")
    cls.theta_interval = 4.5 * 1  # this is given. Radios in the middle of steps 4.5 degree long
    # are set to zero for compression
    # You can still change it to a multiple of 4.5
    cls.cor_pix = 1321.625
    cls.abs_tol = 0.0001
    cls.dataset_info = HDF5DatasetAnalyzer(dataset_downloaded_path)
    update_dataset_info_flats_darks(cls.dataset_info, True)
    cls.cor_options = extract_parameters("side=300.0;  near_width = 20.0", sep=";")


@pytest.mark.skipif(not (__do_long_tests__), reason="Need NABU_LONG_TESTS=1 for this test")
@pytest.mark.usefixtures("bootstrap")
class TestCompositeCorFinder:
    def test(self):
        cor_finder = CompositeCOREstimator(
            self.dataset_info, theta_interval=self.theta_interval, cor_options=self.cor_options
        )

        cor_position = cor_finder.find_cor()
        message = "Computed CoR %f " % cor_position + " and real CoR %f do not coincide" % self.cor_pix
        assert np.isclose(self.cor_pix, cor_position, atol=self.abs_tol), message


@pytest.fixture(scope="class")
def bootstrap_bamboo_reduced(request):
    cls = request.cls
    cls.abs_tol = 0.2
    # Dataset without estimated_cor_frm_motor (non regression test)
    dataset_relpath = os.path.join("bamboo_reduced.nx")
    dataset_downloaded_path = utilstest.getfile(dataset_relpath)
    conf_relpath = os.path.join("bamboo_reduced.conf")
    conf_downloaded_path = utilstest.getfile(conf_relpath)
    cls.ds_std = analyze_dataset(dataset_downloaded_path)
    update_dataset_info_flats_darks(cls.ds_std, True)
    cls.conf_std = parse_nabu_config_file(conf_downloaded_path)

    # Dataset with estimated_cor_frm_motor
    dataset_relpath = os.path.join("bamboo_reduced_bliss.nx")
    dataset_downloaded_path = utilstest.getfile(dataset_relpath)
    conf_relpath = os.path.join("bamboo_reduced_bliss.conf")
    conf_downloaded_path = utilstest.getfile(conf_relpath)
    cls.ds_bliss = analyze_dataset(dataset_downloaded_path)
    update_dataset_info_flats_darks(cls.ds_bliss, True)
    cls.conf_bliss = parse_nabu_config_file(conf_downloaded_path)


@pytest.mark.skipif(not (__do_long_tests__), reason="need environment variable NABU_LONG_TESTS=1")
@pytest.mark.usefixtures("bootstrap_bamboo_reduced")
class TestCorNearPos:
    # TODO adapt test file
    true_cor = 339.486 - 0.5

    def test_cor_sliding_standard(self):
        cor_options = extract_parameters(self.conf_std["reconstruction"].get("cor_options", None), sep=";")
        for side in [None, "from_file", "center"]:
            if side is not None:
                cor_options.update({"side": side})
            finder = CORFinder("sliding-window", self.ds_std, do_flatfield=True, cor_options=cor_options)
            cor = finder.find_cor()
            message = f"Computed CoR {cor} and expected CoR {self.true_cor} do not coincide. Near_pos options was set to {cor_options.get('near_pos',None)}."
            assert np.isclose(self.true_cor, cor, atol=self.abs_tol + 0.5), message  # FIXME

    def test_cor_fourier_angles_standard(self):
        cor_options = extract_parameters(self.conf_std["reconstruction"].get("cor_options", None), sep=";")
        # TODO modify test files
        if "near_pos" in cor_options and "near" in cor_options.get("side", "") == "near":
            cor_options["side"] = cor_options["near_pos"]
        #
        for side in [None, "from_file", "center"]:
            if side is not None:
                cor_options.update({"side": side})
            finder = SinoCORFinder("fourier-angles", self.ds_std, do_flatfield=True, cor_options=cor_options)
            cor = finder.find_cor()
            message = f"Computed CoR {cor} and expected CoR {self.true_cor} do not coincide. Near_pos options was set to {cor_options.get('near_pos',None)}."
            assert np.isclose(self.true_cor + 0.5, cor, atol=self.abs_tol), message

    def test_cor_sliding_bliss(self):
        cor_options = extract_parameters(self.conf_bliss["reconstruction"].get("cor_options", None), sep=";")
        # TODO modify test files
        if "near_pos" in cor_options and "near" in cor_options.get("side", "") == "near":
            cor_options["side"] = cor_options["near_pos"]
        #
        for side in [None, "from_file", "center"]:
            if side is not None:
                cor_options.update({"side": side})
            finder = CORFinder("sliding-window", self.ds_bliss, do_flatfield=True, cor_options=cor_options)
            cor = finder.find_cor()
            message = f"Computed CoR {cor} and expected CoR {self.true_cor} do not coincide. Near_pos options was set to {cor_options.get('near_pos',None)}."
            assert np.isclose(self.true_cor, cor, atol=self.abs_tol), message

    def test_cor_fourier_angles_bliss(self):
        cor_options = extract_parameters(self.conf_bliss["reconstruction"].get("cor_options", None), sep=";")
        for side in [None, "from_file", "center"]:
            if side is not None:
                cor_options.update({"side": side})
            finder = SinoCORFinder("fourier-angles", self.ds_bliss, do_flatfield=True, cor_options=cor_options)
            cor = finder.find_cor()
            message = f"Computed CoR {cor} and expected CoR {self.true_cor} do not coincide. Near_pos options was set to {cor_options.get('near_pos',None)}."
            assert np.isclose(self.true_cor + 0.5, cor, atol=self.abs_tol), message
