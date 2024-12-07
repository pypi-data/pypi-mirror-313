# coding: utf-8

"""
module to convert fluo-tomo files (after PyMCA fit, tif files) to (nexus tomo compliant) .nx
"""

from __future__ import annotations

import logging
import os

from tqdm import tqdm

from tomoscan.esrf.scan.fluoscan import FluoTomoScan

from nxtomo import NXtomo
from nxtomo.nxobject.nxdetector import ImageKey

from nxtomomill import utils
from nxtomomill.io.config.fluoconfig import TomoFluoConfig

_logger = logging.getLogger(__name__)

__all__ = [
    "from_fluo_to_nx",
]


def from_fluo_to_nx(
    configuration: TomoFluoConfig, progress: tqdm | None = None
) -> tuple:
    """
    Converts an fluo-tomo tiff files to a nexus file.
    For now duplicates data.

    :param configuration: configuration to use to process the data
    :param progress: if provided then will be updated with conversion progress
    :return: (nexus_file, entry)
    """
    if configuration.input_folder is None:
        raise ValueError("input_folder should be provided")
    if not os.path.isdir(configuration.input_folder):
        raise OSError(f"{configuration.input_folder} is not a valid folder path")

    if configuration.output_file is None:
        raise ValueError("output_file should be provided")

    if configuration.detectors is None:
        raise ValueError("Detector names should be provided.")

    fileout_h5 = utils.get_file_name(
        file_name=configuration.output_file,
        extension=configuration.file_extension,
        check=True,
    )

    scan = FluoTomoScan(
        scan=configuration.input_folder,
        dataset_basename=configuration.dataset_basename,
        detectors=configuration.detectors,
    )

    if progress is not None:
        progress.set_description("fluo2nx")
        progress.total = len(scan.el_lines)
        progress.n = 0

    _logger.info(f"Fluo lines preset in dataset are {scan.el_lines}")

    entry_list = []
    for element, lines in scan.el_lines.items():
        if progress is not None:
            progress.set_postfix_str(f"elmt - {element}")
            line_progress = tqdm(
                desc=f"elmt: {element} - line: ", position=1, leave=False
            )
            line_progress.total = len(lines)
        else:
            line_progress = None
        for i_line, line in enumerate(lines):
            if line_progress is not None:
                line_progress.set_postfix_str(f"elmt: {element} - line: {line}")

            for det in scan.detectors:
                elmt_line_data = scan.load_data(det, element=element, line_ind=i_line)
                my_nxtomo = NXtomo()
                my_nxtomo.instrument.detector.data = elmt_line_data
                my_nxtomo.instrument.detector.image_key_control = [
                    ImageKey.PROJECTION
                ] * elmt_line_data.shape[0]
                my_nxtomo.sample.rotation_angle = scan.rot_angles_deg
                my_nxtomo.instrument.detector.x_pixel_size.value = scan.pixel_size
                my_nxtomo.instrument.detector.x_pixel_size.unit = "um"
                my_nxtomo.instrument.detector.y_pixel_size.value = scan.pixel_size
                my_nxtomo.instrument.detector.y_pixel_size.unit = "um"
                # define a value to sample-detector and source-sample distance. To be set to the real value in the future
                my_nxtomo.instrument.detector.distance.value = 1.0
                my_nxtomo.instrument.source.distance.value = 1.0
                my_nxtomo.energy = scan.energy

                data_path = f"{det}_{element}_{line}"
                my_nxtomo.save(
                    file_path=fileout_h5,
                    data_path=data_path,
                    overwrite=configuration.overwrite,
                )
                entry_list.append((fileout_h5, data_path))
            if line_progress is not None:
                line_progress.update()
        if progress is not None:
            progress.update()
    return tuple(entry_list)
