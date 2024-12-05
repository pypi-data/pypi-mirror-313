from .. import version
from os import environ

import argparse
import shutil
import os
import sys
import re
import h5py
import numpy as np


from ..resources.logger import LoggerOrPrint
from .utils import parse_params_values
from .cli_configs import CorrectRotConfig
from silx.io.dictdump import h5todict

from nxtomo.application.nxtomo import NXtomo

import h5py
from nabu.utils import DictToObj


def main(user_args=None):
    """Applies the correction found by diag_to_rot to a nexus file"""

    if user_args is None:
        user_args = sys.argv[1:]

    args = DictToObj(
        parse_params_values(
            CorrectRotConfig,
            parser_description=main.__doc__,
            program_version="nabu " + version,
            user_args=user_args,
        )
    )

    # now we read the results of the diag_to_rot utility, they are in the cor_file parameter
    # of the cli
    cor_data = DictToObj(h5todict(args.cor_file, "/"))

    my_cor = cor_data.cor[0]
    # we will take my_cor as cor at the first angular position
    # and then we correct the x_translation at the other angles

    # We now load the nexus that we wish to correct
    nx_tomo = NXtomo().load(args.nexus_source, args.entry_name)

    # The cor_file that we use for correction
    # is providing us with the z_m that gives for each
    # cor position found in the cor array the corresponding value of
    # the translation along z (in meters)
    z_translation = nx_tomo.sample.z_translation.value
    z_translation = z_translation - z_translation[0]

    # now we interpolate to find the correction
    # for each position of the encoders
    cors = np.interp(z_translation, cor_data.z_m, cor_data.cor)

    # this is the correction
    x_correction = nx_tomo.instrument.detector.x_pixel_size.value * (cors - my_cor)  # we are in meters here

    # and we apply it to the nexus that we have loaded
    nx_tomo.sample.x_translation = nx_tomo.sample.x_translation.value + x_correction

    # finally we write it to the corrected nexus file
    nx_tomo.save(file_path=args.nexus_target, data_path=args.entry_name, overwrite=True)

    return 0
