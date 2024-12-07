# coding: utf-8

"""
Application to convert a bliss-hdf5 tomography dataset to Nexus - NXtomo (hdf5) format

.. code-block:: console

    usage: nxtomomill h52nx [-h] [--file-extension FILE_EXTENSION] [--single-file] [--overwrite] [--debug] [--entries ENTRIES] [--ignore-sub-entries IGNORE_SUB_ENTRIES] [--raises-error]
                            [--field-of-view FIELD_OF_VIEW] [--no-input] [--data-copy] [--sample_x_keys SAMPLE_X_KEYS] [--sample_y_keys SAMPLE_Y_KEYS] [--translation_z_keys TRANSLATION_Z_KEYS]
                            [--sample-detector-distance-paths SAMPLE_DETECTOR_DISTANCE_PATHS] [--valid_camera_names VALID_CAMERA_NAMES] [--rot_angle_keys ROT_ANGLE_KEYS] [--acq_expo_time_keys ACQ_EXPO_TIME_KEYS]
                            [--x_pixel_size_key X_PIXEL_SIZE_KEY] [--y_pixel_size_key Y_PIXEL_SIZE_KEY] [--init_titles INIT_TITLES] [--init_zserie_titles INIT_ZSERIE_TITLES] [--dark_titles DARK_TITLES]
                            [--ref_titles REF_TITLES] [--proj_titles PROJ_TITLES] [--align_titles ALIGN_TITLES] [--set-params [SET_PARAMS [SET_PARAMS ...]]] [--format FORMAT] [--config CONFIG]
                            [input_file] [output_file]

    convert data acquired as hdf5 from bliss to nexus `NXtomo` classes. For `zseries` it will create one entry per `z`

    positional arguments:
      input_file            master file of the acquisition
      output_file           output .nx or .h5 file

    optional arguments:
      -h, --help            show this help message and exit
      --file-extension FILE_EXTENSION, --file_extension FILE_EXTENSION
                            extension of the output file. Valid values are .h5/.hdf5/.nx
      --single-file         merge all scan sequence to the same output file. By default create one file per sequence and group all sequence in the output file
      --no-master-file      Avoid creating a master file linking all the NXtomo created
      --overwrite           Do not ask for user permission to overwrite output files
      --debug               Set logs to debug mode
      --entries ENTRIES     Specify (root) entries to be converted. By default it will try to convert all existing entries.
      --ignore-sub-entries IGNORE_SUB_ENTRIES
                            Specify (none-root) sub entries to ignore.
      --raises-error        Raise errors if some data are not met instead of providing some default values
      --field-of-view FIELD_OF_VIEW
                            Force the output to be `Half` or `Full` acquisition. Otherwise parse raw data to find this information.
      --no-input, --no-input-for-missing-information
                            The user won't be ask for any inputs
      --data-copy, --copy-data
                            Force data duplication of frames. This will permit to have an 'all-embed' file. Otherwise the detector/data dataset will haves links to other files.
      --sample_x_keys SAMPLE_X_KEYS, --sample-x-keys SAMPLE_X_KEYS
                            sample x translation key in bliss HDF5 file (direction is independent of the rotation angle)
      --sample_y_keys SAMPLE_Y_KEYS, --sample-y-keys SAMPLE_Y_KEYS
                            sample y translation key in bliss HDF5 file (direction is independent of the rotation angle)
      --translation_z_keys TRANSLATION_Z_KEYS, --translation-z-keys TRANSLATION_Z_KEYS
                            z translation key in bliss HDF5 file
      --sample-detector-distance-paths SAMPLE_DETECTOR_DISTANCE_PATHS, --distance SAMPLE_DETECTOR_DISTANCE_PATHS
                            sample detector distance
      --valid_camera_names VALID_CAMERA_NAMES, --valid-camera-names VALID_CAMERA_NAMES
                            Valid NXDetector dataset name to be considered. Otherwise will try to deduce them from NX_class attribute (value should beNXdetector) or from instrument group child structure.
      --rot_angle_keys ROT_ANGLE_KEYS, --rot-angle-keys ROT_ANGLE_KEYS
                            Valid dataset name for rotation angle
      --acq_expo_time_keys ACQ_EXPO_TIME_KEYS, --acq-expo-time-keys ACQ_EXPO_TIME_KEYS
                            Valid dataset name for acquisition exposure time
      --x_pixel_size_key X_PIXEL_SIZE_KEY, --x-pixel-size-key X_PIXEL_SIZE_KEY
                            X pixel size key to read
      --y_pixel_size_key Y_PIXEL_SIZE_KEY, --y-pixel-size-key Y_PIXEL_SIZE_KEY
                            Y pixel size key to read
      --init_titles INIT_TITLES, --init-titles INIT_TITLES
                            Titles corresponding to init scans
      --init_zserie_titles INIT_ZSERIE_TITLES, --init-zserie-titles INIT_ZSERIE_TITLES
                            Titles corresponding to zserie init scans
      --dark_titles DARK_TITLES, --dark-titles DARK_TITLES
                            Titles corresponding to dark scans
      --flat_titles --flat-titles --ref_titles REF_TITLES, --ref-titles FLAT_TITLES
                            Titles corresponding to ref scans
      --proj_titles PROJ_TITLES, --proj-titles PROJ_TITLES
                            Titles corresponding to projection scans
      --align_titles ALIGN_TITLES, --align-titles ALIGN_TITLES
                            Titles corresponding to alignment scans
      --set-params [SET_PARAMS [SET_PARAMS ...]]
                            Allow manual definition of some parameters. Valid parameters (and expected input unit) are: energy (kev), x_pixel_size (m), y_pixel_size (m). Should be added at the end of the command
                            line because will try to cover all text set after this option.
      --config CONFIG, --config-file CONFIG, --configuration CONFIG, --configuration-file CONFIG
                            file containing the full configuration to convert from h5 bliss to nexus

For a complete tutorial you can have a look at: :ref:`Tomoh52nx`

"""

import argparse
import logging
from typing import Iterable

from tqdm import tqdm

from nxtomomill import utils
from nxtomomill.converter import from_h5_to_nx
from nxtomomill.io.config.confighandler import (
    SETTABLE_PARAMETERS_UNITS,
    TomoHDF5ConfigHandler,
)

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


def _getPossibleInputParams():
    """

    :return: string with param1 (expected unit) ...
    """
    res = []
    for key, value in SETTABLE_PARAMETERS_UNITS.items():
        res.append(f"{key} ({value})")
    return ", ".join(res)


def _ask_for_selecting_detector(det_grps: Iterable):
    res = input(
        "Several detector found. Only one detector is managed at the "
        "time. Please enter the name of the detector you want to use "
        f"or 'Cancel' to stop translation ({det_grps})"
    )
    if res == "Cancel":
        return None
    elif res in det_grps:
        return res
    else:
        # warning: this is not a debug log !!!
        print("detector name not recognized.")
        return _ask_for_selecting_detector(det_grps)


def main(argv):
    """ """
    parser = argparse.ArgumentParser(
        description="convert data acquired as "
        "hdf5 from bliss to nexus "
        "`NXtomo` classes. For `zseries` it will create one entry per `z`"
    )
    parser.add_argument(
        "input_file", help="master file of the " "acquisition", default=None, nargs="?"
    )
    parser.add_argument(
        "output_file", help="output .nx or .h5 file", default=None, nargs="?"
    )
    parser.add_argument(
        "--file-extension",
        "--file_extension",
        default=None,
        help="extension of the output file. Valid values are "
        "" + "/".join(utils.FileExtension.values()),
    )
    parser.add_argument(
        "--single-file",
        help="merge all scan sequence to the same output file. "
        "By default create one file per sequence and "
        "group all sequence in the output file",
        dest="single_file",
        action="store_true",
        default=None,  # default is None and not False for the ConfigHandler so it can knows when set by the user or not
    )
    parser.add_argument(
        "--no-master-file",
        help="Avoid creating a master file linking all .nx files",
        dest="no_master_file",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--overwrite",
        help="Do not ask for user permission to overwrite output files",
        action="store_true",
        default=None,  # default is None and not False for the ConfigHandler so it can knows when set by the user or not
    )
    parser.add_argument(
        "--debug",
        help="Set logs to debug mode",
        action="store_true",
        default=None,  # default is None and not False for the ConfigHandler so it can knows when set by the user or not
    )
    parser.add_argument(
        "--entries",
        help="Specify (root) entries to be converted. By default it will try "
        "to convert all existing entries.",
        default=None,
    )
    parser.add_argument(
        "--ignore-sub-entries",
        help="Specify (none-root) sub entries to ignore.",
        default=None,
    )
    parser.add_argument(
        "--raises-error",
        help="Raise errors if some data are not met instead of providing some"
        " default values",
        action="store_true",
        default=None,  # default is None and not False for the ConfigHandler so it can knows when set by the user or not
    )
    parser.add_argument(
        "--field-of-view",
        help="Force the output to be `Half`  or `Full` acquisition. Otherwise "
        "parse raw data to find this information.",
        default=None,
    )
    parser.add_argument(
        "--no-input",
        "--no-input-for-missing-information",
        help="The user won't be ask for any inputs",
        dest="request_input",
        action="store_false",
        default=None,  # default is None and not False for the ConfigHandler so it can knows when set by the user or not
    )
    parser.add_argument(
        "--data-copy",
        "--copy-data",
        help="Force data duplication of frames. This will permit to have an "
        "'all-embed' file. Otherwise the detector/data dataset will haves "
        "links to other files.",
        action="store_true",
        dest="duplicate_data",
        default=None,  # default is None and not False for the ConfigHandler so it can knows when set by the user or not
    )
    parser.add_argument(
        "--sample_x_keys",
        "--sample-x-keys",
        default=None,
        help="x translation key in bliss HDF5 file",
    )
    parser.add_argument(
        "--sample_y_keys",
        "--sample-y-keys",
        default=None,
        help="y translation key in bliss HDF5 file",
    )
    parser.add_argument(
        "--translation_z_keys",
        "--translation-z-keys",
        default=None,
        help="z translation key in bliss HDF5 file",
    )
    parser.add_argument(
        "--sample-detector-distance-paths",
        "--distance-paths",
        default=None,
        help="sample detector distance paths",
    )
    parser.add_argument(
        "--valid_camera_names",
        "--valid-camera-names",
        default=None,
        help="Valid NXDetector dataset name to be considered. Otherwise will"
        "try to deduce them from NX_class attibute (value should be"
        "NXdetector) or from instrument group child structure.",
    )
    parser.add_argument(
        "--rot_angle_keys",
        "--rot-angle-keys",
        default=None,
        help="Valid dataset name for rotation angle",
    )
    parser.add_argument(
        "--acq_expo_time_keys",
        "--acq-expo-time-keys",
        default=None,
        help="Valid dataset name for acquisition exposure time",
    )
    parser.add_argument(
        "--x_pixel_size_key",
        "--x-pixel-size-key",
        default=None,
        help="X pixel size key to read",
    )
    parser.add_argument(
        "--y_pixel_size_key",
        "--y-pixel-size-key",
        default=None,
        help="Y pixel size key to read",
    )

    # scan titles
    parser.add_argument(
        "--init_titles",
        "--init-titles",
        default=None,
        help="Titles corresponding to init scans",
    )
    parser.add_argument(
        "--init_zserie_titles",
        "--init-zserie-titles",
        default=None,
        help="Titles corresponding to zserie init scans",
    )
    parser.add_argument(
        "--init_pcotomo_titles",
        "--init-pcotomo-titles",
        default=None,
        help="Titles corresponding to pcotomo init scans",
    )
    parser.add_argument(
        "--dark_titles",
        "--dark-titles",
        default=None,
        help="Titles corresponding to dark scans",
    )
    parser.add_argument(
        "--flat_titles" "--flat-titles" "--ref_titles",
        "--ref-titles",
        default=None,
        help="Titles corresponding to ref scans",
        dest="flat_titles",
    )
    parser.add_argument(
        "--proj_titles",
        "--proj-titles",
        default=None,
        help="Titles corresponding to projection scans",
    )
    parser.add_argument(
        "--align_titles",
        "--align-titles",
        default=None,
        help="Titles corresponding to alignment scans",
    )
    parser.add_argument(
        "--set-params",
        default=None,
        nargs="*",
        help="Allow manual definition of some parameters. "
        "Valid parameters (and expected input unit) "
        f"are: {_getPossibleInputParams()}. Should be added at the end of the command line because "
        "will try to cover all text set after this option.",
    )

    # config file
    parser.add_argument(
        "--config",
        "--config-file",
        "--configuration",
        "--configuration-file",
        default=None,
        help="file containing the full configuration to convert from h5 "
        "bliss to nexus",
    )

    options = parser.parse_args(argv[1:])
    if options.request_input:
        callback_det_sel = _ask_for_selecting_detector
    else:
        callback_det_sel = None
    try:
        configuration_handler = TomoHDF5ConfigHandler(options, raise_error=True)
    except Exception:
        _logger.error("Fail to initiate the configuration.", exc_info=True)
        return
    else:
        for title in configuration_handler.configuration.init_titles:
            assert title != ""
        logging.getLogger("nxtomomill").setLevel(
            configuration_handler.configuration.log_level
        )
        from_h5_to_nx(
            configuration=configuration_handler.configuration,
            progress=tqdm(desc="h52nx", delay=1, bar_format="{l_bar}{bar}"),
            input_callback=None,
            detector_sel_callback=callback_det_sel,
        )
