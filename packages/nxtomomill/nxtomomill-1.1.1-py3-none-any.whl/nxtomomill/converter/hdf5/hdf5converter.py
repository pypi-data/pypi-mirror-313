# coding: utf-8
"""
module to convert from (bliss) .h5 to (nexus tomo compliant) .nx
"""

from __future__ import annotations

import logging
import os
import sys

import numpy
import h5py

from tqdm import tqdm

from silx.io.url import DataUrl
from silx.io.utils import open as open_hdf5
from silx.io.utils import h5py_read_dataset
from tomoscan.io import HDF5File

from nxtomomill.converter.hdf5.acquisition.utils import group_series
from nxtomomill.converter.baseconverter import BaseConverter
from nxtomomill.converter.hdf5.acquisition.baseacquisition import _ask_for_file_removal
from nxtomomill.converter.hdf5.acquisition.pcotomoacquisition import PCOTomoAcquisition
from nxtomomill.io.acquisitionstep import AcquisitionStep
from nxtomomill.io.config import TomoHDF5Config
from nxtomomill.io.framegroup import FrameGroup
from nxtomomill.utils.hdf5 import EntryReader
from nxtomomill.utils.utils import str_datetime_to_numpy_datetime64

from .acquisition.baseacquisition import BaseAcquisition
from .acquisition.standardacquisition import StandardAcquisition
from .acquisition.utils import get_entry_type
from .acquisition.zseriesacquisition import (
    ZSeriesBaseAcquisition,
    is_pcotomo_frm_titles,
    is_z_series_frm_titles,
    is_z_series_frm_translation_z,
)
from .post_processing.dark_flat_copy import ZSeriesDarkFlatCopy

try:
    import hdf5plugin  # noqa F401
except ImportError:
    pass
# import that should be removed when h5_to_nx will be removed
from nxtomomill.converter.hdf5.utils import H5FileKeys, H5ScanTitles
from nxtomomill.settings import Tomo

H5_ROT_ANGLE_KEYS = Tomo.H5.ROT_ANGLE_KEYS
H5_VALID_CAMERA_NAMES = Tomo.H5.VALID_CAMERA_NAMES
H5_SAMPLE_X_KEYS = Tomo.H5.SAMPLE_X_KEYS
H5_SAMPLE_Y_KEYS = Tomo.H5.SAMPLE_Y_KEYS
H5_TRANSLATION_Z_KEYS = Tomo.H5.TRANSLATION_Z_KEYS
H5_ALIGNMENT_TITLES = Tomo.H5.ALIGNMENT_TITLES
H5_ACQ_EXPO_TIME_KEYS = Tomo.H5.ACQ_EXPO_TIME_KEYS
H5_X_PIXEL_SIZE = Tomo.H5.X_PIXEL_SIZE
H5_Y_PIXEL_SIZE = Tomo.H5.Y_PIXEL_SIZE
H5_DARK_TITLES = Tomo.H5.DARK_TITLES
H5_INIT_TITLES = Tomo.H5.INIT_TITLES
H5_PCOTOMO_INIT_TITLES = Tomo.H5.PCOTOMO_INIT_TITLES
H5_ZSERIE_INIT_TITLES = Tomo.H5.ZSERIE_INIT_TITLES
H5_PROJ_TITLES = Tomo.H5.PROJ_TITLES
H5_FLAT_TITLES = Tomo.H5.FLAT_TITLES
H5_REF_TITLES = H5_FLAT_TITLES
H5_TRANSLATION_Y_KEYS = Tomo.H5.TRANSLATION_Y_KEYS
H5_DIODE_KEYS = Tomo.H5.DIODE_KEYS


DEFAULT_SCAN_TITLES = H5ScanTitles(
    H5_INIT_TITLES,
    H5_ZSERIE_INIT_TITLES,
    H5_PCOTOMO_INIT_TITLES,
    H5_DARK_TITLES,
    H5_FLAT_TITLES,
    H5_PROJ_TITLES,
    H5_ALIGNMENT_TITLES,
)


DEFAULT_H5_KEYS = H5FileKeys(
    H5_ACQ_EXPO_TIME_KEYS,
    H5_ROT_ANGLE_KEYS,
    H5_VALID_CAMERA_NAMES,
    H5_SAMPLE_X_KEYS,
    H5_SAMPLE_Y_KEYS,
    H5_TRANSLATION_Z_KEYS,
    H5_TRANSLATION_Y_KEYS,
    H5_X_PIXEL_SIZE,
    H5_Y_PIXEL_SIZE,
    H5_DIODE_KEYS,
)


_logger = logging.getLogger(__name__)


class _H5ToNxConverter(BaseConverter):
    """
    Class used to convert a HDF5Config to one or several NXTomoEntry.

    :param configuration: configuration for the translation. such as the
                          input and output file, keys...
    :param input_callback: possible callback in case of missing information
    :param progress: progress bar to be updated if provided
    :param detector_sel_callback: callback for the detector selection if any

    Conversion is a two step process:

    step 1: preprocessing
    * insure configuration is valid and that we don't have "unsafe" or
      "opposite" request / rules
    * normalize input URL (complete data_file if not provided)
    * copy some frame group if requested
    * create instances of BaseAcquisition classes that will be used to write
      NXTomo entries
    * handle z series specific case

    step 2: write NXTomo entries to the output file
    """

    def __init__(
        self,
        configuration: TomoHDF5Config,
        input_callback=None,
        progress: tqdm | None = None,
        detector_sel_callback=None,
    ):
        if not isinstance(configuration, TomoHDF5Config):
            raise TypeError(
                f"configuration should be an instance of HDFConfig not {type(configuration)}"
            )
        self._configuration = configuration
        self._progress = progress
        self._input_callback = input_callback
        self._detector_sel_callback = detector_sel_callback
        self._acquisitions = []
        self._entries_created = []
        self._z_series_v2_v3: list[list[ZSeriesBaseAcquisition]] = []
        # bliss z-series for version 2 and 3. Can be used for post-processing
        self.preprocess()

    @property
    def configuration(self):
        return self._configuration

    @property
    def progress(self):
        return self._progress

    @property
    def input_callback(self):
        return self._input_callback

    @property
    def detector_sel_callback(self):
        return self._detector_sel_callback

    @property
    def entries_created(self) -> tuple:
        """tuple of entries created. Each element is provided as
        (output_file, entry)"""
        return tuple(self._entries_created)

    @property
    def acquisitions(self):
        return self._acquisitions

    def preprocess(self):
        self._preprocess_urls()
        self._check_conversion_is_possible()
        if self.configuration.is_using_titles:
            self._convert_entries_and_sub_entries_to_urls()
            self.build_acquisition_classes_frm_titles()
        else:
            self.configuration.clear_entries_and_subentries()
            self.build_acquisition_classes_frm_urls()
        self._z_series_v2_v3 = self._handle_zseries()

    def _handle_zseries(self):
        # for z series we have a "master" acquisition of type
        # ZSeriesBaseAcquisition. But this is used only to build
        # the acquisition sequence. To write we use the z series
        # "sub_acquisitions" which are instances of "StandardAcquisition"
        acquisitions = []
        z_series_v2_to_v3 = []
        # self._zserie_acq_to_acq = {}
        for acquisition in self.acquisitions:
            if isinstance(acquisition, StandardAcquisition):
                acquisitions.append(acquisition)
            elif isinstance(acquisition, ZSeriesBaseAcquisition):
                sub_acquisitions = acquisition.get_standard_sub_acquisitions()
                acquisitions.extend(sub_acquisitions)
                for sub_acquisition in sub_acquisitions:
                    z_series_v2_to_v3 = group_series(
                        acquisition=sub_acquisition, list_of_series=z_series_v2_to_v3
                    )
            else:
                raise TypeError(f"Acquisition type {type(acquisition)} not handled")
        self._acquisitions = acquisitions
        return z_series_v2_to_v3

    def convert(self):
        mess_conversion = f"start conversion from {self.configuration.input_file} to {self.configuration.output_file}"
        if self.progress is not None:
            # in the case we want to print progress
            sys.stdout.write(mess_conversion)
            sys.stdout.flush()
        else:
            _logger.info(mess_conversion)

        self._entries_created = self.write()
        return self._entries_created

    def build_acquisition_classes_frm_urls(self):
        """
        Build acquisitions classes from the url definition

        :return:
        """
        self.configuration.check_tomo_n = False
        # when building from urls `tomo_n` has no meaning
        if self.configuration.is_using_titles:
            raise ValueError("Configuration specify that titles should be used")
        assert self.configuration.output_file is not None, "output_file requested"
        data_frame_grps = self.configuration.data_frame_grps
        # step 0: copy some urls instead if needed
        # update copy parameter
        for frame_grp in data_frame_grps:
            if frame_grp.copy is None:
                frame_grp.copy = self.configuration.default_copy_behavior

        # step 1: if there is no init FrameGroup create an empty one because
        # this is requested
        if len(data_frame_grps) == 0:
            return
        elif data_frame_grps[0].frame_type is not AcquisitionStep.INITIALIZATION:
            data_frame_grps = [
                FrameGroup(frame_type=AcquisitionStep.INITIALIZATION, url=None),
            ]
            data_frame_grps.extend(self.configuration.data_frame_grps)
            self.configuration.data_frame_grps = data_frame_grps

        # step 2: treat FrameGroups
        root_acquisition = None
        start_index = 0
        require_pcotomo_expected_nx_tomo = False
        for frame_grp in data_frame_grps:
            # handle frame_type == init
            if frame_grp.frame_type is AcquisitionStep.INITIALIZATION:
                if require_pcotomo_expected_nx_tomo is True:
                    _logger.warning(
                        f"Fail to retrieve expected number of nxtomo for {root_acquisition}"
                    )
                require_pcotomo_expected_nx_tomo = False
                from nxtomomill.io.framegroup import filter_acqui_frame_type

                acqui_projs_fg = filter_acqui_frame_type(
                    init=frame_grp,
                    sequences=self.configuration.data_frame_grps,
                    frame_type=AcquisitionStep.PROJECTION,
                )
                acqui_projs_urls = tuple(
                    [acqui_proj.url for acqui_proj in acqui_projs_fg]
                )

                if is_z_series_frm_translation_z(acqui_projs_urls, self.configuration):
                    root_acquisition = ZSeriesBaseAcquisition(
                        root_url=frame_grp.url,
                        configuration=self.configuration,
                        detector_sel_callback=self.detector_sel_callback,
                        start_index=start_index,
                    )
                elif is_pcotomo_frm_titles(acqui_projs_urls, self.configuration):
                    root_acquisition = PCOTomoAcquisition(
                        root_url=frame_grp.url,
                        configuration=self.configuration,
                        detector_sel_callback=self.detector_sel_callback,
                        start_index=start_index,
                    )
                    start_index += 0
                    # this will be defined with the projections
                    self._require_pcotomo_expected_nx_tomo = True

                else:
                    root_acquisition = StandardAcquisition(
                        root_url=frame_grp.url,
                        configuration=self.configuration,
                        detector_sel_callback=self.detector_sel_callback,
                        start_index=start_index,
                    )
                    start_index += root_acquisition.get_expected_nx_tomo()
                self.acquisitions.append(root_acquisition)
            # handle frame_type != init
            else:
                assert (
                    root_acquisition is not None
                ), "processing error. No active root acquisition"
                root_acquisition.register_step(
                    url=frame_grp.url,
                    entry_type=frame_grp.frame_type,
                    copy_frames=frame_grp.copy,
                )

                # in case of z we append an index according to if
                # is already registered or not
                if isinstance(root_acquisition, ZSeriesBaseAcquisition):
                    with EntryReader(frame_grp.url) as entry:
                        z = root_acquisition.get_z(entry)
                        if z not in self._acquisitions:
                            start_index += 1

    def build_acquisition_classes_frm_titles(self):
        """
        Build Acquisition classes that will be used for conversion.
        Usually one Acquisition class will be instantiated per node (h5Group)
        to convert.
        """
        # insert missing z entry title in the common entry title
        scan_init_titles = list(self.configuration.init_titles)
        for title in self.configuration.zserie_init_titles:
            if title not in scan_init_titles:
                scan_init_titles.append(title)

        self.z_series_v3 = []
        with open_hdf5(self.configuration.input_file) as h5d:

            def sort_fct(node_name: str):
                """
                sort the scan according to the 'start_time parameter'. If fails keep the original order.
                If a node has the 'is_rearranged' attribute then skip sort and keep the original sequence.
                """
                #
                node_link_to_treat = h5d.get(node_name, getlink=True)

                note_to_treat = h5d.get(node_name)
                is_rearranged = note_to_treat is not None and note_to_treat.attrs.get(
                    "is_rearranged", False
                )
                # in some case the user might want to keep the order of the original sequence.
                # in this case we expect some preprocessing to be done and which has tag the node with the 'is_rearranged' attribute
                if is_rearranged:
                    return False
                else:
                    node = h5d.get(node_name)
                    if node is not None:
                        # node can be None in the case of a broken link
                        start_time = node.get("start_time", None)
                    else:
                        _logger.warning(f"Broken link at {node_name}")
                        start_time = None

                    if start_time is not None:
                        start_time = h5py_read_dataset(start_time)
                        return str_datetime_to_numpy_datetime64(start_time)
                    elif isinstance(
                        node_link_to_treat, (h5py.ExternalLink, h5py.SoftLink)
                    ):
                        return float(node_link_to_treat.path.split("/")[-1])
                    else:
                        # we expect to have node names like (1.1, 2.1...)
                        return float(node_name)

            groups = list(h5d.keys())
            try:
                groups.sort(key=sort_fct)
            except numpy.core._exceptions._UFuncNoLoopError:
                raise ValueError(
                    "Fail to order according to 'start_time'. Probably not all scans have a 'start_time' dataset"
                )

            # step 1: pre processing: group scan together
            if self.progress is not None:
                progress_read = tqdm(desc="read sequences")
                progress_read.total = len(groups)
            else:
                progress_read = None
            acquisitions = []
            # TODO: acquisition should refer to an url
            # list of acquisitions. Once process each of those acquisition will
            # create one 'scan'
            current_acquisition = None
            start_index = 0
            require_pcotomo_expected_nx_tomo = False
            for group_name in groups:
                _logger.debug(f"parse {group_name}")
                if progress_read is not None:
                    progress_read.update()

                try:
                    entry = h5d[group_name]
                except KeyError:
                    # case the key doesn't exist. Usual use case is that a bliss scan has been canceled
                    _logger.warning(
                        f"Unable to open {group_name} from {h5d.name}. Did the scan was canceled ? (Most likely). Skip this entry"
                    )
                    continue

                # improve handling of External (this is the case of proposal files)
                if isinstance(h5d.get(group_name, getlink=True), h5py.ExternalLink):
                    external_link = h5d.get(group_name, getlink=True)
                    file_path = external_link.filename
                    data_path = external_link.path
                    if not os.path.isabs(file_path):
                        file_path = os.path.abspath(
                            os.path.join(
                                os.path.dirname(self.configuration.input_file),
                                file_path,
                            )
                        )
                else:
                    file_path = self.configuration.input_file
                    data_path = entry.name

                url = DataUrl(
                    file_path=file_path,
                    data_path=data_path,
                    scheme="silx",
                    data_slice=None,
                )

                entry_type = get_entry_type(url=url, configuration=self.configuration)
                if entry_type is AcquisitionStep.INITIALIZATION:
                    if require_pcotomo_expected_nx_tomo is True:
                        _logger.warning(
                            f"Fail to retrieve expected number of nxtomo for {current_acquisition}"
                        )
                    try:
                        if is_z_series_frm_titles(
                            entry=entry, configuration=self.configuration
                        ):
                            current_acquisition = ZSeriesBaseAcquisition(
                                root_url=url,
                                configuration=self.configuration,
                                detector_sel_callback=self.detector_sel_callback,
                                start_index=start_index,
                            )
                            start_index += current_acquisition.get_expected_nx_tomo()
                        elif is_pcotomo_frm_titles(
                            entry=entry, configuration=self.configuration
                        ):
                            current_acquisition = PCOTomoAcquisition(
                                root_url=url,
                                configuration=self.configuration,
                                detector_sel_callback=self.detector_sel_callback,
                                start_index=start_index,
                            )
                            start_index += 0
                            # this will be defined with the projections
                            self._require_pcotomo_expected_nx_tomo = True
                        else:
                            current_acquisition = StandardAcquisition(
                                root_url=url,
                                configuration=self.configuration,
                                detector_sel_callback=self.detector_sel_callback,
                                start_index=start_index,
                            )
                            start_index += current_acquisition.get_expected_nx_tomo()
                    except Exception as e:
                        raise e
                        if self._ignore_entry_frm_titles(group_name):
                            continue
                        else:
                            raise e
                    if self._ignore_entry_frm_titles(group_name):
                        current_acquisition = None
                        continue

                    acquisitions.append(current_acquisition)
                # continue "standard" tomo dataset handling
                elif current_acquisition is not None and not self._ignore_sub_entry(
                    url
                ):
                    current_acquisition.register_step(
                        url=url,
                        entry_type=entry_type,
                        copy_frames=self.configuration.default_copy_behavior,
                    )
                    # in case of z we append an index according to if
                    # is already registered or not
                    if isinstance(current_acquisition, ZSeriesBaseAcquisition):
                        with EntryReader(url) as entry:
                            z = current_acquisition.get_z(entry)
                            if z not in self._acquisitions:
                                start_index += start_index

                    if require_pcotomo_expected_nx_tomo:
                        if entry_type is AcquisitionStep.PROJECTION:
                            nb_loop = current_acquisition.get_nb_loop(url)
                            nb_tomo = current_acquisition.get_nb_tomo(url)
                            if nb_loop is not None and nb_tomo is not None:
                                start_index += int(nb_loop) * int(nb_tomo)
                                require_pcotomo_expected_nx_tomo = False

                else:
                    _logger.info(f"ignore entry {entry}")

            self._acquisitions = acquisitions

    def _ignore_entry_frm_titles(self, group_name):
        if self.configuration.entries is None:
            return False
        else:
            if not group_name.startswith("/"):
                group_name = "/" + group_name
            for entry in self.configuration.entries:
                if group_name == entry.data_path():
                    return False
            return True

    def _ignore_sub_entry(self, sub_entry_url: DataUrl | None):
        """
        :return: True if the provided sub_entry should be ignored
        """
        if sub_entry_url is None:
            return False
        if not isinstance(sub_entry_url, DataUrl):
            raise TypeError(
                f"sub_entry_url is expected to be a DataUrl not {type(sub_entry_url)}"
            )
        if self.configuration.sub_entries_to_ignore is None:
            return False

        sub_entry_fp = sub_entry_url.file_path()
        sub_entry_dp = sub_entry_url.data_path()
        for entry in self.configuration.sub_entries_to_ignore:
            assert isinstance(entry, DataUrl)
            if entry.file_path() == sub_entry_fp and entry.data_path() == sub_entry_dp:
                return True
        return False

    def write(self):
        res = []

        acq_str = [str(acq) for acq in self.acquisitions]
        acq_str.insert(
            0, f"parsing finished. {len(self.acquisitions)} acquisitions found"
        )
        _logger.debug("\n   - ".join(acq_str))
        if len(self.acquisitions) == 0:
            _logger.warning(
                "No valid acquisitions have been found. Maybe no "
                "init (z-series) titles have been found. You can "
                "provide more."
            )

        if self.progress is not None:
            progress_write = tqdm(desc="write NXtomos")
            progress_write.total = len(self.acquisitions)
        else:
            progress_write = None

        # write nx_tomo per acquisition
        has_single_acquisition_in_file = len(self.acquisitions) == 1 and isinstance(
            self.acquisitions, PCOTomoAcquisition
        )
        divide_into_sub_files = self.configuration.bam_single_file or not (
            self.configuration.single_file is False and has_single_acquisition_in_file
        )

        acquisition_to_nxtomo: dict[ZSeriesBaseAcquisition, tuple[str] | None] = {}
        for acquisition in self.acquisitions:
            if self._ignore_sub_entry(acquisition.root_url):
                acquisition_to_nxtomo[acquisition] = None
                continue

            try:
                new_entries = acquisition.write_as_nxtomo(
                    shift_entry=acquisition.start_index,
                    input_file_path=self.configuration.input_file,
                    request_input=self.configuration.request_input,
                    input_callback=self.input_callback,
                    divide_into_sub_files=divide_into_sub_files,
                )
            except Exception as e:
                if self.configuration.raises_error:
                    raise e
                else:
                    _logger.error(
                        f"Fails to write {str(acquisition.root_url)}. Error is {str(e)}"
                    )
                    acquisition_to_nxtomo[acquisition] = None
            else:
                res.extend(new_entries)
                acquisition_to_nxtomo[acquisition] = new_entries
            if progress_write is not None:
                progress_write.update()

        # post processing on nxtomos
        for series in self._z_series_v2_v3:
            self._post_process_series(series, acquisition_to_nxtomo)

        # if we created one file per entry then create a master file with link to those entries
        if (
            self.configuration.single_file is False and divide_into_sub_files
        ) and not self.configuration.no_master_file:
            _logger.info(f"create link in {self.configuration.output_file}")
            for en_output_file, entry in res:
                with HDF5File(self.configuration.output_file, "a") as master_file:
                    link_file = os.path.relpath(
                        en_output_file,
                        os.path.dirname(self.configuration.output_file),
                    )
                    master_file[entry] = h5py.ExternalLink(link_file, entry)

        return tuple(res)

    def _check_conversion_is_possible(self):
        """Insure minimalistic information are provided"""
        if self.configuration.is_using_titles:
            if self.configuration.input_file is None:
                raise ValueError("input file should be provided")
            if not os.path.isfile(self.configuration.input_file):
                raise ValueError(
                    f"Given input file does not exists: {self.configuration.input_file}"
                )
            if not h5py.is_hdf5(self.configuration.input_file):
                raise ValueError("Given input file is not an hdf5 file")

        if self.configuration.input_file == self.configuration.output_file:
            raise ValueError("input and output file are the same")

        output_file = self.configuration.output_file
        dir_name = os.path.dirname(os.path.abspath(output_file))
        if not os.path.exists(dir_name):
            os.makedirs(os.path.dirname(os.path.abspath(output_file)))
        elif os.path.exists(output_file):
            if self.configuration.overwrite is True:
                _logger.warning(f"{output_file} will be removed")
                _logger.info(f"remove {output_file}")
                os.remove(output_file)
            elif not _ask_for_file_removal(output_file):
                raise OSError(f"unable to overwrite {output_file}, exit")
            else:
                os.remove(output_file)
        if not os.access(dir_name, os.W_OK):
            raise OSError(f"You don't have rights to write on {dir_name}")

    def _convert_entries_and_sub_entries_to_urls(self):
        if self.configuration.entries is not None:
            urls = self.configuration.entries
            entries = self._upgrade_urls(
                urls=urls, input_file=self.configuration.input_file
            )
            self.configuration.entries = entries
        if self.configuration.sub_entries_to_ignore is not None:
            urls = self.configuration.sub_entries_to_ignore
            entries = self._upgrade_urls(
                urls=urls, input_file=self.configuration.input_file
            )
            self.configuration.sub_entries_to_ignore = entries

    def _preprocess_urls(self):
        """
        Update darks, flats, projections and alignments urls if
        no file path is provided
        """
        self.configuration.data_frame_grps = self._upgrade_frame_grp_urls(
            frame_grps=self.configuration.data_frame_grps,
            input_file=self.configuration.input_file,
        )

    def _post_process_series(
        self,
        series: list[BaseAcquisition],
        acquisition_to_nxtomo: dict[BaseAcquisition, tuple | None],
    ):
        dark_flat_copy = ZSeriesDarkFlatCopy(
            series=series, acquisition_to_nxtomo=acquisition_to_nxtomo
        )
        dark_flat_copy.run()

    @staticmethod
    def _upgarde_url(url: DataUrl, input_file: str) -> DataUrl:
        if url is not None and url.file_path() in (None, ""):
            if input_file in (None, str):
                raise ValueError(
                    f"file_path for url {url.path()} is not provided and no input_file provided either."
                )
            else:
                return DataUrl(
                    file_path=input_file,
                    scheme="silx",
                    data_slice=url.data_slice(),
                    data_path=url.data_path(),
                )
        else:
            return url

    @staticmethod
    def _upgrade_frame_grp_urls(frame_grps: tuple, input_file: str | None) -> tuple:
        """
        Upgrade all Frame Group DataUrl which did not contain a file_path to
         reference the input_file
        """
        if input_file is not None and not h5py.is_hdf5(input_file):
            raise ValueError(f"{input_file} is not a h5py file")
        for frame_grp in frame_grps:
            frame_grp.url = _H5ToNxConverter._upgarde_url(frame_grp.url, input_file)
        return frame_grps

    @staticmethod
    def _upgrade_urls(urls: tuple, input_file: str | None) -> tuple:
        """
        Upgrade all DataUrl which did not contain a file_path to reference
        the input_file
        """
        if input_file is not None and not h5py.is_hdf5(input_file):
            raise ValueError(f"{input_file} is not a h5py file")
        return tuple([_H5ToNxConverter._upgarde_url(url, input_file) for url in urls])


def from_h5_to_nx(
    configuration: TomoHDF5Config,
    input_callback=None,
    progress: tqdm | None = None,
    detector_sel_callback=None,
):
    """
    convert a bliss file to a set of NXtomo

    :param configuration: configuration for the translation. such as the
                          input and output file, keys...
    :param input_callback: possible callback in case of missing information
    :param progress: progress bar to be updated if provided
    :param detector_sel_callback: callback for the detector selection if any
    :return: tuple of created NXtomo as (output_file, data_path)
    """
    converter = _H5ToNxConverter(
        configuration=configuration,
        input_callback=input_callback,
        progress=progress,
        detector_sel_callback=detector_sel_callback,
    )
    return converter.convert()


def get_bliss_tomo_entries(input_file_path: str, configuration: TomoHDF5Config):
    """.
    Return the set of entries at root that match bliss entries.
    Used by tomwer for example.

    :param input_file_path: path of the file to browse
    :param TomoHDF5Config configuration: configuration of the conversion. This way user can define title to be used or frame groups

    Warning: entries can be external links (in the case of the file beeing a proposal file)
    """
    if not isinstance(configuration, TomoHDF5Config):
        raise TypeError("configuration is expected to be a HDF5Config")

    with open_hdf5(input_file_path) as h5d:
        acquisitions = []

        for group_name in h5d.keys():
            _logger.debug(f"parse {group_name}")
            entry = h5d[group_name]
            # improve handling of External (this is the case of proposal files)
            if isinstance(h5d.get(group_name, getlink=True), h5py.ExternalLink):
                external_link = h5d.get(group_name, getlink=True)
                file_path = external_link.filename
                data_path = external_link.path
            else:
                file_path = input_file_path
                data_path = entry.name
                if not data_path.startswith("/"):
                    data_path = "/" + data_path
            url = DataUrl(file_path=file_path, data_path=data_path)
            if configuration.is_using_titles:
                # if use title take the ones corresponding to init
                entry_type = get_entry_type(url=url, configuration=configuration)
                if entry_type is AcquisitionStep.INITIALIZATION:
                    acquisitions.append(group_name)
            else:
                # check if the entry fit one of the data_frame_grps
                # with an init status
                possible_url_file_path = [
                    os.path.abspath(url.file_path()),
                    url.file_path(),
                ]
                if configuration.output_file not in ("", None):
                    possible_url_file_path.append(
                        os.path.relpath(
                            url.file_path(), os.path.dirname(configuration.output_file)
                        )
                    )
                for frame_grp in configuration.data_frame_grps:
                    if frame_grp.frame_type is AcquisitionStep.INITIALIZATION:
                        if (
                            frame_grp.url.file_path() in possible_url_file_path
                            and frame_grp.data_path() == url.data_path()
                        ):
                            acquisitions.append(entry.name)

        return acquisitions
