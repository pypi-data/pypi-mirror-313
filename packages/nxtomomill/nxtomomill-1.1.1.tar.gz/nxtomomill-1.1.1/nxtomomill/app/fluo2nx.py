# coding: utf-8

"""
Application to convert a fluo-tomo dataset, after PyMCA (https://www.silx.org/doc/PyMca/dev/index.html) fit, into an hdf5/nexus file.

.. code-block:: bash

    usage: nxtomomill fluo2nx [-h] [--info-file INFO_FILE] [--config CONFIG] [scan_path] [output_file]

    convert fluo-tomo data (after PyMCA fit) to hdf5 - nexus compliant file format.

    positional arguments:
    scan_path             folder containing the tiff files
    output_file           foutput .h5 file
    dataset_basename      File prefix to be used to deduce projection file names.

    optional arguments:
    -h, --help            show this help message and exit
    --dataset-basename DATASET_BASENAME, --file-prefix DATASET_BASENAME
                            file prefix to be used to deduce projections
    --info-file INFO_FILE
                            .info file containing acquisition information (ScanRange, Energy, TOMO_N...)
    --config CONFIG, --configuration-file CONFIG, --configuration CONFIG
                            file containing the full configuration to convert from fluo files to nexus. Default configuration file can be created from `nxtomomill fluo-config` command
"""

import argparse
import logging
import os

from nxtomomill import utils
from nxtomomill import converter
from nxtomomill.io.config.fluoconfig import TomoFluoConfig

from tqdm import tqdm

logging.basicConfig(level=logging.INFO)


def main(argv):
    """ """
    parser = argparse.ArgumentParser(
        description="Converts fluo-tomo data (after PyMca fit) "
        "to hdf5 - nexus compliant file format."
    )
    parser.add_argument(
        "scan_path", help="folder containing the projection tiff files", nargs=1
    )
    parser.add_argument(
        "output_file",
        help="File produced by the converter. '.nx' extension recommended.",
        nargs=1,
    )
    parser.add_argument(
        "dataset_basename",
        help="file prefix to be used to deduce projections. ",
        nargs=1,
    )
    parser.add_argument(
        "--detectors",
        nargs="*",
        default=list(),
        help="Define a list of detector names used for the exp (coma separated values). E.g. 'falcon, xmap'.",
    )
    parser.add_argument(
        "--info-file",
        default=None,
        help=".info file containing acquisition information (ScanRange, Energy, TOMO_N...)",
    )
    parser.add_argument(
        "--config",
        "--configuration-file",
        "--configuration",
        default=None,
        help="file containing the full configuration to convert from (PyMCA-computed) fluo  projections to nexus. "
        "Default configuration file can be created from `nxtomomill fluo-config` command",
    )

    parser.add_argument(
        "--mode",
        default="newfile",
        help="What to do if file exists:"
        "- 'newfile': program will fail if file already exists."
        "- 'overwrite': program will overwrite existing file or existing entries in file.",
    )

    options = parser.parse_args(argv[1:])
    config = TomoFluoConfig()
    if options.config is not None:
        config = config.from_cfg_file(options.config)

    check_input = {
        "dataset basename": (options.dataset_basename, config.dataset_basename),
        "scan path": (options.scan_path, config.input_folder),
        "output file": (options.output_file, config.output_file),
        "info file": (options.info_file, config.dataset_info_file),
    }
    for input_name, (opt_value, config_value) in check_input.items():
        if (
            opt_value is not None
            and config_value is not None
            and opt_value != config_value
        ):
            raise ValueError(
                f"two values for {input_name} are provided from arguments and configuration file ({opt_value, config_value})"
            )

    if options.dataset_basename is not None:
        config.dataset_basename = options.dataset_basename[0]
    if options.info_file is not None:
        config.dataset_info_file = options.info_file
    if options.scan_path is not None:
        config.input_folder = options.scan_path[0]
    if options.output_file is not None:
        config.output_file = options.output_file[0]
    if options.detectors is not None:
        config.detectors = options.detectors

    fileout_h5 = utils.get_file_name(
        file_name=config.output_file,
        extension=config.file_extension,
        check=True,
    )
    if os.path.exists(fileout_h5):
        if options.mode == "newfile":
            raise FileExistsError(
                f"The file {fileout_h5} already exists. Please remove it before running the program."
            )
        elif options.mode == "overwrite":
            config.overwrite = True
        else:
            raise RuntimeError(
                f"The value entered for --mode is not valid. Should be either 'newfile' or 'overwrite'. {options.mode} was given."
            )

    converter.from_fluo_to_nx(
        configuration=config,
        progress=tqdm("fluo2nx"),
    )
